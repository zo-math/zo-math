"""Validate that a configured QMD article is ready to enter Human Review.

This gate sits between successful automated render checks and Human Review.  It
checks production invariants that are intentionally outside the core checker:
project navigation integration, required function-graph source/render chains,
profile-to-artifact consistency, recorded automated evidence, and explicit
verification of central semantic relations.

The command never accepts, publishes, stages, commits, or edits content.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

try:
    import yaml
except ImportError:  # Reported with a stable exit code.
    yaml = None

from zo_artifact_freshness import FreshnessError, evaluate_artifact_freshness
from zo_qmd_config import ProjectConfigError, discover_project_config
from zo_qmd_core import qmd_image_records, split_qmd_front_matter
from zo_pdf_contract import (
    CANONICAL_PDF_PIPELINE_INPUTS,
    pdf_build_receipt_path,
    validate_pdf_build_receipt,
    write_pdf_build_receipt,
)


REVIEW_READY_VERSION = 5
SESSION_MANIFEST_VERSION = 3
VISUAL_MEASUREMENT_VERSION = 4
EXIT_OK = 0
EXIT_FAILED = 1
EXIT_USAGE = 2
EXIT_MISSING_TOOL = 3
VALID_AUTOMATED_RESULTS = {"PASS", "PASS_WITH_WARNINGS"}
RELATION_TERMS = (
    "bảo toàn",
    "phụ thuộc vào",
    "làm mất",
    "xác định được từ",
    "khôi phục được từ",
    "giữ nguyên",
    "giữ độ lớn",
)


@dataclass(frozen=True)
class ReviewCheck:
    name: str
    passed: bool
    message: str
    path: str | None = None


class ReviewReadyError(RuntimeError):
    """Raised when review readiness cannot be determined safely."""


def _run(
    command: Sequence[str], cwd: Path
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(command),
        cwd=cwd,
        check=False,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )


def _repo_root(raw: str | None) -> Path:
    git = shutil.which("git")
    if git is None:
        raise ReviewReadyError("Không tìm thấy git trong PATH.")
    start = Path(raw or ".").expanduser().resolve()
    location = start if start.is_dir() else start.parent
    result = _run([git, "-C", str(location), "rev-parse", "--show-toplevel"], location)
    if result.returncode != 0:
        raise ReviewReadyError(
            result.stderr.strip()
            or result.stdout.strip()
            or f"Không tìm thấy repository từ {start}."
        )
    return Path(result.stdout.strip()).resolve()


def _relative_to_root(root: Path, raw: str) -> Path:
    candidate = Path(raw).expanduser()
    resolved = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    try:
        return resolved.relative_to(root)
    except ValueError as exc:
        raise ReviewReadyError(f"Đường dẫn nằm ngoài repository: {raw}") from exc


def _load_yaml(path: Path, label: str) -> dict[str, Any]:
    if yaml is None:
        raise ReviewReadyError("Thiếu dependency PyYAML.")
    if not path.is_file():
        raise ReviewReadyError(f"Không tìm thấy {label}: {path}")
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise ReviewReadyError(f"Không đọc được {label} {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ReviewReadyError(f"{label} phải là YAML mapping: {path}")
    return value


def _mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _truthy(value: Any) -> bool:
    return value is True


def _markdown_heading_titles(body: str) -> list[str]:
    """Return real Markdown H1-H6 titles while ignoring fenced code blocks."""
    titles: list[str] = []
    fence_char: str | None = None
    fence_len = 0
    for line in body.splitlines():
        stripped = line.lstrip()
        fence = re.match(r"^(`{3,}|~{3,})", stripped)
        if fence_char is not None:
            if fence and fence.group(1)[0] == fence_char and len(fence.group(1)) >= fence_len:
                fence_char = None
                fence_len = 0
            continue
        if fence:
            fence_char = fence.group(1)[0]
            fence_len = len(fence.group(1))
            continue
        heading = re.match(r"^\s{0,3}#{1,6}(?!#)\s+(.+?)\s*$", line)
        if heading:
            titles.append(re.sub(r"\s+\{[^{}]*\}\s*$", "", heading.group(1)).strip().casefold())
    return titles


def _markdown_h2_titles(body: str) -> list[str]:
    """Return real Markdown H2 titles while ignoring fenced code blocks."""

    titles: list[str] = []
    fence_char: str | None = None
    fence_len = 0
    for line in body.splitlines():
        stripped = line.lstrip()
        fence = re.match(r"^(`{3,}|~{3,})", stripped)
        if fence_char is not None:
            if fence and fence.group(1)[0] == fence_char and len(fence.group(1)) >= fence_len:
                fence_char = None
                fence_len = 0
            continue
        if fence:
            fence_char = fence.group(1)[0]
            fence_len = len(fence.group(1))
            continue
        heading = re.match(r"^\s*##(?!#)\s+(.+?)\s*$", line)
        if not heading:
            continue
        title = re.sub(r"\s+\{[^{}]*\}\s*$", "", heading.group(1)).strip().casefold()
        titles.append(title)
    return titles


def _empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, dict)):
        return not value
    return False




def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _path_fingerprint(root: Path, relative: Path) -> str:
    path = root / relative
    if path.is_symlink():
        return "symlink:" + str(path.readlink())
    if path.is_file():
        return "sha256:" + _sha256_file(path)
    if path.exists():
        return "directory"
    return "missing"


def _git_text(root: Path, *arguments: str) -> str:
    result = _run(["git", "-C", str(root), *arguments], root)
    if result.returncode != 0:
        raise ReviewReadyError(
            result.stderr.strip() or result.stdout.strip() or "Git command failed."
        )
    return result.stdout.strip()


def _git_dirty_paths(root: Path) -> list[Path]:
    changed = _git_text(root, "diff", "--name-only", "HEAD", "--")
    untracked = _git_text(root, "ls-files", "--others", "--exclude-standard")
    values = {line.strip() for line in changed.splitlines() if line.strip()}
    values.update(line.strip() for line in untracked.splitlines() if line.strip())
    return [Path(value) for value in sorted(values)]


def _path_is_within(path: Path, parent: Path) -> bool:
    if path == parent:
        return True
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _agents_chain(root: Path, target: Path) -> list[Path]:
    absolute = root / target
    current = absolute.parent if absolute.suffix else absolute
    relative_parent = current.resolve().relative_to(root.resolve())
    candidates = [root]
    cursor = root
    for part in relative_parent.parts:
        cursor /= part
        candidates.append(cursor)
    return [
        candidate.relative_to(root) / "AGENTS.md"
        for candidate in candidates
        if (candidate / "AGENTS.md").is_file()
    ]


def _expected_authority_records(root: Path, target: Path, config: Any) -> list[dict[str, Any]]:
    """Return the configured effective authority closure and reference inventory."""

    records: list[dict[str, Any]] = []
    seen: set[Path] = set()

    def add(raw: str | Path, role: str, reason: str, *, lock: bool) -> None:
        relative = _relative_to_root(root, str(raw))
        if relative in seen:
            return
        if not lock and not (root / relative).is_file():
            return
        seen.add(relative)
        records.append(
            {
                "path": relative,
                "role": role,
                "reason": reason,
                "lock": lock,
            }
        )

    for path in _agents_chain(root, target):
        add(path, "governing_required", "agents_chain", lock=True)
    add(config.config_path, "governing_required", "project_config", lock=True)

    registry = config.raw.get("authority_registry", {})
    if not isinstance(registry, dict):
        registry = {}

    for item in registry.get("governing_required", []):
        if isinstance(item, dict) and item.get("path"):
            add(str(item["path"]), "governing_required", str(item.get("reason") or "configured_governing_authority"), lock=True)

    for item in registry.get("provenance_required", []):
        if isinstance(item, dict) and item.get("path"):
            add(str(item["path"]), "provenance_required", str(item.get("reason") or "configured_provenance"), lock=True)

    article_type = config.article_type_for(target)
    policy = _extension_policy(config.raw, article_type.id) if article_type is not None else {}
    graph_required = _truthy(_mapping(policy.get("function_graph")).get("required"))
    for item in registry.get("conditional_required", []):
        if not isinstance(item, dict) or not item.get("path"):
            continue
        condition = str(item.get("when") or "")
        if condition == "function_graph_required" and graph_required:
            add(str(item["path"]), "conditional_required", str(item.get("reason") or condition), lock=True)

    for item in registry.get("reference_only", []):
        if isinstance(item, dict) and item.get("path"):
            add(str(item["path"]), "reference_only", str(item.get("reason") or "optional_reference"), lock=False)

    if not registry:
        references = config.raw.get("references", {})
        if isinstance(references, dict):
            for values in references.values():
                if not isinstance(values, list):
                    continue
                for value in values:
                    if isinstance(value, str) and value.strip():
                        add(config.project_root / Path(value), "governing_required", "legacy_reference_set", lock=True)

    return records


def _canonical_scope(root: Path, target: Path, config: Any, policy: Mapping[str, Any]) -> list[Path]:
    lifecycle = _mapping(policy.get("lifecycle"))
    if not _truthy(lifecycle.get("auto_scope")):
        return []
    paths: list[Path] = [target, config.profile_path_for(target)]
    article_type = config.article_type_for(target)
    if article_type is not None and article_type.id == "function_article":
        paths.append(target.with_suffix(".pdf"))
        paths.append(config.project_root / "_figures" / target.stem)
    navigation = _mapping(policy.get("navigation"))
    if _truthy(navigation.get("explicit_sidebar_required")):
        raw_quarto = navigation.get("quarto_config", "_quarto.yml")
        if isinstance(raw_quarto, str) and raw_quarto.strip():
            paths.append(_relative_to_root(root, raw_quarto.strip()))
    result: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        if path in seen:
            continue
        seen.add(path)
        result.append(path)
    return result


def _session_path(root: Path, target: Path, raw: str | None) -> Path:
    if raw is None:
        resolved = root / "_audit" / f"{target.stem}_session.json"
    else:
        candidate = Path(raw).expanduser()
        resolved = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    audit = (root / "_audit").resolve()
    try:
        resolved.relative_to(audit)
    except ValueError as exc:
        raise ReviewReadyError("Session manifest phải là JSON bên trong _audit/.") from exc
    if resolved.suffix.lower() != ".json":
        raise ReviewReadyError("Session manifest phải là JSON bên trong _audit/.")
    return resolved


def _load_json_mapping(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file():
        raise ReviewReadyError(f"Không tìm thấy {label}: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ReviewReadyError(f"Không đọc được {label} {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ReviewReadyError(f"{label} phải là JSON object: {path}")
    return value


def _extension_policy(config_raw: Mapping[str, Any], article_type: str) -> dict[str, Any]:
    extensions = _mapping(config_raw.get("extensions"))
    gate = _mapping(extensions.get("human_review_gate"))
    if not _truthy(gate.get("enabled")):
        return {}
    article_types = _mapping(gate.get("article_types"))
    policy = _mapping(article_types.get(article_type))
    return policy


def _normalize_href(value: str) -> str:
    text = value.strip().replace("\\", "/")
    while text.startswith("./"):
        text = text[2:]
    return text.lstrip("/")


def _collect_hrefs(value: Any) -> list[str]:
    result: list[str] = []
    if isinstance(value, dict):
        href = value.get("href")
        if isinstance(href, str) and href.strip():
            result.append(_normalize_href(href))
        for child in value.values():
            result.extend(_collect_hrefs(child))
    elif isinstance(value, list):
        for child in value:
            result.extend(_collect_hrefs(child))
    return result


def _quarto_output_dir(root: Path, quarto: Mapping[str, Any]) -> Path:
    project = _mapping(quarto.get("project"))
    raw = project.get("output-dir", "_site")
    if not isinstance(raw, str) or not raw.strip():
        raise ReviewReadyError("project.output-dir trong _quarto.yml không hợp lệ.")
    path = Path(raw.strip().replace("\\", "/"))
    if path.is_absolute() or ".." in path.parts:
        raise ReviewReadyError("project.output-dir phải là đường dẫn tương đối an toàn.")
    return root / path


def _rendered_html_path(root: Path, target: Path, quarto: Mapping[str, Any]) -> Path:
    return _quarto_output_dir(root, quarto) / target.with_suffix(".html")


def _resolve_qmd_asset(root: Path, qmd: Path, target: str) -> Path | None:
    cleaned = target.split("#", 1)[0].split("?", 1)[0].strip()
    if not cleaned or re.match(r"(?i)^[a-z][a-z0-9+.-]*://", cleaned):
        return None
    candidate = Path(cleaned.replace("\\", "/"))
    if candidate.is_absolute():
        absolute = root / str(candidate).lstrip("/\\")
    else:
        absolute = root / qmd.parent / candidate
    try:
        return absolute.resolve().relative_to(root.resolve())
    except ValueError:
        return None


def _graph_chains(root: Path, qmd: Path, body: str) -> list[tuple[Path, Path, Path]]:
    chains: list[tuple[Path, Path, Path]] = []
    for _, target, attrs, alt in qmd_image_records(body):
        relative = _resolve_qmd_asset(root, qmd, target)
        if relative is None or relative.suffix.lower() != ".svg":
            continue
        parts = list(relative.parts)
        if "_figures" not in parts or "svg" not in parts:
            continue
        identity = " ".join((target, attrs or "", alt or "")).casefold()
        if not any(token in identity for token in ("do_thi", "đồ thị", "do thi")):
            continue
        svg_index = len(parts) - 1 - parts[::-1].index("svg")
        src_parts = list(parts)
        pdf_parts = list(parts)
        src_parts[svg_index] = "src"
        pdf_parts[svg_index] = "pdf"
        src = Path(*src_parts).with_suffix(".tex")
        pdf = Path(*pdf_parts).with_suffix(".pdf")
        chains.append((src, pdf, relative))
    return chains


def _json_report(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _evidence_modes(root: Path, target: Path) -> tuple[set[str], list[str]]:
    """Read machine-owned check/render evidence from canonical audit paths."""

    expected = {
        "scope": Path("_audit") / f"{target.stem}_check.json",
        "render": Path("_audit") / f"{target.stem}_render.json",
    }
    modes: set[str] = set()
    errors: list[str] = []
    for mode, relative in expected.items():
        path = root / relative
        if not path.is_file():
            errors.append(f"Thiếu bằng chứng machine-owned: {relative.as_posix()}.")
            continue
        payload = _json_report(path)
        if payload is None:
            errors.append(f"Bằng chứng không phải JSON object hợp lệ: {relative.as_posix()}.")
            continue
        if payload.get("mode") != mode:
            errors.append(f"Báo cáo {relative.as_posix()} không có mode={mode}.")
            continue
        if payload.get("automated_result") not in VALID_AUTOMATED_RESULTS or payload.get("exit_code") != 0:
            errors.append(f"Báo cáo {relative.as_posix()} không đạt PASS/PASS_WITH_WARNINGS với exit_code=0.")
            continue
        scope = payload.get("scope", [])
        if not isinstance(scope, list) or target.as_posix() not in scope:
            errors.append(f"Báo cáo {relative.as_posix()} không bao phủ {target.as_posix()}.")
            continue
        modes.add(mode)
    return modes, errors


def _png_dimensions(path: Path) -> tuple[int, int] | None:
    """Read PNG dimensions without adding an image-library dependency."""

    try:
        with path.open("rb") as handle:
            header = handle.read(24)
    except OSError:
        return None
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        return None
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    if width <= 0 or height <= 0:
        return None
    return width, height


def _strict_int(value: Any) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def _pdf_page_count(root: Path, target: Path) -> tuple[int | None, str | None]:
    """Read the canonical article PDF page count with pdfinfo."""

    pdf_rel = target.with_suffix(".pdf")
    pdf_path = root / pdf_rel
    if not pdf_path.is_file():
        return None, f"Thiếu PDF để xác minh visual evidence: {pdf_rel.as_posix()}."
    pdfinfo = shutil.which("pdfinfo")
    if pdfinfo is None:
        return None, "Không tìm thấy pdfinfo để xác minh số trang PDF."
    result = _run([pdfinfo, str(pdf_path)], root)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        suffix = f" ({detail})" if detail else ""
        return None, f"pdfinfo không đọc được {pdf_rel.as_posix()}{suffix}."
    match = re.search(r"(?mi)^Pages:\s*(\d+)\s*$", result.stdout)
    if match is None:
        return None, f"pdfinfo không trả về số trang hợp lệ cho {pdf_rel.as_posix()}."
    pages = int(match.group(1))
    if pages <= 0:
        return None, f"PDF phải có ít nhất một trang: {pdf_rel.as_posix()}."
    return pages, None


def _machine_visual_errors(
    root: Path,
    target: Path,
    required_mobile_viewports: Sequence[int],
    required_desktop_viewports: Sequence[int],
    require_full_html_capture: bool = False,
) -> list[str]:
    """Validate machine-owned runtime viewport/overflow evidence."""

    mobile = tuple(int(width) for width in required_mobile_viewports)
    desktop = tuple(int(width) for width in required_desktop_viewports)
    required = mobile + desktop
    errors: list[str] = []
    if not mobile:
        errors.append("visual.required_mobile_viewports phải khai báo ít nhất một viewport nguyên dương.")
    if not desktop:
        errors.append("visual.required_desktop_viewports phải khai báo ít nhất một viewport nguyên dương.")
    if len(set(required)) != len(required):
        errors.append("Mobile và desktop viewport canonical không được trùng nhau.")
    if errors:
        return errors

    canonical_root = Path("_audit") / f"{target.stem}_visual"
    report_rel = canonical_root / "html_mobile_measurements.json"
    report_path = root / report_rel
    if not report_path.is_file():
        return [f"Thiếu machine-owned visual evidence: {report_rel.as_posix()}."]

    payload = _json_report(report_path)
    if payload is None:
        return [f"Visual evidence không phải JSON object hợp lệ: {report_rel.as_posix()}."]
    if payload.get("visual_measurement_version") != VISUAL_MEASUREMENT_VERSION:
        errors.append(f"Visual evidence phải có version={VISUAL_MEASUREMENT_VERSION}.")
    if payload.get("generator") != "scripts/zo_qmd_visual.ps1":
        errors.append("Visual evidence không do scripts/zo_qmd_visual.ps1 tạo.")
    if payload.get("target") != target.as_posix():
        errors.append("Visual evidence không thuộc đúng candidate hiện tại.")

    expected_html = Path("docs") / target.with_suffix(".html")
    if payload.get("rendered_html") != expected_html.as_posix():
        errors.append("Visual evidence không trỏ tới rendered HTML canonical: " + expected_html.as_posix() + ".")
    html_path = root / expected_html
    if not html_path.is_file():
        errors.append(f"Thiếu rendered HTML để xác minh visual evidence: {expected_html.as_posix()}.")
    elif payload.get("rendered_html_sha256") != _sha256_file(html_path):
        errors.append("Visual evidence stale: SHA-256 của rendered HTML đã thay đổi.")

    if payload.get("required_mobile_viewports") != list(mobile):
        errors.append("Visual evidence phải khóa đúng mobile viewports: " + ", ".join(map(str, mobile)) + ".")
    if payload.get("required_desktop_viewports") != list(desktop):
        errors.append("Visual evidence phải khóa đúng desktop viewports: " + ", ".join(map(str, desktop)) + ".")

    measurements = payload.get("measurements")
    if not isinstance(measurements, list):
        return errors + ["Visual evidence.measurements phải là list."]

    by_width: dict[int, dict[str, Any]] = {}
    for raw in measurements:
        if not isinstance(raw, dict):
            errors.append("Visual evidence.measurements chứa phần tử không phải mapping.")
            continue
        width = _strict_int(raw.get("requested_width"))
        if width is None:
            errors.append("Visual measurement thiếu requested_width nguyên hợp lệ.")
            continue
        if width in by_width:
            errors.append(f"Visual measurement lặp viewport {width}px.")
            continue
        by_width[width] = raw

    if set(by_width) != set(required):
        missing = sorted(set(required) - set(by_width))
        extra = sorted(set(by_width) - set(required))
        if missing:
            errors.append("Thiếu visual measurement cho viewport: " + ", ".join(map(str, missing)) + ".")
        if extra:
            errors.append("Có visual measurement ngoài viewport canonical: " + ", ".join(map(str, extra)) + ".")

    for width in required:
        raw = by_width.get(width)
        if raw is None:
            continue
        viewport_class = "mobile" if width in mobile else "desktop"
        if raw.get("viewport_class") != viewport_class:
            errors.append(f"Viewport {width}px: viewport_class phải là {viewport_class}.")
        inner = _strict_int(raw.get("window_inner_width"))
        client = _strict_int(raw.get("document_client_width"))
        scroll = _strict_int(raw.get("document_scroll_width"))
        overflow_px = _strict_int(raw.get("overflow_px"))
        horizontal = raw.get("horizontal_overflow")
        if inner != width:
            errors.append(f"Viewport {width}px: window.innerWidth={inner}, phải bằng {width}.")
        if client != width:
            errors.append(f"Viewport {width}px: document.clientWidth={client}, phải bằng {width}.")
        if client is None or scroll is None:
            errors.append(f"Viewport {width}px: thiếu clientWidth/scrollWidth nguyên hợp lệ.")
        elif scroll > client:
            errors.append(f"Viewport {width}px: horizontal overflow {scroll - client}px (scrollWidth={scroll} > clientWidth={client}).")
        if isinstance(horizontal, bool):
            if horizontal:
                errors.append(f"Viewport {width}px: horizontal_overflow=true.")
        else:
            errors.append(f"Viewport {width}px: horizontal_overflow phải là boolean.")
        if client is not None and scroll is not None and overflow_px != scroll - client:
            errors.append(f"Viewport {width}px: overflow_px không khớp scrollWidth-clientWidth.")
        if raw.get("passed") is not True:
            errors.append(f"Viewport {width}px: machine visual measurement không PASS.")

        expected_screenshot = canonical_root / f"html_{viewport_class}_{width}.png"
        if raw.get("screenshot") != expected_screenshot.as_posix():
            errors.append(f"Viewport {width}px: screenshot phải là {expected_screenshot.as_posix()}.")
            continue
        screenshot_path = root / expected_screenshot
        if not screenshot_path.is_file():
            errors.append(f"Thiếu screenshot machine-owned: {expected_screenshot.as_posix()}.")
            continue
        if raw.get("screenshot_sha256") != _sha256_file(screenshot_path):
            errors.append(f"Viewport {width}px: SHA-256 screenshot không khớp.")
        dimensions = _png_dimensions(screenshot_path)
        if dimensions is None:
            errors.append(f"Viewport {width}px: screenshot không phải PNG hợp lệ có IHDR.")
        else:
            if dimensions[0] != width:
                errors.append(f"Viewport {width}px: screenshot rộng {dimensions[0]}px, phải bằng {width}px.")
            requested_height = _strict_int(raw.get("requested_height"))
            if requested_height is None or dimensions[1] != requested_height:
                errors.append(f"Viewport {width}px: chiều cao screenshot {dimensions[1]}px không khớp requested_height={requested_height}.")

    if require_full_html_capture:
        segments = payload.get("html_segments")
        if not isinstance(segments, list) or not segments:
            errors.append("Visual evidence.html_segments phải là list không rỗng khi yêu cầu full HTML capture.")
        else:
            segments_by_width: dict[int, list[dict[str, Any]]] = {}
            for raw in segments:
                if not isinstance(raw, dict):
                    errors.append("Visual evidence.html_segments chứa phần tử không phải mapping.")
                    continue
                width = _strict_int(raw.get("requested_width"))
                if width is None or width not in required:
                    errors.append("HTML segment có requested_width ngoài viewport canonical.")
                    continue
                segments_by_width.setdefault(width, []).append(raw)

            if set(segments_by_width) != set(required):
                missing = sorted(set(required) - set(segments_by_width))
                extra = sorted(set(segments_by_width) - set(required))
                if missing:
                    errors.append("Thiếu full HTML segments cho viewport: " + ", ".join(map(str, missing)) + ".")
                if extra:
                    errors.append("Có full HTML segments ngoài viewport canonical: " + ", ".join(map(str, extra)) + ".")

            for width in required:
                rows = segments_by_width.get(width, [])
                if not rows:
                    continue
                viewport_class = "mobile" if width in mobile else "desktop"
                rows = sorted(rows, key=lambda item: _strict_int(item.get("segment_index")) or 0)
                indices = [_strict_int(item.get("segment_index")) for item in rows]
                if indices != list(range(1, len(rows) + 1)):
                    errors.append(f"Viewport {width}px: segment_index phải liên tục từ 1.")

                measurement = by_width.get(width, {})
                scroll_height = _strict_int(measurement.get("document_scroll_height"))
                if scroll_height is None or scroll_height <= 0:
                    errors.append(f"Viewport {width}px: thiếu document_scroll_height nguyên dương.")
                    continue

                previous_top: int | None = None
                previous_height: int | None = None
                for position, raw in enumerate(rows, start=1):
                    if raw.get("viewport_class") != viewport_class:
                        errors.append(f"Viewport {width}px segment {position}: viewport_class sai.")
                    segment_height = _strict_int(raw.get("requested_height"))
                    actual_top = _strict_int(raw.get("actual_top"))
                    raw_scroll_height = _strict_int(raw.get("document_scroll_height"))
                    if segment_height is None or segment_height <= 0:
                        errors.append(f"Viewport {width}px segment {position}: requested_height không hợp lệ.")
                        continue
                    if actual_top is None or actual_top < 0:
                        errors.append(f"Viewport {width}px segment {position}: actual_top không hợp lệ.")
                        continue
                    if raw_scroll_height != scroll_height:
                        errors.append(f"Viewport {width}px segment {position}: document_scroll_height không khớp measurement.")

                    if previous_top is None:
                        if actual_top != 0:
                            errors.append(f"Viewport {width}px: full HTML capture phải bắt đầu tại top=0.")
                    else:
                        if actual_top <= previous_top:
                            errors.append(f"Viewport {width}px: actual_top của các segment phải tăng nghiêm ngặt.")
                        elif previous_height is not None and actual_top > previous_top + previous_height:
                            errors.append(f"Viewport {width}px: full HTML segments có khoảng hở trước top={actual_top}.")

                    expected = canonical_root / f"html_{viewport_class}_{width}_part_{position:03d}.png"
                    if raw.get("screenshot") != expected.as_posix():
                        errors.append(f"Viewport {width}px segment {position}: screenshot phải là {expected.as_posix()}.")
                    else:
                        screenshot_path = root / expected
                        if not screenshot_path.is_file():
                            errors.append(f"Thiếu full HTML screenshot: {expected.as_posix()}.")
                        else:
                            if raw.get("screenshot_sha256") != _sha256_file(screenshot_path):
                                errors.append(f"Viewport {width}px segment {position}: SHA-256 screenshot không khớp.")
                            dimensions = _png_dimensions(screenshot_path)
                            if dimensions is None:
                                errors.append(f"Viewport {width}px segment {position}: PNG không hợp lệ.")
                            elif dimensions != (width, segment_height):
                                errors.append(
                                    f"Viewport {width}px segment {position}: kích thước PNG {dimensions} "
                                    f"không khớp {(width, segment_height)}."
                                )
                    previous_top = actual_top
                    previous_height = segment_height

                if previous_top is not None and previous_height is not None:
                    if previous_top + previous_height < scroll_height:
                        errors.append(
                            f"Viewport {width}px: full HTML capture chưa phủ tới cuối tài liệu "
                            f"({previous_top + previous_height} < {scroll_height})."
                        )

    pdf_rel = target.with_suffix(".pdf")
    pdf_path = root / pdf_rel
    if payload.get("rendered_pdf") != pdf_rel.as_posix():
        errors.append("Visual evidence không trỏ tới PDF canonical: " + pdf_rel.as_posix() + ".")
    if not pdf_path.is_file():
        errors.append(f"Thiếu PDF để xác minh visual evidence: {pdf_rel.as_posix()}.")
    elif payload.get("rendered_pdf_sha256") != _sha256_file(pdf_path):
        errors.append("Visual evidence stale: SHA-256 của PDF đã thay đổi.")

    page_count, page_error = _pdf_page_count(root, target)
    if page_error is not None:
        errors.append(page_error)
    elif page_count is not None:
        if payload.get("pdf_page_count") != page_count:
            errors.append(f"Visual evidence.pdf_page_count phải bằng {page_count}.")
        pdf_pages = payload.get("pdf_pages")
        if not isinstance(pdf_pages, list):
            errors.append("Visual evidence.pdf_pages phải là list.")
        else:
            by_page: dict[int, dict[str, Any]] = {}
            for raw in pdf_pages:
                if not isinstance(raw, dict):
                    errors.append("Visual evidence.pdf_pages chứa phần tử không phải mapping.")
                    continue
                page = _strict_int(raw.get("page"))
                if page is None or page <= 0:
                    errors.append("Visual PDF page record thiếu số trang nguyên dương.")
                    continue
                if page in by_page:
                    errors.append(f"Visual PDF page record lặp trang {page}.")
                    continue
                by_page[page] = raw
            expected_pages = set(range(1, page_count + 1))
            if set(by_page) != expected_pages:
                missing_pages = sorted(expected_pages - set(by_page))
                extra_pages = sorted(set(by_page) - expected_pages)
                if missing_pages:
                    errors.append("Thiếu machine-owned PDF screenshot cho trang: " + ", ".join(map(str, missing_pages)) + ".")
                if extra_pages:
                    errors.append("Có machine-owned PDF screenshot ngoài số trang hiện tại: " + ", ".join(map(str, extra_pages)) + ".")
            canonical_root = Path("_audit") / f"{target.stem}_visual"
            for page in sorted(expected_pages):
                raw = by_page.get(page)
                if raw is None:
                    continue
                expected = canonical_root / f"pdf_page_{page}.png"
                if raw.get("screenshot") != expected.as_posix():
                    errors.append(f"PDF trang {page}: screenshot phải là {expected.as_posix()}.")
                    continue
                screenshot_path = root / expected
                if not screenshot_path.is_file():
                    errors.append(f"Thiếu machine-owned PDF screenshot: {expected.as_posix()}.")
                    continue
                if raw.get("screenshot_sha256") != _sha256_file(screenshot_path):
                    errors.append(f"PDF trang {page}: SHA-256 screenshot không khớp.")
                if _png_dimensions(screenshot_path) is None:
                    errors.append(f"PDF trang {page}: screenshot không phải PNG hợp lệ có IHDR.")

    if payload.get("automated_result") != "PASS" or payload.get("exit_code") != 0:
        errors.append("Machine-owned visual report không có automated_result=PASS, exit_code=0.")
    return errors


def _self_view_errors(
    root: Path,
    profile: Mapping[str, Any],
    target: Path,
    required_mobile_viewports: Sequence[int] = (),
    required_desktop_viewports: Sequence[int] = (),
    require_pdf_page_coverage: bool = False,
    require_structured_self_review: bool = False,
    required_self_review_criteria: Mapping[str, Any] | None = None,
) -> list[str]:
    """Validate agent-owned visual self-review against machine-owned evidence."""

    self_view = _mapping(profile.get("tu_xem"))
    errors: list[str] = []
    if self_view.get("trang_thai") != "dat":
        errors.append("tu_xem.trang_thai phải là dat trước Human Review.")
    warnings = self_view.get("canh_bao", [])
    if warnings not in ([], None):
        errors.append("tu_xem.canh_bao phải rỗng trước Human Review; cảnh báo chưa xử lí phải chặn readiness.")

    canonical_root = Path("_audit") / f"{target.stem}_visual"
    report_rel = canonical_root / "html_mobile_measurements.json"
    report_path = root / report_rel
    payload = _json_report(report_path) if report_path.is_file() else None
    if payload is None:
        errors.append(f"Thiếu/không đọc được visual report để đối chiếu self-view: {report_rel.as_posix()}.")
        return errors

    evidence = self_view.get("bang_chung", [])
    if not isinstance(evidence, list):
        errors.append("tu_xem.bang_chung phải là list.")
        evidence = []
    evidence_paths: set[Path] = set()
    for raw in evidence:
        if not isinstance(raw, str) or not raw.strip():
            errors.append("tu_xem.bang_chung chứa đường dẫn không hợp lệ.")
            continue
        try:
            relative = _relative_to_root(root, raw)
        except ReviewReadyError as exc:
            errors.append(str(exc))
            continue
        if not _path_is_within(relative, canonical_root):
            errors.append(
                f"Bằng chứng self-view phải nằm dưới {canonical_root.as_posix()}/: {relative.as_posix()}."
            )
            continue
        if not (root / relative).is_file():
            errors.append(f"Thiếu bằng chứng self-view: {relative.as_posix()}.")
            continue
        evidence_paths.add(relative)

    required_base = [report_rel]
    for width in required_desktop_viewports:
        required_base.append(canonical_root / f"html_desktop_{int(width)}.png")
    for width in required_mobile_viewports:
        required_base.append(canonical_root / f"html_mobile_{int(width)}.png")
    for expected in required_base:
        if expected not in evidence_paths:
            errors.append(f"tu_xem.bang_chung phải tham chiếu {expected.as_posix()}.")

    if not require_structured_self_review:
        if require_pdf_page_coverage:
            page_count, page_error = _pdf_page_count(root, target)
            if page_error is not None:
                errors.append(page_error)
            elif page_count is not None:
                for page in range(1, page_count + 1):
                    expected = canonical_root / f"pdf_page_{page}.png"
                    if expected not in evidence_paths:
                        errors.append(f"tu_xem.bang_chung thiếu {expected.as_posix()}.")
        return errors

    criteria_policy = _mapping(required_self_review_criteria or {})

    def validate_criteria(section: Mapping[str, Any], label: str, required_ids: Sequence[str]) -> None:
        if section.get("trang_thai") != "dat":
            errors.append(f"tu_xem.{label}.trang_thai phải là dat.")
        raw_items = section.get("tieu_chi")
        if not isinstance(raw_items, list):
            errors.append(f"tu_xem.{label}.tieu_chi phải là list.")
            return
        by_id: dict[str, dict[str, Any]] = {}
        for raw in raw_items:
            if not isinstance(raw, dict):
                errors.append(f"tu_xem.{label}.tieu_chi chứa phần tử không phải mapping.")
                continue
            cid = raw.get("id")
            if not isinstance(cid, str) or not cid:
                errors.append(f"tu_xem.{label}.tieu_chi có id không hợp lệ.")
                continue
            if cid in by_id:
                errors.append(f"tu_xem.{label}.tieu_chi lặp id {cid}.")
                continue
            by_id[cid] = raw
        expected = list(required_ids)
        if list(by_id) != expected:
            errors.append(
                f"tu_xem.{label}.tieu_chi phải có đúng thứ tự ID: " + ", ".join(expected) + "."
            )
        for cid in expected:
            raw = by_id.get(cid)
            if raw is None:
                continue
            if raw.get("trang_thai") != "dat":
                errors.append(f"tu_xem.{label}.{cid}.trang_thai phải là dat.")
            basis = raw.get("can_cu")
            if not isinstance(basis, list) or not any(isinstance(x, str) and x.strip() for x in basis):
                errors.append(f"tu_xem.{label}.{cid}.can_cu phải có bằng chứng cụ thể.")
            action = raw.get("hanh_dong_sua")
            if action not in (None, "", []):
                errors.append(f"tu_xem.{label}.{cid}.hanh_dong_sua phải rỗng trước Human Review.")

    desktop_section = _mapping(self_view.get("html_desktop"))
    mobile_section = _mapping(self_view.get("html_mobile"))
    pdf_section = _mapping(self_view.get("pdf"))

    validate_criteria(
        desktop_section,
        "html_desktop",
        [str(x) for x in criteria_policy.get("html_desktop", []) if isinstance(x, str)],
    )
    validate_criteria(
        mobile_section,
        "html_mobile",
        [str(x) for x in criteria_policy.get("html_mobile", []) if isinstance(x, str)],
    )
    validate_criteria(
        pdf_section,
        "pdf",
        [str(x) for x in criteria_policy.get("pdf", []) if isinstance(x, str)],
    )

    segments = payload.get("html_segments")
    segments_by_width: dict[int, list[str]] = {}
    if isinstance(segments, list):
        for raw in segments:
            if not isinstance(raw, dict):
                continue
            width = _strict_int(raw.get("requested_width"))
            screenshot = raw.get("screenshot")
            if width is not None and isinstance(screenshot, str):
                segments_by_width.setdefault(width, []).append(screenshot)

    def validate_viewport_records(
        section: Mapping[str, Any],
        label: str,
        widths: Sequence[int],
    ) -> None:
        rows = section.get("viewports")
        if not isinstance(rows, list):
            errors.append(f"tu_xem.{label}.viewports phải là list.")
            return
        by_width: dict[int, dict[str, Any]] = {}
        for raw in rows:
            if not isinstance(raw, dict):
                errors.append(f"tu_xem.{label}.viewports chứa phần tử không phải mapping.")
                continue
            width = _strict_int(raw.get("width"))
            if width is None:
                errors.append(f"tu_xem.{label}.viewports có width không hợp lệ.")
                continue
            if width in by_width:
                errors.append(f"tu_xem.{label}.viewports lặp width={width}.")
                continue
            by_width[width] = raw
        if set(by_width) != set(int(x) for x in widths):
            errors.append(
                f"tu_xem.{label}.viewports phải khớp đúng viewport canonical: "
                + ", ".join(map(str, widths))
                + "."
            )
        for width in widths:
            raw = by_width.get(int(width))
            if raw is None:
                continue
            if raw.get("trang_thai") != "dat":
                errors.append(f"tu_xem.{label}.viewports[{width}].trang_thai phải là dat.")
            if raw.get("da_xem_den_cuoi") is not True:
                errors.append(f"tu_xem.{label}.viewports[{width}].da_xem_den_cuoi phải là true.")
            basis = raw.get("can_cu")
            expected_segments = segments_by_width.get(int(width), [])
            if not isinstance(basis, list) or basis != expected_segments:
                errors.append(
                    f"tu_xem.{label}.viewports[{width}].can_cu phải liệt kê đúng toàn bộ HTML segment "
                    "machine-owned theo thứ tự report."
                )

    validate_viewport_records(desktop_section, "html_desktop", required_desktop_viewports)
    validate_viewport_records(mobile_section, "html_mobile", required_mobile_viewports)

    if require_pdf_page_coverage:
        page_count, page_error = _pdf_page_count(root, target)
        if page_error is not None:
            errors.append(page_error)
        elif page_count is not None:
            rows = pdf_section.get("trang")
            if not isinstance(rows, list):
                errors.append("tu_xem.pdf.trang phải là list.")
            else:
                by_page: dict[int, dict[str, Any]] = {}
                for raw in rows:
                    if not isinstance(raw, dict):
                        errors.append("tu_xem.pdf.trang chứa phần tử không phải mapping.")
                        continue
                    page = _strict_int(raw.get("so"))
                    if page is None or page <= 0:
                        errors.append("tu_xem.pdf.trang có số trang không hợp lệ.")
                        continue
                    if page in by_page:
                        errors.append(f"tu_xem.pdf.trang lặp trang {page}.")
                        continue
                    by_page[page] = raw
                expected_pages = set(range(1, page_count + 1))
                if set(by_page) != expected_pages:
                    errors.append("tu_xem.pdf.trang phải có đúng một bản ghi cho mọi trang PDF.")
                for page in sorted(expected_pages):
                    raw = by_page.get(page)
                    if raw is None:
                        continue
                    if raw.get("trang_thai") != "dat":
                        errors.append(f"tu_xem.pdf.trang[{page}].trang_thai phải là dat.")
                    expected = (canonical_root / f"pdf_page_{page}.png").as_posix()
                    if raw.get("can_cu") != expected:
                        errors.append(f"tu_xem.pdf.trang[{page}].can_cu phải là {expected}.")
    return errors


def _profile_template_shape_errors(
    root: Path,
    config: Any,
    profile: Mapping[str, Any],
) -> list[str]:
    """Require the agent-owned profile to preserve the declared template schema.

    Values may change, and empty list templates remain open-ended. Mapping keys
    and the fixed self-check criterion IDs are structural and must not be
    collapsed, renamed, or replaced by ad-hoc summaries.
    """

    references = config.raw.get("references", {})
    templates = references.get("templates", []) if isinstance(references, dict) else []
    raw_template = next(
        (
            value
            for value in templates
            if isinstance(value, str)
            and Path(value).name == "ho_so_san_xuat_mac_dinh.yml"
        ),
        None,
    )
    if raw_template is None:
        return ["Không xác định được template hồ sơ sản xuất mặc định từ references.templates."]

    template_rel = config.project_root / Path(raw_template)
    template = _load_yaml(root / template_rel, "template hồ sơ sản xuất")
    errors: list[str] = []

    def walk(expected: Any, actual: Any, path: str) -> None:
        if isinstance(expected, dict):
            if not isinstance(actual, Mapping):
                errors.append(f"{path or '<root>'} phải là mapping theo template.")
                return
            missing = [key for key in expected if key not in actual]
            extra = [key for key in actual if key not in expected]
            if missing:
                errors.append(
                    f"{path or '<root>'} thiếu khóa template: "
                    + ", ".join(str(key) for key in missing)
                    + "."
                )
            if extra:
                errors.append(
                    f"{path or '<root>'} có khóa ngoài template: "
                    + ", ".join(str(key) for key in extra)
                    + "."
                )
            for key in expected:
                if key in actual:
                    child = f"{path}.{key}" if path else str(key)
                    walk(expected[key], actual[key], child)
            return

        if isinstance(expected, list):
            if not isinstance(actual, list):
                errors.append(f"{path} phải là danh sách theo template.")
                return
            if expected and isinstance(expected[0], dict):
                for index, item in enumerate(actual):
                    walk(expected[0], item, f"{path}[{index}]")
            return

    walk(template, profile, "")

    template_self = _mapping(template.get("tu_kiem_noi_dung"))
    actual_self = _mapping(profile.get("tu_kiem_noi_dung"))
    for section, expected_section in template_self.items():
        expected_map = _mapping(expected_section)
        expected_criteria = expected_map.get("tieu_chi", [])
        if not isinstance(expected_criteria, list) or not expected_criteria:
            continue
        actual_map = _mapping(actual_self.get(section))
        actual_criteria = actual_map.get("tieu_chi", [])
        if not isinstance(actual_criteria, list):
            errors.append(f"tu_kiem_noi_dung.{section}.tieu_chi phải là danh sách.")
            continue
        expected_ids = [
            item.get("id")
            for item in expected_criteria
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        ]
        actual_ids = [
            item.get("id")
            for item in actual_criteria
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        ]
        if actual_ids != expected_ids:
            errors.append(
                f"tu_kiem_noi_dung.{section}.tieu_chi phải giữ nguyên bộ ID "
                f"{expected_ids}; nhận được {actual_ids}."
            )

    return errors


def _relation_terms_present(text: str) -> list[str]:
    lowered = text.casefold()
    return [term for term in RELATION_TERMS if term.casefold() in lowered]


def _graph_core_style_errors(raw: str, tex: Path) -> list[str]:
    """Return violations of the non-negotiable self-contained graph core."""

    errors: list[str] = []

    def need(pattern: str, label: str, flags: int = 0) -> None:
        if not re.search(pattern, raw, flags):
            errors.append(f"{tex.as_posix()}: thiếu {label}")

    # Engine/font core.
    need(r"\\documentclass\[[^\]]*\bborder\s*=\s*3pt\b[^\]]*\]\{standalone\}", "standalone border=3pt")
    need(r"\\documentclass\[[^\]]*\b10pt\b[^\]]*\]\{standalone\}", "standalone 10pt")
    need(r"\\usepackage\{fontspec\}", "fontspec")
    need(r"\\usepackage\{unicode-math\}", "unicode-math")
    need(r"\\setmainfont\{STIXTwoText-Regular\.otf\}", "STIX Two Text")
    need(r"\\setmathfont\{STIXTwoMath\.otf\}", "STIX Two Math")

    # Locked semantic colors.  Exact HEX values matter because a visually
    # similar color is not the same project role.
    for name, value in (
        ("zoPlotBackground", "FFF9E9"),
        ("zoPlotBorder", "DFD7CA"),
        ("zoAxis", "554F48"),
        ("zoText", "3E3A35"),
        ("zoGraphMain", "EF5350"),
    ):
        need(
            rf"\\definecolor\{{{re.escape(name)}\}}\{{HTML\}}\{{{value}\}}",
            f"{name}={value}",
            re.IGNORECASE,
        )

    # Standard illustration field and hierarchy.
    need(r"\bshow\s+background\s+rectangle\b", "trường nền đồ thị")
    need(r"\binner\s+frame\s+sep\s*=\s*4mm\b", "inner frame sep=4mm")
    need(r"\bfill\s*=\s*zoPlotBackground\b", "nền zoPlotBackground")
    need(r"\bdraw\s*=\s*zoPlotBorder\b", "viền zoPlotBorder")
    need(r"\brounded\s+corners\s*=\s*2mm\b", "rounded corners=2mm")

    # Axis/main-curve core.  Positioning remains local to each graph.
    need(r"\baxis\s+lines\s*=\s*middle\b", "axis lines=middle")
    need(r"\baxis\s+line\s+style\s*=\s*\{[^{}]*draw\s*=\s*zoAxis[^{}]*line\s+width\s*=\s*0\.8pt[^{}]*<->[^{}]*\}", "trục zoAxis 0.8pt với <->")
    need(r"\btickwidth\s*=\s*0\.4mm\b", "tickwidth=0.4mm")
    need(r"\btick\s+style\s*=\s*\{[^{}]*draw\s*=\s*zoAxis[^{}]*line\s+width\s*=\s*0\.32pt[^{}]*\}", "tick zoAxis 0.32pt")
    need(r"\bgrid\s*=\s*none\b", "grid=none")
    need(r"\benlargelimits\s*=\s*false\b", "enlargelimits=false")
    need(r"\bclip\s*=\s*true\b", "clip=true")
    need(r"\bclip\s+mode\s*=\s*individual\b", "clip mode=individual")
    need(r"\bzo\s+graph\s+main/\.style\s*=\s*\{[^{}]*draw\s*=\s*zoGraphMain[^{}]*line\s+width\s*=\s*1\.2pt[^{}]*\}", "zo graph main 1.2pt")

    return errors


def _academic_body_before_exercises(body: str) -> str:
    """Return learner-facing academic body before the real H2 Bài tập."""

    kept: list[str] = []
    fence_char: str | None = None
    fence_len = 0
    for line in body.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        stripped = line.lstrip()
        fence = re.match(r"^(`{3,}|~{3,})", stripped)
        if fence_char is not None:
            kept.append(line)
            if fence and fence.group(1)[0] == fence_char and len(fence.group(1)) >= fence_len:
                fence_char = None
                fence_len = 0
            continue
        if fence:
            fence_char = fence.group(1)[0]
            fence_len = len(fence.group(1))
            kept.append(line)
            continue
        heading = re.match(r"^\s*##(?!#)\s+(.+?)\s*$", line)
        if heading:
            title = re.sub(r"\s+\{[^{}]*\}\s*$", "", heading.group(1)).strip().casefold()
            if title == "bài tập":
                break
        kept.append(line)
    return "\n".join(kept).rstrip() + "\n"


def _academic_content_sha256(body: str) -> str:
    return hashlib.sha256(_academic_body_before_exercises(body).encode("utf-8")).hexdigest()


def _exercise_body_from_heading(body: str) -> str:
    """Return the real H2 Bài tập section, including its heading."""

    normalized = body.replace("\r\n", "\n").replace("\r", "\n")
    kept: list[str] = []
    in_exercises = False
    fence_char: str | None = None
    fence_len = 0
    for line in normalized.split("\n"):
        stripped = line.lstrip()
        fence = re.match(r"^(`{3,}|~{3,})", stripped)
        if fence_char is not None:
            if in_exercises:
                kept.append(line)
            if fence and fence.group(1)[0] == fence_char and len(fence.group(1)) >= fence_len:
                fence_char = None
                fence_len = 0
            continue
        if fence:
            fence_char = fence.group(1)[0]
            fence_len = len(fence.group(1))
            if in_exercises:
                kept.append(line)
            continue
        if not in_exercises:
            heading = re.match(r"^\s*##(?!#)\s+(.+?)\s*$", line)
            if heading:
                title = re.sub(r"\s+\{[^{}]*\}\s*$", "", heading.group(1)).strip().casefold()
                if title == "bài tập":
                    in_exercises = True
                    kept.append(line)
            continue
        kept.append(line)
    if not in_exercises:
        return ""
    return "\n".join(kept).rstrip() + "\n"


def _exercise_content_sha256(body: str) -> str:
    return hashlib.sha256(_exercise_body_from_heading(body).encode("utf-8")).hexdigest()




def _metadata_description_sha256(
    metadata: Mapping[str, Any], fields: Sequence[str]
) -> str:
    payload = {
        field: metadata.get(field)
        for field in fields
    }
    normalized = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _source_without_fenced_or_inline_code(body: str) -> str:
    """Remove fenced and inline-code regions before learner-source linting."""

    kept: list[str] = []
    fence_char: str | None = None
    fence_len = 0
    for line in body.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        stripped = line.lstrip()
        fence = re.match(r"^(`{3,}|~{3,})", stripped)
        if fence_char is not None:
            if fence and fence.group(1)[0] == fence_char and len(fence.group(1)) >= fence_len:
                fence_char = None
                fence_len = 0
            kept.append("")
            continue
        if fence:
            fence_char = fence.group(1)[0]
            fence_len = len(fence.group(1))
            kept.append("")
            continue
        # Inline code is not learner-facing math source and may legitimately show
        # literal slash/Unicode examples.
        kept.append(re.sub(r"`[^`\n]*`", "", line))
    source = "\n".join(kept)
    return re.sub(r"<!--.*?-->", "", source, flags=re.DOTALL)


def _math_segments(body: str) -> list[str]:
    """Return $...$ and $$...$$ payloads outside code regions."""

    source = _source_without_fenced_or_inline_code(body)
    pattern = re.compile(
        r"(?<!\\)\$\$(.*?)(?<!\\)\$\$|(?<!\\)\$(.*?)(?<!\\)\$",
        flags=re.DOTALL,
    )
    result: list[str] = []
    for match in pattern.finditer(source):
        result.append(match.group(1) if match.group(1) is not None else match.group(2))
    return result


def _unicode_math_violations(body: str, symbols: Sequence[str]) -> list[str]:
    violations: set[str] = set()
    for segment in _math_segments(body):
        for symbol in symbols:
            if symbol and symbol in segment:
                violations.add(symbol)
    return sorted(violations)


def _fraction_source_violations(body: str) -> list[str]:
    violations: set[str] = set()
    for segment in _math_segments(body):
        if "/" in segment:
            violations.add("literal /")
        if "\\dfrac" in segment:
            violations.add("\\dfrac")
        if "\\tfrac" in segment:
            violations.add("\\tfrac")
        if re.search(r"\\over\b", segment):
            violations.add("\\over")
    return sorted(violations)


def _exercise_subitem_style_violations(body: str) -> list[str]:
    exercise = _exercise_body_from_heading(body)
    if not exercise:
        return []
    source = _source_without_fenced_or_inline_code(exercise)
    return sorted(
        set(
            match.group(0).strip()
            for match in re.finditer(r"(?m)^\s*[a-z]\)\s+", source)
        )
    )


def _review_copy_paths(
    root: Path, target: Path, project_root: Path, markers: Sequence[str]
) -> list[str]:
    normalized = [marker.casefold() for marker in markers if marker]
    if not normalized:
        return []
    article_root = root / target.parent
    figure_root = root / project_root / "_figures" / target.stem
    found: set[str] = set()
    for base in (article_root, figure_root):
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            try:
                relative = path.relative_to(root)
            except ValueError:
                continue
            name = path.name.casefold()
            if base == article_root and not name.startswith(target.stem.casefold()):
                continue
            if any(marker in name for marker in normalized):
                found.add(relative.as_posix())
    return sorted(found)


def _contains_tex_markup(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    return bool(re.search(r"\$|\\[A-Za-z]+|\\\(|\\\[", value))


def _plain_metadata_incompatible_fields(metadata: Mapping[str, Any], plain_fields: Any) -> list[str]:
    if not isinstance(plain_fields, list):
        return []
    return [field for field in plain_fields if isinstance(field, str) and field and _contains_tex_markup(metadata.get(field))]


def pdf_plain_metadata_preflight_applies(root: Path, target: Path) -> bool:
    """Return whether the new early PDF-string rule applies to this article.

    Current/future production profiles use the new rule. Legacy profiles retain
    their established checker/regression contract until they are migrated.
    """
    root = root.resolve()
    target = Path(target)
    if target.is_absolute():
        try:
            target = target.resolve().relative_to(root)
        except ValueError as exc:
            raise ReviewReadyError(f"Bài QMD nằm ngoài repository: {target.as_posix()}.") from exc

    config = discover_project_config(root, target)
    if config is None:
        raise ReviewReadyError(f"Không tìm thấy cấu hình dự án cho {target.as_posix()}.")
    article_type = config.article_type_for(target)
    if article_type is None:
        raise ReviewReadyError(f"Bài không khớp loại bài đã cấu hình: {target.as_posix()}.")

    policy = _extension_policy(config.raw, article_type.id)
    profile_policy = _mapping(policy.get("profile"))
    required_version = profile_policy.get("required_version")
    if not isinstance(required_version, int):
        return True

    profile_abs = root / config.profile_path_for(target)
    if not profile_abs.is_file():
        return False

    profile = _load_yaml(profile_abs, "hồ sơ sản xuất")
    version = profile.get("phien_ban_ho_so")
    return isinstance(version, int) and version >= required_version


def pdf_plain_metadata_violations(root: Path, target: Path) -> list[str]:
    """Return configured PDF-string metadata fields that contain TeX."""
    root = root.resolve()
    target = Path(target)
    if target.is_absolute():
        try:
            target = target.resolve().relative_to(root)
        except ValueError as exc:
            raise ReviewReadyError(f"Bài QMD nằm ngoài repository: {target.as_posix()}.") from exc
    qmd = root / target
    if not qmd.is_file():
        raise ReviewReadyError(f"Không tìm thấy bài QMD: {target.as_posix()}.")
    config = discover_project_config(root, target)
    if config is None:
        raise ReviewReadyError(f"Không tìm thấy cấu hình dự án cho {target.as_posix()}.")
    article_type = config.article_type_for(target)
    if article_type is None:
        raise ReviewReadyError(f"Bài không khớp loại bài đã cấu hình: {target.as_posix()}.")
    policy = _extension_policy(config.raw, article_type.id)
    pdf_policy = _mapping(policy.get("pdf"))
    text = qmd.read_text(encoding="utf-8")
    metadata, _body, error = split_qmd_front_matter(text)
    if error or metadata is None:
        raise ReviewReadyError(error or "Không đọc được YAML front matter.")
    return _plain_metadata_incompatible_fields(metadata, pdf_policy.get("plain_metadata_fields", []))


def _exercise_section_headings(body: str) -> tuple[bool, list[tuple[str, list[int]]], list[tuple[int, str]], list[str]]:
    """Return exercise-section presence, H3 groups, numbered H4 exercises, invalid H4 titles."""

    in_exercises = False
    fence_char: str | None = None
    fence_len = 0
    groups: list[tuple[str, list[int]]] = []
    exercises: list[tuple[int, str]] = []
    invalid_h4: list[str] = []
    current_group: int | None = None

    for line in body.splitlines():
        stripped = line.lstrip()
        fence = re.match(r"^(`{3,}|~{3,})", stripped)
        if fence_char is not None:
            if fence and fence.group(1)[0] == fence_char and len(fence.group(1)) >= fence_len:
                fence_char = None
                fence_len = 0
            continue
        if fence:
            fence_char = fence.group(1)[0]
            fence_len = len(fence.group(1))
            continue

        h2 = re.match(r"^\s*##(?!#)\s+(.+?)\s*$", line)
        if h2:
            title = re.sub(r"\s+\{[^{}]*\}\s*$", "", h2.group(1)).strip()
            if title.casefold() == "bài tập":
                in_exercises = True
                continue
            if in_exercises:
                break
            continue
        if not in_exercises:
            continue

        h3 = re.match(r"^\s*###(?!#)\s+(.+?)\s*$", line)
        if h3:
            groups.append((re.sub(r"\s+\{[^{}]*\}\s*$", "", h3.group(1)).strip(), []))
            current_group = len(groups) - 1
            continue
        h4 = re.match(r"^\s*####(?!#)\s+(.+?)\s*$", line)
        if h4:
            title = re.sub(r"\s+\{[^{}]*\}\s*$", "", h4.group(1)).strip()
            match = re.match(r"^Bài\s+([1-9][0-9]*)\.\s+\S", title, flags=re.IGNORECASE)
            if match:
                number = int(match.group(1))
                exercises.append((number, title))
                if current_group is None:
                    invalid_h4.append(title + " [không thuộc H3 nhóm]")
                else:
                    groups[current_group][1].append(number)
            else:
                invalid_h4.append(title)

    return in_exercises, groups, exercises, invalid_h4


def _exercise_contract_evaluation(
    body: str,
    profile: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> tuple[list[tuple[str, bool, str]], dict[str, str]]:
    """Evaluate machine-checkable parts of the Exercise Contract.

    Academic quality remains an agent/Human judgment. The machine verifies
    declarations, traceability, synchronization, and public-label boundaries.
    """

    findings: list[tuple[str, bool, str]] = []
    gate_status = {
        "CORE_RECONSTRUCTION": "FAIL",
        "CORE_DEVELOPMENT": "FAIL",
        "EXERCISE_CONTENT_SYNC": "FAIL",
    }

    authority_key = str(policy.get("authority_profile_key") or "quy_chuan_he_bai_tap")
    expected_authority_path = str(
        policy.get("authority_path") or "quy_trinh_xay_dung/quy_chuan_he_bai_tap.md"
    )
    controls = _mapping(profile.get("tai_lieu_dieu_khien"))
    authority = _mapping(controls.get(authority_key))
    authority_ok = (
        authority.get("duong_dan") == expected_authority_path
        and authority.get("da_doc") is True
    )
    findings.append(
        (
            "exercise-authority-profile",
            authority_ok,
            "Quy chuẩn hệ bài tập đã được khai báo và đọc."
            if authority_ok
            else (
                "Hồ sơ phải khai báo tai_lieu_dieu_khien."
                + authority_key
                + f" với duong_dan={expected_authority_path!r} và da_doc=true."
            ),
        )
    )

    system = _mapping(profile.get(str(policy.get("profile_key") or "he_thong_bai_tap")))
    enabled_ok = system.get("kich_hoat") is True
    findings.append(
        (
            "exercise-contract-enabled",
            enabled_ok,
            "Hệ bài tập được kích hoạt trong hồ sơ."
            if enabled_ok
            else "Exercise Contract yêu cầu he_thong_bai_tap.kich_hoat=true trước Human Review.",
        )
    )
    design_ok = system.get("trang_thai_thiet_ke") == "dat"
    findings.append(
        (
            "exercise-design-state",
            design_ok,
            "Hệ bài tập đã được agent đánh dấu trang_thai_thiet_ke=dat."
            if design_ok
            else "he_thong_bai_tap.trang_thai_thiet_ke phải bằng 'dat' trước Human Review.",
        )
    )

    has_section, groups, qmd_exercises, invalid_h4 = _exercise_section_headings(body)
    actual_numbers = [number for number, _ in qmd_exercises]
    qmd_structure_ok = (
        has_section
        and bool(qmd_exercises)
        and not invalid_h4
        and len(actual_numbers) == len(set(actual_numbers))
    )
    findings.append(
        (
            "exercise-qmd-inventory",
            qmd_structure_ok,
            f"QMD có {len(qmd_exercises)} bài tập đánh số hợp lệ dưới H2 Bài tập."
            if qmd_structure_ok
            else (
                "QMD phải có H2 Bài tập và các H4 dạng 'Bài N. ...'; "
                + (
                    "H4 không hợp lệ: " + ", ".join(invalid_h4) + "."
                    if invalid_h4
                    else "không xác định được inventory bài tập hợp lệ."
                )
            ),
        )
    )

    raw_profile_groups = system.get("nhom_bai", [])
    profile_groups = raw_profile_groups if isinstance(raw_profile_groups, list) else []
    profile_group_map: list[tuple[str, list[int]]] = []
    group_errors: list[str] = []
    for index, item in enumerate(profile_groups, start=1):
        if not isinstance(item, dict):
            group_errors.append(f"nhom_bai[{index}] không phải mapping")
            continue
        name = item.get("ten")
        numbers = item.get("bai_so", [])
        if not isinstance(name, str) or not name.strip():
            group_errors.append(f"nhom_bai[{index}].ten rỗng")
            continue
        if not isinstance(numbers, list) or not all(
            isinstance(value, int) and not isinstance(value, bool) and value > 0
            for value in numbers
        ):
            group_errors.append(f"nhom_bai[{index}].bai_so phải là danh sách số nguyên dương")
            continue
        profile_group_map.append((name.strip(), list(numbers)))

    qmd_group_map = [(name, list(numbers)) for name, numbers in groups]
    group_match = not group_errors and profile_group_map == qmd_group_map
    findings.append(
        (
            "exercise-group-inventory",
            group_match,
            f"{len(qmd_group_map)} nhóm bài trong hồ sơ khớp tiêu đề H3 và inventory QMD."
            if group_match
            else (
                "Nhóm bài hồ sơ không khớp QMD: "
                f"QMD={qmd_group_map!r}; hồ sơ={profile_group_map!r}; "
                + ("; ".join(group_errors) if group_errors else "")
            ),
        )
    )

    contract = _mapping(system.get("hop_dong"))
    raw_core = contract.get("mach_cot_loi", [])
    core_items = raw_core if isinstance(raw_core, list) else []
    core_ids: list[str] = []
    core_errors: list[str] = []
    for index, item in enumerate(core_items, start=1):
        if not isinstance(item, dict):
            core_errors.append(f"mach_cot_loi[{index}] không phải mapping")
            continue
        core_id = item.get("id")
        content = item.get("noi_dung")
        if not isinstance(core_id, str) or not core_id.strip():
            core_errors.append(f"mach_cot_loi[{index}].id rỗng")
            continue
        core_id = core_id.strip()
        if core_id in core_ids:
            core_errors.append(f"id trùng {core_id}")
        core_ids.append(core_id)
        if not isinstance(content, str) or not content.strip():
            core_errors.append(f"{core_id}.noi_dung rỗng")
    core_ok = bool(core_ids) and not core_errors
    findings.append(
        (
            "exercise-core-map",
            core_ok,
            f"Đã khai báo {len(core_ids)} mắt xích cốt lõi có ID duy nhất."
            if core_ok
            else "Mạch cốt lõi chưa hợp lệ: " + ("; ".join(core_errors) if core_errors else "danh sách rỗng."),
        )
    )

    raw_entries = contract.get("bai_tap", [])
    entries = raw_entries if isinstance(raw_entries, list) else []
    declared_numbers: list[int] = []
    entry_errors: list[str] = []
    reconstruction_refs: dict[str, set[int]] = {core_id: set() for core_id in core_ids}
    development_count = 0

    for index, item in enumerate(entries, start=1):
        if not isinstance(item, dict):
            entry_errors.append(f"bai_tap[{index}] không phải mapping")
            continue
        number = item.get("so")
        if not isinstance(number, int) or isinstance(number, bool) or number <= 0:
            entry_errors.append(f"bai_tap[{index}].so không phải số nguyên dương")
            continue
        if number in declared_numbers:
            entry_errors.append(f"bài {number} được khai báo lặp")
        declared_numbers.append(number)

        functions = item.get("chuc_nang", [])
        if not isinstance(functions, list) or not functions:
            entry_errors.append(f"bài {number} thiếu chuc_nang")
            functions = []
        function_set = {str(value).strip() for value in functions if isinstance(value, str) and str(value).strip()}
        unexpected_functions = sorted(function_set - {"tai_dung", "phat_trien"})
        if unexpected_functions:
            entry_errors.append(f"bài {number} có chuc_nang lạ: {', '.join(unexpected_functions)}")

        reconstruct = item.get("tai_dung_mat_xich", [])
        develop = item.get("phat_trien_tu_mat_xich", [])
        if not isinstance(reconstruct, list):
            entry_errors.append(f"bài {number}.tai_dung_mat_xich phải là danh sách")
            reconstruct = []
        if not isinstance(develop, list):
            entry_errors.append(f"bài {number}.phat_trien_tu_mat_xich phải là danh sách")
            develop = []

        reconstruct_ids = [str(value).strip() for value in reconstruct if isinstance(value, str) and str(value).strip()]
        develop_ids = [str(value).strip() for value in develop if isinstance(value, str) and str(value).strip()]
        invalid_refs = sorted((set(reconstruct_ids) | set(develop_ids)) - set(core_ids))
        if invalid_refs:
            entry_errors.append(f"bài {number} tham chiếu mắt xích không tồn tại: {', '.join(invalid_refs)}")

        if "tai_dung" in function_set:
            if not reconstruct_ids:
                entry_errors.append(f"bài {number} khai báo tai_dung nhưng không chỉ ra mắt xích")
            for core_id in reconstruct_ids:
                if core_id in reconstruction_refs:
                    reconstruction_refs[core_id].add(number)

        if "phat_trien" in function_set:
            development_count += 1
            if not develop_ids:
                entry_errors.append(f"bài {number} khai báo phat_trien nhưng không chỉ ra mắt xích xuất phát")

    inventory_match = (
        qmd_structure_ok
        and len(declared_numbers) == len(set(declared_numbers))
        and set(declared_numbers) == set(actual_numbers)
    )
    if not inventory_match:
        entry_errors.append(
            "inventory hồ sơ không khớp QMD: "
            f"QMD={sorted(set(actual_numbers))}, hồ sơ={sorted(set(declared_numbers))}"
        )

    dependency_ok = bool(entries) and not entry_errors and core_ok and inventory_match and group_match
    findings.append(
        (
            "exercise-dependency-map",
            dependency_ok,
            f"Bản đồ phụ thuộc khớp {len(qmd_exercises)} bài trong QMD."
            if dependency_ok
            else "Bản đồ phụ thuộc chưa hợp lệ: " + ("; ".join(entry_errors) if entry_errors else "danh sách rỗng."),
        )
    )

    confirmations = _mapping(contract.get("xac_nhan_agent"))
    required_agent_status = str(policy.get("required_agent_status") or "dat")
    reconstruction_covered = core_ok and dependency_ok and all(reconstruction_refs.get(core_id) for core_id in core_ids)
    reconstruction_agent = confirmations.get("tai_dung") == required_agent_status
    reconstruction_ok = authority_ok and enabled_ok and design_ok and reconstruction_covered and reconstruction_agent
    gate_status["CORE_RECONSTRUCTION"] = "PASS" if reconstruction_ok else "FAIL"
    missing_core = [core_id for core_id in core_ids if not reconstruction_refs.get(core_id)]
    findings.append(
        (
            "exercise-core-reconstruction",
            reconstruction_ok,
            (
                "CORE_RECONSTRUCTION=PASS — mọi mắt xích cốt lõi có bài tái dựng và agent đã xác nhận chất lượng."
                if reconstruction_ok
                else "CORE_RECONSTRUCTION=FAIL — "
                + (
                    "thiếu coverage: " + ", ".join(missing_core) + "; "
                    if missing_core
                    else ""
                )
                + f"xac_nhan_agent.tai_dung={confirmations.get('tai_dung')!r}, cần {required_agent_status!r}."
            ),
        )
    )

    development_agent = confirmations.get("phat_trien") == required_agent_status
    development_ok = authority_ok and enabled_ok and design_ok and dependency_ok and development_count > 0 and development_agent
    gate_status["CORE_DEVELOPMENT"] = "PASS" if development_ok else "FAIL"
    findings.append(
        (
            "exercise-core-development",
            development_ok,
            (
                f"CORE_DEVELOPMENT=PASS — có {development_count} bài phát triển truy nguyên về mạch cốt lõi và agent đã xác nhận chất lượng."
                if development_ok
                else "CORE_DEVELOPMENT=FAIL — "
                + f"development_count={development_count}; "
                + f"xac_nhan_agent.phat_trien={confirmations.get('phat_trien')!r}, cần {required_agent_status!r}."
            ),
        )
    )

    sync = _mapping(contract.get("dong_bo"))
    current_academic_hash = _academic_content_sha256(body)
    current_exercise_hash = _exercise_content_sha256(body)
    stored_academic_hash = sync.get("noi_dung_hoc_thuat_sha256")
    stored_exercise_hash = sync.get("noi_dung_bai_tap_sha256")
    academic_hash_ok = (
        isinstance(stored_academic_hash, str)
        and bool(re.fullmatch(r"[0-9a-fA-F]{64}", stored_academic_hash.strip()))
        and stored_academic_hash.strip().lower() == current_academic_hash
    )
    exercise_hash_ok = (
        isinstance(stored_exercise_hash, str)
        and bool(re.fullmatch(r"[0-9a-fA-F]{64}", stored_exercise_hash.strip()))
        and stored_exercise_hash.strip().lower() == current_exercise_hash
    )
    hash_ok = academic_hash_ok and exercise_hash_ok
    sync_agent = confirmations.get("dong_bo") == required_agent_status
    sync_ok = authority_ok and enabled_ok and design_ok and dependency_ok and hash_ok and sync_agent
    gate_status["EXERCISE_CONTENT_SYNC"] = "PASS" if sync_ok else "FAIL"
    findings.append(
        (
            "exercise-content-sync",
            sync_ok,
            (
                "EXERCISE_CONTENT_SYNC=PASS — hồ sơ khớp fingerprint nội dung học thuật và hệ bài tập hiện hành; agent đã xác nhận đồng bộ."
                if sync_ok
                else "EXERCISE_CONTENT_SYNC=FAIL — "
                + f"academic(stored={stored_academic_hash!r}, current={current_academic_hash}); "
                + f"exercises(stored={stored_exercise_hash!r}, current={current_exercise_hash}); "
                + f"xac_nhan_agent.dong_bo={confirmations.get('dong_bo')!r}, cần {required_agent_status!r}."
            ),
        )
    )

    exact_terms = {
        str(value).strip().casefold()
        for value in policy.get("forbidden_public_heading_exact", [])
        if isinstance(value, str) and value.strip()
    }
    prefix_terms = [
        str(value).strip().casefold()
        for value in policy.get("forbidden_public_heading_prefixes", [])
        if isinstance(value, str) and value.strip()
    ]
    leaked: list[str] = []
    learner_headings = [name for name, _ in groups] + [title for _, title in qmd_exercises] + invalid_h4
    for heading in learner_headings:
        visible_title = re.sub(r"^Bài\s+[1-9][0-9]*\.\s+", "", heading.strip(), flags=re.IGNORECASE)
        normalized = visible_title.casefold()
        if normalized in exact_terms or any(
            normalized == prefix or normalized.startswith(prefix + " ")
            for prefix in prefix_terms
        ):
            leaked.append(heading)
    findings.append(
        (
            "exercise-internal-label-leak",
            not leaked,
            "Không phát hiện nhãn thiết kế nội bộ trong tiêu đề dành cho người học."
            if not leaked
            else "Tiêu đề đang lộ nhãn thiết kế nội bộ: " + ", ".join(leaked) + ".",
        )
    )

    return findings, gate_status

def _authoring_quality_self_review_errors(
    profile: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> list[str]:
    """Validate completion/evidence of agent-owned authoring-quality self-review."""

    errors: list[str] = []
    profile_key = str(policy.get("profile_key") or "tu_kiem_noi_dung")
    review = _mapping(profile.get(profile_key))
    required_sections = _mapping(policy.get("required_criteria"))
    section_status = str(policy.get("required_section_status") or "dat")
    criterion_status = str(policy.get("required_criterion_status") or "dat")
    require_evidence = _truthy(policy.get("require_criterion_evidence"))

    if not required_sections:
        return [f"{profile_key}: authoring_quality.required_criteria rỗng hoặc không hợp lệ."]

    for section_name, raw_ids in required_sections.items():
        if not isinstance(section_name, str) or not section_name:
            errors.append(f"{profile_key}: tên section tự kiểm không hợp lệ.")
            continue
        if not isinstance(raw_ids, list) or not raw_ids or not all(
            isinstance(value, str) and value for value in raw_ids
        ):
            errors.append(
                f"{profile_key}.{section_name}: danh sách required_criteria không hợp lệ."
            )
            continue

        section = _mapping(review.get(section_name))
        if not section:
            errors.append(f"{profile_key}.{section_name}: thiếu section tự kiểm.")
            continue
        if section.get("trang_thai") != section_status:
            errors.append(
                f"{profile_key}.{section_name}.trang_thai phải bằng {section_status!r}."
            )

        criteria = section.get("tieu_chi", [])
        if not isinstance(criteria, list):
            errors.append(f"{profile_key}.{section_name}.tieu_chi phải là danh sách.")
            continue
        by_id: dict[str, Mapping[str, Any]] = {}
        for item in criteria:
            item_map = _mapping(item)
            item_id = item_map.get("id")
            if isinstance(item_id, str) and item_id:
                by_id[item_id] = item_map

        for criterion_id in raw_ids:
            item = by_id.get(criterion_id)
            if item is None:
                errors.append(
                    f"{profile_key}.{section_name}: thiếu tiêu chí {criterion_id}."
                )
                continue
            if item.get("trang_thai") != criterion_status:
                errors.append(
                    f"{profile_key}.{section_name}.{criterion_id}.trang_thai "
                    f"phải bằng {criterion_status!r}."
                )
            if require_evidence:
                evidence = item.get("can_cu", [])
                evidence_ok = (
                    isinstance(evidence, list)
                    and bool(evidence)
                    and all(
                        isinstance(value, str) and bool(value.strip())
                        for value in evidence
                    )
                )
                if not evidence_ok:
                    errors.append(
                        f"{profile_key}.{section_name}.{criterion_id}.can_cu "
                        "phải có ít nhất một căn cứ cụ thể."
                    )
            action = item.get("hanh_dong_sua")
            if action not in (None, ""):
                errors.append(
                    f"{profile_key}.{section_name}.{criterion_id}.hanh_dong_sua "
                    "phải rỗng trước Human Review."
                )

    return errors


def _relation_records_valid(profile: Mapping[str, Any]) -> tuple[bool, str]:
    records = profile.get("kiem_tra_quan_he_trung_tam", [])
    if not isinstance(records, list) or not records:
        return False, "Thiếu bản ghi kiểm tra quan hệ trung tâm."
    invalid: list[int] = []
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            invalid.append(index)
            continue
        required = ("phat_bieu", "phep_thu", "ket_luan")
        if any(not isinstance(record.get(key), str) or not record[key].strip() for key in required):
            invalid.append(index)
            continue
        if record.get("trang_thai") != "dat":
            invalid.append(index)
    if invalid:
        return False, "Bản ghi quan hệ chưa đủ căn cứ hoặc chưa dat: " + ", ".join(map(str, invalid)) + "."
    return True, f"Có {len(records)} bản ghi quan hệ đã kiểm tra."


def evaluate_review_ready(
    root: Path, target: Path, session_path: Path | None = None
) -> tuple[list[ReviewCheck], dict[str, Any]]:
    root = root.resolve()
    qmd = root / target
    if not qmd.is_file():
        raise ReviewReadyError(f"Không tìm thấy bài QMD: {target.as_posix()}.")

    config = discover_project_config(root, target)
    if config is None:
        raise ReviewReadyError(f"Không tìm thấy cấu hình dự án cho {target.as_posix()}.")
    article_type = config.article_type_for(target)
    if article_type is None:
        raise ReviewReadyError(f"Bài không khớp loại bài đã cấu hình: {target.as_posix()}.")
    policy = _extension_policy(config.raw, article_type.id)
    if not policy:
        raise ReviewReadyError(
            f"Dự án {config.project_id} chưa bật extensions.human_review_gate cho {article_type.id}."
        )

    checks: list[ReviewCheck] = []

    def add(name: str, passed: bool, message: str, path: Path | None = None) -> None:
        checks.append(
            ReviewCheck(
                name=name,
                passed=passed,
                message=message,
                path=path.as_posix() if path else None,
            )
        )

    session: dict[str, Any] = {}
    lifecycle = _mapping(policy.get("lifecycle"))
    if _truthy(lifecycle.get("require_session_manifest")):
        canonical_session = session_path or (root / "_audit" / f"{target.stem}_session.json")
        session_rel = canonical_session.resolve().relative_to(root.resolve())
        if not canonical_session.is_file():
            add(
                "lifecycle-session-manifest",
                False,
                "Thiếu session manifest; phải chạy start trước khi sản xuất candidate.",
                session_rel,
            )
        else:
            try:
                session = _load_json_mapping(canonical_session, "session manifest")
            except ReviewReadyError as exc:
                add("lifecycle-session-manifest", False, str(exc), session_rel)
                session = {}

            version_ok = session.get("session_manifest_version") == SESSION_MANIFEST_VERSION
            add(
                "lifecycle-session-version",
                version_ok,
                f"Session manifest version={SESSION_MANIFEST_VERSION}."
                if version_ok
                else f"Session manifest phải có version={SESSION_MANIFEST_VERSION}.",
                session_rel,
            )
            target_ok = _mapping(session.get("scope")).get("target") == target.as_posix()
            add(
                "lifecycle-session-target",
                target_ok,
                "Session manifest thuộc đúng candidate."
                if target_ok
                else "Session manifest không thuộc đúng candidate hiện tại.",
                session_rel,
            )
            inspect = _mapping(session.get("inspect"))
            project_info = _mapping(inspect.get("project"))
            project_ok = project_info.get("id") == config.project_id and inspect.get("article_type") == article_type.id
            add(
                "lifecycle-session-project",
                project_ok,
                "Session manifest khớp project/article type."
                if project_ok
                else "Session manifest không khớp project/article type hiện tại.",
                session_rel,
            )

            repository = _mapping(session.get("repository"))
            start_commit = repository.get("commit")
            current_commit = _git_text(root, "rev-parse", "HEAD")
            commit_ok = isinstance(start_commit, str) and start_commit == current_commit
            add(
                "lifecycle-head-stable",
                commit_ok,
                "HEAD không đổi kể từ start."
                if commit_ok
                else "HEAD đã đổi kể từ start; session không còn đại diện cho candidate hiện tại.",
                session_rel,
            )

            scope = _mapping(session.get("scope"))
            expected_scope = _canonical_scope(root, target, config, policy)
            session_allowed = scope.get("allowed", [])
            allowed_ok = (
                scope.get("strategy") == "canonical"
                and isinstance(session_allowed, list)
                and {str(item) for item in session_allowed} == {path.as_posix() for path in expected_scope}
            )
            add(
                "lifecycle-canonical-scope",
                allowed_ok,
                "Session dùng đúng phạm vi production canonical do Cỗ máy suy ra."
                if allowed_ok
                else "Session scope không khớp phạm vi canonical hiện hành; không được tự mở rộng/thu hẹp phạm vi.",
                session_rel,
            )

            initial_scope_dirty = scope.get("initial_scope_dirty", [])
            initial_clean = isinstance(initial_scope_dirty, list) and not initial_scope_dirty
            add(
                "lifecycle-start-before-production",
                initial_clean,
                "Candidate scope sạch tại thời điểm start."
                if initial_clean
                else "Candidate đã có thay đổi trước start; lifecycle không được khóa từ đầu.",
                session_rel,
            )

            if _truthy(lifecycle.get("require_authority_snapshot")):
                authority = _mapping(session.get("authority_sources"))
                snapshot = authority.get("snapshot", [])
                snapshot_map = {
                    str(item.get("path")): item
                    for item in snapshot
                    if isinstance(item, dict) and item.get("path")
                } if isinstance(snapshot, list) else {}
                expected_authority = _expected_authority_records(root, target, config)
                missing: list[str] = []
                metadata_mismatch: list[str] = []
                drift: list[str] = []
                for expected in expected_authority:
                    path = expected["path"]
                    key = path.as_posix()
                    record = snapshot_map.get(key)
                    if not isinstance(record, dict):
                        missing.append(key)
                        continue
                    if record.get("role") != expected["role"] or bool(record.get("lock")) != bool(expected["lock"]):
                        metadata_mismatch.append(key)
                    if expected["lock"]:
                        absolute = root / path
                        if not absolute.is_file() or record.get("sha256") != _sha256_file(absolute):
                            drift.append(key)
                authority_ok = not missing and not metadata_mismatch and not drift
                detail: list[str] = []
                if missing:
                    detail.append("thiếu authority record: " + ", ".join(missing))
                if metadata_mismatch:
                    detail.append("sai role/lock: " + ", ".join(metadata_mismatch))
                if drift:
                    detail.append("effective authority đã đổi: " + ", ".join(drift))
                add(
                    "lifecycle-authority-snapshot",
                    authority_ok,
                    "Effective authority closure và provenance inventory khớp session; các authority bị khóa không drift."
                    if authority_ok
                    else "; ".join(detail),
                    session_rel,
                )

            if _truthy(lifecycle.get("enforce_scope_delta")) and allowed_ok:
                initial_dirty = repository.get("dirty_fingerprints", {})
                initial_dirty = initial_dirty if isinstance(initial_dirty, dict) else {}
                current_dirty = {path.as_posix() for path in _git_dirty_paths(root)}
                candidates = set(initial_dirty) | current_dirty
                changed_since_start: list[Path] = []
                for raw_path in sorted(candidates):
                    path = Path(raw_path)
                    if raw_path in initial_dirty:
                        if _path_fingerprint(root, path) != initial_dirty[raw_path]:
                            changed_since_start.append(path)
                    else:
                        changed_since_start.append(path)

                evidence_roots = [Path(str(item)) for item in scope.get("evidence_roots", []) if isinstance(item, str)]
                allowed_paths = [Path(str(item)) for item in session_allowed]
                excluded_paths = [Path(str(item)) for item in scope.get("excluded", []) if isinstance(item, str)]
                violations: list[str] = []
                for path in changed_since_start:
                    if any(_path_is_within(path, evidence) for evidence in evidence_roots):
                        continue
                    in_allowed = any(_path_is_within(path, allowed) for allowed in allowed_paths)
                    in_excluded = any(_path_is_within(path, excluded) for excluded in excluded_paths)
                    if not in_allowed or in_excluded:
                        violations.append(path.as_posix())
                add(
                    "lifecycle-scope-delta",
                    not violations,
                    "Mọi thay đổi kể từ start nằm trong phạm vi canonical đã khóa."
                    if not violations
                    else "Phát hiện thay đổi ngoài phạm vi kể từ start: " + ", ".join(violations),
                    session_rel,
                )

    review_copy_markers = lifecycle.get("forbidden_review_copy_markers", [])
    if isinstance(review_copy_markers, list):
        copy_paths = _review_copy_paths(
            root,
            target,
            config.project_root,
            [str(value) for value in review_copy_markers if isinstance(value, str)],
        )
        add(
            "human-review-copy-storage",
            not copy_paths,
            "Không có bản sao Human Review trong vùng production của candidate."
            if not copy_paths
            else "Bản sao Human Review phải nằm ngoài production worktree; phát hiện: "
            + ", ".join(copy_paths),
            target.parent,
        )

    try:
        text = qmd.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ReviewReadyError(f"Không đọc được {target.as_posix()}: {exc}") from exc
    metadata, body, error = split_qmd_front_matter(text)
    if error or metadata is None:
        raise ReviewReadyError(error or "Không đọc được YAML front matter.")

    profile_rel = config.profile_path_for(target)
    profile_abs = root / profile_rel
    profile = _load_yaml(profile_abs, "hồ sơ sản xuất")
    add("profile-exists", True, "Hồ sơ sản xuất tồn tại và đọc được.", profile_rel)

    profile_policy = _mapping(policy.get("profile"))
    required_version = profile_policy.get("required_version")
    if isinstance(required_version, int):
        version_ok = profile.get("phien_ban_ho_so") == required_version
        add(
            "profile-schema-version",
            version_ok,
            f"Hồ sơ dùng schema version {required_version}."
            if version_ok
            else f"phien_ban_ho_so phải bằng {required_version}.",
            profile_rel,
        )
    required_top = profile_policy.get("required_top_level", [])
    if isinstance(required_top, list):
        missing_top = [name for name in required_top if isinstance(name, str) and name not in profile]
        add(
            "profile-schema-required-top-level",
            not missing_top,
            "Đủ các nhóm agent-owned bắt buộc của hồ sơ."
            if not missing_top
            else "Thiếu nhóm hồ sơ bắt buộc: " + ", ".join(missing_top),
            profile_rel,
        )
    forbidden_top = profile_policy.get("forbidden_top_level", [])
    if isinstance(forbidden_top, list):
        present_forbidden = [name for name in forbidden_top if isinstance(name, str) and name in profile]
        add(
            "profile-schema-ownership-boundary",
            not present_forbidden,
            "Hồ sơ không chứa trạng thái machine-owned hoặc Human Review/nghiệm thu do agent tự sở hữu."
            if not present_forbidden
            else "Nhóm không thuộc agent-owned profile: " + ", ".join(present_forbidden),
            profile_rel,
        )

    if _truthy(profile_policy.get("require_template_shape")):
        shape_errors = _profile_template_shape_errors(root, config, profile)
        add(
            "profile-schema-template-shape",
            not shape_errors,
            "Hồ sơ giữ nguyên cấu trúc agent-owned và bộ tiêu chí tự kiểm của template."
            if not shape_errors
            else "; ".join(shape_errors),
            profile_rel,
        )

    theory = _mapping(_mapping(profile.get("tai_lieu_dieu_khien")).get("nguon_li_thuyet_day_du"))
    if theory.get("da_dung") is True:
        raw_theory = theory.get("duong_dan")
        positions = theory.get("vi_tri_da_dung", [])
        theory_path_ok = isinstance(raw_theory, str) and bool(raw_theory.strip())
        positions_ok = isinstance(positions, list) and bool(positions) and all(isinstance(item, str) and item.strip() for item in positions)
        provenance_ok = False
        if theory_path_ok:
            try:
                theory_rel = _relative_to_root(root, str(raw_theory))
            except ReviewReadyError:
                theory_rel = None
            if theory_rel is not None:
                authority = _mapping(session.get("authority_sources"))
                snapshot = authority.get("snapshot", [])
                record = next(
                    (item for item in snapshot if isinstance(item, dict) and item.get("path") == theory_rel.as_posix()),
                    None,
                ) if isinstance(snapshot, list) else None
                provenance_ok = (
                    isinstance(record, dict)
                    and record.get("role") == "reference_only"
                    and (root / theory_rel).is_file()
                    and record.get("sha256") == _sha256_file(root / theory_rel)
                )
        add(
            "profile-theory-reference-provenance",
            theory_path_ok and positions_ok and provenance_ok,
            "Nguồn lí thuyết đầy đủ được dùng theo provenance machine-owned của session."
            if theory_path_ok and positions_ok and provenance_ok
            else "Khi da_dung=true, phải ghi vị trí cụ thể và nguồn phải khớp reference inventory của session; không tự duy trì SHA kỳ vọng trong profile.",
            profile_rel,
        )

    # Navigation and rendered HTML are checked at this lifecycle boundary because
    # successful source/render checks alone do not prove production integration.
    navigation = _mapping(policy.get("navigation"))
    if _truthy(navigation.get("explicit_sidebar_required")):
        raw_quarto = navigation.get("quarto_config", "_quarto.yml")
        if not isinstance(raw_quarto, str) or not raw_quarto.strip():
            raise ReviewReadyError("human_review_gate.navigation.quarto_config không hợp lệ.")
        quarto_rel = _relative_to_root(root, raw_quarto)
        quarto = _load_yaml(root / quarto_rel, "cấu hình Quarto")
        sidebar = _mapping(quarto.get("website")).get("sidebar", [])
        hrefs = set(_collect_hrefs(sidebar))
        target_href = _normalize_href(target.as_posix())
        add(
            "navigation-sidebar-source",
            target_href in hrefs,
            "Bài đã đăng kí trong website.sidebar."
            if target_href in hrefs
            else "Bài chưa được đăng kí trong website.sidebar của _quarto.yml.",
            quarto_rel,
        )
        html_abs = _rendered_html_path(root, target, quarto)
        html_rel = html_abs.relative_to(root)
        html_exists = html_abs.is_file()
        add(
            "navigation-rendered-html",
            html_exists,
            "HTML render tồn tại."
            if html_exists
            else f"Thiếu HTML render: {html_rel.as_posix()}.",
            html_rel,
        )
        if html_exists:
            try:
                html_text = html_abs.read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                raise ReviewReadyError(f"Không đọc được HTML render: {exc}") from exc
            has_sidebar = bool(re.search(r"\bid=[\"']quarto-sidebar[\"']", html_text))
            add(
                "navigation-rendered-sidebar",
                has_sidebar,
                "HTML chứa sidebar Quarto thật."
                if has_sidebar
                else "HTML render không chứa phần tử #quarto-sidebar.",
                html_rel,
            )

    # The review handoff is only meaningful when the downloadable PDF is real
    # and current with the source shown to the reviewer.
    pdf_policy = _mapping(policy.get("pdf"))
    if _truthy(pdf_policy.get("download_required")):
        download = _mapping(metadata.get("zo-pdf-download"))
        href = download.get("href")
        valid_href = isinstance(href, str) and bool(href.strip())
        add(
            "pdf-download-metadata",
            valid_href,
            "zo-pdf-download.href đã được khai báo."
            if valid_href
            else "Thiếu zo-pdf-download.href.",
            target,
        )
        if valid_href:
            pdf_rel = _resolve_qmd_asset(root, target, str(href))
            pdf_exists = pdf_rel is not None and (root / pdf_rel).is_file()
            add(
                "pdf-download-artifact",
                pdf_exists,
                "PDF tải xuống tồn tại."
                if pdf_exists
                else "PDF tải xuống không tồn tại trong repository/worktree.",
                pdf_rel or target,
            )
            if pdf_exists and pdf_rel is not None:
                pdf_abs = root / pdf_rel
                is_pdf = pdf_abs.read_bytes()[:5] == b"%PDF-"
                add(
                    "pdf-download-signature",
                    is_pdf,
                    "Tệp tải xuống có chữ kí PDF."
                    if is_pdf
                    else "Tệp tải xuống không có chữ kí %PDF-.",
                    pdf_rel,
                )
                try:
                    freshness = evaluate_artifact_freshness(root, target, pdf_rel)
                    add(
                        "pdf-download-freshness",
                        freshness.current,
                        freshness.message,
                        pdf_rel,
                    )
                except FreshnessError as exc:
                    add("pdf-download-freshness", False, str(exc), pdf_rel)

                if _truthy(pdf_policy.get("require_canonical_build_receipt")):
                    receipt = pdf_build_receipt_path(root, qmd)
                    receipt_errors = validate_pdf_build_receipt(
                        root,
                        qmd,
                        pdf_abs,
                        receipt,
                    )
                    add(
                        "pdf-canonical-build-receipt",
                        not receipt_errors,
                        "PDF có build receipt canonical khớp QMD, PDF và toàn bộ pipeline inputs."
                        if not receipt_errors
                        else "; ".join(receipt_errors),
                        receipt.relative_to(root),
                    )

        plain_fields = pdf_policy.get("plain_metadata_fields", [])
        incompatible = _plain_metadata_incompatible_fields(metadata, plain_fields)
        add(
            "pdf-metadata-latex-compatibility",
            not incompatible,
            "Các trường metadata PDF-string dùng văn bản thuần."
            if not incompatible
            else "Không được chứa TeX trong metadata PDF-string: " + ", ".join(incompatible),
            target,
        )

    graph_policy = _mapping(policy.get("function_graph"))
    if _truthy(graph_policy.get("required")):
        resources = _mapping(profile.get("tai_nguyen_hinh"))
        graph_standard = _mapping(_mapping(profile.get("tai_lieu_dieu_khien")).get("quy_chuan_do_thi"))
        add(
            "graph-profile-enabled",
            resources.get("co_su_dung") is True,
            "Hồ sơ xác nhận bài sử dụng tài nguyên hình."
            if resources.get("co_su_dung") is True
            else "Bài function_article ở cổng Human Review phải có đồ thị; không được tự bỏ hình.",
            profile_rel,
        )
        if _truthy(graph_policy.get("require_default_chain")):
            default_chain = resources.get("ap_dung_cau_truc_mac_dinh") is True
            no_self_exemption = _empty(resources.get("li_do_ngoai_le"))
            add(
                "graph-profile-default-chain",
                default_chain,
                "Hồ sơ dùng cấu trúc hình src/pdf/svg mặc định."
                if default_chain
                else "Không được tự miễn cấu trúc hình src/pdf/svg tại cổng Human Review.",
                profile_rel,
            )
            add(
                "graph-profile-no-self-exemption",
                no_self_exemption,
                "Không có ngoại lệ đồ thị do agent tự khai."
                if no_self_exemption
                else "Phát hiện li_do_ngoai_le; ngoại lệ đồ thị cần được cấu hình ở cấp dự án/người dùng, không tự khai trong candidate.",
                profile_rel,
            )
        if _truthy(graph_policy.get("require_graph_standard")):
            standard_ok = graph_standard.get("kich_hoat") is True and graph_standard.get("da_doc") is True
            add(
                "graph-standard-activated",
                standard_ok,
                "Quy chuẩn đồ thị đã được kích hoạt và đọc."
                if standard_ok
                else "Quy chuẩn đồ thị phải kich_hoat=true và da_doc=true.",
                profile_rel,
            )

        chains = _graph_chains(root, target, body)
        if _truthy(graph_policy.get("canonical_root_required")):
            canonical_graph_root = config.project_root / "_figures" / target.stem
            graph_root_errors = [
                svg.as_posix()
                for _, _, svg in chains
                if not _path_is_within(svg, canonical_graph_root)
            ]
            add(
                "graph-canonical-root",
                bool(chains) and not graph_root_errors,
                f"Mọi đồ thị nằm dưới {canonical_graph_root.as_posix()}/."
                if chains and not graph_root_errors
                else (
                    "Đồ thị phải nằm dưới thư mục canonical "
                    + canonical_graph_root.as_posix()
                    + "/; lệch: "
                    + ", ".join(graph_root_errors)
                    if graph_root_errors
                    else f"Thiếu đồ thị dưới {canonical_graph_root.as_posix()}/."
                ),
                target,
            )
        add(
            "graph-qmd-reference",
            bool(chains),
            f"QMD có {len(chains)} tham chiếu đồ thị SVG theo cấu trúc _figures/.../svg/."
            if chains
            else "QMD không có tham chiếu đồ thị SVG theo cấu trúc bắt buộc.",
            target,
        )
        if chains:
            chain_errors: list[str] = []
            tex_files: list[Path] = []
            for src, pdf, svg in chains:
                for label, relative in (("src", src), ("pdf", pdf), ("svg", svg)):
                    if not (root / relative).is_file():
                        chain_errors.append(f"thiếu {label}: {relative.as_posix()}")
                if (root / src).is_file():
                    tex_files.append(src)
            add(
                "graph-source-render-chain",
                not chain_errors,
                "Mỗi đồ thị SVG có đủ nguồn .tex và PDF tương ứng."
                if not chain_errors
                else "; ".join(chain_errors),
                target,
            )

            lint_errors: list[str] = []
            for tex in tex_files:
                raw = (root / tex).read_text(encoding="utf-8", errors="replace")
                # These are machine-checkable invariants of the current graph standard.
                for pattern, label in (
                    (r"\bxticklabels\s*=", "xticklabels"),
                    (r"\byticklabels\s*=", "yticklabels"),
                    (r"\bxticklabel\s+style\s*=", "xticklabel style"),
                    (r"\byticklabel\s+style\s*=", "yticklabel style"),
                    (r"\bStealth\b", "Stealth"),
                ):
                    if re.search(pattern, raw):
                        lint_errors.append(f"{tex.as_posix()}: dùng {label}")
                if re.search(r"\bxtick\s*=", raw) and not re.search(r"\bxticklabel\s*=\s*\\empty", raw):
                    lint_errors.append(f"{tex.as_posix()}: có xtick nhưng thiếu xticklabel=\\empty")
                if re.search(r"\bytick\s*=", raw) and not re.search(r"\byticklabel\s*=\s*\\empty", raw):
                    lint_errors.append(f"{tex.as_posix()}: có ytick nhưng thiếu yticklabel=\\empty")
            add(
                "graph-tex-policy",
                not lint_errors,
                "Nguồn TikZ/PGFPlots đạt các invariant máy kiểm được của quy chuẩn đồ thị."
                if not lint_errors
                else "; ".join(lint_errors),
                target,
            )

            if _truthy(graph_policy.get("require_graph_core_style")):
                core_errors: list[str] = []
                for tex in tex_files:
                    raw = (root / tex).read_text(encoding="utf-8", errors="replace")
                    core_errors.extend(_graph_core_style_errors(raw, tex))
                add(
                    "graph-tex-core-style",
                    not core_errors,
                    "Nguồn đồ thị mang đủ lõi tự chứa bắt buộc của quy chuẩn."
                    if not core_errors
                    else "; ".join(core_errors),
                    target,
                )

    if _truthy(profile_policy.get("require_check_and_render_evidence")):
        modes, errors = _evidence_modes(root, target)
        evidence_ok = {"scope", "render"}.issubset(modes) and not errors
        detail: list[str] = []
        if "scope" not in modes:
            detail.append("thiếu canonical check evidence")
        if "render" not in modes:
            detail.append("thiếu canonical render evidence")
        detail.extend(errors)
        add(
            "machine-check-render-evidence",
            evidence_ok,
            "Machine-owned audit xác nhận check(scope) và render đạt."
            if evidence_ok
            else "; ".join(detail),
            Path("_audit"),
        )

    visual_policy = _mapping(policy.get("visual"))
    raw_mobile_viewports = visual_policy.get("required_mobile_viewports", [])
    required_mobile_viewports = (
        tuple(int(width) for width in raw_mobile_viewports)
        if isinstance(raw_mobile_viewports, list)
        and all(isinstance(width, int) and not isinstance(width, bool) and width > 0 for width in raw_mobile_viewports)
        else ()
    )
    raw_desktop_viewports = visual_policy.get("required_desktop_viewports", [])
    required_desktop_viewports = (
        tuple(int(width) for width in raw_desktop_viewports)
        if isinstance(raw_desktop_viewports, list)
        and all(isinstance(width, int) and not isinstance(width, bool) and width > 0 for width in raw_desktop_viewports)
        else ()
    )
    if _truthy(visual_policy.get("require_machine_measurements")):
        machine_visual_errors = _machine_visual_errors(
            root,
            target,
            required_mobile_viewports,
            required_desktop_viewports,
            require_full_html_capture=_truthy(visual_policy.get("require_full_html_capture")),
        )
        add(
            "machine-visual-viewport-evidence",
            not machine_visual_errors,
            "Machine-owned visual evidence xác nhận viewport canonical và không có horizontal overflow."
            if not machine_visual_errors
            else "; ".join(machine_visual_errors),
            Path("_audit") / f"{target.stem}_visual" / "html_mobile_measurements.json",
        )

    visual_quality_status = "NOT_REQUIRED"
    if _truthy(profile_policy.get("require_self_view_evidence")):
        self_view_errors = _self_view_errors(
            root,
            profile,
            target,
            required_mobile_viewports=required_mobile_viewports,
            required_desktop_viewports=required_desktop_viewports,
            require_pdf_page_coverage=_truthy(profile_policy.get("require_pdf_page_coverage")),
            require_structured_self_review=_truthy(visual_policy.get("require_structured_self_review")),
            required_self_review_criteria=_mapping(visual_policy.get("required_self_review_criteria")),
        )
        visual_quality_status = "PASS" if not self_view_errors else "FAIL"
        add(
            "profile-agent-self-view-evidence",
            not self_view_errors,
            "Agent self-view có cấu trúc, bao phủ toàn bộ HTML canonical và mọi trang PDF."
            if not self_view_errors
            else "; ".join(self_view_errors),
            profile_rel,
        )

    authoring_quality_status = "NOT_REQUIRED"
    authoring_quality_policy = _mapping(policy.get("authoring_quality"))
    if _truthy(authoring_quality_policy.get("required")):
        authoring_quality_errors = _authoring_quality_self_review_errors(
            profile, authoring_quality_policy
        )
        authoring_quality_ok = not authoring_quality_errors
        authoring_quality_status = "PASS" if authoring_quality_ok else "FAIL"
        add(
            "authoring-quality-self-review",
            authoring_quality_ok,
            "Agent đã hoàn tất toàn bộ tự kiểm chất lượng biên tập bắt buộc và ghi căn cứ cụ thể."
            if authoring_quality_ok
            else "; ".join(authoring_quality_errors),
            profile_rel,
        )

    metadata_sync_status = "NOT_REQUIRED"
    metadata_sync_policy = _mapping(policy.get("metadata_sync"))
    if _truthy(metadata_sync_policy.get("required")):
        profile_key = metadata_sync_policy.get("profile_key", "dong_bo_metadata")
        sync_record = _mapping(profile.get(str(profile_key)))
        fields = metadata_sync_policy.get("descriptive_fields", [])
        descriptive_fields = (
            [str(value) for value in fields if isinstance(value, str) and value]
            if isinstance(fields, list)
            else []
        )
        required_status = metadata_sync_policy.get("required_agent_status", "dat")
        current_academic_hash = _academic_content_sha256(body)
        current_metadata_hash = _metadata_description_sha256(metadata, descriptive_fields)
        stored_academic = sync_record.get("noi_dung_hoc_thuat_sha256")
        stored_metadata = sync_record.get("metadata_mo_ta_sha256")
        status_ok = sync_record.get("trang_thai") == required_status
        academic_ok = (
            isinstance(stored_academic, str)
            and bool(re.fullmatch(r"[0-9a-fA-F]{64}", stored_academic.strip()))
            and stored_academic.strip().lower() == current_academic_hash
        )
        metadata_ok = (
            isinstance(stored_metadata, str)
            and bool(re.fullmatch(r"[0-9a-fA-F]{64}", stored_metadata.strip()))
            and stored_metadata.strip().lower() == current_metadata_hash
        )
        metadata_sync_ok = status_ok and academic_ok and metadata_ok
        metadata_sync_status = "PASS" if metadata_sync_ok else "FAIL"
        detail: list[str] = []
        if not status_ok:
            detail.append(f"{profile_key}.trang_thai phải bằng {required_status!r}")
        if not academic_ok:
            detail.append("fingerprint nội dung học thuật đã stale hoặc thiếu")
        if not metadata_ok:
            detail.append("fingerprint metadata mô tả đã stale hoặc thiếu")
        add(
            "post-content-metadata-sync",
            metadata_sync_ok,
            "Metadata mô tả đã được agent tái duyệt trên đúng nội dung học thuật hiện hành."
            if metadata_sync_ok
            else "; ".join(detail),
            profile_rel,
        )

    exercise_gate_status: dict[str, str] = {}
    exercise_policy = _mapping(policy.get("exercise_contract"))
    if _truthy(exercise_policy.get("required")):
        exercise_findings, exercise_gate_status = _exercise_contract_evaluation(
            body, profile, exercise_policy
        )
        for name, passed, message in exercise_findings:
            add(
                name,
                passed,
                message,
                target
                if name in {"exercise-qmd-inventory", "exercise-internal-label-leak"}
                else profile_rel,
            )

    semantic = _mapping(policy.get("semantic"))
    if _truthy(semantic.get("require_exercises_last_h2")):
        h2_titles = _markdown_h2_titles(body)
        exercise_positions = [index for index, title in enumerate(h2_titles) if title == "bài tập"]
        exercises_last = not exercise_positions or exercise_positions[-1] == len(h2_titles) - 1
        add(
            "semantic-exercises-last-h2",
            exercises_last,
            "Nếu có H2 Bài tập thì đó là H2 học thuật cuối của thân bài." if exercises_last
            else "Sau H2 Bài tập còn có H2 học thuật khác; Bài tập phải là H2 cuối.",
            target,
        )
    forbidden_public_headings = semantic.get("forbidden_public_heading_exact", [])
    if isinstance(forbidden_public_headings, list):
        forbidden_heading_set = {value.casefold().strip() for value in forbidden_public_headings if isinstance(value, str) and value.strip()}
        found_headings = sorted({title for title in _markdown_heading_titles(body) if title in forbidden_heading_set})
        add(
            "semantic-forbidden-public-heading",
            not found_headings,
            "Không dùng nhãn vận hành nội bộ làm heading công khai." if not found_headings else "Heading công khai không được dùng nhãn vận hành nội bộ: " + ", ".join(found_headings) + ".",
            target,
        )

    forbidden_tokens = semantic.get("forbidden_source_tokens", [])
    if isinstance(forbidden_tokens, list):
        found_tokens = [token for token in forbidden_tokens if isinstance(token, str) and token and token in text]
        add(
            "semantic-forbidden-source-tokens",
            not found_tokens,
            "Không có token kí hiệu bị cấm."
            if not found_tokens
            else "Phát hiện token bị cấm: " + ", ".join(found_tokens) + ".",
            target,
        )

    raw_unicode_symbols = semantic.get("forbidden_unicode_math_symbols", [])
    if isinstance(raw_unicode_symbols, list):
        unicode_symbols = [
            str(value) for value in raw_unicode_symbols
            if isinstance(value, str) and value
        ]
        unicode_violations = _unicode_math_violations(body, unicode_symbols)
        add(
            "latex-symbol-source",
            not unicode_violations,
            "Math source dùng lệnh LaTeX thay cho Unicode operator."
            if not unicode_violations
            else "Phát hiện Unicode operator trong math source: "
            + ", ".join(unicode_violations),
            target,
        )

    if _truthy(semantic.get("require_frac_command")):
        fraction_violations = _fraction_source_violations(body)
        add(
            "latex-fraction-contract",
            not fraction_violations,
            "Phân số trong math source dùng \\frac{...}{...}."
            if not fraction_violations
            else "Phát hiện cú pháp phân số ngoài contract: "
            + ", ".join(fraction_violations),
            target,
        )

    if _truthy(semantic.get("require_exercise_subitem_dot_style")):
        subitem_violations = _exercise_subitem_style_violations(body)
        add(
            "exercise-subitem-style",
            not subitem_violations,
            "Tiểu mục bài tập dùng a., b., c. thay cho a), b), c)."
            if not subitem_violations
            else "Phát hiện tiểu mục dùng dấu ngoặc: "
            + ", ".join(subitem_violations),
            target,
        )

    prime_violations = sorted(set(re.findall(r"(?<!\\)\b[A-Za-z][A-Za-z0-9_]*'{1,2}\s*\(", body)))
    add(
        "latex-prime-notation",
        not prime_violations,
        "Đạo hàm trong nội dung mới dùng cú pháp f^\\prime / f^{\\prime\\prime}."
        if not prime_violations
        else "Phát hiện cú pháp đạo hàm apostrophe bị cấm: " + ", ".join(prime_violations),
        target,
    )

    ambiguous_phrases = semantic.get("forbidden_ambiguous_phrases", [])
    if isinstance(ambiguous_phrases, list):
        profile_text = yaml.safe_dump(profile, allow_unicode=True, sort_keys=False) if yaml is not None else ""
        combined_semantic_text = (text + "\n" + profile_text).casefold()
        found_ambiguous = [
            phrase
            for phrase in ambiguous_phrases
            if isinstance(phrase, str) and phrase.strip() and phrase.casefold() in combined_semantic_text
        ]
        add(
            "semantic-ambiguous-relation-phrases",
            not found_ambiguous,
            "Không có cụm quan hệ mơ hồ bị cấu hình cấm."
            if not found_ambiguous
            else "Phát hiện cụm quan hệ mơ hồ: "
            + ", ".join(found_ambiguous)
            + ". Hãy nêu đúng đại lượng/đẳng thức bảo toàn hoặc dùng quan hệ xác định/khôi phục/phụ thuộc chính xác.",
            target,
        )

    if _truthy(semantic.get("require_relation_records_when_triggered")):
        central_parts: list[str] = []
        for key in ("subtitle", "summary", "description", "abstract"):
            value = metadata.get(key)
            if isinstance(value, str):
                central_parts.append(value)
        task = _mapping(profile.get("nhiem_vu"))
        if isinstance(task.get("muc_tieu"), str):
            central_parts.append(str(task["muc_tieu"]))
        cognition = _mapping(profile.get("truc_nhan_thuc"))
        phenomenon = _mapping(cognition.get("hien_tuong_trung_tam"))
        for value in (
            phenomenon.get("phat_bieu"),
            cognition.get("cau_hoi_dan_duong"),
            cognition.get("cau_tra_loi_da_kiem_tra"),
            cognition.get("nhan_thuc_co_the_chuyen_giao"),
        ):
            if isinstance(value, str):
                central_parts.append(value)
        terms = _relation_terms_present("\n".join(central_parts))
        if terms:
            relation_ok, relation_message = _relation_records_valid(profile)
            add(
                "semantic-central-relation-records",
                relation_ok,
                relation_message + " Tác nhân kích hoạt: " + ", ".join(terms) + ".",
                profile_rel,
            )
        else:
            add(
                "semantic-central-relation-records",
                True,
                "Không phát hiện động từ quan hệ trung tâm cần bản ghi bắt buộc trong QMD.",
                target,
            )

    failed = [item for item in checks if not item.passed]
    payload = {
        "review_ready_manifest_version": REVIEW_READY_VERSION,
        "project_id": config.project_id,
        "article_type": article_type.id,
        "target": target.as_posix(),
        "profile": profile_rel.as_posix(),
        "metadata_sync": metadata_sync_status,
        "authoring_quality": authoring_quality_status,
        "visual_quality": visual_quality_status,
        "checks": [item.__dict__ for item in checks],
        "exercise_contract": exercise_gate_status,
        "automated_result": "FAIL" if failed else "PASS",
        "human_review": "BLOCKED" if failed else "READY",
        "final_acceptance": "NOT_RUN",
        "publication": "pending",
        "exit_code": EXIT_FAILED if failed else EXIT_OK,
    }
    return checks, payload


def _report_path(root: Path, raw: str | None) -> Path | None:
    if raw is None:
        return None
    candidate = Path(raw).expanduser()
    resolved = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    audit = (root / "_audit").resolve()
    try:
        resolved.relative_to(audit)
    except ValueError as exc:
        raise ReviewReadyError("--report phải là tệp .json bên trong _audit/.") from exc
    if resolved.suffix.lower() != ".json":
        raise ReviewReadyError("--report phải là tệp .json bên trong _audit/.")
    return resolved


def command_check(
    root: Path, raw_target: str, raw_report: str | None, raw_session: str | None
) -> int:
    target = _relative_to_root(root, raw_target)
    if target.suffix.lower() != ".qmd":
        raise ReviewReadyError("review-ready chỉ nhận một tệp .qmd.")
    session = _session_path(root, target, raw_session)
    checks, payload = evaluate_review_ready(root, target, session)
    report = _report_path(root, raw_report)
    if report is not None:
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"REVIEW-READY REPORT: {report}")

    for item in checks:
        prefix = "PASS" if item.passed else "FAIL"
        path = f" [{item.path}]" if item.path else ""
        print(f"{prefix} {item.name}{path}: {item.message}")
    print(
        f"REVIEW-READY RESULT: {payload['automated_result']} "
        f"| HUMAN_REVIEW={payload['human_review']} | EXIT={payload['exit_code']}"
    )
    return int(payload["exit_code"])


def _git(root: Path, *arguments: str) -> None:
    result = _run(["git", *arguments], root)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Git command failed.")


def _write_yaml(path: Path, value: Mapping[str, Any]) -> None:
    assert yaml is not None
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(dict(value), allow_unicode=True, sort_keys=False), encoding="utf-8")


def command_exercise_hash(root: Path, raw_path: str) -> int:
    target = _relative_to_root(root, raw_path)
    qmd = root / target
    if not qmd.is_file():
        raise ReviewReadyError(f"Không tìm thấy bài QMD: {target.as_posix()}.")
    text = qmd.read_text(encoding="utf-8")
    metadata, body, error = split_qmd_front_matter(text)
    if error or metadata is None:
        raise ReviewReadyError(error or "Không đọc được YAML front matter.")
    academic_digest = _academic_content_sha256(body)
    exercise_digest = _exercise_content_sha256(body)
    print(f"TARGET={target.as_posix()}")
    print(f"EXERCISE_ACADEMIC_CONTENT_SHA256={academic_digest}")
    print(f"EXERCISE_SECTION_SHA256={exercise_digest}")
    return EXIT_OK


def command_metadata_hash(root: Path, raw_path: str) -> int:
    target = _relative_to_root(root, raw_path)
    qmd = root / target
    if not qmd.is_file():
        raise ReviewReadyError(f"Không tìm thấy bài QMD: {target.as_posix()}.")
    config = discover_project_config(root, target)
    if config is None:
        raise ReviewReadyError(f"Không tìm thấy cấu hình dự án cho {target.as_posix()}.")
    article_type = config.article_type_for(target)
    if article_type is None:
        raise ReviewReadyError(f"Bài không khớp loại bài đã cấu hình: {target.as_posix()}.")
    policy = _extension_policy(config.raw, article_type.id)
    sync_policy = _mapping(policy.get("metadata_sync"))
    fields = sync_policy.get("descriptive_fields", [])
    descriptive_fields = (
        [str(value) for value in fields if isinstance(value, str) and value]
        if isinstance(fields, list)
        else []
    )
    text = qmd.read_text(encoding="utf-8")
    metadata, body, error = split_qmd_front_matter(text)
    if error or metadata is None:
        raise ReviewReadyError(error or "Không đọc được YAML front matter.")
    print(f"TARGET={target.as_posix()}")
    print(f"METADATA_ACADEMIC_CONTENT_SHA256={_academic_content_sha256(body)}")
    print(
        "METADATA_DESCRIPTION_SHA256="
        + _metadata_description_sha256(metadata, descriptive_fields)
    )
    print("METADATA_DESCRIPTION_FIELDS=" + ",".join(descriptive_fields))
    return EXIT_OK


def _self_test() -> None:
    if yaml is None:
        raise RuntimeError("Thiếu PyYAML.")
    if shutil.which("git") is None:
        raise RuntimeError("Không tìm thấy Git trong PATH.")

    with tempfile.TemporaryDirectory(prefix="zo-qmd-review-") as raw:
        root = Path(raw)
        _git(root, "init", "-q")
        _git(root, "config", "user.name", "ZO Math Self Test")
        _git(root, "config", "user.email", "self-test@example.invalid")
        (root / "AGENTS.md").write_text("Self-test authority.\n", encoding="utf-8")
        exercise_authority = root / "quy_trinh_xay_dung/quy_chuan_he_bai_tap.md"
        exercise_authority.parent.mkdir(parents=True, exist_ok=True)
        exercise_authority.write_text("# Exercise Contract self-test\n", encoding="utf-8")

        project = Path("content/functions")
        target = project / "core/test.qmd"
        profile_rel = project / "_quy_trinh/ho_so/test.yml"
        graph_base = project / "_figures/test"
        graph_src = graph_base / "src/do_thi_test.tex"
        graph_pdf = graph_base / "pdf/do_thi_test.pdf"
        graph_svg = graph_base / "svg/do_thi_test.svg"

        config = {
            "schema_version": 1,
            "project": {"id": "test-functions", "name": "Test", "root": project.as_posix()},
            "discovery": {"article_types": [{"id": "function_article", "include": ["core/*.qmd"], "exclude": []}]},
            "profiles": {"directory": "_quy_trinh/ho_so", "naming": "by_article_stem", "required": True},
            "modules": {"required": ["qmd-core", "zo-html-pdf", "content-blocks", "functions-article"], "optional": []},
            "metadata": {"core_required": ["title"], "project_required": [], "body_classes_required": [], "placeholders": []},
            "publication": {"production_states": ["draft", "in_production", "validated", "accepted"], "publication_states": ["pending", "published"], "user_confirmation_required": True},
            "references": {"controlling_documents": [], "templates": [], "theory_sources": [], "quality_exemplars": []},
            "authority_registry": {
                "schema_version": 1,
                "governing_required": [
                    {
                        "path": "quy_trinh_xay_dung/quy_chuan_he_bai_tap.md",
                        "reason": "exercise_system_contract",
                    }
                ],
                "conditional_required": [],
                "provenance_required": [],
                "reference_only": [
                    {
                        "path": "content/functions/_quy_trinh/theory.qmd",
                        "reason": "self_test_reference",
                    }
                ],
            },
            "regression": {"articles": ["core/test.qmd"], "expected_checker_version": "2.6.0", "preserve_cli": True},
            "extensions": {
                "human_review_gate": {
                    "enabled": True,
                    "article_types": {
                        "function_article": {
                            "navigation": {"explicit_sidebar_required": True, "quarto_config": "_quarto.yml"},
                            "pdf": {
                                "download_required": True,
                                "require_canonical_build_receipt": True,
                                "plain_metadata_fields": ["title-meta", "pagetitle"],
                            },
                            "lifecycle": {
                                "require_session_manifest": True,
                                "auto_scope": True,
                                "manual_scope_extensions": False,
                                "require_clean_candidate_scope_at_start": True,
                                "enforce_scope_delta": True,
                                "require_authority_snapshot": True,
                                "forbidden_review_copy_markers": [
                                    "human_review",
                                    "owner_review",
                                    "review_copy",
                                ],
                            },
                            "function_graph": {
                                "required": True,
                                "require_default_chain": True,
                                "require_graph_standard": True,
                                "require_graph_core_style": True,
                                "canonical_root_required": True,
                            },
                            "visual": {
                                "require_machine_measurements": True,
                                "require_full_html_capture": True,
                                "require_structured_self_review": True,
                                "required_mobile_viewports": [390, 430],
                                "required_desktop_viewports": [1440],
                                "required_self_review_criteria": {
                                    "html_desktop": ["VD01"],
                                    "html_mobile": ["VM01"],
                                    "pdf": ["VP01", "VP02"],
                                },
                            },
                            "profile": {
                                "required_version": 10,
                                "required_top_level": [
                                    "tai_lieu_dieu_khien",
                                    "tai_nguyen_hinh",
                                    "he_thong_bai_tap",
                                    "kiem_tra_quan_he_trung_tam",
                                    "tu_kiem_noi_dung",
                                    "dong_bo_metadata",
                                    "tu_xem",
                                    "van_de_he_thong",
                                ],
                                "forbidden_top_level": ["nghiem_thu", "ban_giao"],
                                "require_check_and_render_evidence": True,
                                "require_self_view_evidence": True,
                                "require_pdf_page_coverage": True,
                            },
                            "metadata_sync": {
                                "required": True,
                                "profile_key": "dong_bo_metadata",
                                "required_agent_status": "dat",
                                "descriptive_fields": [
                                    "subtitle",
                                    "summary",
                                    "description",
                                    "abstract",
                                    "keywords",
                                ],
                            },
                            "authoring_quality": {
                                "required": True,
                                "profile_key": "tu_kiem_noi_dung",
                                "required_section_status": "dat",
                                "required_criterion_status": "dat",
                                "require_criterion_evidence": True,
                                "required_criteria": {
                                    "mach_giai_thich": ["MG10"],
                                },
                            },
                            "exercise_contract": {
                                "required": True,
                                "profile_key": "he_thong_bai_tap",
                                "authority_profile_key": "quy_chuan_he_bai_tap",
                                "authority_path": "quy_trinh_xay_dung/quy_chuan_he_bai_tap.md",
                                "required_agent_status": "dat",
                                "forbidden_public_heading_exact": [
                                    "tái dựng",
                                    "phát triển",
                                    "mạch cốt lõi",
                                    "mắt xích cốt lõi",
                                    "đồng bộ hệ bài tập",
                                ],
                                "forbidden_public_heading_prefixes": [
                                    "tái dựng mạch cốt lõi",
                                    "phần phát triển",
                                ],
                            },
                            "semantic": {
                                "require_relation_records_when_triggered": True,
                                "require_exercises_last_h2": True,
                                "forbidden_public_heading_exact": ["kết tinh"],
                                "forbidden_source_tokens": ["\\longmapsto", "\\Longleftrightarrow", "\\iff"],
                                "forbidden_ambiguous_phrases": [
                                    "giữ độ lớn",
                                    "giữ nguyên độ lớn",
                                    "bảo toàn độ lớn",
                                    "không xóa độ lớn",
                                ],
                                "forbidden_unicode_math_symbols": [
                                    "∞", "≤", "≥", "≠", "→", "↦", "⇔",
                                    "∈", "∉", "∅", "∪", "∩", "√", "±", "×", "·",
                                ],
                                "require_frac_command": True,
                                "require_exercise_subitem_dot_style": True,
                            },
                        }
                    },
                }
            },
        }
        _write_yaml(root / project / "_quy_trinh/cau_hinh_san_xuat_qmd.yml", config)
        theory_file = root / project / "_quy_trinh/theory.qmd"
        theory_file.write_text("# Theory reference\n", encoding="utf-8")
        _write_yaml(
            root / "_quarto.yml",
            {
                "project": {"type": "website", "output-dir": "docs"},
                "website": {"sidebar": [{"contents": [{"href": target.as_posix()}]}]},
            },
        )

        qmd = root / target
        qmd.parent.mkdir(parents=True, exist_ok=True)
        qmd.write_text(
            "---\ntitle: Test\ntitle-meta: \"Test\"\npagetitle: \"Test\"\nsubtitle: \"Đầu ra xác định được từ quan hệ này\"\nsummary: \"Quan hệ trung tâm của bài.\"\ndescription: \"Bài làm rõ quan hệ trung tâm và hệ quả.\"\nabstract: \"Quan hệ trung tâm được khảo sát theo mạch lập luận.\"\nkeywords:\n  - quan hệ\nzo-pdf-download:\n  href: test.pdf\n---\n\n"
            "Quan hệ này xác định được từ đầu ra.\n\n"
            "![](%s){fig-alt=\"Đồ thị thử\"}\n\n"
            "## Bài tập\n\n"
            "### Quan hệ và đồ thị\n\n"
            "#### Bài 1. Dựng lại quan hệ và đi tiếp\n\n"
            "Tái lập quan hệ trung tâm rồi nêu một hệ quả mới.\n"
            % ("../_figures/test/svg/do_thi_test.svg"),
            encoding="utf-8",
        )
        (root / graph_src).parent.mkdir(parents=True, exist_ok=True)
        (root / graph_pdf).parent.mkdir(parents=True, exist_ok=True)
        (root / graph_svg).parent.mkdir(parents=True, exist_ok=True)
        graph_source_text = r"""\documentclass[tikz,border=3pt,10pt]{standalone}
\usepackage{fontspec}
\usepackage{unicode-math}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\setmainfont{STIXTwoText-Regular.otf}
\setmathfont{STIXTwoMath.otf}
\usetikzlibrary{backgrounds}
\definecolor{zoPlotBackground}{HTML}{FFF9E9}
\definecolor{zoPlotBorder}{HTML}{DFD7CA}
\definecolor{zoAxis}{HTML}{554F48}
\definecolor{zoText}{HTML}{3E3A35}
\definecolor{zoGraphMain}{HTML}{EF5350}
\pgfplotsset{
  zo axis/.style={
    axis lines=middle,
    axis line style={draw=zoAxis,line width=0.8pt,<->},
    tickwidth=0.4mm,
    tick style={draw=zoAxis,line width=0.32pt},
    grid=none,
    enlargelimits=false,
    clip=true,
    clip mode=individual
  },
  zo graph main/.style={draw=zoGraphMain,line width=1.2pt,solid,no marks}
}
\tikzset{
  zo graph field/.style={
    show background rectangle,
    inner frame sep=4mm,
    background rectangle/.style={
      fill=zoPlotBackground,
      draw=zoPlotBorder,
      line width=0.45pt,
      rounded corners=2mm
    }
  }
}
\begin{document}
\begin{tikzpicture}[zo graph field]
\begin{axis}[zo axis,xtick={-1,1},ytick={-1,1},xticklabel=\empty,yticklabel=\empty]
\addplot[zo graph main,domain=-1:1]{x^2};
\end{axis}
\end{tikzpicture}
\end{document}
"""
        (root / graph_src).write_text(graph_source_text, encoding="utf-8")
        (root / graph_pdf).write_bytes(b"%PDF-1.4\ngraph\n")
        (root / graph_svg).write_text("<svg xmlns='http://www.w3.org/2000/svg'></svg>\n", encoding="utf-8")
        for pipeline_input in CANONICAL_PDF_PIPELINE_INPUTS:
            pipeline_file = root / pipeline_input
            pipeline_file.parent.mkdir(parents=True, exist_ok=True)
            pipeline_file.write_text(
                f"self-test pipeline input: {pipeline_input.as_posix()}\n",
                encoding="utf-8",
            )
        article_pdf = root / target.with_suffix(".pdf")

        def write_blank_pdf(path: Path, page_count: int) -> None:
            objects: list[bytes] = []
            page_ids = list(range(3, 3 + page_count))
            content_id = 3 + page_count
            objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
            kids = b" ".join(f"{page_id} 0 R".encode("ascii") for page_id in page_ids)
            objects.append(b"<< /Type /Pages /Count " + str(page_count).encode("ascii") + b" /Kids [" + kids + b"] >>")
            for _page_id in page_ids:
                objects.append(b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents " + str(content_id).encode("ascii") + b" 0 R >>")
            objects.append(b"<< /Length 0 >>\nstream\n\nendstream")
            data = bytearray(b"%PDF-1.4\n")
            offsets = [0]
            for object_id, obj in enumerate(objects, start=1):
                offsets.append(len(data))
                data.extend(f"{object_id} 0 obj\n".encode("ascii"))
                data.extend(obj)
                data.extend(b"\nendobj\n")
            xref = len(data)
            data.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
            data.extend(b"0000000000 65535 f \n")
            for offset in offsets[1:]:
                data.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
            data.extend((f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n").encode("ascii"))
            path.write_bytes(bytes(data))

        write_blank_pdf(article_pdf, 2)
        pdf_receipt = write_pdf_build_receipt(root, qmd, article_pdf)
        html = root / "docs" / target.with_suffix(".html")
        html.parent.mkdir(parents=True, exist_ok=True)
        html.write_text('<html><nav id="quarto-sidebar"></nav></html>\n', encoding="utf-8")

        audit = root / "_audit"
        audit.mkdir(exist_ok=True)
        for mode, name in (("scope", "test_check.json"), ("render", "test_render.json")):
            (audit / name).write_text(
                json.dumps(
                    {
                        "mode": mode,
                        "automated_result": "PASS_WITH_WARNINGS",
                        "exit_code": 0,
                        "scope": [target.as_posix()],
                    }
                ),
                encoding="utf-8",
            )
        visual = audit / "test_visual"
        visual.mkdir()

        def write_png_stub(path: Path, width: int, height: int) -> None:
            path.write_bytes(
                b"\x89PNG\r\n\x1a\n"
                + (13).to_bytes(4, "big")
                + b"IHDR"
                + width.to_bytes(4, "big")
                + height.to_bytes(4, "big")
                + b"\x08\x06\x00\x00\x00"
            )

        write_png_stub(visual / "pdf_page_1.png", 612, 792)
        write_png_stub(visual / "pdf_page_2.png", 612, 792)

        visual_records: list[dict[str, Any]] = []
        html_segments: list[dict[str, Any]] = []
        for viewport_class, width in (("mobile", 390), ("mobile", 430), ("desktop", 1440)):
            screenshot = visual / f"html_{viewport_class}_{width}.png"
            segment = visual / f"html_{viewport_class}_{width}_part_001.png"
            write_png_stub(screenshot, width, 1000)
            write_png_stub(segment, width, 1000)
            visual_records.append(
                {
                    "viewport_class": viewport_class,
                    "requested_width": width,
                    "requested_height": 1000,
                    "window_inner_width": width,
                    "document_client_width": width,
                    "document_scroll_width": width,
                    "document_scroll_height": 1000,
                    "horizontal_overflow": False,
                    "overflow_px": 0,
                    "offender_count": 0,
                    "offenders": [],
                    "screenshot": f"_audit/test_visual/html_{viewport_class}_{width}.png",
                    "screenshot_sha256": _sha256_file(screenshot),
                    "passed": True,
                }
            )
            html_segments.append(
                {
                    "viewport_class": viewport_class,
                    "requested_width": width,
                    "segment_index": 1,
                    "requested_top": 0,
                    "actual_top": 0,
                    "requested_height": 1000,
                    "document_scroll_height": 1000,
                    "screenshot": f"_audit/test_visual/html_{viewport_class}_{width}_part_001.png",
                    "screenshot_sha256": _sha256_file(segment),
                }
            )
        visual_report = visual / "html_mobile_measurements.json"
        visual_report.write_text(
            json.dumps(
                {
                    "visual_measurement_version": VISUAL_MEASUREMENT_VERSION,
                    "generator": "scripts/zo_qmd_visual.ps1",
                    "target": target.as_posix(),
                    "rendered_html": (Path("docs") / target.with_suffix(".html")).as_posix(),
                    "rendered_html_sha256": _sha256_file(html),
                    "required_mobile_viewports": [390, 430],
                    "required_desktop_viewports": [1440],
                    "measurements": visual_records,
                    "html_segments": html_segments,
                    "rendered_pdf": target.with_suffix(".pdf").as_posix(),
                    "rendered_pdf_sha256": _sha256_file(article_pdf),
                    "pdf_page_count": 2,
                    "pdf_pages": [
                        {"page": 1, "screenshot": "_audit/test_visual/pdf_page_1.png", "screenshot_sha256": _sha256_file(visual / "pdf_page_1.png")},
                        {"page": 2, "screenshot": "_audit/test_visual/pdf_page_2.png", "screenshot_sha256": _sha256_file(visual / "pdf_page_2.png")},
                    ],
                    "automated_result": "PASS",
                    "exit_code": 0,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        profile = {
            "phien_ban_ho_so": 10,
            "tai_lieu_dieu_khien": {
                "quy_chuan_do_thi": {"kich_hoat": True, "da_doc": True},
                "quy_chuan_he_bai_tap": {
                    "duong_dan": "quy_trinh_xay_dung/quy_chuan_he_bai_tap.md",
                    "da_doc": True,
                },
                "nguon_li_thuyet_day_du": {"duong_dan": "content/functions/_quy_trinh/theory.qmd", "da_dung": False, "vi_tri_da_dung": []},
            },
            "tai_nguyen_hinh": {"co_su_dung": True, "ap_dung_cau_truc_mac_dinh": True, "li_do_ngoai_le": None},
            "he_thong_bai_tap": {
                "kich_hoat": True,
                "trang_thai_thiet_ke": "dat",
                "nhom_bai": [
                    {
                        "ten": "Quan hệ và đồ thị",
                        "bai_so": [1],
                        "muc_tieu": "Tái dựng rồi phát triển từ quan hệ trung tâm.",
                    }
                ],
                "hop_dong": {
                    "mach_cot_loi": [
                        {"id": "MX01", "noi_dung": "Quan hệ trung tâm của bài."}
                    ],
                    "bai_tap": [
                        {
                            "so": 1,
                            "chuc_nang": ["tai_dung", "phat_trien"],
                            "tai_dung_mat_xich": ["MX01"],
                            "phat_trien_tu_mat_xich": ["MX01"],
                        }
                    ],
                    "xac_nhan_agent": {
                        "tai_dung": "dat",
                        "phat_trien": "dat",
                        "dong_bo": "dat",
                    },
                    "dong_bo": {
                        "noi_dung_hoc_thuat_sha256": None,
                        "noi_dung_bai_tap_sha256": None,
                    },
                },
            },
            "kiem_tra_quan_he_trung_tam": [
                {"phat_bieu": "Đầu ra xác định được đại lượng.", "phep_thu": "Dựng công thức khôi phục.", "ket_luan": "Có công thức khôi phục.", "trang_thai": "dat"}
            ],
            "tu_kiem_noi_dung": {
                "mach_giai_thich": {
                    "trang_thai": "dat",
                    "tieu_chi": [
                        {
                            "id": "MG10",
                            "noi_dung": "ham_phu_va_ten_phu_chi_dung_khi_giam_tai_nhan_thuc",
                            "trang_thai": "dat",
                            "can_cu": ["Không dùng tên phụ trong bài self-test; quan hệ được viết trực tiếp."],
                            "hanh_dong_sua": None,
                        }
                    ],
                }
            },
            "dong_bo_metadata": {
                "trang_thai": "dat",
                "noi_dung_hoc_thuat_sha256": None,
                "metadata_mo_ta_sha256": None,
            },
            "tu_xem": {
                "trang_thai": "dat",
                "html_desktop": {
                    "trang_thai": "dat",
                    "viewports": [
                        {
                            "width": 1440,
                            "trang_thai": "dat",
                            "da_xem_den_cuoi": True,
                            "can_cu": ["_audit/test_visual/html_desktop_1440_part_001.png"],
                        }
                    ],
                    "tieu_chi": [
                        {
                            "id": "VD01",
                            "noi_dung": "da_xem_toan_bai_theo_bang_chung_machine_owned",
                            "trang_thai": "dat",
                            "can_cu": ["_audit/test_visual/html_desktop_1440_part_001.png"],
                            "hanh_dong_sua": None,
                        }
                    ],
                },
                "html_mobile": {
                    "trang_thai": "dat",
                    "viewports": [
                        {
                            "width": 390,
                            "trang_thai": "dat",
                            "da_xem_den_cuoi": True,
                            "can_cu": ["_audit/test_visual/html_mobile_390_part_001.png"],
                        },
                        {
                            "width": 430,
                            "trang_thai": "dat",
                            "da_xem_den_cuoi": True,
                            "can_cu": ["_audit/test_visual/html_mobile_430_part_001.png"],
                        },
                    ],
                    "tieu_chi": [
                        {
                            "id": "VM01",
                            "noi_dung": "da_xem_toan_bai_o_cac_viewport_mobile_canonical",
                            "trang_thai": "dat",
                            "can_cu": [
                                "_audit/test_visual/html_mobile_390_part_001.png",
                                "_audit/test_visual/html_mobile_430_part_001.png",
                            ],
                            "hanh_dong_sua": None,
                        }
                    ],
                },
                "pdf": {
                    "trang_thai": "dat",
                    "trang": [
                        {"so": 1, "trang_thai": "dat", "can_cu": "_audit/test_visual/pdf_page_1.png"},
                        {"so": 2, "trang_thai": "dat", "can_cu": "_audit/test_visual/pdf_page_2.png"},
                    ],
                    "tieu_chi": [
                        {
                            "id": "VP01",
                            "noi_dung": "da_xem_du_tat_ca_trang_pdf",
                            "trang_thai": "dat",
                            "can_cu": ["_audit/test_visual/pdf_page_1.png", "_audit/test_visual/pdf_page_2.png"],
                            "hanh_dong_sua": None,
                        },
                        {
                            "id": "VP02",
                            "noi_dung": "khoi_noi_dung_khong_bi_cat_hoac_vo_bat_hop_li",
                            "trang_thai": "dat",
                            "can_cu": ["_audit/test_visual/pdf_page_1.png", "_audit/test_visual/pdf_page_2.png"],
                            "hanh_dong_sua": None,
                        },
                    ],
                },
                "bang_chung": [
                    "_audit/test_visual/html_mobile_measurements.json",
                    "_audit/test_visual/html_desktop_1440.png",
                    "_audit/test_visual/html_mobile_390.png",
                    "_audit/test_visual/html_mobile_430.png",
                ],
                "canh_bao": [],
            },
            "van_de_he_thong": [],
        }
        _metadata, academic_body, academic_error = split_qmd_front_matter(
            qmd.read_text(encoding="utf-8")
        )
        assert not academic_error and _metadata is not None
        profile["he_thong_bai_tap"]["hop_dong"]["dong_bo"][
            "noi_dung_hoc_thuat_sha256"
        ] = _academic_content_sha256(academic_body)
        profile["he_thong_bai_tap"]["hop_dong"]["dong_bo"][
            "noi_dung_bai_tap_sha256"
        ] = _exercise_content_sha256(academic_body)
        metadata_policy = config["extensions"]["human_review_gate"]["article_types"][
            "function_article"
        ]["metadata_sync"]
        profile["dong_bo_metadata"]["noi_dung_hoc_thuat_sha256"] = (
            _academic_content_sha256(academic_body)
        )
        profile["dong_bo_metadata"]["metadata_mo_ta_sha256"] = (
            _metadata_description_sha256(
                _metadata,
                metadata_policy["descriptive_fields"],
            )
        )
        _write_yaml(root / profile_rel, profile)

        # Commit source + generated artifacts together so freshness is Git-stable.
        _git(root, "add", ".")
        _git(root, "commit", "-q", "-m", "baseline")

        session_rel = Path("_audit/test_session.json")
        expected_scope = [
            target,
            profile_rel,
            target.with_suffix(".pdf"),
            graph_base,
            Path("_quarto.yml"),
        ]
        authority_records = _expected_authority_records(root, target, discover_project_config(root, target))
        session_payload = {
            "session_manifest_version": SESSION_MANIFEST_VERSION,
            "repository": {
                "commit": _git_text(root, "rev-parse", "HEAD"),
                "dirty_fingerprints": {},
            },
            "inspect": {
                "article_type": "function_article",
                "project": {"id": "test-functions"},
            },
            "authority_sources": {
                "snapshot": [
                    {
                        "path": item["path"].as_posix(),
                        "sha256": _sha256_file(root / item["path"]),
                        "size": (root / item["path"]).stat().st_size,
                        "role": item["role"],
                        "reason": item["reason"],
                        "lock": item["lock"],
                    }
                    for item in authority_records
                    if (root / item["path"]).is_file()
                ]
            },
            "scope": {
                "target": target.as_posix(),
                "strategy": "canonical",
                "allowed": [path.as_posix() for path in expected_scope],
                "excluded": [],
                "evidence_roots": ["_audit"],
                "initial_scope_dirty": [],
            },
        }
        (root / session_rel).write_text(json.dumps(session_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 0, [item for item in checks if not item.passed]
        assert payload["metadata_sync"] == "PASS"
        assert payload["authoring_quality"] == "PASS"
        assert any(
            item.name == "authoring-quality-self-review" and item.passed
            for item in checks
        )
        assert payload["exercise_contract"] == {
            "CORE_RECONSTRUCTION": "PASS",
            "CORE_DEVELOPMENT": "PASS",
            "EXERCISE_CONTENT_SYNC": "PASS",
        }
        assert any(
            item.name == "pdf-canonical-build-receipt" and item.passed
            for item in checks
        )
        assert any(
            item.name == "pdf-metadata-latex-compatibility" and item.passed
            for item in checks
        )
        assert any(item.name == "latex-symbol-source" and item.passed for item in checks)
        assert any(item.name == "latex-fraction-contract" and item.passed for item in checks)
        assert any(item.name == "exercise-subitem-style" and item.passed for item in checks)
        assert any(item.name == "human-review-copy-storage" and item.passed for item in checks)

        # Authoring-quality self-review without concrete evidence must block.
        quality_evidence = profile["tu_kiem_noi_dung"]["mach_giai_thich"]["tieu_chi"][0]["can_cu"]
        profile["tu_kiem_noi_dung"]["mach_giai_thich"]["tieu_chi"][0]["can_cu"] = []
        _write_yaml(root / profile_rel, profile)
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert payload["authoring_quality"] == "FAIL"
        assert any(
            item.name == "authoring-quality-self-review" and not item.passed
            for item in checks
        )
        profile["tu_kiem_noi_dung"]["mach_giai_thich"]["tieu_chi"][0]["can_cu"] = quality_evidence
        _write_yaml(root / profile_rel, profile)

        # Canonical PDF provenance is mandatory. A missing receipt must block.
        receipt_backup = pdf_receipt.read_bytes()
        pdf_receipt.unlink()
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(
            item.name == "pdf-canonical-build-receipt" and not item.passed
            for item in checks
        )
        pdf_receipt.write_bytes(receipt_backup)

        # Drift in any canonical PDF pipeline input invalidates the receipt.
        pipeline_probe = root / CANONICAL_PDF_PIPELINE_INPUTS[0]
        pipeline_backup = pipeline_probe.read_bytes()
        pipeline_probe.write_bytes(pipeline_backup + b"drift\n")
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(
            item.name == "pdf-canonical-build-receipt" and not item.passed
            for item in checks
        )
        pipeline_probe.write_bytes(pipeline_backup)

        # Human Review copies belong outside production candidate directories.
        review_copy = qmd.parent / "test_human_review.pdf"
        review_copy.write_bytes(b"%PDF-1.4\nreview-copy\n")
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(
            item.name == "human-review-copy-storage" and not item.passed
            for item in checks
        )
        review_copy.unlink()

        baseline_qmd_text = qmd.read_text(encoding="utf-8")

        # Metadata-only drift must invalidate post-content metadata synchronization.
        qmd.write_text(
            baseline_qmd_text.replace(
                'summary: "Quan hệ trung tâm của bài."',
                'summary: "Quan hệ trung tâm của bài đã được diễn đạt lại."',
            ),
            encoding="utf-8",
        )
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(
            item.name == "post-content-metadata-sync" and not item.passed
            for item in checks
        )
        qmd.write_text(baseline_qmd_text, encoding="utf-8")

        # Plain PDF metadata must not carry raw TeX.
        qmd.write_text(
            baseline_qmd_text.replace(
                'title-meta: "Test"',
                'title-meta: "$x$"',
            ),
            encoding="utf-8",
        )
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(
            item.name == "pdf-metadata-latex-compatibility" and not item.passed
            for item in checks
        )
        assert "title-meta" in pdf_plain_metadata_violations(root, target)
        # summary/description are learner-facing prose and may contain
        # ordinary LaTeX math. Only actual PDF-string metadata fields
        # such as title-meta/pagetitle remain plain-text constrained.
        qmd.write_text(
            baseline_qmd_text.replace(
                'summary: "Quan hệ trung tâm của bài."',
                'summary: "Quan hệ $x$ của bài."',
            ),
            encoding="utf-8",
        )
        assert "summary" not in pdf_plain_metadata_violations(root, target)

        qmd.write_text(
            baseline_qmd_text.replace(
                'description: "Bài làm rõ quan hệ trung tâm và hệ quả."',
                'description: "Bài khảo sát hàm $y=x^3$ và hệ quả."',
            ),
            encoding="utf-8",
        )
        assert "description" not in pdf_plain_metadata_violations(root, target)
        qmd.write_text(baseline_qmd_text, encoding="utf-8")

        # Unicode operators inside math source must use LaTeX commands instead.
        qmd.write_text(baseline_qmd_text + "\n$x → ∞$.\n", encoding="utf-8")
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "latex-symbol-source" and not item.passed for item in checks)
        qmd.write_text(baseline_qmd_text, encoding="utf-8")

        # Inline quotient source must use \frac rather than slash/dfrac/tfrac.
        qmd.write_text(baseline_qmd_text + "\n$x/2$.\n", encoding="utf-8")
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(
            item.name == "latex-fraction-contract" and not item.passed
            for item in checks
        )
        qmd.write_text(baseline_qmd_text, encoding="utf-8")

        # Exercise subitems use a., b., c.; parenthesized markers are rejected.
        qmd.write_text(
            baseline_qmd_text.replace(
                "Tái lập quan hệ trung tâm rồi nêu một hệ quả mới.",
                "a) Tái lập quan hệ trung tâm.\n\nb) Nêu một hệ quả mới.",
            ),
            encoding="utf-8",
        )
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(
            item.name == "exercise-subitem-style" and not item.passed
            for item in checks
        )
        qmd.write_text(baseline_qmd_text, encoding="utf-8")

        # Exercise Contract: structural checks do not replace agent judgment.
        broken = _load_yaml(root / profile_rel, "profile")
        broken["he_thong_bai_tap"]["hop_dong"]["xac_nhan_agent"]["tai_dung"] = "chua_thuc_hien"
        _write_yaml(root / profile_rel, broken)
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "exercise-core-reconstruction" and not item.passed for item in checks)
        _write_yaml(root / profile_rel, profile)

        # Academic-body drift before H2 Bài tập invalidates synchronization.
        safe_qmd_text = qmd.read_text(encoding="utf-8")
        qmd.write_text(
            safe_qmd_text.replace(
                "Quan hệ này xác định được từ đầu ra.",
                "Quan hệ này xác định được từ đầu ra và có thêm một mệnh đề học thuật.",
            ),
            encoding="utf-8",
        )
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "exercise-content-sync" and not item.passed for item in checks)
        qmd.write_text(safe_qmd_text, encoding="utf-8")

        # Exercise-text drift with unchanged H2/H3/H4 inventory also invalidates sync.
        qmd.write_text(
            safe_qmd_text.replace(
                "Tái lập quan hệ trung tâm rồi nêu một hệ quả mới.",
                "Tái lập đầy đủ quan hệ trung tâm rồi nêu một hệ quả mới.",
            ),
            encoding="utf-8",
        )
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "exercise-content-sync" and not item.passed for item in checks)
        qmd.write_text(safe_qmd_text, encoding="utf-8")

        # Internal design labels must not leak into learner-facing headings.
        qmd.write_text(
            safe_qmd_text.replace(
                "### Quan hệ và đồ thị",
                "### Tái dựng mạch cốt lõi",
            ),
            encoding="utf-8",
        )
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "exercise-internal-label-leak" and not item.passed for item in checks)
        qmd.write_text(safe_qmd_text, encoding="utf-8")

        # Profile schema ownership is strict: missing agent-owned groups or
        # agent-authored acceptance state must block.
        broken = _load_yaml(root / profile_rel, "profile")
        broken.pop("tu_xem")
        _write_yaml(root / profile_rel, broken)
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "profile-schema-required-top-level" and not item.passed for item in checks)
        _write_yaml(root / profile_rel, profile)

        broken = _load_yaml(root / profile_rel, "profile")
        broken["nghiem_thu"] = {"ket_luan": "ĐẠT"}
        _write_yaml(root / profile_rel, broken)
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "profile-schema-ownership-boundary" and not item.passed for item in checks)
        _write_yaml(root / profile_rel, profile)

        # Optional full-theory provenance is only enforced when the agent says it
        # was used; then the session reference inventory, path and concrete
        # positions must agree.
        used_theory = _load_yaml(root / profile_rel, "profile")
        used_theory["tai_lieu_dieu_khien"]["nguon_li_thuyet_day_du"]["da_dung"] = True
        used_theory["tai_lieu_dieu_khien"]["nguon_li_thuyet_day_du"]["vi_tri_da_dung"] = ["Mục thử"]
        _write_yaml(root / profile_rel, used_theory)
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 0, [item for item in checks if not item.passed]
        theory_text = theory_file.read_text(encoding="utf-8")
        theory_file.write_text(theory_text + "drift\n", encoding="utf-8")
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "profile-theory-reference-provenance" and not item.passed for item in checks)
        theory_file.write_text(theory_text, encoding="utf-8")
        _write_yaml(root / profile_rel, profile)

        # A new change outside the canonical production scope must block.
        outside = root / "OUTSIDE.txt"
        outside.write_text("should be blocked\n", encoding="utf-8")
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "lifecycle-scope-delta" and not item.passed for item in checks)
        outside.unlink()

        # Missing start/session must block the Human Review gate.
        session_backup = (root / session_rel).read_bytes()
        (root / session_rel).unlink()
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "lifecycle-session-manifest" and not item.passed for item in checks)
        (root / session_rel).write_bytes(session_backup)

        # Authority drift must block even when the candidate itself is untouched.
        authority_text = (root / "AGENTS.md").read_text(encoding="utf-8")
        (root / "AGENTS.md").write_text(authority_text + "drift\n", encoding="utf-8")
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "lifecycle-authority-snapshot" and not item.passed for item in checks)
        (root / "AGENTS.md").write_text(authority_text, encoding="utf-8")

        # A graph chain outside _figures/<slug>/ must block explicitly.
        alt_base = project / "_figures/do_thi_test"
        for src_file, dst_file in (
            (root / graph_src, root / alt_base / "src/do_thi_test.tex"),
            (root / graph_pdf, root / alt_base / "pdf/do_thi_test.pdf"),
            (root / graph_svg, root / alt_base / "svg/do_thi_test.svg"),
        ):
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            dst_file.write_bytes(src_file.read_bytes())
        original_qmd = qmd.read_text(encoding="utf-8")
        qmd.write_text(original_qmd.replace("../_figures/test/svg/do_thi_test.svg", "../_figures/do_thi_test/svg/do_thi_test.svg"), encoding="utf-8")
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "graph-canonical-root" and not item.passed for item in checks)
        qmd.write_text(original_qmd, encoding="utf-8")
        shutil.rmtree(root / alt_base)

        # Missing sidebar must block.
        _write_yaml(root / "_quarto.yml", {"project": {"type": "website", "output-dir": "docs"}, "website": {"sidebar": []}})
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "navigation-sidebar-source" and not item.passed for item in checks)
        _write_yaml(root / "_quarto.yml", {"project": {"type": "website", "output-dir": "docs"}, "website": {"sidebar": [{"href": target.as_posix()}]}})

        # Omission/self-exemption must block.
        broken = _load_yaml(root / profile_rel, "profile")
        broken["tai_nguyen_hinh"]["co_su_dung"] = False
        broken["tai_nguyen_hinh"]["ap_dung_cau_truc_mac_dinh"] = False
        broken["tai_nguyen_hinh"]["li_do_ngoai_le"] = "Tự miễn"
        _write_yaml(root / profile_rel, broken)
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "graph-profile-enabled" and not item.passed for item in checks)
        _write_yaml(root / profile_rel, profile)

        # SVG-only graph must block.
        (root / graph_src).unlink()
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "graph-source-render-chain" and not item.passed for item in checks)
        (root / graph_src).write_text(graph_source_text, encoding="utf-8")

        # A graph that keeps the chain but drops the mandatory visual/font core must block.
        (root / graph_src).write_text(
            r"\begin{axis}[xtick={-1,1},ytick={-1,1},xticklabel=\empty,yticklabel=\empty]\end{axis}" + "\n",
            encoding="utf-8",
        )
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "graph-tex-core-style" and not item.passed for item in checks)
        (root / graph_src).write_text(graph_source_text, encoding="utf-8")

        # Ambiguous preservation wording must block even when a relation record exists.
        safe_qmd_text = qmd.read_text(encoding="utf-8")
        qmd.write_text(
            safe_qmd_text.replace(
                'subtitle: "Đầu ra xác định được từ quan hệ này"',
                'subtitle: "Phép biến đổi giữ độ lớn của đầu vào"',
            ),
            encoding="utf-8",
        )
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "semantic-ambiguous-relation-phrases" and not item.passed for item in checks)
        qmd.write_text(safe_qmd_text, encoding="utf-8")

        # Missing machine-owned render evidence must block.
        render_report = audit / "test_render.json"
        render_backup = render_report.read_bytes()
        render_report.unlink()
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "machine-check-render-evidence" and not item.passed for item in checks)
        render_report.write_bytes(render_backup)

        # Missing canonical self-view evidence must block.
        mobile_evidence = visual / "html_mobile_390.png"
        mobile_backup = mobile_evidence.read_bytes()
        mobile_evidence.unlink()
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "profile-agent-self-view-evidence" and not item.passed for item in checks)
        mobile_evidence.write_bytes(mobile_backup)

        # Missing machine-owned visual measurement report must block even when
        # the agent-owned profile still claims html_mobile=dat.
        visual_report_backup = visual_report.read_bytes()
        visual_report.unlink()
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "machine-visual-viewport-evidence" and not item.passed for item in checks)
        visual_report.write_bytes(visual_report_backup)

        # Missing machine-owned desktop screenshot must block.
        desktop_evidence = visual / "html_desktop_1440.png"
        desktop_backup = desktop_evidence.read_bytes()
        desktop_evidence.unlink()
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "machine-visual-viewport-evidence" and not item.passed for item in checks)
        desktop_evidence.write_bytes(desktop_backup)

        # A viewport mismatch must block; a 390-named screenshot cannot prove a
        # 390px runtime viewport if inner/client width says 500px.
        broken_visual = json.loads(visual_report.read_text(encoding="utf-8"))
        broken_visual["measurements"][0]["window_inner_width"] = 500
        broken_visual["measurements"][0]["document_client_width"] = 500
        visual_report.write_text(json.dumps(broken_visual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "machine-visual-viewport-evidence" and not item.passed for item in checks)
        visual_report.write_bytes(visual_report_backup)

        # Objective horizontal overflow must block regardless of self-view status.
        broken_visual = json.loads(visual_report.read_text(encoding="utf-8"))
        broken_visual["measurements"][0]["document_scroll_width"] = 410
        broken_visual["measurements"][0]["horizontal_overflow"] = True
        broken_visual["measurements"][0]["overflow_px"] = 20
        broken_visual["measurements"][0]["passed"] = False
        broken_visual["automated_result"] = "FAIL"
        broken_visual["exit_code"] = 1
        visual_report.write_text(json.dumps(broken_visual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "machine-visual-viewport-evidence" and not item.passed for item in checks)
        visual_report.write_bytes(visual_report_backup)

        # Missing one PDF page from structured agent self-view must block.
        full_pdf_review = list(profile["tu_xem"]["pdf"]["trang"])
        profile["tu_xem"]["pdf"]["trang"] = full_pdf_review[:1]
        _write_yaml(root / profile_rel, profile)
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert payload["visual_quality"] == "FAIL"
        assert any(item.name == "profile-agent-self-view-evidence" and not item.passed for item in checks)
        profile["tu_xem"]["pdf"]["trang"] = full_pdf_review
        _write_yaml(root / profile_rel, profile)

        # Claiming full HTML self-view without every machine-owned segment must block.
        full_mobile_basis = list(profile["tu_xem"]["html_mobile"]["viewports"][0]["can_cu"])
        profile["tu_xem"]["html_mobile"]["viewports"][0]["can_cu"] = []
        _write_yaml(root / profile_rel, profile)
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "profile-agent-self-view-evidence" and not item.passed for item in checks)
        profile["tu_xem"]["html_mobile"]["viewports"][0]["can_cu"] = full_mobile_basis
        _write_yaml(root / profile_rel, profile)

        # Missing one machine-owned full HTML segment must block.
        segment_path = visual / "html_mobile_390_part_001.png"
        segment_backup = segment_path.read_bytes()
        segment_path.unlink()
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "machine-visual-viewport-evidence" and not item.passed for item in checks)
        segment_path.write_bytes(segment_backup)

        # Missing one machine-owned PDF page record must also block.
        visual_payload = json.loads(visual_report.read_text(encoding="utf-8"))
        full_pdf_pages = list(visual_payload["pdf_pages"])
        visual_payload["pdf_pages"] = full_pdf_pages[:1]
        visual_report.write_text(json.dumps(visual_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "machine-visual-viewport-evidence" and not item.passed for item in checks)
        visual_payload["pdf_pages"] = full_pdf_pages
        visual_report.write_text(json.dumps(visual_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        # A real H2 after Bài tập must block; a fenced fake H2 must not.
        safe_qmd_text = qmd.read_text(encoding="utf-8")
        qmd.write_text(safe_qmd_text + "\n## Bài tập\n\n1. Bài 1.\n\n## Ghi chú thêm\n\nKhông hợp lệ.\n", encoding="utf-8")
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "semantic-exercises-last-h2" and not item.passed for item in checks)
        qmd.write_text(safe_qmd_text + "\n## Bài tập\n\n1. Bài 1.\n\n```markdown\n## H2 giả trong code\n```\n", encoding="utf-8")
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert any(item.name == "semantic-exercises-last-h2" and item.passed for item in checks)
        qmd.write_text(safe_qmd_text, encoding="utf-8")

        # Internal architecture labels must not leak as public headings.
        safe_qmd_text = qmd.read_text(encoding="utf-8")
        qmd.write_text(safe_qmd_text.replace("## Bài tập", "## Kết tinh\n\nTổng hợp thử.\n\n## Bài tập"), encoding="utf-8")
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "semantic-forbidden-public-heading" and not item.passed for item in checks)
        qmd.write_text(safe_qmd_text.replace("## Bài tập", "## Nhìn lại\n\nTổng hợp thử.\n\n## Bài tập"), encoding="utf-8")
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert any(item.name == "semantic-forbidden-public-heading" and item.passed for item in checks)
        qmd.write_text(safe_qmd_text, encoding="utf-8")

        # Long decorative equivalence arrow must block; short Leftrightarrow remains allowed.
        qmd.write_text(safe_qmd_text + "\n$A \\Longleftrightarrow B$.\n", encoding="utf-8")
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "semantic-forbidden-source-tokens" and not item.passed for item in checks)
        qmd.write_text(safe_qmd_text + "\n$A \\Leftrightarrow B$.\n", encoding="utf-8")
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert any(item.name == "semantic-forbidden-source-tokens" and item.passed for item in checks)
        qmd.write_text(safe_qmd_text, encoding="utf-8")

        # \iff renders the same long equivalence arrow and must block.
        qmd.write_text(safe_qmd_text + "\n$A \\iff B$.\n", encoding="utf-8")
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "semantic-forbidden-source-tokens" and not item.passed for item in checks)
        qmd.write_text(safe_qmd_text + "\n$A \\Leftrightarrow B$.\n", encoding="utf-8")
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert any(item.name == "semantic-forbidden-source-tokens" and item.passed for item in checks)
        qmd.write_text(safe_qmd_text, encoding="utf-8")

        # Raw apostrophe derivative notation must block.
        safe_qmd_text = qmd.read_text(encoding="utf-8")
        qmd.write_text(safe_qmd_text + "\n$f'(x)=2x$.\n", encoding="utf-8")
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "latex-prime-notation" and not item.passed for item in checks)
        qmd.write_text(safe_qmd_text, encoding="utf-8")

        # Central relation without recorded proof must block.
        _write_yaml(root / profile_rel, profile)
        broken = _load_yaml(root / profile_rel, "profile")
        broken["kiem_tra_quan_he_trung_tam"] = []
        _write_yaml(root / profile_rel, broken)
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "semantic-central-relation-records" and not item.passed for item in checks)

    print("SELF-TEST PASS: zo_qmd_review")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--repo-root", help="Đường dẫn nằm trong repository; mặc định là thư mục hiện tại.")
    subparsers = result.add_subparsers(dest="command", required=True)
    check = subparsers.add_parser("check", help="Kiểm tra readiness trước Human Review.")
    check.add_argument("path", help="Đường dẫn bài QMD.")
    check.add_argument("--report", help="Báo cáo JSON bên trong _audit/.")
    check.add_argument(
        "--session",
        help="Session manifest do start tạo; mặc định _audit/<slug>_session.json.",
    )
    exercise_hash = subparsers.add_parser(
        "exercise-hash",
        help="Tính fingerprint phần nội dung học thuật trước H2 Bài tập để đồng bộ Exercise Contract.",
    )
    exercise_hash.add_argument("path", help="Đường dẫn bài QMD.")
    metadata_hash = subparsers.add_parser(
        "metadata-hash",
        help="Tính fingerprint nội dung học thuật và metadata mô tả.",
    )
    metadata_hash.add_argument("path", help="Đường dẫn bài QMD.")
    subparsers.add_parser("self-test", help="Chạy self-test nhắm các regression Q1-R2.")
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command == "self-test":
        try:
            _self_test()
            return EXIT_OK
        except Exception as exc:  # self-test is intentionally fail-fast.
            print(f"SELF-TEST FAIL: {exc}")
            return EXIT_FAILED

    try:
        root = _repo_root(args.repo_root)
        if args.command == "exercise-hash":
            return command_exercise_hash(root, args.path)
        if args.command == "metadata-hash":
            return command_metadata_hash(root, args.path)
        return command_check(root, args.path, args.report, args.session)
    except (ProjectConfigError, ReviewReadyError, OSError, RuntimeError) as exc:
        print(f"ERROR: {exc}")
        return EXIT_FAILED


if __name__ == "__main__":
    raise SystemExit(main())

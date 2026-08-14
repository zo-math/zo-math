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


REVIEW_READY_VERSION = 3
SESSION_MANIFEST_VERSION = 3
VISUAL_MEASUREMENT_VERSION = 3
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

    if payload.get("automated_result") != "PASS" or payload.get("exit_code") != 0:
        errors.append("Machine-owned visual report không có automated_result=PASS, exit_code=0.")
    return errors


def _self_view_errors(
    root: Path,
    profile: Mapping[str, Any],
    target: Path,
    required_mobile_viewports: Sequence[int] = (),
    require_pdf_page_coverage: bool = False,
) -> list[str]:
    self_view = _mapping(profile.get("tu_xem"))
    errors: list[str] = []
    status = self_view.get("trang_thai")
    if status not in {"dat", "canh_bao"}:
        errors.append("tu_xem.trang_thai phải là dat hoặc canh_bao trước Human Review.")
    evidence = self_view.get("bang_chung", [])
    if not isinstance(evidence, list) or not evidence:
        return errors + ["tu_xem.bang_chung phải có bằng chứng trực quan thật."]

    canonical_root = Path("_audit") / f"{target.stem}_visual"
    kinds = {"desktop": False, "mobile": False, "pdf": False}
    evidence_paths: set[Path] = set()
    pdf_pages: set[int] = set()
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
        name = relative.name.casefold()
        if "desktop" in name:
            kinds["desktop"] = True
        if "mobile" in name:
            kinds["mobile"] = True
        if "pdf" in name or "page" in name:
            kinds["pdf"] = True
        page_match = re.fullmatch(r"pdf[-_]page[-_](\d+)\.png", name)
        if page_match is not None:
            pdf_pages.add(int(page_match.group(1)))
    missing = [name for name, present in kinds.items() if not present]
    if missing:
        errors.append("Thiếu nhóm bằng chứng self-view: " + ", ".join(missing) + ".")
    for width in required_mobile_viewports:
        expected = canonical_root / f"html_mobile_{int(width)}.png"
        if expected not in evidence_paths:
            errors.append(
                f"tu_xem.bang_chung phải tham chiếu screenshot mobile machine-owned {expected.as_posix()}."
            )
    if require_pdf_page_coverage:
        page_count, page_error = _pdf_page_count(root, target)
        if page_error is not None:
            errors.append(page_error)
        elif page_count is not None:
            expected_pages = set(range(1, page_count + 1))
            missing_pages = sorted(expected_pages - pdf_pages)
            extra_pages = sorted(pdf_pages - expected_pages)
            if missing_pages:
                errors.append(
                    "tu_xem.bang_chung chưa tham chiếu đủ mọi trang PDF; thiếu trang: "
                    + ", ".join(map(str, missing_pages))
                    + "."
                )
            if extra_pages:
                errors.append(
                    "tu_xem.bang_chung có số trang ngoài PDF hiện tại: "
                    + ", ".join(map(str, extra_pages))
                    + "."
                )
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
        machine_visual_errors = _machine_visual_errors(root, target, required_mobile_viewports, required_desktop_viewports)
        add(
            "machine-visual-viewport-evidence",
            not machine_visual_errors,
            "Machine-owned visual evidence xác nhận viewport canonical và không có horizontal overflow."
            if not machine_visual_errors
            else "; ".join(machine_visual_errors),
            Path("_audit") / f"{target.stem}_visual" / "html_mobile_measurements.json",
        )

    if _truthy(profile_policy.get("require_self_view_evidence")):
        self_view_errors = _self_view_errors(
            root,
            profile,
            target,
            required_mobile_viewports=required_mobile_viewports,
            require_pdf_page_coverage=_truthy(profile_policy.get("require_pdf_page_coverage")),
        )
        add(
            "profile-agent-self-view-evidence",
            not self_view_errors,
            "Agent self-view có bằng chứng canonical cho desktop, mobile và toàn bộ các trang PDF."
            if not self_view_errors
            else "; ".join(self_view_errors),
            profile_rel,
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
        "checks": [item.__dict__ for item in checks],
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
                "governing_required": [],
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
                            "pdf": {"download_required": True},
                            "lifecycle": {
                                "require_session_manifest": True,
                                "auto_scope": True,
                                "manual_scope_extensions": False,
                                "require_clean_candidate_scope_at_start": True,
                                "enforce_scope_delta": True,
                                "require_authority_snapshot": True,
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
                                "required_mobile_viewports": [390, 430],
                                "required_desktop_viewports": [1440],
                            },
                            "profile": {
                                "required_version": 5,
                                "required_top_level": [
                                    "tai_lieu_dieu_khien",
                                    "tai_nguyen_hinh",
                                    "kiem_tra_quan_he_trung_tam",
                                    "tu_kiem_noi_dung",
                                    "tu_xem",
                                    "van_de_he_thong",
                                ],
                                "forbidden_top_level": ["nghiem_thu", "ban_giao"],
                                "require_check_and_render_evidence": True,
                                "require_self_view_evidence": True,
                                "require_pdf_page_coverage": True,
                            },
                            "semantic": {
                                "require_relation_records_when_triggered": True,
                                "require_exercises_last_h2": True,
                                "forbidden_source_tokens": ["\\longmapsto", "\\Longleftrightarrow", "\\iff"],
                                "forbidden_ambiguous_phrases": [
                                    "giữ độ lớn",
                                    "giữ nguyên độ lớn",
                                    "bảo toàn độ lớn",
                                    "không xóa độ lớn",
                                ],
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
            "---\ntitle: Test\nsubtitle: \"Đầu ra xác định được từ quan hệ này\"\nzo-pdf-download:\n  href: test.pdf\n---\n\n"
            "Quan hệ này xác định được từ đầu ra.\n\n"
            "![](%s){fig-alt=\"Đồ thị thử\"}\n" % ("../_figures/test/svg/do_thi_test.svg"),
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
        html = root / "docs" / target.with_suffix(".html")
        html.parent.mkdir(parents=True, exist_ok=True)
        html.write_text('<html><nav id="quarto-sidebar"></nav></html>\n', encoding="utf-8")

        audit = root / "_audit"
        audit.mkdir()
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
        (visual / "html-desktop.png").write_bytes(b"visual-evidence\n")
        (visual / "pdf_page_1.png").write_bytes(b"visual-evidence\n")
        (visual / "pdf_page_2.png").write_bytes(b"visual-evidence\n")

        def write_png_stub(path: Path, width: int, height: int) -> None:
            path.write_bytes(
                b"\x89PNG\r\n\x1a\n"
                + (13).to_bytes(4, "big")
                + b"IHDR"
                + width.to_bytes(4, "big")
                + height.to_bytes(4, "big")
                + b"\x08\x06\x00\x00\x00"
            )

        visual_records: list[dict[str, Any]] = []
        for viewport_class, width in (("mobile", 390), ("mobile", 430), ("desktop", 1440)):
            screenshot = visual / f"html_{viewport_class}_{width}.png"
            write_png_stub(screenshot, width, 1000)
            visual_records.append(
                {
                    "viewport_class": viewport_class,
                    "requested_width": width,
                    "requested_height": 1000,
                    "window_inner_width": width,
                    "document_client_width": width,
                    "document_scroll_width": width,
                    "horizontal_overflow": False,
                    "overflow_px": 0,
                    "offender_count": 0,
                    "offenders": [],
                    "screenshot": f"_audit/test_visual/html_{viewport_class}_{width}.png",
                    "screenshot_sha256": _sha256_file(screenshot),
                    "passed": True,
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
            "phien_ban_ho_so": 5,
            "tai_lieu_dieu_khien": {
                "quy_chuan_do_thi": {"kich_hoat": True, "da_doc": True},
                "nguon_li_thuyet_day_du": {"duong_dan": "content/functions/_quy_trinh/theory.qmd", "da_dung": False, "vi_tri_da_dung": []},
            },
            "tai_nguyen_hinh": {"co_su_dung": True, "ap_dung_cau_truc_mac_dinh": True, "li_do_ngoai_le": None},
            "kiem_tra_quan_he_trung_tam": [
                {"phat_bieu": "Đầu ra xác định được đại lượng.", "phep_thu": "Dựng công thức khôi phục.", "ket_luan": "Có công thức khôi phục.", "trang_thai": "dat"}
            ],
            "tu_kiem_noi_dung": {},
            "tu_xem": {
                "trang_thai": "dat",
                "html_desktop": "dat",
                "html_mobile": "dat",
                "pdf": "dat",
                "bang_chung": [
                    "_audit/test_visual/html-desktop.png",
                    "_audit/test_visual/html_mobile_390.png",
                    "_audit/test_visual/html_mobile_430.png",
                    "_audit/test_visual/pdf_page_1.png",
                    "_audit/test_visual/pdf_page_2.png",
                ],
                "canh_bao": [],
            },
            "van_de_he_thong": [],
        }
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

        # Missing one PDF page from agent self-view evidence must block.
        full_evidence = list(profile["tu_xem"]["bang_chung"])
        profile["tu_xem"]["bang_chung"] = [item for item in full_evidence if not item.endswith("pdf_page_2.png")]
        _write_yaml(root / profile_rel, profile)
        checks, payload = evaluate_review_ready(root, target, root / session_rel)
        assert payload["exit_code"] == 1
        assert any(item.name == "profile-agent-self-view-evidence" and not item.passed for item in checks)
        profile["tu_xem"]["bang_chung"] = full_evidence
        _write_yaml(root / profile_rel, profile)

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
        return command_check(root, args.path, args.report, args.session)
    except (ProjectConfigError, ReviewReadyError, OSError, RuntimeError) as exc:
        print(f"ERROR: {exc}")
        return EXIT_FAILED


if __name__ == "__main__":
    raise SystemExit(main())

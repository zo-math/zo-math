"""Unified, scope-aware technical checks for the ZO Math repository."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Any, Mapping, Sequence
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree

from zo_quarto import prepare_quarto

try:
    import yaml
except ImportError:  # Reported as missing dependency with exit code 3 in main().
    yaml = None


EXIT_OK = 0
EXIT_FAILED = 1
EXIT_USAGE = 2
EXIT_MISSING_TOOL = 3

IGNORED_DIRS = {".git", ".quarto", "docs", "_freeze", "__pycache__", ".pytest_cache", ".mypy_cache"}
TEXT_SUFFIXES = {
    ".css", ".html", ".ini", ".js", ".json", ".lua", ".md", ".py",
    ".qmd", ".r", ".rmd", ".scss", ".sh", ".tex", ".toml", ".txt",
    ".xml", ".yaml", ".yml",
}
GRAPHICS = {"path", "line", "polyline", "polygon", "rect", "circle", "ellipse", "text", "use"}
CARD_PROJECT = Path("content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi")
CARD_COMPONENTS = {
    CARD_PROJECT / "_data/cards.yml",
    CARD_PROJECT / "_partials/card_grid.qmd",
    CARD_PROJECT / "index.qmd",
    Path("scripts/zo_build_card_grid.py"),
}
CARD_IMAGE_DIR = CARD_PROJECT / "assets/img/cards"


@dataclass
class Check:
    name: str
    status: str
    message: str
    path: str | None = None


class Checker:
    def __init__(self, root: Path, mode: str, staged: bool) -> None:
        self.root = root
        self.mode = mode
        self.staged = staged
        self.checks: list[Check] = []
        self.warnings: list[str] = []

    def add(self, name: str, passed: bool, message: str, path: Path | None = None) -> None:
        rel = path.relative_to(self.root).as_posix() if path and path.is_absolute() else (path.as_posix() if path else None)
        self.checks.append(Check(name, "pass" if passed else "fail", message, rel))

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    @property
    def failed(self) -> bool:
        return any(item.status == "fail" for item in self.checks)


def run(
    command: Sequence[str], root: Path, env: Mapping[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(command), cwd=root, capture_output=True, text=True, encoding="utf-8",
        errors="replace", check=False, env=env,
    )


def find_repo_root() -> tuple[Path | None, int, str]:
    if shutil.which("git") is None:
        return None, EXIT_MISSING_TOOL, "Không tìm thấy Git trong PATH."
    result = run(["git", "rev-parse", "--show-toplevel"], Path.cwd())
    if result.returncode != 0:
        return None, EXIT_USAGE, result.stderr.strip() or "Không xác định được Git repository."
    return Path(result.stdout.strip()).resolve(), EXIT_OK, ""


def git_names(root: Path, staged: bool) -> list[str]:
    command = ["git", "diff", "--cached" if staged else "HEAD", "--name-only", "-z"]
    result = run(command, root)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    names = [name for name in result.stdout.split("\0") if name]
    if not staged:
        others = run(["git", "ls-files", "--others", "--exclude-standard", "-z"], root)
        if others.returncode != 0:
            raise RuntimeError(others.stderr.strip())
        names.extend(name for name in others.stdout.split("\0") if name)
    return sorted(set(names))


def is_ignored(root: Path, path: Path) -> bool:
    result = run(["git", "check-ignore", "-q", "--", path.relative_to(root).as_posix()], root)
    return result.returncode == 0


def tracked_deleted(root: Path, relative: Path) -> bool:
    result = run(["git", "ls-files", "--error-unmatch", "--", relative.as_posix()], root)
    return result.returncode == 0 and not (root / relative).exists()


def inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def expand_paths(root: Path, raw_paths: Sequence[str], allow_ignored_file: bool = True) -> tuple[list[Path], str | None]:
    files: list[Path] = []
    for raw in raw_paths:
        candidate = Path(raw)
        absolute = (candidate if candidate.is_absolute() else root / candidate).resolve()
        if not inside(absolute, root):
            return [], f"Đường dẫn nằm ngoài repository: {raw}"
        relative = absolute.relative_to(root)
        if not absolute.exists():
            if tracked_deleted(root, relative):
                files.append(relative)
                continue
            return [], f"Đường dẫn không tồn tại và không phải tệp tracked đang bị xóa: {raw}"
        if absolute.is_symlink() and not inside(absolute.resolve(), root):
            return [], f"Symlink đi ra ngoài repository: {raw}"
        if absolute.is_file():
            if allow_ignored_file or not is_ignored(root, absolute):
                files.append(relative)
            continue
        for current, dirs, names in os.walk(absolute, followlinks=False):
            current_path = Path(current)
            dirs[:] = [
                name for name in dirs
                if name not in IGNORED_DIRS
                and not (current_path / name).is_symlink()
                and not is_ignored(root, current_path / name)
            ]
            for name in names:
                path = current_path / name
                if not is_ignored(root, path):
                    files.append(path.relative_to(root))
    return sorted(set(files), key=lambda item: item.as_posix()), None


def read_utf8(path: Path, checker: Checker) -> str | None:
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError) as exc:
        checker.add("utf8", False, str(exc), path)
        return None
    checker.add("utf8", True, "Đọc UTF-8 thành công.", path)
    return text


def is_text(path: Path) -> bool:
    if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"AGENTS.md", ".gitignore", ".gitattributes"}:
        return True
    try:
        return b"\0" not in path.read_bytes()[:8192]
    except OSError:
        return False


def changed_line_numbers(relative: Path, checker: Checker, total_lines: int) -> set[int]:
    tracked = run(["git", "ls-files", "--error-unmatch", "--", relative.as_posix()], checker.root)
    if tracked.returncode != 0:
        return set(range(1, total_lines + 1))
    command = ["git", "diff", "--unified=0"]
    command.append("--cached" if checker.staged else "HEAD")
    command.extend(["--", relative.as_posix()])
    result = run(command, checker.root)
    changed: set[int] = set()
    for start, count in re.findall(r"(?m)^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", result.stdout):
        length = int(count or "1")
        changed.update(range(int(start), int(start) + length))
    return changed


def check_whitespace_and_eol(path: Path, checker: Checker) -> None:
    if not is_text(path):
        return
    data = path.read_bytes()
    crlf = data.count(b"\r\n")
    bare_lf = data.count(b"\n") - crlf
    bare_cr = data.count(b"\r") - crlf
    mixed = sum(value > 0 for value in (crlf, bare_lf, bare_cr)) > 1
    checker.add("mixed-eol", not mixed, "Không có EOL trộn." if not mixed else "Phát hiện nhiều kiểu EOL.", path)
    relative = path.relative_to(checker.root)
    lines = data.splitlines()
    changed = changed_line_numbers(relative, checker, len(lines))
    bad: list[int] = []
    historical: list[int] = []
    for number, line in enumerate(data.splitlines(), 1):
        if line.endswith((b" ", b"\t")):
            markdown_break = path.suffix.lower() in {".md", ".qmd"} and line.endswith(b"  ") and not line.endswith(b"   ")
            if number in changed and not markdown_break:
                bad.append(number)
            elif number not in changed:
                historical.append(number)
    if bad:
        message = f"Trailing whitespace mới tại dòng: {', '.join(map(str, bad[:20]))}"
    elif historical:
        message = f"Không có lỗi mới; whitespace lịch sử không chặn tại dòng: {', '.join(map(str, historical[:20]))}"
    else:
        message = "Không có trailing whitespace mới."
    checker.add("trailing-whitespace", not bad, message, path)


def check_git_eol(paths: Sequence[Path], checker: Checker) -> None:
    if not paths:
        checker.add("git-eol", True, "Không có tệp tracked trong phạm vi.")
        return
    result = run(["git", "ls-files", "--eol", "--", *[path.as_posix() for path in paths]], checker.root)
    if result.returncode != 0:
        checker.add("git-eol", False, result.stderr.strip() or "git ls-files --eol thất bại.")
        return
    mixed = [line for line in result.stdout.splitlines() if "w/mixed" in line or "i/mixed" in line]
    checker.add("git-eol", not mixed, "Git không báo EOL trộn." if not mixed else "; ".join(mixed))


def check_diff(paths: Sequence[Path], checker: Checker) -> None:
    command = ["git", "diff"]
    if checker.staged:
        command.append("--cached")
    command.append("--check")
    if paths:
        command.extend(["--", *[path.as_posix() for path in paths]])
    result = run(command, checker.root)
    checker.add("git-diff-check", result.returncode == 0, result.stdout.strip() or result.stderr.strip() or "Đạt.")


def validate_python(path: Path, text: str, checker: Checker) -> None:
    try:
        compile(text, str(path), "exec")
    except SyntaxError as exc:
        checker.add("python-syntax", False, f"Dòng {exc.lineno}, cột {exc.offset}: {exc.msg}", path)
    else:
        checker.add("python-syntax", True, "Cú pháp Python hợp lệ.", path)


def validate_yaml(path: Path, text: str, checker: Checker) -> Any:
    try:
        value = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        where = f"dòng {mark.line + 1}, cột {mark.column + 1}: " if mark else ""
        checker.add("yaml", False, where + str(exc).splitlines()[0], path)
        return None
    checker.add("yaml", True, "YAML hợp lệ.", path)
    return value


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def reference_target(raw: str, source: Path, root: Path) -> Path | None:
    value = unescape(raw.strip())
    if not value or value.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
        return None
    if "{{" in value or "{%" in value or "$" in value:
        return None
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        return None
    clean = unquote(parsed.path).replace("\\", "/")
    if not clean:
        return None
    return (root / clean.lstrip("/") if clean.startswith("/") else source.parent / clean).resolve()


def normalize_image_extension(value: Any, label: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not re.fullmatch(r"\.?[A-Za-z0-9]+", value.strip()):
        raise ValueError(f"{label} phải là phần mở rộng hợp lệ, ví dụ svg hoặc .png.")
    return "." + value.strip().lstrip(".").lower()


def nested_default_image_extension(metadata: Any) -> Any:
    if not isinstance(metadata, dict):
        return None
    if "default-image-extension" in metadata:
        return metadata["default-image-extension"]
    html = metadata.get("format")
    if isinstance(html, dict):
        html = html.get("html")
        if isinstance(html, dict) and "default-image-extension" in html:
            return html["default-image-extension"]
    return None


def project_default_image_extension(root: Path) -> str | None:
    path = root / "_quarto.yml"
    try:
        config = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        raise ValueError(f"Không đọc được _quarto.yml: {exc}") from exc
    return normalize_image_extension(
        nested_default_image_extension(config), "format.html.default-image-extension trong _quarto.yml"
    )


def validate_local_refs(
    refs: Sequence[str], source: Path, checker: Checker, label: str,
    default_image_extension: str | None = None,
) -> None:
    missing: list[str] = []
    for raw in refs:
        target = reference_target(raw, source, checker.root)
        if target is None:
            continue
        tried = [target]
        if (default_image_extension and not target.suffix and not target.exists()
                and inside(target, checker.root)):
            tried.append(target.with_name(target.name + default_image_extension))
        valid = next((candidate for candidate in tried
                      if inside(candidate, checker.root) and candidate.exists()
                      and not (candidate.is_symlink() and not inside(candidate.resolve(), checker.root))), None)
        if valid is None:
            shown = []
            for candidate in tried:
                try:
                    shown.append(candidate.relative_to(checker.root).as_posix())
                except ValueError:
                    shown.append(f"ngoài-repository:{candidate.name}")
            missing.append(f"{raw} (đã thử: {', '.join(shown)})")
    checker.add(label, not missing, "Các tài nguyên cục bộ tồn tại." if not missing else "Thiếu: " + ", ".join(sorted(set(missing))), source)


def validate_svg(path: Path, text: str, checker: Checker) -> None:
    problems = svg_problems(text)
    checker.add("svg-xml", not problems or not problems[0].startswith("XML:"), problems[0] if problems and problems[0].startswith("XML:") else "XML hợp lệ.", path)
    if problems and problems[0].startswith("XML:"):
        return
    checker.add("svg-structure", not problems, "Cấu trúc và nội dung đồ họa hợp lệ." if not problems else "; ".join(problems), path)
    try:
        root_element = ElementTree.fromstring(text)
    except ElementTree.ParseError:
        return
    refs = []
    for element in root_element.iter():
        for key, value in element.attrib.items():
            if local_name(key) == "href":
                refs.append(value)
    validate_local_refs(refs, path, checker, "svg-resources")


def svg_problems(text: str) -> list[str]:
    try:
        root_element = ElementTree.fromstring(text)
    except ElementTree.ParseError as exc:
        return [f"XML: {exc}"]
    problems = []
    if local_name(root_element.tag) != "svg":
        problems.append("phần tử gốc không phải svg")
    if not (root_element.get("viewBox") or (root_element.get("width") and root_element.get("height"))):
        problems.append("thiếu kích thước và viewBox")
    if not any(local_name(element.tag) in GRAPHICS for element in root_element.iter()):
        problems.append("không có phần tử đồ họa thực tế")
    return problems


def strip_code(text: str) -> str:
    text = re.sub(r"(?ms)^\s*(```|~~~).*?^\s*\1\s*$", "", text)
    return re.sub(r"`[^`\n]*`", "", text)


def validate_markdown(path: Path, text: str, checker: Checker) -> None:
    body = strip_code(text)
    image_refs = re.findall(r"!\[[^\]\n]*\]\(([^\s)]+)(?:\s+[^)]*)?\)", body)
    refs = re.findall(r"(?<!!)\[[^\]\n]*\]\(([^\s)]+)(?:\s+[^)]*)?\)", body)
    image_refs.extend(re.findall(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", body, flags=re.IGNORECASE))
    refs.extend(re.findall(r"\bhref=[\"']([^\"']+)[\"']", body, flags=re.IGNORECASE))
    refs.extend(re.findall(r"<(?!img\b)[^>]*\bsrc=[\"']([^\"']+)[\"']", body, flags=re.IGNORECASE))
    metadata: Any = {}
    if body.startswith("---"):
        parts = body.split("---", 2)
        if len(parts) == 3:
            try:
                metadata = yaml.safe_load(parts[1]) or {}
                for key in ("bibliography", "csl", "include-in-header", "include-before-body", "include-after-body"):
                    value = metadata.get(key) if isinstance(metadata, dict) else None
                    refs.extend(value if isinstance(value, list) else [value] if isinstance(value, str) else [])
            except yaml.YAMLError as exc:
                checker.add("markdown-metadata", False, f"YAML metadata không hợp lệ: {exc}", path)
                return
    try:
        page_value = nested_default_image_extension(metadata)
        extension = (normalize_image_extension(page_value, "default-image-extension trong metadata")
                     if page_value is not None else project_default_image_extension(checker.root))
    except ValueError as exc:
        checker.add("markdown-resources-config", False, str(exc), path)
        return
    validate_local_refs(refs, path, checker, "markdown-resources")
    validate_local_refs(image_refs, path, checker, "markdown-image-resources", extension)


def validate_file(relative: Path, checker: Checker) -> None:
    path = checker.root / relative
    if not path.exists():
        checker.add("deleted", True, "Tệp tracked đang bị xóa; bỏ qua kiểm tra nội dung.", relative)
        return
    check_whitespace_and_eol(path, checker)
    if not is_text(path):
        checker.add("binary", True, "Tệp nhị phân; không phân tích nội dung.", path)
        return
    text = read_utf8(path, checker)
    if text is None:
        return
    suffix = path.suffix.lower()
    if suffix == ".py":
        validate_python(path, text, checker)
    elif suffix in {".yaml", ".yml"}:
        validate_yaml(path, text, checker)
    elif suffix == ".svg":
        validate_svg(path, text, checker)
    elif suffix in {".md", ".qmd"}:
        validate_markdown(path, text, checker)


def card_scope(paths: Sequence[Path]) -> bool:
    for path in paths:
        if path in CARD_COMPONENTS or path == CARD_IMAGE_DIR or CARD_IMAGE_DIR in path.parents:
            return True
    return False


def check_card_grid(checker: Checker) -> None:
    data_path = checker.root / CARD_PROJECT / "_data/cards.yml"
    partial_path = checker.root / CARD_PROJECT / "_partials/card_grid.qmd"
    try:
        data = yaml.safe_load(data_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        checker.add("card-grid-data", False, str(exc), data_path)
        return
    valid = isinstance(data, dict) and isinstance(data.get("special"), list) and isinstance(data.get("groups"), list)
    checker.add("card-grid-structure", valid, "Cấu trúc special/groups hợp lệ." if valid else "Cần dict với special và groups là list.", data_path)
    if not valid:
        return
    items: list[dict[str, Any]] = []
    items.extend(item for item in data["special"] if isinstance(item, dict))
    for group in data["groups"]:
        if not isinstance(group, dict) or not isinstance(group.get("items", []), list):
            checker.add("card-grid-groups", False, "Group hoặc items không đúng cấu trúc.", data_path)
            return
        items.extend(item for item in group.get("items", []) if isinstance(item, dict))
    ids = [str(item["id"]) for item in items if item.get("id") is not None]
    numbers = [int(item["number"]) for item in items if item.get("number") is not None]
    duplicate_ids = sorted(key for key, count in Counter(ids).items() if count > 1)
    duplicate_numbers = sorted(key for key, count in Counter(numbers).items() if count > 1)
    checker.add("card-grid-identifiers", not duplicate_ids and not duplicate_numbers, f"ID trùng: {duplicate_ids}; number trùng: {duplicate_numbers}" if duplicate_ids or duplicate_numbers else "Không có định danh trùng.", data_path)
    bad_status = sorted({str(item.get("status")) for item in items if item.get("status") not in {"published", "pending"}})
    checker.add("card-grid-status", not bad_status, "Trạng thái hợp lệ." if not bad_status else "Trạng thái không hỗ trợ: " + ", ".join(bad_status), data_path)
    visible = [item for item in items if item.get("visible", True) is not False]
    missing: list[str] = []
    images: list[str] = []
    links: list[str] = []
    for item in visible:
        image = item.get("image")
        if isinstance(image, str) and image:
            images.append(image)
            if not (checker.root / CARD_PROJECT / image).exists():
                missing.append(image)
        href = item.get("href")
        if item.get("status") == "published" and not href:
            missing.append(f"href:{item.get('id', item.get('number', '?'))}")
        if isinstance(href, str) and href:
            links.append(href)
            target = reference_target(href, checker.root / CARD_PROJECT / "index.qmd", checker.root)
            if target is not None and not target.exists():
                missing.append(href)
    checker.add("card-grid-resources", not missing, "Ảnh và liên kết bắt buộc tồn tại." if not missing else "Thiếu: " + ", ".join(sorted(set(missing))), data_path)
    try:
        partial = partial_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        checker.add("card-grid-partial", False, str(exc), partial_path)
        return
    count = len(re.findall(r"(?m)^:::\s+\{\.zo-card(?:\s|\})", partial))
    checker.add("card-grid-count", count == len(visible), f"Partial={count}, dữ liệu hiển thị={len(visible)}.", partial_path)
    absent = [value for value in images if f'src="{value}"' not in partial]
    absent.extend(value for value in links if f'href="{value}"' not in partial)
    checker.add("card-grid-partial-refs", not absent, "Tham chiếu quan trọng khớp dữ liệu." if not absent else "Partial thiếu: " + ", ".join(sorted(set(absent))), partial_path)
    svg_paths = set()
    svg_paths.update(checker.root / CARD_PROJECT / value for value in images if value.lower().endswith(".svg"))
    svg_paths.update(checker.root / CARD_PROJECT / value for value in re.findall(r'src="([^"]+\.svg)"', partial))
    svg_errors: list[str] = []
    for svg_path in sorted(svg_paths):
        if not svg_path.exists():
            svg_errors.append(f"{svg_path.relative_to(checker.root).as_posix()}: không tồn tại")
            continue
        try:
            problems = svg_problems(svg_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError) as exc:
            problems = [str(exc)]
        if problems:
            svg_errors.append(f"{svg_path.relative_to(checker.root).as_posix()}: {'; '.join(problems)}")
    checker.add("card-grid-svg", not svg_errors, f"{len(svg_paths)} SVG được tham chiếu đều hợp lệ." if not svg_errors else " | ".join(svg_errors), CARD_IMAGE_DIR)


def run_scope(paths: Sequence[Path], checker: Checker, include_git: bool = True) -> None:
    if include_git:
        check_diff(paths, checker)
        tracked = [path for path in paths if run(["git", "ls-files", "--error-unmatch", "--", path.as_posix()], checker.root).returncode == 0]
        check_git_eol(tracked, checker)
    for path in paths:
        validate_file(path, checker)
    if card_scope(paths):
        check_card_grid(checker)


def output_dir(root: Path) -> Path:
    config = yaml.safe_load((root / "_quarto.yml").read_text(encoding="utf-8")) or {}
    value = (config.get("project") or {}).get("output-dir", "_site")
    return root / str(value)


def render_pages(paths: Sequence[Path], checker: Checker) -> int | None:
    try:
        base_command, quarto_env = prepare_quarto([])
    except FileNotFoundError:
        return EXIT_MISSING_TOOL
    out_dir = output_dir(checker.root)
    for relative in paths:
        page = checker.root / relative
        if page.suffix.lower() != ".qmd" or not page.is_file():
            checker.add("render-input", False, "Render chỉ nhận tệp .qmd tồn tại.", relative)
            continue
        failures_before = sum(item.status == "fail" for item in checker.checks)
        run_scope([relative], checker)
        failures_after = sum(item.status == "fail" for item in checker.checks)
        if failures_after > failures_before:
            checker.add("render", False, "Bỏ qua render vì scope của trang thất bại.", relative)
            continue
        result = run([*base_command, "render", relative.as_posix()], checker.root, quarto_env)
        combined = "\n".join(part for part in (result.stdout, result.stderr) if part).strip()
        warnings = [line.strip() for line in combined.splitlines() if re.search(r"\bwarn(?:ing)?\b|cảnh báo", line, re.IGNORECASE)]
        errors = [line.strip() for line in combined.splitlines() if re.search(r"\berror\b|lỗi", line, re.IGNORECASE)]
        information = [line.strip() for line in combined.splitlines() if line.strip() and line.strip() not in warnings and line.strip() not in errors]
        checker.warnings.extend(warnings)
        detail = f"; chi tiết lỗi: {' | '.join(errors[:3])}" if errors else ""
        checker.add("quarto-render", result.returncode == 0, f"Mã thoát {result.returncode}; lỗi={len(errors)}, cảnh báo={len(warnings)}, thông tin={len(information)}{detail}.", relative)
        html = out_dir / relative.with_suffix(".html")
        checker.add("render-html", html.exists(), f"HTML: {html.relative_to(checker.root).as_posix()}", relative)
    return None


def print_results(checker: Checker, scope: Sequence[Path]) -> None:
    print(f"MODE: {checker.mode} | {'STAGED' if checker.staged else 'WORKTREE'}")
    print(f"ROOT: {checker.root}")
    print(f"SCOPE ({len(scope)}):")
    for path in scope:
        print(f"  - {path.as_posix()}")
    print("CHECKS:")
    for item in checker.checks:
        location = f" [{item.path}]" if item.path else ""
        print(f"  {'PASS' if item.status == 'pass' else 'FAIL'} {item.name}{location}: {item.message}")
    for warning in checker.warnings:
        print(f"  WARN render-log: {warning}")


def report_path(root: Path, raw: str) -> Path | None:
    target = (Path(raw) if Path(raw).is_absolute() else root / raw).resolve()
    audit = (root / "_audit").resolve()
    return target if inside(target, audit) and target.suffix.lower() == ".json" else None


def write_report(path: Path, checker: Checker, scope: Sequence[Path], exit_code: int) -> None:
    payload = {
        "mode": checker.mode,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(checker.root),
        "scope": [item.as_posix() for item in scope],
        "staged": checker.staged,
        "checks": [asdict(item) for item in checker.checks],
        "warnings": checker.warnings,
        "exit_code": exit_code,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--staged", action="store_true", help="Kiểm tra vùng staged.")
    common.add_argument("--report", help="Ghi báo cáo JSON bên trong _audit/.")
    result = argparse.ArgumentParser(description=__doc__)
    subparsers = result.add_subparsers(dest="mode", required=True)
    quick = subparsers.add_parser("quick", parents=[common], help="Kiểm tra nhanh, không render.")
    quick.add_argument("paths", nargs="*")
    scope = subparsers.add_parser("scope", parents=[common], help="Kiểm tra phạm vi tường minh.")
    scope.add_argument("paths", nargs="+")
    render = subparsers.add_parser("render", parents=[common], help="Kiểm tra rồi render trang tường minh.")
    render.add_argument("paths", nargs="+")
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    root, root_exit, message = find_repo_root()
    if root is None:
        print(f"ERROR: {message}", file=sys.stderr)
        return root_exit
    os.chdir(root)
    if yaml is None:
        print("ERROR: Thiếu dependency PyYAML.", file=sys.stderr)
        return EXIT_MISSING_TOOL
    if args.report and report_path(root, args.report) is None:
        print("ERROR: --report phải là tệp .json bên trong _audit/.", file=sys.stderr)
        return EXIT_USAGE
    checker = Checker(root, args.mode, args.staged)
    try:
        raw_paths = args.paths
        if args.mode == "quick" and not raw_paths:
            raw_paths = git_names(root, args.staged)
        paths, error = expand_paths(root, raw_paths)
        if error:
            print(f"ERROR: {error}", file=sys.stderr)
            return EXIT_USAGE
        status = run(["git", "status", "--short"], root)
        checker.add("git-status", status.returncode == 0, status.stdout.strip() or "Repository không có thay đổi.")
        if args.mode in {"quick", "scope"}:
            run_scope(paths, checker)
        else:
            missing = render_pages(paths, checker)
            if missing is not None:
                print("ERROR: Không tìm thấy Quarto trong PATH.", file=sys.stderr)
                return missing
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_FAILED
    exit_code = EXIT_FAILED if checker.failed else EXIT_OK
    if args.report:
        target = report_path(root, args.report)
        try:
            write_report(target, checker, paths, exit_code)
            checker.add("report", True, f"Đã ghi {target.relative_to(root).as_posix()}.")
        except OSError as exc:
            checker.add("report", False, str(exc))
            exit_code = EXIT_FAILED
    print_results(checker, paths)
    print(f"RESULT: {'PASS' if exit_code == 0 else 'FAIL'} | EXIT={exit_code}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())

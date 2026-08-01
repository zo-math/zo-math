"""Unified, scope-aware technical checks for the ZO Math repository.

Includes the technical output contract for function-article QMD files.
"""

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
from typing import Any, Callable, Mapping, Sequence
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree

from zo_qmd_config import ProjectConfig, ProjectConfigError, discover_project_config
from zo_qmd_registry import (
    ModuleRegistryError,
    ValidationPlan,
    build_validation_plan,
)
from zo_qmd_core import (
    split_qmd_front_matter,
    strip_fences_comments_and_inline_code,
    validate_executable_code,
    validate_forbidden_paths,
    validate_headings,
    validate_images,
    validate_placeholders,
    validate_qmd_front_matter,
    validate_required_body_classes,
    validate_required_metadata,
)
from zo_real_world_problem import (
    validate_real_world_problem_article,
    validate_rendered_real_world_problem_page,
)
from zo_quarto import prepare_quarto

try:
    import yaml
except ImportError:  # Reported as missing dependency with exit code 3 in main().
    yaml = None


CHECKER_VERSION = "2.6.0"

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

FUNCTION_LEGACY_CLASSES = (
    ".tieu-de-chu-thich", "collapsible-box-", "highlight-box-",
)
FUNCTION_BLOCK_COLORS = ("zo-block-red", "zo-block-yellow", "zo-block-gray")
FUNCTION_CANONICAL_BASE = "https://zo-math.github.io/zo-math/"
FUNCTION_EXPANDED_FIGURE_CLASS = "column-screen-inset-shaded"


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

    def _path_text(self, path: Path | None) -> str | None:
        if path is None:
            return None
        return path.relative_to(self.root).as_posix() if path.is_absolute() else path.as_posix()

    def add(self, name: str, passed: bool, message: str, path: Path | None = None) -> None:
        self.checks.append(Check(name, "pass" if passed else "fail", message, self._path_text(path)))

    def add_warning(self, name: str, message: str, path: Path | None = None) -> None:
        self.checks.append(Check(name, "warn", message, self._path_text(path)))

    def add_info(self, name: str, message: str, path: Path | None = None) -> None:
        self.checks.append(Check(name, "info", message, self._path_text(path)))

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    @property
    def failed(self) -> bool:
        return any(item.status == "fail" for item in self.checks)

    @property
    def has_warnings(self) -> bool:
        return bool(self.warnings) or any(item.status == "warn" for item in self.checks)


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


def load_yaml_unique(text: str) -> Any:
    class UniqueKeyLoader(yaml.SafeLoader):
        pass

    def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
        mapping: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in mapping:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    f"found duplicate key {key!r}",
                    key_node.start_mark,
                )
            mapping[key] = loader.construct_object(value_node, deep=deep)
        return mapping

    UniqueKeyLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping,
    )
    return yaml.load(text, Loader=UniqueKeyLoader)


def validate_yaml(path: Path, text: str, checker: Checker) -> Any:
    try:
        value = load_yaml_unique(text)
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
        config = load_yaml_unique(path.read_text(encoding="utf-8")) or {}
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



def line_list(text: str, pattern: str, flags: int = 0) -> list[int]:
    expression = re.compile(pattern, flags)
    return [
        number for number, line in enumerate(text.splitlines(), start=1)
        if expression.search(line)
    ]


@dataclass(frozen=True)
class ArticleValidationContext:
    config: ProjectConfig
    article_type: str
    plan: ValidationPlan


def article_validation_context(
    relative: Path,
    root: Path,
    checker: Checker | None = None,
    *,
    report: bool = True,
) -> ArticleValidationContext | None:
    # Resolve project, article type, modules, and symbolic validator adapters.
    if relative.suffix.lower() != ".qmd":
        return None
    try:
        config = discover_project_config(root, relative)
    except ProjectConfigError as exc:
        if checker is not None and report:
            checker.add("qmd-project-discovery", False, str(exc), relative)
        return None

    if config is not None:
        try:
            article_type = config.article_type_for(relative)
        except ProjectConfigError as exc:
            if checker is not None and report:
                checker.add("qmd-project-discovery", False, str(exc), relative)
            return None
        if article_type is None:
            if checker is not None and report:
                checker.add_info(
                    "qmd-project-discovery",
                    f"Thu\u1ed9c project={config.project_id!r} "
                    "nh\u01b0ng kh\u00f4ng kh\u1edbp lo\u1ea1i "
                    "b\u00e0i \u0111\u00e3 \u0111\u0103ng k\u00ed.",
                    relative,
                )
            return None
        try:
            plan = build_validation_plan(config, article_type.id)
        except ModuleRegistryError as exc:
            if checker is not None and report:
                checker.add("qmd-validator-plan", False, str(exc), relative)
            return None
        context = ArticleValidationContext(
            config=config,
            article_type=article_type.id,
            plan=plan,
        )
        if checker is not None and report:
            checker.add(
                "qmd-project-discovery",
                True,
                (
                    f"project={config.project_id!r}; "
                    f"article_type={article_type.id!r}; "
                    f"config={config.config_path.as_posix()}."
                ),
                relative,
            )
            checker.add(
                "qmd-validator-plan",
                True,
                (
                    f"mode={plan.compatibility_mode!r}; "
                    f"modules={list(plan.active_modules)!r}; "
                    f"source={list(plan.source_adapters)!r}; "
                    f"render={list(plan.render_adapters)!r}."
                ),
                relative,
            )
        return context

    return None


def function_project_config(
    relative: Path,
    checker: Checker,
    config: ProjectConfig | None = None,
) -> ProjectConfig | None:
    if config is None:
        try:
            config = discover_project_config(checker.root, relative)
        except ProjectConfigError as exc:
            checker.add("function-project-config", False, str(exc), relative)
            return None
    if config is None:
        checker.add(
            "function-project-config",
            False,
            "Bài hàm số chưa có cấu hình dự án điều khiển.",
            relative,
        )
        return None
    article_type = config.article_type_for(relative)
    if article_type is None or article_type.id != "function_article":
        checker.add(
            "function-project-config",
            False,
            "Cấu hình dự án không đăng kí bài này là function_article.",
            relative,
        )
        return None
    checker.add(
        "function-project-config",
        True,
        (
            f"Đã nạp metadata, body classes, placeholders và hồ sơ từ "
            f"{config.config_path.as_posix()}."
        ),
        relative,
    )
    return config


def flatten_card_items(data: Any) -> list[dict[str, Any]]:
    if not isinstance(data, dict):
        return []
    items: list[dict[str, Any]] = []
    special = data.get("special")
    if isinstance(special, list):
        items.extend(item for item in special if isinstance(item, dict))
    groups = data.get("groups")
    if isinstance(groups, list):
        for group in groups:
            if isinstance(group, dict) and isinstance(group.get("items"), list):
                items.extend(item for item in group["items"] if isinstance(item, dict))
    return items


def normalize_href_path(value: str) -> str:
    parsed = urlsplit(value)
    return unquote(parsed.path).replace("\\", "/").lstrip("/")


def function_card(
    relative: Path, metadata: Mapping[str, Any], checker: Checker
) -> tuple[dict[str, Any] | None, str | None]:
    data_path = checker.root / CARD_PROJECT / "_data/cards.yml"
    try:
        data = load_yaml_unique(data_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        return None, f"Không đọc được cards.yml: {exc}"
    items = flatten_card_items(data)
    expected = relative.relative_to(CARD_PROJECT).with_suffix(".html").as_posix()
    by_href = [
        item for item in items
        if isinstance(item.get("href"), str)
        and normalize_href_path(item["href"]).endswith(expected)
    ]
    if len(by_href) == 1:
        return by_href[0], None
    listing = metadata.get("listing-order")
    by_number = [
        item for item in items
        if isinstance(listing, int) and item.get("number") == listing
    ]
    if len(by_number) == 1:
        return by_number[0], None
    if len(by_href) > 1 or len(by_number) > 1:
        return None, "Có nhiều thẻ cùng khớp bài hoặc listing-order."
    return None, "Không tìm thấy thẻ tương ứng bằng href hoặc listing-order."


def validate_function_metadata(
    path: Path,
    relative: Path,
    metadata: dict[str, Any],
    checker: Checker,
    config: ProjectConfig,
) -> tuple[dict[str, Any] | None, str | None]:
    required_metadata = (
        *config.core_required_metadata,
        *config.project_required_metadata,
    )
    validate_required_metadata(
        path,
        metadata,
        checker,
        prefix="function",
        required=required_metadata,
    )
    expected_values = {
        "author": "ZO Math",
        "date": "last-modified",
        "date-format": "DD-MM-YYYY",
        "page-layout": "article",
        "toc": True,
        "toc-title": "Nội dung",
        "toc-location": "right",
        "toc-depth": 3,
    }
    wrong = [
        f"{key}={metadata.get(key)!r}"
        for key, expected in expected_values.items()
        if metadata.get(key) != expected
    ]
    checker.add(
        "function-yaml-fixed-values", not wrong,
        "Các giá trị cố định đúng chuẩn." if not wrong else "Sai: " + ", ".join(wrong),
        path,
    )

    def contains_tex_markup(value: Any) -> bool:
        if not isinstance(value, str):
            return False
        return bool(re.search(r"\$|\\[A-Za-z]+|\\\(|\\\[", value))

    plain_title_fields = {
        "title-meta": metadata.get("title-meta"),
        "pagetitle": metadata.get("pagetitle"),
    }
    tex_in_plain = [
        f"{key}={value!r}"
        for key, value in plain_title_fields.items()
        if contains_tex_markup(value)
    ]
    checker.add(
        "function-title-plain-metadata", not tex_in_plain,
        "title-meta và pagetitle dùng văn bản thuần."
        if not tex_in_plain
        else "Không được chứa TeX: " + ", ".join(tex_in_plain),
        path,
    )
    validate_required_body_classes(
        path,
        metadata,
        checker,
        prefix="function",
        required=config.required_body_classes,
    )
    listing = metadata.get("listing-order")
    checker.add(
        "function-listing-order-type", isinstance(listing, int) and listing > 0,
        f"listing-order={listing!r}." if isinstance(listing, int) and listing > 0
        else "listing-order phải là số nguyên dương.",
        path,
    )
    image = metadata.get("image")
    image_ok = isinstance(image, str) and image.startswith("/") and (checker.root / image.lstrip("/")).exists()
    checker.add(
        "function-card-image", image_ok,
        f"Ảnh thẻ tồn tại: {image}" if image_ok else f"Ảnh thẻ không hợp lệ hoặc không tồn tại: {image!r}",
        path,
    )

    card, card_error = function_card(relative, metadata, checker)
    if card is None:
        checker.add_warning("function-card-match", card_error or "Không xác định được thẻ.", path)
        status = None
    else:
        checker.add("function-card-match", True, f"Khớp thẻ {card.get('id', card.get('number'))}.", path)
        card_status = card.get("status")
        checker.add(
            "function-card-status", card_status in {"published", "pending"},
            f"status={card_status!r}." if card_status in {"published", "pending"}
            else f"Trạng thái thẻ không hỗ trợ: {card_status!r}.",
            path,
        )
        expected_href = relative.relative_to(CARD_PROJECT).as_posix()
        card_href = card.get("href")
        if card_status == "pending" and card_href in {None, ""}:
            checker.add_info(
                "function-card-href",
                "Thẻ pending chưa cần href; sẽ kiểm tra khi chuyển sang published.",
                path,
            )
        else:
            href_matches = (
                isinstance(card_href, str)
                and normalize_href_path(card_href).endswith(expected_href)
            )
            checker.add(
                "function-card-href", href_matches,
                "href của thẻ khớp bài." if href_matches
                else f"Kì vọng href kết thúc bằng {expected_href!r}, nhận {card_href!r}.",
                path,
            )
        number_ok = card.get("number") == listing
        checker.add(
            "function-listing-order-card", number_ok,
            f"listing-order={listing!r}, card.number={card.get('number')!r}.",
            path,
        )
        card_image = card.get("image")
        normalized_metadata_image = str(image).lstrip("/") if isinstance(image, str) else ""
        normalized_card_image = (
            (CARD_PROJECT / str(card_image)).as_posix()
            if isinstance(card_image, str) and not str(card_image).startswith("/")
            else str(card_image).lstrip("/")
        )
        image_matches = normalized_metadata_image == normalized_card_image
        checker.add(
            "function-image-card", image_matches,
            "image khớp thẻ." if image_matches
            else f"YAML={image!r}, thẻ={card_image!r}.",
            path,
        )
        status = str(card.get("status")) if card.get("status") is not None else None

    pdf_download = metadata.get("zo-pdf-download")
    pdf_branding = metadata.get("zo-pdf-branding")
    download_ok = isinstance(pdf_download, dict)
    branding_ok = isinstance(pdf_branding, dict)
    checker.add("function-pdf-download-yaml", download_ok, "zo-pdf-download hợp lệ." if download_ok else "zo-pdf-download phải là mapping.", path)
    checker.add("function-pdf-branding-yaml", branding_ok, "zo-pdf-branding hợp lệ." if branding_ok else "zo-pdf-branding phải là mapping.", path)

    label = pdf_download.get("label") if download_ok else None
    checker.add(
        "function-pdf-label", label == "Tải PDF",
        "Nhãn tải PDF đúng chuẩn." if label == "Tải PDF"
        else f"Kì vọng 'Tải PDF', nhận {label!r}.",
        path,
    )
    href = pdf_download.get("href") if download_ok else None
    expected_pdf = relative.with_suffix(".pdf").name
    href_shape = isinstance(href, str) and not urlsplit(href).scheme and Path(href).name == href and href.lower().endswith(".pdf")
    checker.add(
        "function-pdf-href", href_shape,
        f"href={href!r}." if href_shape else "href phải là tên PDF tương đối nằm cạnh bài.",
        path,
    )
    if href_shape and href != expected_pdf:
        checker.add_warning(
            "function-pdf-basename",
            f"href={href!r} khác tên mặc định {expected_pdf!r}; cần lí do trong hồ sơ.",
            path,
        )

    expected_url = FUNCTION_CANONICAL_BASE + relative.with_suffix(".html").as_posix()
    canonical = pdf_branding.get("canonical-url") if branding_ok else None
    checker.add(
        "function-canonical-url", canonical == expected_url,
        "canonical-url khớp đường dẫn bài." if canonical == expected_url
        else f"Kì vọng {expected_url!r}, nhận {canonical!r}.",
        path,
    )
    short_title = pdf_branding.get("short-title") if branding_ok else None
    display_url = pdf_branding.get("display-url") if branding_ok else None
    collection = pdf_branding.get("collection") if branding_ok else None
    branding_values_ok = (
        isinstance(short_title, str) and bool(short_title.strip())
        and display_url == "zo-math.github.io/zo-math"
        and collection == "100+ Hàm số: Sự biến thiên và đồ thị"
    )
    checker.add(
        "function-pdf-branding-values", branding_values_ok,
        "Các trường branding cốt lõi đúng chuẩn." if branding_values_ok
        else "short-title phải có giá trị; display-url và collection phải đúng chuẩn dự án.",
        path,
    )

    pdf_path = path.parent / str(href) if href_shape else path.with_suffix(".pdf")
    exists = pdf_path.exists() and pdf_path.stat().st_size > 0
    pdf_header = False
    if exists:
        try:
            pdf_header = pdf_path.read_bytes()[:5] == b"%PDF-"
        except OSError:
            pdf_header = False

    if status == "published":
        checker.add(
            "function-published-pdf", exists and pdf_header,
            f"PDF published tồn tại và có header PDF: {pdf_path.name}."
            if exists and pdf_header else f"Bài published thiếu PDF đọc được cơ bản: {pdf_path.name}.",
            path,
        )
    else:
        checker.add_info(
            "function-published-pdf",
            f"Trạng thái thẻ={status!r}; không chặn vì PDF vật lí ở tầng này.",
            path,
        )

    if exists:
        current = pdf_path.stat().st_mtime >= path.stat().st_mtime
        checker.add(
            "function-pdf-freshness", current,
            "PDF không cũ hơn QMD." if current else "PDF cũ hơn QMD; phải build lại.",
            path,
        )
        pdfinfo = shutil.which("pdfinfo")
        if pdfinfo:
            result = run([pdfinfo, str(pdf_path)], checker.root)
            pages_match = re.search(r"(?m)^Pages:\s*(\d+)\s*$", result.stdout)
            pages = int(pages_match.group(1)) if pages_match else 0
            checker.add(
                "function-pdf-readable", result.returncode == 0 and pages > 0,
                f"pdfinfo đọc được PDF, pages={pages}."
                if result.returncode == 0 and pages > 0
                else result.stderr.strip() or "pdfinfo không xác nhận được số trang hợp lệ.",
                path,
            )
            title_match = re.search(r"(?m)^Title:\s*(.*?)\s*$", result.stdout)
            actual_pdf_title = title_match.group(1).strip() if title_match else ""
            expected_pdf_title = str(metadata.get("title-meta", "")).strip()
            title_ok = (
                result.returncode == 0
                and bool(expected_pdf_title)
                and actual_pdf_title == expected_pdf_title
            )
            checker.add(
                "function-pdf-metadata-title", title_ok,
                f"PDF Title khớp title-meta: {actual_pdf_title!r}."
                if title_ok
                else f"Kì vọng PDF Title={expected_pdf_title!r}, nhận {actual_pdf_title!r}.",
                path,
            )
        else:
            checker.add_warning(
                "function-pdf-readable",
                "Không tìm thấy pdfinfo; mới chỉ kiểm tra header và kích thước PDF.",
                path,
            )
            checker.add_warning(
                "function-pdf-metadata-title",
                "Không tìm thấy pdfinfo; chưa đối chiếu được PDF Title với title-meta.",
                path,
            )
    else:
        checker.add_info(
            "function-pdf-metadata-title",
            "Chưa có PDF vật lí để đối chiếu Title với title-meta.",
            path,
        )
    return card, status


def function_profile_path(relative: Path, config: ProjectConfig) -> Path:
    return config.profile_path_for(relative)


def parse_expanded_figure_profile(
    relative: Path, checker: Checker, config: ProjectConfig
) -> tuple[dict[str, str], bool]:
    profile_relative = function_profile_path(relative, config)
    profile_path = checker.root / profile_relative
    if not profile_path.exists():
        checker.add_warning(
            "function-figure-layout-profile",
            f"Không tìm thấy hồ sơ {profile_relative.as_posix()}; chỉ kiểm tra được vị trí cú pháp của lớp mở rộng.",
            checker.root / relative,
        )
        return {}, False
    try:
        profile = load_yaml_unique(profile_path.read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        checker.add(
            "function-figure-layout-profile", False,
            f"Không đọc được hồ sơ bố cục hình: {exc}",
            checker.root / relative,
        )
        return {}, False
    if not isinstance(profile, dict):
        checker.add(
            "function-figure-layout-profile", False,
            "Hồ sơ sản xuất phải là một mapping YAML.",
            checker.root / relative,
        )
        return {}, False

    version = profile.get("phien_ban_ho_so")
    resources = profile.get("tai_nguyen_hinh")
    layout = resources.get("bo_cuc_qmd") if isinstance(resources, dict) else None
    structural_errors: list[str] = []
    if not isinstance(version, int) or version < 4:
        structural_errors.append(f"phien_ban_ho_so={version!r}, cần từ 4 trở lên")
    if not isinstance(layout, dict):
        structural_errors.append("thiếu tai_nguyen_hinh.bo_cuc_qmd")
        declared_raw: Any = []
    else:
        expected = {
            "mac_dinh_html": "trong_be_ngang_noi_dung",
            "mac_dinh_pdf": "trong_be_ngang_noi_dung",
            "lop_mo_rong_html": FUNCTION_EXPANDED_FIGURE_CLASS,
            "cam_lop_mo_rong_trong_pdf": True,
        }
        for key, value in expected.items():
            if layout.get(key) != value:
                structural_errors.append(
                    f"tai_nguyen_hinh.bo_cuc_qmd.{key}={layout.get(key)!r}, cần {value!r}"
                )
        declared_raw = layout.get("hinh_mo_rong_html", [])
        if not isinstance(declared_raw, list):
            structural_errors.append("hinh_mo_rong_html phải là list")
            declared_raw = []

    declared: dict[str, str] = {}
    entry_errors: list[str] = []
    for index, entry in enumerate(declared_raw, start=1):
        if not isinstance(entry, dict):
            entry_errors.append(
                f"mục {index} phải là mapping có id và li_do, nhận {type(entry).__name__}"
            )
            continue
        figure_id = entry.get("id")
        reason = entry.get("li_do")
        if isinstance(figure_id, str):
            figure_id = figure_id.strip().lstrip("#")
        if not isinstance(figure_id, str) or not re.fullmatch(r"fig-[A-Za-z0-9_-]+", figure_id):
            entry_errors.append(f"mục {index} có id không hợp lệ: {entry.get('id')!r}")
            continue
        if not isinstance(reason, str) or not reason.strip():
            entry_errors.append(f"mục {index} ({figure_id}) thiếu li_do cụ thể")
            continue
        if figure_id in declared:
            entry_errors.append(f"nhãn khai báo trùng: {figure_id}")
            continue
        declared[figure_id] = reason.strip()

    errors = structural_errors + entry_errors
    checker.add(
        "function-figure-layout-profile", not errors,
        (
            f"Hồ sơ phiên bản {version} khai báo {len(declared)} hình mở rộng HTML hợp lệ."
            if not errors else "; ".join(errors)
        ),
        checker.root / relative,
    )
    return declared, not errors


def expanded_figure_records(body: str) -> list[tuple[int, str | None, str | None]]:
    records: list[tuple[int, str | None, str | None]] = []
    stack: list[tuple[int, str]] = []
    opening_pattern = re.compile(r"^(:{3,})\s*\{([^}\n]*)\}\s*$")
    closing_pattern = re.compile(r"^(:{3,})\s*$")

    for number, line in enumerate(body.splitlines(), start=1):
        closing = closing_pattern.match(line)
        if closing:
            marker_length = len(closing.group(1))
            for index in range(len(stack) - 1, -1, -1):
                if stack[index][0] == marker_length:
                    del stack[index:]
                    break
            continue

        opening = opening_pattern.match(line)
        if not opening:
            continue
        marker_length = len(opening.group(1))
        attrs = opening.group(2)
        context = stack + [(marker_length, attrs)]
        classes = set(re.findall(r"\.([A-Za-z0-9_-]+)", attrs))
        if FUNCTION_EXPANDED_FIGURE_CLASS in classes:
            id_match = re.search(r"#(fig-[A-Za-z0-9_-]+)\b", attrs)
            branch_format: str | None = None
            for _, parent_attrs in reversed(context):
                parent_classes = set(re.findall(r"\.([A-Za-z0-9_-]+)", parent_attrs))
                if "content-visible" not in parent_classes:
                    continue
                format_match = re.search(
                    r"\bwhen-format\s*=\s*[\"']([^\"']+)[\"']", parent_attrs
                )
                if format_match:
                    branch_format = format_match.group(1).strip().casefold()
                    break
            records.append((number, id_match.group(1) if id_match else None, branch_format))
        stack.append((marker_length, attrs))
    return records


def validate_function_figure_layout(
    path: Path,
    relative: Path,
    body: str,
    checker: Checker,
    config: ProjectConfig,
) -> None:
    active = strip_fences_comments_and_inline_code(body)
    records = expanded_figure_records(active)
    declared, profile_ok = parse_expanded_figure_profile(
        relative, checker, config
    )

    wrong_branch = [
        f"dòng thân bài {line} ({branch or 'dùng chung'})"
        for line, _, branch in records if branch != "html"
    ]
    checker.add(
        "function-figure-layout-output", not wrong_branch,
        (
            "Lớp mở rộng chỉ xuất hiện trong nhánh HTML."
            if not wrong_branch else
            "Lớp mở rộng xuất hiện ngoài nhánh HTML: " + ", ".join(wrong_branch)
        ),
        path,
    )

    missing_id = [line for line, figure_id, _ in records if figure_id is None]
    checker.add(
        "function-figure-layout-id", not missing_id,
        (
            "Mọi hình mở rộng có nhãn fig-* hợp lệ."
            if not missing_id else
            "Hình mở rộng thiếu nhãn fig-* tại dòng thân bài: "
            + ", ".join(map(str, missing_id))
        ),
        path,
    )

    actual_ids = {figure_id for _, figure_id, _ in records if figure_id is not None}
    declared_ids = set(declared)
    if profile_ok:
        undeclared = sorted(actual_ids - declared_ids)
        unused = sorted(declared_ids - actual_ids)
        checker.add(
            "function-figure-layout-profile-match", not undeclared and not unused,
            (
                "Khai báo hồ sơ khớp các hình mở rộng HTML."
                if not undeclared and not unused else
                "; ".join(filter(None, [
                    "Chưa khai báo trong hồ sơ: " + ", ".join(undeclared) if undeclared else "",
                    "Khai báo thừa trong hồ sơ: " + ", ".join(unused) if unused else "",
                ]))
            ),
            path,
        )

    if not records and not declared_ids:
        checker.add(
            "function-figure-layout-default", True,
            "Không có hình dùng lớp mở rộng; áp dụng bố cục hình thường.",
            path,
        )
    elif records:
        checker.add(
            "function-figure-layout-default", True,
            f"Phát hiện {len(records)} lần dùng lớp mở rộng; đã kiểm tra nhánh đầu ra và hồ sơ.",
            path,
        )


def validate_function_body(
    path: Path, body: str, checker: Checker, config: ProjectConfig
) -> None:
    active = strip_fences_comments_and_inline_code(body)
    headings = validate_headings(
        path,
        active,
        checker,
        prefix="function",
        max_depth=4,
        allow_h1=False,
    )

    legacy = [token for token in FUNCTION_LEGACY_CLASSES if token in active]
    checker.add(
        "function-legacy-classes", not legacy,
        "Không có lớp cũ." if not legacy else "Phát hiện: " + ", ".join(legacy),
        path,
    )
    forbidden_latex = [
        token for token in (r"\(", r"\)", r"\[", r"\]", r"\boxed")
        if token in active
    ]
    checker.add(
        "function-latex-forbidden", not forbidden_latex,
        "Không có cấu trúc LaTeX bị cấm." if not forbidden_latex
        else "Phát hiện: " + ", ".join(forbidden_latex),
        path,
    )
    validate_forbidden_paths(
        path,
        active,
        checker,
        prefix="function",
    )

    validate_images(
        path,
        active,
        checker,
        prefix="function",
    )

    relative = path.relative_to(checker.root)
    validate_function_figure_layout(path, relative, body, checker, config)

    active_lines = active.splitlines()
    block_errors: list[str] = []
    fenced_blocks = 0
    for index, line in enumerate(active_lines):
        opening = re.match(r"^(:{3,})\s+\{([^}\n]*\.zo-block(?:\s|[}.])[^}\n]*)\}\s*$", line)
        if not opening:
            continue
        fenced_blocks += 1
        marker_length = len(opening.group(1))
        classes_text = opening.group(2)
        colors = [color for color in FUNCTION_BLOCK_COLORS if f".{color}" in classes_text]
        if len(colors) != 1:
            block_errors.append(f"dòng thân bài {index + 1}: khối cần đúng một lớp màu")
        closing_index = None
        for candidate in range(index + 1, len(active_lines)):
            close = re.match(r"^(:{3,})\s*$", active_lines[candidate])
            if close and len(close.group(1)) >= marker_length:
                closing_index = candidate
                break
        if closing_index is None:
            block_errors.append(f"dòng thân bài {index + 1}: khối fenced chưa đóng")
            segment = "\n".join(active_lines[index + 1:])
        else:
            segment = "\n".join(active_lines[index + 1:closing_index])
        if ".zo-block-title" not in segment:
            block_errors.append(f"dòng thân bài {index + 1}: thiếu zo-block-title")

    detail_openings = list(re.finditer(
        r"<details\b[^>]*class=[\"'][^\"']*\bzo-block\b[^\"']*[\"'][^>]*>",
        active, flags=re.IGNORECASE,
    ))
    details_blocks = re.findall(
        r"<details\b[^>]*class=[\"'][^\"']*\bzo-block\b[^\"']*[\"'][^>]*>(.*?)</details>",
        active, flags=re.IGNORECASE | re.DOTALL,
    )
    if len(detail_openings) != len(details_blocks):
        block_errors.append("Có details.zo-block chưa đóng đúng")
    for index, (opening_match, block) in enumerate(zip(detail_openings, details_blocks), start=1):
        colors = [color for color in FUNCTION_BLOCK_COLORS if color in opening_match.group(0)]
        if len(colors) != 1:
            block_errors.append(f"details zo-block #{index} cần đúng một lớp màu")
        if not re.search(r"<summary\b[^>]*class=[\"'][^\"']*\bzo-block-title\b", block, flags=re.IGNORECASE):
            block_errors.append(f"details zo-block #{index} thiếu summary.zo-block-title")
        if not re.search(r"<div\b[^>]*class=[\"'][^\"']*\bzo-block-body\b", block, flags=re.IGNORECASE):
            block_errors.append(f"details zo-block #{index} thiếu div.zo-block-body")
    checker.add(
        "function-block-structure", not block_errors,
        f"{fenced_blocks + len(details_blocks)} khối có cấu trúc cơ bản hợp lệ."
        if not block_errors else "; ".join(block_errors),
        path,
    )

    exercise_index = next(
        (index for index, (_, level, title) in enumerate(headings)
         if level == 2 and re.fullmatch(
             r"Bài tập", re.sub(r"\s+\{[^}]*\}\s*$", "", title), flags=re.IGNORECASE
         )),
        None,
    )
    if exercise_index is None:
        checker.add_info("function-exercises", "Hệ bài tập không xuất hiện; cần khớp quyết định trong hồ sơ.", path)
    else:
        section = headings[exercise_index + 1:]
        end = next((index for index, (_, level, _) in enumerate(section) if level <= 2), len(section))
        section = section[:end]
        has_h3 = any(level == 3 for _, level, _ in section)
        has_h4 = any(level == 4 for _, level, _ in section)
        checker.add(
            "function-exercise-structure", has_h3 and has_h4,
            "Phần bài tập có nhóm H3 và bài H4."
            if has_h3 and has_h4 else "Phần bài tập phải có ít nhất một nhóm H3 và một bài H4.",
            path,
        )

    validate_executable_code(
        path,
        body,
        checker,
        prefix="function",
    )


def validate_function_article(
    path: Path,
    text: str,
    checker: Checker,
    context: ArticleValidationContext,
) -> None:
    relative = path.relative_to(checker.root)
    config = function_project_config(relative, checker, context.config)
    if config is None:
        return
    document = validate_qmd_front_matter(
        path,
        text,
        checker,
        prefix="function",
    )
    if document is None:
        return
    validate_placeholders(
        path,
        text,
        checker,
        prefix="function",
        placeholders=config.placeholders,
    )
    checker.add(
        "qmd-core-validator",
        True,
        "Đã áp dụng validator lõi dùng chung cho function_article.",
        path,
    )
    metadata = document.metadata
    body = document.body
    validate_function_metadata(path, relative, metadata, checker, config)
    validate_function_body(path, body, checker, config)
    checker.add_warning(
        "function-human-review-required",
        "Kiểm định tự động không thay thế việc đọc mạch, kiểm tra màu/trạng thái khối, "
        "HTML desktop/mobile, hình, bài tập và PDF thật.",
        path,
    )


def validate_rendered_function_page(
    relative: Path,
    html: Path,
    checker: Checker,
    context: ArticleValidationContext,
) -> None:
    source = checker.root / relative
    try:
        source_text = source.read_text(encoding="utf-8")
        html_text = html.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        checker.add("function-rendered-html-read", False, str(exc), relative)
        return
    metadata, _, error = split_qmd_front_matter(source_text)
    if error or metadata is None:
        checker.add("function-rendered-html-metadata", False, error or "Không đọc được YAML.", relative)
        return
    config = function_project_config(relative, checker, context.config)
    if config is None:
        return
    body_match = re.search(r"<body\b[^>]*class=[\"']([^\"']*)[\"']", html_text, flags=re.IGNORECASE)
    body_classes = set(body_match.group(1).split()) if body_match else set()
    required_body_classes = set(config.required_body_classes)
    classes_ok = required_body_classes.issubset(body_classes)
    checker.add(
        "function-rendered-body-classes", classes_ok,
        "Thẻ body chứa hai lớp trang bắt buộc." if classes_ok
        else "Thẻ body thiếu: " + ", ".join(sorted(required_body_classes - body_classes)),
        relative,
    )
    h1_count = len(re.findall(r"<h1\b", html_text, flags=re.IGNORECASE))
    if h1_count > 1:
        checker.add_warning(
            "function-rendered-h1-count",
            f"HTML có {h1_count} thẻ H1; cần kiểm tra tiêu đề lặp.",
            relative,
        )
    else:
        checker.add("function-rendered-h1-count", True, f"HTML có {h1_count} thẻ H1.", relative)
    pdf_download = metadata.get("zo-pdf-download")
    href = pdf_download.get("href") if isinstance(pdf_download, dict) else None
    if isinstance(href, str) and href:
        href_present = bool(re.search(
            rf"""href=["'][^"']*{re.escape(Path(href).name)}(?:[?#][^"']*)?["']""",
            html_text,
            flags=re.IGNORECASE,
        ))
        checker.add(
            "function-rendered-pdf-link", href_present,
            f"HTML có liên kết tới {Path(href).name}."
            if href_present else f"HTML không có liên kết tới {Path(href).name}.",
            relative,
        )
        published_pdf = html.parent / Path(href).name
        card, _ = function_card(relative, metadata, checker)
        status = card.get("status") if isinstance(card, dict) else None
        if status == "published":
            checker.add(
                "function-rendered-pdf-resource", published_pdf.exists(),
                f"Đầu ra published có {published_pdf.name}."
                if published_pdf.exists() else f"Đầu ra published thiếu {published_pdf.name}.",
                relative,
            )
        elif published_pdf.exists():
            checker.add_info(
                "function-rendered-pdf-resource",
                f"Đầu ra có {published_pdf.name}; trạng thái thẻ={status!r}.",
                relative,
            )
        else:
            checker.add_info(
                "function-rendered-pdf-resource",
                f"Đầu ra chưa có {published_pdf.name}; trạng thái thẻ={status!r}.",
                relative,
            )
    checker.add_warning(
        "function-rendered-visual-review",
        "Cần mở HTML ở desktop/mobile và PDF thật; kiểm tra tự động chỉ xác nhận cấu trúc có thể mã hóa.",
        relative,
    )


SourceValidatorAdapter = Callable[
    [Path, str, Checker, ArticleValidationContext], None
]
RenderValidatorAdapter = Callable[
    [Path, Path, Checker, ArticleValidationContext], None
]

SOURCE_VALIDATOR_ADAPTERS: dict[str, SourceValidatorAdapter] = {
    "functions-article": validate_function_article,
    "real-world-problem": validate_real_world_problem_article,
}
RENDER_VALIDATOR_ADAPTERS: dict[str, RenderValidatorAdapter] = {
    "functions-article": validate_rendered_function_page,
    "real-world-problem": validate_rendered_real_world_problem_page,
}


def dispatch_article_source_validators(
    relative: Path, text: str, checker: Checker
) -> ArticleValidationContext | None:
    context = article_validation_context(relative, checker.root, checker)
    if context is None:
        return None
    path = checker.root / relative
    for adapter_id in context.plan.source_adapters:
        adapter = SOURCE_VALIDATOR_ADAPTERS.get(adapter_id)
        if adapter is None:
            checker.add(
                "qmd-source-adapter",
                False,
                f"Source adapter ch\u01b0a \u0111\u01b0\u1ee3c c\u00e0i \u0111\u1eb7t: {adapter_id!r}.",
                relative,
            )
            continue
        checker.add(
            "qmd-source-adapter",
            True,
            f"Áp dụng source adapter {adapter_id!r}.",
            relative,
        )
        adapter(path, text, checker, context)
    return context


def dispatch_article_render_validators(
    relative: Path, html: Path, checker: Checker
) -> ArticleValidationContext | None:
    context = article_validation_context(
        relative, checker.root, checker, report=False
    )
    if context is None:
        return None
    for adapter_id in context.plan.render_adapters:
        adapter = RENDER_VALIDATOR_ADAPTERS.get(adapter_id)
        if adapter is None:
            checker.add(
                "qmd-render-adapter",
                False,
                f"Render adapter ch\u01b0a \u0111\u01b0\u1ee3c c\u00e0i \u0111\u1eb7t: {adapter_id!r}.",
                relative,
            )
            continue
        checker.add(
            "qmd-render-adapter",
            True,
            f"Áp dụng render adapter {adapter_id!r}.",
            relative,
        )
        adapter(relative, html, checker, context)
    return context


def article_requires_human_acceptance(relative: Path, root: Path) -> bool:
    context = article_validation_context(relative, root, report=False)
    return bool(context and context.plan.requires_human_acceptance)


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
                metadata = load_yaml_unique(parts[1]) or {}
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
        if suffix == ".qmd":
            dispatch_article_source_validators(relative, text, checker)


def card_scope(paths: Sequence[Path]) -> bool:
    for path in paths:
        if path in CARD_COMPONENTS or path == CARD_IMAGE_DIR or CARD_IMAGE_DIR in path.parents:
            return True
    return False


def check_card_grid(checker: Checker) -> None:
    data_path = checker.root / CARD_PROJECT / "_data/cards.yml"
    partial_path = checker.root / CARD_PROJECT / "_partials/card_grid.qmd"
    try:
        data = load_yaml_unique(data_path.read_text(encoding="utf-8"))
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
    config = load_yaml_unique((root / "_quarto.yml").read_text(encoding="utf-8")) or {}
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
        if html.exists():
            dispatch_article_render_validators(relative, html, checker)
    return None


def print_results(checker: Checker, scope: Sequence[Path]) -> None:
    print(f"CHECKER VERSION: {CHECKER_VERSION}")
    print(f"MODE: {checker.mode} | {'STAGED' if checker.staged else 'WORKTREE'}")
    print(f"ROOT: {checker.root}")
    print(f"SCOPE ({len(scope)}):")
    for path in scope:
        print(f"  - {path.as_posix()}")
    print("CHECKS:")
    labels = {"pass": "PASS", "fail": "FAIL", "warn": "WARN", "info": "INFO"}
    for item in checker.checks:
        location = f" [{item.path}]" if item.path else ""
        print(f"  {labels.get(item.status, item.status.upper())} {item.name}{location}: {item.message}")
    for warning in checker.warnings:
        print(f"  WARN render-log: {warning}")


def report_path(root: Path, raw: str) -> Path | None:
    target = (Path(raw) if Path(raw).is_absolute() else root / raw).resolve()
    audit = (root / "_audit").resolve()
    return target if inside(target, audit) and target.suffix.lower() == ".json" else None


def write_report(path: Path, checker: Checker, scope: Sequence[Path], exit_code: int) -> None:
    automated_result = "FAIL" if checker.failed else ("PASS_WITH_WARNINGS" if checker.has_warnings else "PASS")
    payload = {
        "checker_version": CHECKER_VERSION,
        "mode": checker.mode,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "automated_result": automated_result,
        "final_acceptance": "NOT_RUN",
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
    result_label = "FAIL" if checker.failed else ("PASS_WITH_WARNINGS" if checker.has_warnings else "PASS")
    print(f"AUTOMATED RESULT: {result_label} | EXIT={exit_code}")
    if any(article_requires_human_acceptance(path, root) for path in paths):
        print("FINAL ACCEPTANCE: NOT_RUN — cần kiểm định có người quan sát theo quy chuẩn.")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())

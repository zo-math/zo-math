"""Reusable core validation for configured QMD articles.

The module contains checks that are independent of a particular ZO Math
content project.  Project validators choose a check-name prefix and supply
metadata, class, and placeholder requirements from project configuration.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, Sequence

try:
    import yaml
except ImportError:  # Reported by the CLI with a stable exit code.
    yaml = None


EXIT_OK = 0
EXIT_INVALID = 1
EXIT_USAGE = 2
EXIT_MISSING_TOOL = 3


class CheckSink(Protocol):
    """Minimal checker interface required by the reusable core."""

    def add(
        self, name: str, passed: bool, message: str, path: Path | None = None
    ) -> None: ...

    def add_warning(
        self, name: str, message: str, path: Path | None = None
    ) -> None: ...

    def add_info(
        self, name: str, message: str, path: Path | None = None
    ) -> None: ...


@dataclass(frozen=True)
class QmdDocument:
    """Parsed QMD front matter and body."""

    metadata: dict[str, Any]
    body: str


Heading = tuple[int, int, str]
ImageRecord = tuple[int, str, str | None, str]


def _load_yaml_unique(text: str) -> Any:
    if yaml is None:
        raise RuntimeError("Thiếu dependency PyYAML.")

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


def split_qmd_front_matter(
    text: str,
) -> tuple[dict[str, Any] | None, str, str | None]:
    """Split YAML front matter from a QMD source string."""

    match = re.match(
        r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)",
        text,
        flags=re.DOTALL,
    )
    if not match:
        return None, text, "Thiếu YAML front matter ở đầu tệp."
    raw = match.group(1)
    try:
        value = _load_yaml_unique(raw) or {}
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        where = f"dòng {mark.line + 2}, cột {mark.column + 1}: " if mark else ""
        return None, text[match.end():], where + str(exc).splitlines()[0]
    if not isinstance(value, dict):
        return None, text[match.end():], "YAML front matter phải là mapping."
    return value, text[match.end():], None


def validate_qmd_front_matter(
    path: Path,
    text: str,
    checker: CheckSink,
    *,
    prefix: str,
) -> QmdDocument | None:
    """Parse front matter and emit the prefixed core check."""

    metadata, body, error = split_qmd_front_matter(text)
    if error or metadata is None:
        checker.add(
            f"{prefix}-front-matter",
            False,
            error or "Không đọc được YAML.",
            path,
        )
        return None
    checker.add(
        f"{prefix}-front-matter",
        True,
        "YAML front matter hợp lệ.",
        path,
    )
    return QmdDocument(metadata=metadata, body=body)


def metadata_nonempty(value: Any) -> bool:
    """Return whether a metadata value is materially non-empty."""

    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value) and all(metadata_nonempty(item) for item in value)
    return value is not None


def validate_placeholders(
    path: Path,
    text: str,
    checker: CheckSink,
    *,
    prefix: str,
    placeholders: Sequence[str],
) -> None:
    """Reject configured placeholder tokens without owning their vocabulary."""

    found = [
        token
        for token in placeholders
        if token.casefold() in text.casefold()
    ]
    checker.add(
        f"{prefix}-placeholders",
        not found,
        "Không còn giá trị giữ chỗ."
        if not found
        else "Phát hiện: " + ", ".join(sorted(set(found))),
        path,
    )


def validate_required_metadata(
    path: Path,
    metadata: dict[str, Any],
    checker: CheckSink,
    *,
    prefix: str,
    required: Sequence[str],
) -> None:
    """Validate presence and non-empty values for configured metadata."""

    required_set = set(required)
    missing = sorted(key for key in required_set if key not in metadata)
    checker.add(
        f"{prefix}-yaml-required",
        not missing,
        "Đủ trường YAML bắt buộc."
        if not missing
        else "Thiếu: " + ", ".join(missing),
        path,
    )
    empty = sorted(
        key
        for key in required_set
        if key in metadata and not metadata_nonempty(metadata[key])
    )
    checker.add(
        f"{prefix}-yaml-values",
        not empty,
        "Các trường bắt buộc có giá trị."
        if not empty
        else "Rỗng: " + ", ".join(empty),
        path,
    )


def validate_required_body_classes(
    path: Path,
    metadata: dict[str, Any],
    checker: CheckSink,
    *,
    prefix: str,
    required: Sequence[str],
) -> None:
    """Validate configured body classes."""

    classes = str(metadata.get("body-classes", "")).split()
    required_set = set(required)
    missing = required_set - set(classes)
    if not missing and required_set == {"zo-page-article", "zo-meta-hidden"}:
        message = "Có đủ zo-page-article và zo-meta-hidden."
    elif not missing:
        message = "Có đủ body-classes bắt buộc."
    else:
        message = "body-classes thiếu: " + ", ".join(sorted(missing))
    checker.add(f"{prefix}-body-classes", not missing, message, path)


def strip_fences_comments_and_inline_code(text: str) -> str:
    """Remove regions that must not participate in structural body checks."""

    lines = text.splitlines(keepends=True)
    output: list[str] = []
    fence: tuple[str, int] | None = None
    in_comment = False
    for line in lines:
        working = line
        if in_comment:
            if "-->" in working:
                _, working = working.split("-->", 1)
                in_comment = False
            else:
                output.append("\n" if line.endswith(("\n", "\r")) else "")
                continue
        while "<!--" in working:
            before, rest = working.split("<!--", 1)
            if "-->" in rest:
                _, after = rest.split("-->", 1)
                working = before + after
            else:
                working = before
                in_comment = True
                break
        stripped = working.lstrip()
        marker = re.match(r"(`{3,}|~{3,})", stripped)
        if fence is None and marker:
            token = marker.group(1)
            fence = (token[0], len(token))
            output.append("\n" if line.endswith(("\n", "\r")) else "")
            continue
        if fence is not None:
            close = re.match(
                rf"{re.escape(fence[0])}{{{fence[1]},}}[ \t]*$",
                stripped.rstrip("\r\n"),
            )
            if close:
                fence = None
            output.append("\n" if line.endswith(("\n", "\r")) else "")
            continue
        working = re.sub(r"`[^`\r\n]*`", "", working)
        output.append(working)
    return "".join(output)


def analyze_headings(active: str) -> list[Heading]:
    """Return Markdown headings outside fenced code and comments."""

    headings: list[Heading] = []
    for number, line in enumerate(active.splitlines(), start=1):
        match = re.match(r"^(#{1,6})[ \t]+(.+?)\s*$", line)
        if match:
            headings.append(
                (number, len(match.group(1)), match.group(2).strip())
            )
    return headings


def validate_headings(
    path: Path,
    active: str,
    checker: CheckSink,
    *,
    prefix: str,
    max_depth: int = 4,
    allow_h1: bool = False,
) -> list[Heading]:
    """Validate generic heading structure and return the parsed headings."""

    from collections import Counter

    headings = analyze_headings(active)
    h1 = [number for number, level, _ in headings if level == 1]
    checker.add(
        f"{prefix}-heading-h1",
        allow_h1 or not h1,
        "Không có H1 trong thân bài."
        if allow_h1 or not h1
        else "H1 tại dòng thân bài: " + ", ".join(map(str, h1)),
        path,
    )
    duplicates = [
        f"H{level} {title!r}"
        for (level, title), count in Counter(
            (
                level,
                re.sub(r"\s+\{[^}]*\}\s*$", "", title).casefold(),
            )
            for _, level, title in headings
        ).items()
        if count > 1
    ]
    if duplicates:
        checker.add_warning(
            f"{prefix}-heading-duplicates",
            "Tiêu đề trùng cần xét ngữ cảnh: " + ", ".join(duplicates),
            path,
        )
    else:
        checker.add(
            f"{prefix}-heading-duplicates",
            True,
            "Không có tiêu đề trùng hoàn toàn.",
            path,
        )

    deep = [number for number, level, _ in headings if level > max_depth]
    if deep:
        checker.add_warning(
            f"{prefix}-heading-depth",
            f"H{max_depth + 1}/H6 cần lí do và kiểm tra trực quan tại dòng thân bài: "
            + ", ".join(map(str, deep)),
            path,
        )
    else:
        checker.add(
            f"{prefix}-heading-depth",
            True,
            f"Không dùng cấp sâu hơn H{max_depth}.",
            path,
        )

    jumps: list[str] = []
    previous = 1
    for number, level, _ in headings:
        if level > previous + 1:
            jumps.append(f"{previous}->H{level} tại dòng {number}")
        previous = level
    checker.add(
        f"{prefix}-heading-order",
        not jumps,
        "Không nhảy cấp tiêu đề." if not jumps else "; ".join(jumps),
        path,
    )

    empty = [
        number
        for number, line in enumerate(active.splitlines(), 1)
        if re.match(r"^#{1,6}[ \t]*$", line)
    ]
    checker.add(
        f"{prefix}-heading-empty",
        not empty,
        "Không có tiêu đề rỗng."
        if not empty
        else "Tiêu đề rỗng tại dòng: " + ", ".join(map(str, empty)),
        path,
    )
    return headings


def validate_forbidden_paths(
    path: Path,
    active: str,
    checker: CheckSink,
    *,
    prefix: str,
) -> None:
    """Reject machine-local and generated-output paths in article bodies."""

    forbidden: list[str] = []
    path_patterns = {
        "đường dẫn ổ đĩa": r"(?i)(?<![A-Za-z0-9_])[A-Z]:[\\/]",
        "đường dẫn Unix cục bộ": r"(?m)(?:^|[\"'(= \t])/(?:home|Users|tmp|var/tmp)/",
        "localhost": r"(?i)https?://(?:localhost|127\.0\.0\.1)(?::\d+)?",
        "docs/": r"(?i)(?:^|[\"'(= \t])docs/",
        "_audit/": r"(?i)(?:^|[\"'(= \t])_audit/",
    }
    for label, pattern in path_patterns.items():
        if re.search(pattern, active, flags=re.MULTILINE):
            forbidden.append(label)
    checker.add(
        f"{prefix}-forbidden-paths",
        not forbidden,
        "Không có đường dẫn bị cấm trong thân bài."
        if not forbidden
        else "Phát hiện: " + ", ".join(forbidden),
        path,
    )


def qmd_image_records(body: str) -> list[ImageRecord]:
    """Return Markdown image references with line and attribute data."""

    records: list[ImageRecord] = []
    expression = re.compile(
        r"!\[(?P<alt>[^\]\r\n]*)\]\((?P<target>[^)\r\n]+)\)"
        r"(?:\{(?P<attrs>[^}\r\n]*)\})?"
    )
    for match in expression.finditer(body):
        line = body.count("\n", 0, match.start()) + 1
        records.append(
            (
                line,
                match.group("target").strip(),
                match.group("attrs"),
                match.group("alt"),
            )
        )
    return records


def validate_images(
    path: Path,
    active: str,
    checker: CheckSink,
    *,
    prefix: str,
) -> None:
    """Validate relative paths, alternative text, and fixed pixel widths."""

    images = qmd_image_records(active)
    missing_alt = [
        line
        for line, _, attrs, _ in images
        if not attrs
        or (
            not re.search(
                r"(?:^|\s)fig-alt\s*=\s*[\"'][^\"']+[\"']",
                attrs,
            )
            and not re.search(
                r"(?:^|\s)(?:role\s*=\s*[\"']presentation[\"']|aria-hidden\s*=\s*[\"']true[\"'])",
                attrs,
                flags=re.IGNORECASE,
            )
        )
    ]
    non_relative = [
        line
        for line, target, _, _ in images
        if target.startswith("/") or re.match(r"(?i)^[A-Z]:[\\/]", target)
    ]
    checker.add(
        f"{prefix}-image-relative-paths",
        not non_relative,
        "Hình trong thân bài dùng đường dẫn tương đối."
        if not non_relative
        else "Hình dùng đường dẫn không tương đối tại dòng thân bài: "
        + ", ".join(map(str, sorted(set(non_relative)))),
        path,
    )

    html_images = list(re.finditer(r"<img\b[^>]*>", active, flags=re.IGNORECASE))
    missing_html_alt = [
        active.count("\n", 0, match.start()) + 1
        for match in html_images
        if (
            not re.search(
                r"\balt=[\"'][^\"']+[\"']",
                match.group(0),
                flags=re.IGNORECASE,
            )
            and not re.search(
                r"\b(?:role=[\"']presentation[\"']|aria-hidden=[\"']true[\"'])",
                match.group(0),
                flags=re.IGNORECASE,
            )
        )
    ]
    missing_alt.extend(missing_html_alt)
    checker.add(
        f"{prefix}-fig-alt",
        not missing_alt,
        "Mọi hình mang thông tin có văn bản thay thế."
        if not missing_alt
        else "Thiếu fig-alt/alt tại dòng thân bài: "
        + ", ".join(map(str, sorted(set(missing_alt)))),
        path,
    )

    fixed_width = [
        line
        for line, _, attrs, _ in images
        if attrs
        and re.search(
            r"\bwidth\s*=\s*[\"']?\d+(?:px)?[\"']?(?=\s|$)",
            attrs,
            flags=re.IGNORECASE,
        )
    ]
    if fixed_width:
        checker.add_warning(
            f"{prefix}-fixed-pixel-width",
            "Chiều rộng pixel cố định cần lí do và kiểm tra đa đầu ra tại dòng thân bài: "
            + ", ".join(map(str, fixed_width)),
            path,
        )
    else:
        checker.add(
            f"{prefix}-fixed-pixel-width",
            True,
            "Không có width pixel cố định.",
            path,
        )


def validate_executable_code(
    path: Path,
    body: str,
    checker: CheckSink,
    *,
    prefix: str,
) -> None:
    """Flag executable chunks and reject clearly unsafe article code."""

    chunks = re.findall(
        r"(?m)^(```|~~~)\{(?:r|python|julia|bash|sh)\b",
        body,
        flags=re.IGNORECASE,
    )
    if chunks:
        checker.add_warning(
            f"{prefix}-executable-code",
            f"Phát hiện {len(chunks)} code chunk thực thi; cần xác nhận mục đích, phụ thuộc và đầu ra.",
            path,
        )
    dangerous: list[str] = []
    for label, pattern in {
        "cài thư viện": r"(?i)\b(?:install\.packages|pip\s+install|conda\s+install)\b",
        "setwd": r"(?i)\bsetwd\s*\(",
    }.items():
        if re.search(pattern, body):
            dangerous.append(label)
    checker.add(
        f"{prefix}-code-forbidden",
        not dangerous,
        "Không có thao tác mã bị cấm rõ ràng."
        if not dangerous
        else "Phát hiện: " + ", ".join(dangerous),
        path,
    )


class _SelfTestChecker:
    def __init__(self) -> None:
        self.records: list[tuple[str, str]] = []

    def add(
        self, name: str, passed: bool, message: str, path: Path | None = None
    ) -> None:
        self.records.append((name, "pass" if passed else "fail"))

    def add_warning(
        self, name: str, message: str, path: Path | None = None
    ) -> None:
        self.records.append((name, "warn"))

    def add_info(
        self, name: str, message: str, path: Path | None = None
    ) -> None:
        self.records.append((name, "info"))


def _self_test() -> None:
    if yaml is None:
        raise RuntimeError("Thiếu dependency PyYAML.")

    source = """---
title: Demo
body-classes: zo-page-article zo-meta-hidden
---
## Mục thứ nhất

![Đồ thị](figure.svg){fig-alt=\"Đồ thị minh họa\"}
"""
    checker = _SelfTestChecker()
    path = Path("content/demo.qmd")
    document = validate_qmd_front_matter(
        path, source, checker, prefix="demo"
    )
    assert document is not None
    validate_placeholders(
        path,
        source,
        checker,
        prefix="demo",
        placeholders=("CHUA_XAC_DINH",),
    )
    validate_required_metadata(
        path,
        document.metadata,
        checker,
        prefix="demo",
        required=("title", "body-classes"),
    )
    validate_required_body_classes(
        path,
        document.metadata,
        checker,
        prefix="demo",
        required=("zo-page-article", "zo-meta-hidden"),
    )
    active = strip_fences_comments_and_inline_code(document.body)
    headings = validate_headings(path, active, checker, prefix="demo")
    validate_forbidden_paths(path, active, checker, prefix="demo")
    validate_images(path, active, checker, prefix="demo")
    validate_executable_code(path, document.body, checker, prefix="demo")
    assert headings == [(1, 2, "Mục thứ nhất")]
    assert not any(status == "fail" for _, status in checker.records)

    metadata, _, error = split_qmd_front_matter(
        "---\ntitle: A\ntitle: B\n---\n"
    )
    assert metadata is None and error is not None


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    subparsers = result.add_subparsers(dest="command", required=True)
    subparsers.add_parser("self-test", help="Chạy kiểm tra nội bộ độc lập.")
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if yaml is None:
        print("ERROR: Thiếu dependency PyYAML.")
        return EXIT_MISSING_TOOL
    if args.command == "self-test":
        try:
            _self_test()
        except (AssertionError, RuntimeError) as exc:
            print(f"ERROR: zo_qmd_core self-test: {exc}")
            return EXIT_INVALID
        print("PASS: zo_qmd_core self-test")
        return EXIT_OK
    return EXIT_USAGE


if __name__ == "__main__":
    raise SystemExit(main())

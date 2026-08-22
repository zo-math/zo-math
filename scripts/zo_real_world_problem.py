"""Project validator for 100+ Bài toán thực tế QMD articles.

The module reuses ``zo_qmd_core`` for project-independent checks and adds the
minimum contract needed to validate a real-world modelling article, its local
production profile, and its rendered HTML page.
"""

from __future__ import annotations

import argparse
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Protocol, Sequence
from urllib.parse import urlsplit

try:
    import yaml
except ImportError:  # Reported by the CLI with a stable exit code.
    yaml = None

from zo_qmd_core import (
    QmdDocument,
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


EXIT_OK = 0
EXIT_INVALID = 1
EXIT_MISSING_TOOL = 3


class CheckSink(Protocol):
    root: Path

    def add(
        self, name: str, passed: bool, message: str, path: Path | None = None
    ) -> None: ...

    def add_warning(
        self, name: str, message: str, path: Path | None = None
    ) -> None: ...

    def add_info(
        self, name: str, message: str, path: Path | None = None
    ) -> None: ...


class ProjectConfigLike(Protocol):
    project_id: str
    project_root: Path
    profile_required: bool
    core_required_metadata: tuple[str, ...]
    project_required_metadata: tuple[str, ...]
    required_body_classes: tuple[str, ...]
    placeholders: tuple[str, ...]
    raw: Mapping[str, Any]

    def profile_path_for(self, repository_relative: Path) -> Path: ...


class ValidationContextLike(Protocol):
    config: ProjectConfigLike | None
    article_type: str


@dataclass(frozen=True)
class RealWorldRules:
    required_sections: tuple[str, ...]
    forbidden_metadata: tuple[str, ...]
    collection: str
    canonical_base: str
    display_url: str
    profile_version: int


@dataclass(frozen=True)
class ProfileState:
    production: str
    publication: str
    confirmed: bool


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


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any) -> tuple[str, ...] | None:
    if not isinstance(value, list):
        return None
    if not all(_nonempty_string(item) for item in value):
        return None
    return tuple(str(item).strip() for item in value)


def _rules(config: ProjectConfigLike) -> RealWorldRules:
    extensions = config.raw.get("extensions")
    if not isinstance(extensions, dict):
        raise ValueError("extensions phải là mapping.")
    raw = extensions.get("real_world_problem")
    if not isinstance(raw, dict):
        raise ValueError("Thiếu extensions.real_world_problem.")

    required_sections = _string_list(raw.get("required_sections"))
    if not required_sections:
        raise ValueError(
            "extensions.real_world_problem.required_sections phải là list không rỗng."
        )
    forbidden_metadata = _string_list(raw.get("forbidden_metadata"))
    if forbidden_metadata is None:
        raise ValueError(
            "extensions.real_world_problem.forbidden_metadata phải là list."
        )
    collection = raw.get("collection")
    canonical_base = raw.get("canonical_base")
    display_url = raw.get("display_url")
    profile_version = raw.get("profile_version")
    if not _nonempty_string(collection):
        raise ValueError("extensions.real_world_problem.collection phải có giá trị.")
    if not _nonempty_string(canonical_base):
        raise ValueError("extensions.real_world_problem.canonical_base phải có giá trị.")
    if not _nonempty_string(display_url):
        raise ValueError("extensions.real_world_problem.display_url phải có giá trị.")
    if not isinstance(profile_version, int) or profile_version < 1:
        raise ValueError(
            "extensions.real_world_problem.profile_version phải là số nguyên dương."
        )
    return RealWorldRules(
        required_sections=required_sections,
        forbidden_metadata=forbidden_metadata,
        collection=str(collection).strip(),
        canonical_base=str(canonical_base).strip().rstrip("/") + "/",
        display_url=str(display_url).strip(),
        profile_version=profile_version,
    )


def _config_for(
    relative: Path,
    checker: CheckSink,
    context: ValidationContextLike,
) -> tuple[ProjectConfigLike, RealWorldRules] | None:
    config = context.config
    if config is None:
        checker.add(
            "real-world-project-config",
            False,
            "Bài toán thực tế chưa có cấu hình dự án điều khiển.",
            relative,
        )
        return None
    if context.article_type != "real_world_problem":
        checker.add(
            "real-world-project-config",
            False,
            f"Kì vọng article_type='real_world_problem', nhận {context.article_type!r}.",
            relative,
        )
        return None
    try:
        rules = _rules(config)
    except ValueError as exc:
        checker.add("real-world-project-config", False, str(exc), relative)
        return None
    checker.add(
        "real-world-project-config",
        True,
        f"Đã nạp hợp đồng dự án từ project={config.project_id!r}.",
        relative,
    )
    return config, rules


def _contains_tex_markup(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    return bool(re.search(r"\$|\\[A-Za-z]+|\\\(|\\\[", value))


def _normalize_heading(title: str) -> str:
    return re.sub(r"\s+\{[^}]*\}\s*$", "", title).strip().casefold()


def _validate_fixed_metadata(
    path: Path,
    metadata: dict[str, Any],
    checker: CheckSink,
) -> None:
    expected = {
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
        for key, value in expected.items()
        if metadata.get(key) != value
    ]
    checker.add(
        "real-world-yaml-fixed-values",
        not wrong,
        "Các giá trị cố định đúng chuẩn."
        if not wrong
        else "Sai: " + ", ".join(wrong),
        path,
    )

    plain = {
        "title-meta": metadata.get("title-meta"),
        "pagetitle": metadata.get("pagetitle"),
    }
    bad = [f"{key}={value!r}" for key, value in plain.items() if _contains_tex_markup(value)]
    checker.add(
        "real-world-title-plain-metadata",
        not bad,
        "title-meta và pagetitle dùng văn bản thuần."
        if not bad
        else "Không được chứa TeX: " + ", ".join(bad),
        path,
    )


def _validate_project_metadata(
    path: Path,
    relative: Path,
    metadata: dict[str, Any],
    checker: CheckSink,
    rules: RealWorldRules,
) -> None:
    forbidden = sorted(key for key in rules.forbidden_metadata if key in metadata)
    checker.add(
        "real-world-forbidden-metadata",
        not forbidden,
        "Không mang metadata riêng của dự án hàm số."
        if not forbidden
        else "Không được khai báo: " + ", ".join(forbidden),
        path,
    )

    image = metadata.get("image")
    image_ok = (
        isinstance(image, str)
        and image.startswith("/")
        and (checker.root / image.lstrip("/")).is_file()
    )
    checker.add(
        "real-world-card-image",
        image_ok,
        f"Ảnh đại diện tồn tại: {image}"
        if image_ok
        else f"Ảnh đại diện không hợp lệ hoặc không tồn tại: {image!r}",
        path,
    )

    pdf_download = metadata.get("zo-pdf-download")
    pdf_branding = metadata.get("zo-pdf-branding")
    download_ok = isinstance(pdf_download, dict)
    branding_ok = isinstance(pdf_branding, dict)
    checker.add(
        "real-world-pdf-download-yaml",
        download_ok,
        "zo-pdf-download hợp lệ."
        if download_ok
        else "zo-pdf-download phải là mapping.",
        path,
    )
    checker.add(
        "real-world-pdf-branding-yaml",
        branding_ok,
        "zo-pdf-branding hợp lệ."
        if branding_ok
        else "zo-pdf-branding phải là mapping.",
        path,
    )

    label = pdf_download.get("label") if download_ok else None
    checker.add(
        "real-world-pdf-label",
        label == "Tải PDF",
        "Nhãn tải PDF đúng chuẩn."
        if label == "Tải PDF"
        else f"Kì vọng 'Tải PDF', nhận {label!r}.",
        path,
    )
    href = pdf_download.get("href") if download_ok else None
    expected_pdf = relative.with_suffix(".pdf").name
    href_ok = (
        isinstance(href, str)
        and not urlsplit(href).scheme
        and Path(href).name == href
        and href == expected_pdf
    )
    checker.add(
        "real-world-pdf-href",
        href_ok,
        f"href={href!r}."
        if href_ok
        else f"Kì vọng tên PDF cạnh bài là {expected_pdf!r}, nhận {href!r}.",
        path,
    )

    expected_url = rules.canonical_base + relative.with_suffix(".html").as_posix()
    canonical = pdf_branding.get("canonical-url") if branding_ok else None
    short_title = pdf_branding.get("short-title") if branding_ok else None
    display_url = pdf_branding.get("display-url") if branding_ok else None
    collection = pdf_branding.get("collection") if branding_ok else None
    checker.add(
        "real-world-canonical-url",
        canonical == expected_url,
        "canonical-url khớp đường dẫn bài."
        if canonical == expected_url
        else f"Kì vọng {expected_url!r}, nhận {canonical!r}.",
        path,
    )
    branding_values_ok = (
        _nonempty_string(short_title)
        and display_url == rules.display_url
        and collection == rules.collection
    )
    checker.add(
        "real-world-pdf-branding-values",
        branding_values_ok,
        "Các trường branding cốt lõi đúng chuẩn dự án."
        if branding_values_ok
        else "short-title phải có giá trị; display-url và collection phải đúng cấu hình.",
        path,
    )


def _profile_state(
    relative: Path,
    checker: CheckSink,
    config: ProjectConfigLike,
    rules: RealWorldRules,
) -> ProfileState | None:
    profile_relative = config.profile_path_for(relative)
    profile_path = checker.root / profile_relative
    if not profile_path.is_file():
        checker.add(
            "real-world-profile",
            False,
            f"Không tìm thấy hồ sơ {profile_relative.as_posix()}.",
            relative,
        )
        return None
    try:
        data = _load_yaml_unique(profile_path.read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        checker.add("real-world-profile", False, f"Không đọc được hồ sơ: {exc}", relative)
        return None
    if not isinstance(data, dict):
        checker.add("real-world-profile", False, "Hồ sơ phải là mapping YAML.", relative)
        return None

    errors: list[str] = []
    if data.get("phien_ban_ho_so") != rules.profile_version:
        errors.append(
            f"phien_ban_ho_so={data.get('phien_ban_ho_so')!r}, "
            f"cần {rules.profile_version}"
        )
    core = data.get("loi")
    extension = data.get("mo_rong")
    if not isinstance(core, dict):
        errors.append("thiếu mapping loi")
        core = {}
    if not isinstance(extension, dict):
        errors.append("thiếu mapping mo_rong")
        extension = {}
    real_world = extension.get("bai_toan_thuc_te")
    if not isinstance(real_world, dict):
        errors.append("thiếu mo_rong.bai_toan_thuc_te")
        real_world = {}

    expected_qmd = relative.relative_to(config.project_root).as_posix()
    if core.get("loai_bai") != "real_world_problem":
        errors.append("loi.loai_bai phải là real_world_problem")
    if core.get("tep_qmd") != expected_qmd:
        errors.append(f"loi.tep_qmd phải là {expected_qmd!r}")

    publication_config = config.raw.get("publication")
    production_states = (
        publication_config.get("production_states")
        if isinstance(publication_config, dict)
        else None
    )
    publication_states = (
        publication_config.get("publication_states")
        if isinstance(publication_config, dict)
        else None
    )
    production = core.get("trang_thai_san_xuat")
    publication = core.get("trang_thai_xuat_ban")
    confirmed = core.get("xac_nhan_xuat_ban_cua_nguoi_dung")
    if not isinstance(production_states, list) or production not in production_states:
        errors.append(f"trang_thai_san_xuat không hợp lệ: {production!r}")
    if not isinstance(publication_states, list) or publication not in publication_states:
        errors.append(f"trang_thai_xuat_ban không hợp lệ: {publication!r}")
    if not isinstance(confirmed, bool):
        errors.append("xac_nhan_xuat_ban_cua_nguoi_dung phải là boolean")
        confirmed = False
    if publication == "published" and confirmed is not True:
        errors.append("published đòi hỏi xác nhận xuất bản của người dùng")
    if publication == "pending" and confirmed is not False:
        errors.append("pending phải giữ xác nhận xuất bản là false")

    required_extension = {
        "boi_canh": _nonempty_string,
        "dai_luong": lambda value: isinstance(value, list) and bool(value),
        "gia_dinh": lambda value: isinstance(value, list) and bool(value),
        "mo_hinh": _nonempty_string,
        "kiem_tra_thuc_te": lambda value: isinstance(value, list) and bool(value),
    }
    for key, predicate in required_extension.items():
        if not predicate(real_world.get(key)):
            errors.append(f"mo_rong.bai_toan_thuc_te.{key} chưa hợp lệ")

    checker.add(
        "real-world-profile",
        not errors,
        (
            f"Hồ sơ phiên bản {rules.profile_version}; "
            f"production={production!r}; publication={publication!r}."
            if not errors
            else "; ".join(errors)
        ),
        relative,
    )
    if errors:
        return None
    return ProfileState(str(production), str(publication), bool(confirmed))


def _validate_sections(
    path: Path,
    headings: Sequence[tuple[int, int, str]],
    checker: CheckSink,
    rules: RealWorldRules,
) -> None:
    h2 = {_normalize_heading(title) for _, level, title in headings if level == 2}
    missing = [title for title in rules.required_sections if title.casefold() not in h2]
    checker.add(
        "real-world-required-sections",
        not missing,
        "Đủ các phần mô hình hóa bắt buộc."
        if not missing
        else "Thiếu H2: " + ", ".join(missing),
        path,
    )


def validate_real_world_problem_article(
    path: Path,
    text: str,
    checker: CheckSink,
    context: ValidationContextLike,
) -> None:
    """Validate one source QMD article from 100+ Bài toán thực tế."""

    relative = path.relative_to(checker.root)
    resolved = _config_for(relative, checker, context)
    if resolved is None:
        return
    config, rules = resolved

    document = validate_qmd_front_matter(
        path, text, checker, prefix="real-world"
    )
    if document is None:
        return
    validate_placeholders(
        path,
        text,
        checker,
        prefix="real-world",
        placeholders=config.placeholders,
    )
    required_metadata = (
        *config.core_required_metadata,
        *config.project_required_metadata,
    )
    validate_required_metadata(
        path,
        document.metadata,
        checker,
        prefix="real-world",
        required=required_metadata,
    )
    validate_required_body_classes(
        path,
        document.metadata,
        checker,
        prefix="real-world",
        required=config.required_body_classes,
    )
    checker.add(
        "qmd-core-validator",
        True,
        "Đã áp dụng validator lõi dùng chung cho real_world_problem.",
        path,
    )

    _validate_fixed_metadata(path, document.metadata, checker)
    _validate_project_metadata(
        path, relative, document.metadata, checker, rules
    )
    _profile_state(relative, checker, config, rules)

    active = strip_fences_comments_and_inline_code(document.body)
    headings = validate_headings(
        path,
        active,
        checker,
        prefix="real-world",
        max_depth=4,
        allow_h1=False,
    )
    _validate_sections(path, headings, checker, rules)
    validate_forbidden_paths(
        path, active, checker, prefix="real-world"
    )
    validate_images(path, active, checker, prefix="real-world")
    validate_executable_code(
        path, document.body, checker, prefix="real-world"
    )
    checker.add_warning(
        "real-world-human-review-required",
        "Kiểm định tự động không thay thế việc đọc dữ kiện, giả định, mô hình, "
        "đơn vị, phép tính, diễn giải và kiểm tra tính hợp lí trong bối cảnh.",
        path,
    )


def validate_rendered_real_world_problem_page(
    relative: Path,
    html: Path,
    checker: CheckSink,
    context: ValidationContextLike,
) -> None:
    """Validate the rendered HTML contract for a real-world article."""

    resolved = _config_for(relative, checker, context)
    if resolved is None:
        return
    config, rules = resolved
    source = checker.root / relative
    try:
        source_text = source.read_text(encoding="utf-8")
        html_text = html.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        checker.add("real-world-rendered-html-read", False, str(exc), relative)
        return
    metadata, _, error = split_qmd_front_matter(source_text)
    if error or metadata is None:
        checker.add(
            "real-world-rendered-html-metadata",
            False,
            error or "Không đọc được YAML.",
            relative,
        )
        return

    body_match = re.search(
        r"<body\b[^>]*class=[\"']([^\"']*)[\"']",
        html_text,
        flags=re.IGNORECASE,
    )
    body_classes = set(body_match.group(1).split()) if body_match else set()
    required = set(config.required_body_classes)
    missing = required - body_classes
    checker.add(
        "real-world-rendered-body-classes",
        not missing,
        "Thẻ body chứa các lớp trang bắt buộc."
        if not missing
        else "Thẻ body thiếu: " + ", ".join(sorted(missing)),
        relative,
    )

    h1_count = len(re.findall(r"<h1\b", html_text, flags=re.IGNORECASE))
    checker.add(
        "real-world-rendered-h1-count",
        h1_count <= 1,
        f"HTML có {h1_count} thẻ H1."
        if h1_count <= 1
        else f"HTML có {h1_count} thẻ H1; cần kiểm tra tiêu đề lặp.",
        relative,
    )

    pdf_download = metadata.get("zo-pdf-download")
    href = pdf_download.get("href") if isinstance(pdf_download, dict) else None
    if isinstance(href, str) and href:
        href_present = bool(
            re.search(
                rf"""href=[\"'][^\"']*{re.escape(Path(href).name)}(?:[?#][^\"']*)?[\"']""",
                html_text,
                flags=re.IGNORECASE,
            )
        )
        checker.add(
            "real-world-rendered-pdf-link",
            href_present,
            f"HTML có liên kết tới {Path(href).name}."
            if href_present
            else f"HTML không có liên kết tới {Path(href).name}.",
            relative,
        )
        state = _profile_state(relative, checker, config, rules)
        published_pdf = html.parent / Path(href).name
        if state is not None and state.publication == "published":
            checker.add(
                "real-world-rendered-pdf-resource",
                published_pdf.is_file(),
                f"Đầu ra published có {published_pdf.name}."
                if published_pdf.is_file()
                else f"Đầu ra published thiếu {published_pdf.name}.",
                relative,
            )
        elif published_pdf.is_file():
            checker.add_info(
                "real-world-rendered-pdf-resource",
                f"Đầu ra có {published_pdf.name}; trạng thái vẫn pending.",
                relative,
            )
        else:
            checker.add_info(
                "real-world-rendered-pdf-resource",
                f"Đầu ra chưa có {published_pdf.name}; trạng thái vẫn pending.",
                relative,
            )

    checker.add_warning(
        "real-world-rendered-visual-review",
        "Cần mở HTML ở desktop/mobile và PDF thật; kiểm tra tự động chỉ xác nhận cấu trúc có thể mã hóa.",
        relative,
    )


class _SelfTestChecker:
    def __init__(self, root: Path) -> None:
        self.root = root
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


class _SelfTestConfig:
    project_id = "real_world_100"
    project_root = Path("content/demo")
    profile_required = True
    core_required_metadata = (
        "title",
        "title-meta",
        "subtitle",
        "pagetitle",
        "summary",
        "description",
        "image",
        "abstract",
        "keywords",
        "author",
        "date",
        "date-format",
        "page-layout",
        "toc",
        "toc-title",
        "toc-location",
        "toc-depth",
        "body-classes",
        "zo-pdf-download",
        "zo-pdf-branding",
    )
    project_required_metadata: tuple[str, ...] = ()
    required_body_classes = ("zo-page-article", "zo-meta-hidden")
    placeholders = ("CHUA_XAC_DINH",)
    raw = {
        "publication": {
            "production_states": [
                "draft",
                "in_production",
                "validated",
                "accepted",
            ],
            "publication_states": ["pending", "published"],
        },
        "extensions": {
            "real_world_problem": {
                "required_sections": [
                    "Bối cảnh và dữ kiện",
                    "Mô hình hóa",
                    "Giải quyết",
                    "Kiểm tra và diễn giải",
                ],
                "forbidden_metadata": ["listing-order"],
                "collection": "100+ Bài toán thực tế",
                "canonical_base": "https://zomath.vn/",
                "display_url": "zomath.vn",
                "profile_version": 1,
            }
        },
    }

    def profile_path_for(self, repository_relative: Path) -> Path:
        return self.project_root / "_quy_trinh/ho_so" / f"{repository_relative.stem}.yml"


class _SelfTestContext:
    config = _SelfTestConfig()
    article_type = "real_world_problem"


def _self_test() -> None:
    if yaml is None:
        raise RuntimeError("Thiếu dependency PyYAML.")
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        article = root / "content/demo/core/demo.qmd"
        profile = root / "content/demo/_quy_trinh/ho_so/demo.yml"
        image = root / "content/demo/assets/img/demo.svg"
        article.parent.mkdir(parents=True)
        profile.parent.mkdir(parents=True)
        image.parent.mkdir(parents=True)
        image.write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><path d="M0 0h10v10H0z"/></svg>\n',
            encoding="utf-8",
        )
        source = """---
title: Demo
title-meta: Demo
subtitle: Mô hình thử
pagetitle: Demo
summary: Bài thử.
description: Bài thử.
image: /content/demo/assets/img/demo.svg
abstract: Bài thử.
keywords: [mô hình hóa]
author: ZO Math
date: last-modified
date-format: DD-MM-YYYY
page-layout: article
toc: true
toc-title: Nội dung
toc-location: right
toc-depth: 3
body-classes: zo-page-article zo-meta-hidden
zo-pdf-download:
  label: Tải PDF
  href: demo.pdf
zo-pdf-branding:
  short-title: Demo
  display-url: zomath.vn
  collection: 100+ Bài toán thực tế
  canonical-url: https://zomath.vn/content/demo/core/demo.html
---
## Bối cảnh và dữ kiện

Dữ kiện.

## Mô hình hóa

Mô hình.

## Giải quyết

Kết quả.

## Kiểm tra và diễn giải

Kiểm tra.
"""
        article.write_text(source, encoding="utf-8")
        profile.write_text(
            """phien_ban_ho_so: 1
loi:
  loai_bai: real_world_problem
  tep_qmd: core/demo.qmd
  trang_thai_san_xuat: in_production
  trang_thai_xuat_ban: pending
  xac_nhan_xuat_ban_cua_nguoi_dung: false
mo_rong:
  bai_toan_thuc_te:
    boi_canh: Bài thử
    dai_luong: [x]
    gia_dinh: [Giả định]
    mo_hinh: Hàm số
    kiem_tra_thuc_te: [Kiểm tra]
""",
            encoding="utf-8",
        )
        checker = _SelfTestChecker(root)
        validate_real_world_problem_article(
            article,
            source,
            checker,
            _SelfTestContext(),
        )
        assert not any(status == "fail" for _, status in checker.records)
        assert ("qmd-core-validator", "pass") in checker.records
        assert ("real-world-required-sections", "pass") in checker.records
        assert ("real-world-profile", "pass") in checker.records


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("command", choices=("self-test",))
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if yaml is None:
        print("ERROR: Thiếu dependency PyYAML.")
        return EXIT_MISSING_TOOL
    try:
        if args.command == "self-test":
            _self_test()
            print("PASS: zo_real_world_problem self-test")
        return EXIT_OK
    except (AssertionError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return EXIT_INVALID


if __name__ == "__main__":
    raise SystemExit(main())

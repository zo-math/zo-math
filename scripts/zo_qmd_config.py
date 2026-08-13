"""Load and validate project-local QMD production configuration.

This module is intentionally independent from ``zo_check_repo.py`` so it can be
introduced without changing the checker's current behavior.  A later migration
step will use it for project discovery and validator selection.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from zo_qmd_registry import REGISTERED_MODULES

try:
    import yaml
except ImportError:  # Reported by the CLI with a stable exit code.
    yaml = None


CONFIG_RELATIVE_PATH = Path("_quy_trinh/cau_hinh_san_xuat_qmd.yml")
SUPPORTED_SCHEMA_VERSIONS = {1}

EXIT_OK = 0
EXIT_INVALID = 1
EXIT_USAGE = 2
EXIT_MISSING_TOOL = 3


class ProjectConfigError(ValueError):
    """Raised when a project configuration is missing or invalid."""


@dataclass(frozen=True)
class ArticleTypeConfig:
    """Declarative rules used to identify one article type."""

    id: str
    include: tuple[str, ...]
    exclude: tuple[str, ...]

    def matches(self, relative_to_project: Path) -> bool:
        value = relative_to_project.as_posix()
        included = any(fnmatch.fnmatchcase(value, pattern) for pattern in self.include)
        excluded = any(fnmatch.fnmatchcase(value, pattern) for pattern in self.exclude)
        return included and not excluded


@dataclass(frozen=True)
class ProjectConfig:
    """Validated, immutable view of one project configuration."""

    schema_version: int
    config_path: Path
    project_id: str
    project_name: str
    project_root: Path
    article_types: tuple[ArticleTypeConfig, ...]
    profile_directory: Path
    profile_naming: str
    profile_required: bool
    required_modules: tuple[str, ...]
    optional_modules: tuple[str, ...]
    core_required_metadata: tuple[str, ...]
    project_required_metadata: tuple[str, ...]
    required_body_classes: tuple[str, ...]
    placeholders: tuple[str, ...]
    raw: Mapping[str, Any]

    def article_type_for(self, repository_relative: Path) -> ArticleTypeConfig | None:
        """Return the unique matching article type, or raise on overlap."""

        try:
            relative = repository_relative.relative_to(self.project_root)
        except ValueError:
            return None

        matches = [item for item in self.article_types if item.matches(relative)]
        if len(matches) > 1:
            names = ", ".join(item.id for item in matches)
            raise ProjectConfigError(
                f"Đường dẫn {repository_relative.as_posix()!r} khớp nhiều loại bài: {names}."
            )
        return matches[0] if matches else None

    def profile_path_for(self, repository_relative: Path) -> Path:
        """Resolve the profile path for a registered article."""

        article_type = self.article_type_for(repository_relative)
        if article_type is None:
            raise ProjectConfigError(
                f"Đường dẫn {repository_relative.as_posix()!r} không thuộc loại bài nào."
            )
        if self.profile_naming != "by_article_stem":
            raise ProjectConfigError(
                f"Quy tắc đặt tên hồ sơ chưa được hỗ trợ: {self.profile_naming!r}."
            )
        return self.project_root / self.profile_directory / f"{repository_relative.stem}.yml"


def _load_yaml_unique(text: str) -> Any:
    if yaml is None:
        raise ProjectConfigError("Thiếu dependency PyYAML.")

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


def _mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise ProjectConfigError(f"{label} phải là mapping có khóa chuỗi.")
    return value


def _known_keys(
    value: Mapping[str, Any], label: str, allowed: set[str], required: set[str] | None = None
) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise ProjectConfigError(f"{label} có khóa không hỗ trợ: {', '.join(unknown)}.")
    missing = sorted((required or set()) - set(value))
    if missing:
        raise ProjectConfigError(f"{label} thiếu khóa bắt buộc: {', '.join(missing)}.")


def _nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ProjectConfigError(f"{label} phải là chuỗi không rỗng.")
    return value.strip()


def _string_list(value: Any, label: str, *, nonempty: bool = False) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise ProjectConfigError(f"{label} phải là danh sách chuỗi không rỗng.")
    result = tuple(item.strip() for item in value)
    if nonempty and not result:
        raise ProjectConfigError(f"{label} không được rỗng.")
    duplicates = sorted({item for item in result if result.count(item) > 1})
    if duplicates:
        raise ProjectConfigError(f"{label} có giá trị trùng: {', '.join(duplicates)}.")
    return result


def _bool(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        raise ProjectConfigError(f"{label} phải là boolean.")
    return value


def _relative_path(value: Any, label: str) -> Path:
    text = _nonempty_string(value, label).replace("\\", "/")
    path = Path(text)
    if path.is_absolute() or ".." in path.parts:
        raise ProjectConfigError(f"{label} phải là đường dẫn tương đối không chứa '..'.")
    return path


def _inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _read_config(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise ProjectConfigError(f"Không đọc được cấu hình {path}: {exc}") from exc
    try:
        value = _load_yaml_unique(text)
    except ProjectConfigError:
        raise
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        where = f"dòng {mark.line + 1}, cột {mark.column + 1}: " if mark else ""
        raise ProjectConfigError(f"YAML cấu hình không hợp lệ: {where}{str(exc).splitlines()[0]}") from exc
    return _mapping(value, "cấu hình gốc")


def load_project_config(repository_root: Path, config_path: Path) -> ProjectConfig:
    """Load and validate one project-local configuration."""

    root = repository_root.resolve()
    path = (config_path if config_path.is_absolute() else root / config_path).resolve()
    if not _inside(path, root):
        raise ProjectConfigError("Tệp cấu hình nằm ngoài repository.")
    if not path.is_file():
        raise ProjectConfigError(f"Không tìm thấy tệp cấu hình: {path}.")

    data = _read_config(path)
    top_allowed = {
        "schema_version",
        "project",
        "discovery",
        "profiles",
        "modules",
        "metadata",
        "publication",
        "catalog",
        "references",
        "regression",
        "extensions",
        "authority_registry",
    }
    top_required = {
        "schema_version",
        "project",
        "discovery",
        "profiles",
        "modules",
        "metadata",
        "publication",
        "references",
        "regression",
        "extensions",
    }
    _known_keys(data, "cấu hình gốc", top_allowed, top_required)

    schema_version = data["schema_version"]
    if not isinstance(schema_version, int) or schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        supported = ", ".join(map(str, sorted(SUPPORTED_SCHEMA_VERSIONS)))
        raise ProjectConfigError(
            f"schema_version={schema_version!r} không được hỗ trợ; hỗ trợ: {supported}."
        )

    project = _mapping(data["project"], "project")
    _known_keys(project, "project", {"id", "name", "root"}, {"id", "name", "root"})
    project_id = _nonempty_string(project["id"], "project.id")
    project_name = _nonempty_string(project["name"], "project.name")
    project_root = _relative_path(project["root"], "project.root")
    project_root_absolute = (root / project_root).resolve()
    if not _inside(project_root_absolute, root):
        raise ProjectConfigError("project.root đi ra ngoài repository.")
    expected_config = project_root_absolute / CONFIG_RELATIVE_PATH
    if path != expected_config:
        raise ProjectConfigError(
            "Vị trí cấu hình không khớp project.root; "
            f"kì vọng {expected_config.relative_to(root).as_posix()}."
        )

    discovery = _mapping(data["discovery"], "discovery")
    _known_keys(discovery, "discovery", {"article_types"}, {"article_types"})
    raw_types = discovery["article_types"]
    if not isinstance(raw_types, list) or not raw_types:
        raise ProjectConfigError("discovery.article_types phải là danh sách không rỗng.")

    article_types: list[ArticleTypeConfig] = []
    type_ids: set[str] = set()
    for index, raw_item in enumerate(raw_types):
        label = f"discovery.article_types[{index}]"
        item = _mapping(raw_item, label)
        _known_keys(item, label, {"id", "include", "exclude"}, {"id", "include", "exclude"})
        type_id = _nonempty_string(item["id"], f"{label}.id")
        if type_id in type_ids:
            raise ProjectConfigError(f"Trùng loại bài: {type_id!r}.")
        type_ids.add(type_id)
        include = _string_list(item["include"], f"{label}.include", nonempty=True)
        exclude = _string_list(item["exclude"], f"{label}.exclude")
        article_types.append(ArticleTypeConfig(type_id, include, exclude))

    profiles = _mapping(data["profiles"], "profiles")
    _known_keys(
        profiles,
        "profiles",
        {"directory", "naming", "required"},
        {"directory", "naming", "required"},
    )
    profile_directory = _relative_path(profiles["directory"], "profiles.directory")
    profile_naming = _nonempty_string(profiles["naming"], "profiles.naming")
    if profile_naming != "by_article_stem":
        raise ProjectConfigError("Phiên bản 1 chỉ hỗ trợ profiles.naming='by_article_stem'.")
    profile_required = _bool(profiles["required"], "profiles.required")

    modules = _mapping(data["modules"], "modules")
    _known_keys(modules, "modules", {"required", "optional"}, {"required", "optional"})
    required_modules = _string_list(modules["required"], "modules.required", nonempty=True)
    optional_modules = _string_list(modules["optional"], "modules.optional")
    overlap = sorted(set(required_modules) & set(optional_modules))
    if overlap:
        raise ProjectConfigError(
            "Mô-đun không được vừa required vừa optional: " + ", ".join(overlap) + "."
        )
    unknown_modules = sorted(
        (set(required_modules) | set(optional_modules)) - REGISTERED_MODULES
    )
    if unknown_modules:
        raise ProjectConfigError(
            "Mô-đun chưa đăng kí: " + ", ".join(unknown_modules) + "."
        )
    if "qmd-core" not in required_modules:
        raise ProjectConfigError("modules.required phải chứa 'qmd-core'.")

    metadata = _mapping(data["metadata"], "metadata")
    _known_keys(
        metadata,
        "metadata",
        {
            "core_required",
            "project_required",
            "body_classes_required",
            "placeholders",
        },
        {
            "core_required",
            "project_required",
            "body_classes_required",
            "placeholders",
        },
    )
    core_required_metadata = _string_list(
        metadata["core_required"], "metadata.core_required"
    )
    project_required_metadata = _string_list(
        metadata["project_required"], "metadata.project_required"
    )
    required_body_classes = _string_list(
        metadata["body_classes_required"], "metadata.body_classes_required"
    )
    placeholders = _string_list(
        metadata["placeholders"], "metadata.placeholders"
    )

    publication = _mapping(data["publication"], "publication")
    _known_keys(
        publication,
        "publication",
        {
            "production_states",
            "publication_states",
            "user_confirmation_required",
        },
        {
            "production_states",
            "publication_states",
            "user_confirmation_required",
        },
    )
    production_states = _string_list(
        publication["production_states"], "publication.production_states", nonempty=True
    )
    publication_states = _string_list(
        publication["publication_states"], "publication.publication_states", nonempty=True
    )
    if production_states != ("draft", "in_production", "validated", "accepted"):
        raise ProjectConfigError(
            "publication.production_states phải giữ thứ tự "
            "draft, in_production, validated, accepted."
        )
    if publication_states != ("pending", "published"):
        raise ProjectConfigError(
            "publication.publication_states phải là pending, published."
        )
    if _bool(
        publication["user_confirmation_required"],
        "publication.user_confirmation_required",
    ) is not True:
        raise ProjectConfigError(
            "publication.user_confirmation_required bắt buộc phải là true."
        )

    references = _mapping(data["references"], "references")
    _known_keys(
        references,
        "references",
        {
            "controlling_documents",
            "templates",
            "theory_sources",
            "quality_exemplars",
        },
        {"controlling_documents", "templates", "theory_sources"},
    )
    for key in ("controlling_documents", "templates", "theory_sources"):
        _string_list(references[key], f"references.{key}")
    references.setdefault("quality_exemplars", [])
    quality_exemplars = _string_list(
        references["quality_exemplars"],
        "references.quality_exemplars",
    )
    for item in quality_exemplars:
        exemplar = _relative_path(item, "references.quality_exemplars[]")
        absolute = (project_root_absolute / exemplar).resolve()
        if not _inside(absolute, project_root_absolute):
            raise ProjectConfigError(
                "references.quality_exemplars chứa đường dẫn ngoài dự án."
            )

    if "authority_registry" in data and data["authority_registry"] is not None:
        authority_registry = _mapping(
            data["authority_registry"], "authority_registry"
        )
        _known_keys(
            authority_registry,
            "authority_registry",
            {
                "schema_version",
                "governing_required",
                "conditional_required",
                "provenance_required",
                "reference_only",
            },
            {
                "schema_version",
                "governing_required",
                "conditional_required",
                "provenance_required",
                "reference_only",
            },
        )

        authority_schema_version = authority_registry["schema_version"]
        if authority_schema_version != 1:
            raise ProjectConfigError(
                "authority_registry.schema_version hiện chỉ hỗ trợ giá trị 1."
            )

        seen_authority_paths: set[str] = set()
        seen_conditional_ids: set[str] = set()

        for role in (
            "governing_required",
            "conditional_required",
            "provenance_required",
            "reference_only",
        ):
            items = authority_registry[role]
            if not isinstance(items, list):
                raise ProjectConfigError(
                    f"authority_registry.{role} phải là danh sách."
                )

            for index, raw_item in enumerate(items):
                label = f"authority_registry.{role}[{index}]"
                item = _mapping(raw_item, label)

                if role == "conditional_required":
                    allowed = {"id", "when", "path", "reason"}
                    required = allowed
                else:
                    allowed = {"path", "reason"}
                    required = allowed

                _known_keys(item, label, allowed, required)

                authority_path = _relative_path(
                    item["path"], f"{label}.path"
                ).as_posix()
                _nonempty_string(item["reason"], f"{label}.reason")

                if authority_path in seen_authority_paths:
                    raise ProjectConfigError(
                        "authority_registry không được khai cùng một path "
                        f"ở nhiều vai trò: {authority_path!r}."
                    )
                seen_authority_paths.add(authority_path)

                if role == "conditional_required":
                    condition_id = _nonempty_string(
                        item["id"], f"{label}.id"
                    )
                    _nonempty_string(item["when"], f"{label}.when")
                    if condition_id in seen_conditional_ids:
                        raise ProjectConfigError(
                            "authority_registry.conditional_required có id trùng: "
                            f"{condition_id!r}."
                        )
                    seen_conditional_ids.add(condition_id)

    regression = _mapping(data["regression"], "regression")
    _known_keys(
        regression,
        "regression",
        {"articles", "expected_checker_version", "preserve_cli"},
        {"articles", "expected_checker_version", "preserve_cli"},
    )
    regression_articles = _string_list(regression["articles"], "regression.articles")
    for item in regression_articles:
        article = _relative_path(item, "regression.articles[]")
        absolute = (project_root_absolute / article).resolve()
        if not _inside(absolute, project_root_absolute):
            raise ProjectConfigError("regression.articles chứa đường dẫn ngoài dự án.")
    version = regression["expected_checker_version"]
    if version is not None and (not isinstance(version, str) or not version.strip()):
        raise ProjectConfigError(
            "regression.expected_checker_version phải là chuỗi hoặc null."
        )
    _bool(regression["preserve_cli"], "regression.preserve_cli")

    extensions = data["extensions"]
    _mapping(extensions, "extensions")

    if "catalog" in data and data["catalog"] is not None:
        catalog = _mapping(data["catalog"], "catalog")
        _known_keys(
            catalog,
            "catalog",
            {
                "module",
                "data",
                "key",
                "status_field",
                "href_field",
            },
            {
                "module",
                "data",
                "key",
                "status_field",
                "href_field",
            },
        )
        catalog_module = _nonempty_string(catalog["module"], "catalog.module")
        if catalog_module not in REGISTERED_MODULES:
            raise ProjectConfigError(
                f"catalog.module chưa đăng kí: {catalog_module!r}."
            )
        if catalog_module not in set(required_modules) | set(optional_modules):
            raise ProjectConfigError(
                "catalog.module phải xuất hiện trong modules.required hoặc modules.optional."
            )
        _relative_path(catalog["data"], "catalog.data")
        key = _mapping(catalog["key"], "catalog.key")
        _known_keys(
            key,
            "catalog.key",
            {"article_metadata", "item_field"},
            {"article_metadata", "item_field"},
        )
        _nonempty_string(key["article_metadata"], "catalog.key.article_metadata")
        _nonempty_string(key["item_field"], "catalog.key.item_field")
        _nonempty_string(catalog["status_field"], "catalog.status_field")
        _nonempty_string(catalog["href_field"], "catalog.href_field")

    return ProjectConfig(
        schema_version=schema_version,
        config_path=path.relative_to(root),
        project_id=project_id,
        project_name=project_name,
        project_root=project_root,
        article_types=tuple(article_types),
        profile_directory=profile_directory,
        profile_naming=profile_naming,
        profile_required=profile_required,
        required_modules=required_modules,
        optional_modules=optional_modules,
        core_required_metadata=core_required_metadata,
        project_required_metadata=project_required_metadata,
        required_body_classes=required_body_classes,
        placeholders=placeholders,
        raw=data,
    )


def discover_project_config(
    repository_root: Path, article_path: Path
) -> ProjectConfig | None:
    """Find the nearest project configuration governing an article path."""

    root = repository_root.resolve()
    article = (
        article_path if article_path.is_absolute() else root / article_path
    ).resolve()
    if not _inside(article, root):
        raise ProjectConfigError("Đường dẫn bài nằm ngoài repository.")

    current = article.parent if article.suffix else article
    while _inside(current, root):
        candidate = current / CONFIG_RELATIVE_PATH
        if candidate.is_file():
            return load_project_config(root, candidate)
        if current == root:
            break
        current = current.parent
    return None


def _summary(config: ProjectConfig, article: Path | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "schema_version": config.schema_version,
        "config_path": config.config_path.as_posix(),
        "project_id": config.project_id,
        "project_name": config.project_name,
        "project_root": config.project_root.as_posix(),
        "article_types": [item.id for item in config.article_types],
        "required_modules": list(config.required_modules),
        "optional_modules": list(config.optional_modules),
        "core_required_metadata": list(config.core_required_metadata),
        "project_required_metadata": list(config.project_required_metadata),
        "required_body_classes": list(config.required_body_classes),
        "placeholder_count": len(config.placeholders),
        "compatibility_mode": "native",
    }
    if article is not None:
        article_type = config.article_type_for(article)
        payload["article"] = article.as_posix()
        payload["article_type"] = article_type.id if article_type else None
        if article_type is not None:
            payload["profile"] = config.profile_path_for(article).as_posix()
    return payload


def _self_test() -> None:
    if yaml is None:
        raise ProjectConfigError("Thiếu dependency PyYAML.")

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary).resolve()
        project = root / "content/demo"
        config_path = project / CONFIG_RELATIVE_PATH
        article = project / "core/demo.qmd"
        config_path.parent.mkdir(parents=True)
        article.parent.mkdir(parents=True)
        article.write_text("---\ntitle: Demo\n---\n", encoding="utf-8")
        config_path.write_text(
            """schema_version: 1
project:
  id: demo
  name: Demo
  root: content/demo
discovery:
  article_types:
    - id: demo_article
      include:
        - core/*.qmd
      exclude: []
profiles:
  directory: _quy_trinh/ho_so
  naming: by_article_stem
  required: true
modules:
  required:
    - qmd-core
  optional: []
metadata:
  core_required: []
  project_required: []
  body_classes_required: []
  placeholders: []
publication:
  production_states:
    - draft
    - in_production
    - validated
    - accepted
  publication_states:
    - pending
    - published
  user_confirmation_required: true
references:
  controlling_documents: []
  templates: []
  theory_sources: []
regression:
  articles:
    - core/demo.qmd
  expected_checker_version: null
  preserve_cli: true
extensions: {}
""",
            encoding="utf-8",
        )

        loaded = load_project_config(root, config_path)
        assert loaded.project_id == "demo"
        assert loaded.core_required_metadata == ()
        assert loaded.project_required_metadata == ()
        assert loaded.required_body_classes == ()
        assert loaded.placeholders == ()
        assert loaded.raw["references"]["quality_exemplars"] == []
        assert loaded.article_type_for(Path("content/demo/core/demo.qmd")).id == "demo_article"
        assert loaded.profile_path_for(
            Path("content/demo/core/demo.qmd")
        ) == Path("content/demo/_quy_trinh/ho_so/demo.yml")
        discovered = discover_project_config(root, article)
        assert discovered is not None and discovered.project_id == "demo"

        duplicate = config_path.read_text(encoding="utf-8") + "\nschema_version: 1\n"
        config_path.write_text(duplicate, encoding="utf-8")
        try:
            load_project_config(root, config_path)
        except ProjectConfigError:
            pass
        else:
            raise AssertionError("Cấu hình có khóa trùng phải bị từ chối.")

        normalized = duplicate.rsplit("\nschema_version: 1\n", 1)[0]
        normalized = normalized.replace(
            "  theory_sources: []\n",
            "  theory_sources: []\n"
            "  quality_exemplars:\n"
            "    - depth/demo.qmd\n"
            "    - depth/demo.pdf\n",
        )
        config_path.write_text(normalized, encoding="utf-8")
        loaded = load_project_config(root, config_path)
        assert loaded.raw["references"]["quality_exemplars"] == [
            "depth/demo.qmd",
            "depth/demo.pdf",
        ]

        unsafe = normalized.replace("    - depth/demo.qmd\n", "    - ../escape.qmd\n")
        config_path.write_text(unsafe, encoding="utf-8")
        try:
            load_project_config(root, config_path)
        except ProjectConfigError:
            pass
        else:
            raise AssertionError("Quality exemplar ngoài dự án phải bị từ chối.")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument(
        "--repo-root",
        default=".",
        help="Gốc repository; mặc định là thư mục hiện tại.",
    )
    subparsers = result.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser("check", help="Nạp và kiểm tra một tệp cấu hình.")
    check.add_argument("config")

    inspect = subparsers.add_parser(
        "inspect", help="Khám phá cấu hình và loại bài cho một đường dẫn."
    )
    inspect.add_argument("article")

    subparsers.add_parser("self-test", help="Chạy kiểm tra nội bộ độc lập.")
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if yaml is None:
        print("ERROR: Thiếu dependency PyYAML.")
        return EXIT_MISSING_TOOL

    root = Path(args.repo_root).resolve()
    try:
        if args.command == "self-test":
            _self_test()
            print("PASS: zo_qmd_config self-test")
            return EXIT_OK

        if args.command == "check":
            config = load_project_config(root, Path(args.config))
            print(json.dumps(_summary(config), ensure_ascii=False, indent=2))
            return EXIT_OK

        article = Path(args.article)
        config = discover_project_config(root, article)
        if config is None:
            raise ProjectConfigError(
                f"Không tìm thấy {CONFIG_RELATIVE_PATH.as_posix()} cho {article}."
            )
        repository_relative = (
            article if not article.is_absolute() else article.resolve().relative_to(root)
        )
        print(
            json.dumps(
                _summary(config, repository_relative),
                ensure_ascii=False,
                indent=2,
            )
        )
        return EXIT_OK
    except ProjectConfigError as exc:
        print(f"ERROR: {exc}")
        return EXIT_INVALID


if __name__ == "__main__":
    raise SystemExit(main())

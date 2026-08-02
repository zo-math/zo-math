"""Create and verify standard ZO Math QMD context packages.

A standard package contains PROMPT.md, MANIFEST.yml, FILES.sha256, and payload/.
The payload preserves repository-relative paths. This module is an operations
component; it does not validate QMD content, accept work, publish, stage, or
commit repository changes.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping, Sequence

import yaml

from zo_check_repo import CHECKER_VERSION
from zo_qmd_config import ProjectConfigError, discover_project_config


PACKAGE_MODULE_VERSION = "0.2.0"
MANIFEST_VERSION = 1
OPERATIONS_CONTRACT_VERSION = "0.2"
QMD_CORE_VERSION = "1.0"
PROJECT_CONFIG_SCHEMA = 1

EXIT_OK = 0
EXIT_FAILED = 1
EXIT_USAGE = 2
EXIT_MISSING_TOOL = 3

TOP_LEVEL_REQUIRED = ("PROMPT.md", "MANIFEST.yml", "FILES.sha256", "payload")
CHECKSUM_FILE = "FILES.sha256"
HASH_ALGORITHM = "sha256"

CORE_DOCUMENTS = (
    Path("AGENTS.md"),
    Path("quy_trinh_xay_dung/he_thong_san_xuat_qmd/README.md"),
    Path(
        "quy_trinh_xay_dung/he_thong_san_xuat_qmd/"
        "kien_truc_van_hanh_co_may_qmd.md"
    ),
    Path(
        "quy_trinh_xay_dung/he_thong_san_xuat_qmd/"
        "giao_thuc_agent_chat_box_va_goi_ngu_canh.md"
    ),
    Path(
        "quy_trinh_xay_dung/he_thong_san_xuat_qmd/"
        "tieu_chi_nghiem_thu_lop_van_hanh.md"
    ),
    Path(
        "quy_trinh_xay_dung/he_thong_san_xuat_qmd/"
        "mau_manifest_goi_qmd.yml"
    ),
)

RUNTIME_ENTRYPOINTS = (
    Path("scripts/zo_python.py"),
    Path("scripts/zo_qmd.py"),
    Path("scripts/zo_qmd_package.py"),
)

EXCLUDED_DIR_NAMES = {
    ".git",
    ".quarto",
    ".continue",
    "__pycache__",
    "_freeze",
    "docs",
    "node_modules",
    ".venv",
    "venv",
}
HARD_EXCLUDED_DIR_NAMES = EXCLUDED_DIR_NAMES - {"docs"}

FORBIDDEN_FILE_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "id_rsa",
    "id_dsa",
    "id_ed25519",
    "credentials.json",
    "service-account.json",
    ".netrc",
    ".npmrc",
    ".pypirc",
}

FORBIDDEN_SUFFIXES = {
    ".key",
    ".pem",
    ".p12",
    ".pfx",
    ".pyc",
}

AGENT_PATH_PATTERN = re.compile(
    r"`([^`\n]+?\.(?:md|qmd|ya?ml|py))`",
    flags=re.IGNORECASE,
)
CHECKSUM_LINE_PATTERN = re.compile(
    r"^([0-9a-f]{64})  ([^\r\n]+)$"
)
FULL_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
MAX_ZIP_FILES = 100_000
MAX_ZIP_UNCOMPRESSED_BYTES = 2 * 1024 * 1024 * 1024


@dataclass(frozen=True)
class PackageSource:
    path: Path
    role: str
    condition: str | None = None


class PackageError(RuntimeError):
    """Raised when a package cannot be created or verified safely."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _run(
    command: Sequence[str],
    cwd: Path,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(command),
        cwd=cwd,
        check=False,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        env=os.environ.copy(),
    )


def _git_value(root: Path, *args: str) -> str | None:
    git = shutil.which("git")
    if git is None:
        return None
    result = _run([git, *args], root)
    if result.returncode != 0:
        return None
    value = result.stdout.strip()
    return value or None


def _repository_state(root: Path) -> dict[str, Any]:
    branch = _git_value(root, "branch", "--show-current")
    commit = _git_value(root, "rev-parse", "HEAD")

    return {
        "name": root.name,
        "source": "exported_snapshot",
        "branch": branch or "detached",
        "commit": commit if commit and FULL_SHA_PATTERN.fullmatch(commit) else "unknown",
        "dirty": "unknown",
        "ahead_of_origin": "unknown",
    }


def _safe_relative_path(raw: str) -> PurePosixPath:
    value = raw.replace("\\", "/")
    if "\x00" in value or ":" in value:
        raise PackageError(
            f"Đường dẫn không an toàn hoặc không tương thích đa nền tảng: {raw!r}."
        )

    path = PurePosixPath(value)
    if not value or path.is_absolute() or ".." in path.parts:
        raise PackageError(f"Đường dẫn không an toàn trong gói: {raw!r}.")
    if path.as_posix() != value:
        raise PackageError(f"Đường dẫn không chuẩn hóa trong gói: {raw!r}.")
    return path


def _relative_to_root(root: Path, raw: str | Path) -> Path:
    candidate = Path(raw).expanduser()
    resolved = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    try:
        relative = resolved.relative_to(root)
    except ValueError as exc:
        raise PackageError(f"Đường dẫn nằm ngoài repository: {raw}") from exc
    if relative == Path("."):
        return Path()
    return relative


def _is_inside(root: Path, candidate: Path) -> bool:
    try:
        candidate.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _is_forbidden_file(path: Path) -> bool:
    name = path.name.lower()
    return (
        name in FORBIDDEN_FILE_NAMES
        or name.startswith(".env.")
        or path.suffix.lower() in FORBIDDEN_SUFFIXES
    )


def _directory_is_excluded(path: Path) -> bool:
    parts = tuple(part.casefold() for part in path.parts)
    return bool(parts) and (
        parts[0] == "docs"
        or any(part in HARD_EXCLUDED_DIR_NAMES for part in parts)
    )


def _path_is_hard_excluded(path: Path) -> bool:
    return any(
        part.casefold() in HARD_EXCLUDED_DIR_NAMES
        for part in path.parts
    )


def _iter_directory_files(root: Path, relative: Path) -> Iterable[Path]:
    base = root / relative
    for current, dirs, files in os.walk(base, followlinks=False):
        current_path = Path(current)
        current_relative = current_path.relative_to(root)

        kept_dirs: list[str] = []
        for name in sorted(dirs):
            candidate = current_path / name
            rel = candidate.relative_to(root)
            if candidate.is_symlink():
                raise PackageError(f"Không đóng gói symlink: {rel.as_posix()}.")
            if (
                name.casefold() in HARD_EXCLUDED_DIR_NAMES
                or _directory_is_excluded(rel)
            ):
                continue
            kept_dirs.append(name)
        dirs[:] = kept_dirs

        for name in sorted(files):
            candidate = current_path / name
            rel = candidate.relative_to(root)
            if candidate.is_symlink():
                raise PackageError(f"Không đóng gói symlink: {rel.as_posix()}.")
            if _directory_is_excluded(rel):
                continue
            if _is_forbidden_file(candidate):
                raise PackageError(
                    f"Tệp có khả năng chứa bí mật hoặc dữ liệu máy cá nhân: "
                    f"{rel.as_posix()}."
                )
            if candidate.is_file():
                yield rel


def _expand_repository_path(root: Path, relative: Path) -> list[Path]:
    if _path_is_hard_excluded(relative):
        raise PackageError(
            "Không đóng gói đường dẫn hệ thống, cache hoặc dữ liệu máy cá nhân: "
            f"{relative.as_posix()}."
        )
    target = root / relative
    if not target.exists():
        raise PackageError(f"Không tồn tại: {relative.as_posix()}.")
    if target.is_symlink():
        raise PackageError(f"Không đóng gói symlink: {relative.as_posix()}.")
    if target.is_file():
        if _is_forbidden_file(target):
            raise PackageError(
                f"Tệp có khả năng chứa bí mật hoặc dữ liệu máy cá nhân: "
                f"{relative.as_posix()}."
            )
        return [relative]
    if target.is_dir():
        return list(_iter_directory_files(root, relative))
    raise PackageError(f"Không hỗ trợ loại đường dẫn: {relative.as_posix()}.")


def _python_local_imports(path: Path) -> set[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError) as exc:
        raise PackageError(f"Không phân tích được import của {path}: {exc}") from exc

    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.add(alias.name.split(".", 1)[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module.split(".", 1)[0])
    return {name for name in modules if name.startswith("zo_")}


def _runtime_dependency_closure(root: Path) -> set[Path]:
    scripts_dir = root / "scripts"
    pending = list(RUNTIME_ENTRYPOINTS)
    resolved: set[Path] = set()

    while pending:
        relative = pending.pop()
        if relative in resolved:
            continue
        absolute = root / relative
        if not absolute.is_file():
            raise PackageError(
                f"Thiếu runtime dependency bắt buộc: {relative.as_posix()}."
            )
        resolved.add(relative)
        if absolute.suffix.lower() != ".py":
            continue
        for module in sorted(_python_local_imports(absolute)):
            candidate = Path("scripts") / f"{module}.py"
            if (root / candidate).is_file() and candidate not in resolved:
                pending.append(candidate)

    init_file = Path("scripts/__init__.py")
    if (root / init_file).is_file():
        resolved.add(init_file)
    return resolved


def _agent_chain(root: Path, relative: Path) -> list[Path]:
    target = root / relative
    start = target if target.is_dir() else target.parent
    try:
        start_relative = start.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise PackageError(f"Đường dẫn nằm ngoài repository: {relative}") from exc

    chain: list[Path] = []
    current = Path()
    root_agents = Path("AGENTS.md")
    if (root / root_agents).is_file():
        chain.append(root_agents)

    for part in start_relative.parts:
        current /= part
        candidate = current / "AGENTS.md"
        if candidate != root_agents and (root / candidate).is_file():
            chain.append(candidate)
    return chain


def _agent_references(root: Path, agents_path: Path) -> set[Path]:
    absolute = root / agents_path
    if not absolute.is_file():
        return set()
    text = absolute.read_text(encoding="utf-8", errors="replace")
    found: set[Path] = set()
    for raw in AGENT_PATH_PATTERN.findall(text):
        candidate = Path(raw)
        if candidate.is_absolute():
            continue
        normalized = Path(PurePosixPath(raw.replace("\\", "/")))
        if (root / normalized).is_file():
            found.add(normalized)
    return found


def _reference_paths(config: Any, key: str) -> list[Path]:
    references = config.raw.get("references", {})
    values = references.get(key, []) if isinstance(references, dict) else []
    result: list[Path] = []
    for value in values if isinstance(values, list) else []:
        if isinstance(value, str) and value.strip():
            result.append(config.project_root / Path(value))
    return result


def _project_sources(root: Path, scope_files: Iterable[Path]) -> dict[str, list[PackageSource]]:
    required: dict[Path, PackageSource] = {}
    conditional: dict[Path, PackageSource] = {}

    candidates: set[Path] = set()
    for relative in scope_files:
        candidates.add(relative)
        candidates.update(_agent_chain(root, relative))

    for relative in sorted(candidates):
        for agents in _agent_chain(root, relative):
            required.setdefault(
                agents,
                PackageSource(agents, "project_instructions"),
            )

        try:
            config = discover_project_config(root, relative)
        except ProjectConfigError as exc:
            raise PackageError(str(exc)) from exc
        if config is None:
            continue

        required.setdefault(
            config.config_path,
            PackageSource(config.config_path, "project_config"),
        )

        article_type = config.article_type_for(relative)
        if article_type is not None:
            profile = config.profile_path_for(relative)
            if config.profile_required and not (root / profile).is_file():
                raise PackageError(
                    f"Thiếu hồ sơ bắt buộc: {profile.as_posix()}."
                )
            if (root / profile).is_file():
                required.setdefault(
                    profile,
                    PackageSource(profile, "production_profile"),
                )

        for path in _reference_paths(config, "controlling_documents"):
            if (root / path).is_file():
                required.setdefault(
                    path,
                    PackageSource(path, "controlling_document"),
                )
        for path in _reference_paths(config, "templates"):
            if (root / path).is_file():
                required.setdefault(
                    path,
                    PackageSource(path, "template"),
                )
        for path in _reference_paths(config, "theory_sources"):
            if (root / path).is_file() and path not in required:
                conditional.setdefault(
                    path,
                    PackageSource(
                        path,
                        "theory_source",
                        "Đọc khi quy chuẩn nén chưa đủ cho trường hợp đang xét.",
                    ),
                )

    return {
        "required": list(required.values()),
        "conditional": list(conditional.values()),
    }


def _source_record(source: PackageSource) -> dict[str, str]:
    record = {
        "path": source.path.as_posix(),
        "role": source.role,
    }
    if source.condition:
        record["condition"] = source.condition
    return record


def _infer_scope_mode(paths: Sequence[Path]) -> str:
    suffixes = {path.suffix.lower() for path in paths if path.suffix}
    if suffixes and suffixes <= {".md", ".yml", ".yaml"}:
        return "documentation"
    if ".qmd" in suffixes and len(suffixes) == 1:
        return "article"
    return "mixed" if len(suffixes) > 1 else "explicit"


def _copy_payload(
    root: Path,
    package_root: Path,
    files: Iterable[Path],
) -> None:
    payload_root = package_root / "payload"
    payload_root.mkdir(parents=True, exist_ok=False)
    for relative in sorted(set(files), key=lambda item: item.as_posix()):
        source = root / relative
        target = payload_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def _write_checksums(package_root: Path) -> None:
    paths = [
        Path("PROMPT.md"),
        Path("MANIFEST.yml"),
    ]
    payload_root = package_root / "payload"
    for path in sorted(payload_root.rglob("*")):
        if path.is_file():
            paths.append(path.relative_to(package_root))

    lines = [
        f"{sha256(package_root / relative)}  {relative.as_posix()}"
        for relative in sorted(paths, key=lambda item: item.as_posix())
    ]
    (package_root / CHECKSUM_FILE).write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _write_zip(package_root: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{output.stem}.",
        suffix=".tmp.zip",
        dir=output.parent,
    )
    os.close(fd)
    temporary = Path(temporary_name)
    try:
        with zipfile.ZipFile(
            temporary,
            mode="w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        ) as archive:
            for path in sorted(package_root.rglob("*")):
                if path.is_file():
                    arcname = Path(package_root.name) / path.relative_to(package_root)
                    archive.write(path, arcname.as_posix())
        temporary.replace(output)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def _manifest_sources(
    root: Path,
    scope_files: set[Path],
    explicit_includes: set[Path],
) -> tuple[dict[str, list[dict[str, str]]], set[Path]]:
    required: dict[Path, PackageSource] = {}
    conditional: dict[Path, PackageSource] = {}

    for path in CORE_DOCUMENTS:
        if not (root / path).is_file():
            raise PackageError(f"Thiếu tài liệu hệ thống bắt buộc: {path.as_posix()}.")
        role = "repository_instructions" if path == Path("AGENTS.md") else "system_contract"
        required[path] = PackageSource(path, role)

    for agents in [path for path in required if path.name == "AGENTS.md"]:
        for reference in _agent_references(root, agents):
            required.setdefault(
                reference,
                PackageSource(reference, "repository_instruction_dependency"),
            )

    for path in _runtime_dependency_closure(root):
        required.setdefault(path, PackageSource(path, "runtime_dependency"))

    project = _project_sources(root, scope_files)
    for source in project["required"]:
        required.setdefault(source.path, source)
        for reference in _agent_references(root, source.path) if source.path.name == "AGENTS.md" else []:
            required.setdefault(
                reference,
                PackageSource(reference, "project_instruction_dependency"),
            )
    for source in project["conditional"]:
        if source.path not in required:
            conditional.setdefault(source.path, source)

    for path in sorted(scope_files):
        required.setdefault(path, PackageSource(path, "scope_file"))

    for path in sorted(explicit_includes):
        required[path] = PackageSource(path, "explicit_include")
        conditional.pop(path, None)

    all_files = set(required) | set(conditional)
    sources = {
        "required": [
            _source_record(required[path])
            for path in sorted(required, key=lambda item: item.as_posix())
        ],
        "conditional": [
            _source_record(conditional[path])
            for path in sorted(conditional, key=lambda item: item.as_posix())
        ],
        "historical": [],
    }
    return sources, all_files


def create_package(
    root: Path,
    *,
    output: Path,
    prompt_file: Path,
    purpose: str,
    scope_paths: Sequence[str],
    include_paths: Sequence[str],
    scope_mode: str | None,
    inside_repository_reason: str | None,
) -> dict[str, Any]:
    root = root.resolve()
    output = output.expanduser().resolve()
    prompt_file = prompt_file.expanduser().resolve()

    if not purpose.strip():
        raise PackageError("Mục đích gói không được để trống.")
    if not scope_paths:
        raise PackageError("Phải khai báo ít nhất một đường dẫn phạm vi.")
    if output.exists():
        raise PackageError(f"Đầu ra đã tồn tại: {output}.")
    if not prompt_file.is_file():
        raise PackageError(f"Không tìm thấy prompt: {prompt_file}.")

    try:
        prompt_text = prompt_file.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise PackageError("PROMPT.md phải là UTF-8.") from exc
    if not prompt_text.strip():
        raise PackageError("PROMPT.md không được để trống.")

    output_inside = _is_inside(root, output)
    if output_inside and not (inside_repository_reason or "").strip():
        raise PackageError(
            "Đầu ra nằm trong repository; phải khai báo "
            "--inside-repository-reason."
        )

    normalized_scope = [_relative_to_root(root, raw) for raw in scope_paths]
    normalized_include = [_relative_to_root(root, raw) for raw in include_paths]

    scope_files: set[Path] = set()
    for relative in normalized_scope:
        scope_files.update(_expand_repository_path(root, relative))

    explicit_files: set[Path] = set()
    for relative in normalized_include:
        explicit_files.update(_expand_repository_path(root, relative))

    prompt_relative: Path | None = None
    if _is_inside(root, prompt_file):
        prompt_relative = prompt_file.relative_to(root)
        if prompt_relative in scope_files or prompt_relative in explicit_files:
            raise PackageError(
                "Tệp nguồn của PROMPT.md đồng thời nằm trong payload; "
                "hãy đặt prompt ngoài phạm vi hoặc bỏ đường dẫn ấy khỏi phạm vi."
            )

    sources, selected_files = _manifest_sources(
        root,
        scope_files,
        explicit_files,
    )

    output_relative: Path | None = None
    if output_inside:
        output_relative = output.relative_to(root)
        selected_files = {
            path
            for path in selected_files
            if path != output_relative
            and output_relative not in path.parents
        }

    now = datetime.now().astimezone()
    package_id = f"qmd-context-{now.strftime('%Y%m%d-%H%M%S')}"
    repository = _repository_state(root)
    if repository["commit"] == "unknown":
        raise PackageError("Không xác định được commit Git hiện tại.")

    excluded = [
        ".git",
        ".quarto",
        ".continue",
        "__pycache__",
        "_freeze",
        "docs",
        "node_modules",
        ".venv",
        "venv",
        "*.pyc",
        "secrets-and-machine-local-files",
    ]
    if prompt_relative is not None:
        excluded.append(prompt_relative.as_posix())
    if output_relative is not None:
        excluded.append(output_relative.as_posix())

    manifest: dict[str, Any] = {
        "manifest_version": MANIFEST_VERSION,
        "package": {
            "id": package_id,
            "kind": "context",
            "purpose": purpose.strip(),
            "created_at": now.isoformat(timespec="seconds"),
            "created_by": "zo_qmd.py pack",
        },
        "system": {
            "qmd_core_version": QMD_CORE_VERSION,
            "checker_version": CHECKER_VERSION,
            "project_config_schema": PROJECT_CONFIG_SCHEMA,
            "operations_contract_version": OPERATIONS_CONTRACT_VERSION,
            "manifest_schema": MANIFEST_VERSION,
        },
        "repository": repository,
        "scope": {
            "mode": scope_mode or _infer_scope_mode(normalized_scope),
            "roots": [path.as_posix() or "." for path in normalized_scope],
            "excluded": excluded,
        },
        "output": {
            "path": str(output),
            "inside_repository": output_inside,
            "reason": inside_repository_reason.strip()
            if inside_repository_reason
            else None,
        },
        "entrypoints": {
            "current": {
                "checker": "scripts/zo_check_repo.py",
                "operations_cli": "scripts/zo_qmd.py",
            },
            "target": {},
        },
        "sources": sources,
        "evidence": {
            "commands": [
                "git branch --show-current",
                "git rev-parse HEAD",
            ],
            "reports": [],
            "outputs": [],
        },
        "integrity": {
            "algorithm": HASH_ALGORITHM,
            "file": CHECKSUM_FILE,
        },
        "limitations": [
            "Không chứa .git; gói không phản ánh thay đổi của repository sau thời điểm đóng gói.",
            "repository.dirty và repository.ahead_of_origin được ghi unknown vì gói không chứa bằng chứng Git đủ để tái kiểm chứng hai trạng thái này.",
            "Cần Python và PyYAML để chạy lệnh verify đi kèm.",
        ],
    }

    with tempfile.TemporaryDirectory(prefix="zo-qmd-pack-") as temporary_raw:
        temporary = Path(temporary_raw)
        package_root = temporary / package_id
        package_root.mkdir()

        (package_root / "PROMPT.md").write_text(
            prompt_text.rstrip() + "\n",
            encoding="utf-8",
            newline="\n",
        )
        (package_root / "MANIFEST.yml").write_text(
            yaml.safe_dump(
                manifest,
                allow_unicode=True,
                sort_keys=False,
                default_flow_style=False,
            ),
            encoding="utf-8",
            newline="\n",
        )
        _copy_payload(root, package_root, selected_files)
        _write_checksums(package_root)

        verification = verify_directory(package_root)
        if verification["exit_code"] != EXIT_OK:
            raise PackageError(
                "Gói vừa sinh không vượt qua verify nội bộ: "
                + "; ".join(verification["issues"])
            )

        output.parent.mkdir(parents=True, exist_ok=True)
        if output.suffix.lower() == ".zip":
            _write_zip(package_root, output)
        else:
            shutil.move(str(package_root), str(output))

    result = {
        "package_module_version": PACKAGE_MODULE_VERSION,
        "manifest_version": MANIFEST_VERSION,
        "package_id": package_id,
        "kind": "context",
        "output": str(output),
        "format": "zip" if output.suffix.lower() == ".zip" else "directory",
        "inside_repository": output_inside,
        "scope_roots": manifest["scope"]["roots"],
        "payload_files": len(selected_files),
        "repository": repository,
        "automated_result": "PASS",
        "exit_code": EXIT_OK,
    }
    return result


def _zip_member_is_symlink(info: zipfile.ZipInfo) -> bool:
    mode = (info.external_attr >> 16) & 0o170000
    return mode == stat.S_IFLNK


def _extract_zip_safely(path: Path, destination: Path) -> None:
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        if len(infos) > MAX_ZIP_FILES:
            raise PackageError("ZIP có quá nhiều mục.")
        total = sum(info.file_size for info in infos)
        if total > MAX_ZIP_UNCOMPRESSED_BYTES:
            raise PackageError("ZIP vượt giới hạn kích thước giải nén.")

        seen: set[str] = set()
        seen_casefolded: set[str] = set()
        for info in infos:
            name = info.filename
            if name in seen:
                raise PackageError(f"ZIP có mục trùng: {name}.")
            folded = name.casefold()
            if folded in seen_casefolded:
                raise PackageError(
                    f"ZIP có mục va chạm khi không phân biệt hoa-thường: {name}."
                )
            seen.add(name)
            seen_casefolded.add(folded)
            if "\\" in name:
                raise PackageError(f"ZIP dùng dấu phân cách không chuẩn: {name}.")
            _safe_relative_path(name.rstrip("/"))
            if _zip_member_is_symlink(info):
                raise PackageError(f"ZIP chứa symlink: {name}.")
        archive.extractall(destination)


def _locate_package_root(path: Path) -> Path:
    if all((path / name).exists() for name in TOP_LEVEL_REQUIRED):
        return path
    children = [item for item in path.iterdir()]
    directories = [item for item in children if item.is_dir()]
    files = [item for item in children if item.is_file()]
    if not files and len(directories) == 1:
        candidate = directories[0]
        if all((candidate / name).exists() for name in TOP_LEVEL_REQUIRED):
            return candidate
    raise PackageError(
        "Không xác định được package root chứa PROMPT.md, MANIFEST.yml, "
        "FILES.sha256 và payload/."
    )


def _parse_checksums(path: Path) -> tuple[dict[PurePosixPath, str], list[str]]:
    checksums: dict[PurePosixPath, str] = {}
    listed_order: list[PurePosixPath] = []
    issues: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        return {}, [f"Không đọc được FILES.sha256: {exc}."]

    for number, line in enumerate(lines, start=1):
        match = CHECKSUM_LINE_PATTERN.fullmatch(line)
        if match is None:
            issues.append(f"FILES.sha256 dòng {number} sai định dạng.")
            continue
        digest, raw_path = match.groups()
        try:
            relative = _safe_relative_path(raw_path)
        except PackageError as exc:
            issues.append(str(exc))
            continue
        if relative == PurePosixPath(CHECKSUM_FILE):
            issues.append("FILES.sha256 không được tự liệt kê chính nó.")
            continue
        if relative in checksums:
            issues.append(f"Checksum bị lặp: {relative.as_posix()}.")
            continue
        checksums[relative] = digest
        listed_order.append(relative)

    expected_order = sorted(listed_order, key=lambda item: item.as_posix())
    if listed_order != expected_order:
        issues.append("FILES.sha256 phải được sắp xếp theo đường dẫn.")
    return checksums, issues


def _manifest_issues(manifest: Any) -> list[str]:
    issues: list[str] = []
    if not isinstance(manifest, dict):
        return ["MANIFEST.yml phải là mapping."]

    required_top = {
        "manifest_version",
        "package",
        "system",
        "repository",
        "scope",
        "output",
        "sources",
        "integrity",
        "limitations",
    }
    for key in sorted(required_top - set(manifest)):
        issues.append(f"Manifest thiếu trường: {key}.")

    if manifest.get("manifest_version") != MANIFEST_VERSION:
        issues.append("manifest_version phải bằng 1.")

    package = manifest.get("package")
    if not isinstance(package, dict):
        issues.append("package phải là mapping.")
    else:
        for key in ("id", "kind", "purpose", "created_at"):
            if not isinstance(package.get(key), str) or not package.get(key, "").strip():
                issues.append(f"package.{key} phải là chuỗi không rỗng.")
        if package.get("kind") not in {"context", "release"}:
            issues.append("package.kind phải là context hoặc release.")

    system = manifest.get("system")
    if not isinstance(system, dict):
        issues.append("system phải là mapping.")
    else:
        for key in (
            "qmd_core_version",
            "checker_version",
            "project_config_schema",
            "operations_contract_version",
            "manifest_schema",
        ):
            if key not in system:
                issues.append(f"system thiếu trường: {key}.")

    repository = manifest.get("repository")
    if not isinstance(repository, dict):
        issues.append("repository phải là mapping.")
    else:
        if repository.get("source") not in {"live_repository", "exported_snapshot"}:
            issues.append(
                "repository.source phải là live_repository hoặc exported_snapshot."
            )
        commit = repository.get("commit")
        if commit != "unknown" and not (
            isinstance(commit, str) and FULL_SHA_PATTERN.fullmatch(commit)
        ):
            issues.append("repository.commit phải là SHA 40 kí tự hoặc unknown.")
        dirty = repository.get("dirty")
        if not (
            isinstance(dirty, bool)
            or dirty == "unknown"
        ):
            issues.append("repository.dirty phải là true, false hoặc unknown.")
        ahead = repository.get("ahead_of_origin")
        if ahead != "unknown" and not (
            isinstance(ahead, int)
            and not isinstance(ahead, bool)
            and ahead >= 0
        ):
            issues.append(
                "repository.ahead_of_origin phải là số nguyên không âm hoặc unknown."
            )
        for key in ("source", "branch", "commit", "dirty"):
            if key not in repository:
                issues.append(f"repository thiếu trường: {key}.")

    scope = manifest.get("scope")
    if not isinstance(scope, dict):
        issues.append("scope phải là mapping.")
    else:
        if not isinstance(scope.get("roots"), list) or not scope.get("roots"):
            issues.append("scope.roots phải là danh sách không rỗng.")
        if not isinstance(scope.get("excluded"), list):
            issues.append("scope.excluded phải là danh sách.")

    output = manifest.get("output")
    if not isinstance(output, dict):
        issues.append("output phải là mapping.")
    else:
        if not isinstance(output.get("path"), str) or not output.get("path", "").strip():
            issues.append("output.path phải là chuỗi không rỗng.")
        if not isinstance(output.get("inside_repository"), bool):
            issues.append("output.inside_repository phải là boolean.")
        if output.get("inside_repository") and not output.get("reason"):
            issues.append(
                "output.reason bắt buộc khi output.inside_repository=true."
            )

    sources = manifest.get("sources")
    if not isinstance(sources, dict):
        issues.append("sources phải là mapping.")
    else:
        required = sources.get("required")
        if not isinstance(required, list) or not required:
            issues.append("sources.required phải là danh sách không rỗng.")
        for group in ("required", "conditional", "historical"):
            values = sources.get(group, [])
            if not isinstance(values, list):
                issues.append(f"sources.{group} phải là danh sách.")
                continue
            for index, item in enumerate(values):
                if not isinstance(item, dict):
                    issues.append(f"sources.{group}[{index}] phải là mapping.")
                    continue
                if not isinstance(item.get("path"), str) or not item.get("path", "").strip():
                    issues.append(f"sources.{group}[{index}].path không hợp lệ.")
                if not isinstance(item.get("role"), str) or not item.get("role", "").strip():
                    issues.append(f"sources.{group}[{index}].role không hợp lệ.")

    integrity = manifest.get("integrity")
    if not isinstance(integrity, dict):
        issues.append("integrity phải là mapping.")
    else:
        if integrity.get("algorithm") != HASH_ALGORITHM:
            issues.append("integrity.algorithm phải là sha256.")
        if integrity.get("file") != CHECKSUM_FILE:
            issues.append("integrity.file phải là FILES.sha256.")

    if not isinstance(manifest.get("limitations"), list):
        issues.append("limitations phải là danh sách.")

    if isinstance(package, dict) and package.get("kind") == "release":
        release = manifest.get("release")
        if not isinstance(release, dict):
            issues.append("Gói release phải có nhóm release.")
        else:
            for key in (
                "version",
                "tag",
                "previous_version",
                "regression_status",
                "rollback_tested",
            ):
                if key not in release:
                    issues.append(f"release thiếu trường: {key}.")

    return issues


def verify_directory(package_root: Path) -> dict[str, Any]:
    issues: list[str] = []
    checks: list[dict[str, str]] = []

    def add(name: str, status: str, message: str) -> None:
        checks.append({"name": name, "status": status, "message": message})
        if status == "FAIL":
            issues.append(message)

    if not package_root.is_dir():
        add("package-root", "FAIL", f"Không phải thư mục: {package_root}.")
        return {
            "package_root": str(package_root),
            "checks": checks,
            "issues": issues,
            "automated_result": "FAIL",
            "exit_code": EXIT_FAILED,
        }

    top_items = list(package_root.iterdir())
    top_names = {item.name for item in top_items}
    top_symlinks = sorted(item.name for item in top_items if item.is_symlink())
    if top_symlinks:
        add(
            "top-level-symlinks",
            "FAIL",
            "Cấp gốc chứa symlink: " + ", ".join(top_symlinks) + ".",
        )
    else:
        add("top-level-symlinks", "PASS", "Cấp gốc không chứa symlink.")

    required_names = set(TOP_LEVEL_REQUIRED)
    missing_top = sorted(required_names - top_names)
    extra_top = sorted(top_names - required_names)
    if missing_top:
        add(
            "top-level-required",
            "FAIL",
            "Thiếu mục cấp gốc: " + ", ".join(missing_top) + ".",
        )
    else:
        add("top-level-required", "PASS", "Đủ bốn thành phần bắt buộc.")
    if extra_top:
        add(
            "top-level-extra",
            "FAIL",
            "Có mục cấp gốc ngoài hợp đồng: " + ", ".join(extra_top) + ".",
        )
    else:
        add("top-level-extra", "PASS", "Không có mục cấp gốc thừa.")

    prompt = package_root / "PROMPT.md"
    if prompt.is_file():
        try:
            prompt_text = prompt.read_text(encoding="utf-8")
            if prompt_text.strip():
                add("prompt", "PASS", "PROMPT.md là UTF-8 và không rỗng.")
            else:
                add("prompt", "FAIL", "PROMPT.md rỗng.")
        except UnicodeDecodeError:
            add("prompt", "FAIL", "PROMPT.md không phải UTF-8.")
    else:
        add("prompt", "FAIL", "Thiếu PROMPT.md.")

    manifest_path = package_root / "MANIFEST.yml"
    manifest: Any = None
    if manifest_path.is_file():
        try:
            manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
            manifest_errors = _manifest_issues(manifest)
            if manifest_errors:
                for message in manifest_errors:
                    add("manifest", "FAIL", message)
            else:
                add("manifest", "PASS", "MANIFEST.yml đạt schema phiên bản 1.")
        except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
            add("manifest", "FAIL", f"Không đọc được MANIFEST.yml: {exc}.")
    else:
        add("manifest", "FAIL", "Thiếu MANIFEST.yml.")

    payload_root = package_root / "payload"
    symlinks: list[str] = []
    forbidden_payload: list[str] = []
    if payload_root.is_dir():
        for path in payload_root.rglob("*"):
            relative_to_payload = path.relative_to(payload_root)
            if path.is_symlink():
                symlinks.append(path.relative_to(package_root).as_posix())
            elif _path_is_hard_excluded(relative_to_payload):
                forbidden_payload.append(
                    path.relative_to(package_root).as_posix()
                )
            elif path.is_file() and _is_forbidden_file(path):
                forbidden_payload.append(
                    path.relative_to(package_root).as_posix()
                )
        if symlinks:
            add(
                "payload-symlinks",
                "FAIL",
                "Payload chứa symlink: " + ", ".join(sorted(symlinks)) + ".",
            )
        else:
            add("payload-symlinks", "PASS", "Payload không chứa symlink.")
        if forbidden_payload:
            add(
                "payload-forbidden",
                "FAIL",
                "Payload chứa đường dẫn bị cấm: "
                + ", ".join(sorted(forbidden_payload))
                + ".",
            )
        else:
            add(
                "payload-forbidden",
                "PASS",
                "Payload không chứa đường dẫn hệ thống, cache hoặc tệp nhạy cảm theo tên.",
            )
    else:
        add("payload", "FAIL", "Thiếu thư mục payload/.")

    checksum_path = package_root / CHECKSUM_FILE
    checksums, checksum_parse_issues = (
        _parse_checksums(checksum_path)
        if checksum_path.is_file()
        else ({}, ["Thiếu FILES.sha256."])
    )
    for message in checksum_parse_issues:
        add("checksums-format", "FAIL", message)
    if not checksum_parse_issues:
        add("checksums-format", "PASS", "FILES.sha256 đúng định dạng.")

    actual_files: set[PurePosixPath] = set()
    for fixed in ("PROMPT.md", "MANIFEST.yml"):
        if (package_root / fixed).is_file():
            actual_files.add(PurePosixPath(fixed))
    if payload_root.is_dir():
        for path in payload_root.rglob("*"):
            if path.is_file() and not path.is_symlink():
                actual_files.add(
                    PurePosixPath(path.relative_to(package_root).as_posix())
                )

    listed_files = set(checksums)
    missing_files = sorted(
        listed_files - actual_files,
        key=lambda item: item.as_posix(),
    )
    extra_files = sorted(
        actual_files - listed_files,
        key=lambda item: item.as_posix(),
    )
    if missing_files:
        add(
            "checksums-missing",
            "FAIL",
            "Tệp được liệt kê nhưng bị thiếu: "
            + ", ".join(item.as_posix() for item in missing_files)
            + ".",
        )
    else:
        add("checksums-missing", "PASS", "Không có tệp bị thiếu.")
    if extra_files:
        add(
            "checksums-extra",
            "FAIL",
            "Tệp có trong gói nhưng không được liệt kê: "
            + ", ".join(item.as_posix() for item in extra_files)
            + ".",
        )
    else:
        add("checksums-extra", "PASS", "Không có tệp thừa.")

    mismatches: list[str] = []
    for relative in sorted(
        listed_files & actual_files,
        key=lambda item: item.as_posix(),
    ):
        actual = sha256(package_root / Path(relative.as_posix()))
        if actual != checksums[relative]:
            mismatches.append(relative.as_posix())
    if mismatches:
        add(
            "checksums-values",
            "FAIL",
            "Checksum sai: " + ", ".join(mismatches) + ".",
        )
    else:
        add("checksums-values", "PASS", "Các checksum khớp.")

    if isinstance(manifest, dict) and isinstance(manifest.get("sources"), dict):
        missing_sources: list[str] = []
        for group in ("required", "conditional", "historical"):
            values = manifest["sources"].get(group, [])
            if not isinstance(values, list):
                continue
            for item in values:
                if not isinstance(item, dict) or not isinstance(item.get("path"), str):
                    continue
                try:
                    relative = _safe_relative_path(item["path"])
                except PackageError:
                    missing_sources.append(item["path"])
                    continue
                source_path = payload_root / Path(relative.as_posix())
                if not source_path.is_file() or source_path.is_symlink():
                    missing_sources.append(item["path"])
        if missing_sources:
            add(
                "manifest-sources",
                "FAIL",
                "Nguồn khai báo không có trong payload: "
                + ", ".join(sorted(set(missing_sources)))
                + ".",
            )
        else:
            add(
                "manifest-sources",
                "PASS",
                "Các nguồn khai báo đều có trong payload.",
            )

    result = {
        "package_module_version": PACKAGE_MODULE_VERSION,
        "manifest_version": manifest.get("manifest_version")
        if isinstance(manifest, dict)
        else None,
        "package_root": str(package_root),
        "package_id": (
            manifest.get("package", {}).get("id")
            if isinstance(manifest, dict)
            and isinstance(manifest.get("package"), dict)
            else None
        ),
        "kind": (
            manifest.get("package", {}).get("kind")
            if isinstance(manifest, dict)
            and isinstance(manifest.get("package"), dict)
            else None
        ),
        "checks": checks,
        "issues": issues,
        "automated_result": "FAIL" if issues else "PASS",
        "exit_code": EXIT_FAILED if issues else EXIT_OK,
    }
    return result


def verify_package(path: Path) -> dict[str, Any]:
    path = path.expanduser().resolve()
    if not path.exists():
        raise PackageError(f"Không tồn tại: {path}.")

    if path.is_dir():
        package_root = _locate_package_root(path)
        result = verify_directory(package_root)
        result["input"] = str(path)
        result["format"] = "directory"
        return result

    if path.is_file() and path.suffix.lower() == ".zip":
        with tempfile.TemporaryDirectory(prefix="zo-qmd-verify-") as temporary_raw:
            temporary = Path(temporary_raw)
            _extract_zip_safely(path, temporary)
            package_root = _locate_package_root(temporary)
            result = verify_directory(package_root)
            result["input"] = str(path)
            result["format"] = "zip"
            return result

    raise PackageError("verify chỉ nhận thư mục gói hoặc tệp .zip.")


def _print_pack_result(result: Mapping[str, Any], *, json_output: bool) -> None:
    if json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(f"QMD PACKAGE MODULE: {result['package_module_version']}")
    print(f"PACKAGE ID: {result['package_id']}")
    print(f"KIND: {result['kind']}")
    print(f"OUTPUT: {result['output']}")
    print(f"FORMAT: {result['format']}")
    print(f"PAYLOAD FILES: {result['payload_files']}")
    print(
        f"AUTOMATED RESULT: {result['automated_result']} "
        f"| EXIT={result['exit_code']}"
    )


def _print_verify_result(result: Mapping[str, Any], *, json_output: bool) -> None:
    if json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(f"QMD PACKAGE MODULE: {result['package_module_version']}")
    print(f"INPUT: {result.get('input', result['package_root'])}")
    print(f"FORMAT: {result.get('format', 'directory')}")
    print(f"PACKAGE ID: {result.get('package_id') or 'unknown'}")
    print(f"KIND: {result.get('kind') or 'unknown'}")
    print("CHECKS:")
    for item in result["checks"]:
        print(f"  {item['status']} {item['name']}: {item['message']}")
    print(
        f"AUTOMATED RESULT: {result['automated_result']} "
        f"| EXIT={result['exit_code']}"
    )


def self_test() -> int:
    with tempfile.TemporaryDirectory(prefix="zo-qmd-package-self-test-") as raw:
        root = Path(raw) / "sample"
        payload = root / "payload"
        payload.mkdir(parents=True)
        (root / "PROMPT.md").write_text(
            "# Nhiệm vụ\n\nKiểm tra gói.\n",
            encoding="utf-8",
        )
        manifest = {
            "manifest_version": 1,
            "package": {
                "id": "qmd-context-self-test",
                "kind": "context",
                "purpose": "Self-test",
                "created_at": "2026-01-01T00:00:00+07:00",
                "created_by": "self-test",
            },
            "system": {
                "qmd_core_version": "1.0",
                "checker_version": "2.6.0",
                "project_config_schema": 1,
                "operations_contract_version": "0.2",
                "manifest_schema": 1,
            },
            "repository": {
                "name": "sample",
                "source": "exported_snapshot",
                "branch": "master",
                "commit": "0" * 40,
                "dirty": "unknown",
                "ahead_of_origin": "unknown",
            },
            "scope": {
                "mode": "documentation",
                "roots": ["AGENTS.md"],
                "excluded": [".git"],
            },
            "output": {
                "path": "sample",
                "inside_repository": False,
                "reason": None,
            },
            "entrypoints": {
                "current": {
                    "checker": "scripts/zo_check_repo.py",
                    "operations_cli": "scripts/zo_qmd.py",
                },
                "target": {},
            },
            "sources": {
                "required": [
                    {
                        "path": "AGENTS.md",
                        "role": "repository_instructions",
                    }
                ],
                "conditional": [],
                "historical": [],
            },
            "evidence": {"commands": [], "reports": [], "outputs": []},
            "integrity": {
                "algorithm": "sha256",
                "file": "FILES.sha256",
            },
            "limitations": ["Self-test package."],
        }
        (root / "MANIFEST.yml").write_text(
            yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        (payload / "AGENTS.md").write_text(
            "# Chỉ dẫn\n",
            encoding="utf-8",
        )
        _write_checksums(root)

        passed = verify_directory(root)
        if passed["exit_code"] != EXIT_OK:
            print(json.dumps(passed, ensure_ascii=False, indent=2), file=sys.stderr)
            return EXIT_FAILED

        checksum_path = root / "FILES.sha256"
        ordered_lines = checksum_path.read_text(encoding="utf-8").splitlines()
        checksum_path.write_text(
            "\n".join(reversed(ordered_lines)) + "\n",
            encoding="utf-8",
        )
        unsorted = verify_directory(root)
        if unsorted["exit_code"] == EXIT_OK:
            print("Self-test không phát hiện checksum chưa sắp xếp.", file=sys.stderr)
            return EXIT_FAILED

        _write_checksums(root)
        (payload / "AGENTS.md").write_text(
            "# Đã thay đổi\n",
            encoding="utf-8",
        )
        mismatch = verify_directory(root)
        if mismatch["exit_code"] == EXIT_OK:
            print("Self-test không phát hiện checksum sai.", file=sys.stderr)
            return EXIT_FAILED

        _write_checksums(root)
        (payload / "extra.md").write_text("extra\n", encoding="utf-8")
        extra = verify_directory(root)
        if extra["exit_code"] == EXIT_OK:
            print("Self-test không phát hiện tệp thừa.", file=sys.stderr)
            return EXIT_FAILED

        (payload / "extra.md").unlink()
        forbidden = payload / ".GIT"
        forbidden.mkdir()
        _write_checksums(root)
        forbidden_result = verify_directory(root)
        if forbidden_result["exit_code"] == EXIT_OK:
            print("Self-test không phát hiện thư mục bị cấm.", file=sys.stderr)
            return EXIT_FAILED

        for unsafe_path in ("C:/escape.txt", "a//b.txt", "../escape.txt"):
            try:
                _safe_relative_path(unsafe_path)
            except PackageError:
                pass
            else:
                print(
                    f"Self-test không từ chối đường dẫn: {unsafe_path}.",
                    file=sys.stderr,
                )
                return EXIT_FAILED

        if _directory_is_excluded(Path("content/project/docs/source.md")):
            print("Self-test loại nhầm thư mục docs lồng trong nội dung.", file=sys.stderr)
            return EXIT_FAILED
        if not _directory_is_excluded(Path("docs/output.html")):
            print("Self-test không loại thư mục docs ở gốc.", file=sys.stderr)
            return EXIT_FAILED

    print("PASS: zo_qmd_package self-test")
    return EXIT_OK


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    subparsers = result.add_subparsers(dest="command", required=True)

    pack = subparsers.add_parser("pack", help="Tạo gói ngữ cảnh chuẩn.")
    pack.add_argument("--repo-root", required=True)
    pack.add_argument("--output", required=True)
    pack.add_argument("--prompt", required=True)
    pack.add_argument("--purpose", required=True)
    pack.add_argument("--scope-mode")
    pack.add_argument("--include", action="append", default=[])
    pack.add_argument("--inside-repository-reason")
    pack.add_argument("--json", action="store_true")
    pack.add_argument("paths", nargs="+")

    verify = subparsers.add_parser("verify", help="Xác minh gói chuẩn.")
    verify.add_argument("package")
    verify.add_argument("--json", action="store_true")

    subparsers.add_parser("self-test", help="Chạy self-test.")

    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "pack":
            result = create_package(
                Path(args.repo_root),
                output=Path(args.output),
                prompt_file=Path(args.prompt),
                purpose=args.purpose,
                scope_paths=args.paths,
                include_paths=args.include,
                scope_mode=args.scope_mode,
                inside_repository_reason=args.inside_repository_reason,
            )
            _print_pack_result(result, json_output=args.json)
            return int(result["exit_code"])

        if args.command == "verify":
            result = verify_package(Path(args.package))
            _print_verify_result(result, json_output=args.json)
            return int(result["exit_code"])

        if args.command == "self-test":
            return self_test()

        print(f"ERROR: Lệnh chưa được hỗ trợ: {args.command}", file=sys.stderr)
        return EXIT_USAGE
    except PackageError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_FAILED
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_FAILED


if __name__ == "__main__":
    raise SystemExit(main())

"""Unified operations front end for the ZO Math QMD system.

This command coordinates the existing configuration loader, registry, checker,
Quarto wrapper, regression baseline, and package module. It does not duplicate
validators and does not accept, publish, stage, or commit content.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from zo_check_repo import CHECKER_VERSION
from zo_qmd_config import (
    CONFIG_RELATIVE_PATH,
    ProjectConfig,
    ProjectConfigError,
    discover_project_config,
    load_project_config,
)
from zo_qmd_registry import ModuleRegistryError, build_validation_plan
from zo_qmd_prepublish import PrepublishError, build_report
from zo_qmd_review import REVIEW_READY_VERSION
from zo_qmd_version import OPERATIONS_CLI_VERSION

EXIT_OK = 0
EXIT_FAILED = 1
EXIT_USAGE = 2
EXIT_MISSING_TOOL = 3
SESSION_MANIFEST_VERSION = 3

SYSTEM_DOCUMENTS = (
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
    Path("quy_trinh_xay_dung/he_thong_san_xuat_qmd/CHANGELOG.md"),
    Path(
        "quy_trinh_xay_dung/he_thong_san_xuat_qmd/"
        "ma_tran_phien_ban_qmd.md"
    ),
    Path(
        "quy_trinh_xay_dung/he_thong_san_xuat_qmd/"
        "quy_trinh_phat_hanh_va_khoi_phuc_qmd.md"
    ),
    Path(
        "quy_trinh_xay_dung/he_thong_san_xuat_qmd/"
        "mau_ho_so_phat_hanh_qmd.yml"
    ),
)

SYSTEM_SCRIPTS = (
    Path("scripts/zo_python.py"),
    Path("scripts/zo_quarto.py"),
    Path("scripts/zo_qmd.py"),
    Path("scripts/zo_qmd_package.py"),
    Path("scripts/zo_qmd_version.py"),
    Path("scripts/zo_qmd_prepublish.py"),
    Path("scripts/zo_qmd_review.py"),
    Path("scripts/zo_qmd_visual.ps1"),
    Path("scripts/zo_artifact_freshness.py"),
    Path("scripts/zo_check_repo.py"),
    Path("scripts/zo_qmd_config.py"),
    Path("scripts/zo_qmd_registry.py"),
    Path("scripts/zo_qmd_core.py"),
    Path("scripts/zo_real_world_problem.py"),
)

SELF_TEST_SCRIPTS = (
    Path("scripts/zo_artifact_freshness.py"),
    Path("scripts/zo_qmd_config.py"),
    Path("scripts/zo_qmd_registry.py"),
    Path("scripts/zo_qmd_core.py"),
    Path("scripts/zo_real_world_problem.py"),
    Path("scripts/zo_qmd_package.py"),
    Path("scripts/zo_qmd_version.py"),
    Path("scripts/zo_qmd_prepublish.py"),
    Path("scripts/zo_qmd_review.py"),
)


def _run(
    command: Sequence[str],
    cwd: Path,
    *,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(command),
        cwd=cwd,
        check=False,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=capture,
        env=os.environ.copy(),
    )


def _repo_root(raw: str | None) -> tuple[Path | None, int, str]:
    git = shutil.which("git")
    if git is None:
        return None, EXIT_MISSING_TOOL, "Không tìm thấy git trong PATH."

    start = Path(raw or ".").expanduser().resolve()
    location = start if start.is_dir() else start.parent
    result = _run(
        [git, "-C", str(location), "rev-parse", "--show-toplevel"],
        location,
        capture=True,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip()
        return None, EXIT_USAGE, message or f"Không tìm thấy repository từ {start}."

    return Path(result.stdout.strip()).resolve(), EXIT_OK, ""


def _relative_to_root(root: Path, raw: str) -> Path:
    candidate = Path(raw).expanduser()
    resolved = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    try:
        return resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Đường dẫn nằm ngoài repository: {raw}") from exc


def _explicit_output_path(root: Path, raw: str) -> Path:
    candidate = Path(raw).expanduser()
    resolved = (
        candidate.resolve()
        if candidate.is_absolute()
        else (root / candidate).resolve()
    )

    try:
        relative = resolved.relative_to(root)
    except ValueError:
        return resolved

    if not relative.parts or relative.parts[0] != "_audit":
        raise ValueError(
            "Đầu ra nằm trong repository phải ở dưới _audit/: "
            f"{relative.as_posix()}"
        )
    return resolved


def _read_request(args: argparse.Namespace) -> str:
    if args.request is not None:
        request = args.request.strip()
    else:
        request_path = Path(args.request_file).expanduser().resolve()
        request = request_path.read_text(encoding="utf-8").strip()

    if not request:
        raise ValueError("Yêu cầu ban đầu không được rỗng.")
    return request


def _git_snapshot(root: Path) -> dict[str, Any]:
    git = shutil.which("git")
    if git is None:
        raise OSError("Không tìm thấy git trong PATH.")

    def read(*arguments: str) -> str:
        result = _run([git, "-C", str(root), *arguments], root, capture=True)
        if result.returncode != 0:
            message = result.stderr.strip() or result.stdout.strip()
            raise OSError(message or f"Git thất bại: {' '.join(arguments)}")
        return result.stdout.strip()

    status = read("status", "--short")
    return {
        "branch": read("branch", "--show-current") or None,
        "commit": read("rev-parse", "HEAD"),
        "clean": not bool(status),
        "status": status.splitlines(),
    }




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


def _git_dirty_paths(root: Path) -> list[Path]:
    git = shutil.which("git")
    if git is None:
        raise OSError("Không tìm thấy git trong PATH.")

    changed = _run(
        [git, "-C", str(root), "diff", "--name-only", "HEAD", "--"],
        root,
        capture=True,
    )
    if changed.returncode != 0:
        raise OSError(changed.stderr.strip() or "Không đọc được Git diff.")
    untracked = _run(
        [git, "-C", str(root), "ls-files", "--others", "--exclude-standard"],
        root,
        capture=True,
    )
    if untracked.returncode != 0:
        raise OSError(untracked.stderr.strip() or "Không đọc được tệp untracked.")

    values = {line.strip() for line in changed.stdout.splitlines() if line.strip()}
    values.update(line.strip() for line in untracked.stdout.splitlines() if line.strip())
    return [Path(value) for value in sorted(values)]


def _dirty_fingerprints(root: Path) -> dict[str, str]:
    return {
        path.as_posix(): _path_fingerprint(root, path)
        for path in _git_dirty_paths(root)
    }


def _human_review_policy(config: ProjectConfig, article_type: str) -> dict[str, Any]:
    extensions = config.raw.get("extensions", {})
    if not isinstance(extensions, dict):
        return {}
    gate = extensions.get("human_review_gate", {})
    if not isinstance(gate, dict) or gate.get("enabled") is not True:
        return {}
    article_types = gate.get("article_types", {})
    if not isinstance(article_types, dict):
        return {}
    policy = article_types.get(article_type, {})
    return policy if isinstance(policy, dict) else {}


def _canonical_production_scope(
    root: Path, summary: dict[str, Any], config: ProjectConfig
) -> list[Path]:
    target = Path(str(summary["target"]))
    article_type = str(summary.get("article_type") or "")
    policy = _human_review_policy(config, article_type)
    lifecycle = policy.get("lifecycle", {})
    if not isinstance(lifecycle, dict) or lifecycle.get("auto_scope") is not True:
        return []

    paths: list[Path] = [target]
    profile = summary.get("profile")
    if isinstance(profile, dict) and profile.get("path"):
        paths.append(Path(str(profile["path"])))

    if article_type == "function_article":
        paths.append(target.with_suffix(".pdf"))
        paths.append(config.project_root / "_figures" / target.stem)

    navigation = policy.get("navigation", {})
    if isinstance(navigation, dict) and navigation.get("explicit_sidebar_required") is True:
        raw_quarto = navigation.get("quarto_config", "_quarto.yml")
        if isinstance(raw_quarto, str) and raw_quarto.strip():
            paths.append(_relative_to_root(root, raw_quarto.strip()))

    return [Path(value) for value in _unique_paths(paths)]


def _authority_records(
    root: Path,
    summary: dict[str, Any],
    config: ProjectConfig,
    article_type: str,
) -> tuple[list[dict[str, Any]], list[str]]:
    """Build the effective authority closure plus reference inventory.

    Q1-R5 deliberately separates governing/provenance inputs, which are locked
    for the whole production session, from optional references.  The AGENTS
    chain and project config are always included dynamically so a deeper
    AGENTS.md cannot be missed by a static registry.
    """

    records: list[dict[str, Any]] = []
    missing_required: list[str] = []
    seen: set[Path] = set()

    def add(raw: str | Path, role: str, reason: str, *, lock: bool) -> None:
        relative = _relative_to_root(root, str(raw))
        if relative in seen:
            return
        seen.add(relative)
        absolute = root / relative
        if not absolute.is_file():
            if lock:
                missing_required.append(relative.as_posix())
            return
        records.append(
            {
                "path": relative.as_posix(),
                "sha256": _sha256_file(absolute),
                "size": absolute.stat().st_size,
                "role": role,
                "reason": reason,
                "lock": lock,
            }
        )

    for raw in summary.get("agents_chain", []):
        add(str(raw), "governing_required", "agents_chain", lock=True)
    add(config.config_path, "governing_required", "project_config", lock=True)

    registry = config.raw.get("authority_registry", {})
    if not isinstance(registry, dict):
        registry = {}

    for item in registry.get("governing_required", []):
        if isinstance(item, dict) and item.get("path"):
            add(
                str(item["path"]),
                "governing_required",
                str(item.get("reason") or "configured_governing_authority"),
                lock=True,
            )

    for item in registry.get("provenance_required", []):
        if isinstance(item, dict) and item.get("path"):
            add(
                str(item["path"]),
                "provenance_required",
                str(item.get("reason") or "configured_provenance"),
                lock=True,
            )

    policy = _human_review_policy(config, article_type)
    graph_required = (
        isinstance(policy.get("function_graph"), dict)
        and policy["function_graph"].get("required") is True
    )
    for item in registry.get("conditional_required", []):
        if not isinstance(item, dict) or not item.get("path"):
            continue
        condition = str(item.get("when") or "")
        active = condition == "function_graph_required" and graph_required
        if active:
            add(
                str(item["path"]),
                "conditional_required",
                str(item.get("reason") or condition or "configured_condition"),
                lock=True,
            )

    for item in registry.get("reference_only", []):
        if isinstance(item, dict) and item.get("path"):
            add(
                str(item["path"]),
                "reference_only",
                str(item.get("reason") or "optional_reference"),
                lock=False,
            )

    # Backward-compatible fallback for projects not yet migrated to the registry.
    if not registry:
        raw_paths: list[str] = []
        raw_paths.extend(str(value) for value in summary.get("agents_chain", []))
        project = summary.get("project", {})
        if isinstance(project, dict) and project.get("config_path"):
            raw_paths.append(str(project["config_path"]))
        references = summary.get("references", {})
        if isinstance(references, dict):
            for values in references.values():
                if isinstance(values, list):
                    for record in values:
                        if isinstance(record, dict) and record.get("exists") is True and record.get("path"):
                            raw_paths.append(str(record["path"]))
        for raw in raw_paths:
            add(raw, "governing_required", "legacy_reference_set", lock=True)

    return records, missing_required


def _unique_paths(paths: Sequence[Path]) -> list[str]:
    seen: set[Path] = set()
    result: list[str] = []
    for path in paths:
        if path in seen:
            continue
        seen.add(path)
        result.append(path.as_posix())
    return result


def _paths_overlap(left: Path, right: Path) -> bool:
    try:
        left.relative_to(right)
        return True
    except ValueError:
        pass

    try:
        right.relative_to(left)
        return True
    except ValueError:
        return False


def _script_command(root: Path, script: Path, *args: str) -> list[str]:
    return [
        sys.executable,
        str(root / "scripts/zo_python.py"),
        str(root / script),
        *args,
    ]


def _print_step(title: str, command: Sequence[str]) -> None:
    print()
    print(f"=== {title} ===")
    print("$ " + " ".join(command))


def _run_step(root: Path, title: str, command: Sequence[str]) -> int:
    _print_step(title, command)
    return _run(command, root).returncode


def _tool_version(command: Sequence[str], root: Path) -> dict[str, Any]:
    result = _run(command, root, capture=True)
    output = (result.stdout.strip() or result.stderr.strip()).splitlines()
    return {
        "available": result.returncode == 0,
        "command": list(command),
        "version": output[0] if output else None,
        "exit_code": result.returncode,
    }


def _agents_chain(root: Path, target: Path) -> list[Path]:
    absolute = root / target
    current = absolute.parent if absolute.suffix else absolute
    try:
        relative_parent = current.resolve().relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Đường dẫn nằm ngoài repository: {target.as_posix()}") from exc

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


def _reference_records(
    root: Path,
    config: ProjectConfig,
    key: str,
) -> list[dict[str, Any]]:
    references = config.raw.get("references", {})
    values = references.get(key, []) if isinstance(references, dict) else []
    records: list[dict[str, Any]] = []
    for value in values if isinstance(values, list) else []:
        if not isinstance(value, str):
            continue
        relative = config.project_root / Path(value)
        records.append(
            {
                "path": relative.as_posix(),
                "exists": (root / relative).is_file(),
            }
        )
    return records


def _project_summary(root: Path, raw_path: str) -> tuple[dict[str, Any], int]:
    relative = _relative_to_root(root, raw_path)
    config = discover_project_config(root, relative)
    if config is None:
        raise ProjectConfigError(
            f"Không tìm thấy {CONFIG_RELATIVE_PATH.as_posix()} cho {relative.as_posix()}."
        )

    article_type = config.article_type_for(relative)
    profile: dict[str, Any] | None = None
    plan: dict[str, Any] | None = None

    if article_type is not None:
        profile_path = config.profile_path_for(relative)
        profile = {
            "path": profile_path.as_posix(),
            "required": config.profile_required,
            "exists": (root / profile_path).is_file(),
        }
        validation_plan = build_validation_plan(config, article_type.id)
        plan = {
            "article_type": validation_plan.article_type,
            "active_modules": list(validation_plan.active_modules),
            "source_adapters": list(validation_plan.source_adapters),
            "render_adapters": list(validation_plan.render_adapters),
            "requires_human_acceptance": validation_plan.requires_human_acceptance,
            "compatibility_mode": validation_plan.compatibility_mode,
        }

    payload: dict[str, Any] = {
        "operations_cli_version": OPERATIONS_CLI_VERSION,
        "checker_version": CHECKER_VERSION,
        "review_ready_version": REVIEW_READY_VERSION,
        "repo_root": str(root),
        "target": relative.as_posix(),
        "target_exists": (root / relative).exists(),
        "agents_chain": [item.as_posix() for item in _agents_chain(root, relative)],
        "project": {
            "schema_version": config.schema_version,
            "config_path": config.config_path.as_posix(),
            "id": config.project_id,
            "name": config.project_name,
            "root": config.project_root.as_posix(),
        },
        "article_type": article_type.id if article_type else None,
        "profile": profile,
        "validation_plan": plan,
        "references": {
            "controlling_documents": _reference_records(
                root, config, "controlling_documents"
            ),
            "templates": _reference_records(root, config, "templates"),
            "theory_sources": _reference_records(root, config, "theory_sources"),
            "quality_exemplars": _reference_records(
                root, config, "quality_exemplars"
            ),
        },
        "publication": config.raw.get("publication", {}),
    }

    exit_code = EXIT_OK
    if relative.suffix.lower() == ".qmd" and article_type is None:
        payload["error"] = "Tệp QMD không khớp loại bài nào trong cấu hình dự án."
        exit_code = EXIT_FAILED
    elif profile and profile["required"] and not profile["exists"]:
        if (root / relative).exists():
            payload["error"] = "Thiếu hồ sơ bắt buộc của bài."
            exit_code = EXIT_FAILED
        else:
            payload["warning"] = (
                "Hồ sơ bắt buộc chưa tồn tại; phải được tạo trong pha sản xuất."
            )

    return payload, exit_code


def _discover_configs(root: Path) -> list[ProjectConfig]:
    ignored = {".git", ".quarto", "docs", "_freeze", "__pycache__"}
    configs: list[ProjectConfig] = []
    pattern = f"**/{CONFIG_RELATIVE_PATH.as_posix()}"
    for path in sorted(root.glob(pattern)):
        relative = path.relative_to(root)
        if any(part in ignored for part in relative.parts):
            continue
        configs.append(load_project_config(root, relative))
    return configs


def _regression_articles(root: Path) -> list[Path]:
    articles: list[Path] = []
    seen: set[Path] = set()

    for config in _discover_configs(root):
        regression = config.raw.get("regression", {})
        if not isinstance(regression, dict):
            continue

        expected = regression.get("expected_checker_version")
        if expected not in (None, CHECKER_VERSION):
            raise ProjectConfigError(
                f"{config.project_id}: checker mong đợi {expected!r}, "
                f"nhưng hiện tại là {CHECKER_VERSION!r}."
            )

        raw_articles = regression.get("articles", [])
        if not isinstance(raw_articles, list):
            raise ProjectConfigError(
                f"{config.project_id}: regression.articles phải là danh sách."
            )

        for raw in raw_articles:
            if not isinstance(raw, str) or not raw.strip():
                raise ProjectConfigError(
                    f"{config.project_id}: đường dẫn hồi quy không hợp lệ."
                )
            relative = config.project_root / Path(raw)
            if relative not in seen:
                seen.add(relative)
                articles.append(relative)

    if not articles:
        raise ProjectConfigError("Không tìm thấy bài hồi quy trong cấu hình dự án.")

    missing = [item.as_posix() for item in articles if not (root / item).is_file()]
    if missing:
        raise ProjectConfigError("Thiếu bài hồi quy: " + ", ".join(missing) + ".")

    return articles


def command_doctor(root: Path, args: argparse.Namespace) -> int:
    checks: list[dict[str, Any]] = []

    def add(name: str, status: str, message: str) -> None:
        checks.append({"name": name, "status": status, "message": message})

    for relative in (*SYSTEM_DOCUMENTS, *SYSTEM_SCRIPTS):
        exists = (root / relative).is_file()
        add(
            f"file:{relative.as_posix()}",
            "PASS" if exists else "FAIL",
            "Tồn tại." if exists else "Không tồn tại.",
        )

    add(
        "python:utf8",
        "PASS" if sys.flags.utf8_mode else "WARN",
        f"Python {sys.version.split()[0]}; utf8_mode={sys.flags.utf8_mode}.",
    )

    yaml_available = importlib.util.find_spec("yaml") is not None
    add(
        "python:pyyaml",
        "PASS" if yaml_available else "FAIL",
        "PyYAML khả dụng." if yaml_available else "Thiếu PyYAML.",
    )

    git = shutil.which("git")
    if git:
        version = _tool_version([git, "--version"], root)
        add("tool:git", "PASS", version["version"] or "git khả dụng.")
    else:
        add("tool:git", "FAIL", "Không tìm thấy git trong PATH.")

    quarto = shutil.which("quarto")
    if quarto:
        version = _tool_version([quarto, "--version"], root)
        add("tool:quarto", "PASS", version["version"] or "Quarto khả dụng.")
    else:
        add("tool:quarto", "FAIL", "Không tìm thấy Quarto trong PATH.")

    pdfinfo = shutil.which("pdfinfo")
    add(
        "tool:pdfinfo",
        "PASS" if pdfinfo else "WARN",
        "pdfinfo khả dụng."
        if pdfinfo
        else "Không có pdfinfo; checker chỉ kiểm tra PDF ở mức giới hạn.",
    )

    try:
        configs = _discover_configs(root)
        if configs:
            add(
                "project-configs",
                "PASS",
                "Đã nạp: " + ", ".join(config.project_id for config in configs) + ".",
            )
        else:
            add("project-configs", "FAIL", "Không tìm thấy cấu hình dự án.")
        for config in configs:
            exemplars = _reference_records(root, config, "quality_exemplars")
            missing = [record["path"] for record in exemplars if not record["exists"]]
            if missing:
                add(
                    f"quality-exemplars:{config.project_id}",
                    "FAIL",
                    "Thiếu: " + ", ".join(missing) + ".",
                )
            else:
                paths = [record["path"] for record in exemplars]
                add(
                    f"quality-exemplars:{config.project_id}",
                    "PASS",
                    "Đã nhận diện: " + ", ".join(paths) + "."
                    if paths
                    else "Danh sách rỗng.",
                )
        articles = _regression_articles(root)
        add(
            "regression-articles",
            "PASS",
            "Đã nhận diện: " + ", ".join(item.as_posix() for item in articles) + ".",
        )
    except (ProjectConfigError, ModuleRegistryError, OSError) as exc:
        add("project-configs", "FAIL", str(exc))

    status = _run(["git", "status", "--short", "--branch"], root, capture=True)
    if status.returncode == 0:
        message = status.stdout.strip() or "Repository sạch."
        add("git-status", "INFO", message)
    else:
        add("git-status", "FAIL", status.stderr.strip() or "Không đọc được Git status.")

    failed = any(item["status"] == "FAIL" for item in checks)
    result = {
        "operations_cli_version": OPERATIONS_CLI_VERSION,
        "checker_version": CHECKER_VERSION,
        "repo_root": str(root),
        "checks": checks,
        "automated_result": "FAIL" if failed else (
            "PASS_WITH_WARNINGS"
            if any(item["status"] == "WARN" for item in checks)
            else "PASS"
        ),
        "exit_code": EXIT_FAILED if failed else EXIT_OK,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"QMD OPERATIONS CLI: {OPERATIONS_CLI_VERSION}")
        print(f"CHECKER VERSION: {CHECKER_VERSION}")
        print(f"ROOT: {root}")
        print("CHECKS:")
        for item in checks:
            print(f"  {item['status']} {item['name']}: {item['message']}")
        print(
            f"AUTOMATED RESULT: {result['automated_result']} "
            f"| EXIT={result['exit_code']}"
        )

    return int(result["exit_code"])


def command_inspect(root: Path, args: argparse.Namespace) -> int:
    try:
        payload, exit_code = _project_summary(root, args.path)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return exit_code
    except (ProjectConfigError, ModuleRegistryError, ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_FAILED


def command_start(root: Path, args: argparse.Namespace) -> int:
    try:
        request = _read_request(args)
        summary, inspect_exit = _project_summary(root, args.path)
        target = str(summary["target"])
        target_path = Path(target)

        if args.output:
            output = _explicit_output_path(root, args.output)
        else:
            output = root / "_audit" / f"{target_path.stem}_session.json"
        if output.suffix.lower() != ".json":
            raise ValueError("Hồ sơ phiên của start phải là tệp .json.")
        if output.exists():
            raise ValueError(f"Đầu ra đã tồn tại: {output}")

        config = discover_project_config(root, target_path)
        if config is None:
            raise ProjectConfigError(
                f"Không tìm thấy cấu hình dự án cho {target}."
            )
        article_type = str(summary.get("article_type") or "")
        policy = _human_review_policy(config, article_type)
        lifecycle = policy.get("lifecycle", {})
        lifecycle = lifecycle if isinstance(lifecycle, dict) else {}

        reference_groups = summary.get("references", {})
        missing_references: list[str] = []
        for records in reference_groups.values():
            for record in records:
                if not record.get("exists", False):
                    missing_references.append(str(record.get("path")))

        blocked_reasons: list[str] = []
        if inspect_exit != EXIT_OK:
            blocked_reasons.append(
                str(summary.get("error", "Inspect không đạt."))
            )
        registry_configured = isinstance(config.raw.get("authority_registry"), dict)
        if missing_references and not registry_configured:
            blocked_reasons.append(
                "Thiếu nguồn điều khiển: " + ", ".join(missing_references)
            )

        project_root = str(summary["project"]["root"])
        canonical = _canonical_production_scope(root, summary, config)
        auto_scope = lifecycle.get("auto_scope") is True and bool(canonical)
        manual_scope = lifecycle.get("manual_scope_extensions") is True

        if auto_scope and not manual_scope and (args.allow or args.exclude):
            raise ValueError(
                "Dự án đã khóa phạm vi production tự động; không dùng --allow/--exclude "
                "để tự mở rộng hoặc thu hẹp phạm vi."
            )

        if auto_scope:
            allowed_paths = list(canonical)
        else:
            allowed_paths = [_relative_to_root(root, target)]
            profile = summary.get("profile")
            if isinstance(profile, dict) and profile.get("path"):
                allowed_paths.append(_relative_to_root(root, str(profile["path"])))
            allowed_paths.extend(_relative_to_root(root, raw) for raw in args.allow)

        excluded_paths = (
            []
            if auto_scope and not manual_scope
            else [_relative_to_root(root, raw) for raw in args.exclude]
        )
        conflicts = sorted(
            {
                allowed_path.as_posix()
                for allowed_path in allowed_paths
                for excluded_path in excluded_paths
                if _paths_overlap(allowed_path, excluded_path)
            }
        )
        if conflicts:
            raise ValueError(
                "Phạm vi được phép tác động chồng lấn phạm vi loại trừ: "
                + ", ".join(conflicts)
            )

        allowed = _unique_paths(allowed_paths)
        excluded = _unique_paths(excluded_paths)
        dirty_at_start = _dirty_fingerprints(root)
        initial_scope_dirty = sorted(
            path
            for path in dirty_at_start
            if any(
                _paths_overlap(Path(path), Path(allowed_path))
                for allowed_path in allowed
            )
        )
        if lifecycle.get("require_clean_candidate_scope_at_start") is True and initial_scope_dirty:
            blocked_reasons.append(
                "Phạm vi candidate đã có thay đổi trước lệnh start: "
                + ", ".join(initial_scope_dirty)
                + ". Hãy start trước khi sản xuất hoặc dùng một workflow tiếp tục được thẩm quyền định nghĩa riêng."
            )

        snapshot = _git_snapshot(root)
        snapshot["dirty_fingerprints"] = dirty_at_start
        authority, missing_authority = _authority_records(root, summary, config, article_type)
        if missing_authority:
            blocked_reasons.append(
                "Thiếu authority bắt buộc: " + ", ".join(missing_authority)
            )
        effective_authority = [item for item in authority if item.get("lock") is True]
        reference_inventory = [item for item in authority if item.get("lock") is not True]

        payload: dict[str, Any] = {
            "session_manifest_version": SESSION_MANIFEST_VERSION,
            "created_at": datetime.now(timezone.utc).isoformat().replace(
                "+00:00", "Z"
            ),
            "operations_cli_version": OPERATIONS_CLI_VERSION,
            "checker_version": CHECKER_VERSION,
            "review_ready_version": REVIEW_READY_VERSION,
            "manifest_path": output.relative_to(root).as_posix() if output.is_relative_to(root) else str(output),
            "request": {
                "text": request,
                "source": (
                    {"kind": "inline"}
                    if args.request is not None
                    else {
                        "kind": "file",
                        "path": str(
                            Path(args.request_file).expanduser().resolve()
                        ),
                    }
                ),
            },
            "repository": snapshot,
            "inspect": summary,
            "authority_sources": {
                "registry_schema_version": 1,
                "agents_chain": list(summary.get("agents_chain", [])),
                "project_config": summary["project"]["config_path"],
                "references": reference_groups,
                "effective": effective_authority,
                "reference_inventory": reference_inventory,
                "snapshot": authority,
            },
            "scope": {
                "target": target,
                "project_root": project_root,
                "strategy": "canonical" if auto_scope else "explicit",
                "allowed": allowed,
                "excluded": excluded,
                "evidence_roots": ["_audit"],
                "initial_scope_dirty": initial_scope_dirty,
            },
            "plan": {
                "objective": request,
                "expected_files": allowed,
                "authority_snapshot_count": len(authority),
                "effective_authority_count": len(effective_authority),
                "reference_inventory_count": len(reference_inventory),
                "phases": [
                    "lock_authority_sources",
                    "create_or_edit_qmd_and_resources",
                    "check_source",
                    "render",
                    "visual_check",
                    "review_ready",
                    "human_review",
                    "prepublish_report",
                ],
                "expected_commands": {
                    "inspect": (
                        "python scripts/zo_python.py scripts/zo_qmd.py "
                        f"inspect {target}"
                    ),
                    "check": (
                        "python scripts/zo_python.py scripts/zo_qmd.py "
                        f"check --report _audit/{Path(target).stem}_check.json {target}"
                    ),
                    "render": (
                        "python scripts/zo_python.py scripts/zo_qmd.py "
                        f"render --report _audit/{Path(target).stem}_render.json {target}"
                    ),
                    "visual_check": (
                        "python scripts/zo_python.py scripts/zo_qmd.py "
                        f"visual-check {target}"
                    ),
                    "review_ready": (
                        "python scripts/zo_python.py scripts/zo_qmd.py "
                        f"review-ready --report _audit/{Path(target).stem}_review_ready.json {target}"
                    ),
                },
                "user_gates": [
                    "human_review",
                    "publication_confirmation",
                ],
                "stop_conditions": [
                    "missing_authority_source",
                    "candidate_scope_dirty_before_start",
                    "scope_drift",
                    "authority_drift",
                    "automated_check_failure",
                    "render_failure",
                    "visual_verification_failure",
                    "review_readiness_failure",
                    "human_review_not_recorded",
                ],
                "states_not_changed": {
                    "final_acceptance": "not_automated",
                    "publication": "pending",
                },
            },
            "status": {
                "planning": "blocked" if blocked_reasons else "ready",
                "production": "blocked" if blocked_reasons else "planned",
                "publication": "pending",
            },
            "blocked_reasons": blocked_reasons,
            "automated_result": "FAIL" if blocked_reasons else "PASS",
            "exit_code": EXIT_FAILED if blocked_reasons else EXIT_OK,
        }

        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"START MANIFEST: {output}")
        print(f"SCOPE STRATEGY: {payload['scope']['strategy']}")
        print("ALLOWED:")
        for item in allowed:
            print(f"  - {item}")
        print(
            f"AUTHORITY SNAPSHOT: {len(authority)} files "
            f"| EFFECTIVE={len(effective_authority)} "
            f"| REFERENCE={len(reference_inventory)}"
        )
        print(
            f"AUTOMATED RESULT: {payload['automated_result']} "
            f"| EXIT={payload['exit_code']}"
        )
        return int(payload["exit_code"])
    except (
        ProjectConfigError,
        ModuleRegistryError,
        ValueError,
        OSError,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_FAILED


def command_visual_check(root: Path, args: argparse.Namespace) -> int:
    powershell = (
        shutil.which("pwsh")
        or shutil.which("powershell")
        or shutil.which("powershell.exe")
    )
    if powershell is None:
        print("ERROR: Không tìm thấy PowerShell để chạy visual-check.", file=sys.stderr)
        return EXIT_MISSING_TOOL
    command = [powershell, "-NoProfile"]
    if Path(powershell).name.casefold().startswith("powershell"):
        command.extend(["-ExecutionPolicy", "Bypass"])
    command.extend(
        [
            "-File",
            str(root / "scripts/zo_qmd_visual.ps1"),
            "-RepoRoot",
            str(root),
            "-Target",
            args.path,
            "-Height",
            str(args.height),
        ]
    )
    return _run_step(root, "QMD VISUAL-CHECK", command)


def command_review_ready(root: Path, args: argparse.Namespace) -> int:
    review_args = ["check", args.path]
    if args.report:
        review_args.extend(["--report", args.report])
    if args.session:
        review_args.extend(["--session", args.session])
    command = _script_command(
        root,
        Path("scripts/zo_qmd_review.py"),
        *review_args,
    )
    return _run_step(root, "QMD REVIEW-READY", command)


def command_prepublish(root: Path, args: argparse.Namespace) -> int:
    try:
        output = _explicit_output_path(root, args.output)
        if output.suffix.lower() != ".json":
            raise ValueError("Báo cáo prepublish phải là tệp .json.")
        if output.exists():
            raise ValueError(f"Đầu ra đã tồn tại: {output}")

        target = _relative_to_root(root, args.path).as_posix()
        summary, inspect_exit = _project_summary(root, target)
        payload, exit_code = build_report(
            root=root,
            target=target,
            operations_cli_version=OPERATIONS_CLI_VERSION,
            project_summary=summary,
            inspect_exit=inspect_exit,
            session_raw=args.session,
            check_report_raw=args.check_report,
            render_report_raw=args.render_report,
            human_review_raw=args.human_review,
        )
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"PREPUBLISH REPORT: {output}")
        print(
            f"AUTOMATED RESULT: {payload['automated_result']} "
            f"| EXIT={exit_code}"
        )
        print("PUBLICATION: pending | changed=no")
        return exit_code
    except (
        ProjectConfigError,
        ModuleRegistryError,
        PrepublishError,
        ValueError,
        OSError,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_FAILED


def _checker_arguments(args: argparse.Namespace) -> list[str]:
    result: list[str] = []
    if args.staged:
        result.append("--staged")
    if args.report:
        result.extend(["--report", args.report])
    result.extend(args.paths)
    return result


def command_checker(root: Path, mode: str, args: argparse.Namespace) -> int:
    command = _script_command(
        root,
        Path("scripts/zo_check_repo.py"),
        mode,
        *_checker_arguments(args),
    )
    return _run_step(root, f"QMD {mode.upper()}", command)


def command_regression(root: Path, args: argparse.Namespace) -> int:
    try:
        articles = _regression_articles(root)
    except (ProjectConfigError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_FAILED

    for script in SELF_TEST_SCRIPTS:
        command = _script_command(root, script, "self-test")
        exit_code = _run_step(root, f"SELF-TEST {script.name}", command)
        if exit_code != EXIT_OK:
            return exit_code

    raw_articles = [item.as_posix() for item in articles]
    scope_args = ["scope", *raw_articles]
    if args.report and not args.render:
        scope_args.extend(["--report", args.report])
    scope_command = _script_command(
        root,
        Path("scripts/zo_check_repo.py"),
        *scope_args,
    )
    exit_code = _run_step(root, "REGRESSION SOURCE", scope_command)
    if exit_code != EXIT_OK:
        return exit_code

    if args.render:
        render_args = ["render", *raw_articles]
        if args.report:
            render_args.extend(["--report", args.report])
        render_command = _script_command(
            root,
            Path("scripts/zo_check_repo.py"),
            *render_args,
        )
        exit_code = _run_step(root, "REGRESSION RENDER", render_command)
        if exit_code != EXIT_OK:
            return exit_code

    print()
    print(
        "REGRESSION RESULT: PASS "
        f"| projects={len(_discover_configs(root))} "
        f"| articles={len(articles)} "
        f"| render={'yes' if args.render else 'no'}"
    )
    return EXIT_OK



def command_pack(root: Path, args: argparse.Namespace) -> int:
    package_args = [
        "pack",
        "--repo-root",
        str(root),
        "--output",
        args.output,
        "--prompt",
        args.prompt,
        "--purpose",
        args.purpose,
        "--kind",
        args.kind,
    ]
    if args.release_file:
        package_args.extend(["--release-file", args.release_file])
    if args.scope_mode:
        package_args.extend(["--scope-mode", args.scope_mode])
    for path in args.include:
        package_args.extend(["--include", path])
    if args.inside_repository_reason:
        package_args.extend(
            ["--inside-repository-reason", args.inside_repository_reason]
        )
    if args.json:
        package_args.append("--json")
    package_args.extend(args.paths)

    command = _script_command(
        root,
        Path("scripts/zo_qmd_package.py"),
        *package_args,
    )
    if args.json:
        return _run(command, root).returncode
    return _run_step(root, "QMD PACK", command)


def command_verify(args: argparse.Namespace) -> int:
    runtime_root = Path(__file__).resolve().parent.parent
    package_script = runtime_root / "scripts/zo_qmd_package.py"
    python_launcher = runtime_root / "scripts/zo_python.py"

    if not package_script.is_file():
        print(f"ERROR: Thiếu {package_script}.", file=sys.stderr)
        return EXIT_FAILED
    if not python_launcher.is_file():
        print(f"ERROR: Thiếu {python_launcher}.", file=sys.stderr)
        return EXIT_FAILED

    command = [
        sys.executable,
        str(python_launcher),
        str(package_script),
        "verify",
        args.package,
    ]
    if args.json:
        command.append("--json")

    cwd = Path.cwd()
    if not args.json:
        _print_step("QMD VERIFY", command)
    return _run(command, cwd).returncode

def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument(
        "--repo-root",
        help="Đường dẫn nằm trong repository; mặc định là thư mục hiện tại.",
    )
    result.add_argument(
        "--version",
        action="version",
        version=(
            f"%(prog)s {OPERATIONS_CLI_VERSION} "
            f"(checker {CHECKER_VERSION})"
        ),
    )

    subparsers = result.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser(
        "doctor",
        help="Kiểm tra môi trường, tệp hệ thống và đường hồi quy.",
    )
    doctor.add_argument(
        "--json",
        action="store_true",
        help="Xuất kết quả dạng JSON.",
    )

    inspect = subparsers.add_parser(
        "inspect",
        help="Nhận diện dự án, loại bài, hồ sơ và nguồn điều khiển.",
    )
    inspect.add_argument("path", help="Đường dẫn bài hoặc thư mục trong repository.")

    start = subparsers.add_parser(
        "start",
        help="Tạo hồ sơ phiên và kế hoạch sản xuất từ yêu cầu ban đầu.",
    )
    start.add_argument(
        "--output",
        help=(
            "Tệp .json đầu ra; mặc định _audit/<slug>_session.json. Nếu nằm "
            "trong repository thì phải ở dưới _audit/."
        ),
    )
    request_source = start.add_mutually_exclusive_group(required=True)
    request_source.add_argument(
        "--request",
        help="Yêu cầu ban đầu được truyền trực tiếp.",
    )
    request_source.add_argument(
        "--request-file",
        help="Tệp UTF-8 chứa nguyên văn yêu cầu ban đầu.",
    )
    start.add_argument(
        "path",
        help="Đường dẫn bài dự kiến hoặc phạm vi dự án trong repository.",
    )
    start.add_argument(
        "--allow",
        action="append",
        default=[],
        help="Đường dẫn được phép tác động thêm; có thể lặp lại.",
    )
    start.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Đường dẫn phải loại trừ; có thể lặp lại.",
    )

    visual_check = subparsers.add_parser(
        "visual-check",
        help="Tạo machine-owned mobile viewport/overflow evidence sau render.",
    )
    visual_check.add_argument("path", help="Đường dẫn bài QMD trong repository.")
    visual_check.add_argument(
        "--height",
        type=int,
        default=1000,
        help="Chiều cao viewport chụp ảnh; mặc định 1000 px.",
    )

    review_ready = subparsers.add_parser(
        "review-ready",
        help="Kiểm tra invariant bắt buộc trước khi đưa bài vào Human Review.",
    )
    review_ready.add_argument("path", help="Đường dẫn bài QMD trong repository.")
    review_ready.add_argument(
        "--report",
        help="Báo cáo JSON bên trong _audit/.",
    )
    review_ready.add_argument(
        "--session",
        help="Session manifest do start tạo; mặc định _audit/<slug>_session.json.",
    )

    prepublish = subparsers.add_parser(
        "prepublish",
        help="Tổng hợp bằng chứng và tạo báo cáo trước xuất bản.",
    )
    prepublish.add_argument(
        "--output",
        required=True,
        help=(
            "Tệp .json đầu ra tường minh; nếu nằm trong repository thì phải "
            "ở dưới _audit/."
        ),
    )
    prepublish.add_argument(
        "--session",
        required=True,
        help="Manifest JSON do lệnh start tạo.",
    )
    prepublish.add_argument(
        "--check-report",
        required=True,
        help="Báo cáo JSON của checker ở mode scope.",
    )
    prepublish.add_argument(
        "--render-report",
        required=True,
        help="Báo cáo JSON của checker ở mode render.",
    )
    prepublish.add_argument(
        "--human-review",
        required=True,
        help="Bảng kiểm JSON do người quan sát ghi nhận.",
    )
    prepublish.add_argument(
        "path",
        help="Đường dẫn bài QMD trong repository.",
    )

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--staged", action="store_true", help="Kiểm tra vùng staged.")
    common.add_argument("--report", help="Báo cáo JSON bên trong _audit/.")
    common.add_argument("paths", nargs="+", help="Phạm vi tường minh.")

    subparsers.add_parser(
        "check",
        parents=[common],
        help="Điều phối kiểm định nguồn qua checker hiện hành.",
    )
    subparsers.add_parser(
        "render",
        parents=[common],
        help="Điều phối kiểm định nguồn, render và kiểm định đầu ra.",
    )

    regression = subparsers.add_parser(
        "regression",
        help="Chạy self-test và đường cơ sở các dự án đã cấu hình.",
    )
    regression.add_argument(
        "--render",
        action="store_true",
        help="Chạy thêm hồi quy render sau hồi quy nguồn.",
    )
    regression.add_argument(
        "--report",
        help="Báo cáo JSON bên trong _audit/ cho bước checker cuối.",
    )


    pack = subparsers.add_parser(
        "pack",
        help="Tạo gói context hoặc release tại đầu ra tường minh.",
    )
    pack.add_argument(
        "--output",
        required=True,
        help="Thư mục gói hoặc tệp .zip đầu ra; không có giá trị mặc định.",
    )
    pack.add_argument(
        "--prompt",
        required=True,
        help="Tệp Markdown dùng làm PROMPT.md.",
    )
    pack.add_argument(
        "--purpose",
        required=True,
        help="Mục đích ngắn của gói.",
    )
    pack.add_argument(
        "--kind",
        choices=("context", "release"),
        default="context",
        help="Loại gói; mặc định là context để giữ tương thích O2.",
    )
    pack.add_argument(
        "--release-file",
        help="Hồ sơ YAML bắt buộc khi --kind release.",
    )
    pack.add_argument(
        "--scope-mode",
        help="Nhãn chế độ phạm vi; mặc định được suy ra.",
    )
    pack.add_argument(
        "--include",
        action="append",
        default=[],
        help="Đường dẫn hỗ trợ cần thêm; có thể lặp lại.",
    )
    pack.add_argument(
        "--inside-repository-reason",
        help="Lí do bắt buộc nếu đầu ra nằm trong repository.",
    )
    pack.add_argument(
        "--json",
        action="store_true",
        help="Xuất kết quả dạng JSON.",
    )
    pack.add_argument(
        "paths",
        nargs="+",
        help="Các gốc phạm vi tường minh trong repository.",
    )

    verify = subparsers.add_parser(
        "verify",
        help="Xác minh thư mục gói hoặc tệp .zip chuẩn.",
    )
    verify.add_argument("package", help="Đường dẫn thư mục gói hoặc tệp .zip.")
    verify.add_argument(
        "--json",
        action="store_true",
        help="Xuất kết quả dạng JSON.",
    )

    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)

    if args.command == "verify":
        return command_verify(args)

    root, exit_code, message = _repo_root(args.repo_root)
    if root is None:
        print(f"ERROR: {message}", file=sys.stderr)
        return exit_code

    os.chdir(root)

    if args.command == "doctor":
        return command_doctor(root, args)
    if args.command == "inspect":
        return command_inspect(root, args)
    if args.command == "start":
        return command_start(root, args)
    if args.command == "visual-check":
        return command_visual_check(root, args)
    if args.command == "review-ready":
        return command_review_ready(root, args)
    if args.command == "prepublish":
        return command_prepublish(root, args)
    if args.command == "check":
        return command_checker(root, "scope", args)
    if args.command == "render":
        return command_checker(root, "render", args)
    if args.command == "regression":
        return command_regression(root, args)
    if args.command == "pack":
        return command_pack(root, args)

    print(f"ERROR: Lệnh chưa được hỗ trợ: {args.command}", file=sys.stderr)
    return EXIT_USAGE


if __name__ == "__main__":
    raise SystemExit(main())

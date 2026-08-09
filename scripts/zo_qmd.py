"""Unified operations front end for the ZO Math QMD system.

This command coordinates the existing configuration loader, registry, checker,
Quarto wrapper, regression baseline, and package module. It does not duplicate
validators and does not accept, publish, stage, or commit content.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Sequence

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
from zo_qmd_sources import (
    AuthoritySourceError,
    authority_manifest,
    provenance_manifest,
)
from zo_qmd_version import OPERATIONS_CLI_VERSION

EXIT_OK = 0
EXIT_FAILED = 1
EXIT_USAGE = 2
EXIT_MISSING_TOOL = 3

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
    Path("scripts/zo_qmd_sources.py"),
    Path("scripts/zo_qmd_version.py"),
    Path("scripts/zo_qmd_prepublish.py"),
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
    Path("scripts/zo_qmd_sources.py"),
    Path("scripts/zo_qmd_version.py"),
    Path("scripts/zo_qmd_prepublish.py"),
)

REGRESSION_ALLOWED_ROOTS = {"_audit", ".quarto", "_freeze", "docs"}
REGRESSION_ALLOWED_CACHE_DIRS = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
}


def _filesystem_inventory(root: Path) -> set[Path]:
    inventory: set[Path] = set()
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if relative.parts and relative.parts[0] == ".git":
            continue
        inventory.add(relative)
    return inventory


def _regression_hygiene_violations(
    before: set[Path],
    after: set[Path],
    *,
    exact_outputs: Sequence[Path] = (),
    allowed_trees: Sequence[Path] = (),
) -> list[Path]:
    exact = {Path(path) for path in exact_outputs}
    trees = tuple(Path(path) for path in allowed_trees)
    violations: list[Path] = []
    for relative in sorted(after - before, key=lambda item: item.as_posix()):
        if not relative.parts:
            continue
        if relative in exact:
            continue
        if any(output in relative.parents for output in exact):
            violations.append(relative)
            continue
        if relative.parts[0] in REGRESSION_ALLOWED_ROOTS:
            continue
        if any(part in REGRESSION_ALLOWED_CACHE_DIRS for part in relative.parts):
            continue
        if any(relative == tree or tree in relative.parents for tree in trees):
            continue
        violations.append(relative)
    return violations


def _regression_declared_outputs(
    root: Path,
    articles: Sequence[Path],
    report: str | None,
) -> tuple[list[Path], list[Path]]:
    exact_outputs: list[Path] = []
    allowed_trees: list[Path] = []
    for article in articles:
        exact_outputs.extend(
            (
                article.with_suffix(".html"),
                article.with_suffix(".pdf"),
            )
        )
        allowed_trees.append(article.parent / f"{article.stem}_files")
    if report:
        report_path = _explicit_output_path(root, report)
        try:
            exact_outputs.append(report_path.relative_to(root))
        except ValueError:
            pass
    return exact_outputs, allowed_trees


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

    authority_sources = authority_manifest(
        root,
        relative,
        config=config,
    )
    provenance = (
        provenance_manifest(root, config.profile_path_for(relative))
        if article_type is not None
        else None
    )

    payload: dict[str, Any] = {
        "operations_cli_version": OPERATIONS_CLI_VERSION,
        "checker_version": CHECKER_VERSION,
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
        "authority_sources": authority_sources,
        "provenance": provenance,
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

    missing_authority = authority_sources.get("missing_required", [])
    if missing_authority:
        payload["error"] = (
            "Thiếu nguồn có thẩm quyền bắt buộc: "
            + ", ".join(str(item) for item in missing_authority)
        )
        exit_code = EXIT_FAILED

    if isinstance(provenance, dict) and provenance.get("blocked"):
        payload["error"] = "Provenance của nguồn đã dùng bị mismatch hoặc missing."
        exit_code = EXIT_FAILED

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
    except (
        AuthoritySourceError,
        ProjectConfigError,
        ModuleRegistryError,
        ValueError,
        OSError,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_FAILED


def command_start(root: Path, args: argparse.Namespace) -> int:
    try:
        request = _read_request(args)
        output = _explicit_output_path(root, args.output)
        if output.suffix.lower() != ".json":
            raise ValueError("Hồ sơ phiên của start phải là tệp .json.")
        if output.exists():
            raise ValueError(f"Đầu ra đã tồn tại: {output}")

        summary, inspect_exit = _project_summary(root, args.path)
        snapshot = _git_snapshot(root)

        reference_groups = summary.get("references", {})
        authority_sources = summary.get("authority_sources", {})
        expected_authority_fingerprint = str(
            authority_sources.get("fingerprint", "")
        )
        provided_authority_fingerprint = (
            args.authority_ack.strip()
            if isinstance(args.authority_ack, str)
            else ""
        )

        blocked_reasons: list[str] = []
        if inspect_exit != EXIT_OK:
            blocked_reasons.append(
                str(summary.get("error", "Inspect không đạt."))
            )

        if not provided_authority_fingerprint:
            blocked_reasons.append(
                "Chưa có xác nhận của agent rằng đã hoàn tất các hành động "
                "read/observe cho tập nguồn có thẩm quyền bắt buộc."
            )
        elif provided_authority_fingerprint != expected_authority_fingerprint:
            blocked_reasons.append(
                "Fingerprint xác nhận nguồn có thẩm quyền không khớp "
                "fingerprint hiện hành từ inspect."
            )

        target = str(summary["target"])
        project_root = str(summary["project"]["root"])
        allowed_paths = [_relative_to_root(root, target)]
        profile = summary.get("profile")
        if isinstance(profile, dict) and profile.get("path"):
            allowed_paths.append(_relative_to_root(root, str(profile["path"])))
        allowed_paths.extend(_relative_to_root(root, raw) for raw in args.allow)
        excluded_paths = [
            _relative_to_root(root, raw) for raw in args.exclude
        ]
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

        payload: dict[str, Any] = {
            "session_manifest_version": 2,
            "session_id": str(uuid.uuid4()),
            "created_at": datetime.now(timezone.utc).isoformat().replace(
                "+00:00", "Z"
            ),
            "operations_cli_version": OPERATIONS_CLI_VERSION,
            "checker_version": CHECKER_VERSION,
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
                "agents_chain": list(summary.get("agents_chain", [])),
                "project_config": summary["project"]["config_path"],
                "references": reference_groups,
                "discovered": authority_sources,
                "acknowledgement": {
                    "required_fingerprint": expected_authority_fingerprint,
                    "provided_fingerprint": (
                        provided_authority_fingerprint or None
                    ),
                    "matches_current": (
                        bool(provided_authority_fingerprint)
                        and provided_authority_fingerprint
                        == expected_authority_fingerprint
                    ),
                    "status": (
                        "locked"
                        if (
                            provided_authority_fingerprint
                            and provided_authority_fingerprint
                            == expected_authority_fingerprint
                        )
                        else "blocked"
                    ),
                },
            },
            "scope": {
                "target": target,
                "project_root": project_root,
                "allowed": allowed,
                "excluded": excluded,
            },
            "plan": {
                "objective": request,
                "expected_files": allowed,
                "phases": [
                    "lock_authority_sources",
                    "create_or_edit_qmd_and_resources",
                    "check_source",
                    "render",
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
                        f"check --session {output} {target}"
                    ),
                    "render": (
                        "python scripts/zo_python.py scripts/zo_qmd.py "
                        f"render --session {output} {target}"
                    ),
                },
                "user_gates": [
                    "human_review",
                    "publication_confirmation",
                ],
                "stop_conditions": [
                    "missing_authority_source",
                    "authority_sources_not_acknowledged",
                    "automated_check_failure",
                    "render_failure",
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
        print(
            f"AUTOMATED RESULT: {payload['automated_result']} "
            f"| EXIT={payload['exit_code']}"
        )
        return int(payload["exit_code"])
    except (
        AuthoritySourceError,
        ProjectConfigError,
        ModuleRegistryError,
        ValueError,
        OSError,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_FAILED


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


def _checker_arguments(root: Path, args: argparse.Namespace) -> list[str]:
    result: list[str] = []
    if args.staged:
        result.append("--staged")
    if args.report:
        result.extend(["--report", args.report])
    if args.session:
        session_path = Path(args.session).expanduser()
        if not session_path.is_absolute():
            session_path = root / session_path
        session = json.loads(session_path.read_text(encoding="utf-8"))
        if not isinstance(session, dict):
            raise ValueError("Manifest phiên phải là JSON object.")
        if session.get("session_manifest_version") != 2:
            raise ValueError("Evidence production yêu cầu session_manifest_version=2.")
        session_id = session.get("session_id")
        if not isinstance(session_id, str) or not session_id.strip():
            raise ValueError("Manifest phiên thiếu session_id.")
        session_target = session.get("scope", {}).get("target")
        targets = [_relative_to_root(root, raw).as_posix() for raw in args.paths]
        if len(targets) != 1 or session_target != targets[0]:
            raise ValueError("Manifest phiên không khớp đúng một target check/render.")
        result.extend(["--session-id", session_id.strip()])
    result.extend(args.paths)
    return result


def command_checker(root: Path, mode: str, args: argparse.Namespace) -> int:
    try:
        command = _script_command(
            root,
            Path("scripts/zo_check_repo.py"),
            mode,
            *_checker_arguments(root, args),
        )
        return _run_step(root, f"QMD {mode.upper()}", command)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_FAILED


def _run_regression_steps(
    root: Path,
    args: argparse.Namespace,
) -> tuple[int, list[Path]]:
    try:
        articles = _regression_articles(root)
    except (ProjectConfigError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_FAILED, []

    exit_code = _self_test_regression_hygiene()

    if exit_code == EXIT_OK:
        for script in SELF_TEST_SCRIPTS:
            command = _script_command(root, script, "self-test")
            exit_code = _run_step(root, f"SELF-TEST {script.name}", command)
            if exit_code != EXIT_OK:
                break

    raw_articles = [item.as_posix() for item in articles]
    if exit_code == EXIT_OK:
        scope_args = ["scope", *raw_articles]
        if args.report and not args.render:
            scope_args.extend(["--report", args.report])
        scope_command = _script_command(
            root,
            Path("scripts/zo_check_repo.py"),
            *scope_args,
        )
        exit_code = _run_step(root, "REGRESSION SOURCE", scope_command)

    if exit_code == EXIT_OK and args.render:
        render_args = ["render", *raw_articles]
        if args.report:
            render_args.extend(["--report", args.report])
        render_command = _script_command(
            root,
            Path("scripts/zo_check_repo.py"),
            *render_args,
        )
        exit_code = _run_step(root, "REGRESSION RENDER", render_command)

    return exit_code, articles


def command_regression(
    root: Path,
    args: argparse.Namespace,
    *,
    step_runner: Callable[
        [Path, argparse.Namespace], tuple[int, list[Path]]
    ] = _run_regression_steps,
) -> int:
    before = _filesystem_inventory(root)
    articles: list[Path] = []
    exit_code = EXIT_OK
    violations: list[Path] = []
    failure: dict[str, Any] | None = None
    hygiene_error: str | None = None
    try:
        exit_code, articles = step_runner(root, args)
        if exit_code != EXIT_OK:
            failure = {
                "type": "step_exit",
                "exit_code": exit_code,
            }
    except Exception as exc:
        failure = {
            "type": type(exc).__name__,
            "message": str(exc),
        }
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        exit_code = EXIT_FAILED
    finally:
        try:
            exact_outputs, allowed_trees = _regression_declared_outputs(
                root,
                articles,
                args.report,
            )
            violations = _regression_hygiene_violations(
                before,
                _filesystem_inventory(root),
                exact_outputs=exact_outputs,
                allowed_trees=allowed_trees,
            )
        except (OSError, ValueError) as exc:
            hygiene_error = str(exc)
            print(f"ERROR: Hygiene classification: {exc}", file=sys.stderr)
            exit_code = EXIT_FAILED

    if violations:
        exit_code = EXIT_FAILED
    hygiene_status = "ERROR" if hygiene_error else ("FAIL" if violations else "PASS")
    print()
    print(
        json.dumps(
            {
                "automated_result": (
                    "FAIL" if exit_code != EXIT_OK else "PASS"
                ),
                "regression_failure": failure,
                "hygiene": {
                    "status": hygiene_status,
                    "unexpected_new_paths": [
                        path.as_posix() for path in violations
                    ],
                    "error": hygiene_error,
                },
            },
            ensure_ascii=False,
            indent=2,
        )
    )

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


def _self_test_regression_hygiene() -> int:
    import contextlib
    import io
    import tempfile

    with tempfile.TemporaryDirectory(prefix="zo-qmd-hygiene-self-test-") as raw:
        root = Path(raw)
        (root / "content/existing").mkdir(parents=True)
        (root / "content/existing/article.qmd").write_text(
            "existing\n", encoding="utf-8"
        )
        (root / "content/demo").mkdir()
        (root / "pre-existing-root.tmp").write_text(
            "existing\n", encoding="utf-8"
        )
        before = _filesystem_inventory(root)

        (root / "_audit").mkdir()
        (root / "_audit/evidence.json").write_text("{}\n", encoding="utf-8")
        (root / "docs").mkdir()
        (root / "docs/article.html").write_text("output\n", encoding="utf-8")
        (root / ".quarto/cache").mkdir(parents=True)
        (root / ".quarto/cache/state").write_text("cache\n", encoding="utf-8")
        (root / "_freeze/article").mkdir(parents=True)
        (root / "_freeze/article/output.json").write_text(
            "{}\n", encoding="utf-8"
        )
        (root / "content/demo/__pycache__").mkdir(parents=True)
        (root / "content/demo/__pycache__/module.pyc").write_bytes(b"cache")
        allowed = _regression_hygiene_violations(
            before,
            _filesystem_inventory(root),
        )
        if allowed:
            print(
                "Regression hygiene self-test quy lỗi path hợp lệ: "
                + ", ".join(path.as_posix() for path in allowed),
                file=sys.stderr,
            )
            return EXIT_FAILED

        exact_outputs = (
            Path("_audit/regression-report.json"),
            Path("content/demo/article.html"),
            Path("content/demo/article.pdf"),
        )
        allowed_trees = (Path("content/demo/article_files"),)
        declared_after = {
            *exact_outputs,
            Path("_audit/regression-report.json/child.tmp"),
            Path("content/demo/article.html/child.tmp"),
            Path("content/demo/article.pdf/child.tmp"),
            Path("content/demo/article_files"),
            Path("content/demo/article_files/figure.png"),
        }
        declared_violations = _regression_hygiene_violations(
            set(),
            declared_after,
            exact_outputs=exact_outputs,
            allowed_trees=allowed_trees,
        )
        declared_actual = [path.as_posix() for path in declared_violations]
        declared_expected = [
            "_audit/regression-report.json/child.tmp",
            "content/demo/article.html/child.tmp",
            "content/demo/article.pdf/child.tmp",
        ]
        if declared_actual != declared_expected:
            print(
                "Regression hygiene self-test phân loại sai exact/tree: "
                + json.dumps(declared_actual, ensure_ascii=False),
                file=sys.stderr,
            )
            return EXIT_FAILED

        (root / "probe.tmp").write_text("helper\n", encoding="utf-8")
        (root / "empty-root-helper").mkdir()
        (root / "content/scratch").mkdir(parents=True)
        (root / "content/scratch/helper.tmp").write_text(
            "helper\n", encoding="utf-8"
        )
        violations = _regression_hygiene_violations(
            before,
            _filesystem_inventory(root),
        )
        actual = [path.as_posix() for path in violations]
        expected = [
            "content/scratch",
            "content/scratch/helper.tmp",
            "empty-root-helper",
            "probe.tmp",
        ]
        if actual != expected:
            print(
                "Regression hygiene self-test báo sai path: "
                + json.dumps(actual, ensure_ascii=False),
                file=sys.stderr,
            )
            return EXIT_FAILED

        failure_root = root / "failure-fixture"
        failure_root.mkdir()

        def injected_failure(
            injected_root: Path,
            _args: argparse.Namespace,
        ) -> tuple[int, list[Path]]:
            (injected_root / "unexpected-helper.tmp").write_text(
                "helper\n", encoding="utf-8"
            )
            raise RuntimeError("injected regression failure")

        captured_stdout = io.StringIO()
        captured_stderr = io.StringIO()
        failure_args = argparse.Namespace(report=None, render=False)
        with contextlib.redirect_stdout(captured_stdout), contextlib.redirect_stderr(
            captured_stderr
        ):
            failure_exit = command_regression(
                failure_root,
                failure_args,
                step_runner=injected_failure,
            )
        failure_payload = json.loads(captured_stdout.getvalue())
        if (
            failure_exit != EXIT_FAILED
            or failure_payload.get("regression_failure", {}).get("type")
            != "RuntimeError"
            or failure_payload.get("hygiene", {}).get("unexpected_new_paths")
            != ["unexpected-helper.tmp"]
            or "injected regression failure" not in captured_stderr.getvalue()
            or not (failure_root / "unexpected-helper.tmp").is_file()
        ):
            print(
                "Regression hygiene self-test không giữ đủ failure/evidence.",
                file=sys.stderr,
            )
            return EXIT_FAILED

    print("PASS: zo_qmd regression hygiene self-test")
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
        required=True,
        help=(
            "Tệp .json đầu ra tường minh; nếu nằm trong repository thì phải "
            "ở dưới _audit/."
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
        "--authority-ack",
        help=(
            "Fingerprint authority_sources từ inspect. Truyền giá trị này là "
            "xác nhận tường minh của agent rằng đã hoàn tất các hành động "
            "read/observe cho toàn bộ nguồn bắt buộc của fingerprint đó."
        ),
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
    common.add_argument(
        "--session",
        help=(
            "Manifest session version 2 do start tạo. Không bắt buộc cho kiểm tra "
            "độc lập; bắt buộc nếu report sẽ dùng cho prepublish."
        ),
    )
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

    subparsers.add_parser(
        "self-test",
        help="Chạy self-test thuần của lớp vận hành.",
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
    if args.command == "prepublish":
        return command_prepublish(root, args)
    if args.command == "check":
        return command_checker(root, "scope", args)
    if args.command == "render":
        return command_checker(root, "render", args)
    if args.command == "regression":
        return command_regression(root, args)
    if args.command == "self-test":
        return _self_test_regression_hygiene()
    if args.command == "pack":
        return command_pack(root, args)

    print(f"ERROR: Lệnh chưa được hỗ trợ: {args.command}", file=sys.stderr)
    return EXIT_USAGE


if __name__ == "__main__":
    raise SystemExit(main())

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


OPERATIONS_CLI_VERSION = "0.3.0"

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
    Path("scripts/zo_check_repo.py"),
    Path("scripts/zo_qmd_config.py"),
    Path("scripts/zo_qmd_registry.py"),
    Path("scripts/zo_qmd_core.py"),
    Path("scripts/zo_real_world_problem.py"),
)

SELF_TEST_SCRIPTS = (
    Path("scripts/zo_qmd_config.py"),
    Path("scripts/zo_qmd_registry.py"),
    Path("scripts/zo_qmd_core.py"),
    Path("scripts/zo_real_world_problem.py"),
    Path("scripts/zo_qmd_package.py"),
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
        },
        "publication": config.raw.get("publication", {}),
    }

    exit_code = EXIT_OK
    if relative.suffix.lower() == ".qmd" and article_type is None:
        payload["error"] = "Tệp QMD không khớp loại bài nào trong cấu hình dự án."
        exit_code = EXIT_FAILED
    elif profile and profile["required"] and not profile["exists"]:
        payload["error"] = "Thiếu hồ sơ bắt buộc của bài."
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

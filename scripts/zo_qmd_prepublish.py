"""Build a prepublication evidence report without accepting or publishing content."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from zo_check_repo import CHECKER_VERSION


PREPUBLISH_REPORT_VERSION = 1
EXIT_OK = 0
EXIT_FAILED = 1


class PrepublishError(RuntimeError):
    """Raised when prepublish evidence cannot be read or reconciled."""


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
    )


def _load_json(raw: str, label: str) -> tuple[Path, dict[str, Any]]:
    path = Path(raw).expanduser().resolve()
    if not path.is_file():
        raise PrepublishError(f"{label} không tồn tại: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise PrepublishError(f"Không đọc được {label}: {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise PrepublishError(f"{label} phải là một JSON object: {path}")
    return path, payload


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _evidence_record(path: Path, payload: dict[str, Any]) -> dict[str, Any]:
    summary_keys = (
        "session_manifest_version",
        "review_manifest_version",
        "checker_version",
        "mode",
        "automated_result",
        "final_acceptance",
        "exit_code",
        "result",
    )
    return {
        "path": str(path),
        "sha256": _sha256(path),
        "size": path.stat().st_size,
        "summary": {
            key: payload[key] for key in summary_keys if key in payload
        },
    }


def _git_read(root: Path, *arguments: str) -> str:
    git = shutil.which("git")
    if git is None:
        raise PrepublishError("Không tìm thấy git trong PATH.")
    result = _run([git, "-C", str(root), *arguments], root)
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip()
        raise PrepublishError(
            message or f"Git thất bại: {' '.join(arguments)}"
        )
    return result.stdout


def git_snapshot(root: Path) -> dict[str, Any]:
    status = _git_read(root, "status", "--short").strip()
    branch = _git_read(root, "branch", "--show-current").strip()
    commit = _git_read(root, "rev-parse", "HEAD").strip()
    return {
        "branch": branch or None,
        "commit": commit,
        "clean": not bool(status),
        "status": status.splitlines(),
    }


def git_changes_since(root: Path, base_commit: str) -> list[dict[str, str]]:
    _git_read(root, "cat-file", "-e", f"{base_commit}^{{commit}}")
    changes: dict[str, dict[str, str]] = {}

    tracked = _git_read(
        root,
        "diff",
        "--name-status",
        "--find-renames",
        base_commit,
        "--",
    )
    for line in tracked.splitlines():
        fields = line.split("\t")
        if len(fields) < 2:
            continue
        path = fields[-1].replace("\\", "/")
        changes[path] = {
            "status": fields[0],
            "path": path,
            "source": "git-diff",
        }

    untracked = _git_read(root, "ls-files", "--others", "--exclude-standard")
    for line in untracked.splitlines():
        path = line.strip().replace("\\", "/")
        if path:
            changes[path] = {
                "status": "??",
                "path": path,
                "source": "untracked",
            }

    return [changes[path] for path in sorted(changes)]


def _inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _overlap(left: Path, right: Path) -> bool:
    return _inside(left, right) or _inside(right, left)


def _checker_evidence_errors(
    report: dict[str, Any],
    *,
    label: str,
    expected_mode: str,
    target: str,
) -> list[str]:
    errors: list[str] = []
    valid_results = {"PASS", "PASS_WITH_WARNINGS"}
    scope = report.get("scope", [])

    if report.get("mode") != expected_mode:
        errors.append(f"Báo cáo {label} không có mode={expected_mode!r}.")
    if report.get("checker_version") != CHECKER_VERSION:
        errors.append(
            f"Báo cáo {label} không dùng checker {CHECKER_VERSION}."
        )
    if report.get("automated_result") not in valid_results:
        errors.append(f"Báo cáo {label} không đạt PASS/PASS_WITH_WARNINGS.")
    if report.get("exit_code") != EXIT_OK:
        errors.append(f"Báo cáo {label} không có exit_code=0.")
    if report.get("final_acceptance") != "NOT_RUN":
        errors.append(f"Báo cáo {label} đã vượt thẩm quyền tự động.")
    if not isinstance(scope, list) or target not in scope:
        errors.append(f"Báo cáo {label} không bao phủ đích {target}.")
    return errors


def build_report(
    *,
    root: Path,
    target: str,
    operations_cli_version: str,
    project_summary: dict[str, Any],
    inspect_exit: int,
    session_raw: str,
    check_report_raw: str,
    render_report_raw: str,
    human_review_raw: str,
) -> tuple[dict[str, Any], int]:
    session_path, session = _load_json(session_raw, "manifest phiên start")
    check_path, check_report = _load_json(check_report_raw, "báo cáo check")
    render_path, render_report = _load_json(
        render_report_raw, "báo cáo render"
    )
    review_path, review = _load_json(
        human_review_raw, "bảng kiểm có người quan sát"
    )

    blocked: list[str] = []
    session_scope = session.get("scope", {})
    session_status = session.get("status", {})
    session_repository = session.get("repository", {})

    if session.get("session_manifest_version") != 1:
        blocked.append("Manifest phiên không dùng session_manifest_version=1.")
    if session.get("automated_result") != "PASS":
        blocked.append("Manifest phiên start không đạt PASS.")
    if not isinstance(session_scope, dict) or session_scope.get("target") != target:
        blocked.append("Đích trong manifest phiên không khớp đích prepublish.")
    if (
        not isinstance(session_status, dict)
        or session_status.get("publication") != "pending"
    ):
        blocked.append("Manifest phiên không khóa publication=pending.")

    blocked.extend(
        _checker_evidence_errors(
            check_report,
            label="check",
            expected_mode="scope",
            target=target,
        )
    )
    blocked.extend(
        _checker_evidence_errors(
            render_report,
            label="render",
            expected_mode="render",
            target=target,
        )
    )

    review_result = str(review.get("result", "NOT_RUN")).upper()
    production_status = review.get("production_status")
    publication_status = review.get("publication_status")
    review_checks = review.get("checks", [])
    remaining_issues = review.get("remaining_issues", [])
    pending_decisions = review.get("pending_user_decisions", [])
    production_states = project_summary.get("publication", {}).get(
        "production_states", []
    )

    if review.get("review_manifest_version") != 1:
        blocked.append("Bảng kiểm không dùng review_manifest_version=1.")
    if review.get("target") != target:
        blocked.append("Đích trong bảng kiểm có người quan sát không khớp.")
    if not review.get("reviewed_at"):
        blocked.append("Bảng kiểm thiếu reviewed_at.")
    if not review.get("reviewer"):
        blocked.append("Bảng kiểm thiếu reviewer.")
    if review_result != "PASS":
        blocked.append("Kiểm định có người quan sát chưa PASS.")
    if not isinstance(review_checks, list) or not review_checks:
        blocked.append("Bảng kiểm có người quan sát không có checks.")
    if not isinstance(remaining_issues, list):
        blocked.append("remaining_issues phải là một danh sách.")
        remaining_issues = []
    elif remaining_issues:
        blocked.append("Kiểm định có người quan sát còn vấn đề chưa xử lí.")
    if production_status not in production_states:
        blocked.append("production_status không thuộc trạng thái của dự án.")
    elif production_status != "accepted":
        blocked.append("Bài chưa ở production_status=accepted.")
    if publication_status != "pending":
        blocked.append("Bảng kiểm phải giữ publication_status=pending.")
    if not isinstance(pending_decisions, list):
        blocked.append("pending_user_decisions phải là một danh sách.")
        pending_decisions = []
    if inspect_exit != EXIT_OK:
        blocked.append("Inspect hiện tại không đạt.")

    base_commit = (
        session_repository.get("commit")
        if isinstance(session_repository, dict)
        else None
    )
    if not base_commit:
        blocked.append("Manifest phiên thiếu repository.commit.")
        changes: list[dict[str, str]] = []
    else:
        changes = git_changes_since(root, str(base_commit))

    evidence_changes = [
        item
        for item in changes
        if item["path"] == "_audit" or item["path"].startswith("_audit/")
    ]
    affected_files = [item for item in changes if item not in evidence_changes]

    allowed_raw = (
        session_scope.get("allowed", []) if isinstance(session_scope, dict) else []
    )
    excluded_raw = (
        session_scope.get("excluded", [])
        if isinstance(session_scope, dict)
        else []
    )
    allowed = [Path(item) for item in allowed_raw if isinstance(item, str)]
    excluded = [Path(item) for item in excluded_raw if isinstance(item, str)]
    outside_scope: list[str] = []
    excluded_touched: list[str] = []

    for item in affected_files:
        changed = Path(item["path"])
        if not any(_inside(changed, parent) for parent in allowed):
            outside_scope.append(changed.as_posix())
        if any(_overlap(changed, parent) for parent in excluded):
            excluded_touched.append(changed.as_posix())

    if outside_scope:
        blocked.append(
            "Tệp thay đổi ngoài phạm vi được phép: "
            + ", ".join(sorted(outside_scope))
        )
    if excluded_touched:
        blocked.append(
            "Tệp thuộc phạm vi loại trừ đã bị tác động: "
            + ", ".join(sorted(excluded_touched))
        )

    decisions = [item for item in pending_decisions if isinstance(item, str)]
    if "publication_confirmation" not in decisions:
        decisions.append("publication_confirmation")

    expected_commands = session.get("plan", {}).get("expected_commands", {})
    exit_code = EXIT_FAILED if blocked else EXIT_OK
    payload: dict[str, Any] = {
        "prepublish_report_version": PREPUBLISH_REPORT_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat().replace(
            "+00:00", "Z"
        ),
        "operations_cli_version": operations_cli_version,
        "checker_version": CHECKER_VERSION,
        "target": target,
        "snapshot": {
            "session_start": session_repository,
            "current": git_snapshot(root),
        },
        "scope": {
            "allowed": allowed_raw,
            "excluded": excluded_raw,
            "affected_files": affected_files,
            "evidence_files_in_audit": evidence_changes,
            "outside_scope": sorted(outside_scope),
            "excluded_touched": sorted(excluded_touched),
        },
        "authority_sources": session.get("authority_sources", {}),
        "project": project_summary.get("project", {}),
        "article_type": project_summary.get("article_type"),
        "profile": project_summary.get("profile"),
        "evidence": {
            "session": _evidence_record(session_path, session),
            "check": _evidence_record(check_path, check_report),
            "render": _evidence_record(render_path, render_report),
            "human_review": _evidence_record(review_path, review),
        },
        "commands": {
            "expected": expected_commands,
            "results": [
                {
                    "phase": "check",
                    "mode": check_report.get("mode"),
                    "exit_code": check_report.get("exit_code"),
                    "automated_result": check_report.get("automated_result"),
                },
                {
                    "phase": "render",
                    "mode": render_report.get("mode"),
                    "exit_code": render_report.get("exit_code"),
                    "automated_result": render_report.get("automated_result"),
                },
            ],
        },
        "validation": {
            "source": check_report.get("automated_result"),
            "render": render_report.get("automated_result"),
            "human_review": review_result,
            "final_acceptance": {
                "result": review_result,
                "source": "human_review_evidence",
                "decided_by_prepublish": False,
            },
        },
        "status": {
            "production": production_status,
            "publication": "pending",
            "prepublish": "blocked" if blocked else "ready_for_user_decision",
        },
        "remaining_issues": remaining_issues,
        "blocked_reasons": blocked,
        "pending_user_decisions": decisions,
        "publication": {
            "status": "pending",
            "changed_by_command": False,
            "requires_separate_user_confirmation": True,
        },
        "limitations": [
            "Báo cáo chỉ tổng hợp bằng chứng; không chạy lại checker hoặc render.",
            "Báo cáo không tự nghiệm thu và không xuất bản.",
            "Độ mới của mọi tài nguyên phụ chưa thể suy ra chỉ từ báo cáo checker hiện hành.",
        ],
        "automated_result": "FAIL" if blocked else "PASS",
        "exit_code": exit_code,
    }
    return payload, exit_code


def self_test() -> int:
    target = "content/example/core/sample.qmd"
    valid = {
        "checker_version": CHECKER_VERSION,
        "mode": "scope",
        "automated_result": "PASS_WITH_WARNINGS",
        "final_acceptance": "NOT_RUN",
        "scope": [target],
        "exit_code": 0,
    }
    if _checker_evidence_errors(
        valid,
        label="check",
        expected_mode="scope",
        target=target,
    ):
        print("FAIL: valid checker evidence was rejected.")
        return EXIT_FAILED

    invalid = dict(valid)
    invalid["final_acceptance"] = "PASS"
    errors = _checker_evidence_errors(
        invalid,
        label="check",
        expected_mode="scope",
        target=target,
    )
    if not any("thẩm quyền" in item for item in errors):
        print("FAIL: automated acceptance was not rejected.")
        return EXIT_FAILED

    print("PASS: zo_qmd_prepublish self-test")
    return EXIT_OK


if __name__ == "__main__":
    if len(__import__("sys").argv) == 2 and __import__("sys").argv[1] == "self-test":
        raise SystemExit(self_test())
    print("Usage: zo_qmd_prepublish.py self-test")
    raise SystemExit(2)

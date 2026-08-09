"""Build a prepublication evidence report without accepting or publishing content."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from zo_check_repo import CHECKER_VERSION


PREPUBLISH_REPORT_VERSION = 2
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


def _valid_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value.lower())
    )


def _evidence_record(path: Path, payload: dict[str, Any]) -> dict[str, Any]:
    summary_keys = (
        "evidence_report_version",
        "session_manifest_version",
        "review_manifest_version",
        "session_id",
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
    if report.get("evidence_report_version") != 1:
        errors.append(f"Báo cáo {label} không dùng evidence_report_version=1.")
    if report.get("target") != target:
        errors.append(f"Báo cáo {label} không gắn đúng target {target}.")
    return errors


def _parse_timestamp(value: Any, label: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} thiếu timestamp hợp lệ.")
        return None
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{label} có timestamp không hợp lệ.")
        return None
    if parsed.tzinfo is None:
        errors.append(f"{label} phải dùng timestamp có timezone.")
        return None
    return parsed


def _repo_file(root: Path, raw: Any, label: str, errors: list[str]) -> Path | None:
    if not isinstance(raw, str) or not raw.strip():
        errors.append(f"{label} thiếu path hợp lệ.")
        return None
    candidate = Path(raw.strip())
    if candidate.is_absolute():
        errors.append(f"{label} phải là đường dẫn tương đối repository.")
        return None
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        errors.append(f"{label} nằm ngoài repository.")
        return None
    return resolved


def _evidence_chain_errors(
    root: Path,
    target: str,
    session: dict[str, Any],
    check_report: dict[str, Any],
    render_report: dict[str, Any],
    review: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    if session.get("session_manifest_version") != 2:
        errors.append("Manifest phiên không dùng session_manifest_version=2.")
    session_scope = session.get("scope")
    if not isinstance(session_scope, dict) or session_scope.get("target") != target:
        errors.append("Target của manifest phiên không khớp target prepublish.")
    session_id = session.get("session_id")
    if not isinstance(session_id, str) or not session_id.strip():
        errors.append("Manifest phiên thiếu session_id.")
        session_id = None

    for label, evidence in (
        ("check", check_report),
        ("render", render_report),
        ("human review", review),
    ):
        if evidence.get("session_id") != session_id:
            errors.append(f"session_id của {label} không khớp manifest phiên.")
        if evidence.get("target") != target:
            errors.append(f"Target của {label} không khớp target prepublish.")

    target_path = _repo_file(root, target, "Target prepublish", errors)
    current_target_sha = (
        _sha256(target_path)
        if target_path is not None and target_path.is_file()
        else None
    )
    if current_target_sha is None:
        errors.append("Target prepublish không tồn tại để kiểm tra freshness.")
    evidence_target_shas = [
        check_report.get("target_sha256"),
        render_report.get("target_sha256"),
        review.get("target_sha256"),
    ]
    if not all(_valid_sha256(value) for value in evidence_target_shas) or len(
        set(str(value) for value in evidence_target_shas)
    ) != 1:
        errors.append("target_sha256 của check/render/review không đồng nhất.")
    elif current_target_sha != evidence_target_shas[0]:
        errors.append("Target đã thay đổi sau khi evidence được tạo.")

    render_time = _parse_timestamp(
        render_report.get("timestamp"), "Báo cáo render", errors
    )
    review_time = _parse_timestamp(review.get("reviewed_at"), "Human review", errors)
    if render_time is not None and review_time is not None and review_time < render_time:
        errors.append("reviewed_at không được trước timestamp của render report.")

    outputs = render_report.get("outputs")
    if not isinstance(outputs, list) or not outputs:
        errors.append("Render report không có outputs cần human observation.")
        outputs = []
    render_outputs: dict[str, str] = {}
    for index, item in enumerate(outputs):
        label = f"render.outputs[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label} phải là object.")
            continue
        path = item.get("path")
        sha = item.get("sha256")
        output_path = _repo_file(root, path, label, errors)
        if not _valid_sha256(sha):
            errors.append(f"{label} thiếu sha256 hợp lệ.")
            continue
        if not isinstance(path, str) or path in render_outputs:
            errors.append(f"{label} có path thiếu hoặc trùng.")
            continue
        render_outputs[path] = sha
        if output_path is None or not output_path.is_file():
            errors.append(f"Output render không tồn tại: {path}.")
        elif _sha256(output_path) != sha:
            errors.append(f"Output render đã thay đổi sau evidence: {path}.")

    observed = review.get("observed_outputs")
    if not isinstance(observed, list) or not observed:
        errors.append("Human review thiếu observed_outputs.")
        observed = []
    observed_outputs: dict[str, tuple[str, str]] = {}
    for index, item in enumerate(observed):
        label = f"observed_outputs[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label} phải là object.")
            continue
        path = item.get("path")
        sha = item.get("sha256")
        result = str(item.get("result", "")).upper()
        if not isinstance(path, str) or not path.strip() or path in observed_outputs:
            errors.append(f"{label} thiếu path hợp lệ hoặc bị trùng.")
            continue
        if not _valid_sha256(sha):
            errors.append(f"{label} thiếu sha256 hợp lệ.")
            continue
        if result != "PASS":
            errors.append(f"Human observation chưa PASS: {path}.")
        observed_outputs[path] = (sha, result)

    if set(observed_outputs) != set(render_outputs):
        errors.append("observed_outputs không bao phủ đúng tập outputs của render.")
    for path, render_sha in render_outputs.items():
        observed_item = observed_outputs.get(path)
        if observed_item is not None and observed_item[0] != render_sha:
            errors.append(f"SHA observed output không khớp render output: {path}.")

    checks = review.get("checks")
    if not isinstance(checks, list) or not checks:
        errors.append("Human review không có checks.")
        checks = []
    seen_checks: set[str] = set()
    for index, item in enumerate(checks):
        if not isinstance(item, dict):
            errors.append(f"checks[{index}] phải là object.")
            continue
        check_id = item.get("id")
        result = str(item.get("result", "")).upper()
        if not isinstance(check_id, str) or not check_id.strip() or check_id in seen_checks:
            errors.append(f"checks[{index}] thiếu id hợp lệ hoặc bị trùng.")
            continue
        seen_checks.add(check_id)
        if result != "PASS":
            errors.append(f"Human check chưa PASS: {check_id}.")
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

    if session.get("session_manifest_version") != 2:
        blocked.append("Manifest phiên không dùng session_manifest_version=2.")
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
        _evidence_chain_errors(
            root, target, session, check_report, render_report, review
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

    if review.get("review_manifest_version") != 2:
        blocked.append("Bảng kiểm không dùng review_manifest_version=2.")
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
    with tempfile.TemporaryDirectory(prefix="zo-qmd-prepublish-") as raw:
        root = Path(raw)
        target = "content/example/core/sample.qmd"
        output = "docs/content/example/core/sample.html"
        target_path = root / target
        output_path = root / output
        target_path.parent.mkdir(parents=True)
        output_path.parent.mkdir(parents=True)
        target_path.write_text("# Sample\n", encoding="utf-8")
        output_path.write_text("<h1>Sample</h1>\n", encoding="utf-8")
        target_sha = _sha256(target_path)
        output_sha = _sha256(output_path)
        session = {
            "session_manifest_version": 2,
            "session_id": "session-a",
            "scope": {"target": target},
        }
        check = {
            "evidence_report_version": 1,
            "session_id": "session-a",
            "checker_version": CHECKER_VERSION,
            "mode": "scope",
            "timestamp": "2026-08-09T10:00:00Z",
            "automated_result": "PASS_WITH_WARNINGS",
            "final_acceptance": "NOT_RUN",
            "scope": [target],
            "target": target,
            "target_sha256": target_sha,
            "outputs": [],
            "exit_code": 0,
        }
        render = {
            **check,
            "mode": "render",
            "timestamp": "2026-08-09T10:01:00Z",
            "outputs": [{"path": output, "sha256": output_sha, "kind": "html"}],
        }
        review = {
            "review_manifest_version": 2,
            "session_id": "session-a",
            "target": target,
            "target_sha256": target_sha,
            "reviewed_at": "2026-08-09T10:02:00Z",
            "reviewer": "human",
            "result": "PASS",
            "production_status": "accepted",
            "publication_status": "pending",
            "observed_outputs": [
                {"path": output, "sha256": output_sha, "result": "PASS"}
            ],
            "checks": [{"id": "desktop_html", "result": "PASS"}],
            "remaining_issues": [],
            "pending_user_decisions": ["publication_confirmation"],
        }

        def chain_errors(
            session_value: dict[str, Any] | None = None,
            check_value: dict[str, Any] | None = None,
            render_value: dict[str, Any] | None = None,
            review_value: dict[str, Any] | None = None,
        ) -> list[str]:
            return _evidence_chain_errors(
                root,
                target,
                session_value or session,
                check_value or check,
                render_value or render,
                review_value or review,
            )

        if chain_errors():
            print("FAIL: positive full evidence chain was rejected.")
            return EXIT_FAILED

        git = shutil.which("git")
        if git is None:
            print("FAIL: git is required for prepublish self-test.")
            return EXIT_FAILED
        for arguments in (
            ("init", "-q"),
            ("config", "user.name", "ZO Math Self Test"),
            ("config", "user.email", "self-test@example.invalid"),
            ("add", target, output),
            ("commit", "-q", "-m", "fixture"),
        ):
            result = _run([git, *arguments], root)
            if result.returncode != 0:
                print(f"FAIL: git fixture setup failed: {result.stderr.strip()}")
                return EXIT_FAILED
        base_commit = _run([git, "rev-parse", "HEAD"], root).stdout.strip()
        session.update(
            {
                "automated_result": "PASS",
                "status": {"publication": "pending"},
                "repository": {"commit": base_commit},
                "scope": {
                    "target": target,
                    "allowed": [target],
                    "excluded": [],
                },
                "plan": {"expected_commands": {}},
            }
        )
        audit = root / "_audit"
        audit.mkdir()

        def write_json(name: str, value: dict[str, Any]) -> str:
            path = audit / name
            path.write_text(
                json.dumps(value, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            return str(path)

        positive, positive_exit = build_report(
            root=root,
            target=target,
            operations_cli_version="self-test",
            project_summary={
                "publication": {
                    "production_states": ["in_production", "accepted"]
                },
                "project": {},
            },
            inspect_exit=EXIT_OK,
            session_raw=write_json("session.json", session),
            check_report_raw=write_json("check.json", check),
            render_report_raw=write_json("render.json", render),
            human_review_raw=write_json("review.json", review),
        )
        if positive_exit != EXIT_OK or positive["blocked_reasons"]:
            print("FAIL: positive prepublish build was blocked.")
            return EXIT_FAILED

        invalid_acceptance = deepcopy(check)
        invalid_acceptance["final_acceptance"] = "PASS"
        if not _checker_evidence_errors(
            invalid_acceptance, label="check", expected_mode="scope", target=target
        ):
            print("FAIL: automated final acceptance was not rejected.")
            return EXIT_FAILED

        cases: list[tuple[str, dict[str, Any], str]] = []
        missing_observed = deepcopy(review)
        missing_observed.pop("observed_outputs")
        cases.append(("missing observed_outputs", missing_observed, "review"))
        failed_observed = deepcopy(review)
        failed_observed["observed_outputs"][0]["result"] = "FAIL"
        cases.append(("failed observed output", failed_observed, "review"))
        malformed_check = deepcopy(review)
        malformed_check["checks"] = [{}]
        cases.append(("malformed human check", malformed_check, "review"))
        failed_check = deepcopy(review)
        failed_check["checks"][0]["result"] = "FAIL"
        cases.append(("failed human check", failed_check, "review"))
        wrong_check_session = deepcopy(check)
        wrong_check_session["session_id"] = "session-b"
        cases.append(("check session mismatch", wrong_check_session, "check"))
        wrong_render_session = deepcopy(render)
        wrong_render_session["session_id"] = "session-b"
        cases.append(("render session mismatch", wrong_render_session, "render"))
        wrong_review_session = deepcopy(review)
        wrong_review_session["session_id"] = "session-b"
        cases.append(("review session mismatch", wrong_review_session, "review"))
        wrong_observed_sha = deepcopy(review)
        wrong_observed_sha["observed_outputs"][0]["sha256"] = "0" * 64
        cases.append(("observed SHA mismatch", wrong_observed_sha, "review"))
        early_review = deepcopy(review)
        early_review["reviewed_at"] = "2026-08-09T09:59:00Z"
        cases.append(("review before render", early_review, "review"))
        wrong_target = deepcopy(review)
        wrong_target["target"] = "content/example/core/other.qmd"
        cases.append(("target mismatch", wrong_target, "review"))

        for label, evidence, kind in cases:
            kwargs = {f"{kind}_value": evidence}
            if not chain_errors(**kwargs):
                print(f"FAIL: {label} was not rejected.")
                return EXIT_FAILED

        target_path.write_text("# Changed\n", encoding="utf-8")
        if not chain_errors():
            print("FAIL: stale target evidence was not rejected.")
            return EXIT_FAILED
        target_path.write_text("# Sample\n", encoding="utf-8")

        output_path.write_text("<h1>Changed</h1>\n", encoding="utf-8")
        if not chain_errors():
            print("FAIL: stale render output was not rejected.")
            return EXIT_FAILED

    print("PASS: zo_qmd_prepublish self-test")
    return EXIT_OK


if __name__ == "__main__":
    if len(__import__("sys").argv) == 2 and __import__("sys").argv[1] == "self-test":
        raise SystemExit(self_test())
    print("Usage: zo_qmd_prepublish.py self-test")
    raise SystemExit(2)

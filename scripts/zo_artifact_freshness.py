"""Git-aware freshness checks for generated artifacts.

Filesystem modification times are reliable while a source or artifact is being
edited in the current worktree, but they are not stable evidence after a Git
checkout or worktree creation.  This module uses Git state and history for
clean tracked files, and falls back to modification times only for active
worktree changes or files without usable Git history.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


EXIT_OK = 0
EXIT_INVALID = 1
EXIT_USAGE = 2
EXIT_MISSING_TOOL = 3


class FreshnessError(RuntimeError):
    """Raised when freshness cannot be determined safely."""


@dataclass(frozen=True)
class FreshnessResult:
    """Outcome and evidence basis for a source/artifact comparison."""

    current: bool
    basis: str
    message: str


def _run(command: Sequence[str], root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(command),
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def _relative(root: Path, path: Path) -> Path:
    absolute = path if path.is_absolute() else root / path
    try:
        return absolute.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise FreshnessError(f"Đường dẫn nằm ngoài repository: {path}") from exc


def _tracked(root: Path, relative: Path) -> bool:
    result = _run(
        ["git", "ls-files", "--error-unmatch", "--", relative.as_posix()],
        root,
    )
    return result.returncode == 0


def _changed(root: Path, relative: Path, *, staged: bool) -> bool:
    if not _tracked(root, relative):
        return True
    command = ["git", "diff", "--quiet"]
    if staged:
        command.extend(["--cached", "HEAD"])
    else:
        command.append("HEAD")
    command.extend(["--", relative.as_posix()])
    result = _run(command, root)
    if result.returncode == 0:
        return False
    if result.returncode == 1:
        return True
    raise FreshnessError(
        result.stderr.strip()
        or f"Không xác định được trạng thái Git của {relative.as_posix()}."
    )


def _last_change_commit(root: Path, relative: Path) -> str | None:
    result = _run(
        ["git", "log", "-1", "--format=%H", "--", relative.as_posix()],
        root,
    )
    if result.returncode != 0:
        raise FreshnessError(result.stderr.strip() or "git log thất bại.")
    value = result.stdout.strip()
    return value or None


def _is_ancestor(root: Path, older: str, newer: str) -> bool:
    result = _run(["git", "merge-base", "--is-ancestor", older, newer], root)
    if result.returncode == 0:
        return True
    if result.returncode == 1:
        return False
    raise FreshnessError(result.stderr.strip() or "git merge-base thất bại.")


def _latest_change_commit(
    root: Path, source: Path, artifact: Path
) -> str | None:
    result = _run(
        [
            "git",
            "log",
            "-1",
            "--format=%H",
            "--",
            source.as_posix(),
            artifact.as_posix(),
        ],
        root,
    )
    if result.returncode != 0:
        raise FreshnessError(result.stderr.strip() or "git log thất bại.")
    value = result.stdout.strip()
    return value or None


def _mtime_result(source: Path, artifact: Path, basis: str) -> FreshnessResult:
    current = artifact.stat().st_mtime_ns >= source.stat().st_mtime_ns
    message = (
        "Tệp sinh không cũ hơn tệp nguồn theo mtime trong worktree."
        if current
        else "Tệp sinh cũ hơn tệp nguồn theo mtime trong worktree; phải dựng lại."
    )
    return FreshnessResult(current=current, basis=basis, message=message)


def evaluate_artifact_freshness(
    root: Path,
    source: Path,
    artifact: Path,
    *,
    staged: bool = False,
) -> FreshnessResult:
    """Compare a generated artifact with its source without checkout mtime noise."""

    root = root.resolve()
    source_relative = _relative(root, source)
    artifact_relative = _relative(root, artifact)
    source_path = root / source_relative
    artifact_path = root / artifact_relative

    if not source_path.is_file():
        raise FreshnessError(f"Không tìm thấy tệp nguồn: {source_relative.as_posix()}")
    if not artifact_path.is_file():
        raise FreshnessError(
            f"Không tìm thấy tệp sinh: {artifact_relative.as_posix()}"
        )

    source_changed = _changed(root, source_relative, staged=staged)
    artifact_changed = _changed(root, artifact_relative, staged=staged)

    if source_changed or artifact_changed:
        if source_changed and not artifact_changed:
            return FreshnessResult(
                current=False,
                basis="git-worktree",
                message=(
                    "Tệp nguồn đã thay đổi nhưng tệp sinh chưa thay đổi; "
                    "phải dựng lại."
                ),
            )
        return _mtime_result(source_path, artifact_path, "worktree-mtime")

    source_commit = _last_change_commit(root, source_relative)
    artifact_commit = _last_change_commit(root, artifact_relative)

    if source_commit and artifact_commit:
        if source_commit == artifact_commit:
            return FreshnessResult(
                current=True,
                basis="git-same-commit",
                message=(
                    "Tệp nguồn và tệp sinh được cập nhật trong cùng commit; "
                    "bỏ qua sai lệch mtime do checkout."
                ),
            )
        if _is_ancestor(root, source_commit, artifact_commit):
            return FreshnessResult(
                current=True,
                basis="git-history",
                message="Tệp sinh được cập nhật sau tệp nguồn theo lịch sử Git.",
            )
        if _is_ancestor(root, artifact_commit, source_commit):
            return FreshnessResult(
                current=False,
                basis="git-history",
                message="Tệp sinh cũ hơn tệp nguồn theo lịch sử Git; phải dựng lại.",
            )

        latest = _latest_change_commit(root, source_relative, artifact_relative)
        if latest:
            current = latest == artifact_commit
            return FreshnessResult(
                current=current,
                basis="git-topology",
                message=(
                    "Tệp sinh là thay đổi mới nhất theo lịch sử Git."
                    if current
                    else "Tệp nguồn là thay đổi mới nhất theo lịch sử Git; phải dựng lại."
                ),
            )

    return _mtime_result(source_path, artifact_path, "mtime-fallback")


def _git(root: Path, *arguments: str) -> None:
    result = _run(["git", *arguments], root)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Git command failed.")


def _self_test() -> None:
    if shutil.which("git") is None:
        raise RuntimeError("Không tìm thấy Git trong PATH.")

    with tempfile.TemporaryDirectory(prefix="zo-artifact-freshness-") as raw:
        root = Path(raw)
        _git(root, "init", "-q")
        _git(root, "config", "user.name", "ZO Math Self Test")
        _git(root, "config", "user.email", "self-test@example.invalid")

        source = root / "article.qmd"
        artifact = root / "article.pdf"
        source.write_text("version 1\n", encoding="utf-8")
        artifact.write_bytes(b"%PDF-1.4\nversion 1\n")
        _git(root, "add", "article.qmd", "article.pdf")
        _git(root, "commit", "-q", "-m", "baseline")

        source_stat = source.stat()
        artifact_stat = artifact.stat()
        os.utime(
            source,
            ns=(source_stat.st_atime_ns, artifact_stat.st_mtime_ns + 10_000_000),
        )
        same_commit = evaluate_artifact_freshness(root, source, artifact)
        assert same_commit.current
        assert same_commit.basis == "git-same-commit"

        source.write_text("version 2\n", encoding="utf-8")
        source_only = evaluate_artifact_freshness(root, source, artifact)
        assert not source_only.current
        assert source_only.basis == "git-worktree"

        artifact.write_bytes(b"%PDF-1.4\nversion 2\n")
        artifact_stat = artifact.stat()
        source_stat = source.stat()
        os.utime(
            artifact,
            ns=(artifact_stat.st_atime_ns, source_stat.st_mtime_ns + 10_000_000),
        )
        both_changed = evaluate_artifact_freshness(root, source, artifact)
        assert both_changed.current
        assert both_changed.basis == "worktree-mtime"

        _git(root, "add", "article.qmd")
        _git(root, "commit", "-q", "-m", "update source")
        _git(root, "restore", "article.pdf")
        artifact_stat = artifact.stat()
        source_stat = source.stat()
        os.utime(
            artifact,
            ns=(artifact_stat.st_atime_ns, source_stat.st_mtime_ns + 20_000_000),
        )
        source_newer_commit = evaluate_artifact_freshness(root, source, artifact)
        assert not source_newer_commit.current
        assert source_newer_commit.basis == "git-history"

        artifact.write_bytes(b"%PDF-1.4\nversion 2\n")
        _git(root, "add", "article.pdf")
        _git(root, "commit", "-q", "-m", "update artifact")
        artifact_newer_commit = evaluate_artifact_freshness(root, source, artifact)
        assert artifact_newer_commit.current
        assert artifact_newer_commit.basis == "git-history"


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    subparsers = result.add_subparsers(dest="command", required=True)
    subparsers.add_parser("self-test", help="Chạy kiểm tra nội bộ độc lập.")
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command == "self-test":
        try:
            _self_test()
        except (AssertionError, OSError, RuntimeError, FreshnessError) as exc:
            print(f"ERROR: zo_artifact_freshness self-test: {exc}")
            return EXIT_INVALID
        print("PASS: zo_artifact_freshness self-test")
        return EXIT_OK
    return EXIT_USAGE


if __name__ == "__main__":
    raise SystemExit(main())

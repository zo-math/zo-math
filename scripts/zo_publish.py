"""Read-only safety checks for publishing the ZO Math website."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import mimetypes
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence

try:
    import yaml
except ImportError:  # Reported with exit code 3 in main().
    yaml = None


EXIT_OK = 0
EXIT_UNSAFE = 1
EXIT_USAGE = 2
EXIT_MISSING = 3
SUPPORTED_VERSION = 1
TEXT_SUFFIXES = {".css", ".html", ".js", ".json", ".txt", ".xml"}
SOURCE_SUFFIXES = {
    ".aux", ".db", ".fdb_latexmk", ".fls", ".key", ".log", ".md",
    ".pem", ".ps1", ".py", ".qmd", ".r", ".rdata", ".rmd", ".sh",
    ".sqlite", ".tex",
}
FORBIDDEN_COMPONENTS = {
    ".git", ".ipynb_checkpoints", "__pycache__", "_audit", "README",
    "quy_trinh_xay_dung", "scripts",
}
SECRET_PATTERNS = (
    ("private-key", re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----")),
    ("github-token", re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}")),
    ("google-api-key", re.compile(r"AIza[0-9A-Za-z_-]{30,}")),
    ("aws-access-key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("personal-path", re.compile(r"(?i)(?:[A-Z]:[/\\]Users[/\\][^/\\\s]+|/home/[^/\s]+)")),
)


class ConfigError(ValueError):
    """Configuration or command-line error."""


class MissingToolError(RuntimeError):
    """Required tool, dependency, or worktree is missing."""


def run(command: Sequence[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(command), cwd=cwd, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )


def git(root: Path, *args: str, safe: Path | None = None) -> subprocess.CompletedProcess[str]:
    command = ["git"]
    if safe is not None:
        command.extend(["-c", f"safe.directory={safe.as_posix()}"])
    command.extend(["-C", str(root), *args])
    return run(command, root)


def git_text(root: Path, *args: str, safe: Path | None = None) -> str:
    result = git(root, *args, safe=safe)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Git command failed.")
    return result.stdout.strip()


def repo_root() -> Path:
    if shutil.which("git") is None:
        raise MissingToolError("Không tìm thấy Git trong PATH.")
    result = run(["git", "rev-parse", "--show-toplevel"], Path.cwd())
    if result.returncode != 0:
        raise ConfigError("Không xác định được repository Git.")
    return Path(result.stdout.strip()).resolve()


def safe_relative(value: Any, label: str, allow_glob: bool = False) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"{label}: đường dẫn rỗng hoặc không phải chuỗi.")
    raw = value.strip().replace("\\", "/")
    if raw.startswith(("/", "//")) or re.match(r"^[A-Za-z]:", raw):
        raise ConfigError(f"{label}: không được dùng đường dẫn tuyệt đối: {value}")
    parts = PurePosixPath(raw).parts
    if ".." in parts or ".git" in parts:
        raise ConfigError(f"{label}: đường dẫn không an toàn: {value}")
    if allow_glob and raw in {"*", "**", "**/*"}:
        raise ConfigError(f"{label}: mẫu quá rộng: {value}")
    return raw.rstrip("/")


def string_list(value: Any, label: str, allow_glob: bool = False) -> list[str]:
    if not isinstance(value, list):
        raise ConfigError(f"{label} phải là danh sách.")
    return [safe_relative(item, label, allow_glob) for item in value]


def load_config(root: Path, raw_path: str) -> tuple[Path, dict[str, Any]]:
    candidate = Path(raw_path)
    path = (candidate if candidate.is_absolute() else root / candidate).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ConfigError("Tệp cấu hình phải nằm trong repository.") from exc
    if not path.is_file():
        raise ConfigError(f"Không tìm thấy cấu hình: {raw_path}")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise ConfigError(f"YAML không hợp lệ: {exc}") from exc
    if not isinstance(data, dict) or data.get("version") != SUPPORTED_VERSION:
        raise ConfigError(f"Chỉ hỗ trợ version {SUPPORTED_VERSION}.")
    for key in ("source_branch", "target_branch", "output_dir"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ConfigError(f"Thiếu hoặc sai {key}.")
    if data["source_branch"] == data["target_branch"]:
        raise ConfigError("Nhánh nguồn và đích phải khác nhau.")
    data["output_dir"] = safe_relative(data["output_dir"], "output_dir")
    for section in ("allowlist", "denylist"):
        if not isinstance(data.get(section), dict):
            raise ConfigError(f"Thiếu {section}.")
        data[section]["paths" if section == "denylist" else "files"] = string_list(
            data[section].get("paths" if section == "denylist" else "files", []),
            section,
        )
        data[section]["globs"] = string_list(data[section].get("globs", []), section, True)
    limit = data.get("default_max_file_size")
    if not isinstance(limit, int) or limit <= 0:
        raise ConfigError("default_max_file_size phải là số nguyên dương.")
    exceptions = data.get("size_exceptions", {})
    if not isinstance(exceptions, dict):
        raise ConfigError("size_exceptions phải là mapping.")
    normalized: dict[str, int] = {}
    for name, size in exceptions.items():
        path_name = safe_relative(name, "size_exceptions")
        if not isinstance(size, int) or size <= 0:
            raise ConfigError(f"Giới hạn không hợp lệ: {name}")
        normalized[path_name] = size
    data["size_exceptions"] = normalized
    data["required_files"] = string_list(data.get("required_files", []), "required_files")
    denied = data["denylist"]["paths"]
    denied_globs = data["denylist"]["globs"]
    for required in data["required_files"]:
        if path_denied(required, denied, denied_globs):
            raise ConfigError(f"Tệp bắt buộc nằm trong denylist: {required}")
    return path, data


def glob_match(path: str, pattern: str) -> bool:
    # fnmatch is intentionally anchored to the complete POSIX path here.
    return fnmatch.fnmatchcase(path, pattern)


def path_denied(path: str, prefixes: Sequence[str], globs: Sequence[str]) -> bool:
    return any(path == item or path.startswith(item + "/") for item in prefixes) or any(
        glob_match(path, pattern) for pattern in globs
    )


def path_allowed(path: str, files: Sequence[str], globs: Sequence[str]) -> bool:
    return path in files or any(glob_match(path, pattern) for pattern in globs)


def parse_worktrees(root: Path) -> list[dict[str, str]]:
    text = git_text(root, "worktree", "list", "--porcelain")
    blocks: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for line in [*text.splitlines(), ""]:
        if not line:
            if current:
                blocks.append(current)
                current = {}
            continue
        key, _, value = line.partition(" ")
        current[key] = value
    return blocks


def find_publish_worktree(root: Path, branch: str) -> Path:
    ref = f"refs/heads/{branch}"
    matches = [Path(item["worktree"]).resolve() for item in parse_worktrees(root) if item.get("branch") == ref]
    if len(matches) != 1:
        raise MissingToolError(f"Cần đúng một worktree cho {branch}; tìm thấy {len(matches)}.")
    target = matches[0]
    if not target.is_dir() or target == root:
        raise MissingToolError("Worktree xuất bản không tồn tại hoặc trùng repository nguồn.")
    common_main = Path(git_text(root, "rev-parse", "--git-common-dir")).resolve()
    common_target_raw = git_text(target, "rev-parse", "--git-common-dir", safe=target)
    common_target = (target / common_target_raw).resolve() if not Path(common_target_raw).is_absolute() else Path(common_target_raw).resolve()
    if common_main != common_target:
        raise MissingToolError("Worktree xuất bản không thuộc cùng repository.")
    return target


def merge_in_progress(root: Path, safe: Path | None = None) -> bool:
    git_dir_raw = git_text(root, "rev-parse", "--git-dir", safe=safe)
    git_dir = (root / git_dir_raw).resolve() if not Path(git_dir_raw).is_absolute() else Path(git_dir_raw).resolve()
    return any((git_dir / name).exists() for name in ("MERGE_HEAD", "rebase-merge", "rebase-apply"))


def git_state(root: Path, branch: str, remote_ref: str | None, safe: Path | None = None) -> dict[str, Any]:
    current = git_text(root, "branch", "--show-current", safe=safe)
    status = git_text(root, "status", "--porcelain=v1", "--untracked-files=all", safe=safe)
    staged = git_text(root, "diff", "--cached", "--name-only", safe=safe)
    commit = git_text(root, "rev-parse", "HEAD", safe=safe)
    issues: list[str] = []
    if current != branch:
        issues.append(f"Đang ở nhánh {current or '(detached)'}, cần {branch}.")
    if status:
        issues.append("Working tree không sạch.")
    if staged:
        issues.append("Vùng staged không trống.")
    if merge_in_progress(root, safe):
        issues.append("Có merge hoặc rebase dang dở.")
    ahead = behind = None
    compare = remote_ref
    if compare is None:
        upstream = git(root, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}", safe=safe)
        if upstream.returncode != 0:
            issues.append("Nhánh nguồn không có upstream.")
            compare = None
        else:
            compare = upstream.stdout.strip()
    if compare:
        result = git(root, "rev-list", "--left-right", "--count", f"{compare}...HEAD", safe=safe)
        if result.returncode != 0:
            issues.append(f"Không đọc được remote ref {compare}.")
        else:
            behind, ahead = (int(value) for value in result.stdout.split())
            if behind:
                issues.append(f"Nhánh local behind {compare}: {behind} commit.")
    return {"path": str(root), "branch": current, "commit": commit, "remote_ref": compare,
            "ahead": ahead, "behind": behind, "status": status.splitlines(), "issues": issues}


def scan_symlinks(root: Path, skip_git: bool = False) -> list[str]:
    found: list[str] = []
    for current, dirs, files in os.walk(root, followlinks=False):
        base = Path(current)
        if skip_git and base == root and ".git" in dirs:
            dirs.remove(".git")
        for name in [*dirs, *files]:
            candidate = base / name
            if candidate.is_symlink():
                found.append(candidate.relative_to(root).as_posix())
    return found


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sensitive_text(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    hits: list[dict[str, Any]] = []
    for label, pattern in SECRET_PATTERNS:
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            hits.append({"type": label, "line": line})
    return hits


def build_manifest(output: Path, config: Mapping[str, Any]) -> dict[str, Any]:
    if not output.is_dir():
        raise MissingToolError(f"Không tìm thấy thư mục đầu ra: {output}")
    symlinks = scan_symlinks(output)
    allow = config["allowlist"]
    deny = config["denylist"]
    selected: dict[str, dict[str, Any]] = {}
    excluded = Counter()
    issues: list[dict[str, Any]] = [{"type": "symlink", "path": item} for item in symlinks]
    for current, dirs, files in os.walk(output, followlinks=False):
        base = Path(current)
        dirs[:] = [name for name in dirs if not (base / name).is_symlink()]
        for name in files:
            path = base / name
            relative = path.relative_to(output).as_posix()
            parts = PurePosixPath(relative).parts
            suffix = path.suffix.lower()
            private = path_denied(relative, deny["paths"], deny["globs"])
            suspicious = private or bool(FORBIDDEN_COMPONENTS.intersection(parts)) or suffix in SOURCE_SUFFIXES or name.endswith(".synctex.gz")
            if suspicious:
                excluded["forbidden-or-private"] += 1
                issues.append({"type": "forbidden-output", "path": relative})
                continue
            if not path_allowed(relative, allow["files"], allow["globs"]):
                excluded["not-allowlisted"] += 1
                continue
            size = path.stat().st_size
            limit = config["size_exceptions"].get(relative, config["default_max_file_size"])
            if size > limit:
                excluded["oversize"] += 1
                issues.append({"type": "oversize", "path": relative, "size": size, "limit": limit})
                continue
            secrets = sensitive_text(path)
            if secrets:
                excluded["sensitive-content"] += 1
                issues.append({"type": "sensitive-content", "path": relative, "findings": secrets})
                continue
            selected[relative] = {
                "size": size, "sha256": sha256(path),
                "mime": mimetypes.guess_type(relative)[0] or "application/octet-stream",
            }
    missing = [name for name in config["required_files"] if name not in selected]
    issues.extend({"type": "missing-required", "path": item} for item in missing)
    return {"files": selected, "count": len(selected),
            "bytes": sum(item["size"] for item in selected.values()),
            "excluded": dict(excluded), "missing_required": missing, "issues": issues}


def publish_diff(worktree: Path, manifest: Mapping[str, Any], config: Mapping[str, Any]) -> dict[str, Any]:
    allow = config["allowlist"]
    desired = manifest["files"]
    existing: dict[str, dict[str, Any]] = {}
    unmanaged: list[str] = []
    for current, dirs, files in os.walk(worktree, followlinks=False):
        base = Path(current)
        if base == worktree and ".git" in dirs:
            dirs.remove(".git")
        dirs[:] = [name for name in dirs if not (base / name).is_symlink()]
        for name in files:
            path = base / name
            relative = path.relative_to(worktree).as_posix()
            if path_allowed(relative, allow["files"], allow["globs"]):
                existing[relative] = {"size": path.stat().st_size, "sha256": sha256(path)}
            else:
                unmanaged.append(relative)
    added = sorted(set(desired) - set(existing))
    deleted = sorted(set(existing) - set(desired))
    updated = sorted(name for name in set(desired).intersection(existing)
                     if desired[name]["sha256"] != existing[name]["sha256"])
    change_bytes = sum(desired[name]["size"] for name in [*added, *updated]) + sum(existing[name]["size"] for name in deleted)
    return {"add": added, "update": updated, "delete_managed": deleted,
            "unmanaged_existing": sorted(unmanaged), "change_bytes": change_bytes}


def report_target(root: Path, raw: str) -> Path:
    target = (Path(raw) if Path(raw).is_absolute() else root / raw).resolve()
    audit = (root / "_audit").resolve()
    try:
        target.relative_to(audit)
    except ValueError as exc:
        raise ConfigError("--report chỉ được ghi bên trong _audit/.") from exc
    return target


def print_summary(payload: Mapping[str, Any], code: int) -> None:
    manifest = payload.get("manifest", {})
    diff = payload.get("diff", {})
    issues = payload.get("issues", [])
    print("MODE: check | READ-ONLY")
    print(f"SOURCE: {payload.get('source', {}).get('branch')} {payload.get('source', {}).get('commit')}")
    print(f"TARGET: {payload.get('target', {}).get('branch')} {payload.get('target', {}).get('commit')}")
    print(f"MANIFEST: {manifest.get('count', 0)} files | {manifest.get('bytes', 0)} bytes")
    print(f"EXCLUDED: {manifest.get('excluded', {})}")
    print(f"DIFF: add={len(diff.get('add', []))} update={len(diff.get('update', []))} delete-managed={len(diff.get('delete_managed', []))} unmanaged={len(diff.get('unmanaged_existing', []))}")
    print(f"ISSUES: {len(issues)}")
    for item in issues[:20]:
        print(f"  - {item.get('type')}: {item.get('path', item.get('message', ''))}")
    if len(issues) > 20:
        print(f"  - ... và {len(issues) - 20} vấn đề khác")
    print(f"RESULT: {'PASS' if code == 0 else 'FAIL'} | EXIT={code}")


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("command", nargs="?", help="Chỉ hỗ trợ: check")
    value.add_argument("--config", default="publish_public.yml")
    value.add_argument("--report")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command != "check":
        print("ERROR: hiện chỉ hỗ trợ lệnh 'check'; prepare/publish chưa được triển khai.", file=sys.stderr)
        return EXIT_USAGE
    if yaml is None:
        print("ERROR: thiếu dependency PyYAML.", file=sys.stderr)
        return EXIT_MISSING
    try:
        root = repo_root()
        if shutil.which("quarto") is None:
            raise MissingToolError("Không tìm thấy Quarto trong PATH.")
        config_path, config = load_config(root, args.config)
        target = find_publish_worktree(root, config["target_branch"])
        source_state = git_state(root, config["source_branch"], None)
        target_state = git_state(target, config["target_branch"], f"origin/{config['target_branch']}", target)
        issues: list[dict[str, Any]] = []
        issues.extend({"type": "source-git", "message": item} for item in source_state["issues"])
        issues.extend({"type": "target-git", "message": item} for item in target_state["issues"])
        issues.extend({"type": "target-symlink", "path": item} for item in scan_symlinks(target, True))
        manifest = build_manifest((root / config["output_dir"]).resolve(), config)
        issues.extend(manifest["issues"])
        diff = publish_diff(target, manifest, config)
        payload: dict[str, Any] = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "repo_root": str(root), "publish_worktree": str(target),
            "config": str(config_path.relative_to(root).as_posix()),
            "source": source_state, "target": target_state,
            "manifest": {key: value for key, value in manifest.items() if key != "issues"},
            "diff": diff, "issues": issues,
        }
        code = EXIT_UNSAFE if issues else EXIT_OK
        payload["exit_code"] = code
        if args.report:
            report = report_target(root, args.report)
            report.parent.mkdir(parents=True, exist_ok=True)
            report.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print_summary(payload, code)
        return code
    except ConfigError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_USAGE
    except (MissingToolError, FileNotFoundError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_MISSING
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_UNSAFE


if __name__ == "__main__":
    raise SystemExit(main())

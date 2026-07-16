"""Safely check and prepare the public ZO Math website tree."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import mimetypes
import os
import posixpath
import re
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit
from typing import Any, Mapping, Sequence

try:
    import yaml
except ImportError:  # Reported with exit code 3 in main().
    yaml = None


EXIT_OK = 0
EXIT_UNSAFE = 1
EXIT_USAGE = 2
EXIT_MISSING = 3
EXIT_RESTORE = 4
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


class RestoreError(RuntimeError):
    """The publication worktree could not be restored safely."""


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
    if path.is_symlink():
        raise ConfigError("Tệp cấu hình không được là symlink.")
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
    prepare = data.get("prepare")
    if not isinstance(prepare, dict):
        raise ConfigError("Thiếu cấu hình prepare.")
    prepare["staging_dir"] = safe_relative(prepare.get("staging_dir"), "prepare.staging_dir")
    prepare["report_file"] = safe_relative(prepare.get("report_file"), "prepare.report_file")
    if not prepare["staging_dir"].startswith("_audit/") or not prepare["report_file"].startswith("_audit/"):
        raise ConfigError("Staging và báo cáo prepare phải nằm trong _audit/.")
    if prepare.get("generated_target") is not True:
        raise ConfigError("prepare.generated_target phải xác nhận bằng true.")
    prepare["special_files"] = string_list(prepare.get("special_files", []), "prepare.special_files")
    prepare["allowed_target_files"] = string_list(
        prepare.get("allowed_target_files", []), "prepare.allowed_target_files"
    )
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
    return any((git_dir / name).exists() for name in (
        "MERGE_HEAD", "rebase-merge", "rebase-apply", "CHERRY_PICK_HEAD"
    ))


def git_state(root: Path, branch: str, remote_ref: str | None, safe: Path | None = None) -> dict[str, Any]:
    current = git_text(root, "branch", "--show-current", safe=safe)
    status_result = git(root, "status", "--porcelain=v1", "--untracked-files=all", safe=safe)
    if status_result.returncode != 0:
        raise RuntimeError(status_result.stderr.strip() or "Không đọc được Git status.")
    status = status_result.stdout.rstrip("\r\n")
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


def tree_manifest(root: Path, skip_git: bool = False) -> dict[str, Any]:
    files: dict[str, dict[str, Any]] = {}
    for current, dirs, names in os.walk(root, followlinks=False):
        base = Path(current)
        if skip_git and base == root and ".git" in dirs:
            dirs.remove(".git")
        for name in names:
            if skip_git and base == root and name == ".git":
                continue
            path = base / name
            relative = path.relative_to(root).as_posix()
            files[relative] = {"size": path.stat().st_size, "sha256": sha256(path)}
    return {"files": files, "count": len(files), "bytes": sum(v["size"] for v in files.values())}


def safe_remove_tree(path: Path, audit: Path) -> None:
    resolved = path.resolve()
    try:
        resolved.relative_to(audit.resolve())
    except ValueError as exc:
        raise ConfigError(f"Từ chối xóa ngoài _audit/: {path}") from exc
    if resolved.is_symlink():
        raise ConfigError(f"Từ chối staging symlink: {path}")
    if resolved.exists():
        shutil.rmtree(resolved)


def copy_manifest(source: Path, target: Path, manifest: Mapping[str, Any]) -> None:
    for relative in manifest["files"]:
        src = source / relative
        dst = target / relative
        if src.is_symlink():
            raise ConfigError(f"Từ chối symlink: {relative}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if value and key in {"src", "href"}:
                self.links.append((key, value))
            elif value and key == "srcset":
                self.links.extend((key, item.strip().split()[0]) for item in value.split(",") if item.strip())


def validate_public(public: Path, manifest: Mapping[str, Any], config: Mapping[str, Any]) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    files = set(manifest["files"])
    private_fragments = tuple(config["denylist"]["paths"][:3])
    html_count = link_count = 0
    for relative in sorted(name for name in files if name.lower().endswith(".html")):
        html_count += 1
        text = (public / relative).read_text(encoding="utf-8", errors="replace")
        parser = LinkCollector()
        try:
            parser.feed(text)
            parser.close()
        except Exception as exc:
            issues.append({"type": "html-parse", "path": relative, "message": str(exc)})
            continue
        for kind, raw in parser.links:
            link_count += 1
            parsed = urlsplit(raw.strip())
            if parsed.scheme.lower() in {"http", "https", "mailto", "tel", "data", "javascript"} or raw.startswith("//"):
                continue
            decoded = unquote(parsed.path).replace("\\", "/")
            if not decoded:
                continue
            if re.match(r"^[A-Za-z]:", decoded):
                issues.append({"type": "unsafe-link", "path": relative, "value": raw})
                continue
            candidate = decoded.lstrip("/") if decoded.startswith("/") else posixpath.normpath(
                str(PurePosixPath(relative).parent / decoded)
            )
            if candidate == ".." or candidate.startswith("../"):
                issues.append({"type": "unsafe-link", "path": relative, "value": raw})
                continue
            if candidate not in files and not candidate.endswith("/"):
                issues.append({"type": "missing-resource", "path": relative, "value": raw})
            if any(fragment in candidate for fragment in private_fragments):
                issues.append({"type": "private-link", "path": relative, "value": raw})
    return {"html_files": html_count, "local_links": link_count, "issues": issues}


def render_to_staging(root: Path, render_dir: Path) -> dict[str, Any]:
    command = [sys.executable, str(root / "scripts/zo_quarto.py"), "render", "--output-dir", str(render_dir)]
    result = run(command, root)
    matches = re.findall(r"\[\s*\d+/(\d+)\]", result.stdout + result.stderr)
    return {"command": command, "exit_code": result.returncode,
            "source_count": int(matches[-1]) if matches else None,
            "stdout": result.stdout, "stderr": result.stderr}


def exact_diff(target_manifest: Mapping[str, Any], desired: Mapping[str, Any]) -> dict[str, Any]:
    old, new = target_manifest["files"], desired["files"]
    added = sorted(set(new) - set(old))
    updated = sorted(name for name in set(new) & set(old) if new[name]["sha256"] != old[name]["sha256"])
    deleted = sorted(set(old) - set(new))
    return {
        "add": added,
        "update": updated,
        "delete": deleted,
        "unchanged": sorted(name for name in set(new) & set(old) if new[name]["sha256"] == old[name]["sha256"]),
        "change_bytes": (sum(new[name]["size"] for name in [*added, *updated])
                         + sum(old[name]["size"] for name in deleted)),
    }


def sync_exact(source: Path, target: Path, desired: Mapping[str, Any], diff: Mapping[str, Any]) -> None:
    for relative in [*diff["delete"], *diff["update"]]:
        path = target / relative
        if path.exists() and not path.is_dir():
            path.unlink()
    copy_manifest(source, target, {"files": {name: desired["files"][name] for name in [*diff["add"], *diff["update"]]}})
    for current, dirs, files in os.walk(target, topdown=False):
        base = Path(current)
        if base == target:
            continue
        if base.name == ".git" or ".git" in base.relative_to(target).parts:
            continue
        if not any(base.iterdir()):
            base.rmdir()


def restore_from_backup(target: Path, backup: Path, backup_manifest: Mapping[str, Any]) -> None:
    current = tree_manifest(target, True)
    diff = exact_diff(current, backup_manifest)
    sync_exact(backup, target, backup_manifest, diff)
    if tree_manifest(target, True) != backup_manifest:
        raise RestoreError("Không thể hoàn nguyên worktree đúng manifest backup.")


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
    print(f"MODE: {payload.get('mode', 'check')}" + (" | READ-ONLY" if payload.get('mode', 'check') == "check" else ""))
    print(f"SOURCE: {payload.get('source', {}).get('branch')} {payload.get('source', {}).get('commit')}")
    print(f"TARGET: {payload.get('target', {}).get('branch')} {payload.get('target', {}).get('commit')}")
    print(f"MANIFEST: {manifest.get('count', 0)} files | {manifest.get('bytes', 0)} bytes")
    print(f"EXCLUDED: {manifest.get('excluded', {})}")
    deleted = diff.get("delete", diff.get("delete_managed", []))
    print(f"DIFF: add={len(diff.get('add', []))} update={len(diff.get('update', []))} delete={len(deleted)} unchanged={len(diff.get('unchanged', []))} unmanaged={len(diff.get('unmanaged_existing', []))}")
    print(f"ISSUES: {len(issues)}")
    for item in issues[:20]:
        print(f"  - {item.get('type')}: {item.get('path', item.get('message', ''))}")
    if len(issues) > 20:
        print(f"  - ... và {len(issues) - 20} vấn đề khác")
    print(f"RESULT: {'PASS' if code == 0 else 'FAIL'} | EXIT={code}")


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("command", nargs="?", help="Hỗ trợ: check, prepare")
    value.add_argument("--config", default="publish_public.yml")
    value.add_argument("--report")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command not in {"check", "prepare"}:
        print("ERROR: chỉ hỗ trợ lệnh 'check' và 'prepare'; publish chưa được triển khai.", file=sys.stderr)
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
        if args.command == "prepare":
            fetch = git(root, "fetch", "--prune", "origin")
            if fetch.returncode != 0:
                raise RuntimeError(fetch.stderr.strip() or "git fetch thất bại.")
        source_state = git_state(root, config["source_branch"], f"origin/{config['source_branch']}")
        target_state = git_state(target, config["target_branch"], f"origin/{config['target_branch']}", target)
        issues: list[dict[str, Any]] = []
        issues.extend({"type": "source-git", "message": item} for item in source_state["issues"])
        issues.extend({"type": "target-git", "message": item} for item in target_state["issues"])
        issues.extend({"type": "target-symlink", "path": item} for item in scan_symlinks(target, True))
        manifest = build_manifest((root / config["output_dir"]).resolve(), config)
        issues.extend(manifest["issues"])
        diff = publish_diff(target, manifest, config)
        payload: dict[str, Any] = {
            "mode": args.command,
            "config_version": config["version"],
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "repo_root": str(root), "publish_worktree": str(target),
            "config": str(config_path.relative_to(root).as_posix()),
            "source": source_state, "target": target_state,
            "manifest": {key: value for key, value in manifest.items() if key != "issues"},
            "diff": diff, "issues": issues,
        }
        code = EXIT_UNSAFE if issues else EXIT_OK
        if args.command == "prepare":
            # Preflight must pass before rendering or touching the target worktree.
            allowed_changes = {
                "AGENTS.md", "publish_public.yml", "scripts/zo_publish.py",
                "quy_trinh_xay_dung/quy_trinh_xuat_ban_website.md",
            }
            source_status = {line[3:] for line in source_state["status"] if len(line) > 3}
            source_git_messages = [item for item in source_state["issues"] if item != "Working tree không sạch."]
            if source_status - allowed_changes:
                source_git_messages.append("Working tree có thay đổi ngoài phạm vi triển khai prepare.")
            preflight = [item for item in issues if item["type"] in {"target-git", "target-symlink"}]
            preflight.extend({"type": "source-git", "message": item} for item in source_git_messages)
            if preflight:
                code = EXIT_UNSAFE
            else:
                issues = []
                payload["issues"] = issues
                prepare = config["prepare"]
                audit = root / "_audit"
                stage = root / prepare["staging_dir"]
                render_dir, public_dir, backup_dir = stage / "render", stage / "public", stage / "backup"
                safe_remove_tree(stage, audit)
                stage.mkdir(parents=True)
                target_before = tree_manifest(target, True)
                copy_manifest(target, backup_dir, target_before)
                if tree_manifest(backup_dir) != target_before:
                    raise RestoreError("Backup worktree không khớp manifest ban đầu.")
                render = render_to_staging(root, render_dir)
                payload["render"] = render
                if render["exit_code"] != 0:
                    safe_remove_tree(stage, audit)
                    issues.append({"type": "render", "message": "Quarto render thất bại."})
                    code = EXIT_UNSAFE
                else:
                    render_manifest = tree_manifest(render_dir)
                    for special in prepare["special_files"]:
                        path = render_dir / special
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.touch()
                    selected_manifest = build_manifest(render_dir, config)
                    public_dir.mkdir(parents=True, exist_ok=True)
                    copy_manifest(render_dir, public_dir, selected_manifest)
                    public_manifest = tree_manifest(public_dir)
                    validation = validate_public(public_dir, public_manifest, config)
                    blocking_manifest_issues = [item for item in selected_manifest.get("issues", [])
                                                if item.get("type") != "forbidden-output"]
                    issues.extend(blocking_manifest_issues)
                    issues.extend(validation["issues"])
                    missing = [name for name in config["required_files"] if name not in public_manifest["files"]]
                    issues.extend({"type": "missing-required", "path": name} for name in missing)
                    target_diff = exact_diff(target_before, public_manifest)
                    payload.update({"render_manifest": render_manifest,
                                    "manifest": {**public_manifest, "excluded": selected_manifest["excluded"]},
                                    "validation": validation, "diff": target_diff,
                                    "target_before_manifest": target_before})
                    if issues:
                        code = EXIT_UNSAFE
                    else:
                        try:
                            sync_exact(public_dir, target, public_manifest, target_diff)
                            after = tree_manifest(target, True)
                            if after != public_manifest:
                                raise RestoreError("Cây đích sau đồng bộ không khớp cây công khai.")
                            if git_text(target, "diff", "--cached", "--name-only", safe=target):
                                raise RestoreError("Prepare đã tác động Git index.")
                            payload["target_after_manifest"] = after
                            code = EXIT_OK
                        except Exception:
                            restore_from_backup(target, backup_dir, target_before)
                            raise
        payload["exit_code"] = code
        report_raw = args.report or (config["prepare"]["report_file"] if args.command == "prepare" else None)
        if report_raw:
            report = report_target(root, report_raw)
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
    except RestoreError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_RESTORE
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_UNSAFE


if __name__ == "__main__":
    raise SystemExit(main())

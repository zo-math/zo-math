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
REPORT_SCHEMA_VERSION = 1
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
    publish = data.get("publish")
    if not isinstance(publish, dict):
        raise ConfigError("Thiếu cấu hình publish.")
    if publish.get("report_schema_version") != REPORT_SCHEMA_VERSION:
        raise ConfigError(f"publish.report_schema_version phải bằng {REPORT_SCHEMA_VERSION}.")
    if publish.get("require_remote_source") is not True or publish.get("cleanup_after_success") is not True:
        raise ConfigError("Publish phải yêu cầu nguồn remote và dọn dữ liệu sau thành công.")
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
    remote_commit = git_text(root, "rev-parse", compare, safe=safe) if compare else None
    return {"path": str(root), "branch": current, "commit": commit, "remote_ref": compare,
            "remote_commit": remote_commit,
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


def build_manifest(output: Path, config: Mapping[str, Any], skip_git: bool = False) -> dict[str, Any]:
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
        if skip_git and base == output and ".git" in dirs:
            dirs.remove(".git")
        dirs[:] = [name for name in dirs if not (base / name).is_symlink()]
        for name in files:
            if skip_git and base == output and name == ".git":
                continue
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


def manifest_digest(manifest: Mapping[str, Any]) -> str:
    payload = json.dumps(manifest["files"], sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


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


def status_porcelain(root: Path, safe: Path | None = None) -> dict[str, str]:
    result = git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all", safe=safe)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Không đọc được Git status.")
    entries = [item for item in result.stdout.split("\0") if item]
    parsed: dict[str, str] = {}
    index = 0
    while index < len(entries):
        entry = entries[index]
        if len(entry) < 4:
            raise RuntimeError("Git status không đúng định dạng.")
        code, path = entry[:2], entry[3:]
        if "R" in code or "C" in code:
            raise RuntimeError("Không chấp nhận rename/copy trong cây đã prepare.")
        parsed[path.replace("\\", "/")] = code
        index += 1
    return parsed


def expected_worktree_status(diff: Mapping[str, Any]) -> dict[str, str]:
    expected = {path: "??" for path in diff["add"]}
    expected.update({path: " M" for path in diff["update"]})
    expected.update({path: " D" for path in diff["delete"]})
    return expected


def path_batches(paths: Sequence[str], limit: int = 100, char_limit: int = 24000) -> list[list[str]]:
    batches: list[list[str]] = []
    current: list[str] = []
    length = 0
    for path in paths:
        if current and (len(current) >= limit or length + len(path) + 1 > char_limit):
            batches.append(current)
            current, length = [], 0
        current.append(path)
        length += len(path) + 1
    if current:
        batches.append(current)
    return batches


def stage_paths(target: Path, paths: Sequence[str]) -> None:
    for batch in path_batches(paths):
        result = git(target, "add", "--", *batch, safe=target)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "Stage đường dẫn xuất bản thất bại.")


def unstage_paths(target: Path, paths: Sequence[str]) -> None:
    for batch in path_batches(paths):
        result = git(target, "restore", "--staged", "--", *batch, safe=target)
        if result.returncode != 0:
            raise RestoreError(result.stderr.strip() or "Không thể hoàn nguyên index xuất bản.")
    if git_text(target, "diff", "--cached", "--name-only", safe=target):
        raise RestoreError("Index xuất bản không trở lại trạng thái trống.")


def staged_name_status(target: Path) -> dict[str, str]:
    result = git(target, "diff", "--cached", "--name-status", "-z", "--no-renames", safe=target)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Không đọc được staged diff.")
    items = [item for item in result.stdout.split("\0") if item]
    if len(items) % 2:
        raise RuntimeError("Staged diff không đúng định dạng.")
    return {items[index + 1].replace("\\", "/"): items[index]
            for index in range(0, len(items), 2)}


def expected_staged_status(diff: Mapping[str, Any]) -> dict[str, str]:
    expected = {path: "A" for path in diff["add"]}
    expected.update({path: "M" for path in diff["update"]})
    expected.update({path: "D" for path in diff["delete"]})
    return expected


def validate_report_manifest(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict) or not isinstance(raw.get("files"), dict):
        raise RuntimeError("Báo cáo thiếu manifest công khai hợp lệ.")
    files: dict[str, dict[str, Any]] = {}
    for name, metadata in raw["files"].items():
        safe_name = safe_relative(name, "manifest")
        if safe_name != name or not isinstance(metadata, dict):
            raise RuntimeError(f"Manifest không hợp lệ: {name}")
        size, digest = metadata.get("size"), metadata.get("sha256")
        if not isinstance(size, int) or size < 0 or not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise RuntimeError(f"Metadata manifest không hợp lệ: {name}")
        files[name] = {"size": size, "sha256": digest}
    manifest = {"files": files, "count": len(files),
                "bytes": sum(item["size"] for item in files.values())}
    if raw.get("count") != manifest["count"] or raw.get("bytes") != manifest["bytes"]:
        raise RuntimeError("Số lượng hoặc dung lượng manifest không nhất quán.")
    return manifest


def load_prepare_report(root: Path, config_path: Path, config: Mapping[str, Any]) -> tuple[Path, dict[str, Any]]:
    report = report_target(root, config["prepare"]["report_file"])
    if not report.is_file() or report.is_symlink():
        raise RuntimeError("Thiếu báo cáo prepare hợp lệ; hãy chạy lại prepare.")
    try:
        payload = json.loads(report.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Báo cáo prepare không đọc được: {exc}") from exc
    if not isinstance(payload, dict) or payload.get("schema_version") != config["publish"]["report_schema_version"]:
        raise RuntimeError("Schema báo cáo prepare không được hỗ trợ.")
    if payload.get("mode") != "prepare" or payload.get("exit_code") != EXIT_OK or payload.get("issues"):
        raise RuntimeError("Báo cáo không thuộc một lần prepare thành công.")
    if payload.get("config_version") != config["version"] or payload.get("config_sha256") != sha256(config_path):
        raise RuntimeError("Cấu hình xuất bản đã thay đổi sau prepare.")
    manifest = validate_report_manifest(payload.get("manifest"))
    if payload.get("manifest_sha256") != manifest_digest(manifest):
        raise RuntimeError("Hash tổng hợp manifest không khớp.")
    paths = payload.get("prepare_paths")
    stage = config["prepare"]["staging_dir"]
    expected_paths = {
        "staging_dir": stage,
        "render_dir": f"{stage}/render",
        "public_dir": f"{stage}/public",
        "backup_dir": f"{stage}/backup",
        "report_file": config["prepare"]["report_file"],
    }
    if paths != expected_paths:
        raise RuntimeError("Đường dẫn prepare trong báo cáo không khớp cấu hình.")
    for value in paths.values():
        if not safe_relative(value, "prepare_paths").startswith("_audit/"):
            raise RuntimeError("Báo cáo chứa đường dẫn prepare ngoài _audit/.")
    source, target = payload.get("source"), payload.get("target")
    if not isinstance(source, dict) or not isinstance(target, dict):
        raise RuntimeError("Báo cáo thiếu trạng thái Git nguồn hoặc đích.")
    for state in (source, target):
        if not re.fullmatch(r"[0-9a-f]{40}", str(state.get("commit", ""))):
            raise RuntimeError("Báo cáo chứa SHA Git không hợp lệ.")
        if not re.fullmatch(r"[0-9a-f]{40}", str(state.get("remote_commit", ""))):
            raise RuntimeError("Báo cáo thiếu SHA remote hợp lệ.")
    before = validate_report_manifest(payload.get("target_before_manifest"))
    diff = payload.get("diff")
    if not isinstance(diff, dict) or exact_diff(before, manifest) != diff:
        raise RuntimeError("Kế hoạch diff trong báo cáo không nhất quán.")
    validation = payload.get("validation")
    if not isinstance(validation, dict) or validation.get("issues"):
        raise RuntimeError("Validator trong báo cáo prepare chưa đạt.")
    payload["manifest"] = manifest
    payload["target_before_manifest"] = before
    return report, payload


def committed_manifest(target: Path, commit: str) -> dict[str, Any]:
    names = git_text(target, "ls-tree", "-r", "--name-only", commit, safe=target).splitlines()
    files: dict[str, dict[str, Any]] = {}
    for name in names:
        command = ["git", "-c", f"safe.directory={target.as_posix()}", "-C", str(target),
                   "show", f"{commit}:{name}"]
        result = subprocess.run(command, cwd=target, capture_output=True, check=False)
        if result.returncode != 0:
            raise RuntimeError(f"Không đọc được blob commit: {name}")
        files[name] = {"size": len(result.stdout), "sha256": hashlib.sha256(result.stdout).hexdigest()}
    return {"files": files, "count": len(files), "bytes": sum(item["size"] for item in files.values())}


def cleanup_prepare(root: Path, report: Path, config: Mapping[str, Any]) -> list[str]:
    warnings: list[str] = []
    stage = root / config["prepare"]["staging_dir"]
    try:
        safe_remove_tree(stage, root / "_audit")
    except (OSError, ConfigError) as exc:
        warnings.append(f"Không dọn được staging prepare: {exc}")
    try:
        if report.exists():
            report.unlink()
    except OSError as exc:
        warnings.append(f"Không xóa được báo cáo prepare: {exc}")
    return warnings


def validate_prepared_tree(root: Path, target: Path, config: Mapping[str, Any],
                           payload: Mapping[str, Any]) -> None:
    manifest = payload["manifest"]
    paths = payload["prepare_paths"]
    public = root / paths["public_dir"]
    backup = root / paths["backup_dir"]
    render = root / paths["render_dir"]
    if not public.is_dir() or not backup.is_dir() or not render.is_dir():
        raise RuntimeError("Thiếu staging, public tree hoặc backup của lần prepare.")
    if scan_symlinks(target, True) or scan_symlinks(public) or scan_symlinks(backup):
        raise RuntimeError("Phát hiện symlink trong cây prepare hoặc worktree xuất bản.")
    if tree_manifest(public) != manifest:
        raise RuntimeError("Public tree không khớp manifest trong báo cáo.")
    if tree_manifest(backup) != payload["target_before_manifest"]:
        raise RuntimeError("Backup prepare không khớp manifest đích ban đầu.")
    current = tree_manifest(target, True)
    if current != manifest or manifest_digest(current) != payload["manifest_sha256"]:
        raise RuntimeError("Worktree gh-pages không khớp manifest đã prepare.")
    selected = build_manifest(target, config, True)
    if selected["issues"]:
        raise RuntimeError("Worktree đã prepare chứa tệp cấm, quá lớn hoặc nhạy cảm.")
    selected_files = {name: {"size": item["size"], "sha256": item["sha256"]}
                      for name, item in selected["files"].items()}
    if selected_files != manifest["files"]:
        raise RuntimeError("Allowlist không tái tạo đúng manifest đã prepare.")
    validation = validate_public(target, manifest, config)
    if validation["issues"]:
        raise RuntimeError("Validator HTML hoặc tài nguyên không đạt trên worktree đã prepare.")
    missing = [name for name in config["required_files"] if name not in manifest["files"]]
    if missing or ".nojekyll" not in manifest["files"]:
        raise RuntimeError("Cây đã prepare thiếu tệp bắt buộc hoặc .nojekyll.")


def publish_site(root: Path, config_path: Path, config: Mapping[str, Any]) -> int:
    try:
        report, payload = load_prepare_report(root, config_path, config)
    except (RuntimeError, ConfigError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_UNSAFE
    fetch = git(root, "fetch", "--prune", "origin")
    if fetch.returncode != 0:
        print(f"ERROR: {fetch.stderr.strip() or 'git fetch thất bại.'}", file=sys.stderr)
        return EXIT_UNSAFE
    try:
        target = find_publish_worktree(root, config["target_branch"])
        source = git_state(root, config["source_branch"], f"origin/{config['source_branch']}")
        if source["issues"] or source["ahead"] != 0 or source["behind"] != 0:
            raise RuntimeError("Repository nguồn không sạch hoặc chưa đồng bộ remote.")
        expected_source = payload["source"]["commit"]
        if source["commit"] != expected_source or source["remote_commit"] != expected_source:
            raise RuntimeError("master hoặc origin/master đã thay đổi sau prepare.")
        if git_text(target, "branch", "--show-current", safe=target) != config["target_branch"]:
            raise RuntimeError("Worktree xuất bản không ở đúng nhánh gh-pages.")
        target_head = git_text(target, "rev-parse", "HEAD", safe=target)
        remote_target = git_text(root, "rev-parse", f"origin/{config['target_branch']}")
        expected_target = payload["target"]["commit"]
        if target_head != expected_target or remote_target != expected_target:
            raise RuntimeError("gh-pages hoặc origin/gh-pages đã thay đổi sau prepare.")
        if merge_in_progress(target, target):
            raise RuntimeError("Worktree xuất bản có thao tác Git dang dở.")
        if git_text(target, "diff", "--cached", "--name-only", safe=target):
            raise RuntimeError("Worktree xuất bản đã có staged diff.")
        expected_status = expected_worktree_status(payload["diff"])
        if status_porcelain(target, target) != expected_status:
            raise RuntimeError("Git status của worktree không khớp kế hoạch prepare.")
        validate_prepared_tree(root, target, config, payload)
        changed = [*payload["diff"]["add"], *payload["diff"]["update"], *payload["diff"]["delete"]]
        if not changed:
            warnings = cleanup_prepare(root, report, config)
            print("Website đã đồng bộ; không cần tạo commit hoặc push.")
            for warning in warnings:
                print(f"WARN: {warning}", file=sys.stderr)
            return EXIT_OK
        for variable in ("GIT_AUTHOR_IDENT", "GIT_COMMITTER_IDENT"):
            identity = git(target, "var", variable, safe=target)
            if identity.returncode != 0 or not identity.stdout.strip():
                raise MissingToolError("Thiếu danh tính Git hợp lệ để commit xuất bản.")
        try:
            stage_paths(target, changed)
            if staged_name_status(target) != expected_staged_status(payload["diff"]):
                raise RuntimeError("Staged diff không khớp kế hoạch prepare.")
            unstaged = git_text(target, "diff", "--name-only", safe=target)
            if unstaged:
                raise RuntimeError("Còn thay đổi unstaged sau khi stage kế hoạch xuất bản.")
            check = git(target, "diff", "--cached", "--check", safe=target)
            if check.returncode != 0:
                raise RuntimeError(check.stdout.strip() or check.stderr.strip() or "Staged whitespace không đạt.")
            indexed = set(git_text(target, "ls-files", safe=target).splitlines())
            if indexed != set(payload["manifest"]["files"]):
                raise RuntimeError("Index chứa tệp ngoài manifest công khai.")
        except Exception:
            unstage_paths(target, changed)
            raise
        short = expected_source[:12]
        subject = f"Publish website from master {short}"
        body = (f"Source-Master: {expected_source}\n\n"
                f"Previous-GH-Pages: {expected_target}\n\n"
                f"Publish-Config-SHA256: {payload['config_sha256']}")
        commit = git(target, "commit", "-m", subject, "-m", body, safe=target)
        if commit.returncode != 0:
            if git_text(target, "rev-parse", "HEAD", safe=target) == expected_target:
                unstage_paths(target, changed)
            else:
                raise RestoreError("Commit thất bại sau khi HEAD đã thay đổi.")
            raise RuntimeError(commit.stderr.strip() or "Không tạo được commit xuất bản.")
        new_commit = git_text(target, "rev-parse", "HEAD", safe=target)
        parents = git_text(target, "show", "-s", "--format=%P", new_commit, safe=target).split()
        if parents != [expected_target]:
            raise RestoreError("Commit xuất bản không có đúng parent dự kiến.")
        if git_text(target, "branch", "--show-current", safe=target) != config["target_branch"]:
            raise RestoreError("Commit xuất bản nằm sai nhánh.")
        if committed_manifest(target, new_commit) != payload["manifest"]:
            raise RestoreError("Cây commit không khớp manifest công khai.")
        if status_porcelain(target, target) or git_text(target, "diff", "--cached", "--name-only", safe=target):
            raise RestoreError("Worktree không sạch sau commit xuất bản.")
        push = git(target, "push", "origin", config["target_branch"], safe=target)
        if push.returncode != 0:
            print(f"ERROR: push bị từ chối; giữ commit local {new_commit}: {push.stderr.strip()}", file=sys.stderr)
            return EXIT_UNSAFE
        fetched = git(root, "fetch", "--prune", "origin")
        if fetched.returncode != 0:
            print(f"ERROR: push thành công nhưng fetch xác minh thất bại: {fetched.stderr.strip()}", file=sys.stderr)
            return EXIT_UNSAFE
        if git_text(root, "rev-parse", f"origin/{config['target_branch']}") != new_commit:
            raise RestoreError("origin/gh-pages không trỏ tới commit vừa push.")
        ahead_behind = git_text(target, "rev-list", "--left-right", "--count",
                                f"origin/{config['target_branch']}...HEAD", safe=target)
        if ahead_behind.split() != ["0", "0"]:
            raise RestoreError("gh-pages chưa đồng bộ 0/0 sau push.")
        if git_text(root, "rev-parse", config["source_branch"]) != expected_source or \
                git_text(root, "rev-parse", f"origin/{config['source_branch']}") != expected_source:
            raise RestoreError("master thay đổi trong quá trình publish.")
        warnings = cleanup_prepare(root, report, config)
        print(f"Đã xuất bản commit {new_commit} từ master {expected_source}.")
        for warning in warnings:
            print(f"WARN: {warning}", file=sys.stderr)
        return EXIT_OK
    except MissingToolError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_MISSING
    except RestoreError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_RESTORE
    except (RuntimeError, ConfigError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_UNSAFE


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
    value.add_argument("command", nargs="?", help="Hỗ trợ: check, prepare, publish")
    value.add_argument("--config", default="publish_public.yml")
    value.add_argument("--report")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command not in {"check", "prepare", "publish"}:
        print("ERROR: chỉ hỗ trợ lệnh 'check', 'prepare' và 'publish'.", file=sys.stderr)
        return EXIT_USAGE
    if yaml is None:
        print("ERROR: thiếu dependency PyYAML.", file=sys.stderr)
        return EXIT_MISSING
    try:
        root = repo_root()
        config_path, config = load_config(root, args.config)
        if args.command == "publish":
            return publish_site(root, config_path, config)
        if args.command == "prepare" and shutil.which("quarto") is None:
            raise MissingToolError("Không tìm thấy Quarto trong PATH.")
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
            "schema_version": REPORT_SCHEMA_VERSION,
            "mode": args.command,
            "config_version": config["version"],
            "config_sha256": sha256(config_path),
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
                payload["prepare_paths"] = {
                    "staging_dir": prepare["staging_dir"],
                    "render_dir": f"{prepare['staging_dir']}/render",
                    "public_dir": f"{prepare['staging_dir']}/public",
                    "backup_dir": f"{prepare['staging_dir']}/backup",
                    "report_file": prepare["report_file"],
                }
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
                                    "manifest_sha256": manifest_digest(public_manifest),
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

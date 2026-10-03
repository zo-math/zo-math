"""Safely check and prepare the public ZO Math website tree."""

from __future__ import annotations

import argparse
import copy
import difflib
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
import tempfile
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit
from typing import Any, Mapping, Sequence
from xml.etree import ElementTree

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
HTML_PRESERVE_WHITESPACE_TAGS = {"pre", "script", "style", "textarea"}
RENDER_SUPPORT_EXCLUDED_ROOTS = {"_audit", "docs", "tmp"}
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
    custom_domain = data.get("custom_domain")
    if not isinstance(custom_domain, dict):
        raise ConfigError("Thiếu custom_domain.")
    cname = custom_domain.get("cname")
    if not isinstance(cname, str) or not cname:
        raise ConfigError("custom_domain.cname phải là hostname có giá trị.")
    labels = cname.split(".")
    valid_hostname = (
        len(cname) <= 253
        and not any(character.isspace() for character in cname)
        and all(
            1 <= len(label) <= 63
            and re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?", label)
            for label in labels
        )
    )
    if not valid_hostname:
        raise ConfigError(
            "custom_domain.cname phải là hostname hợp lệ, không có scheme, "
            "port, path, query, fragment hoặc whitespace."
        )
    custom_domain["cname"] = cname
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
    path = normalized_public_path(path).casefold()
    normalized_prefixes = [normalized_public_path(item).casefold() for item in prefixes]
    return any(path == item or path.startswith(item + "/") for item in normalized_prefixes) or any(
        glob_match(path, pattern.replace("\\", "/").casefold()) for pattern in globs
    )


def decoded_reference(value: str) -> str:
    """Decode escaped/percent-encoded paths before policy and dot-segment checks."""
    previous = None
    while value != previous:
        previous = value
        value = unquote(unescape(value))
    return value.strip().replace("\\", "/")


def normalized_public_path(value: str) -> str:
    value = decoded_reference(value)
    try:
        value = urlsplit(value).path
    except ValueError:
        # Malformed URLs still must not bypass the private-path policy.
        value = value.split("?", 1)[0].split("#", 1)[0]
    return posixpath.normpath(value.lstrip("/")).lstrip("/")


def require_public_profile(root: Path) -> None:
    """Fail before fetch, render, worktree mutation or publication in preview mode."""
    profiles = re.split(r"[,\s]+", os.environ.get("QUARTO_PROFILE", ""))
    project_path = root / "_quarto.yml"
    if project_path.is_file():
        project = yaml.safe_load(project_path.read_text(encoding="utf-8")) or {}
        defaults = (project.get("profile") or {}).get("default", [])
        profiles.extend([defaults] if isinstance(defaults, str) else defaults)
    if any(str(profile).strip().casefold() == "on-thi-preview" for profile in profiles):
        raise ConfigError("Profile on-thi-preview chỉ dùng cục bộ; không được dùng với zo_publish.py.")


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


def write_text_lf(path: Path, text: str) -> None:
    """Write generated text deterministically without platform newline translation."""
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(text)


class PreserveWhitespaceTracker(HTMLParser):
    """Track HTML elements where changing horizontal whitespace can change content."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.casefold() in HTML_PRESERVE_WHITESPACE_TAGS:
            self.depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() in HTML_PRESERVE_WHITESPACE_TAGS and self.depth:
            self.depth -= 1


def changed_line_indexes(before: bytes, after: bytes) -> set[int]:
    """Return zero-based line indexes added or replaced in *after*."""
    before_lines = before.splitlines(keepends=True)
    after_lines = after.splitlines(keepends=True)
    indexes: set[int] = set()
    matcher = difflib.SequenceMatcher(None, before_lines, after_lines, autojunk=False)
    for operation, _, _, start, end in matcher.get_opcodes():
        if operation in {"insert", "replace"}:
            indexes.update(range(start, end))
    return indexes


def normalize_changed_html_whitespace(target: Path, candidate: Path,
                                      paths: Sequence[str]) -> dict[str, Any]:
    """Remove safe trailing spaces only from changed standalone HTML tag lines."""
    normalized: dict[str, int] = {}
    tag_line = re.compile(rb"^[ \t]*</?[A-Za-z][^<>\r\n]*>[ \t]+$")
    preserve_tag = re.compile(
        rb"</?(?:pre|script|style|textarea)(?:\s|/?>)", re.IGNORECASE,
    )
    for relative in sorted(set(paths)):
        if not relative.lower().endswith(".html"):
            continue
        candidate_path = candidate / relative
        if not candidate_path.is_file():
            continue
        before = (target / relative).read_bytes() if (target / relative).is_file() else b""
        after = candidate_path.read_bytes()
        changed = changed_line_indexes(before, after)
        if not changed:
            continue
        lines = after.splitlines(keepends=True)
        tracker = PreserveWhitespaceTracker()
        count = 0
        for index, line in enumerate(lines):
            body = line[:-1] if line.endswith(b"\n") else line
            ending = b"\n" if line.endswith(b"\n") else b""
            if body.endswith(b"\r"):
                body, ending = body[:-1], b"\r" + ending
            if (index in changed and tracker.depth == 0 and tag_line.fullmatch(body)
                    and not preserve_tag.search(body)):
                stripped = body.rstrip(b" \t")
                if stripped != body:
                    lines[index] = stripped + ending
                    count += 1
            tracker.feed(line.decode("utf-8", errors="replace"))
        tracker.close()
        if count:
            candidate_path.write_bytes(b"".join(lines))
            normalized[relative] = count
    return {"files": normalized, "lines": sum(normalized.values())}


def changed_trailing_whitespace(target: Path, candidate: Path,
                                manifest: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Report Git-style trailing whitespace only on candidate-added text lines."""
    issues: list[dict[str, Any]] = []
    for relative in sorted(manifest["files"]):
        if Path(relative).suffix.lower() not in TEXT_SUFFIXES:
            continue
        candidate_path = candidate / relative
        before = (target / relative).read_bytes() if (target / relative).is_file() else b""
        after = candidate_path.read_bytes()
        if before == after:
            continue
        lines = after.splitlines(keepends=True)
        for index in sorted(changed_line_indexes(before, after)):
            line = lines[index]
            body = line[:-1] if line.endswith(b"\n") else line
            if body.endswith((b" ", b"\t", b"\r")):
                issues.append({
                    "type": "trailing-whitespace", "path": relative, "line": index + 1,
                })
    return issues


def public_index_target(value: Any, relative: str, files: set[str],
                        config: Mapping[str, Any]) -> tuple[str | None, str]:
    """Resolve a structured public-index URL against the copied public manifest."""
    if not isinstance(value, str) or not value.strip():
        return None, "invalid-target"
    decoded = decoded_reference(value)
    try:
        parsed = urlsplit(decoded)
        port = parsed.port
    except ValueError:
        return None, "invalid-target"
    scheme = parsed.scheme.casefold()
    if scheme and scheme not in {"http", "https"}:
        return None, "unsupported-scheme"
    if parsed.netloc:
        hostname = (parsed.hostname or "").casefold()
        if hostname != config["custom_domain"]["cname"].casefold() or port not in {None, 80, 443}:
            return None, "external-target"
    path = parsed.path
    if re.match(r"^[A-Za-z]:", path):
        return None, "unsafe-target"
    trailing_slash = path.endswith("/")
    if path.startswith("/"):
        combined = path.lstrip("/")
    else:
        combined = str(PurePosixPath(relative).parent / path)
    normalized = posixpath.normpath(combined).lstrip("/")
    if normalized in {"", "."}:
        candidates = ["index.html"]
    elif normalized == ".." or normalized.startswith("../"):
        return normalized, "unsafe-target"
    elif trailing_slash:
        candidates = [f"{normalized}/index.html"]
    elif PurePosixPath(normalized).suffix:
        candidates = [normalized]
    else:
        candidates = [normalized, f"{normalized}/index.html"]
    deny = config["denylist"]
    for candidate in candidates:
        if path_denied(candidate, deny["paths"], deny["globs"]):
            return candidate, "denied-target"
    for candidate in candidates:
        if candidate in files:
            return candidate, "public-target"
    return candidates[-1], "missing-target"


def search_navigation_targets(record: Any) -> list[tuple[str, Any]]:
    """Return only fields that identify a search result's navigation target."""
    if not isinstance(record, dict):
        return []
    fields = [("href", record.get("href"))]
    if "objectID" in record:
        fields.append(("objectID", record.get("objectID")))
    return fields


def normalize_public_indexes(public: Path, manifest: Mapping[str, Any],
                             config: Mapping[str, Any]) -> dict[str, Any]:
    """Filter generated indexes using the exact file set copied into the public tree."""
    files = set(manifest["files"])
    report: dict[str, Any] = {"indexes": {}, "issues": []}
    search_relative = "search.json"
    if search_relative in files:
        search_path = public / search_relative
        try:
            records = json.loads(search_path.read_text(encoding="utf-8"))
            if not isinstance(records, list):
                raise ValueError("search.json root must be a list")
        except (OSError, UnicodeError, ValueError) as exc:
            report["issues"].append({
                "type": "invalid-public-index", "path": search_relative, "message": str(exc),
            })
        else:
            kept: list[Any] = []
            removed = Counter()
            for record in records:
                targets = search_navigation_targets(record)
                if not targets or not isinstance(targets[0][1], str) or not targets[0][1].strip():
                    removed["invalid-record"] += 1
                    continue
                resolved = [public_index_target(value, search_relative, files, config)
                            for _, value in targets]
                failure = next((reason for _, reason in resolved if reason != "public-target"), None)
                if failure:
                    removed[failure] += 1
                    continue
                if len({target for target, _ in resolved}) != 1:
                    removed["inconsistent-navigation"] += 1
                    continue
                kept.append(record)
            write_text_lf(search_path, json.dumps(kept, ensure_ascii=False, indent=2) + "\n")
            report["indexes"][search_relative] = {
                "before": len(records), "after": len(kept),
                "removed": len(records) - len(kept), "removed_by_reason": dict(sorted(removed.items())),
            }

    for relative in sorted(name for name in files
                           if PurePosixPath(name).name.lower().startswith("sitemap")
                           and name.lower().endswith(".xml")):
        path = public / relative
        try:
            tree = ElementTree.parse(path)
            root = tree.getroot()
        except (OSError, UnicodeError, ElementTree.ParseError) as exc:
            report["issues"].append({
                "type": "invalid-public-index", "path": relative, "message": str(exc),
            })
            continue
        namespace = root.tag[1:].split("}", 1)[0] if root.tag.startswith("{") else ""
        root_name = root.tag.rsplit("}", 1)[-1]
        entry_name = {"urlset": "url", "sitemapindex": "sitemap"}.get(root_name)
        if entry_name is None:
            report["issues"].append({
                "type": "invalid-public-index", "path": relative,
                "message": f"unsupported sitemap root: {root_name}",
            })
            continue
        entries = [node for node in list(root) if node.tag.rsplit("}", 1)[-1] == entry_name]
        removed = Counter()
        kept_count = 0
        for entry in entries:
            locs = [node for node in list(entry) if node.tag.rsplit("}", 1)[-1] == "loc"]
            if len(locs) != 1:
                root.remove(entry)
                removed["invalid-record"] += 1
                continue
            _, reason = public_index_target(locs[0].text, relative, files, config)
            if reason != "public-target":
                root.remove(entry)
                removed[reason] += 1
                continue
            kept_count += 1
        if namespace:
            ElementTree.register_namespace("", namespace)
        ElementTree.indent(tree, space="  ")
        xml = ElementTree.tostring(root, encoding="utf-8", xml_declaration=True,
                                   short_empty_elements=True)
        path.write_bytes(xml.rstrip(b"\r\n") + b"\n")
        report["indexes"][relative] = {
            "before": len(entries), "after": kept_count,
            "removed": len(entries) - kept_count, "removed_by_reason": dict(sorted(removed.items())),
        }
    return report


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


def private_references(text: str, relative: str, config: Mapping[str, Any]) -> list[str]:
    """Inspect literal paths too, not only clickable href/src attributes."""
    deny = config["denylist"]
    found: set[str] = set()
    # JSON strings are decoded separately below. This also handles escaped slashes
    # in inline HTML scripts and character references in text/attributes.
    tokens = re.findall(r'''[^\s"'<>`{}\[\](),;=]+''', unescape(text).replace("\\/", "/"))
    for token in tokens:
        decoded = decoded_reference(token)
        if "/" not in decoded and decoded not in deny["paths"]:
            continue
        candidate = normalized_public_path(decoded)
        local = normalized_public_path(str(PurePosixPath(relative).parent / candidate))
        if any(path_denied(item, deny["paths"], deny["globs"]) for item in (candidate, local)):
            found.add(token)
    return sorted(found)


def validate_public(public: Path, manifest: Mapping[str, Any], config: Mapping[str, Any]) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    files = set(manifest["files"])
    deny = config["denylist"]
    for relative in sorted(files):
        if path_denied(relative, deny["paths"], deny["globs"]):
            issues.append({"type": "forbidden-manifest", "path": relative})
    expected_cname = config["custom_domain"]["cname"]
    cname_path = public / "CNAME"
    if "CNAME" not in files:
        issues.append({"type": "missing-cname", "path": "CNAME"})
    elif not cname_path.is_file() or cname_path.is_symlink():
        issues.append({"type": "invalid-cname-file", "path": "CNAME"})
    else:
        try:
            cname_value = cname_path.read_text(encoding="utf-8").strip()
        except (OSError, UnicodeError) as exc:
            issues.append({"type": "invalid-cname-file", "path": "CNAME", "message": str(exc)})
        else:
            if cname_value != expected_cname:
                issues.append({
                    "type": "invalid-cname-value",
                    "path": "CNAME",
                    "expected": expected_cname,
                    "actual": cname_value,
                })
    html_count = link_count = 0
    for relative in sorted(name for name in files if name.lower().endswith(".html")):
        html_count += 1
        text = (public / relative).read_text(encoding="utf-8", errors="replace")
        issues.extend({"type": "private-reference", "path": relative, "value": value}
                      for value in private_references(text, relative, config))
        parser = LinkCollector()
        try:
            parser.feed(text)
            parser.close()
        except Exception as exc:
            issues.append({"type": "html-parse", "path": relative, "message": str(exc)})
            continue
        for kind, raw in parser.links:
            link_count += 1
            try:
                parsed = urlsplit(decoded_reference(raw))
            except ValueError:
                issues.append({"type": "unsafe-link", "path": relative, "value": raw})
                continue
            if parsed.scheme.lower() in {"http", "https", "mailto", "tel", "data", "javascript"} or raw.startswith("//"):
                continue
            decoded = parsed.path
            if not decoded:
                continue
            if re.match(r"^[A-Za-z]:", decoded):
                issues.append({"type": "unsafe-link", "path": relative, "value": raw})
                continue
            candidate = posixpath.normpath(decoded.lstrip("/")) if decoded.startswith("/") else posixpath.normpath(
                str(PurePosixPath(relative).parent / decoded)
            )
            if candidate == ".." or candidate.startswith("../"):
                issues.append({"type": "unsafe-link", "path": relative, "value": raw})
                continue
            if candidate not in files and not candidate.endswith("/"):
                issues.append({"type": "missing-resource", "path": relative, "value": raw})
            if path_denied(candidate, deny["paths"], deny["globs"]):
                issues.append({"type": "private-link", "path": relative, "value": raw})
    index_count = 0
    for relative in sorted(files):
        name = PurePosixPath(relative).name.lower()
        if name != "search.json" and not (name.startswith("sitemap") and name.endswith(".xml")):
            continue
        index_count += 1
        try:
            text = (public / relative).read_text(encoding="utf-8")
            if name == "search.json":
                records = json.loads(text)
                if not isinstance(records, list):
                    raise ValueError("search.json root must be a list")
                for position, record in enumerate(records):
                    targets = search_navigation_targets(record)
                    if not targets or not isinstance(targets[0][1], str) or not targets[0][1].strip():
                        issues.append({"type": "invalid-public-index-entry", "path": relative,
                                       "position": position})
                        continue
                    resolved: list[str] = []
                    for field, value in targets:
                        target, reason = public_index_target(value, relative, files, config)
                        if reason == "public-target":
                            resolved.append(target or "")
                        else:
                            issue_type = "private-reference" if reason == "denied-target" else "missing-index-target"
                            issues.append({"type": issue_type, "path": relative,
                                           "field": field, "value": value, "reason": reason})
                    if len(resolved) == len(targets) and len(set(resolved)) != 1:
                        issues.append({"type": "inconsistent-index-target", "path": relative,
                                       "position": position})
            else:
                root = ElementTree.fromstring(text)
                root_name = root.tag.rsplit("}", 1)[-1]
                entry_name = {"urlset": "url", "sitemapindex": "sitemap"}.get(root_name)
                if entry_name is None:
                    raise ValueError(f"unsupported sitemap root: {root_name}")
                entries = [node for node in list(root) if node.tag.rsplit("}", 1)[-1] == entry_name]
                for position, entry in enumerate(entries):
                    locs = [node for node in list(entry) if node.tag.rsplit("}", 1)[-1] == "loc"]
                    if len(locs) != 1:
                        issues.append({"type": "invalid-public-index-entry", "path": relative,
                                       "position": position})
                        continue
                    value = locs[0].text
                    _, reason = public_index_target(value, relative, files, config)
                    if reason != "public-target":
                        issue_type = "private-reference" if reason == "denied-target" else "missing-index-target"
                        issues.append({"type": issue_type, "path": relative,
                                       "value": value, "reason": reason})
        except (OSError, UnicodeError, ValueError, ElementTree.ParseError) as exc:
            issues.append({"type": "invalid-public-index", "path": relative, "message": str(exc)})
    return {"html_files": html_count, "local_links": link_count,
            "index_files": index_count, "issues": issues}


def render_to_staging(root: Path, render_dir: Path,
                      tool_root: Path | None = None) -> dict[str, Any]:
    require_public_profile(root)
    launcher = (tool_root or root) / "scripts/zo_quarto.py"
    command = [sys.executable, str(launcher), "render", "--output-dir", str(render_dir)]
    result = run(command, root)
    matches = re.findall(r"\[\s*\d+/(\d+)\]", result.stdout + result.stderr)
    return {"command": command, "exit_code": result.returncode,
            "source_count": int(matches[-1]) if matches else None,
            "stdout": result.stdout, "stderr": result.stderr}


def published_source_commit(root: Path, target: Path) -> str:
    """Read and validate the source commit recorded by the published target."""
    message = git_text(target, "show", "-s", "--format=%B", "HEAD", safe=target)
    matches = re.findall(r"(?im)^Source-Master:\s*([0-9a-f]{40,64})\s*$", message)
    if len(matches) != 1:
        raise ConfigError("Commit gh-pages phải có đúng một trailer Source-Master hợp lệ.")
    commit = git_text(root, "rev-parse", f"{matches[0]}^{{commit}}")
    ancestor = git(root, "merge-base", "--is-ancestor", commit, "HEAD")
    if ancestor.returncode != 0:
        raise ConfigError("Source-Master của gh-pages không phải tổ tiên của HEAD nguồn.")
    return commit


def copy_ignored_render_support(root: Path, destination: Path) -> dict[str, Any]:
    """Copy ignored build dependencies/caches, but never prior outputs or audit data."""
    result = git(root, "ls-files", "-z", "--others", "--ignored", "--exclude-standard")
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Không kiểm kê được tệp render support bị ignore.")
    copied: list[str] = []
    copied_bytes = 0
    excluded = Counter()
    for raw in result.stdout.split("\0"):
        if not raw:
            continue
        relative = safe_relative(raw, "ignored render support")
        parts = PurePosixPath(relative).parts
        if not parts or parts[0] in RENDER_SUPPORT_EXCLUDED_ROOTS:
            excluded["ephemeral-root"] += 1
            continue
        if "__pycache__" in parts or relative.lower().endswith((".pyc", ".pyo")):
            excluded["python-cache"] += 1
            continue
        source = root / relative
        if not source.is_file():
            continue
        if source.is_symlink():
            raise ConfigError(f"Từ chối render support symlink: {relative}")
        target = destination / relative
        if target.exists():
            if not target.is_file() or sha256(target) != sha256(source):
                raise ConfigError(f"Render support xung đột với baseline tracked: {relative}")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(relative)
        copied_bytes += source.stat().st_size
    return {
        "count": len(copied), "bytes": copied_bytes,
        "excluded": dict(sorted(excluded.items())), "files": copied,
    }


@contextmanager
def detached_source_tree(root: Path, destination: Path, commit: str, audit: Path):
    """Create a read-only-purpose detached worktree under _audit and always remove it."""
    resolved = destination.resolve()
    try:
        resolved.relative_to(audit.resolve())
    except ValueError as exc:
        raise ConfigError(f"Từ chối tạo baseline ngoài _audit/: {destination}") from exc
    if resolved.exists():
        raise ConfigError(f"Thư mục baseline phải chưa tồn tại: {destination}")
    added = git(root, "worktree", "add", "--detach", str(resolved), commit)
    if added.returncode != 0:
        raise RuntimeError(added.stderr.strip() or "Không tạo được worktree baseline.")
    try:
        yield resolved
    finally:
        removed = git(root, "worktree", "remove", "--force", str(resolved))
        if removed.returncode != 0:
            raise RestoreError(removed.stderr.strip() or "Không dọn được worktree baseline.")


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


def restricted_diff(before: Mapping[str, Any], after: Mapping[str, Any],
                    allowed: set[str]) -> dict[str, Any]:
    """Return exact differences only for paths justified by source provenance."""
    raw = exact_diff(before, after)
    added = [path for path in raw["add"] if path in allowed]
    updated = [path for path in raw["update"] if path in allowed]
    deleted = [path for path in raw["delete"] if path in allowed]
    old, new = before["files"], after["files"]
    return {
        "add": added,
        "update": updated,
        "delete": deleted,
        "unchanged": sorted((set(old) & set(new)) - set(updated)),
        "change_bytes": (sum(new[path]["size"] for path in [*added, *updated])
                         + sum(old[path]["size"] for path in deleted)),
    }


def qmd_output_path(path: str) -> str | None:
    suffix = PurePosixPath(path).suffix.casefold()
    if suffix not in {".qmd", ".rmd", ".md"}:
        return None
    return str(PurePosixPath(path).with_suffix(".html"))


def sidebar_records(value: Any) -> dict[str, Any]:
    records = value if isinstance(value, list) else [value]
    result: dict[str, Any] = {}
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            result[f"index:{index}"] = record
            continue
        identity = record.get("id") or record.get("title") or f"index:{index}"
        key = str(identity)
        if key in result:
            key = f"{key}#{index}"
        result[key] = record
    return result


def nested_hrefs(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "href" and isinstance(item, str):
                found.add(item.replace("\\", "/"))
            else:
                found.update(nested_hrefs(item))
    elif isinstance(value, list):
        for item in value:
            found.update(nested_hrefs(item))
    return found


def source_output_scope(root: Path, baseline_commit: str,
                        baseline_manifest: Mapping[str, Any],
                        rendered_manifest: Mapping[str, Any]) -> dict[str, Any]:
    """Infer publishable outputs from tracked source changes and declared dependencies."""
    changed_text = git_text(root, "diff", "--name-only", "--no-renames",
                            f"{baseline_commit}..HEAD")
    changed = {line.replace("\\", "/") for line in changed_text.splitlines() if line}
    available_outputs = set(baseline_manifest["files"]) | set(rendered_manifest["files"])
    allowed: set[str] = {path for path in changed if path in available_outputs}

    source_suffixes = {".css", ".html", ".js", ".json", ".lua", ".md", ".qmd",
                       ".r", ".rmd", ".yaml", ".yml"}
    source_texts: dict[str, str] = {}
    for current, dirs, files in os.walk(root):
        base = Path(current)
        if base == root:
            dirs[:] = [name for name in dirs
                       if name not in {".git", "_audit", "docs", "tmp"}]
        for name in files:
            path = base / name
            relative = path.relative_to(root).as_posix()
            if path.suffix.casefold() not in source_suffixes or path.is_symlink():
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace").replace("\\", "/")
            except OSError:
                continue
            dependency_lines = [
                line for line in text.splitlines()
                if re.search(r"(?i)(?:\binclude(?:s|-after-body|-before-body)?\b|"
                             r"\bmetadata-files?\b|\bfilters?\b)", line)
            ]
            source_texts[relative] = "\n".join(dependency_lines)

    affected = set(changed)
    while True:
        discovered: set[str] = set()
        for source, text in source_texts.items():
            if source in affected:
                continue
            parent = str(PurePosixPath(source).parent)
            for dependency in affected:
                relative = posixpath.relpath(dependency, parent).replace("\\", "/")
                if dependency in text or relative in text:
                    discovered.add(source)
                    break
        if not discovered:
            break
        affected.update(discovered)

    for source in affected:
        output = qmd_output_path(source)
        if output in available_outputs:
            allowed.add(output)

    config_scope: dict[str, Any] = {"sidebar_groups": [], "global": False}
    if "_quarto.yml" in changed:
        baseline_raw = git_text(root, "show", f"{baseline_commit}:_quarto.yml")
        baseline_config = yaml.safe_load(baseline_raw) or {}
        current_config = yaml.safe_load((root / "_quarto.yml").read_text(encoding="utf-8")) or {}
        baseline_sidebars = sidebar_records((baseline_config.get("website") or {}).get("sidebar", []))
        current_sidebars = sidebar_records((current_config.get("website") or {}).get("sidebar", []))
        for key in sorted(set(baseline_sidebars) | set(current_sidebars)):
            before = baseline_sidebars.get(key)
            after = current_sidebars.get(key)
            if before == after:
                continue
            config_scope["sidebar_groups"].append(key)
            for href in nested_hrefs(before) | nested_hrefs(after):
                output = qmd_output_path(href)
                if output in available_outputs:
                    allowed.add(output)
        baseline_global = copy.deepcopy(baseline_config)
        current_global = copy.deepcopy(current_config)
        (baseline_global.get("website") or {}).pop("sidebar", None)
        (current_global.get("website") or {}).pop("sidebar", None)
        if baseline_global != current_global:
            config_scope["global"] = True
            allowed.update(path for path in available_outputs if path.lower().endswith(".html"))

    if allowed:
        allowed.update(path for path in ("search.json", "sitemap.xml")
                       if path in available_outputs)
    return {
        "baseline_commit": baseline_commit,
        "changed_sources": sorted(changed),
        "affected_sources": sorted(affected),
        "config": config_scope,
        "allowed_outputs": sorted(allowed),
    }


def build_public_candidate(raw_output: Path, candidate: Path, target: Path,
                           config: Mapping[str, Any]) -> dict[str, Any]:
    """Build and validate the exact public tree without modifying either input tree."""
    if candidate.exists():
        raise ConfigError(f"Thư mục candidate phải chưa tồn tại: {candidate}")

    target_manifest = tree_manifest(target, True)
    selected = build_manifest(raw_output, config)
    special_files = set(config["prepare"]["special_files"])
    blocking = [
        item for item in selected["issues"]
        if item.get("type") not in {"forbidden-output", "missing-required"}
    ]

    candidate.mkdir(parents=True)
    copy_manifest(raw_output, candidate, selected)
    for relative in sorted(special_files):
        path = candidate / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()

    copied_manifest = tree_manifest(candidate)
    raw_diff = exact_diff(target_manifest, copied_manifest)
    html_whitespace = normalize_changed_html_whitespace(
        target, candidate, [*raw_diff["add"], *raw_diff["update"]],
    )
    copied_manifest = tree_manifest(candidate)
    normalization = normalize_public_indexes(candidate, copied_manifest, config)
    public_manifest = tree_manifest(candidate)
    policy_manifest = build_manifest(candidate, config)
    policy_files = {
        name: {"size": metadata["size"], "sha256": metadata["sha256"]}
        for name, metadata in policy_manifest["files"].items()
    }
    if policy_files != public_manifest["files"]:
        blocking.append({"type": "candidate-manifest-mismatch", "path": str(candidate)})
    blocking.extend(policy_manifest["issues"])
    blocking.extend(normalization["issues"])
    validation = validate_public(candidate, public_manifest, config)
    blocking.extend(validation["issues"])
    blocking.extend(changed_trailing_whitespace(target, candidate, public_manifest))

    return {
        "selected_manifest": selected,
        "public_manifest": public_manifest,
        "manifest": {**public_manifest, "excluded": selected["excluded"]},
        "manifest_sha256": manifest_digest(public_manifest),
        "index_normalization": normalization,
        "html_whitespace_normalization": html_whitespace,
        "validation": validation,
        "issues": blocking,
        "diff": exact_diff(target_manifest, public_manifest),
        "target_before_manifest": target_manifest,
    }


def build_scoped_candidate(baseline: Path, rendered: Path, candidate: Path, target: Path,
                           config: Mapping[str, Any],
                           excluded: Mapping[str, int] | None = None,
                           allowed_outputs: set[str] | None = None) -> dict[str, Any]:
    """Overlay only source-derived output changes onto the published target tree."""
    if candidate.exists():
        raise ConfigError(f"Thư mục candidate phải chưa tồn tại: {candidate}")
    baseline_manifest = tree_manifest(baseline)
    rendered_manifest = tree_manifest(rendered)
    target_manifest = tree_manifest(target, True)
    raw_source_diff = exact_diff(baseline_manifest, rendered_manifest)
    source_diff = (restricted_diff(baseline_manifest, rendered_manifest, allowed_outputs)
                   if allowed_outputs is not None else raw_source_diff)
    render_diff = exact_diff(target_manifest, rendered_manifest)

    candidate.mkdir(parents=True)
    copy_manifest(target, candidate, target_manifest)
    sync_exact(rendered, candidate, rendered_manifest, source_diff)

    public_manifest = tree_manifest(candidate)
    policy_manifest = build_manifest(candidate, config)
    policy_files = {
        name: {"size": metadata["size"], "sha256": metadata["sha256"]}
        for name, metadata in policy_manifest["files"].items()
    }
    blocking: list[dict[str, Any]] = list(policy_manifest["issues"])
    if policy_files != public_manifest["files"]:
        blocking.append({"type": "candidate-manifest-mismatch", "path": str(candidate)})
    validation = validate_public(candidate, public_manifest, config)
    blocking.extend(validation["issues"])
    blocking.extend(changed_trailing_whitespace(target, candidate, public_manifest))

    source_changed = set(source_diff["add"] + source_diff["update"] + source_diff["delete"])
    render_changed = set(render_diff["add"] + render_diff["update"] + render_diff["delete"])
    preserved_render_drift = sorted(render_changed - source_changed)
    final_diff = exact_diff(target_manifest, public_manifest)
    final_changed = set(final_diff["add"] + final_diff["update"] + final_diff["delete"])
    unexpected = sorted(final_changed - source_changed)
    blocking.extend({"type": "output-scope", "path": path} for path in unexpected)

    return {
        "baseline_manifest": baseline_manifest,
        "rendered_public_manifest": rendered_manifest,
        "raw_source_output_diff": raw_source_diff,
        "source_output_diff": source_diff,
        "render_diff_before_scope": render_diff,
        "preserved_render_drift": preserved_render_drift,
        "public_manifest": public_manifest,
        "manifest": {**public_manifest, "excluded": dict(excluded or {})},
        "manifest_sha256": manifest_digest(public_manifest),
        "validation": validation,
        "issues": blocking,
        "diff": final_diff,
        "target_before_manifest": target_manifest,
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
    require_public_profile(root)
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
    print(f"DIFF: added={len(diff.get('add', []))} modified={len(diff.get('update', []))} "
          f"deleted={len(deleted)} unchanged={len(diff.get('unchanged', []))}")
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
        require_public_profile(root)
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
        payload: dict[str, Any] = {
            "schema_version": REPORT_SCHEMA_VERSION,
            "mode": args.command,
            "config_version": config["version"],
            "config_sha256": sha256(config_path),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "repo_root": str(root), "publish_worktree": str(target),
            "config": str(config_path.relative_to(root).as_posix()),
            "source": source_state, "target": target_state,
            "manifest": {}, "diff": {}, "issues": issues,
            "validation": {},
        }
        if args.command == "check":
            raw_output = (root / config["output_dir"]).resolve()
            with tempfile.TemporaryDirectory(prefix="zo_publish_check_") as temporary:
                temporary_root = Path(temporary).resolve()
                for protected in (root.resolve(), target.resolve()):
                    try:
                        temporary_root.relative_to(protected)
                    except ValueError:
                        continue
                    raise ConfigError("Thư mục tạm của check phải nằm ngoài repository và worktree xuất bản.")
                candidate = temporary_root / "public"
                candidate_result = build_public_candidate(raw_output, candidate, target, config)
                issues.extend(candidate_result["issues"])
                payload.update({key: value for key, value in candidate_result.items()
                                if key not in {"issues", "selected_manifest", "public_manifest",
                                               "target_before_manifest"}})
            code = EXIT_UNSAFE if issues else EXIT_OK
        else:
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
                baseline_source_dir = audit / "_zpb"
                baseline_render_dir = stage / "baseline_render"
                baseline_public_dir = stage / "baseline_public"
                rendered_public_dir = stage / "rendered_public"
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
                baseline_commit = published_source_commit(root, target)
                payload["published_source_commit"] = baseline_commit
                with detached_source_tree(root, baseline_source_dir, baseline_commit, audit) as baseline_source:
                    payload["baseline_render_support"] = copy_ignored_render_support(
                        root, baseline_source,
                    )
                    baseline_render = render_to_staging(
                        baseline_source, baseline_render_dir, tool_root=root,
                    )
                payload["baseline_render"] = baseline_render
                if baseline_render["exit_code"] != 0:
                    safe_remove_tree(stage, audit)
                    issues.append({"type": "baseline-render",
                                   "message": "Quarto render baseline thất bại."})
                    code = EXIT_UNSAFE
                else:
                    render = render_to_staging(root, render_dir)
                    payload["render"] = render
                    if render["exit_code"] != 0:
                        safe_remove_tree(stage, audit)
                        issues.append({"type": "render", "message": "Quarto render thất bại."})
                        code = EXIT_UNSAFE
                    else:
                        payload["baseline_render_manifest"] = tree_manifest(baseline_render_dir)
                        payload["render_manifest"] = tree_manifest(render_dir)
                        baseline_candidate = build_public_candidate(
                            baseline_render_dir, baseline_public_dir, target, config,
                        )
                        rendered_candidate = build_public_candidate(
                            render_dir, rendered_public_dir, target, config,
                        )
                        issues.extend(baseline_candidate["issues"])
                        issues.extend(rendered_candidate["issues"])
                        output_scope = source_output_scope(
                            root, baseline_commit, baseline_candidate["public_manifest"],
                            rendered_candidate["public_manifest"],
                        )
                        payload["source_output_scope"] = output_scope
                        scoped_candidate = build_scoped_candidate(
                            baseline_public_dir, rendered_public_dir, public_dir, target, config,
                            rendered_candidate["manifest"].get("excluded", {}),
                            set(output_scope["allowed_outputs"]),
                        )
                        issues.extend(scoped_candidate["issues"])
                        if scoped_candidate["target_before_manifest"] != target_before:
                            issues.append({"type": "target-drift",
                                           "message": "Worktree xuất bản thay đổi trong khi prepare."})
                        payload["index_normalization"] = rendered_candidate["index_normalization"]
                        payload["html_whitespace_normalization"] = rendered_candidate[
                            "html_whitespace_normalization"
                        ]
                        payload.update({key: value for key, value in scoped_candidate.items()
                                        if key not in {"issues", "public_manifest"}})
                        if issues:
                            code = EXIT_UNSAFE
                        else:
                            safe_remove_tree(baseline_render_dir, audit)
                            safe_remove_tree(baseline_public_dir, audit)
                            safe_remove_tree(rendered_public_dir, audit)
                            try:
                                public_manifest = scoped_candidate["public_manifest"]
                                target_diff = scoped_candidate["diff"]
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

"""Keep historical audit files out of official compilation inputs."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from contextvars import ContextVar
import json
import os
from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
_active = ContextVar('official_build_root', default=None)
_installed = False
EXCLUDED = {'.git', '_audit', 'docs', '_freeze', '.quarto', '__pycache__',
            '_design', '_quy_trinh', 'node_modules'}
BUILD_KEYS = {'filters', 'resources', 'css', 'theme', 'include-in-header',
              'include-before-body', 'include-after-body', 'metadata-files',
              'bibliography', 'csl', 'reference-doc', 'pre-render', 'post-render',
              'execute-dir', 'template', 'logo', 'favicon'}
AUDIT_PATH = re.compile(r'(?i)(?:^|[/\\\s\"\'=(])_audit(?:[/\\]|$)')


def require_source(path: Path, root: Path = ROOT) -> Path:
    """Resolve before testing, so aliases and symlinks cannot hide audit inputs."""
    resolved = path.resolve()
    root = root.resolve()
    parts = resolved.relative_to(root).parts if resolved.is_relative_to(root) else resolved.parts
    if '_audit' in {part.casefold() for part in parts} or resolved.is_relative_to((root / '_audit').resolve()):
        raise ValueError('Official build cannot read an _audit input: ' + str(path))
    return resolved


def _io_guard(event, args):
    root = _active.get()
    if root is None:
        return
    if event == 'open':
        path, mode, flags = args
        if isinstance(path, int):
            return
        # Writes of new reports are allowed; reading existing history is not.
        reading = (isinstance(mode, str) and ('r' in mode or '+' in mode)) or (
            mode is None and (flags & (os.O_WRONLY | os.O_RDWR)) != os.O_WRONLY)
        if reading:
            require_source(Path(os.fsdecode(path)), root)
    elif event in {'os.listdir', 'os.scandir'} and args[0] is not None:
        if not isinstance(args[0], int):
            require_source(Path(os.fsdecode(args[0])), root)


@contextmanager
def official_inputs(root: Path = ROOT):
    """Guard Python file reads, including imported and dynamically loaded code."""
    global _installed
    if not _installed:
        sys.addaudithook(_io_guard)
        _installed = True
    token = _active.set(root.resolve())
    try:
        yield
    finally:
        _active.reset(token)


def _strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)


def _build_values(value):
    if isinstance(value, dict):
        for key, item in value.items():
            if key in BUILD_KEYS:
                yield from _strings(item)
            elif key == 'render':
                yield from (v for v in _strings(item) if not v.startswith('!'))
            else:
                yield from _build_values(item)
    elif isinstance(value, list):
        for item in value:
            yield from _build_values(item)


def check(root: Path = ROOT) -> dict:
    """Inspect renderable QMD/configuration, not historical review records."""
    root = root.resolve()
    errors, sources, pending = [], [], []
    for directory, names, files in os.walk(root):
        for name in [*names, *files]:
            candidate = Path(directory) / name
            if name not in EXCLUDED and candidate.is_symlink():
                try:
                    require_source(candidate, root)
                except ValueError as exc:
                    errors.append(str(exc))
        names[:] = [n for n in names if n not in EXCLUDED]
        for name in files:
            path = Path(directory) / name
            if path.suffix.lower() not in {'.qmd', '.rmd'} and not (
                name.startswith('_quarto') or name.startswith('_metadata')):
                continue
            if path.suffix.lower() not in {'.qmd', '.rmd', '.yml', '.yaml'}:
                continue
            pending.append(path)
    seen = set()
    while pending:
        path = pending.pop()
        try:
            path = require_source(path, root)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if path in seen:
            continue
        seen.add(path)
        label = path.relative_to(root).as_posix() if path.is_relative_to(root) else str(path)
        sources.append(label)
        text = path.read_text(encoding='utf-8-sig')
        markup = path.suffix.lower() in {'.qmd', '.rmd', '.md', '.html', '.tpl'}
        front = re.match(r'\A---\s*\n(.*?)\n---\s*(?:\n|$)', text, re.S) if markup else None
        try:
            config = yaml.safe_load(front.group(1) if front else (
                text if path.suffix.lower() in {'.yml', '.yaml'} else '')) or {}
        except yaml.YAMLError as exc:
            errors.append(label + ': invalid YAML: ' + str(exc))
            continue
        values = list(_build_values(config))
        if markup:
            values += re.findall(r'\{\{<\s*include\s+([^>]+?)\s*>\}\}', text)
            values += re.findall(r'(?:src|href)\s*=\s*[\"\']([^\"\']+)', text, re.I)
            values += re.findall(r'!?\[[^\]]*\]\(([^\s)]+)', text)
            values += re.findall(r'```\{(?:python|r|julia|bash|lua)[^\n]*\n(.*?)```', text, re.S | re.I)
        elif path.suffix.lower() in {'.lua', '.css', '.scss', '.tex'}:
            # These are executable/filter/style inputs, not review documents.
            values.append(text)
        for value in values:
            if AUDIT_PATH.search(value):
                errors.append(label + ': forbidden build input: ' + value[:300])
            elif not any(c in value for c in ('\n', '*', '<', '>')):
                candidate = path.parent / value.strip('"\'').split('#', 1)[0]
                try:
                    candidate = require_source(candidate, root)
                except ValueError as exc:
                    errors.append(label + ': ' + str(exc))
                    continue
                if candidate.is_file() and candidate.suffix.lower() in {
                    '.qmd', '.rmd', '.md', '.html', '.tpl', '.lua', '.css', '.scss', '.tex'}:
                    pending.append(candidate)
    return {'passed': not errors, 'sources_checked': len(sources), 'errors': errors}


def require_repository(root: Path = ROOT):
    result = check(root)
    if result['errors']:
        raise ValueError('\n'.join(result['errors']))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    result = check(args.root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return int(not result['passed'])


if __name__ == '__main__':
    raise SystemExit(main())

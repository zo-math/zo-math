"""Repo-wide end-of-day inventory, verified archival and bounded local commits.

This tool does not infer user authorization, owner acceptance, or file ownership.
The repository agent reviews the inventory and fills only the decision fields.
No render, network, push, publication, reset or automatic privilege elevation.
"""
from __future__ import annotations

import argparse
import ast
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = {'.git', '.agents', '.codex', '.aws'}


class Blocked(ValueError):
    pass


def native(path):
    text = str(Path(path).absolute())
    return '\\\\?\\' + text if os.name == 'nt' and not text.startswith('\\\\?\\') else text


def digest(path):
    h = hashlib.sha256()
    with open(native(path), 'rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def safe(root, relative):
    p = PurePosixPath(relative)
    if not relative or relative == '.' or p.is_absolute() or '\\' in relative or ':' in relative or '..' in p.parts:
        raise Blocked('Unsafe repository path: ' + relative)
    if p.as_posix() != relative or any(part.lower() in PRIVATE or part.endswith((' ', '.')) for part in p.parts):
        raise Blocked('Private or noncanonical path: ' + relative)
    target = root.joinpath(*p.parts)
    cursor = root
    for part in p.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise Blocked('Symlink: ' + relative)
        if cursor.exists() and getattr(cursor.lstat(), 'st_file_attributes', 0) & 0x400:
            raise Blocked('Reparse point: ' + relative)
    if not target.resolve().is_relative_to(root.resolve()):
        raise Blocked('Path escapes repository: ' + relative)
    return target


def git(root, *args, check=True):
    env = os.environ.copy()
    env.update(GIT_LITERAL_PATHSPECS='1', GIT_OPTIONAL_LOCKS='0')
    result = subprocess.run(['git', '-C', str(root), *args], env=env,
                            capture_output=True, check=False)
    if check and result.returncode:
        raise Blocked('Git failed (exit ' + str(result.returncode) + '): ' +
                      (result.stderr or result.stdout).decode('utf-8', 'replace').strip())
    return result


def names(data):
    return [s.decode('utf-8') for s in data.split(b'\0') if s]


def changes(root):
    records = names(git(root, 'status', '--porcelain=v1', '-z', '-uall').stdout)
    result = {}
    i = 0
    while i < len(records):
        record = records[i]
        state, path = record[:2], record[3:]
        result[path] = state
        if 'R' in state or 'C' in state:
            i += 1
            result[records[i]] = 'origin:' + state
        i += 1
    return result


def ignored(root):
    return sorted(p for p in names(git(root, 'ls-files', '--others', '--ignored',
                                       '--exclude-standard', '-z').stdout)
                  if not any(part.lower() in PRIVATE for part in PurePosixPath(p).parts))


def fingerprint(root, paths):
    def one(relative):
        path = safe(root, relative)
        if not path.exists():
            return relative, None
        if not stat.S_ISREG(path.lstat().st_mode):
            raise Blocked('Not a regular file: ' + relative)
        return relative, digest(path)
    with ThreadPoolExecutor(max_workers=8) as pool:
        return dict(pool.map(one, sorted(set(paths))))


def under(path, parent):
    return path == parent or path.startswith(parent + '/')


def scan(root, protection=(), manifests=(), exclude=()):
    root = root.resolve()
    if git(root, 'diff', '--cached', '--quiet', check=False).returncode:
        raise Blocked('Existing staged work: preserve it; do not take over the index')
    if git(root, 'ls-files', '-u').stdout:
        raise Blocked('Unmerged files')
    branch = git(root, 'symbolic-ref', '--quiet', '--short', 'HEAD').stdout.decode().strip()
    protected = set()
    manifest_hashes = {}
    for filename in manifests:
        path = Path(filename).resolve()
        data = json.loads(path.read_text(encoding='utf-8-sig'))
        manifest_hashes[str(path)] = digest(path)
        for entry in data['files']:
            safe(root, entry['path'])
            protected.add(entry['path'])
    for relative in protection:
        safe(root, relative)
    state = changes(root)
    hidden = [p for p in ignored(root) if p not in exclude]
    protected.update(p for p in hidden if any(under(p, prefix) for prefix in protection))
    instruction_paths = {'AGENTS.md', 'quy_trinh_xay_dung/quy_tac_lam_viec_voi_agent.md',
                         'quy_trinh_xay_dung/quy_trinh_thuc_hien_nhiem_vu_ky_thuat.md'}
    for relative in set(state) | set(hidden):
        for parent in PurePosixPath(relative).parents:
            instruction_paths.add((parent / 'AGENTS.md').as_posix())
    instruction_paths = {p for p in instruction_paths if (root / p).is_file()}
    all_paths = set(state) | set(hidden) | instruction_paths | {
        p for p in protected if safe(root, p).is_file()}
    return {'version': 1, 'root': str(root), 'head': git(root, 'rev-parse', 'HEAD').stdout.decode().strip(),
            'branch': branch, 'changes': state, 'ignored': hidden,
            'snapshot': fingerprint(root, all_paths), 'protected': sorted(protected),
            'protect_roots': list(protection), 'manifest_hashes': manifest_hashes,
            'instructions': sorted(instruction_paths), 'instructions_reviewed': [],
            'protection_reviewed': False, 'groups': [], 'keep': [], 'archive': []}


def validate(root, plan, exclude=()):
    if plan.get('version') != 1 or Path(plan['root']).resolve() != root.resolve():
        raise Blocked('Plan belongs to another repository or version')
    if not plan.get('protection_reviewed') or set(plan.get('instructions_reviewed', [])) != set(plan['instructions']):
        raise Blocked('Agent must read instructions and review protection before closing')
    current = scan(root, plan['protect_roots'], plan['manifest_hashes'], exclude)
    for key in ('head', 'branch', 'changes', 'ignored', 'snapshot', 'protected', 'manifest_hashes', 'instructions'):
        if current[key] != plan[key]:
            raise Blocked('Repository changed since inventory: ' + key)
    covered = set()
    for group in plan['groups']:
        if group.get('state') not in {'in_progress', 'checked'} or not group.get('message', '').strip():
            raise Blocked('Each commit group needs a message and honest state')
        paths = group.get('paths', [])
        if not paths or len(paths) != len(set(paths)):
            raise Blocked('Empty or duplicate commit group')
        for relative in paths:
            safe(root, relative)
            if relative not in plan['changes'] or relative in covered:
                raise Blocked('Unrelated or multiply classified change: ' + relative)
            parts = PurePosixPath(relative).parts
            if parts[0] in {'_audit', 'docs', '.quarto', '_freeze'} or any(
                    part == '.env' or part.startswith('.env.') or part in {'id_rsa', 'id_ed25519'} for part in parts):
                raise Blocked('Generated/private input cannot enter a closing commit: ' + relative)
            covered.add(relative)
        # Staged renames/copies are already blocked by scan; unstaged deletion
        # plus creation must be grouped by the reviewing agent, not guessed.
        actual = [p for p in paths if not plan['changes'][p].startswith('origin:')]
        if not actual:
            raise Blocked('Group contains only rename origins')
        if group['state'] == 'checked' and not group.get('verification'):
            raise Blocked('Checked group needs the agent technical verification description')
    if covered != set(plan['changes']):
        raise Blocked('Every tracked/untracked change must have exactly one commit group')
    decisions = {}
    for action in ('keep', 'archive'):
        for entry in plan[action]:
            path = entry['path']
            safe(root, path)
            if not entry.get('reason', '').strip():
                raise Blocked('Retention/archive decision needs a reason')
            matches = [p for p in plan['ignored'] if under(p, path)]
            if not matches:
                raise Blocked('Decision matches no ignored file: ' + path)
            for p in matches:
                if p in decisions:
                    raise Blocked('Overlapping artifact decisions: ' + p)
                decisions[p] = action
    if set(decisions) != set(plan['ignored']):
        raise Blocked('Ignored files have not all been classified; do not call the repo clean')
    for path, action in decisions.items():
        if action == 'archive':
            if any(part == '.env' or part.startswith('.env.') or part in {'id_rsa', 'id_ed25519'}
                   for part in PurePosixPath(path).parts):
                raise Blocked('Do not automatically archive secrets: ' + path)
            if path in current['protected'] or any(under(path, p) for p in plan['protect_roots']):
                raise Blocked('Protected artifact cannot be removed: ' + path)
            if safe(root, path).stat().st_nlink != 1:
                raise Blocked('Hard-linked artifact: ' + path)
    return decisions


def save(path, data):
    path = Path(native(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(native(path), 'w', encoding='utf-8') as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def close(root, plan, archive_root, authorized=False, exclude=(), plan_path=None):
    if not authorized:
        raise Blocked('Only an explicit human end-of-day instruction authorizes apply')
    root = root.resolve()
    destination = Path(archive_root).resolve()
    if destination == destination.parent or destination.is_relative_to(root) or root.is_relative_to(destination):
        raise Blocked('Archive must be a dedicated directory outside the repository, not its parent/root')
    decisions = validate(root, plan, exclude)
    plan_hash = digest(plan_path) if plan_path else None
    run = destination / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ-') + uuid.uuid4().hex[:8])
    run.mkdir(parents=True, exist_ok=False)
    result = {'whole_repo_clean': False, 'git_clean': False, 'commits': [], 'archived': [],
              'retained': [p for p, action in decisions.items() if action == 'keep'],
              'archive': str(run), 'scope': 'end_of_day_preservation_not_owner_acceptance',
              'push_or_publication': False}
    save(run / 'plan.json', plan)
    if plan_path and json.loads(Path(plan_path).read_text(encoding='utf-8-sig')) != plan:
        raise Blocked('Local plan changed before archival; no repo mutation performed')
    try:
        # Verify all backups before any source artifact is removed.
        for relative, action in decisions.items():
            if action != 'archive':
                continue
            src = safe(root, relative)
            dst = Path(native(run / 'payload' / relative))
            dst.parent.mkdir(parents=True, exist_ok=True)
            if digest(src) != plan['snapshot'][relative]:
                raise Blocked('Artifact changed: ' + relative)
            shutil.copy2(native(src), native(dst))
            if digest(dst) != plan['snapshot'][relative]:
                raise Blocked('Archive verification failed: ' + relative)
            result['archived'].append({'path': relative, 'sha256': digest(dst), 'bytes': dst.stat().st_size})
        save(run / 'manifest.json', result['archived'])
        # Recheck the entire snapshot after potentially slow copying.
        validate(root, plan, exclude)
        if plan_path and digest(plan_path) != plan_hash:
            raise Blocked('Local plan changed during archival')
        expected_head = plan['head']
        for group in plan['groups']:
            paths = group['paths']
            if git(root, 'rev-parse', 'HEAD').stdout.decode().strip() != expected_head:
                raise Blocked('Another process changed HEAD; stop')
            for p in paths:
                if fingerprint(root, [p])[p] != plan['snapshot'][p]:
                    raise Blocked('Commit input changed: ' + p)
            whitespace = git(root, 'diff', '--check', '--', *paths, check=False)
            syntax_errors = []
            for p in paths:
                if p.endswith('.py') and safe(root, p).is_file():
                    try:
                        ast.parse(safe(root, p).read_text(encoding='utf-8-sig'), filename=p)
                    except (SyntaxError, UnicodeError) as exc:
                        syntax_errors.append(str(exc))
            if group['state'] == 'checked' and (whitespace.returncode or syntax_errors):
                raise Blocked('Checked group failed whitespace/Python syntax checks')
            if git(root, 'diff', '--cached', '--quiet', check=False).returncode:
                raise Blocked('Another process staged files; stop')
            # Literal, exact file pathspecs; never git add . or -A repository-wide.
            git(root, 'add', '--all', '--', *paths)
            staged = set(names(git(root, 'diff', '--cached', '--name-only', '-z', '--no-renames').stdout))
            if staged != set(paths):
                raise Blocked('Staged set differs from the exact commit group')
            if fingerprint(root, paths) != {p: plan['snapshot'][p] for p in paths}:
                raise Blocked('Input changed during staging; preserve index for inspection')
            staged_tree = git(root, 'write-tree').stdout.strip()
            prefix = 'wip(eod)' if group['state'] == 'in_progress' else 'checkpoint(eod)'
            parent = git(root, 'rev-parse', 'HEAD').stdout.decode().strip()
            git(root, 'commit', '-m', prefix + ': ' + group['message'])
            head = git(root, 'rev-parse', 'HEAD').stdout.decode().strip()
            expected_head = head
            result['commits'].append({'sha': head, 'state': group['state'], 'paths': paths,
                                      'verification': group.get('verification'),
                                      'whitespace_passed': not whitespace.returncode,
                                      'python_syntax_errors': syntax_errors})
            save(run / 'result.json', result)
            if git(root, 'rev-parse', 'HEAD^{tree}').stdout.strip() != staged_tree:
                raise Blocked('Hook/concurrent writer changed the staged tree; inspect saved commit')
            if git(root, 'rev-parse', 'HEAD^').stdout.decode().strip() != parent:
                raise Blocked('Unexpected commit parent')
            committed = set(names(git(root, 'diff-tree', '--no-commit-id', '--name-only',
                                     '-r', '-z', '--no-renames', 'HEAD').stdout))
            if committed != set(paths):
                raise Blocked('Commit scope differs from approved paths')
            if fingerprint(root, paths) != {p: plan['snapshot'][p] for p in paths}:
                raise Blocked('Source changed during commit; stop before removing artifacts')
        if changes(root):
            raise Blocked('Uncommitted changes remain or appeared during closing')
        if plan_path and digest(plan_path) != plan_hash:
            raise Blocked('Local plan changed; keep local plan and artifacts')
        retained_snapshot = {p: h for p, h in plan['snapshot'].items()
                             if p not in decisions or decisions[p] == 'keep'}
        if fingerprint(root, retained_snapshot) != retained_snapshot:
            raise Blocked('Retained/protected source changed; stop before removing artifacts')
        for entry in result['archived']:
            src = safe(root, entry['path'])
            if digest(src) != entry['sha256'] or digest(run / 'payload' / entry['path']) != entry['sha256']:
                raise Blocked('Input/archive changed before removal: ' + entry['path'])
            src.unlink()
            parent = src.parent
            while parent != root:
                if any(under(parent.relative_to(root).as_posix(), p) for p in plan['protect_roots']):
                    break
                try:
                    parent.rmdir()
                except OSError:
                    break
                parent = parent.parent
        expected = set(result['retained'])
        if set(ignored(root)) - set(exclude) != expected or changes(root):
            raise Blocked('New/unclassified files appeared; day is not closed')
        if fingerprint(root, retained_snapshot) != retained_snapshot:
            raise Blocked('Retained/protected source changed during closing')
        if plan_path:
            if digest(plan_path) != plan_hash:
                raise Blocked('Local plan changed; retain it')
            Path(plan_path).unlink()
        if changes(root) or set(ignored(root)) - set(exclude) != expected or (plan_path and Path(plan_path).exists()):
            raise Blocked('Final repository state changed; inspect the archive receipt')
        result.update(whole_repo_clean=True, git_clean=True)
        return result
    except Exception as exc:
        result['error'] = str(exc)
        raise
    finally:
        save(run / 'result.json', result)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    scan_parser = sub.add_parser('scan', help='Read-only inventory unless --output is provided')
    scan_parser.add_argument('--protect', action='append', default=[])
    scan_parser.add_argument('--protect-manifest', action='append', default=[])
    scan_parser.add_argument('--output', type=Path)
    scan_parser.add_argument('--summary', action='store_true')
    for command in ('check', 'apply'):
        p = sub.add_parser(command)
        p.add_argument('--plan', type=Path, required=True)
        if command == 'apply':
            p.add_argument('--archive-root', type=Path, required=True)
            p.add_argument('--authorized-day-close', action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.command == 'scan':
            excluded = []
            if args.output:
                output = args.output.resolve()
                if not output.is_relative_to(ROOT / '_audit') or output.exists():
                    raise Blocked('Plan output must be a NEW file inside _audit')
                excluded = [output.relative_to(ROOT).as_posix()]
            plan = scan(ROOT, args.protect, args.protect_manifest, excluded)
            if args.output:
                save(args.output, plan)
            print(json.dumps({'changed_paths': len(plan['changes']), 'ignored_files': len(plan['ignored']),
                              'protected_files': len(plan['protected']), 'instructions': plan['instructions']}
                             if args.summary else plan, ensure_ascii=False, indent=2))
        else:
            plan_file = args.plan.resolve()
            if not plan_file.is_relative_to(ROOT / '_audit'):
                raise Blocked('Plan must be a temporary JSON file inside _audit')
            safe(ROOT, plan_file.relative_to(ROOT).as_posix())
            plan = json.loads(args.plan.read_text(encoding='utf-8-sig'))
            excluded = [args.plan.resolve().relative_to(ROOT).as_posix()]
            if args.command == 'check':
                actions = validate(ROOT, plan, excluded)
                print(json.dumps({'passed': True, 'groups': len(plan['groups']),
                                  'archive_files': sum(a == 'archive' for a in actions.values())}))
            else:
                result = close(ROOT, plan, args.archive_root, args.authorized_day_close, excluded, args.plan)
                print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (Blocked, OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({'whole_repo_clean': False, 'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())

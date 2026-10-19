"""Offline regression tests in disposable Git repositories; no real repo closing."""
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import zo_end_day as eod


class EndDayTests(unittest.TestCase):
    def setUp(self):
        fixture_parent = eod.ROOT / '_audit'
        fixture_parent.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='zo-end-day-test-', dir=fixture_parent)
        self.base = Path(self.temp.name).resolve()
        self.fixture_parent = fixture_parent.resolve()
        self.addCleanup(self.cleanup_fixture)
        self.root = self.base / 'repo'
        self.root.mkdir()
        self.archive = self.base / 'archives'
        eod.git(self.root, 'init', '-b', 'main')
        eod.git(self.root, 'config', 'user.name', 'End Day Fixture')
        eod.git(self.root, 'config', 'user.email', 'fixture@example.invalid')
        eod.git(self.root, 'config', 'core.autocrlf', 'false')
        eod.git(self.root, 'config', 'commit.gpgsign', 'false')
        self.write('.gitignore', '_audit/\n__pycache__/\n')
        self.write('AGENTS.md', 'Fixture instructions\n')
        self.write('lesson.md', 'Initial content\n')
        eod.git(self.root, 'add', '--', '.gitignore', 'AGENTS.md', 'lesson.md')
        eod.git(self.root, 'commit', '-m', 'fixture baseline')
        self.head = eod.git(self.root, 'rev-parse', 'HEAD').stdout
        self.write('lesson.md', 'Work in progress\n')
        self.write('_audit/trash.txt', 'Recoverable bytes\n')
        self.write('_audit/review/preview.html', 'Keep visually reviewed preview\n')

    def cleanup_fixture(self):
        # Validate the exact disposable target before recursive fixture cleanup.
        if self.base.parent != self.fixture_parent or not self.base.name.startswith('zo-end-day-test-'):
            raise RuntimeError('Refusing cleanup outside the dedicated fixture directory')
        if Path(self.temp.name).is_symlink() or Path(self.temp.name).resolve() != self.base:
            raise RuntimeError('Fixture path changed; refusing recursive cleanup')
        self.temp.cleanup()

    def write(self, path, text):
        dest = self.root / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding='utf-8')

    def plan(self, **kwargs):
        plan = eod.scan(self.root, **kwargs)
        plan['instructions_reviewed'] = plan['instructions'][:]
        plan['protection_reviewed'] = True
        plan['groups'] = [{'state': 'in_progress', 'message': 'preserve lesson',
                           'paths': list(plan['changes'])}]
        plan['keep'] = [{'path': '_audit/review', 'reason': 'pending visual review'}]
        plan['archive'] = [{'path': '_audit/trash.txt', 'reason': 'unused test output'}]
        return plan

    def close(self, plan, **kwargs):
        return eod.close(self.root, plan, self.archive, authorized=True, **kwargs)

    def unchanged(self):
        self.assertEqual(eod.git(self.root, 'rev-parse', 'HEAD').stdout, self.head)
        self.assertTrue((self.root / '_audit/trash.txt').exists())

    def test_preview_dependencies_outside_protect_root_cannot_be_archived(self):
        self.write('_audit/review/preview.html','<link rel="stylesheet" href="../delivery/main.css"><a href="../delivery/book.pdf">Download</a>')
        self.write('_audit/delivery/main.css','@import "inner.css";')
        self.write('_audit/delivery/inner.css','@font-face{src:url(font.woff2)}')
        self.write('_audit/delivery/font.woff2','font fixture')
        self.write('_audit/delivery/book.pdf','PDF fixture')
        plan=self.plan(protection=['_audit/review'])
        plan['archive'].append({'path':'_audit/delivery','reason':'simulated mistaken cleanup'})
        self.assertIn('_audit/delivery/font.woff2',plan['protected'])
        self.assertIn('_audit/delivery/book.pdf',plan['protected'])
        with self.assertRaisesRegex(eod.Blocked,'Protected artifact'):
            eod.validate(self.root,plan)

    def test_missing_protected_preview_dependency_blocks_scan(self):
        self.write('_audit/review/preview.html','<link rel="stylesheet" href="../delivery/missing.css">')
        with self.assertRaisesRegex(eod.Blocked,'preview dependency'):
            eod.scan(self.root,protection=['_audit/review'])

    def test_scan_is_read_only(self):
        before = eod.git(self.root, 'status', '--porcelain=v1', '-z').stdout
        plan = eod.scan(self.root)
        self.assertEqual(plan['changes'], {'lesson.md': ' M'})
        self.assertEqual(len(plan['ignored']), 2)
        self.assertEqual(before, eod.git(self.root, 'status', '--porcelain=v1', '-z').stdout)
        self.unchanged()

    def test_authorization_required(self):
        with self.assertRaisesRegex(eod.Blocked, 'explicit human'):
            eod.close(self.root, self.plan(), self.archive)
        self.unchanged()
        self.assertFalse(self.archive.exists())

    def test_success_archives_and_keeps_protected_visual(self):
        plan = self.plan(protection=['_audit/review'])
        original = plan['snapshot']['_audit/trash.txt']
        result = self.close(plan)
        self.assertTrue(result['whole_repo_clean'])
        self.assertFalse(result['push_or_publication'])
        self.assertEqual(eod.changes(self.root), {})
        self.assertFalse((self.root / '_audit/trash.txt').exists())
        self.assertTrue((self.root / '_audit/review/preview.html').exists())
        self.assertEqual(eod.digest(Path(result['archive']) / 'payload/_audit/trash.txt'), original)
        self.assertTrue(eod.git(self.root, 'log', '-1', '--format=%s').stdout.startswith(b'wip(eod):'))
        self.assertEqual(eod.git(self.root, 'remote').stdout, b'')

    def test_protected_archive_blocked(self):
        plan = self.plan(protection=['_audit/review'])
        plan['keep'] = []
        plan['archive'] = [{'path': '_audit', 'reason': 'attempt bulk cleanup'}]
        with self.assertRaisesRegex(eod.Blocked, 'Protected'):
            self.close(plan)
        self.unchanged()

    def test_protected_manifest_blocked(self):
        manifest = self.base / 'protected.json'
        manifest.write_text(json.dumps({'files': [{'path': '_audit/trash.txt'}]}), encoding='utf-8')
        with self.assertRaisesRegex(eod.Blocked, 'Protected'):
            self.close(self.plan(manifests=[str(manifest)]))
        self.unchanged()

    def test_unclassified_ignored_blocked(self):
        plan = self.plan()
        plan['archive'] = []
        with self.assertRaisesRegex(eod.Blocked, 'not all been classified'):
            self.close(plan)
        self.unchanged()

    def test_overlapping_decisions_blocked(self):
        plan = self.plan()
        plan['keep'].append({'path': '_audit', 'reason': 'overlap'})
        with self.assertRaisesRegex(eod.Blocked, 'Overlapping'):
            self.close(plan)

    def test_stale_bytes_blocked(self):
        plan = self.plan()
        self.write('lesson.md', 'Later edit\n')
        with self.assertRaisesRegex(eod.Blocked, 'changed since inventory'):
            self.close(plan)
        self.unchanged()

    def test_new_file_blocked(self):
        plan = self.plan()
        self.write('_audit/new.txt', 'new artifact\n')
        with self.assertRaisesRegex(eod.Blocked, 'changed since inventory'):
            self.close(plan)

    def test_instruction_review_required(self):
        plan = self.plan()
        plan['instructions_reviewed'] = []
        with self.assertRaisesRegex(eod.Blocked, 'read instructions'):
            self.close(plan)

    def test_existing_index_preserved(self):
        eod.git(self.root, 'add', '--', 'lesson.md')
        before = eod.git(self.root, 'diff', '--cached').stdout
        with self.assertRaisesRegex(eod.Blocked, 'Existing staged work'):
            eod.scan(self.root)
        self.assertEqual(before, eod.git(self.root, 'diff', '--cached').stdout)

    def test_all_sources_must_be_classified(self):
        self.write('new.py', 'x = 1\n')
        plan = self.plan()
        plan['groups'][0]['paths'] = ['lesson.md']
        with self.assertRaisesRegex(eod.Blocked, 'exactly one commit group'):
            self.close(plan)

    def test_two_scoped_commits(self):
        self.write('new.py', 'x = 1\n')
        plan = self.plan()
        plan['groups'] = [plan['groups'][0], {'state': 'checked', 'message': 'add helper',
                          'paths': ['new.py'], 'verification': 'fixture syntax test'}]
        plan['groups'][0]['paths'] = ['lesson.md']
        result = self.close(plan)
        self.assertEqual([g['paths'] for g in result['commits']], [['lesson.md'], ['new.py']])
        self.assertTrue(result['whole_repo_clean'])

    def test_checked_invalid_python_not_committed(self):
        self.write('broken.py', 'def broken(\n')
        plan = self.plan()
        plan['groups'][0].update(state='checked', verification='attempted test')
        with self.assertRaisesRegex(eod.Blocked, 'syntax checks'):
            self.close(plan)
        self.unchanged()
        receipt = next(self.archive.glob('*/result.json'))
        self.assertFalse(json.loads(receipt.read_text(encoding='utf-8'))['whole_repo_clean'])

    def test_wip_preserves_known_syntax_failure(self):
        self.write('broken.py', 'def broken(\n')
        result = self.close(self.plan())
        self.assertTrue(result['whole_repo_clean'])
        self.assertTrue(result['commits'][0]['python_syntax_errors'])
        self.assertEqual(result['commits'][0]['state'], 'in_progress')

    def test_wrong_repository_plan_blocked(self):
        plan = self.plan()
        plan['root'] = str(self.base)
        with self.assertRaisesRegex(eod.Blocked, 'another repository'):
            self.close(plan)

    def test_unsafe_paths(self):
        for path in ('../lesson.md', '.', '/tmp/x', 'E:/x', 'a\\b', '.git/config', '.GIT/config', 'a../x'):
            with self.subTest(path=path), self.assertRaises(eod.Blocked):
                eod.safe(self.root, path)

    def test_archive_must_be_outside(self):
        for path in (self.root / '_audit/archive', self.base, self.root):
            with self.subTest(path=path), self.assertRaises(eod.Blocked):
                eod.close(self.root, self.plan(), path, authorized=True)
        self.unchanged()

    def test_cli_plan_is_removed_only_after_verified_close(self):
        excluded = ['_audit/end-day-plan.json']
        plan = self.plan(exclude=excluded)
        filename = self.root / excluded[0]
        eod.save(filename, plan)
        with patch.object(eod, 'ROOT', self.root), redirect_stdout(io.StringIO()):
            code = eod.main(['apply', '--plan', str(filename), '--archive-root', str(self.archive),
                             '--authorized-day-close'])
        self.assertEqual(code, 0)
        self.assertFalse(filename.exists())
        self.assertTrue(next(self.archive.glob('*/plan.json')).is_file())
        self.assertEqual(eod.changes(self.root), {})

    def test_hook_mutation_does_not_remove_artifacts(self):
        # Model a hook changing the index inside commit, portably without sh.
        original_git = eod.git

        def hook_git(root, *args, **kwargs):
            if args[0] == 'commit':
                self.write('lesson.md', 'Unexpected hook rewrite\n')
                original_git(root, 'add', '--', 'lesson.md')
            return original_git(root, *args, **kwargs)

        with patch.object(eod, 'git', hook_git), self.assertRaisesRegex(eod.Blocked, 'staged tree'):
            self.close(self.plan())
        self.assertTrue((self.root / '_audit/trash.txt').exists())
        receipt = json.loads(next(self.archive.glob('*/result.json')).read_text(encoding='utf-8'))
        self.assertFalse(receipt['whole_repo_clean'])
        self.assertEqual(len(receipt['commits']), 1)

    def test_copy_failure_keeps_originals(self):
        with patch.object(eod.shutil, 'copy2', side_effect=OSError('fixture copy failure')):
            with self.assertRaisesRegex(OSError, 'copy failure'):
                self.close(self.plan())
        self.unchanged()
        self.assertFalse(json.loads(next(self.archive.glob('*/result.json')).read_text(encoding='utf-8'))['whole_repo_clean'])

    def test_changed_manifest_is_rejected(self):
        manifest = self.base / 'protected.json'
        manifest.write_text(json.dumps({'files': []}), encoding='utf-8')
        plan = self.plan(manifests=[str(manifest)])
        manifest.write_text(json.dumps({'files': [{'path': '_audit/review/preview.html'}]}), encoding='utf-8')
        with self.assertRaisesRegex(eod.Blocked, 'changed since inventory'):
            self.close(plan)
        self.unchanged()

    def test_renamed_source_is_preserved(self):
        (self.root / 'lesson.md').rename(self.root / 'renamed.md')
        result = self.close(self.plan())
        self.assertTrue(result['whole_repo_clean'])
        self.assertEqual(set(result['commits'][0]['paths']), {'lesson.md', 'renamed.md'})
        self.assertEqual((self.root / 'renamed.md').read_text(encoding='utf-8'), 'Work in progress\n')

    def test_ignored_secret_is_not_archived(self):
        self.write('.gitignore', '_audit/\n__pycache__/\n.env\n')
        self.write('.env', 'FIXTURE_SECRET=not-a-real-secret\n')
        plan = self.plan()
        plan['archive'].append({'path': '.env', 'reason': 'attempt secret cleanup'})
        with self.assertRaisesRegex(eod.Blocked, 'archive secrets'):
            self.close(plan)
        self.unchanged()


    def active_review(self,missing=False):
        self.write('_audit/review/preview.html','<html><link rel="stylesheet" href="../delivery/style.css"><body>Review</body></html>')
        if not missing:
            self.write('_audit/delivery/style.css','@font-face {src:url(font.woff2)}')
            self.write('_audit/delivery/font.woff2','font fixture')
        self.write('content/course/_quy_trinh/ban_dang_duyet.json',json.dumps({'status':'pending_owner_review','entrypoints':['_audit/review/preview.html'],'files':[{'path':'_audit/review/preview.html'}]}))

    def test_owner_approved_outputs_remain_protected(self):
        self.active_review()
        path=self.root/'content/course/_quy_trinh/ban_dang_duyet.json'
        data=json.loads(path.read_text());data['status']='owner_approved';path.write_text(json.dumps(data))
        scan=eod.scan(self.root)
        self.assertIn('_audit/review/preview.html',scan['protected'])
        self.assertIn('_audit/delivery/font.woff2',scan['protected'])

    def test_active_review_auto_protected_without_flags(self):
        self.active_review();scan=eod.scan(self.root)
        self.assertTrue({'_audit/review/preview.html','_audit/delivery/style.css','_audit/delivery/font.woff2'}<=set(scan['protected']))

    def test_missing_active_review_dependency_blocks_scan(self):
        self.active_review(missing=True)
        with self.assertRaisesRegex(eod.Blocked,'dependency failed'):eod.scan(self.root)

    def test_active_review_cannot_be_archived(self):
        self.active_review();plan=self.plan();plan['archive'].append({'path':'_audit/delivery','reason':'mistaken cleanup'})
        with self.assertRaisesRegex(eod.Blocked,'Protected artifact'):eod.validate(self.root,plan)

    def test_active_review_hash_corruption_blocks_scan(self):
        self.active_review();path=self.root/'content/course/_quy_trinh/ban_dang_duyet.json';data=json.loads(path.read_text());data['files'][0]['sha256']='wrong';path.write_text(json.dumps(data))
        with self.assertRaisesRegex(eod.Blocked,'Active review file changed'):eod.scan(self.root)

    def test_external_graphics_dependency_is_verified(self):
        from unittest.mock import patch
        import hashlib
        self.active_review()
        self.write('graphics/graph/engine.py','official engine fixture')
        path=self.root/'content/course/_quy_trinh/ban_dang_duyet.json'
        data=json.loads(path.read_text());data['external_dependencies']=[{'path':'graph/engine.py','sha256':hashlib.sha256((self.root/'graphics/graph/engine.py').read_bytes()).hexdigest()}]
        path.write_text(json.dumps(data))
        with patch('zo_graphics.graphics_root',return_value=self.root/'graphics'):
            eod.scan(self.root)
            (self.root/'graphics/graph/engine.py').write_text('changed engine')
            with self.assertRaisesRegex(eod.Blocked,'External graphics source changed'):eod.scan(self.root)

    def test_removed_active_review_manifest_invalidates_plan(self):
        self.active_review();plan=self.plan();(self.root/'content/course/_quy_trinh/ban_dang_duyet.json').unlink()
        with self.assertRaisesRegex(eod.Blocked,'changed since inventory'):eod.validate(self.root,plan)


    def test_current_operating_preview_requires_active_manifest(self):
        self.write('_audit/current/index.html','<html><body>Current review</body></html>')
        self.write('content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/03_dieu_hanh_chuong_trinh.md','[Current](http://127.0.0.1:8877/_audit/current/index.html)')
        with self.assertRaisesRegex(eod.Blocked,'no active protection manifest'):eod.scan(self.root)

    def test_current_operating_preview_cannot_be_replaced_by_old_manifest(self):
        self.active_review()
        self.write('_audit/current/index.html','<html><body>New review</body></html>')
        self.write('content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/03_dieu_hanh_chuong_trinh.md','[Current](http://127.0.0.1:8877/_audit/current/index.html)')
        with self.assertRaisesRegex(eod.Blocked,'no active protection manifest'):eod.scan(self.root)

if __name__ == '__main__':
    unittest.main(verbosity=2)

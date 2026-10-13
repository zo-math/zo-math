"""Regression tests for official compilation independent of audit history."""
from __future__ import annotations
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from zo_build_boundary import ROOT, check, official_inputs, require_source


class BoundaryTests(unittest.TestCase):
    def setUp(self):
        (ROOT / '_audit').mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix='zo_boundary_', dir=ROOT/'_audit')
        self.root = Path(self.tmp.name)
        (self.root / '_audit').mkdir()
        (self.root / '_audit/old.txt').write_text('historical input', encoding='utf-8')

    def tearDown(self):
        self.tmp.cleanup()

    def test_build_without_audit_directory(self):
        (self.root / '_audit/old.txt').unlink()
        (self.root / '_audit').rmdir()
        (self.root / 'index.qmd').write_text('---\ntitle: Test\n---\nText', encoding='utf-8')
        self.assertTrue(check(self.root)['passed'])

    def test_history_cannot_change_source_check(self):
        first = check(self.root)
        (self.root / '_audit/old.qmd').write_text('---\n: invalid yaml [', encoding='utf-8')
        self.assertEqual(first, check(self.root))

    def test_rejects_include_resource_filter_and_executable_chunk(self):
        for text in [
            '{{< include _audit/old.qmd >}}',
            '---\nresources: [_audit/old.txt]\n---\nText',
            '---\nfilters: [_audit/old.lua]\n---\nText',
            '```{python}\nopen("_audit/old.txt").read()\n```',
            '![Figure](../' + self.root.name + '/_audit/old.svg)',
        ]:
            with self.subTest(text=text):
                (self.root / 'index.qmd').write_text(text, encoding='utf-8')
                self.assertFalse(check(self.root)['passed'])

    def test_audit_render_exclusion_is_allowed(self):
        (self.root / '_quarto.yml').write_text('project:\n  render: ["**/*.qmd", "!_audit/**"]', encoding='utf-8')
        self.assertTrue(check(self.root)['passed'])
        (self.root / '_quarto.yml').write_text('project:\n  render: ["_audit/*.qmd"]', encoding='utf-8')
        self.assertFalse(check(self.root)['passed'])

    def test_transitive_markdown_include_is_checked(self):
        (self.root / 'index.qmd').write_text('{{< include partial.md >}}', encoding='utf-8')
        (self.root / 'partial.md').write_text('![Old image](_audit/old.svg)', encoding='utf-8')
        self.assertFalse(check(self.root)['passed'])

    def test_quarto_cli_overrides_cannot_read_audit(self):
        from zo_quarto import require_arguments
        for args in [['render', '_audit/history.qmd'],
                     ['render', 'index.qmd', '--metadata-file', str(ROOT/'_audit/old.json')],
                     ['render', 'index.qmd', '--lua-filter='+str(ROOT/'_audit/old.lua')]]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                require_arguments(args)

    def test_official_vector_builder_rejects_audit_scratch(self):
        from zo_web_2027_figures import build
        with self.assertRaisesRegex(ValueError, 'inside .quarto'):
            build(ROOT/'_audit/old-vector-build')

    def test_runtime_blocks_reads_but_allows_new_reports(self):
        with official_inputs(self.root):
            with self.assertRaises(ValueError):
                (self.root / '_audit/old.txt').read_bytes()
            with self.assertRaises(ValueError):
                os.listdir(self.root / '_audit')
            (self.root / '_audit/report.json').write_text('{}', encoding='utf-8')
            with self.assertRaises(ValueError):
                (self.root / '_audit/report.json').read_text()
        self.assertEqual((self.root / '_audit/report.json').read_text(), '{}')

    def test_runtime_blocks_read_write_mode(self):
        with official_inputs(self.root):
            with self.assertRaises(ValueError):
                open(self.root / '_audit/old.txt', 'r+')

    def test_runtime_handles_native_open_flags_on_windows(self):
        path = self.root / '_audit/old.txt'
        with official_inputs(self.root):
            for flags in [os.O_RDONLY, os.O_RDWR]:
                with self.assertRaises(ValueError):
                    os.open(path, flags)
            descriptor = os.open(self.root / '_audit/new.txt', os.O_WRONLY | os.O_CREAT)
            os.close(descriptor)

    def test_alias_escape_is_blocked(self):
        with self.assertRaises(ValueError):
            require_source(self.root / 'assets/../_audit/old.txt', self.root)
        with self.assertRaises(ValueError):
            require_source(self.root / 'nested/_audit/old.txt', self.root)
        with self.assertRaises(ValueError):
            require_source(ROOT / '_audit/external-history.txt', self.root)

    def test_official_python_launcher_blocks_history(self):
        env = dict(os.environ, ZO_OFFICIAL_BUILD='1')
        cmd = [sys.executable, str(ROOT/'scripts/zo_python.py'), '-c',
               'from pathlib import Path; Path("_audit/old.txt").read_text()']
        # Run a copy of the launcher/guard rooted in the fixture repository.
        import shutil
        (self.root / 'scripts').mkdir()
        for name in ['zo_python.py', 'zo_build_boundary.py']:
            shutil.copyfile(ROOT/'scripts'/name, self.root/'scripts'/name)
        shutil.copytree(ROOT/'scripts/zo_build_runtime', self.root/'scripts/zo_build_runtime')
        env['PYTHONPATH'] = str(self.root/'scripts/zo_build_runtime')
        cmd[1] = str(self.root/'scripts/zo_python.py')
        result = subprocess.run(cmd, cwd=self.root, env=env, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Official build cannot read an _audit input', result.stderr)


if __name__ == '__main__':
    unittest.main()

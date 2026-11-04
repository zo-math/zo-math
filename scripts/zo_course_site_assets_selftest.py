"""Asset refresh must never certify changed or previously pending content."""
import hashlib
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from zo_course_site_assets import apply

class AssetRefreshTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        out = root/'docs'; out.mkdir()
        assets = out/'assets'; assets.mkdir()
        (out/'index.html').write_text('<p>Protected content</p>','utf-8')
        (assets/'app.js').write_text('old','utf-8')
        def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
        def save(p, data): p.write_text(json.dumps(data),'utf-8')
        self.prior = {'inputs':{'scripts/zo_course_site_sources/app.js':'old'},
            'outputs':{'index.html':sha(out/'index.html')},
            'assets':{'assets/app.js':sha(assets/'app.js')}, 'table_profiles':{}}
        self.current = {'scripts/zo_course_site_sources/app.js':'new'}
        self.pending = {'index.html':['scripts/zo_course_site_sources/app.js']}
        self.c = SimpleNamespace(OUT=out,ASSETS=assets)
        self.site = SimpleNamespace(ROOT=root,c=self.c,CURRENT=root/'record.json',sha=sha,save=save,
            live_inputs=lambda:self.current,scope_state=lambda prior:(None,None,self.pending,None),
            catalog_metadata=lambda:{},install_assets=lambda:(assets/'app.js').write_text('new','utf-8'))
        save(self.site.CURRENT,self.prior)

    def test_changed_qmd_is_rejected(self):
        self.current['lesson.qmd']='new'
        with self.assertRaisesRegex(ValueError,'Non-asset'):
            apply(self.site,Path('result.json'))
        self.assertEqual((self.c.ASSETS/'app.js').read_text(),'old')

    def test_previously_pending_content_is_rejected_even_if_global_inputs_match(self):
        self.pending['lesson.html']=['lesson.qmd']
        with self.assertRaisesRegex(ValueError,'Previously pending'):
            apply(self.site,Path('result.json'))

    def test_changed_html_is_rejected(self):
        (self.c.OUT/'index.html').write_text('<p>Unreviewed rewrite</p>')
        with self.assertRaisesRegex(ValueError,'HTML changed'):
            apply(self.site,Path('result.json'))

    def test_altered_output_asset_is_rejected(self):
        (self.c.ASSETS/'app.js').write_text('untracked output change')
        with self.assertRaisesRegex(ValueError,'outside builder'):
            apply(self.site,Path('result.json'))

    def test_asset_refresh_preserves_html_bytes(self):
        before=(self.c.OUT/'index.html').read_bytes()
        with patch('zo_course_site_scope.page_inputs',return_value={}),patch('zo_course_site_protection.refresh'):
            self.assertEqual(apply(self.site,Path('result.json')),0)
        self.assertEqual(before,(self.c.OUT/'index.html').read_bytes())
        self.assertEqual((self.c.ASSETS/'app.js').read_text(),'new')

    def test_asset_refresh_emits_portable_lines_without_changing_html(self):
        before=(self.c.OUT/'index.html').read_bytes()
        self.site.install_assets=lambda:(self.c.ASSETS/'app.js').write_bytes(b'first\r\nsecond\r\n')
        with patch('zo_course_site_scope.page_inputs',return_value={}),patch('zo_course_site_protection.refresh'):
            self.assertEqual(apply(self.site,Path('result.json')),0)
        self.assertEqual((self.c.ASSETS/'app.js').read_bytes(),b'first\nsecond\n')
        self.assertEqual((self.c.OUT/'index.html').read_bytes(),before)
        record=json.loads(self.site.CURRENT.read_text('utf-8'))
        self.assertEqual(record['shared_asset_refresh']['normalized_asset_line_endings'],['assets/app.js'])

if __name__=='__main__': unittest.main()

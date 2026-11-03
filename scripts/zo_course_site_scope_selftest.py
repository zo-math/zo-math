"""Local edits must not widen builds or certify unrelated pending pages."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import zo_course_site as site
from zo_course_site_scope import TABLES, page_inputs, baseline, merge_evidence, stale_pages


class ScopeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name).resolve();base=Path('content/thpt/on_thi_toan_thpt')
        self.c=SimpleNamespace(PAGES={k:base/'hoc_lieu'/k/'index.html' for k in ['r1_g01','r2_g02']},FOUNDATION=base/'hoc_lieu/_dung_chung/nen/f.html',HOME=base/'tot_nghiep_thpt/2027')
        self.c.PAGES['home']=self.c.HOME/'index.html'
        self.inputs={TABLES:'table-old','shared.css':'same'}
        self.meta={k:{'title':k,'r1-tables':[]} for k in self.c.PAGES}
        self.tables={'shared':'rule','pages':{'r1_g01':[1],'r2_g02':[2]}}
        for p in [*self.c.PAGES.values(),self.c.FOUNDATION]:
            q=self.root/p.with_suffix('.qmd');q.parent.mkdir(parents=True,exist_ok=True);q.write_text('---\ntitle: Test\n---\nText','utf-8')
            self.inputs[p.with_suffix('.qmd').as_posix()]='old'
        self.target=self.c.PAGES['r2_g02'].as_posix();self.other=self.c.PAGES['r1_g01'].as_posix()
        self.old=self.snapshot()
    def snapshot(self):return page_inputs(self.root,self.c,self.inputs,self.meta,self.tables)
    def test_typo_is_one_page(self):
        self.inputs[str(Path(self.target).with_suffix('.qmd')).replace('\\','/')]='new'
        self.assertEqual(set(stale_pages(self.old,self.snapshot())),{self.target})
    def test_table_and_local_metadata_are_one_page(self):
        self.tables['pages']['r2_g02'].append(3);self.inputs[TABLES]='new'
        self.meta['r2_g02']['r1-tables']=[{'id':'new-table'}]
        self.assertEqual(set(stale_pages(self.old,self.snapshot())),{self.target})
    def test_other_dirty_page_does_not_get_certified(self):
        self.inputs[self.c.PAGES['r1_g01'].with_suffix('.qmd').as_posix()]='dirty'
        current=self.snapshot();merged=merge_evidence(self.old,current,[self.target])
        self.assertEqual(set(stale_pages(merged,current)),{self.other})
        with patch.object(site,'c',self.c):site.validate_render_scope([Path(self.target).with_suffix('.qmd')])
    def test_shared_change_keeps_other_pages_pending(self):
        self.inputs['shared.css']='changed';current=self.snapshot()
        merged=merge_evidence(self.old,current,[self.target])
        self.assertNotIn(self.target,stale_pages(merged,current))
        self.assertIn(self.other,stale_pages(merged,current))
    def test_global_table_rule_really_affects_others(self):
        self.tables['shared']='new-rule'
        self.assertIn(self.other,stale_pages(self.old,self.snapshot()))
    def test_catalog_title_is_shared_but_table_metadata_is_not(self):
        self.meta['r2_g02']['title']='Changed title'
        self.assertIn(self.other,stale_pages(self.old,self.snapshot()))
    def test_added_and_deleted_private_asset(self):
        asset=(Path(self.target).parent/'hinh/new.svg').as_posix();self.inputs[asset]='new'
        new=self.snapshot();self.assertEqual(set(stale_pages(self.old,new)),{self.target})
        del self.inputs[asset];self.assertEqual(set(stale_pages(new,self.snapshot())),{self.target})
    def test_legacy_baseline_uses_known_table_bytes_only(self):
        record={'inputs':dict(self.inputs),'catalog_metadata':copy.deepcopy(self.meta)}
        self.assertEqual(baseline(self.root,self.c,record,self.inputs,self.tables),self.old)
        self.inputs[TABLES]='unknown-new'
        old=baseline(self.root,self.c,record,self.inputs,self.tables)
        self.assertIn(TABLES,old[self.target])
        self.assertNotEqual(old,self.snapshot())
    def test_unknown_source_rejected(self):
        with patch.object(site,'c',self.c),self.assertRaises(ValueError):site.validate_render_scope([Path('unknown.qmd')])
    def test_full_build_needs_explicit_opt_in(self):
        import io
        from contextlib import redirect_stderr
        with patch('zo_qmd.main') as render,redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):
            site.main(['build'])
        render.assert_not_called()
    def test_cli_dispatch_does_not_expand_one_page(self):
        source=site.c.PAGES['r2_g02'].with_suffix('.qmd').as_posix()
        with patch('zo_qmd.main',return_value=0) as render:
            self.assertEqual(site.main(['build','--page',source]),0)
        self.assertEqual(render.call_args.args[0],['render',source,'--html-only','--report','_audit/course_site_build.json'])
    def test_shared_include_reaches_both_consumers(self):
        shared=self.root/Path(self.target).parent.parent/'_dung_chung/shared.qmd'
        shared.parent.mkdir(parents=True,exist_ok=True);shared.write_text('Shared text','utf-8')
        for page in [self.target,self.other]:
            (self.root/Path(page).with_suffix('.qmd')).write_text('{{< include ../_dung_chung/shared.qmd >}}','utf-8')
        name=shared.relative_to(self.root).as_posix();self.inputs[name]='old';old=self.snapshot();self.inputs[name]='new'
        self.assertEqual(set(stale_pages(old,self.snapshot())),{self.target,self.other})
    def test_projection_writes_only_selected_page(self):
        from zo_course_site_sources import build
        from contextlib import ExitStack
        context=site.c;page=context.PAGES['r2_g02'];source=page.with_suffix('.qmd');out=self.root/'docs'
        (self.root/source).parent.mkdir(parents=True,exist_ok=True);(self.root/source).write_text('test','utf-8')
        untouched=out/context.PAGES['r1_g01'];untouched.parent.mkdir(parents=True,exist_ok=True);untouched.write_bytes(b'KEEP EXACT BYTES')
        utility=out/context.HOME/'chuyen-de.html';utility.parent.mkdir(parents=True,exist_ok=True);utility.write_bytes(b'KEEP UTILITY')
        native='<html><body><div class="reader-content"><p>Only this lesson</p></div></body></html>'
        with ExitStack() as stack:
            for obj,name,value in [(site,'ROOT',self.root),(site,'CURRENT',self.root/'record.json'),(context,'OUT',out),(context,'ASSETS',out/'assets')]:stack.enter_context(patch.object(obj,name,value))
            stack.enter_context(patch.object(site,'install_assets'))
            stack.enter_context(patch.object(site,'live_inputs',return_value={}))
            stack.enter_context(patch.object(site,'catalog_metadata',return_value={}))
            stack.enter_context(patch.object(site,'scope_state',return_value=({}, {page.as_posix():{}}, {}, {})))
            stack.enter_context(patch.object(context,'catalog',return_value=[{'id':'r2_g02'}]))
            stack.enter_context(patch.object(context,'finish',side_effect=lambda text,page:text))
            stack.enter_context(patch.object(build,'reader',return_value=(native,{})))
            stack.enter_context(patch('zo_course_site_protection.refresh'))
            self.assertEqual(site.project_rendered([source],self.root/'report.json',{page:native}),0)
        self.assertEqual(untouched.read_bytes(),b'KEEP EXACT BYTES')
        self.assertEqual(utility.read_bytes(),b'KEEP UTILITY')
        record=json.loads((self.root/'record.json').read_text('utf-8'))
        self.assertEqual(set(record['outputs']),{page.as_posix()})


if __name__=='__main__':unittest.main()

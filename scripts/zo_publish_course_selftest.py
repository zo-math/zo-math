"""Approved-output release regressions; no network or real publication."""
import copy
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch
import zo_publish as p
import zo_publish_course as course

ROOT = Path(__file__).resolve().parents[1]

class ApprovedCourseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='approved-publish-', dir=ROOT/'_audit')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.target = self.root/'target';self.docs=self.root/'docs'
        self.target.mkdir();self.docs.mkdir()
        self.config = copy.deepcopy(p.load_config(ROOT,'publish_public.yml')[1])
        self.config['required_files']=['CNAME']
        self.page='content/thpt/on_thi_toan_thpt/hoc_lieu/test/index.html'
        self.pdf='content/thpt/on_thi_toan_thpt/hoc_lieu/test/index.pdf'
        self.write(self.target,'CNAME','zomath.vn\n')
        self.write(self.target,'index.html','<html>unchanged outside course</html>')
        self.write(self.docs,self.page,'<html><title>Approved</title><div class="reader-content">Current text</div></html>')
        self.write(self.docs,self.pdf,'PDF fixture bytes')
        self.pdfs={self.pdf:p.sha256(self.docs/self.pdf)}
    def write(self,root,name,text):
        path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8')
    def candidate(self):
        return course.candidate(self.target,self.docs,self.root/'render',self.root/'public',[self.page],self.pdfs,self.config)
    def test_exact_approved_html_pdf_and_unrelated_page_preserved(self):
        result=self.candidate()
        self.assertFalse(result['issues'])
        course.require_exact_products(self.root/'public',self.docs,[self.page],self.pdfs)
        self.assertEqual((self.root/'public/index.html').read_bytes(),(self.target/'index.html').read_bytes())
    def test_changed_html_rejected(self):
        self.candidate();self.write(self.root/'public',self.page,'wrong HTML')
        with self.assertRaisesRegex(p.ConfigError,'HTML bytes changed'):
            course.require_exact_products(self.root/'public',self.docs,[self.page],self.pdfs)
    def test_changed_pdf_rejected(self):
        self.candidate();self.write(self.root/'public',self.pdf,'wrong PDF')
        with self.assertRaisesRegex(p.ConfigError,'PDF bytes changed'):
            course.require_exact_products(self.root/'public',self.docs,[self.page],self.pdfs)
    def test_missing_dependency_rejected(self):
        self.write(self.docs,self.page,'<div class="reader-content"><img src="absent.svg"></div>')
        with self.assertRaisesRegex(p.ConfigError,'Missing canonical dependencies'):self.candidate()
        self.assertFalse((self.root/'public').exists())
    def test_shared_asset_change_blocks_outside_page(self):
        self.write(self.target,'assets/css/common.css','old')
        self.write(self.target,'index.html','<link rel="stylesheet" href="assets/css/common.css">')
        self.write(self.docs,'assets/css/common.css','new')
        self.write(self.docs,self.page,'<div class="reader-content"><link rel="stylesheet" href="/assets/css/common.css"></div>')
        result=self.candidate()
        self.assertTrue(any(x['type']=='shared-asset-needs-pages' for x in result['issues']))
        self.assertEqual((self.target/'assets/css/common.css').read_text(),'old')
    def test_search_and_sitemap_keep_other_entries(self):
        old=[{'href':'index.html','title':'Keep','text':'Keep'},{'href':self.page,'title':'Old','text':'Old'}]
        self.write(self.target,'search.json',json.dumps(old))
        self.write(self.target,'sitemap.xml','<urlset><url><loc>https://zomath.vn/index.html</loc></url><url><loc>https://zomath.vn/'+self.page+'</loc></url></urlset>')
        self.candidate()
        records=json.loads((self.root/'public/search.json').read_text())
        self.assertEqual(records[0],old[0]);self.assertEqual(records[1]['text'],'Current text')
        self.assertIn('https://zomath.vn/index.html',(self.root/'public/sitemap.xml').read_text())
    def test_unsealed_dependency_rejected(self):
        with self.assertRaisesRegex(p.ConfigError,'Unsealed canonical dependency'):
            course.candidate(self.target,self.docs,self.root/'render',self.root/'public',[self.page],self.pdfs,self.config,{})
    def test_current_pdf_provenance_guard_not_skipped(self):
        with patch.object(p,'course_pdf_issues',return_value=[{'type':'stale-course-pdf'}]) as guard:
            result=self.candidate()
        guard.assert_called_once();self.assertTrue(any(x['type']=='stale-course-pdf' for x in result['issues']))
    def test_inherited_pdf_requires_existing_public_bytes(self):
        with self.assertRaisesRegex(p.ConfigError, 'existing public tree'):
            course.candidate(self.target,self.docs,self.root/'render',self.root/'public',
                             [self.page],self.pdfs,self.config,inherited_pdfs=self.pdfs)
    def test_inherited_pdf_checks_canonical_and_candidate_bytes(self):
        self.write(self.root,self.pdf,'PDF fixture bytes')
        self.assertFalse(p.inherited_pdf_issues(self.docs,{self.pdf},self.root,self.pdfs))
        self.write(self.docs,self.pdf,'changed public PDF')
        self.assertEqual(p.inherited_pdf_issues(self.docs,{self.pdf},self.root,self.pdfs)[0]['type'],
                         'inherited-course-pdf-bytes')
        self.write(self.docs,self.pdf,'PDF fixture bytes')
        self.write(self.root,self.pdf,'changed canonical PDF')
        self.assertTrue(p.inherited_pdf_issues(self.docs,{self.pdf},self.root,self.pdfs))
    def test_missing_inherited_pdf_rejected(self):
        self.assertTrue(p.inherited_pdf_issues(self.docs,set(),self.root,self.pdfs))
    def test_inheritance_cannot_use_committed_snapshot_mode(self):
        with self.assertRaisesRegex(p.ConfigError,'canonical approved-course'):
            p.validate_public(self.docs,{'files':{}},self.config,
                              source_root=self.root,inherited_course_pdfs=self.pdfs)
    def test_approved_mode_cannot_mix_render_or_other_commands(self):
        for args in [['check','--approved-course'],['prepare','--approved-course','--full-render'],['prepare','--approved-course','--page','index.html']]:
            with self.subTest(args=args),redirect_stderr(io.StringIO()):self.assertEqual(p.main(args),p.EXIT_USAGE)
    def test_final_gate_rechecks_owner_and_source(self):
        with patch.object(course,'verify_approved',side_effect=p.ConfigError('source changed')):
            with self.assertRaisesRegex(p.ConfigError,'source changed'):
                course.validate_receipt(self.root,self.target,self.config,{})
    def test_failed_sync_restores_original_public_tree(self):
        # Exercise the existing rollback implementation, including new files.
        before=p.tree_manifest(self.target)
        p.copy_manifest(self.target,self.root/'backup',before)
        self.write(self.target,'new.html','partial sync')
        self.write(self.target,'index.html','overwritten')
        p.restore_from_backup(self.target,self.root/'backup',before)
        self.assertEqual(p.tree_manifest(self.target),before)

if __name__=='__main__':unittest.main(verbosity=2)

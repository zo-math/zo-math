"""Routine HTML overwrite regressions. No network or real website changes."""
import copy
import json
import tempfile
import unittest
from types import SimpleNamespace
from pathlib import Path
from unittest.mock import patch
import zo_publish as p
import zo_publish_course as course
import zo_publish_course_html as html
from zo_course_site_sources import context as c

ROOT=Path(__file__).resolve().parents[1]


class HtmlOverwriteTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='course-html-',dir=ROOT/'_audit')
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.docs=self.root/'docs';self.target=self.root/'public'
        self.docs.mkdir();self.target.mkdir()
        self.page='content/thpt/on_thi_toan_thpt/hoc_lieu/test/index.html'
        self.pdf='content/thpt/on_thi_toan_thpt/hoc_lieu/test/index.pdf'
        self.write(self.target,'CNAME','zomath.vn\n')
        self.write(self.target,'index.html','<html>Other website page</html>')
        self.write(self.target,self.pdf,'existing public PDF')
        self.write(self.docs,self.pdf,'different local PDF, not part of HTML update')
        self.write(self.docs,self.page,'<html><title>New</title><div class="reader-content">New page<a href="index.pdf">Download</a></div></html>')
        self.write(self.target,self.page,'<html>Old page</html>')
        self.record=self.root/c.HOME/'_quy_trinh/ho_so/current_site_build.json'
        self.write(self.root,self.record.relative_to(self.root).as_posix(),json.dumps({'outputs':{self.page:p.sha256(self.docs/self.page)}}))
        self.config=copy.deepcopy(p.load_config(ROOT,'publish_public.yml')[1])
        self.config['required_files']=['CNAME']
        self.pages=patch.object(html,'course_pages',return_value=[self.page]);self.pages.start();self.addCleanup(self.pages.stop)

    def write(self,root,name,text):
        path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8')

    def snapshot(self):return html.snapshot(self.root,self.target)

    def candidate(self,seal):
        return course.candidate(self.target,self.docs,self.root/'render',self.root/'candidate',
                                seal['pages'],{},self.config,seal['canonical_files'],preserved_pdfs=seal['preserved_pdfs'])

    def test_overwrite_html_keep_public_pdf_and_unrelated_page(self):
        seal=self.snapshot()
        self.assertFalse(any(name.endswith('.pdf') for name in seal['canonical_files']))
        with patch.object(p,'course_pdf_issues',return_value=[]) as pdf_guard:
            result=self.candidate(seal)
        self.assertFalse(result['issues'])
        self.assertNotIn(self.pdf,pdf_guard.call_args.args[1])
        self.assertEqual((self.root/'candidate'/self.page).read_bytes(),(self.docs/self.page).read_bytes())
        self.assertEqual((self.root/'candidate'/self.pdf).read_bytes(),(self.target/self.pdf).read_bytes())
        self.assertEqual((self.root/'candidate/index.html').read_bytes(),(self.target/'index.html').read_bytes())
        self.assertFalse((self.root/'render'/self.pdf).exists())
        self.assertFalse(result['diff']['delete'])

    def test_unbuilt_or_manually_changed_html_is_rejected(self):
        self.write(self.docs,self.page,'not produced by the builder')
        with self.assertRaisesRegex(p.ConfigError,'Build the changed'):self.snapshot()

    def test_change_after_prepare_is_rejected(self):
        seal=self.snapshot();self.write(self.docs,self.page,'changed after prepare')
        with self.assertRaises(p.ConfigError):html.verify_snapshot(self.root,seal)

    def test_new_pdf_cannot_slip_into_an_html_update(self):
        (self.target/self.pdf).unlink()
        with self.assertRaisesRegex(p.ConfigError,'explicit PDF release'):self.snapshot()

    def test_changed_public_pdf_is_rejected(self):
        seal=self.snapshot();self.write(self.target,self.pdf,'unexpected public PDF')
        with self.assertRaisesRegex(p.ConfigError,'existing public tree'):self.candidate(seal)

    def test_final_validator_rejects_changed_preserved_pdf(self):
        seal=self.snapshot();self.candidate(seal)
        self.write(self.root/'candidate',self.pdf,'changed during release')
        result=p.validate_public(self.root/'candidate',p.tree_manifest(self.root/'candidate'),self.config,
                                 preserved_course_pdfs=seal['preserved_pdfs'])
        self.assertTrue(any(x['type']=='preserved-course-pdf-bytes' for x in result['issues']))

    def test_cli_does_not_mix_html_overwrite_with_other_modes(self):
        for args in [['publish','--course-html'],['prepare','--course-html','--current-course'],
                     ['prepare','--course-html','--existing-course'],['prepare','--course-html','--page','index.html'],
                     ['prepare','--course-html','--with-pdfs']]:
            self.assertEqual(p.main(args),p.EXIT_USAGE)

    def test_final_receipt_uses_automatic_snapshot_not_dated_approval(self):
        seal=self.snapshot();payload={'approved_course':{'verification_mode':'course-html','approval_seal':seal}}
        with patch.object(html,'verify_snapshot',side_effect=p.ConfigError('snapshot changed')) as verifier:
            with self.assertRaisesRegex(p.ConfigError,'snapshot changed'):
                course.validate_receipt(self.root,self.target,self.config,payload)
        verifier.assert_called_once_with(self.root,seal)

    def test_page_prepare_routes_to_existing_files_without_quarto(self):
        state={'issues':[],'branch':'master','commit':'fixture'}
        with patch.object(p,'repo_root',return_value=self.root), \
             patch.object(p,'load_config',return_value=(self.root/'config.yml',self.config)), \
             patch.object(p,'require_public_profile'), \
             patch.object(p,'find_publish_worktree',return_value=self.target), \
             patch.object(p,'git',return_value=SimpleNamespace(returncode=0,stderr='')), \
             patch.object(p,'git_state',return_value=state), \
             patch.object(p.shutil,'which',side_effect=AssertionError('Publisher must not require a builder')), \
             patch.object(course,'prepare',return_value=0) as prepare:
            self.assertEqual(p.main(['prepare','--page',self.page]),0)
        self.assertTrue(prepare.call_args.args[4].built_pages)

    def test_rendering_release_flags_are_blocked_before_any_git_operation(self):
        with patch.object(p,'repo_root',side_effect=AssertionError('Must stop before Git')):
            for flags in [['--full-render'],['--page',self.page,'--committed-source'],
                          ['--page',self.page,'--video-only-page',self.page]]:
                self.assertEqual(p.main(['prepare',*flags]),p.EXIT_USAGE)

    def test_explicit_existing_pdf_is_selected_without_building(self):
        self.write(self.root,self.pdf,(self.docs/self.pdf).read_text('utf-8'))
        seal=html.snapshot(self.root,self.target,[self.page],pdfs=[self.pdf])
        self.assertEqual(seal['mode'],'built-pages')
        self.assertEqual(seal['pdfs'][self.pdf],p.sha256(self.docs/self.pdf))
        self.assertNotIn(self.pdf,seal['preserved_pdfs'])
        html.verify_snapshot(self.root,seal)

    def test_two_updates_overwrite_the_same_target_and_clean_temporary_copies(self):
        config_path=self.root/'publish_public.yml'
        config_path.write_text('fixture configuration',encoding='utf-8')
        args=p.parser().parse_args(['prepare','--course-html'])
        state={'issues':[],'branch':'master','commit':'fixture'}
        target_state={'issues':[],'branch':'gh-pages','commit':'public-fixture'}
        for text in ['First update','Second update']:
            self.write(self.docs,self.page,'<html><title>Latest</title><div class="reader-content">'+text+'<a href="index.pdf">PDF</a></div></html>')
            self.record.write_text(json.dumps({'outputs':{self.page:p.sha256(self.docs/self.page)}}),encoding='utf-8')
            with patch.object(p,'git_text',return_value=''):
                self.assertEqual(course.prepare(self.root,self.target,config_path,self.config,args,state,target_state),0)
            report=self.root/self.config['prepare']['report_file']
            payload=json.loads(report.read_text('utf-8'))
            course.validate_receipt(self.root,self.target,self.config,payload)
            self.assertIn(text,(self.target/self.page).read_text('utf-8'))
            self.assertEqual((self.target/self.pdf).read_text('utf-8'),'existing public PDF')
            self.assertFalse(p.cleanup_prepare(self.root,report,self.config))
            self.assertFalse(report.exists())
            self.assertFalse((self.root/self.config['prepare']['staging_dir']).exists())


if __name__=='__main__':unittest.main(verbosity=2)

"""Scoped PDF release guards, using disposable source/public trees only."""
import copy
import io
import json
from pathlib import Path
import shutil
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from contextlib import redirect_stdout, redirect_stderr

from pypdf import PdfWriter
import zo_publish as p
import zo_publish_pages as pages
import zo_publish_pdfs as pdfs
import zo_pdf_contract as contract
import zo_publish_pages_selftest as page_tests

ROOT = Path(__file__).resolve().parents[1]


class ScopedPdfTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.source = self.root / 'source'
        self.source.mkdir()
        self.config = copy.deepcopy(p.load_config(ROOT, 'publish_public.yml')[1])
        self.config['allowlist']['files'] += ['index.pdf', 'other.pdf', 'lesson.html', 'lesson.pdf']
        for relative in contract.CANONICAL_PDF_PIPELINE_INPUTS:
            self.write(self.source / relative, 'fixture pipeline input')
        self.write(self.source / 'index.qmd', 'Original text')
        self.write(self.source / 'lesson.qmd', 'Another source')
        self.make_pdf(self.source / 'index.pdf')
        self.make_pdf(self.source / 'lesson.pdf')
        contract.write_pdf_build_receipt(self.source, self.source/'index.qmd', self.source/'index.pdf')
        contract.write_pdf_build_receipt(self.source, self.source/'lesson.qmd', self.source/'lesson.pdf')

    @staticmethod
    def write(path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')

    @staticmethod
    def make_pdf(path):
        writer = PdfWriter()
        writer.add_blank_page(width=200, height=200)
        writer.write(path)

    def test_selects_only_requested_sources_and_sealed_evidence_survives_audit_cleanup(self):
        records = pdfs.selected_pdfs(self.source, ['lesson.qmd'])
        self.assertEqual([r['path'] for r in records], ['lesson.pdf'])
        self.assertEqual(pdfs.validate_pdfs(self.source, records, self.config), [])
        shutil.rmtree(self.source/'_audit')
        self.assertEqual(pdfs.validate_pdfs(self.source, records, self.config), [])

    def test_missing_receipt_and_stale_source_are_rejected(self):
        records = pdfs.selected_pdfs(self.source, ['index.qmd'])
        self.write(self.source/'index.qmd', 'Edited text needing a new PDF')
        self.assertTrue(pdfs.validate_pdfs(self.source, records, self.config))
        shutil.rmtree(self.source/'_audit')
        self.assertTrue(pdfs.validate_pdfs(self.source, pdfs.selected_pdfs(self.source, ['index.qmd']), self.config))

    def test_candidate_pdf_tampering_is_rejected(self):
        records = pdfs.selected_pdfs(self.source, ['index.qmd'])
        candidate = self.root/'candidate'
        candidate.mkdir()
        shutil.copyfile(self.source/'index.pdf', candidate/'index.pdf')
        self.assertEqual(pdfs.validate_pdfs(self.source, records, self.config, candidate), [])
        (candidate/'index.pdf').write_bytes(b'wrong bytes')
        self.assertTrue(pdfs.validate_pdfs(self.source, records, self.config, candidate))

    def test_registered_variant_paths_are_used_instead_of_guessed_filenames(self):
        config = SimpleNamespace(raw={'extensions': {'pdf_variants': {
            'full': {'output':'book.pdf'}, 'student': {'output':'student.pdf'}}}}, project_root=Path('.'))
        with patch.object(pdfs, 'discover_project_config', return_value=config), patch.object(contract, 'discover_project_config', return_value=config):
            records = pdfs.selected_pdfs(self.source, ['index.qmd'], evidence=False)
        self.assertEqual([r['path'] for r in records], ['book.pdf', 'student.pdf'])

    def test_candidate_updates_selected_pdf_and_preserves_unselected_outputs(self):
        fixture = page_tests.PageReleaseTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        config = fixture.config
        config['allowlist']['files'] += ['index.pdf']
        shutil.copyfile(self.source/'index.pdf', fixture.raw/'index.pdf')
        self.write(fixture.raw/'content/old.pdf','unrelated working PDF change')
        html=fixture.raw/'index.html'
        self.write(html,html.read_text(encoding='utf-8').replace('</body>','<a href="content/old.pdf">Reference</a></body>'))
        records = pdfs.selected_pdfs(self.source, ['index.qmd'])
        result = pages.candidate(fixture.target, fixture.raw, self.root/'candidate', ['index.html'],
                                 config, source=self.source, pdfs=records)
        self.assertEqual(result['issues'], [])
        self.assertEqual(set(result['diff']['add']), {'index.pdf', 'assets/test/page.css', 'assets/test/page.woff2', 'assets/test/OFL_Test.txt'})
        for name in ['content/other.html', 'content/old.pdf']:
            self.assertEqual((self.root/'candidate'/name).read_bytes(), (fixture.target/name).read_bytes())
        # A PDF from a different source must not be smuggled into the scope.
        with self.assertRaisesRegex(p.ConfigError, 'exactly the selected pages'):
            pages.candidate(fixture.target, fixture.raw, self.root/'wrong', ['index.html'],
                            config, source=self.source, pdfs=pdfs.selected_pdfs(self.source, ['lesson.qmd']))

    def test_stale_pdf_stops_prepare_before_any_render_or_public_mutation(self):
        records = pdfs.selected_pdfs(self.source, ['index.qmd'])
        self.write(self.source/'index.qmd', 'Changed after PDF build')
        config_path = self.source/'publish_public.yml'
        self.write(config_path, 'fixture')
        target = self.root/'public'
        target.mkdir()
        self.write(target/'index.html', 'published bytes')
        before = p.tree_manifest(target)
        state = {'issues': [], 'commit':'a'*40, 'status': []}
        args = SimpleNamespace(page=['index.html'], committed_source=False, with_pdfs=True, report=None)
        with patch.object(pages, 'require_page_scope', return_value='a'*40), patch.object(pages, 'render_pages', side_effect=AssertionError('must not render')), redirect_stdout(io.StringIO()):
            code = pages.prepare(self.source,target,config_path,self.config,args,state,state)
        self.assertEqual(code, 1)
        self.assertEqual(p.tree_manifest(target), before)
        self.assertFalse((self.source/self.config['prepare']['staging_dir']).exists())

    def test_full_site_build_requires_explicit_choice_before_git_or_render(self):
        with patch.object(p, 'repo_root', side_effect=AssertionError('must stop before repository operations')), redirect_stderr(io.StringIO()):
            self.assertEqual(p.main(['prepare']), p.EXIT_USAGE)
            self.assertEqual(p.main(['prepare', '--with-pdfs', '--full-render']), p.EXIT_USAGE)

    def test_prepare_validates_pdf_and_reuses_artifact_without_second_render(self):
        fixture = page_tests.PageReleaseTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        for cmd in [['git','init','-q'], ['git','add','.'],
                    ['git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','fixture']]:
            self.assertEqual(p.run(cmd,fixture.target).returncode,0)
        fixture.config['allowlist']['files'].append('index.pdf')
        config_path = self.source/'publish_public.yml'
        self.write(config_path,'fixture policy')
        inputs = {'index.qmd':p.sha256(self.source/'index.qmd')}
        seal = {'key':'pdf-fixture','inputs':inputs,'tools':{}}
        args = SimpleNamespace(page=['index.html'],committed_source=False,with_pdfs=True,report=None)
        state = {'issues':[],'commit':'a'*40,'status':[]}
        def render(root,destination,sources,tools):
            self.assertEqual(sources,['index.qmd'])
            shutil.copytree(fixture.raw,destination)
            return {'source_count':1,'exit_code':0}
        with patch.object(pages,'fingerprint',return_value=seal), patch.object(pages,'input_fingerprints',return_value=inputs), patch.object(pages,'require_page_scope',return_value='a'*40), patch.object(pages,'render_pages',side_effect=render) as renderer, redirect_stdout(io.StringIO()):
            self.assertEqual(pages.prepare(self.source,fixture.target,config_path,fixture.config,args,state,state),0)
            receipt=json.loads((self.source/fixture.config['prepare']['report_file']).read_text(encoding='utf-8'))
            self.assertEqual(receipt['page_release']['pdfs'][0]['path'],'index.pdf')
            p.validate_prepared_tree(self.source,fixture.target,fixture.config,receipt)
            self.assertEqual((fixture.target/'index.pdf').read_bytes(),(self.source/'index.pdf').read_bytes())
            self.assertEqual((fixture.target/'content/other.html').read_bytes(),b'<html><body>Keep</body></html>')
            p.safe_remove_tree(self.source/fixture.config['prepare']['staging_dir'],self.source/'_audit')
            self.assertEqual(pages.prepare(self.source,fixture.target,config_path,fixture.config,args,state,state),0)
            second=json.loads((self.source/fixture.config['prepare']['report_file']).read_text(encoding='utf-8'))
            self.assertTrue(second['page_release']['cache_hit'])
            self.assertEqual(renderer.call_count,1)
            (fixture.target/'index.pdf').write_bytes(b'tampered after prepare')
            with self.assertRaisesRegex(p.ConfigError,'drift'):
                p.validate_prepared_tree(self.source,fixture.target,fixture.config,second)

    def test_new_page_and_pdf_need_no_page_specific_engine_changes(self):
        fixture = page_tests.PageReleaseTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        for cmd in [['git','init','-q'],['git','add','.'],
                    ['git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','fixture']]:
            self.assertEqual(p.run(cmd,fixture.target).returncode,0)
        source = 'content/thpt/chuyen_de_moi/bai_moi.qmd'
        page = source[:-4]+'.html'
        pdf = source[:-4]+'.pdf'
        self.write(self.source/source,'New page text')
        self.make_pdf(self.source/pdf)
        contract.write_pdf_build_receipt(self.source,self.source/source,self.source/pdf)
        fixture.config['allowlist']['files'].append(pdf)
        config_path=self.source/'publish_public.yml'
        self.write(config_path,'fixture policy')
        seal={'key':'new-page-fixture','inputs':{},'tools':{}}
        args=SimpleNamespace(page=[page],committed_source=False,with_pdfs=True,report=None)
        state={'issues':[],'commit':'a'*40,'status':[]}
        before=p.tree_manifest(fixture.target,True)
        def render(root,destination,sources,tools):
            self.assertEqual(sources,[source])
            self.write(destination/page,'<html><body>New page <a href="bai_moi.pdf">PDF</a></body></html>')
            self.write(destination/'search.json',json.dumps([{'href':page,'text':'New page'}]))
            self.write(destination/'sitemap.xml','<urlset><url><loc>https://zomath.vn/'+page+'</loc></url></urlset>')
            return {'source_count':1,'exit_code':0}
        with patch.object(pages,'fingerprint',return_value=seal),patch.object(pages,'input_fingerprints',return_value={}),patch.object(pages,'require_page_scope',return_value='a'*40),patch.object(pages,'render_pages',side_effect=render) as renderer,redirect_stdout(io.StringIO()):
            self.assertEqual(pages.prepare(self.source,fixture.target,config_path,fixture.config,args,state,state),0)
            receipt=json.loads((self.source/fixture.config['prepare']['report_file']).read_text(encoding='utf-8'))
            p.validate_prepared_tree(self.source,fixture.target,fixture.config,receipt)
        self.assertEqual(renderer.call_count,1)
        self.assertEqual(set(receipt['diff']['add']),{page,pdf})
        self.assertEqual(set(receipt['diff']['update']),{'search.json','sitemap.xml'})
        self.assertEqual(receipt['diff']['delete'],[])
        after=p.tree_manifest(fixture.target,True)
        for name,record in before['files'].items():
            if name not in {'search.json','sitemap.xml'}:
                self.assertEqual(after['files'][name],record)


if __name__ == '__main__':
    unittest.main(verbosity=2)

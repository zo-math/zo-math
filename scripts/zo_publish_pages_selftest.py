"""Page release regression tests. All mutations use disposable fixture repos."""
import copy,io,json,shutil,tempfile,unittest
import sys
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import zo_publish as p
import zo_publish_pages as pages

ROOT=Path(__file__).resolve().parents[1]


class PageReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.target=self.root/'site';self.raw=self.root/'raw'
        self.config=copy.deepcopy(p.load_config(ROOT,'publish_public.yml')[1])
        self.config['required_files']=['CNAME','.nojekyll','index.html']
        self.config['allowlist']['files']+=['content/other.html','content/old.pdf','assets/test/OFL_Test.txt']
        for name,text in {'CNAME':'zomath.vn','.nojekyll':'','index.html':'<html><body>Old</body></html>',
                          'content/other.html':'<html><body>Keep</body></html>',
                          'content/old.pdf':'original PDF bytes',
                          'search.json':json.dumps([{'href':'index.html','text':'Old'},{'href':'content/other.html','text':'Keep'}]),
                          'sitemap.xml':'<urlset><url><loc>https://zomath.vn/index.html</loc><lastmod>old</lastmod></url><url><loc>https://zomath.vn/content/other.html</loc><lastmod>keep</lastmod></url></urlset>'}.items():
            self.write(self.target,name,text)
        self.render_fixture(self.raw)

    @staticmethod
    def write(root,name,text):
        f=root/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(text,encoding='utf-8')

    def render_fixture(self,root):
        self.write(root,'index.html','<html><head><link rel="stylesheet" href="assets/test/page.css"></head><body>New</body></html>')
        self.write(root,'assets/test/page.css',"@font-face{src:url('page.woff2')}")
        self.write(root,'assets/test/page.woff2','font bytes')
        self.write(root,'assets/test/OFL_Test.txt','license')
        self.write(root,'search.json',json.dumps([{'href':'index.html','text':'New'}]))
        self.write(root,'sitemap.xml','<urlset><url><loc>https://zomath.vn/index.html</loc><lastmod>new</lastmod></url></urlset>')

    def build(self):return pages.candidate(self.target,self.raw,self.root/'candidate',['index.html'],self.config)

    def test_candidate_keeps_other_pages_pdf_and_search_entries(self):
        result=self.build();self.assertEqual(result['issues'],[])
        self.assertEqual(result['validation']['html_files'],1)
        candidate=self.root/'candidate'
        for name in ['content/other.html','content/old.pdf']:
            self.assertEqual((candidate/name).read_bytes(),(self.target/name).read_bytes())
        records=json.loads((candidate/'search.json').read_text())
        self.assertEqual(records,[{'href':'index.html','text':'New'},{'href':'content/other.html','text':'Keep'}])
        self.assertIn('<lastmod>keep</lastmod>',(candidate/'sitemap.xml').read_text())
        self.assertIn('assets/test/OFL_Test.txt',result['manifest']['files'])

    def test_changed_pdf_is_blocked_without_provenance_exemption(self):
        self.write(self.raw,'index.html','<html><body><img src="content/old.pdf"></body></html>')
        self.write(self.raw,'content/old.pdf','changed PDF')
        result=self.build()
        self.assertIn({'type':'page-release-pdf-change','path':'content/old.pdf'},result['issues'])

    def test_d0_pdf_requires_current_receipt_inputs_and_exact_candidate_bytes(self):
        source=self.root/'d0-source';candidate=self.root/'d0-candidate'
        for root in (source,candidate):
            file=root/pages.D0_PDF;file.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/pages.D0_PDF,file)
        self.write(source,'input.txt','current')
        self.write(source,'content/thpt/on_thi_toan_thpt/hoc_lieu/d0/_quy_trinh/pdf_build.json',
                   json.dumps({'output_sha256':p.sha256(source/pages.D0_PDF),
                               'pages':20,
                               'inputs_sha256':{'input.txt':p.sha256(source/'input.txt')}}))
        self.assertEqual(pages.d0_pdf_issues(candidate,source),[])
        self.write(source,'input.txt','stale')
        self.assertEqual(pages.d0_pdf_issues(candidate,source)[0]['type'],'d0-pdf-provenance')
        self.write(source,'input.txt','current')
        (candidate/pages.D0_PDF).write_bytes(b'altered')
        self.assertEqual(pages.d0_pdf_issues(candidate,source)[0]['type'],'d0-pdf-provenance')

    def test_missing_asset_fails_before_candidate_copy(self):
        (self.raw/'assets/test/page.woff2').unlink()
        with self.assertRaisesRegex(p.ConfigError,'Missing rendered dependencies'):self.build()
        self.assertFalse((self.root/'candidate').exists())

    def test_forbidden_asset_is_blocked(self):
        self.write(self.raw,'index.html','<html><img src="_quy_trinh/private.png"></html>')
        self.write(self.raw,'_quy_trinh/private.png','private')
        with self.assertRaisesRegex(p.ConfigError,'not allowlisted'):self.build()

    def test_shared_asset_requires_other_affected_page(self):
        self.write(self.target,'assets/test/page.css','old CSS')
        self.write(self.target,'content/other.html','<html><link rel="stylesheet" href="../assets/test/page.css"></html>')
        result=self.build()
        self.assertTrue(any(x['type']=='shared-asset-needs-pages' for x in result['issues']))

    def test_unselected_rendered_page_cannot_leak(self):
        self.write(self.raw,'content/other.html','unreviewed change')
        result=self.build()
        self.assertNotIn('content/other.html',result['diff']['update'])

    def test_invalid_page_and_escaping_source_blocked(self):
        with self.assertRaises(p.ConfigError):pages.selected_sources(self.root,['../escape.html'])
        with self.assertRaises(p.ConfigError):pages.selected_sources(self.root,['missing.html'])

    def test_preflight_finds_missing_input_before_render(self):
        self.write(self.root,'index.qmd','<img src="missing.png">')
        result=pages.preflight(self.root,['index.html'],self.config)
        self.assertEqual(result['issues'][0]['type'],'missing-source-resource')

    def test_prepare_validate_and_cache_reuse_without_push(self):
        self.assertEqual(p.run(['git','init','-q'],self.target).returncode,0)
        self.assertEqual(p.run(['git','add','.'],self.target).returncode,0)
        self.assertEqual(p.run(['git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','fixture'],self.target).returncode,0)
        repo=self.root/'source';repo.mkdir();(repo/'.quarto').mkdir()
        self.write(repo,'index.qmd','New source')
        config_path=repo/'publish_public.yml';config_path.write_text('fixture')
        tool_names=['zo_publish.py','zo_publish_pages.py','zo_quarto.py','zo_python.py','zo_publish_navigation.py']
        seal={'key':'fixture-key','inputs':{'index.qmd':p.sha256(repo/'index.qmd')},
              'tools':{x:pages.tool_sha(ROOT/'scripts'/x) for x in tool_names}}
        args=SimpleNamespace(page=['index.html'],committed_source=False,report=None)
        state={'issues':[],'commit':'a'*40,'remote_commit':'a'*40,'status':[]}
        def render(root,destination,sources,tool_root):
            self.render_fixture(destination)
            return {'source_count':1,'exit_code':0}
        with patch.object(pages,'fingerprint',return_value=seal),patch.object(pages,'input_fingerprints',return_value=seal['inputs']),patch.object(pages,'require_page_scope',return_value='a'*40),patch.object(pages,'render_pages',side_effect=render) as renderer,redirect_stdout(io.StringIO()):
            self.assertEqual(pages.prepare(repo,self.target,config_path,self.config,args,state,state),0)
            receipt=json.loads((repo/self.config['prepare']['report_file']).read_text())
            _,loaded=p.load_prepare_report(repo,config_path,self.config)
            self.assertEqual(loaded['manifest'],receipt['manifest'])
            pages.validate_receipt(repo,self.target,self.config,receipt)
            p.validate_prepared_tree(repo,self.target,self.config,receipt)
            receipt_bytes=(repo/self.config['prepare']['report_file']).read_bytes()
            with self.assertRaisesRegex(p.ConfigError,'receipt preserved'):
                pages.prepare(repo,self.target,config_path,self.config,args,state,state)
            self.assertEqual((repo/self.config['prepare']['report_file']).read_bytes(),receipt_bytes)
            def text_git(root,*args,**kwargs):
                if args==('rev-parse','HEAD'):return 'a'*40
                if args==('diff','--cached','--name-only'):return ''
                raise AssertionError('Unexpected Git operation: '+str(args))
            with patch.object(p,'load_prepare_report',return_value=(repo/'receipt.json',receipt)),patch.object(p,'find_publish_worktree',return_value=self.target),patch.object(p,'git_state',return_value=state),patch.object(p,'git_text',side_effect=text_git),patch.object(p,'git',side_effect=AssertionError('validate must not fetch/stage/commit/push')):
                self.assertEqual(pages.validate_only(repo,config_path,self.config),0)
            self.assertFalse(receipt['page_release']['cache_hit'])
            p.safe_remove_tree(repo/self.config['prepare']['staging_dir'],repo/'_audit')
            self.assertEqual(pages.prepare(repo,self.target,config_path,self.config,args,state,state),0)
            second=json.loads((repo/self.config['prepare']['report_file']).read_text())
            self.assertTrue(second['page_release']['cache_hit'])
            self.assertEqual(second['page_release']['render']['source_count'],0)
            self.assertEqual(renderer.call_count,1)
            pages.validate_receipt(repo,self.target,self.config,second)
            # Corrupt public output: the same final validator must reject it.
            self.write(self.target,'index.html','tampered')
            with self.assertRaisesRegex(p.ConfigError,'drift'):
                pages.validate_receipt(repo,self.target,self.config,second)

    def test_corrupt_cached_artifact_is_not_reused(self):
        repo=self.root/'source';repo.mkdir();self.write(repo,'index.qmd','source')
        seal={'key':'key'};cache=repo/'.quarto/cache';clock=pages.Timings()
        def render(root,dest,sources,tool):
            self.write(dest,'index.html','sealed');return {'source_count':1,'exit_code':0}
        with patch.object(pages,'fingerprint',return_value=seal),patch.object(pages,'render_pages',side_effect=render) as renderer:
            pages.artifact(repo,['index.html'],self.config,repo/'out1',cache,clock,ROOT)
            self.write(cache/'key/render','index.html','corrupted')
            with self.assertRaisesRegex(p.ConfigError,'hash mismatch'):
                pages.artifact(repo,['index.html'],self.config,repo/'out2',cache,clock,ROOT)
            self.assertEqual(renderer.call_count,1)

    def test_input_or_tool_changes_invalidate_cache_key(self):
        repo=self.root/'fingerprint';repo.mkdir()
        self.write(repo,'index.qmd','source')
        for name in ['zo_publish.py','zo_publish_pages.py','zo_quarto.py','zo_python.py','zo_publish_navigation.py']:
            self.write(repo,'scripts/'+name,'tool')
        def source_git(root,*args):
            return '100644 '+('b'*40)+' 0\tindex.qmd\0' if args[0]=='ls-files' else 'index.qmd\0'
        with patch.object(p,'git_text',side_effect=source_git),patch.object(p,'git',return_value=SimpleNamespace(stdout='',returncode=0)),patch.object(p,'run',return_value=SimpleNamespace(stdout='1.0',returncode=0)),patch.object(pages.importlib.metadata,'distributions',return_value=[]):
            first=pages.fingerprint(repo,['index.html'],self.config,repo)
            self.assertEqual(first,pages.fingerprint(repo,['index.html'],self.config,repo))
            self.write(repo,'index.qmd','changed source')
            second=pages.fingerprint(repo,['index.html'],self.config,repo)
            self.assertNotEqual(first['key'],second['key'])
            self.write(repo,'scripts/zo_quarto.py','changed tool')
            self.assertNotEqual(second['key'],pages.fingerprint(repo,['index.html'],self.config,repo)['key'])

    def test_source_drift_during_render_does_not_seal_artifact(self):
        repo=self.root/'drift';repo.mkdir();self.write(repo,'index.qmd','source')
        def render(root,dest,sources,tool):
            self.write(dest,'index.html','rendered');return {'source_count':1,'exit_code':0}
        with patch.object(pages,'fingerprint',side_effect=[{'key':'before'},{'key':'after'}]),patch.object(pages,'render_pages',side_effect=render):
            with self.assertRaisesRegex(p.ConfigError,'changed during'):
                pages.artifact(repo,['index.html'],self.config,repo/'output',repo/'.quarto/cache',pages.Timings(),ROOT)
        self.assertFalse((repo/'.quarto/cache/before').exists())

    def test_git_batch_manifest_preserves_binary_unicode_and_spaces(self):
        self.assertEqual(p.run(['git','init','-q'],self.target).returncode,0)
        binary=self.target/'assets/test/ảnh có dấu.bin';binary.parent.mkdir(parents=True,exist_ok=True)
        binary.write_bytes(b'\x00\xff\n\r\n binary bytes')
        self.assertEqual(p.run(['git','-c','core.autocrlf=false','add','.'],self.target).returncode,0)
        self.assertEqual(p.run(['git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','fixture'],self.target).returncode,0)
        self.assertEqual(p.committed_manifest(self.target,p.git_text(self.target,'rev-parse','HEAD')),p.tree_manifest(self.target,True))

    def test_global_configuration_requires_full_render_before_any_render(self):
        with patch.object(p,'published_source_commit',return_value='a'*40),patch.object(p,'git_text',return_value='_quarto.yml\nindex.qmd'),patch.object(pages,'render_pages',side_effect=AssertionError('must not render')):
            with self.assertRaisesRegex(p.ConfigError,'full-render'):
                pages.require_page_scope(self.root,self.target)

    def test_explicit_scoped_release_records_global_configuration(self):
        with patch.object(p,'published_source_commit',return_value='a'*40),patch.object(p,'git_text',return_value='_quarto.yml\nindex.qmd'):
            self.assertEqual(pages.require_page_scope(self.root,self.target,True),'a'*40)
            self.assertEqual(pages.changed_global_inputs(self.root,'a'*40),['_quarto.yml'])

    def test_executable_or_unknown_shortcode_inputs_disable_cache(self):
        self.write(self.root,'index.qmd','{{< include child.md >}}')
        self.write(self.root,'child.md','Static source')
        self.assertTrue(pages.cache_eligible(self.root,['index.qmd']))
        self.write(self.root,'child.md','```{python}\nprint(1)\n```')
        self.assertFalse(pages.cache_eligible(self.root,['index.qmd']))
        self.write(self.root,'child.md','{{< unknown-dynamic-source >}}')
        self.assertFalse(pages.cache_eligible(self.root,['index.qmd']))

    def test_git_blob_key_detects_working_byte_changes(self):
        repo=self.root/'git-input';repo.mkdir();self.write(repo,'index.qmd','committed source')
        for command in [['git','init','-q'],['git','add','index.qmd'],['git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','fixture']]:
            self.assertEqual(p.run(command,repo).returncode,0)
        first=pages.input_fingerprints(repo)
        self.assertTrue(first['index.qmd'].startswith('git-blob:'))
        self.write(repo,'index.qmd','edited source')
        second=pages.input_fingerprints(repo)
        self.assertEqual(second['index.qmd'],p.sha256(repo/'index.qmd'))
        self.assertNotEqual(first,second)

    def test_cli_plan_missing_source_returns_error_without_traceback(self):
        result=p.run([sys.executable,str(ROOT/'scripts/zo_python.py'),str(ROOT/'scripts/zo_publish.py'),'plan','--page','missing.html'],ROOT)
        self.assertEqual(result.returncode,p.EXIT_USAGE)
        self.assertIn('ERROR:',result.stderr)
        self.assertNotIn('Traceback',result.stderr)


class NavigationInheritanceTests(unittest.TestCase):
    def test_only_menu_changes_and_is_idempotent(self):
        import zo_publish_navigation as n
        old=b'<main>Original &amp; content</main><nav class="course-panel"><a>old</a></nav><footer>unchanged</footer>'
        with patch.object(n,'PAGES',{'g':(Path('lesson.html'),'Lesson')}), patch.object(n,'destinations',return_value=[('g','lesson.html','Lesson')]):
            new=n.refresh(old,'lesson.html',Path('.'))
            self.assertTrue(new.startswith(b'<main>Original &amp; content</main>'))
            self.assertTrue(new.endswith(b'<footer>unchanged</footer>'))
            self.assertIn(b'aria-current="page"',new)
            self.assertEqual(n.refresh(new,'lesson.html',Path('.')),new)
            for bad in [b'<main>No menu</main>',old+old]:
                with self.assertRaises(p.ConfigError):n.refresh(bad,'lesson.html',Path('.'))
    def test_verify_rejects_changed_lesson(self):
        import zo_publish_navigation as n
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);backup=root/'before';target=root/'after';backup.mkdir();target.mkdir()
            old=b'<main>Keep me</main><nav class="course-panel"><a>old</a></nav>'
            (backup/'lesson.html').write_bytes(old)
            with patch.object(n,'PAGES',{'g':(Path('lesson.html'),'Lesson')}), patch.object(n,'destinations',return_value=[('g','lesson.html','Lesson')]):
                (target/'lesson.html').write_bytes(n.refresh(old,'lesson.html',target));seal={'lesson.html':p.sha256(backup/'lesson.html')}
                n.verify(backup,target,seal)
                (target/'lesson.html').write_bytes((target/'lesson.html').read_bytes().replace(b'Keep me',b'Changed'))
                with self.assertRaises(p.ConfigError):n.verify(backup,target,seal)


if __name__=='__main__':unittest.main(verbosity=2)

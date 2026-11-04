"""Negative guards for a byte-preserving video-only publication."""
import copy,json,re,shutil,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import zo_publish as p
import zo_publish_videos as v

BASE='a'*40
class VideoReleaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.backup=self.root/'public';self.target=self.root/'candidate'
        self.old='Existing mathematical explanation: $x^3$.\n\n'
        self.fragment='<details class="zo-block zo-block-gray zo-learning-video" id="video-h01" data-youtube-id="1WBLfF2gTGU"><summary>Video</summary><div class="zo-block-body"><div class="zo-video-player"></div><p><a href="https://www.youtube.com/shorts/1WBLfF2gTGU">YouTube</a></p></div></details>'
        self.write(self.root,v.PACKAGE/'index.qmd',self.old+'```{=html}\n'+self.fragment+'\n```\n\n')
        self.plan={'version':1,'page':v.PAGE,'placements':[{'id':'video-h01','mode':'before_region','anchor':'task'}]}
        self.write(self.root,v.PLAN,json.dumps(self.plan))
        for dest,source in v.ASSETS.items():self.write(self.root,source,'/* page-local video asset */')
        self.html=('<!DOCTYPE html>\n<html><head><title>Đơn điệu</title><script>let a="&amp;";</script></head>'
                   '<body data-zo-course-site="r20-integrated-v1"><section id="bai-hoc"><div class="reading-region">'
                   '<p id="task">Question &amp; math <math><mi>x</mi></math></p></div></section>'
                   '<section id="tu-kiem-tra"><p>Unchanged test</p></section></body></html>').encode()
        self.write(self.backup,v.PAGE,self.html)
        self.write(self.backup,'assets/common.css','unchanged shared style')
        self.git=patch.object(p,'git',return_value=SimpleNamespace(returncode=0,stdout=self.old))
        self.git.start();self.addCleanup(self.git.stop)
    @staticmethod
    def write(root,name,value):
        path=root/name;path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(value if isinstance(value,bytes) else value.encode())
    def candidate(self):
        data,seal=v.refresh(self.root,self.html,v.PAGE,BASE)
        shutil.copytree(self.backup,self.target)
        self.write(self.target,v.PAGE,data)
        for dest,source in v.ASSETS.items():self.write(self.target,dest,(self.root/source).read_bytes())
        return {v.PAGE:seal}
    def test_inverse_preserves_every_existing_byte_and_expected_position(self):
        seals=self.candidate();v.verify(self.root,self.backup,self.target,seals)
        content=(self.target/v.PAGE).read_text()
        self.assertLess(content.index('id="video-h01"'),content.index('id="task"'))
        inverse=re.sub(r'<!-- zo-video:[^>]+ -->.*?<!-- /zo-video:[^>]+ -->\n|<!-- zo-video-assets -->.*?<!-- /zo-video-assets -->','',content,flags=re.S)
        self.assertEqual(inverse.encode(),self.html)
    def test_asset_urls_resolve_from_nested_page_on_windows_and_posix(self):
        from urllib.parse import urljoin
        from bs4 import BeautifulSoup
        self.candidate();doc=BeautifulSoup((self.target/v.PAGE).read_text(),'html.parser')
        urls=[urljoin('https://zomath.vn/'+v.PAGE,n.get('href') or n.get('src')) for n in doc.select('link[href],script[src]')]
        self.assertEqual(set(urls),{'https://zomath.vn/'+name for name in v.ASSETS})
    def test_public_worktree_git_pointer_is_not_website_content(self):
        seals=self.candidate();self.write(self.backup,'.git','gitdir: another/place')
        v.verify(self.root,self.backup,self.target,seals)
    def test_duplicate_or_missing_anchor_rejected(self):
        for data in [self.html.replace(b'id="task"',b'id="absent"'),self.html.replace(b'id="bai-hoc"',b'id="task"')]:
            with self.assertRaisesRegex(p.ConfigError,'placement anchor'):v.refresh(self.root,data,v.PAGE,BASE)
    def test_test_section_insertion_rejected(self):
        self.plan['placements'][0]['anchor']='tu-kiem-tra';self.write(self.root,v.PLAN,json.dumps(self.plan))
        with self.assertRaisesRegex(p.ConfigError,'cannot be placed in the test'):v.refresh(self.root,self.html,v.PAGE,BASE)
    def test_non_video_source_edit_rejected(self):
        file=self.root/v.PACKAGE/'index.qmd';file.write_text(file.read_text().replace('$x^3$','$x^2$'))
        with self.assertRaisesRegex(p.ConfigError,'Non-video source change'):v.refresh(self.root,self.html,v.PAGE,BASE)
    def test_unexpected_html_or_external_link_rejected(self):
        file=self.root/v.PACKAGE/'index.qmd';original=file.read_text()
        for modified in [original.replace('<summary>','<summary onclick="alert(1)">'),original.replace('https://www.youtube.com/shorts/','https://example.com/')]:
            file.write_text(modified)
            with self.assertRaises(p.ConfigError):v.refresh(self.root,self.html,v.PAGE,BASE)
    def test_shared_asset_edit_rejected(self):
        seals=self.candidate();self.write(self.target,'assets/common.css','changed')
        with self.assertRaisesRegex(p.ConfigError,'outside the video page'):v.verify(self.root,self.backup,self.target,seals)
    def test_existing_html_or_new_asset_tamper_rejected(self):
        seals=self.candidate();original=(self.target/v.PAGE).read_bytes()
        self.write(self.target,v.PAGE,original.replace(b'Unchanged test',b'Changed test'))
        with self.assertRaisesRegex(p.ConfigError,'HTML drift'):v.verify(self.root,self.backup,self.target,seals)
        self.write(self.target,v.PAGE,original);self.write(self.target,next(iter(v.ASSETS)),'tamper')
        with self.assertRaisesRegex(p.ConfigError,'asset drift'):v.verify(self.root,self.backup,self.target,seals)
    def test_plan_and_baseline_tamper_rejected(self):
        seals=self.candidate();self.plan['placements'][0]['anchor']='absent';self.write(self.root,v.PLAN,json.dumps(self.plan))
        with self.assertRaises(p.ConfigError):v.verify(self.root,self.backup,self.target,seals)
    def test_duplicate_placement_or_missing_source_video_rejected(self):
        self.plan['placements'].append(copy.deepcopy(self.plan['placements'][0]));self.write(self.root,v.PLAN,json.dumps(self.plan))
        with self.assertRaisesRegex(p.ConfigError,'coverage'):v.refresh(self.root,self.html,v.PAGE,BASE)
    def test_cli_rejects_mixed_release_modes_before_work(self):
        self.assertEqual(p.main(['prepare','--page',v.PAGE,'--video-only-page',v.PAGE,'--with-pdfs']),p.EXIT_USAGE)
        self.assertEqual(p.main(['prepare','--video-only-page',v.PAGE]),p.EXIT_USAGE)

if __name__=='__main__':unittest.main()

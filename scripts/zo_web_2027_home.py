"""Opt-in course Home from fresh Quarto QMD, never from audit HTML or old docs.

Reuses the owner-reviewed home reading map and shared shell. Canonical links
remain portable site-relative URLs; only an explicit preview can map destinations
to already rendered package candidates. No PDF, source promotion, Git or release.
"""
from __future__ import annotations
import argparse
import copy
import html
import json
import os
from pathlib import Path
import shutil
import sys
from urllib.parse import unquote, urlsplit, urlunsplit

sys.dont_write_bytecode = True
from bs4 import BeautifulSoup
from zo_web_2027_preview import PreviewBuilder, REPO, KIT, DESIGN04, BRAND_THOUGHT, template, footer_data, sha

HOME = Path('content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.html')
MARKER = 'zo-web-2027-home'


class HomeBuilder(PreviewBuilder):
    def __init__(self, page: Path, output_root: Path):
        self.page = page.resolve()
        self.output = self.page.parent
        self.output_root = output_root.resolve()
        if not self.page.is_relative_to(self.output_root) or not self.output_root.is_relative_to(REPO):
            raise ValueError('Home output must stay inside the declared repository output tree')
        self.runtime = self.output_root / 'assets/zo_web_2027/home'
        self.resources = {}
        self.links = []
        self.runtime_hrefs = {}
        self.ui_baseline = None
        self.current_home = True
        self.profile = json.loads((KIT / 'profiles/course-home.json').read_text(encoding='utf-8'))

    def href(self, destination: Path, query='', fragment=''):
        return urlunsplit(('', '', os.path.relpath(destination, self.output).replace('\\', '/'), query, fragment))

    def materialize(self, source: Path, destination: str) -> str:
        source = source.resolve()
        target = (self.runtime / destination).resolve()
        if not source.is_relative_to(REPO) or not source.is_file() or not target.is_relative_to(self.runtime):
            raise ValueError('Missing or unsafe Home dependency: ' + str(source))
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        self.resources[destination] = {'source': source.relative_to(REPO).as_posix(), 'sha256': sha(source)}
        self.runtime_hrefs[destination] = self.href(target)
        return self.runtime_hrefs[destination]

    def common_assets(self):
        for name in ['reading-regions.css', 'web-shell.css', 'site-ui.js', 'course-home.css', 'appearance-inline.css']:
            self.materialize(KIT / name, name)
        for name in ['horizontal_color.svg', 'stack_color.svg', 'favicon_color.svg']:
            self.materialize(DESIGN04 / 'logos' / name, 'assets/logos/' + name)
        for name in ['BeVietnamPro_Regular.ttf', 'BeVietnamPro_SemiBold.ttf', 'STIXTwoMath.ttf', 'OFL_BeVietnamPro.txt', 'OFL_STIXTwo.txt']:
            source = DESIGN04 / 'assets' / name
            if name.startswith('OFL_STIX') and not source.is_file():
                sources = list((DESIGN04 / 'assets').glob('*STIX*txt'))
                if len(sources) != 1: raise ValueError('Expected one canonical STIX licence')
                source = sources[0]
            self.materialize(source, 'assets/fonts/' + source.name)
        self.materialize(REPO / self.profile['cover_source'], 'assets/cover-graph.svg')
        self.materialize(REPO / 'assets/images/qr_bao_tro_zo_math_vietcombank.jpg', 'assets/qr_bao_tro_zo_math_vietcombank.jpg')

    def normalize_links(self, root, source_file, *, g01_preview=False):
        for image in root.select('img[src]'):
            if image.find_parent(class_='zo-on-thi-hero__cover'): continue
            url = urlsplit(image['src'])
            if url.scheme or url.netloc: raise ValueError('Unexpected network image in Home')
            source = self.output_root / unquote(url.path).lstrip('/') if url.path.startswith('/') else source_file.parent / unquote(url.path)
            canonical = REPO / source.resolve().relative_to(self.output_root)
            if not canonical.is_file() or sha(source) != sha(canonical):
                raise ValueError('Fresh rendered image differs from canonical Home asset: ' + str(canonical))
            source = canonical
            image['src'] = self.materialize(source, 'assets/content/' + sha(source)[:12] + '_' + source.name)
        for link in root.select('a[href]'):
            original = link['href']; url = urlsplit(original)
            if url.scheme or url.netloc or not url.path: continue
            target = self.output_root / unquote(url.path).lstrip('/') if url.path.startswith('/') else source_file.parent / unquote(url.path)
            if not target.resolve().is_relative_to(self.output_root): raise ValueError('Local link escapes output tree')
            link['data-canonical-href'] = original
            link['href'] = self.href(target, url.query, url.fragment)
            self.links.append({'canonical_href': original, 'output_href': link['href']})

    def site_footer(self):
        data = footer_data()
        for item in data['information'] + data['social']:
            url = urlsplit(item['canonical_href'])
            if url.scheme:
                if url.scheme != 'https': raise ValueError('Non-HTTPS footer URL')
                item['preview_href'] = item['canonical_href']
            else:
                source = REPO / unquote(url.path).lstrip('/')
                if not source.is_file(): raise ValueError('Missing footer canonical source: ' + str(source))
                item['preview_href'] = self.href((self.output_root / source.relative_to(REPO)).with_suffix('.html'), url.query, url.fragment)
        def links(items, external=False):
            return '\n'.join('<a href="' + html.escape(n['preview_href'], quote=True) + '" data-canonical-href="' + html.escape(n['canonical_href'], quote=True) + '">' + html.escape(n['label']) + ('<span class="zo-site-footer__arrow" aria-hidden="true">↗</span>' if external else '') + '</a>' for n in items)
        return template('site-footer.html', information_links=links(data['information']), social_links=links(data['social'], True), copyright=html.escape(data['copyright']), brand_thought=html.escape(BRAND_THOUGHT)), data

    def build_current(self):
        if self.profile.get('layout') == 'editorial-home-2027':
            from zo_web_2027_home_landing import build
            return build(self)
        raw_root = BeautifulSoup(self.page.read_text(encoding='utf-8'), 'html.parser').select_one('.zo-on-thi-program')
        raw_markup = str(raw_root)
        self.common_assets()
        report = self.home(False, source=self.page, write=False)
        doc = BeautifulSoup(report.pop('_html'), 'html.parser')
        doc.title.string = 'Ôn thi Toán THPT 2027 — ZO Math'
        doc.body['class'].append(MARKER)
        doc.body['data-zo-web-production'] = 'course-home'
        doc.html['data-zo-preferences'] = 'zo-web-2027-preview-v1'
        doc.select_one('.brand-thought').string = BRAND_THOUGHT
        doc.select_one('.lab-link').string = 'ZO Math'
        for link in doc.select('.site-top > a:first-child,.course-link,.rail-heading > a,.breadcrumb > a'):
            link['href'] = 'index.html'
        trigger = doc.select_one('.mobile-trigger')
        trigger['aria-label'] = 'Mở mục lục khóa học'
        # site-ui still maintains this hidden state label; do not remove its DOM hook.
        trigger['class'].append('mobile-trigger--icon')
        note = doc.select_one('.prototype-note')
        note.decompose()  # Build status belongs in QA, never in learner copy.
        doc.select_one('.r1-support-link a')['href'] = self.href(self.output_root / 'content/support/donate.html')
        image = doc.select_one('.hero-art img')
        image['alt'] = self.profile['cover_alt']
        frame = doc.new_tag('div', attrs={'class': 'zo-cover-frame', 'data-frame-shape': self.profile['cover']['shape'], 'data-frame-size': self.profile['cover']['size']})
        tokens = json.loads((KIT / 'figure-profile-candidate/frame-tokens.json').read_text(encoding='utf-8'))
        width, height = tokens['sizes_px'][self.profile['cover']['shape']][self.profile['cover']['size']]
        frame['style'] = f'--frame-width:{width}px;--frame-ratio:{width}/{height}'
        image.wrap(frame)
        for node in doc.select('link[href],img[src],script[src]'):
            key = 'href' if node.name == 'link' else 'src'
            if node[key] in self.runtime_hrefs: node[key] = self.runtime_hrefs[node[key]]
        if doc.select_one('script[src*="r1-controller"]') or '_audit/' in str(doc):
            raise ValueError('Home cannot depend on package controller or audit input')
        report['resources'] = self.resources
        report['links'] = self.links
        report['output'] = self.page.relative_to(REPO).as_posix()
        report['preview_input'] = False
        report['source_markup'] = raw_markup
        report['profile_sha256'] = sha(KIT / 'profiles/course-home.json')
        report['frame_tokens_sha256'] = sha(KIT / 'figure-profile-candidate/frame-tokens.json')
        from zo_course_tables import apply as apply_tables
        apply_tables(doc, 'home', self.page, self.runtime)
        self.resources['course-tables.css'] = {'source': '_design/web_2027_mau_dung_chung/course-tables.css', 'sha256': sha(KIT / 'course-tables.css')}
        from zo_web_2027_navigation import apply as apply_course_navigation
        self.resources.update(apply_course_navigation(doc, self.page, self.output_root, self.runtime, 'home'))
        self.page.write_text(str(doc), encoding='utf-8')
        report['html_sha256'] = sha(self.page)
        return report


def adapt(path, output_root):
    from zo_math_notation import require_runtime_css
    require_runtime_css(KIT / 'web-shell.css')
    doc = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    if MARKER not in doc.body.get('class', []):
        raise ValueError('Home opt-in marker missing; refuse silent rollback')
    if doc.body.get('data-zo-web-production') == 'course-home': return False
    if not doc.select_one('.zo-on-thi-program'): raise ValueError('Home marker without canonical program content')
    report = HomeBuilder(path, output_root).build_current()
    destination = os.environ.get('ZO_WEB_2027_HOME_REPORT')
    if destination:
        target = Path(destination).resolve()
        if not target.is_relative_to(REPO / '_audit'): raise ValueError('Home build evidence must stay in _audit')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('Home canonical adapter:', path)
    return True


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--html', type=Path, required=True)
    parser.add_argument('--output-root', type=Path, required=True)
    args=parser.parse_args()
    adapt(args.html.resolve(), args.output_root.resolve())
    return 0


if __name__ == '__main__': raise SystemExit(main())

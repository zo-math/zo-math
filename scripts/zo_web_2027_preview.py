"""Build isolated HTML previews from the accepted web kit; never write production.

Home reads the current rendered content and verifies its projection against the
canonical course data. The optional G01 input is an explicit, hash-pinned visual
reference, not a production dependency. All outputs must be inside repo/_audit.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
from string import Template
import sys
from urllib.parse import quote, unquote, urlsplit, urlunsplit

sys.dont_write_bytecode = True
from bs4 import BeautifulSoup, Tag
import yaml

REPO = Path(__file__).resolve().parents[1]
KIT = REPO / '_design/web_2027_mau_dung_chung'
DESIGN04 = REPO / '_design/ngon_ngu_thiet_ke_zo_math_0_4/07_mau_thi_giac'
ACCEPTED_G01_SHA = '34340b7ca1b2db8e06139dcdcaed89930ad05415df9f9e80ad3f41a1710e7a77'
BRAND_THOUGHT = 'Học trong kỉ nguyên trí tuệ nhân tạo, học để tìm lại chính mình.'
LEGACY_BRAND_THOUGHT = 'Học trong kỉ nguyên AI, học để tìm lại chính mình.'


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def audit_path(path: Path) -> Path:
    result = path.resolve()
    if not result.is_relative_to((REPO / '_audit').resolve()) or result == (REPO / '_audit').resolve():
        raise ValueError('Preview outputs must be a named subdirectory under repository/_audit.')
    return result


def relative_href(target: Path, output: Path, query='', fragment='') -> str:
    path = quote(os.path.relpath(target, output).replace('\\', '/'), safe='/.-_')
    return urlunsplit(('', '', path, query, fragment))


def projection(node: Tag) -> str:
    clone = copy.deepcopy(node)
    for added in clone.select('[data-reading-label], [data-design-note]'):
        added.decompose()
    return re.sub(r'\s+', ' ', clone.get_text(' ', strip=True))


def inventory(node: Tag) -> dict:
    return {
        'text': projection(node),
        'ids': [n['id'] for n in node.select('[id]')],
        'math': [str(n) for n in node.select('math')],
        'headings': [(n.name, n.get_text(' ', strip=True)) for n in node.select('h2,h3,h4,h5')],
        'disclosures': [(n.get('id'), n.has_attr('open')) for n in node.select('details')],
    }


def template(name: str, **values) -> str:
    rendered=Template((KIT / 'templates' / (name + '.tpl')).read_text(encoding='utf-8')).substitute(values)
    if name=='page.html':
        from zo_web_2027_shell import require as require_shell
        require_shell(BeautifulSoup(rendered,'html.parser'))
    return rendered


def footer_data() -> dict:
    """Use the active Quarto footer, never the unused legacy footer fragment."""
    source = REPO / '_quarto.yml'
    config = yaml.safe_load(source.read_text(encoding='utf-8'))
    center = config['website']['page-footer']['center']
    information = [{'label': label, 'canonical_href': href}
                   for label, href in re.findall(r'\[([^\]]+)\]\(([^)]+)\)', center)]
    social = [{'label': n.get('title', ''), 'canonical_href': n['href']}
              for n in BeautifulSoup(center, 'html.parser').select('a[href]')]
    copyright_line = re.search(r'©\s*\d{4}\s+ZO Math', center)
    if ([n['label'] for n in information] != ['Giới thiệu', 'Triết lí và định hướng', 'Liên hệ']
            or [n['label'] for n in social] != ['Facebook', 'TikTok', 'YouTube']
            or not copyright_line):
        raise ValueError('Active site footer has changed; review its mapping rather than silently dropping content.')
    return {'source': '_quarto.yml', 'source_sha256': sha(source), 'information': information,
            'social': social, 'copyright': copyright_line.group()}


def without_site_footer(markup: str) -> str:
    """Normalize only whitespace for an exact pre-existing DOM comparison."""
    doc = BeautifulSoup(markup, 'html.parser')
    for n in doc.select('#site-footer,link[rel=stylesheet][href="site-footer.css"]'):
        n.decompose()
    for text in list(doc.find_all(string=True)):
        if not text.strip():
            text.extract()
    return str(doc)


def without_requested_ui(markup: str) -> str:
    """Allow only the two FB-027 changes, not a general shell redesign."""
    doc = BeautifulSoup(markup, 'html.parser')
    for n in doc.select('.appearance,.brand-thought,.zo-site-footer__brand p,link[rel=stylesheet][href="appearance-inline.css"]'):
        n.decompose()
    for text in list(doc.find_all(string=True)):
        if not text.strip():
            text.extract()
    return str(doc)


class PreviewBuilder:
    def __init__(self, output: Path):
        self.output = audit_path(output)
        self.output.mkdir(parents=True, exist_ok=True)
        self.resources = {}
        self.links = []
        self.ui_baseline = None
        self.current_home = False
        self.profile = json.loads((KIT / 'profiles/course-home.json').read_text(encoding='utf-8'))

    def materialize(self, source: Path, destination: str) -> str:
        source = source.resolve()
        if not source.is_relative_to(REPO) or not source.is_file():
            raise ValueError(f'Missing or out-of-repository dependency: {source}')
        dest = (self.output / destination).resolve()
        if not dest.is_relative_to(self.output):
            raise ValueError('Asset destination escapes preview directory.')
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
        self.resources[destination] = {'source': source.relative_to(REPO).as_posix(), 'sha256': sha(source)}
        return destination

    def common_assets(self) -> None:
        for name in ['reading-regions.css', 'web-shell.css', 'site-ui.js', 'course-home.css', 'r1-controller.js']:
            self.materialize(KIT / name, name)
        for name in ['horizontal_color.svg', 'stack_color.svg', 'favicon_color.svg']:
            self.materialize(DESIGN04 / 'logos' / name, 'assets/logos/' + name)
        for name in ['BeVietnamPro_Regular.ttf', 'BeVietnamPro_SemiBold.ttf', 'STIXTwoMath.ttf', 'OFL_BeVietnamPro.txt', 'OFL_STIX.txt']:
            # The handoff may name the STIX licence differently; resolve explicitly below.
            source = DESIGN04 / 'assets' / name
            if name.startswith('OFL_STIX') and not source.is_file():
                matches = list((DESIGN04 / 'assets').glob('*STIX*txt'))
                if len(matches) != 1:
                    raise ValueError('Expected one existing STIX font licence.')
                source = matches[0]
            self.materialize(source, 'assets/fonts/' + source.name)
        self.materialize(REPO / 'assets/images/qr_bao_tro_zo_math_vietcombank.jpg', 'assets/qr_bao_tro_zo_math_vietcombank.jpg')
        if self.ui_baseline or self.current_home:
            self.materialize(KIT / 'appearance-inline.css', 'appearance-inline.css')

    def normalize_links(self, root: Tag, source_file: Path, *, g01_preview=False) -> None:
        for image in root.select('img[src]'):
            if image.find_parent(class_='zo-on-thi-hero__cover'):
                # The Home cover is replaced by the shared cover illustration below.
                continue
            split = urlsplit(image['src'])
            if split.scheme or split.netloc:
                raise ValueError('Unexpected network image in local course preview.')
            source = (REPO / 'docs' / unquote(split.path).lstrip('/')) if split.path.startswith('/') else source_file.parent / unquote(split.path)
            target = 'assets/content/' + sha(source)[:12] + '_' + source.name
            image['src'] = self.materialize(source, target)
        for link in root.select('a[href]'):
            original = link['href']
            split = urlsplit(original)
            if split.scheme or split.netloc or not split.path:
                continue
            source = (REPO / 'docs' / unquote(split.path).lstrip('/')) if split.path.startswith('/') else source_file.parent / unquote(split.path)
            if not source.is_file():
                raise ValueError(f'Local link has no target: {original} from {source_file}')
            mapped = relative_href(source.resolve(), self.output, split.query, split.fragment)
            if g01_preview and '/hoc_lieu/r1_g01/index.html' in source.as_posix():
                mapped = urlunsplit(('', '', 'g01-kit.html', split.query, split.fragment))
            link['data-canonical-href'] = original
            link['href'] = mapped
            self.links.append({'source_page': source_file.relative_to(REPO).as_posix(), 'canonical_href': original, 'preview_href': mapped})

    def appearance(self) -> str:
        choices = []
        for value, label in self.profile['themes']:
            checked = ' checked' if value == 'yellow-1' else ''
            if self.ui_baseline or self.current_home:
                choices.append(f'<label title="{label}"><input name="background" type="radio" value="{value}" aria-label="Nền {label}" style="--swatch:var(--theme-{value})"{checked}></label>')
            else:
                choices.append(f'<label><input name="background" type="radio" value="{value}" data-label="{label}"{checked}><i style="background:var(--theme-{value})" aria-hidden="true"></i>{label}</label>')
        return template('appearance-inline.html' if self.ui_baseline or self.current_home else 'appearance.html', choices=''.join(choices))

    def navigation(self) -> str:
        parts = ['<nav class="home-nav" aria-label="Mục lục trang Nhà">']
        for group in self.profile['navigation']:
            links = ''.join(f'<a href="#{quote(ident)}">{html.escape(label)}</a>' for label, ident in group['items'])
            parts.append(f'<div class="r1-tab-group"><span class="r1-tab-group-label">{html.escape(group["label"])}</span><div class="r1-tab-group-items">{links}</div></div>')
        return ''.join(parts) + '</nav>'

    def site_footer(self) -> tuple[str, dict]:
        data = footer_data()
        for item in data['information']:
            split = urlsplit(item['canonical_href'])
            target = REPO / 'docs' / unquote(split.path).lstrip('/')
            target = target.with_suffix('.html') if target.suffix == '.qmd' else target
            if not target.is_file():
                raise ValueError('Missing existing footer destination: ' + str(target))
            item['preview_href'] = relative_href(target, self.output, split.query, split.fragment)
        for item in data['social']:
            if urlsplit(item['canonical_href']).scheme != 'https':
                raise ValueError('Unexpected social footer URL')
            item['preview_href'] = item['canonical_href']
        def links(items, external=False):
            return '\n'.join('<a href="' + html.escape(n['preview_href'], quote=True)
                             + '" data-canonical-href="' + html.escape(n['canonical_href'], quote=True)
                             + '">' + html.escape(n['label'])
                             + ('<span class="zo-site-footer__arrow" aria-hidden="true">↗</span>' if external else '')
                             + '</a>' for n in items)
        return template('site-footer.html', information_links=links(data['information']),
                        social_links=links(data['social'], True), copyright=html.escape(data['copyright']),
                        brand_thought=html.escape(BRAND_THOUGHT) if self.ui_baseline or self.current_home else html.escape(LEGACY_BRAND_THOUGHT).replace(', học', ',<br>học')), data

    def home(self, include_g01: bool, footer_baseline: Path | None = None, *, source: Path | None = None, write=True) -> dict:
        source = source or REPO / self.profile['rendered_source']
        if self.profile.get('layout') == 'editorial-home-2027':
            raise ValueError('Native Home uses zo_web_2027_home_check.py and zo_web_2027_home_landing_check.py, not the retired Home projection')
        # Explicit legacy Home illustration; never part of common assets.
        self.materialize(KIT / 'assets/cover-graph.svg', 'assets/cover-graph.svg')
        data_file = REPO / self.profile['data_source']
        partial_file = REPO / self.profile['partial_source']
        doc = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
        root = doc.select_one(self.profile['reader_selector'])
        if not root:
            raise ValueError('Rendered Home does not contain its canonical program root.')
        original = inventory(root)
        data = yaml.safe_load(data_file.read_text(encoding='utf-8'))
        self.verify_home_data(root, data)
        root = copy.deepcopy(root)
        self.normalize_links(root, source, g01_preview=include_g01)
        hero = root.select_one('.zo-on-thi-hero').extract()
        # Reuse the accepted cover structure, keeping the actual Home introduction.
        hero['class'] = ['hero']
        layout = hero.select_one('.zo-on-thi-hero__layout')
        layout.unwrap()
        hero_copy = hero.select_one('.zo-on-thi-hero__copy')
        hero_copy['class'] = ['hero-copy']
        status = hero_copy.select_one('.zo-on-thi-status')
        heading = doc.new_tag('h1', attrs={'data-design-note': ''})
        heading.string = data['program']['title']
        status.insert_after(heading)
        action = hero_copy.select_one('a')
        action['class'] = ['hero-action']
        cover = hero.select_one('.zo-on-thi-hero__cover')
        cover.clear(); cover['class'] = ['hero-art']; cover.name = 'figure'
        image = doc.new_tag('img', src='assets/cover-graph.svg', alt='Minh họa mạch R1: đồ thị p(x)=x³−3x+1')
        cover.append(image)
        root['class'] = ['zo-on-thi', 'zo-on-thi-program', 'reader-content']
        root.attrs.pop('style', None)
        groups = []
        for group in self.profile['groups']:
            sections = [root.find('section', id=ident, recursive=False) for ident in group['sections']]
            if not all(sections):
                raise ValueError('Profile references a missing or non-direct Home section: ' + str(group['sections']))
            if group.get('split_packages'):
                section = sections[0]
                heading = section.find('h2', recursive=False).extract()
                packages = section.select(':scope > .zo-on-thi-package')
                for index, package in enumerate(packages):
                    # Cover accompanies the identity, not a narrow column for the
                    # whole summary. Keep every original word in source order.
                    layout = package.select_one('.zo-on-thi-package__layout')
                    package_copy = layout.select_one('.zo-on-thi-package__copy')
                    source_heading = package_copy.find('h3')
                    if source_heading is None or source_heading.parent.name != 'section':
                        raise ValueError('Unexpected canonical package heading/section structure.')
                    package_heading = doc.new_tag('div', attrs={'class': 'course-package-heading'})
                    package_title = doc.new_tag('div', attrs={'class': 'course-package-title'})
                    source_heading.insert_before(package_heading)
                    package_heading.append(layout.select_one('.zo-on-thi-package__cover').extract())
                    package_title.append(package_copy.select_one('.zo-on-thi-package__meta').extract())
                    package_title.append(source_heading.extract())
                    package_heading.append(package_title)
                    region = doc.new_tag('div', attrs={'class': 'reading-region course-package-region', 'data-reading-beat': package['data-package-id']})
                    if index == 0:
                        region.append(self.label(doc, group['label']))
                        region.append(heading)
                    else:
                        region.append(self.label(doc, 'Chọn học liệu'))
                    package.insert_before(region)
                    region.append(package.extract())
                    groups.append({'label': group['label'], 'owner': package['data-package-id'], 'reason': group['reason']})
            else:
                region = doc.new_tag('div', attrs={'class': 'reading-region', 'data-reading-beat': group['sections'][0]})
                sections[0].insert_before(region)
                region.append(self.label(doc, group['label']))
                for section in sections:
                    region.append(section.extract())
                groups.append(group)
        actual = {
            'text': projection(hero) + ' ' + projection(root),
            'ids': [n['id'] for n in hero.select('[id]')] + [n['id'] for n in root.select('[id]')],
            'math': [str(n) for n in hero.select('math')] + [str(n) for n in root.select('math')],
            'headings': inventory(root)['headings'],
            'disclosures': inventory(root)['disclosures'],
        }
        if actual != original:
            raise ValueError('Home content/order/ID/math/disclosure projection changed: ' + ', '.join(k for k in original if actual[k] != original[k]))
        support = template('support.html', support_href=relative_href(REPO / 'docs/content/support/donate.html', self.output), prototype_note='HTML thử nghiệm trang Nhà · Dùng bộ khung từ G01 đã duyệt; trang Nhà chờ bạn xem, chưa áp dụng vào website chính thức.')
        footer, footer_info = self.site_footer() if footer_baseline or self.current_home else ('', None)
        styles = ['reading-regions.css', 'web-shell.css', 'course-home.css']
        if footer_baseline or self.current_home:
            self.materialize(KIT / 'site-footer.css', 'site-footer.css')
            styles.append('site-footer.css')
        if self.ui_baseline or self.current_home:
            styles.append('appearance-inline.css')
        result = template('page.html', title=html.escape(data['program']['title']), body_class='course-home', home_href='home-reading.html', breadcrumb='Tổng quan', drawer_title='Mục lục khóa học', navigation=self.navigation(), appearance=self.appearance(), hero=str(hero), content=str(root), support=support, site_footer=('\n    ' + footer if footer else ''), styles='\n'.join(f'<link rel="stylesheet" href="{name}">' for name in styles), scripts='<script src="site-ui.js"></script>', brand_thought=html.escape(BRAND_THOUGHT if self.ui_baseline else LEGACY_BRAND_THOUGHT))
        if self.current_home:
            current = BeautifulSoup(result, 'html.parser')
            for role in list(current.select('.reading-region > [data-reading-label]')):
                heading = role.parent.select_one('h2,h3,h4')
                if heading and projection(heading).casefold() == projection(role).casefold():
                    role.decompose()
            result = str(current)
        if footer_baseline:
            compare = without_requested_ui if self.ui_baseline else without_site_footer
            if compare(result) != compare(footer_baseline.read_text(encoding='utf-8')):
                raise ValueError('Footer-only build changed the pre-existing Home DOM; do not overwrite the approved layout.')
            footer_info['baseline'] = footer_baseline.relative_to(REPO).as_posix()
            footer_info['baseline_sha256'] = sha(footer_baseline)
            footer_info['ui_revision'] = 'FB027' if self.ui_baseline else None
        if write:
            (self.output / 'home-reading.html').write_text(result, encoding='utf-8')
        report = {'source': source.relative_to(REPO).as_posix(), 'source_sha256': sha(source), 'canonical_data': self.profile['data_source'], 'canonical_data_sha256': sha(data_file), 'partial_sha256': sha(partial_file), 'preserved_projection': True, 'source_inventory': original, 'reading_beats': groups, 'package_order': self.profile['expected_packages'], 'site_footer': footer_info}
        if not write:
            report['_html'] = result
        return report

    @staticmethod
    def label(doc: BeautifulSoup, text: str) -> Tag:
        node = doc.new_tag('span', attrs={'class': 'role', 'data-reading-label': ''})
        node.string = text
        return node

    @staticmethod
    def verify_home_data(root: Tag, data: dict) -> None:
        content = root.get_text(' ', strip=True)
        program = data['program']
        for key in ['status', 'tagline', 'introduction', 'audience', 'purpose', 'roadmap_note', 'foundations_note', 'r8_note', 'strands_note', 'start', 'd0', 'deployment']:
            if program[key] not in content:
                raise ValueError(f'Rendered Home is stale relative to canonical field {key}; rendering is not authorized in this task.')
        for key in ['learning_steps', 'roadmap']:
            if not all(value in content for value in program[key]):
                raise ValueError(f'Stale rendered sequence {key}')
        if not all(value['title'] in content for value in program['strands']):
            raise ValueError('Stale strands in rendered Home')
        packages = root.select('.zo-on-thi-package[data-package-id]')
        if [n['data-package-id'] for n in packages] != [n['id'] for n in data['packages']]:
            raise ValueError('Rendered package order differs from canonical data')
        for rendered, canonical in zip(packages, data['packages'], strict=True):
            if canonical['summary'] not in rendered.get_text(' ', strip=True):
                raise ValueError('Stale rendered package summary: ' + canonical['id'])

    def g01_reference(self, source: Path) -> dict:
        source = source.resolve()
        if sha(source) != ACCEPTED_G01_SHA:
            raise ValueError('G01 input does not match the owner-approved reference hash.')
        doc = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
        root = doc.select_one('.zo-on-thi-package')
        before = inventory(root)
        root['class'].append('reader-content')
        for style in doc.select('link[rel=stylesheet]'):
            style.decompose()
        for name in ['reading-regions.css', 'web-shell.css']:
            doc.head.append(doc.new_tag('link', rel='stylesheet', href=name))
        if self.ui_baseline:
            doc.head.append(doc.new_tag('link', rel='stylesheet', href='appearance-inline.css'))
            doc.select_one('.brand-thought').string = BRAND_THOUGHT
        for script in doc.select('script[src]'):
            script['src'] = 'r1-controller.js' if 'controller' in script['src'] else 'site-ui.js'
        self.normalize_links(doc.body, source)
        for link in doc.select('.site-top>a:first-child,.course-link,.rail-heading>a,.breadcrumb>a'):
            link['href'] = 'home-reading.html'
        doc.select_one('.appearance').replace_with(BeautifulSoup(self.appearance(), 'html.parser'))
        doc.body['data-zo-web-shell'] = ''
        doc.html['data-zo-preferences'] = 'zo-web-2027-preview-v1'
        trigger = doc.select_one('.mobile-trigger')
        trigger['aria-haspopup'] = 'dialog'; trigger['aria-controls'] = 'mobile-nav'; trigger['aria-expanded'] = 'false'
        doc.select_one('.prototype-note').string = 'Bản đối chứng bộ khung dùng chung · Thiết kế G01 đã duyệt 9/10; chưa áp dụng vào website chính thức.'
        doc.title.string = 'Đơn điệu và cực trị · Đối chứng bộ khung dùng chung · ZO Math'
        if inventory(root) != before:
            raise ValueError('Shared-kit adoption rewrote G01 content/IDs/math/heading order/disclosures.')
        if self.ui_baseline:
            baseline = self.ui_baseline.parent / 'g01-kit.html'
            if without_requested_ui(str(doc)) != without_requested_ui(baseline.read_text(encoding='utf-8')):
                raise ValueError('Requested UI changes modified the remaining G01 DOM.')
        (self.output / 'g01-kit.html').write_text(str(doc), encoding='utf-8')
        return {'source': source.relative_to(REPO).as_posix(), 'source_sha256': sha(source), 'preserved_projection': True, 'math_count': len(before['math']), 'ids_count': len(before['ids']), 'regions': len(root.select('.reading-region'))}

    def build(self, g01: Path | None, footer_baseline: Path | None = None, ui_baseline: Path | None = None) -> dict:
        if ui_baseline:
            if footer_baseline:
                raise ValueError('Use one explicit baseline mode at a time.')
            self.ui_baseline = ui_baseline.resolve()
            footer_baseline = self.ui_baseline
        if footer_baseline:
            footer_baseline = footer_baseline.resolve()
            audit_path(footer_baseline.parent)
            if footer_baseline.parent == self.output or not footer_baseline.is_file():
                raise ValueError('Footer baseline must be a separate existing audit preview, never overwritten.')
        before_file = self.output / 'protected-before.json'
        if not before_file.exists():
            protected = [REPO / name for name in ['_quarto.yml', '.gitignore']]
            for directory in ['assets', 'content/thpt/on_thi_toan_thpt', '_design/ngon_ngu_thiet_ke_zo_math_0_4/06_nguon', '_design/ngon_ngu_thiet_ke_zo_math_0_4/07_mau_thi_giac', '_audit/zo_design_web_2027_discovery_2026-10-07']:
                protected += [p for p in (REPO / directory).rglob('*') if p.is_file() and '_quy_trinh' not in p.parts and '__pycache__' not in p.parts]
            protected += [p for p in (REPO / 'docs/content/thpt/on_thi_toan_thpt').rglob('*') if p.is_file()]
            dump(before_file, {p.relative_to(REPO).as_posix(): sha(p) for p in protected})
        self.common_assets()
        home = self.home(g01 is not None, footer_baseline)
        reference = self.g01_reference(g01) if g01 else None
        report = {'kit': KIT.relative_to(REPO).as_posix(), 'kit_status': 'reusable_preview_not_production_not_final_0_5', 'home': home, 'g01_reference': reference, 'resources': self.resources, 'links': self.links}
        report['kit_source_hashes'] = {p.relative_to(REPO).as_posix(): sha(p) for p in sorted(KIT.rglob('*')) if p.is_file()}
        report['builder_sha256'] = sha(Path(__file__))
        report['output_hashes'] = {p.relative_to(self.output).as_posix(): sha(p) for p in sorted(self.output.rglob('*')) if p.is_file() and p.name in ['home-reading.html', 'g01-kit.html', 'reading-regions.css', 'web-shell.css', 'course-home.css', 'site-ui.js', 'r1-controller.js', 'site-footer.css', 'appearance-inline.css']}
        dump(self.output / 'build-manifest.json', report)
        return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='Named output subdirectory under _audit')
    parser.add_argument('--g01-reference', type=Path, help='Optional owner-approved G01 HTML, exact hash required')
    parser.add_argument('--footer-baseline', type=Path, help='Add Home footer only; require unchanged DOM against a separate existing Home preview')
    parser.add_argument('--ui-baseline', type=Path, help='FB-027 inline controls/full brand phrase; retain the approved Home footer and all remaining DOM')
    parser.add_argument('--g02', action='store_true', help='Build isolated G02 using its own reading map and the approved kit')
    parser.add_argument('--compare', action='store_true', help='Build G01/G02 matrix and isolated paired prototypes')
    args = parser.parse_args()
    if args.compare:
        from zo_web_2027_compare import build
        build(args.output)
        return 0
    if args.g02:
        from zo_web_2027_g02 import build
        print(json.dumps(build(args.output), ensure_ascii=False))
        return 0
    report = PreviewBuilder(args.output).build(args.g01_reference, args.footer_baseline, args.ui_baseline)
    print(json.dumps({'home': str(args.output / 'home-reading.html'), 'g01_reference_built': report['g01_reference'] is not None, 'home_reading_beats': len(report['home']['reading_beats']), 'preserved_projection': report['home']['preserved_projection']}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

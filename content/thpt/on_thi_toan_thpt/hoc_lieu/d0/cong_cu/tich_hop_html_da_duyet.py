"""One-time, explicit import of owner-approved HTML into canonical QMD.

Document scripts/styles are not executed or adopted as instructions. Content
is converted through Pandoc; the approval receipt independently locks every
section's text, TeX sequence, task IDs and comparison links.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from bs4 import BeautifulSoup, Comment

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[4]
RECEIPT = ROOT / '_quy_trinh/noi_dung_da_duyet.json'
SECTIONS = ['bat-dau', 'khai-bao-pham-vi', 'khao-sat', 'doc-ket-qua', 'chon-mach']


def signature(element):
    copy = BeautifulSoup(str(element), 'html.parser')
    for nav in copy.select('nav, .d0-nav-slot, .d0-live-materials'):
        nav.decompose()
    for fig in copy.select('.zo-variation-asset, .zo-variation'):
        fig.replace_with('BBT01_CANONICAL')
    math = []
    for node in copy.select('math'):
        annotation = node.select_one('annotation[encoding="application/x-tex"]')
        if annotation is None:
            raise ValueError('Công thức thiếu annotation TeX')
        tex = annotation.get_text()
        math.append(tex)
        node.replace_with('MATH[' + tex + ']')
    text = re.sub(r'\s+', '', copy.get_text())
    return {'text_sha256': hashlib.sha256(text.encode()).hexdigest(), 'math': math}


def pandoc(text, target, *options):
    result = subprocess.run(
        [sys.executable, str(REPO / 'scripts/zo_quarto.py'), 'pandoc',
         '--from=html+tex_math_single_backslash', '--to=' + target, '--wrap=none', *options],
        input=text, encoding='utf-8', capture_output=True, check=True, cwd=REPO)
    return result.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--approved-html', type=Path, required=True)
    args = parser.parse_args()
    raw = args.approved_html.read_bytes()
    soup = BeautifulSoup(raw.decode('utf-8-sig'), 'html.parser')
    root = soup.select_one('.d0-package')
    assert root is not None
    assert [s.get('id') for s in root.find_all('section', recursive=False)] == SECTIONS
    tasks = root.select('.d0-primary-task')
    expected = [f'd0-r{r}-{n:02}' for r in range(1, 9) for n in range(1, 4)]
    assert [t['id'] for t in tasks] == expected
    assert root.select_one('#doi-chieu-minh-hoa') is not None
    receipt = {'schema_version': 1, 'authority': 'Owner-approved khao_sat_dau_vao_D0.html',
               'source_sha256': hashlib.sha256(raw).hexdigest(),
               'sections': {i: signature(root.find(id=i)) for i in SECTIONS},
               'task_ids': expected,
               'links': [[a.get_text(' ', strip=True), a['href']] for a in root.select('a[href]')],
               'publication': 'pending'}

    # Preserve all wording. Replace only technical asset and link targets.
    for node in root.find_all(string=lambda s: isinstance(s, Comment)):
        node.extract()
    for node in root.select('script, style'):
        node.decompose()
    for node in root.select('math'):
        tex = node.select_one('annotation').get_text()
        node.replace_with(('\\[' + tex + '\\]') if node.get('display') == 'block' else ('\\(' + tex + '\\)'))
    for a in root.select('a[href]'):
        if a['href'] == 'https://zomath.vn/content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.html':
            a['href'] = '../../tot_nghiep_thpt/2027/index.qmd#hoc-lieu-hien-co'
    live = soup.new_tag('div', attrs={'class': 'd0-live-materials'})
    heading = soup.new_tag('p')
    heading.string = 'Học liệu hiện có'
    live.append(heading)
    listing = soup.new_tag('ul')
    for slug in ('r1_g01', 'r1_g02'):
        source = ROOT.parent / slug / 'index.qmd'
        assert source.is_file(), f'Missing learning material: {slug}'
        import yaml
        metadata = yaml.safe_load(source.read_text(encoding='utf-8').split('---', 2)[1])
        item = soup.new_tag('li')
        link = soup.new_tag('a', href=f'../{slug}/index.qmd')
        link.string = metadata['title']
        item.append(link)
        listing.append(item)
    live.append(listing)
    unavailable = soup.new_tag('p', attrs={'class': 'd0-availability'})
    unavailable.string = 'R2–R8: chưa có học liệu để mở.'
    live.append(unavailable)
    root.find(id='chon-mach').find('table').insert_before(live)
    for wrapper in reversed(root.select('.d0-data-table, .r1-table-scroll-x')):
        wrapper.unwrap()
    for image in root.select('img'):
        if image.get('src', '').startswith('data:'):
            image['src'] = 'hinh/hinh_hop.svg'
            image['alt'] = 'Hình biểu diễn hình hộp, không theo tỉ lệ.'
            image.attrs.pop('width', None)
            image.attrs.pop('height', None)
    for figure in root.select('.zo-variation-asset'):
        replacement = soup.new_tag('div', attrs={'class': 'zo-variation', 'bbt': 'BBT01'})
        figure.replace_with(replacement)
    for detail in root.select('details'):
        detail.name = 'div'
        detail['class'] = ['zo-learning-solution', 'r1-details', 'r1-solution']
        summary = detail.find('summary', recursive=False)
        summary.name = 'div'
        summary['class'] = ['zo-learning-summary']
        para = soup.new_tag('p')
        for child in list(summary.contents):
            para.append(child.extract())
        summary.append(para)
    for section in reversed(root.select('section')):
        heading = section.find(re.compile('^h[1-6]$'), recursive=False)
        if heading and section.get('id'):
            heading['id'] = section['id']
        section.unwrap()
    for node in root.select('[data-anchor-id]'):
        del node['data-anchor-id']
    root['class'] = ['zo-on-thi-package', 'd0-package']
    body = pandoc(str(root), 'markdown+fenced_divs+tex_math_dollars')
    metadata = '''---
title: "Khảo sát đầu vào"
lang: vi
draft: false
toc: false
sidebar: on-thi
number-sections: false
page-layout: article
body-classes: zo-page-article zo-meta-hidden zo-on-thi-package-page d0-page
filters:
  - cong_cu/d0.lua
format:
  html:
    title-block-style: default
    title-block-banner: false
    html-math-method: mathml
    anchor-sections: false
    fig-responsive: false
    css:
      - ../../../../../assets/css/zo_on_thi_learning_package.css
      - giao_dien/d0.css
    include-after-body:
      - giao_dien/d0_script.html
---

<!-- D0_APPROVED_CONTENT: canonical text source; approval receipt is provenance, not a second editable source. -->

'''
    qmd = metadata + body
    ROOT.joinpath('index.qmd').write_text(qmd, encoding='utf-8', newline='\n')
    receipt['qmd_sha256'] = hashlib.sha256(qmd.encode()).hexdigest()
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Imported 24 questions, Bài 00, 25 disclosures; canonical QMD ready for validation; unpublished.')


if __name__ == '__main__':
    main()

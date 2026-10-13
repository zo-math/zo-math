"""Shared scoped R1 presentation policy; no changes to mathematical content."""
import json
import os
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / '_design/web_2027_mau_dung_chung'

def apply(document, page, runtime):
    policy = json.loads((KIT/'profiles/r1-consistency.json').read_text(encoding='utf-8'))
    root = document.select_one('.reader-content')
    if root is None:
        raise ValueError('R1 policy needs the canonical reader root')
    for details in root.select('details'):
        details.attrs.pop('open', None)
        details['class'] = [c for c in details.get('class', []) if c != 'r1-open-by-default']
    for paper in root.select('.reading-region'):
        outer = paper.select_one(':scope > [data-reading-label]')
        if outer is None:
            continue
        heading = paper.select_one('h2')
        if heading is not None and heading.get_text(' ', strip=True) in policy['page_roles']:
            outer.string = policy['page_roles'][heading.get_text(' ', strip=True)]
        # Presentation-only metadata may not be duplicated inside its owner.
        for inner in list(paper.select('[data-reading-label]')):
            if inner is not outer and inner.get_text(' ', strip=True) == outer.get_text(' ', strip=True):
                inner.decompose()
    routing = root.select_one('#r1-table-t12, #r1-g02-table-t04')
    if routing is None:
        raise ValueError('Missing repair-routing table')
    table = routing.select_one('table')
    if [n.get_text(' ', strip=True) for n in table.select('thead th')] != policy['routing_headers']:
        raise ValueError('Repair-routing columns differ from the common contract')
    routing['class'] = routing.get('class', []) + ['r1-repair-routing']
    routing['data-col-widths'] = ','.join(str(n) for n in policy['routing_widths'])
    routing['data-min-width'] = '54em'
    routing['aria-label'] = 'Chọn bài sửa lỗi theo nơi phát hiện'
    routing['style'] = '; '.join([f'--r1-table-col-{i+1}: {n}%' for i,n in enumerate(policy['routing_widths'])]+['--r1-table-min-width:54em'])
    for header in root.select('.r1-table th'):
        header.attrs.pop('align', None)
        header['style'] = 'text-align:left'
    runtime.mkdir(parents=True, exist_ok=True)
    css = runtime/'r1-consistency.css'
    shutil.copyfile(KIT/css.name, css)
    document.head.append(document.new_tag('link', rel='stylesheet', href=os.path.relpath(css,page.parent).replace('\\','/')))

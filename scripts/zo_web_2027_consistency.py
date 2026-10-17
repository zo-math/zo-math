"""Shared scoped R1 presentation policy; no changes to mathematical content."""
import json
import re
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


def apply_editorial_policy(document):
    """Approved common page labels and titles; content stays source-owned."""
    policy=json.loads((KIT/'profiles/r1-consistency.json').read_text(encoding='utf-8'))
    root=document.select_one('.reader-content')
    if root is None:raise ValueError('Common editorial policy requires a reader')
    binding_path=ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu'/root['data-r1-code'].lower().replace('-','_')/'giao_dien/he_nhan.json'
    data=json.loads(binding_path.read_text(encoding='utf-8'))
    from zo_course_labels import apply_context_labels
    apply_context_labels(document,data)
    for heading in ([] if root.has_attr("data-zo-context-labels") else root.select('h2')):
        title=heading.get_text(' ',strip=True)
        prior=heading.find_previous_sibling(attrs={'data-reading-label':True})
        if title=='Kiểm tra':
            if prior:prior.decompose()
            continue
        if title not in policy['page_roles']:continue
        if prior:prior.string=policy['page_roles'][title]
        else:
            label=document.new_tag('span',attrs={'class':'role','data-reading-label':''})
            label.string=policy['page_roles'][title];heading.insert_before(label)
    document.title.string=root['data-r1-title']+' — ZO Math'
    require_editorial_policy(document)


def require_editorial_policy(document):
    policy=json.loads((KIT/'profiles/r1-consistency.json').read_text(encoding='utf-8'))
    root=document.select_one('.reader-content')
    for title in ([] if root.has_attr('data-zo-context-labels') else ['Bắt đầu','Bài học','Luyện tập','Ôn lại','Sửa lỗi','Nguồn']):
        heading=next((n for n in root.select('h2') if n.get_text(' ',strip=True)==title),None)
        label=heading.find_previous_sibling(attrs={'data-reading-label':True}) if heading else None
        if not label or label.get_text(strip=True)!=policy['page_roles'][title]:
            raise ValueError('Common area label missing: '+title)
    if document.title.get_text()!=root['data-r1-title']+' — ZO Math':
        raise ValueError('Browser title differs from common contract')
    for heading in ([] if root.has_attr('data-zo-context-labels') else root.select('h2')):
        if heading.get_text(strip=True)=='Kiểm tra' and heading.find_previous_sibling(attrs={'data-reading-label':True}):
            raise ValueError('Assessment must not inherit lesson self-check label')
    for label in root.select('[data-reading-label]'):
        following=label.find_next_sibling()
        if label.get_text(strip=True).casefold()=='ví dụ' and following and following.name in ['h3','h4','h5']:
            title=re.sub(r'^\d+(?:\.\d+)*\.\s*','',following.get_text(' ',strip=True)).casefold()
            if title.startswith('ví dụ'):raise ValueError('Repeated example label')
    for paragraph in root.select('p'):
        if re.search(r'\b(?:R1-)?G0[123]\b',paragraph.get_text(' ',strip=True)):
            raise ValueError('Management package code in learner prose')
    binding_path=ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu'/root['data-r1-code'].lower().replace('-','_')/'giao_dien/he_nhan.json'
    data=json.loads(binding_path.read_text(encoding='utf-8'))
    examples=data.get('editorial_examples') or [n for n in data.get('knowledge_units',[]) if n['type']=='type.example'] or data.get('examples',[])
    from zo_course_labels import context_html_checks, require
    require(context_html_checks(document,data),"parent-context HTML")
    for number,example in enumerate(examples,1):
        node=root.find(id=example['anchor'])
        title=re.search(r'Ví dụ\s+(\d{2})\s+—\s+([^\n]+)',node.get_text(' ',strip=True)) if node else None
        if not title or int(title.group(1))!=number:
            raise ValueError('Example title/continuous numbering differs from source binding: '+example['anchor'])

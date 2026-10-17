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
    if data.get('descriptive_task_titles'):
        for unit in data['units']:
            if unit['function'] not in {'function.guided_thinking','function.self_check','function.warmup'}:continue
            owner=root.find(id=unit['question'])
            candidates=owner.select('h2,h3,h4,h5,h6,.r1-task-label,p > strong')
            title=next((n for n in candidates if n.get_text(' ',strip=True)==unit['title']),None)
            if title is None:raise ValueError('Missing functional task title: '+unit['id'])
            title['class']=list(dict.fromkeys(title.get('class',[])+['zo-task-title']))
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
    require(presentation_checks(document,data),"shared reading presentation")
    from zo_course_math_assets import html_checks as math_asset_html_checks
    require(math_asset_html_checks(document,binding_path.parent.parent.name),"course math assets HTML")
    from zo_course_math_assets import lesson_display_checks
    require(lesson_display_checks(document,binding_path.parent.parent.name),"G03 graph layout HTML")
    for number,example in enumerate(examples,1):
        node=root.find(id=example['anchor'])
        title=re.search(r'Ví dụ\s+(\d{2})\s+—\s+([^\n]+)',node.get_text(' ',strip=True)) if node else None
        if not title or int(title.group(1))!=number:
            raise ValueError('Example title/continuous numbering differs from source binding: '+example['anchor'])


def separate_foundation_resources(document):
    """Each independent foundation disclosure is one paper, as in G01/G02."""
    from bs4 import BeautifulSoup
    factory=BeautifulSoup('', 'html.parser')
    owner=document.find(id='on-nen')
    if owner is None:return
    for resource in list(owner.select('details.r1-foundation-unit')):
        if resource.find_parent('details'):continue
        paper=resource.find_parent(class_='reading-region')
        if paper is None or resource.parent is not paper:continue
        if len(paper.find_all(recursive=False))==1:continue
        siblings=list(resource.find_next_siblings())
        unit=factory.new_tag('div',attrs={'class':'reading-region','data-reading-reason':'Independent foundation resource'})
        paper.insert_after(unit);unit.append(resource.extract())
        if siblings:
            tail=factory.new_tag('div',attrs={'class':'reading-region'})
            unit.insert_after(tail)
            for n in siblings:tail.append(n.extract())
        if not paper.get_text(strip=True) and not paper.find('img'):paper.decompose()


def presentation_checks(doc,data):
    """Four-page consistency contract, activated by its explicit package binding."""
    if not data.get('descriptive_task_titles'):return {}
    root=doc.select_one('.reader-content');checks={}
    for unit in data['units']:
        if unit['function'] not in {'function.guided_thinking','function.self_check','function.warmup'}:continue
        owner=root.find(id=unit['question']);title=owner.select_one('.zo-task-title') if owner else None
        checks[unit['id']+' shared visible question title']=bool(title and title.get_text(' ',strip=True)==unit['title'])
        if unit['function']=='function.guided_thinking':
            checks[unit['id']+' invitation before explanation']=bool(owner and 'Thử trả lời trước khi đọc tiếp.' in owner.get_text(' ',strip=True))
            checks[unit['id']+' local lesson prompt']=bool(owner and owner.find_parent(id='bai-hoc')) and not unit.get('answer')
            if unit.get('question_owner'):checks[unit['id']+' knowledge owner']=bool(owner and owner.find_parent(id=unit['question_owner']))
    for n,spec in enumerate(data.get('heading_context',[]),1):
        owner=root.find(id=spec['owner'])
        matches=[h for h in owner.select('h3,h4,h5,h6') if h.get_text(' ',strip=True)==spec['title']] if owner else []
        checks[f'subgroup {n} explicit context target']=len(matches)==1
    from zo_course_tables import media_html_checks
    checks.update(media_html_checks(doc))
    from zo_course_labels import answer_action_html_checks
    checks.update(answer_action_html_checks(doc,data))
    checks['cross-package references use the current bundle']=not any(re.match(r'https?://(?:www\.)?zomath\.vn/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g0[1-4](?:/|$)',a['href']) for a in root.select('a[href]'))
    notes=root.select('.zo-source-note')
    checks['source notes separate from prose']=bool(notes) and all(n.name=='p' or (n.parent.name=='p' and n.parent.get_text(' ',strip=True)==n.get_text(' ',strip=True)) for n in notes)
    checks['no bibliographic writing narration']=not any(re.search(r'Theo định nghĩa trong SGK|Theo phần .Chú ý. của SGK|Sách giáo khoa trình bày|Bản này dùng',p.get_text()) for p in root.select('#bai-hoc p') if not p.select('.zo-source-note'))
    calendar=root.find(id='on-lai').find('table')
    checks['review calendar has three functional columns']=bool(calendar) and len(calendar.select('thead th'))==3 and len(calendar.select('tbody tr'))==3
    resources=[n for n in root.select('#on-nen details.r1-foundation-unit') if not n.find_parent('details')]
    checks['independent foundation resources have distinct papers']=bool(resources) and len({id(n.find_parent(class_='reading-region')) for n in resources})==len(resources)
    checks['no authored heading-only reading paper']=all(p.select('p,li,table,figure,details,.zo-learning-task') for p in root.select('.reading-region'))
    return checks

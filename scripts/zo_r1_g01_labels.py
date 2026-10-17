"""G01 explicit semantic presentation bindings. No title/function inference.

The QMD and shared includes own mathematics; this file validates and projects
the approved package-specific labels/numbers without editing shared numbering.
"""
import json
import re
from pathlib import Path
from bs4 import NavigableString

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path('content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01')
BINDINGS = ROOT / PACKAGE / 'giao_dien/he_nhan.json'


def local_answer_pair(question, answer):
    """Same owned reading unit, not merely the same HTML page or area."""
    if question is None or answer is None:
        return False
    def owners(node):
        return [n for n in [node, *node.parents] if getattr(n,'attrs',None) is not None
                and ('reading-region' in n.get('class',[]) or
                     any(c in n.get('class',[]) for c in ['r1-foundation-unit','r1-foundation-confirmation']) or
                     (n.name=='details' and 'r1-solution' in n.get('class',[])))]
    return any(q is a for q in owners(question) for a in owners(answer))


def remove_local_answer_actions(root, units):
    for unit in units:
        q,a=root.find(id=unit['question']),root.find(id=unit.get('answer')) if unit.get('answer') else None
        if not local_answer_pair(q,a):continue
        for node,target in [(q,unit['answer']),(a,unit['question'])]:
            for link in list(node.select('.answer-link a[href="#'+target+'"]')):
                wrapper=link.find_parent(class_='answer-link');link.decompose()
                if not wrapper.get_text(' ',strip=True) and not wrapper.find('a'):wrapper.decompose()


def apply(document, binding_path=None):
    data = json.loads(Path(binding_path or BINDINGS).read_text(encoding='utf-8'))
    root = document.select_one('.reader-content')
    if data.get('package') not in ('R1-G01', 'R1-G02'):
        raise ValueError('Unsupported package semantic binding')
    targets = [a for u in data['units'] for a in (u['question'], u.get('answer')) if a]
    if len(targets) != len(set(targets)):
        raise ValueError('Duplicate semantic task/answer binding')
    for unit in data['units']:
        for target in [unit['question'], unit.get('answer')]:
            if not target:
                continue
            node = root.find(id=target)
            if node is None:
                raise ValueError('Missing semantic target: ' + target)
            node['data-zo-type'] = 'solution' if target == unit.get('answer') else 'task'
            node['data-zo-function'] = unit['function']
            node['data-zo-task'] = unit['id']
            if unit.get('number'):
                node['data-zo-number'] = str(unit['number'])
            # Neutral shared anchors precede their paragraphs. The package
            # binding inserts the heading locally; shared QMD contains no G01 number.
            if node.name == 'span':
                p = node.find_parent('p')
                task = p.find_next_sibling('p')
                if not task:
                    raise ValueError('Shared confirmation lacks paragraph: ' + target)
                strong = task.find('strong', recursive=False)
                if strong:
                    strong.decompose()
                holder = document.new_tag('div', attrs=dict(node.attrs))
                node.attrs.pop('id', None)
                if data['package'] == 'R1-G02':
                    for attribute in ['data-zo-type','data-zo-function','data-zo-task','data-zo-number']:
                        node.attrs.pop(attribute,None)
                p.insert_before(holder)
                heading = document.new_tag('h4'); heading.string = unit['title']
                holder.append(heading)
                holder.append(p.extract())
                holder.append(task.extract())
                for sibling in list(holder.find_next_siblings()):
                    if sibling.name == 'details': break
                    holder.append(sibling.extract())
                action = document.new_tag('div', attrs={'class':'answer-link'})
                link = document.new_tag('a',href='#'+unit['answer']);link.string='Xem lời giải'
                action.append(link);holder.append(action)
                node = holder
            title = node.select_one(':scope > h2, :scope > h3, :scope > h4, :scope > .r1-task-label, :scope > p > .r1-task-label, :scope > p > strong, :scope > summary')
            if title is None:
                title = node.select_one(':scope > section > h3, :scope > section > h4, :scope > .reading-region > h3, :scope > .reading-region > h4')
            # The worked repair example has one summary, not a second title
            # inside its answer. Reuse that summary while retaining the anchor.
            inherited_summary = False
            if target == 'lg-cg01':
                disclosure=node.find_parent('details',class_='r1-solution')
                title=disclosure.find('summary',recursive=False) if disclosure else None
                inherited_summary=title is not None
            if title is None:
                raise ValueError('Task/answer has no title: ' + target)
            if inherited_summary:
                title.string=unit['title']
                label=document.new_tag('span',attrs={'class':'role','data-reading-label':''})
                label.string=unit['label'];title.insert(0,label)
                continue
            title.string = unit['title']
            if title.name == 'summary':
                label = document.new_tag('span', attrs={'class':'role', 'data-reading-label':''})
                label.string = unit['label']; title.insert(0, label)
            else:
                existing = node.select_one(':scope > [data-reading-label]')
                if existing:
                    existing.string = unit['label']
                else:
                    label = document.new_tag('span', attrs={'class':'role', 'data-reading-label':''})
                    label.string = unit['label']; title.insert_before(label)
            # An enclosing paper must not repeat an inner task's role.
            paper = node if 'reading-region' in node.get('class', []) else node.find_parent(class_='reading-region')
            if paper:
                outer = paper.select_one(':scope > [data-reading-label]')
                if outer and outer.get_text(' ', strip=True) in ['Nhiệm vụ', 'Tự kiểm tra', 'Lời giải', 'Bài học', 'Ôn lại · Nhiệm vụ'] and outer.get_text(' ',strip=True) != unit['label']:
                    outer.decompose()
    for anchor, context in data['checkpoints'].items():
        node=root.find(id=anchor);node['data-zo-type']='checkpoint'
        label_owner = node
        if data['package'] == 'R1-G02' and 'reading-region' not in node.get('class', []):
            label_owner = node.select_one(':scope > .reading-region')
            if not label_owner:raise ValueError('Checkpoint outside a reading region: '+anchor)
        label=label_owner.select_one(':scope > [data-reading-label]')
        if not label:
            label=document.new_tag('span',attrs={'class':'role','data-reading-label':''})
            label_owner.insert(0,label)
        label.string=context
    for anchor in ['on-nen', 'nhat-ky', 'nguon', 'loi-giai', 'cách-học-với-tài-liệu-này']:
        owner = root.find(id=anchor)
        if owner:
            paper = owner if 'reading-region' in owner.get('class', []) else owner.select_one(':scope > .reading-region')
            if paper:
                label = paper.select_one(':scope > [data-reading-label]')
                heading = paper.select_one('h2,h3')
                if label and heading and label.get_text(' ', strip=True).casefold() == heading.get_text(' ', strip=True).casefold():
                    label.decompose()
    if data['package'] == 'R1-G02':
        for unit in data['knowledge_units']:
            node=root.find(id=unit['anchor'])
            if node is None or root.find(id=unit['owner']) is None:
                raise ValueError('Missing G02 knowledge target/owner: '+unit['anchor'])
            node['data-zo-type']=unit['type'].removeprefix('type.')
            node['data-zo-unit']=unit['id']
    # The common journal retains 14 fields. Only its G01 example references
    # receive the approved package binding (not a new journal schema).
    for text in list(root.select_one('#r1-table-t18').find_all(string=True)):
        if text.find_parent('math'):
            continue
        value = str(text).replace('Điểm kiểm soát sau chặng 1', 'Điểm dừng chặng 1 của Luyện tập').replace('Bài luyện tập 02', 'nhiệm vụ 02 của Luyện tập').replace('Sửa lỗi 02', 'Nhiệm vụ 02 của Sửa lỗi sau Luyện tập')
        if value != str(text):
            text.replace_with(NavigableString(value))
    remove_local_answer_actions(root,data['units'])
    return data


def remove_redundant_labels(document):
    """Omit contextual scaffolding, not the official semantic task labels."""
    trigger=document.select_one('.mobile-trigger')
    if trigger:trigger['aria-label']='Mở mục lục học liệu'
    drawer_title=document.select_one('#drawer-title')
    if drawer_title:drawer_title.string='Mục lục học liệu'
    rail=document.select_one('.rail')
    if rail:rail['aria-label']='Điều hướng học liệu'
    for paper in document.select('.reader-content .reading-region'):
        label=paper.find(attrs={'data-reading-label':True},recursive=False)
        if not label:continue
        wording=label.get_text(' ',strip=True).casefold()
        heading=paper.find(['h2','h3','h4','h5','h6'])
        title=heading.get_text(' ',strip=True).casefold() if heading else ''
        stage=wording=='chặng học' and title.startswith('chặng ')
        example=wording=='ví dụ' and re.sub(r'^\d+(?:\.\d+)*\.\s*','',title).startswith('ví dụ')
        misplaced=wording=='tự kiểm tra' and paper.find_parent(id='tu-kiem-tra')
        same=wording==title
        if stage or example or misplaced or same:label.decompose()

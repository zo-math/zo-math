"""Project explicitly declared review rounds into native, exclusive disclosures."""
import json
from pathlib import Path
import os

ASSETS=Path(__file__).resolve().parent/'assets'

def project(root,document):
    from zo_web_2027_g02 import inv
    before=inv(root)
    originals=list(root.select("details"))
    rounds=root.select('#on-lai > section[data-zo-review-disclosure="closed"]')
    if not rounds:return False
    for section in rounds:
        heading=section.find(['h3','h4'],recursive=False)
        if heading is None:raise ValueError('Review round lacks its source heading')
        panel=document.new_tag('details',attrs={'name':'r01-review-rounds','class':'zo-learning-guidance r01-review-round'})
        summary=document.new_tag('summary')
        summary.append(heading.extract());panel.append(summary)
        for child in list(section.contents):panel.append(child.extract())
        section.append(panel)
    after=inv(root)
    assert all(before[k]==after[k] for k in before if k!="disclosures"), "Review disclosure changed content, formula, link or ID"
    assert all(node in root.descendants for node in originals), "Existing disclosure lost"
    return True

def install(document,page,runtime):
    if not document.select('details.r01-review-round'):return
    for filename,kind in [('revision-review-rounds.js','script'),('revision-review-rounds.css','style')]:
        dest=Path(runtime)/filename;dest.write_bytes((ASSETS/filename).read_bytes())
        url=os.path.relpath(dest,Path(page).parent).replace('\\','/')
        node=document.new_tag('script',src=url) if kind=='script' else document.new_tag('link',rel='stylesheet',href=url)
        (document.body if kind=='script' else document.head).append(node)


def project_remediation(root, document):
    scope = root.find(id='sua-loi')
    if scope is None:
        return
    chooser = scope.select_one(':scope > section[data-zo-remediation-chooser]')
    nested = chooser is not None and chooser.select_one(':scope > section[data-zo-review-disclosure="closed"]') is not None
    parent = chooser if nested else scope
    groups = parent.select(':scope > section[data-zo-review-disclosure="closed"]')
    if not groups:
        return
    entries = []
    for section in parent.select(':scope > section[id]'):
        heading = section.find('h4' if nested else 'h3')
        if heading is None:
            raise ValueError('Remediation section lacks its source heading: ' + section['id'])
        entry = {'target': section['id'], 'label': heading.get_text(' ', strip=True)}
        entries.append(entry)
        if section not in groups:
            continue
        children = section.select(':scope > section.zo-learning-task[id]')
        entry['children'] = [
            {'target': task['id'], 'label': task.find(['h4', 'h5']).get_text(' ', strip=True)}
            for task in children
        ]
        wrap_group(section, heading, document, 'r01-remediation-groups')
    if nested:
        entries = [{'target': chooser['id'], 'label': chooser.find('h3').get_text(' ', strip=True),
                    'children': entries}]
    add_outline(root, 'sua-loi', entries)


def wrap_group(section, heading, document, name):
    panel = document.new_tag('details', attrs={
        'class': 'zo-learning-guidance r01-review-round',
        'name': name,
    })
    summary = document.new_tag('summary')
    label = heading.find_previous_sibling(attrs={'data-reading-label': True})
    if label:
        label['hidden'] = ''
        summary.append(label.extract())
    summary.append(heading.extract())
    panel.append(summary)
    for child in list(section.contents):
        panel.append(child.extract())
    section.append(panel)


def add_outline(root, view, entries):
    contents = json.loads(root.get('data-zo-contents', '[]'))
    if not any(entry['view'] == view for entry in contents):
        contents.append({'view': view, 'items': entries})
        root['data-zo-contents'] = json.dumps(contents, ensure_ascii=False, separators=(',', ':'))


def project_solutions(root):
    groups = root.select('#loi-giai > section:is([data-zo-solution-group="true"], :has(h3[data-zo-solution-group="true"]))')
    if not groups:
        return

    entries = []
    for section in groups:
        heading = section.find('h3')
        if heading is None:
            raise ValueError('Solution group lacks its source heading: ' + section['id'])
        section['data-zo-solution-group'] = 'true'
        entries.append({'target': section['id'], 'label': heading.get_text(' ', strip=True)})
        label = heading.find_previous_sibling(attrs={'data-reading-label': True})
        section.insert(0, heading.extract())
        if label:
            label['hidden'] = ''
            section.insert(0, label.extract())
    add_outline(root, 'loi-giai', entries)

"""Shared foundation hyperlinks: validate real canonical targets, no content duplication."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import json,re

def validate_local_answers(reader, units, action):
    """Keep the authored action for each numbered task's in-place solution."""
    for unit in units:
        if unit['function'] != 'function.foundation_confirmation':
            continue
        question = reader.find(id=unit['question'])
        answer = reader.find(id=unit['answer'])
        card = question.find_parent('details', class_='r1-foundation-unit') if question else None
        summary = answer.find('summary', recursive=False) if answer else None
        if (card is None or answer is None or answer.name != 'details'
                or answer.find_parent('details', class_='r1-foundation-unit') is not card
                or answer.has_attr('open') or summary is None
                or summary.get_text(' ', strip=True) != action):
            raise ValueError(f'Ôn nền: {unit["answer"]} must be a closed local solution labeled {action!r}')

    for activity in reader.select('#on-nen .r1-foundation-confirmation[data-zo-owner]'):
        card = activity.find_parent('details', class_='r1-foundation-unit')
        trailing_note = activity.find_next_sibling(class_='r1-foundation-return')
        if (activity.name != 'div' or card is None or card.get('id') != activity['data-zo-owner']
                or trailing_note is None):
            raise ValueError(f'Ôn nền: {activity["id"]} must appear before the return note in its own card')


def source_checks(source,data):
 if data.get('foundation_mode')!='linked-shared':return {}
 from zo_course_labels import expand
 source=Path(source);checks={};links=data.get('foundation_links',[])
 checks['nonempty unique linked foundation units']=bool(links) and len({v['unit_id'] for v in links})==len(links)
 text=source.read_text(encoding='utf-8')
 for item in links:
  split=urlsplit(item['href']);target=(source.parent/unquote(split.path)).with_suffix('.qmd').resolve()
  checks[item['unit_id']+' existing package QMD']=target.is_file() and target.parent.parent==source.parent.parent
  expanded=expand(target) if target.is_file() else ''
  checks[item['unit_id']+' real shared unit owner']=bool(re.search(r'\{#'+re.escape(unquote(split.fragment))+r'(?=[\s}])|\bid=[\"\']'+re.escape(unquote(split.fragment))+r'[\"\']',expanded))
  checks[item['unit_id']+' linked in source']=item['href'].replace('.html','.qmd') in text
 return checks

def html_checks(root,data):
 from urllib.parse import urlsplit,unquote
 checks={};links=data.get('foundation_links',[]);owner=root.find(id='on-nen')
 checks['linked foundation mode explicit']=data.get('foundation_mode')=='linked-shared' and bool(links) and owner is not None
 if owner is None:return checks
 actual=[(unquote(urlsplit(a['href']).path),urlsplit(a['href']).fragment) for a in owner.select('a[href]')]
 for item in links:
  url=urlsplit(item['href']);checks[item['unit_id']+' visible canonical link']=actual.count((unquote(url.path),url.fragment))==1
 checks['no duplicate authored foundation tasks']=not owner.select('[data-zo-task],details.r1-foundation-unit')
 return checks

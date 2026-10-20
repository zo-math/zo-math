"""Shared foundation hyperlinks: validate real canonical targets, no content duplication."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import json,re

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

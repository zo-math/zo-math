"""Refresh only the course-menu element of already published HTML."""
import html
import json
import re
import shutil
from pathlib import Path
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
import zo_publish as p
from zo_web_2027_navigation import PAGES, destinations


def refresh(data, name, output):
    key=next((k for k,(rel,_) in PAGES.items() if rel.as_posix()==name),None)
    if key is None or key=='home':raise p.ConfigError('Navigation-only requires a registered learner page: '+name)
    text=data.decode('utf-8')
    pattern=r'<nav\b[^>]*class=["\'][^"\']*\bcourse-panel\b[^"\']*["\'][^>]*>.*?</nav>'
    matches=list(re.finditer(pattern,text,re.S))
    if len(matches)!=1:raise p.ConfigError('Expected exactly one existing course menu: '+name)
    match=matches[0];old=BeautifulSoup(match[0],'html.parser').nav
    links=[]
    for dest,href,label in destinations(output,output/name,key):
        current=' aria-current="page"' if dest==key else ''
        links.append('<a data-course-page="'+html.escape(dest,quote=True)+'" href="'+html.escape(href,quote=True)+'"'+current+'>'+html.escape(label)+'</a>')
    opening=match[0][:match[0].index('>')+1]
    replacement=opening+''.join(links)+'</nav>'
    return (text[:match.start()]+replacement+text[match.end():]).encode('utf-8')


def inherit(public, output, names, config):
    manifest=p.tree_manifest(public,True);missing=[]
    keep=set(names)|p.asset_dependencies(public,manifest,names,missing)
    if missing:raise p.ConfigError('Published menu inputs missing dependencies: '+str(missing))
    for name in keep:
        target=output/name
        if not target.exists():
            target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(public/name,target)
    seals={}
    for name in names:
        source=public/name
        (output/name).write_bytes(refresh(source.read_bytes(),name,output))
        seals[name]=p.sha256(source)
    from zo_publish_pages import page_for_record
    search=output/'search.json';old=json.loads((public/'search.json').read_text('utf-8'))
    new=json.loads(search.read_text('utf-8')) if search.exists() else []
    new=[x for x in new if page_for_record(x,config) not in names]+[x for x in old if page_for_record(x,config) in names]
    p.write_text_lf(search,json.dumps(new,ensure_ascii=False,indent=2)+'\n')
    sitemap=output/'sitemap.xml';tree=ET.parse(sitemap if sitemap.exists() else public/'sitemap.xml');root=tree.getroot()
    def location(node):
        loc=next((x for x in node if x.tag.rsplit('}',1)[-1]=='loc'),None)
        return page_for_record({'href':loc.text},config) if loc is not None else None
    for node in list(root):
        if location(node) in names:root.remove(node)
    for node in ET.parse(public/'sitemap.xml').getroot():
        if location(node) in names:root.append(node)
    p.write_text_lf(sitemap,ET.tostring(root,encoding='unicode')+'\n')
    return seals


def verify(backup, target, seals):
    for name,digest in seals.items():
        if p.sha256(backup/name)!=digest:raise p.ConfigError('Navigation baseline changed: '+name)
        if refresh((backup/name).read_bytes(),name,target)!=(target/name).read_bytes():
            raise p.ConfigError('Change outside the canonical menu: '+name)

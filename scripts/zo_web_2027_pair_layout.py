"""Explicit G01 layout migration for the user-authorized pair corrections.

Writes an audit candidate only. Normal production continues to use its strict
canonical source fingerprint and never reads audit HTML as build input.
"""
import copy
import json
from pathlib import Path
import re
import sys
from bs4 import BeautifulSoup, Comment, NavigableString, Tag
from zo_web_2027_production import pools, sha, norm, content_fingerprint

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/'_audit/zo_web_pair_refinement_2026-10-08'
PACKAGE=Path('content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01')

def short(value):
    value={'Khi em gặp lỗi này':'Dấu hiệu cần sửa','Bài sau Luyện tập':'Sau Luyện tập',
           'Bài sau Kiểm tra':'Sau Kiểm tra','Bài sau Ôn lại':'Sau Ôn lại'}.get(value,value)
    for old,new in [('Bài Ôn lại','Ôn lại'),('bài Ôn lại','lượt Ôn lại'),
                    ('Bài sửa lỗi','Sửa lỗi'),('Bài tập khắc phục lỗi','Sửa lỗi'),
                    ('Chọn bài tập khắc phục lỗi','Chọn bài sửa lỗi')]:
        value=value.replace(old,new)
    return value

def main():
    old=BeautifulSoup((AUDIT/'r1_g01-raw/docs'/PACKAGE/'index.html').read_text(encoding='utf-8'),'html.parser')
    fresh=BeautifulSoup((AUDIT/'after/r1_g01-raw/docs'/PACKAGE/'index.html').read_text(encoding='utf-8'),'html.parser')
    oldroot=old.select_one('.zo-on-thi-package');root=fresh.select_one('.zo-on-thi-package')
    oldtexts,_=pools(oldroot);texts,maths=pools(root)
    plan=json.loads((AUDIT/'g01-layout-before.json').read_text(encoding='utf-8'))
    replaced=[]
    def rebind(node):
        if node.get('attrs',{}).get('id')=='loi-giai':return
        if 'text' in node:
            key=node['text']
            if key not in texts:
                value=norm(short(oldtexts[key]));newkey=sha(value)
                if newkey not in texts:
                    raise ValueError('Unapproved missing text binding: '+oldtexts[key])
                node['text']=newkey;replaced.append(value)
        if node.get('tag')=='details':
            node['attrs'].pop('open',None)
            node['attrs']['class']=[c for c in node['attrs'].get('class',[]) if c!='r1-open-by-default']
        for child in node.get('children',[]):rebind(child)
    rebind(plan['layout'])
    def encode(node):
        if isinstance(node,Comment):return None
        if isinstance(node,NavigableString):
            value=str(node)
            if not value.strip():return {'literal':value}
            key=sha(norm(value))
            if key not in texts:return {'literal':value}
            return {'text':key,'leading':re.match(r'^\s*',value).group(),'trailing':re.search(r'\s*$',value).group()}
        if not isinstance(node,Tag):return None
        if node.name=='math':
            key=sha(norm(node.select_one('annotation').get_text()))
            if key not in maths:raise ValueError('Unknown math')
            return {'math':key}
        attrs=copy.deepcopy(node.attrs)
        if node.name=='img':attrs['src']={'package_asset':attrs['src']}
        return {'tag':node.name,'attrs':attrs,'children':[v for c in node.children if (v:=encode(c)) is not None]}
    def get(ident,node=None):
        node=node or plan['layout']
        if node.get('attrs',{}).get('id')==ident:return node
        for child in node.get('children',[]):
            found=get(ident,child)
            if found:return found
    # Approved paper/shell geometry is retained outside the explicitly reopened
    # solution structure and the visible introductory stages.
    stages=encode(root.find(id='lo-trinh-hoc'))
    start=get('cách-học-với-tài-liệu-này')
    def add_stage(node):
        for i,child in enumerate(node.get('children',[])):
            if child.get('tag')=='ol':node['children'].insert(i+1,stages);return True
            if add_stage(child):return True
        return False
    if not add_stage(start):raise ValueError('Start reading beat not found')
    solution=copy.deepcopy(root.find(id='loi-giai'))
    def label(text):
        n=fresh.new_tag('span',attrs={'class':'role','data-reading-label':''});n.string=text;return n
    def wrap(section):
        pending=[]
        def flush():
            if not pending:return
            paper=fresh.new_tag('div',attrs={'class':'reading-region','data-reading-reason':'Đối chiếu đúng hoạt động; giữ đề, đáp án và đường quay về cùng chủ sở hữu.'})
            pending[0].insert_before(paper);paper.append(label('Lời giải'))
            for n in pending:paper.append(n.extract())
            pending.clear()
        for node in list(section.find_all(recursive=False)):
            if node.name=='section':flush();wrap(node)
            elif node.name=='details' and 'r1-solution' in node.get('class',[]):
                pending.append(node);flush()
            else:pending.append(node)
        flush()
    wrap(solution)
    for image in solution.select('figure img'):
        viewport=fresh.new_tag('div',attrs={'class':'figure-viewport','tabindex':'0','role':'region','aria-label':image.get('alt','Hình toán học')+' — có thể cuộn ngang'})
        image.wrap(viewport)
    replacement=encode(solution)
    def replace(node):
        for i,child in enumerate(node.get('children',[])):
            if child.get('attrs',{}).get('id')=='loi-giai':node['children'][i]=replacement;return True
            if replace(child):return True
        return False
    if not replace(plan['layout']):raise ValueError('Solution owner not found')
    # Update only the explicitly modified common controller asset receipt.
    for digest,spec in list(plan['assets'].items()):
        if spec['name']=='r1-controller.js':
            newkey=sha((ROOT/spec['source']).read_bytes());spec['sha256']=newkey
            plan['assets'][newkey]=plan['assets'].pop(digest)
            def assets(node):
                for value in node.get('attrs',{}).values():
                    if isinstance(value,dict) and value.get('asset')==digest:value['asset']=newkey
                for child in node.get('children',[]):assets(child)
            assets(plan['layout'])
    plan['source_fingerprint']=content_fingerprint(root)
    plan['refinement']={'scope':'User-listed G01/G02 corrections 2026-10-08',
        'status':'candidate_pending_owner_review','historical_acceptance_retained':True}
    destination=AUDIT/'g01-layout-candidate.json'
    destination.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (AUDIT/'layout-migration.json').write_text(json.dumps({'rebound_texts':replaced,
        'new_source_fingerprint':plan['source_fingerprint'],'candidate':str(destination),
        'canonical_written':False,'accepted_receipt_updated':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Audit layout candidate ready; bindings',len(replaced))

if __name__=='__main__':main()

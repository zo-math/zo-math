"""Add declared optional videos without rebuilding published course HTML.

The published Git tree is the baseline. Source prose must equal the recorded
published source after removing only the declared video additions. The inverse
check and exact three-file diff are repeated before publication.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import hashlib,json,posixpath,re,shutil
from bs4 import BeautifulSoup
import zo_publish as p

PAGE='content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.html'
PACKAGE=Path(PAGE).parent
PLAN=PACKAGE/'_quy_trinh/ho_so/videos_20261104_placements.json'
ASSETS={f'assets/zo_web_2027/r1_g01_revision_r01/reader/video.{ext}':PACKAGE/f'giao_dien/video.{ext}' for ext in ('css','js')}
BLOCK=re.compile(r'```\{=html\}\n(<details class="zo-block zo-block-gray zo-learning-video".*?</details>)\n```\n\n',re.S)
IMPORTS='```{=html}\n<link rel="stylesheet" href="giao_dien/video.css">\n<script src="giao_dien/video.js" defer></script>\n```\n'
sha=lambda data:hashlib.sha256(data).hexdigest()

class Spans(HTMLParser):
    """Locate insertion boundaries without serializing any existing HTML."""
    VOID=set('area base br col embed hr img input link meta param source track wbr'.split())
    def __init__(self,text):
        super().__init__(convert_charrefs=False)
        self.text=text;self.lines=[0];self.nodes=[];self.stack=[]
        self.lines.extend(m.end() for m in re.finditer('\n',text))
        self.feed(text);self.close()
        if self.stack:raise p.ConfigError('Unclosed published HTML')
    def position(self):
        line,column=self.getpos();return self.lines[line-1]+column
    def handle_starttag(self,tag,attrs):
        start=self.position();end=start+len(self.get_starttag_text())
        node=dict(tag=tag,attrs=dict(attrs),start=start,opening_end=end,end=end,close=start,parent=self.stack[-1] if self.stack else None)
        self.nodes.append(node)
        if tag not in self.VOID:self.stack.append(node)
    def handle_startendtag(self,tag,attrs):
        self.handle_starttag(tag,attrs)
        if tag not in self.VOID:self.stack.pop()
    def handle_endtag(self,tag):
        if tag in self.VOID:return
        if not self.stack or self.stack[-1]['tag']!=tag:raise p.ConfigError('Mismatched published HTML boundary: '+tag)
        node=self.stack.pop();node['close']=self.position();node['end']=self.text.index('>',node['close'])+1
    def one(self,ident):
        found=[n for n in self.nodes if n['attrs'].get('id')==ident]
        if len(found)!=1:raise p.ConfigError('Missing or duplicate placement anchor: '+ident)
        return found[0]

def inside(node,owner):
    while node:
        if node is owner:return True
        node=node['parent']
    return False

def source_blocks(root,baseline):
    if not re.fullmatch('[0-9a-f]{40,64}',baseline):raise p.ConfigError('Invalid published source commit')
    blocks={};seals={};seen=set()
    def visit(name):
        path=(root/name).resolve()
        if not path.is_relative_to((root/PACKAGE).resolve()):raise p.ConfigError('Video source escapes package')
        if name in seen:return
        seen.add(name);text=path.read_text(encoding='utf-8')
        before=p.git(root,'show',baseline+':'+name.as_posix())
        if before.returncode:raise p.ConfigError('Published source unavailable: '+str(name))
        for match in BLOCK.finditer(text):
            fragment=match[1];doc=BeautifulSoup(fragment,'html.parser');node=doc.details
            if node is None:raise p.ConfigError('Video disclosure missing')
            ident=node.get('id','');video=node.get('data-youtube-id','')
            if not re.fullmatch('video-[a-z0-9-]+',ident) or not re.fullmatch(r'[\w-]{11}',video) or ident in blocks:
                raise p.ConfigError('Invalid or duplicate source video')
            if any(n.name not in {'details','summary','div','p','a'} or any(k.startswith('on') or k in {'style','src','srcdoc','open'} for k in n.attrs) for n in doc.find_all()):
                raise p.ConfigError('Unexpected video markup')
            links=doc.select('a[href]')
            if len(links)!=1 or links[0]['href']!='https://www.youtube.com/shorts/'+video or not node.select_one(':scope > summary') or len(node.select('.zo-video-player'))!=1:
                raise p.ConfigError('Invalid source video link or player')
            blocks[ident]=fragment.replace('zo-learning-video"','zo-learning-video r1-details"',1)
        stripped=BLOCK.sub('',text).replace(IMPORTS,'').replace('  - giao_dien/video.css\n  - giao_dien/video.js\n','')
        stripped=stripped.replace('## Bài học {#bai-hoc}\n\n\n','## Bài học {#bai-hoc}\n\n')
        if stripped!=before.stdout.replace('\r\n','\n'):raise p.ConfigError('Non-video source change: '+name.as_posix())
        seals[name.as_posix()]=p.sha256(path)
        for include in re.findall(r'\{\{<\s*include\s+([^>]+?)\s*>\}\}',text):visit(name.parent/include.strip().strip('"'))
    visit(PACKAGE/'index.qmd')
    return blocks,seals

def refresh(root,data,name,baseline):
    if name!=PAGE:raise p.ConfigError('Video-only page is not registered')
    plan=json.loads((root/PLAN).read_text('utf-8'))
    if plan.get('version')!=1 or plan.get('page')!=PAGE:raise p.ConfigError('Unsupported video placement plan')
    blocks,sources=source_blocks(root,baseline);placements=plan['placements']
    if len(placements)!=len(blocks) or {x['id'] for x in placements}!=set(blocks):raise p.ConfigError('Video placement coverage differs from source')
    text=data.decode('utf-8')
    if 'data-zo-course-site="r20-integrated-v1"' not in text or 'zo-learning-video' in text:raise p.ConfigError('Expected unmodified published canonical course HTML')
    doc=Spans(text);edits=[]
    for item in placements:
        anchor=doc.one(item['anchor']);mode=item['mode']
        if inside(anchor,doc.one('tu-kiem-tra')):raise p.ConfigError('Video cannot be placed in the test')
        if mode=='before_region':
            region=anchor['parent']
            if region is None or 'reading-region' not in region['attrs'].get('class','').split():raise p.ConfigError('Task reading region changed')
            at=region['start']
        elif mode=='end_section':
            if anchor['tag']!='section':raise p.ConfigError('Expected a lesson section')
            at=anchor['close']
        elif mode in {'before_paragraph','before_answer'}:
            if anchor['tag']!='details':raise p.ConfigError('Expected an existing support disclosure')
            choices=[]
            for node in doc.nodes:
                if not inside(node,anchor):continue
                markup=text[node['start']:node['end']]
                if mode=='before_paragraph' and node['tag']=='p' and BeautifulSoup(markup,'html.parser').get_text(' ',strip=True).startswith(item['text']):choices.append(node)
                if mode=='before_answer' and 'answer-link' in node['attrs'].get('class','').split() and BeautifulSoup(markup,'html.parser').select_one('a[href="'+item['href']+'"]'):choices.append(node)
            if len(choices)!=1:raise p.ConfigError('Ambiguous video insertion inside '+item['anchor'])
            at=choices[0]['start']
        else:raise p.ConfigError('Unknown video placement mode')
        content=blocks[item['id']]
        if mode in {'before_region','end_section'}:content='<div class="reading-region" data-reading-reason="Optional video supporting the preceding example">'+content+'</div>'
        edits.append((at,'<!-- zo-video:'+item['id']+' -->'+content+'<!-- /zo-video:'+item['id']+' -->\n'))
    heads=[n for n in doc.nodes if n['tag']=='head']
    if len(heads)!=1:raise p.ConfigError('Expected one HTML head')
    imports=[]
    for dest in ASSETS:
        href=posixpath.relpath(dest,PACKAGE.as_posix())
        imports.append('<link rel="stylesheet" href="'+href+'"/>' if dest.endswith('.css') else '<script src="'+href+'" defer></script>')
    edits.append((heads[0]['close'],'<!-- zo-video-assets -->'+''.join(imports)+'<!-- /zo-video-assets -->'))
    if len({at for at,_ in edits})!=len(edits):raise p.ConfigError('Overlapping video placement boundaries')
    result=text
    for at,content in sorted(edits,reverse=True):result=result[:at]+content+result[at:]
    inverse=re.sub(r'<!-- zo-video:[^>]+ -->.*?<!-- /zo-video:[^>]+ -->\n|<!-- zo-video-assets -->.*?<!-- /zo-video-assets -->','',result,flags=re.S)
    if inverse.encode('utf-8')!=data:raise p.ConfigError('Existing HTML bytes changed')
    receipt=dict(baseline_html=sha(data),baseline_source=baseline,sources=sources,plan=p.sha256(root/PLAN),assets={dest:p.sha256(root/src) for dest,src in ASSETS.items()},videos=len(blocks))
    return result.encode('utf-8'),receipt

def inherit(root,public,output,names,config):
    if names!=[PAGE]:raise p.ConfigError('Video-only release must select exactly R1-G01')
    baseline=p.published_source_commit(root,public)
    manifest=p.tree_manifest(public,True);missing=[]
    keep=set(names)|p.asset_dependencies(public,manifest,names,missing)|{'search.json','sitemap.xml'}
    if missing:raise p.ConfigError('Published video baseline has missing dependencies')
    for name in keep:
        dest=output/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(public/name,dest)
    content,seal=refresh(root,(public/PAGE).read_bytes(),PAGE,baseline)
    (output/PAGE).write_bytes(content)
    for name,source in ASSETS.items():
        if (public/name).exists():raise p.ConfigError('Video-only asset already exists in baseline: '+name)
        dest=output/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/source,dest)
    return {PAGE:seal}

def verify(root,backup,target,seals):
    if set(seals)!={PAGE}:raise p.ConfigError('Unexpected video-only receipt scope')
    seal=seals[PAGE]
    expected,current=refresh(root,(backup/PAGE).read_bytes(),PAGE,seal['baseline_source'])
    if current!=seal or (target/PAGE).read_bytes()!=expected:raise p.ConfigError('Video-only source, baseline or HTML drift')
    before=p.tree_manifest(backup,True);after=p.tree_manifest(target,True);diff=p.exact_diff(before,after)
    if diff['delete'] or diff['update']!=[PAGE] or set(diff['add'])!=set(ASSETS):raise p.ConfigError('Change outside the video page and two new assets')
    for name,digest in seal['assets'].items():
        if p.sha256(target/name)!=digest:raise p.ConfigError('Video asset drift: '+name)

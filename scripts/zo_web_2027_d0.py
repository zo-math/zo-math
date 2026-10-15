"""Canonical D0 presentation adapter from fresh Quarto; preserves its own survey."""
from __future__ import annotations
import copy,html,json,os,re,sys
from pathlib import Path
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET
sys.dont_write_bytecode=True
from bs4 import BeautifulSoup,Tag
from zo_web_2027_home import HomeBuilder
from zo_web_2027_preview import REPO,KIT,DESIGN04,BRAND_THOUGHT,template,inventory,sha

PACKAGE=Path('content/thpt/on_thi_toan_thpt/hoc_lieu/d0')
D0=PACKAGE/'index.html'
MARKER='zo-web-2027-d0'
LAYOUT=REPO/PACKAGE/'giao_dien/web_2027_layout.json'

def strip_papers(root):
    root=copy.deepcopy(root)
    for n in root.select('[data-design-disclosure]'):
        summary=n.select_one('summary');p=BeautifulSoup('<p></p>','html.parser').p
        p.string=summary.get_text(' ',strip=True)
        n.select_one('.d0-survey-toc').insert(0,p);summary.decompose()
        n.unwrap()
    for n in root.select('.reading-region'):
        classes=n.get('class',[])
        if n.name=='details':n['class']=[c for c in classes if c!='reading-region'];n.attrs.pop('data-reading-beat',None)
        else:n.unwrap()
    return root

def apply_regions(root,profile):
    maker=BeautifulSoup('','html.parser')
    beats=[]
    def wrap(owner,nodes,key,reason):
        if not nodes:return
        paper=maker.new_tag('div',attrs={'class':'reading-region','data-reading-beat':key})
        nodes[0].insert_before(paper)
        for n in nodes:paper.append(n.extract())
        beats.append({'owner':owner,'key':key,'reason':reason,'source_ids':[n['id'] for n in paper.select('[id]')]})
    def children(n):return [x for x in n.children if isinstance(x,Tag)]
    for spec in profile['views']:
        section=root.find(id=spec['id']);nodes=children(section);policy=spec['policy'];reason=spec['reason']
        if policy=='whole':wrap(spec['id'],nodes,spec['id'],reason)
        elif policy in {'subsections','selection'}:
            front=[]
            for n in nodes:
                if n.name=='section':
                    if front:wrap(spec['id'],front,spec['id'],reason);front=[]
                    wrap(spec['id'],children(n),n['id'],reason)
                else:front.append(n)
            if front:wrap(spec['id'],front,spec['id'],reason)
        elif policy=='tasks':
            front=[n for n in nodes if not(n.name=='section')];wrap(spec['id'],front,spec['id'],reason)
            for strand in [n for n in nodes if n.name=='section']:
                current=[];key=strand['id']
                for n in children(strand):
                    if 'd0-primary-task' in n.get('class',[]):
                        if any('d0-primary-task' in x.get('class',[]) for x in current):wrap(spec['id'],current,key,reason);current=[]
                        key=n['id']
                    current.append(n)
                wrap(spec['id'],current,key,reason)
        elif policy=='answers':
            front=[]
            for n in nodes:
                if n.name in {'details','section'}:
                    if front:wrap(spec['id'],front,spec['id'],reason);front=[]
                    if n.name=='details':
                        n['class']=n.get('class',[])+['reading-region'];n['data-reading-beat']=n['id']
                        beats.append({'owner':spec['id'],'key':n['id'],'reason':reason,'source_ids':[n['id']]})
                    else:wrap(spec['id'],children(n),n['id'],reason)
                else:front.append(n)
            if front:wrap(spec['id'],front,spec['id'],reason)
        else:raise ValueError('Unknown D0 reading policy')
    return beats

class D0Builder(HomeBuilder):
    def __init__(self,page,output_root):
        super().__init__(page,output_root)
        self.runtime=self.output_root/'assets/zo_web_2027/d0'
        self.layout=json.loads(LAYOUT.read_text(encoding='utf-8'))

    def common_assets(self):
        for name in ['reading-regions.css','web-shell.css','site-ui.js','appearance-inline.css','site-footer.css']:
            self.materialize(KIT/name,name)
        for name in ['web_2027.css','web_2027.js']:self.materialize(REPO/PACKAGE/'giao_dien'/name,name)
        for name in ['horizontal_color.svg','stack_color.svg','favicon_color.svg']:
            self.materialize(DESIGN04/'logos'/name,'assets/logos/'+name)
        for name in ['BeVietnamPro_Regular.ttf','BeVietnamPro_SemiBold.ttf','STIXTwoMath.ttf','OFL_BeVietnamPro.txt']:
            self.materialize(DESIGN04/'assets'/name,'assets/fonts/'+name)
        licences=list((DESIGN04/'assets').glob('*STIX*txt'))
        if len(licences)!=1:raise ValueError('Expected STIX license')
        self.materialize(licences[0],'assets/fonts/'+licences[0].name)

    def build_current(self):
        source=BeautifulSoup(self.page.read_text(encoding='utf-8'),'html.parser')
        title=source.select_one('h1.title').get_text(' ',strip=True)
        root=source.select_one('.d0-package');original=inventory(root);markup=str(root)
        if [n.get('id') for n in root.find_all('section',recursive=False)]!=[s['id'] for s in self.layout['views']]:raise ValueError('D0 view map stale')
        self.common_assets()
        beats=apply_regions(root,self.layout)
        if inventory(root)!=original:raise ValueError('Reading map changed D0 content')
        root['class']=root.get('class',[])+['reader-content']
        root['data-d0-views']=json.dumps([s['id'] for s in self.layout['views']])
        toc=root.select_one('.d0-survey-toc');label=toc.select_one(':scope > p');details=source.new_tag('details',attrs={'class':'r1-section-toc','data-design-disclosure':'toc'})
        summary=source.new_tag('summary');summary.string=label.get_text(' ',strip=True);label.decompose();toc.wrap(details);details.insert(0,summary)
        self.normalize_links(root,self.page)
        for image in root.select('img'):
            asset=Path(urlsplit(image['src']).path).name
            canonical=REPO/PACKAGE/'hinh'/('bbt01.svg' if asset.endswith('bbt01.svg') else 'hinh_hop.svg')
            vector=ET.parse(canonical).getroot()
            width=float(vector.attrib['viewBox'].split()[2])*4/3
            image['style']=f'--figure-width:{width:.3f}px'
            frame=source.new_tag('div',attrs={'class':'figure-viewport','tabindex':'0','role':'region','aria-label':'Hình toán — cuộn ngang nếu cần'})
            image.wrap(frame)
        if inventory(strip_papers(root))!=original:raise ValueError('D0 presentation changed original sequence')
        home=self.href(self.output_root/'content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.html')
        nav='<nav class="d0-nav" aria-label="Các phần của bài khảo sát"><div class="r1-tab-group"><span class="r1-tab-group-label">Khảo sát đầu vào</span><div class="r1-tab-group-items">'+''.join('<a class="r1-tab" href="#'+s['id']+'">'+html.escape(s['label'])+'</a>' for s in self.layout['views'])+'</div></div></nav>'
        footer,footer_info=self.site_footer()
        styles=['reading-regions.css','web-shell.css','appearance-inline.css','site-footer.css','web_2027.css']
        hero='<header class="hero"><div class="hero-copy"><h1>'+html.escape(title)+'</h1></div></header>'
        doc=BeautifulSoup(template('page.html',title=title,body_class='d0-web '+MARKER,home_href=home,breadcrumb=title,drawer_title='Mục lục khảo sát',navigation=nav,appearance=self.appearance(),hero=hero,content=str(root),support='',site_footer=footer,styles=''.join('<link rel="stylesheet" href="'+n+'">' for n in styles),scripts='<script src="site-ui.js"></script><script src="web_2027.js"></script>',brand_thought=html.escape(BRAND_THOUGHT)),'html.parser')
        doc.title.string=title+' — ZO Math'
        doc.body['data-zo-web-production']='d0'
        doc.select_one('.lab-link').string='ZO Math'
        doc.select_one('.rail-support')['href']=self.href(self.output_root/'content/support/donate.html')
        trigger=doc.select_one('.mobile-trigger');trigger['aria-label']='Mở mục lục khảo sát';trigger['class'].append('mobile-trigger--icon')
        for n in doc.select('link[href],script[src],img[src]'):
            key='src' if n.has_attr('src') else 'href'
            if n[key] in self.runtime_hrefs:n[key]=self.runtime_hrefs[n[key]]
        if '_audit/' in str(doc) or doc.select('script[src*="r1-controller"]'):raise ValueError('D0 runtime dependency outside canonical scope')
        if inventory(strip_papers(doc.select_one('.d0-package')))!=original:raise ValueError('D0 final projection differs')
        from zo_course_tables import apply as apply_tables
        apply_tables(doc,'d0',self.page,self.runtime)
        self.resources['course-tables.css']={'source':'_design/web_2027_mau_dung_chung/course-tables.css','sha256':sha(KIT/'course-tables.css')}
        from zo_web_2027_navigation import apply as apply_course_navigation
        self.resources.update(apply_course_navigation(doc,self.page,self.output_root,self.runtime,'d0'))
        from zo_course_html import write
        write(self.page, doc)
        return {'source':str(PACKAGE/'index.qmd'),'source_sha256':sha(REPO/PACKAGE/'index.qmd'),'source_inventory':original,'source_markup':markup,'reading_beats':beats,'resources':self.resources,'links':self.links,'site_footer':footer_info,'layout_sha256':sha(LAYOUT),'html_sha256':sha(self.page),'acceptance':'pending_owner_review','publication':'pending'}

def adapt(path,output_root):
    from zo_math_notation import require_runtime_css
    require_runtime_css(KIT / 'web-shell.css')
    doc=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
    if MARKER not in doc.body.get('class',[]):raise ValueError('D0 opt-in marker missing; refuse rollback')
    if doc.body.get('data-zo-web-production')=='d0':return False
    report=D0Builder(path,output_root).build_current()
    destination=os.environ.get('ZO_WEB_2027_D0_REPORT')
    if destination:
        target=Path(destination).resolve()
        if not target.is_relative_to(REPO/'_audit'):raise ValueError('D0 evidence must stay in audit')
        target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('D0 canonical adapter:',path)
    return True

"""Edition gateway using the shared 2027 shell, not duplicate course Home."""
import html
from bs4 import BeautifulSoup
from zo_web_2027_home import HomeBuilder
from zo_web_2027_preview import template,BRAND_THOUGHT
def adapt(path,output_root):
    raw=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
    if 'zo-web-2027-gateway' not in raw.body.get('class',[]):raise ValueError('Gateway opt-in missing')
    if raw.body.get('data-zo-web-production'):return False
    builder=HomeBuilder(path,output_root);builder.runtime=output_root/'assets/zo_web_2027/gateway';builder.common_assets()
    source=raw.select_one('.zo-on-thi-gateway')
    if not source:raise ValueError('Gateway content missing')
    builder.normalize_links(source,path)
    source['class']=['reader-content'];source['id']='gateway-content'
    paper=raw.new_tag('section',attrs={'class':'reading-region'})
    title=raw.new_tag('h1');title.string='Ôn thi Toán THPT';paper.append(title)
    for node in list(source.contents):paper.append(node.extract())
    source.append(paper)
    home=builder.href(output_root/'content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.html')
    footer,_=builder.site_footer()
    styles='\n'.join('<link rel="stylesheet" href="'+builder.runtime_hrefs[n]+'">' for n in ['reading-regions.css','web-shell.css','course-home.css','appearance-inline.css'])
    from zo_web_2027_preview import KIT
    builder.materialize(KIT/'site-footer.css','site-footer.css');styles+='\n<link rel="stylesheet" href="'+builder.runtime_hrefs['site-footer.css']+'">'
    page=template('page.html',title='Ôn thi Toán THPT',body_class='course-home-preview zo-web-2027-gateway',home_href=home,
        appearance=builder.appearance(),brand_thought=html.escape(BRAND_THOUGHT),navigation='<nav aria-label="Ấn bản"><p><a href="#gateway-content">Ấn bản hiện có</a></p><p><a href="'+home+'">Khóa 2027</a></p></nav>',
        breadcrumb='Các ấn bản',hero='',content=str(source),support='',site_footer=footer,drawer_title='Các ấn bản',styles=styles,scripts='<script src="'+builder.runtime_hrefs['site-ui.js']+'"></script>')
    doc=BeautifulSoup(page,'html.parser')
    for node in doc.select('img[src],link[href]'):
        key='src' if node.name=='img' else 'href'
        if node[key].startswith('assets/logos/'):
            node[key]=builder.runtime_hrefs[node[key]]
    doc.body['data-zo-web-production']='course-gateway'
    doc.select_one('.lab-link').string='ZO Math'
    rail=doc.select_one('.rail-support');rail['href']=home;rail.string='Khóa 2027 ↗'
    trigger=doc.select_one('.mobile-trigger');trigger['aria-label']='Mở mục lục các ấn bản';trigger.select_one('.mobile-view').decompose()
    from zo_course_html import write
    write(path,doc);return True

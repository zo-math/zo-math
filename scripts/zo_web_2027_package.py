"""Metadata-owned package adapter using the current shared course shell. No PDF production."""
from pathlib import Path
from urllib.parse import urlsplit,unquote,urlunsplit
import copy,html,json,os,xml.etree.ElementTree as ET
from bs4 import BeautifulSoup,Tag
from zo_web_2027_home import HomeBuilder
from zo_web_2027_preview import PreviewBuilder,REPO,KIT,BRAND_THOUGHT,template
from zo_web_2027_g02 import canonical_math_matches,inv

ROLES={'bat-dau':'Bắt đầu','bai-hoc':'Bài học','phieu-luyen':'Luyện tập','tu-kiem-tra':'Kiểm tra','on-lai':'Ôn lại','on-nen':'Ôn nền','sua-loi':'Sửa lỗi','nhat-ky':'Nhật kí','loi-giai':'Lời giải','nguon':'Nguồn'}
class Builder(HomeBuilder):
 def __init__(self,output_root,key):
  super().__init__(output_root/f'assets/zo_web_2027/{key}/index.html',output_root);self.runtime=self.output
 def common_assets(self):PreviewBuilder.common_assets(self)

def adapt(path,output_root,package):
 PACKAGE=Path(package);settings=json.loads((REPO/PACKAGE/'giao_dien/html.json').read_text(encoding='utf-8'));key=settings['runtime']
 if settings.get('schema_version')!=1 or settings.get('package')!=PACKAGE.name:raise ValueError('Invalid package shell binding')
 from zo_course_labels import source_checks,require,apply as apply_labels
 require(source_checks(REPO/PACKAGE/'index.qmd'),'G05 source labels')
 original=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
 if original.body is None:return False
 if original.body.has_attr('data-zo-web-production'):return False
 if settings['opt_in'] not in original.body.get('class',[]):raise ValueError('Missing G05 opt-in')
 root=copy.deepcopy(original.select_one('.zo-on-thi-package'))
 if root is None:raise ValueError('Missing canonical reader')
 if not canonical_math_matches(REPO/PACKAGE/'index.qmd',root):raise ValueError('Fresh G05 mathematics differ from QMD')
 baseline=inv(root);binding=json.loads((REPO/PACKAGE/'giao_dien/he_nhan.json').read_text(encoding='utf-8'))
 for unit in binding['units']:
  question=root.find(id=unit['question'])
  if question is None or question.get('data-zo-function')!=unit['function']:raise ValueError('Missing task function '+unit['id'])
  if unit.get('answer'):
   answer=root.find(id=unit['answer'])
   if answer is None:raise ValueError('Missing solution '+unit['id'])
   answer['data-zo-type']='solution';answer['data-zo-function']=unit['function'];answer['data-zo-task']=unit['id']
 for node in root.select('[data-zo-task]'):
  if node.find_parent(attrs={'data-zo-task':node['data-zo-task']}) is not None:
   for key in list(node.attrs):
    if key.startswith('data-zo-'):del node[key]
   node['class']=[c for c in node.get('class',[]) if c!='zo-learning-task']
 for note in list(root.select('div.zo-source-note')):
  children=note.find_all(recursive=False)
  if len(children)!=1 or children[0].name!='p':raise ValueError('Source note must be one complete paragraph')
  paragraph=children[0].extract();paragraph['class']=['zo-source-note'];note.replace_with(paragraph)
 root['class']=list(dict.fromkeys(root.get('class',[])+['reader-content']))
 root['data-r1-lesson-selector']=settings['lesson_selector']
 root['data-r1-review-rounds']=json.dumps(settings.get('review_rounds',[]),ensure_ascii=False)
 root['data-zo-reading-contract']='source-owned'
 for formula in root.select('math:not([display=block])'):
  annotation=formula.select_one('annotation[encoding="application/x-tex"]')
  if annotation and (annotation.get_text().count(';')>=4 or len(annotation.get_text())>100):
   viewport=BeautifulSoup('', 'html.parser').new_tag('span',attrs={'class':'zo-inline-math-scroll','tabindex':'0','role':'region','aria-label':'Dãy số hoặc biểu thức; cuộn ngang khi cần'})
   formula.wrap(viewport)
 doc=BeautifulSoup('','html.parser')
 def wrap(nodes):
  nodes=[n for n in nodes if isinstance(n,Tag)]
  if not nodes:return
  paper=doc.new_tag('div',attrs={'class':'reading-region','data-reading-reason':'Source-owned complete reading unit'})
  nodes[0].insert_before(paper)
  for node in nodes:paper.append(node.extract())
 def regions(section):
  if section.has_attr('data-zo-task'):wrap(list(section.children));return
  pending=[]
  for child in list(section.children):
   if isinstance(child,Tag) and child.name=='section':
    if pending:wrap(pending);pending=[]
    regions(child)
   else:pending.append(child)
  if pending:wrap(pending)
  for paper in list(section.select(':scope > .reading-region')):
   substantive=paper.select('p,li,table,figure,details')
   if substantive and any(n.get_text(' ',strip=True) or n.find('img') for n in substantive):continue
   next_paper=paper.find_next(class_='reading-region')
   if next_paper is not None and section in next_paper.parents:
    for node in reversed(list(paper.contents)):next_paper.insert(0,node.extract())
    paper.decompose()
 for ident in ROLES:
  section=root.find('section',id=ident,recursive=False)
  if section is None:raise ValueError('Missing source area '+ident)
  regions(section)
 if inv(root)!=baseline:raise ValueError('Reading projection changed content, mathematics or IDs')
 builder=Builder(output_root,key);builder.output.mkdir(parents=True,exist_ok=True);builder.common_assets()
 from zo_course_cover import load_cover
 builder.materialize(load_cover(REPO,PACKAGE.name,allow_direction_approved=True),'assets/cover.svg')
 for name in ['r1-g02-adapter.css','site-footer.css','r1-consistency.css']:builder.materialize(KIT/name,name)
 if root.select('img[src]'):raise ValueError('Body illustrations need an explicit role-aware adapter')
 for link in root.select('a[href]'):
  split=urlsplit(link['href'])
  if split.scheme or split.netloc or not split.path:continue
  if split.path.endswith('.qmd'):split=split._replace(path=split.path[:-4]+'.html')
  target=(path.parent/unquote(split.path)).resolve()
  if not target.is_relative_to(output_root):raise ValueError('Link escapes output root')
  link['href']=builder.href(target,split.query,split.fragment)
 for details in root.select('details'):
  details.attrs.pop('open',None);guidance='zo-learning-guidance' in details.get('class',[])
  details['class']=list(dict.fromkeys(details.get('class',[])+(['r1-details','zo-block','zo-block-gray'] if guidance else ['r1-details','r1-solution','zo-learning-solution','solution','zo-block','zo-block-gray'])))
  summary=details.find('summary',recursive=False)
  if summary is None:raise ValueError('Disclosure lacks summary')
  summary['class']=list(dict.fromkeys(summary.get('class',[])+['zo-block-title']))
  body=doc.new_tag('div',attrs={'class':'zo-block-body'})
  for child in list(details.contents):
   if child is not summary:body.append(child.extract())
  details.append(body)
 title=root['data-r1-title'];subtitle=original.select_one('.subtitle').get_text(' ',strip=True)
 home=builder.href(output_root/'content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.html')
 hero='<section class="hero" aria-label="Bìa học liệu"><div class="hero-copy"><span class="eyebrow">'+html.escape(settings['eyebrow'])+'</span><h1>'+html.escape(title)+'</h1><p>'+html.escape(subtitle)+'</p></div><figure class="hero-art"><img src="assets/cover.svg" alt="'+html.escape(settings['cover_alt'],quote=True)+'"></figure></section>'
 footer,_=builder.site_footer();support=template('support.html',support_href=builder.href(output_root/'content/support/donate.html'),prototype_note='Bản HTML chờ duyệt.')
 rendered=template('page.html',title=html.escape(title),body_class='g02-preview zo-web-2027-production',home_href=home,appearance=builder.appearance(),brand_thought=html.escape(BRAND_THOUGHT),navigation='<div id="nav-mount"></div>',breadcrumb=html.escape(title),hero=hero,content=str(root),support=support,site_footer=footer,drawer_title='Các phần của học liệu',styles='\n'.join(f'<link rel="stylesheet" href="{n}">' for n in ['reading-regions.css','web-shell.css','site-footer.css','appearance-inline.css','r1-g02-adapter.css','r1-consistency.css']),scripts='<script src="r1-controller.js"></script><script src="site-ui.js"></script>')
 result=BeautifulSoup(rendered,'html.parser');apply_labels(result,binding,{})
 fallback=result.new_tag('noscript');nav=result.new_tag('nav',attrs={'aria-label':'Các phần của học liệu'})
 for anchor,label in ROLES.items():
  para=result.new_tag('p');a=result.new_tag('a',href='#'+anchor);a.string=label;para.append(a);nav.append(para)
 fallback.append(nav);result.find(id='rail-content').append(fallback)
 for node in result.select('[src],link[href],a[href]'):
  key='src' if node.has_attr('src') else 'href';url=urlsplit(node[key])
  if url.scheme or url.netloc or not url.path:continue
  destination=(builder.output/unquote(url.path)).resolve()
  if not destination.is_relative_to(output_root):raise ValueError('Dependency escapes output root')
  node[key]=urlunsplit(('','',os.path.relpath(destination,path.parent).replace('\\','/'),url.query,url.fragment))
 from zo_course_tables import apply as apply_tables
 apply_tables(result,PACKAGE.name,path,builder.output)
 css=KIT/'figure-profile-candidate/production-figures.css';target=builder.output/css.name
 target.write_bytes(css.read_bytes());result.head.append(result.new_tag('link',rel='stylesheet',href=os.path.relpath(target,path.parent).replace('\\','/')))
 from zo_web_2027_navigation import apply as apply_navigation
 apply_navigation(result,path,output_root,builder.output,PACKAGE.name,preview_entry=(PACKAGE/'index.html',title))
 result.body['data-zo-web-production']=root['data-r1-code'];result.title.string=title+' — ZO Math'
 # Source-owned square cover frame uses shared palette and dimensions.
 from zo_course_cover_frame import apply as apply_cover_frame
 apply_cover_frame(result,settings['cover_frame'],path,builder.output)
 from zo_web_2027_consistency import apply_editorial_policy
 apply_editorial_policy(result)
 from zo_course_html import write
 write(path,result)
 print('Package shell:',len(result.select('.reading-region')),'reading regions;',len(result.select('.zo-pdf-card')),'PDF downloads')
 return True

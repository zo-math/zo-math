"""R01 G01 source-owned HTML projection using the shared shell. No PDF production.
Historical accepted layouts and fingerprints stay immutable.
"""
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

def normalize_source_notes(root):
 """Keep source-note paragraphs and explicit link targets intact."""
 for note in list(root.select('div.zo-source-note')):
  children=note.find_all(recursive=False)
  if not children or any(child.name!='p' for child in children):
   raise ValueError('Source note must contain complete paragraphs')
  if len(children)==1:
   paragraph=children[0].extract()
   paragraph.attrs.update(note.attrs)
   note.replace_with(paragraph)

def apply_support_context(root):
 root['data-r1-support-context']='semantic'
 for ident in ['bắt-đầu-từ-đâu','bai-hoc','cp-lt1','cp-lt2','cp-lt3','cp-kt','cp-on1','cp-on2','cp-on3']:
  target=root.find(id=ident)
  if target is not None:
   heading=target.find(['h2','h3','h4'])
   target['data-r1-return-label']='Khởi động' if ident=='bắt-đầu-từ-đâu' else heading.get_text(' ',strip=True)


def adapt(path,output_root,package):
 PACKAGE=Path(package)
 if PACKAGE.name!='r1_g01':raise ValueError('R01 adapter is G01-only')
 settings=json.loads((REPO/PACKAGE/'giao_dien/html.json').read_text(encoding='utf-8'));key=settings['runtime']
 if settings.get('schema_version')!=1 or settings.get('package')!=PACKAGE.name:raise ValueError('Invalid package shell binding')
 from zo_course_labels import source_checks,require,apply as apply_labels
 require(source_checks(REPO/PACKAGE/'index.qmd'),'G01 R01 source labels')
 original=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
 if original.body is None:return False
 if original.body.has_attr('data-zo-web-production'):return False
 if settings['opt_in'] not in original.body.get('class',[]):raise ValueError('Missing G01 R01 opt-in')
 root=copy.deepcopy(original.select_one('.zo-on-thi-package'))
 if root is None:raise ValueError('Missing canonical reader')
 if not canonical_math_matches(REPO/PACKAGE/'index.qmd',root):raise ValueError('Fresh G01 R01 mathematics differ from QMD')
 baseline=inv(root);binding=json.loads((REPO/PACKAGE/'giao_dien/he_nhan.json').read_text(encoding='utf-8'))
 normalize_source_notes(root)
 root['class']=list(dict.fromkeys(root.get('class',[])+['reader-content']))
 root['data-r1-lesson-selector']=settings['lesson_selector']
 root['data-r1-review-rounds']=json.dumps(settings.get('review_rounds',[]),ensure_ascii=False)
 root['data-zo-reading-contract']='source-owned'
 apply_support_context(root)
 from zo_course_contents import apply_contents
 apply_contents(root,settings)
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
   if isinstance(child,Tag) and 'r1-foundation-unit' in child.get('class',[]):
    if pending:wrap(pending);pending=[]
    wrap([child])
   elif isinstance(child,Tag) and child.name=='section':
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
 if root.find(id='tai-tai-lieu') is not None:regions(root.find(id='tai-tai-lieu'))
 if inv(root)!=baseline:raise ValueError('Reading projection changed content, mathematics or IDs')
 builder=Builder(output_root,key);builder.output.mkdir(parents=True,exist_ok=True);builder.common_assets()
 from zo_course_cover import load_cover
 builder.materialize(load_cover(REPO,PACKAGE.name,allow_direction_approved=True),'assets/cover.svg')
 for name in ['r1-g02-adapter.css','site-footer.css','r1-consistency.css']:builder.materialize(KIT/name,name)
 from zo_web_2027_figures import verify,CONFIG
 verify(json.loads(CONFIG.read_text(encoding='utf-8')))
 from zo_graphics import set_lesson_graph_size
 for img in root.select('img[src]'):
  raw=unquote(urlsplit(img['src']).path)
  src=(REPO/raw.lstrip('/') if raw.startswith('/') else REPO/PACKAGE/raw).resolve()
  if not src.is_relative_to(REPO) or src.is_relative_to(REPO/'_audit') or not src.is_file():raise ValueError('Invalid canonical image '+str(src))
  img['src']=builder.materialize(src,'figures/'+src.name)
  if src.name.startswith('do_thi_'):
   set_lesson_graph_size(img,src,REPO)
   img['class']=list(dict.fromkeys(img.get('class',[])+['zo-graph-04','math-illustration']))
   parent=img.find_parent('figure')
   if parent:
    parent['class']=list(dict.fromkeys(parent.get('class',[])+['math-figure']))
    viewport=doc.new_tag('div',attrs={'class':'figure-viewport zo-figure-scroll'})
    img.wrap(viewport)
 # Package-owned optional media assets travel with the projected reader.
 for asset in root.select('link[rel="stylesheet"][href],script[src]'):
  attribute='src' if asset.name=='script' else 'href'
  raw=urlsplit(asset[attribute])
  src=(REPO/PACKAGE/unquote(raw.path)).resolve()
  expected='.js' if asset.name=='script' else '.css'
  if raw.scheme or raw.netloc or not src.is_relative_to((REPO/PACKAGE/'giao_dien').resolve()) or src.suffix!=expected or not src.is_file():
   raise ValueError('Invalid package reader asset '+asset[attribute])
  asset[attribute]=builder.materialize(src,'reader/'+src.name)
 for link in root.select('a[href]'):
  split=urlsplit(link['href'])
  if split.scheme or split.netloc or not split.path:continue
  if split.path.endswith('.qmd'):split=split._replace(path=split.path[:-4]+'.html')
  target=(path.parent/unquote(split.path)).resolve()
  if not target.is_relative_to(output_root):raise ValueError('Link escapes output root')
  link['href']=builder.href(target,split.query,split.fragment)
 for details in root.select('details'):
  details.attrs.pop('open',None);guidance=bool({'zo-learning-guidance','zo-learning-video'} & set(details.get('class',[])))
  details['class']=list(dict.fromkeys(details.get('class',[])+(['r1-details','zo-block','zo-block-gray'] if guidance else ['r1-details','r1-solution','zo-learning-solution','solution','zo-block','zo-block-gray'])))
  summary=details.find('summary',recursive=False)
  if summary is None:raise ValueError('Disclosure lacks summary')
  summary['class']=list(dict.fromkeys(summary.get('class',[])+['zo-block-title']))
  if details.select_one(':scope > .zo-block-body') is not None:continue
  body=doc.new_tag('div',attrs={'class':'zo-block-body'})
  for child in list(details.contents):
   if child is not summary:body.append(child.extract())
  details.append(body)
 title=root['data-r1-title'];subtitle=original.select_one('.subtitle').get_text(' ',strip=True)
 home=builder.href(output_root/'content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.html')
 hero='<section class="hero" aria-label="Bìa học liệu"><div class="hero-copy"><span class="eyebrow">'+html.escape(settings['eyebrow'])+'</span><h1>'+html.escape(title)+'</h1><p>'+html.escape(subtitle)+'</p></div><figure class="hero-art"><img src="assets/cover.svg" alt="'+html.escape(settings['cover_alt'],quote=True)+'"></figure></section>'
 footer,_=builder.site_footer();support=template('support.html',support_href=builder.href(output_root/'content/support/donate.html'),prototype_note=settings.get('status_note','Bản HTML chờ duyệt.'))
 rendered=template('page.html',title=html.escape(title),body_class='g02-preview zo-web-2027-production',home_href=home,appearance=builder.appearance(),brand_thought=html.escape(BRAND_THOUGHT),navigation='<div id="nav-mount"></div>',breadcrumb=html.escape(title),hero=hero,content=str(root),support=support,site_footer=footer,drawer_title='Các phần của học liệu',styles='\n'.join(f'<link rel="stylesheet" href="{n}">' for n in ['reading-regions.css','web-shell.css','site-footer.css','appearance-inline.css','r1-g02-adapter.css','r1-consistency.css']),scripts='<script src="r1-controller.js"></script><script src="site-ui.js"></script>')
 result=BeautifulSoup(rendered,'html.parser')
 for node in result.select('[id="r1-support-title"], [aria-labelledby="r1-support-title"]'):
  if node.find_parent(class_='reader-content') is None:
   if node.get('id')=='r1-support-title':node['id']='r01-shell-support-title'
   if node.has_attr('aria-labelledby'):node['aria-labelledby']='r01-shell-support-title'
 from zo_r1_g01_labels import apply as apply_g01_labels,remove_redundant_labels
 apply_g01_labels(result);remove_redundant_labels(result)
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
 # Project literal BBT data through the established HTML-only variation engine.
 from zo_web_2027_figures import module,VARIATION,CONFIG
 config=json.loads(CONFIG.read_text(encoding='utf-8'))
 variation=module('g01_revision_variation',VARIATION/'zo_variation_html.py')
 records=variation.load_data(REPO/PACKAGE/config['variation_source'])
 fragments=variation.math_fragments(records)
 tables={table['data-bbt']:table for table in result.select('table.variation[data-bbt]')}
 if set(tables)!={r['id'] for r in records}:raise ValueError('G01 source BBT coverage differs')
 for record in records:
  original=tables[record['id']]
  rows=[[cell.get_text(' ',strip=True) for cell in row.find_all(['th','td'],recursive=False)] for row in original.select('tr')]
  expected=copy.deepcopy(record['rows'])
  for row in expected[1:]:
   for col in record.get('excluded_columns',[]):row[col]='∥'
  if rows!=expected:raise ValueError('G01 source BBT data differs: '+record['id'])
  native=BeautifulSoup(variation.render_record(record,fragments),'html.parser').select_one('table')
  native.caption.string=original.caption.get_text(' ',strip=True)
  hidden=original.find_parent(class_='visually-hidden')
  viewport=result.new_tag('div',attrs={'class':'figure-viewport zo-figure-scroll'})
  hidden.replace_with(viewport);viewport.append(native)
 from zo_course_tables import apply as apply_tables
 apply_tables(result,PACKAGE.name,path,builder.output)
 css=KIT/'figure-profile-candidate/production-figures.css';target=builder.output/css.name
 target.write_bytes(css.read_bytes());result.head.append(result.new_tag('link',rel='stylesheet',href=os.path.relpath(target,path.parent).replace('\\','/')))
 from zo_web_2027_navigation import apply as apply_navigation, PAGES
 apply_navigation(result,path,output_root,builder.output,PACKAGE.name,preview_entry=None if PACKAGE.name in PAGES else (PACKAGE/'index.html',title))
 result.body['data-zo-web-production']=root['data-r1-code'];result.title.string=title+' — ZO Math'
 # Source-owned square cover frame uses shared palette and dimensions.
 from zo_course_cover_frame import apply as apply_cover_frame
 apply_cover_frame(result,settings['cover_frame'],path,builder.output)
 from zo_web_2027_consistency import apply_editorial_policy
 apply_editorial_policy(result)
 # Optional package-owned reader refinement, loaded after the shared controller.
 enhancement=settings.get('reader_enhancement',{})
 for kind,relative in enhancement.items():
  if kind not in {'style','script'}:raise ValueError('Unknown reader enhancement')
  source=(REPO/PACKAGE/relative).resolve()
  if not source.is_relative_to((REPO/PACKAGE/'giao_dien').resolve()) or not source.is_file():raise ValueError('Reader enhancement escapes package interface')
  if source.suffix!=('.css' if kind=='style' else '.js'):raise ValueError('Reader enhancement type mismatch')
  asset=builder.materialize(source,'reader'+source.suffix)
  href=os.path.relpath(builder.output/asset,path.parent).replace('\\','/')
  if kind=='style':result.head.append(result.new_tag('link',rel='stylesheet',href=href))
  else:result.body.append(result.new_tag('script',src=href))
 # Render downloads only when the package declares its complete PDF set.
 import yaml
 metadata=yaml.safe_load((REPO/PACKAGE/'index.qmd').read_text(encoding='utf-8').split('---',2)[1])
 if metadata.get('r1-download-files'):
  from zo_web_2027_downloads import apply as apply_downloads
  apply_downloads(result,path,output_root)
  from zo_course_pdf_download_state import apply as apply_pdf_state
  apply_pdf_state(result,REPO,PACKAGE)
  from zo_course_labels import apply_context_labels
  apply_context_labels(result,binding)
  result.select_one('#tai-tai-lieu .zo-pdf-current-note').string='Các PDF đang giữ bản cũ, chưa phản ánh bản sửa R01. Chỉ xem và góp ý HTML trong 10 đợt sửa; PDF sẽ được xây dựng sau khi toàn bộ kết quả đạt yêu cầu.'
 from zo_course_html import write
 write(path,result)
 print('Package shell:',len(result.select('.reading-region')),'reading regions;',len(result.select('.zo-pdf-card')),'PDF downloads')
 return True

def refresh_support_context():
 """Bounded HTML attribute refresh from the same source projection as adapt."""
 from zo_course_labels import require,source_checks
 source=REPO/'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.qmd'
 require(source_checks(source),'R01 source')
 path=REPO/'docs'/source.relative_to(REPO).with_suffix('.html')
 before=path.read_text(encoding='utf-8');doc=BeautifulSoup(before,'html.parser')
 root=doc.select_one('.reader-content')
 if doc.body.get('data-zo-web-production')!='R1-G01':raise ValueError('Only current G01 HTML may be refreshed')
 nodes=[root]+[root.find(id=i) for i in ['bắt-đầu-từ-đâu','bai-hoc','cp-lt1','cp-lt2','cp-lt3','cp-kt','cp-on1','cp-on2','cp-on3']]
 old=[str(node).split('>',1)[0]+'>' for node in nodes]
 apply_support_context(root)
 new=[str(node).split('>',1)[0]+'>' for node in nodes]
 after=before
 for a,b in zip(old,new,strict=True):
  if after.count(a)!=1:raise ValueError('Ambiguous support-context owner')
  after=after.replace(a,b,1)
 restored=after
 for a,b in zip(old,new,strict=True):restored=restored.replace(b,a,1)
 if restored!=before:raise ValueError('Unbounded support refresh')
 path.write_text(after,encoding='utf-8',newline='\n')
 import hashlib
 record={'operation':'support labels from canonical adapter','owners':len(nodes),'outside_attributes_unchanged':True,'HTML_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'PDF_built':False}
 (REPO/'_audit/r1_g01_revision_20261031/support_refresh.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(record)

if __name__=='__main__':
 import sys
 if sys.argv[1:]!=['refresh-support']:raise SystemExit('Use refresh-support')
 refresh_support_context()

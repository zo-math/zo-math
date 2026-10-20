"""G05 source/HTML invariants and regression guards; never renders or edits outputs."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import argparse,copy,hashlib,json,re,shutil,sys,tempfile
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
PACKAGE=Path('content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g05')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(page):
 from zo_course_labels import binding,source_checks,html_checks,expand
 from zo_course_scenes import source_checks as scenes,html_checks as scene_html
 from zo_course_cover import check_html as cover_html
 from zo_web_2027_consistency import presentation_checks
 from zo_web_2027_g02 import canonical_math_matches
 source=ROOT/PACKAGE/'index.qmd';data=binding(source);doc=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser');root=doc.select_one('.reader-content');checks={}
 checks.update({'labels/source/'+k:v for k,v in source_checks(source).items()});checks.update({'labels/HTML/'+k:v for k,v in html_checks(doc,data).items()})
 checks.update({'scenes/source/'+k:v for k,v in scenes(source).items()});checks.update({'scenes/HTML/'+k:v for k,v in scene_html(doc,source,page).items()});checks.update({'presentation/'+k:v for k,v in presentation_checks(doc,data).items()})
 checks['fresh mathematics match QMD/includes']=canonical_math_matches(source,root)
 from zo_math_notation import display_css_errors
 runtime_css=next((page.parent/unquote(urlsplit(n['href']).path)).resolve() for n in doc.select('link[rel=stylesheet][href]') if Path(urlsplit(n['href']).path).name=='reading-regions.css')
 css=runtime_css.read_text(encoding='utf-8')
 checks['rendered CSS retains native centered display mathematics']=not display_css_errors(css)
 notes=root.select('p.zo-source-note')
 checks['seven complete local source paragraphs']=len(notes)==7 and all(n.find_parent(id='bai-hoc') for n in notes)
 checks['source paragraph typography comes from shared component']='.zo-source-note{display:block;font-size:12px;line-height:1.7;color:var(--muted);' in css
 checks['regression left aligned block MathML rejected']=bool(display_css_errors(css.replace('display:block math','display:block')))
 checks['regression missing display MathML rule rejected']=bool(display_css_errors(''))
 checks['regression display scroll removed rejected']=bool(display_css_errors(css.replace('overflow-x:auto','overflow-x:visible')))
 bad=copy.deepcopy(doc);first=bad.select_one('.zo-source-note');first.name='a';first['class']=['footnote-ref'];first.string='1'
 checks['regression bare footnote marker rejected']=not all(presentation_checks(bad,data).values())
 bad=copy.deepcopy(doc);bad.select_one('.zo-source-note').string='SGK Toán 12 KNTT, tr.38–40.'
 checks['regression abbreviated source note rejected']=not all(presentation_checks(bad,data).values())

 checks['cover direction rendered correctly']=cover_html(ROOT,'r1_g05',page,allow_direction_approved=True)
 expected=int(root.get('data-r1-lesson-count','0'));lesson=root.find(id='bai-hoc')
 checks['lesson TOC mount and real entry count']=bool(lesson.select_one('.lesson-toc')) and len(lesson.select(':scope > section.level3'))==expected==7
 checks['29 questions and solutions']=len([u for u in data['units'] if u.get('answer')])==29
 checks['eight semantic caller/return checkpoints']={x.get('id') for x in root.select('section[data-zo-type=checkpoint][data-r1-return-label]')}=={f'cp-{i:02d}' for i in range(1,9)}
 checks['five body illustrations']=len(root.select('.figure-viewport img'))==5
 from zo_course_pdf_download_state import apply as pdf_state
 from zo_web_2027_downloads import download_region_coverage
 from zo_pdf_contract import validate_canonical_pdf_provenance
 from pypdf import PdfReader
 import yaml
 cfg=yaml.safe_load((source.parent/'_quy_trinh/cau_hinh_san_xuat_qmd.yml').read_text('utf-8'))
 variants=cfg['extensions']['pdf_variants'];cards=root.select('#tai-tai-lieu .zo-pdf-card')
 metadata=yaml.safe_load(source.read_text('utf-8').split('---',2)[1])
 from zo_web_2027_g05 import ROLES
 from zo_course_pdf_layout import pdf_id
 answer_ids={pdf_id(u['answer']) for u in data['units'] if u.get('answer')}
 checks['eight registered current PDF downloads']=len(cards)==len(variants)==8 and all(pdf_state(copy.deepcopy(doc),ROOT,PACKAGE))
 checks['all visible PDF labels report current']=all(c.get('data-pdf-current')=='true' and c.select_one('.zo-pdf-version-note').get_text(strip=True)=='PDF đã cập nhật.' for c in cards)
 checks['download cards use shared reading region']=download_region_coverage(root.find(id='tai-tai-lieu'))
 for variant,definition in variants.items():
  pdf=source.parent/definition['output'];card=next((c for c in cards if c.select_one('a[download]')['href']==definition['output']),None)
  checks['PDF current/'+variant]=not validate_canonical_pdf_provenance(ROOT,source,variant=variant)
  names=set(PdfReader(pdf).named_destinations)
  part=next((v for v in metadata['r1-section-download-files'] if v['variant']==variant),None)
  expected=set(ROLES) if variant=='full' else set(ROLES)-{'loi-giai'} if variant=='student' else {'bat-dau','nguon',part['start']}
  checks['PDF functional section scope/'+variant]=names.intersection(ROLES)==expected
  checks['PDF solution inclusion/exclusion/'+variant]=names.intersection(answer_ids)==(answer_ids if variant in {'full','loi_giai'} else set())
  checks['PDF pages and copied bytes/'+variant]=card is not None and int(card.select_one('[data-pdf-pages]')['data-pdf-pages'])==len(PdfReader(pdf).pages) and sha(pdf)==sha(page.parent/definition['output'])
 bad=copy.deepcopy(doc);bad.select_one('.zo-pdf-card').decompose()
 try:pdf_state(bad,ROOT,PACKAGE);rejected=False
 except ValueError:rejected=True
 checks['regression missing PDF card rejected']=rejected
 from unittest.mock import patch
 bad=copy.deepcopy(doc)
 with patch('zo_course_pdf_download_state.validate_canonical_pdf_provenance',return_value=['Stale input fixture']):
  states=pdf_state(bad,ROOT,PACKAGE)
 checks['regression stale PDFs cannot receive current label']=not any(states) and all(c.get('data-pdf-current')=='false' and c.select_one('.zo-pdf-version-note').get_text(strip=True)=='PDF đang chờ cập nhật.' for c in bad.select('.zo-pdf-card'))
 broken=[];cache={page:doc}
 for node in doc.select('a[href],img[src],script[src],link[href]'):
  raw=node.get('src',node.get('href'));url=urlsplit(raw)
  if url.scheme or url.netloc:continue
  target=(page.parent/unquote(url.path)).resolve() if url.path else page
  if not target.is_file():broken.append(raw);continue
  if url.fragment and target.suffix=='.html':
   if target not in cache:cache[target]=BeautifulSoup(target.read_text(encoding='utf-8'),'html.parser')
   if not cache[target].find(id=unquote(url.fragment)):broken.append(raw)
 checks['all local files/anchors exist']=not broken
 for u in data['units']:
  if not u.get('answer'):continue
  q=root.find(id=u['question']);a=root.find(id=u['answer']);fwd=root.find(id='cp-05') if u['function']=='function.test' else q
  checks[u['id']+' one forward/return action']=len(fwd.select('a[href="#'+u['answer']+'"]'))==1 and len(a.select('a[href="#'+u['question']+'"]'))==1
 # Mutate detached DOM, not output files, to verify real failure modes.
 bad=copy.deepcopy(doc)
 for n in list(bad.select('[data-reading-label]')):n.decompose()
 checks['regression missing visible labels rejected']=not all(html_checks(bad,data).values())
 bad=copy.deepcopy(doc);bad.select_one('.figure-viewport img')['src']='missing.svg'
 checks['regression wrong scene rejected']=not all(scene_html(bad,source,page).values())
 bad=copy.deepcopy(doc);bad.select_one('.figure-viewport img')['style']='--figure-em:1em'
 checks['regression unreadable label scale rejected']=not all(scene_html(bad,source,page).values())
 bad=copy.deepcopy(doc);bad.find(id='on-nen').find('a')['href']='missing.html#missing'
 from zo_course_foundation import html_checks as foundation_html
 checks['regression broken shared support link rejected']=not all(foundation_html(bad.select_one('.reader-content'),data).values())
 # Canonical provenance guard, exercised on disposable fixtures.
 with tempfile.TemporaryDirectory(prefix='g05_scene_gate_',dir=ROOT/'.quarto') as tmp:
  fixture=Path(tmp)
  for folder in ['giao_dien','du_lieu','hinh','_quy_trinh']:(fixture/folder).mkdir()
  for rel in ['index.qmd','giao_dien/minh_hoa_manifest.json','du_lieu/minh_hoa.json','_quy_trinh/sinh_hinh.py']:
   shutil.copyfile(source.parent/rel,fixture/rel)
  for path in (source.parent/'hinh').glob('*'):shutil.copyfile(path,fixture/'hinh'/path.name)
  fs=fixture/'index.qmd';checks['regression scene fixture accepted']=all(scenes(fs).values())
  for name,rel in [('generator','_quy_trinh/sinh_hinh.py'),('data','du_lieu/minh_hoa.json'),('SVG','hinh/quay_ban_hang.svg')]:
   path=fixture/rel;original=path.read_bytes();path.write_bytes(original+b' ')
   checks['regression stale '+name+' rejected']=not all(scenes(fs).values());path.write_bytes(original)
 return {'checks':checks,'passed':sum(checks.values()),'total':len(checks),'failures':[k for k,v in checks.items() if not v],'broken_links':broken,'html_sha256':sha(page),'source_sha256':sha(source),'math_count':len(root.select('math')),'tables':len(root.select('table')),'reading_regions':len(root.select('.reading-region')),'owner_acceptance':'pending','PDF_built':True,'published':False}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--html',type=Path,default=ROOT/'docs'/PACKAGE/'index.html');ap.add_argument('--report',type=Path);a=ap.parse_args();result=run(a.html.resolve())
 if a.report:a.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:result[k] for k in ['passed','total','failures','broken_links','math_count','tables','reading_regions']},ensure_ascii=False));raise SystemExit(bool(result['failures']))

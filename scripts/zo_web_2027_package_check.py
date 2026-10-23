"""Source/HTML checks for metadata-owned course packages; no render or PDF."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import argparse,copy,hashlib,json,re,sys,xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
def run(page):
 from zo_course_labels import binding,source_checks,html_checks,require
 from zo_course_cover import check_html
 from zo_web_2027_consistency import presentation_checks
 from zo_web_2027_g02 import canonical_math_matches
 from zo_course_tables import native_records
 from zo_course_table_roles import source_checks as table_source,html_checks as table_html
 from zo_course_remediation import source_checks as remediation_source,html_checks as remediation_html
 from zo_web_2027_shell import checks as shell_checks
 source=ROOT/page.relative_to(ROOT/'docs').with_suffix('.qmd');data=binding(source)
 doc=BeautifulSoup(page.read_text('utf-8'),'html.parser');reader=doc.select_one('.reader-content');checks={}
 for prefix,result in [('labels/source',source_checks(source)),('labels/html',html_checks(doc,data)),('presentation',presentation_checks(doc,data)),('tables/source',table_source(source)),('tables/html',table_html(doc)),('remediation/source',remediation_source(source)),('remediation/html',remediation_html(doc)),('shell',shell_checks(doc))]:
  checks.update({prefix+'/'+k:bool(v) for k,v in result.items()})
 checks['fresh native math matches QMD/includes']=canonical_math_matches(source,reader)
 checks['cover bytes match approved direction']=check_html(ROOT,source.parent.name,page,allow_direction_approved=True)
 checks['no PDFs or downloads promised']=not reader.select('.zo-pdf-card,#tai-tai-lieu') and not any(not urlsplit(a['href']).scheme and urlsplit(a['href']).path.endswith('.pdf') for a in reader.select('a[href]'))
 checks['27 closed solutions']=len(reader.select('details.zo-learning-solution'))==27 and not reader.select('details.zo-learning-solution[open]')
 checks['all 27 task pairs retained']=len([u for u in data['units'] if u.get('answer')])==27
 checks['five lesson headings']=len(reader.select('#bai-hoc > section[data-zo-lesson]'))==5
 checks['three separate review targets']=len(reader.select('#on-lai [data-zo-context^="round:"]'))==3
 checks['source note paragraphs retained']=len(reader.select('p.zo-source-note'))==10
 checks['long data sequences locally scrollable']=len(reader.select('.zo-inline-math-scroll math'))>=4
 checks['no invented variation data']=native_records(source.parent.name)=={} and not (source.parent/'du_lieu/bang_bien_thien.json').exists()
 checks['native data tables classified']=all(t.get('data-table-kind') for t in reader.select('table'))
 ids=[n['id'] for n in doc.select('[id]')];checks['unique HTML IDs']=len(ids)==len(set(ids))
 broken=[];cache={page:doc}
 for n in doc.select('a[href],img[src],script[src],link[href]'):
  raw=n.get('src',n.get('href'));u=urlsplit(raw)
  if u.scheme or u.netloc:continue
  target=(page.parent/unquote(u.path)).resolve() if u.path else page
  if not target.is_file():broken.append(raw);continue
  if u.fragment and target.suffix=='.html':
   if target not in cache:cache[target]=BeautifulSoup(target.read_text('utf-8'),'html.parser')
   if not cache[target].find(id=unquote(u.fragment)):broken.append(raw)
 checks['all files and anchors exist']=not broken
 for u in data['units']:
  if not u.get('answer'):continue
  q=reader.find(id=u['question']);a=reader.find(id=u['answer'])
  checks[u['id']+'/paired forward and return']=len(q.select('a[href="#'+u['answer']+'"]'))==1 and len(a.select('a[href="#'+u['question']+'"]'))==1
 # Real negative cases for the generic summary/label and source-owned wording fixes.
 bad=copy.deepcopy(doc);bad.find(id='giai01').select_one('[data-reading-label]').decompose()
 checks['reject missing summary context label']=not all(html_checks(bad,data).values())
 bad=copy.deepcopy(doc);bad.select_one('.zo-source-note').string='SGK, tr.1.'
 checks['reject abbreviated or undeclared source note']=not all(presentation_checks(bad,data).values())
 from zo_course_numbering import retired_self_check_absent
 bad=copy.deepcopy(reader);heading=BeautifulSoup('<h4>Tự kiểm tra 01</h4>','html.parser').h4;bad.append(heading)
 checks['reject retired activity title']=not retired_self_check_absent(bad,data)
 checks['retain descriptive phrase in approved task title']=retired_self_check_absent(reader,data)
 bad=copy.deepcopy(doc);bad.find(id='gm01').clear()
 try:result=all(presentation_checks(bad,data).values())
 except (ValueError,AttributeError):result=False
 checks['reject missing guided prompt']=not result
 manifest=json.loads((source.parent/'giao_dien/bia_manifest.json').read_text('utf-8'))
 sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 checks['cover generator provenance current']=sha(source.parent/manifest['generator'])==manifest['generator_sha256']
 checks['cover data provenance current']=sha(source.parent/manifest['data'])==manifest['data_sha256']
 vector=ET.parse(source.parent/manifest['svg']['path']).getroot()
 checks['cover shows sixteen dots']=len(vector.findall('{http://www.w3.org/2000/svg}circle'))==16
 checks['cover has four correct groups']=[int(n.get('data-frequency')) for n in vector.findall('{http://www.w3.org/2000/svg}rect')]==[4,3,5,4]
 checks['cover PNG/SVG bytes current']=all(sha(source.parent/manifest[k]['path'])==manifest[k]['sha256'] for k in ['svg','png'])
 return {'package':data['package'],'passed':sum(checks.values()),'total':len(checks),'failures':[k for k,v in checks.items() if not v],'checks':checks,'broken_links':broken,'math_count':len(reader.select('math')),'tables':len(reader.select('table')),'reading_regions':len(reader.select('.reading-region')),'html_sha256':sha(page),'source_sha256':sha(source),'owner_acceptance':'pending','PDF_built':False,'published':False}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--html',type=Path,required=True);ap.add_argument('--report',type=Path);a=ap.parse_args();result=run(a.html.resolve())
 if a.report:a.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
 print(json.dumps({k:result[k] for k in ['passed','total','failures','broken_links','math_count','tables','reading_regions']},ensure_ascii=False));raise SystemExit(bool(result['failures']))

"""G02 R01 source, feedback, mathematical ownership and PDF identity checks."""
from pathlib import Path
import copy,json,hashlib
from bs4 import BeautifulSoup
from pypdf import PdfReader
from zo_course_editorial import source_checks as editorial
from zo_course_learning_goals import source_checks as goals
from zo_course_tables import bind,native_records
from zo_course_labels import answer_action_html_checks,binding
ROOT=Path(__file__).resolve().parents[1]
PACKAGE=ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02'
def main():
 source=PACKAGE/'index.qmd';path=ROOT/'docs'/source.relative_to(ROOT).with_suffix('.html');doc=BeautifulSoup(path.read_text('utf-8'),'html.parser');checks={}
 def check(name,value):checks[name]=bool(value)
 check('G02 projection declared',doc.body.get('data-zo-web-production')=='R1-G02')
 check('reviewed current source',all(editorial(source).values()) and all(goals(source).values()))
 check('unreviewed source rejected',not all(editorial(source,text=source.read_text('utf-8')+'\nUnreviewed change.\n').values()))
 for i in (1,2,3):
  q=doc.find(id=f'o0{i}');a=doc.find(id=f'loi-giai-on-lai-0{i}');cp=doc.find(id=f'cp-on{i}')
  check(f'O{i} no advance criteria or conclusions',q and cp and not any(s in (q.get_text(' ',strip=True)+cp.get_text(' ',strip=True)) for s in ['Lỗi cần quan sát','Đạt khi','Không có giá trị nhỏ nhất','chọn tốc độ thay']))
  check(f'O{i} closed feedback retains criteria',a and a.name=='details' and not a.has_attr('open') and 'Đạt khi' in a.get_text() and 'Lỗi cần quan sát' in a.get_text())
 cards=doc.select('#on-nen .r1-foundation-unit');check('nine foundation cards',len(cards)==9)
 check('nine independently framed cards',len({id(c.find_parent(class_='reading-region')) for c in cards})==9)
 for c in cards:
  check(c['id']+' partial then independent', 'Làm tiếp một bước.' in c.get_text() and bool(c.select('details.zo-learning-guidance')) and bool(c.select('[data-zo-type="task"]')))
  check(c['id']+' feedback closed',not any(d.has_attr('open') for d in c.select('details')))
 for c in doc.select('.r1-foundation-confirmation[data-zo-owner]'):
  check(c['id']+' owned by called card',bool(c.find_parent(id=c['data-zo-owner'])))
 check('two owned confirmations',len(doc.select('.r1-foundation-confirmation[data-zo-owner]'))==2)
 journal=doc.find(id='nhat-ky');check('short journal default','Bốn ý đủ dùng' in journal.get_text())
 for ident in ['r1-table-t13','r1-table-t18']:
  table=doc.find(id=ident);check(ident+' full schema optional',table and len(table.select('tr'))==15 and table.find_parent('details') and not table.find_parent('details').has_attr('open'))
 units=binding(source)['units'];numbers=sorted(set(u['number'] for u in units if 'number' in u))
 check('59 numbered tasks retained',numbers==list(range(1,60)))
 check('all bound questions and answers exist',all(doc.find(id=u['question']) and doc.find(id=u['answer']) for u in units))
 records=native_records('r1_g02');check('all canonical BBTs owned',len(records)>0 and len(doc.select('table.zo-variation-native'))==len(records));bind(doc,'r1_g02')
 bad=copy.deepcopy(doc);bad.select_one('table.zo-variation-native [data-source-value]')['data-source-value']='INVALID'
 try:bind(bad,'r1_g02');rejected=False
 except ValueError:rejected=True
 check('changed mathematical cell rejected',rejected)
 imgs=doc.select('.reader-content img.math-illustration');check('four canonical graphs retained',len(imgs)==4)
 check('motion taught before independent review',bool(doc.select_one('#bai-hoc #g02-toc-do')) and bool(doc.select_one('#nen-n-mh-01-xn01')) and 't^2-6t' in doc.find(id='nen-n-mh-01').decode())
 ids=[n['id'] for n in doc.select('[id]')];check('unique DOM ids',len(ids)==len(set(ids)));check('internal links resolve',all(a['href'][1:] in ids for a in doc.select('a[href^="#"]') if len(a['href'])>1))
 check('canonical answer actions',all(answer_action_html_checks(doc,binding(source)).values()))
 pdfs=doc.select('.zo-pdf-card');check('eight old PDFs disclosed',len(pdfs)==8 and all(c.get('data-pdf-current')=='false' for c in pdfs) and 'Các PDF đang giữ bản cũ' in doc.get_text())
 for c in pdfs:
  filename=c.select_one('a[download]')['href'];actual=len(PdfReader(PACKAGE/filename).pages);check(filename+' G02 page count',int(c.select_one('[data-pdf-pages]')['data-pdf-pages'])==actual)
 check('independent preview identity','BẢN THẢO ĐỘC LẬP' in doc.get_text())
 data={'passed':all(checks.values()),'checks':checks,'owner_acceptance':False,'PDF_built':False};report=ROOT/'_audit/r1_g02_revision_20261102/regressions.json';report.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'passed':data['passed'],'checks':len(checks),'failed':[k for k,v in checks.items() if not v]},ensure_ascii=False));return 0 if data['passed'] else 1
if __name__=='__main__':raise SystemExit(main())

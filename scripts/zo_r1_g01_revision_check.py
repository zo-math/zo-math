"""Focused R01 regressions: retrieval cues, source freshness and mathematical ownership."""
from pathlib import Path
import copy,json,re
from bs4 import BeautifulSoup
from zo_course_editorial import source_checks as editorial,closure
from zo_course_learning_goals import source_checks as goals
from zo_course_tables import bind,native_records
from zo_course_labels import answer_action_html_checks,binding
ROOT=Path(__file__).resolve().parents[1]
PACKAGE=ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01'
def main():
    source=PACKAGE/'index.qmd'
    html=ROOT/'docs'/source.relative_to(ROOT).with_suffix('.html')
    doc=BeautifulSoup(html.read_text('utf-8'),'html.parser')
    checks={}
    def check(name,value):checks[name]=bool(value)
    check('G01 projection declared',doc.body.get('data-zo-web-production')=='R1-G01')
    check('current reviewed source',all(editorial(source).values()) and all(goals(source).values()))
    changed=source.read_text('utf-8')+'\nUnreviewed change.\n'
    check('unreviewed source rejected',not all(editorial(source,text=changed).values()) and not all(goals(source,text=changed).values()))
    for number in (1,2,3):
        question=doc.find(id=f'g01-o0{number}');answer=doc.find(id=f'lg-g01-o0{number}')
        check(f'O{number} no advance criteria or routes',question and not any(x in question.get_text(' ',strip=True) for x in ['Tiêu chí đạt','Tuyến sau bài','Lỗi cần quan sát']))
        check(f'O{number} closed feedback retains criteria and routes',answer and answer.name=='details' and not answer.has_attr('open') and all(x in answer.get_text(' ',strip=True) for x in ['Tiêu chí đạt','Tuyến sau bài']))
    cards=doc.select('#on-nen .r1-foundation-unit')
    check('seven supported foundation skills',len(cards)==7)
    papers=[card.find_parent(class_='reading-region') for card in cards]
    check('independent foundation papers',len({id(p) for p in papers if p})==7)
    for card in cards:
        check(card['id']+' guided attempt before independent task','Làm tiếp một bước.' in card.get_text() and bool(card.select('details.zo-learning-guidance')) and bool(card.select('[data-zo-type="task"]')))
        check(card['id']+' feedback initially closed',not any(d.has_attr('open') for d in card.select('details')))
    journal=doc.find(id='nhat-ky')
    check('short journal default',journal and 'Bốn ý đủ dùng' in journal.get_text())
    for ident in ['r1-table-t13','r1-table-t18']:
        table=doc.find(id=ident)
        check(ident+' optional full schema retained',table and len(table.select('tr'))==15 and table.find_parent('details') and not table.find_parent('details').has_attr('open'))
    records=native_records('r1_g01')
    check('fourteen owned BBTs',len(records)==14 and len(doc.select('table.zo-variation-native'))==14)
    bind(doc,'r1_g01')
    corrupted=copy.deepcopy(doc)
    cell=corrupted.select_one('table.zo-variation-native [data-source-value]')
    cell['data-source-value']='INVALID'
    try:bind(corrupted,'r1_g01');rejected=False
    except ValueError:rejected=True
    check('altered mathematical cell rejected',rejected)
    ids=[n['id'] for n in doc.select('[id]')]
    check('no duplicate DOM ids',len(ids)==len(set(ids)))
    check('all internal links resolve',all(link['href'][1:] in ids for link in doc.select('a[href^="#"]') if len(link['href'])>1))
    check('answer actions retain canonical wording',all(answer_action_html_checks(doc,binding(source)).values()))
    check('PDFs explicitly old',all(c.get('data-pdf-current')=='false' for c in doc.select('.zo-pdf-card')) and 'Các PDF đang giữ bản cũ' in doc.get_text())
    check('preview marker retained',bool(doc.select('[data-zo-revision-preview]')) or 'BẢN THẢO ĐỘC LẬP' in doc.get_text())
    data={'checks':checks,'passed':all(checks.values()),'owner_acceptance':False,'PDF_built':False}
    report=ROOT/'_audit/r1_g01_revision_20261031/regressions.json'
    report.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(data,ensure_ascii=False,indent=2))
    return 0 if data['passed'] else 1
if __name__=='__main__':raise SystemExit(main())


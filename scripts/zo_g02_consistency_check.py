"""Semantic source/HTML regressions; machine evidence is not owner acceptance."""
import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
import yaml
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu'
parser=argparse.ArgumentParser()
parser.add_argument('--output',default='_audit/zo_g02_consistency_2026-10-08')
OUT=ROOT/parser.parse_args().output
plan=json.loads((BASE/'r1_g02/giao_dien/web_2027_layout.json').read_text(encoding='utf-8'))
source=(BASE/'r1_g02/index.qmd').read_text(encoding='utf-8')
g01source=(BASE/'r1_g01/index.qmd').read_text(encoding='utf-8')
page=BeautifulSoup((OUT/'g02-reading.html').read_text(encoding='utf-8'),'html.parser')
reference=ROOT/'docs/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.html'
g01=BeautifulSoup(reference.read_text(encoding='utf-8'),'html.parser')
checks=[]
def check(name,actual,expected=True):
    checks.append({'name':name,'pass':actual==expected,'actual':actual,'expected':expected})
def paper(node):
    return node.find_parent(class_='reading-region') or node.find(class_='reading-region')
def role(node):
    p=paper(node)
    return p.select_one('.role').get_text(' ',strip=True) if p else None
def heading_level(node):
    h=node.find(re.compile('^h[2-6]$'))
    return h.name if h else None
def rows(node):
    return [[cell.get_text(' ',strip=True) for cell in tr.find_all(['th','td'],recursive=False)] for tr in node.select('tbody tr')]
def table_contract(node):
    return {k:node.get(k) for k in ['data-family','data-responsive','data-col-widths','data-min-width','data-row-header']}

receipt=json.loads((BASE/'r1_g01/giao_dien/web_2027_accepted.json').read_text(encoding='utf-8'))
check('Accepted G01 HTML hash unchanged',hashlib.sha256(reference.read_bytes()).hexdigest(),receipt['html_sha256'])
journal=(BASE/'_dung_chung/nhat_ki_hoc_tap.qmd').read_text(encoding='utf-8')
g01journal=re.search(r'^### .*\{#nhat-ky[^\n]*\}\s*\n(.*?)(?=^#{2,3} )',g01source,re.M|re.S)
check('Shared journal exactly reuses G01 canonical body',journal.strip(),g01journal[1].strip() if g01journal else None)
check('G02 journal uses shared include', '{{< include ../_dung_chung/nhat_ki_hoc_tap.qmd >}}' in source)
for ident in ['r1-table-t13','r1-table-t18']:
    a=page.find(id=ident);b=g01.find(id=ident)
    check(ident+' same 14 rows',len(rows(a)),14)
    check(ident+' same field/content rows as accepted G01',rows(a),rows(b))
    check(ident+' same table component contract',table_contract(a),table_contract(b))
check('Journal is one reading beat',len(page.find(id='nhat-ky').select('.reading-region')),1)
for ident,spec in plan['sections'].items():
    node=page.find(id=ident)
    check(ident+' exists',node is not None)
    if node:
        check(ident+' semantic role',role(node),spec['label'])
        if spec.get('unit'):
            check(ident+' one complete beat',len(node.select('.reading-region')) if node.name=='section' else int(paper(node) is not None),1)
for ident in ['doi-tuong','dinh-nghia','tren-doan','tap-khac','loi-van','bắt-đầu-từ-đâu']:
    check(ident+' chapter h3',heading_level(page.find(id=ident)),'h3')
for ident in ['quy-tac-va-tap-xac-dinh','dinh-nghia-tren-tap-dang-xet','dieu-kien-bao-dam-ton-tai','doc-su-dat-duoc-khi-thay-tap','dai-luong-ham-muc-tieu-rang-buoc','on-nen']:
    check(ident+' content/support h4',heading_level(page.find(id=ident)),'h4')
check('Foundation nested under kickoff',page.find(id='on-nen').find_parent(id='bắt-đầu-từ-đâu') is not None)
for ident,owner in [('câu-hỏi-dẫn-đường','dinh-huong-bai-hoc'),('học-xong-em-cần-làm-được-gì','bat-dau')]:
    check(ident+' in current functional owner',page.find(id=ident).find_parent(id=owner) is not None)
    check(ident+' keeps existing anchor kind',page.find(id=ident).name,'span')
check('Warmup task independent from instructions',paper(page.find(id='ba-câu-khởi-động')) is not paper(page.find(id='cach-thuc-hien-bat-dau')))
self_id='ví-dụ-làm-mẫu-so-sánh-giá-trị-không-so-sánh-hoành-độ'
check('Unworked task is not a worked example',role(page.find(id=self_id)),'Tự kiểm tra')
check('Method and self-task separate beats',paper(page.find(id=self_id)) is not paper(page.find(id='quy-trình-so-sánh-một-danh-sách-hữu-hạn')))
tables={n['id']:n for n in page.select('.r1-table[id]')}
check('Every data table classified',sorted(tables),sorted(plan['table_roles']))
for ident,node in tables.items():
    # G01 includes both explicit scope=col and native TH/auto-scope tables.
    # Do not invent a new universal explicit-scope requirement from one sample.
    check(ident+' column header semantics',bool(node.select('thead th')) and all(n.get('scope') in [None,'col'] for n in node.select('thead th')))
    check(ident+' assigned responsive mode',node.get('data-responsive') in ['fit','scroll'])
check('Routing T10 uses local scroll',tables['r1-g02-table-t10'].get('data-responsive'),'scroll')
check('Legacy guide remains hidden',tables['r1-g02-table-t08'].has_attr('hidden'))
check('Objectives same family/responsiveness/widths as G01',{k:table_contract(tables['r1-g02-table-t09'])[k] for k in ['data-family','data-responsive','data-col-widths']},{k:table_contract(g01.find(id='r1-table-t02'))[k] for k in ['data-family','data-responsive','data-col-widths']})
# Deliberately corrupt copies: guards must reject role, hierarchy, journal drift.
broken=copy.deepcopy(page)
paper(broken.find(id=self_id)).select_one('.role').string='Ví dụ'
check('Negative: wrong self-task role detected',role(broken.find(id=self_id))!='Tự kiểm tra')
broken.find(id='quy-tac-va-tap-xac-dinh').find('h4').name='h3'
check('Negative: wrong content level detected',heading_level(broken.find(id='quy-tac-va-tap-xac-dinh'))!='h4')
broken.find(id='r1-table-t13').select_one('tbody tr').decompose()
check('Negative: missing journal field detected',len(rows(broken.find(id='r1-table-t13')))!=14)
broken.find(id='r1-g02-table-t10')['data-responsive']='fit'
check('Negative: routing mode drift detected',broken.find(id='r1-g02-table-t10').get('data-responsive')!='scroll')
inventory=[]
for node in page.select('.reading-region'):
    owner=node.find_parent('section')
    label=node.select_one('.role')
    inventory.append({'owner':owner.get('id') if owner else None,'role':label.get_text(' ',strip=True) if label else 'Ủng hộ ZO Math','headings':[{'level':n.name,'title':n.get_text(' ',strip=True)} for n in node.find_all(re.compile('^h[2-6]$'))],'ids':[n['id'] for n in node.select('[id]')],'tables':[n['id'] for n in node.select('.r1-table[id]')]})
report={'checks':checks,'reading_regions':inventory,'tables':{k:{'role':plan['table_roles'][k],**table_contract(v)} for k,v in tables.items()},'limits':['Checks validate mapped semantic structure, not complete independent pedagogical acceptance.','G01 remains frozen inline journal; G02 consumes exact common include.','No PDF rebuild, release or owner acceptance.']}
(OUT/'semantic-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
failed=[n['name'] for n in checks if not n['pass']]
print(json.dumps({'passed':len(checks)-len(failed),'total':len(checks),'failures':failed},ensure_ascii=False))
raise SystemExit(bool(failed))

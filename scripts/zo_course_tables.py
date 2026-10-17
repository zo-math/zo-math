"""QD_030 table-role binding for the four opt-in 2027 pages, never global CSS.

Content/IDs/links are QMD-owned; native mathematical grids are JSON-owned.
Bindings classify function, not text. Unclassified or stale tables fail build.
"""
from __future__ import annotations
import argparse, copy, json, os, shutil, sys
from pathlib import Path
from bs4 import BeautifulSoup
import yaml

# One browser predicate used by both existing checkers and the table audit.
BROWSER_ALIGNMENT_ERRORS = '''(()=>{const errors=[];for(const t of document.querySelectorAll('.reader-content table')){const kind=t.dataset.tableKind;for(const c of t.querySelectorAll('th,td')){if(!c.getClientRects().length)continue;const head=!!c.closest('thead');let expected='left';if(kind==='values'||kind==='variation'||(kind==='sign'&&t.dataset.tableVariant!=='explained'))expected='center';if(kind==='matrix'&&!head&&c.tagName==='TD')expected='center';if(kind==='frequency'&&!head&&c.tagName==='TD')expected='right';if(c.classList.contains('zo-center-cell'))expected='center';if(t.dataset.tableVariant==='numbered'&&!head&&c.tagName==='TH')expected='center';if(!kind&&c.tagName!=='TH')continue;if(getComputedStyle(c).textAlign!==expected)errors.push({kind,text:c.textContent.trim(),expected,actual:getComputedStyle(c).textAlign})}}return errors})()'''

ROOT=Path(__file__).resolve().parents[1]
KIT=ROOT/'_design/web_2027_mau_dung_chung'
CONTRACT=KIT/'profiles/course-tables.json'
BASE=ROOT/'content/thpt/on_thi_toan_thpt'

def load_contract():
    data=json.loads(CONTRACT.read_text(encoding='utf-8'))
    if data.get('schema_version')!=1 or data.get('decision')!='QD_030':
        raise ValueError('Unsupported current table contract')
    return data

def table_specs(page_key):
    if page_key=='home':return {}
    source=BASE/'hoc_lieu'/page_key/'index.qmd'
    meta=yaml.safe_load(source.read_text(encoding='utf-8').split('---',2)[1])
    return {s['id']:s for s in meta.get('r1-tables',[])}

def native_records(page_key):
    if page_key=='home':return {}
    return {r['id']:r for r in json.loads((BASE/'hoc_lieu'/page_key/'du_lieu/bang_bien_thien.json').read_text(encoding='utf-8'))}

def promote_d0_grid(doc):
    """Opt-in native rendering of unchanged D0 BBT JSON, not regeneration of QMD."""
    from zo_web_2027_figures import module, VARIATION
    sys.path.insert(0,str(VARIATION))
    renderer=module('course_tables_variation04',VARIATION/'zo_variation_html.py')
    records=renderer.load_data(BASE/'hoc_lieu/d0/du_lieu/bang_bien_thien.json')
    fragments=renderer.math_fragments(records)
    for record in records:
        figure=doc.select_one(f'figure.zo-variation-asset[data-bbt="{record["id"]}"]')
        if figure is None:raise ValueError('Missing D0 sign table')
        old=figure.select_one('table.variation')
        rows=[[c.get_text(' ',strip=True) for c in row.find_all(['th','td'],recursive=False)] for row in old.select('tr')]
        if rows!=record['rows']:raise ValueError('D0 sign table differs from canonical JSON')
        caption=figure.select_one('figcaption')
        viewport=figure.select_one('.figure-viewport')
        native=BeautifulSoup(renderer.render_record(record,fragments),'html.parser').select_one('table')
        native.caption.string=caption.get_text(' ',strip=True)
        viewport.select_one('img').decompose()
        figure.select_one('.visually-hidden').decompose()
        viewport.append(native)

def bind(doc,page_key):
    root=doc.select_one('.reader-content')
    if root is None:raise ValueError('Missing course reader root')
    from zo_course_math_assets import apply_native
    apply_native(doc,page_key)
    contract=load_contract();specs=table_specs(page_key);seen=set()
    for entry in contract['pages'][page_key]:
        matches=root.select(entry['selector'])
        if len(matches)!=1:raise ValueError('Missing or ambiguous table role: '+entry['selector'])
        table=matches[0]
        if id(table) in seen:raise ValueError('Duplicate table role binding')
        seen.add(id(table));kind=entry['kind']
        if kind not in contract['types']:raise ValueError('Unknown table type')
        if kind=='variation':raise ValueError('Variation tables must use canonical JSON and the native renderer; ordinary table binding is forbidden')
        owner=table.find_parent(id=True);spec=specs.get(owner.get('id'),{}) if owner else {}
        table['class']=list(dict.fromkeys(table.get('class',[])+['r1-data-table','zo-course-table','zo-course-table--'+kind]))
        table['data-table-kind']=kind;table['data-table-role']=entry['role']
        if entry.get('variant'):table['data-table-variant']=entry['variant']
        rows=table.select('tr');cols=len(rows[0].find_all(['th','td'],recursive=False))
        widths=entry.get('widths',spec.get('widths',[100/cols]*cols))
        if len(widths)!=cols or abs(sum(widths)-100)>.01:raise ValueError('Invalid table widths')
        for colgroup in list(table.select('colgroup')):colgroup.decompose()
        colgroup=doc.new_tag('colgroup')
        for width in widths:colgroup.append(doc.new_tag('col',attrs={'style':f'width:{width:g}%'}))
        table.insert(0,colgroup)
        row_header=entry.get('row_header',spec.get('row_header',True))
        for r,row in enumerate(rows):
            cells=row.find_all(['th','td'],recursive=False)
            if len(cells)!=cols:raise ValueError('Merged table requires an explicit structural policy')
            for c,cell in enumerate(cells):
                header=r==0 or (c==0 and row_header)
                cell.name='th' if header else 'td'
                cell.attrs.pop('align',None);cell.attrs.pop('style',None);cell.attrs.pop('scope',None)
                if header:cell['scope']='col' if r==0 else 'row'
                classes=[n for n in cell.get('class',[]) if not n.startswith('zo-')]
                if r>0 and c+1 in entry.get('center_body_columns',[]):classes.append('zo-center-cell')
                if c+1==entry.get('focus_column'):classes.append('zo-focus-cell')
                if kind=='frequency' and r>0 and (c>0 or not row_header):classes.append('zo-numeric-cell')
                if classes:cell['class']=classes
                elif cell.has_attr('class'):del cell['class']
        if entry.get('corner_label'):
            rows[0].find(['th','td'],recursive=False)['aria-label']=entry['corner_label']
        frame=table.parent
        if not any(c in frame.get('class',[]) for c in ['r1-table','r1-table-scroll-x','table-scroll','zo-course-table-frame']):
            frame=doc.new_tag('div');table.wrap(frame)
        frame['class']=list(dict.fromkeys(frame.get('class',[])+['zo-course-table-frame']))
        frame['tabindex']='0';frame['role']='region'
        frame['aria-label']=spec.get('label',entry['role'])+'; cuộn ngang khi cần'
        # Fit mathematical value grids; preserve the relative position of each x/f(x) pair.
        minimum=None if kind=='values' else spec.get('min_width')
        if minimum is None and page_key=='d0':minimum='32em' if cols>=4 else '26em'
        if entry.get('variant')=='routing':minimum='54em'
        table['style']='min-width:'+str(minimum) if minimum else 'min-width:0'
    records=native_records(page_key);native_seen=set()
    for table in root.select('table.zo-variation-native'):
        rid=table['data-bbt'];record=records.get(rid)
        if record is None:raise ValueError('Unowned native mathematical table: '+rid)
        if rid in native_seen:raise ValueError('Duplicate native mathematical table: '+rid)
        native_seen.add(rid)
        rows=[[c['data-source-value'] for c in row.find_all(['th','td'],recursive=False)] for row in table.select('tr')]
        if rows!=record['rows']:raise ValueError('Native table lost mathematical data: '+rid)
        # Rows and arrows are literal JSON data, not inferred derivative information.
        kind='variation' if any('↗' in v or '↘' in v or '→' in v for row in record['rows'] for v in row) else 'sign'
        table['class']=list(dict.fromkeys(table.get('class',[])+['zo-course-table','zo-course-table--'+kind]))
        table['data-table-kind']=kind;table['data-table-role']=record['title']
        if kind=='sign':
            for cell in table.select('tbody tr:last-child > *'):cell['class']=cell.get('class',[])+['zo-focus-cell']
        frame=table.parent;frame['class']=list(dict.fromkeys(frame.get('class',[])+['zo-course-table-frame']))
        seen.add(id(table))
    if native_seen!=set(records):raise ValueError('Missing canonical native mathematical tables')
    unknown=[t.get('id',str(t)[:140]) for t in root.select('table') if id(t) not in seen]
    if unknown:raise ValueError('Unclassified course tables: '+str(unknown))
    return len(seen)

def apply(doc,page_key,page,runtime):
    if page_key=='d0':promote_d0_grid(doc)
    count=bind(doc,page_key)
    runtime.mkdir(parents=True,exist_ok=True)
    css=runtime/'course-tables.css';shutil.copyfile(KIT/css.name,css)
    doc.head.append(doc.new_tag('link',rel='stylesheet',href=os.path.relpath(css,page.parent).replace('\\','/')))
    doc.body['data-zo-table-contract']='QD_030'
    return count

def self_test():
    data=load_contract();checks={}
    checks['eight supported 0.4 types']=len(set(data['types']))==8
    for key,entries in data['pages'].items():
        checks[key+' unique bindings']=len({e['selector'] for e in entries})==len(entries)
        checks[key+' explicit valid roles']=all(e['kind'] in data['types'] and e.get('role') for e in entries)
    for key in ['r1_g01','r1_g02']:
        specs=table_specs(key)
        checks[key+' all ordinary sources typed']=set(specs)=={e['selector'][1:].split()[0] for e in data['pages'][key]}
    # A table not in the contract must fail, even on a page that currently has none.
    bad=BeautifulSoup('<main class="reader-content"><table><tr><td>x</td></tr></table></main>','html.parser')
    try:bind(bad,'home')
    except ValueError as exc:checks['unclassified table rejected']='Unclassified' in str(exc)
    else:checks['unclassified table rejected']=False
    missing=BeautifulSoup('<main class="reader-content"></main>','html.parser')
    try:bind(missing,'r1_g02')
    except ValueError as exc:checks['missing classified table rejected']='Missing or ambiguous' in str(exc)
    else:checks['missing classified table rejected']=False
    unknown=BeautifulSoup('<main class="reader-content"><table class="zo-variation-native" data-bbt="UNKNOWN"></table></main>','html.parser')
    try:bind(unknown,'home')
    except ValueError as exc:checks['unowned mathematical grid rejected']='Unowned' in str(exc)
    else:checks['unowned mathematical grid rejected']=False
    return checks

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--self-test',action='store_true');args=parser.parse_args()
    checks=self_test();print(json.dumps({'passed':sum(checks.values()),'total':len(checks),'failures':[k for k,v in checks.items() if not v]},ensure_ascii=False))
    raise SystemExit(not all(checks.values()))

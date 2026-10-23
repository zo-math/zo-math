"""QD_030 table-role binding for the four opt-in 2027 pages, never global CSS.

Content/IDs/links are QMD-owned; native mathematical grids are JSON-owned.
Bindings classify function, not text. Unclassified or stale tables fail build.
"""
from __future__ import annotations
import argparse, copy, json, os, re, shutil, sys
from pathlib import Path
from bs4 import BeautifulSoup
import yaml

# One browser predicate used by both existing checkers and the table audit.
BROWSER_ALIGNMENT_ERRORS = '''(()=>{const errors=[];for(const t of document.querySelectorAll('.reader-content table')){const kind=t.dataset.tableKind;for(const c of t.querySelectorAll('th,td')){if(!c.getClientRects().length)continue;const head=!!c.closest('thead');let expected='left';if(kind==='values'||kind==='variation'||(kind==='sign'&&t.dataset.tableVariant!=='explained'))expected='center';if(kind==='matrix'&&!head&&c.tagName==='TD')expected='center';if(kind==='frequency'&&!head&&c.tagName==='TD')expected='right';if(c.classList.contains('zo-center-cell'))expected='center';if(c.classList.contains('zo-numeric-cell'))expected='right';if(t.dataset.tableVariant==='numbered'&&!head&&c.tagName==='TH')expected='center';if(head){const body=t.querySelector('tbody tr')?.children[c.cellIndex];if(body)expected=getComputedStyle(body).textAlign}if(!kind&&c.tagName!=='TH')continue;if(getComputedStyle(c).textAlign!==expected)errors.push({kind,text:c.textContent.trim(),expected,actual:getComputedStyle(c).textAlign})}}return errors})()'''

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
    scene=BASE/'hoc_lieu'/page_key/'giao_dien/minh_hoa_manifest.json'
    if scene.is_file():
        from zo_course_scenes import source_checks
        checks=source_checks(scene.parent.parent/'index.qmd')
        if not all(checks.values()):raise ValueError('Invalid canonical scene inventory')
        return {}
    if not any(e.get('kind')=='variation' for e in load_contract()['pages'].get(page_key,[])):return {}
    return {r['id']:r for r in json.loads((BASE/'hoc_lieu'/page_key/'du_lieu/bang_bien_thien.json').read_text(encoding='utf-8'))}

def place_captions_below(root):
    """Keep one owned name after the figure/scroll area, without changing text."""
    for figure in root.select('figure'):
        captions=[n for n in figure.select('figcaption') if n.find_parent('figure') is figure]
        if len(captions)>1:raise ValueError('Figure has multiple visible captions')
        if captions:figure.append(captions[0].extract())


def apply_mathematical_presentation(root):
    grid=load_contract()['mathematical_grid']
    for table in root.select('table[data-table-kind]'):
        if table['data-table-kind'] in grid['kinds']:
            table['class']=list(dict.fromkeys(table.get('class',[])+[grid['class']]))
    place_captions_below(root)


def media_html_checks(doc):
    root=doc.select_one('.reader-content');grid=load_contract()['mathematical_grid'];checks={}
    for n,table in enumerate(root.select('table[data-table-kind]'),1):
        rows=table.select('tr');kind=table['data-table-kind']
        checks[f'table {n} no conflicting cell alignment classes']=not any(
            {'zo-center-cell','zo-numeric-cell'}.issubset(cell.get('class',[]))
            for cell in table.select('th,td'))
        if len(rows)>1 and kind in {'frequency','matrix'}:
            for c,(head,body) in enumerate(zip(rows[0].find_all(['th','td'],recursive=False),rows[1].find_all(['th','td'],recursive=False)),1):
                center='zo-center-cell' in body.get('class',[]) or kind=='matrix' and body.name=='td'
                right=not center and kind=='frequency' and body.name=='td'
                checks[f'table {n} column {c} header matches data alignment']=('zo-center-cell' in head.get('class',[]))==center and ('zo-numeric-cell' in head.get('class',[]))==right
        if table['data-table-kind'] not in grid['kinds']:continue
        checks[f'table {n} shared mathematical grid']=grid['class'] in table.get('class',[])
        if 'zo-variation-native' in table.get('class',[]):
            figure=table.find_parent('figure');cap=figure.find('figcaption',recursive=False) if figure else None
            checks[f'table {n} one name below scroll']=bool(cap and cap.get_text(strip=True)) and list(figure.find_all(recursive=False))[-1] is cap
    for n,figure in enumerate(root.select('figure'),1):
        own=[c for c in figure.select('figcaption') if c.find_parent('figure') is figure]
        if own:checks[f'figure {n} name below content']=len(own)==1 and own[0].parent is figure and list(figure.find_all(recursive=False))[-1] is own[0]
    for n,image in enumerate(root.select('.figure-viewport img'),1):
        if 'zo-variation-image' in image.get('class',[]):continue
        figure=image.find_parent('figure');cap=figure.find('figcaption') if figure else None
        named=bool(cap and cap.get_text(strip=True));omitted=image.get('data-zo-caption')=='omitted'
        checks[f'image {n} reviewed caption choice']=(named and not omitted) or (not named and omitted and bool(image.get('data-zo-caption-reason','').strip()) and bool(image.get('alt','').strip()))
    from zo_course_remediation import html_checks as remediation_html_checks
    checks.update(remediation_html_checks(doc))
    from zo_course_table_roles import html_checks as function_html_checks
    checks.update(function_html_checks(doc))
    return checks


def media_style_checks(css=None):
    css=(KIT/'course-tables.css').read_text(encoding='utf-8') if css is None else css
    def declarations(selector):
        match=re.search(r'(?m)^'+re.escape(selector)+r'\{([^}]+)\}',css)
        return dict(item.split(':',1) for item in match[1].split(';') if ':' in item) if match else {}
    table=declarations('.reader-content table.zo-course-table.zo-math-grid')
    cells=declarations('.reader-content table.zo-course-table.zo-math-grid :is(th,td)')
    excluded=declarations('.reader-content table.zo-course-table.zo-math-grid .excluded')
    return {'math grid uses native surface':table.get('--zo-grid-paper')=='#FBFAF8' and table.get('background')=='var(--zo-grid-paper)',
            'math grid uses native ink and line':table.get('--zo-grid-ink')=='#3E3A35' and table.get('--zo-grid-line')=='#DFD7CA',
            'math grid uses body-size math':table.get('font-size')=='1em' and table.get('line-height')=='1.6',
            'math grid cells use same stroke and padding':cells.get('border')=='1px solid var(--zo-grid-line)' and cells.get('padding')=='.65em .8em' and cells.get('min-width')=='2.4em',
            'excluded columns retain double boundary':excluded.get('border-left')=='3px double #766F66' and excluded.get('border-right')=='3px double #766F66',
            'table names below': 'caption-side:bottom' in css and not re.search(r'caption-side\s*:\s*top',css)}


def media_source_checks(source,repo=ROOT,text=None):
    source=Path(source);repo=Path(repo)
    if source.name!='index.qmd' or source.parent.name not in {'d0','r1_g01','r1_g02','r1_g03','r1_g04'} or source.parent.parent.name!='hoc_lieu':return {}
    text=source.read_text(encoding='utf-8') if text is None else text
    inherited=yaml.safe_load((repo/'content/thpt/on_thi_toan_thpt/_metadata.yml').read_text(encoding='utf-8'))
    meta=yaml.safe_load(text.split('---',2)[1]);checks={'table caption default below':meta.get('tbl-cap-location',inherited.get('tbl-cap-location'))=='bottom'}
    checks.update(media_style_checks())
    entries=load_contract()['pages'][source.parent.name]
    for entry in entries:
        if entry['kind'] not in {'sign','values'}:continue
        checks[entry['selector']+' reviewed unnamed grid']=entry.get('caption_policy')=='context' and bool(entry.get('caption_reason','').strip())
    for n,m in enumerate(re.finditer(r'!\[([^\n]*?)\]\(([^\s)]+)\)(\{[^\n}]*\})?',text),1):
        caption,path,attrs=m.groups();attrs=attrs or ''
        if not path.endswith('.svg'):continue
        start=text.rfind('<figure',0,m.start());closed=text.rfind('</figure>',0,m.start());end=text.find('</figure>',m.end())
        explicit=start>closed and end>=0 and bool(re.search(r'<figcaption[^>]*>\s*\S',text[start:end]))
        omitted='data-zo-caption="omitted"' in attrs
        if not caption.strip() and not explicit:
            reason=re.search(r'data-zo-caption-reason="([^"]+)"',attrs);alt=re.search(r'fig-alt="([^"]+)"',attrs)
            checks[f'image {n}/{Path(path).name} justified omission']=omitted and bool(reason and reason[1].strip()) and bool(alt and alt[1].strip())
        else:checks[f'image {n}/{Path(path).name} named when shown']=not omitted
    return checks


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
    from zo_course_table_roles import function_profile,apply_function
    for entry in contract['pages'][page_key]:
        matches=root.select(entry['selector'])
        if len(matches)!=1:raise ValueError('Missing or ambiguous table role: '+entry['selector'])
        table=matches[0]
        function=function_profile(entry,contract)
        if id(table) in seen:raise ValueError('Duplicate table role binding')
        seen.add(id(table));kind=entry['kind']
        if kind not in contract['types']:raise ValueError('Unknown table type')
        if kind=='variation':raise ValueError('Variation tables must use canonical JSON and the native renderer; ordinary table binding is forbidden')
        owner=table.find_parent(id=True);spec=specs.get(owner.get('id'),{}) if owner else {}
        table['class']=list(dict.fromkeys(table.get('class',[])+['r1-data-table','zo-course-table','zo-course-table--'+kind]))
        table['data-table-kind']=kind;table['data-table-role']=entry['role']
        if entry.get('variant'):table['data-table-variant']=entry['variant']
        rows=table.select('tr');cols=len(rows[0].find_all(['th','td'],recursive=False))
        widths=function['widths'] if function else entry.get('widths',spec.get('widths',[100/cols]*cols))
        if len(widths)!=cols or abs(sum(widths)-100)>.01:raise ValueError('Invalid table widths')
        for colgroup in list(table.select('colgroup')):colgroup.decompose()
        colgroup=doc.new_tag('colgroup')
        for width in widths:colgroup.append(doc.new_tag('col',attrs={'style':f'width:{width:g}%'}))
        table.insert(0,colgroup)
        row_header=function['row_header'] if function else entry.get('row_header',spec.get('row_header',True))
        right_columns=function.get('right_columns',[]) if function else []
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
                if (c+1 in right_columns or kind=='frequency' and r>0 and (c>0 or not row_header)) and c+1 not in entry.get('center_body_columns',[]):classes.append('zo-numeric-cell')
                if classes:cell['class']=classes
                elif cell.has_attr('class'):del cell['class']
        if entry.get('corner_label'):
            rows[0].find(['th','td'],recursive=False)['aria-label']=entry['corner_label']
        # Headers use the alignment of their data column, including a numeric
        # first column when the table has no row headings. Body policy is intact.
        for c,cell in enumerate(rows[0].find_all(['th','td'],recursive=False)):
            centered=(c+1 in entry.get('center_body_columns',[]) or kind in {'values','sign'} and entry.get('variant')!='explained' or kind=='matrix' and (c>0 or not row_header) or entry.get('variant')=='numbered' and c==0)
            right=c+1 in right_columns or kind=='frequency' and (c>0 or not row_header)
            if centered:cell['class']=cell.get('class',[])+['zo-center-cell']
            elif right:cell['class']=list(dict.fromkeys(cell.get('class',[])+['zo-numeric-cell']))
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
        if function:minimum=function.get('min_width')
        table['style']='min-width:'+str(minimum) if minimum else 'min-width:0'
        if function:
            apply_function(table,function,entry['function'],doc)
            frame['aria-label']=entry['role']+(' ; cuộn ngang khi cần' if function['responsive']=='scroll' else '')
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
    apply_mathematical_presentation(root)
    failed=[name for name,value in media_html_checks(doc).items() if not value]
    if failed:raise ValueError('Course tables/captions: '+str(failed))
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
    checks['column headers follow body contract']=data.get('column_header_alignment')=='match_body_column'
    fixture=BeautifulSoup('<main class="reader-content"><table data-table-kind="frequency"><thead><tr><th>Loại</th><th class="zo-numeric-cell">Lãi</th></tr></thead><tbody><tr><th>A</th><td class="zo-numeric-cell">30</td></tr></tbody></table></main>','html.parser')
    checks['aligned numerical header accepted']=all(media_html_checks(fixture).values())
    fixture.select_one('thead th.zo-numeric-cell').attrs.pop('class')
    checks['left header above right data rejected']=not all(media_html_checks(fixture).values())
    checks.update(media_style_checks())
    for key in ['d0','r1_g01','r1_g02','r1_g03','r1_g04']:
        source=media_source_checks(BASE/'hoc_lieu'/key/'index.qmd')
        checks[key+' current media source']=bool(source) and all(source.values())
    fixture=BeautifulSoup('<main class="reader-content"><figure><div class="figure-viewport"><figcaption>Tên bảng</figcaption><table class="zo-course-table" data-table-kind="values"><tr><th>x</th><td>1</td></tr><tr><th>f(x)</th><td>2</td></tr></table></div></figure></main>','html.parser')
    checks['old mathematical class/caption defects rejected']=not all(media_html_checks(fixture).values())
    cells=[n.get_text() for n in fixture.select('th,td')]
    apply_mathematical_presentation(fixture.select_one('.reader-content'))
    checks['shared math component with name below accepted']=all(media_html_checks(fixture).values())
    checks['math cells unchanged by presentation']=[n.get_text() for n in fixture.select('th,td')]==cells
    cap=fixture.select_one('figcaption')
    checks['name outside horizontal scrolling area']=cap.parent is fixture.figure and fixture.figure.contents[-1] is cap
    once=str(fixture);apply_mathematical_presentation(fixture.select_one('.reader-content'))
    checks['caption placement idempotent']=str(fixture)==once
    broken=copy.deepcopy(fixture);broken.table['class']=['zo-course-table']
    checks['missing math grid class rejected']=not all(media_html_checks(broken).values())
    broken=copy.deepcopy(fixture);broken.figure.insert(0,broken.figcaption.extract())
    checks['caption above figure rejected']=not all(media_html_checks(broken).values())
    unnamed=BeautifulSoup('<main class="reader-content"><table class="zo-course-table" data-table-kind="values"><tr><th>x</th><td>1</td></tr></table></main>','html.parser')
    apply_mathematical_presentation(unnamed.select_one('.reader-content'))
    checks['contextual value table remains unnamed']=not unnamed.find('caption') and not unnamed.find('figcaption') and all(media_html_checks(unnamed).values())
    omitted=BeautifulSoup('<main class="reader-content"><div class="figure-viewport"><img alt="Đồ thị dữ kiện" data-zo-caption="omitted" data-zo-caption-reason="Một đồ thị duy nhất trong đề"></div></main>','html.parser')
    checks['justified graph caption omission accepted']=all(media_html_checks(omitted).values())
    omitted.img.attrs.pop('data-zo-caption-reason')
    checks['unexplained missing graph caption rejected']=not all(media_html_checks(omitted).values())
    css=(KIT/'course-tables.css').read_text(encoding='utf-8')
    for old,new in [('font-size:1em;line-height:1.6','font-size:.88em;line-height:1.6'),('padding:.65em .8em','padding:12px 15px'),('caption-side:bottom','caption-side:top'),('border-left:3px double #766F66','border-left:1px solid #766F66')]:
        checks['reject CSS regression '+new]=not all(media_style_checks(css.replace(old,new)).values())
    source=BASE/'hoc_lieu/r1_g03/index.qmd';text=source.read_text(encoding='utf-8')
    checks['source missing graph-caption reason rejected']=not all(media_source_checks(source,text=text.replace('data-zo-caption-reason=', 'data-omitted-reason=',1)).values())
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

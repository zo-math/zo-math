"""Function-specific course tables. Source validation is not visual acceptance."""
from __future__ import annotations
import copy,json,re
from pathlib import Path
from urllib.parse import unquote
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
RULE='TABLE-FUNCTIONS-20261019'
CONTRACT=Path('_design/web_2027_mau_dung_chung/profiles/course-tables.json')
KINDS={'rubric','comparison','process'}

def contract(root=ROOT):return json.loads((Path(root)/CONTRACT).read_text(encoding='utf-8'))

def function_profile(entry,data):
    name=entry.get('function')
    if entry['kind'] not in KINDS or entry.get('variant')=='routing':return None
    if name not in data.get('function_profiles',{}):raise ValueError('Missing/unknown table function: '+entry['selector'])
    profile=data['function_profiles'][name]
    if profile['kind']!=entry['kind']:raise ValueError('Table kind differs from function: '+name)
    if any(k in entry for k in ['widths','row_header','min_width','right_columns','responsive']):raise ValueError('Per-page override of shared table function: '+name)
    return profile

def table_rows(text,ident):
    """Read a pipe table owned by a stable div or section, never YAML IDs."""
    body=text.split('---',2)[-1] if text.startswith('---') else text
    owners=list(re.finditer(r'\{#'+re.escape(ident)+r'(?=[\s}])',body))
    if len(owners)!=1:return []
    tail=body[owners[0].end():];m=re.search(r'(?m)^\|[^\n]*\n\|[ :|\-]+\|[ \t]*\n(?:\|[^\n]*(?:\n|$))+',tail)
    if not m:
        simple=re.search(r'(?m)^  (.+)\n  (-{3,}[ \t]+-{3,})[ \t]*\n((?:  [^\n]+\n)+)',tail)
        if not simple:return []
        rows=[re.split(r'\s{2,}',line.strip()) for line in [simple[1],*simple[3].splitlines()]]
        return rows if all(len(r)==2 for r in rows) else []
    # No crossing into a different heading/div when a table has been removed.
    if re.search(r'(?m)^(?:#{1,6} |:{3,})',tail[:m.start()]):return []
    return [[v.strip() for v in line.strip().strip('|').split('|')] for line in m[0].splitlines() if not re.fullmatch(r'[| :\-]+',line)]

def pipe_owners(text):
    """Inventory independent of bindings, including tables inside disclosures."""
    body=text.split('---',2)[-1] if text.startswith('---') else text
    lines=body.splitlines();stack=[];heading=None;found=[]
    for n,line in enumerate(lines):
        opening=re.match(r'^(:{3,})\s+(.+)',line)
        closing=re.fullmatch(r'(:{3,})[ \t]*',line)
        if opening:
            ident=re.search(r'\{#([^\s}]+)',line)
            stack.append((len(opening[1]),ident[1] if ident else None))
        elif closing:
            # Colon fences close the innermost matching container.
            for i in range(len(stack)-1,-1,-1):
                if stack[i][0]==len(closing[1]):stack=stack[:i];break
        if re.match(r'^#{1,6} ',line):
            m=re.search(r'\{#([^\s}]+)',line);heading=m[1] if m else None
        if line.startswith('|') and n+1<len(lines) and re.fullmatch(r'\|[| :\-]*-[| :\-]*\|[ \t]*',lines[n+1]):
            found.append(next((ident for _,ident in reversed(stack) if ident),heading))
    return found

def source_checks(path,root=ROOT,text=None):
    from zo_course_editorial import governed,closure
    path=Path(path);root=Path(root)
    if not governed(path) or path.suffix!='.qmd':return {}
    key='home' if path.parent.name=='2027' else path.parent.name;c={}
    try:
        data=contract(root);c['current table function contract']=data.get('function_contract')==RULE
        c['page explicitly inventoried']=key in data['pages']
        if key not in data['pages']:return c
        sources=closure(path,root,text);body='\n'.join(sources.values());tables={}
        anchors=set(re.findall(r'\{#([^\s}]+)',body))|set(re.findall(r'\bid=["\']([^"\']+)',body))
        known={e['selector'][1:].split()[0] for e in data['pages'][key]}
        owners=pipe_owners(body)
        c['all pipe tables explicitly bound']=all(o in known for o in owners) and len(owners)==len(set(owners))
        for entry in data['pages'][key]:
            p=function_profile(entry,data)
            if p is None:continue
            ident=entry['selector'][1:].split()[0];role=entry['function'];rows=table_rows(body,ident);tables[ident]=rows
            prefix=ident+'/'
            c[prefix+'one nonempty source table']=len(rows)>=2
            if len(rows)<2:continue
            n=len(p['widths']);c[prefix+'functional column arity']=all(len(r)==n for r in rows)
            c[prefix+'shared widths']=sum(p['widths'])==100 and all(v>0 for v in p['widths'])
            c[prefix+'responsive policy']=p['responsive'] in {'records','scroll'} and (p['responsive']!='scroll' or bool(re.fullmatch(r'\d+em',p.get('min_width',''))))
            if p.get('headers'):c[prefix+'functional headings']=rows[0]==p['headers']
            c[prefix+'no empty functional cells']=all(all(v for v in r) for r in rows[1:])
            if role in {'assessment','checkpoint'}:
                c[prefix+'each evidence cell names linked work']=all(len(r)==n and bool(re.search(r'\]\(#[^)]+\)',r[1])) for r in rows[1:])
                c[prefix+'no retired task names']=not re.search(r'\b(?:Kiểm tra|Bài|bài)\s+0[1-9]\b',str(rows))
            if role=='scoring':c[prefix+'numeric scores use LaTeX']=all(len(r)==n and bool(re.fullmatch(r'\$\d+(?:\{,\}\d+)?\$',r[-1])) for r in rows[1:])
            if role=='journal':c[prefix+'journal keeps fourteen fields']=len(rows)==15
            if role=='practice':c[prefix+'practice entry or range explicit']=all('Bắt đầu từ ' in r[-1] or '–' in r[-1] for r in rows[1:])
            if role=='review':c[prefix+'checkpoint labels name their destination']=all('Điểm dừng ' in r[-1] for r in rows[1:])
            for row in rows[1:]:
                for target in re.findall(r'\]\(#([^)]*)\)',str(row)):c[prefix+'target '+target]=unquote(target) in anchors
        if key.startswith('r'):
            b=json.loads((path.parent/'giao_dien/he_nhan.json').read_text(encoding='utf-8'))
            goals=b['learning_goals'];assessment=goals.get('assessment_table');rows=tables.get(assessment,[])
            c['goal/result tables have distinct functions']=any(e.get('function')=='assessment' and e['selector']=='#'+str(assessment)+' table' for e in data['pages'][key]) and any(e.get('function')=='goals' and e['selector']=='#'+goals['table']+' table' for e in data['pages'][key])
            for n,g in enumerate(goals['rows'],1):
                indexes=g.get('assessment_rows',[]);c[f'goal {n} result coverage']=bool(indexes) and all(isinstance(i,int) and 0<i<len(rows) for i in indexes)
                if not c[f'goal {n} result coverage']:continue
                evidence=g.get('assessment_evidence',[]);links=re.findall(r'\]\(#([^)]*)\)',' '.join(rows[i][1] for i in indexes))
                c[f'goal {n} reviewed evidence retained']=bool(evidence) and set(evidence)<=set(links)
        c.update(style_checks(root=root))
    except (OSError,ValueError,KeyError,IndexError) as exc:c['table function readable: '+str(exc)]=False
    return c

def apply_function(table,profile,name,doc):
    """Add presentation only; never replace learner text, math, URLs or IDs."""
    table['data-table-function']=name;table['data-table-responsive']=profile['responsive']
    table['role']='table'
    headings=table.select('thead th')
    for group in table.select('thead,tbody,tfoot'):group['role']='rowgroup'
    for row in table.select('tr'):
        row['role']='row'
        for i,cell in enumerate(row.find_all(['th','td'],recursive=False)):
            cell['role']='columnheader' if cell.find_parent('thead') else 'rowheader' if cell.name=='th' else 'cell'
            for old in cell.select('.zo-table-field-label'):old.decompose()
            if profile['responsive']=='records' and not cell.find_parent('thead'):
                label=doc.new_tag('span',attrs={'class':'zo-table-field-label','aria-hidden':'true','data-label':headings[i].get_text(' ',strip=True)})
                cell.insert(0,label)


def html_checks(doc,data=None):
    data=contract() if data is None else data;c={}
    for table in doc.select('.reader-content table[data-table-kind]'):
        kind=table['data-table-kind']
        if kind not in KINDS or table.get('data-table-variant')=='routing':continue
        name=table.get('data-table-function');prefix=str(name)+'/'+str(table.find_parent(id=True).get('id'))+'/'
        c[prefix+'function declared']=name in data.get('function_profiles',{})
        if not c[prefix+'function declared']:continue
        p=data['function_profiles'][name];rows=table.select('tr');headers=[h.get_text(' ',strip=True) for h in table.select('thead th')]
        c[prefix+'kind and responsive policy']=kind==p['kind'] and table.get('data-table-responsive')==p['responsive']
        c[prefix+'column widths']=[x.get('style') for x in table.select('colgroup col')]==[f'width:{w:g}%' for w in p['widths']]
        if p.get('headers'):c[prefix+'shared headings']=headers==p['headers']
        c[prefix+'minimum width']=table.get('style')=='min-width:'+p.get('min_width','0')
        for ri,row in enumerate(rows):
            cells=row.find_all(['th','td'],recursive=False);c[prefix+f'row {ri} arity']=len(cells)==len(p['widths'])
            for i,cell in enumerate(cells,1):
                c[prefix+f'row {ri} numeric {i}']=('zo-numeric-cell' in cell.get('class',[]))==(i in p.get('right_columns',[]))
                if ri and p['responsive']=='records':
                    labels=cell.select('.zo-table-field-label');c[prefix+f'row {ri} accessible field {i}']=len(labels)==1 and labels[0].get('aria-hidden')=='true' and labels[0].get('data-label')==headers[i-1] and not labels[0].get_text()
    return c

def style_checks(css=None,root=ROOT):
    css=(Path(root)/'_design/web_2027_mau_dung_chung/course-tables.css').read_text(encoding='utf-8') if css is None else css
    return {'role numeric alignment':'.zo-course-table .zo-numeric-cell{text-align:right;' in css,
            'record labels scoped and hidden on desktop':'.zo-table-field-label{display:none}' in css,
            'mobile records preserve headers':'[data-table-responsive="records"] thead{position:absolute;' in css and 'clip-path:inset(50%)' in css,
            'mobile records stack cells':'[data-table-responsive="records"] :is(th,td){display:block;' in css,
            'desktop comparisons fit reading region':'[data-table-responsive="scroll"]{min-width:0!important}' in css}

def node_signature(node):
    from zo_course_editorial import inline_signature
    return {'inline':inline_signature(node),'links':[[a.get('href'),a.get_text(' ',strip=True)] for a in node.select('a[href]')], 'ids':[n['id'] for n in node.select('[id]')], 'disclosures':[[n.get('id'),n.has_attr('open')] for n in node.select('details')]}

def same_node_signature(actual,expected):
    """Pandoc may wrap link labels differently in fragments and full pages."""
    def canonical(value):
        value=copy.deepcopy(value)
        value['links']=[[href,re.sub(r'\s+',' ',label).strip()] for href,label in value.get('links',[])]
        return value
    return canonical(actual)==canonical(expected)

def restore_g01_for_comparison(source,plan,qmd):
    from zo_course_editorial import sha,inline_signature
    change=plan.get('table_function_transition')
    if not change:return source
    if change.get('id')!=RULE or change.get('historical_comparison_only') is not True or sha(Path(qmd).read_bytes())!=change.get('source_qmd_sha256'):raise ValueError('Stale table-function source binding')
    result=copy.deepcopy(source)
    for edit in change['edits']:
        nodes=result.find_all(id=edit['id']) if edit.get('id') else [n for n in result.find_all(edit['tag']) if inline_signature(n)==edit['after_signature']['inline']]
        if len(nodes)!=1 or not same_node_signature(node_signature(nodes[0]),edit['after_signature']):raise ValueError('Changed/duplicate table-function block: '+str(edit.get('id') or edit['tag']))
        old=BeautifulSoup(edit['before_html'],'html.parser').find(edit['tag'])
        if edit.get('id'):
            nodes[0].replace_with(copy.deepcopy(old))
        else:
            # A full Quarto page can move a heading ID to its section wrapper,
            # while a Pandoc fragment leaves that ID on the heading itself.
            # These edits change prose only, so retain the current wrapper
            # attributes and restore just the historical child content.
            nodes[0].clear()
            for child in list(old.contents):nodes[0].append(copy.deepcopy(child))
    return result

def source_node(source,ident,plan):
    edits=[e for e in plan.get('table_function_transition',{}).get('edits',[]) if e.get('id')==ident]
    nodes=source.find_all(id=ident)
    if len(edits)!=1 or len(nodes)!=1 or not same_node_signature(node_signature(nodes[0]),edits[0]['after_signature']):raise ValueError('Unbound/changed current table-function node: '+ident)
    return copy.deepcopy(nodes[0])

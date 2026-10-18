"""Source-owned bottleneck tables; structure/coverage binding is not pedagogical acceptance."""
from pathlib import Path
import copy,json,re
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[1]
RULE='BOTTLENECKS-20261019'
CONTRACT='bottlenecks-v1'
HEADERS=['Nút thắt nhận thức','Biểu hiện dễ nhầm','Câu hỏi và cách tháo gỡ','Tự kiểm tra']

def governed(path):
    p=Path(path)
    return p.name=='index.qmd' and p.parent.parent.name=='hoc_lieu' and bool(re.fullmatch(r'r\d+_g\d+',p.parent.name))

def source_checks(path,root=ROOT,text=None):
    path=Path(path);root=Path(root)
    if not governed(path):return {}
    c={}
    try:
        text=path.read_text(encoding='utf-8') if text is None else text
        binding=json.loads((path.parent/'giao_dien/he_nhan.json').read_text(encoding='utf-8')).get('remediation',{})
        c['remediation declared for package']=binding.get('contract')==CONTRACT
        ident=binding.get('table','')
        m=re.search(r'(?m)^(:{3,}) \{#'+re.escape(ident)+r'[^\n]*\}\n.*?^\1[ \t]*$',text,re.S|re.M) if ident else None
        c['one source-owned bottleneck table']=bool(m) and text.count('data-zo-remediation="'+CONTRACT+'"')==1
        if not m:return c
        owners=re.findall(r'(?m)^## ([^\n]+)',text[:m.start()])
        c['table within Sửa lỗi']=bool(owners) and owners[-1].startswith('Sửa lỗi {#sua-loi}')
        lines=[x for x in m[0].splitlines() if x.startswith('|')]
        cells=[[s.strip() for s in x.strip('|').split('|')] for x in lines]
        c['four shared columns']=bool(cells) and cells[0]==HEADERS and all(len(r)==4 for r in cells)
        actual=cells[2:];expected=binding.get('rows',[])
        c['reviewed row coverage and order']=[r[0] for r in actual]==[r['title'] for r in expected] and bool(expected)
        c['unique bottlenecks']=len({r[0] for r in actual})==len(actual)
        from zo_course_editorial import closure
        alltext='\n'.join(closure(path,root,text).values())
        anchors=set(re.findall(r'\{#([^\s}]+)',alltext))|set(re.findall(r'\bid=["\']([^"\']+)',alltext))
        for n,(r,e) in enumerate(zip(actual,expected),1):
            if len(r)!=4:continue
            c[f'row {n} explains a distinction']=all(v.strip() for v in r) and '?' in r[2] and not re.search(r'\bbẫy\b',r[0]+' '+r[1],re.I)
            knowledge=re.findall(r'\]\(#([^)]*)\)',r[2]);routes=re.findall(r'\]\(#([^)]*)\)',r[3])
            c[f'row {n} reviewed knowledge links']=set(knowledge)==set(e['knowledge_anchors']) and bool(knowledge)
            c[f'row {n} reviewed task routes']=set(routes)==set(e['route_anchors'])
            c[f'row {n} link targets exist']=all(unquote(a) in anchors for a in knowledge+routes)
            c[f'row {n} route or explicit gap']=bool(routes) or 'Chưa có bài Sửa lỗi riêng' in r[3]
        c['three contexts explicit']=all(s in m[0] for s in ['Sau Luyện tập','Sau Kiểm tra','Sau Ôn lại'])
    except (OSError,ValueError,KeyError) as exc:c['remediation readable: '+str(exc)]=False
    return c

def html_checks(doc):
    c={}
    for frame in doc.select('[data-zo-remediation]'):
        ident=frame.get('id','');ts=frame.select('table')
        c[ident+' one visible table']=len(ts)==1 and not frame.find_parent('details')
        if len(ts)!=1:continue
        table=ts[0];rows=table.select('tr')
        c[ident+' shared headings']=[x.get_text(' ',strip=True) for x in rows[0].find_all(['th','td'],recursive=False)]==HEADERS
        c[ident+' four columns']=all(len(r.find_all(['th','td'],recursive=False))==4 for r in rows)
        c[ident+' shared table style']=table.get('data-table-kind')=='process' and table.get('data-table-variant')=='routing'
    return c

def restore_g01_for_comparison(source,plan,qmd):
    from zo_course_editorial import restore_g01_for_comparison as restore,RULE as EDITORIAL_RULE
    change=plan.get('remediation_transition')
    if not change:return source
    if change.get('id')!=RULE:raise ValueError('Unknown remediation transition')
    proxy=copy.deepcopy(plan);proxy['editorial_transition']=dict(change,id=EDITORIAL_RULE)
    return restore(source,proxy,qmd)

def source_node(source,ident,plan):
    """Copy fresh QMD payload; never emit historical comparison markup."""
    from zo_course_editorial import inline_signature
    allowed='r1-table-t12'
    if ident!=allowed:raise ValueError('Unreviewed source component')
    matches=source.find_all(id=ident)
    if len(matches)!=1:raise ValueError('Missing or duplicate remediation component')
    edits=plan.get('remediation_transition',{}).get('edits',[])
    if len(edits)!=1 or inline_signature(matches[0])!=edits[0]['after_signature']:raise ValueError('Remediation component differs from reviewed source')
    return copy.deepcopy(matches[0])

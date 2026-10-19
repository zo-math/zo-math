"""Course-wide terminology/readability gate and bounded G01 source revision.

QMD owns learner prose. Rules live in 07 and its lexical profile; the review
ledger binds an actual editorial pass to its sources, never to owner acceptance.
No renderer and no automatic rewrite or review/hash renewal.
"""
from pathlib import Path
from collections import defaultdict
import copy,hashlib,json,re
from bs4 import BeautifulSoup,Comment,NavigableString

ROOT=Path(__file__).resolve().parents[1]
COURSE=Path('content/thpt/on_thi_toan_thpt')
POLICY=Path('_design/web_2027_mau_dung_chung/profiles/editorial-language.json')
RULE='EDITORIAL-20261018'
norm=lambda s:re.sub(r'\s+',' ',s).strip()
sha=lambda x:hashlib.sha256(x if isinstance(x,bytes) else x.encode('utf-8')).hexdigest()

def governed(path):
    p=Path(path)
    return p.name in {'index.qmd','index.html'} and (p.parent.name=='2027' and p.parent.parent.name=='tot_nghiep_thpt' or p.parent.parent.name=='hoc_lieu' and (p.parent.name=='d0' or re.fullmatch(r'r[1-9]\d*_g\d+',p.parent.name)))

def policy(root=ROOT):return json.loads((Path(root)/POLICY).read_text(encoding='utf-8'))

def learner_lines(text):
    """Strip technical IDs/URLs/math/code, retaining headings, captions and alt.

    Only learner-facing YAML values are inspected; paths and management fields
    are not prose. An old word in a stable ID is not an editorial regression.
    """
    yaml=False;code=False
    for n,line in enumerate(text.splitlines(),1):
        if n==1 and line.strip()=='---':yaml=True;continue
        if yaml:
            if line.strip()=='---':yaml=False;continue
            if not re.match(r'\s*(?:title|subtitle|label|description):',line):continue
        if re.match(r'^\s*```',line):code=not code;continue
        if code or line.lstrip().startswith((':::','{{<','<!--')):continue
        s=re.sub(r'\]\([^\n)]*\)|\{#[^\n}]*\}|\b(?:id|href|src|data-[\w-]+)=["\'][^"\']*["\']','',line)
        s=re.sub(r'\$\$.*?\$\$|(?<!\\)\$[^$\n]*\$|`[^`]*`','',s)
        s=re.sub(r'<[^>]+>','',s)
        yield n,s

def scan(text,root=ROOT,raw=False):
    p=policy(root);issues=[]
    rows=enumerate(text.splitlines(),1) if raw else learner_lines(text)
    for line,body in rows:
        for allowed in p['allowed_mien']:body=re.sub(allowed,'',body,flags=re.I)
        for rule in p['rules']:
            if re.search(rule['pattern'],body,re.I):issues.append({'line':line,'rule':rule['id'],'message':rule['message']})
    return issues

def closure(path,root=ROOT,override=None):
    root=Path(root).resolve();out={}
    def visit(p):
        p=p.resolve()
        if not p.is_relative_to(root/COURSE):raise ValueError('Editorial include escapes course: '+str(p))
        if p in out:return
        s=override if p==Path(path).resolve() and override is not None else p.read_text(encoding='utf-8')
        out[p]=s
        for inc in re.findall(r'\{\{<\s*include\s+([^>]+?)\s*>\}\}',s):visit(p.parent/inc.strip().strip('"'))
    visit(Path(path));return out

def dependent_checks(path,review,root=ROOT):
    """Catalog data and display titles are source, not invisible exceptions."""
    root=Path(root);path=Path(path);checks={};dependent=[]
    if path.parent.name=='2027':dependent=[path.parent/'_data/chuong_trinh.yml']
    elif path.parent.name!='d0':dependent=[path.parent/'giao_dien/he_nhan.json']
    fields={'title','label','description','summary','subtitle'}
    def values(node):
        if isinstance(node,dict):
            for key,value in node.items():
                if key in fields and isinstance(value,str):yield value
                elif isinstance(value,(dict,list)):yield from values(value)
        elif isinstance(node,list):
            for value in node:yield from values(value)
    for p in dependent:
        relative=p.relative_to(root).as_posix()
        if p.suffix=='.json':data=json.loads(p.read_text(encoding='utf-8'))
        else:
            import yaml
            data=yaml.safe_load(p.read_text(encoding='utf-8'))
        checks[relative+' reviewed data/title source current']=review.get('dependent_sources',{}).get(relative)==sha(p.read_bytes())
        checks[relative+' visible metadata terminology']=not scan('\n'.join(values(data)),root,raw=True)
    return checks

def source_checks(path,root=ROOT,text=None):
    if not governed(path):return {}
    root=Path(root);checks={}
    try:
        p=policy(root);review=json.loads((root/p['review']).read_text(encoding='utf-8'))
        checks['current editorial policy']=p['id']==review.get('decision')==RULE
        checks['editorial review is source-only']=review.get('status')=='source_reviewed_not_rendered' and review.get('owner_HTML_acceptance') is False
        checks.update(dependent_checks(path,review,root))
        for source,s in closure(path,root,text).items():
            relative=source.relative_to(root).as_posix()
            issues=scan(s,root)
            checks[relative+' no rejected terminology or shorthand']=not issues
            if issues:
                for issue in issues:checks[relative+':'+str(issue['line'])+' '+issue['rule']]=False
            current=source.read_bytes() if text is None or source!=Path(path).resolve() else s.replace('\n','\r\n').encode('utf-8') if b'\r\n' in source.read_bytes() else s.encode('utf-8')
            checks[relative+' reviewed source current']=review.get('sources',{}).get(relative)==sha(current)
    except (OSError,ValueError,KeyError) as exc:checks['editorial source readable: '+str(exc)]=False
    return checks

def html_checks(document,root=ROOT):
    source=document.select_one('.reader-content') or document.select_one('.course-home') or document.select_one('.home-page')
    if source is None:source=document.body
    if source is None:return {'learner content exists':False}
    clone=copy.deepcopy(source)
    for n in clone.select('script,style,math,pre,code'):n.decompose()
    return {'rendered learner terminology and instructions':not scan(clone.get_text('\n',strip=True),root,raw=True)}

def require(checks,label='editorial language'):
    failed=[k for k,v in checks.items() if not v]
    if failed:raise ValueError(label+': '+'; '.join(failed))

def inline_signature(node):
    """Same leaf text/TeX keys as the source-owned G01 layout, ignoring wrappers."""
    if isinstance(node,Comment):return []
    if isinstance(node,NavigableString):return [['text',sha(norm(str(node)))]] if norm(str(node)) else []
    if node.name=='math':
        a=node.select_one('annotation[encoding="application/x-tex"]')
        if a is None:raise ValueError('G01 comparison math lacks its source annotation')
        return [['math',sha(norm(a.get_text()))]]
    return [entry for child in node.children for entry in inline_signature(child)]

def restore_g01_for_comparison(source,plan,qmd):
    """Inverse ONLY enumerated approved prose blocks on a detached tree.

    The original complete fingerprint and accepted receipt remain unchanged.
    Exact new text/TeX leaf keys and counts must match before historical nodes
    are restored for comparison. Old markup is NEVER used for learner output.
    """
    change=plan.get('editorial_transition')
    if not change:return source
    if change.get('id')!=RULE or change.get('historical_comparison_only') is not True or sha(Path(qmd).read_bytes())!=change.get('source_qmd_sha256'):
        raise ValueError('G01 editorial transition differs from its current source')
    for path,digest in change['sources'].items():
        # The current full-QMD binding above is strict. This duplicated entry
        # records the older editorial stage, before later bounded transitions;
        # it is not a second current-source binding. Independent includes stay strict.
        if (ROOT/path).resolve()==Path(qmd).resolve():continue
        if sha((ROOT/path).read_bytes())!=digest:raise ValueError('G01 edited include changed after review: '+path)
    result=copy.deepcopy(source);groups=defaultdict(list)
    for edit in change['edits']:groups[(edit['tag'],json.dumps(edit['after_signature']))].append(edit)
    # Collect matches before modifying any node, so parent/sibling relationships
    # cannot allow one edit to consume another edited block.
    replacements=[]
    for (tag,key),edits in groups.items():
        expected=json.loads(key);nodes=[n for n in result.find_all(tag) if inline_signature(n)==expected]
        if len(nodes)!=len(edits):raise ValueError('G01 edited block missing/changed/duplicated: '+edits[0]['source']+':'+str(edits[0]['line_before']))
        replacements.extend(zip(nodes,edits))
    for node,edit in replacements:
        old=BeautifulSoup(edit['before_html'],'html.parser').find(edit['tag'])
        if old is None:raise ValueError('Invalid historical G01 comparison block')
        node.replace_with(copy.deepcopy(old))
    return result

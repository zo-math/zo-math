"""Validate the current G04 revision, preserving historical manuscript receipts."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import argparse,copy,hashlib,json,re,subprocess
from bs4 import BeautifulSoup
import sympy as s
from zo_web_2027_g04 import PACKAGE,ROLES
from zo_web_2027_preview import REPO
from zo_web_2027_g02 import canonical_math_matches
from zo_math_notation import math_errors
from zo_course_editorial import source_checks as editorial
from zo_course_labels import source_checks as labels,html_checks as html_labels
from zo_course_math_assets import source_checks as assets,html_checks as html_assets

def checks():
    source=REPO/PACKAGE/'index.qmd';text=source.read_text('utf-8');page=REPO/'docs'/PACKAGE/'index.html'
    doc=BeautifulSoup(page.read_text('utf-8'),'html.parser');root=doc.select_one('.reader-content');b=json.loads((source.parent/'giao_dien/he_nhan.json').read_text('utf-8'))
    result={};details={}
    for name,items in [('editorial',editorial(source)),('labels',labels(source)),('HTML labels',html_labels(doc,b)),('assets',assets(source)),('HTML assets',html_assets(doc,'r1_g04'))]:
        result[name]=all(items.values());details[name]={'passed':sum(items.values()),'total':len(items),'failures':[k for k,v in items.items() if not v]}
    result['notation']=not math_errors(text)
    prose=copy.deepcopy(root)
    # Native BBT mathematics is JSON-owned and checked cell by cell above.
    # Compare QMD-authored mathematics separately, without counting it twice.
    for table in prose.select('table.zo-variation-native'):table.decompose()
    result['source mathematics preserved in HTML']=canonical_math_matches(source,prose)
    ids=[n['id'] for n in doc.select('[id]')];result['unique IDs']=len(ids)==len(set(ids))
    result['ten learning areas']=all(root.find(id=i) for i in ROLES)
    lesson=root.find(id='bai-hoc')
    result['lesson navigation container and declared section count']=bool(lesson.select_one('.lesson-toc')) and len(lesson.select(':scope > section.level3'))==int(root['data-r1-lesson-count'])
    result['feedback initially closed']=not root.select('details[open]')
    result['four foundation cards']=len(root.select('details.r1-foundation-unit'))==4
    result['task numbering 1 through 32']=sorted(int(n['data-zo-number']) for n in root.select('[data-zo-type="task"][data-zo-number]:not([data-zo-function="function.guided_thinking"])'))==list(range(1,33))
    result['five knowledge units retained']=len(re.findall(r'^### [1-5]\. ',text,re.M))==5
    result['no audit executable dependency']='_audit/' not in str(doc) and '_quy_trinh/ban_thao/' not in str(doc)
    result['isolated G04 runtime']=any('g04_revision_r01/' in a.get('href','') for a in doc.select('link'))
    result['eight old PDF versions labelled']=len(root.select('.zo-pdf-card[data-pdf-current="false"]'))==8 and 'chưa phản ánh bản sửa R01' in root.select_one('.zo-pdf-current-note').get_text()
    for n,(suffix,owner) in enumerate(zip(['domain','derivative','limits','division'],['nen-mien','nen-dao-ham','nen-gioi-han','nen-chia']),1):
        complete=root.find(id='g04-completion-'+suffix);task=root.find(id=f'N{n}-Q')
        result[f'foundation {n} completion then independent question']=bool(complete and complete.find_parent(id=owner) and task and task.find_parent(id=owner) and task.find('details') and not task.find('details').has_attr('open'))
    for n in range(1,4):
        answer=root.find(id=f'lg-O0{n}').find('details')
        result[f'review {n} criteria in answer']=bool(answer and 'Sau khi tự làm' in answer.get_text() and answer.select_one('a[href="#S05"],a[href="#S06"]'))
    result['review does not prescribe findings']='không có cực trị' not in root.find(id='on-lai').get_text() and 'không lấy' not in root.find(id='O02').get_text()
    journal=root.find(id='nhat-ky');full=journal.find(id='g04-journal-full')
    result['four short journal prompts']=len(journal.select_one('ol').find_all('li',recursive=False))==4
    result['fourteen full fields optional']=bool(full and not full.has_attr('open') and len(full.select('#r1-table-t13 tbody tr'))==14)
    result['journal uses correct practice-stage route']=bool(journal.select_one('a[href="#L03"]') and journal.select_one('a[href="#S02"]') and journal.select_one('a[href="#CP01"]'))
    # Verify that original figures and native variation tables remain complete.
    manifest=json.loads((source.parent/'giao_dien/hinh_manifest.json').read_text('utf-8'))
    result['original vector hashes retained']=all(hashlib.sha256((source.parent/f[k]).read_bytes()).hexdigest()==f[k+'_sha256'] for f in manifest['figures'] for k in ['input','svg','pdf'])
    baseline=subprocess.run(['git','show','e493dff:'+str(PACKAGE/'index.qmd').replace('\\','/')],cwd=REPO,check=True,capture_output=True).stdout.decode('utf-8')
    oldimgs=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',baseline);newimgs=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',text)
    result['original figure occurrences plus one VD04 reuse']=sorted(newimgs)==sorted(oldimgs+['giao_dien/assets/figures_0_4/VD04.svg'])
    result['original native BBT anchors retained']=re.findall(r'data-bbt="([^"]+)"',baseline)==re.findall(r'data-bbt="([^"]+)"',text)
    # Preserve mathematics of original questions outside the deliberately revised review instructions.
    def block(raw,anchor):
        m=re.search(r'^(#{3,5}) [^\n]*\{#'+anchor+r'(?:[ }])[^\n]*\n',raw,re.M)
        if not m:return ''
        tail=raw[m.end():];end=re.search(r'^#{1,'+str(len(m[1]))+r'} ',tail,re.M)
        return tail[:end.start()] if end else tail
    formula=lambda t:re.findall(r'\$\$[\s\S]*?\$\$|(?<!\$)\$(?!\$)[^$]*\$',t)
    originals=[u for u in b['units'] if u['function'] not in ['function.foundation_confirmation','function.guided_thinking','function.review']]
    result['original practice and test mathematics retained']=all(formula(block(baseline,u['question']))==formula(block(text,u['question'])) for u in originals)
    broken=[];cache={page:doc}
    for node in doc.select('a[href],img[src],script[src],link[href]'):
        url=urlsplit(node.get('src',node.get('href','')))
        if url.scheme or url.netloc:continue
        target=(page.parent/unquote(url.path)).resolve() if url.path else page
        if not target.is_file():broken.append(node.get('src',node.get('href')));continue
        if url.fragment and target.suffix=='.html':
            if target not in cache:cache[target]=BeautifulSoup(target.read_text('utf-8'),'html.parser')
            if not cache[target].find(id=unquote(url.fragment)):broken.append(node.get('href'))
    result['local files and anchors resolve']=not broken;details['broken_links']=broken
    x=s.symbols('x',real=True);math=[]
    def v(name,actual,expected):
        ok=(actual==expected) if actual in [s.oo,-s.oo] or expected in [s.oo,-s.oo] else s.simplify(actual-expected)==0
        math.append(dict(check=name,actual=str(actual),expected=str(expected),passed=bool(ok)))
    for name,f,g,a,b0 in [('domain worked',(x*x-16)/(x-4),x+4,4,8),('domain completion',(x*x-2*x-15)/(x-5),x+3,5,8),('domain independent',(x*x+x-12)/(x+4),x-3,-4,-7)]:
        v(name+' identity',s.cancel(f)-g,0);v(name+' hole limit',s.limit(f,x,a),b0)
    v('domain independent ordinate',((x*x+x-12)/(x+4)).subs(x,0),-3)
    for name,f,d in [('quotient worked',(2*x+3)/(x-2),-7/(x-2)**2),('quotient completion',(x+4)/(x-3),-7/(x-3)**2),('quotient independent',(4*x-7)/(x-3),-5/(x-3)**2),('negative remainder independent',x+1-9/(x+2),1+9/(x+2)**2)]:v(name,s.diff(f,x),d)
    for name,f,a,left,right,end in [('limits worked',2+3/(x-1),1,-s.oo,s.oo,2),('limits completion',(3*x-11)/(x-4),4,-s.oo,s.oo,3),('limits independent',4-6/(x-2),2,s.oo,-s.oo,4)]:
        v(name+' left',s.limit(f,x,a,dir='-'),left);v(name+' right',s.limit(f,x,a,dir='+'),right)
        for lim in [-s.oo,s.oo]:v(name+' end '+str(lim),s.limit(f,x,lim),end)
    v('q derivative',s.diff(4-6/(x-2),x),6/(x-2)**2);v('q ordinate',(4-6/(x-2)).subs(x,0),7)
    A=6+40/x;v('model derivative',s.diff(A,x),-40/x**2);v('model maximum',A.subs(x,4),16);v('model minimum',A.subs(x,10),10)
    for name,num,den,q,r in [('division worked',x*x+2*x+8,x+2,x,8),('division completion',x*x-2*x+7,x-1,x-1,6),('division independent',x*x-4*x+10,x-2,x-2,6)]:
        v(name+' reconstruction',s.expand(q*den+r),num)
        for lim in [-s.oo,s.oo]:v(name+' difference '+str(lim),s.limit(num/den-q,x,lim),0)
    v('division independent left',s.limit((x*x-4*x+10)/(x-2),x,2,dir='-'),-s.oo)
    v('division independent right',s.limit((x*x-4*x+10)/(x-2),x,2,dir='+'),s.oo)
    result['new independent mathematical checks']=all(m['passed'] for m in math)
    details.update(figures_before=len(oldimgs),figures_after=len(newimgs),native_BBT=len(re.findall(r'data-bbt=',text)))
    return dict(checks=result,passed=sum(result.values()),total=len(result),details=details,mathematics=math,math_total=len(math),owner_acceptance=False)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();out=checks();args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({k:out[k] for k in ['passed','total','math_total']}));print('Failures:',[k for k,v in out['checks'].items() if not v]);print('Details:',{k:v for k,v in out['details'].items() if isinstance(v,dict) and v.get('failures')})
    raise SystemExit(int(out['passed']!=out['total']))

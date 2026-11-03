"""Check the revised G03's learning boundaries and new mathematics; no rendering."""
from pathlib import Path
from urllib.parse import unquote,urlsplit
import argparse,hashlib,json,re
from bs4 import BeautifulSoup
import sympy as s
from zo_web_2027_g03 import PACKAGE,ROLES
from zo_web_2027_preview import REPO
from zo_web_2027_g02 import canonical_math_matches
from zo_math_notation import math_errors
from zo_course_editorial import source_checks
from zo_course_labels import source_checks as label_source_checks

def checks():
    source=REPO/PACKAGE/'index.qmd';text=source.read_text(encoding='utf-8')
    page=REPO/'docs'/PACKAGE/'index.html';doc=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
    root=doc.select_one('.reader-content');result={}
    result['source editorial checks']=all(source_checks(source).values())
    result['source label checks']=all(label_source_checks(source).values())
    result['notation and delimiters']=not math_errors(text)
    result['current mathematics preserved in HTML']=canonical_math_matches(source,root)
    ids=[n['id'] for n in doc.select('[id]')]
    result['unique HTML IDs']=len(ids)==len(set(ids))
    result['all learning areas present']=all(root.find(id=i) for i in ROLES)
    result['all feedback initially closed']=not root.select('details[open]')
    result['three foundation cards retained']=len(root.select('details.r1-foundation-unit'))==3
    result['no executable audit dependency']='_audit/' not in str(doc) and '_quy_trinh/ban_thao/' not in str(doc)
    result['task sequence 1 to 46']=sorted(int(n['data-zo-number']) for n in root.select('[data-zo-type="task"][data-zo-number]:not([data-zo-function="function.guided_thinking"])'))==list(range(1,47))
    result['six knowledge sections retained']=len(re.findall(r'^### [1-6]\. ',text,re.M))==6
    result['same eleven lesson figures']=len(root.select('img.zo-graph-04'))==11
    result['all local anchors resolve']=all(unquote(a['href'][1:]) in ids for a in root.select('a[href^="#"]'))
    result['isolated G03 runtime used']=any('g03_revision_r01/' in n.get('href','') for n in doc.select('link[href]'))
    result['eight old PDF downloads labelled']=len(root.select('.zo-pdf-card[data-pdf-current="false"]'))==8 and 'chưa phản ánh bản sửa R01' in root.select_one('.zo-pdf-current-note').get_text()
    for suffix in ['sign','infinity','radical','domain','division']:
        node=root.find(id='g03-completion-'+suffix)
        result['completion belongs to foundation '+suffix]=bool(node and node.find_parent('details',class_='r1-foundation-unit') and not node.has_attr('open'))
    review=root.find(id='on-lai')
    result['no advance review criteria']=not any(cue in review.get_text(' ',strip=True) for cue in ['Lỗi cần quan sát:','Mục tiêu:','giới hạn hữu hạn với vô cực','giới hạn hiệu bằng'])
    for i in range(1,4):
        node=root.find(id=f'lg-O0{i}').find('details')
        result[f'review {i} criteria and routes in closed answer']=bool(node and 'Sau khi tự làm' in node.get_text() and node.select_one('a[href="#S-O01"],a[href="#S-O02"],a[href="#sua-sau-on"]'))
    journal=root.find(id='nhat-ky');full=journal.find(id='g03-journal-full')
    result['short journal has four prompts']=len(journal.select_one('ol').find_all('li',recursive=False))==4
    result['full journal stays optional']=bool(full and not full.has_attr('open') and full.find(id='g03-table-12') and full.find(id='g03-table-13'))
    result['journal plans a phase-appropriate new task']='Nhiệm vụ 13' in journal.get_text() and 'Nhiệm vụ 35' in journal.get_text() and 'Điểm dừng 02' in journal.get_text()
    k03=root.find(id='K03').get_text(' ',strip=True)
    result['test 25 does not prescribe division']='tách phân thức' not in k03 and 'cần đủ hai hệ số' not in k03
    # Independent calculations of all new numerical conclusions, including signs.
    x=s.symbols('x',real=True);math=[]
    def verify(name,actual,expected):
        ok=s.simplify(actual-expected)==0 if actual not in [s.oo,-s.oo] and expected not in [s.oo,-s.oo] else actual==expected
        math.append({'check':name,'actual':str(actual),'expected':str(expected),'passed':bool(ok)})
    for direction in ['-','+']:verify('completion square '+direction,s.limit(-3/(x-2)**2,x,2,dir=direction),-s.oo)
    verify('task31 negative numerator left',s.limit(-2/(x+4),x,-4,dir='-'),s.oo)
    verify('task31 negative numerator right',s.limit(-2/(x+4),x,-4,dir='+'),-s.oo)
    verify('task31 allowed right direction',s.limit(-5/(x-1)**2,x,1,dir='+'),-s.oo)
    for end in [s.oo,-s.oo]:
        verify('completion degree2 '+str(end),s.limit((2*x*x-3)/(x*x+4*x),x,end),2)
        verify('task32 equal degrees '+str(end),s.limit((5*x-1)/(2*x+3),x,end),s.Rational(5,2))
        verify('task32 unequal degrees '+str(end),s.limit((2*x-1)/(x*x+3),x,end),0)
        sign=1 if end==s.oo else -1
        verify('root example '+str(end),s.limit(s.sqrt(x*x+2)/x,x,end),sign)
        verify('root completion '+str(end),s.limit(s.sqrt(4*x*x+1)/x,x,end),2*sign)
        verify('root independent '+str(end),s.limit(s.sqrt(x*x+4)/x,x,end),sign)
    for a in [3,4,5]:
        verify('cancel identity '+str(a),s.cancel((x*x-a*a)/(x+a))-(x-a),0)
        verify('cancel limit '+str(a),s.limit((x*x-a*a)/(x+a),x,-a),-2*a)
    for name,numerator,denominator,q,r in [('division model',x*x+2*x+5,x+1,x+1,4),('division completion',x*x+x+5,x-2,x+3,11),('division independent',x*x-2*x+5,x-1,x-1,4)]:
        verify(name,s.expand(denominator*q+r)-numerator,0)
    verify('test25 score sum',s.Rational(1,2)+2+1+s.Rational(3,2),5)
    result['independent new mathematical checks']=all(v['passed'] for v in math)
    # The original G03 figure manifest remains the authority; do not regenerate vectors.
    manifest=json.loads((REPO/PACKAGE/'giao_dien/hinh_manifest.json').read_text(encoding='utf-8'))
    result['all original vectors unchanged']=all(hashlib.sha256((REPO/PACKAGE/f[k]).read_bytes()).hexdigest()==f[k+'_sha256'] for f in manifest['figures'] for k in ['input','svg','pdf'])
    return {'checks':result,'passed':sum(result.values()),'total':len(result),'mathematics':math,'math_total':len(math),'owner_acceptance':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    report=checks();args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['passed','total','math_total']},ensure_ascii=False));print('Failures:',[k for k,v in report['checks'].items() if not v])
    raise SystemExit(0 if report['passed']==report['total'] else 1)

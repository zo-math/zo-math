"""Read-only draft checks, with a report in this package's evidence folder."""
from pathlib import Path
import re,json,hashlib,sys,subprocess
import sympy as S
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/zo_python.py').is_file())
Q=Path(__file__).resolve().parent.parent;D=Q/'ban_thao/noi_dung.md'
sys.path.insert(0,str(ROOT/'scripts'))
from zo_latex_delimiters import delimiter_errors
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=D.read_text(encoding='utf-8');checks=[];errors=[]
def check(name,condition,detail=''):
 checks.append({'check':name,'passed':bool(condition),'detail':detail})
 if not condition:errors.append(name+': '+str(detail))
ids=re.findall(r'<a id="([^"]+)"></a>',s)
check('anchors_unique',len(ids)==len(set(ids)),len(ids))
for stem,n in [('nv',29),('lg',29),('gm',8),('vd',8),('cp',8)]:
 check(stem+'_sequence',all(f'{stem}-{i:02}' in ids for i in range(1,n+1)),n)
for i in range(1,30):
 check(f'solution_return_{i:02}',f'[Xem đề bài](#nv-{i:02})' in s)
 check(f'solution_forward_{i:02}',f'[Xem lời giải](#lg-{i:02})' in s)
links=re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',s)
for link in links:
 path,_,anchor=link.partition('#')
 target=(D.parent/path).resolve() if path else D
 if '://' in path:continue
 check('link:'+link,target.is_file())
 if anchor and target.is_file():
  target_text=target.read_text(encoding='utf-8-sig')
  check('anchor:'+link,anchor in re.findall(r'id="([^"]+)"',target_text) or bool(re.search(r'\{#'+re.escape(anchor)+r'(?:[ }])',target_text)))
formulas=re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',s,re.S)
for i,parts in enumerate(formulas):
 formula=next(x for x in parts if x)
 errs=delimiter_errors(formula)
 check('latex_'+str(i),not errs,errs)
check('no_placeholders',not any(x in s for x in ['CẦN VIẾT','CẦN ĐIỀN','TODO','Chưa điền']))
check('unique_draft',len(list(Q.rglob('noi_dung.md')))==1)
check('no_forbidden_outputs',not any(p.suffix.lower() in {'.qmd','.html','.pdf'} for p in Q.parent.rglob('*') if p.is_file()))
check('goals_once',s.count('### Học xong, em cần làm được gì?')==1)
check('guiding_question_closed','<details>\n<summary>Câu hỏi dẫn đường</summary>' in s and '<details open' not in s)
check('guided_inside_lesson',all(s.index('id="bai-hoc"')<s.index(f'id="gm-{i:02}"')<s.index('id="luyen-tap"') for i in range(1,9)))
# Independent symbolic and exhaustive integer checks against the authored claims.
x=S.symbols('x',positive=True)
for label,L,W,opt,value in [('vd05',30,30,5,2000),('nv17',32,20,4,1152)]:
 V=x*(L-2*x)*(W-2*x);dp=S.diff(V,x)
 check(label+'_critical',S.simplify(dp.subs(x,opt))==0)
 check(label+'_value',V.subs(x,opt)==value)
 roots=S.solve(dp,x);feasible=[r for r in roots if 0<r<min(L,W)/2]
 check(label+'_unique_interior',feasible==[S.Integer(opt)],str(feasible))
for label,a,b,N,winner,value in [('vd07',10,61,6,3,S.Rational(151,3)),('nv15',8,50,8,3,S.Rational(122,3)),('nv20',6,40,7,3,S.Rational(94,3)),('nv25',5,31,6,3,S.Rational(76,3)),('nv27',3,19,6,3,S.Rational(46,3)),('nv29',1,13,8,4,S.Rational(29,4))]:
 vals={n:a*n+S.Rational(b,n) for n in range(1,N+1)};best=min(vals.values())
 check(label+'_integer_exhaustive',[n for n,v in vals.items() if v==best]==[winner] and best==value,str(vals))
for label,L,m,xbest,ybest,area in [('nv10',30,2,S.Rational(15,2),15,S.Rational(225,2)),('nv11',48,2,12,24,288),('nv24',36,2,9,18,162),('nv26',60,3,10,30,300)]:
 A=x*(L-m*x);check(label+'_geometry',S.diff(A,x).subs(x,xbest)==0 and L-m*xbest==ybest and A.subs(x,xbest)==area)
for label,p0,step,q0,growth,cost,fixed,N,best,profit in [('vd04',50,1,100,5,10,400,20,10,4100),('nv07',50,1,100,5,10,400,6,6,4020),('nv12',40,2,80,10,12,240,8,3,2180),('nv19',60,2,60,5,20,300,3,3,2250),('nv22',100,-5,12,-1,20,100,11,0,860),('nv28',30,1,40,4,10,80,4,4,816)]:
 vals={k:(p0-step*k-cost)*(q0+growth*k)-fixed for k in range(N+1)}
 check(label+'_profit_exhaustive',max(vals,key=vals.get)==best and vals[best]==profit,str(vals))
for label,a,b,c,n,total,avg,der,delta in [('vd02',S.Rational(1,50),4,100,50,350,7,6,S.Rational(301,50)),('nv18',S.Rational(1,10),5,80,20,220,11,9,S.Rational(91,10)),('nv24',S.Rational(1,20),2,60,10,85,S.Rational(17,2),3,S.Rational(61,20)),('nv27',S.Rational(1,4),6,40,8,104,13,10,S.Rational(41,4))]:
 C=a*x*x+b*x+c
 check(label+'_marginal',C.subs(x,n)==total and C.subs(x,n)/n==avg and S.diff(C,x).subs(x,n)==der and S.expand(C.subs(x,n+1)-C.subs(x,n))==delta)
for label,s,a,b,t,average,v,acc in [('nv04',x*x+2*x,0,2,2,4,6,2),('nv14',x**3-3*x*x+4*x,1,2,2,2,4,6),('nv23',12*x-x*x,2,4,4,6,4,-2),('nv29',2*x*x+x,1,2,2,7,9,4)]:
 check(label+'_motion',(s.subs(x,b)-s.subs(x,a))/(b-a)==average and S.diff(s,x).subs(x,t)==v and S.diff(s,x,2).subs(x,t)==acc)
area=x*x+128/x;check('nv21_tank',S.diff(area,x).subs(x,4)==0 and area.subs(x,4)==48 and 32/S.Integer(4)**2==2)
check('nv13_average',S.diff(x/2+8+200/x,x).subs(x,20)==0 and (x/2+8+200/x).subs(x,20)==28)
check('nv05_units',(2*x*x+30*x+100).subs(x,2)*1000000/2000==84000)
base=json.loads((Q/'ho_so/tiep_nhan.json').read_text(encoding='utf-8'))
changes=[rel for rel,digest in base['protected_files'].items() if not (ROOT/rel).is_file() or sha(ROOT/rel)!=digest]
check('published_material_preserved',not changes,changes)
manifest=json.loads((Q/'ban_thao/hinh/manifest.json').read_text(encoding='utf-8'))
for name,digest in manifest['outputs'].items():check('asset_hash:'+name,sha(Q/'ban_thao/hinh'/name)==digest)
report={'draft_sha256':sha(D),'checks':checks,'passed':len(checks)-len(errors),'total':len(checks),'errors':errors,'protected_count':len(base['protected_files']),'limits':['Automated checks do not certify pedagogy or owner acceptance','No HTML/PDF or browser layout check','Shared architecture checker failures for old G01 kept in intake record']}
(Q/'ho_so/kiem_ban_thao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ['passed','total','errors','protected_count']},ensure_ascii=False))
raise SystemExit(bool(errors))

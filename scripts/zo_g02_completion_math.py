"""Scoped mathematical checks for new G02 foundation content and separated review.

Symbolic checks complement, not replace, reading the conditions/proofs in QMD.
"""
from pathlib import Path
import json
import sys
sys.dont_write_bytecode=True
import sympy as s
from zo_web_2027_preview import sha
ROOT=Path(__file__).resolve().parents[1]
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--output',default='_audit/zo_g02_completion_2026-10-08')
OUT=ROOT/parser.parse_args().output
x=s.symbols('x',real=True);positive=s.symbols('p',positive=True)
checks=[]
def equal(name,actual,expected):
    checks.append({'name':name,'passed':s.simplify(actual-expected)==0,'actual':str(actual),'expected':str(expected)})
equal('New domain confirmation: polynomial at excluded point',((x+3)**2).subs(x,-3),0)
equal('N-GH example upper witness gain',(x+2)/2-x,(2-x)/2)
equal('N-GH example lower witness gain',x-x/2,x/2)
equal('N-GH confirmation minimum at included endpoint',(4-x).subs(x,3),1)
equal('N-GH confirmation improvement for every x>1',(4-(x+1)/2)-(4-x),(x-1)/2)
equal('N-MH example cost',x*(x+3+12/x),x**2+3*x+12)
equal('N-MH example profit',20*x-x*(x+3+12/x),-x**2+17*x-12)
equal('N-MH retest cost',x*(2*x+4+16/x),2*x**2+4*x+16)
equal('N-MH retest profit',24*x-x*(2*x+4+16/x),-2*x**2+20*x-16)
equal('N-NGUYEN example equal neighbors',(-(x-s.Rational(5,2))**2+10).subs(x,2),s.Rational(39,4))
equal('N-NGUYEN retest at 4',(-x**2+9*x-8).subs(x,4),12)
equal('N-NGUYEN retest at 5',(-x**2+9*x-8).subs(x,5),12)
equal('N-DH02 derivative retains inner factor',s.diff(s.sin(3*x)-x,x),3*s.cos(3*x)-1)
equal('N-DH02 root in [0,pi/3]',(3*s.cos(3*x)-1).subs(x,s.acos(s.Rational(1,3))/3),0)
equal('N-DH03 exponential example',s.diff(x*s.exp(-x),x),s.exp(-x)*(1-x))
equal('N-DH03 logarithmic example not SP02',s.diff(positive*s.log(positive),positive),1+s.log(positive))
equal('N-DH03 exponential retest',s.diff(x*s.exp(-2*x),x),s.exp(-2*x)*(1-2*x))
equal('N-DH03 exponential retest root',s.diff(x*s.exp(-2*x),x).subs(x,s.Rational(1,2)),0)
equal('N-DH03 logarithmic retest',s.diff(s.log(2*positive)/positive,positive),(1-s.log(2*positive))/positive**2)
equal('N-DH03 logarithmic retest root',(1-s.log(2*positive)).subs(positive,s.E/2),0)
equal('O01 interior lower witness',x-(x-1)/2,(x+1)/2)
equal('O02 upper attained at zero',1/(x*x+4).subs(x,0),s.Rational(1,4))
equal('O02 lower witness increases denominator',(s.sqrt(x*x+1)**2+4)-(x*x+4),1)
equal('O03 speed on [1,3]',s.diff(x**3-6*x*x+12*x,x),3*(x-2)**2)
equal('O03 speed at 1',3*(1-2)**2,3)
equal('O03 speed at 2',3*(2-2)**2,0)
equal('O03 speed at 3',3*(3-2)**2,3)
values={i:(-x**2+9*x-8).subs(x,i) for i in range(2,7)}
checks.append({'name':'N-NGUYEN exact allowed integer maximizers','passed':[i for i,v in values.items() if v==max(values.values())]==[4,5]})
sources=list((ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu/_dung_chung/nen').glob('*.qmd'))
sources+=[ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02/index.qmd']
report={'checks':checks,'source_hashes':{p.relative_to(ROOT).as_posix():sha(p) for p in sources},
    'manual_conditions_review':['N-GH witnesses remain strictly inside the open interval; endpoint 3 included','N-MH x is nonzero and constrained to allowed integers; cost units are per item before multiplying','N-DH02 3x lies in [0,pi], cosine strictly decreasing; root unique and derivative changes + to -','N-DH03 logarithm has positive argument; exponential is positive','New graph A shows partial u only, graph B gives u prime only on (2,3); no value u(2.5) supplied','O01 excluded -1 is not a value of f, although substitution in the expression is possible','O02 zero is a lower bound not attained; larger denominator witness works for every real x','O03 velocity nonnegative on [1,3], so speed equals velocity, not coordinate'],
    'scope':'New foundations and separated existing O; not a claim of a new independent full-bank mathematical acceptance'}
(OUT/'math-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
failed=[n for n in checks if not n['passed']]
print(json.dumps({'passed':len(checks)-len(failed),'total':len(checks),'failed':failed},ensure_ascii=False))
raise SystemExit(bool(failed))

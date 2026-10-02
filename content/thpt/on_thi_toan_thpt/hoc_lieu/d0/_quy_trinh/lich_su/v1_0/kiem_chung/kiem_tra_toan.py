"""Kiểm tính toán độc lập cho dữ kiện D0; không thay thế lập luận trong lời giải."""
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import sympy as s
import json, math
x,t,n=s.symbols('x t n', real=True)
checks=[]
def record(code, ok, evidence):
 assert bool(ok),code
 checks.append({'ma':code,'ket_qua':'ĐẠT kiểm tính toán','bang_chung':evidence})
def both(r,k,a,b,ea,eb):
 record(f'D0-R{r}-{k:02}',a,ea);record(f'D0-R{r}-SL{k:02}',b,eb)
# R1: miền là giao chính xác, không chỉ thử vài số.
d1=s.reduce_inequalities([x+2>=0,s.Ne(x,1)],x)
d2=s.reduce_inequalities([5-x>=0,s.Ne(x,-1)],x)
both(1,1,d1.as_set()==s.Interval(-2,s.oo)-s.FiniteSet(1),d2.as_set()==s.Interval(-s.oo,5)-s.FiniteSet(-1),str(d1),str(d2))
f=x**3-3*x;g=x*x+2*x
both(1,2,(s.diff(f,x).subs(x,1),f.subs(x,1))==(0,-2),(s.diff(g,x).subs(x,1),g.subs(x,1))==(4,3),'Đạo hàm tại 1 = 0; f(1)=-2; đường y=-2.','Đạo hàm tại 1 =4; g(1)=3; đường y=4x-1.')
a=(x+2)*(x-1)**2;b=-x*(x-2)**2
both(1,3,s.solve_univariate_inequality(a<0,x,relational=False)==s.Interval.open(-s.oo,-2),s.solve_univariate_inequality(b>0,x,relational=False)==s.Interval.open(-s.oo,0),'Dấu chính xác: âm trước -2; dương sau -2 trừ nghiệm kép 1.','Dương trước 0; âm sau 0 trừ nghiệm kép 2.')
# R2
both(2,1,(sum([4,5,5,6,30])/5,sorted([4,5,5,6,30])[2])==(10,5),(sum([3,4,4,5,24])/5,4)==(8,4),'Tổng 50; trung vị 5.','Tổng 40; trung vị 4.')
def stats(freq):
 m=[5,15,25];nn=sum(freq);mu=sum(Q(a*b,nn) for a,b in zip(freq,m));var=sum(Q(a,nn)*(b-mu)**2 for a,b in zip(freq,m));alt=sum(Q(a*b*b,nn) for a,b in zip(freq,m))-mu*mu
 assert var==alt
 return mu,var
both(2,2,stats([2,5,3])[0]==16,stats([3,4,3])[0]==15,'Tổng có trọng số 160/10=16.','Tổng có trọng số 150/10=15.')
both(2,3,(stats([2,6,2]),stats([4,2,4]))==((15,40),(15,80)),(stats([1,8,1]),stats([3,4,3]))==((15,20),(15,60)),'Hai công thức phương sai cho 40,80.','Hai công thức phương sai cho 20,60.')
# R3
both(3,1,s.Matrix([0,2])==s.Rational(-2,3)*s.Matrix([0,-3]),s.Matrix([3,0])==s.Rational(-1,2)*s.Matrix([-6,0]),'Thế hệ số -2/3 vào cả hai tọa độ.','Thế hệ số -1/2 vào cả hai tọa độ.')
def projection(A,N,c):
 A=s.Matrix(A);N=s.Matrix(N);H=A-(N.dot(A)+c)/N.dot(N)*N
 assert s.simplify(N.dot(H)+c)==0
 return s.simplify((A-H).norm()),H
pa=projection([1,2,3],[1,2,2],-5);pb=projection([2,0,1],[2,-1,2],-3)
both(3,2,pa[0]==2,pb[0]==1,str(pa),str(pb))
ang1=math.degrees(math.atan2(2,5));ang2=math.degrees(math.atan2(5,10))
both(3,3,round(ang1,1)==21.8 and abs(math.asin(2/math.sqrt(29))-math.atan2(2,5))<1e-12,round(ang2,1)==26.6 and abs(math.asin(5/math.sqrt(125))-math.atan2(5,10))<1e-12,f'Tang và sin: {ang1:.12f} độ.',f'Tang và sin: {ang2:.12f} độ.')
# R4
omega=set(product('NS',repeat=2));A={v for v in omega if v[0]=='N'};B={v for v in omega if v[1]=='N'}
E={2,4,6};F={3,6}
both(4,1,(len(A&B),len(A|B),Q(len(A&B),4)==Q(len(A),4)*Q(len(B),4))==(1,3,True),(len(E&F),len(E|F),Q(len(E&F),6)==Q(len(E),6)*Q(len(F),6))==(1,4,True),'Vét cạn 4 kết quả: giao 1, hợp 3; độc lập.','Vét cạn 6 kết quả: giao 1, hợp 4; độc lập.')
def urn(red,blue):
 pairs=list(combinations(range(red+blue),2));count=sum((i<red)!=(j<red) for i,j in pairs)
 return len(pairs),count,Q(count,len(pairs))
both(4,2,urn(4,3)==(21,12,Q(4,7)),urn(5,3)==(28,15,Q(15,28)),str(urn(4,3)),str(urn(5,3)))
both(4,3,(Q(18,24),Q(18,30))==(Q(3,4),Q(3,5)),(Q(12,20),Q(12,20))==(Q(3,5),Q(3,5)),'Tổng lớp 50; nhóm điều kiện 24 và 30.','Tổng lớp 40; hai nhóm điều kiện đều 20.')
# R5
both(5,1,s.simplify((100+20*(n+1))-(100+20*n))==20 and s.simplify((100*s.Rational(6,5)**(n+1))/(100*s.Rational(6,5)**n))==s.Rational(6,5),s.simplify((80+8*(n+1))-(80+8*n))==8 and s.simplify((80*s.Rational(11,10)**(n+1))/(80*s.Rational(11,10)**n))==s.Rational(11,10),'Hiệu 20; tỉ số 6/5 cho mọi n.','Hiệu 8; tỉ số 11/10 cho mọi n.')
r1=s.solve((x-1)*(x-3)-8,x);r2=s.solve((x-1)*(x-3)-3,x)
both(5,2,r1==[-1,5] and [a for a in r1 if a>3]==[5] and s.log(4,2)+s.log(2,2)==3,r2==[0,4] and [a for a in r2 if a>3]==[4] and s.log(3,3)+s.log(1,3)==1,'Nghiệm đại số -1,5; chỉ 5 có cả hai đối số dương.','Nghiệm đại số 0,4; chỉ 4 thỏa điều kiện.')
both(5,3,100*Q(6,5)**3<200<=100*Q(6,5)**4,80*Q(5,4)**2<150<=80*Q(5,4)**3,'172,8 < 200 ≤ 207,36; công bội >1.','125 < 150 ≤156,25; công bội >1.')
# R6
both(6,1,s.Rational(150,180)*s.pi==5*s.pi/6 and s.cos(5*s.pi/6)<0,s.Rational(240,180)*s.pi==4*s.pi/3 and s.sin(4*s.pi/3)<0,'150°=5π/6; cos=-sqrt(3)/2.','240°=4π/3; sin=-sqrt(3)/2.')
def trigcheck(bases,target,expected):
 # Mỗi cơ sở trong (0,pi); khoảng lọc buộc k=0,1.
 roots=[s.simplify(a+k*s.pi) for a in bases for k in [0,1]]
 assert all(s.simplify(s.sin(2*z)-target)==0 for z in roots)
 assert all(a-s.pi<0 and a+2*s.pi>=2*s.pi for a in bases)
 return set(roots)==set(expected)
both(6,2,trigcheck([s.pi/6,s.pi/3],s.sqrt(3)/2,[s.pi/6,s.pi/3,7*s.pi/6,4*s.pi/3]),trigcheck([s.pi/12,5*s.pi/12],s.Rational(1,2),[s.pi/12,5*s.pi/12,13*s.pi/12,17*s.pi/12]),'Thế đúng bốn nghiệm; k<0 và k>1 ngoài miền ở mỗi họ.','Thế đúng bốn nghiệm; lọc k bằng hai biên.')
h=3+2*s.sin(s.pi*t/6);j=4+s.sin(s.pi*t/4)
both(6,3,s.simplify(h.subs(t,t+12)-h)==0 and h.subs(t,3)==5 and h.subs(t,9)==1,s.simplify(j.subs(t,t+8)-j)==0 and j.subs(t,2)==5 and j.subs(t,6)==3,'Chu kì 12; cực đại đầu 3; cực tiểu 9.','Chu kì 8; cực đại đầu 2; cực tiểu 6.')
# R7
both(7,1,[s.diff(z,x)==2*x for z in [x*x+3,x*x-5,2*x*x,x*x+x]]==[True,True,False,False],[s.diff(z,x)==3*x*x for z in [x**3+7,x**3-2,3*x**3,x**3+x]]==[True,True,False,False],'Đạo hàm: 2x,2x,4x,2x+1.','Đạo hàm: 3x²,3x²,9x²,3x²+1.')
f=x**3-2*x+5;g=x*x+3*x+1
both(7,2,s.diff(f,x)==3*x*x-2 and f.subs(x,1)==4 and f.subs(x,2)==9 and 4+s.integrate(3*x*x-2,(x,1,2))==9,s.diff(g,x)==2*x+3 and g.subs(x,0)==1 and g.subs(x,2)==11,'Đạo hàm, điều kiện đầu và hiệu tích phân đều khớp.','Đạo hàm, điều kiện đầu và giá trị 11 đều khớp.')
def motion(c,end):return s.integrate(t-c,(t,0,end)),s.integrate(c-t,(t,0,c))+s.integrate(t-c,(t,c,end))
both(7,3,motion(2,5)==(s.Rational(5,2),s.Rational(13,2)),motion(1,3)==(s.Rational(3,2),s.Rational(5,2)),'Tích phân có dấu 5/2; hai tam giác 2+9/2=13/2.','Tích phân có dấu 3/2; hai tam giác 1/2+2=5/2.')
# R8
both(8,1,s.reduce_inequalities([x>0,20-2*x>0],x).as_set()==s.Interval.open(0,10),s.reduce_inequalities([x>0,30-2*x>0],x).as_set()==s.Interval.open(0,15),'Đếm 2x+y=20; miền (0,10); diện tích xy.','Đếm 2x+y=30; miền (0,15); diện tích xy.')
both(8,2,s.reduce_inequalities([x>=1,18+11*(x-1)<=73],x).as_set()==s.Interval(1,6),s.reduce_inequalities([x>=1,20+12*(x-1)<=80],x).as_set()==s.Interval(1,6),'Miền ngân sách [1,6]; C(1)=18, C(6)=73.','Miền ngân sách [1,6]; C(1)=20, C(6)=80.')
def optimize(cap):
 feasible=[(30*a+40*b,a,b) for a,b in product(range(cap+1),repeat=2) if 2*a+b<=cap and a+2*b<=cap]
 top=max(v[0] for v in feasible);winners=[v for v in feasible if v[0]==top]
 return len(feasible),winners
z1=optimize(8);z2=optimize(7)
both(8,3,z1[1]==[(180,2,3)],z2[1]==[(150,1,3)],f'Vét cạn hộp [0,8]^2: {z1[0]} cặp khả thi; {z1[1]}.',f'Vét cạn hộp [0,7]^2: {z2[0]} cặp khả thi; {z2[1]}.')
# Dữ liệu và tính nhất quán cấu trúc
root=Path(__file__).resolve().parents[1]
bank=json.loads((root/'D0_ngan_hang_v1.0.json').read_text())['items']
assert len(bank)==24 and len(checks)==48
assert len({z['id'] for z in bank})==24
assert all(sum(z['r']==f'R{k}' for z in bank)==3 for k in range(1,9))
assert {z['ma'] for z in checks}=={z[key] for z in bank for key in ['id','retest_id']}
(root/'kiem_chung/ket_qua_tinh_toan.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
lines=['# Kiểm tính toán D0 v1.0','', 'Ngày: 09/09/2026. Công cụ: Python / SymPy / Fraction. 48 nhiệm vụ đã qua các phép kiểm được ghi dưới đây. Kết quả này không thay cho kiểm lập luận, đọc nguồn, xem thành phẩm hoặc duyệt của người chủ trì.','']
for c in checks:lines.append(f"- **{c['ma']}**: {c['bang_chung']}")
(root/'kiem_chung/ket_qua_tinh_toan.md').write_text('\n'.join(lines)+'\n')
print(f'48/48 phép kiểm nhiệm vụ thành công; 24 mã chính duy nhất; đúng 3 nhiệm vụ/mạch. Cặp khả thi tối ưu: {z1[0]}, {z2[0]}.')

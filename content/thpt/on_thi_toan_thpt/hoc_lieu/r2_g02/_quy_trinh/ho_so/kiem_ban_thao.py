"""Kiểm phép tính và cấu trúc bản thảo; không kiểm sản phẩm HTML/PDF."""
from pathlib import Path
from fractions import Fraction as F
import argparse, collections, hashlib, importlib.util, json, math, re

parser = argparse.ArgumentParser()
parser.add_argument("--repo", type=Path, default=Path("E:/zo_math"))
parser.add_argument("--canonical", action="store_true")
args = parser.parse_args()
ROOT = Path(__file__).resolve().parent
STAGE = ROOT / "staged"
REPO = args.repo
HL = "content/thpt/on_thi_toan_thpt/hoc_lieu"
MAIN = REPO / HL / "r2_g02/_quy_trinh/ban_thao/noi_dung.md"
BASE = REPO / HL / "_dung_chung/nen/_quy_trinh/ban_thao/so_gan_dung_sai_so.md"
mapping = {MAIN.resolve(): STAGE/"noi_dung.md", BASE.resolve(): STAGE/"foundation.md"}
for path in (STAGE/"hinh").glob("*"):
    mapping[(MAIN.parent/"hinh"/path.name).resolve()] = path

def actual(p):
    return p if args.canonical else mapping.get(p.resolve(), p)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def median(values):
    n=len(values)
    return values[n//2] if n%2 else (values[n//2-1]+values[n//2])/2

def raw(values):
    x=sorted(map(F, values)); n=len(x); mean=sum(x)/n
    q1=median(x[:n//2]); q3=median(x[(n+1)//2:])
    var=sum((v-mean)**2 for v in x)/n
    return {"n":n, "mean":mean, "R":x[-1]-x[0], "Q1":q1, "Q3":q3,
            "IQR":q3-q1, "variance":var, "sd":math.sqrt(var),
            "lower":q1-F(3,2)*(q3-q1), "upper":q3+F(3,2)*(q3-q1)}

def grouped(edges, freq):
    edges=list(map(F, edges)); n=sum(freq)
    mids=[(a+b)/2 for a,b in zip(edges,edges[1:])]
    mean=sum(m*f for m,f in zip(mids,freq))/n
    var=sum(f*(m-mean)**2 for m,f in zip(mids,freq))/n
    def q(k):
        target=F(k*n,4); before=0
        for i,f in enumerate(freq):
            if f and before+f>=target:
                return edges[i]+(target-before)/f*(edges[i+1]-edges[i])
            before+=f
        raise AssertionError("No quartile group")
    occupied=[i for i,f in enumerate(freq) if f]
    return {"n":n, "mean":mean, "R":edges[occupied[-1]+1]-edges[occupied[0]],
            "Q1":q(1), "Q3":q(3), "IQR":q(3)-q(1), "variance":var,
            "sd":math.sqrt(var)}

cases = [
("NV01a",[3,5,5,7,9],{"mean":"29/5","Q1":4,"Q3":8}),
("NV01b",[2,4,4,4,6,6],{"mean":"13/3","n":6}),
("NV02A",[8,9,10,11,12],{"mean":10,"R":4,"variance":2}),
("NV02B",[2,6,10,14,18],{"mean":10,"R":16,"variance":32}),
("NV03",[2,4,4,5,5,6,8,14],{"R":12,"Q1":4,"Q3":7,"IQR":3,"lower":"-1/2","upper":"23/2"}),
("NV03_modified",[2,4,4,5,5,6,8,24],{"R":22,"IQR":3}),
("NV04",[1,2,3,4,5],{"mean":3,"variance":2}),
("NV07",[181,186,195,193,190,181,195,193,190,186],{"mean":189,"R":14,"Q1":186,"Q3":193,"IQR":7,"variance":"126/5","lower":"351/2","upper":"407/2"}),
("NV08A",[4,5,6,7,8],{"mean":6,"R":4,"IQR":3,"variance":2}),
("NV08B",[4,6,6,6,8],{"mean":6,"R":4,"IQR":2,"variance":"8/5"}),
("NV10A",[2,2,18,18],{"mean":10,"variance":64}),
("NV10B",[8,8,12,12],{"mean":10,"variance":4}),
("NV12A",[103,103,103],{"mean":103,"variance":0}),
("NV12B",[99,100,101],{"mean":100,"variance":"2/3"}),
("NV13",[6,7,7,8,8,9,9,18],{"mean":9,"R":12,"Q1":7,"Q3":9,"IQR":2,"variance":"25/2","lower":4,"upper":12}),
("NV15e_A",[0,2,4],{"mean":2,"variance":"8/3"}),
("NV15e_B",[1,2,3],{"mean":2,"variance":"2/3"}),
("NV17",[3,4,5,6,7,11],{"mean":6,"R":8,"Q1":4,"Q3":7,"IQR":3,"variance":"20/3","lower":"-1/2","upper":"23/2"}),
("NV20",[2,2,5,5,5,8],{"n":6,"mean":"9/2","Q1":2,"Q3":5}),
("NV22A",[1,2,5,8,9],{"mean":5,"R":8,"variance":10}),
("NV22B",[1,4,5,6,9],{"mean":5,"R":8,"variance":"34/5"}),
("NV23",[0,0,6],{"mean":2,"variance":8}),
("NV24",[1,1,1,1,3,3],{"n":6,"mean":"5/3","variance":"8/9"}),
("NV25_original",[7,7,8,8],{"mean":"15/2","R":1,"variance":"1/4"}),
("NV26",[5,5,6,6,6,7,7,20],{"Q1":"11/2","Q3":7,"IQR":"3/2","lower":"13/4","upper":"37/4"}),
("NV29",[3,8,8,8,8,8,8,13],{"mean":8,"IQR":0,"variance":"25/4"}),
("figure3_A",[1,1,19,19],{"mean":10,"variance":81}),
("figure3_B",[9,9,11,11],{"mean":10,"variance":1}),
]
groups = [
("NV05",[0,10,20,30],[2,4,2],{"n":8,"mean":15,"R":30,"Q1":10,"Q3":20,"IQR":10,"variance":50}),
("NV09",[0,5,10,15,20,25],[0,3,6,3,0],{"n":12,"mean":"25/2","R":15,"Q1":10,"Q3":15,"IQR":5,"variance":"25/2"}),
("NV10_group",[0,10,20],[2,2],{"mean":10,"variance":25}),
("NV14",[10,20,30,40,50],[2,6,8,4],{"n":20,"mean":32,"R":40,"Q1":25,"Q3":"155/4","IQR":"55/4","variance":81}),
("NV18",[0,4,8,12,16],[1,3,4,2],{"n":10,"mean":"44/5","R":16,"Q1":6,"Q3":"23/2","IQR":"11/2","variance":"324/25"}),
("NV25",[0,4,8,12,16],[0,2,2,0],{"n":4,"mean":8,"R":8,"Q1":6,"Q3":10,"IQR":4,"variance":4}),
]
checks=[]; numbers={}
def check(name, passed, detail=None):
    checks.append({"name":name,"passed":bool(passed), **({"detail":detail} if detail is not None else {})})

for name,x,expected in cases:
    result=raw(x); numbers[name]={"values":x, "computed":result}
    for key,want in expected.items():
        check(f"{name}/{key}", result[key]==F(want), str(result[key]))
for name,edges,freq,expected in groups:
    result=grouped(edges,freq); numbers[name]={"edges":edges,"frequencies":freq,"computed":result}
    for key,want in expected.items():
        check(f"{name}/{key}", result[key]==F(want), str(result[key]))

source=REPO/HL/"r2_g01/du_lieu/hoc.json"
penguins=json.loads(source.read_text(encoding="utf-8"))["penguins"]
selected=[r for r in penguins if r["species"]=="Adelie" and r["year"]=="2007" and r["flipper_length_mm"]!="NA"][:10]
check("Palmer: preserve exact ten source values", [int(r["flipper_length_mm"]) for r in selected]==cases[7][1])
check("Palmer: source rows", [r["source_row"] for r in selected]==[1,2,3,5,6,7,8,9,10,11])
check("Test scores total ten", sum(map(F,["3","3","2.5","1.5"]))==10)
check("Foundation rounding example", max(abs(F("18.3")-F(x)) for x in ["18.254","18.294"])==F(".046"))
check("Foundation rounding task", max(abs(F("32.5")-F(x)) for x in ["32.447","32.487"])==F(".053"))
check("Foundation relative error 1", F(".3")/50==F(".006"))
check("Foundation relative error 2", F(".4")/120==F(1,300))
check("Change cm to mm: variance", F(".16")*100==16 and 25*100==2500)
check("Change g to kg: variance", F(9,1000000)==F(".000009") and F(1,1000000)==F(".000001"))
check("Frequency scaling", raw([1,1,1,1,3,3]*3)["variance"]==F(8,9))

spec=importlib.util.spec_from_file_location("zo_delimiter_guard",REPO/"scripts/zo_latex_delimiters.py")
guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
texts={p:actual(p).read_text(encoding="utf-8") for p in [MAIN,BASE]}
anchors={}
math_count=0; local_links=0; external=[]
for p,txt in texts.items():
    ids=re.findall(r'<a id="([^"]+)"></a>',txt)
    anchors[p]=set(ids)
    check(p.name+": unique anchors",len(ids)==len(set(ids)))
    check(p.name+": dollars paired",len(re.findall(r"(?<!\\)\$",txt))%2==0)
    check(p.name+": no accidental double LaTex backslashes", not re.search(r"\\\\[A-Za-z]",txt))
    check(p.name+": no empty placeholders",not re.search(r"\b(?:TODO|TBD|FIXME)\b|Chưa điền",txt))
    for m in re.finditer(r"\$\$(.*?)\$\$|(?<!\\)\$([^$\n]*)\$",txt,re.S):
        formula=m[1] if m[1] is not None else m[2]
        math_count+=1
        errors=guard.delimiter_errors(formula)
        if errors: check(p.name+f": delimiters line {txt[:m.start()].count(chr(10))+1}",False,errors)
        if re.search(r"\d+\s*/\s*\d+",formula): check(p.name+": slash fraction",False,formula)
    for target in re.findall(r"!?\[[^\]]+\]\(([^)\s]+)\)",txt):
        if target.startswith(("http://","https://")): external.append(target);continue
        path,sep,fragment=target.partition("#")
        dest=(p.parent/path).resolve() if path else p.resolve()
        dest_actual=actual(dest)
        local_links+=1
        check(p.name+": link "+target,dest_actual.is_file())
        if fragment and dest_actual.is_file():
            other=dest_actual.read_text(encoding="utf-8")
            available=set(re.findall(r'<a id="([^"]+)"',other)+re.findall(r"\{#([^\s}]+)",other))
            check(p.name+": anchor "+target,fragment in available)
    n=29 if p==MAIN else 4
    qprefix="nv" if p==MAIN else "nen-nv"
    aprefix="giai" if p==MAIN else "nen-giai"
    for i in range(1,n+1):
        q=f"{qprefix}{i:02}";a=f"{aprefix}{i:02}"
        check(p.name+f": pair {i:02}", q in ids and a in ids and f"](#{q})" in txt and f"](#{a})" in txt)

main=texts[MAIN]
lesson=main.split("## Bài học\n",1)[1].split('<a id="luyen-tap">',1)[0]
check("Lesson: five numbered sections", len(re.findall(r"^### [1-5]\. ",lesson,re.M))==5)
check("Lesson: no activity headings",not re.search(r"^#{3,6} (Gợi mở|Ví dụ|Nhiệm vụ)",lesson,re.M))
check("Lesson: five Gợi mở in order",re.findall(r"\*\*Gợi mở (\d+)",lesson)==["01","02","03","04","05"])
check("Lesson: examples in order",re.findall(r"\*\*Ví dụ (\d+)",lesson)==[f"{i:02}" for i in range(1,9)])
check("Solutions collapsed: all 29", main.count('.solution collapse="true"')==29)
check("Foundation solutions: all 4",texts[BASE].count('.solution collapse="true"')==4)
journal=main.split('## Nhật kí\n',1)[1].split('<a id="loi-giai">',1)[0]
shared=(REPO/HL/"_dung_chung/nhat_ki_hoc_tap.qmd").read_text(encoding="utf-8")
fields=re.findall(r"^\| (.*?) \| … \|$",shared,re.M)
actual_fields=re.findall(r"^\| (.*?) \| … \|$",journal,re.M)
check("Journal: exact fourteen shared fields", fields==actual_fields and len(fields)==14)
review=main.split("## Ôn lại\n",1)[1].split('<a id="on-nen">',1)[0]
check("Review: no pre-supplied formula", not re.search(r"\\(?:frac|sqrt|sum)",review))

source_paths=[
"content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/mau/ban_thao_goi.md",
"content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/mau/bang_kiem_ban_thao_goi.md",
HL+"/r1_g01/index.qmd",HL+"/r1_g02/index.qmd",HL+"/r2_g01/index.qmd",
HL+"/r2_g01/du_lieu/hoc.json",HL+"/r2_g01/_quy_trinh/ho_so/nguon_va_phan_chia.json",
HL+"/r2_g01/_quy_trinh/ho_so/tong_ket_cai_tien_20261028.md",
HL+"/r2_g01/hinh/y_tuong_v01/build_figures.py",HL+"/_dung_chung/nhat_ki_hoc_tap.qmd",
]
report={
"package":"R2-G02","version":"0.1","date":"2026-10-29","stage":"manuscript_pending_owner_review",
"mode":"canonical" if args.canonical else "staged","passed":sum(c["passed"] for c in checks),"total":len(checks),
"mathematical_expressions_checked":math_count,"local_links_checked":local_links,
"manuscript_sha256":{str(p.relative_to(REPO)).replace("\\","/"):sha(actual(p)) for p in texts},
"reference_sha256":{p:sha(REPO/p) for p in source_paths},
"data_provenance":{"source":str(source),"sha256":sha(source),"rows":selected,"missing_row_4":"excluded, not zero","use":"practice, previously available in R2-G01"},
"numeric_results":numbers,"checks":checks,"external_links_recorded_not_http_tested":sorted(set(external)),
"limits":["Không chứng nhận tương tác HTML/PDF.","Không thay chủ trì duyệt nội dung.","schema/readiness đối chứng có ba lỗi tài sản TEX R1-G01 ngoài phạm vi.","Các kết luận ngữ nghĩa được đọc riêng trong báo cáo trước trình."]}
out=ROOT/("kiem_tra_nguon_chinh.json" if args.canonical else "kiem_tra_ban_thao.json")
out.write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str)+"\n",encoding="utf-8")
print(json.dumps({"passed":report["passed"],"total":report["total"],"math":math_count,"local_links":local_links,"failures":[c for c in checks if not c["passed"]]},ensure_ascii=False))
raise SystemExit(0 if report["passed"]==report["total"] else 1)

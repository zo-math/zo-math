"""Source/DOM regressions. Optional existing HTML is read-only evidence."""
import argparse, copy, hashlib, json, sys
from pathlib import Path
from bs4 import BeautifulSoup
from zo_course_reading_regions import apply, require, source_checks
ROOT=Path(__file__).resolve().parents[1]

def inventory(root):
    return (root.get_text(" ",strip=True),sorted(n["id"] for n in root.select("[id]")),
            [str(n) for n in root.select("math")],
            [(n.get_text(" ",strip=True),n["href"]) for n in root.select("a[href]")],
            [str(n) for n in root.select("img")])

def main():
    parser=argparse.ArgumentParser();parser.add_argument("--fixture-root",type=Path);parser.add_argument("--report",type=Path)
    args=parser.parse_args();checks=source_checks(ROOT);observations={}
    binding={"units":[{"id":str(i),"function":"function.warmup","question":"q"+str(i),"answer":"a"+str(i)} for i in range(2)]}
    d=BeautifulSoup('<div class="reader-content"><div class="reading-region"><h2>Khởi động</h2><div id="group"><div id="q0">Đề đầu <a href="#a0">Xem lời giải</a></div><div id="q1">Đề sau <a href="#a1">Xem lời giải</a></div></div></div><div class="reading-region"><div id="a0">Giải đầu <a href="#q0">Xem đề bài</a></div><div id="a1">Giải sau <a href="#q1">Xem đề bài</a></div></div></div>','html.parser')
    try:require(d,binding);checks['reject grouped independent tasks']=False
    except ValueError:checks['reject grouped independent tasks']=True
    before=inventory(d);apply(d,binding);checks['preserve full inventory']=inventory(d)==before
    serialized=str(d);apply(d,binding);checks['idempotent']=str(d)==serialized
    checks['retain group ID']=d.find(id='group') is not None
    checks['heading joins first task']=d.find(id='q0').find_parent(class_='reading-region').find('h2') is not None
    checks['actions stay with each task']=all(d.find(id='q'+str(i)).find_parent(class_='reading-region').select_one('a')['href']=='#a'+str(i) for i in range(2))
    local=BeautifulSoup('<div class="reader-content"><div class="reading-region" id="q0">Đề <details id="a0"><summary>Đối chiếu</summary>Lời giải</details></div></div>','html.parser')
    saved=str(local);apply(local,{"units":[binding["units"][0]]})
    checks['local solution stays in its task']=str(local)==saved
    template=(ROOT/'_design/web_2027_mau_dung_chung/templates/page.html.tpl').read_text(encoding='utf-8')
    checks['shared breadcrumb Khóa 2027']='>Khóa 2027</a>' in template and 'Nhà khóa 2027' not in template
    plan=json.loads((ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/giao_dien/web_2027_layout.json').read_text(encoding='utf-8'))
    checks['G01 source hero no redundant action']='hero-action' not in json.dumps(plan['layout'],ensure_ascii=False)
    checks['G01 current breadcrumb']='Nhà khóa 2027' not in json.dumps(plan['layout'],ensure_ascii=False)
    for name in ['g02','g03','g04']:
        source=(ROOT/f'scripts/zo_web_2027_{name}.py').read_text(encoding='utf-8')
        checks[name+' hero no redundant action']='class="hero-action"' not in source
    if args.fixture_root:
        for name in ['r1_g01','r1_g02','r1_g03','r1_g04']:
            rel=Path('content/thpt/on_thi_toan_thpt/hoc_lieu')/name
            path=args.fixture_root/rel/'index.html';raw=path.read_bytes()
            doc=BeautifulSoup(raw,'html.parser');root=doc.select_one('.reader-content')
            b=json.loads((ROOT/rel/'giao_dien/he_nhan.json').read_text(encoding='utf-8'))
            before=inventory(root);old=len(root.select('.reading-region'));apply(doc,b)
            checks[name+' preserved all text math IDs links images']=inventory(root)==before
            serialized=str(root);apply(doc,b);checks[name+' idempotent']=str(root)==serialized
            checks[name+' fixture untouched']=path.read_bytes()==raw
            observations[name]={'existing_papers':old,'proposed_papers_in_memory':len(root.select('.reading-region'))}
    report={'checks':checks,'observations':observations,'passed':sum(checks.values()),'total':len(checks)}
    if args.report:
        target=args.report.resolve()
        if not target.is_relative_to(ROOT/'_audit') or target.suffix!='.json':
            raise ValueError('Report must be JSON under _audit')
        target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if all(checks.values()) else 1
if __name__=='__main__':raise SystemExit(main())

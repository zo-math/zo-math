"""Course math assets: role-aware provenance, native BBT calls and shared sizing."""
from __future__ import annotations
import hashlib,json,re,shutil
from pathlib import Path
from bs4 import BeautifulSoup
from zo_graphics import graphics_root,load_variation_html,set_lesson_graph_size

ROOT=Path(__file__).resolve().parents[1]
BASE=Path("content/thpt/on_thi_toan_thpt/hoc_lieu")
KIT=Path("_design/web_2027_mau_dung_chung")
POLICY=KIT/"profiles/course-math-assets.json"

def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def canonical_digest(data):
    return hashlib.sha256(json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def governed(source,repo=ROOT):
    source=Path(source)
    if not source.is_absolute(): source=Path(repo)/source
    try:rel=source.resolve().relative_to((Path(repo)/BASE).resolve())
    except ValueError:return False
    policy=json.loads((Path(repo)/POLICY).read_text(encoding="utf-8"))
    return len(rel.parts)==2 and rel.name=="index.qmd" and bool(re.fullmatch(r"r\d+_g\d+",rel.parts[0])) and rel.parts[0] not in policy["legacy_packages"]

def graph_inputs(package,repo=ROOT):
    repo=Path(repo);package=Path(package);graphics=graphics_root(repo)
    paths={str(p.relative_to(repo)).replace("\\","/"):p for p in
           [package/"_quy_trinh/sinh_hinh.py",repo/"scripts/zo_graphics.py",repo/KIT/"figure-profile-candidate/production-figures.css",repo/POLICY]}
    paths.update({"graphics/"+str(p.relative_to(graphics)).replace("\\","/"):p for p in
        [graphics/"zo_graph.py",graphics/"graph/zo_graph_build.py",graphics/"graph/axis_ticks.py",graphics/"graph/tex/zo_graph_v02.tex",graphics/"graph/tex/zo_graph_v04.tex",graphics/"graph/profiles/lesson-g03.json",*sorted((graphics/"assets/fonts").glob("STIXTwo*.otf"))]})
    return {name:digest(p) for name,p in paths.items()}

def source_checks(source,repo=ROOT):
    source=Path(source);repo=Path(repo)
    if not source.is_absolute():source=repo/source
    if not governed(source,repo):
        if source.parent.name in {'r1_g01','r1_g02','r1_g03'}:return legacy_graph_checks(source,repo)
        return {}
    p=source.parent;s=source.read_text(encoding="utf-8")
    if not (p/"giao_dien/hinh_manifest.json").exists() and not re.search(r"\.svg\)|\.zo-native-bbt|\\(?:nearrow|searrow|rightarrow)",s):
        return {"no graph or BBT resources in this package":True}
    policy=json.loads((repo/POLICY).read_text(encoding="utf-8"))
    manifest=json.loads((p/"giao_dien/hinh_manifest.json").read_text(encoding="utf-8"))
    specs=json.loads((p/"du_lieu/hinh_do_thi.json").read_text(encoding="utf-8"))
    by_id={v["id"]:v for v in specs}
    config_path=p/"_quy_trinh/cau_hinh_san_xuat_qmd.yml"
    requires_pdf=False
    if config_path.exists():
        import yaml
        production=yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        requires_pdf=bool(((production.get("extensions") or {}).get("pdf_variants") or {}))
    values={"graph dependencies match":manifest.get("source_hashes")==graph_inputs(p,repo),
            "graph inventory exact":{f["name"] for f in manifest["figures"]}==set(by_id) and len(manifest["figures"])==len(by_id)}
    from zo_graphics import load_graph
    graph_engine=load_graph("course_graph_axis_gate",repo)
    for f in manifest["figures"]:
        name=f["name"]
        values[name+"/body role"]=f.get("role")=="lesson"
        values[name+"/surface"]=f.get("surface")==policy["lesson_graph"]["surface"]
        values[name+"/style"]=f.get("style")==policy["lesson_graph"]["style"]
        values[name+"/layout"]=f.get("layout")==policy["lesson_graph"]["layout"]
        values[name+"/spec"]=f.get("spec_sha256")==canonical_digest(by_id.get(name))
        for key in ("input","svg"):
            rel=f.get(key);expected=f.get(key+"_sha256")
            values[name+"/"+key]=bool(rel and expected and (p/rel).is_file() and digest(p/rel)==expected)
        if requires_pdf:
            rel=f.get("pdf");expected=f.get("pdf_sha256")
            values[name+"/pdf"]=bool(rel and expected and (p/rel).is_file() and digest(p/rel)==expected)
            values[name+"/no endpoint tick strokes"]=bool(rel and (p/rel).is_file() and graph_engine.graph_axis_check(p/rel)["passed"])
    records=json.loads((p/"du_lieu/bang_bien_thien.json").read_text(encoding="utf-8"))
    renderer=load_variation_html("course_math_source",repo)
    for record in records:renderer.validate_record(record)
    calls=re.findall(r'\.zo-native-bbt\s+data-bbt="([^"]+)"',s)
    values["native BBT inventory"]=len(calls)==len(set(calls))==len(records) and set(calls)=={r["id"] for r in records}
    # Explicit bindings must never let the native mathematical type take the ordinary path.
    tables=json.loads((repo/KIT/"profiles/course-tables.json").read_text(encoding="utf-8"))["pages"][p.name]
    values["no ordinary variation binding"]=not any(e["kind"]=="variation" for e in tables)
    values["no handwritten variation grid"]=not re.search(r"(?m)^\|.*\\(?:nearrow|searrow|rightarrow).*\|",s)
    values.update(draft_table_checks(p))
    values["all graph references owned"]={Path(v).stem for v in re.findall(r'!\[[^\]]*\]\(([^)]+\.svg)\)',s)}==set(by_id)
    return values

def require_source(source,repo=ROOT):
    values=source_checks(source,repo);bad=[k for k,v in values.items() if not v]
    if bad:raise ValueError("Course math assets source: "+"; ".join(bad))

def apply_native(doc,page_key,repo=ROOT):
    root=doc.select_one(".reader-content");calls=root.select(".zo-native-bbt[data-bbt]")
    if not calls:return
    source=Path(repo)/BASE/page_key/"du_lieu/bang_bien_thien.json"
    renderer=load_variation_html("course_math_native",repo)
    records=renderer.load_data(source);by_id={r["id"]:r for r in records}
    fragments=renderer.math_fragments(records);seen=set()
    for call in calls:
        rid=call["data-bbt"]
        if rid not in by_id or rid in seen:raise ValueError("Unknown/duplicate native BBT call: "+rid)
        seen.add(rid)
        existing=call.select("table.zo-variation-native")
        if existing:
            actual=[[c.get("data-source-value") for c in row.find_all(["td","th"],recursive=False)] for row in existing[0].select("tr")]
            if len(existing)!=1 or actual!=by_id[rid]["rows"]:raise ValueError("Native BBT call differs from canonical source")
            continue
        if call.select("table") or call.get_text(strip=True):raise ValueError("Native BBT call contains a second authored source")
        fragment=BeautifulSoup(renderer.render_record(by_id[rid],fragments),"html.parser")
        call.append(fragment.find("figure").extract())
    if seen!=set(by_id):raise ValueError("Missing canonical native BBT call")

def apply_graph_display(doc,page,runtime,repo=ROOT):
    from urllib.parse import urlsplit
    from os.path import relpath
    doc.body["class"]=list(dict.fromkeys(doc.body.get("class",[])+["zo-web-2027-production"]))
    root=doc.select_one(".reader-content")
    for img in root.select(".figure-viewport img"):
        img["class"]=[c for c in img.get("class",[]) if c!="math-illustration"]+["zo-graph-04"]
        from urllib.parse import unquote
        set_lesson_graph_size(img,(page.parent/unquote(urlsplit(img["src"]).path)).resolve(),repo)
        img.parent["class"]=list(dict.fromkeys(img.parent.get("class",[])+["zo-figure-scroll"]))
    source=Path(repo)/KIT/"figure-profile-candidate/production-figures.css"
    target=runtime/"production-figures.css";shutil.copyfile(source,target)
    doc.head.append(doc.new_tag("link",rel="stylesheet",href=relpath(target,page.parent).replace("\\","/")))

def html_checks(doc,page_key,repo=ROOT):
    source=Path(repo)/BASE/page_key/"index.qmd"
    if not governed(source,repo):return {}
    root=doc.select_one(".reader-content")
    records=json.loads((source.parent/"du_lieu/bang_bien_thien.json").read_text(encoding="utf-8"))
    values={"shared figure namespace active":"zo-web-2027-production" in doc.body.get("class",[]),
            "no ordinary variation HTML":not root.select('table[data-table-kind="variation"]:not(.zo-variation-native)'),
            "shared figure stylesheet":any(Path(n["href"].split("?")[0]).name=="production-figures.css" for n in doc.select("link[href]"))}
    for r in records:
        tables=root.select('table.zo-variation-native[data-bbt="'+r["id"]+'"]')
        values[r["id"]+"/single native"]=len(tables)==1
        if len(tables)!=1:continue
        rows=[[c.get("data-source-value") for c in row.find_all(["td","th"],recursive=False)] for row in tables[0].select("tr")]
        values[r["id"]+"/canonical rows"]=rows==r["rows"]
        values[r["id"]+"/rendered math"]=all(c.find("math") for c in tables[0].select('[data-source-value]') if re.search(r"[↗↘→∞]|\d",c["data-source-value"]) and c["data-source-value"]!="Không xác định")
    graphs=root.select(".figure-viewport img")
    expected=json.loads((source.parent/"giao_dien/hinh_manifest.json").read_text())["figures"]
    values["graph display count"]=len(graphs)==len(expected)
    values["graph G03 shared display"]=all("zo-graph-04" in im.get("class",[]) and im.get("data-zo-graph-role")=="lesson" and im.get("data-zo-graph-layout")=="lesson-g03" and bool(re.fullmatch(r"--figure-em:[0-9.]+em",im.get("style",""))) for im in graphs)
    from zo_graphics import lesson_layout
    import xml.etree.ElementTree as ET
    ratio=lesson_layout(repo)["web_svg_bp_per_em"]
    by_name={Path(f["svg"]).name:f for f in expected}
    for im in graphs:
        f=by_name[Path(im["src"]).name]
        w=float(ET.parse(source.parent/f["svg"]).getroot().attrib["viewBox"].split()[2])
        values[f["name"]+"/G03 display scale"]=im.get("style")==f"--figure-em:{w/ratio:.5f}em"
    return values

def lesson_display_checks(doc,page_key,repo=ROOT):
    """G01/G02/G03/G04 use the owner-selected G03 scale, including support graphs."""
    if page_key not in {"r1_g01","r1_g02","r1_g03","r1_g04"}:return {}
    import xml.etree.ElementTree as ET
    from zo_graphics import lesson_layout
    package=Path(repo)/BASE/page_key
    if page_key in {"r1_g03","r1_g04"}:
        files=[package/f["svg"] for f in json.loads((package/"giao_dien/hinh_manifest.json").read_text(encoding="utf-8"))["figures"]]
    else:
        config=json.loads((package/"giao_dien/web_2027_figures.json").read_text(encoding="utf-8"))
        names=config["graphs"] if page_key=="r1_g01" else [Path(f["source"]).stem for f in config["figures"] if f["role"]!="cover"]
        files=[package/"giao_dien/assets/figures_0_4"/(name+".svg") for name in names]
    images=doc.select(".reader-content .figure-viewport img")
    by_name={p.name:p for p in files};ratio=lesson_layout(repo)["web_svg_bp_per_em"]
    values={"G03 shared sizing namespace":"zo-web-2027-production" in doc.body.get("class",[]),"G03 graph inventory":len(images)==len(files),"G03 shared sizing CSS":any(Path(n["href"]).name=="production-figures.css" for n in doc.select("link[href]"))}
    for im in images:
        name=Path(im["src"]).name;p=by_name.get(name)
        values[name+"/owned graph"]=p is not None
        if p is None:continue
        w=float(ET.parse(p).getroot().attrib["viewBox"].split()[2])
        values[name+"/G03 size"]=im.get("style")==f"--figure-em:{w/ratio:.5f}em"
        values[name+"/G03 component"]="zo-graph-04" in im.get("class",[]) and im.get("data-zo-graph-layout")=="lesson-g03"
    return values


def strip_variation_math(text):
    """Compare prose math independently of the explicitly migrated BBTs."""
    return re.sub(r"(?m)(?:^\|.*\n)+",lambda m:"" if re.search(r"\\(?:nearrow|searrow|rightarrow)",m[0]) else m[0],text)


def _clean(value):
    value=value.strip().strip("$").replace("^\\prime","′").replace("\\prime","′")
    for tex,char in [(r"\infty","∞"),(r"\nearrow","↗"),(r"\searrow","↘"),(r"\ ","")]:
        value=value.replace(tex,char)
    return re.sub(r"\s+"," ",value.replace("−","-")).strip()

def _segments(rows,canonical=False):
    rows=[[_clean(v) for v in row] for row in rows]
    def parts(v):
        match=re.fullmatch(r"(.*?)([↗↘→])(.*)",v)
        if not match:raise ValueError("Missing explicit variation direction")
        return tuple(s.strip() for s in match.groups())
    answer=[]
    if canonical or (rows[0][0]=="x" and any("(" in v for v in rows[0][1:])):
        for i in range(2,len(rows[0]),2):
            left,arrow,right=parts(rows[-1][i])
            answer.append((rows[0][i-1],rows[0][i+1],left or rows[-1][i-1],
                           arrow,right or rows[-1][i+1],rows[1][i] if len(rows)==3 else None))
    elif rows[0][0]=="x":
        for i in range(1,len(rows[0])-1):
            left,arrow,unused=parts(rows[-1][i])
            right=re.split("[↗↘→]",rows[-1][i+1])[0].strip()
            answer.append((rows[0][i],rows[0][i+1],left,arrow,right,None))
    else:
        for i,interval in enumerate(rows[0][1:],1):
            match=re.fullmatch(r"[\[(](.*?);(.*?)[\])]",interval)
            if not match:raise ValueError("Missing explicit interval endpoints")
            left,arrow,right=parts(rows[-1][i])
            answer.append((*match.groups(),left,arrow,right,rows[1][i] if len(rows)==3 else None))
    return answer

def draft_table_checks(package):
    """Compare endpoint limits, trends and provided derivative rows with the frozen draft."""
    p=Path(package);draft=(p/"_quy_trinh/ban_thao/noi_dung.md").read_text(encoding="utf-8")
    blocks=[m[0] for m in re.finditer(r"(?m)(?:^\|.*\n)+",draft) if re.search(r"\\(?:nearrow|searrow|rightarrow)",m[0])]
    records=json.loads((p/"du_lieu/bang_bien_thien.json").read_text(encoding="utf-8"))
    values={"approved BBT inventory":len(blocks)==len(records)}
    for block,record in zip(blocks,records):
        rows=[[_clean(v) for v in line.strip("|").split("|")] for line in block.splitlines()
              if not re.fullmatch(r"[| :\-]+",line)]
        name=record["id"]
        values[name+"/approved limits signs trends"]=_segments(rows)==_segments(record["rows"],True)
        values[name+"/provided row count"]=len(rows)==len(record["rows"])
        expected_excluded=[]
        if rows[0][0]!="x":
            intervals=rows[0][1:]
            for i in range(len(intervals)-1):
                if intervals[i].endswith(")") and intervals[i+1].startswith("("):
                    expected_excluded.append(2*i+3)
        values[name+"/excluded points"]=expected_excluded==record.get("excluded_columns",[])

        # Preserve every explicitly supplied derivative zero/status at a point.
        if rows[0][0]=="x" and len(rows)==3:
            values[name+"/provided point derivative"]=rows[1]==[[_clean(v) for v in rr] for rr in record["rows"]][1]
    return values

def self_test(page=None):
    import copy
    from unittest.mock import patch
    source=ROOT/BASE/"r1_g04/index.qmd"
    good=source_checks(source)
    results={"current source accepted":bool(good) and all(good.values())}
    manifest=source.parent/"giao_dien/hinh_manifest.json"
    native=source.parent/"du_lieu/bang_bien_thien.json"
    binding=ROOT/KIT/"profiles/course-tables.json"
    original_read=Path.read_text
    def reject(name,target,change):
        data=json.loads(original_read(target,encoding="utf-8"))
        change(data)
        def read(path,*args,**kwargs):
            if path.resolve()==target.resolve():return json.dumps(data,ensure_ascii=False)
            return original_read(path,*args,**kwargs)
        try:
            with patch.object(Path,"read_text",read):
                checks=source_checks(source)
            results[name]=not all(checks.values())
        except (ValueError,KeyError,OSError):
            results[name]=True
    reject("body may not use cover surface",manifest,lambda d:d["figures"][0].update(surface="transparent-light"))
    reject("body must declare lesson role",manifest,lambda d:d["figures"][0].update(role="cover"))
    reject("missing dependency receipt rejected",manifest,lambda d:d.pop("source_hashes"))
    reject("missing paired graph PDF rejected",manifest,lambda d:d["figures"][0].pop("pdf"))
    reject("changed paired graph PDF hash rejected",manifest,lambda d:d["figures"][0].update(pdf_sha256="changed"))
    for token in ("sinh_hinh.py","zo_graph_v04.tex","STIXTwoMath.otf"):
        reject("changed dependency rejected "+token,manifest,
               lambda d,token=token:d["source_hashes"].update({next(k for k in d["source_hashes"] if k.endswith(token)):"changed"}))
    reject("empty BBT JSON rejected",native,lambda d:d.clear())
    reject("missing BBT record rejected",native,lambda d:d.pop())
    reject("one sided limit corruption rejected",native,
           lambda d:d[2]["rows"][-1].__setitem__(2,"↘ 0"))
    reject("excluded point removed rejected",native,lambda d:d[2].pop("excluded_columns"))
    reject("derivative row invented rejected",native,
           lambda d:d[5]["rows"].insert(1,["f′(x)"]+[""]*(len(d[5]["rows"][0])-1)))
    reject("ordinary variation binding rejected",binding,
           lambda d:d["pages"]["r1_g04"].append({"selector":"#g04-table-04 table","kind":"variation","role":"Bảng biến thiên"}))
    results["new package automatically governed"]=governed(ROOT/BASE/"r2_g01/index.qmd")
    results["legacy exemptions explicit"]=not governed(ROOT/BASE/"r1_g01/index.qmd")
    import zo_web_2027_figures as figures
    config=json.loads(figures.CONFIG.read_text(encoding="utf-8"))
    figures.verify(config);results["existing G01 graph cache still valid"]=True
    actual=figures.dependencies(config)
    for kind,suffix,accepted in [("native","zo_variation_build.py",True),("font","STIXTwoMath.otf",False),("graph","do_thi_01.tex",False),("style","zo_graph_v04.tex",False)]:
        changed=dict(actual);changed[next(k for k in changed if k.endswith(suffix))]="changed"
        try:
            with patch.object(figures,"dependencies",return_value=changed):figures.verify(config)
            valid=True
        except ValueError:valid=False
        results["cache dependency "+kind]=valid==accepted
    renderer=load_variation_html("math_token_regression",ROOT)
    for token,expected in [("2 ↘","\\searrow"),("+∞ ↘","\\infty"),("↗ +∞","\\infty")]:
        actual=renderer.math_token(token)
        results["compound token rendered as math "+token]=actual.startswith("$") and expected in actual
    if page:
        doc=BeautifulSoup(Path(page).read_text(encoding="utf-8"),"html.parser")
        results["fresh HTML accepted"]=all(html_checks(doc,"r1_g04").values())
        broken=copy.deepcopy(doc);broken.body["class"]=[c for c in broken.body.get("class",[]) if c!="zo-web-2027-production"]
        results["stylesheet namespace removed rejected"]=not all(html_checks(broken,"r1_g04").values())
        broken=copy.deepcopy(doc);broken.select_one(".figure-viewport img")["style"]="--figure-em:20em"
        results["old graph sizing rejected"]=not all(html_checks(broken,"r1_g04").values())
        broken=copy.deepcopy(doc);broken.select_one("table.zo-variation-native")["class"]=["zo-course-table"]
        results["native class removed rejected"]=not all(html_checks(broken,"r1_g04").values())
        broken=copy.deepcopy(doc);broken.select_one("table.zo-variation-native td")["data-source-value"]="changed"
        results["HTML data mismatch rejected"]=not all(html_checks(broken,"r1_g04").values())
    return results



def legacy_graph_checks(source,repo=ROOT):
    """Preserve legacy content adapters while enforcing current graph dependencies."""
    from zo_graphics import load_graph
    p=Path(source).parent;engine=load_graph('legacy_graph_source_gate',repo);values={}
    try:
        if p.name=='r1_g01':
            from zo_web_2027_figures import verify_print
            verify_print();c=json.loads((p/'giao_dien/web_2027_figures.json').read_text('utf-8'));files=[p/c['asset_directory']/(n+'.pdf') for n in c['graphs']]
        elif p.name=='r1_g02':
            from zo_web_2027_g02_payloads import verify_print
            verify_print();c=json.loads((p/'giao_dien/web_2027_figures.json').read_text('utf-8'));files=[p/'giao_dien/assets/figures_0_4'/(Path(v['source']).stem+'.pdf') for v in c['figures'] if v['role']!='cover']
        else:
            from zo_course_graph_refresh import inputs
            m=json.loads((p/'giao_dien/hinh_manifest.json').read_text('utf-8'));values['current owned graph tool dependencies']=m.get('source_hashes')==inputs(repo);files=[]
            for v in m['figures']:
                for key in ['input','pdf','svg']:values[v['name']+'/'+key+' hash']=digest(p/v[key])==v[key+'_sha256']
                files.append(p/v['pdf'])
        values['current graph cache']=True
        for pdf in files:values[pdf.stem+'/no endpoint tick strokes']=engine.graph_axis_check(pdf)['passed']
    except (OSError,ValueError) as exc:values['current graph cache: '+str(exc)]=False
    return values

if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--self-test",action="store_true");ap.add_argument("--html",type=Path)
    ap.add_argument("--report",type=Path);args=ap.parse_args()
    values=self_test(args.html)
    result={"checks":values,"passed":sum(values.values()),"total":len(values),"failures":[k for k,v in values.items() if not v]}
    if args.report:args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k!="checks"},ensure_ascii=False))
    raise SystemExit(bool(result["failures"]))

"""Canonical graph data -> paired SVG/PDF assets through the ZO Math graph adapter."""
from pathlib import Path
import argparse, concurrent.futures, hashlib, io, json, math, shutil, subprocess, sys, tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[6]/"scripts"))
import sympy as sp
from PIL import Image, ImageDraw

PACKAGE=Path(__file__).resolve().parent.parent
ROOT=PACKAGE/"hinh"
OUTPUT=PACKAGE/"giao_dien/assets/figures_0_4"
REPO=next(p for p in ROOT.parents if (p/"scripts/zo_python.py").is_file())
EVIDENCE=PACKAGE/"_quy_trinh/ho_so"
x=sp.Symbol("x",real=True)
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def number(v):return f"{float(v):.9g}"
def make_source(s):
    f=sp.sympify(s["expr"],locals={"x":x});df=sp.diff(f,x)
    actual=[v for v in sp.solve(sp.together(df).as_numer_denom()[0],x) if v.is_real]
    actual=[v for v in actual if s["pole"] is None or v!=s["pole"]]
    if not s["domain"]:
        assert set(actual)=={sp.Integer(p[0]) for p in s["critical"]},s["id"]
    for px,py in s["critical"]:
        assert sp.simplify(f.subs(x,px)-py)==0 and df.subs(x,px)==0,s["id"]
    if s["center"]:
        cx,cy=s["center"];assert sp.simplify(f+f.subs(x,2*cx-x)-2*cy)==0
    roots=[v for v in sp.solve(sp.together(f).as_numer_denom()[0],x) if v.is_real]
    roots=[v for v in roots if s["pole"] is None or v!=s["pole"]]
    pts=[(float(v.evalf()),0) for v in roots]+s["critical"]
    if s["pole"]!=0 and not s["domain"]:pts.append((0,float(f.subs(x,0))))
    if s["domain"]:
        lo,hi=s["domain"];pts=[(lo,float(f.subs(x,lo)))]
        if hi is not None:pts.append((hi,float(f.subs(x,hi))))
        xmin,xmax=-1,(hi+2 if hi is not None else 20)
        ymin,ymax=-1,max(p[1] for p in pts)+2
    else:
        cx,cy=s["center"]
        xmin=math.floor(min([0,cx-3]+[p[0] for p in pts]))-1
        xmax=math.ceil(max([0,cx+3]+[p[0] for p in pts]))+1
        ymin=math.floor(min([0,cy-3]+[p[1] for p in pts]))-1
        ymax=math.ceil(max([0,cy+3]+[p[1] for p in pts]))+1
    from zo_graphics import lesson_layout
    layout=lesson_layout(REPO)
    xticks=set();yticks=set()
    for px,py in pts+s["critical"]+([s["center"]] if s["center"] else []):
        if abs(px-round(px))<1e-8 and px!=0:xticks.add(round(px))
        if abs(py-round(py))<1e-8 and py!=0:yticks.add(round(py))
    def sparse(values):
        chosen=[]
        for v in sorted(values):
            if not chosen or v-chosen[-1]>=1:chosen.append(v)
        return ",".join(map(str,chosen))
    if s["line"] and not sp.sympify(s["line"],locals={"x":x}).has(x):
        level=float(sp.sympify(s["line"]))
        if level!=0 and abs(level-round(level))<1e-8:yticks.add(round(level))
    bounds=[xmin,xmax] if s["pole"] is None else [xmin,s["pole"],xmax]
    if s["domain"]:bounds=[s["domain"][0],s["domain"][1] or xmax]
    lines=[r"\documentclass[tikz,border=3pt]{standalone}",r"\usepackage{fontspec}",
      r"\usepackage{unicode-math}",r"\usepackage{pgfplots}",r"\pgfplotsset{compat=1.18}",
      r"\usetikzlibrary{backgrounds,arrows.meta}",r"\input{zo_graph_v02.tex}",
      r"\begin{document}",r"\begin{tikzpicture}[zo graph v02 field]",r"\zoGraphVTwoLayers",
      r"\begin{axis}[zo graph v02 axis,",
      f"width={layout['frame_width_cm']}cm,height={layout['frame_height_cm']}cm,",
      f"xmin={xmin},xmax={xmax},ymin={ymin},ymax={ymax},",
      f"restrict y to domain={ymin}:{ymax},unbounded coords=jump,",
      f"xtick={{{sparse(xticks)}}},ytick={{{sparse(yticks)}}},",
      "xlabel={$x$},ylabel={"+("$A$" if s["domain"] else "$y$")+"},",
      r"every axis x label/.append style={at={(axis description cs:1,"+number((0-ymin)/(ymax-ymin))+r")},anchor=south west,xshift=5pt,yshift=4pt},",
      r"every axis y label/.append style={at={(axis description cs:"+number((0-xmin)/(xmax-xmin))+r",1)},anchor=south west,xshift=4pt,yshift=4pt}",
      "]",r"\node[zo graph v02 font sentinel] at (axis cs:0,0) {x};"]
    if s["pole"] is not None and s["pole"]!=0:
        lines.append(r"\addplot[zo graph v02 asymptote,forget plot] coordinates {("+f"{s['pole']},{ymin}"+") ("+f"{s['pole']},{ymax}"+")};")
    if s["line"]:
        line=sp.sympify(s["line"],locals={"x":x})
        assert all(sp.limit(f-line,x,e)==0 for e in [-sp.oo,sp.oo])
        lines.append(r"\addplot[zo graph v02 asymptote,domain="+f"{xmin}:{xmax}"+r",samples=2,forget plot] {"+s["line"].replace("**","^")+"};")
    for lo,hi in zip(bounds,bounds[1:]):
        eps=0.008 if s["pole"] is not None else 0
        if s["domain"]:eps=0
        lines.append(r"\addplot[zo graph v02 curve solid,domain="+f"{number(lo+eps)}:{number(hi-eps)}"+r",samples=501,forget plot] {"+s["expr"].replace("**","^")+"};")
    points=sorted({tuple(map(float,p)) for p in pts})
    if points:
        coords=" ".join("("+number(px)+","+number(py)+")" for px,py in points)
        lines.append(r"\addplot[zo graph v02 point,forget plot] coordinates {"+coords+"};")
    if s["center"]:
        cx,cy=s["center"]
        lines.append(r"\addplot[only marks,mark=x,mark size=2.3pt,draw=zoGraphVTwoText,line width=0.6pt,on layer=zoGraphVTwoMarkerLayer,forget plot] coordinates {("+f"{cx},{cy}"+")};")
    lines.append(r"\begin{pgfonlayer}{zoGraphVTwoTextLayer}")
    if s["center"]:
        slanted=s["pole"] is not None and s["line"] and sp.sympify(s["line"],locals={"x":x}).has(x)
        rising=s["pole"] is None and df.subs(x,cx)>0
        label_style="anchor=south east,xshift=-7pt,yshift=7pt" if slanted or rising else "anchor=south west,xshift=7pt,yshift=7pt"
        lines.append(r"\node[zo graph v02 protected label,"+label_style+"] at (axis cs:"+f"{cx},{cy}"+r") {$I$};")
    lines.extend([r"\node[zo graph v02 tick label,anchor=north east,xshift=-3pt,yshift=-3pt] at (axis cs:0,0) {$O$};",
      r"\end{pgfonlayer}",r"\end{axis}",r"\end{tikzpicture}",r"\end{document}"])
    header="% Generated from du_lieu/hinh_do_thi.json; edit data or _quy_trinh/sinh_hinh.py.\n"
    header+="% Purpose: "+s["purpose"]+"\n% Profile: ZO Math 0.4, paper; lesson-g03 physical frame, mathematical windows preserved.\n"
    source=ROOT/(s["id"]+".tex");source.write_text(header+"\n".join(lines)+"\n",encoding="utf-8")
    return {"id":s["id"],"source":source.name,"formula":str(f),"derivative":str(sp.factor(df)),
      "roots":[str(v) for v in roots],"critical":[[str(v),str(f.subs(x,v))] for v in actual],
      "view":[xmin,xmax,ymin,ymax],"frame_cm":[layout["frame_width_cm"],layout["frame_height_cm"]],"axis_unit_cm":[layout["frame_width_cm"]/(xmax-xmin),layout["frame_height_cm"]/(ymax-ymin)],"purpose":s["purpose"]}
def build(s):
    rec=make_source(s)
    with tempfile.TemporaryDirectory(prefix="zo_g04_official_",dir=REPO/".quarto") as tmp:
        cmd=[sys.executable,str(REPO/"scripts/zo_python.py"),"-B",str(REPO/"scripts/zo_graphics.py"),
          "graph",str(ROOT/rec["source"]),"--style","0.4","--surface","paper","--layout","lesson-g03","--check","--out-dir",tmp]
        run=subprocess.run(cmd,cwd=REPO,text=True,encoding="utf-8",errors="replace",capture_output=True)
        if run.returncode:raise RuntimeError(s["id"]+"\n"+run.stdout+run.stderr)
        shutil.copy2(Path(tmp)/(s["id"]+".svg"),OUTPUT/(s["id"]+".svg"))
        shutil.copy2(Path(tmp)/(s["id"]+".pdf"),OUTPUT/(s["id"]+".pdf"))
        rec.update({"svg_sha256":H(OUTPUT/(s["id"]+".svg")),
          "pdf_sha256":H(OUTPUT/(s["id"]+".pdf")),"tool_check":"passed",
          "style":"0.4","surface":"paper","pdf_retained":True})
    print("built "+s["id"],flush=True);return rec
def previews(specs):
    images=[]
    for s in specs:
        out=subprocess.run(["rsvg-convert",str(OUTPUT/(s["id"]+".svg"))],check=True,capture_output=True)
        im=Image.open(io.BytesIO(out.stdout)).convert("RGBA")
        # Body figures use the shared paper frame; approved cover is separate.
        images.append((s["id"],im))
    for k in range(0,len(images),6):
        sheet=Image.new("RGB",(1800,1800),"white");draw=ImageDraw.Draw(sheet)
        for j,(label,im) in enumerate(images[k:k+6]):
            im.thumbnail((570,825));px=(j%3)*600+(600-im.width)//2;py=(j//3)*900+35
            sheet.paste(im,(px,py),im);draw.text(((j%3)*600+15,(j//3)*900+8),label,fill="black")
        sheet.save(EVIDENCE/f"xem_hinh_khung_g03_{k//6+1:02d}.png")
def main():
    parser=argparse.ArgumentParser();parser.add_argument("ids",nargs="*");parser.add_argument("--workers",type=int,default=3);args=parser.parse_args()
    from zo_course_math_assets import graph_inputs, canonical_digest
    inputs_before=graph_inputs(PACKAGE,REPO)
    specs=json.loads((PACKAGE/"du_lieu/hinh_do_thi.json").read_text(encoding="utf-8"))
    selected=[s for s in specs if not args.ids or s["id"] in args.ids]
    assert selected and set(args.ids)<={s["id"] for s in specs}
    previous=json.loads((PACKAGE/"giao_dien/hinh_manifest.json").read_text(encoding="utf-8"))
    if args.ids and previous.get("source_hashes")!=inputs_before:
        raise ValueError("Shared graph inputs changed; select all figures to avoid mixed provenance")

    (REPO/".quarto").mkdir(exist_ok=True)
    report=EVIDENCE/"kiem_hinh_khung_g03_20261017.json"
    prior=json.loads(report.read_text(encoding="utf-8")) if report.exists() else []
    kept=[r for r in prior if r["id"] not in {s["id"] for s in selected}]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        records=list(pool.map(build,selected))
    if graph_inputs(PACKAGE,REPO)!=inputs_before:
        raise ValueError("Graph inputs changed during generation; refuse a mixed receipt")
    report.write_text(json.dumps(sorted(kept+records,key=lambda r:r["id"]),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    from zo_course_math_assets import graph_inputs, canonical_digest
    manifest_path=PACKAGE/"giao_dien/hinh_manifest.json"
    manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
    by_id={s["id"]:s for s in specs}
    selected_ids={s["id"] for s in selected}
    for figure in manifest["figures"]:
        if figure["name"] not in selected_ids:continue
        pdf="giao_dien/assets/figures_0_4/"+figure["name"]+".pdf"
        figure.update({"input_sha256":H(PACKAGE/figure["input"]),"svg_sha256":H(PACKAGE/figure["svg"]),
                       "pdf":pdf,"pdf_sha256":H(PACKAGE/pdf),
                       "role":"lesson","style":"0.4","surface":"paper","layout":"lesson-g03",
                       "spec_sha256":canonical_digest(by_id[figure["name"]])})
    manifest["tool"]="scripts/zo_graphics.py graph --style 0.4 --surface paper --layout lesson-g03 --check"
    manifest["source_hashes"]=inputs_before
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if all((OUTPUT/(s["id"]+".svg")).exists() for s in specs):previews(specs)
if __name__=="__main__":main()

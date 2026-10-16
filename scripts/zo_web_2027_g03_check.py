"""Scoped source and fresh-HTML checks for R1-G03; never publishes or accepts."""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path
from urllib.parse import unquote, urlsplit
from bs4 import BeautifulSoup
import yaml
from zo_web_2027_preview import REPO, sha
from zo_web_2027_g03 import PACKAGE, ROLES
from zo_math_notation import math_errors, outline_errors

MATH=re.compile(r"\$\$(.*?)\$\$|\$(.*?)\$",re.S)
def formulas(text):
    text=re.sub(r"^!\[.*$","",text,flags=re.M)
    return ["".join(v.split()) for pair in MATH.findall(text) for v in pair if v]

def checks(page, output_root):
    package=REPO/PACKAGE
    source=(package/"index.qmd").read_text(encoding="utf-8")
    draft=(package/"_quy_trinh/ban_thao/noi_dung.md").read_text(encoding="utf-8")
    binding=json.loads((package/"giao_dien/he_nhan.json").read_text(encoding="utf-8"))
    doc=BeautifulSoup(page.read_text(encoding="utf-8"),"html.parser")
    root=doc.select_one(".reader-content")
    if root is None:return {"canonical reading root exists":False}, {}
    ids=[n["id"] for n in doc.select("[id]")]
    result={"canonical shell applied":doc.body.get("data-zo-web-production")=="R1-G03",
            "draft preserved as math reference":formulas(source.split("---",2)[2])==formulas(draft),
            "native math sequence preserved":formulas(source.split("---",2)[2])==["".join(n.get_text().split()) for n in root.select("annotation")],
            "notation valid":not math_errors(source),
            "unique DOM IDs":len(ids)==len(set(ids)),
            "all original anchors retained":set(re.findall(r'<a id="([^"]+)"',draft))<=set(ids),
            "all reading roles present":all(root.find(id=key) is not None for key in ROLES),
            "no nested reading papers":not root.select(".reading-region .reading-region"),
            "all headings owned":all(n.find_parent(class_="reading-region") for n in root.select("h2,h3,h4,h5,h6")),
            "all disclosures initially closed":not root.select("details[open]"),
            "all tables explicitly classified":all(n.has_attr("data-table-kind") for n in root.select("table")),
            "no executable draft dependency":"_quy_trinh/ban_thao" not in str(doc) and "_audit/" not in str(doc),
            "no package PDF invented":not root.select('a[download]'),
            "fallback navigation available":bool(doc.select("noscript nav a"))}
    lesson=root.find(id="bai-hoc")
    result["controller lesson heading count"]=len(lesson.select("h3"))==int(root["data-r1-lesson-count"])
    # Presentation regressions found by comparing the accepted G01 shell.
    orientation=root.select("details.r1-lesson-orientation")
    result["G01 orientation component"]=len(orientation)==1 and not orientation[0].has_attr("open")
    result["G01 execution guidance components"]=len(root.select("details.r1-guidance"))==7
    result["G01 disclosure body and title"]=all(n.select_one(":scope > summary.zo-block-title") and n.select_one(":scope > .zo-block-body") for n in root.select("details"))
    result["G01 definitions stay open"]=len(root.select('[data-zo-type="definition"] .zo-block-red'))==3 and not any(n.find_parent("details") for n in root.select('[data-zo-type="definition"] .zo-block-red'))
    page_labels=json.loads((REPO/"_design/web_2027_mau_dung_chung/profiles/r1-consistency.json").read_text(encoding="utf-8"))["page_roles"]
    for anchor,key in {"bat-dau":"Bắt đầu","bai-hoc":"Bài học","phieu-luyen":"Luyện tập","nguon":"Nguồn đối chiếu"}.items():
        title=root.find(id=anchor).find("h2")
        label=title.find_previous_sibling(attrs={"data-reading-label":True})
        result["G01 area label "+anchor]=bool(label and label.get_text(strip=True)==page_labels[key])
    result["Vietnamese source notes"]=bool(root.select_one(".footnotes h2") and root.select_one(".footnotes h2").get_text(strip=True)=="Chú thích nguồn")
    foundations=root.select("#on-nen details.r1-foundation-unit")
    result["G02 foundation resources collapsed"]=len(foundations)==3 and all(not n.has_attr("open") for n in foundations)
    kickoff=root.find(id="khởi-động").find("h3")
    kickoff_label=kickoff.find_previous_sibling(attrs={"data-reading-label":True})
    result["G02 kickoff group label"]=bool(kickoff_label and kickoff_label.get_text(strip=True)=="Bài học · Khởi động")
    test_heading=root.find(id="tu-kiem-tra").find("h2")
    result["test area not lesson self-check"]=not test_heading.find_previous_sibling(attrs={"data-reading-label":True})
    result["semantic support context opt-in"]=root.get("data-r1-support-context")=="semantic"
    result["all checkpoint return labels"]=all(n.get("data-r1-return-label") for n in root.select('[data-zo-type="checkpoint"][id]'))
    controller=(REPO/"_design/web_2027_mau_dung_chung/r1-controller.js").read_text(encoding="utf-8")
    result["semantic support controller installed"]='root.dataset.r1SupportContext' in controller and '[data-r1-return-label][id]' in controller
    from zo_course_labels import html_checks, binding_checks
    result.update({"labels/"+k:v for k,v in binding_checks(binding).items()})
    result.update({"labels/"+k:v for k,v in html_checks(doc,binding).items()})
    failures=[]
    for unit in binding["units"]:
        owner=root.find(id=unit["question"])
        result["task "+unit["id"]+" has one owner"]=len(root.select('[data-zo-task="'+unit["id"]+'"][data-zo-type="task"]'))==1
        result["task "+unit["id"]+" function valid"]=owner is not None and owner.get("data-zo-function")==unit["function"]
        if unit.get("answer"):
            answer=root.find(id=unit["answer"])
            forward=owner.select('a[href="#'+unit["answer"]+'"]') if owner else []
            if unit["function"]=="function.test":
                # The test keeps answers out of its individual questions;
                # the post-test checkpoint owns the grouped solution action.
                forward=root.select('#CPK a[href="#lg-kiem-tra"]')
            result["pair "+unit["id"]+" complete"]=bool(owner and answer and forward and answer.select('a[href="#'+unit["question"]+'"]'))
    for node in doc.select("a[href],img[src],script[src],link[href]"):
        value=node.get("src",node.get("href"));url=urlsplit(value)
        if url.scheme or url.netloc:continue
        target=(page.parent/unquote(url.path)).resolve() if url.path else page
        if not target.is_file() and target.is_relative_to(output_root):target=REPO/"docs"/target.relative_to(output_root)
        if not target.is_file():failures.append(value);continue
        if url.fragment and target.suffix==".html":
            dest=doc if target==page else BeautifulSoup(target.read_text(encoding="utf-8"),"html.parser")
            if not dest.find(id=unquote(url.fragment)):failures.append(value)
    result["local resources and fragments resolve"]=not failures
    vectors=json.loads((package/"giao_dien/hinh_manifest.json").read_text(encoding="utf-8"))
    for fig in vectors["figures"]:
        result["figure provenance "+fig["name"]]=all(sha(package/fig[key])==fig[key+"_sha256"] for key in ["input","svg","pdf"])
        text=(package/fig["input"]).read_text(encoding="utf-8")
        limits={key:float(value) for key,value in re.findall(r"(xmin|xmax|ymin|ymax)=(-?[\d.]+)",text)}
        result["axes interior "+fig["name"]]=limits["xmin"]<0<limits["xmax"] and limits["ymin"]<0<limits["ymax"]
    details={"broken_links":failures,"math_count":len(root.select("annotation")),"tables":len(root.select("table")),"figures":len(root.select("img")),"disclosures":len(root.select("details")),"reading_regions":len(root.select(".reading-region")),"source_sha256":sha(package/"index.qmd"),"html_sha256":sha(page)}
    return result,details

def main():
    parser=argparse.ArgumentParser();parser.add_argument("html",type=Path);parser.add_argument("--output-root",type=Path,required=True);parser.add_argument("--report",type=Path)
    args=parser.parse_args();values,details=checks(args.html.resolve(),args.output_root.resolve())
    report={"checks":values,"details":details,"passed":sum(values.values()),"total":len(values),"owner_acceptance":"pending","learning_pdf_built":False,"published":False}
    if args.report:
        target=args.report.resolve()
        if not target.is_relative_to(REPO/"_audit"):raise ValueError("Report must stay in _audit")
        target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"passed":report["passed"],"total":report["total"],"failures":[k for k,v in values.items() if not v],"details":details},ensure_ascii=False))
    return int(not all(values.values()))
if __name__=="__main__":raise SystemExit(main())

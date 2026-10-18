"""Regression/negative cases for QD_025 source and visible label gates."""
from pathlib import Path
import argparse,copy,json
from unittest.mock import patch
from bs4 import BeautifulSoup
from zo_course_labels import ROOT,binding,binding_checks,display_label,contract,html_checks,source_checks,require,context_unit_label


def run(page):
    source=ROOT/"content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g03/index.qmd"
    data=binding(source);doc=BeautifulSoup(page.read_text(encoding="utf-8"),"html.parser");results={}
    results["current source passes"]=all(source_checks(source).values())
    results["current visible labels pass"]=all(html_checks(doc,data).values())
    for code in ["01","02"]:
        package=Path("content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g"+code)
        old=binding(ROOT/package/"index.qmd")
        results["G"+code+" existing binding compatible"]=all(binding_checks(old).values())
        previous=BeautifulSoup((ROOT/"docs"/package/"index.html").read_text(encoding="utf-8"),"html.parser")
        if code=="01":from zo_r1_g01_labels_check import predicates
        else:from zo_r1_g02_labels_check import predicates
        # Published HTML is a historical product after a numbering revision;
        # it must not certify the new binding without a fresh render.
        try:current=all(html_checks(previous,old).values())
        except (ValueError,KeyError):current=False
        results["G"+code+" stale public labels rejected"]=not current
    broken=copy.deepcopy(doc)
    for label in list(broken.select("[data-reading-label]")):label.decompose()
    results["metadata-only old failure rejected"]=not all(html_checks(broken,data).values())
    broken=copy.deepcopy(doc);unit=next(u for u in data["units"] if u["function"]=="function.practice")
    broken.find(id=unit["question"]).select_one("[data-reading-label]").string="KIỂM TRA"
    results["wrong visible context rejected"]=not all(html_checks(broken,data).values())
    bad=copy.deepcopy(data);u=next(u for u in bad["units"] if u["function"]=="function.practice");u.pop("context")
    results["missing binding context rejected"]=not all(binding_checks(bad).values())
    bad=copy.deepcopy(data);u=next(u for u in bad["units"] if u["function"]=="function.practice");u["context"]={"stage":2};u["label"]=display_label(u,contract()["display_contract"])
    results["self-consistent label in wrong source stage rejected"]=not all(html_checks(doc,bad).values())
    bad=copy.deepcopy(data);u=next(u for u in bad["units"] if u["function"]=="function.remediation");u["number"]=1
    results["number reset after context rejected"]=not all(binding_checks(bad).values())
    bad=copy.deepcopy(data);bad["units"][0]["question_owner"]="nguon"
    results["wrong structural owner rejected"]=not all(html_checks(doc,bad).values())
    broken=copy.deepcopy(doc);example=data["examples"][0];node=broken.find(id=example["anchor"])
    label=broken.new_tag("span",attrs={"class":"role","data-reading-label":""});label.string="Ví dụ";node.append(label)
    results["redundant example label rejected"]=not all(html_checks(broken,data).values())
    broken=copy.deepcopy(doc);broken.select_one("[data-reading-label]")["hidden"]=""
    results["hidden label workaround rejected"]=not all(html_checks(broken,data).values())
    broken=copy.deepcopy(doc);u=next(u for u in data["units"] if u["function"]=="function.practice");label=broken.find(id=u["question"]).select_one("[data-reading-label]");label["class"]=[]
    results["unstyled label rejected"]=not all(html_checks(broken,data).values())
    values=source_checks(ROOT/"content/thpt/on_thi_toan_thpt/hoc_lieu/r9_g999/index.qmd")
    results["future package without binding rejected"]=bool(values) and not all(values.values())
    with patch("zo_course_labels.binding",side_effect=FileNotFoundError("missing label binding")):
        results["missing current binding rejected"]=not all(source_checks(source).values())
    # Group size is content-owned, not copied from G01/G02.
    small=copy.deepcopy(data);small["units"]=[u for u in small["units"] if u["function"]=="function.practice"][:2]
    for i,u in enumerate(small['units'],1):
        import re
        u['number']=i
        for key in ['title','answer_title']:
            if key in u:u[key]=re.sub(r'Nhiệm vụ \d+',f'Nhiệm vụ {i:02d}',u[key])
    results["arbitrary group size accepted without quota"]=all(binding_checks(small).values())
    confirmation=copy.deepcopy(small);confirmation["units"]=confirmation["units"][:1];unit=confirmation["units"][0]
    unit["function"]="function.confirmation";unit["context"]={"within":"area.lesson"};unit["context_area"]='bai-hoc'
    unit["label"]=context_unit_label(unit,'question',confirmation)
    results["confirmation context not hard-coded to practice"]=unit["label"]=="MẠCH HỌC · BÀI HỌC" and all(binding_checks(confirmation).values())
    results["other QMD projects unaffected"]=source_checks(ROOT/"content/about.qmd")=={}
    return results

if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--html",type=Path,required=True);ap.add_argument("--report",type=Path);args=ap.parse_args();values=run(args.html.resolve())
    diagnostics={k:v for k,v in values.items() if not isinstance(v,bool)};checks={k:v for k,v in values.items() if isinstance(v,bool)}
    result={"passed":sum(checks.values()),"total":len(checks),"checks":checks,"diagnostics":diagnostics}
    if args.report:
        target=args.report.resolve()
        if not target.is_relative_to(ROOT/"_audit"):raise ValueError("Report belongs in _audit")
        target.write_bytes((json.dumps(result,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
    print(json.dumps({"passed":result["passed"],"total":result["total"],"failures":[k for k,v in checks.items() if not v],"diagnostics":diagnostics},ensure_ascii=False))
    raise SystemExit(int(not all(checks.values())))

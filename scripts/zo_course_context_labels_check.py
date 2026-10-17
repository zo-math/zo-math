
"""Read-only parent-context HTML and preservation checks for migrated packages."""
from pathlib import Path
import argparse,copy,json,re
from bs4 import BeautifulSoup
from zo_course_labels import binding,source_checks,context_html_checks,context_title_text
from zo_web_2027_preview import REPO,sha
from zo_web_2027_g04_check import deliver

def checks(page,package):
    src=REPO/'content/thpt/on_thi_toan_thpt/hoc_lieu'/package/'index.qmd'
    data=binding(src);doc=BeautifulSoup(page.read_text(encoding="utf-8"),"html.parser")
    reader=doc.select_one(".reader-content")
    old=BeautifulSoup((REPO/'docs'/src.relative_to(REPO).with_suffix(".html")).read_text(encoding="utf-8"),"html.parser")
    prior=old.select_one(".reader-content")
    values={"parent mode applied":reader.get("data-zo-context-labels")=="parent-context-v1"}
    values.update({"source/"+k:v for k,v in source_checks(src).items()})
    values.update(context_html_checks(doc,data))
    math=lambda n:["".join(x.get_text().split()) for x in n.select("annotation")]
    values["all prior mathematics retained in order"]=math(reader)==math(prior)
    values["all prior reader IDs retained"]={x["id"] for x in reader.select("[id]")}=={x["id"] for x in prior.select("[id]")}
    ids=[x["id"] for x in doc.select("[id]")];values["unique IDs"]=len(ids)==len(set(ids))
    def text(n):
        n=copy.deepcopy(n)
        for label in n.select("[data-reading-label],.zo-pdf-version-note,.zo-pdf-current-note"):label.decompose()
        return " ".join(n.get_text(" ",strip=True).split())
    values["learner text unchanged except labels and live PDF status"]=text(reader)==text(prior)
    values["all authored disclosures closed"]=not reader.select("details[open]")
    for u in data["units"]:
        for key in ["question","answer"]:
            target=u.get(key)
            if not target:continue
            node=reader.find(id=target)
            values[u["id"]+"/"+key+" identity"]=bool(node and node.get("data-zo-task")==u["id"] and node.get("data-zo-function")==u["function"] and (u.get("number") is None or node.get("data-zo-number")==str(u["number"])))
            field="answer_context_area" if key=="answer" else "context_area"
            if u.get(field):
                actual=next((n.get("id") for n in [node,*node.parents] if n.get("id") in ["bat-dau","bai-hoc","phieu-luyen","tu-kiem-tra","on-lai","on-nen","sua-loi","nhat-ky","loi-giai","nguon","tai-tai-lieu"]),None)
                values[u["id"]+"/"+key+" declared context area matches source"]=actual==u[field]
    kickoff=next((h for h in reader.select("#bai-hoc h3") if context_title_text(h)=="Khởi động"),None)
    values["kickoff exact approved context"]=bool(kickoff and kickoff.find_previous_sibling().get_text(" ",strip=True)=="MẠCH HỌC CHÍNH · BÀI HỌC")
    values["lesson exact approved context"]=reader.select_one("#bai-hoc h2").find_previous_sibling().get_text(" ",strip=True)=="MẠCH HỌC CHÍNH"
    from zo_pdf_contract import validate_canonical_pdf_provenance
    import yaml
    config=yaml.safe_load((src.parent/"_quy_trinh/cau_hinh_san_xuat_qmd.yml").read_text(encoding="utf-8"))
    variants={v["output"]:k for k,v in config["extensions"]["pdf_variants"].items()}
    cards=reader.select(".zo-pdf-card");values["eight retained PDF variants"]=len(cards)==8
    for card in cards:
        name=Path(card.select_one("a[download]")["href"]).name
        values["PDF state/"+name]=card.get("data-pdf-current")==str(not validate_canonical_pdf_provenance(REPO,src,variant=variants[name])).lower()
    return values,{"labels":len(reader.select("[data-reading-label]")),"source_sha256":sha(src),"binding_sha256":sha(src.parent/"giao_dien/he_nhan.json"),"html_sha256":sha(page)}

def main():
    ap=argparse.ArgumentParser();ap.add_argument("package");ap.add_argument("html",type=Path);ap.add_argument("--output-root",type=Path,required=True);ap.add_argument("--report",type=Path,required=True);ap.add_argument("--preview",type=Path);a=ap.parse_args()
    values,details=checks(a.html.resolve(),a.package);r={"checks":values,"details":details,"passed":sum(values.values()),"total":len(values),"failures":[k for k,v in values.items() if not v],"published":False,"PDF_built":False,"owner_review":"pending"}
    a.report.write_bytes((json.dumps(r,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
    if a.preview:deliver(a.html.resolve(),a.output_root.resolve(),a.preview.resolve())
    print(json.dumps({k:r[k] for k in ["passed","total","failures","details"]},ensure_ascii=False))
    return int(bool(r["failures"]))
if __name__=="__main__":raise SystemExit(main())

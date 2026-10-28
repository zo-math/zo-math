"""One visible set of learning goals in Bắt đầu, question-only lesson guide."""
from pathlib import Path
import hashlib,json,re,copy
ROOT=Path(__file__).resolve().parents[1]
TITLE="Học xong, em cần làm được gì?"
GUIDE_TITLE="Câu hỏi dẫn đường"
COLUMNS=["Mục tiêu","Việc em cần làm được"]
norm=lambda s:re.sub(r"\s+"," ",s).strip()
sha=lambda s:hashlib.sha256(s if isinstance(s,bytes) else s.encode("utf-8")).hexdigest()

def spec(path,root=ROOT):
    path=Path(path)
    from zo_course_labels import governed
    if path.name!="index.qmd" or not governed(path):return None
    return json.loads((path.parent/"giao_dien/he_nhan.json").read_text(encoding="utf-8"))["learning_goals"]

def source_checks(path,root=ROOT,text=None):
    path=Path(path);root=Path(root);b=spec(path,root)
    if b is None:return {}
    text=path.read_text(encoding="utf-8") if text is None else text
    checks={}
    start=text.split("## Bắt đầu {#bat-dau}",1)[-1].split("## Bài học {#bai-hoc}",1)[0]
    lesson=text.split("## Bài học {#bai-hoc}",1)[-1]
    marker=re.search(r"^(:{3,}) \{#"+re.escape(b["table"])+r" [^\n]+\}\n(.*?)^\1[ \t]*$",text,re.M|re.S)
    rows=[]
    if marker:
        rows=[[c.strip() for c in line.strip("|").split("|")] for line in marker.group(2).splitlines() if line.startswith("|") and not re.fullmatch(r"[| :\-]+",line)]
    checks["one goal table at Bắt đầu"]=bool(marker and marker.group(0) in start and text.count("{#"+b["table"]+" ")==1)
    checks["visible named goal heading"]=TITLE in start and "#"+b["heading"] in start
    checks["two common goal columns"]=bool(rows and rows[0]==COLUMNS)
    checks["all declared goals retained in order"]=[r[0] for r in rows[1:]]==[r["title"] for r in b["rows"]]
    checks["each goal has a concrete description"]=bool(rows) and all(len(r)==2 and r[1] for r in rows[1:])
    for i,row in enumerate(b["rows"],1):
        checks[f"goal {i} evidence anchors exist"]=bool(row["evidence"]) and all(re.search(r"\{#"+re.escape(a)+r"(?:[ \t}]|$)",text,re.M) for a in row["evidence"])
    legacy=re.search(r"^(:{3,}) \{#"+re.escape(b["guide"])+r" [^\n]+\}\n(.*?)^\1[ \t]*$",lesson,re.M|re.S)
    native=re.search(r'<details\b[^>]*\bid="'+re.escape(b["guide"])+r'"[^>]*>(.*?)</details>',lesson,re.S)
    guide=legacy.group(2) if legacy else native.group(1) if native else ""
    plain=b.get("guide_display")=="plain-introduction"
    visible=b.get("guide_display")=="always-visible"
    label="BÀI HỌC · CÂU HỎI DẪN ĐƯỜNG" if visible else GUIDE_TITLE
    checks["guide display is declared"]=b.get("guide_display","disclosure") in {"disclosure","always-visible","plain-introduction"}
    checks["question-only guide exists"]=bool(guide and (plain or label in guide) and "Định hướng bài học" not in guide)
    if visible:checks["guide is permanently visible in source"]=bool(legacy and ".zo-lesson-question" in legacy.group(0) and "<details" not in guide and "<summary" not in guide)
    checks["guide contains no goal table or chapter table"]=bool(guide) and not re.search(r"(?m)^\s*\||<table\b",guide)
    checks["no repeated guide label"]=label not in guide if plain else guide.count(label)==1
    if plain:
        checks["introduction is ordinary prose"]=bool(legacy and ".zo-lesson-intro" in legacy.group(0) and not re.search(r"(?m)^#{1,6} |\*\*|<details|<summary|zo-guide-label|\{\.role",guide))
    checks["no full goal list duplicated in guide"]=TITLE not in guide and not all(r["title"] in guide for r in b["rows"])
    if path.parent.name=="r1_g01":
        plan=json.loads((path.parent/"giao_dien/web_2027_layout.json").read_text(encoding="utf-8"))
        checks["G01 explicit current transition binding"]=plan.get("source_transition",{}).get("source_qmd_sha256")==sha(text.replace("\r\n","\n").replace("\n","\r\n").encode("utf-8")) if b"\r\n" in path.read_bytes() else plan.get("source_transition",{}).get("source_qmd_sha256")==sha(text)
    return checks

def html_checks(doc,b):
    root=doc.select_one(".reader-content");start=root.find(id="bat-dau") if root else None
    table=root.find(id=b["table"]) if root else None
    heading=root.find(id=b["heading"]) if root else None
    guide=root.find(id=b["guide"]) if root else None
    t=table.find("table") if table else None
    rows=[[c.get_text(" ",strip=True) for c in row.find_all(["th","td"],recursive=False)] for row in t.select("tbody tr")] if t else []
    plain=b.get("guide_display")=="plain-introduction"
    visible=b.get("guide_display")=="always-visible"
    label="BÀI HỌC · CÂU HỎI DẪN ĐƯỜNG" if visible else GUIDE_TITLE
    guide_title=guide.select_one(".zo-guide-label") if guide and visible else guide.find("summary") if guide else None
    plain_display=bool(guide and guide.name=="div" and "zo-lesson-intro" in guide.get("class",[]) and not guide.find_parent("details") and not guide.find(["summary","details","h1","h2","h3","h4","h5","h6","strong"]))
    return {
        "goals belong to Bắt đầu":bool(table and table.find_parent(id="bat-dau")),
        "goals visible without disclosure":bool(table and not table.find_parent("details")),
        "one correctly named goal heading":bool(heading and heading.find_parent(id="bat-dau") and heading.get_text(" ",strip=True)==TITLE),
        "goal columns":bool(t and [c.get_text(" ",strip=True) for c in t.select("thead th")]==COLUMNS),
        "all declared goal rows":[r[0] for r in rows]==[r["title"] for r in b["rows"]],
        "question-only guide":bool(guide and guide.find_parent(id="bai-hoc") and (plain or guide_title and guide_title.get_text(" ",strip=True)==label) and not guide.find("table")),
        "guide display matches binding":plain_display if plain else bool(guide and (guide.name=="div" and "zo-lesson-question" in guide.get("class",[]) and not guide.find_parent("details") and not guide.find(["summary","details"]) if visible else guide and not guide.has_attr("open"))),
        "guide label not repeated":bool(guide and (label not in guide.get_text(" ",strip=True) if plain else guide.get_text(" ",strip=True).count(label)==1)),
    }

def inverse_g01_fingerprint(source,plan,fingerprint,qmd):
    """Restore only approved moved prose/IDs for verification of the old receipt.

    Historical text is used in the comparison string only, never in the DOM
    or output. Math/disclosure fingerprints and every other word/ID stay strict.
    """
    change=plan.get("source_transition")
    if not change:return fingerprint(source)
    if change.get("id")!="GOALS-START-20261018" or sha(Path(qmd).read_bytes())!=change["source_qmd_sha256"]:
        raise ValueError("G01 goal transition does not match current canonical QMD")
    # Page counts are measured from PDFs; preserve the imported receipt while
    # comparing only this explicitly recorded metadata-only transition.
    page_transition=plan.get('metadata_pdf_transition')
    if page_transition:
        if page_transition.get('id')!='PDF-PAGES-SYNC-20261019' or page_transition.get('source_qmd_sha256')!=sha(Path(qmd).read_bytes()):raise ValueError('Unbound PDF page-count transition')
        source=copy.deepcopy(source)
        for item in page_transition['counts']:
            cards=[n for n in source.select('.r1-download-card') if n.select_one('a[download]') and n.select_one('a[download]')['href']==item['href']]
            if len(cards)!=1:raise ValueError('Missing/duplicate source download card: '+item['href'])
            label=cards[0].select_one('.r1-download-card__meta')
            if label is None or norm(label.get_text(' ',strip=True))!=str(item['after'])+' trang · PDF':raise ValueError('PDF page-count text differs from measured transition')
            label.string=str(item['before'])+' trang · PDF'
    current=fingerprint(source);text=norm(source.get_text(" ",strip=True))
    before,after=change["old_intro_text"],change["new_intro_text"]
    start=source.find(id="bat-dau");guide=source.find(id="dinh-huong-bai-hoc")
    if start is None or guide is None or after not in norm(start.get_text(" ",strip=True)) or text.count(after)!=1:
        raise ValueError("G01 current goal block differs from the approved source relocation")
    gtext=norm(guide.get_text(" ",strip=True));prefix=change["new_summary_prefix"];tail=change["scope_text"]
    if not gtext.startswith(prefix) or gtext.count(tail)!=1 or guide.find(id="r1-table-t02"):
        raise ValueError("G01 question guide differs from its bounded transition")
    oldguide=change["old_summary_prefix"]+gtext[len(prefix):]
    oldguide=oldguide.replace(tail,change["old_goal_text"]+" "+tail,1)
    restored=text.replace(after,before,1)
    if restored.count(gtext)!=1:raise ValueError("Ambiguous G01 guide transition")
    restored=restored.replace(gtext,oldguide,1)
    moved=set(change["relocated_ids"])
    ids=[v for v in current["ids"] if v not in moved]
    if any(current["ids"].count(v)!=1 for v in moved):raise ValueError("Lost or duplicated relocated G01 anchor")
    for index,ident in enumerate(plan["source_fingerprint"]["ids"]):
        if ident in moved:ids.insert(index,ident)
    result=copy.deepcopy(current);result["text_sha256"]=sha(restored);result["ids"]=ids
    return result

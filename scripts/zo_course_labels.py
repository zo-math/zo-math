"""QD_025 display projection and gates for reusable learning packages.

Vocabulary/display patterns live in the existing course catalog. Package
bindings own functions, contexts, numbering and titles; no package quotas.
G01/G02 keep their accepted legacy adapters and are compatibility references.
"""
from __future__ import annotations
import json,re
from collections import defaultdict
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
CATALOG=Path("content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/danh_muc_kien_truc_hoc_tap.yml")
VERSION="qd025-display-v1"
LEGACY={"r1_g01","r1_g02"}

def governed(path):
    path=Path(path)
    return path.name in {"index.qmd","index.html"} and bool(re.fullmatch(r"r[1-9]\d*_g\d+",path.parent.name)) and path.parent.parent.name=="hoc_lieu"

def contract(root=ROOT):
    return yaml.safe_load((root/CATALOG).read_text(encoding="utf-8"))["label_contract"]

def binding(path):
    return json.loads((Path(path).parent/"giao_dien/he_nhan.json").read_text(encoding="utf-8"))

def display_label(unit,policy):
    spec=policy["functions"][unit["function"]];label=spec["label"];kind=spec.get("context")
    if kind:
        value=unit["context"][kind]
        pattern=policy["contexts"][kind]
        suffix=pattern[value] if isinstance(pattern,dict) else pattern.format(number=value)
        label=suffix+policy["joiner"]+label if spec.get("context_position")=="prefix" else label+policy["joiner"]+suffix
    return label

def binding_checks(data,root=ROOT):
    vocab=contract(root);policy=vocab["display_contract"];checks={};numbers=defaultdict(list)
    units=data.get("units",[]);ids=[u.get("id") for u in units];targets=[u.get("question") for u in units]
    checks["nonempty unique task IDs/owners"]=bool(units) and None not in ids+targets and len(set(ids))==len(ids) and len(set(targets))==len(targets)
    strict=data.get("display_contract")==VERSION
    for u in units:
        key=u.get("id","missing");function=u.get("function");label=u.get("label")
        checks[key+" known function"]=function in policy["functions"]
        checks[key+" visible label specified"]=isinstance(label,str) and bool(label.strip())
        if function in policy["functions"] and label:
            if strict:
                try:expected=display_label(u,policy)
                except (KeyError,TypeError,ValueError):expected=None
                checks[key+" display context matches function"]=label==expected
            else:
                spec=policy["functions"][function];base=spec["label"]
                bases=[prefix+policy["joiner"]+base for prefix in policy["contexts"][spec["context"]].values()] if spec.get("context_position")=="prefix" else [base]
                checks[key+" legacy label compatible"]=any(label==b or label.startswith(b+policy["joiner"]) for b in bases)
        if function=="function.guided_thinking":checks[key+" no duplicate prompt answer"]=not u.get("answer")
        if strict:
            checks[key+" canonical task title specified"]=isinstance(u.get("title"),str) and bool(u["title"].strip())
            if u.get("answer"):checks[key+" canonical answer title specified"]=isinstance(u.get("answer_title"),str) and bool(u["answer_title"].strip())
        number=u.get("number")
        if number is not None:
            checks[key+" positive integer number"]=isinstance(number,int) and not isinstance(number,bool) and number>0
            numbers[function].append(number)
    for function,values in numbers.items():checks[function+" continuous numbering"]=sorted(values)==list(range(1,len(values)+1))
    for u in data.get("knowledge_units",[]):checks[u["id"]+" known content type"]=u.get("type") in vocab["terms"] and u["type"].startswith("type.")
    return checks

def expand(path,seen=None):
    path=Path(path).resolve();seen=set() if seen is None else seen
    if path in seen:raise ValueError("Cyclic QMD include")
    seen=seen|{path};text=path.read_text(encoding="utf-8")
    return re.sub(r"\{\{<\s*include\s+([^>]+?)\s*>\}\}",lambda m:expand(path.parent/m[1].strip(),seen),text)

def source_checks(path,root=ROOT):
    path=Path(path);checks={}
    if not governed(path) or path.parent.name in LEGACY:return checks
    try:data=binding(path);vocab=contract(root)
    except (OSError,ValueError,KeyError,yaml.YAMLError) as exc:return {"label binding/catalog readable: "+str(exc):False}
    checks.update(binding_checks(data,root));checks["display contract opt-in mandatory"]=data.get("display_contract")==VERSION
    text=expand(path)
    def has_anchor(ident):return bool(re.search(r"\{#"+re.escape(ident)+r"(?=[\s}])|\bid=[\"']"+re.escape(ident)+r"[\"']",text))
    for u in data.get("units",[]):
        checks[u["id"]+" source owner exists"]=has_anchor(u["question"])
        if u.get("answer"):checks[u["id"]+" answer exists"]=has_anchor(u["answer"])
        raw=re.search(r"\{#"+re.escape(u["question"])+r"(?=[\s}])([^}]*)\}",text)
        attrs=dict(re.findall(r'(data-zo-[\w-]+)="([^"]*)"',raw[0])) if raw else {}
        checks[u["id"]+" source function declared"]=attrs.get("data-zo-function")==u["function"] and attrs.get("data-zo-task")==u["id"]
        if u.get("number") is not None:checks[u["id"]+" source number matches binding"]=attrs.get("data-zo-number")==str(u["number"])
        owner=u.get("question_owner")
        checks[u["id"]+" source structural owner exists"]=isinstance(owner,str) and has_anchor(owner)
        if u.get("context") and isinstance(owner,str):
            own=re.search(r"\{#"+re.escape(owner)+r"(?=[\s}])([^}]*)\}",text)
            key,value=next(iter(u["context"].items()))
            checks[u["id"]+" source context matches binding"]=bool(own and 'data-zo-context="'+key+':'+str(value)+'"' in own[0])
    for anchor in data.get("checkpoints",{}):checks[anchor+" checkpoint exists"]=has_anchor(anchor)
    for u in data.get("knowledge_units",[]):
        checks[u["id"]+" source type/owner declared"]=has_anchor(u["anchor"]) and has_anchor(u["owner"]) and 'data-zo-unit="'+u["id"]+'"' in text
    declared=set(re.findall(r'data-zo-type="task"[^}]*data-zo-task="([^"]+)"',text))
    checks["all declared tasks mapped"]=declared=={u["id"] for u in data["units"]}
    checks["checkpoint mapping required"]=bool(data.get("checkpoints"))
    checks["knowledge/example mapping required"]="knowledge_units" in data and "examples" in data
    return checks

def require(values,stage):
    failed=[key for key,value in values.items() if not value]
    if failed:raise ValueError("QD_025 "+stage+": "+"; ".join(failed))
    return values

def plain_title(text):
    return re.sub(r"^\d+(?:\.\d+)*\.\s*","",text).strip()

def omit_type_label(title,type_name):
    title=plain_title(title).casefold();name=type_name.casefold()
    return title==name or title.startswith(name+" ")

def find_title(node,wording=None,selector=None):
    candidates=node.select(selector) if selector else node.select("h2,h3,h4,h5,h6,summary,p > strong")
    if wording is not None:candidates=[n for n in candidates if n.get_text(" ",strip=True)==wording]
    if len(candidates)!=1:raise ValueError("Ambiguous/missing owned title: "+str(wording))
    return candidates[0]

def put_label(doc,title,text):
    for prior in list(title.find_previous_siblings(attrs={"data-reading-label":True})):prior.decompose()
    label=doc.new_tag("span",attrs={"class":"role","data-reading-label":""});label.string=text;title.insert_before(label)

def apply(doc,data,area_labels=None,root=ROOT):
    require(binding_checks(data,root),"binding")
    if data.get("display_contract")!=VERSION:raise ValueError("Explicit QD_025 display contract required")
    reader=doc.select_one(".reader-content");vocab=contract(root)
    for u in data["units"]:
        for target,kind in [(u["question"],"question"),(u.get("answer"),"answer")]:
            if not target:continue
            node=reader.find(id=target)
            if node is None:raise ValueError("Missing label owner "+target)
            wording=u.get("answer_title",u.get("title")) if kind=="answer" else u.get("title")
            title=find_title(node,wording,u.get("title_selector") if kind=="question" else None)
            node["data-zo-type"]="solution" if kind=="answer" else "task"
            node["data-zo-function"]=u["function"];node["data-zo-task"]=u["id"]
            if u.get("number") is not None:node["data-zo-number"]=str(u["number"])
            put_label(doc,title,u["label"])
    for anchor,label in data["checkpoints"].items():
        node=reader.find(id=anchor)
        if node is None:raise ValueError("Missing checkpoint "+anchor)
        headings=node.select("h2,h3,h4,h5,h6")
        if not headings:raise ValueError("Checkpoint lacks heading "+anchor)
        put_label(doc,headings[0],label)
    for u in data["knowledge_units"]:
        node=reader.find(id=u["anchor"])
        if node is None or not node.find_parent(id=u["owner"]):raise ValueError("Wrong knowledge owner "+u["id"])
        title=find_title(node,u["title"]);type_name=vocab["terms"][u["type"]]["name"]
        node["data-zo-type"]=u["type"].removeprefix("type.");node["data-zo-unit"]=u["id"]
        if not omit_type_label(u["title"],type_name):put_label(doc,title,type_name)
    for u in data["examples"]:
        node=reader.find(id=u["anchor"])
        if node is None or not node.find_parent(id=u["owner"]):raise ValueError("Wrong example owner "+u["id"])
        node["data-zo-type"]="example";node["data-zo-unit"]=u["id"]
        # The full example title already carries its type and number.
        title=find_title(node,u["title"])
        if not omit_type_label(title.get_text(" ",strip=True),vocab["terms"]["type.example"]["name"]):put_label(doc,title,"Ví dụ")
    for paper in reader.select(".reading-region"):
        typed=paper.find_parent(attrs={"data-zo-task":True}) or paper.find_parent(attrs={"data-zo-unit":True})
        if typed or paper.select("[data-reading-label]"):continue
        owner=next((n for n in paper.parents if n.get("id") in (area_labels or {})),None)
        title=paper.find(["h2","h3","h4","h5","h6"])
        if owner is None or title is None:continue
        label=area_labels[owner["id"]]
        if label in ["Ôn nền","Lời giải"] or omit_type_label(title.get_text(" ",strip=True),label):continue
        put_label(doc,title,label)
    require(html_checks(doc,data,root),"HTML")
    return data

def html_checks(doc,data,root=ROOT):
    reader=doc.select_one(".reader-content");checks={}
    if reader is None:return {"reader exists for visible labels":False}
    for u in data["units"]:
        for target,kind in [(u["question"],"question"),(u.get("answer"),"answer")]:
            if not target:continue
            node=reader.find(id=target);key=u["id"]+"/"+kind
            checks[key+" metadata/label same owner"]=bool(node and node.get("data-zo-function")==u["function"] and node.get("data-zo-task")==u["id"] and len([n for n in node.select("[data-reading-label]") if n.get_text(" ",strip=True)==u["label"]])==1)
            if data.get("display_contract")==VERSION and node:
                owner=node.find_parent(id=u.get(kind+"_owner")) if u.get(kind+"_owner") else None
                checks[key+" structural owner matches binding"]=owner is not None
                if kind=="question" and u.get("context"):
                    context_key,context_value=next(iter(u["context"].items()))
                    checks[key+" source-owned display context matches"]=bool(owner and owner.get("data-zo-context")==context_key+":"+str(context_value))
                wording=u.get("answer_title",u.get("title")) if kind=="answer" else u.get("title")
                try:title=find_title(node,wording,u.get("title_selector") if kind=="question" else None)
                except ValueError:title=None
                label=title.find_previous_sibling() if title else None
                checks[key+" label adjacent to title with shared style"]=bool(label and label.has_attr("data-reading-label") and "role" in label.get("class",[]) and label.get_text(" ",strip=True)==u["label"])
    for anchor,label in data.get("checkpoints",{}).items():
        node=reader.find(id=anchor);checks[anchor+" checkpoint visible label"]=bool(node and any(n.get_text(" ",strip=True)==label for n in node.select("[data-reading-label]")))
    vocab=contract(root)
    for u in data.get("knowledge_units",[]):
        node=reader.find(id=u["anchor"]);label=vocab["terms"][u["type"]]["name"]
        checks[u["id"]+" type and structural owner"]=bool(node and node.get("data-zo-type")==u["type"].removeprefix("type.") and node.find_parent(id=u["owner"]))
        actual=[n for n in node.select("[data-reading-label]") if n.get_text(" ",strip=True)==label] if node else []
        checks[u["id"]+" visible type obeys no repetition"]=len(actual)==(0 if omit_type_label(u["title"],label) else 1)
    for u in data.get("examples",[]):
        node=reader.find(id=u["anchor"]);checks[u["id"]+" example identity and no duplicate type"]=bool(node and node.get("data-zo-type")=="example" and not any(n.get_text(" ",strip=True).casefold()=="ví dụ" for n in node.select("[data-reading-label]")))
    checks["labels belong to reading papers"]=all(n.find_parent(class_="reading-region") for n in reader.select("[data-reading-label]"))
    checks["no hidden label workaround"]=not reader.select('[data-reading-label][hidden],[data-reading-label][aria-hidden="true"]')
    return checks

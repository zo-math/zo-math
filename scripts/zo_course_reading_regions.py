"""Semantic reading papers for independent R1 tasks; no output I/O."""
from bs4 import Tag

# Local foundation confirmations stay inside their complete resource. Guided
# prompts stay with the knowledge they introduce, rather than becoming a route.
FUNCTIONS = {"function.warmup", "function.self_check", "function.practice",
             "function.test", "function.review", "function.remediation",
             "function.transfer", "function.integration", "function.confirmation"}

def owners(root, binding):
    result = []
    for unit in binding["units"]:
        if unit["function"] not in FUNCTIONS:
            continue
        for key in ("question", "answer"):
            node = root.find(id=unit.get(key)) if unit.get(key) else None
            if key == "answer" and node is not None and node.find_parent(id=unit["question"]) is not None:
                continue
            if node is not None and not node.find_parent(id="on-nen"):
                result.append(node)
    return list({id(n): n for n in result}.values())

def apply(document, binding):
    root = document.select_one(".reader-content")
    units = owners(root, binding)
    def count(node):
        return sum(n is node or any(node is p for p in n.parents) for n in units)
    def substantive(nodes):
        return any(n.name not in ("h2","h3","h4","h5","h6","span")
                   and (n.get_text(strip=True) or n.select("img,table")) for n in nodes)
    def paper(nodes):
        if not nodes:
            return None
        region = document.new_tag("div", attrs={"class":"reading-region",
            "data-reading-reason":"Một nhiệm vụ độc lập hoặc hướng dẫn chung trọn vẹn; giữ dữ kiện, hình, hỗ trợ và hành động cùng chủ sở hữu."})
        nodes[0].insert_before(region)
        for node in nodes:
            region.append(node.extract())
        return region
    def partition(container):
        pending = []
        first = None
        for node in list(container.find_all(recursive=False)):
            hits = count(node)
            if not hits:
                pending.append(node)
                continue
            # Shared guidance forms its own beat; heading-only context joins
            # the following task. Ancestor IDs remain on their original nodes.
            prefix = []
            if pending:
                if substantive(pending):
                    intro = paper(pending)
                    first = first or intro
                else:
                    prefix = pending
                pending = []
            if hits > 1:
                child_first = partition(node)
            else:
                child_first = paper([node])
            if prefix:
                for item in reversed(prefix):
                    child_first.insert(0,item.extract())
            first = first or child_first
        if pending:
            tail = paper(pending)
            first = first or tail
        return first
    for old in list(root.select(".reading-region")):
        if count(old) < 2:
            continue
        old["class"] = [c for c in old.get("class",[]) if c != "reading-region"]
        old.attrs.pop("data-reading-reason",None)
        partition(old)
    require(document, binding)

def require(document, binding):
    root = document.select_one(".reader-content")
    if root.select(".reading-region .reading-region"):
        raise ValueError("Nested reading papers")
    occupied = {}
    for node in owners(root,binding):
        region = node if "reading-region" in node.get("class",[]) else node.find_parent(class_="reading-region")
        # G03/G04 mark a section task on its outer semantic owner, with a
        # paper inside it. It still must have exactly one complete paper.
        if region is None:
            papers = node.select(".reading-region")
            region = papers[0] if len(papers)==1 else None
        if region is None:
            raise ValueError("Independent task lacks one complete paper: "+node["id"])
        prior = occupied.setdefault(id(region),node["id"])
        if prior != node["id"]:
            raise ValueError("Independent tasks share a reading paper: "+prior+" / "+node["id"])


def source_checks(root):
    """Current source entry points; historical receipts are never rewritten."""
    import json
    from pathlib import Path
    root=Path(root)
    template=(root/"_design/web_2027_mau_dung_chung/templates/page.html.tpl").read_text(encoding="utf-8")
    checks={"shared current course breadcrumb":">Khóa 2027</a>" in template and "Nhà khóa 2027" not in template}
    base=root/"content/thpt/on_thi_toan_thpt/hoc_lieu"
    plan=json.loads((base/"r1_g01/giao_dien/web_2027_layout.json").read_text(encoding="utf-8"))
    current=json.dumps(plan["layout"],ensure_ascii=False)
    checks["G01 cover no redundant action"]="hero-action" not in current
    checks["G01 current breadcrumb"]="Nhà khóa 2027" not in current
    for name in ("g02","g03","g04"):
        source=(root/f"scripts/zo_web_2027_{name}.py").read_text(encoding="utf-8")
        checks[name+" cover no redundant action"]='class="hero-action"' not in source
        entry=source if name!="g02" else (root/"scripts/zo_web_2027_g02_production.py").read_text(encoding="utf-8")
        checks[name+" common editorial entry"]="apply_editorial_policy" in entry
    g02=json.loads((base/"r1_g02/giao_dien/web_2027_layout.json").read_text(encoding="utf-8"))
    checks["G02 no legacy grouped warmup"]=not g02["sections"]["ba-câu-khởi-động"].get("unit")
    return checks


def require_cover(document):
    breadcrumb=document.select_one(".breadcrumb > a")
    if breadcrumb is None or breadcrumb.get_text(strip=True)!="Khóa 2027":
        raise ValueError("Course breadcrumb must read Khóa 2027")
    if document.select(".hero .hero-action"):
        raise ValueError("Redundant lesson action in cover")

"""Source-owned G03 content projected through the existing 2027 reading shell."""
from __future__ import annotations
import copy, html, json, os, re
from pathlib import Path
from urllib.parse import urlsplit, unquote, urlunsplit
from bs4 import BeautifulSoup, Tag
from zo_web_2027_home import HomeBuilder
from zo_web_2027_preview import PreviewBuilder, REPO, KIT, BRAND_THOUGHT, template, sha
from zo_web_2027_g02 import canonical_math_matches, inv

PACKAGE = Path("content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g03")
ROLES = {"bat-dau":"Bắt đầu", "bai-hoc":"Bài học", "phieu-luyen":"Luyện tập",
         "tu-kiem-tra":"Kiểm tra", "on-lai":"Ôn lại", "on-nen":"Ôn nền",
         "sua-loi":"Sửa lỗi", "nhat-ky":"Nhật kí", "loi-giai":"Lời giải", "nguon":"Nguồn", "tai-tai-lieu":"Tải tài liệu"}

class Builder(HomeBuilder):
    def __init__(self, output_root):
        super().__init__(output_root / "assets/zo_web_2027/g03/index.html", output_root)
        self.runtime = self.output
    def common_assets(self):
        PreviewBuilder.common_assets(self)

def adapt(path, output_root):
    from zo_course_labels import source_checks, require as require_labels, apply as apply_labels
    require_labels(source_checks(REPO/PACKAGE/"index.qmd"),"source")
    original = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    if original.body is None:
        # Quarto omits draft pages in an ordinary public render.
        return False
    if "zo-web-2027-g03" not in original.body.get("class", []):
        raise ValueError("Missing G03 production opt-in")
    if original.body.has_attr("data-zo-web-production"):
        return False
    from zo_math_notation import math_errors, outline_errors
    source_text=(REPO/PACKAGE/"index.qmd").read_text(encoding="utf-8")
    # G03 has explicit opening guidance and a separately numbered prompt group.
    # Validate its six numbered knowledge units without counting those roles.
    numbered="\n".join(line for line in source_text.splitlines()
        if not re.match(r"^#{3,4} ",line) or re.match(r"^#{3,4} \d+\.",line))
    errors=math_errors(source_text)+outline_errors(numbered)
    if errors:raise ValueError("G03 notation/outline gate: "+json.dumps(errors,ensure_ascii=False))
    if len(re.findall(r"^### \d+\. ",source_text,re.M))!=6:
        raise ValueError("G03 needs six knowledge units")
    root = copy.deepcopy(original.select_one(".zo-on-thi-package"))
    if root is not None:
        notes=original.select_one("section.footnotes")
        if notes is not None:root.find(id="nguon").append(copy.deepcopy(notes))
    if root is None or not canonical_math_matches(REPO/PACKAGE/"index.qmd", root):
        raise ValueError("Fresh G03 render does not preserve canonical mathematics")
    vectors=json.loads((REPO/PACKAGE/"giao_dien/hinh_manifest.json").read_text(encoding="utf-8"))
    for figure in vectors["figures"]:
        for key in ["input","svg","pdf"]:
            if sha(REPO/PACKAGE/figure[key])!=figure[key+"_sha256"]:
                raise ValueError("G03 figure changed; rebuild/review through ZO Math: "+figure["name"])
    baseline = inv(root)
    binding = json.loads((REPO/PACKAGE/"giao_dien/he_nhan.json").read_text(encoding="utf-8"))
    for unit in binding["units"]:
        node = root.find(id=unit["question"])
        if node is None or node.get("data-zo-function") != unit["function"]:
            raise ValueError("Source task binding missing: " + unit["id"])
        if unit.get("answer"):
            answer=root.find(id=unit["answer"])
            if answer is None: raise ValueError("Missing answer: "+unit["id"])
            answer["data-zo-type"]="solution"
            answer["data-zo-function"]=unit["function"]
            answer["data-zo-task"]=unit["id"]
    # Quarto mirrors heading attributes onto its generated section. The section
    # is the sole semantic owner; retain visual headings without duplicate roles.
    for node in root.select("[data-zo-task]"):
        if node.find_parent(attrs={"data-zo-task":node["data-zo-task"]}) is not None:
            for key in list(node.attrs):
                if key.startswith("data-zo-"):del node[key]
            node["class"]=[c for c in node.get("class",[]) if c!="zo-learning-task"]
    root["class"] = list(dict.fromkeys(root.get("class", []) + ["reader-content"]))
    doc=BeautifulSoup("", "html.parser")
    def wrap(owner, nodes, role):
        nodes=[n for n in nodes if isinstance(n,Tag)]
        if not nodes:return
        paper=doc.new_tag("div",attrs={"class":"reading-region","data-reading-reason":"Source-owned complete reading unit"})
        nodes[0].insert_before(paper)
        for n in nodes:paper.append(n.extract())
        return paper
    def regions(section, role):
        if section.has_attr("data-zo-task"):
            wrap(section,list(section.children),role);return
        pending=[]
        for child in list(section.children):
            if isinstance(child,Tag) and child.name=="section":
                if pending:wrap(section,pending,role);pending=[]
                regions(child,role)
            else:pending.append(child)
        if pending:wrap(section,pending,role)
        # Section-only headings belong with the next complete reading unit.
        for paper in list(section.select(":scope > .reading-region")):
            substantive=paper.select("p,li,table,figure,details")
            if substantive and any(n.get_text(" ",strip=True) or n.find("img") for n in substantive):continue
            next_paper=paper.find_next(class_="reading-region")
            if next_paper is not None and section in next_paper.parents:
                for node in reversed(list(paper.contents)):next_paper.insert(0,node.extract())
                paper.decompose()
    for ident,role in ROLES.items():
        section=root.find("section",id=ident,recursive=False)
        if section is None:raise ValueError("Missing source section: "+ident)
        regions(section,role)
    if inv(root)!=baseline:raise ValueError("G03 reading projection changed content, mathematics or IDs")
    if root.select(".reading-region .reading-region"):raise ValueError("Nested reading regions")
    builder=Builder(output_root);builder.output.mkdir(parents=True,exist_ok=True)
    builder.common_assets()
    builder.materialize(REPO/PACKAGE/"giao_dien/assets/figures_0_4/bia_tiem_can.svg", "assets/g03-cover.svg")
    for name in ["r1-g02-adapter.css","site-footer.css","r1-consistency.css"]:builder.materialize(KIT/name,name)
    for img in root.select("img[src]"):
        target=(path.parent/unquote(urlsplit(img["src"]).path)).resolve()
        relative=target.relative_to(output_root)
        source=REPO/relative
        if not source.is_file():raise ValueError("Missing official figure: "+str(source))
        img["src"]=builder.materialize(source,"assets/content/"+source.name)
        img["class"]=img.get("class",[])+["math-illustration"]
        import xml.etree.ElementTree as ET
        width=float(ET.parse(source).getroot().attrib["viewBox"].split()[2])
        img["style"]=f"--figure-em:{width/16.5:.5f}em"
        viewport=doc.new_tag("div",attrs={"class":"figure-viewport","tabindex":"0","role":"region","aria-label":img.get("alt","Hình đồ thị")+"; cuộn ngang khi cần"});img.wrap(viewport)
    for link in root.select("a[href]"):
        value=link["href"];split=urlsplit(value)
        if split.scheme or split.netloc or not split.path:continue
        if split.path.endswith('.qmd'):
            split=split._replace(path=split.path[:-4]+'.html')
        target=(path.parent/unquote(split.path)).resolve()
        if not target.is_relative_to(output_root):raise ValueError("Link escapes output root")
        link["href"]=builder.href(target,split.query,split.fragment)
    for details in root.select("details"):
        details.attrs.pop("open",None)
        guidance=any(c in details.get("class",[]) for c in ["zo-learning-guidance","r1-foundation-unit"])
        details["class"]=list(dict.fromkeys(details.get("class",[])+
            (["r1-details","zo-block","zo-block-gray"] if guidance else
             ["r1-details","r1-solution","zo-learning-solution","solution","zo-block","zo-block-gray"])))
        summary=details.find("summary",recursive=False)
        if summary is None:raise ValueError("Disclosure needs a summary")
        summary["class"]=list(dict.fromkeys(summary.get("class",[])+["zo-block-title"]))
        body=doc.new_tag("div",attrs={"class":"zo-block-body"})
        for child in list(details.contents):
            if child is not summary:body.append(child.extract())
        details.append(body)
    title=root["data-r1-title"];subtitle=original.select_one(".subtitle").get_text(" ",strip=True)
    home=builder.href(output_root/"content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.html")
    hero=f'<section class="hero" aria-label="Bìa học liệu"><div class="hero-copy"><span class="eyebrow">Ôn thi Toán THPT 2027 · Hàm số</span><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p><a class="hero-action" href="?r1-view=bai-hoc#bai-hoc">Vào Bài học <span aria-hidden="true">↗</span></a></div><figure class="hero-art"><img src="assets/g03-cover.svg" alt="Hai nhánh đồ thị tiến gần đường tiệm cận đứng và đường tiệm cận ngang; không phải dữ kiện bài tập"><figcaption>Minh họa nhận diện · Không phải dữ kiện của nhiệm vụ</figcaption></figure></section>'
    footer,_=builder.site_footer()
    support=template("support.html",support_href=builder.href(output_root/"content/support/donate.html"),
        prototype_note="Bản HTML chờ duyệt; chưa phát hành.")
    rendered=template("page.html", title=html.escape(title),body_class="g02-preview",home_href=home,
        appearance=builder.appearance(),brand_thought=html.escape(BRAND_THOUGHT),navigation='<div id="nav-mount"></div>',
        breadcrumb=html.escape(title),hero=hero,content=str(root),support=support,site_footer=footer,drawer_title="Các phần của học liệu",
        styles="\n".join(f'<link rel="stylesheet" href="{n}">' for n in ["reading-regions.css","web-shell.css","site-footer.css","appearance-inline.css","r1-g02-adapter.css","r1-consistency.css"]),
        scripts='<script src="r1-controller.js"></script><script src="site-ui.js"></script>')
    result=BeautifulSoup(rendered,"html.parser")
    apply_labels(result,binding,{})
    page_labels=json.loads((KIT/"profiles/r1-consistency.json").read_text(encoding="utf-8"))["page_roles"]
    from zo_course_labels import put_label
    for ident,title in ROLES.items():
        section=result.find(id=ident)
        heading=section.find("h2")
        if heading is not None and title in page_labels and ident!="tu-kiem-tra":
            put_label(result,heading,page_labels[title])
    # Match the accepted G01 source-area label (its policy uses the old title).
    put_label(result,result.find(id="nguon").find("h2"),page_labels["Nguồn đối chiếu"])
    put_label(result,result.find(id="khởi-động").find("h3"),"Bài học · Khởi động")
    fallback=result.new_tag("noscript");nav=result.new_tag("nav",attrs={"aria-label":"Các phần của học liệu"})
    for anchor,label in ROLES.items():
        para=result.new_tag("p");a=result.new_tag("a",href="#"+anchor);a.string=label;para.append(a);nav.append(para)
    fallback.append(nav);result.find(id="rail-content").append(fallback)
    for node in result.select("[src],link[href],a[href]"):
        key="src" if node.has_attr("src") else "href";url=urlsplit(node[key])
        if url.scheme or url.netloc or not url.path:continue
        destination=(builder.output/unquote(url.path)).resolve()
        if not destination.is_relative_to(output_root):raise ValueError("Dependency escapes output root")
        node[key]=urlunsplit(("","",os.path.relpath(destination,path.parent).replace("\\","/"),url.query,url.fragment))
    from zo_course_tables import apply as apply_tables
    apply_tables(result,"r1_g03",path,builder.output)
    from zo_web_2027_downloads import apply_from_metadata
    apply_from_metadata(result,path,output_root,PACKAGE)
    from zo_web_2027_navigation import apply as apply_course_navigation
    apply_course_navigation(result,path,output_root,builder.output,"g03")
    result.body["data-zo-web-production"]="R1-G03"
    result.title.string=title+" — ZO Math"
    from zo_web_2027_consistency import apply_editorial_policy
    apply_editorial_policy(result)
    from zo_course_html import write
    write(path,result)
    print("G03 shell:",len(root.select(".reading-region")),"reading regions")
    return True

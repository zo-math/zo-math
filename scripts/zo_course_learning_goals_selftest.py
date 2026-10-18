"""Source-only learning-goal regressions. Never render or write HTML/PDF."""
from pathlib import Path
from bs4 import BeautifulSoup
import argparse,copy,json,sys
from zo_course_learning_goals import source_checks,html_checks,inverse_g01_fingerprint,TITLE,spec
from zo_web_2027_production import content_fingerprint
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"content/thpt/on_thi_toan_thpt/hoc_lieu"

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--report",type=Path);args=ap.parse_args();checks={}
    for name in ["r1_g01","r1_g02","r1_g03","r1_g04"]:
        p=BASE/name/"index.qmd";text=p.read_text(encoding="utf-8");b=json.loads((p.parent/"giao_dien/he_nhan.json").read_text(encoding="utf-8"))["learning_goals"]
        values=source_checks(p);checks.update({name+"/"+k:v for k,v in values.items()})
        broken=text.replace("| Mục tiêu | Việc em cần làm được |","| Phần học | Việc em tập làm |",1)
        checks[name+" reject chapter-map columns"]=not all(source_checks(p,text=broken).values())
        first=b["rows"][0]["title"];broken=text.replace("| "+first+" |","| Mất mục tiêu |",1)
        checks[name+" reject missing declared goal"]=not all(source_checks(p,text=broken).values())
        broken=text.replace("Câu hỏi dẫn đường","Định hướng bài học",1)
        checks[name+" reject obsolete guide label"]=not all(source_checks(p,text=broken).values())
        rows=''.join('<tr><th>'+row["title"]+'</th><td>Biểu hiện cụ thể</td></tr>' for row in b["rows"])
        doc=BeautifulSoup('<main class="reader-content"><section id="bat-dau"><p id="'+b["heading"]+'">'+TITLE+'</p><div id="'+b["table"]+'"><table><thead><tr><th>Mục tiêu</th><th>Việc em cần làm được</th></tr></thead><tbody>'+rows+'</tbody></table></div></section><section id="bai-hoc"><details id="'+b["guide"]+'"><summary>Câu hỏi dẫn đường</summary><p>Câu hỏi?</p></details></section></main>','html.parser')
        checks[name+" valid component owners"]=all(html_checks(doc,b).values())
        bad=copy.deepcopy(doc);bad.find(id=b["guide"]).append(bad.find(id=b["table"]).extract())
        checks[name+" reject hidden goals in lesson guide"]=not all(html_checks(bad,b).values())
        bad=copy.deepcopy(doc);bad.find(id=b["guide"])["open"]=""
        checks[name+" reject open guide"]=not all(html_checks(bad,b).values())
    from unittest.mock import patch
    with patch.object(Path,"read_text",return_value=json.dumps({"learning_goals":{"declared":True}})):
        checks["new declared package uses shared rule without whitelist"]=spec(Path("fixture/hoc_lieu/r2_g07/index.qmd"))=={"declared":True}
    checks["D0 is not forced into learning package rule"]=spec(Path("fixture/hoc_lieu/d0/index.qmd")) is None
    p=BASE/'r1_g01/index.qmd';plan=json.loads((p.parent/'giao_dien/web_2027_layout.json').read_text(encoding='utf-8'));c=plan['source_transition'];guide_id='dinh-huong-bai-hoc'
    before=BeautifulSoup('<div class="reader-content"><section id="bat-dau"><p>'+c['old_intro_text']+'</p></section><section id="bai-hoc"><details id="'+guide_id+'"><summary>Định hướng bài học</summary><span id="câu-hỏi-dẫn-đường">Câu hỏi dẫn đường</span><p>Giữ nguyên câu hỏi.</p><span id="học-xong-em-cần-làm-được-gì">'+TITLE+'</span><div id="r1-table-t02">'+c['old_goal_text'][len(TITLE):].strip()+'</div><p>'+c['scope_text']+'</p></details><p id="outside">Nội dung khác <math><semantics><mi>x</mi><annotation encoding="application/x-tex">x</annotation></semantics></math></p></section></div>','html.parser').div
    expected=content_fingerprint(before);after=copy.deepcopy(before)
    start=after.find(id='bat-dau');start.clear()
    # Deliberately different DOM structure, exact approved source text/IDs.
    heading=after.find(id='học-xong-em-cần-làm-được-gì').extract();table=after.find(id='r1-table-t02').extract();start.append(heading)
    lead=BeautifulSoup('<p></p>','html.parser').p;lead.string=c['new_intro_text'][len(TITLE):].removesuffix(table.get_text()).strip();start.append(lead);start.append(table)
    g=after.find(id=guide_id);question=after.find(id='câu-hỏi-dẫn-đường').extract();g.summary.clear();g.summary.append(question)
    scoped=copy.deepcopy(plan);scoped['source_fingerprint']=expected
    checks['G01 bounded inverse retains full old fingerprint']=inverse_g01_fingerprint(after,scoped,content_fingerprint,p)==expected
    before_serialized=str(after);inverse_g01_fingerprint(after,scoped,content_fingerprint,p)
    checks['inverse never edits output DOM']=str(after)==before_serialized
    bad=copy.deepcopy(after);bad.find(id='outside').append(' Thêm câu ngoài phạm vi.')
    checks['unrelated prose remains protected']=inverse_g01_fingerprint(bad,scoped,content_fingerprint,p)!=expected
    bad=copy.deepcopy(after);bad.find('annotation').string='y'
    checks['mathematics remains protected']=inverse_g01_fingerprint(bad,scoped,content_fingerprint,p)!=expected
    bad=copy.deepcopy(after);bad.find(id='outside')['id']='changed-outside'
    checks['unrelated IDs remain protected']=inverse_g01_fingerprint(bad,scoped,content_fingerprint,p)!=expected
    bad=copy.deepcopy(after);bad.find(id='r1-table-t02').string='Thiếu mục tiêu'
    try:inverse_g01_fingerprint(bad,scoped,content_fingerprint,p);checks['missing goal payload rejected']=False
    except ValueError:checks['missing goal payload rejected']=True
    report={'checks':checks,'passed':sum(checks.values()),'total':len(checks),'failures':[k for k,v in checks.items() if not v],'rendered':False}
    if args.report:
        path=args.report.resolve()
        if not path.is_relative_to(ROOT/'_audit') or path.suffix!='.json':raise ValueError('Named audit JSON required')
        path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['passed','total','failures']},ensure_ascii=False));return int(bool(report['failures']))
if __name__=='__main__':raise SystemExit(main())

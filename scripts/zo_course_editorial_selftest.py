"""Terminology, source-review and bounded-comparison regressions; no render."""
from pathlib import Path
import argparse,copy,json,tempfile
from bs4 import BeautifulSoup
from zo_course_editorial import ROOT,COURSE,POLICY,RULE,scan,sha,source_checks,html_checks,restore_g01_for_comparison
from zo_web_2027_production import content_fingerprint

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path);args=ap.parse_args();checks={}
    paths=[ROOT/COURSE/'tot_nghiep_thpt/2027/index.qmd']+[ROOT/COURSE/'hoc_lieu'/p/'index.qmd' for p in ['d0','r1_g01','r1_g02','r1_g03','r1_g04']]
    for p in paths:
        checks.update({p.parent.name+'/'+k:v for k,v in source_checks(p).items()})
        text=p.read_text(encoding='utf-8')+'\nMột câu mới viết đúng thuật ngữ nhưng chưa được rà.\n'
        checks[p.parent.name+' requires review after any prose edit']=not all(source_checks(p,text=text).values())
    for phrase in ['miền xác định','miền tự nhiên','trên toàn miền','miền giá trị được phép chọn','phép đo mới','lấy mẫu mục tiêu','bài thứ ba','chứng nhận độ bền','công thức kiểm điểm','nghiệm đạo hàm','nhân ngược','hàm tự nhiên','câu còn mới','câu đã lộ','tập đang xét xét']:
        checks['reject '+phrase]=bool(scan(phrase))
        checks['reject HTML '+phrase]=not all(html_checks(BeautifulSoup('<main class="reader-content"><p>'+phrase+'</p></main>','html.parser')).values())
    for phrase in ['Tập xác định của hàm số','Tập đang xét là một đoạn.','Điều kiện về sản lượng','Miền nghiệm của hệ bất phương trình','Diện tích miền phẳng','Lấy mẫu nhân với thương rồi cộng phần dư để kiểm phép chia.']:
        checks['allow '+phrase]=not scan(phrase)
    technical='[]{#chọn-giới-hạn-theo-miền}\n[Xem lời giải](#miền-xác-định)\n```text\nmiền xác định\n```'
    checks['stable IDs URLs and code are not learner terminology']=not scan(technical)
    with tempfile.TemporaryDirectory(prefix='zo-editorial-') as folder:
        root=Path(folder);page=root/COURSE/'hoc_lieu/d0/index.qmd';inc=page.parent/'shared.qmd'
        page.parent.mkdir(parents=True);page.write_text('{{< include shared.qmd >}}\n',encoding='utf-8');inc.write_text('Tìm tập xác định.\n',encoding='utf-8')
        dest=root/POLICY;dest.parent.mkdir(parents=True);dest.write_bytes((ROOT/POLICY).read_bytes())
        policy=json.loads(dest.read_text(encoding='utf-8'));ledger=root/policy['review'];ledger.parent.mkdir(parents=True)
        record={'decision':RULE,'status':'source_reviewed_not_rendered','owner_HTML_acceptance':False,'sources':{p.relative_to(root).as_posix():sha(p.read_bytes()) for p in [page,inc]}}
        ledger.write_text(json.dumps(record),encoding='utf-8')
        checks['valid included source review']=all(source_checks(page,root).values())
        inc.write_text('Tìm miền xác định.\n',encoding='utf-8')
        checks['include cannot bypass lexical or review gate']=not all(source_checks(page,root).values())
        inc.write_text('Tìm tập xác định rồi giải thích điều kiện.\n',encoding='utf-8')
        checks['coherent include edit still requires review']=not all(source_checks(page,root).values())
        inc.write_text('Tìm tập xác định.\n',encoding='utf-8')
        record['owner_HTML_acceptance']=True;ledger.write_text(json.dumps(record),encoding='utf-8')
        checks['review does not claim owner HTML acceptance']=not all(source_checks(page,root).values())
    with tempfile.TemporaryDirectory(prefix='zo-editorial-home-') as folder:
        root=Path(folder);page=root/COURSE/'tot_nghiep_thpt/2027/index.qmd';datafile=page.parent/'_data/chuong_trinh.yml'
        datafile.parent.mkdir(parents=True);page.write_text('Giới thiệu khóa học.\n',encoding='utf-8');datafile.write_text('summary: Tìm tập xác định\n',encoding='utf-8')
        dest=root/POLICY;dest.parent.mkdir(parents=True);dest.write_bytes((ROOT/POLICY).read_bytes())
        pol=json.loads(dest.read_text(encoding='utf-8'));ledger=root/pol['review'];ledger.parent.mkdir(parents=True)
        record={'decision':RULE,'status':'source_reviewed_not_rendered','owner_HTML_acceptance':False,'sources':{page.relative_to(root).as_posix():sha(page.read_bytes())},'dependent_sources':{datafile.relative_to(root).as_posix():sha(datafile.read_bytes())}}
        ledger.write_text(json.dumps(record),encoding='utf-8')
        checks['valid Home catalog data binding']=all(source_checks(page,root).values())
        datafile.write_text('summary: Tìm tập xác định và xét điều kiện\n',encoding='utf-8')
        checks['changed catalog data requires editorial review']=not all(source_checks(page,root).values())
        datafile.write_text('summary: Giữ miền\n',encoding='utf-8')
        checks['catalog metadata cannot bypass terminology gate']=not all(source_checks(page,root).values())
    # Generic inverse fixture exercises text/math/ID/disclosure protection outside
    # the explicitly listed changed block, without parsing or writing HTML files.
    qmd=paths[2];plan=json.loads((qmd.parent/'giao_dien/web_2027_layout.json').read_text(encoding='utf-8'))
    plan=copy.deepcopy(plan);change=plan['editorial_transition'];change['edits']=[{'tag':'p','source':'fixture','line_before':1,'before_html':'<p id="edited">Câu trước.</p>','after_signature':[['text',sha('Câu sau đã duyệt.')]]}]
    after=BeautifulSoup('<main><p id="edited">Câu sau đã duyệt.</p><p id="outside">Phần giữ nguyên <math><annotation encoding="application/x-tex">x</annotation></math></p><details id="help"></details></main>','html.parser').main
    expected=copy.deepcopy(after);expected.find(id='edited').string='Câu trước.'
    checks['bounded inverse complete fingerprint']=content_fingerprint(restore_g01_for_comparison(after,plan,qmd))==content_fingerprint(expected)
    original=str(after);restore_g01_for_comparison(after,plan,qmd);checks['inverse never mutates learner DOM']=str(after)==original
    for name,mutate in [('text',lambda d:d.find(id='outside').append(' Thay ngoài phạm vi.')),('math',lambda d:setattr(d.find('annotation'),'string','y')),('ID',lambda d:d.find(id='outside').__setitem__('id','other')),('disclosure',lambda d:d.find('details').__setitem__('open',''))]:
        bad=copy.deepcopy(after);mutate(bad)
        checks['unapproved '+name+' remains detectable']=content_fingerprint(restore_g01_for_comparison(bad,plan,qmd))!=content_fingerprint(expected)
    for name,mutate in [('changed new prose',lambda d:d.find(id='edited').append(' Khác.')),('duplicate block',lambda d:d.append(copy.deepcopy(d.find(id='edited'))))]:
        bad=copy.deepcopy(after);mutate(bad)
        try:restore_g01_for_comparison(bad,plan,qmd);checks['reject '+name]=False
        except ValueError:checks['reject '+name]=True
    stale=copy.deepcopy(plan);stale['editorial_transition']['source_qmd_sha256']='0'*64
    try:restore_g01_for_comparison(after,stale,qmd);checks['reject stale G01 source binding']=False
    except ValueError:checks['reject stale G01 source binding']=True
    duplicate=copy.deepcopy(plan);duplicate['editorial_transition']['sources']={qmd.relative_to(ROOT).as_posix():'0'*64}
    checks['historical self hash uses strict current full source binding']=content_fingerprint(restore_g01_for_comparison(after,duplicate,qmd))==content_fingerprint(expected)
    stale=copy.deepcopy(duplicate);stale['editorial_transition']['source_qmd_sha256']='0'*64
    try:restore_g01_for_comparison(after,stale,qmd);checks['stale current binding cannot hide behind old self hash']=False
    except ValueError:checks['stale current binding cannot hide behind old self hash']=True
    include=copy.deepcopy(plan);include['editorial_transition']['sources']={Path(__file__).relative_to(ROOT).as_posix():'0'*64}
    try:restore_g01_for_comparison(after,include,qmd);checks['independent include hash remains strict']=False
    except ValueError:checks['independent include hash remains strict']=True
    checks['historical accepted receipt unchanged']=plan['accepted_sha256']=='5c97396dd9656971e442cb60a07aa799935d3233bf2ae15a53ebc57f76c77e3c'
    report={'passed':sum(checks.values()),'total':len(checks),'failures':[k for k,v in checks.items() if not v],'checks':checks,'rendered':False}
    if args.report:
        p=args.report.resolve()
        if not p.is_relative_to(ROOT/'_audit') or p.suffix!='.json':raise ValueError('Audit JSON only')
        p.parent.mkdir(exist_ok=True,parents=True);p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['passed','total','failures']},ensure_ascii=False));return int(bool(report['failures']))
if __name__=='__main__':raise SystemExit(main())

"""Current G01 editorial projection/semantic gate, separate from acceptance."""
import argparse
from collections import Counter
import copy
import json
from pathlib import Path
import re
from urllib.parse import unquote
from bs4 import BeautifulSoup
from zo_course_labels import context_unit_label
from zo_web_2027_production import ROOT, PACKAGE, PLAN, sha, norm, content_fingerprint
from zo_learning_architecture import load_yaml
from zo_2027_governance_check import governance_context
from zo_r1_g01_editorial_check import semantic, maths, task_maths, editorial_browser
from zo_web_2027_g01_checkpoint import browser_checks
from zo_web_2027_check import Browser, edge_executable
import socket, subprocess, tempfile, time
import requests


def situations(doc):
    root=doc.select_one('.reader-content')
    text=lambda i:root.find(id=i).get_text(' ',strip=True)
    guide=text('cách-học-với-tài-liệu-này');help_text=text('g01-ho-tro-khi-can')
    link=lambda i,t:bool(root.find(id=i).select_one('a[href="#'+t+'"]'))
    rules={
        'DH01':('đúng lời giải thích hoặc ví dụ trong Bài học' in help_text,['g01-ho-tro-khi-can','bai-hoc']),
        'DH02':(link('bắt-đầu-từ-đâu','nen-n-dh-01') and 'Khởi động chưa đủ' in guide,['bắt-đầu-từ-đâu','nen-n-dh-01','nen-n-dh-01-xn01']),
        'DH03':(link('g01-khoi-dong-01','lg-g01-khoi-dong-01') and link('lg-g01-khoi-dong-01','g01-khoi-dong-01'),['g01-khoi-dong-01','lg-g01-khoi-dong-01']),
        'DH04':('xem lại đúng lời giải thích hoặc ví dụ trong Bài học' in help_text and 'Nếu đã nắm phần học' in guide,['phieu-luyen','g01-ho-tro-khi-can','bai-hoc']),
        'DH05':(link('cp-lt1','nen-n-dau-01'),['cp-lt1','nen-n-dau-01','nen-n-dau-01-xn01']),
        'DH06':(link('cp-lt1','sua-loi-sau-luyen-tap') and 'Nếu đã đáp ứng tiêu chí, không cần qua mọi nhánh hỗ trợ' in help_text,['cp-lt1','sua-loi-sau-luyen-tap']),
        'DH07':(all(t in guide for t in ['Trong lúc Kiểm tra, phải tự lực hoàn toàn','không dùng Bài học, Ôn nền, Lời giải hoặc Sửa lỗi','kết thúc lượt kiểm tra']) and all(t in text('tu-kiem-tra') for t in ['tự tin','Không được chia Kiểm tra thành nhiều đợt','không tự chứng nhận đã đạt']),['cách-học-với-tài-liệu-này','tu-kiem-tra']),
        'DH08':(all(link('cp-kt',t) for t in ['đọc-kết-quả-tự-kiểm-tra','sua-loi-sau-kiem-tra','on-nen']) and 'Giữ điểm ban đầu riêng với kết quả sau sửa' in text('cp-kt'),['cp-kt','đọc-kết-quả-tự-kiểm-tra','sua-loi-sau-kiem-tra','on-nen']),
        'DH09':('Bài học, Luyện tập, Ôn lại và sau khi kết thúc Kiểm tra' in guide and 'đúng tuyến Nền' in text('cp-on2'),['cách-học-với-tài-liệu-này','cp-on2','bai-hoc','on-nen']),
        'DH10':(link('g01-o02','lg-g01-o02') and link('g01-o02','g01-s-o-e05') and link('lg-g01-o02','g01-o02'),['g01-o02','lg-g01-o02','g01-s-o-e05','cp-on2']),
        'DH11':(len(root.select('#r1-table-t13 tbody tr'))==14 and 'không cần ghi sau mọi thao tác' in help_text,['g01-ho-tro-khi-can','nhat-ky','r1-table-t13']),
        'DH12':('Em có thể đi tới hoặc quay lại' in guide and 'phần bỏ qua không tự được xem là đã đạt' in guide,['cách-học-với-tài-liệu-này']),
        'DH13':('Nếu vào thẳng phần hỗ trợ, chọn nhiệm vụ hoặc hoạt động em muốn quay về' in help_text,['g01-ho-tro-khi-can','on-nen','sua-loi']),
        'DH14':(all(t in help_text.casefold() for t in ['đã xem đáp án','không còn nhiệm vụ mới phù hợp','không tính là bằng chứng độc lập mới','không tự đánh dấu đã đạt']) and 'Chưa có bài mới' in text('cp-lt1'),['g01-ho-tro-khi-can','cp-lt1','cp-kt'])}
    return {k:{'passed':bool(ok) and all(root.find(id=i) for i in ids),'source_targets':ids} for k,(ok,ids) in rules.items()}


def targeted_browser(page,g02,images):
    checks={}
    with socket.socket() as probe:probe.bind(('127.0.0.1',0));port=probe.getsockname()[1]
    with tempfile.TemporaryDirectory(prefix='g01_labels_browser_',dir=images.parent) as profile:
        proc=subprocess.Popen([edge_executable(),'--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check',f'--remote-debugging-port={port}','--remote-debugging-address=127.0.0.1','--remote-allow-origins=http://localhost','--user-data-dir='+profile,'about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        b=None
        try:
            endpoint=f'http://127.0.0.1:{port}'
            for _ in range(100):
                try:
                    if requests.get(endpoint+'/json/version',timeout=.3).ok:break
                except requests.RequestException:pass
                time.sleep(.1)
            tab=requests.put(endpoint+'/json/new?about:blank',timeout=10).json();b=Browser(tab['webSocketDebuggerUrl']);b.call('Page.enable');b.call('Runtime.enable')
            for width in [1440,390]:
                b.viewport(width,960 if width>500 else 844);url=page.as_uri()
                for ident in ['cách-học-với-tài-liệu-này','g01-ho-tro-khi-can','g01-chuyen-goi','g01-khoi-dong-01','lg-g01-khoi-dong-01','nen-n-lt-01-xn02']:
                    b.navigate(url+'#'+ident)
                    b.screenshot(images/f'labels-{ident}-{width}.png')
                    checks[f'{width}/{ident} visible correct target']=b.evaluate('!!document.getElementById('+json.dumps(ident)+').getClientRects().length')
                for caller in ['bắt-đầu-từ-đâu','cp-lt1','cp-kt']:
                    b.navigate(url+'#'+caller)
                    dest='nen-n-dh-01' if caller!='cp-kt' else 'on-nen'
                    b.click('#'+caller+' a[href="#'+dest+'"]')
                    checks[f'{width}/{caller} foundation records caller']=b.evaluate('new URL(location.href).searchParams.get("r1-return")')==caller
                    b.call('Page.reload');b.ready();b.click('.r1-return-link')
                    checks[f'{width}/{caller} foundation returns caller']=unquote(b.evaluate('location.hash'))=='#'+caller
                b.navigate(url+'#g01-o02');b.click('#g01-o02 a[href="#g01-s-o-e05"]')
                checks[f'{width} review repair records actual task']=b.evaluate('new URL(location.href).searchParams.get("r1-return")')=='g01-o02'
                b.click('#g01-s-o-e05 .answer-link a');b.click('#lg-g01-s-o-e05 .answer-link a');b.call('Page.reload');b.ready();b.click('.r1-return-link')
                checks[f'{width} review repair/answer/reload returns actual task']=b.evaluate('location.hash')=='#g01-o02'
                b.navigate(url+'#nen-n-dh-01')
                checks[f'{width} direct foundation has manual return options']=b.evaluate('document.querySelectorAll(".r1-return-link").length')>=3
                if g02:
                    b.navigate(g02.as_uri()+'#nen-n-lt-01')
                    checks[f'{width} G02 legacy foundation owner compatible']=b.evaluate('document.querySelector("#r1-view-panel").dataset.r1View')=='on-nen'
        finally:
            if b:b.ws.close()
            proc.terminate()
            try:proc.wait(timeout=10)
            except subprocess.TimeoutExpired:proc.kill();proc.wait()
    return checks


def predicates(doc, bindings):
    root=doc.select_one('.reader-content');checks={}
    checks['independent foundation source owner']=root.find(id='on-nen').find_parent('section') is None
    checks['after-review remediation belongs to repair']=bool(root.find(id='sua-loi-sau-on-lai').find_parent(id='sua-loi')) and not root.find(id='on-lai').find(id='g01-s-o-e01')
    checks['three guide beats']=all(root.find(id=i) and 'reading-region' in root.find(id=i).get('class',[]) for i in bindings['guide_beats'])
    checks['main map has exactly four links']=len(root.find(id='cách-học-với-tài-liệu-này').select_one('[data-learning-main]').select('a'))==4
    checks['no nested papers']=not root.select('.reading-region .reading-region')
    checks['all authored disclosures closed']=not root.select('details[open]')
    checks['all headings/roles belong to paper']=all(n.find_parent(class_='reading-region') for n in root.select('h2,h3,h4,h5,h6,.role'))
    checks['69 unique task bindings']=len(bindings['units'])==69 and len({u['question'] for u in bindings['units']})==69
    for unit in bindings['units']:
        for key in ['question','answer']:
            ident=unit.get(key)
            if not ident:continue
            node=root.find(id=ident)
            # The solved repair example keeps one title in its disclosure
            # summary. Its legacy answer anchor remains inside that disclosure.
            context=node
            if key=='answer' and ident=='lg-cg01' and node:
                context=node.find_parent('details')
            checks[unit['id']+'/'+key+' identity/label/title']=bool(node and context and node.get('data-zo-task')==unit['id'] and node.get('data-zo-function')==unit['function'] and unit['title'] in context.get_text(' ',strip=True) and context_unit_label(unit,key,bindings) in context.get_text(' ',strip=True))
            if key=='answer':
                from zo_r1_g01_labels import local_answer_pair
                q=root.find(id=unit['question']);local=local_answer_pair(q,node)
                links=node.select('.answer-link a[href="#'+unit['question']+'"]') if node else []
                checks[unit['id']+' answer navigation matches ownership']=not links if local else bool(links)
    checks['Gợi mở never has duplicated answers']=all(not u['answer'] for u in bindings['units'] if u['function']=='function.guided_thinking')
    checks['practice continuous across stages']=[u['number'] for u in bindings['units'] if u['function']=='function.practice']==list(range(1,9))
    checks['remediation continuous across contexts']=sorted(u['number'] for u in bindings['units'] if u['function']=='function.remediation')==list(range(1,27))
    for ident in ['on-nen','nhat-ky','nguon','loi-giai','cách-học-với-tài-liệu-này']:
        owner=root.find(id=ident);paper=owner if 'reading-region' in owner.get('class',[]) else owner.select_one(':scope > .reading-region')
        heading=paper.find(['h2','h3']) if paper else None
        checks[ident+' no repeated label/title']=bool(heading) and not any(n.get_text(' ',strip=True).casefold()==heading.get_text(' ',strip=True).casefold() for n in paper.select(':scope > [data-reading-label]'))
    return checks


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--audit',type=Path,required=True);ap.add_argument('--browser',action='store_true');ap.add_argument('--report',default='qa.json');ap.add_argument('--owner-draft',type=Path,help='Explicit historical draft for the migration preservation check');args=ap.parse_args()
    out=args.audit.resolve()
    if not out.is_relative_to(ROOT/'_audit'):raise ValueError('Audit only')
    page=out/'r1_g01-render/docs'/PACKAGE/'index.html'
    parse=lambda p:BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
    doc=parse(page);raw=parse(out/'after/r1_g01-raw/docs'/PACKAGE/'index.html');old=parse(out/'before/r1_g01-raw/docs'/PACKAGE/'index.html')
    bindings=json.loads((ROOT/PACKAGE/'giao_dien/he_nhan.json').read_text(encoding='utf-8'))
    manifest=load_yaml(ROOT/PACKAGE/'_quy_trinh/kien_truc_hoc_tap.yml')
    source=raw.select_one('.zo-on-thi-package');before=old.select_one('.zo-on-thi-package');root=doc.select_one('.reader-content')
    governance, _, _ = governance_context()
    checks=semantic(doc,manifest);checks.update(predicates(doc,bindings))
    checks['current governance documents passed']=governance['documents_passed']
    situation_review=situations(doc)
    checks.update({k+' source targets/wording':v['passed'] for k,v in situation_review.items()})
    checks['fresh QMD math exactly projected in source order']=maths(source)==maths(root)
    checks['all prior math occurrences unchanged']=Counter(maths(source))==Counter(maths(before))
    checks['all old IDs retained']=not (set(n['id'] for n in before.select('[id]'))-set(n['id'] for n in doc.select('[id]')))
    checks['all fresh IDs retained']=not (set(n['id'] for n in source.select('[id]'))-set(n['id'] for n in doc.select('[id]')))
    ids=[n['id'] for n in doc.select('[id]')];checks['all IDs unique']=len(ids)==len(set(ids))
    checks['strict canonical fingerprint current']=json.loads(PLAN.read_text(encoding='utf-8'))['source_fingerprint']==content_fingerprint(source)
    checks['42 manifest payloads retain all mathematics']=all(Counter(task_maths(before.find(id=u['source_anchor'])))<=Counter(task_maths(source.find(id=u['source_anchor']))) for u in manifest['tasks'])
    for task in manifest['tasks']:
        anchor=task['source_anchor']
        # Secondary points and every narrative paragraph/list item must be
        # projected, not merely formulas. Headings are checked against labels.
        paragraphs=[p.get_text(' ',strip=True) for p in source.find(id=anchor).select('p,li')]
        rendered=root.find(id=anchor).get_text(' ',strip=True)
        checks[task['id']+' full canonical task prose projected']=all(p in rendered for p in paragraphs)
    checks['G02 private QMD unchanged']=(out/'r1_g02-before.qmd').read_bytes()==(ROOT/PACKAGE.parent/'r1_g02/index.qmd').read_bytes()
    if args.owner_draft:
        checks['owner edited draft unchanged']=sha(args.owner_draft.read_bytes())=='51fe4f877b2c5e5c19d1ccf1736ff8599244ed43c8cbf257971a0c90482a5c0e'
    checks['historical acceptance unchanged']=(out/'g01-accepted-before.json').read_bytes()==(ROOT/PACKAGE/'giao_dien/web_2027_accepted.json').read_bytes()
    def orphan_heading(d):
        d.select_one('.reader-content').append(d.select_one('.reader-content h3').extract())
    for name,mutate in [('number reset',lambda d:d.find(id='lt05').__setitem__('data-zo-task','wrong')),('wrong answer label',lambda d:d.find(id='loi-giai-2').__setitem__('data-zo-function','wrong')),('orphan heading',orphan_heading)]:
        broken=copy.deepcopy(doc);mutate(broken);checks['negative '+name]=not all(predicates(broken,bindings).values())
    if args.browser:
        images=out/'images';images.mkdir(exist_ok=True)
        g02=out/'g02-compat/g02-reading.html'
        if not g02.is_file():raise ValueError('Fresh shared-source G02 regression preview required')
        checks.update(browser_checks(page,images));checks.update(editorial_browser(page,g02,images));checks.update(targeted_browser(page,g02,images))
    failed=[k for k,v in checks.items() if not v]
    inputs=[ROOT/PACKAGE/'index.qmd', ROOT/PACKAGE/'_quy_trinh/kien_truc_hoc_tap.yml', PLAN,
            ROOT/PACKAGE/'giao_dien/he_nhan.json', Path(__file__),
            ROOT/'scripts/zo_r1_g01_labels.py', ROOT/'scripts/zo_r1_g01_editorial_check.py',
            ROOT/'scripts/zo_web_2027_production.py', ROOT/'_design/web_2027_mau_dung_chung/r1-controller.js']
    inputs.extend((ROOT/PACKAGE.parent/'_dung_chung').rglob('*.qmd'))
    report={'governance':governance,'checks':checks,'situation_review':situation_review,'passed':len(checks)-len(failed),'total':len(checks),'failures':failed,'html':str(page),'html_sha256':sha(page.read_bytes()),'source_sha256':sha((ROOT/PACKAGE/'index.qmd').read_bytes()),'guard_sha256':sha(Path(__file__).read_bytes()),'source_hashes':{p.relative_to(ROOT).as_posix():sha(p.read_bytes()) for p in inputs},'limits':['Edge only; no Safari/Firefox, physical touch or screen reader','Source-target/wording and representative runtime checks, not independent mathematical peer review','G02 shared-source compatibility only, not G02 label migration or acceptance'],'acceptance':'pending_owner_review','pdf_built':False,'promoted':False,'published':False}
    report['historical_owner_draft_checked'] = args.owner_draft is not None
    (out/args.report).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['passed','total','failures']},ensure_ascii=False,indent=2));return int(bool(failed))

if __name__=='__main__':raise SystemExit(main())

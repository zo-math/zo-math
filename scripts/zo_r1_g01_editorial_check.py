"""RD01–RD21 editorial regression guard for G01, not owner acceptance or release.

Run via zo_python.py with an explicit fresh raw HTML and isolated adapted HTML.
Builds never depend on this report or historical audit HTML. Baseline checks are
optional comparisons; canonical wording is always read from current QMD.
"""
from __future__ import annotations
import argparse, copy, inspect, json, re, socket, subprocess, sys, tempfile, time
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import unquote
import requests, yaml
from bs4 import BeautifulSoup, Comment, Tag
sys.dont_write_bytecode=True
from zo_web_2027_production import pools, norm, sha, content_fingerprint
from zo_web_2027_check import Browser, GEOMETRY, edge_executable
from zo_web_2027_g01_checkpoint import browser_checks
from zo_2027_governance_check import governance_context, evidence_current, learning_map_checks
ROOT=Path(__file__).resolve().parents[1]
PKG=Path('content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01')
COMMON=ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu/_dung_chung'
GOALS=['Dùng đúng điều kiện','Nối các biểu diễn','Xét và gọi đúng cực trị','Đọc trong giới hạn dữ kiện','Đánh giá và sửa lập luận']
LIMIT='Chưa có bài mới để xác nhận thêm ở mục tiêu này'

def parse(p):return BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
def browser_guard_fingerprint():
    # Bind the reused subset to its own predicates/harness, not all governance.
    parts=[inspect.getsource(editorial_browser).encode('utf-8')]
    parts.extend((ROOT/'scripts'/n).read_bytes() for n in [
        'zo_web_2027_g01_checkpoint.py','zo_web_2027_check.py'])
    return sha(b'\n'.join(parts))
def maths(n):return [norm(a.get_text()) for a in n.select('annotation') if not a.find_parent(class_='zo-variation-native')]
def task_maths(node):
    # The approved editorial pass rewrites return guidance, not the task itself.
    # Keep the complete fresh-render math projection check independently below.
    result=[]
    for a in node.select('annotation'):
        p=a.find_parent('p')
        if p and p.get_text(' ',strip=True).startswith('Điểm quay về:'):continue
        result.append(norm(a.get_text()))
    return result
def textkeys(n):
    return Counter(sha(norm(str(s))) for s in n.find_all(string=True) if norm(str(s)) and not s.find_parent('math') and not isinstance(s,Comment))
def walk(n):
    yield n
    for c in n.get('children',[]):yield from walk(c)
def semantic(doc, manifest):
    """The same predicates run against real pages and deliberately broken fixtures."""
    get=lambda i:doc.find(id=i)
    start=get('cách-học-với-tài-liệu-này')
    practice=get('phieu-luyen'); stages=get('lo-trinh-hoc')
    opening=[]
    for n in get('tu-kiem-tra').find_all(recursive=False):
        if n.get('id')=='kt01':break
        opening.append(n)
    test_text=' '.join(n.get_text(' ',strip=True) for n in opening if n.name!='details')
    result=get('đọc-kết-quả-tự-kiểm-tra')
    owner=result if 'reading-region' in result.get('class',[]) else result.find_parent(class_='reading-region') or result.select_one('.reading-region')
    def targets(i):return {unquote(a['href'][1:]) for a in get(i).select('a[href^="#"]')}
    task_rows=manifest.get('tasks',manifest.get('nhiem_vu',[]))
    checkpoint_rows=manifest.get('checkpoints',[])
    cp=next((n for n in checkpoint_rows if n.get('id')=='CP-LT3'),{})
    # Actual manifest uses mappings with explicit entries; normalize below.
    if isinstance(checkpoint_rows,dict):cp=checkpoint_rows.get('CP-LT3',{})
    predicates={
        'RD01/RD06: entry choices/map/continuous self-assessment':all(s in start.get_text(' ',strip=True) for s in ['Chọn nơi bắt đầu','Bản đồ học','Trong Bài học, Luyện tập, Ôn lại']) and not start.find('ol',recursive=False) and all(learning_map_checks(doc).values()),
        'RD02: stages owned by practice, not Start':bool(stages.find_parent(id='phieu-luyen')) and not get('bat-dau').find(id='lo-trinh-hoc') and len(stages.select('tbody tr'))==3,
        'RD03: visible practice instructions and closed supplementary guide':all(s in practice.get_text(' ',strip=True) for s in ['giữ bài làm','không mặc định cần thêm một bài thứ ba']) and not get('cach-thuc-hien-luyen-tap').has_attr('open'),
        'RD04: redundant start CTA removed, hero CTA retained':not start.select('.r1-start-action') and bool(doc.select_one('.hero a[href="#bai-hoc"]')),
        'RD05/RD08: test conditions visible with guide closed':all(s in test_text for s in ['45 phút','20','năm nhiệm vụ','tự lực hoàn toàn','Ôn nền','Sửa lỗi','không mô phỏng','đủ tự tin','Không được chia Kiểm tra thành nhiều đợt']) and '45 phút' not in start.get_text(),
        'RD07: goals/prerequisites visible in Start':all(s in get('bat-dau').get_text() for s in GOALS) and 'thương sai phân' in get('bat-dau').get_text() and not get('bat-dau').find_parent('details'),
        'RD09: LT3 sends learner to actual test': 'tu-kiem-tra' in targets('cp-lt3') and 'cp-kt' not in targets('cp-lt3'),
        'RD10/RD21: results table/heading/return have one owner':bool(owner and owner.find(id='r1-table-t17') and owner.find('h3') and owner.select_one('a[href="#cp-kt"]')) and 'đọc-kết-quả-tự-kiểm-tra' in targets('cp-kt'),
        'RD11/RD12: bounded confirmation bank, no compulsory third task':all(LIMIT in get(i).get_text() for i in ['cp-lt1','cp-lt2','cp-lt3','cp-kt','on-nen','sua-loi']) and 'không phải tự tìm thêm bài thứ ba' in get('cp-lt1').get_text(),
        'RD13: five test solutions route to S-K, not S-L':all(not any(t.startswith('sc') for t in targets(i)) and any(t.startswith('g01-s-k-') for t in targets(i)) for i in ['loi-giai-10','loi-giai-11','loi-giai-12','loi-giai-13','loi-giai-14']),
        'RD14: exact 14 journal fields/example in actual L02/sc02 context':len(doc.select('#r1-table-t13 tbody tr'))==14 and len(doc.select('#r1-table-t18 tbody tr'))==14 and [n.get_text(' ',strip=True) for n in doc.select('#r1-table-t13 tbody th')]==[n.get_text(' ',strip=True) for n in doc.select('#r1-table-t18 tbody th')] and all(s in get('nhat-ky').get_text().lower() for s in ['nhiệm vụ 02 của luyện tập','nhiệm vụ 02 của sửa lỗi sau luyện tập','chặng 1']),
        'RD15/RD16: review calendar and primary/durability distinguished':all(s in get('on-lai').get_text() for s in ['hoàn tất lượt chính','2–3 ngày','7 ngày','3–4 tuần','không phải chờ']) and not get('on-lai').has_attr('open'),
        'RD17: narrow foundation explains one-sided limits/difference quotient':all(s in get('nen-n-lt-01').get_text() for s in ['thương sai phân','giới hạn một phía']) and len(get('nen-n-lt-01').select('math'))>0,
        'RD18: finite-zero split not labeled inverse theorem':'E06' not in get('loi-giai-1').get_text() and 'ngắt khoảng máy móc' in get('loi-giai-1').get_text() and 'không phải lỗi suy chiều đảo' in get('loi-giai-11').get_text(),
        'RD19: result table shares exact five learner goal names':[r.find(['th','td']).get_text(' ',strip=True) for r in get('r1-table-t17').select('tbody tr')]==GOALS,
        'RD20: S-L criteria/caller/direct-entry instructions':all('Tiêu chí:' in get('sc'+str(i).zfill(2)).get_text() for i in range(1,9)) and all(i in targets('sua-loi-sau-luyen-tap') for i in ['cp-lt1','cp-lt2','cp-lt3']),
        'all disclosures authored closed':not doc.select('.reader-content details[open]'),
        'no nested papers':not doc.select('.reading-region .reading-region'),
    }
    return predicates

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--html',type=Path,required=True);ap.add_argument('--raw',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True);ap.add_argument('--baseline',type=Path);ap.add_argument('--g02-html',type=Path);ap.add_argument('--g02-raw',type=Path);ap.add_argument('--browser',action='store_true');ap.add_argument('--reuse-browser-report',type=Path)
    args=ap.parse_args();out=args.output.resolve()
    if not out.is_relative_to(ROOT/'_audit'):raise ValueError('Reports must remain under _audit')
    out.mkdir(parents=True,exist_ok=True);checks={}
    governance,governance_checks,governance_registry=governance_context()
    checks.update({'governance: '+k:v for k,v in governance_checks.items()})
    checks['governance: no open G01 learning-route blockers']=not governance_registry['products']['R1-G01']['open_blockers']
    checks['governance: G01 situation audit passed']=governance_registry['products']['R1-G01']['situation_audit']=='passed'
    def test(name,value):checks[name]=bool(value)
    page=parse(args.html);raw=parse(args.raw);root=raw.select_one('.zo-on-thi-package');view=page.select_one('.reader-content')
    manifest=yaml.safe_load((ROOT/PKG/'_quy_trinh/kien_truc_hoc_tap.yml').read_text(encoding='utf-8'))
    checks.update(semantic(page,manifest))
    plan=json.loads((ROOT/PKG/'giao_dien/web_2027_layout.json').read_text(encoding='utf-8'))
    test('strict canonical fingerprint equals fresh source',plan['source_fingerprint']==content_fingerprint(root))
    test('fresh math retained in exact order',maths(root)==maths(view))
    # Support is an accepted separate shell section, outside reader-content.
    missing_ids=sorted(set(n['id'] for n in root.select('[id]'))-set(n['id'] for n in page.select('[id]')))
    duplicates={i:n for i,n in Counter(n['id'] for n in page.select('[id]')).items() if n>1}
    test('source IDs retained/unique',not missing_ids and not duplicates)
    # Missing any newly added wording is a failure even if all hash keys decode.
    layoutkeys=Counter(n['text'] for n in walk(plan['layout']) if 'text' in n)
    omissions=textkeys(root)-layoutkeys
    historical=Counter()
    if args.baseline:
        oldplan=json.loads((args.baseline/'g01-layout-before.json').read_text(encoding='utf-8'))
        oldroot=parse(args.baseline/'before/r1_g01-raw/docs'/PKG/'index.html').select_one('.zo-on-thi-package')
        historical=textkeys(oldroot)-Counter(n['text'] for n in walk(oldplan['layout']) if 'text' in n)
        test('all existing mathematical task payloads retained',all(Counter(task_maths(oldroot.find(id=n['source_anchor'])))<=Counter(task_maths(root.find(id=n['source_anchor']))) for n in manifest['tasks']))
        test('G02 own QMD unchanged',(args.baseline/'r1_g02-before.qmd').read_bytes()==(ROOT/PKG.parent/'r1_g02/index.qmd').read_bytes())
        baseline=json.loads((args.baseline/'before.json').read_text(encoding='utf-8'))
        gov='content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/'
        allowed={gov+n for n in ['README.md','03_dieu_hanh_chuong_trinh.md','04_nhat_ki_quyet_dinh.md','08_danh_muc_tham_quyen_dieu_hanh.md','goi/R1_G01.md']}
        changed=[p for p,h in baseline.items() if p not in allowed and (not (ROOT/p).is_file() or sha((ROOT/p).read_bytes())!=h)]
        test('PDF/docs/index/unrelated baseline preserved',not changed)
        (out/'protected-comparison.json').write_text(json.dumps({'changed_outside_scope':changed,'allowed_status_updates':sorted(allowed)},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        test('historical acceptance receipt unchanged',json.loads((args.baseline/'g01-accepted-before.json').read_text(encoding='utf-8'))==json.loads((ROOT/PKG/'giao_dien/web_2027_accepted.json').read_text(encoding='utf-8')))
    new_omissions=omissions-historical
    test('no newly omitted canonical wording',not new_omissions)
    test('math assets unchanged',all(sha((ROOT/p).read_bytes())==h for p,h in plan['source_asset_hashes'].items()))
    rows=manifest.get('checkpoints',[])
    if isinstance(rows,list):cp=next(n for n in rows if n['id']=='CP-LT3')
    else:cp=rows['CP-LT3']
    test('manifest LT3 targets K01–K05',cp['paths']['pass']['target_ids']==['G01-K01','G01-K02','G01-K03','G01-K04','G01-K05'])
    tasks=manifest['tasks']
    test('manifest S-L keeps activation context',all(n['next_on_pass']['kind']=='activation_checkpoint' for n in tasks if re.fullmatch(r'G01-S-L-E\d+',n['id'])))
    # Calendar calculation is evidence for the stated origin, not a scheduler.
    origin=date(2026,10,10)
    test('calendar from primary completion',[(origin+timedelta(days=d)).isoformat() for d in [2,3,7,21,28]]==['2026-10-12','2026-10-13','2026-10-17','2026-10-31','2026-11-07'])
    # Mutation testing: exercise the actual predicates, not merely byte changes.
    def orphan_result(d):
        n=d.find(id='đọc-kết-quả-tự-kiểm-tra').select_one('.reading-region')
        n['class']=[]
    mutations=[('RD02',lambda d:d.find(id='bat-dau').append(d.find(id='lo-trinh-hoc').extract())),
        ('RD09',lambda d:d.find(id='cp-lt3').find('a',href='#tu-kiem-tra').__setitem__('href','#cp-kt')),
        ('RD13',lambda d:d.find(id='loi-giai-10').find('a',href='#g01-s-k-e01').__setitem__('href','#sc01')),
        ('RD14',lambda d:d.select_one('#r1-table-t13 tbody tr').extract()),
        ('RD19',lambda d:setattr(d.select_one('#r1-table-t17 tbody tr th'),'string','Wrong goal')),
        ('RD11',lambda d:d.find(id='cp-lt1').replace_with(BeautifulSoup('<section id="cp-lt1">Làm bài mới bất kì</section>','html.parser').section)),
        ('RD21',orphan_result)]
    for rd,mutate in mutations:
        broken=copy.deepcopy(page);mutate(broken);values=semantic(broken,manifest)
        test('negative fixture detects '+rd,any(not v for k,v in values.items() if rd in k))
    if args.g02_raw:
        graw=parse(args.g02_raw)
        test('shared journal in G02 retains exact field names',[n.get_text(' ',strip=True) for n in graw.select('#r1-table-t13 tbody th')]==[n.get_text(' ',strip=True) for n in raw.select('#r1-table-t13 tbody th')])
        test('shared narrow N-LT present in G02','thương sai phân' in graw.find(id='nen-n-lt-01').get_text())
        if args.g02_html:
            gpage=parse(args.g02_html)
            test('G02 fresh math preserved',maths(gpage.select_one('.reader-content'))==maths(graw.select_one('.zo-on-thi-package')))
            test('G02 no nested papers',not gpage.select('.reading-region .reading-region'))
    if args.browser:
        images=out/'images';images.mkdir(exist_ok=True)
        checks.update(browser_checks(args.html.resolve(),images))
        checks.update(editorial_browser(args.html.resolve(),args.g02_html.resolve() if args.g02_html else None,images))
    reused=None
    if args.reuse_browser_report:
        if args.browser:raise ValueError('Choose fresh browser run OR explicit same-candidate evidence reuse')
        prior=json.loads(args.reuse_browser_report.read_text(encoding='utf-8'))
        # Only browser checks are reused; current learning predicates run above.
        # Learning-policy edits do not expire browser-only evidence. Inputs and
        # browser predicate implementation must still match the checked scope.
        if not evidence_current(prior,governance,required_rules=()):
            raise ValueError('Resolve current authority conflict before evidence reuse')
        if prior.get('browser_guard_sha256')!=browser_guard_fingerprint():
            raise ValueError('Browser predicates/harness changed or legacy report lacks scoped binding; rerun browser checks only')
        if prior['html_sha256']!=sha(args.html.read_bytes()) or prior['canonical_source_sha256']!=sha((ROOT/PKG/'index.qmd').read_bytes()):
            raise ValueError('Cannot reuse browser checks after candidate/source drift')
        # Retain the original report/guard hash as evidence, not owner acceptance.
        browser_names=[n for n in prior['checks'] if re.match(r'^\d+(?:/| |:)',n) or n.startswith(('no JS','no-JS','negative geometry','multiple tabs'))]
        if len(browser_names)<300:raise ValueError('Incomplete browser evidence')
        checks.update({n:prior['checks'][n] for n in browser_names})
        reused={'report':str(args.reuse_browser_report),'report_sha256':sha(args.reuse_browser_report.read_bytes()),'guard_sha256':prior['guard_sha256'],'checks':len(browser_names),'reason':'Same HTML/QMD inputs and browser predicates/harness; current learning checks rerun separately; unrelated governance edits do not expire browser checks'}
    failures=[k for k,v in checks.items() if not v]
    report={'governance':governance,'checks':checks,'passed':len(checks)-len(failures),'total':len(checks),'failures':failures,'html':str(args.html.resolve()),
        'html_sha256':sha(args.html.read_bytes()),'canonical_source_sha256':sha((ROOT/PKG/'index.qmd').read_bytes()),
        'guard_sha256':sha(Path(__file__).read_bytes()),'browser_guard_sha256':browser_guard_fingerprint(),'new_omissions':dict(new_omissions),'missing_ids':missing_ids,'duplicate_ids':duplicates,'reused_browser_evidence':reused,
        'limits':['Owner HTML review pending','No PDF build/promotion/stage/commit/publish','Edge only; not physical touch/screen reader','No complete new independent mathematical peer review']}
    (out/'editorial-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['passed','total','failures']},ensure_ascii=False))
    return int(bool(failures))

def editorial_browser(page,g02,images):
    checks={}
    def test(n,v):checks[n]=bool(v)
    with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
    with tempfile.TemporaryDirectory(prefix='editorial_browser_',dir=images.parent) as profile:
        proc=subprocess.Popen([edge_executable(),'--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check',f'--remote-debugging-port={port}','--remote-debugging-address=127.0.0.1','--remote-allow-origins=http://localhost','--user-data-dir='+profile,'about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        b=None
        try:
            endpoint=f'http://127.0.0.1:{port}'
            for _ in range(100):
                try:
                    if requests.get(endpoint+'/json/version',timeout=.3).ok:break
                except requests.RequestException:time.sleep(.1)
            target=requests.put(endpoint+'/json/new?about:blank',timeout=10).json();b=Browser(target['webSocketDebuggerUrl']);b.call('Page.enable');b.call('Runtime.enable')
            for width in [1440,430,390]:
                b.viewport(width,960 if width>500 else 844);url=page.as_uri();b.navigate(url)
                for name,route in [('start','bat-dau'),('practice','phieu-luyen'),('test','tu-kiem-tra'),('result','đọc-kết-quả-tự-kiểm-tra'),('repair','sc02'),('journal','nhat-ky'),('review','on-lai'),('foundation','nen-n-lt-01')]:
                    b.navigate(url+'#'+route);b.screenshot(images/f'editorial-{name}-{width}.png')
                    test(f'{width}/{name}: target visible',b.evaluate('!!document.getElementById('+json.dumps(route)+').getClientRects().length'))
                # Follow the real CP link into S-L; each caller must survive reload,
                # answer round-trip, browser Back and the explicit return action.
                for cp in ['cp-lt1','cp-lt2','cp-lt3']:
                    b.navigate(url+'#'+cp);b.click('#'+cp+' a[href="#sua-loi-sau-luyen-tap"]')
                    test(f'{width}/{cp}: actual support link records caller',b.evaluate('new URL(location.href).searchParams.get("r1-return")')==cp)
                    b.navigate(b.evaluate('location.href').split('#')[0]+'#sc04')
                    b.click('#sc04 .answer-link a');b.click('#lg-sc04 .answer-link a')
                    test(f'{width}/{cp}: answer round-trip retains caller',b.evaluate('new URL(location.href).searchParams.get("r1-return")')==cp)
                    b.call('Page.reload');b.ready()
                    test(f'{width}/{cp}: reload return target',b.evaluate('document.querySelector(".r1-return-link").hash')=='#'+cp)
                    b.click('.r1-return-link');test(f'{width}/{cp}: returns to actual caller',b.evaluate('location.hash')=='#'+cp)
                    b.evaluate('history.back()');b.ready();test(f'{width}/{cp}: Back preserves return',b.evaluate('new URL(location.href).searchParams.get("r1-return")')==cp)
                b.navigate(url+'#sua-loi-sau-luyen-tap')
                test(f'{width}: direct S-L exposes three manual caller links',b.evaluate('document.querySelectorAll("#sua-loi-sau-luyen-tap a[href^=\\"#cp-lt\\"]").length')==3)
                if g02:
                    b.navigate(g02.as_uri()+'#nhat-ky');test(f'{width}: G02 journal visible/no page overflow',b.evaluate('document.getElementById("nhat-ky").getClientRects().length>0&&document.documentElement.scrollWidth<=innerWidth+1'))
                    b.screenshot(images/f'g02-journal-{width}.png')
                    b.navigate(g02.as_uri()+'#nen-n-lt-01');test(f'{width}: G02 foundation closed except deep-link ancestors',b.evaluate('(()=>{let n=document.getElementById("nen-n-lt-01");return n.getClientRects().length>0&&!document.querySelector(".reading-region .reading-region")})()'))
            # Separate tabs carry their own URL context, not a global last caller.
            b.navigate(page.as_uri()+'?r1-view=sua-loi&r1-return=cp-lt2&r1-context=cp-lt2#sc04')
            other=requests.put(endpoint+'/json/new?about:blank',timeout=10).json();second=Browser(other['webSocketDebuggerUrl']);second.call('Page.enable');second.call('Runtime.enable')
            try:
                second.navigate(page.as_uri()+'?r1-view=sua-loi&r1-return=cp-lt3&r1-context=cp-lt3#sc04')
                test('multiple tabs: independent CP return',b.evaluate('document.querySelector(".r1-return-link").hash')=='#cp-lt2' and second.evaluate('document.querySelector(".r1-return-link").hash')=='#cp-lt3')
            finally:second.ws.close()
            # ready() waits for JS image/font promises; with scripts disabled,
            # navigate directly and inspect the DOM without those promises.
            b.call('Emulation.setScriptExecutionDisabled',{'value':True})
            b.call('Page.navigate',{'url':page.as_uri()});time.sleep(.6)
            test('no-JS: test conditions and goals visible while guides closed',b.evaluate('(()=>{let n=document.getElementById("tu-kiem-tra"),s=document.getElementById("bat-dau");return n.getClientRects().length>0&&s.getClientRects().length>0&&!document.querySelector(".reader-content details[open]")})()'))
        finally:
            if b:b.ws.close()
            proc.terminate()
            try:proc.wait(timeout=10)
            except subprocess.TimeoutExpired:proc.kill();proc.wait()
    return checks

if __name__=='__main__':raise SystemExit(main())

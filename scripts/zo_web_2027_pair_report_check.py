"""QD_028 pair evidence. No rendering, promotion, PDF or Git writes.

Historical gates remain unchanged. This gate explicitly permits only the
authorized G02 S-O-E06 replacement and the G01 O03 added limit/table proof.
"""
import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
from urllib.parse import unquote
sys.dont_write_bytecode=True
import requests
from bs4 import BeautifulSoup
from zo_r1_g01_labels_check import predicates as g01_predicates, situations as g01_situations, targeted_browser
from zo_r1_g02_labels_check import predicates as g02_predicates, situations as g02_situations, validate_binding, browser_checks as g02_browser
from zo_web_2027_g01_checkpoint import browser_checks as g01_browser
from zo_web_2027_g02_sync_check import parity
from zo_web_2027_check import Browser, edge_executable
from zo_r1_g01_editorial_check import maths, task_maths
from zo_web_2027_production import content_fingerprint

ROOT=Path(__file__).resolve().parents[1]
BASE=Path('content/thpt/on_thi_toan_thpt/hoc_lieu')
GOV=Path('content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh')
GOV_ALLOWED={'README.md','01_kien_truc_hoc_tap.md','02_quy_trinh_va_nghiem_thu.md',
    '03_dieu_hanh_chuong_trinh.md','04_nhat_ki_quyet_dinh.md',
    '07_quy_chuan_cau_truc_trang_nguoi_hoc.md','08_danh_muc_tham_quyen_dieu_hanh.md',
    'danh_muc_kien_truc_hoc_tap.yml','hop_dong_dieu_hanh.json','quy_chuan_goi_qmd.md',
    'goi/R1_G01.md','goi/R1_G02.md'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def parse(p):return BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
def save(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def owner(n):
    return next((p.get('id') for p in [n,*n.parents] if p.name=='section' and p.parent and 'reader-content' in p.parent.get('class',[])),None)
def pair_predicates(doc,package):
    root=doc.select_one('.reader-content');checks={}
    checks['M13 no generic stage/review duplicate label']=not any(n.get_text(' ',strip=True) in ['Chặng học','Ôn lại · Nhiệm vụ'] for n in root.select('[data-reading-label]'))
    test=root.find(id='tu-kiem-tra')
    heading=test.find(['h2','h3'])
    paper=heading.find_parent(class_='reading-region')
    checks['M16 test is not self-check']=not any(n.get_text(' ',strip=True).casefold()=='tự kiểm tra' for n in paper.select('[data-reading-label]'))
    checks['M18 result guide owned by test']=owner(root.find(id='đọc-kết-quả-tự-kiểm-tra'))=='tu-kiem-tra'
    checks['M24 retired checkpoint term absent']='Điểm kiểm soát' not in root.get_text(' ',strip=True)
    checks['M35 no heading-only paper']=all(p.select('li,table,figure,details,.zo-learning-task') or any(n.get_text(' ',strip=True) for n in p.select('p')) for p in root.select('.reading-region') if not p.has_attr('data-support'))
    checks['M36 no redundant example label']=not any(n.get_text(' ',strip=True).casefold()=='ví dụ' and n.find_parent(class_='reading-region').find(['h2','h3','h4','h5']).get_text(' ',strip=True).casefold().startswith('ví dụ') for n in root.select('[data-reading-label]') if n.find_parent(class_='reading-region').find(['h2','h3','h4','h5']))
    checks['M43 neutral drawer vocabulary']=doc.select_one('.mobile-trigger').get('aria-label')=='Mở mục lục học liệu' and 'Mục lục học liệu' in doc.select_one('#mobile-nav').get_text(' ',strip=True)
    ids=[n['id'] for n in doc.select('[id]')];checks['unique IDs']=len(ids)==len(set(ids))
    checks['all internal fragments resolve']=all(doc.find(id=unquote(a['href'][1:])) for a in root.select('a[href^="#"]') if len(a['href'])>1)
    checks['closed authored disclosures']=not root.select('details[open]')
    if package=='r1_g01':
        answer=root.find(id='lg-g01-o03')
        checks['M21 BBT14 exists inside O03 answer']=bool(answer.select_one('[data-bbt="BBT14"] .zo-variation-native'))
        # F is defined at zero, with unequal one-sided derivatives there.
        native=answer.select_one('.zo-variation-native')
        checks['M21 F zero defined but derivative undefined']=bool(native) and native.select_one('[data-source-value="Không xác định"]') is not None and native.select_one('[data-source-value="−2"]') is not None and len(native.select('[data-source-value="0"]'))>=3
        retry=root.find(id='g01-s-o-e05')
        checks['M29 exact unused recovery task and honest exhaustion']=bool(retry.select_one('a[href="#sc05"]')) and all(x in retry.get_text(' ',strip=True).casefold() for x in ['chưa','nhật kí'])
        checks['M34 no extra warmup return outside atomic answers']=not root.find(id='loi-giai-khoi-dong').select(':scope > p a[href="#bắt-đầu-từ-đâu"]')
        summary=root.find(id='g01-loi-giai-sua-loi-mau').select_one('summary')
        checks['M36 sample repair answer title once']=summary.get_text(' ',strip=True).count('Nhiệm vụ 07')==1 and 'Nhiệm vụ 07' not in root.find(id='lg-cg01').get_text(' ',strip=True)
    else:
        checks['M27 graph-label proof routes to graph target']=bool(root.find(id='cp-lt2').select_one('a[href="#g02-nen-do-thi-xac-nhan"]')) and bool(root.select_one('#r1-g02-table-t04 a[href="#g02-nen-do-thi-xac-nhan"]'))
        answer=root.find(id='loi-giai-s-o-e06');q=root.find(id='s-o-e06')
        checks['M28 new quadratic-jump retry not exposed linear example']=any('x^2' in a.get_text() for a in q.select('annotation')) and all(x in answer.get_text(' ',strip=True).casefold() for x in ['4','không']) and '-1' in maths(answer)
        checks['M30 logarithm evidence not exponential']=all(x in root.find(id=i).get_text(' ',strip=True).casefold() for i in ['cp-p','loi-giai-s-p02'] for x in ['lôgarit','mũ','chưa'])
        checks['M31 transfer retry hierarchy same']=root.find(id='thu-lai-chuyen-giao').find(['h3','h4']).name==root.find(id='s-p02').find(['h3','h4']).name
        checks['M10 closed interval worked example not independent task']=root.find(id='g02-vi-du-tren-doan').get('data-zo-type')=='example' and not root.find(id='g02-vi-du-tren-doan').has_attr('data-zo-task')
    return checks

def extra_browser(pages,out):
    checks={};out.mkdir(parents=True,exist_ok=True)
    with socket.socket() as probe:probe.bind(('127.0.0.1',0));port=probe.getsockname()[1]
    with tempfile.TemporaryDirectory(prefix='edge_pair_',dir=out,ignore_cleanup_errors=True) as profile:
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
            for package,page in pages.items():
                review='g01-o01' if package=='r1_g01' else 'o01'
                def isolated(view):
                    return b.evaluate('(()=>{const r=document.getElementById('+json.dumps(review)+'),j=document.getElementById("nhat-ky");return [!!r.getClientRects().length,!!j.getClientRects().length,document.querySelector("#r1-view-panel").dataset.r1View]})()')==([False,True,'nhat-ky'] if view=='nhat-ky' else [True,False,'on-lai'])
                for width in [1440,390,320]:
                    b.viewport(width,844)
                    b.navigate(page.as_uri()+'?r1-view=on-lai');checks[f'{package}/{width}/M33 review isolated']=isolated('on-lai')
                    b.click('button.r1-tab[id="r1-tab-nhat-ky"]');checks[f'{package}/{width}/M33 journal isolated']=isolated('nhat-ky')
                    b.call('Page.reload');b.ready();checks[f'{package}/{width}/M33 journal reload']=isolated('nhat-ky')
                    b.evaluate('history.back()');time.sleep(.3);checks[f'{package}/{width}/M33 Back restores review']=isolated('on-lai')
                    if width<1000:
                        b.evaluate('document.querySelector(".mobile-trigger").focus()');b.key('Enter',13,'\r')
                        checks[f'{package}/{width}/keyboard drawer Enter']=b.evaluate('document.getElementById("mobile-nav").open')
                        b.key('Escape',27);checks[f'{package}/{width}/keyboard Escape restores focus']=b.evaluate('!document.getElementById("mobile-nav").open&&document.activeElement.matches(".mobile-trigger")')
                    b.navigate(page.as_uri()+'?r1-view=kiem-tra')
                    checks[f'{package}/{width}/prepared direct test accessible']=b.evaluate('document.querySelector("#r1-view-panel").dataset.r1View')=='kiem-tra'
                    b.screenshot(out/f'{package}-test-{width}.png')
        finally:
            if b:b.ws.close()
            proc.terminate()
            try:proc.wait(timeout=10)
            except subprocess.TimeoutExpired:proc.kill();proc.wait()
    return checks

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--audit',type=Path,required=True);ap.add_argument('--browser',action='store_true');args=ap.parse_args()
    audit=args.audit.resolve()
    if not audit.is_relative_to(ROOT/'_audit'):raise ValueError('Audit evidence only')
    checks={};groups={};situations={};pages={};inputs=set()
    for pkg,pred,situ in [('r1_g01',g01_predicates,g01_situations),('r1_g02',g02_predicates,g02_situations)]:
        page=audit/'after'/(pkg+'-render/docs')/BASE/pkg/'index.html';pages[pkg]=page
        rawpage=audit/'raw-final'/(pkg+'-raw/docs')/BASE/pkg/'index.html'
        oldpage=audit/(pkg+'-raw/docs')/BASE/pkg/'index.html'
        doc,raw,old=map(parse,[page,rawpage,oldpage]);r=doc.select_one('.reader-content');s=raw.select_one('.zo-on-thi-package');o=old.select_one('.zo-on-thi-package')
        binding_path=ROOT/BASE/pkg/'giao_dien/he_nhan.json';binding=json.loads(binding_path.read_text(encoding='utf-8'))
        if pkg=='r1_g02':validate_binding(binding)
        c=pred(doc,binding);c.update(pair_predicates(doc,pkg));situations[pkg]=situ(doc);c.update({k+' situation':v['passed'] for k,v in situations[pkg].items()})
        c['M24 retired checkpoint term absent']=c['M24 retired checkpoint term absent'] and 'Điểm kiểm soát' not in s.get_text(' ',strip=True) and 'điểm kiểm soát' not in s.get_text(' ',strip=True)
        c['canonical raw mathematics exactly projected']=Counter(maths(s))==Counter(maths(r))
        c['all old IDs retained']=set(n['id'] for n in o.select('[id]'))<=set(n['id'] for n in doc.select('[id]'))
        c['all fresh IDs retained']=set(n['id'] for n in s.select('[id]'))<=set(n['id'] for n in doc.select('[id]'))
        provenance=json.loads((audit/'after'/(pkg+'-render')/'provenance.json').read_text(encoding='utf-8'))
        c['HTML render source hash current']=provenance['sha256']==sha(ROOT/BASE/pkg/'index.qmd')
        for u in binding['units']:
            for key in ['question','answer']:
                ident=u.get(key)
                if not ident:continue
                oldnode,newnode=o.find(id=ident),s.find(id=ident)
                if oldnode and newnode and ident not in {'s-o-e06','loi-giai-s-o-e06','lg-g01-o03'}:
                    c[u['id']+'/'+key+' prior math unchanged']=Counter(task_maths(oldnode))==Counter(task_maths(newnode))
                if newnode and newnode.name!='span':
                    c[u['id']+'/'+key+' fresh math projected']=Counter(maths(newnode))==Counter(maths(r.find(id=ident)))
                elif newnode:
                    # Shared source ID is a zero-text span preceding the task.
                    # The adapter wraps that task, without changing its maths.
                    paragraph=newnode.find_parent('p').find_next_sibling('p')
                    c[u['id']+'/'+key+' shared span task math projected']=Counter(maths(paragraph))<=Counter(maths(r.find(id=ident)))
        if pkg=='r1_g01':
            plan=ROOT/BASE/pkg/'giao_dien/web_2027_layout.json';c['strict current source fingerprint']=json.loads(plan.read_text(encoding='utf-8'))['source_fingerprint']==content_fingerprint(s)
            inputs.add(plan)
        else:
            source_links={a['href'] for a in s.select('#r1-g02-table-t10 a[href]')};after_links={a['href'] for a in r.select('#r1-g02-table-t10 a[href]')}
            c['M37 resource table preserves canonical links']=bool(source_links) and source_links<=after_links
        # Negative fixtures run the same production-shape predicates.
        broken=copy.deepcopy(doc);broken.find(id='đọc-kết-quả-tự-kiểm-tra').extract();c['negative wrong result owner rejected']=not pair_predicates_safe(broken,pkg,'M18 result guide owned by test')
        broken=copy.deepcopy(doc);p=broken.select_one('.reading-region');[n.decompose() for n in list(p.find_all(recursive=False)) if n.name not in ['h2','h3','h4','h5'] and not n.has_attr('data-reading-label')];c['negative heading-only region rejected']=not pair_predicates_safe(broken,pkg,'M35 no heading-only paper')
        groups[pkg]=c;checks.update({pkg+'/'+k:v for k,v in c.items()})
        inputs.update([ROOT/BASE/pkg/'index.qmd',binding_path,ROOT/BASE/pkg/'_quy_trinh/kien_truc_hoc_tap.yml'])
        inputs.update([ROOT/BASE/pkg/'_quy_trinh/ho_so/index.yml',ROOT/BASE/pkg/f'cong_cu/{pkg}.lua'])
    before=json.loads((audit/'before.json').read_text(encoding='utf-8'))
    changed=[p for p,h in before.items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
    allowed={(GOV/n).as_posix() for n in GOV_ALLOWED}
    protected={'count':len(before),'authorized_governing_changes':[p for p in changed if p in allowed],'unexpected':[p for p in changed if p not in allowed]}
    checks['protected docs PDFs Design D0 Git index unchanged']=not protected['unexpected']
    checks['historical G01 acceptance receipt unchanged']=sha(audit/'g01-accepted-before.json')==sha(ROOT/BASE/'r1_g01/giao_dien/web_2027_accepted.json')
    inputs.update((ROOT/BASE/'_dung_chung').rglob('*.qmd'));inputs.update((ROOT/GOV).glob('*.*'))
    for name in ['zo_web_2027_pair_report_check.py','zo_r1_g01_labels_check.py','zo_r1_g02_labels_check.py','zo_r1_g01_labels.py','zo_web_2027_production.py','zo_web_2027_g02_production.py','zo_web_2027_g02.py','zo_r1_g01_rebind.py','zo_web_2027_figures.py']:inputs.add(ROOT/'scripts'/name)
    inputs.update(ROOT/'scripts'/n for n in ['zo_web_2027_check.py','zo_web_2027_g01_checkpoint.py','zo_web_2027_g02_sync_check.py'])
    inputs.update(p for p in (ROOT/'_design/web_2027_mau_dung_chung').rglob('*') if p.is_file() and p.suffix in ['.js','.css','.tpl','.json'])
    inputs.add(ROOT/BASE/'r1_g01/du_lieu/bang_bien_thien.json')
    def report():
        failures=[k for k,v in checks.items() if not v]
        save(audit/'qa.json',{'checks':checks,'passed':len(checks)-len(failures),'total':len(checks),'failures':failures,'situations':situations,'protection':protected,'html_hashes':{p.relative_to(ROOT).as_posix():sha(p) for p in pages.values()},'source_hashes':{p.relative_to(ROOT).as_posix():sha(p) for p in sorted(inputs)},'acceptance':'pending_owner_html_review','learning_pdf_built':False,'promoted':False,'published':False,'limits':['Edge headless only; not Safari/Firefox, physical touch or screen reader','Math projection and independently recomputed changed units; not full external mathematical peer review','No secure exam lockdown or automatic grading is claimed','Historical PDF files intentionally unchanged and stale against edited QMD']})
        print(json.dumps({'passed':len(checks)-len(failures),'total':len(checks),'failures':failures},ensure_ascii=False),flush=True)
        return not failures
    static_ok=report()
    if args.browser:
        for pkg,fn in [('r1_g01',g01_browser),('r1_g02',g02_browser)]:
            out=audit/'images'/pkg;out.mkdir(parents=True,exist_ok=True)
            print('Runtime',pkg,flush=True);checks.update({pkg+'/runtime/'+k:v for k,v in fn(pages[pkg],out).items()});report()
        checks.update({'pair/runtime/'+k:v for k,v in extra_browser(pages,audit/'images/extra').items()})
        checks.update({'G01/support/'+k:v for k,v in targeted_browser(pages['r1_g01'],pages['r1_g02'],audit/'images/r1_g01').items()})
        parity(pages['r1_g01'],pages['r1_g02'],audit/'images/parity')
        pair=json.loads((audit/'images/parity/pair.json').read_text(encoding='utf-8'));checks.update({'pair/style/'+k:v for k,v in pair['checks'].items()});report()
    return int(not report())

def pair_predicates_safe(doc,pkg,key):
    try:return pair_predicates(doc,pkg)[key]
    except (AttributeError,TypeError):return False
if __name__=='__main__':raise SystemExit(main())

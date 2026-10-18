"""G02 QD_021/024/025 application and scoped regression gate.

Builds an isolated preview from fresh configured raw HTML. Reports are evidence,
not owner acceptance, PDF currency or publication. Never edits learner sources.
"""
import argparse
from collections import Counter
import copy
import json
from pathlib import Path
import re
import socket
import subprocess
import tempfile
import time
from urllib.parse import unquote
import sys
sys.dont_write_bytecode = True
from bs4 import BeautifulSoup
import requests
from zo_learning_architecture import COMMON_CATALOG, load_yaml
from zo_learning_labels import read_sources, validate_catalog
from zo_web_2027_preview import sha
from zo_web_2027_check import Browser, GEOMETRY, edge_executable
from zo_r1_g01_labels import apply as apply_labels

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02'
BINDING = PACKAGE / 'giao_dien/he_nhan.json'
VIEWS = ['bat-dau','bai-hoc','luyen-tap','kiem-tra','on-lai','on-nen','sua-loi','nhat-ky','loi-giai','nguon','tai-tai-lieu','toan-van']


def read(path):
    return BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')


def validate_binding(data):
    terms = validate_catalog(load_yaml(COMMON_CATALOG))
    assert data['package'] == 'R1-G02' and data['decision'] == 'QD_025'
    assert data['status'] == 'source_applied_pending_html_acceptance'
    assert len(data['units']) == 64
    targets = [a for u in data['units'] for a in (u['question'], u['answer']) if a]
    assert len(targets) == len(set(targets))
    expected = {'function.practice':9,'function.test':5,'function.review':3,
                'function.remediation':18,'function.transfer':4,
                'function.warmup':3,'function.self_check':5,
                'function.foundation_confirmation':12,'function.guided_thinking':5}
    assert Counter(u['function'] for u in data['units']) == expected
    for function, count in expected.items():
        group = [u for u in data['units'] if u['function'] == function]
        assert function in terms
        prefix = "Gợi mở" if function=="function.guided_thinking" else "Nhiệm vụ"
        assert all(u['title'].startswith(f"{prefix} {u['number']:02d}") for u in group)
    knowledge=data['knowledge_units']
    assert len({u['id'] for u in knowledge})==len(knowledge)
    assert len({u['anchor'] for u in knowledge})==len(knowledge)
    assert all(u['type'] in terms for u in knowledge)
    # QD_028 adds one complete worked example on a closed interval, not
    # an independent task or an extra copy of a self-check's solution.
    assert Counter(u['type'] for u in knowledge)=={'type.definition':3,'type.theorem':1,'type.method':2,'type.example':2}
    assert any(u['anchor']=='g02-vi-du-tren-doan' and u['type']=='type.example' and u['owner']=='tren-doan' for u in knowledge)


def predicates(doc, data):
    root = doc.select_one('.reader-content')
    checks = {}
    for u in data['units']:
        if u['function']=='function.guided_thinking':
            q=root.find(id=u['question'])
            checks[u['id']+' prompt in its knowledge section']=bool(q and q.find_parent(id=u['question_owner'])) and not u.get('answer')
            checks[u['id']+' prompt title and semantic binding']=bool(q) and u['title'] in q.get_text(' ',strip=True) and q.get('data-zo-task')==u['id']
            checks[u['id']+' prompt and bridge share reading unit']=bool(q) and len([p for p in q.find_all('p') if not p.select_one('.r1-task-label,.zo-task-title') and p.get_text(' ',strip=True)!='Thử trả lời trước khi đọc tiếp.'])>=2
            continue
        q, a = root.find(id=u['question']), root.find(id=u['answer'])
        checks[u['id']+' bound question/answer'] = bool(q and a) and all(
            n.get('data-zo-task') == u['id'] and n.get('data-zo-function') == u['function']
            and n.get('data-zo-number') == str(u['number']) for n in (q,a))
        from zo_r1_g01_labels import local_answer_pair
        local=local_answer_pair(q,a)
        qlinks=q.select('.answer-link a[href="#'+u['answer']+'"]') if q else []
        alinks=a.select('.answer-link a[href="#'+u['question']+'"]') if a else []
        checks[u['id']+' question navigation matches ownership'] = bool(q and a) and len(qlinks)==(0 if local else 1)
        checks[u['id']+' answer navigation matches ownership'] = bool(q and a) and len(alinks)==(0 if local else 1)
        checks[u['id']+' matching title'] = bool(q and a) and u['title'] in q.get_text(' ',strip=True) and u['title'] in a.get_text(' ',strip=True)
        checks[u['id']+' question action is not redundant'] = bool(q) and len(qlinks)==(0 if local else 1)
    checks['foundation independent source owner'] = root.find(id='on-nen').find_parent('section') is None
    checks['no foundation inside lesson'] = not root.find(id='bai-hoc').find(id='on-nen')
    checks['result reading belongs to test'] = bool(root.find(id='đọc-kết-quả-tự-kiểm-tra').find_parent(id='tu-kiem-tra'))
    checks['three atomic warmups keep old wrapper'] = all(root.find(id='ba-câu-khởi-động').find(id='g02-khoi-dong-0'+str(i)) for i in range(1,4))
    checks['every disclosure initially closed'] = not root.select('details[open]')
    guide_papers = root.find(id='cách-học-với-tài-liệu-này').select('.reading-region')
    checks['G01 study-guide rhythm: map then support then completion'] = len(guide_papers) == 3 and all(
        guide_papers[0].find(id=a) for a in ['chọn-nơi-bắt-đầu','bản-đồ-học','r1-g02-table-t08'])
    checks['warmup tasks share the same reading result as G01'] = len({id(root.find(id=u['question']).find_parent(class_='reading-region')) for u in data['units'] if u['function']=='function.warmup'}) == 1
    checks['warmup and self-check use G01 task-title role'] = all(root.find(id=u['question']).select_one('.r1-task-label') for u in data['units'] if u['function'] in ['function.warmup','function.self_check'])
    from zo_course_numbering import html_checks as numbering_html_checks
    checks.update(numbering_html_checks(doc,data))
    checks['three-stage overview uses the shared table component'] = bool(root.select_one('#r1-g02-table-t11.r1-table')) and len(root.select('#r1-g02-table-t11 tbody tr')) == 3
    checks['foundation parent context labels valid'] = all(n.get_text(' ',strip=True).startswith('HỖ TRỢ KHI CẦN') for n in root.select('#on-nen [data-reading-label]'))
    checks['no heading duplicates its outer label'] = all(not p.find(['h2','h3','h4','h5']) or not p.find(attrs={'data-reading-label':True},recursive=False) or p.find(['h2','h3','h4','h5']).get_text(' ',strip=True).casefold()!=p.find(attrs={'data-reading-label':True},recursive=False).get_text(' ',strip=True).casefold() for p in root.select('.reading-region'))
    ids = [n['id'] for n in doc.select('[id]')]
    checks['unique DOM IDs'] = len(ids) == len(set(ids))
    checks['all local fragment targets exist'] = all(root.find(id=unquote(a['href'][1:])) or doc.find(id=unquote(a['href'][1:])) for a in root.select('a[href^="#"]'))
    checks['journal exactly 14 fields'] = len(root.select('#r1-table-t13 tbody tr')) == 14
    checks['study support table visible'] = not root.find(id='r1-g02-table-t08').has_attr('hidden')
    checks['main map has exactly four stages'] = [a['href'] for a in root.select('[data-learning-main] a')] == ['#bai-hoc','#phieu-luyen','#tu-kiem-tra','#on-lai']
    guide = root.find(id='cách-học-với-tài-liệu-này').get_text(' ',strip=True)
    help_text = root.find(id='g02-ho-tro-khi-can').get_text(' ',strip=True)
    test = root.find(id='tu-kiem-tra').get_text(' ',strip=True)
    checks['test entry prepared OR confident, single attempt'] = all(t in test for t in ['chuẩn bị kĩ lưỡng hoặc đủ tự tin','không chia thành nhiều đợt','tự lực hoàn toàn','kết thúc lượt kiểm tra','kết quả sau hỗ trợ'])
    checks['retired independent entry rule absent'] = 'Chỉ thử Kiểm tra trực tiếp khi đã có bài làm độc lập' not in root.get_text(' ',strip=True)
    checks['retired interleaved schedule absent'] = 'Đọc xong một bước thì tự giải bài liên quan' not in root.get_text(' ',strip=True)
    checks['bank exhaustion explicitly acknowledged'] = all(t in help_text for t in ['không còn nhiệm vụ mới phù hợp','không tính là bằng chứng độc lập mới','không tự đánh dấu đã đạt'])
    checks['14 situation targets exist'] = all(root.find(id=a) for a in [
        'g02-ho-tro-khi-can','bai-hoc','bắt-đầu-từ-đâu','nen-n-txd-01-xn01',
        'g02-khoi-dong-01','lg-g02-khoi-dong-01','phieu-luyen','cp-lt1','nen-n-dh-01-xn01',
        'sua-loi-sau-luyen-tap','tu-kiem-tra','cp-kt','đọc-kết-quả-tự-kiểm-tra',
        'sua-loi-sau-kiem-tra','on-lai','o02','loi-giai-on-lai-02','cp-on2',
        'g02-chuyen-goi','nhat-ky','r1-table-t13','on-nen','nen-quay-ve'])
    checks['support applies during learning and review, after test'] = 'Bài học, Luyện tập, Ôn lại và sau khi kết thúc Kiểm tra' in guide
    checks['jump is not achievement'] = 'phần bỏ qua không tự được xem là đã đạt' in guide
    checks['journal at decisions not every action'] = 'không cần ghi sau mọi thao tác' in help_text
    checks['direct support does not guess one return'] = 'chọn nhiệm vụ hoặc hoạt động em muốn quay về' in help_text
    checks['core and conditional transfer distinct'] = 'không phải điều kiện để hoàn tất năm mục tiêu cốt lõi' in guide
    checks['completion and spaced review coexist with next package'] = all(t in root.find(id='g02-chuyen-goi').get_text(' ',strip=True) for t in ['2–3 ngày, 7 ngày và 3–4 tuần','không cần chờ hết các lượt ôn'])
    for u in data['knowledge_units']:
        node=root.find(id=u['anchor'])
        checks[u['id']+' atomic knowledge binding']=bool(node) and node.get('data-zo-type')==u['type'].removeprefix('type.') and node.get('data-zo-unit')==u['id'] and bool(root.find(id=u['owner']))
    checks['two definitions not one box']=root.find(id='g02-dinh-nghia-gia-tri-lon-nhat') is not root.find(id='g02-dinh-nghia-gia-tri-nho-nhat')
    return checks


def situations(doc):
    """DH01-DH14 source wording/targets, not fourteen browser simulations."""
    root=doc.select_one('.reader-content')
    text=lambda i:root.find(id=i).get_text(' ',strip=True)
    link=lambda i,t:bool(root.find(id=i).select_one('a[href="#'+t+'"]'))
    guide=text('cách-học-với-tài-liệu-này');help_text=text('g02-ho-tro-khi-can')
    rules={
        'DH01':('đúng lời giải thích hoặc ví dụ trong Bài học' in help_text,['g02-ho-tro-khi-can','bai-hoc']),
        'DH02':(link('bắt-đầu-từ-đâu','nen-n-txd-01') and 'Khởi động chưa đủ' in guide,['bắt-đầu-từ-đâu','nen-n-txd-01','nen-n-txd-01-xn01']),
        'DH03':(link('g02-khoi-dong-01','lg-g02-khoi-dong-01') and link('lg-g02-khoi-dong-01','g02-khoi-dong-01'),['g02-khoi-dong-01','lg-g02-khoi-dong-01']),
        'DH04':('xem lại đúng lời giải thích hoặc ví dụ trong Bài học' in help_text and 'Nếu đã nắm phần học' in guide,['phieu-luyen','g02-ho-tro-khi-can','bai-hoc']),
        'DH05':(link('cp-lt1','nen-n-dh-01'),['cp-lt1','nen-n-dh-01','nen-n-dh-01-xn01']),
        'DH06':(all(link('cp-lt1',t) and root.find(id=t).find_parent(id='sua-loi') and root.find(id=t).get('data-zo-function')=='function.remediation' and 'SỬA LỖI · SAU LUYỆN TẬP' in text(t) for t in ['s00','s01','s02']) and 'Nếu đã đáp ứng tiêu chí, không cần qua mọi nhánh hỗ trợ' in help_text,['cp-lt1','sua-loi-sau-luyen-tap','s00','s01','s02']),
        'DH07':(all(t in guide for t in ['Trong lúc Kiểm tra, phải tự lực hoàn toàn','không dùng Bài học, Ôn nền, Lời giải hoặc Sửa lỗi','kết thúc lượt kiểm tra']) and all(t in text('tu-kiem-tra') for t in ['chuẩn bị kĩ lưỡng hoặc đủ tự tin','không chia thành nhiều đợt','kết quả sau hỗ trợ']),['cách-học-với-tài-liệu-này','tu-kiem-tra']),
        'DH08':(all(link('cp-kt',t) for t in ['đọc-kết-quả-tự-kiểm-tra','sua-loi-sau-kiem-tra','on-nen']) and 'bài làm ban đầu' in text('cp-kt'),['cp-kt','đọc-kết-quả-tự-kiểm-tra','sua-loi-sau-kiem-tra','on-nen']),
        'DH09':('Bài học, Luyện tập, Ôn lại và sau khi kết thúc Kiểm tra' in guide and link('cp-on2','nen-n-gh-01'),['cách-học-với-tài-liệu-này','cp-on2','bai-hoc','on-nen']),
        'DH10':(link('o02','loi-giai-on-lai-02') and link('loi-giai-on-lai-02','o02') and link('cp-on2','sua-loi-sau-on-lai'),['o02','loi-giai-on-lai-02','sua-loi-sau-on-lai','cp-on2']),
        'DH11':(len(root.select('#r1-table-t13 tbody tr'))==14 and 'không cần ghi sau mọi thao tác' in help_text,['g02-ho-tro-khi-can','nhat-ky','r1-table-t13']),
        'DH12':('Em có thể đi tới hoặc quay lại' in guide and 'phần bỏ qua không tự được xem là đã đạt' in guide,['cách-học-với-tài-liệu-này']),
        'DH13':('Nếu vào thẳng phần hỗ trợ, chọn nhiệm vụ hoặc hoạt động em muốn quay về' in help_text,['g02-ho-tro-khi-can','on-nen','sua-loi','nen-quay-ve']),
        'DH14':(all(t in help_text.casefold() for t in ['đã xem đáp án','không còn nhiệm vụ mới phù hợp','không tính là bằng chứng độc lập mới','không tự đánh dấu đã đạt']),['g02-ho-tro-khi-can','cp-lt1','cp-kt'])}
    return {k:{'passed':bool(ok) and all(root.find(id=i) for i in ids),'source_targets':ids} for k,(ok,ids) in rules.items()}


def browser_checks(page, output):
    checks = {}; diagnostics = {}
    output.mkdir(parents=True,exist_ok=True)
    with socket.socket() as probe:
        probe.bind(('127.0.0.1',0)); port=probe.getsockname()[1]
    with tempfile.TemporaryDirectory(prefix='browser_',dir=output,ignore_cleanup_errors=True) as profile:
        proc=subprocess.Popen([edge_executable(),'--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check',
            f'--remote-debugging-port={port}','--remote-debugging-address=127.0.0.1','--remote-allow-origins=http://localhost',
            '--user-data-dir='+profile,'about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,
            creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        b=None
        try:
            endpoint=f'http://127.0.0.1:{port}'
            for _ in range(100):
                try:
                    if requests.get(endpoint+'/json/version',timeout=.3).ok:break
                except requests.RequestException:pass
                time.sleep(.1)
            tab=requests.put(endpoint+'/json/new?about:blank',timeout=10).json()
            b=Browser(tab['webSocketDebuggerUrl']); b.call('Page.enable'); b.call('Runtime.enable')
            # A download card has its own copy cell, not the reading-paper axis.
            # Keep orphan/overflow checks on it; check its three-column layout below.
            geometry=GEOMETRY.replace('visible=n=>',"visible=n=>!n.closest('.support-region')&&").replace("n.matches('h2,h3,h4,h5,.role,summary')", "n.matches('h2,h3,h4,h5,.role,summary')&&!n.closest('.zo-pdf-card')")
            for width in [1440,430,390,320]:
                b.viewport(width,960 if width>500 else 844)
                for view in VIEWS:
                    b.navigate(page.as_uri()+'?r1-view='+view)
                    actual=b.evaluate(geometry)
                    if width == 1440 and (actual['orphan'] or actual['axes'] or not actual['loaded']):
                        diagnostics[view] = actual
                        diagnostics[view]['failed_images'] = b.evaluate('[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src)')
                    for key in ['orphan','overflow','axes']:
                        checks[f'{width}/{view}/{key}']=actual[key]==[]
                    for key in ['fits','white','widths','gaps','loaded']:
                        checks[f'{width}/{view}/{key}']=actual[key]
                    checks[f'{width}/{view}/no nested reading regions']=actual['nested']==0
                    checks[f'{width}/{view}/default closed']=b.evaluate('document.querySelectorAll("details[open]").length')==0
                b.navigate(page.as_uri()+'?r1-view=tai-pdf#tai-tai-lieu')
                cards=b.evaluate("""[...document.querySelectorAll('.zo-pdf-card')].map(c=>{const r=c.getBoundingClientRect(),a=c.querySelector('a').getBoundingClientRect(),p=c.querySelector('.zo-pdf-copy').getBoundingClientRect(),m=c.querySelector('.zo-pdf-pages').getBoundingClientRect(),t=c.querySelector('.zo-pdf-title').getBoundingClientRect(),d=c.querySelector('.zo-pdf-description').getBoundingClientRect();return Math.abs(t.left-p.left)<1.3&&Math.abs(d.left-p.left)<1.3&&a.height>=44&&[a,p,m].every(x=>x.left>=r.left&&x.right<=r.right+1)&&(innerWidth>600?(m.left>=p.right&&a.left>=m.right):(p.bottom<=m.top+1&&p.bottom<=a.top+1))})""")
                checks[f'{width}/PDF own column axes and targets']=len(cards)==8 and all(cards)
                for anchor in ['cách-học-với-tài-liệu-này','g02-ho-tro-khi-can','g02-chuyen-goi','g02-khoi-dong-01','lg-g02-khoi-dong-01','nen-n-dh-03-xn01']:
                    b.navigate(page.as_uri()+'#'+anchor)
                    checks[f'{width}/{anchor}/target visible']=b.evaluate('!!document.getElementById('+json.dumps(anchor)+').getClientRects().length')
                if width in [1440,390]:
                    b.navigate(page.as_uri()+'?r1-view=bat-dau')
                    b.screenshot(output/f'bat-dau-{width}.png')
                    b.navigate(page.as_uri()+'?r1-view=bai-hoc#bắt-đầu-từ-đâu')
                    b.screenshot(output/f'khoi-dong-{width}.png')
                    for caller,dest in [('bắt-đầu-từ-đâu','nen-n-txd-01'),('cp-lt1','nen-n-dh-01'),('cp-kt','on-nen')]:
                        b.navigate(page.as_uri()+'#'+caller)
                        b.click('#'+caller+' a[href="#'+dest+'"]')
                        checks[f'{width}/{caller}/support captures caller']=b.evaluate('new URL(location.href).searchParams.get("r1-return")')==caller
                        b.call('Page.reload');b.ready();b.click('.r1-return-link')
                        checks[f'{width}/{caller}/reload returns caller']=unquote(b.evaluate('location.hash'))=='#'+caller
                    b.navigate(page.as_uri()+'#o02')
                    b.click('#o02 a[href="#loi-giai-on-lai-02"]')
                    checks[f'{width}/review answer opens correct answer']=b.evaluate('document.getElementById("loi-giai-on-lai-02").open')
                    b.click('#loi-giai-on-lai-02 .answer-link a')
                    checks[f'{width}/review answer back to actual task']=b.evaluate('location.hash')=='#o02'
                    b.navigate(page.as_uri()+'#nen-n-dh-03')
                    checks[f'{width}/direct foundation manual return']=b.evaluate('document.querySelectorAll(".r1-return-link").length')>=3
                    b.navigate(page.as_uri()+'?r1-view=on-nen')
                    b.click('#nen-n-dh-03 summary')
                    b.screenshot(output/f'on-nen-{width}.png')
            b.call('Emulation.setScriptExecutionDisabled',{'value':True})
            b.navigate(page.as_uri())
            checks['no JS all tasks remain present']=b.evaluate('document.querySelectorAll("[data-zo-type=task]").length')==64
            checks['no JS independent foundation source owner']=b.evaluate('!document.getElementById("on-nen").parentElement.closest("section")')
            b.call('Emulation.setScriptExecutionDisabled',{'value':False})
        finally:
            if b:
                try:b.call('Browser.close')
                except (OSError,RuntimeError):pass
                b.ws.close()
            if proc.poll() is None:proc.terminate()
            try:proc.wait(timeout=10)
            except subprocess.TimeoutExpired:proc.kill();proc.wait()
    (output/'diagnostics.json').write_text(json.dumps(diagnostics,ensure_ascii=False,indent=2),encoding='utf-8')
    return checks


def build(raw, output):
    from zo_web_2027_g02 import build as build_layout
    from zo_web_2027_g02_payloads import apply as apply_payloads
    data=json.loads(BINDING.read_text(encoding='utf-8'));validate_binding(data)
    build_layout(output,raw)
    import shutil
    figures=output/'assets/figures04';figures.mkdir(parents=True,exist_ok=True)
    for filename in ['cover-light.svg','do_thi_01.svg','do_thi_02.svg','nen_do_thi_01.svg','nen_do_thi_02.svg']:
        source=PACKAGE/'giao_dien/assets/figures_0_4'/filename
        if filename in ['do_thi_01.svg','do_thi_02.svg']:
            source=output.parent/'figure-build'/filename
        if not source.is_file():raise ValueError('Missing current 0.4 graph; build from canonical TeX into audit figure-build: '+filename)
        shutil.copyfile(source,figures/filename)
    payloads=apply_payloads(output/'g02-reading.html',output)
    page=read(output/'g02-reading.html')
    apply_labels(page,BINDING)
    from zo_web_2027_g02_production import align_reading_roles
    align_reading_roles(page)
    (output/'g02-reading.html').write_text(str(page),encoding='utf-8')
    manifest=json.loads((output/'g02-manifest.json').read_text(encoding='utf-8'))
    manifest.update(output_sha256=sha(output/'g02-reading.html'),semantic_binding_sha256=sha(BINDING),
        semantic_mapper_sha256=sha(ROOT/'scripts/zo_r1_g01_labels.py'),payloads=payloads,
        label_state='source_applied_pending_html_acceptance')
    (output/'g02-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def check(page, raw, before, output, browser=False):
    data=json.loads(BINDING.read_text(encoding='utf-8'));validate_binding(data)
    doc=read(page);root=doc.select_one('.reader-content');baseline=read(before).select_one('.zo-on-thi-package')
    current=read(raw).select_one('.zo-on-thi-package')
    checks=predicates(doc,data)
    situation_review=situations(doc)
    checks.update({k+' source targets/wording':v['passed'] for k,v in situation_review.items()})
    maths=lambda d:Counter(''.join(n.get_text().split()) for n in d.select('annotation'))
    checks['all old visible math expressions preserved']=maths(baseline)==maths(current)
    checks['semantic labels do not modify math']=maths(current)==Counter(''.join(n.get_text().split()) for n in root.select('annotation') if not n.find_parent('table',class_='zo-variation-native'))
    checks['all old IDs preserved']=set(n['id'] for n in baseline.select('[id]'))<=set(n['id'] for n in root.select('[id]'))
    for task in load_yaml(PACKAGE/'_quy_trinh/kien_truc_hoc_tap.yml')['tasks']:
        for key in ['source_anchor','answer_anchor']:
            anchor=task[key]
            checks[task['id']+'/'+key+'/math preserved']=maths(baseline.find(id=anchor))==maths(current.find(id=anchor))
    checks['two native BBT retained']=len(root.select('table.zo-variation-native'))==2
    checks['eight PDF cards with current warning']=len(root.select('.zo-pdf-card'))==8 and 'chưa được đồng bộ' in root.find(id='tai-tai-lieu').get_text()
    # Deliberate defects prove the gate detects the old failure classes.
    for name,mutate in [
        ('number reset',lambda d:d['units'][1].update(number=1)),
        ('wrong answer',lambda d:d['units'][0].update(answer=d['units'][1]['answer'])),
        ('wrong function',lambda d:d['units'][0].update(function='function.test'))]:
        fixture=copy.deepcopy(data);mutate(fixture)
        try:validate_binding(fixture);rejected=False
        except (AssertionError,KeyError):rejected=True
        checks['fixture/'+name+' rejected']=rejected
    for name,mutate in [
        ('foundation nested',lambda d:d.find(id='bai-hoc').append(d.find(id='on-nen').extract())),
        ('answer missing',lambda d:d.find(id=data['units'][0]['answer']).decompose()),
        ('disclosure open',lambda d:d.find('details').attrs.update(open='')),
        ('stage overview missing',lambda d:d.find(id='r1-g02-table-t11').decompose()),
        ('guide map split',lambda d:d.find(id='cách-học-với-tài-liệu-này').append(d.new_tag('div',attrs={'class':'reading-region'}))),
        ('old test condition',lambda d:d.find(id='tu-kiem-tra').append('Chỉ thử Kiểm tra trực tiếp khi đã có bài làm độc lập'))]:
        fixture=copy.deepcopy(doc);mutate(fixture)
        checks['fixture/'+name+' rejected']=not all(predicates(fixture,data).values())
    files,placements,lines=read_sources(PACKAGE/'index.qmd')
    source_text=PACKAGE.joinpath('index.qmd').read_text(encoding='utf-8')
    inventory={'package':'R1-G02','decision':'QD_025','status':data['status'],'units':data['units'],
        'checkpoints':data['checkpoints'],'includes':placements,'source_hashes':files,
        'headings':[{'path':line['path'],'line':line['line'],'text':line['text']} for line in lines if re.match(r'^#{2,6} ',line['text'])],
        'source_ids':[{'id':n['id'],'element':n.name} for n in current.select('[id]')],
        'references':[{'href':n['href'],'text':n.get_text(' ',strip=True)} for n in current.select('a[href]')],
        'images':[{'src':n.get('src'),'alt':n.get('alt')} for n in current.select('img')],
        'tables':[{'id':n.get('id'),'rows':len(n.select('tr')),'headers':[h.get_text(' ',strip=True) for h in n.select('th')]} for n in current.select('table')],
        'knowledge_units':data['knowledge_units'],
        'reading_regions':[{'ids':[n['id'] for n in paper.select('[id]')], 'label':paper.select_one('[data-reading-label]').get_text(' ',strip=True) if paper.select_one('[data-reading-label]') else None, 'reason':paper.get('data-reading-reason')} for paper in root.select('.reading-region')],
        'limits':'Source/task mapping, not a new mathematical acceptance or G01 quota.'}
    if browser:checks.update(browser_checks(page,output/'images'))
    files.update({p.relative_to(ROOT).as_posix():sha(p) for p in [
        BINDING,PACKAGE/'giao_dien/web_2027_layout.json',PACKAGE/'giao_dien/support-context.js',
        PACKAGE/'_quy_trinh/kien_truc_hoc_tap.yml',Path(__file__).resolve(),
        ROOT/'scripts/zo_r1_g01_labels.py',ROOT/'scripts/zo_web_2027_g02.py',COMMON_CATALOG]})
    files.update({p.relative_to(ROOT).as_posix():sha(p) for p in [ROOT/'scripts/zo_web_2027_g02_production.py',
        ROOT/'scripts/zo_web_2027_g02_payloads.py',ROOT/'scripts/zo_web_2027_g02_sync_check.py',
        ROOT/'scripts/zo_web_2027_production.py',ROOT/'_design/web_2027_mau_dung_chung/r1-g02-adapter.css',
        PACKAGE/'cong_cu/r1_g02.lua']})
    failures=[k for k,v in checks.items() if not v]
    report={'package':'R1-G02','checks':checks,'situation_review':situation_review,'failures':failures,'passed':len(checks)-len(failures),
        'total':len(checks),'source_hashes':files,'html_sha256':sha(page),
        'scope':'Source, labels, task pairs, preserved math/IDs, 14-situation source targets and representative runtime',
        'limits':['Not owner HTML acceptance','No PDF build or promotion','No publication',
                  'Not independent mathematical peer review of whole package','No Safari/Firefox/touch device/screen reader acceptance']}
    output.mkdir(parents=True,exist_ok=True)
    for name,data in [('qa.json',report),('inventory.json',inventory)]:
        (output/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['passed','total','failures']},ensure_ascii=False))
    return int(bool(failures))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['build','check'])
    parser.add_argument('--raw',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--before',type=Path);parser.add_argument('--page',type=Path);parser.add_argument('--browser',action='store_true')
    args=parser.parse_args();args.output=args.output.resolve();args.raw=args.raw.resolve()
    if not args.output.is_relative_to(ROOT/'_audit') or not args.raw.is_relative_to(ROOT/'_audit'):
        raise ValueError('Isolated audit input/output only')
    if args.command=='build':
        build(args.raw,args.output);return 0
    if not args.before or not args.page:parser.error('check requires --before and --page')
    return check(args.page.resolve(),args.raw,args.before.resolve(),args.output,args.browser)


if __name__=='__main__':
    raise SystemExit(main())


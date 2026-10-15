"""QD_033 scoped regression: checkpoint wording and contextual lesson return.

Read only canonical sources and explicit preview pages. Never render, accept,
publish, or change a historical receipt. Browser uses a disposable test profile.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import socket
import subprocess
import tempfile
import time
from urllib.parse import unquote, urlsplit

import requests
from bs4 import BeautifulSoup
import yaml
from zo_web_2027_check import Browser, edge_executable
import zo_web_2027_backlog_check as backlog
import zo_r1_g01_labels_check as g01_labels
import zo_r1_g02_labels_check as g02_labels
from zo_r1_g01_editorial_check import semantic as g01_semantic

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'content/thpt/on_thi_toan_thpt'
CHECKPOINTS = {'g01': ['cp-kt', 'cp-on1', 'cp-on2', 'cp-on3'],
               'g02': ['cp-lt1', 'cp-lt2', 'cp-lt3', 'cp-p', 'cp-kt',
                       'cp-on1', 'cp-on2', 'cp-on3']}
ROUTES = {
    'g01': [('cp-lt2', 'có-thể-đọc-ngược-đến-đâu'), ('cp-lt3', 'bai-hoc')],
    'g02': [('g02-c1', 'doi-tuong'), ('g02-c1', 'dinh-nghia'),
            ('g02-c1', 'tren-doan'), ('g02-c2', 'tap-khac'),
            ('g02-c3', 'loi-van'), ('cp-p', 'tren-doan'),
            ('cp-on2', 'tren-doan'), ('cp-on3', 'tren-doan')]}


class RouteBrowser(Browser):
    def ready(self):
        # decode() can remain pending for an image in a view hidden by routing.
        # Check actual load completion instead; missing images still fail QA.
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            state = self.evaluate("""(() => {
                for (const i of document.images) i.loading='eager';
                return {complete:document.readyState==='complete',
                    fonts:document.fonts.status==='loaded',
                    missing:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src)};
            })()""")
            if state['complete'] and state['fonts'] and not state['missing']:
                time.sleep(.1)
                return
            time.sleep(.1)
        raise TimeoutError('Page resources did not load: ' + json.dumps(state))


def wording(doc, key):
    checks = {}
    for ident in CHECKPOINTS[key]:
        node = doc.find(id=ident)
        journal = node.find('a', href='#nhat-ky') if node else None
        # The condition must be in the actual instruction, not elsewhere on page.
        sentence = journal.parent.get_text(' ', strip=True) if journal else ''
        checks[ident + ' journal is contextual'] = bool(journal and
            'khi cần lưu quyết định, nơi tiếp tục hoặc kết thúc buổi học' in sentence)
    if key == 'g02':
        cp = doc.find(id='cp-kt')
        items = cp.select('ol > li') if cp else []
        checks['ended test repairs only observed errors'] = len(items) >= 6 and (
            items[3].get_text(' ', strip=True).startswith('Nếu phát hiện lỗi,') and
            items[4].get_text(' ', strip=True).startswith('Khi cần xác nhận sau sửa,') and
            'Nếu đã đủ tiêu chí, giữ kết quả' in cp.get_text(' ', strip=True))
        node = doc.find(id='cp-on3')
        checks['review 3 repair only if needed'] = bool(node and
            'Nếu có lỗi, dùng Sửa lỗi sau Ôn lại' in node.get_text(' ', strip=True))
    return checks


def home_wording(doc):
    method = doc.find(id='học-theo-cách-nào')
    text = method.get_text(' ', strip=True) if method else ''
    return {'Home ends attempt before help and separates later work': all(
        phrase in text for phrase in ['kết thúc lượt Kiểm tra', 'giữ riêng bài đã tự làm',
                                     'không tính vào kết quả tự lực của lượt ấy']),
            'Home retains self-reliance and single session': all(
        phrase in text for phrase in ['không xem lời giải hay tìm trợ giúp trong lúc làm',
                                     'Không chia bài Kiểm tra thành nhiều buổi'])}


def browser_checks(preview, output, check):
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0)); port = sock.getsockname()[1]
    endpoint = f'http://127.0.0.1:{port}'
    with tempfile.TemporaryDirectory(prefix='_tmp_route_browser_', dir=output) as profile:
        proc = subprocess.Popen([edge_executable(), '--headless=new', '--disable-gpu',
            '--no-first-run', '--no-default-browser-check',
            '--remote-debugging-address=127.0.0.1', f'--remote-debugging-port={port}',
            '--remote-allow-origins=http://localhost', '--user-data-dir='+profile,
            'about:blank'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        connections = []
        try:
            for _ in range(100):
                try:
                    if requests.get(endpoint+'/json/version', timeout=.3).ok: break
                except requests.RequestException: pass
                time.sleep(.1)
            else: raise TimeoutError('Test browser did not start')
            def new_tab():
                target = requests.put(endpoint+'/json/new?about:blank', timeout=10).json()
                b = RouteBrowser(target['webSocketDebuggerUrl']); connections.append(b)
                b.ws.settimeout(60)
                return b
            b = new_tab()
            state = """(() => {const p=new URLSearchParams(location.search),n=document.querySelector('.r1-support-return');return {caller:p.get('r1-return'),context:p.get('r1-context'),hash:decodeURIComponent(location.hash.slice(1)),visible:!!n&&!n.hidden,returnHref:n?.querySelector('a')?.getAttribute('href'),view:document.querySelector('[data-r1-view]')?.dataset.r1View,overflow:document.documentElement.scrollWidth>innerWidth+1}})()"""
            for width in [1440, 430, 390]:
                b.viewport(width, 850)
                for key, routes in ROUTES.items():
                    page = (preview/(key+'-reading.html')).as_uri()
                    for caller, target in routes:
                        print(f'Checking {width}/{key}/{caller}/{target}', flush=True)
                        view = 'on-lai' if caller.startswith('cp-on') else 'luyen-tap'
                        b.navigate(page+f'?r1-view={view}#{caller}')
                        selector = f'[id="{caller}"] a[href="#{target}"]'
                        b.click(selector)
                        result = b.evaluate(state)
                        prefix = f'{width}/{key}/{caller}/{target}/'
                        check(prefix+'retains actual caller', result['caller'] == caller and result['context'] == caller)
                        check(prefix+'lesson target and return visible', result['hash'] == target and result['visible'])
                        check(prefix+'no page overflow', not result['overflow'])
                        if not result['visible']: continue  # Legacy failure recorded, no fabricated return click.
                        supported_url = b.evaluate('location.href')
                        b.call('Page.reload'); b.ready()
                        check(prefix+'reload keeps caller', b.evaluate(state)['caller'] == caller)
                        b.click('.r1-support-return a')
                        returned = b.evaluate(state)
                        check(prefix+'return reaches caller and clears context', returned['hash'] == caller and returned['caller'] is None and not returned['visible'])
                        b.evaluate('history.back()'); time.sleep(.2)
                        check(prefix+'Back restores support context', b.evaluate(state)['caller'] == caller and b.evaluate(state)['visible'])
                        if width == 1440 and (caller, target) in [('cp-lt2', 'có-thể-đọc-ngược-đến-đâu'), ('cp-on2', 'tren-doan')]:
                            b.screenshot(output/f'{key}-lesson-return.png')
                            peer = new_tab(); peer.viewport(width, 850)
                            peer.navigate(page+'?r1-view=on-lai#cp-on3')
                            check(prefix+'another tab cannot overwrite caller', b.evaluate(state)['caller'] == caller)
                            peer.navigate(supported_url)
                            check(prefix+'copied URL retains caller in new tab', peer.evaluate(state)['caller'] == caller and peer.evaluate(state)['visible'])
                    b.navigate(page+'?r1-view=bai-hoc#bai-hoc')
                    check(f'{width}/{key}/direct lesson is not a support call', not b.evaluate(state)['visible'] and b.evaluate(state)['caller'] is None)
                    caller, target = routes[0]
                    b.navigate(page+f'?r1-view=luyen-tap#{caller}')
                    b.click(f'[id="{caller}"] a[href="#{target}"]')
                    b.click('#r1-tab-bai-hoc')
                    check(f'{width}/{key}/fresh Lesson tab clears earlier support context', not b.evaluate(state)['visible'] and b.evaluate(state)['caller'] is None)
                    b.navigate(page+'?r1-view=bai-hoc&r1-return=cp-lt2&r1-context=cp-lt2#bắt-đầu-từ-đâu')
                    b.click('[id="bắt-đầu-từ-đâu"] a[href="#nen-n-txd-01"]')
                    check(f'{width}/{key}/nested warmup foundation retains original activity', b.evaluate(state)['caller']=='cp-lt2' and b.evaluate(state)['visible'])
                    b.navigate(page+'?r1-view=bai-hoc#bắt-đầu-từ-đâu')
                    b.click('[id="bắt-đầu-từ-đâu"] a[href="#nen-n-txd-01"]')
                    check(f'{width}/{key}/ordinary warmup foundation retains warmup caller', b.evaluate(state)['caller']=='bắt-đầu-từ-đâu' and b.evaluate(state)['visible'])
                    b.navigate(page+'?r1-view=on-nen#nen-n-txd-01')
                    check(f'{width}/{key}/direct foundation offers lesson and warmup', b.evaluate("!!document.querySelector('.r1-support-return a[href*=bai-hoc]') && [...document.querySelectorAll('.r1-support-return a')].some(a=>a.textContent==='Khởi động')"))
                    b.call('Emulation.setScriptExecutionDisabled', {'value': True})
                    b.navigate(page)
                    check(f'{width}/{key}/noJS content and native lesson links', b.evaluate("document.querySelector('#bai-hoc').getBoundingClientRect().height>0 && !!document.querySelector('[id=cp-lt2] a[href]')"))
                    b.call('Emulation.setScriptExecutionDisabled', {'value': False})
                print('QD_033 routes checked:', width, flush=True)
        finally:
            for browser in connections:
                browser.ws.close()
            proc.terminate()
            try: proc.wait(timeout=10)
            except subprocess.TimeoutExpired: proc.kill(); proc.wait(timeout=10)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--browser', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(ROOT/'_audit') or output.exists():
        parser.error('Use a new named evidence directory under _audit')
    output.mkdir(parents=True)
    values = {}
    def check(name, value):
        values[name] = bool(value)
        if not value: print('FAIL', name, flush=True)
    docs = {key: BeautifulSoup((args.preview/(key+'-reading.html')).read_text(encoding='utf-8'), 'html.parser') for key in ['home','d0','g01','g02']}
    for key in CHECKPOINTS:
        package = BASE/'hoc_lieu'/('r1_'+key)
        binding = json.loads((package/'giao_dien/he_nhan.json').read_text(encoding='utf-8'))
        for name, value in backlog.require_source(package/'index.qmd', binding).items():
            check(key+'/source/'+name, value)
        for name, value in backlog.require(docs[key], binding).items():
            check(key+'/ownership/'+name, value)
        labels = g01_labels if key == 'g01' else g02_labels
        for name, value in labels.predicates(docs[key], binding).items():
            check(key+'/labels/'+name, value)
        for name, result in labels.situations(docs[key]).items():
            check(key+'/situation/'+name, result['passed'])
        if key == 'g01':
            manifest = yaml.safe_load((package/'_quy_trinh/kien_truc_hoc_tap.yml').read_text(encoding='utf-8'))
            for name, value in g01_semantic(docs[key], manifest).items():
                check(key+'/editorial/'+name, value)
        for name, value in wording(docs[key], key).items(): check(key+'/'+name, value)
        # Replace the checkpoint instruction, not the unrelated Cách học paragraph.
        mutated = copy.deepcopy(docs[key]); node = mutated.find(id='cp-kt').find('a', href='#nhat-ky')
        parent = node.parent; parent.clear()
        link = mutated.new_tag('a', href='#nhat-ky'); link.string = 'Ghi Nhật kí'; parent.append(link)
        check(key+'/negative compulsory journal rejected', not wording(mutated,key)['cp-kt journal is contextual'])
    for name, value in home_wording(docs['home']).items(): check(name, value)
    mutated = copy.deepcopy(docs['home']); mutated.find(id='học-theo-cách-nào').clear()
    check('negative missing test exception rejected', not all(home_wording(mutated).values()))
    mutated = copy.deepcopy(docs['g02']); items = mutated.find(id='cp-kt').select('ol > li'); items[3].clear(); items[3].string='Chọn đúng nhiệm vụ để sửa.'
    check('negative unconditional repair rejected', not wording(mutated,'g02')['ended test repairs only observed errors'])
    # All local links, including D0's separate question/answer regions.
    missing = []; cache = {}
    for key, doc in docs.items():
        page = (args.preview/(key+'-reading.html')).resolve()
        for link in doc.select('a[href],img[src],script[src],link[href]'):
            href = link.get('src', link.get('href', '')); url = urlsplit(href)
            if url.scheme or url.netloc: continue
            dest = (page.parent/unquote(url.path)).resolve() if url.path else page
            if not dest.is_file(): missing.append([key,href]); continue
            if url.fragment and dest.suffix == '.html':
                if dest not in cache: cache[dest] = BeautifulSoup(dest.read_text(encoding='utf-8'),'html.parser')
                if not cache[dest].find(id=unquote(url.fragment)): missing.append([key,href])
        ids = [n['id'] for n in doc.select('[id]')]
        check(key+'/unique IDs', len(ids) == len(set(ids)))
    check('four pages local files and fragments resolve', not missing)
    browser_error = None
    if args.browser:
        try:
            browser_checks(args.preview.resolve(), output, check)
        except Exception as exc:
            browser_error = f'{type(exc).__name__}: {exc}'
            check('browser completed without harness error', False)
    failures = [key for key,value in values.items() if not value]
    report = {'decision':'QD_033','checks':values,'passed':len(values)-len(failures),
        'total':len(values),'failures':failures,'missing':missing,'browser':args.browser,
        'browser_error':browser_error,
        'html_sha256':{key:hashlib.sha256((args.preview/(key+'-reading.html')).read_bytes()).hexdigest() for key in docs},
        'owner_acceptance':'pending','published':False,
        'limits':['Scoped A01-A04 regression, not a full mathematics or learner-comprehension audit', 'Edge headless, not real devices or Safari/Firefox']}
    (output/'qa.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['passed','total','failures']},ensure_ascii=False))
    return int(bool(failures))


if __name__ == '__main__':
    raise SystemExit(main())

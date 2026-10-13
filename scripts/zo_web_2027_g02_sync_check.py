"""Role-based G01/G02 parity and a local-only navigation projection."""
import argparse
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile
import time
from urllib.parse import unquote, urlsplit, urlunsplit
import requests
from bs4 import BeautifulSoup
from zo_web_2027_preview import REPO, sha
from zo_web_2027_check import Browser, edge_executable


def preview(page, out, home):
    doc = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
    site = page.parents[5]
    runtime = site / 'assets/zo_web_2027/g02'
    out.mkdir(parents=True, exist_ok=True)
    shutil.copytree(runtime, out / 'runtime', dirs_exist_ok=True)
    records = []
    for node in doc.select('[src],link[href],a[href]'):
        key = 'src' if node.has_attr('src') else 'href'
        url = urlsplit(node[key])
        if url.scheme or url.netloc or not url.path:
            continue
        original = (page.parent / unquote(url.path)).resolve()
        if original.is_relative_to(runtime):
            target = out / 'runtime' / original.relative_to(runtime)
        elif original == page.resolve():
            target = out / 'g02-reading.html'
        elif original == site / 'content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.html':
            target = home
        elif original.is_file():
            target = original
        else:
            target = REPO / 'docs' / original.relative_to(site)
        if not target.is_file() and target != out / 'g02-reading.html':
            raise ValueError('Missing preview destination: ' + str(target))
        node[key] = urlunsplit(('', '', os.path.relpath(target, out).replace('\\', '/'), url.query, url.fragment))
        records.append({'canonical': original.relative_to(site).as_posix(), 'preview': node[key]})
    destination = out / 'g02-reading.html'
    destination.write_text(str(doc), encoding='utf-8')
    (out / 'projection.json').write_text(json.dumps({'canonical_sha256': sha(page),
        'preview_sha256': sha(destination), 'links': records, 'mapping_only': True}, ensure_ascii=False, indent=2), encoding='utf-8')
    return destination


def parity(g01, g02, out):
    checks = {}; measurements = {}
    out.mkdir(parents=True, exist_ok=True)
    with socket.socket() as probe:
        probe.bind(('127.0.0.1', 0)); port = probe.getsockname()[1]
    with tempfile.TemporaryDirectory(prefix='edge_', dir=out, ignore_cleanup_errors=True) as profile:
        proc = subprocess.Popen([edge_executable(), '--headless=new', '--disable-gpu', '--no-first-run',
            '--no-default-browser-check', f'--remote-debugging-port={port}', '--remote-debugging-address=127.0.0.1',
            '--remote-allow-origins=http://localhost', '--user-data-dir=' + profile, 'about:blank'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        browser = None
        try:
            endpoint = f'http://127.0.0.1:{port}'
            for _ in range(100):
                try:
                    if requests.get(endpoint + '/json/version', timeout=.3).ok: break
                except requests.RequestException: pass
                time.sleep(.1)
            tab = requests.put(endpoint + '/json/new?about:blank', timeout=10).json()
            browser = Browser(tab['webSocketDebuggerUrl']); browser.call('Page.enable'); browser.call('Runtime.enable')
            script = """(() => {
              const styles = selector => {const n=document.querySelector(selector);if(!n)return null;const s=getComputedStyle(n);return Object.fromEntries(['fontFamily','fontSize','fontWeight','lineHeight','color','textAlign'].map(k=>[k,s[k]]))};
              const paper=[...document.querySelectorAll('.reading-region')].find(n=>n.getClientRects().length&&!n.closest('[hidden]'));
              const s=paper&&getComputedStyle(paper);
              return {paper:paper?{width:paper.getBoundingClientRect().width,padding:s.padding,background:s.backgroundColor}:null,
                h2:styles('.reader-content h2'),h3:styles('.reader-content h3'),h4:styles('.reader-content h4'),
                role:styles('.reader-content .role'),body:styles('.reader-content p'),
                tableHeader:styles('.reader-content .r1-table th'),
                repairHeader:styles('#r1-table-t12 th,#r1-g02-table-t04 th'),
                journalHeader:styles('#r1-table-t13 th'),
                warmupTitle:styles('[data-zo-type="task"][data-zo-function="function.warmup"] .r1-task-label'),
                selfCheckTitle:styles('[data-zo-type="task"][data-zo-function="function.self_check"] .r1-task-label')};
            })()"""
            for width in [1440, 390, 320]:
                browser.viewport(width, 960 if width > 500 else 844)
                for view in ['bat-dau','bai-hoc','luyen-tap','kiem-tra','on-lai','on-nen','sua-loi','nhat-ky','loi-giai','nguon','tai-tai-lieu']:
                    pair = []
                    for name, page in [('g01',g01),('g02',g02)]:
                        browser.navigate(page.as_uri() + '?r1-view=' + view)
                        pair.append(browser.evaluate(script))
                        if name == 'g02' and view in ['bat-dau','luyen-tap','on-nen','loi-giai','nguon']:
                            browser.screenshot(out / f'{view}-{width}.png')
                        if name == 'g02' and view == 'bat-dau':
                            browser.evaluate("document.getElementById('cách-học-với-tài-liệu-này').scrollIntoView()")
                            browser.screenshot(out / f'cach-hoc-{width}.png')
                    measurements[f'{width}/{view}'] = pair
                    for role in ['paper','h2','h3','h4','role','body','tableHeader','repairHeader','journalHeader','warmupTitle','selfCheckTitle']:
                        # Absence of a mathematical element is not a formatting mismatch.
                        if role in ['warmupTitle','selfCheckTitle']:
                            checks[f'{width}/{view}/{role} same computed style'] = pair[0][role] is not None and pair[0][role] == pair[1][role]
                        elif pair[0][role] is not None and pair[1][role] is not None:
                            checks[f'{width}/{view}/{role} same computed style'] = pair[0][role] == pair[1][role]
            # Shared download cards have their own scoped typography and columns.
        finally:
            if browser:
                try: browser.ws.close()
                except Exception: pass
            proc.terminate()
            try: proc.wait(timeout=10)
            except subprocess.TimeoutExpired: proc.kill(); proc.wait()
    failures = [k for k,v in checks.items() if not v]
    report = {'checks':checks,'measurements':measurements,'passed':len(checks)-len(failures),
        'total':len(checks),'failures':failures,'g01_sha256':sha(g01),'g02_sha256':sha(g02),
        'limits':'Formatting parity, not equal mathematical content/counts or owner acceptance'}
    (out / 'pair.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['passed','total','failures']},ensure_ascii=False))
    return int(bool(failures))


def protected_report(out):
    before=json.loads((out/'before.json').read_text(encoding='utf-8'))
    allowed={
        'content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/'+name
        for name in ['03_dieu_hanh_chuong_trinh.md','08_danh_muc_tham_quyen_dieu_hanh.md','hop_dong_dieu_hanh.json','goi/R1_G02.md']}
    changed=[p for p,h in before.items() if not (REPO/p).is_file() or sha(REPO/p)!=h]
    forbidden=[p for p in changed if p not in allowed]
    package=REPO/'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01'
    g01={name:sha(package/name)==sha(out/snapshot) for name,snapshot in [
        ('index.qmd','r1_g01-before.qmd'),('giao_dien/web_2027_layout.json','g01-layout-before.json'),
        ('giao_dien/web_2027_accepted.json','g01-accepted-before.json')]}
    record={'protected_files':len(before),'intended_operating_document_updates':[p for p in changed if p in allowed],
        'unexpected':forbidden,'g01_source_layout_receipt_unchanged':g01,
        'guard_rejects_index_or_docs_change':'.git/index' not in allowed and not any(p.startswith('docs/') for p in allowed),
        'passed':not forbidden and all(g01.values()),'published':False,'learning_pdf_built':False}
    (out/'protected-final.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(record,ensure_ascii=False))
    return int(not record['passed'])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['preview','parity','protected']);p.add_argument('--g02',type=Path)
    p.add_argument('--g01',type=Path);p.add_argument('--home',type=Path);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();args.output=args.output.resolve()
    if not args.output.is_relative_to(REPO/'_audit'):
        raise ValueError('Isolated audit input/output only')
    if args.command=='protected':return protected_report(args.output)
    if not args.g02:p.error('preview/parity requires --g02')
    args.g02=args.g02.resolve()
    if not args.g02.is_relative_to(REPO/'_audit'):raise ValueError('Isolated audit input only')
    if args.command=='preview':
        if not args.home:p.error('preview requires --home')
        print(preview(args.g02,args.output,args.home.resolve()));return 0
    if not args.g01:p.error('parity requires --g01')
    return parity(args.g01.resolve(),args.g02,args.output)


if __name__=='__main__':raise SystemExit(main())

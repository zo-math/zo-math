"""Rebuild/check canonical course Home in an isolated tree; never publish.

The rendered Home is generated from current QMD/data, not an old preview.
Preview navigation alone may target explicit existing package HTML candidates.
"""
from __future__ import annotations
import argparse
import copy
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from urllib.parse import unquote, urlsplit, urlunsplit

sys.dont_write_bytecode = True
from bs4 import BeautifulSoup
import requests
from zo_web_2027_home import HOME, MARKER
from zo_web_2027_preview import REPO, KIT, BRAND_THOUGHT, sha, inventory, projection, footer_data
from zo_web_2027_check import Browser, GEOMETRY, edge_executable, complete_site_footer
from zo_build_on_thi import outputs, load_yaml, DATA_PATH, package_from_ref, validate_data


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')


def rebuild(out, target=HOME, report_env='ZO_WEB_2027_HOME_REPORT', configured=False):
    mirror=out/'source-render'
    if mirror.exists(): raise ValueError('Use a new rebuild directory; never overwrite historical evidence')
    skip=shutil.ignore_patterns('__pycache__','.quarto','.ipynb_checkpoints','*_cache','*_files')
    for name in ['scripts','assets','quy_trinh_xay_dung','projects','_projects','figures','images',
                 'content/thpt/on_thi_toan_thpt','content/support','_design/web_2027_mau_dung_chung',
                 '_design/ngon_ngu_thiet_ke_zo_math_0_4/07_mau_thi_giac']:
        src=REPO/name
        if src.is_dir():shutil.copytree(src,mirror/name,ignore=skip)
    for src in REPO.iterdir():
        if src.is_file() and (src.suffix in {'.yml','.yaml','.qmd','.md','.scss','.json','.toml'} or src.name in {'CNAME','.gitattributes','.gitignore'}):
            shutil.copyfile(src,mirror/src.name)
    for folder in ['content','content/thpt']:
        for src in (REPO/folder).glob('*'):
            if src.is_file() and (folder=='content' or src.name.startswith('_metadata')):
                (mirror/folder).mkdir(parents=True,exist_ok=True);shutil.copyfile(src,mirror/folder/src.name)
    isolated_index=mirror/'isolated.index';shutil.copyfile(REPO/'.git/index',isolated_index)
    env=dict(os.environ,GIT_DIR=str(REPO/'.git'),GIT_WORK_TREE=str(mirror),GIT_INDEX_FILE=str(isolated_index),
             **{report_env:str(mirror/'_audit/home-build.json')})
    command=['python','scripts/zo_python.py','scripts/zo_qmd.py' if configured else 'scripts/zo_quarto.py','render',
             str(target.with_suffix('.qmd'))]
    if not configured: command += ['--profile','on-thi-preview','--to','html']
    with (out/'render.log').open('w',encoding='utf-8') as log:
        code=subprocess.run(command,cwd=mirror,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
    if code:raise RuntimeError('Isolated Home render failed; see render.log')
    report=json.loads((mirror/'_audit/home-build.json').read_text(encoding='utf-8'))
    save(out/'build.json',report)
    print('Canonical HTML:',mirror/'docs'/target,flush=True)
    return mirror/'docs'/target


def preview(page,out,g01,g02):
    """Keep canonical output intact; build a separate local-navigation projection."""
    doc=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
    before=inventory(doc.select_one('.reader-content'))
    runtime=page.parents[5]/'assets/zo_web_2027/home'
    shutil.copytree(runtime,out/'runtime',dirs_exist_ok=True)
    mapping={'r1_g01':g01,'r1_g02':g02}
    for node in doc.select('img[src],link[href],script[src],a[href]'):
        key='src' if node.has_attr('src') else 'href'
        url=urlsplit(node[key])
        if url.scheme or url.netloc or not url.path:continue
        target=(page.parent/unquote(url.path)).resolve()
        if target.is_relative_to(runtime):
            destination=out/'runtime'/target.relative_to(runtime)
        elif target==page.resolve():destination=out/'home-reading.html'
        else:
            rel=target.relative_to(page.parents[5]).as_posix()
            destination=REPO/'docs'/rel
            for package,candidate in mapping.items():
                if '/hoc_lieu/'+package+'/index.html' in '/'+rel:destination=candidate
        if not destination.is_file() and destination.name!='home-reading.html':
            raise ValueError('Preview destination missing: '+str(destination))
        node[key]=urlunsplit(('', '',os.path.relpath(destination,out).replace('\\','/'),url.query,url.fragment))
    if inventory(doc.select_one('.reader-content'))!=before:raise ValueError('Preview mapping changed learner content')
    (out/'home-reading.html').write_text(str(doc),encoding='utf-8')
    save(out/'preview.json',{'canonical_html_sha256':sha(page),'preview_html_sha256':sha(out/'home-reading.html'),
                           'package_candidates':{k:{'path':str(v),'sha256':sha(v)} for k,v in mapping.items()},
                           'content_preserved':True,'mapping_only':True})
    return out/'home-reading.html'


def static(page,build):
    if build.get('layout') == 'editorial-home-2027':
        from zo_web_2027_home_landing_check import static as editorial_static
        return editorial_static(page, build)
    doc=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
    root=doc.select_one('.reader-content'); hero=doc.select_one('.hero')
    original=build['source_inventory']; actual=inventory(root)
    checks={
        'canonical marker':MARKER in doc.body.get('class',[]) and doc.body.get('data-zo-web-production')=='course-home',
        'text/order preserved':projection(hero)+' '+projection(root)==original['text'],
        'IDs preserved in order':[n['id'] for n in hero.select('[id]')]+actual['ids']==original['ids'],
        'heading roles preserved':actual['headings']==[tuple(n) for n in original['headings']],
        'math preserved':actual['math']==original['math'],
        'disclosure preserved':actual['disclosures']==[tuple(n) for n in original['disclosures']],
        'D0 G01 G02 order':[n['data-package-id'] for n in root.select('[data-package-id]')]==['d0','r1_g01','r1_g02'],
        'no package controller':not doc.select_one('script[src*="r1-controller"]'),
        'full brand':doc.select_one('.brand-thought').get_text(' ',strip=True)==BRAND_THOUGHT,
        'footer complete':complete_site_footer(doc,footer_data()),
        'six radio circles':len(doc.select('.appearance--inline input[type=radio][aria-label]'))==6,
        'grayscale retained':bool(doc.select_one('#grayscale[aria-label][aria-pressed]')),
        'controls no visible names':doc.select_one('.appearance').get_text(' ',strip=True)=='' and not doc.select_one('.appearance summary'),
        'icon drawer accessible':bool(doc.select_one('.mobile-trigger--icon[aria-label]')),
        'principles not sequential':bool(root.select_one('.zo-on-thi-steps ul')) and not root.select_one('.zo-on-thi-steps ol'),
        'no duplicate labels':all(not n.parent.select_one('h2,h3,h4') or n.get_text(' ',strip=True).casefold()!=n.parent.select_one('h2,h3,h4').get_text(' ',strip=True).casefold() for n in root.select('.reading-region > .role')),
        'no orphan prose':all(n.find_parent(class_='reading-region') for n in root.select('h2,h3,h4,h5,p,li,a')),
        'no nested paper':not root.select('.reading-region .reading-region'),
        'all unique IDs':len(doc.select('[id]'))==len({n['id'] for n in doc.select('[id]')}),
        'no internal document links':not any('_quy_trinh' in n['href'] or 'E:/' in n['href'] for n in doc.select('a[href]')),
        'no editorial status in learner copy':not doc.select('.prototype-note') and 'HTML thử nghiệm' not in doc.get_text(' ',strip=True),
        'current source data hash':sha(REPO/build['canonical_data'])==build['canonical_data_sha256'],
        'current partial hash':sha(REPO/'content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_partials/chuong_trinh.qmd')==build['partial_sha256'],
        'generated sources current':all(p.is_file() and p.read_text(encoding='utf-8')==s.rstrip()+'\n' for p,s in outputs().items()),
    }
    data=load_yaml(DATA_PATH)
    checks['catalog availability separate from acceptance']=[package_from_ref(r).display_status for r in data['packages']]==['Có thể học','Bản xem trước','Bản xem trước']
    for name,changed in [('unknown availability',{'learner_availability':'accepted'}),('unaccepted without explicit preview',{'learner_availability':None})]:
        bad=copy.deepcopy(data);bad['packages'][1].update(changed)
        try:
            validate_data(bad);package_from_ref(bad['packages'][1]);rejected=False
        except ValueError:rejected=True
        checks['fixture rejects '+name]=rejected
    missing=[]; parsed={page.resolve():doc}
    for node in doc.select('img[src],script[src],link[href],a[href]'):
        value=node.get('src',node.get('href'));url=urlsplit(value)
        if url.scheme or url.netloc:continue
        target=(page.parent/unquote(url.path)).resolve() if url.path else page.resolve()
        if not target.is_file():missing.append(value);continue
        if url.fragment and target.suffix=='.html':
            if target not in parsed:parsed[target]=BeautifulSoup(target.read_text(encoding='utf-8'),'html.parser')
            if not parsed[target].find(id=unquote(url.fragment)):missing.append(value)
    checks['all resources links fragments']=not missing
    for name,spec in build['resources'].items():
        checks['runtime current '+name]=sha(REPO/spec['source'])==spec['sha256']
        runtime=(page.parent/unquote(urlsplit(doc.select_one('link[rel=stylesheet]')['href']).path)).resolve().parent
        checks['runtime payload exact '+name]=(runtime/name).is_file() and sha(runtime/name)==spec['sha256']
    # Keep real failing fixtures as evidence that content/footer/layout guards fire.
    for name,selector in [('orphan','#học-theo-cách-nào'),('duplicate-label','.reading-region > .role'),('missing-footer','#site-footer')]:
        bad=copy.deepcopy(doc)
        node=bad.select_one(selector)
        if name=='orphan':bad.select_one('.reader-content').append(node.extract());valid=all(n.find_parent(class_='reading-region') for n in bad.select('.reader-content h2'))
        elif name=='missing-footer':node.decompose();valid=complete_site_footer(bad,footer_data())
        else:
            heading=node.parent.select_one('h2,h3');node.string=heading.get_text(' ',strip=True);valid=node.get_text(' ',strip=True).casefold()!=heading.get_text(' ',strip=True).casefold()
        checks['fixture rejects '+name]=not valid
    return checks,missing


def browser(page,out):
    checks={};details={};out.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='home_edge_',dir=out) as temp:
        sock=socket.socket();sock.bind(('127.0.0.1',0));port=sock.getsockname()[1];sock.close()
        process=subprocess.Popen([edge_executable(),'--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check',
            '--remote-allow-origins=http://localhost',f'--remote-debugging-port={port}',f'--user-data-dir={temp}','about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        b=None
        try:
            for _ in range(100):
                try:
                    targets=requests.get(f'http://127.0.0.1:{port}/json',timeout=1).json()
                    ws=next(t['webSocketDebuggerUrl'] for t in targets if t['type']=='page');break
                except (requests.RequestException,ValueError,StopIteration):time.sleep(.1)
            else:raise RuntimeError('Headless Edge unavailable')
            b=Browser(ws);b.call('Page.enable')
            for width in [1920,1440,1000,768,430,390,320]:
                b.viewport(width,900);b.navigate(page.as_uri());b.click('[name=background][value=yellow-1]')
                if b.evaluate('document.documentElement.classList.contains("grayscale")'):b.click('#grayscale')
                geometry=b.evaluate(GEOMETRY);details[str(width)]=geometry
                for key in ['orphan','overflow','axes']:checks[f'{width}/{key}']=geometry[key]==[]
                for key in ['fits','white','widths','gaps','loaded']:checks[f'{width}/{key}']=geometry[key]
                checks[f'{width}/one paper level']=geometry['nested']==0
                controls=b.evaluate("""(()=>{const a=[...document.querySelectorAll('.swatches label,.gray-toggle')].map(n=>n.getBoundingClientRect());return a.length===7&&new Set(a.map(r=>r.top)).size===1&&a.every(r=>r.width>=24&&r.height>=44&&r.right<=innerWidth)&&document.querySelectorAll('[name=background]:checked').length===1})()""")
                checks[f'{width}/inline controls']=controls
                checks[f'{width}/button icon only']=b.evaluate('getComputedStyle(document.querySelector(".mobile-view")).display')=='none'
                if width in [1440,430,390,320]:
                    b.screenshot(out/f'home-cover-{width}.png')
                    for anchor,scene in [('giới-thiệu','orientation'),('học-theo-cách-nào','method'),('tám-mạch','strands'),('hoc-lieu-hien-co','packages'),('bắt-đầu-từ-đâu','start'),('site-footer','footer')]:
                        b.evaluate('document.getElementById('+json.dumps(anchor)+').scrollIntoView({block:"start"})');time.sleep(.1)
                        b.screenshot(out/f'home-{scene}-{width}.png')
                    b.evaluate('scrollTo(0,0)');before=b.evaluate('innerWidth')
                    positions=[]
                    for y in [250,450,850,1250,850,450]:
                        b.evaluate(f'scrollTo(0,{y})');time.sleep(.1)
                        positions.append(b.evaluate('({y:scrollY,top:document.querySelector(".site-top").getBoundingClientRect().top,width:innerWidth,nav:document.querySelector(innerWidth>=1000?".rail":".mobile-trigger").getBoundingClientRect().top})'))
                    checks[f'{width}/stable scroll']=all(abs(p['y']-y)<=1 for p,y in zip(positions,[250,450,850,1250,850,450]))
                    checks[f'{width}/stable toolbar/nav/width']=len({p['top'] for p in positions})==1 and len({p['nav'] for p in positions})==1 and all(p['width']==before for p in positions)
                    for theme in ['gray-3','gray-2','yellow-1','yellow-2','red-1','red-2']:
                        b.click(f'[name=background][value={theme}]')
                        checks[f'{width}/{theme}/white paper']=b.evaluate(GEOMETRY)['white']
                    b.evaluate('document.querySelector("[name=background][value=gray-3]").focus()');b.key('ArrowRight',39)
                    checks[f'{width}/radio keyboard']=b.evaluate('document.querySelector("[name=background][value=gray-2]").checked')
                    b.evaluate('document.getElementById("grayscale").focus()');b.key('Enter',13,'\r')
                    b.call('Page.reload');b.ready()
                    checks[f'{width}/preferences reload']=b.evaluate('document.querySelector("[name=background][value=gray-2]").checked&&document.getElementById("grayscale").getAttribute("aria-pressed")==="true"')
                    b.click('#grayscale');b.click('[name=background][value=yellow-1]')
                    if width<1000:
                        b.evaluate('document.querySelector(".mobile-trigger").focus()');b.key('Enter',13,'\r')
                        checks[f'{width}/drawer keyboard opens']=b.evaluate('document.getElementById("mobile-nav").open')
                        b.screenshot(out/f'home-drawer-{width}.png');b.key('Escape',27)
                        checks[f'{width}/drawer escape focus']=b.evaluate('!document.getElementById("mobile-nav").open&&document.activeElement.matches(".mobile-trigger")')
                        b.click('.mobile-trigger');b.click('.home-nav a[href="#hoc-lieu-hien-co"]')
                        checks[f'{width}/drawer actual target']=b.evaluate('!document.getElementById("mobile-nav").open&&location.hash==="#hoc-lieu-hien-co"&&document.getElementById("hoc-lieu-hien-co").getBoundingClientRect().top>=63')
                        b.click('.mobile-trigger');b.viewport(1440,900);time.sleep(.1)
                        checks[f'{width}/resize restores navigation']=b.evaluate('!document.getElementById("mobile-nav").open&&document.querySelector("#rail-content .home-nav")!==null')
                        b.viewport(width,900)
                b.call('Emulation.setScriptExecutionDisabled',{'value':True});b.navigate(page.as_uri())
                state=b.evaluate(GEOMETRY)
                checks[f'{width}/noJS readable']=state['fits'] and state['white'] and state['loaded'] and state['orphan']==[]
                checks[f'{width}/noJS navigation visible']=b.evaluate('!!document.querySelector(".home-nav").getClientRects().length')
                if width in [1440,430,390,320]:b.screenshot(out/f'home-nojs-{width}.png')
                b.call('Emulation.setScriptExecutionDisabled',{'value':False})
            b.viewport(1440,900)
            for package,count in [('r1_g01',69),('r1_g02',59)]:
                b.navigate(page.as_uri());b.click(f'.zo-on-thi-package[data-package-id={package}] a')
                b.ready()
                checks[package+'/CTA current start view']=b.evaluate('new URL(location.href).searchParams.get("r1-view")==="bat-dau"&&location.hash==="#bat-dau"')
                binding=json.loads((REPO/'content/thpt/on_thi_toan_thpt/hoc_lieu'/package/'giao_dien/he_nhan.json').read_text(encoding='utf-8'))
                expected=sorted(u['id'] for u in binding['units'])
                actual=b.evaluate('[...new Set([...document.querySelectorAll("[data-zo-task]")].map(n=>n.dataset.zoTask))].sort()')
                checks[package+'/CTA current labeled candidate']=actual==expected and len(expected)==count
                b.evaluate('history.back()');time.sleep(.2);b.ready()
                checks[package+'/Back restores Home']=b.evaluate('document.body.classList.contains("course-home")&&!!document.querySelector(".home-nav")')
            b.navigate(page.as_uri());b.click('.home-nav a[href="#hoc-lieu-hien-co"]');b.call('Page.reload');b.ready()
            checks['Home deep link reload']=b.evaluate('location.hash==="#hoc-lieu-hien-co"&&document.getElementById("hoc-lieu-hien-co").getBoundingClientRect().top>=63')
            save(out/'measurements.json',details)
        finally:
            if b:b.ws.close()
            process.terminate();process.wait(timeout=15)
    return checks


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['rebuild','preview','check'])
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--html',type=Path)
    parser.add_argument('--build',type=Path)
    parser.add_argument('--g01',type=Path);parser.add_argument('--g02',type=Path)
    parser.add_argument('--browser',action='store_true')
    args=parser.parse_args();out=args.output.resolve()
    if not out.is_relative_to(REPO/'_audit') or out==REPO/'_audit':parser.error('Output must be named _audit directory')
    out.mkdir(parents=True,exist_ok=True)
    if args.command=='rebuild':rebuild(out);return 0
    if not args.html:parser.error('--html required')
    if args.command=='preview':
        if not args.g01 or not args.g02:parser.error('Explicit current package candidates required')
        preview(args.html.resolve(),out,args.g01.resolve(),args.g02.resolve());return 0
    if not args.build:parser.error('--build required')
    build=json.loads(args.build.read_text(encoding='utf-8'))
    checks,missing=static(args.html.resolve(),build)
    if args.browser:
        if build.get('layout') == 'editorial-home-2027':
            from zo_web_2027_home_landing_check import browser as editorial_browser
            checks.update(editorial_browser(args.html.resolve(),out/'images'))
        else:
            checks.update(browser(args.html.resolve(),out/'images'))
    report={'checks':checks,'passed':sum(checks.values()),'total':len(checks),'failures':[k for k,v in checks.items() if not v],
            'missing_links':missing,'html_sha256':sha(args.html),'checker_sha256':sha(Path(__file__)),
            'limits':['Edge headless only, not Safari/Firefox or real touch/screen reader.','Not owner acceptance, PDF synchronization or publication.']}
    save(out/'qa.json',report);print(json.dumps({k:report[k] for k in ['passed','total','failures']},ensure_ascii=False))
    return 0 if not report['failures'] else 1


if __name__=='__main__':raise SystemExit(main())

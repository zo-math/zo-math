"""Check current G02 completion HTML, source bindings and old defect regressions."""
from __future__ import annotations
import argparse
from collections import Counter
import copy
import json
from pathlib import Path
import re
import socket
import subprocess
import sys
import tempfile
import time
from urllib.parse import unquote,urlsplit
sys.dont_write_bytecode=True
import requests
import yaml
from bs4 import BeautifulSoup
from zo_web_2027_check import Browser, Checks, GEOMETRY, edge_executable
from zo_web_2027_g02 import canonical_math_matches
from zo_web_2027_preview import dump, sha, BRAND_THOUGHT
ROOT=Path(__file__).resolve().parents[1]
PACKAGE=ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02'

def formulas(text):
    text=re.sub(r'^!\[.*$','',text,flags=re.M)
    return [''.join(x.split()) for pair in re.findall(r'\$\$(.*?)\$\$|\$(.*?)\$',text,re.S) for x in pair if x]

def task_blocks(text):
    result={};lines=text.splitlines()
    for i,line in enumerate(lines):
        m=re.match(r'^(:+)\s+\{#((?:l\d\d|kt\d\d|s\d\d|s-[lok]-e\d\d|s-p\d\d|thu-lai-chuyen-giao|loi-giai-[^\s}]+))\s',line)
        if not m:continue
        for j in range(i+1,len(lines)):
            if lines[j].strip()==m[1]:
                result[m[2]]='\n'.join(lines[i:j+1]);break
    return result

def check(output):
    output=output.resolve();c=Checks(output);(output/'images').mkdir(exist_ok=True)
    page_path=output/'g02-reading.html'
    page=BeautifulSoup(page_path.read_text(encoding='utf-8'),'html.parser')
    raw_path=output/'raw/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02/index.html'
    raw=BeautifulSoup(raw_path.read_text(encoding='utf-8'),'html.parser')
    c.check('Fresh canonical math including foundations matches raw render',canonical_math_matches(PACKAGE/'index.qmd',raw.select_one('.zo-on-thi-package')))
    rendered=[n.get_text() for n in page.select('.reader-content annotation') if not n.find_parent(class_='zo-variation-native')]
    canonical=[n.get_text() for n in raw.select('.zo-on-thi-package annotation')]
    c.check('All canonical formulas survive final payloads in order',rendered,canonical)
    old=(output/'source-before.qmd').read_text(encoding='utf-8');new=(PACKAGE/'index.qmd').read_text(encoding='utf-8')
    # Includes are canonical content too: journal reuse must not look like loss.
    def expand(path):
        text=path.read_text(encoding='utf-8')
        return re.sub(r'\{\{<\s*include\s+([^>]+?)\s*>\}\}',lambda m:expand((path.parent/m[1].strip()).resolve()),text)
    missing=list((Counter(formulas(old))-Counter(formulas(expand(PACKAGE/'index.qmd')))).elements())
    c.check('Existing source formulas preserved at least once per occurrence',missing,[])
    old_tasks=task_blocks(old);new_tasks=task_blocks(new)
    drift=[name for name,text in old_tasks.items() if name!='loi-giai-on-lai-01' and (name not in new_tasks or formulas(text)!=formulas(new_tasks[name]))]
    c.check('Existing task and answer mathematics preserved by identity',drift,[])
    review_rows=[line for line in old.splitlines() if line.startswith('| Sau khoảng')]
    for i,line in enumerate(review_rows,1):
        section=re.search(r'\{#o0'+str(i)+r'\s[^}]*\}(.*?)(?=^### )',new,re.S|re.M)[1]
        old_section=re.search(r'\{#o0'+str(i)+r'\s[^}]*\}(.*?)(?=^### )',old,re.S|re.M)
        c.check(f'Review {i} original mathematics intact',formulas(section),formulas(old_section[1] if old_section else line))
    answers='\n'.join(new_tasks['loi-giai-on-lai-0'+str(i)] for i in [1,2,3])
    old_answers='\n'.join(old_tasks['loi-giai-on-lai-0'+str(i)] for i in [1,2,3]) if 'loi-giai-on-lai-02' in old_tasks else old_tasks['loi-giai-on-lai-01']
    c.check('Three separated review answers retain original math sequence',formulas(answers),formulas(old_answers))
    old_ids=set(re.findall(r'\{#([^\s}]+)',old));new_ids=set(re.findall(r'\{#([^\s}]+)',new))
    c.check('Existing explicit source IDs retained',sorted(old_ids-new_ids),[])
    ids=[n['id'] for n in page.select('[id]')];c.check('Unique HTML IDs',len(ids),len(set(ids)))
    architecture=yaml.safe_load((PACKAGE/'_quy_trinh/kien_truc_hoc_tap.yml').read_text(encoding='utf-8'))
    missing=[]
    for task in architecture['tasks']:
        for key in ['source_anchor','answer_anchor']:
            if task.get(key) and not page.find(id=task[key]):missing.append([task['id'],key,task[key]])
    c.check('All 39 task/answer anchors exist',missing,[])
    c.check('Eight real checkpoints',[n for n in ['cp-lt1','cp-lt2','cp-lt3','cp-kt','cp-on1','cp-on2','cp-on3','cp-p'] if not page.find(id=n)],[])
    c.check('Nine real foundation units',len(page.select('details.r1-foundation-unit')),9)
    journal=page.find(id='nhat-ky');c.check('Journal has exact 14 fields',len(journal.select('#r1-table-t13 tbody tr')),14)
    c.check('Journal is separate from review tasks',not journal.select('[id=o01],[id=o02],[id=o03]'))
    c.check('Approved brand thought',page.select_one('.brand-thought').get_text(' ',strip=True),BRAND_THOUGHT)
    c.check('Six themes and grayscale',len(page.select('[name=background]'))==6 and bool(page.select_one('#grayscale')))
    c.check('PDF three-column cards',len(page.select('.zo-pdf-card')),8)
    c.check('PDF synchronization warning',bool(page.select_one('.zo-pdf-current-note')))
    c.check('Two native BBT tables',len(page.select('.zo-variation-native')),2)
    c.check('Four 0.4 mathematical figures',len(page.select('img.zo-graph-04')),4)
    c.check('No nested reading regions',len(page.select('.reading-region .reading-region')),0)
    final_ids=set(ids)
    c.check('Negative guard rejects missing checkpoint',not {'cp-lt1','cp-lt2','cp-lt3'}.issubset(final_ids-{'cp-lt2'}))
    broken=copy.deepcopy(raw.select_one('.zo-on-thi-package'));broken.select_one('annotation').decompose()
    c.check('Negative guard rejects removed mathematical content',not canonical_math_matches(PACKAGE/'index.qmd',broken))
    missing=[]
    for n in page.select('[src],a[href],link[href]'):
        value=n.get('src',n.get('href',''));s=urlsplit(value)
        if s.scheme or s.netloc:continue
        path=(output/unquote(s.path)).resolve() if s.path else page_path
        if not path.is_file():missing.append(value);continue
        if s.fragment and path.suffix=='.html':
            target=page if path==page_path else BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
            if not target.find(id=unquote(s.fragment)):missing.append(value)
    c.check('Every local asset/link/fragment exists',missing,[])
    # Check the final download href and download names against raw canonical pairs.
    c.check('PDF URL and download names preserved',[(n.get('data-canonical-href',n['href']),n['download']) for n in page.select('a[download]')],[(n['href'],n['download']) for n in raw.select('.zo-on-thi-package a[download]')])
    c.check('No default foreign-package foundation return','câu khởi động 04' not in page.find(id='on-nen').get_text(' ',strip=True))
    with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    base=f'http://127.0.0.1:{port}';url=page_path.as_uri()
    geom=GEOMETRY.replace('visible=n=>',"visible=n=>!n.closest('.support-region,.zo-pdf-copy')&&")
    with tempfile.TemporaryDirectory(prefix='browser_',dir=output) as profile:
        process=subprocess.Popen([edge_executable(),'--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check',f'--remote-debugging-port={port}','--remote-debugging-address=127.0.0.1','--remote-allow-origins=http://localhost','--user-data-dir='+profile,'about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        browser=None
        try:
            for _ in range(100):
                try:
                    if requests.get(base+'/json/version',timeout=.3).ok:break
                except requests.RequestException:time.sleep(.1)
            target=requests.put(base+'/json/new?about:blank',timeout=10).json()
            browser=Browser(target['webSocketDebuggerUrl']);browser.call('Page.enable');browser.call('Runtime.enable')
            browser.call('Page.addScriptToEvaluateOnNewDocument',{'source':"window.qaErrors=[];addEventListener('error',e=>qaErrors.push(e.message));console.error=(...a)=>qaErrors.push(a.map(String).join(' '));"})
            for width in [1440,430,390,320,1000,1920]:
                print('G02 completed QA',width,flush=True)
                browser.viewport(width,960 if width>500 else 844);browser.navigate(url)
                tabs=browser.evaluate('[...document.querySelectorAll(".r1-tab")].map(n=>n.id)')
                c.check(f'{width}: controller fully initialized',browser.evaluate('document.querySelector(".reader-content").classList.contains("r1-tabs-ready")'))
                c.check(f'{width}: twelve actual views',len(tabs),12)
                c.check(f'{width}: main route order',tabs[:5],['r1-tab-bat-dau','r1-tab-bai-hoc','r1-tab-luyen-tap','r1-tab-kiem-tra','r1-tab-on-lai'])
                for tab in tabs:
                    browser.click('#'+tab);state=browser.evaluate(geom)
                    for key in ['orphan','overflow','axes']:c.check(f'{width}/{tab}: {key}',state[key],[])
                    for key in ['fits','white','widths','gaps','loaded']:c.check(f'{width}/{tab}: {key}',state[key])
                    c.check(f'{width}/{tab}: nested paper',state['nested'],0)
                    c.check(f'{width}/{tab}: bounded reader',state['readerWidth']<=816)
                browser.navigate(url+'?r1-view=on-lai#o02');c.check(f'{width}: review not journal',browser.evaluate('!document.getElementById("nhat-ky").getClientRects().length'))
                browser.navigate(url+'#bat-dau');c.check(f'{width}: old linear guide is not displayed',browser.evaluate('!document.getElementById("r1-g02-table-t08").getClientRects().length'))
                browser.navigate(url+'?r1-view=on-lai#o02')
                browser.click('#r1-tab-nhat-ky');c.check(f'{width}: journal not review',browser.evaluate('document.getElementById("nhat-ky").getClientRects().length>0&&!document.getElementById("o02").getClientRects().length'))
                browser.navigate(url+'?r1-view=toan-van#bai-hoc');browser.evaluate('document.querySelectorAll(".reader-content details").forEach(n=>n.open=true)')
                state=browser.evaluate(geom)
                for key in ['orphan','overflow','axes']:c.check(f'{width}/open-all: {key}',state[key],[])
                c.check(f'{width}/open-all: fits',state['fits'])
                browser.evaluate('document.querySelector(".reader-content .role").style.transform="translateX(8px)"')
                c.check(f'{width}: negative guard rejects inset role',bool(browser.evaluate(geom)['axes']))
                for cp in ['cp-lt1','cp-kt','cp-on2','cp-on3','cp-p']:
                    browser.navigate(url+f'?r1-view=on-nen&r1-return={cp}&r1-context={cp}#nen-n-txd-01')
                    c.check(f'{width}/{cp}: accurate support return',browser.evaluate(f'document.querySelector(".r1-return-link").hash==="#{cp}"'))
                    browser.call('Page.reload');browser.ready();browser.click('.r1-return-link')
                    c.check(f'{width}/{cp}: reload then return',browser.evaluate('location.hash'), '#'+cp)
                browser.navigate(url+'#s-o-e02')
                c.check(f'{width}: direct review support choices',browser.evaluate('[...document.querySelectorAll(".r1-return-link")].map(n=>n.hash)'),['#cp-on1','#cp-on2','#cp-on3'])
                browser.navigate(url+'#s-p02');c.check(f'{width}: direct transfer return',browser.evaluate('[...document.querySelectorAll(".r1-return-link")].map(n=>n.hash)'),['#cp-p'])
                browser.navigate(url+'#l01');browser.click('#l01 .answer-link a');c.check(f'{width}: task to answer',browser.evaluate('location.hash'),'#loi-giai-l01')
                browser.click('#loi-giai-l01 .answer-link a');c.check(f'{width}: answer to task',browser.evaluate('location.hash'),'#l01')
                browser.evaluate('history.back()');time.sleep(.2);c.check(f'{width}: browser Back restores answer',browser.evaluate('location.hash'),'#loi-giai-l01')
                browser.navigate(url);positions=[]
                for y in [100,200,300,200]:
                    browser.evaluate(f'scrollTo(0,{y})');time.sleep(.06)
                    positions.append(browser.evaluate('({y:scrollY,top:document.querySelector(".site-top").getBoundingClientRect().top,nav:document.querySelector(innerWidth>=1000?".rail":".mobile-trigger").getBoundingClientRect().top})'))
                c.check(f'{width}: no scroll jumps',[n['y'] for n in positions],[100,200,300,200])
                c.check(f'{width}: stable toolbar',len({n['top'] for n in positions}),1)
                c.check(f'{width}: stable nav',len({n['nav'] for n in positions}),1)
                for theme in ['gray-3','gray-2','yellow-1','yellow-2','red-1','red-2']:
                    browser.click('[name=background][value='+theme+']');c.check(f'{width}/{theme}: white paper',browser.evaluate(geom)['white'])
                browser.click('#grayscale');browser.call('Page.reload');browser.ready();c.check(f'{width}: settings survive reload',browser.evaluate('document.documentElement.classList.contains("grayscale")&&document.querySelector("[value=red-2]").checked'))
                browser.click('#grayscale');browser.click('[value=yellow-1]')
                c.check(f'{width}: compact one-row choices',browser.evaluate('new Set([...document.querySelectorAll(".swatches label,.gray-toggle")].map(n=>n.getBoundingClientRect().top)).size===1'))
                c.check(f'{width}: icon-only nav',browser.evaluate('getComputedStyle(document.querySelector(".mobile-view")).display==="none"'))
                if width<1000:
                    browser.click('.mobile-trigger');c.check(f'{width}: mobile drawer opens',browser.evaluate('document.getElementById("mobile-nav").open'))
                    browser.key('Escape',27);c.check(f'{width}: drawer focus returns',browser.evaluate('!document.getElementById("mobile-nav").open&&document.activeElement.matches(".mobile-trigger")'))
                if width in [1440,390]:
                    for name,route in [('cover',''),('start','#bat-dau'),('practice','#g02-c1'),('checkpoint','#cp-lt2'),('review','#o02'),('journal','#nhat-ky'),('foundation','#g02-nen-do-thi-xac-nhan'),('download','#tai-tai-lieu'),('support','#ung-ho')]:
                        browser.navigate(url+route);browser.screenshot(output/'images'/f'{name}-{width}.png')
                    metrics="""(() => ['.reading-region','.reading-region .role','.reading-region h2','.reading-region p'].map(s=>{const n=document.querySelector(s),c=getComputedStyle(n);return [c.fontFamily,c.fontSize,c.lineHeight,c.paddingLeft,c.paddingRight,c.color,c.borderRadius]}))()"""
                    browser.navigate(url+'#bat-dau');g02=browser.evaluate(metrics)
                    accepted=ROOT/'docs/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.html'
                    browser.navigate(accepted.as_uri()+'?r1-view=bat-dau#bat-dau')
                    c.check(f'{width}: same-role typography/inset/radius as current approved G01',g02,browser.evaluate(metrics))
                c.errors+=browser.evaluate('window.qaErrors')
            browser.call('Emulation.setScriptExecutionDisabled',{'value':True});browser.navigate(url)
            c.check('No JavaScript: content still accessible',browser.evaluate('[...document.querySelectorAll(".reader-content>section.level2")].every(n=>n.getClientRects().length>0)'))
        finally:
            if browser:
                try:browser.call('Browser.close')
                except Exception:pass
                browser.ws.close()
            try:process.wait(timeout=10)
            except subprocess.TimeoutExpired:process.terminate();process.wait(timeout=10)
    c.check('No browser JS errors',c.errors,[])
    failed=[n for n in c.checks if not n['pass']]
    dump(output/'completion-qa.json',{'checks':c.checks,'passed':len(c.checks)-len(failed),'total':len(c.checks),'html_sha256':sha(page_path),'raw_sha256':sha(raw_path),'source_sha256':sha(PACKAGE/'index.qmd'),'limits':['Owner review pending','No learning PDF build or synchronization','No Safari/Firefox/real touch/screen-reader testing'],'browser_profile_removed':not Path(profile).exists()})
    print(json.dumps({'passed':len(c.checks)-len(failed),'total':len(c.checks),'failures':[n['name'] for n in failed]},ensure_ascii=False));return int(bool(failed))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=ROOT/'_audit/zo_g02_completion_2026-10-08')
    raise SystemExit(check(parser.parse_args().output))

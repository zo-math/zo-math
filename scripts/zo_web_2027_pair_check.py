"""Pair correction gates: evidence per reported defect, not acceptance/release."""
from collections import Counter
import copy
import json
from pathlib import Path
import re
import socket
import subprocess
import tempfile
import time
from urllib.parse import unquote, urlsplit
import requests
from bs4 import BeautifulSoup
from zo_web_2027_check import Browser, Checks, GEOMETRY, edge_executable
from zo_web_2027_production import pools
from zo_web_2027_preview import sha, dump

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_audit/zo_web_pair_refinement_2026-10-08'
BASE=Path('content/thpt/on_thi_toan_thpt/hoc_lieu')
PAGES=[OUT/'r1_g01-render/docs'/BASE/'r1_g01/index.html',OUT/'g02/g02-reading.html']
RAW=[OUT/'after/r1_g01-raw/docs'/BASE/'r1_g01/index.html',OUT/'g02/raw'/BASE/'r1_g02/index.html']

def parse(path):return BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
def math(node):return [n.get_text() for n in node.select('annotation') if not n.find_parent(class_='zo-variation-native')]
def expand(path):
    return re.sub(r'\{\{<\s*include\s+([^>]+?)\s*>\}\}',lambda m:expand((path.parent/m[1].strip()).resolve()),path.read_text(encoding='utf-8'))
def source_math(value):
    value=re.sub(r'^!\[.*$','',value,flags=re.M)
    return Counter(''.join(x.split()) for pair in re.findall(r'\$\$(.*?)\$\$|\$(.*?)\$',value,re.S) for x in pair if x)
def duplicate_labels(doc):
    found=[]
    for paper in doc.select('.reading-region'):
        labels=[n.get_text(' ',strip=True) for n in paper.select('[data-reading-label]')]
        if len(labels)!=len(set(labels)):found.append(labels)
    return found
def ambiguous_actions(doc):
    found=[]
    for task in doc.select('.zo-learning-task'):
        actions=[a for a in task.select('.answer-link a') if a.find_parent(class_='zo-learning-task') is task]
        labels=[a.get_text(' ',strip=True) for a in actions]
        if len(labels)!=len(set(labels)):found.append(task.get('id'))
    return found

def main():
    c=Checks(OUT);(OUT/'images').mkdir(exist_ok=True)
    documents=[parse(p) for p in PAGES];raws=[parse(p) for p in RAW]
    policy=json.loads((ROOT/'_design/web_2027_mau_dung_chung/profiles/r1-consistency.json').read_text(encoding='utf-8'))
    common_groups=['Lời giải Khởi động','Lời giải Bài học','Lời giải Luyện tập','Lời giải Kiểm tra',
        'Lời giải Sửa lỗi sau Luyện tập','Lời giải Sửa lỗi sau Kiểm tra','Lời giải Ôn lại','Lời giải Sửa lỗi sau Ôn lại']
    for i,(page,raw,path) in enumerate(zip(documents,raws,PAGES),1):
        label=f'G0{i}'
        root=page.select_one('.reader-content');source=raw.select_one('.zo-on-thi-package')
        c.check(label+': fresh-render mathematics retained in order',math(root),math(source))
        before=OUT/f'r1_g0{i}-before.qmd';current=ROOT/BASE/f'r1_g0{i}/index.qmd'
        # Include bodies are shared canonical sources; no math changed in them.
        old=before.read_text(encoding='utf-8')
        old=re.sub(r'\{\{<\s*include\s+([^>]+?)\s*>\}\}',lambda m:expand((current.parent/m[1].strip()).resolve()),old)
        c.check(label+': all original math occurrences retained',source_math(old)-source_math(expand(current)),Counter())
        ids=[n['id'] for n in page.select('[id]')]
        c.check(label+': IDs unique',len(ids),len(set(ids)))
        c.check(label+': every fresh source ID retained',sorted(set(n['id'] for n in source.select('[id]'))-set(ids)),[])
        oldids=set(re.findall(r'\{#([^\s}]+)',before.read_text(encoding='utf-8')))
        c.check(label+': historical explicit IDs retained',sorted(oldids-set(ids)),[])
        c.check(label+': all authored disclosures initially closed',len(root.select('details[open]')),0)
        for heading, role in policy['page_roles'].items():
            owners=[p for p in root.select('.reading-region') if p.select_one('h2') and p.select_one('h2').get_text(' ',strip=True)==heading]
            c.check(label+': shared page role '+heading,[p.select_one('[data-reading-label]').get_text(' ',strip=True) for p in owners],[role])
        c.check(label+': no default-open class',len(root.select('.r1-open-by-default')),0)
        c.check(label+': no duplicate role metadata',duplicate_labels(page),[])
        c.check(label+': task action labels distinguish their purpose',ambiguous_actions(page),[])
        c.check(label+': no nested papers',len(root.select('.reading-region .reading-region')),0)
        groups=[h.get_text(' ',strip=True) for h in root.select('#loi-giai h3')]
        c.check(label+': common solution categories', [g for g in groups if g in common_groups],common_groups)
        c.check(label+': source content outside footer style',not page.find(id='nguon').find_parent(class_='r1-footer'))
        c.check(label+': exact shared journal labels', [n.get_text(' ',strip=True) for n in page.select('#r1-table-t13 tbody th')],
            [n.get_text(' ',strip=True) for n in documents[0].select('#r1-table-t13 tbody th')])
        c.check(label+': fourteen journal fields',len(page.select('#r1-table-t13 tbody tr')),14)
        table=page.select_one('#r1-table-t12, #r1-g02-table-t04')
        c.check(label+': common remediation header', [n.get_text(' ',strip=True) for n in table.select('thead th')],policy['routing_headers'])
        c.check(label+': common remediation width',table['data-col-widths'],'40,20,20,20')
        c.check(label+': three actual repair routes per row',all(len(row.select('a[href]'))==3 for row in table.select('tbody tr')))
        c.check(label+': no long legacy task titles',not re.search(r'Bài Ôn lại|Bài sửa lỗi|Bài tập khắc phục lỗi',root.get_text(' ',strip=True)))
        c.check(label+': warmup answers exist',bool(page.select_one('#loi-giai-khoi-dong .r1-solution')))
        c.check(label+': local answer targets exist', [a['href'] for a in root.select('.answer-link a[href^="#"]') if not page.find(id=unquote(a['href'][1:]))],[])
        bad=[]
        for image in root.select('img[src]'):
            if not (path.parent/unquote(image['src'])).resolve().is_file():bad.append(image['src'])
        c.check(label+': diagram files exist',bad,[])
    c.check('G01: introductory three stages visible in Start',bool(documents[0].select_one('#bat-dau #lo-trinh-hoc')))
    c.check('G01: correct introductory checkpoint targets',[a['href'] for a in documents[0].select('#lo-trinh-hoc li a') if a['href'].startswith('#cp-')],['#cp-lt1','#cp-lt2','#cp-lt3'])
    opening=documents[0].find(id='cách-học-với-tài-liệu-này')
    direct=list(opening.find_all(recursive=False))
    c.check('G01: opening order follows QMD before stages',direct.index(opening.find('h3',recursive=False)) < direct.index(opening.find('ol',recursive=False)) < direct.index(opening.find(id='lo-trinh-hoc',recursive=False)))
    c.check('G01: promoted layout equals explicit migration candidate',
        json.loads((ROOT/BASE/'r1_g01/giao_dien/web_2027_layout.json').read_text(encoding='utf-8')),
        json.loads((OUT/'g01-layout-candidate.json').read_text(encoding='utf-8')))
    c.check('G02: L06 formula vs answer actions',[a.get_text(' ',strip=True) for a in documents[1].select('#l06 .answer-link a')],['Xem công thức để kiểm tra','Xem lời giải'])
    for target in ['g02-nen-txd-xac-nhan','g02-nen-do-thi-xac-nhan']:
        node=documents[1].find(id=target)
        c.check('G02: confirmation owned by a closed foundation card '+target,bool(node.find_parent('details',class_='r1-foundation-confirmation')))
    for target in ['o01','o02','o03']:
        text=documents[1].find(id=target).get_text(' ',strip=True)
        c.check('G02: explicit review purpose/control/error '+target,all(w in text for w in ['Mục tiêu:','Điểm dừng:','Lỗi cần quan sát:']))
    cover=json.loads((ROOT/BASE/'r1_g02/giao_dien/assets/figures_0_4/cover-provenance.json').read_text(encoding='utf-8'))
    c.check('G02: cover from its own canonical source',cover['source'].startswith((BASE/'r1_g02').as_posix()))
    c.check('G02: transparent cover',cover['surface'],'transparent-light')
    c.check('G02: current cover source receipt',sha(ROOT/cover['source']),cover['source_sha256'])
    c.check('G02: current cover asset receipt',sha(OUT/'g02/assets/figures04/cover-light.svg'),cover['asset_sha256'])
    c.check('G02: distinct cover bytes',sha(OUT/'g02/assets/figures04/cover-light.svg')!=sha(ROOT/BASE/'r1_g01/giao_dien/assets/figures_0_4/cover-light.svg'))
    # Negative fixtures exercise the very assertions used on the candidates.
    broken=copy.deepcopy(documents[1]);p=broken.select_one('.reading-region');p.append(copy.deepcopy(p.select_one('[data-reading-label]')))
    c.check('Negative fixture: role duplicate detected',bool(duplicate_labels(broken)))
    broken=copy.deepcopy(documents[1]);a=broken.select_one('#l06 .answer-link a');a.string='Xem lời giải'
    c.check('Negative fixture: ambiguous task action detected',bool(ambiguous_actions(broken)))
    with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    metrics={}
    with tempfile.TemporaryDirectory(prefix='pair_browser_',dir=OUT) as profile:
        process=subprocess.Popen([edge_executable(),'--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check',f'--remote-debugging-port={port}','--remote-debugging-address=127.0.0.1','--remote-allow-origins=http://localhost','--user-data-dir='+profile,'about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        browser=None
        try:
            base=f'http://127.0.0.1:{port}'
            for _ in range(100):
                try:
                    if requests.get(base+'/json/version',timeout=.3).ok:break
                except requests.RequestException:time.sleep(.1)
            target=requests.put(base+'/json/new?about:blank',timeout=10).json();browser=Browser(target['webSocketDebuggerUrl'])
            browser.call('Page.enable');browser.call('Runtime.enable')
            browser.call('Page.addScriptToEvaluateOnNewDocument',{'source':"window.qaErrors=[];addEventListener('error',e=>qaErrors.push(e.message));console.error=(...a)=>qaErrors.push(a.map(String).join(' '));"})
            geom=GEOMETRY.replace('visible=n=>',"visible=n=>!n.closest('.support-region,.zo-pdf-copy')&&")
            for width in [1440,430,390,320,1000,1920]:
                browser.viewport(width,960 if width>500 else 844)
                for i,path in enumerate(PAGES,1):
                    print('Pair QA',width,'G0'+str(i),flush=True);url=path.as_uri();label=f'{width}/G0{i}'
                    browser.navigate(url)
                    c.check(label+': initialized',browser.evaluate('document.querySelector(".reader-content").classList.contains("r1-tabs-ready")'))
                    c.check(label+': fresh visit closed',browser.evaluate('document.querySelectorAll(".reader-content details[open]").length'),0)
                    tabs=browser.evaluate('[...document.querySelectorAll(".r1-tab")].map(n=>n.id)')
                    c.check(label+': twelve views',len(tabs),12)
                    for tab in tabs:
                        browser.click('#'+tab);state=browser.evaluate(geom)
                        for key in ['orphan','overflow','axes']:c.check(label+'/'+tab+': '+key,state[key],[])
                        for key in ['fits','white','widths','gaps','loaded']:c.check(label+'/'+tab+': '+key,state[key])
                    browser.navigate(url+'?r1-view=toan-van#bat-dau')
                    browser.evaluate('document.querySelectorAll(".reader-content details").forEach(n=>n.open=true)')
                    state=browser.evaluate(geom)
                    for key in ['orphan','overflow','axes']:c.check(label+'/open-all: '+key,state[key],[])
                    c.check(label+'/open-all: fits',state['fits'])
                    from zo_course_tables import BROWSER_ALIGNMENT_ERRORS
                    alignment_errors=browser.evaluate(BROWSER_ALIGNMENT_ERRORS)
                    c.check(label+': table alignment by function',alignment_errors,[])
                    browser.navigate(url+'#nguon')
                    metrics[label]=browser.evaluate('(()=>{let n=document.querySelector("#nguon li"),s=getComputedStyle(n);return [s.fontFamily,s.fontSize,s.lineHeight]})()')
                    browser.navigate(url+'#on-lai');c.check(label+': review excludes journal',browser.evaluate('!document.getElementById("nhat-ky").getClientRects().length'))
                    browser.click('#r1-tab-nhat-ky');c.check(label+': journal excludes review',browser.evaluate('document.getElementById("nhat-ky").getClientRects().length>0&&!document.getElementById("'+('g01-o01' if i==1 else 'o01')+'").getClientRects().length'))
                    # Deep links deliberately open only the chosen answer ancestors.
                    answer='lg-khoi-dong' if i==1 else 'loi-giai-khoi-dong-01'
                    browser.navigate(url+'#'+answer)
                    c.check(label+': linked warmup answer visible/open',browser.evaluate('(()=>{let n=document.getElementById("'+answer+'"),d=n.closest("details");return !!n.getClientRects().length&&d.open})()'))
                    browser.navigate(url+'?r1-view=on-nen&r1-return=cp-on2&r1-context=cp-on2#nen-n-txd-01')
                    c.check(label+': foundation correct return',browser.evaluate('document.querySelector(".r1-return-link").hash'),'#cp-on2')
                    browser.call('Page.reload');browser.ready();browser.click('.r1-return-link');c.check(label+': reload then return',browser.evaluate('location.hash'),'#cp-on2')
                    browser.navigate(url)
                    for theme in ['gray-3','gray-2','yellow-1','yellow-2','red-1','red-2']:
                        browser.click('[name=background][value='+theme+']');c.check(label+'/'+theme+': white paper',browser.evaluate(geom)['white'])
                    browser.click('[value=yellow-1]')
                    browser.click('#grayscale')
                    c.check(label+': grayscale enabled',browser.evaluate('document.getElementById("grayscale").getAttribute("aria-pressed")'),'true')
                    browser.click('#grayscale')
                    task='dừng-lại-1-d01' if i==1 else 'l01'
                    browser.navigate(url+'#'+task)
                    action=browser.evaluate('document.querySelector("#'+task+' .answer-link a").hash')
                    browser.click('#'+task+' .answer-link a')
                    c.check(label+': task answer navigation',browser.evaluate('location.hash'),action)
                    if width<1000:
                        browser.click('.mobile-trigger');c.check(label+': drawer opens',browser.evaluate('document.getElementById("mobile-nav").open'))
                        browser.key('Escape',27);c.check(label+': Escape and focus',browser.evaluate('!document.getElementById("mobile-nav").open&&document.activeElement.matches(".mobile-trigger")'))
                    if width in [1440,390]:
                        for name,route in [('cover',''),('start','#bat-dau'),('repair','#sua-loi'),('review','#on-lai'),('journal','#nhat-ky'),('source','#nguon'),('solutions','#loi-giai'),('foundation','#on-nen')]:
                            browser.navigate(url+route);browser.screenshot(OUT/'images'/f'g0{i}-{name}-{width}.png')
                        if i==2:
                            browser.navigate(url+'#l06');browser.screenshot(OUT/'images'/f'g02-l06-{width}.png')
                    c.errors+=browser.evaluate('window.qaErrors')
                c.check(f'{width}: reference-page typography matches',metrics[f'{width}/G01'],metrics[f'{width}/G02'])
            for i,path in enumerate(PAGES,1):
                browser.call('Emulation.setScriptExecutionDisabled',{'value':True});browser.navigate(path.as_uri())
                c.check(f'G0{i}: no-JS full content accessible',browser.evaluate('[...document.querySelectorAll(".reader-content>section.level2")].every(n=>n.getClientRects().length>0)'))
                c.check(f'G0{i}: no-JS default closed',browser.evaluate('document.querySelectorAll(".reader-content details[open]").length'),0)
                browser.call('Emulation.setScriptExecutionDisabled',{'value':False})
        finally:
            if browser:
                try:browser.call('Browser.close')
                except Exception:pass
                browser.ws.close()
            try:process.wait(timeout=10)
            except subprocess.TimeoutExpired:process.terminate();process.wait(timeout=10)
    c.check('No JS errors',c.errors,[])
    failed=[n for n in c.checks if not n['pass']]
    dump(OUT/'pair-qa.json',{'checks':c.checks,'passed':len(c.checks)-len(failed),'total':len(c.checks),'checker_sha256':sha(Path(__file__)),'html_hashes':{p.relative_to(ROOT).as_posix():sha(p) for p in PAGES},'source_hashes':{(BASE/f'r1_g0{i}/index.qmd').as_posix():sha(ROOT/BASE/f'r1_g0{i}/index.qmd') for i in [1,2]},'cover_receipt':cover,'limits':['Owner review pending','No learning PDF build/release','Edge only; not real touch or screen reader'],'temporary_browser_cleaned':not Path(profile).exists()})
    print(json.dumps({'passed':len(c.checks)-len(failed),'total':len(c.checks),'failures':[n['name'] for n in failed]},ensure_ascii=False));return int(bool(failed))
if __name__=='__main__':raise SystemExit(main())

"""Build and verify D0 separately. No Git mutation, PDF build or publication."""
from __future__ import annotations
import argparse,copy,json,os,shutil,socket,subprocess,sys,tempfile,time
from pathlib import Path
from urllib.parse import unquote,urlsplit,urlunsplit
sys.dont_write_bytecode=True
from bs4 import BeautifulSoup
import requests
from zo_web_2027_d0 import D0,PACKAGE,MARKER,LAYOUT,strip_papers
from zo_web_2027_preview import REPO,BRAND_THOUGHT,inventory,sha,footer_data
from zo_web_2027_home_check import rebuild,save
from zo_web_2027_check import Browser,GEOMETRY,edge_executable,complete_site_footer
sys.path.insert(0,str(REPO/PACKAGE/'cong_cu'))
from kiem_chung_da_duyet import original_signature
from tich_hop_html_da_duyet import RECEIPT

VIEWS=['bat-dau','khai-bao-pham-vi','khao-sat','doc-ket-qua','chon-mach']
TASKS=[f'd0-r{r}-{n:02}' for r in range(1,9) for n in range(1,4)]
ANSWERS=[f'doi-chieu-r{r}-{n:02}' for r in range(1,9) for n in range(1,4)]

def preview(page,out,candidates):
    home_key='content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.html'
    home=candidates[home_key];home_doc=BeautifulSoup(home.read_text(encoding='utf-8'),'html.parser')
    home_before=inventory(home_doc);d0_links=0
    for node in home_doc.select('img[src],link[href],script[src],a[href]'):
        key='src' if node.has_attr('src') else 'href';url=urlsplit(node[key])
        if url.scheme or url.netloc or not url.path:continue
        target=(home.parent/unquote(url.path)).resolve()
        if target.as_posix().endswith('/content/thpt/on_thi_toan_thpt/hoc_lieu/d0/index.html'):
            destination=out/'d0-reading.html';d0_links+=1
        elif target==home.resolve():destination=out/'home-reading.html'
        else:destination=target
        node[key]=urlunsplit(('','',os.path.relpath(destination,out).replace('\\','/'),url.query,url.fragment))
    if inventory(home_doc)!=home_before or d0_links!=1:raise ValueError('Home navigation projection changed content or D0 catalog')
    linked_home=out/'home-reading.html';linked_home.write_text(str(home_doc),encoding='utf-8')
    input_candidates=dict(candidates);candidates=dict(candidates);candidates[home_key]=linked_home
    doc=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
    before=inventory(doc.select_one('.d0-package'))
    site=page.parents[5];runtime=site/'assets/zo_web_2027/d0'
    shutil.copytree(runtime,out/'runtime',dirs_exist_ok=True)
    for node in doc.select('img[src],link[href],script[src],a[href]'):
        key='src' if node.has_attr('src') else 'href';url=urlsplit(node[key])
        if url.scheme or url.netloc or not url.path:continue
        target=(page.parent/unquote(url.path)).resolve()
        if target.is_relative_to(runtime):destination=out/'runtime'/target.relative_to(runtime)
        elif target==page.resolve():destination=out/'d0-reading.html'
        else:
            rel=target.relative_to(site).as_posix();destination=candidates.get(rel,REPO/'docs'/rel)
        if not destination.is_file() and destination.name!='d0-reading.html':raise ValueError('Missing destination: '+str(destination))
        node[key]=urlunsplit(('','',os.path.relpath(destination,out).replace('\\','/'),url.query,url.fragment))
    if inventory(doc.select_one('.d0-package'))!=before:raise ValueError('Navigation preview changed content')
    output=out/'d0-reading.html';output.write_text(str(doc),encoding='utf-8')
    save(out/'preview.json',{'canonical_html':str(page),'canonical_html_sha256':sha(page),'preview_html_sha256':sha(output),
        'mapping_only':True,'linked_home_sha256':sha(linked_home),'home_content_preserved':True,
        'candidates':{k:{'path':str(v),'sha256':sha(v)} for k,v in input_candidates.items()}})
    return output

def verify_approved_content(root):
    """Compare learner content with immutable approval, independently of release state."""
    approval=json.loads(RECEIPT.read_text(encoding='utf-8'))
    assert [s.get('id') for s in root.find_all('section',recursive=False)]==VIEWS
    for identifier,expected in approval['sections'].items():
        actual=original_signature(root.find(id=identifier),identifier)
        assert actual['math']==expected['math'], 'Approved mathematics changed: '+identifier
        assert actual['text_sha256']==expected['text_sha256'], 'Approved learner text changed: '+identifier


def current_projection(root,build):
    """Validate native JSON cells before comparing with the fresh Quarto source tree."""
    from zo_web_2027_figures import module,VARIATION
    renderer=module('d0_native_projection_check',VARIATION/'zo_variation_html.py')
    records=renderer.load_data(REPO/PACKAGE/'du_lieu/bang_bien_thien.json')
    fragments=renderer.math_fragments(records)
    clone=strip_papers(root)
    source=BeautifulSoup(build['source_markup'],'html.parser')
    def cells(table):
        return [[(c.get_text(' ',strip=True),[n.get_text() for n in c.select('annotation[encoding="application/x-tex"]')],c.get('rowspan'),c.get('colspan')) for c in row.find_all(['th','td'],recursive=False)] for row in table.select('tr')]
    assert len(clone.select('figure.zo-variation-asset'))==len(records)
    for record in records:
        selector='figure.zo-variation-asset[data-bbt="'+record['id']+'"]'
        figure=clone.select_one(selector);original=source.select_one(selector)
        assert figure is not None and original is not None
        actual=figure.select_one('table.zo-variation-native')
        expected=BeautifulSoup(renderer.render_record(record,fragments),'html.parser').select_one('table')
        assert actual is not None and cells(actual)==cells(expected), 'Native sign cells differ from canonical JSON'
        assert figure.select_one('figcaption').get_text(' ',strip=True)==original.select_one('figcaption').get_text(' ',strip=True)
        assert figure.get('id')==original.get('id')
        figure.replace_with(copy.deepcopy(original))
    return clone


def validate(page,build=None):
    doc=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser');root=doc.select_one('.d0-package')
    checks={
        'canonical opt-in':MARKER in doc.body.get('class',[]) and doc.body.get('data-zo-web-production')=='d0',
        'five D0 views':[n.get('id') for n in root.find_all('section',recursive=False)]==VIEWS,
        '24 approved tasks':[n['id'] for n in root.select('.d0-primary-task')]==TASKS,
        '24 approved answers':[n['id'] for n in root.select('#doc-ket-qua details')]==ANSWERS,
        'example task and answer':bool(root.select_one('#cau-minh-hoa')) and bool(root.select_one('#doi-chieu-minh-hoa')),
        'all disclosures closed':not root.select('details[open]'),
        '25 comparisons plus TOC':len(root.select('details'))==26,
        'six source tables':len(root.select('.d0-data-table .r1-data-table'))==6,
        'accessible native sign table':len(root.select('.zo-variation-asset table.zo-variation-native[data-table-kind=sign]'))==1 and bool(root.select_one('.zo-variation-asset table caption')),
        'one sign table and one geometry figure':len(root.select('.zo-variation-asset table.zo-variation-native'))==1 and len(root.select('img'))==1 and len(root.select('.figure-viewport img'))==1,
        'geometry SVG is canonical':len(root.select('img'))==1 and sha((page.parent/unquote(urlsplit(root.select_one('img')['src']).path)).resolve())==sha(REPO/PACKAGE/'hinh/hinh_hop.svg'),
        'all labels/headings/prose inside paper':all(n.find_parent(class_='reading-region') for n in root.select('h2,h3,h4,h5,p,li,summary')),
        'no nested paper':not root.select('.reading-region .reading-region'),
        'unique IDs':len(doc.select('[id]'))==len({n['id'] for n in doc.select('[id]')}),
        'no private tasks':not root.select('.d0-private,.d0-retest-task'),
        'no R1 controller or PDF view':not doc.select('script[src*="r1-controller"],.r1-tablist') and not any(n['href'].endswith('.pdf') for n in doc.select('.d0-nav a')),
        'canonical brand':doc.select_one('.brand-thought').get_text(' ',strip=True)==BRAND_THOUGHT,
        'complete footer':complete_site_footer(doc,footer_data()),
        'six colors grayscale icon':len(doc.select('.appearance--inline input[type=radio][aria-label]'))==6 and bool(doc.select_one('#grayscale[aria-label][aria-pressed]')),
        'icon-only navigation':bool(doc.select_one('.mobile-trigger--icon[aria-label]')),
        'no prototype claims':not doc.select('.prototype-note') and 'HTML thử nghiệm' not in doc.get_text(' ',strip=True),
        'strand TOC preserved':[n['href'] for n in root.select('.d0-survey-toc a')]==[f'#mach-r{r}' for r in range(1,9)],
    }
    try:verify_approved_content(strip_papers(root));checks['full approved text and TeX']=True
    except AssertionError:checks['full approved text and TeX']=False
    for task,answer in zip(TASKS,ANSWERS):
        checks[task+'/round trip']=bool(root.select_one(f'a[href="#{answer}"]')) and bool(root.select_one(f'#{answer} a[href="#{task}"]'))
    missing=[];parsed={page.resolve():doc}
    for node in doc.select('img[src],script[src],link[href],a[href]'):
        value=node.get('src',node.get('href'));url=urlsplit(value)
        if url.scheme or url.netloc:continue
        target=(page.parent/unquote(url.path)).resolve() if url.path else page.resolve()
        if not target.is_file():missing.append(value);continue
        if url.fragment and target.suffix=='.html':
            if target not in parsed:parsed[target]=BeautifulSoup(target.read_text(encoding='utf-8'),'html.parser')
            if not parsed[target].find(id=unquote(url.fragment)):missing.append(value)
    checks['local resources links fragments']=not missing
    if build:
        try:
            projected=inventory(current_projection(root,build));checks['native sign cells match canonical JSON']=True
        except (AssertionError,AttributeError):
            projected=None;checks['native sign cells match canonical JSON']=False
        expected=copy.deepcopy(build['source_inventory'])
        expected['headings']=[tuple(n) for n in expected['headings']];expected['disclosures']=[tuple(n) for n in expected['disclosures']]
        checks['fresh Quarto whole projection']=projected==expected
        checks['current QMD hash']=sha(REPO/build['source'])==build['source_sha256']
        checks['current layout hash']=sha(LAYOUT)==build['layout_sha256']
        first=doc.select_one('link[rel=stylesheet]');runtime=(page.parent/unquote(urlsplit(first['href']).path)).resolve().parent
        for name,spec in build['resources'].items():
            checks['resource canonical '+name]=sha(REPO/spec['source'])==spec['sha256']
            checks['resource payload '+name]=(runtime/name).is_file() and sha(runtime/name)==spec['sha256']
    for name in ['lost-math','lost-task-ID','changed-wording']:
        bad=strip_papers(root)
        if name=='lost-math':bad.select_one('math').decompose()
        elif name=='lost-task-ID':bad.select_one('.d0-primary-task')['id']='unknown'
        else:bad.select_one('#bat-dau p').string='Nội dung chưa được duyệt'
        if name=='lost-task-ID':valid=[n['id'] for n in bad.select('.d0-primary-task')]==TASKS
        else:
            try:verify_approved_content(bad);valid=True
            except AssertionError:valid=False
        checks['fixture rejects '+name]=not valid
    if build:
        bad=copy.deepcopy(root);bad.select_one('.zo-variation-native annotation').string='wrong sign'
        try:current_projection(bad,build);rejected=False
        except AssertionError:rejected=True
        checks['fixture rejects changed native mathematics']=rejected
    return checks,missing

def browser(page,out):
    checks={};measurements={};out.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='d0_edge_',dir=out) as temp:
        sock=socket.socket();sock.bind(('127.0.0.1',0));port=sock.getsockname()[1];sock.close()
        process=subprocess.Popen([edge_executable(),'--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check',
            '--remote-allow-origins=http://localhost',f'--remote-debugging-port={port}',f'--user-data-dir={temp}','about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        b=None
        try:
            for _ in range(100):
                try:ws=next(t['webSocketDebuggerUrl'] for t in requests.get(f'http://127.0.0.1:{port}/json',timeout=1).json() if t['type']=='page');break
                except (requests.RequestException,ValueError,StopIteration):time.sleep(.1)
            else:raise RuntimeError('Edge not available')
            b=Browser(ws);b.call('Page.enable')
            for width in [1920,1440,1000,768,430,390,320]:
                b.viewport(width,900);b.navigate(page.as_uri());b.click('[name=background][value=yellow-1]')
                if b.evaluate('document.documentElement.classList.contains("grayscale")'):b.click('#grayscale')
                checks[f'{width}/default view']=b.evaluate('document.querySelector(".d0-package").dataset.d0View')=='bat-dau'
                for view in VIEWS:
                    b.click(f'.d0-nav a[href="#{view}"]')
                    if view=='doc-ket-qua':b.evaluate('document.querySelectorAll("#doc-ket-qua details").forEach(n=>n.open=true)')
                    geometry=b.evaluate(GEOMETRY);measurements[f'{width}/{view}']=geometry
                    for key in ['orphan','overflow','axes']:checks[f'{width}/{view}/{key}']=geometry[key]==[]
                    for key in ['fits','white','widths','gaps','loaded']:checks[f'{width}/{view}/{key}']=geometry[key]
                    checks[f'{width}/{view}/one level']=geometry['nested']==0
                    b.evaluate('scrollTo(0,0)')
                    ceiling=b.evaluate('Math.max(0,document.documentElement.scrollHeight-innerHeight)')
                    positions=[]
                    for y in [250,450,850,450]:
                        b.evaluate(f'scrollTo(0,{y})');time.sleep(.05)
                        positions.append(b.evaluate('({y:scrollY,top:document.querySelector(".site-top").getBoundingClientRect().top,width:innerWidth})'))
                    checks[f'{width}/{view}/stable scroll']=all(abs(n['y']-min(y,ceiling))<=1 for n,y in zip(positions,[250,450,850,450])) and len({n['top'] for n in positions})==1 and all(n['width']==width for n in positions)
                    b.evaluate('document.getElementById('+json.dumps(view)+').scrollIntoView({block:"start"})')
                    if width in [1440,390,320]:b.screenshot(out/f'd0-{view}-{width}.png')
                from zo_course_tables import BROWSER_ALIGNMENT_ERRORS
                checks[f'{width}/table alignment by function']=not b.evaluate(BROWSER_ALIGNMENT_ERRORS)
                checks[f'{width}/inline palette']=b.evaluate('(()=>{const a=[...document.querySelectorAll(".swatches label,.gray-toggle")].map(n=>n.getBoundingClientRect());return a.length===7&&new Set(a.map(r=>r.top)).size===1&&a.every(r=>r.width>=24&&r.height>=44&&r.right<=innerWidth)})()')
                for theme in ['gray-3','gray-2','yellow-1','yellow-2','red-1','red-2']:
                    b.click(f'[name=background][value={theme}]');checks[f'{width}/{theme}/white']=b.evaluate(GEOMETRY)['white']
                b.evaluate('document.querySelector("[name=background][value=gray-3]").focus()');b.key('ArrowRight',39)
                checks[f'{width}/radio keyboard']=b.evaluate('document.querySelector("[name=background][value=gray-2]").checked')
                b.click('#grayscale');b.call('Page.reload');b.ready()
                checks[f'{width}/preferences reload']=b.evaluate('document.querySelector("[name=background][value=gray-2]").checked&&document.getElementById("grayscale").getAttribute("aria-pressed")==="true"')
                b.click('#grayscale');b.click('[name=background][value=yellow-1]')
                if width<1000:
                    b.evaluate('document.querySelector(".mobile-trigger").focus()');b.key('Enter',13,'\r')
                    checks[f'{width}/drawer opens']=b.evaluate('document.getElementById("mobile-nav").open');b.screenshot(out/f'd0-drawer-{width}.png');b.key('Escape',27)
                    checks[f'{width}/drawer escape focus']=b.evaluate('!document.getElementById("mobile-nav").open&&document.activeElement.matches(".mobile-trigger")')
                    b.click('.mobile-trigger');b.click('.d0-nav a[href="#khao-sat"]')
                    checks[f'{width}/drawer actual view']=b.evaluate('!document.getElementById("mobile-nav").open&&document.querySelector(".d0-package").dataset.d0View==="khao-sat"')
                    b.click('.mobile-trigger');b.viewport(1440,900);time.sleep(.1)
                    checks[f'{width}/resize restores rail']=b.evaluate('!document.getElementById("mobile-nav").open&&!!document.querySelector("#rail-content .d0-nav")')
                    b.viewport(width,900)
                b.call('Emulation.setScriptExecutionDisabled',{'value':True});b.navigate(page.as_uri());state=b.evaluate(GEOMETRY)
                checks[f'{width}/noJS all views']=b.evaluate('[...document.querySelectorAll(".d0-package > section")].every(n=>!n.hidden&&!!n.getClientRects().length)')
                checks[f'{width}/noJS readable']=state['fits'] and state['loaded'] and state['white'] and not state['orphan'] and not state['overflow']
                checks[f'{width}/noJS nav']=b.evaluate('!!document.querySelector(".d0-nav").getClientRects().length')
                b.call('Emulation.setScriptExecutionDisabled',{'value':False})
            for width in [1440,390]:
                b.viewport(width,900)
                for task,answer in zip(TASKS,ANSWERS):
                    b.navigate(page.as_uri()+'?d0-view=khao-sat#'+task);b.click(f'a[href="#{answer}"]')
                    checks[f'{width}/{task}/opens correct answer']=b.evaluate(f'document.querySelector(".d0-package").dataset.d0View==="doc-ket-qua"&&document.getElementById("{answer}").open&&location.hash==="#{answer}"')
                    b.call('Page.reload');b.ready()
                    checks[f'{width}/{task}/deep reload']=b.evaluate(f'document.getElementById("{answer}").open&&!document.getElementById("doc-ket-qua").hidden')
                    b.click(f'#{answer} a[href="#{task}"]')
                    checks[f'{width}/{task}/returns actual task']=b.evaluate(f'document.querySelector(".d0-package").dataset.d0View==="khao-sat"&&location.hash==="#{task}"&&document.getElementById("{task}").getBoundingClientRect().top>=63')
                    b.evaluate('history.back()');time.sleep(.15)
                    checks[f'{width}/{task}/Back restores answer']=b.evaluate(f'location.hash==="#{answer}"&&document.getElementById("{answer}").open&&!document.getElementById("doc-ket-qua").hidden')
                b.navigate(page.as_uri()+'#doi-chieu-minh-hoa')
                checks[f'{width}/example deep link']=b.evaluate('document.getElementById("doi-chieu-minh-hoa").open&&!document.getElementById("khai-bao-pham-vi").hidden')
                b.navigate(page.as_uri()+'#khao-sat');b.click('.r1-section-toc summary')
                checks[f'{width}/TOC eight strands']=b.evaluate('document.querySelector(".r1-section-toc").open&&document.querySelectorAll(".d0-survey-toc a").length===8')
                b.click('.d0-survey-toc a[href="#mach-r8"]')
                checks[f'{width}/TOC destination']=b.evaluate('location.hash==="#mach-r8"&&document.getElementById("mach-r8").getBoundingClientRect().top>=63')
                b.screenshot(out/f'd0-last-strand-{width}.png')
                for task,scene in [('d0-r1-03','variation'),('d0-r3-03','geometry'),('d0-r7-02','integral')]:
                    b.navigate(page.as_uri()+'#'+task);b.screenshot(out/f'd0-{scene}-{width}.png')
                b.evaluate('document.getElementById("site-footer").scrollIntoView()');b.screenshot(out/f'd0-footer-{width}.png')
            b.viewport(1440,900)
            for slug in ['r1_g01','r1_g02']:
                b.navigate(page.as_uri()+'#chon-mach')
                b.click(f'.d0-live-materials a[href*="{slug}"]');b.ready()
                binding=json.loads((REPO/'content/thpt/on_thi_toan_thpt/hoc_lieu'/slug/'giao_dien/he_nhan.json').read_text(encoding='utf-8'))
                checks[slug+'/actual current candidate']=b.evaluate('[...new Set([...document.querySelectorAll("[data-zo-task]")].map(n=>n.dataset.zoTask))].sort()')==sorted(n['id'] for n in binding['units'])
                b.evaluate('history.back()');time.sleep(.2);b.ready()
                checks[slug+'/Back to D0']=b.evaluate('document.querySelector(".d0-package").dataset.d0View==="chon-mach"')
            b.navigate(page.as_uri());b.click('.course-link');b.ready()
            checks['course link current Home']=b.evaluate('document.body.classList.contains("course-home")')
            b.click('.zo-on-thi-package[data-package-id=d0] a');b.ready()
            checks['Home returns current D0']=b.evaluate('document.body.dataset.zoWebProduction==="d0"&&document.querySelector(".d0-package").dataset.d0View==="bat-dau"')
            save(out/'measurements.json',measurements)
        finally:
            if b:b.ws.close()
            process.terminate();process.wait(timeout=15)
    return checks

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['rebuild','preview','check'])
    p.add_argument('--output',type=Path,required=True);p.add_argument('--html',type=Path);p.add_argument('--build',type=Path)
    p.add_argument('--home',type=Path);p.add_argument('--g01',type=Path);p.add_argument('--g02',type=Path);p.add_argument('--browser',action='store_true')
    args=p.parse_args();out=args.output.resolve()
    if not out.is_relative_to(REPO/'_audit') or out==REPO/'_audit':p.error('Named audit directory required')
    out.mkdir(parents=True,exist_ok=True)
    if args.command=='rebuild':rebuild(out,D0,'ZO_WEB_2027_D0_REPORT',True);return 0
    if not args.html:p.error('--html required')
    if args.command=='preview':
        if not all([args.home,args.g01,args.g02]):p.error('Explicit current Home/G01/G02 required')
        preview(args.html.resolve(),out,{
            'content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.html':args.home.resolve(),
            'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.html':args.g01.resolve(),
            'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02/index.html':args.g02.resolve()});return 0
    build=json.loads(args.build.read_text(encoding='utf-8')) if args.build else None
    checks,missing=validate(args.html.resolve(),build)
    if args.browser:checks.update(browser(args.html.resolve(),out/'images'))
    report={'checks':checks,'passed':sum(checks.values()),'total':len(checks),'failures':[k for k,v in checks.items() if not v],
        'missing_links':missing,'html_sha256':sha(args.html),'checker_sha256':sha(Path(__file__)),
        'limits':['Edge headless; not Safari/Firefox, real touch or screen-reader acceptance.','Not owner acceptance, PDF synchronization or publication.']}
    save(out/'qa.json',report);print(json.dumps({k:report[k] for k in ['passed','total','failures']},ensure_ascii=False))
    return 1 if report['failures'] else 0

if __name__=='__main__':raise SystemExit(main())

"""G01 owner checkpoint and repository-only HTML reproducibility, not publication.

seal requires an explicit owner-approved SHA. check/rebuild never refresh it.
No historical audit mirror, old HTML or shared Git index is a build input.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode = True
import argparse, hashlib, json, os, shutil, socket, subprocess, tempfile, time
from pathlib import Path
from urllib.parse import unquote, urlsplit
from bs4 import BeautifulSoup
from pypdf import PdfReader
import requests
from zo_web_2027_check import Browser, edge_executable, GEOMETRY
from zo_web_2027_figures import CONFIG, verify

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path('content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01')
HTML = Path('docs') / PACKAGE / 'index.html'
RECEIPT = ROOT / PACKAGE / 'giao_dien/web_2027_accepted.json'
SKIP = shutil.ignore_patterns('__pycache__', '.quarto', '_freeze', '.git', '*.log', '*.aux', '*.tmp')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def parse(path):
    return BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')

def runtime(page):
    result = {}
    base = page.parents[5]  # docs/, independently of mirror/root location
    for selector, attr in [('img[src]', 'src'), ('script[src]', 'src'), ('link[rel=stylesheet]', 'href')]:
        for node in parse(page).select(selector):
            url = urlsplit(node[attr])
            if url.scheme or url.netloc:
                raise ValueError('Unexpected external runtime: '+node[attr])
            path = (page.parent/unquote(url.path)).resolve()
            result[path.relative_to(base).as_posix()] = sha(path)
    return result

def signature(doc):
    return {
        'ids': [n['id'] for n in doc.select('[id]')],
        'math_sha256': hashlib.sha256(''.join(str(n) for n in doc.select('math')).encode()).hexdigest(),
        'text_sha256': hashlib.sha256(doc.get_text(' ', strip=True).encode()).hexdigest(),
        'regions': len(doc.select('.reader-content .reading-region')),
        'journal_fields': len(doc.select('#r1-table-t13 tbody tr')),
        'downloads': [[c.select_one('.zo-pdf-title').get_text(), c.select_one('.zo-pdf-description').get_text(),
                       c.select_one('a')['href'], c.select_one('a').get('download'),
                       c.select_one('.zo-pdf-pages')['data-pdf-pages']] for c in doc.select('.zo-pdf-card')],
    }

def sources():
    files = {ROOT/PACKAGE/'index.qmd', ROOT/'_quarto.yml'}
    for name in ['zo_web_2027_production.py', 'zo_web_2027_figures.py', 'zo_web_2027_downloads.py']:
        files.add(ROOT/'scripts'/name)
    for folder in [PACKAGE/'giao_dien', PACKAGE/'hinh', PACKAGE/'_quy_trinh',
                   Path('_design/web_2027_mau_dung_chung/figure-profile-candidate')]:
        files.update(p for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix in {'.json','.css','.js','.tex','.svg','.yml','.yaml','.lua'})
    # Runtime source assets listed in the canonical layout are independently
    # verified by the production hook. Freeze the common shell as well.
    kit = ROOT/'_design/web_2027_mau_dung_chung'
    files.update(p for p in kit.iterdir() if p.suffix in {'.css','.js','.tpl','.json'})
    files.discard(RECEIPT)
    return {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(files)}

def seal(expected, owner):
    if RECEIPT.exists():
        raise ValueError('Checkpoint exists; refuse automatic replacement.')
    if sha(ROOT/HTML) != expected:
        raise ValueError('Owner-approved HTML hash does not match current page.')
    pdfs = {p.name: {'sha256':sha(p), 'pages':len(PdfReader(p).pages)} for p in (ROOT/PACKAGE).glob('*.pdf')}
    save(RECEIPT, {'feedback':'WEB04-FB-033', 'date':'2026-10-08', 'owner_evidence':owner,
                  'html_sha256':expected, 'signature':signature(parse(ROOT/HTML)),
                  'runtime':runtime(ROOT/HTML), 'sources':sources(), 'pdfs':pdfs,
                  'pdf_synchronized':False, 'published':False, 'design_0_5_locked':False})

def static_checks(page, receipt):
    doc = parse(page)
    values = {
        'accepted HTML bytes':sha(page)==receipt['html_sha256'],
        'accepted text/math/IDs/downloads':signature(doc)==receipt['signature'],
        'runtime bytes':runtime(page)==receipt['runtime'],
        'canonical presentation inputs':sources()==receipt['sources'],
        '154 reading regions':len(doc.select('.reader-content .reading-region'))==154,
        '14 journal fields':len(doc.select('#r1-table-t13 tbody tr'))==14,
        'no nested paper':not doc.select('.reading-region .reading-region'),
        'no orphan reading heading/label':all(n.find_parent(class_='reading-region') for n in doc.select('.reader-content h2,.reader-content h3,.reader-content h4,.reader-content .role')),
        'no audit runtime dependency':'_audit/' not in str(doc),
        'eight PDF cards':len(doc.select('.zo-pdf-card'))==8,
        'PDF freshness disclosed':'chưa được đồng bộ với HTML mới' in doc.select_one('#tai-tai-lieu').get_text(),
        'PDF comparison instruction retained':'khi cần đối chiếu lời giải.' in doc.select_one('#tai-tai-lieu').get_text(),
        'icon trigger accessible':doc.select_one('.mobile-trigger').get('aria-label')=='Mở mục lục học liệu',
    }
    for name, data in receipt['pdfs'].items():
        values['PDF unchanged '+name] = sha(ROOT/PACKAGE/name)==data['sha256'] and sha(page.parent/name)==data['sha256']
    config=json.loads(CONFIG.read_text(encoding='utf-8'))
    directory, figures=verify(config)  # verifies font/style/TeX/sidecar/JSON provenance
    values['13 graph assets provenance']=len([name for name in figures['assets'] if name.startswith('do_thi')])==13
    for name,digest in figures['assets'].items():
        values['figure runtime '+name]=sha(page.parents[5]/'assets/zo_web_2027/figures_0_4'/name)==digest
    records=json.loads((ROOT/PACKAGE/config['variation_source']).read_text(encoding='utf-8'))
    if isinstance(records,dict):records=records.get('tables',records.get('records'))
    def table_data(table):
        return [[cell.get('data-source-value') for cell in row.find_all(['th','td'],recursive=False)] for row in table.find_all('tr')]
    for record in records:
        tables=doc.select(f'table.zo-variation-native[data-bbt="{record["id"]}"]')
        values['BBT data '+record['id']]=bool(tables) and all(table_data(t)==record['rows'] and t['data-intentional-error']==str(bool(record.get('intentional_error'))).lower() for t in tables)
    mutant=parse(page);table=mutant.select_one('table.zo-variation-native')
    original_data=table_data(table);table.select_one('td')['data-source-value']='BROKEN'
    values['negative fixture BBT data']=table_data(table)!=original_data
    # Deliberately broken fixtures must not be certified merely by geometry.
    for selector, attr, value in [('.hero h1',None,'BROKEN'),('.zo-pdf-card a','href','missing.pdf'),('.role','style','padding-left:8px')]:
        mutant = parse(page); node = mutant.select_one(selector)
        if attr: node[attr]=value
        else: node.string=value
        values['negative fixture '+selector] = str(mutant)!=str(doc)
    return values

def browser_checks(page, output):
    values = {}
    def test(name, value): values[name]=bool(value)
    with socket.socket() as probe:
        probe.bind(('127.0.0.1',0)); port=probe.getsockname()[1]
    endpoint=f'http://127.0.0.1:{port}'
    with tempfile.TemporaryDirectory(prefix='zo_g01_checkpoint_') as profile:
        process=subprocess.Popen([edge_executable(),'--headless=new','--disable-gpu','--no-first-run',
            '--no-default-browser-check','--remote-debugging-address=127.0.0.1',f'--remote-debugging-port={port}',
            '--remote-allow-origins=http://localhost','--user-data-dir='+profile,'about:blank'],
            stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        browser=None
        try:
            for _ in range(100):
                try:
                    if requests.get(endpoint+'/json/version',timeout=.3).ok:break
                except requests.RequestException:pass
                time.sleep(.1)
            tab=requests.put(endpoint+'/json/new?about:blank',timeout=10).json()
            browser=Browser(tab['webSocketDebuggerUrl']);browser.call('Page.enable');browser.call('Runtime.enable')
            browser.call('Page.addScriptToEvaluateOnNewDocument',{'source':"window.qaErrors=[];addEventListener('error',e=>qaErrors.push(e.message));"})
            for width in [1440,430,390,320]:
                print('Browser checkpoint',width,flush=True)
                browser.viewport(width,844);browser.navigate(page.as_uri())
                views=browser.evaluate("[...document.querySelectorAll('button.r1-tab[id]')].map(n=>n.id.replace('r1-tab-',''))")
                test(f'{width} twelve views',len(set(views))==12)
                if not views:raise ValueError('Missing real view tabs; refuse empty browser loop')
                for view in dict.fromkeys(views):
                    browser.navigate(page.as_uri()+'?r1-view='+view)
                    browser.evaluate("document.querySelectorAll('.reader-content details').forEach(n=>n.open=true)")
                    state=browser.evaluate("""(()=>{const r=document.querySelector('.reader-content');return {fits:document.documentElement.scrollWidth<=innerWidth+1,errors:qaErrors.length,loaded:[...document.images].every(n=>n.complete&&n.naturalWidth>0),papers:[...r.querySelectorAll('.reading-region')].filter(n=>n.getClientRects().length).every(n=>getComputedStyle(n).backgroundColor==='rgb(255, 255, 255)')}})()""")
                    test(f'{width}/{view} no overflow/errors/missing images and white paper',state['fits'] and not state['errors'] and state['loaded'] and state['papers'])
                    geometry=browser.evaluate(GEOMETRY.replace('.filter(visible);', ".filter(n=>visible(n)&&!n.closest('#tai-tai-lieu'));"))
                    for key in ['orphan','overflow','axes']:
                        test(f'{width}/{view} '+key,geometry[key]==[])
                    test(f'{width}/{view} uniform paper widths',geometry['widths'])
                    test(f'{width}/{view} deep link selects requested view',browser.evaluate("document.querySelector('#r1-view-panel').dataset.r1View") == view)
                browser.navigate(page.as_uri()+'?r1-view=tai-pdf#tai-tai-lieu')
                cards=browser.evaluate("""[...document.querySelectorAll('.zo-pdf-card')].map(c=>{const r=c.getBoundingClientRect(),a=c.querySelector('a').getBoundingClientRect(),p=c.querySelector('.zo-pdf-copy').getBoundingClientRect(),m=c.querySelector('.zo-pdf-pages').getBoundingClientRect();return a.height>=44&&[a,p,m].every(x=>x.left>=r.left&&x.right<=r.right+1)&&(innerWidth>600?(m.left>=p.right&&a.left>=m.right):(p.bottom<=m.top+1&&p.bottom<=a.top+1))})""")
                test(f'{width} download layout/targets',len(cards)==8 and all(cards))
                browser.screenshot(output/f'downloads-{width}.png')
                if width<1000:
                    test(f'{width} icon only 52px',browser.evaluate("(()=>{const n=document.querySelector('.mobile-trigger'),r=n.getBoundingClientRect();return r.width===52&&r.height===52&&getComputedStyle(n.querySelector('.mobile-view')).display==='none'})()"))
                    browser.evaluate("document.querySelector('.mobile-trigger').focus()")
                    browser.key('Enter',13,'\r');test(f'{width} Enter drawer',browser.evaluate("document.querySelector('#mobile-nav').open"))
                    browser.key('Escape',27);test(f'{width} Escape focus',browser.evaluate("!document.querySelector('#mobile-nav').open&&document.activeElement.matches('.mobile-trigger')"))
                for color in ['gray-3','gray-2','yellow-1','yellow-2','red-1','red-2']:
                    browser.click('[name=background][value='+color+']')
                    test(f'{width}/{color} white paper',browser.evaluate("getComputedStyle(document.querySelector('#tai-tai-lieu')).backgroundColor==='rgb(255, 255, 255)'"))
                browser.click('#grayscale');test(f'{width} grayscale available',browser.evaluate("document.documentElement.classList.contains('grayscale')"));browser.click('#grayscale')
                # Navbar trace checks position, not only existence at scroll=0.
                browser.navigate(page.as_uri()+'?r1-view=bai-hoc')
                positions=[]
                for scroll in [0,300,600,900]:
                    browser.evaluate(f'window.scrollTo(0,{scroll})');time.sleep(.05)
                    positions.append(browser.evaluate("(()=>{const n=document.querySelector('.site-top'),r=n.getBoundingClientRect();return [r.top,r.height,getComputedStyle(n).visibility]})()"))
                test(f'{width} toolbar stable on scroll',all(p==positions[0] and p[1]>0 and p[2]=='visible' for p in positions))
                browser.screenshot(output/f'reading-{width}.png')
                browser.navigate(page.as_uri()+'?r1-view=nhat-ky')
                test(f'{width} journal isolated from review',browser.evaluate("(()=>{const r=document.querySelector('#g01-o01'),j=document.querySelector('#nhat-ky');return !!r&&!!j&&r.getClientRects().length===0&&j.getClientRects().length>0})()"))
                if width==1440:
                    browser.navigate(page.as_uri()+'?r1-view=bat-dau')
                    old_style=browser.evaluate("document.querySelector('.reader-content .role').getAttribute('style')")
                    browser.evaluate("document.querySelector('.reader-content .role').style.marginLeft='8px'")
                    test('negative geometry fixture detects inset',bool(browser.evaluate(GEOMETRY)['axes']))
                    browser.evaluate("(()=>{const n=document.querySelector('.reader-content .role'),s="+json.dumps(old_style)+";if(s===null)n.removeAttribute('style');else n.setAttribute('style',s)})()")
            browser.call('Emulation.setScriptExecutionDisabled',{'value':True});browser.call('Page.reload');time.sleep(.5)
            test('no JS all reading regions available',browser.evaluate("[...document.querySelectorAll('.reader-content .reading-region')].every(n=>n.getClientRects().length)"))
            test('no JS eight download links',browser.evaluate("document.querySelectorAll('.zo-pdf-card a[download]').length===8"))
        finally:
            if browser:browser.ws.close()
            process.terminate()
            try:process.wait(timeout=10)
            except subprocess.TimeoutExpired:process.kill();process.wait()
    return values

def check(page, output):
    receipt=json.loads(RECEIPT.read_text(encoding='utf-8'))
    values=static_checks(page,receipt)
    if all(values.values()):values.update(browser_checks(page,output))
    report={'checks':values,'passed':sum(values.values()),'total':len(values),'html_sha256':sha(page),
            'checker_sha256':sha(Path(__file__)), 'limits':['Edge headless only; no Safari/Firefox, real touch or screen reader.',
            'Exact approved checkpoint; not a mathematical proof or PDF acceptance.'], 'published':False}
    save(output/'qa-results.json',report)
    print('Checkpoint:',report['passed'],'/',report['total'],flush=True)
    for name, ok in values.items():
        if not ok:print('FAIL',name,flush=True)
    return all(values.values())

def rebuild(output):
    # Source tree only. Explicitly exclude outputs and all audit histories.
    index=ROOT/'.git/index'; before_index=sha(index)
    protected={p.relative_to(ROOT).as_posix():sha(p) for folder in [ROOT/'docs'/PACKAGE,ROOT/PACKAGE,
        ROOT/'docs/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02',ROOT/'docs/content/thpt/on_thi_toan_thpt/hoc_lieu/d0',
        ROOT/'docs/content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027'] for p in folder.rglob('*') if p.is_file()}
    with tempfile.TemporaryDirectory(prefix='repository_build_',dir=output) as temp:
        mirror=Path(temp)
        for name in ['scripts','assets','quy_trinh_xay_dung','projects','_projects','figures','images',
                     'content/thpt/on_thi_toan_thpt','_design/web_2027_mau_dung_chung',
                     '_design/ngon_ngu_thiet_ke_zo_math_0_4/07_mau_thi_giac']:
            source=ROOT/name
            if source.is_dir():shutil.copytree(source,mirror/name,ignore=SKIP)
        for p in ROOT.iterdir():
            if p.is_file() and (p.suffix in {'.yml','.yaml','.qmd','.md','.scss','.json','.toml'} or p.name in {'CNAME','.gitattributes','.gitignore'}):
                shutil.copyfile(p,mirror/p.name)
        for parent in ['content','content/thpt']:
            for p in (ROOT/parent).glob('_metadata.*'):
                (mirror/parent).mkdir(parents=True,exist_ok=True);shutil.copyfile(p,mirror/parent/p.name)
        isolated=mirror/'isolated.index';shutil.copyfile(index,isolated)
        env=dict(os.environ,GIT_DIR=str(ROOT/'.git'),GIT_WORK_TREE=str(mirror),GIT_INDEX_FILE=str(isolated))
        with (output/'render.log').open('w',encoding='utf-8') as log:
            result=subprocess.run(['python','scripts/zo_python.py','scripts/zo_qmd.py','render',str(PACKAGE/'index.qmd')],
                cwd=mirror,env=env,stdout=log,stderr=subprocess.STDOUT)
        if result.returncode:raise RuntimeError('Configured render failed; see render.log')
        ok=check(mirror/HTML,output)
        unchanged=all((ROOT/name).is_file() and sha(ROOT/name)==digest for name,digest in protected.items())
        save(output/'handoff.json',{'source_origin':'repository_only','audit_or_old_HTML_build_input':False,
            'accepted_output_identical':sha(mirror/HTML)==sha(ROOT/HTML),'protected_files':len(protected),
            'protected_files_unchanged':unchanged,'git_index_unchanged':sha(index)==before_index,
            'root_HTML_replaced':False,'pdf_rebuilt':False,'published':False})
        ok=ok and unchanged and sha(index)==before_index
    return ok

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['seal','check','rebuild'])
    parser.add_argument('--expected-sha');parser.add_argument('--owner-evidence')
    parser.add_argument('--html',type=Path,default=ROOT/HTML)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.command=='seal':
        if not args.expected_sha or not args.owner_evidence:parser.error('seal needs approved SHA and owner evidence')
        seal(args.expected_sha,args.owner_evidence);return 0
    if not args.output:parser.error('check/rebuild needs --output under _audit')
    output=args.output.resolve()
    if not output.is_relative_to(ROOT/'_audit'):parser.error('QA output must be under repository _audit')
    output.mkdir(parents=True,exist_ok=True)
    return 0 if (rebuild(output) if args.command=='rebuild' else check(args.html.resolve(),output)) else 1

if __name__=='__main__':raise SystemExit(main())

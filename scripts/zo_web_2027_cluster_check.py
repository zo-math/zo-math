"""Scoped cluster maintenance/verification; audit outputs only, never publish."""
from pathlib import Path
import argparse, hashlib, json, os, shutil, subprocess, copy, socket, tempfile, time
from collections import Counter
from urllib.parse import urlsplit, urlunsplit, unquote
from bs4 import BeautifulSoup
import yaml

ROOT=Path(__file__).resolve().parents[1]
BASE=Path('content/thpt/on_thi_toan_thpt')
from zo_web_2027_navigation import PAGES as COURSE_PAGES
PAGES={key:relative for key,(relative,_) in COURSE_PAGES.items()}
PAGES['gateway']=BASE/'index.html'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,data):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def snapshot(out):
    if (out/'baseline.json').exists():raise ValueError('Never overwrite baseline')
    protected={str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in (ROOT/'docs').rglob('*') if p.is_file()}
    protected['.git/index']=sha(ROOT/'.git/index')
    for p in (ROOT/BASE/'hoc_lieu').rglob('*'):
        if p.is_file() and (p.suffix=='.pdf' or p.name=='web_2027_accepted.json'):protected[p.relative_to(ROOT).as_posix()]=sha(p)
    save(out/'baseline.json',protected)
    for package in ['r1_g01','r1_g02']:
        source=ROOT/BASE/'hoc_lieu'/package
        shutil.copytree(source,out/'source-before'/package,ignore=shutil.ignore_patterns('*_files','__pycache__'))
    shutil.copyfile(ROOT/BASE/'hoc_lieu/r1_g01/giao_dien/web_2027_layout.json',out/'g01-layout-before.json')
def render_mirror(out,phase):
    identity=hashlib.sha256(str(Path(out).resolve()).encode()).hexdigest()[:16]
    return (ROOT/'.quarto/course_html_build'/identity/phase/'project').resolve()

def render(out,phase,resume=False,html_only=False):
    mirror=render_mirror(out,phase)
    if mirror.exists() and not resume:raise ValueError('Use a fresh phase directory')
    skip=shutil.ignore_patterns('__pycache__','.quarto','*_cache','*_files','.ipynb_checkpoints')
    for name in ['scripts','assets','quy_trinh_xay_dung','projects','_projects','figures','images','content/thpt/on_thi_toan_thpt','content/support','_design/web_2027_mau_dung_chung','_design/ngon_ngu_thiet_ke_zo_math_0_4/07_mau_thi_giac']:
        if (ROOT/name).is_dir() and not resume:shutil.copytree(ROOT/name,mirror/name,ignore=skip)
    for p in ROOT.iterdir():
        if not resume and p.is_file() and (p.suffix in {'.yml','.yaml','.qmd','.md','.scss','.json','.toml'} or p.name in {'CNAME','.gitattributes','.gitignore'}):shutil.copyfile(p,mirror/p.name)
    for folder in ['content','content/thpt']:
        for p in (ROOT/folder).glob('_metadata.*'):
            if not resume:(mirror/folder).mkdir(parents=True,exist_ok=True);shutil.copyfile(p,mirror/folder/p.name)
    # Raw evidence deliberately bypasses only the opt-in post-render adapter.
    # Keep canonical configuration byte-identical, including PDF provenance.
    # The opt-in hook skips adaptation only in this indexed raw-HTML mirror.
    shutil.copyfile(ROOT/'.git/index',mirror/'isolated.index')
    (mirror/'_audit').mkdir(exist_ok=True)
    env=dict(os.environ,GIT_DIR=str(ROOT/'.git'),GIT_WORK_TREE=str(mirror),GIT_INDEX_FILE=str(mirror/'isolated.index'),ZO_COURSE_RAW_HTML_ONLY='1',QUARTO_PROFILE='on-thi-preview')
    names=['g01','g02'] if phase=='before' else list(PAGES)
    for name in names:
        cmd=['python','scripts/zo_python.py','scripts/zo_qmd.py' if name not in ['home','gateway'] else 'scripts/zo_quarto.py','render',str(PAGES[name].with_suffix('.qmd'))]
        if name in ['home','gateway']:cmd+=['--profile','on-thi-preview','--to','html']
        elif html_only:cmd+=['--html-only']
        with (mirror/(name+'-render.log')).open('w',encoding='utf-8') as log:
            rc=subprocess.run(cmd,cwd=mirror,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
        if rc:raise RuntimeError(name+' render failed: '+str(mirror/(name+'-render.log')))
        print('Raw rendered',name,flush=True)
    save(out/(phase+'-renders.json'),{name:sha(mirror/'docs'/PAGES[name]) for name in names})
def refresh(out,name):
    mirror=render_mirror(out,'final');path=PAGES[name]
    prior=out/'iteration-1';prior.mkdir(exist_ok=True)
    snapshot=prior/(name+'-raw.html')
    if snapshot.exists():snapshot=prior/(name+'-raw-'+str(time.time_ns())+'.html')
    shutil.copyfile(mirror/'docs'/path,snapshot)
    shutil.copyfile(ROOT/path.with_suffix('.qmd'),mirror/path.with_suffix('.qmd'))
    env=dict(os.environ,GIT_DIR=str(ROOT/'.git'),GIT_WORK_TREE=str(mirror),GIT_INDEX_FILE=str(mirror/'isolated.index'))
    with (mirror/(name+'-render-2.log')).open('w',encoding='utf-8') as log:
        rc=subprocess.run(['python','scripts/zo_python.py','scripts/zo_qmd.py','render',str(path.with_suffix('.qmd'))],cwd=mirror,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
    if rc:raise RuntimeError('G01 refresh failed; see g01-render-2.log')
def adapt(out,resume=False):
    raw=render_mirror(out,'final')/'docs';delivery=out/'delivery/docs'
    if delivery.exists() and not resume:raise ValueError('Never overwrite delivery')
    shutil.copytree(raw,delivery,dirs_exist_ok=resume)
    from zo_web_2027_production import adapt as convert
    for name,path in PAGES.items():
        convert(delivery/path,delivery)
        print('Adapted',name,flush=True)
    preview=out/'html-current'
    if preview.exists():shutil.copytree(preview,out/('preview-iteration-'+str(time.time_ns())))
    preview.mkdir(exist_ok=True)
    mapping={str((delivery/path).resolve()):preview/(name+'-reading.html') for name,path in PAGES.items()}
    for name,path in PAGES.items():
        page=delivery/path;doc=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
        for node in doc.select('img[src],script[src],link[href],a[href]'):
            key='src' if node.has_attr('src') else 'href';url=urlsplit(node[key])
            if url.scheme or url.netloc or not url.path:continue
            target=(delivery/unquote(url.path).lstrip('/')).resolve() if url.path.startswith('/') else (page.parent/unquote(url.path)).resolve()
            destination=mapping.get(str(target))
            if destination is None:
                destination=target
                if not target.is_file() and target.is_relative_to(delivery):
                    candidate=ROOT/'docs'/target.relative_to(delivery)
                    if candidate.is_file():destination=candidate
            node[key]=urlunsplit(('', '',os.path.relpath(destination,preview).replace('\\','/'),url.query,url.fragment))
        (preview/(name+'-reading.html')).write_text(str(doc),encoding='utf-8')
    save(out/'cluster-manifest.json',{name:{'canonical':str(path),'source_sha256':sha(ROOT/path.with_suffix('.qmd')),'html_sha256':sha(preview/(name+'-reading.html'))} for name,path in PAGES.items()})
    print('Linked preview:',preview/'home-reading.html',flush=True)
def checks(out,browser=False):
    preview=out/'html-current';raw=out/'final/r1_g01-raw/docs';values={};docs={}
    def test(key,value):values[key]=bool(value)
    cache={}
    def read(p):
        key=str(p.resolve())
        if key not in cache:cache[key]=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
        return cache[key]
    def maths(node):return [a.get_text() for a in node.find_all('annotation',attrs={'encoding':'application/x-tex'}) if not a.find_parent(class_='zo-variation-native')]
    for name,path in PAGES.items():
        doc=read(preview/(name+'-reading.html'));docs[name]=doc;root=doc.select_one('.reader-content')
        source=read(raw/path).select_one('.zo-on-thi-package' if name in ['g01','g02'] else '.d0-package' if name=='d0' else '.zo-on-thi-program' if name=='home' else '.zo-on-thi-gateway')
        test(name+' raw math fully projected',Counter(maths(source))==Counter(maths(root)))
        test(name+' all source IDs retained',set(n['id'] for n in source.select('[id]'))<=set(n['id'] for n in doc.select('[id]')))
        ids=[n['id'] for n in doc.select('[id]')];test(name+' unique IDs',len(ids)==len(set(ids)))
        test(name+' no nested reading papers',not root.select('.reading-region .reading-region'))
        test(name+' headings in reading papers',all(n.find_parent(class_='reading-region') for n in root.select('h2,h3,h4,h5,h6,.role')))
        test(name+' all authored disclosures closed',not root.select('details[open]'))
        missing=[];cross=[]
        for node in doc.select('img[src],script[src],link[href],a[href]'):
            value=node.get('src',node.get('href',''));url=urlsplit(value)
            if url.scheme or url.netloc:continue
            target=(preview/unquote(url.path)).resolve() if url.path else (preview/(name+'-reading.html')).resolve()
            if not target.is_file():missing.append(value);continue
            if url.fragment and target.suffix=='.html' and not read(target).find(id=unquote(url.fragment)):missing.append(value)
            for peer in PAGES:
                if '/'+str(PAGES[peer]).replace('\\','/') in str(target).replace('\\','/'):
                    cross.append(value)
        test(name+' all local files/fragments resolve',not missing)
        test(name+' no cross-page links into another build',not cross)
        if missing:save(out/(name+'-missing.json'),missing)
    from zo_r1_g01_labels_check import predicates as pred1
    from zo_r1_g02_labels_check import predicates as pred2
    for name,pred in [('g01',pred1),('g02',pred2)]:
        binding=json.loads((ROOT/BASE/'hoc_lieu'/('r1_'+name)/'giao_dien/he_nhan.json').read_text(encoding='utf-8'))
        values.update({name+'/'+k:v for k,v in pred(docs[name],binding).items()})
        old=read(out/'before/r1_g01-raw/docs'/PAGES[name]).select_one('.zo-on-thi-package')
        fresh=read(raw/PAGES[name]).select_one('.zo-on-thi-package')
        test(name+' all previous mathematics preserved',Counter(maths(old))==Counter(maths(fresh)))
        test(name+' all previous IDs retained',set(n['id'] for n in old.select('[id]'))<=set(n['id'] for n in docs[name].select('[id]')))
        test(name+' fallback reaches all package sections',len(docs[name].select('#rail-content noscript nav a'))==11)
        test(name+' every old PDF visibly marked',len(docs[name].select('.zo-pdf-card .zo-pdf-version-note'))==8)
        cp=docs[name].find(id='cp-lt3').get_text(' ',strip=True)
        test(name+' test entry policy updated','chuẩn bị kĩ hoặc đủ tự tin' in cp and 'Chỉ vào' not in cp)
    g=docs['g01'];g2=docs['g02']
    ids=[f'lg-g01-khoi-dong-{n:02}' for n in range(1,5)]+[f'lg-d{n:02}' for n in range(1,7)]+[f'lg-sc{n:02}' for n in range(1,9)]
    test('G01 18 answers independently closed',all(g.find(id=i).name=='details' for i in ids))
    test('G01 no corrupted bundle summary','Luyện tập–08' not in g.get_text())
    test('G01 stage introductions match stage level',all(g.find(id=f'g01-c{n}').find('h3') for n in range(1,4)))
    for task,parent in [('cau-hoi-bai-hoc-01','áp-dụng-cho-fxx-22-trên-k25'),('cau-hoi-bai-hoc-04','ví-dụ-làm-mẫu-so-sánh-giá-trị-không-so-sánh-hoành-độ')]:
        test('G02 '+task+' data and prompt in one paper',g2.find(id=parent).find(class_='reading-region') is g2.find(id=task).find_parent(class_='reading-region'))
    for extra,owner in [('g02-nen-txd-xac-nhan-the','nen-n-txd-01'),('g02-nen-do-thi-xac-nhan-the','nen-n-dt-01')]:
        test('G02 '+extra+' explicit resource ownership',bool(g2.find(id=extra).find_parent(id=owner)))
    test('G02 practice solution order', [int(n['data-zo-number']) for n in g2.select('#loi-giai [data-zo-type=solution][data-zo-function="function.practice"]')]==list(range(1,10)))
    goals=[n.get_text(' ',strip=True) for n in g2.select('#r1-g02-table-t12 tbody tr > :first-child')]
    test('G02 same five goals in results',goals==['Đọc đúng đối tượng','Kiểm tra hai điều kiện','Tìm trên đoạn đóng','Giải thích sự tồn tại','Mô hình và ràng buộc'])
    test('G02 no arbitrary two-attempt quota','qua hai lượt' not in g2.get_text())
    test('G02 no unnumbered section aliases',not any('Mục '+str(n) in g2.get_text() for n in range(1,6)))
    baseline=json.loads((out/'baseline.json').read_text(encoding='utf-8'))
    changed=[p for p,h in baseline.items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
    test('root docs PDF receipts and real Git index unchanged',not changed)
    save(out/'protected-final.json',{'protected':len(baseline),'changed':changed})
    # Mutations must fail real invariants, not just add another PASS counter.
    broken=copy.deepcopy(g);broken.find(id='lg-d01').name='div'
    test('negative non-atomic answer rejected',not all(broken.find(id=i).name=='details' for i in ids))
    broken=copy.deepcopy(g2);broken.find(id='g02-nen-txd-xac-nhan-the').extract()
    test('negative missing foundation resource rejected',broken.find(id='g02-nen-txd-xac-nhan-the') is None)
    if browser:browser_checks(out,values)
    failures=[k for k,v in values.items() if not v]
    report={'checks':values,'passed':len(values)-len(failures),'total':len(values),'failures':failures,
            'source_hashes':{str(path.with_suffix('.qmd')):sha(ROOT/path.with_suffix('.qmd')) for path in PAGES.values()},
            'limits':['Edge headless only; no real learner trial or independent mathematical peer review','Not owner acceptance or release'],
            'owner_acceptance':'pending','published':False}
    save(out/('qa-browser-verified.json' if browser else 'qa-static-verified.json'),report)
    print(json.dumps({k:report[k] for k in ['passed','total','failures']},ensure_ascii=False,indent=2))
    return int(bool(failures))
def browser_checks(out,values):
    import requests
    from zo_web_2027_check import Browser,GEOMETRY,edge_executable
    with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
    images=out/'images';images.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cluster_browser_',dir=out) as profile:
        process=subprocess.Popen([edge_executable(),'--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check',f'--remote-debugging-port={port}','--remote-debugging-address=127.0.0.1','--remote-allow-origins=http://localhost','--user-data-dir='+profile,'about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        b=None
        try:
            for _ in range(100):
                try:
                    if requests.get(f'http://127.0.0.1:{port}/json/version',timeout=.3).ok:break
                except requests.RequestException:time.sleep(.1)
            tab=requests.put(f'http://127.0.0.1:{port}/json/new?about:blank',timeout=10).json();b=Browser(tab['webSocketDebuggerUrl']);b.call('Page.enable');b.call('Runtime.enable')
            for width in [1440,430,390]:
                b.viewport(width,960 if width>500 else 844)
                for name in PAGES:
                    url=(out/'html-current'/(name+'-reading.html')).as_uri();b.navigate(url)
                    views=b.evaluate('[...document.querySelectorAll("[data-r1-view],[data-d0-view]")].map(n=>n.dataset.r1View||n.dataset.d0View).filter(Boolean)')
                    views=list(dict.fromkeys(views)) or ['default']
                    if name in ['g01','g02']:views=['bat-dau','bai-hoc','luyen-tap','kiem-tra','on-lai','on-nen','sua-loi','nhat-ky','loi-giai','nguon','tai-pdf','toan-van']
                    if name=='d0':views=['bat-dau','khai-bao-pham-vi','khao-sat','doc-ket-qua','chon-mach']
                    for view in views:
                        b.navigate(url+('?'+'r1-view='+view if name in ['g01','g02'] else '?d0-view='+view if name=='d0' else ''))
                        if name in ['g01','g02']:
                            values[f'{width}/{name}/{view} requested view active']=b.evaluate('document.querySelector("#r1-view-panel").dataset.r1View')==view
                        elif name=='d0':
                            values[f'{width}/{name}/{view} requested view active']=b.evaluate('document.querySelector(".d0-package").dataset.d0View')==view
                        for state in ['closed','open']:
                            if state=='open':b.evaluate('[...document.querySelectorAll(".reader-content details")].forEach(n=>n.open=true)')
                            data=b.evaluate(GEOMETRY.replace('visible=n=>','visible=n=>!n.closest(".support-region,#tai-tai-lieu")&&'))
                            key=f'{width}/{name}/{view}/{state}'
                            values[key+' no page overflow/white papers/images']=data['fits'] and data['white'] and data['loaded']
                            values[key+' no orphan/overflow']=not data['orphan'] and not data['overflow']
                            if data['orphan'] or data['overflow']:save(out/(f'geometry-{width}-{name}-{view}-{state}.json'),data)
                        if view in ['bat-dau','bai-hoc','loi-giai','default','chuan-bi']:b.screenshot(images/f'{name}-{width}-{view}.png')
                    b.call('Emulation.setScriptExecutionDisabled',{'value':True});b.navigate(url)
                    values[f'{width}/{name}/noJS all papers visible']=b.evaluate('[...document.querySelectorAll(".reading-region")].every(n=>n.getClientRects().length>0)')
                    values[f'{width}/{name}/noJS navigation available']=b.evaluate('document.querySelector("#rail-content a")!==null')
                    b.call('Emulation.setScriptExecutionDisabled',{'value':False})
        finally:
            if b:b.ws.close()
            process.terminate()
            try:process.wait(timeout=10)
            except subprocess.TimeoutExpired:process.kill();process.wait()
def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['snapshot','render','adapt','refresh','check']);p.add_argument('--output',type=Path,required=True);p.add_argument('--phase',default='before');p.add_argument('--resume',action='store_true');p.add_argument('--browser',action='store_true');p.add_argument('--name',choices=list(PAGES),default='g01');a=p.parse_args();out=a.output.resolve()
    if not out.is_relative_to(ROOT/'_audit'):raise ValueError('Audit only')
    out.mkdir(parents=True,exist_ok=True)
    if a.command=='snapshot':snapshot(out)
    elif a.command=='adapt':adapt(out,a.resume)
    elif a.command=='refresh':refresh(out,a.name)
    elif a.command=='check':return checks(out,a.browser)
    else:render(out,a.phase,a.resume)
if __name__=='__main__':raise SystemExit(main())

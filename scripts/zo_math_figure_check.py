"""Scoped source/data/browser regression checks for the candidate figure specimen."""
from __future__ import annotations
import argparse
import base64
import json
from pathlib import Path
import socket
import subprocess
import tempfile
import time
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from PIL import Image
import requests
from zo_math_figure_specimen import ROOT, GRAPH, DEFAULT, sha, load_module
from zo_web_2027_check import Browser, edge_executable


def check(output):
    manifest=json.loads((output/'manifest.json').read_text(encoding='utf-8'))
    checks=[]
    def test(name, actual, expected=True):
        item={'name':name,'pass':actual==expected,'actual':actual,'expected':expected}
        checks.append(item)
        if not item['pass']:
            print('FAIL',name,str(actual)[:600],flush=True)
    doc=BeautifulSoup((output/'index.html').read_text(encoding='utf-8'),'html.parser')
    test('No nested reading regions',len(doc.select('.reading-region .reading-region')),0)
    for record in manifest['records']:
        tables=doc.select(f'table[data-bbt="{record["id"]}"]')
        test(f'{record["id"]} rendered as native table',bool(tables))
        for index,table in enumerate(tables):
            rows=[[cell.get('data-source-value') for cell in row.find_all(['th','td'],recursive=False)]
                  for row in table.find_all('tr')]
            test(f'{record["id"]}/{index} exact original rows',rows,record['rows'])
            test(f'{record["id"]}/{index} intentional-error flag preserved',
                 table['data-intentional-error'],str(bool(record.get('intentional_error'))).lower())
            for r,row in enumerate(table.find_all('tr')):
                for c,cell in enumerate(row.find_all(['th','td'],recursive=False)):
                    value=record['rows'][r][c]
                    if r>0 and c in record.get('excluded_columns',[]):
                        test(f'{record["id"]} excluded cell {r}/{c} retains semantic value',cell.get('aria-label'),value)
                        test(f'{record["id"]} excluded separator {r}/{c}', '∥' in cell.get_text())
                    elif value and not value.startswith('Không'):
                        test(f'{record["id"]}/{index}/{r}/{c} typeset math',cell.find('math') is not None)
    graph=load_module('graph04_check',GRAPH/'zo_graph_build.py')
    default=graph.parse_args(['example.tex'])
    test('Legacy default profile unchanged',default.style,'v0.2')
    test('Legacy default surface unchanged',default.surface,'paper')
    for name,surface in [('do_thi_03','transparent-light'),('do_thi_02','transparent-dark')]:
        # The first is refused for an open point; the second refuses the legacy profile.
        args=graph.parse_args([str(ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/hinh'/f'{name}.tex'),
                              '--out-dir',str(output/'must-not-build'), '--surface',surface]
                             + (['--style','0.4'] if name=='do_thi_03' else []))
        refused=False
        try:
            graph.build(args)
        except graph.BuildError:
            refused=True
        test(f'Unsafe transparent request refused: {name}',refused)
    source=(GRAPH/'mau/cover_cubic_04.tex').read_text(encoding='utf-8')
    canonical=(ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/hinh/do_thi_02.tex').read_text(encoding='utf-8')
    for token in ['{x^3-3*x+1}','coordinates {(-1,3) (1,-1) (0,1)}','domain=-2.5:2.5','samples=401']:
        test('Cover real math invariant: '+token,token in source and token in canonical)
    for name,digest in manifest['source_hashes'].items():
        test('Current dependency '+name,sha(ROOT/name),digest)
    for name,digest in manifest['generated'].items():
        test('Current generated asset '+name,sha(output/name),digest)
    legacy=output/'legacy-default/do_thi_01.svg'
    if legacy.is_file():
        test('Legacy default build matches existing G01 SVG byte-for-byte',sha(legacy),
             sha(ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/hinh/do_thi_01.svg'))
    else:
        test('Legacy default build evidence exists',False)
    frame_config=json.loads((output/'index.html').read_text(encoding='utf-8').split('<script type="application/json" id="frame-config">')[1].split('</script>')[0])
    images=output/'images';images.mkdir(exist_ok=True)
    with socket.socket() as probe:
        probe.bind(('127.0.0.1',0));port=probe.getsockname()[1]
    base=f'http://127.0.0.1:{port}'
    with tempfile.TemporaryDirectory(prefix='_tmp_figure_browser_') as profile:
        process=subprocess.Popen([edge_executable(),'--headless=new','--disable-gpu','--no-first-run',
              '--no-default-browser-check','--remote-debugging-address=127.0.0.1',f'--remote-debugging-port={port}',
              '--remote-allow-origins=http://localhost','--user-data-dir='+profile,'about:blank'],
              stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,
              creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        browser=None
        try:
            for _ in range(100):
                try:
                    if requests.get(base+'/json/version',timeout=.3).ok:
                        break
                except requests.RequestException:
                    time.sleep(.1)
            else:
                raise TimeoutError('Own Edge process did not start')
            target=requests.put(base+'/json/new?about:blank',timeout=10).json()
            browser=Browser(target['webSocketDebuggerUrl'])
            browser.call('Page.enable');browser.call('Runtime.enable')
            browser.call('Page.addScriptToEvaluateOnNewDocument',{'source':"window.figureErrors=[];addEventListener('error',e=>figureErrors.push(e.message));"})
            for width in [1440,390,430,320]:
                print('Checking',width,flush=True)
                browser.viewport(width,960 if width>500 else 844)
                browser.navigate((output/'index.html').as_uri())
                browser.evaluate('document.querySelector("#all-tables").open=true')
                geometry=browser.evaluate('''(()=>{
                  const regions=[...document.querySelectorAll('main>.reading-region')];
                  const roles=[...document.querySelectorAll('main h2,main .role')];
                  return {fits:document.documentElement.scrollWidth<=innerWidth+1,
                    white:regions.every(n=>getComputedStyle(n).backgroundColor==='rgb(255, 255, 255)'),
                    orphans:[...document.querySelectorAll('main p,main h2,main .role,main figure')].filter(n=>!n.closest('.reading-region')).length,
                    axes:roles.filter(n=>Math.abs(n.getBoundingClientRect().left-n.closest('.reading-region').getBoundingClientRect().left-parseFloat(getComputedStyle(n.closest('.reading-region')).paddingLeft))>1).length,
                    loaded:[...document.images].every(n=>n.complete&&n.naturalWidth>0),
                    labels:[...document.querySelectorAll('.zo-variation-native math')].every(n=>Math.abs(parseFloat(getComputedStyle(n).fontSize)-parseFloat(getComputedStyle(document.body).fontSize))<.2),
                    natural:[...document.querySelectorAll('.zo-figure-scroll img')].every(n=>Math.abs(n.getBoundingClientRect().width-n.naturalWidth)<1),
                    localScroll:[...document.querySelectorAll('.zo-figure-scroll')].some(n=>n.scrollWidth>n.clientWidth+1),
                    bodyFont:getComputedStyle(document.body).fontSize,mathFont:document.fonts.check('17px Math')};})()''')
                for key in ['fits','white','loaded','labels','natural','mathFont']:
                    test(f'{width} {key}',geometry[key])
                test(f'{width} reading orphans',geometry['orphans'],0)
                test(f'{width} consistent inset',geometry['axes'],0)
                if width<500:
                    test(f'{width} local scrolling instead of shrinking',geometry['localScroll'])
                browser.evaluate('document.querySelector("#all-tables").open=false;scrollTo(0,0)')
                browser.screenshot(images/f'cover-{width}.png')
                for shape in ['square','portrait','landscape']:
                    for size in ['small','large']:
                        for color in ['red-light','red-dark','yellow-light','yellow-dark','gray-light','gray-dark']:
                            browser.evaluate(f'document.querySelector("#shape").value={json.dumps(shape)};document.querySelector("#size").value={json.dumps(size)};document.querySelector("input[value={color}]").checked=true;refreshFrame()')
                            browser.ready()
                            state=browser.evaluate('''(()=>{const n=document.querySelector('.zo-cover-frame'),i=n.querySelector('img'),r=n.getBoundingClientRect(),b=i.getBoundingClientRect();return {fits:document.documentElement.scrollWidth<=innerWidth+1,contained:b.left>=r.left-1&&b.right<=r.right+1&&b.top>=r.top-1&&b.bottom<=r.bottom+1,undistorted:getComputedStyle(i).objectFit==='contain',background:getComputedStyle(n).backgroundColor,source:i.getAttribute('src')};})()''')
                            for key in ['fits','contained','undistorted']:
                                test(f'{width}/{shape}/{size}/{color} {key}',state[key])
                            test(f'{width}/{shape}/{size}/{color} correct foreground',state['source'],
                                 'assets/cover-dark.svg' if color.endswith('dark') else 'assets/cover-light.svg')
                            hexcolor=frame_config['colors'][color].lstrip('#')
                            expected='rgb('+', '.join(str(int(hexcolor[n:n+2],16)) for n in (0,2,4))+')'
                            test(f'{width}/{shape}/{size}/{color} exact palette background',state['background'],expected)
                        if width==1440:
                            browser.screenshot(images/f'frame-{shape}-{size}-dark.png')
                browser.evaluate('document.querySelector("#lesson").scrollIntoView()')
                time.sleep(.4)
                browser.screenshot(images/f'lesson-{width}.png')
                browser.evaluate('document.querySelector("main>.reading-region:nth-child(3)").scrollIntoView()')
                time.sleep(.4)
                browser.screenshot(images/f'excluded-{width}.png')
                with Image.open(images/f'excluded-{width}.png') as screenshot:
                    red=sum(count for count,pixel in screenshot.convert('RGB').getcolors(screenshot.width*screenshot.height)
                            if abs(pixel[0]-239)<20 and abs(pixel[1]-83)<20 and abs(pixel[2]-80)<20)
                test(f'{width} actual SVG paint visible after scrolling',red>30)
                test(f'{width} no JS errors',browser.evaluate('window.figureErrors'),[])
            browser.viewport(1440,960)
            browser.navigate((output/'index.html').as_uri())
            for name in ['cover-light','cover-dark']:
                data='data:image/svg+xml;base64,'+base64.b64encode((output/'assets'/f'{name}.svg').read_bytes()).decode()
                metrics=browser.evaluate('''(async()=>{const i=new Image();i.src=%s;await i.decode();const c=document.createElement('canvas');c.width=i.naturalWidth;c.height=i.naturalHeight;const ctx=c.getContext('2d');ctx.drawImage(i,0,0);const d=ctx.getImageData(0,0,c.width,c.height).data;let clear=0,ink=0;for(let j=3;j<d.length;j+=4){if(d[j]===0)clear++;else ink++}return {transparentRatio:clear/(d.length/4),hasInk:ink>100,corners:[d[3],d[(c.width-1)*4+3],d[(c.width*(c.height-1))*4+3],d[d.length-1]]};})()'''%json.dumps(data))
                test(f'{name} transparent corners',metrics['corners'],[0,0,0,0])
                test(f'{name} no background canvas',metrics['transparentRatio']>.70)
                test(f'{name} has actual drawing',metrics['hasInk'])
            browser.call('Emulation.setScriptExecutionDisabled',{'value':True})
            browser.navigate((output/'index.html').as_uri())
            test('No JS cover still visible and page fits',browser.evaluate('document.querySelector(".zo-cover-frame").getBoundingClientRect().width>100&&document.documentElement.scrollWidth<=innerWidth+1'))
        finally:
            if browser:
                try:browser.call('Browser.close')
                except Exception:pass
                browser.ws.close()
            try:process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.terminate();process.wait(timeout=10)
    changed=[name for name,digest in manifest['protected_hashes'].items() if sha(ROOT/name)!=digest]
    test('G01 production, source, accepted HTML and immutable 0.4 assets unchanged',changed,[])
    report={'checks':checks,'passed':sum(n['pass'] for n in checks),'total':len(checks),
            'checker_sha256':sha(Path(__file__)),
            'input_hashes':{name:sha(output/name) for name in ['index.html','manifest.json','figure.css','specimen.js']},
            'protected_file_count':len(manifest['protected_hashes']),'temporary_browser_removed':not Path(profile).exists(),
            'limits':['Edge headless only; no screen reader, real touch or Firefox/Safari.',
                      'Owner acceptance still required.', 'No course PDF, production render or publication.']}
    (output/'qa-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='checks'},ensure_ascii=False,indent=2))
    return 0 if report['passed']==report['total'] else 1


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview',type=Path,default=DEFAULT)
    args=parser.parse_args()
    raise SystemExit(check(args.preview.resolve()))

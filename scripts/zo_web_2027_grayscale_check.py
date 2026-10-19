"""Real-browser regression: grayscale must preserve viewport navigation while scrolling.

Run on an explicit freshly rendered four-page bundle; no production writes.
The negative fixture reinstates the former body filter and must fail geometry.
"""
from pathlib import Path
import argparse, json, socket, subprocess, sys, tempfile, time
sys.dont_write_bytecode = True
import requests
from zo_web_2027_check import Browser, edge_executable

def run(out):
    values={}
    def check(name,value):
        values[name]=bool(value)
        if not value: print('FAIL '+name,flush=True)
    metric="""(() => {
      const n=document.querySelector('.rail'),r=n.getBoundingClientRect();
      const top=document.querySelector('.site-top').getBoundingClientRect();
      const link=[...n.querySelectorAll('a,button')].find(x=>x.getBoundingClientRect().height>0);
      const q=link?.getBoundingClientRect(), hit=q&&document.elementFromPoint(q.left+q.width/2,q.top+q.height/2);
      return {y:r.y,bottom:r.bottom,height:r.height,top:top.y,
        visible:r.top>=-1&&r.bottom<=innerHeight+1&&r.height>100,
        clickable:!!hit&&(link===hit||link.contains(hit)),
        scroll:scrollY,max:document.documentElement.scrollHeight-innerHeight};
    })()"""
    def scroll(fraction):
        b.evaluate(f'window.scrollTo(0,(document.documentElement.scrollHeight-innerHeight)*{fraction})')
        time.sleep(.12)
        return b.evaluate(metric)
    with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
    base=f'http://127.0.0.1:{port}'
    with tempfile.TemporaryDirectory(prefix='_tmp_gray_',dir=out) as profile:
        proc=subprocess.Popen([edge_executable(),'--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check','--remote-debugging-address=127.0.0.1',f'--remote-debugging-port={port}','--remote-allow-origins=http://localhost','--user-data-dir='+profile,'about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        b=None
        try:
            for _ in range(100):
                try:
                    if requests.get(base+'/json/version',timeout=.3).ok:break
                except requests.RequestException:pass
                time.sleep(.1)
            else:raise TimeoutError('Browser did not start')
            target=requests.put(base+'/json/new?about:blank',timeout=10).json()
            b=Browser(target['webSocketDebuggerUrl'])
            for width in [1440,1000]:
                b.viewport(width,850)
                for key in ['d0','g01','g02','g03','g04']:
                    b.navigate((out/'html-current'/f'{key}-reading.html').as_uri()+('?r1-view=bai-hoc' if key!='d0' else ''))
                    # Set a real background radio and toggle through the shipped control.
                    for background in ['gray-3','gray-2','yellow-1','yellow-2','red-1','red-2']:
                        scroll(0)
                        b.click(f'.appearance input[value="{background}"]')
                        if b.evaluate("document.documentElement.classList.contains('grayscale')"):b.click('#grayscale')
                        color=[scroll(f) for f in [0,.5,.95,1]]
                        b.click('#grayscale')
                        gray=[scroll(f) for f in [0,.5,.95,1]]
                        prefix=f'{width}/{key}/{background}'
                        check(prefix+' scrolled to bottom',gray[-1]['max']>0 and abs(gray[-1]['max']-gray[-1]['scroll'])<2)
                        check(prefix+' navigation visible and clickable',all(m['visible'] and m['clickable'] and abs(m['top'])<1 for m in gray))
                        check(prefix+' color geometry unchanged',all(abs(a['y']-c['y'])<1 and abs(a['height']-c['height'])<1 for a,c in zip(color,gray)))
                    if width==1440:
                        scroll(.95)
                        b.call('Input.dispatchMouseEvent',{'type':'mouseWheel','x':width-50,'y':700,'deltaX':0,'deltaY':10000})
                        time.sleep(.2)
                        wheel=b.evaluate(metric)
                        check(key+' wheel to bottom preserves navigation',wheel['visible'] and wheel['clickable'] and abs(wheel['max']-wheel['scroll'])<2)
                        b.screenshot(out/f'{key}-gray-bottom.png')
                        b.evaluate("const old=document.createElement('style');old.id='negative-body-filter';old.textContent='html.grayscale{filter:none!important}.grayscale body{filter:grayscale(1)!important}';document.head.append(old)")
                        bad=scroll(1)
                        check(key+' former body-filter defect reproduced and rejected',not bad['visible'])
                        b.evaluate("document.querySelector('#negative-body-filter').remove()")
                        check(key+' navigation restored after negative fixture',scroll(1)['visible'])
            b.viewport(390,850)
            b.navigate((out/'html-current/g01-reading.html').as_uri())
            if not b.evaluate("document.documentElement.classList.contains('grayscale')"):b.click('#grayscale')
            scroll(1)
            b.click('.mobile-trigger')
            check('mobile grayscale drawer opens at bottom',b.evaluate("document.querySelector('#mobile-nav').open"))
            b.key('Escape',27)
            check('mobile grayscale Escape closes drawer',b.evaluate("!document.querySelector('#mobile-nav').open"))
        finally:
            if b:b.ws.close()
            proc.terminate()
            try:proc.wait(timeout=10)
            except subprocess.TimeoutExpired:proc.kill();proc.wait()
    report={'checks':values,'passed':sum(values.values()),'total':len(values),'failures':[k for k,v in values.items() if not v],'published':False}
    (out/'grayscale-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='checks'}))
    return int(bool(report['failures']))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    raise SystemExit(run(a.output.resolve()))

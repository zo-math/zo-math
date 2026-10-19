"""Measure all live tables/graphs and save wide/narrow review evidence."""
import argparse,json,socket,subprocess,tempfile,time
from pathlib import Path
import requests
from zo_web_2027_check import Browser,edge_executable
ROOT=Path(__file__).resolve().parents[1]
MEASURE=r"""(() => {
 const visible=n=>n.getClientRects().length&&getComputedStyle(n).visibility!=='hidden';
 const tables=[...document.querySelectorAll('.reader-content table')].filter(visible).map((t,i)=>{
  t.dataset.qaTableIndex=String(i);const r=t.getBoundingClientRect(),cap=t.querySelector('caption');
  const cells=[...t.querySelectorAll('td,th')].filter(visible);
  return {index:i,kind:t.dataset.tableFunction||t.dataset.tableKind||(t.classList.contains('zo-variation-native')?'variation':'ordinary'),width:r.width,height:r.height,rows:t.rows.length,cells:cells.length,overflowCells:cells.filter(c=>c.scrollWidth>c.clientWidth+3).map(c=>c.textContent.trim().slice(0,90)),captionBottom:!cap||!visible(cap)||getComputedStyle(cap).captionSide==='bottom'};
 });
 const graphs=[...document.querySelectorAll('.reader-content .figure-viewport img')].filter(visible).map(i=>{
  const css=getComputedStyle(i),em=parseFloat(css.getPropertyValue('--figure-em')),font=parseFloat(css.fontSize),expected=Number.isFinite(em)?em*font:parseFloat(css.getPropertyValue('--figure-width')); 
  return {src:i.getAttribute('src'),loaded:i.complete&&i.naturalWidth>0,width:i.getBoundingClientRect().width,expectedWidth:expected,scaleCorrect:Number.isFinite(expected)&&Math.abs(i.getBoundingClientRect().width-expected)<2};
 });
 return {title:document.title,viewport:innerWidth,pageWidth:document.documentElement.scrollWidth,fullView:!!document.querySelector('.r1-full-view'),tables,graphs};
})()"""
def run(bundle,output):
 bundle=Path(bundle).resolve();output=Path(output).resolve();output.mkdir(parents=True,exist_ok=False);shots=output/'screenshots';shots.mkdir();records=[];failures=[]
 with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
 base=f'http://127.0.0.1:{port}'
 with tempfile.TemporaryDirectory(prefix='course_browser_',dir=ROOT/'.quarto') as profile:
  process=subprocess.Popen([edge_executable(),'--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check','--remote-debugging-address=127.0.0.1',f'--remote-debugging-port={port}','--remote-allow-origins=http://localhost','--user-data-dir='+profile,'about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0));browser=None
  try:
   for _ in range(100):
    try:
     if requests.get(base+'/json/version',timeout=.3).ok:break
    except requests.RequestException:pass
    time.sleep(.1)
   else:raise RuntimeError('Review browser failed to start')
   tab=requests.put(base+'/json/new?about:blank',timeout=10).json();browser=Browser(tab['webSocketDebuggerUrl'])
   for key in ['home','d0','g01','g02','g03','g04']:
    for width in [1440,390]:
     browser.viewport(width,1000 if width==1440 else 850);browser.navigate((bundle/'html-current'/(key+'-reading.html')).as_uri()+('?r1-view=toan-van' if key.startswith('g') else ''))
     views=browser.evaluate("JSON.parse(document.querySelector('.d0-package')?.dataset.d0Views||'[]')") if key=='d0' else ['current']
     for view in views:
      if key=='d0':browser.navigate((bundle/'html-current'/(key+'-reading.html')).as_uri()+'?d0-view='+view)
      browser.evaluate("document.fonts.ready.then(()=>{document.querySelectorAll('.reader-content details').forEach(d=>d.open=true);return true})")
      info=browser.evaluate(MEASURE);info.update(page=key,width=width,view=view);records.append(info)
      if info['pageWidth']>width+3:failures.append(f'{key}/{width}/global horizontal overflow')
      if key.startswith('g') and not info['fullView']:failures.append(f'{key}/{width}/full view missing')
      for graph in info['graphs']:
       if not graph['loaded'] or not graph['scaleCorrect']:failures.append(f"{key}/{width}/graph {graph['src']}")
      captured=set();browser.evaluate('window.scrollTo(0,0)');browser.screenshot(shots/f'{key}-{view}-{width}-header.png')
      for table in info['tables']:
       if table['overflowCells']:failures.append(f"{key}/{width}/table {table['index']} cell overflow")
       if not table['captionBottom']:failures.append(f"{key}/{width}/table {table['index']} caption above")
       if table['kind'] in captured:continue
       captured.add(table['kind']);selector='table[data-qa-table-index="'+str(table['index'])+'"]'
       browser.evaluate('document.querySelector('+json.dumps(selector)+').scrollIntoView({block:"start"});window.scrollBy(0,-70)');time.sleep(.06)
       safe=''.join(c if c.isalnum() or c in '-_' else '_' for c in table['kind']);browser.screenshot(shots/f'{key}-{view}-{width}-{safe}.png')
      print('Reviewed live',key,width,'tables',len(info['tables']),'graphs',len(info['graphs']),flush=True)
     if key.startswith('g'):
      browser.navigate((bundle/'html-current'/(key+'-reading.html')).as_uri()+'?r1-view=tai-pdf#tai-tai-lieu')
      browser.click('input[name="background"][value="red-2"]')
      for gray in [False,True]:
       if gray:browser.click('#grayscale')
       utility=browser.evaluate("""(() => {
        const section=document.querySelector('#tai-tai-lieu');
        const cards=[...section.querySelectorAll('.zo-pdf-card')];
        return {cards:cards.length,visible:!!section.getClientRects().length,
          fits:document.documentElement.scrollWidth<=innerWidth+3,
          white:cards.every(c=>{const r=c.closest('.reading-region');return r&&getComputedStyle(r).backgroundColor==='rgb(255, 255, 255)'&&parseFloat(getComputedStyle(r).paddingLeft)>0}),
          textFits:cards.every(c=>c.scrollWidth<=c.clientWidth+3)};
       })()""")
       utility.update(page=key,width=width,view='tai-pdf',theme='red-2',grayscale=gray)
       records.append(utility)
       if utility['cards']!=8 or not all(utility[k] for k in ['visible','fits','white','textFits']):failures.append(f'{key}/{width}/download reading presentation/{gray}')
       browser.evaluate("document.querySelector('#tai-tai-lieu').scrollIntoView({block:'start'});window.scrollBy(0,-70)")
       browser.screenshot(shots/f'{key}-downloads-{width}-gray-{gray}.png')
      browser.click('#grayscale')

  finally:
   if browser:
    try:browser.call('Browser.close')
    except Exception:pass
    browser.ws.close()
   try:process.wait(timeout=10)
   except subprocess.TimeoutExpired:process.kill();process.wait(timeout=10)
 result={'records':records,'failures':failures,'owner_acceptance':'pending','published':False};(output/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({'failures':failures}));return bool(failures)
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('bundle',type=Path);parser.add_argument('output',type=Path);a=parser.parse_args();raise SystemExit(run(a.bundle,a.output))

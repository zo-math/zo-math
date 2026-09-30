/** Kiểm tra tràn ngang cấp trang của R1-G02 bằng viewport CDP thật.
 * Dùng: node <tệp> --url http://127.0.0.1:8781/.../r1_g02/ --out _audit/<lượt>
 */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawn} from 'node:child_process';

const args=Object.fromEntries(Array.from({length:(process.argv.length-2)/2},(_,index)=>process.argv.slice(2+index*2,4+index*2)));
if(!args['--url']||!args['--out']) throw Error('Required: --url HTTP_URL --out AUDIT_DIRECTORY');
const url=args['--url'],out=path.resolve(args['--out']);
if(!/^http:\/\/(127\.0\.0\.1|localhost):/.test(url)) throw Error('Local HTTP only');
fs.mkdirSync(out,{recursive:true});
const profile=fs.mkdtempSync(path.join(os.tmpdir(),'r1-g02-mobile-'));
const chrome=args['--chrome']||'C:/Program Files/Google/Chrome/Application/chrome.exe';
const child=spawn(chrome,['--headless=new','--remote-debugging-port=0',`--user-data-dir=${profile}`,'--no-first-run','--no-default-browser-check','--disable-background-networking','--disable-component-update','--disable-sync','about:blank'],{windowsHide:true,stdio:'ignore'});
const sleep=milliseconds=>new Promise(resolve=>setTimeout(resolve,milliseconds));
let ws,sequence=0;
const pending=new Map();
const results={url,viewports:{},checks:[]};
const check=(name,ok,evidence)=>results.checks.push({name,ok:!!ok,evidence});
const call=(method,params={})=>new Promise((resolve,reject)=>{const id=++sequence;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}));});
const evaluate=async expression=>{const response=await call('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(response.exceptionDetails)throw Error(JSON.stringify(response.exceptionDetails));return response.result.value;};
const screenshot=async name=>{const response=await call('Page.captureScreenshot',{format:'png'});fs.writeFileSync(path.join(out,`${name}.png`),Buffer.from(response.data,'base64'));};
const navigate=async()=>{await call('Page.navigate',{url});for(let index=0;index<100;index++){await sleep(100);if(await evaluate('document.readyState==="complete" && !!document.querySelector(".r1-tab")'))break;}await evaluate('document.fonts.ready');await sleep(350);};
const measure=()=>evaluate(`(() => {
  const root=document.documentElement, body=document.body;
  const viewport=root.clientWidth;
  const componentStyles=selector=>[...document.querySelectorAll(selector)].filter(element=>element.getBoundingClientRect().width>0).map(element=>{
    const summary=element.querySelector(':scope > summary');
    const outerStyle=getComputedStyle(element),summaryStyle=summary&&getComputedStyle(summary);
    return {id:element.id,backgroundColor:outerStyle.backgroundColor,borderColor:outerStyle.borderColor,borderRadius:outerStyle.borderRadius,summaryColor:summaryStyle?.color||'',summaryMinHeight:summaryStyle?.minHeight||'',summaryHeight:summary?.getBoundingClientRect().height||0};
  });
  const offenders=[...document.querySelectorAll('body *')].map(element=>{
    const rect=element.getBoundingClientRect(),style=getComputedStyle(element);
    const intentionalOverflow=element.closest('.r1-tablist,#quarto-sidebar,nav#TOC,.quarto-toc,.toc,.r1-table-scroll-x,.table-scroll');
    const section=element.closest('[id]');
    return {tag:element.tagName,id:element.id,classes:typeof element.className==='string'?element.className:'',text:(element.textContent||'').trim().slice(0,240),sectionId:section?.id||'',left:rect.left,right:rect.right,width:rect.width,overflowX:style.overflowX,hidden:style.display==='none'||style.visibility==='hidden'||rect.width===0,intentionalOverflow:!!intentionalOverflow};
  }).filter(item=>!item.hidden&&(item.left<-.5||item.right>viewport+.5)&&!item.intentionalOverflow).slice(0,20);
  const tableScrollers=[...document.querySelectorAll('.r1-table-scroll-x')].filter(element=>element.getBoundingClientRect().width>0).map(element=>({id:element.id,clientWidth:element.clientWidth,scrollWidth:element.scrollWidth,overflowX:getComputedStyle(element).overflowX}));
  const visibleCount=selector=>[...document.querySelectorAll(selector)].filter(element=>element.getBoundingClientRect().width>0).length;
  const supportImages=[...document.querySelectorAll('.r1-download-support img')];
  return {viewport,innerWidth,rootClientWidth:root.clientWidth,rootScrollWidth:root.scrollWidth,bodyClientWidth:body.clientWidth,bodyScrollWidth:body.scrollWidth,pageOverflow:Math.max(root.scrollWidth-root.clientWidth,body.scrollWidth-root.clientWidth),offenders,tableScrollers,components:{toc:componentStyles('details.r1-section-toc'),guidance:componentStyles('details.zo-learning-guidance'),solution:componentStyles('details.zo-learning-solution')},downloads:{cards:visibleCount('.r1-download-card'),sectionItems:visibleCount('.r1-section-download-item'),support:visibleCount('.r1-download-support'),images:supportImages.length,imagesLoaded:supportImages.every(image=>image.complete&&image.naturalWidth>0)}};
})()`);

try {
  const active=path.join(profile,'DevToolsActivePort');
  for(let index=0;index<100&&!fs.existsSync(active);index++)await sleep(100);
  const port=fs.readFileSync(active,'utf8').split('\n')[0];
  const targets=await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
  ws=new WebSocket(targets.find(target=>target.type==='page').webSocketDebuggerUrl);
  ws.addEventListener('message',event=>{const message=JSON.parse(event.data);if(pending.has(message.id)){const promise=pending.get(message.id);pending.delete(message.id);message.error?promise.reject(Error(JSON.stringify(message.error))):promise.resolve(message.result);}});
  await new Promise((resolve,reject)=>{ws.addEventListener('open',resolve,{once:true});ws.addEventListener('error',reject,{once:true});});
  await call('Page.enable');
  await call('Runtime.enable');
  for(const width of [1440,430,390]){
    await call('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:true});
    await call('Emulation.setTouchEmulationEnabled',{enabled:true,maxTouchPoints:5});
    await navigate();
    const views={};
    for(const tab of await evaluate(`[...document.querySelectorAll('.r1-tab')].map(element=>({id:element.id,view:element.id.replace(/^r1-tab-/, '')}))`)){
      await evaluate(`document.getElementById(${JSON.stringify(tab.id)}).click()`);
      await sleep(180);
      views[tab.view]=await measure();
    }
    results.viewports[width]=views;
    const states=Object.values(views);
    check(`${width}: no page-level horizontal overflow`,states.every(state=>state.pageOverflow<=1&&state.offenders.length===0),Object.fromEntries(Object.entries(views).filter(([,state])=>state.pageOverflow>1||state.offenders.length)));
    check(`${width}: wide tables retain local scrolling`,states.flatMap(state=>state.tableScrollers).every(table=>table.overflowX==='auto'&&table.scrollWidth>=table.clientWidth),states.flatMap(state=>state.tableScrollers));
    const lessonComponents=views['bai-hoc'].components;
    const tocColor=lessonComponents.toc[0]?.summaryColor;
    check(`${width}: guidance uses the canonical white surface and muted title`,
      lessonComponents.guidance.length>0&&lessonComponents.guidance.every(item=>item.backgroundColor==='rgb(255, 255, 255)'&&item.summaryColor===tocColor&&item.summaryHeight>=44),
      {toc:lessonComponents.toc,guidance:lessonComponents.guidance});
    const downloadComponents=views['tai-pdf'].downloads;
    check(`${width}: PDF view renders every canonical download component`,
      downloadComponents.cards===2&&downloadComponents.sectionItems===6&&downloadComponents.support===1&&downloadComponents.images===2&&downloadComponents.imagesLoaded,
      downloadComponents);
    await evaluate(`document.getElementById('r1-tab-bai-hoc').click();scrollTo({top:0,behavior:'instant'})`);
    await sleep(250);
    await screenshot(`${width}_bai_hoc`);
    await evaluate(`(() => { const target=document.querySelector('details.zo-learning-guidance'); target.scrollIntoView({block:'center',behavior:'instant'}); })()`);
    await sleep(250);
    await screenshot(`${width}_guidance`);
    await evaluate(`document.getElementById('r1-tab-tai-pdf').click();scrollTo({top:0,behavior:'instant'})`);
    await sleep(250);
    await screenshot(`${width}_tai_pdf`);
    await evaluate(`document.getElementById('r1-tab-loi-giai').click()`);
    await sleep(100);
    await evaluate(`(() => { const target=document.getElementById('loi-giai-kt04')||document.querySelector('details.zo-learning-solution'); if(!target)return; for(let details=target.matches('details')?target:target.closest('details');details;details=details.parentElement?.closest('details')) details.open=true; target.scrollIntoView({block:'center',behavior:'instant'}); })()`);
    await sleep(250);
    await screenshot(`${width}_loi_giai_kt04`);
  }
} catch(error) {
  check('runtime completed',false,String(error));
} finally {
  try{ws?.close();}catch{}
  try{child.kill();}catch{}
  const report=path.join(out,'mobile-overflow.json');
  fs.writeFileSync(report,JSON.stringify(results,null,2));
  const failures=results.checks.filter(item=>!item.ok);
  console.log(JSON.stringify({checks:results.checks.length,failures,report},null,2));
  process.exitCode=failures.length?1:0;
}

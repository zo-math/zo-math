/** Local-only Chromium regression. No personal profile, acceptance or publication. */
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {spawn} from 'node:child_process';
import {createHash} from 'node:crypto';
const args=Object.fromEntries(Array.from({length:(process.argv.length-2)/2},(_,i)=>process.argv.slice(2+i*2,4+i*2)));
if(!args['--url']||!args['--out']) throw Error('Required --url LOCAL_URL --out AUDIT_DIRECTORY');
const url=args['--url'], out=path.resolve(args['--out']);
if(!/^http:\/\/127\.0\.0\.1:\d+\//.test(url)) throw Error('Local HTTP only');
fs.mkdirSync(out,{recursive:true});
const profile=fs.mkdtempSync(path.join(os.tmpdir(),'zo-d0-browser-'));
const chrome=args['--chrome']||'C:/Program Files/Google/Chrome/Application/chrome.exe';
const child=spawn(chrome,['--headless=new','--remote-debugging-port=0',`--user-data-dir=${profile}`,'--no-first-run','--no-default-browser-check','--disable-background-networking','--disable-component-update','--disable-sync','about:blank'],{windowsHide:true,stdio:'ignore'});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const pending=new Map(); let ws,seq=0;
const result={url,checks:[],viewports:{},errors:[],limitation:'Desktop and simulated mobile Chromium, not real-device or owner visual acceptance.'};
const check=(name,ok,evidence)=>result.checks.push({name,ok:!!ok,evidence});
const call=(method,params={})=>new Promise((resolve,reject)=>{const id=++seq;const timer=setTimeout(()=>{pending.delete(id);reject(Error('CDP timeout: '+method));},10000);pending.set(id,{resolve:r=>{clearTimeout(timer);resolve(r);},reject:r=>{clearTimeout(timer);reject(r);}});ws.send(JSON.stringify({id,method,params}));});
const ev=async expression=>{const r=await call('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
const shot=async file=>{const r=await call('Page.captureScreenshot',{format:'png'});fs.writeFileSync(path.join(out,file+'.png'),Buffer.from(r.data,'base64'));};
const go=async suffix=>{await call('Page.navigate',{url:url+suffix});for(let i=0;i<100;i++){await sleep(80);if(await ev('document.readyState==="complete" && !!document.querySelector(".d0-tab")'))break;}await ev('document.fonts.ready');await sleep(250);};
const state=()=>ev(`(() => {const p=document.querySelector('.d0-view-panel');return {view:p.dataset.d0View,visible:[...p.children].filter(s=>!s.hidden).map(s=>s.id),overflow:document.documentElement.scrollWidth-document.documentElement.clientWidth,selected:document.querySelector('.d0-tab[aria-selected=true]').id};})()`);
try {
  const portFile=path.join(profile,'DevToolsActivePort');
  for(let i=0;i<100&&!fs.existsSync(portFile);i++)await sleep(100);
  if(!fs.existsSync(portFile))throw Error('Chromium did not start');
  const port=fs.readFileSync(portFile,'utf8').split('\n')[0];
  const targets=await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
  ws=new WebSocket(targets.find(t=>t.type==='page').webSocketDebuggerUrl);
  await new Promise((resolve,reject)=>{ws.onopen=resolve;ws.onerror=reject;});
  ws.onmessage=event=>{const r=JSON.parse(event.data);if(r.id){const p=pending.get(r.id);pending.delete(r.id);r.error?p.reject(Error(JSON.stringify(r.error))):p.resolve(r.result);}else if(r.method==='Runtime.exceptionThrown')result.errors.push(r.params.exceptionDetails);};
  await call('Page.enable');await call('Runtime.enable');
  for(const width of [1366,430,390]) {
    await call('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:width<600});
    await go('');
    let s=await state();
    check(`${width}: default voluntary entry`,s.view==='bat-dau'&&s.visible.join()==='bat-dau'&&s.overflow<=1,s);
    await shot(`${width}_bat_dau`);
    const views=['bat-dau','khai-bao-pham-vi','khao-sat','doc-ket-qua','chon-mach'];
    for(const view of views){
      await ev(`document.querySelector('#d0-tab-${view}').click()`);await sleep(80);
      s=await state();check(`${width}: tab ${view}`,s.view===view&&s.overflow<=1,s);
    }
    await ev('document.querySelector("#d0-tab-khao-sat").click();document.querySelector("#khao-sat .r1-section-toc summary").click()');await sleep(100);
    const toc=await ev('(() => {const d=document.querySelector("#khao-sat .r1-section-toc"),l=d.querySelector(".d0-survey-toc");return {open:d.open,links:[...l.querySelectorAll("a")].map(a=>a.hash),columns:getComputedStyle(l).columnCount,overflow:document.documentElement.scrollWidth-document.documentElement.clientWidth,oldStrip:!!document.querySelector(".d0-strand-nav")};})()');
    check(`${width}: canonical survey TOC`,toc.open&&toc.links.length===8&&toc.columns===(width<600?'1':'2')&&toc.overflow<=1&&!toc.oldStrip,toc);
    await shot(`${width}_muc_luc`);
    for(let i=1;i<=8;i++){
      await ev(`document.querySelector('.d0-survey-toc a[href$="#mach-r${i}"]').click()`);await sleep(40);
      const anchor=await ev(`({hash:location.hash,view:document.querySelector('.d0-view-panel').dataset.d0View,title:document.querySelector('#mach-r${i} > h3').textContent})`);
      check(`${width}: TOC R${i}`,anchor.hash===`#mach-r${i}`&&anchor.view==='khao-sat'&&anchor.title.startsWith(`R${i} — `),anchor);
    }
    await ev('document.querySelector("#d0-tab-chon-mach").click()');await sleep(100);
    await shot(`${width}_chon_mach`);
    await ev('document.querySelector("#d0-tab-khai-bao-pham-vi").click();document.querySelector("#doi-chieu-minh-hoa").open=false;document.querySelector("#doi-chieu-minh-hoa summary").click();document.querySelector("#doi-chieu-minh-hoa").scrollIntoView()');await sleep(100);
    check(`${width}: Bài 00 disclosure opens`,await ev('document.querySelector("#doi-chieu-minh-hoa").open'));
    await ev('document.querySelector("#doi-chieu-minh-hoa summary").click()');
    check(`${width}: Bài 00 disclosure closes`,await ev('!document.querySelector("#doi-chieu-minh-hoa").open'));
    await ev('document.querySelector("#doi-chieu-minh-hoa summary").click()');
    await shot(`${width}_bai_00`);
    for(let r=1;r<=8;r++)for(let n=1;n<=3;n++){
      const task=`d0-r${r}-${String(n).padStart(2,'0')}`,answer=`doi-chieu-r${r}-${String(n).padStart(2,'0')}`;
      await ev(`document.querySelector('#d0-tab-khao-sat').click();document.querySelector('a[href$="#${answer}"]').click()`);await sleep(40);
      s=await state();const open=await ev(`document.getElementById('${answer}').open`);
      check(`${width}: ${task} -> comparison`,s.view==='doc-ket-qua'&&open&&s.overflow<=1,s);
      await ev(`document.querySelector('#${answer} a[href$="#${task}"]').click()`);await sleep(40);
      s=await state();check(`${width}: ${answer} -> question`,s.view==='khao-sat'&&s.overflow<=1,s);
    }
    await go('?d0-view=doc-ket-qua#doi-chieu-r8-03');
    s=await state();check(`${width}: deep link opens answer`,s.view==='doc-ket-qua'&&await ev('document.querySelector("#doi-chieu-r8-03").open'),s);
    await shot(`${width}_doi_chieu`);
    await ev('document.querySelector("#d0-tab-khao-sat").click();document.querySelector("#d0-r3-03").scrollIntoView()');await sleep(200);
    await shot(`${width}_hinh_hop`);
    await ev('document.querySelector("#d0-r3-01").scrollIntoView()');await sleep(150);
    await shot(`${width}_phan_so_0_0`);
    const images=await ev('[...document.querySelectorAll(".d0-package img")].map(i=>({src:i.getAttribute("src"),ok:i.complete&&i.naturalWidth>0,width:i.getBoundingClientRect().width}))');
    check(`${width}: canonical images load`,images.length===2&&images.every(i=>i.ok),images);
    const inlineMath=await ev('[...document.querySelectorAll(".d0-inline-math")].map(m=>({tex:m.querySelector("annotation")?.textContent||"",overflowX:getComputedStyle(m).overflowX,overflowY:getComputedStyle(m).overflowY,scrollHeight:m.scrollHeight,clientHeight:m.clientHeight}))');
    check(`${width}: inline math has no vertical scrollbar controls`,inlineMath.length>0&&inlineMath.every(m=>m.overflowY==='hidden'),inlineMath.filter(m=>m.overflowY!=='hidden'));
    await ev('document.querySelector("#d0-tab-doc-ket-qua").click();document.querySelectorAll("#doc-ket-qua details").forEach(d=>d.open=true)');await sleep(100);
    s=await state();check(`${width}: all comparisons open without page overflow`,s.view==='doc-ket-qua'&&s.overflow<=1,s);
    check(`${width}: no full-text tab`,!await ev('!!document.querySelector("#d0-tab-toan-van")'),{});
    const tables=await ev('[...document.querySelectorAll(".d0-data-table")].map(t=>({scroll:t.scrollWidth,client:t.clientWidth,overflow:getComputedStyle(t).overflowX}))');
    check(`${width}: table scroll stays local`,tables.every(t=>t.scroll<=t.client+1||['auto','scroll'].includes(t.overflow)),tables);
    const nav=await ev('(() => {scrollTo(0,3000);return new Promise(resolve=>setTimeout(()=>{const n=document.querySelector(".d0-nav-slot");resolve({top:n.getBoundingClientRect().top,sticky:getComputedStyle(n).position});},250));})()');
    check(`${width}: lesson controls remain sticky`,Math.abs(nav.top)<=1&&nav.sticky==='sticky',nav);
    const navbarDown=await ev('document.querySelector("#quarto-header").getBoundingClientRect().bottom');
    await ev('scrollBy(0,-300)');await sleep(500);
    const navbarUp=await ev('document.querySelector("#quarto-header").getBoundingClientRect().bottom');
    check(`${width}: Navbar returns on upward scroll`,navbarUp>navbarDown+1,{navbarDown,navbarUp});
    await go('?d0-view=khao-sat#d0-r1-03');
    await shot(`${width}_bang_dau`);
    // Browser back restores the owner tab and answer state.
    await ev(`document.querySelector('a[href$="#doi-chieu-r1-03"]').click()`);await sleep(80);
    await ev(`document.querySelector('#doi-chieu-r1-03 a[href$="#d0-r1-03"]').click()`);await sleep(80);
    await ev('history.back()');await sleep(150);
    s=await state();check(`${width}: back restores comparison`,s.view==='doc-ket-qua',s);
    result.viewports[width]={final:s,images,tables};
  }
  // Progressive enhancement: no JS still has all public content and native details.
  await call('Emulation.setScriptExecutionDisabled',{value:true});
  await call('Page.navigate',{url});await sleep(600);
  await call('Emulation.setScriptExecutionDisabled',{value:false});
  check('No-JS content readable',await ev('document.querySelectorAll(".d0-primary-task").length===24 && document.querySelectorAll(".d0-package details").length===25 && !document.querySelector(".d0-package [hidden]")'));
  check('No JavaScript runtime errors',result.errors.length===0,result.errors);
} catch(error){result.fatal=String(error);check('runtime completes',false,String(error));try{result.debug=await ev('({url:location.href,tabs:[...document.querySelectorAll(".d0-tab")].map(t=>t.id),links:[...document.querySelectorAll(".d0-package a")].slice(0,12).map(a=>a.getAttribute("href"))})');console.log(JSON.stringify(result.debug));}catch{}}
finally {
  try{result.html_sha256=createHash('sha256').update(Buffer.from(await (await fetch(url)).arrayBuffer())).digest('hex');}catch{}
  result.screenshots=Object.fromEntries(fs.readdirSync(out).filter(f=>f.endsWith('.png')).map(f=>[f,createHash('sha256').update(fs.readFileSync(path.join(out,f))).digest('hex')]));
  result.status=result.checks.every(c=>c.ok)?'PASS':'FAIL';
  fs.writeFileSync(path.join(out,'runtime.json'),JSON.stringify(result,null,2));
  console.log(JSON.stringify({status:result.status,checks:result.checks.length,failed:result.checks.filter(c=>!c.ok),out},null,2));
  if(ws)ws.close();child.kill();
  // Explicit exact temporary profile, verified beneath the OS temp directory.
  if(path.resolve(profile).startsWith(path.resolve(os.tmpdir())+path.sep)){
    for(let i=0;i<30;i++){try{fs.rmSync(profile,{recursive:true,force:true});break;}catch{await sleep(100);}}
  }
  if(result.status!=='PASS')process.exitCode=1;
}

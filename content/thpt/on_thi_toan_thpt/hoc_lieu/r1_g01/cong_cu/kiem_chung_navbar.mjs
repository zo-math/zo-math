/** Output regression: node <this-file> --url http://127.0.0.1:8781/.../index.html
 * --out _audit/<run> [--chrome path]. A fresh CDP profile; no personal browser data.
 * Exits nonzero on a reader-visible failure. Not owner acceptance or a real device test.
 */
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {spawn} from 'node:child_process';
const args=Object.fromEntries(Array.from({length:(process.argv.length-2)/2},(_,i)=>process.argv.slice(2+i*2,4+i*2)));
if(!args['--url']||!args['--out']) throw Error('Required: --url HTTP_URL --out AUDIT_DIRECTORY');
const url=args['--url'], out=path.resolve(args['--out']);
if(!/^http:\/\/(127\.0\.0\.1|localhost):/.test(url)) throw Error('Local HTTP only');
fs.mkdirSync(out,{recursive:true});
const profile=fs.mkdtempSync(path.join(out,'browser-cache-'));
const chrome=args['--chrome']||'C:/Program Files/Google/Chrome/Application/chrome.exe';
const child=spawn(chrome,['--headless=new','--remote-debugging-port=0',`--user-data-dir=${profile}`,'--no-first-run','--no-default-browser-check','--disable-background-networking','--disable-component-update','--disable-sync','about:blank'],{windowsHide:true,stdio:'ignore'});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let ws, seq=0; const pending=new Map(), results={url,viewports:{},checks:[],platform:os.platform(),input:'CDP; touch is simulated'};
const check=(name,ok,evidence)=>results.checks.push({name,ok:!!ok,evidence});
const call=(method,params={})=>new Promise((resolve,reject)=>{const id=++seq;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}));});
const ev=async expression=>{const r=await call('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
const shot=async file=>{const r=await call('Page.captureScreenshot',{format:'png'});fs.writeFileSync(path.join(out,file+'.png'),Buffer.from(r.data,'base64'));};
const shotElement=async(file,selector)=>{const box=await ev(`(() => {const r=document.querySelector(${JSON.stringify(selector)}).getBoundingClientRect();return {x:r.left+scrollX,y:r.top+scrollY,width:r.width,height:r.height,scale:1};})()`);const r=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip:box});fs.writeFileSync(path.join(out,file+'.png'),Buffer.from(r.data,'base64'));};
const go=async suffix=>{await call('Page.navigate',{url:url+suffix});for(let i=0;i<100;i++){await sleep(100);if(await ev('document.readyState==="complete" && !!document.querySelector(".r1-tab")')) break;}await ev('document.fonts.ready');await sleep(300);};
const rectScript=`(() => {const h=document.querySelector('#quarto-header'), n=document.querySelector('.r1-section-nav'), b=h.querySelector('.navbar');const r=e=>{const x=e.getBoundingClientRect();return {top:x.top,bottom:x.bottom,left:x.left,width:x.width,height:x.height}};return {time:performance.now(),y:scrollY,header:r(h),navbar:r(b),nav:r(n),gap:r(n).top-r(h).bottom,cls:h.className,view:document.querySelector('.r1-view-panel').dataset.r1View,overflow:document.documentElement.scrollWidth-document.documentElement.clientWidth,navParent:n.parentElement.id,visibility:getComputedStyle(n).visibility};})()`;
const begin=()=>ev(`window.__r1frames=[];window.__r1record=true;window.__r1phase='start';(function sample(){if(!window.__r1record)return;window.__r1frames.push({...${rectScript},phase:window.__r1phase});requestAnimationFrame(sample)})();true`);
const key=async(k,code)=>{await call('Input.dispatchKeyEvent',{type:'keyDown',key:k,code:k,windowsVirtualKeyCode:code,...(k==='Enter'?{text:'\r'}:{})});await call('Input.dispatchKeyEvent',{type:'keyUp',key:k,code:k,windowsVirtualKeyCode:code});await sleep(120);};
const link=async(hash,scope='document')=>ev(`[...${scope}.querySelectorAll('a')].find(a=>decodeURIComponent(a.hash)===${JSON.stringify(hash)}).click()`);
const targetState=()=>ev(`(() => {const p=document.querySelector('.r1-view-panel'),t=document.getElementById(decodeURIComponent(location.hash.slice(1))),n=document.querySelector('.r1-section-nav'),h=document.querySelector('#quarto-header');return {view:p.dataset.r1View,hash:decodeURIComponent(location.hash),targetTop:t?.getBoundingClientRect().top,cover:Math.max(0,n.getBoundingClientRect().bottom,h.getBoundingClientRect().bottom),focus:document.activeElement.id,visible:[...p.children].filter(e=>!e.hidden).map(e=>e.id)};})()`);
const stripState=()=>ev(`(() => {const l=document.querySelector('.r1-tablist'),t=l.querySelector('[aria-selected=true]'),r=l.getBoundingClientRect(),s=t.getBoundingClientRect();return {left:l.scrollLeft,selected:t.id,tabLeft:s.left,tabRight:s.right,stripLeft:r.left,stripRight:r.right,visible:s.left>=r.left-1&&s.right<=r.right+1};})()`);
const tabVisualState=()=>ev(`(() => {const style=(e,pseudo=null)=>{const c=getComputedStyle(e,pseudo);return {background:c.backgroundColor,borderTop:c.borderTop,borderRight:c.borderRight,borderBottom:c.borderBottom,borderLeft:c.borderLeft,boxShadow:c.boxShadow,color:c.color,fontWeight:c.fontWeight,outline:c.outline,outlineOffset:c.outlineOffset,textDecoration:c.textDecorationLine,content:c.content,width:c.width,height:c.height,padding:c.padding}};const list=document.querySelector('.r1-tablist'),selected=list.querySelector('[aria-selected=true]'),regular=document.querySelector('#r1-tab-cach-hoc'),nav=document.querySelector('.r1-section-nav'),header=document.querySelector('#quarto-header');return {selected:{id:selected.id,focusVisible:selected.matches(':focus-visible'),hover:selected.matches(':hover'),style:style(selected),before:style(selected,'::before'),after:style(selected,'::after')},regular:{id:regular.id,focusVisible:regular.matches(':focus-visible'),hover:regular.matches(':hover'),style:style(regular),before:style(regular,'::before'),after:style(regular,'::after')},list:style(list),nav:style(nav),docked:header.classList.contains('r1-nav-docked'),navParent:nav.parentElement.id};})()`);
const focusVisualState=()=>ev(`(() => {
  const focused=document.activeElement, style=getComputedStyle(focused), rect=focused.getBoundingClientRect();
  const parseColor=value=>{if(/^#[0-9a-f]{6}$/i.test(value))return {r:parseInt(value.slice(1,3),16),g:parseInt(value.slice(3,5),16),b:parseInt(value.slice(5,7),16),a:1};const match=value.match(/rgba?\\(([^)]+)\\)/);if(!match)return null;const parts=match[1].split(',').map(Number);return {r:parts[0],g:parts[1],b:parts[2],a:parts[3]??1};};
  const luminance=color=>[color.r,color.g,color.b].map(value=>{value/=255;return value<=.04045?value/12.92:((value+.055)/1.055)**2.4;}).reduce((sum,value,index)=>sum+value*[.2126,.7152,.0722][index],0);
  const contrast=(first,second)=>{const values=[luminance(first),luminance(second)].sort((a,b)=>b-a);return (values[0]+.05)/(values[1]+.05);};
  const outlineColor=parseColor(style.outlineColor), elementBackground=parseColor(style.backgroundColor);
  let parent=focused.parentElement, parentBackground=null, parentBackgroundNode=null;
  while(parent&&!parentBackground){const candidate=parseColor(getComputedStyle(parent).backgroundColor);if(candidate&&candidate.a===1){parentBackground=candidate;parentBackgroundNode=parent;}parent=parent.parentElement;}
  const backgrounds=[['element',elementBackground],['ancestor',parentBackground]].filter(([,color])=>color&&color.a===1);
  const contrasts=Object.fromEntries(backgrounds.map(([name,color])=>[name,contrast(outlineColor,color)]));
  const width=parseFloat(style.outlineWidth), offset=parseFloat(style.outlineOffset);
  const extent=Math.max(0,width+offset), outlineRect={left:rect.left-extent,right:rect.right+extent,top:rect.top-extent,bottom:rect.bottom+extent};
  const clippedBy=[];
  for(let node=focused.parentElement;node&&node!==document.documentElement;node=node.parentElement){
    const nodeStyle=getComputedStyle(node), nodeRect=node.getBoundingClientRect();
    const clipsX=/^(hidden|clip|auto|scroll)$/.test(nodeStyle.overflowX), clipsY=/^(hidden|clip|auto|scroll)$/.test(nodeStyle.overflowY);
    if((clipsX&&(outlineRect.left<nodeRect.left-.5||outlineRect.right>nodeRect.right+.5))||(clipsY&&(outlineRect.top<nodeRect.top-.5||outlineRect.bottom>nodeRect.bottom+.5))){
      clippedBy.push({tag:node.tagName,id:node.id,classes:node.className,overflowX:nodeStyle.overflowX,overflowY:nodeStyle.overflowY,rect:{left:nodeRect.left,right:nodeRect.right,top:nodeRect.top,bottom:nodeRect.bottom}});
    }
  }
  const expectedColor='#554f48', expectedColorValue=parseColor(expectedColor);
  const colorMatches=outlineColor&&expectedColorValue&&outlineColor.r===expectedColorValue.r&&outlineColor.g===expectedColorValue.g&&outlineColor.b===expectedColorValue.b&&outlineColor.a===expectedColorValue.a;
  const viewportClipped=outlineRect.left<-.5||outlineRect.right>innerWidth+.5||outlineRect.top<-.5||outlineRect.bottom>innerHeight+.5;
  if(viewportClipped)clippedBy.push({tag:'VIEWPORT',id:'',classes:'',overflowX:'clip',overflowY:'clip',rect:{left:0,right:innerWidth,top:0,bottom:innerHeight}});
  const header=document.querySelector('#quarto-header'), nav=document.querySelector('.r1-section-nav'), tablist=document.querySelector('.r1-tablist'), slot=document.querySelector('.r1-nav-slot');
  const box=node=>{const value=node.getBoundingClientRect();return {left:value.left,right:value.right,top:value.top,bottom:value.bottom,width:value.width,height:value.height};};
  return {tag:focused.tagName,id:focused.id,classes:typeof focused.className==='string'?focused.className:'',focusVisible:focused.matches(':focus-visible'),outlineStyle:style.outlineStyle,outlineWidth:style.outlineWidth,outlineColor:style.outlineColor,outlineOffset:style.outlineOffset,expectedColor,colorMatches,backgrounds:{element:style.backgroundColor,ancestor:parentBackgroundNode?getComputedStyle(parentBackgroundNode).backgroundColor:null},contrasts,minContrast:Math.min(...Object.values(contrasts)),clippedBy,outlineRect,rect:box(focused),layout:{nav:box(nav),tablist:box(tablist),slot:box(slot)},docked:header.classList.contains('r1-nav-docked'),navParent:nav.parentElement.id,documentOverflow:document.documentElement.scrollWidth-document.documentElement.clientWidth};
})()`);
const keyboardFocusState=()=>ev(`(() => {const e=document.activeElement,c=getComputedStyle(e),all=[...document.querySelectorAll('*')];return {domIndex:all.indexOf(e),tag:e.tagName,id:e.id,classes:typeof e.className==='string'?e.className:'',role:e.getAttribute('role'),href:e.getAttribute('href'),tabindex:e.getAttribute('tabindex'),text:(e.textContent||e.getAttribute('aria-label')||'').trim().replace(/\\s+/g,' ').slice(0,100),focusVisible:e.matches(':focus-visible'),outlineStyle:c.outlineStyle,outlineWidth:c.outlineWidth,outlineColor:c.outlineColor,outlineOffset:c.outlineOffset};})()`);
const keyboardFocusInventory=async()=>{await go('?r1-view=toan-van');await ev("document.body.setAttribute('tabindex','-1');document.body.focus({preventScroll:true})");const items=[];for(let i=0;i<240;i++){await key('Tab',9);const item=await keyboardFocusState();if(item.tag==='BODY'||items.some(old=>old.domIndex===item.domIndex))break;items.push(item);}await ev("document.body.removeAttribute('tabindex')");return items;};
const uniformFocusPass=state=>state.focusVisible&&state.outlineStyle==='solid'&&state.outlineWidth==='2px'&&state.outlineColor==='rgb(85, 79, 72)'&&state.outlineOffset==='2px';
const focusPass=(state,expectedId=null)=>uniformFocusPass(state)&&(!expectedId||state.id===expectedId)&&state.clippedBy.length===0&&state.documentOverflow<=1;
const focusCase=async(selector,file,setup='')=>{
  await key('Tab',9);
  await ev(`(() => {${setup}const element=document.querySelector(${JSON.stringify(selector)});if(!element)throw Error('Missing focus target: '+${JSON.stringify(selector)});element.scrollIntoView({block:'center',inline:'nearest',behavior:'instant'});element.focus({preventScroll:true});return true;})()`);
  await sleep(180);const state=await focusVisualState();await shot(file);return state;
};
const accountVisualState=()=>ev(`(() => {const e=document.querySelector('.r1-download-support'),qr=e.querySelector('.r1-support-qr'),link=e.querySelector('.r1-support-link'),c=getComputedStyle(e),r=e.getBoundingClientRect(),q=qr.getBoundingClientRect(),l=link.getBoundingClientRect();return {background:c.backgroundColor,border:c.border,padding:c.padding,boxShadow:c.boxShadow,fontWeight:c.fontWeight,rect:{left:r.left,right:r.right,width:r.width},qr:{left:q.left,right:q.right,width:q.width},link:{left:l.left,right:l.right,width:l.width},clientWidth:e.clientWidth,scrollWidth:e.scrollWidth,viewport:innerWidth,inside:q.left>=r.left&&q.right<=r.right&&l.left>=r.left&&l.right<=r.right,notClipped:e.scrollWidth<=e.clientWidth+1};})()`);
const sectionDownloadsState=()=>ev(`(() => {const list=document.querySelector('.r1-section-download-list'),r=list.getBoundingClientRect(),items=[...list.children].map(item=>{const x=item.getBoundingClientRect(),a=item.querySelector('a'),s=getComputedStyle(item);return {title:item.querySelector('.r1-section-download-title')?.textContent.trim(),href:a?.getAttribute('href'),download:a?.getAttribute('download'),left:x.left,right:x.right,width:x.width,display:s.display,overflow:item.scrollWidth-item.clientWidth}});return {count:items.length,items,clientWidth:list.clientWidth,scrollWidth:list.scrollWidth,inside:items.every(x=>x.left>=r.left-1&&x.right<=r.right+1),cards:list.querySelectorAll('.r1-download-card').length};})()`);
const wheel=async(delta,label,width)=>{await ev(`window.__r1phase=${JSON.stringify(label)}`);await call('Input.dispatchMouseEvent',{type:'mouseWheel',x:width/2,y:700,deltaX:0,deltaY:delta});for(let i=0;i<4;i++){await sleep(i===0?25:85);await shot(`${width}_${label}_${i}`);}await sleep(250);};
try {
  const active=path.join(profile,'DevToolsActivePort');
  for(let i=0;i<100&&!fs.existsSync(active);i++)await sleep(100);
  const port=fs.readFileSync(active,'utf8').split('\n')[0];
  const targets=await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
  ws=new WebSocket(targets.find(t=>t.type==='page').webSocketDebuggerUrl);
  ws.addEventListener('message',e=>{const m=JSON.parse(e.data);if(pending.has(m.id)){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(Error(JSON.stringify(m.error))):p.resolve(m.result);}});
  await new Promise((r,j)=>{ws.addEventListener('open',r,{once:true});ws.addEventListener('error',j,{once:true});});
  await call('Page.enable');await call('Runtime.enable');await call('DOM.enable');await call('CSS.enable');
  for(const width of [1440,430,390]) {
    await call('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:width<500});
    await call('Emulation.setTouchEmulationEnabled',{enabled:width<500,maxTouchPoints:5});
    await go('');await ev("scrollTo({top:0,behavior:'instant'});document.querySelector('#r1-tab-bai-hoc').focus({preventScroll:true})");await key('Enter',13);await sleep(450);
    const dockingFocus=await ev("({active:document.activeElement.id,parent:document.querySelector('.r1-section-nav').parentElement.id,y:scrollY})");
    check(`${width}: keyboard focus survives first docking`,dockingFocus.active==='r1-tab-bai-hoc',dockingFocus);
    await go('?r1-view=bai-hoc');await ev("scrollTo({top:0,behavior:'instant'});document.querySelector('#r1-tab-cach-hoc').focus({preventScroll:true})");await key('ArrowRight',39);await sleep(150);
    const focusAudit={undocked:await focusVisualState()};await shot(`${width}_focus_before_docking`);
    await ev("scrollTo({top:1800,behavior:'instant'})");await sleep(500);focusAudit.docked=await focusVisualState();await shot(`${width}_focus_docked`);
    await ev("scrollTo({top:0,behavior:'instant'})");await sleep(500);focusAudit.undockedAgain=await focusVisualState();await shot(`${width}_focus_after_undocking`);
    check(`${width}: exact keyboard focus before docking`,focusPass(focusAudit.undocked,'r1-tab-bai-hoc')&&!focusAudit.undocked.docked,focusAudit.undocked);
    check(`${width}: exact keyboard focus while docked`,focusPass(focusAudit.docked,'r1-tab-bai-hoc')&&focusAudit.docked.docked&&focusAudit.docked.navParent==='quarto-header',focusAudit.docked);
    check(`${width}: exact keyboard focus after undocking`,focusPass(focusAudit.undockedAgain,'r1-tab-bai-hoc')&&!focusAudit.undockedAgain.docked,focusAudit.undockedAgain);
    const focusInventory=await keyboardFocusInventory();
    check(`${width}: all keyboard focus rings are uniform`,focusInventory.length>0&&focusInventory.every(uniformFocusPass),focusInventory.filter(item=>!uniformFocusPass(item)));
    await go('?r1-view=toan-van');
    const summaryFocus={
      closedFirst:await focusCase('#cach-thuc-hien-su-dung-tai-lieu > summary',`${width}_summary_closed_first`,"document.querySelectorAll('.r1-g01 details').forEach(item=>item.open=false);"),
      openMiddle:await focusCase('#cach-thuc-hien-luyen-tap > summary',`${width}_summary_open_middle`,"document.querySelectorAll('.r1-g01 details').forEach(item=>item.open=false);document.querySelector('#cach-thuc-hien-luyen-tap').open=true;"),
      closedLast:await focusCase('#cach-thuc-hien-dung-loi-giai > summary',`${width}_summary_closed_last`,"document.querySelectorAll('.r1-g01 details').forEach(item=>item.open=false);"),
      inner:await focusCase('#loi-giai-2 a[href]',`${width}_details_inner_focus`,"document.querySelectorAll('.r1-g01 details').forEach(item=>item.open=false);document.querySelector('#loi-giai-2').open=true;")
    };
    check(`${width}: summary focus is unclipped when closed and open`,Object.values(summaryFocus).every(state=>focusPass(state)),summaryFocus);
    const summaryGeometry=await ev(`(() => {const details=[...document.querySelectorAll('.r1-g01 details.zo-block')];details.forEach(item=>item.open=true);const summaries=details.map(item=>item.querySelector(':scope > summary'));return {detailsOverflow:details.map(item=>({id:item.id,open:item.open,overflowX:getComputedStyle(item).overflowX,overflowY:getComputedStyle(item).overflowY,clientWidth:item.clientWidth,scrollWidth:item.scrollWidth})),summaryHeights:[...new Set(summaries.map(item=>item.getBoundingClientRect().height))],summaryMinHeights:[...new Set(summaries.map(item=>getComputedStyle(item).minHeight))],icons:summaries.map(item=>{const s=getComputedStyle(item,'::after'),r=item.getBoundingClientRect();return {id:item.parentElement.id,right:s.right,top:s.top,summaryHeight:r.height}})}})()`);
    check(`${width}: details content and summary geometry remain contained`,summaryGeometry.detailsOverflow.every(item=>item.scrollWidth<=item.clientWidth+1)&&summaryGeometry.summaryMinHeights.every(value=>parseFloat(value)>=44),summaryGeometry);
    await go('?r1-view=toan-van');
    const tabFocus={};
    tabFocus.first=await focusCase('#r1-tab-cach-hoc',`${width}_tab_first_start`,"const list=document.querySelector('.r1-tablist');list.scrollLeft=0;");
    tabFocus.middle=await focusCase('#r1-tab-sua-loi',`${width}_tab_middle`,"const list=document.querySelector('.r1-tablist');list.scrollLeft=(list.scrollWidth-list.clientWidth)/2;");
    tabFocus.last=await focusCase('#r1-tab-toan-van',`${width}_tab_last_end`,"const list=document.querySelector('.r1-tablist');list.scrollLeft=list.scrollWidth;");
    tabFocus.scroll=await ev(`(() => {const list=document.querySelector('.r1-tablist'),nav=document.querySelector('.r1-section-nav'),first=document.querySelector('#r1-tab-cach-hoc'),last=document.querySelector('#r1-tab-toan-van'),box=e=>{const r=e.getBoundingClientRect();return {left:r.left,right:r.right,width:r.width,height:r.height}};return {scrollLeft:list.scrollLeft,maxScroll:list.scrollWidth-list.clientWidth,list:box(list),nav:box(nav),first:box(first),last:box(last),pageOverflow:document.documentElement.scrollWidth-document.documentElement.clientWidth};})()`);
    check(`${width}: first, middle and last tab focus is unclipped`,focusPass(tabFocus.first,'r1-tab-cach-hoc')&&focusPass(tabFocus.middle,'r1-tab-sua-loi')&&focusPass(tabFocus.last,'r1-tab-toan-van'),tabFocus);
    check(`${width}: focus gutter preserves tab alignment and page width`,Math.abs(tabFocus.first.rect.left-tabFocus.first.layout.nav.left)<=1&&(tabFocus.scroll.maxScroll<=1||Math.abs(tabFocus.last.rect.right-tabFocus.last.layout.nav.right)<=1)&&tabFocus.scroll.pageOverflow<=1,tabFocus.scroll);
    results.viewports[width]={focusAudit,focusInventory,summaryFocus,summaryGeometry,tabFocus};
    if(args['--focus-only']==='yes')continue;
    await go('?r1-view=toan-van');await ev("scrollTo({top:0,behavior:'instant'})");await sleep(350);
    const tabVisual={undocked:await tabVisualState()};
    const documentNode=await call('DOM.getDocument');const regularNode=await call('DOM.querySelector',{nodeId:documentNode.root.nodeId,selector:'#r1-tab-cach-hoc'});
    await call('CSS.forcePseudoState',{nodeId:regularNode.nodeId,forcedPseudoClasses:['hover']});await sleep(120);tabVisual.hover=await tabVisualState();
    await call('CSS.forcePseudoState',{nodeId:regularNode.nodeId,forcedPseudoClasses:[]});
    await key('Tab',9);await ev("document.querySelector('#r1-tab-toan-van').focus({preventScroll:true})");await sleep(120);tabVisual.focus=await tabVisualState();
    await ev("document.activeElement.blur();scrollTo({top:1800,behavior:'instant'})");await sleep(500);tabVisual.docked=await tabVisualState();
    await ev("scrollTo({top:0,behavior:'instant'})");await sleep(500);tabVisual.undockedAgain=await tabVisualState();
    const tabStates=Object.values(tabVisual),selectedStyles=tabStates.map(state=>state.selected.style);
    check(`${width}: active tab uses only neutral background`,selectedStyles.every(style=>style.background==='rgb(248, 245, 240)'&&style.borderTop==='1px solid rgba(0, 0, 0, 0)'&&style.borderBottom==='1px solid rgba(0, 0, 0, 0)'&&style.boxShadow==='none'&&style.fontWeight==='400'));
    check(`${width}: tab pseudo-elements add no edge`,tabStates.every(state=>state.selected.before.content==='none'&&state.selected.before.boxShadow==='none'&&state.selected.after.content==='none'&&state.selected.after.boxShadow==='none'));
    check(`${width}: tab dimensions stay stable through docking`,selectedStyles.every(style=>style.width===selectedStyles[0].width&&style.height===selectedStyles[0].height&&style.padding===selectedStyles[0].padding),selectedStyles);
    check(`${width}: keyboard focus remains visible`,tabVisual.focus.selected.focusVisible&&tabVisual.focus.selected.style.outline!=='none'&&tabVisual.focus.selected.style.outline!=='rgb(0, 0, 0) none 0px',tabVisual.focus.selected.style);
    check(`${width}: hover uses text color without underline or lower edge`,tabVisual.hover.regular.hover&&tabVisual.hover.regular.style.color==='rgb(37, 34, 31)'&&tabVisual.hover.regular.style.textDecoration==='none'&&tabVisual.hover.regular.style.boxShadow==='none'&&tabVisual.hover.regular.style.borderBottom==='1px solid rgba(0, 0, 0, 0)',tabVisual.hover.regular);
    check(`${width}: dock and undock preserve tab appearance`,!tabVisual.undocked.docked&&tabVisual.docked.docked&&!tabVisual.undockedAgain.docked&&tabVisual.docked.navParent==='quarto-header'&&tabVisual.docked.selected.style.background===tabVisual.undocked.selected.style.background&&tabVisual.docked.selected.style.boxShadow===tabVisual.undocked.selected.style.boxShadow,tabVisual);
    await go('?r1-view=toan-van');await ev("scrollTo({top:0,behavior:'instant'})");await sleep(350);
    const stripBefore=await stripState();
    if(args['--strip-only']==='yes'){
      await ev("scrollTo({top:1800,behavior:'instant'})");await sleep(400);const stripAfter=await stripState();
      check(`${width}: horizontal tab position survives docking`,stripBefore.visible&&stripAfter.visible,{stripBefore,stripAfter});continue;
    }
    const top=await ev(rectScript);await shot(`${width}_top`);await begin();
    await wheel(650,'down_title',width);await wheel(1800,'down_deep',width);
    await wheel(-260,'up',width);await wheel(180,'down_again',width);await wheel(-180,'up_again',width);
    const stripAfter=await stripState();check(`${width}: horizontal tab position survives docking`,stripBefore.visible&&stripAfter.visible,{stripBefore,stripAfter});
    const frames=await ev('window.__r1record=false;window.__r1frames');
    const deep=frames.filter(f=>f.y>1100);
    const visible=deep.filter(f=>f.nav.bottom>0&&f.header.bottom>0);
    const hidden=deep.filter(f=>f.header.bottom<=0);
    check(`${width}: flush throughout motion`,visible.length>5&&visible.every(f=>Math.abs(f.gap)<=1),{frames:visible.length,maxGap:Math.max(...visible.map(f=>Math.abs(f.gap)))});
    check(`${width}: directly beneath actual navbar`,visible.length>0&&visible.every(f=>Math.abs(f.nav.top-f.navbar.bottom)<=1),{maxGap:Math.max(...visible.map(f=>Math.abs(f.nav.top-f.navbar.bottom)))});
    check(`${width}: identical movement`,visible.slice(1).every((f,i)=>Math.abs((f.nav.top-visible[i].nav.top)-(f.navbar.top-visible[i].navbar.top))<1));
    // During hiding, a contiguous trailing edge is valid; a stationary orphan is not.
    const settledHidden=deep.filter((f,i)=>i>=5&&f.header.bottom<=0&&
      deep.slice(i-5,i).every(p=>p.phase===f.phase&&Math.abs(p.header.top-f.header.top)<.1)&&
      f.time-deep[i-5].time>=60);
    check(`${width}: no orphan after navbar hides`,settledHidden.length>0&&settledHidden.every(f=>f.nav.bottom<=1),{frames:settledHidden.length,maxNavBottom:Math.max(...settledHidden.map(f=>f.nav.bottom))});
    check(`${width}: no page overflow`,frames.every(f=>f.overflow<=1),Math.max(...frames.map(f=>f.overflow)));
    results.viewports[width]={...results.viewports[width],top,frames,tabVisual};
    // A tab selected while reading deeply must reveal its heading without an intermediate jump to title.
    await ev("document.querySelector('#r1-tab-bai-hoc').click()");await sleep(700);
    const destination=await ev(`({...${rectScript},target:document.querySelector('#bai-hoc > h2').getBoundingClientRect().top,navCount:document.querySelectorAll('.r1-section-nav').length})`);
    check(`${width}: deep tab destination clear`,destination.target>=Math.max(0,destination.header.bottom,destination.nav.bottom)-1&&destination.target<500&&destination.navCount===1,destination);
    await shot(`${width}_tab_destination`);
    await ev("scrollTo({top:0,behavior:'instant'})");await sleep(350);
    const restored=await ev(rectScript);
    check(`${width}: return to top preserves position`,Math.abs(restored.nav.top-top.nav.top)<2,{before:top.nav,after:restored.nav});
    if(width<500){
      await ev("scrollTo({top:1800,behavior:'instant'})");await sleep(300);await wheel(-200,'menu_up',width);
      await ev("document.querySelector('.navbar-toggler').click()");await sleep(450);
      const menu=await ev(`(() => {const m=document.querySelector('.navbar-collapse'),n=document.querySelector('.r1-section-nav');const mr=m.getBoundingClientRect(),nr=n.getBoundingClientRect();return {open:m.classList.contains('show'),menuBottom:mr.bottom,navTop:nr.top,navHidden:getComputedStyle(n).visibility==='hidden',inert:n.inert};})()`);
      check(`${width}: open navbar menu unobstructed`,menu.open&&(menu.navHidden||menu.navTop>=menu.menuBottom-1),menu);await shot(`${width}_menu_open`);
      await ev("document.querySelector('.navbar-toggler').click()");await sleep(450);
      const closed=await ev(rectScript);check(`${width}: menu closes to flush dock`,Math.abs(closed.gap)<1&&closed.visibility==='visible',closed);
    }
    await go('#cach-thuc-hien-don-dieu');
    const guidance=await ev(`(() => {const d=document.querySelector('#cach-thuc-hien-don-dieu');return {open:d.open,native:d.tagName==='DETAILS',top:d.getBoundingClientRect().top,summaryRole:d.querySelector('summary').getAttribute('role'),aria:d.querySelector('summary').getAttribute('aria-expanded')};})()`);
    const linked=await targetState();check(`${width}: native guidance hash opens clear`,guidance.open&&guidance.native&&!guidance.summaryRole&&!guidance.aria&&linked.targetTop>=linked.cover-1,{guidance,linked});
    await ev("document.querySelector('#cach-thuc-hien-don-dieu > summary').focus({preventScroll:true})");await key('Enter',13);
    check(`${width}: guidance keyboard closes`,await ev("!document.querySelector('#cach-thuc-hien-don-dieu').open"));await key('Enter',13);
    check(`${width}: guidance keyboard opens`,await ev("document.querySelector('#cach-thuc-hien-don-dieu').open"));
    await go('#lt01');await link('#loi-giai-2',"document.getElementById('lt01')");await sleep(600);
    const answer=await targetState();
    check(`${width}: answer link clear and focused`,answer.hash==='#loi-giai-2'&&answer.targetTop>=answer.cover-1,answer);
    await link('#lt01',"document.getElementById('loi-giai-2')");await sleep(550);
    const backToQuestion=await targetState();check(`${width}: return to question`,backToQuestion.hash==='#lt01'&&backToQuestion.targetTop>=backToQuestion.cover-1,backToQuestion);
    await ev('history.back()');await sleep(500);const back=await targetState();
    await ev('history.forward()');await sleep(500);const forward=await targetState();
    check(`${width}: Back/Forward`,back.hash===answer.hash&&forward.hash===backToQuestion.hash,{back,forward});
    await go('?r1-view=toan-van#lt01');await link('#loi-giai-2',"document.getElementById('lt01')");await sleep(500);
    const allAnswer=await targetState();check(`${width}: full text answer keeps view`,allAnswer.view==='toan-van'&&allAnswer.visible.length===10,allAnswer);
    await link('#lt01',"document.getElementById('loi-giai-2')");await sleep(400);
    check(`${width}: full text return keeps view`,(await targetState()).view==='toan-van');
    await go('#xem-toan-bo');check(`${width}: old full-text alias`,(await targetState()).view==='toan-van');
    const inventory=await ev(`(() => {const r=document.querySelector('.r1-g01'),ids=[...document.querySelectorAll('[id]')].map(e=>e.id),css=e=>{const c=getComputedStyle(e);return {color:c.color,background:c.backgroundColor,weight:c.fontWeight}};return {math:r.querySelectorAll('math').length,answers:r.querySelectorAll('.answer-link').length,details:r.querySelectorAll('details:not(.r1-section-toc)').length,guidance:r.querySelectorAll('.r1-guidance').length,tables:r.querySelectorAll('.r1-data-table').length,bbt:r.querySelectorAll('.zo-variation-asset').length,figures:r.querySelectorAll('figure').length,duplicates:ids.length-new Set(ids).size,tabs:[...document.querySelectorAll('.r1-tab')].map(t=>t.textContent),h1:css(document.querySelector('h1.title')),h2:css(r.querySelector('h2')),h3:css(r.querySelector('h3')),tableHeaders:[...r.querySelectorAll('.r1-data-table th')].map(css)};})()`);
    check(`${width}: canonical inventory preserved`,inventory.math===989&&inventory.answers===42&&inventory.details===31&&inventory.guidance===15&&inventory.tables===17&&inventory.bbt===13&&inventory.figures===10&&inventory.duplicates===0,inventory);
    check(`${width}: table emphasis and headings preserved`,inventory.tableHeaders.every(c=>c.weight==='400'&&c.background==='rgb(255, 255, 255)')&&inventory.h1.color==='rgb(239, 83, 80)'&&inventory.h2.color===inventory.h1.color&&inventory.h3.color!==inventory.h1.color);
    await ev("document.querySelector('#r1-tab-tai-pdf').click()");await sleep(450);
    const cards=await ev("[...document.querySelectorAll('.r1-download-card h3')].map(e=>e.textContent)");check(`${width}: distinct PDF labels remain`,cards.includes('Bản đầy đủ')&&cards.includes('Bản học và bài tập'),cards);await shot(`${width}_downloads`);await shotElement(`${width}_downloads_full`,'#tai-tai-lieu');
    results.viewports[width].sectionDownloads=await sectionDownloadsState();
    const sectionDownloads=results.viewports[width].sectionDownloads;
    check(`${width}: six section downloads are compact and unclipped`,sectionDownloads.count===6&&sectionDownloads.cards===0&&sectionDownloads.inside&&sectionDownloads.scrollWidth<=sectionDownloads.clientWidth+1&&sectionDownloads.items.every(item=>item.overflow<=1),sectionDownloads);
    check(`${width}: section download order matches tabs`,sectionDownloads.items.map(item=>item.title).join('|')==='Bài học|Luyện tập|Kiểm tra|Sửa lỗi|Ôn lại|Lời giải',sectionDownloads.items);
    results.viewports[width].account=await accountVisualState();
    const account=results.viewports[width].account;
    check(`${width}: account container uses neutral framed surface`,account.background==='rgb(248, 245, 240)'&&account.border==='1px solid rgb(222, 226, 230)'&&account.boxShadow==='none'&&account.fontWeight==='400'&&parseFloat(account.padding)>=20,account);
    check(`${width}: account content is not clipped`,account.inside&&account.notClipped&&account.scrollWidth<=account.clientWidth+1,account);
    await ev("document.querySelector('#r1-tab-tai-pdf').focus({preventScroll:true})");await key('ArrowRight',39);
    check(`${width}: arrow changes focus only`,(await targetState()).view==='tai-pdf'&&await ev("document.activeElement.id==='r1-tab-toan-van'"));await key('Enter',13);await sleep(400);
    check(`${width}: Enter activates full text`,(await targetState()).view==='toan-van');
    if(width<500){
      await ev("document.querySelectorAll('.r1-g01 details').forEach(d=>d.open=true)");
      const touch=[];
      for(const id of ['04','05','06','07','08','12','13','14','15','17']) {
        const selector=`#r1-table-t${id}`;
        const start=await ev(`(() => {const e=document.querySelector('${selector}');e.scrollIntoView({block:'center',behavior:'instant'});e.scrollLeft=0;const r=e.getBoundingClientRect();return {x:r.left+r.width*.8,y:Math.max(180,Math.min(650,r.top+r.height/2)),width:e.clientWidth,scrollWidth:e.scrollWidth}})()`);await sleep(250);
        const swipe=async vertical=>{const before=await ev(`({x:document.querySelector('${selector}').scrollLeft,y:scrollY})`);await call('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:start.x,y:start.y,id:1}]});for(let step=1;step<=8;step++){await call('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:start.x-(vertical?0:step*20),y:start.y-(vertical?step*18:0),id:1}]});await sleep(24);}await call('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await sleep(200);return {before,after:await ev(`({x:document.querySelector('${selector}').scrollLeft,y:scrollY})`)};};
        const horizontal=await swipe(false);check(`${width}: touch table T${id}`,horizontal.after.x-horizontal.before.x>30,horizontal);
        const vertical=id==='04'?await swipe(true):null;if(vertical)check(`${width}: vertical touch remains`,vertical.after.y-vertical.before.y>30,vertical);
        await ev(`document.querySelector('${selector}').focus({preventScroll:true});document.querySelector('${selector}').scrollLeft=0`);await key('ArrowRight',39);
        check(`${width}: table T${id} arrow does not switch tab`,(await targetState()).view==='toan-van'&&await ev(`document.querySelector('${selector}').scrollLeft>0`));
        touch.push({id,horizontal,vertical});
      }
      results.viewports[width].touch=touch;
    }
    await ev("document.querySelector('[data-bbt=BBT01]').scrollIntoView({block:'center',behavior:'instant'})");await sleep(300);await shot(`${width}_bbt`);
  }
  await call('Emulation.setScriptExecutionDisabled',{value:true});await call('Page.navigate',{url});await sleep(1200);
  const nojs=await ev(`(() => {const suffix='content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.html', links=selector=>[...document.querySelectorAll(selector)].filter(a=>new URL(a.href,location.href).pathname.endsWith(suffix)).map(a=>({text:a.textContent.trim().replace(/\\s+/g,' '),href:a.getAttribute('href'),path:new URL(a.href,location.href).pathname}));return {tabs:document.querySelectorAll('.r1-tab').length,sections:document.querySelectorAll('.r1-g01 > section').length,hidden:document.querySelectorAll('.r1-g01 > section[hidden]').length,packagePdfs:document.querySelectorAll('.r1-downloads a[download]').length,sectionPdfs:document.querySelectorAll('.r1-section-download-list a[download]').length,sidebar:links('#quarto-sidebar a[href]'),breadcrumb:links('.quarto-page-breadcrumbs a[href]')};})()`);
  check('no-JS linear content and downloads',nojs.tabs===0&&nojs.sections===10&&nojs.hidden===0&&nojs.packagePdfs===2&&nojs.sectionPdfs===6,nojs);
  const officialTitle='Kết nối hàm số, bảng biến thiên và đồ thị';
  check('no-JS sidebar and breadcrumb use the learning-material title',nojs.sidebar.length===1&&nojs.breadcrumb.length===1&&nojs.sidebar[0].text===officialTitle&&nojs.breadcrumb[0].text===officialTitle&&!nojs.sidebar[0].text.includes('R1-G01')&&!nojs.breadcrumb[0].text.includes('R1-G01'),{sidebar:nojs.sidebar,breadcrumb:nojs.breadcrumb});
} catch(error){results.error=String(error);check('runtime completed',false,String(error));}
finally {
  fs.writeFileSync(path.join(out,'navbar.json'),JSON.stringify(results,null,2));
  try{await call('Browser.close')}catch{};ws?.close();child.kill();await sleep(600);
  if(path.dirname(profile)===out&&path.basename(profile).startsWith('browser-cache-'))fs.rmSync(profile,{recursive:true,force:true,maxRetries:10,retryDelay:300});
}
console.log(JSON.stringify({checks:results.checks.length,failures:results.checks.filter(c=>!c.ok),error:results.error,report:path.join(out,'navbar.json')},null,2));
process.exitCode=results.checks.some(c=>!c.ok)?1:0;

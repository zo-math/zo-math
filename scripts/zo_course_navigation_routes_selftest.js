/* Source-only regression fixtures: no browser, page rendering, or saved HTML. */
const fs=require('fs'),path=require('path'),vm=require('vm');
const root=path.resolve(__dirname,'..');
const source=fs.readFileSync(path.join(root,'_design/web_2027_mau_dung_chung/r1-controller.js'),'utf8');
const checks={};function check(name,value){checks[name]=!!value;}
function fn(name){const start=source.indexOf('    function '+name+'(');if(start<0)throw Error(name);const end=source.indexOf('\n    function ',start+1);return source.slice(start,end<0?undefined:end);}
const base='http://127.0.0.1:8877/content/thpt/on_thi_toan_thpt/hoc_lieu/';
const targets=new Map(['CP01','CP-O03','nen-mien','nen-gioi-han'].map(id=>[id,{id}]));
function element(tag){return {tag,dataset:{},children:[],append(...n){this.children.push(...n)},replaceChildren(...n){this.children=n}};}
const bar=element('aside');
const sandbox={URL,URLSearchParams,location:new URL(base+'r1_g04/index.html?r1-view=on-nen&r1-return=CP-O03#nen-gioi-han'),
 root:{contains:()=>true},byView:new Map(['bat-dau','bai-hoc','luyen-tap','kiem-tra','on-lai','on-nen','sua-loi','nhat-ky','loi-giai','nguon','toan-van'].map(x=>[x,{}])),
 VIEW_PARAM:'r1-view',RETURN_PARAM:'r1-return',CONTEXT_PARAM:'r1-context',returnBar:bar,
 document:{getElementById:id=>targets.get(id),createElement:element,createTextNode:text=>({text})},
 sourceCheckpoint:()=>new URLSearchParams(sandbox.location.search).get('r1-return')||'nen-mien',
 ownerView:node=>node.id.startsWith('CP')?'on-lai':'on-nen',checkpointLabel:id=>'Hoạt động '+id,supportTarget:()=>false,directReturnOptions:()=>[]};
vm.createContext(sandbox);
for(const name of ['externalReturn','externalReturnUrl','decorateExternalSupport','renderExternalReturn','renderReturnBar','urlFor'])vm.runInContext(fn(name),sandbox);
function link(href,returning=false){return {href:new URL(href,sandbox.location.href).href,classList:{contains:()=>returning},closest:()=>({id:'nen-mien'})};}
let a=link('../r1_g03/index.html?r1-view=on-nen#N-GH-02');sandbox.decorateExternalSupport(a);
let url=new URL(a.href,sandbox.location.href);
check('cross-package call keeps original review checkpoint',url.searchParams.get('r1-return')==='CP-O03'&&url.searchParams.get('r1-return-page')==='r1_g04'&&url.searchParams.get('r1-return-view')==='on-lai');
check('cross-package call keeps target view and anchor',url.searchParams.get('r1-view')==='on-nen'&&url.hash==='#N-GH-02');
sandbox.location=url;
check('direct URL and reload recover return context',sandbox.externalReturn()?.id==='CP-O03');
sandbox.renderReturnBar({id:'N-GH-02'});
check('return bar identifies external owner',bar.dataset.r1ExternalReturn==='true'&&!bar.hidden&&bar.children.length===1);
let back=new URL(bar.children[0].href,sandbox.location.href);
check('external return reaches original page view and checkpoint',back.pathname.endsWith('/r1_g04/index.html')&&back.searchParams.get('r1-view')==='on-lai'&&back.hash==='#CP-O03');
let consulted=new URL(sandbox.urlFor('loi-giai','lg-L01',null),sandbox.location.href);
check('local solution consultation keeps original caller',consulted.searchParams.get('r1-return-page')==='r1_g04'&&consulted.searchParams.get('r1-return')==='CP-O03');
a=link('../r1_g02/index.html?r1-view=on-nen#nen-n-gh-01');sandbox.decorateExternalSupport(a);url=new URL(a.href,sandbox.location.href);
check('second support package retains original caller',url.searchParams.get('r1-return-page')==='r1_g04'&&url.searchParams.get('r1-return')==='CP-O03');
sandbox.location=new URL(base+'r1_g03/index.html?'+url.searchParams.toString()+'#N-GH-02');
a=link('../r1_g04/index.html?r1-view=on-lai#CP-O03',true);const saved=a.href;sandbox.decorateExternalSupport(a);
check('return link is never redecorated',a.href===saved);
for(const href of ['https://example.com/hoc_lieu/r1_g02/index.html?r1-view=on-nen#x','../r1_g02/index.html?r1-view=bat-dau#bat-dau','#N-GH-03']){
 a=link(href);const prior=a.href;sandbox.decorateExternalSupport(a);check('ordinary link unchanged '+href,a.href===prior);
}
for(const query of ['r1-return-page=../../other&r1-return=x&r1-return-view=on-nen','r1-return-page=r1_g04&r1-return=x&r1-return-view=unknown','r1-return-page=r1_g04&r1-return-view=on-nen']){
 sandbox.location=new URL(base+'r1_g03/index.html?'+query);check('reject invalid context '+query,sandbox.externalReturn()===null);
}
sandbox.location=new URL(base+'r1_g03/index.html?r1-view=on-nen');sandbox.renderReturnBar({id:'none'});
check('stale external marker cleared on ordinary entry',bar.dataset.r1ExternalReturn===undefined&&bar.hidden);
sandbox.location=new URL(base+'r1_g04/index.html?r1-view=on-nen#nen-mien');
a=link('../r1_g01/index.html?r1-view=on-nen#nen-n-txd-01');sandbox.decorateExternalSupport(a);url=new URL(a.href,sandbox.location.href);
check('direct resource caller gets its own return anchor',url.searchParams.get('r1-return')==='nen-mien');
const events={};sandbox.root.addEventListener=(name,handler)=>{events[name]=handler};
const eventStart=source.indexOf("    for (const type of ['pointerdown', 'focusin', 'click', 'auxclick'])");
const eventEnd=source.indexOf("    root.addEventListener('click', event => {",eventStart);
vm.runInContext(source.slice(eventStart,eventEnd),sandbox);
for(const type of ['pointerdown','focusin','click','auxclick']){
 a=link('../r1_g03/index.html?r1-view=on-nen#N-GH-02');events[type]({target:{closest:()=>a}});url=new URL(a.href,sandbox.location.href);
 check('caller prepared for native navigation '+type,url.searchParams.get('r1-return-page')==='r1_g04');
}
// Model independent tabs from their separate URLs; there is no shared storage.
sandbox.location=new URL(base+'r1_g01/index.html?r1-return-page=r1_g04&r1-return=CP01&r1-return-view=luyen-tap');const tab1=sandbox.externalReturn();
sandbox.location=new URL(base+'r1_g01/index.html?r1-return-page=r1_g03&r1-return=CP-O03&r1-return-view=on-lai');const tab2=sandbox.externalReturn();
check('tabs retain independent callers',tab1.page==='r1_g04'&&tab1.id==='CP01'&&tab2.page==='r1_g03'&&tab2.id==='CP-O03');
const g02=fs.readFileSync(path.join(root,'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02/giao_dien/support-context.js'),'utf8');
check('G02 defers validated external return to shared owner',g02.includes("if(bar.dataset.r1ExternalReturn==='true')return;"));
// Execute the actual shared drawer click handler with Home and D0 anchors.
const ui=fs.readFileSync(path.join(root,'_design/web_2027_mau_dung_chung/site-ui.js'),'utf8');
const start=ui.indexOf("  dialog.addEventListener('click', event => {");const end=ui.indexOf("  matchMedia(",start);
let callback,closed=0;const target={id:'chon-mach'};
const shell={dialog:{addEventListener:(name,handler)=>{callback=handler}},document:{getElementById:id=>id==='chon-mach'?target:null},closeDrawer:()=>closed++,pendingDestination:null};vm.createContext(shell);vm.runInContext(ui.slice(start,end),shell);
for(const context of ['home','d0']){
 shell.pendingDestination=null;callback({target:{closest:selector=>selector.includes('.'+(context==='d0'?'d0':'home')+'-nav a')?{hash:'#chon-mach'}:null}});
 check(context+' drawer closes and selects focus destination',closed>0&&shell.pendingDestination===target);
}
vm.runInContext(fn('openAncestors'),sandbox);
const owned={tagName:'DETAILS',open:false,closest:()=>section};
const unrelated={tagName:'DETAILS',open:false,closest:()=>({})};
const section={tagName:'SECTION',parentElement:sandbox.root,matches:()=>true,querySelectorAll:()=>[unrelated,owned]};
sandbox.openAncestors(section);
check('solution section opens its owned disclosure',owned.open);
check('solution section keeps unrelated disclosures closed',!unrelated.open);
const grouped={tagName:'SECTION',parentElement:sandbox.root,matches:()=>false,querySelectorAll:()=>[unrelated]};
sandbox.openAncestors(grouped);check('solution group does not reveal all answers',!unrelated.open);
const direct={tagName:'DETAILS',parentElement:sandbox.root,matches:()=>true,open:false};
sandbox.openAncestors(direct);check('direct disclosure targets still open',direct.open);
const report={checks,passed:Object.values(checks).filter(Boolean).length,total:Object.keys(checks).length,failures:Object.keys(checks).filter(k=>!checks[k]),html_built:false,browser_checked:false};
console.log(JSON.stringify(report,null,2));
if(process.argv[2]){
 const output=path.resolve(process.argv[2]);if(!output.startsWith(path.join(root,'_audit')+path.sep))throw Error('Audit report path required');fs.writeFileSync(output,JSON.stringify(report,null,2)+'\n');
}
process.exitCode=report.failures.length?1:0;
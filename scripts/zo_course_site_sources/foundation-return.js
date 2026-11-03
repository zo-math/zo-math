/* A return destination must be a real, known course and a real source anchor. */
(() => {
  const data=JSON.parse(document.querySelector('#page-data').textContent);
  const query=new URLSearchParams(location.search);
  const id=query.get('r1-return-page'),target=query.get('r1-return');
  const p=(data.catalog||[]).find(p=>p.id===id);
  if(!p||!target||target.length>256)return;
  const url=new URL(p.url,location.href);
  if(url.origin!==location.origin)return;
  fetch(url,{credentials:'same-origin'}).then(r=>r.ok?r.text():null).then(text=>{
    if(!text)return;
    const doc=new DOMParser().parseFromString(text,'text/html');
    const node=doc.getElementById(target);
    if(!node||!node.closest('.reader-content'))return;
    const box=document.querySelector('#foundation-return');
    const link=document.createElement('a');link.className='text-link';
    url.hash=target;if(query.get('r1-return-view')==='toan-van')url.searchParams.set('view','toan-van');link.href=url.href;link.textContent='Quay lại '+p.title;
    box.replaceChildren(link);box.hidden=false;
  }).catch(()=>{});
})();

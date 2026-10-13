/* D0 view enhancement. Never moves source content or gates entry into learning. */
(() => {
  const root=document.querySelector('.d0-package[data-d0-views]');
  if(!root)return;
  const views=JSON.parse(root.dataset.d0Views), sections=[...root.children].filter(n=>views.includes(n.id));
  const links=[...document.querySelectorAll('.d0-nav a')];
  const owner=target=>sections.find(n=>n===target||n.contains(target))?.id;
  function show(id){
    id=views.includes(id)?id:views[0];
    sections.forEach(n=>n.hidden=n.id!==id);
    links.forEach(n=>{if(decodeURIComponent(n.hash.slice(1))===id)n.setAttribute('aria-current','page');else n.removeAttribute('aria-current')});
    root.dataset.d0View=id;
    return id;
  }
  function reveal(target){
    for(let n=target;n&&n!==root;n=n.parentElement)if(n.tagName==='DETAILS')n.open=true;
    requestAnimationFrame(()=>{
      target.scrollIntoView({block:'start'});
      const focus=target.matches('details')?target.querySelector('summary'):target.querySelector('h2,h3,h4')||target;
      if(!focus.matches('summary'))focus.setAttribute('tabindex','-1');
      focus.focus({preventScroll:true});
    });
  }
  function apply(){
    let target=null;try{target=document.getElementById(decodeURIComponent(location.hash.slice(1)))}catch{}
    show(owner(target)||new URLSearchParams(location.search).get('d0-view'));
    if(owner(target))reveal(target);
  }
  document.addEventListener('click',event=>{
    const link=event.target.closest('a[href]');if(!link||event.defaultPrevented||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey||event.button!==0)return;
    const destination=new URL(link.href,location.href);
    if(destination.origin!==location.origin||destination.pathname!==location.pathname||!destination.hash)return;
    let target;try{target=document.getElementById(decodeURIComponent(destination.hash.slice(1)))}catch{return}
    const id=owner(target);if(!id)return;
    event.preventDefault();show(id);
    destination.searchParams.set('d0-view',id);
    history.pushState({d0View:id},'',destination.pathname+destination.search+destination.hash);
    reveal(target);
  });
  apply();addEventListener('popstate',apply);addEventListener('hashchange',apply);
})();

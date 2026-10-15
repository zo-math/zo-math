/* Native details and real links remain functional without JavaScript. */
(() => {
  const header=document.querySelector('.site-top--course-navigation');
  if(!header)return;
  const menu=header.querySelector('.zo-course-menu'), summary=menu.querySelector('summary');
  const close=()=>{menu.open=false};
  document.addEventListener('pointerdown',event=>{if(!menu.contains(event.target))close()});
  document.addEventListener('focusin',event=>{if(!menu.contains(event.target))close()});
  document.addEventListener('keydown',event=>{if(event.key==='Escape'&&menu.open){event.preventDefault();close();summary.focus()}});
  menu.querySelectorAll('a').forEach(link=>link.addEventListener('click',close));
  window.addEventListener('pageshow',close);
  window.addEventListener('resize',close);
  header.querySelector('[data-course-action=top]').addEventListener('click',event=>{
    event.preventDefault();close();
    window.scrollTo({top:0,behavior:'instant'});
  });
})();

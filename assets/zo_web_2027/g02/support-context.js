/* G02-specific route data only. The frozen shared controller stays unchanged. */
(() => {
  const root=document.querySelector('[data-r1-code="R1-G02"]');
  const bar=root?.querySelector('.r1-support-return');
  if(!bar)return;
  const labels={
    'cp-lt1':'Điểm dừng sau chặng 1','cp-lt2':'Điểm dừng sau chặng 2',
    'cp-lt3':'Điểm dừng sau chặng 3','cp-kt':'Điểm dừng sau Kiểm tra',
    'cp-on1':'Điểm dừng Ôn lại 1','cp-on2':'Điểm dừng Ôn lại 2',
    'cp-on3':'Điểm dừng Ôn lại 3','cp-p':'Điểm dừng Chuyển giao',
    'bắt-đầu-từ-đâu':'Khởi động'
  };
  const label=id=>labels[id]||document.getElementById(id)?.querySelector('h3,h4,h5')?.textContent.trim()||'bài vừa làm';
  const owner=id=>{
    const target=document.getElementById(id);
    if(target?.closest('#on-lai'))return 'on-lai';
    if(target?.closest('#tu-kiem-tra'))return 'kiem-tra';
    if(target?.closest('#bai-hoc'))return 'bai-hoc';
    if(target?.closest('#sua-loi'))return 'sua-loi';
    return 'luyen-tap';
  };
  const all=['bắt-đầu-từ-đâu','bai-hoc','cp-lt1','cp-lt2','cp-lt3','cp-kt','cp-on1','cp-on2','cp-on3','cp-p'];
  function update(){
    if(bar.hidden)return;
    // The shared controller owns return routes to another package.
    if(bar.dataset.r1ExternalReturn==='true')return;
    const params=new URLSearchParams(location.search),returnId=params.get('r1-return'),context=params.get('r1-context');
    let hash='';try{hash=decodeURIComponent(location.hash.slice(1));}catch{}
    const target=document.getElementById(hash);
    const fragment=document.createDocumentFragment();
    function link(id,text){
      const a=document.createElement('a');a.className='r1-return-link';
      a.href=`?r1-view=${owner(id)}#${encodeURIComponent(id)}`;a.textContent=text||label(id);return a;
    }
    const span=document.createElement('span');
    if(returnId&&document.getElementById(returnId)){
      span.textContent=context?`Đang hỗ trợ từ ${label(context)}. `:'Đang ở nhánh hỗ trợ. ';
      fragment.append(span,link(returnId,`Quay lại ${label(returnId)}`));
    }else{
      const id=target?.id||'';
      const choices=id.startsWith('s-k-')?['cp-kt']:id.startsWith('s-o-')?['cp-on1','cp-on2','cp-on3']:id.startsWith('s-p')?['cp-p']:id.startsWith('s-l-')?['cp-lt1','cp-lt2','cp-lt3']:all;
      span.textContent='Em mở trực tiếp tài nguyên hỗ trợ này. Chọn nơi cần quay về: ';
      fragment.append(span);
      choices.forEach((id,i)=>{if(i)fragment.append(document.createTextNode(' · '));fragment.append(link(id));});
    }
    const probe=document.createElement('div');probe.append(fragment);
    if(bar.innerHTML!==probe.innerHTML)bar.replaceChildren(...probe.childNodes);
  }
  new MutationObserver(update).observe(bar,{childList:true});
  addEventListener('hashchange',update);addEventListener('popstate',update);update();
})();

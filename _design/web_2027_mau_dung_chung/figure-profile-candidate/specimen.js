/* Authoring preview only. Does not write learner preferences/localStorage. */
const profile=JSON.parse(document.querySelector('#frame-config').textContent);
const frame=document.querySelector('.zo-cover-frame');
function refreshFrame(){
  const shape=document.querySelector('#shape').value,size=document.querySelector('#size').value;
  const background=document.querySelector('input[name=frame-bg]:checked').value;
  const [w,h]=profile.sizes_px[shape][size];
  frame.style.setProperty('--frame-width',w+'px');
  frame.style.setProperty('--frame-ratio',w+'/'+h);
  frame.style.setProperty('--frame-bg',profile.colors[background]);
  frame.dataset.shape=shape;frame.dataset.size=size;frame.dataset.background=background;
  frame.querySelector('img').src=background.endsWith('-dark')?'assets/cover-dark.svg':'assets/cover-light.svg';
  document.querySelector('#frame-description').textContent=`${w} × ${h} px — khung thu theo màn hình; hình không bị cắt hay kéo méo.`;
}
document.querySelectorAll('.authoring-tools input,.authoring-tools select').forEach(n=>n.addEventListener('change',refreshFrame));
refreshFrame();

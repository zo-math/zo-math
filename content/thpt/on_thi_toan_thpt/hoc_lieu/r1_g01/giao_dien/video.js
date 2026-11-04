/* Optional lesson videos: load only on request; stop when their view closes. */
(() => {
  'use strict';
  const videos = [...document.querySelectorAll('.zo-learning-video[data-youtube-id]')];
  function visible(video) {
    if (!video.open || video.closest('[hidden]') || !video.getClientRects().length) return false;
    for (let node = video.parentElement; node; node = node.parentElement) {
      if (node.matches('details:not([open])')) return false;
    }
    return true;
  }
  function sync() {
    videos.forEach(video => {
      const host = video.querySelector('.zo-video-player');
      if (!visible(video)) { host.replaceChildren(); return; }
      if (host.firstChild) return;
      const id = video.dataset.youtubeId;
      if (!/^[\w-]{11}$/.test(id)) return;
      const frame = document.createElement('iframe');
      frame.src = `https://www.youtube-nocookie.com/embed/${id}?playsinline=1&rel=0`;
      frame.title = video.querySelector('summary').textContent.trim();
      frame.allow = 'accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen';
      frame.allowFullscreen = true;
      frame.referrerPolicy = 'strict-origin-when-cross-origin';
      host.append(frame);
    });
  }
  document.addEventListener('toggle', sync, true);
  window.addEventListener('hashchange', sync);
  window.addEventListener('popstate', sync);
  new MutationObserver(sync).observe(document.body, {
    subtree: true, attributes: true, attributeFilter: ['hidden', 'open']
  });
  sync();
})();

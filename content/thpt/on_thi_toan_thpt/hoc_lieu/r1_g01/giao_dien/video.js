/* Optional videos: lazy load, clear release notices, stop when hidden. */
(() => {
  'use strict';
  const videos = [...document.querySelectorAll('.zo-learning-video[data-youtube-id]')];
  const players = new Map();
  let api;
  function youtubeAPI() {
    if (window.YT?.Player) return Promise.resolve(window.YT);
    if (api) return api;
    api = new Promise((resolve, reject) => {
      const script = document.createElement('script');
      const previous = window.onYouTubeIframeAPIReady;
      const timer = setTimeout(() => reject(new Error('YouTube API timeout')), 15000);
      window.onYouTubeIframeAPIReady = () => {
        clearTimeout(timer);
        resolve(window.YT);
        if (typeof previous === 'function') previous();
      };
      script.src = 'https://www.youtube.com/iframe_api';
      script.async = true;
      script.onerror = () => { clearTimeout(timer); reject(new Error('YouTube API unavailable')); };
      document.head.append(script);
    }).catch(error => { api = null; throw error; });
    return api;
  }
  function clearNotice(video) {
    video.querySelectorAll('.zo-video-status, .zo-video-retry').forEach(node => node.remove());
  }
  function stop(video) {
    players.get(video)?.destroy();
    players.delete(video);
    video.querySelector('.zo-video-player').replaceChildren();
  }
  function trackAvailability(video, frame) {
    const current = () => frame.isConnected && video.querySelector('iframe') === frame;
    youtubeAPI().then(YT => {
      if (!current()) return;
      const available = () => {
        if (!current()) return;
        clearNotice(video);
        video.dataset.publicPlayback = 'public';
      };
      const player = new YT.Player(frame, { events: {
        onReady: available,
        onStateChange: event => {
          if ([YT.PlayerState.PLAYING, YT.PlayerState.CUED].includes(event.data)) available();
        }
      }});
      players.set(video, player);
    }).catch(() => { /* Playback works without the optional state API. */ });
  }
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
      const scheduled = Date.parse(video.dataset.scheduledAt || '');
      const pending = video.dataset.publicPlayback === 'pending';
      if (pending && (!Number.isFinite(scheduled) || Date.now() < scheduled)) {
        if (host.firstChild) stop(video);
        return;
      }
      // At the release time the player replaces the schedule in place.
      clearNotice(video);
      if (!visible(video)) { if (host.firstChild) stop(video); return; }
      if (host.firstChild) return;
      const id = video.dataset.youtubeId;
      if (!/^[\w-]{11}$/.test(id)) return;
      const frame = document.createElement('iframe');
      frame.src = `https://www.youtube-nocookie.com/embed/${id}?playsinline=1&rel=0&enablejsapi=1&origin=${encodeURIComponent(location.origin)}`;
      frame.title = video.querySelector('summary').textContent.trim();
      frame.allow = 'accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen';
      frame.allowFullscreen = true;
      frame.referrerPolicy = 'strict-origin-when-cross-origin';
      host.append(frame);
      trackAvailability(video, frame);
    });
  }
  document.addEventListener('toggle', sync, true);
  window.addEventListener('hashchange', sync);
  window.addEventListener('popstate', sync);
  window.addEventListener('focus', sync);
  setInterval(sync, 30000);
  new MutationObserver(sync).observe(document.body, {
    subtree: true, attributes: true, attributeFilter: ['hidden', 'open']
  });
  sync();
})();

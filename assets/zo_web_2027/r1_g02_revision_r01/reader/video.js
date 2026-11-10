/* Optional lesson videos: load only on request; stop when their view closes. */
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
  function stop(video) {
    players.get(video)?.destroy();
    players.delete(video);
    video.querySelector('.zo-video-player').replaceChildren();
  }
  function trackAvailability(video, frame) {
    const status = video.querySelector('.zo-video-status');
    if (!status) return;
    const retry = video.querySelector('.zo-video-retry');
    status.hidden = false;
    status.textContent = status.dataset.initial;
    retry.hidden = false;
    const current = () => frame.isConnected && video.querySelector('iframe') === frame;
    youtubeAPI().then(YT => {
      if (!current()) return;
      const player = new YT.Player(frame, { events: {
        onError: () => {
          if (!current()) return;
          status.hidden = false;
          status.textContent = 'YouTube chưa cho phát video này. Video có thể chưa công khai hoặc tạm thời không xem được. Hãy thử tải lại hoặc mở liên kết YouTube bên dưới.';
          retry.hidden = false;
        },
        onStateChange: event => {
          if (!current() || event.data !== YT.PlayerState.PLAYING) return;
          status.hidden = true;
          retry.hidden = true;
        }
      }});
      players.set(video, player);
    }).catch(() => {
      if (!current()) return;
      status.textContent = 'Chưa kiểm tra được trạng thái từ YouTube. Bạn vẫn có thể thử phát, tải lại khung hoặc mở liên kết YouTube bên dưới.';
    });
  }
  videos.forEach(video => {
    const status = video.querySelector('.zo-video-status');
    if (!status) return;
    status.dataset.initial = status.textContent;
    const retry = document.createElement('button');
    retry.type = 'button';
    retry.className = 'zo-video-retry';
    retry.textContent = 'Thử tải lại video';
    retry.addEventListener('click', () => { stop(video); sync(); });
    status.after(retry);
  });
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
      // Time permits a playback attempt; only YouTube confirms availability.
      const scheduled = Date.parse(video.dataset.scheduledAt || '');
      const pending = video.dataset.publicPlayback === 'pending';
      const status = video.querySelector('.zo-video-status');
      const retry = video.querySelector('.zo-video-retry');
      if (pending && (!Number.isFinite(scheduled) || Date.now() < scheduled)) {
        if (host.firstChild) stop(video);
        if (retry && !retry.hidden) retry.hidden = true;
        return;
      }
      if (pending && status) {
        status.dataset.initial = 'Đã đến lịch công khai dự kiến. Bạn có thể thử phát; khả năng xem phụ thuộc trạng thái hiện tại trên YouTube.';
        if (!host.firstChild) status.textContent = status.dataset.initial;
      }
      if (!visible(video)) { if (host.firstChild) stop(video); return; }
      if (host.firstChild) return;
      const id = video.dataset.youtubeId;
      if (!/^[\w-]{11}$/.test(id)) return;
      const frame = document.createElement('iframe');
      frame.src = `https://www.youtube-nocookie.com/embed/${id}?playsinline=1&rel=0`;
      if (video.querySelector('.zo-video-status')) frame.src += `&enablejsapi=1&origin=${encodeURIComponent(location.origin)}`;
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

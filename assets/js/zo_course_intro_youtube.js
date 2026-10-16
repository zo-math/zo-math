/* Load YouTube only after the viewer asks to play, and after the release time. */
(() => {
  for (const host of document.querySelectorAll('.home-youtube[data-youtube-id]')) {
    const button = host.querySelector('button');
    const notice = host.parentElement.querySelector('.home-youtube-notice');
    const release = Date.parse(host.dataset.publishAt);
    if (!button || !/^[A-Za-z0-9_-]{11}$/.test(host.dataset.youtubeId) || !Number.isFinite(release)) continue;
    const update = () => {
      const remaining = release - Date.now();
      button.disabled = remaining > 0;
      if (notice) notice.hidden = remaining <= 0;
      if (remaining > 0) window.setTimeout(update, Math.min(remaining + 100, 60000));
    };
    update();
    button.addEventListener('click', () => {
      if (Date.now() < release) return;
      const frame = document.createElement('iframe');
      frame.src = `https://www.youtube-nocookie.com/embed/${host.dataset.youtubeId}?autoplay=1&playsinline=1&rel=0`;
      frame.title = 'Giới thiệu khóa Ôn thi Toán THPT 2027 — ZO Math';
      frame.width = '1920';
      frame.height = '1080';
      frame.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      frame.allowFullscreen = true;
      frame.referrerPolicy = 'strict-origin-when-cross-origin';
      host.replaceChildren(frame);
      frame.focus();
    }, { once: true });
  }
})();

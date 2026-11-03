/* Shared course utilities; all dates and bank details come from canonical course sources. */
(() => {
  'use strict';
  const info = JSON.parse(document.querySelector('#page-data').textContent).presence;
  const dock = document.querySelector('#course-presence');
  const dialog = document.querySelector('#presence-dialog');
  const target = Date.parse(info.target);
  const auto = document.querySelector('#exam-auto');
  let returnFocus = null;
  let running = true;
  let frozen = null;
  const appearanceKey = 'zomath:website-2027:appearance';
  const allowedCanvases = ['red-1','red-2','yellow-1','yellow-2','gray-2','gray-3'];
  let appearance = {canvas:'gray-3', grayscale:false};
  try { const stored = JSON.parse(localStorage.getItem(appearanceKey)); if (stored && allowedCanvases.includes(stored.canvas)) appearance = stored; } catch (_) {}
  function applyAppearance() {
    document.documentElement.style.setProperty('--canvas', 'var(--zo-'+appearance.canvas+')');
    document.documentElement.classList.toggle('monochrome', appearance.grayscale === true);
    document.querySelectorAll('input[name="canvas"]').forEach(input => { input.checked = input.value === appearance.canvas; });
    document.querySelector('#grayscale').checked = appearance.grayscale === true;
  }
  applyAppearance();
  document.querySelectorAll('input[name="canvas"],#grayscale').forEach(input => input.addEventListener('change', () => {
    appearance = {canvas:document.querySelector('input[name="canvas"]:checked').value,grayscale:document.querySelector('#grayscale').checked};
    applyAppearance();
    try { localStorage.setItem(appearanceKey,JSON.stringify(appearance)); } catch (_) {}
  }));
  const study = document.querySelector('#mobile-contents');
  const save = document.querySelector('#mobile-save');
  if (study) dock.querySelector('.presence-study-tools').append(study);
  if (save) dock.querySelector('.presence-save').append(save);
  if (study) document.querySelector('.mobile-reader-bar').hidden = true;

  const compactClock = dock.querySelector('.presence-time');
  const largeClock = document.querySelector('.course-home #exam-hero-clock .exam-readout');
  if (largeClock) {
    const header = document.querySelector('.site-header');
    let pendingFrame = false;
    function syncClockVisibility() {
      pendingFrame = false;
      const rect = largeClock.getBoundingClientRect();
      const top = Math.max(0, header.getBoundingClientRect().bottom);
      const bottom = Math.min(innerHeight, dock.getBoundingClientRect().top);
      const visibleHeight = Math.max(0, Math.min(rect.bottom, bottom) - Math.max(rect.top, top));
      const visibleWidth = Math.max(0, Math.min(rect.right, innerWidth) - Math.max(rect.left, 0));
      // Keep the compact clock until its larger counterpart can actually be read.
      const visible = rect.height > 0 && rect.width > 0 &&
        visibleHeight >= rect.height * .9 && visibleWidth >= rect.width * .9 &&
        !compactClock.contains(document.activeElement);
      dock.classList.toggle('home-clock-in-view', visible);
      compactClock.inert = visible;
      if (visible) compactClock.setAttribute('aria-hidden', 'true');
      else compactClock.removeAttribute('aria-hidden');
    }
    function queueClockVisibility() {
      if (!pendingFrame) {
        pendingFrame = true;
        requestAnimationFrame(syncClockVisibility);
      }
    }
    addEventListener('scroll', queueClockVisibility, {passive:true});
    addEventListener('resize', queueClockVisibility);
    addEventListener('pageshow', queueClockVisibility);
    compactClock.addEventListener('focusout', queueClockVisibility);
    if ('ResizeObserver' in window) {
      const observer = new ResizeObserver(queueClockVisibility);
      [largeClock, header, dock].forEach(element => observer.observe(element));
    }
    document.fonts?.ready.then(queueClockVisibility);
    queueClockVisibility();
  }

  function update() {
    const stamp = running ? Date.now() : frozen;
    const seconds = Math.max(0, Math.ceil((target - stamp) / 1000));
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor(seconds % 86400 / 3600);
    const minutes = Math.floor(seconds % 3600 / 60);
    const remainder = seconds % 60;
    for (const [selector,value] of [['days',days],['hours',String(hours).padStart(2,'0')],['minutes',String(minutes).padStart(2,'0')],['seconds',String(remainder).padStart(2,'0')]]) {
      document.querySelectorAll('[data-'+selector+']').forEach(n => { n.textContent = value; });
    }
    document.querySelectorAll('.exam-readout').forEach(n => {
      n.setAttribute('aria-label', `Còn ${days} ngày, ${hours} giờ, ${minutes} phút, ${remainder} giây đến ngày thi tạm tính${running ? '' : '; đã tạm dừng cập nhật'}`);
    });
    compactClock.setAttribute('aria-label', `Còn ${days} ngày, ${hours} giờ, ${minutes} phút, ${remainder} giây đến ngày thi tạm tính${running ? '' : '; đã tạm dừng cập nhật'}. Ngày thi và tùy chọn đồng hồ`);
    document.querySelectorAll('.exam-paused').forEach(n => { n.hidden = running; });
    if (seconds === 0) {
      document.querySelectorAll('.presence-count').forEach(n => { n.textContent = 'Đã đến ngày tạm tính'; });
      document.querySelectorAll('.exam-reference > span').forEach(n => { n.textContent = 'Đã đến ngày tạm tính'; });
    }
  }
  auto.addEventListener('change', () => {
    running = auto.checked;
    frozen = running ? null : Date.now();
    update();
  });
  if (Number.isFinite(target) && info.status === 'reference') {
    update();
    setInterval(() => { if (running && !document.hidden) update(); }, 1000);
    addEventListener('pageshow', update);
    document.addEventListener('visibilitychange', () => { if (!document.hidden) update(); });
  } else {
    dock.querySelector('.presence-count').textContent = 'Chưa có ngày thi';
    auto.disabled = true;
  }

  document.querySelectorAll('[data-open-presence]').forEach(button => button.addEventListener('click', () => {
    returnFocus = button;
    const name = button.dataset.openPresence;
    dialog.querySelectorAll('[data-presence-panel]').forEach(n => { n.hidden = n.dataset.presencePanel !== name; });
    document.querySelector('#presence-dialog-title').textContent = ({support:'Bảo trợ ZO Math',timer:'Ngày thi Toán 2027',appearance:'Tùy chọn giao diện'})[name];
    document.querySelector('.presence-copy-status').textContent = '';
    update();
    dialog.showModal();
  }));
  dialog.querySelector('[data-close-presence]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', e => {
    if (e.target !== dialog) return;
    const r = dialog.getBoundingClientRect();
    if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => returnFocus?.focus({preventScroll:true}));
  document.querySelector('[data-copy-account]').addEventListener('click', async () => {
    const status = document.querySelector('.presence-copy-status');
    try {
      await navigator.clipboard.writeText(info.account);
      status.textContent = 'Đã sao chép số tài khoản ' + info.account + '.';
    } catch (_) {
      status.textContent = 'Chưa sao chép được. Số tài khoản: ' + info.account;
    }
  });
})();

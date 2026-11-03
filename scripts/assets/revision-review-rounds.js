/* Native details remain usable without JS; this adds exclusive deep navigation. */
(() => {
  const panels = [...document.querySelectorAll('#on-lai details.r01-review-round')];
  if (!panels.length) return;
  const select = panel => panels.forEach(other => { other.open = other === panel; });
  const reveal = hash => {
    let id;
    try { id = decodeURIComponent(hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    const panel = target?.closest('details.r01-review-round') ||
      (target?.matches('[data-zo-review-disclosure="closed"]') ? target.querySelector('details.r01-review-round') : null);
    if (panel) select(panel);
  };
  panels.forEach(panel => panel.addEventListener('toggle', () => {
    if (panel.open) panels.forEach(other => { if (other !== panel) other.open = false; });
  }));
  document.addEventListener('click', event => {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const link = event.target.closest('a[href]');
    if (link && link.origin === location.origin && link.pathname === location.pathname) reveal(link.hash);
  }, true);
  addEventListener('hashchange', () => reveal(location.hash));
  addEventListener('popstate', () => reveal(location.hash));
  reveal(location.hash);
})();

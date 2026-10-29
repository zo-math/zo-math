/* R2-G01 reader refinements. The shared controller owns all view transitions. */
(() => {
  const root = document.querySelector('.zo-on-thi-package[data-r1-page-navigation="true"]');
  if (!root) return;
  const panel = document.getElementById('r1-view-panel');
  const support = document.getElementById('ung-ho');
  if (!panel || !support) throw new Error('Reader navigation requires the initialized course shell');
  root.querySelector('.r1-section-toc')?.remove();
  const buttons = [...document.querySelectorAll('.r1-section-nav .r1-tab')];
  const sequence = buttons.filter(button => !button.dataset.parentView && button.id !== 'r1-tab-toan-van');
  const navigation = document.createElement('nav');
  navigation.className = 'zo-page-navigation';
  navigation.setAttribute('aria-label', 'Chuyển phần học liệu');
  support.after(navigation);
  function update() {
    const active = document.getElementById('r1-tab-' + panel.dataset.r1View);
    const owner = active?.dataset.parentView ? document.getElementById('r1-tab-' + active.dataset.parentView) : active;
    const index = sequence.indexOf(owner);
    navigation.replaceChildren();
    navigation.hidden = index < 0;
    if (index < 0) return;
    for (const [offset, direction] of [[-1, 'previous'], [1, 'next']]) {
      const button = sequence[index + offset];
      if (!button) continue;
      const label = button.textContent.trim();
      const url = new URL(location.href);
      url.searchParams.set('r1-view', button.id.slice('r1-tab-'.length));
      url.searchParams.delete('r1-return'); url.searchParams.delete('r1-context'); url.hash = '';
      const link = document.createElement('a');
      link.className = 'zo-page-navigation__' + direction;
      link.href = url.pathname + url.search;
      link.rel = offset < 0 ? 'prev' : 'next';
      link.setAttribute('aria-label', (offset < 0 ? 'Phần trước: ' : 'Phần tiếp theo: ') + label);
      link.title = link.getAttribute('aria-label');
      const icon = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      icon.setAttribute('viewBox', '0 0 24 24');
      icon.setAttribute('aria-hidden', 'true');
      icon.setAttribute('focusable', 'false');
      const arrow = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      arrow.setAttribute('d', offset < 0 ? 'M19 12H5M12 5l-7 7 7 7' : 'M5 12h14M12 5l7 7-7 7');
      icon.append(arrow);
      link.append(icon);
      link.addEventListener('click', event => {
        if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        event.preventDefault(); button.click();
      });
      navigation.append(link);
    }
  }
  new MutationObserver(update).observe(panel, {attributes:true, attributeFilter:['data-r1-view']});
  addEventListener('popstate', update);
  update();
})();

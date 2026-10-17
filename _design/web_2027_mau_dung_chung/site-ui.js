/* Canonical shell behavior shared by course pages. No learner content rewriting. */
(() => {
  if (!document.body.matches('[data-zo-web-shell]')) return;
  document.documentElement.classList.add('prototype-js');
  const root = document.documentElement;
  const settings = document.querySelector('.appearance');
  const inlineControls = settings.classList.contains('appearance--inline');
  const grayscale = settings.querySelector('#grayscale');
  const choices = [...settings.querySelectorAll('[name=background]')];
  const storage = root.dataset.zoPreferences;
  const preferences = {background: 'yellow-1', gray: false};
  try {
    const saved = JSON.parse(localStorage.getItem(storage) || '{}');
    if (typeof saved.background === 'string') preferences.background = saved.background;
    if (typeof saved.gray === 'boolean') preferences.gray = saved.gray;
  } catch {}
  function applyPreferences() {
    let choice = choices.find(input => input.value === preferences.background);
    if (!choice) {
      preferences.background = 'yellow-1';
      choice = choices.find(input => input.value === preferences.background);
    }
    // Color values live in CSS only, not in a second JavaScript palette.
    const color = getComputedStyle(root).getPropertyValue('--theme-' + choice.value).trim();
    root.style.setProperty('--canvas', color);
    if (!inlineControls) {
      settings.querySelector('.current-name').textContent = choice.dataset.label + (preferences.gray ? ' · Sắc xám' : '');
      settings.querySelector('.current-swatch').style.background = color;
    }
    choice.checked = true;
    if (inlineControls) grayscale.setAttribute('aria-pressed', String(preferences.gray));
    else grayscale.checked = preferences.gray;
    root.classList.toggle('grayscale', preferences.gray);
    try { localStorage.setItem(storage, JSON.stringify(preferences)); } catch {}
  }
  applyPreferences();
  choices.forEach(input => input.addEventListener('change', () => {
    preferences.background = input.value; applyPreferences();
  }));
  if (inlineControls) {
    grayscale.addEventListener('click', () => { preferences.gray = !preferences.gray; applyPreferences(); });
  } else {
    grayscale.addEventListener('change', event => { preferences.gray = event.target.checked; applyPreferences(); });
    document.addEventListener('click', event => { if (!settings.contains(event.target)) settings.open = false; });
    settings.addEventListener('keydown', event => {
      if (event.key === 'Escape') { settings.open = false; settings.querySelector('summary').focus(); }
    });
  }

  const rail = document.querySelector('#rail-content');
  const slot = document.querySelector('.r1-nav-slot');
  const mount = document.querySelector('#nav-mount');
  if (slot && mount) mount.append(slot);
  const tablist = document.querySelector('.r1-tablist');
  if (tablist) {
    tablist.setAttribute('aria-orientation', 'vertical');
    tablist.addEventListener('keydown', event => {
      if (!['ArrowUp', 'ArrowDown'].includes(event.key)) return;
      const tabs = [...tablist.querySelectorAll('.r1-tab')];
      const index = tabs.indexOf(document.activeElement);
      if (index < 0) return;
      event.preventDefault(); event.stopImmediatePropagation();
      const next = tabs[(index + (event.key === 'ArrowDown' ? 1 : tabs.length - 1)) % tabs.length];
      next.click(); next.focus();
    }, true);
  }
  const dialog = document.querySelector('#mobile-nav');
  const drawer = document.querySelector('#drawer-mount');
  const trigger = document.querySelector('.mobile-trigger');
  const closeButton = dialog.querySelector('.drawer-close');
  let pendingDestination = null;
  function closeDrawer() { if (dialog.open) dialog.close(); }
  trigger.addEventListener('click', () => {
    drawer.append(...rail.childNodes);
    dialog.showModal(); trigger.setAttribute('aria-expanded', 'true'); closeButton.focus();
  });
  closeButton.addEventListener('click', closeDrawer);
  dialog.addEventListener('close', () => {
    rail.append(...drawer.childNodes); trigger.setAttribute('aria-expanded', 'false');
    trigger.focus({preventScroll: true});
    if (pendingDestination) {
      const target = pendingDestination;
      pendingDestination = null;
      requestAnimationFrame(() => {
        target.scrollIntoView({block: 'start'});
        target.setAttribute('tabindex', '-1'); target.focus({preventScroll: true});
      });
    }
  });
  dialog.addEventListener('click', event => {
    if (event.target === dialog) closeDrawer();
    const anchor = event.target.closest('.home-nav a');
    if (anchor) {
      pendingDestination = document.getElementById(decodeURIComponent(anchor.hash.slice(1)));
      closeDrawer();
    } else if (event.target.closest('.r1-tab')) closeDrawer();
  });
  matchMedia('(min-width: 1000px)').addEventListener('change', event => {
    if (event.matches) closeDrawer();
  });
  function selectedView() {
    // Icon-only shell component keeps its accessible name across view changes.
    if (trigger.classList.contains("mobile-trigger--icon")) return;
    const current = document.querySelector('.r1-tab[aria-selected=true]');
    trigger.querySelector('.mobile-view').textContent = current ? current.textContent + ' · Mục lục' : 'Mục lục khóa học';
  }
  if (tablist) new MutationObserver(selectedView).observe(tablist, {subtree: true, attributes: true, attributeFilter: ['aria-selected']});
  selectedView();

  const homeLinks = [...document.querySelectorAll('.home-nav a')];
  if (homeLinks.length) {
    const targets = homeLinks.map(link => ({link, target: document.getElementById(decodeURIComponent(link.hash.slice(1)))})).filter(item => item.target);
    let scheduled = false;
    function markSection() {
      scheduled = false;
      let active = targets[0];
      // The reading beat starts at its paper, before the source heading/label.
      // Looking only at a nested section can leave the prior item selected.
      for (const item of targets) if ((item.target.closest('.reading-region') || item.target).getBoundingClientRect().top <= 120) active = item;
      for (const item of targets) {
        if (item === active) item.link.setAttribute('aria-current', 'location');
        else item.link.removeAttribute('aria-current');
      }
    }
    addEventListener('scroll', () => {
      if (!scheduled) { scheduled = true; requestAnimationFrame(markSection); }
    }, {passive: true});
    addEventListener('hashchange', markSection);
    addEventListener('resize', markSection);
    markSection();
  }
})();

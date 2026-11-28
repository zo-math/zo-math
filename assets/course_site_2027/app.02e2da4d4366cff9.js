/* Browser-local study state. No analytics or account tracking. */
(() => {
  'use strict';
  const data = JSON.parse(document.querySelector('#page-data').textContent);
  const catalog = data.catalog || [];
  if (document.body.dataset.page === 'home' && (new URLSearchParams(location.search).has('intent') || ['#chuyen-de','#hoc-lieu-hien-co'].includes(location.hash))) {
    location.replace('chuyen-de.html' + location.search + '#chuyen-de'); return;
  }
  const storageKey = 'zomath:course-2027:study-v1';
  const $ = (s, root = document) => root.querySelector(s);
  const $$ = (s, root = document) => [...root.querySelectorAll(s)];
  const clean = (s) => s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd').replace(/Đ/g, 'D').toLowerCase();
  const escape = (s) => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function readingUrl(course, record, resume = false) {
    const query = new URLSearchParams();
    if (resume) query.set('resume', '1');
    if (record.view === 'toan-van') query.set('view', 'toan-van');
    return course.url + (query.size ? '?' + query : '') + (record.target ? '#' + encodeURIComponent(record.target) : '');
  }
  let state = {bookmarks: [], recent: null};
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey));
    if (saved && Array.isArray(saved.bookmarks)) state = saved;
  } catch (_) { /* The page remains usable with in-memory state. */ }
  let toastTimer;
  function toast(message) {
    const node = $('.toast');
    node.textContent = message; node.hidden = false;
    clearTimeout(toastTimer); toastTimer = setTimeout(() => node.hidden = true, 3500);
  }
  function persist(notify = false) {
    try { localStorage.setItem(storageKey, JSON.stringify(state)); return true; }
    catch (_) { if (notify) toast('Trình duyệt chưa cho phép lưu trên máy. Dấu lưu chỉ giữ trong lần mở này.'); return false; }
  }
  function updateBadges() {
    $$('.saved-count').forEach(n => {n.textContent = state.bookmarks.length; n.hidden = !state.bookmarks.length;});
    $$('[data-save]').forEach(button => {
      const saved = state.bookmarks.some(b => b.id === button.dataset.save && b.kind === 'course');
      const p = catalog.find(p => p.id === button.dataset.save);
      button.setAttribute('aria-pressed', String(saved));
      button.setAttribute('aria-label', (saved ? 'Bỏ lưu chuyên đề ' : 'Lưu chuyên đề ') + (p?.title || ''));
    });
  }
  $$('[data-save]').forEach(button => button.addEventListener('click', () => {
    const p = catalog.find(p => p.id === button.dataset.save);
    const index = state.bookmarks.findIndex(b => b.id === p.id && b.kind === 'course');
    if (index >= 0) state.bookmarks.splice(index, 1);
    else state.bookmarks.unshift({id:p.id, kind:'course', title:p.title, code:p.code, url:p.url, label:'Chuyên đề'});
    if (persist(true)) toast(index >= 0 ? 'Đã bỏ lưu chuyên đề.' : 'Đã lưu chuyên đề. Mở “Đã lưu” để tìm lại.');
    updateBadges();
  }));
  updateBadges();

  if (document.body.dataset.page === 'topics') {
    let filter = 'all';
    const cards = $$('.course-card');
    function filterCards() {
      const query = clean($('#course-search').value.trim());
      let count = 0;
      cards.forEach(card => {
        const p = catalog.find(p => p.id === card.dataset.course);
        const visible = (filter === 'all' || p.group === filter) && clean(`${p.title} ${p.summary} ${p.code}`).includes(query);
        card.hidden = !visible; if (visible) count++;
      });
      $$('.topic-strand').forEach(group => { group.hidden = !Array.from(group.querySelectorAll('.course-card')).some(card => !card.hidden); });
      $('#filter-status').textContent = count + ' chuyên đề';
      $('#filter-status').classList.toggle('visually-hidden', !query && filter === 'all');
      $('#no-courses').hidden = count !== 0;
      $$('[data-filter]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.filter === filter)));
    }
    $('#course-search').addEventListener('input', filterCards);
    $$('[data-filter]').forEach(b => b.addEventListener('click', () => {filter = b.dataset.filter; filterCards();}));
    $('#clear-search').addEventListener('click', () => {filter = 'all'; $('#course-search').value = ''; filterCards(); $('#course-search').focus();});
    filterCards();
  }
  if ($('#recent-reading') && state.recent && catalog.some(p => p.id === state.recent.id)) {
      const r = state.recent, p = catalog.find(p => p.id === r.id);
      const target = r.target || 'tong-quan';
      const recent = $('#recent-reading');
      recent.innerHTML = `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg><div><small>VỊ TRÍ ĐỌC GẦN NHẤT</small><strong>${escape(p.title)} · ${escape(r.label)}</strong></div><a href="${escape(readingUrl(p,{...r,target},true))}">Tiếp tục đọc <span aria-hidden="true">→</span></a>`;
      recent.hidden = false;
      const dismiss = document.createElement('button'); dismiss.className='icon-button'; dismiss.textContent='×';
      dismiss.setAttribute('aria-label','Bỏ vị trí đọc gần nhất');
      dismiss.addEventListener('click', () => {state.recent=null;persist(true);recent.hidden=true;});
      recent.append(dismiss);
    }

  if (document.body.dataset.page === 'saved') {
    function renderSaved() {
      const list = $('#saved-list'); list.replaceChildren();
      state.bookmarks.filter(b => catalog.some(p => p.id === b.id)).forEach(b => {
        const p = catalog.find(p => p.id === b.id);
        const item = document.createElement('article'); item.className = 'saved-item';
        const a = document.createElement('a'); a.className = 'saved-item-link';
        a.href = readingUrl(p,b);
        a.innerHTML = `<small>${b.kind === 'course' ? 'CHUYÊN ĐỀ' : 'VỊ TRÍ ĐỌC'}</small><h2>${escape(p.title)}</h2><p>${escape(b.label)}</p>`;
        const remove = document.createElement('button'); remove.textContent = 'Bỏ lưu';
        remove.setAttribute('aria-label', `Bỏ lưu ${p.title} · ${b.label}`);
        remove.addEventListener('click', () => {
          state.bookmarks = state.bookmarks.filter(x => x !== b); persist(true); renderSaved(); updateBadges(); toast('Đã bỏ dấu lưu.');
        });
        item.append(a, remove); list.append(item);
      });
      $('#saved-empty').hidden = list.children.length > 0;
    }
    renderSaved();
  }

  if (document.body.dataset.page !== 'reader') return;
  const p = data.course;
  const root = $('.reader-content');
  if (p.id === 'r1_g01' || p.id === 'r1_g02') {
    for (const summary of $$('.zo-learning-video > summary', root)) {
      const title = summary.textContent.trim().replace(/^Video:\s*/iu, '');
      const icon = document.createElement('span');
      icon.className = 'zo-video-play-icon';
      icon.setAttribute('aria-hidden', 'true');
      summary.classList.add('zo-video-card-title');
      summary.replaceChildren(icon, title);
    }
  }
  const overview = $('#tong-quan');
  const overviewHome = overview.nextElementSibling;
  const fullTextOverview = overview.querySelector('#overview-introduction[data-reading-scale]')
    ? $('#bat-dau > .reading-region', root) : null;
  const topicOverview = p.id !== 'd0';
  const overviewLayout = 'orientation-12';
  const overviewAliases = data.overviewAliases || {};
  const sections = [...root.children].filter(n => n.id);
  const labels = {'tong-quan':'Tổng quan','bat-dau':'Bắt đầu','bai-hoc':'Bài học','phieu-luyen':'Luyện tập','tu-kiem-tra':'Kiểm tra','on-lai':'Ôn lại','on-nen':'Ôn nền','sua-loi':'Sửa lỗi','nhat-ky':'Nhật kí','loi-giai':'Lời giải','nguon':'Tài liệu','tai-tai-lieu':'Tải PDF','toan-van':'Toàn văn','khai-bao-pham-vi':'Chọn phạm vi','khao-sat':'Khảo sát','doc-ket-qua':'Đọc kết quả','chon-mach':'Chọn mạch học'};
  const supportViews = new Set(['on-lai','on-nen','sua-loi','nhat-ky','loi-giai','doc-ket-qua']);
  const contextReturn = $('#context-return');
  const returnButton = $('#return-to-task');
  returnButton.classList.add('icon-button');
  const legacyBackIcon = $(':scope > .icon', contextReturn);
  returnButton.replaceChildren(legacyBackIcon || $('.icon', returnButton));
  contextReturn.replaceChildren(returnButton);
  const saveButton = $('#save-position');
  if (contextReturn.nextElementSibling !== saveButton) saveButton.before(contextReturn);
  const viewLabel = $('#current-view-label');
  const supportGate = $('#support-gate');
  const finishTestButton = $('button[value="end"]', supportGate);
  const finishTestLabel = finishTestButton.firstChild;
  if (finishTestLabel?.nodeType === Node.TEXT_NODE) finishTestLabel.nodeValue = 'Đã kết thúc ';
  let view = '', origin = null, pendingSupport = null, testEnded = false;
  const testReview = $('#tu-kiem-tra .zo-post-test-review', root)
    ? '#tu-kiem-tra .zo-post-test-review, #loi-giai-kiem-tra' : null;
  const testReviewPanels = testReview
    ? $$(testReview, root).flatMap(region => $$('details', region)) : [];
  const isTestReview = node => testReview && node?.closest(testReview);
  function requestTestEnd(pending) {
    pendingSupport = pending;
    supportGate.returnValue = '';
    supportGate.showModal();
  }
  testReviewPanels.forEach(panel => {
    panel.addEventListener('toggle', () => {
      if (!testEnded) panel.open = false;
    });
    $(':scope > summary', panel)?.addEventListener('click', event => {
      if (testEnded || panel.open) return;
      event.preventDefault();
      requestTestEnd({panel});
    });
  });
  let crossPageOrigin = null;
  let originFocus = null, outlineLinks = [], scrollTimer, suppressSave = true;
  const inlineReturnMarkers = $$('#loi-giai [data-zo-solution-return="inline"]', root);
  const solutionsWithInlineReturn = inlineReturnMarkers
    .find(marker => !marker.closest('details.r1-solution'))?.closest('#loi-giai');
  const warmupGroup = $('#sau-khi-lam-xong a[href="#loi-giai-khoi-dong"]', root)
    && $('#loi-giai-khoi-dong', root);
  const testGroup = $('#cach-thuc-hien-sau-kiem-tra a[href="#loi-giai-kiem-tra"]', root)
    && $('#loi-giai-kiem-tra:is([data-zo-solution-group="true"], :has(h3[data-zo-solution-group="true"]))', root);
  const solutionReturnControls = new Map();
  function bindSolutionReturn(control, target) {
    control.addEventListener('click', event => {
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      const entry = activeSolutionReturn();
      if (entry?.target !== target) return;
      event.preventDefault();
      returnToReadingPosition(entry.position, solutionSourceLink(entry), entry.sourceOffset);
    });
  }
  function styleSolutionReturn(link) {
    link.classList.add('icon-button', 'solution-return');
    link.setAttribute('aria-label', 'Quay lại đề bài');
    const backIcon = $('.icon', returnButton);
    if (backIcon) link.replaceChildren(backIcon.cloneNode(true));
  }
  if (solutionsWithInlineReturn) {
    $$('.answer-link a[href^="#"]', solutionsWithInlineReturn).forEach(link => {
      const block = link.closest('.answer-link');
      const destination = block.closest('details.r1-solution[id], section[id]');
      if (!destination) return;
      styleSolutionReturn(link);
      block.replaceChildren(link);
      const cards = destination.matches('details.r1-solution')
        ? [] : $$('details.r1-solution[id]', destination);
      const controls = cards.length ? cards.map((card, index) => {
        const footer = index === 0 ? block : block.cloneNode(true);
        if (index > 0) footer.removeAttribute('id');
        card.append(footer);
        return $('a', footer);
      }) : [link];
      controls.forEach(control => bindSolutionReturn(control, destination.id));
      solutionReturnControls.set(destination.id, controls);
    });
  }
  for (const group of [warmupGroup, testGroup].filter(Boolean)) {
    if (!solutionReturnControls.has(group.id)) {
      const controls = $$('details.r1-solution .answer-link a[href^="#"]', group);
      controls.forEach(control => {
        styleSolutionReturn(control);
        bindSolutionReturn(control, group.id);
      });
      if (controls.length) solutionReturnControls.set(group.id, controls);
    }
  }
  if (!solutionsWithInlineReturn) {
    inlineReturnMarkers.forEach(marker => {
      const answer = marker.closest('details.r1-solution[id]');
      const control = answer && $('.answer-link a[href^="#"]', answer);
      if (!control || solutionReturnControls.has(answer.id)) return;
      styleSolutionReturn(control);
      bindSolutionReturn(control, answer.id);
      solutionReturnControls.set(answer.id, [control]);
    });
  }
  let renderVersion = 0;
  let bookmarkPosition = null;
  history.scrollRestoration = 'manual';
  const originalRecent = state.recent?.id === p.id ? {...state.recent} : null;
  function nodeText(node, {omitReadingLabel = false} = {}) {
    if (!node) return '';
    const clone = node.cloneNode(true);
    const excluded = omitReadingLabel ? 'annotation,.anchorjs-link,[data-reading-label]' : 'annotation,.anchorjs-link';
    $$(excluded, clone).forEach(n => n.remove());
    return clone.textContent.replace(/\s+/g, ' ').trim();
  }
  function sectionFor(target) {
    if (target === 'tong-quan' || target === 'toan-van') return target;
    let node = document.getElementById(target);
    if (node && overview.contains(node)) return 'tong-quan';
    if (!node || !root.contains(node)) return 'tong-quan';
    while (node.parentElement !== root) node = node.parentElement;
    // Detailed legacy guidance remains available in its original full text.
    if (topicOverview && node.id === 'bat-dau') return 'toan-van';
    return node.id || 'tong-quan';
  }
  function orientationTarget(target, mode) {
    if (mode === 'toan-van' && fullTextOverview && overviewAliases[target] === 'overview-goals') {
      return 'overview-goals';
    }
    return mode === 'toan-van' ? target : overviewAliases[target] || target;
  }
  function hashTarget() {
    let legacyView = new URLSearchParams(location.search).get('r1-view');
    if (legacyView === 'luyen-tap') legacyView = 'phieu-luyen';
    if (legacyView === 'kiem-tra') legacyView = 'tu-kiem-tra';
    if (/^on-lai-\d+$/.test(legacyView || '')) legacyView='on-lai';
    const fallback = legacyView && (legacyView === 'toan-van' || sections.some(n => n.id === legacyView)) ? legacyView : 'tong-quan';
    try { return decodeURIComponent(location.hash.slice(1)) || fallback; }
    catch (_) { return 'tong-quan'; }
  }
  function activeSolutionReturn() {
    return solutionReturnControls.size && (view === 'loi-giai' || view === 'toan-van')
      ? history.state?.zoSolutionReturn : null;
  }
  function solutionSourceLinks(href) {
    return $$('a[href]', root).filter(link => link.getAttribute('href') === href);
  }
  function solutionSourceLink(entry) {
    const links = solutionSourceLinks(entry.sourceHref || '#' + entry.target);
    return entry.sourceIndex === undefined && links.length !== 1 ? null : links[entry.sourceIndex ?? 0];
  }
  function returnContext() {
    return activeSolutionReturn()?.position || (origin && view !== origin.view ? origin : crossPageOrigin);
  }
  function updateReturnContext() {
    const context = returnContext();
    contextReturn.hidden = !context;
    const solutionReturn = activeSolutionReturn();
    function labelSolutionReturn(control, label) {
      control.setAttribute('aria-label', label);
      control.title = label;
    }
    solutionReturnControls.forEach(controls => {
      controls.forEach(control => labelSolutionReturn(control, 'Quay lại đề bài'));
    });
    solutionReturnControls.get(solutionReturn?.target)?.forEach(control =>
      labelSolutionReturn(control, 'Quay lại chỗ vừa đọc'));
    const destination = !context ? '' : context.crossPage
      ? context.courseTitle + ' · ' + context.label
      : context.label === labels[context.view] ? context.label : (labels[context.view] || '') + ' · ' + context.label;
    returnButton.setAttribute('aria-label', destination ? 'Quay lại ' + destination : 'Quay lại');
    returnButton.title = destination;
  }
  async function loadCrossPageOrigin() {
    const query = new URLSearchParams(location.search);
    const sourcePage = query.get('r1-return-page');
    const target = query.get('r1-return');
    // Only known local courses can be destinations; the query never supplies a URL.
    let sourcePath=''; try {sourcePath=sourcePage ? new URL(sourcePage,location.href).pathname : '';} catch (_) {return;}
    const course = catalog.find(c => c.id !== p.id && (sourcePage === c.id || sourcePage === c.url || sourcePath===new URL(c.url,location.href).pathname));
    if (!course || !target || target.length > 256 || /[\s\u0000-\u001f]/u.test(target)) return;
    const sourceUrl = new URL(course.url, location.href);
    if (sourceUrl.origin !== location.origin || sourceUrl.pathname === location.pathname) return;
    try {
      // Validate the actual destination and its reading section, rather than trusting query labels.
      const response = await fetch(sourceUrl, {credentials:'same-origin'});
      if (!response.ok || response.url !== sourceUrl.href) return;
      const sourceDoc = new DOMParser().parseFromString(await response.text(), 'text/html');
      const sourceRoot = sourceDoc.querySelector('.reader-content');
      const node = sourceDoc.getElementById(target);
      if (!sourceRoot || !node || !sourceRoot.contains(node)) return;
      let section = node;
      while (section.parentElement !== sourceRoot) section = section.parentElement;
      if (!section.id || !Object.hasOwn(labels, section.id)) return;
      const returnView = query.get('r1-return-view') === 'toan-van' ? 'toan-van' : section.id;
      const heading = node.matches('details') ? $('summary', node) : $('h2,h3,h4,h5', node);
      crossPageOrigin = {crossPage:true, id:course.id, courseTitle:course.title,
        view:returnView, target, label:nodeText(heading) || labels[section.id],
        url:readingUrl(course, {target,view:returnView})};
      updateReturnContext();
    } catch (_) { /* An unavailable source never produces a speculative return link. */ }
  }
  function position() {
    const current = view === 'tong-quan' ? $('#tong-quan') : view === 'toan-van' ? root : document.getElementById(view);
    let chosen = current;
    if (current) {
      $$('[id]', current).forEach(node => {
        if (node.matches('section,details,.zo-learning-task') && node.getClientRects().length && node.getBoundingClientRect().top <= 185) chosen = node;
      });
    }
    const heading = chosen && (chosen.matches('details') ? $('summary', chosen) : $('h2,h3,h4,h5', chosen));
    return {id:p.id, view, target:chosen?.id || view, label:nodeText(heading) || labels[view] || view,
      scroll:window.scrollY, width:document.documentElement.clientWidth, offset:chosen?.getBoundingClientRect().top || 0,
      ...(topicOverview && view === 'tong-quan' ? {overviewLayout} : {})};
  }
  function saveHistoryPosition() {
    history.replaceState({...history.state,zoPosition:position(),zoView:view,zoOrigin:origin,zoTestEnded:testEnded},'');
  }
  function routeUrl(target, mode) {
    const url = new URL(location.href);
    url.searchParams.delete('resume');
    if (mode === 'toan-van' && target !== 'toan-van') url.searchParams.set('view','toan-van');
    else url.searchParams.delete('view');
    url.hash = encodeURIComponent(target);
    return url;
  }
  function restorePosition(record) {
    const target = document.getElementById(record.target);
    const changedWidth = record.width && record.width !== document.documentElement.clientWidth;
    const top = changedWidth && target ? window.scrollY + target.getBoundingClientRect().top - (record.offset || 0) : record.scroll;
    window.scrollTo({top:Math.max(0,top || 0),behavior:'instant'});
  }
  function remember() {
    if (suppressSave) return;
    state.recent = position(); persist(); saveHistoryPosition();
  }
  function openAncestors(node) {
    for (let ancestor = node; ancestor && ancestor !== root; ancestor = ancestor.parentElement) {
      // A video fragment locates the card; playback is requested from its summary.
      if (ancestor.matches('details:not(.zo-learning-video)')) ancestor.open = true;
    }
    if (node?.matches('[data-zo-review-disclosure="closed"]')) {
      const round = $(':scope > details.r01-review-round', node);
      if (round) round.open = true;
    }
    // A solution anchor may own a section whose disclosure is a child.
    // Open only that unit's solution, never all answers in a group.
    if (node?.matches('[data-zo-type="solution"][data-zo-task]') && node.tagName !== 'DETAILS') {
      const owned = [...node.querySelectorAll('details.r1-solution,details.zo-learning-solution,details.solution')]
        .find(answer => answer.closest('[data-zo-task]') === node);
      if (owned) owned.open = true;
    }
  }
  // Canonical contents take precedence. Other packages retain their complete
  // semantic heading/activity structure, without making activity names headings.
  const authoredContents = JSON.parse(root.dataset.zoContents || '[]');
  const uniformOutline = root.dataset.r1Code === 'R1-G01';
  const g02FullText = root.dataset.r1Code === 'R1-G02';
  const editedLesson = root.dataset.r1Code === 'R1-G02'
    && $('#bai-hoc:has(.zo-lesson-intro [data-lesson-intro-end])', root);
  const editedPractice = root.dataset.r1Code === 'R1-G02'
    && $('#phieu-luyen:has(#dinh-huong-luyen-tap [data-lesson-intro-end])', root);
  const editedTest = root.dataset.r1Code === 'R1-G02'
    && $('#tu-kiem-tra:has(#dinh-huong-kiem-tra)', root);
  const outlineHeading = $('.reading-outline > .nav-label');
  const defaultOutlineHeading = outlineHeading.textContent;
  const mobileOutline = document.createElement('details');
  mobileOutline.className = 'mobile-reading-outline';
  const mobileOutlineTitle = document.createElement('summary'); mobileOutlineTitle.textContent = 'Trong phần này';
  const mobileOutlineLinks = document.createElement('nav'); mobileOutlineLinks.id = 'mobile-page-outline';
  mobileOutlineLinks.setAttribute('aria-label','Mục lục phần đang đọc trên điện thoại');
  mobileOutline.append(mobileOutlineTitle,mobileOutlineLinks); $('.reading-column').prepend(mobileOutline);
  function updateMobileOutline(grouped, nested = false) {
    const links = [...$('#page-outline').children].map(a => a.cloneNode(true));
    mobileOutlineLinks.replaceChildren();
    if (grouped) {
      const depthOf = link => link ? (nested ? Number(link.dataset.depth) : Number(link.dataset.depth !== '0')) : -1;
      const ancestors = [];
      links.forEach((link, index) => {
        const depth = depthOf(link);
        while (ancestors.length && ancestors.at(-1).depth >= depth) ancestors.pop();
        const parent = ancestors.at(-1)?.list || mobileOutlineLinks;
        const hasChildren = depthOf(links[index + 1]) > depth;
        if (parent !== mobileOutlineLinks && !hasChildren) {
          parent.append(link);
          return;
        }
        const group = document.createElement('div');
        group.className = 'mobile-outline-group';
        group.append(link);
        parent.append(group);
        if (hasChildren) {
          const subtopics = document.createElement('details');
          const toggle = document.createElement('summary');
          toggle.setAttribute('aria-label', 'Mục con của ' + link.textContent);
          subtopics.append(toggle);
          group.append(subtopics);
          ancestors.push({depth, list: subtopics});
        }
      });
    } else {
      mobileOutlineLinks.append(...links);
    }
    mobileOutline.hidden = !mobileOutlineLinks.children.length; mobileOutline.open = false;
  }
  const pageNavigation = document.createElement('nav');
  pageNavigation.className = 'zo-page-navigation';
  pageNavigation.setAttribute('aria-label','Chuyển phần học liệu');
  $('.reading-column').append(pageNavigation);
  const pageSequence = $$('.lesson-nav > a[data-view]').filter(a => a.dataset.view !== 'toan-van');
  function updatePageNavigation() {
    pageNavigation.replaceChildren();
    const index = pageSequence.findIndex(a => a.dataset.view === view);
    pageNavigation.hidden = index < 0;
    if (index < 0) return;
    for (const [offset,direction] of [[-1,'previous'],[1,'next']]) {
      const destination = pageSequence[index+offset]; if (!destination) continue;
      const a = document.createElement('a'); a.href = destination.getAttribute('href');
      a.className = 'zo-page-navigation__'+direction; a.rel = offset < 0 ? 'prev' : 'next';
      a.setAttribute('aria-label',(offset < 0 ? 'Phần trước: ' : 'Phần tiếp theo: ')+nodeText(destination));
      a.title = a.getAttribute('aria-label');
      const svg = document.createElementNS('http://www.w3.org/2000/svg','svg');
      svg.setAttribute('viewBox','0 0 24 24'); svg.setAttribute('aria-hidden','true');
      const path = document.createElementNS('http://www.w3.org/2000/svg','path');
      path.setAttribute('d',offset < 0 ? 'M19 12H5M12 5l-7 7 7 7' : 'M5 12h14M12 5l7 7-7 7');
      svg.append(path); a.append(svg); pageNavigation.append(a);
    }
  }
  function rebuildOutline(current, groupPractice, groupReview) {
    const nav = $('#page-outline'); nav.replaceChildren(); outlineLinks = [];
    if (!current) return;
    const seen = new Set();
    function add(node,label,depth=0) {
      if (!node?.id || seen.has(node.id) || !label) return;
      const a = document.createElement('a'); a.href = '#'+encodeURIComponent(node.id);
      a.textContent = label; a.dataset.depth = String(Math.min(depth,3));
      nav.append(a); outlineLinks.push({a,node}); seen.add(node.id);
    }
    if (view === 'tong-quan') {
      if (topicOverview) return;
      $$('.topic-overview-section[id]',current).forEach(n => add(n,nodeText($('h2',n)))); return;
    }
    if (view === 'toan-van') {
      if (!uniformOutline && !g02FullText) {
        $$('h2',current).forEach(h => {
          const section = h.closest('[id]');
          add(section, nodeText(h));
          if (section === editedLesson) {
            collectSectionOutline(section, 'bai-hoc', (node,label,depth=0) => add(node,label,depth+1));
          }
          if (section === editedPractice) {
            collectSectionOutline(section, 'phieu-luyen', (node,label,depth=0) => add(node,label,depth+1), true);
          }
          if (section === editedTest) {
            collectSectionOutline(section, 'tu-kiem-tra', (node,label,depth=0) => add(node,label,depth+1));
          }
          if (section?.id === 'loi-giai' && authoredContents.some(group => group.view === 'loi-giai')) {
            collectSectionOutline(section, 'loi-giai', (node,label,depth=0) => add(node,label,depth+1));
          }
        });
        return;
      }
      sections.forEach(section => {
        const heading = $(':scope > .reading-region > h2', section);
        if (!heading) return;
        add(section, nodeText(heading, {omitReadingLabel:true}));
        if (section.contains(overview)) {
          $$('.topic-overview-section[id]', overview).forEach(n => add(n,nodeText($('h2',n)),1));
        }
        collectSectionOutline(section, section.id, (node,label,depth=0) => add(node,label,depth+1),
          section.id === 'phieu-luyen' && Boolean($('#dinh-huong-luyen-tap [data-lesson-intro-end]', section)),
          section.id === 'on-lai' && Boolean($('#cach-thuc-hien-on-lai [data-lesson-intro-end]', section)));
      });
      return;
    }
    collectSectionOutline(current, view, add, groupPractice, groupReview);
  }
  function collectSectionOutline(current, sectionView, add, groupPractice, groupReview) {
    if (sectionView === 'nhat-ky' && $('#huong-dan-ghi-nhat-ki [data-lesson-intro-end]',current)) return;
    if (sectionView === 'tai-tai-lieu' && $('#huong-dan-tai-pdf [data-lesson-intro-end]',current)) return;
    if (sectionView === 'nguon' && $('#tai-lieu-doi-chieu',current)) return;
    if (sectionView === 'on-nen') {
      const cards = $$('details.r1-foundation-unit[id]', current);
      if (cards.length) {
        cards.forEach(card =>
          add(card, nodeText($(':scope > summary', card), {omitReadingLabel:true})));
        return;
      }
    }
    const bindingView = {'phieu-luyen':'luyen-tap','tu-kiem-tra':'kiem-tra'}[sectionView] || sectionView;
    const declared = authoredContents.find(g => g.view === bindingView);
    if (declared) {
      function visit(items,depth=0) {
        items.forEach(item => {
          const node = document.getElementById(item.target);
          add(node,item.label,depth);
          if (item.children?.length) {
            visit(item.children,depth+1);
          } else if (sectionView === 'loi-giai' && node?.matches('[data-zo-solution-group]')) {
            $$('details.r1-solution[id]',node).forEach(answer => {
              add(answer,nodeText($(':scope > summary',answer), {omitReadingLabel:true}),depth+1);
            });
          }
        });
      }
      visit(declared.items); return;
    }
    if (current === editedTest) {
      for (const group of $$(':scope > section[id]', current)) {
        add(group,nodeText($('h3',group),{omitReadingLabel:true}));
        for (const item of $$('[data-zo-type="task"][id], [data-zo-type="checkpoint"][id]',group)) {
          add(item,nodeText($('h4',item),{omitReadingLabel:true}),1);
        }
      }
      return;
    }
    if (sectionView === 'sua-loi' && $(':scope > section[data-zo-review-disclosure="closed"]', current)) {
      for (const group of $$(':scope > section[id]', current)) {
        add(group,nodeText($('h3',group),{omitReadingLabel:true}));
        for (const task of $$('[data-zo-type="task"][id]',group)) {
          add(task,nodeText($('h4',task),{omitReadingLabel:true}),1);
        }
      }
      return;
    }
    if (groupPractice) {
      if (current === editedPractice) {
        $$('[data-zo-outline-group], [data-zo-type="task"][id], [data-zo-type="checkpoint"][id]', current).forEach(unit => {
          const heading = unit.matches('h3,h4') ? unit : $('h3,h4', unit);
          if (!heading) return;
          const group = unit.hasAttribute('data-zo-outline-group');
          add(unit.id ? unit : unit.closest('section[id]'), nodeText(heading, {omitReadingLabel:true}), group ? 0 : 1);
        });
        return;
      }
      $$(':scope > section[id]', current).forEach(unit => {
        const heading = $('h3', unit);
        if (heading) add(unit, nodeText(heading), unit.hasAttribute('data-zo-outline-group') || heading.hasAttribute('data-zo-outline-group') ? 0 : 1);
      });
      return;
    }
    if (groupReview) {
      $$('details.r01-review-round', current).forEach(round => {
        const task = $('section.zo-learning-task[id]', round);
        const checkpoint = $('section[data-zo-type="checkpoint"][id]', round);
        const section = round.closest('section[data-zo-review-disclosure][id]');
        add(section || task, nodeText($('summary', round)));
        if (section && task) add(task, nodeText($('h3,h4', task)), 1);
        if (checkpoint) add(checkpoint, nodeText($('h3,h4', checkpoint)), 1);
      });
      return;
    }
    const items = $$('h3,h4,h5,.zo-lesson-activity,details[id]',current);
    let hasEntries = false;
    function addEntry(node, label, depth) {
      if (!node?.id || !label) return;
      hasEntries = true;
      add(node, label, depth);
    }
    items.forEach(n => {
      if (n.matches('h3,h4,h5')) {
        if (n.closest('.zo-lesson-activity,details')) return;
        const depth = Number(n.tagName.slice(1))-3;
        addEntry(n.closest('[id]'),nodeText(n),depth);
      } else if (n.matches('.zo-lesson-activity')) {
        if (n.hasAttribute('data-zo-lead')) return;
        const title = $('p > strong,.zo-task-title',n);
        const target = n.id ? n : $('[id]',n);
        addEntry(target,nodeText(title),n.parentElement.closest('.level4,.zo-knowledge-section')?2:1);
      } else if (!n.parentElement.closest('details') && !n.closest('#bai-hoc')) {
        addEntry(n,nodeText($('summary',n)),0);
      }
    });
    if (!hasEntries) add(current,labels[sectionView]||sectionView);
  }
  function renderRoute(target, options = {}) {
    const oldTarget = target;
    const reloadedPanel = options.reload ? document.getElementById(target)?.closest(
      '#on-nen details.r1-foundation-unit[id], :is(#on-lai,#sua-loi) [data-zo-review-disclosure="closed"][id]'
    ) : null;
    if (reloadedPanel) {
      target = reloadedPanel.id;
      options = {...options, position:undefined, scroll:undefined};
    }
    target = orientationTarget(target, options.mode);
    const migrated = oldTarget !== target;
    const staleOverviewPosition = topicOverview && options.position?.view === 'tong-quan'
      && options.position.overviewLayout !== overviewLayout;
    if (migrated || staleOverviewPosition || (topicOverview && options.position?.view === 'bat-dau')) {
      options = {...options, position:undefined, scroll:undefined};
    }
    suppressSave = true;
    $('#save-position').disabled = true; $('#mobile-save').disabled = true;
    const version = ++renderVersion;
    const previousView = view;
    view = options.mode === 'toan-van' ? 'toan-van' : sectionFor(target);
    const legacyGuidance = topicOverview && view === 'toan-van' && options.mode !== 'toan-van' && target !== 'toan-van';
    if (migrated || legacyGuidance) history.replaceState({...history.state,zoView:view}, '', routeUrl(target,view));
    document.body.classList.toggle('overview-open', topicOverview && view === 'tong-quan');
    if (view === 'tu-kiem-tra' && !options.returning && previousView !== view && !origin) testEnded = false;
    if (!testEnded) testReviewPanels.forEach(panel => {panel.open = false;});
    const fullText = view === 'toan-van';
    if (fullText && fullTextOverview) {
      if (fullTextOverview.nextElementSibling !== overview) fullTextOverview.after(overview);
    } else if (overview.nextElementSibling !== overviewHome) {
      overviewHome.before(overview);
    }
    overview.hidden = view !== 'tong-quan' && !(fullText && fullTextOverview);
    root.hidden = view === 'tong-quan';
    root.classList.toggle('reading-full-text', fullText);
    sections.forEach(section => section.hidden = view !== 'toan-van' && section.id !== view);
    $$('[data-view]').forEach(a => {
      if (a.dataset.view === view) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
    });
    viewLabel.textContent = labels[view] || view;
    $('#mobile-view').textContent = labels[view] || view;
    updateReturnContext();
    const current = view === 'tong-quan' ? $('#tong-quan') : view === 'toan-van' ? root : document.getElementById(view);
    const lessonIntro = view === 'bai-hoc' && $('[data-lesson-intro-end]', current)?.parentElement;
    const practiceIntro = view === 'phieu-luyen' && $('#dinh-huong-luyen-tap [data-lesson-intro-end]', current);
    const testIntro = view === 'tu-kiem-tra' && $('#dinh-huong-kiem-tra', current);
    const reviewIntro = view === 'on-lai' && $('#cach-thuc-hien-on-lai [data-lesson-intro-end]', current);
    const foundationIntro = view === 'on-nen' && $('#huong-dan-on-nen', current);
    const remediationIntro = view === 'sua-loi' && $('#cach-thuc-hien-sua-loi [data-lesson-intro-end]', current);
    const solutionIntro = view === 'loi-giai' && $('#cach-thuc-hien-dung-loi-giai [data-lesson-intro-end]', current);
    const g02 = p.id === 'r1_g02';
    const inlineIntro = lessonIntro || practiceIntro?.parentElement || testIntro
      || ((uniformOutline || g02) && reviewIntro?.parentElement) || foundationIntro
      || remediationIntro?.parentElement || solutionIntro?.parentElement
      || (view === 'nhat-ky' && $('#huong-dan-ghi-nhat-ki [data-lesson-intro-end]', current)?.parentElement)
      || (view === 'tai-tai-lieu' && $('#huong-dan-tai-pdf [data-lesson-intro-end]', current)?.parentElement)
      || (view === 'nguon' && $('#tai-lieu-doi-chieu', current));
    const outlineTitle = fullText ? 'Mục lục toàn văn' : lessonIntro ? 'Mục lục bài học' : practiceIntro ? 'Mục lục luyện tập' : testIntro ? 'Mục lục kiểm tra' : reviewIntro ? 'Mục lục ôn lại' : foundationIntro ? 'Mục lục ôn nền' : remediationIntro ? 'Mục lục sửa lỗi' : solutionIntro ? 'Mục lục lời giải' : '';
    outlineHeading.textContent = outlineTitle || defaultOutlineHeading;
    mobileOutlineTitle.textContent = outlineTitle || 'Trong phần này';
    mobileOutlineLinks.setAttribute('aria-label', outlineTitle || 'Mục lục phần đang đọc');
    if (inlineIntro) inlineIntro.after(mobileOutline);
    else $('.reading-column').prepend(mobileOutline);
    rebuildOutline(current, Boolean(practiceIntro), Boolean(reviewIntro));
    $('.reading-outline').hidden = !outlineLinks.length;
    const groupedOutline = (fullText && g02FullText) || lessonIntro || practiceIntro || testIntro || foundationIntro || remediationIntro
      || (g02 && (reviewIntro || solutionIntro)) || (uniformOutline && outlineTitle)
      || (fullText && (editedLesson || editedTest));
    updateMobileOutline(Boolean(groupedOutline), Boolean(g02 && (remediationIntro || fullText)));
    if (reviewIntro && !uniformOutline && !g02) mobileOutline.hidden = true;
    updatePageNavigation();
    const node = document.getElementById(target);
    const reloadedDisclosure = reloadedPanel?.matches('details') ? reloadedPanel
      : reloadedPanel && $(':scope > details.r01-review-round', reloadedPanel);
    const warmupAnswer = uniformOutline && (options.initial || options.returning)
      ? node?.closest('#loi-giai-khoi-dong details.r1-solution') : null;
    if (node && root.contains(node)) {
      if (node === warmupGroup || node.matches('#loi-giai, #loi-giai > section[data-zo-solution-group]')) {
        $$('details.r1-solution[open]', node).forEach(answer => { answer.open = false; });
      }
      if (reloadedPanel) {
        // A fragment inside a closed panel makes the browser reveal it on load.
        // The panel's own anchor keeps its heading reachable without opening it.
        if (reloadedDisclosure) reloadedDisclosure.open = false;
      } else if (warmupAnswer) {
        // A restored fragment inside a closed answer would make the browser reveal it.
        if (node !== warmupAnswer) history.replaceState(history.state, '', routeUrl(warmupAnswer.id, view));
        warmupAnswer.open = false;
      } else if (testEnded || !isTestReview(node)) {
        openAncestors(node);
      }
    }
    requestAnimationFrame(() => {
      if (version !== renderVersion) return;
      if (reloadedDisclosure) {
        reloadedDisclosure.open = false;
        reloadedPanel.scrollIntoView({block:'start',behavior:'instant'});
      } else if (warmupAnswer) {
        warmupAnswer.open = false;
        warmupAnswer.scrollIntoView({block:'start', behavior:'instant'});
      }
      else if (options.returnLink?.getClientRects().length && Number.isFinite(options.returnOffset)) {
        window.scrollTo({
          top: window.scrollY + options.returnLink.getBoundingClientRect().top - options.returnOffset,
          behavior: 'instant'
        });
      }
      else if (options.position) restorePosition(options.position);
      else if (options.scroll !== undefined) window.scrollTo({top:options.scroll, behavior:'instant'});
      else if ((inlineIntro || fullText) && target === view) window.scrollTo({top:0, behavior:'instant'});
      else if (target === view && mobileOutline.getClientRects().length) mobileOutline.scrollIntoView({block:'start',behavior:'instant'});
      else if (!options.initial && node && target !== 'tong-quan' && target !== 'toan-van') node.scrollIntoView({block:'start', behavior:'instant'});
      else if (!options.initial || topicOverview && target === 'tong-quan') window.scrollTo({top:0, behavior:'instant'});
      else if (node && target !== view) node.scrollIntoView({block:'start', behavior:'instant'});
      suppressSave = false;
      $('#save-position').disabled = false; $('#mobile-save').disabled = false;
      remember(); updatePositionButton();
    });
  }
  function navigate(target, options = {}) {
    const withinFullText = view === 'toan-van' && options.source && (root.contains(options.source) || options.source.closest('#page-outline,#mobile-page-outline'));
    target = orientationTarget(target, withinFullText ? 'toan-van' : undefined);
    const targetSection = sectionFor(target);
    const nextView = withinFullText ? 'toan-van' : targetSection;
    const revealsSupport = supportViews.has(targetSection) || ['tong-quan','bai-hoc','tai-tai-lieu','toan-van'].includes(targetSection);
    const fromTest = view === 'tu-kiem-tra' || (withinFullText && options.source.closest('#tu-kiem-tra'));
    if (!options.approved && !testEnded &&
        ((fromTest && revealsSupport) || isTestReview(document.getElementById(target)))) {
      requestTestEnd({target, options});
      return;
    }
    saveHistoryPosition();
    const contextualLink = (options.source && root.contains(options.source) && nextView !== view && target !== nextView)
      || (view === 'tu-kiem-tra' && nextView !== view && revealsSupport);
    if (nextView !== view && (supportViews.has(nextView) || contextualLink) && !origin) {
      origin = position(); originFocus = document.activeElement;
      const caller = options.source?.closest('.zo-learning-task[id], [data-zo-type="checkpoint"][id]');
      if (caller) {
        origin.target = caller.id;
        origin.label = nodeText($('h3,h4,h5', caller)) || origin.label;
        origin.offset = caller.getBoundingClientRect().top;
      }
    } else if (!supportViews.has(nextView) && !contextualLink) origin = null;
    let solutionReturn = null;
    if ((nextView === 'loi-giai' || withinFullText) && solutionReturnControls.has(target)
        && options.source && root.contains(options.source) && !options.source.closest('#loi-giai')
        && ['Xem lời giải', 'Xem công thức để kiểm tra'].includes(nodeText(options.source))) {
      const sourceHref = options.source.getAttribute('href');
      const sourceIndex = solutionSourceLinks(sourceHref).indexOf(options.source);
      const sourceOffset = options.source.getBoundingClientRect().top;
      solutionReturn = {target, position:position(), sourceHref, sourceIndex, sourceOffset};
    }
    history.pushState({zoOrigin:origin,zoView:nextView,zoTestEnded:testEnded,zoSolutionReturn:solutionReturn}, '', routeUrl(target,nextView));
    const mobileWasOpen = document.body.classList.contains('nav-open');
    closeNav(false);
    renderRoute(target, {...options,mode:nextView});
    if (mobileWasOpen) {const main = $('#main-content'); main.tabIndex = -1; main.focus({preventScroll:true});}
  }
  document.addEventListener('click', event => {
    const a = event.target.closest('a[href]');
    if (!a || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const u = new URL(a.href, location.href);
    if (u.origin === location.origin && u.pathname !== location.pathname) {
      const destination=catalog.find(c=>new URL(c.url,location.href).pathname===u.pathname);
      const foundation=u.pathname.endsWith('/_dung_chung/nen/so_gan_dung_sai_so.html');
      const pdf=u.pathname.endsWith('.pdf');
      if(view==='tu-kiem-tra' && !testEnded && (destination||foundation||pdf)) {
        event.preventDefault();requestTestEnd({href:u.href});return;
      }
      if((destination||foundation)&&root.contains(a)) {
        const current=position();
        const caller=a.closest('.zo-learning-task[id],details[id],section[id],.reading-region[id]');
        const declared=u.searchParams.get('r1-return-page')===p.id ? document.getElementById(u.searchParams.get('r1-return')) : null;
        if(declared&&root.contains(declared))current.target=declared.id;
        else if(caller&&root.contains(caller))current.target=caller.id;
        u.searchParams.set('r1-return-page',p.id);
        u.searchParams.set('r1-return',current.target);u.searchParams.set('r1-return-view',current.view);
        a.href=u.href; // Preserve native link navigation, including browser tooling.
      }
      return;
    }
    if (u.origin !== location.origin || u.pathname !== location.pathname || !u.hash) return;
    let target; try {target = decodeURIComponent(u.hash.slice(1));} catch (_) {return;}
    const targetNode = document.getElementById(target);
    if (target !== 'tong-quan' && target !== 'toan-van' && !overviewAliases[target] && (!targetNode || !root.contains(targetNode) && !overview.contains(targetNode))) return;
    event.preventDefault(); navigate(target, {source:a});
  });
  window.addEventListener('popstate', () => {
    origin = history.state?.zoOrigin || null;
    testEnded = !!history.state?.zoTestEnded;
    closeNav(false); renderRoute(hashTarget(), {returning:true,mode:history.state?.zoView || new URLSearchParams(location.search).get('view'),position:history.state?.zoPosition});
  });
  supportGate.addEventListener('close', () => {
    const pending = pendingSupport; pendingSupport = null;
    if (supportGate.returnValue === 'end' && pending) {
      testEnded = true;
      if (pending.panel) {
        history.replaceState({...history.state, zoTestEnded:true}, '');
        pending.panel.open = true;
      } else if (pending.href) {
        location.assign(pending.href);
      } else {
        navigate(pending.target, {...pending.options, approved:true});
      }
    }
  });
  function returnToReadingPosition(context, focus, sourceOffset) {
    if (!context) return;
    saveHistoryPosition();
    if (context.crossPage) {location.assign(context.url); return;}
    origin = null;
    history.pushState({zoOrigin:null,zoView:context.view,zoPosition:context,zoTestEnded:testEnded}, '', routeUrl(context.target,context.view));
    renderRoute(context.target, {returning:true, mode:context.view, position:context,
      returnLink:focus, returnOffset:sourceOffset});
    if (focus?.isConnected && focus.getClientRects().length) focus.focus({preventScroll:true});
  }
  returnButton.addEventListener('click', () => {
    const entry = activeSolutionReturn();
    returnToReadingPosition(returnContext(), entry ? solutionSourceLink(entry) : originFocus, entry?.sourceOffset);
  });
  function updatePositionButton() {
    const pos = position();
    bookmarkPosition = pos;
    const saved = state.bookmarks.some(b => b.id === p.id && b.kind === 'position' && b.target === pos.target);
    $('#save-position').setAttribute('aria-pressed', String(saved));
    $('#save-position').setAttribute('aria-label', (saved ? 'Bỏ lưu vị trí: ' : 'Lưu chỗ đang đọc: ') + pos.label);
    $('#mobile-save').setAttribute('aria-pressed', String(saved));
  }
  function savePosition() {
    // Save the same reading location named by the visible control, even if
    // focusing the sticky toolbar changes the viewport during activation.
    const pos = bookmarkPosition || position();
    const index = state.bookmarks.findIndex(b => b.id === p.id && b.kind === 'position' && b.target === pos.target);
    if (index >= 0) state.bookmarks.splice(index, 1);
    else state.bookmarks.unshift({...pos, kind:'position', title:p.title, code:p.code});
    if (persist(true)) toast(index >= 0 ? 'Đã bỏ dấu lưu tại vị trí này.' : 'Đã lưu “' + pos.label + '”.');
    updatePositionButton(); updateBadges();
  }
  $('#save-position').addEventListener('click', savePosition);
  $('#mobile-save').addEventListener('click', savePosition);
  $('#text-size').addEventListener('click', () => {
    const large = document.body.classList.toggle('large-type');
    $('#text-size').setAttribute('aria-label', large ? 'Dùng cỡ chữ thường' : 'Tăng cỡ chữ');
    $('#text-size').setAttribute('aria-pressed', String(large));
  });
  function setFocus(on) {
    document.body.classList.toggle('focus-on', on); $('.exit-focus').hidden = !on;
    $('#focus-mode').setAttribute('aria-pressed', String(on));
    $('#focus-mode').setAttribute('aria-label', on ? 'Tắt chế độ tập trung' : 'Bật chế độ tập trung');
    if (on) $('.exit-focus').focus({preventScroll:true}); else $('#focus-mode').focus({preventScroll:true});
  }
  $('#focus-mode').addEventListener('click', () => setFocus(!document.body.classList.contains('focus-on')));
  $('.exit-focus').addEventListener('click', () => setFocus(false));
  const sidebar = $('#reader-sidebar'), media = matchMedia('(max-width:760px)');
  function closeNav(focus = true) {
    const wasOpen = document.body.classList.contains('nav-open');
    document.body.classList.remove('nav-open'); $('.nav-scrim').hidden = true;
    $('#mobile-contents').setAttribute('aria-expanded','false');
    sidebar.inert = media.matches;
    if (focus && wasOpen) $('#mobile-contents').focus({preventScroll:true});
  }
  $('#mobile-contents').setAttribute('aria-expanded','false');
  $('#mobile-contents').setAttribute('aria-controls','reader-sidebar');
  $('#mobile-contents').addEventListener('click', () => {
    sidebar.inert = false; document.body.classList.add('nav-open'); $('.nav-scrim').hidden = false;
    $('#mobile-contents').setAttribute('aria-expanded','true'); $('.mobile-nav-close').focus();
  });
  $('.mobile-nav-close').addEventListener('click', () => closeNav());
  $('.nav-scrim').addEventListener('click', () => closeNav());
  document.addEventListener('keydown', event => {
    if (!document.body.classList.contains('nav-open')) return;
    if (event.key === 'Escape') {event.preventDefault(); closeNav();}
    if (event.key === 'Tab') {
      const focusable = $$('a[href],button,summary', sidebar).filter(n => n.getClientRects().length);
      const first = focusable[0], last = focusable.at(-1);
      if (event.shiftKey && document.activeElement === first) {event.preventDefault();last.focus();}
      else if (!event.shiftKey && document.activeElement === last) {event.preventDefault();first.focus();}
    }
  });
  media.addEventListener('change', () => {closeNav(false);sidebar.inert=media.matches;});
  sidebar.inert = media.matches;
  // Local scrolling preserves the intended scale of mathematical figures/tables.
  $$('table', root).forEach(table => {
    if (table.closest('.table-scroll,.figure-viewport,.safe-table-scroll,.zo-course-table-frame')) return;
    const wrapper = document.createElement('div'); wrapper.className = 'safe-table-scroll'; wrapper.tabIndex = 0;
    wrapper.setAttribute('role','region'); wrapper.setAttribute('aria-label','Bảng nội dung; cuộn ngang khi cần');
    table.before(wrapper); wrapper.append(table);
  });
  window.addEventListener('scroll', () => {
    clearTimeout(scrollTimer); scrollTimer = setTimeout(() => {remember();updatePositionButton();}, 220);
    let active = null;
    outlineLinks.forEach(pair => {if (pair.node.getBoundingClientRect().top <= 190) active = pair; pair.a.removeAttribute('aria-current');});
    active?.a.setAttribute('aria-current','location');
  }, {passive:true});
  window.addEventListener('pagehide', remember);
  origin = history.state?.zoOrigin || null;
  const initialHistory = history.state?.zoPosition;
  testEnded = !!history.state?.zoTestEnded;
  const reload = performance.getEntriesByType('navigation')[0]?.type === 'reload';
  renderRoute(hashTarget(), {initial:true,reload,mode:new URLSearchParams(location.search).get('view') || history.state?.zoView,position:initialHistory});
  loadCrossPageOrigin();
  if (new URLSearchParams(location.search).has('resume') && originalRecent) {
    document.fonts.ready.then(() => {
      renderRoute(originalRecent.target || 'tong-quan', {returning:true,mode:originalRecent.view,position:originalRecent});
    });
  }
})();

// Public aggregate only: no API credential or visitor details reach this page.
(() => {
  const footer = document.querySelector('.site-footer .footer-inner');
  if (!footer) return;
  const row = document.createElement('p');
  row.className = 'site-views';
  row.setAttribute('aria-live', 'polite');
  function lines(today, total) {
    const first = document.createElement('span'), second = document.createElement('span');
    first.textContent = 'Lượt xem trong ngày: ' + today;
    second.textContent = total;
    first.style.display = second.style.display = 'block';
    row.replaceChildren(first, second);
  }
  lines('đang tải…', 'Tổng lượt xem: đang tải…');
  footer.append(row);
  const local = ['127.0.0.1', 'localhost'].includes(location.hostname);
  const endpoint = local ? 'http://127.0.0.1:8878/api/site-views' : 'https://zo-math-site-views.khongvamot2024.workers.dev/api/site-views';
  let busy = false, last = null;
  const format = new Intl.NumberFormat('vi-VN');
  const date = value => new Date(value).toLocaleDateString('vi-VN', {timeZone:'Asia/Ho_Chi_Minh'});
  const vietnamDay = value => new Intl.DateTimeFormat('en-CA', {timeZone:'Asia/Ho_Chi_Minh',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date(value));
  function show(value, stale) {
    const currentDay = value.day === vietnamDay(Date.now());
    lines(currentDay ? format.format(value.today) : 'chưa cập nhật', 'Tổng lượt xem tính từ ' + date(value.since) + ': ' + format.format(value.total));
    row.title = (stale || !currentDay ? 'Chưa cập nhật được số mới. ' : '') + 'Nguồn: Cloudflare. Cập nhật: ' + new Date(value.updated_at).toLocaleString('vi-VN') + '. Đã loại bot.';
  }
  async function refresh() {
    if (busy || document.hidden) return;
    busy = true;
    try {
      const response = await fetch(endpoint, {cache:'no-store',credentials:'omit',signal:AbortSignal.timeout(10000)});
      if (!response.ok) throw Error('Unavailable');
      const value = await response.json();
      if (value.source !== 'Cloudflare Web Analytics' || value.metric !== 'page_views' || value.scope !== 'website'
          || !Number.isSafeInteger(value.total) || value.total < 0 || value.exclude_bots !== true
          || !Number.isSafeInteger(value.today) || value.today < 0 || value.day_timezone !== 'Asia/Ho_Chi_Minh'
          || value.day !== vietnamDay(value.updated_at)
          || !Number.isFinite(Date.parse(value.since)) || !Number.isFinite(Date.parse(value.updated_at))
          || Date.parse(value.updated_at) > Date.now()+60000 || Date.parse(value.since) > Date.parse(value.updated_at)) throw Error('Invalid aggregate');
      last = value;
      show(value, value.stale === true || Date.now()-Date.parse(value.updated_at)>20*60000);
    } catch {
      if (last) show(last, true);
      else lines('chưa lấy được số liệu', 'Tổng lượt xem: chưa lấy được số liệu');
    } finally { busy = false; }
  }
  refresh();
  setInterval(refresh, 60000);
  document.addEventListener('visibilitychange', () => { if (!document.hidden) refresh(); });
})();


(() => {
  const root = document.querySelector('.zo-on-thi-package');
  if (!root) return;

  const TITLE = root.dataset.r1Title || 'Gói học liệu';
  const VIEW_PARAM = 'r1-view';
  const RETURN_PARAM = 'r1-return';
  const CONTEXT_PARAM = 'r1-context';
  const hasStartSection = Boolean(root.querySelector(':scope > section#bat-dau'));
  const baseGroups = [
    {
      id: 'main',
      label: 'Mạch học chính',
      definitions: [
        hasStartSection
          ? {view: 'bat-dau', label: 'Bắt đầu', ids: ['bat-dau']}
          : {view: 'cach-hoc', label: 'Cách học', ids: ['cách-học-với-tài-liệu-này']},
        {view: 'bai-hoc', label: 'Bài học', ids: ['bai-hoc']},
        {view: 'luyen-tap', label: 'Luyện tập', ids: ['phieu-luyen']},
        {view: 'kiem-tra', label: 'Kiểm tra', ids: ['tu-kiem-tra']},
        {view: 'on-lai', label: 'Ôn lại', ids: ['on-lai']}
      ]
    },
    {
      id: 'support',
      label: 'Hỗ trợ khi cần',
      definitions: [
        {view: 'on-nen', label: 'Ôn nền', ids: document.getElementById('on-nen')?.classList.contains('level2') ? ['on-nen'] : ['bai-hoc'], target: 'on-nen'},
        {view: 'sua-loi', label: 'Sửa lỗi', ids: ['sua-loi']},
        {view: 'nhat-ky', label: 'Nhật kí', ids: document.getElementById('nhat-ky')?.classList.contains('level2') ? ['nhat-ky'] : ['on-lai'], target: 'nhat-ky'},
        {view: 'loi-giai', label: 'Lời giải', ids: ['loi-giai', 'đọc-kết-quả-tự-kiểm-tra']}
      ]
    },
    {
      id: 'utility',
      label: 'Tiện ích',
      definitions: [
        {view: 'tai-pdf', label: 'Tải PDF', ids: ['tai-tai-lieu']},
        {view: 'nguon', label: 'Nguồn', ids: ['nguon']},
        {view: 'toan-van', label: 'Toàn văn', ids: []}
      ]
    }
  ];
  const baseContentOrder = [
    hasStartSection ? 'bat-dau' : 'cách-học-với-tài-liệu-này',
    'bai-hoc', 'phieu-luyen', 'tu-kiem-tra',
    'on-lai', 'on-nen', 'sua-loi', 'nhat-ky', 'loi-giai', 'đọc-kết-quả-tự-kiểm-tra', 'nguon',
    'tai-tai-lieu'
  ];
  const contentOrder = baseContentOrder.filter(id =>
    root.querySelector(`:scope > section#${CSS.escape(id)}`)
  );
  const contentIds = new Set(contentOrder);
  const definitions = baseGroups.flatMap(group => group.definitions
    .map(item => ({
      ...item,
      group: group.id,
      groupLabel: group.label,
      ids: item.ids.filter(id => contentIds.has(id))
    }))
    .filter(item => (
      item.view === 'toan-van' ||
      (item.ids.length > 0 && (!item.target || root.querySelector(`#${CSS.escape(item.target)}`)))
    )));
  const byView = new Map(definitions.map(item => [item.view, item]));

  const draft = document.getElementById('quarto-draft-alert');
  const status = root.querySelector('.r1-status');
  if (draft && status) {
    draft.textContent = status.textContent.trim();
    draft.className = '';
    status.replaceChildren(draft);
  }

  // Closed on a fresh visit; explicit deep links may open only their ancestors.
  root.querySelectorAll('details').forEach(details => {
    details.open = false;
  });

  function normalizeConfiguredTable(wrapper) {
    const table = wrapper.querySelector(':scope > table');
    if (!table) return;
    table.classList.add('r1-data-table');
    const label = wrapper.getAttribute('aria-label');
    if (label && !table.getAttribute('aria-label')) table.setAttribute('aria-label', label);
    table.querySelectorAll('thead th').forEach(cell => cell.setAttribute('scope', 'col'));
    if (wrapper.dataset.rowHeader === 'true') {
      table.querySelectorAll('tbody tr').forEach(row => {
        const first = row.firstElementChild;
        if (first) first.setAttribute('role', 'rowheader');
      });
    }
  }
  root.querySelectorAll('.r1-table[data-r1-table]').forEach(normalizeConfiguredTable);

  const tableWrappers = [...root.querySelectorAll('.r1-table-scroll-x')];
  function updateTableOverflow(wrapper) {
    const hint = document.getElementById(`${wrapper.id}-hint`);
    if (!hint) return;
    const overflowing = wrapper.scrollWidth > wrapper.clientWidth + 1;
    hint.hidden = !overflowing;
    if (overflowing) {
      wrapper.tabIndex = 0;
      wrapper.setAttribute('aria-describedby', hint.id);
    } else {
      wrapper.removeAttribute('tabindex');
      wrapper.removeAttribute('aria-describedby');
      wrapper.scrollLeft = 0;
    }
  }
  function updateAllTables() {
    tableWrappers.forEach(updateTableOverflow);
  }
  tableWrappers.forEach(wrapper => {
    wrapper.addEventListener('keydown', event => {
      if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
      if (wrapper.scrollWidth <= wrapper.clientWidth + 1) return;
      const direction = event.key === 'ArrowRight' ? 1 : -1;
      wrapper.scrollLeft += direction * Math.max(32, wrapper.clientWidth * .2);
      event.preventDefault();
    });
  });
  if ('ResizeObserver' in window) {
    const tableObserver = new ResizeObserver(entries => {
      entries.forEach(entry => updateTableOverflow(entry.target));
    });
    tableWrappers.forEach(wrapper => tableObserver.observe(wrapper));
  } else {
    window.addEventListener('resize', updateAllTables);
  }

  try {
    const sectionById = new Map();
    contentOrder.forEach(id => {
      const section = root.querySelector(`:scope > section#${CSS.escape(id)}`);
      sectionById.set(id, section);
    });

    const nav = document.createElement('nav');
    nav.className = 'r1-section-nav';
    nav.setAttribute('aria-label', `Các phần của học liệu “${TITLE}”`);
    const tablist = document.createElement('div');
    tablist.className = 'r1-tablist';
    tablist.setAttribute('role', 'tablist');
    tablist.setAttribute('aria-label', 'Chọn phần nội dung');
    tablist.setAttribute('aria-orientation', 'horizontal');
    nav.append(tablist);

    const viewPanel = document.createElement('div');
    viewPanel.id = 'r1-view-panel';
    viewPanel.className = 'r1-view-panel';
    viewPanel.setAttribute('role', 'tabpanel');
    viewPanel.tabIndex = 0;

    const returnBar = document.createElement('aside');
    returnBar.className = 'r1-support-return reading-region';
    returnBar.hidden = true;
    returnBar.setAttribute('aria-live', 'polite');

    const firstSection = sectionById.get(contentOrder[0]);
    const navSentinel = document.createElement('div');
    navSentinel.className = 'r1-nav-sentinel';
    navSentinel.setAttribute('aria-hidden', 'true');
    const navSlot = document.createElement('div');
    navSlot.className = 'r1-nav-slot';
    navSlot.append(nav);
    const navSpacer = document.createElement('div');
    navSpacer.className = 'r1-nav-spacer';
    navSpacer.setAttribute('aria-hidden', 'true');
    firstSection.before(navSentinel, navSlot, navSpacer, returnBar, viewPanel);
    contentOrder.forEach(id => viewPanel.append(sectionById.get(id)));

    const footer = root.querySelector('.r1-footer');
    // Prototype keeps the existing footer inside its reading region.

    const tabGroups = new Map();
    baseGroups.forEach(group => {
      const groupDefinitions = definitions.filter(item => item.group === group.id);
      if (!groupDefinitions.length) return;
      const groupNode = document.createElement('div');
      groupNode.className = `r1-tab-group r1-tab-group--${group.id}`;
      groupNode.dataset.r1TabGroup = group.id;
      const groupLabel = document.createElement('span');
      groupLabel.id = `r1-tab-group-label-${group.id}`;
      groupLabel.className = 'r1-tab-group-label';
      groupLabel.textContent = group.label;
      const groupItems = document.createElement('div');
      groupItems.className = 'r1-tab-group-items';
      groupNode.append(groupLabel, groupItems);
      tablist.append(groupNode);
      tabGroups.set(group.id, {label: groupLabel, items: groupItems});
    });

    const tabs = definitions.map((definition, index) => {
      const tab = document.createElement('button');
      tab.type = 'button';
      tab.id = `r1-tab-${definition.view}`;
      tab.className = 'r1-tab';
      tab.textContent = definition.label;
      tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-controls', viewPanel.id);
      tab.setAttribute('aria-describedby', tabGroups.get(definition.group).label.id);
      tab.setAttribute('aria-selected', index === 0 ? 'true' : 'false');
      tab.tabIndex = index === 0 ? 0 : -1;
      tabGroups.get(definition.group).items.append(tab);
      return tab;
    });

    const lessonPanel = sectionById.get('bai-hoc');
    const lessonToc = lessonPanel.querySelector('.lesson-toc');
    const lessonHeadings = [...lessonPanel.querySelectorAll(':scope > section.level3')].map(n => n.querySelector('h3'));
    const expectedLessonCount = Number.parseInt(root.dataset.r1LessonCount || '9', 10);
    if (!lessonToc || lessonHeadings.length !== expectedLessonCount) {
      throw new Error(`Lesson table of contents must contain ${expectedLessonCount} headings`);
    }
    if (!lessonToc.querySelector('a')) {
      const lineBlock = document.createElement('div');
      lineBlock.className = 'line-block';
      lessonHeadings.forEach(heading => {
        const line = document.createElement('div');
        line.className = 'line';
        const link = document.createElement('a');
        link.href = `#${heading.closest('section.level3').id}`;
        link.textContent = heading.textContent.trim();
        line.append(link);
        lineBlock.append(line);
      });
      lessonToc.append(lineBlock);
    }
    const lessonDetails = document.createElement('details');
    lessonDetails.className = 'r1-section-toc';
    const lessonSummary = document.createElement('summary');
    lessonSummary.textContent = 'Mục lục';
    const lessonNav = document.createElement('nav');
    lessonNav.setAttribute('aria-label', 'Mục lục bên trong Bài học');
    lessonToc.before(lessonDetails);
    lessonNav.append(lessonToc);
    lessonDetails.append(lessonSummary, lessonNav);

    let currentView = definitions[0].view;

    const header = document.getElementById('quarto-header');
    const navbar = header?.querySelector('.navbar');
    let expandedNavFootprint = 0;
    let condensedNavFootprint = 0;
    let expandedNavWidth = 0;
    function measureNavFootprints() {
      const wasCondensed = document.body.classList.contains('r1-nav-condensed');
      const oldSpacerHeight = navSpacer.style.height;
      navSpacer.style.height = '0px';
      document.body.classList.remove('r1-nav-condensed');
      navSlot.classList.remove('r1-nav-slot--condensed');
      expandedNavFootprint = navSpacer.getBoundingClientRect().top - navSentinel.getBoundingClientRect().top;
      document.body.classList.add('r1-nav-condensed');
      navSlot.classList.add('r1-nav-slot--condensed');
      condensedNavFootprint = navSpacer.getBoundingClientRect().top - navSentinel.getBoundingClientRect().top;
      document.body.classList.toggle('r1-nav-condensed', wasCondensed);
      navSlot.classList.toggle('r1-nav-slot--condensed', wasCondensed);
      navSpacer.style.height = oldSpacerHeight;
      expandedNavWidth = window.innerWidth;
    }
    function ensureTabVisible(tab) {
      if (!tab) return;
      const scroller = document.body.classList.contains('r1-nav-condensed')
        ? tablist
        : tab.closest('.r1-tab-group-items') || tablist;
      const tabEdgePadding = 12;
      if (tab.offsetLeft - tabEdgePadding < scroller.scrollLeft) {
        scroller.scrollLeft = Math.max(0, tab.offsetLeft - tabEdgePadding);
      } else if (tab.offsetLeft + tab.offsetWidth + tabEdgePadding > scroller.scrollLeft + scroller.clientWidth) {
        scroller.scrollLeft = tab.offsetLeft + tab.offsetWidth + tabEdgePadding - scroller.clientWidth;
      }
    }
    function updateDock() {
      if (!header || !navbar) return;
      const headerOffset = Math.max(0, header.getBoundingClientRect().bottom);
      const menuOpen = Boolean(navbar.querySelector('.navbar-collapse.show, .navbar-collapse.collapsing'));
      const condensed = navSentinel.getBoundingClientRect().bottom <= headerOffset + 1;
      const needsExpandedMeasure = !expandedNavFootprint || expandedNavWidth !== window.innerWidth;
      if (needsExpandedMeasure) measureNavFootprints();
      document.body.style.setProperty('--r1-header-height', `${headerOffset}px`);
      const spacerHeight = condensed ? Math.max(0, expandedNavFootprint - condensedNavFootprint) : 0;
      navSpacer.style.height = `${spacerHeight}px`;
      document.body.classList.toggle('r1-nav-condensed', condensed);
      navSlot.classList.toggle('r1-nav-slot--condensed', condensed);
      const navHeight = condensed ? navSlot.getBoundingClientRect().height : 0;
      document.body.style.setProperty('--r1-reader-offset', `${headerOffset + navHeight + 16}px`);
      header.classList.toggle('r1-menu-open', menuOpen);
      document.body.classList.toggle('r1-menu-open', menuOpen);
      nav.inert = menuOpen;
      ensureTabVisible(tablist.querySelector('.r1-tab[aria-selected="true"]'));
    }

    function defaultTarget(view) {
      if (view === 'toan-van') return contentOrder[0];
      const definition = byView.get(view);
      return definition?.target || definition?.ids[0] || contentOrder[0];
    }
    function ownerView(target) {
      if (!target || !root.contains(target)) return null;
      const explicitDefinition = definitions.find(item => {
        if (!item.target) return false;
        const explicitTarget = document.getElementById(item.target);
        return explicitTarget && (explicitTarget === target || explicitTarget.contains(target));
      });
      if (explicitDefinition) return explicitDefinition.view;
      const ownerSection = contentOrder
        .map(id => sectionById.get(id))
        .find(section => section === target || section.contains(target));
      if (!ownerSection) return definitions[0].view;
      return definitions.find(item => !item.target && item.ids.includes(ownerSection.id))?.view || definitions[0].view;
    }
    function targetFromHash(hash) {
      if (!hash || hash === '#') return null;
      let id;
      try { id = decodeURIComponent(hash.slice(1)); } catch { return null; }
      const target = document.getElementById(id);
      return target && root.contains(target) ? target : null;
    }
    function checkpointLabel(id) {
      const labels = {
        'bắt-đầu-từ-đâu': 'Khởi động',
        'cp-lt1': 'Điểm dừng sau chặng 1',
        'cp-lt2': 'Điểm dừng sau chặng 2',
        'cp-lt3': 'Điểm dừng sau chặng 3',
        'cp-kt': 'Điểm dừng sau Kiểm tra',
        'cp-on1': 'Điểm dừng Ôn lại 1',
        'cp-on2': 'Điểm dừng Ôn lại 2',
        'cp-on3': 'Điểm dừng Ôn lại 3'
      };
      const target = document.getElementById(id);
      const heading = target?.querySelector(':scope > h3, :scope > h4, :scope > .r1-task-label, :scope > p > .r1-task-label');
      if (root.dataset.r1SupportContext === 'semantic') {
        return target?.dataset.r1ReturnLabel ||
          target?.querySelector('h3,h4,h5,summary')?.textContent.trim() || 'hoạt động đang làm';
      }
      return labels[id] || heading?.textContent.trim() || id;
    }
    function supportTarget(target) {
      if (!target) return false;
      const owner = ownerView(target);
      return owner === 'sua-loi' || Boolean(target.closest('#on-nen, .r1-foundation-unit'));
    }
    function sourceCheckpoint(link) {
      const params = new URLSearchParams(location.search);
      // A second support resource must retain the original activity, not
      // replace it with the confirmation task currently being consulted.
      if (link.closest('#on-nen, #sua-loi, #loi-giai, #bai-hoc') && params.get(RETURN_PARAM)) {
        return params.get(RETURN_PARAM);
      }
      if (root.dataset.r1SupportContext === 'semantic') {
        const caller = link.closest('[data-zo-type="checkpoint"][id], [data-zo-type="task"][id], [data-zo-context^="stage:"][id]');
        return caller?.id || '';
      }
      if (link.closest('#bắt-đầu-từ-đâu')) return 'bắt-đầu-từ-đâu';
      const source = link.closest('section[id^="cp-"], [id^="cp-"]');
      if (source) return source.id;
      const task = link.closest('section.zo-learning-task--item[id], section.r1-confirmation-task[id]');
      if (task) return task.id;
      const stage = link.closest('[id^="g01-c"], [id^="g02-c"], #chuyen-giao');
      if (stage) return stage.id;
      return '';
    }
    function lessonSupportCall(link, target, callerId) {
      if (ownerView(target) !== 'bai-hoc' || !callerId) return false;
      const sourceOwner = ownerView(link);
      // Ordinary entry/lesson TOC clicks are not support calls. The ended
      // test checkpoint is eligible; test-question links are not invitations
      // to get help during an independent attempt.
      return sourceOwner === 'luyen-tap' || sourceOwner === 'on-lai' ||
        (sourceOwner === 'kiem-tra' && Boolean(link.closest(root.dataset.r1SupportContext === 'semantic' ? '[data-zo-type="checkpoint"][id]' : '#cp-kt'))) ||
        ((sourceOwner === 'sua-loi' || sourceOwner === 'on-nen' || sourceOwner === 'loi-giai') &&
          Boolean(new URLSearchParams(location.search).get(RETURN_PARAM)));
    }
    function directReturnOptions(target) {
      const id = target?.id || '';
      if (root.dataset.r1SupportContext === 'semantic') {
        const checkpoints = [...root.querySelectorAll('[data-r1-return-label][id]')];
        const area = id.startsWith('S-K') ? '#tu-kiem-tra' : id.startsWith('S-L') ? '#phieu-luyen' : id.startsWith('S-O') ? '#on-lai' : '';
        return checkpoints.filter(n => !area || n.closest(area)).map(n => n.id);
      }
      if (id.startsWith('g01-s-k-')) return ['cp-kt'];
      if (id.startsWith('sc')) return ['cp-lt1', 'cp-lt2', 'cp-lt3'];
      if (id.startsWith('g01-s-o-')) return ['cp-on1', 'cp-on2', 'cp-on3'];
      return ['bắt-đầu-từ-đâu', 'bai-hoc', 'cp-lt1', 'cp-lt2', 'cp-lt3', 'cp-kt', 'cp-on1', 'cp-on2', 'cp-on3'];
    }
    // Cross-package support carries its caller in the URL, independently per tab.
    function externalReturn(params = new URLSearchParams(location.search)) {
      const page = params.get('r1-return-page'), id = params.get(RETURN_PARAM);
      const view = params.get('r1-return-view');
      const current = location.pathname.match(/\/hoc_lieu\/([^/]+)\/index\.html$/)?.[1];
      if (!/^r[1-9]\d*_g\d+$/.test(page || '') || page === current || !id || !byView.has(view)) return null;
      return {page, id, view, label: params.get('r1-return-label') || 'hoạt động đã gọi hỗ trợ'};
    }
    function externalReturnUrl(context) {
      const url = new URL(`../${context.page}/index.html`, location.href);
      url.searchParams.set(VIEW_PARAM, context.view);
      url.hash = context.id;
      return `${url.pathname}${url.search}${url.hash}`;
    }
    function decorateExternalSupport(link) {
      if (!link || !root.contains(link) || link.classList.contains('r1-return-link')) return;
      const url = new URL(link.href, location.href);
      if (url.origin !== location.origin || url.pathname === location.pathname ||
          !/\/hoc_lieu\/r[1-9]\d*_g\d+\/index\.html$/.test(url.pathname) || !url.hash ||
          !['on-nen', 'bai-hoc', 'nhat-ky'].includes(url.searchParams.get(VIEW_PARAM))) return;
      const inherited = externalReturn();
      const page = location.pathname.match(/\/hoc_lieu\/([^/]+)\/index\.html$/)?.[1];
      const id = sourceCheckpoint(link) || link.closest('[id]')?.id;
      const caller = id && document.getElementById(id);
      const context = inherited || (caller && page ?
        {page, id, view: ownerView(caller), label: checkpointLabel(id)} : null);
      if (!context) return;
      url.searchParams.set('r1-return-page', context.page);
      url.searchParams.set(RETURN_PARAM, context.id);
      url.searchParams.set('r1-return-view', context.view);
      url.searchParams.set('r1-return-label', context.label);
      link.href = `${url.pathname}${url.search}${url.hash}`;
    }
    function renderExternalReturn() {
      const context = externalReturn();
      if (!context) return false;
      const link = document.createElement('a');
      link.className = 'r1-return-link';
      link.href = externalReturnUrl(context);
      link.textContent = `Quay lại ${context.label}`;
      returnBar.dataset.r1ExternalReturn = "true";
      returnBar.append(link);
      returnBar.hidden = false;
      return true;
    }
    function renderReturnBar(target) {
      const params = new URLSearchParams(location.search);
      const returnId = params.get(RETURN_PARAM);
      const context = params.get(CONTEXT_PARAM);
      returnBar.replaceChildren();
      delete returnBar.dataset.r1ExternalReturn;
      if (renderExternalReturn()) return;
      if (returnId && document.getElementById(returnId)) {
        const text = document.createElement('span');
        text.textContent = context ? `Đang hỗ trợ từ ${checkpointLabel(context)}. ` : 'Đang ở nhánh hỗ trợ. ';
        const link = document.createElement('a');
        link.className = 'r1-return-link';
        link.href = `?${VIEW_PARAM}=${encodeURIComponent(ownerView(document.getElementById(returnId)))}#${encodeURIComponent(returnId)}`;
        link.textContent = `Quay lại ${checkpointLabel(returnId)}`;
        returnBar.append(text, link);
        returnBar.hidden = false;
        return;
      }
      if (!supportTarget(target)) {
        returnBar.hidden = true;
        return;
      }
      const lead = document.createElement('span');
      lead.textContent = 'Em mở trực tiếp tài nguyên hỗ trợ này. Chọn nơi cần quay về: ';
      returnBar.append(lead);
      directReturnOptions(target).filter(id => document.getElementById(id)).forEach((id, index) => {
        if (index) returnBar.append(document.createTextNode(' · '));
        const link = document.createElement('a');
        link.className = 'r1-return-link';
        link.href = `?${VIEW_PARAM}=${encodeURIComponent(ownerView(document.getElementById(id)))}#${encodeURIComponent(id)}`;
        link.textContent = checkpointLabel(id);
        returnBar.append(link);
      });
      returnBar.hidden = false;
    }
    function openAncestors(target) {
      for (let node = target; node && node !== root; node = node.parentElement) {
        if (node.tagName === 'DETAILS') node.open = true;
      }
    }
    function focusTarget(target) {
      const focusNode = target?.matches('details') ? target.querySelector(':scope > summary') : target;
      if (!focusNode) return;
      const hadTabindex = focusNode.hasAttribute('tabindex');
      const oldTabindex = focusNode.getAttribute('tabindex');
      if (!hadTabindex) focusNode.tabIndex = -1;
      focusNode.focus({preventScroll: true});
      if (!hadTabindex) {
        focusNode.addEventListener('blur', () => focusNode.removeAttribute('tabindex'), {once: true});
      } else if (oldTabindex !== null) {
        focusNode.setAttribute('tabindex', oldTabindex);
      }
    }
    function scrollToTarget(target, focus = false) {
      requestAnimationFrame(() => requestAnimationFrame(() => {
        updateDock();
        target.scrollIntoView({block: 'start'});
        if (focus) focusTarget(target);
      }));
    }
    function clearViewScope() {
      viewPanel.querySelectorAll('[data-r1-view-hidden="true"]').forEach(node => {
        node.hidden = false;
        delete node.dataset.r1ViewHidden;
      });
      delete viewPanel.dataset.r1DeepTarget;
    }
    function hideForView(node) {
      if (!node || node.hidden) return;
      node.hidden = true;
      node.dataset.r1ViewHidden = 'true';
    }
    function applyViewScope(definition) {
      if (definition.view === 'toan-van') return;
      definitions
        .filter(item => item.target && item.view !== definition.view)
        .forEach(item => hideForView(document.getElementById(item.target)));
      if (!definition.target) return;
      const target = document.getElementById(definition.target);
      const ownerSection = contentOrder
        .map(id => sectionById.get(id))
        .find(section => section === target || section.contains(target));
      if (!target || !ownerSection) return;
      for (let branch = target; branch && branch !== ownerSection; branch = branch.parentElement) {
        const parent = branch.parentElement;
        if (!parent) break;
        [...parent.children].forEach(sibling => {
          if (sibling !== branch) hideForView(sibling);
        });
      }
      viewPanel.dataset.r1DeepTarget = target.id;
    }
    function showView(view) {
      const definition = byView.get(view) || definitions[0];
      currentView = definition.view;
      const showAll = currentView === 'toan-van';
      clearViewScope();
      contentOrder.forEach(id => {
        sectionById.get(id).hidden = !showAll && !definition.ids.includes(id);
      });
      applyViewScope(definition);
      tabs.forEach((tab, index) => {
        const selected = definitions[index].view === currentView;
        tab.setAttribute('aria-selected', selected ? 'true' : 'false');
        tab.tabIndex = selected ? 0 : -1;
      });
      const selectedTab = tabs[definitions.findIndex(item => item.view === currentView)];
      viewPanel.setAttribute('aria-labelledby', selectedTab.id);
      viewPanel.dataset.r1View = currentView;
      root.classList.toggle('r1-full-view', showAll);
      // Only scroll the tab strip horizontally; scrollIntoView would also
      // scroll the document back to the slot before the target is revealed.
      ensureTabVisible(selectedTab);
      requestAnimationFrame(() => {
        updateAllTables();
        updateLessonPosition();
      });
    }
    function urlFor(view, targetId, context) {
      const url = new URL(location.href);
      url.searchParams.set(VIEW_PARAM, view);
      if (externalReturn()) {
        // Keep the original caller while consulting local answers or another resource.
      } else if (context === null) {
        url.searchParams.delete(RETURN_PARAM);
        url.searchParams.delete(CONTEXT_PARAM);
      } else if (context) {
        url.searchParams.set(RETURN_PARAM, context.returnId);
        url.searchParams.set(CONTEXT_PARAM, context.checkpointId || context.returnId);
      }
      url.hash = targetId ? `#${encodeURIComponent(targetId)}` : '';
      return `${url.pathname}${url.search}${url.hash}`;
    }
    function writeLocation(view, targetId, replace = false, context) {
      const method = replace ? 'replaceState' : 'pushState';
      history[method]({r1View: view, r1Target: targetId}, '', urlFor(view, targetId, context));
    }
    function activateTab(index) {
      const definition = definitions[index];
      const target = document.getElementById(defaultTarget(definition.view));
      showView(definition.view);
      writeLocation(definition.view, target.id, false, null);
      openAncestors(target);
      renderReturnBar(target);
      scrollToTarget(target);
    }

    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => activateTab(index));
      tab.addEventListener('keydown', event => {
        let nextIndex = null;
        if (event.key === 'ArrowLeft') nextIndex = (index - 1 + tabs.length) % tabs.length;
        if (event.key === 'ArrowRight') nextIndex = (index + 1) % tabs.length;
        if (event.key === 'Home') nextIndex = 0;
        if (event.key === 'End') nextIndex = tabs.length - 1;
        if (nextIndex !== null) {
          tabs[nextIndex].focus();
          event.preventDefault();
          return;
        }
        if (event.key === 'Enter' || event.key === ' ') {
          activateTab(index);
          event.preventDefault();
        }
      });
    });

    // Decorate before native navigation, including modifier clicks and new tabs.
    for (const type of ['pointerdown', 'focusin', 'click', 'auxclick']) {
      root.addEventListener(type, event => decorateExternalSupport(event.target.closest('a[href]')));
    }
    root.addEventListener('click', event => {
      if (event.defaultPrevented || event.button !== 0 || event.metaKey ||
          event.ctrlKey || event.shiftKey || event.altKey) return;
      const link = event.target.closest('a[href]');
      if (!link || !root.contains(link) || link.origin !== location.origin ||
          link.pathname !== location.pathname || !link.hash) return;
      if (link.hash === '#xem-toan-bo') {
        event.preventDefault();
        const target = sectionById.get(defaultTarget('toan-van'));
        showView('toan-van');
        writeLocation('toan-van', target.id);
        scrollToTarget(target, true);
        return;
      }
      const target = targetFromHash(link.hash);
      if (!target) return;
      event.preventDefault();
      const checkpointId = sourceCheckpoint(link);
      const contextualSupport = supportTarget(target) || lessonSupportCall(link, target, checkpointId);
      const view = currentView === 'toan-van' ? 'toan-van' : ownerView(target);
      showView(view);
      openAncestors(target);
      if (link.classList.contains('r1-return-link')) {
        writeLocation(view, target.id, false, null);
      } else {
        const context = contextualSupport && checkpointId
          ? {returnId: checkpointId, checkpointId}
          : ownerView(target) === 'bai-hoc' && ownerView(link) === 'bai-hoc'
            ? undefined : null;
        writeLocation(view, target.id, false, context);
      }
      renderReturnBar(target);
      scrollToTarget(target, true);
    });

    function applyLocation(options = {}) {
      const params = new URLSearchParams(location.search);
      const requested = params.get(VIEW_PARAM);
      if (location.hash === '#xem-toan-bo') {
        const target = sectionById.get(defaultTarget('toan-van'));
        showView('toan-van');
        openAncestors(target);
        writeLocation('toan-van', target.id, true);
        if (options.scroll) scrollToTarget(target, options.focus);
        return;
      }
      const target = targetFromHash(location.hash);
      let view = byView.has(requested) ? requested : definitions[0].view;
      if (target && view !== 'toan-van') view = ownerView(target);
      showView(view);
      const finalTarget = target || document.getElementById(defaultTarget(view));
      openAncestors(finalTarget);
      const hasCanonicalState = requested === view && Boolean(target);
      const cleanDefault = !requested && !location.hash && view === definitions[0].view;
      if (!hasCanonicalState && !cleanDefault) writeLocation(view, finalTarget.id, true);
      renderReturnBar(finalTarget);
      if (options.scroll && target) scrollToTarget(finalTarget, options.focus);
    }

    let lessonTicking = false;
    function updateLessonPosition() {
      lessonTicking = false;
      updateDock();
      if (lessonPanel.hidden) return;
      const offset = Math.max(120, window.innerHeight * .24);
      let activeId = lessonHeadings[0].closest('section.level3').id;
      lessonHeadings.forEach(heading => {
        if (heading.getBoundingClientRect().top <= offset) activeId = heading.closest('section.level3').id;
      });
      lessonToc.querySelectorAll('a').forEach(link => {
        let linkId = '';
        try { linkId = decodeURIComponent(link.hash.slice(1)); } catch { linkId = ''; }
        if (linkId === activeId) link.setAttribute('aria-current', 'true');
        else link.removeAttribute('aria-current');
      });
    }
    function scheduleReaderPosition() {
      if (lessonTicking) return;
      lessonTicking = true;
      requestAnimationFrame(updateLessonPosition);
    }
    window.addEventListener('scroll', scheduleReaderPosition, {passive: true});
    window.addEventListener('resize', scheduleReaderPosition);
    if (header && navbar) {
      const dockObserver = new ResizeObserver(scheduleReaderPosition);
      [header, nav, navSlot].forEach(node => dockObserver.observe(node));
      new MutationObserver(scheduleReaderPosition).observe(navbar, {
        subtree: true, attributes: true, attributeFilter: ['class', 'aria-expanded']
      });
      new MutationObserver(scheduleReaderPosition).observe(header, {
        attributes: true, attributeFilter: ['class', 'style']
      });
      header.addEventListener('transitionend', scheduleReaderPosition);
    }

    document.querySelectorAll('.quarto-secondary-nav-title, .sidebar-title, .menu-text, .breadcrumb-item a')
      .forEach(node => {
        if (node.textContent.trim() === (root.dataset.r1Code || '')) node.textContent = TITLE;
      });
    document.querySelector('nav#TOC.toc-active')?.setAttribute('role', 'doc-toc');
    root.classList.add('r1-tabs-ready');
    document.body.classList.add('zo-on-thi-package-nav-ready', 'r1-package-nav-ready');
    updateDock();
    applyLocation({scroll: Boolean(location.hash), focus: false});
    window.addEventListener('load', () => {
      updateAllTables();
      if (location.hash) applyLocation({scroll: true, focus: false});
    }, {once: true});
    window.addEventListener('hashchange', () => applyLocation({scroll: true, focus: true}));
    window.addEventListener('popstate', () => applyLocation({scroll: true, focus: true}));
  } catch (error) {
    console.error(`Navigation for “${TITLE}” was not initialized.`, error);
  }
})();

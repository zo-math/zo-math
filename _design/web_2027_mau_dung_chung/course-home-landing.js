/* Progressive catalog enhancement. Without JS all canonical cards stay usable. */
/* Wall-clock countdown: never accumulate interval ticks or infer a new date. */
(() => {
  const clock = document.querySelector('.home-editorial .home-countdown');
  if (!clock) return;
  const target = Date.parse(clock.dataset.countdownTarget);
  const readout = clock.querySelector('.countdown-readout');
  const fallback = clock.querySelector('.countdown-fallback');
  const ended = clock.querySelector('.countdown-ended');
  if (!Number.isFinite(target) || !['reference', 'official'].includes(clock.dataset.countdownStatus)) {
    fallback.textContent = 'Chưa có mốc hợp lệ để đếm ngược. Xem thông tin lịch thi bên trên.';
    clock.dataset.countdownState = 'invalid';
    return;
  }
  let timer;
  function update() {
    const remaining = Math.max(0, Math.ceil((target - Date.now()) / 1000));
    const values = {days: Math.floor(remaining / 86400), hours: Math.floor(remaining / 3600) % 24,
      minutes: Math.floor(remaining / 60) % 60, seconds: remaining % 60};
    for (const [key, value] of Object.entries(values)) {
      const text = key === 'days' ? String(value) : String(value).padStart(2, '0');
      const node = clock.querySelector(`[data-time="${key}"]`);
      if (node.textContent !== text) node.textContent = text;
    }
    readout.setAttribute('aria-label', `Còn ${values.days} ngày, ${values.hours} giờ, ${values.minutes} phút, ${values.seconds} giây tới mốc thi Toán`);
    clock.querySelector('.countdown-sweep').style.strokeDashoffset = String(60-values.seconds);
    clock.dataset.countdownState = remaining ? 'running' : 'ended';
    readout.hidden = false;
    fallback.hidden = true;
    if (!remaining) {
      if (ended.hidden) ended.textContent = clock.dataset.countdownStatus === 'reference'
        ? 'Đã đến mốc tham chiếu. Hãy kiểm tra lịch thi chính thức; mốc này không xác nhận kỳ thi đã bắt đầu.'
        : 'Đã đến mốc giờ thi. Theo dõi thông báo chính thức của kỳ thi.';
      ended.hidden = false;
      clearInterval(timer);
    } else ended.hidden = true;
    return remaining;
  }
  function resume() {
    clearInterval(timer);
    if (update() && !document.hidden) timer = setInterval(update, 1000);
  }
  document.addEventListener('visibilitychange', resume);
  window.addEventListener('pageshow', resume);
  resume();
})();
(() => {
  if (!document.body.classList.contains('home-editorial')) return;
  const tools = document.querySelector('.home-catalog-tools');
  const search = document.querySelector('#home-search');
  const cards = [...document.querySelectorAll('.home-card[data-package-id]')];
  const status = document.querySelector('.home-filter-status');
  const filters = [...tools.querySelectorAll('[data-filter]')];
  let category = 'all';
  const fold = text => text.toLocaleLowerCase('vi').normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd');
  function apply() {
    const query = fold(search.value.trim());
    let count = 0;
    cards.forEach(card => {
      card.hidden = (category !== 'all' && card.dataset.category !== category) || !fold(card.textContent).includes(query);
      if (!card.hidden) count++;
    });
    filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
    status.hidden = false;
    status.textContent = count ? `${count} học liệu phù hợp.` : 'Chưa có học liệu phù hợp. Thử tên khác hoặc chọn Tất cả.';
  }
  filters.forEach(button => button.addEventListener('click', () => { category = button.dataset.filter; apply(); }));
  search.addEventListener('input', apply);
  tools.hidden = false;
})();

/* Reveal only the requested solution; other answers stay closed. */
(() => {
  const reveal = hash => {
    let id; try { id = decodeURIComponent((hash || "").replace(/^#/, "")); } catch { return; }
    const target = document.getElementById(id);
    if (target instanceof HTMLDetailsElement) target.open = true;
    for (let node = target?.parentElement; node; node = node.parentElement) {
      if (node instanceof HTMLDetailsElement) node.open = true;
    }
  };
  addEventListener("hashchange", () => reveal(location.hash));
  document.addEventListener("click", event => {
    const link = event.target.closest?.("a[href]");
    if (!link) return;
    const target = new URL(link.href, location.href);
    if (target.origin === location.origin && target.pathname === location.pathname) reveal(target.hash);
  });
  reveal(location.hash);
})();

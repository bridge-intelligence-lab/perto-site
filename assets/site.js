/* perto.life — the one script: theme toggle and WhatsApp click counts. No cookies, nothing personal. */
(function () {
  var KEY = 'perto-theme';
  var root = document.documentElement;

  function stored() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function store(v) {
    try { localStorage.setItem(KEY, v); } catch (e) { /* private window or blocked storage: the choice lasts this page only */ }
  }
  function current() {
    var t = root.getAttribute('data-theme');
    if (t === 'dark' || t === 'light') return t;
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  /* The button shows the theme you would switch TO; its title must say the same as the visible icon's hidden text. */
  function syncTitle() {
    var btn = document.querySelector('[data-theme-toggle]');
    var shown = btn && btn.querySelector(current() === 'dark' ? '.to-light' : '.to-dark');
    if (shown) btn.title = shown.textContent.trim();
  }
  function toggleTheme() {
    var next = current() === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    store(next);
    syncTitle();
  }
  syncTitle();

  document.addEventListener('click', function (e) {
    var btn = e.target.closest && e.target.closest('[data-theme-toggle]');
    if (btn) { toggleTheme(); return; }

    /* Count a WhatsApp button click as an event, then let the navigation proceed. */
    var a = e.target.closest && e.target.closest('a[data-source]');
    if (!a) return;
    var source = a.getAttribute('data-source');
    if (window.goatcounter && window.goatcounter.count) {
      try {
        window.goatcounter.count({
          path: 'event/whatsapp/' + source,
          title: 'WhatsApp ' + source,
          referrer: location.pathname,
          event: true
        });
      } catch (err) { /* counting must never break the link */ }
      /* count.js uses sendBeacon, which survives navigation; without it, give the request a moment. */
      if (!navigator.sendBeacon && !e.defaultPrevented) {
        e.preventDefault();
        setTimeout(function () { location.href = a.href; }, 150);
      }
    }
  });
})();

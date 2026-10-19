/* Derm Teach — small vanilla JS. Works from file:// and any static host (no modules, no frameworks). */
(function () {
  "use strict";
  var doc = document, html = doc.documentElement, body = doc.body;
  var root = body.getAttribute("data-root") || "";
  var $ = function (s, el) { return (el || doc).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || doc).querySelectorAll(s)); };
  function escH(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  /* ---------------- initial scroll position ----------------
     A fresh load without a #hash must start at the very top. Some iOS in-app browsers (WKWebView /
     SFSafariViewController) restore or nudge the scroll position while fonts and the sticky header settle,
     which left the hero title under the header. Back/forward keeps the browser's normal restoration. */
  var navType = ""; try { var ne = performance.getEntriesByType("navigation")[0]; navType = ne ? ne.type : ""; } catch (e) {}
  var userMoved = false;
  ["touchstart", "wheel", "keydown", "mousedown"].forEach(function (ev) { window.addEventListener(ev, function () { userMoved = true; }, { passive: true, once: true }); });
  function toTop() { if (!location.hash && navType !== "back_forward" && !userMoved && window.scrollY !== 0) window.scrollTo(0, 0); }
  if (!location.hash && navType !== "back_forward" && "scrollRestoration" in history) history.scrollRestoration = "manual";
  toTop();
  window.addEventListener("load", function () { toTop(); requestAnimationFrame(function () { toTop(); html.classList.add("ready"); }); });
  window.addEventListener("pageshow", function (e) { if (!e.persisted) toTop(); });
  if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(toTop);
  /* sticky section bar on narrow condition pages: keep scroll-padding equal to header + bar */
  var tocBar = doc.querySelector(".toc");
  if (tocBar) {
    html.classList.add("has-toc");
    var setTocH = function () { var h = tocBar.getBoundingClientRect().height; if (h) html.style.setProperty("--toc-h", Math.round(h) + "px"); };
    setTocH(); window.addEventListener("resize", setTocH, { passive: true });
  }

  /* ---------------- theme ---------------- */
  var mq = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
  function effectiveTheme() { var t = html.getAttribute("data-theme"); return t || (mq && mq.matches ? "dark" : "light"); }
  function syncThemeMeta() {
    var dark = effectiveTheme() === "dark";
    $$("meta[name=theme-color]").forEach(function (m) { m.setAttribute("content", dark ? "#0b1214" : "#ffffff"); m.removeAttribute("media"); });
    $$(".theme-toggle").forEach(function (b) { b.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode"); b.setAttribute("aria-pressed", dark ? "true" : "false"); });
  }
  $$(".theme-toggle").forEach(function (b) {
    b.addEventListener("click", function () {
      var next = effectiveTheme() === "dark" ? "light" : "dark";
      // if the choice matches the OS preference, drop the override so the site follows the OS again
      var sys = mq && mq.matches ? "dark" : "light";
      try { if (next === sys) { localStorage.removeItem("dt-theme"); } else { localStorage.setItem("dt-theme", next); } } catch (e) {}
      if (next === sys) html.removeAttribute("data-theme"); else html.setAttribute("data-theme", next);
      syncThemeMeta();
    });
  });
  if (mq && mq.addEventListener) mq.addEventListener("change", syncThemeMeta);
  syncThemeMeta();

  /* ---------------- drawer ---------------- */
  var drawer = $("#drawer"), backdrop = $(".drawer-backdrop"), openBtns = $$("[data-drawer-open]"), lastOpener = null;
  function setDrawer(open, opener) {
    if (!drawer) return;
    drawer.classList.toggle("open", open);
    drawer.setAttribute("aria-hidden", open ? "false" : "true");
    if (open) drawer.removeAttribute("inert"); else drawer.setAttribute("inert", "");
    backdrop.hidden = !open;
    body.classList.toggle("drawer-open", open);
    openBtns.forEach(function (b) { b.setAttribute("aria-expanded", open ? "true" : "false"); });
    if (open) {
      lastOpener = opener || null;
      var cur = drawer.querySelector("[aria-current=page]") || drawer.querySelector("a,button,summary");
      if (cur) {
        cur.focus({ preventScroll: true });
        var sc = drawer.querySelector(".drawer-scroll");
        if (sc) { var r = cur.getBoundingClientRect(), sr = sc.getBoundingClientRect(); sc.scrollTop += (r.top - sr.top) - (sc.clientHeight - r.height) / 2; }
      }
    } else if (lastOpener) lastOpener.focus({ preventScroll: true });
  }
  openBtns.forEach(function (b) { b.addEventListener("click", function () { setDrawer(true, b); }); });
  $$("[data-drawer-close]").forEach(function (b) { b.addEventListener("click", function () { setDrawer(false); }); });

  /* ---------------- search ---------------- */
  var INDEX = window.DERM_SEARCH || [];
  if (!INDEX.length && window.fetch) {
    fetch(root + "assets/data/search-index.json").then(function (r) { return r.json(); }).then(function (d) { INDEX = d; }).catch(function () {});
  }
  function norm(s) { return (s || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[’']/g, "'"); }
  function hl(text, q) {
    var t = escH(text); if (!q) return t;
    var i = norm(text).indexOf(q);
    if (i < 0) return t;
    return escH(text.slice(0, i)) + "<mark>" + escH(text.slice(i, i + q.length)) + "</mark>" + escH(text.slice(i + q.length));
  }
  function wordStart(text, q) { var i = text.indexOf(q); while (i > -1) { if (i === 0 || /[^a-z0-9]/.test(text.charAt(i - 1))) return true; i = text.indexOf(q, i + 1); } return false; }
  function score(item, q) {
    var t = norm(item.t), s = 0, akaHit = "";
    if (t === q) s = 100; else if (t.indexOf(q) === 0) s = 80; else if (wordStart(t, q)) s = 70; else if (t.indexOf(q) > -1) s = 32;
    (item.a || []).forEach(function (a) {
      var n = norm(a); if (!n) return;
      var v = n === q ? 75 : n.indexOf(q) === 0 ? 58 : wordStart(n, q) ? 50 : n.indexOf(q) > -1 ? 30 : 0;
      if (v > s) s = v;
      if (v && !akaHit) akaHit = a;
    });
    if (!s && norm(item.c).indexOf(q) > -1) s = 25;
    if (!s && norm(item.s).indexOf(q) > -1) s = 20;
    if (!s && q.indexOf(" ") > -1) {
      var hay = norm(item.t + " " + (item.a || []).join(" ") + " " + item.s + " " + item.c);
      if (q.split(/\s+/).every(function (w) { return hay.indexOf(w) > -1; })) s = 10;
    }
    if (item.cat && s) s -= 3;
    return { s: s, aka: akaHit };
  }
  $$(".search").forEach(function (box) {
    var input = $(".search-input", box), list = $(".search-results", box), sel = -1;
    var lid = "sr-" + Math.random().toString(36).slice(2, 8);
    list.id = lid; input.setAttribute("aria-controls", lid);
    function close() { list.hidden = true; input.setAttribute("aria-expanded", "false"); }
    function render() {
      var raw = input.value.trim(), q = norm(raw);
      if (!q) { list.innerHTML = ""; close(); return; }
      var items = INDEX.map(function (it) { var r = score(it, q); return { it: it, s: r.s, aka: r.aka }; })
        .filter(function (r) { return r.s > 0; })
        .sort(function (a, b) { return b.s - a.s || a.it.t.localeCompare(b.it.t); }).slice(0, 9);
      sel = items.length ? 0 : -1;
      if (!items.length) {
        list.innerHTML = '<li class="r-empty">No matches for “' + escH(raw) + '”. Try another name or <a href="' + root + 'index.html#categories">browse categories</a>.</li>';
      } else {
        list.innerHTML = items.map(function (r, i) {
          var it = r.it;
          var meta = it.cat ? "Category · " + (it.n || 0) + " pages" : it.c + (it.soon ? " · soon" : "");
          var via = r.aka && norm(it.t).indexOf(q) < 0 ? ' <span class="r-via">· “' + hl(r.aka, q) + "”</span>" : "";
          return '<li role="presentation"><a role="option" id="' + lid + "-" + i + '" href="' + root + it.u + '" style="--col:' + it.col + '" aria-selected="' + (i === sel) + '">' +
            '<span class="r-t">' + hl(it.t, q) + via + "</span>" +
            '<span class="r-m">' + escH(meta) + "</span>" +
            '<span class="r-s">' + escH(it.s) + "</span></a></li>";
        }).join("") + '<li class="r-foot" role="presentation" aria-hidden="true"><span><kbd>↑</kbd> <kbd>↓</kbd> move</span><span><kbd>↵</kbd> open</span><span><kbd>esc</kbd> close</span></li>';
      }
      list.hidden = false; input.setAttribute("aria-expanded", "true");
      input.setAttribute("aria-activedescendant", sel > -1 ? lid + "-" + sel : "");
    }
    function move(d) {
      var links = $$("a[role=option]", list); if (!links.length) return;
      sel = (sel + d + links.length) % links.length;
      links.forEach(function (a, i) { a.setAttribute("aria-selected", i === sel ? "true" : "false"); });
      input.setAttribute("aria-activedescendant", links[sel].id);
      var lr = links[sel].getBoundingClientRect(), br = list.getBoundingClientRect();
      if (lr.top < br.top) list.scrollTop -= br.top - lr.top; else if (lr.bottom > br.bottom) list.scrollTop += lr.bottom - br.bottom;
    }
    input.addEventListener("input", render);
    input.addEventListener("focus", function () { if (input.value) render(); });
    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") { e.preventDefault(); move(1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); move(-1); }
      else if (e.key === "Enter") {
        var links = $$("a[role=option]", list);
        if (links[sel]) { e.preventDefault(); window.location.href = links[sel].getAttribute("href"); }
      } else if (e.key === "Escape") {
        if (input.value) { input.value = ""; render(); } else { input.blur(); body.classList.remove("search-open"); }
      }
    });
    doc.addEventListener("click", function (e) { if (!box.contains(e.target)) close(); });
  });
  // mobile search toggle
  var st = $(".search-toggle");
  if (st) st.addEventListener("click", function () {
    var open = !body.classList.contains("search-open");
    body.classList.toggle("search-open", open);
    st.setAttribute("aria-expanded", open ? "true" : "false");
    if (open) { var i = $(".search-top .search-input"); if (i) setTimeout(function () { i.focus({ preventScroll: true }); }, 30); }
  });
  function focusSearch() {
    var s = $(".search-hero .search-input");
    if (!s || s.getBoundingClientRect().bottom < 60) {
      if (st && getComputedStyle(st).display !== "none") { body.classList.add("search-open"); }
      s = $(".search-top .search-input");
    }
    if (s) { s.focus({ preventScroll: true }); s.select(); }
  }
  doc.addEventListener("keydown", function (e) {
    var tag = ((doc.activeElement || {}).tagName || "").toLowerCase();
    if ((e.key === "/" && !/input|textarea|select/.test(tag)) || (e.key === "k" && (e.metaKey || e.ctrlKey))) { e.preventDefault(); focusSearch(); }
    if (e.key === "Escape" && drawer && drawer.classList.contains("open")) setDrawer(false);
  });

  /* ---------------- sections: hash, expand/collapse, scrollspy, progress ---------------- */
  function openFor(hash) {
    if (!hash || hash.length < 2) return;
    var el; try { el = doc.getElementById(decodeURIComponent(hash.slice(1))); } catch (e) { return; }
    if (!el) return;
    var d = el.matches("details") ? el : el.querySelector(":scope > details:not(.more)");
    if (d && !d.open) d.open = true;
    var p = el.closest("details"); if (p) p.open = true;
  }
  openFor(location.hash);
  window.addEventListener("hashchange", function () { openFor(location.hash); });
  $$("[data-toc]").forEach(function (a) { a.addEventListener("click", function () { openFor(a.getAttribute("href")); }); });
  var exp = $("[data-expand]"), col = $("[data-collapse]"), prt = $("[data-print]");
  if (exp) exp.addEventListener("click", function () { $$(".sec > details").forEach(function (d) { d.open = true; }); });
  if (col) col.addEventListener("click", function () { $$(".sec > details").forEach(function (d) { d.open = false; }); });
  if (prt) prt.addEventListener("click", function () { window.print(); });
  // print: open every section and load lazy images
  var reclose = [];
  window.addEventListener("beforeprint", function () {
    reclose = $$("details:not([open])"); reclose.forEach(function (d) { d.open = true; });
    $$("img[loading=lazy]").forEach(function (i) { i.loading = "eager"; });
  });
  window.addEventListener("afterprint", function () { reclose.forEach(function (d) { d.open = false; }); reclose = []; });

  var tocLinks = $$("[data-toc]");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var map = {}; tocLinks.forEach(function (a) { map[a.getAttribute("data-toc")] = a; });
    var visible = {}, current = null;
    var setActive = function (id) {
      if (id === current) return; current = id;
      tocLinks.forEach(function (a) { var on = a === map[id]; a.classList.toggle("active", on); if (on) a.setAttribute("aria-current", "location"); else a.removeAttribute("aria-current"); });
      var a = map[id], bar = a && a.closest(".toc-list");
      if (a && bar && bar.scrollWidth > bar.clientWidth + 4) {
        var left = a.offsetLeft - 24;
        if (left < bar.scrollLeft || left + a.offsetWidth + 48 > bar.scrollLeft + bar.clientWidth) bar.scrollTo({ left: left, behavior: "smooth" });
      }
    };
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { visible[e.target.id] = e.isIntersecting ? e.boundingClientRect.top : undefined; });
      var best = null, bestTop = Infinity;
      Object.keys(visible).forEach(function (id) { var t = visible[id]; if (t !== undefined && t < bestTop) { bestTop = t; best = id; } });
      if (best) setActive(best);
    }, { rootMargin: "-130px 0px -55% 0px", threshold: 0 });
    $$(".sec[id]").forEach(function (s) { io.observe(s); });
  }
  var bar = $(".progress span");
  if (bar && body.classList.contains("condition")) {
    var ticking = false;
    var upd = function () {
      ticking = false;
      var h = doc.documentElement.scrollHeight - window.innerHeight;
      bar.style.setProperty("--p", h > 0 ? Math.min(1, window.scrollY / h).toFixed(4) : 0);
    };
    window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(upd); } }, { passive: true });
    upd();
  }

  /* ---------------- lightbox ---------------- */
  var lb = $("#lightbox");
  var triggers = $$("[data-lb]");
  if (lb && triggers.length) {
    var img = $("img", lb), cap = $(".lb-cap", lb), cred = $(".lb-credit", lb), cnt = $(".lb-count", lb), cur = 0, lastFocus = null;
    var show = function (i) {
      cur = (i + triggers.length) % triggers.length;
      var t = triggers[cur];
      img.src = t.getAttribute("data-src");
      img.alt = (t.querySelector("img") || {}).alt || "";
      cap.textContent = t.getAttribute("data-caption") || "";
      var href = t.getAttribute("data-href"), ai = t.getAttribute("data-ai") === "1";
      cred.innerHTML = escH(t.getAttribute("data-credit") || "") + (href ? ' · <a href="' + escH(href) + '" target="_blank" rel="noopener">View source</a>' : "");
      cnt.textContent = (cur + 1) + " / " + triggers.length;
      // preload neighbours
      [cur - 1, cur + 1].forEach(function (k) { var n = triggers[(k + triggers.length) % triggers.length]; (new Image()).src = n.getAttribute("data-src"); });
    };
    var open = function (i) { lastFocus = doc.activeElement; show(i); lb.hidden = false; body.style.overflow = "hidden"; $(".lb-close", lb).focus({ preventScroll: true }); };
    var close = function () { lb.hidden = true; body.style.overflow = ""; img.removeAttribute("src"); if (lastFocus) lastFocus.focus({ preventScroll: true }); };
    triggers.forEach(function (t, i) { t.addEventListener("click", function () { open(i); }); });
    $(".lb-close", lb).addEventListener("click", close);
    $(".lb-prev", lb).addEventListener("click", function () { show(cur - 1); });
    $(".lb-next", lb).addEventListener("click", function () { show(cur + 1); });
    lb.addEventListener("click", function (e) { if (e.target === lb || e.target.classList.contains("lb-fig") || e.target.classList.contains("lb-stage")) close(); });
    doc.addEventListener("keydown", function (e) {
      if (lb.hidden) return;
      if (e.key === "Escape") close();
      else if (e.key === "ArrowLeft") show(cur - 1);
      else if (e.key === "ArrowRight") show(cur + 1);
      else if (e.key === "Tab") { // keep focus inside the dialog
        var f = $$("button, a[href]", lb).filter(function (x) { return x.offsetParent !== null; });
        if (!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && doc.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && doc.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    var x0 = null;
    lb.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener("touchend", function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) > 50) show(cur + (dx < 0 ? 1 : -1));
    });
  }
})();

/* ---------------- v3 lessons: progress, next-step, module list ---------------- */
(function () {
  "use strict";
  var doc = document, KEY = "dt-progress-v1";
  var $$ = function (s, el) { return Array.prototype.slice.call((el || doc).querySelectorAll(s)); };
  function load() { try { return JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { return {}; } }
  function save(d) { try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (e) {} }

  // module (category) page
  $$(".les[data-lesson]").forEach(function (li) {
    var all = load(), done = (all[li.getAttribute("data-lesson")] || []).length, n = +li.getAttribute("data-steps") || 0;
    var state = li.querySelector(".les-state");
    if (n && done >= n) { li.classList.add("is-done"); if (state) state.textContent = "Completed"; }
    else if (done) { li.classList.add("is-started"); if (state) state.textContent = done + "/" + n + " steps"; }
  });
  var mp = doc.querySelector(".module-progress");
  if (mp) {
    var les = $$(".les[data-lesson]"), c = les.filter(function (l) { return l.classList.contains("is-done"); }).length;
    mp.querySelector(".mp-n").textContent = c;
    mp.querySelector(".lp-bar span").style.setProperty("--pct", les.length ? c / les.length : 0);
  }

  // lesson page
  var body = doc.querySelector(".lesson-body[data-lesson]");
  if (!body) return;
  var slug = body.getAttribute("data-lesson"), steps = $$(".step[data-step]", body), n = steps.length;
  var links = {}; $$("[data-step-link]").forEach(function (a) { links[a.getAttribute("data-step-link")] = a; });
  var lp = doc.querySelector(".lesson-progress"), nowN = doc.querySelector(".toc-now-n"), nowBar = doc.querySelector(".toc-now-bar span");
  var stepbar = doc.querySelector(".stepper");
  function doneSet() { return (load()[slug] || []).map(String); }
  function render() {
    var d = doneSet();
    steps.forEach(function (s) {
      var k = s.getAttribute("data-step"), on = d.indexOf(k) > -1;
      s.classList.toggle("done", on);
      if (links[k]) { links[k].classList.toggle("done", on); links[k].setAttribute("title", on ? "Done" : ""); }
    });
    if (lp) { lp.querySelector(".lp-n").textContent = d.length; lp.querySelector(".lp-bar span").style.setProperty("--pct", n ? d.length / n : 0); }
  }
  function mark(k) {
    var all = load(), d = (all[slug] || []).map(String);
    if (d.indexOf(String(k)) < 0) { d.push(String(k)); all[slug] = d; save(all); render(); }
  }
  render();
  // the sticky lesson bar height feeds scroll-padding so headings are never hidden under it
  function syncBar() {
    var h = stepbar && getComputedStyle(stepbar).position === "sticky" ? stepbar.getBoundingClientRect().height : 0;
    doc.documentElement.style.setProperty("--stepbar", Math.round(h) + "px");
  }
  syncBar(); window.addEventListener("resize", syncBar);
  // current step + mark steps the reader has scrolled all the way through
  var ticking = false, dwell = {}, lastT = 0;
  setInterval(function () { if (!document.hidden) onScroll(); }, 1000);
  function onScroll() {
    ticking = false;
    var top = (parseFloat(getComputedStyle(doc.documentElement).getPropertyValue("--top")) || 60) + (stepbar && getComputedStyle(stepbar).position === "sticky" ? stepbar.offsetHeight : 0);
    var cur = 1, now = Date.now();
    steps.forEach(function (s) {
      var r = s.getBoundingClientRect();
      if (r.top <= top + 80) cur = +s.getAttribute("data-step");
      var k = s.getAttribute("data-step"), vis = r.top < innerHeight && r.bottom > top;
      if (vis) { dwell[k] = (dwell[k] || 0) + (now - (lastT || now)); }
      // a step counts as done once it has been read for a while (≥ 4 s in view) and scrolled past
      if (r.bottom < top + 40 && (dwell[k] || 0) > 4000) mark(k);
    });
    lastT = now;
    if (nowN) nowN.textContent = "Step " + cur + " of " + n;
    if (nowBar) nowBar.style.setProperty("--pct", n ? cur / n : 0);
  }
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
  $$("[data-next]").forEach(function (a) { a.addEventListener("click", function () { var s = a.closest(".step"); if (s) mark(s.getAttribute("data-step")); }); });
  $$("[data-finish]").forEach(function (a) { a.addEventListener("click", function () { var s = a.closest(".step"); if (s) mark(s.getAttribute("data-step")); }); });
  var reset = doc.querySelector("[data-reset]");
  if (reset) reset.addEventListener("click", function () { var all = load(); delete all[slug]; save(all); render(); });
})();

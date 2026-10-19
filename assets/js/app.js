/* Derm Teach: small vanilla JS. Works from file:// (no fetch, no modules). */
(function () {
  "use strict";
  var root = document.body.getAttribute("data-root") || "";
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };

  /* ---------------- drawer ---------------- */
  var drawer = $("#drawer"), backdrop = $(".drawer-backdrop"), openBtn = $("[data-drawer-open]");
  function setDrawer(open) {
    if (!drawer) return;
    drawer.classList.toggle("open", open);
    drawer.setAttribute("aria-hidden", open ? "false" : "true");
    backdrop.hidden = !open;
    document.body.classList.toggle("drawer-open", open);
    if (openBtn) openBtn.setAttribute("aria-expanded", open ? "true" : "false");
    if (open) { var f = drawer.querySelector("a,button,summary"); if (f) f.focus(); }
    else if (openBtn) openBtn.focus();
  }
  if (openBtn) openBtn.addEventListener("click", function () { setDrawer(true); });
  $$("[data-drawer-close]").forEach(function (b) { b.addEventListener("click", function () { setDrawer(false); }); });

  /* ---------------- search ---------------- */
  var INDEX = window.DERM_SEARCH || [];
  function norm(s) { return (s || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[’']/g, "'"); }
  function escH(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function hl(text, q) {
    var t = escH(text); if (!q) return t;
    var i = norm(text).indexOf(q);
    if (i < 0) return t;
    return escH(text.slice(0, i)) + "<mark>" + escH(text.slice(i, i + q.length)) + "</mark>" + escH(text.slice(i + q.length));
  }
  function score(item, q) {
    var t = norm(item.t), s = 0;
    if (t === q) s = 100; else if (t.indexOf(q) === 0) s = 80; else if (t.indexOf(q) > -1) s = 60;
    var akaHit = "";
    (item.a || []).forEach(function (a) {
      var n = norm(a);
      if (!n) return;
      var v = n === q ? 70 : n.indexOf(q) === 0 ? 55 : n.indexOf(q) > -1 ? 45 : 0;
      if (v > s) { s = v; }
      if (v && !akaHit) akaHit = a;
    });
    if (!s && norm(item.s).indexOf(q) > -1) s = 20;
    if (!s && norm(item.c).indexOf(q) > -1) s = 15;
    // multi-word: every word must appear somewhere
    if (!s && q.indexOf(" ") > -1) {
      var hay = norm(item.t + " " + (item.a || []).join(" ") + " " + item.s + " " + item.c);
      if (q.split(/\s+/).every(function (w) { return hay.indexOf(w) > -1; })) s = 10;
    }
    if (item.cat) s -= 5;
    return { s: s, aka: akaHit };
  }
  $$(".search").forEach(function (box) {
    var input = $(".search-input", box), list = $(".search-results", box), sel = -1, items = [];
    function render() {
      var q = norm(input.value.trim());
      if (!q) { list.hidden = true; list.innerHTML = ""; return; }
      items = INDEX.map(function (it) { var r = score(it, q); return { it: it, s: r.s, aka: r.aka }; })
        .filter(function (r) { return r.s > 0; })
        .sort(function (a, b) { return b.s - a.s || a.it.t.localeCompare(b.it.t); }).slice(0, 10);
      sel = items.length ? 0 : -1;
      if (!items.length) {
        list.innerHTML = '<li class="r-empty">No conditions match “' + escH(input.value) + '”. Try another name or <a href="' + root + 'index.html">browse categories</a>.</li>';
      } else {
        list.innerHTML = items.map(function (r, i) {
          var it = r.it;
          var meta = it.cat ? "Category" : it.c + (it.soon ? " · coming soon" : "");
          var via = r.aka && norm(it.t).indexOf(q) < 0 ? " · matches “" + hl(r.aka, q) + "”" : "";
          return '<li><a role="option" href="' + root + it.u + '" style="--col:' + it.col + '"' + (i === sel ? ' aria-selected="true"' : "") + ">" +
            '<span class="r-t">' + hl(it.t, q) + "</span>" +
            '<span class="r-m">' + escH(meta) + via + "</span>" +
            '<span class="r-s">' + escH(it.s) + "</span></a></li>";
        }).join("");
      }
      list.hidden = false;
    }
    function move(d) {
      var links = $$("a[role=option]", list); if (!links.length) return;
      sel = (sel + d + links.length) % links.length;
      links.forEach(function (a, i) { a.setAttribute("aria-selected", i === sel ? "true" : "false"); });
      links[sel].scrollIntoView({ block: "nearest" });
    }
    input.addEventListener("input", render);
    input.addEventListener("focus", function () { if (input.value) render(); });
    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") { e.preventDefault(); move(1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); move(-1); }
      else if (e.key === "Enter") {
        var links = $$("a[role=option]", list);
        if (links[sel]) { e.preventDefault(); window.location.href = links[sel].getAttribute("href"); }
      } else if (e.key === "Escape") { input.value = ""; render(); input.blur(); }
    });
    document.addEventListener("click", function (e) { if (!box.contains(e.target)) list.hidden = true; });
  });
  // "/" focuses search
  document.addEventListener("keydown", function (e) {
    if (e.key === "/" && !/input|textarea/i.test((document.activeElement || {}).tagName || "")) {
      var s = $(".search-hero .search-input") || $(".search-top .search-input");
      if (s && s.offsetParent !== null) { e.preventDefault(); s.focus(); }
    }
    if (e.key === "Escape" && drawer && drawer.classList.contains("open")) setDrawer(false);
  });

  /* ---------------- sections: hash, expand/collapse, scrollspy ---------------- */
  function openFor(hash) {
    if (!hash || hash.length < 2) return;
    var el = document.getElementById(decodeURIComponent(hash.slice(1)));
    if (!el) return;
    var d = el.matches("details") ? el : el.querySelector("details");
    if (d && !d.open) d.open = true;
    var p = el.closest("details"); if (p) p.open = true;
  }
  openFor(location.hash);
  window.addEventListener("hashchange", function () { openFor(location.hash); });
  $$("[data-toc]").forEach(function (a) {
    a.addEventListener("click", function () { openFor(a.getAttribute("href")); });
  });
  var exp = $("[data-expand]"), col = $("[data-collapse]");
  if (exp) exp.addEventListener("click", function () { $$(".sec > details").forEach(function (d) { d.open = true; }); });
  if (col) col.addEventListener("click", function () { $$(".sec > details").forEach(function (d) { d.open = false; }); });

  var tocLinks = $$("[data-toc]");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var map = {}; tocLinks.forEach(function (a) { map[a.getAttribute("data-toc")] = a; });
    var visible = {};
    var setActive = function (id) {
      tocLinks.forEach(function (a) { a.classList.toggle("active", a === map[id]); });
      var a = map[id];
      var bar = a && a.closest(".toc-list");
      if (a && bar && bar.scrollWidth > bar.clientWidth) {
        var left = a.offsetLeft - 20;
        if (left < bar.scrollLeft || left + a.offsetWidth > bar.scrollLeft + bar.clientWidth) bar.scrollTo({ left: left, behavior: "smooth" });
      }
    };
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { visible[e.target.id] = e.isIntersecting ? e.boundingClientRect.top : undefined; });
      var best = null, bestTop = Infinity;
      Object.keys(visible).forEach(function (id) { var t = visible[id]; if (t !== undefined && t < bestTop) { bestTop = t; best = id; } });
      if (best) setActive(best);
    }, { rootMargin: "-120px 0px -55% 0px", threshold: 0 });
    $$(".sec[id]").forEach(function (s) { io.observe(s); });
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
      var href = t.getAttribute("data-href");
      cred.innerHTML = escH(t.getAttribute("data-credit") || "") + (href ? ' — <a href="' + escH(href) + '" target="_blank" rel="noopener">source</a>' : "");
      cnt.textContent = (cur + 1) + " / " + triggers.length;
    };
    var open = function (i) { lastFocus = document.activeElement; show(i); lb.hidden = false; document.body.style.overflow = "hidden"; $(".lb-close", lb).focus(); };
    var close = function () { lb.hidden = true; document.body.style.overflow = ""; img.src = ""; if (lastFocus) lastFocus.focus(); };
    triggers.forEach(function (t, i) { t.addEventListener("click", function () { open(i); }); });
    $(".lb-close", lb).addEventListener("click", close);
    $(".lb-prev", lb).addEventListener("click", function () { show(cur - 1); });
    $(".lb-next", lb).addEventListener("click", function () { show(cur + 1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
    document.addEventListener("keydown", function (e) {
      if (lb.hidden) return;
      if (e.key === "Escape") close();
      else if (e.key === "ArrowLeft") show(cur - 1);
      else if (e.key === "ArrowRight") show(cur + 1);
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

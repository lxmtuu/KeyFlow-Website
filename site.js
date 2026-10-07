/* ==========================================================================
   Keyflow · product site behaviour
   No dependencies, no build step, no trackers.  Everything degrades:
   with scripting off the pages are still complete documents in English.

   1. helpers          5. sliders             8. release info from GitHub
   2. language         6. lightbox            9. video, copy buttons
   3. header & drawer  7. reveal & counters  10. boot
   4. dropdown
   ========================================================================== */
(function () {
  "use strict";

  var root = document.documentElement;
  var ASSET_ROOT = root.getAttribute("data-root") || "";
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!reduceMotion && "IntersectionObserver" in window) root.classList.add("motion-ready");

  /* 1. helpers ------------------------------------------------------------- */
  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }
  function on(el, ev, fn, opt) { if (el) el.addEventListener(ev, fn, opt || false); }
  function miB(bytes) { return (bytes / 1048576).toFixed(1) + " MiB"; }

  /* Icons for the bits this file injects (lightbox chrome). */
  var ICON = {
    close: '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg>',
    left: '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>',
    right: '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 18 6-6-6-6"/></svg>'
  };

  /* 2. language ------------------------------------------------------------ */
  /* English lives in the markup; the Vietnamese tables are generated into
     i18n/vi/*.js and land on window.KEYFLOW_VI.  Keys are stable across pages
     ("ui.*" for the shared chrome, "<page>.*" for page copy). */
  var vi = window.KEYFLOW_VI || {};
  var langButtons = $$(".lang button");
  var currentLang = "en";

  /* A UI string for the language on screen (English fallback), for text that is
     built in script instead of sitting in the markup. */
  function t(key, en) {
    var val = currentLang === "vi" ? vi[key] : null;
    return (val === undefined || val === null) ? en : val;
  }

  function storeLang(lang) {
    try { localStorage.setItem("keyflow-site-lang", lang); } catch (e) { /* private mode */ }
  }
  function readLang() {
    var saved = null;
    try { saved = localStorage.getItem("keyflow-site-lang"); } catch (e) { /* ignore */ }
    var query = new URLSearchParams(location.search).get("lang");
    if (query === "vi" || query === "en") return query;
    if (saved === "vi" || saved === "en") return saved;
    return ((navigator.language || "").toLowerCase().indexOf("vi") === 0) ? "vi" : "en";
  }

  function applyLang(lang) {
    var isVi = lang === "vi";
    currentLang = lang;
    root.lang = isVi ? "vi" : "en";
    root.removeAttribute("data-lang-pref");   // lift the anti-flash veil

    $$("[data-i18n]").forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      var en = el.getAttribute("data-en");
      if (en === null) { en = el.innerHTML; el.setAttribute("data-en", en); }
      var val = isVi ? vi[key] : null;
      el.innerHTML = (val === undefined || val === null) ? en : val;
    });
    $$("[data-i18n-attr]").forEach(function (el) {
      el.getAttribute("data-i18n-attr").split(";").forEach(function (pair) {
        var bits = pair.split("=");
        if (bits.length !== 2) return;
        var attr = bits[0].trim(), key = bits[1].trim();
        var en = el.getAttribute("data-en-" + attr);
        if (en === null) { en = el.getAttribute(attr) || ""; el.setAttribute("data-en-" + attr, en); }
        var val = isVi ? vi[key] : null;
        el.setAttribute(attr, (val === undefined || val === null) ? en : val);
      });
    });
    // Screenshots are rendered once per language by the app's CI.
    $$("[data-poster-shot]").forEach(function (video) {
      var posterShot = video.getAttribute("data-poster-shot");
      video.setAttribute("poster", ASSET_ROOT + "previews/" + (isVi ? "vi" : "en") + "/" + posterShot + ".png");
    });
    $$("[data-shot]").forEach(function (pic) {
      var shot = pic.getAttribute("data-shot");
      var img = pic.tagName === "IMG" ? pic : $("img", pic);
      var source = $("source", pic);
      if (source) source.setAttribute("srcset", ASSET_ROOT + "previews/webp/" + (isVi ? "vi" : "en") + "/" + shot + ".webp");
      if (img) img.setAttribute("src", ASSET_ROOT + "previews/" + (isVi ? "vi" : "en") + "/" + shot + ".png");
    });
    langButtons.forEach(function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-lang") === lang)); });
    sliders.forEach(function (slider) { slider.relabel(); });
    lightbox.relabel();
    var ogLocale = $('meta[property="og:locale"]');
    if (ogLocale) ogLocale.setAttribute("content", isVi ? "vi_VN" : "en_US");
    document.querySelectorAll(".js-date").forEach(formatDate);
    storeLang(lang);
  }

  langButtons.forEach(function (b) {
    on(b, "click", function () {
      var lang = b.getAttribute("data-lang");
      applyLang(lang);
    });
  });

  /* 3. header, progress bar, drawer --------------------------------------- */
  var nav = $(".nav");
  var progress = $(".progress");
  var totop = $(".totop");

  function onScroll() {
    var y = window.scrollY || root.scrollTop || 0;
    if (nav) nav.classList.toggle("is-stuck", y > 8);
    if (totop) totop.classList.toggle("is-on", y > 700);
    if (progress) {
      var h = document.body.scrollHeight - window.innerHeight;
      var p = h > 0 ? Math.min(1, y / h) : 0;
      progress.style.transform = "scaleX(" + p + ")";
      progress.classList.toggle("is-on", p > 0.002 && p < 0.999);
    }
  }
  on(window, "scroll", onScroll, { passive: true });
  on(window, "resize", onScroll);
  on(totop, "click", function () {
    window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" });
  });

  var drawer = $(".drawer");
  var burger = $(".burger");
  var lastFocus = null;
  function openDrawer() {
    if (!drawer) return;
    lastFocus = document.activeElement;
    drawer.classList.add("is-open");
    if (burger) burger.setAttribute("aria-expanded", "true");
    document.body.style.overflow = "hidden";
    var close = $(".drawer-close", drawer);
    if (close) close.focus();
  }
  function closeDrawer() {
    if (!drawer || !drawer.classList.contains("is-open")) return;
    drawer.classList.remove("is-open");
    if (burger) burger.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  on(burger, "click", openDrawer);
  on($(".drawer-close"), "click", closeDrawer);
  on(drawer, "click", function (e) { if (e.target === drawer) closeDrawer(); });
  on(drawer, "click", function (e) {
    var link = e.target.closest && e.target.closest("a[href]");
    if (link) closeDrawer();
  });
  on(drawer, "keydown", function (e) {
    if (e.key !== "Tab") return;
    var focusable = $$("a[href], button:not([disabled]), [tabindex]:not([tabindex='-1'])", drawer)
      .filter(function (el) { return el.getClientRects().length > 0; });
    if (!focusable.length) { e.preventDefault(); return; }
    var first = focusable[0], last = focusable[focusable.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });
  on(document, "keydown", function (e) {
    if (e.key !== "Escape") return;
    if (lightbox.isOpen()) return;   // the viewer closes itself
    if (drawer && drawer.classList.contains("is-open")) { closeDrawer(); return; }
    $$(".has-menu.is-open").forEach(function (m) {
      m.classList.remove("is-open");
      if (m.matches(":hover")) m.classList.add("is-dismissed");
      var button = $(".menu-btn", m);
      if (button) { button.setAttribute("aria-expanded", "false"); if (m.contains(document.activeElement)) button.focus(); }
    });
  });

  /* 4. features dropdown (click/touch; hover is pure CSS) ------------------ */
  $$(".has-menu").forEach(function (wrap) {
    var btn = $(".menu-btn", wrap);
    if (!btn) return;
    btn.setAttribute("aria-expanded", "false");
    on(wrap, "mouseenter", function () {
      if (!wrap.classList.contains("is-dismissed")) btn.setAttribute("aria-expanded", "true");
    });
    on(wrap, "mouseleave", function () {
      wrap.classList.remove("is-dismissed");
      if (wrap.contains(document.activeElement)) return;
      wrap.classList.remove("is-open");
      btn.setAttribute("aria-expanded", "false");
    });
    on(wrap, "focusout", function (e) {
      if (wrap.contains(e.relatedTarget)) return;
      wrap.classList.remove("is-open");
      if (wrap.matches(":hover")) wrap.classList.add("is-dismissed");
      btn.setAttribute("aria-expanded", "false");
    });
    on(btn, "click", function (e) {
      e.preventDefault();
      var open = btn.getAttribute("aria-expanded") !== "true";
      wrap.classList.toggle("is-open", open);
      wrap.classList.remove("is-dismissed");
      if (!open && wrap.matches(":hover")) wrap.classList.add("is-dismissed");
      btn.setAttribute("aria-expanded", String(open));
      $$(".has-menu").forEach(function (other) {
        if (other !== wrap) {
          other.classList.remove("is-open");
          if (other.matches(":hover")) other.classList.add("is-dismissed");
          var b = $(".menu-btn", other); if (b) b.setAttribute("aria-expanded", "false");
        }
      });
    });
  });
  on(document, "click", function (e) {
    if (e.target.closest && e.target.closest(".has-menu")) return;
    $$(".has-menu.is-open").forEach(function (m) {
      m.classList.remove("is-open");
      if (m.matches(":hover")) m.classList.add("is-dismissed");
      var b = $(".menu-btn", m); if (b) b.setAttribute("aria-expanded", "false");
    });
  });

  /* 5. sliders -------------------------------------------------------------- */
  /* Markup comes from tools/sitekit.py (render_slider).  One picture shows at a
     time; the picker, the arrows, the keys and a swipe change it.  Where a page
     asks for a slideshow it follows the WAI-ARIA carousel pattern: the pause
     button is the first Tab stop, rotation holds while the pointer is over the
     region and stops for good once keyboard focus enters it, it only runs while
     the region is on screen, and it never starts for visitors who prefer reduced
     motion. */
  var sliders = [];

  function pad2(n) { return (n < 10 ? "0" : "") + n; }
  function fmt(tpl, n, total) { return tpl.replace("{n}", n).replace("{total}", total); }

  function createSlider(box) {
    var viewport = $(".slider-viewport", box);
    var slides = $$(".slide", box);
    if (!viewport || slides.length < 2) return null;

    var list = $(".slides", box);
    var picker = $(".slider-nav", box);
    var pickers = $$("button", picker);
    var play = $(".slider-play", box);
    var counter = $(".slider-count b", box);
    var interval = parseInt(box.getAttribute("data-interval"), 10) || 6000;
    var oneShot = box.hasAttribute("data-stop-on-interact");   // any use of the controls ends the slideshow
    var index = 0;
    var playing = box.getAttribute("data-autoplay") === "on" && !reduceMotion;
    var hovering = false, visible = false, viewing = false, dragging = false;
    var elapsed = 0, stamp = 0, raf = 0;

    function running() { return playing && visible && !hovering && !viewing && !dragging && !document.hidden; }
    function paint(p) { box.style.setProperty("--p", p.toFixed(3)); }
    function halt() { if (raf) cancelAnimationFrame(raf); raf = 0; stamp = 0; }
    function schedule() { if (!raf && running()) raf = requestAnimationFrame(tick); }
    function tick(now) {
      raf = 0;
      if (!running()) { stamp = 0; return; }
      if (stamp) elapsed += now - stamp;   // time only counts while it is running
      stamp = now;
      if (elapsed >= interval) { go(index + 1, { dir: 1 }); return; }
      paint(elapsed / interval);
      schedule();
    }

    function centre() {
      if (!picker || picker.scrollWidth <= picker.clientWidth + 2) return;
      var b = pickers[index];
      picker.scrollTo({ left: Math.max(0, b.offsetLeft - (picker.clientWidth - b.offsetWidth) / 2), behavior: reduceMotion ? "auto" : "smooth" });
    }

    function show() {
      var hadFocus = slides.some(function (s) { return s.contains(document.activeElement); });
      slides.forEach(function (slide, i) {
        var current = i === index;
        slide.classList.toggle("is-active", current);
        slide.setAttribute("aria-hidden", current ? "false" : "true");
        if ("inert" in slide) slide.inert = !current;
        var trigger = $(".lb-trigger", slide);
        if (trigger) trigger.tabIndex = current ? 0 : -1;
      });
      pickers.forEach(function (b, i) {
        b.classList.toggle("is-current", i === index);
        b.classList.toggle("is-done", i < index);
        if (i === index) b.setAttribute("aria-current", "true"); else b.removeAttribute("aria-current");
      });
      if (counter) counter.textContent = pad2(index + 1);
      if (hadFocus) {   // keep the keyboard where it was instead of dropping it on <body>
        var t2 = $(".lb-trigger", slides[index]);
        if (t2) t2.focus({ preventScroll: true });
      }
      centre();
    }

    function go(n, opts) {
      opts = opts || {};
      var total = slides.length;
      var target = ((n % total) + total) % total;
      if (target !== index) {
        var dir = opts.dir || (target > index ? 1 : -1);
        box.setAttribute("data-dir", dir > 0 ? "next" : "prev");
        index = target;
        show();
      }
      elapsed = 0; stamp = 0; paint(0);
      if (opts.user && oneShot) setPlaying(false);
      schedule();
    }

    function relabelPlay() {
      if (!play) return;
      var label = playing ? t("ui.car.pause", "Pause slideshow") : t("ui.car.play", "Play slideshow");
      play.setAttribute("aria-label", label);
      play.title = label;
      var shown = $(".slider-play-label", play);
      if (shown) shown.textContent = label;
    }
    function setPlaying(on_) {
      playing = on_;
      box.classList.toggle("is-playing", on_);
      if (list) list.setAttribute("aria-live", on_ ? "off" : "polite");   // never announce while it rotates
      relabelPlay();
      if (on_) schedule(); else halt();
    }
    function relabel() {
      var total = slides.length, tpl = t("ui.car.n", "Picture {n} of {total}");
      slides.forEach(function (s, i) { s.setAttribute("aria-label", fmt(tpl, i + 1, total)); });
      if (box.classList.contains("slider-spotlight")) {
        pickers.forEach(function (b, i) { b.setAttribute("aria-label", fmt(tpl, i + 1, total)); });
      }
      relabelPlay();
    }

    /* controls */
    on($(".slider-btn.prev", box), "click", function () { go(index - 1, { dir: -1, user: true }); });
    on($(".slider-btn.next", box), "click", function () { go(index + 1, { dir: 1, user: true }); });
    pickers.forEach(function (b, i) { on(b, "click", function () { go(i, { user: true }); }); });
    on(play, "click", function () { setPlaying(!playing); });

    on(box, "keydown", function (e) {
      if (e.altKey || e.ctrlKey || e.metaKey || e.shiftKey) return;
      var inPicker = !!picker && picker.contains(e.target);
      var vertical = inPicker && box.classList.contains("slider-tabs");
      var to = null, dir = 0;
      if (e.key === "ArrowRight" || (vertical && e.key === "ArrowDown")) { to = index + 1; dir = 1; }
      else if (e.key === "ArrowLeft" || (vertical && e.key === "ArrowUp")) { to = index - 1; dir = -1; }
      else if (inPicker && e.key === "Home") to = 0;
      else if (inPicker && e.key === "End") to = slides.length - 1;
      if (to === null) return;
      e.preventDefault();
      go(to, { dir: dir || undefined, user: true });
      if (inPicker) pickers[index].focus();
    });

    /* hold still while the pointer is over it, or a key has focus */
    on(box, "pointerenter", function (e) { if (e.pointerType === "mouse") { hovering = true; halt(); } });
    on(box, "pointerleave", function (e) { if (e.pointerType === "mouse") { hovering = false; schedule(); } });
    on(box, "focusin", function (e) {
      var byKeyboard = false;
      try { byKeyboard = e.target.matches(":focus-visible"); } catch (err) { /* very old browsers */ }
      if (byKeyboard && playing) setPlaying(false);
    });

    /* swipe (touch, pen and mouse drag); a drag must not count as a click */
    var sx = 0, sy = 0, down = false, moved = false;
    on(viewport, "pointerdown", function (e) {
      if (e.pointerType === "mouse" && e.button !== 0) return;
      down = true; moved = false; sx = e.clientX; sy = e.clientY;
    });
    on(viewport, "pointermove", function (e) {
      if (!down || moved) return;
      var dx = e.clientX - sx, dy = e.clientY - sy;
      if (Math.abs(dx) > 12 && Math.abs(dx) > Math.abs(dy) * 1.4) {
        moved = true; dragging = true; halt();
        try { viewport.setPointerCapture(e.pointerId); } catch (err) { /* ignore */ }
      }
    });
    function release(e) {
      if (!down) return;
      down = false; dragging = false;
      var dx = e.clientX - sx;
      if (moved && Math.abs(dx) > 40) { var dir = dx < 0 ? 1 : -1; go(index + dir, { dir: dir, user: true }); }
      else schedule();
    }
    on(viewport, "pointerup", release);
    on(viewport, "pointercancel", function () { down = false; dragging = false; schedule(); });
    on(viewport, "click", function (e) {
      if (moved) { e.preventDefault(); e.stopPropagation(); moved = false; }
    }, true);

    /* only rotate while it is on screen, in a visible tab, with no viewer open */
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        visible = entries[entries.length - 1].isIntersecting;
        if (visible) schedule(); else halt();
      }, { threshold: 0.4 }).observe(box);
    } else {
      visible = true;
    }
    on(document, "visibilitychange", function () { if (document.hidden) halt(); else schedule(); });
    on(document, "keyflow:lightbox", function (e) {
      var d = e.detail || {};
      viewing = !!d.open;
      if (viewing) { halt(); return; }
      if (d.host === box && typeof d.index === "number") go(d.index); else schedule();
    });

    box.classList.add("is-ready");
    show();
    relabel();
    setPlaying(playing);
    paint(0);
    return { box: box, go: go, relabel: relabel };
  }

  $$("[data-slider]").forEach(function (box) {
    var s = createSlider(box);
    if (s) sliders.push(s);
  });

  /* 6. lightbox ------------------------------------------------------------- */
  /* One viewer for the whole page.  Every [data-lightbox] host is its own group
     and its pictures are read when the viewer opens, so the language that is on
     screen right now decides which screenshot and which caption appear. */
  var lightbox = (function () {
    var el = null, img, cap, count, btnClose, btnPrev, btnNext;
    var items = [], n = 0, host = null, opener = null, opened = false;
    var px = 0, py = 0, tracking = false;

    function relabel() {
      if (!el) return;
      el.setAttribute("aria-label", t("ui.lb.label", "Image viewer"));
      btnClose.setAttribute("aria-label", t("ui.close", "Close"));
      btnPrev.setAttribute("aria-label", t("ui.car.prev", "Previous picture"));
      btnNext.setAttribute("aria-label", t("ui.car.next", "Next picture"));
    }

    function build() {
      el = document.createElement("div");
      el.className = "lightbox";
      el.setAttribute("role", "dialog");
      el.setAttribute("aria-modal", "true");
      el.innerHTML =
        '<button type="button" class="lb-btn lb-close">' + ICON.close + "</button>" +
        '<button type="button" class="lb-btn lb-prev">' + ICON.left + "</button>" +
        '<figure class="lb-figure"><img alt=""><figcaption class="lb-cap"></figcaption><div class="lb-count"></div></figure>' +
        '<button type="button" class="lb-btn lb-next">' + ICON.right + "</button>";
      document.body.appendChild(el);
      img = $(".lb-figure img", el); cap = $(".lb-cap", el); count = $(".lb-count", el);
      btnClose = $(".lb-close", el); btnPrev = $(".lb-prev", el); btnNext = $(".lb-next", el);
      on(btnClose, "click", close);
      on(btnPrev, "click", function () { show(n - 1); });
      on(btnNext, "click", function () { show(n + 1); });
      on(el, "click", function (e) { if (e.target === el || e.target === $(".lb-figure", el)) close(); });
      on(el, "pointerdown", function (e) { tracking = true; px = e.clientX; py = e.clientY; });
      on(el, "pointerup", function (e) {
        if (!tracking) return;
        tracking = false;
        var dx = e.clientX - px, dy = e.clientY - py;
        if (items.length > 1 && Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) show(n + (dx < 0 ? 1 : -1));
      });
    }

    /* the host may itself be the only item (a lone screenshot) */
    function collect(h) {
      var found = $$("[data-lb-item]", h);
      if (h.hasAttribute("data-lb-item")) found.unshift(h);
      return found.map(function (item) {
        var im = $("img", item);
        var c = $(".lb-caption", item) || $("figcaption", item);
        return { el: item, src: im ? (im.currentSrc || im.src) : "", alt: im ? im.alt : "", cap: c ? c.textContent.trim() : "" };
      });
    }

    function show(i) {
      n = (i + items.length) % items.length;
      img.src = items[n].src;
      img.alt = items[n].alt;
      cap.textContent = items[n].cap;
      cap.hidden = !items[n].cap;
      count.textContent = items.length > 1 ? (n + 1) + " / " + items.length : "";
    }

    function open(i, h, from) {
      if (!el) build();
      host = h;
      items = collect(h);
      if (!items.length) return;
      opener = from || document.activeElement;
      relabel();
      el.classList.toggle("is-single", items.length < 2);
      show(i);
      el.classList.add("is-open");
      opened = true;
      document.body.style.overflow = "hidden";
      btnClose.focus();
      document.dispatchEvent(new CustomEvent("keyflow:lightbox", { detail: { open: true, host: host, index: n } }));
    }

    function close() {
      if (!opened) return;
      opened = false;
      el.classList.remove("is-open");
      document.body.style.overflow = "";
      document.dispatchEvent(new CustomEvent("keyflow:lightbox", { detail: { open: false, host: host, index: n } }));
      /* a slider follows the picture last viewed, so the opener may now be on an inert slide */
      var back = (opener && !opener.closest("[inert]")) ? opener : (host && $(".slide.is-active .lb-trigger", host));
      if (back && back.focus) back.focus({ preventScroll: true });
    }

    on(document, "click", function (e) {
      var trigger = e.target.closest ? e.target.closest(".lb-trigger") : null;
      if (!trigger) return;
      var group = trigger.closest("[data-lightbox]");
      var item = trigger.closest("[data-lb-item]");
      if (!group || !item) return;
      e.preventDefault();
      var all = collect(group);
      var at = 0;
      all.forEach(function (entry, k) { if (entry.el === item) at = k; });
      open(at, group, trigger);
    });

    on(document, "keydown", function (e) {
      if (!opened) return;
      if (e.key === "Escape") { e.preventDefault(); close(); }
      else if (e.key === "ArrowRight") { e.preventDefault(); show(n + 1); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); show(n - 1); }
      else if (e.key === "Tab") {
        var f = $$(".lb-btn", el).filter(function (b) { return b.offsetParent !== null; });
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });

    return { open: open, close: close, relabel: relabel, isOpen: function () { return opened; } };
  })();

  /* 7. reveal on scroll + counters ---------------------------------------- */
  (function () {
    var targets = $$(".reveal");
    if (!targets.length) return;
    if (reduceMotion || !("IntersectionObserver" in window)) {
      targets.forEach(function (t) { t.classList.add("is-in"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-in");
        io.unobserve(entry.target);
        var counter = entry.target.matches("[data-count]") ? entry.target : $("[data-count]", entry.target);
        if (counter) countUp(counter);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    targets.forEach(function (t) { io.observe(t); });
  })();

  function countUp(el) {
    var target = parseFloat(el.getAttribute("data-count"));
    if (isNaN(target)) return;
    var suffix = el.getAttribute("data-count-suffix") || "";
    var dur = 900, t0 = null;
    function frame(ts) {
      if (!t0) t0 = ts;
      var p = Math.min(1, (ts - t0) / dur);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased) + suffix;
      if (p < 1) requestAnimationFrame(frame);
    }
    if (reduceMotion) { el.textContent = target + suffix; return; }
    requestAnimationFrame(frame);
  }
  $$("[data-count]").forEach(function (el) {
    // Counters above the fold never meet the observer's threshold change.
    var r = el.getBoundingClientRect();
    if (r.top < window.innerHeight && r.bottom > 0) countUp(el);
  });

  /* 8. release info straight from GitHub ---------------------------------- */
  /* The links in the markup are pinned to v1.0.0 so the page works offline;
     when the API answers they move to the newest release by themselves. */
  (function () {
    var nodes = $$("[data-asset], [data-release-tag], [data-release-date], [data-release-size]");
    if (!nodes.length || !window.fetch) return;
    var PATTERNS = {
      setup: /^Keyflow-Setup-.*\.exe$/i,
      portable: /^Keyflow-[\d.]+-win-x64\.zip$/i,
      fd: /^Keyflow-.*-win-x64-fd\.zip$/i,
      arm64: /^Keyflow-.*-win-arm64\.zip$/i,
      sums: /^SHA256SUMS\.txt$/i
    };
    fetch("https://api.github.com/repos/lxmtuu/KeyFlow/releases/latest", { headers: { Accept: "application/vnd.github+json" } })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (rel) {
        if (!rel || !rel.assets) return;
        var byKind = {};
        rel.assets.forEach(function (a) {
          Object.keys(PATTERNS).forEach(function (kind) {
            if (PATTERNS[kind].test(a.name)) byKind[kind] = a;
          });
        });
        $$("[data-asset]").forEach(function (el) {
          var asset = byKind[el.getAttribute("data-asset")];
          if (asset) el.href = asset.browser_download_url;
        });
        $$("[data-release-size]").forEach(function (el) {
          var asset = byKind[el.getAttribute("data-release-size")];
          if (asset) el.textContent = miB(asset.size);
        });
        $$("[data-release-tag]").forEach(function (el) { el.textContent = rel.tag_name || el.textContent; });
        $$("[data-release-name]").forEach(function (el) { el.textContent = rel.name || el.textContent; });
        $$("[data-release-date]").forEach(function (el) {
          el.setAttribute("data-date", rel.published_at || "");
          formatDate(el);
        });
      })
      .catch(function () { /* offline or rate-limited: the pinned links still work */ });
  })();

  function formatDate(el) {
    var iso = el.getAttribute("data-date");
    if (!iso) return;
    var d = new Date(iso);
    if (isNaN(d.getTime())) return;
    try {
      el.textContent = d.toLocaleDateString(currentLang === "vi" ? "vi-VN" : "en-GB", { year: "numeric", month: "short", day: "numeric" });
    } catch (e) { el.textContent = iso.slice(0, 10); }
  }

  /* 9. video gating + copy buttons + footer year -------------------------- */
  (function () {
    var video = $(".hero-media video");
    if (video) {
      var wide = window.matchMedia && window.matchMedia("(min-width: 940px)").matches;
      if (reduceMotion || !wide) {
        video.removeAttribute("autoplay");
        video.setAttribute("preload", "none");
        video.pause && video.pause();
      }
      // The showcase has no dialogue: keep it muted, but let people turn sound on.
      video.setAttribute("muted", "");
      video.muted = true;
    }
  })();

  $$(".copy-btn").forEach(function (btn) {
    on(btn, "click", function () {
      var target = document.getElementById(btn.getAttribute("data-copy"));
      if (!target) return;
      var text = target.innerText;
      var done = function () {
        var old = btn.textContent;
        btn.textContent = btn.getAttribute("data-copied") || "✓";
        setTimeout(function () { btn.textContent = old; }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, function () {});
      } else {
        var ta = document.createElement("textarea");
        ta.value = text; document.body.appendChild(ta); ta.select();
        try { document.execCommand("copy"); done(); } catch (e) { /* ignore */ }
        document.body.removeChild(ta);
      }
    });
  });

  $$(".js-year").forEach(function (el) { el.textContent = String(new Date().getFullYear()); });

  /* 10. boot --------------------------------------------------------------- */
  var wanted = readLang();
  applyLang(wanted);
  onScroll();
})();

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

  /* A string from the shared UI table in the active language (English fallback). */
  function tr(key, en) {
    var val = currentLang === "vi" ? vi[key] : null;
    return (val === undefined || val === null) ? en : val;
  }
  function fmt(tpl, map) {
    return tpl.replace(/\{(\w+)\}/g, function (m, k) { return map[k] === undefined ? m : map[k]; });
  }

  /* 2. language ------------------------------------------------------------ */
  /* English lives in the markup; the Vietnamese tables are generated into
     i18n/vi/*.js and land on window.KEYFLOW_VI.  Keys are stable across pages
     ("ui.*" for the shared chrome, "<page>.*" for page copy). */
  var vi = window.KEYFLOW_VI || {};
  var langButtons = $$(".lang button");
  var currentLang = "en";

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
    sliders.forEach(function (sl) { sl.relabel(); });
    var ogLocale = $('meta[property="og:locale"]');
    if (ogLocale) ogLocale.setAttribute("content", isVi ? "vi_VN" : "en_US");
    document.querySelectorAll(".js-date").forEach(formatDate);
    storeLang(lang);
  }

  langButtons.forEach(function (b) {
    on(b, "click", function () {
      applyLang(b.getAttribute("data-lang"));
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
    if (lightbox && lightbox.isOpen()) { lightbox.close(); return; }
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

  /* 5. sliders ------------------------------------------------------------- */
  /* Markup comes from tools/sitekit.py (render_slider).  Without this script
     every slide is listed one after another; with it the slides stack, the
     arrows, the pause button and the optional auto-advance come alive.
     Auto-advance is paused for as long as the pointer is over a slider, a
     keyboard user is inside it, the tab is hidden, the slider is off screen or
     the lightbox is open - and it is off altogether for visitors who ask their
     system for reduced motion. */
  var sliders = [];

  function pad2(n) { return n < 10 ? "0" + n : String(n); }

  function Slider(box) {
    var list = $(".slides", box);
    var slides = $$(".slide", box);
    var count = slides.length;
    if (!list || count < 2) return null;
    var viewport = $(".slider-viewport", box);
    var playBtn = $(".slider-play", box);
    var navBtns = $$(".slider-nav button", box);
    var curEl = $("[data-count-cur]", box);
    var bar = $(".slider-bar b", box);
    var interval = parseInt(box.getAttribute("data-interval"), 10) || 6000;
    var playing = box.getAttribute("data-autoplay") === "on" && !reduceMotion;
    var stopOnInteract = box.hasAttribute("data-stop-on-interact");
    var index = 0, elapsed = 0, last = 0, raf = 0, ignoreFocus = false, swallow = false;
    var holds = {};
    var self = {};

    /* The arrows and the progress line are placed against the picture, not the
       whole slide (the caption would push them off-centre), so the picture's
       height is measured into --pic-h and kept current. */
    var frame = $(".frame", slides[0]);
    function measure() {
      if (frame && frame.offsetHeight) box.style.setProperty("--pic-h", frame.offsetHeight + "px");
    }
    measure();
    if (frame && "ResizeObserver" in window) new ResizeObserver(measure).observe(frame);
    else on(window, "resize", measure);

    function held() { return Object.keys(holds).some(function (k) { return holds[k]; }); }
    function setBar(p) { if (bar) bar.style.transform = "scaleX(" + p + ")"; }

    function render() {
      slides.forEach(function (sl, i) {
        var on = i === index;
        sl.classList.toggle("is-active", on);
        sl.setAttribute("aria-hidden", on ? "false" : "true");
        if ("inert" in sl) sl.inert = !on;
      });
      navBtns.forEach(function (btn, i) {
        if (i === index) btn.setAttribute("aria-current", "true"); else btn.removeAttribute("aria-current");
        btn.classList.toggle("is-done", i < index);
      });
      if (curEl) curEl.textContent = pad2(index + 1);
      keepNavInView();
    }

    /* When the page list is a row of chips that scrolls sideways (small
       screens), keep the chosen one in the middle without moving the page. */
    function keepNavInView() {
      var cur = navBtns[index], nav = cur && cur.parentNode;
      if (!nav || nav.scrollWidth <= nav.clientWidth + 1) return;
      var left = cur.offsetLeft - (nav.clientWidth - cur.offsetWidth) / 2;
      if (nav.scrollTo) nav.scrollTo({ left: left, behavior: reduceMotion ? "auto" : "smooth" });
      else nav.scrollLeft = left;
    }

    function go(n, opts) {
      opts = opts || {};
      var next = ((n % count) + count) % count;
      if (next === index) return;
      var from = index;
      box.style.setProperty("--dir", opts.dir || (n >= index ? 1 : -1));
      slides[from].classList.add("is-leaving");
      setTimeout(function () { slides[from].classList.remove("is-leaving"); }, 800);
      index = next;
      elapsed = 0;
      setBar(0);
      render();
    }

    /* The clock: one rAF loop that only runs while the slider is playing and
       nothing is holding it, so a hover freezes the bar and resumes from the
       same spot instead of restarting. */
    function tick(ts) {
      raf = 0;
      if (!playing || held()) { last = 0; return; }
      if (!last) last = ts;
      elapsed += ts - last;
      last = ts;
      if (elapsed >= interval) go(index + 1, { dir: 1 });
      setBar(Math.min(1, elapsed / interval));
      raf = requestAnimationFrame(tick);
    }
    function sync() {
      box.classList.toggle("is-playing", playing);
      box.classList.toggle("is-held", playing && held());
      list.setAttribute("aria-live", playing ? "off" : "polite");
      if (playBtn) {
        playBtn.setAttribute("aria-label", playing ? tr("ui.car.pause", "Pause slideshow") : tr("ui.car.play", "Play slideshow"));
      }
      if (playing && !held() && !raf) { last = 0; raf = requestAnimationFrame(tick); }
      if (!playing) setBar(0);
    }
    function hold(reason, on) { holds[reason] = !!on; sync(); }
    function interact() {
      elapsed = 0;
      setBar(0);
      if (stopOnInteract && playing) playing = false;
      sync();
    }

    function relabel() {
      var tpl = tr("ui.car.n", "Picture {n} of {total}");
      navBtns.forEach(function (btn, i) {
        if (btn.hasAttribute("data-dynamic-label")) btn.setAttribute("aria-label", fmt(tpl, { n: i + 1, total: count }));
      });
      sync();
    }

    /* controls */
    on($(".slider-btn.prev", box), "click", function () { interact(); go(index - 1, { dir: -1 }); });
    on($(".slider-btn.next", box), "click", function () { interact(); go(index + 1, { dir: 1 }); });
    navBtns.forEach(function (btn, i) {
      on(btn, "click", function () { interact(); go(i); });
    });
    on(playBtn, "click", function () {
      playing = !playing;
      if (playing) { holds.focus = false; ignoreFocus = true; }
      elapsed = playing ? 0 : elapsed;
      sync();
    });
    on(box, "keydown", function (e) {
      var k = e.key;
      if (k === "ArrowRight") { e.preventDefault(); interact(); go(index + 1, { dir: 1 }); }
      else if (k === "ArrowLeft") { e.preventDefault(); interact(); go(index - 1, { dir: -1 }); }
      else if (k === "Home") { e.preventDefault(); interact(); go(0, { dir: -1 }); }
      else if (k === "End") { e.preventDefault(); interact(); go(count - 1, { dir: 1 }); }
    });

    /* holds */
    on(box, "pointerenter", function (e) { if (e.pointerType === "mouse") hold("hover", true); });
    on(box, "pointerleave", function () { hold("hover", false); });
    on(box, "focusin", function (e) {
      var kb = false;
      try { kb = e.target.matches(":focus-visible"); } catch (err) { kb = false; }
      if (kb && !ignoreFocus) hold("focus", true);
    });
    on(box, "focusout", function (e) {
      if (box.contains(e.relatedTarget)) return;
      ignoreFocus = false;
      hold("focus", false);
    });
    on(document, "visibilitychange", function () { hold("hidden", document.hidden); });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        hold("offscreen", !entries[0].isIntersecting);
      }, { threshold: 0.2 }).observe(box);
    }

    /* swipe: vertical scrolling stays native (touch-action: pan-y in the CSS) */
    if (viewport) {
      var sx = 0, sy = 0, down = false;
      on(viewport, "pointerdown", function (e) {
        if (e.pointerType === "mouse" && e.button !== 0) return;
        down = true; sx = e.clientX; sy = e.clientY;
      });
      on(viewport, "pointerup", function (e) {
        if (!down) return;
        down = false;
        var dx = e.clientX - sx, dy = e.clientY - sy;
        if (Math.abs(dx) > 44 && Math.abs(dx) > Math.abs(dy) * 1.4) {
          interact();
          go(index + (dx < 0 ? 1 : -1), { dir: dx < 0 ? 1 : -1 });
          swallow = true;                          // do not also open the lightbox
          setTimeout(function () { swallow = false; }, 350);
        }
      });
      on(viewport, "pointercancel", function () { down = false; });
      on(viewport, "dragstart", function (e) { e.preventDefault(); });
      on(viewport, "click", function (e) {
        if (swallow) { e.stopPropagation(); e.preventDefault(); swallow = false; }
      }, true);
    }

    self.box = box;
    self.go = go;
    self.hold = hold;
    self.relabel = relabel;
    self.focusActive = function () {
      var fig = $("[data-lb-item]", slides[index]);
      if (fig && fig.focus) fig.focus();
    };
    box.classList.add("is-ready");
    render();
    relabel();
    box._slider = self;
    return self;
  }
  $$("[data-slider]").forEach(function (box) {
    var sl = Slider(box);
    if (sl) sliders.push(sl);
  });

  /* 6. lightbox ------------------------------------------------------------ */
  /* One viewer for every group of pictures on the page.  What it shows is read
     from the page at the moment it opens, so it always matches the language
     the screenshots and captions are currently in. */
  var lightbox = null;
  (function () {
    var hosts = $$("[data-lightbox]");
    if (!hosts.length) return;
    var el, img, cap, counter, btnClose, btnPrev, btnNext;
    var group = [], n = 0, opener = null, activeHost = null, sx = 0;

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
      img = $(".lb-figure img", el); cap = $(".lb-cap", el); counter = $(".lb-count", el);
      btnClose = $(".lb-close", el); btnPrev = $(".lb-prev", el); btnNext = $(".lb-next", el);
      on(btnClose, "click", close);
      on(btnPrev, "click", function () { show(n - 1); });
      on(btnNext, "click", function () { show(n + 1); });
      on(el, "click", function (e) { if (e.target === el) close(); });
      on(el, "pointerdown", function (e) { sx = e.clientX; });
      on(el, "pointerup", function (e) {
        var dx = e.clientX - sx;
        if (e.pointerType !== "mouse" && Math.abs(dx) > 50) show(n + (dx < 0 ? 1 : -1));
      });
      on(document, "keydown", function (e) {
        if (!el.classList.contains("is-open")) return;
        if (e.key === "Escape") { e.preventDefault(); close(); }
        else if (e.key === "ArrowRight") { e.preventDefault(); show(n + 1); }
        else if (e.key === "ArrowLeft") { e.preventDefault(); show(n - 1); }
        else if (e.key === "Tab") {
          var f = $$(".lb-btn", el), first = f[0], last = f[f.length - 1];
          if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
          else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
        }
      });
    }
    function relabelChrome() {
      el.setAttribute("aria-label", tr("ui.lb.label", "Image viewer"));
      btnClose.setAttribute("aria-label", tr("ui.close", "Close"));
      btnPrev.setAttribute("aria-label", tr("ui.car.prev", "Previous picture"));
      btnNext.setAttribute("aria-label", tr("ui.car.next", "Next picture"));
    }
    function read(item) {
      var im = $("img", item);
      var c = $(".lb-caption", item) || $("figcaption", item);
      return {
        src: im ? (im.getAttribute("data-full") || im.currentSrc || im.src) : "",
        alt: im ? im.alt : "",
        cap: c ? c.textContent.trim() : ""
      };
    }
    function show(i) {
      n = (i + group.length) % group.length;
      var d = read(group[n]);
      img.src = d.src;
      img.alt = d.alt;
      cap.textContent = d.cap;
      counter.textContent = (n + 1) + " / " + group.length;
    }
    function open(host, i, from) {
      if (!el) build();
      activeHost = host;
      group = $$("[data-lb-item]", host);
      opener = from || document.activeElement;
      relabelChrome();
      show(i);
      el.classList.add("is-open");
      document.body.style.overflow = "hidden";
      sliders.forEach(function (sl) { sl.hold("lightbox", true); });
      btnClose.focus();
    }
    function close() {
      if (!el || !el.classList.contains("is-open")) return;
      el.classList.remove("is-open");
      document.body.style.overflow = "";
      sliders.forEach(function (sl) { sl.hold("lightbox", false); });
      if (activeHost && activeHost._slider) {          // land the slider on the picture last viewed
        activeHost._slider.go(n);
        activeHost._slider.focusActive();
      } else if (opener && opener.focus) {
        opener.focus();
      }
    }

    hosts.forEach(function (host) {
      $$("[data-lb-item]", host).forEach(function (item) {
        function go() { open(host, $$("[data-lb-item]", host).indexOf(item), item); }
        item.setAttribute("tabindex", "0");
        item.setAttribute("role", "button");
        on(item, "click", function (e) {
          if (e.target.closest("a[href]:not([data-lb-open])")) return;
          e.preventDefault();
          go();
        });
        on(item, "keydown", function (e) {
          if (e.key === "Enter" || e.key === " ") { e.preventDefault(); go(); }
        });
      });
    });
    lightbox = { open: open, close: close, isOpen: function () { return !!el && el.classList.contains("is-open"); } };
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

/* ==========================================================================
   Keyflow · product site behaviour
   No dependencies, no build step, no trackers.  Everything degrades:
   with scripting off the pages are still complete documents in English.

   1. helpers          5. carousel            8. release info from GitHub
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
    $$(".dots button").forEach(function (b, i) { b.setAttribute("aria-label", (isVi ? "Ảnh " : "Picture ") + (i + 1)); });
    var lbDialog = $(".lightbox");
    if (lbDialog) {
      lbDialog.setAttribute("aria-label", isVi ? "Trình xem ảnh" : "Image viewer");
      var lbClose = $(".lb-close", lbDialog), lbPrev = $(".lb-prev", lbDialog), lbNext = $(".lb-next", lbDialog);
      if (lbClose) lbClose.setAttribute("aria-label", isVi ? "Đóng" : "Close");
      if (lbPrev) lbPrev.setAttribute("aria-label", isVi ? "Ảnh trước" : "Previous picture");
      if (lbNext) lbNext.setAttribute("aria-label", isVi ? "Ảnh tiếp theo" : "Next picture");
    }
    var ogLocale = $('meta[property="og:locale"]');
    if (ogLocale) ogLocale.setAttribute("content", isVi ? "vi_VN" : "en_US");
    document.querySelectorAll(".js-date").forEach(formatDate);
    storeLang(lang);
  }

  langButtons.forEach(function (b) {
    on(b, "click", function () {
      var lang = b.getAttribute("data-lang");
      applyLang(lang);
      if (carousel) carousel.refresh();
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

  /* 5. carousel ------------------------------------------------------------ */
  var carousel = null;
  (function () {
    var box = $(".carousel");
    if (!box) return;
    var track = $(".track", box);
    var slides = track ? track.children : [];
    var dots = $(".dots", box);
    var index = 0;

    if (!track || !slides.length) return;
    if (dots) {
      dots.innerHTML = "";
      for (var i = 0; i < slides.length; i++) {
        var d = document.createElement("button");
        d.type = "button";
        d.setAttribute("aria-pressed", String(i === 0));
        d.setAttribute("aria-label", "Picture " + (i + 1));
        (function (n) { on(d, "click", function () { go(n); }); })(i);
        dots.appendChild(d);
      }
    }
    function go(n) {
      index = (n + slides.length) % slides.length;
      track.scrollTo({ left: slides[index].offsetLeft - track.offsetLeft, behavior: reduceMotion ? "auto" : "smooth" });
      mark();
    }
    function mark() {
      if (!track.clientWidth) return;
      index = Math.max(0, Math.min(slides.length - 1, Math.round(track.scrollLeft / track.clientWidth)));
      if (dots) $$("button", dots).forEach(function (b, n) { b.setAttribute("aria-pressed", String(n === index)); });
      $$(".slide", track).forEach(function (s, n) { s.setAttribute("aria-label", (n + 1) + " / " + slides.length); });
    }
    on(track, "scroll", function () {
      if (!track.clientWidth) return;
      index = Math.max(0, Math.min(slides.length - 1, Math.round(track.scrollLeft / track.clientWidth)));
      if (dots) $$("button", dots).forEach(function (b, n) { b.setAttribute("aria-pressed", String(n === index)); });
    }, { passive: true });
    on($(".car-btn.prev", box), "click", function () { go(index - 1); });
    on($(".car-btn.next", box), "click", function () { go(index + 1); });
    on(track, "keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); go(index + 1); }
      if (e.key === "ArrowLeft") { e.preventDefault(); go(index - 1); }
    });
    on(window, "resize", function () {
      track.scrollTo({ left: slides[index].offsetLeft - track.offsetLeft, behavior: "auto" });
      mark();
    });
    carousel = { go: go, refresh: mark };
    mark();
  })();

  /* 6. lightbox ------------------------------------------------------------ */
  var lightbox = null;
  (function () {
    var host = $("[data-lightbox]");
    if (!host) return;
    var items = $$("[data-lb-item]", host).map(function (el) {
      var img = $("img", el) || el;
      var cap = $(".lb-caption", el) || $("figcaption", el);
      return { src: img.getAttribute("data-full") || img.currentSrc || img.src, alt: img.alt || "", cap: cap ? cap.textContent.trim() : "" };
    });
    if (!items.length) return;

    var el = document.createElement("div");
    el.className = "lightbox";
    el.setAttribute("role", "dialog");
    el.setAttribute("aria-modal", "true");
    el.setAttribute("aria-label", currentLang === "vi" ? "Trình xem ảnh" : "Image viewer");
    el.innerHTML =
      '<button type="button" class="lb-btn lb-close" aria-label="Close">' + ICON.close + "</button>" +
      '<button type="button" class="lb-btn lb-prev" aria-label="Previous">' + ICON.left + "</button>" +
      '<figure class="lb-figure"><img alt=""><figcaption class="lb-cap"></figcaption><div class="lb-count"></div></figure>' +
      '<button type="button" class="lb-btn lb-next" aria-label="Next">' + ICON.right + "</button>";
    document.body.appendChild(el);

    var img = $(".lb-figure img", el), cap = $(".lb-cap", el), count = $(".lb-count", el), n = 0, opener = null;
    function show(i) {
      n = (i + items.length) % items.length;
      img.src = items[n].src;
      img.alt = items[n].alt;
      cap.textContent = items[n].cap;
      count.textContent = (n + 1) + " / " + items.length;
    }
    function open(i, from) {
      opener = from || document.activeElement;
      show(i);
      el.classList.add("is-open");
      document.body.style.overflow = "hidden";
      $(".lb-close", el).focus();
    }
    function close() {
      el.classList.remove("is-open");
      document.body.style.overflow = "";
      if (opener && opener.focus) opener.focus();
    }
    on($(".lb-close", el), "click", close);
    on($(".lb-prev", el), "click", function () { show(n - 1); });
    on($(".lb-next", el), "click", function () { show(n + 1); });
    on(el, "click", function (e) { if (e.target === el) close(); });
    on(document, "keydown", function (e) {
      if (!el.classList.contains("is-open")) return;
      if (e.key === "Escape") { e.preventDefault(); close(); }
      if (e.key === "Tab") {
        var f = $$(".lb-btn", el), first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
      if (e.key === "ArrowRight") { e.preventDefault(); show(n + 1); }
      if (e.key === "ArrowLeft") { e.preventDefault(); show(n - 1); }
    });
    $$("[data-lb-item]", host).forEach(function (item, i) {
      on(item, "click", function (e) {
        if (e.target.closest("a[href]:not([data-lb-open])")) return;
        e.preventDefault();
        open(i, item);
      });
      item.setAttribute("tabindex", "0");
      item.setAttribute("role", "button");
      on(item, "keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(i, item); }
      });
    });
    lightbox = { open: open, close: close, isOpen: function () { return el.classList.contains("is-open"); } };
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

/* ==========================================================================
   Keyflow · stardust
   A quiet field of gold dust that drifts and twinkles behind the page, like
   light caught in the air of a concert hall: fine dust, four-point sparkles
   and a few large, soft out-of-focus lights.  One fixed <canvas>, no
   dependencies, nothing to download.

   - decorative only: aria-hidden, pointer-events: none, never takes focus
   - sits behind all content (z-index in style.css), so text contrast is
     decided by the page, not by the dust
   - prefers-reduced-motion: one still frame, no animation, no pointer effects
   - drawn only while the tab is visible; sheds particles if the device struggles
   - scrolling gives depth (near dust moves more than far dust); the mouse
     pushes dust aside and lights a faint pool under the cursor
   ========================================================================== */
(function () {
  "use strict";

  var doc = document;
  if (!doc.body || !window.requestAnimationFrame) return;
  var canvas = doc.createElement("canvas");
  var ctx = canvas.getContext && canvas.getContext("2d");
  if (!ctx) return;
  canvas.className = "stardust";
  ctx.imageSmoothingQuality = "high";
  canvas.setAttribute("aria-hidden", "true");
  doc.body.insertBefore(canvas, doc.body.firstChild);

  /* 1. sprites: soft dots and four-point sparkles, drawn once ---------------- */
  function sprite(size, paint) {
    var c = doc.createElement("canvas");
    c.width = c.height = size;
    paint(c.getContext("2d"), size);
    return c;
  }
  function disc(g, size, stops) {
    var r = size / 2, grad = g.createRadialGradient(r, r, 0, r, r, r);
    stops.forEach(function (s) { grad.addColorStop(s[0], s[1]); });
    g.fillStyle = grad;
    g.fillRect(0, 0, size, size);
  }
  var DOTS = [
    sprite(32, function (g, n) {   // gold
      disc(g, n, [[0, "rgba(255,248,224,1)"], [.18, "rgba(255,226,140,.95)"], [.46, "rgba(242,199,92,.30)"], [1, "rgba(242,199,92,0)"]]);
    }),
    sprite(32, function (g, n) {   // ivory
      disc(g, n, [[0, "rgba(255,255,248,1)"], [.2, "rgba(255,243,210,.9)"], [.5, "rgba(255,243,210,.24)"], [1, "rgba(255,243,210,0)"]]);
    }),
    sprite(32, function (g, n) {   // copper
      disc(g, n, [[0, "rgba(255,236,200,1)"], [.2, "rgba(236,162,96,.9)"], [.5, "rgba(217,138,78,.24)"], [1, "rgba(217,138,78,0)"]]);
    })
  ];
  var STAR = sprite(96, function (g, n) {
    var c = n / 2;
    disc(g, n, [[0, "rgba(255,244,214,.9)"], [.12, "rgba(255,226,140,.5)"], [.4, "rgba(242,199,92,.10)"], [1, "rgba(242,199,92,0)"]]);
    g.globalCompositeOperation = "lighter";
    [true, false].forEach(function (horizontal) {   // two tapered rays
      var grad = horizontal ? g.createLinearGradient(0, c, n, c) : g.createLinearGradient(c, 0, c, n);
      grad.addColorStop(0, "rgba(255,226,140,0)");
      grad.addColorStop(.5, "rgba(255,250,232,1)");
      grad.addColorStop(1, "rgba(255,226,140,0)");
      g.fillStyle = grad;
      g.beginPath();
      if (horizontal) { g.moveTo(0, c); g.quadraticCurveTo(c, c - 2.4, n, c); g.quadraticCurveTo(c, c + 2.4, 0, c); }
      else { g.moveTo(c, 0); g.quadraticCurveTo(c - 2.4, c, c, n); g.quadraticCurveTo(c + 2.4, c, c, 0); }
      g.fill();
    });
  });
  var BOKEH = [
    sprite(128, function (g, n) {   // champagne gold
      disc(g, n, [[0, "rgba(255,226,140,.20)"], [.7, "rgba(242,199,92,.28)"], [.88, "rgba(255,236,170,.44)"], [.96, "rgba(242,199,92,.12)"], [1, "rgba(242,199,92,0)"]]);
    }),
    sprite(128, function (g, n) {   // copper
      disc(g, n, [[0, "rgba(236,162,96,.18)"], [.7, "rgba(217,138,78,.26)"], [.88, "rgba(255,214,170,.40)"], [.96, "rgba(217,138,78,.12)"], [1, "rgba(217,138,78,0)"]]);
    })
  ];
  var POOL = sprite(256, function (g, n) {   // the faint light under the cursor
    disc(g, n, [[0, "rgba(255,226,140,.55)"], [.4, "rgba(242,199,92,.16)"], [1, "rgba(242,199,92,0)"]]);
  });

  /* 2. state ------------------------------------------------------------------ */
  var w = 0, h = 0, dpr = 1;
  var parts = [];
  var quality = 1;                       // shed particles when frames get slow
  var mouse = { x: -9999, y: -9999, on: false, seen: 0, glow: 0 };
  var scrolled = 0;                      // smoothed scroll position
  var raf = 0, last = 0, clock = 0, slow = 0, ema = 0.0167, frames = 0;
  var query = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : null;
  var still = !!(query && query.matches);

  function rand(a, b) { return a + Math.random() * (b - a); }
  function wanted() {   // about one particle per 14,000 px², between 40 and 140
    return Math.round(Math.max(40, Math.min(140, w * h / 14000)) * quality);
  }

  function make(anywhere) {
    var roll = Math.random();
    var type = roll < .09 ? "bokeh" : (roll < .24 ? "star" : "dot");
    var z = type === "bokeh" ? rand(.15, .4) : rand(.25, 1);   // depth: 1 is near
    return {
      type: type,
      x: rand(0, w), y: anywhere ? rand(0, h) : h + rand(40, 80), z: z,
      kind: type === "star" ? 0 : (type === "bokeh" ? (Math.random() < .7 ? 0 : 1) : (Math.random() < .62 ? 0 : (Math.random() < .55 ? 1 : 2))),
      size: type === "bokeh" ? rand(28, 76) : (type === "star" ? 11 + z * 17 : 3.6 + z * 6.6),
      rise: type === "bokeh" ? 2 + z * 8 : 4 + z * 11,           // px per second
      sway: rand(2, 7) * z, swayRate: rand(.15, .5),
      phase: rand(0, 6.283), rate: type === "star" ? rand(.5, 1.4) : (type === "bokeh" ? rand(.2, .5) : rand(.9, 2.8)),
      alpha: type === "bokeh" ? rand(.1, .2) : (type === "star" ? 1 : .3 + z * .55),
      spin: rand(-.3, .3), angle: rand(0, 6.283),
      ox: 0, oy: 0, vx: 0, vy: 0         // displacement from the mouse and its spring
    };
  }

  function reseed() {
    parts.length = 0;
    for (var i = 0, n = wanted(); i < n; i++) parts.push(make(true));
  }

  function resize() {
    var nw = doc.documentElement.clientWidth, nh = window.innerHeight;
    if (canvas.width && nw === w && Math.abs(nh - h) < 160) return;   // a phone's address bar is not a resize
    w = nw; h = nh;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    reseed();
    if (still) paintStill();
  }

  /* 3. drawing ----------------------------------------------------------------- */
  function put(p, x, y, a) {
    if (a <= .01) return;
    ctx.globalAlpha = a > 1 ? 1 : a;
    if (p.type === "star") {
      var s = p.size;
      ctx.save();
      ctx.translate(x, y);
      ctx.rotate(p.angle);
      ctx.drawImage(STAR, -s / 2, -s / 2, s, s);
      ctx.restore();
    } else {
      ctx.drawImage(p.type === "bokeh" ? BOKEH[p.kind] : DOTS[p.kind], x - p.size / 2, y - p.size / 2, p.size, p.size);
    }
  }

  function paintStill() {
    ctx.clearRect(0, 0, w, h);
    ctx.globalCompositeOperation = "lighter";
    parts.forEach(function (p) { put(p, p.x, p.y, p.type === "star" ? .55 : p.alpha * .8); });
    ctx.globalAlpha = 1;
  }

  function frame(now) {
    raf = 0;
    var dt = Math.min(.05, (now - last) / 1000 || .0167);
    last = now;
    clock += dt;

    /* adaptive quality: if the average frame is slower than ~34 fps, shed a quarter of the dust (twice at most) */
    ema += (dt - ema) * .04;
    if (++frames % 90 === 0) {
      slow = ema > .029 ? slow + 1 : 0;
      if (slow >= 2 && quality > .5) { quality -= .25; slow = 0; if (parts.length > wanted()) parts.length = wanted(); }
    }

    var target = window.pageYOffset || doc.documentElement.scrollTop || 0;
    scrolled += (target - scrolled) * Math.min(1, dt * 7);
    var span = h + 60;

    if (mouse.on && clock - mouse.seen > 3.5) mouse.glow += (0 - mouse.glow) * Math.min(1, dt * 2);
    else mouse.glow += ((mouse.on ? 1 : 0) - mouse.glow) * Math.min(1, dt * 4);

    ctx.clearRect(0, 0, w, h);
    ctx.globalCompositeOperation = "lighter";
    if (mouse.glow > .02) {
      ctx.globalAlpha = .14 * mouse.glow;
      ctx.drawImage(POOL, mouse.x - 240, mouse.y - 240, 480, 480);
    }

    for (var i = 0; i < parts.length; i++) {
      var p = parts[i];
      p.y -= p.rise * dt;
      p.x += Math.sin(clock * p.swayRate + p.phase) * p.sway * dt;
      p.angle += p.spin * dt;
      if (p.y < -30) { parts[i] = make(false); parts[i].x = rand(0, w); continue; }
      if (p.x < -30) p.x = w + 20; else if (p.x > w + 30) p.x = -20;

      var y = (((p.y + 30 - scrolled * (.04 + p.z * .3)) % span) + span) % span - 30;   // depth: near dust travels further
      var boost = 1;
      if (mouse.on) {
        var dx = p.x + p.ox - mouse.x, dy = y + p.oy - mouse.y, d2 = dx * dx + dy * dy;
        if (d2 < 19600 && d2 > 1) {      // within 140 px: be pushed away, glow a little brighter
          var d = Math.sqrt(d2), f = 1 - d / 140;
          f *= f;
          p.vx += dx / d * f * 900 * (.4 + p.z) * dt;
          p.vy += dy / d * f * 900 * (.4 + p.z) * dt;
          if (p.type !== "bokeh") boost += f * 1.4;
        }
      }
      if (p.ox || p.oy || p.vx || p.vy) {   // spring back to where it was
        p.vx += -p.ox * 5 * dt; p.vy += -p.oy * 5 * dt;
        p.vx *= 1 - 3.2 * dt; p.vy *= 1 - 3.2 * dt;
        p.ox += p.vx * dt; p.oy += p.vy * dt;
        if (Math.abs(p.ox) + Math.abs(p.oy) + Math.abs(p.vx) + Math.abs(p.vy) < .05) p.ox = p.oy = p.vx = p.vy = 0;
      }

      var s = Math.sin(clock * p.rate + p.phase);
      var a = p.type === "star"
        ? Math.pow(Math.max(0, s), 7) * .95                       // sparkles flash, then rest
        : p.alpha * (.45 + .55 * (.5 + .5 * s));                   // dust and bokeh breathe
      put(p, p.x + p.ox, y + p.oy, a * boost);
    }
    ctx.globalAlpha = 1;
    if (!doc.hidden) raf = requestAnimationFrame(frame);
  }

  /* 4. wiring -------------------------------------------------------------------- */
  function start() {
    if (raf || still || doc.hidden) return;
    last = performance.now();
    raf = requestAnimationFrame(frame);
  }
  function stop() { if (raf) cancelAnimationFrame(raf); raf = 0; }

  function motion() {
    still = !!(query && query.matches);
    if (still) { stop(); mouse.on = false; paintStill(); } else start();
  }

  var timer = 0;
  window.addEventListener("resize", function () { clearTimeout(timer); timer = setTimeout(resize, 120); }, { passive: true });
  window.addEventListener("pointermove", function (e) {
    if (e.pointerType === "touch" || still) return;
    mouse.x = e.clientX; mouse.y = e.clientY; mouse.on = true; mouse.seen = clock;
  }, { passive: true });
  doc.documentElement.addEventListener("pointerleave", function () { mouse.on = false; });
  doc.addEventListener("visibilitychange", function () { if (doc.hidden) stop(); else start(); });
  if (query) {
    if (query.addEventListener) query.addEventListener("change", motion);
    else if (query.addListener) query.addListener(motion);
  }

  resize();
  if (still) paintStill(); else start();
})();

# Keyflow product site

The Keyflow product and download website. It is a dependency-free static site, deployed to [ymkeyflow.online](https://ymkeyflow.online/) with GitHub Pages.

## Local preview

```sh
python3 tools/build.py
python3 -m http.server 8000
```

Then open <http://localhost:8000>. The optional live preview in Arena should bind on `0.0.0.0`.

## Pages

- `index.html` — product landing page
- `features/` — GPU stage, practice, sound and MIDI, recording, design, camera and hand tracking
- `gallery.html` — app-rendered screenshots and showcase video, shown as carousels rather than a wall of images
- `guide.html` — setup, keyboard shortcuts, interface map, command line and product reference
- `download.html` — release packages, checksums and system requirements

English copy is in the generated HTML. Vietnamese strings are collected in the `tools/content_*.py` content modules and written to `i18n/vi/` as runtime dictionaries. `site.js` handles language switching, the responsive navigation drawer, screenshot swapping, the carousel, image viewer and latest-release links. `style.css` is the shared design system.

## Look and feel

The site is a concert-piano stage in gold and black. It is plain CSS and JavaScript; there is nothing to install.

- **Palette and type** — the design tokens (gold, ivory, champagne and copper on near-black, plus the rem type scale) are in `style.css` §1. Headings use Playfair Display and text uses Inter; both cover Vietnamese.
- **Stardust** — `stardust.js` paints drifting, twinkling dust, sparkles and bokeh on one fixed canvas behind the page. It reacts to the pointer, lowers its own quality when frames run long, and is a still picture under `prefers-reduced-motion`.
- **Stage lighting** — every hero is lit by soft beams and a pool of light, with a piano keyboard along its bottom edge; the closing call to action ends on the same keyboard (`stage_fx()` in `tools/sitekit.py`, `style.css` §15). It is decoration only (`aria-hidden`). Beams, key glints and the gold foil on headings all stop when the visitor asks for reduced motion. Cards also glow along their edge where the pointer is, on devices with a mouse.
- **Carousels** — `slider()` in `tools/sitekit.py` renders three variants: a spotlight with thumbnails, tabs, and a numbered stepper. Each has arrows, a picker, keyboard keys, swipe and an autoplay toggle. Autoplay pauses on hover, on focus, when the tab is hidden and when the slider is off screen, and every slide opens in one shared lightbox (`site.js` §5 and §6).
- **Readability** — body copy is 16.5–17 px, lines stop at about 75 characters, small capitals are never under 13 px, and touch targets reach 44 px on phones. `tools/check_site.py` fails on a skipped heading level, a missing credit or a decorative element that is not `aria-hidden`.

## Build and verify

No npm install or build tool is needed. After editing a content module, regenerate the HTML and language dictionaries:

```sh
python3 tools/build.py
python3 tools/build.py --check
python3 tools/check_site.py        # links, routes, translations, assets and JS syntax
python3 tools/make_images.py       # only when source screenshots change
```

The screenshot PNGs in `previews/en/` and `previews/vi/` remain the source of truth. `tools/make_images.py` creates smaller WebP variants in `previews/webp/`; pages provide the WebP first and keep PNG/JPEG fallbacks.

GitHub Actions checks generated-page freshness and runs the static QA suite before publishing the pages, language dictionaries, screenshots, WebP images and showcase video.

## Credits and licence

Keyflow is made by **Yami**, **Neyu** and **Jin**. Every page credits all three in its footer, in `<meta name="author">` and in the JSON-LD (`author`, `copyrightHolder`, `copyrightYear`). The names live in `tools/sitekit.py` (`AUTHORS`), and `tools/check_site.py` fails if one goes missing.

© 2026 Yami, Neyu, Jin. The application is released under the MIT licence (see `LICENSE` in the [Keyflow repository](https://github.com/lxmtuu/KeyFlow)); the piano samples are Salamander Grand Piano V3, recorded by Alexander Holm, under CC BY 3.0 — downloaded by the app on request, not bundled with it.

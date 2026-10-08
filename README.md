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
- `gallery.html` — app-rendered screenshots and showcase video
- `guide.html` — setup, keyboard shortcuts, interface map, command line and product reference
- `download.html` — release packages, checksums and system requirements

English copy is in the generated HTML. Vietnamese strings are collected in the `tools/content_*.py` content modules and written to `i18n/vi/` as runtime dictionaries. `site.js` handles language switching, the responsive navigation drawer, screenshot swapping, the carousel, image viewer and latest-release links. `style.css` is the shared design system.

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

© 2026 Yami, Neyu, Jin. The application is released under the MIT licence (see `LICENSE` in the [Keyflow repository](https://github.com/lxmtuu/KeyFlow)); the bundled YDP Grand Piano SoundFont is by FreePats under CC BY 3.0.

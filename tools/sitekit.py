#!/usr/bin/env python3
"""Page assembler for the Keyflow product site.

The site is plain static HTML — no framework, no bundler, no JavaScript at
build time.  What this module does instead is keep the twelve pages honest with
each other: one header, one footer, one design vocabulary, and one place where
every English string is paired with its Vietnamese translation.

Content lives in ``tools/content_*.py`` as small dictionaries built with the
helpers below (``hero``, ``split``, ``grid``, ``table`` …).  ``build.py`` walks
those definitions, renders the HTML and writes the generated Vietnamese tables
into ``i18n/vi/<page>.js``.

English is the source of truth and stays in the markup; Vietnamese is swapped in
at runtime by ``site.js``, so a page is still a complete document with scripting
turned off.
"""
from __future__ import annotations

import html as _html
import json
from typing import Any, Iterable, Sequence

SITE_URL = "https://ymkeyflow.online"
REPO = "https://github.com/lxmtuu/KeyFlow"
RELEASES = f"{REPO}/releases"
RELEASE_TAG = "v1.0.0"
RELEASE_PAGE = f"{REPO}/releases/tag/{RELEASE_TAG}"
ISSUES = f"{REPO}/issues"
CHANGELOG = f"{REPO}/blob/main/CHANGELOG.en.md"
CHANGELOG_VI = f"{REPO}/blob/main/CHANGELOG.md"
README_EN = f"{REPO}/blob/main/README.en.md"
README_VI = f"{REPO}/blob/main/README.md"
LICENSE = f"{REPO}/blob/main/LICENSE"
DOTNET = "https://dotnet.microsoft.com/download/dotnet/10.0"
FREEPATS = "https://freepats.zenvoid.org/"
VORTICE = "https://github.com/amerkoleci/Vortice.Windows"

# Credits.  All three are authors and copyright holders; none is given a role.  The names appear in the
# footer of every page, in <meta name="author"> and in the JSON-LD, and check_site.py fails if one goes missing.
AUTHORS = ("Yami", "Neyu", "Jin")
COPYRIGHT_YEAR = 2026

ASSETS = {
    "setup": f"{REPO}/releases/download/{RELEASE_TAG}/Keyflow-Setup-1.0.0.exe",
    "portable": f"{REPO}/releases/download/{RELEASE_TAG}/Keyflow-1.0.0-win-x64.zip",
    "fd": f"{REPO}/releases/download/{RELEASE_TAG}/Keyflow-1.0.0-win-x64-fd.zip",
    "arm64": f"{REPO}/releases/download/{RELEASE_TAG}/Keyflow-1.0.0-win-arm64.zip",
    "sums": f"{REPO}/releases/download/{RELEASE_TAG}/SHA256SUMS.txt",
}

# Internal pages, in the order the footer, the menu and the prev/next links use.
FEATURES = [
    ("features/stage.html", "stage"),
    ("features/practice.html", "practice"),
    ("features/sound.html", "sound"),
    ("features/recording.html", "recording"),
    ("features/design.html", "design"),
    ("features/camera.html", "camera"),
]
PAGES = [("index.html", "home")] + FEATURES + [
    ("gallery.html", "gallery"),
    ("guide.html", "guide"),
    ("download.html", "download"),
]

# ---------------------------------------------------------------------------
# Icons: 24×24 stroke glyphs, drawn with currentColor so a card can tint them.
# ---------------------------------------------------------------------------
_S = 'fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"'
ICONS: dict[str, str] = {
    "chip": f'<path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/><rect x="6" y="6" width="12" height="12" rx="2"/><rect x="10" y="10" width="4" height="4" rx="1"/>',
    "spark": f'<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6.3 6.3l2.8 2.8M14.9 14.9l2.8 2.8M17.7 6.3l-2.8 2.8M9.1 14.9l-2.8 2.8"/>',
    "flame": '<path d="M12 22c4 0 6.5-2.6 6.5-6 0-4.2-4-6-4-10 0 0-3 1.6-3 5 0 1.6.7 2.4.7 3.4 0 1-.8 1.6-1.6 1.6-1 0-1.8-.8-1.8-2.2C7 15.4 5.5 17 5.5 19c0 1.9 2.4 3 6.5 3Z"/>',
    "note": '<path d="M9 18V6l10-2v12"/><circle cx="6.5" cy="18" r="2.5"/><circle cx="16.5" cy="16" r="2.5"/>',
    "piano": '<rect x="2.5" y="5" width="19" height="14" rx="2"/><path d="M7 5v9M12 5v9M17 5v9M2.5 14h19"/>',
    "wave": '<path d="M2 12h2.5l2-6 3 14 3-11 2.5 6 2-3H22"/>',
    "mic": '<rect x="9" y="2.5" width="6" height="11" rx="3"/><path d="M5.5 11.5a6.5 6.5 0 0 0 13 0M12 18v3.5M8.5 21.5h7"/>',
    "video": '<rect x="2.5" y="6" width="13" height="12" rx="2.5"/><path d="m15.5 12 6-3.5v11l-6-3.5"/>',
    "rec": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="3.5" fill="currentColor" stroke="none"/>',
    "target": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1" fill="currentColor" stroke="none"/>',
    "chart": '<path d="M3 20h18M6 20v-6M11 20V6M16 20v-9M21 20v-4"/>',
    "palette": '<path d="M12 21a9 9 0 1 1 9-9c0 2-1.6 3-3.4 3H16a2 2 0 0 0-1.4 3.4c.5.6.2 1.6-.6 2A8.9 8.9 0 0 1 12 21Z"/><circle cx="8" cy="10" r="1.2" fill="currentColor" stroke="none"/><circle cx="12" cy="7.5" r="1.2" fill="currentColor" stroke="none"/><circle cx="16" cy="10" r="1.2" fill="currentColor" stroke="none"/>',
    "sliders": '<path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h9M17 18h3"/><circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="15" cy="18" r="2"/>',
    "layers": '<path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3.5 12.5 8.5 4.7 8.5-4.7M3.5 16.8l8.5 4.7 8.5-4.7"/>',
    "camera": '<path d="M3 8.5A2.5 2.5 0 0 1 5.5 6h1.8l1.3-2h6.8l1.3 2h1.8A2.5 2.5 0 0 1 21 8.5v9A2.5 2.5 0 0 1 18.5 20h-13A2.5 2.5 0 0 1 3 17.5v-9Z"/><circle cx="12" cy="13" r="3.6"/>',
    "hand": '<path d="M8 11V5.5a1.5 1.5 0 0 1 3 0V11m0-1.5a1.5 1.5 0 0 1 3 0V12m0-1.5a1.5 1.5 0 0 1 3 0V16a5.5 5.5 0 0 1-5.5 5.5h-1A6.5 6.5 0 0 1 4 15v-2.5a1.5 1.5 0 0 1 3 0V13"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.6 2.6 15 0 18M12 3c-2.6 2.6-2.6 15 0 18"/>',
    "download": '<path d="M12 3v11m0 0 4-4m-4 4-4-4M4 17.5V19a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-1.5"/>',
    "github": '<path fill="currentColor" stroke="none" d="M12 .5a11.5 11.5 0 0 0-3.64 22.41c.58.1.79-.25.79-.56v-2c-3.2.7-3.88-1.37-3.88-1.37-.52-1.33-1.28-1.69-1.28-1.69-1.04-.71.08-.7.08-.7 1.15.08 1.76 1.19 1.76 1.19 1.03 1.76 2.69 1.25 3.35.96.1-.74.4-1.25.73-1.54-2.55-.29-5.24-1.28-5.24-5.69 0-1.26.45-2.28 1.19-3.09-.12-.29-.52-1.46.11-3.05 0 0 .97-.31 3.17 1.18a11 11 0 0 1 5.77 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.59.23 2.76.11 3.05.74.81 1.19 1.83 1.19 3.09 0 4.42-2.7 5.4-5.27 5.68.41.36.78 1.06.78 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 12 .5Z"/>',
    "windows": '<path d="M3 5.6 10.4 4.5v7H3v-5.9ZM11.6 4.3 21 3v8.5h-9.4v-7.2ZM3 12.5h7.4v7L3 18.4v-5.9ZM11.6 12.5H21V21l-9.4-1.3v-7.2Z"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "arrow": '<path d="M4 12h15m0 0-6-6m6 6-6 6"/>',
    "left": '<path d="m15 18-6-6 6-6"/>',
    "right": '<path d="m9 18 6-6-6-6"/>',
    "down": '<path d="m6 9 6 6 6-6"/>',
    "up": '<path d="m18 15-6-6-6 6"/>',
    "menu": '<path d="M3.5 6.5h17M3.5 12h17M3.5 17.5h17"/>',
    "close": '<path d="M18 6 6 18M6 6l12 12"/>',
    "bolt": '<path d="M13 2 4.5 13.5H11L10 22l9-12h-6.5L13 2Z"/>',
    "gauge": '<path d="M4 18a9 9 0 1 1 16 0"/><path d="m12 14 4-4"/><circle cx="12" cy="15" r="1.6"/>',
    "folder": '<path d="M3 7.5A2 2 0 0 1 5 5.5h3.7l1.8 2.2H19a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-10Z"/>',
    "file": '<path d="M6 3.5h7.5L19 9v11.5H6V3.5Z"/><path d="M13 3.5V9h5.5M8.5 13h7M8.5 16.5h5"/>',
    "terminal": '<rect x="2.5" y="4.5" width="19" height="15" rx="2.5"/><path d="m6.5 9.5 3 2.5-3 2.5M12.5 15h5"/>',
    "shield": '<path d="M12 3 5 5.5v5.8c0 4.3 2.9 8.1 7 9.7 4.1-1.6 7-5.4 7-9.7V5.5L12 3Z"/><path d="m9 12 2 2 4-4"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5.5M12 7.8v.4"/>',
    "alert": '<path d="M12 3.5 21.5 20h-19L12 3.5Z"/><path d="M12 9.5v4.5M12 17v.3"/>',
    "book": '<path d="M4 5.5A2 2 0 0 1 6 3.5h13v14H6a2 2 0 0 0-2 2v-14Z"/><path d="M4 19.5a2 2 0 0 1 2-2h13v3H6a2 2 0 0 1-2-1Z"/>',
    "keys": '<rect x="2.5" y="6" width="19" height="12" rx="2"/><path d="M6 9.5h.01M9.5 9.5h.01M13 9.5h.01M16.5 9.5h.01M6 12.8h.01M18 12.8h.01M8.5 15.5h7"/>',
    "loop": '<path d="M4 9a5 5 0 0 1 5-5h9m0 0-3-3m3 3-3 3M20 15a5 5 0 0 1-5 5H6m0 0 3 3m-3-3 3-3"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5.3l3.3 2"/>',
    "image": '<rect x="3" y="4.5" width="18" height="15" rx="2.5"/><circle cx="8.5" cy="10" r="1.8"/><path d="m4 17.5 4.8-4.3 3.4 3 3-2.6 4.8 4.2"/>',
    "grid": '<rect x="3.5" y="3.5" width="7" height="7" rx="1.6"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.6"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.6"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.6"/>',
    "wand": '<path d="m4 20 10-10M14.5 4.5 16 3M19.5 9.5 21 11M17 6l3 3M13 3.5 14 6M18.5 14 21 15"/>',
    "share": '<circle cx="6" cy="12" r="2.6"/><circle cx="17.5" cy="6" r="2.6"/><circle cx="17.5" cy="18" r="2.6"/><path d="m8.4 10.8 6.8-3.6M8.4 13.2l6.8 3.6"/>',
    "heart": '<path d="M12 20s-7.5-4.4-7.5-9.4A4.1 4.1 0 0 1 12 7.6a4.1 4.1 0 0 1 7.5 3c0 5-7.5 9.4-7.5 9.4Z"/>',
    "eye": '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12Z"/><circle cx="12" cy="12" r="3.2"/>',
    "plug": '<path d="M9 3v5M15 3v5M6.5 8h11v3a5.5 5.5 0 0 1-11 0V8ZM12 16.5V21"/>',
    "search": '<circle cx="11" cy="11" r="6.5"/><path d="m16 16 4.5 4.5"/>',
    "undo": '<path d="M4 9h9.5a5.5 5.5 0 0 1 0 11H8m-4-11 4-4m-4 4 4 4"/>',
    "play": '<path d="M8 5.2v13.6a.6.6 0 0 0 .9.5l10.8-6.8a.6.6 0 0 0 0-1L8.9 4.7a.6.6 0 0 0-.9.5Z" fill="currentColor"/>',
    "pause": '<path d="M8.5 5v14M15.5 5v14" stroke-width="3.2"/>',
    "zoom": '<circle cx="11" cy="11" r="6.5"/><path d="m16 16 4.5 4.5M11 8.3v5.4M8.3 11h5.4"/>',
}


def icon(name: str, size: int = 20, cls: str = "") -> str:
    body = ICONS.get(name, ICONS["info"])
    klass = f' class="{cls}"' if cls else ""
    return (f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" aria-hidden="true"'
            f' focusable="false"{klass} {_S}>{body}</svg>')


def iconbox(name: str, size: int = 20, tint: str = "") -> str:
    cls = "ico" + (f" {tint}" if tint else "")
    return f'<span class="{cls}">{icon(name, size)}</span>'


# ---------------------------------------------------------------------------
# Translation pairs
# ---------------------------------------------------------------------------
def T(en: str, vi: str) -> tuple[str, str]:
    """A bilingual string: ``T("Download", "Tải về")``."""
    return (en, vi)


def E(en: str) -> tuple[str, str]:
    """A string that is the same in both languages (names, ids, numbers)."""
    return (en, en)


class Doc:
    """Collects the Vietnamese half of one page while the HTML is rendered."""

    def __init__(self, pid: str, root: str = ""):
        self.pid = pid
        self.root = root
        self.vi: dict[str, str] = {}       # copy that belongs to this page
        self.shared: dict[str, str] = {}   # chrome copy, shared by every page
        self._n = 0

    def key(self, pair: tuple[str, str] | str, field: str = "") -> tuple[str, str]:
        """Register a pair and return ``(key, english_html)``.

        Strings that come from the shared ``UI`` table keep their stable
        ``ui.*`` key, so the header and the footer are translated once for the
        whole site instead of once per page.
        """
        if isinstance(pair, str):
            pair = (pair, pair)
        en, vi = pair
        if not isinstance(en, str) or not isinstance(vi, str):
            raise TypeError(f"translation pair must contain strings, got {type(en).__name__}, {type(vi).__name__}")
        if not field:
            stable = UI_KEY_BY_PAIR.get(pair)
            if stable:
                if vi and vi != en:
                    self.shared[stable] = vi
                return stable, en
        self._n += 1
        key = f"{self.pid}.{self._n}" + (f".{field}" if field else "")
        if vi and vi != en:
            self.vi[key] = vi
        return key, en

    def url(self, path: str) -> str:
        if path.startswith(("http://", "https://", "mailto:", "#")):
            return path
        return self.root + path


# ---------------------------------------------------------------------------
# Small pieces
# ---------------------------------------------------------------------------
def picture(doc: Doc, shot: str, alt: tuple[str, str], *, width: int = 1080, height: int = 700,
            lazy: bool = True, badge: tuple[str, str] | None = None, cls: str = "frame",
            zoom: bool = False) -> str:
    """A ``<picture>`` with the WebP copy first and the PNG as the fallback.

    ``data-shot`` is what ``site.js`` rewrites when the language changes: the
    application renders one set of screenshots per language in CI.  With
    ``zoom`` a real ``<button class="lb-trigger">`` is laid over the picture; the
    lightbox in ``site.js`` listens for it (the ``<img>`` keeps its own alt text).
    """
    key, en = doc.key(alt, "alt")
    loading = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    root = doc.root
    badge_html = ""
    if badge:
        bkey, ben = doc.key(badge)
        badge_html = (f'<span class="frame-badge"><span class="dot"></span>'
                      f'<span data-i18n="{bkey}">{ben}</span></span>')
    return (
        f'<div class="{cls}" data-shot="{shot}">'
        f'<picture><source type="image/webp" srcset="{root}previews/webp/en/{shot}.webp">'
        f'<img src="{root}previews/en/{shot}.png" width="{width}" height="{height}" '
        f'data-i18n-attr="alt={key}" alt="{_html.escape(en, quote=True)}" '
        f'decoding="async"{loading}></picture>'
        f"{badge_html}{_zoom_trigger(doc) if zoom else ''}</div>"
    )


def _zoom_trigger(doc: Doc) -> str:
    k, v = doc.key(UI["ui.lb.enlarge"])
    return (f'<button type="button" class="lb-trigger" data-i18n-attr="aria-label={k}" '
            f'aria-label="{_html.escape(v, quote=True)}">{icon("zoom", 20)}</button>')


def figure(doc: Doc, shot: str, alt: tuple[str, str], cap: tuple[str, str] | None = None, **kw) -> str:
    inner = picture(doc, shot, alt, zoom=True, **kw)
    if cap:
        ckey, cen = doc.key(cap)
        inner += f'<figcaption class="lb-caption" data-i18n="{ckey}">{cen}</figcaption>'
    return f'<figure class="shot" data-lightbox data-lb-item>{inner}</figure>'


def framed(doc: Doc, shot: str, alt: tuple[str, str], cap: tuple[str, str] | None = None,
           badge: tuple[str, str] | None = None, lazy: bool = True,
           width: int = 1080, height: int = 700) -> str:
    """A figure with a ``<picture>``, an optional badge and a translated caption."""
    inner = picture(doc, shot, alt, lazy=lazy, badge=badge, width=width, height=height, zoom=True)
    out = f'<figure class="shot" style="margin:0" data-lightbox data-lb-item>{inner}'
    if cap:
        ck, cv = doc.key(cap)
        out += f'<figcaption class="frame-cap lb-caption" data-i18n="{ck}">{cv}</figcaption>'
    return out + "</figure>"


def chip_item(item: Any) -> tuple[tuple[str, str], str]:
    """Return a bilingual pair and optional tint from supported chip shapes."""
    if isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], tuple):
        pair, tint = item[0], item[1]
    elif isinstance(item, tuple) and len(item) == 3:
        pair, tint = (item[0], item[1]), item[2]
    elif isinstance(item, tuple):
        pair, tint = item, ""
    else:
        pair, tint = (item, item), ""
    return pair, (str(tint) if tint else "")


def buttons(doc: Doc, items: Sequence[dict[str, Any]], cls: str = "actions") -> str:
    out = []
    for b in items:
        label_key, label = doc.key(b["label"])
        klass = "btn " + b.get("kind", "btn-ghost") + (" " + b["size"] if b.get("size") else "")
        href = doc.url(b.get("href", "#"))
        extra = ""
        if b.get("asset"):
            extra += f' data-asset="{b["asset"]}"'
        if b.get("external"):
            extra += ' target="_blank" rel="noopener"'
        if b.get("aria"):
            akey, aen = doc.key(b["aria"])
            extra += f' data-i18n-attr="aria-label={akey}" aria-label="{_html.escape(aen, quote=True)}"'
        ico = icon(b["icon"], 18) + " " if b.get("icon") else ""
        out.append(f'<a class="{klass}" href="{href}"{extra}>{ico}<span data-i18n="{label_key}">{label}</span></a>')
    return f'<div class="{cls}">' + "".join(out) + "</div>"


# ---------------------------------------------------------------------------
# Sections.  Every helper returns a dict that ``render_section`` understands.
# ---------------------------------------------------------------------------
def sec(kind: str, **kw) -> dict[str, Any]:
    kw["kind"] = kind
    return kw


def hero(**kw): return sec("hero", **kw)
def pagehero(**kw): return sec("pagehero", **kw)
def band(**kw): return sec("band", **kw)
def grid(**kw): return sec("grid", **kw)
def split(**kw): return sec("split", **kw)
def steps(**kw): return sec("steps", **kw)
def table(**kw): return sec("table", **kw)
def specdl(**kw): return sec("specdl", **kw)
def callout(**kw): return sec("callout", **kw)
def codeblock(**kw): return sec("code", **kw)
def faq(**kw): return sec("faq", **kw)
def cta(**kw): return sec("cta", **kw)
def slider(**kw): return sec("slider", **kw)
def chipcloud(**kw): return sec("chips", **kw)
def groups(**kw): return sec("groups", **kw)
def carousel(**kw): return sec("slider", **{"variant": "spotlight", "autoplay": True, **kw})
def pagenav(**kw): return sec("pagenav", **kw)
def dlhero(**kw): return sec("dlhero", **kw)
def raw(html_text: str): return sec("raw", html=html_text)


def head(doc: Doc, s: dict[str, Any]) -> str:
    parts = []
    center = " center" if s.get("center") else ""
    if s.get("eyebrow"):
        k, v = doc.key(s["eyebrow"])
        parts.append(f'<p class="eyebrow" data-i18n="{k}">{v}</p>')
    if s.get("title"):
        k, v = doc.key(s["title"])
        parts.append(f'<h2 data-i18n="{k}">{v}</h2>')
    if s.get("sub"):
        k, v = doc.key(s["sub"])
        parts.append(f'<p class="sub" data-i18n="{k}">{v}</p>')
    inner = f'<div class="section-head{center}">' + "".join(parts) + "</div>"
    return inner


def wrap(doc: Doc, s: dict[str, Any], inner: str, extra_cls: str = "") -> str:
    sid = f' id="{s["id"]}"' if s.get("id") else ""
    cls = "section" + (f" {extra_cls}" if extra_cls else "") + (f' {s["cls"]}' if s.get("cls") else "")
    return f'<section{sid} class="{cls}"><div class="container">{inner}</div></section>'


def render_section(doc: Doc, s: dict[str, Any]) -> str:  # noqa: C901 - one dispatch table
    kind = s["kind"]

    if kind == "raw":
        return s["html"]

    if kind == "hero":
        return render_hero(doc, s)

    if kind == "pagehero":
        return render_pagehero(doc, s)

    if kind == "band":
        return render_band(doc, s)

    if kind == "grid":
        cards = []
        for i, c in enumerate(s["cards"]):
            ik, iv = doc.key(c["t"])
            dk, dv = doc.key(c["d"])
            delay = f' style="--d:{(i % 3) * 70}ms"'
            inner = ""
            if c.get("icon"):
                inner += iconbox(c["icon"], 20, c.get("tint", ""))
            inner += f'<h3 data-i18n="{ik}">{iv}</h3><p data-i18n="{dk}">{dv}</p>'
            if c.get("href"):
                mk, mv = doc.key(c.get("more") or T("Learn more", "Xem chi tiết"))
                inner += (f'<span class="card-more"><span data-i18n="{mk}">{mv}</span> '
                          f'<span class="arw">{icon("arrow", 15)}</span></span>')
                cards.append(f'<a class="card reveal" href="{doc.url(c["href"])}"{delay}>{inner}</a>')
            else:
                cards.append(f'<article class="card reveal"{delay}>{inner}</article>')
        cols = {2: " two", 4: " four"}.get(s.get("cols", 3), "")
        inner = head(doc, s) + f'<div class="grid{cols}">' + "".join(cards) + "</div>"
        return wrap(doc, s, inner)

    if kind == "split":
        return render_split(doc, s)

    if kind == "steps":
        items = []
        for st in s["items"]:
            tk, tv = doc.key(st["t"])
            dk, dv = doc.key(st["d"])
            items.append(f'<li class="reveal"><b data-i18n="{tk}">{tv}</b><span data-i18n="{dk}">{dv}</span></li>')
        cls = "steps" + {2: " two", 4: " four"}.get(s.get("cols", 3), "")
        if s.get("numbered"):
            cls = "steps-num"
            items = []
            for st in s["items"]:
                tk, tv = doc.key(st["t"])
                dk, dv = doc.key(st["d"])
                items.append(f'<li class="reveal"><b data-i18n="{tk}">{tv}</b> — <span data-i18n="{dk}">{dv}</span></li>')
        inner = head(doc, s) + f'<ol class="{cls}">' + "".join(items) + "</ol>"
        if s.get("note"):
            nk, nv = doc.key(s["note"])
            inner += f'<p class="table-note" data-i18n="{nk}">{nv}</p>'
        return wrap(doc, s, inner)

    if kind == "table":
        return render_table(doc, s)

    if kind == "specdl":
        rows = []
        for k, v in s["items"]:
            kk, kv = doc.key(k)
            vk, vv = doc.key(v)
            rows.append(f'<div><dt data-i18n="{kk}">{kv}</dt><dd data-i18n="{vk}">{vv}</dd></div>')
        inner = head(doc, s) + '<dl class="spec">' + "".join(rows) + "</dl>"
        return wrap(doc, s, inner)

    if kind == "callout":
        return render_callout(doc, s)

    if kind == "code":
        return render_code(doc, s)

    if kind == "faq":
        items = []
        for i, q in enumerate(s["items"]):
            qk, qv = doc.key(q["q"])
            ak, av = doc.key(q["a"])
            items.append(
                f'<details class="qa reveal" style="--d:{min(i, 4) * 50}ms">'
                f'<summary data-i18n="{qk}">{qv}</summary>'
                f'<div class="a" data-i18n="{ak}">{av}</div></details>'
            )
        inner = head(doc, s) + '<div class="faq">' + "".join(items) + "</div>"
        return wrap(doc, s, inner)

    if kind == "cta":
        return render_cta(doc, s)

    if kind == "slider":
        return render_slider(doc, s)

    if kind == "chips":
        chips = []
        for c in s["items"]:
            pair, color = chip_item(c)
            tint = f" {color}" if color else ""
            ck, cv = doc.key(pair)
            chips.append(f'<span class="chip{tint}" data-i18n="{ck}">{cv}</span>')
        inner = head(doc, s) + '<div class="chips">' + "".join(chips) + "</div>"
        if s.get("actions"):
            inner += buttons(doc, s["actions"]).replace('class="actions"', 'class="actions" style="margin-top:22px"', 1)
        return wrap(doc, s, inner)

    if kind == "groups":
        cols = []
        for g in s["groups"]:
            gk, gv = doc.key(g["name"])
            rows = []
            for name, desc in g["items"]:
                nk, nv = doc.key(name)
                dk, dv = doc.key(desc)
                rows.append(f'<li><b data-i18n="{nk}">{nv}</b><span data-i18n="{dk}">{dv}</span></li>')
            ico = iconbox(g.get("icon", "grid"), 18)
            cols.append(f'<div class="group reveal"><h3>{ico}<span data-i18n="{gk}">{gv}</span></h3>'
                        f'<ul>{"".join(rows)}</ul></div>')
        inner = head(doc, s) + '<div class="groups">' + "".join(cols) + "</div>"
        return wrap(doc, s, inner)


    if kind == "pagenav":
        cells = []
        for direction, item in (("prev", s.get("prev")), ("next", s.get("next"))):
            if not item:
                cells.append("<span></span>")
                continue
            path, pid = item
            label = UI["feature." + pid] if "feature." + pid in UI else UI["page." + pid]
            lk, lv = doc.key(label)
            dk = "ui.nav.prev" if direction == "prev" else "ui.nav.next"
            dk, dv = doc.key(UI[dk])
            arrow = icon("left", 15) if direction == "prev" else icon("right", 15)
            cls = "pagenav-" + direction
            cells.append(
                f'<a class="{cls} {"prev" if direction == "prev" else "next"}" href="{doc.url(path)}">'
                f'<span class="dir"><span data-i18n="{dk}">{dv}</span> {arrow}</span>'
                f'<span class="ttl" data-i18n="{lk}">{lv}</span></a>'
            )
        inner = '<div class="pagenav">' + "".join(cells) + "</div>"
        return wrap(doc, s, inner)

    if kind == "dlhero":
        return render_dlhero(doc, s)

    raise ValueError(f"unknown section kind: {kind}")


# ---------------------------------------------------------------------------
# Section renderers that need more room
# ---------------------------------------------------------------------------
def render_hero(doc: Doc, s: dict[str, Any]) -> str:
    copy_html = ""
    if s.get("eyebrow"):
        k, v = doc.key(s["eyebrow"])
        copy_html += f'<p class="eyebrow" data-i18n="{k}">{v}</p>'
    k, v = doc.key(s["title"])
    copy_html += f'<h1 data-i18n="{k}">{v}</h1>'
    if s.get("lead"):
        k, v = doc.key(s["lead"])
        copy_html += f'<p class="lead" data-i18n="{k}">{v}</p>'
    if s.get("actions"):
        copy_html += buttons(doc, s["actions"])
    if s.get("facts"):
        lis = []
        for f in s["facts"]:
            k, v = doc.key(f)
            lis.append(f'<li data-i18n="{k}">{v}</li>')
        copy_html += '<ul class="facts">' + "".join(lis) + "</ul>"
    if s.get("chips"):
        chips = []
        for c in s["chips"]:
            pair, color = chip_item(c)
            k, v = doc.key(pair)
            tint = f" {color}" if color else ""
            chips.append(f'<span class="chip{tint}" data-i18n="{k}">{v}</span>')
        copy_html += '<div class="meta-chips">' + "".join(chips) + "</div>"

    media = s.get("media", "")
    return (f'<section class="hero"><div class="container hero-in">'
            f'<div class="hero-copy">{copy_html}</div>'
            f'<div class="hero-media">{media}</div>'
            f'</div></section>')


def render_pagehero(doc: Doc, s: dict[str, Any]) -> str:
    nav_key, nav_label = doc.key(UI["ui.breadcrumb"])
    crumbs = [f'<nav class="crumbs" aria-label="{_html.escape(nav_label, quote=True)}" data-i18n-attr="aria-label={nav_key}"><ol>']
    hk, hv = doc.key(UI["ui.home"])
    crumbs.append(f'<li><a href="{doc.url("index.html")}" data-i18n="{hk}">{hv}</a></li>')
    for label, href in s.get("crumbs", []):
        k, v = doc.key(label)
        crumbs.append(f'<li aria-hidden="true" class="sep">/</li><li><a href="{doc.url(href)}" data-i18n="{k}">{v}</a></li>')
    k, v = doc.key(s["crumb"])
    crumbs.append(f'<li aria-hidden="true" class="sep">/</li><li aria-current="page" data-i18n="{k}">{v}</li>')
    crumbs.append("</ol></nav>")

    copy_html = "".join(crumbs)
    if s.get("eyebrow"):
        k, v = doc.key(s["eyebrow"])
        copy_html += f'<p class="eyebrow" data-i18n="{k}">{v}</p>'
    k, v = doc.key(s["title"])
    copy_html += f'<h1 data-i18n="{k}">{v}</h1>'
    if s.get("lead"):
        k, v = doc.key(s["lead"])
        copy_html += f'<p class="lead" data-i18n="{k}">{v}</p>'
    if s.get("chips"):
        chips = []
        for c in s["chips"]:
            pair, color = chip_item(c)
            k, v = doc.key(pair)
            tint = f" {color}" if color else ""
            chips.append(f'<span class="chip{tint}" data-i18n="{k}">{v}</span>')
        copy_html += '<div class="meta-chips">' + "".join(chips) + "</div>"
    if s.get("actions"):
        copy_html += '<div style="margin-top:24px">' + buttons(doc, s["actions"]) + "</div>"

    media = s.get("media", "")
    klass = "pagehero" + (" " + s["cls"] if s.get("cls") else "")
    return (f'<section class="{klass}"><div class="container pagehero-in">'
            f'<div class="split-copy">{copy_html}</div>'
            f'<div class="split-media">{media}</div>'
            f'</div></section>')


def render_band(doc: Doc, s: dict[str, Any]) -> str:
    """A thin full-width strip: stats, a quote or a row of chips."""
    inner = ""
    if s.get("stats"):
        cells = []
        for item in s["stats"]:
            value, label = item[0], item[1]
            count = item[2] if len(item) > 2 else None
            if isinstance(value, tuple):
                vk, vv = doc.key(value)
                attrs = f' data-i18n="{vk}"'
            else:
                vv, attrs = value, ""
            if count:
                attrs += f' data-count="{count}"'
            lk, lv = doc.key(label)
            cells.append(f'<div class="stat"><b{attrs}>{vv}</b><span data-i18n="{lk}">{lv}</span></div>')
        cols = " four" if len(cells) == 4 else ""
        inner = f'<div class="stats{cols}">' + "".join(cells) + "</div>"
    if s.get("quote"):
        qk, qv = doc.key(s["quote"])
        who = ""
        if s.get("who"):
            wk, wv = doc.key(s["who"])
            who = f'<footer class="muted small" data-i18n="{wk}" style="margin-top:12px">{wv}</footer>'
        inner += (f'<blockquote style="margin:0;max-width:78ch;font-family:var(--font-display);'
                  f'font-size:clamp(20px,2.4vw,29px);line-height:1.4;color:var(--text)">'
                  f'<span data-i18n="{qk}">{qv}</span>{who}</blockquote>')
    if s.get("html"):
        inner += s["html"]
    extra = ""
    if s.get("center"):
        extra = ' style="display:grid;justify-items:center;text-align:center"'
    sid = f' id="{s["id"]}"' if s.get("id") else ""
    return f'<section{sid} class="section band"><div class="container"{extra}>{inner}</div></section>'


def render_split(doc: Doc, s: dict[str, Any]) -> str:
    copy_html = ""
    if s.get("eyebrow"):
        k, v = doc.key(s["eyebrow"])
        copy_html += f'<p class="eyebrow" data-i18n="{k}">{v}</p>'
    if s.get("title"):
        k, v = doc.key(s["title"])
        copy_html += f'<h2 data-i18n="{k}">{v}</h2>'
    for para in s.get("body", []) or []:
        k, v = doc.key(para)
        copy_html += f'<p class="body" data-i18n="{k}">{v}</p>'
    if s.get("ticks"):
        lis = []
        for t in s["ticks"]:
            k, v = doc.key(t)
            lis.append(f'<li data-i18n="{k}">{v}</li>')
        notes = " notes" if s.get("note_ticks") else ""
        copy_html += f'<ul class="ticks{notes}">' + "".join(lis) + "</ul>"
    if s.get("chips"):
        chips = []
        for c in s["chips"]:
            pair, color = chip_item(c)
            k, v = doc.key(pair)
            tint = f" {color}" if color else ""
            chips.append(f'<span class="chip{tint}" data-i18n="{k}">{v}</span>')
        copy_html += '<div class="meta-chips">' + "".join(chips) + "</div>"
    if s.get("actions"):
        copy_html += buttons(doc, s["actions"])
    if s.get("extra"):
        copy_html += s["extra"]

    media = s.get("media", "")
    flip = " flip" if s.get("flip") else ""
    sid = f' id="{s["id"]}"' if s.get("id") else ""
    return (f'<section{sid} class="section"><div class="container split{flip}">'
            f'<div class="split-copy reveal">{copy_html}</div>'
            f'<div class="split-media reveal">{media}</div>'
            f'</div></section>')


def render_table(doc: Doc, s: dict[str, Any]) -> str:
    cols = s.get("cols") or []
    thead = ""
    if s.get("head"):
        ths = []
        for hcell in s["head"]:
            k, v = doc.key(hcell)
            ths.append(f'<th scope="col" data-i18n="{k}">{v}</th>')
        thead = "<thead><tr>" + "".join(ths) + "</tr></thead>"
    rows = []
    for r in s["rows"]:
        tds = []
        for cell in r:
            if isinstance(cell, dict) and "html" in cell:
                tds.append(f'<td class="{cell.get("cls", "")}">{cell["html"]}</td>')
            elif isinstance(cell, dict) and "link" in cell:
                lk, lv = doc.key(cell["text"])
                extra = ' target="_blank" rel="noopener"' if cell["link"].startswith("http") else ""
                attrs = f' data-asset="{cell["asset"]}"' if cell.get("asset") else ""
                tds.append(f'<td><a href="{doc.url(cell["link"])}"{extra}{attrs} data-i18n="{lk}">{lv}</a>'
                           + (f'<div class="muted tiny" >{cell["sub"]}</div>' if cell.get("sub") else "")
                           + "</td>")
            else:
                k, v = doc.key(cell)
                tds.append(f'<td data-i18n="{k}">{v}</td>')
        rows.append("<tr>" + "".join(tds) + "</tr>")
    caption = ""
    if s.get("caption"):
        ck, cv = doc.key(s["caption"])
        caption = f'<caption data-i18n="{ck}">{cv}</caption>'
    tid = f' id="{s["table_id"]}"' if s.get("table_id") else ""
    table_html = (f'<div class="table-wrap reveal"><table class="data"{tid}>'
                  f"{caption}{thead}<tbody>{''.join(rows)}</tbody></table></div>")
    if s.get("note"):
        nk, nv = doc.key(s["note"])
        table_html += f'<p class="table-note" data-i18n="{nk}">{nv}</p>'
    inner = head(doc, s) + table_html
    if s.get("actions"):
        inner += buttons(doc, s["actions"]).replace('class="actions"', 'class="actions" style="margin-top:20px"', 1)
    return wrap(doc, s, inner)


def render_callout(doc: Doc, s: dict[str, Any]) -> str:
    kind = s.get("style", "gold")
    ik = s.get("icon", {"warn": "alert", "tip": "info", "gold": "info"}.get(kind, "info"))
    body = ""
    if s.get("title"):
        k, v = doc.key(s["title"])
        body += f'<p><b data-i18n="{k}">{v}</b></p>'
    for para in s.get("body", []) or []:
        k, v = doc.key(para)
        body += f'<p data-i18n="{k}">{v}</p>'
    if s.get("html"):
        body += s["html"]
    inner = (f'<div class="callout {kind} reveal">{iconbox(ik, 18)}<div>{body}</div></div>')
    return wrap(doc, s, inner)


def render_code(doc: Doc, s: dict[str, Any]) -> str:
    hid = f"code-{doc.pid}-{doc._n}"
    bar = ""
    if s.get("label"):
        lk, lv = doc.key(s["label"])
        ck, cv = doc.key(T("Copy", "Sao chép"))
        dk, dv = doc.key(T("Copied", "Đã chép"))
        bar = (f'<div class="code-head"><span data-i18n="{lk}">{lv}</span>'
               f'<button type="button" class="copy-btn" data-copy="{hid}" data-i18n="{ck}" '
               f'data-copied="{_html.escape(dv, quote=True)}">{cv}</button></div>')
    else:
        ck, cv = doc.key(T("Copy", "Sao chép"))
        dk, dv = doc.key(T("Copied", "Đã chép"))
        bar = (f'<div class="code-head"><span>terminal</span>'
               f'<button type="button" class="copy-btn" data-copy="{hid}" data-i18n="{ck}" '
               f'data-copied="{_html.escape(dv, quote=True)}">{cv}</button></div>')
    code_html = f'<pre class="code" id="{hid}">{s["text"]}</pre>'
    inner = head(doc, s) + f"<div>{bar}{code_html}</div>"
    if s.get("note"):
        nk, nv = doc.key(s["note"])
        inner += f'<p class="table-note" data-i18n="{nk}">{nv}</p>'
    return wrap(doc, s, inner)


def render_cta(doc: Doc, s: dict[str, Any]) -> str:
    k, v = doc.key(s["title"])
    inner = f'<h2 data-i18n="{k}">{v}</h2>'
    if s.get("sub"):
        sk, sv = doc.key(s["sub"])
        inner += f'<p class="sub" data-i18n="{sk}">{sv}</p>'
    inner += buttons(doc, s.get("actions", []), cls="actions center")
    return f'<section class="cta"><div class="container">{inner}</div><div class="keys" aria-hidden="true"></div></section>'


SLIDER_VARIANTS = ("spotlight", "tabs", "steps")


def render_slider(doc: Doc, s: dict[str, Any]) -> str:  # noqa: C901 - one flat template
    """One picture at a time: arrows, a picker and an optional slideshow.

    ``variant`` picks the picker that suits the content:

    * ``spotlight`` - a self-playing showcase; a segmented progress bar is the picker.
    * ``tabs`` - a list of named pages next to the picture; hold still unless asked.
    * ``steps`` - a numbered stepper above the picture for a sequence of actions.

    DOM order matters: the play/pause button comes first so it is the first Tab
    stop inside the region, then the picker/stage in reading order.  Without
    JavaScript the slides simply stack as a list (``.slider:not(.is-ready)``).
    """
    variant = s.get("variant", "spotlight")
    if variant not in SLIDER_VARIANTS:
        raise ValueError(f"unknown slider variant: {variant}")
    items = s["slides"]
    total = len(items)
    if total < 2:
        raise ValueError("a slider needs at least two slides")
    auto = bool(s.get("autoplay", False))
    esc = lambda text: _html.escape(text, quote=True)  # noqa: E731

    slides, nav = [], []
    for i, item in enumerate(items):
        title = item.get("title")
        alt = item.get("alt") or title or item.get("cap") or E(item["shot"])
        pic = picture(doc, item["shot"], alt, lazy=True, badge=item.get("badge"), zoom=True)
        cap_html = ""
        if item.get("cap"):
            ck, cv = doc.key(item["cap"])
            cap_html = f'<figcaption class="lb-caption" data-i18n="{ck}">{cv}</figcaption>'
        slides.append(
            f'<li class="slide" role="group" aria-roledescription="slide" aria-label="{i + 1} / {total}">'
            f'<figure data-lb-item>{pic}{cap_html}</figure></li>'
        )
        if variant == "spotlight":
            nav.append('<button type="button" class="seg"><i></i></button>')
        else:
            tk, tv = doc.key(title)
            label = f'<span class="{"tab" if variant == "tabs" else "step"}-t" data-i18n="{tk}">{tv}</span>'
            if variant == "tabs":
                nav.append(f'<button type="button" class="tab"><span class="tab-n">{i + 1:02d}</span>{label}<i class="fill"></i></button>')
            else:
                nav.append(f'<button type="button" class="step"><span class="step-n">{i + 1}</span>{label}<i class="fill"></i></button>')

    pk, pv = doc.key(UI["ui.car.prev"])
    nk, nv = doc.key(UI["ui.car.next"])
    ck, cv = doc.key(UI["ui.car.choose"])
    lk, lv = doc.key(s.get("label") or UI["ui.car.region"])
    play_label = UI["ui.car.pause" if auto else "ui.car.play"][0]

    # The play/pause label is owned by site.js (it depends on the live state), so
    # it deliberately has no data-i18n-attr.
    play = (f'<button type="button" class="slider-play" aria-label="{esc(play_label)}">'
            f'<span class="ic ic-pause">{icon("pause", 16)}</span><span class="ic ic-play">{icon("play", 16)}</span>'
            f'<span class="slider-play-label">{esc(play_label)}</span></button>')
    arrows = (
        f'<button type="button" class="slider-btn prev" data-i18n-attr="aria-label={pk}" aria-label="{esc(pv)}">{icon("left", 22)}</button>'
        f'<button type="button" class="slider-btn next" data-i18n-attr="aria-label={nk}" aria-label="{esc(nv)}">{icon("right", 22)}</button>'
    )
    # tabs and steps already show their numbers in the picker; the spotlight has bars only
    count = (f'<span class="slider-count" aria-hidden="true"><b>01</b><i>/</i>{total:02d}</span>'
             if variant == "spotlight" else "")
    stage = (
        '<div class="slider-stage"><div class="slider-viewport">'
        f'{arrows}<ul class="slides" aria-live="off">{"".join(slides)}</ul>'
        '</div></div>'
    )
    picker = (f'<div class="slider-nav" role="group" data-i18n-attr="aria-label={ck}" aria-label="{esc(cv)}">'
              f'{"".join(nav)}</div>')
    body = (picker + stage) if variant == "steps" else (stage + picker)

    flags = ' data-stop-on-interact' if s.get("stop_on_interact") else ""
    root = (
        f'<div class="slider slider-{variant} reveal" data-slider data-lightbox '
        f'data-autoplay="{"on" if auto else "off"}" data-interval="{int(s.get("interval", 6000))}"{flags} '
        f'role="region" aria-roledescription="carousel" data-i18n-attr="aria-label={lk}" aria-label="{esc(lv)}">'
        f'{play}{count}{body}</div>'
    )
    out = head(doc, s) + root
    if s.get("actions"):
        out += buttons(doc, s["actions"]).replace('class="actions"', 'class="actions" style="margin-top:22px;justify-content:center"', 1)
    return wrap(doc, s, out, extra_cls="slider-section")


def render_dlhero(doc: Doc, s: dict[str, Any]) -> str:
    main = s["main"]
    rk, rv = doc.key(T("Recommended", "Khuyên dùng"))
    tk, tv = doc.key(main["t"])
    dk, dv = doc.key(main["d"])
    fk, fv = doc.key(main.get("file") or E("Keyflow-Setup-1.0.0.exe"))
    lk, lv = doc.key(main["label"])
    left = (
        '<div class="dl-card reveal">'
        f'<span class="tag-rec" data-i18n="{rk}">{rv}</span>'
        f'<h2 data-i18n="{tk}">{tv}</h2>'
        f'<p class="file" data-i18n="{fk}">{fv}</p>'
        f'<p class="muted" style="margin:12px 0 20px;max-width:56ch" data-i18n="{dk}">{dv}</p>'
        f'<a class="btn btn-gold btn-lg" href="{doc.url(ASSETS["setup"])}" data-asset="setup">'
        f'{icon("download", 18)} <span data-i18n="{lk}">{lv}</span></a>'
        '<div class="badge-row">'
        '<span class="badge">Windows 10 / 11 · x64</span>'
        f'<span class="badge"><span data-release-size="setup">83.2 MiB</span></span>'
        f'<span class="badge">v<span data-release-tag>1.0.0</span></span>'
        f'<span class="badge js-date" data-release-date data-date="2026-10-02T10:10:24Z">2 Oct 2026</span>'
        '</div></div>'
    )
    cards = []
    for c in s.get("side", []):
        ck, cv = doc.key(c["t"])
        sk, sv = doc.key(c["d"])
        ak, av = doc.key(c["label"])
        extra = f' data-asset="{c["asset"]}"' if c.get("asset") else ""
        cards.append(
            f'<div class="dl-mini reveal"><b data-i18n="{ck}">{cv}</b>'
            f'<span data-i18n="{sk}">{sv}</span>'
            f'<a class="btn btn-quiet btn-sm" style="margin-top:8px;justify-self:start" href="{doc.url(c["href"])}"{extra}>'
            f'{icon("download", 15)} <span data-i18n="{ak}">{av}</span></a></div>'
        )
    inner = f'<div class="dl-hero">{left}<div class="dl-side">{"".join(cards)}</div></div>'
    return wrap(doc, s, head(doc, s) + inner)


# ---------------------------------------------------------------------------
# Shared chrome strings: header, drawer, footer, injected UI.
# ---------------------------------------------------------------------------
UI: dict[str, tuple[str, str]] = {
    "ui.skip": T("Skip to content", "Tới nội dung chính"),
    "ui.breadcrumb": T("Breadcrumb", "Đường dẫn trang"),
    "ui.nav.label": T("Main navigation", "Điều hướng chính"),
    "ui.home": T("Home", "Trang chủ"),
    "ui.nav.features": T("Features", "Tính năng"),
    "ui.nav.gallery": T("Gallery", "Hình ảnh"),
    "ui.nav.guide": T("Guide", "Hướng dẫn"),
    "ui.nav.download": T("Download", "Tải về"),
    "ui.nav.cta": T("Get Keyflow", "Tải Keyflow"),
    "ui.nav.prev": T("Previous", "Trang trước"),
    "ui.nav.next": T("Next", "Trang tiếp"),
    "ui.github": T("Keyflow on GitHub", "Keyflow trên GitHub"),
    "ui.lang": T("Language", "Ngôn ngữ"),
    "ui.menu": T("Menu", "Menu"),
    "ui.close": T("Close", "Đóng"),
    "ui.lb.label": T("Image viewer", "Trình xem ảnh"),
    "ui.drawer.label": T("Site menu", "Menu trang web"),
    "ui.allfeatures": T("All features", "Tất cả tính năng"),
    "ui.menu.foot": T("Every feature ships in the same free download — English and Tiếng Việt included.",
                      "Mọi tính năng đều nằm trong cùng một bản tải miễn phí — kèm cả English và Tiếng Việt."),
    "ui.drawer.features": T("Features", "Tính năng"),
    "ui.drawer.pages": T("Pages", "Trang"),
    "ui.car.choose": T("Choose a picture", "Chọn ảnh"),
    "ui.car.region": T("Picture slideshow", "Trình chiếu hình ảnh"),
    "ui.car.prev": T("Previous picture", "Ảnh trước"),
    "ui.car.next": T("Next picture", "Ảnh sau"),
    "ui.car.play": T("Play slideshow", "Phát trình chiếu"),
    "ui.car.pause": T("Pause slideshow", "Tạm dừng trình chiếu"),
    "ui.car.n": T("Picture {n} of {total}", "Ảnh {n} / {total}"),
    "ui.lb.enlarge": T("Enlarge picture", "Phóng to ảnh"),

    "page.home": T("Home", "Trang chủ"),
    "page.gallery": T("Gallery", "Hình ảnh"),
    "page.guide": T("Guide", "Hướng dẫn"),
    "page.download": T("Download", "Tải về"),
    "feature.stage": T("GPU stage & VFX", "Sân khấu GPU & hiệu ứng"),
    "feature.practice": T("Practice & scoring", "Luyện tập & chấm điểm"),
    "feature.sound": T("Sound & MIDI", "Âm thanh & MIDI"),
    "feature.recording": T("Recording & export", "Ghi hình & xuất bản"),
    "feature.design": T("Looks, presets & themes", "Diện mạo, preset & theme"),
    "feature.camera": T("Camera & hand tracking", "Camera & theo dõi bàn tay"),

    "feature.stage.d": T("Direct3D 11 render loop, HDR bloom, 24,000 particles, ray-traced keys",
                         "Vòng lặp vẽ Direct3D 11, bloom HDR, 24.000 hạt, phím ray-tracing"),
    "feature.practice.d": T("Wait-for-note, one hand, A-B loop, history, ghost and staff layer",
                            "Chờ nốt, tập một tay, vòng lặp A-B, lịch sử, bóng luyện tập và khuông nhạc"),
    "feature.sound.d": T("Bundled Yamaha grand, hall reverb, three pedals, MIDI in and out",
                         "Grand Yamaha đi kèm, reverb phòng hoà nhạc, ba pedal, MIDI vào và ra"),
    "feature.recording.d": T("MP4 with the sound inside, AVI, or 32-bit PNG with transparency",
                             "MP4 có sẵn tiếng, AVI, hoặc chuỗi PNG 32-bit trong suốt"),
    "feature.design.d": T("14 presets, three concert themes, theme studio and one-line share codes",
                          "14 preset, ba giao diện hoà nhạc, xưởng theme và mã chia sẻ một dòng"),
    "feature.camera.d": T("Webcam overlay with green key and hand tracking, no model to download",
                          "Lớp phủ webcam có key xanh và theo dõi bàn tay, không cần tải mô hình"),

    "ui.foot.product": T("Product", "Sản phẩm"),
    "ui.foot.resources": T("Resources", "Tài nguyên"),
    "ui.foot.about": T("About", "Giới thiệu"),
    "ui.foot.tagline": T("Piano performance and concert VFX studio for Windows. Play, practise and record from MIDI — free, open documentation, two languages.",
                         "Studio biểu diễn piano và hiệu ứng sân khấu cho Windows. Chơi, luyện tập và quay video từ MIDI — miễn phí, tài liệu mở, hai ngôn ngữ."),
    "ui.foot.changelog": T("Changelog", "Nhật ký thay đổi"),
    "ui.foot.issues": T("Report an issue", "Báo lỗi"),
    "ui.foot.readme": T("Full documentation", "Tài liệu đầy đủ"),
    "ui.foot.releases": T("All releases", "Tất cả bản phát hành"),
    "ui.foot.license": T("MIT licence", "Giấy phép MIT"),
    "ui.foot.soundfont": T("SoundFont credit (FreePats)", "Ghi công SoundFont (FreePats)"),
    "ui.foot.privacy": T("No trackers, no cookies", "Không tracker, không cookie"),
    "ui.foot.authors": T("Authors", "Tác giả"),
    "ui.foot.credits": T(f"© {COPYRIGHT_YEAR} {' · '.join(AUTHORS)}. Keyflow is released under the MIT licence.",
                         f"© {COPYRIGHT_YEAR} {' · '.join(AUTHORS)}. Keyflow được phát hành theo giấy phép MIT."),
    "ui.foot.made": T("Site published with GitHub Pages.", "Trang xuất bản bằng GitHub Pages."),
    "ui.foot.version": T("Version", "Phiên bản"),
    "ui.top": T("Back to top", "Lên đầu trang"),
    "ui.learn": T("Learn more", "Xem chi tiết"),
}


UI_KEY_BY_PAIR: dict[tuple[str, str], str] = {}
for _k, _pair in UI.items():
    UI_KEY_BY_PAIR.setdefault(_pair, _k)


def render_chrome(doc: Doc, active: str, page_title: tuple[str, str]) -> tuple[str, str, str]:
    """Return (header_html, drawer_html, footer_html) for one page."""
    # --- header -------------------------------------------------------------
    feature_links = []
    for path, pid in FEATURES:
        name = UI["feature." + pid]
        desc = UI["feature." + pid + ".d"]
        nk, nv = doc.key(name)
        dk, dv = doc.key(desc)
        current = ' aria-current="page"' if active == pid else ""
        icon_name = {"stage": "chip", "practice": "target", "sound": "wave",
                     "recording": "rec", "design": "palette", "camera": "camera"}[pid]
        feature_links.append(
            f'<a class="menu-item" href="{doc.url(path)}"{current}>{iconbox(icon_name, 18)}'
            f'<span><b data-i18n="{nk}">{nv}</b><span data-i18n="{dk}">{dv}</span></span></a>'
        )
    mk, mv = doc.key(UI["ui.menu"])
    feature_nav_k, feature_nav_v = doc.key(UI["ui.nav.features"])
    gk, gv = doc.key(UI["ui.github"])
    ak, av = doc.key(UI["ui.allfeatures"])
    fk, fv = doc.key(UI["ui.menu.foot"])
    lk, lv = doc.key(UI["ui.lang"])
    cur = lambda pid: ' aria-current="page"' if active == pid else ""  # noqa: E731

    sk_, sv_ = doc.key(UI["ui.skip"])
    gal_k, gal_v = doc.key(UI["ui.nav.gallery"])
    gui_k, gui_v = doc.key(UI["ui.nav.guide"])
    dlo_k, dlo_v = doc.key(UI["ui.nav.download"])
    cls_k, cls_v = doc.key(UI["ui.close"])

    nav_label_key, nav_label_en = doc.key(UI["ui.nav.label"])
    header = f"""
<a class="skip" href="#main" data-i18n="{sk_}">{sv_}</a>
<div class="progress" aria-hidden="true"></div>
<header class="nav">
  <div class="nav-in">
    <a class="brand" href="{doc.url('index.html')}">
      <img src="{doc.root}favicon.svg" width="30" height="30" alt="" decoding="async">
      <span>Keyflow</span><span class="ver">v<span data-release-tag>1.0.0</span></span>
    </a>
    <nav class="nav-links" aria-label="{_html.escape(nav_label_en, quote=True)}" data-i18n-attr="aria-label={nav_label_key}">
      <div class="has-menu">
        <button type="button" class="menu-btn" aria-haspopup="true"><span data-i18n="{feature_nav_k}">{feature_nav_v}</span>
          <span class="caret">{icon('down', 14)}</span></button>
        <div class="menu">
          <div class="menu-grid">{''.join(feature_links)}</div>
          <div class="menu-foot"><span data-i18n="{fk}">{fv}</span>
            <a class="link-more" href="{doc.url('index.html')}#features"><span data-i18n="{ak}">{av}</span>
              <span class="arw">{icon('arrow', 15)}</span></a></div>
        </div>
      </div>
      <a href="{doc.url('gallery.html')}"{cur('gallery')} data-i18n="{gal_k}">{gal_v}</a>
      <a href="{doc.url('guide.html')}"{cur('guide')} data-i18n="{gui_k}">{gui_v}</a>
      <a href="{doc.url('download.html')}"{cur('download')} data-i18n="{dlo_k}">{dlo_v}</a>
    </nav>
    <div class="nav-tools">
      <a class="icon-link" href="{REPO}" target="_blank" rel="noopener" title="GitHub"
         data-i18n-attr="aria-label={gk}" aria-label="{_html.escape(gv, quote=True)}">{icon('github', 18)}</a>
      <div class="lang" role="group" data-i18n-attr="aria-label={lk}" aria-label="{_html.escape(lv, quote=True)}">
        <button type="button" data-lang="en" aria-pressed="true">EN</button>
        <button type="button" data-lang="vi" aria-pressed="false">VI</button>
      </div>
      <a class="btn btn-gold btn-sm" href="{doc.url('download.html')}">{icon('download', 15)} <span data-i18n="{doc.key(UI['ui.nav.cta'])[0]}">{doc.key(UI['ui.nav.cta'])[1]}</span></a>
      <button type="button" class="burger" data-i18n-attr="aria-label={mk}" aria-label="{_html.escape(mv, quote=True)}"
              aria-controls="drawer">{icon('menu', 20)}</button>
    </div>
  </div>
</header>"""

    # --- mobile drawer ------------------------------------------------------
    drawer_key, drawer_label = doc.key(UI["ui.drawer.label"])
    dl = [f'<div class="drawer" id="drawer" role="dialog" aria-modal="true" aria-label="{_html.escape(drawer_label, quote=True)}" data-i18n-attr="aria-label={drawer_key}"><div class="drawer-panel">',
          '<div class="drawer-top"><a class="brand" href="' + doc.url("index.html") + '">',
          f'<img src="{doc.root}favicon.svg" width="28" height="28" alt=""><span>Keyflow</span></a>',
          f'<button type="button" class="drawer-close" data-i18n-attr="aria-label={cls_k}" '
          f'aria-label="{_html.escape(cls_v, quote=True)}">{icon("close", 18)}</button></div>']
    gk2, gv2 = doc.key(UI["ui.drawer.features"])
    dl.append(f'<p class="dgroup" data-i18n="{gk2}">{gv2}</p>')
    for path, pid in FEATURES:
        nk, nv = doc.key(UI["feature." + pid])
        dl.append(f'<a class="dlink dsub" href="{doc.url(path)}"{cur(pid)} data-i18n="{nk}">{nv}</a>')
    pk2, pv2 = doc.key(UI["ui.drawer.pages"])
    dl.append(f'<p class="dgroup" data-i18n="{pk2}">{pv2}</p>')
    for path, pid in [("index.html", "home"), ("gallery.html", "gallery"), ("guide.html", "guide"), ("download.html", "download")]:
        nk, nv = doc.key(UI["page." + pid])
        dl.append(f'<a class="dlink" href="{doc.url(path)}"{cur(pid)} data-i18n="{nk}">{nv}</a>')
    dl.append('<div class="drawer-foot">')
    dl.append(f'<a class="btn btn-gold btn-block" href="{doc.url("download.html")}">{icon("download", 17)} '
              f'<span data-i18n="{dlo_k}">{dlo_v}</span></a>')
    dl.append(f'<a class="btn btn-ghost btn-block" href="{REPO}" target="_blank" rel="noopener">{icon("github", 17)} GitHub</a>')
    dl.append(f'<div class="lang" role="group" style="justify-content:center" data-i18n-attr="aria-label={lk}" aria-label="{_html.escape(lv, quote=True)}">'
              '<button type="button" data-lang="en" aria-pressed="true">EN</button>'
              '<button type="button" data-lang="vi" aria-pressed="false">VI</button></div>')
    dl.append("</div></div></div>")
    drawer = "".join(dl)

    # --- footer -------------------------------------------------------------
    def ul(items: Iterable[tuple[str, tuple[str, str], dict[str, Any]]]) -> str:
        out = []
        for key, label, opts in items:
            lk2, lv2 = doc.key(label)
            href = doc.url(opts["href"])
            ext = ' target="_blank" rel="noopener"' if str(opts.get("href", "")).startswith("http") else ""
            out.append(f'<li><a href="{href}"{ext} data-i18n="{lk2}">{lv2}</a></li>')
        return "<ul>" + "".join(out) + "</ul>"

    hk, hv = doc.key(UI["ui.foot.product"])
    rk, rv = doc.key(UI["ui.foot.resources"])
    ak2, av2 = doc.key(UI["ui.foot.about"])
    tk, tv = doc.key(UI["ui.foot.tagline"])
    ck, cv = doc.key(UI["ui.foot.credits"])
    uak, uav = doc.key(UI["ui.foot.authors"])
    names = "".join(f"<li>{name}</li>" for name in AUTHORS)
    mk2, mv2 = doc.key(UI["ui.foot.made"])
    topk, topv = doc.key(UI["ui.top"])
    gk3, gv3 = doc.key(UI["ui.foot.issues"])

    product = ul([(f"f{i}", UI["feature." + pid], {"href": path}) for i, (path, pid) in enumerate(FEATURES)])
    resources = ul([
        ("r0", UI["ui.nav.gallery"], {"href": "gallery.html"}),
        ("r1", UI["ui.nav.guide"], {"href": "guide.html"}),
        ("r2", UI["ui.nav.download"], {"href": "download.html"}),
        ("r3", UI["ui.foot.changelog"], {"href": CHANGELOG}),
        ("r4", UI["ui.foot.readme"], {"href": README_EN}),
        ("r5", UI["ui.foot.releases"], {"href": RELEASES}),
    ])
    about = ul([
        ("a0", UI["ui.foot.license"], {"href": LICENSE}),
        ("a1", UI["ui.foot.soundfont"], {"href": FREEPATS}),
        ("a2", UI["ui.foot.issues"], {"href": ISSUES}),
        ("a3", UI["ui.foot.privacy"], {"href": "guide.html#privacy"}),
    ])

    footer = f"""
<footer class="foot">
  <div class="container">
    <div class="foot-in">
      <div class="foot-brand">
        <a class="brand" href="{doc.url('index.html')}">
          <img src="{doc.root}favicon.svg" width="30" height="30" alt="" decoding="async"><span>Keyflow</span>
        </a>
        <p data-i18n="{tk}">{tv}</p>
        <div class="social">
          <a href="{REPO}" target="_blank" rel="noopener">{icon('github', 17)} <span data-i18n="{gk}">{gv}</span></a>
          <a href="{ISSUES}" target="_blank" rel="noopener">{icon('alert', 17)} <span data-i18n="{gk3}">{gv3}</span></a>
        </div>
      </div>
      <div><h4 data-i18n="{hk}">{hv}</h4>{product}</div>
      <div><h4 data-i18n="{rk}">{rv}</h4>{resources}</div>
      <div><h4 data-i18n="{ak2}">{av2}</h4>{about}</div>
    </div>
    <div class="credits">
      <p class="credits-label" data-i18n="{uak}">{uav}</p>
      <ul class="credits-names">{names}</ul>
    </div>
    <div class="foot-bottom">
      <span data-i18n="{ck}">{cv}</span>
      <span class="muted tiny" data-i18n="{mk2}">{mv2}</span>
    </div>
  </div>
</footer>
<button type="button" class="totop" data-i18n-attr="aria-label={topk}" aria-label="{_html.escape(topv, quote=True)}">{icon('up', 18)}</button>"""
    return header, drawer, footer


# ---------------------------------------------------------------------------
# Whole page
# ---------------------------------------------------------------------------
JSONLD = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Keyflow",
    "alternateName": "Keyflow · Piano Performance & Concert VFX Studio",
    "applicationCategory": "MultimediaApplication",
    "applicationSubCategory": "Piano performance, practice and video production",
    "operatingSystem": "Windows 10 (22H2) or Windows 11, 64-bit",
    "softwareVersion": "1.0.0",
    "inLanguage": ["en", "vi"],
    "isAccessibleForFree": True,
    "license": LICENSE,
    "downloadUrl": ASSETS["setup"],
    "softwareRequirements": "Direct3D 11 GPU (feature level 11_0, shader model 5.0)",
    "screenshot": f"{SITE_URL}/previews/en/stage-gpu-galaxy.png",
    "author": [{"@type": "Person", "name": name} for name in AUTHORS],
    "copyrightHolder": [{"@type": "Person", "name": name} for name in AUTHORS],
    "copyrightYear": COPYRIGHT_YEAR,
    "featureList": [
        "Direct3D 11 GPU stage with 16-bit HDR and multi-level bloom",
        "Ray-traced 88-key keyboard (GGX, softbox penumbra, ACES tonemap)",
        "Practice modes: follow along, wait for my note, one hand, A-B loop",
        "Recording to MP4 (H.264 + AAC), AVI or 32-bit PNG sequence with alpha",
        "MIDI and MusicXML import, bundled Yamaha grand SoundFont, three pedals",
        "14 stage presets, three concert themes and a user theme studio",
        "Webcam overlay with green key and classical hand tracking",
        "English and Tiếng Việt, switched live without a restart",
    ],
}


def render_page(pid: str, path: str, builder) -> tuple[str, dict[str, str], dict[str, str]]:
    """Render one page and return ``(html, page_vi, shared_vi)``.

    ``builder(doc)`` is the content module's entry point: it receives the page's
    :class:`Doc` (so it can register translations and build ``<picture>`` blocks)
    and returns the page spec.
    """
    depth = path.count("/")
    root = "../" * depth
    doc = Doc(pid, root)
    active = pid
    spec = builder(doc)

    title_en, title_vi = spec["title"]
    desc_en, desc_vi = spec["description"]
    # Metadata is page-specific (the shared chrome dictionary is identical on
    # every page), so keep title/description in this page's own table.
    if title_vi != title_en:
        doc.vi["ui.title"] = title_vi
    if desc_vi != desc_en:
        doc.vi["ui.description"] = desc_vi

    header, drawer, footer = render_chrome(doc, active, spec["title"])
    body = "\n".join(render_section(doc, s) for s in spec["body"])

    canonical = f"{SITE_URL}/{path}" if path != "index.html" else f"{SITE_URL}/"
    og_image = spec.get("og_image", "previews/en/stage-gpu-galaxy.png")
    jsonld = dict(JSONLD)
    jsonld["url"] = canonical
    jsonld["name"] = "Keyflow"
    if pid != "home":
        jsonld = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": title_en,
            "url": canonical,
            "inLanguage": ["en", "vi"],
            "isPartOf": {"@type": "WebSite", "name": "Keyflow", "url": f"{SITE_URL}/"},
            "author": JSONLD["author"],
            "copyrightHolder": JSONLD["copyrightHolder"],
            "copyrightYear": COPYRIGHT_YEAR,
            "about": jsonld,
        }
    trail = spec.get("crumb_trail")
    bc_jsonld = ""
    if trail:
        items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"}]
        for i, (label, href) in enumerate(trail, start=2):
            items.append({"@type": "ListItem", "position": i, "name": label,
                          "item": (f"{SITE_URL}/{href}" if href else None)})
        bc_jsonld = ("\n<script type=\"application/ld+json\">"
                     + json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList",
                                   "itemListElement": items}, ensure_ascii=False)
                     + "</script>")

    html_out = f"""<!doctype html>
<html lang="en" data-root="{root}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title data-i18n="ui.title">{_html.escape(title_en)}</title>
<meta name="description" content="{_html.escape(desc_en, quote=True)}" data-i18n-attr="content=ui.description">
<meta name="author" content="{', '.join(AUTHORS)}">
<meta name="copyright" content="© {COPYRIGHT_YEAR} {', '.join(AUTHORS)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Keyflow">
<meta property="og:title" content="{_html.escape(title_en, quote=True)}" data-i18n-attr="content=ui.title">
<meta property="og:description" content="{_html.escape(desc_en, quote=True)}" data-i18n-attr="content=ui.description">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE_URL}/{og_image}">
<meta property="og:locale" content="en_US">
<meta property="og:locale:alternate" content="vi_VN">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{_html.escape(title_en, quote=True)}" data-i18n-attr="content=ui.title">
<meta name="twitter:description" content="{_html.escape(desc_en, quote=True)}" data-i18n-attr="content=ui.description">
<meta name="theme-color" content="#060504">
<meta name="color-scheme" content="dark">
<link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}style.css">
<script>/* Choose the language before the first paint; a timer lifts the veil if
        the dictionaries or site.js never arrive. */
(function () {{
  try {{
    var s = localStorage.getItem("keyflow-site-lang");
    var q = new URLSearchParams(location.search).get("lang");
    var want = q || s || ((navigator.language || "").toLowerCase().indexOf("vi") === 0 ? "vi" : "en");
    if (want === "vi") {{
      document.documentElement.lang = "vi";
      document.documentElement.setAttribute("data-lang-pref", "vi");
      setTimeout(function () {{ document.documentElement.removeAttribute("data-lang-pref"); }}, 2500);
    }}
  }} catch (e) {{ /* private mode */ }}
}})();</script>
<script defer src="{root}i18n/vi/ui.js"></script>
<script defer src="{root}i18n/vi/{pid}.js"></script>
<script defer src="{root}site.js"></script>
<script defer src="{root}stardust.js"></script>
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False, indent=1)}</script>{bc_jsonld}
</head>
<body>
{header}
{drawer}
<main id="main">
{body}
</main>
{footer}
</body>
</html>
"""
    return html_out, doc.vi, doc.shared


def write_vi_js(table: dict[str, str]) -> str:
    """A dictionary file that merges itself into ``window.KEYFLOW_VI``."""
    body = json.dumps(table, ensure_ascii=False, indent=0, sort_keys=True)
    return ("/* Generated by tools/build.py — edit the content modules, not this file. */\n"
            "window.KEYFLOW_VI = Object.assign(window.KEYFLOW_VI || {}, " + body + ");\n")

#!/usr/bin/env python3
"""Build the Keyflow static marketing site.

No packages or bundler are required.  Run from anywhere:

    python3 tools/build.py
    python3 tools/build.py --check

The canonical content is kept in the small Python modules next to this file;
this script renders the HTML and per-page Vietnamese dictionaries.
"""
from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import content_home  # noqa: E402
import content_features  # noqa: E402
import content_studio  # noqa: E402
import content_more  # noqa: E402
from sitekit import SITE_URL, UI, render_page, write_vi_js  # noqa: E402

PAGES = [
    ("home", "index.html", content_home.build),
    ("stage", "features/stage.html", content_features.build_stage),
    ("practice", "features/practice.html", content_features.build_practice),
    ("sound", "features/sound.html", content_features.build_sound),
    ("recording", "features/recording.html", content_studio.build_recording),
    ("design", "features/design.html", content_studio.build_design),
    ("camera", "features/camera.html", content_studio.build_camera),
    ("gallery", "gallery.html", content_more.build_gallery),
    ("guide", "guide.html", content_more.build_guide),
    ("download", "download.html", content_more.build_download),
]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="report stale generated files without writing")
    args = ap.parse_args()

    ROOT.mkdir(parents=True, exist_ok=True)
    translations: dict[str, dict[str, str]] = {}
    shared_tables: list[tuple[str, dict[str, str]]] = []
    outputs: dict[Path, str] = {}
    errors: list[str] = []

    for pid, path, builder in PAGES:
        html, page_vi, shared_vi = render_page(pid, path, builder)
        out = ROOT / path
        outputs[out] = html
        translations[pid] = page_vi
        shared_tables.append((pid, shared_vi))

    # The shared chrome dictionary is independent of page composition.  Ship
    # the complete UI catalogue so breadcrumb and previous/next labels remain
    # available on every route even where that control is not rendered.
    baseline = {key: pair[1] for key, pair in UI.items()}
    for pid, table in shared_tables:
        for key, value in table.items():
            if key not in baseline or baseline[key] != value:
                errors.append(f"shared UI string mismatch on {pid}: {key}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 2

    outputs[ROOT / "i18n" / "vi" / "ui.js"] = write_vi_js(baseline)
    for pid, _, _ in PAGES:
        outputs[ROOT / "i18n" / "vi" / f"{pid}.js"] = write_vi_js(translations[pid])

    urls = [f"{SITE_URL}/" if path == "index.html" else f"{SITE_URL}/{path}" for _, path, _ in PAGES]
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap.extend(f"  <url><loc>{url}</loc><lastmod>2026-10-03</lastmod></url>" for url in urls)
    sitemap.append("</urlset>")
    outputs[ROOT / "sitemap.xml"] = "\n".join(sitemap) + "\n"
    outputs[ROOT / "robots.txt"] = f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n"

    # Ensure a route never silently overwrites another route's generated file.
    if len(outputs) != len(PAGES) + 1 + len(PAGES) + 2:
        print("duplicate generated output path", file=sys.stderr)
        return 2

    changed: list[Path] = []
    for path, text in outputs.items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != text:
            changed.append(path)
            if args.check:
                if current is None:
                    print(f"missing: {path.relative_to(ROOT)}")
                else:
                    print(f"stale: {path.relative_to(ROOT)}")
                    diff = difflib.unified_diff(current.splitlines(), text.splitlines(),
                                                fromfile="current", tofile="generated", n=1)
                    for line in list(diff)[:32]:
                        print(line)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
                print(f"wrote {path.relative_to(ROOT)}")

    if args.check:
        if changed:
            print(f"\n{len(changed)} generated file(s) are stale")
            return 1
        print(f"all {len(outputs)} generated files are current")
        return 0

    print(f"\nbuilt {len(PAGES)} pages and {len(PAGES) + 1} Vietnamese dictionaries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

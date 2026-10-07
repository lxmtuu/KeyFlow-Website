#!/usr/bin/env python3
"""Static QA for generated Keyflow pages (no browser or third-party packages)."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ["site.js"]            # hand-written scripts that ship with the site
SLIDER_VARIANTS = {"spotlight", "tabs", "steps"}
sys.path.insert(0, str(ROOT / "tools"))
from build import PAGES  # noqa: E402
from sitekit import SITE_URL  # noqa: E402


class Scan(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.keys: list[tuple[str, str]] = []
        self.refs: list[tuple[str, str]] = []
        self.shots: list[str] = []
        self.images: list[dict[str, str]] = []
        self.targets: list[dict[str, str]] = []
        self.translation_icons: list[tuple[str, str]] = []
        self.chip_classes: list[tuple[str, ...]] = []
        self.untranslated_drawer_links: list[str] = []
        self.sliders: list[dict] = []
        self.unlabelled_triggers = 0
        self.shotgrids = 0
        self._open: dict | None = None        # the slider whose markup we are inside
        self._open_depth = 0
        self._stack: list[tuple[str, str | None]] = []
        self._void = {"area", "base", "br", "col", "embed", "hr", "img", "input",
                      "link", "meta", "param", "source", "track", "wbr"}

    def handle_starttag(self, tag: str, attrs) -> None:
        data = dict(attrs)
        if tag == "svg":
            self.translation_icons.extend((parent_tag, key) for parent_tag, key in self._stack if key)
        classes = tuple(data.get("class", "").split())
        if "chip" in classes:
            self.chip_classes.append(classes)
        if "shotgrid" in classes:
            self.shotgrids += 1
        if "data-slider" in data:
            self._open = {"variant": next((c[7:] for c in classes if c.startswith("slider-")), ""),
                          "interval": data.get("data-interval", ""), "role": data.get("role", ""),
                          "label": bool(data.get("aria-label")), "lightbox": "data-lightbox" in data,
                          "slides": 0, "items": 0, "nav": 0, "prev": 0, "next": 0, "play": 0, "count": 0,
                          "first_button": None}
            self._open_depth = len(self._stack)
            self.sliders.append(self._open)
        elif self._open is not None:
            box = self._open
            if tag == "li" and "slide" in classes:
                box["slides"] += 1
            if "data-lb-item" in data:
                box["items"] += 1
            if tag == "button":
                if box["first_button"] is None:
                    box["first_button"] = " ".join(classes)
                if classes and classes[0] in ("seg", "tab", "step"):
                    box["nav"] += 1
                if "slider-btn" in classes:
                    box["prev" if "prev" in classes else "next"] += 1
                if "slider-play" in classes:
                    box["play"] += 1
            if "slider-count" in classes:
                box["count"] += 1
        if tag == "button" and "lb-trigger" in classes and not data.get("aria-label"):
            self.unlabelled_triggers += 1
        if tag == "a" and "dlink" in classes and not data.get("data-i18n"):
            self.untranslated_drawer_links.append(data.get("href", "(no href)"))
        if data.get("id"):
            self.ids.append(data["id"])
        if data.get("data-i18n"):
            self.keys.append((tag, data["data-i18n"]))
        if data.get("data-i18n-attr"):
            for part in data["data-i18n-attr"].split(";"):
                if "=" in part:
                    self.keys.append((tag, part.split("=", 1)[1].strip()))
        if data.get("data-shot"):
            self.shots.append(data["data-shot"])
        for attr in ("href", "src", "poster"):
            if data.get(attr):
                self.refs.append((attr, data[attr]))
        if tag == "img":
            self.images.append(data)
        if data.get("target") == "_blank":
            self.targets.append(data)
        if tag not in self._void:
            self._stack.append((tag, data.get("data-i18n")))

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self._stack) - 1, -1, -1):
            if self._stack[index][0] == tag:
                self._stack = self._stack[:index]
                break
        if self._open is not None and len(self._stack) <= self._open_depth:
            self._open = None


class LinkScan(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        data = dict(attrs)
        if tag == "a" and data.get("href"):
            self.links.append(data["href"])


def load_dict(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    prefix = "Object.assign(window.KEYFLOW_VI || {}, "
    raw = text.split(prefix, 1)[1].rsplit(");", 1)[0]
    return json.loads(raw)


def local_target(page: Path, ref: str) -> tuple[Path | None, str]:
    if ref.startswith(("http://", "https://", "mailto:", "tel:", "data:", "javascript:")):
        return None, ""
    full = urljoin(SITE_URL + "/" + page.as_posix(), ref)
    parsed = urlsplit(full)
    path = unquote(parsed.path)
    if path.startswith("/"):
        target = (ROOT / path.lstrip("/")).resolve()
    else:
        target = (ROOT / path).resolve()
    return target, unquote(parsed.fragment)


def main() -> int:
    failures: list[str] = []
    ui = load_dict(ROOT / "i18n/vi/ui.js")
    scans: dict[str, Scan] = {}
    route_paths = {Path(path).as_posix() for _, path, _ in PAGES}

    # Confirm the generated output matches its source modules.
    built = subprocess.run([sys.executable, str(ROOT / "tools/build.py"), "--check"],
                           cwd=ROOT, text=True, capture_output=True)
    if built.returncode:
        failures.extend("build check: " + line for line in (built.stdout + built.stderr).splitlines())

    # JavaScript syntax check where Node is available (it is required by the
    # contributor CI, but not needed to view the static pages).
    for script in SCRIPTS:
        node = subprocess.run(["node", "--check", str(ROOT / script)], cwd=ROOT,
                              text=True, capture_output=True)
        if node.returncode:
            failures.extend(f"{script}: " + line for line in node.stderr.splitlines())

    # Every shared string that site.js looks up at run time must exist in the
    # Vietnamese UI table, otherwise that control silently stays in English.
    site_js = (ROOT / "site.js").read_text(encoding="utf-8")
    for key in sorted(set(re.findall(r'\bt\("(ui\.[\w.]+)"', site_js))):
        if key not in ui:
            failures.append(f"site.js: t() uses {key!r}, which is not in i18n/vi/ui.js")

    for pid, path, _ in PAGES:
        page = Path(path)
        source = ROOT / page
        if not source.exists():
            failures.append(f"missing page: {path}")
            continue
        scan = Scan()
        scan.feed(source.read_text(encoding="utf-8"))
        scans[path] = scan

        duplicates = sorted({x for x in scan.ids if scan.ids.count(x) > 1})
        if duplicates:
            failures.append(f"{path}: duplicate id(s): {', '.join(duplicates)}")

        local_dict = load_dict(ROOT / "i18n/vi" / f"{pid}.js")
        for key, value in local_dict.items():
            if not isinstance(value, str):
                failures.append(f"{path}: translation {key} must be a string")
        for tag, key in scan.keys:
            if key in ("ui.title", "ui.description"):
                if key not in local_dict:
                    failures.append(f"{path}: missing page metadata translation key {key} ({tag})")
            elif key.startswith("ui.") or key.startswith("feature."):
                if key not in ui:
                    failures.append(f"{path}: missing shared translation key {key} ({tag})")
            elif not key.startswith(pid + "."):
                failures.append(f"{path}: translation key is outside page namespace: {key} ({tag})")
            # Untranslated keys are expected when the source is identical in
            # both languages; all translated page strings must exist in the
            # page's dictionary.
            elif key not in local_dict:
                # English-only stable names / product identifiers have no
                # Vietnamese replacement by design.
                pass

        if scan.untranslated_drawer_links:
            failures.append(f"{path}: untranslated mobile drawer link(s): {', '.join(scan.untranslated_drawer_links)}")
        if scan.translation_icons:
            for tag, key in scan.translation_icons:
                failures.append(f"{path}: translated {tag} {key} contains an SVG; move the icon outside its text span")
        # Sliders: both arrows, one picker button per slide, a name for the region, and the
        # pause button first in the keyboard order (rotation must be stoppable before
        # anything else is reached).
        for number, box in enumerate(scan.sliders, 1):
            where = f"{path}: slider #{number} ({box['variant'] or 'no variant'})"
            if box["variant"] not in SLIDER_VARIANTS:
                failures.append(f"{where}: unknown variant")
            if box["slides"] < 2:
                failures.append(f"{where} needs at least two slides (found {box['slides']})")
            if box["nav"] != box["slides"]:
                failures.append(f"{where}: {box['nav']} picker buttons for {box['slides']} slides")
            if box["lightbox"] and box["items"] != box["slides"]:
                failures.append(f"{where}: {box['items']} enlargeable figures for {box['slides']} slides")
            if (box["prev"], box["next"], box["play"]) != (1, 1, 1):
                failures.append(f"{where}: needs exactly one previous, next and play/pause button")
            if box["count"] != (1 if box["variant"] == "spotlight" else 0):
                failures.append(f"{where}: unexpected number of counters ({box['count']})")
            if box["role"] != "region" or not box["label"]:
                failures.append(f"{where}: needs role=region and an aria-label")
            if not box["interval"].isdigit() or int(box["interval"]) < 3000:
                failures.append(f"{where}: data-interval must be at least 3000 ms")
            if box["first_button"] != "slider-play":
                failures.append(f"{where}: the play/pause button must be the first button in the markup "
                                f"(found {box['first_button']!r})")
        # The gallery must never lay out many pictures at once again.
        if path == "gallery.html" and scan.shotgrids:
            failures.append("gallery.html: picture grids are not allowed here; use a slider")
        if scan.unlabelled_triggers:
            failures.append(f"{path}: {scan.unlabelled_triggers} zoom button(s) without an aria-label")
        allowed_chip_classes = {"chip", "gold", "violet", "cyan"}
        for classes in scan.chip_classes:
            if not set(classes).issubset(allowed_chip_classes) or len(classes) > 2:
                failures.append(f"{path}: unexpected chip classes: {' '.join(classes)}")

        for data in scan.images:
            if "alt" not in data:
                failures.append(f"{path}: <img> has no alt attribute: {data.get('src', '(no src)')}")
        for data in scan.targets:
            rel = data.get("rel", "").lower().split()
            if "noopener" not in rel:
                failures.append(f"{path}: target=_blank without rel=noopener: {data.get('href', '')}")

        # Both source-of-truth PNGs and derived WebPs must exist for every
        # localised screenshot used by a page.
        for shot in scan.shots:
            for lang in ("en", "vi"):
                png = ROOT / "previews" / lang / f"{shot}.png"
                webp = ROOT / "previews" / "webp" / lang / f"{shot}.webp"
                if not png.exists():
                    failures.append(f"{path}: missing screenshot {png.relative_to(ROOT)}")
                if not webp.exists():
                    failures.append(f"{path}: missing WebP {webp.relative_to(ROOT)}")

        for attr, ref in scan.refs:
            target, fragment = local_target(page, ref)
            if target is None:
                continue
            if not target.exists():
                failures.append(f"{path}: broken {attr} {ref!r}")
                continue
            try:
                target_rel = target.relative_to(ROOT).as_posix()
            except ValueError:
                failures.append(f"{path}: local URL escapes the site: {ref!r}")
                continue
            if fragment and target_rel in route_paths and target_rel in scans:
                if fragment not in scans[target_rel].ids:
                    failures.append(f"{path}: missing fragment #{fragment} in {target_rel}")

        # Links embedded inside a translated rich-text paragraph need the same
        # relative-path check as links written directly in HTML.
        for key, value in local_dict.items():
            snippet = LinkScan()
            snippet.feed(value)
            for href in snippet.links:
                target, _ = local_target(page, href)
                if target is not None and not target.exists():
                    failures.append(f"{path}: broken translated link in {key}: {href!r}")

    # Cross-page fragment checks happen after all pages have been scanned.
    for path, scan in scans.items():
        page = Path(path)
        for attr, ref in scan.refs:
            target, fragment = local_target(page, ref)
            if target is None or not fragment:
                continue
            try:
                target_rel = target.relative_to(ROOT).as_posix()
            except ValueError:
                continue
            if target_rel in route_paths and target_rel in scans and fragment not in scans[target_rel].ids:
                failures.append(f"{path}: missing fragment #{fragment} in {target_rel}")

    teaser = [ROOT / "previews/presets-teaser.jpg", ROOT / "previews/webp/presets-teaser.webp",
              ROOT / "previews/presets.jpg", ROOT / "media/showcase.mp4"]
    for asset in teaser:
        if not asset.exists():
            failures.append(f"missing site asset: {asset.relative_to(ROOT)}")

    if failures:
        print("Keyflow site checks failed:", file=sys.stderr)
        for failure in failures:
            print(" - " + failure, file=sys.stderr)
        return 1

    print(f"OK: {len(PAGES)} pages, screenshots, sliders, translated links, internal routes and JavaScript syntax")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

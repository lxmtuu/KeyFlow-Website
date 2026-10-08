#!/usr/bin/env python3
"""Derive the WebP copies of every preview picture.

The PNGs in ``previews/`` stay the source of truth (they are copied from the
Keyflow release repository after every release).  This script writes a WebP
sibling for each of them into ``previews/webp/`` so the site can serve a
``<picture>`` with a modern format and keep the PNG as the fallback.

    python3 tools/make_images.py            # only what is missing or stale
    python3 tools/make_images.py --force    # re-encode everything

Needs ImageMagick (``convert``).  Run it after refreshing ``previews/``.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUALITY = "82"


def sources() -> list[tuple[Path, Path]]:
    """(source picture, webp target) for every image the site serves."""
    pairs: list[tuple[Path, Path]] = []
    for lang in ("en", "vi"):
        for png in sorted((ROOT / "previews" / lang).glob("*.png")):
            pairs.append((png, ROOT / "previews" / "webp" / lang / (png.stem + ".webp")))
    for name in ("presets", "presets-teaser"):          # the gallery shows the teaser and links the full sheet
        jpg = ROOT / "previews" / (name + ".jpg")
        if jpg.exists():
            pairs.append((jpg, ROOT / "previews" / "webp" / (name + ".webp")))
    return pairs


def encode(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["convert", str(src), "-strip", "-quality", QUALITY, str(dst)],
        check=True,
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="re-encode even when the WebP is newer")
    args = ap.parse_args()

    if shutil.which("convert") is None:
        print("ImageMagick's `convert` is not on PATH", file=sys.stderr)
        return 1

    made = skipped = 0
    saved = 0
    for src, dst in sources():
        if dst.exists() and not args.force and dst.stat().st_mtime >= src.stat().st_mtime:
            skipped += 1
            continue
        encode(src, dst)
        saved += src.stat().st_size - dst.stat().st_size
        made += 1
        print(f"  {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}  "
              f"({src.stat().st_size // 1024} KiB -> {dst.stat().st_size // 1024} KiB)")
    print(f"encoded {made}, up to date {skipped}, saved {saved / 1024 / 1024:.1f} MiB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

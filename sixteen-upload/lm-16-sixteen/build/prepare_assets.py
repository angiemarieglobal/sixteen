#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prepares the Sixteen banner for the PDF cover and the web hero.

THE ASSET LAW (locked 27 July 2026, amg-brand-boards) is enforced here rather than
in the document. The cream fade at the bottom of the banner is burned into the
pixels before the image ever reaches the PDF, so the finished file contains no
shading, no soft mask and no transparency group. That is the whole reason a magenta
stripe cannot happen to this asset.

Output is JPEG, not PNG. A DCTDecode RGB image cannot carry an alpha channel at all,
which makes the law structurally impossible to break, and it takes the PDF from
2.6MB down to something that survives a corporate mail server.

Usage: python3 prepare_assets.py path/to/banner.png
"""

import os
import sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
WEB = os.path.join(HERE, "..", "..", "docs", "sixteen")

PALE_OAT = (0xFB, 0xF7, 0xEE)      # the page the banner has to join
FADE_FRACTION = 0.22               # how much of the base melts into the page
PDF_WIDTH = 1500                   # ~2.5x the placed width on A4, print sharp
PDF_QUALITY = 88
WEB_QUALITY = 86


def bake_fade(im):
    """Burn the fade into the raster. No alpha anywhere, ever."""
    w, h = im.size
    px = im.load()
    fade_h = int(h * FADE_FRACTION)
    start = h - fade_h
    for y in range(start, h):
        t = (y - start) / (fade_h - 1)
        t = t * t * (3 - 2 * t)                    # smoothstep, gentle at the seam
        for x in range(w):
            r, g, b = px[x, y]
            px[x, y] = (int(r + (PALE_OAT[0] - r) * t),
                        int(g + (PALE_OAT[1] - g) * t),
                        int(b + (PALE_OAT[2] - b) * t))
    return im


def main():
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python3 prepare_assets.py path/to/banner.png")
    src = sys.argv[1]
    os.makedirs(ASSETS, exist_ok=True)
    os.makedirs(WEB, exist_ok=True)

    base = Image.open(src).convert("RGB")          # convert drops any alpha channel
    w, h = base.size

    cover = bake_fade(base.copy())
    cover = cover.resize((PDF_WIDTH, round(PDF_WIDTH * h / w)), Image.LANCZOS)
    cover_path = os.path.join(ASSETS, "sixteen-cover.jpg")
    cover.save(cover_path, "JPEG", quality=PDF_QUALITY, optimize=True,
               subsampling=0, progressive=False)

    hero_path = os.path.join(WEB, "sixteen-hero.jpg")
    base.save(hero_path, "JPEG", quality=WEB_QUALITY, optimize=True, progressive=True)

    for p in (cover_path, hero_path):
        print(f"  {os.path.basename(p)}  {round(os.path.getsize(p)/1024,1)} KB")
    print("no alpha, no shading, plain RGB. the law holds.")


if __name__ == "__main__":
    main()

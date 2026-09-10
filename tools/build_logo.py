# -*- coding: utf-8 -*-
"""Turn the supplied 8K brand logos into transparent, web-sized assets.

The source files are flat RGB with a solid background, so the background is
keyed out by colour distance and the edge pixels are un-premultiplied. That
keeps the anti-aliasing clean instead of leaving an ivory or navy halo.
"""
from PIL import Image
import numpy as np
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "brand")

SOURCES = [
    # slug,          file,                          fallback ink for the halo test
    ("logo",       "HST-Primary-Logo-8K.png"),      # navy artwork on ivory
    ("logo-light", "HST-Secondary-Logo-8K.png"),    # ivory artwork on navy
]
CANDIDATE_DIRS = [os.path.join(ROOT, "source"), os.path.expanduser("~/Desktop")]
WIDTHS = [1200, 640, 320]


def find(name):
    for d in CANDIDATE_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    return None


def key_out(im, tol=42.0, soft=26.0, inset=8):
    """Return RGBA with the flat background removed.

    The sources carry a thin drawn border around the canvas, so a few pixels are
    cropped off every edge before the background colour is sampled.
    """
    im = im.convert("RGB").crop((inset, inset, im.width - inset, im.height - inset))
    a = np.asarray(im).astype(np.float32)
    h, w, _ = a.shape
    # background colour = median of a border band, which is always empty canvas
    band = np.concatenate([a[:8].reshape(-1, 3), a[-8:].reshape(-1, 3),
                           a[:, :8].reshape(-1, 3), a[:, -8:].reshape(-1, 3)])
    bg = np.median(band, axis=0)

    dist = np.sqrt(((a - bg) ** 2).sum(axis=2))
    alpha = np.clip((dist - tol) / soft, 0.0, 1.0)

    # un-premultiply so semi-transparent edge pixels do not carry the background
    al = alpha[..., None]
    with np.errstate(divide="ignore", invalid="ignore"):
        rgb = np.where(al > 0.004, (a - bg * (1.0 - al)) / np.maximum(al, 1e-4), a)
    rgb = np.clip(rgb, 0, 255)

    out = np.dstack([rgb, alpha * 255.0]).astype(np.uint8)
    return Image.fromarray(out, "RGBA"), bg


def trim(im, pad_ratio=0.03, min_run=12):
    """Crop to the artwork, ignoring isolated specks along the edges."""
    mask = np.asarray(im.getchannel("A")) > 8
    rows = np.where(mask.sum(axis=1) > min_run)[0]
    cols = np.where(mask.sum(axis=0) > min_run)[0]
    if not len(rows) or not len(cols):
        return im
    t, b = int(rows.min()), int(rows.max()) + 1
    l, r = int(cols.min()), int(cols.max()) + 1
    pad = int(round(max(r - l, b - t) * pad_ratio))
    return im.crop((max(0, l - pad), max(0, t - pad),
                    min(im.width, r + pad), min(im.height, b + pad)))


def main():
    os.makedirs(OUT, exist_ok=True)
    made = []
    for slug, fname in SOURCES:
        src = find(fname)
        if not src:
            sys.exit(f"'{fname}' not found. Looked in:\n  " + "\n  ".join(CANDIDATE_DIRS))
        im = Image.open(src)
        keyed, bg = key_out(im)
        keyed = trim(keyed)
        for w in WIDTHS:
            h = round(keyed.height * w / keyed.width)
            r = keyed.resize((w, h), Image.LANCZOS)
            r.save(os.path.join(OUT, f"{slug}-{w}.webp"), "WEBP", quality=92, method=6, exact=True)
            if w == WIDTHS[0]:
                r.save(os.path.join(OUT, f"{slug}.png"), "PNG", optimize=True)
        made.append(f"{slug}  {keyed.width}x{keyed.height}  bg={tuple(int(v) for v in bg)}  <- {fname}")
    # app icon: the real mark on the brand navy, square, opaque (iOS masks it itself)
    mark = Image.open(os.path.join(OUT, "logo-light.png")).convert("RGBA")
    for size, name in ((180, "apple-touch-icon.png"), (512, "icon-512.png")):
        canvas = Image.new("RGB", (size, size), "#182331")
        w = int(size * 0.80)
        h = round(mark.height * w / mark.width)
        m = mark.resize((w, h), Image.LANCZOS)
        canvas.paste(m, ((size - w) // 2, (size - h) // 2), m)
        canvas.save(os.path.join(ROOT, name), "PNG", optimize=True)
    made.append("apple-touch-icon.png + icon-512.png from the secondary mark")

    print("OK")
    for m in made:
        print("  +", m)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Prepare the supplied architectural plan drawings for use as background texture.

The client supplied a transparent PNG set, each drawing in two inks: graphite for
the light theme and white for the dark one. This script trims, resizes and
re-encodes them as WebP at the width the layout actually paints them, and reports
where the ink sits in each frame so the drawing can be placed on the side of a
section that is genuinely empty.

Each drawing is a single flat ink colour over transparency, so the colour channels
are flattened to that one value before encoding. That leaves the alpha channel as
the only real content, and a drawing painted at 22-30% opacity tolerates a lossy
alpha. Together the two cut the set from 2.3 MB to well under a third of that.

Put the set in `source/blueprints/` (git-ignored, they are client assets) or leave
it where it was delivered, then run:

    python tools/build_plans.py
"""
from PIL import Image
import numpy as np
import os, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "plans")

CANDIDATE_DIRS = [
    os.path.join(ROOT, "source", "blueprints"),
    os.path.expanduser("~/Desktop/architectural-blueprint-transparent-complete-set"),
]

# Painted at most ~560px wide in a section, ~980px for the centred slot, so 1100
# covers both at 2x without carrying pixels nothing will ever show.
WIDTH = 1100

# The alpha channel carries the whole drawing once the colour is flat, and these
# are painted at 22-30% opacity, so a lossy alpha costs nothing anyone can see.
ALPHA_Q = 70

# source stem -> slug. The stems come from the delivered file names.
PLANS = {
    "architectural-blueprint":                    "atrium",
    "architectural-blueprint-02-orthogonal":      "orthogonal",
    "architectural-blueprint-03-diagonal":        "diagonal",
    "architectural-blueprint-04-courtyard":       "courtyard",
    "architectural-blueprint-05-curved":          "curved",
    "architectural-blueprint-06-dual-fragments":  "dual",
    "architectural-blueprint-07-minimal-corner":  "corner",
}

# delivered ink name -> the theme the file is used on
INKS = {"graphite": "light", "white": "dark"}


def find_dir():
    for d in CANDIDATE_DIRS:
        if os.path.isdir(d):
            return d
    sys.exit("Blueprint set not found. Looked in:\n  " + "\n  ".join(CANDIDATE_DIRS))


def flatten_ink(im):
    """Replace the colour channels with the single ink colour the drawing uses.

    The delivered artwork is one flat colour throughout, so this changes nothing
    visible, but it leaves the encoder with a constant to compress instead of
    per-pixel noise from the original rasteriser."""
    a = np.asarray(im).copy()
    solid = a[..., 3] > 200
    if not solid.any():
        return im
    ink = np.median(a[..., :3][solid], axis=0).astype(np.uint8)
    a[..., :3] = ink
    return Image.fromarray(a, "RGBA")


def ink_bias(im):
    """Where does the drawing actually sit? Returns the horizontal centre of mass
    of the ink, 0 = hard left, 1 = hard right."""
    a = np.asarray(im.getchannel("A"), dtype=np.float32)
    total = a.sum()
    if total <= 0:
        return 0.5, 0.0
    xs = np.arange(a.shape[1], dtype=np.float32)
    cx = float((a.sum(axis=0) * xs).sum() / total) / a.shape[1]
    coverage = float((a > 8).mean())
    return cx, coverage


def main():
    src_dir = find_dir()
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith((".svg", ".webp", ".png")):
            os.remove(os.path.join(OUT, f))

    report, total = {}, 0
    for stem, slug in PLANS.items():
        for ink, theme in INKS.items():
            name = f"{stem}-{ink}-transparent.png"
            path = os.path.join(src_dir, name)
            if not os.path.exists(path):
                sys.exit(f"missing source: {name}")

            im = Image.open(path).convert("RGBA")
            # trim fully transparent margins so the drawing fills its box
            bbox = im.getchannel("A").point(lambda v: 255 if v > 4 else 0).getbbox()
            if bbox:
                im = im.crop(bbox)

            h = round(im.height * WIDTH / im.width)
            im = im.resize((WIDTH, h), Image.LANCZOS)
            im = flatten_ink(im)
            dest = os.path.join(OUT, f"plan-{slug}-{theme}.webp")
            im.save(dest, "WEBP", quality=80, alpha_quality=ALPHA_Q, method=6, exact=True)
            total += os.path.getsize(dest)

            if theme == "light":
                cx, cov = ink_bias(im)
                side = "left" if cx < 0.42 else "right" if cx > 0.58 else "centre"
                report[slug] = {"w": WIDTH, "h": h, "ink_x": round(cx, 2),
                                "coverage": round(cov * 100, 1), "sits": side}

    with open(os.path.join(OUT, "plans.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1, sort_keys=True)

    print(f"OK  {len(PLANS)} plans x 2 inks  ({total / 1024 / 1024:.2f} MB total)")
    for slug, m in sorted(report.items()):
        print(f"  + plan-{slug:11} {m['w']}x{m['h']:<5} ink sits {m['sits']:6} "
              f"(x={m['ink_x']}, {m['coverage']}% coverage)")


if __name__ == "__main__":
    main()

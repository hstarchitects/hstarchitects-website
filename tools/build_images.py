# -*- coding: utf-8 -*-
"""Extract and optimise project photography straight from the source company profiles.

Reproducible by design: every image is addressed as (document, page, index) inside
the original PDFs, so a fresh checkout can regenerate the whole asset set.

Put the two profile PDFs in `source/` (git-ignored, they are client documents) or
point SOURCES at wherever they live, then run:

    python tools/build_images.py

Attribution rule: a slug names the project the photograph actually belongs to.
Images from the profiles' "Our 3D Design" pages are prefixed `render-` and must
never be presented as delivered work.
"""
from PIL import Image, ImageOps, ImageFilter
import io, os, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img")

# Where the source PDFs live. First existing path wins.
SOURCES = {
    "hst": [os.path.join(ROOT, "source", "HST GROUP PROFILE.pdf"),
            os.path.expanduser("~/Desktop/HST GROUP PROFILE.pdf")],
    "el":  [os.path.join(ROOT, "source", "company profile ELEGANT LINES.pdf"),
            os.path.expanduser("~/Desktop/company profile ELEGANT LINES.pdf")],
}

WIDTHS = [1920, 1280, 800, 480]
# Full-bleed heroes get a sharpened upscale rather than a soft stretch.
UPSCALE = {"hero-pool-dusk", "hero-pergola-lounge", "hero-architecture-dark"}

# slug -> (document, page number (1-based), image index on that page, category)
#
# Page captions from the source profiles are noted so attribution stays checkable.
CURATED = {
    # ---------- heroes ----------
    "hero-pool-dusk":        ("el",  30, 0, "hero"),      # GARDEN, DUBAI-DISTRICT ONE
    "hero-pergola-lounge":   ("el",  31, 0, "hero"),      # ROOF GARDEN, DUBAI-DISTRICT ONE
    "hero-office-skyline":   ("el",  10, 0, "hero"),      # OFFICE RENOVATION, DUBAI
    "hero-architecture-dark":("hst",  2, 2, "hero"),      # company overview

    # ---------- interior design ----------
    "interior-lounge-seaview":  ("hst",  3, 1, "services"),
    "interior-marble-lobby":    ("el",  13, 0, "services"),
    "interior-curved-living":   ("el",  15, 1, "services"),   # PRIVATE VILLA, DUBAI-JUMEIRAH
    "interior-loft-living":     ("el",  14, 0, "services"),
    "interior-styled-living":   ("el",  21, 0, "services"),
    "interior-kitchen-brass":   ("el",  19, 0, "services"),   # KITCHEN RENOVATION
    "interior-corridor-gold":   ("el",   8, 0, "services"),   # OFFICE RENOVATION, DUBAI
    "interior-corridor-white":  ("el",   9, 1, "services"),
    "interior-bath-marble":     ("hst", 15, 1, "services"),   # PRIVATE VILLA, EMIRATES HILLS
    "interior-bath-green":      ("hst", 15, 2, "services"),

    # ---------- renovation / fit-out ----------
    "renovation-boardroom":         ("el",   6, 0, "services"),
    "renovation-industrial-office": ("el",   7, 0, "services"),
    "renovation-loft-stairs":       ("el",  17, 0, "services"),
    "renovation-loft-office":       ("el",  18, 0, "services"),
    "renovation-executive-office":  ("hst", 13, 0, "services"),  # PRIVATE OFFICE, BUSINESS BAY
    "renovation-meeting-room":      ("hst", 17, 0, "services"),
    "renovation-office-seaview":    ("hst", 17, 1, "services"),
    "renovation-progress-shell":    ("el",  16, 1, "services"),

    # ---------- landscape (all real photography, no renders) ----------
    "landscape-villa-pool":     ("el",  30, 0, "services"),   # GARDEN, DISTRICT ONE
    "landscape-roof-garden":    ("el",  31, 0, "services"),   # ROOF GARDEN, DISTRICT ONE
    "landscape-pergola-lawn":   ("hst", 25, 0, "services"),   # LANDSCAPE PRIVATE VILLA, DAMAC HILLS
    "landscape-garden-terrace": ("hst", 24, 0, "services"),
    "landscape-planters":       ("hst", 23, 0, "services"),
    "landscape-hills-lawn":     ("el",  32, 0, "services"),   # DUBAI HILLS LANDSCAPE
    "landscape-hills-sculpture":("el",  34, 0, "services"),

    # ---------- projects ----------
    # Springfield Office — HST profile p20-21
    "proj-springfield-sign":       ("hst", 21, 0, "projects"),
    "proj-springfield-reception":  ("hst", 21, 1, "projects"),
    "proj-springfield-boardroom":  ("hst", 21, 2, "projects"),
    "proj-springfield-bar":        ("hst", 21, 3, "projects"),
    # Floward Office — HST profile p18-19  (Floward wordmark visible in these shots)
    "proj-floward-lounge":  ("hst", 19, 0, "projects"),
    "proj-floward-desk":    ("hst", 19, 1, "projects"),
    "proj-floward-green":   ("hst", 19, 2, "projects"),
    "proj-floward-studio":  ("hst", 19, 3, "projects"),
    # Gym Renovation, Al Wasl — HST profile p8-11
    "proj-gym-cardio":  ("hst", 11, 0, "projects"),
    "proj-gym-floor":   ("hst", 11, 1, "projects"),
    "proj-gym-rigs":    ("hst", 11, 2, "projects"),
    "proj-gym-lounge":  ("hst",  9, 1, "projects"),
    # Private Office, Deira — HST profile p6-7
    "proj-office-deira-floor": ("hst", 7, 0, "projects"),
    "proj-office-deira":       ("hst", 7, 1, "projects"),
    "proj-office-reception":   ("hst", 7, 2, "projects"),
    # Private Office, Business Bay — HST profile p12-13
    "proj-bb-pantry": ("hst", 13, 1, "projects"),
    "proj-bb-powder": ("hst", 13, 2, "projects"),
    # Private Villa, Emirates Hills — HST profile p14-15
    "proj-emirates-hills-shower": ("hst", 15, 0, "projects"),
    # Office Renovation, NBD Building
    "proj-nbd-office":   ("el", 11, 0, "projects"),
    "proj-nbd-office-2": ("el", 12, 0, "projects"),
    # Private Villa, Jumeirah
    "proj-villa-jumeirah": ("el", 16, 0, "projects"),
    # Penthouse, Dubai Marina
    "proj-penthouse-marina": ("el", 20, 0, "projects"),
    # IMA Gallery Showroom
    "proj-ima-gallery":  ("el", 22, 0, "projects"),
    "proj-ima-interior": ("el", 23, 1, "projects"),
    # GAMA Fashion Showroom, Abu Dhabi
    "proj-gama-showroom": ("el", 24, 0, "projects"),
    "proj-gama-retail":   ("el", 24, 1, "projects"),
    # DNG Furniture Showroom, Al Barsha One
    "proj-dng-furniture": ("el", 25, 0, "projects"),
    "proj-dng-progress":  ("el", 25, 1, "projects"),   # during fit-out
    # Mehr o Mah Art Café
    "proj-cafe-terrace":  ("el", 26, 0, "projects"),
    "proj-cafe-greenery": ("el", 27, 0, "projects"),
    "proj-cafe-interior": ("el", 28, 1, "projects"),
    # Dubai Hills Landscape
    "proj-dubai-hills-lawn":      ("el", 32, 0, "projects"),
    "proj-dubai-hills-before":    ("el", 32, 1, "projects"),
    "proj-dubai-hills-sculpture": ("el", 34, 0, "projects"),
    # Roof Garden, District One — during works
    "proj-district-one-garden": ("el", 30, 1, "projects"),

    # ---------- 3D visualisations (source pages headed "Our 3D Design") ----------
    "render-lounge":         ("hst", 27, 0, "renders"),
    "render-living":         ("hst", 27, 1, "renders"),
    "render-workspace":      ("hst", 27, 2, "renders"),
    "render-gallery":        ("hst", 27, 3, "renders"),
    "render-villa-night":    ("hst", 26, 0, "renders"),
    "render-villa-entrance": ("hst", 26, 1, "renders"),
}


def find_pdf(key):
    for p in SOURCES[key]:
        if os.path.exists(p):
            return p
    return None


def load_docs():
    import fitz
    docs = {}
    for key in SOURCES:
        path = find_pdf(key)
        if not path:
            sys.exit(f"Source PDF for '{key}' not found. Looked in:\n  " +
                     "\n  ".join(SOURCES[key]))
        docs[key] = fitz.open(path)
        print(f"  {key}: {os.path.basename(path)} ({len(docs[key])} pages)")
    return docs


def extract(doc, page_no, idx):
    """Return a PIL image for the idx-th image on the given 1-based page."""
    import fitz
    page = doc[page_no - 1]
    imgs = page.get_images(full=True)
    if idx >= len(imgs):
        raise IndexError(f"page {page_no} has {len(imgs)} images, wanted index {idx}")
    pix = fitz.Pixmap(doc, imgs[idx][0])
    if pix.n - pix.alpha >= 4:
        pix = fitz.Pixmap(fitz.csRGB, pix)
    im = Image.open(io.BytesIO(pix.tobytes("png")))
    return ImageOps.exif_transpose(im).convert("RGB")


def process():
    print("Reading source profiles:")
    docs = load_docs()
    manifest, made, failed = {}, [], []

    for slug, (doc_key, page_no, idx, cat) in CURATED.items():
        try:
            im = extract(docs[doc_key], page_no, idx)
        except Exception as e:
            failed.append(f"{slug}: {doc_key} p{page_no} #{idx} — {e}")
            continue

        ow, oh = im.size
        if ow < 300 or oh < 300:
            failed.append(f"{slug}: too small ({ow}x{oh})")
            continue

        dest = os.path.join(OUT, cat)
        os.makedirs(dest, exist_ok=True)
        allow_up = slug in UPSCALE
        avail = []

        for w in WIDTHS:
            if w > ow and not allow_up and w != min(WIDTHS):
                continue
            tw = w if allow_up else min(w, ow)
            th = round(oh * tw / ow)
            r = im.resize((tw, th), Image.LANCZOS)
            if tw > ow:
                r = r.filter(ImageFilter.UnsharpMask(radius=1.4, percent=62, threshold=3))
            r.save(os.path.join(dest, f"{slug}-{w}.webp"), "WEBP", quality=82, method=6)
            avail.append({"label": w, "real": tw})

        # JPEG fallback, and the image social platforms are given (they do not decode WebP)
        fw = min(1280, ow)
        im.resize((fw, round(oh * fw / ow)), Image.LANCZOS).save(
            os.path.join(dest, f"{slug}.jpg"), "JPEG", quality=82, optimize=True, progressive=True)

        manifest[f"{cat}/{slug}"] = {"w": ow, "h": oh, "widths": avail,
                                     "src": f"{doc_key} p{page_no} #{idx}"}
        made.append(f"{cat}/{slug}  {ow}x{oh}  <- {doc_key} p{page_no} #{idx}")

    with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1, sort_keys=True)

    for d in docs.values():
        d.close()

    print(f"\nOK {len(made)} images -> assets/img/manifest.json")
    for m in made:
        print("  +", m)
    if failed:
        print(f"\nFAILED {len(failed)}:")
        for f in failed:
            print("  !", f)
        sys.exit(1)


if __name__ == "__main__":
    process()

# -*- coding: utf-8 -*-
"""Curate + optimise project photography extracted from the HST / Elegant Lines profiles."""
from PIL import Image, ImageOps, ImageFilter
import os, json

SRC = r"C:/Users/TUF/AppData/Local/Temp/claude/D--Claude-HST/3f969b87-5f83-42ec-8513-ebcbb1f0f648/scratchpad/pdf/img"
OUT = r"D:/Claude HST/assets/img"

# slug -> (source file, category)
CURATED = {
    # ---------- hero / atmosphere ----------
    "hero-villa-night":        ("hst_p26_0_1285x723.png",  "hero"),
    "hero-pool-dusk":          ("el_p30_0_1024x1024.png",  "hero"),
    "hero-pergola-lounge":     ("el_p31_0_1024x1024.png",  "hero"),
    "hero-office-skyline":     ("el_p10_0_1804x1347.png",  "hero"),
    "hero-architecture-dark":  ("hst_p02_2_851x996.png",   "hero"),
    "hero-villa-entrance":     ("hst_p26_1_1285x723.png",  "hero"),

    # ---------- interior design ----------
    "interior-lounge-seaview":     ("hst_p03_1_936x959.png",    "services"),
    "interior-marble-lobby":       ("el_p13_0_1138x640.png",    "services"),
    "interior-curved-living":      ("el_p15_1_1280x640.png",    "services"),
    "interior-loft-living":        ("el_p14_0_512x576.png",     "services"),
    "interior-styled-living":      ("el_p21_0_1026x1152.png",   "services"),
    "interior-kitchen-brass":      ("el_p19_0_576x576.png",     "services"),
    "interior-corridor-gold":      ("el_p08_0_1804x1347.png",   "services"),
    "interior-corridor-white":     ("el_p09_1_1315x982.png",    "services"),
    "interior-bath-marble":        ("hst_p15_1_445x665.png",    "services"),
    "interior-bath-green":         ("hst_p15_2_466x697.png",    "services"),

    # ---------- renovation / fit-out ----------
    "renovation-boardroom":        ("el_p06_0_1021x1024.png",   "services"),
    "renovation-industrial-office":("el_p07_0_576x548.png",     "services"),
    "renovation-loft-stairs":      ("el_p17_0_1024x576.png",    "services"),
    "renovation-loft-office":      ("el_p18_0_1024x576.png",    "services"),
    "renovation-executive-office": ("hst_p13_0_720x1280.png",   "services"),
    "renovation-meeting-room":     ("hst_p17_0_1280x606.png",   "services"),
    "renovation-office-seaview":   ("hst_p17_1_1152x546.png",   "services"),
    "renovation-progress-shell":   ("el_p16_1_981x981.png",     "services"),

    # ---------- landscape ----------
    "landscape-villa-pool":        ("el_p29_0_1014x932.png",    "services"),
    "landscape-roof-progress":     ("el_p31_1_1748x981.png",    "services"),
    "landscape-roof-garden":       ("el_p31_0_1024x1024.png",   "services"),
    "landscape-water-wall":        ("hst_p26_2_1285x723.png",   "services"),
    "landscape-side-garden":       ("hst_p26_3_1285x723.png",   "services"),
    "landscape-pergola-lawn":      ("hst_p25_0_1280x720.png",   "services"),
    "landscape-planters":          ("hst_p23_0_1104x576.png",   "services"),
    "landscape-garden-terrace":    ("hst_p24_0_1280x720.png",   "services"),

    # ---------- portfolio projects ----------
    "proj-springfield-reception":  ("hst_p21_1_908x456.png",    "projects"),
    "proj-springfield-lounge":     ("hst_p19_0_1187x720.png",   "projects"),
    "proj-springfield-desk":       ("hst_p19_1_1088x687.png",   "projects"),
    "proj-springfield-green":      ("hst_p19_2_1232x723.png",   "projects"),
    "proj-springfield-studio":     ("hst_p19_3_1200x717.png",   "projects"),
    "proj-springfield-sign":       ("hst_p21_0_811x432.png",    "projects"),
    "proj-gym-floor":              ("hst_p11_1_900x1600.png",   "projects"),
    "proj-gym-rigs":               ("hst_p11_2_900x1600.png",   "projects"),
    "proj-gym-cardio":             ("hst_p11_0_900x1600.png",   "projects"),
    "proj-gym-lounge":             ("hst_p09_1_720x1280.png",   "projects"),
    "proj-office-deira":           ("hst_p07_1_720x1280.png",   "projects"),
    "proj-office-reception":       ("hst_p07_2_720x1280.png",   "projects"),
    "proj-villa-pantry":           ("hst_p13_1_720x1280.png",   "projects"),
    "proj-villa-powder":           ("hst_p13_2_720x1280.png",   "projects"),
    "proj-ima-gallery":            ("el_p22_0_2038x1330.png",   "projects"),
    "proj-ima-interior":           ("el_p23_1_1024x724.png",    "projects"),
    "proj-gama-showroom":          ("el_p24_0_1024x576.png",    "projects"),
    "proj-gama-retail":            ("el_p24_1_1000x562.png",    "projects"),
    "proj-dng-furniture":          ("el_p25_0_2048x1152.png",   "projects"),
    "proj-cafe-terrace":           ("el_p26_0_2365x1330.png",   "projects"),
    "proj-cafe-greenery":          ("el_p27_0_1411x2051.png",   "projects"),
    "proj-cafe-interior":          ("el_p28_1_1536x2048.png",   "projects"),
    "proj-penthouse-marina":       ("el_p20_0_576x1024.png",    "projects"),
    "proj-villa-jumeirah":         ("el_p16_0_1280x640.png",    "projects"),
    "proj-district-one-garden":    ("el_p30_1_1748x981.png",    "projects"),
    "proj-render-lounge":          ("hst_p27_0_1375x773.png",   "projects"),
    "proj-render-living":          ("hst_p27_1_1375x773.png",   "projects"),
    "proj-render-workspace":       ("hst_p27_2_1600x823.png",   "projects"),
    "proj-render-gallery":         ("hst_p27_3_1359x731.png",   "projects"),
    "proj-nbd-office":             ("el_p11_0_1152x546.png",    "projects"),
    "proj-restaurant-bar":         ("el_p04_0_910x1024.png",    "projects"),
}

WIDTHS = [1920, 1280, 800, 480]
# heroes are shown full-bleed, so allow a sharpened upscale rather than a soft stretch
UPSCALE = {"hero-pool-dusk", "hero-pergola-lounge", "hero-villa-night", "hero-villa-entrance",
           "hero-architecture-dark"}

def process():
    made, missing, manifest = [], [], {}
    for slug, (fname, cat) in CURATED.items():
        src = os.path.join(SRC, fname)
        if not os.path.exists(src):
            missing.append((slug, fname)); continue
        dest_dir = os.path.join(OUT, cat)
        os.makedirs(dest_dir, exist_ok=True)
        im = Image.open(src)
        im = ImageOps.exif_transpose(im).convert("RGB")
        ow, oh = im.size
        avail = []
        allow_up = slug in UPSCALE
        for w in WIDTHS:
            if w > ow and not allow_up and w != min(WIDTHS):
                continue
            tw = w if allow_up else min(w, ow)
            avail.append((w, tw))
            th = round(oh * tw / ow)
            r = im.resize((tw, th), Image.LANCZOS)
            if tw > ow:
                r = r.filter(ImageFilter.UnsharpMask(radius=1.4, percent=62, threshold=3))
            r.save(os.path.join(dest_dir, f"{slug}-{w}.webp"), "WEBP", quality=82, method=6)
        # jpeg fallback at 1280
        fw = min(1280, ow)
        im.resize((fw, round(oh*fw/ow)), Image.LANCZOS).save(
            os.path.join(dest_dir, f"{slug}.jpg"), "JPEG", quality=82, optimize=True, progressive=True)
        manifest[f"{cat}/{slug}"] = {"w": ow, "h": oh,
                                     "widths": [{"label": a, "real": r} for a, r in avail]}
        made.append(f"{cat}/{slug}  ({ow}x{oh})")
    with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1, sort_keys=True)
    print(f"OK {len(made)} images -> manifest.json")
    for m in made: print("  +", m)
    if missing:
        print("MISSING:")
        for s, f in missing: print("  !", s, f)

if __name__ == "__main__":
    process()

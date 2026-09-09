# -*- coding: utf-8 -*-
"""WCAG contrast checker for the palette in assets/css/site.css."""
def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def lum(hexcol):
    h = hexcol.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return 0.2126*_lin(r) + 0.7152*_lin(g) + 0.0722*_lin(b)

def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

def check(label, fg, bg, need):
    r = ratio(fg, bg)
    print(f"{'PASS' if r >= need else 'FAIL'}  {r:5.2f}:1  (need {need})  {label:44} {fg} on {bg}")
    return r >= need

if __name__ == "__main__":
    LB, LS = "#F1EDE4", "#FFFDF8"          # light bg / light surface
    DB, DS = "#0E1620", "#16212E"          # dark bg / dark surface
    print("--- LIGHT ---")
    ok = True
    ok &= check("body copy  --ink-muted",        "#5A626C", LB, 4.5)
    ok &= check("captions   --ink-faint",        "#646C77", LB, 4.5)
    ok &= check("display .lite (large text)",    "#7E8792", LB, 3.0)
    ok &= check("accent as text --accent",       "#9C4F3A", LB, 4.5)
    ok &= check("accent on white surface",       "#9C4F3A", LS, 4.5)
    ok &= check("white on accent button",        "#FFFFFF", "#9C4F3A", 4.5)
    ok &= check("control border --line-strong",  "#767E88", LB, 3.0)
    ok &= check("error text",                    "#A8362B", LB, 4.5)
    ok &= check("success text",                  "#276848", LB, 4.5)
    print("--- DARK ---")
    ok &= check("body copy  --ink-muted",        "#A8B2BE", DB, 4.5)
    ok &= check("captions   --ink-faint",        "#8B95A1", DB, 4.5)
    ok &= check("display .lite (large text)",    "#7C8794", DB, 3.0)
    ok &= check("accent as text --accent",       "#E0937B", DB, 4.5)
    ok &= check("accent on dark surface",        "#E0937B", DS, 4.5)
    ok &= check("control border",                "#79838F", DB, 3.0)
    ok &= check("error text",                    "#F08A7C", DB, 4.5)
    ok &= check("success text",                  "#6FCB9B", DB, 4.5)
    raise SystemExit(0 if ok else 1)

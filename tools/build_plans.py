# -*- coding: utf-8 -*-
"""Generate architectural floor-plan line drawings used as background texture.

The output is a stencil: every stroke is black with a varying stroke-opacity, so
the file can be used as a CSS mask and tinted by the theme (grey on light, copper
on dark) from a single asset. Nothing here is a real HST drawing; it is generic
plan linework in the conventions of a general arrangement drawing.

    python tools/build_plans.py
"""
import os, math, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "plans")

# stroke weights, in the same spirit as a real drawing set
W_WALL   = 2.6      # structural wall
W_PART   = 1.5      # partition
W_THIN   = 0.7      # dimension, grid, symbol
W_HAIR   = 0.5      # hatching, fixtures

O_WALL, O_PART, O_THIN, O_HAIR, O_GRID = 1.0, 0.85, 0.5, 0.38, 0.3


class Plan:
    def __init__(self, w, h, seed):
        self.w, self.h = w, h
        self.r = random.Random(seed)
        self.parts = []

    # ---- primitives ------------------------------------------------------
    def line(self, x1, y1, x2, y2, sw=W_THIN, op=O_THIN, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<path d="M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}" stroke-width="{sw}" '
            f'stroke-opacity="{op}"{d}/>')

    def rect(self, x, y, w, h, sw=W_THIN, op=O_THIN):
        self.parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'stroke-width="{sw}" stroke-opacity="{op}"/>')

    def circle(self, cx, cy, r, sw=W_THIN, op=O_THIN):
        self.parts.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" stroke-width="{sw}" '
            f'stroke-opacity="{op}"/>')

    def arc(self, cx, cy, r, a0, a1, sw=W_THIN, op=O_THIN):
        x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
        large = 1 if abs(a1 - a0) > 180 else 0
        sweep = 1 if a1 > a0 else 0
        self.parts.append(
            f'<path d="M{x0:.1f} {y0:.1f}A{r:.1f} {r:.1f} 0 {large} {sweep} {x1:.1f} {y1:.1f}" '
            f'stroke-width="{sw}" stroke-opacity="{op}"/>')

    # ---- drawing conventions ---------------------------------------------
    def wall(self, x1, y1, x2, y2, t=9):
        """A wall drawn as two parallel lines, the way a plan shows it."""
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L * t / 2, dx / L * t / 2
        self.line(x1 + nx, y1 + ny, x2 + nx, y2 + ny, W_WALL, O_WALL)
        self.line(x1 - nx, y1 - ny, x2 - nx, y2 - ny, W_WALL, O_WALL)

    def partition(self, x1, y1, x2, y2, t=5):
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L * t / 2, dx / L * t / 2
        self.line(x1 + nx, y1 + ny, x2 + nx, y2 + ny, W_PART, O_PART)
        self.line(x1 - nx, y1 - ny, x2 - nx, y2 - ny, W_PART, O_PART)

    def door(self, x, y, size=30, rot=0):
        """Leaf plus quarter-circle swing."""
        a = math.radians(rot)
        lx, ly = x + size * math.cos(a), y + size * math.sin(a)
        self.line(x, y, lx, ly, W_PART, O_PART)
        self.arc(x, y, size, rot, rot + 90, W_THIN, O_THIN * .85)

    def window(self, x1, y1, x2, y2):
        """Three thin lines across the opening."""
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        for o in (-3, 0, 3):
            self.line(x1 + nx * o, y1 + ny * o, x2 + nx * o, y2 + ny * o, W_THIN, O_THIN)

    def stair(self, x, y, w, h, treads=11, up=True):
        self.rect(x, y, w, h, W_PART, O_PART)
        step = h / treads
        for i in range(1, treads):
            self.line(x, y + i * step, x + w, y + i * step, W_THIN, O_THIN)
        # direction arrow along the flight
        cx = x + w / 2
        self.line(cx, y + h - step * .6, cx, y + step * .6, W_THIN, O_THIN)
        tip = y + step * .6
        self.line(cx, tip, cx - 4, tip + 8, W_THIN, O_THIN)
        self.line(cx, tip, cx + 4, tip + 8, W_THIN, O_THIN)

    def grid_bubble(self, cx, cy, label, r=13):
        self.circle(cx, cy, r, W_THIN, O_THIN)
        self.parts.append(
            f'<text x="{cx:.1f}" y="{cy + 4.2:.1f}" text-anchor="middle" '
            f'font-family="Helvetica,Arial,sans-serif" font-size="13" '
            f'fill="#000" fill-opacity="{O_THIN}" stroke="none">{label}</text>')

    def dim_chain(self, x, y, stops, vertical=False):
        """A dimension line with 45-degree ticks at each station."""
        a, b = stops[0], stops[-1]
        if vertical:
            self.line(x, a, x, b, W_THIN, O_THIN)
        else:
            self.line(a, y, b, y, W_THIN, O_THIN)
        for s in stops:
            if vertical:
                self.line(x - 4, s + 4, x + 4, s - 4, W_THIN, O_THIN)
            else:
                self.line(s - 4, y + 4, s + 4, y - 4, W_THIN, O_THIN)

    def level_tag(self, x, y, text):
        self.line(x - 7, y - 7, x + 7, y - 7, W_THIN, O_THIN)
        self.line(x - 7, y - 7, x, y, W_THIN, O_THIN)
        self.line(x + 7, y - 7, x, y, W_THIN, O_THIN)
        self.parts.append(
            f'<text x="{x + 11:.1f}" y="{y - 1:.1f}" font-family="Helvetica,Arial,sans-serif" '
            f'font-size="11" fill="#000" fill-opacity="{O_THIN}" stroke="none">{text}</text>')

    def hatch(self, x, y, w, h, gap=7):
        """45-degree hatching, used for cores and shafts."""
        n = int((w + h) / gap)
        for i in range(n):
            t = i * gap
            x1, y1 = x + t, y
            x2, y2 = x, y + t
            if x1 > x + w:
                y1 += x1 - (x + w); x1 = x + w
            if y2 > y + h:
                x2 += y2 - (y + h); y2 = y + h
            if x1 >= x and y2 >= y:
                self.line(x1, y1, x2, y2, W_HAIR, O_HAIR)

    def svg(self, ink="#000000"):
        """Self-contained drawing: ink colour and the edge feather are baked in,
        so the browser only has to paint a background image."""
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
            f'width="{self.w}" height="{self.h}" fill="none" stroke="{ink}" '
            f'stroke-linecap="square">'
            f'<defs><radialGradient id="f" cx="50%" cy="50%" r="62%">'
            f'<stop offset="46%" stop-color="#fff" stop-opacity="1"/>'
            f'<stop offset="100%" stop-color="#fff" stop-opacity="0"/>'
            f'</radialGradient>'
            f'<mask id="m"><rect width="{self.w}" height="{self.h}" fill="url(#f)"/></mask></defs>'
            f'<g mask="url(#m)">' + "".join(self.parts).replace('fill="#000"', f'fill="{ink}"')
            + "</g></svg>")


# ---------------------------------------------------------------------------
# extra conventions used by the denser plans
# ---------------------------------------------------------------------------
def _fixtures_bath(p, x, y, w, h):
    """WC, basin and a shower tray, drawn the way a plan shows sanitaryware."""
    p.rect(x + 4, y + 4, 26, 16, W_HAIR, O_HAIR)          # basin
    p.circle(x + 17, y + 12, 6, W_HAIR, O_HAIR)
    p.rect(x + 4, y + h - 30, 18, 26, W_HAIR, O_HAIR)     # wc
    p.circle(x + 13, y + h - 17, 7, W_HAIR, O_HAIR)
    p.rect(x + w - 40, y + h - 40, 36, 36, W_HAIR, O_HAIR)  # shower
    p.line(x + w - 40, y + h - 40, x + w - 4, y + h - 4, W_HAIR, O_HAIR)


def _fixtures_kitchen(p, x, y, w, h):
    p.rect(x, y, w, 22, W_HAIR, O_HAIR)                   # counter run
    for i in range(1, 4):
        p.line(x + i * w / 4, y, x + i * w / 4, y + 22, W_HAIR, O_HAIR)
    p.circle(x + w * 0.72, y + 11, 7, W_HAIR, O_HAIR)     # sink
    for cx, cy in ((x + w * .2, y + 8), (x + w * .28, y + 8),
                   (x + w * .2, y + 15), (x + w * .28, y + 15)):
        p.circle(cx, cy, 3, W_HAIR, O_HAIR)               # hob


def _furniture(p, x, y, w, h, seats=0):
    p.rect(x, y, w, h, W_HAIR, O_HAIR)
    for i in range(seats):
        p.rect(x + 6 + i * ((w - 12) / max(seats, 1)), y - 12, 16, 9, W_HAIR, O_HAIR)


def _section_mark(p, x, y, label="A"):
    p.circle(x, y, 12, W_THIN, O_THIN)
    p.line(x - 12, y, x + 12, y, W_THIN, O_THIN)
    p.line(x + 12, y, x + 26, y, W_THIN, O_THIN)
    p.line(x + 26, y, x + 20, y - 5, W_THIN, O_THIN)
    p.line(x + 26, y, x + 20, y + 5, W_THIN, O_THIN)
    p.parts.append(
        f'<text x="{x:.1f}" y="{y - 2:.1f}" text-anchor="middle" '
        f'font-family="Helvetica,Arial,sans-serif" font-size="9" fill="#000" '
        f'fill-opacity="{O_THIN}" stroke="none">{label}</text>')


def _grid_and_dims(p, cols, rows, T, B, L, R):
    for i, x in enumerate(cols):
        p.line(x, T - 84, x, B + 48, W_THIN, O_GRID, dash="16 6 3 6")
        p.grid_bubble(x, T - 102, chr(ord("A") + i))
    for j, y in enumerate(rows):
        p.line(L - 98, y, R + 48, y, W_THIN, O_GRID, dash="16 6 3 6")
        p.grid_bubble(L - 116, y, str(j + 1))
    p.dim_chain(0, T - 46, cols)                       # bay dimensions
    p.dim_chain(0, T - 66, [cols[0], cols[-1]])        # overall
    p.dim_chain(L - 54, 0, rows, vertical=True)
    p.dim_chain(L - 74, 0, [rows[0], rows[-1]], vertical=True)


# ---------------------------------------------------------------------------
def apartment_plan(seed=7):
    """A residential floor: column grid, dimension chains, rooms, wet areas."""
    p = Plan(1240, 860, seed)
    L, T, R, B = 175, 155, 1090, 735
    cols = [L, L + 175, L + 330, L + 520, L + 700, L + 830, R]
    rows = [T, T + 130, T + 268, T + 400, T + 500, B]
    _grid_and_dims(p, cols, rows, T, B, L, R)

    # envelope
    p.wall(L, T, R, T); p.wall(R, T, R, B); p.wall(R, B, L, B); p.wall(L, B, L, T)

    # primary partitions
    for x in (cols[2], cols[4]):
        p.partition(x, T, x, rows[4])
    p.partition(L, rows[2], cols[2], rows[2])
    p.partition(cols[2], rows[1], cols[4], rows[1])
    p.partition(cols[4], rows[2], R, rows[2])
    p.partition(L, rows[4], R, rows[4])
    p.partition(cols[1], rows[4], cols[1], B)
    p.partition(cols[3], rows[4], cols[3], B)
    p.partition(cols[5], T, cols[5], rows[2])
    p.partition(cols[1], T, cols[1], rows[2])
    p.partition(cols[2], rows[3], cols[4], rows[3])

    # circulation core with stair and lift shaft
    p.rect(cols[2] + 20, rows[1] + 18, 170, 118, W_PART, O_PART)
    p.stair(cols[2] + 34, rows[1] + 30, 92, 94)
    p.rect(cols[2] + 140, rows[1] + 30, 44, 94, W_PART, O_PART)
    p.hatch(cols[2] + 140, rows[1] + 30, 44, 94, gap=8)

    # wet areas
    _fixtures_bath(p, cols[4] + 16, rows[0] + 16, 110, 96)
    _fixtures_bath(p, cols[0] + 18, rows[2] + 18, 110, 96)
    _fixtures_kitchen(p, cols[2] + 26, rows[3] + 22, 150, 40)

    # furniture blocks
    _furniture(p, cols[0] + 30, rows[0] + 34, 108, 58, seats=3)
    _furniture(p, cols[4] + 40, rows[2] + 40, 122, 64, seats=4)
    _furniture(p, cols[1] + 34, rows[4] + 30, 96, 52)

    # openings
    p.window(cols[0] + 36, T, cols[1] - 26, T)
    p.window(cols[1] + 26, T, cols[2] - 26, T)
    p.window(cols[4] + 30, T, cols[5] - 26, T)
    p.window(R, rows[0] + 34, R, rows[1] - 26)
    p.window(R, rows[2] + 30, R, rows[3] - 26)
    p.window(cols[1] + 30, B, cols[3] - 30, B)
    p.window(L, rows[2] + 34, L, rows[3] - 26)
    for x, y, rot in ((cols[2], rows[0] + 52, 0), (cols[2], rows[2] + 60, 0),
                      (cols[4], rows[0] + 60, 90), (cols[4], rows[3] + 40, 90),
                      (cols[1], rows[4] + 40, 270), (cols[3], rows[4] + 40, 270),
                      (cols[5], rows[1] + 40, 180), (cols[1], rows[0] + 60, 0),
                      (cols[2] + 96, rows[3], 180)):
        p.door(x, y, 32, rot)

    # annotation
    p.level_tag(cols[0] + 60, rows[1] + 62, "FFL +4.25")
    p.level_tag(cols[3] + 40, rows[2] + 96, "CL +3.00")
    p.level_tag(cols[5] + 20, rows[3] + 60, "FFL +4.15")
    _section_mark(p, cols[3] + 20, T - 128, "A")
    return p


def villa_plan(seed=19):
    """A lower-density plan: living, terrace and a pool beyond the envelope."""
    p = Plan(1160, 820, seed)
    L, T, R, B = 195, 165, 960, 670
    cols = [L, L + 210, L + 395, L + 560, R]
    rows = [T, T + 165, T + 300, T + 400, B]
    _grid_and_dims(p, cols, rows, T, B, L, R)

    p.wall(L, T, R, T); p.wall(R, T, R, B); p.wall(R, B, L, B); p.wall(L, B, L, T)
    p.partition(cols[1], T, cols[1], rows[3])
    p.partition(cols[1], rows[1], R, rows[1])
    p.partition(L, rows[3], R, rows[3])
    p.partition(cols[2], rows[1], cols[2], rows[3])
    p.partition(cols[3], T, cols[3], rows[1])
    p.partition(cols[1], rows[2], cols[2], rows[2])

    p.stair(cols[1] + 26, rows[1] + 22, 92, 108)
    _fixtures_bath(p, cols[3] + 16, rows[0] + 16, 104, 92)
    _fixtures_kitchen(p, cols[2] + 24, rows[1] + 26, 132, 38)
    _furniture(p, cols[0] + 44, rows[0] + 56, 122, 66, seats=4)
    _furniture(p, cols[2] + 40, rows[2] + 30, 104, 56)

    p.window(cols[0] + 46, T, cols[1] - 34, T)
    p.window(cols[1] + 34, T, cols[3] - 34, T)
    p.window(L, rows[0] + 44, L, rows[1] - 34)
    p.window(cols[1] + 40, B, cols[3] - 40, B)
    for x, y, rot in ((cols[1], rows[0] + 70, 0), (cols[2], rows[2] - 56, 180),
                      (cols[1] + 110, rows[3], 270), (cols[3], rows[0] + 56, 180),
                      (cols[2], rows[1] + 56, 0)):
        p.door(x, y, 32, rot)

    # terrace, pool and paving beyond the building line
    p.line(R, rows[1], R + 130, rows[1], W_THIN, O_GRID, dash="9 6")
    p.line(R, rows[3], R + 130, rows[3], W_THIN, O_GRID, dash="9 6")
    p.rect(R + 34, rows[1] + 44, 148, 92, W_PART, O_PART * .75)
    p.rect(R + 46, rows[1] + 56, 124, 68, W_HAIR, O_HAIR)
    for i in range(1, 5):
        p.line(R + 46, rows[1] + 56 + i * 13.6, R + 170, rows[1] + 56 + i * 13.6, W_HAIR, O_HAIR * .8)

    p.level_tag(cols[0] + 66, rows[1] + 70, "FFL +0.00")
    p.level_tag(cols[2] + 60, rows[2] + 66, "CL +3.20")
    _section_mark(p, cols[2] + 20, T - 128, "B")
    return p


def core_detail(seed=31):
    """A tighter detail: stair core, services and wet rooms, for narrow slots."""
    p = Plan(720, 820, seed)
    L, T, R, B = 150, 150, 600, 690
    cols = [L, (L + R) / 2, R]
    rows = [T, T + 210, T + 360, B]
    _grid_and_dims(p, cols, rows, T, B, L, R)

    p.wall(L, T, R, T); p.wall(R, T, R, B); p.wall(R, B, L, B); p.wall(L, B, L, T)
    p.partition(L, rows[1], R, rows[1])
    p.partition(cols[1], rows[1], cols[1], B)
    p.partition(L, rows[2], cols[1], rows[2])

    p.stair(L + 34, T + 34, 140, 150)
    p.rect(R - 150, T + 34, 108, 150, W_PART, O_PART)
    p.hatch(R - 150, T + 34, 108, 150, gap=8)

    _fixtures_bath(p, L + 22, rows[1] + 22, 130, 110)
    _fixtures_bath(p, cols[1] + 22, rows[1] + 22, 130, 110)
    _fixtures_kitchen(p, L + 26, rows[2] + 30, 120, 36)

    p.window(L, T + 60, L, T + 150)
    p.window(cols[1] + 30, B, R - 30, B)
    for x, y, rot in ((L + 34, rows[1] - 42, 0), (cols[1], rows[1] + 66, 90),
                      (cols[1], rows[2] + 50, 270), (L + 120, rows[2], 180)):
        p.door(x, y, 30, rot)
    p.level_tag(L + 50, B - 66, "FFL +4.25")
    _section_mark(p, cols[1] + 10, T - 128, "C")
    return p


VARIANTS = {"plan-apartment": apartment_plan, "plan-villa": villa_plan, "plan-core": core_detail}


# ink per theme: warm grey on the light ground, copper on the dark one
THEMES = {"light": "#8C8778", "dark": "#C07E66"}


def main():
    os.makedirs(OUT, exist_ok=True)
    total = 0
    for name, fn in VARIANTS.items():
        plan = fn()
        for theme, ink in THEMES.items():
            svg = plan.svg(ink)
            path = os.path.join(OUT, f"{name}-{theme}.svg")
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(svg)
            total += len(svg)
            print(f"  + {name}-{theme}.svg  {len(svg) / 1024:.1f} KB")
    print(f"OK  {total / 1024:.1f} KB total")


if __name__ == "__main__":
    main()

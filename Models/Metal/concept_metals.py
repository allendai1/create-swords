# concept_metals.py: candidate textures for the 2026-11-05 "cool concepts" brainstorm (Allen: "can u implement these
# so i can choose which to keep"). Same tile rules as metal_textures.py (1024 px, wraps, true colours with the part left
# white). Writes <name>_color / _normal / _rough per metal. The kept ones get uploaded as <Name>Ingot / <Name>Blade.
# Run: python concept_metals.py <out dir> [name ...]
import os, sys
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import metal_textures as mt
from metal_textures import N, xx, yy, blur, norm, noise, warped, mix, rgb, gray, normal

rng = np.random.default_rng(1105)


def wd(a, p):  # wrapped signed distance on the unit tile
    return (a - p + 0.5) % 1 - 0.5


def paint(fn, width=None):  # draw shapes with PIL, each copied at the 8 wrapped offsets so the tile wraps
    img = Image.new("L", (N, N))
    d = ImageDraw.Draw(img)
    for ox in (-N, 0, N):
        for oy in (-N, 0, N):
            fn(d, ox, oy)
    return np.asarray(img, dtype=float) / 255


def vor(g, jitter=0.9):  # wrapped Voronoi: nearest, second nearest (tile units) and cell id
    pts = (np.stack(np.mgrid[0:g, 0:g], -1).reshape(-1, 2) + 0.5 + (rng.random((g * g, 2)) - 0.5) * jitter) / g
    d1, d2, ids = np.full((N, N), 9.0), np.full((N, N), 9.0), np.zeros((N, N), int)
    for k, (py, px) in enumerate(pts):
        d = np.hypot(wd(xx, px), wd(yy, py))
        near = d < d1
        d2 = np.where(near, d1, np.minimum(d2, d))
        d1, ids = np.where(near, d, d1), np.where(near, k, ids)
    return d1, d2, ids


def save(out, name, col, h, k, rough):
    rgb(out, f"{name}_color", col)
    normal(out, name, h, k)
    gray(out, f"{name}_rough", rough)


def ramp(t, stops):  # colour ramp: stops = [(t, (r, g, b)), ...] in rising t
    t = np.clip(t, 0, 1)
    c = np.zeros((N, N, 3)) + np.array(stops[0][1], float)
    for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
        f = np.clip((t - t0) / (t1 - t0), 0, 1)
        c = np.where((t >= t0)[..., None], mix(c0, c1, f), c)
    return c


# ---- cool concepts -------------------------------------------------------------------------------------------------

def carbon(out):  # 2x2 twill weave, black with a grey sheen on each tow
    c = 32
    i, j = (yy * N // c).astype(int), (xx * N // c).astype(int)
    fu, fv = (xx * N / c) % 1, (yy * N / c) % 1
    horiz = ((i + j) % 4) < 2
    across = np.where(horiz, fv, fu)
    along = np.where(horiz, xx * N, yy * N)
    shade = np.sin(np.pi * across) ** 0.7
    fibre = 0.5 + 0.5 * np.sin(along * 0.9 + across * 40)
    v = 0.05 + 0.20 * shade * (0.85 + 0.15 * fibre)
    col = np.stack([v, v, v * 1.08], -1)
    save(out, "carbon", col, shade * 0.3, 1.2, 0.18 + (1 - shade) * 0.15)


def circuit(out):  # green board, gold traces with pads, a few black chips
    g = 32  # grid step in px
    traces, pads, chips = [], [], []
    for _ in range(46):
        x, y = rng.integers(0, N // g) * g, rng.integers(0, N // g) * g
        pts, dirs = [(x, y)], [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1)]
        dx, dy = dirs[rng.integers(0, 4)]
        for _ in range(rng.integers(4, 12)):
            if rng.random() < 0.35:
                dx, dy = dirs[rng.integers(0, 6)]
            x, y = x + dx * g, y + dy * g
            pts.append((x, y))
        traces.append(pts)
        pads += [pts[0], pts[-1]]
    for _ in range(5):
        chips.append((rng.integers(0, N), rng.integers(0, N), rng.integers(3, 6) * g // 2, rng.integers(2, 3) * g // 2))

    def tr(d, ox, oy):
        for pts in traces:
            d.line([(px + ox, py + oy) for px, py in pts], fill=255, width=6, joint="curve")
        for px, py in pads:
            d.ellipse([px + ox - 9, py + oy - 9, px + ox + 9, py + oy + 9], fill=255)

    def holes(d, ox, oy):
        for px, py in pads:
            d.ellipse([px + ox - 3, py + oy - 3, px + ox + 3, py + oy + 3], fill=255)

    def chip(d, ox, oy):
        for cx, cy, w, h in chips:
            d.rectangle([cx + ox - w, cy + oy - h, cx + ox + w, cy + oy + h], fill=255)

    def pins(d, ox, oy):
        for cx, cy, w, h in chips:
            for px in range(cx - w + 6, cx + w - 2, 12):
                for py in (cy - h - 8, cy + h + 2):
                    d.rectangle([px + ox, py + oy, px + ox + 5, py + oy + 6], fill=255)

    t, ho, ch, pn = paint(tr), paint(holes), paint(chip), paint(pins)
    grid = ((np.abs(((xx * N) % g) - g / 2) < 0.6) | (np.abs(((yy * N) % g) - g / 2) < 0.6)).astype(float)
    board = mix((0.04, 0.26, 0.12), (0.07, 0.36, 0.18), noise(40)) * (1 - grid * 0.08)[..., None]
    gold = mix((0.70, 0.50, 0.18), (0.95, 0.78, 0.38), noise(6))
    col = mix(board, gold, np.maximum(t, pn))
    col = mix(col, (0.05, 0.05, 0.06), ch)
    col = mix(col, (0.02, 0.06, 0.03), ho)
    h = np.maximum(t, pn) * 0.4 + ch * 0.8 - ho * 0.3
    save(out, "circuit", col, h, 1.2, 0.45 - t * 0.3 - ch * 0.1)


def synthwave(out):  # pink and cyan glowing grid on deep purple
    s = 64
    along = (np.abs(((yy * N) % s) - s / 2) > s / 2 - 1.8).astype(float)  # lines along U (the blade's length)
    across = (np.abs(((xx * N) % s) - s / 2) > s / 2 - 1.8).astype(float)
    bg = mix((0.06, 0.01, 0.12), (0.20, 0.03, 0.26), noise(120))
    cy, pk = np.array((0.15, 0.95, 1.0)), np.array((1.0, 0.25, 0.75))
    glow_a, glow_c = np.clip(blur(along, 4) * 3, 0, 1), np.clip(blur(across, 4) * 3, 0, 1)
    col = bg + cy * (along + glow_a * 0.5)[..., None] + pk * (across + glow_c * 0.5)[..., None]
    lines = np.maximum(along, across)
    save(out, "synthwave", col, lines * 0.2, 1.0, 0.12 + lines * 0.1)


def soulfire(out):  # dark steel with blue flames licking along the blade
    tongue = np.zeros((N, N))
    for s, w in ((22, 0.6), (8, 0.4)):
        r = 1 - np.abs(norm(blur(rng.normal(size=(N, N)), s * 3, s)) * 2 - 1)  # ridges stretched along U
        tongue += warped(r, 0.06, 40) ** 5 * w
    f = np.clip(norm(tongue) * 1.5 - 0.2, 0, 1)
    base = mix((0.05, 0.05, 0.08), (0.10, 0.11, 0.16), noise(60))
    fire = ramp(f, [(0, (0, 0, 0)), (0.25, (0.02, 0.10, 0.45)), (0.55, (0.10, 0.45, 1.0)), (0.85, (0.55, 0.90, 1.0)), (1, (1, 1, 1))])
    col = base + fire
    save(out, "soulfire", col, noise(3) * 0.02, 0.6, 0.20 - f * 0.08)


def blackhole(out):  # black, a few accretion discs: dark core, orange-white ring, spiral arms
    col = np.zeros((N, N, 3)) + 0.015
    stars = np.clip(blur(np.clip((rng.random((N, N)) - 0.998) * 600, 0, 1), 1.0) * 5, 0, 1)
    col += stars[..., None] * 0.5
    h = np.zeros((N, N))
    for _ in range(6):
        px, py, R = rng.random(), rng.random(), 0.045 + rng.random() * 0.03
        dx, dy = wd(xx, px), wd(yy, py)
        d = np.hypot(dx, dy) / R
        a = np.arctan2(dy, dx)
        arms = 0.5 + 0.5 * np.cos(2 * a + np.log(d + 1e-3) * 6 + rng.random() * 6)
        ring = np.exp(-((d - 0.62) / 0.12) ** 2)
        disc = np.clip(1 - (d - 0.55) / 1.4, 0, 1) * (d > 0.5) * (0.3 + 0.7 * arms) * 0.8 + ring
        light = ramp(np.clip(disc, 0, 1), [(0, (0, 0, 0)), (0.3, (0.55, 0.12, 0.02)), (0.7, (1.0, 0.55, 0.12)), (1, (1, 0.95, 0.85))])
        core = d < 0.5
        col = np.where(core[..., None], 0.0, np.maximum(col, light))
        h = np.maximum(h, np.clip(1 - d, 0, 1))
    save(out, "blackhole", col, -h * 0.4, 1.0, 0.15 + (col.mean(-1) < 0.05) * 0.1)


def runestone(out):  # dark stone with glowing cyan runes in rows along the blade
    lattice = [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2), (0.5, 1)]
    rows, cw, chh = 10, 40, 64
    glyphs = []
    for r in range(N // chh):
        for c in range(N // cw):
            if rng.random() < 0.18:
                continue
            strokes = []
            for _ in range(rng.integers(2, 5)):
                a, b = rng.choice(len(lattice), 2, replace=False)
                strokes.append((lattice[a], lattice[b]))
            strokes.append(((0, 0), (0, 2)) if rng.random() < 0.7 else ((1, 0), (1, 2)))  # a staff, like real runes
            glyphs.append((c * cw + 10, r * chh + 12, strokes))

    def draw(d, ox, oy):
        for gx, gy, strokes in glyphs:
            for (ax, ay), (bx, by) in strokes:
                d.line([(gx + ax * 18 + ox, gy + ay * 18 + oy), (gx + bx * 18 + ox, gy + by * 18 + oy)], fill=255, width=4)

    rune = paint(draw)
    glow = np.clip(blur(rune, 5) * 2.5, 0, 1)
    stone = (0.16 + 0.10 * noise(30) + 0.05 * noise(3))[..., None] * np.array((0.95, 1.0, 1.05))
    col = stone * (1 - rune[..., None]) + np.array((0.25, 0.95, 1.0)) * rune[..., None] + np.array((0.0, 0.35, 0.45)) * glow[..., None]
    save(out, "runestone", col, noise(8) * 0.3 - rune * 0.3, 1.4, 0.7 - rune * 0.5)


def clockwork(out):  # brass with interlocking engraved gears
    gears = []
    for _ in range(26):
        gears.append((rng.random() * N, rng.random() * N, 25 + rng.random() * 70, rng.random() * 6.28))

    def outline(d, ox, oy):
        for cx, cy, r, a0 in gears:
            teeth = max(8, int(r / 6))
            pts = []
            for k in range(teeth * 4):
                a = a0 + k * 2 * np.pi / (teeth * 4)
                rr = r if (k % 4) in (1, 2) else r * 0.86
                pts.append((cx + ox + rr * np.cos(a), cy + oy + rr * np.sin(a)))
            d.polygon(pts, outline=255, width=5)
            d.ellipse([cx + ox - r * 0.55, cy + oy - r * 0.55, cx + ox + r * 0.55, cy + oy + r * 0.55], outline=255, width=3)
            d.ellipse([cx + ox - r * 0.15, cy + oy - r * 0.15, cx + ox + r * 0.15, cy + oy + r * 0.15], fill=255)
            for k in range(5):
                a = a0 + k * 2 * np.pi / 5
                d.line([(cx + ox + r * 0.15 * np.cos(a), cy + oy + r * 0.15 * np.sin(a)), (cx + ox + r * 0.55 * np.cos(a), cy + oy + r * 0.55 * np.sin(a))], fill=255, width=4)

    e = paint(outline)
    brass = mix((0.62, 0.44, 0.18), (0.92, 0.74, 0.40), noise(50) * 0.7 + noise(6) * 0.3)
    col = brass * (1 - e * 0.75)[..., None]
    save(out, "clockwork", col, -e * 0.3 + noise(4) * 0.02, 1.4, 0.25 + e * 0.25)


def bloodmoon(out):  # crimson moon surface: dark seas and craters
    seas = noise(110) * 0.7 + noise(30) * 0.3
    col = mix((0.80, 0.14, 0.10), (0.38, 0.03, 0.05), np.clip(seas * 1.8 - 0.5, 0, 1))
    h = noise(4) * 0.03
    shade = np.zeros((N, N))
    for _ in range(90):
        px, py, R = rng.random(), rng.random(), (0.006 + rng.random() ** 3 * 0.04)
        dx, dy = wd(xx, px), wd(yy, py)
        d = np.hypot(dx, dy) / R
        bowl = np.clip(1 - d, 0, 1)
        rim = np.exp(-((d - 1) / 0.18) ** 2)
        h = h - bowl ** 2 * R * 8 + rim * R * 3
        shade += rim * np.clip(-dx / R, 0, 1) * 0.5 - bowl * np.clip(dx / R + 0.3, 0, 1) * 0.4  # light from the left
    col = col * (1 + shade)[..., None]
    save(out, "bloodmoon", col, h, 6.0, 0.6 + (noise(20) - 0.5) * 0.1)


def seraph(out):  # white-gold feathers overlapping like scales, with a shaft and barbs
    C, R = 6, 12
    u, v = xx * C, yy * R
    h, col_t, barb_t = np.zeros((N, N)), np.zeros((N, N)), np.zeros((N, N))
    for r in range(-1, R + 1):
        shift = 0.5 * (r % 2)
        for c in range(-1, C + 2):
            for wu in (-C, 0, C):
                for wv in (-R, 0, R):
                    lu, lv = u - (c + shift + wu), v - (r + wv)  # feather root at (0, 0), pointing +U
                    t = np.clip(lu / 1.4, 0, 1)
                    half = 0.95 * np.sin(np.pi * np.clip(lu / 1.4, 0, 1)) ** 0.8  # leaf outline
                    inside = (lu > 0) & (lu < 1.4) & (np.abs(lv) < half)
                    if not inside.any():
                        continue
                    barbs = 0.5 + 0.5 * np.sin((lu * 22 - np.abs(lv) * 14) * np.pi)
                    shaft = np.exp(-(lv / 0.05) ** 2)
                    hh = (1 - (np.abs(lv) / (half + 1e-6)) ** 2) * 0.6 + t * 0.4
                    h = np.where(inside, hh, h)
                    col_t = np.where(inside, np.abs(lv) / (half + 1e-6), col_t)
                    barb_t = np.where(inside, np.maximum(barbs * 0.6, shaft), barb_t)
    col = mix((0.99, 0.96, 0.86), (0.80, 0.56, 0.20), col_t ** 1.6) * (0.72 + 0.28 * barb_t)[..., None]
    save(out, "seraph", col, h * 0.4 + barb_t * 0.05, 1.6, 0.25 + col_t * 0.1)


def infernal(out):  # black steel, glowing red-orange cracks
    d1, d2, _ = vor(9, 0.95)
    d1b, d2b, _ = vor(20, 0.95)
    crack = np.clip(1 - (warped(d2 - d1, 0.01, 10)) * 9 / 0.08, 0, 1) + np.clip(1 - (d2b - d1b) * 20 / 0.10, 0, 1) * 0.5
    crack = np.clip(crack, 0, 1)
    glow = np.clip(blur(crack, 6) * 2.2, 0, 1)
    base = (0.04 + 0.05 * noise(20))[..., None] * np.ones(3)
    hot = ramp(np.maximum(crack, glow * 0.7), [(0, (0, 0, 0)), (0.3, (0.45, 0.03, 0.0)), (0.7, (1.0, 0.30, 0.03)), (1, (1.0, 0.85, 0.40))])
    save(out, "infernal", base + hot, -crack * 0.4 + noise(5) * 0.05, 1.4, 0.55 - crack * 0.3)


def prism(out):  # clear cut facets, each splitting light into its own pale spectral colour, white edges
    d1, d2, ids = vor(8, 0.85)
    n = ids.max() + 1
    hue = rng.random(n)
    edge = np.clip(1 - (d2 - d1) * 8 / 0.05, 0, 1)
    spec = np.stack([0.5 + 0.5 * np.cos(2 * np.pi * (hue + o)) for o in (0, 1 / 3, 2 / 3)], -1)
    shade = 0.78 + rng.random(n) * 0.22
    # each facet has a little rainbow sweep across it, so it reads as split light, not flat colour
    sweep = np.stack([0.5 + 0.5 * np.cos(2 * np.pi * ((xx + yy) * 3 + hue[ids] + o)) for o in (0, 1 / 3, 2 / 3)], -1)
    col = (spec[ids] * 0.25 + sweep * 0.25 + 0.55) * shade[ids][..., None]
    col = mix(col, (1, 1, 1), edge * 0.9)
    ang, tilt = rng.random(n) * 2 * np.pi, 0.25 + rng.random(n) * 0.35
    h = (np.cos(ang) * tilt)[ids] * xx + (np.sin(ang) * tilt)[ids] * yy  # flat tilted facets (normal only)
    save(out, "prism", col, h * 0.05, 1.0, 0.05 - edge * 0.03)


# ---- Japanese myth -------------------------------------------------------------------------------------------------

def kitsunebi(out):  # dusk-indigo steel with drifting pale blue foxfire flames
    flames = [(rng.random() * N, rng.random() * N, 10 + rng.random() * 16) for _ in range(34)]

    def draw(d, ox, oy):
        for cx, cy, r in flames:
            x, y = cx + ox, cy + oy
            d.ellipse([x - r, y - r, x + r, y + r], fill=255)
            d.polygon([(x - r * 0.9, y - r * 0.5), (x - r * 3.4, y + r * 0.1 * np.sin(cx)), (x - r * 0.9, y + r * 0.5)], fill=180)  # tail trails along -U

    f = paint(draw)
    f = np.clip(blur(f, 4) * 1.3, 0, 1)
    halo = np.clip(blur(f, 14) * 2, 0, 1)
    base = mix((0.10, 0.10, 0.22), (0.22, 0.20, 0.38), noise(70))
    fire = ramp(f, [(0, (0, 0, 0)), (0.3, (0.10, 0.30, 0.80)), (0.7, (0.45, 0.80, 1.0)), (1, (0.95, 1.0, 1.0))])
    col = base + fire + np.array((0.05, 0.15, 0.35)) * halo[..., None]
    save(out, "kitsunebi", col, noise(3) * 0.02, 0.6, 0.18 - f * 0.06)


def raijin(out):  # storm-dark blue with branching yellow lightning running along the blade
    bolts = []
    for _ in range(22):  # 9 read as plain navy on a real blade (2026-11-05)
        x, y = rng.random() * N, rng.random() * N
        pts = [(x, y)]
        for _ in range(rng.integers(8, 16)):
            x, y = x + 18 + rng.random() * 30, y + (rng.random() - 0.5) * 50
            pts.append((x, y))
            if rng.random() < 0.25:  # a short fork
                bx, by, br = x, y, [(x, y)]
                for _ in range(rng.integers(2, 5)):
                    bx, by = bx + 12 + rng.random() * 20, by + (rng.random() - 0.3) * 40 * (1 if rng.random() < 0.5 else -1)
                    br.append((bx, by))
                bolts.append((br, 2))
        bolts.append((pts, 5))

    def draw(d, ox, oy):
        for pts, w in bolts:
            d.line([(px + ox, py + oy) for px, py in pts], fill=255, width=w, joint="curve")

    b = paint(draw)
    glow = np.clip(blur(b, 7) * 3.5, 0, 1)
    cloud = noise(90) * 0.6 + noise(25) * 0.4
    base = mix((0.03, 0.04, 0.12), (0.14, 0.17, 0.32), cloud)
    col = base + np.array((1.0, 0.80, 0.15)) * glow[..., None] * 0.9 + np.array((1, 0.95, 0.55)) * b[..., None]
    save(out, "raijin", col, noise(3) * 0.02 + b * 0.1, 0.8, 0.20 - b * 0.1)


def fujin(out):  # pale wind-green with white cloud curls and long streaks
    curls = [(rng.random() * N, rng.random() * N, 14 + rng.random() * 22, rng.random() * 6.28, 1 if rng.random() < 0.5 else -1) for _ in range(22)]
    streaks = [(rng.random() * N, rng.random() * N, 120 + rng.random() * 260) for _ in range(30)]

    def draw(d, ox, oy):
        for cx, cy, r, a0, sgn in curls:
            th = np.linspace(0, 4.2 * np.pi, 120)
            rr = r * th / th[-1]
            pts = [(cx + ox + q * np.cos(a0 + sgn * t), cy + oy + q * np.sin(a0 + sgn * t)) for t, q in zip(th, rr)]
            pts.append((pts[-1][0] + r * 2.5, pts[-1][1]))  # the curl trails off along U
            d.line(pts, fill=255, width=4, joint="curve")
        for sx, sy, ln in streaks:
            d.line([(sx + ox, sy + oy), (sx + ox + ln, sy + oy + 6)], fill=200, width=3)

    w = paint(draw)
    w = np.clip(blur(w, 1.0) * 1.2, 0, 1)
    base = mix((0.50, 0.70, 0.58), (0.70, 0.86, 0.74), noise(80) * 0.7 + noise(10, 2) * 0.3)
    col = mix(base, (0.97, 1.0, 0.97), w)
    save(out, "fujin", col, w * 0.15 + noise(4) * 0.02, 1.0, 0.30 - w * 0.1)


def yurei(out):  # ghost white-blue with faint drifting wisps (meant to be part see-through, like Air)
    wisp = np.zeros((N, N))
    for s, w in ((40, 0.5), (14, 0.35), (5, 0.15)):
        r = 1 - np.abs(noise(s) * 2 - 1)
        wisp += warped(warped(r, 0.10, 60), 0.05, 20) ** 6 * w
    wisp = np.clip(norm(wisp) * 1.5 - 0.1, 0, 1)
    base = mix((0.72, 0.80, 0.90), (0.86, 0.91, 0.97), noise(90))
    col = mix(base, (1, 1, 1), wisp * 0.7) - np.array((0.10, 0.06, 0.0)) * np.clip(noise(50) * 2 - 1.2, 0, 1)[..., None]
    save(out, "yurei", col, noise(3) * 0.01, 0.5, 0.08 + (1 - wisp) * 0.05)


def oni(out):  # crimson with black tiger stripes (oni wear tiger skins)
    warp = (noise(70) - 0.5) * 0.10 + (noise(15) - 0.5) * 0.02
    s = np.sin(2 * np.pi * (xx * 9 + warp * 9 + np.abs(yy - 0.5) * 0.4))  # stripes across the blade
    width = 0.55 + 0.35 * noise(40)
    stripe = np.clip((s - (1 - width)) * 6, 0, 1) * np.clip((noise(25) - 0.25) * 4, 0, 1)
    red = mix((0.55, 0.04, 0.04), (0.85, 0.12, 0.06), noise(30))
    col = mix(red, (0.04, 0.02, 0.02), stripe)
    save(out, "oni", col, -stripe * 0.15 + noise(4) * 0.02, 1.0, 0.25 + stripe * 0.15)


def koi(out):  # white with orange and black koi patches over faint scales
    C, R, rad = 40, 40, 0.75
    u, v = xx * C, yy * R
    fu, fv = u % 1, v % 1
    odd = (np.floor(v).astype(int) % 2) == 1
    fu = np.where(odd, (u + 0.5) % 1, fu)
    sc = np.clip(1 - np.hypot(fu - 0.5, (fv - 0.0) * 1.15) / rad, 0, 1)  # cheap scale bumps
    orange = np.clip((noise(55) * 0.8 + noise(12) * 0.2 - 0.55) * 10, 0, 1)
    black = np.clip((noise(30) - 0.78) * 12, 0, 1) * (1 - orange * 0.5)
    base = mix((0.97, 0.96, 0.92), (0.90, 0.89, 0.86), noise(8))
    col = mix(mix(base, (0.96, 0.40, 0.08), orange), (0.06, 0.05, 0.05), black) * (0.93 + 0.07 * sc)[..., None]
    save(out, "koi", col, sc * 0.08, 1.0, 0.18 + (noise(20) - 0.5) * 0.05)


def sumi(out):  # rice-paper grey with black ink brush strokes along the blade, dry-brush edges
    paper = (0.86 + 0.06 * noise(60) + (noise(1.2) - 0.5) * 0.04)
    stroke = norm(blur(rng.normal(size=(N, N)), 90, 14))
    dry = noise(40, 0.8)  # bristle streaks along U
    ink = np.clip((stroke - 0.62) * 9, 0, 1) * np.clip((dry - 0.18) * 3, 0, 1)
    wash = np.clip((norm(blur(rng.normal(size=(N, N)), 60, 30)) - 0.55) * 2.2, 0, 1) * 0.45
    v = paper * (1 - np.maximum(ink * 0.95, wash))
    col = np.stack([v, v * 0.99, v * 0.97], -1)
    save(out, "sumi", col, -ink * 0.1 + noise(1.5) * 0.03, 1.0, 0.55 - ink * 0.2)


# ---- weird Secrets -------------------------------------------------------------------------------------------------

def antimatter(out):  # inverted: white steel with black smoke and magenta / cyan fringes
    wisp = np.zeros((N, N))
    for s, w in ((40, 0.5), (14, 0.35), (5, 0.15)):
        r = 1 - np.abs(noise(s) * 2 - 1)
        wisp += warped(warped(r, 0.10, 60), 0.05, 20) ** 6 * w
    wisp = np.clip(norm(wisp) * 1.7 - 0.15, 0, 1)
    sh = 4
    r = 1 - np.roll(wisp, sh, 1) * 0.95
    g = 1 - wisp * 0.97
    b = 1 - np.roll(wisp, -sh, 1) * 0.95
    save(out, "antimatter", np.stack([r, g, b], -1), -wisp * 0.05, 0.6, 0.10 + wisp * 0.1)


def static(out):  # TV snow: grey noise, scan lines along U, a few bright rolling bands
    snow = rng.random((N, N))
    snow = 0.6 * snow + 0.4 * np.repeat(rng.random((N, N // 2)), 2, 1)
    scan = 0.85 + 0.15 * (np.arange(N)[:, None] % 4 < 2)
    band = 1 + 0.35 * np.clip(np.sin(2 * np.pi * (yy * 3 + noise(200) * 0.3)) * 3 - 2, 0, 1)
    v = np.clip((0.15 + 0.75 * snow) * scan * band, 0, 1)
    col = np.stack([v * 0.96, v, v * 1.06], -1)
    save(out, "static", col, snow * 0.03, 0.5, 0.35 + (snow - 0.5) * 0.1)


def coderain(out):  # black with green glyph trails running along the blade, bright at each head
    cs = 16
    rows, cols = N // cs, N // cs
    glyphs = rng.random((64, 5, 3)) < 0.5
    cell = np.zeros((N, N))
    bright = np.zeros((rows, cols))
    for r in range(rows):
        for _ in range(rng.integers(1, 3)):
            head, ln = rng.integers(0, cols), rng.integers(6, 26)
            for k in range(ln):
                c = (head - k) % cols
                bright[r, c] = max(bright[r, c], 1 - k / ln)
    gid = rng.integers(0, 64, (rows, cols))
    ri, ci = (yy * N // cs).astype(int), (xx * N // cs).astype(int)
    py, px = ((yy * N) % cs).astype(int), ((xx * N) % cs).astype(int)
    gy, gx = (py - 2) // 3, (px - 3) // 3  # 3 px glyph pixels, rotated so they read along U
    on = (gy >= 0) & (gy < 3) & (gx >= 0) & (gx < 5)
    bit = glyphs[gid[ri, ci], np.clip(gx, 0, 4), np.clip(gy, 0, 2)] & on
    lvl = bright[ri, ci] * bit
    head = (bright[ri, ci] > 0.97) & bit
    col = np.array((0.15, 1.0, 0.35)) * lvl[..., None] ** 1.3 + np.array((0.8, 1.0, 0.85)) * head[..., None] * 0.8
    col = col + np.array((0.0, 0.25, 0.08)) * np.clip(blur(lvl, 3) * 1.5, 0, 1)[..., None]
    save(out, "coderain", col + 0.01, lvl * 0.05, 0.5, 0.2 + 0 * lvl)



# ---- Mythril redo, 2026-11-07 (Allen: "mythril is a legendary, but it doesnt look very legendary": it was the only
# Legendary with no texture, a pale tinted plain metal like Silver) ----------------------------------------------------

def mythril_aurora(out):  # bright silver with flowing cyan / pale violet sheen waves, pearly highlights
    warp = (noise(90) - 0.5) * 0.35 + (noise(25) - 0.5) * 0.06
    t = 0.5 + 0.5 * np.sin(2 * np.pi * (xx * 2 + yy * 1 + warp * 2))
    t2 = 0.5 + 0.5 * np.sin(2 * np.pi * (xx * 1 - yy * 2 + warp * 3 + 0.3))
    silver = (0.30 + 0.12 * noise(40))[..., None] * np.array((0.80, 0.92, 1.10))  # deep moonlit steel
    col = mix(silver, (0.30, 0.95, 1.0), np.clip(t * 2.2 - 1.1, 0, 1) * 0.95)
    col = mix(col, (0.62, 0.50, 1.0), np.clip(t2 * 2.4 - 1.5, 0, 1) * 0.85)
    pearl = np.clip((t * t2) * 2.2 - 1.3, 0, 1)
    col = mix(col, (1, 1, 1), pearl * 0.8)
    save(out, "mythril_aurora", col, t * 0.05 + noise(3) * 0.01, 0.8, 0.06 + (1 - t) * 0.06)


def mythril_flake(out):  # crystalline flakes, silver to turquoise, a few blazing white-cyan, thin bright edges
    d1, d2, ids = vor(18, 0.9)
    n = ids.max() + 1
    k = rng.random(n)
    shade = 0.30 + rng.random(n) * 0.45
    base = np.ones((n, 3)) * shade[:, None] * np.array((0.92, 1.0, 1.04))
    teal = k < 0.45
    base[teal] = base[teal] * np.array((0.55, 0.98, 1.05)) + np.array((0.0, 0.05, 0.08))
    hot = k > 0.90
    base[hot] = np.array((0.85, 1.0, 1.0))
    edge = np.clip(1 - (d2 - d1) * 18 / 0.06, 0, 1)
    sheen = 0.5 + 0.5 * np.sin(2 * np.pi * (xx * 2 + yy + (noise(80) - 0.5) * 0.4))
    col = base[ids] * (0.9 + 0.2 * sheen)[..., None]
    col = mix(col, (0.80, 1.0, 1.0), edge * 0.7)
    ang, tilt = rng.random(n) * 2 * np.pi, 0.2 + rng.random(n) * 0.35
    h = (np.cos(ang) * tilt)[ids] * xx + (np.sin(ang) * tilt)[ids] * yy
    save(out, "mythril_flake", col, h * 0.04, 1.0, 0.05 + (1 - hot[ids]) * 0.06 - edge * 0.03)


def mythril_filigree(out):  # bright silver engraved with glowing cyan elven vines curling along the blade
    vines = []
    for r in range(4):
        y0, amp, ph = (r + 0.5) * N / 4, 30 + rng.random() * 20, rng.random() * 6.28
        vines.append([(x, y0 + amp * np.sin(2 * np.pi * x / (N / 2) + ph)) for x in range(-40, N + 41, 8)])
    curls = []
    for v in vines:
        for i in range(8, len(v) - 8, 11):  # tendrils: a spiral leaving the vine, alternately up and down
            cx, cy = v[i]
            s = 1 if (i // 11) % 2 else -1
            curls.append([(cx + a * 6 + 34 * np.sin(a) * (1 - a / 11), cy + s * 34 * (1 - np.cos(a)) * (1 - a / 11)) for a in np.linspace(0, 8, 40)])

    def draw(d, ox, oy):
        for v in vines:
            d.line([(x + ox, y + oy) for x, y in v], fill=255, width=14)
        for c in curls:
            d.line([(x + ox, y + oy) for x, y in c], fill=255, width=10)

    line = paint(draw)
    glow = np.clip(blur(line, 6) * 2.4, 0, 1)
    silver = (0.42 + 0.14 * noise(60) + 0.03 * noise(3))[..., None] * np.array((0.82, 0.92, 1.08))
    col = silver * (1 - glow[..., None] * 0.2) + np.array((0.05, 0.55, 0.70)) * glow[..., None] * 0.7
    col = mix(col, (0.55, 1.0, 1.0), line)
    save(out, "mythril_filigree", col, -line * 0.25 + noise(3) * 0.01, 1.2, 0.08 + line * 0.05)


ALL = ["carbon", "circuit", "synthwave", "soulfire", "blackhole", "runestone", "clockwork", "bloodmoon", "seraph",
       "infernal", "prism", "kitsunebi", "raijin", "fujin", "yurei", "oni", "koi", "sumi", "antimatter", "static", "coderain"]

if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for name in sys.argv[2:] or ALL:
        globals()[name](out)
        print(name, "ok", flush=True)

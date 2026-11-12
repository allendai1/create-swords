# metal_textures.py: surface maps for ingots and blades (2026-10-23). Allen: "That way we're not just using a solid
# color for all of our ingots/swords", then "Try" (a tinted grey metal MaterialVariant on an ingot and a sword).
# Near-white colour maps, so the material's part Color still tints them (MaterialVariant ColorMap x Part.Color) and
# one set serves all 13 metals. Every tile wraps (periodic FFT blurs, wrapped cells). 1024 px over 4 studs.
#   ingot   -> IngotMetal (Metal)          cast bar: soft hammer dimples, mottled roughness
#   blade   -> BladeShine0/1/2 colour      faint long streaks along U
#   blade0  -> BladeShine0 normal/rough    forged: shallow hammer marks and coarse grind lines, rough 0.55
#   blade1  -> BladeShine1 normal/rough    brushed: grind lines along U, rough 0.30
#   blade2  -> BladeShine2 normal/rough    mirror: faint lines only, rough 0.15
# Metalness stays on the existing BladeShine maps (IngotMetal reuses BladeShine1's).
# Textured metals (Shared/Materials `texture`), one set each for DragonIngot / DragonBlade etc.:
#   dragon     -> Dragon*      (Metal)   overlapping dome scales with dark rims; tinted by Dragonsteel's red
#   melon_rind -> WatermelonIngot (Plastic) wavy dark-green stripes on light green, true colours (part stays white)
#   melon_pulp -> WatermelonBlade (Plastic) pink flesh with black seeds, true colours
#   rainbow    -> Rainbow*     (Metal)   Allen's gradient picture, mirrored both ways, true colours (part white)
#   diamond    -> Diamond*     (Metal)   cut facets, each its own tilted normal, bright edges; tinted icy blue (2026-11-04)
#   gem        -> Gem*         (Metal)   Diamond's cut in plain greys, tinted by Amethyst / Sapphire / Ruby / Emerald (2026-11-05)
#   jade, amber, obsidian -> Jade* / Amber* / Obsidian* (Metal, smooth): veins; honey bands and bubbles; shell ripples
#   (run gem in its own process so it gets Diamond's cut: the rng is shared and seeded once)
# IngotMetal since 2026-11-04: shallower dimples, rough ~0.15 and an all-white metalness map (not from this script).
# Run: python -I metal_textures.py <out dir>, serve the folder on localhost and upload with Studio MCP upload_image.
import os, sys
import numpy as np
from PIL import Image

N = 1024
rng = np.random.default_rng(23)
yy, xx = np.mgrid[0:N, 0:N] / N  # 0..1, x = U


def blur(a, sx, sy=None):  # periodic gaussian, sigma in pixels
    sy = sx if sy is None else sy
    fy, fx = np.fft.fftfreq(N)[:, None], np.fft.fftfreq(N)[None, :]
    g = np.exp(-2 * np.pi ** 2 * ((fx * sx) ** 2 + (fy * sy) ** 2))
    return np.real(np.fft.ifft2(np.fft.fft2(a) * g))


def norm(a):
    return (a - a.min()) / (a.max() - a.min() + 1e-9)


def noise(sx, sy=None):
    return norm(blur(rng.normal(size=(N, N)), sx, sy))


def cells(count, jitter=0.9):  # wrapped Voronoi on a jittered grid: nearest distance, in cell units
    g = int(np.ceil(np.sqrt(count)))
    pts = (np.stack(np.mgrid[0:g, 0:g], -1).reshape(-1, 2) + 0.5 + (rng.random((g * g, 2)) - 0.5) * jitter) / g
    d1 = np.full((N, N), 9.0)
    for py, px in pts:
        for oy in (-1, 0, 1):
            for ox in (-1, 0, 1):
                d1 = np.minimum(d1, np.hypot(xx - (px + ox), yy - (py + oy)))
    return d1 * g


def gray(out, name, v):
    Image.fromarray((np.clip(v, 0, 1) * 255).astype(np.uint8)).save(os.path.join(out, f"{name}.png"))


def normal(out, name, h, k):
    gy = (np.roll(h, -1, 0) - np.roll(h, 1, 0)) * 0.5 * N / 64
    gx = (np.roll(h, -1, 1) - np.roll(h, 1, 1)) * 0.5 * N / 64
    nx, ny, nz = -gx * k, gy * k, np.ones_like(h)
    l = np.sqrt(nx ** 2 + ny ** 2 + nz ** 2)
    n = np.stack([nx / l, ny / l, nz / l], -1) * 0.5 + 0.5  # OpenGL, +Y up
    Image.fromarray((n * 255).astype(np.uint8)).save(os.path.join(out, f"{name}_normal.png"))


def ingot(out):
    d = cells(110)  # about 0.4-stud hammer dimples
    dimple = np.clip(d, 0, 0.75) ** 2  # bowl, deepest at each centre
    mottle = noise(120)
    gray(out, "ingot_color", 0.90 + (mottle - 0.5) * 0.10 + (noise(8) - 0.5) * 0.03 - (0.56 - dimple) * 0.05)
    # 2026-11-04 shinier (Allen: "any ways to make ores shinier?"): dimples 1.6 -> 0.6, rough 0.45-0.55 -> about 0.15-0.2
    normal(out, "ingot", dimple * 0.5 + noise(3) * 0.02, 0.6)
    gray(out, "ingot_rough", 0.15 + (noise(60) - 0.5) * 0.08 + dimple * 0.04)


def blades(out):
    gray(out, "blade_color", 0.93 + (noise(220, 3) - 0.5) * 0.06)
    hammer = np.clip(cells(60), 0, 0.8) ** 2
    grind = noise(160, 1.5)  # long lines along U
    fine = noise(260, 0.8)
    normal(out, "blade0", hammer * 0.35 + grind * 0.08, 1.4)
    gray(out, "blade0_rough", 0.55 + (grind - 0.5) * 0.24 + (hammer - 0.3) * 0.15)
    normal(out, "blade1", grind * 0.10 + fine * 0.05, 1.0)
    gray(out, "blade1_rough", 0.30 + (fine - 0.5) * 0.16)
    normal(out, "blade2", fine * 0.04, 0.6)
    gray(out, "blade2_rough", 0.15 + (fine - 0.5) * 0.08)


def rgb(out, name, c):
    Image.fromarray((np.clip(c, 0, 1) * 255).astype(np.uint8)).save(os.path.join(out, f"{name}.png"))


def mix(a, b, t):  # colour a where t = 0, b where t = 1
    return np.array(a) * (1 - t[..., None]) + np.array(b) * t[..., None]


def dragon(out):
    C, R, rad = 16, 16, 0.78  # scales per tile across and down (R even so the row offset wraps)
    u, v = xx * C, yy * R
    h = np.zeros((N, N))
    for r in range(-1, R + 1):  # later rows lie over earlier ones
        shift = 0.5 * (r % 2)
        for c in range(-1, C + 1):
            for wu in (-C, 0, C):
                for wv in (-R, 0, R):
                    d = np.hypot(u - (c + 0.5 + shift + wu), (v - (r + wv)) * 1.15) / rad
                    h = np.where(d < 1, 1 - d ** 2, h)
    rim = np.clip(h * 4, 0, 1)  # dark gap at each scale's edge
    gray(out, "dragon_color", (0.45 + 0.5 * np.sqrt(h)) * (0.55 + 0.45 * rim) + (noise(4) - 0.5) * 0.04)
    normal(out, "dragon", h * 0.6, 2.2)
    gray(out, "dragon_rough", 0.55 - 0.25 * h + (noise(30) - 0.5) * 0.08)


def watermelon(out):
    warp = (noise(60) - 0.5) * 0.10 + (noise(10) - 0.5) * 0.02
    s = np.sin(2 * np.pi * (yy * 8 + warp))  # stripes along U
    dark = np.clip((s - 0.1) * 3, 0, 1)
    rind = mix((0.55, 0.78, 0.35), (0.12, 0.36, 0.12), dark) * (0.92 + 0.16 * noise(5))[..., None]
    rgb(out, "melon_rind_color", rind)
    normal(out, "melon_rind", noise(25) * 0.15, 1.0)
    gray(out, "melon_rind_rough", 0.5 + (noise(20) - 0.5) * 0.1)
    # flesh: pink with lighter grain, black teardrop seeds on a jittered grid
    pulp = mix((0.86, 0.22, 0.30), (1.0, 0.55, 0.58), noise(6) * 0.6 + noise(40) * 0.4)
    g = 7
    seed = np.zeros((N, N))
    for i in range(g):
        for j in range(g):
            py, px = (i + 0.5 + (rng.random() - 0.5) * 0.6) / g, (j + 0.5 + (rng.random() - 0.5) * 0.6) / g
            for oy in (-1, 0, 1):
                for ox in (-1, 0, 1):
                    dy, dx = (yy - py - oy) * g, (xx - px - ox) * g
                    seed = np.maximum(seed, np.clip(1 - np.hypot(dx / 0.10, dy / 0.18), 0, 1))
    inside = seed > 0
    rgb(out, "melon_pulp_color", np.where(inside[..., None], mix((0.10, 0.07, 0.05), (0.35, 0.28, 0.22), seed ** 4), pulp))
    normal(out, "melon_pulp", seed * 0.4 + noise(6) * 0.05, 1.5)
    gray(out, "melon_pulp_rough", np.where(inside, 0.2, 0.38 + (noise(8) - 0.5) * 0.1))


def rainbow(out):  # 2026-11-10 (Allen: "replace our current rainbow metal with this one"): his Art/Textures/rainbow_gradient.png
    # as the colour map. Studio maps U one way on a blade's front and the other way on its back, from the blade's base
    # (seen 2026-10-23), so the tile is the picture plus its mirror image both ways: with half a tile per blade
    # (StudsPerTile = 2 x its length) both faces run left to right from hilt to tip, and the tile still wraps.
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "Art", "Textures", "rainbow_gradient.png")
    half = np.asarray(Image.open(src).convert("RGB").resize((N // 2, N // 2), Image.LANCZOS), dtype=float) / 255
    row = np.concatenate([half, half[:, ::-1]], 1)
    rgb(out, "rainbow_color", np.concatenate([row, row[::-1]], 0))
    # normal and roughness stay the 2026-10-23 uploads (88693148403940, 116211403159266)


def folds(warp, layers=36):  # pattern-welded steel: bright/dark layers along U, bent by warp (tile units)
    s = np.sin(2 * np.pi * (yy * layers + warp * layers))
    return np.clip(s * 1.6, -1, 1) * 0.5 + 0.5  # sharpened: 0 dark layer, 1 bright layer


def damascus_set(out, name, warp):  # true greys (part white); the etched dark layers sit lower and rougher
    t = folds(warp)
    rgb(out, f"{name}_color", mix((0.30, 0.30, 0.33), (0.86, 0.85, 0.82), t) * (0.96 + 0.08 * noise(3))[..., None])
    normal(out, name, t * 0.12 + noise(3) * 0.01, 1.0)
    gray(out, f"{name}_rough", 0.42 - 0.18 * t + (noise(20) - 0.5) * 0.06)


def damascus(out):  # three folded-steel patterns to choose from
    wild = (noise(70) - 0.5) * 0.14 + (noise(18) - 0.5) * 0.04
    damascus_set(out, "damascus_wild", wild)  # random pattern: meandering layers
    drops = np.clip(1 - cells(40, 0.8) / 0.45, 0, 1) ** 1.5  # rings pushed up by drilled spots
    damascus_set(out, "damascus_drops", wild * 0.4 + drops * 0.12)  # raindrop pattern
    ladder = np.abs(((xx * 7) % 1) - 0.5) * 0.10  # V rungs ground across the blade
    damascus_set(out, "damascus_ladder", wild * 0.4 + ladder)  # ladder pattern


def starmetal(out):  # deep blue-violet nebula with star specks, true colours (part white)
    cloud = noise(90) * 0.6 + noise(25) * 0.4
    base = mix((0.05, 0.05, 0.16), (0.36, 0.20, 0.55), np.clip(cloud * 1.4 - 0.35, 0, 1))
    base = mix(base, (0.20, 0.45, 0.70), np.clip(noise(60) * 2 - 1.2, 0, 1) * 0.6)
    stars = np.clip((rng.random((N, N)) - 0.9985) * 700, 0, 1)
    stars = np.clip(blur(stars, 1.2) * 6, 0, 1)
    rgb(out, "starmetal_color", base + stars[..., None] * 0.9)
    normal(out, "starmetal", noise(3) * 0.02, 0.6)
    gray(out, "starmetal_rough", 0.20 - stars * 0.15 + (noise(30) - 0.5) * 0.04)


def mythril(out):  # crystalline flakes: wrapped cells, each a slightly different brightness and tilt
    g, d1 = 14, np.full((N, N), 9.0)
    pts = (np.stack(np.mgrid[0:g, 0:g], -1).reshape(-1, 2) + 0.5 + (rng.random((g * g, 2)) - 0.5) * 0.9) / g
    shade, ids = np.zeros((N, N)), rng.random(g * g)
    for k, (py, px) in enumerate(pts):
        for oy in (-1, 0, 1):
            for ox in (-1, 0, 1):
                d = np.hypot(xx - (px + ox), yy - (py + oy))
                near = d < d1
                d1, shade = np.where(near, d, d1), np.where(near, ids[k], shade)
    gray(out, "mythril_color", 0.82 + shade * 0.16)
    normal(out, "mythril", shade * 0.03 + noise(2) * 0.01, 1.0)
    gray(out, "mythril_rough", 0.12 + shade * 0.12)


def warped(f, amt, sx):  # sample f at a wrapped, noise-shifted position
    dy = ((noise(sx) - 0.5) * amt * N).astype(int)
    dx = ((noise(sx) - 0.5) * amt * N).astype(int)
    return f[(np.arange(N)[:, None] + dy) % N, (np.arange(N)[None, :] + dx) % N]


def doppler(out):  # CS:GO-style candy smoke (after Allen's reference): wisps over black, red / green / blue bands along U
    wisp = np.zeros((N, N))
    for s, w in ((40, 0.5), (14, 0.35), (5, 0.15)):  # ridged turbulence, folded twice to curl like smoke
        r = 1 - np.abs(noise(s) * 2 - 1)
        wisp += warped(warped(r, 0.10, 60), 0.05, 20) ** 6 * w
    wisp = np.clip(norm(wisp) * 1.6 - 0.1, 0, 1)
    t = (xx + (noise(80) - 0.5) * 0.12) % 1  # three bands per tile, soft edges, wraps
    band = np.stack([np.clip(1 - np.abs(((t - c + 0.5) % 1) - 0.5) * 4.5, 0, 1) for c in (0.17, 0.5, 0.83)], -1)
    glow = band * (0.10 + 0.95 * wisp + 0.15 * noise(90))[..., None]
    rgb(out, "doppler_color", glow * np.array((1.0, 0.85, 1.0)) + 0.025)
    normal(out, "doppler", noise(2) * 0.015, 0.5)  # anodised: smooth
    gray(out, "doppler_rough", 0.14 + (1 - wisp) * 0.06)


def diamond(out):  # 2026-11-04 (Allen: "Diamond doesnt look diamond enough"; Glass ignores variants): cut facets, each a flat
    # tilted plane (its own normal) in ice-white, a few pale cyan or faintly rainbow ("fire"), bright thin edges; true colours
    facets(out, "diamond", 0.80, 0.30, 0.10, 0.9)


def gem(out):  # 2026-11-05 (Allen: "try cut gems"): Diamond's facets in plain greys with more spread, tinted by each gem's
    # colour (Amethyst, Sapphire, Ruby, Emerald); same seed and draw order, so the same cut as Diamond
    facets(out, "gem", 0.62, 0.0, 0.0, 0.6)


def facets(out, name, lo, cyan_share, fire_share, edge_white):
    g = 7
    pts = (np.stack(np.mgrid[0:g, 0:g], -1).reshape(-1, 2) + 0.5 + (rng.random((g * g, 2)) - 0.5) * 0.85) / g
    d1, d2, ids = np.full((N, N), 9.0), np.full((N, N), 9.0), np.zeros((N, N), int)
    for k, (py, px) in enumerate(pts):
        for oy in (-1, 0, 1):
            for ox in (-1, 0, 1):
                d = np.hypot(xx - (px + ox), yy - (py + oy))
                near = d < d1
                d2 = np.where(near, d1, np.minimum(d2, d))
                d1, ids = np.where(near, d, d1), np.where(near, k, ids)
    edge = np.clip(1 - (d2 - d1) * g / 0.06, 0, 1)  # 1 on a facet border
    n = g * g
    shade = lo + rng.random(n) * (1 - lo)
    hue = rng.random(n)
    kind = rng.random(n)  # diamond: most ice-white, some pale cyan, a few with fire
    base = np.ones((n, 3)) * shade[:, None]
    cyan = kind < cyan_share
    base[cyan] *= np.array((0.86, 0.96, 1.0))
    fire = kind > 1 - fire_share
    fc = np.stack([0.5 + 0.5 * np.cos(2 * np.pi * (hue + o)) for o in (0, 1 / 3, 2 / 3)], -1)
    base[fire] = base[fire] * 0.88 + fc[fire] * 0.12
    col = base[ids] * (1 + (noise(2) - 0.5) * 0.02)[..., None]
    rgb(out, f"{name}_color", mix(col, (1, 1, 1), edge * edge_white))
    ang, tilt = rng.random(n) * 2 * np.pi, 0.25 + rng.random(n) * 0.35
    nx, ny = (np.cos(ang) * tilt)[ids], (np.sin(ang) * tilt)[ids]
    l = np.sqrt(nx ** 2 + ny ** 2 + 1)
    Image.fromarray(((np.stack([nx / l, ny / l, 1 / l], -1) * 0.5 + 0.5) * 255).astype(np.uint8)).save(os.path.join(out, f"{name}_normal.png"))
    gray(out, f"{name}_rough", 0.05 - edge * 0.03)


# Polished stones, 2026-11-05 (Allen: "for stones make their appropriate textures"): near-white maps tinted by the part
# colour, on Plastic (not metallic), very smooth so the sky shows as a gloss
def jade(out):  # cloudy, with pale veins and a few dark flecks
    cloud = noise(90) * 0.6 + noise(25) * 0.4
    vein = sum(np.clip(1 - np.abs(warped(noise(s), 0.08, 30) - 0.5) * k, 0, 1) * w for s, k, w in ((70, 70, 0.22), (30, 90, 0.14)))  # thin pale lines where the noise crosses 0.5
    fleck = np.clip((noise(3) - 0.86) * 8, 0, 1)
    gray(out, "jade_color", (0.56 + 0.40 * cloud) * (1 - fleck * 0.35) + vein)
    normal(out, "jade", noise(4) * 0.02, 0.4)
    gray(out, "jade_rough", 0.10 + cloud * 0.06)


def amber(out):  # honey with flowing darker bands and a few small bubbles
    warp = (noise(80) - 0.5) * 0.6 + (noise(20) - 0.5) * 0.08
    band = 0.5 + 0.5 * np.sin(2 * np.pi * (yy * 3 + warp))
    bub = np.clip((rng.random((N, N)) - 0.99975) * 3000, 0, 1)
    bub = np.clip(blur(bub, 3) * 20, 0, 1)  # soft dots about 6 px
    gray(out, "amber_color", 0.45 + 0.55 * band * (0.8 + 0.2 * noise(10)) + bub * 0.35)
    normal(out, "amber", bub * 0.6 + noise(5) * 0.01, 1.2)
    gray(out, "amber_rough", 0.07 + (1 - band) * 0.04 - bub * 0.04)


def obsidian(out):  # glassy black with conchoidal ripples (rings round a few chip points) and a faint sheen
    ripple, fade = np.zeros((N, N)), np.zeros((N, N))
    for _ in range(7):
        py, px = rng.random(2)
        a0 = rng.random() * 2 * np.pi
        dx, dy = xx - px, yy - py
        dx, dy = (dx + 0.5) % 1 - 0.5, (dy + 0.5) % 1 - 0.5  # nearest wrapped copy
        d = np.hypot(dx, dy) + (noise(30) - 0.5) * 0.04
        shell = np.clip(np.cos(np.arctan2(dy, dx) - a0) * 1.5 + 0.3, 0, 1)  # a shell-shaped fan, not a full ring
        f = np.clip(1 - d / 0.30, 0, 1) ** 1.5 * shell
        take = f > fade
        ripple = np.where(take, 0.5 + 0.5 * np.cos(2 * np.pi * d * 16), ripple)
        fade = np.maximum(fade, f)
    sheen = noise(120)
    gray(out, "obsidian_color", 0.80 + ripple * fade * 0.12 + sheen * 0.08)
    normal(out, "obsidian", ripple * fade * 0.5 + noise(4) * 0.01, 1.4)
    gray(out, "obsidian_rough", 0.05 + (1 - fade) * 0.04)


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for f in [globals()[a] for a in sys.argv[2:]] or (ingot, blades, dragon, watermelon):
        f(out)
        print(f.__name__, "ok")

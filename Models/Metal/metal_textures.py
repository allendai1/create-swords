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
#   rainbow    -> Rainbow*     (Metal)   soft vertical spectrum bands with paper grain, true colours (part white)
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
    normal(out, "ingot", dimple * 0.5 + noise(3) * 0.02, 1.6)
    gray(out, "ingot_rough", 0.45 + (noise(60) - 0.5) * 0.24 + dimple * 0.1)


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


def rainbow(out):  # Allen's Art/Textures/rainbow.webp is a watermarked stock preview, so this is an original in its style
    # soft vertical bands, red to violet and back across the tile: Studio maps U one way on a blade's front and the other
    # way on its back, from the blade's base (seen 2026-10-23), so a one-way sweep ran backwards on one face. With half a
    # tile per blade (StudsPerTile = 2 x its length) both faces go red at the hilt to violet at the tip.
    t = (xx + (noise(90) - 0.5) * 0.06 + (noise(12) - 0.5) * 0.01) % 1
    hue = 0.76 * (1 - np.abs(1 - 2 * t))
    i, f = np.floor(hue * 6).astype(int) % 6, hue * 6 - np.floor(hue * 6)
    s, v = 0.42, 0.90
    p, q, t = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    r = np.choose(i, [v + 0 * f, q, p + 0 * f, p + 0 * f, t, v + 0 * f])
    g = np.choose(i, [t, v + 0 * f, v + 0 * f, q, p + 0 * f, p + 0 * f])
    b = np.choose(i, [p + 0 * f, p + 0 * f, t, v + 0 * f, v + 0 * f, q])
    grain = (noise(1.0) - 0.5) * 0.14 + (noise(30) - 0.5) * 0.06
    fibre = np.clip((noise(5, 0.6) - 0.78) * 6, 0, 1) * 0.12 - np.clip((noise(4, 0.8) - 0.80) * 6, 0, 1) * 0.10  # pale and dark fibres, as in handmade paper
    rgb(out, "rainbow_color", np.stack([r, g, b], -1) * (1 + grain + fibre)[..., None])
    normal(out, "rainbow", noise(2) * 0.05 + fibre * 0.3, 1.0)
    gray(out, "rainbow_rough", 0.32 + (noise(20) - 0.5) * 0.08)


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for f in [globals()[a] for a in sys.argv[2:]] or (ingot, blades, dragon, watermelon):
        f(out)
        print(f.__name__, "ok")

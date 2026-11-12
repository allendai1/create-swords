# style_textures.py: hand-painted tiles for the Genshin-style street test (2026-10-22). Allen: "build the Genshin-style
# test of the gate street: lighting, painted road/wall/roof textures, one smooth tree and one softened building."
# Painted look: flat shapes with soft light painted in (top-left light, darker rims), wide low-frequency colour drift,
# a light posterize for brush bands, almost no fine noise. Near-grey with warm lights and cool shadows, so the part
# colour still tints them (MaterialVariant ColorMap x Part.Color). Every tile wraps (periodic FFT blurs, wrapped cells).
#   stone   -> PaintStone   (Slate, 8)       rounded cobbles with dark gaps
#   earth   -> PaintEarth   (Ground, 32)     packed earth: big soft patches, strokes along the street, few pebbles
#   plaster -> PaintPlaster (Plaster, 16)    cream wall wash with faint vertical strokes
#   roof    -> PaintRoof    (ClayRoofTiles, 6) hongawara: wide pans and narrow round covers, soft course laps
#   roof_trim -> PaintRoofTrim (ClayRoofTiles, 6) the roof's tone, no tiles (round trims)
#   wood    -> PaintWood    (Wood, 8)        painted grain streaks along U, soft plank seams
# Each also gets a gentle normal map and a flat rough roughness map (no shine on painted surfaces).
# Run: python -I style_textures.py <out dir>, serve the folder on localhost and upload with Studio MCP upload_image.
import os, sys
import numpy as np
from PIL import Image

N = 1024
rng = np.random.default_rng(22)
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


def smooth(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def paint(v, steps=7, amt=0.35):  # soft posterize: brush bands without hard banding
    q = np.round(v * steps) / steps
    return v * (1 - amt) + q * amt


def save(out, name, v, warm=0.10, h=None, k=2.0):
    v = np.clip(v, 0, 1)
    d = v - 0.5  # warm lights, cool shadows
    rgb = np.stack([v * (1 + warm * d), v * (1 + 0.3 * warm * d), v * (1 - warm * d)], -1)
    Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(os.path.join(out, f"{name}_color.png"))
    h = v if h is None else h
    gy = (np.roll(h, -1, 0) - np.roll(h, 1, 0)) * 0.5 * N / 64
    gx = (np.roll(h, -1, 1) - np.roll(h, 1, 1)) * 0.5 * N / 64
    nx, ny, nz = -gx * k, gy * k, np.ones_like(h)
    l = np.sqrt(nx ** 2 + ny ** 2 + nz ** 2)
    n = np.stack([nx / l, ny / l, nz / l], -1) * 0.5 + 0.5  # OpenGL, +Y up
    Image.fromarray((n * 255).astype(np.uint8)).save(os.path.join(out, f"{name}_normal.png"))
    Image.fromarray(np.full((64, 64), 235, np.uint8)).save(os.path.join(out, f"{name}_rough.png"))


def cells(count, jitter=0.8):  # wrapped Voronoi on a jittered grid: nearest id, nearest and second distance, centre
    g = int(np.ceil(np.sqrt(count)))
    pts = (np.stack(np.mgrid[0:g, 0:g], -1).reshape(-1, 2) + 0.5 + (rng.random((g * g, 2)) - 0.5) * jitter) / g
    d1 = np.full((N, N), 9.0); d2 = np.full((N, N), 9.0); idx = np.zeros((N, N), int)
    cx = np.zeros((N, N)); cy = np.zeros((N, N))
    for i, (py, px) in enumerate(pts):
        for oy in (-1, 0, 1):
            for ox in (-1, 0, 1):
                d = np.hypot(xx - (px + ox), yy - (py + oy))
                closer = d < d1
                d2 = np.where(closer, d1, np.minimum(d2, d))
                cx = np.where(closer, px + ox, cx); cy = np.where(closer, py + oy, cy)
                idx = np.where(closer, i, idx); d1 = np.where(closer, d, d1)
    return idx, d1, d2, cx, cy, g


def stone(out):
    idx, d1, d2, cx, cy, g = cells(36)
    e = (d2 - d1) * g  # distance to the gap, in cell units
    tone = rng.uniform(0.66, 0.86, idx.max() + 1)[idx]
    light = np.clip(((cx - xx) + (cy - yy)) * g * 0.45, -0.5, 0.5)  # lit toward the top-left of each stone
    bevel = smooth(0.04, 0.32, e)
    v = tone + light * 0.16 * bevel - (1 - bevel) * 0.22 + (noise(40) - 0.5) * 0.08
    v = paint(v)
    v = np.where(e < 0.045, 0.30 + (noise(6) - 0.5) * 0.05, v)
    save(out, "stone", v, warm=0.14, h=smooth(0.0, 0.35, e), k=3.0)


def earth(out):
    big, mid = noise(150), noise(45)
    streak = noise(80, 10)  # long strokes along U (the street)
    v = 0.80 + (big - 0.5) * 0.12 + (mid - 0.5) * 0.06 + (streak - 0.5) * 0.06
    v = paint(v, 10, 0.2)
    idx, d1, d2, cx, cy, g = cells(49, 1.0)  # a few painted pebbles at some cell centres
    keep = rng.random(idx.max() + 1)[idx] < 0.25
    r = 0.035 + 0.025 * rng.random(idx.max() + 1)[idx]  # about 0.2-0.3 studs at 32 studs per tile
    peb = keep & (d1 * g < r)
    lit = np.clip(((cx - xx) + (cy - yy)) * g / r, -1, 1)
    v = np.where(peb, 0.74 + lit * 0.06, np.where(keep & (d1 * g < r + 0.02), v - 0.06, v))
    save(out, "earth", v, warm=0.12, h=np.where(peb, 0.3, 0) + big * 0.2, k=1.2)


def plaster(out):
    v = 0.90 + (noise(180) - 0.5) * 0.08 + (noise(70) - 0.5) * 0.04 + (noise(12, 60) - 0.5) * 0.03  # wash + soft vertical strokes
    save(out, "plaster", paint(v, 12, 0.15), warm=0.08, k=0.6)


def roof(out):
    # 2026-11-05 (Allen: "can you fix the clay roof tiles, they look odd"): hongawara, not identical barrels. Across U,
    # 6 tiles a tile (1 stud each at 6 studs per tile): a wide concave pan, then a narrow round cover roll on its seam;
    # down V, 4 courses with a soft lap shadow, the pans and rolls running on through it as on a real roof. Each tile
    # gets its own tone. Was: 8 equal rolls with a hard dark band at every course (stacked-barrel look).
    cols, courses = 6, 4
    u = (xx * cols) % 1.0
    w = (yy * courses) % 1.0
    col = np.floor(xx * cols).astype(int) % cols
    row = np.floor(yy * courses).astype(int) % courses
    R = 0.30  # the cover roll's width, centred on the tile's seam (u = 0)
    du = (u + 0.5) % 1.0 - 0.5  # -0.5..0.5, 0 on the seam
    t = np.clip(np.abs(du) / (R / 2), 0, 1)  # 0..1 across the roll
    on_roll = np.abs(du) < R / 2
    roll_h = np.sqrt(np.clip(1 - t ** 2, 0, 1))  # round cover
    pu = np.clip((u - R / 2) / (1 - R), 0, 1)  # 0..1 across the pan
    pan_h = 0.35 - 0.35 * np.sin(np.pi * pu)  # shallow trough
    # light from the left: the roll's left flank lit, the pan's right side (facing left) lit
    roll_v = 0.64 + 0.30 * roll_h - 0.22 * np.sign(du) * (1 - roll_h)
    pan_v = 0.62 + 0.07 * (2 * pu - 1) - 0.03 * np.sin(np.pi * pu)  # right side faces the light; trough a touch darker
    gap = smooth(0.0, 0.05, np.abs(np.abs(du) - R / 2))  # dark crease where roll meets pan
    v = np.where(on_roll, roll_v, pan_v) * (0.80 + 0.20 * gap)
    lap = 0.84 + 0.16 * smooth(0.0, 0.25, w)  # soft shadow under the course above
    lip = 1.0 + 0.05 * smooth(0.90, 1.0, w)  # a little light on each tile's lower edge
    tone = 1.0 + (rng.random((courses, cols * 2)) - 0.5) * 0.08
    seam = np.round(xx * cols).astype(int) % cols  # a roll straddles two pans: it takes its seam's tone
    v = v * lap * lip * np.where(on_roll, tone[row, seam * 2 + 1], tone[row, col * 2])
    v = paint(v + (noise(50) - 0.5) * 0.04, 9, 0.25)
    h = np.where(on_roll, 0.45 + 0.55 * roll_h, pan_h * 0.6) * (0.85 + 0.15 * smooth(0.0, 0.22, w))
    save(out, "roof", v, warm=0.10, h=h, k=2.0)


def roof_trim(out):
    # 2026-11-05: PaintRoofTrim, for the round roof trims (ridges, eaves, ridge caps, wall ridges, knobs). The tile
    # pattern wrapped round a cylinder read as a coiled spring; these get the roof's painted tone with no tiles.
    v = 0.70 + (noise(160) - 0.5) * 0.08 + (noise(40) - 0.5) * 0.04
    save(out, "roof_trim", paint(v, 9, 0.25), warm=0.10, h=np.zeros((N, N)), k=0.0)


def wood(out):
    planks = 4
    w = (yy * planks) % 1.0
    plank = np.floor(yy * planks).astype(int) % planks
    tone = np.array([0.74, 0.80, 0.70, 0.77])[plank]
    grain = noise(90, 2.0)
    rings = np.sin((grain * 9 + noise(200) * 3) * np.pi) * 0.5 + 0.5  # wavy painted streaks
    seam = smooth(0.0, 0.06, np.minimum(w, 1 - w))
    v = tone + (rings - 0.5) * 0.10 + (noise(120) - 0.5) * 0.06
    v = paint(v, 7, 0.4) * (0.7 + 0.3 * seam)
    save(out, "wood", v, warm=0.12, h=seam * 0.5 + rings * 0.05, k=1.5)


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    only = sys.argv[2:]  # e.g. "roof" to remake one
    for f in (stone, earth, plaster, roof, roof_trim, wood):
        if only and f.__name__ not in only:
            continue
        f(out)
        print(f.__name__, "ok")

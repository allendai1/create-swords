# style_textures.py: hand-painted tiles for the Genshin-style street test (2026-10-22). Allen: "build the Genshin-style
# test of the gate street: lighting, painted road/wall/roof textures, one smooth tree and one softened building."
# Painted look: flat shapes with soft light painted in (top-left light, darker rims), wide low-frequency colour drift,
# a light posterize for brush bands, almost no fine noise. Near-grey with warm lights and cool shadows, so the part
# colour still tints them (MaterialVariant ColorMap x Part.Color). Every tile wraps (periodic FFT blurs, wrapped cells).
#   stone   -> PaintStone   (Slate, 8)       rounded cobbles with dark gaps
#   earth   -> PaintEarth   (Ground, 32)     packed earth: big soft patches, strokes along the street, few pebbles
#   plaster -> PaintPlaster (Plaster, 16)    cream wall wash with faint vertical strokes
#   roof    -> PaintRoof    (ClayRoofTiles, 6) kawara rolls with a lit crest and a shadow at each course
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
    rolls = 8  # tile rolls across U, courses down V
    u = (xx * rolls) % 1.0
    prof = np.sin(np.pi * u)  # round kawara roll
    crest = np.exp(-((u - 0.42) / 0.12) ** 2)  # painted light on the roll's crest
    courses = 4
    w = (yy * courses) % 1.0
    lap = smooth(0.0, 0.18, w)  # shadow under the course above
    v = 0.48 + prof * 0.22 + crest * 0.18
    v = v * (0.72 + 0.28 * lap) - (1 - smooth(0.0, 0.10, prof)) * 0.12
    v = paint(v + (noise(60) - 0.5) * 0.05, 7, 0.4)
    save(out, "roof", v, warm=0.10, h=prof * lap, k=2.5)


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
    for f in (stone, earth, plaster, roof, wood):
        f(out)
        print(f.__name__, "ok")

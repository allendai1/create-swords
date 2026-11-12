# secret_metals.py: the moving Secret metals (2026-11-10, Allen picked "Moving texture + particles", held swords too,
# and Galaxy, Lava Lamp, Glitch; vault Sessions/2026-11-10#Secret metals: moving textures and a new lineup).
# Each metal: a base colour map for <Name>Ingot / <Name>Blade (true colours, the part stays white), plus a see-through
# overlay tile the client scrolls or jumps over the blade and ingot (StarterPlayerScripts.SecretMetalFx), plus shared
# particle sprites. Every tile wraps.
#   galaxy   -> galaxy_color (vivid teal / magenta nebula, brighter than Starmetal's), galaxy_over (stars, drifting)
#   lavalamp -> lavalamp_color (purple to magenta liquid), lavalamp_over (soft orange blobs, rising)
#   glitch   -> glitch_color (pink-and-black missing-texture checker), glitch_over (RGB-split bars, jumping)
#   sprites  -> spark_star (4-point twinkle), spark_blob (soft dot), spark_pixel (hard square), all white
# Run: py -3.11 -I secret_metals.py <out dir> [names...]; upload with Development/upload_asset.py.
import os
import sys

import numpy as np
from PIL import Image

N = 1024
rng = np.random.default_rng(1110)


def grid(n):
    yy, xx = np.mgrid[0:n, 0:n] / n
    return yy, xx


def blur(a, s):  # periodic gaussian, sigma in pixels
    n = a.shape[0]
    f = np.fft.fftfreq(n)
    g = np.exp(-2 * np.pi ** 2 * ((f[None, :] * s) ** 2 + (f[:, None] * s) ** 2))
    return np.real(np.fft.ifft2(np.fft.fft2(a) * g))


def norm(a):
    return (a - a.min()) / (a.max() - a.min() + 1e-9)


def noise(s, n=N):
    return norm(blur(rng.normal(size=(n, n)), s))


def mix(a, b, t):
    return np.array(a) * (1 - t[..., None]) + np.array(b) * t[..., None]


def save_rgb(out, name, c):
    Image.fromarray((np.clip(c, 0, 1) * 255).astype(np.uint8), "RGB").save(os.path.join(out, name + ".png"))


def save_rgba(out, name, c, a):
    px = np.concatenate([np.clip(c, 0, 1), np.clip(a, 0, 1)[..., None]], -1)
    Image.fromarray((px * 255).astype(np.uint8), "RGBA").save(os.path.join(out, name + ".png"))


def dots(n, count, radius, size_spread=0.0):  # wrapped soft dots: (intensity map) at random spots
    yy, xx = grid(n)
    m = np.zeros((n, n))
    for _ in range(count):
        py, px = rng.random(2)
        r = radius * (1 + size_spread * (rng.random() - 0.5) * 2)
        dy = (yy - py + 0.5) % 1 - 0.5
        dx = (xx - px + 0.5) % 1 - 0.5
        m = np.maximum(m, np.exp(-(dx ** 2 + dy ** 2) / (2 * r ** 2)) * (0.6 + 0.4 * rng.random()))
    return m


def galaxy(out):
    cloud = noise(80) * 0.55 + noise(22) * 0.45
    base = mix((0.03, 0.02, 0.10), (0.42, 0.10, 0.62), np.clip(cloud * 1.6 - 0.45, 0, 1))
    base = mix(base, (0.95, 0.30, 0.70), np.clip(noise(50) * 2.2 - 1.35, 0, 1) * 0.8)  # magenta clouds
    base = mix(base, (0.15, 0.80, 0.90), np.clip(noise(70) * 2.2 - 1.40, 0, 1) * 0.7)  # teal clouds
    fine = np.clip((rng.random((N, N)) - 0.997) * 400, 0, 1)
    save_rgb(out, "galaxy_color", base + np.clip(blur(fine, 0.8) * 5, 0, 1)[..., None] * 0.7)
    n = 512  # the overlay: bright stars of a few sizes, a little blue or pink, on clear
    stars = np.clip(dots(n, 70, 0.0035, 0.6) * 1.4, 0, 1)
    big = dots(n, 8, 0.008)
    yy, xx = grid(n)
    a = np.clip(stars + big, 0, 1)
    tint = mix((0.85, 0.92, 1.0), (1.0, 0.85, 0.95), noise(40, n))
    save_rgba(out, "galaxy_over", tint, a)


def lavalamp(out):
    yy, xx = grid(N)
    flow = noise(120) * 0.7 + noise(40) * 0.3
    base = mix((0.24, 0.04, 0.38), (0.80, 0.10, 0.45), np.clip(flow * 1.5 - 0.25, 0, 1))
    save_rgb(out, "lavalamp_color", base)
    n = 512  # the overlay: soft-edged wax blobs, stretched a little along the direction they rise (U)
    m = np.zeros((n, n))
    gy, gx = grid(n)
    for _ in range(14):
        py, px = rng.random(2)
        rx, ry = 0.05 + rng.random() * 0.06, 0.04 + rng.random() * 0.04
        dy = (gy - py + 0.5) % 1 - 0.5
        dx = (gx - px + 0.5) % 1 - 0.5
        m += np.exp(-((dx / rx) ** 2 + (dy / ry) ** 2) * 1.6)
    wax = np.clip((m - 0.45) * 3.0, 0, 1)  # metaball threshold: blobs merge softly
    core = np.clip((m - 0.9) * 2.0, 0, 1)
    save_rgba(out, "lavalamp_over", mix((1.0, 0.45, 0.10), (1.0, 0.85, 0.35), core), wax * 0.95)


def glitch(out):
    yy, xx = grid(N)
    cells = 8  # big checker cells, like Roblox's missing-texture
    chk = ((np.floor(xx * cells) + np.floor(yy * cells)) % 2).astype(float)
    base = mix((0.03, 0.02, 0.04), (1.0, 0.10, 0.85), chk)
    save_rgb(out, "glitch_color", base)
    n = 512  # the overlay: horizontal (along V) torn bars in cyan, magenta and white, mostly clear
    c = np.zeros((n, n, 3))
    a = np.zeros((n, n))
    for _ in range(22):
        y0 = rng.integers(0, n)
        h = int(rng.integers(3, 22))
        x0 = rng.integers(0, n)
        w = int(rng.integers(n // 8, n // 2))
        col = [(0.0, 1.0, 1.0), (1.0, 0.0, 1.0), (1.0, 1.0, 1.0), (0.1, 1.0, 0.3)][rng.integers(0, 4)]
        rows = np.arange(y0, y0 + h) % n
        cols = np.arange(x0, x0 + w) % n
        c[np.ix_(rows, cols)] = col
        a[np.ix_(rows, cols)] = 0.55 + rng.random() * 0.35
    save_rgba(out, "glitch_over", c, a)


def sprites(out):
    n = 128
    yy, xx = grid(n)
    dx, dy = xx - 0.5, yy - 0.5
    r = np.hypot(dx, dy)
    white = np.ones((n, n, 3))
    star = np.exp(-(r / 0.06) ** 2) + np.exp(-(np.abs(dx) / 0.012) ** 2) * np.exp(-(np.abs(dy) / 0.35) ** 2) \
        + np.exp(-(np.abs(dy) / 0.012) ** 2) * np.exp(-(np.abs(dx) / 0.35) ** 2)
    save_rgba(out, "spark_star", white, np.clip(star, 0, 1))
    save_rgba(out, "spark_blob", white, np.clip(np.exp(-(r / 0.22) ** 2) * 1.2, 0, 1))
    sq = ((np.abs(dx) < 0.36) & (np.abs(dy) < 0.36)).astype(float)
    save_rgba(out, "spark_pixel", white, sq)


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for f in [globals()[a] for a in sys.argv[2:]] or (galaxy, lavalamp, glitch, sprites):
        f(out)
        print(f.__name__, "ok")

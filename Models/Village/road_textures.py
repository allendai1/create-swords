# road_textures.py: the street textures build_simple.luau's ROAD_STYLE uses (2026-10-22). Allen: "The roads look ugly."
# Greyscale 1024 px tiles, tinted in Studio by the part colour; fixed seeds, so a rerun makes the same images.
#   slab_*  -> MaterialVariant TownSlab  (Pavement, StudsPerTile 16, Regular): tidy cut stone, 6 courses 2.67 studs wide,
#              slabs 4 studs long in running bond; per-slab tone +-5, faint grain, thin dark joints with a soft bevel.
#   earth_* -> MaterialVariant TownEarth (Ground, StudsPerTile 24, Organic): packed earth, calm two-scale mottling, faint
#              streaks along the street, sparse small pebbles; periodic (FFT) blurs, so it tiles.
# Run: python road_textures.py <out dir>. Upload the PNGs (Studio MCP upload_image) and put the ids in build_simple.luau.
import os, sys
import numpy as np
from PIL import Image, ImageFilter

N = 1024


def normal_map(h, k):  # OpenGL (+Y up)
    gy, gx = np.gradient(h)
    nx, ny, nz = -gx * k, gy * k, np.ones_like(h)
    l = np.sqrt(nx ** 2 + ny ** 2 + nz ** 2)
    return Image.fromarray(((np.stack([nx / l, ny / l, nz / l], -1) * 0.5 + 0.5) * 255).astype(np.uint8))


def slabs(out):
    STUDS = 16
    rng = np.random.default_rng(7)
    y, x = np.mgrid[0:N, 0:N] / (N / STUDS)  # studs; x along the street (U), y across
    CW = STUDS / 6
    course = np.floor(y / CW).astype(int)
    xs = x + (course % 2) * 2.0
    slab = np.floor(xs / 4.0).astype(int) % 4
    d = np.minimum(np.minimum(xs % 4.0, 4.0 - xs % 4.0), np.minimum(y % CW, CW - y % CW))  # to the nearest joint
    JW, BEV = 0.06, 0.14  # half joint width, bevel width
    base = 196 + rng.normal(0, 5, size=(6, 4))[course % 6, slab]
    noise = lambda s, blur: np.asarray(Image.fromarray(rng.normal(128, s, (N, N)).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur)), dtype=float) - 128
    grain = noise(40, 1.2)
    mottle = np.asarray(Image.fromarray(rng.normal(128, 60, (N // 16, N // 16)).clip(0, 255).astype(np.uint8)).resize((N, N), Image.Resampling.BICUBIC), dtype=float) - 128
    fine = noise(50, 0.5)
    col = base + grain * 0.12 + fine * 0.18 + mottle * 0.04
    col = col * (0.86 + 0.14 * np.clip((d - JW) / BEV, 0, 1))
    col = np.where(d < JW, 112 + grain * 0.1, col)
    Image.fromarray(np.stack([col, col * 0.995, col * 0.985], -1).clip(0, 255).astype(np.uint8)).save(os.path.join(out, "slab_color.png"))
    normal_map((np.clip((d - JW) / BEV, 0, 1) ** 0.6 + grain * 0.002) * 6.0, 1).save(os.path.join(out, "slab_normal.png"))


def earth(out):
    rng = np.random.default_rng(11)
    fy, fx = np.fft.fftfreq(N)[:, None], np.fft.fftfreq(N)[None, :]

    def blur(a, sx, sy=None):
        sy = sx if sy is None else sy
        return np.real(np.fft.ifft2(np.fft.fft2(a) * np.exp(-2 * np.pi ** 2 * ((fx * sx) ** 2 + (fy * sy) ** 2))))

    def norm(a):
        return (a - a.mean()) / a.std()

    big = norm(blur(rng.normal(size=(N, N)), 60))
    mid = norm(blur(rng.normal(size=(N, N)), 14))
    streak = norm(blur(rng.normal(size=(N, N)), 40, 3))  # long along x (U), thin across
    fine = norm(blur(rng.normal(size=(N, N)), 1.2))
    col = 200 + big * 5 + mid * 4 + streak * 2.5 + fine * 4
    h = big * 0.2 + mid * 0.3 + fine * 0.15
    yy, xx = np.mgrid[0:N, 0:N]
    for _ in range(260):  # pebbles: small soft discs, a little darker or lighter
        cx, cy, r = rng.integers(0, N), rng.integers(0, N), rng.uniform(2.5, 6.5)
        dx, dy = (xx - cx + N // 2) % N - N // 2, (yy - cy + N // 2) % N - N // 2
        m = np.clip(1 - np.sqrt(dx ** 2 + dy ** 2) / r, 0, 1)
        if m.max() == 0:
            continue
        col += m ** 0.5 * rng.choice([-26, -18, 14])
        h += m ** 0.7 * 1.2
    Image.fromarray(np.stack([col, col, col], -1).clip(0, 255).astype(np.uint8)).save(os.path.join(out, "earth_color.png"))
    normal_map(h, 1.5).save(os.path.join(out, "earth_normal.png"))


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    slabs(out)
    earth(out)

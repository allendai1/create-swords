# style_sky.py: the painted skybox for the Genshin-style rollout (2026-10-22). Allen: "Roll the Genshin style out across
# the village: ... a painted sky ...".
# A soft blue gradient (pale at the horizon, deep at the zenith) with puffy cumulus: clusters of soft round puffs with
# flat bottoms, sunlit cream tops, lavender-blue undersides, a lightly posterized light for brush bands. Painted per
# direction, so the six faces meet without seams. Face directions, measured in Studio with a labelled test sky:
# Bk +Z, Rt -X, Ft -Z, Lf +X, each upright with its right side = forward x up; Up: image top +X, image right -Z.
# Dn is below the ground, one horizon colour. Run: python -I style_sky.py <out dir>  ->  sky_<Face>.png (1024 px).
import os, sys
import numpy as np
from PIL import Image

N = 1024
rng = np.random.default_rng(41)
FACES = {  # forward, right, up (image axes)
    "Bk": ((0, 0, 1), (-1, 0, 0), (0, 1, 0)),
    "Rt": ((-1, 0, 0), (0, 0, -1), (0, 1, 0)),
    "Ft": ((0, 0, -1), (1, 0, 0), (0, 1, 0)),
    "Lf": ((1, 0, 0), (0, 0, 1), (0, 1, 0)),
    "Up": ((0, 1, 0), (0, 0, -1), (1, 0, 0)),
}


def smooth(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def unit(az, el):
    return np.array([np.cos(el) * np.cos(az), np.sin(el), np.cos(el) * np.sin(az)])


# clouds: a base elevation, a top and puffs (azimuth, elevation, angular radius); low cumulus round the horizon and a
# few broad, flatter clouds higher up
CLOUDS = []
def cloud(az, base, size, n, tall, opacity):
    puffs = []
    for k in range(n):
        dx = rng.uniform(-1.7, 1.7) * size  # along the horizon
        dy = abs(rng.normal(0.5, 0.3)) * size * tall * (1.2 - abs(dx) / (2.2 * size))  # taller in the middle
        rad = size * rng.uniform(0.5, 0.85)
        puffs.append((az + dx / np.cos(base), base + dy + rad * 0.3, rad))
    CLOUDS.append((base, max(p[1] + p[2] for p in puffs), puffs, opacity))
for i in range(22):
    base = np.radians(rng.uniform(1.0, 12))
    cloud(i / 22 * 2 * np.pi + rng.uniform(-0.1, 0.1), base, np.radians(rng.uniform(5, 10)), int(rng.integers(7, 12)), 1.0, 1.0)
for i in range(9):
    cloud(rng.uniform(0, 2 * np.pi), np.radians(rng.uniform(20, 42)), np.radians(rng.uniform(6, 11)), int(rng.integers(6, 10)), 0.45, 0.8)


def face(fwd, right, up):
    a = (np.arange(N) + 0.5) / N * 2 - 1
    A, B = np.meshgrid(a, a)  # A: left -> right, B: top -> bottom
    d = np.array(fwd)[None, None] + A[..., None] * np.array(right) - B[..., None] * np.array(up)
    d /= np.linalg.norm(d, axis=-1, keepdims=True)
    el = np.arcsin(np.clip(d[..., 1], -1, 1))
    az = np.arctan2(d[..., 2], d[..., 0])
    # sky gradient
    t = np.clip(el / np.radians(70), 0, 1) ** 0.6
    stops = [(0.0, (214, 232, 238)), (0.25, (160, 208, 236)), (0.6, (96, 166, 226)), (1.0, (62, 132, 214))]
    sky = np.stack([np.interp(t, [s[0] for s in stops], [s[1][c] for s in stops]) for c in range(3)], -1)
    # clouds
    alpha = np.zeros((N, N))
    light = np.zeros((N, N))
    for base, top, puffs, opacity in CLOUDS:
        for paz, pel, rad in puffs:
            c = unit(paz, pel)
            ang = np.arccos(np.clip(d @ c, -1, 1))
            m = smooth(rad, rad * 0.72, ang) * smooth(base - np.radians(0.4), base + np.radians(1.2), el) * opacity
            if not m.any():
                continue
            # light from above across the whole cloud, plus a little per puff
            l = 0.3 + 0.6 * np.clip((el - base) / (top - base), 0, 1) + 0.15 * np.clip((el - pel) / rad, -1, 1)
            light = np.where(m > alpha, np.clip(l, 0, 1), light)
            alpha = np.maximum(alpha, m)
    light = light * 0.65 + np.round(light * 4) / 4 * 0.35  # brush bands
    shade = np.array((172, 182, 222))
    lit = np.array((255, 252, 244))
    cloud = shade + (lit - shade) * light[..., None]
    col = sky * (1 - alpha[..., None]) + cloud * alpha[..., None]
    return Image.fromarray(col.clip(0, 255).astype(np.uint8))


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for name, axes in FACES.items():
        face(*axes).save(os.path.join(out, f"sky_{name}.png"))
        print(name)
    Image.new("RGB", (64, 64), (214, 232, 238)).save(os.path.join(out, "sky_Dn.png"))

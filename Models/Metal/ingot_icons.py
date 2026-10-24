# ingot_icons.py: the collection book's ingot images (2026-10-23). Allen: "we can just use the ingot and display the
# material on it. Would it also be possible to use an image of the ingot, somehow instead?"
# Input: Studio screen captures of the real ingot (SwordParts.Ingot dressed by Materials.dressIngot, yawed -25 degrees,
# camera 3 studs off at the item cards' angle) in front of a flat chroma wall: pure green, or magenta for green metals.
# Every capture uses the same camera, so one fixed crop frames them all alike. The wall is keyed out (its colour is
# read from the bottom-right corner, away from the sun glare and the HUD), the key colour's spill is pulled from the
# edges, and the result is shrunk premultiplied (no coloured halo) to a 256 px square PNG with alpha.
# Run: python -I ingot_icons.py <out dir> <manifest.json>   (manifest: {"Iron": "capture.jpg", "Rainbow Alloy": [green, magenta]})
import json, os, sys
import numpy as np
from PIL import Image

HALF, Y0, Y1 = 240, 177, 657  # a 480 px square around the capture's centre column (753 px tall): the ingot plus a margin
SIZE = 256
LO, HI = 30, 120  # key strength (0-255) from fully kept to fully cut


def shot(path):  # the crop, its key strength per pixel and whether the wall is magenta
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.float32)
    corner = a[-40:, -40:].reshape(-1, 3).mean(0)
    magenta = corner[0] > corner[1]  # green wall: g wins; magenta wall: r (and b) win
    cx = a.shape[1] // 2  # the Studio window's width varies; the ingot is always in the middle
    c = a[Y0:Y1, cx - HALF:cx + HALF]
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    return c, (np.minimum(r, b) - g) if magenta else (g - np.maximum(r, b)), magenta


def icon(path):  # path: a capture, or [green, magenta] captures of a metal with both key colours in it (Rainbow Alloy,
    # 2026-10-23): each pixel then comes from the photo whose wall it looks least like
    shots = [shot(p) for p in (path if isinstance(path, list) else [path])]
    c, key, magenta = shots[0]
    magenta = np.full(key.shape, magenta)
    for c2, key2, m2 in shots[1:]:
        take = key2 < key
        c, key, magenta = np.where(take[..., None], c2, c), np.where(take, key2, key), np.where(take, m2, magenta)
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    alpha = np.clip(1 - (key - LO) / (HI - LO), 0, 1)
    spill = np.clip(key, 0, None)  # pull the wall's colour out of what's kept
    r, g, b = np.where(magenta, r - spill, r), np.where(magenta, g, g - spill), np.where(magenta, b - spill, b)
    rgb = np.stack([r, g, b], -1) / 255
    pre = Image.fromarray((np.dstack([rgb * alpha[..., None], alpha]) * 255).clip(0, 255).astype(np.uint8), "RGBA")
    pre = pre.resize((SIZE, SIZE), Image.LANCZOS)
    p = np.asarray(pre).astype(np.float32) / 255
    al = p[..., 3:4]
    out = np.where(al > 0, p[..., :3] / np.maximum(al, 1e-6), 0)
    return Image.fromarray((np.dstack([out, al]) * 255).clip(0, 255).astype(np.uint8), "RGBA")


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for name, path in json.load(open(sys.argv[2])).items():
        icon(path).save(os.path.join(out, name.replace(" ", "_") + ".png"))
        print(name, "ok")

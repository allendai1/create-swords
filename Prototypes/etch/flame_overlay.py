"""Curled Flame vs the reference, layered (2026-11-10, Allen: "layer over the reference and analyze if it matches and
keep doing it until it does").

The reference is rotated flat (tip right, edge down); its blade face runs from the spine line to the edge line, about
380 px wide and nearly constant over the straight part. Its red is masked and resampled into face coordinates:
x in blade widths, w from the edge (0) to the spine (1). Our Flame is drawn from curled_flame_preview.flame_polys on a
straight blade of the same width, shifted along to the best fit, and laid over it.

Measured, both ways:
  coverage(w)   share of the face that is red at each height (the band, then the tongues thinning out)
  tongues/width red runs crossing the line w = 0.40, per blade width
  curl share    columns where the red is cut more than once (a pocket under a head, a hook)
  IoU           of the two masks in the tongue zone (w 0.30-0.75) at the best shift

Run:  python flame_overlay.py  -> flame_overlay.png next to this file, numbers printed
"""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import curled_flame_preview as cf

HERE = os.path.dirname(os.path.abspath(__file__))
PX = 380                 # the reference face's width in its rotated image, px
X0, X1 = 250, 1850       # its straight stretch, before the kissaki
NW = 100                 # rows across the face in the resampled grids


def reference():
    im = Image.open(cf.REF).convert("RGB").rotate(-43, resample=Image.BICUBIC, expand=True)
    a = np.asarray(im).astype(int)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    red = (R > 70) & (R > 2.0 * G) & (R > 2.0 * B)
    bright = a.mean(axis=2)
    cols = range(X0, X1)
    edge, spine = [], []
    for x in cols:
        ys = np.nonzero(red[1350:1700, x])[0]
        edge.append(1350 + ys.max())
        sp = np.nonzero(bright[1150:1450, x] > 70)[0]
        spine.append(1150 + sp[0])
    edge = np.convolve(np.array(edge, float), np.ones(41) / 41, mode="same")
    spine = np.convolve(np.array(spine, float), np.ones(41) / 41, mode="same")
    edge[:20], edge[-20:] = edge[20], edge[-21]
    spine[:20], spine[-20:] = spine[20], spine[-21]
    width = float(np.median(edge - spine))
    n = X1 - X0
    grid = np.zeros((NW, n), bool)
    for j, x in enumerate(cols):
        for k in range(NW):
            w = (k + 0.5) / NW
            y = int(round(edge[j] - w * (edge[j] - spine[j])))
            grid[k, j] = red[y, x]
    face = np.zeros((NW * 4, n, 3), np.uint8)  # the reference's face, straightened, for the picture
    for j, x in enumerate(cols):
        for k in range(NW * 4):
            w = (k + 0.5) / (NW * 4)
            face[NW * 4 - 1 - k, j] = a[int(round(edge[j] - w * (edge[j] - spine[j]))), x]
    return grid, width, face


def ours(length_w, px_per_w, shift):
    """Our Flame on a straight blade 1 unit wide, `length_w` widths of it starting `shift` widths in."""
    L = 40.0
    polys = cf.flame_polys(L, lambda x: 1.0, L - 1.0)
    W, H = int(length_w * px_per_w), NW
    SS = 4
    m = Image.new("L", (W * SS, H * SS), 0)
    d = ImageDraw.Draw(m)
    for poly in polys:
        d.polygon([((x - shift) * px_per_w * SS, (1 - y) * H * SS) for x, y in poly], fill=255)
    a = np.asarray(m.resize((W, H), Image.BOX), np.float32) / 255 > 0.5
    return a[::-1]  # row k = height w


def metrics(g, px_per_w):
    cov = g.mean(axis=1)
    k = int(0.40 * NW)
    row = g[k]
    runs = np.count_nonzero(np.diff(row.astype(int)) == 1)
    per_w = runs / (g.shape[1] / px_per_w)
    zone = g[int(0.2 * NW):int(0.85 * NW)]
    cuts = (np.diff(zone.astype(int), axis=0) == 1).sum(axis=0)  # red starting again above dark, per column
    curl = float((cuts >= 1).mean())
    return cov, per_w, curl


def iou(a, b):
    z = slice(int(0.30 * NW), int(0.75 * NW))
    a, b = a[z], b[z]
    return (a & b).sum() / max(1, (a | b).sum())


def main():
    ref, width, face = reference()
    n = ref.shape[1]
    ppw = width  # px per width in the reference grid
    best = (-1, 0)
    for s in np.arange(2.0, 10.0, 0.02):
        o = ours(n / ppw, ppw, s)[:, :n]
        v = iou(ref, o)
        if v > best[0]:
            best = (v, s)
    o = ours(n / ppw, ppw, best[1])[:, :n]
    rc, rpw, rcurl = metrics(ref, ppw)
    oc, opw, ocurl = metrics(o, ppw)
    bands = [(0.05, 0.25), (0.25, 0.35), (0.35, 0.45), (0.45, 0.55), (0.55, 0.65), (0.65, 0.75)]
    print(f"reference width {width:.0f} px, stretch {n / ppw:.2f} widths")
    print(f"IoU (tongue zone, best shift {best[1]:.2f} w): {best[0]:.3f}")
    print(f"tongues per width at w=0.40: ref {rpw:.2f}  ours {opw:.2f}")
    print(f"curl share (columns cut twice):  ref {rcurl:.2f}  ours {ocurl:.2f}")
    err = 0
    for a, b in bands:
        s = slice(int(a * NW), int(b * NW))
        r, q = rc[s].mean(), oc[s].mean()
        err += abs(r - q)
        print(f"  coverage w {a:.2f}-{b:.2f}: ref {r:.2f}  ours {q:.2f}")
    print(f"coverage error (sum over bands): {err:.3f}")

    # the picture: the straightened reference with our outline on it, then the masks (red = reference only,
    # blue = ours only, white = both), then the coverage curves
    H = face.shape[0]
    up = Image.fromarray(face)
    om = Image.fromarray((o[::-1] * 255).astype(np.uint8)).resize((n, H), Image.NEAREST)
    edges = np.asarray(om.filter(__import__("PIL.ImageFilter", fromlist=["FIND_EDGES"]).FIND_EDGES)) > 0
    over = np.asarray(up).copy()
    over[edges] = (0, 255, 255)
    rm = np.asarray(Image.fromarray((ref[::-1] * 255).astype(np.uint8)).resize((n, H), Image.NEAREST)) > 0
    omb = np.asarray(om) > 0
    cmp_ = np.zeros((H, n, 3), np.uint8) + 18
    cmp_[rm & ~omb] = (200, 30, 30)
    cmp_[~rm & omb] = (40, 110, 255)
    cmp_[rm & omb] = (235, 235, 235)
    ch, cw = 220, n
    chart = Image.new("RGB", (cw, ch), (250, 248, 244))
    cd = ImageDraw.Draw(chart)
    for curve, col in ((rc, (200, 30, 30)), (oc, (40, 110, 255))):
        pts = [((k + 0.5) / NW * cw, ch - 10 - curve[k] * (ch - 20)) for k in range(NW)]
        cd.line(pts, fill=col, width=3)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except OSError:
        font = ImageFont.load_default()
    cd.text((10, 8), "coverage by height (edge left, spine right): red = reference, blue = curled Flame", fill=(30, 30, 30), font=font)
    sheet = Image.new("RGB", (n + 40, 3 * H + ch + 150), (230, 226, 218))
    d = ImageDraw.Draw(sheet)
    y = 15
    d.text((20, y), "Reference, straightened (edge down), with the curled Flame's outline laid on it (cyan)", fill=(30, 30, 30), font=font)
    y += 28
    sheet.paste(Image.fromarray(over), (20, y))
    y += H + 12
    d.text((20, y), f"Masks: red = reference only, blue = ours only, white = both. IoU {best[0]:.2f}, tongues/width {rpw:.2f} vs {opw:.2f}, curls {rcurl:.2f} vs {ocurl:.2f}", fill=(30, 30, 30), font=font)
    y += 28
    sheet.paste(Image.fromarray(cmp_), (20, y))
    y += H + 12
    sheet.paste(chart, (20, y))
    out = os.path.join(HERE, "flame_overlay.png")
    sheet.save(out)
    print(out)


if __name__ == "__main__":
    main()

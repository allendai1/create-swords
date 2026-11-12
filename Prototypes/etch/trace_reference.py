"""Trace the curled Flame from the reference (Allen 2026-11-10: "What's so hard about copying the reference"): the red /
black outline of References/Etching Table/curled-flame-2026-11-10/curled-flame-reference.png, straightened along the
blade, as one polyline in blade widths (u along toward the point, v up from the cutting edge), smoothed of pixel noise
only. The game tiles it along each blade (Shared/EtchPatterns Flame); the data goes to flame_trace.json.

Run:  python trace_reference.py  -> flame_trace.json and trace_check.png next to this file
"""
import json, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
VAULT = os.path.normpath(os.path.join(HERE, "..", ".."))
REF = os.path.join(VAULT, "References", "Etching Table", "curled-flame-2026-11-10", "curled-flame-reference.png")
X0, X1 = 240, 1860       # the straight stretch in the rotated photo, before the point curves up
H = 400                  # rows across the face in the straightened image


def straighten():
    im = Image.open(REF).convert("RGB").rotate(-43, resample=Image.BICUBIC, expand=True)
    a = np.asarray(im).astype(int)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    red = (R > 70) & (R > 2.0 * G) & (R > 2.0 * B)
    bright = a.mean(axis=2)
    edge, spine = [], []
    for x in range(X0, X1):
        ys = np.nonzero(red[1350:1700, x])[0]
        edge.append(1350 + ys.max())
        sp = np.nonzero(bright[1150:1450, x] > 70)[0]
        spine.append(1150 + sp[0])
    k = 61
    pad = lambda v: np.concatenate([np.full(k // 2, v[0]), v, np.full(k // 2, v[-1])])
    edge = np.convolve(pad(np.array(edge, float)), np.ones(k) / k, mode="valid")
    spine = np.convolve(pad(np.array(spine, float)), np.ones(k) / k, mode="valid")
    n = X1 - X0
    mask = np.zeros((H, n), np.float32)
    rgb = np.zeros((H, n, 3), np.uint8)
    for j in range(n):
        for r in range(H):
            w = 1 - (r + 0.5) / H
            y = edge[j] - w * (edge[j] - spine[j])
            y0 = int(math.floor(y))
            f = y - y0
            mask[r, j] = red[y0, X0 + j] * (1 - f) + red[y0 + 1, X0 + j] * f
            rgb[r, j] = a[int(round(y)), X0 + j]
    width = float(np.median(edge - spine))
    return mask, rgb, width


def contour(mask):
    """Marching squares at 0.5 on the mask with the bottom row forced red; returns the longest polyline (x px, row)."""
    m = mask.copy()
    m[-3:, :] = 1.0
    h, w = m.shape
    segs = {}
    def interp(p1, p2, v1, v2):
        t = (0.5 - v1) / (v2 - v1)
        return (p1[0] + (p2[0] - p1[0]) * t, p1[1] + (p2[1] - p1[1]) * t)
    edges = []
    for r in range(h - 1):
        for c in range(w - 1):
            v = (m[r, c], m[r, c + 1], m[r + 1, c + 1], m[r + 1, c])
            idx = sum(1 << i for i, val in enumerate(v) if val >= 0.5)
            if idx in (0, 15):
                continue
            P = [(c, r), (c + 1, r), (c + 1, r + 1), (c, r + 1)]
            pts = []
            for e in range(4):
                a, b = e, (e + 1) % 4
                if (v[a] >= 0.5) != (v[b] >= 0.5):
                    pts.append(interp(P[a], P[b], v[a], v[b]))
            if len(pts) == 2:
                edges.append((pts[0], pts[1]))
            elif len(pts) == 4:
                edges.append((pts[0], pts[1]))
                edges.append((pts[2], pts[3]))
    # link segments into polylines by shared endpoints
    key = lambda p: (round(p[0], 4), round(p[1], 4))
    adj = {}
    for a, b in edges:
        adj.setdefault(key(a), []).append(key(b))
        adj.setdefault(key(b), []).append(key(a))
    seen = set()
    lines = []
    for start in adj:
        if start in seen:
            continue
        # walk from an end if there is one
        line = [start]
        seen.add(start)
        cur = start
        while True:
            nxt = [q for q in adj[cur] if q not in seen]
            if not nxt:
                break
            cur = nxt[0]
            seen.add(cur)
            line.append(cur)
        cur = start
        back = []
        while True:
            nxt = [q for q in adj[cur] if q not in seen]
            if not nxt:
                break
            cur = nxt[0]
            seen.add(cur)
            back.append(cur)
        lines.append(back[::-1] + line)
    lines.sort(key=lambda l: -len(l))
    return lines[0]


def simplify(pts, tol):
    """Ramer-Douglas-Peucker."""
    if len(pts) < 3:
        return pts
    a, b = np.array(pts[0]), np.array(pts[-1])
    ab = b - a
    L = np.hypot(*ab) or 1e-9
    d = [abs(np.cross(ab, np.array(p) - a)) / L for p in pts[1:-1]]
    i = int(np.argmax(d)) + 1
    if d[i - 1] > tol:
        return simplify(pts[:i + 1], tol)[:-1] + simplify(pts[i:], tol)
    return [pts[0], pts[-1]]


def main():
    mask, rgb, width = straighten()
    mask = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5)), np.float32) / 255
    line = contour(mask)
    if line[0][0] > line[-1][0]:
        line = line[::-1]
    # keep the band's top only: from where it leaves the left border to where it reaches the right border
    line = [p for p in line if 1 <= p[0] <= mask.shape[1] - 2]
    # smooth pixel noise along the curve (a short moving average), then thin it
    P = np.array(line, float)
    k = 7
    Ps = np.copy(P)
    for i in range(len(P)):
        lo, hi = max(0, i - k // 2), min(len(P), i + k // 2 + 1)
        Ps[i] = P[lo:hi].mean(axis=0)
    pts = simplify([tuple(p) for p in Ps], 0.6)
    uv = [(x / width, 1 - (r + 0.5) / H) for x, r in pts]
    out = {"width_px": width, "length": uv[-1][0] - uv[0][0], "points": [[round(u - uv[0][0], 4), round(v, 4)] for u, v in uv]}
    json.dump(out, open(os.path.join(HERE, "flame_trace.json"), "w"), indent=0)
    # a check picture: the straightened photo with the traced outline on it
    im = Image.fromarray(rgb).resize((rgb.shape[1], H))
    d = ImageDraw.Draw(im)
    d.line([(x, r) for x, r in pts], fill=(0, 255, 255), width=2)
    im.save(os.path.join(HERE, "trace_check.png"))
    print(f"{len(pts)} points, {out['length']:.2f} widths, width {width:.0f} px")


if __name__ == "__main__":
    main()

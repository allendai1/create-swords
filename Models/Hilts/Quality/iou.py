# python -I iou.py <render dir> <meta json> <prefix> [kinds...]
# Front-silhouette IoU of a Blender hilt render (with its review blade) against the matching sword of
# References/Sword Silhouettes/common-sword-silhouettes-v1.png (reference-modeling Phase 3 gate, hilt only).
# Both crops run from the landmark row (the first row, coming down the blade, whose width passes 1.8x the blade's:
# the guard's blade-side face, or the top of the rapier's rings) to the pommel's end. Holes are filled (filled masks),
# the render is scaled to the reference crop's height (hilt length), then the best fit over scale 0.90-1.10, a small
# turn (curved hilts), a mirror and a shift is kept. Writes <prefix>iou_<kind>.png (green both, red reference only,
# blue model only) and prints JSON.
import json
import sys
import cv2
import numpy as np

SHEET = r"C:\Users\Allen\Documents\Create Swords!\References\Sword Silhouettes\common-sword-silhouettes-v1.png"
# sheet sword -> component box (x0, y0, x1, y1) found by connected components (cv2), threshold 110
REF = {"Longsword": (713, 24, 825, 420), "Rapier": (1315, 31, 1402, 411), "Claymore": (987, 483, 1136, 935),
       "Flamberge": (1302, 497, 1427, 935), "Scimitar": (724, 530, 822, 933), "Cutlass": (149, 644, 210, 933)}
TURN = {"Scimitar": range(-14, 15, 2), "Cutlass": range(-14, 15, 2)}


def fill(m):
    m = m.astype(np.uint8)
    h, w = m.shape
    pad = np.zeros((h + 2, w + 2), np.uint8)
    pad[1:-1, 1:-1] = m
    ff = pad.copy()
    mask = np.zeros((h + 4, w + 4), np.uint8)
    cv2.floodFill(ff, mask, (0, 0), 2)
    return (ff[1:-1, 1:-1] != 2)


def landmark(m, start_frac=0.45):
    rows = np.nonzero(m.any(1))[0]
    ext = np.zeros(m.shape[0])
    for r in rows:
        c = np.nonzero(m[r])[0]
        ext[r] = c[-1] - c[0] + 1
    r0 = int(rows[0] + (rows[-1] - rows[0]) * start_frac)
    for r in range(r0, rows[-1]):
        blade = np.median(ext[max(rows[0], r - 25):r - 3]) if r - 3 > rows[0] else ext[r]
        if ext[r] > 1.8 * blade and ext[r] - blade > 4:
            return r, blade
    return r0, 0


def ref_mask(kind):
    im = cv2.imread(SHEET, cv2.IMREAD_GRAYSCALE)
    m = (im < 110).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    x0, y0, x1, y1 = REF[kind]
    best = max(range(1, n), key=lambda i: ((lab[y0:y1, x0:x1] == i).sum()))
    return lab == best


def crop(m, r0):
    rows = np.nonzero(m.any(1))[0]
    sub = m[r0:rows[-1] + 1]
    cols = np.nonzero(sub.any(0))[0]
    return sub[:, cols[0]:cols[-1] + 1]


def iou_fit(ref, mod, turns):
    H, W = ref.shape
    best = None
    for mirror in (False, True):
        m0 = mod[:, ::-1] if mirror else mod
        for s in np.arange(0.90, 1.101, 0.02):
            h = max(4, int(round(H * s)))
            w = max(2, int(round(m0.shape[1] * h / m0.shape[0])))
            ms = cv2.resize(m0.astype(np.uint8) * 255, (w, h), interpolation=cv2.INTER_AREA) > 127
            for t in turns:
                if t:
                    pad = int(max(h, w) * 0.3)
                    big = np.zeros((h + 2 * pad, w + 2 * pad), np.uint8)
                    big[pad:pad + h, pad:pad + w] = ms
                    M = cv2.getRotationMatrix2D((pad + w / 2, pad + h * 0.15), t, 1.0)
                    rot = cv2.warpAffine(big * 255, M, big.shape[::-1]) > 127
                    rr, cc = np.nonzero(rot)
                    mm = rot[rr.min():rr.max() + 1, cc.min():cc.max() + 1]
                else:
                    mm = ms
                mh, mw = mm.shape
                CW, CH = max(W, mw) + 40, max(H, mh) + 20
                R = np.zeros((CH, CW), bool)
                ry, rx = 10, (CW - W) // 2
                R[ry:ry + H, rx:rx + W] = ref
                for dy in range(-6, 7, 2):
                    for dx in range(-(CW - mw) // 2 + 2, (CW - mw) // 2 - 1, 1):
                        Mc = np.zeros_like(R)
                        y0 = ry + dy
                        x0 = (CW - mw) // 2 + dx
                        if y0 < 0 or x0 < 0 or y0 + mh > CH or x0 + mw > CW:
                            continue
                        Mc[y0:y0 + mh, x0:x0 + mw] = mm
                        i = (R & Mc).sum()
                        u = (R | Mc).sum()
                        v = i / u
                        if best is None or v > best[0]:
                            best = (v, mirror, round(float(s), 2), t, dx, dy, R, Mc)
    return best


def main():
    rdir, meta_path, prefix = sys.argv[1], sys.argv[2], sys.argv[3]
    kinds = sys.argv[4:] or list(REF)
    meta = json.load(open(meta_path))
    out = {}
    for k in kinds:
        if k not in REF or k not in meta:
            continue
        ref = fill(ref_mask(k))
        lr, bw = landmark(ref)
        rc = crop(ref, lr)
        img = cv2.imread(f"{rdir}\\{prefix}{k}.png", cv2.IMREAD_UNCHANGED)
        mod = fill(img[::-1, :, 3] > 127)          # blade up, like the sheet
        mt = meta[k]
        if mt.get("land_z") is not None:          # an explicit landmark (e.g. the flamberge's cross, under its lugs)
            H = mod.shape[0]
            lm = int(round(H - (mt["cz"] + mt["h"] / 2 - mt["land_z"]) * mt["ppu"]))
        else:
            lm, _ = landmark(mod)
        mc = crop(mod, lm)
        v, mirror, s, t, dx, dy, R, Mc = iou_fit(rc, mc, TURN.get(k, [0]))
        vis = np.full(R.shape + (3,), 255, np.uint8)
        vis[R & Mc] = (60, 170, 40)
        vis[R & ~Mc] = (40, 40, 220)
        vis[Mc & ~R] = (230, 80, 40)
        cv2.imwrite(f"{rdir}\\{prefix}iou_{k}.png", cv2.resize(vis, (vis.shape[1] * 4, vis.shape[0] * 4), interpolation=cv2.INTER_NEAREST))
        out[k] = dict(iou=round(float(v), 3), mirror=mirror, scale=s, turn=t, dx=dx, dy=dy, ref_rows=[int(lr), rc.shape],
                      ref_crop=list(rc.shape), model_crop=list(mc.shape))
    print(json.dumps(out))


if __name__ == "__main__":
    main()

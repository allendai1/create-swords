# Fictional swords (2026-10-29): straightens and colour-traces the Seraph and Thornspire of References/Swords/roblox unique swords.png.
# Paths below are the scratch folder it ran from; point D at this folder to rerun. Needs numpy and opencv.
# Traces the Seraph (left) and Thornspire (middle) swords of References/Swords/roblox unique swords.png:
# straightens each sword (fits its axis through the grip and blade centres), classifies colours, and writes
#   traced.json  - per sword: angle, axis column, rows, outline spans per row, part polygons (pixels), grip/pommel widths
#   rot_<name>.png - the straightened crop, for checks
import json, math
import cv2
import numpy as np

D = r"C:\Users\Allen\AppData\Local\Temp\claude\C--Users-Allen-Documents-Create-Swords-\e0c9e625-ab77-4c0b-b9ee-9975cad9bd0e\scratchpad\fic"
SRC = r"C:\Users\Allen\Documents\Create Swords!\References\Swords\roblox unique swords.png"
img = cv2.cvtColor(cv2.imread(SRC), cv2.COLOR_BGR2RGB).astype(np.int32)

SWORDS = {
    # cols, grip-row guess, rows used to fit the axis
    "seraph": dict(cols=(0, 205), grip=723, fit=[(100, 420), (660, 790)], pair=1e9),  # every part paired: average only
    "thornspire": dict(cols=(205, 415), grip=703.5, fit=[(130, 330), (620, 790)], pair=6),
}


def classes(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    bg = (r > g + 25) & (r > b + 20)
    bg[:12] = True
    mx = np.maximum(np.maximum(r, g), b)
    gem = (b > 170) & (r < 150) & ~bg
    gold = (np.minimum(r, g) - b > 22) & (r > 120) & ~bg
    dark = (mx < 105) & ~bg & ~gem
    light = ~bg & ~gem & ~gold & ~dark
    return dict(fg=~bg, gem=gem, gold=gold, dark=dark, light=light)


def spans(mask):
    out = {}
    for y in range(mask.shape[0]):
        xs = np.flatnonzero(mask[y])
        if len(xs) == 0:
            continue
        segs, s = [], xs[0]
        for a, b in zip(xs, xs[1:]):
            if b != a + 1:
                segs.append((int(s), int(a)))
                s = b
        segs.append((int(s), int(xs[-1])))
        out[y] = [q for q in segs if q[1] - q[0] >= 1]
    return out


def symmetric(mask, ax, pair=6):
    """The mask made symmetric about column ax (2026-10-29: the picture shows both swords a little turned, so the
    traced marks and wings were lopsided). By signed distance: where both sides have the shape (within `pair` pixels)
    the two meet halfway; a mark only one side shows (the other lost in a highlight) is mirrored."""
    m = mask.astype(np.uint8)
    sd = cv2.distanceTransform(1 - m, cv2.DIST_L2, 5) - cv2.distanceTransform(m, cv2.DIST_L2, 5)
    h, w = m.shape
    mapx = np.tile((2 * ax - np.arange(w)).astype(np.float32), (h, 1))
    mapy = np.tile(np.arange(h, dtype=np.float32)[:, None], (1, w))
    mir = cv2.remap(sd.astype(np.float32), mapx, mapy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return np.where(np.abs(sd - mir) < pair, (sd + mir) / 2, np.minimum(sd, mir)) < 0


def polys(mask, min_area=6, eps=1.0):
    m = mask.astype(np.uint8) * 255
    cs, hier = cv2.findContours(m, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    out = []
    for i, c in enumerate(cs):
        if cv2.contourArea(c) < min_area:
            continue
        hole = hier is not None and hier[0][i][3] >= 0
        a = cv2.approxPolyDP(c, eps, True)[:, 0, :].tolist()
        if len(a) >= 3:
            out.append(dict(hole=bool(hole), pts=a, area=float(cv2.contourArea(c))))
    return out


result = {}
for name, cfg in SWORDS.items():
    c0, c1 = cfg["cols"]
    crop = img[:, c0:c1].copy()
    cl = classes(crop)
    fg = cl["fg"]
    # axis: column centre of the foreground per row over the fit rows, a straight line through them
    ys, xs = [], []
    for a, b in cfg["fit"]:
        for y in range(a, b, 2):
            q = np.flatnonzero(fg[y])
            if len(q):
                ys.append(y)
                xs.append((q[0] + q[-1]) / 2)
    slope, icpt = np.polyfit(ys, xs, 1)
    angle = math.degrees(math.atan(slope))
    gy = cfg["grip"]
    gx = slope * gy + icpt
    # rotate about the grip centre so the axis is vertical
    M = cv2.getRotationMatrix2D((gx, gy), -angle, 1.0)
    rot = cv2.warpAffine(crop.astype(np.uint8), M, (crop.shape[1], crop.shape[0]), flags=cv2.INTER_LINEAR,
                         borderValue=(216, 168, 167))
    cv2.imwrite(f"{D}\\rot_{name}.png", cv2.cvtColor(rot, cv2.COLOR_RGB2BGR))
    cl = classes(rot.astype(np.int32))
    # the wings, arrowhead, cut-outs, marks and crescent are made symmetric about the straightened blade's own centre
    # column (the centre line and gem are left as traced)
    a, b = cfg["fit"][0]
    cb = float(np.mean([(q[0] + q[-1]) / 2 for q in (np.flatnonzero(cl["fg"][y]) for y in range(a, b, 2)) if len(q)]))
    sym = lambda m: symmetric(m, cb, cfg["pair"])
    res_cb = round(cb, 3)
    k = {n: cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8)).astype(bool) if n != "fg" else m
         for n, m in cl.items()}
    res = dict(angle=round(angle, 3), axis=round(float(gx), 2), cb=res_cb, grip_row=gy, col0=c0,
               outline={int(y): v for y, v in spans(cl["fg"]).items()})
    for n in ("gem", "gold", "dark", "light"):
        res[n] = polys(k[n])
    res["fg_polys"] = polys(cl["fg"], min_area=20, eps=0.5)
    rows = np.arange(rot.shape[0])[:, None]
    cols = np.arange(rot.shape[1])[None, :]
    fgm = cl["fg"]

    def extents(mask, y0, y1):
        out = {}
        for y in range(y0, y1):
            xs = np.flatnonzero(mask[y])
            if len(xs):
                out[y] = (int(xs[0]), int(xs[-1]))
        return out

    # the dark grip: the dark component reaching furthest down
    n_, lab, stats, _ = cv2.connectedComponentsWithStats(k["dark"].astype(np.uint8))
    grip_lab = max(range(1, n_), key=lambda i: stats[i, cv2.CC_STAT_TOP] + stats[i, cv2.CC_STAT_HEIGHT])
    grip = lab == grip_lab
    opn = lambda m: cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)).astype(bool)
    ero = lambda m: cv2.erode(m.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
    dil = lambda m: cv2.dilate(m.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
    if name == "seraph":
        band = np.abs(cols - gx) <= 24
        res["regions"] = dict(
            line=polys(cv2.morphologyEx((k["gold"] & (rows < 446)).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((45, 5), np.uint8)).astype(bool) & fgm),  # joined across the highlight that crosses it
            arrow=polys(sym(dil(k["gold"] & (rows >= 446) & (rows < 790)) & ero(ero(fgm))), min_area=10),
            cuts=polys(sym(opn(k["dark"] & ~grip & (rows >= 430) & (rows < 640)))),
            base=polys(sym(opn(fgm & (rows >= 548) & (rows < 790) & ~(grip | k["gem"]) & ~(band & (rows >= 646)))), min_area=10),
            gem=polys(k["gem"] & (rows > 590), min_area=10),
        )
        g = cv2.dilate(grip.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool) & fgm
        res["grip_w"] = extents(g, 590, 800)
        res["pommel_w"] = extents(fgm & (rows >= 790), 790, 860)
    else:
        band = np.abs(cols - gx) <= 16
        res["regions"] = dict(
            marks=polys(sym(dil(cl["dark"] & ~grip & (rows < 597)) & fgm & (rows < 597)), min_area=8, eps=1.3),
            slot=[q for q in polys(sym(fgm & (rows < 300)), min_area=3, eps=0.9) if q["hole"]],
            crescent=polys(sym(fgm & (rows >= 597) & (rows <= 662) & ~(band & (rows >= 609))), min_area=30),
        )
        res["grip_w"] = extents(fgm & (np.abs(cols - gx) <= 20), 606, 798)
        res["pommel_w"] = extents(fgm & (np.abs(cols - gx) <= 22), 790, 852)
        n2, lab2, st2, _ = cv2.connectedComponentsWithStats((k["gold"] & (rows > 600)).astype(np.uint8))
        res["bands"] = [(int(st2[i, cv2.CC_STAT_TOP]), int(st2[i, cv2.CC_STAT_TOP] + st2[i, cv2.CC_STAT_HEIGHT])) for i in range(1, n2)
                        if st2[i, cv2.CC_STAT_AREA] > 20]
    result[name] = res
    print(name, "angle", round(angle, 2), "axis", round(float(gx), 1), {n: [(q["hole"], round(q["area"])) for q in v] for n, v in res["regions"].items()}, res.get("bands"))
json.dump(result, open(f"{D}\\traced.json", "w"))

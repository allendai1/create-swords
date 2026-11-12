"""Turn parts/<id>.png into what build_blender.py needs (miniconda python: cv2).
Per sword and part: smooth sub-pixel outline loops (px) and the bevel line inside them; for the grip,
a half-thickness map (round in section, grooves where the bands' gaps were). Blade, guard and pommel
heights are worked out in Blender from the exact distance to the outline.
Saved as <out>/<id>.npz + <id>.json. Run: python prep.py <out_dir>

v2 (2026-11-10, Allen: "some of the models in blender have jagged edges", "some of them the blades
don't seem to be attached to the hilt"):
- outlines follow the sheet's anti-aliased grey, not the thresholded mask, and are smoothed along the
  curve, except at corners (turns over CORNER_DEG), so points and notches stay sharp;
- the sheet's white separator lines became gaps in 3D: the blade now runs SEAT_BLADE px down into the
  guard, the grip SEAT_GRIP px up into the guard and the pommel SEAT_POMMEL px up into the grip, never
  outside the sword's own (closed) silhouette."""
import cv2, numpy as np, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, '..', '..', '..', 'References', 'Sword Silhouettes')
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
UP = 2                      # grip map at 2x the sheet
SS = 4                      # outlines traced at 4x
P0 = dict(blade_t=2.2, blade_bevel=7.0, guard_t=3.8, guard_round=4.0, pommel_round=9.0, groove=0.78)
# per sword (2026-11-11): Inversion's guard is a block a little deeper than its grip, as its sheet's side view
PER = {'Inversion': dict(guard_t=16.0, guard_round=5.0)}
SEAT_BLADE, SEAT_GRIP, SEAT_POMMEL = 8, 5, 5
CORNER_DEG, SMOOTH_PX = 45.0, 0.9
meta = json.load(open(os.path.join(HERE, 'segment.json')))
cells = json.load(open(os.path.join(HERE, 'cells.json')))
sheets = {}


def smooth_loop(c):
    """Gaussian along a dense closed contour (4x px), held at corners; returns sheet px."""
    p = c[:, 0, :].astype(float)
    n = len(p)
    if n < 24:
        return p / SS
    k = 2 * SS                                   # 2 px either side to measure the turn
    a, b = p - np.roll(p, k, 0), np.roll(p, -k, 0) - p
    cosang = (a * b).sum(1) / (np.linalg.norm(a, axis=1) * np.linalg.norm(b, axis=1) + 1e-9)
    turn = np.degrees(np.arccos(np.clip(cosang, -1, 1)))
    corner = turn > CORNER_DEG
    sig = SMOOTH_PX * SS
    r = int(3 * sig)
    w = np.exp(-0.5 * (np.arange(-r, r + 1) / sig) ** 2); w /= w.sum()
    ext = np.concatenate([p[-r:], p, p[:r]])
    sm = np.stack([np.convolve(ext[:, j], w, 'valid') for j in range(2)], 1)
    # hold the outline near corners: weight 0 at a corner, 1 from 2 px away
    idx = np.nonzero(corner)[0]
    hold = np.ones(n)
    if len(idx):
        dist = np.min(np.abs(np.arange(n)[:, None] - idx[None, :]), 1)
        dist = np.minimum(dist, n - dist)
        hold = np.clip(dist / k, 0, 1)
    q = p * (1 - hold[:, None]) + sm * hold[:, None]
    return q / SS


def loops_of(field):
    """Smooth outline loops (outer and holes) of a 0..1 field at the sheet's scale."""
    f = cv2.resize(field.astype(np.float32), None, fx=SS, fy=SS, interpolation=cv2.INTER_CUBIC)
    f = cv2.GaussianBlur(f, (0, 0), 0.6 * SS)
    b = (f > 0.5).astype(np.uint8)
    cs, _ = cv2.findContours(b, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    out = []
    for c in cs:
        if cv2.contourArea(c) < 30 * SS * SS:    # under 30 px²: stray grey between parts
            continue
        q = smooth_loop(c)
        q = cv2.approxPolyDP((q * 64).astype(np.int32).reshape(-1, 1, 2), 0.15 * 64, True)[:, 0, :] / 64.0
        if len(q) >= 3:
            out.append(q.tolist())
    return out


def raster(loops, shape, scale):
    m = np.zeros((shape[0] * scale, shape[1] * scale), np.uint8)
    cv2.fillPoly(m, [(np.array(l) * scale * 16).astype(np.int32) for l in loops], 1, lineType=cv2.LINE_8, shift=4)
    return m


for sid, mt in meta.items():
    P = dict(P0, **PER.get(sid, {}))
    be, gt, gb = mt['cuts']
    lab = cv2.imread(os.path.join(HERE, 'parts', sid + '.png'), 0)
    groove = cv2.imread(os.path.join(HERE, 'parts', sid + '_groove.png'), 0) > 0
    cell = cells[sid]
    if cell['sheet'] not in sheets:
        sheets[cell['sheet']] = cv2.imread(os.path.join(REF, cell['sheet']), 0)
    g = sheets[cell['sheet']][cell['y0']:cell['y0'] + cell['h'], cell['x0']:cell['x0'] + cell['w']]
    dark = 1 - g.astype(np.float32) / 255.0
    H, W = lab.shape
    # every pixel goes to the part of its nearest labelled pixel, so edge pixels keep their grey
    _, near = cv2.distanceTransformWithLabels((lab == 0).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    zeros = np.argwhere(lab != 0)            # labelled pixels in scan order = the zero pixels of (lab == 0)
    owner = np.zeros(len(zeros) + 1, np.uint8)
    owner[1:] = lab[zeros[:, 0], zeros[:, 1]]
    nearlab = owner[near]
    allowed = cv2.morphologyEx((lab > 0).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8)) > 0

    def seat(mask, rows, dy, steps):
        """Copy the mask's pixels in `rows` `steps` px along dy (+1 down, -1 up), inside the silhouette."""
        add = np.zeros_like(mask)
        src = np.zeros_like(mask); src[rows] = mask[rows]
        for s in range(1, steps + 1):
            add |= np.roll(src, dy * s, 0)
        return add & allowed

    out, arrs = {'meta': mt, 'up': UP, 'P': P, 'parts': {}}, {}
    for k, name in [(1, 'Blade'), (2, 'Guard'), (3, 'Grip'), (4, 'Pommel')]:
        m = lab == k
        if m.sum() < 20:
            continue
        field = np.where(nearlab == k, dark, 0.0)
        extra = np.zeros_like(m)
        if name == 'Blade':
            extra = seat(m, slice(max(be - 4, 0), be), 1, SEAT_BLADE)
        elif name == 'Grip':
            extra = seat(m | groove, slice(gt, min(gt + 4, H)), -1, SEAT_GRIP)
            extra |= groove
        elif name == 'Pommel':
            extra = seat(m, slice(gb, min(gb + 4, H)), -1, SEAT_POMMEL)
        field = np.maximum(field, cv2.GaussianBlur(extra.astype(np.float32), (0, 0), 0.7))
        loops = loops_of(field)
        part = {'loops': loops}
        reach = {'Blade': P['blade_bevel'], 'Guard': P['guard_round']}.get(name)
        if reach:
            r = raster(loops, (H, W), SS)
            d = cv2.distanceTransform(r, cv2.DIST_L2, cv2.DIST_MASK_PRECISE) / SS
            part['inner'] = loops_of(cv2.resize((d >= reach).astype(np.float32), (W, H), interpolation=cv2.INTER_AREA)) if (d >= reach).any() else []
        if name == 'Grip':
            mu = raster(loops, (H, W), UP) > 0
            h = np.zeros(mu.shape, np.float32)
            for y in range(mu.shape[0]):
                xs = np.nonzero(mu[y])[0]
                if len(xs) == 0:
                    continue
                br = np.nonzero(np.diff(xs) > 1)[0]
                for seg in np.split(xs, br + 1):     # each run is a round section
                    c, rr = (seg[0] + seg[-1]) / 2, (seg[-1] - seg[0] + 1) / 2
                    h[y, seg] = np.sqrt(np.clip(rr * rr - (seg - c) ** 2, 0, None)) / UP
            gr = cv2.resize(groove.astype(np.uint8), (mu.shape[1], mu.shape[0]), interpolation=cv2.INTER_NEAREST) > 0
            h[gr] *= P['groove']
            h = cv2.GaussianBlur(h, (0, 0), 0.8)
            arrs['Grip'] = h.astype(np.float16)
        out['parts'][name] = part
    np.savez_compressed(os.path.join(OUT, sid + '.npz'), **arrs)
    json.dump(out, open(os.path.join(OUT, sid + '.json'), 'w'))
print('ok', len(meta), P0, PER)

"""Split each sword mask into blade / guard / grip / pommel (miniconda python: cv2).
cuts.json per sword: [blade_end, grip_top, grip_bot] in mask rows (picked by eye from ruler.png).
Blade = what joins the tip above blade_end; grip = the axis run in grip rows (band gaps closed);
other pixels in grip rows go to the guard (knuckle bows, swept rings); below grip_bot = pommel.
Writes parts/<id>.png (label image 0 bg, 1 blade, 2 guard, 3 grip, 4 pommel) and segment.png."""
import cv2, numpy as np, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
cuts = json.load(open(os.path.join(HERE, 'cuts.json')))
EXTRA = {'S02': {'blade_x': [55, 79]},  # rapier: the swept rings touch the blade
         'Inversion': {'wrap': 7}}       # 2026-11-11: its silhouette's grip is smooth; the sheet draws a wrap, a groove every 7 rows
os.makedirs(os.path.join(HERE, 'parts'), exist_ok=True)
COL = {1: (200, 200, 200), 2: (40, 170, 230), 3: (40, 70, 140), 4: (200, 120, 40)}
tiles, meta = [], {}

def runs(row):
    d = np.diff(np.concatenate([[0], row.astype(np.int8), [0]]))
    return list(zip(np.nonzero(d == 1)[0], np.nonzero(d == -1)[0] - 1))

for sid, (be, gt, gb) in cuts.items():
    m = cv2.imread(os.path.join(HERE, 'masks', sid + '.png'), 0) > 127
    H, W = m.shape
    lab = np.zeros((H, W), np.uint8)
    # blade: component of the tip in rows above blade_end
    top = m.copy(); top[be:] = False
    n, cc = cv2.connectedComponents(top.astype(np.uint8), connectivity=8)
    ty = np.nonzero(m.any(1))[0][0]; tx = np.nonzero(m[ty])[0][0]
    lab[cc == cc[ty, tx]] = 1
    bx = EXTRA.get(sid, {}).get('blade_x')
    if bx: lab[:, :bx[0]][lab[:, :bx[0]] == 1] = 2; lab[:, bx[1] + 1:][lab[:, bx[1] + 1:] == 1] = 2
    lab[:gt][m[:gt] & (lab[:gt] == 0)] = 2
    # grip axis: width-weighted median centre of narrow runs in grip rows
    cs, ws = [], []
    for y in range(gt, gb):
        for a, b in runs(m[y]):
            if b - a + 1 <= 40: cs.append((a + b) / 2); ws.append(b - a + 1)
    o = np.argsort(cs); cw = np.cumsum(np.array(ws)[o]); gc = np.array(cs)[o][np.searchsorted(cw, cw[-1] / 2)]
    half = []
    for y in range(gt, gb):
        best = None
        for a, b in runs(m[y]):
            if a - 2 <= gc <= b + 2 and b - a + 1 <= 50: best = (a, b)
        if best:
            lab[y, best[0]:best[1] + 1] = 3; half.append((best[1] - best[0] + 1) / 2)
    gr = m[gt:gb] & (lab[gt:gb] == 0); lab[gt:gb][gr] = 2
    # close band gaps inside the grip column (grooves remembered for the 3D rings)
    hw = int(round(np.median(half))) if half else 10
    grip = lab == 3
    closed = cv2.morphologyEx(grip.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((9, 1), np.uint8)) > 0
    col = np.zeros_like(m); col[gt:gb, int(gc - hw):int(gc + hw) + 1] = True
    groove = closed & ~grip & col
    wrap = EXTRA.get(sid, {}).get('wrap')
    if wrap:
        for y in range(gt + wrap, gb - 3, wrap):
            groove[y:y + 2] |= grip[y:y + 2]
    lab[groove] = 3
    lab[gb:][m[gb:]] = 4
    cv2.imwrite(os.path.join(HERE, 'parts', sid + '.png'), lab)
    cv2.imwrite(os.path.join(HERE, 'parts', sid + '_groove.png'), groove.astype(np.uint8) * 255)
    meta[sid] = {'axis': float(gc), 'grip_half': hw, 'cuts': [be, gt, gb], 'H': H, 'W': W}
    t = np.full((H, W, 3), 255, np.uint8)
    for k, c in COL.items(): t[lab == k] = c
    t[groove] = (0, 0, 255)
    for y in (be, gt, gb): cv2.line(t, (0, y), (W - 1, y), (0, 0, 255), 1)
    t = cv2.copyMakeBorder(t, 16, 470 - H, 3, 3, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    cv2.putText(t, sid, (2, 12), 0, 0.38, (0, 0, 0), 1); tiles.append(t)
json.dump(meta, open(os.path.join(HERE, 'segment.json'), 'w'), indent=1)
rows = [tiles[i:i + 8] for i in range(0, len(tiles), 8)]
wmax = max(sum(t.shape[1] for t in r) for r in rows)
cv2.imwrite(os.path.join(HERE, 'segment.png'), np.vstack([cv2.copyMakeBorder(np.hstack(r), 0, 0, 0, wmax - sum(t.shape[1] for t in r), cv2.BORDER_CONSTANT, value=(255, 255, 255)) for r in rows]))
print('ok', len(meta))

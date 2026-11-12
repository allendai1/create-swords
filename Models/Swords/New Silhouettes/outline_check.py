"""Draw prep.py's loops over each sword at 3x (miniconda python): outline_check.png. Run: python outline_check.py <prep out>"""
import cv2, numpy as np, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = sys.argv[1]; S = 3
cells = json.load(open(os.path.join(HERE, 'cells.json')))
COL = {'Blade': (90, 90, 90), 'Guard': (0, 140, 230), 'Grip': (30, 60, 140), 'Pommel': (200, 100, 0)}
tiles, small = [], []
for sid in json.load(open(os.path.join(HERE, 'segment.json'))):
    d = json.load(open(os.path.join(SRC, sid + '.json')))
    m = cv2.imread(os.path.join(HERE, 'masks', sid + '.png'), 0)
    t = cv2.resize(cv2.cvtColor(255 - m // 4, cv2.COLOR_GRAY2BGR), None, fx=S, fy=S, interpolation=cv2.INTER_NEAREST)
    for name, part in d['parts'].items():
        for l in part['loops']:
            a = np.array(l)
            area = abs(cv2.contourArea(a.astype(np.float32)))
            if area < 30: small.append((sid, name, round(area, 1), [round(v) for v in a.mean(0)]))
            cv2.polylines(t, [(a * S * 16).astype(np.int32)], True, COL[name], 1, cv2.LINE_AA, shift=4)
        for l in part.get('inner', []):
            cv2.polylines(t, [(np.array(l) * S * 16).astype(np.int32)], True, (0, 0, 255), 1, cv2.LINE_AA, shift=4)
    cv2.putText(t, sid, (4, 16), 0, 0.5, (0, 0, 0), 1)
    tiles.append(t)
h = max(t.shape[0] for t in tiles)
tiles = [cv2.copyMakeBorder(t, 0, h - t.shape[0], 2, 2, cv2.BORDER_CONSTANT, value=(255, 255, 255)) for t in tiles]
rows = [tiles[i:i + 8] for i in range(0, len(tiles), 8)]
wmax = max(sum(t.shape[1] for t in r) for r in rows)
cv2.imwrite(os.path.join(HERE, 'outline_check.png'), np.vstack([cv2.copyMakeBorder(np.hstack(r), 0, 0, 0, wmax - sum(t.shape[1] for t in r), cv2.BORDER_CONSTANT, value=(255, 255, 255)) for r in rows]))
print('small loops (<30 px²):'); [print(' ', s) for s in small]

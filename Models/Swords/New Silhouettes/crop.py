"""Cut the two new silhouette sheets into one mask per sword (miniconda python: cv2).
Writes masks/<id>.png (white sword on black, sheet pixels) and cells.json (crop origins)
plus a ruler sheet for picking the blade / grip cuts by eye."""
import cv2, numpy as np, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, '..', '..', '..', 'References', 'Sword Silhouettes')
SHEETS = {
    'a': ('new-silhouettes-a-v1.png', 6, [(0, 455), (500, 968)],
          ['S01','S02','S03','S04','S05','S06','S07','S08','S09','S10','S11','S12']),
    'b': ('new-silhouettes-b-v1.png', 5, [(0, 468), (505, 972)],
          ['EclipseFang','Tidebreaker','Crownsplitter','Mothwing','Lockjaw',
           'Cometspine','Gravebell','OrchidEdge','IronAnchor','Riftkey']),
    # Inversion (2026-11-11): the front silhouette of References/Swords/inversion-reference-sheet.png, 450 px tall (make it
    # again: that sheet's core-silhouette panel, ink at its median made black, scaled 450/509, 10 px white margin)
    'c': ('inversion-v1.png', 1, [(0, 491)], ['Inversion']),
}
os.makedirs(os.path.join(HERE, 'masks'), exist_ok=True)
cells, tiles = {}, []
for key, (fn, cols, rows, ids) in SHEETS.items():
    g = cv2.cvtColor(cv2.imread(os.path.join(REF, fn)), cv2.COLOR_BGR2GRAY)
    m = (g < 128).astype(np.uint8) * 255
    H, W = m.shape; cw = W // cols
    for r, (y0, y1) in enumerate(rows):
        for c in range(cols):
            sid = ids[r * cols + c]
            cell = m[y0:y1, c * cw:(c + 1) * cw]
            ys, xs = np.nonzero(cell)
            bx0, bx1, by0, by1 = max(0, xs.min() - 6), xs.max() + 7, max(0, ys.min() - 6), ys.max() + 7
            crop = cell[by0:by1, bx0:bx1]
            cv2.imwrite(os.path.join(HERE, 'masks', sid + '.png'), crop)
            cells[sid] = {'sheet': fn, 'x0': int(c * cw + bx0), 'y0': int(y0 + by0),
                          'w': int(crop.shape[1]), 'h': int(crop.shape[0])}
            t = cv2.cvtColor(255 - crop, cv2.COLOR_GRAY2BGR)
            for y in range(0, crop.shape[0], 20):
                cv2.line(t, (0, y), (8 if y % 100 else 20, y), (0, 0, 255), 1)
                if y % 100 == 0: cv2.putText(t, str(y), (0, y + 12), 0, 0.35, (0, 0, 255), 1)
            t = cv2.copyMakeBorder(t, 18, 0, 0, 0, cv2.BORDER_CONSTANT, value=(255, 255, 255))
            cv2.putText(t, sid, (2, 13), 0, 0.4, (200, 0, 0), 1)
            tiles.append(t)
json.dump(cells, open(os.path.join(HERE, 'cells.json'), 'w'), indent=1)
h = max(t.shape[0] for t in tiles)
tiles = [cv2.copyMakeBorder(t, 0, h - t.shape[0], 4, 4, cv2.BORDER_CONSTANT, value=(255, 255, 255)) for t in tiles]

rows_ = [tiles[i:i + 6] for i in range(0, len(tiles), 6)]
wmax = max(sum(t.shape[1] for t in rr) for rr in rows_)
sheet = np.vstack([cv2.copyMakeBorder(np.hstack(rr), 0, 0, 0, wmax - sum(t.shape[1] for t in rr), cv2.BORDER_CONSTANT, value=(255, 255, 255)) for rr in rows_])
cv2.imwrite(os.path.join(HERE, 'ruler.png'), sheet)
print(len(cells), sheet.shape)

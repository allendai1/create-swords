# python -I iou.py : silhouette IoU of the Blender front renders (hilt + blade) against the reference masks
import json
import numpy as np
from PIL import Image

D = r"C:\Users\Allen\AppData\Local\Temp\claude\C--Users-Allen-Documents-Create-Swords-\e0c9e625-ab77-4c0b-b9ee-9975cad9bd0e\scratchpad\fic"
ref = np.asarray(Image.open(r"C:\Users\Allen\Documents\Create Swords!\References\Swords\roblox unique swords.png").convert("RGB")).astype(int)
r, g, b = ref[..., 0], ref[..., 1], ref[..., 2]
fg = ~((r > g + 25) & (r > b + 20))
fg[:12, :] = False                       # the dark band along the picture's top edge
T = json.load(open(D + "\\traced.json"))
CASES = {
    # name: render, ppu, top, grip row, grip col, ref column range, blade-root row (straightened crops, trace_ref.py)
    "seraph": ("sil_se.png", 1 / 0.007335, 1.3, 723, T["seraph"]["axis"], None, 540),
    "thornspire": ("sil_ts.png", 560 * 20 / 80.0, 1.3, 703, T["thornspire"]["axis"], None, 600),
}
out = {}
for name, (f, ppu, top, gr, gc, _, root) in CASES.items():
    rr = np.asarray(Image.open(f"{D}\\rot_{name}.png").convert("RGB")).astype(int)
    fg = ~((rr[..., 0] > rr[..., 1] + 25) & (rr[..., 0] > rr[..., 2] + 20))
    fg[:12, :] = False
    mask = fg.copy()
    if name == "seraph":   # the specular bloom beside the blade (rows 290-372) is lighting, not sword
        cb = sum((T["seraph"]["outline"][str(r)][0][0] + T["seraph"]["outline"][str(r)][-1][1]) / 2 for r in range(100, 221, 2)) / 61
        mask[290:373, int(cb + 19):] = False
    c0, c1 = 0, fg.shape[1]
    sil = np.asarray(Image.open(f"{D}\\{f}").convert("L")) < 128
    sil = sil[::-1]                          # blade up, like the reference
    H, W = sil.shape
    srow = H - top * ppu                     # grip centre row in the flipped render
    scol = W / 2
    best = None
    for mirror in (False, True):
        s = sil[:, ::-1] if mirror else sil
        for dy in range(-12, 13):
            for dx in range(-8, 9):
                canvas = np.zeros_like(fg)
                y0 = int(round(gr - srow)) + dy
                x0 = int(round(gc - scol)) + dx
                ys, xs = slice(max(0, y0), min(fg.shape[0], y0 + H)), slice(max(0, x0), min(fg.shape[1], x0 + W))
                canvas[ys, xs] = s[ys.start - y0:ys.stop - y0, xs.start - x0:xs.stop - x0]
                inter = (canvas & mask).sum()
                union = (canvas | mask).sum()
                iou = inter / union
                if not best or iou > best[0]:
                    best = (iou, mirror, dx, dy, canvas)
    iou, mirror, dx, dy, canvas = best
    rows = np.arange(fg.shape[0])[:, None]
    blade, hilt = rows < root + dy * 0, rows >= root
    part = lambda m: float((canvas & mask & m).sum() / max(1, ((canvas | mask) & m).sum()))
    out[name] = dict(iou=round(float(iou), 4), blade=round(part(blade), 4), hilt=round(part(hilt), 4), mirror=mirror, dx=dx, dy=dy)
    # diff overlay: green = both, red = reference only, blue = model only
    img = np.full(fg.shape + (3,), 255, np.uint8)
    img[canvas & mask] = (40, 170, 60)
    img[mask & ~canvas] = (220, 40, 40)
    img[canvas & ~mask] = (40, 80, 230)
    Image.fromarray(img[:, c0:c1]).resize(((c1 - c0) * 2, fg.shape[0] * 2), Image.NEAREST).save(f"{D}\\iou_{name}.png")
print(json.dumps(out))

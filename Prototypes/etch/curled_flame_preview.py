"""Curled Flame etch (Create Swords!, 2026-11-10): flat preview beside the reference
(References/Etching Table/curled-flame-2026-11-10/curled-flame-reference.png, rotated so the blade lies flat).

The flames are the dark shapes (Allen: "the black is actually the flame"): pointed tongues hanging from the dark steel
toward the cutting edge, each curling to a sharp tip, with round heads of the band colour between them. The band's top
is one boundary curve along the blade, built flame by flame from cubic Beziers in local blade widths and sampled into
points; the colour is everything below it. It is cut at every head's crown into pieces the canvas fills (concave, but
each column crosses a piece's outline cleanly). Coordinates: centimetres on the face, x along the blade, y across
from the cutting-edge line. Shared/EtchPatterns builds the same shape in the game.

Run:  python curled_flame_preview.py  -> curled_flame_preview.png next to this file
"""
import json, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
VAULT = os.path.normpath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(VAULT, "Prototypes", "tanto-forge", "dist", "data")
REF = os.path.join(VAULT, "References", "Etching Table", "curled-flame-2026-11-10", "curled-flame-reference.png")
BG = (24, 24, 28)
MOTIF_CM = 7.0          # EtchCanvas.MOTIF_CM: sizes come from the width up to this
from flame_shape import BAND, FOOT, boundary  # the shape itself (shared with the overlay and the game port)


def flame_polys(length, widthAt, limit):
    """Polygons (cm, x along / y from the edge line): the region under the boundary, cut at every head's crown."""
    cap = lambda x: min(widthAt(x), MOTIF_CM)
    pts, cuts = boundary(length, cap, limit)
    cuts = [0] + cuts + [len(pts) - 1]
    polys = []
    for a, b in zip(cuts, cuts[1:]):
        run = [(x, v * cap(min(max(x, 0), length))) for x, v in pts[a:b + 1]]
        x0, x1 = run[0][0], run[-1][0]
        polys.append(run + [(x1, FOOT * cap(min(max(x1, 0), length))), (x0, FOOT * cap(min(max(x0, 0), length)))])
    return polys


# --- drawing -----------------------------------------------------------------------------------------------------
def blade(name):
    d = json.load(open(os.path.join(DATA, name + ".json"), encoding="utf-8"))
    st = d["stages"]["refined"]
    L = st["length"]

    def curve(pts):
        pts = sorted(pts)
        return lambda u: np.interp(u, [p[0] for p in pts], [p[1] for p in pts])

    return L, curve(st["spine"]), curve(st["edge"]), curve(st["ridge"])


def limit_of(L, widthAt):
    lim = L - 1.1 * widthAt(L * 0.95)
    x, start, gap = lim - 0.25, None, 0
    while x > 0.4 * L:
        if widthAt(x) - widthAt(x + 0.25) > 0.25 * 0.25:
            start, gap = x, 0
        else:
            gap += 0.25
            if gap > 0.5 * widthAt(x):
                break
        x -= 0.25
    return start or lim


def draw(name, ppc, style, flip=False):
    """Flat blade, hilt left, edge at the bottom. style 'ref': red band on dark steel; 'game': the canvas's look on
    a see-through body (mark = accent lifted toward white, dark ink halo) over plain steel."""
    L, spine, edge, ridge = blade(name)
    widthAt = lambda x: float(spine(x / L) - edge(x / L))
    polys = flame_polys(L, widthAt, limit_of(L, widthAt))
    half = max(float(spine(0)), -float(edge(0))) + 0.3
    SS = 3
    W, H = int(L * ppc) + 4, int(2 * half * ppc) + 4
    mask = Image.new("L", (W * SS, H * SS), 0)
    dr = ImageDraw.Draw(mask)
    for poly in polys:  # y from the edge line -> blade cm -> pixels (edge at the bottom)
        pts = [(x * ppc * SS, (half - float(edge(min(max(x, 0), L) / L)) - y) * ppc * SS) for x, y in poly]
        dr.polygon(pts, fill=255)
    mask = mask.resize((W, H), Image.LANCZOS)
    cov = np.asarray(mask, np.float32) / 255
    X, Y = np.meshgrid((np.arange(W) + 0.5) / ppc, half - (np.arange(H) + 0.5) / ppc)
    u = np.clip(X / L, 0, 1)
    sp, ed = spine(u), edge(u)
    inside = (Y <= sp) & (Y >= ed) & (X <= L)
    w = (Y - ed) / np.maximum(sp - ed, 1e-6)
    pxw = np.maximum(sp - ed, 1e-6) * ppc
    on = np.clip(np.minimum(w - 0.032, 0.968 - w) * pxw + 0.5, 0, 1)  # the overlay's edge and spine strips stay bare
    wr = 1 - ridge(u)
    lit = (np.where(w < wr, 1 - w / wr, 0.0) ** 1.4) * np.clip(1 - u / 0.5, 0.25, 1)
    if style == "ref":
        dark = np.array([6, 12, 20]) + (np.array([30, 56, 84]) - np.array([6, 12, 20])) * lit[..., None]
        red = np.array([108, 9, 8]) + (np.array([165, 14, 10]) - np.array([108, 9, 8])) * np.clip(lit * 1.4, 0, 1)[..., None]
        k = (cov * on)[..., None]
        face = dark * (1 - k) + red * k
        line = np.clip(1 - on, 0, 1)[..., None]
        face = face * (1 - line) + np.array([205, 222, 240]) * line
    else:
        steel = np.array([150, 156, 168]) + 60 * lit[..., None]
        glow_r = 0.07 * min(widthAt(L * 0.3), MOTIF_CM) * ppc
        g = np.asarray(Image.fromarray((cov * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(glow_r / 2)), np.float32) / 255
        g = np.clip(g * 2.2, 0, 1)
        accent = np.array([165, 14, 10])
        mark = accent + (255 - accent) * 0.55
        ink = np.array([14, 10, 10])
        a = np.maximum(cov, g * 0.95)[..., None] * on[..., None]
        col = ink * (1 - cov[..., None]) + mark * cov[..., None]
        face = steel * (1 - a) + col * a
    img = np.where(inside[..., None], face, np.array(BG, np.float32))
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    return im, L, len(polys)


def main():
    try:
        font = ImageFont.truetype("arial.ttf", 22)
        small = ImageFont.truetype("arial.ttf", 18)
    except OSError:
        font = small = ImageFont.load_default()
    ref = Image.open(REF).convert("RGB").rotate(-43, resample=Image.BICUBIC, expand=True)
    ref = ref.crop((0, 1230, 2500, 1700))
    ref = ref.resize((ref.width * 2 // 5, ref.height * 2 // 5), Image.LANCZOS)
    kat, _, _ = draw("katana", 60, "ref")
    sec = kat.crop((kat.width - 780, 0, kat.width, kat.height))  # the last 13 cm: the 5.5 blade widths the reference shows
    sec = sec.resize((sec.width * ref.height // sec.height, ref.height), Image.LANCZOS)
    rows = []
    for n in ("katana", "wakizashi", "tanto", "longsword"):
        for style in ("ref", "game"):
            im, L, n_polys = draw(n, 16, style)
            rows.append((im, f"{n}: {L:.0f} cm, {'red on dark (reference colours)' if style == 'ref' else 'in-game: accent on see-through body, ink halo, over steel'}"))
    pad = 30
    width = max(ref.width + sec.width + 3 * pad, max(r[0].width for r in rows) + 2 * pad)
    height = pad + 30 + max(ref.height, sec.height) + 40 + sum(r[0].height + 50 for r in rows) + pad
    sheet = Image.new("RGB", (width, height), (230, 226, 218))
    d = ImageDraw.Draw(sheet)
    d.text((pad, pad), "Reference (rotated flat, tip right)", fill=(30, 30, 30), font=font)
    d.text((2 * pad + ref.width, pad), "Curled Flame: katana's last 13 cm (same 5.5 widths), flat", fill=(30, 30, 30), font=font)
    y = pad + 30
    sheet.paste(ref, (pad, y))
    sheet.paste(sec, (2 * pad + ref.width, y))
    y += max(ref.height, sec.height) + 40
    for im, label in rows:
        d.text((pad, y), label, fill=(30, 30, 30), font=small)
        y += 26
        sheet.paste(im, (pad, y))
        y += im.height + 24
    out = os.path.join(HERE, "curled_flame_preview.png")
    sheet.save(out)
    print(out, sheet.size)


def check():
    polys = flame_polys(70, lambda x: 3.2 - 1.2 * x / 70, 62)
    assert len(polys) > 20, len(polys)
    pts, cuts = boundary(70, lambda x: 3.0, 62)
    xs = [pts[c][0] for c in cuts]
    assert xs == sorted(xs), 'cut points out of order'
    for c in cuts:                                  # a cut is a dark tip: the colour below it reaches the band
        assert 0.10 < pts[c][1] < 0.26, pts[c]


if __name__ == "__main__":
    check()
    main()

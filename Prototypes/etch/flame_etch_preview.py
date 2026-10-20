"""Flat preview of the Flame etch v4 (Create Swords!), matched to Allen's reference screenshot
(References/Etching Table/flame-band-reference.webp): a red band along the cutting edge whose boundary with
the dark blade is a shallow, uneven run of rounded humps with an occasional small point.

Measured from the reference (measure_reference.py):
  red band   ~28% of the width from the edge line (19-38% across the humps)
  humps      one per 0.75-1.05 local blade widths (the reference reads 0.6-1.0 in perspective), amplitude 10-17% of the width
  shape      red dips broad and rounded, deepest red at 45% of a period
  colours    red 165,14,10 -> 110,9,8; dark 14,34,54 (lit bevel) -> 6,12,20; edge lines ~205,222,240

Drawn on the true blade outlines from Prototypes/tanto-forge/dist/data/*.json. The pattern is a function of
position along the blade (in local widths), so it ports directly to Luau (Shared/BladeEtch).
Run:  python flame_etch_preview.py   -> flame_etch_v4_preview.png next to this file
"""
import json, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
VAULT = os.path.normpath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(VAULT, "Prototypes", "tanto-forge", "dist", "data")
REF = os.path.join(VAULT, "References", "Etching Table", "flame-band-reference.webp")
STUDS_PER_CM = 0.05
BG = (206, 199, 186)

BASE, EDGE_LINE, SPINE_LINE = 0.28, 0.032, 0.032    # band centre, bright line widths (fractions of the width)
RED_HI, RED_LO = np.array([165, 14, 10]), np.array([108, 9, 8])
DARK_HI, DARK_LO = np.array([30, 56, 84]), np.array([6, 12, 20])
LINE = np.array([205, 222, 240])
AMP = 0.14                                          # hump height, fraction of the width
K = math.log(0.5) / math.log(0.45)                 # puts the deepest red at 45% of each period


def humps(n_widths, seed=11):
    """Hump list along the blade in local widths: start, period, amplitude, optional small point."""
    rng = np.random.default_rng(seed)
    out, s = [], -rng.uniform(0, 0.6)
    while s < n_widths:
        period = rng.uniform(0.75, 1.05)
        out.append((s, period, AMP, None))   # even heights (Allen); only the spacing varies
        s += period
    return out


def reach(sw, hl):
    """Red reach from the edge (fraction of the width) at positions sw (local widths from the hilt)."""
    r = np.full_like(sw, BASE)
    for s0, period, amp, point in hl:
        ph = (sw - s0) / period
        m = (ph >= 0) & (ph < 1)
        p = np.sin(math.pi * np.clip(ph, 0, 1) ** K) ** 2          # 0 at the dark humps, 1 deepest red
        val = BASE + amp * (p - 0.5)
        if point is not None:
            val = val + 0.03 * np.clip(1 - np.abs(ph - point) / 0.035, 0, 1) ** 1.5
        r = np.where(m, val, r)
    return r


def draw_blade(name, px_per_cm=22):
    data = json.load(open(os.path.join(DATA, name + ".json"), encoding="utf-8"))
    st = data["stages"]["refined"]
    L = st["length"]

    def curve(pts):
        pts = sorted(pts)
        return lambda u: np.interp(u, [p[0] for p in pts], [p[1] for p in pts])

    spine, edge, ridge = curve(st["spine"]), curve(st["edge"]), curve(st["ridge"])
    # along-blade position in local widths: integrate dx / width (floor keeps the point finite)
    xs = np.linspace(0, L, 2000)
    wid = spine(xs / L) - edge(xs / L)
    sw_of_x = np.concatenate([[0], np.cumsum(np.diff(xs) / np.maximum(wid[1:], 0.8))])
    hl = humps(sw_of_x[-1])
    W = int(L * px_per_cm) + 2
    half_max = max(p[1] for p in st["spine"])
    H = int(2 * half_max * px_per_cm) + 6
    X, Y = np.meshgrid((np.arange(W) + 0.5) / px_per_cm, half_max + 0.1 - (np.arange(H) + 0.5) / px_per_cm)
    u = np.clip(X / L, 0, 1)
    sp, ed = spine(u), edge(u)
    inside = (Y <= sp) & (Y >= ed) & (X <= L)
    w = (Y - ed) / np.maximum(sp - ed, 1e-6)               # 0 edge .. 1 spine
    px_w = np.maximum(sp - ed, 1e-6) * px_per_cm           # blade width in pixels, for anti-aliasing
    R = reach(np.interp(X, xs, sw_of_x), hl)
    # bevel shading: lit near the edge, darker toward the ridge; the flat above the ridge stays dark
    wr = 1 - ridge(u)
    lit = np.where(w < wr, 1 - w / wr, 0.0) ** 1.4
    along = np.clip(1 - u / 0.5, 0.25, 1)                  # the sheen fades along the blade
    shade = (lit * along)[..., None]
    dark = DARK_LO + (DARK_HI - DARK_LO) * shade
    red = RED_LO + (RED_HI - RED_LO) * np.clip(shade * 1.4, 0, 1)
    red_cov = np.clip((R - w) * px_w + 0.5, 0, 1)[..., None]
    face = dark * (1 - red_cov) + red * red_cov
    crease = np.clip(1 - np.abs(w - wr) * px_w / 0.8, 0, 1)[..., None] * 0.12   # faint ridge line
    face = face * (1 - crease) + 120 * crease
    line_cov = np.clip(np.maximum(EDGE_LINE - w, w - (1 - SPINE_LINE)) * px_w + 0.5, 0, 1)[..., None]
    face = face * (1 - line_cov) + LINE * line_cov
    img = np.where(inside[..., None], face, np.array(BG, np.float32))
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)), data["name"], L, st


def oriented_section(name, n_widths=15.3, px_per_cm=40, angle=21.7, bend=0.06):
    """The first n_widths of a blade, edge up and hilt on the left, bent and turned like the reference view."""
    im, _, L, st = draw_blade(name, px_per_cm)
    im = im.transpose(Image.FLIP_TOP_BOTTOM)                # edge on top, like the reference
    base_w = st["spine"][0][1] - st["edge"][0][1]
    cut = int(min(L, n_widths * base_w * 0.85) * px_per_cm)
    a = np.asarray(im.crop((0, 0, cut, im.height)))
    pad = int(bend * cut) + 4
    out = np.zeros((a.shape[0] + pad, a.shape[1], 3), np.uint8) + np.array(BG, np.uint8)
    for x in range(a.shape[1]):                             # sori: the blade sags toward the point
        dy = int(round(bend * x * x / cut))
        out[dy:dy + a.shape[0], x] = a[:, x]
    return Image.fromarray(out).rotate(-angle, expand=True, resample=Image.BICUBIC, fillcolor=BG)


def main():
    font = small = ImageFont.load_default()
    try:
        font, small = ImageFont.truetype("arial.ttf", 22), ImageFont.truetype("arial.ttf", 18)
    except OSError:
        pass
    ref = Image.open(REF).convert("RGB")
    rev = oriented_section("katana")
    rev.thumbnail((ref.width, ref.height))
    rows = [draw_blade(n)[:3] for n in ("katana", "wakizashi", "tanto")]
    pad, gap = 40, 34
    width = max(2 * ref.width + 3 * pad, max(r[0].width for r in rows) + 2 * pad)
    height = pad + 30 + max(ref.height, rev.height) + 50 + sum(r[0].height + gap + 28 for r in rows) + pad
    sheet = Image.new("RGB", (width, height), BG)
    dr = ImageDraw.Draw(sheet)
    dr.text((pad, pad), "Reference (Allen's screenshot)", fill=(40, 36, 32), font=font)
    dr.text((2 * pad + ref.width, pad), "Flame etch v4: katana from the guard, same orientation", fill=(40, 36, 32), font=font)
    y = pad + 30
    sheet.paste(ref, (pad, y))
    sheet.paste(rev, (2 * pad + ref.width, y))
    y += max(ref.height, rev.height) + 50
    for im, nm, L in rows:
        dr.text((pad, y), f"{nm}: {L:.0f} cm ({L * STUDS_PER_CM:.2f} studs), flat, true scale, hilt on the left, edge at the bottom", fill=(40, 36, 32), font=small)
        y += 28
        sheet.paste(im, (pad, y))
        y += im.height + gap
    out = os.path.join(HERE, "flame_etch_v4_preview.png")
    sheet.save(out)
    print(out, sheet.size)


def check():
    hl = humps(30)
    r = reach(np.linspace(0, 30, 6000), hl)
    assert 0.18 < r.min() and r.max() < 0.42, (r.min(), r.max())
    assert abs(r.mean() - BASE) < 0.03, r.mean()
    assert all(0.75 <= h[1] <= 1.05 for h in hl)


if __name__ == "__main__":
    check()
    main()

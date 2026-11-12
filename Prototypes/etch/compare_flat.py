"""Fair side-by-side for judging the curled Flame by eye: the reference's straight stretch, straightened (edge down),
above our Flame drawn on a straight blade of the same width and length, in the same red and dark, no outlines.
Run:  python compare_flat.py  -> compare_flat.png next to this file"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import curled_flame_preview as cf
import flame_overlay as fo

HERE = os.path.dirname(os.path.abspath(__file__))


def ours_image(n_px, h_px, shift):
    L = 40.0
    polys = cf.flame_polys(L, lambda x: 1.0, L - 1.0)
    SS = 3
    m = Image.new("L", (n_px * SS, h_px * SS), 0)
    d = ImageDraw.Draw(m)
    for poly in polys:
        d.polygon([((x - shift) * h_px * SS, (1 - y) * h_px * SS) for x, y in poly], fill=255)
    k = np.asarray(m.resize((n_px, h_px), Image.LANCZOS), np.float32)[..., None] / 255
    rows = np.linspace(1, 0, h_px)[:, None, None]
    dark = np.array([22, 22, 26]) + np.array([18, 18, 20]) * (rows > 0.62)  # the photo's lighter flat near the spine
    red = np.array([150, 12, 10]) + np.array([40, 6, 4]) * rows  # darker toward the edge, as in the photo
    return Image.fromarray(np.clip(dark * (1 - k) + red * k, 0, 255).astype(np.uint8))


def main(shift=6.0):
    _, width, face = fo.reference()
    ref = Image.fromarray(face)
    ours = ours_image(ref.width, ref.height, shift)
    try:
        font = ImageFont.truetype("arial.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
    sheet = Image.new("RGB", (ref.width + 40, 2 * ref.height + 110), (230, 226, 218))
    d = ImageDraw.Draw(sheet)
    d.text((20, 10), "A: reference (straightened, edge down, 4.2 blade widths)", fill=(30, 30, 30), font=font)
    sheet.paste(ref, (20, 40))
    d.text((20, ref.height + 55), "B: curled Flame on a straight blade, same width and length", fill=(30, 30, 30), font=font)
    sheet.paste(ours, (20, ref.height + 85))
    out = os.path.join(HERE, "compare_flat.png")
    sheet.save(out)
    print(out)


if __name__ == "__main__":
    main()

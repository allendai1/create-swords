# python -I make_sparkle.py : writes sparkle.png (256 px, white, for ImageColor3 tints): a four-point star with
# concave sides (|x|^P + |y|^P = 1) on a soft glow, the twinkles on the Shop cards (2026-11-07).
import math, os
from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SIZE, SS = 256, 4
P = 0.45  # < 1 gives concave sides; lower = thinner points
R = 0.44  # star radius as a fraction of the image


def star(scale):
    n, c = SIZE * SS, SIZE * SS / 2
    pts = []
    for i in range(720):
        t = 2 * math.pi * i / 720
        ct, st = math.cos(t), math.sin(t)
        r = (abs(ct) ** P + abs(st) ** P) ** (-1 / P) if (ct or st) else 1
        pts.append((c + ct * r * R * scale * n, c + st * r * R * scale * n))
    m = Image.new("L", (n, n), 0)
    ImageDraw.Draw(m).polygon(pts, fill=255)
    return m.resize((SIZE, SIZE), Image.Resampling.LANCZOS)


core = star(1.0)
glow = star(0.75).filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(min(255, v * 1.6) * 0.6))
alpha = ImageChops.lighter(core, glow)  # star over its glow
out = Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 0))
out.putalpha(alpha)
out.save(os.path.join(HERE, "sparkle.png"))
print("wrote sparkle.png")

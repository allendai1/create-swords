# Sunray images for UI cards (Book sword cards, 2026-10-29): white rays on transparent, 512 px.
# Run: python make_rays.py  -> rays8.png, rays12.png, rays16.png, rays12thin.png, rays8soft.png next to this file.
import math, os
from PIL import Image

SIZE, SS = 512, 2  # output size, supersampling
HERE = os.path.dirname(os.path.abspath(__file__))


def rays(n, duty, soft=False, fade=0.35):
    s = SIZE * SS
    img = Image.new("L", (s, s), 0)
    px = img.load()
    c = s / 2
    for y in range(s):
        for x in range(s):
            dx, dy = x - c, y - c
            r = math.hypot(dx, dy) / c
            if r > 1.42:
                continue
            a = (math.atan2(dy, dx) / (2 * math.pi) * n) % 1  # position within one ray period
            if soft:
                v = max(0.0, math.cos(math.pi * (a - 0.5) / duty)) if abs(a - 0.5) < duty / 2 else 0.0
            else:
                v = 1.0 if abs(a - 0.5) < duty / 2 else 0.0
            v *= 1 - fade * min(r, 1)  # a little dimmer toward the edge
            px[x, y] = int(255 * v)
    alpha = img.resize((SIZE, SIZE), Image.LANCZOS)
    out = Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 0))
    out.putalpha(alpha)
    return out


for name, args in {
    "rays8": (8, 0.5),
    "rays12": (12, 0.5),
    "rays16": (16, 0.5),
    "rays12thin": (12, 0.28),
    "rays8soft": (8, 0.7, True, 0.6),
}.items():
    rays(*args).save(os.path.join(HERE, name + ".png"))
    print(name)

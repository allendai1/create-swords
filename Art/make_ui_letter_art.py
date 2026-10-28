"""Mail letter art and the guide's ground arrow (2026-10-27).

Run: python Art/make_ui_letter_art.py  -> Art/ui-guide-arrow.png, ui-letter-paper.png, ui-envelope.png, ui-wax-seal.png
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).parent
random.seed(7)


def guide_arrow():
    # Points right (+U along a Beam). Chunky green chevron-arrow with a dark rim and a soft glow, transparent round it.
    S = 512
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    shape = [(110, 200), (290, 200), (290, 110), (440, 256), (290, 402), (290, 312), (110, 312)]
    glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(glow).polygon(shape, fill=(70, 255, 90, 170))
    glow = glow.filter(ImageFilter.GaussianBlur(26))
    img.alpha_composite(glow)
    d = ImageDraw.Draw(img)
    d.polygon(shape, fill=(20, 120, 30, 255))  # rim
    inner = [(124, 214), (304, 214), (304, 144), (420, 256), (304, 368), (304, 298), (124, 298)]
    d.polygon(inner, fill=(60, 220, 70, 255))
    hi = [(124, 214), (304, 214), (304, 144), (362, 200), (124, 256)]
    d.polygon(hi, fill=(120, 245, 120, 255))  # light top half
    img.save(OUT / "ui-guide-arrow.png")


def noise_layer(w, h, scale, amount):
    small = Image.effect_noise((max(1, w // scale), max(1, h // scale)), amount).resize((w, h), Image.Resampling.BICUBIC)
    return small


def torn_mask(w, h, margin, jag):
    # A rough-edged rectangle: each side wanders and has small tears.
    pts = []
    def edge(x0, y0, x1, y1, nx, ny, n):
        for i in range(n):
            t = i / n
            off = margin + random.uniform(-jag, jag) + math.sin(t * 9 + random.random()) * jag * 0.4
            pts.append((x0 + (x1 - x0) * t + nx * off, y0 + (y1 - y0) * t + ny * off))
    n = 90
    edge(0, 0, w, 0, 0, 1, n)
    edge(w, 0, w, h, -1, 0, n)
    edge(w, h, 0, h, 0, -1, n)
    edge(0, h, 0, 0, 1, 0, n)
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).polygon(pts, fill=255)
    return m


def paper():
    W, H = 1200, 760
    base = Image.new("RGBA", (W, H), (244, 231, 204, 255))
    n = noise_layer(W, H, 6, 40).convert("L")
    blot = noise_layer(W, H, 60, 70).convert("L")
    px = base.load()
    npx, bpx = n.load(), blot.load()
    for y in range(H):
        for x in range(W):
            # darker toward the edges, blotchy, grainy
            ex = min(x, W - 1 - x) / (W * 0.5)
            ey = min(y, H - 1 - y) / (H * 0.5)
            edge = 1 - min(1, min(ex, ey) * 3.2)
            g = (npx[x, y] - 128) * 0.06 + (bpx[x, y] - 128) * 0.06 - edge * 30
            r, gg, b, _ = px[x, y]
            px[x, y] = (int(r + g), int(gg + g * 1.05), int(b + g * 1.25), 255)
    mask = torn_mask(W, H, 14, 7)
    shadow = Image.new("RGBA", (W, H), (60, 35, 15, 0))
    shadow.putalpha(mask.filter(ImageFilter.GaussianBlur(8)).point(lambda v: v * 0.55))
    paper_l = base.copy()
    paper_l.putalpha(mask)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.alpha_composite(shadow, (0, 6))
    out.alpha_composite(paper_l)
    out.save(OUT / "ui-letter-paper.png")


def envelope():
    W, H = 1000, 640
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    body = (16, 16, W - 16, H - 16)
    d.rectangle(body, fill=(232, 216, 186, 255))
    # flaps: shaded triangles meeting in the middle
    cx, cy = W / 2, H * 0.56
    d.polygon([(16, 16), (cx, cy), (16, H - 16)], fill=(222, 204, 172, 255))
    d.polygon([(W - 16, 16), (cx, cy), (W - 16, H - 16)], fill=(222, 204, 172, 255))
    d.polygon([(16, H - 16), (cx, cy - 40), (W - 16, H - 16)], fill=(214, 195, 160, 255))
    d.polygon([(16, 16), (W - 16, 16), (cx, cy)], fill=(238, 224, 196, 255))
    for a, b in [((16, 16), (cx, cy)), ((W - 16, 16), (cx, cy)), ((16, H - 16), (cx, cy - 40)), ((W - 16, H - 16), (cx, cy - 40))]:
        d.line([a, b], fill=(176, 150, 112, 255), width=3)
    d.rectangle(body, outline=(150, 120, 84, 255), width=4)
    grain = noise_layer(W, H, 5, 30).convert("L")
    tint = Image.new("RGBA", (W, H), (90, 60, 30, 0))
    tint.putalpha(grain.point(lambda v: max(0, v - 118) // 3))
    img.alpha_composite(Image.composite(tint, Image.new("RGBA", (W, H), (0, 0, 0, 0)), img.getchannel("A")))
    img.save(OUT / "ui-envelope.png")


def wax_seal():
    S = 512
    c = S / 2
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    # blobby outer rim
    pts = []
    for i in range(72):
        a = i / 72 * math.tau
        r = 200 + random.uniform(-10, 10) + 8 * math.sin(a * 5)
        pts.append((c + math.cos(a) * r, c + math.sin(a) * r))
    sh = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(sh).polygon([(x + 6, y + 10) for x, y in pts], fill=(40, 0, 0, 140))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(img)
    d.polygon(pts, fill=(150, 30, 34, 255))
    d.ellipse((c - 150, c - 150, c + 150, c + 150), fill=(122, 20, 26, 255))  # pressed ring
    d.ellipse((c - 132, c - 132, c + 132, c + 132), fill=(158, 36, 40, 255))
    # sword, diagonal: blade, guard, grip, pommel (darker emboss with a light edge)
    rot = math.radians(-45)
    def p(x, y):
        return (c + x * math.cos(rot) - y * math.sin(rot), c + x * math.sin(rot) + y * math.cos(rot))
    def quad(x0, y0, x1, y1, fill):
        d.polygon([p(x0, y0), p(x1, y0), p(x1, y1), p(x0, y1)], fill=fill)
    dark, light = (100, 14, 20, 255), (196, 70, 70, 255)
    d.polygon([p(-14, 40), p(14, 40), p(14, -80), p(0, -112), p(-14, -80)], fill=light)
    d.polygon([p(-10, 40), p(10, 40), p(10, -80), p(0, -104), p(-10, -80)], fill=dark)
    quad(-46, 40, 46, 56, dark)
    quad(-9, 56, 9, 100, dark)
    d.ellipse([*(v - 13 for v in p(0, 112)), *(v + 13 for v in p(0, 112))], fill=dark)
    img = img.filter(ImageFilter.SMOOTH)
    img.save(OUT / "ui-wax-seal.png")


if __name__ == "__main__":
    guide_arrow()
    paper()
    envelope()
    wax_seal()
    print("ok")

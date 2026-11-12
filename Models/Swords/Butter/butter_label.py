"""Butter Stick sword label (2026-11-07, Allen: "the text should be on the sword, and any metal on it, the text is still
there"). A transparent 1024 x 1024 PNG worn as two Decals (Top, Bottom) on the blade part (Shared/SwordMeshCache).
A decal on a MeshPart spreads over its bounding box, and BladeView's box is +-reach (72 cm = 3.6 studs) around the
blade's base in X and Z, so the 70 x 16 cm stick fills one thin band of the image: the top face's text in the left
half, the bottom face's in the right half, each turned 180 degrees (measured with a gradient image in Studio). Dark
blue text with a cream outline, so it reads on every metal. Run: python butter_label.py -> butter_label.png beside it.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = "C:/Windows/Fonts/"
INK, LINE = (24, 48, 138, 255), (255, 248, 222, 255)
# the face is 70 x 16 cm (4.375:1); draw at that ratio, then squeeze into a 1024 x 256 half
FW, FH = 1120, 256


def font(size, condensed=False):
    f = ImageFont.truetype(FONTS + "bahnschrift.ttf", size)
    f.set_variation_by_name("Bold Condensed" if condensed else "Bold")
    return f


def face():
    im = Image.new("RGBA", (FW, FH), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    def text(xy, s, f, anchor, stroke):
        d.text(xy, s, font=f, fill=INK, anchor=anchor, stroke_width=stroke, stroke_fill=LINE)

    text((150, 118), "4oz.", font(118), "mm", 5)
    text((150, 196), "NET WT. (113 G)", font(30), "mm", 3)
    text((720, 52), "SALTED", font(34), "mm", 3)
    text((720, 150), "BUTTER", font(190, True), "mm", 6)
    return im


SIZE, REACH, LENGTH, WIDTH = 1024, 72.0, 70.0, 16.0  # image px; cm (BladeView reach = length + 2)
px = lambda cm: round(cm / (2 * REACH) * SIZE)
w, h = px(LENGTH), px(WIDTH)
f = face().resize((w, h), Image.Resampling.LANCZOS).rotate(180)
out = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
top = SIZE // 2 - h // 2
out.paste(f, (SIZE // 2 - w, top))  # top face: blade X 0..70 runs right to left in the image's left half
out.paste(f, (SIZE // 2, top))  # bottom face: left to right in the right half
assert out.getpixel((0, 0))[3] == 0 and out.getpixel((SIZE - 1, SIZE - 1))[3] == 0
out.save(os.path.join(HERE, "butter_label.png"))
print("saved")

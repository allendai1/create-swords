# python -I make_clothes.py : the lever hand's classic Shirt and Pants templates (585 x 559, Roblox's layout), drawn
# flat in the game's painted palette (2026-11-07, Allen's reference for the NPC who pulls the ore lever: a village
# worker in a red vest over a white collar, wide yellow sleeves, dark baggy trousers). An original villager, not the
# reference's character: the hyottoko mask comes from the Swordsmith model the crew already wear.
# Writes shirt.png and pants.png next to this file.
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 585, 559
RED, RED_DARK = (178, 52, 40), (138, 36, 30)
WHITE, CREAM_SHADE = (244, 238, 224), (214, 204, 186)
YELLOW, YELLOW_DARK = (226, 176, 60), (192, 140, 40)
TIE = (232, 210, 150)
PANT, PANT_DARK = (62, 64, 72), (44, 46, 54)

# Roblox's template rectangles (x, y, w, h)
TORSO = {"up": (231, 8, 128, 64), "left": (165, 74, 64, 128), "front": (231, 74, 128, 128), "right": (361, 74, 64, 128),
         "back": (427, 74, 128, 128), "down": (231, 204, 128, 64)}
RARM = {"up": (217, 289, 64, 64), "left": (19, 355, 64, 128), "back": (85, 355, 64, 128), "right": (151, 355, 64, 128),
        "front": (217, 355, 64, 128), "down": (217, 485, 64, 64)}
LARM = {"up": (308, 289, 64, 64), "front": (308, 355, 64, 128), "left": (374, 355, 64, 128), "back": (440, 355, 64, 128),
        "right": (506, 355, 64, 128), "down": (308, 485, 64, 64)}


def fill(d, r, c):
    x, y, w, h = r
    d.rectangle((x, y, x + w - 1, y + h - 1), fill=c)


def sleeve(d, r, hand_row=True):
    x, y, w, h = r
    fill(d, r, YELLOW)
    for k in range(1, 4):  # soft vertical stripes, like the reference's woven sleeves
        sx = x + k * w // 4
        d.line((sx, y, sx, y + h - 1), fill=YELLOW_DARK, width=2)
    if hand_row:  # the cuff ends above the hand: skin shows below (the body colour)
        d.rectangle((x, y + h - 22, x + w - 1, y + h - 1), fill=(0, 0, 0, 0))
        d.line((x, y + h - 23, x + w - 1, y + h - 23), fill=YELLOW_DARK, width=3)


def shirt():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for k, r in TORSO.items():
        fill(d, r, RED)
    # front: the white collar in a V, the vest's edges, a pale tie knot at the waist
    x, y, w, h = TORSO["front"]
    cx = x + w // 2
    d.polygon([(x + 34, y), (cx, y + 62), (x + w - 34, y)], fill=WHITE)
    d.polygon([(x + 44, y), (cx, y + 50), (x + w - 44, y)], fill=CREAM_SHADE)
    d.line((cx, y + 62, cx - 16, y + h - 1), fill=RED_DARK, width=3)  # the vest's overlap
    d.rectangle((x, y + h - 30, x + w - 1, y + h - 22), fill=RED_DARK)  # a cord round the waist
    d.ellipse((cx + 10, y + h - 34, cx + 26, y + h - 18), fill=TIE)
    d.line((cx + 18, y + h - 20, cx + 14, y + h - 4), fill=TIE, width=4)
    d.line((cx + 20, y + h - 20, cx + 26, y + h - 6), fill=TIE, width=4)
    # back: the collar's band
    x, y, w, h = TORSO["back"]
    d.rectangle((x + 40, y, x + w - 41, y + 10), fill=WHITE)
    d.rectangle((x, y + h - 30, x + w - 1, y + h - 22), fill=RED_DARK)
    for side in ("left", "right"):
        x, y, w, h = TORSO[side]
        d.rectangle((x, y + h - 30, x + w - 1, y + h - 22), fill=RED_DARK)
    x, y, w, h = TORSO["up"]
    d.rectangle((x + 34, y + h - 16, x + w - 35, y + h - 1), fill=WHITE)
    for arm in (RARM, LARM):
        for k, r in arm.items():
            if k == "up":
                fill(d, r, YELLOW)
            elif k == "down":
                continue  # the hand's underside: skin
            else:
                sleeve(d, r)
    return im


def pants():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for k in ("front", "back", "left", "right", "down"):
        fill(d, TORSO[k], PANT)
    for leg in (RARM, LARM):
        for k, r in leg.items():
            if k == "down":
                continue
            fill(d, r, PANT)
            x, y, w, h = r
            if k != "up":
                for s in range(2):  # folds of a baggy leg
                    fx = x + 16 + s * 28
                    d.line((fx, y + 10, fx + 6, y + h - 30), fill=PANT_DARK, width=3)
                d.rectangle((x, y + h - 16, x + w - 1, y + h - 1), fill=PANT_DARK)  # gathered at the ankle
    return im


shirt().save(os.path.join(HERE, "shirt.png"))
pants().save(os.path.join(HERE, "pants.png"))
print("ok")

"""Draws the four weather icons (Sunny, Snow, Rain, Rainbow) in the Free Icon Pack's 1st Outline look:
navy outline, flat cel-shaded fill (shadow rim, body, top highlight), small white glint. Original art, 256 px."""
import math
import sys
import numpy as np
import cv2
from PIL import Image, ImageDraw

N = 1024  # supersampled canvas, downscaled 4x
OW = 46  # outline width at N
NAVY = (4, 4, 53)
OUT = sys.argv[1]


def blank():
    return Image.new("L", (N, N), 0)


def A(img):
    return np.array(img) > 127


def disk(r):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def dil(a, r):
    return cv2.dilate(a.astype(np.uint8), disk(r)) > 0


def ero(a, r):
    return cv2.erode(a.astype(np.uint8), disk(r)) > 0


def shift(a, dx, dy):
    m = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(a.astype(np.uint8), m, (N, N)) > 0


def rounded(a, r):  # round off sharp corners
    return dil(ero(a, r), r)


class Canvas:
    def __init__(self):
        self.rgba = np.zeros((N, N, 4), np.uint8)

    def paint(self, a, col):
        self.rgba[a] = (*col, 255)

    def piece(self, a, dark, mid, light, d=34, glint=None, hi=None):
        """Outline, shadow rim lower-left, body, highlight up top, white glint."""
        self.paint(dil(a, OW), NAVY)
        self.paint(a, dark)
        body = a & shift(a, d, -d)
        self.paint(body, mid)
        h = a & (hi if hi is not None else shift(ero(a, int(d * 1.5)), d, -2 * d))
        self.paint(h, light)
        if glint is not None:
            self.paint(glint & a, (255, 255, 255))

    def save(self, path):
        Image.fromarray(self.rgba, "RGBA").resize((256, 256), Image.Resampling.LANCZOS).save(path)


def ellipse(cx, cy, rx, ry, angle=0):
    m = np.zeros((N, N), np.uint8)
    cv2.ellipse(m, (int(cx), int(cy)), (int(rx), int(ry)), angle, 0, 360, 1, -1)
    return m > 0


def poly(pts):
    m = blank()
    ImageDraw.Draw(m).polygon([tuple(p) for p in pts], fill=255)
    return A(m)


def thick_line(x0, y0, x1, y1, w):
    m = np.zeros((N, N), np.uint8)
    cv2.line(m, (int(x0), int(y0)), (int(x1), int(y1)), 1, int(w))
    m = m > 0
    return m | ellipse(x0, y0, w / 2, w / 2) | ellipse(x1, y1, w / 2, w / 2)


def cloud(cx, cy, s):
    """A puffy cloud: three top puffs on a flat rounded base. s = width scale (1 = ~760 px wide)."""
    a = ellipse(cx - 200 * s, cy + 40 * s, 170 * s, 140 * s)
    a |= ellipse(cx + 10 * s, cy - 70 * s, 230 * s, 210 * s)
    a |= ellipse(cx + 230 * s, cy + 30 * s, 160 * s, 150 * s)
    a |= ellipse(cx, cy + 90 * s, 330 * s, 110 * s)
    return rounded(a, int(20 * s))


def glint_at(cx, cy, r):
    return ellipse(cx, cy, r, r * 0.62, -35)


# ---- Sunny ----------------------------------------------------------------------------------------
def sunny(path):
    c = Canvas()
    cx = cy = N / 2
    rays = np.zeros((N, N), bool)
    for i in range(8):
        t = math.radians(i * 45 - 90)
        u = (math.cos(t), math.sin(t))
        v = (-u[1], u[0])
        r0, r1, w = 240, 425, 88
        pts = [(cx + u[0] * r0 + v[0] * w, cy + u[1] * r0 + v[1] * w), (cx + u[0] * r1, cy + u[1] * r1),
               (cx + u[0] * r0 - v[0] * w, cy + u[1] * r0 - v[1] * w)]
        rays |= poly(pts)
    rays = rounded(rays, 26)
    c.piece(rays, (232, 118, 22), (255, 160, 36), (255, 196, 84), d=22, hi=np.zeros((N, N), bool))
    disc = ellipse(cx, cy, 270, 270)
    c.piece(disc, (240, 170, 20), (255, 210, 48), (255, 236, 130), d=40,
            glint=glint_at(cx - 120, cy - 130, 52))
    c.save(path)


# ---- Snow -----------------------------------------------------------------------------------------
def snow(path):
    c = Canvas()
    cx = cy = N / 2
    a = ellipse(cx, cy, 120, 120)
    for i in range(6):
        t = math.radians(i * 60 - 90)
        ex, ey = cx + math.cos(t) * 375, cy + math.sin(t) * 375
        a |= thick_line(cx, cy, ex, ey, 96)
        bx, by = cx + math.cos(t) * 235, cy + math.sin(t) * 235
        for side in (-1, 1):
            tb = t + side * math.radians(48)
            a |= thick_line(bx, by, bx + math.cos(tb) * 140, by + math.sin(tb) * 140, 80)
    c.piece(a, (110, 178, 232), (168, 222, 255), (226, 246, 255), d=26,
            glint=glint_at(cx - 38, cy - 310, 28) | glint_at(cx - 55, cy - 40, 34))
    c.save(path)


# ---- Rain -----------------------------------------------------------------------------------------
def drop(x, y, r):
    a = ellipse(x, y, r, r)
    a |= poly([(x - r * 0.97, y - r * 0.25), (x, y - r * 2.3), (x + r * 0.97, y - r * 0.25)])
    return rounded(a, 10)


def rain(path):
    c = Canvas()
    drops = drop(330, 850, 72) | drop(530, 905, 72) | drop(730, 850, 72)
    c.piece(drops, (24, 104, 210), (52, 150, 240), (130, 200, 255), d=20,
            glint=glint_at(305, 845, 20) | glint_at(505, 900, 20) | glint_at(705, 845, 20))
    body = cloud(N / 2, 380, 0.98)
    c.piece(body, (136, 160, 196), (182, 202, 230), (222, 232, 248), d=38,
            glint=glint_at(N / 2 - 90, 230, 44))
    c.save(path)


# ---- Rainbow --------------------------------------------------------------------------------------
def rainbow(path):
    c = Canvas()
    cx, cy = N / 2, 650
    bands = [(255, 74, 74), (255, 156, 40), (255, 222, 60), (96, 210, 80), (70, 160, 250)]
    bw, r_out = 56, 430
    yy, xx = np.mgrid[0:N, 0:N]
    dist = np.hypot(xx - cx, yy - cy)
    top = yy <= cy
    arc = top & (dist <= r_out) & (dist >= r_out - bw * len(bands))
    c.paint(dil(arc, OW), NAVY)
    for i, col in enumerate(bands):
        ring = top & (dist <= r_out - bw * i) & (dist > r_out - bw * (i + 1))
        c.paint(ring, col)
        # top-edge highlight strip of each band
        lite = tuple(min(255, int(v + (255 - v) * 0.45)) for v in col)
        c.paint(ring & (dist > r_out - bw * i - 16), lite)
    c.paint(arc & glint_at(cx - 250, cy - 300, 26), (255, 255, 255))
    for x in (cx - 300, cx + 300):
        c.piece(cloud(x, 680, 0.4), (196, 212, 234), (234, 242, 252), (255, 255, 255), d=18)
    c.save(path)


# ---- Golden Hour (2026-11-09) ----------------------------------------------------------------------
def sparkle(cx, cy, r):
    """A four-point star."""
    w = r * 0.3
    return poly([(cx, cy - r), (cx + w, cy - w), (cx + r, cy), (cx + w, cy + w), (cx, cy + r), (cx - w, cy + w),
                 (cx - r, cy), (cx - w, cy - w)])


def golden(path):
    """A low sun on the horizon, rays fanning up, two sparkles: every boost at once."""
    c = Canvas()
    cx, cy = N / 2, 660
    rays = np.zeros((N, N), bool)
    for deg in (-90, -54, -18, 18, 54, 90):
        t = math.radians(deg - 90)
        u = (math.cos(t), math.sin(t))
        v = (-u[1], u[0])
        r0, r1, w = 250, 420, 80
        rays |= poly([(cx + u[0] * r0 + v[0] * w, cy + u[1] * r0 + v[1] * w), (cx + u[0] * r1, cy + u[1] * r1),
                      (cx + u[0] * r0 - v[0] * w, cy + u[1] * r0 - v[1] * w)])
    rays = rounded(rays, 24) & (np.mgrid[0:N, 0:N][0] <= cy)
    c.piece(rays, (214, 112, 18), (250, 150, 30), (255, 190, 80), d=22, hi=np.zeros((N, N), bool))
    disc = ellipse(cx, cy, 270, 270) & (np.mgrid[0:N, 0:N][0] <= cy)
    c.piece(disc, (236, 150, 16), (255, 196, 40), (255, 232, 120), d=40, glint=glint_at(cx - 120, cy - 150, 50))
    ground = rounded(poly([(150, cy + 10), (874, cy + 10), (874, cy + 130), (150, cy + 130)]), 40)
    c.piece(ground, (190, 110, 30), (226, 146, 48), (246, 184, 90), d=24)
    stars = sparkle(200, 230, 90) | sparkle(830, 300, 70)
    c.piece(stars, (240, 190, 40), (255, 226, 90), (255, 248, 190), d=14, hi=np.zeros((N, N), bool))
    c.save(path)


for name, fn in (("Sunny", sunny), ("Snow", snow), ("Rain", rain), ("Rainbow", rainbow), ("GoldenHour", golden)):
    fn(f"{OUT}/Weather {name} 256px.png")

# side-by-side sheet with the pack's cloud for comparison (when its path is given)
if len(sys.argv) < 3:
    sys.exit()
sheet = Image.new("RGBA", (256 * 5, 256), (60, 60, 60, 255))
pack = Image.open(sys.argv[2]).convert("RGBA")
for i, im in enumerate([pack] + [Image.open(f"{OUT}/Weather {n} 256px.png") for n in ("Sunny", "Snow", "Rain", "Rainbow")]):
    sheet.alpha_composite(im, (256 * i, 0))
sheet.save(f"{OUT}/_sheet.png")
small = sheet.resize((sheet.width * 48 // 256, 48), Image.Resampling.LANCZOS)
small.save(f"{OUT}/_sheet_small.png")

# py -3.11 -I make_sparks.py : writes the anvil hit textures (white, tinted by the emitters' Color), 2026-11-10.
#   streak.png  128 px: a thin hot streak, round bright head at the top tapering to a fading tail (VelocityParallel
#               points the top along the spark's flight; Squash stretches it).
#   flare.png   256 px: the contact flash, a hot core in a soft glow with four long and four short thin rays.
import math, os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))


def save(alpha, name):
    a = (np.clip(alpha, 0, 1) * 255).astype(np.uint8)
    rgba = np.dstack([np.full_like(a, 255)] * 3 + [a])
    Image.fromarray(rgba, "RGBA").save(os.path.join(HERE, name))
    print("wrote", name)


# streak: head at y 0.12, tail at y 0.95 (of the height)
N = 128
y, x = np.mgrid[0:N, 0:N].astype(float) / (N - 1)
dx = np.abs(x - 0.5)
along = np.clip((y - 0.12) / (0.95 - 0.12), 0, 1)  # 0 at the head, 1 at the tail
width = 0.045 * (1 - along) ** 0.6 + 0.005  # tapers to a point
body = np.exp(-(dx / width) ** 2) * (1 - along) ** 0.9 * (y >= 0.12)
head = np.exp(-((dx / 0.05) ** 2 + ((y - 0.12) / 0.05) ** 2))  # the round hot tip
above = np.exp(-(np.clip(0.12 - y, 0, None) / 0.05) ** 2)  # the glow rounds off over the head, no hard edge
glow = np.exp(-(dx / (width * 3.5)) ** 2) * (1 - along) ** 1.6 * 0.4 * above
save(np.maximum.reduce([body, head, glow]), "streak.png")

# flare
N = 256
y, x = np.mgrid[0:N, 0:N].astype(float) / (N - 1) - 0.5
r = np.hypot(x, y)
ang = np.arctan2(y, x)
core = np.exp(-(r / 0.05) ** 2)
glow = np.exp(-(r / 0.16) ** 2) * 0.55
rays = np.zeros_like(r)
for i in range(8):
    t = i * math.pi / 4 + 0.12 * (i % 2)  # a slight twist on the short rays
    length = 0.48 if i % 2 == 0 else 0.26
    d = np.abs(np.sin(ang - t)) * r  # distance from the ray's line
    ahead = np.cos(ang - t) > 0
    rays = np.maximum(rays, np.exp(-(d / 0.006) ** 2) * np.clip(1 - r / length, 0, 1) ** 1.5 * ahead)
edge = np.clip((0.5 - r) / 0.04, 0, 1)  # nothing at the square's edge
save(np.maximum.reduce([core, glow, rays * 0.9]) * edge, "flare.png")

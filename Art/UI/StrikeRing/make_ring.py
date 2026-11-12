# The anvil's strike ring (2026-11-09): a white band with black edges, drawn 4x and scaled down for clean edges.
# 256 px shows at 56 px: white band 4 px, black edges 1.5 px (radii 128/121/103/96 at 256).
from PIL import Image, ImageDraw
N, K = 256, 4
img = Image.new("RGBA", (N * K, N * K), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
c = N * K / 2
for r, col in ((128, (0, 0, 0, 255)), (121, (255, 255, 255, 255)), (103, (0, 0, 0, 255)), (96, (0, 0, 0, 0))):
    R = r * K
    d.ellipse((c - R, c - R, c + R, c + R), fill=col)
img.resize((N, N), Image.LANCZOS).save("strike_ring.png")
print("ok")

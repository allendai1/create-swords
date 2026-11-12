"""Black sword silhouettes for the sword pads (2026-11-07, Allen: "The sword upgrades should get the black sword
silhouette shape above it like the swordcrafter has a headshot above its upgrade pad").

Input: one JSON per blueprint, {id, tris: [x, z, x, z, x, z, ...]}, the sword's real hilt meshes and baked blade
(ReplicatedStorage.SwordMeshes B|<id>|0) flattened onto the flat face in sword space (X along the sword), exported
from Studio Edit. Output: <id>.png, 256 px, point up and to the right, black (12, 8, 6) with a thin white rim, on clear.

Usage: python draw_silhouettes.py <json dir> <out dir>
"""
import json, math, os, sys
from PIL import Image, ImageDraw, ImageFilter

SIZE, SS, MARGIN, RIM = 256, 4, 10, 3
INK = (12, 8, 6)


def draw(tris):
    c, s = math.cos(math.pi / 4), math.sin(math.pi / 4)
    pts = [(tris[i] * c - tris[i + 1] * s, tris[i] * s + tris[i + 1] * c) for i in range(0, len(tris), 2)]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    span = max(max(xs) - min(xs), max(ys) - min(ys))
    k = (SIZE - 2 * MARGIN - 2 * RIM) * SS / span
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    big = Image.new("L", (SIZE * SS, SIZE * SS), 0)
    d = ImageDraw.Draw(big)
    half = SIZE * SS / 2
    for i in range(0, len(pts), 3):
        tri = [(half + (x - cx) * k, half - (y - cy) * k) for x, y in pts[i:i + 3]]
        d.polygon(tri, fill=255)
    alpha = big.resize((SIZE, SIZE), Image.LANCZOS)
    rim = alpha.filter(ImageFilter.MaxFilter(2 * RIM + 1)).filter(ImageFilter.GaussianBlur(0.6))
    out = Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 0))
    out.putalpha(rim)
    ink = Image.new("RGBA", (SIZE, SIZE), INK + (255,))
    ink.putalpha(alpha)
    return Image.alpha_composite(out, ink)


def main(src, dst):
    os.makedirs(dst, exist_ok=True)
    made = []
    for name in sorted(os.listdir(src)):
        if name.endswith(".json"):
            data = json.load(open(os.path.join(src, name)))
            img = draw(data["tris"])
            assert img.size == (SIZE, SIZE) and img.getbbox() is not None, name
            img.save(os.path.join(dst, data["id"] + ".png"))
            made.append(data["id"])
    print(len(made), "silhouettes:", ", ".join(made))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

# freestylized_textures.py: prepares the FreeStylized 2K textures for the style's MaterialVariants (2026-10-22). Allen:
# "Yes, download the 2K versions of the picked FreeStylized textures (Ground_02, Ground_Stones_01, Concrete_Wall_01,
# Stones_Wall_02, Wood_10, Wood_02, Wood_11) and swap them into the Paint* MaterialVariants."
# Source: https://freestylized.com/material/<name>/ ("Royalty Free License: Free to use for all Commercial and
# Non-Commercial purposes"), 2K zips from .../Textures/2k/<name>_2k.zip, unzipped flat into one folder.
# Per texture: colour x ambient occlusion (0.6), then white-balanced (each channel divided by its mean, scaled to 0.82)
# and mostly greyed (TINT) so the part colour still sets the hue as with the painted tiles, while the texture keeps its
# own light and dark and a little of its tint; OpenGL normal map (Roblox's convention); roughness floored at 0.6 (no shine). All resized to 1024 (Roblox's
# limit). Run: python -I freestylized_textures.py <unzipped dir> <out dir> [variant=source ...]  ->  <variant>_{color,normal,rough}.png
# (with variant=source pairs, only those are made, e.g. PaintFloor=floor_tiles_09 for a trial).
# 2026-10-25, Allen: "replace some of our current textures with appropriate textures": PaintPlanks wood_11 -> wood_planks_04
# (clean warm boards), new PaintCrate (wood_planks_23: crate face with iron brackets and a cloth banner, one per crate
# side) and PaintFloor (floor_tiles_01: big worn stone tiles, the workshop floor).
import os, sys
import numpy as np
from PIL import Image

N = 1024
TINT = 0.35  # how much of the white-balanced tint survives (full balance turned wood blue and earth pink)
TEX = {  # variant -> source name
    "PaintEarth": "ground_02",
    "PaintStone": "ground_stones_01",
    "PaintPlaster": "concrete_wall_01",
    "PaintStoneWall": "stone_wall_02",
    "PaintWood": "wood_10",
    "PaintWoodDark": "wood_02",
    "PaintPlanks": "wood_planks_04",
    "PaintCrate": "wood_planks_23",
    "PaintFloor": "floor_tiles_01",
    "PaintFurniture": "wood_09",  # shop displays, cashier counter, workshop benches and racks (2026-10-25)
}


def find(src, name, *kinds):
    for k in kinds:
        p = os.path.join(src, f"{name}_{k}_2k.png")
        if os.path.exists(p):
            return p
    raise FileNotFoundError(f"{name}: none of {kinds}")


def load(p, mode):
    return np.asarray(Image.open(p).convert(mode).resize((N, N), Image.Resampling.LANCZOS), dtype=float) / 255


def main(src, out, tex=TEX):
    os.makedirs(out, exist_ok=True)
    for variant, name in tex.items():
        col = load(find(src, name, "color", "baseColor", "basecolor"), "RGB")
        ao = load(find(src, name, "ambient_occlusion", "ambientOcclusion", "ambientocclusion"), "L")
        col = col * (1 - 0.6 * (1 - ao))[..., None]
        col = col / col.reshape(-1, 3).mean(0) * 0.82
        grey = (col @ np.array([0.299, 0.587, 0.114]))[..., None]
        col = grey + TINT * (col - grey)  # mostly light and dark; a little of the texture's own tint (moss, grain)
        Image.fromarray((col.clip(0, 1) * 255).astype(np.uint8)).save(os.path.join(out, f"{variant}_color.png"))
        nrm = Image.open(find(src, name, "normal_gl")).convert("RGB").resize((N, N), Image.Resampling.LANCZOS)
        nrm.save(os.path.join(out, f"{variant}_normal.png"))
        rough = np.maximum(load(find(src, name, "roughness"), "L"), 0.6)
        Image.fromarray((rough * 255).astype(np.uint8)).save(os.path.join(out, f"{variant}_rough.png"))
        print(variant, name, "mean", col.reshape(-1, 3).mean(0).round(2))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], dict(a.split("=") for a in sys.argv[3:]) or TEX)

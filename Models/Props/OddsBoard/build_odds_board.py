# OddsBoard - Lucky Metal's Ore Chances sign as a village notice board (kosatsu), Sell Swords! 2026-11-07 (Allen: the
# board "looks a bit plain ... anything that could also fit the theme of japanese demon slayer small village vibe").
# Low poly, flat shaded, the festival props' helpers and export. Built around the sign's existing Face part (a plain
# Roblox Part that carries OddsGui; it is not in this mesh): 9.04 wide, 2.75 to 10.06 above the post feet.
#   Wood         - two posts on foot blocks, a top bar and a bottom bar framing the face, a low rail, an upper beam
#   Roof         - a tiled gable over it all, wide enough to shelter the two lanterns
#   Rope         - a shimenawa straw rope along the upper beam, thicker in the middle
#   Paper        - four shide paper zigzags hanging from the rope (over the top bar, clear of the face's text)
#   LanternPaper - two small paper lanterns under the eaves (red; in Studio under Board, every look)
#   LanternGold  - the same lanterns 4% larger (gold; in Studio under Owned: they cover the red ones once owned)
#   LanternDark  - their caps and cords
#
# Run in Blender (MCP execute_blender_code: exec(open(<this file>).read())). Writes OddsBoard.fbx next to this file.
# Units are studs, Z up, the front faces -Y (Roblox -Z), origin on the floor at the foot centre.
import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

FESTIVAL = "C:/Users/Allen/Documents/Create Swords!/Models/Props/Festival/build_festival.py"
_src = open(FESTIVAL).read()
exec(_src[:_src.index("def export(name):")])
HERE = "C:/Users/Allen/Documents/Create Swords!/Models/Props/OddsBoard"  # the festival file sets its own

FACE_W, FACE_Z0, FACE_Z1 = 9.04, 2.75, 10.06  # the Face part's width and its bottom and top over the post feet
PX = 4.82  # post centres


def limb(p0, p1, r0, r1, verts=6):
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    o = cyl(r0, d.length, (p0 + p1) / 2, verts=verts, r2=r1)
    o.rotation_mode = "QUATERNION"
    o.rotation_quaternion = d.normalized().to_track_quat("Z", "Y")
    return o


def build():
    coll = fresh_collection("OddsBoard")
    parts = {}
    wood = []
    for x in (-PX, PX):
        wood.append(box((0.6, 0.6, 11.8), (x, 0, 5.9)))            # posts, tucked up into the roof
        wood.append(box((0.85, 0.85, 0.25), (x, 0, 0.125)))        # foot blocks
    wood.append(box((10.4, 0.6, 0.44), (0, 0, FACE_Z1 + 0.22)))    # top bar on the face's top edge
    wood.append(box((FACE_W, 0.56, 0.32), (0, 0, FACE_Z0 - 0.16)))  # bottom bar under it
    wood.append(box((FACE_W, 0.3, 0.24), (0, 0, 0.95)))            # low rail
    wood.append(box((11.0, 0.4, 0.36), (0, 0, 11.05)))             # upper beam
    parts["Wood"] = join(wood, "Wood", coll)

    parts["Roof"] = join(gable(12.8, 1.45, 12.35, math.radians(34), 13, thick=0.18), "Roof", coll)

    # shimenawa: sags from the posts to the middle, fattest at the middle
    def rope_at(t):  # t in -1..1 across
        return Vector((t * 4.4, -0.45, 10.74 + 0.22 * t * t))
    rope = []
    n = 8
    for k in range(n):
        t0, t1 = -1 + 2 * k / n, -1 + 2 * (k + 1) / n
        r0 = 0.11 + 0.08 * (1 - abs(t0))
        r1 = 0.11 + 0.08 * (1 - abs(t1))
        rope.append(limb(rope_at(t0), rope_at(t1), r0, r1, verts=6))
        rope.append(cyl(r1 * 1.0, 0.04, rope_at(t1), verts=6))  # knot rings hide the segment joins
    parts["Rope"] = join(rope, "Rope", coll)

    # shide: three steps zigzagging down from the rope's underside
    paper = []
    for x in (-3.3, -1.1, 1.1, 3.3):
        top = rope_at(x / 4.4).z - 0.12
        for k in range(3):
            paper.append(box((0.2, 0.03, 0.2), (x + (0.06 if k % 2 == 0 else -0.06), -0.58, top - 0.1 - k * 0.19)))
    parts["Paper"] = join(paper, "Paper", coll)

    # lanterns under the eaves, outside the posts
    prof = [(0, 0), (0.42, 0.0), (0.6, 0.18), (0.655, 0.36), (0.65, 0.45), (0.655, 0.54), (0.6, 0.72), (0.42, 0.9), (0, 0.9)]
    s, top = 0.75, 10.95
    h = 0.9 * s
    reds, golds, dark = [], [], []
    for x in (-5.75, 5.75):
        p = [(r * s, z * s) for r, z in prof]
        reds.append(lathe(p, (x, -0.6, top - h), verts=8))
        mid = top - h / 2
        g = [(r * s * 1.04, (z * s - h / 2) * 1.04 + h / 2) for r, z in prof]
        golds.append(lathe(g, (x, -0.6, top - h), verts=8))
        dark.append(cyl(0.035, 0.7, (x, -0.6, top + 0.35), verts=4))
        dark.append(cyl(0.46 * s, 0.075, (x, -0.6, top + 0.015), verts=8))
        dark.append(cyl(0.46 * s, 0.075, (x, -0.6, top - h - 0.015), verts=8))
    parts["LanternPaper"] = join(reds, "LanternPaper", coll)
    parts["LanternGold"] = join(golds, "LanternGold", coll)
    parts["LanternDark"] = join(dark, "LanternDark", coll)
    return coll, parts


def export(name):
    p = os.path.join(SKILLS, "blender-export-pipelines", "scripts")
    if p not in sys.path:
        sys.path.insert(0, p)
    import importlib
    exp = importlib.import_module("export_asset")
    return exp.run(preset="roblox", collection=name, out=os.path.join(HERE, name + ".fbx"), batch=False, no_anim=True)


coll, PARTS = build()
print({n: len(o.data.polygons) for n, o in PARTS.items()},
      "tris", sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in PARTS.values()))

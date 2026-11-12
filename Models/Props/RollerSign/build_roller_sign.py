# RollerSign - the Auto Ore Roller's spot before it is bought, Sell Swords! 2026-11-10 (Allen: the buy prompt stood
# over "nothing physical"; he picked "Small sign post"). A small village kanban by the lever: one post on a foot block,
# a framed plank and a little tiled cap. The plank's face is a plain Roblox Part (Face, carrying the pass's icon as a
# Decal); it is not in this mesh. The lever hand villager replaces it once the pass is owned (WorldStoreController:
# the sign is under AutoRoller.Locked).
#   Wood - post, foot block, the frame around the face, the plank behind it
#   Roof - a small tiled gable over the plank
#
# Run in Blender (MCP execute_blender_code: exec(open(<this file>).read())), then export("RollerSign").
# Units are studs, Z up, the front faces -Y (Roblox -Z), origin on the floor at the post's foot.
import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

FESTIVAL = "C:/Users/Allen/Documents/Create Swords!/Models/Props/Festival/build_festival.py"
_src = open(FESTIVAL).read()
exec(_src[:_src.index("def export(name):")])
HERE = "C:/Users/Allen/Documents/Create Swords!/Models/Props/RollerSign"

FACE_W, FACE_Z0, FACE_Z1 = 1.7, 2.0, 3.3  # the Face part's width, bottom and top over the foot
FRAME = 0.16


def build():
    coll = fresh_collection("RollerSign")
    parts = {}
    zc = (FACE_Z0 + FACE_Z1) / 2
    h = FACE_Z1 - FACE_Z0
    wood = [
        box((0.34, 0.34, 3.9), (0, 0.22, 1.95)),                                     # post behind the plank, up into the cap
        box((0.6, 0.6, 0.2), (0, 0.22, 0.1)),                                        # foot block
        box((FACE_W + 0.1, 0.12, h + 0.1), (0, 0.0, zc)),                            # plank behind the face
        box((FACE_W + 2 * FRAME, 0.2, FRAME), (0, -0.04, FACE_Z1 + FRAME / 2)),      # frame top
        box((FACE_W + 2 * FRAME, 0.2, FRAME), (0, -0.04, FACE_Z0 - FRAME / 2)),      # frame bottom
        box((FRAME, 0.2, h), (-(FACE_W + FRAME) / 2, -0.04, zc)),                    # frame sides
        box((FRAME, 0.2, h), ((FACE_W + FRAME) / 2, -0.04, zc)),
    ]
    parts["Wood"] = join(wood, "Wood", coll)
    parts["Roof"] = join(gable(2.5, 0.45, 3.8, math.radians(34), 5, thick=0.1), "Roof", coll)
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

# Sorting bench and straw tray for the ore slots (2026-11-07; Allen on the sanbo stands: "my concern is more so the
# pedestals. do they make sense?", then "Yes, build benches"): smiths graded their steel by quality, which is what a
# rarity reveal is. Low poly, flat shaded, the festival props' helpers. Two collections, each its own FBX:
#   SortBench - one low workbench under a row of three slots (the stands' 4.3 spacing): a top of three planks, six
#               legs, front and back stretchers, end rails. 12.8 long, 2.6 deep, top at 2.52 over the floor. Bench.
#   SortTray  - one slot's woven straw tray, sitting on the bench: floor (its top 2.6 over the floor, where the ingot
#               lay before), a low rim, darker weave strips across the floor and a band round the rim. Straw, Weave.
#               In Studio it goes inside each Stand model, so it hides with the slot until bought.
# Run in Blender (MCP execute_blender_code: exec(open(<this file>).read())). Units are studs, Z up, the front faces -Y,
# origin on the floor (the tray: on the floor under its centre).
import math

import bmesh
import bpy
from mathutils import Vector

FESTIVAL = "C:/Users/Allen/Documents/Create Swords!/Models/Props/Festival/build_festival.py"
_src = open(FESTIVAL).read()
exec(_src[:_src.index("def export(name):")])
HERE = "C:/Users/Allen/Documents/Create Swords!/Models/Props/OreRollerV3"
SOFT = True  # the stations' soft bevels (2026-11-07, Allen: "it doesnt have the bevelled edges style in the models")
if SOFT:
    exec(open("C:/Users/Allen/Documents/Create Swords!/Models/Props/soft_bevel.py").read())

TOP = 2.52     # the bench top, under the trays
TRAY = 2.6     # the tray floor's top, where the ingot lies


def build_bench():
    coll = fresh_collection("SortBench")
    L, D, T = 12.8, 2.6, 0.22
    parts = []
    w = (D - 0.06) / 3
    for k in range(3):  # three planks, 0.03 apart
        parts.append(box((L, w, T), (0, -D / 2 + w / 2 + k * (w + 0.03), TOP - T / 2)))
    for x in (-5.9, 0, 5.9):
        for y in (-0.95, 0.95):
            parts.append(box((0.32, 0.32, TOP - T), (x, y, (TOP - T) / 2)))
    for y in (-0.95, 0.95):
        parts.append(box((11.8, 0.18, 0.24), (0, y, 0.55)))           # stretchers
    for x in (-5.9, 5.9):
        parts.append(box((0.2, 1.9, 0.24), (x, 0, 0.55)))             # end rails
        parts.append(box((0.24, 2.2, 0.2), (x, 0, TOP - T - 0.1)))    # end aprons under the top
    return coll, {"Bench": join(parts, "Bench", coll)}


def build_tray():
    coll = fresh_collection("SortTray")
    W, D, H, F = 3.1, 2.3, 0.2, 0.08  # width, depth, rim height over the floor's top, floor thickness
    straw = [box((W - 0.16, D - 0.16, F), (0, 0, TRAY - F / 2))]
    for s in (-1, 1):
        straw.append(box((W, 0.08, F + H), (0, s * (D / 2 - 0.04), TRAY - F + (F + H) / 2)))
        straw.append(box((0.08, D - 0.16, F + H), (s * (W / 2 - 0.04), 0, TRAY - F + (F + H) / 2)))
    weave = []
    for k in range(5):  # strips across the floor, 0.02 proud
        x = -1.1 + k * 0.55
        weave.append(box((0.12, D - 0.2, 0.02), (x, 0, TRAY + 0.01)))
    for s in (-1, 1):  # a band round the rim, 0.02 proud of each side
        weave.append(box((W + 0.04, 0.02, 0.06), (0, s * (D / 2 + 0.01), TRAY + H * 0.5)))
        weave.append(box((0.02, D, 0.06), (s * (W / 2 + 0.01), 0, TRAY + H * 0.5)))
    return coll, {"Straw": join(straw, "Straw", coll), "Weave": join(weave, "Weave", coll)}


BUILT = {}
for label, fn in (("SortBench", build_bench), ("SortTray", build_tray)):
    coll, ps = fn()
    BUILT[label] = ps
    tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in ps.values())
    print(label, {n: [round(c, 3) for c in (sum((o.matrix_world @ Vector(b) for b in o.bound_box), Vector()) / 8)] for n, o in ps.items()}, "tris", tris)

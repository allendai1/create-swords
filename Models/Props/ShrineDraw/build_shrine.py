# Shrine draw - the ore roller told as a wayside shrine (2026-11-07; Allen: "is there a better way to it make sense to
# the setting of our game", then "do the shrine draw and let me compare"). In place of the ore lever: a small hokora on
# a stone plinth with a vermilion bell frame in front; pulling the bell rope (the old lever's hold) rings the bell and the
# ores land on the sanbo offering stands (Models/Props/OreRollerV3). Low poly, flat shaded, the festival props' helpers.
#   ShrineDraw - the fixed shrine, origin on the floor at the plinth's centre, front -Y (Roblox -Z; turned in Studio to
#                face the path): Stone (plinth, step), Wood (legs, deck, body, ridge cap), Roof (gable), Vermilion (two
#                front posts, the crossbeam, its cap), Lattice (the doors' dark grid), Rope (a short shimenawa on the
#                crossbeam), Paper (its shide). 3.2 wide, 3.6 deep, 4.6 tall.
#   ShrineBell - what swings, built hanging from the pivot at the origin (the crossbeam's underside): Bell (a bronze
#                suzu with a slit), RopeRed and RopeWhite (a thick twisted rope in alternating segments), Tassel.
#                In Studio welded to OreRoller.Lever.ArmPivot, as the lever's arm was.
# Run in Blender (MCP execute_blender_code: exec(open(<this file>).read())).
import math

import bmesh
import bpy
from mathutils import Vector

FESTIVAL = "C:/Users/Allen/Documents/Create Swords!/Models/Props/Festival/build_festival.py"
_src = open(FESTIVAL).read()
exec(_src[:_src.index("def export(name):")])
HERE = "C:/Users/Allen/Documents/Create Swords!/Models/Props/ShrineDraw"
SOFT = True  # the stations' soft bevels (2026-11-07, Allen: "it doesnt have the bevelled edges style in the models")
if SOFT:
    exec(open("C:/Users/Allen/Documents/Create Swords!/Models/Props/soft_bevel.py").read())

PIVOT_Z = 3.95   # the crossbeam's underside, where the bell hangs
FRONT_Y = -1.2   # the bell frame's posts


def build_shrine():
    coll = fresh_collection("ShrineDraw")
    parts = {}
    parts["Stone"] = join([box((3.2, 3.6, 0.3), (0, 0, 0.15)),
                           box((1.4, 0.4, 0.16), (0, -1.95, 0.08))], "Stone", coll)  # plinth, front step
    wood = []
    for x in (-0.85, 0.85):
        for y in (-0.05, 1.25):
            wood.append(box((0.18, 0.18, 0.5), (x, y, 0.55)))  # legs
    wood.append(box((2.2, 1.7, 0.14), (0, 0.6, 0.87)))           # deck
    wood.append(box((1.9, 1.4, 1.5), (0, 0.65, 1.69)))           # body
    wood.append(box((0.22, 0.2, 1.5), (-0.86, -0.08, 1.69)))     # door posts, 0.04 proud of the body's front
    wood.append(box((0.22, 0.2, 1.5), (0.86, -0.08, 1.69)))
    parts["Wood"] = join(wood, "Wood", coll)
    parts["Lattice"] = join([box((0.06, 0.04, 1.3), (x, -0.07, 1.69)) for x in (-0.45, -0.15, 0.15, 0.45)] +
                            [box((1.5, 0.04, 0.06), (0, -0.07, z)) for z in (1.25, 1.69, 2.13)], "Lattice", coll)
    parts["Roof"] = join(gable(2.7, 1.25, 3.25, math.radians(35), 9, thick=0.16), "Roof", coll)
    parts["Roof"].location.y += 0.6  # over the body (join keeps the first box's origin: add, don't set)
    bpy.ops.object.select_all(action="DESELECT"); parts["Roof"].select_set(True)
    bpy.context.view_layer.objects.active = parts["Roof"]
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
    ver = []
    for x in (-1.35, 1.35):
        ver.append(box((0.22, 0.22, PIVOT_Z + 0.3), (x, FRONT_Y, (PIVOT_Z + 0.3) / 2)))  # front posts
    ver.append(box((3.1, 0.26, 0.26), (0, FRONT_Y, PIVOT_Z + 0.13)))                    # crossbeam (nuki)
    ver.append(box((3.6, 0.36, 0.16), (0, FRONT_Y, PIVOT_Z + 0.5)))                     # cap (kasagi)
    ver.append(box((0.16, 0.2, 0.22), (0, FRONT_Y, PIVOT_Z + 0.37)))                    # the strut between
    parts["Vermilion"] = join(ver, "Vermilion", coll)
    # a short shimenawa along the crossbeam's front and four shide under it
    def rope_at(t):
        return Vector((t * 1.15, FRONT_Y - 0.2, PIVOT_Z + 0.02 - 0.1 * (1 - t * t)))
    rope = []
    for k in range(6):
        t0, t1 = -1 + k / 3, -1 + (k + 1) / 3
        r0, r1 = 0.08 + 0.05 * (1 - abs(t0)), 0.08 + 0.05 * (1 - abs(t1))
        p0, p1 = rope_at(t0), rope_at(t1)
        d = p1 - p0
        o = cyl(r0, d.length, (p0 + p1) / 2, verts=6, r2=r1)
        o.rotation_mode = "QUATERNION"
        o.rotation_quaternion = d.normalized().to_track_quat("Z", "Y")
        rope.append(o)
    parts["Rope"] = join(rope, "Rope", coll)
    paper = []
    for x in (-0.95, 0.95):  # clear of the bell in the middle
        top = rope_at(x / 1.15).z - 0.1
        for k in range(3):
            paper.append(box((0.16, 0.03, 0.16), (x + (0.05 if k % 2 == 0 else -0.05), FRONT_Y - 0.3, top - 0.08 - k * 0.15)))
    parts["Paper"] = join(paper, "Paper", coll)
    return coll, parts


def build_bell():
    coll = fresh_collection("ShrineBell")
    parts = {}
    # the suzu: a slightly squashed ball on a short loop, with a slit round its lower half
    prof = [(0, -0.72), (0.18, -0.70), (0.3, -0.62), (0.36, -0.5), (0.36, -0.38), (0.3, -0.25), (0.18, -0.17), (0, -0.15)]
    bell = [lathe(prof, (0, 0, 0), verts=10), cyl(0.06, 0.16, (0, 0, -0.08), verts=6)]
    parts["Bell"] = join(bell, "Bell", coll)
    parts["Slit"] = join([box((0.5, 0.06, 0.04), (0, -0.33, -0.6)), box((0.04, 0.06, 0.16), (0, -0.33, -0.52))], "Slit", coll)
    # the rope: alternating red and white twisted segments from under the bell to hand height
    top, bottom, n = -0.72, -2.55, 8
    reds, whites = [], []
    for k in range(n):
        z0 = top - (top - bottom) * k / n
        z1 = top - (top - bottom) * (k + 1) / n
        o = cyl(0.11, (z0 - z1) + 0.01, (0, 0, (z0 + z1) / 2), verts=6, rot=(0, 0, math.radians(30 * k)))
        (reds if k % 2 == 0 else whites).append(o)
    parts["RopeRed"] = join(reds, "RopeRed", coll)
    parts["RopeWhite"] = join(whites, "RopeWhite", coll)
    parts["Tassel"] = join([cyl(0.15, 0.12, (0, 0, bottom - 0.06), verts=6),
                            cyl(0.18, 0.45, (0, 0, bottom - 0.12 - 0.225), verts=6, r2=0.22)], "Tassel", coll)
    return coll, parts


BUILT = {}
for label, fn in (("ShrineDraw", build_shrine), ("ShrineBell", build_bell)):
    coll, ps = fn()
    BUILT[label] = ps
    tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in ps.values())
    print(label, {n: [round(c, 3) for c in (sum((o.matrix_world @ Vector(b) for b in o.bound_box), Vector()) / 8)] for n, o in ps.items()}, "tris", tris)

# Delivery bay dressing, Sell Swords! 2026-11-08 (Allen: "the delivery area seems a bit empty with only a cart there ...
# so it looks like a delivery station", then "Top 3, i'll find a model for the ox"). Low poly, soft-bevelled
# (Models/Props/soft_bevel.py), one object per Studio material. Collections, each exported to its own FBX:
#   PackingBench - a long work table against the shop wall: top, four legs, a low shelf with straw on it, a straw heap,
#                  a rope coil and a rolled cloth bolt on the right of the top (the left half is where bundles lie).
#   WrapBundle   - one sword wrapped in cloth with two rope ties (the bench shows one per sword of a queued order).
#   StockCrate   - a plank crate with a dark frame (the stack by the plot wall grows with the cart's Capacity).
#   HitchPost    - a post on a foot block with an iron ring, where the ox is tied.
#   Trough       - a plank feed trough on two trestles, water inside.
#   HayBale      - a tied hay bale.
# Run in Blender (MCP execute_blender_code: exec(open(<this file>).read())). Writes <Name>.fbx next to this file.
# Units are studs, Z up, the front faces -Y (Roblox -Z), origin on the floor at the footprint's centre.
import math
import os
import sys

import bmesh
import bpy

FESTIVAL = "C:/Users/Allen/Documents/Create Swords!/Models/Props/Festival/build_festival.py"
_src = open(FESTIVAL).read()
exec(_src[:_src.index("def export(name):")])
HERE = "C:/Users/Allen/Documents/Create Swords!/Models/Props/DeliveryBay"
exec(open("C:/Users/Allen/Documents/Create Swords!/Models/Props/soft_bevel.py").read())

BENCH_L, BENCH_D, BENCH_H = 9.0, 2.6, 3.0


def build_bench():
    coll = fresh_collection("PackingBench")
    parts = {}
    wood = [box((BENCH_L, BENCH_D, 0.3), (0, 0, BENCH_H - 0.15))]  # top
    for sx in (-1, 1):
        for sy in (-1, 1):
            wood.append(box((0.4, 0.4, BENCH_H - 0.3), (sx * (BENCH_L / 2 - 0.45), sy * (BENCH_D / 2 - 0.35), (BENCH_H - 0.3) / 2)))
    wood.append(box((BENCH_L - 1.3, BENCH_D - 0.5, 0.2), (0, 0, 0.75)))  # low shelf between the legs
    wood.append(box((BENCH_L - 1.3, 0.25, 0.35), (0, BENCH_D / 2 - 0.35, BENCH_H - 0.45)))  # back apron
    parts["Wood"] = join(wood, "Wood", coll)
    straw = []
    for (x, y, r, sz) in ((-2.4, 0.1, 0.75, 0.55), (-0.9, -0.1, 0.7, 0.5), (0.8, 0.15, 0.8, 0.55), (2.5, -0.05, 0.7, 0.5)):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=r, location=(x, y, 0.85 + r * sz * 0.8))
        o = bpy.context.active_object
        o.scale = (1.3, 1.0, sz)
        straw.append(o)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.75, location=(2.9, 0.25, BENCH_H + 0.3))
    o = bpy.context.active_object
    o.scale = (1.2, 1.0, 0.5)
    straw.append(o)
    parts["Straw"] = join(straw, "Straw", coll)
    rope = []
    for k in range(3):  # a coil: three flat rings, each a little smaller
        bpy.ops.mesh.primitive_torus_add(major_radius=0.5 - 0.06 * k, minor_radius=0.08, major_segments=10, minor_segments=4,
                                         location=(1.2, -0.5, BENCH_H + 0.08 + 0.15 * k))
        rope.append(bpy.context.active_object)
    parts["Rope"] = join(rope, "Rope", coll)
    parts["Cloth"] = join([cyl(0.3, 2.2, (1.6, 0.55, BENCH_H + 0.3), rot=(0, math.pi / 2, 0), verts=8)], "Cloth", coll)
    return coll, parts


def build_bundle():
    coll = fresh_collection("WrapBundle")
    parts = {}
    # a katana-length bundle, flattened, the hilt end a little thicker
    parts["Cloth"] = join([cyl(0.28, 4.4, (0, 0, 0.22), rot=(0, math.pi / 2, 0), verts=6, r2=0.22)], "Cloth", coll)
    parts["Cloth"].scale = (1, 1, 0.75)
    bpy.ops.object.select_all(action="DESELECT")
    parts["Cloth"].select_set(True)
    bpy.context.view_layer.objects.active = parts["Cloth"]
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    ties = [cyl(0.31 - 0.02 * i, 0.12, (x, 0, 0.22), rot=(0, math.pi / 2, 0), verts=6) for i, x in enumerate((-1.2, 1.2))]
    for t in ties:
        t.scale = (1, 1, 0.78)
    parts["Tie"] = join(ties, "Tie", coll)
    return coll, parts


def build_crate(s=2.4):
    coll = fresh_collection("StockCrate")
    parts = {}
    planks = []
    gap = 0.06
    n = 3
    pw = (s - 0.3 - gap * (n - 1)) / n
    for face in range(4):  # side planks, horizontal
        a = face * math.pi / 2
        for k in range(n):
            z = 0.15 + pw / 2 + k * (pw + gap)
            cx, cy = math.sin(a) * (s / 2 - 0.08), -math.cos(a) * (s / 2 - 0.08)
            planks.append(_hard_box((s - 0.3, 0.14, pw), (cx, cy, z), rot=(0, 0, a)))  # planks stay hard: the frame carries the bevel
    for k in range(n):  # lid
        y = -s / 2 + 0.15 + pw / 2 + k * (pw + gap)
        planks.append(_hard_box((s - 0.3, pw, 0.14), (0, y, s - 0.15)))
    parts["Wood"] = join(planks, "Wood", coll)
    frame = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            frame.append(box((0.3, 0.3, s), (sx * (s / 2 - 0.15), sy * (s / 2 - 0.15), s / 2)))  # corner posts
    for z in (0.15, s - 0.15):
        for a in (0, math.pi / 2):
            for sgn in (-1, 1):
                cx, cy = (0, sgn * (s / 2 - 0.15)) if a == 0 else (sgn * (s / 2 - 0.15), 0)
                frame.append(box((s - 0.6, 0.26, 0.26), (cx, cy, z), rot=(0, 0, a)))
    parts["Frame"] = join(frame, "Frame", coll)
    return coll, parts


def build_post():
    coll = fresh_collection("HitchPost")
    parts = {}
    parts["Wood"] = join([box((0.9, 0.9, 0.35), (0, 0, 0.175)), box((0.5, 0.5, 4.2), (0, 0, 2.3)),
                          box((0.62, 0.62, 0.2), (0, 0, 4.45))], "Wood", coll)
    ring = []
    bpy.ops.mesh.primitive_torus_add(major_radius=0.32, minor_radius=0.06, major_segments=10, minor_segments=4,
                                     location=(0, -0.62, 3.3), rotation=(0, math.pi / 2, 0))
    ring.append(bpy.context.active_object)
    ring.append(box((0.14, 0.4, 0.14), (0, -0.35, 3.62)))  # the staple holding it
    parts["Iron"] = join(ring, "Iron", coll)
    return coll, parts


def build_trough(l=4.0, w=1.6, h=1.6):
    coll = fresh_collection("Trough")
    parts = {}
    wood = [box((l, w, 0.15), (0, 0, h - 0.95))]  # floor of the box
    for sy in (-1, 1):
        wood.append(box((l, 0.15, 0.95), (0, sy * (w / 2 - 0.075), h - 0.55)))
    for sx in (-1, 1):
        wood.append(box((0.15, w - 0.3, 0.95), (sx * (l / 2 - 0.075), 0, h - 0.55)))
        # a trestle: two splayed legs and a cross bar
        for sy in (-1, 1):
            wood.append(box((0.22, 0.22, h - 0.6), (sx * (l / 2 - 0.5), sy * (w / 2 - 0.15), (h - 0.6) / 2), rot=(sy * 0.15, 0, 0)))
        wood.append(box((0.2, w, 0.2), (sx * (l / 2 - 0.5), 0, 0.35)))
    parts["Wood"] = join(wood, "Wood", coll)
    parts["Water"] = join([box((l - 0.3, w - 0.3, 0.1), (0, 0, h - 0.35))], "Water", coll)
    return coll, parts


def build_hay(l=2.8, w=1.6, h=1.3):
    coll = fresh_collection("HayBale")
    parts = {}
    parts["Hay"] = join([box((l, w, h), (0, 0, h / 2))], "Hay", coll)
    parts["Tie"] = join([box((0.12, w + 0.04, h + 0.04), (x, 0, h / 2)) for x in (-l / 4, l / 4)], "Tie", coll)
    return coll, parts


def export(name):
    p = os.path.join(SKILLS, "blender-export-pipelines", "scripts")
    if p not in sys.path:
        sys.path.insert(0, p)
    import importlib
    exp = importlib.import_module("export_asset")
    return exp.run(preset="roblox", collection=name, out=os.path.join(HERE, name + ".fbx"), batch=False, no_anim=True)


BUILT = {}
for name, fn in (("PackingBench", build_bench), ("WrapBundle", build_bundle), ("StockCrate", build_crate),
                 ("HitchPost", build_post), ("Trough", build_trough), ("HayBale", build_hay)):
    coll, ps = fn()
    for o in ps.values():  # join leaves the origin on the first piece: put every part's origin on the prop's origin
        bpy.ops.object.select_all(action="DESELECT")
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    BUILT[name] = coll
    print(name, {n: len(o.data.polygons) for n, o in ps.items()},
          "tris", sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in ps.values()))


# --- Packing prototype props (2026-11-08, Allen: "brainstorm other manual steps ... boxing up something", then "all of
# them"). Run after the code above (it is the same file; BUILT gains these four).
#   SwordCrate - a long open crate for swords: inner 5.0 x 1.5 x 0.55 (a 10 x 3 grid of 0.5 cells), walls 0.2, a straw
#                lining on the floor (Straw), dark corner posts (Frame); origin on the floor at its centre.
#   CrateLid   - its lid: three planks and two battens, 5.4 x 1.9 x 0.16.
#   Nail       - one iron nail, head up, 0.5 long (its point at the origin, head at +Z).
#   Hanko      - a seal stamp: a turned wooden handle on a red stone base (Ink), base face at the origin.
CRATE_IN = (5.0, 1.5, 0.55)
WALL = 0.2


def build_sword_crate():
    coll = fresh_collection("SwordCrate")
    parts = {}
    ix, iy, iz = CRATE_IN
    ox, oy = ix + 2 * WALL, iy + 2 * WALL
    wood = [_hard_box((ox, oy, 0.15), (0, 0, 0.075))]  # floor
    for s in (-1, 1):
        wood.append(_hard_box((ox, WALL, iz + 0.15), (0, s * (iy / 2 + WALL / 2), (iz + 0.15) / 2)))
        wood.append(_hard_box((WALL, iy, iz + 0.15), (s * (ix / 2 + WALL / 2), 0, (iz + 0.15) / 2)))
    parts["Wood"] = join(wood, "Wood", coll)
    frame = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            frame.append(box((0.26, 0.26, iz + 0.2), (sx * (ox / 2 - 0.1), sy * (oy / 2 - 0.1), (iz + 0.2) / 2)))
    parts["Frame"] = join(frame, "Frame", coll)
    parts["Straw"] = join([_hard_box((ix - 0.02, iy - 0.02, 0.06), (0, 0, 0.15 + 0.03))], "Straw", coll)
    return coll, parts


def build_lid():
    coll = fresh_collection("CrateLid")
    parts = {}
    ix, iy, _ = CRATE_IN
    ox, oy = ix + 2 * WALL, iy + 2 * WALL
    pw = (oy - 0.08) / 3
    planks = [_hard_box((ox, pw - 0.02, 0.1), (0, -oy / 2 + pw / 2 + 0.04 + k * pw, 0.05)) for k in range(3)]
    parts["Wood"] = join(planks, "Wood", coll)
    parts["Frame"] = join([box((0.3, oy, 0.08), (x, 0, 0.13)) for x in (-ox / 2 + 0.45, ox / 2 - 0.45)], "Frame", coll)
    return coll, parts


def build_nail():
    coll = fresh_collection("Nail")
    parts = {}
    parts["Iron"] = join([_hard_cyl(0.03, 0.45, (0, 0, 0.225), verts=6), _hard_cyl(0.08, 0.05, (0, 0, 0.475), verts=8)], "Iron", coll)
    return coll, parts


def build_hanko():
    coll = fresh_collection("Hanko")
    parts = {}
    parts["Ink"] = join([cyl(0.32, 0.22, (0, 0, 0.11), verts=12)], "Ink", coll)
    parts["Wood"] = join([_hard_lathe([(0.0, 0.22), (0.22, 0.22), (0.16, 0.5), (0.13, 0.9), (0.2, 1.05), (0.16, 1.2), (0.0, 1.22)], (0, 0, 0), verts=10)], "Wood", coll)
    return coll, parts


for name, fn in (("SwordCrate", build_sword_crate), ("CrateLid", build_lid), ("Nail", build_nail), ("Hanko", build_hanko)):
    coll, ps = fn()
    for o in ps.values():
        bpy.ops.object.select_all(action="DESELECT")
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    BUILT[name] = coll
    print(name, {n: len(o.data.polygons) for n, o in ps.items()},
          "tris", sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in ps.values()))

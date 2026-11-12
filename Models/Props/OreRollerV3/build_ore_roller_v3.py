# Ore stand and ore lever, village style (2026-11-07; Allen, after the Ore Chances notice board: "it feels like the ore
# roller + the platforms dont really fit", then "yes build them out and do a side by side so i can compare").
# Low poly, flat shaded, the festival props' helpers. Three collections, each exported to its own FBX:
#   OreStandV3 - a sanbo (shrine offering stand): a hinoki tray with a rim on a narrower box base with a dark arched
#                "eye" on each side, lips top and bottom. Same 3.25 footprint as the old stand; the tray floor (where
#                the ore lies) 2.6 over the floor. Wood (tray floor, base), Trim (rim, lips), Eye (the four arches).
#   OreLeverV3 - the lever's fixed body: a stone plinth (2.6 x 3.5, the old Base's footprint), two wooden cheeks with
#                chamfered tops either side of the arm's slot, iron straps round them, an iron hinge pin with bolt heads
#                at the old hinge height (2.015 over the floor). Stone, Wood, Iron.
#   LeverArmV3 - the moving arm, built upright from the hinge at the origin (+Z): an iron shaft, a brass ferrule, a
#                chunky grip wrapped in cord crossings (a katana handle's tsuka-ito; vermilion with black cord in
#                Studio), a brass cap. Iron, Grip,
#                Wrap, Brass. In Studio these are welded to OreRoller.Lever.ArmPivot like the old Arm and Knob.
#
# Run in Blender (MCP execute_blender_code: exec(open(<this file>).read())). Units are studs, Z up, the front faces -Y
# (Roblox -Z), origin on the floor at the centre (the arm: at the hinge). One object per Studio material.
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


def prism_x(points, x0, x1):
    """A solid from a closed (y, z) outline, extruded along X from x0 to x1."""
    bm = bmesh.new()
    a = [bm.verts.new((x0, y, z)) for y, z in points]
    b = [bm.verts.new((x1, y, z)) for y, z in points]
    n = len(points)
    bm.faces.new(a[::-1])
    bm.faces.new(b)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((a[i], a[j], b[j], b[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new("prism")
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new("prism", me)
    bpy.context.scene.collection.objects.link(o)
    return soften(o) if SOFT else o


def arch(width, height, steps=6):
    """A flat-bottomed arch outline (u, v) from the bottom centre: straight sides, a half-ellipse top."""
    r = width / 2
    side = height - r * 0.9
    pts = [(-r, 0), (r, 0), (r, side)]
    for k in range(1, steps):
        a = math.pi * k / steps
        pts.append((r * math.cos(a), side + r * 0.9 * math.sin(a)))
    pts.append((-r, side))
    return pts


def build_stand():
    coll = fresh_collection("OreStandV3")
    parts = {}
    T, FLOOR = 3.25, 2.6           # tray width, tray floor (top of the floor slab) over the floor
    B = 2.3                        # base box width
    parts["Wood"] = join([box((T - 0.24, T - 0.24, 0.16), (0, 0, FLOOR - 0.08)),      # tray floor, inside the rim
                          box((B, B, FLOOR - 0.16 - 0.32), (0, 0, 0.16 + (FLOOR - 0.48) / 2))],  # base box
                         "Wood", coll)
    trim = []
    RIM_TOP, RIM_BOT = FLOOR + 0.22, FLOOR - 0.2
    for s in (-1, 1):
        trim.append(box((T, 0.12, RIM_TOP - RIM_BOT), (0, s * (T / 2 - 0.06), (RIM_TOP + RIM_BOT) / 2)))
        trim.append(box((0.12, T - 0.24, RIM_TOP - RIM_BOT), (s * (T / 2 - 0.06), 0, (RIM_TOP + RIM_BOT) / 2)))
    trim.append(box((B + 0.3, B + 0.3, 0.16), (0, 0, 0.08)))                  # foot lip
    trim.append(box((B + 0.2, B + 0.2, 0.12), (0, 0, FLOOR - 0.16 - 0.06 - 0.1)))  # top lip under the tray
    parts["Trim"] = join(trim, "Trim", coll)
    eyes = []
    pts = arch(1.25, 1.35)
    for k in range(4):  # one per side, 0.04 proud of the base's face
        o = prism_x([(u, v + 0.42) for u, v in pts], -0.02, 0.02)
        o.location = (0, 0, 0)
        # stand the outline on the face: X extrusion is the face normal; rotate to each side
        o.rotation_euler = (0, 0, math.pi / 2 * k)
        o.location = (B / 2 * math.cos(math.pi / 2 * k), B / 2 * math.sin(math.pi / 2 * k), 0)
        eyes.append(o)
    # prism_x put u along Y and v along Z with X as the normal; shift each 0.02 outward so it is 0.04 proud, never coplanar
    for k, o in enumerate(eyes):
        d = Vector((math.cos(math.pi / 2 * k), math.sin(math.pi / 2 * k), 0))
        o.location = o.location + d * 0.02
    parts["Eye"] = join(eyes, "Eye", coll)
    return coll, parts


HINGE = 2.015  # the old ArmPivot's height over the floor


def build_lever_body():
    coll = fresh_collection("OreLeverV3")
    parts = {}
    parts["Stone"] = join([box((2.6, 3.5, 0.24), (0, 0, 0.12)), box((2.4, 3.3, 0.08), (0, 0, 0.28))], "Stone", coll)
    L, top = 2.8, HINGE + 0.55
    outline = [(-L / 2, 0.32), (L / 2, 0.32), (L / 2, top - 0.6), (L / 2 - 0.6, top), (-L / 2 + 0.6, top), (-L / 2, top - 0.6)]
    cheeks = [prism_x(outline, x0, x1) for x0, x1 in ((-0.92, -0.22), (0.22, 0.92))]
    parts["Wood"] = join(cheeks, "Wood", coll)
    iron = []
    for y in (-0.85, 0.85):  # straps round each cheek, 0.04 proud on every side
        for xc in (-0.57, 0.57):
            iron.append(box((0.78, 0.14, top - 0.6 - 0.32 + 0.04), (xc, y, 0.32 + (top - 0.6 - 0.32) / 2 + 0.02)))
    iron.append(cyl(0.16, 2.1, (0, 0, HINGE), rot=(0, math.pi / 2, 0), verts=8))      # hinge pin across both cheeks
    for x in (-1.05, 1.05):
        iron.append(cyl(0.26, 0.1, (x, 0, HINGE), rot=(0, math.pi / 2, 0), verts=6))   # bolt heads
    parts["Iron"] = join(iron, "Iron", coll)
    return coll, parts


def build_arm():
    coll = fresh_collection("LeverArmV3")
    parts = {}
    G0, G1, GW = 1.45, 2.55, 0.46  # the grip, along the arm from the hinge, and its width (chunky: it reads from the path)
    parts["Iron"] = join([box((0.28, 0.28, G0 + 0.1), (0, 0, (G0 - 0.1) / 2)),
                          cyl(0.24, 0.36, (0, 0, 0), rot=(0, math.pi / 2, 0), verts=8)],  # the eye round the pin
                         "Iron", coll)
    parts["Grip"] = join([box((GW, GW, G1 - G0), (0, 0, (G0 + G1) / 2))], "Grip", coll)
    wraps = []
    n = 4
    step = (G1 - G0) / n
    for k in range(n):
        zc = G0 + step * (k + 0.5)
        for face in range(4):
            a = math.pi / 2 * face
            nx, ny = math.cos(a), math.sin(a)
            for s in (-1, 1):  # a cord crossing on each face, 0.03 proud
                o = box((GW, 0.03, 0.1), (nx * (GW / 2 + 0.015), ny * (GW / 2 + 0.015), zc))
                o.rotation_mode = "XYZ"
                o.rotation_euler = (s * math.radians(40), 0, a + math.pi / 2)
                wraps.append(o)
    parts["Wrap"] = join(wraps, "Wrap", coll)
    parts["Brass"] = join([box((GW - 0.04, GW - 0.04, 0.12), (0, 0, G0 - 0.06)),
                           box((GW + 0.1, GW + 0.1, 0.18), (0, 0, G1 + 0.09)),
                           box((GW - 0.1, GW - 0.1, 0.08), (0, 0, G1 + 0.22))], "Brass", coll)
    return coll, parts


BUILT = {}
for label, fn in (("OreStandV3", build_stand), ("OreLeverV3", build_lever_body), ("LeverArmV3", build_arm)):
    coll, ps = fn()
    BUILT[label] = ps
    tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in ps.values())
    print(label, {n: [round(c, 3) for c in (sum((o.matrix_world @ Vector(b) for b in o.bound_box), Vector()) / 8)] for n, o in ps.items()}, "tris", tris)

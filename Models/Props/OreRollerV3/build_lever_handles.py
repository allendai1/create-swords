# Four handle options for the village ore lever (2026-11-07; Allen on the vermilion cord-wrapped grip: "i dont like the
# handle design", then "build them all so i can compare"). Each is a whole arm built upright from the hinge at the
# origin (+Z), like LeverArmV3, so it welds to OreRoller.Lever.ArmPivot the same way. One collection, one FBX; every
# object is prefixed with its option so Studio picks one set (Builders.restyle_ore_roller handle(lever, letter)).
#   A - red ball knob (the old lever's cue): iron shaft, brass collar, a red ball. HdlA_Iron, HdlA_Brass, HdlA_Knob
#   B - turned wooden grip: iron shaft, brass ferrule, a lathe-turned light wood grip, a dark wood cap.
#       HdlB_Iron, HdlB_Brass, HdlB_Grip, HdlB_Cap
#   C - wooden T-bar: iron shaft and hub, a light wood crossbar with brass end caps. HdlC_Iron, HdlC_Bar, HdlC_Brass
#   D - rope-bound wooden haft: one wooden haft from the hinge, an iron eye and band, straw rope rings at the grip.
#       HdlD_Haft, HdlD_Iron, HdlD_Rope
# Soft-bevelled (Models/Props/soft_bevel.py). Run in Blender: exec(open(<this file>).read()). Writes LeverHandles.fbx.
import math

import bmesh
import bpy
from mathutils import Vector

FESTIVAL = "C:/Users/Allen/Documents/Create Swords!/Models/Props/Festival/build_festival.py"
_src = open(FESTIVAL).read()
exec(_src[:_src.index("def export(name):")])
HERE = "C:/Users/Allen/Documents/Create Swords!/Models/Props/OreRollerV3"
exec(open("C:/Users/Allen/Documents/Create Swords!/Models/Props/soft_bevel.py").read())


def eye():
    """The iron eye round the hinge pin (along X)."""
    return cyl(0.24, 0.36, (0, 0, 0), rot=(0, math.pi / 2, 0), verts=12)


def build():
    coll = fresh_collection("LeverHandles")
    parts = {}
    # A: red ball knob
    parts["HdlA_Iron"] = join([box((0.28, 0.28, 2.0), (0, 0, 0.95)), eye()], "HdlA_Iron", coll)
    parts["HdlA_Brass"] = join([cyl(0.22, 0.12, (0, 0, 1.92), verts=12)], "HdlA_Brass", coll)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=10, radius=0.46, location=(0, 0, 2.38))
    parts["HdlA_Knob"] = join([bpy.context.active_object], "HdlA_Knob", coll)
    # B: turned wooden grip
    parts["HdlB_Iron"] = join([box((0.28, 0.28, 1.5), (0, 0, 0.7)), eye()], "HdlB_Iron", coll)
    parts["HdlB_Brass"] = join([cyl(0.21, 0.14, (0, 0, 1.49), verts=12)], "HdlB_Brass", coll)
    parts["HdlB_Grip"] = join([lathe([(0, 1.56), (0.18, 1.56), (0.22, 1.75), (0.25, 2.0), (0.23, 2.25), (0.19, 2.44), (0, 2.44)],
                                     (0, 0, 0), verts=12)], "HdlB_Grip", coll)
    parts["HdlB_Cap"] = join([lathe([(0, 2.42), (0.23, 2.42), (0.28, 2.5), (0.24, 2.6), (0, 2.63)], (0, 0, 0), verts=12)],
                             "HdlB_Cap", coll)
    # C: wooden T-bar
    parts["HdlC_Iron"] = join([box((0.28, 0.28, 2.25), (0, 0, 1.075)), eye(), box((0.4, 0.4, 0.4), (0, 0, 2.32))], "HdlC_Iron", coll)
    parts["HdlC_Bar"] = join([cyl(0.18, 1.5, (0, 0, 2.32), rot=(0, math.pi / 2, 0), verts=12)], "HdlC_Bar", coll)
    parts["HdlC_Brass"] = join([cyl(0.21, 0.08, (x, 0, 2.32), rot=(0, math.pi / 2, 0), verts=12) for x in (-0.79, 0.79)],
                               "HdlC_Brass", coll)
    # D: rope-bound wooden haft
    parts["HdlD_Haft"] = join([box((0.3, 0.3, 2.75), (0, 0, 1.2))], "HdlD_Haft", coll)
    parts["HdlD_Iron"] = join([eye(), box((0.36, 0.36, 0.14), (0, 0, 0.35))], "HdlD_Iron", coll)  # eye and a band, proud of the haft
    parts["HdlD_Rope"] = join([cyl(0.2, 0.11, (0, 0, 1.8 + k * 0.12), verts=10, rot=(0, 0, math.radians(18 * k))) for k in range(6)],
                              "HdlD_Rope", coll)
    return coll, parts


coll, PARTS = build()
for n, o in PARTS.items():
    c = sum((o.matrix_world @ Vector(b) for b in o.bound_box), Vector()) / 8
    print(n, [round(v, 3) for v in c], "tris", sum(len(p.vertices) - 2 for p in o.data.polygons))

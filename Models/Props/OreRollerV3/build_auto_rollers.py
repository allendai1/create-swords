# Three village versions of the Auto Ore Roller (2026-11-07; Allen: "i feel like the auto roller doesn't look good",
# then "Build all three"). Same place and job as WorldStore.AutoRoller: beside the ore lever, the lever side +X here
# (Roblox -X in the part's own axes), a shaft at the old height (z 2.0) running to the lever, the Roblox ball lamp kept
# (placed in Studio at each LAMP point). One collection, one FBX; objects prefixed WW_ (water wheel), KD_ (karakuri
# doll), CW_ (clockwork weight); kinds after the underscore pick the Studio look.
#   WW - a stone basin with water, a spoked water wheel with paddles turning on the shaft between two wooden bearing
#        posts, a bamboo spout on a post pouring over its top, a lamp post at the front corner.
#   KD - a wooden box by the lever with a karakuri doll on it: red robe with a dark obi, cream face, black hair; its
#        right arm (KD_Arm) hangs from the shoulder and is turned in Studio to reach for the knob on a pull.
#   CW - a two-post frame with a top beam, a brass gear and a wooden rope drum on the shaft, a rope down to a hanging
#        stone weight, the lamp on the beam.
# Soft-bevelled (Models/Props/soft_bevel.py). Run in Blender: exec(open(<this file>).read()). Writes AutoRollers.fbx.
import math

import bmesh
import bpy
from mathutils import Vector

FESTIVAL = "C:/Users/Allen/Documents/Create Swords!/Models/Props/Festival/build_festival.py"
_src = open(FESTIVAL).read()
exec(_src[:_src.index("def export(name):")])
HERE = "C:/Users/Allen/Documents/Create Swords!/Models/Props/OreRollerV3"
exec(open("C:/Users/Allen/Documents/Create Swords!/Models/Props/soft_bevel.py").read())

AZ = 2.0                       # the shaft's height, as the old roller's
LAMP = {"WW": (0.9, -1.05, 2.75), "KD": (2.2, -0.05, 3.72), "CW": (-0.4, 0, 4.45)}  # where the ball lamp's centre goes
SHOULDER = (2.68, -0.05, 2.78)  # the doll's right shoulder: KD_Arm turns about Blender Y here


def shaft(x0, x1):
    return cyl(0.14, x1 - x0, ((x0 + x1) / 2, 0, AZ), rot=(0, math.pi / 2, 0), verts=10)


def ring_x(r, width, x, z, verts=12):
    return cyl(r, width, (x, 0, z), rot=(0, math.pi / 2, 0), verts=verts)


def build():
    coll = fresh_collection("AutoRollers")
    P = {}
    # --- WW: water wheel -----------------------------------------------------------------------------------------
    P["WW_Stone"] = join([box((3.2, 2.8, 0.24), (-0.2, 0, 0.12)),
                          box((1.3, 2.6, 0.5), (-0.6, 0, 0.49)) ], "WW_Stone", coll)            # plinth, basin walls
    P["WW_Water"] = join([box((1.1, 2.4, 0.06), (-0.6, 0, 0.72))], "WW_Water", coll)          # 0.02 under the basin top
    wood = []
    for x in (-1.15, -0.05):
        wood.append(box((0.26, 0.4, AZ + 0.1), (x, 0, 0.24 + (AZ - 0.24) / 2 + 0.05)))      # bearing posts
    wood.append(box((0.22, 0.22, 2.9), (-0.6, 1.25, 1.69)))                                 # spout post
    wood.append(box((0.22, 0.22, 2.5), (0.9, -1.05, 1.49)))                                 # lamp post
    wood.append(box((0.4, 0.4, 0.1), (0.9, -1.05, 2.79)))                                   # lamp seat
    P["WW_Wood"] = join(wood, "WW_Wood", coll)
    b0, b1 = Vector((-0.6, 1.25, 3.2)), Vector((-0.6, 0.15, 3.55))
    d = b1 - b0
    o = cyl(0.11, d.length, (b0 + b1) / 2, verts=8)
    o.rotation_mode = "QUATERNION"
    o.rotation_quaternion = d.normalized().to_track_quat("Z", "Y")
    P["WW_Bamboo"] = join([o], "WW_Bamboo", coll)
    R, rim, wx = 1.3, 0.16, -0.6
    wheel = []
    for side in (-0.2, 0.2):
        for k in range(12):  # twelve-sided rims
            a = 2 * math.pi * (k + 0.5) / 12
            rr = R - rim / 2
            wheel.append(box((0.08, 2 * R * math.tan(math.pi / 12) + 0.02, rim), (wx + side, rr * math.cos(a), AZ + rr * math.sin(a)), rot=(a - math.pi / 2, 0, 0)))
    for k in range(12):  # paddles across both rims
        a = 2 * math.pi * k / 12
        wheel.append(box((0.5, 0.06, 0.36), (wx, (R - 0.05) * math.cos(a), AZ + (R - 0.05) * math.sin(a)), rot=(a, 0, 0)))
    for k in range(4):  # spokes
        a = math.pi / 4 * k
        wheel.append(box((0.08, 2 * R - 0.2, 0.1), (wx - 0.2, 0, AZ), rot=(a, 0, 0)))
        wheel.append(box((0.08, 2 * R - 0.2, 0.1), (wx + 0.2, 0, AZ), rot=(a, 0, 0)))
    P["WW_Wheel"] = join(wheel, "WW_Wheel", coll)
    P["WW_Hub"] = join([ring_x(0.26, 0.56, wx, AZ)], "WW_Hub", coll)
    P["WW_Axle"] = join([shaft(-1.35, 4.3)], "WW_Axle", coll)
    # --- KD: karakuri doll ---------------------------------------------------------------------------------------
    P["KD_Stone"] = join([box((1.9, 1.7, 0.24), (2.2, 0, 0.12))], "KD_Stone", coll)
    P["KD_Wood"] = join([box((1.5, 1.3, 1.0), (2.2, 0, 0.74)), box((1.6, 1.4, 0.1), (2.2, 0, 1.29))], "KD_Wood", coll)
    P["KD_Robe"] = join([lathe([(0, 1.34), (0.55, 1.34), (0.5, 1.9), (0.42, 2.5), (0.36, 2.86), (0, 2.9)], (2.2, -0.05, 0), verts=12)],
                        "KD_Robe", coll)
    P["KD_Obi"] = join([lathe([(0, 2.0), (0.5, 2.0), (0.48, 2.25), (0, 2.25)], (2.2, -0.05, 0), verts=12)], "KD_Obi", coll)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=14, ring_count=9, radius=0.34, location=(2.2, -0.05, 3.2))
    P["KD_Face"] = join([bpy.context.active_object], "KD_Face", coll)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=14, ring_count=9, radius=0.36, location=(2.2, 0.03, 3.28))
    hair = bpy.context.active_object
    hair.scale = (1.0, 0.9, 0.85)
    P["KD_Hair"] = join([hair, cyl(0.16, 0.2, (2.2, 0.05, 3.55), verts=10)], "KD_Hair", coll)   # with a topknot under the lamp
    # the arm hangs from the shoulder: sleeve then hand
    sx, sy, sz = SHOULDER
    P["KD_Arm"] = join([box((0.26, 0.3, 0.9), (sx, sy, sz - 0.45)),
                        cyl(0.12, 0.26, (sx, sy, sz - 1.0), verts=10)], "KD_Arm", coll)
    # --- CW: clockwork weight ------------------------------------------------------------------------------------
    P["CW_Stone"] = join([box((2.4, 2.0, 0.24), (-0.4, 0, 0.12))], "CW_Stone", coll)
    P["CW_Wood"] = join([box((0.26, 0.4, 4.0), (-1.3, 0, 2.24)), box((0.26, 0.4, 4.0), (0.5, 0, 2.24)),
                         box((2.3, 0.5, 0.26), (-0.4, 0, 4.25)), box((0.5, 0.5, 0.1), (-0.4, 0, 4.42))], "CW_Wood", coll)
    gear = [ring_x(0.75, 0.16, -0.75, AZ, verts=16)]
    for k in range(14):  # teeth
        a = 2 * math.pi * k / 14
        gear.append(box((0.16, 0.18, 0.24), (-0.75, 0.84 * math.cos(a), AZ + 0.84 * math.sin(a)), rot=(a - math.pi / 2, 0, 0)))
    P["CW_Gear"] = join(gear, "CW_Gear", coll)
    P["CW_Drum"] = join([ring_x(0.35, 0.5, -0.25, AZ, verts=12), ring_x(0.45, 0.06, -0.52, AZ), ring_x(0.45, 0.06, 0.02, AZ)], "CW_Drum", coll)
    P["CW_Axle"] = join([shaft(-1.45, 4.3)], "CW_Axle", coll)
    P["CW_Rope"] = join([box((0.06, 0.06, AZ - 1.05), (-0.25, -0.38, (AZ + 1.05) / 2))], "CW_Rope", coll)
    P["CW_Weight"] = join([box((0.6, 0.6, 0.6), (-0.25, -0.38, 0.75))], "CW_Weight", coll)
    return coll, P


coll, PARTS = build()
for n, o in PARTS.items():
    c = sum((o.matrix_world @ Vector(b) for b in o.bound_box), Vector()) / 8
    print(n, [round(v, 3) for v in c], sum(len(p.vertices) - 2 for p in o.data.polygons))

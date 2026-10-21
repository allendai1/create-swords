# Ore Roller stand v2 for Create Swords! (Allen 2026-10-20: "can you design a low poly ore roller stand").
# Follows Allen's Studio blockout (Smithy.OreRoller.Stand1): a spool with a brown base disc, a cream drum, a
# brown cap disc and the ingot-shaped Ore on top, 4.1 across and 2.25 to the top of the cap.
# Low-poly finish: octagonal and flat-shaded, with one-segment chamfers. The drum swells at the waist like a
# taiko drum, has two iron hoops studded with gold tacks, and the cap carries a lighter wooden seat for the ore.
#
# Run headless:  blender --background --python build_ore_stand_v2.py
# Writes, next to this script: OreStandV2.blend, OreStandV2.fbx (Roblox preset, no ore), review/*.png, qa.json.
# Units are studs, Z up, front faces -Y, origin on the floor under the centre.
import math
import os
import sys
import json
import bpy
import bmesh

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import build_stations as bs  # noqa: E402
from build_stations import at, box, cyl, frustum  # noqa: E402

bs.DETAIL = "low"
bs.PAL.update({
    "spool":    (0.36, 0.235, 0.157),  # Allen's blockout brown (92, 60, 40)
    "spool_lt": (0.55, 0.36, 0.22),
    "drum":     (0.925, 0.87, 0.77),   # Allen's blockout cream (236, 222, 196)
})

SIDES = 8
BASE = (0.0, 0.37, 2.05, 1.98)       # z0, z1, r bottom, r top
DRUM = ((0.33, 1.42), (1.15, 1.58), (1.97, 1.42))  # (z, r) rings, 0.04 into the base and cap
CAP = (1.93, 2.25, 1.98, 2.05)
SEAT = (2.23, 2.29, 1.5)             # the ore's bottom sits on 2.29, as in Studio
HOOPS = (0.60, 1.54)                 # bottoms of the two 0.16-tall hoops
HOOP_H, HOOP_R = 0.16, 1.55
APOTHEM = math.cos(math.pi / SIDES)


def drum(name, rings, color):
    """Octagonal loft through (z, r) rings, faces centred on the axes like bs.cyl, fan caps."""
    bm = bmesh.new()
    loops = [[bm.verts.new((r * math.cos(a), r * math.sin(a), z))
              for a in (2 * math.pi * i / SIDES + math.pi / SIDES for i in range(SIDES))] for z, r in rings]
    for lo, hi in zip(loops, loops[1:]):
        for i in range(SIDES):
            j = (i + 1) % SIDES
            bm.faces.new((lo[i], lo[j], hi[j], hi[i]))
    for loop, z, flip in ((loops[0], rings[0][0], True), (loops[-1], rings[-1][0], False)):
        c = bm.verts.new((0, 0, z))
        for i in range(SIDES):
            j = (i + 1) % SIDES
            bm.faces.new((loop[j], loop[i], c) if flip else (loop[i], loop[j], c))
    return bs._finish(name, bm, color, at(0, 0, 0), (0, 0, 0), 0.03)


def build():
    root = bs.station("OreStandV2", 0, 0)
    z0, z1, rb, rt = BASE
    cyl("Base", rb, z1 - z0, at(0, 0, z0), "spool", sides=SIDES, r2=rt, bevel=0.05)
    drum("Drum", DRUM, "drum")
    for k, hz in enumerate(HOOPS):
        cyl(f"Hoop{k}", HOOP_R, HOOP_H, at(0, 0, hz), "iron", sides=SIDES, bevel=0.02)
        for i in range(SIDES):  # one tack on each face of the hoop
            a = 2 * math.pi * i / SIDES
            d = HOOP_R * APOTHEM - 0.02
            cyl(f"Tack{k}_{i}", 0.085, 0.08, at(d * math.cos(a), d * math.sin(a), hz + HOOP_H / 2), "gold",
                sides=6, rot=(-90, 0, math.degrees(a) - 90))
    z0, z1, rb, rt = CAP
    cyl("Cap", rb, z1 - z0, at(0, 0, z0), "spool", sides=SIDES, r2=rt, bevel=0.05)
    s0, s1, sr = SEAT
    cyl("Seat", sr, s1 - s0, at(0, 0, s0), "spool_lt", sides=SIDES)
    return root


def build_ore_preview():
    """Stand-in for Studio's Ore ingot (2.3 x 1.2 x 0.75), for the renders only."""
    bs.station("OrePreview", 0, 0)
    frustum("Ore", 2.3, 1.2, 1.85, 0.8, 0.75, at(0, 0, SEAT[1]), "ore", bevel=0.06)


def review():
    sc = bpy.context.scene
    os.makedirs(os.path.join(HERE, "review"), exist_ok=True)
    for eng in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        try:
            sc.render.engine = eng
            break
        except TypeError:
            pass
    sc.view_settings.view_transform = "Standard"
    w = sc.world or bpy.data.worlds.new("World")
    sc.world = w
    w.use_nodes = True
    bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs[0].default_value = bs.srgb2lin((0.82, 0.82, 0.84)) + (1,)
    bg.inputs[1].default_value = 0.9
    sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN"))
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(50), 0, math.radians(-35))
    sc.collection.objects.link(sun)
    me = bpy.data.meshes.new("Ground")
    me.from_pydata([(-30, -30, -0.002), (30, -30, -0.002), (30, 30, -0.002), (-30, 30, -0.002)], [], [(0, 1, 2, 3)])
    g = bpy.data.objects.new("Ground", me)
    gm = bpy.data.materials.new("Review_Ground")
    gm.use_nodes = True
    b = next(n for n in gm.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = bs.srgb2lin((0.78, 0.78, 0.80)) + (1,)
    b.inputs["Roughness"].default_value = 1.0
    me.materials.append(gm)
    sc.collection.objects.link(g)
    bs.avatar(3.6, 0.4, yaw=-90)  # 5.2-stud player beside it, for scale
    bpy.data.collections["Avatar"].hide_render = True
    cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = 1100, 1000
    from mathutils import Vector
    shots = {"front": ((0, -1, 0.2), 9.5, (0, 0, 1.4), False),
             "three_quarter": ((0.7, -1, 0.45), 10, (0, 0, 1.4), False),
             "top": ((0.15, -0.4, 1), 10, (0, 0, 1.4), False),
             "scale": ((0.35, -1, 0.3), 15, (1.6, 0, 2.2), True)}
    out = []
    for name, (d, dist, target, with_avatar) in shots.items():
        bpy.data.collections["Avatar"].hide_render = not with_avatar
        cam.data.lens = 50
        t = Vector(target)
        cam.location = t + Vector(d).normalized() * dist
        cam.rotation_euler = (t - cam.location).to_track_quat("-Z", "Y").to_euler()
        sc.render.filepath = os.path.join(HERE, "review", f"ore_stand_v2_{name}.png")
        bpy.ops.render.render(write_still=True)
        out.append(sc.render.filepath)
    for ob in (sun, g, cam):
        bpy.data.objects.remove(ob)
    for o in list(bpy.data.collections["Avatar"].objects):
        bpy.data.objects.remove(o)
    bpy.data.collections.remove(bpy.data.collections["Avatar"])
    return out


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    build()
    build_ore_preview()
    hits = bs.zfight_check()
    report = bs.qa(names=("OreStandV2",))
    tris = sum(len(p.vertices) - 2 for o in bpy.data.collections["OreStandV2"].objects if o.type == "MESH"
               for p in o.data.polygons)
    shots = review()
    bs.export_fbx(HERE, names=("OreStandV2",))
    with open(os.path.join(HERE, "qa.json"), "w") as f:
        json.dump({"tris": tris, "zfight_pairs": len(hits), "qa": report}, f, indent=1, default=str)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, "OreStandV2.blend"))
    print("ORESTAND tris", tris, "zfight", len(hits), "shots", shots)


main()

# Mine shaft for Create Swords! (Allen 2026-10-20): replaces the Ore Roller's pedestals, lore-wise. The lever
# works a winch, a bucket comes up the shaft, and the ore lands in mine carts parked on a rail track. Each cart is
# what a stand is today (a model with an `Ore` part the roll recolours), so more carts = more stands.
#
# Run headless:  blender --background --python build_mine_shaft.py
# Writes, next to this script: MineShaft.blend, review/*.png, qa.json. Layout sketch only, not exported yet.
# Units are studs, Z up, front faces -Y, origin on the floor. Low poly: flat-shaded, one-segment chamfers.
#
# Layout (plan, studs):
#   shaft centre (0, 2): stone curb 7 x 7, 1.2 high, timber-lined 4.2 opening with a black void
#   headframe: two A-frames at x +-2.8 to 8.5 high, a crossbeam with a sheave wheel, a small gabled roof
#   winch (x 6.5): drum on two trestles; rope from the sheave; the brake lever (x 8.6, y 0) is the roll lever
#   track along x at y -4.5, carts at x -5 / 0 / 5 (Cart1 to start, Cart2 and Cart3 from pads)
import math
import os
import sys
import json
import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import build_stations as bs  # noqa: E402
from build_stations import at, box, cyl, frustum, ring  # noqa: E402

bs.DETAIL = "low"
bs.PAL.update({
    "spool":  (0.36, 0.235, 0.157),
    "timber": (0.62, 0.42, 0.26),
    "tile":   (0.30, 0.33, 0.42),
    "void":   (0.02, 0.02, 0.03),
    "dirt":   (0.55, 0.47, 0.38),
    "rope":   (0.80, 0.70, 0.50),
})

SHAFT = Vector((0, 2))
CURB_H = 1.2
TRACK_Y, GAUGE = -4.5, 1.6
CARTS = (-5.0, 0.0, 5.0)
FRAME_X, APEX_Z = 2.8, 8.5
WHEEL = dict(c=Vector((0.9, 2, 7.1)), r=0.9)
DRUM = dict(x=6.5, z=1.9, r=0.7, len=2.4)


def beam(name, p0, p1, t, color, bevel=0.03):
    """Square timber from p0 to p1 (box along its local Z)."""
    p0, p1 = Vector(p0), Vector(p1)
    e = (p1 - p0).to_track_quat("Z", "Y").to_euler()
    return box(name, t, t, (p1 - p0).length, p0, color, rot=tuple(math.degrees(a) for a in e), bevel=bevel)


def shaft():
    bs.station("MineShaft", 0, 0)
    sx, sy = SHAFT
    box("Yard", 22, 16, 0.04, at(0, -1.5, -0.02), "dirt")
    # stone curb: front/back full width, sides between them, alternating tones
    for k, s in enumerate((-1, 1)):
        box(f"CurbFB{k}", 7, 1.4, CURB_H, at(sx, sy + s * 2.8, 0), "stone" if k else "stone_dk", bevel=0.08)
        box(f"CurbSide{k}", 1.4, 4.2, CURB_H, at(sx + s * 2.8, sy, 0), "stone_dk" if k else "stone", bevel=0.08)
    ring("Lining", 4.2, 4.2, 0.25, CURB_H + 0.04, at(sx, sy, 0), "spool")
    box("Void", 3.7, 3.7, 0.04, at(sx, sy, 0.04), "void")
    # headframe: an A-frame on each side, standing on the curb
    for k, s in enumerate((-1, 1)):
        x = s * FRAME_X
        apex = (x, sy, APEX_Z)
        for j, t in enumerate((-1, 1)):
            beam(f"Leg{k}{j}", (x, sy + t * 2.3, CURB_H - 0.05), apex, 0.45 - 0.04 * j, "timber")  # unequal: no shared side planes
        beam(f"Tie{k}", (x, sy - 1.25, 4.6), (x, sy + 1.25, 4.6), 0.35, "spool")
    beam("CrossBeam", (-FRAME_X - 0.5, sy, APEX_Z - 0.2), (FRAME_X + 0.5, sy, APEX_Z - 0.2), 0.5, "spool")
    # sheave wheel under the beam, hung from two blocks
    c, r = WHEEL["c"], WHEEL["r"]
    cyl("Wheel", r, 0.22, at(c.x, c.y - 0.11, c.z), "iron", sides=10, rot=(-90, 0, 0), bevel=0.03)
    cyl("WheelHub", 0.22, 0.5, at(c.x, c.y - 0.25, c.z), "iron_dk", sides=6, rot=(-90, 0, 0))
    for j, t in enumerate((-1, 1)):
        box(f"Hanger{j}", 0.25, 0.14, APEX_Z - 0.25 - c.z + 0.2, at(c.x, c.y + t * 0.32, c.z - 0.2), "iron_dk")
    # gabled roof over the beam
    for j, t in enumerate((-1, 1)):
        box(f"Roof{j}", 7.6 - 0.1 * j, 1.9, 0.2, at(0, sy + t * 0.82, APEX_Z - 0.29), "tile", rot=(-t * 28, 0, 0), bevel=0.04)
    box("Ridge", 7.8, 0.3, 0.25, at(0, sy, APEX_Z + 0.2), "iron_dk", bevel=0.04)
    # bucket coming up, hung from the wheel's left side
    bx = c.x - r
    frustum("Bucket", 1.1, 1.1, 1.4, 1.4, 1.2, at(bx, sy, 1.7), "timber", bevel=0.05)
    for z in (1.85, 2.6):
        f = (z - 1.7) / 1.2
        w = 1.1 + 0.3 * f + 0.06
        frustum(f"BucketBand{int(z * 10)}", w, w, w + 0.04, w + 0.04, 0.12, at(bx, sy, z), "iron_dk")
    beam("Bail", (bx - 0.72, sy, 2.85), (bx, sy, 3.5), 0.08, "iron_dk", bevel=0)
    beam("Bail2", (bx + 0.72, sy, 2.85), (bx, sy, 3.5), 0.07, "iron_dk", bevel=0)
    beam("RopeDown", (bx, sy, 3.45), (bx, sy, c.z), 0.1, "rope", bevel=0)
    # winch: drum on two trestles, rope from the top of the wheel to the top of the drum
    d = DRUM
    for j, t in enumerate((-1, 1)):
        y = sy + t * (d["len"] / 2 + 0.25)
        box(f"TrestleFoot{j}", 1.6, 0.5, 0.3, at(d["x"], y, 0), "spool", bevel=0.04)
        box(f"TrestlePost{j}", 0.45, 0.45, d["z"] + 0.35, at(d["x"], y, 0.28), "timber", bevel=0.03)
    cyl("Drum", d["r"], d["len"], at(d["x"], sy - d["len"] / 2, d["z"]), "timber", sides=8, rot=(-90, 0, 0), bevel=0.04)
    for j, t in enumerate((-1, 1)):
        cyl(f"DrumRim{j}", d["r"] + 0.12, 0.15, at(d["x"], sy + t * (d["len"] / 2 - 0.1) - 0.075, d["z"]), "iron_dk",
            sides=8, rot=(-90, 0, 0))
    cyl("Axle", 0.12, d["len"] + 1.4, at(d["x"], sy - d["len"] / 2 - 0.7, d["z"]), "iron_dk", sides=6, rot=(-90, 0, 0))
    cyl("RopeCoil", d["r"] + 0.06, 1.2, at(d["x"], sy - 0.6, d["z"]), "rope", sides=8, rot=(-90, 0, 0))
    beam("RopeOver", (c.x + r * 0.7, sy, c.z + r * 0.7), (d["x"] - 0.2, sy, d["z"] + d["r"] + 0.04), 0.1, "rope", bevel=0)
    # the roll lever: a brake lever on its own block, beside the winch
    bs.station("Lever", 8.6, -0.4)
    box("Base", 1.2, 1.0, 0.45, at(0, 0, 0), "spool", bevel=0.05)
    box("Bracket", 0.45, 0.4, 0.8, at(0, 0, 0.44), "iron", bevel=0.03)
    box("Arm", 0.2, 0.2, 2.2, at(0, 0, 1.0), "timber", rot=(-25, 0, 0), bevel=0.02)
    s, cz = math.sin(math.radians(25)), math.cos(math.radians(25))
    box("Knob", 0.36, 0.36, 0.45, at(0, 2.05 * s, 1.0 + 2.05 * cz), "red", rot=(-25, 0, 0), bevel=0.04)


def track():
    bs.station("Track", 0, 0)
    x0, x1 = CARTS[0] - 3.5, CARTS[-1] + 3.5
    n = int((x1 - x0) / 1.4) + 1
    for i in range(n):
        box(f"Sleeper{i}", 0.5, GAUGE + 1.0, 0.12, at(x0 + 0.25 + i * (x1 - x0 - 0.5) / (n - 1), TRACK_Y, 0), "spool")
    for j, t in enumerate((-1, 1)):
        box(f"Rail{j}", x1 - x0 + 0.2, 0.16, 0.16, at((x0 + x1) / 2, TRACK_Y + t * GAUGE / 2, 0.12), "iron")
    for j, x in enumerate((x0 - 0.3, x1 + 0.3)):
        box(f"Stop{j}", 0.6, GAUGE + 0.6, 0.7, at(x, TRACK_Y, 0), "timber", bevel=0.05)


def cart(i, x):
    """One stand: a wooden mine tub on four wheels; `Ore` sits in its bed (OrePreview in the renders)."""
    bs.station(f"Cart{i}", x, TRACK_Y)
    wz = 0.28 + 0.35
    for j, (wx, wy) in enumerate(((-0.8, -1), (0.8, -1), (-0.8, 1), (0.8, 1))):
        cyl(f"Wheel{j}", 0.35, 0.2, at(wx, wy * GAUGE / 2 - 0.1, wz), "iron_dk", sides=8, rot=(-90, 0, 0))
    for wx in (-0.8, 0.8):
        cyl(f"Axle{int(wx * 10)}", 0.08, GAUGE - 0.1, at(wx, -(GAUGE - 0.1) / 2, wz), "iron", sides=6, rot=(-90, 0, 0))
    box("Chassis", 2.2, 1.0, 0.2, at(0, 0, wz + 0.05), "iron", bevel=0.03)
    frustum("Body", 2.4, 1.5, 2.8, 1.9, 0.85, at(0, 0, wz + 0.22), "timber", bevel=0.05)
    top = wz + 0.22 + 0.85
    ring("Rim", 2.84, 1.94, 0.16, 0.34, at(0, 0, top - 0.06), "spool")
    for j, t in enumerate((-1, 1)):
        frustum(f"Strap{j}", 0.14, 1.5 + 0.4 * 0.05 / 0.85 + 0.06, 0.14, 1.5 + 0.4 * 0.8 / 0.85 + 0.06, 0.75, at(t * 0.75, 0, wz + 0.27), "iron_dk")
    return top


def ore_preview(top):
    bs.station("OrePreview", 0, 0)
    for i, x in enumerate(CARTS):
        frustum(f"Ore{i}", 2.0, 1.05, 1.6, 0.7, 0.65, at(x, TRACK_Y, top), "ore", bevel=0.05)


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
    me.from_pydata([(-60, -60, -0.01), (60, -60, -0.01), (60, 60, -0.01), (-60, 60, -0.01)], [], [(0, 1, 2, 3)])
    g = bpy.data.objects.new("Ground", me)
    gm = bpy.data.materials.new("Review_Ground")
    gm.use_nodes = True
    b = next(n for n in gm.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = bs.srgb2lin((0.70, 0.74, 0.62)) + (1,)
    b.inputs["Roughness"].default_value = 1.0
    me.materials.append(gm)
    sc.collection.objects.link(g)
    bs.avatar(-2.5, -8.0, yaw=0)
    cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = 1400, 1000
    shots = {"overview": ((0.6, -1, 0.55), 34, (0.5, -1, 3.0), 50, False),
             "front": ((0, -1, 0.18), 30, (0.5, -1, 3.6), 50, False),
             "carts": ((0.35, -1, 0.5), 13, (0, TRACK_Y, 1.2), 50, False),
             "headframe": ((-0.5, -1, 0.25), 15, (2, 2, 4.5), 50, False),
             "plan": ((0, 0, 1), 40, (0.5, -1.5, 0), 0, True)}
    out = []
    for name, (d, dist, target, lens, ortho) in shots.items():
        cam.data.type = "ORTHO" if ortho else "PERSP"
        cam.data.ortho_scale = 25
        cam.data.lens = lens or 50
        t = Vector(target)
        cam.location = t + Vector(d).normalized() * dist
        cam.rotation_euler = (t - cam.location).to_track_quat("-Z", "Y").to_euler()
        sc.render.filepath = os.path.join(HERE, "review", f"mine_shaft_{name}.png")
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
    shaft()
    track()
    top = 0
    for i, x in enumerate(CARTS, 1):
        top = cart(i, x)
    ore_preview(top)
    names = ("MineShaft", "Lever", "Track", "Cart1", "Cart2", "Cart3")
    hits = bs.zfight_check()
    report = bs.qa(names=names)
    tris = {n: sum(len(p.vertices) - 2 for o in bpy.data.collections[n].objects if o.type == "MESH"
                   for p in o.data.polygons) for n in names}
    shots = review()
    with open(os.path.join(HERE, "qa.json"), "w") as f:
        json.dump({"tris": tris, "zfight": sorted(hits), "qa": report}, f, indent=1, default=str)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, "MineShaft.blend"))
    print("MINESHAFT tris", tris, "zfight", len(hits), "ore top", round(top, 2))


if __name__ == "__main__":  # importable by build_mine_entrance.py
    main()

# Mine entrance for Create Swords! (Allen 2026-10-20, a Clash of Clans gold-mine reference: "it just comes out of
# the ground"). Replaces the mine shaft's headframe and bucket: a log A-frame tunnel mouth sinking back into a rocky
# mound, dark inside, with the rail track running out of it. Pull the lever and the carts roll out of the dark one
# by one with their ore; each cart is still a stand (a model with an `Ore` part the roll recolours).
#
# Run headless:  blender --background --python build_mine_entrance.py
# Writes, next to this script: MineEntrance.blend, review/*.png, qa.json. Design pass only, not exported yet.
# Units are studs, Z up, front faces -Y, origin on the floor at the middle of the mouth. Low poly, flat-shaded.
#
# Layout (plan, studs): the mouth's front edge at y -2.6, the frame sinking 1.2 over 7 studs into the mound behind;
# a black panel at y -0.6 closes the tunnel, so a cart rolling in vanishes. Six cart stops at most (Allen: "max of
# 6 carts/rolls"): the track runs straight out of the mouth past stops 1-3, turns right (as you face the mine, +X)
# on a 4-stud curve, then runs past stops 4-6 to an end stop. Stop 1 is nearest the mouth; with N carts the first
# out goes to stop N and the rest stop behind it. Lever at the left of the mouth.
import math
import os
import sys
import json
import bpy
import bmesh
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "MineShaft"))
import build_stations as bs  # noqa: E402
import build_mine_shaft as ms  # noqa: E402  (palette, beam(), cart())
from build_stations import at, box, cyl, frustum, rock  # noqa: E402

bs.PAL.update({"earth": (0.47, 0.40, 0.33), "gold": (0.95, 0.72, 0.25)})

Y0, Y1, DROP = -2.6, 4.4, 1.2          # frame front, back, and how far it sinks over that length
BASE, APEX = (3.0, 0.45), (0.4, 4.2)   # one slope of logs at the front: base (x, z) to top (x, z)
LOGS, LOG_R = 6, 0.46
PANEL_Y = -0.6                          # black panel closing the tunnel
GAUGE = ms.GAUGE
TRACK_START = 0.4                       # behind the black panel
TURN_Y, TURN_R = -14.2, 4.0             # the straight run ends here and curves toward +X
STOPS = (5.6, 9.1, 12.6, 22.5, 26.0, 29.5)  # cart stops, as distance along the track from TRACK_START
TRACK_END = 31.6


def path():
    """Track centreline as a polyline: straight out of the mouth, a quarter turn to +X, straight on."""
    pts = [Vector((0, TRACK_START, 0)), Vector((0, TURN_Y, 0))]
    c = Vector((TURN_R, TURN_Y, 0))
    for k in range(1, 7):  # 15-degree steps
        a = math.radians(180 + 15 * k)
        pts.append(c + Vector((math.cos(a), math.sin(a), 0)) * TURN_R)
    arc_end = TRACK_START - TURN_Y + sum((pts[i + 1] - pts[i]).length for i in range(1, 7))
    pts.append(pts[-1] + Vector((TRACK_END - arc_end, 0, 0)))
    return pts


def along(s):
    """Point and heading (radians) at distance s along the track."""
    pts = path()
    for a, b in zip(pts, pts[1:]):
        seg = (b - a).length
        if s <= seg:
            d = (b - a).normalized()
            return a + d * s, math.atan2(d.y, d.x)
        s -= seg
    d = (pts[-1] - pts[-2]).normalized()
    return pts[-1], math.atan2(d.y, d.x)


def sweep(name, pts, offset, w, z0, z1, color):
    """Square bar along a polyline, `offset` to the left of it, mitred at the bends (one rail)."""
    bm = bmesh.new()
    rings = []
    for i, p in enumerate(pts):
        ds = [(pts[j + 1] - pts[j]).normalized() for j in (i - 1, i) if 0 <= j < len(pts) - 1]
        t = sum(ds, Vector()).normalized()
        n = Vector((-t.y, t.x, 0))
        scale = 1 / max(n.dot(Vector((-ds[0].y, ds[0].x, 0))), 0.5)  # keep the bar width through the mitre
        rings.append([bm.verts.new(p + n * (offset + sx * w / 2) * scale + Vector((0, 0, z)))
                      for sx, z in ((-1, z0), (1, z0), (1, z1), (-1, z1))])
    for a, b in zip(rings, rings[1:]):
        for k in range(4):
            bm.faces.new((a[k], a[(k + 1) % 4], b[(k + 1) % 4], b[k]))
    bm.faces.new(rings[0][::-1]); bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return bs._finish(name, bm, color, at(0, 0, 0), (0, 0, 0), 0, smooth=False)


def sink(y):
    """How far the frame has dropped at y."""
    return (y - Y0) / (Y1 - Y0) * DROP


def log(name, x, z, y0, color="timber", r=LOG_R):
    """A log along the tunnel, sinking toward the back (octagonal prism between the two ends)."""
    p0, p1 = Vector((x, y0, z)), Vector((x, Y1, z - DROP))
    e = (p1 - p0).to_track_quat("Z", "X").to_euler()
    return cyl(name, r, (p1 - p0).length, p0, color, sides=8, rot=tuple(math.degrees(a) for a in e), bevel=0.03)


def strip(name, p0, p1, color="iron_dk", w=0.45, t=0.12):
    """Flat band from p0 to p1, its width along Y (iron straps over the logs)."""
    p0, p1 = Vector(p0), Vector(p1)
    e = (p1 - p0).to_track_quat("Z", "Y").to_euler()
    return box(name, t, w, (p1 - p0).length, p0, color, rot=tuple(math.degrees(a) for a in e), bevel=0.02)


def entrance():
    bs.station("MineEntrance", 0, 0)
    (bx, bz), (ax, az) = BASE, APEX
    for s in (-1, 1):
        for i in range(LOGS):  # log ends staggered so neighbours never share a cap plane
            f = i / (LOGS - 1)
            x, z = s * (bx + (ax - bx) * f), bz + (az - bz) * f
            log(f"Log{'LR'[s > 0]}{i}", x, z, Y0 - (0.14 if (i + (s > 0)) % 2 else 0))
    log("Ridge", 0, az + 0.55, Y0 - 0.25, color="spool", r=0.5)
    # iron straps over both slopes, near the front and the middle
    n = Vector((az - bz, 0, bx - ax)).normalized()  # outward normal of the right slope (x, z)
    for k, y in enumerate((Y0 + 0.7, Y0 + 2.9)):
        d = sink(y)
        for s in (-1, 1):
            off = (LOG_R + 0.05)
            p0 = (s * (bx + n.x * off), y, bz + n.z * off - d - 0.3)
            p1 = (s * (ax + n.x * off) * 0.2, y, az + n.z * off - d + 0.45)
            strip(f"Strap{k}{'LR'[s > 0]}", p0, p1)
    # black panel closing the tunnel: carts roll through it and vanish
    d = sink(PANEL_Y)
    bm = bmesh.new()
    pts = [(-3.3, 0.02), (3.3, 0.02), (0, az + 0.4 - d)]
    vs = [[bm.verts.new((x, y, z)) for x, z in pts] for y in (0, 0.1)]
    bm.faces.new(vs[0][::-1]); bm.faces.new(vs[1])
    for i in range(3):
        j = (i + 1) % 3
        bm.faces.new((vs[0][i], vs[0][j], vs[1][j], vs[1][i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bs._finish("TunnelDark", bm, "void", at(0, PANEL_Y, 0), (0, 0, 0), 0, smooth=False)
    box("TunnelFloor", 5.4, PANEL_Y - Y0 + 0.4, 0.04, at(0, (PANEL_Y + Y0) / 2 - 0.2, 0), "spool")
    # the mound the tunnel sinks into, rocks along the base, rubble by the mouth
    rock("Mound", 1.0, at(0, 4.4, -0.8), "earth", scale=(6.6, 5.0, 4.6), seed=7)
    for i, (x, y, r, c) in enumerate(((-3.7, -2.2, 0.95, "stone"), (3.8, -2.0, 1.05, "stone_dk"),
                                      (-3.9, -0.4, 0.8, "stone_dk"), (3.9, -0.2, 0.85, "stone"),
                                      (-3.4, 1.3, 0.9, "stone"), (3.5, 1.4, 0.8, "stone_dk"))):
        rock(f"BaseRock{i}", r, at(x, y, r * 0.35), c, scale=(1.1, 1.0, 0.75), seed=11 + i)
    for i, (x, y, z, r) in enumerate(((-4.5, 3.5, 1.5, 1.1), (4.4, 5.5, 1.5, 1.0), (1.8, 7.8, 1.5, 0.9),
                                      (-1.5, 8.2, 1.1, 0.8))):  # boulders breaking up the mound
        rock(f"MoundRock{i}", r, at(x, y, z), "stone" if i % 2 else "stone_dk", scale=(1.2, 1.0, 0.8), seed=50 + i)
    for i, (x, y, r) in enumerate(((-1.8, -3.4, 0.28), (-2.3, -4.1, 0.2), (1.9, -3.6, 0.32), (2.5, -4.4, 0.22),
                                   (1.6, -4.6, 0.18), (-1.6, -4.9, 0.22))):
        rock(f"Rubble{i}", r, at(x, y, r * 0.4), "stone_dk" if i % 2 else "stone", scale=(1.2, 1.0, 0.7), seed=30 + i)
    # paper lantern hanging at the front of the ridge
    ms.beam("LanternCord", (0, Y0 - 0.45, az + 0.1), (0, Y0 - 0.45, 3.55), 0.06, "iron_dk", bevel=0)
    cyl("LanternCap", 0.3, 0.1, at(0, Y0 - 0.45, 3.45), "red", sides=8)
    cyl("Lantern", 0.36, 0.7, at(0, Y0 - 0.45, 2.77), "paper", sides=8)
    cyl("LanternFoot", 0.3, 0.1, at(0, Y0 - 0.45, 2.69), "red", sides=8)
    # a crate of ingots beside the mouth
    box("Crate", 1.7, 1.4, 1.0, at(4.9, -3.9, 0), "timber", bevel=0.06)
    bs.ring("CrateRim", 1.76, 1.46, 0.14, 0.2, at(4.9, -3.9, 0.9), "spool")
    for i, (x, y, rz) in enumerate(((4.5, -4.1, 10), (5.25, -3.7, -15), (4.8, -3.6, 70))):
        frustum(f"Ingot{i}", 0.7, 0.36, 0.55, 0.24, 0.22, at(x, y, 1.0 + 0.05 * i), "gold", rot=(0, 0, rz), bevel=0.03)


def track():
    bs.station("Track", 0, 0)
    n = int((TRACK_END - 0.5) / 1.4) + 1
    for i in range(n):
        p, h = along(0.35 + i * (TRACK_END - 0.7) / (n - 1))
        box(f"Sleeper{i}", 0.5, GAUGE + 1.0, 0.12 + 0.02 * (i % 2), p, "spool", rot=(0, 0, math.degrees(h)))  # alternate tops: angled ones overlap on the curve
    pts = path()
    for j, t in enumerate((-1, 1)):
        sweep(f"Rail{j}", pts, t * GAUGE / 2, 0.16, 0.1, 0.28, "iron")
    p, h = along(TRACK_END)
    d = Vector((math.cos(h), math.sin(h), 0))
    box("Stop", 0.6, GAUGE + 0.6, 0.7, p + d * 0.25, "timber", rot=(0, 0, math.degrees(h)), bevel=0.05)


def lever():
    bs.station("Lever", -4.6, -4.2)
    box("Base", 1.2, 1.0, 0.45, at(0, 0, 0), "spool", bevel=0.05)
    box("Bracket", 0.45, 0.4, 0.8, at(0, 0, 0.44), "iron", bevel=0.03)
    box("Arm", 0.2, 0.2, 2.2, at(0, 0, 1.0), "timber", rot=(-25, 0, 0), bevel=0.02)
    s, c = math.sin(math.radians(25)), math.cos(math.radians(25))
    box("Knob", 0.36, 0.36, 0.45, at(0, 2.05 * s, 1.0 + 2.05 * c), "red", rot=(-25, 0, 0), bevel=0.04)


def carts():
    """One cart on each of the six stops (the most a player can own), each with a stand-in ore."""
    top = 0
    looks = ("ore", "gold", "ore_iron", "red", "indigo", "teal")
    bs.station("OrePreview", 0, 0)
    for i, s in enumerate(STOPS, 1):
        p, h = along(s)
        top = ms.cart(i, 0)
        root = bs._coll[0][1]
        root.location = p
        root.rotation_euler.z = h  # long side along the track
        bs._coll[0] = (bpy.data.collections["OrePreview"], bpy.data.objects["OrePreview"])
        frustum(f"Ore{i}", 2.0, 1.05, 1.6, 0.7, 0.65, Vector((p.x, p.y, top)), looks[i - 1],
                rot=(0, 0, math.degrees(h)), bevel=0.05)


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
    glow = bpy.data.objects.new("LanternGlow", bpy.data.lights.new("LanternGlow", "POINT"))
    glow.data.energy, glow.data.color = 80, (1.0, 0.6, 0.3)
    glow.location = (0, Y0 - 0.45, 3.1)
    sc.collection.objects.link(glow)
    me = bpy.data.meshes.new("Ground")
    me.from_pydata([(-60, -60, -0.01), (60, -60, -0.01), (60, 60, -0.01), (-60, 60, -0.01)], [], [(0, 1, 2, 3)])
    g = bpy.data.objects.new("Ground", me)
    gm = bpy.data.materials.new("Review_Ground")
    gm.use_nodes = True
    b = next(n for n in gm.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = bs.srgb2lin((0.72, 0.74, 0.78)) + (1,)
    b.inputs["Roughness"].default_value = 1.0
    me.materials.append(gm)
    sc.collection.objects.link(g)
    bs.avatar(-3.4, -18.5, yaw=-40)
    cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = 1400, 1000
    shots = {"overview": ((0.75, -1, 0.6), 40, (4, -9, 1.5)),
             "plan": ((0.0001, -0.0001, 1), 46, (4.5, -8, 0)),
             "front": ((-0.35, -1, 0.3), 36, (4, -8, 1.5)),
             "mouth": ((0.35, -1, 0.25), 11, (0, -2.5, 2.0)),
             "side": ((1, -0.15, 0.3), 34, (3, -8, 1.8))}
    out = []
    for name, (d, dist, target) in shots.items():
        cam.data.lens = 50
        t = Vector(target)
        cam.location = t + Vector(d).normalized() * dist
        cam.rotation_euler = (t - cam.location).to_track_quat("-Z", "Y").to_euler()
        sc.render.filepath = os.path.join(HERE, "review", f"mine_entrance_{name}.png")
        bpy.ops.render.render(write_still=True)
        out.append(sc.render.filepath)
    for ob in (sun, glow, g, cam):
        bpy.data.objects.remove(ob)
    for o in list(bpy.data.collections["Avatar"].objects):
        bpy.data.objects.remove(o)
    bpy.data.collections.remove(bpy.data.collections["Avatar"])
    return out


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    entrance()
    track()
    lever()
    carts()
    names = ("MineEntrance", "Track", "Lever", "Cart1")
    hits = bs.zfight_check()
    report = bs.qa(names=names)
    tris = {n: sum(len(p.vertices) - 2 for o in bpy.data.collections[n].objects if o.type == "MESH"
                   for p in o.data.polygons) for n in names}
    shots = review()
    with open(os.path.join(HERE, "qa.json"), "w") as f:
        json.dump({"tris": tris, "zfight": sorted(hits), "qa": report}, f, indent=1, default=str)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, "MineEntrance.blend"))
    print("ENTRANCE tris", tris, "zfight", len(hits))


if __name__ == "__main__":
    main()

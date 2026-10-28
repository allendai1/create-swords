# Chunky low-poly style pilot (2026-10-26). Allen's reference: the clay game's Clay Reroll lever machine, built from
# simple shapes, chunky, a small flat chamfer on every edge, flat shading, flat colours (dark brown loaf body split
# by a slot, orange arch panel on each side, sage-green base with a big chamfered rim, red ball knob, tan arm).
#
# Pilot: the Ore Roller's lever (OreRoller.Lever). Same hinge (ArmPivot) and swing; the body is the reference's shape.
# The knob is a Roblox Ball part (Allen: "just use a regular roblox sphere part"), 0.95, colour 176,34,30, at the
# arm's end (ARM_LEN from the hinge). Every part is built symmetric under a 180° turn about the vertical, so Roblox's import turn doesn't show.
# 1 Blender unit = 1 stud; Blender z is Roblox y; z 0 is the floor. The arm is built upright, centred on its own
# axis, with its hinge PIVOT_IN_ARM below its centre; Studio places it from ArmPivot.
#
# Style rule for the rest of the level: convex blocks (convex_hull of a few points), big design chamfers in the shape
# itself, then a 1-segment chamfer of CHAMFER on every edge, flat shaded, one flat colour per part.
import bpy, bmesh, math, os, sys
from mathutils import Vector

HERE = "C:/Users/Allen/Documents/Create Swords!/Models/Stations/Chunky"
sys.path.insert(0, os.path.dirname(HERE))
import build_stations as bs  # auto_uv, srgb2lin, _skill

CHAMFER = 0.04
COLL = "OreLeverChunky"
COLOURS = {  # Roblox Color3 (0-255), as set in Studio (darker than the reference: the workshop light is warm)
    "Base": (126, 134, 98), "Body": (80, 38, 20), "Panel": (180, 100, 30),
    "Slot": (32, 26, 22), "Arm": (178, 168, 140)
}
SLAB_TOP = 0.4
BODY_TOP = 2.3
PIVOT_Z = 2.0           # hinge height above the floor
ARM_LEN, ARM_TAIL = 2.3, 0.3   # hinge to knob centre; arm reaches this far below the hinge
PIVOT_IN_ARM = (ARM_LEN + ARM_TAIL) / 2 - ARM_TAIL  # arm centre is this far above the hinge


def hull(points, chamfer=CHAMFER):
    bm = bmesh.new()
    for p in points:
        bm.verts.new(p)
    bmesh.ops.convex_hull(bm, input=bm.verts[:])
    bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(0.5), verts=bm.verts[:], edges=bm.edges[:])
    if chamfer:
        bmesh.ops.bevel(bm, geom=bm.edges[:], offset=chamfer, segments=1, affect="EDGES", clamp_overlap=True)
    return bm


def mirror_x(pts):
    return pts + [(-x, y, z) for x, y, z in pts]


def mirror_y(pts):
    return pts + [(x, -y, z) for x, y, z in pts]


def slab():
    """Sage base: straight sides to 0.22, then a big chamfer to the top."""
    pts = []
    for z, hx, hy in ((0, 1.3, 1.75), (0.22, 1.3, 1.75), (SLAB_TOP, 1.12, 1.57)):
        pts += [(sx * hx, sy * hy, z) for sx in (1, -1) for sy in (1, -1)]
    return hull(pts, 0.03)


PROFILE = [(1.4, 0.0), (1.4, 0.84), (1.15, 1.51), (0.62, 1.79)]  # body side outline (y, height above its bottom)


def body():
    """Two loaf halves either side of the slot, outer top edge chamfered."""
    bm = bmesh.new()
    z0 = SLAB_TOP - 0.02  # sunk into the slab: no shared faces
    top = BODY_TOP - z0
    for side in (1, -1):
        pts = [(0.17, y, z0 + h) for y, h in PROFILE] + [(0.17, 0.6, z0 + top)]
        pts += [(0.95, y, z0 + h) for y, h in PROFILE] + [(0.85, 0.6, z0 + top)]
        half = hull(mirror_y([(side * x, y, z) for x, y, z in pts]))
        me = bpy.data.meshes.new("tmp")
        half.to_mesh(me)
        half.free()
        bm.from_mesh(me)
        bpy.data.meshes.remove(me)
    return bm


def panel():
    """Orange arch on each outer face: 0.06 proud, 0.02 buried."""
    bm = bmesh.new()
    z0 = SLAB_TOP - 0.02
    outline = [(1.2, 0.13), (1.2, 0.78), (0.98, 1.32), (0.52, 1.57)]
    for side in (1, -1):
        pts = [(side * x, y, z0 + h) for x in (0.93, 1.01) for y, h in outline]
        p = hull(mirror_y(pts), 0.02)
        me = bpy.data.meshes.new("tmp")
        p.to_mesh(me)
        p.free()
        bm.from_mesh(me)
        bpy.data.meshes.remove(me)
    return bm


def slot():
    """Dark block filling the slot floor, set back 0.1 from the body's ends."""
    pts = [(sx * 0.19, sy * 1.3, z) for sx in (1, -1) for sy in (1, -1) for z in (SLAB_TOP - 0.02, 1.3)]
    return hull(pts, 0.02)


def arm():
    sides, r, h = 8, 0.14, (ARM_LEN + ARM_TAIL) / 2
    pts = []
    for z, rr in ((-h, r - 0.03), (-h + 0.03, r), (h - 0.03, r), (h, r - 0.03)):
        pts += [(rr * math.cos(2 * math.pi * (i + 0.5) / sides), rr * math.sin(2 * math.pi * (i + 0.5) / sides), z)
                for i in range(sides)]
    return hull(pts, 0)


def make(name, bm, loc=(0, 0, 0)):
    bmesh.ops.dissolve_degenerate(bm, dist=1e-5, edges=bm.edges[:])
    bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 4])
    bs.auto_uv(bm)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = False  # flat shading: every facet reads, as in the reference
    m = bpy.data.materials.get("CH_" + name) or bpy.data.materials.new("CH_" + name)
    col = bs.srgb2lin([c / 255 for c in COLOURS[name]]) + (1.0,)
    m.diffuse_color = col
    next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED").inputs["Base Color"].default_value = col
    me.materials.append(m)
    o = bpy.data.objects.new(name, me)
    o.location = loc
    bpy.data.collections[COLL].objects.link(o)
    return o


def build():
    c = bpy.data.collections.get(COLL)
    if c:
        for o in list(c.objects):
            bpy.data.objects.remove(o, do_unlink=True)
    else:
        c = bpy.data.collections.new(COLL)
        bpy.context.scene.collection.children.link(c)
    make("Base", slab())
    make("Body", body())
    make("Panel", panel())
    make("Slot", slot())
    # Review pose: leaning back 25° about the hinge, as at rest in the game
    lean = math.radians(25)
    a = make("Arm", arm(), (0, -PIVOT_IN_ARM * math.sin(lean), PIVOT_Z + PIVOT_IN_ARM * math.cos(lean)))
    a.rotation_euler = (lean, 0, 0)
    for o in c.objects:
        print(o.name, len(o.data.polygons), "faces", [round(d, 3) for d in o.dimensions])


def export():
    """One FBX, every part at its review place (the arm at rest)."""
    exp = bs._skill("export_asset", "blender-export-pipelines")
    return exp.run(preset="roblox", collection=COLL, out=os.path.join(HERE, "OreLeverChunky.fbx"), no_anim=True)


if __name__ == "__main__":
    build()
    export()

# The anvil's swing hammer (2026-11-11). Allen: "can we create a better looking hammer in blender and use that in the
# animation. bevel the edges of the hammer like the rest of our models."
#
# Two objects, so the game can colour them apart: Head (steel) and Handle (wood).
# Bevels follow Models/Stations/Bevelled (bevel_for: 0.2 of the smallest side, at most 0.09 stud, rounded, 3 segments;
# smooth shading with weighted normals, so flat faces stay flat and the curve sits in the bevel).
# 1 Blender unit = 1 stud. Roblox (x, y, z) is Blender (x, -z, y).
#
# How AnvilController uses them (head and handle are placed apart every frame):
#   Head  : Roblox local -X is the striking face (down), +X the cross peen (up); the handle leaves along local -Z,
#           so the peen's edge runs along local Y (across the handle). Centred on its bounding box.
#   Handle: along Roblox local Z; +Z end at the head, -Z end the grip (a swell). The game stretches its length.
import bpy, bmesh, math, os, sys

HERE = "C:/Users/Allen/Documents/Create Swords!/Models/Props/AnvilHammer"
STATIONS = "C:/Users/Allen/Documents/Create Swords!/Models/Stations"
sys.path.insert(0, STATIONS)
sys.path.insert(0, STATIONS + "/Bevelled")
import build_stations as bs  # auto_uv, _skill
from build_bevelled import bevel_for, colour


def R(x, y, z):
    """Roblox local (x, y, z) -> Blender, turned 180 degrees about the vertical first: Roblox's importer turns meshes
    180 degrees about Y (seen on the station wedges, and on this hammer's first upload, 136312638180747, whose face came
    out at +X and grip at +Z)."""
    return (-x, z, y)


def collection(name):
    c = bpy.data.collections.get(name)
    if c:
        for o in list(c.objects):
            bpy.data.objects.remove(o, do_unlink=True)
    else:
        c = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(c)
    return c


def box(bm, x0, x1, y, z, w=None):
    """A Roblox-axes box from x0 to x1, y wide, z deep, all edges bevelled."""
    verts = [bm.verts.new(R(x, sy * y / 2, sz * z / 2)) for x in (x0, x1) for sy in (-1, 1) for sz in (-1, 1)]
    geom = bmesh.ops.convex_hull(bm, input=verts)
    faces = [f for f in geom["geom"] if isinstance(f, bmesh.types.BMFace)]
    edges = list({e for f in faces for e in f.edges})
    bw, seg = w or bevel_for(min(x1 - x0, y, z))
    bmesh.ops.bevel(bm, geom=edges, offset=bw, segments=seg, profile=0.5, affect="EDGES", clamp_overlap=True)


def prism(bm, x0, x1, radius, sides=8):
    """An octagonal face along Roblox X, rims bevelled."""
    rings = [[bm.verts.new(R(x, radius * math.cos(a), radius * math.sin(a)))
              for a in (2 * math.pi * (i + 0.5) / sides for i in range(sides))] for x in (x0, x1)]
    geom = bmesh.ops.convex_hull(bm, input=rings[0] + rings[1])
    faces = [f for f in geom["geom"] if isinstance(f, bmesh.types.BMFace)]
    edges = list({e for f in faces for e in f.edges})
    w, seg = bevel_for(min(x1 - x0, 2 * radius))
    bmesh.ops.bevel(bm, geom=edges, offset=w, segments=seg, profile=0.5, affect="EDGES", clamp_overlap=True)


def peen(bm, x0, x1, y, z0, z1):
    """The cross peen: y wide, tapering in z from z0 at x0 to a z1-thin edge at x1."""
    verts = [bm.verts.new(R(x, sy * y / 2, sz * z / 2)) for x, z in ((x0, z0), (x1, z1)) for sy in (-1, 1) for sz in (-1, 1)]
    geom = bmesh.ops.convex_hull(bm, input=verts)
    faces = [f for f in geom["geom"] if isinstance(f, bmesh.types.BMFace)]
    edges = list({e for f in faces for e in f.edges})
    bmesh.ops.bevel(bm, geom=edges, offset=0.016, segments=2, profile=0.5, affect="EDGES", clamp_overlap=True)


def section(x, hy, hz, c):
    """An 8-point cross-section at Roblox x: half-width hy (across the handle), half-depth hz (along the handle),
    corners cut by c (c = 0.586 * hy on a square gives a regular octagon)."""
    pts = ((hy, hz - c), (hy - c, hz), (-(hy - c), hz), (-hy, hz - c), (-hy, -(hz - c)), (-(hy - c), -hz), (hy - c, -hz), (hy, -(hz - c)))
    return [R(x, y, z) for y, z in pts]


HEAD_SECTIONS = (  # (x, half across, half along the handle, corner cut)
    (-0.24, 0.12, 0.12, 0.07),  # the striking face: a regular octagon
    (-0.165, 0.12, 0.12, 0.07),
    (-0.135, 0.08, 0.08, 0.03),  # a sloped shoulder in to the neck
    (-0.1, 0.08, 0.08, 0.03),
    (-0.075, 0.1, 0.1, 0.025),  # out to the cheek
    (0.05, 0.1, 0.1, 0.025),
    (0.24, 0.088, 0.018, 0.012),  # the cross peen: full width across the handle, thin along it
)


def head_mesh():
    bm = bmesh.new()
    rings = [[bm.verts.new(p) for p in section(*s)] for s in HEAD_SECTIONS]
    n = len(rings[0])
    for a, b in zip(rings, rings[1:]):
        for i in range(n):
            j = (i + 1) % n
            bm.faces.new((a[i], a[j], b[j], b[i]))
    bm.faces.new(rings[0][::-1])
    bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    sharp = [e for e in bm.edges if e.is_manifold and e.calc_face_angle(0) > math.radians(20)]
    bmesh.ops.bevel(bm, geom=sharp, offset=0.014, segments=3, profile=0.5, affect="EDGES", clamp_overlap=True)
    return bm


def finish(name, bm, rgb, material, coll):
    bmesh.ops.dissolve_degenerate(bm, dist=1e-5, edges=bm.edges[:])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 4])
    bs.auto_uv(bm)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    me.materials.append(colour(rgb, material))
    o = bpy.data.objects.new(name, me)
    coll.objects.link(o)
    wn = o.modifiers.new("WeightedNormal", "WEIGHTED_NORMAL")
    wn.mode, wn.weight, wn.keep_sharp = "FACE_AREA", 100, True
    with bpy.context.temp_override(object=o, active_object=o, selected_objects=[o]):
        bpy.ops.object.modifier_apply(modifier=wn.name)
    return o


def build():
    coll = collection("AnvilHammer")
    # Head, 0.48 long, one solid (Allen 2026-11-11: "should look like one piece, not multiple parts together. the final
    # piece should have the bevelled edges"): lofted through cross-sections along X, from an octagonal striking face
    # (0.24 across) in to a slim neck, out to a square cheek where the handle goes in, then a cross peen tapering to a
    # thin edge across the handle. Every sharp edge of the finished solid is then bevelled.
    head = finish("Head", head_mesh(), (72, 72, 78), "Metal", coll)
    # Handle, 1 stud (stretched in game): an oval section, a slim neck under the head, a swell at the grip.
    bm = bmesh.new()
    sides = 10
    rings = []
    for z, r in ((0.5, 0.048), (0.44, 0.048), (0.3, 0.042), (0.0, 0.047), (-0.32, 0.057), (-0.44, 0.063), (-0.5, 0.057)):
        rings.append([bm.verts.new(R(0.85 * r * math.cos(a), r * math.sin(a), z))
                      for a in (2 * math.pi * i / sides for i in range(sides))])
    for k in range(len(rings) - 1):
        for i in range(sides):
            j = (i + 1) % sides
            bm.faces.new((rings[k][i], rings[k][j], rings[k + 1][j], rings[k + 1][i]))
    for ring, flip in ((rings[0], False), (rings[-1], True)):
        f = bm.faces.new(ring[::-1] if flip else ring)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    caps = [e for e in bm.edges if all(abs(v.co.y) > 0.499 for v in e.verts)]
    bmesh.ops.bevel(bm, geom=caps, offset=0.012, segments=2, profile=0.5, affect="EDGES", clamp_overlap=True)
    handle = finish("Handle", bm, (168, 122, 78), "Wood", coll)
    head.location = (0, 0, 0)
    handle.location = (0.8, 0, 0)  # apart for review; the export moves each to its own origin
    return head, handle


def export():
    exp = bs._skill("export_asset", "blender-export-pipelines")
    res = exp.run(preset="roblox", collection="AnvilHammer", out=os.path.join(HERE, "AnvilHammer.fbx"), no_anim=True)
    bpy.ops.object.select_all(action="DESELECT")
    return res


if __name__ == "__main__":
    build()
    export()

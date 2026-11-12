# The stations' soft bevel for the Blender props (Decisions Log 2026-10-24, "Soft-bevelled stations"; the rule is
# Models/Stations/Bevelled/build_bevelled.py's): every block gets a rounded bevel of 0.2 of its smallest side, at most
# 0.09 studs, 3 segments (2 or 1 on small parts), and the joined mesh is smooth shaded with weighted normals so flat
# faces stay flat and the curve sits in the bevel.
# Use after the festival helpers are exec'd: exec(open(<this file>).read()) wraps box, cyl, lathe and join in place.
# (2026-11-07, Allen on the sanbo stands and the shrine: "it doesnt have the bevelled edges style in the models".)
import math

import bmesh
import bpy


def bevel_for(m):
    """Bevel width and segments for a part whose smallest side is m (build_bevelled.py's rule)."""
    w = min(max(0.2 * m, 0.008), 0.09, 0.45 * m)
    return w, 3 if w >= 0.03 else 2 if w >= 0.012 else 1


def soften(o):
    """Bevel the object's own mesh: every edge sharper than 40 degrees, sized from its smallest side."""
    me = o.data
    xs = [v.co for v in me.vertices]
    dims = [max(c[i] for c in xs) - min(c[i] for c in xs) for i in range(3)]
    m = min(d for d in dims if d > 1e-6)
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.normal_update()
    edges = [e for e in bm.edges if e.is_manifold and e.calc_face_angle(0) > math.radians(40)]
    w, seg = bevel_for(m)
    if edges:
        bmesh.ops.bevel(bm, geom=edges, offset=w, segments=seg, profile=0.5, affect="EDGES", clamp_overlap=True)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-5, edges=bm.edges[:])
    bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 4])  # bevel corners: no n-gons
    bm.to_mesh(me)
    bm.free()
    return o


def smooth(o):
    """Smooth shading with weighted normals, applied into the mesh."""
    for p in o.data.polygons:
        p.use_smooth = True
    wn = o.modifiers.new("WeightedNormal", "WEIGHTED_NORMAL")
    wn.mode, wn.weight, wn.keep_sharp = "FACE_AREA", 100, True
    with bpy.context.temp_override(object=o, active_object=o, selected_objects=[o]):
        bpy.ops.object.modifier_apply(modifier=wn.name)
    return o


_hard_box, _hard_cyl, _hard_lathe, _hard_join = box, cyl, lathe, join  # noqa: F821 (the festival helpers)


def box(size, loc, rot=(0, 0, 0)):
    return soften(_hard_box(size, loc, rot))


def cyl(r, depth, loc, rot=(0, 0, 0), verts=8, r2=None):
    return soften(_hard_cyl(r, depth, loc, rot=rot, verts=verts, r2=r2))


def lathe(profile, loc, verts=8):
    return soften(_hard_lathe(profile, loc, verts=verts))


def join(objs, name, coll):
    return smooth(_hard_join(objs, name, coll))

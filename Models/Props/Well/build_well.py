# Well (ido) for the shrine-end plaza, Sell Swords! (2026-11-04, plaza dressing pass; Allen: "if you're going to create
# models, create them in Blender with a low poly style"). Low poly, flat shaded: three staggered courses of stone blocks,
# a wooden rim, two square posts, a beam with a pulley, a gabled tiled roof, a rope and a bucket on the rim.
#
# Run in Blender (MCP execute_blender_code: exec(open(<this file>).read())) or headless:
#   blender --background --python build_well.py
# Writes Well.fbx (blender-export-pipelines `roblox` preset) next to this file.
#
# Units are studs, Z up, the posts along X, origin on the floor under the well's centre. One object per Studio
# material, named for its part (Stone, Wood, Roof, Water, Rope); Studio sets each MeshPart's material and colour.
import math
import os

import bmesh
import bpy

HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else "C:/Users/Allen/Documents/Create Swords!/Models/Props/Well"
SKILLS = "C:/Users/Allen/.claude/plugins/cache/blender-agent-skills/blender-agent-skills/1.1.0/skills"
COLL = "Well"

R_IN, R_OUT = 1.45, 1.9     # the stone ring
COURSE, COURSES, STONES = 0.75, 3, 8
RIM_Z0, RIM_Z1 = COURSE * COURSES, COURSE * COURSES + 0.2
POST_X, POST_H = 2.3, 6.6
BEAM_Z = 5.0
ROOF_PITCH = math.radians(25)


def fresh_collection():
    old = bpy.data.collections.get(COLL)
    if old:
        for o in list(old.objects):
            bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(old)
    c = bpy.data.collections.new(COLL)
    bpy.context.scene.collection.children.link(c)
    return c


def mesh_object(name, bm):
    me = bpy.data.meshes.new(name)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    return o


def sector(r0, r1, a0, a1, z0, z1, segs=2):
    """An annular sector block (a stone or a rim piece) from angle a0 to a1."""
    bm = bmesh.new()
    rings = []
    for r, z in ((r0, z0), (r1, z0), (r1, z1), (r0, z1)):
        rings.append([bm.verts.new((r * math.cos(a0 + (a1 - a0) * i / segs), r * math.sin(a0 + (a1 - a0) * i / segs), z))
                      for i in range(segs + 1)])
    for k in range(4):
        a, b = rings[k], rings[(k + 1) % 4]
        for i in range(segs):
            bm.faces.new((a[i], a[i + 1], b[i + 1], b[i]))
    bm.faces.new([r[0] for r in rings])
    bm.faces.new([r[-1] for r in reversed(rings)])
    return bm


def box(name, size, loc, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return o


def cyl(name, r, depth, loc, rot=(0, 0, 0), verts=8, r2=None):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r2, depth=depth, location=loc, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    return o


def join(objs, name):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    if len(objs) > 1:
        bpy.ops.object.join()
    ob = bpy.context.view_layer.objects.active
    ob.name = ob.data.name = name
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    for p in ob.data.polygons:
        p.use_smooth = False
    return ob


def build():
    coll = fresh_collection()
    parts = {}

    # stone: three courses of eight blocks, each course turned half a block, small gaps, heights varied a little
    stones = []
    gap = 0.035
    step = 2 * math.pi / STONES
    for c in range(COURSES):
        off = step / 2 * (c % 2)
        for i in range(STONES):
            a0 = off + i * step + gap / R_OUT
            a1 = off + (i + 1) * step - gap / R_OUT
            z0 = c * COURSE + (gap / 2 if c else 0)
            z1 = (c + 1) * COURSE - gap / 2 + (0.03 * ((i * 5 + c * 3) % 3 - 1) if c < COURSES - 1 else 0)
            bulge = 0.04 * ((i * 7 + c) % 3)
            stones.append(mesh_object("Stone", sector(R_IN, R_OUT + bulge, a0, a1, z0, z1)))
    parts["Stone"] = join(stones, "Stone")

    # wood: the rim (eight boards), two posts, the beam, the pulley and its block, the bucket
    wood = []
    for i in range(STONES):
        wood.append(mesh_object("Rim", sector(R_IN - 0.05, R_OUT + 0.12, i * step + 0.01, (i + 1) * step - 0.01, RIM_Z0, RIM_Z1, segs=1)))
    for s in (-1, 1):
        wood.append(box("Post", (0.36, 0.36, POST_H), (s * POST_X, 0, POST_H / 2)))
        wood.append(box("Brace", (0.5, 0.5, 0.18), (s * POST_X, 0, 0.09)))  # a foot block under each post
    wood.append(box("Beam", (2 * POST_X + 0.5, 0.3, 0.3), (0, 0, BEAM_Z)))
    wood.append(box("Block", (0.18, 0.24, 0.3), (0, 0, BEAM_Z - 0.3)))
    wood.append(cyl("Pulley", 0.32, 0.14, (0, 0, BEAM_Z - 0.55), rot=(0, math.pi / 2, 0), verts=8))
    wood.append(cyl("Bucket", 0.3, 0.7, (0, -1.68, RIM_Z1 + 0.35), verts=8, r2=0.38))
    wood.append(box("Handle", (0.05, 0.62, 0.05), (0, -1.68, RIM_Z1 + 0.95)))
    parts["Wood"] = join(wood, "Wood")

    # roof: two tiled slopes over the posts, the ridge along X, ribs of tiles running down each slope, a ridge cap
    roof = []
    run = 1.6
    length = 2 * POST_X + 1.4
    slope_w = run / math.cos(ROOF_PITCH) + 0.5
    top = POST_H + 0.05
    for s in (-1, 1):
        cy = s * (slope_w / 2 - 0.25) * math.cos(ROOF_PITCH)
        cz = top - (slope_w / 2 - 0.25) * math.sin(ROOF_PITCH)
        rot = (-s * ROOF_PITCH, 0, 0)  # each slope falls away from the ridge
        roof.append(box("Slope", (length, slope_w, 0.2), (0, cy, cz), rot=rot))
        n = 9
        for k in range(n):
            x = (k - (n - 1) / 2) * (length - 0.4) / (n - 1)
            nz = math.cos(ROOF_PITCH) * 0.12
            ny = s * math.sin(ROOF_PITCH) * 0.12
            roof.append(box("Rib", (0.16, slope_w, 0.12), (x, cy + ny, cz + nz), rot=rot))
    roof.append(box("Ridge", (length + 0.3, 0.42, 0.34), (0, 0, top + 0.08)))
    for s in (-1, 1):
        roof.append(box("RidgeEnd", (0.3, 0.55, 0.5), (s * (length / 2 + 0.2), 0, top + 0.2)))
    parts["Roof"] = join(roof, "Roof")

    # water: a dark octagon down inside the ring
    parts["Water"] = join([cyl("Water", R_IN + 0.02, 0.06, (0, 0, 1.5), rot=(0, 0, step / 2), verts=8)], "Water")

    # rope: from the pulley down to the bucket's handle
    p0 = (0, 0, BEAM_Z - 0.85)
    p1 = (0, -1.68, RIM_Z1 + 0.98)
    dy, dz = p1[1] - p0[1], p1[2] - p0[2]
    ln = math.hypot(dy, dz)
    ang = math.atan2(dy, dz)
    parts["Rope"] = join([cyl("Rope", 0.04, ln, (0, (p0[1] + p1[1]) / 2, (p0[2] + p1[2]) / 2), rot=(-ang, 0, 0), verts=5)], "Rope")

    for o in parts.values():
        for c in o.users_collection:
            c.objects.unlink(o)
        coll.objects.link(o)
        if len(o.data.uv_layers) == 0:
            o.data.uv_layers.new(name="UVMap")
    return coll, parts


def export(coll):
    import importlib
    import sys
    p = os.path.join(SKILLS, "blender-export-pipelines", "scripts")
    if p not in sys.path:
        sys.path.insert(0, p)
    exp = importlib.reload(importlib.import_module("export_asset"))
    return exp.run(preset="roblox", collection=coll.name, out=os.path.join(HERE, "Well.fbx"), batch=True, no_anim=True)


if __name__ == "__main__" or True:
    coll, parts = build()
    tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in parts.values())
    print("built", {n: len(o.data.polygons) for n, o in parts.items()}, "tris", tris)

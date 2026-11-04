# Training dummy for Sell Swords! (Allen 2026-11-03: "just a quirky decoration, players can hit it and it does a little
# animation"; like +1 simulators' dummies, stand close and it gets hit). A straw-stuffed burlap sack on a wooden post
# with a crossbar for arms, rope bands, a sack head with stitched X eyes and a smile, on two crossed foot planks.
#
# Run in Blender (MCP execute_blender_code: exec(open(<this file>).read())) or headless:
#   blender --background --python build_training_dummy.py
# Writes TrainingDummy.fbx (blender-export-pipelines `roblox` preset) and TrainingDummy.blend next to this file.
#
# Units are studs, Z up, front faces -Y, origin on the floor under the post. One object per Studio material, named
# for its part; everything but `Feet` wobbles about the top of the feet (TrainingDummy client code), so `Feet` is the
# only part that stays put. A player is about 5 studs tall; the dummy's head top is at about 5.3.
import math
import os

import bmesh
import bpy
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else "C:/Users/Allen/Documents/Create Swords!/Models/Props/TrainingDummy"
SKILLS = "C:/Users/Allen/.claude/plugins/cache/blender-agent-skills/blender-agent-skills/1.1.0/skills"
COLL = "TrainingDummy"

FEET_TOP = 0.3        # the planks' top; the wobble's pivot
POST_R = 0.17
BODY_Z0, BODY_Z1 = 1.55, 3.75
ARM_Z = 3.35
HEAD_Z, HEAD_R = 4.55, 0.62


def fresh_collection():
    old = bpy.data.collections.get(COLL)
    if old:
        for o in list(old.objects):
            bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(old)
    c = bpy.data.collections.new(COLL)
    bpy.context.scene.collection.children.link(c)
    return c


def link(obj, coll):
    for c in obj.users_collection:
        c.objects.unlink(obj)
    coll.objects.link(obj)
    return obj


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
    return ob


def box(size, loc, rot=(0, 0, 0), bevel=0.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.active_object
    o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        m = o.modifiers.new("Bevel", "BEVEL")
        m.width, m.segments = bevel, 2
        bpy.ops.object.modifier_apply(modifier=m.name)
    return o


def cyl(r, depth, loc, rot=(0, 0, 0), verts=12):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    return bpy.context.active_object


def lathe(profile, verts=16, name="lathe"):
    """A closed solid of revolution about Z from (radius, z) points, bottom to top (end radii 0 close the caps)."""
    bm = bmesh.new()
    rings = []
    for r, z in profile:
        if r <= 1e-4:
            rings.append([bm.verts.new((0, 0, z))])
        else:
            rings.append([bm.verts.new((r * math.cos(2 * math.pi * i / verts), r * math.sin(2 * math.pi * i / verts), z))
                          for i in range(verts)])
    for a, b in zip(rings, rings[1:]):
        for i in range(verts):
            j = (i + 1) % verts
            if len(a) == 1:
                bm.faces.new((a[0], b[i], b[j]))
            elif len(b) == 1:
                bm.faces.new((a[i], b[0], a[j]))
            else:
                bm.faces.new((a[i], b[i], b[j], a[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    for p in me.polygons:
        p.use_smooth = True
    return o


def torus(R, r, z, scale_xy=1.0):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, major_segments=20, minor_segments=6, location=(0, 0, z))
    o = bpy.context.active_object
    o.scale = (scale_xy, scale_xy, 1)
    return o


def tuft(loc, direction, length=0.65, spread=0.24, n=6):
    """A little fan of straw: thin cones splaying out from loc along direction."""
    d = Vector(direction).normalized()
    side = d.cross(Vector((0, 0, 1)))
    if side.length < 1e-3:
        side = Vector((1, 0, 0))
    side.normalize()
    up = side.cross(d)
    out = []
    for i in range(n):
        a = (i / (n - 1) - 0.5) * 1.4
        b = ((i * 37) % 5 / 4 - 0.5) * 0.8
        dir_i = (d + side * math.sin(a) * 0.7 + up * b * 0.6).normalized()
        ln = length * (0.8 + 0.4 * ((i * 53) % 7) / 6)
        bpy.ops.mesh.primitive_cone_add(vertices=5, radius1=spread * 0.35, radius2=0.0, depth=ln,
                                        location=Vector(loc) + dir_i * ln / 2)
        c = bpy.context.active_object
        c.rotation_mode = "QUATERNION"
        c.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(dir_i)
        out.append(c)
    return out


def build():
    coll = fresh_collection()
    parts = {}

    # feet: two crossed planks (one a hair higher so their tops never share a plane)
    a = box((2.6, 0.5, 0.26), (0, 0, 0.13))
    b = box((0.5, 2.6, 0.26), (0, 0, 0.17))
    parts["Feet"] = join([a, b], "Feet")

    # wood that wobbles: the post and the arm crossbar with knobbed ends
    post = cyl(POST_R, 4.3, (0, 0, FEET_TOP - 0.05 + 4.3 / 2), verts=10)
    arm = cyl(0.12, 2.9, (0, 0, ARM_Z), rot=(0, math.pi / 2, 0), verts=8)
    parts["Wood"] = join([post, arm], "Wood")

    # burlap body: a barrel sack, cinched under the head, a little bulge at the belly
    body = lathe([(0.0, BODY_Z0 - 0.06), (0.46, BODY_Z0), (0.66, BODY_Z0 + 0.35), (0.72, 2.45), (0.70, 2.95),
                  (0.62, 3.4), (0.40, BODY_Z1 - 0.05), (0.0, BODY_Z1 + 0.05)], verts=18, name="Body")
    body.scale = (1.0, 0.86, 1.0)
    parts["Burlap"] = body

    # head: a squashed sack ball with a pinched top
    head = lathe([(0.0, HEAD_Z - HEAD_R * 0.92), (0.36, HEAD_Z - HEAD_R * 0.8), (0.58, HEAD_Z - 0.25), (HEAD_R, HEAD_Z + 0.05),
                  (0.56, HEAD_Z + 0.4), (0.34, HEAD_Z + 0.6), (0.12, HEAD_Z + 0.7), (0.0, HEAD_Z + 0.74)], verts=18, name="Head")
    head.scale = (1.0, 0.9, 1.0)
    parts["Head"] = head

    # rope: two bands round the body, a neck tie, and wraps where the arms cross the post
    ropes = [torus(0.71, 0.06, 2.0, 1.0), torus(0.72, 0.06, 2.95, 1.0), torus(0.3, 0.07, BODY_Z1 + 0.12, 1.0)]
    for o in ropes[:2]:
        o.scale = (1.0, 0.86, 1.0)
    for x in (-1.15, 1.15):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.14, minor_radius=0.05, major_segments=12, minor_segments=5,
                                         location=(x, 0, ARM_Z), rotation=(0, math.pi / 2, 0))
        ropes.append(bpy.context.active_object)
    parts["Rope"] = join(ropes, "Rope")

    # straw: tufts out of each arm end, the neck and the top of the head
    straw = []
    straw += tuft((1.45, 0, ARM_Z), (1, 0, -0.15))
    straw += tuft((-1.45, 0, ARM_Z), (-1, 0, -0.15))
    straw += tuft((0, 0, HEAD_Z + 0.7), (0, 0, 1), length=0.35, n=6)
    straw += tuft((0, -0.25, BODY_Z1 + 0.05), (0, -1, -0.6), length=0.3, n=4)
    parts["Straw"] = join(straw, "Straw")

    # face: stitched X eyes and a stitched smile on the head's front (-Y), sunk a little into the sack
    face_y = -HEAD_R * 0.9 + 0.02
    marks = []
    for ex in (-0.22, 0.22):
        for ang in (math.pi / 4, -math.pi / 4):
            marks.append(box((0.24, 0.07, 0.05), (ex, face_y + 0.04, HEAD_Z + 0.12), rot=(0, ang, 0), bevel=0.015))
    for i in range(5):
        t = (i - 2) / 2
        x = t * 0.24
        z = HEAD_Z - 0.2 + 0.07 * t * t
        marks.append(box((0.13, 0.09, 0.05), (x, face_y - 0.02 + 0.03 * t * t, z), rot=(0, -math.atan(0.14 * t / 0.24 * 2), 0), bevel=0.012))
    for i in range(4):
        x = (i - 1.5) * 0.12
        marks.append(box((0.035, 0.09, 0.12), (x, face_y - 0.01, HEAD_Z - 0.2 + 0.07 * ((i - 1.5) / 2) ** 2), bevel=0.01))
    parts["Stitch"] = join(marks, "Stitch")
    # a patch on the belly (quirky), slightly proud of the sack
    patch = box((0.42, 0.08, 0.34), (0.22, -0.62 * 0.86 - 0.01, 2.5), rot=(0, 0.2, 0), bevel=0.03)
    parts["Patch"] = join([patch], "Patch")

    for name, o in parts.items():
        link(o, coll)
        o.name = name
        if o.data.uv_layers.get("UVMap") is None and len(o.data.uv_layers) == 0:
            o.data.uv_layers.new(name="UVMap")
    return coll, parts


def export(coll):
    import importlib
    import sys
    p = os.path.join(SKILLS, "blender-export-pipelines", "scripts")
    if p not in sys.path:
        sys.path.insert(0, p)
    exp = importlib.reload(importlib.import_module("export_asset"))
    return exp.run(preset="roblox", collection=coll.name, out=os.path.join(HERE, "TrainingDummy.fbx"), batch=True, no_anim=True)


if __name__ == "__main__" or True:
    coll, parts = build()
    tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in parts.values())
    print("built", {n: len(o.data.polygons) for n, o in parts.items()}, "tris", tris)

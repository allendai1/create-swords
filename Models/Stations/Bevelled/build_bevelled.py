# Soft-bevelled stations (2026-10-24). Allen: "Notice our shop tables have bevels on the edges. I would like our
# current stations to also have those soft bevels."
#
# The *_parts.json files are exported from Studio: every visible block, cylinder and wedge Part of a model as
#   [model, name, key, shape "B"/"C"/"W", size (x, y, z), plot-space CFrame (12 components), rgb, material].
# stations_parts.json: OreRoller, IngotRack(2), HiltBench, PolishStation, EtchingTable(2), SwordRack(2).
# shelves_parts.json: the shop's WallRack1-4 (Allen: "try the shelves in the shop as well").
# key is the shape and size in millistuds: "B<x>_<y>_<z>" for a block, "W<x>_<y>_<z>" for a wedge,
# "C<length>_<diameter>" for a cylinder (Roblox cylinders run along X). Parts of one size share one mesh.
#
# build():   one bevelled mesh per key in the StationBevels collection (a grid, for the FBX), then every model
#            assembled from linked copies in its own collection, coloured like the game, for review.
# export():  StationBevels.fbx, one object per key named by its key (the `roblox` preset, as build_stations);
#            export(keys) writes only those keys (the sizes Studio's StationBevels folder doesn't have yet).
#
# Bevel: the SwordTable's top is bevelled about 0.2 of its thickness (0.085 on 0.41), so each part gets 0.2 of its
# smallest side, at most 0.09; rounded, 3 segments (2 or 1 on small parts). Shading is smooth with weighted
# normals, so flat faces stay flat and the curve sits in the bevel.
# 1 Blender unit = 1 stud. Roblox (x, y, z) is Blender (x, -z, y).
import bpy, bmesh, json, math, os, sys
from mathutils import Matrix, Vector

HERE = "C:/Users/Allen/Documents/Create Swords!/Models/Stations/Bevelled"
sys.path.insert(0, os.path.dirname(HERE))
import build_stations as bs  # auto_uv, srgb2lin, _skill, zfight_check

C = Matrix(((1, 0, 0), (0, 0, -1), (0, 1, 0)))  # Roblox axes -> Blender axes
CI = C.transposed()


def bevel_for(m):
    """Bevel width and segments for a part whose smallest side is m."""
    w = min(max(0.2 * m, 0.008), 0.09, 0.45 * m)
    return w, 3 if w >= 0.03 else 2 if w >= 0.012 else 1


def block_mesh(key, sx, sy, sz):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(sx, sz, sy), verts=bm.verts)  # Roblox size -> Blender local axes
    w, seg = bevel_for(min(sx, sy, sz))
    bmesh.ops.bevel(bm, geom=bm.edges[:], offset=w, segments=seg, profile=0.5, affect="EDGES", clamp_overlap=True)
    return finish(key, bm)


def wedge_mesh(key, sx, sy, sz):
    """Roblox WedgePart: full bottom (-y) and back (+z) faces, the slope facing front (-z) and up. Built turned 180°
    about the vertical, because Roblox's importer turns meshes 180° about Y (boxes and cylinders don't show it)."""
    bm = bmesh.new()
    ends = [[bm.verts.new((-x, z, y)) for y, z in ((-sy / 2, -sz / 2), (-sy / 2, sz / 2), (sy / 2, sz / 2))]
            for x in (-sx / 2, sx / 2)]
    bm.faces.new(ends[0][::-1])
    bm.faces.new(ends[1])
    for i in range(3):
        j = (i + 1) % 3
        bm.faces.new((ends[0][i], ends[0][j], ends[1][j], ends[1][i]))
    bm.normal_update()
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    w, seg = bevel_for(min(sx, sy, sz))
    bmesh.ops.bevel(bm, geom=bm.edges[:], offset=w, segments=seg, profile=0.5, affect="EDGES", clamp_overlap=True)
    return finish(key, bm)


def cylinder_mesh(key, length, d):
    sides = 12 if d < 0.15 else 20 if d < 0.5 else 28
    bm = bmesh.new()
    rings = [[bm.verts.new((x, d / 2 * math.cos(a), d / 2 * math.sin(a)))
              for a in (2 * math.pi * i / sides for i in range(sides))] for x in (-length / 2, length / 2)]
    ends = [bm.verts.new((-length / 2, 0, 0)), bm.verts.new((length / 2, 0, 0))]
    for i in range(sides):  # caps as triangle fans: no n-gons
        j = (i + 1) % sides
        bm.faces.new((rings[0][i], rings[0][j], rings[1][j], rings[1][i]))
        bm.faces.new((rings[0][j], rings[0][i], ends[0]))
        bm.faces.new((rings[1][i], rings[1][j], ends[1]))
    bm.normal_update()
    rims = [e for e in bm.edges if e.calc_face_angle(0) > math.radians(40)]
    w, seg = bevel_for(min(length, d))
    bmesh.ops.bevel(bm, geom=rims, offset=w, segments=seg, profile=0.5, affect="EDGES", clamp_overlap=True)
    return finish(key, bm)


def finish(key, bm):
    bmesh.ops.dissolve_degenerate(bm, dist=1e-5, edges=bm.edges[:])
    bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 4])  # bevel corners: no n-gons
    bs.auto_uv(bm)
    me = bpy.data.meshes.new(key)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    me.materials.append(colour((163, 162, 165), "Plastic"))  # the game sets each part's own colour and material
    o = bpy.data.objects.new(key, me)
    bpy.data.collections["StationBevels"].objects.link(o)
    wn = o.modifiers.new("WeightedNormal", "WEIGHTED_NORMAL")
    wn.mode, wn.weight, wn.keep_sharp = "FACE_AREA", 100, True
    with bpy.context.temp_override(object=o, active_object=o, selected_objects=[o]):
        bpy.ops.object.modifier_apply(modifier=wn.name)  # custom normals now live in the mesh, shared by every copy
    return o


def colour(rgb, material):
    name = "BV_%d_%d_%d_%s" % (*rgb, material)
    m = bpy.data.materials.get(name)
    if not m:
        m = bpy.data.materials.new(name)
        col = bs.srgb2lin([c / 255 for c in rgb]) + (1.0,)
        m.diffuse_color = col
        b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
        b.inputs["Base Color"].default_value = col
        b.inputs["Roughness"].default_value = 0.4 if material == "Metal" else 0.8
        b.inputs["Metallic"].default_value = 0.7 if material == "Metal" else 0.0
    return m


def collection(name, parent=None):
    c = bpy.data.collections.get(name)
    if c:
        for o in list(c.objects):
            bpy.data.objects.remove(o, do_unlink=True)
    else:
        c = bpy.data.collections.new(name)
        (parent or bpy.context.scene.collection).children.link(c)
    return c


def build():
    rows = [r for f in sorted(os.listdir(HERE)) if f.endswith("_parts.json")
            for r in json.load(open(os.path.join(HERE, f)))]
    for o in [o for o in bpy.data.objects if o.name in ("Cube", "Camera", "Light")]:
        bpy.data.objects.remove(o, do_unlink=True)  # the startup scene
    collection("StationBevels")
    masters = {}
    for st, name, key, shape, size, cf, rgb, mat in rows:
        if key in masters:
            continue
        if shape == "C":
            masters[key] = cylinder_mesh(key, size[0], min(size[1], size[2]))
        elif shape == "W":
            masters[key] = wedge_mesh(key, *size)
        else:
            masters[key] = block_mesh(key, *size)
    for i, (key, o) in enumerate(sorted(masters.items())):
        o.location = ((i % 10) * 10.0, -40.0 - (i // 10) * 10.0, 0)  # export grid, away from the stations
    review = collection("Stations")
    roots = {}
    for st in dict.fromkeys(r[0] for r in rows):
        roots[st] = bpy.data.objects.new(st, None)  # an empty at the plot origin, so a station can be framed by name
        collection(st, review).objects.link(roots[st])
    for st, name, key, shape, size, cf, rgb, mat in rows:
        x, y, z, *r = cf
        R = C @ Matrix((r[0:3], r[3:6], r[6:9])) @ CI
        if shape == "W":
            R = R @ Matrix.Rotation(math.pi, 3, "Z")  # undo the wedge's import turn for the review copy
        o = bpy.data.objects.new(name, masters[key].data)
        o.parent = roots[st]
        o.matrix_basis = Matrix.Translation(C @ Vector((x, y, z))) @ R.to_4x4()
        o.material_slots[0].link = "OBJECT"
        o.material_slots[0].material = colour(rgb, mat)
        bpy.data.collections[st].objects.link(o)
    tris = {k: sum(len(p.vertices) - 2 for p in o.data.polygons) for k, o in masters.items()}
    print("meshes", len(masters), "parts", len(rows), "triangles placed", sum(tris[r[2]] for r in rows))
    return masters


def export(keys=None, name="StationBevels"):
    exp = bs._skill("export_asset", "blender-export-pipelines")
    pick = dict(objects=sorted(keys)) if keys else dict(collection="StationBevels")
    res = exp.run(preset="roblox", out=os.path.join(HERE, name + ".fbx"), no_anim=True, **pick)
    bpy.ops.object.select_all(action="DESELECT")
    return res


if __name__ == "__main__":
    build()
    export()

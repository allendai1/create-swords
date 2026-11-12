# Festival props for the street, Sell Swords! (2026-11-04; Allen: "if you're going to create models, create them in Blender
# with a low poly style", then "can keep the latnern strings": the food stall and the nobori banner are remade here).
# Low poly, flat shaded. Two collections, each exported to its own FBX:
#   Yatai  - a food stall: a counter on two wheels, a front beam, four posts, a gabled tiled roof with ribs, three
#            indigo noren cloths (a white diamond crest on the middle one), a paper lantern at the front corner, two bowls and a pot on the counter.
#   Yagura - a bon-odori festival tower for the plaza's centre (deck, red-and-white skirt, roof, taiko, lanterns).
#   Handcart - a two-wheeled cart, shafts on the ground, cloth bundles and a crate.
#   LowFence - a 6-stud run of low fence on cut stones (the street's edge across the grass gaps).
#   Nobori - a banner: a pole on a cross foot with a knob, a crossbar at the top, a folded cloth beside the pole and a
#            white band at its top.
#
# Run in Blender (MCP execute_blender_code: exec(open(<this file>).read())) or headless:
#   blender --background --python build_festival.py
# Writes Yatai.fbx, Nobori.fbx, Yagura.fbx, Handcart.fbx and LowFence.fbx (blender-export-pipelines `roblox` preset) next to this file.
#
# Units are studs, Z up, the front faces -Y (Roblox -Z), origin on the floor: the stall's centre, the banner pole's foot.
# One object per Studio material, named for its part; Studio sets each MeshPart's material and colour (the banner's
# Cloth colour per copy).
import math
import os
import sys

import bmesh
import bpy

HERE = "C:/Users/Allen/Documents/Create Swords!/Models/Props/Festival"
SKILLS = "C:/Users/Allen/.claude/plugins/cache/blender-agent-skills/blender-agent-skills/1.1.0/skills"


def fresh_collection(name):
    old = bpy.data.collections.get(name)
    if old:
        for o in list(old.objects):
            bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(old)
    c = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(c)
    return c


def box(size, loc, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.active_object
    o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return o


def cyl(r, depth, loc, rot=(0, 0, 0), verts=8, r2=None):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r2, depth=depth, location=loc, rotation=rot)
    return bpy.context.active_object


def lathe(profile, loc, verts=8):
    """A closed solid of revolution about Z from (radius, z) points, bottom to top (end radii 0 close the caps)."""
    bm = bmesh.new()
    rings = []
    for r, z in profile:
        if r <= 1e-4:
            rings.append([bm.verts.new((loc[0], loc[1], loc[2] + z))])
        else:
            rings.append([bm.verts.new((loc[0] + r * math.cos(2 * math.pi * i / verts), loc[1] + r * math.sin(2 * math.pi * i / verts), loc[2] + z))
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
    me = bpy.data.meshes.new("lathe")
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new("lathe", me)
    bpy.context.scene.collection.objects.link(o)
    return o


def join(objs, name, coll):
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
    for c in ob.users_collection:
        c.objects.unlink(ob)
    coll.objects.link(ob)
    if len(ob.data.uv_layers) == 0:
        ob.data.uv_layers.new(name="UVMap")
    return ob


def gable(length, depth, top, pitch, ribs, thick=0.2):
    """Two tiled slopes, the ridge along X at height `top`, each slope `depth` deep in Y, ribs of tiles down each."""
    out = []
    w = depth / math.cos(pitch)
    for s in (-1, 1):
        cy = s * (w / 2 - 0.15) * math.cos(pitch)
        cz = top - (w / 2 - 0.15) * math.sin(pitch)
        rot = (-s * pitch, 0, 0)
        out.append(box((length, w, thick), (0, cy, cz), rot=rot))
        for k in range(ribs):
            x = (k - (ribs - 1) / 2) * (length - 0.35) / (ribs - 1)
            out.append(box((0.15, w, 0.11), (x, cy + s * math.sin(pitch) * 0.11, cz + math.cos(pitch) * 0.11), rot=rot))
    out.append(box((length + 0.25, 0.38, 0.3), (0, 0, top + 0.06)))
    return out


def build_yatai():
    coll = fresh_collection("Yatai")
    parts = {}
    # counter: a body on a low frame, a plank band across the front, the top overhanging at the front
    wood = [box((4.6, 2.4, 1.8), (0, 0, 1.35)),
            box((4.7, 0.1, 0.22), (0, -1.24, 1.0)), box((4.7, 0.1, 0.22), (0, -1.24, 1.75))]
    parts["Wood"] = join(wood, "Wood", coll)
    dark = [box((4.9, 2.8, 0.2), (0, -0.1, 2.35)),
            box((4.4, 2.2, 0.15), (0, 0, 0.42))]
    for x in (-2.45, 2.45):
        dark.append(cyl(0.75, 0.24, (x, 0.3, 0.75), rot=(0, math.pi / 2, 0), verts=10))
        dark.append(cyl(0.18, 0.4, (x, 0.3, 0.75), rot=(0, math.pi / 2, 0), verts=6))
    for x in (-2.2, 2.2):
        for y in (-1.0, 1.0):
            dark.append(box((0.22, 0.22, 2.5), (x, y, 2.45 + 1.25)))
    dark.append(box((4.62, 0.2, 0.25), (0, -1.0, 4.62)))   # the front beam the noren hang from
    dark.append(box((4.62, 0.2, 0.25), (0, 1.0, 4.62)))
    dark.append(cyl(0.05, 0.5, (2.6, -1.4, 4.45), verts=4))  # the lantern's cord
    parts["Dark"] = join(dark, "Dark", coll)
    parts["Roof"] = join(gable(5.6, 1.85, 5.45, math.radians(28), 9), "Roof", coll)
    # noren: three cloths from the front beam, each with a slight outward kick at the bottom
    tilt = math.radians(-4)
    parts["Noren"] = join([box((1.4, 0.05, 1.0), (x, -1.13, 3.98), rot=(tilt, 0, 0)) for x in (-1.5, 0, 1.5)], "Noren", coll)
    # the shop's crest: a white diamond on the middle cloth (the references' indigo noren with a white mon)
    parts["Crest"] = join([box((0.42, 0.04, 0.42), (0, -1.175, 3.98), rot=(tilt, math.radians(45), 0))], "Crest", coll)
    # a paper lantern hanging at the front corner, dark caps
    parts["Lantern"] = join([lathe([(0, 0), (0.28, 0.02), (0.42, 0.25), (0.42, 0.55), (0.28, 0.78), (0, 0.8)], (2.6, -1.4, 3.42))], "Lantern", coll)
    parts["Dark"] = join([parts["Dark"], cyl(0.22, 0.08, (2.6, -1.4, 3.42), verts=8), cyl(0.22, 0.08, (2.6, -1.4, 4.22), verts=8)], "Dark", coll)
    # bowls and a pot on the counter
    bowls = [lathe([(0, 0), (0.18, 0), (0.33, 0.2), (0.0, 0.2)], (x, y, 2.45)) for x, y in ((-1.2, -0.6), (-0.4, -0.75))]
    bowls.append(lathe([(0, 0), (0.4, 0), (0.48, 0.35), (0.42, 0.55), (0, 0.55)], (1.1, 0.2, 2.45)))
    parts["Bowl"] = join(bowls, "Bowl", coll)
    return coll, parts


def build_nobori():
    coll = fresh_collection("Nobori")
    parts = {}
    pole = [cyl(0.13, 9.5, (0, 0, 4.75), verts=6),
            box((1.3, 0.25, 0.25), (0, 0, 0.125)), box((0.25, 1.3, 0.25), (0, 0, 0.125)),
            lathe([(0, 0), (0.16, 0.05), (0.2, 0.2), (0.12, 0.38), (0, 0.42)], (0, 0, 9.45)),
            box((0.14, 1.55, 0.14), (0, 0.82, 9.15))]
    parts["Pole"] = join(pole, "Pole", coll)
    # the cloth: four vertical strips folded alternately in X, hung from the crossbar beside the pole
    bm = bmesh.new()
    ys = [0.2 + 1.3 * i / 4 for i in range(5)]
    xs = [0.0, 0.07, -0.05, 0.06, 0.0]
    z0, z1 = 3.2, 8.35
    front = [[bm.verts.new((xs[i], ys[i], z)) for z in (z0, z1)] for i in range(5)]
    for i in range(4):
        bm.faces.new((front[i][0], front[i + 1][0], front[i + 1][1], front[i][1]))
    bmesh.ops.solidify(bm, geom=bm.faces[:], thickness=0.05)
    me = bpy.data.meshes.new("Cloth")
    bm.to_mesh(me)
    bm.free()
    cloth = bpy.data.objects.new("Cloth", me)
    bpy.context.scene.collection.objects.link(cloth)
    parts["Cloth"] = join([cloth], "Cloth", coll)
    # the white band across the cloth's top (just proud of both faces)
    # and a white diamond crest across both faces, a third of the way down
    parts["Band"] = join([box((0.2, 1.32, 0.7), (0.01, 0.85, 8.7)),
                          box((0.24, 0.62, 0.62), (0.01, 0.85, 7.1), rot=(math.radians(45), 0, 0))], "Band", coll)
    return coll, parts


def build_yagura():
    """A bon-odori festival tower: four posts, braces, a deck with a railing and a red-and-white skirt, a ladder at the
    front, a gabled tiled roof on the posts, a taiko drum on the deck and paper lanterns under the eaves."""
    coll = fresh_collection("Yagura")
    parts = {}
    H, DECK, TOP = 4, 5.0, 11.2
    wood = []
    for x in (-H, H):
        for y in (-H, H):
            wood.append(box((0.6, 0.6, 9.0), (x, y, 4.5)))
            wood.append(box((0.9, 0.9, 0.3), (x, y, 0.15)))  # foot stones' timber pads
    # X braces on the sides and the back (the front stays open for the ladder)
    L = math.hypot(2 * H, DECK - 0.6)
    a = math.atan2(DECK - 0.6, 2 * H)
    for s in (-1, 1):
        wood.append(box((0.25, L, 0.25), (s * H, 0, (DECK - 0.6) / 2 + 0.3), rot=(a, 0, 0)))
        wood.append(box((0.25, L, 0.25), (s * H, 0, (DECK - 0.6) / 2 + 0.3), rot=(-a, 0, 0)))
    wood.append(box((L, 0.25, 0.25), (0, H, (DECK - 0.6) / 2 + 0.3), rot=(0, a, 0)))
    wood.append(box((L, 0.25, 0.25), (0, H, (DECK - 0.6) / 2 + 0.3), rot=(0, -a, 0)))
    for s in (-1, 1):  # tie beams under the deck
        wood.append(box((2 * H + 0.6, 0.4, 0.4), (0, s * H, DECK - 0.2)))
        wood.append(box((0.4, 2 * H + 0.6, 0.4), (s * H, 0, DECK - 0.2)))
    wood.append(box((2 * H + 1.4, 2 * H + 1.4, 0.35), (0, 0, DECK + 0.175)))
    # railing round the deck, open at the ladder
    rz = DECK + 1.15
    for s in (-1, 1):
        wood.append(box((0.18, 2 * H + 1.3, 0.18), (s * (H + 0.6), 0, rz)))
        wood.append(box((2 * H + 1.3, 0.18, 0.18), (0, H + 0.6, rz)))
        wood.append(box((H - 0.4, 0.18, 0.18), (s * (H / 2 + 0.6), -(H + 0.6), rz)))
    for x in (-H - 0.6, -2.2, -0.9, 0.9, 2.2, H + 0.6):
        for y in (-H - 0.6, H + 0.6):
            if not (y < 0 and -0.9 < x < 0.9):
                wood.append(box((0.16, 0.16, 1.15), (x, y, DECK + 0.35 + 0.55)))
    for y in (-2.2, 0, 2.2):
        for x in (-H - 0.6, H + 0.6):
            wood.append(box((0.16, 0.16, 1.15), (x, y, DECK + 0.35 + 0.55)))
    # ladder up the front
    la = math.atan2(1.8, DECK + 0.35)
    ll = math.hypot(1.8, DECK + 0.35)
    for x in (-0.55, 0.55):
        wood.append(box((0.16, 0.16, ll), (x, -H - 0.7 - 0.9, (DECK + 0.35) / 2), rot=(-la, 0, 0)))
    for k in range(1, 7):
        t = k / 7
        wood.append(box((1.1, 0.12, 0.1), (0, -H - 0.7 - 1.8 * (1 - t), (DECK + 0.35) * t)))
    # drum stand
    wood.append(box((0.2, 1.2, 1.0), (-0.85, 0, DECK + 0.85)))
    wood.append(box((0.2, 1.2, 1.0), (0.85, 0, DECK + 0.85)))
    parts["Wood"] = join(wood, "Wood", coll)
    # skirt: alternating red and white stripes round the deck's edge, hung under it
    red, white = [], []
    n = 10
    for side in range(4):
        for k in range(n):
            u = -H - 0.7 + (2 * H + 1.4) * (k + 0.5) / n
            w = (2 * H + 1.4) / n
            if side == 0:
                b = box((w, 0.06, 1.4), (u, -H - 0.74, DECK - 0.7))
            elif side == 1:
                b = box((w, 0.06, 1.4), (u, H + 0.74, DECK - 0.7))
            elif side == 2:
                b = box((0.06, w, 1.4), (-H - 0.74, u, DECK - 0.7))
            else:
                b = box((0.06, w, 1.4), (H + 0.74, u, DECK - 0.7))
            (red if k % 2 == 0 else white).append(b)
    parts["Maku"] = join(red, "Maku", coll)
    parts["MakuWhite"] = join(white, "MakuWhite", coll)
    parts["Roof"] = join(gable(2 * H + 2.6, H + 1.4, TOP, math.radians(26), 13), "Roof", coll)
    # taiko: a barrel drum lying across the stand, cream skins at the ends
    drum = lathe([(0, -0.8), (0.82, -0.8), (0.98, -0.4), (1.02, 0), (0.98, 0.4), (0.82, 0.8), (0, 0.8)], (0, 0, 0), verts=12)
    drum.rotation_euler = (0, math.pi / 2, 0)
    drum.location = (0, 0, DECK + 1.75)
    parts["Drum"] = join([drum], "Drum", coll)
    parts["Skin"] = join([cyl(0.78, 0.04, (s * 0.81, 0, DECK + 1.75), rot=(0, math.pi / 2, 0), verts=12) for s in (-1, 1)], "Skin", coll)
    # lanterns under the eaves, four along the front and back, three along each side
    lan, caps = [], []
    eave = TOP - (H + 1.4) * math.tan(math.radians(26))
    spots = [(x, s * (H + 0.95)) for x in (-3.3, -1.1, 1.1, 3.3) for s in (-1, 1)] + [(s * (H + 0.95), y) for y in (-2.4, 0, 2.4) for s in (-1, 1)]
    for x, y in spots:
        lan.append(lathe([(0, 0), (0.25, 0.02), (0.38, 0.22), (0.38, 0.5), (0.25, 0.7), (0, 0.72)], (x, y, eave - 1.6)))
        caps.append(cyl(0.2, 0.07, (x, y, eave - 1.6), verts=8))
        caps.append(cyl(0.2, 0.07, (x, y, eave - 0.88), verts=8))
        caps.append(cyl(0.035, 0.75, (x, y, eave - 0.45), verts=4))
    parts["Lantern"] = join(lan, "Lantern", coll)
    parts["Dark"] = join(caps, "Dark", coll)
    return coll, parts


def build_cart():
    """A two-wheeled handcart (daihachi-guruma) with its shafts resting on the ground, three cloth bundles and a crate."""
    coll = fresh_collection("Handcart")
    parts = {}
    wood = [box((2.6, 4.4, 0.2), (0, 0.4, 1.25))]
    for s in (-1, 1):
        wood.append(box((0.15, 4.4, 0.35), (s * 1.25, 0.4, 1.52)))
    wood.append(box((2.6, 0.15, 0.35), (0, 2.55, 1.52)))
    sa = math.atan2(1.05, 2.8)
    sl = math.hypot(1.05, 2.8)
    for s in (-1, 1):
        wood.append(box((0.18, sl, 0.18), (s * 0.85, -1.8 - 1.4, 1.2 - 0.525), rot=(sa, 0, 0)))
    wood.append(box((1.9, 0.18, 0.18), (0, -4.4, 0.25)))
    wood.append(box((0.9, 0.9, 0.8), (0.5, 1.6, 1.75)))  # the crate
    parts["Wood"] = join(wood, "Wood", coll)
    dark = []
    for s in (-1, 1):
        dark.append(cyl(1.15, 0.2, (s * 1.45, 0.4, 1.15), rot=(0, math.pi / 2, 0), verts=12))
        dark.append(cyl(0.25, 0.35, (s * 1.45, 0.4, 1.15), rot=(0, math.pi / 2, 0), verts=6))
    dark.append(cyl(0.09, 3.2, (0, 0.4, 1.15), rot=(0, math.pi / 2, 0), verts=6))
    parts["Dark"] = join(dark, "Dark", coll)
    sacks = []
    for (x, y, z, r) in ((-0.55, -0.6, 1.75, 0.55), (0.5, -0.5, 1.72, 0.5), (-0.4, 0.9, 1.75, 0.55)):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=r, location=(x, y, z))
        o = bpy.context.active_object
        o.scale = (1.0, 1.15, 0.75)
        sacks.append(o)
    parts["Sack"] = join(sacks, "Sack", coll)
    return coll, parts


def build_fence():
    """A 6-stud run of low fence on a stone base: three cut stones, a post at -X, two rails. `EndPost` (the +X post) is
    its own mesh so a row of runs keeps it only on the last one (no doubled posts)."""
    coll = fresh_collection("LowFence")
    parts = {}
    stones = []
    for k, (h, d) in enumerate(((0.95, 0.9), (0.9, 0.92), (0.97, 0.88))):
        stones.append(box((1.98, d, h), (-2 + k * 2, 0, h / 2)))
    parts["Base"] = join(stones, "Base", coll)
    wood = [box((0.36, 0.36, 2.75), (-3, 0, 1.375)), box((0.42, 0.42, 0.12), (-3, 0, 2.81))]
    for z in (1.55, 2.35):
        wood.append(box((6.0, 0.16, 0.24), (0, 0, z)))
    parts["Wood"] = join(wood, "Wood", coll)
    parts["EndPost"] = join([box((0.36, 0.36, 2.75), (3, 0, 1.375)), box((0.42, 0.42, 0.12), (3, 0, 2.81))], "EndPost", coll)
    return coll, parts


def export(name):
    p = os.path.join(SKILLS, "blender-export-pipelines", "scripts")
    if p not in sys.path:
        sys.path.insert(0, p)
    import importlib
    exp = importlib.import_module("export_asset")
    return exp.run(preset="roblox", collection=name, out=os.path.join(HERE, name + ".fbx"), batch=False, no_anim=True)


yatai, yparts = build_yatai()
nobori, nparts = build_nobori()
yagura, gparts = build_yagura()
cart, cparts = build_cart()
fence, fparts = build_fence()
for label, ps in (("Yatai", yparts), ("Nobori", nparts), ("Yagura", gparts), ("Handcart", cparts), ("LowFence", fparts)):
    tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in ps.values())
    print(label, {n: len(o.data.polygons) for n, o in ps.items()}, "tris", tris)

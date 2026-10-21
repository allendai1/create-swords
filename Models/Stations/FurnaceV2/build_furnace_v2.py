# Furnace v2 for Create Swords! (Allen 2026-10-20, reference image: a grey stone furnace with an arched iron door):
# "Build the furnace shell as a simple mesh. Keep the door separate. Use UV-mapped textures for the stone blocks
# and mortar, with a normal map for shallow depth. Do not model individual bricks."
#
# Run headless:  blender --background --python build_furnace_v2.py
# Writes, next to this script: FurnaceV2.blend, FurnaceV2.fbx (Roblox preset), Textures/furnace_v2_color.png and
# furnace_v2_normal.png (1024 px, OpenGL normal), review/*.png, qa.json.
#
# Units are studs, Z up, front faces -Y, origin on the floor under the centre (project convention).
#   Furnace_Shell: one mesh (plinth, tapered body with an arched recess and a raised arch band, sloped hood, neck,
#                  two posts and a chimney cap). Unique UVs in 0-1 carry the baked stone texture.
#   Furnace_Door:  a separate mesh (arched iron door, strap hinges, rivets, ring handle, glowing slot), its origin
#                  on the hinge line so it can swing.
# The stone is never modelled: a procedural stone surface (no block or mortar lines), laid in studs along each face
# (TileUV), is baked into the colour map, and its chisel facets, grain and pits into the normal map.
import math
import os
import sys
import json
import bpy
import bmesh
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, "Textures")
REVIEW = os.path.join(HERE, "review")
SKILLS = "C:/Users/Allen/.claude/plugins/cache/blender-agent-skills/blender-agent-skills/1.1.0/skills"
TEX_SIZE = 1024                      # Roblox SurfaceAppearance maximum

# ---------------------------------------------------------------- dimensions (studs)
PLINTH = dict(w=5.2, d=4.4, h=0.7)
BODY_Z0, BODY_Z1 = 0.65, 3.6         # 0.05 into the plinth
BODY_BOTTOM = (-2.0, 2.0, -1.7, 1.7)  # x0, x1, y0, y1 (front face vertical at y -1.7)
BODY_TOP = (-1.8, 1.8, -1.7, 1.4)
HOOD_Z0, HOOD_Z1 = 3.55, 4.85        # starts 0.05 inside the body: a ledge, then slopes in
HOOD_BOTTOM = (-1.95, 1.95, -1.85, 1.55)
HOOD_TOP = (-1.15, 1.15, -0.95, 0.65)
NECK = dict(x=(-1.2, 1.2), y=(-1.0, 0.7), z=(4.8, 5.2))
POSTS_X, POST = (-0.85, 0.85), dict(w=0.4, y=(-0.8, 0.5), z=(5.15, 5.65))
CAP = dict(x=(-1.5, 1.5), y=(-1.25, 0.95), z=(5.6, 6.05))
OPEN = dict(w=2.0, z0=0.75, zs=2.45, rise=0.4, depth=0.22)   # arched recess in the body front (y = -1.7)
FRONT_Y = -1.7


def srgb(c):
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c)


# ---------------------------------------------------------------- scene
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = "NONE"
    w = bpy.data.worlds.new("World")
    sc.world = w
    return sc


def new_object(name, bm, coll):
    me = bpy.data.meshes.new(name)
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    coll.objects.link(o)
    return o


# ---------------------------------------------------------------- bmesh pieces
def bm_rect_frustum(bm, z0, z1, bottom, top):
    """Closed six-sided solid between two axis-aligned rectangles (x0, x1, y0, y1) at heights z0 and z1."""
    def ring(r, z):
        x0, x1, y0, y1 = r
        return [bm.verts.new(p) for p in ((x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z))]
    a, b = ring(bottom, z0), ring(top, z1)
    bm.faces.new(a[::-1])
    bm.faces.new(b)
    for i in range(4):
        j = (i + 1) % 4
        bm.faces.new((a[i], a[j], b[j], b[i]))


def bm_box(bm, x, y, z):
    bm_rect_frustum(bm, z[0], z[1], (x[0], x[1], y[0], y[1]), (x[0], x[1], y[0], y[1]))


def arch_outline(w, z0, zs, rise, n=10, cx=0.0):
    """Arched opening outline in the XZ plane, counter-clockwise seen from -Y: flat bottom at z0, straight sides up
    to zs, a segmental arch rising `rise` above zs."""
    c = w / 2
    R = (c * c + rise * rise) / (2 * rise)
    zc = zs + rise - R
    a0 = math.asin(c / R)
    pts = [(cx - c, z0), (cx + c, z0)]
    for k in range(n + 1):
        a = -a0 + 2 * a0 * k / n          # right to left across the top
        pts.append((cx + R * math.sin(-a), zc + R * math.cos(a)))
    return pts, (R, zc, a0)


def bm_prism_xz(bm, pts, y0, y1):
    """Extrude a convex XZ outline from y0 to y1 (y0 < y1); caps triangulated."""
    a = [bm.verts.new((x, y0, z)) for x, z in pts]
    b = [bm.verts.new((x, y1, z)) for x, z in pts]
    f0 = bm.faces.new(a)
    f1 = bm.faces.new(b[::-1])
    n = len(pts)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((a[j], a[i], b[i], b[j]))
    bmesh.ops.triangulate(bm, faces=[f0, f1])


def bm_arc_band(bm, R0, R1, zc, a0, y0, y1, n=12, cx=0.0):
    """Curved band between radii R0 < R1 around (cx, zc) over angles -a0..a0 from vertical, y0..y1 deep; quad strips
    only, so the concave outline never triangulates badly."""
    rows = []
    for k in range(n + 1):
        a = -a0 + 2 * a0 * k / n
        s, c = math.sin(a), math.cos(a)
        rows.append([bm.verts.new((cx + R * s, y, zc + R * c)) for R, y in ((R0, y0), (R1, y0), (R1, y1), (R0, y1))])
    for r, q in zip(rows, rows[1:]):
        for i in range(4):
            j = (i + 1) % 4
            bm.faces.new((r[i], q[i], q[j], r[j]))
    bm.faces.new(rows[0])
    bm.faces.new(rows[-1][::-1])


def bm_sphere(bm, centre, r, segs=8, rings=4):
    res = bmesh.ops.create_uvsphere(bm, u_segments=segs, v_segments=rings, radius=r)
    bmesh.ops.translate(bm, verts=res["verts"], vec=Vector(centre))


def bm_cyl_y(bm, centre, r, length, sides=8):
    """Cylinder along Y, from centre.y - length to centre.y (sticks out toward -Y)."""
    res = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=True, segments=sides, radius1=r, radius2=r, depth=length)
    bmesh.ops.rotate(bm, verts=res["verts"], cent=(0, 0, 0), matrix=Matrix.Rotation(math.radians(90), 3, "X"))
    bmesh.ops.translate(bm, verts=res["verts"], vec=Vector(centre) + Vector((0, -length / 2, 0)))


def bm_cyl_z(bm, centre, r, h, sides=8):
    res = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=True, segments=sides, radius1=r, radius2=r, depth=h)
    bmesh.ops.translate(bm, verts=res["verts"], vec=Vector(centre))


def bm_torus_xz(bm, centre, R, r, segs=12, tube=6):
    """Ring standing in the XZ plane (a door knocker), centred at `centre`."""
    grid = []
    for i in range(segs):
        u = 2 * math.pi * i / segs
        ring = []
        for j in range(tube):
            v = 2 * math.pi * j / tube
            rr = R + r * math.cos(v)
            ring.append(bm.verts.new(Vector(centre) + Vector((rr * math.cos(u), r * math.sin(v), rr * math.sin(u)))))
        grid.append(ring)
    for i in range(segs):
        for j in range(tube):
            a, b = grid[i][j], grid[(i + 1) % segs][j]
            c, d = grid[(i + 1) % segs][(j + 1) % tube], grid[i][(j + 1) % tube]
            bm.faces.new((a, b, c, d))


def bevel(o, width, segments=3):
    """Rounded edges (Allen 2026-10-20: "can you smooth out the bevels"): 3 segments, round profile."""
    m = o.modifiers.new("Bevel", "BEVEL")
    m.width, m.segments, m.limit_method, m.angle_limit = width, segments, "ANGLE", math.radians(30)
    m.profile = 0.5
    m.harden_normals = False
    apply_modifiers(o)


def smooth_shade(o, angle):
    """Smooth across rounded bevels and curved parts, sharp where faces meet at more than `angle` degrees (the door
    recess, real corners); weighted normals keep the big flat faces flat."""
    me = o.data
    for poly in me.polygons:
        poly.use_smooth = True
    me.set_sharp_from_angle(angle=math.radians(angle))
    m = o.modifiers.new("WeightedNormals", "WEIGHTED_NORMAL")
    m.keep_sharp = True
    m.mode = "FACE_AREA"
    apply_modifiers(o)


def apply_modifiers(o):
    with bpy.context.temp_override(object=o, active_object=o, selected_objects=[o], selected_editable_objects=[o]):
        for m in list(o.modifiers):
            bpy.ops.object.modifier_apply(modifier=m.name)


def smart_unwrap(o, margin, scale_to_bounds=False):
    """Smart UV Project on the whole mesh (headless-safe: makes `o` the active, only selected object)."""
    vl = bpy.context.view_layer
    for ob in vl.objects:
        ob.select_set(False)
    vl.objects.active = o
    o.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(50), island_margin=margin, area_weight=0.0, correct_aspect=True,
                             scale_to_bounds=scale_to_bounds)
    bpy.ops.object.mode_set(mode="OBJECT")


def join(objs, name):
    with bpy.context.temp_override(active_object=objs[0], selected_editable_objects=objs, selected_objects=objs):
        bpy.ops.object.join()
    objs[0].name = objs[0].data.name = name
    return objs[0]


# ---------------------------------------------------------------- shell
def build_shell(coll):
    parts = []

    def piece(name, fill, bevel_w, part=0):
        bm = bmesh.new()
        fill(bm)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        tag = bm.faces.layers.int.new("part")   # 1 = arch band (its stone shifted in unwrap_shell)
        for f in bm.faces:
            f[tag] = part
        o = new_object(name, bm, coll)
        if bevel_w:
            bevel(o, bevel_w)
        parts.append(o)
        return o

    p = PLINTH
    piece("Plinth", lambda bm: bm_box(bm, (-p["w"] / 2, p["w"] / 2), (-p["d"] / 2, p["d"] / 2), (0, p["h"])), 0.12)
    body = piece("Body", lambda bm: bm_rect_frustum(bm, BODY_Z0, BODY_Z1, BODY_BOTTOM, BODY_TOP), 0.08)
    piece("Hood", lambda bm: bm_rect_frustum(bm, HOOD_Z0, HOOD_Z1, HOOD_BOTTOM, HOOD_TOP), 0.08)
    piece("Neck", lambda bm: bm_box(bm, NECK["x"], NECK["y"], NECK["z"]), 0.06)
    for i, px in enumerate(POSTS_X):
        piece(f"Post{i}", lambda bm, px=px: bm_box(bm, (px - POST["w"] / 2, px + POST["w"] / 2), POST["y"], POST["z"]), 0.05)
    piece("Cap", lambda bm: bm_box(bm, CAP["x"], CAP["y"], CAP["z"]), 0.12)

    # arched recess for the door: boolean a prism out of the body front
    o = OPEN
    pts, (R, zc, a0) = arch_outline(o["w"], o["z0"], o["zs"], o["rise"])
    bm = bmesh.new()
    bm_prism_xz(bm, pts, FRONT_Y - 0.5, FRONT_Y + o["depth"])
    cutter = new_object("RecessCutter", bm, coll)
    m = body.modifiers.new("Recess", "BOOLEAN")
    m.operation, m.solver, m.object = "DIFFERENCE", "EXACT", cutter
    apply_modifiers(body)
    bpy.data.objects.remove(cutter)

    # raised arch band above the opening, sunk 0.1 into the face, standing 0.08 proud
    piece("ArchBand", lambda bm: bm_arc_band(bm, R + 0.1, R + 0.3, zc, a0 * 1.12, FRONT_Y - 0.08, FRONT_Y + 0.1), 0.04, part=1)

    shell = join(parts, "Furnace_Shell")
    smooth_shade(shell, 40)
    bm = bmesh.new()
    bm.from_mesh(shell.data)
    bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 4])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(shell.data)
    bm.free()
    return shell


def unwrap_shell(shell):
    """UVMap: unique islands in 0-1 (what the baked maps use). TileUV: each face laid out in studs along its own
    horizontal tangent and up-slope bitangent, so blocks keep one size and run level on every face."""
    me = shell.data
    smart_unwrap(shell, 0.006, scale_to_bounds=True)
    me.uv_layers[0].name = "UVMap"
    tile = me.uv_layers.new(name="TileUV")
    for poly in me.polygons:
        n = poly.normal
        t = Vector((0, 0, 1)).cross(n)
        t = Vector((1, 0, 0)) if t.length < 1e-4 else t.normalized()
        b = n.cross(t).normalized()
        if b.z < 0 or (abs(b.z) < 1e-4 and b.y < 0):
            b = -b
        for li in poly.loop_indices:
            p = me.vertices[me.loops[li].vertex_index].co
            tile.data[li].uv = (p.dot(t), p.dot(b))
    # the arch band: shifted, so its stone doesn't repeat the wall's right behind it (which reads as see-through)
    part = me.attributes["part"].data
    for poly in me.polygons:
        if part[poly.index].value == 1:
            for li in poly.loop_indices:
                tile.data[li].uv = (tile.data[li].uv[0] + 3.7, tile.data[li].uv[1] + 2.1)
    me.attributes.remove(me.attributes["part"])
    me.uv_layers.active = me.uv_layers["UVMap"]
    me.uv_layers["UVMap"].active_render = True


def stone_source_material():
    """Procedural stone with no block or mortar lines (Allen 2026-10-20: "give it a stone texture", then "without
    the brick lines"): two greys blended by broad cloudy noise, finer stains and granite speckle, laid in studs along
    TileUV. Height (for the baked normal map): soft chisel facets, fine grain and pitting, kept shallow."""
    m = bpy.data.materials.new("m_src_furnace_stone")
    m.use_nodes = True
    nt = m.node_tree
    nodes, links = nt.nodes, nt.links
    bsdf = next(n for n in nodes if n.type == "BSDF_PRINCIPLED")

    def node(kind, **inputs):
        n = nodes.new(kind)
        for k, v in inputs.items():
            n.inputs[k].default_value = v
        return n

    def math_node(op, a, b=None):
        n = nodes.new("ShaderNodeMath")
        n.operation = op
        for i, v in enumerate((a, b)):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                n.inputs[i].default_value = v
            else:
                links.new(v, n.inputs[i])
        return n.outputs[0]

    def noise(scale, detail, rough=0.5, kind="ShaderNodeTexNoise"):
        n = node(kind, Scale=scale) if kind != "ShaderNodeTexNoise" else node(kind, Scale=scale, Detail=detail, Roughness=rough)
        links.new(uv.outputs["UV"], n.inputs["Vector"])
        return n

    uv = nodes.new("ShaderNodeUVMap")
    uv.uv_map = "TileUV"
    # colour: two stone greys blended by broad clouds, then finer stains and granite speckle
    clouds = noise(0.7, 4.0)
    tone = nodes.new("ShaderNodeMix"); tone.data_type = "RGBA"
    tone.inputs["A"].default_value = srgb((0.35, 0.35, 0.37)) + (1,)
    tone.inputs["B"].default_value = srgb((0.46, 0.45, 0.44)) + (1,)
    clouds_f = nodes.new("ShaderNodeMapRange")
    clouds_f.inputs["From Min"].default_value, clouds_f.inputs["From Max"].default_value = 0.3, 0.7
    links.new(clouds.outputs["Fac"], clouds_f.inputs["Value"])
    links.new(clouds_f.outputs["Result"], tone.inputs["Factor"])
    # stone tints (Allen 2026-10-20: "add some coloring", "Stone tints"): warm sandy and cool bluish patches,
    # blended through the grey by their own broad clouds, and a few faint mossy-green patches
    hue = noise(0.6, 3.0)
    hue_f = nodes.new("ShaderNodeMapRange")
    hue_f.inputs["From Min"].default_value, hue_f.inputs["From Max"].default_value = 0.25, 0.75
    links.new(hue.outputs["Fac"], hue_f.inputs["Value"])
    tint = nodes.new("ShaderNodeMix"); tint.data_type = "RGBA"
    tint.inputs["A"].default_value = srgb((0.36, 0.39, 0.45)) + (1,)    # cool blue-grey
    tint.inputs["B"].default_value = srgb((0.50, 0.45, 0.39)) + (1,)    # warm sand
    links.new(hue_f.outputs["Result"], tint.inputs["Factor"])
    tinted = nodes.new("ShaderNodeMix"); tinted.data_type = "RGBA"
    tinted.inputs["Factor"].default_value = 0.42   # clear warm and cool patches; it still reads as grey stone
    links.new(tone.outputs["Result"], tinted.inputs["A"])
    links.new(tint.outputs["Result"], tinted.inputs["B"])
    moss = noise(1.8, 4.0)
    moss_f = nodes.new("ShaderNodeMapRange")                             # only the noise's highest peaks
    moss_f.inputs["From Min"].default_value, moss_f.inputs["From Max"].default_value = 0.62, 0.75
    moss_f.inputs["To Max"].default_value = 0.3
    links.new(moss.outputs["Fac"], moss_f.inputs["Value"])
    mossy = nodes.new("ShaderNodeMix"); mossy.data_type = "RGBA"
    mossy.inputs["B"].default_value = srgb((0.36, 0.42, 0.30)) + (1,)
    links.new(moss_f.outputs["Result"], mossy.inputs["Factor"])
    links.new(tinted.outputs["Result"], mossy.inputs["A"])
    stains = noise(2.2, 6.0, 0.6)
    stain_f = nodes.new("ShaderNodeMapRange")
    stain_f.inputs["From Min"].default_value, stain_f.inputs["From Max"].default_value = 0.35, 0.7
    stain_f.inputs["To Min"].default_value, stain_f.inputs["To Max"].default_value = 0.9, 1.06
    links.new(stains.outputs["Fac"], stain_f.inputs["Value"])
    speck = noise(55.0, 0, kind="ShaderNodeTexVoronoi")
    speck_f = nodes.new("ShaderNodeMapRange")
    speck_f.inputs["To Min"].default_value, speck_f.inputs["To Max"].default_value = 0.82, 1.1
    links.new(speck.outputs["Color"], speck_f.inputs["Value"])   # a random value per fleck
    shade = math_node("MULTIPLY", stain_f.outputs["Result"], speck_f.outputs["Result"])
    mul = nodes.new("ShaderNodeMix"); mul.data_type = "RGBA"; mul.blend_type = "MULTIPLY"
    mul.inputs["Factor"].default_value = 1.0
    links.new(mossy.outputs["Result"], mul.inputs["A"])
    links.new(shade, mul.inputs["B"])
    links.new(mul.outputs["Result"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.9

    # height: soft chisel facets, fine grain and small pits
    facets = noise(3.0, 0, kind="ShaderNodeTexVoronoi")
    grain = noise(18.0, 4.0)
    pits = noise(30.0, 0, kind="ShaderNodeTexVoronoi")
    pit = math_node("POWER", pits.outputs["Distance"], 0.35)             # sharp little craters
    height = math_node("ADD", math_node("MULTIPLY", facets.outputs["Distance"], 0.25),
                       math_node("ADD", math_node("MULTIPLY", grain.outputs["Fac"], 0.12), math_node("MULTIPLY", pit, 0.1)))
    bump = node("ShaderNodeBump", Strength=1.0, Distance=0.03)
    links.new(height, bump.inputs["Height"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return m


def bake_stone(shell, sc):
    os.makedirs(TEX, exist_ok=True)
    src = stone_source_material()
    shell.data.materials.clear()
    shell.data.materials.append(src)
    sc.render.engine = "CYCLES"
    sc.cycles.samples = 16
    sc.cycles.device = "CPU"
    bake = sc.render.bake
    bake.margin = TEX_SIZE // 64
    images = {}
    for kind, colorspace in (("color", "sRGB"), ("normal", "Non-Color")):
        img = bpy.data.images.new(f"furnace_v2_{kind}", TEX_SIZE, TEX_SIZE, alpha=False)
        img.colorspace_settings.name = colorspace
        node = src.node_tree.nodes.new("ShaderNodeTexImage")
        node.image = img
        src.node_tree.nodes.active = node
        for o in sc.objects:
            o.hide_render = o is not shell
        with bpy.context.temp_override(object=shell, active_object=shell, selected_objects=[shell], selected_editable_objects=[shell]):
            if kind == "color":
                bpy.ops.object.bake(type="DIFFUSE", pass_filter={"COLOR"}, use_clear=True, margin=bake.margin)
            else:
                bpy.ops.object.bake(type="NORMAL", normal_space="TANGENT", use_clear=True, margin=bake.margin)
        img.filepath_raw = os.path.join(TEX, f"furnace_v2_{kind}.png")
        img.file_format = "PNG"
        img.save()
        src.node_tree.nodes.remove(node)
        images[kind] = img
    for o in sc.objects:
        o.hide_render = False
    # final material: just the baked images (what the FBX and Roblox SurfaceAppearance carry)
    m = bpy.data.materials.new("m_furnace_v2_stone")
    m.use_nodes = True
    nt = m.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    col = nt.nodes.new("ShaderNodeTexImage"); col.image = images["color"]
    nrm_img = nt.nodes.new("ShaderNodeTexImage"); nrm_img.image = images["normal"]
    nmap = nt.nodes.new("ShaderNodeNormalMap"); nmap.uv_map = "UVMap"
    nt.links.new(col.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(nrm_img.outputs["Color"], nmap.inputs["Color"])
    nt.links.new(nmap.outputs["Normal"], bsdf.inputs["Normal"])
    bsdf.inputs["Roughness"].default_value = 0.85
    shell.data.materials.clear()
    shell.data.materials.append(m)
    shell.data.uv_layers.remove(shell.data.uv_layers["TileUV"])   # bake-only; the game needs just UVMap
    bpy.data.materials.remove(src)


# ---------------------------------------------------------------- door
def flat_material(name, rgb, emit=0.0, rough=0.6, metal=0.6):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    c = srgb(rgb) + (1,)
    b.inputs["Base Color"].default_value = c
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = c
        b.inputs["Emission Strength"].default_value = emit
    m.diffuse_color = c
    return m


def build_door(coll):
    """Arched iron door in the recess, 0.08 behind the body front, never touching the shell. Built in place, then
    its origin moves to the hinge line (left edge, bottom) so the game can swing it."""
    o = OPEN
    yf = FRONT_Y + 0.08                       # door front face
    yb = yf + 0.1                             # door back (recess back is FRONT_Y + 0.22)
    pts, (R, zc, a0) = arch_outline(o["w"] - 0.12, o["z0"] + 0.03, o["zs"] - 0.02, o["rise"] - 0.03)
    x0 = -(o["w"] - 0.12) / 2
    iron, strap, glow = (flat_material("m_furnace_v2_iron", (0.20, 0.20, 0.22)),
                         flat_material("m_furnace_v2_strap", (0.32, 0.32, 0.34), rough=0.45),
                         flat_material("m_furnace_v2_glow", (1.0, 0.38, 0.04), emit=6.0, metal=0.0))
    parts = []

    def piece(name, fill, mat, bevel_w=0.0):
        bm = bmesh.new()
        fill(bm)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        ob = new_object(name, bm, coll)
        ob.data.materials.append(mat)
        if bevel_w:
            bevel(ob, bevel_w)
        parts.append(ob)

    piece("Panel", lambda bm: bm_prism_xz(bm, pts, yf, yb), iron, 0.03)
    # a raised rim inside the edge: a slightly smaller arch, 0.03 proud of the panel
    rim, _ = arch_outline(o["w"] - 0.32, o["z0"] + 0.13, o["zs"] - 0.08, o["rise"] - 0.08)
    inner, _ = arch_outline(o["w"] - 0.44, o["z0"] + 0.19, o["zs"] - 0.12, o["rise"] - 0.11)
    piece("RimOuter", lambda bm: bm_prism_xz(bm, rim, yf - 0.03, yf + 0.02), strap, 0.01)
    piece("RimInner", lambda bm: bm_prism_xz(bm, inner, yf - 0.035, yf + 0.015), iron, 0.0)
    # glowing slot in an iron frame
    zs = 1.85
    piece("SlotFrame", lambda bm: bm_box(bm, (-0.5, 0.5), (yf - 0.07, yf + 0.01), (zs - 0.16, zs + 0.16)), strap, 0.02)
    piece("Glow", lambda bm: bm_box(bm, (-0.42, 0.42), (yf - 0.08, yf - 0.05), (zs - 0.09, zs + 0.09)), glow)
    # strap hinges (pointed), knuckles on the hinge line, rivets
    for hz in (1.15, 2.25):
        strap_pts = [(x0 + 0.02, hz - 0.08), (x0 + 0.62, hz - 0.08), (x0 + 0.74, hz), (x0 + 0.62, hz + 0.08), (x0 + 0.02, hz + 0.08)]
        piece("Strap", lambda bm, sp=strap_pts: bm_prism_xz(bm, sp, yf - 0.075, yf + 0.01), strap)
        piece("Knuckle", lambda bm, hz=hz: bm_cyl_z(bm, (x0 + 0.02, yf - 0.02, hz), 0.055, 0.3), strap)
        for rx in (x0 + 0.22, x0 + 0.55):
            piece("Rivet", lambda bm, rx=rx, hz=hz: bm_sphere(bm, (rx, yf - 0.075, hz), 0.04), strap)
    for rx, rz in ((-0.05, 2.62), (-0.05, 1.08), (0.62, 2.4), (0.62, 1.3), (-0.3, 2.5), (0.3, 2.5)):
        piece("Rivet", lambda bm, rx=rx, rz=rz: bm_sphere(bm, (rx, yf - 0.035, rz), 0.045), strap)
    # ring handle on a boss
    piece("Boss", lambda bm: bm_cyl_y(bm, (0.68, yf + 0.01, 1.62), 0.06, 0.07), strap)          # 0.01 into the panel
    piece("Ring", lambda bm: bm_torus_xz(bm, (0.68, yf - 0.065, 1.48), 0.13, 0.025, segs=16, tube=8), strap)     # hangs through the boss
    door = join(parts, "Furnace_Door")
    smooth_shade(door, 50)
    # origin on the hinge line
    hinge = Vector((x0 + 0.02, yf, o["z0"] + 0.03))
    door.data.transform(Matrix.Translation(-hinge))
    door.location = hinge
    smart_unwrap(door, 0.01)
    return door


# ---------------------------------------------------------------- review
def review(sc, objs):
    os.makedirs(REVIEW, exist_ok=True)
    for eng in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        try:
            sc.render.engine = eng
            break
        except TypeError:
            pass
    sc.view_settings.view_transform = "Standard"
    w = sc.world
    w.use_nodes = True
    bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs[0].default_value = srgb((0.82, 0.82, 0.84)) + (1,)
    bg.inputs[1].default_value = 0.9
    sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN"))
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(50), 0, math.radians(-35))
    sc.collection.objects.link(sun)
    fill = bpy.data.objects.new("Fill", bpy.data.lights.new("Fill", "AREA"))
    fill.data.energy, fill.data.size = 400, 6
    fill.location = (-6, -6, 5)
    fill.rotation_euler = (math.radians(60), 0, math.radians(-45))
    sc.collection.objects.link(fill)
    glow = bpy.data.objects.new("DoorGlow", bpy.data.lights.new("DoorGlow", "POINT"))
    glow.data.energy, glow.data.color = 60, (1.0, 0.55, 0.2)
    glow.location = (0, FRONT_Y - 0.6, 1.0)
    sc.collection.objects.link(glow)
    ground = bpy.data.meshes.new("Ground")
    ground.from_pydata([(-30, -30, -0.002), (30, -30, -0.002), (30, 30, -0.002), (-30, 30, -0.002)], [], [(0, 1, 2, 3)])
    g = bpy.data.objects.new("Ground", ground)
    gm = flat_material("m_review_ground", (0.80, 0.80, 0.82), rough=1.0, metal=0.0)
    ground.materials.append(gm)
    sc.collection.objects.link(g)
    cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = 1200, 1100
    shots = {"front_three_quarter": ((0.55, -1, 0.35), 13, (0, 0, 3.0), 50),
             "door_close": ((0.15, -1, 0.15), 5.2, (0, FRONT_Y, 1.8), 50),
             "back_three_quarter": ((-0.7, 1, 0.4), 13, (0, 0, 3.0), 50),
             "top": ((0.2, -0.5, 1), 13, (0, 0, 3.0), 50)}
    out = []
    for name, (d, dist, target, lens) in shots.items():
        cam.data.lens = lens
        t = Vector(target)
        cam.location = t + Vector(d).normalized() * dist
        cam.rotation_euler = (t - cam.location).to_track_quat("-Z", "Y").to_euler()
        sc.render.filepath = os.path.join(REVIEW, f"furnace_v2_{name}.png")
        bpy.ops.render.render(write_still=True)
        out.append(sc.render.filepath)
    for ob in (sun, fill, glow, g, cam):
        bpy.data.objects.remove(ob)
    return out


def skill(module, sub):
    import importlib
    p = os.path.join(SKILLS, sub, "scripts")
    if p not in sys.path:
        sys.path.insert(0, p)
    return importlib.reload(importlib.import_module(module))


def export_door_parts(door):
    """FurnaceDoor.fbx for the game's current forges (Allen 2026-10-20: "edit our current forge in studio to have the
    same door"): the door alone, split by material into FurnaceDoor_iron / _strap / _glow, so the game can light the
    window only while an ingot heats. Returns each part's bounding-box centre in furnace space, for seating it."""
    coll = bpy.data.collections.new("FurnaceDoor")
    bpy.context.scene.collection.children.link(coll)
    root = bpy.data.objects.new("FurnaceDoor", None)
    coll.objects.link(root)
    copy = door.copy()
    copy.data = door.data.copy()
    copy.parent = None
    copy.matrix_world = door.matrix_world.copy()
    coll.objects.link(copy)
    vl = bpy.context.view_layer
    for ob in vl.objects:
        ob.select_set(False)
    vl.objects.active = copy
    copy.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.separate(type="MATERIAL")
    bpy.ops.object.mode_set(mode="OBJECT")
    centres = {}
    for ob in [o for o in coll.objects if o.type == "MESH"]:
        ob.name = ob.data.name = "FurnaceDoor_" + ob.data.materials[0].name.replace("m_furnace_v2_", "")
        ob.parent = root
        ob.matrix_parent_inverse.identity()
        pts = [ob.matrix_world @ v.co for v in ob.data.vertices]
        centres[ob.name] = [round((min(p[k] for p in pts) + max(p[k] for p in pts)) / 2, 4) for k in range(3)]
    result = skill("export_asset", "blender-export-pipelines").run(
        preset="roblox", collection="FurnaceDoor", out=os.path.join(HERE, "FurnaceDoor.fbx"), batch=False, no_anim=True)
    for ob in list(coll.objects):
        bpy.data.objects.remove(ob)
    bpy.data.collections.remove(coll)
    return {"centres": centres, "export": result}


def main():
    sc = reset()
    coll = bpy.data.collections.new("FurnaceV2")
    sc.collection.children.link(coll)
    root = bpy.data.objects.new("FurnaceV2", None)
    coll.objects.link(root)
    shell = build_shell(coll)
    unwrap_shell(shell)
    bake_stone(shell, sc)
    door = build_door(coll)
    for ob in (shell, door):
        ob.parent = root
    report = {"triangles": {o.name: sum(len(p.vertices) - 2 for p in o.data.polygons) for o in (shell, door)}}
    try:
        report["qa"] = skill("qa_check", "blender-asset-qa").run(objects=[shell.name, door.name], profile="roblox")
    except Exception as e:  # noqa: BLE001 - record and carry on, the review still runs
        report["qa_error"] = repr(e)
    report["renders"] = review(sc, (shell, door))
    try:
        report["export"] = skill("export_asset", "blender-export-pipelines").run(
            preset="roblox", collection="FurnaceV2", out=os.path.join(HERE, "FurnaceV2.fbx"), batch=False, no_anim=True)
    except Exception as e:  # noqa: BLE001
        report["export_error"] = repr(e)
    try:
        report["door_parts"] = export_door_parts(door)
    except Exception as e:  # noqa: BLE001
        report["door_parts_error"] = repr(e)
    bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, "FurnaceV2.blend"))
    with open(os.path.join(HERE, "qa.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str)
    print("FURNACE_V2_DONE", json.dumps(report["triangles"]))


main()

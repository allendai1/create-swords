# Anvil v2 for Create Swords! (Allen 2026-10-22, reference: References/Anvil/anvil-sheet-v1.webp): a stylized,
# hand-painted blue-grey steel anvil. Horn, working face, waist and proportions follow the sheet; the sheet's stone
# blocks, wooden pedestal and gold trim are left out on purpose ("preserve the original's integrated metal base"),
# so the body flares into four broad metal feet instead.
#
# Run headless:  blender --background --python build_anvil_v2.py
# Writes, next to this script: AnvilV2.blend, AnvilV2.fbx (Roblox preset), AnvilV2.glb, Textures/anvil_v2_color.png
# (1024 px painted colour map), review/anvil_v2_*.png (seven views of this mesh), qa.json.
# Then:  python contact_sheet.py   (review/anvil_v2_sheet.png, the views beside the reference)
#
# Units are studs, Z up, front faces -Y, origin on the floor under the waist (project convention). The horn points
# to -X like AnvilHorned (the blade mount's end), the heel with the hardy hole to +X. Working face top at 2.3 studs,
# the same ANVIL_TOP as the current station.
#
# Form: ONE subdivision cage. A vertical loft of rounded-rectangle outlines (feet -> waist -> head), whose -X end
# patch is extruded into the horn and +X end patch into the heel, then Subdivision level 2, the hardy hole cut by a
# boolean, and decimated to the triangle budget. Close support loops keep the face, horn and heel edges crisp while
# the head-to-waist and waist-to-feet transitions stay broad and soft.
# Paint: a procedural "hand-painted" surface (light top planes, darker undersides and recesses, broad lavender and
# grey patches, edge highlights broken up by noise, sparse scratches and scuffs) baked as emission into one colour
# map, so the look comes from the texture, not from Blender's lighting. The final material is just that image.
import json
import math
import os
import random
import sys

import bmesh
import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, "Textures")
REVIEW = os.path.join(HERE, "review")
SKILLS = "C:/Users/Allen/.claude/plugins/cache/blender-agent-skills/blender-agent-skills/1.1.0/skills"
TEX_SIZE = 1024                      # Roblox SurfaceAppearance maximum
TRI_TARGET = 10000

# ---------------------------------------------------------------- dimensions (studs)
TOP = 2.3                            # working face, = ANVIL_TOP
HEAD_HX, HEAD_HY = 1.25, 0.64        # head half length / half width (face 2.5 x 1.28, heel adds 0.55)
HEAD_BOTTOM = 1.5
HEEL_BOTTOM = 1.9
HORN_LEN = 1.3                       # tip at x = -2.59
HOLE = dict(x=1.53, half=0.1, bottom=2.06)   # square hardy hole in the heel
LOBES = (1.0, 0.9, 1.08, 0.94)
ARCH = 0.17                          # height of the arch between two feet       # per-foot size: a little uneven, so the base reads hand-made
# outline counts: 3 points per corner arc, 5 on each long side, 3 on each short side (28 per ring)
C_ARC, L_SIDE, S_SIDE = 3, 5, 3
# rings bottom to top: z, half x, half y, corner radius, notch (arch between feet), lobe (feet push out)
RINGS = [
    (-0.025, 1.42, 0.95, 0.30, 0.20, 0.10),  # below 0: subdivision lifts the sole back to the floor
    (0.035, 1.42, 0.95, 0.30, 0.20, 0.10),   # support: crisp sole edge
    (0.28, 1.37, 0.91, 0.29, 0.17, 0.09),
    (0.36, 1.28, 0.85, 0.27, 0.13, 0.07),   # top of the feet
    (0.54, 1.00, 0.68, 0.24, 0.04, 0.03),
    (0.76, 0.84, 0.56, 0.20, 0.0, 0.0),
    (1.00, 0.78, 0.51, 0.18, 0.0, 0.0),     # waist
    (1.22, 0.86, 0.55, 0.16, 0.0, 0.0),
    (1.40, 1.07, 0.60, 0.13, 0.0, 0.0),     # head underside sweeps out
    (HEAD_BOTTOM, HEAD_HX, 0.62, 0.10, 0.0, 0.0),
    (1.56, HEAD_HX, 0.625, 0.10, 0.0, 0.0),  # support: head bottom edge
    (HEEL_BOTTOM, HEAD_HX, HEAD_HY, 0.10, 0.0, 0.0),
    (2.23, HEAD_HX, HEAD_HY, 0.10, 0.0, 0.0),  # support: face edge
    (TOP, HEAD_HX, HEAD_HY, 0.10, 0.0, 0.0),
]


def srgb(c):
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c)


# ---------------------------------------------------------------- scene helpers
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = "NONE"
    sc.world = bpy.data.worlds.new("World")
    return sc


def new_object(name, bm, coll):
    me = bpy.data.meshes.new(name)
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    coll.objects.link(o)
    return o


def apply_modifiers(o):
    with bpy.context.temp_override(object=o, active_object=o, selected_objects=[o], selected_editable_objects=[o]):
        for m in list(o.modifiers):
            bpy.ops.object.modifier_apply(modifier=m.name)


def tris(o):
    return sum(len(p.vertices) - 2 for p in o.data.polygons)


# ---------------------------------------------------------------- cage
def outline(hx, hy, r, notch, lobe):
    """Rounded rectangle, counter-clockwise from above, always C_ARC*4 + 2*L_SIDE + 2*S_SIDE points so rings
    bridge one to one. `lobe` pushes the corners out diagonally (feet); `notch` pulls the side middles in (the
    arch between two feet). Returns (point, arch weight) pairs; the weight is 0 at the corners (the feet)."""
    cx, cy = hx - r, hy - r
    wl, ws = (0.35, 0.85, 1.0, 0.85, 0.35), (0.6, 1.0, 0.6)
    pts = []
    for ci, (ox, oy, a0) in enumerate(((cx, cy, 0), (-cx, cy, 90), (-cx, -cy, 180), (cx, -cy, 270))):
        d = Vector((math.copysign(1, ox), math.copysign(1, oy))).normalized() * lobe * LOBES[ci]
        for k in range(C_ARC):
            a = math.radians(a0 + 90 * k / (C_ARC - 1))
            pts.append((Vector((ox + r * math.cos(a), oy + r * math.sin(a))) + d, 0.0))
        if ci == 0:      # +Y side, toward -X
            pts += [(Vector((cx - 2 * cx * (i + 1) / (L_SIDE + 1), hy - notch * wl[i])), wl[i]) for i in range(L_SIDE)]
        elif ci == 1:    # -X end, toward -Y
            pts += [(Vector((-hx + 0.8 * notch * ws[i], cy - 2 * cy * (i + 1) / (S_SIDE + 1))), 0.8 * ws[i])
                    for i in range(S_SIDE)]
        elif ci == 2:    # -Y side, toward +X
            pts += [(Vector((-cx + 2 * cx * (i + 1) / (L_SIDE + 1), -hy + notch * wl[i])), wl[i]) for i in range(L_SIDE)]
        else:            # +X end, toward +Y
            pts += [(Vector((hx - 0.8 * notch * ws[i], -cy + 2 * cy * (i + 1) / (S_SIDE + 1))), 0.8 * ws[i])
                    for i in range(S_SIDE)]
    return pts


def end_patch(bm, sign, zmin):
    """The flat end faces of the head at x = sign * HEAD_HX, above zmin."""
    bm.normal_update()
    out = []
    for f in bm.faces:
        c = f.calc_center_median()
        if abs(c.x - sign * HEAD_HX) < 1e-4 and c.z > zmin and abs(f.normal.x) > 0.9:
            out.append(f)
    return out


def narrow(t, s):
    """Width factor by height in the section: the horn's underside is narrower than its top (rounded belly)."""
    return 1.0 - s * (1.0 - min(1.0, t / 0.55)) ** 2


def extrude_steps(bm, faces, section, steps):
    """Extrude a face region step by step. section/steps are (x, half width, bottom z, top z, narrowing); each new
    ring keeps every vertex's relative place in the section, so the end patch's grid tapers smoothly."""
    cur, prev = faces, section
    for step in steps:
        ret = bmesh.ops.extrude_face_region(bm, geom=cur)
        bmesh.ops.delete(bm, geom=[f for f in cur if f.is_valid], context="FACES")
        verts = [g for g in ret["geom"] if isinstance(g, bmesh.types.BMVert)]
        cur = [g for g in ret["geom"] if isinstance(g, bmesh.types.BMFace)]
        _, pw, pb, pt, ps = prev
        x, w, b, t_, s = step
        for v in verts:
            t = (v.co.z - pb) / (pt - pb)
            u = v.co.y / (pw * narrow(t, ps))
            v.co = Vector((x, u * w * narrow(t, s), b + t * (t_ - b)))
        prev = step
    return cur


def horn_steps():
    out = []
    for th in (0.12, 0.3, 0.5, 0.7, 0.86, 1.0):
        out.append((-HEAD_HX - HORN_LEN * th,
                    HEAD_HY * (1 - 0.75 * th ** 1.3),              # convex taper: a fat cone, blunt tip
                    HEAD_BOTTOM + 0.42 * (1 - (1 - th) ** 1.6),   # belly sweeps up, then runs to the tip
                    TOP - 0.22 * th ** 1.5,                        # top slopes gently down to the tip
                    0.4 * min(1.0, th / 0.3)))
    out.append((-HEAD_HX - HORN_LEN * 1.04, 0.08, 1.96, 2.04, 0.4))   # rounds the tip off
    return out


def build_cage(coll):
    bm = bmesh.new()
    rnd = random.Random(7)
    rings = []
    for i, (z, hx, hy, r, notch, lobe) in enumerate(RINGS):
        ring = []
        for p, w in outline(hx, hy, r, notch, lobe):
            j = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1))) * (0.012 if i < 8 else 0.0)   # base and waist only
            arch = ARCH * w if i < 2 else 0.0      # the sole lifts between the feet, so four feet stand on the floor
            ring.append(bm.verts.new((p.x + j.x, p.y + j.y, z + arch)))
        rings.append(ring)
    k = len(rings[0])
    for a, b in zip(rings, rings[1:]):
        for i in range(k):
            j = (i + 1) % k
            bm.faces.new((a[i], a[j], b[j], b[i]))
    bm.faces.new(rings[0][::-1])
    top = bm.faces.new(rings[-1])
    bmesh.ops.inset_region(bm, faces=[top], thickness=0.07, depth=0.0)   # support loop just inside the face edge

    head = (0.0, HEAD_HY, HEAD_BOTTOM, TOP, 0.0)
    extrude_steps(bm, end_patch(bm, -1, HEAD_BOTTOM), head, horn_steps())
    heel = (0.0, HEAD_HY, HEEL_BOTTOM, TOP, 0.0)
    extrude_steps(bm, end_patch(bm, 1, HEEL_BOTTOM), heel,
                  [(1.4, 0.60, 1.92, TOP, 0.0), (1.73, 0.57, 1.94, TOP, 0.0), (1.8, 0.565, 1.95, TOP, 0.0)])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return new_object("AnvilV2", bm, coll)


def finish_mesh(o, coll):
    m = o.modifiers.new("Subdivision", "SUBSURF")
    m.levels = m.render_levels = 2
    m.quality = 3
    apply_modifiers(o)
    # hardy hole
    bm = bmesh.new()
    h = HOLE
    res = bmesh.ops.create_cube(bm, size=1.0)
    for v in res["verts"]:
        v.co = Vector((h["x"] + v.co.x * 2 * h["half"], v.co.y * 2 * h["half"],
                       h["bottom"] + (v.co.z + 0.5) * (TOP + 0.3 - h["bottom"])))
    cutter = new_object("HoleCutter", bm, coll)
    b = o.modifiers.new("Hole", "BOOLEAN")
    b.operation, b.solver, b.object = "DIFFERENCE", "EXACT", cutter
    apply_modifiers(o)
    bpy.data.objects.remove(cutter)
    d = o.modifiers.new("Decimate", "DECIMATE")
    d.ratio = min(1.0, TRI_TARGET / tris(o))
    d.use_collapse_triangulate = True
    apply_modifiers(o)
    me = o.data
    # sit on the floor
    zmin = min(v.co.z for v in me.vertices)
    for v in me.vertices:
        v.co.z -= zmin
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 3])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    me.set_sharp_from_angle(angle=math.radians(55))   # sharp only around the hardy hole


def unwrap(o):
    vl = bpy.context.view_layer
    for ob in vl.objects:
        ob.select_set(False)
    vl.objects.active = o
    o.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(60), island_margin=0.006, area_weight=0.0,
                             correct_aspect=True, scale_to_bounds=True)
    bpy.ops.object.mode_set(mode="OBJECT")
    o.data.uv_layers[0].name = "UVMap"


# ---------------------------------------------------------------- paint
class Nodes:
    def __init__(self, nt):
        self.nt = nt

    def n(self, kind, **props):
        node = self.nt.nodes.new(kind)
        for k, v in props.items():
            setattr(node, k, v)
        return node

    def link(self, a, b):
        self.nt.links.new(a, b)

    def put(self, sock, v):
        if isinstance(v, (int, float)):
            sock.default_value = v
        elif isinstance(v, tuple):
            sock.default_value = v
        else:
            self.link(v, sock)

    def math(self, op, a, b=0.0, clamp=False):
        m = self.n("ShaderNodeMath", operation=op, use_clamp=clamp)
        self.put(m.inputs[0], a)
        self.put(m.inputs[1], b)
        return m.outputs[0]

    def rng(self, v, a, b, lo=0.0, hi=1.0, smooth=True):
        m = self.n("ShaderNodeMapRange", interpolation_type="SMOOTHSTEP" if smooth else "LINEAR", clamp=True)
        self.put(m.inputs["Value"], v)
        m.inputs["From Min"].default_value, m.inputs["From Max"].default_value = a, b
        m.inputs["To Min"].default_value, m.inputs["To Max"].default_value = lo, hi
        return m.outputs["Result"]

    def mix(self, fac, a, b, blend="MIX"):
        m = self.n("ShaderNodeMix", data_type="RGBA", blend_type=blend, clamp_result=True)
        ins = {s.identifier: s for s in m.inputs}
        self.put(ins["Factor_Float"], fac)
        self.put(ins["A_Color"], srgb(a) + (1,) if isinstance(a, tuple) else a)
        self.put(ins["B_Color"], srgb(b) + (1,) if isinstance(b, tuple) else b)
        return next(s for s in m.outputs if s.identifier == "Result_Color")

    def noise(self, vec, scale, w=0.0, detail=3.0, rough=0.5):
        t = self.n("ShaderNodeTexNoise", noise_dimensions="4D")
        self.link(vec, t.inputs["Vector"])
        t.inputs["Scale"].default_value, t.inputs["W"].default_value = scale, w
        t.inputs["Detail"].default_value, t.inputs["Roughness"].default_value = detail, rough
        return t.outputs["Fac"]

    def voronoi(self, vec, scale, feature="F1"):
        t = self.n("ShaderNodeTexVoronoi", feature=feature)
        self.link(vec, t.inputs["Vector"])
        t.inputs["Scale"].default_value = scale
        return t.outputs["Distance"]

    def stretch(self, vec, sx, sy, sz):
        m = self.n("ShaderNodeMapping")
        self.link(vec, m.inputs["Vector"])
        m.inputs["Scale"].default_value = (sx, sy, sz)
        return m.outputs["Vector"]


# palette (sRGB), from the reference: lavender-blue top planes, cooler blue-grey sides, deep blue-grey recesses
DEEP = (0.17, 0.18, 0.27)
SIDE = (0.37, 0.42, 0.58)
FACE = (0.62, 0.64, 0.82)
SIDE_LIGHT = (0.50, 0.53, 0.70)
LAVENDER = (0.53, 0.48, 0.68)
GREY = (0.44, 0.47, 0.55)
EDGE_BLUE = (0.74, 0.82, 0.95)
EDGE_WHITE = (0.93, 0.94, 0.97)


def paint_source():
    m = bpy.data.materials.new("m_src_anvil_paint")
    m.use_nodes = True
    nt = m.node_tree
    for node in list(nt.nodes):
        nt.nodes.remove(node)
    N = Nodes(nt)
    out = N.n("ShaderNodeOutputMaterial")
    emit = N.n("ShaderNodeEmission")
    N.link(emit.outputs["Emission"], out.inputs["Surface"])
    co = N.n("ShaderNodeTexCoord").outputs["Object"]
    geo = N.n("ShaderNodeNewGeometry")
    sep = N.n("ShaderNodeSeparateXYZ")
    N.link(geo.outputs["Normal"], sep.inputs[0])
    nz = sep.outputs["Z"]
    pos = N.n("ShaderNodeSeparateXYZ")
    N.link(co, pos.inputs[0])

    # light planes: up-facing faces lightest, sides mid, undersides deep; darker toward the floor
    c = N.mix(N.rng(nz, -0.2, 0.95), SIDE, FACE)
    c = N.mix(N.rng(nz, -0.15, -0.95, 0.0, 0.75), c, DEEP)
    c = N.mix(N.rng(pos.outputs["Z"], 0.0, 1.7, 0.5, 0.0), c, DEEP)
    # painted light on the head's sides: lighter toward the face edge
    side = N.math("MULTIPLY", N.rng(nz, 0.6, 0.1), N.rng(pos.outputs["Z"], 1.7, 2.3, 0.0, 0.6))
    c = N.mix(side, c, SIDE_LIGHT)
    # broad painted patches
    c = N.mix(N.rng(N.noise(co, 1.4, 0.0), 0.42, 0.66, 0.0, 0.6), c, LAVENDER)
    c = N.mix(N.rng(N.noise(co, 2.1, 5.0), 0.45, 0.68, 0.0, 0.5), c, GREY)
    # soft brush-stroke value variation, longer than wide
    strokes = N.noise(N.stretch(co, 2.5, 6.0, 2.5), 2.2, 9.0, 2.0, 0.4)
    c = N.mix(1.0, c, N.rng(strokes, 0.3, 0.7, 0.86, 1.14, smooth=False), blend="MULTIPLY")
    # recesses: local AO
    ao = N.n("ShaderNodeAmbientOcclusion", samples=16, only_local=True)
    ao.inputs["Distance"].default_value = 0.45
    c = N.mix(N.rng(ao.outputs["AO"], 0.95, 0.35, 0.0, 0.7), c, DEEP)
    # dents and smudges: a few soft darker blotches
    blot = N.rng(N.voronoi(co, 5.0), 0.16, 0.05, 0.0, 1.0)
    blot = N.math("MULTIPLY", blot, N.rng(N.noise(co, 3.0, 2.0), 0.5, 0.7))
    c = N.mix(N.math("MULTIPLY", blot, 0.22), c, DEEP)

    # edge highlights: bevel-normal vs true normal finds the convex edges; noise breaks them into painted strokes
    bev = N.n("ShaderNodeBevel", samples=12)
    bev.inputs["Radius"].default_value = 0.2
    dot = N.n("ShaderNodeVectorMath", operation="DOT_PRODUCT")
    N.link(bev.outputs["Normal"], dot.inputs[0])
    N.link(geo.outputs["Normal"], dot.inputs[1])
    edge = N.rng(dot.outputs["Value"], 0.9993, 0.972)
    glow = N.rng(dot.outputs["Value"], 0.99995, 0.995, 0.0, 0.45)      # a soft lighter band before the hard edge
    c = N.mix(glow, c, SIDE_LIGHT)
    breakup = N.rng(N.noise(co, 6.0, 3.0, 4.0, 0.6), 0.38, 0.62, 0.6, 1.0)
    edge = N.math("MULTIPLY", edge, breakup)
    edge = N.math("MULTIPLY", edge, N.rng(nz, -0.6, 0.6, 0.45, 1.0))   # upper edges brightest
    hi = N.mix(N.rng(N.noise(co, 4.0, 7.0), 0.45, 0.6), EDGE_BLUE, EDGE_WHITE)
    c = N.mix(N.math("MINIMUM", N.math("MULTIPLY", edge, 1.3), 0.95), c, hi)

    # scratches: thin cell borders of stretched Voronoi, sparse, mostly on the working face
    scratch = None
    for (sx, sy, sz), w in (((1.0, 5.0, 5.0), 0.0), ((5.0, 1.0, 5.0), 4.0)):
        lines = N.rng(N.voronoi(N.stretch(co, sx, sy, sz), 3.2, "DISTANCE_TO_EDGE"), 0.018, 0.0, 0.0, 1.0)
        gate = N.rng(N.noise(co, 2.6, w + 11.0), 0.56, 0.68)
        s = N.math("MULTIPLY", lines, gate)
        scratch = s if scratch is None else N.math("MAXIMUM", scratch, s)
    scratch = N.math("MULTIPLY", scratch, N.rng(nz, 0.2, 0.9, 0.35, 0.8))
    c = N.mix(scratch, c, EDGE_BLUE)
    # small scuffs near edges
    chips = N.rng(N.voronoi(co, 18.0), 0.09, 0.03, 0.0, 1.0)
    chips = N.math("MULTIPLY", chips, N.math("MULTIPLY", N.rng(edge, 0.05, 0.4), 0.7))
    c = N.mix(chips, c, EDGE_WHITE)
    N.link(c, emit.inputs["Color"])
    return m


def blur(img, passes=1):
    """Soften the baked noise a touch (3x3 box) so it reads painted, not grainy."""
    import numpy as np
    w, h = img.size
    a = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(a)
    a = a.reshape(h, w, 4)
    for _ in range(passes):
        p = np.pad(a, ((1, 1), (1, 1), (0, 0)), mode="edge")
        a = sum(p[dy:dy + h, dx:dx + w] for dy in range(3) for dx in range(3)) / 9.0
    img.pixels.foreach_set(a.ravel())


def bake_paint(o, sc):
    os.makedirs(TEX, exist_ok=True)
    src = paint_source()
    o.data.materials.clear()
    o.data.materials.append(src)
    sc.render.engine = "CYCLES"
    sc.cycles.samples = 96
    sc.cycles.device = "CPU"
    img = bpy.data.images.new("anvil_v2_color", TEX_SIZE, TEX_SIZE, alpha=False)
    img.colorspace_settings.name = "sRGB"
    node = src.node_tree.nodes.new("ShaderNodeTexImage")
    node.image = img
    src.node_tree.nodes.active = node
    for ob in sc.objects:
        ob.hide_render = ob is not o
    with bpy.context.temp_override(object=o, active_object=o, selected_objects=[o], selected_editable_objects=[o]):
        bpy.ops.object.bake(type="EMIT", use_clear=True, margin=TEX_SIZE // 64)
    blur(img)
    img.filepath_raw = os.path.join(TEX, "anvil_v2_color.png")
    img.file_format = "PNG"
    img.save()
    for ob in sc.objects:
        ob.hide_render = False
    m = bpy.data.materials.new("m_anvil_v2_steel")
    m.use_nodes = True
    nt = m.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.6
    bsdf.inputs["Metallic"].default_value = 0.0      # painted steel: the shine is in the texture, not a mirror
    o.data.materials.clear()
    o.data.materials.append(m)
    bpy.data.materials.remove(src)


# ---------------------------------------------------------------- review renders
VIEWS = {  # name: (direction from target to camera, orthographic)
    "front_three_quarter": ((0.62, -1.0, 0.55), False),
    "rear_three_quarter": ((-0.62, 1.0, 0.55), False),
    "left": ((-1.0, 0.0, 0.0), True),
    "right": ((1.0, 0.0, 0.0), True),
    "front": ((0.0, -1.0, 0.0), True),
    "back": ((0.0, 1.0, 0.0), True),
    "top": ((0.0, 0.0, 1.0), True),
}


def review(sc, o):
    os.makedirs(REVIEW, exist_ok=True)
    engines = [i.identifier for i in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items]
    sc.render.engine = next(e for e in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE") if e in engines)
    sc.view_settings.view_transform = "Standard"
    w = sc.world
    w.use_nodes = True
    bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs[0].default_value = srgb((0.30, 0.29, 0.33)) + (1,)
    bg.inputs[1].default_value = 1.3
    sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN"))
    sun.data.energy, sun.data.color, sun.data.angle = 3.4, (1.0, 0.95, 0.88), math.radians(8)
    sun.rotation_euler = (math.radians(42), 0, math.radians(-40))
    sc.collection.objects.link(sun)
    fill = bpy.data.objects.new("Fill", bpy.data.lights.new("Fill", "SUN"))
    fill.data.energy, fill.data.color = 0.6, (0.75, 0.8, 1.0)
    fill.rotation_euler = (math.radians(60), 0, math.radians(150))
    sc.collection.objects.link(fill)
    gme = bpy.data.meshes.new("Ground")
    gme.from_pydata([(-30, -30, -0.002), (30, -30, -0.002), (30, 30, -0.002), (-30, 30, -0.002)], [], [(0, 1, 2, 3)])
    g = bpy.data.objects.new("Ground", gme)
    gm = bpy.data.materials.new("m_review_ground")
    gm.use_nodes = True
    gb = next(n for n in gm.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    gb.inputs["Base Color"].default_value = srgb((0.34, 0.33, 0.37)) + (1,)
    gb.inputs["Roughness"].default_value = 1.0
    gme.materials.append(gm)
    sc.collection.objects.link(g)
    cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    sc.render.resolution_x = sc.render.resolution_y = 900
    pts = [o.matrix_world @ v.co for v in o.data.vertices]
    lo = Vector([min(p[k] for p in pts) for k in range(3)])
    hi_ = Vector([max(p[k] for p in pts) for k in range(3)])
    centre = (lo + hi_) / 2
    out = []
    for name, (d, ortho) in VIEWS.items():
        d = Vector(d).normalized()
        cam.data.type = "ORTHO" if ortho else "PERSP"
        if ortho:
            cam.data.ortho_scale = 5.4
            cam.location = centre + d * 12
        else:
            cam.data.lens = 50
            cam.location = centre + d * 8.5
        if name == "top":
            cam.rotation_euler = (0, 0, 0)
        else:
            cam.rotation_euler = (centre - cam.location).to_track_quat("-Z", "Y").to_euler()
        sc.render.filepath = os.path.join(REVIEW, f"anvil_v2_{name}.png")
        bpy.ops.render.render(write_still=True)
        out.append(sc.render.filepath)
    for ob in (sun, fill, g, cam):
        bpy.data.objects.remove(ob)
    return out


def skill(module, sub):
    import importlib
    p = os.path.join(SKILLS, sub, "scripts")
    if p not in sys.path:
        sys.path.insert(0, p)
    return importlib.reload(importlib.import_module(module))


def main():
    sc = reset()
    coll = bpy.data.collections.new("AnvilV2")
    sc.collection.children.link(coll)
    o = build_cage(coll)
    cage_faces = len(o.data.polygons)
    finish_mesh(o, coll)
    unwrap(o)
    bake_paint(o, sc)
    pts = [v.co for v in o.data.vertices]
    report = {"triangles": tris(o), "cage_faces": cage_faces,
              "size_studs": [round(max(p[k] for p in pts) - min(p[k] for p in pts), 3) for k in range(3)],
              "x_range": [round(min(p.x for p in pts), 3), round(max(p.x for p in pts), 3)]}
    try:
        report["qa"] = skill("qa_check", "blender-asset-qa").run(objects=[o.name], profile="roblox")
    except Exception as e:  # noqa: BLE001 - record and carry on, the review still runs
        report["qa_error"] = repr(e)
    report["renders"] = review(sc, o)
    ex = skill("export_asset", "blender-export-pipelines")
    for preset, name in (("roblox", "AnvilV2.fbx"), ("roblox_gltf", "AnvilV2.glb")):
        try:
            report[f"export_{preset}"] = ex.run(preset=preset, collection="AnvilV2", out=os.path.join(HERE, name),
                                                batch=False, no_anim=True)
        except Exception as e:  # noqa: BLE001
            report[f"export_{preset}_error"] = repr(e)
    bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, "AnvilV2.blend"))
    with open(os.path.join(HERE, "qa.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str)
    print("ANVIL_V2_DONE", report["triangles"], report["size_studs"])


main()

# Low-poly helpers. 1 Blender unit = 1 Roblox stud, Z up, station front faces -Y.
import bpy, bmesh, math
from mathutils import Vector, Matrix, Euler

PAL = {
    "wood":     (0.88, 0.50, 0.24),
    "wood_dk":  (0.58, 0.29, 0.14),
    "cream":    (0.93, 0.83, 0.66),
    "cream_dk": (0.79, 0.69, 0.55),
    "iron":     (0.24, 0.24, 0.29),
    "iron_dk":  (0.14, 0.14, 0.17),
    "steel":    (0.74, 0.77, 0.82),
    "red":      (0.90, 0.20, 0.18),
    "indigo":   (0.22, 0.33, 0.72),
    "teal":     (0.13, 0.66, 0.62),
    "gold":     (0.95, 0.72, 0.25),
    "paper":    (1.00, 0.96, 0.84),
    "ore":      (0.25, 0.88, 0.90),
    "ore_iron": (0.38, 0.39, 0.44),
    "chamber":  (0.18, 0.08, 0.06),
    "ember":    (1.00, 0.32, 0.06),
    "hot":      (1.00, 0.62, 0.12),
    "iron_face": (0.31, 0.32, 0.38),
    "ingot":    (1.00, 0.40, 0.08),
    "skin":     (0.98, 0.80, 0.62),
    "shirt":    (0.42, 0.48, 0.60),
    "pants":    (0.27, 0.29, 0.35),
}
GLOW = {"ember": 4.0, "hot": 4.0, "ingot": 2.5}

# One switch for the whole set. "mid-high": rounded 3-segment bevels with smooth shading (flats stay
# crisp), round cylinders, finer rocks. "low": the original flat-shaded chamfered look.
DETAIL = "mid-high"
LEVELS = {
    "low":      dict(segments=1, bevel_scale=1.0, min_bevel=0.0, min_sides=0, rock_subdiv=1, smooth=False),
    "mid-high": dict(segments=3, bevel_scale=1.4, min_bevel=0.025, min_sides=28, rock_subdiv=2, smooth=True),
}
def lvl(k):
    return LEVELS[DETAIL][k]

def srgb2lin(c):
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c)

def mat(key):
    name = "LP_" + key
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    col = srgb2lin(PAL[key]) + (1.0,)
    m.diffuse_color = col
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = col
    b.inputs["Roughness"].default_value = 0.75
    b.inputs["Emission Color"].default_value = col
    b.inputs["Emission Strength"].default_value = GLOW.get(key, 0.0)
    return m

_coll = [None]
def station(name, x, y=0):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if c.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(c)
    for o in list(c.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    root = bpy.data.objects.new(name, None)
    root.empty_display_size = 1
    root.location = (x, y, 0)
    c.objects.link(root)
    _coll[0] = (c, root)
    return root

def auto_uv(bm):
    """One UV set inside 0-1 (Roblox requires it): box projection scaled to the part's largest side."""
    uv = bm.loops.layers.uv.verify()
    lo = [min(v.co[k] for v in bm.verts) for k in range(3)]
    span = max(max(v.co[k] for v in bm.verts) - lo[k] for k in range(3)) or 1.0
    bm.normal_update()
    for f in bm.faces:
        ax = max(range(3), key=lambda k: abs(f.normal[k]))
        a, b = [k for k in range(3) if k != ax]
        for l in f.loops:
            l[uv].uv = ((l.vert.co[a] - lo[a]) / span, (l.vert.co[b] - lo[b]) / span)

def _finish(name, bm, color, loc, rot, bevel, smooth=True):
    dims = [max(v.co[k] for v in bm.verts) - min(v.co[k] for v in bm.verts) for k in range(3)]
    off = bevel * lvl("bevel_scale") if bevel else (lvl("min_bevel") if smooth and min(dims) > 0.12 else 0)
    if off:
        bm.normal_update()
        sharp = [e for e in bm.edges if e.calc_face_angle(0) > math.radians(30)]  # not round-body seams
        bmesh.ops.bevel(bm, geom=sharp, offset=off, segments=lvl("segments"), profile=0.5,
                        affect="EDGES", clamp_overlap=True)
        bmesh.ops.dissolve_degenerate(bm, dist=1e-5, edges=bm.edges[:])
    auto_uv(bm)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    soft = smooth and lvl("smooth")
    for p in me.polygons:
        p.use_smooth = soft
    if soft:
        me.set_sharp_from_angle(angle=math.radians(35))
    me.materials.append(mat(color))
    c, root = _coll[0]
    o = bpy.data.objects.new(name, me)
    c.objects.link(o)
    o.parent = root
    o.location = loc
    o.rotation_euler = Euler([math.radians(a) for a in rot])
    return o

def frustum(name, w1, d1, w2, d2, h, loc, color, rot=(0, 0, 0), bevel=0.0):
    """Rectangular frustum, bottom w1 x d1 at z=0, top w2 x d2 at z=h (local)."""
    bm = bmesh.new()
    v = [bm.verts.new((sx * w / 2, sy * d / 2, z))
         for (w, d, z) in ((w1, d1, 0), (w2, d2, h))
         for (sx, sy) in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    bm.faces.new(v[3::-1]); bm.faces.new(v[4:])
    for i in range(4):
        j = (i + 1) % 4
        bm.faces.new((v[i], v[j], v[4 + j], v[4 + i]))
    return _finish(name, bm, color, loc, rot, bevel)

def box(name, w, d, h, loc, color, rot=(0, 0, 0), bevel=0.0):
    """Box w x d x h, loc is the bottom-centre."""
    return frustum(name, w, d, w, d, h, loc, color, rot, bevel)

def cyl(name, r, h, loc, color, sides=8, r2=None, rot=(0, 0, 0), bevel=0.0):
    """Prism/cone along local Z, bottom at z=0."""
    r2 = r if r2 is None else r2
    sides = max(sides, lvl("min_sides"))
    bm = bmesh.new()
    bot = [bm.verts.new((r * math.cos(a), r * math.sin(a), 0)) for a in
           (2 * math.pi * i / sides + math.pi / sides for i in range(sides))]
    if r2 > 0:
        top = [bm.verts.new((r2 * math.cos(a), r2 * math.sin(a), h)) for a in
               (2 * math.pi * i / sides + math.pi / sides for i in range(sides))]
        tc = bm.verts.new((0, 0, h))  # caps as triangle fans: no n-gons (Roblox QA)
        for i in range(sides):
            j = (i + 1) % sides
            bm.faces.new((bot[i], bot[j], top[j], top[i]))
            bm.faces.new((top[i], top[j], tc))
    else:
        tip = bm.verts.new((0, 0, h))
        for i in range(sides):
            bm.faces.new((bot[i], bot[(i + 1) % sides], tip))
    bc = bm.verts.new((0, 0, 0))
    for i in range(sides):
        bm.faces.new((bot[(i + 1) % sides], bot[i], bc))
    return _finish(name, bm, color, loc, rot, bevel)

def rock(name, r, loc, color, scale=(1, 1, 1), seed=0, rot=(0, 0, 0)):
    """Faceted lump (ore, coal, embers): jittered icosphere, always flat-shaded so it reads as cut."""
    import random
    rnd = random.Random(seed)
    sub = lvl("rock_subdiv")
    lo, hi = (0.85, 1.12) if sub == 1 else (0.92, 1.06)
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=sub, radius=r)
    for v in bm.verts:
        v.co = Vector((v.co.x * scale[0], v.co.y * scale[1], v.co.z * scale[2])) * rnd.uniform(lo, hi)
    return _finish(name, bm, color, loc, rot, 0, smooth=False)

def at(x, y, z):
    return Vector((x, y, z))


# ---------------------------------------------------------------- stations
# v3, from Art/Blender Station Review (v2 feedback). z = 0 is the floor the station stands on.
# Heights measured in Studio 2026-10-19 (floor-relative):
#   forge trays top 0.93, ingot slot 0.15 inside the mouth at x +-0.45
#   anvil Face top 3.0 today; ANVIL_TOP below is the proposed lower height
#   hilt bench top 2.9
#   displayed sword: grip (0.75) centred on the Slot, guard 0.1 below it, blade hangs from the guard
ANVIL_TOP = 2.3
GRIP, GUARD = 0.75, 0.1
BLADES = {"tanto": 1.29, "wakizashi": 2.5, "katana": 3.5}  # nagasa x 0.05 studs/cm
COLLAR_TOP = 0.45 + BLADES["katana"]   # guard rests here; katana tip clears the plinth by ~0.1


def forge(x=0, y=0):
    station("Forge", x, y)
    box("Plinth", 4.6, 3.6, 0.3, at(0, 0, 0), "cream_dk", bevel=0.06)
    # body built around a real chamber: x -1.2..1.2, z 0.6..2.0, 1.5 deep from the front (y -1.6)
    for sx in (-1, 1):
        box("Wall", 0.9, 3.2, 2.4, at(sx * 1.65, 0, 0.3), "cream", bevel=0.08)
    box("Hearth", 2.4, 3.2, 0.3, at(0, 0, 0.3), "cream", bevel=0.04)
    box("Crown", 2.4, 3.2, 0.7, at(0, 0, 2.0), "cream", bevel=0.08)
    box("Back", 2.4, 1.7, 1.4, at(0, 0.75, 0.6), "chamber")
    box("Course", 4.4, 3.4, 0.4, at(0, 0, 2.7), "cream", bevel=0.1)
    # dark lining so the inside of the mouth reads deep, with the heat at the back
    for sx in (-1, 1):
        box("Lining", 0.05, 1.5, 1.4, at(sx * 1.175, -0.85, 0.6), "chamber")
    box("LiningTop", 2.3, 1.5, 0.05, at(0, -0.85, 1.95), "chamber")
    box("Coals", 2.3, 1.45, 0.12, at(0, -0.85, 0.6), "ember")
    box("BackGlow", 2.3, 0.04, 0.7, at(0, -0.12, 0.72), "hot")
    for i, (ex, ey) in enumerate(((-0.8, -0.4), (-0.3, -0.6), (0.25, -0.35), (0.8, -0.55), (0.0, -0.25))):
        rock(f"Ember{i}", 0.22, at(ex, ey, 0.74), "hot" if i % 2 else "ember", scale=(1.2, 1, 0.7), seed=i)
    box("Lintel", 3.0, 0.4, 0.45, at(0, -1.7, 2.0), "iron", bevel=0.05)  # one heavy iron beam over the mouth
    # trays run from deep in the fire out past the mouth; ingot slot is 0.15 inside the mouth
    for n, sx in ((1, -0.45), (2, 0.45)):
        box(f"Tray{n}", 0.64, 2.2, 0.06, at(sx, -1.5, 0.87), "iron")
        for rx in (-0.36, 0.36):
            box(f"Tray{n}Rail", 0.08, 2.2, 0.16, at(sx + rx, -1.5, 0.87), "iron_dk")
        box(f"Tray{n}Lip", 0.8, 0.08, 0.16, at(sx, -2.64, 0.87), "iron_dk")
        cyl(f"Tray{n}Pull", 0.05, 0.35, at(sx, -2.68, 0.95), "iron_dk", sides=6, rot=(90, 0, 0))
    frustum("Hood", 3.8, 2.8, 1.5, 1.3, 1.4, at(0, 0, 3.1), "cream", bevel=0.08)
    box("Collar", 1.4, 1.3, 0.45, at(0, 0, 4.45), "iron", bevel=0.06)
    box("Chimney", 0.95, 0.95, 1.2, at(0, 0, 4.9), "iron", bevel=0.06)
    box("Flue", 0.6, 0.6, 0.04, at(0, 0, 6.08), "iron_dk")
    # box bellows (fuigo) with its one moving part: the push-pull handle out the front
    for lx in (-0.6, 0.6):
        for ly in (-0.75, 0.75):
            box("BellowsLeg", 0.25, 0.25, 0.3, at(-3.25 + lx, ly, 0), "wood_dk")
    box("Bellows", 1.6, 2.0, 1.1, at(-3.25, 0, 0.3), "wood", bevel=0.08)
    box("BellowsEnd", 1.3, 0.12, 0.8, at(-3.25, -1.04, 0.45), "wood_dk", bevel=0.03)
    for rx in (-0.35, 0.35):
        cyl("BellowsRod", 0.05, 0.75, at(-3.25 + rx, -1.08, 0.85), "iron_dk", sides=6, rot=(90, 0, 0))
    cyl("BellowsHandle", 0.11, 1.2, at(-3.85, -1.85, 0.85), "red", sides=6, rot=(0, 90, 0))
    box("BellowsPipe", 0.75, 0.3, 0.3, at(-2.1, 0.4, 0.45), "iron_dk")


def anvil(x=0, y=0):
    station("Anvil", x, y)
    t = ANVIL_TOP
    base_h = t - 0.85
    for i, px in enumerate((-1.2, -0.4, 0.4, 1.2)):  # squat block of upright timbers
        box(f"Timber{i}", 0.8, 1.8, base_h, at(px, 0, 0), "wood", bevel=0.08)
    box("Band", 3.3, 1.9, 0.3, at(0, 0, base_h * 0.4), "iron_dk", bevel=0.03)
    for bx in (-1.2, -0.4, 0.4, 1.2):
        box("Bolt", 0.16, 0.06, 0.16, at(bx, -0.97, base_h * 0.4 + 0.07), "iron")
    # hornless kanatoko, low and broad: dark body, a chamfer, then the lighter striking face on top
    box("Block", 3.6, 2.0, 0.8, at(0, 0, base_h), "iron", bevel=0.14)
    box("StrikeFace", 3.24, 1.64, 0.05, at(0, 0, t - 0.05), "iron_face", bevel=0.015)  # nearly flush


def anvil_horned(x=0, y=0):
    """Classic anvil with a horn (Allen 2026-10-20: "make the anvil look like an actual anvil with the horn"),
    on a banded log stump. The striking face stays ANVIL_TOP above the floor and 3.0 x 1.3 like the scripted
    Face; the horn points to -X (the blade mount's end), the heel with its hardy hole to +X."""
    station("AnvilHorned", x, y)
    t = ANVIL_TOP
    cyl("Stump", 1.05, 1.0, at(0, 0, 0), "wood", sides=10, r2=0.95, bevel=0.04)
    cyl("StumpBand", 1.07, 0.16, at(0, 0, 0.62), "iron_dk", sides=10)
    frustum("Feet", 2.3, 1.45, 1.6, 0.95, 0.36, at(0, 0, 0.98), "iron", bevel=0.05)
    frustum("Waist", 1.0, 0.7, 1.25, 0.85, 0.38, at(0, 0, 1.32), "iron", bevel=0.04)
    box("Body", 3.0, 1.3, t - 0.05 - 1.68, at(0, 0, 1.68), "iron", bevel=0.08)
    box("Face", 2.92, 1.22, 0.06, at(0, 0, t - 0.06), "iron_face", bevel=0.015)
    # horn: a cone off the -X end, its top just under the face
    cyl("Horn", 0.52, 1.5, at(-1.45, 0, t - 0.6), "iron", sides=14, r2=0.05, rot=(0, -90, 0))
    # heel: a lower step off the +X end with the square hardy hole and round pritchel hole
    box("Heel", 0.7, 1.0, 0.32, at(1.75, 0, t - 0.42), "iron", bevel=0.04)
    box("HardyHole", 0.22, 0.22, 0.03, at(1.62, 0, t - 0.11), "iron_dk")
    cyl("PritchelHole", 0.07, 0.03, at(1.95, 0, t - 0.11), "iron_dk", sides=8)


PAL.setdefault("anvil", (0.40, 0.38, 0.37))


def anvil_one_piece(x=0, y=0):
    """Anvil as ONE low-poly mesh (Allen 2026-10-20, from his reference: "it should look like one piece, not
    multiple shapes put together"): a flat top that runs straight into a tapering horn (-X, the blade mount's
    end) and a squared heel (+X), a body that pinches into a waist, and four notched feet. Built from stacked
    16-point outlines bridged with quads and flat-shaded. Face top at ANVIL_TOP, standing on the floor."""
    station("AnvilOnePiece", x, y)
    t = ANVIL_TOP
    top = [(1.8, -0.45), (1.8, 0.45), (1.5, 0.65), (0.8, 0.65), (0, 0.65), (-0.8, 0.65), (-1.5, 0.62), (-2.4, 0.25),
           (-2.95, 0.04), (-2.95, -0.04), (-2.4, -0.25), (-1.5, -0.62), (-0.8, -0.65), (0, -0.65), (0.8, -0.65), (1.5, -0.65)]
    feet = [(1.3, -0.4), (1.3, 0.4), (1.0, 0.85), (0.4, 0.85), (0.15, 0.6), (-0.15, 0.6), (-0.4, 0.85), (-1.0, 0.85),
            (-1.3, 0.4), (-1.3, -0.4), (-1.0, -0.85), (-0.4, -0.85), (-0.15, -0.6), (0.15, -0.6), (0.4, -0.85), (1.0, -0.85)]
    waist = [(0.55, -0.25), (0.55, 0.25), (0.45, 0.38), (0.25, 0.38), (0.08, 0.38), (-0.08, 0.38), (-0.25, 0.38), (-0.45, 0.38),
             (-0.55, 0.25), (-0.55, -0.25), (-0.45, -0.38), (-0.25, -0.38), (-0.08, -0.38), (0.08, -0.38), (0.25, -0.38), (0.45, -0.38)]
    under = [(1.35, -0.38), (1.35, 0.38), (1.2, 0.5), (0.6, 0.5), (0, 0.5), (-0.6, 0.5), (-1.1, 0.48), (-1.35, 0.3),
             (-1.45, 0.05), (-1.45, -0.05), (-1.35, -0.3), (-1.1, -0.48), (-0.6, -0.5), (0, -0.5), (0.6, -0.5), (1.2, -0.5)]
    # z per point for the ring just under the top edge: the horn's underside rises toward the tip
    edge_z = [t - 0.32, t - 0.32] + [t - 0.35] * 5 + [t - 0.22, t - 0.12, t - 0.12, t - 0.22] + [t - 0.35] * 5
    top_z = [t] * 8 + [t - 0.03, t - 0.03] + [t] * 6
    rings = [
        [(px, py, 0.0) for px, py in feet],
        [(px * 0.86, py * 0.86, 0.42) for px, py in feet],
        [(px, py, 1.0) for px, py in waist],
        [(px, py, t - 0.8) for px, py in under],
        [(px, py, z) for (px, py), z in zip(top, edge_z)],
        [(px, py, z) for (px, py), z in zip(top, top_z)],
    ]
    bm = bmesh.new()
    vr = [[bm.verts.new(v) for v in ring] for ring in rings]
    n = 16
    for a, b in zip(vr, vr[1:]):
        for i in range(n):
            j = (i + 1) % n
            bm.faces.new((a[i], a[j], b[j], b[i]))
    for ring, z, flip in ((vr[0], 0.0, True), (vr[-1], t, False)):   # caps as fans (no n-gons)
        cx = sum(v.co.x for v in ring) / n
        c = bm.verts.new((cx, 0, z))
        for i in range(n):
            j = (i + 1) % n
            bm.faces.new((ring[j], ring[i], c) if flip else (ring[i], ring[j], c))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    _finish("Anvil", bm, "anvil", at(0, 0, 0), (0, 0, 0), 0, smooth=False)


def hilt_bench(x=0, y=0):
    station("HiltBench", x, y)
    top = 2.9
    for lx in (-2.2, 2.2):
        for ly in (-0.85, 0.85):
            box("Leg", 0.4, 0.4, top - 0.3, at(lx, ly, 0), "wood", bevel=0.05)
        box("Stretcher", 0.26, 1.5, 0.3, at(lx, 0, 0.45), "wood_dk", bevel=0.03)
    box("Apron", 4.1, 1.8, 0.6, at(0, 0, top - 0.9), "wood_dk", bevel=0.04)
    for dx in (-1.0, 1.0):
        box("Drawer", 1.7, 0.06, 0.42, at(dx, -0.93, top - 0.81), "wood", bevel=0.03)
        box("Pull", 0.4, 0.08, 0.1, at(dx, -0.98, top - 0.65), "iron_dk", bevel=0.02)
    box("Top", 5.0, 2.4, 0.3, at(0, 0, top - 0.3), "wood", bevel=0.06)
    for sx in (-1, 1):
        box("BoardPost", 0.34, 0.34, 1.8, at(sx * 2.3, 1.0, top), "wood", bevel=0.04)
    box("Board", 4.3, 0.2, 1.15, at(0, 1.0, top + 0.3), "wood_dk", bevel=0.04)
    # grips with wrap diamonds on the front face (hex turned so a flat faces -Y)
    for i, (gx, col, wrap) in enumerate(((-1.6, "red", "paper"), (-1.05, "indigo", "paper"), (-0.5, "teal", "iron_dk"))):
        cyl(f"PegGrip{i}", 0.15, 0.8, at(gx, 0.82, top + 0.45), col, sides=6, rot=(0, 0, 30))
        cyl(f"PegGripCap{i}", 0.17, 0.12, at(gx, 0.82, top + 1.25), "iron_dk", sides=6, rot=(0, 0, 30))
        for k in range(3):
            box(f"PegWrap{i}", 0.08, 0.03, 0.08, at(gx, 0.665, top + 0.52 + k * 0.22), wrap, rot=(0, 45, 0))
    # guards with the central blade opening (it shows the board behind)
    for i, (tx, col) in enumerate(((0.55, "iron"), (1.2, "gold"), (1.85, "iron"))):
        cyl(f"PegTsuba{i}", 0.3, 0.08, at(tx, 0.9, top + 0.9), col, sides=8, rot=(90, 0, 0))
        frustum(f"PegTsubaHole{i}", 0.05, 0.02, 0.1, 0.02, 0.22, at(tx, 0.81, top + 0.8), "wood_dk")
    cyl("WorkGrip", 0.14, 0.9, at(0.2, -0.45, top + 0.15), "red", sides=6, rot=(0, 90, 0))
    for k, wx in enumerate((0.35, 0.6, 0.85)):
        cyl(f"WorkWrap{k}", 0.15, 0.05, at(wx, -0.45, top + 0.15), "paper", sides=6, rot=(0, 90, 0))
    for i, (tx, col) in enumerate(((1.6, "iron"), (2.05, "gold"))):
        cyl(f"WorkTsuba{i}", 0.2, 0.06, at(tx, -0.4, top), col, sides=8)
        frustum(f"WorkTsubaHole{i}", 0.04, 0.08, 0.04, 0.08, 0.01, at(tx, -0.4, top + 0.06), "wood")


def ore_stand(name="OreStand", x=0, y=0, ore="ore", ore_r=0.6):
    """One self-contained, repeatable material stand. `Ore` is the part a roll recolours."""
    station(name, x, y)
    for fx in (-0.75, 0.75):
        for fy in (-0.75, 0.75):
            box("Foot", 0.4, 0.4, 0.3, at(fx, fy, 0), "iron_dk", bevel=0.03)
    # two broad stone courses with offset joints (the chamfers make the joint lines)
    box("CourseLow", 1.0, 2.0, 0.45, at(-0.5, 0, 0.3), "cream", bevel=0.07)
    box("CourseLow", 1.0, 2.0, 0.45, at(0.5, 0, 0.3), "cream_dk", bevel=0.07)
    box("CourseHigh", 2.0, 1.2, 0.45, at(0, -0.4, 0.75), "cream_dk", bevel=0.07)
    box("CourseHigh", 2.0, 0.8, 0.45, at(0, 0.6, 0.75), "cream", bevel=0.07)
    # low tray so the ore sits above the rails, on a raised iron seat
    box("TrayFloor", 1.66, 1.66, 0.1, at(0, 0, 1.2), "wood_dk")  # inside the rails, no shared bottom faces
    for s in (-1, 1):
        box("TrayRail", 2.1, 0.22, 0.2, at(0, s * 0.94, 1.2), "wood", bevel=0.03)
        box("TrayRail", 0.22, 1.66, 0.2, at(s * 0.94, 0, 1.2), "wood", bevel=0.03)
    box("Seat", 0.8, 0.8, 0.22, at(0, 0, 1.3), "iron", bevel=0.04)
    if ore:
        rock("Ore", ore_r, at(0, 0, 1.52 + ore_r * 0.8), ore, scale=(1.05, 1, 0.85), seed=3)


def ore_lever(x=0, y=0):
    """The one shared lever: its own model, never part of a stand."""
    station("OreLever", x, y)
    box("Base", 1.4, 1.1, 0.4, at(0, 0, 0), "wood", bevel=0.06)
    for bx in (-0.55, 0.55):
        box("Bolt", 0.14, 0.06, 0.14, at(bx, -0.57, 0.13), "iron_dk")
    box("Bracket", 0.5, 0.45, 0.85, at(0.15, 0, 0.4), "iron", bevel=0.04)
    s, c = math.sin(math.radians(20)), math.cos(math.radians(20))
    box("Handle", 0.22, 0.22, 1.9, at(0.15, 0, 0.95), "wood_dk", rot=(0, -20, 0), bevel=0.03)
    box("Grip", 0.32, 0.32, 0.6, at(0.15 - 1.75 * s, 0, 0.95 + 1.75 * c), "red", rot=(0, -20, 0), bevel=0.04)


def half_disc(name, r, t, loc, color, segments=24, bevel=0.04):
    """Half disc standing on its flat edge: the arc rises in the YZ plane, thickness t along X; loc = centre
    of the flat bottom edge."""
    bm = bmesh.new()
    sides = []
    for x in (-t / 2, t / 2):
        ring = [bm.verts.new((x, r * math.cos(a), r * math.sin(a))) for a in
                (math.pi * i / segments for i in range(segments + 1))]
        sides.append(ring)
    a, b = sides
    bm.faces.new(a[::-1])
    bm.faces.new(b)
    for i in range(segments):
        bm.faces.new((a[i], a[i + 1], b[i + 1], b[i]))
    bm.faces.new((a[segments], a[0], b[0], b[segments]))   # flat bottom
    bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 4])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return _finish(name, bm, color, loc, (0, 0, 0), bevel)


PAL.setdefault("sage", (0.62, 0.70, 0.62))
PAL.setdefault("sage_dk", (0.50, 0.58, 0.52))
LEVER_PIVOT_Z = 0.62   # the arm swings about the X axis through (0, 0, LEVER_PIVOT_Z)


def ore_lever_v2(x=0, y=0):
    """Reroll lever (Allen's reference, 2026-10-20): a soft sage base with a raised rim, two half-disc
    cheeks (dark and light wood) either side of a dark slot, and a short arm with a big red knob. The arm
    and knob are separate parts that the game swings about LEVER_PIVOT_Z while E is held; modelled upright."""
    station("OreLever", x, y)
    box("Base", 2.4, 2.0, 0.3, at(0, 0, 0), "sage", bevel=0.12)
    for sy in (-1, 1):                                      # raised rim front and back
        box("Rim", 2.3, 0.3, 0.2, at(0, sy * 0.8, 0.3), "sage_dk", bevel=0.08)
    box("Slot", 0.34, 1.2, 0.06, at(0, 0, 0.3), "iron_dk", bevel=0.01)
    half_disc("CheekDark", 0.75, 0.3, at(-0.36, 0, 0.3), "wood_dk")
    half_disc("CheekLight", 0.75, 0.3, at(0.36, 0, 0.3), "wood")
    box("Arm", 0.16, 0.16, 1.5, at(0, 0, LEVER_PIVOT_Z - 0.1), "iron_dk", bevel=0.03)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=14, radius=0.32)   # smooth ball, unlike rock()
    _finish("Knob", bm, "red", at(0, 0, LEVER_PIVOT_Z + 1.55), (0, 0, 0), 0)


def sword_holder(name="SwordHolder", x=0, y=0):
    """Universal holder: the guard rests on padded crossbar halves, the blade drops through the slot
    between them; no tip socket, so any blade length fits. Slot (grip centre) = COLLAR_TOP + GUARD + GRIP / 2."""
    station(name, x, y)
    ct = COLLAR_TOP
    box("Plinth", 1.8, 1.4, 0.35, at(0, 0, 0), "wood", bevel=0.06)
    for cx in (-0.8, 0.8):
        box("CornerIron", 0.24, 0.06, 0.2, at(cx, -0.71, 0.07), "iron_dk")
    for sx in (-1, 1):
        box("Upright", 0.26, 0.26, ct - 0.35 + 0.15, at(sx * 0.62, 0, 0.35), "wood", bevel=0.05)
        frustum("UprightCap", 0.3, 0.3, 0.16, 0.16, 0.12, at(sx * 0.62, 0, ct + 0.15), "wood_dk", bevel=0.02)
        box("Crossbar", 0.49, 0.34, 0.28, at(sx * 0.375, 0, ct - 0.32), "wood_dk", bevel=0.04)
        box("Pad", 0.14, 0.3, 0.04, at(sx * 0.2, 0, ct - 0.04), "red")
    box("Tag", 0.32, 0.04, 0.22, at(0.45, -0.72, 0.07), "paper")


def polish_station(x=0, y=0):
    """Polishing Station (2026-10-20): the last step, a finished sword lies on two felt pads on a waist-high
    bench (same 2.9 top as the hilt bench) while the edge is polished; a water-cooled stone wheel at the
    right end and a pair of whetstones give it a read from across the room. Blade mount = top centre."""
    station("PolishStation", x, y)
    top = 2.9
    for lx in (-1.9, 1.9):
        for ly in (-0.7, 0.7):
            box("Leg", 0.38, 0.38, top - 0.3, at(lx, ly, 0), "wood", bevel=0.05)
        box("Stretcher", 0.24, 1.3, 0.28, at(lx, 0, 0.45), "wood_dk", bevel=0.03)
    box("Apron", 3.6, 1.5, 0.5, at(0, 0, top - 0.8), "wood_dk", bevel=0.04)
    box("Top", 4.4, 2.0, 0.3, at(0, 0, top - 0.3), "wood", bevel=0.06)
    for px in (-1.3, 0.7):                      # felt pads the sword lies on
        box("Pad", 0.5, 0.75, 0.1, at(px, -0.15, top), "indigo", bevel=0.02)
    box("Stone", 0.9, 0.34, 0.14, at(1.55, 0.62, top), "cream_dk", bevel=0.03)
    box("StoneFine", 0.7, 0.28, 0.1, at(0.45, 0.66, top), "cream", bevel=0.02)
    box("Cloth", 0.42, 0.3, 0.05, at(-0.6, 0.66, top), "paper", bevel=0.015)
    # water-cooled stone wheel off the right end
    box("TroughStand", 0.9, 0.8, 0.9, at(2.85, 0, 0), "wood", bevel=0.05)
    box("Trough", 1.0, 1.0, 0.3, at(2.85, 0, 0.9), "wood_dk", bevel=0.03)
    box("Water", 0.84, 0.66, 0.03, at(2.85, 0, 1.2), "teal")  # brim-full, on the trough
    for py in (-0.43, 0.43):  # clear of the water
        box("WheelPost", 0.14, 0.12, 0.95, at(2.85, py, 1.2), "iron", bevel=0.02)
    cyl("Axle", 0.06, 0.9, at(2.85, 0.45, 1.95), "iron_dk", sides=8, rot=(90, 0, 0))
    cyl("Wheel", 0.62, 0.22, at(2.85, 0.11, 1.95), "cream_dk", sides=32, rot=(90, 0, 0), bevel=0.02)
    box("Crank", 0.08, 0.08, 0.4, at(2.85, -0.47, 1.95), "iron_dk")
    cyl("CrankGrip", 0.07, 0.25, at(2.85, -0.47, 2.33), "red", sides=8, rot=(90, 0, 0))
    # water bucket on the floor at the left end
    cyl("Bucket", 0.34, 0.52, at(-2.7, -0.2, 0), "wood", sides=16, r2=0.38)
    cyl("BucketBand", 0.39, 0.07, at(-2.7, -0.2, 0.42), "iron_dk", sides=16)
    cyl("BucketWater", 0.33, 0.02, at(-2.7, -0.2, 0.52), "teal", sides=16)  # brim-full


def sword(prefix, x, y, blade):
    """A displayed sword as the game builds it: guard on the collar, grip above, blade down."""
    g = COLLAR_TOP
    L = BLADES[blade]
    frustum(prefix + "Tip", 0.03, 0.04, 0.2, 0.05, 0.3, at(x, y, g - L), "steel")
    box(prefix + "Blade", 0.2, 0.05, L - 0.3, at(x, y, g - L + 0.3), "steel")
    box(prefix + "Guard", 0.5, 0.14, GUARD, at(x, y, g), "gold", bevel=0.02)
    cyl(prefix + "Grip", 0.08, GRIP, at(x, y, g + GUARD), "red", sides=6)
    rock(prefix + "Pommel", 0.1, at(x, y, g + GUARD + GRIP + 0.05), "iron_dk", seed=1)


def avatar(x, y, yaw=0, strike_top=None):
    """Blocky 5.2-stud avatar facing +Y (before yaw). strike_top: swing the right arm so the
    hammer head lands on a face of that height ~2 studs ahead."""
    root = station("Avatar", x, y)
    root.rotation_euler.z = math.radians(yaw)
    for lx in (-0.5, 0.5):
        box("Leg", 0.95, 1.0, 2.0, at(lx, 0, 0), "pants", bevel=0.05)
    box("Torso", 2.0, 1.0, 2.0, at(0, 0, 2.0), "shirt", bevel=0.06)
    box("Head", 1.2, 1.2, 1.2, at(0, 0, 4.0), "skin", bevel=0.25)
    box("ArmL", 0.95, 1.0, 2.0, at(-1.5, 0, 3.85), "skin", rot=(180, 0, 0), bevel=0.05)
    if strike_top is None:
        box("ArmR", 0.95, 1.0, 2.0, at(1.5, 0, 3.85), "skin", rot=(180, 0, 0), bevel=0.05)
        return root
    dz = (strike_top + 0.24 - 3.85) / 2.0
    dy = math.sqrt(max(0.0, 1 - dz * dz))
    box("ArmR", 0.95, 1.0, 2.0, at(1.5, 0, 3.85), "skin", rot=(math.degrees(math.atan2(-dy, dz)), 0, 0), bevel=0.05)
    hy, hz = 2 * dy, 3.85 + 2 * dz
    cyl("HammerHandle", 0.08, 1.1, at(1.5, hy, hz), "wood_dk", sides=6, rot=(-90, 0, 0))
    box("HammerHead", 0.42, 0.6, 0.44, at(1.5, hy + 1.1, strike_top + 0.02), "iron_dk", bevel=0.04)
    return root


# Review layout: one row, same spacing, so every close-up is framed the same way.
LAYOUT = {
    "Forge": (0, 0), "Anvil": (11, 0), "HiltBench": (22, 0),
    "OreStand": (31, 0), "OreStand_2": (33.8, 0), "OreStand_3": (36.6, 0), "OreLever": (39.2, 0),
    "SwordHolder": (45, 0), "SwordHolder_2": (47.6, 0), "SwordHolder_3": (50.2, 0), "SwordHolder_4": (52.8, 0),
}
EXPORT = ("Forge", "Anvil", "HiltBench", "OreStand", "OreLever", "SwordHolder", "PolishStation")


def preview_props():
    """Scale props for the review renders only. Not exported."""
    station("PreviewProps", 0, 0)
    fx, fy = LAYOUT["Forge"]
    box("HotIngot", 0.42, 0.9, 0.2, at(fx - 0.45, fy - 1.45, 0.93), "ingot", bevel=0.03)
    box("IngotCore", 0.2, 0.6, 0.03, at(fx - 0.45, fy - 1.45, 1.13), "hot")
    ax, ay = LAYOUT["Anvil"]
    box("RawBlade", 3.6, 0.3, 0.07, at(ax - 0.2, ay - 0.1, ANVIL_TOP), "steel", rot=(0, 0, 6))
    hx, hy = LAYOUT["HiltBench"]
    box("BenchBlade", 3.0, 0.3, 0.06, at(hx - 0.9, hy - 0.1, 2.9), "steel", rot=(0, 0, -3))
    for key, blade in (("SwordHolder", "katana"), ("SwordHolder_2", "wakizashi"), ("SwordHolder_3", "tanto")):
        sx, sy = LAYOUT[key]
        sword(blade.capitalize(), sx, sy, blade)


def build_all(avatar_at="Anvil"):
    for c in list(bpy.data.collections):
        for o in list(c.objects):
            bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(c)
    for me in [m for m in bpy.data.meshes if m.users == 0]:
        bpy.data.meshes.remove(me)
    L = LAYOUT
    forge(*L["Forge"]); anvil(*L["Anvil"]); hilt_bench(*L["HiltBench"])
    ore_stand("OreStand", *L["OreStand"], ore="ore")
    ore_stand("OreStand_2", *L["OreStand_2"], ore="ore_iron", ore_r=0.38)
    ore_stand("OreStand_3", *L["OreStand_3"], ore=None)
    ore_lever(*L["OreLever"])
    for k in ("SwordHolder", "SwordHolder_2", "SwordHolder_3", "SwordHolder_4"):
        sword_holder(k, *L[k])
    preview_props()
    place_avatar(avatar_at)


AVATAR_SPOTS = {  # (dx, dy, yaw, strike) relative to each station, all facing the station
    "Forge": (4.6, -0.6, -60, False), "Anvil": (-1.5, -2.6, 0, True), "HiltBench": (-1.0, -2.6, 0, False),
    "OreStand": (11.6, 0.6, 90, False), "SwordHolder": (-2.4, -1.2, 0, False),
}


def place_avatar(key):
    old = bpy.data.collections.get("Avatar")
    if old:
        for o in list(old.objects):
            bpy.data.objects.remove(o, do_unlink=True)
    dx, dy, yaw, strike = AVATAR_SPOTS[key]
    x, y = LAYOUT[key]
    avatar(x + dx, y + dy, yaw, ANVIL_TOP if strike else None)


def preview_setup():
    """Neutral review stage: warm grey ground and sky, one sun, level camera."""
    sc = bpy.context.scene
    w = sc.world or bpy.data.worlds.new("World")
    sc.world = w
    w.use_nodes = True
    bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs[0].default_value = srgb2lin((0.80, 0.78, 0.75)) + (1,)
    bg.inputs[1].default_value = 1.0
    g = bpy.data.objects.get("Ground")
    if not g:
        me = bpy.data.meshes.new("Ground")
        me.from_pydata([(-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0)], [], [(0, 1, 2, 3)])
        g = bpy.data.objects.new("Ground", me)
        sc.collection.objects.link(g)
    g.location = (25, 0, -0.005)
    g.scale = (400, 400, 1)
    gm = bpy.data.materials.get("Preview_Ground") or bpy.data.materials.new("Preview_Ground")
    gm.use_nodes = True
    b = next(n for n in gm.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = srgb2lin((0.72, 0.70, 0.67)) + (1,)
    b.inputs["Roughness"].default_value = 1
    g.data.materials.clear()
    g.data.materials.append(gm)
    sun = bpy.data.objects.get("Sun")
    if sun:
        sun.rotation_euler = (math.radians(45), 0, math.radians(-30))
        sun.data.energy = 3.0
    sc.view_settings.view_transform = "Standard"


def shoot(path, target, distance, width=1600, height=1000, lens=40, elev=14, yaw=32, solo=None, show_avatar=True):
    """Level camera (no roll) looking at `target` from `yaw` degrees off the front, `elev` up.
    solo: collection names to keep visible (the avatar and preview props always stay)."""
    sc = bpy.context.scene
    for c in bpy.data.collections:
        c.hide_render = bool(solo) and c.name not in set(solo) | {"Avatar", "PreviewProps"}
    if "Avatar" in bpy.data.collections:
        bpy.data.collections["Avatar"].hide_render = not show_avatar
    props = bpy.data.collections.get("PreviewProps")
    for o in (props.objects if props else ()):
        o.hide_render = bool(solo) and (o.matrix_world.translation.xy - Vector(target).xy).length > 6
    cam = bpy.data.objects.get("PreviewCam")
    if not cam:
        cam = bpy.data.objects.new("PreviewCam", bpy.data.cameras.new("PreviewCam"))
        sc.collection.objects.link(cam)
    cam.data.lens = lens
    e, a = math.radians(elev), math.radians(yaw)
    t = Vector(target)
    cam.location = t + Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e))) * distance
    cam.rotation_euler = (t - cam.location).to_track_quat("-Z", "Y").to_euler()
    sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = width, height
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)


SKILLS = "C:/Users/Allen/.claude/plugins/cache/blender-agent-skills/blender-agent-skills/1.1.0/skills"


def _skill(module, sub):
    """Import a script from an installed Blender agent skill (fresh each call)."""
    import importlib, os, sys
    p = os.path.join(SKILLS, sub, "scripts")
    if p not in sys.path:
        sys.path.insert(0, p)
    return importlib.reload(importlib.import_module(module))


def export_fbx(folder, names=EXPORT):
    """One FBX per model with the blender-export-pipelines `roblox` preset (FBX unit scale, triangulated,
    textures copied and embedded), each with its root moved to the origin."""
    import os
    exp = _skill("export_asset", "blender-export-pipelines")
    results = [exp.run(preset="roblox", collection=n, out=os.path.join(folder, n + ".fbx"), batch=True, no_anim=True)
               for n in names]
    bpy.ops.object.select_all(action="DESELECT")
    return results


def qa(names=EXPORT, profile="roblox"):
    """blender-asset-qa check, one model at a time."""
    q = _skill("qa_check", "blender-asset-qa")
    return {n: q.run(objects=[o.name for o in bpy.data.collections[n].objects if o.type == "MESH"], profile=profile)
            for n in names}


def zfight_check():
    """Print pairs of objects with coplanar, same-facing, overlapping faces (Z-fighting).
    Downward faces are skipped: bottoms resting on a surface are never seen."""
    from collections import defaultdict
    bpy.context.view_layer.update()
    buckets = defaultdict(list)
    for c in bpy.data.collections:
        for o in c.objects:
            if o.type != "MESH":
                continue
            M = o.matrix_world
            R = M.to_3x3().inverted().transposed()
            for f in o.data.polygons:
                if f.area < 1e-5:
                    continue
                n = (R @ f.normal).normalized()
                if n.z < -0.9:
                    continue
                vs = [M @ o.data.vertices[i].co for i in f.vertices]
                key = (round(n.x, 2), round(n.y, 2), round(n.z, 2), round(n.dot(vs[0]), 3))
                lo = [min(v[k] for v in vs) for k in range(3)]
                hi = [max(v[k] for v in vs) for k in range(3)]
                buckets[key].append((o.name, lo, hi))
    hits = set()
    for fs in buckets.values():
        for i, a in enumerate(fs):
            for b in fs[i + 1:]:
                if a[0] != b[0] and all(min(a[2][k], b[2][k]) - max(a[1][k], b[1][k]) > 1e-3
                                        or a[2][k] - a[1][k] < 1e-4 for k in range(3)):
                    hits.add(tuple(sorted((a[0], b[0]))))
    for h in sorted(hits):
        print("Z-fight:", *h)
    print("z-fight pairs:", len(hits))
    return hits


if __name__ == "__main__":
    build_all()
    preview_setup()
    zfight_check()

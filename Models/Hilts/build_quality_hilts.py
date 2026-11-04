# Hilt quality pass (2026-10-29): the real-sword hilts rebuilt or refined against references, for Sell Swords!.
# Runs after the earlier hilt helpers, in one namespace:
#   ns = {"__name__": "lib"}
#   for f in ("Models/Stations/build_stations.py", "Models/Hilts/build_hilt.py", "Models/Hilts/build_western_hilts.py",
#             "Models/Hilts/build_more_hilts.py", "Models/Hilts/build_fictional_hilts.py",
#             "Models/Hilts/build_quality_hilts.py"):
#       exec(open(f).read(), ns)
#   ns["build_quality"](); ns["export_western"](folder, kinds=ns["QUALITY"])
# Same frame as the earlier hilts: studs, root empty at the grip centre, the grip up +Z toward the pommel, the blade
# toward -Z; single edges (and knuckle bows) toward -X, flats face +-Y. Each hilt is <Prefix>Grip / Guard / Pommel,
# renamed to exactly Grip / Guard / Pommel on export. The review blades are the game's finished blades
# (Models/Hilts/Quality/blades.json, from Studio's BladeCore), placed as Hilts.span / HiltSeat place them.
# Checks: blender-asset-qa qa_check.py --profile roblox; Models/Hilts/Quality/iou.py (front-silhouette IoU against
# References/Sword Silhouettes/common-sword-silhouettes-v1.png); reference measurements in the session note.
import math
import json
import os
import bmesh
from mathutils import Vector

VAULT = "C:/Users/Allen/Documents/Create Swords!/"
QDIR = VAULT + "Models/Hilts/Quality/"
QBLADES = json.load(open(QDIR + "blades.json"))
OLD_BUILDERS = dict(MORE_BUILDERS)
OLD_BUILDERS.update(BUILDERS)
BLADE_KEY = dict(Machete="machete", Scimitar="scimitar", Cutlass="cutlass", Jian="jian", Khopesh="khopesh",
                 Dao="dadao", Rapier="rapier", HookSword="hooksword", Claymore="claymore", Flamberge="flamberge",
                 Longsword="longsword", Falchion="falchion", Gladius="gladius")
X_ = Vector((1, 0, 0))
Z_ = Vector((0, 0, 1))


# ---------------------------------------------------------------- review blade (not exported)
def quality_blade(root, key, bo, name, max_cm=None):
    """The game's finished blade from the station rows: spine / ridge / edge on both faces, the blade root at -bo."""
    b = QBLADES[key]
    rows = b["rows"]
    c = bpy.data.collections.get("PreviewBlades") or bpy.data.collections.new("PreviewBlades")
    if c.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(c)
    bm = bmesh.new()
    rings = []
    if max_cm:
        rows = [r for r in rows if r[0] <= max_cm] or rows[:2]
    for px, py, a, s, e, th, rg in rows:
        rp = s + rg * (e - s)
        ring = []
        for side in (1, -1):
            for w, h in (((s, 0.012), (rp, th / 2), (e, 0.012)) if side > 0 else ((e, 0.012), (rp, th / 2), (s, 0.012))):
                x, y = px - math.sin(a) * w, py + math.cos(a) * w
                ring.append(bm.verts.new((0.05 * y, side * 0.05 * h, -(bo + 0.05 * x))))
        rings.append(ring)
    for A, B in zip(rings, rings[1:]):
        for k in range(6):
            m = (k + 1) % 6
            bm.faces.new((A[k], A[m], B[m], B[k]))
    bm.faces.new(rings[0][::-1])
    bm.faces.new(rings[-1])
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-6)
    _outward(bm)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(mat("steel"))
    o = bpy.data.objects.new(name, me)
    c.objects.link(o)
    o.parent = root
    return o


# ---------------------------------------------------------------- geometry helpers
def band(name, path, width, wrap, inward, thick, n=9, seg_cap=True):
    """A curved sheet-metal band along a planar path (list of Vectors): at each path point the section is an arc across
    Y of half width width(u), its edges curled by wrap(u) toward inward(u, point, tangent) (a unit Vector, the side the
    hand is on), thick studs thick toward that side. Closed solid: outer arc, inner arc, flat rims and strip end caps."""
    N = len(path)
    rings = []
    for i, p in enumerate(path):
        u = i / (N - 1)
        a, b = path[max(i - 1, 0)], path[min(i + 1, N - 1)]
        T = (b - a).normalized()
        nin = inward(u, p, T)
        W, D = width(u), wrap(u)
        outer, inner = [], []
        for j in range(n):
            s = -1 + 2 * j / (n - 1)
            cy, cn = s * W, D * s * s
            ty, tn = W, 2 * D * s                  # tangent of the section arc
            ln = math.hypot(ty, tn) or 1.0
            ny, nn = -tn / ln, ty / ln              # its normal toward the inward side
            q = p + Vector((0, cy, 0)) + nin * cn
            outer.append(q)
            inner.append(q + Vector((0, ny * thick, 0)) + nin * (nn * thick))
        rings.append(outer + inner[::-1])
    bm = bmesh.new()
    V = [[bm.verts.new(q) for q in r] for r in rings]
    M = 2 * n
    for A, B in zip(V, V[1:]):
        for k in range(M):
            m = (k + 1) % M
            bm.faces.new((A[k], A[m], B[m], B[k]))
    for R, flip in ((V[0], True), (V[-1], False)):
        for j in range(n - 1):
            f = (R[j], R[j + 1], R[M - 2 - j], R[M - 1 - j])
            bm.faces.new(f[::-1] if flip else f)
    _outward(bm)
    return mesh_obj(name, bm, "neutral")


def plate(name, pts, t, te=0.45, dr=0.02, h=0.06, taper=None, y0=0.0):
    """slab() with its middle plane moved to y = y0."""
    o = slab(name, pts, t, te=te, dr=dr, h=h, taper=taper)
    if y0:
        for v in o.data.vertices:
            v.co.y += y0
    return o


def arc_pts(c, r, a0, a1, n):
    return [(c[0] + r * math.cos(a0 + (a1 - a0) * i / n), c[1] + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def tris(o):
    return sum(len(p.vertices) - 2 for p in o.data.polygons)


# ---------------------------------------------------------------- silhouettes and review sheets
def _only(objs):
    keep = set(o.name for o in objs)
    for o in bpy.context.scene.objects:
        o.hide_render = o.name not in keep


def hilt_objects(kind, coll=None):
    c = bpy.data.collections[coll or kind + "HiltGame"]
    return [o for o in c.objects if o.type == "MESH"]


def silhouette(kind, path, coll=None, blade=None, ppu=400):
    """Front (flat) silhouette, camera looking +Y, alpha = sword. Returns the frame: ppu, centre x/z, size."""
    objs = hilt_objects(kind, coll) + ([blade] if blade else [])
    bpy.context.view_layer.update()
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    x0, x1 = min(p.x for p in pts) - 0.05, max(p.x for p in pts) + 0.05
    z0, z1 = min(p.z for p in pts) - 0.05, max(p.z for p in pts) + 0.05
    sc = bpy.context.scene
    try:
        sc.render.engine = "BLENDER_WORKBENCH"
    except TypeError:
        pass
    sh = sc.display.shading
    sh.light, sh.color_type = "FLAT", "SINGLE"
    sh.single_color = (0, 0, 0)
    sc.render.film_transparent = True
    sc.view_settings.view_transform = "Standard"
    cam = bpy.data.objects.get("SilCamQ") or bpy.data.objects.new("SilCamQ", bpy.data.cameras.new("SilCamQ"))
    if cam.name not in sc.collection.objects:
        sc.collection.objects.link(cam)
    cam.data.type = "ORTHO"
    w, h = x1 - x0, z1 - z0
    cam.data.ortho_scale = max(w, h)
    cam.data.clip_end = 100
    cam.location = ((x0 + x1) / 2, -20, (z0 + z1) / 2)
    cam.rotation_euler = (math.radians(90), 0, 0)
    sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = max(8, round(w * ppu)), max(8, round(h * ppu))
    sc.render.resolution_percentage = 100
    # ortho_scale spans the larger side; make ppu exact on both
    cam.data.sensor_fit = "AUTO"
    sc.render.filepath = path
    _only(objs)
    bpy.ops.render.render(write_still=True)
    for o in sc.objects:
        o.hide_render = False
    return dict(ppu=ppu, cx=(x0 + x1) / 2, cz=(z0 + z1) / 2, w=w, h=h, root_x=objs[0].parent.location.x if objs[0].parent else 0)


def review_colours(objs):
    """Leather grip, steel guard, brass pommel (review only; the game colours the parts by tier)."""
    PAL.setdefault("brass", (0.86, 0.72, 0.42))
    for o in objs:
        role = o.name.split("_", 1)[1]
        key = {"Grip": "leather", "Guard": "steel", "Pommel": "brass"}.get(role)
        if key:
            o.data.materials.clear()
            o.data.materials.append(mat(key))


def review_sheet(kind, path, coll=None, blade=None, res=480):
    """blender-asset-qa review_shots, front / edge (right) / three-quarter: material colours on the top row, wire on
    the bottom row, in one sheet."""
    import numpy as np
    rs = _skill("review_shots", "blender-asset-qa")
    hobjs = hilt_objects(kind, coll)
    review_colours(hobjs)
    objs = [o.name for o in hobjs] + ([blade.name] if blade else [])
    rows = []
    for mode in ("material", "wire"):
        r = rs.run(objects=objs, out=path + "." + mode + ".png", views=["front", "right", "three_quarter"], mode=mode, res=res)
        imgs = [bpy.data.images.load(v) for v in r["views"]]
        arr = [np.array(i.pixels[:], dtype=np.float32).reshape(i.size[1], i.size[0], 4) for i in imgs]
        rows.append(np.concatenate(arr, 1))
        for i in imgs:
            bpy.data.images.remove(i)
        for v in r["views"] + [r["sheet"]]:
            if os.path.exists(v):
                os.remove(v)
    full = np.concatenate(rows[::-1], 0)
    out = bpy.data.images.new("QSheet", full.shape[1], full.shape[0])
    out.pixels.foreach_set(full.ravel())
    out.filepath_raw, out.file_format = path, "PNG"
    out.save()
    bpy.data.images.remove(out)
    return path


def qa(kind, coll=None, blade=None, tol=0.008):
    q = _skill("qa_check", "blender-asset-qa")
    objs = [o.name for o in hilt_objects(kind, coll)] + ([blade.name] if blade else [])
    return q.run(objects=objs, profile="roblox", tol=tol)


# ---------------------------------------------------------------- the hilts
# Each builder returns (root, numbers): GripLength / BladeOffset / Back as built. Grip lengths and blade offsets are
# the game's (unchanged); Back follows the new pommels. Reference numbers: Sessions/2026-10-29 "Hilt quality pass".
QUALITY = dict(
    Cutlass=dict(grip=0.62, blade_offset=0.45), Rapier=dict(grip=0.85, blade_offset=0.6),
    Khopesh=dict(grip=0.55, blade_offset=0.3), Scimitar=dict(grip=0.65, blade_offset=0.4),
    Flamberge=dict(grip=1.45, blade_offset=0.75), Claymore=dict(grip=1.5, blade_offset=0.95),
    Jian=dict(grip=0.8, blade_offset=0.5), Dao=dict(grip=1.2, blade_offset=0.66), HookSword=dict(grip=0.7, blade_offset=0.45),
    Machete=dict(grip=0.65, blade_offset=0.38), Longsword=dict(grip=1.15, blade_offset=0.7),
    Falchion=dict(grip=0.72, blade_offset=0.44), Gladius=dict(grip=0.56, blade_offset=0.42),
)


def toward(c):
    """inward() for band(): the in-plane normal of the path that points toward point c (the hand's side)."""
    c = Vector(c)

    def f(u, p, T):
        n = Vector((0, 1, 0)).cross(T).normalized()
        return n if n.dot(c - p) > 0 else -n
    return f


def build_cutlass_q(x=0, y=0, name="CutlassHiltGame", p="CU_"):
    """Naval cutlass (British 1845/1858, US 1860/1917): a sheet-steel half-basket. A wide bowl under the hand, its
    spine-side trailing end turned out, running round the knuckle side as a broad plate that narrows into the pommel
    cap; its sides curl round the hand. Ring-grooved grip, backstrap and a small cap pommel."""
    W = QUALITY["Cutlass"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    base = lambda z: 0.94 + 0.06 * (1 - (2 * z / L) ** 2)
    wrap_grip(p + "Grip", g0, g1, 0.07, 0.056, base, pitch=0.045, amp=0.075, tilt=0.0, seg=14, tuck=0.03)
    path = spline([(0.33, 0, -0.42), (0.2, 0, -0.455), (0.05, 0, -0.462), (-0.12, 0, -0.455), (-0.25, 0, -0.425),
                   (-0.33, 0, -0.36), (-0.365, 0, -0.24), (-0.37, 0, -0.07), (-0.345, 0, 0.07), (-0.275, 0, 0.19),
                   (-0.17, 0, 0.285), (-0.07, 0, 0.34), (-0.02, 0, 0.35)], per=3)
    wid = table([(0, 0.05), (0.05, 0.15), (0.12, 0.25), (0.22, 0.3), (0.36, 0.28), (0.55, 0.22), (0.8, 0.13), (1, 0.07)])
    wrp = table([(0, 0.02), (0.15, 0.09), (0.3, 0.11), (0.6, 0.09), (0.85, 0.04), (1, 0.01)])
    shell = band("_shell", path, wid, wrp, toward((-0.03, 0, -0.05)), 0.022, n=9)
    ferrule = block("_ferrule", -0.445, g0 + 0.03, 0.08, 0.064, 0.074, 0.06, chamfer=0.006)
    join(p + "Guard", [shell, ferrule])
    zs = grip_stations(g0 - 0.01, g1 + 0.01, [], step=0.1)
    strap = stack("_strap", [(z, 0.018, 0.026, 0.07 * base(z) + 0.004) for z in zs], seg=12, n=4.0)
    cap = stack("_cap", [(g1 - 0.01, 0.086, 0.07), (g1 + 0.02, 0.098, 0.078), (g1 + 0.05, 0.088, 0.07),
                         (g1 + 0.072, 0.055, 0.044), (g1 + 0.08, 0, 0)], seg=16)
    join(p + "Pommel", [strap, cap])
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(g1 + 0.08, 4))


def build_rapier_q(x=0, y=0, name="RapierHiltGame", p="RA_"):
    """Swept-hilt rapier (c. 1580-1630; V&A O97278, Met 14.25.1053, Greig Watson repro): long straight quillons with
    baluster ends, two pas d'ane rings over the ricasso, a side ring on the outer face, a knuckle bow on the edge side
    and three swept bars (two outer, one inner) from the ring and block to the bow; wire grip with turk's heads,
    inverted-fig pommel."""
    W = QUALITY["Rapier"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    base = lambda z: 0.9 + 0.1 * (1 - (2 * z / L) ** 2)
    wrap_grip(p + "Grip", g0, g1, 0.066, 0.056, base, pitch=0.05, amp=0.08, tilt=0.018, seg=12, band=0.04)
    zq = -0.47
    r = 0.021
    blk = block("_block", zq - 0.035, g0 + 0.005, 0.075, 0.06, 0.07, 0.055, chamfer=0.006)
    size = table([(0, 0.024), (0.8, 0.019), (0.87, 0.028), (0.93, 0.034), (0.975, 0.024), (1, 0)])
    quill = arm_bar("_quill", 1.32, zq, size, n=2.0, seg=8)
    parts = [blk, quill]
    # pas d'ane: two rings in the blade's plane, either side of the ricasso
    for s in (-1, 1):
        parts.append(loop("_pas%d" % s, circle((s * 0.12, s * 0.008, zq - 0.2), (1, 0, 0), (0, 0, 1), 0.175, 0.2, 18), r, seg=6))
    # side ring on the outer face (+Y), under the quillons
    ring_c = Vector((0.0, 0.11, zq + 0.285))
    parts.append(loop("_side", circle(ring_c, (1, 0, 0), (0, 0, 1), 0.32, 0.28, 22), r, seg=6))
    parts.append(tube("_sidepost", [Vector((0, 0.03, zq + 0.01)), Vector((0, 0.07, zq + 0.01)), Vector((0, 0.115, zq + 0.01))],
                      r, up=X_, seg=6))
    # knuckle bow, edge side
    bow = spline([(-0.05, 0, zq + 0.01), (-0.22, 0, zq + 0.07), (-0.36, 0, zq + 0.24), (-0.405, 0, zq + 0.47),
                  (-0.38, 0, 0.17), (-0.27, 0, 0.33), (-0.1, 0, 0.41), (-0.05, 0, g1 + 0.01)], per=4)
    parts.append(tube("_bow", bow, lambda u: 0.026 - 0.004 * u, seg=8))  # bow keeps 8 sides: the most seen bar

    def on_bow(z):
        q = min(bow, key=lambda v: abs(v.z - z))
        return (q.x, 0.0, q.z)
    # two swept bars on the outer face: one from the quillon block, one from the side ring, both into the bow
    for pts in ([(0.05, 0.05, zq + 0.02), (0.02, 0.15, zq + 0.24), (-0.17, 0.13, zq + 0.4), on_bow(zq + 0.43)],
                [(0.31, 0.11, zq + 0.2), (0.16, 0.17, zq + 0.45), (-0.1, 0.12, zq + 0.62), on_bow(0.13)]):
        parts.append(tube("_bar", spline(pts, per=5), r, seg=6))
    join(p + "Guard", parts)
    collar = block("_collar", g1 - 0.005, g1 + 0.04, 0.07, 0.06, 0.06, 0.052, chamfer=0.006)
    z0, H = g1 + 0.03, 0.235
    prof = table([(0, 0.05), (0.12, 0.075), (0.35, 0.122), (0.55, 0.132), (0.75, 0.12), (0.9, 0.08), (1, 0.03)])
    fig = stack("_fig", [(z0 + H * s, prof(s), prof(s) * 0.9) for s in
                         (0, 0.08, 0.17, 0.27, 0.38, 0.5, 0.62, 0.73, 0.83, 0.91, 0.96, 1.0)], seg=12)
    btn = knob("_btn", z0 + H - 0.006, 0.028, 0.02, seg=10)
    join(p + "Pommel", [collar, fig, btn])
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(z0 + H - 0.006 + 0.02, 4))


def fluted(a, b, flutes, depth, seg):
    """Oval section a x b with `flutes` rounded grooves (depth relative), counter-clockwise points."""
    out = []
    for i in range(seg):
        t = 2 * math.pi * i / seg
        k = 1 - depth * (0.5 - 0.5 * math.cos(flutes * t))
        out.append((a * k * math.cos(t), b * k * math.sin(t)))
    return out


def build_khopesh_q(x=0, y=0, name="KhopeshHiltGame", p="KH_"):
    """Egyptian khopesh (Louvre E 25689, Met 11.166.1, Tutankhamun's): a broad cast hilt with raised flanges framing
    inlaid scales, no crossguard (the hilt flares straight into the shaft) and a flat fan pommel with a crescent top."""
    W = QUALITY["Khopesh"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    bands = (-0.2, 0.2)
    sc = riser_scale(lambda z: 0.9 + 0.1 * (z - g0) / L, bands, h=0.06, w=0.018)
    loft(p + "Grip", [zring(oval(0.092 * sc(z), 0.062 * sc(z), 3.2, 18), z)
                      for z in grip_stations(g0 - 0.015, g1 + 0.015,
                                             [r + d for r in bands for d in (-0.018, -0.011, 0.011, 0.018)], step=0.06)])
    # guard: the hilt's flared shoulder running into the blade's shaft (0.09 x 0.05 there)
    stack(p + "Guard", [(-bo, 0.056, 0.033), (-bo + 0.012, 0.062, 0.038), (-bo + 0.035, 0.08, 0.05),
                        (g0 + 0.02, 0.092, 0.06), (g0 + 0.03, 0.088, 0.058)], seg=18, n=3.2)
    # pommel: a fan flaring from the grip end, its top a shallow crescent with rounded horns, thinner toward them
    top = g1 + 0.135
    fan = [(-0.1, g1 - 0.02), (-0.13, g1 + 0.03), (-0.165, g1 + 0.08), (-0.19, g1 + 0.12), (-0.19, top),
           (-0.17, top + 0.008), (-0.12, top - 0.012), (-0.06, top - 0.03), (0.0, top - 0.035)]
    pts = fan + [(-px, pz) for px, pz in reversed(fan[:-1])]
    plate(p + "Pommel", pts[::-1], 0.155, te=0.5, dr=0.03, h=0.05,
          taper=lambda px, pz: 1 - 0.45 * min(1.0, abs(px) / 0.19) ** 1.5)
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(top + 0.008, 4))


def build_scimitar_q(x=0, y=0, name="ScimitarHiltGame", p="SC_"):
    """Persian shamshir / Ottoman kilij: a short cross with langets and down-turned, bulbous quillon ends; a pistol grip
    whose end bends toward the edge into a bird's-head pommel cap hooking back toward the blade."""
    W = QUALITY["Scimitar"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    Rb, zb = 0.42, g1 - 0.2
    th = 0.2 / Rb
    arc = lambda a: Vector((-Rb + Rb * math.cos(a), 0, zb + Rb * math.sin(a)))
    path = [Vector((0, 0, z)) for z in (g0 - 0.02, g0 + 0.06, g0 + 0.16, g0 + 0.26, g0 + 0.36, zb)]
    path += [arc(th * i / 5) for i in range(1, 6)]
    rad = table([(0, 0.066), (0.4, 0.07), (0.75, 0.076), (1, 0.08)])
    tube(p + "Grip", path, rad, seg=16, ry=0.74)
    # guard: block, quillons sloping toward the hand with drop-shaped ends, pointed langets on both flats
    blk = block("_block", -bo, g0 + 0.015, 0.09, 0.054, 0.075, 0.052, chamfer=0.006)
    size = table([(0, 0.032), (0.6, 0.025), (0.8, 0.028), (0.88, 0.044), (0.94, 0.048), (0.985, 0.034), (1, 0)])
    curve = lambda t: 0.12 * max(0.0, (t - 0.4) / 0.6) ** 2
    arms = arm_bar("_arms", 0.8, -bo + 0.035, size, curve, n=2.0, seg=12)
    parts = [blk, arms]
    lw = table([(0, 0.036), (0.6, 0.024), (0.85, 0.012), (1, 0)])
    for s in (-1, 1):
        parts.append(stack("_down%d" % s, [(-bo + 0.03 - 0.17 * u, lw(u), 0.007 if u < 1 else 0, 0, s * 0.028)
                                           for u in (0, 0.4, 0.7, 0.88, 1.0)], seg=10, n=4.0))
        parts.append(stack("_up%d" % s, [(g0 + 0.12 * u, lw(u) * 0.9, 0.007 if u < 1 else 0, 0, s * 0.052)
                                         for u in (0, 0.4, 0.7, 0.88, 1.0)], seg=10, n=4.0))
    join(p + "Guard", parts)
    # pommel: a cap continuing the bend, swelling into a head and hooking down into a beak on the edge side
    e = arc(th)
    d = Vector((-math.sin(th), 0, math.cos(th)))
    head = spline([tuple(e - d * 0.05), tuple(e), tuple(e + d * 0.06 + Vector((-0.02, 0, 0))),
                   tuple(e + d * 0.075 + Vector((-0.1, 0, -0.01))), tuple(e + d * 0.02 + Vector((-0.19, 0, -0.08)))], per=4)
    capr = table([(0, 0.083), (0.15, 0.09), (0.4, 0.094), (0.6, 0.075), (0.8, 0.045), (1, 0.012)])
    cap = tube(p + "Pommel", head, capr, seg=16, ry=0.78)
    top = max(v.co.z for v in cap.data.vertices)
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(top, 4))


def build_flamberge_q(x=0, y=0, name="FlambergeHiltGame", p="FL_"):
    """German two-hander (Cleveland 1919.70: cross 53.7, grip 43.2, ricasso 34.7 cm; Brunswick 1574; Christie's
    mid-16th c.): a long cross with flared ends, side rings on both faces, a leather-covered ricasso ending in
    flame-shaped parrying lugs (Parierhaken), a grip tapering toward a large fluted fig pommel."""
    W = QUALITY["Flamberge"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    risers = (-0.25, 0.25)
    sc = riser_scale(lambda z: 1.0 - 0.15 * (z - g0) / L, risers, h=0.08)
    grip = loft("_grip", [zring(oval(0.125 * sc(z), 0.095 * sc(z), 2.3, 16), z)
                          for z in grip_stations(g0 - 0.015, g1 + 0.015,
                                                 [r + d for r in risers for d in (-0.022, -0.0132, 0.0132, 0.022)],
                                                 step=0.12)])
    # leather sleeve over the ricasso (the blade is 0.2 x 0.05 there), tied at both ends, in the grip's colour
    z_end = -bo - 0.62
    ties = (-bo - 0.03, z_end + 0.03)
    ssc = riser_scale(lambda z: 1.0, ties, h=0.12, w=0.02)
    sleeve = loft("_sleeve", [zring(oval(0.118 * ssc(z), 0.04 * ssc(z), 2.6, 14), z)
                              for z in grip_stations(z_end, -bo + 0.005,
                                                     [r + d for r in ties for d in (-0.02, -0.012, 0.012, 0.02)],
                                                     step=0.1)])
    join(p + "Grip", [grip, sleeve])
    blk = block("_block", -bo, g0 + 0.01, 0.12, 0.058, 0.1, 0.058, chamfer=0.006)
    size = table([(0, 0.032), (0.2, 0.03), (0.72, 0.026), (0.88, 0.032), (0.94, 0.045), (0.975, 0.04), (0.995, 0.02), (1, 0)])
    arms = arm_bar("_arms", 1.8, -bo + 0.034, size, n=3.0, seg=12)
    parts = [blk, arms]
    for s in (-1, 1):
        d = Vector((0, s * 0.36, -0.933)).normalized()
        c = Vector((0, s * 0.045, -bo + 0.015)) + d * 0.15
        parts.append(loop("_ring%d" % s, circle(c, X_, d, 0.15, 0.15, 20), 0.018, up=X_.cross(d), seg=6))
    # flame lugs at the sleeve's end: flat tongues out from both edges, curling back toward the hand in two waves
    zl = z_end + 0.02
    half = [(0.1, zl - 0.05), (0.17, zl - 0.06), (0.23, zl - 0.04), (0.27, zl - 0.005), (0.315, zl + 0.015),
            (0.27, zl + 0.05), (0.28, zl + 0.09), (0.33, zl + 0.125), (0.28, zl + 0.15), (0.29, zl + 0.2),
            (0.345, zl + 0.27), (0.27, zl + 0.23), (0.225, zl + 0.17), (0.2, zl + 0.11), (0.17, zl + 0.07),
            (0.13, zl + 0.045), (0.1, zl + 0.04)]
    for s in (-1, 1):
        pts = [(s * px, pz) for px, pz in half]
        parts.append(plate("_lug%d" % s, pts if s > 0 else pts[::-1], 0.05, te=0.45, dr=0.018, h=0.04,
                           taper=lambda px, pz: 1 - 0.55 * min(1.0, max(0.0, (abs(px) - 0.12) / 0.18))))
    join(p + "Guard", parts)
    collar = block("_collar", g1 - 0.005, g1 + 0.05, 0.09, 0.072, 0.078, 0.064, chamfer=0.006)
    z0, H = g1 + 0.04, 0.3
    pr = table([(0, 0.07), (0.12, 0.1), (0.3, 0.162), (0.5, 0.198), (0.66, 0.2), (0.8, 0.172), (0.92, 0.112), (1.0, 0.058)])
    us = (0, 0.1, 0.22, 0.36, 0.5, 0.62, 0.74, 0.84, 0.92, 1.0)
    fig = loft("_fig", [zring(fluted(pr(u), pr(u) * 0.94, 8, 0.12 * math.sin(math.pi * min(1.0, u * 1.1)), 24), z0 + H * u)
                        for u in us])
    btn = knob("_btn", z0 + H - 0.006, 0.034, 0.03, seg=12)
    join(p + "Pommel", [collar, fig, btn])
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(z0 + H - 0.006 + 0.03, 4))


def build_claymore_q(x=0, y=0, name="ClaymoreHiltGame", p="CL_"):
    """Scottish two-handed claymore (claidheamh mor; Met 27515, Bonhams lot 111): straight quillons of diamond section
    sloping toward the blade, ending in quatrefoils (four rings round a boss), flat langets over the ricasso, a long
    leather grip and a large ball pommel."""
    W = QUALITY["Claymore"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    risers = (-0.42, 0.0, 0.42)
    base = lambda z: 0.9 + 0.1 * (1 - (2 * z / L) ** 2)
    sc = riser_scale(base, risers, h=0.08)
    loft(p + "Grip", [zring(oval(0.125 * sc(z), 0.095 * sc(z), 2.3, 14), z)
                      for z in grip_stations(g0 - 0.015, g1 + 0.015,
                                             [r + d for r in risers for d in (-0.022, -0.0132, 0.0132, 0.022)],
                                             step=0.15)])
    parts = [block("_ecu", -bo, g0 + 0.01, 0.17, 0.072, 0.11, 0.07, seg=16)]
    ang = math.radians(25)
    for s in (-1, 1):
        lw = table([(0, 0.055), (0.6, 0.045), (0.85, 0.03), (0.97, 0.012), (1, 0)])
        parts.append(stack("_langet%d" % s, [(-bo + 0.05 - 0.27 * u, lw(u), 0.007 if u < 1 else 0, 0, s * 0.028)
                                             for u in (0, 0.3, 0.6, 0.85, 0.97, 1.0)], seg=10, n=4.0))
        a0 = Vector((s * 0.06, 0, -bo + 0.05))
        dvec = Vector((s * math.cos(ang), 0, -math.sin(ang)))
        path = [a0 + dvec * (0.68 * i / 6) for i in range(7)]
        parts.append(tube("_arm%d" % s, path, lambda u: 0.062 - 0.022 * u, seg=4))
        c = path[-1] + dvec * 0.075
        q = Y.cross(dvec)
        parts.append(ball("_boss%d" % s, c, 0.05, 0.04, 0.05, seg=10, lat=5))
        for j in range(4):
            phi = math.pi / 4 + j * math.pi / 2
            lc = c + (dvec * math.cos(phi) + q * math.sin(phi)) * 0.082 + Y * (0.004 if j % 2 else -0.004)
            parts.append(loop("_lobe%d%d" % (s, j), circle(lc, (1, 0, 0), (0, 0, 1), 0.058, 0.058, 10),
                              0.021, seg=5, ry=1.3))
    join(p + "Guard", parts)
    collar = block("_collar", g1 - 0.005, g1 + 0.055, 0.1, 0.08, 0.085, 0.068, chamfer=0.007)
    rz = 0.19
    zc = g1 + 0.05 + rz - 0.03
    b = ball("_ball", (0, 0, zc), 0.215, 0.18, rz, seg=16, lat=8)
    peen = knob("_peen", zc + rz - 0.008, 0.032, 0.035, seg=10)
    join(p + "Pommel", [collar, b, peen])
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(zc + rz - 0.008 + 0.035, 4))


def build_longsword_q(x=0, y=0, name="LongswordHiltGame", p="LO_"):
    """Late-medieval longsword (Oakeshott XVIIIa; Albion Regent: guard 24.4, grip 19, pommel 7.6 cm): a straight cross
    of square section with knobbed ends over a small ecusson, a leather grip with risers, a large wheel pommel."""
    W = QUALITY["Longsword"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    risers = (-0.29, 0.0, 0.29)
    base = lambda z: 0.92 + 0.08 * (1 - (z / (L / 2)) ** 2)
    sc = riser_scale(base, risers, h=0.09)
    loft(p + "Grip", [zring(oval(0.108 * sc(z), 0.08 * sc(z), 2.3, 16), z)
                      for z in grip_stations(g0 - 0.015, g1 + 0.015,
                                             [r + d for r in risers for d in (-0.022, -0.0132, 0.0132, 0.022)],
                                             step=0.08)])
    ecu = block("_ecu", -bo, g0, 0.145, 0.066, 0.095, 0.066)
    size = table([(0, 0.046), (0.2, 0.044), (0.78, 0.034), (0.88, 0.04), (0.945, 0.064), (0.985, 0.054), (1, 0)])
    arms = arm_bar("_arms", 1.36, -bo + 0.05, size)
    join(p + "Guard", [ecu, arms])
    R = 0.18
    zc = g1 + 0.03 + R - 0.03
    collar = block("_collar", g1, g1 + 0.05, 0.1, 0.076, 0.09, 0.07, chamfer=0.006)
    wheel = disc("_wheel", zc, [(0, -0.07), (0.06, -0.07), (0.072, -0.064), (0.078, -0.05), (0.15, -0.05),
                                (0.168, -0.044), (R, -0.03), (R, 0.03), (0.168, 0.044), (0.15, 0.05),
                                (0.078, 0.05), (0.072, 0.064), (0.06, 0.07), (0, 0.07)], seg=32)
    peen = knob("_peen", zc + R - 0.008, 0.028, 0.032)
    join(p + "Pommel", [collar, wheel, peen])
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(zc + R - 0.008 + 0.032, 4))


def build_falchion_q(x=0, y=0, name="FalchionHiltGame", p="FA_"):
    """Medieval falchion (Conyers: cross 16.8, grip 9.5, wheel pommel 4.2 cm; Thorpe: guard 19.6, grip 10 cm): a long
    straight cross turning down toward the blade at knobbed ends, a plain grip, a bevelled wheel pommel."""
    W = QUALITY["Falchion"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    base = lambda z: 0.9 + 0.1 * (1 - (z / (L / 2)) ** 2)
    loft(p + "Grip", [zring(oval(0.08 * base(z), 0.064 * base(z), 2.2, 18), z)
                      for z in grip_stations(g0 - 0.015, g1 + 0.015, [], step=0.09)])
    blk = block("_block", -bo, g0, 0.12, 0.064, 0.088, 0.064)
    size = table([(0, 0.042), (0.82, 0.034), (0.92, 0.045), (0.965, 0.038), (0.995, 0.02), (1, 0)])
    curve = lambda t: 0.085 * max(0.0, (t - 0.5) / 0.5) ** 2
    arms = arm_bar("_arms", 1.16, -bo + 0.04, size, curve, n=3.0, seg=12)
    join(p + "Guard", [blk, arms])
    R = 0.135
    zc = g1 + 0.04 + R - 0.035
    collar = block("_collar", g1, g1 + 0.04, 0.084, 0.068, 0.078, 0.064, chamfer=0.006)
    wheel = disc("_wheel", zc, [(0, -0.07), (0.045, -0.07), (0.052, -0.062), (0.056, -0.05), (0.1, -0.05),
                                (0.112, -0.045), (R, -0.026), (R, 0.026), (0.112, 0.045), (0.1, 0.05),
                                (0.056, 0.05), (0.052, 0.062), (0.045, 0.07), (0, 0.07)], seg=28)
    join(p + "Pommel", [collar, wheel])
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(zc + R, 4))


def build_gladius_q(x=0, y=0, name="GladiusHiltGame", p="GL_"):
    """Roman gladius (Pompeii type; Windlass/SBG: guard 7.3 wide and 3.2 cm deep, grip 8.9 cm with four finger ridges,
    pommel about 6.3 cm): an oval cushion handguard on a blade plate, a ridged bone grip, a big ovoid pommel and nut."""
    W = QUALITY["Gladius"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    ridge = lambda z: 0.8 + 0.2 * (0.5 + 0.5 * math.cos(2 * math.pi * (z - g0) / (L / 4) - math.pi))
    zs = [g0 - 0.015] + [g0 + L * i / 24 for i in range(25)] + [g1 + 0.015]
    loft(p + "Grip", [zring(oval(0.078 * ridge(z), 0.068 * ridge(z), 2.0, 8, math.pi / 8), z) for z in zs])
    plate_ = block("_plate", -bo, -bo + 0.016, 0.17, 0.11, 0.17, 0.11, chamfer=0.004, n=3.0, seg=32)
    z0, z1 = -bo + 0.01, g0 + 0.035
    prof = [(0.8, z0), (0.95, z0 + 0.014), (1.0, z0 + 0.045), (1.0, z0 + 0.09), (0.95, z1 - 0.03),
            (0.82, z1 - 0.01), (0.62, z1)]
    body = loft("_body", [zring(oval(0.22 * r, 0.145 * r, 2.0, 32), z) for r, z in prof])
    join(p + "Guard", [plate_, body])
    hz = 0.13
    zc = g1 + hz - 0.02
    rings = [[Vector((0, 0, zc - hz))]]
    for i in range(1, 12):
        a = math.pi * i / 12
        rings.append(zring(oval(0.18 * math.sin(a), 0.145 * math.sin(a), 2.0, 24), zc - hz * math.cos(a)))
    rings.append([Vector((0, 0, zc + hz))])
    egg = loft("_egg", rings)
    nut = knob("_nut", zc + hz - 0.012, 0.048, 0.05, seg=12)
    join(p + "Pommel", [egg, nut])
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(zc + hz - 0.012 + 0.05, 4))


def build_hooksword_q(x=0, y=0, name="HookSwordHiltGame", p="HO_"):
    """Qing hook sword (Mandarin Mansion: crescent guard 31.6 x 10.9 cm on two bars, handle about 20 cm, pommel spike
    22 cm): the earlier build with the dagger spike cut to the measured 1.1 x handle."""
    W = QUALITY["HookSword"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    base = lambda z: 0.94 + 0.06 * (1 - (2 * z / L) ** 2)
    wrap_grip(p + "Grip", g0, g1, 0.066, 0.054, base, pitch=0.05, amp=0.06, tilt=0.02, seg=14)
    ferrule = block("_ferrule", -bo, g0 + 0.03, 0.085, 0.066, 0.076, 0.06, chamfer=0.006)
    h, xt, xo, xi, t = 0.55, -0.13, -0.51, -0.37, 0.05
    xo_ = lambda z: xt + (xo - xt) * (1 - (z / h) ** 2)
    xi_ = lambda z: xt + (xi - xt) * (1 - (z / h) ** 2)
    rings = [[Vector((xt, 0, h))]]
    N = 28
    for k in range(1, N):
        z = h * math.cos(math.pi * k / N)
        o, i = xo_(z), xi_(z)
        w = i - o
        e, ch = min(0.035, w * 0.45), min(0.006, w * 0.2)
        th_ = t / 2 * min(1.0, 0.35 + w / 0.06)
        rings.append([Vector(v) for v in ((i, -th_ * 0.6, z), (i - ch, -th_, z), (o + e, -th_, z), (o, 0, z),
                                          (o + e, th_, z), (i - ch, th_, z), (i, th_ * 0.6, z))])
    rings.append([Vector((xt, 0, -h))])
    crescent = loft("_crescent", rings)
    bars = [tube("_bar%d" % j, [Vector((-0.04, 0, z)), Vector((xi_(z) - 0.012, 0, z))], 0.03, seg=10)
            for j, z in enumerate((-0.4, 0.29))]
    join(p + "Guard", [ferrule, crescent] + bars)
    collar = block("_collar", g1 - 0.005, g1 + 0.045, 0.078, 0.064, 0.064, 0.052, chamfer=0.006)
    z0, S_ = g1 + 0.035, 0.78
    taper = table([(0, 1.0), (0.08, 1.06), (0.3, 0.88), (0.7, 0.48), (0.92, 0.15), (1, 0)])
    spike = stack("_spike", [(z0 + S_ * u, 0.05 * taper(u), 0.03 * taper(u))
                             for u in (0, 0.04, 0.08, 0.18, 0.3, 0.45, 0.6, 0.7, 0.8, 0.88, 0.94, 1.0)], seg=4)
    join(p + "Pommel", [collar, spike])
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(z0 + S_, 4))


def build_dao_q(x=0, y=0, name="DaoHiltGame", p="DA_"):
    """Dadao (Mandarin Mansion Republican dadao; Qing saber guard 8.8 x 7.9 cm with a raised rim): a long cord-wrapped
    two-hand grip, an oval guard with a raised rim and a ferrule, a ring pommel."""
    W = QUALITY["Dao"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    base = lambda z: 0.94 + 0.06 * (1 - (2 * z / L) ** 2)
    wrap_grip(p + "Grip", g0, g1, 0.076, 0.062, base, pitch=0.07, amp=0.1, tilt=0.035, seg=14, tuck=0.03)
    disc_ = stack("_disc", [(-bo, 0.178, 0.132), (-bo + 0.008, 0.19, 0.143), (-bo + 0.016, 0.19, 0.143),
                            (-bo + 0.02, 0.176, 0.13), (-bo + 0.032, 0.176, 0.13), (-bo + 0.036, 0.19, 0.143),
                            (-bo + 0.044, 0.19, 0.143), (-bo + 0.052, 0.178, 0.132)], seg=32)
    ferrule = block("_ferrule", -bo + 0.045, g0 + 0.03, 0.09, 0.074, 0.084, 0.069, chamfer=0.006)
    join(p + "Guard", [disc_, ferrule])
    collar = block("_collar", g1 - 0.005, g1 + 0.05, 0.084, 0.07, 0.074, 0.062, chamfer=0.006)
    R, rr = 0.115, 0.026
    zc = g1 + 0.05 + R + rr - 0.022
    ring = loop("_ring", circle((0, 0, zc), (1, 0, 0), (0, 0, 1), R, R, 28), rr, seg=10, ry=1.25)
    join(p + "Pommel", [collar, ring])
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(zc + R + rr, 4))


QBUILD = dict(Cutlass=build_cutlass_q, Rapier=build_rapier_q, Khopesh=build_khopesh_q, Scimitar=build_scimitar_q,
              Flamberge=build_flamberge_q, Claymore=build_claymore_q, Longsword=build_longsword_q,
              Falchion=build_falchion_q, Gladius=build_gladius_q, HookSword=build_hooksword_q, Dao=build_dao_q)


def build_quality(kinds=None, spacing=2.4, y=0.0, blades=True):
    out = {}
    for i, k in enumerate(kinds or QBUILD):
        root, nums = QBUILD[k](x=i * spacing, y=y)
        if blades:
            quality_blade(root, BLADE_KEY[k], QUALITY[k]["blade_offset"], k + "PreviewBlade")
        out[k] = (root, nums)
    return out

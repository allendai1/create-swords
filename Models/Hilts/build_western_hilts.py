# Western sword hilts (longsword, falchion, gladius) for Create Swords!, built from code in Blender.
# Runs after the katana's helpers, in one namespace:
#   ns = {"__name__": "lib"}
#   for f in ("Models/Stations/build_stations.py", "Models/Hilts/build_hilt.py", "Models/Hilts/build_western_hilts.py"):
#       exec(open(f).read(), ns)
#   ns["build_western_hilts"]()
# Same frame as build_game_hilt: studs, root empty at the grip centre, the grip runs up +Z toward the pommel,
# the guard and blade are toward -Z (game blade direction +X = Blender -Z). Edges along X, flats face +-Y.
# Each hilt is three meshes named by the game's colour roles: <Prefix>Grip / Guard / Pommel, renamed to
# exactly Grip / Guard / Pommel while exporting (export_western).
import math
import bmesh
from mathutils import Vector

PAL.setdefault("neutral", (0.7, 0.7, 0.7))
PAL.setdefault("leather", (0.36, 0.20, 0.11))

# Game numbers per hilt: grip length, blade-side face of the guard (BladeOffset), blade width for previews.
WESTERN = dict(
    Longsword=dict(grip=1.15, blade_offset=0.70, blade_w=0.25, blade_w_tip=0.2, blade_t=0.04),
    Falchion=dict(grip=0.72, blade_offset=0.44, blade_w=0.2, blade_w_tip=0.28, blade_t=0.035),
    Gladius=dict(grip=0.56, blade_offset=0.42, blade_w=0.275, blade_w_tip=0.25, blade_t=0.045),
)


def oval(a, b, n=2.0, seg=24, phase=0.0):
    """Points around a superellipse (n = 2 ellipse, larger = squarer), counter-clockwise."""
    pts = []
    for i in range(seg):
        t = 2 * math.pi * i / seg + phase
        c, s = math.cos(t), math.sin(t)
        pts.append((a * math.copysign(abs(c) ** (2 / n), c), b * math.copysign(abs(s) ** (2 / n), s)))
    return pts


def zring(pts, z, cx=0.0):
    """A section in the XY plane at height z (grip axis)."""
    return [Vector((x + cx, y, z)) for x, y in pts]


def yring(r, y, zc, seg=28):
    """A circle in the XZ plane (around the Y axis, the disc pommels) at depth y."""
    if r == 0:
        return [Vector((0, y, zc))]
    return [Vector((r * math.cos(2 * math.pi * i / seg), y, zc + r * math.sin(2 * math.pi * i / seg)))
            for i in range(seg)]


def xring(pts, x, zc):
    """A section in the YZ plane at x (crossguard arms): pts are (z, y) offsets."""
    if not pts:
        return [Vector((x, 0, zc))]
    return [Vector((x, y, zc + z)) for z, y in pts]


def loft(name, rings, color="neutral"):
    """Closed solid through rings of points (equal length); a one-point ring is a pole, and open
    end rings get a fan cap. Normals recalculated outward."""
    bm = bmesh.new()
    loops = [[bm.verts.new(p) for p in r] for r in rings]
    for A, B in zip(loops, loops[1:]):
        if len(A) == 1:
            for k in range(len(B)):
                bm.faces.new((A[0], B[k], B[(k + 1) % len(B)]))
        elif len(B) == 1:
            for k in range(len(A)):
                bm.faces.new((A[k], A[(k + 1) % len(A)], B[0]))
        else:
            for k in range(len(A)):
                m = (k + 1) % len(A)
                bm.faces.new((A[k], A[m], B[m], B[k]))
    for ring in (loops[0], loops[-1]):
        if len(ring) > 1:
            c = bm.verts.new(sum((v.co for v in ring), Vector()) / len(ring))
            for k in range(len(ring)):
                bm.faces.new((ring[k], ring[(k + 1) % len(ring)], c))
    _outward(bm)
    return mesh_obj(name, bm, color)


def table(pts):
    """Piecewise-linear function through (t, value) points, t ascending."""
    def f(t):
        for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
            if t <= t1:
                return v0 + (v1 - v0) * max(0.0, t - t0) / (t1 - t0)
        return pts[-1][1]
    return f


def join(name, objs):
    with bpy.context.temp_override(active_object=objs[0], selected_editable_objects=objs, selected_objects=objs):
        bpy.ops.object.join()
    objs[0].name = objs[0].data.name = name
    return objs[0]


def grip(name, half, z0, z1, a, b, n, seg, scale, phase=0.0, stations=24):
    """Grip along Z from z0 to z1; scale(z) multiplies the a x b section."""
    rings = []
    for i in range(stations + 1):
        z = z0 + (z1 - z0) * i / stations
        s = scale(z)
        rings.append(zring(oval(a * s, b * s, n, seg, phase), z))
    return loft(name, rings)


def riser_scale(base, risers, h=0.1, w=0.022):
    """base(z) plus raised bands (risers) at the given z: flat-topped bumps of relative height h."""
    def f(z):
        bump = 0.0
        for zr in risers:
            d = abs(z - zr)
            if d < w:
                bump = max(bump, h * min(1.0, (w - d) / (w * 0.4)))
        return base(z) * (1 + bump)
    return f


def grip_stations(z0, z1, extra, step=0.06):
    """Even samples plus the riser/ridge points (so bumps are always hit)."""
    zs = {round(z0 + (z1 - z0) * i / max(1, round((z1 - z0) / step)), 5)
          for i in range(round((z1 - z0) / step) + 1)}
    zs |= {round(z, 5) for z in extra if z0 < z < z1}
    return sorted(zs)


def arm_bar(name, span, zc, size, curve=lambda t: 0.0, n=4.0, seg=16):
    """Crossguard bar along X from -span/2 to +span/2 through (0, zc). size(t) is the half section at
    t = |x| / (span/2) (0 at the end = pole); curve(t) drops the centre line toward the blade (-Z)."""
    ts = [1.0, 0.995, 0.975, 0.94, 0.88, 0.75, 0.45, 0.15]
    rings = []
    for sgn in (-1, 1):
        for t in (ts if sgn < 0 else ts[::-1]):
            h = size(t)
            pts = oval(h, h, n, seg) if h > 0 else []
            rings.append(xring(pts, sgn * t * span / 2, zc - curve(t)))
        if sgn < 0:
            rings.append(xring(oval(size(0.0), size(0.0), n, seg), 0.0, zc))
    return loft(name, rings)


def block(name, z0, z1, a0, b0, a1, b1, chamfer=0.008, n=6.0, seg=24):
    """Rounded block along Z: section a0 x b0 (half sizes) at z0 to a1 x b1 at z1, chamfered ends."""
    lerp = lambda u, p, q: p + (q - p) * u
    rings = []
    for z, ch in ((z0, chamfer), (z0 + chamfer, 0), (z1 - chamfer, 0), (z1, chamfer)):
        u = (z - z0) / (z1 - z0)
        rings.append(zring(oval(lerp(u, a0, a1) - ch, lerp(u, b0, b1) - ch, n, seg), z))
    return loft(name, rings)


def disc(name, zc, profile, seg=28):
    """Revolve a (r, y) profile around the Y axis through (0, 0, zc): a disc whose faces look along Y."""
    return loft(name, [yring(r, y, zc, seg) for r, y in profile])


def knob(name, z0, r, h, seg=12):
    """Small domed button on the end, along +Z from z0."""
    prof = [(r, z0), (r, z0 + h * 0.5), (r * 0.8, z0 + h * 0.85), (r * 0.4, z0 + h), (0, z0 + h)]
    return loft(name, [zring(oval(rr, rr, 2, seg), z) if rr else [Vector((0, 0, z))] for rr, z in prof])


# ---------------------------------------------------------------- the three hilts
# Each builder returns (root, numbers) with numbers = GripLength / BladeOffset / Back as built.

def build_longsword_hilt(x=0, y=0, name="LongswordHiltGame", p="L_"):
    W = WESTERN["Longsword"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    # grip: swelling oval, three leather risers, ends tucked 0.015 into the guard and the pommel collar
    risers = (-0.29, 0.0, 0.29)
    base = lambda z: 0.86 + 0.14 * (1 - (z / (L / 2)) ** 2)
    sc = riser_scale(base, risers, h=0.09)
    rings = [zring(oval(0.085 * sc(z), 0.065 * sc(z), 2.3, 20), z)
             for z in grip_stations(g0 - 0.015, g1 + 0.015,
                                    [r + d for r in risers for d in (-0.022, -0.0132, 0.0132, 0.022)])]
    loft(p + "Grip", rings)
    # guard: shield-shaped centre block (ecusson) widening to the blade, square arms tapering then flaring
    ecu = block("_ecu", -bo, g0, 0.14, 0.065, 0.09, 0.065)
    size = table([(0, 0.035), (0.2, 0.035), (0.75, 0.027), (0.94, 0.038), (0.975, 0.032), (0.995, 0.018), (1, 0)])
    arms = arm_bar("_arms", 1.15, -bo + 0.04, size)   # bottom 0.005 above the blade-side face
    join(p + "Guard", [ecu, arms])
    # pommel: collar over the grip end, wheel with a raised boss on both faces, peen button on the end
    R, zc = 0.13, g1 + 0.025 + 0.13 - 0.03
    collar = block("_collar", g1, g1 + 0.05, 0.088, 0.068, 0.078, 0.06, chamfer=0.006)
    wheel = disc("_wheel", zc, [(0, -0.066), (0.05, -0.066), (0.06, -0.06), (0.064, -0.045), (0.112, -0.045),
                                (0.124, -0.04), (R, -0.028), (R, 0.028), (0.124, 0.04), (0.112, 0.045),
                                (0.064, 0.045), (0.06, 0.06), (0.05, 0.066), (0, 0.066)])
    peen = knob("_peen", zc + R - 0.008, 0.026, 0.032)
    join(p + "Pommel", [collar, wheel, peen])
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(zc + R - 0.008 + 0.032, 4))


def build_falchion_hilt(x=0, y=0, name="FalchionHiltGame", p="F_"):
    W = WESTERN["Falchion"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    base = lambda z: 0.9 + 0.1 * (1 - (z / (L / 2)) ** 2)
    loft(p + "Grip", [zring(oval(0.075 * base(z), 0.06 * base(z), 2.2, 20), z)
                      for z in grip_stations(g0 - 0.015, g1 + 0.015, [], step=0.09)])
    # guard: small block, arms curving toward the blade at the tips and ending in knobs
    blk = block("_block", -bo, g0, 0.12, 0.062, 0.085, 0.062)
    size = table([(0, 0.03), (0.86, 0.025), (0.94, 0.034), (0.975, 0.028), (0.995, 0.016), (1, 0)])
    curve = lambda t: 0.1 * max(0.0, (t - 0.3) / 0.7) ** 2
    arms = arm_bar("_arms", 0.85, -bo + 0.04, size, curve, n=3.0)
    join(p + "Guard", [blk, arms])
    # pommel: lens disc over a short collar
    R, zc = 0.1, g1 + 0.04 + 0.1 - 0.035
    collar = block("_collar", g1, g1 + 0.04, 0.082, 0.066, 0.076, 0.062, chamfer=0.006)
    lens = disc("_lens", zc, [(0, -0.04), (0.03, -0.038), (0.06, -0.031), (0.085, -0.02), (R, -0.008),
                              (R, 0.008), (0.085, 0.02), (0.06, 0.031), (0.03, 0.038), (0, 0.04)])
    join(p + "Pommel", [collar, lens])
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(zc + R, 4))


def build_gladius_hilt(x=0, y=0, name="GladiusHiltGame", p="G_"):
    W = WESTERN["Gladius"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    # grip: octagonal bone grip, four finger ridges (troughs at both ends)
    ridge = lambda z: 0.8 + 0.2 * (0.5 + 0.5 * math.cos(2 * math.pi * (z - g0) / (L / 4) - math.pi))
    zs = [g0 - 0.015] + [g0 + L * i / 24 for i in range(25)] + [g1 + 0.015]
    loft(p + "Grip", [zring(oval(0.075 * ridge(z), 0.065 * ridge(z), 2.0, 8, math.pi / 8), z) for z in zs])
    # guard: thin blade plate under a cushion-shaped oval hand guard
    plate = block("_plate", -bo, -bo + 0.016, 0.18, 0.11, 0.18, 0.11, chamfer=0.004, n=3.0, seg=32)
    z0, z1 = -bo + 0.01, g0     # body overlaps the plate by 0.006, top at the grip end
    prof = [(0.78, z0), (0.95, z0 + 0.012), (1.0, z0 + 0.04), (1.0, z0 + 0.07), (0.95, z1 - 0.025),
            (0.82, z1 - 0.008), (0.62, z1)]
    body = loft("_body", [zring(oval(0.19 * r, 0.12 * r, 2.0, 32), z) for r, z in prof])
    join(p + "Guard", [plate, body])
    # pommel: big ovoid (0.28 across the edges, 0.22 along the grip and across the flats) and a button nut
    zc, hz = g1 + 0.11 - 0.01, 0.11
    rings = [[Vector((0, 0, zc - hz))]]
    for i in range(1, 12):
        a = math.pi * i / 12
        rings.append(zring(oval(0.14 * math.sin(a), 0.11 * math.sin(a), 2.0, 24), zc - hz * math.cos(a)))
    rings.append([Vector((0, 0, zc + hz))])
    egg = loft("_egg", rings)
    nut = knob("_nut", zc + hz - 0.012, 0.032, 0.045, seg=12)
    join(p + "Pommel", [egg, nut])
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(zc + hz - 0.012 + 0.045, 4))


BUILDERS = dict(Longsword=build_longsword_hilt, Falchion=build_falchion_hilt, Gladius=build_gladius_hilt)


def build_western_hilts(spacing=1.6):
    """All three, side by side along X. Returns {kind: (root, numbers)}."""
    return {k: f(x=i * spacing) for i, (k, f) in enumerate(BUILDERS.items())}


def export_western(folder, kinds=BUILDERS):
    """One FBX per hilt with the same `roblox` preset as KatanaHiltGame.fbx (export_fbx in build_stations),
    root moved to the origin, parts renamed exactly Grip / Guard / Pommel for the file."""
    import os
    exp = _skill("export_asset", "blender-export-pipelines")
    out = {}
    for k in kinds:
        name = k + "HiltGame"
        parts = [o for o in bpy.data.collections[name].objects if o.type == "MESH"]
        old = [(o, o.name) for o in parts]
        for o in parts:
            o.name = o.data.name = o.name.split("_", 1)[1]
        try:
            out[k] = exp.run(preset="roblox", collection=name, out=os.path.join(folder, name + ".fbx"),
                             batch=True, no_anim=True)
        finally:
            for o, n in old:
                o.name = o.data.name = n
    bpy.ops.object.select_all(action="DESELECT")
    return out


# ---------------------------------------------------------------- review props (not exported)

def preview_blade(root, offset, w0, w1, t, length=1.2, single_edge=False, name="PreviewBlade"):
    """A straight blade stub from the blade root (buried 0.01 in the guard) down -Z, width w0 -> w1,
    diamond section (or a wedge, edge toward -X, for single-edged blades). Lives in `PreviewBlades`."""
    c = bpy.data.collections.get("PreviewBlades") or bpy.data.collections.new("PreviewBlades")
    if c.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(c)
    bm = bmesh.new()
    rings = []
    for i in range(2):
        z = -offset + 0.01 - length * i
        w = w0 + (w1 - w0) * i
        if single_edge:
            sec = ((-w / 2, 0), (w / 2 - t, -t / 2), (w / 2, -t * 0.3), (w / 2, t * 0.3), (w / 2 - t, t / 2))
        else:
            sec = ((-w / 2, 0), (0, -t / 2), (w / 2, 0), (0, t / 2))
        rings.append([bm.verts.new((sx, sy, z)) for sx, sy in sec])
    n = len(rings[0])
    for k in range(n):
        m = (k + 1) % n
        bm.faces.new((rings[0][k], rings[0][m], rings[1][m], rings[1][k]))
    bm.faces.new(rings[0][::-1])
    bm.faces.new(rings[1])
    _outward(bm)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(mat("steel"))
    o = bpy.data.objects.new(name, me)
    c.objects.link(o)
    o.parent = root
    return o

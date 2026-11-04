# Six more hilts (rapier, jian, dao, hook sword, claymore, machete) for Create Swords!, built from code in Blender.
# Runs after the western hilts' helpers, in one namespace:
#   ns = {"__name__": "lib"}
#   for f in ("Models/Stations/build_stations.py", "Models/Hilts/build_hilt.py",
#             "Models/Hilts/build_western_hilts.py", "Models/Hilts/build_more_hilts.py"):
#       exec(open(f).read(), ns)
#   ns["build_more_hilts"](); ns["export_western"](folder, kinds=ns["MORE"])
# Same frame as build_western_hilts: studs, root empty at the grip centre, the grip runs up +Z toward the pommel,
# the guard and blade are toward -Z. Edges along X (single edges toward -X), flats face +-Y.
# Each hilt is three meshes <Prefix>Grip / Guard / Pommel, renamed to exactly Grip / Guard / Pommel on export.
import math
import bmesh
from mathutils import Vector

# Game numbers per hilt: grip length, blade-side face of the guard (BladeOffset), preview blade.
MORE = dict(
    Rapier=dict(grip=0.85, blade_offset=0.6, blade_w=0.12, blade_w_tip=0.08, blade_t=0.04, single=False),
    Jian=dict(grip=0.8, blade_offset=0.5, blade_w=0.18, blade_w_tip=0.15, blade_t=0.035, single=False),
    Dao=dict(grip=1.2, blade_offset=0.66, blade_w=0.24, blade_w_tip=0.3, blade_t=0.04, single=True),
    HookSword=dict(grip=0.7, blade_offset=0.45, blade_w=0.15, blade_w_tip=0.15, blade_t=0.035, single=True),
    Claymore=dict(grip=1.5, blade_offset=0.95, blade_w=0.28, blade_w_tip=0.24, blade_t=0.04, single=False),
    Machete=dict(grip=0.65, blade_offset=0.38, blade_w=0.2, blade_w_tip=0.26, blade_t=0.025, single=True),
    # second batch (2026-10-29): swords known for their hilts
    Cutlass=dict(grip=0.62, blade_offset=0.45, blade_w=0.19, blade_w_tip=0.2, blade_t=0.035, single=True),
    Scimitar=dict(grip=0.65, blade_offset=0.4, blade_w=0.155, blade_w_tip=0.15, blade_t=0.04, single=True),
    Khopesh=dict(grip=0.55, blade_offset=0.3, blade_w=0.09, blade_w_tip=0.09, blade_t=0.05, single=True),
    Flamberge=dict(grip=1.45, blade_offset=0.75, blade_w=0.2, blade_w_tip=0.18, blade_t=0.045, single=False),
)
Y = Vector((0, 1, 0))


# ---------------------------------------------------------------- helpers on top of the western ones

def stack(name, secs, seg=20, n=2.0):
    """Loft through z-sections (z, a, b[, cx, cy]): an a x b superellipse centred at (cx, cy); a == 0 is a pole."""
    rings = []
    for s in secs:
        z, a, b, cx, cy = (tuple(s) + (0.0, 0.0))[:5]
        rings.append([Vector((cx, cy, z))] if a == 0 else [Vector((x + cx, y + cy, z)) for x, y in oval(a, b, n, seg)])
    return loft(name, rings)


def ball(name, c, rx, ry, rz, seg=16, lat=8):
    """Ellipsoid around point c (poles along Z)."""
    secs = [(c[2] - rz, 0, 0, c[0], c[1])]
    for i in range(1, lat):
        t = math.pi * i / lat
        secs.append((c[2] - rz * math.cos(t), rx * math.sin(t), ry * math.sin(t), c[0], c[1]))
    return stack(name, secs + [(c[2] + rz, 0, 0, c[0], c[1])], seg)


def spline(pts, per=6):
    """Catmull-Rom curve through (x, y, z) points, `per` samples per span."""
    P = [Vector(p) for p in pts]
    P = [2 * P[0] - P[1]] + P + [2 * P[-1] - P[-2]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1:i + 3]
        for k in range(per):
            t = k / per
            out.append(0.5 * (2 * p1 + (p2 - p0) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                              + (3 * p1 - p0 - 3 * p2 + p3) * t ** 3))
    return out + [P[-2].copy()]


def _frames(path, radius, up, seg, ry, closed):
    """Section rings along a path that lies in the plane with normal `up`: radius(u) in the plane,
    radius(u) * ry across it (u = 0..1 along the path)."""
    N = len(path)
    rings = []
    for i, p in enumerate(path):
        if closed:
            a, b = path[i - 1], path[(i + 1) % N]
        else:
            a, b = path[max(i - 1, 0)], path[min(i + 1, N - 1)]
        T = (b - a).normalized()
        nn = up.cross(T).normalized()
        bb = T.cross(nn)
        r = radius(i / (N - 1 if not closed else N))
        if r <= 1e-6:
            rings.append([p.copy()])      # pole: a pointed end
            continue
        rings.append([p + nn * r * math.cos(2 * math.pi * k / seg) + bb * r * ry * math.sin(2 * math.pi * k / seg)
                      for k in range(seg)])
    return rings


def tube(name, path, radius, up=Y, seg=12, ry=1.0):
    """Open tube along a planar path (ends flat-capped; bury them in other parts)."""
    return loft(name, _frames(path, radius if callable(radius) else (lambda u: radius), up, seg, ry, False))


def loop(name, path, r, up=Y, seg=10, ry=1.0):
    """Closed tube (a ring) along a closed planar path."""
    bm = bmesh.new()
    loops = [[bm.verts.new(p) for p in ring] for ring in _frames(path, lambda u: r, up, seg, ry, True)]
    for A, B in zip(loops, loops[1:] + loops[:1]):
        for k in range(seg):
            m = (k + 1) % seg
            bm.faces.new((A[k], A[m], B[m], B[k]))
    _outward(bm)
    return mesh_obj(name, bm, "neutral")


def circle(c, u, v, ru, rv, n, a0=0.0, a1=2 * math.pi, closed=True):
    """Points c + u*ru*cos + v*rv*sin; the full circle (closed) or the arc a0..a1 with both ends."""
    c, u, v = Vector(c), Vector(u), Vector(v)
    k = n if closed else n + 1
    return [c + u * ru * math.cos(a0 + (a1 - a0) * i / n) + v * rv * math.sin(a0 + (a1 - a0) * i / n) for i in range(k)]


def wrap_grip(name, g0, g1, a, b, base, pitch, amp, tilt=0.0, seg=16, n=2.0, band=0.0, band_s=1.12, tuck=0.015):
    """Grip along Z: a x b section times base(z), wrapped in close ridges (one every `pitch`, `amp` relative
    height) whose rings lean by `tilt` across the width so they read as a spiral wrap; plain bands of length
    `band` at both ends (band_s times the section). The ends are tucked `tuck` into the guard and pommel."""
    za, zb = (g0 + band, g1 - band) if band else (g0 - tuck, g1 + tuck)
    k = max(2, 2 * round((zb - za) / pitch))
    rings = []

    def ring(z, s, t=0.0):
        r = zring(oval(a * s * base(z), b * s * base(z), n, seg), z)
        for v in r:
            v.z += t * v.x / a
        return r

    if band:
        rings += [ring(g0 - tuck, band_s), ring(za - 0.007, band_s)]
    for i in range(k + 1):
        z = za + (zb - za) * i / k
        fade = min(1.0, i / 2, (k - i) / 2)
        rings.append(ring(z, 1 + amp * (i % 2), tilt * fade))
    if band:
        rings += [ring(zb + 0.007, band_s), ring(g1 + tuck, band_s)]
    return loft(name, rings)


def wing_bar(name, span, zc, zh, yh, drop, n=4.0, seg=16):
    """Crossguard along X with separate half sizes: zh(t) along the grip, yh(t) across the flats, the wings
    dropping drop(t) toward the blade; t = |x| / (span/2), zh(1) = 0 is the tip pole."""
    ts = [1.0, 0.99, 0.96, 0.92, 0.85, 0.72, 0.55, 0.35, 0.15]
    rings = []
    for sgn in (-1, 1):
        for t in (ts if sgn < 0 else ts[::-1]):
            h = zh(t)
            rings.append(xring(oval(h, yh(t), n, seg) if h > 0 else [], sgn * t * span / 2, zc - drop(t)))
        if sgn < 0:
            rings.append(xring(oval(zh(0), yh(0), n, seg), 0.0, zc))
    return loft(name, rings)


def shift(o, dx=0.0, dz=0.0):
    for v in o.data.vertices:
        v.co.x += dx
        v.co.z += dz
    return o


# ---------------------------------------------------------------- the six hilts
# Each builder returns (root, numbers) with numbers = GripLength / BladeOffset / Back as built.

def build_rapier_hilt(x=0, y=0, name="RapierHiltGame", p="R_"):
    W = MORE["Rapier"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    # grip: slim oval wound with wire (close slanted ridges) between two turk's-head bands
    base = lambda z: 0.9 + 0.1 * (1 - (2 * z / L) ** 2)
    wrap_grip(p + "Grip", g0, g1, 0.058, 0.048, base, pitch=0.042, amp=0.07, tilt=0.016, seg=14, band=0.04)
    # guard: quillon block, round quillons with knob ends, a ricasso sleeve down to the blade root,
    # two pas d'ane loops beside the sleeve, a side ring on +Y and the knuckle bow on the -X side
    zq = -0.465
    blk = block("_block", -0.505, g0 + 0.005, 0.075, 0.062, 0.07, 0.06, chamfer=0.006)
    size = table([(0, 0.022), (0.84, 0.019), (0.89, 0.028), (0.95, 0.033), (0.985, 0.022), (1, 0)])
    quill = arm_bar("_quill", 1.1, zq, size, n=2.0, seg=10)
    sleeve = block("_sleeve", -bo, -0.495, 0.068, 0.027, 0.062, 0.027, chamfer=0.005)
    pas = [tube("_pas%d" % s, circle((s * 0.035, 0, -0.53), (s, 0, 0), (0, 0, 1), 0.095, 0.056, 10,
                                     math.pi / 2, -math.pi / 2, closed=False), 0.013, seg=8)
           for s in (-1, 1)]
    tilt = math.radians(25)
    ey = Vector((0, math.cos(tilt), -math.sin(tilt)))
    side = loop("_side", circle(Vector((0, 0.035, zq)) + ey * 0.14, (1, 0, 0), ey, 0.1, 0.14, 22),
                0.013, up=Vector((1, 0, 0)).cross(ey), seg=8)
    bow = tube("_bow", spline([(-0.05, 0, -0.475), (-0.15, 0, -0.43), (-0.21, 0, -0.26), (-0.225, 0, 0.02),
                               (-0.19, 0, 0.29), (-0.09, 0, 0.44), (-0.01, 0, 0.5)], per=4),
               lambda u: 0.02 - 0.005 * u, seg=8)
    join(p + "Guard", [blk, quill, sleeve, side, bow] + pas)
    # pommel: collar, pear-shaped pommel and a button
    collar = block("_collar", g1, g1 + 0.04, 0.074, 0.062, 0.062, 0.052, chamfer=0.006)
    z0, H = g1 + 0.03, 0.24
    prof = table([(0, 0.045), (0.15, 0.055), (0.4, 0.088), (0.62, 0.1), (0.82, 0.088), (0.95, 0.05), (1, 0.02)])
    pear = stack("_pear", [(z0 + H * s, prof(s), prof(s) * 0.92) for s in
                           (0, 0.08, 0.17, 0.27, 0.38, 0.5, 0.62, 0.73, 0.83, 0.91, 0.96, 1.0)], seg=16)
    btn = knob("_btn", z0 + H - 0.005, 0.024, 0.03, seg=12)
    join(p + "Pommel", [collar, pear, btn])
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(z0 + H - 0.005 + 0.03, 4))


def build_jian_hilt(x=0, y=0, name="JianHiltGame", p="J_"):
    W = MORE["Jian"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    # grip: oval with a slight waist, cord wrap
    base = lambda z: 1.0 - 0.08 * (1 - (2 * z / L) ** 2)
    wrap_grip(p + "Grip", g0, g1, 0.072, 0.056, base, pitch=0.06, amp=0.06, tilt=0.022, seg=16, n=2.2, tuck=0.04)
    # guard: compact crossguard, thick in the middle, the wings bending toward the blade with flared ends
    zc = -bo + 0.05
    zh = table([(0, 0.05), (0.35, 0.036), (0.72, 0.028), (0.85, 0.034), (0.92, 0.042), (0.96, 0.038),
                (0.99, 0.022), (1, 0)])
    yh = table([(0, 0.068), (0.35, 0.05), (0.72, 0.03), (0.92, 0.03), (1, 0.02)])
    drop = lambda t: 0.09 * t ** 1.6
    guard = wing_bar(p + "Guard", 0.5, zc, zh, yh, drop, n=3.5, seg=16)
    # pommel: flat mushroom, wider than the grip across X, thin across Y, flat top
    z0 = g1 - 0.005
    stack(p + "Pommel", [(z0, 0.078, 0.06), (z0 + 0.02, 0.08, 0.06), (z0 + 0.05, 0.095, 0.058),
                         (z0 + 0.085, 0.122, 0.054), (z0 + 0.1, 0.13, 0.052), (z0 + 0.115, 0.128, 0.048),
                         (z0 + 0.125, 0.118, 0.042), (z0 + 0.13, 0.105, 0.036)], seg=24, n=3.0)
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(z0 + 0.13, 4))


def build_dao_hilt(x=0, y=0, name="DaoHiltGame", p="D_"):
    W = MORE["Dao"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    # grip: long plain oval for two hands, bending slightly toward the edge (-X) at the butt
    cx = lambda z: -0.035 * ((z - g0) / L) ** 2
    base = lambda z: 0.93 + 0.07 * (1 - (2 * z / L) ** 2)
    stack(p + "Grip", [(z, 0.075 * base(z), 0.06 * base(z), cx(z))
                       for z in grip_stations(g0 - 0.015, g1 + 0.015, [], step=0.08)], seg=20, n=2.2)
    # guard: plain round disc, flat faces toward blade and grip, ferrule over the grip end
    disc_ = stack("_disc", [(-bo, 0.158, 0.158), (-bo + 0.007, 0.17, 0.17), (-bo + 0.033, 0.17, 0.17),
                            (-bo + 0.04, 0.158, 0.158)], seg=36)
    ferrule = block("_ferrule", -bo + 0.035, g0 + 0.03, 0.09, 0.073, 0.084, 0.069, chamfer=0.006)
    join(p + "Guard", [disc_, ferrule])
    # pommel: collar, then a ring whose hole looks along Y
    c1 = cx(g1)
    collar = shift(block("_collar", g1 - 0.005, g1 + 0.05, 0.08, 0.066, 0.07, 0.058, chamfer=0.006), dx=c1)
    R, rr = 0.115, 0.026
    zc = g1 + 0.05 + R + rr - 0.022
    ring = loop("_ring", circle((c1, 0, zc), (1, 0, 0), (0, 0, 1), R, R, 32), rr, seg=10, ry=1.25)
    join(p + "Pommel", [collar, ring])
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(zc + R + rr, 4))


def build_hooksword_hilt(x=0, y=0, name="HookSwordHiltGame", p="H_"):
    W = MORE["HookSword"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    base = lambda z: 0.94 + 0.06 * (1 - (2 * z / L) ** 2)
    wrap_grip(p + "Grip", g0, g1, 0.066, 0.054, base, pitch=0.05, amp=0.06, tilt=0.02, seg=14)
    # guard: ferrule at the blade end, a crescent plate (faces along Y) bowed out to -X with its horns
    # pointing +-Z and a sharpened convex rim, held off the grip by two bars
    ferrule = block("_ferrule", -bo, g0 + 0.03, 0.085, 0.066, 0.076, 0.06, chamfer=0.006)
    h, xt, xo, xi, t = 0.55, -0.13, -0.5, -0.38, 0.034
    xo_ = lambda z: xt + (xo - xt) * (1 - (z / h) ** 2)
    xi_ = lambda z: xt + (xi - xt) * (1 - (z / h) ** 2)
    rings = [[Vector((xt, 0, h))]]
    N = 28
    for k in range(1, N):
        z = h * math.cos(math.pi * k / N)
        o, i = xo_(z), xi_(z)
        w = i - o
        e, ch = min(0.035, w * 0.45), min(0.006, w * 0.2)
        th = t / 2 * min(1.0, 0.35 + w / 0.06)
        rings.append([Vector(v) for v in ((i, -th * 0.6, z), (i - ch, -th, z), (o + e, -th, z), (o, 0, z),
                                          (o + e, th, z), (i - ch, th, z), (i, th * 0.6, z))])
    rings.append([Vector((xt, 0, -h))])
    crescent = loft("_crescent", rings)
    bars = [tube("_bar%d" % j, [Vector((-0.04, 0, z)), Vector((xi_(z) - 0.012, 0, z))], 0.022, seg=10)
            for j, z in enumerate((-0.4, 0.29))]
    join(p + "Guard", [ferrule, crescent] + bars)
    # pommel: collar and the long dagger spike (diamond section)
    collar = block("_collar", g1 - 0.005, g1 + 0.045, 0.078, 0.064, 0.064, 0.052, chamfer=0.006)
    z0, S = g1 + 0.035, 0.95
    taper = table([(0, 1.0), (0.08, 1.06), (0.3, 0.86), (0.7, 0.45), (0.92, 0.14), (1, 0)])
    spike = stack("_spike", [(z0 + S * u, 0.05 * taper(u), 0.03 * taper(u))
                             for u in (0, 0.04, 0.08, 0.18, 0.3, 0.45, 0.6, 0.7, 0.8, 0.88, 0.94, 1.0)], seg=4)
    join(p + "Pommel", [collar, spike])
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(z0 + S, 4))


def build_claymore_hilt(x=0, y=0, name="ClaymoreHiltGame", p="C_"):
    W = MORE["Claymore"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    # grip: long two-hand leather grip with four risers
    risers = (-0.45, -0.15, 0.15, 0.45)
    base = lambda z: 0.88 + 0.12 * (1 - (2 * z / L) ** 2)
    sc = riser_scale(base, risers, h=0.09)
    loft(p + "Grip", [zring(oval(0.09 * sc(z), 0.07 * sc(z), 2.3, 16), z)
                      for z in grip_stations(g0 - 0.015, g1 + 0.015,
                                             [r + d for r in risers for d in (-0.022, -0.0132, 0.0132, 0.022)],
                                             step=0.1)])
    # guard: centre block wider at the blade, langets down the flats, arms sloping toward the blade
    # and ending in quatrefoils (four rings round a boss, faces along Y)
    parts = [block("_ecu", -bo, g0 + 0.01, 0.16, 0.07, 0.09, 0.07)]
    for s in (-1, 1):
        lw = table([(0, 0.05), (0.6, 0.04), (0.85, 0.028), (0.97, 0.012), (1, 0)])
        parts.append(stack("_langet%d" % s, [(-bo + 0.05 - 0.24 * u, lw(u), 0.006 if u < 1 else 0, 0, s * 0.027)
                                             for u in (0, 0.25, 0.6, 0.85, 0.97, 1.0)], seg=12, n=4.0))
        path = spline([(s * 0.04, 0, -0.84), (s * 0.12, 0, -0.865), (s * 0.3, 0, -0.985), (s * 0.48, 0, -1.105),
                       (s * 0.62, 0, -1.195)], per=3)
        parts.append(tube("_arm%d" % s, path, lambda u: 0.045 - 0.014 * u, seg=10))
        d = (path[-1] - path[-2]).normalized()
        q = Y.cross(d)
        c = path[-1] + d * 0.045
        parts.append(ball("_boss%d" % s, c, 0.036, 0.026, 0.036, seg=12, lat=6))
        for j in range(4):
            phi = math.pi / 4 + j * math.pi / 2
            # neighbouring lobes overlap: stagger them 0.006 in Y so their flat faces never share a plane
            lc = c + (d * math.cos(phi) + q * math.sin(phi)) * 0.056 + Y * (0.003 if j % 2 else -0.003)
            parts.append(loop("_lobe%d%d" % (s, j), circle(lc, (1, 0, 0), (0, 0, 1), 0.041, 0.041, 10),
                              0.013, seg=6, ry=1.25))
    join(p + "Guard", parts)
    # pommel: collar, ball and peen button
    collar = block("_collar", g1 - 0.005, g1 + 0.055, 0.092, 0.072, 0.075, 0.06, chamfer=0.007)
    rz = 0.14
    zc = g1 + 0.05 + rz - 0.025
    b = ball("_ball", (0, 0, zc), 0.15, 0.135, rz, seg=18, lat=9)
    peen = knob("_peen", zc + rz - 0.008, 0.03, 0.035)
    join(p + "Pommel", [collar, b, peen])
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(zc + rz - 0.008 + 0.035, 4))


def build_machete_hilt(x=0, y=0, name="MacheteHiltGame", p="M_"):
    W = MORE["Machete"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    # grip: slab of two wooden scales (flat faces along Y), the butt swelling toward the edge (-X)
    xmin = table([(g0, -0.074), (0.0, -0.068), (g1 - 0.12, -0.072), (g1, -0.094)])
    xmax = table([(g0, 0.07), (0.0, 0.073), (g1, 0.068)])
    sec = lambda z, b=0.044: (z, (xmax(z) - xmin(z)) / 2, b, (xmax(z) + xmin(z)) / 2)
    zs = grip_stations(g0 - 0.015, g1 + 0.015, [g1 - 0.12, g1 - 0.06], step=0.05)
    stack(p + "Grip", [sec(z) for z in zs], seg=20, n=3.5)
    # guard: bolster at the blade end (finger swell on the edge side) and the tang showing between
    # the scales along both edges
    bol = shift(block("_bolster", -bo, g0 + 0.03, 0.112, 0.034, 0.09, 0.052, chamfer=0.006), dx=-0.008)
    tz = [g0 - 0.01] + [z for z in zs if g0 < z < g1] + [g1]
    tangs = [stack("_tang%d" % s, [(z, 0.008, 0.007, (xmax(z) if s > 0 else xmin(z)) - s * 0.004) for z in tz],
                   seg=8, n=4.0) for s in (-1, 1)]
    join(p + "Guard", [bol] + tangs)
    # pommel: hooked butt cap flaring toward the edge, plus brass rivets through the scales
    z0 = g1 - 0.02
    cap = stack("_cap", [(z0, 0.084, 0.05, -0.012), (z0 + 0.03, 0.096, 0.05, -0.026),
                         (z0 + 0.055, 0.114, 0.048, -0.05), (z0 + 0.075, 0.118, 0.045, -0.064),
                         (z0 + 0.09, 0.104, 0.04, -0.08), (z0 + 0.1, 0.078, 0.032, -0.094),
                         (z0 + 0.105, 0.05, 0.022, -0.106)], seg=20, n=3.0)
    rivets = []
    for zr in (-0.2, 0.0, 0.18):
        for s in (-1, 1):
            prof = [(0, 0.03), (0.016, 0.03), (0.016, 0.046), (0.012, 0.052), (0.006, 0.0548), (0, 0.0555)]
            rivets.append(disc("_rivet", zr, [(r, s * yy) for r, yy in prof], seg=10))
    join(p + "Pommel", [cap] + rivets)
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(z0 + 0.105, 4))


def build_cutlass_hilt(x=0, y=0, name="CutlassHiltGame", p="X_"):
    W = MORE["Cutlass"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    base = lambda z: 0.92 + 0.08 * (1 - (2 * z / L) ** 2)
    wrap_grip(p + "Grip", g0, g1, 0.064, 0.052, base, pitch=0.05, amp=0.06, tilt=0.02, seg=14, tuck=0.03)
    # guard: a cupped shell (open toward the hand, set toward the knuckle side -X), a ferrule from the
    # shell floor to the grip, and a flat D-shaped knuckle bow from the shell rim up to the pommel cap
    A, B, cx = 0.27, 0.21, -0.05
    prof = [(0, -bo), (0.35, -bo + 0.002), (0.6, -bo + 0.01), (0.78, -bo + 0.025), (0.9, -bo + 0.055),
            (0.97, -bo + 0.11), (1.0, -bo + 0.175), (0.995, -bo + 0.2),
            (0.958, -bo + 0.195), (0.932, -bo + 0.14), (0.87, -bo + 0.08), (0.76, -bo + 0.045),
            (0.58, -bo + 0.027), (0.33, -bo + 0.018), (0, -bo + 0.016)]
    shell = stack("_shell", [(z, A * s, B * s, cx) for s, z in prof], seg=28)
    ferrule = block("_ferrule", -bo + 0.01, g0 + 0.03, 0.075, 0.062, 0.07, 0.058, chamfer=0.006)
    bow = tube("_bow", spline([(-0.305, 0, -0.29), (-0.315, 0, -0.16), (-0.29, 0, 0.03), (-0.215, 0, 0.2),
                               (-0.1, 0, 0.3), (-0.02, 0, 0.335)], per=4), 0.015, seg=8, ry=1.8)
    join(p + "Guard", [shell, ferrule, bow])
    # pommel: a backstrap down the spine side (+X) of the grip and the cap over the end
    zs = grip_stations(g0 - 0.01, g1 + 0.01, [], step=0.1)
    strap = stack("_strap", [(z, 0.011, 0.022, 0.064 * base(z) - 0.002) for z in zs], seg=12, n=4.0)
    cap = stack("_cap", [(g1 - 0.01, 0.072, 0.059), (g1 + 0.02, 0.075, 0.06), (g1 + 0.045, 0.064, 0.052),
                         (g1 + 0.06, 0.04, 0.032), (g1 + 0.066, 0, 0)], seg=16)
    join(p + "Pommel", [strap, cap])
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(g1 + 0.066, 4))


def build_scimitar_hilt(x=0, y=0, name="ScimitarHiltGame", p="S_"):
    W = MORE["Scimitar"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    # grip: straight to zb, then the last 0.225 bends toward the edge (-X) on an arc (pistol grip)
    Rb, zb = 0.45, g1 - 0.225
    th = 0.225 / Rb                                  # 28.6 degrees
    arc = lambda a: Vector((-Rb + Rb * math.cos(a), 0, zb + Rb * math.sin(a)))
    path = [Vector((0, 0, z)) for z in (g0 - 0.02, g0 + 0.06, g0 + 0.16, g0 + 0.26, g0 + 0.36, zb)]
    path += [arc(th * i / 6) for i in range(1, 7)]
    rad = table([(0, 0.058), (0.4, 0.06), (0.75, 0.064), (1, 0.068)])
    tube(p + "Grip", path, rad, seg=16, ry=0.75)
    # guard: block, quillons whose ends turn down toward the blade, langets down the blade and up the grip
    blk = block("_block", -bo, g0 + 0.015, 0.088, 0.052, 0.07, 0.05, chamfer=0.006)
    size = table([(0, 0.03), (0.7, 0.024), (0.88, 0.03), (0.96, 0.033), (0.99, 0.02), (1, 0)])
    curve = lambda t: 0.11 * max(0.0, (t - 0.55) / 0.45) ** 2
    arms = arm_bar("_arms", 0.55, -bo + 0.035, size, curve, n=3.0, seg=12)
    parts = [blk, arms]
    lw = table([(0, 0.034), (0.7, 0.02), (1, 0)])
    for s in (-1, 1):
        parts.append(stack("_down%d" % s, [(-bo + 0.03 - 0.14 * u, lw(u), 0.006 if u < 1 else 0, 0, s * 0.027)
                                           for u in (0, 0.4, 0.7, 0.9, 1.0)], seg=10, n=4.0))
        parts.append(stack("_up%d" % s, [(g0 + 0.11 * u, lw(u) * 0.85, 0.006 if u < 1 else 0, 0, s * 0.047)
                                         for u in (0, 0.4, 0.7, 0.9, 1.0)], seg=10, n=4.0))
    join(p + "Guard", parts)
    # pommel: angled cap over the bent end, domed along the grip's end direction
    cap_path = [arc(th + a) for a in (-0.05, -0.02, 0.03, 0.08, 0.12, 0.15, 0.17)]
    capr = table([(0, 0.07), (0.15, 0.076), (0.4, 0.078), (0.65, 0.07), (0.85, 0.05), (1, 0)])
    cap = tube(p + "Pommel", cap_path, capr, seg=16, ry=0.78)
    top = max(v.co.z for v in cap.data.vertices)
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(top, 4))


def build_khopesh_hilt(x=0, y=0, name="KhopeshHiltGame", p="K_"):
    W = MORE["Khopesh"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    # grip: flattened oval widening toward the pommel, two shallow inlay bands
    bands = (-0.1, 0.12)
    sc = riser_scale(lambda z: 0.72 + 0.28 * (z - g0) / L, bands, h=0.06, w=0.02)
    loft(p + "Grip", [zring(oval(0.07 * sc(z), 0.046 * sc(z), 2.6, 18), z)
                      for z in grip_stations(g0 - 0.015, g1 + 0.015,
                                             [r + d for r in bands for d in (-0.02, -0.012, 0.012, 0.02)],
                                             step=0.07)])
    # guard: just a thin ferrule at the blade end
    block(p + "Guard", -bo, g0 + 0.025, 0.058, 0.04, 0.056, 0.04, chamfer=0.005)
    # pommel: flat fan whose top is a crescent (horns up), thin across Y; sections along X
    S = 0.12
    zlo = lambda u: g1 - 0.01 + 0.13 * max(0.0, (u - 0.55) / 0.45) ** 1.6
    zhi = lambda u: g1 + 0.085 + 0.06 * u ** 2.2
    ts = [1.0, 0.985, 0.95, 0.9, 0.8, 0.68, 0.55, 0.4, 0.2]
    rings = []
    for sgn in (-1, 1):
        for u in (ts if sgn < 0 else ts[::-1]):
            h, zm = (zhi(u) - zlo(u)) / 2, (zhi(u) + zlo(u)) / 2
            rings.append(xring(oval(h, 0.05 * (1 - 0.5 * u), 3.0, 14) if u < 1 else [], sgn * u * S, zm))
        if sgn < 0:
            rings.append(xring(oval((zhi(0) - zlo(0)) / 2, 0.05, 3.0, 14), 0.0, (zhi(0) + zlo(0)) / 2))
    loft(p + "Pommel", rings)
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(zhi(0.985), 4))


def build_flamberge_hilt(x=0, y=0, name="FlambergeHiltGame", p="B_"):
    W = MORE["Flamberge"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    risers = (-0.42, -0.14, 0.14, 0.42)
    sc = riser_scale(lambda z: 0.88 + 0.12 * (1 - (2 * z / L) ** 2), risers, h=0.09)
    loft(p + "Grip", [zring(oval(0.085 * sc(z), 0.068 * sc(z), 2.3, 16), z)
                      for z in grip_stations(g0 - 0.015, g1 + 0.015,
                                             [r + d for r in risers for d in (-0.022, -0.0132, 0.0132, 0.022)],
                                             step=0.1)])
    # guard: block, long straight cross, a side ring on each face hanging below the cross, and a ricasso
    # collar 0.35 below the guard with parrying lugs curving back toward the hand
    blk = block("_block", -bo, g0 + 0.01, 0.112, 0.055, 0.095, 0.055, chamfer=0.006)
    size = table([(0, 0.028), (0.2, 0.028), (0.75, 0.024), (0.94, 0.036), (0.975, 0.03), (0.995, 0.017), (1, 0)])
    arms = arm_bar("_arms", 1.6, -bo + 0.032, size, n=4.0, seg=12)
    parts = [blk, arms]
    X = Vector((1, 0, 0))
    zl = -bo - 0.35
    parts.append(block("_collar", zl - 0.022, zl + 0.022, 0.108, 0.031, 0.108, 0.031, chamfer=0.005))
    for s in (-1, 1):
        d = Vector((0, s * 0.26, -0.966)).normalized()
        c = Vector((0, s * 0.03, -bo + 0.015)) + d * 0.1
        parts.append(loop("_ring%d" % s, circle(c, X, d, 0.1, 0.1, 20), 0.014, up=X.cross(d), seg=8))
        lug = spline([(s * 0.09, 0, zl), (s * 0.18, 0, zl - 0.006), (s * 0.26, 0, zl + 0.03),
                      (s * 0.3, 0, zl + 0.1)], per=4)
        parts.append(tube("_lug%d" % s, lug, lambda u: 0.026 * (1 - u) ** 0.6, seg=10, ry=0.8))
    join(p + "Guard", parts)
    # pommel: collar and a faceted scent-stopper pommel with a button
    collar = block("_collar", g1 - 0.005, g1 + 0.05, 0.088, 0.07, 0.075, 0.062, chamfer=0.006)
    z0, H = g1 + 0.04, 0.25
    pr = table([(0, 0.05), (0.12, 0.06), (0.3, 0.09), (0.55, 0.118), (0.72, 0.122), (0.85, 0.105),
                (0.93, 0.07), (1.0, 0.045)])
    stopper = stack("_stopper", [(z0 + H * u, pr(u), pr(u) * 0.95)
                                 for u in (0, 0.12, 0.3, 0.45, 0.55, 0.65, 0.72, 0.8, 0.85, 0.93, 1.0)], seg=8)
    btn = knob("_btn", z0 + H - 0.005, 0.028, 0.03, seg=12)
    join(p + "Pommel", [collar, stopper, btn])
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(z0 + H - 0.005 + 0.03, 4))


MORE_BUILDERS = dict(Rapier=build_rapier_hilt, Jian=build_jian_hilt, Dao=build_dao_hilt,
                     HookSword=build_hooksword_hilt, Claymore=build_claymore_hilt, Machete=build_machete_hilt)
MORE_BUILDERS.update(Cutlass=build_cutlass_hilt, Scimitar=build_scimitar_hilt, Khopesh=build_khopesh_hilt,
                     Flamberge=build_flamberge_hilt)


def build_more_hilts(spacing=1.9, x0=0.0, kinds=None):
    """The given kinds (default all) side by side along X, each with a preview blade stub.
    Returns {kind: (root, numbers)}."""
    out = {}
    for i, k in enumerate(kinds or MORE_BUILDERS):
        root, nums = MORE_BUILDERS[k](x=x0 + i * spacing)
        W = MORE[k]
        preview_blade(root, W["blade_offset"], W["blade_w"], W["blade_w_tip"], W["blade_t"],
                      single_edge=W["single"], name=k + "PreviewBlade")
        out[k] = (root, nums)
    return out


# ---------------------------------------------------------------- review renders (not exported)

def review_colours(kinds):
    """Leather grips, steel guards, brass pommels, like the western review sheet."""
    PAL.setdefault("brass", (0.86, 0.72, 0.42))
    for k in kinds:
        for o in bpy.data.collections[k + "HiltGame"].objects:
            if o.type == "MESH":
                role = o.name.split("_", 1)[1]
                o.data.materials.clear()
                o.data.materials.append(mat({"Grip": "leather", "Guard": "steel", "Pommel": "brass"}[role]))


def review_render(path_sheet, path_34, roots, labels):
    """Flat view (top row) and edge view (bottom row, roots turned so -X faces the camera) stitched into
    one sheet, plus a 3/4 view. roots/labels in order along X."""
    import os
    import numpy as np
    sc = bpy.context.scene
    for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT", "BLENDER_WORKBENCH"):
        try:
            sc.render.engine = eng
            break
        except TypeError:
            pass
    sc.view_settings.view_transform = "Standard"
    w = sc.world or bpy.data.worlds.new("World")
    sc.world = w
    w.use_nodes = True
    bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs[0].default_value = srgb2lin((0.78, 0.77, 0.74)) + (1,)
    bg.inputs[1].default_value = 1.0
    sun = bpy.data.objects.get("ReviewSun") or bpy.data.objects.new("ReviewSun", bpy.data.lights.new("ReviewSun", "SUN"))
    if sun.name not in sc.collection.objects:
        sc.collection.objects.link(sun)
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(58), 0, math.radians(-25))
    xs = [r.location.x for r in roots]
    cx = (min(xs) + max(xs)) / 2
    width = max(xs) - min(xs) + 1.9
    top, bot = 1.45, -2.6
    texts = []
    tm = mat("iron")
    for r, lab in zip(roots, labels):
        cu = bpy.data.curves.new("Label_" + lab, "FONT")
        cu.body, cu.align_x, cu.size = lab, "CENTER", 0.2
        t = bpy.data.objects.new("Label_" + lab, cu)
        t.data.materials.append(tm)
        sc.collection.objects.link(t)
        t.location = (r.location.x, -1.5, bot + 0.12)
        t.rotation_euler = (math.radians(90), 0, 0)
        texts.append(t)
    cam = bpy.data.objects.get("ReviewCam") or bpy.data.objects.new("ReviewCam", bpy.data.cameras.new("ReviewCam"))
    if cam.name not in sc.collection.objects:
        sc.collection.objects.link(cam)
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = width
    cam.data.clip_end = 100
    sc.camera = cam
    px = 220
    sc.render.resolution_x, sc.render.resolution_y = round(width * px), round((top - bot) * px)
    sc.render.resolution_percentage = 100
    cam.location = (cx, -20, (top + bot) / 2)
    cam.rotation_euler = (math.radians(90), 0, 0)
    sc.render.film_transparent = False
    tmp = [path_sheet + ".flat.png", path_sheet + ".edge.png"]
    sc.render.filepath = tmp[0]
    bpy.ops.render.render(write_still=True)
    for r in roots:
        r.rotation_euler.z = math.radians(90)          # -X (edge side) toward the camera
    sc.render.filepath = tmp[1]
    bpy.ops.render.render(write_still=True)
    for r in roots:
        r.rotation_euler.z = 0
    imgs = [bpy.data.images.load(p) for p in tmp]
    W_, H_ = imgs[0].size
    arr = [np.array(i.pixels[:], dtype=np.float32).reshape(H_, W_, 4) for i in imgs]
    out = bpy.data.images.new("Sheet", W_, H_ * 2)
    out.pixels.foreach_set(np.concatenate([arr[1], arr[0]]).ravel())   # rows go bottom-up
    out.filepath_raw, out.file_format = path_sheet, "PNG"
    out.save()
    for i in imgs:
        bpy.data.images.remove(i)
    for p in tmp:
        os.remove(p)
    # 3/4 view: no labels, each hilt turned 35 degrees, camera 12 degrees up
    for t in texts:
        t.hide_render = True
    for r in roots:
        r.rotation_euler.z = math.radians(-35)
    e = math.radians(12)
    cam.location = (cx, -30 * math.cos(e), (top + bot) / 2 + 30 * math.sin(e))
    cam.rotation_euler = (math.radians(90) - e, 0, 0)
    sc.render.filepath = path_34
    bpy.ops.render.render(write_still=True)
    for r in roots:
        r.rotation_euler.z = 0

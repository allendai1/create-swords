# Detailed katana hilt (koshirae) for Create Swords!, built from code in Blender.
# Reuses the palette / material / station helpers from Models/Stations/build_stations.py:
#   ns = {"__name__": "lib"}; exec(build_stations.py, ns); exec(build_hilt.py, ns); ns["build_katana"]()
# Units are studs. The grip runs up +Z from the guard (z = 0 is the top of the tsuba); the blade hangs
# down -Z. Width (edge to spine) is X with the edge toward -X; thickness is Y, the front face is -Y.
# The hilt's root empty sits at the middle of the grip, like the game's `Handle` part.
import math
import bmesh
from mathutils import Vector

HILT = dict(
    diamonds=4,         # whole front-face crossings between the fuchi and the kashira; sets the grip length
    tsuba_r=0.26, tsuba_t=0.06,
    colors=dict(ito="indigo", same="paper", fittings="gold", band="iron_dk", tsuba="iron", rim="gold",
                habaki="ingot_dull", blade="steel"),
)
# Grip section and wrap (approved on a test section 2026-10-19).
WRAP2 = dict(a=0.1, b=0.065, n=4.0,      # half-width, half-thickness, squareness of the section
             pitch=0.24,                 # z-distance between crossings on the same face
             cover=0.66,                 # z-span of one cord as a fraction of the pitch; above half,
                                         # so passes overlap along the edges and the openings close
                                         # to diamond points on the flat faces
             h=0.009,                    # cord thickness
             steps=72)                   # samples per pitch along each cord
# Katana blade for review (game scale: 0.05 studs/cm). Preview only, not exported with the hilt.
BLADE = dict(nagasa=3.5, sori=0.09, motohaba=0.16, sakihaba=0.115, kasane=0.04, kissaki=0.18)

PAL.setdefault("ingot_dull", (0.85, 0.48, 0.22))  # copper habaki


def mesh_obj(name, bm, color, loc=(0, 0, 0), smooth=True):
    """Like _finish, but no automatic bevel: the hilt parts carry their own profiles."""
    auto_uv(bm)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = smooth
    if smooth:
        me.set_sharp_from_angle(angle=math.radians(40))
    me.materials.append(mat(color))
    c, root = _coll[0]
    o = bpy.data.objects.new(name, me)
    c.objects.link(o)
    o.parent = root
    o.location = loc
    return o


def _outward(bm):
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])


def lathe(name, profile, color, sx=1.0, sy=1.0, segments=48, loc=(0, 0, 0), closed=False, smooth=True):
    """Revolve a (r, z) profile around Z, scaled to an oval by sx / sy. A profile point with r == 0
    at either end becomes a cap; closed=True joins the last point back to the first (a ring)."""
    bm = bmesh.new()
    angles = [2 * math.pi * i / segments for i in range(segments)]
    rings, centers = [], {}
    for idx, (r, z) in enumerate(profile):
        if r == 0:
            centers[idx] = bm.verts.new((0, 0, z))
            rings.append(None)
        else:
            rings.append([bm.verts.new((r * sx * math.cos(a), r * sy * math.sin(a), z)) for a in angles])
    pairs = list(zip(range(len(profile) - 1), range(1, len(profile))))
    if closed:
        pairs.append((len(profile) - 1, 0))
    for i, j in pairs:
        A, B = rings[i], rings[j]
        for k in range(segments):
            n = (k + 1) % segments
            if A is None:
                bm.faces.new((centers[i], B[n], B[k]))
            elif B is None:
                bm.faces.new((A[k], A[n], centers[j]))
            else:
                bm.faces.new((A[k], A[n], B[n], B[k]))
    _outward(bm)
    return mesh_obj(name, bm, color, loc, smooth)


def cut(target, cutters):
    """Boolean-difference the cutters out of target, apply, delete the cutters."""
    for cobj in cutters:
        m = target.modifiers.new("cut", "BOOLEAN")
        m.operation = "DIFFERENCE"
        m.solver = "EXACT"
        m.object = cobj
    dg = bpy.context.evaluated_depsgraph_get()
    new = bpy.data.meshes.new_from_object(target.evaluated_get(dg))
    old = target.data
    target.modifiers.clear()
    bm = bmesh.new()  # clean the boolean result: weld, drop slivers, triangulate n-gons (Roblox QA)
    bm.from_mesh(new)
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-5)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-5, edges=bm.edges[:])
    bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 4])
    bm.to_mesh(new)
    bm.free()
    target.data = new
    bpy.data.meshes.remove(old)
    for cobj in cutters:
        bpy.data.objects.remove(cobj, do_unlink=True)
    new.set_sharp_from_angle(angle=math.radians(40))


# ---------------------------------------------------------------- grip section and wrap

def section_table(a, b, n, samples=720):
    """Points and outward normals around a superellipse, evenly spaced by arc length (u in 0..1)."""
    pts = []
    for i in range(samples):
        t = 2 * math.pi * i / samples
        c, s = math.cos(t), math.sin(t)
        pts.append(Vector((a * math.copysign(abs(c) ** (2 / n), c), b * math.copysign(abs(s) ** (2 / n), s), 0)))
    seg = [(pts[(i + 1) % samples] - pts[i]).length for i in range(samples)]
    total = sum(seg)
    cum = [0.0]
    for d in seg[:-1]:
        cum.append(cum[-1] + d)

    def at_u(u):
        target = (u % 1.0) * total
        lo, hi = 0, samples - 1
        while lo < hi:  # last index with cum <= target
            mid = (lo + hi + 1) // 2
            if cum[mid] <= target:
                lo = mid
            else:
                hi = mid - 1
        i, j = lo, (lo + 1) % samples
        f = (target - cum[i]) / seg[i]
        p = pts[i].lerp(pts[j], f)
        tang = (pts[j] - pts[i]).normalized()
        return p, Vector((tang.y, -tang.x, 0))  # outward for a counter-clockwise outline
    front = min((i for i in range(samples) if pts[i].y < 0), key=lambda i: abs(pts[i].x))  # centre of the -Y face
    return at_u, total, cum[front] / total


def section_loft(name, rings, color, W=WRAP2, segments=96, closed=False, caps=True):
    """Loft offset copies of the grip section: rings = [(outward offset, z), ...]. Open lofts get
    triangle-fan caps; closed=True joins the last ring back to the first (a band)."""
    at_u, _, _ = section_table(W["a"], W["b"], W["n"])
    samples = [at_u(i / segments) for i in range(segments)]
    bm = bmesh.new()
    loops = [[bm.verts.new(p + nrm * d + Vector((0, 0, z))) for p, nrm in samples] for d, z in rings]
    pairs = list(zip(loops, loops[1:])) + ([(loops[-1], loops[0])] if closed else [])
    for A, B in pairs:
        for k in range(segments):
            n = (k + 1) % segments
            bm.faces.new((A[k], A[n], B[n], B[k]))
    if caps and not closed:
        for ring, (d, z), flip in ((loops[0], rings[0], True), (loops[-1], rings[-1], False)):
            c = bm.verts.new((0, 0, z))
            for k in range(segments):
                n = (k + 1) % segments
                bm.faces.new((ring[n], ring[k], c) if flip else (ring[k], ring[n], c))
    return mesh_obj(name, bm, color)  # built outward: CCW rings, rising z


def flat_core(name, z0, z1, color, W=WRAP2, segments=96):
    return section_loft(name, [(0.0, z0), (0.0, z1)], color, W, segments)


def flat_band(name, hand, over_parity, z0, z1, color, W=WRAP2, phase_z=None):
    """One flat cord from z0 to z1. hand = +1 / -1 for the two opposite helices; both cross at the
    centre of the front face at phase_z (default z0) and every pitch / 2 from there (front, back ...).
    Each top point checks whether it lies over the other cord; if so, the crossing it belongs to decides
    which cord is on top (alternating), and only the upper cord lifts one thickness, so the two never
    share a surface. Ends are cut flat at z0 / z1 (hidden under the fittings)."""
    at_u, P, u_front = section_table(W["a"], W["b"], W["n"])
    pitch, h = W["pitch"], W["h"]
    zp = z0 if phase_z is None else phase_z
    dzw = W["cover"] * pitch / 2                    # half the cord width, measured along z
    tops = (-0.9, -0.45, 0.0, 0.45, 0.9)

    def lifted(zc, zv):
        base = 2 * zp - zc                          # the other cord's centre line at this u (mod pitch)
        zb = base + round((zv - base) / pitch) * pitch
        if abs(zv - zb) >= dzw:
            return 0.0
        j = round(((zc + zb) / 2 - zp) / (pitch / 2))   # the crossing these two passes share
        upper = (j // 2) % 2 == over_parity
        return 1.0 if (upper if hand > 0 else not upper) else 0.0

    steps = max(2, int((z1 - z0) / pitch * W["steps"]))
    bm = bmesh.new()
    rows = []
    for s in range(steps + 1):
        zc = z0 + (z1 - z0) * s / steps             # point on the cord's centre line
        p, nrm = at_u(u_front + hand * (zc - zp) / pitch)
        row = []
        for f in (-1.0,) + tops + (1.0,):
            zv = min(z1, max(z0, zc + f * dzw))
            lift = -0.002 if abs(f) == 1.0 else h * (1 + lifted(zc, zv))  # near-vertical walls: crisp edges
            row.append(bm.verts.new(p + nrm * (lift + 0.0005) + Vector((0, 0, zv))))
        rows.append(row)
    for r0, r1 in zip(rows, rows[1:]):
        for i in range(len(r0) - 1):
            bm.faces.new((r0[i], r0[i + 1], r1[i + 1], r1[i]))
    # the flat-cut ends collapse some points: weld them and drop the slivers
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-5)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-5, edges=bm.edges[:])
    # an open ribbon: orient every face away from the grip axis, consistently, from one probe face
    bm.normal_update()
    bm.faces.ensure_lookup_table()
    probe = bm.faces[(len(rows) // 2) * (len(rows[0]) - 1) + len(rows[0]) // 2]  # a top face mid-cord
    c = probe.calc_center_median()
    if probe.normal.dot(Vector((c.x, c.y, 0))) < 0:
        bmesh.ops.reverse_faces(bm, faces=bm.faces[:])
    return mesh_obj(name, bm, color)


def menuki(name, z, side, color, W=WRAP2, scale=0.75):
    """Small gold ornament on a flat face, under the cord: a three-bloom cluster."""
    b = W["b"]
    bm = bmesh.new()
    for dz, dx, r in ((0, 0, 0.032), (0.045, 0.02, 0.024), (-0.045, -0.02, 0.024)):
        r, dz, dx = r * scale, dz * scale, dx * scale
        tmp = bmesh.new()
        bmesh.ops.create_uvsphere(tmp, u_segments=16, v_segments=10, radius=r)
        for v in tmp.verts:
            v.co = Vector((v.co.x + dx, v.co.y * 0.4 + side * (b + 0.003), v.co.z + z + dz))
        me = bpy.data.meshes.new("_tmp")
        tmp.to_mesh(me)
        tmp.free()
        bm.from_mesh(me)
        bpy.data.meshes.remove(me)
    return mesh_obj(name, bm, color)


def wrap_test(x=3, y=0, crossings=3, name="WrapTest"):
    """A short section of the wrap for review: `crossings` front-face crossings."""
    W, C = WRAP2, HILT["colors"]
    root = station(name, x, y)
    span = W["pitch"] * crossings
    flat_core("Core", -0.06, span + 0.06, C["same"])
    flat_band("CordA", 1, 0, -0.02, span + 0.02, C["ito"])
    flat_band("CordB", -1, 0, -0.02, span + 0.02, C["ito"])
    return root


# ---------------------------------------------------------------- hilt

def build_hilt(x=0, y=0, name="KatanaHilt"):
    """Returns (root, mid): mid is the z of the grip middle that the root sits at."""
    H, W, C = HILT, WRAP2, HILT["colors"]
    tt = H["tsuba_t"]
    root = station(name, x, y)
    # stack along Z: habaki < seppa < tsuba < seppa < fuchi < wrapped core < kashira
    z_su0, z_su1 = 0.0, 0.012
    z_f0, z_f1 = z_su1, z_su1 + 0.05
    w0 = z_f1                               # visible wrap: a whole number of pitches, so it starts and
    w1 = w0 + H["diamonds"] * W["pitch"]    # ends on a front-face crossing at the fuchi and the kashira
    z_k0, z_k1 = w1, w1 + 0.06
    phase = w0

    flat_core("Core", z_f0 + 0.005, z_k0 + 0.042, C["same"])  # ends clear of the cords' cut ends
    for nm, hand, tuck in (("CordA", 1, 0.03), ("CordB", -1, 0.026)):  # ends tuck under the fittings,
        flat_band(nm, hand, 0, w0 - tuck, w1 + tuck, C["ito"], phase_z=phase)  # cut at different depths
    menuki("MenukiFront", w0 + 2.5 * W["pitch"], -1, C["fittings"])     # front window toward the kashira
    menuki("MenukiBack", w0 + 1.0 * W["pitch"], 1, C["fittings"])       # back window toward the fuchi

    # slim fittings that follow the flat grip section (offsets clear the cords' 2 x 0.009 + 0.0005)
    section_loft("Fuchi", [(0.019, z_f0), (0.024, z_f0 + 0.006), (0.024, z_f1 - 0.005), (0.02, z_f1)], C["fittings"])
    section_loft("Kashira", [(0.02, z_k0), (0.024, z_k0 + 0.005), (0.024, z_k0 + 0.032),
                             (0.014, z_k1 - 0.01), (-0.015, z_k1 - 0.002), (-0.032, z_k1)], C["fittings"])
    section_loft("KashiraBand", [(0.012, z_k0 + 0.014), (0.027, z_k0 + 0.014), (0.027, z_k0 + 0.022),
                                 (0.012, z_k0 + 0.022)], C["band"], closed=True)
    section_loft("SeppaUpper", [(0.034, z_su0), (0.034, z_su1)], C["fittings"])
    section_loft("SeppaLower", [(0.034, -tt - 0.012), (0.034, -tt)], C["fittings"])

    # tsuba: plate, slim raised rim, two hitsu-ana and four small sukashi cut through
    R = H["tsuba_r"]
    plate = lathe("Tsuba", [(0, -tt + 0.008), (R - 0.016, -tt + 0.008), (R - 0.016, -0.008), (0, -0.008)],
                  C["tsuba"], segments=64)
    lathe("TsubaRim", [(R - 0.026, -tt), (R - 0.003, -tt), (R, -tt + 0.005), (R, -0.005), (R - 0.003, 0.0),
                       (R - 0.026, 0.0)], C["rim"], segments=64, closed=True)
    cutters = []
    for s in (-1, 1):  # hitsu-ana either side of the blade's flat (along Y)
        cutters.append(lathe("_c", [(0, -0.2), (1, -0.2), (1, 0.2), (0, 0.2)], C["tsuba"], sx=0.05, sy=0.028,
                             segments=32, loc=(0, s * 0.155, 0)))
    for k in range(4):  # small round sukashi on the diagonals
        ang = math.radians(45 + 90 * k)
        cutters.append(lathe("_c", [(0, -0.2), (1, -0.2), (1, 0.2), (0, 0.2)], C["tsuba"], sx=0.022, sy=0.022,
                             segments=24, loc=(math.cos(ang) * 0.17, math.sin(ang) * 0.17, 0)))
    cut(plate, cutters)

    # habaki: copper blade collar under the lower seppa
    zh1 = -tt - 0.012
    lathe("Habaki", [(0, zh1 - 0.12), (0.85, zh1 - 0.12), (1.0, zh1 - 0.022), (1.0, zh1), (0, zh1)],
          C["habaki"], sx=0.085, sy=0.026, segments=40)  # preview only: the game's Habaki is a 0.18 x 0.138 x 0.06 box Part (2026-10-20), since this oval let the blade root poke through

    mid = (z_su0 + z_k1) / 2  # root at the middle of the grip, like the game's Handle part
    for o in bpy.data.collections[name].objects:
        if o is not root:
            o.location.z -= mid
    return root, mid, zh1


def build_blade(x, y, z_top, name="KatanaBlade", stations=72):
    """Curved katana blade hanging from z_top: edge toward -X, sori bows the middle toward the edge,
    tapering width and thickness, kissaki curving up to the spine. Review prop."""
    B, C = BLADE, HILT["colors"]
    root = station(name, x, y)
    Lb = B["nagasa"]
    s_k = 1 - B["kissaki"] / Lb
    bm = bmesh.new()
    rings = []
    for i in range(stations):
        s = i / (stations - 1) * (1 - 1e-3)
        z = z_top - s * Lb
        w = B["motohaba"] + (B["sakihaba"] - B["motohaba"]) * s
        t = B["kasane"] * (1 - 0.35 * s)
        spine = w / 2 + 4 * B["sori"] * s * s                # leaves the habaki on the grip axis, curving
                                                             # toward the spine; sori = depth from the chord
        if s > s_k:                                          # kissaki: edge curves up to the spine
            q = (s - s_k) / (1 - s_k)
            w *= math.sqrt(max(0.0, 1 - q * q))
            t *= 1 - 0.6 * q
        edge = spine - w
        ridge = spine - 0.32 * w                             # shinogi
        rings.append([bm.verts.new(v) for v in (
            (edge, 0, z), (ridge, -t / 2, z), (spine, -t * 0.32, z), (spine, t * 0.32, z), (ridge, t / 2, z))])
    tip = bm.verts.new((rings[-1][2].co.x, 0, z_top - Lb))
    for A, Bn in zip(rings, rings[1:]):
        for k in range(5):
            n = (k + 1) % 5
            bm.faces.new((A[k], A[n], Bn[n], Bn[k]))
    for k in range(5):
        bm.faces.new((rings[-1][k], rings[-1][(k + 1) % 5], tip))
    bm.faces.new(rings[0][::-1])
    _outward(bm)
    o = mesh_obj("Blade", bm, C["blade"])
    o.data.set_sharp_from_angle(angle=math.radians(25))
    return root


def build_katana(x=0, y=0, z=0.0):
    """Hilt plus a review blade, both rooted at the grip middle; z lifts the whole sword."""
    root, mid, zh1 = build_hilt(x, y)
    broot = build_blade(x, y, zh1 - mid - 0.02)
    root.location.z = broot.location.z = z
    return root, broot


# ---------------------------------------------------------------- game export

# Parts merged by colour role; the game recolours each role per hilt recipe (ReplicatedStorage.Shared.Hilts).
GAME_ROLES = {
    "Same": ("Core",),
    "Ito": ("CordA", "CordB"),
    "Fittings": ("Fuchi", "SeppaUpper", "SeppaLower", "MenukiFront", "MenukiBack"),
    "Kashira": ("Kashira",),
    "Band": ("KashiraBand",),
    "Tsuba": ("Tsuba",),
    "Rim": ("TsubaRim",),
    "Habaki": ("Habaki",),
}


def build_game_hilt(name="KatanaHiltGame"):
    """The hilt at the origin (root = grip middle), merged into one object per GAME_ROLES role."""
    root, mid, zh1 = build_hilt(0, 0, name=name)
    objs = {o.name.split(".")[0]: o for o in bpy.data.collections[name].objects if o.type == "MESH"}
    for role, parts in GAME_ROLES.items():
        group = [objs[p] for p in parts]
        if len(group) > 1:
            with bpy.context.temp_override(active_object=group[0], selected_editable_objects=group, selected_objects=group):
                bpy.ops.object.join()
        group[0].name = group[0].data.name = role
    return root, mid, zh1


# ---------------------------------------------------------------- flame guard (etch prototype, 2026-10-19)
# An original flame-outline tsuba for the Flame etch: the rim breaks into leaning flame tongues all the
# way round. Three colour-role parts, same frame as the hilt (z = 0 is the top of the guard):
#   FlameRim   - bright band following the flame outline, full guard thickness
#   FlameCore  - dark plate inside the rim, slightly thinner, so the rim stands proud
#   FlameInner - a smaller flame inlay on both faces, tongues between the outer ones
# The game colours them from the etch (Core = body, Rim = flame, Inner = flame lightened).
FLAME = dict(r0=0.21, amp=0.1, tongues=7, lean=0.72, rim=0.022,
             inner_r0=0.115, inner_amp=0.06, t=0.06, samples=240)


def flame_radius(theta, r0, amp, tongues, lean, phase=0.0):
    """Star-shaped flame outline. Each tongue swells up a rounded belly to a sharp tip at `lean` of its
    period, then drops steeply on a concave flank into the next valley, so the tongues read as flames
    licking round the guard rather than symmetric spikes; heights vary per tongue."""
    t = theta / (2 * math.pi) * tongues + phase
    i = math.floor(t)
    p = t - i
    if p < lean:
        g = (p / lean) ** 0.65                      # convex belly, still sloped at the tip
    else:
        g = (1 - (p - lean) / (1 - lean)) ** 2.6     # steep concave fall: a sharp, curling tip
    x = math.sin((i % tongues) * 127.1 + 311.7) * 43758.5453
    h = 0.75 + 0.25 * (x - math.floor(x))
    return r0 + amp * h * g


def _ring(bm, radii, z):
    n = len(radii)
    return [bm.verts.new((r * math.cos(2 * math.pi * k / n), r * math.sin(2 * math.pi * k / n), z))
            for k, r in enumerate(radii)]


def flame_plate(name, radii, z0, z1, color):
    """Closed solid: the outline extruded from z0 to z1, capped with fans (star-shaped outline)."""
    bm = bmesh.new()
    b, t = _ring(bm, radii, z0), _ring(bm, radii, z1)
    cb, ct = bm.verts.new((0, 0, z0)), bm.verts.new((0, 0, z1))
    n = len(radii)
    for k in range(n):
        m = (k + 1) % n
        bm.faces.new((b[k], b[m], t[m], t[k]))
        bm.faces.new((t[k], t[m], ct))
        bm.faces.new((b[m], b[k], cb))
    return mesh_obj(name, bm, color)


def flame_band(name, outer, inner, z0, z1, color):
    """Closed ring solid between two outlines (outer wall, top, inner wall, bottom)."""
    bm = bmesh.new()
    ob, ot, it, ib = _ring(bm, outer, z0), _ring(bm, outer, z1), _ring(bm, inner, z1), _ring(bm, inner, z0)
    n = len(outer)
    for k in range(n):
        m = (k + 1) % n
        bm.faces.new((ob[k], ob[m], ot[m], ot[k]))   # outer wall, outward
        bm.faces.new((ot[k], ot[m], it[m], it[k]))   # top, +z
        bm.faces.new((it[k], it[m], ib[m], ib[k]))   # inner wall, toward the axis
        bm.faces.new((ib[k], ib[m], ob[m], ob[k]))   # bottom, -z
    return mesh_obj(name, bm, color)


def build_flame_guard(x=0, y=0, name="FlameGuard", hilt_frame=True):
    """The flame tsuba. hilt_frame=True places it like the hilt's tsuba relative to a root at the grip
    middle (same frame as build_hilt / build_game_hilt), so the game can swap it for Tsuba + Rim."""
    F = FLAME
    n = F["samples"]
    thetas = [2 * math.pi * k / n for k in range(n)]
    outer = [flame_radius(th, F["r0"], F["amp"], F["tongues"], F["lean"]) for th in thetas]
    core = [r - F["rim"] for r in outer]
    inner = [flame_radius(th, F["inner_r0"], F["inner_amp"], F["tongues"], F["lean"], phase=0.5) for th in thetas]
    tt = F["t"]
    root = station(name, x, y)
    flame_band("FlameRim", outer, core, -tt, 0.0, "red")
    flame_plate("FlameCore", core, -tt + 0.006, -0.006, "iron_dk")
    bm_parts = []
    for z0, z1 in ((-0.006, -0.002), (-tt + 0.002, -tt + 0.006)):  # inlay on both faces
        bm_parts.append(flame_plate("_inner", inner, z0, z1, "gold"))
    with bpy.context.temp_override(active_object=bm_parts[0], selected_editable_objects=bm_parts, selected_objects=bm_parts):
        bpy.ops.object.join()
    bm_parts[0].name = bm_parts[0].data.name = "FlameInner"
    if hilt_frame:
        H, W = HILT, WRAP2
        grip_top = 0.012 + 0.05 + H["diamonds"] * W["pitch"] + 0.06   # seppa + fuchi + wrap + kashira
        mid = grip_top / 2
        for o in bpy.data.collections[name].objects:
            if o is not root:
                o.location.z -= mid
    return root


# ---------------------------------------------------------------- guard set (2026-10-20)
# More tsuba shapes for the hilt recipes, on the same three colour roles and frame as the flame guard:
# <Name>Rim (band along the outline), <Name>Core (plate, thinner), <Name>Inner (inlay ring on both faces,
# optional). The grip stays the approved KatanaHilt one; only the guard changes.

def superellipse(theta, n):
    return (abs(math.cos(theta)) ** n + abs(math.sin(theta)) ** n) ** (-1 / n)


GUARDS = dict(
    # four lobes with sharp notches on the diagonals (mokko)
    Mokko=dict(outline=lambda th: 0.215 + 0.04 * abs(math.cos(2 * th)) ** 0.45,
               inner=lambda th: 0.178 + 0.03 * abs(math.cos(2 * th)) ** 0.45, hitsu=True),
    # sixteen rounded petals (kiku, chrysanthemum)
    Kiku=dict(outline=lambda th: 0.232 + 0.022 * abs(math.cos(8 * th)) ** 0.5,
              inner=lambda th: 0.16 + 0.018 * abs(math.cos(8 * th + math.pi / 2)) ** 0.5, hitsu=False),
    # rounded square (kaku), corners on the diagonals
    Kaku=dict(outline=lambda th: 0.2 * superellipse(th, 5.0),
              inner=None, hitsu=True, square_windows=True),
    # six uneven cloud lobes (kumo)
    Kumo=dict(outline=lambda th: 0.205 + 0.045 * abs(math.sin(3 * th + 0.4)) ** 0.6
              * (0.8 + 0.2 * math.sin(th * 2 + 1.0)),
              inner=None, hitsu=False),
    # round wheel with eight spoked windows (kuruma)
    Kuruma=dict(outline=lambda th: 0.245, inner=None, hitsu=False, spokes=8),
)


def prism(name, pts, z0, z1, color):
    """Closed solid: a polygon (star-shaped about its centroid) extruded from z0 to z1."""
    bm = bmesh.new()
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    b = [bm.verts.new((x, y, z0)) for x, y in pts]
    t = [bm.verts.new((x, y, z1)) for x, y in pts]
    cb, ct = bm.verts.new((cx, cy, z0)), bm.verts.new((cx, cy, z1))
    n = len(pts)
    for k in range(n):
        m = (k + 1) % n
        bm.faces.new((b[k], b[m], t[m], t[k]))
        bm.faces.new((t[k], t[m], ct))
        bm.faces.new((b[m], b[k], cb))
    _outward(bm)
    return mesh_obj(name, bm, color)


def build_guard(kind, x=0, y=0, hilt_frame=True, colors=("iron_dk", "gold", "gold")):
    """One guard from GUARDS as <kind>Guard (root at the grip middle, like build_flame_guard)."""
    G, n, tt, rim = GUARDS[kind], 240, 0.06, 0.022
    name = kind + "Guard"
    thetas = [2 * math.pi * k / n for k in range(n)]
    outer = [G["outline"](th) for th in thetas]
    core_r = [r - rim for r in outer]
    root = station(name, x, y)
    flame_band(kind + "Rim", outer, core_r, -tt, 0.0, colors[1])
    core = flame_plate(kind + "Core", core_r, -tt + 0.006, -0.006, colors[0])
    big = [(0, -0.2), (1, -0.2), (1, 0.2), (0, 0.2)]
    cutters = []
    if G.get("hitsu"):  # hitsu-ana either side of the blade's flat (along Y)
        for s in (-1, 1):
            cutters.append(lathe("_c", big, colors[0], sx=0.042, sy=0.022, segments=32, loc=(0, s * 0.14, 0)))
    if G.get("square_windows"):  # four small rounded-square windows toward the corners
        for k in range(4):
            a = math.radians(45 + 90 * k)
            pts = [(math.cos(a) * 0.155 + 0.025 * superellipse(t, 4) * math.cos(t),
                    math.sin(a) * 0.155 + 0.025 * superellipse(t, 4) * math.sin(t))
                   for t in [2 * math.pi * j / 32 for j in range(32)]]
            cutters.append(prism("_c", pts, -0.2, 0.2, colors[0]))
    if G.get("spokes"):  # annular-sector windows between spokes
        m = G["spokes"]
        for k in range(m):
            a0, a1 = 2 * math.pi * k / m + 0.13, 2 * math.pi * (k + 1) / m - 0.13
            arc = [a0 + (a1 - a0) * j / 10 for j in range(11)]
            pts = [(0.19 * math.cos(a), 0.19 * math.sin(a)) for a in arc]
            pts += [(0.085 * math.cos(a), 0.085 * math.sin(a)) for a in reversed(arc)]
            cutters.append(prism("_c", pts, -0.2, 0.2, colors[0]))
    if cutters:
        cut(core, cutters)
    if G.get("inner"):  # inlay ring on both faces, outside the seppa
        inner = [G["inner"](th) for th in thetas]
        parts = [flame_band("_inner", inner, [r - 0.014 for r in inner], z0, z1, colors[2])
                 for z0, z1 in ((-0.006, -0.002), (-tt + 0.002, -tt + 0.006))]
        with bpy.context.temp_override(active_object=parts[0], selected_editable_objects=parts, selected_objects=parts):
            bpy.ops.object.join()
        parts[0].name = parts[0].data.name = kind + "Inner"
    if hilt_frame:
        H, W = HILT, WRAP2
        mid = (0.012 + 0.05 + H["diamonds"] * W["pitch"] + 0.06) / 2
        for o in bpy.data.collections[name].objects:
            if o is not root:
                o.location.z -= mid
    return root

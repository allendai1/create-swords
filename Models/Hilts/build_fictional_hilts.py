# Seven fictional hilts (Crescent Fang, Shard Blade, Moonbite, Serpent, Leviathan Cleaver, Thornspire, Seraph) for
# Sell Swords!, built from code in Blender (2026-10-29). Runs after the earlier hilt helpers, in one namespace:
#   ns = {"__name__": "lib"}
#   for f in ("Models/Stations/build_stations.py", "Models/Hilts/build_hilt.py", "Models/Hilts/build_western_hilts.py",
#             "Models/Hilts/build_more_hilts.py", "Models/Hilts/build_fictional_hilts.py"):
#       exec(open(f).read(), ns)
#   ns["BLADES"] = json.load(open("Models/Hilts/Fictional/blades.json"))   # per-station refined blade params (design.py)
#   ns["TRACED"] = json.load(open("Models/Hilts/Fictional/traced.json"))   # the traced reference swords (trace_ref.py)
#   ns["build_fictional_hilts"](); ns["export_western"](folder, kinds=ns["FICTIONAL"])
# Checks used: blender-asset-qa qa_check.py --profile roblox (with the review blade, contact tolerance 0.008), and
# Fictional/iou.py (front-silhouette IoU against the straightened reference) for Seraph and Thornspire.
# Same frame as build_western_hilts: studs, root empty at the grip centre, the grip runs up +Z toward the pommel, the
# blade toward -Z; single edges toward -X (the blade's spine is +X), flats face +-Y. Each hilt is meshes named
# <Prefix>Grip / Guard / Pommel (coloured by the hilt tier in the game) plus extra parts the game keeps in their own
# colour (KeepLook in Studio): gems, white wings, gold bands, and the markings painted on the blade (decal sheets that
# follow the blade's surface 0.006 studs proud, from its per-station params).
import math
import bmesh
from mathutils import Vector

FICTIONAL = dict(
    CrescentFang=dict(grip=0.8, blade_offset=0.47, blade="crescentfang"),
    ShardBlade=dict(grip=0.75, blade_offset=0.45, blade="shardblade"),
    Moonbite=dict(grip=0.75, blade_offset=0.42, blade="moonbite"),
    Serpent=dict(grip=0.8, blade_offset=0.5, blade="serpent"),
    Leviathan=dict(grip=1.1, blade_offset=0.7, blade="leviathan"),
    Thornspire=dict(grip=1.34, blade_offset=0.736, blade="thornspire"),
    Seraph=dict(grip=1.07, blade_offset=1.342, blade="seraph"),
)
S = 0.05            # studs per cm (Blueprints.STUDS_PER_CM)
LIFT = 0.12         # cm a painted marking stands off the blade (0.006 studs)


# ---------------------------------------------------------------- helpers
def tri2d(pts, dr, h):
    """Constrained Delaunay inside the 2D outline pts: the outline, a ring dr inside it and a sparse h grid.
    Returns (points, triangles, boundary edges, distance-to-rim function)."""
    from mathutils.geometry import delaunay_2d_cdt
    n = len(pts)
    P = [Vector(q) for q in pts]
    xs, zs = [q.x for q in P], [q.y for q in P]

    def dist(q):
        best = 1e9
        for i in range(n):
            a, b = P[i], P[(i + 1) % n]
            ab = b - a
            t_ = max(0.0, min(1.0, (q - a).dot(ab) / max(1e-12, ab.length_squared)))
            best = min(best, (a + ab * t_ - q).length)
        return best

    def inside(q):
        c = False
        for i in range(n):
            a, b = P[i], P[(i + 1) % n]
            if (a.y > q.y) != (b.y > q.y) and q.x < a.x + (q.y - a.y) * (b.x - a.x) / (b.y - a.y):
                c = not c
        return c

    grid = []
    for i in range(n):
        a, b, c = P[i - 1], P[i], P[(i + 1) % n]
        if (b - a).length < 1e-9 or (c - b).length < 1e-9:
            continue
        e1, e2 = (b - a).normalized(), (c - b).normalized()
        nrm = Vector((-(e1.y + e2.y), e1.x + e2.x))
        if nrm.length < 1e-6:
            continue
        for sgn in (1, -1):
            q = b + nrm.normalized() * dr * sgn
            if inside(q) and dist(q) > 0.6 * dr:
                grid.append(q)
                break
    zz = min(zs) + h / 2
    while zz < max(zs):
        xx = min(xs) + h / 2 + (h / 2 if int((zz - min(zs)) / h) % 2 else 0)
        while xx < max(xs):
            q = Vector((xx, zz))
            if inside(q) and dist(q) > dr + 0.4 * h:
                grid.append(q)
            xx += h
        zz += h * 0.866
    out = delaunay_2d_cdt(P + grid, [], [list(range(n))], 1, 1e-7)
    vco = [Vector((q[0], q[1])) for q in out[0]]
    faces = [f for f in out[2] if len(f) >= 3]
    use = {}
    for f in faces:
        for i in range(len(f)):
            e = tuple(sorted((f[i], f[(i + 1) % len(f)])))
            use[e] = use.get(e, 0) + 1
    edges = [(f[i], f[(i + 1) % len(f)]) for f in faces for i in range(len(f))
             if use[tuple(sorted((f[i], f[(i + 1) % len(f)])))] == 1]
    return vco, faces, edges, dist


def shell(name, vco, faces, edges, front, back, color="neutral", smooth=True):
    """Closed solid from a 2D triangulation: front(q) and back(q) give each point's 3D position on the two faces."""
    bm = bmesh.new()
    F = [bm.verts.new(front(q)) for q in vco]
    B = [bm.verts.new(back(q)) for q in vco]
    for f in faces:
        bm.faces.new([F[i] for i in f])
        bm.faces.new([B[i] for i in f][::-1])
    for a_, b_ in edges:
        bm.faces.new((F[b_], F[a_], B[a_], B[b_]))
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-7)
    _outward(bm)
    return mesh_obj(name, bm, color, smooth=smooth)


def slab(name, pts, t, te=0.4, dr=0.025, h=0.09, taper=None):
    """A plate with real form through the (x, z) outline pts: t thick in the middle, te * t at the rim, rising over
    dr studs from the rim (a rounded bevel), times taper(x, z) when given. Closed, all triangles."""
    vco, faces, edges, dist = tri2d(pts, dr, h)

    def half(q):
        d = dist(q)
        return (te + (1 - te) * min(1.0, (0.0 if d < 1e-6 else d) / dr) ** 0.7) * t / 2 * (taper(q.x, q.y) if taper else 1.0)
    return shell(name, vco, faces, edges, lambda q: (q.x, half(q), q.y), lambda q: (q.x, -half(q), q.y))


def paint_poly(name, bm_map, polys_uw, lift=LIFT, depth=0.05, h=0.6):
    """Markings painted on both faces of the blade, from filled outlines in (u, w) (w in cm): thin closed shells
    following the blade's surface lift cm proud, one per outline and face."""
    L = bm_map.b["length"]
    objs = []
    for pts in polys_uw:
        vco, faces, edges, dist = tri2d([(u * L, w) for u, w in pts], 0.15, h)
        for side in (1, -1):
            objs.append(shell("_mark", vco, faces, edges,
                              lambda q, s=side: bm_map.point(q.x / L, q.y, s, lift),
                              lambda q, s=side: bm_map.point(q.x / L, q.y, s, lift - depth), smooth=False))
    return join(name, objs)


def paint_sym(name, bm_map, polys_uw, lift=LIFT, depth=0.05, h=0.6, keep=-1):
    """paint_poly made exactly symmetric (2026-10-29, Allen: the markings were "not symmetrical"; the picture shows the
    sword a little turned): outlines in (u, w) with w in cm off the blade's own middle at u ((spine + edge) / 2); only
    the half on the keep side (-1: toward the edge) is used, reflected to the other, and painted on both faces."""
    L = bm_map.b["length"]
    flat = bmesh.new()
    for pts in polys_uw:
        vco, faces, _, _ = tri2d([(u * L, w) for u, w in pts], 0.15, h)
        vs = [flat.verts.new((q.x, q.y, 0)) for q in vco]
        for f in faces:
            flat.faces.new([vs[i] for i in f])
    every = lambda: flat.verts[:] + flat.edges[:] + flat.faces[:]
    bmesh.ops.bisect_plane(flat, geom=every(), plane_co=(0, 0, 0), plane_no=(0, -keep, 0), clear_outer=True)
    bmesh.ops.mirror(flat, geom=every(), axis="Y", merge_dist=1e-6)
    bmesh.ops.triangulate(flat, faces=flat.faces[:])
    flat.normal_update()
    for f in flat.faces:
        if f.normal.z < 0:
            f.normal_flip()
    mid = lambda u: sum(bm_map.width(u)) / 2
    for v in flat.verts:   # kept on the blade, 0.15 cm in from its edges (the traced slashes ran past the game blade's)
        s, e = bm_map.width(v.co.x / L)
        half = max(0.0, (s - e) / 2 - 0.15)
        v.co.y = max(-half, min(half, v.co.y))
    bm = bmesh.new()
    for side in (1, -1):
        top = {v: bm.verts.new(bm_map.point(v.co.x / L, mid(v.co.x / L) + v.co.y, side, lift)) for v in flat.verts}
        bot = {v: bm.verts.new(bm_map.point(v.co.x / L, mid(v.co.x / L) + v.co.y, side, lift - depth)) for v in flat.verts}
        for f in flat.faces:
            bm.faces.new([top[v] for v in f.verts])
            bm.faces.new([bot[v] for v in f.verts][::-1])
        for e in flat.edges:
            if len(e.link_faces) == 1:
                lp = next(l for l in e.link_faces[0].loops if l.edge == e)
                a, b = lp.vert, lp.link_loop_next.vert
                bm.faces.new((top[b], top[a], bot[a], bot[b]))
    flat.free()
    _outward(bm)
    return mesh_obj(name, bm, "neutral", smooth=False)


def mirror_halves(obj, keep=-1):
    """A part made exactly symmetric across the hilt's centre plane (x = 0, through the blade's centre): the half on
    the keep side (-1: x <= 0) is kept and reflected (2026-10-29, as paint_sym)."""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    every = lambda: bm.verts[:] + bm.edges[:] + bm.faces[:]
    bmesh.ops.bisect_plane(bm, geom=every(), plane_co=(0, 0, 0), plane_no=(-keep, 0, 0), clear_outer=True)
    bmesh.ops.mirror(bm, geom=every(), axis="X", merge_dist=1e-5)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    _outward(bm)
    auto_uv(bm)
    bm.to_mesh(obj.data)
    bm.free()
    return obj


def mirror_x(pts):
    return [(-x, z) for x, z in pts]


def sym(half):
    """A closed outline from its +X half listed from the top centre round to the bottom centre."""
    return half + [(-x, z) for x, z in reversed(half) if abs(x) > 1e-9]


def interp(arr, f):
    i = max(0, min(len(arr) - 2, int(f)))
    t = f - i
    return arr[i] + (arr[i + 1] - arr[i]) * t


class BladeMap:
    """Blade-local (u, w) -> Blender point on the blade's +-Y surface, for a hilt with this blade offset.
    u: 0 at the blade root, 1 at the point; w: cm across from the centre line toward the spine (+) or edge (-)."""

    def __init__(self, b, bo):
        self.b, self.bo = b, bo
        self.c1 = (b["spine"][0] + b["edge"][0]) / 2

    def height(self, f, w):
        b = self.b
        s, e, r = interp(b["spine"], f), interp(b["edge"], f), interp(b["ridge"], f)
        th, eT, sT = interp(b["thick"], f), interp(b["edgeT"], f), interp(b["spineT"], f)
        rp = s + r * (e - s)
        t, ts, te = th / 2, th * sT / 2, eT / 2
        if w >= rp:
            k = min(1.0, max(0.0, (s - w) / max(1e-6, s - rp)))
            return ts + (t - ts) * k
        k = min(1.0, max(0.0, (rp - w) / max(1e-6, rp - e)))
        return t + (te - t) * k

    def point(self, u, w, side, lift=LIFT):
        b = self.b
        f = u * (b["N"] - 1)
        px, py, a = interp(b["px"], f), interp(b["py"], f), interp(b["ang"], f)
        x, y = px - math.sin(a) * w, py + math.cos(a) * w
        h = self.height(f, w) + lift
        return Vector((S * (y - self.c1), side * S * h, -(self.bo + S * x)))

    def width(self, u):
        f = u * (self.b["N"] - 1)
        return interp(self.b["spine"], f), interp(self.b["edge"], f)


def paint(name, bm_map, strokes, lift=LIFT, color="neutral", depth=0.05):
    """Markings painted on both faces of the blade: each stroke a thin closed shell (depth cm) standing lift cm proud of
    the blade's surface. strokes: (path, left, right[, k]) with path a list of (u, w) and left(s) / right(s) half widths
    in cm (s = 0..1 along the path, at least 0.025), k samples across."""
    bm = bmesh.new()
    L = bm_map.b["length"]
    for st in strokes:
        path, wl, wr = st[0], st[1], st[2]
        k = st[3] if len(st) > 3 else 3
        n = len(path)
        for side in (1, -1):
            shells = []
            for lf in (lift, lift - depth):
                rows = []
                for i, (u, w) in enumerate(path):
                    a = path[max(0, i - 1)]
                    c = path[min(n - 1, i + 1)]
                    tx, tw = (c[0] - a[0]) * L, c[1] - a[1]
                    ln = math.hypot(tx, tw) or 1
                    nx, nw = -tw / ln, tx / ln
                    s_ = i / (n - 1)
                    l_, r_ = max(0.025, wl(s_)), max(0.025, wr(s_)) if wr(s_) >= 0 else wr(s_)
                    row = []
                    for j in range(k):
                        q = -r_ + (l_ + r_) * j / (k - 1)
                        row.append(bm.verts.new(bm_map.point(u + nx * q / L, w + nw * q, side, lf)))
                    rows.append(row)
                shells.append(rows)
            O, I = shells
            for A, B in ((O, None), (I, None)):
                for r0, r1 in zip(A, A[1:]):
                    for j in range(k - 1):
                        bm.faces.new((r0[j], r0[j + 1], r1[j + 1], r1[j]))
            for i in range(n - 1):     # side walls
                for j in (0, k - 1):
                    bm.faces.new((O[i][j], O[i + 1][j], I[i + 1][j], I[i][j]))
            for i in (0, n - 1):       # end walls
                for j in range(k - 1):
                    bm.faces.new((O[i][j], O[i][j + 1], I[i][j + 1], I[i][j]))
    _outward(bm)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    return mesh_obj(name, bm, color, smooth=False)


def line(p0, p1, n=12):
    return [(p0[0] + (p1[0] - p0[0]) * i / n, p0[1] + (p1[1] - p0[1]) * i / n) for i in range(n + 1)]


def poly(pts, per=6):
    out = []
    for a, b in zip(pts, pts[1:]):
        out += line(a, b, per)[:-1]
    return out + [pts[-1]]


def const(v):
    return lambda s: v


def lens(v, p=1.0):
    return lambda s: v * math.sin(math.pi * s) ** p


def real_blade(root, bm_map, name):
    """The refined blade as a review prop (not exported): spine / ridge / edge rings, both faces."""
    c = bpy.data.collections.get("PreviewBlades") or bpy.data.collections.new("PreviewBlades")
    if c.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(c)
    b = bm_map.b
    bm = bmesh.new()
    rings = []
    for i in range(b["N"]):
        u = i / (b["N"] - 1)
        s, e = b["spine"][i], b["edge"][i]
        r = s + b["ridge"][i] * (e - s)
        ring = []
        for side in (1, -1):
            for w in ((s, r, e) if side > 0 else (e, r, s)):
                ring.append(bm.verts.new(bm_map.point(u, w, side, 0.0)))
        rings.append(ring)
    for A, B in zip(rings, rings[1:]):
        for k in range(6):
            m = (k + 1) % 6
            bm.faces.new((A[k], A[m], B[m], B[k]))
    bm.faces.new(rings[0][::-1])
    bm.faces.new(rings[-1])
    _outward(bm)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    auto_uv(bm)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(mat("steel"))
    o = bpy.data.objects.new(name, me)
    c.objects.link(o)
    o.parent = root
    return o


# ---------------------------------------------------------------- the hilts
# Each builder returns (root, numbers) with numbers = GripLength / BladeOffset / Back as built, and the names of the
# parts the game keeps in their own colour.

def clean(q, d=0.9):
    """A traced outline without points closer than d pixels to the previous one (they pinch the triangulation)."""
    out = [q[0]]
    for a in q[1:]:
        if abs(a[0] - out[-1][0]) + abs(a[1] - out[-1][1]) >= d:
            out.append(a)
    if len(out) > 3 and abs(out[0][0] - out[-1][0]) + abs(out[0][1] - out[-1][1]) < d:
        out.pop()
    # drop zero-width spikes (the outline running out and straight back), which make non-manifold rim walls
    changed = True
    while changed and len(out) > 3:
        changed = False
        for i in range(len(out)):
            a, b = out[i - 1], out[(i + 1) % len(out)]
            if abs(a[0] - b[0]) + abs(a[1] - b[1]) < 1.5:
                del out[i]
                changed = True
                break
    return out


def _traced(name, k):
    """Helpers over TRACED[name] (the straightened reference, scratch trace_ref.py): pixel -> stud converters and
    the traced regions."""
    T = TRACED[name]
    ax, gr = T["axis"], T["grip_row"]
    X = lambda px: (px - ax) * k
    Z = lambda py: (py - gr) * k
    pts = lambda q: [(X(px), Z(py)) for px, py in clean(q["pts"])]
    solid = lambda lst, a=0: [q for q in lst if not q["hole"] and q["area"] >= a]
    rows = lambda key: {int(r): v for r, v in T[key].items()}
    return T, X, Z, pts, solid, rows


def _sections(widths, X, Z, k, ratio, tol=0.8, skip=()):
    """Stack sections from traced row extents {row: (left, right)}: half width, ratio across, centre offset; rows kept
    where the width or centre leaves a straight run by more than tol pixels (Douglas-Peucker)."""
    rs = [r for r in sorted(widths) if r not in skip]
    w = {r: ((widths[r][1] - widths[r][0] + 1) / 2, (widths[r][0] + widths[r][1] + 1) / 2) for r in rs}

    def keep(i0, i1, out):
        best, bi = 0.0, None
        for i in range(i0 + 1, i1):
            t = (rs[i] - rs[i0]) / (rs[i1] - rs[i0])
            d = max(abs(w[rs[i]][j] - (w[rs[i0]][j] + t * (w[rs[i1]][j] - w[rs[i0]][j]))) for j in (0, 1))
            if d > best:
                best, bi = d, i
        if bi is not None and best > tol:
            keep(i0, bi, out)
            out.add(bi)
            keep(bi, i1, out)
    idx = {0, len(rs) - 1}
    keep(0, len(rs) - 1, idx)
    return [(Z(rs[i]), w[rs[i]][0] * k, w[rs[i]][0] * k * ratio, X(w[rs[i]][1])) for i in sorted(idx)]


def build_seraph_hilt(x=0, y=0, name="SeraphHiltGame", p="SE_"):
    """Traced from the left sword of References/Swords/roblox unique swords.png (straightened; trace_ref.py): the
    blade root is row 540, the grip centre row 723, 0.007335 studs a pixel."""
    W = FICTIONAL["Seraph"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    bmp = BladeMap(BLADES[W["blade"]], bo)
    k = 0.007335
    T, X, Z, pts, solid, rows = _traced("seraph", k)
    R = T["regions"]
    # grip: the dark grip and its socket, row by row from the picture
    gw = rows("grip_w")
    secs = _sections(gw, X, Z, k, 0.78)
    top = min(gw)
    stack(p + "Grip", [(Z(top - 1), 0, 0, secs[0][3])] + secs, seg=16)
    # pommel: the gold finial, six-sided
    pw = rows("pommel_w")
    ps = _sections(pw, X, Z, k, 0.72, tol=0.6)
    stack(p + "Pommel", ps[:-1] + [(Z(max(pw) + 1), 0, 0, ps[-1][3])], seg=6)
    back = Z(max(pw) + 1)
    # gem
    for q in solid(R["gem"], 50):
        g = pts(q)   # the traced gem is its bright core; the cut stone is half as wide again (its dark facets read as grip)
        cx_, cz_ = sum(v[0] for v in g) / len(g), sum(v[1] for v in g) / len(g)
        slab(p + "Gem", [(cx_ + (v[0] - cx_) * 1.5, cz_ + (v[1] - cz_) * 1.25) for v in g], 0.29, te=0.55, dr=0.02, h=0.05)
    # guard (gold, tier-coloured): the arrowhead and its fins over the blade's base, the rims and trims over the
    # white parts, and the centre line painted up the blade
    cb = sum((T["outline"][str(r)][0][0] + T["outline"][str(r)][-1][1]) / 2 for r in range(100, 221, 2)) / 61
    s_cm = 76.0 / (540 - 22)
    uw = lambda q: [((540 - py) / (540 - 22), (px - cb) * s_cm) for px, py in clean(q["pts"])]
    parts = []
    for q in solid(R["arrow"], 10):   # one gold layer: rim 0.056 thick, so it covers the blade (0.045) and the white
        parts.append(slab("_gold", pts(q), 0.07, te=0.8, dr=0.015))
    parts.append(paint_poly("_line", bmp, [uw(q) for q in solid(R["line"], 30)]))
    join(p + "Guard", parts)
    # white crest and wings under the gold (kept white): one plate, thinning toward the wing tips
    wt = lambda x_, z_: 1 - 0.4 * min(1.0, max(0.0, (abs(x_) - 0.25) / 0.4))
    join(p + "Wings", [slab("_white", pts(q), 0.05, te=0.5, dr=0.02, taper=wt) for q in solid(R["base"], 50)])
    # dark cut-outs (kept dark): the spike and teardrops on the arrowhead, the slits on the wings
    cuts = []
    for q in solid(R["cuts"], 20):
        mean = sum(py for _, py in q["pts"]) / len(q["pts"])
        cuts.append(slab("_cut", pts(q), 0.078 if mean < 556 else 0.058, te=0.95, dr=0.004, h=0.05))
    join(p + "Trim", cuts)
    for part in ("Guard", "Wings", "Trim", "Gem", "Grip", "Pommel"):   # one half, reflected (paint_sym)
        mirror_halves(bpy.data.objects[p + part])
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(back, 4)), ["Gem", "Wings", "Trim"]


def build_thornspire_hilt(x=0, y=0, name="ThornspireHiltGame", p="TS_"):
    """Traced from the middle sword of References/Swords/roblox unique swords.png (straightened 2.6 degrees;
    trace_ref.py): blade root row 600, tip row 40 (80 cm), grip rows 609-797."""
    W = FICTIONAL["Thornspire"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    bmp = BladeMap(BLADES[W["blade"]], bo)
    k = 80.0 / 560 / 20
    T, X, Z, pts, solid, rows = _traced("thornspire", k)
    T = dict(T, grip_row=703)
    X = lambda px: (px - T["axis"]) * k
    Z = lambda py: (py - 703) * k
    pts = lambda q: [(X(px), Z(py)) for px, py in clean(q["pts"])]
    R = T["regions"]
    gw = rows("grip_w")
    band_rows = {r for a, b in T["bands"] for r in range(a - 1, b + 2)}
    # grip: round, navy in the reference (the tier's wrap colour here); the bands are their own parts
    secs = _sections({r: v for r, v in gw.items() if r >= 609}, X, Z, k, 1.0, tol=1.0)
    stack(p + "Grip", [(z, a * 0.97, b * 0.97, c) for z, a, b, c in secs], seg=14)
    bands = []
    for a, b in T["bands"]:
        l, r = max((gw[q] for q in range(a, b) if q in gw), key=lambda v: v[1] - v[0])
        hw = (r - l + 1) / 2 * k + 0.004
        c = X((l + r + 1) / 2)
        z0, z1 = Z(a), Z(b)
        bands.append(stack("_band", [(z0, hw * 0.92, hw * 0.92, c), (z0 + 0.008, hw, hw, c), (z1 - 0.008, hw, hw, c),
                                     (z1, hw * 0.92, hw * 0.92, c)], seg=14))
    join(p + "Bands", bands)
    # guard: the crescent, horns down toward the hand, thick in the middle and thinning to the horns
    q = max(solid(R["crescent"]), key=lambda q: q["area"])
    slab(p + "Guard", pts(q), 0.13, te=0.35, dr=0.05, taper=lambda x_, z_: 1 - 0.45 * min(1.0, abs(x_) / 0.62) ** 2)
    # pommel: flared collar, neck and round disc
    pw = rows("pommel_w")
    ps = _sections({r: v for r, v in pw.items() if r >= 797}, X, Z, k, 1.0, tol=0.6)
    stack(p + "Pommel", [(Z(797) - 0.03, ps[0][1] * 0.95, ps[0][1] * 0.95, ps[0][3])] + ps[:-1] + [(Z(max(pw) + 1), 0, 0, ps[-1][3])], seg=16)
    back = Z(max(pw) + 1)
    # the markings painted on the blade (kept dark), traced: the slot below the tip and the dark marks; w is off the
    # traced blade's centre column (cb), and paint_sym lays them about the game blade's own middle, one half reflected
    t_cm = 80.0 / 560
    uw = lambda q: [((600 - py) / 560, (px - T["cb"]) * t_cm) for px, py in clean(q["pts"])]
    marks = [uw(q) for q in R["marks"] if not q["hole"] and q["area"] >= 7] + [uw(q) for q in R["slot"]]
    paint_sym(p + "Marks", bmp, marks, h=0.8)
    for part in ("Guard", "Grip", "Pommel", "Bands"):
        mirror_halves(bpy.data.objects[p + part])
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(back, 4)), ["Bands", "Marks"]


def build_crescentfang_hilt(x=0, y=0, name="CrescentFangHiltGame", p="CF_"):
    W = FICTIONAL["CrescentFang"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    base = lambda z: 0.93 + 0.07 * (1 - (2 * z / L) ** 2)
    wrap_grip(p + "Grip", g0, g1, 0.062, 0.05, base, pitch=0.05, amp=0.07, tilt=0.02, seg=14, tuck=0.03)
    # guard: a crescent moon round the blade root, its horns reaching up the blade, on a ferrule
    # outer circle centre (0,-0.66) r 0.30, inner (0,-0.74) r 0.27: they cross at the horns (+-0.292, -0.593); both
    # arcs run over the hand side (+z), so the thick middle is by the grip and the horns point up the blade
    ah = math.atan2(-0.593 + 0.66, 0.292)
    outer = [(0.30 * math.cos(a), -0.66 + 0.30 * math.sin(a)) for a in [ah + (math.pi - 2 * ah) * i / 28 for i in range(29)]]
    i0, i1 = math.atan2(-0.593 + 0.74, -0.292), math.atan2(-0.593 + 0.74, 0.292)
    inner = [(0.27 * math.cos(a), -0.74 + 0.27 * math.sin(a)) for a in [i0 + (i1 - i0) * i / 24 for i in range(1, 24)]]
    crescent = slab("_crescent", outer + inner, 0.085, te=0.4, dr=0.03,
                    taper=lambda x, z: 1 - 0.4 * min(1.0, abs(x) / 0.3) ** 2)
    crescent.name = crescent.data.name = p + "Guard"
    # moonstone boss on the crescent's middle, both faces (kept pale)
    disc(p + "Gem", -0.41, [(0, -0.056), (0.045, -0.054), (0.075, -0.045), (0.085, -0.03), (0.085, 0.03), (0.075, 0.045),
                             (0.045, 0.054), (0, 0.056)], seg=20)
    # pommel: a collar and a fang curling toward the edge side
    collar = block("_collar", g1 - 0.01, g1 + 0.05, 0.072, 0.058, 0.075, 0.06, chamfer=0.006)
    fang = spline([(0, 0, g1 + 0.042), (0, 0, g1 + 0.12), (-0.03, 0, g1 + 0.22), (-0.1, 0, g1 + 0.3), (-0.19, 0, g1 + 0.33)],
                  per=5)
    tip = tube("_fang", fang, lambda u: 0.062 * (1 - u ** 1.3) + 0.002, seg=12, ry=0.8)
    join(p + "Pommel", [collar, tip])
    back = max(v.co.z for v in bpy.data.objects[p + "Pommel"].data.vertices)
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(back, 4)), ["Gem"]


def build_shardblade_hilt(x=0, y=0, name="ShardBladeHiltGame", p="SB_"):
    W = FICTIONAL["ShardBlade"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    # grip: six-sided, waisted, with two raised hex bands
    zs = grip_stations(g0 - 0.02, g1 + 0.02, [-0.15, -0.13, -0.11, 0.11, 0.13, 0.15], step=0.08)
    sc = riser_scale(lambda z: 0.94 + 0.06 * (2 * z / L) ** 2, (-0.13, 0.13), h=0.12, w=0.025)
    stack(p + "Grip", [(z, 0.07 * sc(z), 0.06 * sc(z)) for z in zs], seg=6)
    # guard: a faceted block and two crystal arms angled up the blade (six-sided, pointed)
    blk = stack("_block", [(-bo, 0.12, 0.07), (-bo + 0.03, 0.14, 0.075), (g0 + 0.01, 0.11, 0.07)], seg=6)
    parts = [blk]
    for s, ang, ln, r in ((1, 30, 0.44, 0.066), (-1, 36, 0.4, 0.062)):
        d = Vector((s * math.cos(math.radians(ang)), 0, -math.sin(math.radians(ang))))
        a = Vector((s * 0.08, 0, -bo + 0.04))
        path = [a + d * (ln * i / 6) for i in range(7)]
        parts.append(tube("_arm%d" % s, path, lambda u: r * (1 if u < 0.62 else max(0.0, (1 - u) / 0.38)), seg=6))
    join(p + "Guard", parts)
    # loose crystals growing from the block (kept glassy)
    shards = []
    for s, ang, ln, off, r in ((1, 62, 0.3, 0.045, 0.042), (-1, 70, 0.26, 0.04, 0.04), (1, 14, 0.24, -0.02, 0.036),
                               (-1, 18, 0.25, -0.045, 0.036), (1, 48, 0.2, -0.055, 0.03), (-1, 52, 0.22, 0.0, 0.032)):
        d = Vector((s * math.cos(math.radians(ang)), 0, -math.sin(math.radians(ang))))
        a = Vector((s * 0.05, off, -bo + 0.06))
        path = [a + d * (ln * i / 5) for i in range(6)]
        shards.append(tube("_shard", path, lambda u, r=r: r * (1 if u < 0.6 else max(0.0, (1 - u) / 0.4)), seg=6))
    join(p + "Crystal", shards)
    # pommel: a collar and a six-sided double-pointed crystal
    collar = stack("_collar", [(g1 - 0.01, 0.08, 0.068), (g1 + 0.04, 0.085, 0.072)], seg=6)
    c0 = g1 + 0.03
    gem = stack("_gem", [(c0, 0.05, 0.045), (c0 + 0.07, 0.1, 0.085), (c0 + 0.16, 0.1, 0.085), (c0 + 0.3, 0.0, 0.0)], seg=6)
    join(p + "Pommel", [collar, gem])
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(c0 + 0.3, 4)), ["Crystal"]


def build_moonbite_hilt(x=0, y=0, name="MoonbiteHiltGame", p="MB_"):
    W = FICTIONAL["Moonbite"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    bmp = BladeMap(BLADES[W["blade"]], bo)
    base = lambda z: 0.92 + 0.08 * (1 - (2 * z / L) ** 2)
    wrap_grip(p + "Grip", g0, g1, 0.066, 0.054, base, pitch=0.065, amp=0.08, tilt=0.03, seg=14, tuck=0.03)
    # guard: an oval collar with two tusks curving up beside the blade, like a bite
    blk = block("_block", -bo, g0 + 0.02, 0.17, 0.07, 0.1, 0.065, chamfer=0.01)
    parts = [blk]
    for s in (-1, 1):
        path = spline([(s * 0.1, 0, -bo + 0.03), (s * 0.21, 0, -bo - 0.0), (s * 0.29, 0, -bo - 0.07),
                       (s * 0.31, 0, -bo - 0.17), (s * 0.27, 0, -bo - 0.25)], per=5)
        parts.append(tube("_tusk%d" % s, path, lambda u: 0.048 * (1 - u ** 1.4) + 0.002, seg=10))
    join(p + "Guard", parts)
    # pommel: a collar and a full-moon disc with a raised rim
    collar = block("_collar", g1 - 0.01, g1 + 0.05, 0.072, 0.06, 0.08, 0.062, chamfer=0.006)
    R, zc = 0.13, g1 + 0.05 + 0.13 - 0.02
    moon = disc("_moon", zc, [(0, -0.03), (0.1, -0.03), (0.11, -0.042), (0.125, -0.045), (R, -0.035), (R, 0.035),
                               (0.125, 0.045), (0.11, 0.042), (0.1, 0.03), (0, 0.03)], seg=28)
    join(p + "Pommel", [collar, moon])
    # pale inlays (kept): the moon's faces and three moon phases along the blade's back
    inl = [disc("_face", zc, [(0, -0.034), (0.095, -0.034), (0.095, 0.034), (0, 0.034)], seg=24)]
    w0 = -1.2
    phases = []
    R_ = 1.1
    for u0, kind in ((0.46, "crescent"), (0.58, "half"), (0.70, "full")):
        L_ = bmp.b["length"]
        du = R_ / L_
        path = [(u0 - du + 2 * du * i / 10, w0) for i in range(11)]
        circ = lambda s: R_ * math.sqrt(max(0.0, 1 - (2 * s - 1) ** 2))
        if kind == "full":
            phases.append((path, circ, circ, 4))
        elif kind == "half":
            phases.append((path, circ, const(0.0), 3))
        else:
            phases.append((path, lambda s, c=circ: c(s), lambda s, c=circ: -0.55 * c(s), 3))
    inl.append(paint("_phases", bmp, phases))
    join(p + "Moon", inl)
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(zc + R, 4)), ["Moon"]


def build_serpent_hilt(x=0, y=0, name="SerpentHiltGame", p="SP_"):
    W = FICTIONAL["Serpent"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    # grip: scaled, close raised rings
    base = lambda z: 0.94 + 0.06 * (1 - (2 * z / L) ** 2)
    wrap_grip(p + "Grip", g0, g1, 0.064, 0.054, base, pitch=0.04, amp=0.09, tilt=0.0, seg=14, tuck=0.03)
    # guard: a block and two serpentine quillons in an S, one rising up the spine side, one curling back
    # toward the hand on the edge side, each ending in a small snake's head
    blk = block("_block", -bo, g0 + 0.02, 0.1, 0.066, 0.085, 0.062, chamfer=0.008)
    up = spline([(0.06, 0, -bo + 0.04), (0.17, 0, -bo + 0.0), (0.27, 0, -bo - 0.09), (0.29, 0, -bo - 0.2),
                 (0.24, 0, -bo - 0.28)], per=5)
    down = spline([(-0.06, 0, -bo + 0.06), (-0.17, 0, -bo + 0.1), (-0.27, 0, -bo + 0.19), (-0.29, 0, -bo + 0.3),
                   (-0.24, 0, -bo + 0.38)], per=5)
    parts = [blk]
    for path in (up, down):
        parts.append(tube("_coil", path, lambda u: 0.036 - 0.01 * u, seg=10))
        d = (path[-1] - path[-2]).normalized()
        c = path[-1] + d * 0.035
        head = ball("_head", c, 0.042, 0.032, 0.042, seg=12, lat=6)
        parts.append(head)
    join(p + "Guard", parts)
    # pommel: a snake's head along the grip, green eyes on its flats (kept)
    pr = [(g1 - 0.01, 0.07, 0.06), (g1 + 0.05, 0.08, 0.066), (g1 + 0.12, 0.09, 0.07), (g1 + 0.19, 0.076, 0.06),
          (g1 + 0.25, 0.05, 0.042), (g1 + 0.28, 0.0, 0.0)]
    stack(p + "Pommel", pr, seg=16)
    eyes = [ball("_eye", (s * 0.035, t * 0.064, g1 + 0.16), 0.016, 0.012, 0.02, seg=10, lat=5) for s in (1,) for t in (-1, 1)]
    join(p + "Gem", eyes)
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(g1 + 0.28, 4)), ["Gem"]


def build_leviathan_hilt(x=0, y=0, name="LeviathanHiltGame", p="LV_"):
    W = FICTIONAL["Leviathan"]
    L, bo = W["grip"], W["blade_offset"]
    root = station(name, x, y)
    g0, g1 = -L / 2, L / 2
    risers = (-0.3, 0.0, 0.3)
    sc = riser_scale(lambda z: 0.9 + 0.1 * (1 - (2 * z / L) ** 2), risers, h=0.1)
    loft(p + "Grip", [zring(oval(0.085 * sc(z), 0.068 * sc(z), 2.3, 16), z)
                      for z in grip_stations(g0 - 0.015, g1 + 0.015,
                                             [r + d for r in risers for d in (-0.022, -0.0132, 0.0132, 0.022)], step=0.1)])
    # guard: a heavy block and a webbed fin on each side, swept back toward the hand
    blk = block("_block", -bo, g0 + 0.01, 0.22, 0.085, 0.16, 0.08, chamfer=0.012)
    parts = [blk]
    for s in (-1, 1):
        web = [(s * 0.18, -0.69), (s * 0.3, -0.76), (s * 0.4, -0.75), (s * 0.47, -0.69), (s * 0.5, -0.6),
               (s * 0.47, -0.5), (s * 0.43, -0.42), (s * 0.34, -0.47), (s * 0.24, -0.53), (s * 0.18, -0.58)]
        parts.append(slab("_web", web if s > 0 else web[::-1], 0.036, te=0.5, dr=0.02))
        for tip, z0 in (((0.42, -0.77), -0.645), ((0.52, -0.6), -0.62), ((0.45, -0.38), -0.595)):
            path = [Vector((s * 0.15, 0, z0)), Vector((s * (0.15 + tip[0]) / 2, 0, (z0 + tip[1]) / 2 - 0.01)),
                    Vector((s * tip[0], 0, tip[1]))]
            parts.append(tube("_spine", spline([tuple(v) for v in path], per=4), lambda u: 0.024 * (1 - u) + 0.004, seg=8))
    join(p + "Guard", parts)
    # a sea-green orb set in both faces of the block (kept)
    ball(p + "Gem", (0, 0, -0.625), 0.05, 0.092, 0.05, seg=16, lat=8)
    # pommel: a collar and a fish tail
    collar = block("_collar", g1 - 0.01, g1 + 0.06, 0.09, 0.072, 0.075, 0.062, chamfer=0.006)
    tail = slab("_tail", [(0.0, g1 + 0.04), (0.08, g1 + 0.07), (0.17, g1 + 0.15), (0.22, g1 + 0.26), (0.13, g1 + 0.22),
                          (0.05, g1 + 0.17), (0.0, g1 + 0.2), (-0.05, g1 + 0.17), (-0.13, g1 + 0.22), (-0.22, g1 + 0.26),
                          (-0.17, g1 + 0.15), (-0.08, g1 + 0.07)][::-1], 0.075, te=0.45, dr=0.03,
                taper=lambda x, z: 1 - 0.5 * min(1.0, abs(x) / 0.22))
    join(p + "Pommel", [collar, tail])
    return root, dict(GripLength=L, BladeOffset=bo, Back=round(g1 + 0.26, 4)), ["Gem"]


FICTIONAL_BUILDERS = dict(CrescentFang=build_crescentfang_hilt, ShardBlade=build_shardblade_hilt,
                          Moonbite=build_moonbite_hilt, Serpent=build_serpent_hilt, Leviathan=build_leviathan_hilt,
                          Thornspire=build_thornspire_hilt, Seraph=build_seraph_hilt)


def build_fictional_hilts(spacing=1.9, x0=0.0, kinds=None, blades=True):
    """The given kinds (default all) side by side along X, each with its real refined blade as a review prop.
    Returns {kind: (root, numbers, kept part names)}."""
    out = {}
    for i, k in enumerate(kinds or FICTIONAL_BUILDERS):
        root, nums, keep = FICTIONAL_BUILDERS[k](x=x0 + i * spacing)
        if blades:
            real_blade(root, BladeMap(BLADES[FICTIONAL[k]["blade"]], FICTIONAL[k]["blade_offset"]), k + "PreviewBlade")
        out[k] = (root, nums, keep)
    return out

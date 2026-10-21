# Low-poly redesign of the player plot's buildings and bamboo for Create Swords! (Allen 2026-10-20:
# "re-design our building in blender, keeping a low-poly style. also the bamboo").
# Reuses the helpers and palette in Models/Stations/build_stations.py:
#   ns = {"__name__": "lib"}; exec(build_stations.py, ns); exec(build_buildings.py, ns); ns["build_all"]()
# Same footprints, openings and heights as the Studio buildings, so floors, stations, lanterns and paths
# still fit. Blender X = Roblox X, Blender Y = -Roblox Z (fronts face -Y), z = 0 is the plot pad (floors 0.2).
#   Storefront: x -45..-20, y -16..22; open shop front (two lattice bays + a 12-stud entrance) on y = -16,
#               east side open from y -16 to 4 onto the courtyard; gable roof, ridge along Y.
#   Pavilion:   x -19..31, y 4..32; walls on the back (y 32) and west (x -19), front and east open; gable
#               roof, ridge along X; tie beams and king posts at x -5 and 13.
import math
import bmesh
from mathutils import Vector

DETAIL = "low"          # flat, chunky low-poly look (no auto bevels), overriding the stations' mid-high
PAL.update({
    "plaster": (0.95, 0.90, 0.80),
    "timber": (0.40, 0.24, 0.15),
    "timber_dk": (0.27, 0.17, 0.12),
    "stone": (0.58, 0.58, 0.60),
    "stone_dk": (0.45, 0.46, 0.49),
    "flag": (0.72, 0.70, 0.66),
    "flag_dk": (0.62, 0.60, 0.57),
    "roof": (0.33, 0.39, 0.48),
    "roof_dk": (0.25, 0.30, 0.38),
    "bamboo": (0.48, 0.70, 0.30),
    "bamboo_lt": (0.62, 0.80, 0.36),
    "bamboo_dk": (0.33, 0.52, 0.22),
    "leaf": (0.36, 0.62, 0.26),
    "leaf_lt": (0.52, 0.74, 0.30),
})
EAVE = 11.0             # top of the walls / underside of the eaves
FLOOR = 0.2
# colour roles for the shared wall helpers; the feudal shop passes a brighter map
OLD = dict(sill="stone_dk", boards="timber_dk", band="timber", plaster="plaster", post="timber", foot="stone",
           bar="timber_dk", lintel="timber", step="stone")


def prism(name, pts, depth, loc, color, axis="y", rot=(0, 0, 0)):
    """Closed prism from a convex 2D outline pts [(u, v)] extruded `depth` along `axis` (centred). For
    axis y the outline is in XZ; for axis x it is in YZ. loc offsets it."""
    bm = bmesh.new()
    def v3(u, v, d):
        return (d, u, v) if axis == "x" else (u, d, v)
    a = [bm.verts.new(v3(u, v, -depth / 2)) for u, v in pts]
    b = [bm.verts.new(v3(u, v, depth / 2)) for u, v in pts]
    bm.faces.new(a[::-1]); bm.faces.new(b)
    n = len(pts)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((a[i], a[j], b[j], b[i]))
    bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 4])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return _finish(name, bm, color, loc, rot, 0)


def post(name, x, y, h=EAVE + 0.8, w=1.1, C=OLD):
    """Timber post on a chunky stone footing."""
    frustum(name + "Foot", w + 0.9, w + 0.9, w + 0.5, w + 0.5, 0.6, at(x, y, 0), C["foot"])
    box(name, w, w, h - 0.56, at(x, y, 0.56), C["post"])   # 0.04 into the footing: no shared faces


def wall(name, a, b, fixed, along="x", top=EAVE, t=0.5, C=OLD):
    """Wall panel between two posts: stone sill, dark board wainscot, plaster, a mid tie band (inside and
    out), along X (y = fixed) or along Y (x = fixed). a..b are the clear span between post faces."""
    L, c = b - a + 0.2, (a + b) / 2   # 0.1 into each post, so no faces are shared with them
    if along == "x":
        def put(n, h, z, col, thick, off=0.0, trim=0.1):   # trim layers end 0.05 short of the plaster's ends
            box(n, L if off == 0 else L - trim, thick, h, at(c, fixed + off, z), col)
        sides = (-1, 1)
        for s in sides:
            put(name + "Sill", 0.5, FLOOR, C["sill"], 0.3, s * (t / 2 + 0.1))
            put(name + "Boards", 2.54, FLOOR + 0.46, C["boards"], 0.2, s * (t / 2 + 0.06), trim=0.14)
            put(name + "Band", 0.5, 7.0, C["band"], 0.2, s * (t / 2 + 0.06))
        put(name, top - FLOOR + 0.01, FLOOR + 0.04, C["plaster"], t)
    else:
        def put(n, h, z, col, thick, off=0.0, trim=0.1):
            box(n, thick, L if off == 0 else L - trim, h, at(fixed + off, c, z), col)
        for s in (-1, 1):
            put(name + "Sill", 0.5, FLOOR, C["sill"], 0.3, s * (t / 2 + 0.1))
            put(name + "Boards", 2.54, FLOOR + 0.46, C["boards"], 0.2, s * (t / 2 + 0.06), trim=0.14)
            put(name + "Band", 0.5, 7.0, C["band"], 0.2, s * (t / 2 + 0.06))
        put(name, top - FLOOR + 0.01, FLOOR + 0.04, C["plaster"], t)


def lattice_bay(name, x0, x1, y, top=EAVE, C=OLD):
    """Shop-front bay: low board wall, sill, vertical lattice bars, lintel and plaster transom (along X)."""
    L, c = x1 - x0 + 0.2, (x0 + x1) / 2
    box(name + "Low", L, 0.5, 2.8, at(c, y, FLOOR), C["boards"])
    box(name + "Sill", L + 0.2, 0.8, 0.25, at(c, y, 3.0), C["lintel"])
    n = max(3, int(L / 0.9))
    for i in range(1, n):
        box(name + "Bar", 0.18, 0.18, 4.9, at(x0 + L * i / n, y, 3.25), C["bar"])
    box(name + "Rail", L, 0.22, 0.18, at(c, y, 5.6), C["bar"])
    box(name + "Lintel", L + 0.1, 0.6, 0.45, at(c, y, 8.15), C["lintel"])
    box(name + "Transom", L, 0.5, top - 8.56 + 0.05, at(c, y, 8.56), C["plaster"])


def gable_roof(name, ridge_axis, c, half, overhang, lo, hi, eave, pitch_deg, rib=1.7, t=0.6):
    """Gable roof: two thick slope slabs, tile ribs running down each slope in two tones, round eave tiles,
    a chunky ridge with flared end blocks, and fascia boards. ridge_axis 'y': ridge at x = c, slopes fall
    to x = c +- (half + overhang), roof spans y lo..hi. 'x': ridge at y = c, spans x lo..hi."""
    p = math.radians(pitch_deg)
    run = half + overhang
    slope_len = run / math.cos(p)
    rise = run * math.tan(p)
    length = hi - lo
    mid_l = (lo + hi) / 2
    for side in (-1, 1):
        # slab: box local X runs up the slope; rotate about the ridge axis so it rises toward the ridge
        if ridge_axis == "y":
            ang = (0, pitch_deg if side > 0 else -pitch_deg, 0)
            mid = Vector((c + side * run / 2, mid_l, eave + rise / 2))
            normal = Vector((side * math.sin(p), 0, math.cos(p)))
            box(f"{name}Slope", slope_len, length, t, mid, "roof_dk", rot=ang)
            k = 0
            u = lo + rib / 2
            while u < hi:
                box(f"{name}Rib", slope_len, rib * 0.55, 0.32, Vector((mid.x, u, mid.z)) + normal * t, "roof" if k % 2 else "roof_dk", rot=ang)
                cyl(f"{name}EaveTile", 0.32, 0.5, Vector((c + side * (run + 0.05), u, eave + t * 0.4)), "roof", sides=6, rot=(0, 90, 0))
                u += rib
                k += 1
            box(f"{name}Fascia", 0.35, length + 0.4, 0.7, at(c + side * (run + 0.1), mid_l, eave - 0.45), "timber_dk")
            for e in (lo - 0.15, hi + 0.15):                 # barge boards along the rake edges
                box(f"{name}Barge", slope_len, 0.35, t + 0.4, Vector((mid.x, e, mid.z - 0.1)), "timber_dk", rot=ang)
        else:
            ang = (-pitch_deg if side > 0 else pitch_deg, 0, 0)
            mid = Vector((mid_l, c + side * run / 2, eave + rise / 2))
            normal = Vector((0, side * math.sin(p), math.cos(p)))
            box(f"{name}Slope", length, slope_len, t, mid, "roof_dk", rot=ang)
            k = 0
            u = lo + rib / 2
            while u < hi:
                box(f"{name}Rib", rib * 0.55, slope_len, 0.32, Vector((u, mid.y, mid.z)) + normal * t, "roof" if k % 2 else "roof_dk", rot=ang)
                cyl(f"{name}EaveTile", 0.32, 0.5, Vector((u, c + side * (run + 0.05), eave + t * 0.4)), "roof", sides=6, rot=(90, 0, 0))
                u += rib
                k += 1
            box(f"{name}Fascia", length + 0.4, 0.35, 0.7, at(mid_l, c + side * (run + 0.1), eave - 0.45), "timber_dk")
            for e in (lo - 0.15, hi + 0.15):                 # barge boards along the rake edges
                box(f"{name}Barge", 0.35, slope_len, t + 0.4, Vector((e, mid.y, mid.z - 0.1)), "timber_dk", rot=ang)
    top = eave + rise + t
    if ridge_axis == "y":
        box(f"{name}Ridge", 1.6, length + 0.6, 1.1, at(c, mid_l, top - 0.5), "stone_dk")
        box(f"{name}RidgeCap", 1.0, length + 0.8, 0.4, at(c, mid_l, top + 0.6), "roof_dk")
        for e in (lo - 0.2, hi + 0.2):
            frustum(f"{name}RidgeEnd", 1.8, 1.0, 2.4, 1.0, 2.0, at(c, e, top - 0.6), "stone_dk")
    else:
        box(f"{name}Ridge", length + 0.6, 1.6, 1.1, at(mid_l, c, top - 0.5), "stone_dk")
        box(f"{name}RidgeCap", length + 0.8, 1.0, 0.4, at(mid_l, c, top + 0.6), "roof_dk")
        for e in (lo - 0.2, hi + 0.2):
            frustum(f"{name}RidgeEnd", 1.0, 1.8, 1.0, 2.4, 2.0, at(e, c, top - 0.6), "stone_dk")
    return rise


def gable_end(name, ridge_axis, c, half, at_coord, eave, overhang, pitch_deg, t=0.5):
    """Plaster gable from the wall top (EAVE) up to the underside of the roof slabs, with a lattice vent."""
    p = math.radians(pitch_deg)
    h1 = (eave - EAVE) + overhang * math.tan(p)          # roof underside height above EAVE at the wall line
    apex = h1 + half * math.tan(p)
    pts = [(-half, 0), (half, 0), (half, h1 - 0.35), (0, apex - 0.35), (-half, h1 - 0.35)]   # starts 0.3 into the
    if ridge_axis == "y":                                                                    # beam, stops 0.05 under the roof
        prism(name, pts, t, Vector((c, at_coord, EAVE + 0.3)), "plaster", axis="y")
        box(name + "Vent", 2.4, t + 0.12, 1.2, Vector((c, at_coord, EAVE + h1 + (apex - h1) * 0.25)), "timber_dk")
    else:
        prism(name, pts, t, Vector((at_coord, c, EAVE + 0.3)), "plaster", axis="x")
        box(name + "Vent", t + 0.12, 2.4, 1.2, Vector((at_coord, c, EAVE + h1 + (apex - h1) * 0.25)), "timber_dk")


def door_bay(name, a, b, x, door=5.0, top=EAVE, C=OLD):
    """Wall along Y between posts with a centred doorway: wall stubs either side, lintel and plaster above."""
    c = (a + b) / 2
    wall(name + "L", a, c - door / 2, x, along="y", top=top, C=C)
    wall(name + "R", c + door / 2, b, x, along="y", top=top, C=C)
    box(name + "Lintel", 0.6, door + 0.4, 0.45, at(x, c, 8.15), C["lintel"])
    box(name + "Transom", 0.46, door + 0.2, top - 8.56 + 0.03, at(x, c, 8.56), C["plaster"])   # top 0.02 under the stubs   # thinner than the stubs: no shared faces
    box(name + "Step", 1.6, door, 0.23, at(x, c, FLOOR - 0.05), C["step"])


def screen(name, a, b, y, h=3.6):
    """Low lattice screen along X between two posts: bottom and top rails, vertical slats with gaps."""
    L, c = b - a + 0.2, (a + b) / 2
    box(name + "Base", L, 0.5, 0.4, at(c, y, FLOOR - 0.04), "stone_dk")
    box(name + "RailLow", L - 0.1, 0.3, 0.29, at(c, y, FLOOR + 0.32), "timber")   # 0.04 into the base
    box(name + "RailTop", L - 0.1, 0.36, 0.3, at(c, y, FLOOR + h - 0.3), "timber")
    n = int(L / 0.55)
    for i in range(n):
        box(name + "Slat", 0.3, 0.12, h - 0.66, at(a + (i + 0.5) * L / n - 0.1, y, FLOOR + 0.6), "timber_dk")


def paving(name, xa, xb, ya, yb, flag=3.0, gap=0.12):
    """Stone-flag courtyard: a grout bed with two-tone flags on top (tops at the 0.2 floor height)."""
    import random
    rnd = random.Random(5)
    box(name + "Bed", xb - xa, yb - ya, 0.2, at((xa + xb) / 2, (ya + yb) / 2, -0.05), "stone_dk")
    y = ya
    row = 0
    while y < yb - 0.5:
        h = min(flag, yb - y)
        x = xa + (flag / 2 if row % 2 else 0)   # running bond: every other row shifted half a flag
        if row % 2:
            box(name + "Flag", flag / 2 - gap, h - gap, 0.17, at(xa + flag / 4, y + h / 2, 0.03), "flag")
        while x < xb - 0.5:
            w = min(flag, xb - x)
            box(name + "Flag", w - gap, h - gap, 0.17, at(x + w / 2, y + h / 2, 0.03), ("flag", "flag_dk")[rnd.random() < 0.35])
            x += flag
        y += flag
        row += 1


# ---------------------------------------------------------------- buildings

def make_shop(name, x0, x1, y0, y1, entrance, door_segment=1, P=1.1):
    """A shop in the low-poly style: posts on stone footings, plaster and timber walls, an open front with a
    centred entrance between two lattice bays and a signboard, a side door onto the courtyard on the east wall
    (in side bay `door_segment`, counted from the front), tie beams, and a gable roof with its ridge toward
    the street. Roof and gables are named Roof*/Gable* so join_by_material keeps them as separate parts the
    game can hide while a player is inside."""
    station(name, 0, 0)
    c = (x0 + x1) / 2
    ex0, ex1 = c - entrance / 2, c + entrance / 2
    n_side = max(2, math.ceil((y1 - y0) / 10.0))
    side_y = [y0 + (y1 - y0) * k / n_side for k in range(n_side + 1)]
    n_back = max(2, math.ceil((x1 - x0) / 13.0))
    back_x = [x0 + (x1 - x0) * k / n_back for k in range(n_back + 1)]
    posts = {(x0, y0), (ex0, y0), (ex1, y0), (x1, y0)}
    posts |= {(x0, y) for y in side_y} | {(x1, y) for y in side_y} | {(x, y1) for x in back_x}
    for i, (x, y) in enumerate(sorted(posts)):
        post(f"Post{i}", x, y, w=P)
    for k in range(n_side):
        a, b = side_y[k] + P / 2, side_y[k + 1] - P / 2
        wall("WallW", a, b, x0, along="y")
        if k == door_segment:
            door_bay("DoorE", a, b, x1, door=min(5.0, b - a - 2.0))   # side door onto the courtyard
        else:
            wall("WallE", a, b, x1, along="y")
    for k in range(n_back):
        wall("WallBack", back_x[k] + P / 2, back_x[k + 1] - P / 2, y1, along="x")
    lattice_bay("BayW", x0 + P / 2, ex0 - P / 2, y0)
    lattice_bay("BayE", ex1 + P / 2, x1 - P / 2, y0)
    box("EntranceBeam", entrance - P, 0.7, 0.8, at(c, y0, EAVE - 0.8), "timber")
    sign_w = min(6.0, entrance * 0.8)
    box("Signboard", sign_w, 0.3, 1.3, at(c, y0 - 0.5, EAVE + 0.5), "timber_dk")
    box("SignFace", sign_w - 0.6, 0.1, 0.95, at(c, y0 - 0.7, EAVE + 0.68), "paper")
    w, d = x1 - x0, y1 - y0
    box("BeamFront", w + 1.3, 1.2, 1.2, at(c, y0, EAVE), "timber")
    box("BeamBack", w + 1.3, 1.2, 1.2, at(c, y1, EAVE), "timber")
    box("BeamW", 1.16, d + 0.6, 1.16, at(x0, (y0 + y1) / 2, EAVE + 0.02), "timber")
    box("BeamE", 1.16, d + 0.6, 1.16, at(x1, (y0 + y1) / 2, EAVE + 0.02), "timber")
    for y in side_y[1:-1]:
        box("TieBeam", w - 1.0, 0.9, 0.9, at(c, y, EAVE + 0.1), "timber")
    half = w / 2
    gable_roof("Roof", "y", c, half, 2.6, y0 - 2.4, y1 + 2.4, EAVE + 1.2, 28)
    for yy in (y0, y1):
        gable_end("Gable", "y", c, half - 0.6, yy, EAVE + 1.2, 2.6 + 0.6, 28)


# Allen 2026-10-20: both shops wider. Same street front (Blender y -16 = Roblox z 16), east wall at x -18.
# Allen 2026-10-20: starter about 3x bigger, and the Upgraded Store deeper so it stays a clear step up.
SHOP_UPGRADED = dict(x0=-49.0, x1=-18.0, y0=-16.0, y1=30.0, entrance=12.0, door_segment=1)   # 31 x 46
SHOP_STARTER = dict(x0=-49.0, x1=-18.0, y0=-16.0, y1=16.0, entrance=12.0, door_segment=1)    # 31 x 32


def storefront():
    """The Upgraded Store."""
    make_shop("Storefront", **SHOP_UPGRADED)


def starter_shop():
    """The shop players start with."""
    make_shop("StarterShop", **SHOP_STARTER)


# ---------------------------------------------------------------- feudal shop
# Allen 2026-10-20: "Re-design a stylized Japanese feudal style building for the shop ... less realistic, more
# low polyish ... Colors should be bright." From References/Concept Art/feudal architecture.jfif: irimoya
# (hip-and-gable) roofs with upturned eaves, a pent roof between the storeys and a gabled entrance canopy.
PAL.update({
    "fd_red": (0.90, 0.27, 0.17), "fd_red_dk": (0.68, 0.17, 0.12),
    "fd_wood": (0.97, 0.67, 0.34), "fd_wood_dk": (0.74, 0.42, 0.21),
    "fd_plaster": (1.00, 0.97, 0.90),
    "fd_roof": (0.20, 0.62, 0.88), "fd_roof_lt": (0.38, 0.80, 0.97), "fd_roof_dk": (0.12, 0.42, 0.70),
    "fd_stone": (0.86, 0.84, 0.80), "fd_stone_dk": (0.70, 0.68, 0.65),
})
FD = dict(sill="fd_stone_dk", boards="fd_wood_dk", band="fd_red", plaster="fd_plaster", post="fd_red",
          foot="fd_stone", bar="fd_wood", lintel="fd_red", step="fd_stone")


def _rib(bm, pts, lat, w, h, sink=0.15, out=None):
    """Faceted triangular rib laid along pts (points on a roof surface); lat is its sideways 2D direction. `out`
    pushes the first cap 0.08 past the eave edge and pulls the last one 0.08 back, so neither shares a face
    with the slab's edges."""
    if out is not None:
        pts = [pts[0] + Vector(out) * 0.08] + pts[1:-1] + [pts[-1] - Vector(out) * 0.08]
    L = Vector((lat[0], lat[1], 0)).normalized() * (w / 2)
    dn, up = Vector((0, 0, sink)), Vector((0, 0, h))
    rows = [(bm.verts.new(p - L - dn), bm.verts.new(p + L - dn), bm.verts.new(p + up)) for p in pts]
    for a, b in zip(rows, rows[1:]):
        for i in range(3):
            j = (i + 1) % 3
            bm.faces.new((a[i], a[j], b[j], b[i]))
    bm.faces.new(rows[0]); bm.faces.new(rows[-1][::-1])


def sori_roof(name, cx, cy, R, H, eave, pitch, d1, d_stop=None, lift=0.35, corner=1.8, t=0.6, rib=2.4):
    """Low-poly roof with upturned (sori) eaves and corners, ridge along Y, as one welded slab plus tile ribs,
    hip ridges, ridge and gables. R / H: half-width across / half-length along the ridge, to the eave edge.
    d1 is the hip depth: 0 < d1 < H gives an irimoya (hipped up to d1, then a vertical gable), d1 = 0 a plain
    gable, d1 = R with d_stop < R a pent skirt that stops at d_stop (no ridge). A point's height comes from d,
    its distance in from its own eave, and o, its distance from the crossing eave, so facets meeting at a hip
    agree there. Returns that height function."""
    tp = math.tan(math.radians(pitch))
    dmax = d_stop if d_stop is not None else R
    D = min(5.0, 0.8 * d1) if 0 < d1 < R else min(5.0, 0.7 * dmax)
    Dc = 0.5 * min(R, H)

    def z(d, o):
        return eave + tp * d + max(0.0, 1 - d / D) ** 2 * (lift + corner * max(0.0, 1 - o / Dc) ** 2)

    ds = {round(f * D, 4) for f in (0, 0.12, 0.28, 0.48, 0.72, 1.0)}
    n = max(1, math.ceil((dmax - D) / 4.0))
    ds |= {round(D + (dmax - D) * k / n, 4) for k in range(n + 1)}
    if 0 < d1 < dmax:
        ds.add(round(d1, 4))
    ds = sorted(d for d in ds if d <= dmax + 1e-6)
    F = (-1, -0.82, -0.58, -0.3, 0, 0.3, 0.58, 0.82, 1)
    bm = bmesh.new()
    top, bot = {}, {}

    def V(x, y, zz):
        k = (round(x, 4), round(y, 4), round(zz, 4))
        if k not in top:
            top[k] = bm.verts.new((x, y, zz))
            bot[k] = bm.verts.new((x, y, zz - t))
        return k

    def sheet(grid):
        for r0, r1 in zip(grid, grid[1:]):
            for j in range(len(F) - 1):
                q = list(dict.fromkeys((r0[j], r0[j + 1], r1[j + 1], r1[j])))
                if len(q) >= 3:
                    bm.faces.new([top[k] for k in q])
                    bm.faces.new([bot[k] for k in q[::-1]])

    for s in (-1, 1):   # long facets (eaves along Y)
        sheet([[V(cx + s * (R - d), cy + e * f, z(d, H - abs(e * f))) for f in F]
               for d in ds for e in [H - min(d, d1)]])
        if d1 > 0:      # hipped ends (eaves along X)
            sheet([[V(cx + e * f, cy + s * (H - d), z(d, R - abs(e * f))) for f in F]
                   for d in ds if d <= d1 + 1e-6 for e in [R - d]])
    key_of = {v: k for k, v in top.items()}
    for e in [e for e in bm.edges if len(e.link_faces) == 1 and e.verts[0] in key_of and e.verts[1] in key_of]:
        a, b = e.verts
        bm.faces.new((a, b, bot[key_of[b]], bot[key_of[a]]))
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    _finish(name + "Slab", bm, "fd_roof_dk", at(0, 0, 0), (0, 0, 0), 0, smooth=False)

    # tile ribs (two tones) and hip ridges; ribs follow every other curved row (sunk 0.15, so they stay on the
    # slab) and past D, where the slope is straight, only their last row
    def trim(pts):
        return [p for i, p in enumerate(pts)
                if i == len(pts) - 1 or any(abs(ds[i] - f * D) < 1e-3 for f in (0, 0.28, 0.72, 1.0))]
    ribs = [bmesh.new(), bmesh.new()]
    k = 0
    for s in (-1, 1):
        v = -H + rib / 2
        while v < H:
            pts = [Vector((cx + s * (R - d), cy + v, z(d, H - abs(v)))) for d in ds if abs(v) <= H - min(d, d1) - 0.5]
            if len(pts) > 1:
                _rib(ribs[k % 2], trim(pts), (0, 1), rib * 0.55, 0.4, out=(s, 0, 0))
            v += rib
            k += 1
        if d1 > 0:
            u = -R + rib / 2
            while u < R:
                pts = [Vector((cx + u, cy + s * (H - d), z(d, R - abs(u)))) for d in ds if d <= d1 + 1e-6 and abs(u) <= R - d - 0.5]
                if len(pts) > 1:
                    _rib(ribs[k % 2], trim(pts), (1, 0), rib * 0.55, 0.4, out=(0, s, 0))
                u += rib
                k += 1
            for sv in (-1, 1):   # hip ridges from each corner up to the gable
                pts = [Vector((cx + s * (R - d), cy + sv * (H - d), z(d, d))) for d in ds if d <= min(d1, dmax) + 1e-6]
                _rib(ribs[0], pts, (s, -sv), 1.0, 0.65, sink=0.1, out=(s, sv, 0))
                cyl(name + "HipTip", 0.42, 0.5, pts[0] - Vector((0, 0, 0.2)), "gold", sides=6)
    for bmr, col in zip(ribs, ("fd_roof", "fd_roof_lt")):
        bmesh.ops.recalc_face_normals(bmr, faces=bmr.faces[:])
        _finish(name + "Rib", bmr, col, at(0, 0, 0), (0, 0, 0), 0, smooth=False)

    if d_stop is not None:
        return z
    # ridge with gold end tiles
    half_r = H - d1 if d1 > 0 else H
    zr = z(R, H)
    box(name + "Ridge", 1.5, 2 * half_r + 0.4, 1.3, at(cx, cy, zr - 0.6), "fd_roof_dk")
    box(name + "RidgeCap", 0.9, 2 * half_r + 0.6, 0.45, at(cx, cy, zr + 0.65), "fd_roof_lt")
    for sv in (-1, 1):
        frustum(name + "RidgeEnd", 1.6, 0.8, 2.6, 0.8, 2.3, at(cx, cy + sv * (half_r + 0.2), zr - 0.7), "gold")
    # gables: plaster under the roof's underside, a gold crest, red barge boards
    gu = R - d1 if d1 > 0 else R - 2.0
    for sv in (-1, 1):
        gv = sv * (half_r - (0.4 if d1 > 0 else 0.5))
        # outline points only where the rake curves (past D it is straight; collinear points make slivers)
        us = sorted({-gu, gu, 0.0} | {s * (R - d) for d in ds if d < D and R - d < gu for s in (-1, 1)})
        zb = z(d1, d1) - t - 0.3 if d1 > 0 else eave - t + 0.3
        pts = [(gu, zb)] + [(u, z(R - abs(u), H) - t - 0.05) for u in reversed(us)] + [(-gu, zb)]
        prism(name + "Gable", pts, 0.3, at(cx, cy + gv, 0), "fd_plaster")
        cyl(name + "GableCrest", 0.9, 0.36, at(cx, cy + gv + sv * 0.1, z(R, H) - t - 1.6), "gold", sides=8, rot=(-90 * sv, 0, 0))
        if d1 > 0:
            a = math.atan2(z(R, H) - z(d1, H), R - d1)
            Ln = (R - d1) / math.cos(a)
            for s in (-1, 1):
                th = s * a
                nrm = Vector((math.sin(th), 0, math.cos(th)))
                mid = Vector((cx + s * (R - d1) / 2, cy + sv * (half_r + 0.25), (z(R, H) + z(d1, H)) / 2))
                box(name + "Barge", Ln, 0.4 + 0.06 * (s > 0), 1.0, mid - nrm * 0.8, "fd_red", rot=(0, math.degrees(th), 0))
    return z


def upper_storey(name, x0, x1, y0, y1, zb, top, C=FD, P=1.0, skip_front=None):
    """Set-in upper storey: red posts, plaster panels with shoji windows, a beam ring at `top`. skip_front is an
    x-range on the front wall whose panels get no window (the entrance canopy runs into it)."""
    def marks(a, b):
        n = max(2, math.ceil((b - a) / 8.0))
        return [a + (b - a) * k / n for k in range(n + 1)]
    xs, ys = marks(x0, x1), marks(y0, y1)
    pts = {(x, y0) for x in xs} | {(x, y1) for x in xs} | {(x0, y) for y in ys} | {(x1, y) for y in ys}
    for i, (x, y) in enumerate(sorted(pts)):
        box(f"{name}Post{i}", P - 0.1, P - 0.1, top + 0.6 - zb, at(x, y, zb), C["post"])   # thinner than the beams
    for along, line, fixed in (("x", xs, y0), ("x", xs, y1), ("y", ys, x0), ("y", ys, x1)):
        for a, b in zip(line, line[1:]):
            L, c = b - a - P + 0.2, (a + b) / 2

            def bx(n, u, du, h, zz, col, th):
                if along == "x":
                    box(n, du, th, h, at(c + u, fixed, zz), col)
                else:
                    box(n, th, du, h, at(fixed, c + u, zz), col)
            bx(name + "Wall", 0, L, top + 0.05 - zb, zb, C["plaster"], 0.5)
            if skip_front and along == "x" and fixed == y0 and skip_front[0] < c < skip_front[1]:
                continue
            ww, wh, zc = min(L - 2.4, 4.0), 2.2, top - 2.6
            bx(name + "Shoji", 0, ww, wh, zc - wh / 2, "paper", 0.6)
            for u, du, h, zz in ((0, ww + 0.56, 0.3, zc - wh / 2 - 0.3), (0, ww + 0.56, 0.3, zc + wh / 2),
                                 (-ww / 2 - 0.1, 0.3, wh + 0.02, zc - wh / 2 - 0.01), (ww / 2 + 0.1, 0.3, wh + 0.02, zc - wh / 2 - 0.01)):
                bx(name + "WinFrame", u, du, h, zz, C["boards"], 0.76 if du > 0.3 else 0.72)
            for i in range(1, 3):
                bx(name + "WinBar", -ww / 2 + ww * i / 3, 0.14, wh - 0.04, zc - wh / 2 + 0.02, C["boards"], 0.68)
            bx(name + "WinBar", 0, ww - 0.04, 0.14, zc - 0.07, C["boards"], 0.66)
    w, d = x1 - x0, y1 - y0
    box(name + "BeamF", w + P + 0.1, P, P, at((x0 + x1) / 2, y0, top), "fd_red_dk")
    box(name + "BeamB", w + P + 0.1, P, P, at((x0 + x1) / 2, y1, top), "fd_red_dk")
    box(name + "BeamW", P - 0.04, d + P - 0.16, P - 0.04, at(x0, (y0 + y1) / 2, top + 0.02), "fd_red_dk")
    box(name + "BeamE", P - 0.04, d + P - 0.16, P - 0.04, at(x1, (y0 + y1) / 2, top + 0.02), "fd_red_dk")


def feudal_shop(name, x0, x1, y0, y1, entrance, door_segment=1, P=1.1, dx=0.0, storeys=None):
    """Stylized feudal shop with make_shop's footprint and openings (open front with a centred entrance between
    lattice bays, side door onto the courtyard, ground eave at EAVE). With storeys=2 (default: both sides >= 24)
    it gets a set-in upper storey under an irimoya roof, a pent roof skirting the ground floor and a gabled canopy
    over the entrance; with 1, it is one storey under the irimoya roof. Everything above the ground-floor eave is named
    Roof*/Upper*/Canopy*/Beam*/TieBeam so the game can hide it while a player is inside."""
    C = FD
    station(name, dx, 0)
    c, cy = (x0 + x1) / 2, (y0 + y1) / 2
    w, d = x1 - x0, y1 - y0
    ex0, ex1 = c - entrance / 2, c + entrance / 2
    n_side = max(2, math.ceil(d / 10.0))
    side_y = [y0 + d * k / n_side for k in range(n_side + 1)]
    n_back = max(2, math.ceil(w / 13.0))
    back_x = [x0 + w * k / n_back for k in range(n_back + 1)]
    posts = {(x0, y0), (ex0, y0), (ex1, y0), (x1, y0)}
    posts |= {(x0, y) for y in side_y} | {(x1, y) for y in side_y} | {(x, y1) for x in back_x}
    for i, (x, y) in enumerate(sorted(posts)):
        post(f"Post{i}", x, y, w=P, C=C)
    for k in range(n_side):
        a, b = side_y[k] + P / 2, side_y[k + 1] - P / 2
        wall("WallW", a, b, x0, along="y", C=C)
        if k == door_segment:
            door_bay("DoorE", a, b, x1, door=min(5.0, b - a - 2.0), C=C)
        else:
            wall("WallE", a, b, x1, along="y", C=C)
    for k in range(n_back):
        wall("WallBack", back_x[k] + P / 2, back_x[k + 1] - P / 2, y1, along="x", C=C)
    lattice_bay("BayW", x0 + P / 2, ex0 - P / 2, y0, C=C)
    lattice_bay("BayE", ex1 + P / 2, x1 - P / 2, y0, C=C)
    box("EntranceBeam", entrance - P, 0.7, 0.8, at(c, y0, EAVE - 0.8), "fd_red")
    box("BeamFront", w + 1.3, 1.2, 1.2, at(c, y0, EAVE), "fd_red_dk")
    box("BeamBack", w + 1.3, 1.2, 1.2, at(c, y1, EAVE), "fd_red_dk")
    box("BeamW", 1.16, d + 0.6, 1.16, at(x0, cy, EAVE + 0.02), "fd_red_dk")
    box("BeamE", 1.16, d + 0.6, 1.16, at(x1, cy, EAVE + 0.02), "fd_red_dk")
    for y in side_y[1:-1]:
        box("TieBeam", w - 1.0, 0.9, 0.9, at(c, y, EAVE + 0.1), "fd_red_dk")
    beam_top, t = EAVE + 1.2, 0.6

    def eave_for(pitch, ov, top):   # roof underside meets the beam top at the wall line
        return top + t + 0.05 - math.tan(math.radians(pitch)) * ov

    if (storeys or (2 if min(w, d) >= 24 else 1)) == 2:
        inset, ov_p, top2 = 3.5, 3.0, EAVE + 8.5
        ux0, ux1, uy0, uy1 = x0 + inset, x1 - inset, y0 + inset, y1 - inset
        sori_roof("RoofPent", c, cy, w / 2 + ov_p, d / 2 + ov_p, eave_for(24, ov_p, beam_top), 24, d1=w / 2 + ov_p,
                  d_stop=ov_p + inset + 0.1, lift=0.25, corner=1.1, t=t)
        upper_storey("Upper", ux0, ux1, uy0, uy1, beam_top, top2, skip_front=(ex0, ex1))
        ov = 3.5
        R, H = (ux1 - ux0) / 2 + ov, (uy1 - uy0) / 2 + ov
        sori_roof("Roof", c, cy, R, H, eave_for(30, ov, top2 + 1.0), 30, d1=0.45 * R, t=t)
        # gabled canopy over the entrance, running back into the upper storey
        ch0, ch1 = y0 - 3.6, uy0 + 0.3
        sori_roof("Canopy", c, (ch0 + ch1) / 2, entrance / 2 + 1.6, (ch1 - ch0) / 2, EAVE + 0.9, 34, d1=0,
                  lift=0.3, corner=1.4, t=0.5)
        box("CanopySign", 4.9, 0.25, 1.9, at(c, ch0 + 0.15, EAVE + 1.4), "gold")
        box("CanopySignBoard", 4.4, 0.45, 1.4, at(c, ch0 + 0.15, EAVE + 1.65), "fd_wood_dk")
    else:
        ov = 3.0
        R, H = w / 2 + ov, d / 2 + ov
        sori_roof("Roof", c, cy, R, H, eave_for(30, ov, beam_top), 30, d1=min(0.45 * R, 0.6 * H), t=t)
        sign_w = min(6.0, entrance * 0.8)
        box("Signboard", sign_w + 0.5, 0.25, 1.8, at(c, y0 - 0.55, EAVE - 2.4), "gold")
        box("SignBoard", sign_w, 0.45, 1.3, at(c, y0 - 0.55, EAVE - 2.15), "fd_wood_dk")


def feudal_storefront(dx=0.0):
    feudal_shop("FeudalStore", **SHOP_UPGRADED, dx=dx)


def feudal_starter(dx=0.0):
    feudal_shop("FeudalStarter", **SHOP_STARTER, dx=dx, storeys=1)


WALL_AXIS_Z = 4.4                  # height of the sword's axis
WALL_SLOT = (-0.58, -0.56)         # holder-local (x, y) of the grip centre (the game's WallHolder.Mount): blade root at
                                   # x 0 (BladeOffset 0.58), blade +X; 0.56 out keeps the 0.52 guard off the board
WALL_HOOKS = (-0.475, 0.9)         # under the grip, and under the blade inside even a tanto's 1.29


def wall_sword_holder(name="WallSwordHolder", x=0, y=0, rows=1):
    """Horizontal wall rack (katana-kake) in the feudal shop's palette (Allen 2026-10-20: "can you design sword
    holders that attach to the wall", "i was thinking the holder is horizontal", "remove the hood"); rows=3 is
    the 3-sword Wall Sword Rack bought from a tycoon pad. Each sword lies along the wall, broad face out, on two
    padded hooks with front lips: one under the grip, one under the blade 0.9 past the guard, so a tanto sits
    as well as a katana. Rows are 1.0 apart, lowest axis at WALL_AXIS_Z (1 row) or 4.0 (more). Origin = the
    wall's plaster face at floor level; it faces -Y; 5.2 wide, so racks tile 5.2 apart or more. The 0.3-deep
    backboard sits above the wall's 3.2 wainscot."""
    station(name, x, y)
    cx = 1.25                            # board centred on a katana (pommel -0.95 .. tip 3.5)
    zs = [WALL_AXIS_Z] if rows == 1 else [4.0 + k for k in range(rows)]
    lo, hi = zs[0] - 0.75, zs[-1] + 0.75
    box("Board", 5.0, 0.3, hi - lo, at(cx, -0.13, lo), "fd_wood_dk")
    ring("Frame", 5.2, hi - lo + 0.2, 0.16, 0.36, at(cx, 0, (lo + hi) / 2), "fd_red", rot=(90, 0, 0))
    for gx in (cx - 2.45, cx + 2.45):
        for gz in (lo + 0.05, hi - 0.05):
            box("Corner", 0.24, 0.06, 0.24, at(gx, -0.38, gz - 0.12), "gold")   # inside the frame edge
    for za in zs:
        _hooks(0, za)
    return zs


def _hooks(x0, za, py=0.0, brace=True, cap_z=0.35):
    """The two padded hooks under one horizontal sword (axis height za, blade root at x0): one under the grip, one
    under the blade 0.9 along (WALL_HOOKS). Each is an arm standing out toward -Y from the plane y = py, a red pad
    (the sword sits a little further out, at WALL_SLOT), a front lip with a gold cap (cap_z up the arm; under 0.35
    sinks it into the lip) and, on a wall, a brace."""
    for hx, top in zip(WALL_HOOKS, (za - 0.08, za - 0.1)):   # pad tops: grip radius 0.08, blade half-width 0.1
        x, arm = x0 + hx, top - 0.05
        box("HookArm", 0.24, 0.5, 0.2, at(x, py - 0.5, arm - 0.2), "fd_wood")
        box("HookPad", 0.2, 0.36, 0.05, at(x, py - 0.45, arm), "fd_red_dk")
        box("HookLip", 0.22, 0.1, 0.35, at(x, py - 0.7, arm), "fd_wood")
        box("HookCap", 0.26, 0.14, 0.06, at(x, py - 0.7, arm + cap_z), "gold")
        if brace:
            box("HookBrace", 0.14, 0.14, 0.74, at(x, py - 0.26, arm - 0.8), "fd_wood", rot=(36.3, 0, 0))


PAL.setdefault("fd_lacquer", (0.16, 0.13, 0.14))   # black lacquer, as on the reference katana stand
TABLE_TOP = 2.4
TABLE_ROOT = -1.19                   # blade root x: centres a katana (pommel -1.77 - 0.54 .. tip +3.5) on the table
TABLE_STAND_Y = 0.35                 # the stand's hooks stand out from this plane, toward the customer (-Y)
TABLE_TIERS = (2.95, 3.65, 4.35)     # sword axis heights; 0.7 apart so the 0.52 guards clear


def sword_table(name="SwordTable", x=0, y=0):
    """Display table with a katana stand on top (Allen 2026-10-20, reference photo of a sword rack on a counter):
    two black-lacquer uprights on a low base hold 3 swords stacked horizontally, edge up and broad face toward the
    customer (-Y), on the wall rack's padded hooks (under the grip, and 0.9 along the blade so a tanto fits). Grip
    centre of sword i = (TABLE_ROOT - 0.58, TABLE_STAND_Y + WALL_SLOT[1], TABLE_TIERS[i]). Origin = floor under the
    table centre."""
    station(name, x, y)
    th = TABLE_TOP
    box("Top", 5.6, 2.4, 0.25, at(0, 0, th - 0.25), "fd_wood_dk")
    box("Apron", 5.3, 2.1, 0.4, at(0, 0, th - 0.64), "fd_red")
    for lx in (-2.4, 2.4):
        for ly in (-0.8, 0.8):
            box("Leg", 0.36, 0.36, th - 0.62, at(lx, ly, 0.04), "fd_red_dk")
            box("Foot", 0.48, 0.48, 0.12, at(lx, ly, 0), "gold")
    for ly in (-0.8, 0.8):
        box("Stretcher", 4.5, 0.2, 0.2, at(0, ly, 0.6), "fd_red_dk")
    for cx_ in (-2.66, 2.66):
        for cy_ in (-1.06, 1.06):
            box("Corner", 0.24, 0.24, 0.05, at(cx_, cy_, th), "gold")
    # the stand: an upright behind each hook, on a foot, joined by a low base
    py, top = TABLE_STAND_Y, TABLE_TIERS[-1] + 0.45
    xs = [TABLE_ROOT + hx for hx in WALL_HOOKS]
    box("StandBase", xs[1] - xs[0] + 0.6, 0.3, 0.07, at(sum(xs) / 2, py - 0.05, th + 0.01), "fd_lacquer")   # off the feet's bottoms
    for sx in xs:
        box("StandFoot", 0.36, 1.1, 0.14, at(sx, py - 0.3, th), "fd_lacquer")
        box("Upright", 0.3, 0.45, top - th - 0.1, at(sx, py - 0.045, th + 0.1), "fd_lacquer")   # 0.04 into the foot; front face at py - 0.27
        box("UprightCap", 0.36, 0.51, 0.08, at(sx, py - 0.045, top - 0.04), "gold")   # 0.04 over the upright
    for za in TABLE_TIERS:
        _hooks(TABLE_ROOT, za, py, brace=False, cap_z=0.33)


def sword_flat(prefix, gx, y, z, blade):
    """Review prop: a sword lying along X as the rack shows it, guard at gx, grip toward -X, blade edge up."""
    L = BLADES[blade]
    box(prefix + "Blade", L - 0.3, 0.05, 0.2, at(gx + (L - 0.3) / 2, y, z - 0.1), "steel")
    frustum(prefix + "Tip", 0.2, 0.05, 0.03, 0.04, 0.3, at(gx + L - 0.3, y, z), "steel", rot=(0, 90, 0))
    box(prefix + "Guard", 0.1, 0.14, 0.5, at(gx - 0.05, y, z - 0.25), "gold")
    cyl(prefix + "Grip", 0.08, GRIP, at(gx - 0.1, y, z), "red", sides=6, rot=(0, -90, 0))
    rock(prefix + "Pommel", 0.1, at(gx - 0.1 - GRIP - 0.05, y, z), "iron_dk", seed=1)


def wall_holder_review():
    """Review only: a 3-sword wall rack and a 3-sword table in the shop's colours, with a katana, wakizashi and
    tanto on each. Not exported."""
    zs = wall_sword_holder("WallSwordRack", 190.0, 0, rows=3)
    sword_table("SwordTable", 199.5, -4.0)
    station("WallHolderReview", 0, 0)
    for xp in (186.2, 196.2):
        post("ReviewPost", xp, 0.25, C=FD)
    wall("ReviewWall", 186.75, 195.65, 0.25, along="x", C=FD)
    box("ReviewFloor", 24, 12, 0.2, at(194.0, -5.0, 0), "fd_wood_dk")
    blades = ("katana", "wakizashi", "tanto")
    for za, blade in zip(zs, blades):
        sword_flat("Wall" + blade.capitalize(), 190.0, WALL_SLOT[1], za, blade)
    for za, blade in zip(TABLE_TIERS, blades):
        sword_flat("Table" + blade.capitalize(), 199.5 + TABLE_ROOT, -4.0 + TABLE_STAND_Y + WALL_SLOT[1], za, blade)


PAV_DX = 8.0   # Allen 2026-10-20: the crafting pavilion stands apart from the shop (walls 9 apart, eaves ~4 apart)


def pavilion():
    """The crafting courtyard (Allen 2026-10-20: "remove the roof and the pillars. just keep the stone tile
    floors"): the stations work in the open on a paved stone courtyard, 8 studs east of the shop."""
    station("Courtyard", PAV_DX, 0)   # old coordinates, shifted by the root
    x0, x1, y0, y1 = -19.0, 31.0, 4.0, 32.0
    # front edge reaches Roblox z 2.5, where the main courtyard paving starts
    paving("Paving", x0 - 3, x1 + 3, y0 - 6.5, y1 + 2)


def stone_lantern(name="StoneLantern", x=0, y=0):
    """Low-poly standing stone lantern (ishi-doro), 5.6 studs tall: square base, hexagonal pillar, platform,
    a light box with paper windows (the game adds a PointLight at LIGHT_Z), a wide hexagonal roof and a
    finial."""
    station(name, x, y)
    frustum("Base", 1.9, 1.9, 1.5, 1.5, 0.5, at(0, 0, 0), "stone_dk")
    cyl("Pillar", 0.42, 2.03, at(0, 0, 0.47), "stone", sides=6, r2=0.36)
    frustum("Platform", 1.1, 1.1, 1.5, 1.5, 0.38, at(0, 0, 2.47), "stone")
    box("LightBox", 1.0, 1.0, 1.03, at(0, 0, 2.82), "stone")
    for ax, ay, w, d in ((0, -0.51, 0.6, 0.04), (0, 0.51, 0.6, 0.04), (-0.51, 0, 0.04, 0.6), (0.51, 0, 0.04, 0.6)):
        box("Window", w, d, 0.6, at(ax, ay, 3.05), "paper")
    cyl("Roof", 1.25, 0.55, at(0, 0, 3.82), "stone_dk", sides=6, r2=0.35)
    cyl("RoofTop", 0.36, 0.3, at(0, 0, 4.34), "stone_dk", sides=6, r2=0.18)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=8, v_segments=6, radius=0.25)
    _finish("Finial", bm, "stone", at(0, 0, 4.85), (0, 0, 0), 0, smooth=False)


LANTERN_LIGHT_Z = 3.15


# ---------------------------------------------------------------- bamboo

def bamboo(name="Bamboo1", x=0, y=0, seed=1, stalks=6, height=15.0):
    """Low-poly bamboo clump: hexagonal stalks in segments that step in at every node ring, a slight lean,
    three greens, and fans of long double-sided leaves on the upper half."""
    import random
    rnd = random.Random(seed)
    station(name, x, y)
    for s in range(stalks):
        a = rnd.uniform(0, 2 * math.pi)
        d = rnd.uniform(0.2, 1.6) if s else 0.0
        bx, by = d * math.cos(a), d * math.sin(a)
        h = height * rnd.uniform(0.75, 1.05)
        lean = Vector((rnd.uniform(-0.06, 0.06), rnd.uniform(-0.06, 0.06), 1)).normalized()
        r = rnd.uniform(0.2, 0.3)
        col = ("bamboo", "bamboo_dk", "bamboo_lt")[s % 3]
        seg = rnd.uniform(1.8, 2.4)
        z = -0.03 * s   # each stalk sinks a little deeper, so no two share a bottom face
        k = 0
        while z < h - 0.5:
            sl = min(seg, h - z)
            base = Vector((bx, by, 0)) + lean * z
            rr = r * (1 - 0.35 * z / h)
            cyl(f"{name}Stalk", rr, sl - 0.06, base, col, sides=6, r2=rr * 0.96,
                rot=(math.degrees(math.atan2(-lean.y, lean.z)), math.degrees(math.atan2(lean.x, lean.z)), 30 * (k % 2)))
            cyl(f"{name}Node", rr * 1.18, 0.12, base + lean * (sl - 0.09), "bamboo_dk", sides=6,
                rot=(math.degrees(math.atan2(-lean.y, lean.z)), math.degrees(math.atan2(lean.x, lean.z)), 0))
            # leaf fans from the upper nodes
            if z > h * 0.45:
                for _ in range(rnd.randint(2, 4)):
                    leaf(f"{name}Leaf", base + lean * (sl - 0.1), rnd, ("leaf", "leaf_lt")[rnd.randint(0, 1)])
            z += sl
            k += 1


def leaf(name, root, rnd, color):
    """A long, slightly drooping blade: a thin double-sided prism, low-poly."""
    yaw = rnd.uniform(0, 2 * math.pi)
    L = rnd.uniform(1.8, 3.0)
    w = L * 0.16
    droop = rnd.uniform(-35, -10)
    pts = [(0, 0), (L * 0.35, w / 2), (L, 0), (L * 0.35, -w / 2)]
    bm = bmesh.new()
    th = 0.05
    a = [bm.verts.new((u, v, -th / 2)) for u, v in pts]
    b = [bm.verts.new((u, v, th / 2)) for u, v in pts]
    bm.faces.new(a[::-1]); bm.faces.new(b)
    for i in range(4):
        j = (i + 1) % 4
        bm.faces.new((a[i], a[j], b[j], b[i]))
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return _finish(name, bm, color, root, (0, -droop, math.degrees(yaw)), 0, smooth=False)


def join_by_material(coll_name):
    """Merge a collection's meshes into one object per material (fewer MeshParts in Roblox)."""
    coll = bpy.data.collections[coll_name]
    groups = {}
    for o in list(coll.objects):
        if o.type == "MESH" and o.data.materials:
            # roof, gables and the overhead beams (eave beams, tie beams) kept apart so they hide together
            part = "Roof_" if o.name.startswith(("Roof", "Gable", "Beam", "TieBeam", "Upper", "Canopy")) else ""
            groups.setdefault((part, o.data.materials[0].name), []).append(o)
    for (part, matname), objs in groups.items():
        if len(objs) > 1:
            with bpy.context.temp_override(active_object=objs[0], selected_editable_objects=objs, selected_objects=objs):
                bpy.ops.object.join()
        objs[0].name = objs[0].data.name = coll_name + "_" + part + matname.replace("LP_", "")


BUILD_EXPORT = ("Storefront", "Courtyard", "Bamboo1", "Bamboo2", "Bamboo3", "StoneLantern")


def build_all():
    storefront()
    pavilion()
    bamboo("Bamboo1", 60, -10, seed=1, stalks=6, height=15)
    bamboo("Bamboo2", 70, -10, seed=2, stalks=7, height=16.5)
    bamboo("Bamboo3", 80, -10, seed=3, stalks=5, height=13.5)
    stone_lantern("StoneLantern", 90, -10)
    for n in BUILD_EXPORT:
        join_by_material(n)

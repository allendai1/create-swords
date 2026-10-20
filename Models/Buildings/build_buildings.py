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


def post(name, x, y, h=EAVE + 0.8, w=1.1):
    """Timber post on a chunky stone footing."""
    frustum(name + "Foot", w + 0.9, w + 0.9, w + 0.5, w + 0.5, 0.6, at(x, y, 0), "stone")
    box(name, w, w, h - 0.56, at(x, y, 0.56), "timber")   # 0.04 into the footing: no shared faces


def wall(name, a, b, fixed, along="x", top=EAVE, t=0.5):
    """Wall panel between two posts: stone sill, dark board wainscot, plaster, a mid tie band (inside and
    out), along X (y = fixed) or along Y (x = fixed). a..b are the clear span between post faces."""
    L, c = b - a + 0.2, (a + b) / 2   # 0.1 into each post, so no faces are shared with them
    if along == "x":
        def put(n, h, z, col, thick, off=0.0):   # trim layers end 0.05 short of the plaster's ends
            box(n, L if off == 0 else L - 0.1, thick, h, at(c, fixed + off, z), col)
        sides = (-1, 1)
        for s in sides:
            put(name + "Sill", 0.5, FLOOR, "stone_dk", 0.3, s * (t / 2 + 0.1))
            put(name + "Boards", 2.54, FLOOR + 0.46, "timber_dk", 0.2, s * (t / 2 + 0.06))
            put(name + "Band", 0.5, 7.0, "timber", 0.2, s * (t / 2 + 0.06))
        put(name, top - FLOOR + 0.01, FLOOR + 0.04, "plaster", t)
    else:
        def put(n, h, z, col, thick, off=0.0):
            box(n, thick, L if off == 0 else L - 0.1, h, at(fixed + off, c, z), col)
        for s in (-1, 1):
            put(name + "Sill", 0.5, FLOOR, "stone_dk", 0.3, s * (t / 2 + 0.1))
            put(name + "Boards", 2.54, FLOOR + 0.46, "timber_dk", 0.2, s * (t / 2 + 0.06))
            put(name + "Band", 0.5, 7.0, "timber", 0.2, s * (t / 2 + 0.06))
        put(name, top - FLOOR + 0.01, FLOOR + 0.04, "plaster", t)


def lattice_bay(name, x0, x1, y, top=EAVE):
    """Shop-front bay: low board wall, sill, vertical lattice bars, lintel and plaster transom (along X)."""
    L, c = x1 - x0 + 0.2, (x0 + x1) / 2
    box(name + "Low", L, 0.5, 2.8, at(c, y, FLOOR), "timber_dk")
    box(name + "Sill", L + 0.2, 0.8, 0.25, at(c, y, 3.0), "timber")
    n = max(3, int(L / 0.9))
    for i in range(1, n):
        box(name + "Bar", 0.18, 0.18, 4.9, at(x0 + L * i / n, y, 3.25), "timber_dk")
    box(name + "Rail", L, 0.22, 0.18, at(c, y, 5.6), "timber_dk")
    box(name + "Lintel", L + 0.1, 0.6, 0.45, at(c, y, 8.15), "timber")
    box(name + "Transom", L, 0.5, top - 8.56 + 0.05, at(c, y, 8.56), "plaster")


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


def door_bay(name, a, b, x, door=5.0, top=EAVE):
    """Wall along Y between posts with a centred doorway: wall stubs either side, lintel and plaster above."""
    c = (a + b) / 2
    wall(name + "L", a, c - door / 2, x, along="y")
    wall(name + "R", c + door / 2, b, x, along="y")
    box(name + "Lintel", 0.6, door + 0.4, 0.45, at(x, c, 8.15), "timber")
    box(name + "Transom", 0.46, door + 0.2, top - 8.56 + 0.03, at(x, c, 8.56), "plaster")   # top 0.02 under the stubs   # thinner than the stubs: no shared faces
    box(name + "Step", 1.6, door, 0.23, at(x, c, FLOOR - 0.05), "stone")


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
SHOP_UPGRADED = dict(x0=-49.0, x1=-18.0, y0=-16.0, y1=22.0, entrance=12.0, door_segment=1)   # 31 x 38
SHOP_STARTER = dict(x0=-42.0, x1=-18.0, y0=-16.0, y1=-2.0, entrance=7.0, door_segment=1)     # 24 x 14


def storefront():
    """The Upgraded Store."""
    make_shop("Storefront", **SHOP_UPGRADED)


def starter_shop():
    """The shop players start with."""
    make_shop("StarterShop", **SHOP_STARTER)


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
            part = "Roof_" if o.name.startswith(("Roof", "Gable", "Beam", "TieBeam")) else ""
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

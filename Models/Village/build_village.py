# Cliff ring and village props for Create Swords! (Allen 2026-10-20: "we actually have the mineshaft built into
# the walls of the map ... the walls should enclose all of them", then "Don't use terrain, make the mountains
# in blender").
# Reuses the helpers and palette in Models/Stations/build_stations.py and join_by_material from
# Models/Buildings/build_buildings.py:
#   ns = {"__name__": "lib"}; exec(build_stations.py, ns); exec(build_buildings.py, ns); exec(build_village.py, ns)
#   ns["build_all"]()
# Blender X = Roblox X, Blender Y = -Roblox Z, z = 0 is the ground (Baseplate top).
#
# Village (Roblox coordinates): the open floor inside the cliff is x -226..234, z -66..194. Three 140 x 110 plot
# slots back onto the north face (z -66, fronts toward +z) and three onto the south face (z 194, fronts toward
# -z); a stone path runs east-west between them. Plot 1 is the middle north slot (centre x 4, z -11).
# The ring never comes inside the face line. Each plot carries its own MineFace: a rock buttress that comes out
# of the cliff around the mine portal, so it moves with the plot when the plot is cloned into the other slots.
import math
import random
import bmesh
from mathutils import Vector, noise

DETAIL = "low"
PAL.update({
    "rock":     (0.47, 0.44, 0.40),
    "rock_dk":  (0.38, 0.36, 0.33),
    "rock_lt":  (0.55, 0.52, 0.47),
    "grass":    (0.44, 0.60, 0.28),
    "grass_dk": (0.34, 0.49, 0.22),
    "pine":     (0.20, 0.40, 0.24),
    "pine_dk":  (0.14, 0.31, 0.19),
    "bark":     (0.36, 0.25, 0.18),
    "sakura":   (0.96, 0.72, 0.80),
    "sakura_lt": (0.99, 0.84, 0.88),
    "maple":    (0.80, 0.26, 0.17),
    "maple_lt": (0.90, 0.42, 0.20),
})

X0, X1, Z0, Z1 = -226.0, 234.0, -66.0, 194.0   # inside face line
RC = 12.0                                      # inner corner radius
PLINTH = 5.5                                   # height of the plain base band under the strata
def B(x, z, h):
    return Vector((x, -z, h))


def ring_samples(step=8.0):
    """Points on the inner face line, walking the rounded rectangle, with outward normals."""
    pts = []

    def edge(a, b, fixed, along_x, sign):
        n = max(1, round(abs(b - a) / step))
        for i in range(n):
            t = a + (b - a) * i / n
            pts.append(((t, fixed) if along_x else (fixed, t), (0.0, sign) if along_x else (sign, 0.0)))

    def arc(cx, cz, a0):
        for i in range(4):
            a = math.radians(a0 + 90 * i / 4)
            pts.append(((cx + RC * math.cos(a), cz + RC * math.sin(a)), (math.cos(a), math.sin(a))))

    # north face (z = Z0, outward -z) west to east, then round the corners clockwise
    edge(X0 + RC, X1 - RC, Z0, True, -1.0)
    arc(X1 - RC, Z0 + RC, 270)
    edge(Z0 + RC, Z1 - RC, X1, False, 1.0)
    arc(X1 - RC, Z1 - RC, 0)
    edge(X1 - RC, X0 + RC, Z1, True, 1.0)
    arc(X0 + RC, Z1 - RC, 90)
    edge(Z1 - RC, Z0 + RC, X0, False, -1.0)
    arc(X0 + RC, Z0 + RC, 180)
    return pts


def cliff_ring(name="CliffRing"):
    """One closed ring: a ledged cliff face from the floor to the rim (four strata, each stepping back onto a
    grassy ledge), a grassy rim, and mountains rising behind it that drop back to the ground far outside.
    Coloured by slope: steep faces are rock in bands per stratum, gentle faces grass."""
    station(name, 0, 0)
    samples = ring_samples()
    STRATA = 4
    back = [3, 10, 20, 34, 52, 74, 100, 130, 162, 195]               # distance behind the rim edge
    # colour of each face quad, bottom up: the plinth, then per stratum its face and the ledge above it
    bands = ["rock_dk"] + [("rock_lt", "rock", "rock_dk", "rock")[s] for s in range(STRATA) for _ in (0, 1)][:-1]
    grid = []
    u = 0.0
    prev = None
    for (px, pz), (nx, nz) in samples:
        if prev:
            u += math.hypot(px - prev[0], pz - prev[1])
        prev = (px, pz)
        rim = 52 + 8 * math.sin(u / 53) + 5 * math.sin(u / 19 + 1) + 3 * noise.noise(Vector((u / 15, 0.3, 0.7)))
        peak = 45 + 55 * (0.5 + 0.5 * noise.noise(Vector((u / 70, 1.7, 0.2))))
        def J(amp, k):   # jitter that is smooth along the ring, so the fine columns at a portal stay clean
            return amp * noise.noise(Vector((u / 3.2, k * 1.37, 9.1)))
        rows = [(0.3, -0.5), (1.1 + J(0.3, 1), PLINTH)]
        d = rows[-1][0]
        for st in range(STRATA):
            lo = PLINTH + (rim - PLINTH) * st / STRATA
            hi = PLINTH + (rim - PLINTH) * (st + 1) / STRATA
            if st:   # step back onto the next stratum: a ledge (the first stratum starts on the notch row)
                d += 1.0 + 1.4 * (0.5 + 0.5 * noise.noise(Vector((u / 30, st * 2.3, 1.1)))) + J(0.3, 10 + st) + 0.3
                rows.append((d + J(0.8, 20 + st), lo + J(0.3, 30 + st)))
            d += 0.6 + 2.6 * (0.5 + 0.5 * noise.noise(Vector((u / 7, st * 1.7, 4.0))))   # lean and vertical ribs
            top = hi if st == STRATA - 1 else hi + J(1.2, 40 + st)
            rows.append((d + J(1.0, 50 + st), top))
        col = list(rows)
        d_rim = col[-1][0]
        for k, db in enumerate(back):
            s_ = max(0.0, min(1.0, (db - 8) / 120)) ** 1.15
            hh = rim + peak * s_ + 3 * noise.noise(Vector((u / 14, db / 25, 2.0))) + (1.0 if k == 0 else 0)
            col.append((d_rim + db + J(2.0, 60 + k), hh))
        col.append((d_rim + 230, -1.0))
        grid.append([B(px + nx * dd, pz + nz * dd, hh) for dd, hh in col])

    groups = {}
    nu, nv = len(grid), len(grid[0])
    nf = len(bands)        # quads 0..nf-1 run up the face; the rest are the rim and mountains
    for i in range(nu):
        a, b = grid[i], grid[(i + 1) % nu]
        (_, (nx, nz)) = samples[i]
        out = Vector((nx, -nz, 0))
        for j in range(nv - 1):
            # faces point away from the rock: toward the village up the face, up on top, outward on the far slope
            want = (-out + Vector((0, 0, 0.3))) if j < nf else (Vector((0, 0, 1)) if j < nv - 2 else out + Vector((0, 0, 1)))
            mid = (a[j] + b[j + 1]) / 2
            for tri in ((a[j], b[j], b[j + 1]), (a[j], b[j + 1], a[j + 1])):
                n = (tri[1] - tri[0]).cross(tri[2] - tri[0])
                if n.length < 1e-6:
                    continue
                n.normalize()
                if n.dot(want) < 0:
                    tri = (tri[0], tri[2], tri[1])
                    n = -n
                if n.z > 0.55:
                    key = "grass_dk" if j < nf or noise.noise(mid / 70) < -0.2 else "grass"
                elif j < nf:
                    key = bands[j]
                else:
                    key = "rock"
                groups.setdefault(key, []).append(tri)
    _mesh_groups(name, groups, at(0, 0, 0))
    return groups


def _tris_by_colour(cols, want, key_for):
    """Triangulate a grid of columns (lists of points, bottom to top), wind every triangle toward `want`,
    and sort them by colour key."""
    groups = {}
    for i in range(len(cols) - 1):
        a, b = cols[i], cols[i + 1]
        for j in range(len(a) - 1):
            for tri in ((a[j], b[j], b[j + 1]), (a[j], b[j + 1], a[j + 1])):
                n = (tri[1] - tri[0]).cross(tri[2] - tri[0])
                if n.length < 1e-6:
                    continue
                n.normalize()
                if n.dot(want) < 0:
                    tri, n = (tri[0], tri[2], tri[1]), -n
                groups.setdefault(key_for(n, (tri[0] + tri[1] + tri[2]) / 3, j), []).append(tri)
    return groups


def _mesh_groups(name, groups, loc):
    for key, tris in groups.items():
        bm = bmesh.new()
        vmap = {}
        for tri in tris:
            vs = []
            for p in tri:
                k = (round(p.x, 3), round(p.y, 3), round(p.z, 3))
                if k not in vmap:
                    vmap[k] = bm.verts.new(p)
                vs.append(vmap[k])
            try:
                bm.faces.new(vs)
            except ValueError:
                pass
        _finish(f"{name}_{key}", bm, key, loc, (0, 0, 0), 0, smooth=False)


MINE_FLAT, MINE_W, MINE_OUT, MINE_BURY = 9.0, 20.0, 10.0, 6.0
NOTCH_W, NOTCH_H = 4.5, 5.5


def mine_face(name="MineFace", x=0, y=0):
    """Rock buttress that grows out of the cliff around a plot's mine portal, in the cliff's strata colours.
    Origin on the cliff's face line at ground level, centred on the portal; the village is toward -Y.
    It comes MINE_OUT studs out for MINE_FLAT either side of the portal (so the cave's rocks sit in it, not in
    front of it), tapers into the cliff by MINE_W and toward its top (buried MINE_BURY studs into the rock
    there, more higher up), and leaves a NOTCH_W x NOTCH_H opening for the portal, recessed
    to the face line. Plot 1's portal is at Roblox (44, z -66); the cave model stands in the opening."""
    station(name, x, y)
    xs = sorted(set([-MINE_W - 2, MINE_W + 2] + [i * 3.0 for i in range(-6, 7)]
                    + [i * 1.5 for i in range(-5, 6)] + [-NOTCH_W, NOTCH_W]))
    hs = [-0.5, 3.0, NOTCH_H, 9, 13, 17, 21, 25, 29, 33]
    cols = []
    for gx in xs:
        col = []
        for h in hs:
            ax = abs(gx)
            k = 1.0 if ax <= MINE_FLAT else (0.5 + 0.5 * math.cos(math.pi * (ax - MINE_FLAT) / (MINE_W - MINE_FLAT)) if ax < MINE_W else 0.0)
            e = k * (1 - max(0.0, min(1.0, (h - 8) / 22)))
            d = -MINE_OUT * e + (1 - e) * (MINE_BURY + 0.45 * max(h, 0))   # the cliff's upper strata step back, so bury deeper higher up
            d += 0.9 * e * noise.noise(Vector((gx / 2.5, h / 3.0, 5.5)))
            if abs(gx) < NOTCH_W - 0.01 and h <= NOTCH_H:
                d = 0.0
            col.append(Vector((gx, d, h)))
        cols.append(col)

    def key_for(n, c, j):
        if n.z > 0.8:      # only real shelves get grass; the buttress shoulders stay rock
            return "grass_dk"
        return ("rock_dk", "rock_lt", "rock", "rock_dk")[min(3, int(max(c.z, 0) // 9))]
    _mesh_groups(name, _tris_by_colour(cols, Vector((0, -1, 0.3)), key_for), at(0, 0, 0))


PATH_Z = (54.0, 74.0)   # Roblox z of the stone path's edges; plot fronts are at z 44 (north) and 84 (south)


def village_path(name="VillagePath"):
    """The village street: the courtyard's stone flags (paving()), 4-stud flags, wall to wall along X."""
    station(name, 0, 0)
    paving("Path", X0, X1, -PATH_Z[1], -PATH_Z[0], flag=4.0)


# ---------------------------------------------------------------- props

def pine(name="Pine", x=0, y=0, seed=1, height=18.0):
    """Low-poly Japanese-style pine: tall trunk and three or four flat, offset tiers of needles."""
    rnd = random.Random(seed)
    station(name, x, y)
    cyl("Trunk", 0.55, height * 0.75, at(0, 0, 0), "bark", sides=6, r2=0.35)
    tiers = rnd.randint(3, 4)
    for t in range(tiers):
        z = height * (0.38 + 0.6 * t / tiers)
        r = (5.4 - 1.0 * t) * rnd.uniform(0.9, 1.1)
        off = at(rnd.uniform(-0.6, 0.6), rnd.uniform(-0.6, 0.6), z)
        cyl("Tier", r, r * 0.45, off, ("pine", "pine_dk")[t % 2], sides=7, r2=r * 0.3)


def blossom_tree(name="Sakura", x=0, y=0, seed=1, colors=("sakura", "sakura_lt"), height=11.0):
    """Low-poly sakura or maple: a leaning trunk that forks into two limbs, under a canopy of faceted clumps."""
    rnd = random.Random(seed)
    station(name, x, y)
    lean = rnd.uniform(-8, 8)
    cyl("Trunk", 0.8, height * 0.5, at(0, 0, 0), "bark", sides=6, r2=0.55, rot=(lean, 0, 0))
    top = at(0, -math.sin(math.radians(lean)) * height * 0.5, height * 0.48)
    for sgn in (-1, 1):
        cyl("Limb", 0.42, height * 0.35, top, "bark", sides=6, r2=0.25, rot=(0, sgn * rnd.uniform(25, 40), 0))
    for i in range(9):
        a = 2 * math.pi * i / 8 + rnd.uniform(-0.3, 0.3)
        d = rnd.uniform(3.0, 4.6) if i else 0.0
        c = top + at(d * math.cos(a), d * math.sin(a), rnd.uniform(2.4, 4.0) if i else 4.6)
        rock("Canopy", rnd.uniform(2.8, 3.6), c, colors[i % 2], scale=(1.2, 1.2, 0.8), seed=seed * 31 + i)


VILLAGE_EXPORT = ("CliffRing", "MineFace", "VillagePath", "Pine1", "Pine2", "Sakura1", "Sakura2", "Maple1")


def build_all():
    cliff_ring()
    village_path()
    mine_face("MineFace", 44, 66)   # Plot 1's portal (Roblox x 44, z -66), for review in place
    pine("Pine1", 300, -600, seed=1, height=18)
    pine("Pine2", 320, -600, seed=2, height=22)
    blossom_tree("Sakura1", 340, -600, seed=1)
    blossom_tree("Sakura2", 360, -600, seed=2, height=12)
    blossom_tree("Maple1", 380, -600, seed=3, colors=("maple", "maple_lt"))
    for n in VILLAGE_EXPORT[2:]:
        join_by_material(n)

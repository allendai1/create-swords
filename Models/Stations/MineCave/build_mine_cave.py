# Mine cave for Create Swords! (Allen 2026-10-20, two references of a stylised mine entrance,
# References/Concept Art/mine-cave-ref-1.png and -2.png): "can you make the mineshaft look more like this. Ignore the
# details of the trees and rocks, just look the silhouette of the cave. soft bevels, and soft looking rocks, with
# handpainted texturing."
#
# Replaces the log A-frame MineEntrance (same footprint, same mouth, same track). After Allen's reviews ("a messy pile
# of rocks on top of the wooden mine shaft", "too round like a ball or igloo", "they look like stacked rectangular
# blocks"): a cohesive rocky outcrop of large, irregular, interlocking angular boulders with an asymmetric stepped top
# (peak at the back right) and masses protruding along the sides and base. The entrance is excavated into it: timber
# (two posts, a lintel, a plank awning, rope lashings) holds the mouth, and behind it a rock tunnel narrows and fades
# into darkness, past two dim support frames, to a black closure 5.8 studs back.
#
# Run headless:  blender --background --python build_mine_cave.py
# Writes, next to this script: MineCave.blend, Mine_Cave.fbx (Roblox preset), Textures/mine_cave_rocks.png and
# mine_cave_wood.png (1024 px colour, baked), review/*.png, qa.json.
#
# Units are studs, Z up, front faces -Y, origin on the floor at the middle of the mouth (the MineEntrance origin, at
# Roblox (44, 0.2, -58) facing +Z).
#   Rocks: one mesh, the boulders (tunnel cut out of each) and the tunnel's rock lining, which fades to black.
#   Wood:  one mesh, the mouth's posts, lintel, plank awning and rope lashings, and two support frames inside.
#   void:  the black closure at the end of the tunnel (flat black in the game).
# The hand-painted look is baked, never photo textures: each rock runs light at its top to dark at its foot, catches
# a pale highlight on its upper edges and chips, darkens in the crevices (AO against the other rocks, the wood and the ground)
# and gets broad brushy value breakup and a little moss at the foot. Wood is warm with painted grain lines, per-plank
# tone shifts, lit edges and dark joints; the rope has a twist stripe. No normal map: the bevels and chips are real
# geometry.
import math
import os
import random
import sys
import json
import bpy
import bmesh
from mathutils import Vector, Matrix, Euler

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, "Textures")
REVIEW = os.path.join(HERE, "review")
SKILLS = "C:/Users/Allen/.claude/plugins/cache/blender-agent-skills/blender-agent-skills/1.1.0/skills"
sys.path.insert(0, os.path.dirname(HERE))
import build_stations as bs  # noqa: E402  (zfight_check)

TEX_SIZE = 1024                      # Roblox SurfaceAppearance maximum

# ---------------------------------------------------------------- layout (studs)
POST_X, POST_Y, POST_W, POST_H = 2.05, -2.4, 0.55, 3.3   # front posts: centre x +-2.05, top at 3.3
LINTEL = dict(x=3.0, y=(-2.73, -2.07), z=(3.25, 3.8))     # sits 0.05 into the post tops
ROOF_Y, ROOF_Z = (-3.15, 0.0), 3.76                       # plank awning on the lintel; projects from the rock face
LANTERN = (2.65, -2.95, 3.45)                             # top of the game's lantern, hung under the awning's right end
# The tunnel behind the mouth: a rock lining from just inside the posts back to the black closure, narrowing and
# lowering a little with depth. A cart parked at CartPath.Hidden must sit wholly behind the closure: Hidden −4.5
# (y 4.9) once this is in the game (ForgeService carries the path straight on back for negative distances).
TUNNEL = dict(y0=-2.45, y1=3.4, w=1.95, h=3.3, taper=0.85, sink=0.94, wall=0.25, r=0.8, floor=0.04)
INNER_FRAMES = (0.0, 2.0)                                 # support frames inside the tunnel (y), dimmer with depth
AWNING = dict(x=3.15, y=(-3.45, -0.7), z=(3.6, 4.3))      # the awning's projecting part: no rock may enter it
OPENING = dict(x=1.75, z=3.2)                             # carts (1.94 wide, 2.45 tall) roll through x +-0.97

FULL = {61, 56, 36, 43, 44, 46, 53, 55, 52}   # seeds given fuller bodies and softer tips (Allen: these read as shards)
SOFTEN = FULL | {52, 34}          # right-side blocks: broad merged faces and the soft slab's bevel
GROUNDED = {53}                   # the tall boulder right of the awning: fuller corners, a broad flat foot, no taper
TILT = {44: (7, -6), 55: (-10, 9), 61: (7, -6)}   # x/y tilt (degrees) by hand: no stepped shelves at the right
                                                   # base, and the peak leans a little so it doesn't read as a box
# centre (x, y, z), size (x, y, z), seed[, yaw: set for the blocks framing the mouth so their faces stay square to it]
# Interlocking, tilted boulders; heavier on the right (+X, the side the track turns to); steps up to the peak at the
# back right; masses protruding along the sides and base.
BOULDERS = [
    ((0.4, 4.8, 1.4), (8.8, 8.4, 5.6), 30),           # core and a higher filler: no gaps, so the outcrop is one mass;
    ((1.0, 5.0, 3.6), (6.0, 5.4, 3.4), 29),           # both kept behind the front cluster, where they never show
    # framing the mouth
    ((-3.75, -0.8, 1.8), (3.0, 4.6, 3.8), 59, 10),
    ((4.1, -1.3, 1.3), (3.8, 3.8, 2.8), 52, -8),     # right jamb, low; a smaller block set back on top of it
    ((3.95, 0.2, 2.2), (2.8, 2.8, 2.0), 55, -14),    # tucked under the awning's right end and back into the mass
    ((3.4, 1.4, 4.6), (3.2, 3.2, 2.6), 53),           # steps up behind the right jamb
    ((0.1, 0.9, 4.4), (4.6, 3.0, 2.4), 33, 3),        # the slab over the mouth, set back: the awning projects from it
    # the main mass, right and back, up to the peak
    ((3.6, 2.8, 2.0), (3.8, 3.4, 4.0), 34),           # the big right mass, split in two offset blocks
    ((4.0, 5.0, 2.6), (3.4, 3.0, 4.4), 56),
    ((1.4, 4.6, 5.0), (3.6, 3.4, 3.4), 35),           # the top, split: a step, then the peak behind it
    ((3.4, 6.0, 5.4), (3.4, 3.2, 3.2), 61),          # (seed 57 had a V-notched corner)
    ((4.4, 7.4, 1.4), (3.4, 3.4, 3.6), 36),          # lowered: its top no longer shows as a sliver
    ((1.0, 3.0, 5.4), (3.6, 3.4, 3.0), 37),
    ((-0.3, 6.6, 5.3), (3.6, 3.4, 3.2), 42),
    # the lower left and back, stepping down
    ((-2.8, 2.8, 2.6), (3.8, 4.2, 4.6), 60),
    ((-1.7, 5.0, 3.8), (4.4, 4.2, 3.2), 39),
    ((-3.6, 6.6, 1.6), (3.6, 4.0, 3.2), 40),
    ((-0.4, 8.4, 1.8), (4.4, 2.8, 3.6), 41),
    # protruding along the sides and base
    ((4.6, 1.8, 1.0), (2.6, 3.0, 2.4), 43),          # tucked in, so its tip no longer pokes out
    ((4.9, -2.7, 0.7), (2.4, 2.2, 1.8), 44),
    ((-4.8, 3.4, 1.0), (2.2, 2.6, 2.0), 45),
    ((4.8, 6.6, 0.9), (2.4, 2.6, 1.9), 46),
    ((-3.0, -2.9, 0.45), (1.5, 1.3, 1.1), 47),
    ((-4.3, 8.2, 0.6), (2.0, 2.0, 1.2), 48),
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


def new_object(name, bm, coll, loc=(0, 0, 0), rot=(0, 0, 0)):
    me = bpy.data.meshes.new(name)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    o.location = loc
    o.rotation_euler = Euler([math.radians(a) for a in rot])
    coll.objects.link(o)
    return o


def apply_modifiers(o):
    with bpy.context.temp_override(object=o, active_object=o, selected_objects=[o], selected_editable_objects=[o]):
        for m in list(o.modifiers):
            bpy.ops.object.modifier_apply(modifier=m.name)


def bevel(o, width, segments):
    m = o.modifiers.new("Bevel", "BEVEL")
    m.width, m.segments, m.limit_method, m.profile = width, segments, "NONE", 0.5
    m.use_clamp_overlap = True
    apply_modifiers(o)


def bake_transform(o):
    o.data.transform(o.matrix_basis)   # not matrix_world: that is stale until the depsgraph updates
    o.matrix_basis = Matrix.Identity(4)


def set_attr(o, name, values, kind="FLOAT"):
    a = o.data.attributes.new(name, kind, "POINT")
    a.data.foreach_set("value" if kind == "FLOAT" else "vector", [c for v in values for c in (v if kind != "FLOAT" else (v,))])


def join(objs, name):
    with bpy.context.temp_override(active_object=objs[0], selected_editable_objects=objs, selected_objects=objs):
        bpy.ops.object.join()
    objs[0].name = objs[0].data.name = name
    return objs[0]


def finish(o, smooth_angle):
    """Smooth across the bevels, weighted normals keep the big faces flat, then triangles only (Roblox)."""
    me = o.data
    for p in me.polygons:
        p.use_smooth = True
    me.set_sharp_from_angle(angle=math.radians(smooth_angle))
    m = o.modifiers.new("WeightedNormals", "WEIGHTED_NORMAL")
    m.keep_sharp, m.mode = True, "FACE_AREA"
    apply_modifiers(o)
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=0.0005)          # slivers the tunnel boolean leaves
    bmesh.ops.dissolve_degenerate(bm, edges=bm.edges[:], dist=0.0005)
    bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 3])
    bm.to_mesh(me)
    bm.free()


def unwrap(o, margin=0.004, angle=55):
    vl = bpy.context.view_layer
    for ob in vl.objects:
        ob.select_set(False)
    vl.objects.active = o
    o.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(angle), island_margin=margin, area_weight=0.0,
                             correct_aspect=True, scale_to_bounds=True)
    bpy.ops.object.mode_set(mode="OBJECT")


# ---------------------------------------------------------------- rocks
def boulder(name, centre, size, seed, coll, yaw=None):
    """A heavy, worn boulder: the convex hull of skewed corners (broad irregular faces, none square to another; the top
    corners pulled in less, so there are no wedge ridges or peaks), a broad top and two or three broad changes of plane
    on the sides, a few small chips, then a corner-only bevel: the rounding stays at the corners and the face centres
    stay flat (Allen 2026-10-20: subdivision made them look swollen and rubbery). Upper boulders barely tilt."""
    rnd = random.Random(seed)
    full, soften, grounded = seed in FULL, seed in SOFTEN, seed in GROUNDED
    ext = Vector(size) / 2 * (1.0 if yaw is not None else 1.15)   # the cuts and rounding eat volume; boulders interlock
    pts = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                lo = 0.78 if grounded else (0.7 if full else (0.6 if sz > 0 else 0.5))
                pts.append(Vector((sx * ext.x * rnd.uniform(lo, 1.0) + rnd.gauss(0, 0.1) * ext.x,
                                   sy * ext.y * rnd.uniform(lo, 1.0) + rnd.gauss(0, 0.1) * ext.y,
                                   sz * ext.z * rnd.uniform(0.7, 1.0) + rnd.gauss(0, 0.06) * ext.z)))
    low = []
    for _ in range(3):
        d = Vector((rnd.gauss(0, 1), rnd.gauss(0, 1), -abs(rnd.gauss(0, 1)))).normalized() * rnd.uniform(0.9, 1.0)
        low.append(Vector((d.x * ext.x, d.y * ext.y, d.z * ext.z)))
    if not grounded:            # the low points give the foot its taper; a grounded boulder sits on a broad base
        pts += low
    bm = bmesh.new()
    hull = bmesh.ops.convex_hull(bm, input=[bm.verts.new(p) for p in pts])
    bmesh.ops.delete(bm, geom=list({g for g in hull["geom_interior"] + hull["geom_unused"] if isinstance(g, bmesh.types.BMVert)}),
                     context="VERTS")

    def slice_off(n, depth):
        """Plane off everything beyond `depth` (a fraction of the boulder's extent along n)."""
        n = n.normalized()
        ds = [v.co.dot(n) for v in bm.verts]
        off = max(ds) - depth * (max(ds) - min(ds))
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=n * off, plane_no=n,
                               clear_outer=True)
        bmesh.ops.holes_fill(bm, edges=[e for e in bm.edges if e.is_boundary], sides=0)

    slope = 0.12 if full else 0.28
    slice_off(Vector((rnd.gauss(0, slope), rnd.gauss(0, slope), 1)), rnd.uniform(0.14, 0.24))  # broad top, gently sloped its own way
    if grounded:
        slice_off(Vector((0, 0, -1)), 0.12)                                                     # flat, broad foot
    a0 = rnd.uniform(0, 2 * math.pi)
    for k in range(rnd.randint(2, 3)):                                                         # broad changes of plane
        a = a0 + k * 2.1 + rnd.uniform(-0.4, 0.4)
        slice_off(Vector((math.cos(a), math.sin(a), rnd.gauss(0, 0.12))),
                  rnd.uniform(0.04, 0.08) if full else rnd.uniform(0.07, 0.14))   # near-vertical: no ridges
    keep = bm
    if full:                    # no chips on the fuller rocks (one cut a V notch into the top-right boulder); they are
        bm = keep.copy()        # still drawn on a scratch copy, so the random sequence (and every later turn) is unchanged
    for _ in range(rnd.randint(1, 3)):                                                         # small chips
        upper = sorted(bm.verts, key=lambda v: v.co.z)[len(bm.verts) // 2:]
        c = rnd.choice(upper).co.normalized()
        slice_off(c + Vector((rnd.gauss(0, 0.2), rnd.gauss(0, 0.2), rnd.gauss(0, 0.2))), rnd.uniform(0.03, 0.06))
    if full:
        bm.free()
        bm = keep
    # the right-side blocks merge their near-flat hull facets into broad faces (no small triangular facets)
    bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(20 if soften else 6), verts=bm.verts[:], edges=bm.edges[:])
    turn = (yaw + rnd.uniform(-6, 6)) if yaw is not None else rnd.uniform(0, 360)
    tilt = 3 if full else (4 if yaw is not None or centre[2] > 3.5 else 8)
    rot = [rnd.uniform(-tilt, tilt), rnd.uniform(-tilt, tilt), turn]
    if seed in TILT:            # set by hand: breaks the stepped shelves at the right base
        rot[:2] = TILT[seed]
    o = new_object(name, bm, coll, centre, rot)
    # bevel: the fuller and right-side blocks match the soft slab over the mouth
    bevel(o, min(0.45, min(size) * 0.14) if full else (min(0.42, min(size) * 0.13) if soften else min(0.38, min(size) * 0.1)), 3)
    bake_transform(o)
    zs = [v.co.z for v in o.data.vertices]
    z0, z1 = min(zs), max(zs)
    set_attr(o, "h", [(z - z0) / (z1 - z0) for z in zs])
    set_attr(o, "rnd", [rnd.random()] * len(zs))
    set_attr(o, "depth", [0.0] * len(zs))
    set_attr(o, "grain", [(0.0, 0.0, 0.0)] * len(zs), "FLOAT_VECTOR")
    set_attr(o, "rope", [0.0] * len(zs))
    return o


def tunnel_scale(y):
    """(width scale, height scale, depth 0..1) of the tunnel at y."""
    t = TUNNEL
    f = min(max((y - t["y0"]) / (t["y1"] - t["y0"]), 0.0), 1.0)
    return 1 - (1 - t["taper"]) * f, 1 - (1 - t["sink"]) * f, f


def tunnel_profile(w, h, r, z0, n_floor=4, n_side=3, n_arc=4, n_top=3):
    """Closed tunnel cross-section (x, z, outward normal): flat floor at z0, straight sides, rounded top corners."""
    pts = []
    for i in range(n_floor):
        pts.append((-w + 2 * w * i / n_floor, z0, (0.0, -1.0)))
    for i in range(n_side):
        pts.append((w, z0 + (h - r - z0) * i / n_side, (1.0, 0.0)))
    for i in range(n_arc):
        a = math.pi / 2 * i / n_arc
        pts.append((w - r + r * math.cos(a), h - r + r * math.sin(a), (math.cos(a), math.sin(a))))
    for i in range(n_top):
        pts.append(((w - r) - 2 * (w - r) * i / n_top, h, (0.0, 1.0)))
    for i in range(n_arc):
        a = math.pi / 2 + math.pi / 2 * i / n_arc
        pts.append((-(w - r) + r * math.cos(a), h - r + r * math.sin(a), (math.cos(a), math.sin(a))))
    for i in range(n_side):
        pts.append((-w, (h - r) - (h - r - z0) * i / n_side, (-1.0, 0.0)))
    return pts


def tunnel_lining(coll, rings=12):
    """The excavated tunnel: a solid rock shell (rough inner face, plain outer face) from just inside the posts back to
    the closure. Its front edge hides inside the posts and lintel. `depth` (0 at the mouth, 1 at the closure) paints it
    into darkness."""
    from mathutils import noise
    t = TUNNEL
    bm = bmesh.new()
    loops, depth = [], []
    for k in range(rings + 1):
        y = t["y0"] + (t["y1"] - t["y0"]) * k / rings
        sw, sh, f = tunnel_scale(y)
        inner = tunnel_profile(t["w"] * sw, t["h"] * sh, t["r"], t["floor"])
        outer = tunnel_profile(t["w"] * sw + t["wall"], t["h"] * sh + t["wall"], t["r"] + t["wall"], t["floor"] - t["wall"])
        rough = min(f / 0.08, 1.0) * 0.14                                    # smooth where it meets the timber
        ring_in = []
        for x, z, (nx, nz) in inner:
            d = 0.0 if nz < -0.5 else rough * noise.noise(Vector((x, y, z)) * 1.1)
            ring_in.append(bm.verts.new((x + nx * d, y, z + nz * d)))
        ring_out = [bm.verts.new((x, y, z)) for x, z, _ in outer]
        loops.append((ring_in, ring_out))
        depth += [f] * (len(inner) + len(outer))
    n = len(loops[0][0])
    for (ai, ao), (bi, bo) in zip(loops, loops[1:]):
        for j in range(n):
            jn = (j + 1) % n
            bm.faces.new((ai[j], ai[jn], bi[jn], bi[j]))
            bm.faces.new((ao[j], bo[j], bo[jn], ao[jn]))
    for ring_in, ring_out in (loops[0], loops[-1]):                          # front and back rims
        for j in range(n):
            jn = (j + 1) % n
            bm.faces.new((ring_in[j], ring_out[j], ring_out[jn], ring_in[jn]))
    o = new_object("TunnelLining", bm, coll)
    m = len(o.data.vertices)
    set_attr(o, "depth", depth)
    set_attr(o, "h", [0.3] * m)
    set_attr(o, "rnd", [0.4] * m)
    set_attr(o, "grain", [(0.0, 0.0, 0.0)] * m, "FLOAT_VECTOR")
    set_attr(o, "rope", [0.0] * m)
    return o


def clear_tunnel(o, coll, k=0):
    """Cut the tunnel's room out of a boulder: a box just inside the lining's outer face, from behind the posts' front
    to past the closure. Cut k sits 0.02 * k further in, so neighbouring boulders' cut faces never share a plane (all
    of them are hidden behind the lining)."""
    t = TUNNEL
    x = t["w"] + t["wall"] - 0.06 - 0.02 * k
    z = t["h"] + t["wall"] - 0.06 - 0.02 * k
    y0, y1 = POST_Y - 0.3 + 0.02 * k, t["y1"] + 0.4 - 0.02 * k
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    zb = -1.0 - 0.02 * k                     # underground, staggered like the rest
    bmesh.ops.scale(bm, vec=Vector((2 * x, y1 - y0, z - zb)), verts=bm.verts[:])
    cutter = new_object("TunnelCut", bm, coll, (0, (y0 + y1) / 2, (z + zb) / 2))
    bake_transform(cutter)
    m = o.modifiers.new("Tunnel", "BOOLEAN")
    m.operation, m.solver, m.object = "DIFFERENCE", "EXACT", cutter
    apply_modifiers(o)
    bpy.data.objects.remove(cutter)


# ---------------------------------------------------------------- wood
def plank(name, size, loc, rot, coll, seed, bevel_w=0.06, chip=None):
    """Box `size` (long axis first, laid along local X), centred on loc. `grain` carries the local position, so the
    painted grain runs along the plank whatever its rotation. chip = (side +-1, depth): wear the top corner of the
    local -X end off at a slant."""
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector(size), verts=bm.verts[:])
    if chip:
        side, depth = chip
        n = Vector((-1.0, side * 0.9, 0.6)).normalized()
        corner = Vector((-size[0] / 2, side * size[1] / 2, size[2] / 2))
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=corner - n * depth,
                               plane_no=n, clear_outer=True)
        bmesh.ops.holes_fill(bm, edges=[e for e in bm.edges if e.is_boundary], sides=0)
    o = new_object(name, bm, coll, loc, rot)
    bevel(o, bevel_w, 3)
    n = len(o.data.vertices)
    set_attr(o, "grain", [tuple(v.co) for v in o.data.vertices], "FLOAT_VECTOR")
    set_attr(o, "rnd", [random.Random(seed).random()] * n)
    set_attr(o, "h", [0.0] * n)
    set_attr(o, "rope", [0.0] * n)
    bake_transform(o)
    return o


def rope_ring(name, centre, R, r, coll, rot=(0, 0, 0), segs=20, tube=8):
    """One coil of rope: a torus in local XY. `grain` = (distance round the ring, distance round the tube)."""
    bm = bmesh.new()
    grid, grain = [], []
    for i in range(segs):
        u = 2 * math.pi * i / segs
        ring = []
        for j in range(tube):
            v = 2 * math.pi * j / tube
            rr = R + r * math.cos(v)
            ring.append(bm.verts.new((rr * math.cos(u), rr * math.sin(u), r * math.sin(v))))
            grain.append((u * R, v * r, 0.0))
        grid.append(ring)
    for i in range(segs):
        for j in range(tube):
            bm.faces.new((grid[i][j], grid[(i + 1) % segs][j], grid[(i + 1) % segs][(j + 1) % tube], grid[i][(j + 1) % tube]))
    o = new_object(name, bm, coll, centre, rot)
    n = len(o.data.vertices)
    set_attr(o, "grain", grain, "FLOAT_VECTOR")
    set_attr(o, "rope", [1.0] * n)
    set_attr(o, "rnd", [0.5] * n)
    set_attr(o, "h", [0.0] * n)
    bake_transform(o)
    return o


def portal(coll):
    parts = []
    # front posts, a hair taller on the right so the tops never share a plane with anything
    for i, s in enumerate((-1, 1)):
        h = POST_H + 0.1 + 0.03 * i
        parts.append(plank(f"Post{i}", (h, POST_W, POST_W), (s * POST_X, POST_Y, h / 2 - 0.1), (0, -90, 0), coll, 20 + i, 0.08))
    x, (y0, y1), (z0, z1) = LINTEL["x"], LINTEL["y"], LINTEL["z"]
    parts.append(plank("Lintel", (2 * x, y1 - y0, z1 - z0), (0, (y0 + y1) / 2, (z0 + z1) / 2), (0, 0, 1.2), coll, 22, 0.08))
    # roof: five planks of mixed widths laid left to right (Allen 2026-10-20), stacked from the front edge back into the
    # rock, each with its own small tilt, uneven ends and sometimes a worn corner on one end
    widths = (0.66, 0.58, 0.64, 0.55, 0.6)
    gap, half = 0.04, 3.03
    rnd = random.Random(31)
    y = ROOF_Y[0]
    for i, w in enumerate(widths):
        x0, x1 = -half + rnd.uniform(-0.25, 0.15), half + rnd.uniform(-0.15, 0.25)   # uneven lengths
        t = 0.2 + 0.02 * (i % 3)
        right = rnd.random() < 0.5                      # the worn end: local -X is the left end, or the right if turned
        chip = (rnd.choice((-1, 1)), rnd.uniform(0.08, 0.16)) if rnd.random() < 0.6 else None
        parts.append(plank(f"Roof{i}", (x1 - x0, w, t), ((x0 + x1) / 2, y + w / 2, ROOF_Z + t / 2 + 0.01 * (i % 2)),
                           (rnd.uniform(-1.5, 1.5), 0, (180 if right else 0) + rnd.uniform(-1.2, 1.2)), coll, 40 + i, 0.05, chip))
        y += w + gap
    # support frames inside the tunnel: two posts and a cap each, fitted to the lining, dimmer with depth
    for k, fy in enumerate(INNER_FRAMES):
        sw, sh, _ = tunnel_scale(fy)
        px, top = TUNNEL["w"] * sw - 0.2, TUNNEL["h"] * sh - TUNNEL["r"] * 0.35
        for i, sx in enumerate((-1, 1)):
            hh = top + 0.05 + 0.02 * i
            parts.append(plank(f"InnerPost{k}{i}", (hh, 0.4, 0.4), (sx * px, fy, hh / 2 - 0.05), (0, -90, 0), coll, 70 + 2 * k + i, 0.05))
        parts.append(plank(f"InnerCap{k}", (2 * px + 0.5, 0.42, 0.34), (0, fy, top - 0.1), (0, 0, 0), coll, 74 + k, 0.05))
    # rope lashings: two coils round each post under the lintel, one round each lintel end
    for i, s in enumerate((-1, 1)):
        for k, z in enumerate((2.85, 3.02)):
            parts.append(rope_ring(f"Lash{i}{k}", (s * POST_X, POST_Y, z), POST_W * 0.68, 0.075, coll, (0, 0, 8 * k)))
        for k, dx in enumerate((0.0, 0.17)):
            parts.append(rope_ring(f"LintelLash{i}{k}", (s * (POST_X + 0.25 + dx), POST_Y, 3.52), 0.42, 0.07, coll,
                                   (0, 90, 6 * k)))
    # short rope the lantern hangs from (the lantern itself stays the game's Neon part)
    lx, ly, lz = LANTERN
    top = ROOF_Z + 0.06
    parts.append(plank("LanternRope", (top - lz + 0.02, 0.07, 0.07), (lx, ly, (top + lz) / 2), (0, -90, 0), coll, 60, 0.02))
    parts[-1].data.attributes["rope"].data.foreach_set("value", [1.0] * len(parts[-1].data.vertices))
    return parts


def void_panel(coll):
    """The black closure at the end of the tunnel, its edges sunk into the lining."""
    sw, sh, _ = tunnel_scale(TUNNEL["y1"])
    w, h = TUNNEL["w"] * sw + 0.1, TUNNEL["h"] * sh + 0.1
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector((2 * w, 0.1, h)), verts=bm.verts[:])
    o = new_object("void", bm, coll, (0, TUNNEL["y1"] - 0.08, h / 2 - 0.02))
    bake_transform(o)
    return o


# ---------------------------------------------------------------- hand-painted bake
class Nodes:
    def __init__(self, mat):
        mat.use_nodes = True
        self.nt = mat.node_tree
        for n in list(self.nt.nodes):
            self.nt.nodes.remove(n)
        self.out = self.nt.nodes.new("ShaderNodeOutputMaterial")

    def new(self, kind, **inputs):
        n = self.nt.nodes.new(kind)
        for k, v in inputs.items():
            if isinstance(v, bpy.types.NodeSocket):
                self.nt.links.new(v, n.inputs[k])
            else:
                n.inputs[k].default_value = v
        return n

    def attr(self, name, out="Fac"):
        n = self.nt.nodes.new("ShaderNodeAttribute")
        n.attribute_name = name
        return n.outputs[out]

    def math(self, op, a, b=0.0, clamp=False):
        n = self.nt.nodes.new("ShaderNodeMath")
        n.operation, n.use_clamp = op, clamp
        for i, v in enumerate((a, b)):
            if isinstance(v, bpy.types.NodeSocket):
                self.nt.links.new(v, n.inputs[i])
            else:
                n.inputs[i].default_value = v
        return n.outputs[0]

    def remap(self, v, a, b, c=0.0, d=1.0):
        n = self.new("ShaderNodeMapRange", Value=v)
        n.inputs[1].default_value, n.inputs[2].default_value = a, b
        n.inputs[3].default_value, n.inputs[4].default_value = c, d
        return n.outputs[0]

    def mix(self, a, b, f, blend="MIX"):
        n = self.nt.nodes.new("ShaderNodeMix")
        n.data_type, n.blend_type, n.clamp_result = "RGBA", blend, True
        for key, v in (("Factor", f), ("A", a), ("B", b)):
            sock = n.inputs[key] if key == "Factor" else next(s for s in n.inputs if s.name == key and s.type == "RGBA")
            if isinstance(v, bpy.types.NodeSocket):
                self.nt.links.new(v, sock)
            else:
                sock.default_value = (srgb(v) + (1,)) if isinstance(v, tuple) else v
        return next(s for s in n.outputs if s.type == "RGBA")

    def ramp(self, v, stops):
        n = self.nt.nodes.new("ShaderNodeValToRGB")
        self.nt.links.new(v, n.inputs[0])
        els = n.color_ramp.elements
        while len(els) < len(stops):
            els.new(0.5)
        for e, (pos, col) in zip(els, stops):
            e.position, e.color = pos, srgb(col) + (1,)
        return n.outputs[0]

    def noise(self, vec, scale, detail=2.0, rough=0.5, distortion=0.0):
        return self.new("ShaderNodeTexNoise", Vector=vec, Scale=scale, Detail=detail, Roughness=rough,
                        Distortion=distortion).outputs["Fac"]

    def emit(self, col):
        e = self.new("ShaderNodeEmission", Color=col, Strength=1.0)
        self.nt.links.new(e.outputs[0], self.out.inputs["Surface"])


def painted_rock_material():
    m = bpy.data.materials.new("m_src_mine_rock")
    N = Nodes(m)
    geo = N.nt.nodes.new("ShaderNodeNewGeometry")
    pos = geo.outputs["Position"]
    nz = N.new("ShaderNodeSeparateXYZ", Vector=geo.outputs["Normal"]).outputs["Z"]
    h, rnd = N.attr("h"), N.attr("rnd")
    # value: each boulder lighter toward its top, faces turned up lighter, a tone per boulder so neighbours read apart;
    # only very broad, quiet variation across the outcrop (Allen 2026-10-20: no cloudy mottling)
    light = N.math("ADD", N.math("MULTIPLY", h, 0.3), N.math("MULTIPLY", nz, 0.4))
    light = N.math("ADD", light, N.math("MULTIPLY", N.math("SUBTRACT", rnd, 0.5), 0.28))
    broad = N.noise(pos, 0.15, 0.0)
    light = N.math("ADD", light, N.math("MULTIPLY", N.math("SUBTRACT", broad, 0.5), 0.18))
    light = N.math("ADD", light, 0.18, clamp=True)
    col = N.ramp(light, [(0.0, (0.15, 0.17, 0.22)), (0.45, (0.31, 0.34, 0.40)),
                         (0.8, (0.47, 0.51, 0.55)), (1.0, (0.60, 0.64, 0.65))])
    col = N.mix(col, N.mix((0.94, 0.97, 1.0), (1.0, 0.98, 0.93), rnd), 1.0, "MULTIPLY")
    # restrained painted variation (Allen 2026-10-20): soft warm/cool drift, then separate blue-grey, warm-grey and
    # muted green patches that each land on only some faces; darker faces turned down and darker feet
    patch = N.remap(N.noise(pos, 0.45, 0.0), 0.36, 0.64)
    col = N.mix(col, N.mix((0.94, 0.98, 1.05), (1.05, 1.0, 0.93), patch), 1.0, "MULTIPLY")

    def patches(offset, scale, lo, hi):
        p = N.new("ShaderNodeMapping", Vector=pos, Location=offset).outputs[0]
        return N.remap(N.noise(p, scale, 0.0), lo, hi)

    # broad cool-grey and warm-grey patches, big enough to sit within a single rock and shift across it softly
    col = N.mix(col, (0.9, 0.96, 1.08), N.math("MULTIPLY", patches((17.3, 4.1, 9.7), 0.25, 0.45, 0.7), 0.85), "MULTIPLY")
    col = N.mix(col, (1.08, 1.02, 0.92), N.math("MULTIPLY", patches((-6.2, 13.8, 2.9), 0.25, 0.45, 0.7), 0.85), "MULTIPLY")
    green = N.math("MULTIPLY", patches((3.3, -9.1, 21.4), 0.5, 0.62, 0.74), N.remap(nz, -0.2, 0.6), clamp=True)
    col = N.mix(col, (0.36, 0.42, 0.31), N.math("MULTIPLY", green, 0.15))
    col = N.mix(col, (0.08, 0.09, 0.13), N.math("MULTIPLY", N.remap(nz, 0.05, -0.6), 0.65))
    col = N.mix(col, (0.10, 0.11, 0.15), N.math("MULTIPLY", N.remap(h, 0.35, 0.0), 0.3))
    # soft key light: faces turned toward it (above, front left), near each boulder's top
    key = N.nt.nodes.new("ShaderNodeVectorMath")
    key.operation = "DOT_PRODUCT"
    N.nt.links.new(geo.outputs["Normal"], key.inputs[0])
    key.inputs[1].default_value = Vector((-0.35, -0.45, 0.82)).normalized()
    lit = N.math("MULTIPLY", N.remap(key.outputs["Value"], 0.68, 0.96), N.remap(h, 0.45, 0.9), clamp=True)
    col = N.mix(col, (0.68, 0.72, 0.71), N.math("MULTIPLY", lit, 0.4))
    # selective upper-edge highlights: where the bevel shader's rounded normal parts from the true one (the rounded
    # corners), only on upward-turned corners in each boulder's upper half; wide and soft, so no broken lines
    bev = N.new("ShaderNodeBevel", Radius=0.14)
    bev.samples = 8
    edge = N.nt.nodes.new("ShaderNodeVectorMath")
    edge.operation = "DOT_PRODUCT"
    N.nt.links.new(bev.outputs["Normal"], edge.inputs[0])
    N.nt.links.new(geo.outputs["Normal"], edge.inputs[1])
    bnz = N.new("ShaderNodeSeparateXYZ", Vector=bev.outputs["Normal"]).outputs["Z"]
    rim = N.math("MULTIPLY", N.remap(edge.outputs["Value"], 0.995, 0.93), N.remap(bnz, 0.25, 0.75), clamp=True)
    rim = N.math("MULTIPLY", rim, N.remap(h, 0.5, 0.85), clamp=True)
    col = N.mix(col, (0.74, 0.78, 0.76), N.math("MULTIPLY", rim, 0.5))
    # selective shoulder highlights: a soft band where an upturned face rolls toward the key light, high on the rock
    shoulder = N.math("MULTIPLY", N.math("MULTIPLY", N.remap(nz, 0.3, 0.6), N.remap(nz, 0.95, 0.78)),
                      N.math("MULTIPLY", N.remap(h, 0.55, 0.9), N.remap(key.outputs["Value"], 0.5, 0.85)), clamp=True)
    col = N.mix(col, (0.70, 0.74, 0.73), N.math("MULTIPLY", shoulder, 0.35))
    # sparse, irregular fractures: Voronoi cell edges on noise-distorted coordinates (wandering lines), their width and
    # darkness varying along them, faded in and out by a broad mask so each one tapers away
    wob = N.new("ShaderNodeTexNoise", Vector=pos, Scale=0.9, Detail=2.0).outputs["Color"]
    off = N.nt.nodes.new("ShaderNodeVectorMath")
    off.operation = "MULTIPLY_ADD"
    N.nt.links.new(wob, off.inputs[0])
    off.inputs[1].default_value = (0.7, 0.7, 0.7)
    N.nt.links.new(pos, off.inputs[2])
    vor = N.nt.nodes.new("ShaderNodeTexVoronoi")
    vor.feature = "DISTANCE_TO_EDGE"
    vor.inputs["Scale"].default_value = 0.5
    N.nt.links.new(off.outputs["Vector"], vor.inputs["Vector"])
    width = N.remap(N.noise(pos, 1.3, 0.0), 0.3, 0.7, 0.004, 0.028)
    line = N.math("SUBTRACT", 1.0, N.math("DIVIDE", vor.outputs["Distance"], width), clamp=True)
    depth = N.remap(N.noise(pos, 0.8, 0.0), 0.3, 0.7, 0.15, 0.45)                     # faint
    mask = N.remap(N.noise(N.new("ShaderNodeMapping", Vector=pos, Location=(8.1, 2.7, -5.5)).outputs[0], 0.6, 0.0), 0.6, 0.7)
    crack = N.math("MULTIPLY", N.math("MULTIPLY", line, depth), mask, clamp=True)
    col = N.mix(col, (0.11, 0.12, 0.16), crack)
    # crevices: dark blue-grey where rocks meet each other, the wood and the ground, darkest right in the contact
    ao = N.new("ShaderNodeAmbientOcclusion", Distance=0.7).outputs["AO"]
    col = N.mix(col, (0.07, 0.08, 0.12), N.math("MULTIPLY", N.remap(ao, 0.25, 0.9, 1.0, 0.0), 0.92))
    tight = N.new("ShaderNodeAmbientOcclusion", Distance=0.25).outputs["AO"]
    col = N.mix(col, (0.04, 0.05, 0.08), N.math("MULTIPLY", N.remap(tight, 0.35, 0.95, 1.0, 0.0), 0.85))
    # moss: a broad, faint green wash at the foot only
    z = N.new("ShaderNodeSeparateXYZ", Vector=pos).outputs["Z"]
    foot = N.math("MULTIPLY", N.remap(z, 0.8, 0.0), N.remap(N.noise(pos, 0.35, 0.0), 0.4, 0.6))
    col = N.mix(col, (0.30, 0.38, 0.22), N.math("MULTIPLY", foot, 0.35))
    # the tunnel lining sinks into darkness with depth
    col = N.mix(col, (0.02, 0.02, 0.03), N.remap(N.attr("depth"), 0.0, 0.55, 0.3, 0.98))
    N.emit(col)
    return m


def painted_wood_material():
    m = bpy.data.materials.new("m_src_mine_wood")
    N = Nodes(m)
    geo = N.nt.nodes.new("ShaderNodeNewGeometry")
    nz = N.new("ShaderNodeSeparateXYZ", Vector=geo.outputs["Normal"]).outputs["Z"]
    g, rnd, rope = N.attr("grain", "Vector"), N.attr("rnd"), N.attr("rope")
    # grain lines along each plank's long (local X) axis: stretch along X, wobbly bands across
    gs = N.new("ShaderNodeMapping", Vector=g, Scale=(0.25, 1.0, 1.0)).outputs[0]
    wave = N.new("ShaderNodeTexWave", Vector=gs, Scale=3.2, Distortion=6.0, Detail=1.5)
    wave.bands_direction = "Y"
    lines = N.remap(wave.outputs["Fac"], 0.0, 0.3, 1.0, 0.0)
    light = N.math("ADD", N.math("MULTIPLY", nz, 0.25), N.math("MULTIPLY", N.math("SUBTRACT", rnd, 0.5), 0.5))
    light = N.math("ADD", light, N.math("MULTIPLY", N.math("SUBTRACT", N.noise(gs, 2.0, 1.0), 0.5), 0.4))
    light = N.math("ADD", light, 0.5, clamp=True)
    col = N.ramp(light, [(0.0, (0.34, 0.19, 0.10)), (0.5, (0.54, 0.33, 0.17)), (1.0, (0.74, 0.50, 0.28))])
    col = N.mix(col, (0.26, 0.14, 0.07), N.math("MULTIPLY", lines, 0.7))
    # rope: straw colour with a diagonal twist stripe
    twist = N.math("SINE", N.math("MULTIPLY", N.math("ADD", N.new("ShaderNodeSeparateXYZ", Vector=g).outputs["X"],
                                                     N.new("ShaderNodeSeparateXYZ", Vector=g).outputs["Y"]), 22.0))
    rope_col = N.mix((0.84, 0.70, 0.45), (0.56, 0.42, 0.24), N.remap(twist, -0.2, 0.6))
    col = N.mix(col, rope_col, rope)
    edge = N.math("MULTIPLY", N.remap(geo.outputs["Pointiness"], 0.5, 0.56), N.remap(nz, -0.3, 0.5), clamp=True)
    col = N.mix(col, (0.95, 0.76, 0.48), N.math("MULTIPLY", edge, 0.6))
    ao = N.new("ShaderNodeAmbientOcclusion", Distance=0.8).outputs["AO"]
    col = N.mix(col, (0.16, 0.09, 0.05), N.math("MULTIPLY", N.remap(ao, 0.3, 0.95, 1.0, 0.0), 0.8))
    # inside the tunnel the timber sinks into darkness with depth
    p = N.new("ShaderNodeSeparateXYZ", Vector=geo.outputs["Position"]).outputs
    inside = N.math("MULTIPLY", N.math("LESS_THAN", N.math("ABSOLUTE", p["X"]), TUNNEL["w"] + 0.1),
                    N.math("LESS_THAN", p["Z"], TUNNEL["h"] + 0.05))
    deep = N.math("MULTIPLY", inside, N.remap(p["Y"], TUNNEL["y0"] + 0.3, TUNNEL["y1"] - 0.6, 0.0, 0.95))
    col = N.mix(col, (0.03, 0.02, 0.02), deep)
    N.emit(col)
    return m


def bake(sc, targets):
    """targets: {object: (source material, image name)}. Bakes the emission (the painted colour) of each into its own
    image, with everything else (and a ground plane) visible so AO darkens the contacts."""
    os.makedirs(TEX, exist_ok=True)
    gm = bpy.data.meshes.new("BakeGround")
    gm.from_pydata([(-40, -40, 0), (40, -40, 0), (40, 40, 0), (-40, 40, 0)], [], [(0, 1, 2, 3)])
    ground = bpy.data.objects.new("BakeGround", gm)
    sc.collection.objects.link(ground)
    sc.render.engine = "CYCLES"
    sc.cycles.samples, sc.cycles.device = 32, "CPU"
    out = {}
    for o, (src, name) in targets.items():
        o.data.materials.clear()
        o.data.materials.append(src)
    for o, (src, name) in targets.items():
        # baked at twice the size and scaled down (antialiased island edges), margins filled from the face across each
        # seam rather than smeared outward: no serrated pale lines where a highlight meets a UV seam
        img = bpy.data.images.new(name, 2 * TEX_SIZE, 2 * TEX_SIZE, alpha=False)
        node = src.node_tree.nodes.new("ShaderNodeTexImage")
        node.image = img
        src.node_tree.nodes.active = node
        with bpy.context.temp_override(object=o, active_object=o, selected_objects=[o], selected_editable_objects=[o]):
            bpy.ops.object.bake(type="EMIT", use_clear=True, margin=TEX_SIZE // 32, margin_type="ADJACENT_FACES")
        img.scale(TEX_SIZE, TEX_SIZE)
        img.filepath_raw = os.path.join(TEX, f"{name}.png")
        img.file_format = "PNG"
        img.save()
        src.node_tree.nodes.remove(node)
        out[o] = img
    bpy.data.objects.remove(ground)
    for o, img in out.items():
        src = o.data.materials[0]
        m = bpy.data.materials.new(img.name.replace("mine_cave_", "m_mine_cave_"))
        m.use_nodes = True
        b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
        t = m.node_tree.nodes.new("ShaderNodeTexImage")
        t.image = img
        m.node_tree.links.new(t.outputs["Color"], b.inputs["Base Color"])
        b.inputs["Roughness"].default_value = 0.9
        o.data.materials.clear()
        o.data.materials.append(m)
        bpy.data.materials.remove(src)
        for a in ("h", "rnd", "grain", "rope", "depth"):   # bake-only
            if a in o.data.attributes:
                o.data.attributes.remove(o.data.attributes[a])


# ---------------------------------------------------------------- review
def review(sc):
    os.makedirs(REVIEW, exist_ok=True)
    for eng in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        try:
            sc.render.engine = eng
            break
        except TypeError:
            pass
    sc.view_settings.view_transform = "Standard"
    w = sc.world
    w.use_nodes = True
    bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND")
    sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN"))
    sun.rotation_euler = (math.radians(50), 0, math.radians(-35))
    sc.collection.objects.link(sun)
    lamp = bpy.data.objects.new("Lantern", bpy.data.lights.new("Lantern", "POINT"))
    lamp.data.color = (1.0, 0.62, 0.3)
    lamp.location = (LANTERN[0], LANTERN[1], LANTERN[2] - 0.45)
    sc.collection.objects.link(lamp)
    gme = bpy.data.meshes.new("Ground")
    gme.from_pydata([(-40, -40, -0.01), (40, -40, -0.01), (40, 40, -0.01), (-40, 40, -0.01)], [], [(0, 1, 2, 3)])
    g = bpy.data.objects.new("Ground", gme)
    gm = bpy.data.materials.new("m_review_ground")
    gm.use_nodes = True
    gb = next(n for n in gm.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    gme.materials.append(gm)
    sc.collection.objects.link(g)
    cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = 1400, 1000
    # (direction from target, distance, target, lighting)
    shots = {"ref_angle": ((1.0, -1.2, 0.8), 28, (0, 2.6, 2.6), "day"),
             "clay": ((1.0, -1.2, 0.8), 28, (0, 2.6, 2.6), "clay"),
             "front": ((0, -1, 0.3), 24, (0, 2.4, 2.8), "day"),
             "side": ((1, -0.1, 0.35), 27, (0, 2.6, 2.8), "day"),
             "clay_front": ((0, -1, 0.3), 24, (0, 2.4, 2.8), "clay"),
             "clay_side": ((1, -0.1, 0.35), 27, (0, 2.6, 2.8), "clay"),
             "mouth": ((0.25, -1, 0.2), 12, (0.3, -1.0, 1.8), "day"),
             "right_close": ((0.9, -1.0, 0.35), 11, (3.3, -1.2, 2.4), "day"),
             "night": ((1.0, -1.2, 0.8), 28, (0, 2.6, 2.6), "night")}
    out = []
    mats = {o: o.data.materials[0] for o in sc.objects if o.type == "MESH" and o.data.materials and o is not g}
    clay = bpy.data.materials.new("m_review_clay")
    clay.use_nodes = True
    next(n for n in clay.node_tree.nodes if n.type == "BSDF_PRINCIPLED").inputs["Base Color"].default_value = srgb((0.55, 0.55, 0.55)) + (1,)
    for name, (d, dist, target, light) in shots.items():
        night = light == "night"
        bg.inputs[0].default_value = (srgb((0.05, 0.06, 0.09)) if night else srgb((0.82, 0.82, 0.84))) + (1,)
        bg.inputs[1].default_value = 0.6 if night else 0.7
        gb.inputs["Base Color"].default_value = (srgb((0.22, 0.16, 0.11)) if night else srgb((0.72, 0.74, 0.78))) + (1,)
        sun.data.energy = 0.25 if night else 2.4
        lamp.data.energy = 220 if night else 0
        for o, m in mats.items():
            o.data.materials[0] = clay if light == "clay" else m
        cam.data.lens = 50
        t = Vector(target)
        cam.location = t + Vector(d).normalized() * dist
        cam.rotation_euler = (t - cam.location).to_track_quat("-Z", "Y").to_euler()
        sc.render.filepath = os.path.join(REVIEW, f"mine_cave_{name}.png")
        bpy.ops.render.render(write_still=True)
        out.append(sc.render.filepath)
    for o, m in mats.items():
        o.data.materials[0] = m
    for ob in (sun, lamp, g, cam):
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
    coll = bpy.data.collections.new("MineCave")
    sc.collection.children.link(coll)
    root = bpy.data.objects.new("MineCave", None)
    coll.objects.link(root)
    rocks = [boulder(f"Boulder{i}", *b[:3], coll, *b[3:]) for i, b in enumerate(BOULDERS)]
    wood = portal(coll)
    void = void_panel(coll)
    t = TUNNEL
    cuts = 0
    for o in rocks:                 # one clean convex shell at a time; the joined outcrop overlaps itself
        if any(abs(v.co.x) < t["w"] + t["wall"] and POST_Y - 0.3 < v.co.y < t["y1"] + 0.4 and v.co.z < t["h"] + t["wall"]
               for v in o.data.vertices):
            clear_tunnel(o, coll, cuts)
            cuts += 1
    rocks = [o for o in rocks if len(o.data.vertices) or bpy.data.objects.remove(o)]
    # the mouth and the cart run in front of it stay clear of rock
    blocked = [tuple(round(c, 2) for c in v.co) for o in rocks for v in o.data.vertices
               if abs(v.co.x) < OPENING["x"] and 0 < v.co.z < OPENING["z"] and v.co.y < POST_Y]
    in_awning = [tuple(round(c, 2) for c in v.co) for o in rocks for v in o.data.vertices
                 if abs(v.co.x) < AWNING["x"] and AWNING["y"][0] < v.co.y < AWNING["y"][1]
                 and AWNING["z"][0] < v.co.z < AWNING["z"][1]]
    rocks.append(tunnel_lining(coll))
    zfight = sorted(bs.zfight_check())
    rocks = join(rocks, "Rocks")
    wood = join(wood, "Wood")
    finish(rocks, 40)
    finish(wood, 50)
    finish(void, 30)
    unwrap(rocks, 0.006, 72)        # bevel strips stay on their faces' islands (no seams along the edges)
    unwrap(wood)
    unwrap(void)
    vm = bpy.data.materials.new("m_mine_cave_void")
    vm.use_nodes = True
    next(n for n in vm.node_tree.nodes if n.type == "BSDF_PRINCIPLED").inputs["Base Color"].default_value = srgb((0.02, 0.02, 0.03)) + (1,)
    void.data.materials.append(vm)
    bake(sc, {rocks: (painted_rock_material(), "mine_cave_rocks"), wood: (painted_wood_material(), "mine_cave_wood")})
    for o in (rocks, wood, void):
        o.parent = root
    report = {"triangles": {o.name: len(o.data.polygons) for o in (rocks, wood, void)},
              "zfight_pairs": zfight, "rock_verts_in_opening": blocked[:10], "rock_verts_in_awning": in_awning[:10],
              "bounds": {o.name: [[round(min(v.co[k] for v in o.data.vertices), 2) for k in range(3)],
                                  [round(max(v.co[k] for v in o.data.vertices), 2) for k in range(3)]]
                         for o in (rocks, wood, void)}}
    try:
        report["qa"] = skill("qa_check", "blender-asset-qa").run(objects=[rocks.name, wood.name, void.name], profile="roblox")
    except Exception as e:  # noqa: BLE001 - record and carry on, the review still runs
        report["qa_error"] = repr(e)
    report["renders"] = review(sc)
    try:
        report["export"] = skill("export_asset", "blender-export-pipelines").run(
            preset="roblox", collection="MineCave", out=os.path.join(HERE, "Mine_Cave.fbx"), batch=False, no_anim=True)
    except Exception as e:  # noqa: BLE001
        report["export_error"] = repr(e)
    bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, "MineCave.blend"))
    with open(os.path.join(HERE, "qa.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str)
    print("MINE_CAVE_DONE", json.dumps(report["triangles"]), "zfight", len(zfight), "blocked", len(blocked))


main()

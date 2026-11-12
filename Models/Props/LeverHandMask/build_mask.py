# The lever hand's mask, v3 (2026-11-07). Allen's notes so far: "how hard would it be to make our mask look like this",
# "Lever hand only"; v2: "the mask is not accurate. most importantly, the eyebrows", "also look at the eyes"; v3: "the
# eyes should be 3d balls, yours has too many rings. the eye is literally just white with a black ring and then white
# pupils. your eyebrows are too long and not thick. the mask doesnt look 3d. it shouldn't be low poly."
# Our own take on the hyottoko folk mask (not a copy of any show's character):
#   Face      - a smooth, high-resolution sculpted shell: a domed oval with raised cheeks, a brow ridge, a raised snout
#               running down the middle, soft eye sockets; a short rim turns back toward the head
#   EyeWhite  - two white eyeballs, half sunk in the sockets
#   EyeRing   - one thick black ring on each ball (the ball's white shows in its middle)
#   Brow      - short, thick, puffy brows angled down toward the middle, a curl at the outer end, hugging the face
#   Cheek     - red patches draped on the cheek bumps
#   Mouth, MouthHole - the pursed lips at the end of the snout; Nostril - a dot beside it
# Built in the lever hand's head space (head 1.32 studs): origin at the head's centre, front -Y (Roblox -Z), Z up.
# Studio welds each piece to the Head at this offset (the Face's bounding-box centre, printed below: (0, -0.6393, 0.06)),
# EyeWhite and EyeRing 0.07 further forward along the head's front (sunk as built, only the balls' middles showed).
# Run in Blender: exec(open(<this file>).read()). Writes LeverHandMask.fbx next to this file.
import math

import bmesh
import bpy
from mathutils import Vector

FESTIVAL = "C:/Users/Allen/Documents/Create Swords!/Models/Props/Festival/build_festival.py"
_src = open(FESTIVAL).read()
exec(_src[:_src.index("def export(name):")])
HERE = "C:/Users/Allen/Documents/Create Swords!/Models/Props/LeverHandMask"

A, B, C = 0.6, 0.22, 0.7      # the base dome's half width, depth and half height
CY, CZ = -0.56, 0.06           # its centre (forward of the head's centre so the shell clears the face)
EYES = [(s * 0.23, 0.13) for s in (-1, 1)]
CHEEKS = [(s * 0.37, -0.2) for s in (-1, 1)]


def g(x, z, cx, cz, sx, sz):
    return math.exp(-(((x - cx) / sx) ** 2 + ((z - cz) / sz) ** 2))


def relief(x, z):
    """How far the sculpted face stands out from the base dome at (x, z)."""
    r = 0.0
    for cx, cz in CHEEKS:
        r += 0.055 * g(x, z, cx, cz, 0.15, 0.13)                 # round cheeks
    for s in (-1, 1):
        r += 0.03 * g(x, z, s * 0.21, 0.34, 0.16, 0.06)          # brow ridge
    for cx, cz in EYES:
        r -= 0.03 * g(x, z, cx, cz, 0.12, 0.1)                   # sockets for the eyeballs
    # the snout: a ridge down the middle from between the eyes, fuller toward the mouth
    t = min(max((0.02 - z) / 0.34, 0.0), 1.0)
    if -0.36 < z < 0.08:
        r += (0.02 + 0.05 * t) * math.exp(-((x + 0.03 * t) / (0.045 + 0.03 * t)) ** 2)
    return r


def depth(x, z):
    """The face's front surface y at (x, z)."""
    u = 1 - (x / A) ** 2 - ((z - CZ) / C) ** 2
    return CY - B * math.sqrt(max(u, 0.0)) - relief(x, z) * min(1.0, max(u, 0.0) * 6)  # relief fades at the rim


def surface(x, z):
    """Point and outward normal of the sculpted face at (x, z)."""
    e = 0.002
    p = Vector((x, depth(x, z), z))
    tx = Vector((2 * e, depth(x + e, z) - depth(x - e, z), 0))
    tz = Vector((0, depth(x, z + e) - depth(x, z - e), 2 * e))
    n = tz.cross(tx).normalized()
    if n.y > 0:
        n = -n
    return p, n


def to_obj(bm, name):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    return o


def ellipse_grid(bm, cx, cz, rx, rz, rings, segs, at):
    """Verts in polar rings over an ellipse, placed by at(x, z); returns the faces' vertex rows."""
    centre = bm.verts.new(at(cx, cz))
    rows = []
    for i in range(1, rings + 1):
        k = (i / rings) ** 0.85
        rows.append([bm.verts.new(at(cx + rx * k * math.cos(2 * math.pi * j / segs), cz + rz * k * math.sin(2 * math.pi * j / segs)))
                     for j in range(segs)])
    for j in range(segs):
        bm.faces.new((centre, rows[0][j], rows[0][(j + 1) % segs]))
    for r0, r1 in zip(rows, rows[1:]):
        for j in range(segs):
            jj = (j + 1) % segs
            bm.faces.new((r0[j], r1[j], r1[jj], r0[jj]))
    return rows


def face_shell(rings=48, segs=112):
    bm = bmesh.new()
    rows = ellipse_grid(bm, 0, CZ, A * 0.995, C * 0.995, rings, segs, lambda x, z: surface(x, z)[0])
    rim = [bm.verts.new((v.co.x * 0.97, v.co.y + 0.12, CZ + (v.co.z - CZ) * 0.97)) for v in rows[-1]]
    for j in range(segs):
        jj = (j + 1) % segs
        bm.faces.new((rows[-1][j], rim[j], rim[jj], rows[-1][jj]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return to_obj(bm, "Face")


def patch(cx, cz, rx, rz, lift, rings=8, segs=48):
    """A painted patch draped on the face, `lift` proud, following every bump."""
    def at(x, z):
        p, n = surface(x, z)
        return p + n * lift
    bm = bmesh.new()
    ellipse_grid(bm, cx, cz, rx, rz, rings, segs, at)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    for f in bm.faces:
        if f.normal.y > 0:
            f.normal_flip()
    return to_obj(bm, "patch")


# the +x brow's outline (x, z): short, inner end low, rising to a curl at the outer end, a few tufts on top
BROW = [(0.05, 0.27), (0.12, 0.275), (0.19, 0.29), (0.26, 0.315), (0.31, 0.345), (0.335, 0.38),
        (0.33, 0.43), (0.305, 0.455), (0.28, 0.44), (0.29, 0.41), (0.27, 0.43), (0.235, 0.45),
        (0.215, 0.425), (0.17, 0.44), (0.15, 0.415), (0.10, 0.425), (0.08, 0.395), (0.045, 0.38)]


def brow(sign):
    """A thick, puffy brow: the outline filled, subdivided, each vertex lifted off the face most in the middle."""
    pts = [(sign * x, 0.27 + (z - 0.27) * 1.35) for x, z in BROW]  # 35% taller: chunkier
    if sign < 0:
        pts = pts[::-1]
    bm = bmesh.new()
    f = bm.faces.new([bm.verts.new((x, 0, z)) for x, z in pts])
    bmesh.ops.triangulate(bm, faces=[f])
    for _ in range(3):
        bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=1, use_grid_fill=True)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    edge = [v for v in bm.verts if any(e.is_boundary for e in v.link_edges)]
    edge_set = set(edge)
    puff = {}
    for v in bm.verts:
        dmin = 0.0 if v in edge_set else min((v.co - b.co).length for b in edge)
        puff[v] = 0.012 + 0.08 * min(dmin / 0.06, 1.0) ** 0.6
    for _ in range(6):  # even out the cushion (the uneven fill made it stringy)
        new = {}
        for v in bm.verts:
            if v in edge_set:
                new[v] = puff[v]
            else:
                nb = [e.other_vert(v) for e in v.link_edges]
                new[v] = 0.5 * puff[v] + 0.5 * sum(puff[u] for u in nb) / len(nb)
        puff = new
    for v in bm.verts:
        p, n = surface(v.co.x, v.co.z)
        v.co = p + n * puff[v]
    back = {}
    for v in edge:
        p, n = surface(v.co.x, v.co.z)
        back[v] = bm.verts.new(p - n * 0.01)
    for e in [e for e in bm.edges if e.is_boundary]:
        a, b = e.verts
        bm.faces.new((a, b, back[b], back[a]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return to_obj(bm, "brow")


def build():
    coll = fresh_collection("LeverHandMask")
    P = {}
    P["Face"] = join([face_shell()], "Face", coll)
    whites, rings = [], []
    R, ring_r = 0.155, 0.095
    for ex, ez in EYES:
        p, n = surface(ex, ez)
        c = p - n * 0.05  # half sunk in the socket
        bpy.ops.mesh.primitive_uv_sphere_add(segments=40, ring_count=24, radius=R, location=c)
        whites.append(bpy.context.active_object)
        d = math.sqrt(R * R - ring_r * ring_r) + 0.004  # the ring sits on the ball's front
        bpy.ops.mesh.primitive_torus_add(major_radius=ring_r, minor_radius=0.032, major_segments=48, minor_segments=14,
                                         location=c + n * d)
        t = bpy.context.active_object
        t.rotation_mode = "QUATERNION"
        t.rotation_quaternion = n.to_track_quat("Z", "Y")
        rings.append(t)
    P["EyeWhite"] = join(whites, "EyeWhite", coll)
    P["EyeRing"] = join(rings, "EyeRing", coll)
    P["Brow"] = join([brow(-1), brow(1)], "Brow", coll)
    P["Cheek"] = join([patch(cx, cz, 0.12, 0.11, 0.004) for cx, cz in CHEEKS], "Cheek", coll)
    p, n = surface(-0.03, -0.33)  # the pursed lips at the end of the snout
    lips = cyl(0.075, 0.1, (0, 0, 0), verts=32, r2=0.06)
    lips.rotation_mode = "QUATERNION"
    lips.rotation_quaternion = n.to_track_quat("Z", "Y")
    lips.location = p + n * 0.035
    P["Mouth"] = join([lips], "Mouth", coll)
    hole = cyl(0.03, 0.02, (0, 0, 0), verts=20)
    hole.rotation_mode = "QUATERNION"
    hole.rotation_quaternion = n.to_track_quat("Z", "Y")
    hole.location = p + n * 0.087
    P["MouthHole"] = join([hole], "MouthHole", coll)
    q, m = surface(-0.09, -0.1)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=10, radius=0.022, location=q + m * 0.005)
    P["Nostril"] = join([bpy.context.active_object], "Nostril", coll)
    for o in P.values():  # smooth, not faceted
        for f in o.data.polygons:
            f.use_smooth = True
    return coll, P


coll, PARTS = build()
for n, o in PARTS.items():
    c = sum((o.matrix_world @ Vector(b) for b in o.bound_box), Vector()) / 8
    print(n, [round(v, 4) for v in c], sum(len(p.vertices) - 2 for p in o.data.polygons))

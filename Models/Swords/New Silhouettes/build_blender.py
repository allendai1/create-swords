"""Build the 22 new silhouette swords in Blender from prep.py's output.

Run inside Blender:  SRC = r'<prep out dir>'; exec(open(r'<this file>').read())
Each sword is an Empty <id> with <id>_Blade / _Guard / _Grip / _Pommel children.
Frame: blade up +Z, width X, thickness Y (front faces -Y), origin at the grip's middle
(the game's Handle frame). 1 unit = 1 stud; K studs per sheet pixel (a 450 px sword = 5 studs).
Each part is a closed shell: the front is a height field over a constrained Delaunay
triangulation of the traced outline (+ the bevel line + an interior grid), the back mirrors it,
and a thin wall joins them round every outline loop (holes included).
v2 (2026-11-10): inside tests and heights come from the outline itself (even-odd test, exact distance
to its edges), not from a pixel map, so bevels and rounded rims follow the smoothed outline; only the
grip's round section still comes from prep.py's map."""
import bpy, bmesh, json, os, math
import numpy as np
from mathutils.geometry import delaunay_2d_cdt
from mathutils import Vector

K = 5.0 / 450
RIM = {'Blade': 0.35, 'Guard': 0.9, 'Grip': 1.0, 'Pommel': 1.0}   # half wall height, px
GRID = {'Blade': 4.0, 'Guard': 3.0, 'Grip': 2.5, 'Pommel': 2.5}   # interior point spacing, px
SMOOTH_ITERS = 6   # height relaxation passes on guards and pommels
ORDER = ['S01', 'S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'S10', 'S11', 'S12',
         'EclipseFang', 'Tidebreaker', 'Crownsplitter', 'Mothwing', 'Lockjaw',
         'Cometspine', 'Gravebell', 'OrchidEdge', 'IronAnchor', 'Riftkey', 'Inversion']
MATS = {'Blade': ((0.80, 0.80, 0.82), 1.0, 0.28), 'Guard': ((0.761, 0.445, 0.045), 0.9, 0.3),
        'Grip': ((0.06, 0.03, 0.02), 0.0, 0.85), 'Pommel': ((0.761, 0.445, 0.045), 0.9, 0.3)}


def box_uv(bm):
    """UVs inside 0-1 (2026-11-11; the 22 got theirs afterwards, 2026-11-10): Models/Stations/build_stations.py auto_uv's
    box projection, scaled to the part's largest side, so Wood, Fabric and Metal show on the hilt."""
    uv = bm.loops.layers.uv.verify()
    lo = [min(v.co[k] for v in bm.verts) for k in range(3)]
    span = max(max(v.co[k] for v in bm.verts) - lo[k] for k in range(3)) or 1.0
    bm.normal_update()
    for f in bm.faces:
        ax = max(range(3), key=lambda k: abs(f.normal[k]))
        a, b = [k for k in range(3) if k != ax]
        for l in f.loops:
            l[uv].uv = ((l.vert.co[a] - lo[a]) / span, (l.vert.co[b] - lo[b]) / span)


def material(part):
    name = 'NS_' + part
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    col, met, rough = MATS[part]
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Metallic'].default_value = met
    b.inputs['Roughness'].default_value = rough
    m.diffuse_color = (*col, 1)
    return m


def bilinear(a, x, y):
    H, W = a.shape
    x = min(max(x, 0), W - 1.001); y = min(max(y, 0), H - 1.001)
    i, j = int(y), int(x); fy, fx = y - i, x - j
    return float((a[i, j] * (1 - fx) + a[i, j + 1] * fx) * (1 - fy) + (a[i + 1, j] * (1 - fx) + a[i + 1, j + 1] * fx) * fy)


def segments(loops):
    A = np.concatenate([np.array(l) for l in loops]); B = np.concatenate([np.roll(np.array(l), -1, 0) for l in loops])
    return A, B


def dist_to(P, A, B):
    """Distance from each point to the nearest outline edge (px)."""
    out = np.empty(len(P))
    AB = B - A; L2 = np.maximum((AB ** 2).sum(1), 1e-12)
    for s in range(0, len(P), 2048):
        p = P[s:s + 2048, None, :]
        t = np.clip(((p - A) * AB).sum(2) / L2, 0, 1)
        q = A + t[..., None] * AB
        out[s:s + 2048] = np.sqrt(((p - q) ** 2).sum(2).min(1))
    return out


def inside(P, A, B):
    """Even-odd test against every loop at once (holes stay out)."""
    out = np.zeros(len(P), bool)
    for s in range(0, len(P), 2048):
        x, y = P[s:s + 2048, 0:1], P[s:s + 2048, 1:2]
        cond = (A[:, 1] > y) != (B[:, 1] > y)
        xc = A[:, 0] + (y - A[:, 1]) * (B[:, 0] - A[:, 0]) / np.where(B[:, 1] - A[:, 1] == 0, 1e-12, B[:, 1] - A[:, 1])
        out[s:s + 2048] = ((cond & (x < xc)).sum(1) % 2) == 1
    return out


def rounded(d, r):           # quarter-circle rise over r px, then flat
    t = np.clip(d / r, 0, 1); return np.sqrt(1 - (1 - t) ** 2)


def build_part(name, part, P, grip, up, axis, zc):
    loops = part['loops']
    if not loops: return None
    A, B = segments(loops)
    pts, edges, outer = [], [], set()
    def add_loop(loop, is_outer):
        base = len(pts)
        for p in loop: pts.append(Vector(p))
        n = len(loop)
        for k in range(n):
            edges.append((base + k, base + (k + 1) % n))
            if is_outer: outer.add(base + k)
    for lp in loops: add_loop(lp, True)
    for lp in part.get('inner', []): add_loop(lp, False)
    # interior grid, kept clear of the outline
    s = GRID[name]
    xs = [p.x for p in pts]; ys = [p.y for p in pts]
    gx, gy = np.meshgrid(np.arange(min(xs) + s / 2, max(xs), s), np.arange(min(ys) + s / 2, max(ys), s))
    G = np.stack([gx.ravel(), gy.ravel()], 1)
    if len(G):
        keep = inside(G, A, B)
        G = G[keep]
        G = G[dist_to(G, A, B) > 0.45 * s]
        # and clear of the bevel line
        if part.get('inner'):
            Ai, Bi = segments(part['inner'])
            G = G[dist_to(G, Ai, Bi) > 0.3 * s]
        for x, y in G: pts.append(Vector((float(x), float(y))))
    vco, eo, fo, ov, oe, of = delaunay_2d_cdt(pts, edges, [], 0, 1e-4, True)
    on_outline = [any(o in outer for o in orig) for orig in ov]
    C = np.array([[sum(vco[v].x for v in f) / len(f), sum(vco[v].y for v in f) / len(f)] for f in fo])
    tris = [f for f, ok in zip(fo, inside(C, A, B)) if ok] if len(C) else []
    if not tris: return None
    used = sorted({v for f in tris for v in f}); idx = {v: k for k, v in enumerate(used)}
    V = np.array([[vco[v].x, vco[v].y] for v in used])
    d = dist_to(V, A, B)
    if name == 'Blade':
        h = P['blade_t'] * np.clip(d / P['blade_bevel'], 0, 1)
    elif name == 'Guard':
        h = P['guard_t'] * rounded(d, P['guard_round'])
    elif name == 'Pommel':
        r = min(P['pommel_round'], float(d.max()))
        h = r * rounded(d, r)
    else:
        h = np.array([bilinear(grip, x * up, y * up) for x, y in V])
    rim = RIM[name]
    zs = [rim if on_outline[v] else max(rim, float(h[k])) for k, v in enumerate(used)]
    if name in ('Guard', 'Pommel'):
        # the distance field ridges along thin pieces (a knuckle bow): relax the heights over the mesh, outline held
        nb = [set() for _ in used]
        for f in tris:
            a, b, c = (idx[v] for v in f)
            nb[a] |= {b, c}; nb[b] |= {a, c}; nb[c] |= {a, b}
        fixed = [on_outline[v] for v in used]
        for _ in range(SMOOTH_ITERS):
            zs = [z if fixed[k] or not nb[k] else 0.5 * z + 0.5 * sum(zs[j] for j in nb[k]) / len(nb[k]) for k, z in enumerate(zs)]
    bm = bmesh.new()
    front = [bm.verts.new(((vco[v].x - axis) * K, -zs[k] * K, (zc - vco[v].y) * K)) for k, v in enumerate(used)]
    back = [bm.verts.new(((vco[v].x - axis) * K, zs[k] * K, (zc - vco[v].y) * K)) for k, v in enumerate(used)]
    ecount = {}
    for f in tris:
        a, b, c = (idx[v] for v in f)
        for e in ((a, b), (b, c), (c, a)):
            ecount[tuple(sorted(e))] = ecount.get(tuple(sorted(e)), 0) + 1
        try:
            bm.faces.new((front[a], front[b], front[c]))
            bm.faces.new((back[c], back[b], back[a]))
        except ValueError:
            pass
    for (a, b), n in ecount.items():
        if n == 1:
            try: bm.faces.new((front[a], front[b], back[b], back[a]))
            except ValueError: pass
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    # where the outline pinches through one vertex, its wall edge carries 4 faces: split it
    pinch = [e for e in bm.edges if len(e.link_faces) > 2]
    if pinch: bmesh.ops.split_edges(bm, edges=pinch)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    box_uv(bm)
    bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    me.set_sharp_from_angle(angle=math.radians(40))
    return me


def build_all(SRC, coll_name='NewSilhouettes', ids=None):
    coll = bpy.data.collections.get(coll_name) or bpy.data.collections.new(coll_name)
    if coll.name not in bpy.context.scene.collection.children: bpy.context.scene.collection.children.link(coll)
    for o in list(coll.objects): bpy.data.objects.remove(o, do_unlink=True)
    report = {}
    for i, sid in enumerate(ids or ORDER):
        info = json.load(open(os.path.join(SRC, sid + '.json')))
        arr = np.load(os.path.join(SRC, sid + '.npz'))
        mt = info['meta']; be, gt, gb = mt['cuts']; zc = (gt + gb) / 2
        root = bpy.data.objects.new(sid, None); coll.objects.link(root)
        root.empty_display_size = 0.2
        root.location = ((i % 11) * 2.4, 0, -(i // 11) * 6.5)
        tri = 0
        grip = arr['Grip'].astype(np.float32) if 'Grip' in arr else None
        for name, part in info['parts'].items():
            me = build_part(name, part, info['P'], grip, info['up'], mt['axis'], zc)
            if me is None: continue
            me.materials.append(material(name))
            ob = bpy.data.objects.new(f'{sid}_{name}', me); coll.objects.link(ob); ob.parent = root
            tri += sum(len(p.vertices) - 2 for p in me.polygons)
        report[sid] = tri
    for m in list(bpy.data.meshes):
        if m.users == 0: bpy.data.meshes.remove(m)
    return report

# one sword on its own: COLL = 'Inversion'; IDS = ['Inversion'] before the exec
print(build_all(SRC, globals().get('COLL', 'NewSilhouettes'), globals().get('IDS')))

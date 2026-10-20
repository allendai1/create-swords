# Painted textures for the stations (ore stand style test + forge soot). Run after build_stations.py
# in the same namespace:
#   ns = {}; exec(build_stations.py, ns); exec(station_textures.py, ns)
#   ns["textured_ore_stand"](x, y); ns["forge_soot"]()
# Tileable 512 px PNGs whose average colour stays on the PAL swatch. UVs are box-projected at about
# one tile per 2 studs, with a different random offset and scale per part so neighbouring boards and
# stones never show the same marks. `Ore` stays a separate flat-colour part so a roll can recolour it.
import math
import os
import zlib
import numpy as np

TEX_DIR = r"C:\Users\Allen\Documents\Create Swords!\Models\Stations\Textures"
N = 512
TILE = 2.7  # studs per texture repeat; every part (max ~2.1 studs) then fits one tile, so UVs stay in 0-1


def _grid():
    y, x = np.mgrid[0:N, 0:N] / N
    return x, y


def _wrap(d):
    """Shortest distance on the tile (so every mark tiles)."""
    d = np.abs(d)
    return np.minimum(d, 1 - d)


def _shade(base, factor):
    return np.clip(np.asarray(base)[None, None, :] * factor[..., None], 0, 1)


def _blobs(rng, x, y, count, smin, smax):
    """Isotropic soft noise: wrapped gaussian blobs of mixed sizes and signs, in -1..1."""
    v = np.zeros_like(x)
    for _ in range(count):
        cx, cy = rng.uniform(0, 1, 2)
        s = rng.uniform(smin, smax)
        sx, sy = s * rng.uniform(0.75, 1.3), s * rng.uniform(0.75, 1.3)
        v += rng.choice((-1, 1)) * np.exp(-((_wrap(x - cx) / sx) ** 2 + (_wrap(y - cy) / sy) ** 2))
    return v / np.abs(v).max()


def wood(base, seed):
    """Grain runs along U (each board's long axis): soft bands, curved lines, tapered strokes, one knot."""
    rng = np.random.default_rng(seed)
    x, y = _grid()
    f = np.ones_like(x)
    # very soft broad bands
    f *= 1 + 0.035 * np.sin(2 * np.pi * (3 * y + 0.12 * np.sin(2 * np.pi * x + rng.uniform(0, 6))))
    # a knot, with the grain lines bowing around it
    kx, ky = rng.uniform(0.2, 0.8, 2)
    kdx, kdy = _wrap(x - kx), _wrap(y - ky)
    bow = 0.05 * np.exp(-((kdx / 0.09) ** 2)) * np.sign(0.5 - ((y - ky) % 1.0))
    # gently curved grain lines, thickening and thinning along their length
    for i in range(7):
        y0 = (i + rng.uniform(0.1, 0.9)) / 7
        fx, amp, ph = rng.integers(1, 3), rng.uniform(0.008, 0.025), rng.uniform(0, 6.28)
        path = y0 + amp * np.sin(2 * np.pi * fx * x + ph) + bow
        width = 0.004 + 0.0035 * (1 + np.sin(2 * np.pi * rng.integers(1, 3) * x + rng.uniform(0, 6.28)))
        f *= 1 - 0.12 * np.clip(1 - _wrap(y - path) / width, 0, 1) ** 0.5
    # occasional tapered strokes, darker or lighter
    for _ in range(9):
        xs, ys, L = rng.uniform(0, 1), rng.uniform(0, 1), rng.uniform(0.12, 0.3)
        t = ((x - xs) % 1.0) / L
        inside = t < 1
        w = 0.006 * np.sin(np.pi * np.clip(t, 0, 1))
        bend = 0.01 * np.sin(np.pi * np.clip(t, 0, 1))
        k = np.where(inside, np.clip(1 - _wrap(y - ys - bend) / np.maximum(w, 1e-4), 0, 1), 0) ** 0.5
        f *= 1 + rng.choice((-0.1, 0.07)) * k
    knot = np.sqrt((kdx / 0.03) ** 2 + (kdy / 0.018) ** 2)
    f[knot < 1] *= 0.78
    f[(knot > 1.35) & (knot < 1.7)] *= 0.9
    return _shade(base, f)


def stone(base, seed):
    """Soft, non-directional variation: mixed-size blobs and a few pits."""
    rng = np.random.default_rng(seed)
    x, y = _grid()
    v = 0.65 * _blobs(rng, x, y, 26, 0.05, 0.16) + 0.35 * _blobs(rng, x, y, 40, 0.02, 0.05)
    f = 1 + 0.065 * np.tanh(2.2 * v)  # painted plateaus with soft edges
    pits = rng.random((N, N)) < 0.0008
    for _ in range(2):
        pits = pits | np.roll(pits, 1, 0) | np.roll(pits, 1, 1)
    f[pits] *= 0.93
    return _shade(base, f)


def _pnoise(rng, x, y, freqs):
    v = np.zeros_like(x)
    for fx in freqs:
        for fy in freqs:
            if fx == fy == 0:
                continue
            v += rng.uniform(0.4, 1.0) / (abs(fx) + abs(fy)) * np.sin(2 * np.pi * (fx * x + fy * y) + rng.uniform(0, 6.28))
    return v / np.abs(v).max()


def iron(base, seed):
    """Restrained wear (approved 2026-10-19): a few lighter patches and short scratches."""
    rng = np.random.default_rng(seed)
    x, y = _grid()
    n = _pnoise(rng, x, y, (1, 2, 4))
    f = np.ones_like(n)
    f[n > 0.35] = 1.22
    f[n < -0.5] = 0.94
    for _ in range(14):
        x0, y0 = rng.uniform(0, 1, 2)
        ang, length = rng.uniform(0, np.pi), rng.uniform(0.05, 0.14)
        for t in np.linspace(0, length, 80):
            px, py = int((x0 + t * np.cos(ang)) * N) % N, int((y0 + t * np.sin(ang)) * N) % N
            f[py, px] = f[(py + 1) % N, px] = 1.5
    return _shade(base, f)


def soot():
    """RGBA soot: darkest just above the mouth, rising and fading, ragged at the edges. Not tiled."""
    rng = np.random.default_rng(5)
    x, y = _grid()  # y = 0 is the bottom of the soot area (mouth top)
    y = 1 - y
    spread = 0.22 + 0.18 * y                         # widens as it rises
    ragged = 0.08 * _blobs(rng, x, y, 30, 0.03, 0.08)
    a = np.exp(-(((x - 0.5) / spread) ** 2)) * np.clip(1.15 - (y - 0.15) * 1.5, 0, 1) + ragged
    a = np.clip(a, 0, 1) * 0.6                       # restrained: never past 60% opaque
    rgba = np.zeros((N, N, 4))
    rgba[..., :3] = (0.17, 0.13, 0.11)
    rgba[..., 3] = a
    return rgba


def save_png(name, rgb_or_rgba):
    os.makedirs(TEX_DIR, exist_ok=True)
    arr = rgb_or_rgba
    alpha = arr.shape[2] == 4
    if not alpha:
        arr = np.concatenate([arr, np.ones((N, N, 1))], axis=2)
    img = bpy.data.images.get(name) or bpy.data.images.new(name, N, N, alpha=alpha)
    img.pixels.foreach_set(arr[::-1].astype(np.float32).ravel())  # Blender rows run bottom-up
    img.filepath_raw = os.path.join(TEX_DIR, name + ".png")
    img.file_format = "PNG"
    img.save()
    return img


def tex_material(name, img, alpha=False):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Roughness"].default_value = 0.8
    t = next((n for n in nt.nodes if n.type == "TEX_IMAGE"), None) or nt.nodes.new("ShaderNodeTexImage")
    t.image = img
    nt.links.new(t.outputs["Color"], b.inputs["Base Color"])
    if alpha:
        nt.links.new(t.outputs["Alpha"], b.inputs["Alpha"])
        if hasattr(m, "surface_render_method"):
            m.surface_render_method = "BLENDED"
    return m


TEXTURES = {  # PAL key -> (texture name, painter)
    "wood":     ("ore_stand_wood", wood),
    "wood_dk":  ("ore_stand_wood_dark", wood),
    "cream":    ("ore_stand_stone", stone),
    "cream_dk": ("ore_stand_stone_dark", stone),
    "iron":     ("ore_stand_iron", iron),
    "iron_dk":  ("ore_stand_iron_dark", iron),
}


def box_uv(o, seed_name):
    """World-scale box projection; U follows the part's longest axis so grain runs along boards.
    Each part gets its own offset (and, for stone, scale) so marks don't repeat across neighbours."""
    import bmesh
    rng = np.random.default_rng(zlib.crc32(seed_name.encode()))
    off_u, off_v = rng.uniform(0, 1, 2)
    scale = rng.uniform(0.8, 1.25) if "Course" in o.name else rng.uniform(0.92, 1.08)
    me = o.data
    bm = bmesh.new()
    bm.from_mesh(me)
    uv = bm.loops.layers.uv.verify()
    dims = [max(v.co[k] for v in bm.verts) - min(v.co[k] for v in bm.verts) for k in range(3)]
    long_axis = max(range(3), key=lambda k: dims[k])
    off = o.matrix_local.translation
    for f in bm.faces:
        ax = max(range(3), key=lambda k: abs(f.normal[k]))
        a, b = [k for k in range(3) if k != ax]
        if b == long_axis:
            a, b = b, a
        for l in f.loops:
            p = l.vert.co + off
            l[uv].uv = (p[a] / (TILE * scale) + off_u, p[b] / (TILE * scale) + off_v)
    # move the part inside 0-1 (Roblox wants one tile), keeping a random placement that still fits
    us = [l[uv].uv.copy() for f in bm.faces for l in f.loops]
    lo_u, lo_v = min(u.x for u in us), min(u.y for u in us)
    span_u, span_v = max(u.x for u in us) - lo_u, max(u.y for u in us) - lo_v
    su, sv = rng.uniform(0, max(0.0, 1 - span_u)), rng.uniform(0, max(0.0, 1 - span_v))
    for f in bm.faces:
        for l in f.loops:
            l[uv].uv = (l[uv].uv.x - lo_u + su, l[uv].uv.y - lo_v + sv)
    bm.to_mesh(me)
    bm.free()


def textured_ore_stand(x, y, name="OreStand_Textured"):
    ore_stand(name, x, y, ore="ore")
    c = bpy.data.collections[name]
    mats = {}
    for i, (key, (tname, painter)) in enumerate(TEXTURES.items()):
        mats[key] = tex_material("TX_" + tname, save_png(tname, painter(PAL[key], seed=11 + i)))
    groups = {}
    for i, o in enumerate(list(c.objects)):
        if o.type != "MESH" or o.name.startswith("Ore"):
            continue
        key = o.data.materials[0].name[3:]  # "LP_wood" -> "wood"
        box_uv(o, f"{o.name}#{i}")
        o.data.materials[0] = mats[key]
        groups.setdefault(key, []).append(o)
    for key, objs in groups.items():  # one mesh per texture
        if len(objs) > 1:
            with bpy.context.temp_override(active_object=objs[0], selected_editable_objects=objs, selected_objects=objs):
                bpy.ops.object.join()
        objs[0].name = objs[0].data.name = f"{name}_{key}"
    return bpy.data.objects[name]


def forge_soot():
    """Restrained soot decal over the forge mouth: thin planes 0.02 proud of the crown, course and hood.
    One texture spans them all (u from x, v from height) so the smudge runs continuously."""
    import bmesh
    mat = tex_material("TX_forge_soot", save_png("forge_soot", soot()), alpha=True)
    root = bpy.data.objects["Forge"]
    z0, z1, half = 2.0, 4.4, 1.9  # soot area: mouth top to mid-hood, x -1.9..1.9

    def quad(name, pts):
        bm = bmesh.new()
        vs = [bm.verts.new(p) for p in pts]
        f = bm.faces.new(vs)
        uv = bm.loops.layers.uv.verify()
        for l in f.loops:
            l[uv].uv = ((l.vert.co.x + half) / (2 * half), (l.vert.co.z - z0) / (z1 - z0))
        me = bpy.data.meshes.new(name)
        bm.to_mesh(me)
        bm.free()
        me.materials.append(mat)
        o = bpy.data.objects.new(name, me)
        bpy.data.collections["Forge"].objects.link(o)
        o.parent = root

    quad("SootCrown", [(-1.6, -1.62, 2.45), (1.6, -1.62, 2.45), (1.6, -1.62, 2.69), (-1.6, -1.62, 2.69)])
    quad("SootCourse", [(-1.9, -1.72, 2.8), (1.9, -1.72, 2.8), (1.9, -1.72, 3.0), (-1.9, -1.72, 3.0)])
    # hood front face runs from (y -1.4, z 3.1) to (y -0.65, z 4.5); offset 0.02 along its normal
    ny, nz = -0.881, 0.472
    lo, hi = (-1.39 + 0.02 * ny, 3.12 + 0.02 * nz), (-0.75 + 0.02 * ny, 4.32 + 0.02 * nz)
    quad("SootHood", [(-1.55, lo[0], lo[1]), (1.55, lo[0], lo[1]), (0.7, hi[0], hi[1]), (-0.7, hi[0], hi[1])])

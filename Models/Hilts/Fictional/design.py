# Seven fictional blade profiles for Sell Swords! (BladeCore port: monotone cubic, gaussian bend, centreline).
# python -I design.py  -> profiles.luau (BladeData entries), blades.json (per-station refined params), preview.png
import json, math, os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REF = r"C:\Users\Allen\Documents\Create Swords!\References\Swords\roblox unique swords.png"
MASKS = json.load(open(os.path.join(HERE, "masks.json")))


# ---------------------------------------------------------------- BladeCore port
def make_curve(points):
    n = len(points)
    xs = [p[0] for p in points]; ys = [p[1] for p in points]
    if n == 1:
        return lambda u: ys[0]
    d = [(ys[k + 1] - ys[k]) / (xs[k + 1] - xs[k]) for k in range(n - 1)]
    m = [0.0] * n
    m[0], m[-1] = d[0], d[-1]
    for k in range(1, n - 1):
        m[k] = 0 if d[k - 1] * d[k] <= 0 else (d[k - 1] + d[k]) / 2
    for k in range(n - 1):
        if d[k] == 0:
            m[k] = m[k + 1] = 0
        else:
            a, b = m[k] / d[k], m[k + 1] / d[k]
            s = a * a + b * b
            if s > 9:
                t = 3 / math.sqrt(s)
                m[k], m[k + 1] = t * a * d[k], t * b * d[k]

    def f(u):
        if u <= xs[0]:
            return ys[0]
        if u >= xs[-1]:
            return ys[-1]
        k = 0
        while u > xs[k + 1]:
            k += 1
        h = xs[k + 1] - xs[k]
        t = (u - xs[k]) / h
        t2, t3 = t * t, t * t * t
        return ((2 * t3 - 3 * t2 + 1) * ys[k] + (t3 - 2 * t2 + t) * h * m[k] + (-2 * t3 + 3 * t2) * ys[k + 1]
                + (t3 - t2) * h * m[k + 1])
    return f


def sample(shape, N):
    c = {k: make_curve(shape[k]) for k in ("spine", "edge", "ridge", "thickness", "edgeThickness", "spineThickness")}
    seg = shape["length"] / (N - 1)
    sori, center, spread = shape["curve"]
    dens = [math.exp(-((((i + 0.5) / (N - 1)) - center) / spread) ** 2) for i in range(N - 1)]
    tot = sum(dens)
    out = dict(segLen=[], bend=[], spine=[], edge=[], ridge=[], thick=[], edgeT=[], spineT=[])
    for i in range(N):
        u = i / (N - 1)
        out["segLen"].append(seg if i < N - 1 else 0)
        out["bend"].append(sori * dens[i] / tot if i < N - 1 else 0)
        out["spine"].append(c["spine"](u)); out["edge"].append(c["edge"](u)); out["ridge"].append(c["ridge"](u))
        out["thick"].append(c["thickness"](u)); out["edgeT"].append(c["edgeThickness"](u))
        out["spineT"].append(c["spineThickness"](u))
    return out


def centerline(p):
    N = len(p["segLen"])
    px, py, ang = [0.0] * N, [0.0] * N, [0.0] * N
    seg, acc = [0.0] * (N - 1), 0.0
    for i in range(N - 1):
        seg[i] = acc + p["bend"][i] / 2
        acc += p["bend"][i]
    for i in range(N - 1):
        px[i + 1] = px[i] + p["segLen"][i] * math.cos(seg[i])
        py[i + 1] = py[i] + p["segLen"][i] * math.sin(seg[i])
    for i in range(N):
        ang[i] = seg[0] if i == 0 else seg[-1] if i == N - 1 else (seg[i - 1] + seg[i]) / 2
    return px, py, ang


def outline(p):
    px, py, ang = centerline(p)
    sp, ed = [], []
    for i in range(len(px)):
        nx, ny = -math.sin(ang[i]), math.cos(ang[i])
        sp.append((px[i] + nx * p["spine"][i], py[i] + ny * p["spine"][i]))
        ed.append((px[i] + nx * p["edge"][i], py[i] + ny * p["edge"][i]))
    return sp, ed


def measure(shape, N):
    p = sample(shape, N)
    px, py, ang = centerline(p)
    back = lambda i: (px[i] - math.sin(ang[i]) * p["spine"][i], py[i] + math.cos(ang[i]) * p["spine"][i])
    x0, y0 = back(0)
    t = (p["spine"][-1] + p["edge"][-1]) / 2
    x1, y1 = px[-1] - math.sin(ang[-1]) * t, py[-1] + math.cos(ang[-1]) * t
    nag = math.hypot(x1 - x0, y1 - y0)
    nx, ny = -(y1 - y0) / nag, (x1 - x0) / nag
    sori = 0.0
    for i in range(1, N - 1):
        x, y = back(i)
        below = -((x - x0) * nx + (y - y0) * ny)
        if abs(below) > abs(sori):
            sori = below
    return nag, sori


# ---------------------------------------------------------------- helpers
def taper(u, p):
    return 1 - u ** p


def dp(pts, tol):
    """Douglas-Peucker on (u, v) points with u scaled to cm by the caller."""
    if len(pts) < 3:
        return pts
    a, b = pts[0], pts[-1]
    best, idx = -1, 0
    for i in range(1, len(pts) - 1):
        # vertical distance to the chord (v as a function of u)
        t = (pts[i][0] - a[0]) / (b[0] - a[0])
        d = abs(pts[i][1] - (a[1] + t * (b[1] - a[1])))
        if d > best:
            best, idx = d, i
    if best <= tol:
        return [a, b]
    return dp(pts[:idx + 1], tol)[:-1] + dp(pts[idx:], tol)


def fn_points(f, us, tol=0.03):
    return [(round(u, 4), round(v, 4)) for u, v in dp([(u, f(u)) for u in us], tol)]


def grid(n):
    return [i / n for i in range(n + 1)]


# ---------------------------------------------------------------- the seven blades (refined shapes, cm)
P = {}

# 1 Crescent Fang: a crescent, the back curving in (concave) while the edge bulges, thin at both ends
def cf_c(u): return -5.0 * math.sin(math.pi * u) ** 1.1
def cf_s(u): return cf_c(u) + 0.9 * (1 - math.sin(math.pi * u)) * taper(u, 8) + 0.07
def cf_e(u): return cf_c(u) - (0.9 + 3.6 * math.sin(math.pi * u) ** 0.8) * taper(u, 5) - 0.07
P["crescentfang"] = dict(name="Crescent Fang", L=70, N=96, double=False, curve=(0, 0.5, 0.35),
    spine=fn_points(cf_s, grid(40)), edge=fn_points(cf_e, grid(40)),
    ridge=[(0, 0.35)], thickness=[(0, 0.9), (0.5, 0.75), (1, 0.3)], edgeT=[(0, 0.03)], spineT=[(0, 0.8)],
    tang=(11, 1.6), value=480,
    note="a crescent: the back curves in like a new moon while the edge bulges out, thin at both ends and broad in the middle")

# 2 Shard Blade: straight back, an edge of three flat runs meeting at corners, a diagonal chisel tip
P["shardblade"] = dict(name="Shard Blade", L=75, N=128, double=False, curve=(0, 0.5, 0.35),
    spine=[(0, 1.6), (1, 1.6)],
    edge=[(0, -3.0), (0.16, -2.55), (0.312, -2.1225), (0.32, -2.1), (0.335, -3.6), (0.343, -3.5685), (0.49, -2.99),
          (0.632, -2.4315), (0.64, -2.4), (0.655, -3.9), (0.663, -3.8727), (0.76, -3.5415), (0.852, -3.2273), (0.86, -3.2),
          (0.93, -0.95), (1.0, 1.3)],
    ridge=[(0, 0.45)], thickness=[(0, 1.0), (0.86, 0.7), (1, 0.35)], edgeT=[(0, 0.03)], spineT=[(0, 0.85)],
    tang=(12, 1.7), value=540,
    note="faceted crystal look: a straight back, an edge of three flat runs meeting at corners, and a diagonal chisel tip")

# 3 Serpent: the whole blade snakes in an S, back and edge waving together
def sp_c(u):
    ramp = min(1.0, u / 0.22); ramp = ramp * ramp * (3 - 2 * ramp)
    return 3.2 * math.sin(3 * math.pi * u) * ramp
def sp_h(u): return 1.7 * taper(u, 6) + 0.06
P["serpent"] = dict(name="Serpent", L=80, N=128, double=False, curve=(0, 0.5, 0.35),
    spine=fn_points(lambda u: sp_c(u) + sp_h(u), grid(80), 0.02),
    edge=fn_points(lambda u: sp_c(u) - sp_h(u), grid(80), 0.02),
    ridge=[(0, 0.35)], thickness=[(0, 0.9), (1, 0.35)], edgeT=[(0, 0.03)], spineT=[(0, 0.8)],
    tang=(13, 1.6), value=680,
    note="the whole blade snakes in an S (one and a half waves), back and edge waving together")

# 4 Leviathan Cleaver: a very wide falchion with a stepped notch in the back near the tip
P["leviathan"] = dict(name="Leviathan Cleaver", L=88, N=96, double=False, curve=(0, 0.5, 0.35),
    spine=[(0, 2.4), (0.712, 2.4), (0.72, 2.38), (0.732, 0.7), (0.74, 0.6), (0.86, 0.6), (0.92, 0.45), (0.97, -0.3), (1, -0.9)],
    edge=[(0, -4.5), (0.2, -5.4), (0.5, -6.9), (0.75, -8.1), (0.85, -8.5), (0.92, -8.1), (0.97, -6.2), (0.99, -3.6), (1, -1.2)],
    ridge=[(0, 0.72)], thickness=[(0, 1.1), (0.7, 0.85), (1, 0.4)], edgeT=[(0, 0.03)], spineT=[(0, 0.85)],
    tang=(16, 2.2), value=780,
    note="a very wide falchion (11 cm at the notch) with a stepped notch in the back near the tip")

# 5 Seraph and 6 Thornspire: the left and middle swords of References/Swords/roblox unique swords.png, traced from the
# straightened picture (trace_ref.py: each sword turned upright about its grip centre; traced.json)
TR = json.load(open(os.path.join(HERE, "traced.json")))
def outline_rows(name):
    return {int(k): v for k, v in TR[name]["outline"].items()}
SER = outline_rows("seraph")
S_ROOT, S_TIP, S_LEN = 540, 22, 76.0
s_cm = S_LEN / (S_ROOT - S_TIP)
cb = sum((SER[y][0][0] + SER[y][-1][1]) / 2 for y in range(100, 221, 2)) / 61   # the blade's centre column
ser = []
for y in range(S_TIP, S_ROOT + 1, 2):
    u = (S_ROOT - y) / (S_ROOT - S_TIP)
    h = 22.5 if y > 490 else max(0.25, cb - (SER[y][0][0] - 0.5) if y in SER else 0.25)  # the left (unglared) side
    ser.append((round(u, 4), h * s_cm))
ser.sort()
ser = [ser[0]] + [(ser[i][0], (ser[i - 1][1] + 2 * ser[i][1] + ser[i + 1][1]) / 4) for i in range(1, len(ser) - 1)] + [ser[-1]]
ser[-1] = (1.0, 0.05)
P["seraph"] = dict(name="Seraph", L=S_LEN, N=128, double=True, curve=(0, 0.5, 0.35),
    spine=[(u, round(v, 4)) for u, v in dp(ser, 0.05)], edge=[(u, round(-v, 4)) for u, v in dp(ser, 0.05)],
    ridge=[(0, 0.5)], thickness=[(0, 0.9), (0.8, 0.62), (1, 0.25)], edgeT=[(0, 0.03)], spineT=[(0, 0.06)],
    tang=(16, 2.0), value=980, keep_thickness=True,
    note="the left sword of References/Swords/roblox unique swords.png, traced: a long straight double-edged blade "
         "flaring into down-pointing barbs above the guard; the gold centre line is painted on by its hilt (SwordParts.SeraphHilt.Guard)")

TH = outline_rows("thornspire")
TA = TR["thornspire"]["axis"]
T_ROOT, T_TIP, T_LEN = 600, 40, 80.0
t_cm = T_LEN / (T_ROOT - T_TIP)
sp, ed = [], []
for y in range(T_TIP, 597, 2):
    if y not in TH:
        continue
    segs = TH[y]
    if y < 300:   # the upper blade: its outer extents (the slot below the tip is painted, not cut)
        L, R = segs[0][0], segs[-1][1]
    else:         # the lower blade: the piece round the centre line (the horn tips standing apart are left out)
        L, R = min(segs, key=lambda q: 0 if q[0] <= TA <= q[1] else min(abs(q[0] - TA), abs(q[1] - TA)))
    if 548 < y <= 558:   # the bottom horns: a steep flank from the body out to each horn tip
        f = (y - 548) / 10
        L, R = 70 + (40 - 70) * f, 130 + (160 - 130) * f
    elif 558 < y < 568:
        L, R = 40.5, 159.5
    u = (T_ROOT - y) / (T_ROOT - T_TIP)
    sp.append((round(u, 4), (R + 0.5 - TA) * t_cm)); ed.append((round(u, 4), (L - 0.5 - TA) * t_cm))
sp.append((0.0, sp[-1][1])); ed.append((0.0, ed[-1][1]))
sp.sort(); ed.sort()
sp[-1] = (1.0, sp[-1][1]); ed[-1] = (1.0, ed[-1][1])


def smooth3(pts):
    """[1 2 1] smoothing of a traced run (takes the 1-pixel stair steps off; the ends stay)."""
    return [pts[0]] + [(pts[i][0], (pts[i - 1][1] + 2 * pts[i][1] + pts[i + 1][1]) / 4) for i in range(1, len(pts) - 1)] + [pts[-1]]
sp, ed = smooth3(sp), smooth3(ed)
P["thornspire"] = dict(name="Thornspire", L=T_LEN, N=192, double=True, curve=(0, 0.5, 0.35),
    spine=[(u, round(v, 4)) for u, v in dp(sp, 0.05)], edge=[(u, round(v, 4)) for u, v in dp(ed, 0.05)],
    ridge=[(0, 0.5)], thickness=[(0, 0.9), (0.5, 0.7), (1, 0.3)], edgeT=[(0, 0.03)], spineT=[(0, 0.06)],
    tang=(15, 2.2), value=880, keep_thickness=True,
    note="the middle sword of References/Swords/roblox unique swords.png, traced: thorn spikes on both edges of the broad "
         "lower blade, a narrow upper blade leaning to one side; the slot below the tip and the dark markings are painted "
         "on by its hilt (SwordParts.ThornspireHilt.Marks), the blade itself is solid")

# 7 Moonbite: a broad curved cleaver with a round bite out of the edge near the guard (generic silhouette only)
MB_UC, MB_R = 0.17, 3.0
def mb_e(u):
    v = make_curve([(0, -4.6), (0.3, -6.0), (0.5, -6.8), (0.65, -6.6), (0.8, -5.2), (0.9, -3.4), (0.97, -1.4), (1, 0.9)])(u)
    ru = MB_R / 66.0
    d = (u - MB_UC) / ru
    if abs(d) < 1:
        v += MB_R * math.sqrt(1 - d * d)
    t = (u - (MB_UC - ru - 0.012)) / 0.012          # a small tooth under the bite
    if -1 < t < 1:
        v -= 0.7 * (1 - abs(t))
    return v
us = sorted(set(grid(200) + [MB_UC + MB_R / 66.0 * math.sin(a * math.pi / 40) for a in range(-20, 21)]))
P["moonbite"] = dict(name="Moonbite", L=66, N=128, double=False, curve=(0.2, 0.7, 0.3),
    spine=[(0, 1.5), (0.85, 1.5), (0.95, 1.35), (1, 1.1)], edge=fn_points(mb_e, us, 0.02),
    ridge=[(0, 0.55)], thickness=[(0, 1.0), (0.8, 0.7), (1, 0.35)], edgeT=[(0, 0.03)], spineT=[(0, 0.85)],
    tang=(12, 2.0), value=600, keep_thickness=True,
    note="a broad curved cleaver with a round bite out of the edge near the guard and a small tooth under it (the silhouette "
         "idea only; hilt, colours and markings are its own)")

ORDER = ["crescentfang", "shardblade", "moonbite", "serpent", "leviathan", "thornspire", "seraph"]

RECIPE = [("lengthen", 0.12, 0.3, "center", False, 0), ("lengthen", 0.38, 0.3, "center", False, 6),
          ("lengthen", 0.62, 0.3, "center", True, -5), ("lengthen", 0.88, 0.3, "center", True, 4),
          ("taper", 0.2, 0.32, "edge", False, 0), ("taper", 0.5, 0.32, "edge", False, -6),
          ("taper", 0.78, 0.3, "spine", True, 5), ("taper", 0.95, 0.25, "edge", True, -4),
          ("tip", 0.97, 0.12, "edge", False, 8), ("tip", 0.85, 0.16, "edge", False, 4),
          ("tip", 0.55, 0.32, "edge", True, -4), ("tip", 0.2, 0.32, "edge", True, 0)]


def stages(pid):
    d = P[pid]
    L, N = d["L"], d["N"]
    refined = dict(length=L, curve=d["curve"], spine=d["spine"], edge=d["edge"], ridge=d["ridge"],
                   thickness=d["thickness"], edgeThickness=d["edgeT"], spineThickness=d["spineT"])
    p = sample(refined, N)
    mean_w = sum(a - b for a, b in zip(p["spine"], p["edge"])) / N
    h = round(min(2.6, max(1.2, 0.5 * mean_w)), 2)
    lengthened = dict(length=round(0.78 * L, 1), curve=(0, 0.5, 0.35),
                      spine=[(0, h), (0.92, round(0.95 * h, 4)), (1, round(0.8 * h, 4))],
                      edge=[(0, -h), (0.92, round(-0.95 * h, 4)), (1, round(-0.8 * h, 4))],
                      ridge=[(0, 0.5 if d["double"] else 0.85)], thickness=[(0, 0.95), (1, 0.82)],
                      edgeThickness=[(0, 0.55)], spineThickness=[(0, 0.6 if d["double"] else 0.92)])
    # preform: the refined outline smoothed (box filter 0.1), at 11 points
    def smooth(key):
        out = []
        for u in grid(10):
            vals = [p[key][i] for i in range(N) if abs(i / (N - 1) - u) <= 0.05]
            out.append((u, round(sum(vals) / len(vals), 4)))
        return out
    ps, pe = smooth("spine"), smooth("edge")
    for k in range(len(ps)):  # keep a little width everywhere
        if ps[k][1] - pe[k][1] < 0.3:
            m = (ps[k][1] + pe[k][1]) / 2
            ps[k], pe[k] = (ps[k][0], round(m + 0.15, 4)), (pe[k][0], round(m - 0.15, 4))
    keep = d.get("keep_thickness")
    preform = dict(length=L, curve=(round(d["curve"][0] * 0.6, 4), d["curve"][1], d["curve"][2]), spine=ps, edge=pe,
                   ridge=d["ridge"] if keep else [(0, 0.5 if d["double"] else 0.4)],
                   thickness=d["thickness"] if keep else [(0, 0.86), (1, 0.62)],
                   edgeThickness=[(0, 0.28)], spineThickness=d["spineT"] if keep else [(0, 0.32 if d["double"] else 0.85)])
    return lengthened, preform, refined


def lua_pts(pts):
    return "{ " + ", ".join("{ %s, %s }" % (fmt(u), fmt(v)) for u, v in pts) + " }"


def fmt(x):
    s = ("%.4f" % x).rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def lua_shape(sh, ind):
    t = "\t" * ind
    c = sh["curve"]
    return (f"{{\n{t}\tlength = {fmt(sh['length'])},\n{t}\tcurve = {{ sori = {fmt(c[0])}, center = {fmt(c[1])}, spread = {fmt(c[2])} }},\n"
            f"{t}\tspine = {lua_pts(sh['spine'])},\n{t}\tedge = {lua_pts(sh['edge'])},\n{t}\tridge = {lua_pts(sh['ridge'])},\n"
            f"{t}\tthickness = {lua_pts(sh['thickness'])},\n{t}\tedgeThickness = {lua_pts(sh['edgeThickness'])},\n"
            f"{t}\tspineThickness = {lua_pts(sh['spineThickness'])},\n{t}}}")


def lua_profile(pid):
    d = P[pid]
    le, pr, re = stages(pid)
    nag, sori = measure(re, d["N"])
    rec = ",\n".join(f"\t\t\t\t{{ stage = \"{s}\", u = {fmt(u)}, radius = {fmt(r)}, side = \"{side}\", flip = {str(f).lower()}, turn = {t} }}"
                     for s, u, r, side, f, t in RECIPE)
    note = (f"Drafted 2026-10-29 (Allen picked it from References/Sword Silhouettes/fictional-silhouettes-v1.png), not approved. "
            f"Fictional: {d['note']}. Same 12-strike recipe as the other blades. Units are centimetres.")
    return (f"\t\t{pid} = {{\n\t\t\tid = \"{pid}\",\n\t\t\tname = \"{d['name']}\",\n\t\t\tversion = 1,\n"
            f"\t\t\tnote = {json.dumps(note, ensure_ascii=False)},\n\t\t\tstations = {d['N']},\n"
            + ("\t\t\tdoubleEdged = true,\n" if d["double"] else "")
            + f"\t\t\ttang = {{ length = {d['tang'][0]}, width = {d['tang'][1]} }},\n"
            f"\t\t\tspec = {{ note = \"Measured from the refined shape (BladeCore.measureShape), 2026-10-29.\", sori = {sori:.2f}, nagasa = {nag:.2f} }},\n"
            f"\t\t\tstages = {{\n\t\t\t\tlengthened = {lua_shape(le, 4)},\n\t\t\t\tpreform = {lua_shape(pr, 4)},\n\t\t\t\trefined = {lua_shape(re, 4)},\n\t\t\t}},\n"
            f"\t\t\tforgedAllowance = {{ note = \"The 90% blade is the refined blade plus this subtle excess along the edge, with a duller, thicker edge. Grinding removes exactly this and nothing more.\", edge = 0.14, edgeThickness = 0.12 }},\n"
            f"\t\t\trecipe = {{\n{rec},\n\t\t\t}},\n\t\t}},\n")


if __name__ == "__main__":
    with open(os.path.join(HERE, "profiles.luau"), "w", encoding="utf-8", newline="\n") as f:
        for pid in ORDER:
            f.write(lua_profile(pid))
    blades = {}
    for pid in ORDER:
        d = P[pid]
        _, pr, re = stages(pid)
        p = sample(re, d["N"]); q = sample(pr, d["N"])
        px, py, ang = centerline(p)
        blades[pid] = dict(N=d["N"], double=d["double"], px=px, py=py, ang=ang, spine=p["spine"], edge=p["edge"],
                           ridge=p["ridge"], thick=p["thick"], edgeT=[max(a + 0.12, b) for a, b in zip(p["edgeT"], q["edgeT"])],
                           spineT=p["spineT"], length=d["L"])
        print(pid, "points", len(d["spine"]), len(d["edge"]), "nagasa/sori %.2f %.2f" % measure(re, d["N"]),
              "max width %.2f" % max(a - b for a, b in zip(p["spine"], p["edge"])))
    json.dump(blades, open(os.path.join(HERE, "blades.json"), "w"))
    # preview: each blade at 6 px/cm, base at the bottom, plus the two references at matching scale
    PXC = 6
    W = 160 * len(ORDER) + 400
    img = Image.new("RGB", (W, 760), (246, 241, 232))
    dr = ImageDraw.Draw(img)
    base_y = 720
    for k, pid in enumerate(ORDER):
        d = P[pid]
        p = sample(stages(pid)[2], d["N"])
        sp_, ed_ = outline(p)
        ox = 80 + 160 * k
        poly = [(ox - y * PXC, base_y - x * PXC) for x, y in sp_ + ed_[::-1]]  # spine to screen left
        dr.polygon(poly, fill=(30, 32, 38))
        dr.text((ox - 40, base_y + 8), d["name"], fill=(0, 0, 0))
    # references, scaled so their blade length matches
    ref = Image.open(REF).convert("RGB")
    for name, x0, x1, root, tip, L, ox in (("seraph", 0, 205, S_ROOT, S_TIP, S_LEN, 160 * len(ORDER) + 40),
                                             ("thorn", 205, 415, T_ROOT, T_TIP, T_LEN, 160 * len(ORDER) + 220)):
        sc = L * PXC / (root - tip)
        crop = ref.crop((x0, tip - 10, x1, root + 10))
        crop = crop.resize((int(crop.width * sc), int(crop.height * sc)))
        img.paste(crop, (ox, base_y - crop.height + int(10 * sc)))
    img.save(os.path.join(HERE, "preview.png"))

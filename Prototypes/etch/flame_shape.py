"""The curled Flame's shape (Create Swords!, 2026-11-10): the band's top along a blade, the same code Shared/EtchPatterns
runs in the game (port any change there).

Traced from the reference (Allen: "What's so hard about copying the reference"): flame_trace.json is the photo's red /
black outline, straightened, in blade widths (u along toward the point, v up from the cutting edge), from
trace_reference.py. It repeats along the blade, end joined to start, each point placed by the local width (capped), from
its first deep dark tip. At the canvas's strip seams it breaks at a deep tip into plain band; the last run goes on into
the point, shrinking with the width, and the band runs out to the very tip.
(The hand-drawn attempts before it are in git history: they never got past 6/10 in side-by-side reviews.)
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
BAND = 0.17             # plain band top at the guard, the seams and the point (fraction of the capped width)
FOOT = -0.06            # where the pieces reach below the edge line (off the canvas): no ink there
SIZE = 1.0              # the trace this much wider along the blade (1: the photo's own proportions)
SEAM = 0.12             # widths of plain band either side of a canvas strip seam (the texture wraps there)
END = 0.2               # the flames run into the point until the face is this share of its width where the point starts
STEPS = 8

TRACE = [tuple(p) for p in json.load(open(os.path.join(HERE, "flame_trace.json")))["points"]]
# one copy's end joins the next copy's start through a small dip (a short dark tail), not a step
JOIN = 0.08
TRACE.append((TRACE[-1][0] + JOIN / 2, 0.20))
PERIOD = TRACE[-1][0] + JOIN / 2


def deep_tips(P):
    """Indices of the deep dark tips: the lowest point nearby, under 0.26 of the width."""
    out = []
    for i in range(1, len(P) - 1):
        near = [q[1] for q in P[max(0, i - 6):i + 7]]
        if P[i][1] < 0.26 and P[i][1] == min(near):
            out.append(i)
    return out


TIPS = deep_tips(TRACE)


def bez(p0, c1, c2, p3, out):
    for k in range(1, STEPS + 1):
        t = k / STEPS
        a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
        out.append((a * p0[0] + b * c1[0] + c * c2[0] + d * p3[0], a * p0[1] + b * c1[1] + c * c2[1] + d * p3[1]))


def piece(k):
    """Piece k of the endless run of the trace: from one deep tip to the next, as (u, v) with u growing per copy."""
    n = len(TIPS)
    copy, j = divmod(k, n)
    a = TIPS[j]
    if j + 1 < n:
        return [(u + copy * PERIOD, v) for u, v in TRACE[a:TIPS[j + 1] + 1]]
    seg = [(u + copy * PERIOD, v) for u, v in TRACE[a:]]          # across the join into the next copy
    return seg + [(u + (copy + 1) * PERIOD, v) for u, v in TRACE[:TIPS[0] + 1]]


FIT = (0.8, 1.25)       # how far a run of pieces may be squeezed or stretched to end at a seam or the point


def boundary(length, cap, limit, seams=()):
    """The band's top from before the guard to past the point, as (x cm, v) points (v: fraction of the capped width),
    and the indices of the cut points (every deep tip: only colour straight below it). Between the guard, each seam and
    the sloping point the pieces are fitted (squeezed or stretched within FIT) so the last ends at a deep tip just short
    of the seam; plain band runs across it."""
    capx = lambda x: cap(min(max(x, 0), length))

    def place(seg, x, s):
        xs = [x]
        for (u0, _), (u1, _) in zip(seg, seg[1:]):
            xs.append(xs[-1] + (u1 - u0) * capx(xs[-1]) * SIZE * s)
        return xs

    pts = [(-0.5, BAND)]
    cuts = []
    starts = [0.45 * cap(0)] + [sm + SEAM * capx(sm) * SIZE for sm in seams]
    # the last run goes on into the point (Allen: "all the way to the tip"), the flames shrinking with the width
    last_end = length
    while last_end > limit and cap(last_end) < END * cap(limit):
        last_end -= 0.05
    ends = [sm - SEAM * capx(sm) * SIZE for sm in seams] + [last_end]
    k = 0
    for a, b in zip(starts, ends):
        W = capx(a) * SIZE
        x0 = a + 0.2 * W                           # room for the first piece reaching back
        # how many whole pieces fit at their own size, and how far the next would overshoot
        x, n, his = x0, 0, []
        while True:
            xs = place(piece(k + n), x, 1.0)
            if max(xs) > b:
                over = max(xs)
                break
            his.append(max(xs))
            x = xs[-1]
            n += 1
        options = []
        if n > 0:
            options.append((n, (b - x0) / (his[-1] - x0)))  # stretch n
        options.append((n + 1, (b - x0) / (over - x0)))     # squeeze n + 1
        options = [o for o in options if FIT[0] <= o[1] <= FIT[1]]
        if not options:
            if n == 0:
                continue                           # too short for a piece: plain band
            options = [(n, 1.0)]
        n, sc = min(options, key=lambda o: abs(math.log(o[1])))
        x = x0
        for q in range(n):
            seg = piece(k + q)
            xs = place(seg, x, sc)
            if q == 0:                             # rise from the plain band to the first tip
                pts.append((min(min(xs), x) - 0.1 * W, BAND))
            same = abs(pts[-1][0] - xs[0]) < 1e-9 and abs(pts[-1][1] - seg[0][1]) < 1e-9
            cuts.append(len(pts) - 1 if same else len(pts))
            for i, ((u, v), xx) in enumerate(zip(seg, xs)):
                if i > 0 or not same:
                    pts.append((xx, v))
            x = xs[-1]
        k += n
        last = pts[-1]                             # down to the band after the run
        w = capx(last[0]) * SIZE                   # the width there (the last run ends in the narrowing point)
        bez(last, (last[0] + 0.1 * w, last[1]), (last[0] + 0.2 * w, BAND), (last[0] + 0.35 * w, BAND), pts)
    xe = pts[-1][0]
    m = max(2, math.ceil((length + 0.5 - xe) / 0.25))
    for i in range(1, m + 1):
        pts.append((xe + (length + 0.5 - xe) * i / m, BAND))
    return pts, cuts

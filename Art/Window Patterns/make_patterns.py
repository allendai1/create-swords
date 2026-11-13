"""Seamless 256 px pattern tiles: white shapes on transparent, antialiased by 4x4 supersampling. No Pillow needed."""
import math, os, struct, sys, zlib

N = 256
SS = 4
OUT = sys.argv[1]


def png(path, alpha):
    raw = bytearray()
    for y in range(N):
        raw.append(0)
        for x in range(N):
            raw += bytes((255, 255, 255, alpha[y * N + x]))
    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    data = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', N, N, 8, 6, 0, 0, 0)) \
        + chunk(b'IDAT', zlib.compress(bytes(raw), 9)) + chunk(b'IEND', b'')
    open(path, 'wb').write(data)


def render(inside):
    """inside(u, v) -> bool, u/v in [0,1) tile space; wraps by construction of each pattern."""
    a = []
    for y in range(N):
        for x in range(N):
            hit = 0
            for sy in range(SS):
                for sx in range(SS):
                    if inside((x + (sx + 0.5) / SS) / N, (y + (sy + 0.5) / SS) / N):
                        hit += 1
            a.append(round(255 * hit / (SS * SS)))
    return a


def cells(u, v, n, offset_rows=True):
    """Local coords in an n x n grid (rows offset by half a cell when asked), centred: (-0.5..0.5)."""
    gy = v * n
    row = math.floor(gy)
    gx = u * n + (0.5 if offset_rows and row % 2 else 0)
    return gx - math.floor(gx) - 0.5, gy - row - 0.5


def star(px, py, r_out, r_in, points=5, rot=-math.pi / 2):
    ang = math.atan2(py, px) - rot
    r = math.hypot(px, py)
    seg = 2 * math.pi / points
    a = (ang % seg) - seg / 2
    # edge between outer tip (angle 0) and inner notch (angle seg/2), linear in polar is close enough for a game tile
    t = abs(a) / (seg / 2)
    edge = r_out * (1 - t) + r_in * t
    return r <= edge


def seg_dist(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - ax - t * dx, py - ay - t * dy)


def sword(px, py, ang):
    c, s = math.cos(-ang), math.sin(-ang)
    x, y = px * c - py * s, px * s + py * c  # sword along +x, tip at +0.36
    if seg_dist(x, y, -0.06, 0, 0.30, 0) < 0.035:  # blade
        return True
    if x >= 0.30 and x <= 0.38 and abs(y) <= 0.035 * (0.38 - x) / 0.08:  # tip
        return True
    if seg_dist(x, y, -0.07, -0.11, -0.07, 0.11) < 0.025:  # guard
        return True
    if seg_dist(x, y, -0.20, 0, -0.08, 0) < 0.022:  # grip
        return True
    return math.hypot(x + 0.23, y) < 0.04  # pommel


PATTERNS = {
    'pat_dots': lambda u, v: math.hypot(*cells(u, v, 4)) < 0.17,
    'pat_stars': lambda u, v: star(*cells(u, v, 4), 0.27, 0.11),
    'pat_stripes': lambda u, v: ((u + v) * 4) % 1 < 0.38,
    'pat_checks': lambda u, v: (math.floor(u * 4) + math.floor(v * 4)) % 2 == 0,
    'pat_sparkles': lambda u, v: (lambda x, y: (abs(x) ** 0.5 + abs(y) ** 0.5) < 0.42 ** 0.5
                                  or math.hypot(x - 0.32, y + 0.3) < 0.035)(*cells(u, v, 3)),
    'pat_swords': lambda u, v: (lambda x, y: sword(x, y, math.pi / 4) or sword(x, y, 3 * math.pi / 4))(*cells(u, v, 2)),
    'pat_zigzag': lambda u, v: abs(((v * 4 + abs(((u * 8) % 2) - 1) * 0.5) % 1) - 0.5) < 0.12,
    'pat_diamonds': lambda u, v: (lambda x, y: abs(x) + abs(y) < 0.3)(*cells(u, v, 4)),
}

os.makedirs(OUT, exist_ok=True)
for name, f in PATTERNS.items():
    png(os.path.join(OUT, name + '.png'), render(f))
    print(name)

"""Flat preview of a stroked etch from the game's own canvas (2026-11-10, Lightning).

Input: a Studio MCP saved output with lines "COVER <blade> <cols> <length cm> <strokes> <widths,every 8th col> <base64> END",
1 bit a pixel (EtchCanvas cover >= 128), column-major, 128 rows a column, row 0 at the cutting edge.
Output: each blade at true proportions (one scale), edge at the bottom, marks white on grey steel.

python lightning_preview.py <saved output.txt> <out.png>   (needs Pillow)
"""
import base64
import re
import sys

from PIL import Image

PX_CM = 14
blades = []
for line in open(sys.argv[1], encoding="utf-8").read().splitlines():
    m = re.match(r"COVER (\w+) (\d+) ([\d.]+) (\d+) (\S+) (\S+) END", line)
    if m:
        blades.append((m[1], int(m[2]), float(m[3]), [float(w) for w in m[5].split(",")], base64.b64decode(m[6])))
assert blades, "no COVER lines"

pad = 16
rows = []
for name, n, length, ws, raw in blades:
    w_px, h_px = int(length * PX_CM), int(max(ws) * PX_CM) + 2
    img = Image.new("RGB", (w_px, h_px), (34, 26, 22))
    px = img.load()
    for x in range(w_px):
        i = min(n - 1, x * n // w_px)
        width = ws[min(len(ws) - 1, i // 8)] * PX_CM
        for y in range(int(width)):
            r = min(127, int(y / width * 128))
            on = raw[i * 16 + r // 8] >> (r % 8) & 1
            px[x, h_px - 1 - y] = (240, 244, 250) if on else (120, 126, 138)
    rows.append(img)
sheet = Image.new("RGB", (max(r.width for r in rows) + 2 * pad, sum(r.height + pad for r in rows) + pad), (34, 26, 22))
y = pad
for r in rows:
    sheet.paste(r, (pad, y))
    y += r.height + pad
sheet.save(sys.argv[2])
print([b[0] for b in blades], sheet.size)

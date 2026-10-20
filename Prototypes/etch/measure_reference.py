"""Measures the red band in References/Etching Table/flame-band-reference.webp: band width as a fraction of the
blade width and the hump spacing/amplitude. Feeds the numbers in flame_etch_preview.py."""
import numpy as np
from PIL import Image
import os
REF = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'References', 'Etching Table', 'flame-band-reference.webp')
im = np.asarray(Image.open(REF).convert('RGB')).astype(int)
H, W, _ = im.shape
r, g, b = im[..., 0], im[..., 1], im[..., 2]
red = (r > 90) & (r > 2 * g) & (r > 2 * b)
bright = (b > 200) & (g > 200) & (r > 150)
dark = (r < 60) & (g < 70) & (b < 90)
rows = []
for x in range(80, 1172, 4):
    col_b = np.where(bright[:, x])[0]
    col_r = np.where(red[:, x])[0]
    col_d = np.where(dark[:, x])[0]
    if len(col_r) < 2 or len(col_b) < 2: continue
    rtop, rbot = col_r.min(), col_r.max()
    # bright lines: the one just above the red, and the one below the dark body
    above = col_b[col_b < rtop]; below = col_b[col_b > rbot + 5]
    if len(above) == 0 or len(below) == 0: continue
    top = above.max(); bot = below.min()
    w = bot - top
    rows.append((x, top, rbot, bot, (rbot - top) / w, w))
rows = np.array(rows)
f = rows[:, 4]
print('n', len(rows), 'red frac mean %.3f min %.3f max %.3f' % (f.mean(), f.min(), f.max()))
print('blade px width', rows[:, 5].min(), rows[:, 5].max())
# detrend and find peaks (dark humps = local minima of red frac)
from numpy import convolve
trend = np.convolve(f, np.ones(25) / 25, mode='same')
d = f - trend
mins = [i for i in range(2, len(f) - 2) if f[i] == f[i-2:i+3].min() and d[i] < -0.01]
xs = rows[mins, 0]
print('hump x', xs.tolist())
print('spacing px', np.diff(xs).tolist())
print('spacing / blade width', (np.diff(xs) / rows[mins[:-1], 5]).round(2).tolist())
print('amp (max-min frac) local', [round(float(f[max(0,i-6):i+6].max() - f[i]), 3) for i in mins])

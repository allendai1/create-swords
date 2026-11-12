"""Etch pattern card images for the Etching Table's picker (2026-11-09, Allen: "instead of showing the sword with the
etch here, can we just use an image of the pattern that would be etched").

Input: the Studio MCP's saved outputs of an Edit-mode render, one per pattern ("CROP <id> <base64> END"). Each pattern
is drawn by the game's own code on the gladius (SwordMeshCache.overlay's layout and surface; Flame by
EtchCanvas:revealBand with BladeEtch.bandReach, the stroked ones by EtchPatterns.strokes), see-through body and white
marks, then a window two blade widths long at true proportions is cut out with the cutting edge at the bottom:
256 x 128, 2 bytes a pixel (luminance, alpha). Output: <id>.png (white marks, dark ink, transparent body; the picker
tints it with ImageColor3) and preview.png (each tinted on the picker's dark well, for checking).

python build_pattern_cards.py <tool-results dir>   (needs Pillow: miniconda's python has it)
"""
import base64
import pathlib
import re
import sys

from PIL import Image

HERE = pathlib.Path(__file__).parent
W, H = 256, 128
TINTS = {"Flame": (165, 14, 10), "WovenWind": (196, 214, 236), "Lightning": (196, 214, 236)}  # Lightning replaced Fracture 2026-11-10

found = {}
for f in sorted(pathlib.Path(sys.argv[1]).glob("mcp-Roblox_Studio-execute_luau-*.txt")):
    m = re.match(r"CROP (\w+) (\S+) END", f.read_text())
    if m:
        found[m[1]] = m[2]  # sorted by name (a timestamp): the newest render wins

for pid in sorted(found):
    raw = base64.b64decode(found[pid])
    assert len(raw) == W * H * 2, (pid, len(raw))
    img = Image.new("RGBA", (W, H))
    img.putdata([(raw[i], raw[i], raw[i], raw[i + 1]) for i in range(0, len(raw), 2)])
    img.save(HERE / f"{pid}.png")
    print(pid, "ok")
# the preview shows every pattern on offer, from the PNGs here (a run may render only one)
shown_ids = [pid for pid in TINTS if (HERE / f"{pid}.png").exists()]
preview = Image.new("RGBA", (W + 32, (H + 16) * len(shown_ids) + 16), (34, 26, 22, 255))
for row, pid in enumerate(shown_ids):
    img = Image.open(HERE / f"{pid}.png").convert("RGBA")
    r, g, b, a = img.split()
    tr, tg, tb = TINTS[pid]
    shown = Image.merge("RGBA", (r.point(lambda v: v * tr // 255), g.point(lambda v: v * tg // 255), b.point(lambda v: v * tb // 255), a))
    preview.alpha_composite(shown, (16, 16 + row * (H + 16)))
preview.save(HERE / "preview.png")

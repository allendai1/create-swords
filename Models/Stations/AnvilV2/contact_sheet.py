# Contact sheet for Anvil v2: the reference's main view beside the seven renders of the built mesh.
# Run after build_anvil_v2.py:  python contact_sheet.py   ->  review/anvil_v2_sheet.png
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "..", "..", "..", "References", "Anvil", "anvil-sheet-v1.webp")
VIEWS = ["front_three_quarter", "rear_three_quarter", "left", "right", "front", "back", "top"]
T = 600

tiles = [("REFERENCE (main view)", Image.open(REF).convert("RGB").crop((0, 0, 730, 625)))]
tiles += [(v.replace("_", " ").upper(), Image.open(os.path.join(HERE, "review", f"anvil_v2_{v}.png")).convert("RGB"))
          for v in VIEWS]
sheet = Image.new("RGB", (4 * T, 2 * T), (40, 39, 44))
draw = ImageDraw.Draw(sheet)
try:
    font = ImageFont.truetype("arial.ttf", 24)
except OSError:
    font = ImageFont.load_default()
for i, (label, im) in enumerate(tiles):
    im.thumbnail((T - 8, T - 8))
    x, y = (i % 4) * T, (i // 4) * T
    sheet.paste(im, (x + (T - im.width) // 2, y + (T - im.height) // 2))
    draw.text((x + 16, y + T - 40), label, fill=(225, 225, 232), font=font)
sheet.save(os.path.join(HERE, "review", "anvil_v2_sheet.png"))
print("sheet saved")

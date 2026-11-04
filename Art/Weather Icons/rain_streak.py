# Rain drop texture for ReplicatedStorage.WeatherFx.Rain.Drops (Fixes3): a thin vertical streak, white (the emitter tints
# it), fading out at both ends. 32 x 256, transparent. Run: python rain_streak.py
from PIL import Image

W, H = 32, 256
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
px = img.load()
for y in range(H):
    t = y / (H - 1)
    along = min(t / 0.35, 1.0) * min((1 - t) / 0.12, 1.0)  # long soft tail at the top, short at the bottom
    for x in range(W):
        across = max(0.0, 1 - abs(x - (W - 1) / 2) / (W * 0.18))
        a = int(255 * along * across ** 1.5)
        if a:
            px[x, y] = (255, 255, 255, a)
img.save(__file__.replace("rain_streak.py", "Rain Streak 32x256.png"))
print("ok")

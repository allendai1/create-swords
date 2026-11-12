"""Cuts the 30-second trailer from Allen's recordings with FFmpeg (2026-11-10).

    python build_trailer.py [out.mp4]

The cut list is SHOTS below: clip, in, out (seconds in the source), speed, crop, caption. Edit it and run again.
Sources: C:/Users/Allen/Videos/game-clips (1920x1080, 60 fps, recorded with the Windows title bar and taskbar in
frame, except the three staged scenes). The recordings have no game sound (mean -54 dB), so the only sound is the
music track: MUSIC below.
"""
import os
import subprocess
import sys

FFMPEG = r"C:\Users\Allen\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe"
CLIPS = r"C:\Users\Allen\Videos\game-clips"
OUT = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\Allen\Videos\Swordsmith Tycoon trailer - draft 4.mp4"
# "Angry Guitar Riff" (APM Music, Roblox audio 1836019934; Allen: "i have this track from roblox studio"), taken from
# MUSIC_START seconds in: the band comes in at 10 s of the track, which lands on the first hammer blow (5.7 s)
MUSIC = os.path.join(CLIPS, "music", "Angry Guitar Riff (APM, Roblox 1836019934).ogg")  # None = silent
MUSIC_START = 4.3
FONT = "C\\:/Windows/Fonts/comicbd.ttf"  # Comic Sans Bold (Allen: "use comic sans if possible")

# the game without the title bar (y < 23), Roblox's top bar, the taskbar (y > 1032) and the Trailer button: 16:9
GAME = "1706:960:107:72"
TIGHT = "1440:810:400:150"  # closer: also loses the coin HUD on the left
FULL = "1740:979:180:60"  # the staged scenes: clean but for Roblox's top-bar icons in the top left corner

ORE, FULLP, SCENES, DISPLAY, CREW = "ore-rolling.mp4", "full process.mp4", "game 3-scene.mp4", "put sword on display.mp4", "time-lapse overhead of crew.mp4"

SHOTS = [
    # clip, in, out, speed, crop, caption (a leading ^ puts it at the top: the station's own buttons are at the bottom)
    (ORE, 11.6, 14.6, 1, GAME, "ROLL FOR RARE ORE"),  # the camera is still from 10.3 s (Allen: the panning cut out)
    (ORE, 25.3, 27.3, 1, GAME, "HIT A SECRET"),
    (FULLP, 23.6, 24.8, 1, TIGHT, "HEAT IT"),
    (FULLP, 48.6, 51.6, 1, GAME, "^FORGE IT"),
    (FULLP, 53.7, 55.2, 1, GAME, ""),
    (FULLP, 61.0, 70.0, 4.5, GAME, "^POLISH IT"),
    (FULLP, 75.5, 80.5, 2.5, GAME, "^ETCH IT"),
    (DISPLAY, 7.6, 10.6, 1, GAME, "PUT IT ON SALE"),  # holds 2 s on the racked sword (Allen: "stay on the frame for a bit longer")
    (CREW, 36.0, 48.0, 6, GAME, "HIRE A CREW"),
    # the cashier reacts while he is still walking in (Allen, draft 1: "have the cashier react before rengoku fully
    # reaches the end"), then back to him arriving at the counter
    (SCENES, 4.7, 7.7, 1, FULL, "SERVE VIP CUSTOMERS"),
    (SCENES, 10.1, 11.75, 1, FULL, ""),  # 0.2 s of the calm face, then the shock at 10.3 (Allen: "only see his blank face for very brief")
    (SCENES, 8.2, 9.4, 1, FULL, ""),
    (SCENES, 13.15, 14.45, 1, FULL, ""),
    (SCENES, 16.6, 19.75, 1, FULL, ""),
]
END = None  # (clip, in, out) for a title card: that clip dimmed and blurred under TITLE. Allen: "no title card at the end"
TITLE, SUB = "SWORDSMITH TYCOON", "PLAY FREE ON ROBLOX"


def text(s, size, y):
    return (f"drawtext=fontfile='{FONT}':text='{s}':fontsize={size}:fontcolor=white:borderw=6:bordercolor=black@0.9:"
            f"x=(w-text_w)/2:y={y}")


def main():
    files = sorted({s[0] for s in SHOTS} | ({END[0]} if END else set()))
    cmd = [FFMPEG, "-y", "-v", "error", "-stats"]
    for f in files:
        cmd += ["-i", os.path.join(CLIPS, f)]
    parts, total = [], 0.0
    for i, (clip, a, b, speed, crop, cap) in enumerate(SHOTS):
        chain = [f"[{files.index(clip)}:v]trim={a}:{b}", f"setpts=(PTS-STARTPTS)/{speed}"]
        if crop:
            chain.append(f"crop={crop}")
        chain += ["scale=1920:1080:flags=lanczos", "fps=60", "setsar=1"]
        if cap:
            chain.append(text(cap.lstrip("^"), 84, "100"))  # every caption at the top (Allen: "on the top not the bottom")
        parts.append(",".join(chain) + f"[v{i}]")
        total += (b - a) / speed
    n = len(SHOTS)
    if END:
        clip, a, b = END
        parts.append(f"[{files.index(clip)}:v]trim={a}:{b},setpts=PTS-STARTPTS,scale=1920:1080,fps=60,setsar=1,"
                     f"gblur=sigma=14,eq=brightness=-0.28,{text(TITLE, 170, '(h-text_h)/2-70')},{text(SUB, 64, '(h/2)+90')}[v{n}]")
        total += b - a
        n += 1
    parts.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,"
                 f"fade=t=in:st=0:d=0.2,fade=t=out:st={total - 0.4:.2f}:d=0.4[v]")
    if MUSIC:
        cmd += ["-ss", str(MUSIC_START), "-i", MUSIC]
        audio = ["-map", f"{len(files)}:a", "-af", f"afade=t=in:d=0.3,afade=t=out:st={total - 1:.2f}:d=1"]
    else:
        cmd += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
        audio = ["-map", f"{len(files)}:a"]
    cmd += ["-filter_complex", ";".join(parts), "-map", "[v]", *audio, "-t", f"{total:.3f}",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", OUT]
    print(f"{n} shots, {total:.2f} s -> {OUT}")
    assert abs(total - 30) < 0.05, total  # the trailer is 30 seconds
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()

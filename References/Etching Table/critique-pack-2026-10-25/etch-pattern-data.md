# Etch patterns: how they're made

Game: a Roblox sword-smithing game (stylised, mostly played on phones). At the Etching Table the player picks a finished sword and one of seven patterns. A stylus then draws the pattern onto the blade in about 3 seconds. An etch adds +15% to the sword's value, and a sword holds one etch at a time.

Every image here comes from the game's own code in Roblox Studio. It was refined on 2026-10-25 after a first critique, and the images from before are in `before/`. Each one shows an Iron sword, fully polished. Spine is up, cutting edge down, and the grey bar is the tang. The 3D metal shine isn't reproduced: the blade is drawn flat in Iron's colour, with a slight light on the edge bevel.

- `by-blade-<blade>.png`: one blade large, with all seven patterns.
- `by-pattern-<pattern>.png`: one pattern on all seven blades at one scale (15 px per cm).
- `phone-size-contrast.png`: Studio renders of katanas in Iron, Black Iron, Gold and Dragonsteel (red scale texture), with all seven patterns. Each is shrunk to phone pixels: a 180 px held sword on top, an 80 px hotbar card below, magnified 3× with hard pixel edges.
- `source/`: the four Luau modules exactly as they are in the game.

## Nothing is stored: every pattern is a formula

No pattern is a picture. Each one is generated from the blade it goes on, from its length in cm and its width at any point, `widthAt(x)`.

- **Width is capped at 7 cm for sizing.** Motif sizes are fractions of `min(width, 7 cm)`, and repeat counts come from the usable length. On a wider face (only the zanbatō, 18.5 cm) the motifs are moved to the middle of the face.
- **Motifs stop before a sloped tip.** The face coordinates follow the cutting edge, so anything drawn where the edge rises into a tip bends with it. The tip starts at the first place past 40% of the length where the width falls faster than 0.25 cm per cm: the zanbatō's chisel, the gladius' long point, a katana's kissaki. Motifs end half a width before it.

**Coordinates on the blade face.** `x` is cm from the blade base. `y` is cm across, measured from the cutting-edge line, or written `w` as a fraction from 0 (edge) to 1 (spine). A pattern is a list of strokes, each a polyline of `{x, y, h}` points, where `h` is the stroke's half-width there. Points are about 0.12 cm apart. Strokes are drawn in list order, with the stylus lifted between them.

**Shared helpers** (in `EtchPatterns.luau`):
- `usable(length, widthAt, limit)` gives the motif zone: from `0.8 × width at the base` to `min(length − 1.9 × width at 90% of the length, limit − 0.5 × width)`, plus the mean width over that zone.
- `taper(t, tip)` ramps 0 → 1 → 0 at both ends of a stroke. `spike(t, peak)` rises to 1 at `peak` along concave flanks, for star rays.
- `hash(i) = frac(sin(i·127.1 + 311.7) · 43758.5453)` is a fixed pseudo-random source, so the "irregular" patterns come out the same every time.

**Drawing.** `EtchCanvas` unrolls the face into an image 1024 px long by 128 px across, split into 1 to 6 strips so a pixel is roughly square on the steel. It draws each stroke as tapered capsules with anti-aliasing, 1.7× the stated width. Each mark has two parts:
- a bright core: the metal's mark colour lifted 55% toward white;
- a dark "engraved groove" halo at 95% opacity. Its reach is 7% of the blade's capped mean width (about 0.16 cm on a tantō, 0.19 cm on a katana, 0.49 cm on the zanbatō). It used to be a fixed 0.24 cm, which buried a tantō's marks and was a hairline on the zanbatō.

A stroke can instead carry a crisp border, `ink = { solid, fade }`: fully dark out to `solid` cm, gone by `solid + fade`. Fracture's shards and Falling Stars' trails use one. The body between marks is see-through on every metal, so the blade's own metal shows around the marks.

**Bare strips.** The outer 3.2% of the width at the edge and at the spine always stays bare metal.

## The seven patterns

| Pattern | What the formula draws, in drawing order |
|---|---|
| **Flame** | Not stroked: one band from the edge line up to `reach(sw)`, with a dark ink line 4.5% of the width along its wavy top. `sw` is the position in capped widths. Band height is `(0.28 + 0.14·(sin²(π·ph^K) − 0.5)) × min(1, 7 cm / width)` of the width, with `K = ln 0.5 / ln 0.45`; humps are `0.75 + 0.3·hash(i)` capped widths long. Its colour is the metal's colour lifted 55% toward white, like the stroked marks. |
| **Eclipse** | `n = floor(usable / (4.4 × mean))` rings, radius 0.33 × width, mid-face. Drawn as: connectors with diamond nodes between rings, ending 0.2 widths clear of each ring; then for each ring a crescent with a ±55° mouth, alternately facing tip and hilt (half-width up to 0.06 × width), with a small sliver arc inside the mouth that stays clear of the crescent's ends; then a four-point star on the tail. |
| **Tide** | `max(2, floor(usable / (4.4 × mean)))` crests. One continuous ribbon: troughs at 16% of the width, backs rising as `t³` to crests at 74%, faces dropping into the trough over 1.3 widths. Then a curl at each crest, then a thin current under each back. |
| **Stormroot** | A zigzag trunk swinging `±(0.10–0.22)` of the width about the middle, with a kink between turns. It swells in from a narrow root over its first 1.2 widths (it used to start as a round blob), peaks at a half-width of 0.072 × width and thins to a point. Branches leave at a third of the trunk's width and fork outward and forward; twigs are 60% of their branch. |
| **Woven Wind** | `round(usable / (7 × mean))` full twists. Two ribbons follow `0.5 ± 0.32·sin(phase)` of the width, widest where they cross the middle. At each crossing one ribbon passes over. The other breaks for the over-ribbon's full drawn width (1.7× plus half its halo) plus a 4% gap, alternating which one. |
| **Fracture** | One connected band. Faults cross the middle every `width × (1.5 − 0.95u) × (0.85 + 0.3·hash)`, where u goes from 0 to 1 along the blade. The band's half-height narrows from 0.38 to 0.18 of the width. Faults lean either way, and one stands upright on each image-strip seam. Cell corners slide at most 8% along the faults. Before 62% of the length, big cells split along a diagonal; after it, cells become diamonds. A shard is dropped only in the last 12%. Shards are inset by half the 6%-of-width fault and carry a solid dark border of the same size, so the faults are clean dark gaps. |
| **Falling Stars** | `max(2, round(usable / (5.5 × mean)))` stars, each at the end of its share of the blade. A star is two concave rays (upright ±0.36, lengthwise ±0.40 widths, peak half-width 0.085) and two short diagonals. Behind it come three thin trails, streaming back toward the guard and rising toward the spine. They start at 0.022 × width and taper out, the middle one up to 2.6 widths long, with half the normal halo. The star is drawn first. |

## What each blade gets

Fully polished blades. Each cell is the stroke count, then the length of pen-down drawing in cm.

| Blade | Length | Image | Eclipse | Tide | Stormroot | Woven Wind | Fracture | Falling Stars |
|---|---|---|---|---|---|---|---|---|
| Tantō | 25.8 cm | 1024×128 | 6 / 22 | 5 / 33 | 19 / 35 | 4 / 35 | 10 / 48 | 14 / 40 |
| Wakizashi | 50.3 cm | 1024×384 | 12 / 52 | 7 / 67 | 34 / 73 | 6 / 79 | 23 / 106 | 21 / 64 |
| Katana | 70.4 cm | 1024×384 | 18 / 77 | 11 / 101 | 50 / 107 | 8 / 114 | 28 / 148 | 28 / 92 |
| Longsword | 90.0 cm | 1024×384 | 15 / 96 | 9 / 124 | 43 / 132 | 8 / 144 | 25 / 190 | 28 / 129 |
| Falchion | 72.0 cm | 1024×256 | 9 / 75 | 5 / 90 | 26 / 100 | 6 / 105 | 16 / 146 | 14 / 95 |
| Gladius | 51.9 cm | 1024×128 | 6 / 43 | 5 / 61 | 14 / 60 | 4 / 59 | 8 / 81 | 14 / 80 |
| Zanbatō | 100.0 cm | 1024×128 | 9 / 95 | 5 / 118 | 24 / 130 | 4 / 132 | 12 / 176 | 14 / 119 |

## Still open

- **The zanbatō leaves a lot of bare steel.** Its motifs are sized for a 7 cm face and sit in a 5–6 cm band in the middle of an 18.5 cm blade. Raising the cap makes them bigger and fewer.
- **The zanbatō's image is only 128 px across,** so a pixel is about 1.4 mm there and its borders are slightly stepped.
- **Iron is the weakest metal for contrast.** Light marks sit on a light, reflective blade, and mostly the dark groove carries them. Black Iron and Dragonsteel read best, and Gold is fine.
- **At hotbar size (80 px) most patterns blur together** except on dark or strongly coloured metals.
- **Double-edged blades** (longsword, gladius) are treated like single-edged ones: `y` runs from the front edge to the back edge.

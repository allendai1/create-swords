---
title: Blade Profile Authoring
status: working notes — all blade numbers are exploratory drafts, not approved
date: 2026-10-19
tags: [forging, swords, prototype, modeling]
---

# Blade Profile Authoring

How the starter blades in `Prototypes/tanto-forge` got their shapes, and how to make new ones with the profile editor.

![[References/Blade Shaping/starter-blades-at-one-scale-v1.png]]

*Universal blank, tantō, wakizashi and katana drafts at one scale (base of each blade at 0 cm; the dark bar is the tang). Captured from the editor.*

## How the tantō shape was chosen

No reference was measured. Claude picked the numbers from general knowledge of real tantō, then exaggerated them slightly for readability, following the approved art direction ([[Create Swords! GDD]]: grounded starter blades, slightly exaggerated, distinct silhouettes). They haven't been checked against photos or against the wakizashi and katana at the same scale.

| Property | Typical real tantō | Study value (`dist/data/tanto.json`) |
|---|---|---|
| Blade length (nagasa) | Under 1 shaku (≈30.3 cm); often 22–28 cm | 26 cm |
| Width at base (motohaba) | about 2.4–2.8 cm | 2.6 cm, narrowing to about 2.0 cm near the point |
| Thickness (kasane) | about 0.5–0.7 cm | 0.7 cm at base → 0.55 → 0.12 at the point |
| Cross-section | Usually hira-zukuri: flat sides, no ridge line | Thickest line 22% of the way from spine to edge, then one long bevel to the edge |
| Curve (sori) | Straight, or slightly inward (uchizori) | Slight outward curve: 0.03 rad total, about 1 mm of sori. **Not true to most tantō; easy to flip.** |
| Point (fukura) | Full, rounded rise of the edge up to the spine | Edge rises over the last 18% of the blade to meet the spine |

The three in-between stages (lengthened bar, tapered preform, forged 90%) are invented to read well while forging. They aren't based on real smithing measurements. The universal blank is 12 × 3.2 × 1.1 cm.

The Japanese length classes give useful anchors for the other starter blades: tantō under 1 shaku (30.3 cm), wakizashi 1–2 shaku (30.3–60.6 cm), katana over 2 shaku. These are standard definitions from general knowledge and weren't sourced in this vault.

## Wakizashi and katana drafts

Built from typical catalogue-style measurements (general knowledge, not measured blades) and stored in each file's `spec`:

| | Tantō | Wakizashi | Katana |
|---|---|---|---|
| Blade length | 26 cm | 48 cm | 72 cm |
| Width at base / near point | 2.6 / about 2.0 cm | 2.9 / 2.15 cm | 3.2 / 2.3 cm |
| Thickness at base | 0.7 cm | 0.72 cm | 0.78 cm |
| Sori | about 0.1 cm | 1.1 cm | 1.7 cm |
| Point section | long rising edge, last 18% | 2.9 cm kissaki | 3.6 cm kissaki |
| Cross-section | flat sides, one long bevel | ridge (shinogi) about a third of the way from the spine | same as wakizashi |
| Tang shown | 6 cm | 10 cm | 14 cm |

All three use the same 12-strike recipe, following the approved "same hit count initially" rule. The in-between stages for the new blades were set by hand in the same way as the tantō's.

## How a blade is described

Every stage shape is a small table of curves along the blade, from `u = 0` (base) to `u = 1` (point):

- `length` in cm, and `curve` (`sori` as a total bend in radians, with `center` and `spread` saying where along the blade it bends)
- `spine` and `edge`: distance from the centreline to the back and to the cutting edge, as `[u, value]` points
- `ridge`: where the thickest line sits, as a fraction from spine to edge
- `thickness`, `edgeThickness`, `spineThickness`

Points are joined with smooth monotone curves, sampled at 64 stations, and turned into one fixed 782-vertex mesh. A blueprint also has its 90% edge allowance and a strike recipe (where each hit lands, its stage, side, turn and flip). The universal blank is shared.

## How easy it is to add a sword

**Easy (data only, minutes in the editor):** any single-edged or straight blade whose outline is a simple function along its length. That covers the wakizashi, katana, nodachi, most sabres, cutlasses, machetes, leaf blades and daggers. Add the file to `dist/data/profiles.json` and the tests and both pages pick it up.

**Possible with care:** double-edged blades (set `spineThickness` near 0 and the ridge at 0.5 so the "spine" becomes a second edge, though grinding still only treats one side as the edge); wavy flamberge edges (need more stations than 64).

**Not supported by this model:** hooks or points that curl back past themselves, forked or split blades, holes, serrations, and surface details such as fullers (hi) or a katana's yokote line. These would need extra mesh features or decals. The Studio `BladeMesh` already draws fullers and a yokote, so those can come back as surface detail.

## Using the profile editor

Open `editor.html` next to the forge study (link in the study's bottom bar).

1. **Start from a blueprint** in the picker, or paste a profile's JSON and choose Load.
2. **Type catalogue measurements** (blade length, sori, widths at base and point, thickness, point section length) and choose *Rebuild refined outline*. Sori converts as `bend ≈ 8 × sori ÷ length`, so a 1.7 cm sori on 72 cm is about 0.19 rad.
3. **Choose *Derive in-between stages*** to generate the lengthened bar and preform from the universal blank and the finished blade. Adjust them if forging looks wrong.
4. **Trace and tweak.** Load a reference photo, scale it in cm, and drag the spine (pale) and edge (orange) points. Double-click to add a point, select one and press Delete to remove it. Other curves (thickness, ridge, edge and spine thickness) edit on a graph. The previous stage shows as a dashed ghost.
5. **Watch the checks** (the same ones the tests run), scrub the 3D preview through every strike, and compare all blueprints at one scale.
6. **Try in forge study** forges the draft right away. To keep it, copy the JSON into `dist/data/` and list it in `profiles.json`. The editor writes the same format as the files, so an unchanged profile round-trips exactly.

Edits stay in the page until copied out. Nothing is saved to the files automatically.

Related: [[Next Session Handoff]] · [[Blade Shaping Study]] · [[Sword Silhouettes]]

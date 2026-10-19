---
title: Blade Profile Authoring
status: working notes — tantō numbers are exploratory, not approved
date: 2026-10-19
tags: [forging, swords, prototype, modeling]
---

# Blade Profile Authoring

How the tantō in `Prototypes/tanto-forge` got its shape, and what it takes to add new sword shapes.

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

## How a blade is described

Every stage shape is a small table of curves along the blade, from `u = 0` (base) to `u = 1` (point):

- `length` in cm, and `curve` (`sori` as a total bend in radians, with `center` and `spread` saying where along the blade it bends)
- `spine` and `edge`: distance from the centreline to the back and to the cutting edge, as `[u, value]` points
- `ridge`: where the thickest line sits, as a fraction from spine to edge
- `thickness`, `edgeThickness`, `spineThickness`

Points are joined with smooth monotone curves, sampled at 64 stations, and turned into one fixed 782-vertex mesh. A blueprint also has its 90% edge allowance and a strike recipe (where each hit lands, its stage, side, turn and flip). The universal blank is shared.

## How easy it is to add a sword

**Easy (data only, about 30–60 minutes of tweaking by hand today):** any single-edged or straight blade whose outline is a simple function along its length. That covers the wakizashi, katana, nodachi, most sabres, cutlasses, machetes, leaf blades and daggers. Copy `tanto.json`, change the numbers, reload, repeat. The tests check coverage, geometry and grinding for any profile once they are pointed at the new file.

**Possible with care:** double-edged blades (set `spineThickness` near 0 and the ridge at 0.5 so the "spine" becomes a second edge, though grinding still only treats one side as the edge); wavy flamberge edges (need more stations than 64).

**Not supported by this model:** hooks or points that curl back past themselves, forked or split blades, holes, serrations, and surface details such as fullers (hi) or a katana's yokote line. These would need extra mesh features or decals. The Studio `BladeMesh` already draws fullers and a yokote, so those can come back as surface detail.

## Making new shapes faster

1. **Type in catalogue specs.** Museum and appraisal records list blade length, base width, point width, thickness and sori in cm. Accept those directly in the data. Sori converts approximately as `bend ≈ 8 × sori ÷ length` (a katana with 1.6 cm sori on 70 cm ≈ 0.18 rad).
2. **A profile editor page.** Drag the spine and edge points over a traced reference photo, with a live 3D preview, the same checks the tests run, and a JSON export. This would cut a new shape to minutes and let non-programmers author blades. Not built yet.
3. **Check shapes together.** Show tantō, wakizashi and katana side by side at one scale before tuning forging animations, as [[Blade Implementation Research]] recommends.

Related: [[Next Session Handoff]] · [[Blade Shaping Study]] · [[Sword Silhouettes]]

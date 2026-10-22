---
title: Katana Hilt
status: v2 hilt in the game (2026-10-19)
type: art
date: 2026-10-19
updated: 2026-10-19
tags: [art, blender, hilt, sword, create-swords]
---

# Katana Hilt

A detailed katana hilt (koshirae) modeled in Blender at Allen's request, using the katana models he pasted into Studio as reference (`Workspace.Nichirins`, `Workspace.Rengoku Katana`).

![[Models/Hilts/review/hilt-vs-today.png]]

*Left: the new hilt. Right: today's in-game hilt (Iron Crossguard recipe) at the same scale.*

## What the references have

Oval grip with a raised criss-cross cord wrap over a contrasting core, so diamonds of the core show between crossings; a metal collar at the guard; an end cap; a decorative guard. Their grips are about 1.6 studs long and 0.22 × 0.12 in section, on blades of about 4.9.

## The model (v1, superseded by v2 below)

Built from code: `Models/Hilts/build_hilt.py` (uses the palette and helpers in `Models/Stations/build_stations.py`), file `Models/Hilts/KatanaHilt.blend`, export `Models/Hilts/KatanaHilt.fbx`.

- **Tsuka:** oval core 0.2 × 0.15 with a slight hourglass, cream "same" (ray skin) showing in the windows.
- **Ito (wrap):** two indigo cords of opposite hand crossing at the centre of each flat face, five crossings per face, alternating over and under; the ends tuck under the fittings.
- **Menuki:** small gold three-bloom ornaments under the wrap, front toward the end cap and back toward the guard.
- **Fuchi and kashira:** gold oval collar and domed end cap, with a dark band on the cap.
- **Tsuba:** iron plate with a gold raised rim, two hitsu-ana and four small round openings cut through; gold seppa washers either side.
- **Habaki:** copper blade collar. The blade stub in the renders is preview only and not exported.

Grip length 1.2 studs (25 cm at the blade's 0.05 studs/cm, a little long for readability), guard diameter 0.52. The root sits at the middle of the grip like the game's `Handle`; the grip runs up +Z with the guard at the bottom. About 13k triangles in 13 parts.

![[Models/Hilts/review/hilt-wrap-closeup.png]]
![[Models/Hilts/review/hilt-tsuba.png]]

## Not done yet

- **Not in the game.** `SmithyCore.buildSword` still builds the hilt from a 0.75-stud cylinder, a block guard and a ball pommel, coloured per recipe in `ReplicatedStorage.Shared.Hilts` (Wooden … Gem). Using this model means importing the meshes and changing `buildSword`; the grip is 1.2 against today's `GRIP_LENGTH` 0.75, which also moves where displayed swords sit on their holders.
- The six hilt recipes are western (crossguard widths 0.8–1.4). Colour variants of this hilt per recipe, or a Japanese recipe set, is an open design choice.
- 13k triangles is fine for one MeshPart but heavy if many swords are visible at once (displayed and held). A lighter version can come from fewer cord steps and core segments.
- **Reference models contain scripts:** each pasted `Nichirins` Tool has 4–15 scripts and `Rengoku Katana` has 2. Free models can carry backdoors; delete them (or at least their scripts) before publishing. Nothing in them was run or changed.

## Wrap v2 test section (2026-10-19)

Allen asked for flatter bands, tighter overlaps, crisp repeating diamond openings, a steadier silhouette, a flatter grip, slimmer gold fittings and a review on the full katana, with one wrap section approved first.

![[Models/Hilts/review/wrap-test-sheet.png]]

- Grip section is a flat-faced oval (superellipse), 0.2 × 0.13, with no hourglass.
- Cords are flat 0.009-thick bands with near-vertical edges. They advance evenly around the outline, so on the flat faces they run as straight diagonals and the openings are straight-edged diamonds (crossing every 0.24).
- Each cord spans 66% of the pitch, so passes overlap along the narrow edges and close them; the cord heading back to the front rides on top there. At each face crossing the upper cord steps up exactly one thickness and lies tight on the other, alternating.
- Code: `flat_band`, `flat_core` and `wrap_test` in `Models/Hilts/build_hilt.py` (`WRAP2` holds the numbers). The section is about 6.5k triangles for 0.72 studs.
- Not yet: the full hilt still uses the first wrap. On approval it gets this wrap, slimmer fittings, and a review on a full katana.

## v2 hilt (2026-10-19)

Allen approved the wrap test section. Full hilt rebuilt with it, reviewed on a full katana. **Allen approved v2.**

![[Models/Hilts/review/hilt-v2-sheet.png]]
![[Models/Hilts/review/katana-full.png]]

- **Grip:** flat-faced oval 0.2 × 0.13, no hourglass. The wrap is exactly four pitches (0.24 each) long, so it starts and ends on a front-face crossing tight against the fuchi and the kashira, with four whole diamond openings per face. That sets the grip at **1.08 studs** from the upper seppa to the kashira end (v1: 1.2; game today: 0.75).
- **Cords:** flat bands as approved. Each point checks whether it lies over the other cord, and the crossing decides who is on top (alternating), so only one cord lifts and they never share a surface. Ends are cut flat under the fittings at slightly different depths.
- **Fittings, slimmer:** fuchi 0.05 tall, kashira 0.06 with a domed top and a thin dark band, seppa 0.012, all following the flat grip shape instead of an oval; guard rim narrowed to 0.026.
- **Menuki:** front one in the third window toward the kashira, back one in a back window toward the fuchi.
- **Review blade:** game-scale katana, 3.5 studs, leaving the habaki on the grip axis and curving toward the spine (sori 0.09), tapering, with a kissaki. Preview only.
- **QA:** `qa_check.py --profile roblox` passes. Accepted warnings: the cords are open ribbons resting on the core; 3 open edges on the guard from the boolean; hidden faces where fittings touch.
- **Size:** about 14.9k triangles (two cords about 4k each). Fine for one MeshPart; for many swords on screen, baking the wrap onto a light core is the next step.
- **Files:** `Models/Hilts/build_hilt.py` (`build_katana`), `KatanaHilt.blend`, `KatanaHilt.fbx` exported with the `roblox` preset (hilt only).

## In the game (2026-10-19)

- Exported a game version (`build_game_hilt`): 8 parts merged by colour role (Same, Ito, Fittings, Kashira, Band, Tsuba, Rim, Habaki) → `Models/Hilts/KatanaHiltGame.fbx`, Roblox QA pass.
- Uploaded with the Open Cloud Assets API (key from `ROBLOX_API_KEY`) as Model asset **74688698547736** on user 14722022, and inserted through the Studio MCP. It imported at exactly 1 Blender unit = 1 stud, which settles the scale test for the FBX `roblox` preset.
- Stored as `ServerStorage.SwordParts.KatanaHilt`, each part relative to the Handle frame. `SmithyCore.buildSword` now clones it onto every held, displayed and anvil-built sword in recipe colours: cord = grip colour, fittings and guard rim = guard colour, end cap = pommel colour (the Gem's blue glass) or guard; ray skin, guard plate, cap band and copper collar are fixed. Grip 1.082, `BladeOffset` 0.613.
- Playtest: six recipe swords and a held Gold-hilt katana built without script errors; Allen confirmed it looks good. The only console errors came from the pasted reference katanas' own scripts.
- A "Disconnected … Recover (Error 0x89AF2)" dialog appeared over the play view while those reference scripts were running; it wasn't clicked. Removing the reference models (or their scripts) is still recommended.
- **Open:** displayed swords sit 0.19 lower than before, so check the storefront holders; triangle count (about 15k per hilt, shared mesh) for crowded scenes. Allen saved the place.

## Smaller blade collar (2026-10-20)

Allen found the copper habaki oversized. In `ServerStorage.SwordParts.KatanaHilt.Habaki`, it was 0.21 wide, 0.084 thick and 0.17 long against a blade root about 0.16 × 0.039. It is now **0.17 wide × 0.052 thick × 0.12 long**, still starting at `BladeOffset` 0.613 (centre X 0.673). Only the template part was resized; the colour and the FBX are unchanged.

![[Models/Hilts/review/habaki-smaller.jpg]]

Checked in a playtest on a katana, a tantō and an etched katana, with no script errors. **Allen needs to save the place.**

## Guard set and Hilt Bench art (2026-10-20)

Allen asked for more hilts: "the pattern of the handle doesn't need to be complex, ideally some different blade guards would be cool." Every recipe keeps the approved grip in its own colours. Five recipes now get their own guard; Wooden keeps the round one.

![[Models/Hilts/review/guard-set-faces.png]]
![[Models/Hilts/review/guard-set-ingame.jpg]]

| Guard | Shape | Recipe |
|---|---|---|
| Kaku | rounded square, four small square windows, two hitsu-ana | Leather Wrap |
| Mokko | four lobes with sharp notches, lobed inlay ring, hitsu-ana | Iron Crossguard |
| Kiku | sixteen-petal chrysanthemum, petal inlay ring | Bronze Guard |
| Kumo | six uneven cloud lobes | Gold Guard |
| Kuruma | round wheel with eight spoked windows | Gem Pommel |

- **Model:** built from code with `build_guard` and the `GUARDS` table in `Models/Hilts/build_hilt.py`, on the flame guard's three colour roles: `<Name>Rim` (band), `<Name>Core` (plate) and `<Name>Inner` (inlay ring outside the seppa, on both faces). Each guard is about 2–5k triangles. Roblox QA passes; the accepted warnings are hidden faces where the parts touch.
- **Upload:** Open Cloud Model assets: Mokko 96466464802775, Kiku 97618754040830, Kaku 95395648141392, Kumo 87714086027628, Kuruma 97695460308097. Stored as `ReplicatedStorage.SwordParts.<Name>Guard` in the Handle frame at X 0.571, same rotation as `FlameGuard`.
- **Colours:** the core is dark iron, the rim takes the recipe's guard colour, and the inlay takes the pommel colour (the Gem's blue glass ring). An etch's guard (Flame) still wins over the recipe's.
- **Hilt Bench cards:** the picker now draws the real hilt and guard, tipped toward the camera so the guard face shows, in place of the old bar, cylinder and ball.

![[Models/Hilts/review/hilt-bench-cards-1.jpg]]
![[Models/Hilts/review/hilt-bench-cards-2.jpg]]

- **Playtest:** one sword per recipe built with the right guard. The real bench flow (blade card, Iron card, three taps) gave a Steel Katana with the Mokko guard, with no script errors. Guards whose meshes haven't loaded yet appeared a moment late on the first open, so `ItemPicker` now preloads `SwordParts`.
- **Review-file note:** `KatanaHilt.blend` has a `Ground` plane at z −0.005 that hides anything below it; lift review models above it.
- `build_hilt.py`'s habaki now matches the smaller game collar (0.17 × 0.052 × 0.12).
- Backups: `ServerStorage.Legacy.SmithyCore_beforeGuardSet`, `Hilts_beforeGuardSet`, `ItemPicker_beforeHiltArt`.

Related: [[Archive/Art/Blender Station Review]] · [[Art/Flame Etch]] · [[Development/Code Map]] · [[Sessions/2026-10-19]]

## Habaki encloses the blade root (2026-10-20)

Allen saw Z-fighting and overlap at the base of an etched sword. The smaller oval habaki (0.17 × 0.052) was thinner at its ends than the blade root (about 0.16 × 0.04, plus the etch skin), so the blade's corners poked through. The blade's end face also sat exactly on the habaki's face.

- `SwordParts.KatanaHilt.Habaki` is now a squared copper **Part, 0.18 wide × 0.06 thick × 0.138 long**, spanning 0.595–0.733 along the grip. It buries the blade's end face (`BladeOffset` 0.613) and tucks 0.006 into the guard.
- Checked on a copper Flame katana from the face and the edge: nothing pokes through. The old mesh is `ServerStorage.Legacy.Habaki_beforeBox`.
- `build_hilt.py`'s oval habaki is now preview-only.

**Then removed (2026-10-20).** Allen: "ideally there is no collar". The habaki is gone from `SwordParts.KatanaHilt` and from `Hilts.dress`. `KatanaHilt`'s `BladeOffset` moved from 0.613 to **0.58**, so the blade root starts inside the seppa and guard instead of floating 0.012 short of the guard. Every script reads that attribute (`SmithyCore`, `SwordRenderer`, `ItemPicker`, `HiltBenchController`). Checked an etched and a plain katana in Edit: the blade goes cleanly into the guard. Backup `Legacy.Hilts_beforeNoHabaki`.

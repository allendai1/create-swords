---
title: Building Redesign
status: in the game (2026-10-20) — shop shell, stone courtyard, bamboo and stone lanterns swapped in
type: art
date: 2026-10-20
updated: 2026-10-20
tags: [art, blender, buildings, bamboo, plot, create-swords]
---

# Building Redesign

Allen asked: "re-design our building in blender, keeping a low-poly style. also the bamboo."

![[Models/Buildings/review/building-redesign-sheet.png]]

## What was built

Source: `Models/Buildings/build_buildings.py`, which uses the helpers and palette from `Models/Stations/build_stations.py` at `DETAIL = "low"` (flat, chunky, no auto bevels). File: `Models/Buildings/Buildings.blend`. Renders: `Models/Buildings/review/`.

- **Same footprint as in Studio**, so floors, stations, lanterns and paths still fit. Blender X = Roblox X and Blender Y = −Roblox Z.
  - **Storefront:** x −45..−20, Roblox z −22..16.
  - **Pavilion:** x −19..31, Roblox z −32..−4.
  - **Heights:** walls up to the 11-stud eave line. Posts sit where the current Studio posts are.
- **Storefront:** an open shop front with two lattice bays (low board wall, sill, bars, lintel, plaster transom) either side of a 12-stud entrance, with a signboard above. The east side stays open onto the courtyard from the front to Roblox z −4. The gable roof (28°) runs its ridge toward the street, with plaster gables and vents.
- **Pavilion:** walls on the back and west only; the front and east stay open. Tie beams and king posts sit at x −5 and 13, with brackets under the front beam. The gable roof is 30°.
- **Shared low-poly language:**
  - Timber posts on stone footings.
  - Walls of plaster panels with a dark board wainscot, a stone sill and a mid tie band, inside and out.
  - Thick eave beams.
  - Two-tone tile ribs, round eave tiles, a chunky ridge with flared end blocks, fascia and barge boards.
- **Bamboo:** three clumps (`Bamboo1..3`) of 5–7 hexagonal stalks.
  - Stalks are 13–17 studs tall and step in at every node ring, in three greens with a slight lean.
  - Fans of long, double-sided low-poly leaves grow on the upper half.
- **Merged by material** for fewer Roblox parts. Storefront ≈ 1.9k triangles in 8 parts, pavilion ≈ 2.0k in 7, bamboo 1.6–2.7k in 5 each.
- **QA (`roblox` profile):** all five pass with no Z-fighting. To get there, every layer that meets a post, beam or sill now runs 0.04–0.1 into it instead of sharing a face; side beams and tie beams sit 0.02–0.04 inside the main beams; bamboo stalk bases are staggered.

## Separate shop and crafting pavilion (2026-10-20)

Allen: "can we separate the shop and the stations so they're not connected".

![[Models/Buildings/review/building-redesign-separate.png]]

- The pavilion moved **8 studs east** (`PAV_DX`, now x −11..39). The walls are 9 studs apart and the eaves about 4, leaving a walkway between the buildings, and the roofs no longer meet.
- The shop's east side is closed, with one 5-stud doorway (lintel, transom, stone step) onto the courtyard at Roblox z about 1. The shop is now a building of its own.
- QA still passes for both, with no Z-fighting.
- **For the game swap:** everything in the pavilion moves +8 in x with it: `Pavilion.Floor`, `Lanterns`, the stations in `Workspace.Smithy` (forge, anvil, ore stand and lever, Etching Table, Hilt Bench, Polishing Station, ingot shelf), the work apron, and the courtyard paving that met the old junction. The pavilion's east end (x 39) passes the lawn curb at x 37.4 only behind the curb's z range, but the eave overhangs it, so check the curb and the expansion lawn.

## Stations outdoors, only the shop indoors (2026-10-20)

Allen: "Can we just have the stations outside, only the shop is inside. there can be an outside courtyard or pavillion for it".

![[Models/Buildings/review/building-redesign-open.png]]

- The crafting pavilion is now **open-air**: a roof on posts with beams, tie beams, king posts and gables, and no walls. A low lattice screen (3.6 high: stone base, rails, slats) runs along the back between the posts, and the west and east sides are fully open.
- It stands on a **paved stone courtyard**: two-tone 3-stud flags in a running bond on a grout bed, flag tops at the 0.2 floor height. The paving runs 3 studs beyond the posts at the front and sides and 2 at the back. It would replace `Pavilion.Floor`.
- The review places the real station models at their game spots (+8 in x): forge, anvil, ore stand and lever, Hilt Bench and Polishing Station. The Etching Table has no Blender model yet.
- QA on the structure passes with no Z-fighting. The flag layer is checked by construction (gaps between flags, raised off the bed), because the full pairwise check timed out on about 200 flags.
- The shop is unchanged from the separated version: the only enclosed building, with its side door onto the courtyard.

## Courtyard only: no roof, no pillars (2026-10-20)

Allen: "remove the roof and the pillars. just keep the stone tile floors".

![[Models/Buildings/review/building-redesign-courtyard.png]]

- The crafting area is now just the **stone-flag courtyard** (`pavilion()` builds only `paving`): about 56 × 33 studs of two-tone flags on a grout bed, flag tops at 0.2, 8 studs east of the shop. The roof, posts, beams and lattice screen are gone. The open-pavilion section above records the step before this.
- The shop is the only building.
- **For the game swap:** the hanging chochin lanterns (`Pavilion.Lanterns`) hung from the pavilion's beams and wall lamps sat on its walls. With nothing to hang from, they need replacing, for example with standing stone lanterns at the courtyard corners.

## In the game (2026-10-20)

Allen: "Looks good. Swap the shop, the stone courtyard and the bamboo into the game, move the stations with it, and use standing stone lanterns."

![[Models/Buildings/review/ingame-overview.jpg]]
![[Models/Buildings/review/ingame-courtyard.jpg]]

- **Stone lantern:** a low-poly standing lantern (`stone_lantern`: square base, hexagonal pillar, platform, light box with paper windows, wide hexagonal roof, finial) was added, 5.1 studs tall. QA passes.
- **Uploads** (Open Cloud, user 14722022):
  - Storefront 107391952159431, Courtyard 108468728394313.
  - Bamboo1–3: 103989737550089, 112411480938286, 138925870861876.
  - StoneLantern 101979524114768.
  - Staged in `ServerStorage.Buildings3D` and coloured from the palette (FBX colours don't import).
- **Orientation:** these imports came in turned 180° about the origin (Roblox = (−bx, bz, by)), so each is rotated back about the origin.
- **Shop:** `Plot.Storefront.Frame`, `Walls` and `Roof` are replaced by `Plot.Storefront.Shell` (7 MeshParts), sunk 0.03.
  - `Floor`, `Interior`, `Lanterns` and `Front` are kept. The shop keeps its kanji signboard; the shell's blank sign face was removed.
  - Walls and timber use **PreciseConvexDecomposition** collision (rebuilt with `AssetService:CreateMeshPartAsync` + `ApplyMesh`, because CollisionFidelity can't be set directly), so the entrance and side door stay open. The roof doesn't collide.
- **Courtyard:** `Plot.Pavilion` was renamed `Plot.Courtyard`, and its frame, walls, roof, earth floor, work apron and hanging lanterns were removed. `Courtyard.Paving` covers x −14..42, z −34..2.5, flag tops at 0.2, with Box collision.
- **Moved +8 in x:** every `Workspace.Smithy` station except `DisplayRack` (forge, anvil, ore roller and lever, Hilt Bench, Etching Table, Polishing Station), plus `Plot.IngotShelf` and the two pots. No script uses absolute positions, so prompts, mounts and the lever animation all follow.
- **Yard:** `CourtyardE` was removed (now under the paving). `CourtyardW` was trimmed to x −20..−14, the path from the shop's side door. `LawnCurb` now starts at z 2.5.
- **Bamboo:** the 12 `Plot.Greenery.Bamboo*` clumps are the three new variants, rotated at random and sunk 0.1. Their leaves don't collide.
- **Stone lanterns:**
  - Five new ones stand in `Courtyard.StoneLanterns` (corners and middle back).
  - The eight older part-built ones in `Plot.StoneLanterns` (gate, corners, apron) became the new model at the same spots and keep their lights; the apron pair moved +8.
  - Every lantern is seated 0.02 into the ground by raycast, with a neon paper window and a warm PointLight.
- **Checks:**
  - The coplanar check between the new meshes and the plot or smithy is clean. The 3 bounding-box matches left are false positives from large merged meshes.
  - Playtest: walked from the front yard into the shop, out the side door and onto the courtyard.
  - The lever roll worked (Iron, Common) and the Polishing Station picker opened. No script errors.
- **Backups:** `ServerStorage.Legacy.Plot_beforeRedesign` and `Smithy_beforeRedesign`.

## Starter Shop (2026-10-20)

Allen: "Our store right now is large enough to be the "Upgraded Store", can we have smaller version that players start with".

![[Models/Buildings/review/starter-shop-sheet.png]]

- `starter_shop()` in `build_buildings.py`: the same style at about a third of the floor area, **16 × 14 studs** (Roblox x −40.5..−24.5, z 2..16) on the same street front.
  - A 6-stud entrance between two lattice bays, with a signboard.
  - Room for **2 sword holders**; the Upgraded Store has 3.
  - A side door onto the courtyard, a tie beam, and a gable roof with its ridge toward the street.
- QA passes with no Z-fighting. Fixing that lowered the door-bay transom 0.02, which also applies to the big shop's side door the next time it's rebuilt.
- **Not in the game yet.** Swapping it in means:
  - parking the big shop (shell, floor, interior, lanterns, noren) as the Upgraded Store;
  - a smaller floor, 2 holder slots, and the noren and lanterns fitted to the new front;
  - moving `DisplayRack` slots, InspectPoints and EntryPoint;
  - deciding how the upgrade is bought, since the tycoon purchase system doesn't exist yet.

## Wider shops and roof fade (2026-10-20)

Allen: "the store and the upgraded store need to be wider" and "when inside the building, the roof should disappear".

- `SHOP_UPGRADED` is now 31 × 38 (x −49..−18) and `SHOP_STARTER` 24 × 14 (x −42..−18), both through `make_shop()`. Uploads: Upgraded 84499583042886, Starter 73411167806206.
- The Upgraded Store replaced `Plot.Storefront.Shell`; floor, front items, interior and lanterns were refit, and the pad was extended to x −50.3. The Starter Shop is still staged only.
- Roof parts are grouped as `Shell.Roof`. `RoofHider` fades them while you stand inside `InsideZone`; the walls stay.

## Beams hide with the roof (2026-10-20)

Allen: "the beams should also disappear in the shop with the roof."

- `join_by_material` now puts `Beam*` (the four eave beams) and `TieBeam` into the `Roof_` group, so they come out as `<shop>_Roof_timber` and fade with the roof. The door lintel (`EntranceBeam`) stays with the walls.
- Re-uploaded: Upgraded Store 93233426162701, Starter Shop 137151111652654. In Studio only the wall timber mesh (now without beams, precise collision) was swapped and `Roof_timber` added under `Shell.Roof`, in the plot and in `ServerStorage.Buildings3D` (UpgradedShop, StarterShop).

## Not done yet

- **Not in the game.** Next steps after approval:
  - Export the FBX files (the `roblox` preset) and upload them through Open Cloud.
  - Colour the parts from their materials (FBX colours don't import).
  - Swap out `Plot.Storefront` / `Plot.Pavilion`'s `Frame`, `Walls` and `Roof`, keeping `Floor`, `Interior`, `Lanterns` and `Front` (noren).
  - Replace the 12 `Plot.Greenery.Bamboo*` clumps with the three variants, rotated.
  - Rerun the coplanar check against the plot.
- Lanterns hang at the old post positions, which still match.

Related: [[Art/Player Plot Review]] · [[Art/Blender Station Review]] · [[Sessions/2026-10-19]]

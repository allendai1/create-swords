---
title: Town Street Redesign References
type: art-reference
status: the simplified map is the live map (2026-10-22); the redesign is parked
updated: 2026-10-22
tags: [town, map, architecture, references]
---

# Town Street Redesign References

Reference pack for a wider, less claustrophobic Japanese town street while preserving six identical player shop-and-workshop plots. Allen requested additional images to give Claude on 2026-10-22.

**Latest exploration, 2026-10-22:** Allen then requested a simplistic map with six plots separated from each other. See `06-simple-separated-plots-v1.png`: six repeated plots, three per side, clear side-lane gaps, broad central paving and minimal scenery. This simpler concept relaxes the connected-frontage emphasis of the earlier images. It remains a proposal; use the real plot template for exact geometry. Its prompt is saved at [[References/Town Street Redesign/simplified-map-prompt]].

![[References/Town Street Redesign/06-simple-separated-plots-v1.png]]

## Intent and constraints

- Keep a built-up **town shopping street** with connected frontage, dark timber, plaster, tiled eaves, noren and lanterns.
- Add breathing room through a broader paved street, a modest market-square widening, side-street openings, small setbacks and varied roof heights.
- Keep all **six player plots identical**, including shop/workshop geometry and full upgrade reserve. Move/rotate copies of the real template; the images do not establish new building dimensions.
- Customer traffic belongs to each player's own progression and upgrades. More customers and more VIP customers affect arrivals at that player's shop; there is no shared customer pool to distribute between the six shops. Relative shop distances are not a customer-competition balancing requirement.
- Players are expected to spend most of their time near their own shop. Side streets can provide visible urban depth without new exploration mechanics or fully functional background businesses.
- Allen corrected the earlier open-green concept because it lost the city/town-street atmosphere. This pack follows the town-street direction.

## Images to give Claude

All seven images are together in `References/Town Street Redesign/`.

| File | Kind | Use |
|---|---|---|
| `00-town-plan-and-street-sketch-v1.png` | Generated sketch from the preceding discussion | Overall proposal: three player plots per side, two staggered side-street openings, a modest central paved widening, town gate and distant shrine. |
| `01-broad-town-street-v1.png` | New generated concept | Main reference for the view from a player's own shop: broad paving, visible sky, connected urban frontage and a secondary landmark. |
| `02-market-intersection-v1.png` | New generated concept | Main reference for a corner and branching side street; openings give depth while buildings keep the town cohesive. |
| `03-town-aerial-v1.png` | New generated concept | Broad massing and six repeated shop/workshop groups in a town context. Use the actual plot template for their proportions and entrances. |
| `References/Japanese Village/Old-Town-in-Takayama-scaled.webp` | Shared original photograph | Timber lattice, eaves, doors, gutters and frontage character. Its narrow street width is not the redesign target. |
| `References/Japanese Village/Edo-Post-Towns_04-Kawagoe-1024x683.jpg` | Shared original photograph | Plaster storehouse fronts, roof variation and attached-shop character. Modern signs, asphalt and road markings are outside the proposed game style. |
| `06-simple-separated-plots-v1.png` | Latest generated simplified concept | Six clearly separated plots with side lanes, broad paving and minimal decoration. Use this for the newest separation/clarity request. |

The duplicate pack copies were consolidated during the 2026-10-22 cleanup. The shared originals remain at `References/Japanese Village/Old-Town-in-Takayama-scaled.webp` and `References/Japanese Village/Edo-Post-Towns_04-Kawagoe-1024x683.jpg`. No new attribution or ownership claim is made for them.

## How to interpret the concepts

These images explain the intended atmosphere and spatial variety. They are not measured drawings or matching camera renders of one exact model. The aerial invents roof arrangements and some extra cross connections; the numbered sketch is illustrative rather than dimensionally exact. Keep all six actual templates identical and use the sketch's simple street structure as the starting proposal, with the street-level images guiding openness and architecture.

The earlier suggested street width of roughly 85 studs, locally widening toward 120, was a concept starting point, not an approved final measurement. Block out the real templates and inspect at normal player-camera height before choosing widths. Additional frontage/background buildings can be shallow shells built from the existing kit; the images' fine surface detail and building count are not mandatory scope.

## Preview

### Overall layout concept

![[References/Town Street Redesign/00-town-plan-and-street-sketch-v1.png]]

### Outside a player's shop

![[References/Town Street Redesign/01-broad-town-street-v1.png]]

### Market intersection

![[References/Town Street Redesign/02-market-intersection-v1.png]]

### Town massing

![[References/Town Street Redesign/03-town-aerial-v1.png]]

### Real architectural references

![[References/Japanese Village/Old-Town-in-Takayama-scaled.webp]]

![[References/Japanese Village/Edo-Post-Towns_04-Kawagoe-1024x683.jpg]]

## Prompt for Claude

Read this note and inspect its seven images, then read the current Six Plots and Japanese Street notes and inspect the actual plot template. Start with the latest brief and image 06: a simplistic map with six identical shop/workshop plots clearly separated by side lanes or buffers, plus a broad paved town street. Use the earlier concepts and real photos for Japanese architecture and atmosphere where compatible with that simpler layout. Preserve each plot's full upgrade space. Customer arrivals are independent per player and driven by that player's upgrades; shop separation is not a shared-customer balancing constraint. Use the real template for dimensions. Keep background streets/scenery modest in scope. Present the blockout dimensions and player-height views before detailed rebuilding.

Generated concepts used the built-in image-generation tool. Exact new generation prompts are saved at [[References/Town Street Redesign/generation-prompts]].

## Built for comparison (2026-10-22)

Allen: "Can you look at Town Street Redesign References for re-designing our map? Can you build it parallel to our existing map so I can compare as well."

`Workspace.TownRedesign` stands 354 studs south of the current street (centre (17.5, 0, −200)), facing the same way: gate west, shrine east. `Workspace.Village` is untouched, and no script reads the new model. It is built by `Models/Village/build_town.luau` (seed 22), which reuses the current street's townhouse kit unchanged. See [[Archive/Project History/Code Map before cleanup — 2026-10-22#Town redesign (2026-10-22)]].

![[References/Town Street Redesign/build-v1-top-both.jpg]]

*From above: the current street (top) and the redesign (bottom).*

| | Current street | Redesign |
|---|---|---|
| Fronts apart | 44 | **72**; **112** at the market widening |
| House rows | 700 long | 560 long |
| Lots | 48.5 × 96, three per side, about 187 apart | The same lots, 180 apart |
| Side streets | None | Two lanes, 24 between fronts and about 120 deep, staggered |
| Townhouses | 54 | 30 on the main street, 10 on the lanes, plus 2 houses closing the lanes (v1: 41 and 14) |

**Layout.** It follows the sketch's simple structure, turned so the street runs west to east like the current one.
- **North side, west to east:** houses, lot N1, houses, the lane, houses, lot N2, houses, a step back out to the main front, houses, lot N3, houses.
- **South side:** the same plan turned 180°, so its lane is at the east end.

**Market widening.** Lots N2 and S2 face each other across the middle.
- They and their neighbours stand 20 further back than the main fronts.
- In front of their neighbour townhouses: four market stalls per side (cream canopy, indigo valance, red chochin, goods on the counter).
- A sakura in a stone planter where the front steps out.

**Lanes.**
- Townhouses face the lane from both sides, behind the 30-deep corner houses.
- Each lane is closed by a two-storey house that ends the view.
- Each lane has the same walkway and water channel as the main street.

**Everywhere:**
- Every front, lane fronts included, keeps the current street's cross-section (walkway, then the water channel 6 to 8 out). So the shop front, its bridge and `CustomerSpawn` fit every lot as they do now.
- Standing andon lamps on every lot's two front corners, on the road.

**Ends:**
- **West:** a roofed gate with the 刀鍛冶の里 sign over a 32-wide opening, with walls out to the bounds.
- **East:** a plaza with a larger torii (×1.35), four stone lanterns, and a bigger shrine on a stone base with steps.

**Preview plots.** Each of the six lots holds a copy of `Workspace.Plot` as a new player first sees it: the Starter shop, one furnace and the free stations.
- Removed from the copies: locked upgrades, pads, spawns, prompts, tags and attributes, so no script picks them up.
- They are snapshots, so rebuild the town to refresh them after the template changes.

![[References/Town Street Redesign/build-v1-shop-view.jpg]]

*From beside lot N2's shop, looking east across the market toward the shrine. Same spot on the current street:*

![[References/Town Street Redesign/current-shop-view.jpg]]

![[References/Town Street Redesign/build-v1-market.jpg]]
![[References/Town Street Redesign/build-v1-lane.jpg]]
![[References/Town Street Redesign/build-v1-gate.jpg]]
![[References/Town Street Redesign/build-v1-shrine.jpg]]
![[References/Town Street Redesign/build-v1-aerial.jpg]]

**Checks (Edit, v1):**
- **Z-fighting:** 0 visible coplanar pairs over 9,472 parts. The check ran in 50-stud slices, counting a hit only inside its own slice. Two overlapping door bridges at the south lane's end were fixed, and the lane-end houses got a walkway.
- **Solid overlaps:** no solid street part sits inside any plot copy.
- **Customer walk:** each lot's walk from `CustomerSpawn` to `EntryPoint` is clear at knee and chest height. Spawns land on the road (N1, N3, S1, S3) or on the market paving (N2, S2).
- **Not done:** Play. In Play, PlotService puts you on your plot in the current street, so the redesign can only be viewed in Edit.

### Calmer fronts (v2, 2026-10-22)

Allen asked "Do you think the map is too busy?" Claude's answer: not overall. The wide street is close to empty, but the fronts are busier than the references. Long runs of one style give a steady roofline there, while v1 changed style and height every house, with many small signs and lanterns. Allen: "try that out." `Workspace.TownRedesign` is now v2. v1 is kept as `ServerStorage.Legacy.TownRedesign_before_20261022045159`.

- **Wider houses:** 22–40 wide, most 24–34 (v1: 16–26). That gives 30 houses on the main street instead of 41.
- **One style per run.** A run is the 2–3 houses between two lots, a lot and a lane, or a lot and the step.
  - Plain stretches are Takayama (two in three) or Tsumago.
  - Storehouses and gable fronts are kept for the corners: the street ends, the lane corners and the step.
  - Round the market: merchant kura or Takayama.
  - Lanes: Takayama, Tsumago or single-storey. The houses closing the lanes are a kura or gable front.
- **Fewer signs and lanterns** on plain townhouses (a 30% sign and 40% lantern chance). Signs went from 36 houses to 15, lanterns from 41 to 15. Shops, kura signboards and the stalls keep theirs. Roofs are tile only; no rust metal roofs.
- **Flagstone paving:** the road, the market and the lanes use a generated MaterialVariant, `MaterialService` `TownFlagstone`.
  - It is on Pavement, 24 studs a tile, tinted (226, 220, 208), and gives big pale flags laid in rows.
  - At 10 studs a tile it read as dark striped planks.
  - Built-in Limestone read as snow.
- **Checks:**
  - 0 visible coplanar pairs over 9,067 parts;
  - no solid street part inside a plot copy;
  - every lot's customer walk clear.
  - The first v2 build showed a bug in the shared house code: at width 25 a pent-roof rafter sat flush with a beam end. The town builder now moves such a rafter by 0.05. `build_street.luau` has the same latent bug, but its seed never triggers it.

![[References/Town Street Redesign/build-v2-street.jpg]]

*Looking east down the main street from near the gate.*

![[References/Town Street Redesign/build-v2-shop-view.jpg]]
![[References/Town Street Redesign/build-v2-market.jpg]]
![[References/Town Street Redesign/build-v2-aerial.jpg]]

**Open:**
- Allen compares the two streets and picks one. Widths 72 and 112 are a first pass.
- Behind the lots there is grass and trees, not the concepts' dense surrounding town.
- The gate is a roofed gate, not a gatehouse.
- The lanes are scenery only.

## Simplified map built (2026-10-22)

Allen: "could we also try a simplified map. there should 3 new files for how to generate it in the vault". The three files are the brief at the top of this note, `06-simple-separated-plots-v1.png` and [[References/Town Street Redesign/simplified-map-prompt]].

`Workspace.TownSimple` stands east of the redesign (centre (640, 0, −200)), facing the same way: gate west, shrine east. It is built by `Models/Village/build_simple.luau` (seed 23), with the same house code as the redesign. No script reads it. See [[Archive/Project History/Code Map before cleanup — 2026-10-22#Simplified map (2026-10-22)]].

![[References/Town Street Redesign/simple-v1-aerial.jpg]]

*From above: the simplified map (right), with the redesign and the current street behind it.*

| | Current street | Redesign (v2) | Simplified |
|---|---|---|---|
| Fronts apart | 44 | 72; 112 at the market | 72; 88 at the middle pair |
| Between plots | Townhouses (continuous row) | Townhouses, a lane on each side | A 24-wide paved lane (half a frontage) |
| Lot centres | about 187 apart | 180 apart | 72.5 apart |
| Town size | 790 × 272 | 690 × 380 | about 350 × 310 inside the walls |
| Other buildings | 54 townhouses | 42 townhouses | 6 small single-storey houses |

**Layout, following image 06 turned to run west to east:**
- **Lots:** three per side at x −72.5, 0 and 72.5, each 48.5 × 96.
  - Each lot has an earth pad with stone edging on its sides and back, just outside the building. Behind the workshop, the pad shows the upgrade reserve.
  - The street front keeps the walkway and water channel, so the shop's door bridge and `CustomerSpawn` fit as before.
- **Lanes:** a 24-wide paved lane separates each pair of neighbouring lots, so no buildings, walls or roofs touch.
  - The north lane between lots 1 and 2 runs on through the back wall. Turned on the south side, that is the lane between S2 and S3, so the two exits are staggered as in the brief.
- **Junction:** the middle pair stands 8 further back, a modest widening at the middle of the street.
- **Paving:** the street uses the pale flagstones. Lanes and the open ground inside the walls use the same flagstones, greyer.
- **Lamps:** standing lamps on every lot's front corners. There are no stalls, trees or filler houses on the street.
- **Edges:**
  - A tile-capped town wall runs round the town, with pillars at the corners and the lane exits.
  - West: the timber gate (刀鍛冶の里).
  - East: a small shrine plaza with a torii (×1.1), four stone lanterns, a sakura and a maple.
  - Six small plain townhouses: one at each end of the street front, and one outside the back wall beside each lane exit.
- **Preview plots:** all six lots hold the inert Starter-shop copies, as in the redesign.

![[References/Town Street Redesign/simple-v1-street.jpg]]

*Looking east from just inside the gate.*

![[References/Town Street Redesign/simple-v1-shop-view.jpg]]

*From the lane mouth beside lot N2, looking east.*

![[References/Town Street Redesign/simple-v1-lane.jpg]]

*Into the lane between N1 and N2, which runs on through the back wall.*

**Checks (Edit):**
- 0 visible coplanar pairs over 4,190 parts.
- No solid part inside any plot copy.
- Each lot's walk from `CustomerSpawn` to `EntryPoint` is clear. The middle pair's spawns land on the junction paving, the others on the street.
- Not done: Play. PlotService still places players on the current street.

**Made the live map (2026-10-22).** Allen: "I compared them. Make the simplified map the live map."
- It is now `Workspace.Village`, the map PlotService uses.
- The plot template stands in lot N2.
- **Parked in `ServerStorage.Legacy`:**
  - the old town street (`Village_before_20261022052609`);
  - the redesign (`TownRedesign_v2_parked`; v1 is `TownRedesign_before_20261022045159`).
- No scripts changed. See [[Archive/Project History/Code Map before cleanup — 2026-10-22#Simplified map (2026-10-22)]].

**Changes the same day:**
- **All six plots always on the map.** Allen: "Why don't you just have all 6 player plots on the map. no need to replace them with another empty building when its already empty". An unclaimed lot shows its plot, empty and unusable; the closed shopfronts are gone.
- **Wider gaps.** Allen: "Also expand the map and separate the houses more".
  - The lanes are now 48 wide (a full shop width), so lot centres are 96.5 apart.
  - The end lanes, small houses, walls, gate and shrine moved out to match.
  - The street itself is unchanged.
- **Gable-front roofs, tried and undone.** Allen: "Also can we try to rotate the roofs so the sides so looking at it front on, the slant is left right". Then: "actually undo it so the roofs face the entrance". The roofs keep their eaves to the street.

![[References/Town Street Redesign/live-street.jpg]]

*From the gate: six empty plots, eaves to the street.*

![[References/Town Street Redesign/live-shop-front.jpg]]

*Lot N2's shop from the street (in Edit the Starter and the Upgraded Store overlap).*

*The gable-front try, for the record:*

![[References/Town Street Redesign/gable-try-starter.jpg]]
![[References/Town Street Redesign/gable-try-upgraded.jpg]]

![[References/Town Street Redesign/live-aerial.jpg]]

**Open:**
- The lanes are bare paving between the workshop side walls: the plain white walls show along every lane.
- Shop doors are now about 96 studs apart along the street.

Related: [[Archive/Art/Japanese Street]] · [[Design/Six Plots]] · [[Development/Code Map]]

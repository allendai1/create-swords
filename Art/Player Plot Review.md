---
title: Player Plot Review
status: build pass done 2026-10-19 — awaiting Allen's walkthrough
type: art
date: 2026-10-19
updated: 2026-10-19
tags: [art, environment, player-plot, review, create-swords]
---

# Player Plot Review

Allen's feedback: the built plot feels small, and the stations feel claustrophobic and tight. This note preserves the screenshot critique and proposed improvements for another Studio pass.

**Scope:** review of Claude's saved screenshots and build notes, not a fresh Studio inspection or traversal test. Allen requested that the critique be saved; the dimensions below are exploratory blockout targets, not finalized construction dimensions. No Studio changes were made during this review.

## Evidence and main finding

![[References/Player Plot/built-overview.jpg]]

![[References/Player Plot/built-storefront.jpg]]

![[References/Player Plot/built-storefront-entrance.jpg]]

Also reviewed the earlier station close-ups in [[Art/Smithy Redesign]] and compared the property with `References/Japanese Village/player-plot-spacious-v2.png` in [[Art/Japanese Village Concept Art]]. The station close-ups predate the storefront addition; use the plot screenshots for the current overall arrangement.

**The property grew around the original workshop, but the active working space did not grow with it.** Equipment remains compressed beneath a shallow roof while much of the property is empty paving or lawn. The issue is the distribution of usable space as well as total plot size.

The build record supports this reading: the original workshop became the crafting wing, largely retaining its station positions. The documented plot is 126 × 58 studs; the workshop is about 41 × 17. These dimensions come from the saved notes, not new measurements.

## Keep

- Connected L-shaped storefront and crafting wings, with separate customer and crafting areas.
- Cream plaster, dark timber, blue-grey tiles, warm lighting, and substantial stylized proportions.
- Expansion reserve that allows visible early/mid/late growth.
- Equipment at usable avatar scale; enlarge its surroundings rather than scaling every prop up.

## Proposed next pass, in priority order

1. **Deepen the crafting wing and bring the anvil forward.** The forge, anvil, and fittings bench read as equipment lined against a wall. Give the anvil its own working area forward of the forge, beneath a deeper canopy, with access from several sides. Keep the core crafting route short.
2. **Give each station a clear working area.** Measure clearance from the outermost props, including bellows, buckets, and tool stands, rather than from station centers. Keep the main route outside the space where a player stands to work.
3. **Use fewer, wider openings across the workshop front.** Closely repeated chunky posts visually cage the stations and obscure them from the courtyard. Retain substantial timber, but place posts between activity zones and leave a broad opening in front of the forge/anvil area.
4. **Add plot depth before more frontage.** The long, shallow property needs more usable working depth. Test the dimensions below before detailed rebuilding, and check the resulting footprint against the eventual six-plot village.
5. **Strengthen the storefront display layout.** Empty holders read low and small on the dark platform while the rear cabinet draws attention. Try taller individual display bases, clear browsing room, and a direct route past the displays to the counter. Judge with actual swords displayed and an NPC browsing.
6. **Connect the outdoor space to the activities.** Extend the crafting floor into the courtyard and connect the expansion lawn to future building/station growth. Group planting around corners and boundaries. Improve the bamboo silhouette: the current bright poles and rounded green clumps read as placeholders. Prioritize these changes over more decorative clutter.

## Initial blockout targets

| Element | Proposed starting target |
|---|---|
| Overall plot | About 126 × 78 studs, compared with the documented 126 × 58 |
| Crafting wing | About 50 × 28 studs, compared with about 41 × 17 |
| Clear passage between station footprints | 6–8 studs |
| Clear space in front of station interactions | 8–10 studs |
| Main circulation route | 10–12 studs |

These are starting hypotheses, not acceptance thresholds or approved final sizes. Passage and working space must be checked together so an occupied station does not consume the route. Avoid increasing repeated travel just to make the property look larger.

## Verification before another detail pass

- [ ] Block out the deeper pavilion, wider openings, and forward anvil with simple geometry first.
- [ ] Place a normal avatar at every station and walk roll → heat → anvil/grind → hilt → display → sale using real input.
- [ ] Rotate the normal player camera at each stop; check posts, roof, walls, and curtains for obstruction or forced zoom.
- [ ] Recheck the dedicated forging camera after moving the anvil, including full katana length and hammer clearance.
- [ ] Check station prompts and interaction reach after repositioning; review dependencies in [[Development/Code Map]] rather than assuming all coordinates are movable.
- [ ] Load the display holders with swords and pass a browsing customer through the gate, shop, and exit without blocking the player's route.
- [ ] Capture matching player-height and overhead screenshots for comparison, then settle dimensions and add detail.

**Recommended direction:** a deeper, more open crafting pavilion, an anvil forward of the forge, and wider station bays. Screenshot evidence establishes visual crowding; a walkthrough is still needed to establish comfort and camera clearance.

## Build pass (2026-10-19)

Allen asked to work on this review. Built in Studio, not just blocked out; dimensions are the review's starting targets.

![[References/Player Plot/v2-overview.jpg]]

| Proposal | Done |
|---|---|
| 1. Deeper crafting wing, anvil forward | New `Pavilion`, **50 × 28 studs** (was 41 × 17); the shallow workshop was archived. Forge on the back wall; the anvil stands on open floor **≈ 9 studs** in front of it, reachable from all sides, with **≈ 10 studs** of floor in front of the smith. |
| 2. Clear area per station | Footprint-to-footprint gaps: ore shrine ↔ forge **6.5**, forge ↔ hilt bench **12**, forge ↔ anvil **8.9**. Main route runs along the open front (z −10…−4) and the courtyard, outside the standing spots. |
| 3. Fewer, wider openings | Four front posts (spans 14 / 18 / 18) with brackets instead of seven; the east side is open toward the lawn. |
| 4. Plot depth | **126 × 78 studs** (was 126 × 58); the extra depth went into the pavilion and a planted strip behind it. |
| 5. Storefront displays | Three tall individual pedestals (cap at 2.6, was 1.2) in two columns either side of a clear aisle from the door to the counter. The drawer chest was toned down. Customers now walk door → their holder's own stand point (per-holder `InspectPoint1..3` plus `EntryPoint`; ShopService change). |
| 6. Outdoor space | The earth floor runs out into the courtyard as a work apron with two stone lanterns. Bamboo was rebuilt (muted stalks with nodes, leaf blades) and grouped at corners and boundaries. |
| Random thoughts: no Z-fighting | Ground layers on fixed heights. A coplanar-face check nudged 180 faces; none were left. Rule recorded in [[Development/Code Map]]. |

![[References/Player Plot/v2-pavilion.jpg]]

![[References/Player Plot/v2-storefront-aisle.jpg]]

**Verification (real input, Studio playtest):** rolled an ingot at the moved ore shrine → heated it 15 s at the moved forge → forged an Obsidian katana to 90% → wooden hilt at the moved hilt bench → displayed it on the back-left holder → an Adventurer walked road → gate → door → that holder's stand point, offered 792 coins → accepted → walked back out without snagging. No script errors; one Roblox asset-type warning that was already there before this pass.

- [x] Forging camera with the full katana: nothing from the pavilion in frame (`v2-forging-camera-katana.jpg`).
- [x] Normal camera at the forge: open floor around every station, no posts or roof in the way (`v2-player-camera-forge.jpg`).
- [x] Prompts work at the new positions (ore, forge, anvil, hilt bench, holders).
- [ ] Not done: grinding wasn't replayed; only one holder was loaded (customers to Slot1/Slot2 use the same code path but weren't walked); a 360° camera rotation at every stop; a phone-sized check; comparing the footprint against the six-plot village.

Related: [[Art/Smithy Redesign]] · [[Art/Japanese Village Concept Art]] · [[Current Status]] · [[Development/Roadmap]] · [[Sessions/2026-10-19]]

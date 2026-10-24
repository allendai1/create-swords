---
title: Workshop Layout
status: built 2026-10-22, playtest pending
type: art
date: 2026-10-22
updated: 2026-10-24
tags: [workshop, stations, layout, plot, create-swords]
---

# Workshop Layout

Allen (2026-10-22) asked to redesign the workshop interior from a top-down screenshot of the old one, keeping the timber-and-plaster building and the six identical plots: "Make the workshop feel cohesive and functional, with simple geometry and restrained detail."

| Before | After |
|---|---|
| ![[References/Workshop Layout/before-top.png]] | ![[References/Workshop Layout/after-top.jpg]] |

*Top views, back wall at the top: the screenshot's left is the workshop's left wall.*

## Layout

- **Supply chest, back-left corner:** an open cedar chest with six compartments replaces the raised alcove with its hatch and chute. *Later the same day the chest became the [[Art/Ore Loot Box]], on the same spot.*
  - The six ore slots' trays sit in the compartments, with a low front so the ore stays in view.
  - The lid leans open against the back wall. The lever stands beside the chest, where it was.
- **Furnaces:** both stand freestanding, 1.65 off the back wall, on one shared stone hearth with a kerb in front. Since 2026-10-23 they use Allen's Japanese smelting furnace model: an arched door whose vents glow while heating.
  - Furnace 2's bay is empty until it is bought, so the hearth already shows where it goes.
- **Anvil, the focal point:** in the middle of the room, about 6 in front of the hearth, between the two furnaces, still facing them.
  - Since 2026-10-22 it is Allen's `fantasy_anvil` (horn, heel with a hardy hole, its own stepped pedestal) standing straight on a round dark stone set in the floor; the timber stump is gone ([[Sessions/2026-10-22#Fantasy anvil]]).
- **Finishing bench, right wall:** three matching sections end to end, from the back toward the shop door: **hilt assembly → polishing → etching**.
  - **Shared look:** dark timber bases with drawers, and counters at waist height (3.0, as before).
  - **Unlocks:** each section belongs to its station, so polishing and etching still appear with their own upgrades.
- **Racks:** the ingot rack (left wall) and the sword rack (by the door) are where they were.
  - *Since 2026-10-24 ([[Sessions/2026-10-24#Refinements 3]]):* **Finished Sword Rack 2** (600, after the first) is a second 6-hook rack on the wall left of the first, 0.9 apart at the plinths. Both racks were raised 1.1 studs (a hanging longsword went through the plinth) and widened slightly (posts ±3.75, hooks 1.18 apart), so longsword guards clear the posts and each other.
- **On the walls:**
  - a tool rail with hammers, tongs and files over the hilt and polishing sections;
  - a shallow shelf over the etching section;
  - a shelf on the left wall between the ingot rack and the chest;
  - tongs and a poker on the back wall right of the hearth.
- **Free floor:** a wide central aisle from the door to the anvil. The front of the right wall and the back-right corner stay free for future equipment.
  - *Since 2026-10-24* the back-right corner holds **Etching Table 2** (2,500, after the Etching Table and the Finished Sword Rack), a copy of the Etching Table mirroring the Hilt Bench, facing into the room, with no demo sword. Only the Sword Etcher uses it; E there opens his crew page.

![[References/Workshop Layout/after-door.jpg]]

*From the shop door, everything bought.*

![[References/Workshop Layout/after-new-player.jpg]]

*What a new player gets: one ore slot, one furnace, the anvil and the hilt section. Buy pads (not shown in Edit) stand in front of each empty place.*

## The bench sections

![[References/Workshop Layout/after-bench.jpg]]

| Section | Equipment |
|---|---|
| Hilt assembly (back) | A wooden blade mount with a notch at the back end (the seated sword's tip rests in it), two guards on a fittings board, a mallet and a punch at the back edge |
| Polishing (middle) | A long polishing stone set into the counter under the blade, a shallow water tray at the back, a cloth |
| Etching (front) | A blade cradle with a practice blank (both hidden while the real sword lies there), the engraving stylus on its rest, an ink pot. *Since [[Sessions/2026-10-23#Refinements 2, second list]] the blank is a real etched demo katana (Copper, Woven Wind), hidden during the etching show.* |

## What stayed the same

- Station names, prompts, mounts and the parts the scripts read; ownership checks, upgrades and crafting.
- The cameras follow the moved stations.
  - The anvil, polishing and etching views were already set from the station itself.
  - The hilt bench's view now turns with the bench, which now faces the right wall. For the bench where it used to stand, this gives exactly the old view.
- The Upgraded Store's push moves the whole workshop, furniture included, 12 back.

Built by `Models/Village/build_workshop.luau`; details and checks in [[Archive/Project History/Code Map before cleanup — 2026-10-22#Workshop layout (2026-10-22)]].

## Tested

In Edit, not in Play:
- Every station can be reached on foot from the door and the spawn, and its prompt is in reach. The camera views were checked with the scripts' own formulas.
- No Z-fighting, the upgrade states, and the push.

Allen's playtest list is in [[Sessions/2026-10-22]].

Related: [[Archive/Art/Japanese Street]] · [[Design/Tycoon Upgrades]] · [[Design/Six Plots]] · [[Development/Code Map]] · [[Sessions/2026-10-22]]

**Ore roller moved (2026-10-23, [[Sessions/2026-10-23#Refinements 2, second list]]):** Allen: "Need to move the ore roller out of the corner, right now it seems like an after thought" — it now stands on the left wall (as seen from the shop) just in front of the Ingot Rack, facing the room, lever end by the rack; its Ore Slot and Lucky Roller pads are in front of it. The delivery door in the shop's right wall now covers its jambs and hangs from a rail.

**Refinements 3 (2026-10-24, [[Sessions/2026-10-24#Refinements 3]]):** besides the second sword rack and Etching Table 2 (above), two changes in the shop, and what the builder doesn't make:
- **The cashier's counter:** the old shop counter is back in the Upgraded Store, in front of the back wall, right of the workshop door, its panel facing the street. It shows once the Cashier (Aki) is hired. Its left end stands 3.7 studs in front of the workshop door, so the doorway stays clear. In Edit it overlaps the starter workshop floor, as every Upgraded Store item does.
- **Wider wall shelves:** the four wall shelves are 0.6 studs wider toward the shop's front, with the cradles under the grip and the axis 0.05 higher. A longsword (6.05 studs) has 0.07 clear at each end, and WallRack3 clears the open delivery door by 0.05.
- **Hand edits, not in the builder:** Rack 2 and both racks' raise and widening, Etching Table 2, the counter and the new pads (only `MergeSlots` is in `build_workshop`'s PADS). The shelf numbers are in `build_workshop`, so its shelf section is safe to rerun.

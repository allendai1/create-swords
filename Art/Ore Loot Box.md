---
title: Ore Loot Box
status: built 2026-10-22, playtest pending
type: art
date: 2026-10-22
updated: 2026-10-24
tags: [ore, roller, loot-box, workshop, create-swords]
---

# Ore Loot Box

Allen (2026-10-22, from [[Archive/Design/Completed quick thoughts — 2026-10-22]]):
- "try to make our ore roller look like a Call of Duty loot box, where you open it, the ore floats around and spins its different types, and then falls down onto the lootbox again"
- "players need to pick up their ores before rolling again. so until then, the ores should just stay on top. there's 6 ore rolls late game, so the box should be able to fit all 6 at a time even if only 1 is rolled early on."

Reference: `References/Concept Art/ingot crate opening`. It shows a wooden chest with dark iron straps and its lid open, with glowing ingots floating above it.

| Open (0.6 s) | Locking in (2.3 s) | Landed (3.6 s) |
|---|---|---|
| ![[References/Ore Loot Box/open-0.6s.jpg]] | ![[References/Ore Loot Box/lock-in-2.3s.jpg]] | ![[References/Ore Loot Box/landed-3.6s.jpg]] |

*Previewed in Edit with all six slots. In play, only the bought slots roll.*

## The box

- **Where:** it replaces the open supply chest in the workshop's back-left corner, on the same spot.
- **Look:** a closed wooden box, 9.4 × 4.6 and 1.75 tall, with a 0.4-thick lid. Two dark iron straps run over the lid and down the front, and an iron handle plate sits on the front.
- **Room for all six:** the lid fits all six ore slots, three across and two deep, even when only slot 1 is bought.
- **The lever** stays beside the box.
- **Empty slots show nothing.** An ingot on the lid always means rolled ore waiting to be collected, so the box on an unclaimed lot is bare.

## The roll (3.6 s)

| Time | What happens |
|---|---|
| 0–0.4 s | The lid flies open, to just past upright, and the inside glows warm |
| 0.2–0.75 s | An ingot rises out of the box over each rolled slot; the back row floats a stud higher than the front |
| Until it locks in | Each ingot spins (6 turns) and flickers through the ore types, both slowing down |
| 2.0 s, then every 0.12 s | One by one, the ingots lock in on their result with a pop and a flash in the rarity's colour |
| 2.75–3.05 s | The lid shuts under them |
| 3.05–3.55 s | They drop onto the lid, each onto its slot |
| 3.6 s | The real ores are there, with the name and rarity label and Collect (E) |

Everyone near the box sees the show. Only the player who rolled can collect.

## Collect first

*Superseded on 2026-10-24 by [[#Spin as often as you like (2026-10-24)]]. The rule as built on 2026-10-22:*

- While any rolled ore lies on the lid, the lever has no prompt. It comes back when the last one is collected.
- Each pull rolls every bought slot.
- With full hands (6 ingots), the ore stays on the lid and the lever stays off until the player uses an ingot and collects.
- This replaces the unlimited re-rolls of 2026-10-20, when a pull replaced uncollected ore.

## Spin as often as you like (2026-10-24)

Allen: "Players should be able to spin the ores as many times as they want" ([[Sessions/2026-10-24#Refinements 3]]).
- The lever is off only while a roll plays.
- Pulling it with ore still waiting puts that ore into your hands first, as many as fit (a NEW card for a first-time metal). What doesn't fit is rolled over.
- Then the show plays as before, and each pull still rolls every bought slot.
- Collecting with E is unchanged, including "Your hands are full".

## Merge Ore Slots (2026-10-24)

A rebirth for the ore box only (Allen: "Its basically a rebirth"; then "Repeatable, gentler prices"). The one exception to "no rebirth/prestige reset" ([[Design/Decisions Log#Refinements 3 — 2026-10-24]]).
- **Where:** once Ore Slots 2–6 are bought, Ore Slot 6's pad spot becomes **Merge Ore Slots**, labelled "Luck ×1.5" (the luck after this merge), with the button "Merge".
- **What it does:** free. Ore Slots 2–6 go back to unbought; slot 1, coins and everything else stay. Luck becomes ×(1 + 0.5 × merges) on top of Lucky Roller, and the Ore Slot pads cost ×1.5 per merge (Slot 2: 75 → 112 → 168; Slot 6: 4,000 → 6,000 → 9,000). Repeatable.
- **Waiting ore** goes to your hands first. With no room for it, the merge is refused ("Your hands are full"), so locked slots never hold ore.
- **No accidents:** the Merge button waits 1 s after the pad appears under you, so mashing Buy through Ore Slot 6 can't merge.
- **After a merge:** the Ingot Rack, Lucky Roller I and Delivery Cart pads stay available; the tutorial counts as done, and "Workshop open!" doesn't replay.
- **Luck past the old ceiling:** the roll used to break above luck ~2.24. Now each merge keeps raising rare ore, while Common and Uncommon never drop under 10%. At Lucky III, Legendary is 1.7%, then 2.6% / 3.5% / 4.4% after 1 / 2 / 3 merges (`Materials.roll`).
- Saved as `merges` ([[Development/Saving]]).

The box is built by `Models/Village/build_workshop.luau`. `ForgeService` holds the rule and the timing, and the client `OreBoxShow` / `OreBoxAnimator` play the show. Details are in [[Archive/Project History/Code Map before cleanup — 2026-10-22#Ore loot box (2026-10-22)]].

## Tested

In Edit, not in Play:
- **The show:** stepped every 0.01 s with six slots.
  - No ingot touches the lid or another ingot.
  - The open lid stays 0.67 off the back wall.
  - Each ingot lands exactly on its slot at full size.
  - Afterwards, the lid is back exactly and no copies are left.
- **The push:** the lid still turns on its hinge after the box moves, as it does in the Upgraded Store push.
- **Z-fighting:** none on the box.
- **Reach:** the spot in front of the box is clear and can be reached from the shop door, and every collect prompt is in reach from there.

Allen's playtest list is in [[Sessions/2026-10-22#Ore loot box and collect first]].

Related: [[Art/Workshop Layout]] · [[Design/Game Design Document]] · [[Design/Tycoon Upgrades]] · [[Development/Code Map]] · [[Sessions/2026-10-22]]

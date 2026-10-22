---
title: Tycoon Upgrades before cleanup — 2026-10-22
status: archived — historical snapshot; superseded by the active note
type: design
date: 2026-10-20
updated: 2026-10-22
tags: [design, tycoon, upgrades, shop, create-swords]
---

# Tycoon Upgrades

Historical snapshot retained during the 2026-10-22 cleanup. Current guidance: [[Design/Tycoon Upgrades]]. Older rules and completion states below may be superseded.

Allen (2026-10-20): "Can you take a look at some photos i dropped into the create game pottery folder. I want something similar where you press buttons on the floor like a typical roblox tycoon to buy the upgrades. Where theres a custom gui to choose where to put your sword. a buy button shows up when you walk over the button so that accidental touching of the button doesnt buy it."

References: `References/Create Pottery! game image reference/`: `upgrade buy button.png`, `stations and upgrades.png`, `shop buy shelf.png`, `shop for sale rack.png`, `shop for sale table.png`.

## How it works

- **Floor pads:** a green pad on a grey base, with the upgrade's name and price floating above it. Each pad sits where its upgrade will appear.
- **Buy button:** standing on a pad brings up a big green **Buy** button over the pad (click, tap or E). Touching the pad alone never buys.
- **Chained:** buying a pad builds its upgrade and reveals the next pad or pads.
- **Display slots:** every empty spot for a sword shows a round **+** marker. The nearest one grows a "For sale" label and an E key. E, click or tap opens the sword picker for that spot.
- **Ownership:** each player has their own plot (since 2026-10-21, [[Design/Six Plots]]), a copy with the same pads; upgrades are bought per plot. Only the owner sees the Buy button and can buy with their coins.
- **Saving:** none yet. Upgrades are session-only, like coins and swords; they reset when the owner leaves. Saving comes with the DataStore pass.

## Answers (Allen, 2026-10-20)

| Question | Answer |
|---|---|
| What pads buy | Sword displays, extra stations, the shop upgrade, racks (helpers later) |
| Unlock order | Chained |
| Displays | Multi-sword displays (3 swords each) |
| Pad position | Where the upgrade will appear |
| Chain and prices | As proposed below |
| Early displays | Floor displays only in the Starter Shop; wall racks unlock inside the Upgraded Store, so nothing needs moving |
| Saving | Session-only for now |
| Ownership | Per player: claim the one plot now |

## Start and chain

**Start:** the Starter Shop with 2 floor holders; the ore lever with 1 stand; the furnace; the anvil; the Hilt Bench.

| # | Pad | Builds | Price (coins) |
|---|---|---|---|
| 1 | Ore Stand 2 | a second stand at the roller | 75 |
| 2 | Display Table 1 | a low table for 3 swords, in the Starter Shop | 150 |
| 3 | Polishing Station | on the courtyard | 250 |
| 4 | Ingot Rack | on the courtyard | 200 |
| 5 | Finished Sword Rack | on the courtyard | 250 |
| 6 | Ore Stand 3 | a third stand | 300 |
| 7 | Furnace 2 | a second furnace | 500 |
| 8 | Upgraded Store | Starter Shop → the two-storey feudal store, with its third floor holder | 1,500 |
| 9 | Wall Sword Rack 1 | a wall rack for 3 swords, inside the Upgraded Store | 400 |
| 10 | Etching Table | on the courtyard | 800 |
| 11 | Display Table 2 · Wall Sword Rack 2 | more displays in the store | 600 · 700 |

Employee pads (like the pottery game's Cashier) come when employees exist. Prices and order are tuning knobs.

## Built (2026-10-20)

- **Models** (Blender, `build_buildings.py`): `wall_sword_holder(rows=3)` → Wall Sword Rack (asset 95282562443763, 452 tris); `sword_table()` → Display Table (72714030293837, 372 tris). QA passes and the coplanar check is clean. Review: `Models/Buildings/review/display-pads-models.png`.
- **Placed:**
  - Display Table 1 (−22, 10) by the Starter Shop's east wall, where it can stay after the upgrade.
  - Display Table 2 (−24.5, −7) in the Upgraded Store.
  - Wall Sword Rack 1 on the west wall (z 1.75); Wall Sword Rack 2 on the east wall (z −17.25).
  - Ore Stands 2 (−9.2, −24) and 3 (−4.5, −19.4); Furnace 2 (2, −21), in front of the forge.
  - The Starter Shop (x −42..−18, z 2..16) and the Upgraded Store share the street front. The third floor holder comes with the Upgraded Store.
- Customers enter at x −30 (through either shop's doorway). Table 2 and the wall racks are reached along the aisle.
- How it works in code: [[Development/Code Map]] (TycoonService).

## Zones and branching chains (2026-10-20)

Allen: "Can you organize the stations so they're more separated. so upgrades have room. and so it's not just a linear path for them." He chose the zoned layout and upgrades branching by zone.

The courtyard (x −14..42, z −34..2.5) is split into zones. Work goes around an open plaza instead of along the back wall: ore yard → forge hall → smithing → finishing → sword rack by the shop's side door → shop. Each zone keeps empty spots for its future upgrades. The lawn east of the courtyard (x 42..74) stays free.

| Zone | Where (centres) | Now | Reserved for later |
|---|---|---|---|
| Ore yard (back right) | lever (35, −31.5); stands in two columns x 31 / 39 | Stand 1 (31, −26), Stand 2 (39, −26), Stand 3 (31, −21); Ingot Rack (35, −10.5) at its front | Stands 4–6 at (39, −21), (31, −16), (39, −16) |
| Forge hall (back middle) | along the back, 6.5 apart | Furnace 1 (8.5, −29), Furnace 2 (15, −29) | Furnace 3 at (21.5, −29) |
| Smithing (middle) | open floor | Anvil (11, −12), Hilt Bench (20, −12) | a second anvil or bench nearby |
| Finishing (back left) | along the back | Polishing Station (−7.5, −29), Etching Table (0, −29) | — |
| By the shop door (front left) | | Finished Sword Rack (−6, −8) | — |

Branching chains (no `after` = buyable from the start):

| Zone | Chain |
|---|---|
| Ore yard | Ore Cart 2 (75) → Ore Cart 3 (300) → Ore Cart 4 (900) → Ore Cart 5 (2,000) → Ore Cart 6 (4,000); Ore Cart 2 → Ingot Rack (200). Since 2026-10-20 the stands are mine carts (ids `OreStand2..6`), six at most (Allen). The pads sit beside each cart's stop. Prices 4–6 are Claude's first guess. Since 2026-10-22 they are shown as Ore Slot 2–6, and the slots lie on the ore loot box's lid, with the pad in front of the box ([[Art/Ore Loot Box]]) |
| Forge hall | Furnace 2 (500) |
| Finishing | Polishing Station (250) → Etching Table (800) |
| By the shop door | Finished Sword Rack (250) |
| Shop | Display Table 1 (150) → Upgraded Store (1,500) → Wall Sword Rack 1 (400) → Wall Sword Rack 2 (700); Upgraded Store → Display Table 2 (600) |
| Delivery (reserved 2026-10-22) | Id `Delivery`, not in `Shared/Upgrades` yet: buying it will swap the shop's left wall panel for the door to the delivery bay (`Shop.DeliveryWall` → `Shop.DeliveryDoor`). Price, pad (`Plot.Pads.Delivery`) and place in the chain come with the delivery board |

This replaces the single chain in "Start and chain" above (same prices).

**Start with a wall rack (2026-10-20):** Allen: "Can we actually have the wall rack be the first thing the players have. so a wall rack that holds 3 swords, and then player can buy another wall rack as the 2nd upgrade. and then a table".

- Players start with one 3-sword wall rack (`Displays.WallRack1`, west wall near the front). Since 2026-10-20 all wall racks use Allen's imported `sword_rack` model (two posts with three hook pairs and a fretwork header), coloured wood. The floor holders are retired (`Legacy.FloorHolders_beforeWallRacks`).
- The shop branch is now: Wall Sword Rack 2 (150, east wall facing it) → Display Table 1 (250, middle of the Starter Shop at (−37, −6)) → Upgraded Store (1,500) → Wall Sword Rack 3 (400, west wall z −16.2) → Wall Sword Rack 4 (700, east wall z −16.2). The Upgraded Store also unlocks Display Table 2 (600). This replaces the shop row in the branching table above.
- The Starter's and the store's side walls are on the same lines, but their posts differ. Racks 1 and 2 sit at z 12, the one stretch clear of posts in both shops, so they stay put through the upgrade.

**Shop sizes (2026-10-20, Allen: "expand it by maybe 3x"):** Starter Shop 31 × 32 (one storey), Upgraded Store 31 × 46 (two storeys). See [[Archive/Art/Building Redesign]].

Supersedes the 100-coin wall-spot prompts of earlier on 2026-10-20 (see [[Archive/Art/Building Redesign]]).

**Workshop layout (2026-10-22):** the workshop pads stand in front of the new places: polishing and etching in front of their bench sections, Furnace 2 in front of its empty hearth bay, the ore slots in front of the supply chest ([[Art/Workshop Layout]]).

**Shop + back-room workshop (2026-10-21):** every pad moved with its upgrade into the one building (positions in [[Archive/Project History/Code Map before cleanup — 2026-10-22#Shop and back-room workshop (2026-10-21)]]). The Ore Cart pads are "Ore Slot 2…6" now, all on one spot in front of the supply alcove; the chain shows one at a time. The Upgraded Store pad is on the shop floor, since the store no longer grows backward.

**The store grows (2026-10-21):** buying the Upgraded Store makes the shop room 12 deeper (48 × 28 → 48 × 40): the workshop behind it, with every station, its pads and the player spawn, is pushed 12 studs further back (Allen: "the shop expands upon upgrade [and] the blacksmith area just gets pushed further back"). Wall Sword Racks 3 and 4 and Display Table 2 stand in the new space. See [[Archive/Art/Japanese Street#Shop grows on the upgrade (2026-10-21)]].

![[References/Japanese Village/upgrade-pushes-workshop.jpg]]

Related: [[Design/Game Design Document]] · [[Design/Workshop Growth]] · [[Development/Roadmap]] · [[Design/Decisions Log]]

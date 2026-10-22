---
title: Tycoon Upgrades
status: built — current catalogue summary; Play and persistence pending
type: design
updated: 2026-10-22
tags: [design, tycoon, upgrades, shop, create-swords]
---

# Tycoon Upgrades

Current recorded purchase behavior, consolidating the later changes to the original 2026-10-20 chain. The old floor-holder start, linear courtyard chain, mine-cart presentation and previous shop dimensions are historical: [[Archive/Design/Tycoon Upgrades before cleanup — 2026-10-22]]. Confirm the live `Shared.Upgrades` catalogue before changing prices; no balance was retuned during cleanup.

## How it works

- Each player owns a plot and purchases its upgrades with coins. Floor pads show an explicit **Buy** button on approach; touching alone does not buy.
- Prerequisites branch by workshop/shop function; buying reveals the next applicable pads. The server checks owner, proximity, prerequisite/state and funds.
- Empty display slots show **+** markers and open the sword picker. Stations and displays remain unusable until unlocked.
- Upgrades are saved with the player's progress (2026-10-22) and re-bought on whichever lot they get when they return, before it appears ([[Development/Saving]]).

## Starting plot

Starter Shop with **one three-sword wall rack**, one ore slot, one unlocked single-ingot furnace, anvil and Hilt Bench. Polishing and etching are purchasable station unlocks. The box physically accommodates all six ore slots from the start; purchased slots determine outputs.

## Recorded branches and prices

| Branch | Chain / price in coins |
|---|---|
| Ore | Ore Slot 2 (75) → 3 (300) → 4 (900) → 5 (2,000) → 6 (4,000) |
| Ingot storage | Ore Slot 2 → Ingot Rack (200), recorded capacity 12 |
| Heating | Furnace 2 (500); the first furnace is already unlocked |
| Finishing | Polishing Station (250) → Etching Table (800); applying the current patterns is free |
| Sword storage | Finished Sword Rack (250), recorded capacity 6 |
| Shop | Wall Sword Rack 2 (150) → Display Table 1 (250) → Upgraded Store (1,500) → Wall Sword Rack 3 (400) → Wall Sword Rack 4 (700) |
| Extra upgraded display | Upgraded Store → Display Table 2 (600) |

Later ore-slot prices were explicitly provisional; all prices still need progression testing. The second ore slot is the first tutorial upgrade **after** the Iron Wakizashi hand-in; since 2026-10-22 the first-session guide points the player to its pad then. The pad itself is buyable from the start, as before.

## Layout and expansion

- The current shop/workshop is one townhouse. Workshop pads sit near the loot box, empty furnace bay and finishing-bench sections. Ore Slot 2–6 pads share a location and reveal sequentially.
- Upgraded Store expands the shop room from about 28 to 40 studs deep and pushes the workshop, stations, workshop pads and spawn **12 studs** back in plot space. Two more wall racks and the second table use the expanded space.
- Per-player station references and turned south plots are already implemented. Check both orientations and the full push in Play.
- `Shop.DeliveryWall` / `Shop.DeliveryDoor` reserve a hidden doorway to the built bay. `Delivery` still needs its catalogue entry, price, prerequisite and pad with the future delivery board.

## Remaining work

Playtest purchases, locked states, camera/prompt positions, display routes and workshop movement; tune affordability; persist upgrades; then add further speed/luck/storage/employee/delivery progression. [[Development/Roadmap]] is the task list, so completion checkboxes are maintained there.

References: [[Development/Code Map]], [[Design/Six Plots]], [[Art/Workshop Layout]], [[Art/Ore Loot Box]]. Original pottery screenshots remain in `References/Create Pottery! game image reference/`.

---
title: Tycoon Upgrades
status: built — current catalogue summary; Play and persistence pending
type: design
updated: 2026-10-24
tags: [design, tycoon, upgrades, shop, create-swords]
---

> **Snapshot 2026-11-01:** Tycoon Upgrades before it was rewritten from the exported catalogue. The current one is [[Design/Tycoon Upgrades]].

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

**Since Economy pass 2 (2026-10-27):** every price is new and each stage's pads also wait for the goal before them (the Katana, Longsword, Sword Crafter, Falchion, Stocker, Shop Promoter, Gladius, Cashier, Sword Etcher, Zanbatō); the Zanbatō, Anvil 3 and Anvil 4 are new pads. The current prices and gates are in [[Design/Economy Pass 2#2. The spine: the next sword, the next employee]]; the chains below still hold, the prices in them are the earlier ones.

**Since the upgrade order (2026-10-28, built, not played):** the Sword Crafter comes before the Longsword, Anvil 3 after the Sword Crafter and Anvil 4 after Anvil 3 and the Stocker; two stages of pads are open at once; the prices and gates are in [[Archive/Design/Upgrade Order Review — 2026-10-28#Built (2026-10-28, not played)]].

**Evening of 2026-10-30** ([[Sessions/2026-10-30#Refinements, evening list]]): the Polishing Station costs **30** (the tutorial's letter wants a polished sword, bought from the first sale); the **Delivery Cart** is buyable from the start; **Polish Boost I** comes after Polishing Station 2; the **Stocker** after the Sword Crafter only; Faster Heating is 10 / 7 / 5 / 4 s. Pads moved: the Sword Crafter's in front of Anvil 2's hearth (plot -4.3, 59.5), the Delivery Cart's to the yard's corner by the bay (30, 0). Pad labels show within 22 studs, drawn over nearby walls and stations, hidden behind walls. Later that evening (Allen's answers): **only the 3 cheapest pads on offer stand on the floor, plus the next sword and the Delivery Cart** (a hidden pad can't be bought; the Sword Crafter's waits its turn like the rest, Allen: "Keep the cap"; [[Design/Refinements Proposals — 2026-10-30]]), and the furnace starts at **15 s** (Faster Heating 15 / 11 / 8 / 6).

**One sword chain since 2026-10-30** ([[Sessions/2026-10-30#One sword chain in the game]]): Wakizashi 60 → Machete 360 → Katana 1,300 → Scimitar 3,600 → Longsword 10,200 → Cutlass 26,000 → Falchion 28,000 → Jian 50,000 → Gladius 60,000 → Khopesh 150,000 → Dadao 160,000 → Rapier 270,000 → Hook Sword 290,000 → Crescent Fang … Seraph 840,000; big swords Zanbatō 88,000 (after the Gladius and the Big Sword Stand) → Claymore 340,000 → Flamberge 430,000.

**Prices since 2026-10-30** ([[Sessions/2026-10-30#New prices: the Zanbatō at 4 h, the crafter a milestone]]; the table below keeps the older history): Jian 28,000, Dadao 60,000, Zanbatō 88,000 (were 80,000 / 170,000 / 250,000); Sword Crafter 40,000 (was 10,000); ×2 for the racks, heat, stations, display holders, Faster Strikes, Polish Boost and the cart pads: Ingot Rack 460, Ingot Rack 2 2,000, Sword Rack 280, Sword Rack 2 2,600, Faster Heating I–III 580 / 3,000 / 5,200, Furnace 2 2,800 (its heating 1,800 / 9,000 / 15,600), Furnace 3 11,600 (7,000 / 36,000 / 62,000), Faster Strikes I–V 500 / 2,000 / 5,000 / 10,000 / 20,000, Polishing Station 200, Polishing Station 2 5,000, Polish Boost I–III 4,000 / 16,000 / 50,000, Etching Table 1,580, Etching Table 2 240,000, Wall Sword Rack 2 106, Back Wall Rack 900, Wall Sword Racks 3–4 6,400 / 30,000, Display Tables 1–6 440 / 9,000 / 42,000 / 46,000 / 80,000 / 120,000, Upgraded Store 6,000, Delivery Cart 6,200, Rickshaw Bays 1–3 2,200 / 44,000 / 152,000. Unchanged: the tutorial's, the ore slots, the other swords, the crew past the crafter, the Cashier, Shop Promoter and Big Sword Stand. The Big Sword Stand comes after the Upgraded Store and the Zanbatō after the Dadao and the stand (no Cashier).

| Branch | Chain / price in coins |
|---|---|
| Ore | Ore Slot 2 (75) → 3 (300) → 4 (900) → 5 (2,000) → 6 (4,000); since 2026-10-24 these prices are ×1.5 per merge, rounded down (Slot 2: 75 → 112 → 168; Slot 3: 300 → 450; Slot 6: 4,000 → 6,000 → 9,000) |
| Ore merge (2026-10-24) | Ore Slot 6 → **Merge Ore Slots** (free, on the ore-slot pad spot; button "Merge", label "Luck ×1.5" on the first merge, then ×2): Slots 2–6 go back to unbought (slot 1, coins and everything else stay); luck ×(1 + 0.5 × merges) (the only luck since Lucky Roller went, 2026-10-25). Repeatable. Waiting ore goes to your hands first; with no room for it the merge is refused. The Merge button waits 1 s after the pad appears under you, so mashing Buy through Ore Slot 6 can't merge. The Ingot Rack, Lucky Roller I and Delivery Cart pads (after Ore Slot 2) stay available after a merge. Saved as `merges` ([[Sessions/2026-10-24#Refinements 3]]) |
| Ingot storage | Ore Slot 2 → Ingot Rack (200), 6 full-size ingots since 2026-10-23 (12 small ones before) → Ingot Rack 2 (500, 2026-10-24, [[Sessions/2026-10-24#Refinement 4]]): a second 6-slot shelf right of the first, 12 ingots in all |
| Heating | Faster Heating III → Furnace 2 (500) since 2026-10-25 (it was buyable from the start); the first furnace is already unlocked |
| Faster heating (2026-10-22) | Faster Heating I (300) → II (900) → III (2,500): 10 → 8 → 6 → 4 s on every furnace; pad in front of the forge |
| Polish boost (2026-10-30) | Polishing Station → Polish Boost I (2,000) → II (8,000) → III (25,000): a full polish adds 13 / 16 / 20% (was 10%) to every polished sword you own; pad beside the station ([[Sessions/2026-10-30#Polish Boost]]) |
| Faster strikes (2026-10-30) | Faster Strikes I (250, after the Wakizashi) → II (1,000) → III (2,500) → IV (5,000) → V (10,000), each after the one before (chained, no milestones, same day): your anvil's strike cycle ×0.9 … ×0.5 (12 strikes ~9 s → ~4.5 s); pad left of Anvil 1's hearth ([[Sessions/2026-10-30#Faster Strikes]]) |
| Employees (2026-10-23) | Ingot Rack + Furnace 2 + Finished Sword Rack (all three since [[Sessions/2026-10-23#Urgency phase 2: the crafter's furnace and your forgotten ingot]]; plots that already own Anvil 2 keep it) → Anvil 2 (1,500) → Sword Crafter (1,000): the hire is its own pad on Anvil 2's spot since [[Sessions/2026-10-23#Refinements 2]] ([[Sessions/2026-10-23#The sword crafter (first employee)]]) → Stocker (2,000, since 2026-10-24; on the Finished Sword Rack's pad spot) |
| More staff (2026-10-24) | One person per role, each on its own pad, placeholder prices ([[Sessions/2026-10-24#Refinements 3]]): Upgraded Store → **Cashier** (3,000): the old shop counter comes back in front of the back wall, right of the workshop door. Display Table 1 → **Shop Promoter** (1,500): on the street left of the shop door. Etching Table + Finished Sword Rack → **Etching Table 2** (2,500): the workshop's right-back corner, mirroring the Hilt Bench; only the Etcher uses it → **Sword Etcher** (2,000), on the same pad spot |
| Delivery (2026-10-22) | Ore Slot 2 → Delivery Cart (1,200): opens the bay door, board and cart; Capacity and Speed are bought in the Deliveries window ([[Sessions/2026-10-22#Deliveries]]) |
| Luck | **Removed 2026-10-25** ([[Sessions/2026-10-25#Refinements 5]]): Lucky Roller I–III (400 / 1,200 / 3,000, 2026-10-22) went; Merge Ore Slots is the only luck. The Ore Slot pad moved onto its spot |
| Blueprints (2026-10-23) | Wakizashi Sword (60) → Katana Sword (400) → Longsword (1,000) → Falchion (2,000) → Gladius (3,500); the western three added later that day, placeholder prices ([[Sessions/2026-10-23#Western swords and automatic hilts]]). All on one pad spot, on the stone circle in the middle of the workshop since 2026-10-25 (by the anvil and furnace before; Allen: "it needs to be in a clearer position"; the first two were named "… Blueprint" until [[Sessions/2026-10-23#More refinements]]); buying one learns it (Allen: "the different swords you get are earned by just buying them through the tycoon pads"; letters no longer teach) [[Sessions/2026-10-23#Refinements 2, second list]] |
| Finishing | Polishing Station (250) → Etching Table (800); applying the current patterns is free. Etching Table 2 (2026-10-24) is in More staff |
| Sword storage | Finished Sword Rack (250), recorded capacity 6 → Finished Sword Rack 2 (600, 2026-10-24): a second 6-hook rack on the wall left of the first, 12 hooks in all. Both racks were raised 1.1 studs and widened slightly so hanging longswords clear the plinth, the posts and each other |
| Shop | Wall Sword Rack 2 (150) → Display Table 1 (250) → Upgraded Store (1,500) → Wall Sword Rack 3 (400) → Wall Sword Rack 4 (700) |
| Extra upgraded display | Upgraded Store → Display Table 2 (600) → Display Table 3 (900) → Display Table 4 (1,300); Tables 3 and 4 (2026-10-23) mirror Tables 1 and 2 on the store's right side |
| Big swords (2026-10-23) | Upgraded Store → Big Sword Stand (2,500, placeholder): one big sword standing upright by the back wall, left of the workshop door; only big blueprints go on it and they go nowhere else ([[Sessions/2026-10-23#Big Sword Stand]]). No big-sword blueprint pad yet. |
| Rickshaw parking (2026-10-23) | Display Table 1 → Rickshaw Bay 1 (500) → 2 (1,500) → 3 (4,000): bays on the street in front of the shop, pads on them; each lets one more customer in at once on top of More Clients, arriving by rickshaw ([[Sessions/2026-10-23#More refinements]]) |
| Decorations (2026-10-29) | No pads: bought in the Decorate window ([[Sessions/2026-10-29#Decorations]]). Planters (150), Wall Scroll (300), Paper Lamp (600), Bonsai Pine (1,000), Stone Lanterns (1,800), Shop Banners (3,000), any order, cosmetic |

Later ore-slot prices were explicitly provisional; all prices still need progression testing. The second ore slot is the first tutorial upgrade **after** the Iron Wakizashi hand-in; since 2026-10-22 the first-session guide points the player to its pad then. The pad itself is buyable from the start, as before.

## Layout and expansion

- The current shop/workshop is one townhouse. Workshop pads sit near the loot box, empty furnace bay and finishing-bench sections. Ore Slot 2–6 pads share a location and reveal sequentially; since 2026-10-24 Merge Ore Slots takes that spot once Slot 6 is bought. The Stocker pad shares the Finished Sword Rack's spot, and the Sword Etcher pad shares Etching Table 2's.
- Upgraded Store expands the shop room from about 28 to 40 studs deep and pushes the workshop, stations, workshop pads and spawn **12 studs** back in plot space. Two more wall racks and the second table use the expanded space. Its grand decor (`Shell.Grand`, 2026-10-22) was removed the same day ([[Sessions/2026-10-22#Shop extras removed, black hilt wrap]]); it keeps the kura upper storey, gold-framed signboard and wall lamps.
- Every wall rack is a three-tier sword shelf since 2026-10-22 (6.7 wide, tiers 2 studs apart); names, ids and prices are unchanged. Since 2026-10-24 each shelf is 0.6 studs wider toward the shop's front, so a longsword fits.
- Per-player station references and turned south plots are already implemented. Check both orientations and the full push in Play.
- `Shop.DeliveryDoor`: the doorway to the bay stands from the start with its sliding door shut, a tease (Allen 2026-10-23); the Delivery Cart slides it open and hangs its curtains. Its pad still appears after Ore Slot 2.
- Floor pads sink in while you stand on them (2026-10-23).
- Since 2026-10-25 a pad's label is one line, "Name · price", shown only within 14 studs of you ([[Sessions/2026-10-25#Refinements 5]]).

## Remaining work

Playtest purchases, locked states, camera/prompt positions, display routes and workshop movement; tune affordability (live-number findings: [[Archive/Design/Alignment Review — 2026-10-23#Balance findings]]); then add further speed/luck/storage/employee/delivery progression. [[Development/Roadmap]] is the task list, so completion checkboxes are maintained there.

References: [[Development/Code Map]], [[Design/Six Plots]], [[Art/Workshop Layout]], [[Art/Ore Loot Box]]. Original pottery screenshots remain in `References/Create Pottery! game image reference/`.

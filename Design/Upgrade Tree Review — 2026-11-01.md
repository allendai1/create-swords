---
title: Upgrade Tree Review — 2026-11-01
status: overhaul built 2026-11-02 (not played); see the section at the end
type: design
updated: 2026-11-01
tags: [review, upgrades, progression, gates, crew, create-swords]
---

# Upgrade Tree Review — 2026-11-01

Allen: "Need to completely re-evaluate the upgrade path tree. Things are locked behind things that seem illogical." / "Upgraded store is available after only 3 shop upgrades, seems a bit quick to get to." / "First employee Taise says it requires 40,000 coins but doesn't state that you also need the stations bought as well."

Sources: live `ReplicatedStorage.Shared.Upgrades`, `Shared.Employees`, `Shared.GemUpgrades` and `TycoonService.standing` (read in Edit, 2026-11-01, after today's Furnace 2 ungating); [[Design/Decisions Log]] (2026-10-28 to 2026-11-01), [[Archive/Design/Upgrade Order Review — 2026-10-28]], [[Design/Reviews 2026-10-31/Handoff — Upgrade progression]], the sim (`Development/sim`, today's `balance.json`). Read only; no Studio or sim file changed.

## How gating works today

- A pad is **on offer** once everything in its `after` is bought.
- It **stands** if it is a sword blueprint (after the tutorial letter), in `PAD_ALWAYS` (Delivery Cart, Anvil 2), or the next step of a chain already begun (`Upgrades.CHAINS`). Of the rest, only the `PAD_CAP` 3 cheapest stand.
- Rule since 2026-10-31: **no gate partway along a chain**; only a chain's first upgrade may wait on something outside it.
- Gem upgrades have no gates. Crafters hire in the crew window by `after` (+ `needs`).

## Current gate graph

| Chain | Item (price) | Waits for |
|---|---|---|
| Ore | Ore Slot 2 (75) → 3 (280) → 4 (2,000) → 5 (9,800) → 6 (20,000) → Merge (free) | each the one before |
| Ingot Rack | Ingot Rack (460) → Ingot Rack 2 (2,000) | **Ore Slot 2** |
| Sword Rack | Sword Rack (280) → Sword Rack 2 (2,600) | — |
| Heat | Faster Heating I (580) → II (3,000) → III (5,200) | — |
| Furnace 2 | Furnace 2 (2,800) → its Heating I–III (1,800 / 9,000 / 15,600) | — (ungated today) |
| Strikes | Faster Strikes I (500) → II–V (2k / 5k / 10k / 20k) | **Wakizashi blueprint** |
| Finishing | Polishing Station (30) | — |
| | Etching Table (1,580) | Polishing Station |
| Polish | Polishing Station 2 (5,000) → Polish Boost I–III (4k / 16k / 50k) | Polishing Station + **Etching Table** |
| Crafters | Anvil 2 (3,400) → Sword Crafter / Taise (40,000) → Anvil 3 (14,000) → Furnace 3 (11,600), Anvil 4 (22,000) | Ingot Rack + Sword Rack + Furnace 2 |
| | F3 Heating I–III (7k / 36k / 62k) | Furnace 3 |
| Crew window | Haru (23k + 10 gems) · Mei (70k + 25) · Kenji (460k + 40) · Rin (710k + 80) | Furnace 3 · Anvil 4 · Mei + **Wakizashi** · Kenji + **Katana** |
| Staff | Stocker (36,000) | Sword Crafter |
| | Cashier (50,000) | Upgraded Store + **Stocker** |
| | Shop Promoter (40,000) | Display Table 1 + **Longsword blueprint** |
| Etcher | Etching Table 2 (240,000) → Sword Etcher (270,000) | Etching Table + Sword Rack + **Gladius blueprint** |
| Shop | Wall Rack 2 (106) → Display Table 1 (440) → Back Wall Rack (900) → **Upgraded Store (6,000)** | — |
| | Wall Rack 3 (6,400) → 4 (30,000); Display Tables 2–6 (9k / 42k / 46k / 80k / 120k); Big Sword Stand (36,000) | Upgraded Store, each the one before |
| Parking | Rickshaw Bay 1 (2,200) → 2 (44,000) → 3 (152,000) | Display Table 1 + **Katana blueprint** |
| Swords | Wakizashi (60) → … → Seraph (840,000), one chain | the sword before (and the tutorial letter) |
| Big swords | Zanbatō (88,000) → Claymore (340,000) → Flamberge (430,000) | Gladius + Big Sword Stand |
| Other | Delivery Cart (6,200), decorations (150–3,000) | — |

## Gates that look illogical

| # | Gate | Why it reads wrong | Severity |
|---|---|---|---|
| 1 | **Upgraded Store** after 3 starter-shop buys | The whole starter shop costs 1,446, the store 6,000. Sim median: manager 36 min, grinder 38, casual 75, efficient 85 — before the Longsword for most, an hour before the first crafter. It's the biggest visual upgrade in the game and comes cheap. | high (Allen's note) |
| 2 | **Rickshaw Bay 1** after the **Katana** | A parking bay for customers waits on a sword blueprint. Nothing about the street needs a katana. | high |
| 3 | **Shop Promoter** after the **Longsword** | A street hawker waits on a sword blueprint. Left over from the 2026-10-28 stage gates. | high |
| 4 | **Etching Table 2** after the **Gladius** | The etcher's table waits on a sword. The 240,000 price already paces it ("the price alone is already enough", 2026-10-29, said of blueprint gates). | medium |
| 5 | **Polishing Station 2** after the **Etching Table** | A second polishing station waits on a different station. A player who polishes but never etches can't get it. | medium |
| 6 | **Faster Strikes I** after the **Wakizashi** | Anvil speed waits on a sword. Its real job is keeping the pad off the floor during the tutorial; the blueprints already do that with a `TutorialDone` check. | low |
| 7 | **Cashier** after the **Stocker** | The Cashier works the Upgraded Store counter; the Stocker is unrelated. It only keeps the crew order. | low |
| 8 | **Kenji `needs` Wakizashi, Rin `needs` Katana** | Dead gates: with one sword chain both are known hours before Mei. | low (no effect) |
| 9 | **Ingot Rack** after **Ore Slot 2** | Ingots come from the furnace, not the second slot. Mild; it does keep the first buys simple. | low |
| — | **Sword Crafter** after Anvil 2 ← Ingot Rack + Sword Rack + Furnace 2 | **Logical** (his input, output, furnace, anvil; Workshop Urgency phase 2). The fault is that the pad shows 40,000 and hides ~6,900 of stations in front of it. Fix the label (handled elsewhere), keep the gate. | keep |

Kept as logical: Furnace 3 → Haru, Anvil 4 → Mei (crew behind their station); Big Sword Stand → Zanbatō (sells only on it); Cashier → Upgraded Store (his post); Stocker → Crafter (Allen: first employee is a milestone, "I don't want Stocker locked behind the sword upgrades"); Polish Boost after Polishing Station 2 (Allen's call 2026-10-30).

## Proposed tree

Three rules, all extensions of existing decisions:
- **Stations before their upgrades, crew behind the station they work** (Workshop Urgency phase 2, Furnace 3 → Haru).
- **No sword blueprint gates anything but swords** (extends 2026-10-29 "Blueprints aren't gated by the crafter anvils" the other way round). The tutorial hides non-sword pads with the same `TutorialDone` check the blueprints use.
- **The shop grows on its own track** (2026-10-29) **but the Upgraded Store costs a real share of shop progress**, not 1,446 coins of it. Its gate stays shop-side only.

| Item | Today | Proposed | Why |
|---|---|---|---|
| Upgraded Store | after the 3 starter buys, 6,000 | after the 3 starter buys **and Rickshaw Bay 1**, **15,000** | Five shop-side buys first (more customers outgrow the small shop), and a price ~2.5× today. Split `CHAINS.Shop` into StarterShop (Wall Rack 2, Table 1, Back Wall Rack) and Store (Upgraded Store onward), so the store is a chain start and the "no gate partway" rule holds. |
| Rickshaw Bay 1 | Display Table 1 + Katana | **Display Table 1** | Street item behind the shop, not a sword. |
| Shop Promoter | Display Table 1 + Longsword | **Upgraded Store + Sword Crafter** | Works the street for the bigger shop; Taise stays the first hire. |
| Cashier | Upgraded Store + Stocker | **Upgraded Store + Sword Crafter** | His counter, plus the first-hire rule; no dependence on the Stocker. |
| Etching Table 2 | Etching Table + Sword Rack + Gladius | **Etching Table + Sword Crafter** | Etcher's station behind the first station of its kind and the first hire; price paces it. |
| Polishing Station 2 | Polishing Station + Etching Table | **Polishing Station** | Second of a station behind the first. |
| Faster Strikes I | Wakizashi | **none** (hidden until `TutorialDone`) | Anvil upgrade, no sword. |
| Kenji / Rin `needs` | Wakizashi / Katana | **drop** (or a late sword if Allen wants one) | No effect today. |
| Sword Crafter | Anvil 2 ← stations | **unchanged**; the pad (or Anvil 2's) lists what's missing | The gate is right; only the label was. |

Optional, needs building and Allen's design: give the starter shop one more holder (a second display table or a fourth wall rack) so "full starter shop" means more than three buys.

### Time to the Upgraded Store (sim, median minutes)

Read-only what-if: today's `balance.json` changed in memory by a scratchpad script, 40 free players a type, 6 h. Not a saved run, not comparable with 150-player runs.

| Scenario | efficient | manager | grinder | casual |
|---|---|---|---|---|
| Today (6,000, 3 buys) | 85 | 36 | 38 | 75 |
| 12,000 | 160 | 56 | 58 | 105 |
| 18,000 | 201 | 62 | 63 | 125 |
| 24,000 | 201 | 70 | 81 | 154 |
| **Proposed (15,000 + Bay 1, all gates above)** | 170 | 57 | 58 | 107 |

- **Sword Crafter unchanged** by the proposal (efficient 132 → 117, manager 110 → 109, grinder 135 → 134, casual 257 → 258). The Zanbatō, Stocker, Promoter and Cashier move ≤ 15 min.
- With the proposal the store lands **about 1 h for engaged players and 1:45 for casual** — before or around the first crafter, still on its own track.
- **Check before trusting:** the efficient type puts the store after the crafter once it costs 12,000+ (it rates shop space low). Read one efficient player's buys (`purchase_times.py`) before taking 170 min as real.
- Rickshaw Bay 1 for grinders moves 81 → 20 min without the Katana gate.

## What needs the sim

- **Data only (re-export `balance.json`, rerun):** every `after` and price above, Kenji/Rin `needs`. The engine reads gates and prices from the export.
- **Also the export/engine:** splitting `CHAINS.Shop` (exported as `B.chains`; `engine.offers` uses it — check it handles the new chain name); hiding Faster Strikes during the tutorial (the engine's tutorial guard only covers blueprints — mirror `TycoonService.standing`).
- **SaveSpec** has chain-rule checks (each chain past its first upgrade waits only inside itself) — rerun after the split.
- Old saves will show odd pads after a gate change: Reset progress ([[old-save-after-gate-change]] — no live players).

## Open for Allen

1. Upgraded Store: 15,000 after Bay 1 (proposed), or a different price, or a new starter-shop holder to fill first?
2. Promoter, Cashier and Etching Table 2 behind the Sword Crafter, keeping Taise as the first hire?
3. Drop Kenji's and Rin's `needs`, or give them a real late sword?


## Overhaul proposal — 2026-11-02

Allen: "we need to overhaul the whole upgrades progression system. it seems too tangled and things are locked behind other upgrades that just don't make sense." Proposal only; nothing changed in Studio.

**One rule:** an upgrade waits only for the one before it in its line, or for the thing it is used with. Swords gate only swords. Price does the pacing. It's Allen's own words applied everywhere: "the price alone is already enough" (2026-10-29), "once an upgrade is available, it shouldn't then be locked behind something else" (2026-10-31), Furnace 2 "no gate" (2026-11-01). Kept: the first hire (Taise) before other staff, and `PAD_CAP` 3.

Cross-line gates go from 32 to 15, and gates on a sword blueprint for a non-sword from 8 to 0.

| Item | Today | Overhaul |
|---|---|---|
| Ingot Rack | Ore Slot 2 | none |
| Faster Strikes I | Wakizashi | none (hidden until `TutorialDone`) |
| Bay 1 | Display Table 1 + Katana | none |
| Polishing Station 2 | Polishing Station + Etching Table | Polishing Station |
| Anvil 2 | Ingot Rack + Sword Rack + Furnace 2 | Ingot Rack + Sword Rack (Taise's route) |
| Furnace 3 | Anvil 3 (in the crafters' chain) | Sword Crafter; leads its own heating chain (Allen: "the furnace is for the crafter they should definitely not get the 3rd furnace before their 1st crafter") |
| Anvil 3 | Sword Crafter (Furnace 3 sat between) | Sword Crafter |
| Haru / Mei | Furnace 3 / Anvil 4 | Anvil 3 / Anvil 4 |
| Kenji / Rin `needs` | Wakizashi / Katana | dropped |
| Upgraded Store | 3 starter buys, 6,000 | 3 starter buys, **15,000** |
| Shop Promoter | Display Table 1 + Longsword | Sword Crafter |
| Cashier | Upgraded Store + Stocker | Upgraded Store + Sword Crafter |
| Etching Table 2 | Etching Table + Sword Rack + Gladius + Flame Etch | Etching Table |
| Delivery capacity/speed levels | Longsword, Falchion / Anvil 3, Anvil 4, Promoter | none past the cart |
| `CHAINS` | Crafters = Anvil 2, Crafter, Anvil 3, Furnace 3, Anvil 4 | Crafters = Anvil 2, Crafter, Anvil 3, Anvil 4; F3Heat = Furnace 3, F3Heat1–3 |

**Sim** (scenario `overhaul` in `Development/sim/scenarios.py`; 40 free players a type, 10 h, same seeds, run `overhaul-check2` in a scratch copy, not saved, after Furnace 3 moved behind the Sword Crafter): the Sword Crafter moves ≤ 15 min for every type (casual 4:39 → 4:37, efficient 2:12 → 1:59), waits over 15 min the same or fewer (10–13). The Upgraded Store moves from 38 min–1:23 to 1:00–2:49 (automator 3:37). Furnace 3 comes 1–15 min after the Sword Crafter for every type. Promoter, Cashier, Etcher, Zanbatō, Mei: within ~20 min of today.

To build: `Shared.Upgrades` gates, prices and `CHAINS`, `Shared.Employees` (`after`, `needs`), the Deliveries gates, `TycoonService.standing` hiding Faster Strikes until `TutorialDone`, SaveSpec's chain checks, then re-export `balance.json` and rerun the sim tests. Old saves: Reset progress.

### Built 2026-11-02

Allen: "work on those". Built in Studio Edit, not played. Two changes from the proposal above, from the code's own reasons and Allen's "the furnace is for the crafter": **Anvil 2 keeps Furnace 2** (the crafter's furnace, "so it doesn't take yours"), and **Furnace 3, Anvil 3 and Haru keep their gates** (Furnace 3 after Anvil 3, Haru after Furnace 3: his furnace, never before the first crafter). **Etching Table 2 keeps the Flame Etch** (an etch for the Etcher to use). **Faster Strikes isn't hidden in the tutorial**: under the pad cap the 3 cheapest new pads then are the Polishing Station, Ore Slot 2 and Wall Rack 2.

Changed: Ingot Rack, Faster Strikes I and Bay 1 have no gate; Polishing Station 2 after the Polishing Station; Shop Promoter after the Sword Crafter; Cashier after the Upgraded Store and the Sword Crafter; Etching Table 2 after the Etching Table and Flame Etch; Kenji and Taru need no blueprint; the Deliveries levels have no gates; the Upgraded Store costs 15,000. `CHAINS` unchanged. Details: [[Sessions/2026-11-02#Upgrade overhaul built]].

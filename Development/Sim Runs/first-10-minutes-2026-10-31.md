---
title: "Sim run: first-10-minutes-2026-10-31"
type: sim-run
updated: 2026-10-31
tags: [sim, tutorial, first-session, create-swords]
---

# Sim run: first-10-minutes-2026-10-31

For [[Design/Reviews 2026-10-31/First 10 Minutes Review]]. The first 15 minutes of 200 free players per type (efficient, manager, grinder, casual), seeds `1:0`–`1:199`, the exported `balance.json` as it stood (exportedAt 1793411392: heat 15 / 11 / 8 / 6, `padCap` 3, 10 strikes), baseline scenario. Hand-action times are Allen's measured playtest medians (`timings.json`: forge 10.8 s at 12 strikes, scaled to 9.0 s at 10; polish 6.2 s; offers answered at a 9.5 s median, 38.6% missed; walking 10.8 studs/s on measured routes).

- `python -m unittest` in `Development/sim`: **38 tests, OK** (9.0 s).
- Run from `Development/sim` with plain `python` by two throwaway scripts outside the vault: one calls `engine.simulate` as is ("stock sim"); the other subclasses `engine.Sim` with four of the game's tutorial rules the sim doesn't have ("game rules", below). **Nothing in `Development/sim` was changed** and nothing was written to `results/`.

## What "game rules" patches in (the sim's disagreements with the code)

| # | The game (code) | The sim today |
|---|---|---|
| 1 | The first letter lands **3 s** after the first sale (`ShopService` `FIRST_LETTER_DELAY`, line 742) | `shop.letterDelay` **45 s** for it too (`engine.on_answer`, line 985) |
| 2 | The first pull is a **Common**, the second an **Uncommon**, while nothing has been collected (`ForgeService.rollFor`, `tutorialPulls`, lines 408–421) | Plain odds from the first pull (a Rare or Epic first sword happens) |
| 3 | While the letter is open a pull brings **Iron** one time in 3, and always on the second (`wantPulls`, lines 396–406) | Plain odds: Iron is 12% a pull, kept when it comes |
| 4 | The Guide asks for **one** buy, the Polishing Station, once the letter's Iron Tantō exists. Nothing prompts the Wakizashi or Ore Slot 2 (Fixes2: "Don't prompt to buy ore slot 2") | `pick_target` treats the Wakizashi, Ore Slot 2 and the station as "the Guide's" buys and targets the **Wakizashi first**, so the letter's first Iron Tantō is usually sold to pay for it |

Not patched, noted:
- 5. The game sends the first customer **the moment the first sword is displayed** (`ShopService` lines 332–334). The sim waits for its 12–22 s spawn clock, and its first offer can be missed like any other.
- 6. The sim pays the day-1 daily (5 gems) at 0:00, so Better Advertising I is bought at 0:00. The game holds the daily window until after the gem step and pays that buy with the letter's 5 gems. Both end at Better Advertising I with 5 gems left, and the tutorial's walk-in gap overrides Advertising until the letter is sent, so nothing moves.
- 7. Policies, not rules: sim players don't wait for the first customer (they forge 2–3 swords first), they re-pull after the first sale for Uncommon+ (casual) or Rare+ (the others), and they use Allen's hand speeds. A kid who takes every ore and waits for each guide line is slower and earns less. Read the coins below as an upper bound.

## Main points (median minute)

| Type | | First sale | Polishing Station | Letter sent (tutorial over) | Wakizashi | Ore Slot 2 |
|---|---|---|---|---|---|---|
| efficient | stock | 1.2 | 2.4 | 4.8 | 2.0 | 3.3 |
| | game rules | 1.2 | 1.3 | **2.6** | 2.3 | 5.4 |
| manager | stock | 1.0 | 1.9 | 4.3 | 1.7 | 2.8 |
| | game rules | 1.0 | 1.2 | **2.4** | 2.0 | 4.7 |
| grinder | stock | 1.2 | 2.5 | 4.7 | 2.1 | 3.2 |
| | game rules | 1.2 | 1.3 | **2.5** | 2.3 | 3.1 |
| casual | stock | 1.8 | 3.7 | 7.7 (184/200 by 15 min) | 3.1 | 4.6 |
| | game rules | 1.8 | 2.1 | **4.0** (200/200) | 3.5 | 4.6 |

- **The sim's tutorial is 2.2–3.7 min too long** (patches 1–4). The money by 10–15 minutes barely moves: coins earned by 15 min are within 7% (efficient 8,511 → 8,353, manager 12,670 → 12,346, grinder 7,215 → 7,442, casual 2,653 → 2,489), so the long-run pacing reports stand.
- **Buy order, game rules (200/200 players each):** PolishStation > Wakizashi > Machete > Ore Slot 2 (efficient, manager); PolishStation > Wakizashi > Ore Slot 2 > Wall Sword Rack 2 (grinder, casual). The stock sim has the Wakizashi before the station for every player.
- **Offers missed in 15 minutes** (game rules): efficient 6, manager 2, grinder 6, casual 7, against 10 / 11 / 10 / 8 sold. About 40% of offer cards go unanswered for everyone but the manager. A card shows only within 35 studs of the camera.

## Game rules, minute by minute (median coins held, 10th–90th; median coins earned; swords made)

**efficient:** tutorial over at 2.6
| min | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 12 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| held | 0 | 12 | 72 | 145 | 168 | 214 | 401 | 430 | 480 | 622 (65–1,959) | 994 | 1,240 |
| earned | 0 | 42 | 162 | 258 | 455 | 678 | 1,214 | 1,664 | 2,449 | 2,996 | 4,883 | 8,353 |
| made | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 12 | 16 |

Buys by 15 min (players of 200, median minute): PolishStation 200 (1.3), Wakizashi 200 (2.3), Machete 200 (5.1), Ore Slot 2 200 (5.4), Wall Sword Rack 2 200 (6.0), Katana 200 (8.6), Ore Slot 3 200 (8.8), Sword Rack 200 (9.3), Faster Strikes I 197 (10.1), Scimitar 138 (12.7), Ingot Rack 126 (13.2), Faster Heating I 110 (13.4), Etching Table 68 (13.5).

**manager:** tutorial over at 2.4
| min | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 12 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| held | 12 | 16 | 134 | 169 | 217 | 409 | 479 | 539 | 606 | 1,026 (173–3,027) | 1,260 | 1,217 |
| earned | 42 | 102 | 226 | 392 | 644 | 1,160 | 1,914 | 2,630 | 3,270 | 4,322 | 7,070 | 12,346 |
| made | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 11 | 13 | 16 |

Buys by 15 min: PolishStation 200 (1.2), Wakizashi 200 (2.0), Machete 200 (4.3), Ore Slot 2 200 (4.7), Wall Sword Rack 2 200 (5.2), Katana 200 (7.2), Ore Slot 3 200 (7.4), Sword Rack 200 (8.0), Faster Strikes I 200 (8.7), Scimitar 193 (11.6), Display Table 1 191 (12.1), Ingot Rack 182 (12.2), Faster Heating I 173 (12.6), Back Wall Rack 163 (12.9), Etching Table 132 (13.4).

**grinder:** tutorial over at 2.5
| min | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 12 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| held | 0 | 12 | 61 | 72 | 91 | 177 | 225 | 280 | 298 | 345 (82–1,168) | 529 | 1,002 |
| earned | 0 | 42 | 162 | 277 | 481 | 785 | 1,221 | 1,630 | 2,253 | 2,869 | 4,558 | 7,442 |
| made | 1 | 3 | 4 | 5 | 5 | 6 | 7 | 8 | 9 | 11 | 13 | 16 |

Buys by 15 min: PolishStation 200 (1.3), Wakizashi 200 (2.3), Ore Slot 2 200 (3.1), Wall Sword Rack 2 200 (4.1), Ore Slot 3 200 (5.5), Sword Rack 200 (6.3), Machete 200 (7.1), Display Table 1 200 (8.2), Ingot Rack 199 (8.9), Faster Strikes I 198 (9.7), Faster Heating I 193 (10.3), Back Wall Rack 185 (11.4), Katana 156 (12.6), Etching Table 108 (13.3).

**casual:** tutorial over at 4.0
| min | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 12 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| held | 0 | 12 | 12 | 58 | 71 | 72 | 96 | 139 | 187 | 196 (39–631) | 256 | 353 |
| earned | 0 | 42 | 42 | 162 | 230 | 308 | 456 | 598 | 827 | 994 | 1,527 | 2,489 |
| made | 1 | 2 | 3 | 3 | 4 | 5 | 6 | 6.5 | 7 | 8 | 10 | 12 |

Buys by 15 min: PolishStation 200 (2.1), Wakizashi 200 (3.5), Ore Slot 2 200 (4.6), Wall Sword Rack 2 200 (6.0), Ore Slot 3 198 (7.9), Sword Rack 193 (9.3), Machete 181 (10.8), Display Table 1 154 (11.9), Ingot Rack 120 (12.5), Faster Strikes I 89 (13.0), Back Wall Rack 25 (13.1), Katana 14 (13.2), Faster Heating I 51 (13.4), Etching Table 7 (14.2).

## Stock sim, for comparison (median coins held at 3 / 5 / 10 / 15 min; earned at 5 / 10 / 15)

| Type | held | earned |
|---|---|---|
| efficient | 42 / 215 / 662 / 1,061 | 644 / 3,252 / 8,511 |
| manager | 98 / 270 / 1,208 / 1,167 | 908 / 5,008 / 12,670 |
| grinder | 42 / 156 / 347 / 830 | 612 / 3,143 / 7,215 |
| casual | 42 / 63 / 167 / 351 | 241 / 1,150 / 2,653 |

## Suggested sim fixes (not made: the sim's code wasn't to be changed in this review)

- `engine.on_answer`: the first letter at 3 s (export `FIRST_LETTER_DELAY` with the shop's numbers).
- `rules.roll` or `engine.task_ore`: `tutorialPulls` (Common, then Uncommon, until an ore is collected) and `wantPulls` (the letter's metal at 1 in 3, always by the second pull).
- `engine.pick_target`: only the Polishing Station is the Guide's buy, while the first letter is open; the Wakizashi and Ore Slot 2 go back to each type's own choice.
- Optional: the first customer at once on the first display (sold == 0).

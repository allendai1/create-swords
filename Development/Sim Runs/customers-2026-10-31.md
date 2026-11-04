# Sim run: customers-2026-10-31

150 players per group, 2 h each; archetypes casual, efficient, automator, rusher, grinder, manager; payers free; scenarios baseline; seed 1. Full report: `Development/sim/results/customers-2026-10-31/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **casual · free:** Sword Crafter —, 0 waits over 15 min between buys
- **efficient · free:** Sword Crafter —, 0 waits over 15 min between buys
- **automator · free:** Sword Crafter 1 h 49, 0 waits over 15 min between buys
- **rusher · free:** Sword Crafter —, 1 waits over 15 min between buys
- **grinder · free:** Sword Crafter —, 0 waits over 15 min between buys
- **manager · free:** Sword Crafter 1 h 51, 0 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | casual | efficient | automator | rusher | grinder | manager |
|---|---|---|---|---|---|---|---|
| Katana | 15 min | 22 min | 9 min | 34 min | 9 min | 13 min | 8 min |
| Longsword | 40 min | 1 h 59 | 42 min | — | 33 min | 1 h 02 | 29 min |
| Sword Crafter | 1 h 30 | — | — | 1 h 49 | — | — | 1 h 51 |
| 1st merge | 2 h 00 | — | 1 h 19 | — | — | 1 h 15 | 1 h 08 |
| Haru (2nd crafter) | 3 h 00 | — | — | — | — | — | — |
| Gems: all Lv. 1 | 3 h 00 | — | — | — | — | — | — |
| Stocker | 3 h 30 | — | — | — | — | — | — |
| Falchion | 4 h 00 | — | 1 h 35 | — | 54 min | 1 h 47 | 1 h 19 |
| 2nd merge | 4 h 00 | — | 1 h 39 | — | — | 1 h 53 | — |
| Mei (3rd crafter) | 6 h 00 | — | — | — | — | — | — |
| Gladius | 6 h 20 | — | — | — | 1 h 30 | — | 1 h 45 |
| Shop Promoter | 6 h 40 | — | — | — | — | — | — |
| 3rd merge | 7 h 00 | — | — | — | — | — | — |
| Cashier | 7 h 30 | — | — | — | — | — | — |
| Zanbatō | 4 h 00 | — | — | — | — | — | — |
| Sword Etcher | 8 h 30 | — | — | — | — | — | — |
| Gems: own pair Lv. 3 | 10 h 00 | — | — | — | — | — | — |
| Kenji (4th crafter) | 10 h 30 | — | — | — | — | — | — |
| Rin (5th crafter) | 12 h 30 | — | — | — | — | — | — |
| Seraph | 20 h 00 | — | — | — | — | — | — |
| Gems: a pair Lv. 5 | 20 h 00 | — | — | — | — | — | — |

## What changed and what it did

Mirrors ShopService's browse wait (Handoff — Customers and values, 2026-10-31): a walk-in with nothing free waits `BROWSE_WAIT` (8 s, now `shop.browseWait` in `balance.json`) inside, then leaves; their place in the shop's cap frees when they give up, not once they're out. `engine.on_spawn` holds the place for walk-in + 8 s (5.55 + 8 = 13.55 s) instead of walk in and out + 2.5 s (13.60 s).

**Effect: none measurable.** The two holds differ by 0.05 s. Same code with the old hold, same seeds: all 900 players sell and earn exactly the same; browses 17,068 against 17,060 in all. The milestone table equals ftue-fixes-2026-10-31's.

Against [[final-2026-10-30]] (400 h run; its coins at 2 h read from the same earned series), medians:

| | efficient | manager | grinder | casual |
|---|---|---|---|---|
| Coins at 2 h, final-10-30 | 452,027 | 571,410 | 356,780 | 124,703 |
| Coins at 2 h, now | 424,514 | 527,113 | 359,277 | 124,167 |
| Sales per hour, now | 54.5 | 69.0 | 54.0 | 44.5 |
| Sword Crafter, final-10-30 | 2 h 03 | 1 h 46 | 2 h 17 | 4 h 21 |
| Sword Crafter, now | past 2 h | 1 h 51 | past 2 h | past 2 h |
| Zanbatō, final-10-30 | 2 h 59 | 2 h 39 | 4 h 06 | 11 h 41 |

Zanbatō is past this run's 2 h for every type. The efficient/manager coin drop (−6 %, −8 %) came with the other 2026-10-31 changes (ramp, FTUE), not this one. Not mirrored: a browser who sees a sword freed during their 8 s would take it in the game; the sim's browser just leaves.

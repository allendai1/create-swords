# Sim run: away-earnings-2026-11-11

20 players per group, 20 h each; archetypes casual, live; payers free; scenarios baseline, no-away; seed 1. Full report: `Development/sim/results/away-earnings-2026-11-11/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **casual · free:** Sword Crafter 18 min, 13 waits over 15 min between buys
- **live · free:** Sword Crafter 19 min, 21 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | casual | live |
|---|---|---|---|
| Katana | 15 min | 14 min | 11 min |
| Sword Crafter | 15 min | 18 min | 19 min |
| Longsword | 40 min | 1 h 15 | 51 min |
| 1st merge | 2 h 00 | 2 h 51 | 3 h 48 |
| Haru (2nd crafter) | 3 h 00 | 3 h 22 | 4 h 23 |
| Gems: all Lv. 1 | 3 h 00 | 5 h 00 | 4 h 00 |
| Stocker | 3 h 30 | 1 h 57 | 2 h 26 |
| Falchion | 4 h 00 | 3 h 17 | 4 h 15 |
| 2nd merge | 4 h 00 | 3 h 41 | 4 h 42 |
| Mei (3rd crafter) | 6 h 00 | 6 h 00 | 8 h 04 |
| Gladius | 6 h 20 | 6 h 24 | 8 h 42 |
| Shop Promoter | 6 h 40 | 4 h 31 | 6 h 05 |
| 3rd merge | 7 h 00 | 5 h 05 | 6 h 52 |
| Cashier | 7 h 30 | 5 h 35 | 7 h 32 |
| Zanbatō | 4 h 00 | 6 h 32 | 8 h 56 |
| Sword Etcher | 8 h 30 | 8 h 08 | 11 h 00 |
| Gems: own pair Lv. 3 | 10 h 00 | — | 12 h 00 |
| Kenji (4th crafter) | 10 h 30 | 9 h 28 | 12 h 35 |
| Taru (5th crafter) | 12 h 30 | 12 h 05 | 18 h 07 |
| Seraph | 20 h 00 | 11 h 00 | 14 h 09 |
| Gems: a pair Lv. 5 | 20 h 00 | — | — |

## Away on vs off (Claude, 2026-11-11)

Medians, minutes of play at 1 h a day, 20 players each, free:

| | casual on | casual off | live on | live off |
|---|---|---|---|---|
| Coins earned in 20 h | 81.9 M | 53.2 M | 46.2 M | 28.2 M |
| Of it, away coins | 22.0 M | 0 | 11.5 M | 0 |
| Cashier | 336 | 336 | 453 | 453 |
| Sword Etcher | 490 | 557 | 660 | 731 |
| Zanbatō | 394 | 414 | 538 | 563 |
| Claymore | 515 | 584 | 687 | 768 |

The Cashier comes at 5.6 h (casual) / 7.6 h (live), day 6-8 at 1 h a day; after him later goals come 5-12% sooner (the Claymore 69-81 min). In the sim the time away is always past Aki's 2 h, so each day adds 24 min of income.

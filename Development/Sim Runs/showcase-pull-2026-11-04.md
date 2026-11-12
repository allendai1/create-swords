# Sim run: showcase-pull-2026-11-04

100 players per group, 8 h each; archetypes efficient, manager, grinder, casual; payers free; scenarios baseline; seed 1. Full report: `Development/sim/results/showcase-pull-2026-11-04/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **efficient · free:** Sword Crafter 17 min, 3 waits over 15 min between buys
- **manager · free:** Sword Crafter 15 min, 3 waits over 15 min between buys
- **grinder · free:** Sword Crafter 20 min, 4 waits over 15 min between buys
- **casual · free:** Sword Crafter 33 min, 7 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | efficient | manager | grinder | casual |
|---|---|---|---|---|---|
| Katana | 15 min | 9 min | 7 min | 13 min | 21 min |
| Sword Crafter | 15 min | 17 min | 15 min | 20 min | 33 min |
| Longsword | 40 min | 48 min | 35 min | 1 h 04 | 2 h 24 |
| 1st merge | 2 h 00 | 2 h 38 | 2 h 21 | 1 h 30 | 4 h 11 |
| Haru (2nd crafter) | 3 h 00 | 2 h 23 | 2 h 01 | 1 h 45 | 4 h 43 |
| Gems: all Lv. 1 | 3 h 00 | — | 7 h 45 | 6 h 22 | 4 h 55 |
| Stocker | 3 h 30 | 1 h 03 | 1 h 03 | 1 h 07 | 2 h 36 |
| Falchion | 4 h 00 | 2 h 58 | 2 h 36 | 2 h 04 | 5 h 37 |
| 2nd merge | 4 h 00 | 3 h 05 | 3 h 11 | 2 h 17 | 5 h 53 |
| Mei (3rd crafter) | 6 h 00 | 4 h 08 | 3 h 07 | 4 h 19 | — |
| Gladius | 6 h 20 | 3 h 46 | 3 h 02 | 3 h 44 | — |
| Shop Promoter | 6 h 40 | 5 h 38 | 5 h 59 | — | 7 h 07 |
| 3rd merge | 7 h 00 | 3 h 52 | 3 h 46 | 3 h 06 | — |
| Cashier | 7 h 30 | 5 h 51 | 6 h 08 | — | — |
| Zanbatō | 4 h 00 | 4 h 52 | 3 h 36 | 4 h 41 | — |
| Sword Etcher | 8 h 30 | 7 h 07 | 7 h 37 | — | — |
| Gems: own pair Lv. 3 | 10 h 00 | 3 h 23 | 3 h 45 | 2 h 53 | — |
| Kenji (4th crafter) | 10 h 30 | — | — | — | — |
| Taru (5th crafter) | 12 h 30 | — | — | — | — |
| Seraph | 20 h 00 | — | — | — | — |
| Gems: a pair Lv. 5 | 20 h 00 | 7 h 43 | 7 h 33 | 6 h 14 | — |

# Sim run: time-model-2

30 players per group, 22 h each; archetypes efficient, manager, grinder; payers free; scenarios timed; seed 1. Full report: `Development/sim/results/time-model-2/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **efficient · free:** Sword Crafter 2 h 05, 24 waits over 15 min between buys
- **manager · free:** Sword Crafter 48 min, 22 waits over 15 min between buys
- **grinder · free:** Sword Crafter 1 h 19, 28 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | efficient | manager | grinder |
|---|---|---|---|---|
| Katana | 15 min | 21 min | 17 min | 23 min |
| Longsword | 40 min | 51 min | 31 min | 1 h 02 |
| Sword Crafter | 1 h 30 | 2 h 05 | 48 min | 1 h 19 |
| 1st merge | 2 h 00 | 2 h 49 | 2 h 43 | 2 h 09 |
| Haru (2nd crafter) | 3 h 00 | 2 h 28 | 2 h 26 | 3 h 44 |
| Gems: all Lv. 1 | 3 h 00 | — | — | 20 h 00 |
| Stocker | 3 h 30 | 2 h 10 | 1 h 00 | 1 h 30 |
| Falchion | 4 h 00 | 1 h 32 | 1 h 39 | 2 h 22 |
| 2nd merge | 4 h 00 | 3 h 29 | 3 h 50 | 3 h 22 |
| Mei (3rd crafter) | 6 h 00 | 5 h 25 | 5 h 23 | 4 h 24 |
| Gladius | 6 h 20 | 2 h 01 | 2 h 11 | 3 h 00 |
| Shop Promoter | 6 h 40 | 14 h 02 | 14 h 09 | 21 h 51 |
| 3rd merge | 7 h 00 | 4 h 19 | 4 h 26 | 3 h 54 |
| Cashier | 7 h 30 | 16 h 35 | 17 h 18 | — |
| Zanbatō | 4 h 00 | 6 h 05 | 5 h 14 | 5 h 03 |
| Sword Etcher | 8 h 30 | 20 h 27 | — | — |
| Gems: own pair Lv. 3 | 10 h 00 | 7 h 46 | 9 h 38 | 7 h 31 |
| Kenji (4th crafter) | 10 h 30 | — | — | — |
| Taru (5th crafter) | 12 h 30 | — | — | — |
| Seraph | 20 h 00 | — | — | — |
| Gems: a pair Lv. 5 | 20 h 00 | — | — | 19 h 49 |

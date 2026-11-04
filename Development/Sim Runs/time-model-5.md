# Sim run: time-model-5

30 players per group, 22 h each; archetypes efficient, manager, grinder; payers free; scenarios timed; seed 1. Full report: `Development/sim/results/time-model-5/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **efficient · free:** Sword Crafter 55 min, 28 waits over 15 min between buys
- **manager · free:** Sword Crafter 44 min, 27 waits over 15 min between buys
- **grinder · free:** Sword Crafter 1 h 19, 28 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | efficient | manager | grinder |
|---|---|---|---|---|
| Katana | 15 min | 17 min | 14 min | 18 min |
| Longsword | 40 min | 43 min | 25 min | 47 min |
| Sword Crafter | 1 h 30 | 55 min | 44 min | 1 h 19 |
| 1st merge | 2 h 00 | 2 h 16 | 2 h 24 | 2 h 21 |
| Haru (2nd crafter) | 3 h 00 | 1 h 10 | 57 min | 1 h 38 |
| Gems: all Lv. 1 | 3 h 00 | — | — | 21 h 46 |
| Stocker | 3 h 30 | 1 h 00 | 49 min | 1 h 34 |
| Falchion | 4 h 00 | 1 h 39 | 1 h 50 | 1 h 48 |
| 2nd merge | 4 h 00 | 3 h 10 | 3 h 02 | 2 h 36 |
| Mei (3rd crafter) | 6 h 00 | 1 h 38 | 1 h 19 | 1 h 55 |
| Gladius | 6 h 20 | 1 h 40 | 1 h 53 | 1 h 50 |
| Shop Promoter | 6 h 40 | 9 h 31 | 9 h 27 | 13 h 40 |
| 3rd merge | 7 h 00 | 3 h 26 | 3 h 16 | 2 h 46 |
| Cashier | 7 h 30 | 10 h 06 | 10 h 08 | 15 h 17 |
| Zanbatō | 4 h 00 | 2 h 42 | 2 h 34 | 2 h 26 |
| Sword Etcher | 8 h 30 | 11 h 51 | 12 h 12 | 15 h 12 |
| Gems: own pair Lv. 3 | 10 h 00 | 7 h 44 | 9 h 47 | 7 h 48 |
| Kenji (4th crafter) | 10 h 30 | 13 h 35 | 14 h 02 | 14 h 22 |
| Taru (5th crafter) | 12 h 30 | 17 h 21 | 18 h 03 | 17 h 22 |
| Seraph | 20 h 00 | 16 h 28 | 17 h 06 | 20 h 02 |
| Gems: a pair Lv. 5 | 20 h 00 | — | — | 21 h 26 |

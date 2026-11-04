# Sim run: time-model-7

30 players per group, 22 h each; archetypes efficient, manager, grinder; payers free; scenarios timed; seed 1. Full report: `Development/sim/results/time-model-7/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **efficient · free:** Sword Crafter 54 min, 30 waits over 15 min between buys
- **manager · free:** Sword Crafter 44 min, 28 waits over 15 min between buys
- **grinder · free:** Sword Crafter 1 h 07, 31 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | efficient | manager | grinder |
|---|---|---|---|---|
| Katana | 15 min | 15 min | 13 min | 17 min |
| Longsword | 40 min | 41 min | 24 min | 45 min |
| Sword Crafter | 1 h 30 | 54 min | 44 min | 1 h 07 |
| 1st merge | 2 h 00 | 2 h 41 | 3 h 02 | 2 h 39 |
| Haru (2nd crafter) | 3 h 00 | 1 h 19 | 1 h 18 | 2 h 00 |
| Gems: all Lv. 1 | 3 h 00 | — | — | 20 h 39 |
| Stocker | 3 h 30 | 1 h 02 | 53 min | 1 h 23 |
| Falchion | 4 h 00 | 3 h 43 | 3 h 52 | 3 h 29 |
| 2nd merge | 4 h 00 | 4 h 10 | 4 h 59 | 3 h 56 |
| Mei (3rd crafter) | 6 h 00 | 2 h 03 | 1 h 16 | 2 h 21 |
| Gladius | 6 h 20 | 3 h 52 | 3 h 55 | 3 h 33 |
| Shop Promoter | 6 h 40 | 11 h 28 | 11 h 20 | 15 h 20 |
| 3rd merge | 7 h 00 | 5 h 33 | 5 h 15 | 4 h 13 |
| Cashier | 7 h 30 | 12 h 52 | 12 h 55 | 17 h 19 |
| Zanbatō | 4 h 00 | 4 h 35 | 4 h 06 | 3 h 44 |
| Sword Etcher | 8 h 30 | 13 h 53 | 14 h 02 | 16 h 13 |
| Gems: own pair Lv. 3 | 10 h 00 | 7 h 56 | 9 h 44 | 7 h 36 |
| Kenji (4th crafter) | 10 h 30 | 15 h 07 | 15 h 20 | 15 h 16 |
| Taru (5th crafter) | 12 h 30 | 18 h 58 | 19 h 14 | 18 h 17 |
| Seraph | 20 h 00 | 18 h 06 | 18 h 23 | 20 h 48 |
| Gems: a pair Lv. 5 | 20 h 00 | — | — | 20 h 21 |

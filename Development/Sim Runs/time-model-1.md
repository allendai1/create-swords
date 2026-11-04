# Sim run: time-model-1

30 players per group, 22 h each; archetypes efficient, manager, grinder; payers free; scenarios timed; seed 1. Full report: `Development/sim/results/time-model-1/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **efficient · free:** Sword Crafter 1 h 11, 27 waits over 15 min between buys
- **manager · free:** Sword Crafter 57 min, 26 waits over 15 min between buys
- **grinder · free:** Sword Crafter 1 h 18, 30 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | efficient | manager | grinder |
|---|---|---|---|---|
| Katana | 15 min | 16 min | 13 min | 21 min |
| Longsword | 40 min | 25 min | 21 min | 41 min |
| Sword Crafter | 1 h 30 | 1 h 11 | 57 min | 1 h 18 |
| 1st merge | 2 h 00 | 2 h 12 | 1 h 35 | 1 h 13 |
| Haru (2nd crafter) | 3 h 00 | 1 h 36 | 1 h 16 | 2 h 33 |
| Gems: all Lv. 1 | 3 h 00 | — | — | 21 h 22 |
| Stocker | 3 h 30 | 1 h 16 | 1 h 03 | 1 h 32 |
| Falchion | 4 h 00 | 1 h 00 | 50 min | 1 h 52 |
| 2nd merge | 4 h 00 | 2 h 34 | 1 h 50 | 2 h 08 |
| Mei (3rd crafter) | 6 h 00 | 3 h 30 | 2 h 56 | 2 h 48 |
| Gladius | 6 h 20 | 1 h 06 | 55 min | 1 h 58 |
| Shop Promoter | 6 h 40 | 10 h 32 | 10 h 07 | 15 h 33 |
| 3rd merge | 7 h 00 | 3 h 10 | 2 h 37 | 2 h 41 |
| Cashier | 7 h 30 | 10 h 41 | 10 h 18 | 17 h 07 |
| Zanbatō | 4 h 00 | 4 h 18 | 2 h 51 | 3 h 05 |
| Sword Etcher | 8 h 30 | 13 h 09 | 13 h 19 | 13 h 34 |
| Gems: own pair Lv. 3 | 10 h 00 | 7 h 34 | 10 h 20 | 7 h 37 |
| Kenji (4th crafter) | 10 h 30 | 13 h 44 | 13 h 54 | 15 h 30 |
| Taru (5th crafter) | 12 h 30 | 15 h 25 | 15 h 36 | 17 h 55 |
| Seraph | 20 h 00 | 17 h 33 | 17 h 56 | 18 h 57 |
| Gems: a pair Lv. 5 | 20 h 00 | — | — | 20 h 57 |

# Sim run: time-model-3

30 players per group, 22 h each; archetypes efficient, manager, grinder; payers free; scenarios timed; seed 1. Full report: `Development/sim/results/time-model-3/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **efficient · free:** Sword Crafter 1 h 34, 27 waits over 15 min between buys
- **manager · free:** Sword Crafter 44 min, 26 waits over 15 min between buys
- **grinder · free:** Sword Crafter 1 h 10, 30 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | efficient | manager | grinder |
|---|---|---|---|---|
| Katana | 15 min | 15 min | 13 min | 17 min |
| Longsword | 40 min | 42 min | 25 min | 47 min |
| Sword Crafter | 1 h 30 | 1 h 34 | 44 min | 1 h 10 |
| 1st merge | 2 h 00 | 2 h 38 | 2 h 16 | 1 h 45 |
| Haru (2nd crafter) | 3 h 00 | 1 h 54 | 1 h 47 | 2 h 51 |
| Gems: all Lv. 1 | 3 h 00 | — | — | 21 h 18 |
| Stocker | 3 h 30 | 1 h 40 | 50 min | 1 h 23 |
| Falchion | 4 h 00 | 1 h 20 | 1 h 30 | 2 h 40 |
| 2nd merge | 4 h 00 | 3 h 09 | 2 h 53 | 2 h 58 |
| Mei (3rd crafter) | 6 h 00 | 3 h 31 | 3 h 11 | 3 h 07 |
| Gladius | 6 h 20 | 1 h 27 | 1 h 37 | 2 h 44 |
| Shop Promoter | 6 h 40 | 10 h 59 | 10 h 48 | 16 h 21 |
| 3rd merge | 7 h 00 | 3 h 39 | 3 h 19 | 3 h 12 |
| Cashier | 7 h 30 | 11 h 43 | 11 h 38 | 17 h 18 |
| Zanbatō | 4 h 00 | 4 h 15 | 3 h 05 | 3 h 23 |
| Sword Etcher | 8 h 30 | 13 h 01 | 13 h 06 | 17 h 15 |
| Gems: own pair Lv. 3 | 10 h 00 | 7 h 40 | 9 h 32 | 7 h 43 |
| Kenji (4th crafter) | 10 h 30 | 14 h 53 | 15 h 06 | 15 h 12 |
| Taru (5th crafter) | 12 h 30 | 19 h 22 | 20 h 04 | 20 h 05 |
| Seraph | 20 h 00 | 18 h 34 | 19 h 11 | 21 h 21 |
| Gems: a pair Lv. 5 | 20 h 00 | — | — | 21 h 02 |

# Sim run: time-model-8

30 players per group, 22 h each; archetypes efficient, manager, grinder; payers free; scenarios timed; seed 1. Full report: `Development/sim/results/time-model-8/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **efficient · free:** Sword Crafter 55 min, 25 waits over 15 min between buys
- **manager · free:** Sword Crafter 44 min, 25 waits over 15 min between buys
- **grinder · free:** Sword Crafter 1 h 29, 27 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | efficient | manager | grinder |
|---|---|---|---|---|
| Katana | 15 min | 14 min | 13 min | 17 min |
| Longsword | 40 min | 42 min | 25 min | 47 min |
| Sword Crafter | 1 h 30 | 55 min | 44 min | 1 h 29 |
| 1st merge | 2 h 00 | 2 h 59 | 2 h 51 | 2 h 49 |
| Haru (2nd crafter) | 3 h 00 | 1 h 12 | 58 min | 1 h 50 |
| Gems: all Lv. 1 | 3 h 00 | — | — | 20 h 18 |
| Stocker | 3 h 30 | 1 h 00 | 50 min | 1 h 40 |
| Falchion | 4 h 00 | 1 h 51 | 2 h 00 | 2 h 07 |
| 2nd merge | 4 h 00 | 4 h 10 | 3 h 51 | 3 h 08 |
| Mei (3rd crafter) | 6 h 00 | 2 h 03 | 2 h 31 | 2 h 03 |
| Gladius | 6 h 20 | 1 h 57 | 2 h 06 | 2 h 10 |
| Shop Promoter | 6 h 40 | 10 h 11 | 9 h 59 | 17 h 03 |
| 3rd merge | 7 h 00 | 4 h 29 | 4 h 21 | 3 h 39 |
| Cashier | 7 h 30 | 11 h 16 | 11 h 02 | 17 h 17 |
| Zanbatō | 4 h 00 | 2 h 37 | 2 h 27 | 2 h 30 |
| Sword Etcher | 8 h 30 | 17 h 49 | 18 h 54 | 18 h 25 |
| Gems: own pair Lv. 3 | 10 h 00 | 8 h 00 | 9 h 17 | 7 h 51 |
| Kenji (4th crafter) | 10 h 30 | — | — | 21 h 54 |
| Taru (5th crafter) | 12 h 30 | — | — | — |
| Seraph | 20 h 00 | 21 h 13 | — | — |
| Gems: a pair Lv. 5 | 20 h 00 | — | — | 20 h 03 |

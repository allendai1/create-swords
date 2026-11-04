# Sim run: time-model-9

30 players per group, 22 h each; archetypes efficient, manager, grinder; payers free; scenarios timed; seed 1. Full report: `Development/sim/results/time-model-9/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **efficient · free:** Sword Crafter 57 min, 29 waits over 15 min between buys
- **manager · free:** Sword Crafter 45 min, 28 waits over 15 min between buys
- **grinder · free:** Sword Crafter 1 h 11, 32 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | efficient | manager | grinder |
|---|---|---|---|---|
| Katana | 15 min | 14 min | 13 min | 17 min |
| Longsword | 40 min | 41 min | 24 min | 46 min |
| Sword Crafter | 1 h 30 | 57 min | 45 min | 1 h 11 |
| 1st merge | 2 h 00 | 4 h 00 | 4 h 31 | 3 h 28 |
| Haru (2nd crafter) | 3 h 00 | 1 h 29 | 1 h 12 | 2 h 38 |
| Gems: all Lv. 1 | 3 h 00 | — | — | 19 h 38 |
| Stocker | 3 h 30 | 1 h 05 | 53 min | 1 h 22 |
| Falchion | 4 h 00 | 3 h 32 | 3 h 54 | 4 h 06 |
| 2nd merge | 4 h 00 | 5 h 08 | 5 h 02 | 4 h 54 |
| Mei (3rd crafter) | 6 h 00 | 3 h 49 | 4 h 18 | 4 h 24 |
| Gladius | 6 h 20 | 3 h 38 | 3 h 59 | 4 h 12 |
| Shop Promoter | 6 h 40 | 11 h 52 | 11 h 51 | 17 h 50 |
| 3rd merge | 7 h 00 | 6 h 20 | 6 h 18 | 5 h 32 |
| Cashier | 7 h 30 | 12 h 48 | 12 h 45 | 18 h 53 |
| Zanbatō | 4 h 00 | 4 h 48 | 4 h 09 | 4 h 36 |
| Sword Etcher | 8 h 30 | 16 h 07 | 16 h 37 | 18 h 43 |
| Gems: own pair Lv. 3 | 10 h 00 | 8 h 00 | 9 h 32 | 7 h 30 |
| Kenji (4th crafter) | 10 h 30 | 19 h 11 | 19 h 44 | 19 h 49 |
| Taru (5th crafter) | 12 h 30 | 21 h 04 | 21 h 09 | — |
| Seraph | 20 h 00 | — | — | — |
| Gems: a pair Lv. 5 | 20 h 00 | — | — | 19 h 18 |

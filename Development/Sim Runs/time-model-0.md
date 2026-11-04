# Sim run: time-model-0

30 players per group, 22 h each; archetypes efficient, manager, grinder; payers free; scenarios timed; seed 1. Full report: `Development/sim/results/time-model-0/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **efficient · free:** Sword Crafter 1 h 54, 25 waits over 15 min between buys
- **manager · free:** Sword Crafter 1 h 31, 22 waits over 15 min between buys
- **grinder · free:** Sword Crafter 1 h 23, 26 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | efficient | manager | grinder |
|---|---|---|---|---|
| Katana | 15 min | 24 min | 26 min | 1 h 08 |
| Longsword | 40 min | 28 min | 28 min | 1 h 12 |
| Sword Crafter | 1 h 30 | 1 h 54 | 1 h 31 | 1 h 23 |
| 1st merge | 2 h 00 | 3 h 01 | 2 h 12 | 2 h 59 |
| Haru (2nd crafter) | 3 h 00 | 2 h 24 | 1 h 51 | 4 h 24 |
| Gems: all Lv. 1 | 3 h 00 | — | — | 20 h 05 |
| Stocker | 3 h 30 | 2 h 00 | 1 h 36 | 1 h 38 |
| Falchion | 4 h 00 | 1 h 26 | 1 h 11 | 3 h 06 |
| 2nd merge | 4 h 00 | 3 h 44 | 3 h 22 | 3 h 53 |
| Mei (3rd crafter) | 6 h 00 | 5 h 41 | 5 h 03 | 4 h 55 |
| Gladius | 6 h 20 | 1 h 50 | 1 h 30 | 3 h 18 |
| Shop Promoter | 6 h 40 | 12 h 53 | 12 h 24 | — |
| 3rd merge | 7 h 00 | 4 h 39 | 4 h 04 | 4 h 18 |
| Cashier | 7 h 30 | 13 h 25 | 12 h 59 | — |
| Zanbatō | 4 h 00 | 6 h 34 | 4 h 54 | 5 h 36 |
| Sword Etcher | 8 h 30 | — | — | — |
| Gems: own pair Lv. 3 | 10 h 00 | 7 h 56 | 9 h 30 | 7 h 46 |
| Kenji (4th crafter) | 10 h 30 | — | — | — |
| Taru (5th crafter) | 12 h 30 | — | — | — |
| Seraph | 20 h 00 | — | — | — |
| Gems: a pair Lv. 5 | 20 h 00 | — | — | 20 h 00 |

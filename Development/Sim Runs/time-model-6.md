# Sim run: time-model-6

30 players per group, 22 h each; archetypes efficient, manager, grinder; payers free; scenarios timed; seed 1. Full report: `Development/sim/results/time-model-6/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **efficient · free:** Sword Crafter 2 h 02, 25 waits over 15 min between buys
- **manager · free:** Sword Crafter 1 h 34, 23 waits over 15 min between buys
- **grinder · free:** Sword Crafter 1 h 08, 27 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | efficient | manager | grinder |
|---|---|---|---|---|
| Katana | 15 min | 17 min | 15 min | 18 min |
| Longsword | 40 min | 43 min | 25 min | 47 min |
| Sword Crafter | 1 h 30 | 2 h 02 | 1 h 34 | 1 h 08 |
| 1st merge | 2 h 00 | 3 h 47 | 3 h 13 | 3 h 36 |
| Haru (2nd crafter) | 3 h 00 | 2 h 36 | 1 h 47 | 3 h 47 |
| Gems: all Lv. 1 | 3 h 00 | — | — | 19 h 47 |
| Stocker | 3 h 30 | 2 h 13 | 1 h 38 | 1 h 16 |
| Falchion | 4 h 00 | 1 h 47 | 1 h 21 | 3 h 58 |
| 2nd merge | 4 h 00 | 4 h 16 | 3 h 33 | 4 h 24 |
| Mei (3rd crafter) | 6 h 00 | 4 h 36 | 4 h 00 | 4 h 35 |
| Gladius | 6 h 20 | 2 h 00 | 1 h 31 | 4 h 10 |
| Shop Promoter | 6 h 40 | 14 h 04 | 13 h 49 | — |
| 3rd merge | 7 h 00 | 4 h 55 | 4 h 09 | 4 h 50 |
| Cashier | 7 h 30 | 15 h 43 | 15 h 48 | — |
| Zanbatō | 4 h 00 | 5 h 18 | 3 h 51 | 5 h 07 |
| Sword Etcher | 8 h 30 | 21 h 29 | — | — |
| Gems: own pair Lv. 3 | 10 h 00 | 7 h 54 | 9 h 31 | 7 h 37 |
| Kenji (4th crafter) | 10 h 30 | — | — | — |
| Taru (5th crafter) | 12 h 30 | — | — | — |
| Seraph | 20 h 00 | — | — | — |
| Gems: a pair Lv. 5 | 20 h 00 | — | — | 19 h 31 |

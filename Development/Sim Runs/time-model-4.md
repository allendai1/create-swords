# Sim run: time-model-4

30 players per group, 22 h each; archetypes efficient, manager, grinder; payers free; scenarios timed; seed 1. Full report: `Development/sim/results/time-model-4/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **efficient · free:** Sword Crafter 1 h 03, 24 waits over 15 min between buys
- **manager · free:** Sword Crafter 49 min, 24 waits over 15 min between buys
- **grinder · free:** Sword Crafter 1 h 09, 27 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | efficient | manager | grinder |
|---|---|---|---|---|
| Katana | 15 min | 19 min | 16 min | 21 min |
| Longsword | 40 min | 48 min | 27 min | 52 min |
| Sword Crafter | 1 h 30 | 1 h 03 | 49 min | 1 h 09 |
| 1st merge | 2 h 00 | 2 h 54 | 2 h 59 | 2 h 28 |
| Haru (2nd crafter) | 3 h 00 | 1 h 30 | 1 h 11 | 1 h 33 |
| Gems: all Lv. 1 | 3 h 00 | — | — | 20 h 00 |
| Stocker | 3 h 30 | 1 h 14 | 57 min | 1 h 23 |
| Falchion | 4 h 00 | 4 h 11 | 4 h 21 | 3 h 27 |
| 2nd merge | 4 h 00 | 4 h 50 | 5 h 00 | 3 h 42 |
| Mei (3rd crafter) | 6 h 00 | 4 h 39 | 4 h 56 | 4 h 07 |
| Gladius | 6 h 20 | 4 h 19 | 4 h 26 | 3 h 33 |
| Shop Promoter | 6 h 40 | 12 h 53 | 12 h 51 | 20 h 35 |
| 3rd merge | 7 h 00 | 5 h 04 | 5 h 11 | 3 h 54 |
| Cashier | 7 h 30 | 14 h 15 | 14 h 19 | 20 h 51 |
| Zanbatō | 4 h 00 | 5 h 39 | 4 h 45 | 4 h 37 |
| Sword Etcher | 8 h 30 | 21 h 09 | — | 21 h 59 |
| Gems: own pair Lv. 3 | 10 h 00 | 7 h 43 | 9 h 18 | 7 h 32 |
| Kenji (4th crafter) | 10 h 30 | — | — | — |
| Taru (5th crafter) | 12 h 30 | — | — | — |
| Seraph | 20 h 00 | — | — | — |
| Gems: a pair Lv. 5 | 20 h 00 | — | — | 20 h 00 |

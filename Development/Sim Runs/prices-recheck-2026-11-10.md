# Sim run: prices-recheck-2026-11-10

60 players per group, 20 h each; archetypes casual, efficient, automator, rusher, grinder, manager; payers free, starter; scenarios baseline; seed 1. Full report: `Development/sim/results/prices-recheck-2026-11-10/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **casual · free:** Sword Crafter 28 min, 12 waits over 15 min between buys
- **casual · starter:** Sword Crafter 20 min, 12 waits over 15 min between buys
- **efficient · free:** Sword Crafter 15 min, 15 waits over 15 min between buys
- **efficient · starter:** Sword Crafter 11 min, 14 waits over 15 min between buys
- **automator · free:** Sword Crafter 34 min, 15 waits over 15 min between buys
- **automator · starter:** Sword Crafter 16 min, 14 waits over 15 min between buys
- **rusher · free:** Sword Crafter 32 min, 20 waits over 15 min between buys
- **rusher · starter:** Sword Crafter 27 min, 18 waits over 15 min between buys
- **grinder · free:** Sword Crafter 17 min, 16 waits over 15 min between buys
- **grinder · starter:** Sword Crafter 12 min, 13 waits over 15 min between buys
- **manager · free:** Sword Crafter 15 min, 15 waits over 15 min between buys
- **manager · starter:** Sword Crafter 13 min, 13 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | casual | efficient | automator | rusher | grinder | manager |
|---|---|---|---|---|---|---|---|
| Katana | 15 min | 16 min | 7 min | 49 min | 7 min | 11 min | 7 min |
| Sword Crafter | 15 min | 28 min | 15 min | 34 min | 32 min | 17 min | 15 min |
| Longsword | 40 min | 1 h 49 | 50 min | 3 h 25 | 26 min | 49 min | 54 min |
| 1st merge | 2 h 00 | 2 h 57 | 1 h 24 | 4 h 38 | 2 h 49 | 1 h 28 | 1 h 33 |
| Haru (2nd crafter) | 3 h 00 | 3 h 19 | 1 h 50 | 2 h 55 | 2 h 57 | 1 h 41 | 2 h 30 |
| Gems: all Lv. 1 | 3 h 00 | 5 h 00 | — | 2 h 14 | — | 11 h 00 | 9 h 06 |
| Stocker | 3 h 30 | 1 h 56 | 55 min | 1 h 45 | 1 h 51 | 53 min | 59 min |
| Falchion | 4 h 00 | 3 h 45 | 1 h 42 | 5 h 01 | 1 h 04 | 1 h 58 | 1 h 50 |
| 2nd merge | 4 h 00 | 3 h 55 | 2 h 26 | 5 h 08 | 3 h 48 | 2 h 07 | 2 h 38 |
| Mei (3rd crafter) | 6 h 00 | 6 h 31 | 2 h 56 | 4 h 34 | 6 h 25 | 4 h 11 | 2 h 50 |
| Gladius | 6 h 20 | 5 h 58 | 2 h 21 | 6 h 17 | 1 h 36 | 3 h 34 | 2 h 24 |
| Shop Promoter | 6 h 40 | 4 h 41 | 4 h 01 | 5 h 33 | 4 h 51 | 8 h 03 | 5 h 00 |
| 3rd merge | 7 h 00 | 5 h 06 | 2 h 42 | 5 h 53 | 5 h 23 | 2 h 57 | 3 h 21 |
| Cashier | 7 h 30 | 5 h 39 | 4 h 10 | 6 h 06 | 5 h 26 | 8 h 47 | 5 h 09 |
| Zanbatō | 4 h 00 | 6 h 50 | 3 h 41 | 6 h 46 | 4 h 06 | 4 h 32 | 3 h 14 |
| Sword Etcher | 8 h 30 | 9 h 00 | 5 h 16 | 7 h 20 | 7 h 27 | 9 h 01 | 6 h 40 |
| Gems: own pair Lv. 3 | 10 h 00 | 13 h 00 | 4 h 24 | 5 h 58 | 4 h 00 | 3 h 22 | 4 h 00 |
| Kenji (4th crafter) | 10 h 30 | 10 h 37 | 6 h 09 | 7 h 38 | 8 h 05 | 8 h 46 | 6 h 58 |
| Taru (5th crafter) | 12 h 30 | 17 h 08 | 9 h 08 | 9 h 21 | 10 h 30 | 10 h 18 | 9 h 35 |
| Seraph | 20 h 00 | 12 h 30 | 8 h 37 | 11 h 38 | 6 h 56 | 11 h 00 | 9 h 43 |
| Gems: a pair Lv. 5 | 20 h 00 | — | — | 17 h 39 | — | 10 h 00 | 9 h 00 |

**starter**

| Milestone | Target | casual | efficient | automator | rusher | grinder | manager |
|---|---|---|---|---|---|---|---|
| Katana | 15 min | 8 min | 6 min | 35 min | 6 min | 7 min | 8 min |
| Sword Crafter | 15 min | 20 min | 11 min | 16 min | 27 min | 12 min | 13 min |
| Longsword | 40 min | 1 h 37 | 44 min | 3 h 01 | 24 min | 45 min | 51 min |
| 1st merge | 2 h 00 | 2 h 40 | 1 h 16 | 4 h 00 | 2 h 38 | 1 h 24 | 1 h 30 |
| Haru (2nd crafter) | 3 h 00 | 3 h 01 | 1 h 41 | 2 h 35 | 2 h 44 | 1 h 37 | 2 h 25 |
| Gems: all Lv. 1 | 3 h 00 | 3 min | 14 h 37 | 2 min | 15 h 00 | 5 h 00 | 5 h 20 |
| Stocker | 3 h 30 | 1 h 44 | 48 min | 1 h 33 | 1 h 39 | 50 min | 55 min |
| Falchion | 4 h 00 | 3 h 21 | 1 h 34 | 4 h 19 | 57 min | 1 h 54 | 1 h 47 |
| 2nd merge | 4 h 00 | 3 h 27 | 2 h 13 | 4 h 25 | 3 h 32 | 2 h 02 | 2 h 32 |
| Mei (3rd crafter) | 6 h 00 | 6 h 01 | 2 h 39 | 3 h 56 | 5 h 52 | 3 h 56 | 2 h 45 |
| Gladius | 6 h 20 | 5 h 26 | 2 h 12 | 5 h 19 | 1 h 27 | 3 h 24 | 2 h 21 |
| Shop Promoter | 6 h 40 | 4 h 11 | 3 h 32 | 4 h 48 | 4 h 23 | 7 h 13 | 4 h 49 |
| 3rd merge | 7 h 00 | 4 h 36 | 2 h 26 | 5 h 03 | 4 h 56 | 2 h 48 | 3 h 15 |
| Cashier | 7 h 30 | 5 h 09 | 3 h 42 | 5 h 13 | 4 h 57 | 7 h 45 | 4 h 56 |
| Zanbatō | 4 h 00 | 6 h 18 | 3 h 17 | 5 h 50 | 3 h 47 | 4 h 18 | 3 h 07 |
| Sword Etcher | 8 h 30 | 8 h 15 | 4 h 43 | 6 h 23 | 6 h 53 | 7 h 55 | 6 h 12 |
| Gems: own pair Lv. 3 | 10 h 00 | 3 min | 2 min | 2 min | 3 min | 3 min | 3 min |
| Kenji (4th crafter) | 10 h 30 | 9 h 44 | 5 h 34 | 6 h 40 | 7 h 14 | 7 h 44 | 6 h 26 |
| Taru (5th crafter) | 12 h 30 | 11 h 20 | 7 h 58 | 7 h 53 | 9 h 00 | 9 h 01 | 8 h 08 |
| Seraph | 20 h 00 | 11 h 41 | 7 h 59 | 10 h 28 | 6 h 23 | 9 h 46 | 8 h 20 |
| Gems: a pair Lv. 5 | 20 h 00 | — | 13 h 40 | 13 h 00 | 6 h 59 | 5 h 00 | 5 h 12 |

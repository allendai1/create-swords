# Sim run: econ-review-2026-11-08

100 players per group, 20 h each; archetypes casual, efficient, automator, rusher, grinder, manager; payers free, starter, allpasses; scenarios baseline; seed 1. Full report: `Development/sim/results/econ-review-2026-11-08/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **casual · allpasses:** Sword Crafter 1 min, 15 waits over 15 min between buys
- **casual · free:** Sword Crafter 37 min, 31 waits over 15 min between buys
- **casual · starter:** Sword Crafter 1 min, 29 waits over 15 min between buys
- **efficient · allpasses:** Sword Crafter 1 min, 14 waits over 15 min between buys
- **efficient · free:** Sword Crafter 18 min, 18 waits over 15 min between buys
- **efficient · starter:** Sword Crafter 1 min, 16 waits over 15 min between buys
- **automator · allpasses:** Sword Crafter 1 min, 15 waits over 15 min between buys
- **automator · free:** Sword Crafter 36 min, 19 waits over 15 min between buys
- **automator · starter:** Sword Crafter 1 min, 18 waits over 15 min between buys
- **rusher · allpasses:** Sword Crafter 1 min, 17 waits over 15 min between buys
- **rusher · free:** Sword Crafter 37 min, 24 waits over 15 min between buys
- **rusher · starter:** Sword Crafter 1 min, 23 waits over 15 min between buys
- **grinder · allpasses:** Sword Crafter 1 min, 13 waits over 15 min between buys
- **grinder · free:** Sword Crafter 22 min, 20 waits over 15 min between buys
- **grinder · starter:** Sword Crafter 1 min, 18 waits over 15 min between buys
- **manager · allpasses:** Sword Crafter 1 min, 13 waits over 15 min between buys
- **manager · free:** Sword Crafter 16 min, 16 waits over 15 min between buys
- **manager · starter:** Sword Crafter 1 min, 13 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**allpasses**

| Milestone | Target | casual | efficient | automator | rusher | grinder | manager |
|---|---|---|---|---|---|---|---|
| Katana | 15 min | 20 min | 14 min | 32 min | 12 min | 15 min | 14 min |
| Sword Crafter | 15 min | 1 min | 1 min | 1 min | 1 min | 1 min | 1 min |
| Longsword | 40 min | 1 h 00 | 27 min | 1 h 51 | 23 min | 40 min | 28 min |
| 1st merge | 2 h 00 | 1 h 39 | 1 h 01 | 2 h 40 | 1 h 24 | 55 min | 1 h 03 |
| Haru (2nd crafter) | 3 h 00 | 1 h 56 | 1 h 00 | 1 h 31 | 1 h 27 | 1 h 00 | 1 h 00 |
| Gems: all Lv. 1 | 3 h 00 | 0 min | 4 h 51 | 0 min | 6 h 00 | 3 h 31 | 4 h 10 |
| Stocker | 3 h 30 | 1 h 00 | 36 min | 52 min | 1 h 00 | 42 min | 39 min |
| Falchion | 4 h 00 | 2 h 25 | 1 h 10 | 3 h 03 | 36 min | 1 h 04 | 1 h 11 |
| 2nd merge | 4 h 00 | 2 h 32 | 1 h 14 | 3 h 10 | 2 h 04 | 1 h 12 | 1 h 37 |
| Mei (3rd crafter) | 6 h 00 | 4 h 56 | 1 h 55 | 2 h 37 | 4 h 00 | 2 h 23 | 1 h 34 |
| Gladius | 6 h 20 | 4 h 12 | 1 h 38 | 4 h 08 | 49 min | 2 h 04 | 1 h 27 |
| Shop Promoter | 6 h 40 | 3 h 12 | 2 h 55 | 3 h 32 | 2 h 44 | 4 h 33 | 3 h 15 |
| 3rd merge | 7 h 00 | 3 h 40 | 1 h 41 | 3 h 51 | 3 h 15 | 1 h 41 | 1 h 59 |
| Cashier | 7 h 30 | 4 h 00 | 3 h 02 | 4 h 00 | 3 h 17 | 5 h 01 | 3 h 20 |
| Zanbatō | 4 h 00 | 5 h 23 | 2 h 26 | 4 h 48 | 2 h 14 | 2 h 37 | 1 h 54 |
| Sword Etcher | 8 h 30 | 8 h 14 | 3 h 49 | 5 h 36 | 4 h 45 | 5 h 10 | 4 h 02 |
| Gems: own pair Lv. 3 | 10 h 00 | 0 min | 0 min | 0 min | 0 min | 0 min | 0 min |
| Kenji (4th crafter) | 10 h 30 | 9 h 22 | 4 h 32 | 5 h 54 | 4 h 54 | 5 h 00 | 5 h 07 |
| Taru (5th crafter) | 12 h 30 | 10 h 28 | 5 h 36 | 6 h 45 | 5 h 46 | 5 h 54 | 5 h 54 |
| Seraph | 20 h 00 | 10 h 56 | 5 h 28 | 8 h 41 | 4 h 24 | 6 h 23 | 5 h 38 |
| Gems: a pair Lv. 5 | 20 h 00 | 13 h 32 | 4 h 02 | 9 h 00 | 4 h 42 | 3 h 22 | 4 h 00 |

**free**

| Milestone | Target | casual | efficient | automator | rusher | grinder | manager |
|---|---|---|---|---|---|---|---|
| Katana | 15 min | 23 min | 9 min | 53 min | 9 min | 14 min | 7 min |
| Sword Crafter | 15 min | 37 min | 18 min | 36 min | 37 min | 22 min | 16 min |
| Longsword | 40 min | 2 h 22 | 50 min | 4 h 00 | 34 min | 1 h 00 | 37 min |
| 1st merge | 2 h 00 | 4 h 00 | 2 h 41 | 5 h 40 | 3 h 01 | 1 h 30 | 2 h 12 |
| Haru (2nd crafter) | 3 h 00 | 4 h 28 | 2 h 23 | 3 h 40 | 3 h 09 | 1 h 45 | 1 h 54 |
| Gems: all Lv. 1 | 3 h 00 | 5 h 00 | 7 h 54 | 2 h 55 | 10 h 00 | 6 h 30 | 7 h 52 |
| Stocker | 3 h 30 | 2 h 34 | 1 h 00 | 1 h 51 | 1 h 59 | 1 h 04 | 1 h 00 |
| Falchion | 4 h 00 | 5 h 25 | 3 h 02 | 6 h 27 | 1 h 00 | 2 h 06 | 2 h 30 |
| 2nd merge | 4 h 00 | 5 h 41 | 3 h 08 | 6 h 37 | 4 h 03 | 2 h 22 | 3 h 04 |
| Mei (3rd crafter) | 6 h 00 | 10 h 27 | 4 h 08 | 5 h 32 | 7 h 57 | 4 h 18 | 2 h 59 |
| Gladius | 6 h 20 | 9 h 11 | 3 h 53 | 8 h 37 | 1 h 33 | 3 h 55 | 2 h 52 |
| Shop Promoter | 6 h 40 | 7 h 00 | 5 h 50 | 7 h 17 | 5 h 19 | 8 h 33 | 5 h 51 |
| 3rd merge | 7 h 00 | 7 h 50 | 3 h 59 | 7 h 50 | 6 h 19 | 3 h 15 | 3 h 45 |
| Cashier | 7 h 30 | 8 h 41 | 6 h 04 | 8 h 17 | 6 h 26 | 9 h 19 | 6 h 00 |
| Zanbatō | 4 h 00 | 11 h 01 | 4 h 59 | 9 h 48 | 4 h 26 | 4 h 44 | 3 h 35 |
| Sword Etcher | 8 h 30 | 16 h 16 | 7 h 31 | 11 h 07 | 9 h 21 | 9 h 33 | 7 h 37 |
| Gems: own pair Lv. 3 | 10 h 00 | 7 h 56 | 3 h 22 | 6 h 00 | 3 h 30 | 3 h 00 | 4 h 09 |
| Kenji (4th crafter) | 10 h 30 | 18 h 12 | 9 h 07 | 11 h 40 | 9 h 37 | 9 h 18 | 9 h 21 |
| Taru (5th crafter) | 12 h 30 | 19 h 56 | 11 h 00 | 13 h 03 | 11 h 12 | 11 h 00 | 10 h 26 |
| Seraph | 20 h 00 | — | 10 h 55 | 16 h 28 | 8 h 43 | 11 h 49 | 10 h 16 |
| Gems: a pair Lv. 5 | 20 h 00 | — | 7 h 15 | 14 h 11 | 9 h 00 | 6 h 21 | 7 h 44 |

**starter**

| Milestone | Target | casual | efficient | automator | rusher | grinder | manager |
|---|---|---|---|---|---|---|---|
| Katana | 15 min | 18 min | 18 min | 26 min | 11 min | 21 min | 21 min |
| Sword Crafter | 15 min | 1 min | 1 min | 1 min | 1 min | 1 min | 1 min |
| Longsword | 40 min | 1 h 40 | 43 min | 3 h 06 | 32 min | 1 h 00 | 43 min |
| 1st merge | 2 h 00 | 3 h 12 | 2 h 04 | 4 h 19 | 2 h 31 | 1 h 26 | 1 h 59 |
| Haru (2nd crafter) | 3 h 00 | 3 h 46 | 1 h 51 | 2 h 35 | 2 h 39 | 1 h 41 | 1 h 42 |
| Gems: all Lv. 1 | 3 h 00 | 0 min | 5 h 00 | 0 min | 5 h 00 | 3 h 18 | 4 h 20 |
| Stocker | 3 h 30 | 1 h 48 | 58 min | 1 h 09 | 1 h 36 | 1 h 00 | 1 h 00 |
| Falchion | 4 h 00 | 4 h 17 | 2 h 22 | 5 h 00 | 48 min | 2 h 01 | 2 h 12 |
| 2nd merge | 4 h 00 | 4 h 32 | 2 h 28 | 5 h 09 | 3 h 42 | 2 h 14 | 2 h 48 |
| Mei (3rd crafter) | 6 h 00 | 8 h 53 | 3 h 30 | 4 h 12 | 7 h 06 | 4 h 06 | 2 h 44 |
| Gladius | 6 h 20 | 7 h 52 | 3 h 05 | 7 h 04 | 1 h 12 | 3 h 46 | 2 h 35 |
| Shop Promoter | 6 h 40 | 5 h 47 | 5 h 00 | 5 h 48 | 4 h 36 | 8 h 00 | 5 h 27 |
| 3rd merge | 7 h 00 | 6 h 38 | 3 h 11 | 6 h 21 | 5 h 31 | 3 h 07 | 3 h 31 |
| Cashier | 7 h 30 | 7 h 27 | 5 h 15 | 6 h 49 | 5 h 37 | 8 h 43 | 5 h 34 |
| Zanbatō | 4 h 00 | 9 h 36 | 4 h 09 | 8 h 03 | 4 h 00 | 4 h 30 | 3 h 20 |
| Sword Etcher | 8 h 30 | 14 h 17 | 6 h 35 | 9 h 24 | 8 h 22 | 8 h 56 | 6 h 46 |
| Gems: own pair Lv. 3 | 10 h 00 | 0 min | 0 min | 0 min | 0 min | 0 min | 0 min |
| Kenji (4th crafter) | 10 h 30 | 16 h 10 | 8 h 06 | 9 h 49 | 8 h 37 | 8 h 42 | 8 h 16 |
| Taru (5th crafter) | 12 h 30 | 17 h 52 | 10 h 01 | 11 h 00 | 9 h 30 | 10 h 20 | 9 h 18 |
| Seraph | 20 h 00 | 18 h 44 | 9 h 50 | 14 h 22 | 7 h 50 | 11 h 04 | 9 h 05 |
| Gems: a pair Lv. 5 | 20 h 00 | 17 h 32 | 4 h 36 | 9 h 42 | 4 h 32 | 3 h 09 | 4 h 06 |

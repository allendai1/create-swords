# Sim run: crafter-15min-goal-2026-11-02

100 players per group, 8 h each; archetypes efficient, manager, grinder, casual; payers free; scenarios first1.5k-goal, first2k-goal, first3k-goal, first2k-no-sit-back, no-sit-back; seed 1. Full report: `Development/sim/results/crafter-15min-goal-2026-11-02/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **efficient · free:** Sword Crafter 17 min, 5 waits over 15 min between buys
- **manager · free:** Sword Crafter 16 min, 4 waits over 15 min between buys
- **grinder · free:** Sword Crafter 10 min, 5 waits over 15 min between buys
- **casual · free:** Sword Crafter 16 min, 9 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | efficient | manager | grinder | casual |
|---|---|---|---|---|---|
| Katana | 15 min | 9 min | 7 min | 14 min | 24 min |
| Longsword | 40 min | 45 min | 33 min | 59 min | 2 h 19 |
| Sword Crafter | 1 h 30 | 17 min | 16 min | 10 min | 16 min |
| 1st merge | 2 h 00 | 2 h 34 | 2 h 00 | 1 h 26 | 4 h 12 |
| Haru (2nd crafter) | 3 h 00 | 2 h 18 | 1 h 40 | 1 h 44 | 4 h 51 |
| Gems: all Lv. 1 | 3 h 00 | — | — | — | 6 h 00 |
| Stocker | 3 h 30 | 60 min | 54 min | 1 h 02 | 2 h 30 |
| Falchion | 4 h 00 | 2 h 54 | 2 h 12 | 2 h 00 | 5 h 52 |
| 2nd merge | 4 h 00 | 3 h 31 | 2 h 57 | 2 h 15 | 6 h 06 |
| Mei (3rd crafter) | 6 h 00 | 4 h 00 | 2 h 54 | 4 h 13 | — |
| Gladius | 6 h 20 | 3 h 27 | 2 h 43 | 3 h 40 | — |
| Shop Promoter | 6 h 40 | 5 h 51 | 5 h 56 | — | 7 h 29 |
| 3rd merge | 7 h 00 | 3 h 44 | 3 h 35 | 3 h 00 | — |
| Cashier | 7 h 30 | 6 h 06 | 6 h 03 | — | — |
| Zanbatō | 4 h 00 | 4 h 58 | 3 h 25 | 4 h 36 | — |
| Sword Etcher | 8 h 30 | 7 h 46 | 7 h 43 | — | — |
| Gems: own pair Lv. 3 | 10 h 00 | 7 h 33 | — | 7 h 17 | — |
| Kenji (4th crafter) | 10 h 30 | — | — | — | — |
| Taru (5th crafter) | 12 h 30 | — | — | — | — |
| Seraph | 20 h 00 | — | — | — | — |
| Gems: a pair Lv. 5 | 20 h 00 | — | — | — | — |

Compared with the baseline and the other options in [[Development/Sim Runs/crafter-15min-2026-11-02#A 15-minute Sword Crafter (options, 2026-11-02)]].

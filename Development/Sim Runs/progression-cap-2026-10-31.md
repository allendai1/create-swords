# Sim run: progression-cap-2026-10-31

150 players per group, 12 h each; archetypes efficient, manager, grinder, casual; payers free; scenarios baseline, cap1, cap2; seed 1. Full report: `Development/sim/results/progression-cap-2026-10-31/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **efficient · free:** Sword Crafter 2 h 14, 16 waits over 15 min between buys
- **manager · free:** Sword Crafter 1 h 51, 16 waits over 15 min between buys
- **grinder · free:** Sword Crafter 2 h 16, 15 waits over 15 min between buys
- **casual · free:** Sword Crafter 4 h 21, 18 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | efficient | manager | grinder | casual |
|---|---|---|---|---|---|
| Katana | 15 min | 9 min | 8 min | 13 min | 22 min |
| Longsword | 40 min | 42 min | 29 min | 1 h 02 | 1 h 59 |
| Sword Crafter | 1 h 30 | 2 h 14 | 1 h 51 | 2 h 16 | 4 h 21 |
| 1st merge | 2 h 00 | 1 h 19 | 1 h 08 | 1 h 15 | 2 h 38 |
| Haru (2nd crafter) | 3 h 00 | 2 h 27 | 2 h 06 | 2 h 29 | 4 h 47 |
| Gems: all Lv. 1 | 3 h 00 | — | — | — | 6 h 00 |
| Stocker | 3 h 30 | 2 h 23 | 2 h 01 | 2 h 43 | 5 h 17 |
| Falchion | 4 h 00 | 1 h 35 | 1 h 19 | 1 h 47 | 3 h 24 |
| 2nd merge | 4 h 00 | 1 h 39 | 2 h 15 | 1 h 53 | 3 h 36 |
| Mei (3rd crafter) | 6 h 00 | 2 h 49 | 2 h 28 | 4 h 30 | 10 h 44 |
| Gladius | 6 h 20 | 2 h 07 | 1 h 45 | 3 h 50 | 9 h 05 |
| Shop Promoter | 6 h 40 | 5 h 20 | 5 h 37 | 9 h 09 | 5 h 38 |
| 3rd merge | 7 h 00 | 2 h 41 | 3 h 07 | 3 h 04 | 6 h 54 |
| Cashier | 7 h 30 | 5 h 41 | 5 h 48 | 10 h 18 | 8 h 22 |
| Zanbatō | 4 h 00 | 4 h 14 | 2 h 52 | 4 h 50 | 11 h 46 |
| Sword Etcher | 8 h 30 | 7 h 46 | 8 h 02 | 10 h 41 | — |
| Gems: own pair Lv. 3 | 10 h 00 | 8 h 02 | 9 h 02 | 7 h 57 | — |
| Kenji (4th crafter) | 10 h 30 | 9 h 18 | 10 h 19 | 10 h 16 | — |
| Rin (5th crafter) | 12 h 30 | — | — | — | — |
| Seraph | 20 h 00 | 11 h 52 | — | — | — |
| Gems: a pair Lv. 5 | 20 h 00 | — | — | — | — |

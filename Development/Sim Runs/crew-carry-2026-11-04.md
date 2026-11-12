# Sim run: crew-carry-2026-11-04

100 players per group, 8 h each; archetypes efficient, manager, grinder, casual; payers free; scenarios baseline; seed 1. Full report: `Development/sim/results/crew-carry-2026-11-04/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **efficient · free:** Sword Crafter 17 min, 3 waits over 15 min between buys
- **manager · free:** Sword Crafter 15 min, 3 waits over 15 min between buys
- **grinder · free:** Sword Crafter 20 min, 4 waits over 15 min between buys
- **casual · free:** Sword Crafter 35 min, 8 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | efficient | manager | grinder | casual |
|---|---|---|---|---|---|
| Katana | 15 min | 9 min | 7 min | 13 min | 21 min |
| Sword Crafter | 15 min | 17 min | 15 min | 20 min | 35 min |
| Longsword | 40 min | 47 min | 37 min | 1 h 04 | 2 h 29 |
| 1st merge | 2 h 00 | 2 h 40 | 2 h 23 | 1 h 29 | 4 h 13 |
| Haru (2nd crafter) | 3 h 00 | 2 h 22 | 2 h 03 | 1 h 46 | 4 h 50 |
| Gems: all Lv. 1 | 3 h 00 | — | 7 h 44 | 6 h 14 | 4 h 51 |
| Stocker | 3 h 30 | 1 h 04 | 1 h 03 | 1 h 07 | 2 h 39 |
| Falchion | 4 h 00 | 2 h 59 | 2 h 38 | 2 h 04 | 5 h 44 |
| 2nd merge | 4 h 00 | 3 h 04 | 3 h 12 | 2 h 18 | 5 h 59 |
| Mei (3rd crafter) | 6 h 00 | 4 h 09 | 3 h 09 | 4 h 18 | — |
| Gladius | 6 h 20 | 3 h 47 | 3 h 04 | 3 h 46 | — |
| Shop Promoter | 6 h 40 | 5 h 42 | 6 h 02 | — | 7 h 18 |
| 3rd merge | 7 h 00 | 3 h 52 | 3 h 50 | 3 h 08 | — |
| Cashier | 7 h 30 | 5 h 57 | 6 h 10 | — | — |
| Zanbatō | 4 h 00 | 4 h 58 | 3 h 40 | 4 h 40 | — |
| Sword Etcher | 8 h 30 | 7 h 15 | 7 h 50 | — | — |
| Gems: own pair Lv. 3 | 10 h 00 | 3 h 22 | 3 h 47 | 2 h 55 | — |
| Kenji (4th crafter) | 10 h 30 | — | — | — | — |
| Taru (5th crafter) | 12 h 30 | — | — | — | — |
| Seraph | 20 h 00 | — | — | — | — |
| Gems: a pair Lv. 5 | 20 h 00 | 7 h 37 | 7 h 32 | 6 h 05 | — |

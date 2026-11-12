# Sim run: crew-tiers-2026-11-04

100 players per group, 8 h each; archetypes efficient, manager, grinder, casual; payers free; scenarios baseline; seed 1. Full report: `Development/sim/results/crew-tiers-2026-11-04/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **efficient · free:** Sword Crafter 17 min, 3 waits over 15 min between buys
- **manager · free:** Sword Crafter 15 min, 3 waits over 15 min between buys
- **grinder · free:** Sword Crafter 20 min, 3 waits over 15 min between buys
- **casual · free:** Sword Crafter 35 min, 8 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | efficient | manager | grinder | casual |
|---|---|---|---|---|---|
| Katana | 15 min | 9 min | 7 min | 13 min | 21 min |
| Sword Crafter | 15 min | 17 min | 15 min | 20 min | 35 min |
| Longsword | 40 min | 48 min | 36 min | 1 h 04 | 2 h 27 |
| 1st merge | 2 h 00 | 2 h 41 | 2 h 23 | 1 h 30 | 4 h 11 |
| Haru (2nd crafter) | 3 h 00 | 2 h 24 | 2 h 04 | 1 h 46 | 4 h 51 |
| Gems: all Lv. 1 | 3 h 00 | — | 7 h 27 | 6 h 11 | 4 h 52 |
| Stocker | 3 h 30 | 1 h 04 | 1 h 03 | 1 h 08 | 2 h 38 |
| Falchion | 4 h 00 | 3 h 00 | 2 h 39 | 2 h 05 | 5 h 45 |
| 2nd merge | 4 h 00 | 3 h 06 | 3 h 13 | 2 h 18 | 5 h 58 |
| Mei (3rd crafter) | 6 h 00 | 4 h 11 | 3 h 10 | 4 h 18 | — |
| Gladius | 6 h 20 | 3 h 51 | 3 h 04 | 3 h 47 | — |
| Shop Promoter | 6 h 40 | 5 h 42 | 6 h 03 | — | 7 h 19 |
| 3rd merge | 7 h 00 | 3 h 55 | 3 h 49 | 3 h 08 | — |
| Cashier | 7 h 30 | 5 h 58 | 6 h 09 | — | — |
| Zanbatō | 4 h 00 | 4 h 56 | 3 h 41 | 4 h 41 | — |
| Sword Etcher | 8 h 30 | 7 h 15 | 7 h 46 | — | — |
| Gems: own pair Lv. 3 | 10 h 00 | 3 h 25 | 3 h 45 | 2 h 56 | — |
| Kenji (4th crafter) | 10 h 30 | — | — | — | — |
| Taru (5th crafter) | 12 h 30 | — | — | — | — |
| Seraph | 20 h 00 | — | — | — | — |
| Gems: a pair Lv. 5 | 20 h 00 | 7 h 37 | 7 h 18 | 6 h 03 | — |

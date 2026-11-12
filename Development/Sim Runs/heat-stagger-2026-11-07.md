# Sim run: heat-stagger-2026-11-07

60 players per group, 6 h each; archetypes casual, efficient, automator, rusher, grinder, manager; payers free; scenarios baseline; seed 1. Full report: `Development/sim/results/heat-stagger-2026-11-07/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **casual · free:** Sword Crafter 37 min, 5 waits over 15 min between buys
- **efficient · free:** Sword Crafter 18 min, 3 waits over 15 min between buys
- **automator · free:** Sword Crafter 35 min, 7 waits over 15 min between buys
- **rusher · free:** Sword Crafter 36 min, 7 waits over 15 min between buys
- **grinder · free:** Sword Crafter 22 min, 1 waits over 15 min between buys
- **manager · free:** Sword Crafter 15 min, 1 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | casual | efficient | automator | rusher | grinder | manager |
|---|---|---|---|---|---|---|---|
| Katana | 15 min | 21 min | 9 min | 53 min | 9 min | 14 min | 7 min |
| Sword Crafter | 15 min | 37 min | 18 min | 35 min | 36 min | 22 min | 15 min |
| Longsword | 40 min | 2 h 27 | 48 min | 4 h 15 | 33 min | 1 h 06 | 34 min |
| 1st merge | 2 h 00 | 4 h 14 | 2 h 46 | 5 h 53 | 3 h 00 | 1 h 31 | 2 h 17 |
| Haru (2nd crafter) | 3 h 00 | 4 h 50 | 2 h 31 | 3 h 47 | 3 h 09 | 1 h 45 | 1 h 57 |
| Gems: all Lv. 1 | 3 h 00 | 4 h 45 | — | 3 h 00 | — | — | — |
| Stocker | 3 h 30 | 2 h 38 | 1 h 05 | 1 h 56 | 2 h 01 | 1 h 09 | 1 h 02 |
| Falchion | 4 h 00 | 5 h 50 | 3 h 05 | — | 1 h 01 | 2 h 04 | 2 h 34 |
| 2nd merge | 4 h 00 | — | 3 h 11 | — | 4 h 16 | 2 h 18 | 3 h 10 |
| Mei (3rd crafter) | 6 h 00 | — | 4 h 22 | 5 h 45 | — | 4 h 20 | 3 h 08 |
| Gladius | 6 h 20 | — | 3 h 58 | — | 1 h 36 | 3 h 45 | 3 h 00 |
| Shop Promoter | 6 h 40 | — | 5 h 58 | — | 5 h 28 | — | 5 h 59 |
| 3rd merge | 7 h 00 | — | 4 h 04 | — | — | 3 h 06 | 3 h 46 |
| Cashier | 7 h 30 | — | — | — | — | — | — |
| Zanbatō | 4 h 00 | — | 5 h 07 | — | 4 h 35 | 4 h 42 | 3 h 36 |
| Sword Etcher | 8 h 30 | — | — | — | — | — | — |
| Gems: own pair Lv. 3 | 10 h 00 | — | 3 h 34 | — | 3 h 53 | 3 h 00 | 4 h 00 |
| Kenji (4th crafter) | 10 h 30 | — | — | — | — | — | — |
| Taru (5th crafter) | 12 h 30 | — | — | — | — | — | — |
| Seraph | 20 h 00 | — | — | — | — | — | — |
| Gems: a pair Lv. 5 | 20 h 00 | — | — | — | — | — | — |

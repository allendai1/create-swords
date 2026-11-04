# Sim run: audit-fixes-2026-11-02

100 players per group, 8 h each; archetypes efficient, manager, grinder, casual; payers free; scenarios baseline; seed 1. Full report: `Development/sim/results/audit-fixes-2026-11-02/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **efficient · free:** Sword Crafter 18 min, 5 waits over 15 min between buys
- **manager · free:** Sword Crafter 16 min, 4 waits over 15 min between buys
- **grinder · free:** Sword Crafter 20 min, 5 waits over 15 min between buys
- **casual · free:** Sword Crafter 35 min, 9 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | efficient | manager | grinder | casual |
|---|---|---|---|---|---|
| Katana | 15 min | 9 min | 7 min | 13 min | 21 min |
| Sword Crafter | 15 min | 18 min | 16 min | 20 min | 35 min |
| Longsword | 40 min | 46 min | 34 min | 1 h 00 | 2 h 19 |
| 1st merge | 2 h 00 | 2 h 31 | 1 h 57 | 1 h 26 | 4 h 06 |
| Haru (2nd crafter) | 3 h 00 | 2 h 14 | 1 h 42 | 1 h 43 | 4 h 48 |
| Gems: all Lv. 1 | 3 h 00 | — | — | — | 6 h 00 |
| Stocker | 3 h 30 | 1 h 00 | 58 min | 1 h 05 | 2 h 29 |
| Falchion | 4 h 00 | 2 h 52 | 2 h 11 | 2 h 01 | 5 h 48 |
| 2nd merge | 4 h 00 | 2 h 58 | 2 h 54 | 2 h 15 | 6 h 01 |
| Mei (3rd crafter) | 6 h 00 | 4 h 01 | 2 h 51 | 4 h 14 | — |
| Gladius | 6 h 20 | 3 h 38 | 2 h 41 | 3 h 39 | — |
| Shop Promoter | 6 h 40 | 5 h 51 | 5 h 53 | — | 7 h 19 |
| 3rd merge | 7 h 00 | 3 h 42 | 3 h 34 | 2 h 59 | — |
| Cashier | 7 h 30 | 6 h 07 | 6 h 00 | — | — |
| Zanbatō | 4 h 00 | 4 h 59 | 3 h 23 | 4 h 36 | — |
| Sword Etcher | 8 h 30 | 7 h 47 | 7 h 43 | — | — |
| Gems: own pair Lv. 3 | 10 h 00 | 7 h 34 | — | 7 h 17 | — |
| Kenji (4th crafter) | 10 h 30 | — | — | — | — |
| Taru (5th crafter) | 12 h 30 | — | — | — | — |
| Seraph | 20 h 00 | — | — | — | — |
| Gems: a pair Lv. 5 | 20 h 00 | — | — | — | — |

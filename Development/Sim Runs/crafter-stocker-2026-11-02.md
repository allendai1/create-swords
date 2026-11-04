# Sim run: crafter-stocker-2026-11-02

200 players per group, 12 h each; archetypes efficient, casual; payers free; scenarios crafter15k-stocker12k, crafter15k-stocker12k-no-sit-back; seed 1. Full report: `Development/sim/results/crafter-stocker-2026-11-02/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **efficient · free:** Sword Crafter 1 h 12, 11 waits over 15 min between buys
- **casual · free:** Sword Crafter 2 h 13, 17 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | efficient | casual |
|---|---|---|---|
| Katana | 15 min | 9 min | 21 min |
| Longsword | 40 min | 43 min | 2 h 04 |
| Sword Crafter | 1 h 30 | 1 h 12 | 2 h 13 |
| 1st merge | 2 h 00 | 1 h 58 | 3 h 33 |
| Haru (2nd crafter) | 3 h 00 | 1 h 38 | 4 h 15 |
| Gems: all Lv. 1 | 3 h 00 | — | 6 h 00 |
| Stocker | 3 h 30 | 1 h 14 | 2 h 20 |
| Falchion | 4 h 00 | 2 h 26 | 5 h 18 |
| 2nd merge | 4 h 00 | 2 h 32 | 5 h 33 |
| Mei (3rd crafter) | 6 h 00 | 3 h 16 | 10 h 58 |
| Gladius | 6 h 20 | 3 h 07 | 9 h 34 |
| Shop Promoter | 6 h 40 | 5 h 32 | 6 h 58 |
| 3rd merge | 7 h 00 | 3 h 24 | 7 h 55 |
| Cashier | 7 h 30 | 5 h 49 | 8 h 59 |
| Zanbatō | 4 h 00 | 4 h 37 | 11 h 53 |
| Sword Etcher | 8 h 30 | 7 h 32 | — |
| Gems: own pair Lv. 3 | 10 h 00 | 7 h 43 | — |
| Kenji (4th crafter) | 10 h 30 | 9 h 18 | — |
| Taru (5th crafter) | 12 h 30 | 11 h 28 | — |
| Seraph | 20 h 00 | 11 h 16 | — |
| Gems: a pair Lv. 5 | 20 h 00 | — | — |

# Sim run: first-mythril-2026-11-10

200 players per group, 2 h each; archetypes casual, efficient; payers free; scenarios baseline, beginner-luck; seed 1. Full report: `Development/sim/results/first-mythril-2026-11-10/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **casual · free:** Sword Crafter 17 min, 0 waits over 15 min between buys
- **efficient · free:** Sword Crafter 13 min, 0 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | casual | efficient |
|---|---|---|---|
| Katana | 15 min | 14 min | 5 min |
| Sword Crafter | 15 min | 17 min | 13 min |
| Longsword | 40 min | 1 h 10 | 31 min |
| 1st merge | 2 h 00 | — | 1 h 17 |
| Haru (2nd crafter) | 3 h 00 | — | 1 h 36 |
| Gems: all Lv. 1 | 3 h 00 | 1 h 15 | — |
| Stocker | 3 h 30 | 1 h 51 | 52 min |
| Falchion | 4 h 00 | — | 1 h 27 |
| 2nd merge | 4 h 00 | — | 1 h 54 |
| Mei (3rd crafter) | 6 h 00 | — | — |
| Gladius | 6 h 20 | — | — |
| Shop Promoter | 6 h 40 | — | — |
| 3rd merge | 7 h 00 | — | — |
| Cashier | 7 h 30 | — | — |
| Zanbatō | 4 h 00 | — | — |
| Sword Etcher | 8 h 30 | — | — |
| Gems: own pair Lv. 3 | 10 h 00 | — | 1 h 08 |
| Kenji (4th crafter) | 10 h 30 | — | — |
| Taru (5th crafter) | 12 h 30 | — | — |
| Seraph | 20 h 00 | — | — |
| Gems: a pair Lv. 5 | 20 h 00 | — | — |

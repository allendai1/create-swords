# Sim run: leaderboard-5h-2026-11-12

20 players per group, 40 h each; archetypes casual, efficient, manager; payers free; scenarios baseline; seed 1. Full report: `Development/sim/results/leaderboard-5h-2026-11-12/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **casual · free:** Swordsmith 18 min, 17 waits over 15 min between buys
- **efficient · free:** Swordsmith 13 min, 11 waits over 15 min between buys
- **manager · free:** Swordsmith 14 min, 4 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | casual | efficient | manager |
|---|---|---|---|---|
| Katana | 15 min | 14 min | 6 min | 6 min |
| Swordsmith | 15 min | 18 min | 13 min | 14 min |
| Longsword | 40 min | 1 h 20 | 31 min | 26 min |
| 1st merge | 2 h 00 | 1 h 07 | 33 min | 38 min |
| Haru (2nd crafter) | 3 h 00 | 3 h 06 | 1 h 34 | 2 h 20 |
| Gems: all Lv. 1 | 3 h 00 | 5 h 00 | — | — |
| Stocker | 3 h 30 | 1 h 59 | 50 min | 56 min |
| Falchion | 4 h 00 | 2 h 58 | 1 h 27 | 1 h 35 |
| 2nd merge | 4 h 00 | 3 h 24 | 1 h 56 | 2 h 24 |
| Mei (3rd crafter) | 6 h 00 | 6 h 00 | 2 h 48 | 2 h 40 |
| Gladius | 6 h 20 | 6 h 10 | 2 h 39 | 2 h 12 |
| Shop Promoter | 6 h 40 | 4 h 18 | 4 h 19 | 5 h 22 |
| 3rd merge | 7 h 00 | 4 h 51 | 2 h 15 | 3 h 13 |
| Cashier | 7 h 30 | 5 h 18 | 4 h 28 | 5 h 29 |
| Zanbatō | 4 h 00 | 6 h 20 | 3 h 41 | 3 h 02 |
| Sword Etcher | 8 h 30 | 8 h 01 | 5 h 07 | 6 h 22 |
| Gems: own pair Lv. 3 | 10 h 00 | — | 4 h 00 | 4 h 00 |
| Kenji (4th crafter) | 10 h 30 | 9 h 17 | 6 h 09 | 7 h 32 |
| Taru (5th crafter) | 12 h 30 | 12 h 22 | 8 h 00 | 8 h 27 |
| Seraph | 20 h 00 | 10 h 56 | 7 h 18 | 8 h 20 |
| Gems: a pair Lv. 5 | 20 h 00 | — | — | — |

# Sim run: sword-chain-2026-11-10

40 players per group, 16 h each; archetypes casual, efficient, manager; payers free; scenarios baseline, swords-even, swords-value; seed 1. Full report: `Development/sim/results/sword-chain-2026-11-10/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **casual · free:** Sword Crafter 29 min, 8 waits over 15 min between buys
- **efficient · free:** Sword Crafter 15 min, 12 waits over 15 min between buys
- **manager · free:** Sword Crafter 14 min, 12 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | casual | efficient | manager |
|---|---|---|---|---|
| Katana | 15 min | 15 min | 7 min | 7 min |
| Sword Crafter | 15 min | 29 min | 15 min | 14 min |
| Longsword | 40 min | 1 h 48 | 50 min | 51 min |
| 1st merge | 2 h 00 | 2 h 58 | 1 h 24 | 1 h 32 |
| Haru (2nd crafter) | 3 h 00 | 3 h 19 | 1 h 52 | 2 h 29 |
| Gems: all Lv. 1 | 3 h 00 | 5 h 00 | — | 9 h 20 |
| Stocker | 3 h 30 | 1 h 57 | 54 min | 55 min |
| Falchion | 4 h 00 | 3 h 45 | 1 h 42 | 1 h 50 |
| 2nd merge | 4 h 00 | 3 h 55 | 2 h 27 | 2 h 36 |
| Mei (3rd crafter) | 6 h 00 | 6 h 29 | 2 h 56 | 2 h 51 |
| Gladius | 6 h 20 | 5 h 54 | 2 h 23 | 2 h 23 |
| Shop Promoter | 6 h 40 | 4 h 42 | 3 h 59 | 5 h 02 |
| 3rd merge | 7 h 00 | 5 h 06 | 2 h 41 | 3 h 21 |
| Cashier | 7 h 30 | 5 h 38 | 4 h 09 | 5 h 11 |
| Zanbatō | 4 h 00 | 6 h 47 | 3 h 41 | 3 h 11 |
| Sword Etcher | 8 h 30 | 8 h 59 | 5 h 12 | 6 h 43 |
| Gems: own pair Lv. 3 | 10 h 00 | 13 h 00 | 4 h 55 | 4 h 00 |
| Kenji (4th crafter) | 10 h 30 | 10 h 36 | 6 h 06 | 6 h 58 |
| Taru (5th crafter) | 12 h 30 | 13 h 21 | 9 h 10 | 9 h 40 |
| Seraph | 20 h 00 | 12 h 31 | 8 h 22 | 9 h 47 |
| Gems: a pair Lv. 5 | 20 h 00 | — | — | 9 h 08 |

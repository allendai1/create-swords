# Sim run: audit-fixes-2026-11-10

6 players per group, 16 h each; archetypes efficient, manager; payers free; scenarios baseline; seed 1. Full report: `Development/sim/results/audit-fixes-2026-11-10/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **efficient · free:** Sword Crafter 14 min, 9 waits over 15 min between buys
- **manager · free:** Sword Crafter 13 min, 5 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | efficient | manager |
|---|---|---|---|
| Katana | 15 min | 6 min | 6 min |
| Sword Crafter | 15 min | 14 min | 13 min |
| Longsword | 40 min | 48 min | 53 min |
| 1st merge | 2 h 00 | 1 h 25 | 1 h 34 |
| Haru (2nd crafter) | 3 h 00 | 1 h 48 | 2 h 30 |
| Gems: all Lv. 1 | 3 h 00 | — | 9 h 00 |
| Stocker | 3 h 30 | 52 min | 57 min |
| Falchion | 4 h 00 | 1 h 42 | 1 h 50 |
| 2nd merge | 4 h 00 | 2 h 26 | 2 h 32 |
| Mei (3rd crafter) | 6 h 00 | 2 h 55 | 2 h 55 |
| Gladius | 6 h 20 | 2 h 21 | 2 h 24 |
| Shop Promoter | 6 h 40 | 4 h 02 | 4 h 55 |
| 3rd merge | 7 h 00 | 2 h 39 | 3 h 18 |
| Cashier | 7 h 30 | 4 h 13 | 5 h 03 |
| Zanbatō | 4 h 00 | 3 h 42 | 3 h 14 |
| Sword Etcher | 8 h 30 | 5 h 13 | 6 h 36 |
| Gems: own pair Lv. 3 | 10 h 00 | 4 h 00 | 3 h 49 |
| Kenji (4th crafter) | 10 h 30 | 6 h 10 | 6 h 51 |
| Taru (5th crafter) | 12 h 30 | 9 h 00 | 9 h 20 |
| Seraph | 20 h 00 | 8 h 28 | 9 h 36 |
| Gems: a pair Lv. 5 | 20 h 00 | — | 8 h 59 |

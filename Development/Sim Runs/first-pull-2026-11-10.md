# Sim run: first-pull-2026-11-10

200 players per group, 2 h each; archetypes casual, efficient; payers free; scenarios baseline, first-rare, first-epic, first-legendary; seed 1. Full report: `Development/sim/results/first-pull-2026-11-10/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **casual · free:** Sword Crafter 18 min, 0 waits over 15 min between buys
- **efficient · free:** Sword Crafter 15 min, 0 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | casual | efficient |
|---|---|---|---|
| Katana | 15 min | 16 min | 7 min |
| Sword Crafter | 15 min | 18 min | 15 min |
| Longsword | 40 min | 1 h 15 | 32 min |
| 1st merge | 2 h 00 | — | 1 h 20 |
| Haru (2nd crafter) | 3 h 00 | — | 1 h 38 |
| Gems: all Lv. 1 | 3 h 00 | 1 h 15 | — |
| Stocker | 3 h 30 | 1 h 55 | 54 min |
| Falchion | 4 h 00 | — | 1 h 30 |
| 2nd merge | 4 h 00 | — | 1 h 56 |
| Mei (3rd crafter) | 6 h 00 | — | — |
| Gladius | 6 h 20 | — | — |
| Shop Promoter | 6 h 40 | — | — |
| 3rd merge | 7 h 00 | — | — |
| Cashier | 7 h 30 | — | — |
| Zanbatō | 4 h 00 | — | — |
| Sword Etcher | 8 h 30 | — | — |
| Gems: own pair Lv. 3 | 10 h 00 | — | 1 h 11 |
| Kenji (4th crafter) | 10 h 30 | — | — |
| Taru (5th crafter) | 12 h 30 | — | — |
| Seraph | 20 h 00 | — | — |
| Gems: a pair Lv. 5 | 20 h 00 | — | — |

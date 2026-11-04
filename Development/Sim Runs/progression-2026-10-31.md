# Sim run: progression-2026-10-31

150 players per group, 4 h each; archetypes casual, efficient, automator, rusher, grinder, manager; payers free; scenarios baseline; seed 1. Full report: `Development/sim/results/progression-2026-10-31/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **casual · free:** Sword Crafter —, 2 waits over 15 min between buys
- **efficient · free:** Sword Crafter 2 h 12, 1 waits over 15 min between buys
- **automator · free:** Sword Crafter 1 h 49, 3 waits over 15 min between buys
- **rusher · free:** Sword Crafter —, 4 waits over 15 min between buys
- **grinder · free:** Sword Crafter 2 h 18, 0 waits over 15 min between buys
- **manager · free:** Sword Crafter 1 h 52, 1 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | casual | efficient | automator | rusher | grinder | manager |
|---|---|---|---|---|---|---|---|
| Katana | 15 min | 22 min | 9 min | 33 min | 9 min | 13 min | 8 min |
| Longsword | 40 min | 1 h 59 | 41 min | 2 h 39 | 33 min | 1 h 03 | 29 min |
| Sword Crafter | 1 h 30 | — | 2 h 12 | 1 h 49 | — | 2 h 18 | 1 h 52 |
| 1st merge | 2 h 00 | 2 h 37 | 1 h 17 | — | 2 h 27 | 1 h 15 | 1 h 09 |
| Haru (2nd crafter) | 3 h 00 | — | 2 h 28 | 3 h 04 | — | 2 h 31 | 2 h 07 |
| Gems: all Lv. 1 | 3 h 00 | — | — | — | — | — | — |
| Stocker | 3 h 30 | — | 2 h 22 | 2 h 22 | — | 2 h 44 | 2 h 01 |
| Falchion | 4 h 00 | 3 h 23 | 1 h 33 | — | 54 min | 1 h 48 | 1 h 20 |
| 2nd merge | 4 h 00 | 3 h 35 | 1 h 37 | — | 3 h 29 | 1 h 54 | 2 h 16 |
| Mei (3rd crafter) | 6 h 00 | — | 2 h 47 | — | — | — | 2 h 28 |
| Gladius | 6 h 20 | — | 2 h 07 | — | 1 h 30 | 3 h 49 | 1 h 47 |
| Shop Promoter | 6 h 40 | — | — | — | — | — | — |
| 3rd merge | 7 h 00 | — | 2 h 43 | — | — | 3 h 03 | 3 h 07 |
| Cashier | 7 h 30 | — | — | — | — | — | — |
| Zanbatō | 4 h 00 | — | — | — | 3 h 44 | — | 2 h 53 |
| Sword Etcher | 8 h 30 | — | — | — | — | — | — |
| Gems: own pair Lv. 3 | 10 h 00 | — | — | — | — | — | — |
| Kenji (4th crafter) | 10 h 30 | — | — | — | — | — | — |
| Rin (5th crafter) | 12 h 30 | — | — | — | — | — | — |
| Seraph | 20 h 00 | — | — | — | — | — | — |
| Gems: a pair Lv. 5 | 20 h 00 | — | — | — | — | — | — |

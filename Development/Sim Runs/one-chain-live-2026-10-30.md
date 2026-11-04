# Sim run: one-chain-live-2026-10-30

150 players per group, 400 h each; archetypes casual, efficient, automator, rusher, grinder, manager; payers free; scenarios baseline; seed 1. Full report: `Development/sim/results/one-chain-live-2026-10-30/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **casual · free:** Sword Crafter 4 h 21, 46 waits over 15 min between buys
- **efficient · free:** Sword Crafter 2 h 11, 17 waits over 15 min between buys
- **automator · free:** Sword Crafter 1 h 45, 38 waits over 15 min between buys
- **rusher · free:** Sword Crafter 4 h 34, 13 waits over 15 min between buys
- **grinder · free:** Sword Crafter 2 h 18, 21 waits over 15 min between buys
- **manager · free:** Sword Crafter 1 h 49, 18 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | casual | efficient | automator | rusher | grinder | manager |
|---|---|---|---|---|---|---|---|
| Katana | 15 min | 23 min | 9 min | 27 min | 9 min | 13 min | 8 min |
| Longsword | 40 min | 1 h 58 | 40 min | 1 h 59 | 33 min | 1 h 03 | 29 min |
| Sword Crafter | 1 h 30 | 4 h 21 | 2 h 11 | 1 h 45 | 4 h 34 | 2 h 18 | 1 h 49 |
| 1st merge | 2 h 00 | 2 h 38 | 1 h 16 | 4 h 24 | 2 h 27 | 1 h 15 | 1 h 08 |
| Haru (2nd crafter) | 3 h 00 | 4 h 40 | 2 h 28 | 2 h 58 | 4 h 37 | 2 h 27 | 2 h 06 |
| Gems: all Lv. 1 | 3 h 00 | 6 h 00 | — | 3 h 00 | — | — | — |
| Stocker | 3 h 30 | 4 h 51 | 2 h 18 | 2 h 17 | 4 h 39 | 2 h 33 | 1 h 57 |
| Falchion | 4 h 00 | 3 h 24 | 1 h 31 | 5 h 21 | 52 min | 1 h 48 | 1 h 18 |
| 2nd merge | 4 h 00 | 3 h 36 | 1 h 36 | 5 h 34 | 3 h 26 | 1 h 54 | 2 h 18 |
| Mei (3rd crafter) | 6 h 00 | 10 h 39 | 2 h 43 | 4 h 27 | 8 h 24 | 4 h 28 | 2 h 22 |
| Gladius | 6 h 20 | 8 h 57 | 2 h 06 | 8 h 25 | 1 h 28 | 3 h 46 | 1 h 44 |
| Shop Promoter | 6 h 40 | 5 h 32 | 5 h 20 | 6 h 23 | 4 h 47 | 9 h 12 | 5 h 36 |
| 3rd merge | 7 h 00 | 6 h 47 | 2 h 44 | 7 h 11 | 6 h 00 | 3 h 00 | 3 h 06 |
| Cashier | 7 h 30 | 8 h 18 | 5 h 39 | 7 h 56 | 6 h 09 | 10 h 24 | 5 h 48 |
| Zanbatō | 4 h 00 | 11 h 40 | 4 h 11 | 10 h 14 | 3 h 42 | 4 h 48 | 2 h 53 |
| Sword Etcher | 8 h 30 | 18 h 29 | 7 h 39 | 12 h 07 | 10 h 19 | 10 h 47 | 8 h 05 |
| Gems: own pair Lv. 3 | 10 h 00 | — | 7 h 38 | 16 h 37 | 8 h 00 | 7 h 17 | 8 h 43 |
| Kenji (4th crafter) | 10 h 30 | 21 h 57 | 9 h 14 | 12 h 56 | — | 10 h 22 | 10 h 23 |
| Rin (5th crafter) | 12 h 30 | 24 h 45 | — | 15 h 20 | — | 12 h 52 | — |
| Seraph | 20 h 00 | 26 h 23 | 11 h 50 | 22 h 10 | 9 h 35 | 14 h 13 | 12 h 17 |
| Gems: a pair Lv. 5 | 20 h 00 | — | — | — | — | — | — |

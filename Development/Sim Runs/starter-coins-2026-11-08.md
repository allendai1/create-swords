# Sim run: starter-coins-2026-11-08

100 players per group, 12 h each; archetypes casual, efficient; payers starter; scenarios starter0k, starter5k, starter10k, starter25k; seed 1. Full report: `Development/sim/results/starter-coins-2026-11-08/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **casual · starter:** Sword Crafter 33 min, 13 waits over 15 min between buys
- **efficient · starter:** Sword Crafter 17 min, 7 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**starter**

| Milestone | Target | casual | efficient |
|---|---|---|---|
| Katana | 15 min | 20 min | 9 min |
| Sword Crafter | 15 min | 33 min | 17 min |
| Longsword | 40 min | 1 h 58 | 45 min |
| 1st merge | 2 h 00 | 3 h 30 | 2 h 01 |
| Haru (2nd crafter) | 3 h 00 | 4 h 00 | 1 h 46 |
| Gems: all Lv. 1 | 3 h 00 | 0 min | 5 h 06 |
| Stocker | 3 h 30 | 2 h 08 | 58 min |
| Falchion | 4 h 00 | 4 h 37 | 2 h 20 |
| 2nd merge | 4 h 00 | 4 h 50 | 2 h 26 |
| Mei (3rd crafter) | 6 h 00 | 9 h 11 | 3 h 30 |
| Gladius | 6 h 20 | 8 h 02 | 3 h 01 |
| Shop Promoter | 6 h 40 | 6 h 06 | 5 h 03 |
| 3rd merge | 7 h 00 | 6 h 52 | 3 h 07 |
| Cashier | 7 h 30 | 7 h 43 | 5 h 15 |
| Zanbatō | 4 h 00 | 9 h 51 | 4 h 11 |
| Sword Etcher | 8 h 30 | — | 6 h 36 |
| Gems: own pair Lv. 3 | 10 h 00 | 0 min | 0 min |
| Kenji (4th crafter) | 10 h 30 | — | 8 h 05 |
| Taru (5th crafter) | 12 h 30 | — | 10 h 01 |
| Seraph | 20 h 00 | — | 9 h 50 |
| Gems: a pair Lv. 5 | 20 h 00 | — | 4 h 52 |

**How these scenarios were run (2026-11-08):** `starter0k` … `starter25k` set `store.starterCoins` in a scratch runner that adds them to `scenarios.SCENARIOS` and calls `run.main()`; `scenarios.py` is unchanged. Compare with the free players of [[Development/Sim Runs/econ-review-2026-11-08]] (same seed 1, 100 players, same flags but 20 h). Used in [[Design/Economy and Progression Review — 2026-11-08#3. The Starter Pack's 25,000 coins buy the first half hour in one tap; its gems are what speed the game]].

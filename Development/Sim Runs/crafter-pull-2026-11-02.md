# Sim run: crafter-pull-2026-11-02

100 players per group, 8 h each; archetypes efficient, manager, grinder, casual; payers free; scenarios baseline, crafter-goal, crafter-hold; seed 1. Full report: `Development/sim/results/crafter-pull-2026-11-02/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **efficient · free:** Sword Crafter 18 min, 6 waits over 15 min between buys
- **manager · free:** Sword Crafter 16 min, 4 waits over 15 min between buys
- **grinder · free:** Sword Crafter 20 min, 5 waits over 15 min between buys
- **casual · free:** Sword Crafter 35 min, 9 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | efficient | manager | grinder | casual |
|---|---|---|---|---|---|
| Katana | 15 min | 9 min | 7 min | 13 min | 20 min |
| Sword Crafter | 15 min | 18 min | 16 min | 20 min | 35 min |
| Longsword | 40 min | 46 min | 34 min | 59 min | 2 h 09 |
| 1st merge | 2 h 00 | 2 h 32 | 2 h 01 | 1 h 26 | 4 h 05 |
| Haru (2nd crafter) | 3 h 00 | 2 h 17 | 1 h 41 | 1 h 42 | 4 h 43 |
| Gems: all Lv. 1 | 3 h 00 | — | — | — | 6 h 00 |
| Stocker | 3 h 30 | 1 h 01 | 55 min | 1 h 01 | 2 h 20 |
| Falchion | 4 h 00 | 2 h 54 | 2 h 14 | 2 h 00 | 5 h 45 |
| 2nd merge | 4 h 00 | 3 h 29 | 3 h 00 | 2 h 14 | 6 h 00 |
| Mei (3rd crafter) | 6 h 00 | 3 h 59 | 2 h 54 | 4 h 13 | — |
| Gladius | 6 h 20 | 3 h 24 | 2 h 45 | 3 h 38 | — |
| Shop Promoter | 6 h 40 | 5 h 51 | 5 h 57 | — | 7 h 24 |
| 3rd merge | 7 h 00 | 3 h 43 | 3 h 37 | 2 h 58 | — |
| Cashier | 7 h 30 | 6 h 07 | 6 h 06 | — | — |
| Zanbatō | 4 h 00 | 4 h 56 | 3 h 27 | 4 h 36 | — |
| Sword Etcher | 8 h 30 | 7 h 44 | 7 h 46 | — | — |
| Gems: own pair Lv. 3 | 10 h 00 | 7 h 29 | — | 7 h 17 | — |
| Kenji (4th crafter) | 10 h 30 | — | — | — | — |
| Taru (5th crafter) | 12 h 30 | — | — | — | — |
| Seraph | 20 h 00 | — | — | — | — |
| Gems: a pair Lv. 5 | 20 h 00 | — | — | — | — |

## What it says (2026-11-02)

On the live export (Sword Crafter 2,000 with Anvil 2, after the Ingot Rack and Sword Rack). Casual players hire at 34 min today. If they head for him once his pad stands (`crafter-goal`), they hire at 17 min with a 4½-minute save. If no new chain opens while his pad stands (`crafter-hold`), they hire at 27 min, still buying begun chains' next levels first. Engaged players hire at 11–20 min in all three. Options: [[Design/Crafter Pull Options — 2026-11-02]].

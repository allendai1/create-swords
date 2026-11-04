# Sim run: early-rarity-2026-10-31

150 players per group, 2 h each; archetypes casual, efficient, automator, rusher, grinder, manager; payers free; scenarios baseline, rare-odds+50; seed 1. Full report: `Development/sim/results/early-rarity-2026-10-31/report.html` (not in git). Hand-action times: measured in playtests for pull_hold, collect, furnace_put, furnace_take, forge, polish, etch, place, rack, buy, detour, the rest estimates ([[Development/Gameplay Simulator Plan]]).

Main point, median (`pacing.py` for more):
- **casual · free:** Sword Crafter —, 0 waits over 15 min between buys
- **efficient · free:** Sword Crafter —, 0 waits over 15 min between buys
- **automator · free:** Sword Crafter —, 0 waits over 15 min between buys
- **rusher · free:** Sword Crafter —, 1 waits over 15 min between buys
- **grinder · free:** Sword Crafter —, 0 waits over 15 min between buys
- **manager · free:** Sword Crafter 1 h 46, 0 waits over 15 min between buys

Median time to each target, by payer (10th–90th percentile in the full report):

**free**

| Milestone | Target | casual | efficient | automator | rusher | grinder | manager |
|---|---|---|---|---|---|---|---|
| Katana | 15 min | 22 min | 8 min | 23 min | 8 min | 13 min | 7 min |
| Longsword | 40 min | 1 h 58 | 32 min | 1 h 19 | 23 min | 1 h 03 | 21 min |
| Sword Crafter | 1 h 30 | — | — | — | — | — | 1 h 46 |
| 1st merge | 2 h 00 | — | 1 h 13 | 1 h 43 | — | 1 h 13 | 1 h 04 |
| Haru (2nd crafter) | 3 h 00 | — | — | — | — | — | — |
| Gems: all Lv. 1 | 3 h 00 | — | — | — | — | — | — |
| Stocker | 3 h 30 | — | — | — | — | — | 1 h 52 |
| Falchion | 4 h 00 | — | 1 h 28 | — | 48 min | 1 h 47 | 1 h 14 |
| 2nd merge | 4 h 00 | — | 1 h 33 | — | — | 1 h 53 | 1 h 38 |
| Mei (3rd crafter) | 6 h 00 | — | — | — | — | — | — |
| Gladius | 6 h 20 | — | 1 h 57 | — | 1 h 17 | — | 1 h 33 |
| Shop Promoter | 6 h 40 | — | — | — | — | — | — |
| 3rd merge | 7 h 00 | — | — | — | — | — | — |
| Cashier | 7 h 30 | — | — | — | — | — | — |
| Zanbatō | 4 h 00 | — | — | — | — | — | — |
| Sword Etcher | 8 h 30 | — | — | — | — | — | — |
| Gems: own pair Lv. 3 | 10 h 00 | — | — | — | — | — | — |
| Kenji (4th crafter) | 10 h 30 | — | — | — | — | — | — |
| Rin (5th crafter) | 12 h 30 | — | — | — | — | — | — |
| Seraph | 20 h 00 | — | — | — | — | — | — |
| Gems: a pair Lv. 5 | 20 h 00 | — | — | — | — | — | — |

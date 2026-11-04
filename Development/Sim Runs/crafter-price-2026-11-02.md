# Sim run: crafter-price-2026-11-02

Three runs, 200 players per group, 12 h each; archetypes efficient, casual; payers free; seed 1. Full reports: `Development/sim/results/crafter-price-2026-11-02/`, `crafter-sitback-2026-11-02/`, `crafter-stocker-2026-11-02/` (`report.html`, not in git). Scenarios in `Development/sim/scenarios.py` (`crafterNk`, `overhaul-crafterNk`, `crafterNk-no-sit-back`, `crafter15k-stocker12k[-no-sit-back]`). For [[Design/Earlier First Crafter — 2026-11-02]].

Main point, median Sword Crafter (efficient / casual) and waits over 15 min between buys:

| Scenario | Sword Crafter | Waits > 15 min | Coins 12 h (eff / cas) |
|---|---|---|---|
| baseline | 2:13 / 4:44 | 12 / 17 | 15.9 M / 1.92 M |
| crafter25k | 1:14 / 3:02 | 12 / 18 | 14.4 M / 1.68 M |
| crafter20k | 1:13 / 3:00 | 12 / 18 | 14.4 M / 1.69 M |
| crafter15k | 1:12 / 2:13 | 12 / 18 | 14.4 M / 1.59 M |
| crafter10k | 0:46 / 2:04 | 12 / 19 | 13.9 M / 1.58 M |
| overhaul | 1:59 / 4:45 | 12 / 16 | 16.1 M / 1.93 M |
| overhaul-crafter15k | 1:12 / 1:56 | 12 / 18 | 14.9 M / 1.59 M |
| crafter15k-stocker12k | 1:12 / 2:13 | 11 / 17 | 14.2 M / 1.81 M |
| no-sit-back | 2:13 / 4:44 | — | 16.1 M / 2.65 M |
| crafter15k-no-sit-back | 1:12 / 2:13 | — | 15.9 M / 2.64 M |
| crafter15k-stocker12k-no-sit-back | 1:12 / 2:13 | 11 / 12 | 15.5 M / 2.78 M |

Casual crew swords / hours the crafter waited on a full rack: no-sit-back 356 / 2.1 h, crafter15k-no-sit-back 365 / 6.1 h, crafter15k-stocker12k-no-sit-back 500 / 1.9 h. Stocker (casual): 5:34 → 2:19 with the 12k Stocker.

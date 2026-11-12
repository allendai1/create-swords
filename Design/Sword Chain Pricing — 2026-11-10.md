---
title: Sword Chain Pricing — 2026-11-10
status: built 2026-11-10 — the Even set is in Shared.Upgrades (Allen: "Yes, build Even"); not played
type: design
updated: 2026-11-10
tags: [design, economy, pacing, swords, sim, create-swords]
---

# Sword Chain Pricing — 2026-11-10

Allen asked whether the upgrade order makes sense and whether players get better in a way they feel, then: "Yes, sword chain" (work up the sword-chain price fix with numbers).

## What the hand review said, and what the sim corrected

- **By the price list**, the Longsword to Gladius stretch looks uneven: Scimitar → Longsword ×3.7 for +19% value, then pairs at almost one price (Cutlass 33,800 / Falchion 36,400, Jian 65,000 / Gladius 78,000).
- **By waiting time it isn't a cliff.** In the sim each of those swords is a 4–10 min save at the moment it's bought, inside the LihFolk band. Gladius → Khopesh isn't a cliff either: the Big Sword Stand and the Zanbatō sit between them.
- **"Every sword at least +20%" can't be done by price.** 20 swords span 20 → 980 base value (×49). The first three take ×5.5 of it, which leaves +13.7% a step for the other 17. Bigger steps need a higher Seraph value (and every late price with it) or fewer swords.
- **What is real: new swords arrive in clumps.** A casual player gets the Cutlass and Falchion 7 min apart, then nothing for 1 h 48, then the Jian and Gladius 22 min apart.

## Two price sets tried

Both keep the coins up to the Zanbatō (387,300 with its stand). Nothing else changes.

| | Longsword | Cutlass | Falchion | Jian | Gladius | Zanbatō |
|---|---|---|---|---|---|---|
| Today | 13,300 | 33,800 | 36,400 | 65,000 | 78,000 | 114,000 |
| **Even** (×2 a step) | 7,200 | 14,400 | 29,000 | 58,000 | 115,000 | 114,000 |
| **Value** (priced by what each adds; the saving on the Zanbatō) | 5,400 | 9,000 | 16,000 | 24,000 | 38,000 | 248,000 |

## Sim result

[[Development/Sim Runs/sword-chain-2026-11-10]]: 360 players (40 a group), free, 16 h, seed 1, medians. Scenarios `swords-even` and `swords-value` in `Development/sim/scenarios.py`. The export is 2026-11-10 00:45; the sim's players buy Musashi designs in all three sets.

| | Longsword | Cutlass | Falchion | Jian | Gladius | Zanbatō | Seraph | Waits over 15 min |
|---|---|---|---|---|---|---|---|---|
| casual, today | 1:49 | 3:38 | 3:45 | 5:33 | 5:55 | 6:47 | 12:32 | 8 |
| casual, Even | 1:10 | 1:48 | 3:10 | 4:47 | 6:34 | 6:42 | 12:26 | 8 |
| casual, Value | 1:01 | 1:25 | 1:57 | 2:37 | 3:20 | 7:35 | 12:05 | 9 |
| efficient, today | 0:49 | 1:37 | 1:42 | 2:15 | 2:23 | 3:41 | 8:22 | 12 |
| efficient, Even | 0:33 | 0:51 | 1:31 | 1:56 | 2:42 | 3:39 | 8:27 | 12 |
| efficient, Value | 0:30 | 0:40 | 0:51 | 1:01 | 1:29 | 3:48 | 8:10 | 12 |
| manager, today | 0:51 | 1:44 | 1:50 | 2:15 | 2:24 | 3:11 | 9:47 | 12 |
| manager, Even | 0:30 | 0:52 | 1:39 | 1:55 | 2:58 | 3:14 | 9:38 | 12 |
| manager, Value | 0:29 | 0:39 | 0:51 | 1:02 | 1:36 | 4:44 | 9:19 | 12 |

- **Even** spreads the swords out and moves nothing else: the Zanbatō and the Seraph stay within 1–2%, the waits over 15 min don't change. The Longsword comes back near its 40 min target for engaged players (0:30–0:33, today 0:49–0:51). One thing to see in Play: the Gladius (115,000) and the Zanbatō (114,000) land close together.
- **Value** uses the five swords up early. A casual player has all five by 3:20, then no new sword until the Khopesh at 6:37, and the Zanbatō comes 48 min later (a manager's 1 h 33 later). It front-loads content, the same result as the 2026-10-30 "cheaper blueprints shorten the game" runs.

## Recommendation

**Even**, as a tidy-up: five prices in `Shared.Upgrades`. It makes the list read as a steady ×2 and spaces the new swords; it does not make any sword a bigger step. **Value** is not recommended.

What would make swords a bigger step is a design call, not a price: a higher late value curve with late prices to match, or something else a new sword gives (the Legendary Commissions proposal in [[Design/Major Updates Plan — 2026-11-07]] asks for specific swords, which does this).

Related: [[Design/Tycoon Upgrades]] · [[Design/Economy and Progression Review — 2026-11-08]] · [[Design/Upgrade Time Model — 2026-11-02]]

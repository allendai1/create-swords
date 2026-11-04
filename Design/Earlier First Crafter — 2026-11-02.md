---
title: Earlier First Crafter — 2026-11-02
status: answered — Allen picked 20,000 for the Sword Crafter (2026-11-02, built); the Stocker at 12,000 built the same day (Allen: "Yes, both")
type: design
updated: 2026-11-02
tags: [proposal, crew, pacing, sim, create-swords]
---

# Earlier First Crafter — 2026-11-02

Allen picked "Earlier first crafter" from the core loop review (the first hire comes 2–5 h in; sessions are 10–30 min). The target is already **Sword Crafter 1 h 30** (Allen, 2026-10-29), and the first hire should "feel like a milestone" (2026-10-30). Today the sim misses it: **efficient 2 h 13, casual 4 h 44**.

## Why he comes late

Not the gate. Anvil 2 is bought at 25 min (efficient) / 43 min (casual). Then **Taise's 40,000** sits about 4× above every pad near him (Longsword 10,200, Furnace 2 2,800, Strikes IV 10,000), so a cheapest-first player buys ~50 other pads first (the Falchion and Gladius too) and Taise comes last. Read from one median player of each type in [[Development/Sim Runs/crafter-price-2026-11-02]].

## A second problem the runs found

**Taise makes swords nobody moves.** His swords wait on the full Finished Sword Rack for **2–6 h of a 12 h game** (`crew_wait.rackFull`), because the Stocker (36,000) comes 1–3 h after him. So hiring him earlier on its own adds almost nothing: casual crew swords 356 → 365, coins the same.

## Proposal

1. **Sword Crafter 40,000 → 15,000.**
2. **Stocker 36,000 → 12,000** (his gate stays: after the Sword Crafter). Taise and Sora come together as "the workshop runs itself".

Nothing else changes (gates, other prices). Fits the pending [[Design/Upgrade Tree Review — 2026-11-01#Overhaul proposal — 2026-11-02|overhaul]], which leaves Taise as he is (tested together below).

## Simulated

200 players per group, 12 h, efficient and casual, free, seed 1 (same flags as [[Development/Sim Runs/showcase-2026-11-02]]). Medians. "Forging on" = the sim's sit-back estimate off (players keep making their own swords once the crew works).

| Option | Taise eff / cas | Sora (Stocker) eff / cas | Gladius cas | Zanbatō cas | Coins 12 h cas | Waits > 15 min cas |
|---|---|---|---|---|---|---|
| Today, forging on | 2:13 / 4:44 | 2:22 / 5:34 | 8:15 | 9:56 | 2.65 M | — |
| Taise 15k, forging on | 1:12 / 2:13 | 1:56 / 5:24 | 8:13 | 9:56 | 2.64 M | — |
| **Taise 15k + Sora 12k, forging on** | **1:12 / 2:13** | **1:15 / 2:19** | **7:57** | **9:37** | **2.78 M** | **12** |
| Today (sit-back on) | 2:13 / 4:44 | 2:22 / 5:37 | 9:09 | 11:39 | 1.92 M | 17 |
| Taise 15k + Sora 12k (sit-back on) | 1:12 / 2:13 | 1:14 / 2:20 | 9:34 | 11:53 | 1.81 M | 17 |

Other prices tried for Taise alone (sit-back on): 25k → 1:14 / 3:02, 20k → 1:13 / 3:00, 10k → 0:46 / 2:04. Overhaul + Taise 15k: 1:12 / 1:56.

What this says:
- **15k hits the target for engaged players** (1:12) and halves the casual wait (4:44 → 2:13). Below 15k the casual time barely moves (10k: 2:04); casual players are then waiting on income, not on him.
- **With Sora behind him, the crew earns its keep:** casual crew swords +40% (356 → 500), the full-rack wait 6.1 → 1.9 h, coins +5%, the Gladius and Zanbatō ~20 min sooner, waits over 15 min 17 → 12.
- **The sit-back estimate cuts the other way:** if players really stop forging once the crew works (Allen 2026-10-29), an earlier crew means less of their own forging, and 12 h coins drop 6% (1.92 → 1.81 M). Taise makes about half what the player does (500 vs 968 swords). That's a separate question: whether the first crafter should out-earn your own hands.

## Questions for Allen

1. Taise at 15,000 and Sora at 12,000?
2. Is ~2 h 15 OK for a casual first hire, or should Taise go further (that needs more income early, not a lower price)?
3. Should Taise out-earn your own forging (faster at Lv. 1, or more crafter speed per level) so sitting back isn't a loss?

If yes to 1: change the two prices in `Shared.Upgrades`, re-export `balance.json`, rerun the sim tests ([[sim-mirrors-game-rules]]).

---
title: Upgrade Time Model — 2026-11-02
status: proposal — a sim tool and a price set; nothing changed in Studio
type: design
updated: 2026-11-02
tags: [design, economy, pacing, upgrades, sim, create-swords]
---

# Upgrade Time Model — 2026-11-02

Allen: "look at the lihfolk vault and read up on tycoon games. i remember it said something about a time based model for game progression. is that what we have?" Then "Yes, model it".

## What the vault says

LihFolk Genre Playbook - Tycoons §3, Progression and Pacing Design §3, Pricing Curves and Upgrade Costs:
- Price each buy in **minutes of income**: `wait(k) = cost(k+1) / income(k)`. Small 1–3 min, meaningful 5–15, big unlocks 15–45, capstones 1–2 h.
- Waits between buys: under ~2 min early, 5–10 min late, rising slowly; after a long wait, a "spectacle" buy.
- Derive every price from the model; don't hand-tune ("fix the model, then derive every price from it again").
- Gates between tracks are "experienced as a chore"; players take the best benefit per coin, not the intended order.

## Is that what we have?

No. Our prices were hand-picked and nudged with the sim. In minutes of income at the moment of buying (sim, today's prices, engaged players) they land inside the vault's bands (2–3 min early, 5–20 later), but:
- **The buys are packed into the first hour.** 28 buys before the Longsword (40 min target), then 22 ordinary buys and 6 milestones across 4 h → 20 h (24 min per buy against the vault's ~10–12).
- **To fill 4 h → 20 h at the vault's late waits takes ~40 more buys**, and ~17 more between the Crafter and the Zanbatō. This is the post-Zanbatō trough ([[Sessions/2026-10-30#One sword chain in the game]]) in numbers.

## The tool

`Development/sim/time_model.py` (scenario `timed` in `scenarios.py` reads its `time_prices.json`):
1. **Order:** every coin buy in the order engaged players (efficient, manager, grinder) first buy them, gates kept (the overhaul's gates, [[Design/Upgrade Tree Review — 2026-11-01#Overhaul proposal — 2026-11-02]]).
2. **Schedule:** the decided targets split the order into stretches: Katana 15 min, Longsword 40 min, Sword Crafter 1 h 30 ([[Design/Decisions Log]] 2026-10-29), Zanbatō 4 h (2026-10-30), Seraph 20 h. Each stretch's time is shared over its buys by a wait curve (1.5 min rising to 12 min at 12 h); a milestone (Crafter, Upgraded Store, crew hires, Etching Table 2, Etcher, the big swords, the Seraph) takes 3 buys' worth.
3. **Price** = its share of time × income at that moment × the stretch's correction. Each pass runs the sim (30 players a type, 22 h), re-measures income and corrects each stretch by how late or early players reach its target (at most ×0.8–1.25 a pass).

Tried first and dropped: pricing each buy by when players happened to buy it ran away (Ore Slot 3 ×571, swords ×0.15), as the sim's players put off what pays little.

## Result (8 passes)

Targets reached by engaged players: Katana 0:12–0:19, Longsword ~0:47, Sword Crafter 1:36–1:42, Zanbatō 3:54–4:39. **The Seraph isn't reached in 22 h**: Thornspire comes at 16–18 h and the Seraph (5.2M, a 92-minute save) after the run ends; more passes would bring it in.

| Buy | Today | Time model |
|---|---|---|
| Ingot Rack / Faster Heating I / Display Table 1 | 460 / 580 / 440 | 1,500 / 1,700 / 1,600 |
| Katana / Longsword | 1,300 / 10,200 | 1,500 / 3,900 |
| Sword Crafter | 40,000 | 28,000 |
| Upgraded Store | 15,000 (overhaul) | 12,000 |
| Haru | 23,000 | 110,000 |
| Zanbatō | 88,000 | 140,000 |
| Jian / Gladius | 50,000 / 60,000 | 8,200 / 9,200 |
| Shop Promoter / Cashier | 40,000 / 50,000 | 340,000 / 390,000 |
| Sword Etcher / Kenji | 270,000 / 460,000 | 1.8M / 3.5M |
| Seraph | 840,000 | 5.2M |

The pattern: the first-ring pads are ~3× too cheap, mid swords ~5× too dear, the staff and late crew far too cheap for where they sit. Full list: `Development/sim/time_prices.json`.

## Before using these prices

- **Rerun on today's export.** The runs used the 2026-11-02 00:31 `balance.json`; the 17:34 export adds the Showcase Stands ([[Sessions/2026-11-02#Showcase Stands]]). Rerun `overhaul-check2` (`run.py --scenarios overhaul`), then `python time_model.py 8`.
- **The Sword Crafter is 20,000 since 2026-11-02** (Allen's pick; the model said 28,000). Pinned in `time_model.py`'s `FIXED`.
- **Content, not prices, is the late-game gap.** Prices alone stretch 22 late buys over 16 h. Allen's call: ~40 new buys for 4–20 h, or an earlier Seraph target (~10 h fits today's content at the vault's waits).
- Casual players weren't in the pricing runs; check them on the final set.

## On the built gates (2026-11-02, evening)

After the overhaul was built ([[Sessions/2026-11-02#Upgrade overhaul built]]), rerun on the 19:02 export with the Crafter 20,000 and Stocker 12,000 pinned (10 passes): the early stretches hold (Katana 0:14, Longsword 0:40, Crafter ~0:55), but the Zanbatō swings 2:31–4:59 and the Seraph between 17–19 h and never, pass to pass. With 22 ordinary buys over 16 h each is a 20–90 min save, so the late prices can't settle. **Not applied.** The late game needs its content decided first; then rerun `python time_model.py 10`.


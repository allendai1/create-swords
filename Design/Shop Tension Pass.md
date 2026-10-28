---
title: Shop Tension Pass
type: design
status: built 2026-10-27 (recommended picks), not played
updated: 2026-10-27
tags: [design, economy, customers, events, urgency]
---

# Shop Tension Pass

Allen picked all three suggestions from [[Design/Pottery Playthrough 2026-10-27#Compared with Sell Swords!]]: an offer spread, a customer rush, and a felt first heating upgrade. Two of them meet earlier decisions, so they are reshaped to fit:
- **No lowball offers** ([[Design/Decisions Log]], Refinement 4: "Customers should never make lowball offers", value to +20%). The spread can only go up, so it becomes **VIP buyers**: the high tail of Pottery's +10%–139%.
- **The rush is the Sunshine weather** from the monetization plan (Allen: "sunshine can give 2x more customers", about 5 minutes). It is built free first; the bought version comes with the monetization work.

The [[Design/Urgency Review#5. Guardrails|guardrails]] hold throughout: nothing before Ore Slot 2, one surprise at a time, nothing owned lost, no Robux prompt during an event.

## Model

`Development/economy_model.py` run on 2026-10-27 with the pass-2 prices for a casual Rare+ picker following the plan, with customers on. The variants were patched in from a scratch script; the model file is unchanged. These are estimates.

| Variant | Katana | Crafter | Gladius | Rin (last goal) | Swords carted |
|---|---|---|---|---|---|
| Today | 21 min | 2 h 05 | 5 h 43 | 13 h 12 | 151 |
| Heating 10 / 6 / 4 / 3 s | 21 min | 2 h 03 | 5 h 39 | 13 h 04 | 170 |
| VIP 5% of walk-ins at ×2 | 19 min | 2 h 01 | 5 h 33 | 12 h 48 | 166 |
| VIP 8% at ×2 | 19 min | 1 h 57 | 5 h 26 | 12 h 31 | 174 |
| Sunshine 5 min in every 20 | 20 min | 2 h 05 | 5 h 43 | 13 h 04 | **0** |
| All three (VIP 5%) | 19 min | 2 h 00 | 5 h 28 | 12 h 29 | 0 |

All three together bring the plan about 5% sooner (43 min over 13 h). That is inside the plan's slack, so **no reprice is needed**.

## 1. VIP buyers (recommended: 5% of walk-ins)

- **Who:** about 1 walk-in in 20, from Ore Slot 2 on. A gold name tag over the head marks them (a `WorldText` template, cloned by `ShopService`).
- **Offer:** ×1.75–2.25 the sword's value (×2 average), plus the usual ×1.25 if they like it. Declining gets no raise, so the choice is take it or lose it.
- **Timer:** they wait **60 s** (others 45 s), so the walk over is worth it.
- **Later hooks:** the rainbow weather raises the VIP chance, and the VIP pass's +10% stacks on top.
- **Cost:** about 3% sooner across the plan.
- **Where:** a `VIP` entry in `Shared/Customers` (weight 0 until Ore Slot 2, then picked by its own 5% roll), a per-customer timeout in `ShopService.askOwner`, and the offer card's gold style in `ShopController`. The model gets a `vip=(p, mult)` option.
- **About 2–3 hours.**

**Browsers who don't offer (recommended: skip them).** Pottery's slump after its tutorial came partly from customers who looked and left. With our walk-ins at 45–75 s since today, a browser would be a full minute with no sale. Keep Pottery's good part instead: a customer **says a line about the sword** while looking ("That etch is beautiful!", "A Gold katana!"), naming its metal, etch or polish, then makes the offer as usual. Flavour only, about 1 hour.

## 2. Sunshine weather (recommended: 5 min, every 15–25 min)

- **Effect:** walk-in gaps ×0.5 (45–75 s becomes 22–38 s) for 5 minutes, server-wide on all six shops.
- **When:** random, 15–25 minutes apart, never before a player's Ore Slot 2. A player still in the tutorial just doesn't get the effect.
- **Shown:** a HUD sun icon with a countdown (a `StarterGui` template sized with Scale and constraints), brighter `Lighting` for its length, and the street NPCs picking up.
- **What it does in numbers:** little to coins (about 8 min over 13 h). It empties the backlog: no sword goes by cart at 0.8×, against 151 today. A hand-crafter (no swords waiting) feels it as offers coming twice as fast, so they hurry to restock. That's the Pottery tension. With the crafter and stocker, it's the moment the full shelves sell.
- **Where:**
  - a new `ServerScriptService.Weather` that sets a `Weather` attribute plus an end time on `ReplicatedStorage`;
  - `ShopService` multiplies the gap by 0.5 when sunny;
  - a `WeatherController` for the HUD and lighting.
  - The other three weathers (rainbow, rain, snow) and buying weather slot into the same service later.
- **About 3–4 hours.**

## 3. Faster Heating I that you feel (recommended: 10 → 6 s)

- `Upgrades.HEAT_TIMES` goes from {10, 8, 6, 4} to **{10, 6, 4, 3}**. The first level takes off 40% instead of 20%, and the last level reaches 3 s.
- **Cost:** about 2 minutes sooner over the whole plan.
- **The pad:** it keeps its one-line name. The furnace's countdown shows the shorter time from the first ingot.
- **About 15 minutes.** No save change: the level is stored, the times are not.

## 4. Offer timer: measure, don't change yet

45 s stays. In the next playtest, count offers that expire before you reach the customer. More than 1 in 4 → raise it to 60 s.

## Decisions for Allen

1. VIP share: **5%** (recommended), 8%, or 10% at ×1.75?
2. Browsers: **skip, with sword lines** (recommended), or real browsers who leave without an offer?
3. Sunshine spacing: **every 15–25 min** (recommended), or rarer?
4. Heating: **10 / 6 / 4 / 3** (recommended), or 10 / 7 / 5 / 3?

Suggested build order: Heating (15 min) → VIP and sword lines (3–4 h) → Sunshine (3–4 h).

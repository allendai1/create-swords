---
title: Monetization Pricing Pass — 2026-11-11
status: prices applied, first-buy double and Daily Deal built 2026-11-11 (not played); coin packs and Fireworks open
type: design
updated: 2026-11-11
tags: [monetization, robux, pricing, game-pass, developer-product, create-swords]
---

# Monetization Pricing Pass — 2026-11-11

Allen: "Can we do a monetization pass for our game. Are passes/developer products too cheap for some, or too expensive? ... Ideally we have some cheap products for sale as well that are repeatable, or can get their foot in the door for more purchases."

**The six price changes were applied later the same day** (Allen: "Yes, apply them"; readback 9 of 9, [[Design/Monetization Plan#Price changes (2026-11-11)]]). The rest is proposed. Skills read: roblox-collaboration-mode, roblox-monetization. Checked against [[Design/Monetization Plan]], [[Design/Monetization Review — 2026-11-08]], [[Design/Monetization Ideas — 2026-10-31]], [[Design/Monetization Ideas — 2026-11-09]] and [[Design/Economy and Progression Review — 2026-11-08]].

## What this rests on

- **No sales data.** Analytics Query API, Swordsmith Tycoon (10769630190), 2026-11-05 to 2026-11-09: DAU 4, 7, 10, 5, 1; paying users 0 every day; `ItemMonetizationRevenue` empty for 2026-11-08 to 2026-11-11. So every verdict below is from the sim's value per pass and the market bands in the 2026-10-31 notes, not from buyers.
- **Live prices read back from Roblox today** (Open Cloud list, both passes and products). Managed pricing is on for all of them, so Roblox will test prices itself once there are buyers.

## Verdicts

| Item | Now | Verdict | Proposed | Why |
|---|---|---|---|---|
| 50% More Coins | 199 | too cheap | **249** | The strongest pass: +107% coins over 10 h (sim, efficient), Rin 13 h 17 → 9 h 18. 2× cash sells for 299–399 elsewhere |
| VIP | 299 | too expensive | **199** | +40% coins in the sim against More Coins' +107%, at 100 R$ more. Open since the 2026-11-08 review |
| 50% More Gems | 199 | too expensive | **149** | Only letters, mail and carts: most player types earn 295–597 gems in 24 h, so it adds 150–300 gems over a whole day of play (135–270 R$ of gems), and mail players already end with 744 unspent |
| Sunshine, Snow | 79 | too expensive | **39** (gems stay 60) | 5 minutes, and each already falls free about a third of the time (weights 35 and 30 of 100). The only repeatable that isn't currency should be an impulse price |
| Golden Hour | 149 | too expensive, and off sale | **99** (gems stay 120) | Bought-only and three bonuses, so it keeps a premium over 39. Still `isForSale: false` on Roblox |
| 100,000 Coins | 449 | too expensive | see below | 2.8 min of a casual player's income at 20 h (35,618 a minute) |
| 300,000 Coins | 999 | too expensive | see below | 8.4 min of that income; the dearest item in the shop |
| Auto Anvil, Auto Etch, Bigger Bag | 49 | fine | — | The impulse rung |
| Swift Boots | 99 | fine | — | +16% in the sim |
| Auto Ore Roller | 149 | fine | — | Beside the 179 Automation Pack it makes the pack the obvious buy |
| Lucky Metal | 149 | fine | — | Weak in pace (+3%) but luck sells to collectors; others charge 399–800 |
| Automation Pack | 179 | fine | — | 28% off |
| Starter Pack | 99 | fine | — | 2.5× the gem packs' value |
| Everything Bundle | 599 | fine | — | 1,092 R$ apart today (45% off); 1,042 after the changes above (43% off) |
| 7 / 15 / 80 / 500 Gems, 800 / 1,800 / 5,000 / 20,000 Coins | 9–449 | fine | — | Small packs are top-ups for the short-of-gems offer |

**The two big coin packs.** They are fixed amounts (Allen, 2026-10-28) while income grows about 1,000× over the game, so they are far too dear late and nothing else in the shop is priced that badly. Options: (a) leave them, since few players will reach for them; (b) make the top two "1 hour / 3 hours of your income" (the description stays a fixed sentence); (c) take them off sale. Claude's pick: (b).

**Each price change is two PATCHes** where the item has a gift copy (VIP, More Coins, More Gems), and the Bundle's Shop card works its "apart" total out live.

## Cheap, repeatable, foot in the door

Today the cheapest things are also the worst value in the shop (7 gems at 0.78 a Robux against 1.11 for the 500 pack), and the only repeatable that isn't currency costs 79.

1. **Weather at 39 R$** (above). No build: a price change. The buyer is named to the whole server, which is the best advert the shop has.
2. **First buy of each gem pack gives double.** No new product: a flag per pack in the save, a "2×" tag on the card until used. 9 R$ then buys 14 gems, which is a real first purchase. About 1 h.
3. **Daily Deal:** one product, 29 R$ for 40 gems, once a day per player (1.4 gems a Robux, better than any pack). A real limit, not a countdown. About 2 h.
4. **Fireworks over your shop, 19 R$** (asked on 2026-10-31 and 2026-11-08, never answered). Fun only, everyone sees it. About 2–3 h.

## Seen, not changed

- Rain's description on Roblox (3729904356, off sale) has broken arrows ("â†’"); fix before it goes on sale.

## Questions for Allen

1. Apply the six price changes (More Coins 249, VIP 199, More Gems 149, Sunshine and Snow 39, Golden Hour 99)?
2. The two big coin packs: leave, income-based, or off sale?
3. Which of the cheap items to build: double first buy, Daily Deal, Fireworks?

---

Related: [[Design/Monetization Plan]] · [[Design/Monetization Review — 2026-11-08]] · [[Sessions/2026-11-11#Monetization pricing pass]]

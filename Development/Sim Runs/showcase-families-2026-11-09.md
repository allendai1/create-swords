# Sim run: showcase-families-2026-11-09

`Development/sim/showcase_families.py` wraps `engine.Sim`: the Showcase families aren't in the game yet. Setup for every run:
- free players, casual and efficient, 12 seeds each, 10 h of play;
- every Showcase Stand the player owns holds its best sword of **one** family: that family's best collected metal, its best sword type, polished and etched once those are owned;
- the families and numbers are [[Design/Tycoon Psychology Review — 2026-11-09#Showcase families, redraft 2 (Allen: "Yes, redraft", 2026-11-09)]].

Results are coins earned in each stage, as % over stands that give nothing ("none"). "today" is the game's rule now: every stand pulls customers, at a Rare metal.

**Limits:**
- The stand's sword is never taken off sale.
- The sim's player buys pads the same way whatever the stands give.
- The Cashier's till ignores Coins.
- **0-1 h numbers are mostly noise.** Showcase 1 comes at 18-37 min, and one cheap stand is worth a few %, so a ±20% swing there is two different random paths, not the stand.

## Run 1: redraft 2's numbers

| casual | 0-1 h | 1-4 h | 4-10 h | gems | Zanbatō |
|---|---|---|---|---|---|
| today | +3% | +3% | +39% | -18 | 7.3 h |
| **Customers** | +19% | **+11%** | **+80%** | -40 | 7.1 h |
| VIP | +22% | +9% | +13% | -2 | 7.4 h |
| Coins | +9% | +9% | +21% | -2 | 7.3 h |
| Luck | +16% | +5% | +10% | -2 | 7.6 h |
| Crew | +7% | 0% | +3% | +10 | 7.8 h |
| Swift | +15% | -2% | +4% | +6 | 7.8 h |
| Mail, Gems, Forge, Cart | 0 to +20% (noise) | -3 to 0% | -1 to +1% | -4 to +4 | 7.8-7.9 h |

| efficient | 0-1 h | 1-4 h | 4-10 h | gems | Seraph |
|---|---|---|---|---|---|
| none | | | | | 8.54 h |
| today | +9% | +10% | +20% | -34 | 8.00 h |
| **Customers** | 0% | **+20%** | **+32%** | -54 | 7.65 h |
| VIP | -1% | +7% | +15% | +2 | 8.23 h |
| Coins | +5% | +12% | +29% | 0 | 8.00 h |
| Luck | +3% | +4% | +4% | -2 | 8.48 h |
| Crew | +2% | 0% | +3% | +20 | 8.45 h |
| Swift | +1% | +1% | +3% | +21 | 8.55 h |
| Mail, Gems, Forge, Cart | 0 to +1% | -3 to -1% | 0 to +3% | -2 to +12 | 8.50-8.55 h |

**Passes vs full stands (efficient, coins in 10 h):**

| Family | Full stands | The pass | Both |
|---|---|---|---|
| Luck | +2.9% | Lucky Ore +3.0% | +3.6% |
| Coins | +26% | 50% More Coins +88% | +127% |
| Swift | +1.5% | Swift Boots +18% | +20% |
| VIP | +14% | VIP +44% | +44% |

## Run 2: caps on the strong three

Customers capped at 20%, Coins at 8%, Luck at 0.15. Crew doubled (2% a point, cap 60%) to see whether a supply stat can matter at all.

| | casual 1-4 h | casual 4-10 h | efficient 1-4 h | efficient 4-10 h | efficient Seraph |
|---|---|---|---|---|---|
| today | +3% | +39% | +10% | +20% | 8.00 h |
| Customers (cap 20%) | +10% | **+36%** | **+17%** | +13% | 8.12 h |
| VIP | +9% | +13% | +7% | **+15%** | 8.23 h |
| Coins (cap 8%) | +9% | +13% | +9% | +14% | 8.14 h |
| Luck (cap 0.15) | +4% | +9% | +4% | +1% | 8.64 h |
| Crew (doubled) | 0% | +2% | -2% | +6% | 8.37 h |

**Passes:** Luck stands -0.2% against Lucky Ore +3.0%; Coins stands +13% against 50% More Coins +88%.

## What it says

1. **The shop runs short of customers for all 10 hours** (as the 2026-11-08 review found for the Promoter). So only stats that bring customers or raise what a sale pays move income: Customers, VIP, Coins, a little Luck. Crew, Forge, Swift, Cart, Mail and Gems stay within about ±3%. Doubling Crew didn't change that, so their numbers can't fix it.
2. **Redraft 2's Customers wins every stage:** +80% late for casual players, +32% for efficient players.
3. **With the caps, efficient players get a real choice:** Customers is best at 1-4 h (+17%), VIP at 4-10 h (+15%), Coins close behind both (+14%). Casual players still get the most from Customers late (+36%): they buy fewer customer upgrades, so customers stay their bottleneck.
4. **Every pass stays worth buying:** each beats full stands of its family by a wide margin with the caps.
5. **Gems and Mail families add 4-12 gems in 10 h,** which is nothing. Customers costs 40-54 gems, because more shop sales mean fewer cart trips.

## Run 3: more customers instead? (Allen: "cant we just increase the limit on customers per store or have more customers?")

Free players, 10 seeds, 10 h, no stand bonuses.
- **"walk-ins x1.5" / "x2":** every Better Advertising level's walk-in gap divided by 1.5 or 2.
- **"2 more at once":** `shop.walkIns` 2 -> 4.
- **"Shop full":** the share of walk-ins turned away because the shop's room was full.
- **"Nothing to buy":** customers who came in to empty shelves.

| | Coins | Zanbatō | Seraph | Made / sold / carted | Shop full | Nothing to buy |
|---|---|---|---|---|---|---|
| casual, now | | 7.55 h | - | 1,403 / 1,056 / 278 | 0% | 58 |
| casual, walk-ins x1.5 | +56% | 6.60 h | - | 1,604 / 1,348 / 200 | 1% | 132 |
| casual, walk-ins x2 | +121% | 6.05 h | - | 1,740 / 1,636 / 60 | 4% | 260 |
| casual, 2 more at once | -3% | 7.54 h | - | 1,409 / 1,058 / 285 | 0% | 58 |
| efficient, now | | 3.73 h | 8.63 h | 1,804 / 1,446 / 298 | 0% | 70 |
| efficient, walk-ins x1.5 | +28% | 3.31 h | 7.59 h | 1,842 / 1,684 / 110 | 1% | 298 |
| efficient, walk-ins x2 | +42% | 3.10 h | 7.09 h | 1,856 / 1,745 / 34 | 3% | 650 |
| efficient, 2 more at once | +1% | 3.73 h | 8.56 h | 1,812 / 1,470 / 292 | 0% | 74 |

**Crew family (cap 30%) with walk-ins x2,** efficient: +1.5% (Customers +9.3%).

**What it says:**
1. **The cap is never the limit:** 0% of walk-ins find the shop full today, so room for 2 more changes nothing. What limits sales is how often customers come.
2. **More walk-ins pay a lot** (x1.5: +28-56% coins) and send far fewer swords to the cart at 0.8x. But the whole game speeds up: the Zanbatō comes 25-60 min sooner and the Seraph 1 h sooner, so the post-Seraph trough (the 11-08 review's first finding) comes sooner too. It needs a pricing pass or more content with it.
3. **Even at x2, Crew stands do almost nothing.** Customers then often find empty shelves (efficient: 650 times in 10 h), but made swords barely rise (1,804 -> 1,856). The limit moves to getting swords onto the shelves (Stocker, holders), not to crafting speed.

## Run 4: six families on the new walk-in rate

Allen: "just do 6 for now, maybe later we can add more". Six families (the table in [[Sessions/2026-11-09#Showcase families built: six stats by metal]]), walk-ins already 1.5x with 10,000+ prices x1.3. 12 seeds, 10 h, free players; % coins over stands that give nothing.

| casual | 0-1 h | 1-4 h | 4-10 h | gems | Zanbatō |
|---|---|---|---|---|---|
| none | | | | | 7.84 h |
| Customers (cap 20%) | -8% | +1% | **+35%** | -36 | 7.48 h |
| VIP | +1% | +1% | +18% | -4 | 7.50 h |
| Coins | +6% | +8% | +16% | 0 | 7.58 h |
| Luck | +1% | +3% | +8% | -1 | 7.72 h |
| Mail | 0% | 0% | +6% | +1 | 7.88 h |
| Swift | -3% | -2% | +7% | +7 | 7.82 h |

| efficient | 0-1 h | 1-4 h | 4-10 h | gems | Seraph |
|---|---|---|---|---|---|
| none | | | | | 8.79 h |
| Customers | -2% | **+12%** | +11% | -19 | 8.44 h |
| VIP | +1% | **+12%** | +14% | 0 | 8.35 h |
| Coins | +3% | +10% | **+16%** | +8 | 8.26 h |
| Luck | -2% | +3% | +2% | +4 | 8.75 h |
| Mail | 0% | +2% | -3% | **+22** | 8.87 h |
| Swift | -3% | +3% | +4% | +23 | 8.75 h |

**Passes against full stands (efficient, 10 h):**

| Family | Full stands | The pass | Both |
|---|---|---|---|
| Luck | +1.7% | Lucky Ore +2.6% | +2.9% |
| Coins | +15% | 50% More Coins +107% | +127% |
| Swift | +3.2% | Swift Boots +16% | +24% |
| VIP | +14% | VIP +40% | +61% |

**What it says:**
- **Efficient players get a real three-way choice:** Customers and VIP lead at 1-4 h, Coins at 4-10 h, all within a few %. Mail is the gem pick (+22 gems).
- **Casual players still get the most from Customers late (+35%):** customers stay their bottleneck. That's acceptable. A 15% cap is the knob if it should be closer.
- **Every pass stays well ahead of full stands.**
- **The engine now applies the families itself** (`stand_swords` / `stand_effects`). Its player fills the stands with its rarest collected metals, a different metal a stand. Against this afternoon's run on the same walk-ins: casual Zanbatō 7:26 (7:19), Seraph 14:42 (14:18); efficient 3:42 (3:47), 8:18 (8:29). That's within noise.

## Run 5: sword points 0-6 (2026-11-09, later)

`python showcase_families.py 12 10` after `Showcase.SWORD` (sword type 0-6 along the chain, was difficulty past 1 = 0-4, stopping at Rapier). [[Sessions/2026-11-09#Showcase sword points stretched to 0-6]]

| Family | casual 4-10 h (Run 4) | efficient 1-4 h (Run 4) | efficient 4-10 h (Run 4) | efficient gems (Run 4) |
|---|---|---|---|---|
| Customers | +34.9% (+34.9%) | +11.7% (+11.7%) | +10.9% (+10.9%) | -19 (-19) |
| VIP | +17.8% (+17.8%) | +11.6% (+11.6%) | +14.0% (+14.0%) | +0 (+0) |
| Coins | +16.0% (+16.0%) | +9.7% (+9.7%) | +16.1% (+16.1%) | +8 (+8) |
| Luck | +8.2% (+7.9%) | +3.3% (+3.2%) | +3.0% (+2.1%) | +13 (+4) |
| Swift | +6.6% (+6.6%) | +3.3% (+3.3%) | +3.7% (+3.7%) | +23 (+23) |
| Mail | +0.0% (+6.0%) | +1.5% (+2.1%) | -3.5% (-2.6%) | +18 (+22) |

Passes against full stands (efficient, 10 h): Luck stands +3.0% (was +1.7%), Lucky Ore +2.6%, both +6.3%; Coins +15.4% vs +107%; Swift +3.2% vs +16%; VIP +14.3% vs +40%. Unchanged except Luck.

**What it says:**
- **Almost nothing moves.** The extra points only come from Thornspire on (5) and Claymore/Flamberge (6), which the sim's players reach after 4 h, when most families are already at their cap. Customers, VIP, Coins and Swift give exactly what they did.
- **Luck reaches its cap sooner** (15 points). In coins, full Luck stands (+3.0%) now edge past the Lucky Ore pass (+2.6%). Both are small and within a few seeds' noise. In luck itself the pass is still 3.3x the stands (+0.5 vs the +0.15 cap), and Lucky Ore's value is the odds, not coins. Not changed; watch it if the Luck cap ever goes up.
- **Mail casual +6.0% -> 0.0%** is noise: Mail pays casual players almost nothing in coins either way.
- Pacing (Zanbatō, Seraph) unchanged.

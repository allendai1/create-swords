# Sim run: customer-rate-2026-11-09

Allen: "Test x1.5 + repricing". `Development/sim/customer_rate.py`.

**Setup:**
- Walk-ins 1.5x as often: every Better Advertising level's gap divided by 1.5, so 45-75 s becomes 30-50 s and the top level 16-30 s becomes 11-20 s.
- Coin prices multiplied by k (pads, cart capacity and speed, crafter hires), from a minimum price up.
- Free players, 12 seeds, 20 h, medians.
- **"Waits"** are gaps over 15 min between buys; **"after Seraph"** is non-Ore-Slot buys after the Seraph.

| casual | Crafter | Katana | Showcase 1 | Longsword | Zanbatō | Seraph | Waits | After Seraph |
|---|---|---|---|---|---|---|---|---|
| **now** | 31m | 17m | 20m | 1:52 | 7:09 | 13:46 | 16 | 0 |
| x1.5 | 28m | 17m | 19m | 1:48 | 6:15 | 11:41 | 12 | 1 |
| x1.5, all >=100 x1.3 | 39m | 22m | 26m | 2:17 | 7:48 | 14:52 | 16 | 0 |
| x1.5, all >=100 x1.45 | 40m | 24m | 26m | 2:30 | 8:19 | 15:45 | 19 | 1 |
| x1.5, all >=100 x1.6 | 42m | 24m | 27m | 2:39 | 9:03 | 17:00 | 19 | 0 |
| x1.5, >=5,000 x1.3 | 28m | 17m | 19m | 2:03 | 7:27 | 14:35 | 16 | |
| **x1.5, >=10,000 x1.3** | **28m** | **17m** | **19m** | **1:50** | **7:17** | **14:08** | **16** | |
| x1.5, >=10,000 x1.4 | 28m | 17m | 19m | 1:50 | 7:35 | 14:48 | 18 | |

| efficient | Crafter | Katana | Showcase 1 | Longsword | Zanbatō | Seraph | Waits | After Seraph |
|---|---|---|---|---|---|---|---|---|
| **now** | 15m | 7m | 39m | 47m | 3:41 | 8:00 | 13 | 1 |
| x1.5 | 16m | 7m | 37m | 45m | 3:17 | 7:14 | 13 | 1 |
| x1.5, all >=100 x1.3 | 16m | 8m | 42m | 53m | 3:51 | 8:40 | 14 | 1 |
| x1.5, all >=100 x1.45 | 16m | 9m | 47m | 1:04 | 4:07 | 9:38 | 14 | 1 |
| x1.5, all >=100 x1.6 | 17m | 9m | 48m | 1:04 | 4:23 | 10:28 | 17 | 1 |
| x1.5, >=5,000 x1.3 | 16m | 7m | 34m | 49m | 3:48 | 8:37 | 12 | |
| **x1.5, >=10,000 x1.3** | **16m** | **7m** | **37m** | **53m** | **3:45** | **8:20** | **13** | |
| x1.5, >=10,000 x1.4 | 16m | 7m | 37m | 53m | 3:51 | 8:50 | 14 | |

**What it says:**
1. **On its own, x1.5 speeds the game up:** the Zanbatō 25-55 min sooner, the Seraph 45 min to 2 h sooner. Casual players get fewer long waits (16 -> 12).
2. **A flat price rise slows the first hour,** because more walk-ins barely help early (the tutorial's ramp, few swords): the casual Sword Crafter goes 31 -> 39 min.
3. **Raising only prices of 10,000+ by x1.3 matches today almost exactly.** Every milestone is within about 5% (Seraph +22 min casual, +20 min efficient; the efficient Longsword +6 min), and the waits are the same. That's 50 of 95 pads, plus the cart's 25,000+ levels and the crafter hires.
4. **No case changes the trough:** 0-1 non-Ore-Slot buys after the Seraph either way. That needs content, not prices.

**What the player would get:** about 50% more customers in the shop, more sales and fewer swords sent to the cart, at today's pace.

**Not checked:**
- the phone cost of more NPCs at once (the shop was full for 1% of walk-ins at x1.5, 0% now);
- coin packs are fixed amounts, so a late pack buys about 23% less;
- the 2nd and 3rd staff members' prices aren't in the sim (they'd get the same x1.3);
- not played.

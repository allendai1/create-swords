# Economy Review — 2026-10-29

Allen: "Thoroughly analyze the game's economy and progression now with all these new swords."

The game as built on 2026-10-29: 24 swords on three blueprint pads (Eastern, Western & World, Fictional), no anvil gates, Furnaces 2–3 with their own heating. Built in Edit, **not played**.

The numbers come from [[Development/economy_model.py]], with its pads updated to today's tree. Each run is a player from the first second to 40 h.

**How the data was made:**
- Live values were read from fresh copies of the Studio modules.
- Every sword takes the same 12 hammer strikes, so every sword takes as long to forge.
- Scripts: scratch `econ_review.py` and `econ_alt.py`.

**What the model doesn't cover:**
- Mail orders and the cart's real trips.
- Gems.
- Decorations.
- How often the Big Sword Stand's sword sells. It assumes one in three of your own swords is big (`ZANBATO_EVERY`).

## 1. When each sword comes

Four players are modelled; each buys the cheapest thing on offer:
- **Casual:** a Rare+ ore picker.
- **Relaxed:** casual, 1.5× slower.
- **Focused:** about 50 s a sword, buys blueprints first.
- **Never picks:** never chooses ores.

| Sword | Pad | Base | Price | Casual | Relaxed | Focused | Never picks |
|---|---|---|---|---|---|---|---|
| Wakizashi | East | 45 | 60 | 4 min | 6 min | 3 min | 4 min |
| Machete | West | 70 | 600 | 13 min | 20 min | 9 min | 22 min |
| Katana | East | 110 | 1,300 | 21 min | 32 min | 7 min | 33 min |
| Scimitar | West | 135 | 6,000 | 1 h 08 | 1 h 41 | 13 min | 2 h 18 |
| Longsword | West | 160 | 17,000 | 2 h 02 | 2 h 53 | 23 min | 4 h 19 |
| Cutlass | West | 185 | 26,000 | 3 h 21 | 4 h 18 | 37 min | 6 h 31 |
| Falchion | West | 220 | 50,000 | 4 h 42 | 5 h 46 | 58 min | 8 h 29 |
| Jian | East | 245 | 80,000 | 6 h 00 | 7 h 05 | 2 h 13 | 10 h 19 |
| Gladius | West | 280 | 150,000 | 6 h 55 | 8 h 04 | 1 h 50 | 11 h 36 |
| Khopesh | West | 310 | 190,000 | 7 h 42 | 8 h 53 | 3 h 04 | 12 h 39 |
| Dadao | East | 340 | 240,000 | 8 h 45 | 9 h 59 | 4 h 04 | 14 h 01 |
| Zanbatō (big) | East | 1,000 | 300,000 | 9 h 20 | 10 h 35 | 8 h 58 | 14 h 44 |
| Rapier | West | 380 | 380,000 | 10 h 15 | 11 h 33 | 5 h 32 | 15 h 49 |
| Hook Sword | East | 430 | 520,000 | 11 h 46 | 13 h 12 | 9 h 23 | 17 h 36 |
| Claymore (big) | West | 1,400 | 700,000 | 12 h 16 | 13 h 43 | 9 h 52 | 18 h 09 |
| Flamberge (big) | West | 1,900 | 950,000 | 14 h 19 | 15 h 56 | 10 h 28 | 20 h 29 |
| Crescent Fang | Fict | 480 | 1.2M | 16 h 22 | 18 h 11 | 11 h 10 | 22 h 49 |
| Shard Blade | Fict | 540 | 1.5M | 17 h 11 | 19 h 04 | 11 h 58 | 23 h 44 |
| Moonbite | Fict | 600 | 1.85M | 19 h 39 | 21 h 46 | 12 h 53 | 26 h 34 |
| Serpent | Fict | 680 | 2.3M | 20 h 39 | 22 h 51 | 13 h 56 | 27 h 43 |
| Leviathan Cleaver | Fict | 780 | 2.8M | 23 h 37 | 26 h 02 | 15 h 05 | 31 h 08 |
| Thornspire | Fict | 880 | 3.4M | 24 h 46 | 27 h 15 | 16 h 20 | 32 h 27 |
| Seraph | Fict | 980 | 4.2M | 28 h 12 | 30 h 53 | 17 h 45 | 36 h 24 |

**The spine is unchanged:** for a casual player, the Katana comes at 21 min, the Sword Crafter at 1 h 30, the Longsword at 2 h 02 and the Zanbatō at 9 h 20, as in the [[Archive/Design/Upgrade Order Review — 2026-10-28|upgrade order review]]. Regrouping the pads and removing the anvil gates moved nothing for a casual player, who buys the cheap things first anyway. The focused player gains the most: the Falchion at 58 min and the Gladius at 1 h 50.

**Content ends at about 28 h** for a casual player: 18 h focused, 31 h relaxed, 36 h for a player who never picks.

## 2. What each sword is worth buying

You and your crafters always make your most valuable regular sword, so a blueprint only pays by how much it raises that. Each one is 10–19% above the one below it, except the early steps (Wakizashi +125%, Machete +56%, Katana +57%). Casual player:

| Bought at | Sword | Price | Income before → after (coins/min) | Pays for itself in | Cost in minutes of income |
|---|---|---|---|---|---|
| 13 min | Machete | 600 | 330 → 483 (+46%) | 4 min | 2 |
| 21 min | Katana | 1,300 | 532 → 837 (+57%) | 4 min | 2 |
| 1 h 08 | Scimitar | 6,000 | 970 → 1,191 (+23%) | 27 min | 6 |
| 2 h 02 | Longsword | 17,000 | 1,874 → 2,221 (+19%) | 49 min | 9 |
| 3 h 21 | Cutlass | 26,000 | 3,945 → 4,562 (+16%) | 42 min | 7 |
| 4 h 42 | Falchion | 50,000 | 6,454 → 7,676 (+19%) | 41 min | 8 |
| 6 h 00 | Jian | 80,000 | 9,697 → 10,799 (+11%) | 73 min | 8 |
| 6 h 55 | Gladius | 150,000 | 11,537 → 13,185 (+14%) | 91 min | 13 |
| 7 h 42 | Khopesh | 190,000 | 14,276 → 15,806 (+11%) | 124 min | 13 |
| 8 h 45 | Dadao | 240,000 | 16,062 → 17,616 (+10%) | 154 min | 15 |
| 9 h 20 | Zanbatō | 300,000 | 19,121 → 21,041 (+10%) | 156 min | 16 |
| 10 h 15 | Rapier | 380,000 | 21,085 → 23,221 (+10%) | 178 min | 18 |
| 11 h 46 | Hook Sword | 520,000 | 23,568 → 26,276 (+11%) | 192 min | 22 |
| 12 h 16 | **Claymore** | 700,000 | 26,276 → 27,472 (**+4.6%**) | **585 min** | 27 |
| 14 h 19 | **Flamberge** | 950,000 | 28,407 → 29,953 (**+5.4%**) | **615 min** | 33 |
| 16 h 22 | Crescent Fang | 1.2M | 30,938 → 33,830 (+9%) | 415 min | 39 |
| 17 h 11 | Shard Blade | 1.5M | 33,830 → 37,300 (+10%) | 432 min | 44 |
| 19 h 39 | Moonbite | 1.85M | 38,489 → 42,069 (+9%) | 517 min | 48 |
| 20 h 39 | Serpent | 2.3M | 42,069 → 46,844 (+11%) | 482 min | 55 |
| 23 h 37 | Leviathan Cleaver | 2.8M | 48,290 → 54,442 (+13%) | 455 min | 58 |
| 24 h 46 | Thornspire | 3.4M | 54,442 → 60,595 (+11%) | 553 min | 62 |
| 28 h 12 | Seraph | 4.2M | 62,409 → 68,746 (+10%) | 663 min | 67 |

**Up to the Hook Sword (about 12 h)** the curve is healthy:
- Every buy costs 2–22 minutes of income.
- It pays back in under about 3 h.
- 3–4 things are on offer at once.

**After that:**
- Each buy costs 27–67 minutes of income.
- Payback is 7–11 h, longer than the time to the next sword.

## 3. Income and the shop

| Played | Income (coins/min) | Earned so far |
|---|---|---|
| 1 h | 679 | 41k |
| 4 h | 3,756 | 485k |
| 8 h | 13,295 | 2.6M |
| 12 h | 21,808 | 7.2M |
| 20 h | 36,369 | 21.5M |
| 28 h | 57,430 | 45.2M |
| 40 h | 68,482 | 92.4M |

**Prices outrun income:**
- From the Rapier (10 h) to the Seraph (28 h), prices rise 11× (380k → 4.2M) while income rises 2.7×.
- After the Seraph, income only grows with ore-slot luck: +19% from 28 h to 40 h.

**The shop is full from about 4 h:**
- Walk-ins can't keep up, so a quarter of all swords leave by cart at 0.8× value: 12% at 4 h, 25–28% from 8 h on. That costs about 7% of income.
- The shop always holds about 19 waiting swords.
- Walk-in speed is the late game's bottleneck, and an untapped sink.

## 4. Findings

1. **A carted big sword beats every regular sword in the shop.** A Bulk Order takes any sword at 0.8× its value, and the cart carries up to 15 every 70–150 s.
   - A carted Flamberge (base 1,900) pays 1,520 and a carted Claymore 1,120, against about 1,060 for a Seraph sold in the shop.
   - A carted Zanbatō (800) beats the Crescent Fang, Shard Blade, Moonbite and Serpent in the shop.
   - From the Claymore on, a player's best move is to forge big swords and cart them. The fictional swords only matter for the crafters, who can't make big ones.
   - The model doesn't play this way; it assumes one big sword in three.
2. **The Claymore and Flamberge are poor buys** when they're sold the intended way, one at a time on the Big Sword Stand.
   - Each adds 5% income and takes about 10 h to pay back.
   - Together they cost 1.65M, and the fictional pad waits behind the Flamberge.
   - Moving the fictional pad earlier changes nothing (the model was run with it after the Hook Sword): the big swords are cheaper than the Crescent Fang, so a cheapest-first player buys them first anyway.
3. **The late game is a queue.** From about 12 h 45 to the Seraph, only the next sword and the ore-slot merge loop are on offer.
   - There are ten gaps of 45+ minutes with nothing new, the longest 73 min.
   - The crew is complete with Rin at 12 h 45, and every floor pad is bought by about 10 h.
4. **After the Seraph there is only the merge loop.**
   - The ore slots cost 1.5× more after every merge, so the waits grow: 93, 134 and 197 minutes between buys from 28 h to 40 h.
   - There is nothing new to see or unlock.
5. **The fictional prices were never fitted.**
   - They're Claude's proposal (1.2M–4.2M), and so are the Western & World pad's prices; only the spine to the Zanbatō was fitted.
   - At those prices each fictional sword costs 39–67 minutes of income, rising.
6. **The Eastern pad waits a long time for the Jian.**
   - After the Katana (21 min), its next pad, the Jian at 80,000, sits for about 5 h 40.
   - The Western & World pad keeps moving, so nothing stalls; the Jian is just a long-visible goal.
7. **What's healthy:**
   - The first hour: the Machete and Katana each pay back in 4 min.
   - The spine to the Zanbatō is unchanged.
   - Every sword is worth more than the one before.
   - Every sword forges in the same time, so no sword is a trap.

## 5. Options

**A. Close the cart loophole** (finding 1; small, recommended).
- Pick one:
  - A Bulk Order doesn't take big swords; they sell only on the stand.
  - Or the cart pays less for a big sword.
- Either way the stand's sword stays a showpiece and the fictional swords become your best regular work.

**B. Fit the late prices** (findings 3 and 5). A test run moved the fictional pad after the Hook Sword and priced the swords 0.7M → 2.4M:
- Crescent Fang 700k, Shard Blade 900k, Moonbite 1.1M, Serpent 1.35M, Leviathan 1.65M, Thornspire 2M, Seraph 2.4M.
- Result: the Seraph comes at 20 h 33, not 28 h 12.
- The longest gap from 10 h to the Seraph drops from 73 min to 45 min, and only one gap reaches 45 min (now ten do).
- Each fictional buy costs 25–41 minutes of income, and income at 28 h is 64,900/min instead of 57,400.
- The cost: content ends about 8 h sooner.

**C. Make the big swords worth it** (finding 2). Pick one:
- A second Big Sword Stand.
- Big swords on the shop's Big Sword Stand sell to walk-ins at a premium.
- Lower Claymore and Flamberge prices.

**D. Late sinks beside the queue** (findings 3 and 4). Something to buy between swords from about 12 h on:
- Walk-in rate upgrades (the shop is the bottleneck from 4 h, finding 3 in section 3).
- Crew levels past Lv. 5.
- Decorations (built today, not modelled).
- An endgame loop after the Seraph.

These are design calls for Allen; nothing has been changed.

## Built (2026-10-29, Allen: "both"; not played)

**A. The cart doesn't take big swords:**
- `Shared/Deliveries.mismatch` refuses the Zanbatō, Claymore and Flamberge ("Stand only"), so the cart window doesn't list them.
- `DeliveryService` makes no Special Orders for them.
- Big swords now sell only on the Big Sword Stand, plus the occasional mail order for one (1.2×, one at a time).

**B. The fictional pad was moved and repriced:** it opens after the Hook Sword. New prices: Crescent Fang 700,000, Shard Blade 900,000, Moonbite 1,100,000, Serpent 1,350,000, Leviathan Cleaver 1,650,000, Thornspire 2,000,000, Seraph 2,400,000.

**Rerun, casual player:**
- **Fictional swords:** Crescent Fang 12 h 44, Shard Blade 14 h 36, Moonbite 15 h 40, Serpent 17 h 17, Leviathan 17 h 56, Thornspire 19 h 48, Seraph 20 h 33 (was 28 h 12).
- **Big swords:** the Claymore stays at 12 h 16; the Flamberge moves to 15 h 06 (was 14 h 19).
- **Seraph by player:** focused 14 h 46, relaxed 22 h 36, never-picks 27 h 36.
- **Waits:** from 10 h to the Seraph the longest wait is 45 min, and every gap of 30+ min still has 2–3 things on offer.
- **Fictional swords' cost:** 25–41 minutes of income each, paying back in 4–7 h.
- **Income:** 16 h 33,400/min (was 28,000), 20 h 48,800 (was 36,400), 24 h 62,900 (was 45,600).

**Still open:**
- Option C (the Claymore and Flamberge still add about 5% each).
- Option D (late sinks): after the Seraph, only the merge loop is left, with waits of 1–3 h.

## Customers, weather and ore odds (added after Allen asked, same day)

Checked against the live modules (`ShopService`, `Customers`, `GemUpgrades`, `Weather`, `Materials`, `Upgrades`, `Orders`). Runs are scratch `econ_weather.py` (casual picker, the built prices).

**Customers:**
- **Offers:** the model's offers match the live `Customers`. The customer mix is Farmer 5, Adventurer 3 and Knight 2; every first offer is at least the sword's value, and a VIP pays 1.75–2.25×.
- **What isn't modelled:** declining for a raise, and the 45 s answer window before the Cashier. The model assumes every walk-in buys.
- **Walk-in rate:** the model's Better Advertising level 3 was out of date (22–42 s; live 25–45 s), now fixed. Levels 4–5 (20–38 s and 16–30 s, 200 and 320 gems) aren't in the model's timeline.
- **How many fit at once:** 2, +1 with the Shop Promoter, +1 per Rickshaw Bay, so up to 6. Walk-ins every 23–60 s staying 30–60 s means 0.5–2.6 customers inside at once, so the limit hardly ever binds.

**Weather** (5 min each, never the same twice running). By weight, Sunny is on 31.4% of the time, Snow 29.0%, Rain 22.1% and Rainbow 17.6%. On average:
- **Walk-ins:** ×1.31 (Sunny doubles them).
- **VIP chance:** ×1.35 (Rainbow triples it).
- **Mail:** ×1.29 (Snow doubles it).
- **Luck:** +0.5 for 22% of the time (Rain).

| Run (casual) | 6 h | 12 h | 20 h | Sent by cart at 12 / 20 h | Zanbatō | Seraph |
|---|---|---|---|---|---|---|
| Model as was (no weather, old Advertising 3) | 7,018 | 21,808 | 48,832 | 26% / 25% | 9 h 20 | 20 h 33 |
| Live Advertising, no weather | 7,018 | 20,927 | 47,073 | 31% / 31% | 9 h 24 | 20 h 53 |
| Live Advertising + weather | 8,166 | 25,939 | 61,837 | 11% / 10% | 8 h 51 | 19 h 14 |
| + Advertising 4 at 10 h, 5 at 16 h | 8,166 | 27,855 | 67,285 | 9% / 5% | 8 h 51 | 18 h 48 |
| No customer limit at all + weather | 10,026 | 29,393 | 67,781 | 0% | 8 h 24 | 18 h 24 |

- **Weather is worth about +16% income at 6 h and +31% at 20 h.** Nearly all of that is Sunny turning cart sales (0.8×) into shop sales.
- **The "shop full" finding shrinks:** with weather, carting falls from 25–31% to about 10% of swords, and to 5% with Better Advertising 4–5.
- **Prices weren't fitted with weather,** so the real game runs about 4–6% ahead of the timeline in section 1 (the Zanbatō at about 8 h 50 rather than 9 h 20).

**Ore odds:** the model's tiers and luck formula match the live `Materials`:
- **The rolls:** odds are 60 / 25 / 10 / 4 / 1 / 0.1, multipliers ×1 / 1.5 / 2.5 / 5 / 12 / 25, and the cascade show doesn't change the odds.
- **What luck does for a picker:** a player who keeps Rare+ gets a ×3.94 ore at every luck up to about 8 merges. Luck only shortens the pulling, from 5.5 s to 1 s per Rare+ ore with 6 slots, until Common and Uncommon hit their 10% floors. Past that the picked ore climbs to ×4.4 at 12 merges and ×4.95 at 16.
- **For a non-picker,** the average ore rises steadily: ×1.57 at 0 merges, ×2.56 at 4, ×3.29 at 8.
- **So Rain is the weakest weather for a picker:** +0.5 luck changes the picked ore's worth by nothing to 3%. It matters to non-pickers and the Auto-Roll.
- **The model always keeps Rare+.** A late picker who keeps Epic+ (Auto-Roll's rarity) would earn more, so late income is understated.

**Mail orders are a late-game loss:**
- `Orders.make` asks for a random known sword in a collected metal, with commoner metals more likely.
- With all 24 swords known and every metal collected, that averages base 497 × metal ×2.22, about 1,320 at 1.2× pay.
- That's about a third of your best sword sold in the shop (Seraph × a Rare+ pick: 980 × 3.94 × 1.08, about 4,170, before the shared bonuses), plus the pulls to find the metal.
- The 1–3 gems are the only reason to fill one, and Snow doubles how often they come.
- 12% of them ask for a big sword, which pays well (1.2× a 1,000–1,900 base).

**New options:**
- **E.** Weight mail orders toward your best few swords, or pay them as your best sword would sell.
- **F.** Fit the prices with weather in the model, or leave the game running about 5% ahead of the plan.

## Built: mail orders pay like a sale (2026-10-29, Allen: "Yes, weight mail orders toward my best swords so they pay like a normal sale"; not played)

**What changed in `Shared/Orders`:**
- **Which sword:** an order asks for one of your three most valuable regular swords, weighted 3:2:1, never a big one.
- **What metal pays:** the order's metal counts at no less than a typical ingot at your merges' luck (`Orders.typicalMetal`: ×1.57 at 0 merges, ×2.37 at 3, ×3.29 at 8). A Common metal costs no pulls, so the order pays about what a sale does.
- **Rarer metals:** these pay 1.2× as before.
- `ShopService` passes the metal and the luck to `Orders.pay`.
- Cart Special Orders use the same pick.

**Simulated, 3,000 orders each:**
- **Late** (all 24 known, 8 merges): the Seraph 49%, Thornspire 33% and Leviathan 17%. Pay averages 4,167 per unit of the shared bonuses, against 4,170 for a Rare+ Seraph sold in the shop (was about 1,320).
- **Mid** (up to the Gladius, 3 merges): the Gladius, Jian or Falchion, paying 929. That's between a non-picker's sale (717) and a picker's (1,191).
- **Start** (Tantō and Wakizashi known): the Wakizashi 59% and Tantō 40%.

**Not changed:** the mail row's "+20%" chip still shows. For a Common or Uncommon metal the order now pays more than that.

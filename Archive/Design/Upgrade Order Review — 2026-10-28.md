---
title: Upgrade Order Review — 2026-10-28
status: built 2026-10-28 in Edit, not played
type: design
updated: 2026-10-28
tags: [review, economy, progression, upgrades, crew, create-swords]
---

> **Archived 2026-11-01.** Built 2026-10-28; the tree was reviewed again in [[Design/Upgrade Tree Review — 2026-11-01]].

# Upgrade Order Review — 2026-10-28

Allen: "Analyze our current game progression and economy. I feel like the upgrades order is not well constructed."

Sources: the live `Shared.Upgrades`, `Deliveries`, `Employees` and `Blueprints` in Edit (read only, 2026-10-28, after the day's [[Design/Decisions Log#Ore Slots: always the next one — 2026-10-28|Ore Slot]] and [[Design/Decisions Log#Shop-floor pads out of the stage gates — 2026-10-28|shop-floor]] ungating), run through `Development/economy_model.py` with the live prices and `after` gates and the live customer rate (45–75 s walk-ins). The player is the casual Rare+ picker [[Design/Economy Pass 2]] is priced for, buying the cheapest pad on offer. **Nothing here is measured;** the model's seconds are still estimates ([[Design/Economy Pass 2#8. To time in the next playtest]]). The scripts are in the session's scratchpad, not the vault. Proposals are not decisions until Allen picks them.

## The short version

The prices are roughly right for an 8-hour game. The order is the problem:

1. **The first worker is buried.** The Sword Crafter adds half again to your income (+52%, the biggest jump after the first two swords), but he waits behind the Longsword (22,000) and 34,000 coins of prerequisites that do almost nothing: Faster Heating III, Furnace 2 and Anvil 2. From 0:52 to 2:18 only two things are on offer.
2. **The crew comes in a clump at the end.** Crafters are hired at 2:18, then 10:10, 10:51, 11:46 and 13:00. In the six hours between (2:18 to 8:38) you buy staff and shop space, and the model sees almost none of it adding income.
3. **The selling upgrades come before the making upgrades.** You plus one crafter never make swords faster than walk-ins buy them: until the third crafter (about 11 h) six swords wait at once for one minute in all, and never more. 12 of the 21 shop-space, customer and cart buys (93,000 coins) come before 6 swords have ever waited at once (3 h).
4. **Hidden gates with no reason you could guess.** Pads stay invisible until an unrelated goal is bought. You hit this twice today: "how come i can only buy 3", then "why dont i see any more shop upgrades?" (only the 61,000 Falchion on offer).
5. **Prices follow the clock, not the effect.** Each price is the coins earned in its time slot, so do-nothing buys cost as much as big ones, and the Falchion and Gladius are each bought twice (the blueprint, then the crew's training).

**Proposed:** the crafter at about 1 h, three crafters working by about 6 h, each one followed by the shop space and customers its swords need, gates only where the world needs them, and a new sword teaching the crew. The Katana at 20 minutes, the 8 h length and the Zanbatō as the finale stay.

## 1. The first worker is buried

The crafter's chain today: Katana → Longsword (22,000) → Faster Heating III (18,000) → Furnace 2 (4,000) → Anvil 2 (12,000) → Sword Crafter (26,000).

| Buy | Price | Coins a minute it adds | Pays for itself in |
|---|---|---|---|
| Longsword | 22,000 | +437 | 50 min |
| Faster Heating III | 18,000 | +13 (4 s → 3 s heating) | 24 h of play |
| Furnace 2 | 4,000 | nothing by itself | — |
| Anvil 2 | 12,000 | nothing by itself | — |
| **Sword Crafter** | 26,000 | **+750** | 35 min |

- **The wall:** 0:52–1:17 only the Longsword and Ore Slot 5 are on offer, 1:17–2:18 only two things at a time (Heat III, Furnace 2, Anvil 2, the Crafter, Ore Slot 5 at 26,000 for +21 a minute). 86 minutes, six buys.
- **The chain itself is right** (Allen's rule: Furnace 2 waits for Faster Heating III; the crafter needs his own furnace, rack and anvil). The prices on it are what's wrong: 34,000 of the 56,000 before the hire is for buys that do nothing until he comes.

## 2. The crew comes in a clump

| Hire | Today | Gap |
|---|---|---|
| Sword Crafter (Taise, Anvil 2) | 2:18 | |
| Haru (Anvil 3, after the Zanbatō) | 10:10 | 7 h 52 |
| Kenji (Anvil 4) | 10:51 | 41 min |
| Mei, Rin (replace the weakest) | 11:46, 13:00 | |

Allen's "3 anvils can exist" vision lands after 10 hours. Between the first crafter and the Zanbatō, the buys are the Stocker, Shop Promoter, Cashier and Sword Etcher (561,000 coins in all) and the shop space: freedom and capacity, with no sword waiting to use the capacity yet. Anvil 3 and Anvil 4 are bought before any spare crafter exists (Anvil 4 at 9:26, Haru at 10:10).

## 3. Selling before making

Swords made against swords sold (you plus the crew, live walk-in rate):

| Time | 1 h | 2 h | 3 h | 5 h | 8 h | 10 h | 12 h |
|---|---|---|---|---|---|---|---|
| Waiting for a customer | 0 | 0 | 5 | 0 | 0 | 2 | 20 |

[[Design/Economy Pass 2#9. Customer rate]] slowed the walk-ins so the shop upgrades would matter "around the Sword Crafter". With one crafter they barely do: supply and walk-ins run even, and the starting shelves hold what waits. So Wall Racks 3–4 and Display Tables 2–4 (82,000), Rickshaw Bays 1–3 (109,000) and the Shop Promoter (72,000) are bought hours before they hold anything. The cart is different: it's also the gem and reputation faucet, so it has a job early.

## 4. Gates you can't see a reason for

Economy Pass 2 made each stage's pads wait for the goal before it (Allen: "Pads and cart levels"), so a cheapest-first player keeps to the plan. In the world, that reads as:

- the **Falchion** needs the Sword Crafter; the **Stocker** needs the Falchion; the **Shop Promoter** needs the Stocker;
- the **Gladius** needs the Shop Promoter; the **Cashier** needs the Gladius; the **Sword Etcher** needs the Cashier;
- the **Big Sword Stand** needs the Sword Etcher; **Anvil 3** needs the Zanbatō; **Etching Table 2** needs the Stocker.

None of these has a reason a player could guess, and the locked pad doesn't show, so it looks like there's nothing left. The same two rules (a goal is the last 40% of its stage; the next stage's pads wait for it) also build a save-for-the-goal stretch into every stage. Today's two fixes filled that stretch with buys that do nothing yet (shop space, Ore Slots 5–6).

## 5. Prices by the clock

`fit()` prices each buy at the coins earned in its slot of the plan, whatever it does. What each buy adds, in minutes to pay for itself (casual picker):

| Pays back fast | | Pays back in a day or more | |
|---|---|---|---|
| Katana | 4 min | Ore Slot 5 (26,000) | 20 h |
| Sword Crafter | 35 min | Faster Heating III (18,000) | 24 h |
| Longsword | 50 min | Ore Slot 6 (100,000) | 32 h |
| Zanbatō | 101 min | | |
| Falchion | 125 min, +57 min training | | |
| Gladius | 242 min, +130 min training | | |
| Sword Etcher | 418 min | | |

- **Ore Slots 5 and 6** add 1–2% (four slots already pull a Rare+ in about 8 s). Their real reward is the merge's luck, 126,000 coins away.
- **Training tax:** the Falchion needs the crafter, so he's always trained on the Longsword when it arrives; the crew then needs Falchion training (37,000) and later Gladius training (110,000). The Falchion and the Gladius each cost twice (98,000 and 230,000 for the crew to make them).
- **The blueprint ladder flattens while the prices climb:** Katana ×2.44 the Wakizashi's value for 2,000, Longsword ×1.45 for 22,000, Falchion ×1.38 for 61,000, Gladius ×1.27 for 120,000. The Zanbatō (+30% income, the biggest jump of the game) is the right finale.

## 6. Proposed order

Rules, in order of weight:

1. **Make more → sell more → freedom.** Each new crafter is followed by the shop space and customers his swords need; the Stocker, Cashier and Etcher come once there are crafters to free you from.
2. **Something to work toward every 35–60 min,** alternating a sword and a worker, with three crafters working by about 6 h.
3. **Gates only where the world needs them** (a station needs its table, a crafter needs an anvil, the next tier needs the last), and the next locked pad shows on the floor with "After Longsword" in its one-line label.
4. **A new sword teaches the crew** (training stays for switching what an anvil makes).
5. **Price by effect:** do-nothing prerequisites are cheap side buys; the goals carry the pacing.

Modelled with the same casual picker buying the cheapest pad on offer, one stage open at a time as today, Ore Slots ungated as today:

| Goal | Comes with it | Today | Proposed |
|---|---|---|---|
| Katana | Wall Rack 2, Polishing Station, Finished Sword Rack, Display Table 1, Ingot Rack, Faster Heating I, Ore Slot 3 (unchanged) | 0:19 | 0:20 |
| **Sword Crafter** | Etching Table, Faster Heating II–III, Furnace 2, Anvil 2, Ingot Rack 2 | 2:18 | **1:01** |
| Longsword | Finished Sword Rack 2, Rickshaw Bay 1, Delivery Cart, Capacity 1, Speed 1 | 1:17 | 2:06 |
| **Second crafter** (Haru, Anvil 3) | Upgraded Store, Wall Rack 3, Display Table 2 | 10:10 | **3:08** |
| Stocker | Rickshaw Bay 2, Capacity 2 | 4:05 | 3:51 |
| Falchion | Wall Rack 4, Display Table 3, Speed 2 | 3:34 | 4:24 |
| **Third crafter** (Anvil 4) | | 10:51 (Kenji) | **5:53** (Mei) |
| Shop Promoter | Display Table 4, Capacity 3, Rickshaw Bay 3 | 4:45 | 6:43 |
| Gladius | Speed 3 | 6:04 | 7:21 |
| Cashier | Speed 4 | 7:11 | 8:18 |
| Sword Etcher | Etching Table 2 | 7:56 | 8:50 |
| Zanbatō | Big Sword Stand | 8:38 | 9:17 |
| The last two hires, replacing the weakest | | 11:46, 13:00 (Mei, Rin) | 10:41, 12:31 (Kenji, Rin) |

- **Pays back on a rising curve:** Katana 5 min, Crafter 32, Longsword 36, Falchion 39, Haru 63, Gladius 78, Zanbatō 170, Etcher 234, Mei 239.
- **About an hour long:** `fit()` assumes every sword sells the moment it's made, so with walk-ins the plan runs 47 minutes past its 8 h (1 h 17 for the cheapest-first player). A build re-fits with customers in.
- **First-draft goal prices** (the fit, before that fix): Crafter 16,000, Longsword 28,000, Haru 47,000, Stocker 62,000, Falchion 78,000, Mei 260,000, Promoter 170,000, Gladius 230,000, Cashier 430,000, Etcher 290,000, Zanbatō 270,000. Cheap side buys in the crafter stage: Faster Heating III 7,600, Furnace 2 1,600, Anvil 2 4,500.
- **The save-for-the-goal stretch stays** while a goal is the last 40% of its stage and only one stage is open: 11 stretches of 15–40 minutes with two or fewer things on offer (today: 6, filled in the middle with buys that don't do anything yet). Opening two stages at once (a stage's pads appear when the goal *before last* is bought) cuts it to 4, but a cheapest-first player then buys ahead and runs about 45 minutes behind at the crafter. Question 3.

## Decisions this touches

- "The goal order stays: Katana, Longsword, Sword Crafter, Falchion, Stocker, Shop Promoter, Gladius, Cashier, Sword Etcher, then the Zanbatō and the crew" ([[Design/Decisions Log#Economy pass 2 direction — 2026-10-27|Economy pass 2]]): the crafter moves before the Longsword, and Haru and Mei move into the spine.
- "Each stage's pads and cart levels wait for the previous goal": replaced by physical gates plus the stage rule for goals, or two stages open (question 3).
- "Up to three crafters work at once … Haru with Anvil 3 (9 h 50), Mei with Anvil 4 (11 h 20)": kept, moved to 3 h and 6 h.
- Kept: the 8 h length, the Katana at 20 min, the tutorial's prices, Furnace 2 after Faster Heating III, the crafter trained on hire, Ore Slots always the next one, shop-floor pads out of the stage gates, the Zanbatō as the late goal.

## Questions for Allen

1. **Order:** move the Sword Crafter to about 1 h (before the Longsword) and Haru and Mei to about 3 h and 6 h? *Decided: yes, all three.*
2. **Training:** should buying a new sword also teach the working crafters (training stays for switching), or keep training as its own buy? *Decided: a new sword teaches the crew.*
3. **Gates:** one stage open as today (plan-accurate, a 15–40 minute save at the end of each stage), two stages open (fewer saves, cheapest-first players run a bit behind), or one stage plus a pinned next goal with its progress ("Falchion · 7,547 / 61,000") so the save reads as a goal? *Decided: two stages open.*
4. **Ore Slots 5–6:** price them by what they do (cheap, so the first merge comes mid-game), or give them a felt effect of their own? *Decided: the first merge about 2 h in; merges keep ×1.5.*
5. **The goal share:** keep a goal at 40% of its stage, or 25% (shorter saves, more small buys)? Allen kept 40% over 25% on 2026-10-27; the question is back because of the saves. *Dropped: no saving stretch is left with two stages open, so 40% stays.*

## Allen's answers (walkthrough, 2026-10-28)

"Yes, all three" (the order), "New sword teaches crew", "Two stages open", "first merge about 2 hours in" (typed), then "x1.5, as today" (merges) and "Crew window, as today" (hiring Haru and Mei). Recorded with Claude's defaults in [[Design/Decisions Log#Upgrade order — 2026-10-28]].

- **What the answers change:** Ore Slots 5–6 at about 10,000 and 22,000 so the first merge lands at 2 h; the next Ore Slot is always on offer, and with two stages open the model finds no stretch with two or fewer things on offer before the Zanbatō (6 today). The fifth question (the goal share) was dropped for that reason.
- **Merges at ×1.5:** 2:03, 2:51, 4:05, 4:30, 5:07, 6:16, 8:08 … 11 by 16 h, luck ×6.5. Each adds luck and income faster than the re-buy grows (×2 gave 7 merges, ×3 gave 5). Lucky Ore's +0.5 is worth about 45 minutes of merging by mid-game.
- Modelled (first draft, casual Rare+ picker buying the cheapest pad on offer): Katana 0:23, Sword Crafter 0:56, Longsword 1:41, Haru 2:22, Stocker 3:17, Falchion 3:29, Shop Promoter 4:52, Mei 5:39, Gladius 6:51, Sword Etcher 7:21, Cashier 7:37, Zanbatō 7:52, Kenji 10:51, Rin 13:22; merges at 2:03, 2:51, 4:05, 4:30, 5:07, 6:16 … (11 by 16 h, luck ×6.5); no stretch with two or fewer things on offer before the Zanbatō.
- **First-draft prices** (fit with customers in, scaled ×0.64 to land the Zanbatō at 8 h for a cheapest-first player): Katana 1,400, Sword Crafter 9,600, Longsword 17,000, Haru 26,000, Stocker 35,000, Falchion 44,000, Shop Promoter 84,000, Mei 150,000, Gladius 200,000, Cashier 230,000, Sword Etcher 180,000, Zanbatō 150,000. The build re-fits them so goals only rise and the Katana stays near 20 min.

## Built (2026-10-28, not played)

Allen: "Build it". [[Sessions/2026-10-28#Upgrade order built]] · [[Design/Decisions Log#Upgrade order built — 2026-10-28]]

| Goal | Price | Comes with it |
|---|---|---|
| Katana | 1,300 | Wall Rack 2 53, Polishing Station 100, Finished Sword Rack 140, Display Table 1 220, Ingot Rack 230, Faster Heating I 290, Ore Slot 3 280 |
| Sword Crafter | 10,000 | Etching Table 790, Faster Heating II 1,500, Ore Slot 4 2,000, Ingot Rack 2 1,000, Faster Heating III 2,600, Furnace 2 1,400, Anvil 2 3,400 |
| Longsword | 17,000 | Finished Sword Rack 2 1,300, Rickshaw Bay 1 1,100, Delivery Cart 3,100, Capacity 1 1,500, Speed 1 2,400, Ore Slots 5–6 9,800 / 20,000 |
| Haru (Anvil 3) | 23,000 | Upgraded Store 8,900, Wall Rack 3 3,200, Display Table 2 4,500, Anvil 3 14,000 |
| Stocker | 36,000 | Rickshaw Bay 2 22,000, Capacity 2 25,000 |
| Falchion | 50,000 | Wall Rack 4 15,000, Display Table 3 21,000, Speed 2 40,000 |
| Mei (Anvil 4) | 70,000 | Anvil 4 22,000 |
| Shop Promoter | 130,000 | Display Table 4 23,000, Capacity 3 64,000, Rickshaw Bay 3 76,000 |
| Gladius | 150,000 | Speed 3 55,000 |
| Cashier | 210,000 | Speed 4 76,000 |
| Sword Etcher | 270,000 | Etching Table 2 120,000 |
| Zanbatō | 300,000 | Big Sword Stand 36,000 |
| Kenji, Rin | 460,000, 710,000 | (crew window, replacing the weakest) |

- **Modelled** (`python economy_model.py`, casual picker, cheapest first): Katana 0:19, Sword Crafter 1:04, Longsword 1:48, Haru 2:35, Stocker 3:11, Falchion 4:01, Mei 4:55, Shop Promoter 5:46, Gladius 6:09, Cashier 6:58, Sword Etcher 7:54, Zanbatō 8:15, Kenji 9:25, Rin 11:07; merges at 1:59, 2:53, 3:39 … (11 by 16 h); never two or fewer things on offer before the Zanbatō; longest gap between buys 21 min. Pays for itself: Katana 3 min, Crafter 19, Longsword 21, Falchion 24, Haru 28, Gladius 53, Mei 58, Zanbatō 143, Etcher 218.
- **Other players:** relaxed (×1.5) Zanbatō 9:16, focused 5:52, a player who never picks 12:48.
- **Not built:** locked pads showing "After Longsword" on the floor (rule 3's second half; not asked in the walkthrough).

Related: [[Design/Economy Pass 2]] · [[Archive/Design/Progression and Economy Review — 2026-10-27]] · [[Design/Tycoon Upgrades]] · [[Design/Workshop Growth]] · [[Development/Roadmap]]

---
title: Economy and Progression Review — 2026-11-08
status: review — nothing changed in Studio; every recommendation waits for Allen's OK
type: design
updated: 2026-11-08
tags: [design, economy, pacing, gems, robux, staff, sim, create-swords]
---

# Economy and Progression Review — 2026-11-08

Allen: "Evaluate our game economy and progression". This review covers today's changes too: the daily ladder, the 250-gem Starter Pack, the Cashier at 15 s, three of each staff role and "More [x%]". **Nothing was changed in the place.**

## How it was checked

- **Main sim run.** `econ-review-2026-11-08`: 1,800 players. That is 6 types × free / starter / all passes × 100 players, 20 h each, seed 1 ([[Development/Sim Runs/econ-review-2026-11-08]]).
- **Starter Pack run.** `starter-coins-2026-11-08`: 800 players, casual and efficient, Starter Pack holders with 0 / 5,000 / 10,000 / 25,000 coins, 12 h, seed 1 ([[Development/Sim Runs/starter-coins-2026-11-08]]).
- **Export check.** `balance.json` is the 2026-11-07 14:19 export, patched by hand today (daily, Starter Pack, Cashier). I hashed the live place's sources in Edit, read-only: 23 of 24 match. `EmployeeService` differs only by the Neutral Smile head (`CREW_HEAD`), which changes no number.
- **Not in the sim.** The 2nd and 3rd staff members (the sim keeps the first of each role); crew levels bought with gems; bought weather (not built). The staff numbers below come from the live `Shared/Employees` (lines 235–252).
- **What the sim assumes.** A day is 1 h of play, so 20 h is 20 daily rewards. Starter Pack holders get the pack at minute 0; in the game it shows only after the tutorial, about 5 min in.
- **Buy order checked.** A casual player buys the cheap pads first and the Sword Crafter at 28 min. A Starter Pack holder buys 19 pads in the first minute. An efficient player heads for the swords.

## Ranked findings

### 1. The catalogue ends at ~10 h for engaged players; after that only the ore merge is left

**Evidence (sim, free players, medians of 100 each):**

| | casual | efficient | automator | rusher | grinder | manager |
|---|---|---|---|---|---|---|
| Zanbatō | 11:01 | 4:59 | 9:48 | 4:26 | 4:44 | 3:35 |
| Seraph (the last sword) | 3 of 100 by 20 h | 10:55 | 16:28 | 8:43 | 11:49 | 10:17 |
| Buys from 4 h to 20 h: other / Ore Slot and merge | 48 / 54 | 41 / 81 | 54 / 84 | 36 / 90 | 32 / 77 | 33 / 83 |
| Buys after the Seraph that aren't Ore Slots | — | 1 | 0 | 8 | 2 | 1 |
| Waits over 15 min between buys (20 h) | 31 | 18 | 19 | 24 | 20 | 16 |
| Longest wait | 32 min | 83 min | 42 min | 95 min | 82 min | 89 min |
| Income at 20 h (coins a min) | 35,618 | 89,099 | 95,813 | 88,896 | 88,789 | 127,008 |

- **The Seraph is aimed at 20 h** (Decisions Log). Engaged players reach it at 8:43–11:49, then spend 8–11 h buying only Ore Slots 2–6 and merges: 16–17 merges by 20 h.
- **From 4 h on, 60–73% of all buys are the Ore Slot loop.**
- **A casual player is the opposite case.** They earn about a third as much (35,618 a minute at 20 h), reach the Zanbatō at 11 h, and 97 of 100 never see the Seraph in 20 h.
- **This matches the 2026-11-02 Upgrade Time Model:** "content, not prices, is the late-game gap". Repricing can't help both players: dearer late swords lengthen the casual player's wait, and cheaper ones end the engaged player's game sooner.

**Recommendation.** Make the Legendary Commissions ([[Design/Major Updates Plan — 2026-11-07]], proposal 2: about 38 goals across 4–20 h) the next content build, and keep today's prices until then.
- **Target to measure it by:** an efficient player makes at least 20 buys after the Seraph that aren't Ore Slots (today 1).
- **The open question still stands:** an earlier Seraph target (~10 h, what today's content fits), or ~40 new buys for 4–20 h. The sim says engaged players already behave like the 10 h target.

### 2. A 2nd or 3rd staff member arrives weaker than the one they replace

A new hire starts at Lv. 1. Only the one at work gains jobs, and staff take 25 / 75 / 175 / 375 jobs to reach Lv. 2–5 (`LEVEL_AT` × `STAFF_SCALE` 2.5). Lv. 1 of the new member against Lv. 5 of the first (`Shared/Employees` 235–252, `PROMOTER_CROWD` and `carry` by level):

| Role | 1★ at Lv. 5 | 2★ at Lv. 1 | 3★ at Lv. 1 | 3★ at Lv. 5 | Price of 2★ / 3★ |
|---|---|---|---|---|---|
| Stocker | Sora walk 12, carries 4 | Yuto walk 10, carries 2 | Ren walk 12, carries 2 | walk 16, carries 4 | 36,000 + 15 / 150,000 + 40 |
| Cashier | Aki answers in 5 s | Hana 12 s | Daichi 9 s | 3 s | 150,000 + 15 / 600,000 + 40 |
| Promoter | Kaito wait ×0.65, +3 in the shop | Mio ×0.75, +1 | Riku ×0.70, +1 | ×0.55, +3 | 120,000 + 15 / 480,000 + 40 |
| Etcher | Yume 5 s | Sen 8 s | Kohana 6 s | 3 s | 800,000 + 15 / 3,200,000 + 40 |

- **Every new hire makes the shop worse on the day it's bought.** The Promoter is the worst case: Riku lets 2 fewer customers in at once until his 75th job. To get back to even, the player puts him to work and loses customers meanwhile, or pays up to 380 gems to level him (20 / 55 / 105 / 200).
- **This breaks what Allen asked for:** "2 more NPCs with upgraded stats from the previous". The 10-27 review found the same trap with crafters.
- **The prices are fine as late buys.** For an engaged player, Ren is 5–7 min of income at 8 h and Kohana 25–36 min at 20 h. For a casual player, Kohana is about 90 min at 20 h. These are 8 new buys in the trough.

**Declined (2026-11-08, Allen: "Leave as is"):** a maxed first member being better than a fresh 2nd or 3rd is intended; each tier tops out higher. The follow-up (carry and the Promoter's crowd never below the best reached) was declined too. [[Sessions/2026-11-08#Staff tiers stay as built]]

**Recommendation (declined).** A new member starts with the job count of the role's member at work.
- **Where:** in `EmployeeService`'s `hireStaff`, the new record's `count` = the working record's `count`.
- **What it does:** at hire they're at once a step above the one they replace, for example Ren at Lv. 5 walks 16 and carries 4.
- **Sim:** mirror the three members in `Development/sim` in the same pass, so the late game counts them.

### 3. The Starter Pack's 25,000 coins buy the first half hour in one tap; its gems are what speed the game

**Evidence (`starter-coins-2026-11-08`, 100 each, medians):**

| Starter coins | casual: buys in the first 2 min | casual: Sword Crafter | casual: Zanbatō | efficient: buys in the first 2 min | efficient: Sword Crafter | efficient: Zanbatō |
|---|---|---|---|---|---|---|
| 0 (gems only) | 0 | 0:32 | 9:52 | 1 | 0:17 | 4:11 |
| 5,000 | 10 | 0:26 | 9:47 | 7 | 0:13 | 4:07 |
| 10,000 | 13 | 0:22 | 9:48 | 12 | 0:00 | 4:21 |
| 25,000 (today) | 19 | 0:01 | 9:36 | 18 | 0:00 | 4:09 |

- **Without the pack**, a casual player reaches the Zanbatō at 11:01 (main run, same seeds and flags).
- **The 250 gems do almost all of the speed-up** (11:01 → 9:52, through the Gem Shop's customer upgrades).
- **The coins add 16 min more**, but at 25,000 they buy the first 19 pads at once. That includes the Sword Crafter, which is the first hour's goal (Allen: the hire at ~15 min, as Create Pottery's Apprentice). Those are the best-paced buys in the game, and they'd go in one tap.

**Built (2026-11-08, Allen: "Starter coins 5,000"):** [[Sessions/2026-11-08#Starter Pack coins 5,000]].

**Recommendation.** `Shared/Store` `STARTER_COINS` 25,000 → **5,000**, keeping the 250 gems.
- **What 5,000 still buys:** 10 pads at once, the Crafter left as a goal at ~26 min. The live tag would read about 2.4× VALUE (224.5 + 16.7 R$ against 99).
- **Alternative:** keep 25,000 but show the pack only once the Sword Crafter is hired.

### 4. Engaged players run out of gem buys at 12–19 h; casual players never finish the Gem Shop

**Evidence (free, 20 h):**

| | casual | efficient | automator | rusher | grinder | manager |
|---|---|---|---|---|---|---|
| Gems in: daily / cart / mail | 370 / 354 / 2 | 370 / 348 / 655 | 370 / 357 / 751 | 370 / 266 / 560 | 370 / 405 / 932 | 370 / 714 / 354 |
| Gem Shop levels (of 20) | 15 | 20, done 16:42 | 20, 16:39 | 20, 19:00 (67 of 100) | 20, 12:06 | 20, 14:00 |
| Gems left at 20 h | 67 | 227 | 342 | 78 | 573 | 297 |

- **Spent in the sim:** the Gem Shop (990) and the crafter hires (155).
- **Not counted:**
  - the new staff (4 × (15 + 40) = 220);
  - crew levels bought with gems (up to 380 a member, 17 members);
  - weather for 60 gems (decided 2026-10-27, not built).
- **The daily reward is half of a casual player's gems** (370 of 731). The new ladder is 150 a week (was 90), about Create Pottery's 156.
- **No price is wrong here.** Engaged players simply have nothing left to spend gems on from about 15 h.

**Recommendation.** Build bought weather for **60 gems** (Monetization Plan §3, already decided). It's the only sink that never runs out. Keep the Gem Shop at 990.

### 5. The daily reward's coin days shrink to 5–13 min of income after the first week

`coinRate` is lifetime coins ÷ minutes played. Income keeps rising, so that average lags behind it. Sim medians, claim day → the gift as minutes of that hour's income:

| | Day 2 (15 min) | Day 5 (30 min) | Day 9 (15) | Day 12 (30) | Day 16 (15) | Day 19 (30) |
|---|---|---|---|---|---|---|
| casual | 15 | 19 | 7 | 13 | 6 | 7 |
| efficient | 15 | 13 | 6 | 9 | 6 | 12 |

**Recommendation.** `GemUpgrades.coinRate` = income over the last 15 min played (the coin packs' rule from 2026-10-28), floor 50. Then "15 min of coins" means what it says.

### 6. The 2★ and 3★ staff gains are small for 3× and 12× the price

Lv. 5 to Lv. 5:
- Promoter ×0.65 → 0.60 → 0.55 (walk-ins +8%, then +9%);
- Cashier 5 → 4 → 3 s (offers last 45 s);
- Stocker walk 12 → 14 → 16;
- Etcher 5 → 4 → 3 s.

Only the Promoter's step reaches the economy, and only while the shop is the bottleneck (from about 4 h).

**Recommendation (Allen's call).** Give each star one step the player can see.
- **Example:** the Stocker's carry +1 per star: Yuto 3 / 3 / 4 / 4 / 5, Ren 4 / 4 / 5 / 5 / 6 (`Employees.carry` by member).
- **Keep the Promoter's crowd cap of 8** (Allen 2026-11-07).

### 7. Reputation has no effect after Rank 5, and its two effects are hard to see

- **What earns it:** +1 a sale, +3 an order (`Shared/Reputation`; thresholds 0 / 5 / 15 / 30 / 50 / 80 / 120 / 175).
- **What it gives (live `Shared/Orders` 183, 186):**
  - from Rank 4, a twist order asks for Rare 35% of the time (instead of Uncommon);
  - from Rank 5, +1 gem an order.
- **What it doesn't do:** ranks 6–8 do nothing, and the mail's slots come from More Clients, not from rank. The rank shows only in the Deliveries window.

**Recommendation.** Let Ranks 6–8 each open a Legendary Commission letter chain (finding 1). Otherwise drop ranks 6–8 from `Reputation.THRESHOLDS`.

## Robux packs and passes

- **"Anyone can earn everything" holds.** All 600 free players reach the Zanbatō in 20 h. Casual players reach the Seraph past 20 h.
- **All passes roughly halve the times.** Efficient Seraph 10:55 → 5:28, casual never → 10:56, manager Zanbatō 3:35 → 1:54. 50% More Coins is most of it (Monetization Plan §1).
- **Gem packs per R$:**

| Pack | Gems per R$ |
|---|---|
| 7 gems | 0.78 |
| 15 gems | 0.79 |
| 80 gems | 0.81 |
| 200 gems (the decoy, Allen's 2026-11-02 pick) | 0.50 |
| 500 gems | 1.11 |
| Starter Pack | 2.53 |

- **Coin packs per R$:** 89 (800 coins) up to 300 (300,000 coins). They are fixed amounts, so 300,000 is several hours of a first-day player's income and 8 min at 20 h. The short-of-coins offer late can only fit the 100,000 and 300,000 packs. No change suggested.
- **Small: two Rikus** (fixed 2026-11-08: the Promoter is Haruto). The 3★ Promoter is named Riku, and so is the courier who pulls the cart and sends mail (`Shared.Senders`). One wants another name.
- **Still open from before:** VIP at 299 against 50% More Coins at 199; Lucky Ore sold on the Store tab; managed pricing waiting on the Creator Hub step.

## What's healthy

- **The first hour.**
  - Sword Crafter at 0:16–0:37 by type; engaged players are near the 15 min target, and casual players buy cheaper pads first, which Allen accepted.
  - Katana at 0:07–0:22; the automator is the slow one at 0:53.
  - A casual player has 2 waits over 15 min in the first 4 h (31 in 20 h).
- **Today's changes are mirrored and cost nothing in pace.** The daily ladder and the Cashier are in the sim. The Cashier is hired at 6:00–9:19 and sells any offer at its default.
- **"More [x%]"** shows the real raise odds; no lowball offers come back.

## Compared with Create Pottery ("the clay game")

| | Create Pottery | Sell Swords! |
|---|---|---|
| First helper | Apprentice $900 at 14:01, 55% of 15 min income | Sword Crafter 2,000 at 0:16–0:37 |
| Price steps | "every purchase empties the wallet", ×2.25–4 a level | first ring 30–2,000; the sword chain ×1.07–6 a step (Cutlass → Falchion ×1.08, Wakizashi → Machete ×6) |
| Daily week | 6 / 14 / 16 / 18 / 20 / 22 / 60 = 156 gems | 10 / 15 min coins / 15 / 20 / 30 min coins / 25 / 80 = 150 gems + 2 coin days |
| First gem upgrades | 2–15 gems | 5–20 gems; 990 for all 20 levels |
| Top crew | 5★ 1M coins + 1,000 gems | Taru 710,000 + 80; Kohana 3.2M + 40 |
| Offers | +10% to +139%, 60 s | 1.15–1.5× regulars, 2–3.5× VIPs, 45 s; More [50%] |
| Auto roll | 149 R$ | 149 R$ |
| First paid bundle | "Support the Game! 300 Coins & 50 Gems" | 250 gems + 25,000 coins, 99 R$ |
| Luck | Lucky Clay ×2 Rare+, odds panel | Lucky Ore +0.5 luck, odds panel |

- **Where we differ the most:**
  - Pottery's first paid bundle is small. Ours buys 19 pads (finding 3).
  - Pottery's top crew costs 1,000 gems. Ours costs 40–80, which is why our gems pile up late (finding 4).
- **Not measured in our notes:** how long Pottery's content lasts, and its retention ([[Design/Pottery Tutorial Review]]). There's no benchmark for the 10–20 h gap.

## For Allen: what each OK would build

1. **Legendary Commissions as the next update** (finding 1): content, not prices.
2. ~~New staff start at the worker's job count~~ (finding 2). **Declined 2026-11-08: leave as is.**
3. **`STARTER_COINS` 5,000** (finding 3). **Built 2026-11-08.**
4. **Weather for 60 gems** (finding 4).
5. **`coinRate` from the last 15 min** (finding 5).
6. **Stocker carry +1 per star** (finding 6).
7. **Ranks 6–8 open commission chains** (finding 7).
8. **Rename the 3★ Promoter** (Riku clash). **Built 2026-11-08: Haruto.**

Related: [[Archive/Design/Progression and Economy Review — 2026-10-27]] · [[Design/Economy Review — 2026-10-29]] · [[Design/Upgrade Time Model — 2026-11-02]] · [[Design/Monetization Plan]] · [[Design/Tycoon Upgrades]] · [[Design/Pottery Playthrough 2026-11-02]] · [[Sessions/2026-11-08#Economy and progression review]]

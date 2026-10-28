---
title: Economy Pass 2
status: built 2026-10-27 in Edit, not played
type: design
updated: 2026-10-27
tags: [economy, progression, pricing, upgrades, ore, crew, create-swords]
---

# Economy Pass 2

Allen, 2026-10-27, after [[Design/Progression and Economy Review — 2026-10-27|the economy review]]: "Keep unlimited free spins. Plan the economy pass around players picking rare ore, plus a scrap bin for leftover ingots." Then: "Also plan the economy based around the upgrades, it should take a meaningful amount of time to get the next sword and to also get an employee." The same day he walked through the plan and answered each part; his answers are in each section and in the [[Design/Decisions Log#Economy pass 2 direction — 2026-10-27|Decisions Log]].

**Built 2026-10-27 in Edit, not played** (Allen: "Build Economy Pass 2 as decided"; [[Sessions/2026-10-27#Economy pass 2 built]], [[Development/Code Map#Economy pass 2 (2026-10-27)]]). Two things differ from the plan below: Anvil 4 comes after Anvil 3, not after Haru (pads can only wait for upgrades, not crew hires), and a save from before keeps its crafters but not where they work (the crew window's Station page puts them back). Every number here comes from `Development/economy_model.py` (`python economy_model.py`): its picking player, `STAGES` and `fit()`. Seconds per sword, per pull and how often a Zanbatō sells are still estimates (§8). Pass 1 was [[Sessions/2026-10-23#Economy pass 1]].

## The short version

- **Picking is the intended play.** Spins stay free and unlimited, and prices assume a player who keeps pulling until a Rare or better ore shows: about twice a non-picker's income.
- **Progress is a spine of goals,** each the next sword or the next employee: Katana 20 min, Longsword 1 h 20, Sword Crafter 2 h 05, Falchion 3 h 10, Stocker 3 h 55, Shop Promoter 4 h 40, Gladius 5 h 45, Cashier 6 h 55, Sword Etcher 8 h, Zanbatō 8 h 45, a second crafter (Haru, Anvil 3) 9 h 50, a third (Mei, Anvil 4) 11 h 20, Rin 13 h 10, for a casual picker.
- **A stage's pads and cart levels appear once the stage before ends on its goal,** so a player who buys whatever's cheapest still keeps to the plan.
- **The Sword Crafter comes trained on your best sword.** Up to three crafters work at once (Anvils 2–4); a crafter you buy can replace a working one.
- **Pulling again replaces the ore left on the lid.** No scrap bin and no pay: anything you carry can be dragged onto a trash icon in the bag.
- **The tutorial teaches the pick:** its first roll asks you to pull again before you collect.

## 1. Picking is the play

Allen: "Players should be able to spin the ores as many times as they want" (Refinements 3, 2026-10-23), "remove this limit" (2026-10-24), and now "keep unlimited free spins". **Prices are built for a Rare+ picker** (Allen picked it over pricing for Epic+ hunters, which would have put a Rare+ picker's Gladius at 5 h 30 instead of 4 h on the old 5 h 30 plan, and a non-picker's at 11 h 40).

| Ore slots | Pulling a Rare+ ore takes | A casual picker earns |
|---|---|---|
| 1 | 33 s | ×2.0 a non-picker |
| 2 | 17 s | ×2.2 |
| 4 | 8 s | ×2.4 |
| 6 | 6 s | ×2.4 |

5 s a pull with the hold, not timed yet.

- **Ore Slots become real income upgrades:** each one cuts the pulling a sword needs. A merge adds luck (more Epics and Legendaries within Rare+) but puts you back on one slot, so it's a trade.
- **The ceiling:** a focused player who keeps only Epic+ at six slots earns ×3.6 a non-picker, about 40% more than the Rare+ baseline, and finishes about 30% sooner. Knowledge and patience pay; that's fine.
- **The model assumes the picker also racks Rare+ ingots for the crafters** (their pulls come out of the player's time). Racking commons for them instead earns less.
- Uncommon+ and Rare+ mail orders get easy, and the cart already pays 0.8× whatever the swords are worth. The thrill moves up to Epic, Legendary, Secret and the collection book.

## 2. The spine: the next sword, the next employee

Allen kept this order, set **8 h to today's last floor pad** for a casual picker (the Katana stays at 20 min; everything after it stretches), and kept the goal at **40% of its stage**: the small buys before it share the first 60% by today's relative prices (so Furnace 2 stays cheap next to Faster Heating III), none taking more than three quarters of the goal's share, so the goal is always the dearest buy in its stage. The model rounds every price to two figures. Prices: today → proposed.

| Stage ends on | At | Goal price | Small buys on the way |
|---|---|---|---|
| Katana Sword | 20 min | 400 → 2,000 | Wall Sword Rack 2 150 → 68 · Polishing Station 250 → 210 · Finished Sword Rack 250 → 270 · Display Table 1 250 → 370 · Ingot Rack 200 → 320 · Faster Heating I 300 → 490 · Ore Slot 3 300 → 520 |
| Longsword | 1 h 20 | 1,000 → 22,000 | Etching Table 800 → 1,600 · Ore Slot 4 900 → 3,900 · Faster Heating II 900 → 4,300 · Rickshaw Bay 1 500 → 2,400 · Ingot Rack 2 500 → 2,400 · Finished Sword Rack 2 600 → 2,900 · Delivery Cart 1,200 → 5,700 · Cart Capacity 1 600 → 2,900 · Cart Speed 1 800 → 3,800 |
| Sword Crafter | 2 h 05 | 1,000 → 26,000 | Faster Heating III 2,500 → 18,000 · Furnace 2 500 → 4,000 · Anvil 2 1,500 → 12,000 |
| Falchion | 3 h 10 | 2,000 → 61,000 | Upgraded Store 1,500 → 18,000 · Rickshaw Bay 2 1,500 → 20,000 · Cart Capacity 2 1,500 → 20,000 · Cart Speed 2 1,600 → 21,000 |
| Stocker | 3 h 55 | 2,000 → 79,000 | Training: Falchion 4,000 → 37,000 · Display Table 2 600 → 6,800 · Wall Sword Rack 3 400 → 4,900 · Ore Slot 5 2,000 → 26,000 |
| Shop Promoter | 4 h 40 | 1,500 → 72,000 | Display Table 3 900 → 14,000 · Etching Table 2 2,500 → 39,000 · Cart Capacity 3 3,500 → 53,000 |
| Gladius | 5 h 45 | 3,500 → 120,000 | Wall Sword Rack 4 700 → 14,000 · Cart Speed 3 3,000 → 60,000 · Rickshaw Bay 3 4,000 → 87,000 |
| Cashier | 6 h 55 | 3,000 → 240,000 | Training: Gladius 6,000 → 110,000 · Display Table 4 1,300 → 42,000 |
| Sword Etcher | 8 h | 2,000 → 170,000 | Ore Slot 6 4,000 → 100,000 · Cart Speed 4 5,000 → 120,000 |
| Zanbatō | 8 h 45 | new → 200,000 | Big Sword Stand 2,500 → 85,000 |
| Haru, the second crafter | 9 h 50 | 2,500 → 370,000 | Anvil 3 (new) → 160,000 |
| Mei, the third crafter | 11 h 20 | 6,000 → 640,000 | Anvil 4 (new) → 250,000 |
| Rin | 13 h 10 | 25,000 → 1,100,000 | Kenji 12,000 → 420,000 |

Unchanged: the guide's Mailbox 15, Wakizashi Sword 60 and Ore Slot 2 75 (Allen: "Keep them"), so the tutorial and its haggling lesson stay as they are, and training on the Tantō, Wakizashi, Katana and Longsword (200 / 600 / 1,500 / 2,500; optional, since the hire already trains him on your best sword). The crew window's gems stay as today. The **Upgraded Store stays in the Falchion stage** (Allen picked it over the Longsword stage): it arrives when the crafter's swords start filling the shop.

- **Along the way** (casual picker): about 350 coins a minute at the Katana, rising to roughly 6,000 by the Etcher and 15,000 once three crafters and the Zanbatō are working. A purchase every 2–3 minutes in the first hour, every 10 minutes to 3 h, every 12–13 minutes to 5 h 30, then every 20–30.
- **The next sword** is 60 minutes after the Katana, then 110, 155 and 180 (the Zanbatō). **The next employee** comes 45–135 minutes after the last.
- **After Ore Slot 6,** merges re-buy the slots at ×1.5 a time.

**Who gets there when** (each buying the cheapest pad they can, with the gates):

| Player | Katana | Longsword | Sword Crafter | Gladius | Today's floor pads | Rin |
|---|---|---|---|---|---|---|
| Focused picker (50 s a sword) | 8 min | 26 min | 59 min | 3 h 36 | 6 h 02 | 10 h 07 |
| Casual picker (the plan) | 20 min | 1 h 19 | 2 h 05 | 5 h 45 | 8 h 14 | 13 h 06 |
| Relaxed picker (casual ×1.5) | 31 min | 1 h 59 | 3 h 07 | 7 h 23 | 10 h 17 | 15 h 52 |
| Casual, never picks | 33 min | 2 h 51 | 4 h 37 | 12 h 15 | 18 h 10 | 28 h 55 |

"Today's floor pads" ends on the Big Sword Stand, which now comes with the Zanbatō.

## 3. Gates

Allen: "Pads and cart levels."

- **Pads:** each stage's pads get the previous stage's goal added to their `after` in `Shared.Upgrades` (TycoonService already takes a list, as Anvil 2's). The Katana stage needs none.
- **Cart levels:** Capacity 1 and Speed 1 come with the Delivery Cart, Capacity 2 and Speed 2 after the Sword Crafter, Capacity 3 after the Stocker, Speed 3 after the Shop Promoter, Speed 4 after the Cashier. A level that isn't open shows "After Sword Crafter" (or the like) where its Buy would be.
- **Training and the crew window need none:** a blueprint and the Sword Crafter already gate training, and the crew's prices only rise.
- **Why:** on the 8 h plan, a player who buys whatever's cheapest would get the Longsword at 4 h 12 with no gates, and at 2 h 05 with the pads gated but not the cart levels. Gated, they land within a few minutes of the plan, and each goal makes its stage's pads appear together.

## 4. The crew: trained on hire, three at work

- **The Sword Crafter comes trained on your best sword** (Allen: "Trained on hire"), so he works the moment he's hired. Training is then for later swords (Falchion, Gladius) or for switching what an anvil makes.
- **Up to three crafters work at once** (Allen: "Should be at most 3 active sword crafter at a time. different crafters bought can replace active ones if players want. That means 3 anvils can exist"): Taise at Anvil 2, then Anvil 3 and Anvil 4 as pads, each beside your own anvil. Read as three crafter anvils (Anvils 2–4) besides yours. Every crafter you hire is kept; the crew window picks which three work, and a new hire can replace a working one. Each still levels on its own from Lv. 1, so a new hire at a new anvil adds swords at once, and one that replaces a crafter pays off as he levels.
- **The plan's order:** Haru with Anvil 3 (9 h 50), Mei with Anvil 4 (11 h 20), then Kenji and Rin as replacements for the weakest (Rin, 3★, last at 13 h 10). Replaces Refinements 2's "One at Anvil 2".
- **To watch when it's built:** three crafters empty the 12-slot Ingot Rack in about four minutes and fill the Finished Sword Rack about as fast; the Stocker, the racks and the shop's customer upgrades (Better Advertising, More Clients, Rickshaw Bays, the Promoter) start to matter here, as the review hoped.

## 5. Ore, the bag and the tutorial

- **Pulling again replaces the lid** (Allen: "just spin new ones, existing ones are replaced"). The ore you collected (E) is in your hands; anything still on the lid when you pull again is gone, so leftovers never become Tools or save entries. That includes a Legendary or a metal you've never collected (NEW) if you don't take it first. A merge still puts the waiting ore in your hands, as today. `ForgeService.collectWaiting` is the one place that changes.
- **No scrap bin, no pay** (Allen: "no scrap bin", scrapping pays "Nothing").
- **A trash icon in the bag** (Allen: "opening inventory, there should be a trash icon that allows you to trash it"): drag a stack onto it, the way you drag onto the bag today, and the whole stack is gone (Iron 12x, all twelve). Ingots, blades and swords can all be trashed (Allen: "Ingots and swords"), and it never asks first (Allen: "Never").
- **The tutorial teaches the pick** (Allen: "Inside the tutorial"): its first roll asks you to pull again before you collect. Claude's default for the build: the tutorial's first pull always brings a Common and the second an Uncommon, so the lesson lands and the first sale (about 64 coins) still leaves the Wakizashi a sale away, keeping the haggling lesson. A player who never picks still gets everything, about twice as slowly.

## 6. The Zanbatō

Allen: "Sell the Zanbatō." It's the seventh sword: a pad after the Gladius and the Big Sword Stand, at 8 h 45, with the stand (85,000) in its stage. It's yours to make (base 1,000, about 3.6× a Gladius); crafters aren't trained on it, since the stand holds one. The model guesses one sells about every third sword you make (`ZANBATO_EVERY`); its hilt is still the katana's stand-in.

## 7. Build order, once approved

1. **Prices and gates:** `Shared.Upgrades` (prices, `after`, Anvil 3, Anvil 4 and the Zanbatō's pad), `Shared.Deliveries` (Capacity and Speed prices and the goal that opens each level) with `DeliveryService` and `DeliveryController`, `Shared.Employees` (training for the Falchion and Gladius, the crew's prices).
2. **The crew:** `EmployeeService` trains the Sword Crafter on your best sword when hired and runs up to three crafters, one per bought crafter anvil; the crew window chooses which three work.
3. **Ore and the bag:** `ForgeService.collectWaiting` replaces the lid on a pull; the `Hotbar` bag gets the trash icon (and a server remote that removes the stack).
4. **The tutorial step** in `Guide`.
5. **The vault:** GDD, [[Design/Tycoon Upgrades]], Code Map and Decisions Log; then rerun the model with the playtest's timings and adjust.

## 8. To time in the next playtest

A lever pull (hold and show) and the pulls to a Rare+ with one and four slots; a casual sword from roll to sale, with and without polish and etch; coins at 20 and 80 minutes; how often a displayed Zanbatō sells. The model's seconds move with them, and the prices with the model.

## 9. Customer rate

Allen: "It seems like customers come in very frequently and make an offer very frequently as well which would negate the point of having gems to upgrade shops customer rates and also special events that drive customer rates."

**Applied 2026-10-27, not played** (Allen: "Apply the recommended customer rate"): the recommendation below, as written. [[Sessions/2026-10-27#Customer rate applied]]

**How it works today** (`ShopService`): a walk-in is sent every 12–22 s at Better Advertising 0 (6–12 s at level 3), and the gap also shrinks 6% a reputation rank (×0.58 at rank 8) and by the Shop Promoter's perk (×0.8 → 0.65). Up to 2 customers at once (More Clients 3, 4; +1 with the Promoter; +1 a Rickshaw Bay). A walk-in only comes in while a sword is free on display, and every one makes an offer 2 s after reaching it; the first sale's customer comes at once.

**What that means** (casual picker on this plan's prices; the model's customer side, `run(customers=…)`):

| Time | Swords made a minute | Walk-ins a minute today |
|---|---|---|
| 15 min | 0.6 | 4.6 |
| 1 h | 0.5 | 4.9 |
| 2 h 30 | 1.2 | 6.1 |
| 5 h | 1.4 | 12.5 |
| 8 h | 1.4 | 16 |
| 12 h | 3.0 | 16 |

Walk-ins outnumber swords 5–11× all game, so no sword ever waits for a customer. Better Advertising, More Clients, the Rickshaw Bays, the Promoter's walk-ins, reputation's walk-ins and any event that brings customers change nothing; every sword gets its offer about 20 s after it goes up.

**Recommended:**

1. **A slower base:** a walk-in every 45–75 s at Better Advertising 0, then 36–64, 30–52 and 22–42 s (today's steps).
2. **Reputation stops shortening the gap.** It compounds with the rest (×1.72 by rank 8, about 3 h in) and swamps them: with it kept, a 45–75 s base still never leaves a sword waiting. Its ranks keep the better orders, and ranks 6–8 wait for special visitors (GDD §7, the review's VIP buyers).
3. **The tutorial keeps today's pace** (12–22 s, the first customer at once) until Ore Slot 2, so the first session stays brisk.
4. The Promoter's perk stays (Allen's numbers).

**Then** (same player): about 1.2 walk-ins a minute early against 0.5–0.6 swords, so a sword gets its offer about 40 s after it goes up; around the Sword Crafter (2 h to 4 h 40) walk-ins and swords run about even, the shelves start holding swords, and Better Advertising, the bays and a customer event pay; the Promoter tips it back to the forge until the crew grows; with three crafters (11 h on) the shop can't keep up (2.6 walk-ins against 3.2 swords) and the cart takes the rest at 0.8×. The plan barely moves (Rin at 13 h 16 instead of 13 h 06; 8% of swords by cart). Stopping Better Advertising at level 1 costs about 30 minutes by Rin and sends a quarter of the swords by cart, so gems buy something real. Keeping reputation's speed-up instead needs a base of about 85–115 s for the same late-game effect, which makes the first hour's offers take about a minute.

- **Customers at once:** where swords wait, walk-ins overlap, and a shop capped at two turns some away while you take your time over an offer, so More Clients and the bays start to count too (not in the model).
- **Events:** a customer event pays only while swords wait (around the crafter, and with three crafters); in between, a heating or forging event is the one that pays.

Related: [[Design/Progression and Economy Review — 2026-10-27]] · [[Design/Tycoon Upgrades]] · [[Design/Workshop Growth]] · [[Design/Core Loop Review]] · [[Development/Roadmap]]

---
title: Progression and Economy Review — 2026-10-27
status: review — questions and decisions waiting for Allen
type: design
updated: 2026-10-27
tags: [review, economy, progression, retention, tutorial, monetization, create-swords]
---

# Progression and Economy Review — 2026-10-27

Allen: "Review our game progression and economy. Are players advancing too slow, or too fast? Are players earning enough gold to reach the next upgrades quickly enough? Is there a sense of urgency for a player to juggle between their stations and managing the shop? Is the games core loop refined? Are there enough upgrades to grind for? Enough swords to create? Does our gold and gems you earn have a purpose for players to want to get more? What makes a player want to come back? What makes a player want to stay around longer? I know we don't have any random events yet or weather event mulitpliers yet, which we should have. We also don't have any game passes or developer products yet, which we should eventually have and implement into our shop. Is our tutorial simple enough to follow? … Bring up any questions or concerns you have."

Sources: the live constants and scripts, read (nothing changed) from the Studio place during Allen's Play session on 2026-10-27: `Shared.Upgrades`, `Blueprints`, `Hilts`, `Materials`, `Customers`, `Orders`, `Deliveries`, `GemUpgrades`, `Employees`, `Commissions`, `Reputation`; `SmithyCore.swordValue`, `ShopService`, `ForgeService`, `Guide`, `GemController`; the vault through [[Sessions/2026-10-26]]; and a pacing model built from those numbers ([[Sessions/2026-10-27#Progression and economy review]]). **Nothing here is measured.** Seconds per sword come from the one timed note ([[Sessions/2026-10-23#Urgency phase 1: cues, crew status, 45 s offers|urgency phase 1]]: an anvil visit ≈ 25 s, the walk to a customer 5.6 s, "about 35–60 s" a sword). [[Design/Alignment Review — 2026-10-23]] was the last pass; this one redoes its numbers after Refinements 3–5, the western blueprints, the crew and the mail rework. Proposals are not decisions until Allen picks them.

## The short version

- **Too fast after the first 15 minutes, then nothing left to buy.** Every floor pad, cart upgrade, training and crew hire (126,350 coins) is bought in about **1 hour** by a focused player, **2 h 20** by a casual one and **3 h 10** by a relaxed one. A purchase comes every 1–2½ minutes from the first minute to the last, and all but the last crew hire cost **1–8 minutes of the income you have when you buy them**, early or late. Afterwards 2,300–3,300 coins a minute go to the ore merge alone.
- **Free, unlimited ore is a loophole.** A pull costs nothing, the lever is ready again after the 3.6 s show and hands have no limit, so the best play is to keep pulling and forge only Rare+ ore: about **×1.6 income with one ore slot, ×2.3–3.3 with six**, and 6–19 unwanted ingots a sword piling up in the backpack and the save.
- **Gold and gems run out of purpose.** After the catalogue gold has only the merge; gems have 480 to spend in all (Gem Shop 325 since the same day's tutorial fix, crew 155).
- **The plates to spin exist; surprise and choice don't.** Offers need you at the customer within 45 s, and the furnace, racks, till, mail and cart all run on their own clocks. But every customer is alike, offers never go below value and nothing random happens, so the shop asks for no decisions. Polishing and etching your own swords lose coins a minute.
- **Coming back and staying:** the daily gem streak and two or three waiting orders are the only pulls back; no offline earnings, events, daily goals, badges or leaderboards. Nothing names the next goal after the katana letter, reputation is hidden in the Deliveries window, and the place has the anvil's clang, four cues and no music.
- **The tutorial is clear but long:** about 30 guided prompts and three full crafts (5–8 minutes) before "Workshop open!", with three small faults (§10; the first two fixed the same day).
- **Robux:** after a longer economy and real gem sinks. A 2× Coins pass on a 1–3 hour economy sells the content away; a paid Lucky Roll is a paid random item (odds before purchase, `PolicyService`).
- **Suggested order:** decide the ore rule and the target length → reprice and fix the three tutorial faults → a pinned next goal → VIP buyers with tastes → offline crew earnings → events → more blueprints and gem sinks → Robux.

## 1. The economy today

### What a sword is worth

`base × metal × 2.0 (100%) × 1.10 if polished × (1 + hilt + 0.06 seat + 0.15 etch)` (`SmithyCore.swordValue`). Hilts climb to the Gem Pommel's +40% at 15 swords made. The average rolled metal is ×1.57 (Common 59.9%, Uncommon 25, Rare 10, Epic 4, Legendary 1, Secret 0.1).

| Blueprint | Base | Pad | Step | Common, Gem hilt | Average metal, polished + etched |
|---|---|---|---|---|---|
| Tantō | 20 | start | | 58 | 111 |
| Wakizashi | 45 | 60 | ×2.25 | 131 | 250 |
| Katana | 110 | 400 | ×2.44 | 321 | 611 |
| Longsword | 160 | 1,000 | ×1.45 | 467 | 889 |
| Falchion | 220 | 2,000 | ×1.38 | 642 | 1,223 |
| Gladius | 280 | 3,500 | ×1.27 | 818 | 1,556 |

The western three are a flattening tail: each costs about twice the last and adds a third or less. Each still pays for itself within about a quarter of an hour.

### Where coins come from

- **Shop:** never below value since [[Sessions/2026-10-24#Refinement 4|Refinement 4]]. Farmer 100–110% (half the walk-ins), Adventurer 100–115% (×1.25 on a wakizashi), Knight 105–120% and ×1.25 on any sword of 95%+, which is every sword you forge. **The average first offer is about 113% of value** (121% on a wakizashi). Declining risks nothing: the sword stays up and the next customer comes 12–22 s later.
- **Mail orders:** 1.2× the sword sent, 1–3 gems, 3 reputation; one every 3–10 minutes while the inbox has room (2, or 3 from rank 3), also while away. An order picks any blueprint you know, so a gladius-maker still gets tantō orders worth about 70 coins.
- **Cart:** 0.8× the packed swords, 2–6 gems a trip, one reputation a sword, trips of 150 s down to 70 s.
- **Letters:** 120 (wakizashi) and 300 (katana), once each.

### Where coins go

| Branch | Coins |
|---|---|
| Staff and their stations (Anvil 2, crafter, stocker, cashier, Etching Table 2, etcher) | 12,000 |
| Customers (Rickshaw Bays 1–3, Shop Promoter) | 7,500 |
| Ore Slots 2–6 (×1.5 after each merge) | 7,275 |
| Blueprints | 6,960 |
| Shop holders and the Upgraded Store | 5,800 |
| Heating (Faster Heating I–III, Furnace 2) | 4,200 |
| Mailbox, Delivery Cart, Big Sword Stand | 3,715 |
| Storage racks, Polishing Station, Etching Table | 2,600 |
| **41 floor pads** | **50,050** |
| Cart Capacity and Speed (Deliveries window) | 16,000 |
| Crafter training, all six shapes | 14,800 |
| Four more crafters in the crew window (+155 gems) | 45,500 |
| **Everything** | **126,350** |

Gems: the Gem Shop's five levels cost 325 (Better Advertising 5/60/120 since the tutorial fix, 25/60/120 before; More Clients 40/100), the crew's crafters 155. Faucets: the daily streak (90 a week), orders (1–3 each), the cart (2–6 a trip).

## 2. Pace: too slow or too fast?

Three players, modelled from the numbers above: **focused** (50 s a sword, loads the next ingot while forging, skips polishing because it costs coins a minute, holds out for better offers), **casual** (75 s a sword, waits at the furnace, polishes and etches everything, takes the first offer, buys the cheapest pad in sight after the guide's three) and **relaxed** (the casual player at 1.5× the time). All follow the guide first; the crafter joins once bought.

| Bought at | Focused | Casual | Relaxed |
|---|---|---|---|
| Ore Slot 2 (tutorial done) | 3 min | 5 min | 7 min |
| Katana | 5 min | 19 min | 29 min |
| Longsword | 7 min | 35 min | 52 min |
| Gladius | 12 min | 1 h 38 | 2 h 24 |
| Sword Crafter | 17 min | 1 h 14 | 1 h 51 |
| Every floor pad | 46 min | 1 h 47 | 2 h 34 |
| Everything, crew included | 1 h 06 | 2 h 18 | 3 h 12 |
| Income afterwards | ~3,300 a min | ~2,650 a min | ~2,300 a min |

- **The first 15 minutes are right:** a purchase every 1–2 minutes, the guide leading, the first sale inside two minutes.
- **After that the gaps never grow.** The median gap between purchases stays 1–2½ minutes in every stretch, and each purchase costs 1–8 minutes of the player's own income when bought (Falchion 2.4–5.3, Gladius 3.0–6.7, Rickshaw Bay 3 2.5–6.0, Cart Speed 4 3.2–7.5). Only the last crew crafter (25,000) takes 16–37. The dearest pads cost 4,000, when a casual player's own swords already bring about 1,000 a minute.
- **A 1–3 hour first chapter works on Roblox only when another layer follows** (a rebirth, a second world). Here the only layer after is Merge Ore Slots: merges 1–6 take about an hour, then each costs ×1.5 more for less luck (average value +18%, +15%, +11%, +8% …).
- **At the GDD's 10–30 minute sessions, that's a few days of play for most players.**

**Proposal:** pick the length first (Alignment decision 7, still open). A starting target: the katana inside the first session, the crafter by the end of the first hour or two, the last floor pad after about 8–12 hours of play, merges and new blueprints beyond. Then price each item as minutes of the income a player has when it unlocks: early 1–3, mid 5–10, late 15–30. At casual income, 10, 15 and 20 minutes of the previous sword's income put the Longsword near 3,500, the Falchion near 8,000 and the Gladius near 15,000 (today 1,000 / 2,000 / 3,500). Give each new blueprint a felt jump (×1.6–2 the last, not ×1.3), and keep the cheap, frequent purchases early where they are.

## 3. Free, unlimited ore

Since [[Sessions/2026-10-24#No hand limit, 1.7× ingots, labels that don't overlap|2026-10-24]] a pull is free, the lever is ready again after the 3.6 s show, waiting ore goes to your hands and hands have no limit (Allen: "remove this limit"; `ForgeService`: "each is a Tool and a save entry, so stack or cap them if hoards of thousands ever slow the pushes or near the 4 MB save"). Crafting time is the only real limit on income, so ore costs nothing to waste:

| Forge only… | Value | Extra pulling a sword | Income | Left over a sword |
|---|---|---|---|---|
| Rare+, 1 ore slot | ×2.5 | 33 s | ×1.6 | 6 ingots |
| Rare+, 6 ore slots | ×2.5 | 6 s | ×2.3 | 6 ingots |
| Epic+, 6 ore slots | ×4.3 | 16 s | ×3.3 | 19 ingots |

(Focused player, 5 s a pull including the hold.)

What it breaks: §2's numbers for anyone who finds it (one video tip away); the thrill of a Legendary, when you can spin for one; luck and merges, which now mean fewer pulls to the same rare instead of rarer swords; Ore Slots 3–6, which mostly save lever pulls; the backpack and the save, with hundreds of ingot Tools.

Options, each a cost on the spin:

1. **Ore on a clock (recommended):** each slot refills on a timer (say one ore every 30 s; more slots, and later a faster refill, give more ore a minute). Spinning stays free whenever ore is ready. Ore Slots become a production upgrade you feel, commons get forged, a full lid is a beat to come back to like the furnace, and a lucky hour (§6) means something.
2. **A carry limit again** (the old 6, or the racks) with no discard, so you forge what you roll. Simple, but it's the limit Allen asked to remove.
3. **Coins a pull**, scaled to the slots: a coin sink, and cherry-picking becomes a gamble you pay for. The tutorial's pulls stay free.

Either way, a **scrap bin** (or Sell on an ingot card) buying unwanted ingots back for a few coins keeps the backpack clean; on its own it makes cherry-picking smoother, not harder.

## 4. Upgrades and swords

**Count:** 41 floor pads, 7 cart levels, 6 trainings, 4 crew crafters and 5 gem levels: about 63 purchases, plenty for a first release. **Felt effect** is the gap:

| Upgrade | What it changes today |
|---|---|
| Faster Heating I–III (3,700) | Nothing for a player who loads the next ingot while forging (the guide teaches it); 6 s a sword for one who waits |
| Ore Slots 3–6 (7,200) | Fewer lever pulls (ore is unlimited, §3) |
| Better Advertising, More Clients (325 gems), Rickshaw Bays (6,000), Shop Promoter (1,500), Wall Racks 3–4, Display Tables 2–4 | Little while you make every sword by hand: about 3.5 walk-ins a minute against about one sword. They matter with the crafter, stocker and a stockpile, or in a rush (§6) |
| Big Sword Stand (2,500) | Nothing: no big-sword blueprint can be bought (the Zanbatō is Dev panel only) |
| Haru, Mei, Kenji, Rin (45,500 + 155 gems) | A better crafter for the one crafter spot: only the one at Anvil 2 works |
| Polishing Station, Etching Table | Fewer coins a minute on your own swords (§5); a pure gain on the crew's |

**Swords:** six blueprints, 31 metals, 7 etch patterns and polish give plenty to look at, but the blueprint ladder ends at the gladius within 12 minutes to 2½ hours, the western steps are small, and big swords have a stand and no way to buy one. The GDD already names the next steps: traditions brought by a visitor's commission (GDD §6.2, §9), big swords as a top tier, shapes from [[Design/Sword Profile Ideas]].

**Proposals:** sell the Zanbatō on a pad after the Big Sword Stand, or hide the stand until one is buyable. Let more crafters work (Anvil 3–5, each with a furnace: Create Pottery!'s "one more station than workers"), so the crew roster is a workforce rather than a swap, and a long coin sink. Give Faster Heating and the Ore Slots their felt effect through ore on a clock (§3), and customer upgrades their moment through rushes and VIPs (§6).

## 5. The core loop

**Moment to moment** the chain is good and reads well: roll, heat, forge, hilt, finish, display, serve. The first sale lands inside two minutes. Three things wear it thin by the hour mark:

1. **No choices.** The hilt fits itself, the best blueprint is always right, customers like nothing in particular (the Knight's 95% rule likes every sword you make), and offers never go below value, so Accept is always fine. After the gladius every sword is the same clicks for the same number.
2. **Optional care loses coins.** Polish (×1.10) pays only if it takes under about 6 s (focused) to 9 s (casual) of a sword; etching (+15%, ×1.10 on a Gem-hilted sword) the same. A polish by hand probably takes longer (not timed yet), so a player who thinks about it stops polishing. On the crew's swords both are free gains.
3. **Near silence.** The anvil's clang and the four cues (furnace ready, offer, sale, cart back) are the only sounds: no loot-box sounds, music, ambience or station sounds. The roll is the game's best clip moment, and it's silent.

**Proposals:** customer tastes shown before the offer (Alignment decision 5), first as VIP buyers (Urgency P3): a highlighted walk-in who wants one thing (etched, polished, Rare+, a katana) and pays about 1.5× for it. That gives polish, etching and the hilt a job and the shop a decision. Then a sound for every station, the roll first. Later, the Test Anvil's shaping (hammer to the line, sand) is the natural skill layer, e.g. a masterwork bonus for a near-perfect match, once it has been played.

## 6. Urgency, events and weather

What already pulls you between stations and shop: offers you have to walk to (45 s), the furnace (cue, glow, "Ready!"), mail orders on a random clock, the cart's trip, the crafter's Ingot Rack (empty in about 8–16 minutes) and Finished Sword Rack (full in about 6–15 without the stocker), and the cashier's till you collect by hand. That's a good set of plates. Missing: anything that makes one moment worth more than another.

Events, to the [[Design/Urgency Review#5. Guardrails|Urgency Review's guardrails]] (bonus only, one at a time, none in the first session, no Robux prompts during one):

| Event | Effect | Length | Matters once |
|---|---|---|---|
| Sunny spell (weather) | Walk-ins ×2; the street fills, rickshaws arrive | 3 min | The crafter and stocker keep stock (Urgency P6) |
| Market day | Every offer +25% | 3 min | From the start: a hand-crafter gains too |
| Hot forge | Heating 3× faster | 3 min | From the start |
| Lucky hour | Luck one merge higher (+0.5) | 3 min | Ore is limited (§3); until then it rewards spinning (P7) |
| VIP visit | One highlighted buyer with a want, about 1.5×, waits about 60 s | until served | Rank 4 (P3) |

Server-wide, so all six shops share it, announced with a HUD icon and a countdown, roughly every 10–15 minutes with quiet stretches between. Rain or evening can come as plain weather with no penalty (GDD §7). A shared event also gives players a reason to look at each other's shops.

## 7. Gold and gems: a reason to want more

- **Gold:** the catalogue in 1–3 hours, then only merges. Long sinks that suit the game: more blueprints and traditions; more working crafters (Anvil 3–5); shop and workshop decor (GDD §11: cosmetic, no stats); the merge.
- **Gems:** 480 to spend in all, earned in a few days. GDD §10.1's Lucky Rolls and timer skips aren't built. Sinks that fit: a Lucky Roll (one roll at higher luck), finishing a cart trip or a heat now, **gem-only etch patterns** (the most visible thing on a sword, a show-off sink), More Special Customers (VIPs more often), inviting a VIP now. A faucet to add: collection-book milestones (GDD §10.1).
- **Reputation:** rank 8 after about 2–3 hours of sales and orders, shown only as "Rank N" in the Deliveries window; ranks 6–8 change nothing you can see. It was meant to bring special visitors (GDD §7), the natural reward for VIPs.

## 8. Coming back and staying

**Coming back tomorrow:**

1. **Offline crew earnings with a welcome-back card** ("While you were away, your crew earned 12,400"), the confirmed later direction ([[Design/Workshop Growth#Later capped offline earnings (confirmed 2026-10-22)]]). It fits because the crew already works without you. Cap it (a few hours, at a reduced rate) so playing stays better.
2. **A daily letter:** one named villager wants an exact sword (an etched Rare+ wakizashi) for a big reward and gems, once a day (Alignment "worth considering" 6), built from the letters already there.
3. **Events on a clock** (§6), and a day-7 streak reward worth waiting for (an exclusive etch pattern).
4. **Collection-book rewards and badges:** first Legendary, every blueprint, all 31 metals.

**Staying longer:**

1. **A pinned next goal** after the katana letter: the next pad or blueprint, with the coins still needed (Alignment "worth considering" 1). Progress nobody can see is the most common reason Roblox players drift off.
2. **Show the progress they have:** the rank on the shop's sign or the HUD, crafter levels, the merge count.
3. **Juice:** sound and a bigger moment for a Rare+ roll and a big sale.
4. **Neighbours:** six plots already share one street; a "Legendary forged!" server message and admiring a neighbour's shop (Alignment "worth considering" 3 and 5).

## 9. Game passes and developer products

GDD §15's rule stays: Robux speeds things up or adds style, and everything can be earned. Timing: after the reprice and the gem sinks. 2× Coins on today's economy turns two hours into one, and gem packs with nothing to buy sell nothing.

| Product | Kind | Why |
|---|---|---|
| Starter pack (gems, an exclusive etch, an Epic ingot) | Developer product, once | A cheap first purchase |
| Gem packs | Developer product | Need §7's sinks first |
| 2× Coins | Game pass, plus a 30-minute boost as a product | The classic; only once the economy is long |
| VIP | Game pass | A golden rack (+10% there, GDD §15) and a name tag: show-off |
| Extra crafter spot (Anvil 3 early) | Game pass | The "large business" fantasy; still buyable with coins later |
| Exclusive etch patterns | Game pass or pack | Cosmetic show-off on every sword |
| Auto-collect the till | Game pass | Convenience; the till stays a hand job for everyone else |
| Lucky Roll | Developer product | **A paid random item** (Roblox counts luck boosts too): odds shown before purchase, and `PolicyService:GetPolicyInfoForPlayerAsync().ArePaidRandomItemsRestricted` checked; where restricted, one of Roblox's listed alternatives, e.g. buying a chosen ingot outright |
| Finish the cart trip now | Developer product | A skip at a point of need |

The HUD's Shop button already exists ("Coming soon"). Offer things where the player is already looking (the cart tracker's "finish now"), never during an event or an offer's countdown; an unaffordable pad keeps its shake, not a Robux prompt. Grant everything from a server receipt handler (`ProcessReceipt`).

## 10. The tutorial

What the guide asks for (`Guide`): pull the lever → collect → heat (3 s) → take it out → forge a tantō → fit a hilt → display → accept the fair offer → **Mailbox** pad → read the letter → accept → *make and sell a second tantō* (the Wakizashi pad is 60, about 27 in hand; sale 2 teaches haggling) → **Wakizashi** pad → make the wakizashi → Send → **Ore Slot 2** pad → "Workshop open!" → daily reward → Gem Shop step. About 30 prompts, three full crafts, 5–8 minutes. Each prompt is one short line with an arrow or a spotlight, and it picks up from your state after a rejoin. It's clear. It's long by Roblox developers' rules of thumb (a 7-minute follow-the-steps tutorial "way too long", 30 steps hurting completion), though most of it is the game itself.

**Faults:**

1. **Saving for the Katana, the guide says "Forge a Tantō"** though you know the wakizashi, worth 2.25× as much. `craft(plot, nil)` always names the tantō; it should name the best blueprint you know. *Fixed 2026-10-27 ([[Sessions/2026-10-27#Tutorial fixes: the best blade, a Gem Shop step that ends on a buy]]).*
2. **The Gem Shop step comes with about 5 gems** (the day-1 reward) and the cheapest gem upgrade costs 25, so the tour ends on things you can't buy. Make Better Advertising's first level cost 5, or hold the step until one is affordable. *Fixed 2026-10-27: the first level costs 5, and the step ends on buying it.*
3. **Nothing after the katana letter.** The guide falls silent once both letters are done (§8, pinned goal).

**Shortening it:** price the Wakizashi pad at 25 or less so the first sale covers the Mailbox and the Wakizashi (one craft fewer; the haggling lesson moves to the next sale), or keep the second tantō as practice. Allen's call.

**Not taught at all:** polishing, etching, the cart, the crew (stocking the Ingot Rack, a full rack), the cashier's till, merging. Each could get a one-time first-use step like the Gem Shop's when its pad is bought.

## Questions for Allen

1. **Length:** how many hours of play to the last floor pad? (Suggested 8–12, with merges and new blueprints beyond.) *Decided 2026-10-27: 8 h to today's last floor pad for a casual picker, the Katana still at 20 min ([[Design/Economy Pass 2]]).*
2. **Ore:** keep free unlimited spins and live with cherry-picking, or put a cost on the spin: ore on a clock, a carry limit, or coins a pull? *Decided 2026-10-27: free unlimited spins stay and the economy is priced for picking; a pull replaces the ore left on the lid and the bag gets a trash icon (the scrap bin was dropped); planned in [[Design/Economy Pass 2]].*
3. **After the gladius:** more blueprints for coins, a tradition by commission, big swords, or all three? And more working crafters (Anvil 3–5)? *Decided 2026-10-27, in part: the Zanbatō as a seventh sword, and up to three crafters working at Anvils 2–4 ([[Design/Economy Pass 2]]).*
4. **VIP buyers with tastes (Urgency P3):** build them next? They give finishing, haggling and reputation a job at once.
5. **Offline crew earnings:** now, and how generous?
6. **Events:** server-wide for all six shops, or per plot? Which first?
7. **Gems long term:** boosts, cosmetics (gem-only etches, decor), or both?
8. **Tutorial:** keep the second tantō, or cut a craft by repricing the Wakizashi pad? *Decided 2026-10-27: keep the tutorial's prices (and its second tantō).*
9. **Big Sword Stand:** sell the Zanbatō now, or hide the stand until big swords are ready? *Decided 2026-10-27: sell the Zanbatō, a late goal with the stand in its stage.*
10. **Robux:** after the economy pass, starting with a starter pack, gem packs and 2× Coins?

## Concerns

- **None of the economy has been timed.** In the next playtest, time one sword (roll to sale, with and without polish and etch), one polish, coins at 10, 30 and 60 minutes, and when the katana gets bought; the model's numbers move with them.
- **No economy analytics:** only the onboarding funnel is logged. Log coin and gem sources and sinks (`AnalyticsService:LogEconomyEvent`) before any public test.
- **Hoarded ingots** (§3) grow saves and the hotbar whatever the economy rule.
- **Placeholder prices** on the crew, the western blueprints, the Big Sword Stand and Etching Table 2 are still the ones set the day they were built.

## Second look (later on 2026-10-27)

Allen: "Review the findings for today." Checked against the live modules in Edit, read only (`Upgrades`, `Blueprints`, `Materials`, `Hilts`, `Customers`, `Employees`, `Deliveries`, `GemUpgrades`, `Orders`, `Reputation`, `ValueFormula`, `ForgeCheck`, `SmithyCore.swordValue`, `EmployeeService`, `EmployeeController`, `Hud`), and the model rerun.

- **The numbers hold.** All 41 pads with their prices and `after` chains, the odds (×1.569), hilts, offers (113%, 121% on a wakizashi), crew, training and cart prices match the model, and it reproduces §2's table. Every player sword is 100% (×2.0; `ForgeCheck`: all strikes done = 100%), so the Knight's ×1.25 does take every one.
- **"Too fast" survives slower hands.** At twice the casual player's time everything is bought in 4 h; at three times, 5 h 30. Both are still under the suggested 8–12 h, so the playtest timings move the dates, not the verdict.
- **Gems:** 480 to spend now (Gem Shop 325 since the tutorial fix), corrected above.
- **New: a crew hire starts at Lv. 1.** Each crafter levels on its own (`hired[id].made` starts at 0) and only the equipped one works, so against a levelled Taise every hire is a step down at first (70–85% against his 86% at Lv. 3; the crew window shows ▼) and pays back only after 10–30 swords. Haru barely ever does: 2% more quality a level and 1 s faster forging at Lv. 5. Strengthens §4's Anvil 3–5 proposal.
- **Ore (§3): unlimited spins are Allen's own call:** "Players should be able to spin the ores as many times as they want" (Refinements 3, 2026-10-23), then "remove this limit" (2026-10-24). Option 1 reverses the first, option 2 the second; only option 3 keeps both, but a price per pull high enough to stop picking Rare+ (about a quarter of an average sword's value per ore) takes the same quarter off normal play. Option 1's example rate (one ore every 30 s a slot) also still leaves a pick: six slots give 12 ore a minute against about two swords (yours and the crafter's), so the best of about six is Rare+ on ~62% of your swords. Commons get forged only if the refill follows sword speed (roughly 1.2–1.5 ore a sword). The crafter already takes the cheapest ingot first ("so your rare metals wait for you"), but at about one a minute it can't eat 6–19 leftovers a sword, so the scrap bin is needed either way.
- **Polish and etch already have a small job (§5):** about a third of mail orders and half of Special deliveries ask for a polished or etched sword (1.2× plus gems and reputation; the cart 0.8×), so today's best play is "finish only for orders". VIP buyers would widen that rather than create it.
- **Smaller:** `EmployeeService`'s header still says "+3% a level" (`Employees.QUALITY_STEP` is 8 since Refinements 5). The HUD's Reputation pill still exists, hidden since 2026-10-24 (`HudGui.Reputation.Visible` false; `Hud` still fills it), so §8's "show the rank" is one property if Allen wants it back.

Related: [[Design/Alignment Review — 2026-10-23]] · [[Design/Urgency Review]] · [[Design/Tycoon Upgrades]] · [[Design/Workshop Growth]] · [[Design/Game Design Document]] · [[Design/Core Loop Review]] · [[Development/Roadmap]]

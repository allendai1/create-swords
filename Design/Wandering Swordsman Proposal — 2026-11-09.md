---
title: Wandering Swordsman Proposal — 2026-11-09
status: option D built 2026-11-10 with placeholder designs (see Sessions/2026-11-10)
type: design
updated: 2026-11-10
tags: [design, npc, blueprints, pacing, gems, create-swords]
---

# Wandering Swordsman Proposal — 2026-11-09

Allen ([[tonights notes]] line 26): "wandering swordsman? someone who offers blueprints of swords, you can only buy thru him". Earlier today he put it as "wondering swordsman that daily offers for unique sword designs that you can only buy (either with gems or gold) providing more incentive to get more of either" ([[Design/Monetization Ideas — 2026-11-09#Allen's answers (2026-11-09, later)]]). This note builds on that note's short stub. **Nothing is built or decided.**

Checked against [[Design/Decisions Log]], [[Design/Monetization Plan]] §4 and §7, the guardrails in [[Archive/Design/Urgency Review#5. Guardrails]], [[Design/Economy and Progression Review — 2026-11-08]], [[Design/Major Updates Plan — 2026-11-07]] and the sim export (`Development/sim/balance.json`, 2026-11-07).

## What already exists

- **Musashi is already the Wandering Swordsman.** He's in `Shared/Senders` with a face and an outfit, and he wrote the old Katana letter (2026-10-22 to 10-28). Today he never writes ([[Design/Major Updates Plan — 2026-11-07]] gives him the Sakabatō secret letter, not decided).
- **Blueprints are tycoon pads** (2026-10-23): 23 pad blueprints on one chain, Wakizashi 60 coins to Seraph 1,090,000. The big swords (Zanbatō → Claymore → Flamberge) are a chain on their own pad. The Butter Stick is the only blueprint you can't buy; it comes from a secret letter.
- **The Japanese line is thin.** Tantō, Wakizashi, Katana, then nothing Japanese until the Zanbatō. The middle and late chain is Western, Chinese and Fictional. [[Design/Sword Profile Ideas#Japanese]] lists eight Japanese shapes marked Easy (data only in BladeCore), all unbuilt.
- **Japanese hilts are fitted automatically** (2026-10-23), so a Japanese design needs no hilt work.

## The problem it solves: the trough

- From the Zanbatō on (about 4:30–5:00 for engaged players), the catalogue thins out. Engaged players reach the Seraph at 8:43–11:49, then buy almost nothing but Ore Slots and merges until 20 h. Efficient players make **1** buy after the Seraph that isn't an Ore Slot ([[Design/Economy and Progression Review — 2026-11-08#1. The catalogue ends at ~10 h for engaged players; after that only the ore merge is left]]).
- The fix the sim asks for is **new things to buy in the 5–11 h window, about 5–10 min of income each**. Cheaper late blueprints only shorten the game.
- Income then: an engaged player earns about 20,000–30,000 coins a minute at 8 h (Ren's 150,000 is 5–7 min of income). A casual player earns about a third of that.
- A wandering swordsman is exactly this: a set of extra blueprints, off the main chain, that show up when the pads run out.

## Rules it has to keep

| Rule (source) | What it means here |
|---|---|
| Requests come by mail; no in-person visitor requests (2026-10-23) | Musashi never asks for a sword. He only sells. His arrival comes as a letter. |
| Blueprints are tycoon pads (2026-10-23); stations never open menus (2026-10-25) | His designs are **pads** on his stall, like Showcase Stands 2 and 3. Pressing E on him opens nothing. |
| Pad labels: one line "Name · price", within ~14 studs | One currency per pad, so the label stays one line. |
| One sword chain (2026-10-30) | His designs aren't on the chain. They sit last in the Book, like the Butter Stick. |
| Paid random items (Monetization Plan §4) | You always see a design before you pay. Which designs he has today is random, but you never pay for a random one. **No "mystery scroll".** |
| No lowball offers (2026-10-31) | His swords sell like any sword: customers open at value to +20%. No haggling with Musashi. ~~No "50% off today"~~: overruled 2026-11-10, he sells discounted upgrades (see "Discounted upgrades"). |
| No Robux at the moment of urgency; nothing owned is lost (Urgency Review §5) | No Robux price on his pads. The "short of gems → covering pack" popup (2026-10-28) stays **off** on his pads, because his stock has a clock. A design you miss comes back on a later day. |
| Real timers, end time shown, no "last chance" text (Roblox timer rules, as the Festival plan) | His sign shows when the stock changes. The clock never restarts. |
| None of it in the first session (Urgency Review §5) | He comes after a progress gate (see below). |
| Secret swords are never bought (Monetization Ideas 2026-11-09) | His designs are real swords; the Butter Stick, Sakabatō and Moonhook stay letter rewards. |

## The designs (the same pool for every option)

Eight Japanese shapes from [[Design/Sword Profile Ideas#Japanese]], each **pinned** to a chain sword. A design is offered only once you own its pinned sword. Its value is about **×1.1 the pinned sword's**: a step up from what you make now, not a jump ahead of the chain.

| # | Design | Shape | Pinned to (value) | Its value |
|---|---|---|---|---|
| 1 | Chokutō | ancient straight sword | Khopesh (310) | ~340 |
| 2 | Shōbu-zukuri | iris-leaf, long taper | Rapier (380) | ~420 |
| 3 | Unokubi-zukuri | slim near the tip | Hook Sword (430) | ~470 |
| 4 | Tachi | deep curve by the hilt | Shard Blade (540) | ~590 |
| 5 | Ō-kissaki | wide, oversized point | Serpent (680) | ~750 |
| 6 | Nodachi | stretched katana | Leviathan Cleaver (780) | ~860 |
| 7 | Naginata-naoshi | flares wide near the tip | Thornspire (880) | ~970 |
| 8 | Kogarasu-maru | half double-edged; the masterwork | Seraph (980) | ~1,080 |

- **Coin price:** about 0.4–0.5× the pinned sword's pad price. For example, the Chokutō costs about 80,000–100,000, about 4–5 min of income when you get it; the Kogarasu-maru about 450,000–550,000. These are starting numbers; the sim sets the real ones.
- **Gem price:** 50–80 gems by tier. Daily rewards give 192 gems a week, and weathers cost 60 / 120, so a gem design costs 2–3 days of daily gems.
- Two **spares** for later pool growth: Ninjatō (Allen's "fun one") and Yoroi-dōshi. Adding designs later is a cheap content update.

## Options

### A. Daily stall (Allen's version) — recommended

- **When:** after the gate, a letter from Musashi: he's come down from the mountain and will stay by your shop. From then on he's **always there**.
- **Where:** a small stall in your plot (a rug, a low stand, three pads in a row sideways), on clear floor where you see him from the shop. Claude's default spot: the front yard, left of the shop door, clear of the cart. Allen picks the spot in Studio.
- **Stock:** each day, at the daily reward's reset, **3 designs** from the ones you qualify for and don't own: **2 coin pads and 1 gem pad**. The same design can be on a coin pad one day and the gem pad another. That gives "either with gems or gold" without two prices on one label. Today's 3 are saved (one small save field), so buying one doesn't refill the slot; the bought pad shows the sword on its stand until tomorrow.
- **Return hook:** "what does Musashi have today" is the D1–D7 reason to log in. The game has no such hook today.
- **Weak spot:** a player who plays 6 h in a day sees one stock. They are the trough players. A shorter clock (every 4 h) fixes that; see question 3.

### B. Visits to the village

- He walks in **server-wide**, like a weather, every ~45–60 min. He stays ~10 min at a plaza stall (the plaza is built and "nothing walks it"). Everyone on the server sees the same 3 designs. A banner like the weather's: "[Musashi] In the plaza · 9:12".
- **Good:** the most "wandering", social, and uses the plaza.
- **Bad:** a 10-minute countdown is the pressure the guardrails warn about, and most players are under 13. It collides with "one surprise at a time" (weather is always on). It also pulls players away from the plot mid-craft. A player who misses him waits an hour.
- Better kept as a **Village Festival** add-on later ([[Design/Major Updates Plan — 2026-11-07#3. Village Festival — the live-ops update]]) than as the main way to get designs.

### C. Master's ladder (no rotation)

- After the gate, his stall is permanent and shows **one design at a time**: the next one you qualify for, its price fixed. Buy it and the next appears once you own its pinned sword.
- **Good:** no clock, no pressure, simplest to build and to model in the sim.
- **Bad:** it's just 8 more pads. No daily reason to come back, and no "he's here" moment. It doesn't do what Allen asked ("daily offers").

### Recommendation

**A, with C's gate inside it:** a daily stall that only offers designs you qualify for. It answers Allen's "daily" and "gems or gold", adds 8 trough buys at roughly 5–10 min of income, adds the return hook the game lacks, and breaks none of the rules above. B can come later as a Festival extra.

**Changed 2026-11-10:** Allen wants Grow a Garden's restock system. Option D below (A's always-there stall with Grow a Garden's Seed Shop restocks) is now the recommendation.

## The gate

- **Recommended: when you buy the Zanbatō.** That's where the trough starts (4:26–4:59 for engaged players). By then they already own the Khopesh or the Rapier, so the first stock isn't empty.
- **The cost:** casual players reach the Zanbatō at ~11 h, so they meet Musashi around day 11. They still have chain pads to buy, so they don't need him sooner.
- **The other choice:** after the Sword Crafter (15–35 min). Every player gets the daily hook in week 1. But the stock is empty until they own the Khopesh, and an empty stall reads as broken.

## How players are told

1. **The first time:** Musashi's letter in the mail (the mail dot, the channel players already know). One line in his voice, no tutorial spotlight (letters after the first don't replay the tutorial, 2026-10-28). He's standing at the stall when you close the mail.
2. **New stock each day:** a small marker over his head while today's stock is unseen (a Studio template billboard, like the pad labels). Walking within ~14 studs clears it. No toast, no popup (minimal UI text).
3. **His sign:** "New designs in 6:41:12" on the stall, only within ~14 studs.
4. **Nothing in the top bar** for A. (B would need a weather-style banner.)

## What it costs to build (A)

- **Blades:** 7 Easy profiles (data only) + Kogarasu-maru (Care: the back becomes an edge near the tip). Each needs its blade bake for etches and the sheen, a Book entry, a silhouette, and prototype JSON so `BladeCoreSpec` covers it. About 2–3 sessions.
- **Stall and Musashi:** his rig from `ServerStorage.Cast` with the Senders outfit; the stall props modelled in Blender, low-poly, uploaded. A natural idle pose (NpcWalk rules). About 1 session.
- **Stock and pads:** daily stock, one save field, 3 pads (2 coin, 1 gem) that read the stock, the letter, the marker, the sign. Server-side purchase like other pads. About 1–2 sessions.
- **Sim:** the export gains the designs (pin, value, prices); `rules.py` rolls a 3-design stock each sim day (1 h a day); the buy order treats his pads like pads. Measure against the review's target: **at least 20 non-Ore-Slot buys after the Seraph for an efficient player** (today 1), and fewer waits over 15 min. 8 designs alone won't reach 20; with Legendary Commissions they could. About 1 session.
- **Total:** about 5–7 sessions.

## How it sits with Legendary Commissions

- They fill the same window in different ways: commissions are **letters** (craft to order), Musashi's designs are **buys** (new swords to make and sell). The review needs both kinds of goal.
- Musashi is the cheaper build: Easy blades, auto-fitted hilts, the pad system as it is. Commissions need four New-feature blades (fork, serrations, hook, flame edge).
- **One clash:** the Major Updates plan has Musashi send the Sakabatō secret letter. If he becomes the seller, his letter is the stall letter, and the Sakabatō gets a new sender (or stays his as a later surprise). Allen's call.

## Grow a Garden's restocks, and what fits us (2026-11-10)

Allen: "look up how Grow a Garden does their restocks, they have a good system i want to copy, but they also have multiple things that are stocked at different prices, see which one applies to our game."

### What Grow a Garden does

Sources are fan guides and stock trackers, not official; some mix Grow a Garden 1 and 2. Treat the numbers as close, not exact.

| Shop | Restock | How it works |
|---|---|---|
| **Seed Shop** (Sam) | every ~5 min | The whole list is replaced at once. Each seed rolls its own chance to appear: Carrot (1–10 sheckles) is in every time; the top seeds cost tens of millions and show well under 1% of restocks. Each seed that appears rolls a quantity. Sold out shows a grey NO STOCK. |
| Gear Shop (Eloise) | every ~5 min | Same roll, for tools used up as you play (a Watering Can 1–4 in stock, a Trowel 1–3) |
| Pet Egg Shop (Raphael) | every 30 min | Eggs hatch a random pet |
| Cosmetics Shop (Isaac) | every 4 h | Decorations |
| Daily Deals | every 24 h | A daily row in the Seed Shop (Grow a Garden 2) |
| **Traveling Merchant** | every ~4 h, from 00:00 UTC, not guaranteed | Stands beside the Seed Shop for **30 min**. One of several themed merchants (Gnome, Sky, Honey, Sprinkler…), 3–15 items each |
| Instant restock | 79 R$ (90 for eggs) | Refreshes one shop's stock once |

- **One clock for everyone:** the timer and the stock list are the same on every server, so players can talk about it (and fan sites run live stock trackers and Discord notifiers).
- **Your buys don't empty anyone else's stock** (one guide says purchases are client-side; another says a Beanstalk buyout empties it for everyone, so this is disputed).

### What carries over

1. **The Seed Shop's restock is the system to copy.** One shared clock; the whole stock replaced at once; every item rolls its own chance, so cheap ones are nearly always in and the best ones rarely; a visible countdown; buys are per player. This is what makes players check the shop again every few minutes.
2. **"Things stocked at different prices" = his designs in price tiers.** The 8 designs split into Common, Rare and Legendary, like Grow a Garden's seed rarities: cheap ones in most restocks, the masterworks seldom.
3. **The Traveling Merchant gives Musashi his identity, not his timing.** A 30-minute visit every 4 hours overlaps a 1-hour session about 1 day in 3 (the sim's player plays 1 h a day), often for only a few minutes. That's option B's problem, made worse.

### What doesn't carry over

- **Quantities.** A seed or a watering can is used up, so its quantity matters. A blueprint is learned once, so each design is quantity 1: once bought, it's gone from your stock for good.
- **The Gear Shop.** We have nothing that's used up and bought again.
- **The Egg Shop.** A random pet bought with gems is a **paid random item** (gems can be bought with Robux): an odds panel and hidden in restricted regions. His stock is shown before you pay, so it isn't one.
- **The Robux instant restock.** Paying to reroll a stock that might hold a rare design is paying for a chance: a paid random item (odds panel, hidden in restricted regions), and Robux at the moment of urgency (Urgency Review §5). Not recommended.
- **Ingots as the cheap row** (the obvious "seeds" for us). Spins are free and unlimited (Decisions Log), so common ingots are worth nothing. Rare ones for coins would undercut Lucky Ore and the "pick 6" Legendary pack idea ([[Design/Monetization Ideas — 2026-11-09#Legendary ore pack: you pick the metal (proposal)]]). Not recommended.

### D. Musashi's stall with Grow a Garden restocks — now recommended

- **Where and when:** as A. After the gate, his letter, then he stays at his stall in your plot for good.
- **Clock:** every **10 min**, the same everywhere. The stock is rolled from the time slot (`os.time() // 600` as the random seed), so every server agrees without any cross-server messages. Grow a Garden uses 5 min; ours is 10 because a design is a big buy (5–10 min of income), not a seed.
- **Tiers and chances** (each design you qualify for and don't own rolls on each restock):

| Tier | Designs | Chance a restock | Average wait |
|---|---|---|---|
| Common | Chokutō, Shōbu-zukuri, Unokubi-zukuri | 50% | 20 min |
| Rare | Tachi, Ō-kissaki, Nodachi | 20% | 50 min |
| Legendary | Naginata-naoshi, Kogarasu-maru | 8% | ~2 h |

- **Never locked out:** if a design you qualify for hasn't shown for you in 12 restocks (2 h of play), it's in your next one. This is per player, on top of the shared roll. Grow a Garden has no such floor; its rarest seeds can stay away for days.
- **"Either gems or gold":** each row has a coins button and a gems button, like Grow a Garden's sheckles and Robux buttons. No Robux button, and no pack popup on his rows.
- **A window, not pads:** E on Musashi opens his stock as rows (the sword, its tier, both prices, the countdown at the top), like talking to Sam. 8 pads with labels don't fit a phone screen. This breaks the pad rule (blueprints are tycoon pads, 2026-10-23; stations never open menus, 2026-10-25), but Musashi is a person, not a station. Allen's call.
- **How players are told:** the countdown on his sign and at the top of his window; a marker over his head only while something you can buy is in stock. No toast, no top-bar icon.
- **Pacing:** it fixes A's weak spot. A player in a 6-hour session sees 36 restocks, not one stock. The 8 designs still run out; new designs are the content updates.
- **Build:** as A, but a window (phone-first, UI audit) instead of 3 pads, and no save field for the stock (it comes from the clock). The save keeps only each design's last-seen slot for the floor. About 5–7 sessions.
- **Sim:** `rules.py` rolls the stock each 10 sim-minutes from the same seed; the buy order buys a design when it's in and affordable.

## Allen's answers (2026-11-10)

Allen: "1. im not sure what the options are 2. after the sword crafter 3. we dont have as much variety as grow a garden, so probably not every 5 minutes , every hour or few hours? consult me on this? 4. we can have his stock show in a window"

- **The options, in one line each:** A: he's always there with 3 new designs once a day. B: he visits the plaza for 10 min every hour, for the whole server. C: he's always there with one design at a time, never changing. D: he's always there and his stock changes on a clock, rarer designs less often (Grow a Garden). **The answers below already pick D** (a stock that changes every hour or few, in a window).
- **Gate: after the Sword Crafter** (15–35 min, 37 min for casual players). Musashi's letter comes once you have the Crafter and the Katana (the Katana nearly always comes first, at 12–19 min).
- **Window:** E on Musashi opens his stock as rows. He's a person, not a station, so the "stations never open menus" rule stands.
- Already decided on 2026-11-09 (Decisions Log): designs sell for more than a regular sword of their tier, each has a Book page, a missed design comes back, and Allen first said "maybe every 3 hours?" for the stock.

### What the Crafter gate changes: 10 designs, pinned from the Katana

The old pins started at the Khopesh (about 3 h in), so the stall would sit empty for hours after his letter. Re-pinned from the Katana, adding the two spares (Yoroi-dōshi, Ninjatō: both Easy, about half a session more):

| Tier | Design | Pinned to (value) | Its value | Coins (0.4–0.5× the pinned pad) |
|---|---|---|---|---|
| Common | Yoroi-dōshi | Katana (110) | ~120 | ~520–650 |
| Common | Ninjatō | Longsword (160) | ~175 | ~5,300–6,700 |
| Common | Chokutō | Falchion (220) | ~240 | ~15,000–18,000 |
| Common | Shōbu-zukuri | Gladius (280) | ~310 | ~31,000–39,000 |
| Rare | Unokubi-zukuri | Dadao (340) | ~375 | ~83,000–104,000 |
| Rare | Tachi | Hook Sword (430) | ~470 | ~150,000–190,000 |
| Rare | Ō-kissaki | Shard Blade (540) | ~590 | ~210,000–260,000 |
| Legendary | Nodachi | Serpent (680) | ~750 | ~300,000–370,000 |
| Legendary | Naginata-naoshi | Leviathan Cleaver (780) | ~860 | ~330,000–420,000 |
| Legendary | Kogarasu-maru | Seraph (980) | ~1,080 | ~440,000–545,000 |

- Engaged players earn a new design about **once an hour** (Crafter at ~20 min to the Seraph at ~10 h). Casual players reach about 6 of them in 20 h.
- **Risk:** the first four come while the main chain still has lots to buy, so they speed up the early game a little. The sim checks this before the prices are set.

### The stock with a slow clock

A 5-minute Grow a Garden clock works because each roll can come up empty: the next one is close. With a clock of hours, each stock has to be worth looking at:

- **Up to 3 designs a stock** (the 2026-11-09 default). Common designs you qualify for are always in; Rare 50%; Legendary 25%. If more than 3 roll in, 3 are picked.
- **Floor:** every design you qualify for is in by the **4th stock you see** (stocks that change while you're offline don't count).
- The stock is still rolled from the clock, so every server shows the same designs to players at the same point.

### The clock: 1 hour or 3 hours

Pinning means most players qualify for only 1–3 unbought designs at a time, so the clock mostly decides **how long a newly earned design waits before it shows**, and how often a Legendary roll comes.

| | Every 1 h | Every 3 h (Allen's 2026-11-09 guess) |
|---|---|---|
| Stocks a 1-hour session sees | 2 (the one on, then one change) | 1, sometimes 2 |
| Stocks a 6-hour session sees | 6–7 | 2–3 |
| A newly earned design shows | within 1 h | within 3 h, often next login |
| Average wait for a Legendary design (≈2.7 stocks seen) | ~1.5 days at 1 h a day; ~3 h in a long session | ~2 days at 1 h a day; ~8 h in a long session |
| The countdown on his sign | "New stock in 0:23:10": a reason to stay a bit longer | "New stock in 2:41:05": mostly a reason to come back tomorrow |
| How it feels | Steady: about one design an hour, the same pace players earn them | Batches: designs pile up and come 2–3 at a time |

- **Claude's pick: every 1 hour.** Still 12× slower than Grow a Garden. It matches the pace players earn designs (about one an hour), and it gives long sessions something to come back to. With only 10 designs, a 3-hour clock means many players see the same stock all session.
- **For 3 hours:** fewer, bigger moments, and a new stock nearly every login. Better if the stall should feel like a rare visit rather than a shop.
- Allen decides; the sim can run both.

## Discounted upgrades (Allen, 2026-11-10)

Allen asked whether Musashi could also sell "existing sword upgrades but at a discount from what they are normally". Claude advised against it for three reasons; Allen overruled all three:
1. It shortens the game. Allen: "if it shortens the game, we can always add more to lengthen it.."
2. The same upgrade sold in two places could break the unlock order. Allen: "this is easy to fix no? we just need to ensure the one that musashi sells is the next one to be upgraded."
3. A discount that ends on a countdown is pressure. Allen: "this is a non-problem and is good for our game."

**So his window has two kinds of row:** his designs (still to pick) and **deals**.

**Claude's defaults for the deals:**
- **Which upgrade:** only pads you could buy right now on your floor: the next step of a chain, never one whose earlier step you're missing. Buying the deal buys that pad: it builds as if you'd stepped on it, and the pad disappears. Ore Slots and merges count, so deals keep coming after the Seraph.
- **How many:** 2 deals a stock, picked at random from your buyable pads. Always something in the window, even once every design is bought (this also answers "not much variety").
- **Discount: 10% to 50% off, low more likely** (Allen, 2026-11-10: "10% floor to 50% ceiling, obviously with lower % more likely than a 50% off"). Claude's weights: 10% (40), 15% (25), 20% (15), 25% (10), 30% (5), 40% (3), 50% (2); about 17% off on average, a 50% deal about 1 in 50. Shown as the pad's real price crossed out, as the Everything Bundle does. The pad keeps its full price on the floor. You see the discount before you buy, so it isn't a paid random item.
- **Currency:** the pad's own: coin pads in coins, gem pads (Showcase Stands 2 and 3, the gem etches) in gems.
- **Clock:** the same hourly stock. A deal you don't take is gone at the restock; the pad stays at full price.
- **Per player:** deals come from your own buyable pads, so they can't be shared between servers like the designs. Each player's 2 deals are rolled from the hour and their UserId, so a rejoin shows the same deals.
- **Sim:** mirror it in the same pass (`rules.py` rolls 2 deals an hour from the buyable pads; the buy order takes a deal when it's a pad it would buy anyway). Measure how much sooner the Crafter, the Zanbatō and the Seraph come, so the content to lengthen it is sized from the run.

## Questions for Allen

**Answered 2026-11-10:** option D; the gate is the Sword Crafter; the stock shows in a window; **the stock changes every 1 hour** (Allen: "Every 1 hour").

**Must answer (Allen, 2026-11-10: "we never agreed on what he would sell"):**
1. ~~The clock~~: every 1 hour.
2. **What he sells.** Agreed so far (2026-11-09): "unique sword designs that you can only buy", for coins or gems, worth more than a regular sword of their tier, with a Book page. **Not agreed:** which swords, how many, and whether they're all Japanese. The 10 Japanese designs in the re-pinned table are Claude's proposal only.
3. ~~A Robux "bring every design in now" button~~: **dropped** (Allen, 2026-11-10: "drop it"). Common designs are always in, the floor caps the wait at 4 stocks, and most hours nothing is missing, so there was little to pay for. No Robux restock of any kind.
4. ~~Deals~~: 10–50% off, weighted low (Allen, 2026-11-10); 2 a stock stays Claude's default.
5. **Designs may come from Allen's other sword session** (2026-11-10: "i have another session working on more swords").

**Claude's defaults unless you say otherwise:**
2. Up to 3 designs a stock: Common always in, Rare 50%, Legendary 25%; every design you qualify for is in by the 4th stock you see.
3. Every row has both a coins and a gems price (replaces the 2026-11-09 default of 2 coin + 1 gem: a window has room for both); no Robux price, no Robux restock, no pack popup.
4. A design is worth about ×1.1 its pinned sword (a step up).
5. ~~The pool~~: moved to "Must answer" above.
6. Musashi doesn't send the Sakabatō letter; it gets a new sender.

Sources (Grow a Garden): [Nerds Chalk, GaG 2 restock times](https://nerdschalk.com/grow-a-garden-2-shop-restock-times/) · [Beebom, traveling merchants](https://beebom.com/grow-a-garden-traveling-merchants-guide/) · [Gamezebo, seeds](https://gamezebo.com/walkthroughs/grow-a-garden-seeds) · [Gamezebo, pet eggs](https://www.gamezebo.com/walkthroughs/grow-a-garden-pet-eggs/) · [Pro Game Guides, merchant timings](https://progameguides.com/roblox/grow-a-garden-traveling-merchant-location-and-timings) · [Sportskeeda, Beanstalk restock](https://www.sportskeeda.com/roblox-news/how-often-beanstalk-restock-grow-garden) · [All Things How, GaG 2 seeds](https://allthings.how/all-grow-a-garden-2-plants-and-seeds-costs-rarities-and-how-to-get-them/)

---

Related: [[Design/Monetization Ideas — 2026-11-09]] · [[Design/Economy and Progression Review — 2026-11-08]] · [[Design/Major Updates Plan — 2026-11-07]] · [[Design/Sword Profile Ideas]] · [[Design/Decisions Log]] · [[Sessions/2026-11-09]]

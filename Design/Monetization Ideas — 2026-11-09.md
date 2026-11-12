---
title: Monetization Ideas — 2026-11-09
type: design
status: Golden Hour being built; the rest proposed
updated: 2026-11-09
tags: [monetization, robux, developer-product, weather, gifting, cosmetics, gems, create-swords]
---

# Monetization Ideas — 2026-11-09

Allen: "can we brainstorm some more developer products or purchases. like one time purchases" — timed server boosts (coins, gems, forge speed, anvil speed, all multipliers for 5 minutes), legendary ore packs, Sword Crafter skins, a timed ore-chance multiplier, gems or direct Robux to skip levels, offline earnings, instant polish/anvil/forge completion, gifting to friends, more custom etches, more custom/fun swords. [[Sessions/2026-11-09#Monetization brainstorm 2]]

**Proposals only:** nothing built, decided or changed on Roblox. Each idea was checked against [[Design/Monetization Plan]] §8, [[Design/Monetization Ideas — 2026-10-31]] (its Don't table) and the [[Design/Decisions Log]].

## Fits the rules: build candidates

| # | Idea | Shape | Price | Why it fits | Watch |
|---|---|---|---|---|---|
| 1 | **Golden Hour** (Allen's "all multipliers for 5 min") | A fifth bought weather: Sunshine + Rainbow + Snow together, whole server, 5 min, buyer named | 149 R$ or 120 gems | Uses the built weather queue; one system for server boosts | Leave **luck out**: with luck it's a paid random item (odds panel, restricted players), like Rain |
| 2 | **Gifting** | Gift button on pass cards and weather; a Roblox friend in this server | the item's price | 2026-10-31 idea #5; weather gifts are already "for the server" | Buyer's initiative only; no requests, a daily cap; `Store.owns` reads saved gifts too |
| 3 | **Crew outfits** (Allen's "swordcrafter skins") | Themed outfits per crew member, picked on the crew card; visitors see them | 49 R$ each or 149 R$ for all (the Crew Wardrobe) | Style only; catalog outfits already dress the crew | Each crafter is dressed differently today (2026-11-01); a theme must keep them tellable apart |
| 4 | **Fun swords as cosmetics** | A held/swung look (e.g. a fish, a baguette, a giant key) — not shop stock, sells for nothing | 49–99 R$ each | Style; no economy effect | One model per object; Blender low-poly; must not read as a metal or tier |
| 5 | **Etches for gems** (Allen's "more custom etches") | New etch patterns in the Gem Shop | 40–120 gems | Earnable by play, so not "buyers-only"; Robux buyers reach them through gem packs | Allen ruled out *buyers-only* etches on 2026-10-27; this keeps that rule |

## Already covered or already ruled out

| Idea | Status | Where |
|---|---|---|
| Timed coin boost | Dropped 2026-10-27: Sunshine (bought weather) and coin packs cover it | Plan §8 |
| Timed gem boost | 50% More Gems pass (2026-11-09) covers it | Plan §50% More Gems |
| Timed ore-chance multiplier | That is **Rain**, a bought weather (planned, not built: needs the odds panel and the policy check) | Plan §3 |
| Timed forge or anvil speed | Competes with the Faster Heating / Faster Strikes upgrades (one system per effect) | Plan §8, instant heat |
| Instant polish / anvil / forge | Skips ruled out; the Auto Anvil (and the proposed Auto Polish) sell comfort instead | 2026-10-31 Don't #24 |
| Legendary ore pack (random) | Paid random item (odds, restricted regions); Allen called ingots "pointless" as rewards on 2026-11-08. The fixed Epic/Legendary Ingot products exist, off sale, for restricted players | Plan §4 |
| Offline earnings | Decided as a **later, capped** game system, not built. A product only after it exists (e.g. a pass that lengthens the cap) | Decisions Log, "Later capped offline earnings" |

## Gems or direct Robux skips?

**Keep gems.**
- **The rule:** "anyone can earn everything by playing" (GDD §15; gems buyable with Robux since 2026-10-17). Gems are earnable; a Robux-only skip isn't.
- **One price list:** each upgrade has one gem price. A Robux skip per upgrade means a product per upgrade and per level.
- **The one-tap skip exists:** tapping an unaffordable upgrade already offers the smallest gem or coin pack that covers it (2026-10-28).
- **Pricing:** Managed Pricing tests a few gem packs, not dozens of skip products.
- Robux for pads or levels directly is on the Don't list (2026-10-31 #29).

## Questions for Allen

1. Golden Hour as a fifth weather, without luck, 149 R$ / 120 gems?
2. Gifting: passes and weather, friends in the same server?
3. Crew outfits: per outfit (49) or one Wardrobe pass (149)?
4. Fun swords: which three first?
5. New etches for gems in the Gem Shop?


## Allen's answers (2026-11-09, later)

Allen: "lets do golden hour. but maybe also more boosts/weather effects? legendary ore pack doesn't have to be random necessarily, they could pick like 6 of their choice for example. offline earnings maybe after buying cashier? in cashier description we could include that so players know to buy it. i do like the more etches with gems idea. also what about wondering swordsman that daily offers for unique sword designs that you can only buy (either with gems or gold) providing more incentive to get more of either."

**Golden Hour: being built** (149 R$ or 120 gems; product 3730123757 in Swordsmith, off sale like the other weathers). Allen: new items go in Swordsmith (10769630190) only; the Sell Swords! copy 3730123763 is unused.

### More weathers (proposal)

Weathers cover four of the six boost stats (Sunny Customers, Snow Mail, Rain Luck, Rainbow VIP). Two are missing, so two new ones:

| Weather | Bonus | Look | Note |
|---|---|---|---|
| **Cherry Blossom** | +25% coins on every sale | pink petals drifting (the village already has cherry trees) | A timed coin boost was dropped on 2026-10-27; as a weather it's the server format, not a personal 2x |
| **Breezy** | walk 25% faster, cart trips 25% shorter | leaves and dust blowing past | Swift Boots and the Swift stands stay bigger |

Questions: in the free rotation too (with weights), or bought only? 79 R$ / 60 gems like the others? Does Golden Hour then include them?

### Legendary ore pack: you pick the metal (proposal)

- **6 ingots of one Legendary metal you pick** (maybe an Epic pack too). A fixed choice, so **not a paid random item**: no odds panel, sold everywhere.
- **Only metals already in your Book** (as the restricted-region ingot): buying can't skip finding a metal, and the ingots don't fill its Book page.
- Questions: found metals only? Legendary only, or Epic and Legendary packs? Price (the single Legendary Ingot product is 99 R$)?

### Offline earnings with the Cashier (proposal)

Turns the decided "later capped offline earnings" into: **the Cashier keeps selling while you're away.**
- She sells the swords left on your racks and stands to walk-ins at her answer rate, until the stock runs out or the cap (say 2 h) is reached. The stock you leave is the natural cap. The crew don't craft offline.
- On return: one "While you were away" card with the coins and swords sold.
- Her pad's line: "Sells your swords while you're away (up to 2 h)".
- Questions: sell the stock you left (above), or a flat share of your recent income? Cap 2 h? Later, a pass for a longer cap?

### More etches for gems (Allen likes it)

Today: three etches bought with coins on pads by the Etching Table (Flame 800, Woven Wind 8,000, Fracture 40,000). Proposal: **three more on pads beside them, priced in gems** (like Showcase Stands 2 and 3), from the retired patterns (Eclipse, Tide, Stormroot, Falling Stars).
- Questions: pads (as the coin etches), or in the Gem Shop? Which three? Bonus a step above Fracture's +25%, or the same and they're just looks?

### The Wandering Swordsman's daily designs (proposal)

- **Musashi** (already "the Wandering Swordsman" who sends letters) sets up a stall by your shop. Each day he offers **3 unique blueprints**, each priced in coins **or** gems (say two coin, one gem), learned forever once bought.
- **Rotation, not one-time:** each design comes back in a later day's stock, so a kid who misses one isn't locked out (Roblox: no pressure on minors; real timers that don't restart). His sign says when the stock changes.
- **Content cost:** each design is a new blade profile and hilt (BladeCore, Blender), so the pool size sets the build. 6–9 designs is enough for a rotation that doesn't repeat often.
- **Not the secret swords:** gag swords stay never-bought (surprise letters); his designs are real swords.
- Questions: Musashi? 3 a day? What a design gives: higher value, a Book page, or looks only? Coin/gem split? Which designs first?

### Allen's picks (2026-11-09, later)

- **Weathers:** free rotation + buy.
- **Ore pack:** found Legendary metals only.
- **Offline:** a share of recent income (not the stock left), with the Cashier.
- **Gem etches:** pads by the Etching Table.
- **Musashi:** yes; designs sell for more and get a Book page; they come back later; a new stock **every 3 hours** (Allen: "it should probably be by some hour not a day, maybe every 3 hours?").

Recorded in the [[Design/Decisions Log]]. Not built.

## Grow a Garden's restocks, and what fits Musashi (research 2026-11-10)

Allen: "for the wandering swordsman, can you look up how Grow a Garden does their restocks, they have a good system i want to copy, but they also have multiple things that are stocked at different prices, see which one applies to our game."

**How Grow a Garden stocks its shops** (fan wikis and guides; their numbers disagree, so treat them as approximate):

| Shop | Restock | How the stock is picked | Prices |
|---|---|---|---|
| Seed Shop (Sam) | every ~5 min | each seed rolls its own chance by rarity (Carrot ~always, Beanstalk ~0.03%), with a quantity; the same stock in every server; one player's buy doesn't take yours | Sheckles, 10 to 70M by rarity; a Robux restock 39–79 R$ |
| Gear Shop (Eloise) | ~5 min | the same, with quantities (Watering Can 1–4) | Sheckles or Robux each (Watering Can 50k / 39 R$) |
| Egg Shop (Raphael) | 30 min | eggs (random pets inside) | Sheckles; restock 90 R$ |
| Cosmetics (Isaac) | 4 h | rotating | Sheckles |
| Travelling merchants | may come every 4 h on the clock (00, 04, 08… UTC), stay 30 min | themed; each item its own stock chance (Summer Seed Merchant: Cauliflower 33% … Feijoa 0.15%) | Sheckles or Robux each (135–1,215 R$) |

**What carries over to Musashi:**
- **The Seed Shop's stock rules, on Allen's 3-hour clock.** His stall is always there. A new stock every 3 hours on the clock, the same in every server, so a "Musashi has new swords!" banner can go out everywhere at once, and his sign counts down. Each design rolls its own chance by its rarity: common designs nearly every stock, legendary ones rarely, which gives a reason to check back.
- **Different prices by tier** (the "multiple things at different prices"): cheaper designs for coins, the rarer ones for gems.
- **Per player:** your buy never takes a design from anyone else.
- **No quantities:** a design is learned forever, so it's "in stock" or not, and one you own shows Owned.
- **Not the travelling merchants' 30-minute visits:** with a 3-hour gap most sessions would miss him. Keep him always there, with the stock changing.
- **Not copied:** eggs (random contents: paid random items) and a **Robux restock** (paying to re-roll a random stock is close to a paid random item, and it would sell around gems). Robux buyers reach gem designs through gem packs.

Example tiers to tune: Common in ~90% of stocks (coins), Rare ~40% (coins), Epic ~15% (gems), Legendary ~4% (gems, about once a day across 8 stocks). Pool and prices open.

Sources: [allthings.how](https://allthings.how/grow-a-garden-2-stock-predictor-how-restock-timing-works/) · [Gamezebo seeds](https://gamezebo.com/walkthroughs/grow-a-garden-seeds) · [Nerdschalk restock times](https://nerdschalk.com/grow-a-garden-2-shop-restock-times/) · [Nerdschalk seed stock chances](https://nerdschalk.com/?p=504076) · [TheGamer merchants](https://www.thegamer.com/roblox-grow-a-garden-complete-travelling-merchants-items-timer/) · [DroidGamers merchant times](https://www.droidgamers.com/guides/grow-a-garden-traveling-merchant-times/) · [Sportskeeda Beanstalk](https://www.sportskeeda.com/roblox-news/how-often-beanstalk-restock-grow-garden). The DevForum post reverse-engineering the stock system was down (maintenance).

---

Related: [[Design/Monetization Plan]] · [[Design/Monetization Ideas — 2026-10-31]] · [[Design/Monetization Review — 2026-11-08]] · [[Design/Decisions Log]]

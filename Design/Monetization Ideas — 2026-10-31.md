---
title: Monetization Ideas — 2026-10-31
type: design
status: proposed
updated: 2026-10-31
tags: [monetization, robux, game-pass, developer-product, weather, crew, gifting, private-servers, create-swords]
---

# Monetization Ideas — 2026-10-31

From Allen's 2026-10-31 bullets at the end of [[Refinements]] and his evening ask, "brainstorm for more monetization strategeis. more convenience features" ([[Sessions/2026-10-31#Refinements, Allen's new notes and the big review (evening)]]). **Proposals only:** nothing here is built or decided, nothing was changed in Studio, and no price or product moved on Roblox. It builds on [[Design/Monetization Plan]] (its §7 rules and §8 "left out") and checks every idea against the [[Design/Decisions Log]] and the [[Archive/Design/Urgency Review#5. Guardrails|Urgency Review guardrails]]. Pace numbers come from the vault's simulator, run this session (§5).

## The short version

**Build next (top 5):**
1. **Bought weather** (the plan's §3): Sunshine and Snow first, then Rainbow, Rain last (it needs the odds panel). 79 R$ or 60 gems, for the whole server, the buyer named at the weather icon. It's the server-wide boost note (a) reaches for, and it's already designed.
2. **Paid private servers**, 99 R$ a month: a Creator Hub switch once the game is public. Roblox Plus members get them free, and Roblox pays up to 100 R$ a month for each Plus member who plays an hour in one.
3. **Fireworks over your shop**, 19 R$ each: a 20-second show everyone in the server sees. Fun, no power.
4. **Slash trails**, 49 R$ pass: a fire, frost or rainbow trail when you swing a sword. Style other players see.
5. **Gifting**: buy any pass for a Roblox friend in your server, at the pass's price. Only ever on the buyer's initiative.

**Allen's four notes:**
- **a. Crew XP or delivery XP boost: don't.** Crew levels already come from work and from gems (20 / 55 / 105 / 200), so a boost would be a third way to the same effect. Simulated, even a permanent 2× crew XP adds only 1–3% coins by 6 h. There is no delivery XP: delivered swords give reputation (Rank), which good players max by about 2 h and which only changes cart orders.
- **b. More places to offer:** pills in the station HUDs (anvil, polish), the weather icon, the crew card, gift buttons, a fireworks crate, and owned items that visitors can see. No offers after a great roll, at a full rack or during a long save.
- **c. Convenience impulse buys:** nearly every chore is already sold (rolling, striking, walking), a crew job, or ruled out. One is left: **Auto Polish, 49 R$** (Allen's call). The rest of the cheap shelf should sell fun, not time: fireworks, trails.
- **d. Auto Anvil at 49 R$: keep 49.** It sells comfort, not speed. It isn't on the Shop page yet.

**Fix the Shop page first** (§4): add the Auto Anvil card, plain effect lines, owned passes to the end, and VIP's price and name.

## 1. What successful Roblox games sell (2025–2026)

The fan sources are thin and their prices drift; treat single prices as examples, not a market rate.

| Game | Item | Price | Source |
|---|---|---|---|
| Steal a Brainrot | Server Luck: the whole server's luck 1× → 2× → 4× → 5×, stacking | 249 R$, then 999 R$ a step | Sportskeeda, fan guides |
| Steal a Brainrot | VIP · 2x Money | 499 · 299 R$ (one guide says 119) | Deltia's Gaming, U7Buy |
| Grow a Garden | Season Pass premium · skip a tier · skip the season | 749 · 49 · 1,699 R$ | Sportskeeda, Deltia's Gaming |
| Grow a Garden | Gift Shop: seeds bought for other players with Robux; hold-to-gift crops | — | Deltia's Gaming, TreyEx |
| Blox Fruits | Gifting of passes and permanent fruits, to other servers, with a message (Update 24) | the item's price | Blox Fruits Wiki |
| Fisch | Emote Pack · Sell Anywhere · Appraiser's Luck | 99 · 399 · 399 R$ | Pocket Tactics, Sportskeeda |
| Pet Simulator 99 | VIP · Ultra Lucky | 400 · 800 R$ | Filibuster Blog, U7Buy |
| Restaurant Tycoon 3 | Starter pass · 350 cash | 25 · 99 R$ | RT3 Wiki, a guide |
| War Tycoon | 2X Cash | 399 R$ | Sportskeeda |

**Price bands:** impulse passes 50–100 R$, convenience (speed, auto-collect, storage) 50–150, VIP 200–500, with fewer buyers past 500 (RoWatcher 2026, figures unsourced). The LihFolk vault's rule of thumb: impulse under 100 (75, 79, 99), core 150–600, premium 700–1,500; prices end in 9; leave room between rungs.

**Platform facts** (Roblox docs unless marked; as of October 2026, recheck before shipping):
- You get 70% of a price. **Roblox Plus** members pay 10% less for their first two months and 20% after; Roblox pays the difference, so earnings don't change. That is probably the "about 10% less" Roblox quoted Allen's account (plan §11), not a pricing setting.
- **Plus sign-up bonus:** 250 R$ a month for a new subscriber's first three months, when they subscribe through the game's own prompt (`PromptRobloxSubscriptionPurchase`).
- **Private servers:** free, or a monthly Robux price; only once the game is public. Plus members get paid ones free and you earn 70% of your price, at most 100 R$, for each Plus member who spends 60+ minutes in theirs over 30 days (if it's among their five most-played paid servers). Changing the price cancels every subscription. Players under 13 may not be able to join one, depending on parental settings.
- **Experience subscriptions:** $2.99 / 4.99 / 7.99 / 9.99 / 14.99, or 49+ R$ a month; the same benefits on every platform; no Bronze/Silver/Gold tiers; benefits for the whole term.
- **Promoted passes:** some players who buy Robux get your pass free and are asked to join the game to claim it. The pass needs a thumbnail, no paid random items, and (if on sale) a price over 49 and under 801 R$. **Listed** passes also show on the homepage and in search; both need an icon.
- **Robux transfers** through a game (Plus members, 10–500 R$ each, 10% to the creator; age rules and parental consent apply).
- **Rewarded video:** only users 13+ see the ads; the game needs 2,000+ monthly visitors and an approved questionnaire (LihFolk vault, October 2026 docs; the August 2025 DevForum post asked for 100K DAU). March 2026 reports say rewarded formats are barred for under-13s.
- **Creator Rewards replaced Premium Payouts on 2025-07-24:** 5 R$ a day per Active Spender who plays 10+ minutes when the game is one of their first three that day, and 35% of a new player's first $100 when they came by your link. The plan's §9 line on Premium Payouts is out of date.
- **Managed Pricing** (2026-06-15): regional prices and price tests in one opt-in; a test runs about three weeks and keeps a new price only if revenue rises. Roblox reports +4–10% spend from regional prices and +4% on average from price tests. It's off for items made through Open Cloud (a release blocker already).
- **Paid random items:** every outcome's odds before buying; luck boosts explained in numbers and the odds updated while active; restricted players handled through `PolicyService`.
- **Kids:** parents of under-13s can set monthly spending limits (Roblox Help). Since June 2026 Roblox Kids (5–8) and Roblox Select (9–15) accounts see only reviewed games rated for them (Kinzoo, third-party).
- **EU consumer authorities' key principles on in-game currencies** (2025-03-21, not binding): real-money prices clear, nothing that exploits children (Reed Smith summary).

**Roblox on selling to kids:** its monetization guide asks creators to "avoid using pushy or urgent messages when interacting with minors". It also says players must never be misled, confused or pressured into a purchase; countdown timers must be accurate and never restart; a discount isn't genuine if the item is always on sale.

**Ethical tactics that convert:**
- Offer the thing where it's used (the roller's bar, the anvil's pill), not in a popup. The LihFolk vault calls contextual offers the strongest converter.
- Keep a real impulse rung under 100 R$ (the 9 and 19 R$ packs, the Auto Anvil).
- Offer the first purchase after a success (the Starter Pack after the tutorial, as built).
- Put honest numbers on cards, with bonus labels computed from the real amounts.
- Let ownership be seen: visitors watch your motor crank, your fireworks go up, your weather carry your name.
- Gifting, on the buyer's initiative only.
- Let Roblox test prices (Managed Pricing) rather than hand-made duplicate products.

**Dark patterns to keep out:** fake or restarting timers; confirm-shaming; offers on join or after a loss; near-misses on paid rolls; loss-framed upsells ("you'd have earned 620 more"); top-spender boards; gifting pressure ("your friend wants this"); paid streak restores.

## 2. Allen's four notes

### a. "a server-wide (or player only?) boost for employee xp, or delivery xp"

**What exists:**
- **Crew levels:** Lv. 2–5 at 10 / 30 / 70 / 150 swords (staff need 2.5× the jobs). A crafter gains 8% quality a level and forges faster (Taise 30 → 15 s), so Taise's swords go from ×1.0 (Lv. 1–2) to ×1.3, ×1.7 and ×2.0 at Lv. 5.
- **Levels for gems:** 20 / 55 / 105 / 200 (2026-10-30, Allen: "Crew levels increase those gems cost by 1/3"). Today's crew bars and the level-up prompt by the employee put that shortcut where the crew is.
- **No delivery XP.** The cart's Capacity and Speed are coin levels in the Deliveries window. Each delivered sword gives 1 reputation point (a sale 1, an order 3, a commission 5); 8 ranks run from 0 to 175 points, shown only as "Rank N" in that window. Since 2026-10-27, rank no longer speeds walk-ins. What it still changes (Shared/Orders, mirrored in the sim): from Rank 4 a Special Order may ask for Rare metal, and from Rank 5 cart orders pay one more gem.

**Simulated** (§5):
- A permanent 2× crew XP (every level at half the swords) changes nothing before the Sword Crafter and adds 1–3% coins by 6 h (casual +1%, efficient +3%, grinder +2%, manager +3%).
- Reputation: Rank 5 by about 1 h for every type. Efficient, grinder and manager players reach the top rank (8) by 2 h; casual players are at Rank 6. A reputation boost would have nothing left to speed up after the second hour, and before that it would mostly bring Rare-metal Special Orders sooner.

**Server-wide or personal:**
- **Server-wide** feels best: generous, the buyer named, fair, since everyone gains. But crew come with the Sword Crafter, at about 1:50–2:20 for good players and 4:20 for casual ones (sim), so in a six-plot server many plots have no crew yet, and that part of the gift lands on nobody.
- **Too short to feel:** a crafter makes a sword every two minutes or so, so a 5-minute 2× gives each one two or three swords' XP. It would need 30–60 minutes, which doesn't fit the weather's 5 minutes, the game's one format for server-wide boosts.
- **Personal, priced against gems:** a 30-minute 2× would add about 20–35 sword-XP for a workshop with two or three crafters (the sim's crew make 45–70 swords an hour at 2–4 h). That's about 55–90 gems of levels, or 50–110 R$ at the gem packs' rates, but well under 1% of the session's coins. At a price that matches gems it's poor value; any cheaper and it undercuts the gem levels Allen just built.
- **Showing it:** server-wide on the weather icon with the buyer's name; personal as a chip on the Crew button. Either is new UI for a small effect.

**One system per effect:** crew levels already have two paths, work and gems; a boost adds a third. Allen's precedents: the Lucky Roller removed because merges gave luck, the Auto Cashier left out because the Cashier is a hire, instant heat left out because it competes with Faster Heating.

**Recommendation: build neither.** For a server-wide Robux moment, build bought weather (plan §3), which already names its buyer. For crew, the gems shortcut by the employee is the paid path. If Allen still wants a crew event, the clean shape is a fifth weather ("Festival": crew XP ×2) in the free rotation and the weather shop. That keeps one system for server boosts, but it would be the weakest weather and make the others rarer.

### b. "more in-game ways to prompt players to buy things"

Six world spots are being built ([[Design/Refinements Proposals — 2026-10-30]] §2). Beyond them, these places keep the rules: where the player already is, after the tutorial, and nothing opens by itself.

| Where | What it offers | Why it fits |
|---|---|---|
| The anvil's HUD | Auto Anvil: a pill like Auto-Roll's, locked until owned (`AnvilHud.Auto` is in Studio) | At the station, in its HUD, not a menu |
| The polishing HUD | Auto Polish, if Allen wants it (§2c) | Same pattern |
| The weather icon, bottom left | Tap: the bonus and time left (as now), then "Change the weather" for gems or Robux | The player opens it |
| Each crew card | Outfits (if the Crew Wardrobe is made), next to Level up | Style, where the crew lives |
| A fireworks crate by the shop sign | Fireworks, 19 R$ | Allen: "players are more likely to buy something they can see in the game" |
| Shop cards | A Gift button (if gifting is made) | Buyer's initiative |
| Other players' plots | Nothing to tap: their motor cranks, their chest is full, their sign glows | A neighbour's bigger build is the advert (LihFolk tycoon playbook); prompts stay on your own plot |

Allen's three examples, checked:
- **A full rack:** the free fixes are there (stock the shop, Sword Rack 2, the Stocker), and the covering coin pack already appears when you tap a pad you can't afford. An offer on the full rack itself would sell around a pad. Don't.
- **A long wait:** the 20–30 minute saves after the Zanbatō are a known design gap ([[Development/Sim Runs/pacing-check-2026-10-30]]). An offer there is what the LihFolk vault calls pain-to-pay. The fix is things to buy in the 5–11 h window; the covering pack on a tap stays.
- **After a great roll:** don't. Lucky Ore is a paid random item, and the LihFolk notes call the moment right after a big roll the most ethically loaded in RNG games. The roll's own show is the reward.

**A rule to restate:** the plan says offers appear "never during the tutorial, a weather or an offer's countdown" (plan §7). That was written when weather was a rare spell; since Fixes2 a weather is always on, so read literally it forbids every offer. Suggested: "No offer opens by itself, none sells more of the weather that's running, and none plays on a timer."

### c. "more convenience impulse purchases"

Every chore, and what takes it today:

| Chore | Taken by |
|---|---|
| Pulling the lever | Auto Ore Roller, 149 R$ |
| Collecting ore | You (Allen: "rolls only") |
| Heating | You; Faster Heating (instant heat left out, plan §8) |
| Striking | Auto Anvil, 49 R$ |
| Polishing your own swords | You (the crafter polishes its own) |
| Etching | The Sword Etcher |
| Stocking the shop | The Stocker |
| Answering offers | The Cashier (an Auto Cashier was left out, plan §8) |
| Walking | Swift Boots, 99 R$ |
| Cart trips | Too short to pay to skip (plan §8); Special Orders' 5-minute wait stops gem farming (2026-10-29) |

The only chore no pass, hire or ruling covers is polishing your own swords. So:
- **Auto Polish, 49 R$:** the stone works the blade by itself at hand pace while you watch, with the same result as a full hand polish; you can still polish by hand. No effect for a player who polishes anyway; one who usually skips it gains the polish bonus (+10–20%) on those swords. The risk is that polishing is one of the game's best feelings (the scrape, the value counting up), and a kid with both autos mostly watches. Allen's call.
- **The rest of the cheap shelf should sell fun, not time:** fireworks (19 R$), slash trails (49 R$), a shop name (49 R$). The 9 and 19 R$ packs already catch leftover Robux.

### d. "auto-anvil clicker that can be super cheap?"

- **The ladder today:** Auto Anvil 49 · Swift Boots and the Starter Pack 99 · Auto Ore Roller and Lucky Ore 149 · 50% More Coins 199 · VIP 299.
- **The market:** convenience passes usually cost 50–150 R$ (RoWatcher); the LihFolk impulse rung is under 100.
- **What it's worth:** nothing in pace, by design: strikes land at your own Faster Strikes pace and you stay at the anvil. The upper bound, an anvil you could walk away from (the player's anvil time ×0.25 in the sim), would bring the Sword Crafter 5–7% sooner and add 5–18% coins by 6 h. That's VIP's size of effect, and the Sword Crafter's job (the first employee, a 40,000-coin milestone) for 49 R$. Keep it "stand and watch".
- **Keep 49:** honest for comfort, the shop's cheapest pass and so a natural first purchase, with room below Swift Boots. Not lower: a pass sells once, and 25 R$ earns 17 R$. 49 sits under the promoted-pass floor (50), which only matters for a pass made for that pool.
- **Later:** if it outsells the others, let Managed Pricing test 79 R$ once the game qualifies, rather than changing it by hand.
- **Missing:** a Shop card (§4). Its line should say it doesn't speed you up: "Strikes for you, at your speed".

## 3. More ideas, ranked

| # | Idea | Price | Verdict | Build |
|---|---|---|---|---|
| 1 | Bought weather | 79 R$ or 60 gems | Build next | Medium |
| 2 | Paid private servers | 99 R$ a month | Build next (at release) | Tiny |
| 3 | Fireworks over your shop | 19 R$ | Build next | Small |
| 4 | Slash trails | 49 R$ | Build next | Small |
| 5 | Gifting passes to friends | the pass's price | Build next | Medium |
| 6 | A pass for Roblox's Buy Robux bonus pool | free to them | Soon | Tiny |
| 7 | Auto Polish | 49 R$ | Allen's call | Small |
| 8 | Crew Wardrobe | 149 R$ | Soon | Medium |
| 9 | A quiet Roblox Plus button | Roblox's price | Allen's call | Small |
| 10 | Name your shop | 49 R$ | Soon | Small to medium |
| 11 | Smith's Season (season pass) | free + 399 R$ | After launch | Large |
| 12 | Smith's Guild (subscription) | 499 R$ a month | After launch | Medium |
| 13 | Rewarded video | free (an ad) | When eligible | Small |
| 14 | Gold Workshop paints | 199 R$ | Later | Medium |
| 15 | Shop cat | 149 R$ | Later | Medium |
| 16 | Event cosmetics, earned or bought | 99 R$ | After launch | Medium per event |
| 17 | Comfort Pack | 249 R$ | Later | Medium |
| 18 | Nameplate frames | 49 R$ | Later | Small |
| 19 | Emote pack | 49 R$ | Later | Small |
| 20–33 | Fourteen ideas below | — | Don't | — |

### Build next

**1. Bought weather** (the four developer products, made 2026-10-27, off sale)
- **Does:** starts Sunshine, Snow, Rainbow or Rain for the whole server for 5 minutes (plan §3), the buyer named beside the weather icon; a bought one queues behind another bought one.
- **Offered:** the weather icon (tap it, then "Change the weather"), and a WEATHER row in the Shop.
- **Touches:** plan §3 and §7 (the "during a weather" wording above); the guardrail against "extend the rush" (a bought weather never extends one); Rain is a paid random item (the odds panel, `PolicyService`).
- **Pace:** one bought Sunshine is worth about 0.5–2 minutes of the buyer's income at 2–4 h, and the same for every shop in the server; a Rain or Rainbow is worth less than a minute; Snow's mail isn't simulated (§5). Fair for the buyer, generous to the server.
- **Risk:** low: one at a time, nothing during the tutorial, the buyer's name the only text.
- **Build:** medium: the picker, receipt → a server queue, the gems path; Rain's odds panel last.

**2. Paid private servers**
- **Does:** friends get their own server.
- **Price:** 99 R$ a month (Claude's suggestion). 143 R$ or more would earn the full 100 R$ per Plus member; 99 earns 69 R$.
- **Offered:** Roblox's game page (Servers); nothing in the game.
- **Touches:** plan §9 ("Allen's call").
- **Pace:** none.
- **Risk:** changing the price later cancels every server; under-13 settings may keep some kids out; decide whether the all-servers leaderboard counts private servers.
- **Build:** tiny, a Creator Hub switch once the game is public.

**3. Fireworks over your shop**
- **Does:** a 20-second show over your shop that everyone in the server sees; one show at a time per server (the next waits); none on a plot still in the tutorial.
- **Price:** 19 R$, a developer product.
- **Offered:** a fireworks crate by your shop sign (a world spot; one model per object) and a FUN row in the Shop.
- **Touches:** style only. The Settings Weather switch could hide fireworks too.
- **Pace:** none.
- **Risk:** noise → one at a time and short; keep the particles within a phone's budget.
- **Build:** small: a VFX template, the product, a server queue.

**4. Slash trails**
- **Does:** a fire, frost or rainbow trail behind any sword you swing (the `SwordSlash` combo), seen by everyone.
- **Price:** 49 R$, one pass with all three; pick one in Settings or on the card.
- **Offered:** the Shop's FUN row.
- **Touches:** style. The trail shows only during a slash, so it never reads as polish or an etch (effects follow state).
- **Pace:** none.
- **Risk:** low.
- **Build:** small: a Trail in the sword Tool, switched on by the server for owners so others see it.

**5. Gifting passes to friends**
- **Does:** a Gift button on each pass card: pick a Roblox friend in this server, pay the pass's price, and they get it. Both see who gave it.
- **Price:** the pass's own price (one developer product per pass: seven new products).
- **Offered:** Shop cards only.
- **Touches:** LihFolk ethics (gifting only on the player's initiative): no wish lists, no "X wants this", no notice to the friend before the gift. A gifted pass is save data, not Roblox ownership, so `Store.owns` must read both.
- **Pace:** the pass's own effect, for the friend.
- **Risk:** begging and "gift me back" deals among kids → friends in the same server only, no requests, a daily cap. The experience page's Store tab can still sell the real pass to someone who was gifted it (Roblox can't know).
- **Build:** medium: seven products, a gift record that survives the friend leaving mid-purchase, a friend picker, StoreService reading saved gifts.

### Soon or Allen's call

**6. A pass for Roblox's Buy Robux bonus pool:** some players who buy Robux get the pass free and are asked to join the game to claim it. Make it a cosmetic that exists only for this (a lantern banner for your shop). Free to them, so no Robux in, but new players. Needs a thumbnail and no paid random items. Tiny build: the cosmetic, a pass, and "Include this item in the bonus pool".

**7. Auto Polish,** 49 R$ pass: a lock pill on the polishing HUD like Auto-Roll's; see §2c. Touches nothing ruled; small build (the Auto Anvil's pattern).

**8. Crew Wardrobe,** 149 R$ pass: dress all your crew in one of six themes (samurai, ronin, pirate, knight and more), picked on each crew card; visitors see them. Style only. Medium build: catalog outfits applied to the crew NPCs, saved.

**9. A quiet Roblox Plus button:** at the bottom of the Shop, opening Roblox's own prompt; subscribers get a gold sheen on their anvil. Roblox pays 250 R$ a month for three months per sign-up through it, and Plus members pay 10–20% less for every pass (Roblox funds it). No popups, ever: it's a real-money subscription that parents pay. Small build.

**10. Name your shop,** 49 R$ pass: a hanging sign with a name made from preset words ("Iron Fox Forge"). No free text, so nothing to filter. Small to medium build.

### After launch or later

**11. Smith's Season (season pass):** four weeks; free and premium tracks (399 R$); points from the game's own verbs (forge 20 Katanas, serve 10 VIP buyers, send 5 carts). Free rewards: coins and gems. Premium: cosmetics and gems, capped at about three days of gem income. No paid tier skips. Touches "anyone can earn everything", so premium cosmetics need Allen's OK. Real end dates. Large build; worth it once there's a content cadence, since Roblox's recommendations now weigh 28-day retention and spend days. For scale, Grow a Garden sells its premium track at 749 R$.

**12. Smith's Guild (subscription),** 499 R$ or $4.99 a month: +15 gems each day you play (about 20% more than an engaged player earns), a new shop banner each month, a gold frame on your plot's nameplate while subscribed. Not hilt colours: a hilt's colour shows its tier and value. The same everywhere; no tiers. Medium build; after launch.

**13. Rewarded video:** watch an ad for 7 gems once a day. Players 13+ only, so it reaches a minority here; needs 2,000+ monthly visitors and the questionnaire. Small build.

**14. Gold Workshop paints,** 199 R$: gold anvils, a jade ore roller, copper furnaces. Rarity colours and callouts must stay readable. Medium build.

**15. Shop cat,** 149 R$: a cat that naps on your counter and follows you round your plot. Medium build (model and animations).

**16. Event cosmetics, earned or bought:** a seasonal shop banner or roller paint earned in the event week (deliver 20 swords), or 99 R$. Real end dates. Medium build per event.

**17. Comfort Pack,** 249 R$: Auto Ore Roller, Auto Anvil and Swift Boots (297 R$ apart). Awkward for anyone who owns one already, and Roblox can't bundle passes, so it would be a product granting saved ownership. Later.

**18. Nameplate frames,** 49 R$: a frame on your plot's nameplate, with others earned at milestones (first crew, Rin) so status comes from play too. Small build.

**19. Emote pack,** 49 R$: hammer raise, bow, sword salute. Small build.

### Don't

| # | Idea | Why not |
|---|---|---|
| 20 | Crew XP boost, server-wide or personal | §2a: a third path to crew levels; +1–3% coins at most |
| 21 | Delivery XP / reputation boost | §2a: rank maxes by about 2 h and only changes cart orders |
| 22 | Auto Collect at the roller | Allen: "rolls only" (plan §5) |
| 23 | Auto Etch, Auto Stock, Auto Cashier | The Sword Etcher, Stocker and Cashier hires (plan §8) |
| 24 | Skips: instant heat, finishing a cart trip, the Special Order wait | Plan §8; the 5-minute wait stops gem farming (2026-10-29) |
| 25 | Teleport to the shop, sell or answer offers from anywhere (Fisch's Sell Anywhere, 399 R$) | The walk between shop and workshop is the designed pull (Urgency Review) |
| 26 | More luck: Lucky Ore II, "next pull Epic+" | Plan §4: nothing else changes the odds or sells a random item |
| 27 | A second Starter Pack, a "Crafter Pack" | Allen: exactly one Starter Pack |
| 28 | Buyers-only etches or blade glows | Allen: "no buyers-only etch"; a glow would read as polish or etch value |
| 29 | Pads, racks, slots or crew levels for Robux | Sells the progression; gems and the covering pack already close gaps |
| 30 | Robux transfers through the game, tip jars, top-spender boards | Money between kids, spending status |
| 31 | Countdown bundles, comeback discounts, a doubled first purchase | Roblox's timer and discount rules; the Starter Pack is already the first-purchase deal |
| 32 | 2× Gems, a timed 2× Coins | Plan §8 |
| 33 | An offline-earnings boost | There's no offline income to boost; a new system |

**The ladder with the top ten added:** under 50 R$: the 9 / 19 R$ packs, fireworks 19, Auto Anvil, slash trails, Auto Polish and the shop name at 49. 50–100 R$: weather 79, Swift Boots, the Starter Pack, 80 gems and a private server at 99. 100–300 R$: Auto Ore Roller, Lucky Ore, the Crew Wardrobe and 20,000 coins at 149, 50% More Coins 199, 200 gems 229, VIP 149–299. 400 R$ and up: 100,000 coins and 500 gems at 449, 300,000 coins at 999.

## 4. The Shop page today

Read in Studio (Edit, read-only): `StarterGui.MenuGui.ShopWindow` and `StarterPlayerScripts.MenuController`. In order: the Starter Pack as a big gold card (first, gone once owned), then GAME PASSES, two wide (Auto Ore Roller, 50% More Coins, Lucky Ore, VIP, Swift Boots), then CURRENCY, four to a row (7, 15, 80, 200 and 500 gems, then 800 to 300,000 coins). Prices come from `GetProductInfoAsync`; owned passes say Owned; Lucky Ore's Buy opens its odds first and its card hides where paid random items are restricted; the Shop button's amber dot shows once a session until opened, after the tutorial, while the Starter Pack isn't owned. All of that is right.

Issues, most important first:
1. **The Auto Anvil isn't on the page.** `Shared/Store.PASSES.AutoAnvil` exists, but `ShopWindow…List.Grid` has no `AutoAnvil` card, and `MenuController` skips a pass without one. No script but `Shared/Store` names it yet; `AnvilHud.Auto` (icon, lock, switch) is in place, so its wiring may still be in progress.
2. **VIP looks like the worst deal.** A kid reads "+50% coins on every sale" for 199 R$ and "+10% on every sale, chat tag" for 299. Simulated, VIP brings the Sword Crafter 6–8% sooner, the Auto Ore Roller (149) 8–18%, Swift Boots (99) 5–7%. Lower it to 149, or give it a style perk worth 299. Its name also clashes with VIP buyers, More VIPs and the Rainbow, and the planned VIP rope at the door "where VIP customers come in" will read as "this pass brings VIP customers". Rename one of them (the pass as "Master Smith", say).
3. **"Luck one merge higher" means nothing before a first merge,** which comes at about 1:05–1:15 for good players and 2:40 for casual ones (sim). Say it in numbers: "Rare ores ×1.5". The odds panel shows the rest.
4. **Owned passes keep their place,** so after two buys the first row says Owned and what's left sits below the fold. On a phone the list shows about 273 px (the window at 0.7): the Starter Pack and one row. Move owned cards to the end.
5. **Order:** the first row is the Auto Ore Roller (149) and 50% More Coins (199), and the cheapest pass (Swift Boots, 99) comes last. Suggested: 50% More Coins and the Auto Ore Roller (the biggest helps), then the Auto Anvil and Swift Boots (cheap comfort), then Lucky Ore and VIP. Check it with the per-place funnel.
6. **Gems and coins share one grid,** and a row breaks mid-currency (500 gems sits with 800–5,000 coins). Use two headers, GEMS and COINS. The gem cards hide their only hint ("Spend on Upgrades"); one line under GEMS, "for Upgrades and crew levels", says what a kid can't see.
7. **The coin ladder's biggest jump is at 449 R$:** 100,000 coins give 223 coins a Robux against 20,000's 134, a 66% jump, while the other steps are 7–35%. The LihFolk ladder rule wants the jumps to shrink as the price rises, so the big pack doesn't make every other look foolish. For example, 100,000 → 80,000 coins.
8. **No item had an image on Roblox at the plan's last check** (plan, Open; not rechecked), so Roblox's purchase window and the Store tab show a blank icon, and passes can't be Listed for the homepage and search without one.
9. **Wording:** the Auto Ore Roller's "Pulls the lever for you" → "Rolls for you, stops at good ore"; VIP's "chat tag" → "gold name in chat".
10. **Before going public** (unchanged): Lucky Ore on the Store tab, Managed Pricing off on the Open Cloud items, the restricted-region ingot not built.

## 5. Sim estimates

**How:** `engine.Sim` from `Development/sim` with today's `balance.json` (exported 2026-10-31), 100 players a type (casual, efficient, grinder, manager), 6 h, seeds 1:0–1:99, medians. Each pass alone as an extra payer tier; crew XP ×2 = every crew level at half the swords; the walk-away anvil = the player's anvil visit ×0.25; a constant weather = one weather all game instead of the rotation. Run from Claude's scratchpad, so nothing in the vault's sim folder changed. Not modelled: the Auto Anvil (no pace change by design), crew levels for gems, Snow's mail clock. The sim owns the Starter Pack from minute 0; in the game it comes after the tutorial. One casual and one efficient player's buy orders were checked: stations within reach first, as a real player would.

**Sword Crafter (h:mm), and the change against free:**

| Type | Free | Starter Pack | Auto Ore Roller | 50% More Coins | VIP | Lucky Ore | Swift Boots | Crew XP ×2 | Walk-away anvil |
|---|---|---|---|---|---|---|---|---|---|
| Casual | 4:22 | 4:00 (−8%) | 3:35 (−18%) | 3:09 (−28%) | 4:03 (−7%) | 4:09 (−5%) | 4:10 (−5%) | 4:22 | 4:09 (−5%) |
| Efficient | 2:03 | 1:47 (−13%) | 1:49 (−11%) | 1:30 (−26%) | 1:55 (−6%) | 1:59 (−3%) | 1:56 (−6%) | 2:03 | 1:55 (−6%) |
| Grinder | 2:19 | 2:07 (−9%) | 2:00 (−13%) | 1:41 (−27%) | 2:08 (−8%) | 2:14 (−4%) | 2:10 (−7%) | 2:19 | 2:09 (−7%) |
| Manager | 1:48 | 1:37 (−10%) | 1:39 (−8%) | 1:16 (−30%) | 1:39 (−8%) | 1:45 (−3%) | 1:43 (−5%) | 1:48 | 1:43 (−5%) |

**Coins earned by 6 h, against free:** Starter Pack +4 to +11%, Auto Ore Roller +9 to +25%, 50% More Coins +56 to +104%, VIP +9 to +19%, Lucky Ore +7 to +9%, Swift Boots +5 to +13%, crew XP ×2 +1 to +3%, the walk-away anvil +5 to +18%. Per 100 R$, 50% More Coins and the Starter Pack do the most and VIP and Lucky Ore the least (Lucky Ore's real job is the book).

**One weather all game, coins earned from 2 h to 4 h against the rotation** (Sunshine 35, Snow 30, Rain 20, Rainbow 15):

| Type | Sunshine | Snow (no bonus in the sim) | Rain | Rainbow |
|---|---|---|---|---|
| Casual | +28.7% | −13.6% | −7.0% | −2.2% |
| Efficient | +17.5% | −9.6% | −7.8% | −5.2% |
| Grinder | +6.6% | −8.8% | −3.5% | −2.9% |
| Manager | +27.2% | −14.5% | −8.3% | −10.6% |

Against a no-bonus weather (the sim's Snow), Sunshine is worth +17–49% coins while it lasts, Rain +2–8% and Rainbow +5–13% (the free rotation as a whole: +10–17%). A bought 5-minute Sunshine in place of a free spell adds about 2.2 minutes of a casual player's income, 1.4 for efficient, 0.5 for grinder and 2.1 for manager players.

**Reputation and crew** (free, median): Rank 2 / 3 / 5 / 6 at 15 / 30 / 60 / 120 min for casual players; Rank 3 / 4 / 6 / 8 for the other three. Taise's level at 6 h: casual 3 (4 with crew XP ×2), the others 4 (5 with ×2). Gems earned by 6 h: casual 119, efficient 362, grinder 508, manager 424.

## 6. Questions for Allen

1. Build bought weather next, Sunshine and Snow first?
2. Restate "never during a weather" as "No offer opens by itself, none sells more of the weather that's running, and none plays on a timer"?
3. Private servers: paid at 99 R$ a month, free, or off?
4. VIP: lower to 149 R$, or keep 299 and add a style perk? And rename the pass, since it clashes with VIP buyers?
5. Which fun items: fireworks, slash trails, a shop name, the Crew Wardrobe, a shop cat?
6. Gifting passes to friends in the same server: yes?
7. Auto Polish, or keep polishing by hand?
8. A quiet Roblox Plus button at the bottom of the Shop: yes?

## Sources

- Roblox docs: monetization overview (selling to minors, timers, discounts) https://create.roblox.com/docs/production/monetization · passes, listing and promoted passes https://create.roblox.com/docs/production/monetization/game-passes · developer products https://create.roblox.com/docs/production/monetization/developer-products · subscriptions https://create.roblox.com/docs/production/monetization/subscriptions · private servers https://create.roblox.com/docs/production/monetization/private-servers · Roblox Plus https://create.roblox.com/docs/production/monetization/roblox-plus · Creator Rewards https://create.roblox.com/docs/creator-rewards · paid random items https://create.roblox.com/docs/production/monetization/paid-random-items
- Managed Pricing (2026-06-15): https://devforum.roblox.com/t/managed-pricing-one-system-for-better-pricing-and-earnings-growth/4684738 · rewarded video (13+): https://devforum.roblox.com/t/more-creators-can-now-use-rewarded-video-ads/3838678 · Roblox Plus launch: https://about.roblox.com/newsroom/2026/04/introducing-roblox-plus-subscription · https://tubefilter.com/2026/04/13/roblox-plus-creator-payouts
- Under-13 ads (March 2026 reports): https://wsau.com/2026/03/20/roblox-to-overhaul-ad-policies-introduce-revenue-sharing-in-2027/ · spending limits: https://en.help.roblox.com/hc/articles/4409558125460 · Roblox Kids and Select: https://www.kinzoo.com/blog/robloxs-new-kid-accounts-explained-what-parents-need-to-know-before-june · EU key principles on in-game currencies: https://www.reedsmith.com/en/perspectives/2025/03/qas-on-the-eu-consumer-protection-authorities-joint-guidance-paper
- Game examples: Steal a Brainrot server luck https://www.sportskeeda.com/roblox-news/how-often-secrets-spawn-steal-brainrot · its passes https://deltiasgaming.com/roblox-steal-a-brainrot-all-gear-and-game-passes · https://www.u7buy.com/blog/steal-a-brainrot-best-game-pass/ · Grow a Garden season pass https://www.sportskeeda.com/roblox-news/grow-garden-season-1-pass-all-tier-rewards-premium-price · https://deltiasgaming.com/?p=357417 · gifting https://deltiasgaming.com/?p=239851 · https://www.treyexgaming.com/how-to-gift-items-in-grow-a-garden/ · Blox Fruits gifting https://blox-fruits.fandom.com/wiki/Gifting · Fisch https://www.pockettactics.com/fisch-shop · https://sportskeeda.com/roblox-news/roblox-fisch-all-official-links-gamepasses · Pet Simulator 99 https://thefilibusterblog.com/explaining-the-vip-benefits-of-pet-simulator-99/ · https://www.u7buy.com/blog/pet-sim-99-vip-pass-is-it-worth-it-in-2025/ · Restaurant Tycoon 3 https://rt3.fandom.com/wiki/Shop · War Tycoon https://www.sportskeeda.com/roblox-news/5-best-gamepasses-use-roblox-war-tycoon · price bands https://rowatcher.com/news/roblox-monetization-strategies-that-actually-work-in-2026
- LihFolk vault (rules of thumb, ethics, offer design): Robux Price Points and Offer Design · Ethical Design and Player Trust · Genre Playbook - Tycoons · Discovery and Monetization Changes 2025-2026 · Subscriptions and Premium Payouts · Ads and Rewarded Video · Limited-Time Offers - Design and Ethics · Menu Archetypes - Shop Settings Codes Rewards

---

Related: [[Design/Monetization Plan]] · [[Design/Refinements Proposals — 2026-10-30]] · [[Archive/Design/Urgency Review]] · [[Design/Game Design Document#15. Monetization (Robux)|GDD §15]] · [[Development/Code Map#Shop page (2026-10-27)]] · [[Development/Sim Runs/pacing-check-2026-10-30]] · [[Sessions/2026-10-31]] · [[Refinements]]

---
title: Alignment Review — 2026-10-23
status: review — decisions waiting for Allen
type: design
updated: 2026-10-23
tags: [review, economy, roadmap, create-swords]
---

# Alignment Review — 2026-10-23

Allen: "It feels like we've been working all over the place on the project. Can we re-align, look at our vault, find out what's been done, what needs refining, what decisions need to be made, what features we're missing, what additional features we should consider, how we should balance the game/economy."

Sources: the current vault through [[Sessions/2026-10-23]], and the live constants read from the Studio place on 2026-10-23 (`Shared.Materials`, `Blueprints`, `Hilts`, `Customers`, `Upgrades`, `Orders`, `Reputation`, `Deliveries`, `GemUpgrades`, `Employees`, `Commissions`; `SmithyCore.swordValue`, `ShopService`). Nothing was played. Times per sword are estimates until a playtest measures them. Proposals here are not decisions until Allen picks them; record picks in [[Design/Decisions Log]] and the [[Design/Game Design Document|GDD]].

## The short version

- **The whole game exists; almost none of the last two days has been played.** 2026-10-17 to 10-23 built the craft, the shop, the first session, saving, board orders, reputation, deliveries, gems, the collection book and the first employee. The last full-loop playtest predates the map, workshop, loot box, saving and everything after. The biggest risk is an unplayed stack, not a missing feature.
- **The economy has a leak and a wall.** The leak: request-board orders refill the moment one is filled and pay more than the shop for any common sword, so the efficient loop skips the shop, haggling, polishing and etching. The wall: the katana is the last blueprint (about 10 minutes in) and the Gem Pommel the last fitting (15 swords), so sword value stops growing early, and the whole upgrade catalogue (43,175 coins) costs roughly 1–2 hours of play.
- **Optional care doesn't pay, and choices aren't choices.** Polish adds about 6% real value for its time; the best hilt is free, so it's always picked; the Knight's quality preference is always met, because every player sword is 100%.
- **The game is nearly silent.** The only sound in the place is the anvil's `Clang` (also used when the hilt seats). No music, ambience, sale, loot-box, furnace, polishing or interface sounds.
- **Suggested order:** [[#One playtest session]] → economy pass 1 ([[#Decisions waiting|decisions 1–5]]) → sound → the next blueprints and the first outside tradition → stocker and cashier → gem sinks, badges and a small public test.

## What's built

| Area | Built | Played? |
|---|---|---|
| Craft | Loot box (1–6 slots, collect before rolling) → heat (3 s until the first sword, then 10 s) → 12 guided strikes to 100% → drag-on hilt → optional polish (+10%) → optional etch (7 patterns, +15%, strong glow) | Last full loop before 2026-10-22 |
| Shop | Sword shelves and SwordTables, the offer bubble with its %, haggling, fair first sale, haggling lesson on sale 2, friends' avatars as customers | Partly (shelf and table seating) |
| First session | Guide line and arrow; Guard Captain's Wakizashi (any metal, 120); Ore Slot 2 and "Workshop open!"; Wandering Swordsman's Katana (300) | No |
| Progress | Session-locked saving of everything, upgrades rebuilt on any lot | Edit tests (`SaveSpec` 54/54) |
| Goals | Rotating board orders, reputation levels 1–8, collection book (39 entries), NEW metals, reward card, coins/reputation HUD | No |
| Growth | 24 tycoon upgrades incl. Faster Heating I–III and Lucky Roller I–III; Delivery Cart with Capacity and Speed; gems, the daily streak and the Gem Shop | No |
| Employees | Sword crafter at Anvil 2: hire, per-shape training, 70% → 100% over 30 swords | No |
| World | Six-lot walled town, Genshin-style lighting, FreeStylized textures, Autumn Terracotta shops, block mountains, street villagers; trees removed | Partly |
| Swords | Baked meshes, polish shine, katana koshirae, etch overlays | Earlier builds |

Details: [[Current Status]].

## The economy today

### Sword value

`base × metal × 2.0 (100% forged) × (1 + hilt + 0.06 seat + 0.10 polish + 0.15 etch)` (`SmithyCore.swordValue`). The seat bonus is always the full +6% since the drag seating (`HiltBenchController` sends three good taps).

| Blueprint | Base | Wooden grip | Iron (+10%) | Gem (+40%) | Gem + polish + etch |
|---|---|---|---|---|---|
| Tantō | 20 | 42 | 46 | 58 | 68 |
| Wakizashi | 45 | 95 | 104 | 131 | 154 |
| Katana | 110 | 233 | 255 | 321 | 376 |

Metal multiplies everything: Uncommon ×1.5, Rare ×2.5, Epic ×5, Legendary ×12 (a Legendary katana with everything: 4,514). The average metal is ×1.545, then ×1.654 / 1.790 / 1.954 with Lucky Roller I / II / III: +26% average value at III, the strongest income upgrade in the catalogue.

### Where coins come from

Customers (`Shared.Customers`): Farmer (half of walk-ins) opens at 70–95% of value, Adventurer (30%) 85–105% and ×1.25 on wakizashis, Knight (20%) 90–110% and ×1.25 on any 95%+ sword, which is every player sword. The average first offer is about 95% of value (102% on wakizashis). A decline brings a 5–15% raise at 30 / 45 / 50% odds; otherwise the customer leaves and the sword stays on display.

| Outlet, common katana | Pays | Also |
|---|---|---|
| Shop, first offer | ≈ 95% of value: 221 (Wooden) to 356 (Gem + polish + etch) | 1 reputation |
| Shop, holding out for a Knight | ≈ 125%: 291 to 470 | 1 reputation |
| Board order, plain katana | 365 at reputation 1, 415 at 4, 490 at 8 — for **any** katana (Wooden, unpolished, a 70% crafter sword) | 3 reputation, 1–3 gems, refills at once |
| Delivery | ≈ 1.1× the board per sword: 402 to 539 | 1 reputation a sword, gems; 150 s → 70 s trip |
| Commissions | 120 (Wakizashi), 300 (Katana), once each | 5 reputation |

*Changed by economy pass 1 (2026-10-23):* board orders now pay 1.2× the handed-in sword's value, with a new order every 3 minutes; deliveries pay 1.1× the packed swords' value (1.3× at first); a polished common katana with everything is 390.

### Where coins go

| Branch | Coins |
|---|---|
| Delivery: cart, Capacity 1–3, Speed 1–4 | 17,200 |
| Ore Slots 2–6 | 7,275 |
| Crafter: Anvil 2, hire, training | 4,800 |
| Lucky Roller I–III | 4,600 |
| Faster Heating I–III | 3,700 |
| Shop: racks, tables, Upgraded Store | 3,600 |
| Furnace 2, Ingot Rack, Finished Sword Rack, Polishing, Etching | 2,000 |
| **Total** | **43,175** |

Gems: the Gem Shop totals 345 (Better Advertising 25/60/120, More Clients 40/100). Faucets: the daily streak (90 a week), board orders (1–3 each), deliveries (more per trip).

### Pace

- **First session:** the first tantō sells for about 42, the Wakizashi request pays 120, Ore Slot 2 costs 75. Next purchases (Wall Rack 2 150, Polishing 250, Display Table 250) follow within a few sales. This part matches the design.
- **Katana:** learned after the third shop sale, around 10 minutes in (estimate). The Gem Pommel unlocks at 15 swords.
- **After that:** at an estimated 40 s a sword (55 s with polish and etch) a katana-maker earns about 600–900 coins a minute (average metal, Lucky Roller 0 to III), so the catalogue is gone in roughly 1–2 hours.

Estimates: 12 strikes at the client's fastest cycle (≈ 0.75 s, `ForgeCheck`) are about 9 s, plus the 3.6 s roll, pickers, the hilt drag and walking. Time one real sword in the playtest and redo these numbers.

## Balance findings

Ranked by how much they bend the game.

1. **Board orders beat the shop for every common sword.** They refill the moment one is filled (`ShopService.refillOrders`), pay about 1.5× a middling sword of the shape (`Orders.make`) and take the cheapest sword that matches: any metal, any hilt, any quality (commissions check 90%; orders check nothing). A Wooden common katana worth 233 fetches 365, gems and 3 reputation. So for commons (60% of rolls) the efficient loop is roll → heat → forge → hilt → board, with no display, customer, haggle, polish or etch; that alone lifts income about 8% at reputation 1 and 24% at reputation 8. The crafter's 70% katanas (worth 172 in the shop) fetch the same 365, and reputation and gems farm without limit.
   - *Proposal:* one new order every ~3 minutes up to the board's slots (2, or 3 from reputation 3) instead of an instant refill; pay 1.2× the handed-in sword's own value, so metal, finishes and quality count, plus the gems and reputation; deliveries the same at ~1.3×. The board becomes a steady bonus and a purpose, not a better shop.
   - *Built 2026-10-23* ([[Sessions/2026-10-23#Economy pass 1]]). The cart's 1.3× had no limit but the trip, so the leak moved there: decision 20 lowered it to 1.1× the same day.
2. **Value stops growing after about 15 swords.** The katana is the top blueprint and the Gem Pommel the top fitting; afterwards only Lucky Roller and the crafter raise income. With no prestige reset (decided 2026-10-22), growth has to come from content: blueprints bought with coins and traditions brought by commissions, both decided directions and neither built.
   - *Proposal:* continue the base-price ladder (20 → 45 → 110 is about ×2.2–2.4 a step) with 2–3 more Japanese blades bought for ~20–30 minutes of income each, then the first outside tradition by commission at a reputation level. Set the target length first (decision 7).
3. **Optional care doesn't pay.**
   - Polish's +10% is added to the other bonuses, so on a Gem-hilted, etched sword it adds 6.2% (9.4% on a bare one). If a polish takes 10–15 s of a ~40 s sword, polishing lowers coins per minute. Etching (+15% for a ~3 s show) about breaks even. This is [[Design/Core Loop Review#Proposed refinement 4: make optional care a real choice|Core Loop Review refinement 4]] with live numbers.
   - Hilts are free once unlocked, so the best one is always right, and after 15 swords the hilt picker is a click-through.
   - The seat's +6% is a hidden flat bonus on every sword.
   - *Proposal:* polish multiplies the whole value by 1.10 (on a Legendary katana +425 coins rather than +264); customer tastes give finishes and fittings a reason (finding 4); fold the seat bonus into the base price or drop it.
   - *Polish ×1.10 built 2026-10-23.* Tastes and the seat bonus are still open.
4. **Customers have no real tastes.** Three personalities; the Adventurer likes wakizashis, and the Knight's 95% rule was written when forging ended at 90%, so now it likes everything: a flat ×1.25 on 20% of walk-ins. With the % on the bubble, "decline until it's green" is safe (the sword stays up and the next customer comes within 12–22 s) and earns about +30%.
   - *Proposal:* each regular likes one thing the player can choose to make (a blueprint, a rarity, polished, etched, a plain or ornate hilt) and shows it before offering. That gives polish, etch, fittings and display choices a purpose, and starts pillar 3 ("Every customer is a little story") ahead of familiarity and letters.
5. **Some upgrades change nothing you can feel yet.**
   - Customers rarely limit income: about 3 walk-ins a minute against ~1–1.5 swords a minute. Only a player holding out for the best offers runs short of customers. For everyone else, Better Advertising, More Clients, reputation's shorter walk-ins and extra holders (Wall Racks 3–4, Display Table 2, much of the Upgraded Store) barely change income.
   - With one anvil the player is the limit: Ore Slots 3–6 (7,200) mostly add ingots to carry (6 in hand, 12 on the rack, no way to discard), and Faster Heating (3,700) and Furnace 2 only help a player who waits at the furnace instead of loading the next ingot.
   - These start to matter once the crafter shares the furnaces and the Ingot Rack. *Proposal:* put Ore Slots 4–6 and Faster Heating II–III after Anvil 2; give the Upgraded Store a felt effect (the cashier is already decided for it; a special-visitor chance or +1 customer at once); add a scrap bin that buys unwanted ingots back for a few coins, below their crafting value ([[Design/Core Loop Review#Proposed refinement 3: upgrades should improve a felt limitation|refinement 3]]).
6. **Gems have no long-term sink.** An order-farming player clears the 345-gem shop in a few hours, then gems pile up. GDD §10.1's Lucky Rolls and timer skips don't exist, so Robux gem packs would have nothing to buy.
   - *Proposal:* add sinks before Robux: a Lucky Roll (one boosted pull), skipping a heat or a delivery trip, cosmetic etch patterns, later VIP visitors. The order timer (finding 1) also caps the faucet.
7. **Reputation maxes quickly and unlocks little.** Level 8 needs 175 points, about 58 orders. Levels shorten walk-ins, open the third order (3), Rare orders (4) and +1 order gem (5); levels 6–8 add nothing else. Special visitors, the designed reward, aren't built (decision 10).
8. **The crafter fits, but strands its swords.** At level 1 its katanas are worth half a player's (70% → ×1.0 against ×2.0); it reaches 100% after 30 swords. On common katanas it earns roughly 160 coins a minute at level 1 and 460 at the top, so its 4,800 coins pay back in about 15–25 minutes. Its swords stop on the 6-sword Finished Sword Rack until the player carries them: the stocker is the natural next hire.

### How to balance from here

1. **Pick the length** (decision 7) and a pacing rule: early purchases every 1–3 minutes, mid-game every 5–10, late every 15–30.
2. **Grow income mainly through blueprints** (each about ×2.2 the last), then luck and employees. Price each purchase as minutes of the income a player has when it unlocks.
3. **Give each outlet its own job.** The shop pays best for well-made swords that match a customer's taste; the board gives steady small goals, gems and reputation on a timer; deliveries take bulk commons on a trip.
4. **Measure, then tune.** Time real swords (roll to sale, with and without polish); log every coin and gem source and sink with `AnalyticsService:LogEconomyEvent` before the first public test (none is logged today; only the onboarding funnel); rerun these numbers from the live modules.

## What needs refining

Built, but not right yet:

- **The unplayed stack:** [[#One playtest session]] covers the Play checks scattered through [[Development/Roadmap]] §1–§6.
- **Audit leftovers** (Roadmap §1): polishing has no gamepad input; stroked etches on the Finished Sword Rack rebuild in one frame; `EtchCanvas` keeps its pixel buffers; the polish save rebuilds an etch in one frame.
- **No goal after the tutorial:** the guide stops once its lessons are done; after Ore Slot 2 and the katana nothing names a next goal ([[Design/Core Loop Review#Proposed refinement 1: lead the next craft with a purpose|refinement 1]] asks for one pinned goal).
- **Offers during crafting:** the bubble's 20 s runs while you're in a station camera, so a customer can walk off mid-forge ([[Design/Core Loop Review#Proposed refinement 6: remove interruptions and preserve active crafting|refinement 6]]).
- **The Genshin look only lives in `build_style_test`:** rerunning a builder brings back the old look (Roadmap §2).
- **Hilt names:** the six Japanese koshirae still carry the old ladder's names (Iron Crossguard, Gem Pommel).
- **Small art fixes:** the etch strip seam (inset the overlay UVs half a texel and re-bake); the shop lanterns don't match the village's.
- **Sound:** one sound in the place.
- **Studio tidying:** loose items at the Workspace root (12 `Bamboo` models, `AuxScene`, two `Courtyard`s, a `Lighting` folder, `MaterialDemo`, `Weapon Rack`) — Allen's to keep or file; `ServerStorage.Legacy` holds 222 backups (about 60,000 instances).

## Decisions waiting

Recommendations are Claude's; the choice is Allen's. 1–5 unblock economy pass 1; 7–8 unblock the next content. **1–3 and 20 were decided and built on 2026-10-23** ([[Sessions/2026-10-23#Economy pass 1]], [[Sessions/2026-10-23#Cart pay lowered to 1.1×]]); 20 came out of building 1–3.

| # | Decision | Recommendation |
|---|---|---|
| 1 | Board orders: instant refill (then) or one new order every few minutes? | **Decided 2026-10-23:** one every ~3 minutes |
| 2 | Order pay: flat estimate (then, ≈ 1.5×) or a multiple of the handed-in sword's value? | **Decided 2026-10-23:** 1.2× its value; deliveries 1.3× |
| 3 | Polish: +10% added to the other bonuses (then, ≈ +6% real) or ×1.10 on the whole value? | **Decided 2026-10-23:** ×1.10 |
| 4 | Hilts: free and always the best (today), preferred by some customers, or a coin cost per fitting? | Customer preferences; per-fitting costs only if a coin sink is still missing later |
| 5 | Customer tastes: what can a regular like? | One visible like each: a blueprint, a rarity, polished, etched, a plain or ornate hilt |
| 6 | Gem sinks? | Lucky Roll, heat or trip skip, cosmetic etches |
| 7 | How long should the first expansion last (to the last blueprint and upgrade)? | About 8–10 hours (today about 1–2) |
| 8 | Blueprints after the katana: which, how many, bought or by commission? | 2–3 Japanese blades bought with coins (e.g. tachi, nodachi, ōdachi), about 20–30 minutes of income each. **Allen 2026-10-23:** more Japanese blades look too alike. Prefer clearly different silhouettes; see [[Design/Sword Profile Ideas#Suggested order]] (still open) |
| 9 | The first outside tradition, and who brings it? | A visiting knight with a longsword; western fittings come with it |
| 10 | What each reputation level unlocks? | 4: the first special visitor; 5: the outside commission; 6–8: rarer visitors and better offers |
| 11 | Next employee: stocker or cashier? | Stocker (the crafter's rack fills at 6) |
| 12 | Retire the smith / finisher / furnace-operator split and the bare-blade rack, now the crafter makes whole swords? | Yes: more crafters (Anvil 3…), then stocker, cashier and ore attendant |
| 13 | Street: earth with a stone path (live) or tidy cut stone? | Allen's eye ([[Random thoughts]]) |
| 14 | Trees: when, and in which look? | After the playtest; parked since 2026-10-22 |
| 15 | `AnvilV2`: still wanted, now the fantasy anvil is in? | Drop the roadmap item |
| 16 | Genshin look: fold it into the builders or keep the switch? | Fold it in |
| 17 | Japanese names for the six hilts? | Allen's pick |
| 18 | Pause new features until one full playtest session? | Yes |
| 19 | Commit the vault? Everything since `3200add` (2026-10-22) is uncommitted, including new models and references | Yes, once reviewed |
| 20 | The cart pays 1.3× for any sword with only the trip as a limit (2–3 swords per 150 s trip before upgrades; offers refill at once), so it beats the shop's average first offer (≈ 95%) for every sword. Lower its pay, or throttle its offers like the board? | **Decided 2026-10-23:** lowered to 1.1×, above a first offer and below a patient or liked sale, so the shop keeps its job |

## Missing features

Designed in the GDD or roadmap, not built:

| Feature | Designed in | Note |
|---|---|---|
| Special visitors gated by reputation; an early outsider | GDD §7, §9 | The reward reputation was meant to give |
| Familiarity, letters, personal commission chains | GDD §7, §9 | Pillar 3 |
| More blueprints; outside traditions with their own fittings | GDD §6.2, §6.5 | Finding 2 |
| Stocker, cashier, ore attendant, employee management window | GDD §8, §10.4 | The cashier unlocks with the Upgraded Store (decided) |
| Weather traffic bonus | GDD §7 | Little effect while customers aren't the limit |
| Per-factor value breakdown | GDD §6.4 | The reward card shows only the last step's gain |
| Storage upgrades | GDD §10.2 | Racks fixed at 12 ingots and 6 swords (the Ingot Rack holds 6 full-size ingots since [[Sessions/2026-10-23#Racks split, one ingot model, NPC walking, no offer ping]]) |
| Collection milestones paying gems | GDD §10.1 | The book has no reward |
| Gem sinks: Lucky Roll, timer skips | GDD §10.1 | Finding 6 |
| Robux: gem packs, 2× Coins, Auto Cashier, VIP Rack | GDD §15 | No `MarketplaceService` code yet |
| Offline earnings | GDD §10.4 | Later, after online automation is balanced |
| Sound and music | Roadmap §4, §7 | One sound in the place |
| Gem Socket, Colour/Enamel finishes | GDD §6.3 | Scope check pending |
| Polishing on gamepad; manual etching | Roadmap §1; [[Random thoughts]] | Manual etching parked |

## Worth considering

Not designed yet; each is small next to the missing features above.

1. **A pinned next goal after the tutorial:** the next affordable upgrade, hilt milestone or commission, with progress.
2. **Badges** for the first sword, the first Legendary, every hilt, half and all of the collection book. None exist.
3. **A server message when someone forges a Legendary:** social proof across the six plots and more loot-box excitement.
4. **A masterpiece stand:** one sword kept on show, not for sale, with its maker's name; pride, and a reason to visit neighbours ([[Design/Core Loop Review#Proposed refinement 5: preserve the player's accomplishments and next project|refinement 5]]).
5. **Admire a neighbour's shop:** a like that gives its owner a little reputation; uses the six-plot social space.
6. **A daily special visitor** with one specific commission (say, an etched Starmetal Wakizashi): a daily reason to return beyond the gem streak, built from the existing commissions.
7. **A friends-in-server bonus:** a common Roblox growth lever that suits friends' avatars already being the customers.

## One playtest session

Covers the Play checks scattered through [[Development/Roadmap]] §1–§6. Save the place first; DevPanel's **Reset progress** gives a fresh player. Note what breaks, feels slow or confuses, and time one sword from roll to sale (with and without polish).

**A — New player**

1. Join: spawn in the workshop; guide line and arrow; nameplate over the plot; roofs fade inside.
2. Roll with one slot: the 3.6 s show, NEW and its card; collect.
3. Heat (3 s), forge the tantō, drag the hilt on, see the reward card; put it on a shelf (a held sword goes straight on); the first customer comes at once with the fair offer.
4. Guard Captain: accept, forge a Wakizashi of any metal, hand it in at the request board (120); two orders appear on the board.
5. Buy Ore Slot 2: "Workshop open!", then a two-ingot roll.
6. Sale 2: the haggling hint and a guaranteed raise. Sale 3: the Wandering Swordsman and the katana.
7. Fill a board order: 1.2× that sword's value, gems and the reputation bar move; the board shows "New order · in 3:00" and the order comes 3 minutes later.
8. Leave with an ingot in the furnace, ore on the lid and a blade half-forged; rejoin: the hot ingot in the bag, the ore as ingots, displays on the same holders, the guide where you left it.

**B — Skip ahead** (DevPanel **Skip tutorial**, DevTools coins)

9. Buy the shop chain up to the Upgraded Store while standing in the workshop (the 12-stud push); roof and ceiling fade; customers reach every holder; tantō, wakizashi and katana sit centred on shelves and tables.
10. Polishing Station and Etching Table: polish and etch an Obsidian or Starmetal katana; check it held, displayed, in the hotbar and on picker cards; open an inventory of etched swords and watch for hitches.
11. Faster Heating, Lucky Roller, Furnace 2, Ore Slots up to 6: full hands and the Ingot Rack.
12. Delivery Cart: an offer shows +10%; accept, pack (the card shows the coins), send, leave during the trip, rejoin, collect.
13. The crafter: Ingot Rack, Finished Sword Rack, Anvil 2, hire, train the tantō, stock ingots; watch it fetch, heat (use its furnace), forge, polish (stand at the stone), rack; fill the rack; leave mid-sword and rejoin.
14. Gems: the daily popup and a Gem Shop purchase; the collection book.

**C — Two players** (Test → Clients and Servers, 2 players)

15. Each gets a lot (N2, then N1) and spawns in their workshop; neither can use the other's stations or pads; both shops get customers; one leaves and their lot shows the empty plot; they rejoin onto a lot with their upgrades.

**D — Devices**

16. Touch (device emulator): pickers, hilt drag, polishing, offers, inventory drag. Gamepad: anvil R2/B, pads Y, offers Y/L2, hotbar R1/L1 (polishing has no gamepad input yet).

## Vault upkeep done with this review

Stale lines corrected in the living notes: the three hilt knocks (now the drag) in [[Current Status]], [[Development/Roadmap]] and [[Development/Code Map]]; "delivery not built" in Current Status, Code Map and [[Design/Tycoon Upgrades]]; the saved fields `reputation`, `orders`, `delivery` and `crafter` in [[Development/Saving]]; "persist upgrades" in Tycoon Upgrades; customers at once in Code Map; reputation in GDD §8. Dated reviews ([[Design/Core Loop Review]], [[Design/Pottery Tutorial Review]]) are left as written.

Related: [[Home]] · [[Current Status]] · [[Development/Roadmap]] · [[Design/Decisions Log]] · [[Design/Core Loop Review]] · [[Design/Workshop Growth]] · [[Design/Tycoon Upgrades]]

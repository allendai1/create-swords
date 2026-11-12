# Analytics Funnels

Built 2026-10-29. Allen: "look at where we can add funnels to our game, and also make sure the funnels can give us a better view of what needs improvement and similarly to our simulations, gives us better data to run our simulations."

Everything is logged on the server through `AnalyticsService`. Only live servers report: Studio Play sends nothing. The game is live and public on Swordsmith Tycoon since 2026-11-10. Related: [[Development/Gameplay Simulator Plan]], [[Development/Code Map]].

## How it is wired

- **One event vocabulary.** The services already call `PlaytestLog.log(player, kind, data)` at every step the simulator times. `PlaytestLog` now hands every event to `ServerScriptService.Analytics`, in Studio and in live servers. In Studio it still also posts to `receive.py` for `calibrate.py`.
- **`Analytics` turns kinds into dashboard events.** For example, `offer` becomes OfferAnswer and `buy` becomes Milestone. New kinds: `coins`, `gems`, `merge`, `haggle`, `mail_decline`, `pass`.
- **The onboarding funnel stays `SmithyCore.funnel(player, id)`.** Ids are saved and never renumbered. A `step` field gives the dashboard order.
- **Recurring funnels** use `Analytics.funnel(player, name, orderId, step, stepName)` from ShopService and DeliveryService. Each order is its own funnel session (`<UserId>-<name>-<id>`).
- **Limits.** Roblox allows 120 + 20 × players calls a minute per server. Economy and counters are summed and sent every 2 min. One-off events are capped at 8 per player a minute, and the extras are counted in AnalyticsDropped. Milestones, funnel steps and session ends always go.
- **Usage (ours):** 6 funnels, 17 custom event names, 2 currencies. The universe also holds the old bridge game's 13 funnels; whether Roblox's per-experience limits leave room for ours is unchecked (see Proposed).
- **Privacy:** no names or text, only ids, counts and seconds.

## Funnels

### 1. Onboarding (`LogOnboardingFunnelStepEvent`, once per player, saved in `d.funnel`)

| Step | Name | Fires when | Id |
|---|---|---|---|
| 1 | Joined | a new save loads (`SmithyCore` load) | 1 |
| 2 | Rolled ore | first pull (ForgeService) | 2 |
| 3 | Collected the ore | first ore taken off the roller (ForgeService `takeOre`) | 12 |
| 4 | Heated the ingot | first ingot into a furnace (ForgeService) | 13 |
| 5 | Started forging | BeginForge (SmithService) | 3 |
| 6 | Forged a sword | FinishBlade (SmithService) | 4 |
| 7 | Displayed a sword | DisplaySword (ShopService) | 6 |
| 8 | First sale | a sale (ShopService) | 7 |
| 9 | Opened the first letter | Commission "read" of the Guard Captain's letter | 14 |
| 10 | Accepted the first letter | Commission "accept" | 8 |
| 11 | Delivered the first letter | Commission "deliver": the tutorial's end | 9 |
| 12 | Bought an upgrade | any pad (TycoonService; was Ore Slot 2) | 10 |
| 13 | Opened the Gem Shop | GemService "tour" | 11 |
| 14 | Bought a gem upgrade | GemService "buy" | 15 |

- **Id 16** (2026-11-10) is saved in `d.funnel` but is not a dashboard step: the Guide's one-off far-offer hint has shown (GemService "offerHint"). Don't give it a step without moving the hint's flag.

- **Id 5** ("Assembled a sword") came at the same moment as id 4 once the hilt folded into the anvil, so it is no longer a step.
- **The old list had a bug.** A comment swallowed "Bought Ore Slot 2", so step 10 was sent as "Opened the Gem Shop" and step 11 had no name.
- **Steps 12–14 done before the tutorial ends are held back.** They are logged, in order, when step 11 comes. Roblox counts every step before a logged one as done, so logging them early would mark the tutorial finished.
- **OnboardingTime** goes with each step: the seconds played, with CF1 = the step.

### 2. Playtime (`LogFunnelStepEvent`, no session id, once per player)

- **Steps:** 1, 5, 10, 15, 30, 60, 120, 300 and 600 minutes played, in lifetime played time (`SmithyCore.totals`).
- **When:** it is checked every 30 s and when the player leaves. A rejoin carries on from the saved total.
- **Why it isn't an upgrade-ordered funnel:** players buy in different orders (the Rusher buys the Longsword before the Crafter). Roblox would mark every skipped step as done, so an upgrade-ordered funnel would show false completions. Played time is ordered for everyone. Upgrades go in the Milestone event, which gives each pad's reach and timing without assuming an order. See [[Design/Decisions Log#2026-10-29: Analytics funnels]].

### 3. MailOrder (recurring, one session per order)

| Step | Name | Fires when (ShopService) |
|---|---|---|
| 1 | Arrived | `refillOrders` makes an order |
| 2 | Opened | Order "read", the first time |
| 3 | Accepted | Order "accept", the first time |
| 4 | Filled | Order "fill" pays |

A declined order counts in OrderSkipped (CF1 Mail). Since 2026-11-11 every step carries CF1 the asked metal's rarity (`Uncommon+` for a rarity ask, `Any`) and CF2 the shape.

### 4. Delivery (recurring, one session per cart offer)

| Step | Name | Fires when (DeliveryService) |
|---|---|---|
| 1 | Offered | `refill` makes an offer |
| 2 | Accepted | "accept" |
| 3 | Sent | "dispatch" |
| 4 | Collected | "collect" pays |

A skipped offer counts in OrderSkipped (CF1 Delivery).

### 5. SwordChain (`LogFunnelStepEvent`, no session id, once per player; 2026-11-10)

One step per blade of the main sword chain, as its blueprint pad is bought (`Analytics`, kind `buy`): 1 Wakizashi, 2 Machete, 3 Katana, 4 Scimitar, 5 Longsword, 6 Cutlass, 7 Falchion, 8 Jian, 9 Gladius, 10 Khopesh, 11 Dadao, 12 Rapier, 13 Hook, 14 Crescent Fang, 15 Shard Blade, 16 Moonbite, 17 Serpent, 18 Leviathan Cleaver, 19 Thornspire, 20 Seraph. Read from `Upgrades.list` (the blueprint with no `after`, then each whose `after` is the one before), so a new chain sword joins by itself. The big swords (Zanbatō, Claymore, Flamberge) also wait on a stand, a side branch, and aren't steps. The chain is gated, so the order holds for everyone.

### 6. Shop (recurring, one session per Shop opening; 2026-11-10)

| Step | Name | Fires when |
|---|---|---|
| 1 | Opened | the Shop window shows (`MenuController` → `Remotes.ShopFunnel` "Opened"); a new session at most every 5 s |
| 2 | Pressed Buy | a Shop Buy opens Roblox's prompt (`MenuController.buy` → "Prompted", key), once per session |
| 3 | Bought | Roblox's purchase answer (`PromptGamePassPurchaseFinished` / `PromptProductPurchaseFinished`, purchased) for an item pressed in that session, within 10 min |

Logged in `WorldStoreLog`. Session id `<UserId>-Shop-<os.time() at opening>`. The server accepts only the two step names and a real Store key. Purchases started elsewhere (the world spots, the shortfall pack offers, the Auto-Roll and Auto Anvil locks) aren't in it.

## Custom events and what each one calibrates

| Event | Value | Fields | From | Simulator parameter |
|---|---|---|---|---|
| OnboardingTime | seconds played | CF1 step | `SmithyCore.funnel` | first pull → first sale (report 2b); the tutorial's timings |
| Milestone | minutes played (lifetime) | CF1 pad id / crafter id / `Merge n` / `<gem id> <level>` / letter id; CF2 time bin (0-5 … 600+ min); CF3 Pad, Crew, Merge, Gem, Letter | `buy`, `hire`, `merge`, `gem_buy`, `letter` | report §7.1 time to each milestone and "% reached by T"; §7.4 share who buy each pad; which archetype's buy rule real players follow |
| OfferAnswer | seconds to answer | CF1 Accepted / Declined / Missed; CF2 VIP / Regular; CF3 offer ÷ value (<0.9, 0.9-1, 1-1.1, 1.1+) | `offer` | `Archetype.react` (mean), `Archetype.miss` (Missed share), `haggle` (Declined share by offer bin); `timings.json` offers |
| DeclineResult | count | CF1 Raised / WalkedOff; CF2 Player / Cashier (tutorial lessons left out) | `haggle` (ShopService) | the value of declining: checks `Customers.raise` against real walk-offs |
| SwordSold | seconds on the holder | CF1 Player / Cashier; CF2 declines first (0, 1, 2+) | `display` → `sale` | the loop's "selling" part (report 2b) |
| SwordLoop | seconds from ore collected to sold | none | `collect` → `forge_finish` → `sale` | the whole own-sword loop (report 2b) |
| ForgeGrade | forge percent | CF1 blueprint | `forge_finish` | skill → `grade` (Plan §8.4, "the biggest value lever") |
| OreRolled | ores rolled | none | `pull` | with OreKept: pulls per kept ore |
| OreKept | count | CF1 rarity; CF2 Hand / Gathered | `collect` | `Archetype.keep` (the rarity kept, against `Materials.odds`) |
| SwordFinish | count | CF1 Polished / PolishLeft / PolishNone / Etched | `polish`, `etch` | `Archetype.polish`, `Archetype.etch`; polish success |
| OrderSkipped | count | CF1 Mail / Delivery | `mail_decline`, `cart_skip` | `Archetype.mail`, `Archetype.cart` (with the two funnels) |
| DailyClaim | count | CF1 Day 1-7 | `gems` with `day` | days played, `PLAY_DAY`, streaks |
| PassPrompt | count | CF1 pass or product key; CF2 Bought / Closed (products since 2026-11-10); CF3 source Shop / World / Lock / Offer / Other (2026-11-11). Only events with a key since 2026-11-11: ShopService's customer "pass" (walked past a sword) shares the kind and was logged as CF1 nil | StoreService | `PAYERS` shares (free / starter / allpasses) |
| Purchase | Robux spent (a pass: its price from Roblox, nil if unknown) | CF1 Store key; CF2 Pass / Product; CF3 minutes-played bin | StoreService: a granted receipt (once per purchase id), a pass bought in the game (2026-11-10) | what sells, at what point in a player's time; never dropped by the budget |
| WorldStore | 1 | CF1 spot key; CF2 Shown / Prompted / Bought | WorldStoreLog (world spots, after the tutorial) | which in-world offers convert |
| SessionEnd | minutes this session | CF1 the furthest simulator milestone (Katana … Seraph), or the furthest onboarding step before Katana; CF2 First / Returning; CF3 the Guide's line on screen, None without one (2026-11-11) | leave | session lengths; where players quit; a quit hazard (Plan §5, "Quitting") |
| FirstPrompt | seconds played | CF1 `<model>/<action>`, first use of each prompt on your own plot in your first session (2026-11-11) | Analytics (PromptTriggered) | where new players stop at a station |
| BuyGap | minutes since this session's last buy or its start | CF1 pad; CF2 Last buy / Session start (2026-11-11) | `buy` | the simulator's waits between buys |
| AnalyticsDropped | events dropped by the cap | none | leave | coverage: how much of the above is missing |

## Economy events (`LogEconomyEvent`, Coins and Gems)

- **Sent:** summed by SKU every 2 min and when the player leaves.
- **The balance** is the committed one at the send: `leaderstats.Coins` (where coins live) and `SmithyCore` gems. With the summing it is the balance after the last change in the batch, not after each one.

| Flow | Currency | SKU (transaction type) | Where |
|---|---|---|---|
| Source | Coins | Sale, Cashier (till collected), Letter, MailOrder, Delivery (Gameplay) | ShopService, DeliveryService |
| Source | Coins, Gems | StarterPack, coin and gem packs by key (IAP) | StoreService |
| Source | Gems | DailyReward (TimedReward); Letter, MailOrder, Delivery (Gameplay) | GemService, ShopService, DeliveryService |
| Sink | Coins | each pad's id, `Cart capacity` / `Cart speed`, Train, crafter ids (Shop) | TycoonService, DeliveryService, EmployeeService |
| Sink | Gems | gem upgrade ids, crafter ids (Shop) | GemService, EmployeeService |

These give the income per minute (report §7.3), sink/source by SKU, and the gem economy the simulator models (gem income from mail, carts and daily rewards against Gem Shop and crew spending).

**Not logged:**
- DevTools coins.
- A Cashier till that is saved without being collected. The save adds it to coins without going through `addCoins`.

## Reading it in the Creator Dashboard

- **Where:** Creator Hub → the experience → Analytics.
  - **Funnels:** Onboarding, Playtime, MailOrder, Delivery. Each shows conversion and drop-off per step.
  - **Economy:** Coins and Gems sources and sinks by SKU and transaction type.
  - **Custom events:** pick an event, then break it down by custom field. For example, Milestone by CF1 and then CF2 gives each pad's "% reached by" bins, and OfferAnswer by CF1 gives the miss rate.
- **Dashboard lag:** about 24 h. **View Events** at the top shows events in near real time, so use it to check a live test.
- **Into the simulator, by hand for now:**
  - medians: OfferAnswer seconds, SwordSold and SwordLoop seconds, ForgeGrade by blueprint;
  - shares: Missed, Declined by offer bin, OreKept by rarity, mail Filled ÷ Arrived, cart Accepted ÷ Offered;
  - the Playtime and Milestone bins against `results/<run>/report.html`.
- **What needs fixing:** compare real "% reached by T" per milestone with the archetypes'. A milestone real players reach far later than every archetype is a wall. A Playtime step with a big drop-off, together with SessionEnd's CF1 at that time, shows where players quit.

## Not covered (outside the server)

- **Viewing a single pack in the Shop** (scrolling past a card). The Shop funnel counts openings and Buy presses only.
- **Passes bought on the experience's Store tab**, outside the game: no Purchase event (Roblox's own sales page has them).
- **Gaps between sessions and D1/D7.** Use the dashboard's built-in retention.

## Proposed (2026-11-09, not built)

- **ShopPurchase** and **SwordChain:** built 2026-11-10 as the Shop and SwordChain funnels above (Allen: "Add them").
- **Blocked on a check:** since 2026-11-09 the game lives in Swordsmith Tycoon's universe (the old bridge game), which already has 13 custom funnels (BridgeTutorial … ForestMilestones). The "4 of 10 funnels" above counted only ours. First check that Playtime, MailOrder and Delivery appear in the dashboard.
- **Checked 2026-11-10 through the Analytics Query API** (`POST /analytics-query-api/v1/universes/10769630190/dimension-values`, read with the Studio MCP's `open_cloud_invoke`, scope `universe.analytics:read`), last 90 days: 16 funnel names hold data: the old game's 13 (BridgeTutorial, BridgeLoop, SessionLength, BridgeProgress, Quests, LifetimePlaytime, LockedStation, PlaytimeRewards, BridgeMilestones, Tutorial, RobuxShop, ForestLoop, ForestMilestones), the shared `FUNNEL_TYPE_ONBOARDING`, and ours **Playtime** and **MailOrder**. So the old funnels don't stop ours being recorded; ten is the dashboard's tab limit. **Delivery, SwordChain and Shop have no data yet** (SwordChain and Shop were built 2026-11-10; nobody has reached a cart offer). The onboarding funnel is one per experience, so ours shares it with the old game's steps. Custom events: 31 names, ours arriving (Milestone 5 events and SessionEnd 3 users on 2026-11-10, plus OreRolled, ForgeGrade, OfferAnswer, OreKept, SwordLoop, SwordSold, SwordFinish, DailyClaim, WorldStore).
- **Onboarding funnel checked 2026-11-10 (same API, `FunnelUserTotalCount` by `FunnelStep`, funnel `FUNNEL_TYPE_ONBOARDING`):** it is shared with the old bridge game. Over 90 days steps 1-6 carry the old game's names and players (Joined 7,105, PickedUpSeeds 6,230, PlacedPlank 5,237, Trained 4,158, BoughtUpgrade 3,310, FinishedBridge 1,323) and steps 7-14 ours (Displayed a sword 3 ... Bought a gem upgrade 2). **From 2026-11-09 on it is clean**: all our names in order (Joined 2, Rolled ore 2, Collected the ore 1 ... Accepted the first letter 1). So read onboarding with a start date of 2026-11-09 or later; any window reaching back before it mixes the two games. The 90-day and the 3-day counts of our steps 7-10 differ (3 against 1); not looked into (testing before 2026-11-09, or late data).

**Admins (2026-11-11):** Shared/Admins.USERS and Admins.ALTS (Allen's five alts) send nothing, through `Admins.quiet` (Analytics.skip, SmithyCore.logStep, WorldStoreLog.log). Data before the next publish still includes them.

- **LoadTime / LoadQuit (2026-11-11):** LoadTime value = seconds from joining to the Guide's first line, CF1 First / Returning / Unknown. LoadQuit value = seconds in the server for a player who left before that, same CF1. Once per server visit.

## Journeys (built 2026-11-12)

Allen: "Can we look into ROBLOX Journeys? Would they be helpful for our game and serve a purpose different from funnels?", then "Build all three".

- **What:** `AnalyticsService:LogJourneyEvent(player, journey, node, sessionId?, fields?)`. A journey is 2–10 stages; each stage holds 1–10 nodes that are alternatives (equal progress). The dashboard (Creator Hub → Analytics → Journeys → View) shows a Sankey of paths, a path breakdown, churn by node and stage, Sessions and Users views, filters by CF1–3, platform, payer, new user. Source: https://create.roblox.com/docs/production/analytics/journey-events
- **Against funnels:** both mark skipped stages as done, so stages must come in one order for everyone. A journey also records *which* node in each stage and the paths between them. Funnels say how many got through; journeys say which way they went.
- **Node names hold their stage** ("Buy 3: Crew", "2nd: Mail order"): `LogJourneyEvent` takes no stage, so a name sits in one stage only.
- **A player who logs nothing isn't in a journey.** That's why AfterTutorial starts with "Tutorial done": quitters right after it show as churn there.

| Journey | Session | Stages and nodes | Logged in `Analytics.log` |
|---|---|---|---|
| **BuyOrder** | once per player | stages = the 1st, 2nd, 3rd, 4th, 5th, 6th, 8th, 10th, 15th, 20th pad bought; nodes `Buy N: <kind>`, kind one of Ore, Blueprint, Station, Boost, Crew, Display, Customers, Delivery, Decor, Other. CF1 the time bin | `buy`. N = pads owned + 5 per ore merge (a merge un-buys Ore Slots 2-6). A pad with `with` (Swordsmith + Anvil 2) can pass two stages: the later one logs |
| **SwordFate** | one per sword (`<UserId>-Sword-<id>`) | Forged → Polished / Not polished → Etched / Not etched → Customer sale / Cashier sale / Mail order / Letter / Delivery. CF1 (Forged) the blueprint | `forge_finish` starts it; `polish` (polished) and `etch` log as they happen; `sale`, `mail`, `letter`, `cart_send` (DeliveryService now sends `swords`, the packed ids) fill the finishes it skipped, then the end |
| **AfterTutorial** | once per player | Tutorial done → the 1st to 5th *new* thing done: Upgrade, Mail order, Delivery (cart accepted), Gem upgrade, Crew, Polish, Etch, Merge, Robux, Letter | `letter` with the first letter's id starts it; then `buy`, `mail`, `cart_accept`, `gem_buy`, `hire`, `polish`, `etch`, `merge`, `purchase`, other `letter`s |

- **Kinds of pads** (from `Upgrades.list`, 2026-11-12): Ore 10 (ore slots, ingot racks, merge), Blueprint 23, Station 9 (furnaces, anvils, polishing stations, etching tables), Boost 19 (heating, strikes, polish boosts, etch patterns), Crew 5, Display 16 (sword and wall racks, display tables, big sword stands, Upgraded Store), Customers 6 (bays, showcase stands), Delivery 1, Decor 6. Nothing falls in Other today; a new pad that matches no rule does.
- **Configs:** published 2026-11-12 through Open Cloud with `ROBLOX_API_KEY` (`PATCH .../creator-configs-public-api/v1/configs/universes/10769630190/repositories/JourneysConfig/draft`, then `POST .../publish`), config version 1. The Studio MCP's `open_cloud_invoke` lacks `universe:write`. Roblox processes configs daily; an edit is a new version, and players keep the version they started on.
- **Limits (known):**
  - SwordFate covers swords forged by hand in this server visit. A sword kept over a rejoin never logs its end, and crew-made swords aren't in it (a sword has no maker field).
  - AfterTutorial lives only in the visit the tutorial ends in: a player who rejoins before five new things shows as stopping.
  - BuyOrder for a player who had pads before the next publish starts mid-way, with earlier stages marked skipped. Blueprints learned from a letter count their pad as owned.
- **Checked (Edit):** Analytics and DeliveryService compile; a fresh Analytics clone requires. A test copy with LogJourneyEvent, SmithyCore and Admins stubbed, fed a fake player's events: the tutorial letter, a buy, polish → sale, etch → polish → mail order, a delivery with one tracked and one unknown sword, a sale of an untracked sword, the Swordsmith with Anvil 2 (logs Buy 6), an ore merge (the count carries on to Buy 15). Every node came out as in the table, nothing for untracked swords. All pads map to a kind.
- **Not checked:** a live server (Studio Play sends nothing). Journeys show in the dashboard a day after the next publish.

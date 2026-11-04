# Analytics Funnels

Built 2026-10-29. Allen: "look at where we can add funnels to our game, and also make sure the funnels can give us a better view of what needs improvement and similarly to our simulations, gives us better data to run our simulations."

Everything is logged on the server through `AnalyticsService`. Only live servers report: Studio Play sends nothing, and there are no live players yet. Related: [[Development/Gameplay Simulator Plan]], [[Development/Code Map]].

## How it is wired

- **One event vocabulary.** The services already call `PlaytestLog.log(player, kind, data)` at every step the simulator times. `PlaytestLog` now hands every event to `ServerScriptService.Analytics`, in Studio and in live servers. In Studio it still also posts to `receive.py` for `calibrate.py`.
- **`Analytics` turns kinds into dashboard events.** For example, `offer` becomes OfferAnswer and `buy` becomes Milestone. New kinds: `coins`, `gems`, `merge`, `haggle`, `mail_decline`, `pass`.
- **The onboarding funnel stays `SmithyCore.funnel(player, id)`.** Ids are saved and never renumbered. A `step` field gives the dashboard order.
- **Recurring funnels** use `Analytics.funnel(player, name, orderId, step, stepName)` from ShopService and DeliveryService. Each order is its own funnel session (`<UserId>-<name>-<id>`).
- **Limits.** Roblox allows 120 + 20 × players calls a minute per server. Economy and counters are summed and sent every 2 min. One-off events are capped at 8 per player a minute, and the extras are counted in AnalyticsDropped. Milestones, funnel steps and session ends always go.
- **Usage:** 4 of 10 funnels, 15 of 100 custom event names, 2 of 10 currencies.
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

A declined order counts in OrderSkipped (CF1 Mail).

### 4. Delivery (recurring, one session per cart offer)

| Step | Name | Fires when (DeliveryService) |
|---|---|---|
| 1 | Offered | `refill` makes an offer |
| 2 | Accepted | "accept" |
| 3 | Sent | "dispatch" |
| 4 | Collected | "collect" pays |

A skipped offer counts in OrderSkipped (CF1 Delivery).

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
| PassPrompt | count | CF1 pass key; CF2 Bought / Closed | StoreService | `PAYERS` shares (free / starter / allpasses) |
| SessionEnd | minutes this session | CF1 the furthest simulator milestone (Katana … Seraph), or the furthest onboarding step before Katana; CF2 First / Returning | leave | session lengths; where players quit; a quit hazard (Plan §5, "Quitting") |
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

- **Opening the Shop page and viewing a pack.** That is client UI. A store-page funnel needs a whitelisted client signal (`roblox-networking`).
- **Gaps between sessions and D1/D7.** Use the dashboard's built-in retention.

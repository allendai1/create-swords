# Gameplay Simulator Plan

Allen (2026-10-29): build a gameplay simulation system to balance progression, economy, resource probabilities and the player experience. It should simulate thousands of players, run experiments on prices, drops, crafting times, sale values and upgrade costs, and compare them. His preference: a custom Python simulator, independent of Studio, with a shared source of truth for balance data.

Status: **built** in `Development/sim` (steps 1–2 below); runs are in `Development/Sim Runs/`. See also [[Design/Economy Review — 2026-10-29]] and [[Development/economy_model.py]].

## 1. Verdict

**A custom Python simulator is the right approach.** It needs two conditions, and both are cheap:
1. **Studio stays the only source of truth.** The Luau modules (`Shared.Upgrades`, `Blueprints`, `Materials`, `Customers`, `GemUpgrades`, `Employees`, `Deliveries`, `Orders`, the Weather table…) are what the game runs, and they're edited in Studio (no Rojo). An exporter dumps their numbers to `balance.json`; Python never holds its own copy of a game number.
2. **Every rule Python re-implements is checked against the real Luau.** Studio runs the real functions over fixed inputs and saves the answers ("golden" files), and Python must reproduce them.

**Why not the alternatives:**
- **Simulating in Studio (Luau):** it would reuse the real code, but Studio is slow for millions of events, ties up the place Allen works in, and has no plotting or statistics.
- **Simulating real Roblox clients or physics:** this answers nothing about the economy that a travel-time table can't.
- **JSON as the source the game reads:** Allen tunes in Studio, and moving every module to read a JSON blob is a big refactor for no gain.

**Why today's model isn't enough:** `economy_model.py` already simulates one player, but it has three limits that matter for these questions.
- **It hard-copies constants by hand, and they drift.** Better Advertising level 3 was stale by today; the blueprint pads had to be patched three times today.
- **It has no randomness.** It uses expected values: one deterministic player per profile, no ore luck, no distributions, no percentiles.
- **It ticks every second and has no walking or stations.** It works from a seconds-per-sword estimate.

Keep it as a cross-check (the new simulator's casual median should land near it), then retire it.

## 2. Shape (the smallest thing that answers the questions)

The code lives in the vault, beside the model:

```
Development/sim/
  balance.json        exported from Studio (never hand-edited); has the export time and a hash of the modules' sources
  golden/*.json       input → output pairs from the real Luau functions (exported with it)
  layout.json         station positions per plot layout (exported from the plot template, with the upgrade push)
  rules.py            the game's mechanics, pure functions mirroring the Luau (value, offers, odds, pay, prices, gates)
  engine.py           discrete-event loop for one player
  behavior.py         the archetypes: modelled player decisions (assumptions, not mechanics)
  scenarios.py        named experiments = overrides on balance.json (prices ×0.9, odds, durations …)
  run.py              N players × scenarios, seeded, in parallel (multiprocessing), → results/*.parquet or csv
  report.py           one HTML/Markdown report per run, comparing scenarios
  test_parity.py      pytest: rules.py against golden/*.json, and balance.json is current
```

**On the Studio side:**
- **`ServerStorage.Builders.ExportBalance`:** run in Edit through the MCP. It requires fresh clones of the Shared modules and posts `balance.json`, `golden/*.json` and `layout.json` to a localhost receiver.
- **`ServerStorage.Tests.BalanceExportSpec`:** checks that every exported table is complete. For example, every upgrade has a price and a position, and every blueprint has a base value.

The localhost receiver is the same one used today to pull etch data out of Studio.

**Mechanics vs behavior, kept apart in the files:**

| Layer | Holds | Who changes it | How it's checked |
|---|---|---|---|
| `balance.json` | numbers: prices, odds, multipliers, durations the code states | only the exporter | its hash against Studio |
| `rules.py` | how the game computes: a sword's value, an offer, a roll, gates, prices after merges | code, when a Luau rule changes | golden tests |
| `layout.json` + measured timings | where stations are, how long hand actions take | exporter + calibration | playtest logs (§4) |
| `behavior.py` | what a modelled player chooses and how fast they react | design assumptions | sensitivity runs (§6), later real analytics |
| `scenarios.py` | the experiment's changes | the experimenter | logged in each report |

## 3. Simulation method: discrete events, one player at a time

Players don't affect each other (separate plots). The one shared thing is the **server's weather**, and it's simply a timeline each simulated player is given. So every player runs alone, and runs spread across CPU cores.

**One player is a priority queue of timed events** (`heapq`). Time jumps from one event to the next, never frame by frame:
- **The player's own steps:** arrive at a station, pull lever done, ingot heated, forge done, hilt seated, polish done, etch done, sword shelved, upgrade bought.
- **The world:** a customer arrives, an offer times out, a crafter finishes a sword, the Stocker or Cashier acts, the cart returns, a mail order arrives, the weather changes, the session ends.

**Rough cost:**
- About 1,000–2,000 events an hour of play (about 45 swords of your own, crew swords, about 90 customers, mail, weather).
- 10,000 players × 10 h is about 100–200 M events. In pure Python that's a few minutes over 8 cores.
- That's enough: at 10,000 players a median or P90 is stable to about ±1%.
- **Millions of players add nothing measurable.** Run 2,000 per scenario while iterating and 10,000 for a decision.

**Movement:**
- **A travel-time table** between stations: plot-space distance ÷ walk speed (16 studs/s; 20 with Swift Boots), times a detour factor for paths round tables, measured once.
- **Positions come from `layout.json`**, including the 12-stud workshop push when the Upgraded Store is bought.
- **A trip happens in the engine whenever the policy sends the player somewhere,** so "walk back and forth while managing stations" is where the time goes, not a guess folded into seconds-per-sword.

**Player state** (per simulated player):
- **Money and goods:** coins, gems; ingots (metal, hot or not, where); swords (blueprint, metal, quality, polish, etch, where: hotbar, rack, holder, stand, cart, mail).
- **The plot:** upgrades owned, merges, blueprints known, crew hired, trained and levelled, staff.
- **Activity:** the current action and position; furnace, anvil and crafter progress; the open offers, mail and cart.
- **Time:** the clock, session number, played vs offline time.
- **Results:** milestone timestamps and a running log of income, spend and idle time, sampled each minute for the reports.

**Seeds (reproducible and comparable):**
- Each player has a seed. Every random thing draws from its own stream, keyed by (seed, stream name, draw number): ore rolls, customer arrival and type and offer, weather, crew quality, and behavior noise. A counter-based generator (NumPy `Philox`, or a hash) does this.
- So player #417's 300th ore roll is the same in every scenario, even if a price change shifts when they pull. Scenarios differ only by what they change: these are common random numbers.

## 4. Keeping it in step with the game, and proving it matches

1. **Numbers:** `ExportBalance` writes them, and `balance.json` carries a hash of every source module. `run.py` refuses to run if the hash in Studio differs; a quick MCP call compares them. Re-export after any balance edit; it's one command.
2. **Formulas, through golden tests:** Studio calls the real functions on fixed inputs and saves the outputs, and pytest makes `rules.py` reproduce them exactly (integers) or within 1e-9. The functions:
   - `SmithyCore.swordValue` (several swords: metals, quality, hilts, polish, etch);
   - `Customers.offer` and `.raise` (with a seeded RNG, or on the share draws);
   - `Materials.odds` at luck 1 to 10;
   - `Orders.pay` and `.typicalMetal`;
   - `Upgrades.price` after merges;
   - `GemUpgrades` intervals;
   - `Employees` levels and perks;
   - `Deliveries.pay` and `.mismatch`;
   - pad availability for a list of owned sets.
3. **Random rules:** draw 1 million rolls in each language, then run a chi-square test of the rarity counts against `Materials.odds` (and the same for customer types and weather). It fails at p < 0.001.
4. **Gates:** export the full `after` graph. A test checks that the simulator's "what's on offer" equals the game's for random owned-sets.
5. **Timings the code doesn't state** (walking, how long a person takes on the forge minigame and the polish, reaction to an offer card) are measured, not invented.
   - A dev-only `PlaytestLog` (Studio only, off in live servers) posts timestamped events to the localhost receiver while Allen playtests: arrived at a station, action started and finished, offer shown and answered, ore pulled.
   - Each action's duration becomes a distribution in `timings.json`: median and spread, not one number.
   - After release, Roblox analytics (custom events and funnels) can replace these with real players' numbers.
6. **End-to-end check:** replay one of Allen's logged sessions through the simulator, using his actions and the logged rolls. Coins and unlock times should come out within a few percent. If they don't, a rule or timing is wrong.
7. **When to rerun:** after every balance change, re-export and run `pytest`. A red test means the game and the simulator disagree, and nothing gets balanced until it's fixed.

## 5. Modelled players (behavior)

A modelled player is a **policy**: at each decision point it scores the available choices with simple, stated rules plus noise. It doesn't claim to be a real person. Its parameters are the assumptions, and §6 checks which conclusions survive changing them.

**Decision points:**
- What to do next: pull ore, feed the furnace, forge, finish (hilt, polish, etch), stock a holder, answer an offer, fill mail, pack the cart, buy something, or wait.
- Which ore to keep (a rarity threshold).
- Which upgrade to buy and when (the buy rule).
- When to stop the session.

**Parameters each archetype sets:**
- **Buy rule:** cheapest first (today's model), best payback first, blueprints first, or crew/staff first.
- **Ore threshold:** keep any, Uncommon+, or Rare+; the Auto-Roll once owned.
- **Skill:** forge quality (feeds `grade`), and polish and etch success.
- **Pace:** reaction delay to offers and idle stations (a lognormal), extra walking, a chance of a wasted trip.
- **Attention:** the chance to miss an offer within its 45 s, mail checked every N minutes.
- **Session:** session lengths and gaps between sessions.

**Recommended for v1 (four):**

| Archetype | Buy rule | Ore | Pace | Why |
|---|---|---|---|---|
| **Casual** | cheapest first | Uncommon+ | slow reactions, some idle and wasted trips | the main audience; matches today's "casual picker" |
| **Efficient** | best payback | Rare+, Auto-Roll when owned | fast, no idle | the ceiling; shows how far good play gets ahead |
| **Automator** | crew and staff first, then cheapest | Rare+ | casual pace | tests the "buy an employee early" path |
| **Rusher** | blueprints first | Rare+ | fast | today's "focused" profile; stresses the sword chain |

**Not archetypes:**
- **Unlucky players.** Luck isn't a behavior: it's the player's own draws. Every archetype gets the same seeds, and the report shows outcomes by **luck percentile**: the realized ore value against the expected, P10 vs P90.
- **Grinders.** These are efficient players who never buy non-income upgrades. Add them later if needed.
- **Explorers.** "Tries things" has no rules to check against. Leave them out until there's analytics to fit.

**Quitting:** v1 doesn't predict quitting. It simulates **played time**, and reports progress by played minutes and the **stuck time** players would have to sit through. A quit hazard (for example, quit-chance rising with minutes stuck) can be added later as an explicit experiment knob.

## 6. Telling a real improvement from noise

- **Same seeds for every scenario** (§3), so the comparison is paired: each player against themselves.
- **For each milestone, report:**
  - the per-player difference (scenario − baseline), with its median and a bootstrap 95% interval (resample players 1,000×);
  - the difference in percentiles (P10/P50/P90) and in "% reached by T", with the same bootstrap.
- **A change counts only when both hold:**
  1. the 95% interval excludes 0;
  2. it beats a practical threshold set in advance. For example, a milestone moves by at least 5% or at least 5 min, or "% reached by 30 min" moves by at least 3 points.
- **Check that it holds up:** a winning scenario must win for all four archetypes, and when one behavior parameter at a time is changed ±30% (reaction time, ore threshold, skill). A change that only helps one invented player type isn't a conclusion.
- **Sanity check every run:** the baseline against itself with a fresh seed set should show no meaningful difference. If it does, the run is too small.

## 7. Report: the smallest useful first version

Seven metrics, by archetype (columns), at P10/P25/P50/P75/P90:

1. **Time to each milestone:** every station, upgrade, blueprint, crew hire and merge, plus % reached by 5, 10, 15, 30 and 60 min, 2 h, 5 h and 10 h, and % never reached within the horizon.
2. **Swords completed by 5, 10, 15 and 30 min:** yours and the crew's, plus the average seconds per sword of your own and its split by station: walking, pulling, heating, forging, finishing, selling.
3. **Income per minute over time,** with coins held and spent: median and P10–P90 bands.
4. **Each purchase at the moment it's bought:** price in minutes of income, payback minutes, and the share of players who buy it at all. This flags pads that are too expensive or too strong.
5. **Stuck time:** stretches of 10+ minutes with no purchase, unlock or new sword. Report the count per player, the longest one, and when they happen (by minute bins). This finds the bottlenecks.
6. **Luck:** ore rarity counts against the odds; each player's luck percentile against their milestone times (does a P10-lucky player fall more than X% behind?).
7. **Waiting:** time stations sit finished but uncollected, offers missed, and swords sent by cart vs sold. This shows where the walking and managing hurts.

**Leave out of v1:** heatmaps of movement, per-customer haggling stats, and gem-economy detail beyond Better Advertising and More VIPs levels.

**Format:** one self-contained HTML file per run (tables plus a few line charts), plus the raw per-player CSV for digging. A comparison run puts the scenarios side by side with the §6 intervals.

## 8. Mechanics to confirm before building

These aren't guessed. Each needs a check in the code or Allen's call:

**Possibly not in the code:**
1. **Offline progress.** Does anything happen while a player is logged out? Deliveries and mail use `os.time()`, so they finish or refill while away. Crafters, the Stocker, the Cashier and customers: per the code they run only while the plot is loaded. Confirm, and say whether a model "session" should include offline time.
2. **Crafters' ingots.** Do crafters use the player's pulled ingots from the Ingot Rack, kept stocked by the Stocker? And does a crafter stall when the rack is empty? (The current model assumes their pulls are yours.)
3. **Parallel work.** Furnace slots per furnace, anvils usable at once by the player, whether a furnace heats while you forge, and the hotbar, rack and holder capacities.
4. **Forging skill.** How the strike minigame turns player input into quality (and so `grade`, ×1–2). It's the biggest value lever. Measure a quality distribution per archetype from playtests rather than assume one.
5. **Offers.** What happens when nobody answers within 45 s: the customer leaves without buying? What does the Cashier accept (its setting)? Does an unanswered offer block the holder?
6. **The Big Sword Stand:** one slot, restocked how often, and does a waiting big sword block anything?
7. **Session start and the tutorial:** fixed steps and timings (the tutorial gap is 12–22 s; the letter delay is 45 s) and whether the Guide forces an order.
8. **Gems:** every source (daily, orders, deliveries, letters, passes) and sink. v1 can treat gem upgrade levels as bought at fixed times, as the model does now.
9. **Passes and products** (Lucky Ore, Swift Boots, coin passes): v1 runs without them. Add a "paying player" archetype later.

**Timings that need measuring (playtest log):** walking (the detour factor), and the hand-action times: lever pull, carrying, forge minigame, hilt seat, polish, etch, stocking a holder, opening and answering an offer, mail, cart packing. Also reaction times.

## 9. Order of work

1. **Export and parity (about half a day):**
   - `ExportBalance` and `golden/*.json`, `rules.py`, `test_parity.py` and the hash check.
   - Port today's model onto `balance.json`, so the drifting constants are gone at once.
2. **Engine v1 (1–2 days):** the event loop and the full loop of hand actions with a travel table.
   - The hand actions: pull, heat, forge, finish, stock, sell.
   - The rest of the loop: customers with weather, the upgrades graph, the crew and staff, merges.
   - Four archetypes, seeds, multiprocessing, and the seven-metric report.
   - Timings come from the code where it states them, and from flagged placeholders otherwise.
3. **Calibrate (needs one or two of Allen's playtests):** `PlaytestLog`, `timings.json`, then the end-to-end replay check.
4. **Experiments:** the §6 harness. Scenarios: prices ±10%, rarer ore odds, faster crafting, sale values, and the review's open options C and D.

Mail orders, the cart, the gem shop timing and passes are added once v1's numbers are trusted.

## Allen's answers (2026-10-29)

- **Focus: "Both equally."** v1 builds the full loop to the Seraph, and the report shows the first hour in finer bins (each minute to 15 min, then every 5 min to 60), beside the whole curve.
- **Sessions: played time only.** Every result is in minutes actually played. Logged-out time and offline progress wait until §8.1 is confirmed.
- **Timings: estimates for now.**
  - Use the code's stated durations: cascade show, heat times, tutorial gaps, offer timeout, cart trips, customer walk speed 6.
  - Use travel from `layout.json` at 16 studs/s.
  - Hand actions with no stated time get placeholder distributions, each marked `ESTIMATE` in `timings.json`. The report prints which of its results depend on them.
  - The `PlaytestLog` calibration (§4.5) stays planned for later.
- **Paid items: included in v1.**
  - A "paying player" switch can be set on any archetype: which passes it owns (Lucky Ore: luck one merge higher; Swift Boots: WalkSpeed 20; the coin passes' sale boost; the Auto Ore Roller) and when it buys gem packs.
  - The numbers come from the export (`Shared/Store`, `GemUpgrades`).
  - The report always shows free and paying players side by side, so paid items never hide inside the free curve.

## §8 settled (2026-10-29)

**Read from the code:**
- **Crafters** (`EmployeeService.oneSword`):
  - Each fetches the **cheapest** ingot on the Ingot Rack (12 slots with Ingot Rack 2), then waits for a free furnace.
  - A crafter waits (shown as a status) when it has no shape trained (`noShape`), there's no Finished Sword Rack (`noRack`), that rack is full (`rackFull`), or there are no ingots (`noIngots`).
  - So crafters live on the ingots you rack, and stall when you don't keep up.
- **Offers** (`ShopService`): an offer you don't answer within 45 s (60 s for a VIP) means **no sale**; the customer leaves. Declining may bring a raise (`Customers.raise`). The Cashier answers after his perk's delay and sells at or above value plus his setting.
- **Customers at once:** 2, +1 with the Shop Promoter, +1 per Rickshaw Bay.
- **Logged-out time:** not needed (played time only).

**Allen's calls:**
- **Targets:** keep Economy Pass 2's stage targets and extend them:
  - Katana 20 min, Sword Crafter 1 h, Longsword 1 h 45, Falchion about 4 h, Gladius about 6 h 20, Zanbatō 8 h;
  - then the Seraph at about 20 h for a casual player.
  - Experiments are scored by how close each archetype's median comes to these, and by stuck time.
- **Forge skill:** everyone near 100% (the minigame is easy), so `grade` is about ×2 for all. It's marked `ESTIMATE` until measured.
- **Paying players: several tiers,** shown side by side:
  - free;
  - Starter Pack;
  - all the gameplay passes (Lucky Ore, Swift Boots, the coin passes, the Auto Ore Roller).
- **Stuck:** 10 minutes with no purchase, unlock or new sword.
- **Reports:** a short vault note in `Development/` per run, with the full HTML report and the per-player CSV beside it.
- **Logistics are modelled:** the player (or the Stocker) walks ingots to the Ingot Rack and swords from the Finished Sword Rack to the shop. Crafters wait when the rack is empty or full, so keeping up costs real walking.

**Archetypes, now six:**

| Archetype | Buys | Spends time on | Note |
|---|---|---|---|
| **Casual** | cheapest first | own swords, some idle and wasted trips | the main audience |
| **Efficient** | best payback first | own forging, fast | the ceiling for a hands-on player |
| **Automator** | crew and staff first | casual pace | the "buy an employee early" path |
| **Rusher** | blueprints first | own forging, fast | stresses the sword chain |
| **Grinder** | only what raises income (swords, crew, ore slots); saves otherwise | crafting nonstop, never idle | added by Allen |
| **Manager** | best payback, plus every rack and holder upgrade | keeping things full first: Ingot Rack always stocked so crafters never stall, finished swords moved to the shop, holders always filled, the cart kept running and the mail filled. Forges only when everything is topped up | Allen: "super OCD … maximize efficiency"; the upper bound for logistics |

The Efficient player and the Manager differ by **what they do with their hands**: the Efficient player forges their own swords and lets the crew stall now and then, while the Manager feeds the crew and the shop first. The gap between them shows what tending stations is worth.

## Built: step 1, export and parity (2026-10-29)

**In Studio:** `ServerStorage.Builders.ExportBalance` (ModuleScript). It runs in Edit only, because it requires a copy of SmithyCore:
- **What it reads:** it requires a fresh copy of `Shared`, plus a copy of SmithyCore pointed at it, so cached modules can't leak in. Constants that live in Scripts are read from their Source by pattern, and the export stops if one is missing: the shop's walk-ins, offer timeout, tutorial gap, letter delay, card gap and customer walk speed; the weather table and its spell; Materials' `MIN_COMMON`.
- **What it writes,** to `Development/sim/` through `receive.py`:
  - `balance.json`: upgrades and gates, blueprints, metals and odds, hilts, etches, grade, customers, gem upgrades, crew and staff, cart, orders, store, letters, reputation, shop constants, weather, and walk speed.
  - `golden.json`: the real functions' answers on fixed inputs (the odds at 15 lucks, 300 sword values, offers, raises, picks, 60 order draws, prices after merges, heat times, levels, perks, the Cashier, reputation, the cart and the store's pack choice).
- **Freshness:** both files carry FNV-1a hashes of the 22 sources (16 `Shared` modules, 6 server scripts).

**In the vault, `Development/sim/`:**
- **`rules.py`:** the game's rules in Python. Each function names its Luau original, and every number comes from `balance.json`. `FakeRng` mirrors the export's stand-in Random, so random draws are compared draw for draw.
- **`test_parity.py`:** 25 unittest tests. They check `rules.py` against `golden.json`, check that both files come from one export, check that every gate and pad resolves, and run a chi-square test on 200,000 rolls each at luck 1 and 3.
  - **Result:** all 25 pass.
  - **Proof the tests bite:** five deliberate one-number errors (the customer preference bonus, the polish bonus, `MIN_COMMON`, the mail etch chance and the Cashier's default) were each caught. The etch chance needed an extra golden draw at 0.305, now in the export.
- **`check_export.py`:** compares the hashes Studio prints now with `balance.json`'s and lists every changed source.
- **`receive.py`:** the localhost receiver for the export.

**`economy_model.py` now reads `balance.json`:**
- **What it reads:** blueprint values, big swords, hilts, seat, etch, polish, rarities and odds (`rules.odds`), grade, heat times, crew levels and roster, merge luck and price, the VIP chance and share, customer shares (from the customer list), every pad and its gates, the cart levels, crew prices and gates, Advertising levels 0–3 and the reputation thresholds.
- **Its own guesses stay its own:** pace, pull time, the 1-in-3 big swords, and when gem levels are bought.
- **The game's 76 pads matched the model's hand-copied ones exactly** (Merge Ore Slots is free and comes with Ore Slot 6).
- **Rerun:** every line of output is identical, except the focused profile. Its "blueprints first" now takes the cheapest blueprint on offer instead of the first in list order (the export lists the Eastern pad first), so the Katana comes at 8 min (was 7) and the Gladius at 2 h 13 (was 1 h 50).

**To use:**
1. Run `python Development/sim/receive.py`.
2. In Studio (Edit), run `require(game.ServerStorage.Builders.ExportBalance:Clone())()`.
3. Stop the receiver.
4. Run `python -m unittest test_parity` from `Development/sim`.

Re-export after any balance change. A red test means the game and the simulator disagree.

**Next, step 2:** the event engine (`engine.py`), the six archetypes and the payer tiers (`behavior.py`), seeds and parallel runs (`run.py`), and the seven-metric report (`report.py`).

## Built: step 2, engine, archetypes, runs and report (2026-10-29)

**Export:** the export now also writes the template plot's layout, in plot space: the Smithy stations, each shop holder with its slots (and whether it's the Big Sword Stand), every pad, and the customer spawn, entry point and delivery bay.

**`engine.py`: one player, event to event.** The station flow comes from the server scripts:
- **Ore:** a pull rolls every ore slot, and an ore not collected is replaced by the next pull (ForgeService). The Auto Ore Roller pulls by itself and stops while a Rare+ ore waits.
- **Furnaces:** one ingot each. The first sword heats in 3 s (`FIRST_HEAT_TIME`), then each furnace follows its own Faster Heating chain.
- **The anvil:** the hilt is fitted there.
- **Finishing:** polish (+10%) and etch (+15%) per the archetype.
- **Shop holders:** a big sword goes only on the Big Sword Stand.
- **Customers** (ShopService):
  - The walk-in gap comes from Better Advertising (the tutorial's 12–22 s until the first letter), with Sunny weather and the Shop Promoter's perk applied.
  - The shop's room is 2, +1 with the Promoter, +1 per Rickshaw Bay.
  - A customer heads for a sword they like, otherwise a random one, walks in at 6 studs/s, looks for 2.5 s, then makes an offer (the first sale is the fair value).
  - You answer within 45 s (60 s for a VIP), or they leave. The Cashier answers from the third sale, at value +10% or over, into his till.
  - Declining may bring a raise. VIPs come at More VIPs × the Rainbow.
- **Letters:** the Iron Tantō letter 45 s after the first sale ends the tutorial; the Katana letter comes after 3 sales.
- **The crew** (EmployeeService):
  - **Crafters:** each takes the cheapest racked ingot, takes a free furnace (pulling out a ready ingot of yours that's been forgotten), hammers for its level's time, polishes if the station is bought, and racks the sword. It waits on `noIngots`, `rackFull`, `noRack` or `furnace`.
  - **Stocker:** carries one sword per trip to an empty holder, faster with levels.
  - **Etcher:** etches swords off the rack.
- **Cart:** Bulk Orders at 0.8×, never a big sword, with its trip time and 1 + n÷3 gems.
- **Weather:** a 5-minute spell, never the same twice in a row; Rain adds luck.
- **Merges:** Merge Ore Slots resets Ore Slots 2–6.
- **Passes:** the coin boost and Lucky Ore luck, Swift Boots walking at 20, the Starter Pack's 100 gems and Gold ingot.

**Walking:** plot-space distance × 1.3 detour ÷ walk speed.

**`timings.py`:** the hand-action seconds, all `ESTIMATE`. The report lists them.

**`behavior.py`:** the six archetypes and three payer tiers, with buy rules: cheapest, income-first, crew-first, blueprints-first, grinder (only what raises income or gates a sword) and manager.
- **Haggling is off for everyone.** Customers are the shop's limit, so a walk-off costs more than a raise brings; it can be turned on as a test.
- **The gem shop:** Better Advertising first, then More VIPs.

**`scenarios.py`:** `baseline`, `prices-10`, `prices+10`, `rare-odds+50`, `forge-20` (your forging and the crew's, ×0.8) and `values+10`.

**`run.py`:** every scenario × archetype × payer on the same seeds, in parallel. It writes `results/<name>/players.jsonl` (results are git-ignored, since the repo is public), `report.html`, and `Development/Sim Runs/<name>.md`.

**`report.py`,** the seven metrics:
1. Targets, with % reached by time and every milestone.
2. Swords made by 5/10/15/30/60 min, seconds per sword, and where the time goes.
3. Income over time, with a chart.
4. Each purchase's price in minutes of income, and its payback.
5. Stuck stretches of 10+ min, by period.
6. Luck percentile against milestones.
7. Crew waits, missed offers, empty-shop visits, sold, carted and walked off.

Scenario comparisons pair each seed with itself and use bootstrap 95% intervals: a change is "meaningful" only if the interval excludes 0 and the change is at least 5 min and 5%.

**`test_engine.py`:**
- The same seed gives the same player.
- Each archetype and payer's time adds up to the horizon.
- Coins and the shop's count never go negative.
- 28 tests pass, with the parity tests.

**Speed:** about 0.05 s for a 3-hour player, and 960 players × 6 h in 25 s on this PC.

**The empty shop:** Allen asked mid-step that customers keep coming to an empty shop. That's now built in the game, and the engine models it: such a customer takes a place in the shop for the visit and buys nothing.

**Not yet:** mail orders, cart Special Orders, daily gems, the workshop push, the measured timings (`PlaytestLog`) and offline time.

## The loop metric and the playtest timing log (2026-10-29)

Allen: "another important metric is doing the whole loop, from ore to placing it on the shelf and getting a sale. do we have that accounted for?" Then "yes" to adding it and building the timing log.

**The loop, in the engine:** every sword carries its times.
- Your own swords run from the ore collected to the sale. The crew's run from the ingot it fetched.
- The report's section 2b gives the median loop and its three parts:
  - **making:** ore to finished sword;
  - **getting out:** finished to on a holder;
  - **selling:** on a holder to sold.
- It also gives the first loop: first pull to first sale.

**`ServerScriptService.PlaytestLog` (Studio only):** `log(player, kind, data)`. Outside Studio it does nothing.
- **Events:**
  - pull, collect, furnace_put, furnace_take;
  - forge_begin, forge_finish (ingot id → sword id), polish_begin, polish, etch;
  - display, visit, browse, offer (answer and seconds), sale, buy.
- **Also logged:** every prompt used, and the player's position in plot space every second.
- **Sending:** batched and posted every 15 s, and when the server closes, to `receive.py`. If nothing is listening, the events wait (up to 50,000) and are sent on the next try.

**`receive.py`:** also takes `POST /playtest/<session>` and appends to `Development/sim/playtests/<session>.jsonl`, which is git-ignored.

**`calibrate.py`:** measures the hand times from the logs.
- What it measures:
  - forge and polish (server seconds);
  - etch, furnace and place (from the prompt to the action);
  - pull hold, collect gaps;
  - detour (path walked ÷ straight line between stations, from the positions).
- It also prints:
  - offer answer time and miss rate;
  - customers per minute and walking speed;
  - the ore-to-sale loop;
  - first pull to first sale.
- It writes `timings.json` with the median, 25–75% and n for each action. `timings.T` uses those medians over the estimates for any action with at least 5 samples.
- The report marks measured values with `*`.
- Not measurable from the server: hilt seat, rack, buy, menu, cart pack and letter. They stay estimates.

**Checks:**
- All seven scripts compile.
- The real module posted through the receiver into a session file, and calibrate read it.
- 29 tests pass, including `test_calibrate`.

**Not yet:** a real playtest. These are Allen's times, an expert's.

**Baseline rerun with the loop (`baseline-2026-10-29`; 5,400 players × 24 h in 11 min; free players, medians):**

- **First pull to first sale:** 1.2–1.4 min for every archetype.
- **Own sword, ore to sale:**

  | Archetype | Total | Making | Getting out | Selling |
  |---|---|---|---|---|
  | Casual | 6.5 min | 3.2 min | 1.2 min | 1.4 min |
  | Efficient | 5.8 min | — | — | — |
  | Rusher | 5.3 min | — | — | — |
  | Automator | 7.4 min | — | — | — |
  | Manager | 10 min | — | — | 6 min |

  The Manager's swords sell more slowly because his shop is always full and customers are the limit.
- **Crew sword:** 3–7 min. About 66 s of that is making; the rest is waiting to sell.
- **Grinder:** about 4.7 h from ore to sale, almost all of it getting out. Its policy buys no holders, so swords pile up. This is a behaviour artifact, not a game finding.
- **Targets:** the casual free player is still about 2× behind past Katana (Crafter 1 h 58, Longsword 2 h 54). The efficient player is near target.

**Playtesting from your save or after Reset progress (2026-10-29):** Allen asked whether either way affects the readings.

- **Action times:** either way works. Each is measured from its own start and end.
- **Logged with each event:** `pull` now carries `fresh` (the save's `completed == 0`) and `sale` carries `n` (the save's sales so far).
- **How `calibrate` uses them:**
  - The ore-to-sale loop restarts at the first fresh pull after a non-fresh one, because ids start over after a reset.
  - The first loop is the fresh save's first pull to its sale with `n == 1`. Sessions on an old save don't count toward it.
- **Checks:** 30 tests pass, including the reset case.

**Per-route walking times (2026-10-29):** Allen asked how movement is measured, for example shop shelf → ore roller. Then "yes" to timing each route.

- **Stations:** every logged action names the station it happened at:
  - OreRoller (pull, collect);
  - the furnace by name (`forge` on furnace_put and furnace_take);
  - Anvil, PolishStation, EtchingTable, shop (display);
  - IngotRack and SwordRack (the new `rack` event).
- **The time:** for two different stations in a row at most 90 s apart, the walk is the seconds spent moving between them (position steps over 2 studs/s). Standing at a picker isn't counted.
- **Route keys:** either direction counts as the same route (`timings.route_key`). Routes are kept apart from " upgraded" once the Upgraded Store is bought: `pos` carries `u`, and that purchase moves the workshop back.
- **Using it:** with 3 or more walks, a route's median replaces the layout's distance × detour. `timings.ROUTES` and `WALK_SPEED` feed `engine.walk`, which scales the time to that player's speed (Swift Boots).
  - Routes with fewer walks stay on distance × detour.
  - Staff walks never use these times.
- **Output:** `calibrate` prints each route against the layout's estimate.
- **Checks:** 32 tests pass (route measuring, and the engine using a measured route). The scripts compile, and a test log ran through calibrate.

**Automator guard (2026-10-29):** Allen: "give the Automator the same guard so it takes cheap buys while saving for crew".

**The change:** `behavior.choose_target` now gives "crew" the income rule's guard. A crew or rack goal costing more than 4× the cheapest buy + 2,000 waits, and the cheapest buy goes first.

**Effect** (`automator-strict` against `automator-guard`, 300 seeds × 3 payers × 24 h):
- All 900 players change their buy order. Typically they buy Furnace 2 heat before the Crafter, at about 45 min.
- Every milestone stays within ±2 min (paired 95% intervals), apart from all-passes Seraph at +5 min.

So the Automator's milestones don't depend on this. The baseline report predates the guard.

## Gems, mail orders, Special Orders and days (2026-10-29)

Allen: "Also do we account for gem spending? ... I think we should factor in the special orders, daily rewards as those are all part of the game. and anything else that a player might interact with."

**His answers:**
- Play: "1 h a day".
- Gem buys: "Differs by type".

**Every coin and gem source and sink in the game** (from the server scripts):
- **Coins** come from shop sales, the Cashier's till, letters, mail orders and the cart.
- **Gems** come from the daily reward, letters, mail orders, the cart and the Starter Pack (Robux packs aside).
- **Gems go to** the four gem upgrades and crew hires.

All of these are now modelled.

**Days:**
- 24 h of play = 24 days of 1 h (`behavior.PLAY_DAY`), each with a daily claim (`GemUpgrades.daily`: 5, 5, 10, 10, 15, 15, 30, looping).
- Between days, the cart comes back and the mail fills to More Clients' count. Both run on `os.time` in the game. Nothing else runs offline.

**Mail orders** (Shared/Orders, ShopService.refillOrders):
- They start Quicker Mail's gap after the first letter, while the mail has room.
- Each asks for one of your 3 best non-big swords (3:2:1), a metal you have collected (each rarity half as likely), and an etch 30% of the time once the Etching Table is bought.
- Pay: `Orders.pay` with a typical metal at your merge luck. Gems: 1, +1 for Rare+ metal, +1 if etched. Reputation: +3.
- **Chasers** (every type but Casual) keep an ore an open order asks for, heat it first, forge the order's shape, etch it if asked, and hand it in from the mail.
- **Casual** only hands in swords that happen to fit.
- No one declines orders.

**The cart** (Shared/Deliveries, DeliveryService):
- Three offers from `Deliveries.make`:
  - Bulk: any non-big sword, cap−1 to cap of them, 1 + count/3 gems.
  - Special: 2–4 of one shape with a twist, the order's gems + count − 1.
- Offers are refilled after each accept or skip.
- At the board the player takes the fillable offer with the most gems, packed with its cheapest fitting swords, skipping up to 3 offers. If nothing fits, they look again a minute later.
- The cart is collected at the bay when it's back (no longer automatic), paying its swords' value × 0.8, its gems, and reputation +1 per sword.
- Reputation (sale 1, order 3, letter 5, cart 1 per sword) feeds Special Orders: Rare at level 4+, +1 gem at level 5+.

**Gem shop:**
- Better Advertising I first, for everyone (the Guide's step).
- Then:

  | Types | Order |
  |---|---|
  | Manager, Grinder | Mail pair first (More Clients, Quicker Mail) |
  | Efficient, Rusher | Customers pair first (Better Advertising, More VIPs) |
  | Casual, Automator | Cheapest next level (Automator wasn't stated) |

  Within a pair the cheapest level goes first; when the pair is maxed, the rest.
- Gems are kept back for the next crew hire whose gate is open.

**Parity:** `rules.make_delivery`, `order_fits` and `daily` are checked against new golden vectors (`deliveryMake`, `orderMismatch`, `daily`). The export now has `deliveries.senders`. 28 parity tests pass, 35 in all.

**Report:** a new section 8 shows:
- gems in by source and out by sink, what's left, and gem shop levels;
- mail orders and their share of coins, orders open at the end;
- Bulk and Special trips, skips and reputation.

**Targets changed (2026-10-29).** Allen: "the katana target ideally should be 15 minutes ... sword crafter should take about 1h 30 minutes, long sword could come at 40 minutes."

`report.TARGETS` is now:

| Milestone | Target |
|---|---|
| Katana | 15 min |
| Longsword | 40 min (now before the Crafter) |
| Sword Crafter | 1 h 30 |
| Falchion | 4 h |
| Gladius | 6 h 20 |
| Zanbatō | 8 h |
| Seraph | 20 h |

These are still for a casual player, and there are still only these seven. Every other milestone is reported without a target. Runs before this were scored against the old targets (Katana 20 min, Crafter 1 h, Longsword 1 h 45).

**All targets (2026-10-29).** Allen asked for targets beyond the seven ("crew hires, Stocker, Cashier, merges, gem levels"), then: "Use the proposed targets as they are."

Hours of play for a casual player (`report.TARGETS`; at an hour a day, hours are days):

| Milestone | Target |
|---|---|
| Katana | 0:15 |
| Longsword | 0:40 |
| Sword Crafter | 1:30 |
| 1st merge | 2:00 |
| Haru (2nd crafter, Anvil 3) | 3:00 |
| Every gem upgrade at Lv. 1 | 3:00 (day 3) |
| Stocker | 3:30 |
| Falchion | 4:00 |
| 2nd merge | 4:00 |
| Mei (3rd crafter, Anvil 4) | 6:00 |
| Gladius | 6:20 |
| Shop Promoter | 6:40 |
| 3rd merge | 7:00 |
| Cashier | 7:30 |
| Zanbatō | 8:00 |
| Sword Etcher | 8:30 |
| The type's gem pair at Lv. 3 | 10:00 (day 10) |
| Kenji (4th crafter) | 10:30 |
| Rin (5th crafter) | 12:30 |
| Seraph | 20:00 |
| One gem pair at Lv. 5 | 20:00 (day 20) |

**Where the new times come from:**
- Most follow the Upgrade Order Review's decided plan: the first merge about 2 h in, three crafters by about 6 h, and its Promoter, Etcher, Kenji and Rin times.
- The Stocker frees you once two crafters run.
- The Cashier comes before the Zanbatō.

**How the gem targets are measured:** `engine.gem_milestones` adds them to each player's milestones.
- `GemsAllLv1`: all four upgrades at Lv. 1.
- `GemPairLv3`: both of the type's pair at Lv. 3. A cheapest-first buyer counts whichever pair gets there first.
- `GemPairLv5`: any pair at Lv. 5.

**Conflict:** with the pair-first gem order, Manager, Grinder, Efficient and Rusher never buy the other pair's Lv. 1 until their own pair is maxed. "Every gem upgrade at Lv. 1 by day 3" can't be met by that buying rule as it stands.

**Report:**
- Section 1 now lists the targets as rows, with each group as a column.
- The vault note has one table per payer.

**Also fixed:** a simulator bug. The Katana letter was offered only at exactly the 3rd sale, and only if the first letter was already done, so about 14% of players got it. The game checks after every sale; now every player does.

**Baseline with gems, mail, Special Orders and days** (`baseline-gems-2026-10-29`; 5,400 players × 24 h in 32 min; free players, medians; the scores are in [[Development/Sim Runs/baseline-gems-2026-10-29]]).

**Against the targets:**
- **Casual** is behind on every target: Katana 28 min (target 15), Longsword 2 h 53 (40 min), Crafter 1 h 57 (1 h 30), Falchion 8 h 46 (4 h), Gladius 15 h 56 (6 h 20).
- **Efficient** beats most crew targets but never buys the Cashier in 24 h, and gets the Promoter at 18 h 46. Its buy rule ranks them low.
- **Longsword at 40 min:** only the Rusher (29 min) reaches it. Every other type takes 1 h 11 to 2 h 53.
- **Gem targets** are mostly unmet. A free player earns 295–600 gems in 24 h, against 3,330 to max the gem shop.

**Against the earlier baseline:**
- Gems, mail and the real cart made no type faster. Gladius moved +5 to +136 min (Automator +136, Grinder +99).
- Chasing mail orders costs forge time for little: mail is 4–11% of coins.
- This comparison also includes the Automator guard, the walk-in rule and the Katana letter fix, all small on their own.

**Special Orders are a gem farm.**
- The Manager runs about 290 Special Orders in 24 h, for about 1,500 gems (1,847 gems in all; other types get 295–597).
- Skipping offers is free and instant, so it skips until a Special it can fill comes up. A Special pays its order's gems + count − 1 (4–6 gems for 2–4 swords), against 1 + count/3 for a Bulk Order.
- This is a game rule, not a simulator artifact.

## Special Order gem farm: fixes compared (2026-10-29)

Allen: "Yes, propose fixes". Five rules were run as scenarios (sim only; none is in the game) on `cart-gem-fixes`: 150 seeds × Manager, Automator and Efficient, free, 24 h. The run used the estimated hand times.

Manager figures are medians; the milestone change is paired against the game's rule today:

| Rule | Cart gems | All gems | Specials | Gladius | Zanbatō |
|---|---|---|---|---|---|
| Today (instant free skips) | 1,512 | 1,849 | 290 | — | — |
| No skipping | 11 | 344 | 0 | +74 min | +5 h 24 |
| A skipped offer's replacement comes 5 min later | 864 | 1,203 | 122 | +3 | +11 |
| A Special pays its order's gems only (1–3) | 924 | 1,264 | 288 | 0 | 0 |
| Cart gems capped at 20 a day | 420 | 753 | 290 | 0 | +1 |
| 5-min skip wait + order's gems | 611 | 947 | 119 | +3 | +10 |

**Other types:**
- The Automator and Efficient barely use Specials: 66 and 11 cart gems.
- Every fix leaves them within 4 min, except no-skipping, which slows the Automator's Falchion by 80 min.

**Reading it:**
- Removing skips stops the cart for everyone, so skipping is needed.
- The 5-min wait plus the order's gems brings the Manager to about 2× the other types' gems with almost no slowdown. It also uses a pattern the game already has: mail's timer between letters.
- The 20-a-day cap is the strongest cut and the simplest number, but it's a hidden ceiling unless the board shows it.

**Also (2026-10-29), calibrate fixes from Allen's first playtests:**
- An action straight off its prompt (taking from the furnace) now times as 0 instead of from the previous prompt.
- Placing a sword (the on-screen +, not a prompt) times from when the player stops walking.
- Two sessions (8 min) replaced 6 estimates and 5 routes: forge 11.1 s (was 22), and ore roller ↔ shop 11.1 s (the map's straight line said 3.8).

**Offer habits and the cart visit, from playtests (2026-10-29).**

*Offer habits* (Allen: "Yes, use mine"):
- `calibrate` writes `offers` to `timings.json` once 10+ offer cards are seen: the median answer and the share missed (now 9.47 s, 41.9%, n 31).
- `behavior.offer_habits` gives each type a miss chance and a mean answer time (the median ÷ ln 2), times `OFFER_SCALE`:
  - Casual: ×1.25 miss, ×1.5 time;
  - Manager: ×0.5 both;
  - the rest as measured.
- An answer now always lands before the card's timeout.

*The cart visit* (Allen: "yes" to measuring the whole visit):
- `cart_pack` (per sword) is gone, because Auto-Fill packs the crate in one tap.
- `cart_visit` (estimate 8 s; 1 sample, 3.3 s) times the board, from its prompt to the cart leaving. The engine adds it once per send.
- Collecting is just the walk, since the board's prompt pays at once.
- A look at the board with nothing to fill still costs `menu`.

The `baseline-measured-2026-10-29` run was started before the cart change: it uses the measured hand times and offer habits, with the old per-sword packing (1 s a sword + 3 s).

**Allen's own times for what the server can't see (2026-10-29):** "seating the hilt is part of the anvil station now. and it takes basically 0.5 seconds. letters and cart visits take minimal time, the GUI is probably open for like 3 seconds".

New estimates:

| Action | Was | Now |
|---|---|---|
| `hilt_seat` | 3 s | 0.5 s |
| `letter` | 2 s | 3 s |
| `cart_visit` | 8 s | 3 s |

A measured median still replaces any of them once it has 5 samples (`cart_visit` has 2, at 4.4 s). `menu` (gem shop, crew window) stays 3 s.

**Engine speed-ups (2026-10-29).** Allen: "Yes, speed it up". Grinder and Manager players make about 4,700 swords in 24 h and were the slow part of every run.

**Changes:**
- `mail_fit` checks only swords of a shape an open order asks for; it was every sword against every order at every decision.
- `offers` rebuilds the pad list only after a purchase (`bought_n`).
- `best_bp` is cached by the number of blueprints known.
- `on_stocker` lists the free holders once per wake.

**Result:** identical to before on 12 test players (milestones, sales, carts, mail, coins, gems, swords made), and 1.8× faster (49.6 s → 28.1 s).

## Run on the current game, with a shop counter scenario (2026-10-29)

`current-2026-10-29-pre-queue`: 200 seeds × 6 types × 3 payers × 2 scenarios, 24 h. It used:
- Allen's captured timings and offer habits;
- the export with his Cashier (50,000, after the Stocker) and Promoter (40,000, after the Longsword) and Polishing Station 2.

**The Cashier and Promoter cuts fixed those targets** (free, old prices → new):

| Type | Promoter | Cashier | Zanbatō |
|---|---|---|---|
| Casual | 11:56 → 6:16 | 15:35 → 8:10 | — |
| Efficient | 12:31 → 5:59 | 15:35 → 6:42 | 15:59 → 8:47 |
| Rusher | — | — | 9:59 → 7:30 |

**Shop counter** (`offer-counter-25`; Allen: "maybe with the visible customers count, we can say that the percent goes down to 25%"). The miss base is 25% instead of the measured 39%.

Casual, free:
- sold 1,388 → 1,745; missed 1,289 → 794; earned 6.2M → 7.0M;
- Longsword −15 min, Crafter −14, Falchion −29, Gladius −45, Cashier −30, Zanbatō −71.

Other types gain 2–51 min on the same milestones, more the later the milestone.

**Still missed (free):**
- Casual: Katana 25 min, Longsword 2:37, Crafter 1:49, and 1.5–2× on most later targets.
- Every type: the Sword Etcher (12–21 h against 8:30).
- The Rusher gets its crew late (Crafter 5:44, Mei 20:17), which follows from its rule.

**Simulator fixes found in this run:**
- A sword forged for a mail order that another sword filled first stayed tagged forever. The shop step then looped at zero seconds (4 Manager players hung). Fixed: filling an order frees any sword made for it, and the shop step counts only swords it can place.

**Game changes from another session during the run, now modelled:**
- The Starter Pack is 100 gems and 10,000 coins (no Gold ingot). The other session updated `engine.run` itself.
- A queued cart order: packed while the cart is out, sent when it's collected (`task_cart(queue=True)`, `cart_queue`, `send_cart`).
- The run was redone as `current-2026-10-29`.

**Hang guards (2026-10-29).** Allen: "make sure there's no hangs like last time, if it takes too long find out why".

- `engine.run` raises if 20,000 events in a row happen at one instant: a loop that takes no time.
- It also raises past `wall_limit` seconds of computer time; `run.PLAYER_LIMIT` is 120 s, against about 3 s for a 24 h Manager.
- `run.work` catches either, skips that player, and prints `SKIPPED <scenario> <type> <payer> <seed>: <why>`. The run carries on, and the final line counts the skips.
- Both guards were checked to fire.

**`current-2026-10-29`** (the rerun with the queued cart and the 10,000-coin Starter Pack): 7,200 players, no stalls (watched).

**Against the run before:**
- The queued cart changed almost nothing: carts per type are within 1%, and every free milestone is within 10 min.
- The Starter Pack (paid tier): Katana at 0–1 min for everyone, and a casual Crafter at 1:24 (on target).
- 100 gems buys every gem upgrade's Lv. 1 at once for cheapest-first buyers.
- The free tables and the shop counter effect stand as reported (counter, Gladius: Casual −44 min, Automator −35, Rusher −20, Efficient −11, Grinder −11, Manager −8).

## The 40-minute Longsword: fixes compared (2026-10-29)

Allen chose this miss to work on.

**Cause:** the Longsword path costs 23,660 coins (Wakizashi 60, Machete 600, Scimitar 6,000, Longsword 17,000). A cheapest-first Casual buys 38 other things for 116,000 coins first; Efficient buys 36 for 97,000. Only the Rusher (swords first) buys it early.

**Scenarios** (`longsword-fixes`, `longsword-fixes-k`; 150 seeds, free, 8 h; `engine.pick_target` honours `raw["goalFirst"]`):
- `ls-path-60`: Machete, Scimitar and Longsword at 60%.
- `ls-pinned`: players buy the Machete → Scimitar → Longsword path as soon as each is on offer, as if a pinned next goal were followed.
- `ls-pinned-k`: the same with the Katana pinned first.
- The `+path-60` variants combine both.

Median, with the share of players on target:

| | Katana (0:15) | Longsword (0:40) | Crafter (1:30) |
|---|---|---|---|
| Casual, today | 0:25 (1%) | 2:37 (0%) | 1:50 (7%) |
| Casual, path 60% | 0:24 | 1:54 (0%) | 1:45 |
| Casual, pinned (no Katana) | 1:00 | 0:54 (10%) | 1:51 |
| Casual, pinned with Katana | 0:11 (85%) | 0:48 (19%) | 1:47 (7%) |
| **Casual, pinned with Katana + path 60%** | **0:11 (85%)** | **0:35 (73%)** | **1:36 (31%)** |
| Other types, that last fix | 0:06–0:08 (100%) | 0:16–0:24 (100%) | unchanged or earlier |

**Reading it:**
- The order players buy in is the lever. A price cut alone doesn't move Casual.
- Pinning the Longsword path without the Katana delays the Katana for everyone.
- Pinned with the Katana first, plus the 40% cut, hits the Katana and Longsword for most casual players and nothing later slips: Haru, Falchion and Gladius all come a little earlier.

**Caveat:** "pinned" assumes players follow a next-goal pin. The game has no such pin. On 2026-10-28 Allen chose "two stages open" over "one stage plus a pinned next goal" in the Upgrade Order Review.

**How far players get (2026-10-29, `current-2026-10-29`, free, 24 h):**
- **Casual:** the Rapier at most (100%, 20:54); the Hook Sword 10%; no fantasy swords.
- **Automator:** the Claymore (98%); Crescent Fang 38%.
- **Grinder:** through the Leviathan (22:46).
- **Efficient, Rusher, Manager:** every sword including the Seraph, at 20–22 h. Their first fantasy sword, the Crescent Fang, comes at 10:30–14:20.

**Longsword path at 60% in the game** (Allen: "i think we should lower the costs for now"): Machete 360, Scimitar 3,600, Longsword 10,200. Re-exported; parity passes.

## Until every pad is bought; sitting back (2026-10-29)

Allen: "is it possible to run the experiment until they all reach the last upgrade", then "once players get automated employees, the actual player production tends to fall off. they like to just sit back and collect money".

**Run until done:** `run.py --until-done` (with `--hours` as a cap and `--player-limit`). `engine.Sim.until_done` stops a player once every non-decor pad (the repeatable merge aside) has been bought once, and marks `AllPads`. The result's `horizon_min` is then the stopping time.

**Sitting back** (`behavior.Archetype.sit_back`, my estimates):

| Type | sit_back |
|---|---|
| Casual | 0.7 |
| Automator | 0.8 |
| Efficient, Rusher, Manager | 0.3 |
| Grinder | 0 |

- It scales by a third each for the Sword Crafter, Stocker and Cashier.
- At each decision, with that chance (`engine.sitting_back`), the player starts no sword of their own. They still rack ingots or pull ore for the crew when the rack has room; otherwise they idle 30–120 s.
- `no-sit-back` turns it off, which is the engine as it was before.

**Also fixed:** the Grinder now buys the rest, cheapest first, once only ore slots and merges are left in its kinds. They come back after every merge, so before, it never finished.

**Result** (`until-done-2026-10-29`; 150 seeds × 6 types × free and all passes × with and without sitting back; 3,600 players in 12 min; all finished):

| Type | Free: every pad | Without sitting back | All passes |
|---|---|---|---|
| Casual | 45.6 h | 45.4 h | 27.0 h |
| Efficient | 22.6 h | 21.6 h | 12.6 h |
| Automator | 42.5 h | 38.5 h | 25.4 h |
| Rusher | 22.9 h | 21.1 h | 12.6 h |
| Grinder | 27.0 h | 27.0 h | 14.4 h |
| Manager | 23.4 h | 21.9 h | 13.0 h |

At an hour a day, a free player finishes in about 3 weeks (Efficient, Rusher, Manager) to about 6 weeks (Casual).

**Sitting back halves a Casual player's own swords** (3,300 → 1,618) but delays the finish by only 0.3 h; the Automator by 4 h. By then the crew makes most swords, and the shop sells about 100 an hour, limited by customers: the late game is limited by customers, not by making swords.

**Last pad bought:** the Seraph (600 of 900 free players) or the Sword Etcher (300).

## Late swords cheaper (B), mail gems, gem use (2026-10-29)

**B** (Allen: "Do B"). The `late-swords-25` scenario prices each sword after the Gladius at about 25 min of an Efficient player's income when it's bought; they cost 29–72 min.

| Sword | Now | B |
|---|---|---|
| Khopesh | 190,000 | 160,000 |
| Dadao | 240,000 | 170,000 |
| Zanbatō | 300,000 | 250,000 |
| Rapier | 380,000 | 270,000 |
| Hook Sword | 520,000 | 290,000 |
| Claymore | 700,000 | 340,000 |
| Crescent Fang | 700,000 | 370,000 |
| Shard Blade | 900,000 | 400,000 |
| Flamberge | 950,000 | 430,000 |
| Moonbite | 1,100,000 | 530,000 |
| Serpent | 1,350,000 | 570,000 |
| Leviathan | 1,650,000 | 640,000 |
| Thornspire | 2,000,000 | 740,000 |
| Seraph | 2,400,000 | 840,000 |

Run until done (free, 150 seeds):

| Type | Every pad: now → B | 10-min stretches with something new after 16 h |
|---|---|---|
| Efficient | 22.6 → 15.9 h | 25% → 67% |
| Rusher | 22.9 → 14.9 h | 24% → 67% |
| Grinder | 27.0 → 16.9 h | 24% → 66% |
| Manager | 23.4 → 16.7 h | 24% → 46% |
| Automator | 42.5 → 31.2 h | 23% → 34% |
| Casual | 45.6 → 34.0 h | 22% → 30% |

- Hours 8–16 move less (Efficient 33% → 44%).
- Nothing before the Gladius changes.
- The game is about 30% shorter.

**Casual and mail orders** (Allen: "we can assume casual players will do a mail order 10% of the time"): `Archetype.mail` is now the share of orders worked on (Casual 0.1, the rest 1.0). Each new order rolls `chase`; any order still takes a sword that happens to fit.

**Sitting-back bug:** a player sitting back racked the ingots kept for mail orders, so Efficient fell to about 40 orders a day. Now an order's ingot is still heated and forged (138–208 again). The `until-done-2026-10-29` and `late-swords-25` runs had the bug, so their mail gems are low; their finish times move by under an hour.

**Gems to the end** (`gems-to-end`; free, until done; with and without `mail-gems-x2`, mail orders paying double gems):
- **No type maxes the gem shop before owning every pad** (0%). By then a Casual has 4/3/3/3 of the four upgrades; Efficient and Rusher 4/4/0/0 (customer pair first); the Manager 1/0/4/4.
- 60–250 gems are unspent at the finish (saving for the next level or a hire).
- Gems never run out of use within the game. They're the scarcer currency all the way through.
- **Double mail gems:** +200–700 gems for the types that work orders (Automator 1,620 → 2,143, Grinder 2,403 → 3,009), about one more gem level each, and 0.1–1.6 h earlier to finish. Casual gets nothing (3 → 6 mail gems): it works only 10% of orders.
- Gems by source to the finish (Efficient): daily 275, letters 5, mail 236, cart 601.

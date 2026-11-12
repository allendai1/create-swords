---
title: Major Updates Plan — 2026-11-07
type: design
status: proposal
updated: 2026-11-07
tags: [design, roadmap, create-swords]
---

# Major Updates Plan — 2026-11-07

Three post-launch updates for Allen to decide on. **Proposal only:** nothing here is built, no price or product moved, nothing changed in Studio. Each builds on a system already in the place and says what the sim must learn (`Development/sim`, [[Development/Gameplay Simulator Plan]]). Checked against [[Design/Decisions Log]], [[Design/Monetization Plan]] §7–8, the Don't list in [[Design/Monetization Ideas — 2026-10-31]] and the guardrails in [[Archive/Design/Urgency Review#5. Guardrails]]; where an idea touched one of them it is reshaped and the ruling named.

## 1. Why these three

- **The first session is in hand; the week after it isn't.** First sale about 1:30, the lessons end on the gem buy, the Sword Crafter at 15–21 min for engaged players and 35 min casual ([[Development/Sim Runs/notes-2026-11-05]]). What the sim can't show is who comes back on day 7 and day 30.
- **The trough is the D7 problem.** 28 buys before the Longsword, then 22 ordinary buys and 6 milestones over 4 h → 20 h; at the vault's late waits that stretch wants ~40 more buys, ~17 of them between the Crafter and the Zanbatō; the Seraph isn't reached in 22 h; casual players stall after ~6 h ([[Design/Upgrade Time Model — 2026-11-02]]: "Content, not prices, is the late-game gap"; [[Sessions/2026-10-30#The trough after the Zanbatō, simulated]]: "the trough can't be priced away without shortening the game"). At Allen's "1 h a day" (the sim's `PLAY_DAY`), 4 h is day 4 and 6 h is day 6.
- **What the LihFolk vault says moves each window** ("Retention and Return Hooks"): D1 the first session and an unfinished goal; D7 progression with visible next steps, weekly goals, collections; D30 updates, live events, seasons, social. Roblox's cadence through the same note: small updates every 2–4 weeks, big ones every 2–3 months. "Genre Playbook - Tycoons": "once the plot is finished, the game is finished, unless rebirth, upgrades, decoration or competition continue it". Rebirth is ruled out (Merge Ore Slots is the one exception), so content and events have to.
- **Legendary Commissions** fills 4–20 h with goals that aren't price hikes (D7). **Village Festival** gives D30 a calendar beat and a shared place: the plaza, yagura and stalls are built and "nothing walks it" ([[Sessions/2026-11-04#Map pass 1: Blender stalls and banners, yagura, carts, warmer road]]). **Trade Routes** deepens 1–6 h, is Allen's open ask ("think of other ways to make delivery an important part of the game", [[Design/Delivery Ideas — 2026-11-05]]) and brings the one return hook the game lacks: something earned while away.
- None needs a reset, a new currency, player trading or a new material-tier gate. The sim counts a letter or an order as a goal the way it counts a buy, so each update's section ends with what `rules.py`, `engine.py` and the balance export must learn.

## 2. Legendary Commissions — the late-game update

**The hook:** "Zaro wrote to me. He wants a sword only I can make."

**What the player does**
1. After enough VIP sales, a named VIP sends a personal letter: a known sword, in a metal you've already found, with their finish ask (polished, or an etch).
2. Roll for it (the ore says "<name> wants this!"), forge and finish; the quest board tracks it like any letter.
3. Hand it in through the mail's picker: order pay × the shop boost, plus gems, plus a line from them.
4. The chain's third letter rewards a blueprint nobody can buy (one of the waiting fictional swords) or a trophy; a thank-you letter follows, and that VIP walks in again paying at the top of their range.
5. Meanwhile the hidden clock already in the game runs on: a Strange letter at 2–4 h and a Legendary one at 6–10 h of play, surprises like the Butter Stick's.

**Content**
- **Two more secret letters** on the built tiers ([[Sessions/2026-11-07#Secret letters built; the Butter Stick comes from Kenta's letter]]; Allen: "secret swords can also have tiers behind the scenes so rarer ones can be even less frequent"): Strange (2–4 h) → **Sakabatō** ("Easy (flip the curve)", [[Design/Sword Profile Ideas#Fictional]]); Legendary (6–10 h) → **Moonhook** (the tip curls back; a new hook feature). Senders: Musashi for the Sakabatō (he's in `Shared/Senders` and never writes), a new one for the Moonhook.
- **Four VIP commission chains, 3 letters each** (Claude's pairing, Allen's call): Zaro → **Twin Fang**, Renguko → **Ember Tongue**, Myhawk → **Sawtooth**, Tenjiro → a Smith's Mark (a nameplate frame and a wall plaque, no sword). Letter 1 wants a known sword in a Rare+ metal you've found; letter 2 an Epic+, polished; letter 3 a Legendary you've found, polished and etched. Every want is a metal already in your Book, as `Shared/Orders` does today, so no letter can strand you. Pay 1.2× value × shop boost (as orders) + 5 / 10 / 20 gems; the thank-you letter 20 gems and the frame.
- **Gates:** a chain opens on total VIP sales (shop offers accepted + VIP mail orders filled) of 5 / 15 / 30 plus a play-time floor of 1 / 3 / 6 h, and its letters arrive inside a 40–60 min window after the gate, as `secretAt` does, so they still feel like surprises. The VIP who writes is the one you've sold to most. Reputation can't be the gate: good players max Rank 8 by about 2 h ([[Design/Monetization Ideas — 2026-10-31]] §2a), so it only opens chain 1. Chains run one at a time: chain 1 about 1–4 h, chain 2 4–8 h, chain 3 8–14 h, chain 4 14–20 h; the Strange letter 2–4 h, the Legendary 6–10 h.
- **What it does to the trough:** 9 chain letters, the Legendary letter, 3 thank-you letters and 3 blueprints between 4 h and 20 h, each a 20–40 min craft-and-wait with the metal roll inside it. With the 22 late buys that is ~38 goals over 16 h, about one every 25 min against ~44 min today. It halves the gaps; it doesn't close them. An earlier Seraph target (~10 h fits today's content at the vault's waits) stays Allen's call from [[Design/Upgrade Time Model — 2026-11-02]].
- **Learned swords' value** (Claude's default): a learned sword's base value sits just under the pad sword players typically hold when it arrives, so it's a new thing to make, train a crafter on and sell, not a free top sword; the Butter Stick (the Katana's 110) already follows this. The sword chain stays one chain: none of these is on a pad; they sit last in the Book like the Butter Stick.
- **The "early outsider"** (GDD §7, [[Development/Roadmap#4. Crafting, economy and customer progression]]) is the Night Knight's chain in a later drop: letters about the Western swords you already buy. No new tradition system.
- **Where it lands against the ladder:** Katana 0:12–0:19, the Crafter 15–35 min, Longsword ~0:47, chain 1 from ~1 h, the Strange letter 2–4 h, Zanbatō ~4 h, chain 2 4–8 h, the Legendary letter 6–10 h, chains 3–4 8–20 h, Thornspire 16–18 h.

**Systems reused and new**
- Reused: `Shared/Commissions` (`title`, `rewardBlueprint`, `secret`, `SECRET_TIERS`, `nextSecret`, `due`), `ShopService.secretLetter` on the mail clock, `Shared/Senders` (23 senders with portraits, the 12 VIPs since [[Sessions/2026-11-07#VIPs send mail]]), `Shared/Customers` (`vips`, `pick`), `Shared/Orders` (metals from the Book), `SmithyCore` (`secretAt`, `played`), `MailController` and the quest board, `SecretUnlockGui` / `SecretUnlock` (the card), `CollectionController` (secrets last), `Blueprints` / `BladeData`, `SwordMeshCache` and the Sword Mesh Pipeline, `EmployeeController` (hides a secret shape until made), the Dialogue Editor for every line, `Analytics` (a funnel per letter like MailOrder).
- New: `Commissions.CHAINS` (per-VIP letter triples with gates), a `SmithyCore` save field `vipSales` (a count) and chain statuses, a letter with no ask (the thank-you: Accept claims it), the plaque and frame as Studio templates, five blade profiles: Sakabatō and Ember Tongue are "Easy" / "Care"; Twin Fang, Moonhook and Sawtooth need fork, hook and serration features in `BladeCore` and Blender hilts like the seven fictional swords'.

**Monetization within the rules:** nothing is sold. VIP (VIP customers twice as often) and More VIPs speed the gates ("speeds things up"); 50% More Coins applies to the letters' coins as to orders; the frames are earned, as [[Design/Monetization Ideas — 2026-10-31]] #18 wants ("others earned at milestones"). No Robux on a letter, no skip.

**Phone and performance:** letters, portraits and the card exist; the new blades are baked meshes (`SwordMeshSpec`); three more Book entries; the quest board shows 2½ slips on phones, so a chain letter plus two orders still fits; no new HUD.

**Risks and Allen's calls**
1. Under your best pad sword, or free to beat it? (Q5)
2. 4 chains (12 letters of text) or all 12 VIPs (36)? (Q6)
3. Ship Sakabatō and Ember Tongue first and the three feature blades in a second drop?
4. Letter text about anime-inspired VIPs: Claude's lines, "no quotes from the shows" as on 2026-11-07. OK?
5. Should letter 3 ask for a Legendary you've found (1% base, 13 Legendaries; hours at low merges) or any Epic+?

**Build:** 6–8 sessions: letters and the two easy blades (1); `vipSales`, the chain scheduler and thank-you letters (1–2); the three feature blades and hilts in Blender and `BladeCore` (2–3); plaque, frame, Book and card (1); text in the Dialogue Editor, play-checks, sim (1).

**Play-check:** Dev Panel → Secret letter twice: Strange then Legendary arrive in order, each wants a sword you can make, the card pops, the Book lists them last; Send VIP and sell until chain 1's first letter comes; its ore says "<VIP> wants this!"; hand in; the thank-you letter; that VIP's next walk-in; a crafter trained on the Sakabatō; Reset progress clears `vipSales`; phone: a chain slip with two orders on the quest board; all 25 + 5 blueprints in `ForgeCheckSpec` and `SwordMeshSpec`.

**Sim:** the export's `commissions` gains the chain letters (giver, wants, gems, `vipSales` gate, floor, `rewardBlueprint`); `rules.Balance.letters_due(statuses, vip_sales, played)` mirrors `Commissions.due` / `nextSecret`; `engine.Sim.on_answer` counts VIP sales, `maybe_katana_letter` / `task_letter` / `on_letter` become one `next_letter()` over story, chain and secret letters (the Butter letter is "not in the sim" today: add it), and a taught `rewardBlueprint` reaches `best_bp` and the crafters; `pacing.py` gets a row per letter and blueprint; re-export `golden.json`, `test_parity` and `test_engine`. Check: waits over 15 min between goals (letters count) per type, Seraph time unchanged, casual players reach chain 1 by 6 h.

## 3. Village Festival — the live-ops update

**The hook:** "It's the Koi Festival this week. The stalls want koi-steel katanas."

**What the player does**
1. Join during a festival: a banner like the weather's ("[Festival] Koi Steel in the roller until Sunday"), the plaza lit, a drum at the yagura.
2. The festival metal is in the roller: an Epic, in Epic's pool only, so the rarity odds and the odds board are unchanged.
3. The festival board at the yagura posts two orders a day ("3 Koi Steel swords", "a polished Legendary"); hand in through the picker for coins × shop boost and gems.
4. The stall sells the festival's three cosmetics for gems or Robux: a shop banner, a lantern string for your bay, a nameplate frame. Gone when the festival ends, back next year.
5. The Smith's Season (4 weeks) counts forges, sales, carts and festival orders toward 10 free tiers and 10 premium ones.

**Content**
- **Four festivals a year, about 10 days each,** one metal each from [[Design/Metal Ideas]]: spring **Koi Steel** (koinobori; texture made 2026-11-05, not kept), summer **Kitsunebi** (foxfire; made, not kept), autumn **Pumpkin**, new year **Firework** (both on the events list, not made). Sakura and Candy are permanent metals since 2026-11-04, so they can't be the event ones. The metal is an Epic for the festival; ingots and swords keep it afterwards; the Book card keeps a festival stamp with the month.
- **Per festival:** 6 festival orders over the 10 days (2 standing, refilled daily, wanting known swords, often in the festival metal, paying like orders + 4 / 6 / 10 gems); 3 cosmetics at **60 / 120 / 200 gems or 99 R$ each** (the "earned or bought" item, [[Design/Monetization Ideas — 2026-10-31]] #16); the stall's dressing (lanterns lit at night, a drum loop); one Roblox Experience Event with Notify Me and a 60-character update announcement.
- **Smith's Season** (#11 there, after Roblox's guidance via LihFolk "Battle Pass and Season Design"): 4 weeks on, 1 week off; 10 tiers; three daily missions from the game's own verbs (forge N swords, serve N VIPs, send N carts, fill a festival order), none needing gems; free track coins, gems and the festival banner; premium **399 R$** adds two cosmetics (a roller paint, a crew hachimaki) and gems capped at about three days' income; buying premium late grants the tiers already reached; unclaimed rewards are granted at season end; no tier skips (Grow a Garden sells them at 49 R$; our Don't list says no skips). The first season starts with the first festival.
- **Not a fifth weather.** [[Design/Monetization Ideas — 2026-10-31]] floated "Festival" as a weather with crew XP ×2 if Allen wanted a crew event; the same note's Don't list rules out crew XP boosts (a third path to crew levels, +1–3% coins). The festival's bonus is the metal and the orders, and weather stays bonus-only.
- **Where it lands:** after the lessons for everyone (the guardrail: nothing in the first session before Ore Slot 2); the festival metal appears after the tutorial's fixed pulls; orders want known swords, so a 20-minute player can fill one; the Season counts from the first session; cosmetics are the first gem sink before the Gem Shop's 990 is done.

**Systems reused and new**
- Reused: `ServerScriptService.Weather` and `WeatherController` (attribute + end time + banner, "[Sunny] 2x Customers" since 2026-11-02) for a `Festival` attribute the same way; `Shared/Materials` pools and `ForgeService.rollFor`; `Shared/Orders` (`make`, `prose`, picker hand-in) for festival orders; the board pattern from `DeliveryController` for the yagura board; the WorldStore spot pattern (the odds board's Buy → Roblox's prompt) for the stall; `GemService` for gem spends; `StoreService.ProcessReceipt` and a `starterGranted`-style flag for the premium product; `PlaytestLog` / `Analytics` kinds (forge, sale, cart, buy) as mission events; `PlotService`'s nameplate for frames; `SmithyCore` save fields `festival` (stamps, cosmetics) and `season` (id, points, claimed); the Shop's card style for the Season window; Roblox's Experience Events, notifications (13+, one a day) and update announcements ("Live Ops Events and Updates").
- New: a live calendar (a DataStore key read on server start plus a MessagingService push, "Global State and Live Config"; fallback a table shipped per update), the festival board (Blender), three cosmetics a festival, the Season window and missions.

**Monetization within the rules:** everything is earnable (free track, gems); premium is cosmetics and gems only, no power, odds or skips; the end date is shown plainly, no "last chance" copy, nothing restarts (Roblox's timer rules via "Limited-Time Offers - Design and Ethics"; [[Design/Kids and Reward Loops Research — 2026-10-31]]: no fake urgency on anything paid); the stall doesn't badge every session. A festival metal is not a paid random item: no purchase touches the odds, and Lucky Ore stays as it is.

**Phone and performance:** the plaza dressing is 188 non-colliding parts already; lit lanterns on a phone means 2–4 lights plus Neon, not 14; one Sound for the drum; the Season window one ScreenGui, Scale and constraints, checked at phone size first; the festival board's text a Studio template; check the anime forest and the lit plaza together on a phone (the Roadmap's open play-check).

**Risks and Allen's calls**
1. "Village-wide events deferred" (2026-10-19): this un-defers them. Yes?
2. Premium cosmetics under "anyone can earn everything by playing"? The 2026-10-31 note already flagged it. (Q7)
3. Festival metals every year (the Book stays completable, GDD §10.3's "Material Index completion") or once? (Q8)
4. The calendar: live config (servers change without a publish) or shipped per update?
5. Season length: 4 weeks at 1 h a day is ~28 h for the engaged; the free track should finish by ~10 h of play so casual players (6 h) get most of it. Tuning in the sim.

**Build:** 8–10 sessions: festival state, calendar, banner, metal pool (1–2); board, orders, hand-in (1–2); stall cosmetics, gem and Robux purchase, save (1–2); the Season: missions, tiers, window, product, receipts (3–4); the Roblox event page, notifications, icons (1). Then about 1 session per festival (metal, 3 cosmetics, 6 orders' text).

**Play-check:** force a festival on (Dev Panel): the banner at join, the roller rolls the festival metal with the odds board unchanged; an order at the yagura, hand in, pay and gems; buy a cosmetic with gems and see it from the street and on a visitor's screen; test-buy the 99 R$ one; the Season window: a mission ticks on a forge, a tier claims, premium grants earlier tiers; festival off: the metal leaves the pool, owned swords keep it, the stall shows its date and closes; phone frame rate on the lit plaza; six plots in Clients and Servers.

**Sim:** the export gains `festival` (metal, orders, cosmetics, dates) and `season` (tiers, missions); `rules.Balance.roll` adds the festival metal to its tier's pool when the festival is on; `engine.Sim.on_day` (the 1 h play-day) toggles festivals by calendar day and refills festival orders; a `task_festival(order)` with a plaza walk (`layout` gets the yagura point); `gem_milestones` adds the stall's cosmetics as sinks; a `season` tally in `result()` from `push` kinds; `pacing.py`: orders filled, gems spent at the stall, season tier by play-day; `scenarios`: `festival-on`, `no-festival`. Check: gems an hour with the stall as a sink against the Gem Shop's 990; the free track done by ~10 h for engaged players; Crafter and Zanbatō times unmoved (the festival metal is an Epic like the others).

## 4. Trade Routes — the mid-game and away update

**The hook:** "My cart earns on the road while I'm at the anvil, and while I'm gone."

**What the player does**
1. The board shows the Dojo's standing order (Lv. 2: 6 swords), a gold rush slip ("Takeda: 2 polished Katanas, 1.5×, 10 min") and the bulk outlet.
2. Keep a spare sword back; pack; send. Riku pulls the cart out through the gate, down the street to the west gate and back.
3. It returns with 0.8× the swords plus the trip's extra: gems on most trips, a rare-ore crate now and then.
4. The client levels up: bigger orders, better pay, a thank-you letter at Lv. 3 and Lv. 5, a banner for your bay.
5. Leave with orders packed: the cart keeps running them while you're away, up to the cap; the welcome-back card shows the coins waiting.

**Content**
- **Three regular clients, Lv. 1–5 over hours** (the crew's cap rule): the Dojo (Eastern swords, many), the Town Guard (Takeda's: polished, Rare+), the Merchant (any, big counts). A level every 6 / 10 / 14 / 18 deliveries, so Lv. 5 at about 6–8 h for a player who carts twice an hour; pay 0.8× at Lv. 1 to 1.0× at Lv. 5 (+0.05 a level); thank-you letters through the mail at Lv. 3 (20 gems) and Lv. 5 (40 gems and the client's bay banner).
- **Rush orders:** one gold slip every 10–15 min (a random gap, like the mail's), from one of the 23 senders, 1–3 swords with a twist, **1.5×** (Claude's default; 2× is the alternative), standing 10 min on the board and then replaced, never two at once; no popup, a gold dot on the Deliveries button. An accepted one never expires (the guardrail "letters and orders don't expire").
- **Delivery-only rewards:** 2–6 gems on 7 trips in 10 (today only Special Orders pay gems), a rare-ore crate (an ingot of an Epic or Legendary metal you've found, the restricted-region ingot for free) on 1 in 6 orders of 9 swords or more. Not hilt or etch colours as [[Design/Delivery Ideas — 2026-11-05]] #1 floated: a hilt's colour shows its tier ([[Design/Monetization Ideas — 2026-10-31]] #12) and "no buyers-only etch" set the tone; the bay banner and the cart's lantern are the style rewards.
- **The bulk outlet** (#5 there): a standing bulk order at 0.8× that the Stocker fills with the cheapest rack swords when the shop is full; his "etched first, then any" rule (2026-11-05) stays for the shelves.
- **The cart on the street** (#3): since [[Sessions/2026-11-07#A bigger cart and board, a Delivery sign]] it leaves through the gate and turns into the street; extend the path to the west gate and back along the courier lane (`LANE` 35, `GATE_X` 422.5), so everyone sees every plot's deliveries go out. Trip time unchanged (2:30 → 1:10 by Speed): the drive is the trip.
- **Away earnings** ([[Design/Workshop Growth#Later capped offline earnings (confirmed 2026-10-22)]]: "once automation is established and online production is balanced"; the Sword Crafter and the Stocker are in, so this is that "later"): the cart keeps delivering the orders you packed, at the trip time, for up to **8 h** away (Q3). Only packed swords ship, so nothing is duplicated and the pay is the same 0.8× plus the trip's gems. Collected on return in a welcome-back card in the Daily window: cart back (+coins), letters waiting, today's gift (change #4 in [[Design/Kids and Reward Loops Research — 2026-10-31]]). An opt-in notification "Your cart is back: 3,200 coins waiting" (13+, one a day, "Live Ops Events and Updates").
- **Where it lands:** the Delivery Cart (6,200, "Delivery upgrade should always be available") comes at ~30–60 min; clients from the first trip; rush orders after the Sword Crafter (15–35 min), when a spare sword exists; away earnings after the Stocker (12,000; ~1 h engaged, 2:35 casual); Lv. 5 clients at 6–8 h, inside the trough. No new pads; Capacity and Speed stay as they are.

**Systems reused and new**
- Reused: `DeliveryService` and `Shared/Deliveries` (offers through `Orders.make`, status, capacity and speed, `trip`, `skipWait`, `senders`, encode/decode with SmithyCore's coders), `DeliveryController` (layout C), `Shared/Senders`, `Shared/Commissions` for the thank-you letters (a reward field for a cosmetic next to `rewardBlueprint`), the mail clock in `ShopService`, `EmployeeService` (the Stocker's loop), `NpcWalk` and the courier lane, `SmithyCore` (queued deliveries are saved already; add `clients` and `awayAt`), `Reputation` (a delivered sword's point stays), the Daily window in `GemController` for the card, the Delivery funnel in `Analytics`, `Store` (50% More Coins multiplies carts today).
- New: client data, levels and letters; the rush generator; the reward tables; the bay banner and cart lantern (Studio templates); the away settlement on load.

**Monetization within the rules:** no new product. The Don't list holds: no offline-earnings boost (#33), no finishing a trip for Robux (#24), no delivery XP boost (#21). 50% More Coins already covers "sales, carts, orders"; whether the away trips count is Allen's call (risk 4).

**Phone and performance:** the Deliveries strip's small tap targets are an open handoff (2026-10-31): fix them here; the gold slip and the client level are two more things in layout C, checked at phone size; six carts on the street plus 20 villagers: check the Busy street switch's frame rate; the card is the Daily window, which exists.

**Risks and Allen's calls**
1. Away earnings now, or later as the Decisions Log says? (Q2)
2. The cap: 8 h and packed orders only, or the crew's output too? Packed only is the one that can't pay twice.
3. Rush at 1.5× or 2×? At 2× a rush beats most regulars' offers (1.15–1.5×), so players would hold swords for the board; 1.5× keeps the shop first. (Q4)
4. Does 50% More Coins multiply away coins?
5. Three clients, or the senders' eight villagers as clients?

**Build:** 5–7 sessions: clients, levels, letters (1–2); rush, rewards, the bulk outlet (1–2); the street path (0.5); the away settlement, card and notification (1–2); the phone fixes, sim and checks (1).

**Play-check:** buy the cart; a Dojo order at Lv. 1; six deliveries → Lv. 2 and the pay line changes; a gold slip within 15 min, standing 10 min, replaced, never two; a trip pays gems and Collect shows them; a crate on a big order (Dev Panel to force); the Stocker fills the bulk crate when the shelves are full and still leaves etched swords for the Etcher; the cart drives to the west gate and back with six plots in Clients and Servers, no `NpcWalk … stuck`; pack two orders, leave, return after 10 min: the card shows the trips and the coins, nothing paid twice on a second rejoin; the notification prompt once; phone: the strip's tap targets.

**Sim:** the export's `deliveries` gains `clients` (levels, per-delivery thresholds, pay step, letters), `rush` (gap, pay, window), `rewards` (gems, crate odds), `away` (cap hours); `rules.make_delivery` draws regular, rush and bulk; `engine.Sim.task_cart` / `cart_fill` / `send_cart` / `task_cart_collect` pay rewards and count client levels; `on_day` settles the away queue between play-days and adds its coins at the next day's start; `behavior.Archetype` gets `rush` (efficient and manager chase gold slips, casual doesn't); `pacing.py`: carts an hour, share of income by cart, first Lv. 5 client, away coins a day; `scenarios`: `rush-2x`, `no-away`. Check: cart income stays under the shop's for ordinary swords, rush at most one order per 10–15 min, gems an hour against the Gem Shop's 990, and the Crafter, Longsword and Zanbatō times move under 5 min against a run with the same flags ([[Development/Sim Runs/notes-2026-11-05]]'s method).

## 5. Order to ship

1. **Trade Routes first, 2–4 weeks after launch.** The smallest of the three, Allen's own ask, and it touches every player from the first hour. Away earnings are the return hook that moves D1 and D7 ("something is ready", the accumulation family in "Retention and Return Hooks"). It also builds the one generalisation Legendary Commissions reuses: a letter whose reward is a cosmetic or a blueprint.
2. **Legendary Commissions second, 6–8 weeks.** Engaged players reach the trough in week 1, most players in weeks 3–6 at 1 h a day; the Blender blades take longest, so start them during Trade Routes. Once its content is decided, rerun the time model on the late prices ("the late game needs its content decided first; then rerun `python time_model.py 10`").
3. **Village Festival third, 10–12 weeks, on a real holiday.** It needs a player base to be seen (6 a server), the live calendar and the season's receipts. Make the first festival the one the launch date lands near: a new-year Firework festival if launch is December.

Between the majors, the small updates every 2–4 weeks: Decorate's return, the phone handoffs, play-check fixes. Watch each update's curve the way "Update Cadence and Hype Cycles" reads it: a spike that falls back to the old baseline in a week means the content was consumed, not a new goal.

## 6. Not chosen, and why

- **Workshop Makeover** (Decorate back, Name your shop 49 R$, Gold Workshop paints 199 R$): the cheapest to ship, with 6 decorations built and 14 candidates in `ServerStorage.DecorCandidates` ("lets keep this in backlog ill come back to it", [[Design/Tycoon Upgrades]]); style is the right thing to sell to kids. But it adds no goal to 4–20 h and no return trigger. **Rank 4:** release Decorate as the first small update, and let each festival's cosmetics use its spots; Name your shop fits there too.
- **An expansion area** ("a visible next tier", a mountain forge): the map is closed by the forest (2026-11-06) and "remove the mountains, we will work on it later" (2026-10-21); a new area means new nature (Toolbox or Blender only), a new workshop layout and a new material-tier gate, which needs its own decision. The biggest build, and the Seraph isn't reached in 22 h: there's no one to send up the mountain yet. **Rank 5;** revisit when the sim shows players finishing the chain.
- **Crew depth** (Pottery's 1–5★ employees, levels past 5): against the Lv. 5 cap reached over hours and "one system per effect"; the hires already carry 1–3★; crew XP ×2 adds 1–3% coins in the sim ([[Design/Monetization Ideas — 2026-10-31]] §2a). **Rank 6;** the Crew Wardrobe (149 R$) covers the "my crew" fantasy without power.
- **A second currency sink:** gems already have the Gem Shop (990 for all 20 levels), crew levels (20 / 55 / 105 / 200) and bought weather (60 gems, designed); the festival stall adds a sink inside Update 2; a token currency would be a third number on a phone HUD. Not an update of its own.

## 7. Questions for Allen

1. Ship order Trade Routes → Legendary Commissions → Festival? (yes, or your order)
2. Away earnings in Trade Routes now, or later? (now / later)
3. The away cap, in hours of cart trips? (a number; proposal 8)
4. Rush order pay: 1.5× or 2×?
5. Learned swords: worth less than your best pad sword, or free to beat it? (under / free)
6. VIP chains in the first release: 4 or 12?
7. Season premium cosmetics are fine under "anyone can earn everything by playing"? (yes / no)
8. Festival metals come back every year? (yes / once)

Sources: [[Current Status]] · [[Design/Game Design Document#7. Customers (NPCs)]] · [[Design/Game Design Document#9. In-person commissions and letters]] · [[Design/Decisions Log#Ten new swords - 2026-10-29]] · [[Sessions/2026-11-07#Secret swords by surprise letter (design, not built)]] · [[Sessions/2026-11-07#VIPs are the named characters; the first VIP only turns their head]] · [[Design/Pottery Playthrough 2026-11-02]] · [[Design/Pottery Playthrough 2026-10-27]] · [[Design/Shop Tension Pass]] · [[Development/Code Map]] · [[Development/Analytics Funnels]] · [[Development/Saving]] · [[Design/Six Plots]] · LihFolk Vault V2: "Retention and Return Hooks", "Genre Playbook - Tycoons", "Live Ops Events and Updates", "Battle Pass and Season Design", "Event Calendars and Content Planning", "Limited-Time Offers - Design and Ethics", "Update Cadence and Hype Cycles", "Economy Inflation Sinks and Faucets Math", "Global State and Live Config".

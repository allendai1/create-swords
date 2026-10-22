---
title: "Sell Swords! — Game Design Document"
status: "approved direction; partially implemented"
source: "[[Archive/Create Swords!|Create Swords!]]"
tags: [gdd, roblox, create-swords]
type: "design"
updated: "2026-10-22"
aliases: ["Create Swords! GDD", "Sell Swords! GDD"]
---

# Sell Swords! — Game Design Document

*Working title: **Sell Swords!** (alternatives were Create Swords! and Craft Swords!).*

> Refined from the original brainstorm in [[Archive/Create Swords!|Create Swords!]]. The brainstorm is left untouched; this note is the working design.
> Direction approved 2026-10-19, with later dated decisions incorporated through 2026-10-22. The latest dated decision takes precedence over older rules. This document describes the intended game, not a claim that the changes are implemented. Earlier prototype details remain in [[Development/Code Map|Code Map]], session notes, and [[Archive/Design/GDD before 2026-10-19 revision|GDD before 2026-10-19 revision]]. New onboarding proposals are separate in [[Design/Core Loop Review|Core Loop Review]].

---

## 1. One-line pitch

**Build your smithy in a Japanese mountain village, forge swords by hand, and earn a reputation among sword wielders from across the world.**

A cozy crafting tycoon inspired by the atmosphere and craftsmanship of Demon Slayer's Swordsmith Village. Daily village life is peaceful, punctuated by spectacular individual visitors. Original locals share the world with recognizable fictional and historical sword users, including knights and other non-Japanese traditions. Their coexistence needs no crossover explanation. Village-wide events are deferred.

## 2. Pillars

**Progression direction confirmed 2026-10-22:** relaxed swordmaking serves the larger fantasy of becoming rich. Make more valuable swords by hand, invest profits in familiar production, then personally pursue the next designs and special commissions. Most upgrades and blueprints are money-led; milestone commissions introduce special designs and sword traditions. After personally crafting a sword shape, pay coins to train employees to produce it in any permitted material supplied to them; no separate training per material combination. Fully trained smiths can match the player's 100% forging quality. Initially the player supplies rolled ore; a later ore attendant runs the existing roller using the same material odds. Training costs and ownership remain open; see [[Design/Workshop Growth#Wealth and staged automation (confirmed 2026-10-22)]].

1. **Making a sword feels satisfying.** Every hammer hit visibly shapes the blade, with sparks, sound, and movement.
2. **Simple actions, optional extra care.** Hitting every forging circle gives 100% quality; optional final polishing on the assembled sword adds +10% value (Allen 2026-10-20). Quality remains a visible percentage and affects price. Employee output has separate capability limits (see §10.4).
3. **Every customer is a little story.** Flexible everyday tastes, personal relationships, and specific special commissions give swords a purpose.
4. **A workshop worth growing.** Sales fund functional upgrades; crafting milestones unlock fittings; commissions introduce sword traditions.
5. **A cozy home for extraordinary visitors.** Japanese village identity, varied customers, no combat or testing-area scope for now.

## 3. Target & platform

- **Platform:** Roblox (PC, mobile, console). All interactions must work with touch: the anvil minigame is tap/click based.
- **Audience:** 9–16, fans of *Create Pottery!*, cozy tycoons and simulator games.
- **Session:** 10–30 minutes, with clear crafting and progression goals. No quench/temper step.

## 4. Core loop

```text
Roll ingot → Heat → Hit every forging circle (100%) → Fit hilt → (Polish, +10% value) → (Etch, unlocked station)
    ↑                                                                     ↓
Upgrades ← Coins + reputation ← Display and haggle / fulfill an accepted order

Direct commissions, optional courier deliveries, and relationships provide goals alongside ordinary shop sales.
```

| Step | Action | Current direction |
|---|---|---|
| Roll | Ore loot box (Ore Roller) | Since 2026-10-22, a loot box in the workshop's back-left corner, from Allen's Call of Duty loot box idea ([[Art/Ore Loot Box]]). Before it there were placeholders: the supply chest (2026-10-21) and the alcove; the 2026-10-20 mine and carts are parked ([[Archive/Art/Blender Station Review]]). Pull the shared lever: the lid opens, one ingot per bought slot (up to 6) floats up, spins through the ore types and locks in on its result, and all drop onto the lid, in 3.6 s. **Collect before rolling again** (Allen 2026-10-22): the lever is off while rolled ore waits on the lid. This replaces the unlimited re-rolls of 2026-10-20. Keep the full fantasy material roster. |
| Heat | Forge | Load an ingot and collect it after heating. One furnace heats **one ingot at a time** (Allen 2026-10-20; the forge model shows one tray), and its label shows only the time left, then "Ready!"; heating more at once means buying another furnace in the tycoon. Base heating time is **10 seconds** (approved 2026-10-19, built 2026-10-22), replacing the 15-second prototype duration. **Until the player's first sword is finished an ingot heats in 3 seconds** (Allen 2026-10-22: "first time tutorial, the furnace and other processes need to be sped up"). No quench or cooling countdown while shaping. |
| Forge | Anvil | Choose a hot ingot and unlocked blueprint. Hit every circle, without timing windows or misses. Each hit improves the blade; completing all circles gives **100% quality** (Allen 2026-10-20; was 90%). The anvil view closes when the blade is done. |
| Assemble | Hilt Bench | Choose fittings appropriate to the sword's tradition and attach them with three untimed knocks: click the ring on the hilt's end (or Space) and each knock slides the hilt further onto the tang on the bench (2026-10-20). No timing bonus or penalty. |
| Polish, optionally | Polishing Station | On the finished sword: freehand polishing along the edge removes the last excess metal and brightens the finish. A fully polished sword is worth **+10%** and is named "(Polished)"; quality is already 100% from forging (Allen 2026-10-20). The anvil only forges. |
| Etch, optionally (last step) | Etching Table | Apply a finish pattern. The last step, after polishing, because the Etching Table will be an unlocked station (Allen 2026-10-20). Current approved interim flow is free and instant; a trace minigame is deferred. |
| Display | Sword holders | Put the complete sword on display. Stock influences regular visitors. Players start with one 3-sword wall rack in the Starter Shop, then buy a second wall rack, a display table, the Upgraded Store and more racks and tables from tycoon floor pads ([[Design/Tycoon Upgrades]], 2026-10-20). |
| Sell | Customer | Accept or haggle; pushing for more can cause the customer to leave. Sales earn coins and build reputation and familiarity. |
| Deliver, optionally | Delivery board and courier/cart | Fulfill a separate remote order, pack swords, dispatch, and collect the reward when the courier returns. Direct commissions retain their immediate picker hand-in. |
| Grow | Workshop and commissions | Upgrade the workshop, unlock fittings through crafting, and learn new sword traditions through commissions. |

**Picker behavior (confirmed 2026-10-19):** every item-selection interaction opens its picker every time, even with only one valid item. Do not auto-select the current workpiece or bypass a picker. Commission delivery is a parallel route to ordinary display sales: open the commission, select the finished sword through a picker, and receive the agreed reward. No display listing or haggling is required for commission delivery.

## 5. Forging and optional grinding

**Current station split:** the anvil forges; the Polishing Station performs the former freehand grinding as an optional step after hilt assembly; etching comes after it, last (2026-10-20). The section title is retained for existing links. Player forging completes at 100% quality; optional polish is a separate +10% finish bonus (2026-10-20). Older employee quality/recovery rules in §10.4 need reconciliation with this change.

**Approved 2026-10-19; replaces the timed Points and freehand hammering prototypes as the intended main mode.**

- **Forging camera (approved 2026-10-19):** slightly angled overhead, showing the blade outline clearly while retaining visible thickness, hammer movement, and the anvil. Keep the entire blade visible throughout lengthening and repositioning. Exact framing and camera movement remain to be tuned.
- **Universal starting blank (approved 2026-10-19):** every sword blueprint starts from the same blank shape and size. Forging stretches it to the selected blade’s length and establishes its distinct profile; do not use blueprint-sized starting blanks. The rolled material still determines its material appearance.
- Guided circles identify hammer strikes. **The blade moves by itself, without visible tongs:** it slides, turns, and flips beneath the fixed hammer point between strikes. Players do not manually reposition it.
- Players hit every circle. No overall timer, timing window, misses, cooling countdown, or reheat loop during shaping. Earlier retry/minimum-hit discussions are superseded by this simpler rule.
- **Staged shaping (approved 2026-10-19):** early hits lengthen the thick blank; middle hits establish the blade’s taper and curve where appropriate; final hits form the point and refine the rough outline. Each hammer impact visibly changes the section beneath it. The blade progresses from a thick blank to a long rough blade to a recognizable sword. Exact hit counts, intermediate shapes, and animation pacing remain to be designed.
- **Impact deformation (approved 2026-10-19):** quickly and smoothly deform the struck area at hammer contact, blending the change into neighboring metal. Flatten or stretch the local section as appropriate to the shaping stage. Avoid discrete shape snaps, wobbling, or a slow melting effect. Exact deformation timing and falloff remain to be tuned.
- Each completed circle shapes its section and increases quality. All circles completed gives **100% player quality** (revised 2026-10-20). **Initial implementation uses the same circle/hit count across sword blueprints. Higher-tier swords should eventually require modestly more effort**, rather than making all larger swords automatically take longer. Exact tier thresholds, added effort, circle count, and transition pacing remain to be tuned; the previous 12 is only a prototype baseline. No timing challenge or failure penalty is introduced by this direction.
- **Forged blade appearance (original art direction, 2026-10-19):** clean and recognizable, with the intended silhouette, subtle excess metal along the edge, and a dull finish. It should already look like a desirable finished sword after fitting the hilt, not a visibly jagged or misshapen failure. Optional polishing refines the small edge allowance and improves the finish; it adds a finish bonus rather than completing missing player forging quality.
- Forging ends at **100%** (changed 2026-10-20 from 90%) and the blade is finished right away; it goes to the Hilt Bench. (Changed 2026-10-20: grinding moved from the anvil to the Polishing Station, an optional step on the finished sword.)
- Polishing (at the Polishing Station, on the assembled sword) is freehand but constrained to remove only excess metal toward the target. It cannot overcut or reduce quality. A full polish adds **+10% value** (finish bonus, like the hilt and etch bonuses). The polishing action is free after unlocking the station; the recorded station purchase is 250 coins ([[Design/Tycoon Upgrades]]). Selling unpolished stays a choice.
- Quality is shown as a percentage, not a grade name. It is now a guided completion/refinement measure; the old silhouette mismatch formula is not the new scoring specification.
- Accent lines and bevels remain automatic visual details on finished swords, suited to the blueprint.
- Server validation must enforce valid circle progress and bounded grinding improvements. The recorded BladeCore/ForgeCheck integration covers this flow; see [[Development/Code Map]] and [[Current Status]] for implementation and remaining validation.

**Balance still to test:** whether polishing feels satisfying and genuinely optional for its +10% value bonus, how its progress reads, and how many forging circles keep repeated crafting enjoyable.

## 6. Materials, blueprints & finishes

### 6.1 Materials (rolled at the Ore Roller)

**Roller behavior (revised 2026-10-22):** one shared lever rolls every bought slot (up to six) in a 3.6-second loot-box show. Each slot holds one result on the lid. **Collect all waiting results before rolling again**; collection does not start another roll. Buying another ore slot increases results per pull without changing per-result rarity odds. This supersedes the older rule that skipped occupied stands while rolling empty ones. See [[Art/Ore Loot Box]].

| Rarity | Examples | Base multiplier | Roll odds (starting) |
|---|---|---|---|
| Common | Iron, Copper, Stone | ×1 | 60% |
| Uncommon | Steel, Bronze | ×1.5 | 25% |
| Rare | Blue Steel, Silver | ×2.5 | 10% |
| Epic | Gold, Obsidian, Damascus | ×5 | 4% |
| Legendary | Mythril, Starmetal, Rainbow Alloy 🌈 | ×12 | 1% |

- Each material has a distinct texture (Damascus swirls, rainbow shimmer), mirroring *Create Pottery!*'s "Cocoa Swirl / Porcelain" clays.
- "NEW" badge and a small celebration the first time a material is rolled; a **Material Index** (collection book) tracks discoveries.
- Fantasy materials remain available from the start through the roller odds; they are not gated behind a grounded-materials phase.

### 6.2 Blueprints (sword shapes)

**Blade art direction (approved 2026-10-19):** grounded starter tantō, wakizashi, and katana, with slightly exaggerated proportions for clear readability. Give each its own silhouette rather than simply scaling one katana. Later special blueprints can introduce extravagant fantasy shapes and details. Exact profiles and forging transformation choreography remain under design.

**Japanese starting progression: tantō → wakizashi → katana.** Players start with the **tantō blueprint** and simple on-screen instructions for their first sword. Later local teaching commissions introduce **wakizashi, then katana**, providing each blueprint when its commission begins.

Later visitors introduce other sword traditions through a first commission that supplies its required pattern. Additional blueprints within that tradition can be purchased with coins. Longswords, cutlasses, rapiers, claymores, and flamberges remain expansion candidates; their order and prices are not yet tuned.

Tantō and wakizashi replace the dagger/shortsword starting progression. The old blueprint price/difficulty table is historical, not the approved new progression. Katana's existing smooth curved profile remains a visual reference.

### 6.3 Finishes (optional value-adds)

| Finish | Station | Minigame | Bonus |
|---|---|---|---|
| **Polish** | Polishing Station (built 2026-10-20) | Freehand edge polishing (the old anvil grinding), on the finished sword | +10% value when fully polished (2026-10-20) |
| **Color / Enamel** | Etching Table | Paint coverage, pick colours (rainbow = multi-colour) | +10–20%, matches NPC wants |
| **Etching / Rune** | Etching Table | Free and instant in the approved interim flow; since 2026-10-21 the player watches it drawn on their sword (Flame, Eclipse; Tide, Stormroot, Woven Wind, Fracture and Falling Stars since 2026-10-22); trace minigame deferred | +15% |
| **Hilt** | Hilt Bench | Choose matching fittings; three untimed knocks seat the hilt on the tang. Completes the sword (see §6.5) | +0% to +40% price by hilt; some NPCs care |
| **Gem Socket** (late) | Hilt Bench | Insert a gem | Large bonus; consumes a gem item |

### 6.4 Sword value formula

```
Value = Blueprint base
      × Material multiplier
      × Quality multiplier (×1.0 at 80% → ×2.0 at 100%)
      × (1 + hilt bonus + other finish bonuses)
      × NPC preference bonus (see §7)
```

The tooltip on a finished sword shows each factor so players learn what to chase. Since 2026-10-20 every player-forged blade is 100% (×2.0) and a full polish is a +10% finish bonus. Review that incentive in [[Design/Core Loop Review|Core Loop Review]]. Employee quality below 90% needs explicit value/refinement rules before implementation, particularly if starting quality is below the table's 80% baseline; do not invent extrapolation. Optional finishes remain optional; other proposed bonuses still need tuning.

### 6.5 Hilt Bench and fittings

- Choose a blade and fittings, then attach with **three untimed taps**. No timing challenge or quality penalty.
- Fittings **match the sword tradition**: Japanese blades use appropriate wrapped grips and tsuba; western swords use their own guards and pommels. No cross-tradition mixing.
- Fittings unlock through **swords-crafted milestones**, without a later coin-purchase requirement.
- Exact fitting sets, milestone counts, and price bonuses need tuning. The old universal Wooden Grip → Gem Pommel ladder is superseded.
- **Built 2026-10-22:** every blueprint and hilt has a tradition, and the bench (and the server) only fit hilts of the blade's tradition. All six current hilts are Japanese koshirae; their names still come from the old ladder and the milestones are unchanged (0/2/4/7/10/15 swords).
- Completed swords can be held, collected, displayed, or sold. Combat and a testing area are outside current scope.

## 7. Customers (NPCs)

**First-sale tutorial (approved 2026-10-19):** no customers visit the player’s shop while they make their first sword. Putting that sword on sale triggers the tutorial customer’s arrival. This replaces the proposed waiting customer/commission before the first craft. Players start with the tantō blueprint and simple on-screen guidance; local commissions introduce wakizashi and katana afterward. This rule applies to the beginning tutorial, not yet to all later crafting. **Built in part (2026-10-22):** customers only come while a sword is on display, and until the first sale a listing brings one at once (later walk-ins come every 12–22 s). The fair first offer is built too (§8). **The on-screen guidance is built (2026-10-22):** one short line at the top names the next action and an arrow marks the station, from rolling through the first sale, the teaching commissions and Ore Slot 2 ([[Development/Code Map#First session and saving (2026-10-22)]]).

- Early customers are primarily original local villagers, guards, and wandering swordsmen, with an **early special outsider** hinting at the wider cast.
- Later customers can include knights, pirates, and any fictional or historical sword wielders. The cast combines original regulars and recognizable special visitors; exact named roster is not selected.
- **Displayed stock influences regular customer arrivals. Reputation unlocks surprise special visitors.**
- **Weather traffic (confirmed 2026-10-19):** sunshine can grant extra customer traffic; other weather stays at the normal baseline. Bad weather does not reduce arrivals below baseline. Weather bonuses must respect the first-sale tutorial arrival gate. Bonus values, schedules, and combination with reputation/customer upgrades remain untuned; see [[Design/Workshop Growth]].
- Regular customers have flexible tastes (such as elegance, color, or craftsmanship); special commissions specify concrete combinations.
- Repeat sales build familiarity. Relationship milestones unlock personal commission chains, stories, and rewards.
- Individual special visitors bring distinctive commissions and rewards. No village-wide event system for now.
- Existing preference bonuses are economy baselines; broad taste matching needs a defined rule before implementation.

## 8. Selling & haggling

**Tutorial exception (approved 2026-10-19):** the first customer gives a guaranteed fair offer, providing a clear reward for the first sword. Haggling is introduced on the **second ordinary shop sale**, not the first. Commission deliveries pay their agreed reward and do not count as shop sales for this tutorial step. The exact fair-price calculation remains to be tuned. Regular negotiation rules below apply after the introductory sale. **Built 2026-10-22:** the fair offer is the sword's full value and a decline gets no counter-offer; on the second sale the offer card says "Decline and they may offer more" and the first decline always brings a better offer.

1. NPC inspects and offers a price (roughly 80–110% of value, nudged by personality).
2. Player chooses **Accept** or **Decline**.
3. On decline, NPC either:
   - raises the offer (chance based on personality; Pirate rarely, Noble often), or
   - leaves unhappy. Each NPC has a hidden **patience** of 1–3 declines.
4. Accepting fills a small **reputation** meter; reputation raises customer frequency and unlocks special customers.

**Recorded build:** per-plot displays and customer routes, up to two customers at once, and a 20-second offer card. Before the first sale a listing brings a customer immediately; later arrivals use 12–22 s intervals. The first two ordinary sales use the tutorial exceptions above. Older NPC opener/preference tables are historical tuning; confirm the live `Shared.Customers` catalogue before balancing. Reputation/familiarity remain unimplemented.

**Cashier upgrade:** an NPC cashier auto-accepts offers above a threshold the player sets (e.g. "accept ≥ 100% of value").

## 9. In-person commissions and letters

- Customers introduce requests **in person**; returning customers can also send **letters**. This replaces the smartphone/text-message framing.
- Special visitors leave **untimed commissions** and return when the sword is ready. Their requests do not expire or lose a speed bonus while the player prepares.
- The tantō blueprint is available from the start with on-screen tutorial guidance. **After the first sale, the next goal is a local wakizashi teaching commission**, which provides its blueprint when the commission begins. A later local teaching commission introduces katana. No workshop purchase or additional tantō sale is required before introducing the wakizashi commission. **The first commission requests an Iron Wakizashi with at least 90% quality.** Completing all forging circles satisfies the quality requirement; grinding remains optional. Iron is available in the starter Ore Roller’s Common pool; no guaranteed roll or odds change has been approved.
- Outside visitors introduce new traditions through a first commission; additional patterns in that tradition become coin purchases.
- Relationships grow through ordinary sales and unlock personal commission chains.
- Coins and gems remain proposed rewards; commissions remain a gem source.
- **Commission delivery:** open the commission and select the finished sword through a picker, then receive the agreed reward. This also applies to the first Iron Wakizashi commission; it does not require putting the sword on sale or negotiating.
- **Built 2026-10-22 (Claude's defaults, [[Design/Decisions Log]]):** the Guard Captain walks in after the first sale and asks for the Iron Wakizashi (90%+, 120 coins); talking to him or using the shop's request board accepts and teaches the wakizashi, and the sword is handed in at the board through a picker. The Wandering Swordsman asks for a Katana of any metal (90%+, 300 coins) after the wakizashi and the third shop sale. Requests don't expire. Hand-ins don't count as shop sales.
- Exact letter interface, active-request capacity, and ordinary commission timing are not settled. [[Design/Core Loop Review|Core Loop Review]] separates this confirmed sequence from proposed timing targets and playtest questions.

### 9.1 Remote delivery orders

**Confirmed 2026-10-19:** add a separate optional delivery board/station using a village courier or cart. Accept an order showing recipient and requested swords → craft and pack the crate → dispatch → delivery and return trip → collect the payout at the station. An order can be pinned on screen. Upgrade directions include delivery speed and carrying capacity.

This is a parallel order route. In-person/letter commissions retain the direct picker hand-in above, including the first Iron Wakizashi commission. Delivery travel does not require the player to stop crafting. Exact order rules, capacity, rewards, trip time, unlock stage, expiry/cancellation and offline behavior remain open.

**Delivery bay (2026-10-22):** every plot has a fenced yard in the lane beside its shop, with a gateway onto the street, kept for the courier's cart (Allen: "each plot should have an area where we can eventually add a delivery carrier. maybe a guy with a carriage. potentially could carry over into the street."). Nothing works there yet. When delivery is unlocked, a door opens in the shop's wall onto the bay (built 2026-10-22, hidden until then).

The pottery reference's van, 3:30 round trip, 3000-gold upgrade, and 6→9 capacity are comparison notes, not selected assets or balance numbers. Full context: [[Design/Workshop Growth#Optional remote delivery orders]].

## 10. Economy & progression

**Permanent growth (confirmed 2026-10-22):** the player retains wealth and workshop progress while expanding into higher-value swords, facilities and prestigious customers. No rebirth/prestige reset is selected for the current plan. Detailed late-game milestones and expansion limits remain open.

**Tutorial progression (approved 2026-10-19):** first tantō shop sale → Iron Wakizashi commission (90% minimum, delivered through a picker) → first workshop upgrade, **Ore Slot 2**. The purchase already exists; since 2026-10-22 the guide points to it once the Iron Wakizashi is handed in (the first sale plus the 120-coin reward is about 160). The currently recorded price is 75 coins and needs affordability testing. Each bought slot adds one result per pull; the 3.6-second loot-box show and collect-before-reroll rule supersede the old empty-stand behavior. More slots increase output, not per-result rarity odds.

### 10.1 Currencies

| Currency | Earned from | Spent on |
|---|---|---|
| **Coins** | Selling swords | Blueprints, stations, shop expansions, decor |
| **Gems** | Commissions, special customer tips, Material Index milestones, **Robux purchase** | Customer/client upgrades, Lucky Rolls, timer skips |

### 10.2 Upgrades

**Coin upgrades (smithy & shop):**
- Additional **material stands for the Ore Roller** (the second slot is the first tutorial upgrade; one shared lever rolls all bought slots after previous results are collected, separate from luck upgrades)
- Extra **display racks** and **ingot shelf** space
- Additional **anvils, bare-blade rack capacity and finished-sword rack capacity** for employee production; prices and station-assignment rules need design
- Faster **heating** timers
- Better **roll odds** (Lucky Roller I–V)
- New **blueprints** and **finish stations**
- **Shop expansions**: start with one three-sword wall rack in the Starter Shop; buy further racks, tables and the Upgraded Store. The shop grows from about 28 to 40 studs deep and the workshop moves back 12 studs. See [[Design/Tycoon Upgrades]]. Purely cosmetic decoration gives no stats.

**Gem upgrades (customers):**
- **More Customers**: shorter time between walk-ins
- **More Special Customers**: higher chance of special NPCs
- **More Clients**: more simultaneous commissions
- **Regular Clients**: returning clients send letters sooner

**Automation (late game):**
- **Cashier**: auto-accept offers (see §8)
- **Five initial employee professions**: furnace operator, smith, finisher, stocker and cashier, with hiring/upgrade UI and levels; an ore attendant is a later upgrade. The finisher combines hilt assembly and optional polishing; the stocker transfers ready swords from the finished rack to empty holders. **Racks built 2026-10-20:** an Ingot Rack (12 ingots) and a Finished Sword Rack (6 swords) in the workshop; players carry items and store or take them with E, ready for employees later. Smiths leave bare blades on their own rack and improve from lower starter output toward **100% forging quality** when fully trained. See §10.4. The old fixed 85% apprentice, 90% ceiling and separate hilter/polisher proposals are superseded; starting values and progression remain untuned.

**Delivery progression (unlock stage and currency open):** improve courier/cart trip speed and carrying capacity; prices and values remain undecided.

### 10.3 Progression arc

**Visual progression direction (2026-10-19):** early game starts sparse with basic stations; mid game adds displayed swords and stations; late game expands the shop with station workers and advanced upgrades. See [[Archive/Art/Japanese Village Concept Art|Japanese Village Concept Art]] for the same-plot comparison. Illustrated capacities and precise unlocks are proposals, not fixed balance rules.

| Stage | Player has | Goal |
|---|---|---|
| Early (pacing to test) | Roller, forge, anvil, hilt bench, optional Polishing Station, display; local teaching commissions | First tantō sale, fittings milestone, progress toward wakizashi and katana |
| Mid (pacing to test) | New traditions, letters, better workshop facilities | Customer relationships, additional blueprints and capacity |
| Late (pacing to test) | Cashier, Apprentice, Claymore/Flamberge | Legendary metals, 98%+ blades, Material Index completion |

### 10.4 Employees and production handoffs

**Latest decision, 2026-10-22:** the first employee is a **sword crafter**, operating the anvil, polishing and placing the sword in the sword rack. This supersedes separating forging and polishing between smith and finisher for that first hire. Hilt assembly responsibility and input supply still need clarification; polishing remains on an assembled sword. Reconcile the older five-role breakdown below and its bare-blade handoff before implementation; it is not the final roster under this revision. The later ore attendant, paid shape training and 100% trained forging ceiling remain selected. See [[Design/Workshop Growth#First employee — sword crafter (latest decision, 2026-10-22)]].

**Confirmed from Allen's notes and answers, 2026-10-19:** five professions, with multiple workers per profession possible subject to station/capacity limits. Hire and compare workers through an employee management/upgrade window; employees level through completed work. Buy additional anvils and provide separate bare-blade and finished-sword racks.

- **Furnace operator:** loads, heats and collects ingots for the next stage.
- **Smith:** uses an available anvil to forge trained sword shapes in permitted supplied materials and deposits the un-hilted blade on the blade rack. Starter quality is lower; fully trained smiths can reach **100% forging quality**, matching manual forging (revised 2026-10-22; replaces the 90% ceiling). Starting quality and progression costs/curve remain open.
- **Finisher:** combines fitting the selected hilt with optional polishing. Speed and polishing ceiling improve through training. Players can choose fittings and whether to polish. For player etching, pause after assembly and resume final polishing after etching. No separate hilter or polisher profession.
- **Stocker:** visibly carries ready-for-sale swords from the finished-sword rack to empty shop holders. It preserves swords reserved for commissions, deliveries or further finishing, and waits when the shop is full or no eligible swords are ready. Stocking speed is the initial progression direction; display-priority modes remain later options.
- **Cashier:** retains the offer threshold described in §8.

**Player completion is allowed:** the player can improve an employee's unfinished bare blade at the anvil toward 100% forging quality and improve its assembled finish separately. Fully trained smiths can also reach 100%; starter quality, remaining-work representation, recovery/data/value rules and finisher polishing ceilings need design before implementing employees. The older employee 90% ceiling and polishing-to-100%-quality model are superseded. Polishing remains a separate finish bonus and must not substitute for unfinished forging.

The production route is furnace operator → smith → bare-blade rack → finisher (hilt, optional polish after any player etch) → ready-for-sale finished-sword rack → stocker → shop holders → cashier. Reserved commission/delivery swords bypass retail stocking. Players can also place their own ready swords on the finished rack for retail automation.

Exact starting quality, polishing ceilings, progression curves, prices, unlock timing, material permissions, intermediate storage, queues and station priority remain open. The current 90–100% implementation needs an explicit extension for sub-90% employee work. **Later revision, 2026-10-22:** retain these five initial professions and add an ore attendant as a later upgrade, operating the existing roller with unchanged material odds. Initial employees consume player-supplied ore; familiar shapes require a personal first craft and paid training. Hiring, training and upgrades are one-time purchases, with **no ongoing wages**. Add **capped offline workshop earnings as a later feature** after online automation is balanced, collected on return; cap, rate, unlock and stock/ore-attendant rules remain open. No automated etcher or employee courier is selected; courier offline rules are separate. See [[Design/Workshop Growth#Employees and workstations]].

## 11. World & multiplayer

**Current layout (2026-10-22):** each player has a street-facing shop with a connected back-room workshop on the simplified six-lot map. The recorded lot footprint is 48.5 × 96 studs; upgrading deepens retail space and moves the workshop back. The earlier L-shaped property concepts in [[Archive/Art/Japanese Village Concept Art]] are historical visual studies, not the current construction plan.

- **6 players per server**, each with a workshop plot in a Japanese swordsmith village. Since 2026-10-21 a joining player gets the first free lot (N2, N1, N3, S2, S1, S3) with a fresh copy of the plot; others can visit but not use it; it is cleared when they leave, and since 2026-10-22 their purchases, displays and racks come back on whichever lot they get next time ([[Development/Saving]]). See [[Design/Six Plots]].
- **The map (2026-10-22):** a small walled Japanese town.
  - **Street:** one broad flagstone street (fronts 72 apart) runs from a timber gate to a small shrine.
  - **Plots:** three per side, each separated from the next by a 48-wide paved lane (a full shop width). The middle pair stands a little back, as a junction. Two lanes run on through the back wall.
  - **Other buildings:** a few small houses at the edges, with no clutter.
  - **Unclaimed lots:** all six plots are always on the map; a lot without a player shows its plot, empty and unusable.
  - **History:** this replaced the continuous town street of 2026-10-21 ([[Archive/Art/Japanese Street]]) after Allen compared it, a broader redesign and this simplified map. See [[Art/Town Street Redesign References]].
- **Shop + back-room workshop (2026-10-21):** one machiya on each separated player lot. The shop room is on the street (the Starter Shop, then the two-storey kura Upgraded Store), and a centre door leads to the workshop behind. Buying the Upgraded Store pushes the workshop 12 studs further back, so the shop room grows from 28 to 40 deep. Crafting runs clockwise round the workshop: ore intake, furnace, anvil, hilt bench, optional polish, optional etch, then the finished rack by the door. Layout: `References/Concept Art/shop design`. This replaces the earlier open-front workshop with visible forging. Since 2026-10-22 the workshop is one working room ([[Art/Workshop Layout]]): supply chest back-left, furnaces on a shared hearth, the anvil centred in front of them, and a finishing bench along the right wall (hilt → polish → etch toward the door).
- Progression expands the plot with more elaborate roofing, timber, signage and displays: the shop upgrades in place on the street, and the workshop fills with stations. Freeform building placement is not the selected direction.
- **Indoor roof visibility (built):** `RoofHider` locally fades unlocked plot roofs while the player is inside and restores them outside. Current layout, eave/detection transitions and station cameras still need Play checks. See the exterior/interior pottery reference pair in [[Design/Workshop Growth#Roof visibility while indoors]].
- Warm, cozy, stylized art: timber, tiled roofs, lanterns, stone paths, streams, and mountain scenery. Demon Slayer's Swordsmith Village is an atmosphere reference.
- NPCs travel through the village and visit shops. Admiring other players' shops remains the light social layer; no player trading in v1.
- Cosmetic decoration is freely expressive; functional displays and facilities provide business benefits.
- The previously built medieval cabin (`Models/Archive/SwordShop.fbx`) is a historical asset, not the target shop design. Earlier workshop builds remain documented in [[Archive/Art/Smithy Redesign|Smithy Redesign]]; [[Art/Workshop Layout]] describes the current interior.

## 12. Technical notes (Roblox)

Implementation details and script paths are maintained in [[Development/Code Map]]; the current state and design/build differences are summarized in [[Current Status]]. The BladeCore port and Japanese workshop rebuild are documented as implemented, while other parts of this design remain future work.

- Studio scripts/models are saved in the place; reusable browser and Luau blade sources also live in `Prototypes/tanto-forge/`.
- Server-owned state and `ForgeCheck` validate forging completion and refinement. The client renders responsive blade motion from BladeCore/BladeData through BladeView.
- Finished swords use the implemented baked-first shared mesh pipeline with live fallback; active forging/polishing retains deforming geometry. Many-sword, EditableImage and published-device tests remain pending. See [[Development/Sword Mesh Pipeline]].
- **Saving is built (2026-10-22):** session-locked DataStore saves of coins, items with their finishes, racks, displays, learned blueprints, upgrades, discovered metals, commissions and counters, with recovery rules for furnaces, the ore box and unfinished work. See [[Development/Saving]]. Rejoin and multi-server behaviour still needs Play checks.
- Six-player plot assignment and per-plot stations are built. Multiplayer ownership, south-lot orientation, release/reclaim and device behavior still need testing.

## 13. Decisions log

The full dated record is [[Design/Decisions Log|Decisions Log]]. The approved 2026-10-19 decisions supersede conflicting prototype rules, including the medieval cabin, timed forging, minimum-hit failure, damaging grinding, timed hilt taps, smartphone commissions, and universal fitting ladder.

See [[Sessions/2026-10-19]] for this revision's scope and [[Design/Core Loop Review|Core Loop Review]] for recommendations still awaiting discussion.

## 14. Build plan

See [[Development/Roadmap|Roadmap]] for implementation status. Prior completed prototypes remain historical achievements, not evidence that the revised design is built.

Anvil forging, final polishing on its own station, and the Japanese workshop have implementation records. Remaining work includes first-session progression, saving, later upgrades, relationships, employees, courier orders, weather traffic bonuses and current-build validation. Plot assignment, upgrade purchases and indoor roof fading already have implementation records. [[Development/Roadmap]] owns the actionable task list; this document owns intended game behavior.

[[Design/Core Loop Review]] distinguishes confirmed tutorial choices from unapproved pacing and interaction recommendations.

## 15. Monetization (Robux)

Guiding rule: Robux speeds things up or adds style, but anyone can earn everything by playing.

| Product | Type | What it gives |
|---|---|---|
| Gem packs | Developer product | Gems (same currency earned from commissions) |
| 2× Coins | Game pass | Double coins from sales |
| Auto Cashier | Game pass | Cashier from the start (still unlockable with coins later) |
| VIP Rack | Game pass | Extra golden display rack, NPCs pay +10% there |
| Lucky Roll | Developer product | One roll with boosted rare odds |
| Heating skip (earlier proposal, review pending) | Developer product | Potential skip for the forge heating wait; no quench step exists |

Prices are set during Phase 3 tuning.

---

Related: [[Home]] · [[Development/Roadmap|Roadmap]] · [[Design/Decisions Log|Decisions Log]] · [[Archive/Create Swords!|Create Swords!]] · References: ![[Screenshot 2026-10-16 230815.png]]

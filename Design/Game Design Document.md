---
title: "Sell Swords! — Game Design Document"
status: "approved direction; partially implemented"
source: "[[Archive/Create Swords!|Create Swords!]]"
tags: [gdd, roblox, create-swords]
type: "design"
updated: "2026-10-19"
aliases: ["Create Swords! GDD", "Sell Swords! GDD"]
---

# Sell Swords! — Game Design Document

*Working title: **Sell Swords!** (alternatives were Create Swords! and Craft Swords!).*

> Refined from the original brainstorm in [[Archive/Create Swords!|Create Swords!]]. The brainstorm is left untouched; this note is the working design.
> Current design direction approved 2026-10-19. This document describes the intended game, not a claim that the changes are implemented. Earlier prototype details remain in [[Development/Code Map|Code Map]], session notes, and [[Archive/Design/GDD before 2026-10-19 revision|GDD before 2026-10-19 revision]]. New onboarding proposals are separate in [[Design/Core Loop Review|Core Loop Review]].

---

## 1. One-line pitch

**Build your smithy in a Japanese mountain village, forge swords by hand, and earn a reputation among sword wielders from across the world.**

A cozy crafting tycoon inspired by the atmosphere and craftsmanship of Demon Slayer's Swordsmith Village. Daily village life is peaceful, punctuated by spectacular individual visitors. Original locals share the world with recognizable fictional and historical sword users, including knights and other non-Japanese traditions. Their coexistence needs no crossover explanation. Village-wide events are deferred.

## 2. Pillars

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
| Roll | Supply alcove (Ore Roller) | Since 2026-10-21 a placeholder: the lever rolls up to 6 ore trays on a stage in the workshop corner, in place, while Allen chooses the ore source (the 2026-10-20 mine and carts are parked; [[Art/Blender Station Review]]). Activate the shared lever: all empty stands cycle ore appearances together and reveal one result each in under five seconds. A stand you own can be **re-rolled as many times as you like** (Allen 2026-10-20); a re-roll replaces the ore on it. Keep the full fantasy material roster. |
| Heat | Forge | Load an ingot and collect it after heating. One furnace heats **one ingot at a time** (Allen 2026-10-20; the forge model shows one tray), and its label shows only the time left, then "Ready!"; heating more at once means buying another furnace in the tycoon. Base heating time is **10 seconds** (approved 2026-10-19), replacing the 15-second prototype duration. No quench or cooling countdown while shaping. |
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

**Current station split:** the anvil forges; the Polishing Station performs the former freehand grinding as an optional step after hilt assembly; etching comes after it, last (2026-10-20). The section title is retained for existing links. The 90% forging rule below describes the player's completed sequence; employee forging and player completion of employee work are defined in §10.4.

**Approved 2026-10-19; replaces the timed Points and freehand hammering prototypes as the intended main mode.**

- **Forging camera (approved 2026-10-19):** slightly angled overhead, showing the blade outline clearly while retaining visible thickness, hammer movement, and the anvil. Keep the entire blade visible throughout lengthening and repositioning. Exact framing and camera movement remain to be tuned.
- **Universal starting blank (approved 2026-10-19):** every sword blueprint starts from the same blank shape and size. Forging stretches it to the selected blade’s length and establishes its distinct profile; do not use blueprint-sized starting blanks. The rolled material still determines its material appearance.
- Guided circles identify hammer strikes. **The blade moves by itself, without visible tongs:** it slides, turns, and flips beneath the fixed hammer point between strikes. Players do not manually reposition it.
- Players hit every circle. No overall timer, timing window, misses, cooling countdown, or reheat loop during shaping. Earlier retry/minimum-hit discussions are superseded by this simpler rule.
- **Staged shaping (approved 2026-10-19):** early hits lengthen the thick blank; middle hits establish the blade’s taper and curve where appropriate; final hits form the point and refine the rough outline. Each hammer impact visibly changes the section beneath it. The blade progresses from a thick blank to a long rough blade to a recognizable sword. Exact hit counts, intermediate shapes, and animation pacing remain to be designed.
- **Impact deformation (approved 2026-10-19):** quickly and smoothly deform the struck area at hammer contact, blending the change into neighboring metal. Flatten or stretch the local section as appropriate to the shaping stage. Avoid discrete shape snaps, wobbling, or a slow melting effect. Exact deformation timing and falloff remain to be tuned.
- Each completed circle shapes its section and increases quality. All circles completed gives **90%**. **Initial implementation uses the same circle/hit count across sword blueprints. Higher-tier swords should eventually require modestly more effort**, rather than making all larger swords automatically take longer. Exact tier thresholds, added effort, circle count, and transition pacing remain to be tuned; the previous 12 is only a prototype baseline. No timing challenge or failure penalty is introduced by this direction.
- **90% blade appearance (approved 2026-10-19):** clean and recognizable, with the intended silhouette, subtle excess metal along the edge, and a dull finish. It should already look like a desirable finished sword after fitting the hilt, not a visibly jagged or misshapen failure. Optional grinding refines the small edge allowance and improves the finish toward the 100% appearance.
- Forging ends at **100%** (changed 2026-10-20 from 90%) and the blade is finished right away; it goes to the Hilt Bench. (Changed 2026-10-20: grinding moved from the anvil to the Polishing Station, an optional step on the finished sword.)
- Polishing (at the Polishing Station, on the assembled sword) is freehand but constrained to remove only excess metal toward the target. It cannot overcut or reduce quality. A full polish adds **+10% value** (finish bonus, like the hilt and etch bonuses). The station is free and available from the start; selling unpolished stays a choice.
- Quality is shown as a percentage, not a grade name. It is now a guided completion/refinement measure; the old silhouette mismatch formula is not the new scoring specification.
- Accent lines and bevels remain automatic visual details on finished swords, suited to the blueprint.
- Server validation must enforce valid circle progress and bounded grinding improvements. The recorded BladeCore/ForgeCheck integration covers this flow; see [[Development/Code Map]] and [[Current Status]] for implementation and remaining validation.

**Balance still to test:** whether grinding feels satisfying and genuinely optional; how many circles keep repeated crafting enjoyable; how grinding progress maps to the final ten percentage points.

## 6. Materials, blueprints & finishes

### 6.1 Materials (rolled at the Ore Roller)

**Roller behavior (revised 2026-10-19):** one shared lever controls all owned material stands. Activating it starts a roulette-style reveal on every empty stand together: ore appearances rapidly cycle, then each stand stops on its rolled material in **under five seconds**. Each stand holds one result. An occupied stand cannot roll until its ore is collected; it is skipped while empty stands roll. Collecting ore does not start a roll. If every stand is occupied, none can roll. Buying another “roller” adds another stand to this shared-lever setup, not another lever. More stands provide more roll results per activation without changing per-result rarity odds. Changing the displayed object’s material/appearance is a suggested animation method; exact reveal duration remains to be tuned.

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
| **Etching / Rune** | Etching Table | Free and instant in the approved interim flow; trace minigame deferred | +15% |
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
- Completed swords can be held, collected, displayed, or sold. Combat and a testing area are outside current scope.

## 7. Customers (NPCs)

**First-sale tutorial (approved 2026-10-19):** no customers visit the player’s shop while they make their first sword. Putting that sword on sale triggers the tutorial customer’s arrival. This replaces the proposed waiting customer/commission before the first craft. Players start with the tantō blueprint and simple on-screen guidance; local commissions introduce wakizashi and katana afterward. This rule applies to the beginning tutorial, not yet to all later crafting.

- Early customers are primarily original local villagers, guards, and wandering swordsmen, with an **early special outsider** hinting at the wider cast.
- Later customers can include knights, pirates, and any fictional or historical sword wielders. The cast combines original regulars and recognizable special visitors; exact named roster is not selected.
- **Displayed stock influences regular customer arrivals. Reputation unlocks surprise special visitors.**
- **Weather traffic (confirmed 2026-10-19):** sunshine can grant extra customer traffic; other weather stays at the normal baseline. Bad weather does not reduce arrivals below baseline. Weather bonuses must respect the first-sale tutorial arrival gate. Bonus values, schedules, and combination with reputation/customer upgrades remain untuned; see [[Design/Workshop Growth]].
- Regular customers have flexible tastes (such as elegance, color, or craftsmanship); special commissions specify concrete combinations.
- Repeat sales build familiarity. Relationship milestones unlock personal commission chains, stories, and rewards.
- Individual special visitors bring distinctive commissions and rewards. No village-wide event system for now.
- Existing preference bonuses are economy baselines; broad taste matching needs a defined rule before implementation.

## 8. Selling & haggling

**Tutorial exception (approved 2026-10-19):** the first customer gives a guaranteed fair offer, providing a clear reward for the first sword. Haggling is introduced on the **second ordinary shop sale**, not the first. Commission deliveries pay their agreed reward and do not count as shop sales for this tutorial step. The exact fair-price calculation remains to be tuned. Regular negotiation rules below apply after the introductory sale.

1. NPC inspects and offers a price (roughly 80–110% of value, nudged by personality).
2. Player chooses **Accept** or **Decline**.
3. On decline, NPC either:
   - raises the offer (chance based on personality; Pirate rarely, Noble often), or
   - leaves unhappy. Each NPC has a hidden **patience** of 1–3 declines.
4. Accepting fills a small **reputation** meter; reputation raises customer frequency and unlocks special customers.

**Built so far (2026-10-17):** a 3-slot display rack with price tags; customers walk in every 12–22 s while a sword is displayed (max 2 at once). The owner gets an offer card (20 s to answer). Openers: Farmer 70–95% of value (1 decline), Adventurer 85–105% (×1.25 for Shortswords, 2 declines), Knight 90–110% (×1.25 for 90%+ blades, 2 declines). A decline gets a 5–15% raise by chance (30% / 45% / 50%), otherwise they leave.

**Cashier upgrade:** an NPC cashier auto-accepts offers above a threshold the player sets (e.g. "accept ≥ 100% of value").

## 9. In-person commissions and letters

- Customers introduce requests **in person**; returning customers can also send **letters**. This replaces the smartphone/text-message framing.
- Special visitors leave **untimed commissions** and return when the sword is ready. Their requests do not expire or lose a speed bonus while the player prepares.
- The tantō blueprint is available from the start with on-screen tutorial guidance. **After the first sale, the next goal is a local wakizashi teaching commission**, which provides its blueprint when the commission begins. A later local teaching commission introduces katana. No workshop purchase or additional tantō sale is required before introducing the wakizashi commission. **The first commission requests an Iron Wakizashi with at least 90% quality.** Completing all forging circles satisfies the quality requirement; grinding remains optional. Iron is available in the starter Ore Roller’s Common pool; no guaranteed roll or odds change has been approved.
- Outside visitors introduce new traditions through a first commission; additional patterns in that tradition become coin purchases.
- Relationships grow through ordinary sales and unlock personal commission chains.
- Coins and gems remain proposed rewards; commissions remain a gem source.
- **Commission delivery:** open the commission and select the finished sword through a picker, then receive the agreed reward. This also applies to the first Iron Wakizashi commission; it does not require putting the sword on sale or negotiating.
- Exact letter interface, active-request capacity, and ordinary commission timing are not settled. The proposed first-session flow in [[Design/Core Loop Review|Core Loop Review]] is not yet approved.

### 9.1 Remote delivery orders

**Confirmed 2026-10-19:** add a separate optional delivery board/station using a village courier or cart. Accept an order showing recipient and requested swords → craft and pack the crate → dispatch → delivery and return trip → collect the payout at the station. An order can be pinned on screen. Upgrade directions include delivery speed and carrying capacity.

This is a parallel order route. In-person/letter commissions retain the direct picker hand-in above, including the first Iron Wakizashi commission. Delivery travel does not require the player to stop crafting. Exact order rules, capacity, rewards, trip time, unlock stage, expiry/cancellation and offline behavior remain open.

The pottery reference's van, 3:30 round trip, 3000-gold upgrade, and 6→9 capacity are comparison notes, not selected assets or balance numbers. Full context: [[Design/Workshop Growth#Optional remote delivery orders]].

## 10. Economy & progression

**Tutorial progression (approved 2026-10-19):** first tantō shop sale → Iron Wakizashi commission (90% minimum, delivered through a picker) → first workshop upgrade. This introduces spending earnings to grow the business. The first upgrade is **a second material stand for the Ore Roller**. One shared lever activates all empty stands together, giving more material results per activation. Occupied stands are skipped until their ores are collected. This increases roll opportunities, not per-result rarity odds. Upgrade price and exact reveal duration (under five seconds) remain undecided.

### 10.1 Currencies

| Currency | Earned from | Spent on |
|---|---|---|
| **Coins** | Selling swords | Blueprints, stations, shop expansions, decor |
| **Gems** | Commissions, special customer tips, Material Index milestones, **Robux purchase** | Customer/client upgrades, Lucky Rolls, timer skips |

### 10.2 Upgrades

**Coin upgrades (smithy & shop):**
- Additional **material stands for the Ore Roller** (the second stand is the first tutorial upgrade; one shared lever rolls all empty stands, separate from luck upgrades)
- Extra **display racks** and **ingot shelf** space
- Additional **anvils, bare-blade rack capacity and finished-sword rack capacity** for employee production; prices and station-assignment rules need design
- Faster **heating** timers
- Better **roll odds** (Lucky Roller I–V)
- New **blueprints** and **finish stations**
- **Shop expansions** (players start with a small Starter Shop, 24 × 14 with 2 sword holders; today's 31 × 38, 3-holder shop is the Upgraded Store (both widened 2026-10-20) (Allen 2026-10-20); one evolving open-front workshop; displays and functional facilities improve business, purely cosmetic decoration gives no stats)

**Gem upgrades (customers):**
- **More Customers**: shorter time between walk-ins
- **More Special Customers**: higher chance of special NPCs
- **More Clients**: more simultaneous commissions
- **Regular Clients**: returning clients send letters sooner

**Automation (late game):**
- **Cashier**: auto-accept offers (see §8)
- **Five employee professions**: furnace operator, smith, finisher, stocker and cashier, with hiring/upgrade UI and levels. The finisher combines hilt assembly and optional polishing; the stocker transfers ready swords from the finished rack to empty holders. **Racks built 2026-10-20:** an Ingot Rack (12 ingots) and a Finished Sword Rack (6 swords) on the courtyard; players carry items and store or take them with E, ready for employees later. Smiths leave bare blades on their own rack and train from below 90% toward 90%. See §10.4. The old fixed 85% apprentice and separate hilter/polisher proposals are superseded; exact values remain untuned.

**Delivery progression (unlock stage and currency open):** improve courier/cart trip speed and carrying capacity; prices and values remain undecided.

### 10.3 Progression arc

**Visual progression direction (2026-10-19):** early game starts sparse with basic stations; mid game adds displayed swords and stations; late game expands the shop with station workers and advanced upgrades. See [[Art/Japanese Village Concept Art|Japanese Village Concept Art]] for the same-plot comparison. Illustrated capacities and precise unlocks are proposals, not fixed balance rules.

| Stage | Player has | Goal |
|---|---|---|
| Early (pacing to test) | Roller, forge, anvil, hilt bench, optional Polishing Station, display; local teaching commissions | First tantō sale, fittings milestone, progress toward wakizashi and katana |
| Mid (pacing to test) | New traditions, letters, better workshop facilities | Customer relationships, additional blueprints and capacity |
| Late (pacing to test) | Cashier, Apprentice, Claymore/Flamberge | Legendary metals, 98%+ blades, Material Index completion |

### 10.4 Employees and production handoffs

**Confirmed from Allen's notes and answers, 2026-10-19:** five professions, with multiple workers per profession possible subject to station/capacity limits. Hire and compare workers through an employee management/upgrade window; employees level through completed work. Buy additional anvils and provide separate bare-blade and finished-sword racks.

- **Furnace operator:** loads, heats and collects ingots for the next stage.
- **Smith:** uses an available anvil and deposits the un-hilted blade on the blade rack. Starter quality is below 90%; training improves forging capability toward a maximum of 90%.
- **Finisher:** combines fitting the selected hilt with optional polishing. Speed and polishing ceiling improve through training. Players can choose fittings and whether to polish. For player etching, pause after assembly and resume final polishing after etching. No separate hilter or polisher profession.
- **Stocker:** visibly carries ready-for-sale swords from the finished-sword rack to empty shop holders. It preserves swords reserved for commissions, deliveries or further finishing, and waits when the shop is full or no eligible swords are ready. Stocking speed is the initial progression direction; display-priority modes remain later options.
- **Cashier:** retains the offer threshold described in §8.

**Player completion is allowed:** the player can take an employee's sub-90% un-hilted blade back to the anvil and complete forging to 90%. After assembly and optional etching, the player can polish beyond an employee's polishing ceiling up to 100% at the Polishing Station. Preserve station order; polishing does not replace unfinished forging.

The production route is furnace operator → smith → bare-blade rack → finisher (hilt, optional polish after any player etch) → ready-for-sale finished-sword rack → stocker → shop holders → cashier. Reserved commission/delivery swords bypass retail stocking. Players can also place their own ready swords on the finished rack for retail automation.

Exact starting quality, polishing ceilings, progression curves, prices, unlock timing, material permissions, intermediate storage, queues and station priority remain open. The current 90–100% implementation needs an explicit extension for sub-90% employee work. This roster does not add an ore attendant, automated etcher or employee courier, and does not decide the separate offline-earnings idea. See [[Design/Workshop Growth#Employees and workstations]].

## 11. World & multiplayer

**Plot scale clarification (2026-10-19):** each player needs a larger property with a distinct storefront for customers and a dedicated place for crafting, plus room to expand. Avoid compressing both into a small shop stall. A connected L-shaped retail/crafting layout is explored in [[Art/Japanese Village Concept Art|Japanese Village Concept Art]]; its exact floor plan and dimensions are not yet approved.

- **6 players per server**, each with a workshop plot in a Japanese swordsmith village. Since 2026-10-21 a joining player gets the first free lot (N2, N1, N3, S2, S1, S3) with a fresh copy of the plot; others can visit but not use it; it is cleared when they leave until saving exists. See [[Design/Six Plots]].
- **Town street (2026-10-21):** the village is one straight street of two-storey machiya (lattice fronts, pent roofs, noren, lanterns, a water channel) running from a village gate to a shrine (the mountains around it are parked until the scenery pass). The six plot lots open onto the street, three per side, each the width of the shop + workshop so the row of buildings is continuous; a lot without a player shows a closed shopfront. See [[Art/Japanese Street]].
- **Shop + back-room workshop (2026-10-21):** one machiya in the street's house row. The shop room is on the street (the Starter Shop, then the two-storey kura Upgraded Store), and a centre door leads to the workshop behind. Crafting runs clockwise round the workshop: ore intake, furnace, anvil, hilt bench, optional polish, optional etch, then the finished rack by the door. Layout: `References/Concept Art/shop design`. This replaces the earlier open-front workshop with visible forging.
- Progression expands the plot with more elaborate roofing, timber, signage and displays: the shop upgrades in place on the street, and the workshop fills with stations. Freeform building placement is not the selected direction.
- **Indoor roof visibility (requested 2026-10-19):** make the roof transparent or cut it away while the player is beneath it, restoring the exterior view outside. A smooth local-only fade/hide is the recommended implementation; exact opacity and detection are tuning decisions. See the exterior/interior pottery reference pair in [[Design/Workshop Growth#Roof visibility while indoors]].
- Warm, cozy, stylized art: timber, tiled roofs, lanterns, stone paths, streams, and mountain scenery. Demon Slayer's Swordsmith Village is an atmosphere reference.
- NPCs travel through the village and visit shops. Admiring other players' shops remains the light social layer; no player trading in v1.
- Cosmetic decoration is freely expressive; functional displays and facilities provide business benefits.
- The previously built medieval cabin (`Models/Archive/SwordShop.fbx`) is a historical asset, not the target shop design. The Japanese open-front workshop is now built in Studio from parts ([[Art/Smithy Redesign|Smithy Redesign]]).

## 12. Technical notes (Roblox)

Implementation details and script paths are maintained in [[Development/Code Map]]; the current state and design/build differences are summarized in [[Current Status]]. The BladeCore port and Japanese workshop rebuild are documented as implemented, while other parts of this design remain future work.

- Studio scripts/models are saved in the place; reusable browser and Luau blade sources also live in `Prototypes/tanto-forge/`.
- Server-owned state and `ForgeCheck` validate forging completion and refinement. The client renders responsive blade motion from BladeCore/BladeData through BladeView.
- Held/displayed blades currently use one EditableMesh per visible sword, a documented resource concern awaiting optimization and published-device testing.
- Saves are still documented as session-only; persistence remains roadmap work.
- The six-player village is the intended structure; the recorded build has one plot (storefront wing + crafting wing + courtyard + expansion lawn), still with shared stations.

## 13. Decisions log

The full dated record is [[Design/Decisions Log|Decisions Log]]. The approved 2026-10-19 decisions supersede conflicting prototype rules, including the medieval cabin, timed forging, minimum-hit failure, damaging grinding, timed hilt taps, smartphone commissions, and universal fitting ladder.

See [[Sessions/2026-10-19]] for this revision's scope and [[Design/Core Loop Review|Core Loop Review]] for recommendations still awaiting discussion.

## 14. Build plan

See [[Development/Roadmap|Roadmap]] for implementation status. Prior completed prototypes remain historical achievements, not evidence that the revised design is built.

Anvil forging, final polishing on its own station, and the Japanese workshop have implementation records. Remaining work includes design/build gaps, first-session progression, saving, village/plot growth, relationships, employees, courier orders, weather traffic bonuses, and indoor roof visibility. The new growth features are not recorded as implemented. [[Development/Roadmap]] owns the actionable task list; this document owns intended game behavior.

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

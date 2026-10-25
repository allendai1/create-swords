---
title: "Sell Swords! — Game Design Document"
status: "approved direction; partially implemented"
source: "[[Archive/Create Swords!|Create Swords!]]"
tags: [gdd, roblox, create-swords]
type: "design"
updated: "2026-10-24"
aliases: ["Create Swords! GDD", "Sell Swords! GDD"]
---

# Sell Swords! — Game Design Document

*Working title: **Sell Swords!** (alternatives were Create Swords! and Craft Swords!).*

> Refined from the original brainstorm in [[Archive/Create Swords!|Create Swords!]]. The brainstorm is left untouched; this note is the working design.
> Direction approved 2026-10-19, with later dated decisions incorporated through 2026-10-24. The latest dated decision takes precedence over older rules. This document describes the intended game, not a claim that the changes are implemented. Earlier prototype details remain in [[Development/Code Map|Code Map]], session notes, and [[Archive/Design/GDD before 2026-10-19 revision|GDD before 2026-10-19 revision]]. New onboarding proposals are separate in [[Design/Core Loop Review|Core Loop Review]].

---

## 1. One-line pitch

**Build your smithy in a Japanese mountain village, forge swords by hand, and earn a reputation among sword wielders from across the world.**

A cozy crafting tycoon inspired by the atmosphere and craftsmanship of Demon Slayer's Swordsmith Village. Daily village life is peaceful, punctuated by spectacular individual visitors. Original locals share the world with recognizable fictional and historical sword users, including knights and other non-Japanese traditions. Their coexistence needs no crossover explanation. Village-wide events are deferred.

## 2. Pillars

**Progression direction confirmed 2026-10-22:** relaxed swordmaking serves the larger fantasy of becoming rich. Make more valuable swords by hand, invest profits in familiar production, then personally pursue the next designs and special commissions. Most upgrades and blueprints are money-led; milestone commissions introduce special designs and sword traditions. After personally crafting a sword shape, pay coins to train employees to produce it in any permitted material supplied to them; no separate training per material combination. Fully trained smiths can match the player's 100% forging quality. Initially the player supplies rolled ore; a later ore attendant runs the existing roller using the same material odds. Training costs and ownership remain open; see [[Design/Workshop Growth#Wealth and staged automation (confirmed 2026-10-22)]].

1. **Making a sword feels satisfying.** Every hammer hit visibly shapes the blade, with sparks, sound, and movement.
2. **Simple actions, optional extra care.** Hitting every forging circle gives 100% quality; optional final polishing on the assembled sword adds 10% to the sword's whole value (Allen 2026-10-20; on the whole value since 2026-10-23). Quality remains a visible percentage and affects price. Employee output has separate capability limits (see §10.4).
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
| Roll | Ore loot box (Ore Roller) | Since 2026-10-22, a loot box in the workshop's back-left corner, from Allen's Call of Duty loot box idea ([[Art/Ore Loot Box]]). Before it there were placeholders: the supply chest (2026-10-21) and the alcove; the 2026-10-20 mine and carts are parked ([[Archive/Art/Blender Station Review]]). Pull the shared lever: the lid opens, one ingot per bought slot (up to 6) floats up, spins through the ore types and locks in on its result, and all drop onto the lid, in 3.6 s. **Spin as often as you like** (Allen 2026-10-24: "Players should be able to spin the ores as many times as they want"): the lever is off only while a roll plays, and pulling it with ore still waiting puts that ore into your hands first (all of it: there is no limit on ingots in hand since later that day, [[Sessions/2026-10-24#No hand limit, 1.7× ingots, labels that don't overlap]]). This supersedes "collect before rolling again" (2026-10-22), which had replaced the unlimited re-rolls of 2026-10-20. With Ore Slots 2–6 bought, **Merge Ore Slots** trades them for more luck (§10.2). Keep the full fantasy material roster. |
| Heat | Forge | Load an ingot and collect it after heating. One furnace heats **one ingot at a time** (Allen 2026-10-20; the forge model shows one tray), and its label shows only the time left, then "Ready!"; heating more at once means buying another furnace in the tycoon. Base heating time is **10 seconds** (approved 2026-10-19, built 2026-10-22), replacing the 15-second prototype duration. **Until the player's first sword is finished an ingot heats in 3 seconds** (Allen 2026-10-22: "first time tutorial, the furnace and other processes need to be sped up"). No quench or cooling countdown while shaping. |
| Forge | Anvil | Choose a hot ingot and unlocked blueprint. Hit every circle, without timing windows or misses. Each hit improves the blade; completing all circles gives **100% quality** (Allen 2026-10-20; was 90%). The anvil view closes when the blade is done. |
| Assemble | Hilt Bench | Choose a blade; its hilt is fitted automatically (since 2026-10-23: the blueprint's own hilt shape, in the best tier unlocked). Attach it by dragging the hilt along onto the tang in one motion (or holding Space / A); it seats with a clang (Allen 2026-10-22, replacing the three knocks of 2026-10-20). No timing bonus or penalty. |
| Polish, optionally | Polishing Station | On the finished sword: freehand polishing along the edge removes the last excess metal and brightens the finish. A fully polished sword is worth **×1.10** (its whole value since 2026-10-23; added to the other bonuses before); it was named "(Polished)" until 2026-10-24, when the tag left every sword name; quality is already 100% from forging (Allen 2026-10-20). The anvil only forges. |
| Etch, optionally (last step) | Etching Table | Apply a finish pattern. The last step, after polishing, because the Etching Table will be an unlocked station (Allen 2026-10-20). Current approved interim flow is free and instant; a trace minigame is deferred. |
| Display | Sword holders | Put the complete sword on display. Stock influences regular visitors. Players start with one 3-sword wall rack in the Starter Shop, then buy a second wall rack, a display table, the Upgraded Store and more racks and tables from tycoon floor pads ([[Design/Tycoon Upgrades]], 2026-10-20). Since 2026-10-22 every wall rack is a three-tier sword shelf (concept art `sword shelf.png`) and every display table is Allen's imported SwordTable with three stands. A displayed sword is centred on its holder, which closes in under a short one. |
| Sell | Customer | Accept or haggle; pushing for more can cause the customer to leave. Sales earn coins and build reputation and familiarity. |
| Deliver, optionally | Delivery board and courier/cart | Fulfill a separate remote order, pack swords (chosen on a packing page since 2026-10-24, §9.1), dispatch, and collect the reward when the courier returns. Direct commissions retain their immediate picker hand-in. |
| Grow | Workshop and commissions | Upgrade the workshop, unlock fittings through crafting, and learn new sword traditions through commissions. |

**Picker behavior (confirmed 2026-10-19):** every item-selection interaction opens its picker every time, even with only one valid item. Do not auto-select the current workpiece or bypass a picker. **One exception since 2026-10-24:** holding a cold ingot and pressing E at the furnace puts that ingot in, with no picker; the picker opens only with empty hands (or a hot ingot or a sword). Closing the anvil's picker with no blade on the anvil now leaves the anvil view. Commission delivery is a parallel route to ordinary display sales: open the commission, select the finished sword through a picker, and receive the agreed reward. No display listing or haggling is required for commission delivery.

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
- Polishing (at the Polishing Station, on the assembled sword) is freehand but constrained to remove only excess metal toward the target. It cannot overcut or reduce quality. A full polish multiplies the whole value by **1.10** (since 2026-10-23; before, a +10% finish bonus added to the hilt and etch bonuses). The polishing action is free after unlocking the station; the recorded station purchase is 250 coins ([[Design/Tycoon Upgrades]]). Selling unpolished stays a choice.
- Quality is shown as a percentage, not a grade name. It is now a guided completion/refinement measure; the old silhouette mismatch formula is not the new scoring specification.
- Accent lines and bevels remain automatic visual details on finished swords, suited to the blueprint.
- Server validation must enforce valid circle progress and bounded grinding improvements. The recorded BladeCore/ForgeCheck integration covers this flow; see [[Development/Code Map]] and [[Current Status]] for implementation and remaining validation.

**Balance still to test:** whether polishing feels satisfying and genuinely optional for its +10% value bonus, how its progress reads, and how many forging circles keep repeated crafting enjoyable.

## 6. Materials, blueprints & finishes

### 6.1 Materials (rolled at the Ore Roller)

**Roller behavior (revised 2026-10-22, 2026-10-24):** one shared lever rolls every bought slot (up to six) in a 3.6-second loot-box show. Each slot holds one result on the lid. **Since 2026-10-24 you can roll as often as you like** (supersedes "collect all waiting results before rolling again", 2026-10-22): the lever is off only while a roll plays, and a pull first puts waiting results into your hands (all of them since the hand limit went, later that day; a NEW card for a first-time metal). Collection does not start another roll. Buying another ore slot increases results per pull without changing per-result rarity odds; merging the slots raises luck (§10.2). The 2026-10-22 rule superseded the older one that skipped occupied stands while rolling empty ones. See [[Art/Ore Loot Box]].

| Rarity | Examples | Base multiplier | Roll odds (starting) |
|---|---|---|---|
| Common | Iron, Copper, Stone, Pewter, Black Iron | ×1 | 60% (59.9% with Secret) |
| Uncommon | Steel, Bronze, Rose Gold, Brass, Amber, Marble | ×1.5 | 25% |
| Rare | Blue Steel, Silver, Jade, Amethyst, Ruby, Frost Iron | ×2.5 | 10% |
| Epic | Gold, Obsidian, Damascus, Sapphire, Magma Steel 🌋, Air | ×5 | 4% |
| Legendary | Mythril, Starmetal, Rainbow Alloy 🌈, Dragonsteel 🐉, Sunsteel ☀️ | ×12 | 1% |
| Secret | Watermelon 🍉, Cardboard 📦, Rubber Duck 🦆 | ×25 | 0.1% |

**30 metals since 2026-10-23** (Allen: "I want to have around 30 different metals/ingots"); the last twelve use Roblox's own materials as their look ([[Sessions/2026-10-23#Thirty metals]]). **31 since 2026-10-24:** **Air**, a new Epic metal (Allen: "an airsword that is part transparent?"; then "Epic"), is pale blue-white glass with the blade about 45% see-through wherever it's drawn, etched too; the ingot is solid pale glass. Epic now has 6 ([[Sessions/2026-10-24#Refinements 3]]).

- Each material has a distinct texture (Damascus swirls, rainbow shimmer), mirroring *Create Pottery!*'s "Cocoa Swirl / Porcelain" clays. **Since 2026-10-23** every metal ingot and blade has a shared surface (hammered ingots, forged-to-mirror blades) tinted by its colour; the distinct per-material patterns are still to come ([[Sessions/2026-10-23#Metal textures on ingots and blades]]). **Since 2026-10-24 Rainbow Alloy has a rainbow texture**, an original in the style of Allen's `rainbow.webp` (a watermarked stock preview, so it isn't used): a katana reads red at the hilt to violet at the tip on both faces, and the ingot is red in the middle, violet at the ends. The sweep is sized for the katana, so a tantō shows red to yellow and a longsword runs on into blue. **Added the same day:** Pewter, Rose Gold and Jade (tinted), Dragonsteel (its own scale texture) and Watermelon (striped rind ingot, pink seeded blade) in a new **Secret** tier for joke metals ([[Sessions/2026-10-23#New metals]]). More ideas: [[Design/Metal Ideas]].
- "NEW" badge and a small celebration the first time a material is rolled; a **Material Index** (collection book) tracks discoveries. **Collection book built 2026-10-22; since 2026-10-23 one ingot card per metal** (30; 31 since Air, 2026-10-24), dark silhouettes until collected ([[Sessions/2026-10-23#Collection book: one ingot per metal]]). Before that: 39 entries, then 90 (30 metals × tantō, wakizashi, katana), silhouettes until that blade × metal is made, polished and etched as badges, saved. **NEW built 2026-10-22:** a rolled metal its roller has never collected shows NEW on the lid, collecting it the first time shows a card (the ingot, NEW, its rarity), and the book dims the names of metals never collected ([[Sessions/2026-10-22#Core loop: requests, reputation, heat/luck, HUD, reward card]]).
- Fantasy materials remain available from the start through the roller odds; they are not gated behind a grounded-materials phase.

### 6.2 Blueprints (sword shapes)

**Blade art direction (approved 2026-10-19):** grounded starter tantō, wakizashi, and katana, with slightly exaggerated proportions for clear readability. Give each its own silhouette rather than simply scaling one katana. Later special blueprints can introduce extravagant fantasy shapes and details. Exact profiles and forging transformation choreography remain under design.

**Japanese starting progression: tantō → wakizashi → katana.** Players start with the **tantō blueprint** and simple on-screen instructions for their first sword. Later local teaching commissions introduce **wakizashi, then katana**, providing each blueprint when its commission begins. **Superseded 2026-10-23 (Allen: "the different swords you get are earned by just buying them through the tycoon pads"):** the Wakizashi Blueprint (60 coins) and Katana Blueprint (400, after it) are bought on one pad spot by the anvil; buying one learns it. Saves that learned a blueprint from a commission count its pad as bought.

Later visitors introduce other sword traditions through a first commission that supplies its required pattern. Additional blueprints within that tradition can be purchased with coins. Longswords, cutlasses, rapiers, claymores, and flamberges remain expansion candidates; their order and prices are not yet tuned. **Built 2026-10-23 (Allen: "Lets do 3 western swords, the longsword, falchion, and the gladius"):** the three are bought on the same blueprint pad after the Katana Sword (Longsword 1,000 → Falchion 2,000 → Gladius 3,500; placeholder prices), not through a commission. Shapes: [[Development/Blade Profile Authoring#Western blades (2026-10-23)]]; other candidates: [[Design/Sword Profile Ideas]].

**Big swords (proposed 2026-10-23, Allen: "a new category of swords that are big swords... ones that take two hands to hold or are different than the typical silhoute. the big swords would require you to purchase a standing big sword rack and it only holds one. they can sell for a lot"):** oversized two-handed blueprints, each shown only on a bought standing rack that holds one, priced well above ordinary swords. The first shape is the **Zanbatō** (a slab with a chisel point, from Allen's buster-sword references), 100 cm, about 6.4 studs with its grip (Allen). **Built 2026-10-23:** the Zanbatō is a blueprint in the game (1,000 coins base, ★5, the katana's hilt for now) with no pad to buy it yet, so it only comes from the Dev panel. The **Big Sword Stand** (2,500 coins, after the Upgraded Store; placeholders) holds one big sword upright by the shop's back wall, and big swords can't go on any other holder. Customers buy from it like any holder. Still open: the Zanbatō's blueprint pad and price, its own hilt, who buys big swords, the two-handed grip, and whether the crafter can make them. See [[Development/Blade Profile Authoring#Big swords (2026-10-23)]] and [[Sessions/2026-10-23#Big Sword Stand]].

Tantō and wakizashi replace the dagger/shortsword starting progression. The old blueprint price/difficulty table is historical, not the approved new progression. Katana's existing smooth curved profile remains a visual reference.

### 6.3 Finishes (optional value-adds)

| Finish | Station | Minigame | Bonus |
|---|---|---|---|
| **Polish** | Polishing Station (built 2026-10-20) | Freehand edge polishing (the old anvil grinding), on the finished sword | ×1.10 on the whole value when fully polished (2026-10-23; +10% added to the other bonuses before) |
| **Color / Enamel** | Etching Table | Paint coverage, pick colours (rainbow = multi-colour) | +10–20%, matches NPC wants |
| **Etching / Rune** | Etching Table | Free and instant in the approved interim flow; since 2026-10-21 the player watches it drawn on their sword (Flame, Eclipse; Tide, Stormroot, Woven Wind, Fracture and Falling Stars since 2026-10-22); trace minigame deferred | +15% |
| **Hilt** | Hilt Bench | Fitted automatically (the blueprint's shape, the best tier unlocked); drag the hilt onto the tang to seat it. Completes the sword (see §6.5) | +0% to +40% price by hilt; some NPCs care |
| **Gem Socket** (late) | Hilt Bench | Insert a gem | Large bonus; consumes a gem item |

### 6.4 Sword value formula

```
Value = Blueprint base
      × Material multiplier
      × Quality multiplier (×1.0 at 80% → ×2.0 at 100%)
      × (1 + hilt bonus + seat bonus + etch bonus)
      × 1.10 if fully polished (since 2026-10-23)
      × NPC preference bonus (see §7)
```

The tooltip on a finished sword shows each factor so players learn what to chase (not built; since 2026-10-22 a card after hilt, polish and etch shows the sword's value and that step's gain). Since 2026-10-20 every player-forged blade is 100% (×2.0); since 2026-10-23 a full polish multiplies the whole value by 1.10 (it was a +10% finish bonus added to the others). The seat bonus is always the full +6% since the drag seating. Review that incentive in [[Design/Core Loop Review|Core Loop Review]]. Employee quality below 90% needs explicit value/refinement rules before implementation, particularly if starting quality is below the table's 80% baseline; do not invent extrapolation. Optional finishes remain optional; other proposed bonuses still need tuning.

### 6.5 Hilt Bench and fittings

- Choose a blade and fittings, then attach by **dragging the hilt onto the tang** (one motion, untimed; 2026-10-22 replaced the three taps). No timing challenge or quality penalty.
- Fittings **match the sword tradition**: Japanese blades use appropriate wrapped grips and tsuba; western swords use their own guards and pommels. No cross-tradition mixing.
- Fittings unlock through **swords-crafted milestones**, without a later coin-purchase requirement.
- Exact fitting sets, milestone counts, and price bonuses need tuning. The old universal Wooden Grip → Gem Pommel ladder is superseded.
- **Built 2026-10-22:** every blueprint and hilt has a tradition, and the bench (and the server) only fit hilts of the blade's tradition. All six current hilts are Japanese koshirae; their names still come from the old ladder and the milestones are unchanged (0/2/4/7/10/15 swords).
- **Superseded 2026-10-23: nothing is chosen** (Allen: "the correct hilt is automatically applied.. so japanese swords have a japanese hilt, and western swords have their respective hilts. no need to choose"). Each blueprint names its hilt shape: the katana hilt for the tantō, wakizashi and katana, and its own hilt for the longsword, falchion and gladius. The six tiers became tradition-free colourings of that shape, and the bench and the crafter fit the best one unlocked. Picking a blade at the bench goes straight to seating. See [[Sessions/2026-10-23#Western swords and automatic hilts]].
- Completed swords can be held, collected, displayed, or sold. Clicking with a held sword swings a four-slash combo, one slash per click (2026-10-23, looks only: nothing is hit). Combat and a testing area are outside current scope.

## 7. Customers (NPCs)

**First-sale tutorial (approved 2026-10-19):** no customers visit the player’s shop while they make their first sword. Putting that sword on sale triggers the tutorial customer’s arrival. This replaces the proposed waiting customer/commission before the first craft. Players start with the tantō blueprint and simple on-screen guidance; local commissions introduce wakizashi and katana afterward. This rule applies to the beginning tutorial, not yet to all later crafting. **Built in part (2026-10-22):** customers only come while a sword is on display, and until the first sale a listing brings one at once (later walk-ins come every 12–22 s). The fair first offer is built too (§8). **The on-screen guidance is built (2026-10-22):** one short line at the top names the next action and an arrow marks the station, from rolling through the first sale, the teaching commissions and Ore Slot 2 ([[Development/Code Map#First session and saving (2026-10-22)]]).

- Early customers are primarily original local villagers, guards, and wandering swordsmen, with an **early special outsider** hinting at the wider cast.
- **Friends as customers (built 2026-10-22):** a shop's ordinary customers wear the avatars and display names of the owner's Roblox friends, and street villagers those of anyone in the server; random looks fill in. Commission visitors keep their own look (no visitors since 2026-10-23: requests come by mail, §9).
- Later customers can include knights, pirates, and any fictional or historical sword wielders. The cast combines original regulars and recognizable special visitors; exact named roster is not selected.
- **Displayed stock influences regular customer arrivals. Reputation unlocks surprise special visitors.**
- **Weather traffic (confirmed 2026-10-19):** sunshine can grant extra customer traffic; other weather stays at the normal baseline. Bad weather does not reduce arrivals below baseline. Weather bonuses must respect the first-sale tutorial arrival gate. Bonus values, schedules, and combination with reputation/customer upgrades remain untuned; see [[Design/Workshop Growth]].
- Regular customers have flexible tastes (such as elegance, color, or craftsmanship); special commissions specify concrete combinations.
- Repeat sales build familiarity. Relationship milestones unlock personal commission chains, stories, and rewards.
- Individual special visitors bring distinctive commissions and rewards. No village-wide event system for now.
- Existing preference bonuses are economy baselines; broad taste matching needs a defined rule before implementation.

## 8. Selling & haggling

**Tutorial exception (approved 2026-10-19):** the first customer gives a guaranteed fair offer, providing a clear reward for the first sword. Haggling is introduced on the **second ordinary shop sale**, not the first. Commission deliveries pay their agreed reward and do not count as shop sales for this tutorial step. The exact fair-price calculation remains to be tuned. Regular negotiation rules below apply after the introductory sale. **Built 2026-10-22:** the fair offer is the sword's full value and a decline gets no counter-offer; on the second sale the offer card says "Decline and they may offer more" and the first decline always brings a better offer.

1. NPC inspects and offers a price (roughly 80–110% of value, nudged by personality). **Since 2026-10-24 ([[Sessions/2026-10-24#Refinement 4]]) never below value** (Allen: "Customers should never make lowball offers"; he chose "Value to +20%"): Farmer 100–110%, Adventurer 100–115%, Knight 105–120%, ×1.25 when they like the sword.
2. Player chooses **Accept** or **Decline**.
3. On decline, NPC either:
   - raises the offer (chance based on personality; Pirate rarely, Noble often), or
   - leaves unhappy. Each NPC has a hidden **patience** of 1–3 declines.
4. Accepting fills a small **reputation** meter; reputation raises customer frequency and unlocks special customers. **Built 2026-10-22:** +1 per shop sale, +3 per board order, +5 per commission; levels 1–8 (0/5/15/30/50/80/120/175 points), each shortening walk-ins 6% on top of Better Advertising; level 3 opens a third board order. It never drops. Special customers are not built ([[Sessions/2026-10-22#Core loop: requests, reputation, heat/luck, HUD, reward card]]). **Since 2026-10-24 the HUD has no star/level pill** (Allen chose "Delivery window only"): the reputation shows as "Rank N" only in the Deliveries window.

**Recorded build:** per-plot displays and customer routes, up to two customers at once (more with the More Clients gem upgrade, and one more with the Shop Promoter since 2026-10-24, §10.4), and an offer shown since 2026-10-22 as a bubble over the customer, e.g. "$120 [+20%]" (green above the sword's worth, red below). **Since 2026-10-23 an offer lasts 45 s** (was 20; a starting value to tune, [[Design/Workshop Urgency Recommendations]]): it rings once, a coin with the seconds left shows over a customer you're too far from (no price), and a waiting customer's card comes 1.5 s after the last one closed. **Since 2026-10-24 every offer has its own card over its customer, several at once,** and a customer says the offer only when its card shows; only the tutorial's first two sales still wait their turn ([[Sessions/2026-10-24#Refinement 4]]). Displayed swords carry no price tag. Before the first sale a listing brings a customer immediately; later arrivals use 12–22 s intervals. The first two ordinary sales use the tutorial exceptions above. Older NPC opener/preference tables are historical tuning; confirm the live `Shared.Customers` catalogue before balancing. Familiarity remains unimplemented (reputation is built, step 4).

**Cashier upgrade:** an NPC cashier auto-accepts offers above a threshold the player sets (e.g. "accept ≥ 100% of value"). **Built 2026-10-24 as the Cashier employee (§10.4)** (Allen: "if they're offering +20% and my setting is set to anything >10%, then it should be sold. Should be a slider in the employee settings/info page"): he sells when an offer is at least the slider's % over the sword's value and otherwise declines, and the customer may raise (he checks each raise). The slider is on his crew page, −20% to +50% in 5% steps, default +10%. Your first two sales stay yours (the tutorial). **Since 2026-10-24 he holds the cash** (Allen: "The cashier should hold all the cash so the player can walk up to him and collect it"; then "press e with him to get the cash out. not just automatically"): he holds a coin pouch with the amount over it, and E at him collects it; a save counts it in your coins.

## 9. In-person commissions and letters

**Requests come by mail (Allen 2026-10-23, supersedes the in-person visitors and the request board below):** "remove the concept of the visitors with their requests. i want the requests to come through mail. for example, we can have a mail button. when clicked it opens your inbox with mail from various people that wanted something. when you have what they're looking for, you can submit in the UI to them and get your reward. the different swords you get are earned by just buying them through the tycoon pads." **Built 2026-10-23 ([[Sessions/2026-10-23#Refinements 2, second list]]):** a Mail button (scroll icon) first in the HUD menu opens the inbox: the named letters (Guard Captain's Wakizashi, Wandering Swordsman's Katana: same rewards and triggers as below) and every rotating order (same clock, pay and gems as below; the clock is random, 3–10 minutes, since 2026-10-24), each with sender, the sword wanted, the reward and Hand in, which opens your swords in the picker (fitting ones first). Hand in is veiled and shakes when nothing fits; an amber dot on the button means an unread letter, a new order or something you can hand in. Opening the mail reads the letters. No visitor walks in and the shop has no request board. Letters teach nothing: the Wakizashi Blueprint (60) and Katana Blueprint (400, after it) are tycoon pads by the anvil (§6.2). **Since 2026-10-24 ([[Sessions/2026-10-24#Refinements 3]]):** the mail no longer says "New order in m:ss", and an empty inbox says "No mail". The left HUD is just the icons (menu buttons, coin and gem counters and the pinned order have no plate; the numbers have a dark outline), and the gem shop button is the House icon (Allen: "Remove the background on left UIs so its just the icons").

- Customers introduce requests **in person**; returning customers can also send **letters**. This replaces the smartphone/text-message framing. *(Superseded 2026-10-23: all requests are letters.)*
- Special visitors leave **untimed commissions** and return when the sword is ready. Their requests do not expire or lose a speed bonus while the player prepares.
- The tantō blueprint is available from the start with on-screen tutorial guidance. **After the first sale, the next goal is a local wakizashi teaching commission**, which provides its blueprint when the commission begins. A later local teaching commission introduces katana. No workshop purchase or additional tantō sale is required before introducing the wakizashi commission. **The first commission requests an Iron Wakizashi with at least 90% quality.** Completing all forging circles satisfies the quality requirement; grinding remains optional. Iron is available in the starter Ore Roller’s Common pool; no guaranteed roll or odds change has been approved.
- Outside visitors introduce new traditions through a first commission; additional patterns in that tradition become coin purchases.
- Relationships grow through ordinary sales and unlock personal commission chains.
- Coins and gems remain proposed rewards; commissions remain a gem source.
- **Commission delivery:** open the commission and select the finished sword through a picker, then receive the agreed reward. This also applies to the first Wakizashi commission; it does not require putting the sword on sale or negotiating.
- **Built 2026-10-22 (Claude's defaults, [[Design/Decisions Log]]):** the Guard Captain walks in after the first sale and asks for a Wakizashi (90%+, 120 coins; any metal since 2026-10-22, so the tutorial never waits on an Iron roll — Allen chose this over a supplied ingot); talking to him or using the shop's request board accepts and teaches the wakizashi, and the sword is handed in at the board through a picker. The Wandering Swordsman asks for a Katana of any metal (90%+, 300 coins) after the wakizashi and the third shop sale. Requests don't expire. Hand-ins don't count as shop sales.
- **Rotating board orders (built 2026-10-22):** after the first commission is handed in, the request board keeps 2 small orders from locals (3 from reputation 3): a known blueprint, sometimes with one twist (Uncommon+ or Rare+ metal, polished, etched; finish twists only once their station is bought). Handed in through the picker like a commission for **1.2× the handed-in sword's value** plus 1–3 gems. The board opens full; after that **a new order comes 3 to 10 minutes after the last, at random** (since 2026-10-24, a fresh gap per order; Allen: "The orders should actually be randomized, with a minimum of 3 minutes to say 10 minutes"; supersedes every 3 minutes, 2026-10-23) while it has room, also while the player is away (2026-10-23; before, a new order replaced a filled one at once and paid about 1.5× a middling sword of the shape). Not shop sales; no expiry; saved ([[Sessions/2026-10-22#Core loop: requests, reputation, heat/luck, HUD, reward card]]).
- Exact letter interface, active-request capacity, and ordinary commission timing are not settled. [[Design/Core Loop Review|Core Loop Review]] separates this confirmed sequence from proposed timing targets and playtest questions.

### 9.1 Remote delivery orders

**Confirmed 2026-10-19:** add a separate optional delivery board/station using a village courier or cart. Accept an order showing recipient and requested swords → craft and pack the crate → dispatch → delivery and return trip → collect the payout at the station. An order can be pinned on screen. Upgrade directions include delivery speed and carrying capacity.

This is a parallel order route. In-person/letter commissions retain the direct picker hand-in above, including the first Wakizashi commission. Delivery travel does not require the player to stop crafting. Exact order rules, capacity, rewards, trip time, unlock stage, expiry/cancellation and offline behavior remain open.

**Built 2026-10-22, after Create Pottery!'s deliveries ([[Sessions/2026-10-22#Deliveries]]):** the Delivery Cart upgrade (1,200, after Ore Slot 2) opens the bay door and brings the board and cart. The board's window has Orders (Bulk: any metal up to the cart's capacity; Special: one twist; Skip; Accept one at a time) and Cart (Capacity 3–6 crates, Speed 2:30–1:10 a trip, bought with coins), a rank bar and a four-step trip tracker. Pack fitting swords through the picker (on a packing page instead since 2026-10-24, below), send the cart (it rolls out and back), collect **1.1× the packed swords' value** (2026-10-23: 1.3× at first, lowered the same day so the shop keeps its job; was ≈ request pay × count × 1.1), gems and one reputation per sword. The order is pinned on screen (off by default since 2026-10-24, below); trips finish offline; cancelling before sending returns the swords.

**Cart vs shop (2026-10-23, [[Sessions/2026-10-23#More refinements]]):** the cart is the sure, quick way to sell a lot; the shop usually pays more. A delivery pays **0.8× the packed swords' value** (supersedes 1.1×), the cart carries **6 / 9 / 12 / 15** swords by Capacity level, and a **Bulk Order takes any sword**; a Special Order keeps its shape and twist (2–4 swords).

**Packing page (2026-10-24, [[Sessions/2026-10-24#Refinements 3]]):** Allen: "once i accept a delivery. it should show a page that i can then choose which swords to fill into the delivery. look at the clay game reference". Accepting an order opens a page like Create Pottery!'s: what the order wants, one crate slot per sword and your fitting swords as cards (what the cart pays for each). Tap a card to pack it and a slot to take it back. **Auto-Fill** packs the cheapest first (keeping your best for the shop), **Cancel Order** drops the order, and **Fill the Crate** sends the cart once every slot is full. Swords leave your inventory only then. The pinned order is **off by default**: Pin on the page or on the active order card shows it for the session.

**Delivery bay (2026-10-22):** every plot has a fenced yard in the lane beside its shop, with a gateway onto the street, kept for the courier's cart (Allen: "each plot should have an area where we can eventually add a delivery carrier. maybe a guy with a carriage. potentially could carry over into the street."). Nothing works there yet. When delivery is unlocked, a door opens in the shop's wall onto the bay (built 2026-10-22, hidden until then). **Courier (built 2026-10-23, [[Sessions/2026-10-23#Refinements 2, second list]]):** someone pulls the cart: out of the bay and down the street toward the gate when it's sent, and back, reversing it into the bay, as the trip's timer runs out.

The pottery reference's van, 3:30 round trip, 3000-gold upgrade, and 6→9 capacity are comparison notes, not selected assets or balance numbers. Full context: [[Design/Workshop Growth#Optional remote delivery orders]].

## 10. Economy & progression

**Permanent growth (confirmed 2026-10-22):** the player retains wealth and workshop progress while expanding into higher-value swords, facilities and prestigious customers. No rebirth/prestige reset is selected for the current plan, with one exception since 2026-10-24: **Merge Ore Slots**, a rebirth for the ore box only (Allen: "Its basically a rebirth"), resets Ore Slots 2–6 for more luck and keeps everything else (§10.2). Detailed late-game milestones and expansion limits remain open.

**Tutorial progression (approved 2026-10-19; mail since 2026-10-23):** first tantō shop sale → the Guard Captain's letter ("Open your mail") → buy the Wakizashi Sword pad (60; named Wakizashi Blueprint until 2026-10-23; the guide sends you round the tantō loop again until you can afford it) → forge it → hand it in from the mail (90% minimum, through a picker, 120 coins) → first workshop upgrade, **Ore Slot 2**. The purchase already exists; since 2026-10-22 the guide points to it once the Iron Wakizashi is handed in (the first sale plus the 120-coin reward is about 160). The currently recorded price is 75 coins and needs affordability testing. Each bought slot adds one result per pull; the 3.6-second loot-box show supersedes the old empty-stand behavior (its collect-before-reroll rule was dropped 2026-10-24: roll as often as you like). More slots increase output, not per-result rarity odds.

### 10.1 Currencies

| Currency | Earned from | Spent on |
|---|---|---|
| **Coins** | Selling swords | Blueprints, stations, shop expansions, decor |
| **Gems** | **Daily rewards** (built 2026-10-22), commissions, special customer tips, Material Index milestones, **Robux purchase** | Customer/client upgrades, Lucky Rolls, timer skips |

### 10.2 Upgrades

**Coin upgrades (smithy & shop):**
- Additional **material stands for the Ore Roller** (the second slot is the first tutorial upgrade; one shared lever rolls all bought slots, as often as you like since 2026-10-24 (waiting results go to your hands first), separate from luck upgrades)
- Extra **display racks** and **ingot shelf** space
- Additional **anvils, bare-blade rack capacity and finished-sword rack capacity** for employee production; prices and station-assignment rules need design. **Since 2026-10-24** Finished Sword Rack 2 (600, after the first) adds a second 6-hook rack, 12 hooks in all
- Faster **heating** timers — **built 2026-10-22:** Faster Heating I–III (300/900/2500 coins; 10 → 8 → 6 → 4 s, every furnace); since 2026-10-25 Furnace 2 comes only after Faster Heating III
- ~~Better **roll odds** (Lucky Roller I–V)~~ **removed 2026-10-25: merging is the only luck** ([[Sessions/2026-10-25#Refinements 5]]); was **built 2026-10-22 as I–III** (400/1200/3000 coins, after Ore Slot 2; non-Common odds ×1.2/1.45/1.75, Common 60 → 52 → 42 → 30%) ([[Sessions/2026-10-22#Core loop: requests, reputation, heat/luck, HUD, reward card]])
- **Merge Ore Slots** (a rebirth for the ore box only) — **built 2026-10-24** (Allen: "once you get 6 rollers, you can actually merge so that rare clay turns up more often and you get back a single roller and new ones cost more"; then "Repeatable, gentler prices"): with Ore Slots 2–6 bought, their pad becomes Merge Ore Slots. Merging is free and repeatable: Slots 2–6 go back to unbought (slot 1, coins and everything else stay), luck is ×(1 + 0.5 × merges) on top of Lucky Roller, and the Ore Slot pads cost ×1.5 per merge (Slot 2: 75 → 112 → 168). Waiting ore goes to your hands first (all of it since the hand limit went, later that day). **Luck keeps paying past the old ceiling** (Claude, the same day): the rarer tiers take their luck-multiplied odds from the rarest down while every tier below keeps at least 10%, unchanged below luck ~2.24. At Lucky III, Legendary is 1.7%, then 2.6% / 3.5% / 4.4% after 1 / 2 / 3 merges ([[Sessions/2026-10-24#Refinements 3]])
- New **blueprints** and **finish stations**
- **Shop expansions**: start with one three-sword wall rack in the Starter Shop; buy further racks, tables and the Upgraded Store. The shop grows from about 28 to 40 studs deep and the workshop moves back 12 studs, and the Upgraded Store has a two-storey kura front with a gold-framed signboard and wall lamps (its extra decor was removed on 2026-10-22: the shop holds only what the game uses). See [[Design/Tycoon Upgrades]]. Purely cosmetic decoration gives no stats.

- **Rickshaw parking** — **built 2026-10-23:** Rickshaw Bay 1–3 (500/1,500/4,000 coins, after Display Table 1): each bay lets one more customer in at once on top of More Clients; those customers arrive by rickshaw (after Create Pottery!'s parking spaces)

**Gem upgrades (customers):** bought in the Gem Shop menu, not on floor pads. **Built 2026-10-22:** Better Advertising (3 levels, 25/60/120 gems: walk-ins every 12–22 → 10–18 → 8–15 → 6–12 s) and More Clients (2 levels, 40/100 gems: 2 → 3 → 4 customers at once). VIP clients wait for special customers. **Daily reward:** a 7-day streak that never resets (5, 5, 10, 10, 15, 15, 30 gems; a gap moves on one day, it loops after day 7), claimed from a popup on join. Values are tuning knobs.
- **More Customers**: shorter time between walk-ins
- **More Special Customers**: higher chance of special NPCs
- **More Clients**: more simultaneous commissions
- **Regular Clients**: returning clients send letters sooner

**Automation (late game):**
- **Cashier**: auto-accept offers (see §8; built 2026-10-24 as an employee with a % slider, §10.4)
- **Five initial employee professions**: furnace operator, smith, finisher, stocker and cashier, with hiring/upgrade UI and levels; an ore attendant is a later upgrade. Since 2026-10-24 the stocker and cashier are built, alongside a shop promoter and a sword etcher (§10.4). The finisher combines hilt assembly and optional polishing; the stocker transfers ready swords from the finished rack to empty holders. **Racks built 2026-10-20:** an Ingot Rack (12 ingots) and a Finished Sword Rack (6 swords; Finished Sword Rack 2 adds 6 more since 2026-10-24) in the workshop; players carry items and store or take them with E, ready for employees later. Smiths leave bare blades on their own rack and improve from lower starter output toward **100% forging quality** when fully trained. See §10.4. The old fixed 85% apprentice, 90% ceiling and separate hilter/polisher proposals are superseded; starting values and progression remain untuned.

**Delivery progression (unlock stage and currency open):** improve courier/cart trip speed and carrying capacity; prices and values remain undecided.

### 10.3 Progression arc

**Visual progression direction (2026-10-19):** early game starts sparse with basic stations; mid game adds displayed swords and stations; late game expands the shop with station workers and advanced upgrades. See [[Archive/Art/Japanese Village Concept Art|Japanese Village Concept Art]] for the same-plot comparison. Illustrated capacities and precise unlocks are proposals, not fixed balance rules.

| Stage | Player has | Goal |
|---|---|---|
| Early (pacing to test) | Roller, forge, anvil, hilt bench, optional Polishing Station, display; local teaching commissions | First tantō sale, fittings milestone, progress toward wakizashi and katana |
| Mid (pacing to test) | New traditions, letters, better workshop facilities | Customer relationships, additional blueprints and capacity |
| Late (pacing to test) | Cashier, Apprentice, Claymore/Flamberge | Legendary metals, 98%+ blades, Material Index completion |

### 10.4 Employees and production handoffs

**Built 2026-10-23:** the sword crafter, hired for 1,000 coins on its own pad once Anvil 2 (1,500) is bought (the pad since [[Sessions/2026-10-23#Refinements 2]]; its window opens at Anvil 2 or from the HUD's crew button), trained per shape you've made (200 / 600 / 1,500), starts at 70% and gains 3% every 3 swords to 100%; it takes the cheapest ingot from the Ingot Rack, heats it at a free furnace, forges at Anvil 2, fits your best unlocked hilt, polishes when the station is free and racks the sword ([[Sessions/2026-10-23#The sword crafter (first employee)]]). **Roster ([[Sessions/2026-10-23#Refinements 2, second list]]):** five crafters in a Create Pottery!-style crew window (roster, stats, station), one working at Anvil 2; see [[Design/Workshop Growth]]. **Since [[Sessions/2026-10-23#Urgency phase 2: the crafter's furnace and your forgotten ingot]]:** Anvil 2 comes after the Ingot Rack, Furnace 2 and the Finished Sword Rack, and a ready ingot you leave in a furnace for 10 s is taken out by the crafter (into your hands, hot) when it needs that furnace.

**Built 2026-10-24 ([[Sessions/2026-10-24#Refinements 3]]):** four more employees, one person per role, each hired on its own pad like the Sword Crafter (Allen chose "A pad each"). Each shows "Role / Name / Lv. n" overhead, levels every 5 jobs to Lv. 11 and has one perk that grows. Prices, names and perks are placeholders.

- **Stocker (Sora, 2,000, after the Sword Crafter):** carries swords one at a time from the rack(s) to empty shop holders; waits when the rack is empty or the shop is full. Perk: walk speed 8 → 12.
- **Cashier (Aki, 3,000, after the Upgraded Store):** stands at the old shop counter, back in front of the back wall right of the workshop door, and answers offers by your slider (§8), facing the shop (since 2026-10-24 he doesn't turn to each customer); what he takes he holds until you press E at him (§8). Perk: answer time 3 s → 1 s.
- **Shop Promoter (Kaito, 1,500, after Display Table 1):** on the street left of the shop door, waves at the nearest passer-by or customer every few seconds (since 2026-10-24 he faces the street and turns only to people in front of him). Walk-ins come sooner and one more customer can be in the shop at once (Claude's default for Allen's "stat increaser"). Perk: walk-ins 20% → 35% sooner.
- **Sword Etcher (Yume, 2,000, after Etching Table 2):** takes un-etched swords off the rack, etches the pattern picked on his crew page at **Etching Table 2** (2,500, after the Etching Table and the Finished Sword Rack, in the workshop's right-back corner; only he uses it) and racks them again. While he has a pattern, the Stocker leaves un-etched swords for him. Perk: etch time 10 s → 5 s.

The crew window has a tab per hired role and a page per employee; its dot lights only when someone is waiting on you. The crafter counts the sword the Etcher is carrying as taking its hook, so it can't fill that hook while he works. None of these loops has run in Play yet.

**Outfits (2026-10-24, [[Sessions/2026-10-24#Refinement 4]]):** every employee is dressed from the Roblox catalog (Allen: "Give employees more complete outfits"): the crafters in a smith's apron or a work kimono with a hachimaki, the Stocker in a jinbei, the Cashier in a haori over hakama, the Promoter in a festival yukata, the Etcher in a floral kimono with glasses. **The racks are never the crafter's** since the same day: you can store and take while he walks over (stations are still blocked).

**Latest decision, 2026-10-22:** the first employee is a **sword crafter**, operating the anvil, polishing and placing the sword in the sword rack. This supersedes separating forging and polishing between smith and finisher for that first hire. Hilt assembly responsibility and input supply still need clarification; polishing remains on an assembled sword. Reconcile the older five-role breakdown below and its bare-blade handoff before implementation; it is not the final roster under this revision. The later ore attendant, paid shape training and 100% trained forging ceiling remain selected. See [[Design/Workshop Growth#First employee — sword crafter (latest decision, 2026-10-22)]].

**Confirmed from Allen's notes and answers, 2026-10-19:** five professions, with multiple workers per profession possible subject to station/capacity limits. Hire and compare workers through an employee management/upgrade window; employees level through completed work. Buy additional anvils and provide separate bare-blade and finished-sword racks.

- **Furnace operator:** loads, heats and collects ingots for the next stage.
- **Smith:** uses an available anvil to forge trained sword shapes in permitted supplied materials and deposits the un-hilted blade on the blade rack. Starter quality is lower; fully trained smiths can reach **100% forging quality**, matching manual forging (revised 2026-10-22; replaces the 90% ceiling). Starting quality and progression costs/curve remain open.
- **Finisher:** combines fitting the selected hilt with optional polishing. Speed and polishing ceiling improve through training. Players can choose fittings and whether to polish. For player etching, pause after assembly and resume final polishing after etching. No separate hilter or polisher profession.
- **Stocker:** visibly carries ready-for-sale swords from the finished-sword rack to empty shop holders. It preserves swords reserved for commissions, deliveries or further finishing, and waits when the shop is full or no eligible swords are ready. Stocking speed is the initial progression direction; display-priority modes remain later options. **Built 2026-10-24** (above): it carries from the Finished Sword Rack(s), and its perk is walk speed.
- **Cashier:** retains the offer threshold described in §8. **Built 2026-10-24** (above): the threshold is a % over value set on a slider.

**Player completion is allowed:** the player can improve an employee's unfinished bare blade at the anvil toward 100% forging quality and improve its assembled finish separately. Fully trained smiths can also reach 100%; starter quality, remaining-work representation, recovery/data/value rules and finisher polishing ceilings need design before implementing employees. The older employee 90% ceiling and polishing-to-100%-quality model are superseded. Polishing remains a separate finish bonus and must not substitute for unfinished forging.

The production route is furnace operator → smith → bare-blade rack → finisher (hilt, optional polish after any player etch) → ready-for-sale finished-sword rack → stocker → shop holders → cashier. Reserved commission/delivery swords bypass retail stocking. Players can also place their own ready swords on the finished rack for retail automation.

Exact starting quality, polishing ceilings, progression curves, prices, unlock timing, material permissions, intermediate storage, queues and station priority remain open. The current 90–100% implementation needs an explicit extension for sub-90% employee work. **Later revision, 2026-10-22:** retain these five initial professions and add an ore attendant as a later upgrade, operating the existing roller with unchanged material odds. Initial employees consume player-supplied ore; familiar shapes require a personal first craft and paid training. Hiring, training and upgrades are one-time purchases, with **no ongoing wages**. Add **capped offline workshop earnings as a later feature** after online automation is balanced, collected on return; cap, rate, unlock and stock/ore-attendant rules remain open. No employee courier is selected; courier offline rules are separate. (The Sword Etcher, built 2026-10-24, supersedes "no automated etcher is selected".) See [[Design/Workshop Growth#Employees and workstations]].

## 11. World & multiplayer

**Current layout (2026-10-22):** each player has a street-facing shop with a connected back-room workshop on the simplified six-lot map. The recorded lot footprint is 48.5 × 96 studs; upgrading deepens retail space and moves the workshop back. The earlier L-shaped property concepts in [[Archive/Art/Japanese Village Concept Art]] are historical visual studies, not the current construction plan.

- **6 players per server**, each with a workshop plot in a Japanese swordsmith village. Since 2026-10-21 a joining player gets the first free lot (N2, N1, N3, S2, S1, S3) with a fresh copy of the plot; others can visit but not use it; it is cleared when they leave, and since 2026-10-22 their purchases, displays and racks come back on whichever lot they get next time ([[Development/Saving]]). See [[Design/Six Plots]].
- **The map (2026-10-22):** a small walled Japanese town.
  - **Street:** one broad street (fronts 72 apart) runs from a timber gate to a small shrine. Since 2026-10-22 it is packed earth with a strip of cut stones down the middle and stone gutters (a tidy cut-stone version is kept to compare). Stepped block mountains ring the town outside the walls.
  - **Plots:** three per side, each separated from the next by a 48-wide paved lane (a full shop width). The middle pair stood 8 studs back as a junction until 2026-10-24; now N2 and S2 line up with the street like the other lots (Allen: "The shop building is misaligned with the actual street"; [[Design/Six Plots]]). Two lanes run on through the back wall.
  - **Other buildings:** a few small houses at the edges, with no clutter.
  - **Unclaimed lots:** all six plots are always on the map; a lot without a player shows its plot, empty and unusable.
  - **History:** this replaced the continuous town street of 2026-10-21 ([[Archive/Art/Japanese Street]]) after Allen compared it, a broader redesign and this simplified map. See [[Art/Town Street Redesign References]].
- **Shop + back-room workshop (2026-10-21):** one machiya on each separated player lot. The shop room is on the street (the Starter Shop, then the two-storey kura Upgraded Store), and a centre door leads to the workshop behind. Buying the Upgraded Store pushes the workshop 12 studs further back, so the shop room grows from 28 to 40 deep. Crafting runs clockwise round the workshop: ore intake, furnace, anvil, hilt bench, optional polish, optional etch, then the finished rack by the door. Layout: `References/Concept Art/shop design`. This replaces the earlier open-front workshop with visible forging. Since 2026-10-22 the workshop is one working room ([[Art/Workshop Layout]]): supply chest back-left, furnaces on a shared hearth, the anvil centred in front of them, and a finishing bench along the right wall (hilt → polish → etch toward the door).
- Progression expands the plot with more elaborate roofing, timber, signage and displays: the shop upgrades in place on the street, and the workshop fills with stations. Freeform building placement is not the selected direction.
- **Indoor roof visibility (built):** `RoofHider` locally fades unlocked plot roofs while the player is inside and restores them outside. Current layout, eave/detection transitions and station cameras still need Play checks. See the exterior/interior pottery reference pair in [[Design/Workshop Growth#Roof visibility while indoors]].
- Warm, cozy, stylized art: timber, tiled roofs, lanterns, stone paths, streams, and mountain scenery. Demon Slayer's Swordsmith Village is an atmosphere reference. **Since 2026-10-22:** a Genshin-inspired look (Inazuma-like) across the village and plot: painted textures, livelier colours, soft lighting, round posts and rolled eaves, blue-violet roofs and an anime skybox; the block mountains keep their low-poly look, and there are no trees, shrubs or scattered rocks for now ([[Sessions/2026-10-22#Genshin style rolled out]], [[Sessions/2026-10-22#Smooth trees and mountains removed]], [[Sessions/2026-10-22#All trees, shrubs and rocks cleared]]).
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

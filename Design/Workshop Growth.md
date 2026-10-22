---
title: Workshop Growth
status: direction confirmed — balance and implementation details open
type: design
date: 2026-10-19
updated: 2026-10-22
tags: [design, employees, delivery, weather, camera, create-swords]
---

# Workshop Growth

Organized from Allen's [[Random thoughts]] and follow-up answers on 2026-10-19. The [[Design/Game Design Document]] owns intended behavior, [[Development/Roadmap]] the work list, and [[Current Status]] implementation status. Employees, functional courier orders and weather bonuses remain design work. Roof fading, the delivery bay/hidden door, and ingot/finished-sword racks have implementation records; see [[Current Status]] for verification limits.

Original wording: [[Archive/Design/Random thoughts before growth alignment — 2026-10-19]]. Reference-game prices, timers, and capacities are observations from Allen's notes, not selected balance values for Sell Swords!.

## Employees and workstations

### Wealth and staged automation (confirmed 2026-10-22)

Allen's roadmap discussion establishes relaxed swordmaking as the enjoyable activity and becoming rich as the larger tycoon fantasy. Progression moves from making more valuable swords by hand to scaling familiar production, while the player personally explores new designs and special commissions. Most upgrades and blueprints are bought with profits; milestone commissions introduce special designs and new sword traditions. Progression does not add precision penalties or retries to ordinary manual crafting.

**Permanent growth selected:** retain accumulated money and workshop progress, expanding through more valuable swords, facilities and prestigious customers. Rebirth/prestige resets are not part of the current progression plan. The exact long-term content ladder and expansion limits remain to design.

After personally crafting a sword shape, the player can spend coins to train employees to produce that shape in any permitted material supplied to them. Training is per shape, not per material-and-shape combination. It is an investment in future production, separate from employee capability/level progression. Training ownership, prices, material permissions and finish selection remain open.

Initial automation consumes ore rolled and stocked by the player. A later **ore attendant** upgrade operates the existing roller and collects its results using the same material odds. This adds a later sixth profession to the original five; it supersedes the earlier exclusion of an ore attendant. Unlock timing, output/storage handling, input reservations and full-storage behavior need design. Workers automate trained familiar production; the player's next discoveries and special commissions remain hands-on goals. Automated etching is not selected; offline earnings are addressed below.

**Employee costs:** hiring, recipe training and worker upgrades are one-time purchases. Employees have no ongoing wages; an idle workshop does not drain the player's coins.

### Later capped offline earnings (confirmed 2026-10-22)

Once automation is established and online production is balanced, add limited offline workshop earnings, collected on return. This is a later feature, not initial employee scope. The cap duration, earning rate, unlock requirements, stored-material consumption and ore-attendant contribution remain undecided. Define how the calculation relates to actual production capacity and persisted stock before implementation; offline earnings must not duplicate stock or online payouts. Courier offline behavior remains a separate unresolved rule.

### First employee — sword crafter (latest decision, 2026-10-22)

Allen selected a **sword crafter as the first employee**: operates the anvil, polishes the sword and deposits it in the sword rack. This supersedes the earlier split assigning forging to a smith and polishing to a separate finisher for this first hire. Confirm whether the crafter also fits the hilt, its input supply and any player handoff before defining the full job. Keep polishing on an assembled sword. The earlier five-profession breakdown below is a reference to reconcile, not a final role count under this revision. The later ore attendant remains selected.

### Earlier role breakdown — reconcile with the sword crafter

- Buy additional anvils so hired smiths have places to work. Employee production uses workshop space and station capacity.
- Provide an employee management/upgrade window for hiring more workers and comparing workers with different speeds and quality capabilities.
- Workers have levels and progress through completed work. Better hires and training improve relevant capability; exact curves and thresholds remain untuned.
- **Five initial employee roles confirmed:** furnace operator, smith, finisher, stocker, and cashier; a later ore attendant is confirmed above. The finisher combines hilt assembly and optional polishing; there is no separate hilter or polisher profession.
- A smith leaves an un-hilted blade on the **bare-blade rack**. The finisher takes that blade, attaches the selected fittings, and optionally polishes the completed sword to its worker ceiling. If the player wants to etch, the finisher pauses after assembly and polishing resumes after etching.
- A separate **finished-sword rack** holds swords ready for the retail handoff. The stocker visibly carries eligible swords from it into empty shop holders.
- **Quality ceiling revised 2026-10-22:** starter smiths produce lower-quality blades, but fully trained smiths can reach **100% forging quality**, matching completed manual forging. This supersedes the older 90% employee ceiling. Starting quality, progression curve, training costs and player recovery details remain open; polish remains a separate finish bonus.
- The finisher's speed and polishing ceiling improve through training. Exact values remain untuned; hilt assembly does not gain a new quality minigame from combining the roles.
- **The player can improve both stages:** resume an employee's un-hilted blade at the anvil and improve its assembled finish at the Polishing Station. Forging can reach 100%; define the remaining work and recovery data for employee blades before implementation. Worker polish ceilings remain open. Polishing does not substitute for unfinished forging.
- Retain the existing cashier role and its configurable offer threshold.

| Role | Responsibility | Progression direction |
|---|---|---|
| Furnace operator | Load, heat, and collect ingots | Handling/heating speed; values untuned |
| Smith | Forge trained sword shapes using permitted materials; deposit bare blades | Speed and forging capability up to 100% when fully trained |
| Finisher | Fit selected hilts; optionally polish after any chosen etch | Speed and polishing ceiling |
| Stocker | Carry ready-for-sale swords from the finished rack to empty holders | Stocking speed initially |
| Cashier | Handle offers using the player's acceptance threshold | Exact progression remains open |

The five initial professions are not a five-worker population cap. Multiple workers may share a role, subject to future station/capacity limits. The later ore attendant becomes a sixth profession; no automated etcher is selected. The courier remains part of the separate delivery system.

### Production handoff

```text
Cold ingot → furnace operator / player → hot ingot
    → smith on an available anvil → un-hilted blade rack
    → optional player forging completion toward 100% (recovery mechanics to design)
    → finisher / player fits hilt → complete sword
    → optional player etching → optional final polishing by finisher / player
    → ready-for-sale finished-sword rack → stocker → shop holders → cashier

Swords reserved for direct commissions or courier deliveries bypass retail stocking.
```

Both bare-blade and finished-sword racks are now selected. Storage for hot ingots and intermediate swords awaiting etching/polishing remains open. The stocker only takes swords marked ready for sale; it preserves commission/delivery reservations and further-finishing work, and waits when holders are full or no eligible stock is ready. The stocker does not negotiate prices. Highest-value/oldest-stock/type priorities are later options, not selected initial rules. Automated etching is not selected. Later capped offline earnings have their own design requirements above.

### Details still to design

- Starting forging quality, work/XP thresholds, maximum level, speed curves, hiring prices, and the relationship between hire tier and training.
- Polishing ceilings and representation of polish progress on sub-90% employee blades. The current implementation's 90–100% refinement model needs a deliberate extension.
- Assignment, dedicated versus shared stations, player/worker priority, queues, and behavior when inputs run out or the rack is full.
- Allowed materials/blueprints and material reservations before workers can consume valuable inputs.
- Whether trained finishers can fully polish a sword and the employee unlock stage. Smith forging has a confirmed 100% ceiling; finisher polish capability is a separate decision. Ongoing wages are excluded; no premium-currency hiring requirement was chosen.

## Optional remote delivery orders

### Confirmed direction

**Space built, gameplay pending (2026-10-22):** each plot has a delivery bay and a doorway hidden until a future `Delivery` purchase. Add a **separate delivery board/station with a village courier or cart**; its catalogue entry/pad, packing, dispatch and payouts remain unbuilt. Existing in-person and letter commissions retain direct picker hand-in and agreed rewards. The first Iron Wakizashi teaching commission stays a direct commission.

Adapt the qualitative flow in Allen's reference:

1. Accept an order identifying its recipient and requested swords.
2. Craft matching swords and pack the order's crate.
3. Dispatch the courier/cart.
4. Wait for delivery and return while continuing workshop activities.
5. Collect the payout at the delivery station when it returns.

An order can be pinned on screen. Delivery speed and carrying capacity are upgrade directions. Exact active-order count, matching rules, capacity, rewards, timer, unlock stage, expiry/cancellation rules, offline behavior, and upgrade prices remain open.

### Reference values — not game balance

Allen described Create Pottery!'s van as taking **3 minutes 30 seconds** to deliver and return, a **3000-gold** delivery upgrade, and capacity increasing from **6 to 9 pieces**. Preserve those as comparison values only. The selected presentation here is a village courier/cart, not a modern van.

## Weather and customer traffic

Confirmed: weather grants **positive traffic bonuses**, with sunshine as the example. Other weather uses normal baseline customer traffic; bad weather does not reduce it below baseline.

Preserve the first-sale tutorial: no visitors before the first sword is listed; listing triggers the tutorial customer. Weather does not change existing commission requirements or expiry rules. Bonus amounts, weather types/durations, scheduling, and interaction with reputation/customer upgrades remain open. No paid weather controls were chosen.

## Roof visibility while indoors

Allen requested that the roof become transparent or disappear when the player is under it, making the workshop feel open. The supplied reference pair shows an opaque exterior and a roof cutaway inside:

![[References/Create Pottery! game image reference/closed roof (1).png]]

![[References/Create Pottery! game image reference/closed roof (2).png]]

Both files are named "closed roof"; the second is the indoor/cutaway example referred to as "open roof" in the inbox.

**Implemented:** `StarterPlayerScripts.RoofHider` locally fades unlocked roofs on a plot when the viewing player enters its interior; empty plots retain the same cutaway behavior. Roof fading is no longer missing implementation. Playtest the current shop/workshop, transition bounds, eaves and station cameras; opacity and timing remain tuning choices. See [[Development/Code Map]].

## Clarification resolved

Allen approved combining hilting and polishing as the **finisher**, with the **stocker** filling the fifth profession. This supersedes the separate-hilter / undecided-polisher wording in the earlier organization record. Balance values and operational details above remain open.

Related: [[Design/Game Design Document]] · [[Design/Decisions Log]] · [[Design/Core Loop Review]] · [[Development/Roadmap]] · [[Current Status]]

---
title: Workshop Growth
status: direction confirmed — balance and implementation details open
type: design
date: 2026-10-19
updated: 2026-10-19
tags: [design, employees, delivery, weather, camera, create-swords]
---

# Workshop Growth

Organized from Allen's [[Random thoughts]] and follow-up answers on 2026-10-19. The [[Design/Game Design Document]] owns intended behavior, [[Development/Roadmap]] the work list, and [[Current Status]] implementation status. These are design additions, not features verified in Studio.

Original wording: [[Archive/Design/Random thoughts before growth alignment — 2026-10-19]]. Reference-game prices, timers, and capacities are observations from Allen's notes, not selected balance values for Sell Swords!.

## Employees and workstations

### Confirmed direction

- Buy additional anvils so hired smiths have places to work. Employee production uses workshop space and station capacity.
- Provide an employee management/upgrade window for hiring more workers and comparing workers with different speeds and quality capabilities.
- Workers have levels and progress through completed work. Better hires and training improve relevant capability; exact curves and thresholds remain untuned.
- **Five employee roles confirmed:** furnace operator, smith, finisher, stocker, and cashier. The finisher combines hilt assembly and optional polishing; there is no separate hilter or polisher profession.
- A smith leaves an un-hilted blade on the **bare-blade rack**. The finisher takes that blade, attaches the selected fittings, and optionally polishes the completed sword to its worker ceiling. If the player wants to etch, the finisher pauses after assembly and polishing resumes after etching.
- A separate **finished-sword rack** holds swords ready for the retail handoff. The stocker visibly carries eligible swords from it into empty shop holders.
- Starter smiths produce blades below 90% and train toward the 90% forging ceiling. Player forging still reaches 90% after completing its guided sequence.
- The finisher's speed and polishing ceiling improve through training. Exact values remain untuned; hilt assembly does not gain a new quality minigame from combining the roles.
- **The player can improve both stages:** return a sub-90% un-hilted employee blade to the anvil and finish forging to 90%; after assembly and optional etching, continue beyond an employee's polishing ceiling at the Polishing Station, up to 100%. Polishing does not substitute for unfinished forging.
- Retain the existing cashier role and its configurable offer threshold.

| Role | Responsibility | Progression direction |
|---|---|---|
| Furnace operator | Load, heat, and collect ingots | Handling/heating speed; values untuned |
| Smith | Forge and deposit bare blades | Speed and forging capability toward 90% |
| Finisher | Fit selected hilts; optionally polish after any chosen etch | Speed and polishing ceiling |
| Stocker | Carry ready-for-sale swords from the finished rack to empty holders | Stocking speed initially |
| Cashier | Handle offers using the player's acceptance threshold | Exact progression remains open |

Five means five professions, not a five-worker population cap. Multiple workers may share a role, subject to future station/capacity limits. No ore attendant or automated etcher is selected; the courier remains part of delivery rather than a sixth employee-management role.

### Production handoff

```text
Cold ingot → furnace operator / player → hot ingot
    → smith on an available anvil → un-hilted blade rack
    → optional player forging completion to 90%
    → finisher / player fits hilt → complete sword
    → optional player etching → optional final polishing by finisher / player
    → ready-for-sale finished-sword rack → stocker → shop holders → cashier

Swords reserved for direct commissions or courier deliveries bypass retail stocking.
```

Both bare-blade and finished-sword racks are now selected. Storage for hot ingots and intermediate swords awaiting etching/polishing remains open. The stocker only takes swords marked ready for sale; it preserves commission/delivery reservations and further-finishing work, and waits when holders are full or no eligible stock is ready. The stocker does not negotiate prices. Highest-value/oldest-stock/type priorities are later options, not selected initial rules. Automated etching and offline business simulation are not approved by this employee-roster decision; the new offline-earnings thought remains in [[Random thoughts]].

### Details still to design

- Starting forging quality, work/XP thresholds, maximum level, speed curves, hiring prices, and the relationship between hire tier and training.
- Polishing ceilings and representation of polish progress on sub-90% employee blades. The current implementation's 90–100% refinement model needs a deliberate extension.
- Assignment, dedicated versus shared stations, player/worker priority, queues, and behavior when inputs run out or the rack is full.
- Allowed materials/blueprints and material reservations before workers can consume valuable inputs.
- Whether trained finishers can reach 100%, the employee unlock stage, and whether wages exist. No wages or premium-currency hiring requirement was chosen.

## Optional remote delivery orders

### Confirmed direction

Add a **separate delivery board/station with a village courier or cart**. Existing in-person and letter commissions retain direct picker hand-in and agreed rewards. The first Iron Wakizashi teaching commission stays a direct commission.

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

Recommended presentation: smoothly fade or hide the current building's roof locally for the viewing player and restore it outside. Retain walls and exterior identity. Exact opacity, transition time, detection bounds, eaves, and station-camera handling remain tuning decisions. No shared-world roof removal or collision change is required.

## Clarification resolved

Allen approved combining hilting and polishing as the **finisher**, with the **stocker** filling the fifth profession. This supersedes the separate-hilter / undecided-polisher wording in the earlier organization record. Balance values and operational details above remain open.

Related: [[Design/Game Design Document]] · [[Design/Decisions Log]] · [[Design/Core Loop Review]] · [[Development/Roadmap]] · [[Current Status]]

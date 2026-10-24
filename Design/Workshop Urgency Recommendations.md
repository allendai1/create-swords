---
title: Workshop Urgency Recommendations
type: design
status: combined recommendations — stage 1 implemented and played 2026-10-23 (Sessions/2026-10-23#Urgency phase 1); stage 2 partly built 2026-10-23, not played (Sessions/2026-10-23#Urgency phase 2); stages 3–4 not started
updated: 2026-10-23
tags: [design, urgency, psychology, employees, create-swords]
---

# Workshop Urgency Recommendations

Combined recommendations from [[Building urgency in the game]], Claude's [[Design/Urgency Review]], and the latest recorded decisions in [[Sessions/2026-10-23#More refinements]]. Saved from the follow-up discussion with Allen. This is the starting brief for work on urgency; the two source analyses remain background. Recommendations are not a record of implemented or approved gameplay changes.

**Direction:** make the existing business easy to understand and rewarding to manage, then add VIP buyers and occasional rushes. Players should understand the next useful job, have time to finish their current craft, and earn employees that genuinely change their responsibilities.

## 1. Make the workshop communicate

Add a furnace-ready ding and glow, customer arrival/offer cues, sale feedback, and a distinct cart-return cue. Keep sounds short, quiet and tied to meaningful state changes, with visual equivalents when sound is off. Avoid a separate alert for every routine employee movement.

The crew window should explain why a stopped crafter is waiting: no ingots, equipment occupied, or output storage full. Preserve Allen's decision against worker speech bubbles. Show actual state; silence alone cannot reliably distinguish a supply problem from walking between stations.

**Success:** players notice a useful next job without repeatedly checking every station or menu. Multiple simultaneous completions remain understandable rather than noisy.

## 2. Give customers enough patience

Start by testing regular offers at **45 seconds**, retaining nearby price inspection and negotiation. Pair the window with a subtle cue. Keep crafts untimed.

Measure whether players can finish a normal station interaction and walk to the customer. If offers still regularly force them to abandon crafting, tune the duration or when the response window begins. Forty-five seconds is a starting value, not a proven answer. The reference recording's 60 seconds applies to that observed tutorial offer, not necessarily every Pottery customer.

Missed income can feel frustrating even when owned items are safe. Judge the experience by whether players feel able to manage it.

## 3. Make the first employee create freedom

Recommend having Furnace 2 before the first crafter begins working. Make station reservations predictable: the current employee claims stations while walking toward them as well as while using them. A second furnace increases access, but does not guarantee ready material or remove competition at the polishing station.

Explain the complete cost of a functioning employee, including required equipment and training. Preserve already-owned workers and progress when changing purchase prerequisites; avoid locking existing players out of their purchased employee.

Tune input and output buffers so the player can finish a personal sword between tending visits. Add a deliberate way to protect special materials from employee consumption, with its exact interaction and persistence designed before implementation.

**Success:** the player makes a chosen sword while routine production advances, and the hire noticeably reduces their workload.

## 4. Make VIP buyers the next major feature

A distinctive arrival, one readable preference and a worthwhile matching premium give the physical shop a reason to hold interesting stock. Preferences might include a polished sword, an etched blade or a particular shape. Introduce the first VIP with a preference matching something the player already has; later visits can reward preparation.

Provide a way to reserve a sword for a special buyer, protecting it from ordinary selling and future automatic stocking. Keep requests in Mail: VIPs are retail customers, not a return to the removed request visitors or board.

Serve VIPs personally initially. Leave permanent exclusion from cashier service open until later play shows whether it remains enjoyable. Arrival frequency, reputation unlock, premiums, bonus currencies and patience require tuning; Claude's suggested figures are starting proposals, not selected values.

## 5. Let hires change the player's role

Default next-hire order: **stocker → cashier → later ore attendant**. Bring the cashier forward if offers interrupt players more than carrying swords does. Keep one active crafter under the latest decision; assess output handling and demand before proposing additional active crafters.

Let the player pin one upgrade, showing remaining cost and what it changes. Include prerequisite equipment and training in the path to a working hire.

Develop new sword shapes and worthwhile personal projects alongside automation. Fully delegated production still needs interesting player choices. The intended progression is from making everything, to supplying and allocating production, to managing a larger shop while personally pursuing new designs and special work.

## 6. Give each selling route its own job

The latest recorded cart behavior supersedes the earlier 1.1× figure in the first analysis: **0.8× packed value**, capacity **6 / 9 / 12 / 15**, and Bulk Orders accepting any sword. Confirm the live state before changing it.

| Route | Reason to choose it |
|---|---|
| Shop | Better returns through customer attention and matching preferences |
| Mail | A specific crafting objective and its rewards |
| Bulk delivery | Conveniently clear accumulated stock for a predictable payout |

Compare rewards and attention required, including gems, reputation, waiting, travel and inventory committed. Keep bulk useful for surplus; VIPs should reward selective retail without making ordinary customers irrelevant.

## Later opportunities

Test a sunny traffic rush once players can maintain stock and benefit from extra demand. Twice the arrivals does not imply twice the sales when production limits supply. Respect the first-sale tutorial and the selected positive-only weather direction. A timed server-wide event revisits the GDD's deferred village-event scope.

Defer lucky hours until storage and surplus handling support repeated rolling. Defer repeated empty-shop walkouts: they may become reminders of a shortage the player cannot yet fix. Neither is necessary to establish the first satisfying business rhythm.

## Suggested implementation stages

1. **First phase: communication and customer timing.** Inspect the live game, add the relevant sound/visual cues and useful crew status, and test 45-second offers. Teach loading the next ingot before working on the current sword once the basic loop is understood. Check crafter/player station competition during the same Play session. *Implemented and played 2026-10-23: [[Sessions/2026-10-23#Urgency phase 1: cues, crew status, 45 s offers]]. Finding for stage 2: your ready ingot left in a furnace is what blocks the crafter most.*
2. **Employee access and stock control.** Resolve furnace prerequisites without harming existing progress, then material/sword reservations and buffer tuning. Select the next employee from observed friction. *Built 2026-10-23, not played: [[Sessions/2026-10-23#Urgency phase 2: the crafter's furnace and your forgotten ingot]] (Anvil 2 after the Ingot Rack, Furnace 2 and the Finished Sword Rack; the crafter takes your forgotten ready ingot out into your hands). Left open: protecting special metals (needs a design), buffer tuning after play; next hire: the stocker.*
3. **Distinctive customers and progression.** Introduce VIPs and the chosen next hire, with a pinned improvement and personal sword goals.
4. **Optional events.** Test a sunny rush only after production and retail can use it; revisit luck events later.

The first phase is deliberately bounded. This sequencing is a recommended handoff, not a claim that Allen separately approved every detail. Later stages contain choices that should be made using the first phase's evidence.

## Verification and handoff

Before implementing, read [[Current Status]], [[Design/Decisions Log]], [[Development/Code Map]] and the latest session changes, then inspect the live Studio scripts and GUI. Gameplay source is recorded as living in Studio; vault build notes alone are not runtime proof. Preserve current unrelated work.

Play the manual loop and the crafter loop. Observe missed offers during station use, notification clarity, worker waiting reasons, shared-equipment access, and whether players know their next useful action. Check touch presentation and sound disabled where tooling permits. Separate completed Edit checks from actual Play/device evidence.

**First milestone:** a player notices a ready ingot, finishes their current sword, serves a customer, collects employee output and can explain the next upgrade they want.

Update the owning design/build notes and session record for changes actually implemented. Report what changed, what was verified, and any remaining decisions or unrun checks. Publishing is separate from implementation.

Related: [[Design/Game Design Document]] · [[Design/Workshop Growth]] · [[Design/Alignment Review — 2026-10-23]]

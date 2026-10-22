---
title: Core Loop Review
status: engagement review — refinements proposed; player evidence pending
type: design
updated: 2026-10-22
tags: [design, onboarding, gameplay, create-swords]
---

# Core Loop Review

The player-facing loop is **get metal → make a sword → sell it → improve the shop**. This note owns the experience review and playtest questions; [[Design/Game Design Document]] owns confirmed rules, [[Current Status]] build status, and [[Development/Roadmap]] remaining tasks. The older review, including superseded 90% forging and station-order advice, is preserved in [[Archive/Design/Core Loop Review before cleanup — 2026-10-22]].

**Engagement review, 2026-10-22:** requested by Allen after the vault cleanup. The refinements below are proposals, not approved changes to the GDD or implemented features. Assessment uses the current design, upgrade catalogue and saved build records; no live Studio inspection, new-player observations, funnel data or retention dashboard was available for this review. Risks are hypotheses, not measured causes of churn.

## Confirmed first-session sequence

| Moment | Intended experience | Recorded status |
|---|---|---|
| Join | Spawn at the owned workshop; start with tantō and a clear first-craft objective. | Plot assignment built; guided starting progression pending. |
| Roll and heat | Pull the loot-box lever, collect ore, heat it; collect before rolling again. | Built; latest combined Play pass pending. First heat is 3 s until the first sword is finished, then 10 s. |
| Forge | Untimed guided strikes visibly shape the universal blank into the selected sword. All strikes give 100% player quality. | Built; rhythm, framing and repeated enjoyment need testing. |
| Assemble | Choose tradition-appropriate fittings and seat them with three untimed knocks. | Knock flow built; fitting progression needs reconciliation/tuning. |
| Optional finishing | Polish adds +10% value; etching adds +15%. Recommended route is hilt → polish → etch; the recorded build also permits polishing an etched sword. | Stations built; clarity, sheen and value per minute need testing. |
| First sale | No visitor before listing; listing brings a customer with an exact-value fair offer. | Built, not freshly playtested. |
| Next goal | First shop sale introduces an Iron Wakizashi commission (minimum 90%), supplying its blueprint. Hand in through a sword picker for the agreed reward. | Commission system pending. No guaranteed Iron roll or odds change approved. |
| First upgrade | After commission delivery, direct the player to Ore Slot 2 and tune its cost against earnings. | Purchase exists; tutorial direction pending. |
| Further learning | Second ordinary shop sale teaches haggling; a later local commission introduces katana. | Haggling hint/first raise built; katana teaching commission pending. |

Explicit item pickers are confirmed even with one valid item. Improve their clarity and responsiveness; do not bypass them. Courier deliveries remain separate from direct commission hand-in.

## Experience risks to test

- **Repetition:** untimed circles are accessible, but visible transformation, hammer feedback and meaningful goals must carry repeated crafting. Test the fifth sword as well as the first.
- **Transfers and menus:** walking, collecting and repeated selections can outweigh shaping. Measure each separately before changing the interaction flow.
- **Optional polish:** the +10% bonus should reward extra care without making players feel every sword requires polishing. Compare enjoyment and coins per minute.
- **Offers during crafting:** check that offer cards, timeouts and tutorial messages do not make station interactions frustrating.
- **Next-goal clarity:** after the first sale, a commission and then a useful upgrade should explain why to continue.

## First playtest questions

Use a small initial group, for example 3–5 new players across desktop and touch, to find obvious problems. Proposed first-sale target: roughly 3–5 minutes; this is a playtest target, not measured performance or a new approved timer.

**Reference-video update:** [[Design/Pottery Tutorial Review]] observes shaping at about 0:10 and a first sale at about 1:12 in the supplied pottery recording. That challenges the earlier 3–5-minute planning target: test a compact first-sword route around 1–2 minutes while preserving satisfying crafting. The recording starts in-world and is one session, so its timing is neither join-to-sale evidence nor a typical-player benchmark. The older target below remains visible as the proposal being reconsidered, not a requirement.

- Can they begin without verbal coaching and identify the next station?
- How long until the first hammer hit, complete sword and sale? Separate waiting, walking, selecting and crafting time.
- Can they make a second sword without help? After several swords, what do they enjoy or try to skip?
- Do they understand 100% forging and the separate optional polish bonus?
- Can they explain their next goal and why an upgrade is useful?
- Are mobile targets, full-blade cameras, roof cutaways and inventory controls readable?
- Once implemented, are direct commissions, courier orders and ordinary shop sales clearly distinct?
- Once implemented, can players understand employee handoffs and preserve swords reserved for further work?

No new mandatory minigame is required to answer these questions. Employee quality/recovery rules must be reconciled with current 100% player forging before the older 90%-cap design is implemented.

## Assessment: where engagement currently comes from

The crafting loop has three useful sources of interest: material surprise, visible transformation from blank to blade, and ownership of a growing shop. Untimed forging and safe polishing fit the cozy premise. Preserve those strengths.

The weak connection is **sale → reason to make another sword**. Much of the intended purpose—teaching commissions, familiar customers, collection progress, reputation and special visitors—is still unbuilt. Repeating the production sequence currently offers more coins and different materials, but the next craft may ask little new of the player.

| Timescale | Player question | Current support | Most important gap |
|---|---|---|---|
| A sword | What am I making, and why? | Material reveal, shaping, fitting, sale | A visible purpose or customer need before repeating production |
| A session | What changes because I made these swords? | Purchased capacity, displays and shop expansion | Tutorial follow-through, purposeful unlocks and evidence that upgrades help |
| A return visit | What am I looking forward to continuing? | Planned collections, relationships, commissions | Persistent progress and a clearly remembered next project |

This follows Roblox's distinction between repeated actions and the progression system that changes future play. The game-specific diagnosis above is an inference from the vault. [Roblox: Core loops](https://create.roblox.com/docs/production/game-design/core-loops)

## Proposed refinement 1: lead the next craft with a purpose

After the first sale, use the already-planned teaching commission to make the next sword feel different. Later, let players choose a customer request or personal collection goal, or simply continue ordinary shop production. Show one pinned goal with its next action and reward.

Proposed repeat loop:

```text
Choose a request, collection goal or shop-stock plan
    → use available metal / roll for more
    → choose blueprint and fittings for that purpose
    → forge and assemble
    → choose any useful or desired finishing
    → sell or hand in
    → see customer, collection and workshop progress
    → choose the next project
```

The first craft still begins with the player's own tantō, with no waiting customer. Open the commission after its sale, as already agreed. After the teaching sequence, offer a small choice of achievable goals instead of prescribing every sword.

Examples to explore: a local guard requesting a familiar blade, a collector interested in a particular finish, and a new blueprint that visibly changes the forging transformation. Give customers recognizable preferences and brief reactions tied to the delivered sword. Flexible preferences should affect worthwhile choices; a universal highest-bonus fitting on every sword would weaken them.

**Hypothesis:** a specific next project increases the proportion of first-sale players who voluntarily start and complete another sword. Watch whether the objective is understood and whether players still feel free to make their own designs.

## Proposed refinement 2: remove randomness from the teaching bottleneck

The first commission requires Iron, but the current direction explicitly approves neither a guaranteed Iron roll nor supplied material. The documented 60% Common probability is not an Iron probability; it includes multiple materials. The first teaching commission can therefore require an unpredictable number of rolls before the player can use the new blueprint.

This interacts with the built rules in [[Art/Ore Loot Box]]: all ore must be collected before rerolling, only six ingots can be carried, and the lever remains off with ore on the lid. The Ingot Rack is behind Ore Slot 2 in the purchase chain, while the tutorial points players toward Ore Slot 2 only after the commission. Buying it early may be possible, but it is a confusing escape from a lesson that is supposed to teach a new sword.

**Recommended proposal:** the teaching customer supplies one Iron ingot with the wakizashi blueprint. Grant it once for that commission and preserve its state through reconnects; make the learning path recoverable if the player uses the supplied metal elsewhere. Keep the ordinary roller's odds and full material roster unchanged.

Alternative if supplied material is undesirable: accept any-material wakizashi for the teaching step, then introduce specific-material requests later. That changes the agreed Iron requirement more substantially, so supplied Iron is the narrower recommendation.

This would explicitly revise the earlier decision about tutorial material access. Later optional requests may involve material hunting, with alternative goals available while the player waits for a desired roll.

## Proposed refinement 3: upgrades should improve a felt limitation

More ore slots increase results per pull, not automatically swords sold per minute. Six results can amplify inventory work while the player still has one manually operated anvil. A second furnace also has limited benefit if heating already finishes while the player forges the previous ingot. These are throughput risks to measure, not proof that either upgrade is bad.

- Teach batching after the basic craft: load the next ingot before working on the current sword, where the existing interaction supports it.
- Present Ore Slot 2 as more material choice and less repeated rolling. Demonstrate its two-result reveal immediately after purchase.
- Make storage reachable before larger ore batches regularly fill the player's hands. A clear collect-to-owned-storage action could preserve the collect-before-reroll rule with fewer transfers.
- Provide an explicit way to clear unwanted common stock when hands and storage are full. A low-value exchange/sell-back or discard action needs economy and accidental-loss review; avoid creating a more profitable roll-and-resell loop than crafting.
- Recommend additional displays when players actually have unsold stock, and extra furnaces when heat is delaying work. Track use after purchase, rather than treating the purchase itself as proof of value.

Keep the currently agreed first upgrade after the teaching commission, but test that buying it changes the next few minutes in a way a new player can explain.

## Proposed refinement 4: make optional care a real choice

Polishing requires active work for a documented +10% finish bonus; etching supplies +15% with an automatic show. It is plausible that polishing will be skipped for efficiency while etching becomes a routine extra stop. Neither outcome has been measured.

The value formula also makes finish bonuses additive. For the same sword/customer, a +40% hilt and +15% etch give a finish factor of 1.55. Adding 0.10 polish raises it to 1.65, only **about 6.45% more total value**, if the live code matches the documented formula. A fixed bonus label should not obscure the actual coin difference.

Recommended changes to test:

- Show the sword's actual before/after coin value and visible finish difference.
- Give polishing a compact, satisfying action with safe partial progress; determine its duration from player enjoyment and measured opportunity cost.
- Let selected optional customer requests reward care explicitly, while ordinary unpolished sales remain viable.
- Give etch patterns expressive/customer relevance rather than treating every pattern as an interchangeable compulsory price buff.
- Once the novelty has worn off, check the repeated etching show and station transitions for unnecessary waiting. Preserve the admired result even if repeat presentation is shortened.

For a production-limited player, a useful first approximation is that added polish time should be compared with its **relative total-value increase**, not just the advertised additive bonus. Include walking/pickers, concurrent heating and customer demand in the real measurement before changing the bonus.

## Proposed refinement 5: preserve the player's accomplishments and next project

Persistence is a prerequisite for evaluating this game's return loop. Save tutorial milestones, commissions, inventory, discoveries, chosen goal and upgrades, and make resuming clear. A returning player should see what they were working toward and be able to continue it quickly.

Use the planned Material Index as permanent recognition of discovery. Consider a small record of the player's first or favourite crafted designs so selling a beautiful sword leaves an accomplishment behind. Show a specific next blueprint, fitting or customer milestone, with progress, rather than only a larger coin target.

An early special visitor can preview the wider sword traditions already in the design. Their request should remain available while the player prepares; return motivation comes from an interesting unfinished project and an improved shop. Keep the session enjoyable and self-contained even when the player does not return on a schedule.

The six plots can support admiring other players' distinctive swords and workshops later. Validate the solo experience first; the loop must still work when neighbouring plots are empty.

## Proposed refinement 6: remove interruptions and preserve active crafting

Test how the recorded 20-second customer offer window behaves while the player is in a station camera. If sales expire during otherwise enjoyable crafting, let offers wait or begin their response window when the player can meaningfully respond, with a bounded queue. This is a proposed behavior change, not a verified bug.

Keep pickers at every item-selection step, as agreed. Within them, clearly identify the relevant workpiece or commission-compatible items while requiring the player's choice. Keep the next station legible after closing a picker or finishing an animation.

Employee progression should gradually hand off repetitive work while leaving desirable player choices and personal commissions. Prototype one useful role after manual production is validated. Implementing all five roles early could automate the very activity the game is trying to prove enjoyable.

## Refined opening to test

The times below are planning targets, not observed completion times or approved timers. Use new-player tests to adjust them.

| Moment | Experience | Payoff |
|---|---|---|
| First minute | One visible objective; roll, collect and heat; reach the anvil promptly | See the signature shaping action, not a tour of every system |
| Roughly first 3–5 minutes | Finish and sell the first tantō with the built fair offer | A finished creation, a customer reaction and a visible reward |
| Immediately afterwards | Customer introduces wakizashi and, under this proposal, supplies its Iron | A new shape and a dependable next purpose |
| First upgrade | Commission reward makes Ore Slot 2 affordable; player pulls it once | A visible change to the workshop and material choice |
| Before ending the first session | Choose a next request or preview the katana milestone; save the goal | A specific project to resume |

Avoid exposing polishing, etching, employees, courier orders and every currency during the first sword. Offer optional depth after the basic transformation and sale have paid off. This is consistent with Roblox's guidance to teach essentials, reach enjoyable play quickly and show future goals. [Roblox: Onboarding](https://create.roblox.com/docs/production/game-design/onboarding)

## Priority and validation

| Order | Work | Why now |
|---|---|---|
| 1 | Validate the current loop and save/rejoin reliability | Broken interactions and erased progress undermine every retention experiment |
| 2 | Complete the guided opening and dependable teaching commission | Gives first-sale players a clear, achievable second craft |
| 3 | Test Ore Slot 2, storage pressure and the benefit of early purchases | Ensures progression improves play rather than increasing handling |
| 4 | Add a small set of purposeful requests and persistent discovery/milestone feedback | Tests variety and return motivation using existing swords and stations |
| 5 | Tune finishing choices and interruptions | Improves the repeated loop after its purpose is established |
| 6 | Expand workers, deliveries and longer progression based on observed needs | Avoids building large systems before knowing which repetition players want help with |

Instrument the sequence **join → first roll → first hammer hit → assembled sword → first sale → teaching commission accepted → teaching commission delivered → first upgrade**. Also record voluntary next-sword completion, goal selection and progression on return. Separate desktop/touch, build version and acquisition cohorts; distinguish required tutorial repeats from voluntary crafting.

Start with observed sessions from 3–5 new players, allowing several swords each. Record time spent shaping versus walking, menus, waiting and blocked inventory. This finds usability problems; it does not estimate population retention or prove a causal improvement.

**First focused experiment, once commissions and saving are stable:** compare the same teaching commission with ordinary material access versus one supplied Iron ingot. Primary metric: commission delivery per eligible first-sale player. Counter-metrics: confusion, inventory blockage, repeat-grant abuse, ordinary crafting after delivery and progression/economy distortion. Track D1 return as a downstream outcome. Keep rewards, blueprint and other onboarding changes constant during this comparison.

Collect a baseline before choosing the minimum worthwhile improvement, sample size and run duration; preregister those and a decision rule before comparing variants. Adopt a variant only when the primary improvement is supported without material counter-metric regressions. If traffic is too small, report qualitative findings and uncertainty rather than a percentage uplift.

Track **D1 and D7 return by first-join cohort**, plus whether returning players continue a meaningful goal. Longer sessions alone can reflect waiting or confusion, so assess progress and player feedback alongside time. Roblox likewise connects D1 with the core loop, onboarding and performance, and D7 with progression. [Roblox: Retention](https://create.roblox.com/docs/production/analytics/retention)

---
title: Technical Debt and Deferred Features
type: development
status: notes audit — live verification pending
updated: 2026-10-24
tags: [backlog, technical-debt, create-swords]
---

# Technical Debt and Deferred Features

Review of project notes through **2026-10-24**, requested by Allen after organizing [[refinement4]]. This is a consolidated discovery list, not a new implementation plan or approval of every idea. Gameplay scripts live in Studio; no live script inspection or playtest was performed for this review. “Recorded” below means supported by the notes, not freshly reproduced.

## Technical debt worth addressing

| Item | What remains and why it matters | Evidence |
|---|---|---|
| **Builders do not reproduce the current place** | Newer station spacing, delivery-door changes, display tables, Finished Sword Rack 2, rack dimensions, Etching Table 2, cashier counter and several pads are hand edits. Rerunning older builder sections can undo them. The roadmap also flags the Genshin-style rollout and removed vegetation as needing reconciliation with builders. | [[Development/Roadmap#1. Validate the current combined build]], [[Development/Roadmap#2. Complete the first-session journey]], [[Sessions/2026-10-24#Backups and hand edits]] |
| **Known failing tests and missing coverage** | Latest recorded results: SwordMeshSpec **218/236**, EtchingSpec **35/36**, attributed to unbaked Zanbatō shapes and the removed demo tray. Resolve missing assets and stale expectations. Studio's BladeGolden still covers only Japanese starter blades, leaving western blades and Zanbatō outside the JS/Luau comparison. SaveSpec was 85/85; that does not close these other gaps. | [[Sessions/2026-10-24#Checked in Edit]], [[Sessions/2026-10-23#Big swords: findings and open risks]] |
| **Whole-rack redraws** | Crafter, Stocker and Etcher rack changes redraw every sword. Etched swords make this more expensive. Investigate updating only changed slots and cache lifetime before more automation increases the frequency. The older claim that all world etches build in one frame is partly superseded by later spreading work. | [[Sessions/2026-10-24#Not done / known]], [[Sessions/2026-10-23#Etchings that pop (strong glow)]] |
| **Etch memory and remaining frame spikes** | Older audit calls for allocating EditableImage before painting, releasing finished pixel buffers (~2 MB each), and avoiding a synchronous etch rebuild when saving across a polish level. Recheck these in current code. The picker now spreads work, but its last recorded measurement still had a 58 ms frame in Edit. Low-memory device measurements remain open. | [[Development/Roadmap#1. Validate the current combined build]], [[Sessions/2026-10-23#Etching Table window no longer freezes]] |
| **Incomplete gamepad controls** | Polishing has no recorded gamepad implementation; consistent station exit/confirm/save behavior is unfinished. The shaping experiment also lacks gamepad support and has not been tested on touch hardware. | [[Refinement#Found 2026-10-23 (code and place audit, not played)]], [[Prototypes/sword-shaping/README.md#Known limits]] |
| **Older server-hardening findings need a fresh check** | Audit items 34–35 report missing plot/distance validation on some crafting/order calls and missing rate limits on three read calls. Item 10 reports a newer-version save rejection leaving its session lock held. No explicit closure was found in the reviewed records; inspect current scripts before treating these as current bugs. | [[Refinement#Found 2026-10-23 (code and place audit, not played)]] |
| **Automation lacks explicit item reservations** | Cheapest-first ore selection does not guarantee rare metals stay reserved. Commission/delivery sword reservations are not recorded for the Stocker; leaving un-etched swords for the Etcher is implemented. Define protection rules before adding the ore attendant or more automated output. | [[Development/Roadmap#5. Employees and production]], [[Design/Workshop Urgency Recommendations]], [[Sessions/2026-10-23#Urgency phase 2: the crafter's furnace and your forgotten ingot]] |
| **Rendering and asset cleanup** | Rainbow's colour sweep fits the katana but not shorter/longer blades. Etch strip seams and detailed hilt geometry remain roadmap items. Unused rainbow/book uploads and a Zanbatō preview are recorded; verify references before cleanup. | [[Sessions/2026-10-24#Not done / known]], [[Development/Roadmap#4. Crafting, economy and customer progression]], [[Sessions/2026-10-23#Big Sword Stand]] |
| **Cashier behavior is a shortcut** | The cashier answers every waiting customer at once, turning to each. Employee prices and perks are placeholders. Decide whether sequential service is wanted; the collect-cash behavior is already a new request in Refinement 4. | [[Sessions/2026-10-24#Not done / known]], [[refinement4]] |
| **Verification backlog** | Most recent employees, merge/reroll, delivery packing and associated interactions have Edit evidence only. Still open: a complete current-build loop, save/rejoin and shutdown, two-player ownership, south lots, 20+ visible swords, published/mobile memory and input checks. Keep these distinct from unbuilt features. | [[Sessions/2026-10-24#Checked in Edit]], [[Development/Roadmap#1. Validate the current combined build]], [[Development/Roadmap#3. Persistent progress]] |

## Partially built features

### Zanbatō / big swords

The blueprint and Big Sword Stand exist, but the sword is currently obtained through the Dev panel. Remaining work recorded:

- Blueprint purchase pad and price, an original hilt, and a two-handed hold/appropriate slash behavior.
- Baked meshes; training price and a deliberate crafter rule.
- Check rack and Stocker compatibility, and stop the tutorial guide pointing at an incompatible big-sword stand.
- Buyer behavior and customer offers tested in Play. The notes mention a buyer still to do; do not assume a special-buyer design is already settled.

Sources: [[Development/Roadmap#2. Complete the first-session journey]], [[Sessions/2026-10-23#Big Sword Stand]], [[Sessions/2026-10-23#Big swords: findings and open risks]].

### Sword-shaping experiment

Built and exercised with mouse/keyboard, but not adopted as the normal crafting loop. Touch testing, gamepad, curve shaping and its relationship to quality/value and the crafter remain open. A gentler finishing strike was considered. [[refinement4]] now adds smoothing near the target outline; these belong in the same experiment.

Sources: [[Prototypes/sword-shaping/README.md]], [[Development/Roadmap#4. Crafting, economy and customer progression]].

### Sound, feedback and sword value

The anvil clang and four urgency cues exist, but music and fuller station audio remain unfinished. Crafting-completion effects, camera blends, a stronger rare-roll reveal, and a per-factor sword-value breakdown remain recorded opportunities. Older refinement entries are suggestions, not blanket implementation approval.

Sources: [[Current Status#Missing systems]], [[Refinement#Found 2026-10-23 (code and place audit, not played)]], [[Development/Roadmap#4. Crafting, economy and customer progression]].

## Features and ideas put aside

| Feature | Recorded status / remaining decision | Source |
|---|---|---|
| **Ore attendant** | Selected for later: operate the roller and collect using its existing odds. Unlock, storage, reservations and full-storage rules are undecided. | [[Design/Workshop Growth#Wealth and staged automation (confirmed 2026-10-22)]] |
| **Capped offline workshop earnings** | Confirmed later direction, after online automation is balanced. Cap, rate, unlock and material consumption remain open. Separate from already-built offline delivery timing. | [[Design/Workshop Growth#Later capped offline earnings (confirmed 2026-10-22)]] |
| **Manual etching** | Explicitly parked. Proposed interaction: trace a guide with mouse/finger, with an automatic option and no accuracy score. That interaction remains a proposal. | [[Random thoughts#Ideas still to resolve]], [[Design/Decisions Log]] |
| **Fixed-wheel grinder polishing** | Backlogged prototype: move the sword against the wheel and compare it with current optional polishing. No replacement has been selected. | [[Development/Roadmap#4. Crafting, economy and customer progression]] |
| **VIPs, customer tastes and personal stories** | Special arrivals, meaningful preferences, familiarity and personal commission chains remain missing. Ordinary Mail requests already exist. VIP prices, frequency and cashier participation still need decisions. | [[Design/Workshop Urgency Recommendations]], [[Current Status#Missing systems]] |
| **Bare-blade rack and player/worker handoffs** | Earlier selected direction, but requires reconciliation with the current all-in-one crafter. Do not blindly restore the old separate smith/finisher staffing plan. | [[Design/Workshop Growth#Employees and workstations]], [[Development/Roadmap#5. Employees and production]] |
| **Weather traffic bonuses / sunny rushes** | Positive-only weather traffic is selected design. Timed rushes are a proposal; village-wide events remain deferred. | [[Development/Roadmap#6. Deliveries and weather]], [[Design/Workshop Urgency Recommendations#Later opportunities]] |
| **Lucky hours and empty-shop walkouts** | Explicitly deferred recommendations until stock handling and production support them. | [[Design/Workshop Urgency Recommendations#Later opportunities]] |
| **Pin an upgrade / reserve a sword / scrap unwanted ingots** | Suggestions scattered across urgency and economy reviews; no implementation record found. Item reservations overlap the automation debt above. | [[Design/Workshop Urgency Recommendations]], [[Design/Alignment Review — 2026-10-23]] |
| **Longer progression and gem uses** | Further shapes, milestone visitors, storage/facility tiers and lasting gem uses need design/tuning. Do not reuse the old economy review's exact income estimates after the newer swords and employees. | [[Development/Roadmap#4. Crafting, economy and customer progression]], [[Design/Alignment Review — 2026-10-23]] |
| **Robux shop, badges and economy analytics** | Shop shell exists but has no products. Only onboarding analytics is recorded. Monetization choices still need alignment with actual progression. | [[Current Status#Missing systems]] |
| **Environment/art choices** | Trees were removed pending a chosen style; earth versus stone street remains an inbox choice; AnvilV2 adoption is undecided. Old map layouts and the mine are retired alternatives, not automatically work to resume. | [[Random thoughts]], [[Development/Roadmap#2. Complete the first-session journey]], [[Development/Roadmap#7. Presentation and release]] |

## Stale entries to avoid reopening as missing work

- **Already built:** per-shape paid crafter training and 70%→100% quality progression; Stocker, Cashier, Promoter and Etcher; western swords; mail requests; delivery sword selection; additional finished-sword storage; repeatable ore-slot merging.
- **Etching-picker freeze:** a later fix spreads and queues card image builds. Verify runtime performance instead of implementing the old fix again.
- **Crafter at the wrong furnace:** later station-specific heating and a recorded Furnace 2 play check supersede the old finding.
- **Old cart's 3-second return bug:** the old motion was replaced with the clock-driven courier. Test the current dispatch/return path; do not assume the obsolete implementation survives.
- **Gem/book windows over a picker:** the later HUD-hiding system changes this path. Reproduce before carrying the older bug forward.
- **Formula conflict:** the roadmap's older completion-VFX brief says polishing is additive; later economy records make full polish multiply the whole value by 1.10. Any value presentation must follow the newer rule.
- **Document maintenance itself is debt:** Current Status/Home still introduce the records as reconciled through October 22 despite later additions. Some roadmap checkboxes combine implemented work with remaining tuning, and older rack sizes, role plans and delivery payouts appear beside newer values.

Sources: [[Sessions/2026-10-23]], [[Sessions/2026-10-24]], [[Development/Roadmap]], [[Current Status]], [[Home]]. Historical source notes have been preserved.

## Suggested order to revisit

1. Address the current player-observed bugs in [[refinement4]] and run the combined loop, automation and save/rejoin checks.
2. Recheck the older save-lock/server findings; reconcile builders and restore meaningful passing test coverage.
3. Measure and address rack/etch rendering cost and finish input support.
4. Complete Zanbatō and decide the shaping/smoothing experiment.
5. Choose the next expansion from the deferred-feature list, with reservations and online balance resolved before deeper automation/offline income.

This ordering is a recommendation from the review, not a newly approved development sequence.

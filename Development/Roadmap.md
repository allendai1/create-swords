---
title: Roadmap
status: active — remaining work only
type: development
updated: 2026-10-22
tags: [roadmap, create-swords]
---

# Roadmap

Remaining work reconciled against records through **2026-10-22**. Implementation already recorded as built belongs in [[Current Status]]; unrun Play checks remain open. Historical task lists: [[Archive/Project History/Roadmap before cleanup — 2026-10-22]]. Intended behavior: [[Design/Game Design Document]].

## 1. Validate the current combined build

**Code audit 2026-10-22:** five reviewers checked the scripts against this list and a second reviewer per area tried to refute each finding: 26 confirmed, the high and medium ones fixed ([[Sessions/2026-10-22#Roadmap 1–3: build audit, first-session journey and saving]]). The Play checks below are still open, and these audit findings are not fixed yet:

- [ ] Give polishing a gamepad input (Thumbstick cursor with R2 held, B leaves, Y saves); today only the anvil, pads, offers and hotbar have one.
- [ ] Stroked etches on the Finished Sword Rack rebuild in one frame whenever the rack changes (`SwordMeshCache.release` frees at 0 refs; `SwordRenderer` builds without spreading). Delay the release by a few seconds and spread the build; `SwordMeshSpec`'s "empty after release" checks then need to wait.
- [ ] `EtchCanvas`: create the EditableImage before painting, so a refused one fails fast; drop a finished canvas's pixel buffers (about 2 MB each).
- [ ] Polish save right after crossing a sheen level rebuilds the etch in one frame (`PolishController` stale branch): release it after a short delay instead.
- [x] Set the server size to 6 (was 50; set and read back through Open Cloud on 2026-10-22).

- [ ] Play the complete loop on the current map: roll → collect → heat → forge (100% player quality) → three hilt knocks → optional polish (+10%) → optional etch (+15%) → display → sale. Check all three blade lengths, holder clearance and picker framing.
- [ ] Test the opening: 3 s heat before the first completed sword, 10 s afterwards; no visitors before listing; immediate first customer; fair first offer; second-sale hint and guaranteed first raise; normal negotiation from the third sale.
- [ ] Test the loot box with 1–6 purchased slots: lid/reveal/landing, collect-before-reroll, full hands, observer visibility, wrong-owner collection and workshop movement after upgrading.
- [ ] Test workshop prompts, mounts, cameras and exit positions, Furnace 2/polish/etch pads, roof transitions and the Upgraded Store's 12-stud push, including a character inside the workshop.
- [ ] Test multiple clients on north and south lots: own-plot actions and purchases, customers reaching every display, visitors unable to use stations, empty plots, leaving/reclaiming and respawn. Server size is 6 (set 2026-10-22).
- [ ] Test etch/polish transitions for Flame and Eclipse across materials: sheen changes without hitches, partial/full polish, consistent held/displayed/picker/hotbar art, and etching an already polished sword.
- [ ] Test etch interruption and failure recovery: early close, repeated use, death/respawn, stale/rejected requests, allocation failure, restored controls/camera and no duplicated items/bonuses.
- [ ] Test 20+ visible swords, viewport previews and multiple players with the baked mesh pipeline; check streaming pop-in, EditableImage/live-mesh allocations and cleanup on a published lower-memory/mobile client.
- [ ] Check touch framing and controls, inventory overflow/drag/drop and gamepad navigation. Gamepad hotbar cycling (R1/L1), anvil (R2/B), pads (Y) and offers (Y/L2) were added 2026-10-22 and need a controller test.

## 2. Complete the first-session journey

**Built 2026-10-22** (Claude's defaults in [[Design/Decisions Log]]): tantō-only start with the guide line and arrow, the Guard Captain's Iron Wakizashi request (90%+, 120 coins) with its blueprint, acceptance and picker hand-in at the request board, the guide to Ore Slot 2, the Wandering Swordsman's Katana request (any metal, after the third sale, 300 coins), learned-blueprint and tradition checks, and the onboarding funnel. Remaining:

- [ ] Play-check the opening and both requests, including the picker at every step, rejoining mid-request, a displayed or racked Iron Wakizashi, full hands of other metals, and that the haggling hint still lands on the second shop sale.
- [ ] Tune the rewards (120 / 300), the katana trigger (third sale) and Ore Slot 2's price against real first sessions. Decide on the open proposal to supply the Iron ([[Design/Core Loop Review#Proposed refinement 2: remove randomness from the teaching bottleneck]]).
- [ ] Tune the fitting milestones (0/2/4/7/10/15 swords) and decide Japanese names for the six hilts (they keep the old ladder's names). Western fittings come with the first western blueprint.
- [ ] Run new-player sessions on desktop and touch: record time to first hammer hit/sword/sale, where help is needed, next-goal understanding and enjoyment after several swords. See [[Design/Core Loop Review]]. Published servers also log the onboarding funnel (Creator Dashboard → Analytics → Onboarding funnel; steps in `SmithyCore.FUNNEL`).

## 3. Persistent progress

**Built 2026-10-22:** session-locked saves of everything listed in [[Development/Saving]], the recovery rules there, upgrades reapplied on the new lot, schema version 1 with a migration rule. Checked in Edit: `SaveSpec` 38/38 over an in-memory store, and the lock sequence (wait, take over, refuse the old session, release) against the real Studio DataStore with a throwaway key. Remaining:

- [ ] Play-check leave/rejoin: upgrades and the pushed workshop, displays on the same holders, racks, furnace ingot back hot, ore back as ingots, guide step and blueprints as left, no duplicated or missing items.
- [ ] On a published server: rejoining straight into another server (the lock wait, then the takeover), a server shutdown (BindToClose), and two clients at once.

## 4. Crafting, economy and customer progression

**Confirmed progression direction (2026-10-22):** relaxed crafting → higher-value swords → invest profits in trained familiar production → personally pursue new designs and special commissions. Most upgrades/blueprints are bought; milestone commissions introduce special designs and new traditions. Details: [[Design/Workshop Growth#Wealth and staged automation (confirmed 2026-10-22)]].

- [ ] Map the permanent progression ladder beyond the starter Japanese swords: higher-value shapes, milestone commissions, purchased blueprints, facilities and prestigious customers. Keep earned wealth/workshop progress; no rebirth/prestige reset in the current plan. Existing fantasy materials remain available through starting roller odds; do not add new material-tier gates without a separate decision.

- [ ] Tune hit rhythm, staged/local deformation, blade proportions, full-blade framing and hot-to-steel presentation. Keep the shared starting hit count; tune modest higher-tier effort later.
- [ ] Tune prices, material rewards, fitting milestones and commission requirements. Compare unpolished versus polished coins per minute so polishing remains optional.
- [ ] Finish polishing sound and cursor-following stone feedback; add an etching stylus scratch sound.
- [ ] **Prototype moving the sword against a fixed grinder as an alternative polishing interaction** (backlogged 2026-10-22). Reference: [[References/sword shaping demo.mp4]]. Compare against current polishing before selecting a replacement; this task does not approve replacing anvil forging or adding a mandatory station.
  - Drag the assembled sword against the wheel with assisted alignment, visible contact sparks, removal of the small edge allowance and a brighter finish. Preserve optional polishing and its existing +10% value bonus; prevent overcutting, ruined swords and forced restarts.
  - Support mouse and a broad touch drag area with the contact point clear of the finger; releasing pauses. Start by testing a few passes over roughly 10–15 seconds, treating this as a prototype target rather than approved balance.
  - Compare desktop and touch comprehension, completion time, control frustration, visible improvement and enjoyment across five consecutive swords. Decide whether to adopt, revise or shelve it based on repeated use, not first-impression novelty.
- [ ] **Prototype crafting completion and improvement VFX** (backlogged 2026-10-22). Reference: [[References/sword shaping demo.mp4]]. Check the current build first: anvil sparks/clang/shake, etching contact sparks/glow and ore-box rarity flashes already have implementation records.
  - **First priority — assembled sword:** final hilt knock → fittings settle → restrained flash/expanding ring behind the sword → name and value → return control. Start with roughly half a second; keep the blade readable and ordinary production quick. Reserve stronger celebration for the first sword or first completion of a newly unlocked blueprint.
  - **Second priority — polishing:** tie a modest directional spark stream to actual tool contact in the grinder prototype above; stop emission when contact ends. Emphasize permanent edge/sheen improvement with one brief finishing light sweep. Preserve the earlier removal of the anvil's polish flash.
  - Show the actual before/after value gain at hilt, polish and etch completion. Calculate from the existing additive bonus formula; do not represent the polish bonus as multiplying the current total by 1.10.
  - Lower priority: test a small ember puff on furnace loading and brief warm glow on collection, complementing existing heat feedback.
  - Verify effect timing, cleanup on exit/interruption, blade visibility and mobile performance; judge pacing over repeated crafts. Avoid full-screen streaks, repeated rarity announcements and long stat reveals during routine production.
- [ ] Etching follow-ups. The five more patterns (Tide, Stormroot, Woven Wind, Fracture, Falling Stars) were built on 2026-10-22 and are recorded in [[Art/Animated Blade Etching#Five more patterns (2026-10-22)]]. Still to do:
  - Playtest them at the table and on held, displayed, picker and hotbar swords.
  - Check the pattern picker's build hitch (about 0.4 s for seven cards on a katana in Studio) and the six card images' EditableImage cost on a low-memory client.
  - Remove the faint seam where an etch texture's strips meet: inset the overlay UVs half a texel and re-bake the overlays. Fracture already keeps off it.
  - Evaluate sharing final images across materials if budgets require it.
- [ ] Reduce hilt geometry for many visible swords; retain appearance while checking the current detailed wrap cost.
- [ ] Add the Material Index and discovery feedback, heating-speed/storage/luck progression and further building/station upgrade tiers. Existing ore-slot, furnace, display and shop purchases are already built.
- [ ] Implement stock-aware regular visitors, reputation-gated special arrivals, familiarity, letters and personal commission chains; introduce an early outsider and later sword traditions through commissions.
- [ ] Keep decoration cosmetic and make functional facilities affect business. Check optional enamel/colour and gem-work scope before adding them to progression.

## 5. Employees and production

Confirmed roles and unresolved tuning: [[Design/Workshop Growth#Employees and workstations]].

- [ ] **First employee: sword crafter.** Operates the anvil, polishes and deposits the sword in its rack (Allen, 2026-10-22). Confirm hilt assembly responsibility and input supply, then revise the older smith/finisher split, role count and rack handoffs before implementation. Polishing remains on assembled swords.

- [ ] Add paid training per sword shape after the player's personal first craft of that shape. It permits production in any allowed supplied material, without separate material-combination training. Set training ownership/cost, material permissions, finish choices and production selection; keep shape authorization distinct from worker levels and quality/speed training.
- [ ] Start automation with player-rolled, player-stocked ore; add a later ore attendant upgrade to operate the existing roller and collect results with unchanged material odds. Define unlock, storage/collection, reservations and full-storage behavior before implementing the attendant.

- [ ] Define one-time hiring/training/upgrade costs, unlocks, levels, work/XP thresholds, speed/quality ceilings and worker limits; build the management UI. Employees have no ongoing wages.
- [ ] Add purchasable anvils and a bare-blade rack; define station assignment, player/worker access, queues, material reservations and full-rack behavior. A finished-sword rack already exists.
- [ ] Implement smith quality progression from lower starter output to **100% forging quality when fully trained**, matching the player and superseding the old 90% ceiling. Define starting quality, curve/costs, lower-quality data/appearance/value and player recovery; keep polishing a separate finish bonus with its own worker capability rules.
- [ ] Implement the first sword crafter, then the remaining production roles after reconciling the older furnace-operator/smith/finisher split; include player finishing/etching handoffs.
- [ ] Implement visible stocker transfers of ready-for-sale swords, preserving commission/delivery/further-finishing reservations; wait when there is no eligible stock or display space.
- [ ] Implement cashier offer thresholds and validate the revised employee chain, later ore attendant and player handoffs.
- [ ] **Later, after online automation is balanced:** design and implement capped offline workshop earnings collected on return. Set cap duration, rate, unlock requirements, stock consumption and ore-attendant behavior; account for production capacity and persisted stock without duplicate payouts. Keep courier offline rules separate. See [[Design/Workshop Growth#Later capped offline earnings (confirmed 2026-10-22)]].

## 6. Deliveries and weather

- [ ] Build the separate remote delivery board, requirements/pinned orders, packing, courier/cart dispatch/return and payout collection. Add the `Delivery` upgrade and pad to open the already-built bay door. Keep tutorial/direct commissions immediate.
- [ ] Set delivery matching, capacity, trip speed, rewards, expiry/cancellation and offline rules; tune upgrades. Reference-game numbers are not selected balance.
- [ ] Implement bonus-only weather traffic, scheduling and stacking; preserve normal baseline traffic and the first-listing customer gate.

## 7. Presentation and release

- [ ] Finish remaining HUD/offer/assembly UI, sound, environment art and storefront imagery. Scenery/mountains were deliberately deferred; preserve the chosen simplified layout.
- [ ] Review gem rewards and monetization against the final progression.
- [ ] Complete published desktop/touch/console checks, new-player/public testing and release gates.

Import scale checks remain deferred unless a concrete mismatch requires the existing ScaleTest assets. No new ore-source selection, plot-template conversion, Starter Shop import, roof-fade implementation or finished-sword mesh strategy is required by the current build records.

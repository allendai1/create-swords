---
title: Roadmap
status: active
type: development
updated: 2026-10-19
tags: [roadmap, create-swords]
---

# Roadmap

Remaining work against [[Design/Game Design Document]]. Built behavior and verification limits belong in [[Current Status]] and [[Development/Code Map]]. Completed historical phases are preserved in [[Archive/Project History/Roadmap before vault organization — 2026-10-19]].

## First-session loop

- [ ] Set base forge heating to **10 seconds** (latest build note still reports 15).
- [x] Ore roulette (2026-10-20): the shared lever spins every empty stand (2.6 s), results wait on the stands until collected, occupied stands are skipped, no automatic restart. One stand today; buying more stands is still to do.
- [ ] Start with the tantō blueprint and on-screen guidance. Suppress customer visits during the first craft; the first listing triggers the tutorial customer.
- [ ] Guarantee a fair first offer; teach haggling on the second ordinary shop sale.
- [ ] After the first sale, introduce **Iron Wakizashi**, minimum 90% quality, providing the blueprint at commission start. Final polishing remains optional.
- [ ] Deliver commissions through a sword picker for the agreed reward, without display listing or haggling.
- [ ] After delivery, offer the **second material stand** upgrade; tune its cost against tutorial earnings.
- [ ] Replace hilt timing/seat bonuses with three untimed taps; introduce tradition-matched fittings unlocked by crafting milestones.
- [ ] Introduce katana through a later local teaching commission.
- [ ] Implement session-locked persistent saves for currencies, inventory, unlocks, and upgrades.

## Crafting quality and validation

- [ ] Tune hit rhythm, staged/local deformation, blade proportions, full-blade camera framing, and hot-to-steel presentation from player feedback. Retain the initial shared hit count; tune modest extra effort for higher tiers later.
- [ ] Verify final polishing at the Polishing Station is understandable, safe, and genuinely optional in coins earned per minute; test enjoyment after several swords.
- [ ] Recheck roll → heat → forge to 90% → hilt → optional etch → optional final polish → display → sale, including saving partial polish and reaching 100%, after the imported-station changes.
- [ ] Reduce the documented one-EditableMesh-per-visible-sword resource pressure; decide caching/static-mesh strategy while preserving refined appearance.
- [ ] Test published clients, lower-memory phones, multiplayer observers, and leaving/rejoining during crafting. Studio probe timings are not device-wide performance evidence.
- [ ] Tune blueprint prices/stars, fitting milestones, material rewards, and commission requirements.

## Shop, village, and progression

- [ ] Build six-player plot assignment and the shared mountain village. **Village street built 2026-10-21** (`Workspace.Village`, six empty `PlotSlot` lots; see [[Art/Japanese Street]]); plot assignment, moving the plot into a lot and per-player stations remain.
- [x] Move the plot, `SpawnLocation` and `Village.CustomerSpawn` onto the street (2026-10-21): lot N2 widened to 280; see [[Development/Code Map#Village street (2026-10-21)]].
- [ ] Playtest the plot in lot N2: spawn, pads, customer routes to every display (`AISLE_ROWS` now follow `EntryPoint`), ore lever.
- [ ] Settle the plot footprint, then size all six lots to it (only N2 is widened).
- [x] Build a spacious property with distinct storefront/crafting areas, broad routes, and expansion reserve (one plot, 126 × 78 studs after the [[Art/Player Plot Review|Player Plot Review]] pass, 2026-10-19; see [[Development/Code Map]]). Dimensions still to be checked with six plots side by side.
- [x] Second plot layout geometry pass from [[Art/Player Plot Review]]: deeper pavilion, wider openings, forward anvil, and revised displays built; historical traversal playtest recorded. Remaining checks are listed below and in the review.
- [ ] Finish plot comfort checks: rotate the camera at every station, check touch framing, all holder/customer paths, the newly imported stations, and the footprint of six plots side by side.
- [x] Detailed katana hilt in the game (2026-10-19): `SmithyCore.buildSword` dresses every sword with `ServerStorage.SwordParts.KatanaHilt` in recipe colours; Allen checked it in a playtest. See [[Art/Katana Hilt#In the game (2026-10-19)]].
- [ ] Validate the imported blade-down universal holders with tantō, wakizashi and katana: guard on pads, tip above floor, customer approach clear. Slots have already been raised/rotated; verify final Hilt Bench and holder picker framing.
- [ ] Lighter hilt for many visible swords: bake the wrap onto a light core (about 15k triangles now).
- [x] Prototype the first etch pattern (2026-10-19): original flame etch on the blade (`BladeEtch`) and a flame tsuba (`SwordParts.FlameGuard`), working held and displayed. See [[Art/Flame Etch]].
- [x] Etching Table station (2026-10-20): pick a sword and a pattern, applied instantly and free (Allen's call), +15% value. See [[Art/Flame Etch]].
- [x] Flame etch v4 in the game (2026-10-20): Allen's reference band, ported to `BladeEtch` (vertex-coloured skin; no texture needed) and playtested on katana, wakizashi and tantō. See [[Art/Flame Etch]].
- [x] Smaller copper blade collar (habaki) on the katana hilt (2026-10-20).
- [x] Guard set (2026-10-20): five new tsuba shapes (Kaku, Mokko, Kiku, Kumo, Kuruma), one per hilt recipe, and Hilt Bench cards that show the real hilt and guard. See [[Art/Katana Hilt]].
- [ ] Complete the Blender-station post-import playtest: models are placed, coloured and checked for Z-fighting. The later Polishing Station session tested forging and rolling, but the complete heat → hilt → all blade-down holders → customer sale loop remains open. See the checklist and subsequent recorded tests in [[Sessions/2026-10-19]] and [[Art/Blender Station Review]].
- [ ] Picker icons that match their item (2026-10-20): blade and sword cards draw the real blueprint blade, and sword cards the real hilt. Etching pattern cards show the etch. **Playtest pending** for the final framing.
- [x] Polishing Station (2026-10-20): grinding moved off the anvil; polishing the finished sword to 100% is the free final step. Reroll lever with hold animation and a bigger ore display. See [[Development/Code Map]] (Polishing Station).
- [ ] Polishing Station follow-ups: polish sounds and a stone that follows the cursor; decide whether etching a polished sword should be allowed (today it is).
- [x] Low-poly building and bamboo redesign (2026-10-20): the shop is the only building; stations sit on an open stone courtyard (moved +8 in x); new bamboo and standing stone lanterns. In the game and playtested. See [[Art/Building Redesign]].
- [ ] **EditableMesh budget (found 2026-10-20; shared-mesh fix built, playtest pending):** `Shared/SwordMeshCache` caps sword meshes at 9 blade + 9 etch, shared by every sword. Retest with 20+ swords once Studio Play responds. Original note: about nine swords on screen (blade + etch each) hit the client's EditableMesh memory budget, and further blades and etches failed to draw. Needed before multiplayer and full display racks: share one static mesh per blueprint and finish (and per etch), lower the etch sampling, or bake finished swords to MeshParts.
- [ ] Starter Shop (2026-10-20): Blender model and review made (16 × 14, 2 holders); on Allen's approval, swap it in and keep the big shop as the Upgraded Store. See [[Art/Building Redesign]].
- [x] Forge heats one ingot at a time (2026-10-20, `ForgeService.SLOT_OFFSETS` has one entry); a second furnace will be a tycoon purchase (not built).
- [x] 100% from forging, +10% polish finish, anvil view closes, panel silhouette straightened, no polish flash (2026-10-20). Playtest pending.
- [x] Hilt seated by three untimed knocks with the hilt sliding onto the blade (2026-10-20). Playtest pending.
- [x] Courtyard zones (2026-10-20): stations spread into an ore yard, forge hall, smithing area, finishing corner and sword rack by the shop door, with room left for more stands and furnaces; upgrades branch by zone. Playtest pending. See [[Design/Tycoon Upgrades]].
- [x] Tycoon floor pads (2026-10-20): plot claim, 12 chained buy pads with a Buy button, 3-sword display table and wall rack, + markers for display slots, locked stations, second furnace and the Starter → Upgraded Store swap. Playtest pending. Saving bought upgrades comes with DataStore saving. See [[Design/Tycoon Upgrades]].
- [x] Wall sword holders (2026-10-20, replaced the same day by tycoon pads): buy one for 100 coins on any of nine marked spots on the shop walls; `ShopService` handles any number of holders. Saving bought holders comes with DataStore saving. See [[Art/Building Redesign]].
- [x] Stylized feudal shop (2026-10-20): two-storey Upgraded Store in the game (kanji sign on the entrance canopy); one-storey Starter Shop staged in `Buildings3D.StarterShop`. Playtest pending. See [[Art/Building Redesign]].
- [x] One-piece anvil mesh, unlimited ore re-rolls, wider shops (Upgraded 31 × 38, Starter 24 × 14 staged), roof fades when inside (2026-10-20). Playtest pending.
- [x] Ingot Rack (12) and Finished Sword Rack (6), carry then deposit (2026-10-20). Playtest pending; employees using them comes with the employee system.
- [x] Quick thoughts batch (2026-10-20): one-tray forge, timer-only forge label, anvil Cancel button, Polishing Station before Etching Table, simpler 1.5x ore stand with floating ore. Playtest pending.
- [ ] Tycoon purchases: buying more furnaces, ore stands and the Upgraded Store (coins exist; no purchase system yet).
- [ ] Etching Table follow-ups: prices for the table and patterns (Allen: free for now), deferred trace minigame, more patterns, and persistent `etch` data. Etch-aware picker art is implemented; final framing remains a validation task above.
- [ ] Settle remaining import-scale validation using `Models/Stations/ScaleTest/ScaleTest.fbx` / `.glb` if needed (deferred by Allen 2026-10-19). Mid-high stations and hilts are already imported; this is no longer a pre-import blocker.
- [ ] Turn the plot into a per-player template: stations looked up per plot instead of the shared `Workspace.Smithy`, so it can be cloned six times.
- [ ] Implement early/mid/late building and station upgrades using [[Art/Japanese Village Concept Art]] as the visual reference; concept counts are illustrative.
- [ ] Add upgrade purchases for holders, forge capacity, heating speed, ingot storage, material stands, and roll luck; add Material Index.
- [ ] Use displayed stock to influence regular customers and reputation to unlock special arrivals. Include primarily local early customers and an early special outsider.
- [ ] Add letters, in-person commissions, untimed special requests, familiarity, and personal commission chains.
- [ ] Introduce outside sword traditions through visitor commissions, then offer additional blueprints for coins.
- [ ] Make functional facilities affect business while keeping decoration cosmetic.

## Employees, deliveries, weather, and roof visibility

Design source and open tuning details: [[Design/Workshop Growth]]. These features are not recorded as implemented.

- [ ] Build employee hiring/management/upgrade UI showing role, level, speed, forging ceiling and polishing ceiling where relevant; workers progress through completed work. Choose prices, thresholds, hire variants and unlock timing before implementation.
- [ ] Add purchasable anvils and separate bare-blade/finished-sword racks; define assignment, input permissions, queues, player/worker station priority, and full-rack behavior.
- [ ] Implement the furnace operator, smith and combined finisher. Smiths deposit bare blades; finishers attach the selected hilt and optionally polish to their worker ceiling. Support pause after assembly for player etching, then resume final polishing. There are no separate hilter/polisher professions.
- [ ] Implement the stocker: visibly move ready-for-sale swords from the finished rack to empty shop holders; preserve commission/delivery/further-finishing reservations; wait when holders are full or no eligible stock exists. Initial progression is stocking speed; priority modes remain later options.
- [ ] Define sub-90% employee forging data, appearances and value rules: starter smiths train toward 90%. Extend the current 90–100% refinement assumptions deliberately, including any value range below 80%.
- [ ] Let players resume an employee's un-hilted blade at the anvil to 90%, then polish the assembled sword beyond an employee's polish cap up to 100%. Keep forging and polish completion separate.
- [ ] Add the cashier with its configurable acceptance threshold; test employee output against player crafting and preserve a reason for personal finishing.
- [ ] Validate the five-role chain and player handoffs: furnace operator → smith → bare-blade rack → finisher → finished-sword rack → stocker → holders → cashier. Worker-count caps, balance and offline earnings remain separate design work; no ore-attendant/automated-etcher profession is selected.
- [ ] Design and build a separate remote delivery board: recipient/requirements, pinned order, sword packing, courier/cart dispatch/return, and payout collection. Keep direct commissions and the first Iron Wakizashi hand-in unchanged.
- [ ] Tune courier trip-speed/capacity upgrades, matching rules, rewards, expiry/cancellation and offline behavior. The pottery reference's 3:30 / 3000 gold / 6→9 numbers are not selected balance.
- [ ] Add weather traffic bonuses: sunny weather can boost arrivals; other weather stays at baseline. Define scheduling and bonus stacking; preserve the first-sale customer gate.
- [ ] Add indoor roof transparency/cutaway and exterior restoration, following the supplied pottery screenshots. Prefer a local fade/hide; verify roof/eave transitions and normal/station cameras without changing shared-world collision.

## Later systems and launch

- [ ] Review optional color/enamel and gem-work scope; keep existing etching and final polishing optional rather than adding them to the required crafting path.
- [ ] Implement gem rewards/upgrades and review monetization proposals against the final loop.
- [ ] Finish HUD/offer/assembly UI, sound, environment art, tutorial polish, and storefront imagery.
- [ ] Run new-player tests across desktop and touch, then public testing and launch checks.

## Already built — see Current Status for evidence

Browser study/editor, BladeCore port, untimed anvil forging, safe grinding, server Finish checks, and the Japanese workshop/station rebuild are documented as implemented. They are not new pending tasks here. A complete build chronology remains in [[Sessions/2026-10-19]].

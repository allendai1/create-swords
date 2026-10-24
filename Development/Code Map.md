---
title: Code Map
status: current recorded architecture — runtime verification pending
type: development
updated: 2026-10-24
tags: [code, architecture, create-swords]
---

# Code Map

Current architecture consolidated from the build records through 2026-10-22. Gameplay code lives in the Studio place (`goku19876's Place: 10172026_1`), with no Rojo export in this vault. Confirm live sources before editing and save the place after Studio work. This document was reconciled offline, not verified against a running place.

The former chronological code map, including asset IDs, exact geometry, backup names and dated implementation details, is preserved in [[Archive/Project History/Code Map before cleanup — 2026-10-22]]. Current tasks belong in [[Development/Roadmap]] and design in [[Design/Game Design Document]].

## Gameplay and state

```text
Owned ore-box lever → ForgeService → collect cold ingot
ForgePut / ForgeTake → heat one ingot per furnace → hot ingot
BeginForge / FinishBlade → SmithService + ForgeCheck → forged blade
AttachHilt → drag-on hilt seat → assembled sword
Optional BeginPolish / PolishSword → polish finish bonus
Optional EtchSword → accepted etch + client playback
DisplaySword → customer Offer / RespondOffer → coins + sale count
```

Recorded player-facing rule: completing forging gives **100% quality**; full polish multiplies the value by **1.10** (since 2026-10-23; it was +10% added to the other bonuses) and etching adds **+15%**. Old 90%-cap descriptions in the archived map predate that rule. Blade refinement remains an internal geometry/finish concept; do not infer current displayed quality or server limits from old port/probe descriptions. Inspect live SmithService/ForgeCheck when changing either.

Server state is authoritative: inventory, coins, completed/sold counters, racks, displays, furnace contents and bought upgrades. Since 2026-10-22 it is saved per player under a session lock ([[Development/Saving]], [[#First session and saving (2026-10-22)]]). Item pickers open even when only one valid item exists.

## Workspace and plot ownership

- `Workspace.Village`: the chosen simplified walled map, six lots, gate, shrine and broad flagstone street. `Village.Lots.PlotSlotN2` is the template's Edit pivot, (640, 0.5, −284) since 2026-10-24 (−292 before): the middle lots N2 and S2 no longer stand 8 studs back as a junction, they sit on the street's line like the others ([[#Refinements 3 (2026-10-24)]]); other slots identify the five remaining lots.
- `Workspace.Plot` in Edit: reusable template with `Shop`, `Workshop`, `Smithy`, `Pads`, `Yard`, `PlayerSpawn`, `CustomerSpawn` and the delivery bay. At runtime PlotService moves the template to `ServerStorage.PlotTemplate`.
- Claim order: **N2, N1, N3, S2, S1, S3**. A joining player gets `Plot_<lot>` with `Lot`, `OwnerId` and `OwnerName`; the player receives a `Plot` attribute and their own respawn location. South lots turn the whole plot toward the street.
- Unclaimed lots hold inert empty plot copies. Claiming replaces one; leaving destroys the owned copy and restores the empty one. Visitors can walk through but cannot use another player's stations or buy upgrades.
- `Plot.Shop`: Starter/Upgraded shells, displays, entry point and decor-only commission boards. `Plot.Smithy`: ore roller, furnaces, anvil, hilt/polish/etch stations and racks.
- Upgraded Store pushes the workshop, stations, workshop pads, spawn and characters inside it back **12 studs** in plot space. Use plot-local coordinates for moves, cameras and customer routing.
- `Shop.DeliveryDoor` stands from the start (since 2026-10-23; `Shop.DeliveryWall` is gone) with its sliding door, `Slide`, shut; its curtains (`Noren`) are TycoonItems of `Delivery`. The Delivery Cart upgrade (2026-10-22) slides the door aside by `Slide.OpenOffset` (DeliveryService) and brings the board and cart (`Shared/Deliveries` below).

Details: [[Design/Six Plots]], [[Design/Tycoon Upgrades]], [[Art/Workshop Layout]], [[Art/Ore Loot Box]].

## ServerScriptService

| Script/module | Responsibility |
|---|---|
| `SmithyCore` | Per-player ingots/blades/swords, coin transactions, completed/sold counters, public state, item Tools/Models and respawn restoration. Sword values include fitting/polish/etch bonuses. |
| `PlotService` | Template, lot allocation, empty copies and owner/plot lookup. API: `plotOf(player)`, `plotFrom(inst)`, `ownerOf(inst)`; preparation, claim and release hooks. |
| `TycoonService` | Per-plot `Bought_<id>` flags, prerequisite pads, ownership/reach/spend checks, `TycoonItem` locking and workshop push. Since 2026-10-24 it charges `Upgrades.price(plot, u)` and runs Merge Ore Slots ([[#Refinements 3 (2026-10-24)]]). |
| `ForgeService` | Each plot's ore box and purchased slots; spin whenever no roll is playing, waiting ore going into your hands first (since 2026-10-24; supersedes collect-before-reroll, 2026-10-22); roll luck from `Upgrades.luck` (Lucky Roller × merges); one ingot per unlocked furnace. Heating is 3 s until first completion, then 10 s. |
| `SmithService` | Begin/finish forge requests, blueprint/ingot validation through `ForgeCheck`, and hilt assembly. |
| `ShopService` | Owner-specific displays, per-plot customer routes/spawners, offers/haggling and sale payouts. 2–4 customers at once per plot (More Clients), plus one per Rickshaw Bay (`Rickshaws`, 2026-10-23), plus one with the Shop Promoter (2026-10-24). Since 2026-10-24 a hired Cashier answers offers for you. Since 2026-10-23 `DisplaySword` and the restore on claim check `Blueprints.fits` (big swords only on `BigSword` holders). |
| `PolishService` | BeginPolish/PolishSword, station reach/unlock checks, refinement replay/timing validation, state update and rebuilt sword. `PolishSword(swordId, saved, leaving)`: leaving the station sends what was polished (or nil) with `leaving = true`, which keeps a partial polish and ends the session; `PlayerPolishing` on the station from BeginPolish until then keeps the crafter off it (2026-10-23). |
| `EtchService` | Valid sword/pattern, own unlocked station/reach and one-etch-per-sword checks; accepted finish updates authoritative state. |
| `RackService` | Own-plot ingot/sword storage and retrieval; capacities 6 ingots (12 until 2026-10-23), swords up to the open hooks (`Upgrades.openSlots`: 6, or 12 with Finished Sword Rack 2, since 2026-10-24; was a fixed 6), 6 carried. |
| `LeverAnimator` | Lever hold/release motion for plot rollers. |
| `DevTools` | Studio-only coin and example-sword grants; guarded by `RunService:IsStudio()`. |

First-sale exceptions: a listing spawns a customer immediately until `sold > 0`; later arrivals use 12–22 s intervals (shorter with the Shop Promoter, since 2026-10-24). The Cashier answers only from `sold >= 2`, so the first two sales stay the player's. At `sold == 0` the offer is exact value and declining ends it. At `sold == 1` a hint shows and the first decline guarantees a raise. Later sales use normal negotiation. Future direct commissions must not increment the ordinary-shop sale counter.

## ReplicatedStorage

| Module/asset | Responsibility |
|---|---|
| `Shared/BladeCore`, `BladeData`, `Blueprints` | Blade geometry/progress, universal blank and tantō/wakizashi/katana data. Local port/data tools remain under `Prototypes/tanto-forge/`. Since 2026-10-23 also the western blades and the Zanbatō; `Blueprint.big` marks a big sword and `Blueprints.fits(id, holder)` says whether it may stand on a display holder (`BigSword` attribute = the Big Sword Stand). |
| `Shared/BladeView`, `BladeMesh` | Active deforming blade presentation; anvil/polishing need live geometry. |
| `Shared/ForgeCheck` | Server replay and completion/refinement/timing validation. |
| `Shared/Materials`, `Hilts`, `ValueFormula`, `Customers` | Material odds/appearance/value, fittings/milestones, price rules and NPC offer/raise behavior. |
| `Shared/Upgrades` | Upgrade IDs, prices and prerequisites; pad IDs and `TycoonItem.Upgrade` attributes must match. Since 2026-10-22 also `HEAT_TIMES`, `LUCK` and `tier(plot, prefix)` for Faster Heating (`Heat1–3`) and Lucky Roller (`Lucky1–3`), read by ForgeService. Since 2026-10-24 also the merge helpers (`merges`, `mergeFactor`, `luck(plot)`, `price(plot, u)`), `openSlots(slots)` and the crew and second-rack pads. |
| `Shared/Employees` | (2026-10-23) The sword crafter's training prices, levels (`level`, `quality`, `seconds`); its hire is the `Crafter` upgrade in `Shared/Upgrades` (a pad after Anvil 2). `EmployeeService` (server) hires on `Bought_Crafter` (Anvil 2's `CrafterPrompt` stays off until then), trains and switches shapes through the `Employee` remote (anywhere on your plot) and runs the crafter NPC's loop (Ingot Rack → `Hook_HeatIngot` in ForgeService, whose slot carries `OwnerId` 0 so clients count it busy → Anvil 2 → Polishing Station with `CrafterBusy`, set before it walks over, and only while you're not polishing (`PlayerPolishing`) → Finished Sword Rack, redrawn by `Hook_RackChanged` in RackService); `EmployeeController` (client) is its window. SmithyCore saves `crafter`. Since 2026-10-24 also `STAFF`: the Stocker, Cashier, Shop Promoter and Sword Etcher, each on its own pad, saved as `staff` ([[#Refinements 3 (2026-10-24)]]). |
| `Shared/Deliveries` | (2026-10-22) Delivery offers (bulk/special via `Orders.make`'s kind), status, public view, capacity/speed levels and prices, encode/decode with SmithyCore's sword coders. `DeliveryService` (server) runs the `Delivery` remote (accept, skip, cancel, dispatch, collect, upgrade; since 2026-10-24 there is no `pack` action and `dispatch` takes the chosen sword ids), the cart's roll and crates and the board's timer; `DeliveryController` (client) is the window, its packing page (2026-10-24) and the pinned order. `build_delivery` builds the cart, board and Delivery pad on the template. Since 2026-10-23 `PAY` (1.1; 1.3 at first) and `pay(packed, valueOf)`: DeliveryService pays it on collect and `public(s, now, valueOf)` sends it as `pay` (valueOf = `SmithyCore.swordValue`); a delivery stores no reward. |
| `Shared/Orders`, `Reputation` | (2026-10-22) Rotating board orders: `make`, `title`, `mismatch`, `decode`, `slots(level)`. Reputation points → level, bar and walk-in factor. ShopService makes, checks and pays both; SmithyCore saves `reputation`, `orders`, `nextOrder`. Since 2026-10-23 the board's clock: `GAP` {180, 600} (since 2026-10-24: a fresh random gap of 3–10 minutes per order; it was `EVERY`, 180 s) and `refill(n, slots, at, now, opening, gap)` on SmithData `orderAt` (ShopService's `refillOrders`, ticked every second per plot from `onPlot`; the board opens full), and `PAY` (1.2) / `pay(value)` on the handed-in sword's value; orders store no reward. `CommissionController` shows "+20% value", each sword's pay and a "New order · in m:ss" card (since 2026-10-23 `MailController` lists the orders as mail; the board is gone; since 2026-10-24 there is no "New order" row and an empty inbox says "No mail"). |
| `Shared/Etches`, `EtchPatterns`, `EtchCanvas` | Finish catalogue, stroke paths and progressive/final image work. Flame and Eclipse have build records; further patterns require confirmation. Since 2026-10-23 `EtchCanvas` draws the strong glow (GLOW_CM, GLOW, CORE, THICK at its top) and paints raised pixels once per flush; `SwordRenderer` builds world etches over frames. |
| `Shared/SwordMeshCache` | Shared, baked-first finished-sword geometry with live fallback and etch/polish appearance. |
| `SwordMeshes`, `SwordParts.KatanaHilt` | Uploaded finished meshes and dressed hilt/guard templates used by world and viewport art. |
| `Remotes` | Forge/hilt/polish/etch, state, rack, display/offer and upgrade request/event boundary. Client choices require server ownership, reach and state checks. |

Legacy `BladeProfile`, `AnvilScore` and probe modules may remain dependencies or test references. Inspect callers before removal; they are not the current design specification.

## Client controllers and interface

**GUIs live in StarterGui (2026-10-23).** Every screen everyone sees is a ScreenGui (or singleton BillboardGui) in `StarterGui`, editable in Studio's UI editor; its controller finds it with `PlayerGui:WaitForChild(name)` and fills it. Repeated pieces (cards, slots, rows, chips, order cards, book entries, holder markers) are cloned from a hidden `Templates` Frame inside the GUI (a Folder doesn't hide GUI objects, so templates in one drew on screen; turn the Frame's `Visible` on to edit them); 3D art in ViewportFrames, the coin fly-in, "+N" pops and confetti stay in code. Every moved GUI has `ResetOnSpawn = false` (a respawn must not swap in a fresh copy) and arrives at the first spawn, so controllers and `ItemPicker` wait for it then. Still built in code: `DevPanel` (developer-only) and `TycoonController`'s per-pad labels. **A ViewportFrame's Camera in a StarterGui template never reaches the client** (Cameras don't replicate): make the camera in code when it's missing, as `CollectionController` and `DeliveryController` do (the book threw and never opened until 2026-10-23).

| GUI in StarterGui | Controller | Notes |
|---|---|---|
| `PickerGui` | `ItemPicker` | `Window` (desktop) and `CompactWindow` (under 500 px tall), `Toast`, `Templates.Card`/`CompactCard`; Q, Backspace and B close it. API unchanged. `PickerBlur` stays in Lighting. |
| `HudGui` | `Hud` | `Coins`, `Reputation` pills (y −52 / −104 on the left edge). Since 2026-10-24 `Coins` has no plate (the number outlined) and `Reputation` is hidden (`Visible` false; `Hud` still fills it); the rank shows only in the Deliveries window. |
| `MenuGui` | `MenuController` (+ `GemController`, `CollectionController`, `EmployeeController`) | (2026-10-23) `Buttons`: a 3-across grid at y +30 under the gem counter: `Shop`, `Upgrades` (House → Gem Shop; Charts until 2026-10-24), `Daily` (gift, `Dot`), `Book` (sword), `Crew` (hidden until anyone is hired; until 2026-10-24 the crafter), `Settings`; VectorIcons. Since 2026-10-24 just the icons (38 px, were 30): no plates, and each button's stroke shows only as an amber edge on the gamepad's selection. MenuController styles every button and runs `ShopWindow` (empty Robux shop, "Coming soon") and `SettingsWindow` (`Music` / `Sound` rows with a `Switch`), `Dim`. |
| `HotbarGui` | `Hotbar` | `Bar` (+ `Bag` button), `BagPanel`, `Templates.Slot` (with a `Metal` line since 2026-10-24); slot size, art box, gap and padding read from the instances. On touch the bar shows as many stacks as fit left of a 170 px jump-button corner; the rest sit at the front of the bag. |
| `GemGui` | `GemController` | `Gems` counter (a Frame since 2026-10-23, no plate since 2026-10-24; Hud pops "+N" on it), `DailyReward`, `GemShop`, `Templates.Day`/`Upgrade`. Opened from `MenuGui`'s Upgrades (the House) and Daily buttons. |
| `CollectionGui` | `CollectionController` | `Window` (its `Entries` a 4-wide `UIGridLayout`), `Templates.Entry` (an `Art` ImageLabel and a `Label`; Row/Polished/Etched removed 2026-10-23); opened from `MenuGui.Buttons.Book` (its own button is gone). |
| `DeliveryGui` | `DeliveryController` | `Window` (868×450 design, `Fit`), `PinnedOrder` (since 2026-10-24 at (0, 12, 0.5, −104), the Reputation pill's old slot, with no plate, shown only while pinned; it was at y −156, or beside Reputation on screens under ~480 px tall), `Window.Body.Packing` (2026-10-24), `Templates.Order`/`Crate`/`Button`/`Slot`/`Sword`/`Pin`. |
| `RewardGui` | `RewardCard` | `Templates.Card`/`Chip`. |
| `GuideGui`, `WorkshopOpenGui`, `GuideArrow` | `Guide` | The arrow is a BillboardGui directly in StarterGui; the script sets its Adornee. |
| `PolishHud` | `PolishController` | `Panel` (+ `Fit`), `Templates.Cell`/`Bracket`. |
| `EtchHud`, `HiltSeatGui` | `EtchingTableController`, `HiltBenchController` | Matching close rings (`Close`). |
| `StrikeRingGui`, `GrindMap` | `AnvilController` | `AnvilHud` and `AnvilPoints` were already here. |
| `OfferBubble`, `ShopHud` | `ShopController` | `OfferBubble` (BillboardGui) holds the `OfferCard` that was in ShopHud; `ShopHud.Templates.SlotMarker` for the + / bag / for-sale markers. |

`UiFx` (ModuleScript, 2026-10-23) is the shared behaviour: `press` (hover 1.04 / held 0.94), `open`/`close` (16 px rise, 0.22 s), `dim` + `nudge` (a veil and a shake for what you can't do yet), `fit` (UIScale to the screen, never under 0.7), `commas` and `COIN`. Backups of every changed controller: `ServerStorage.Legacy.<Name>_beforeStarterGui` (and `ShopHud_beforeStarterGui`).

- `MyPlot`: `current()`, `get()`, `owns(inst)`, `plotOf(inst)`; controllers resolve their own plot instead of `workspace.Smithy`.
- `PromptFilter` and the shop/tycoon controllers limit prompts, buy buttons and display markers to the player's plot. Server ownership checks remain authoritative.
- `AnvilController`, `ForgeController`, `HiltBenchController`, `PolishController`, `EtchingTableController`, `RackController`, `ShopController`: station pickers, interaction, framing and feedback. The hilt view follows bench orientation.
- `ItemPicker`: reusable item cards with real blade/hilt/etch art, toasts and small-screen layout. Free temporary resources on rebuild/close.
- `EtchPlayback`: private progressive canvas over a shared overlay, stylus/sparks and station camera; restore controls, camera and hidden table props on finish/interruption. Server acceptance determines the finish, even if the show is interrupted.
- `OreBoxShow` / `OreBoxAnimator`: all clients see the 3.6 s lid/ingot show; ForgeService exposes the real results at the end.
- `SwordSlash` (LocalScript, 2026-10-23): click (Tool.Activated) with a held `ForgedSword` plays the slash combo, Animation `rbxassetid://95323165375256` (uploaded from `Workspace["Sword Animations"]["Sword Slashes"].AnimSaves.swordcombo1`: Action priority, no loop, 2.8 s). One slash per click: `SLASHES` holds the four time ranges (0–0.43, 0.72–1.17, 1.17–1.88, 2.07–2.82 s; the combo's two still holds are skipped). After a slash the arms ease back to the held pose (`Stop(0.25)`, no freeze); a click within `WINDOW` (0.8 s) goes on to the next slash, later starts over; a click during a slash is queued. Looks only; unequipping stops it. To change the animation, edit the KeyframeSequence, re-upload, and recheck `SLASHES`.
- `SwordRenderer`: held/displayed blade art and release on removal. `SwordMeshCache` uses baked finished meshes; no blanket one-live-mesh-per-finished-sword assumption remains.
- `RoofHider`: locally fades unlocked roofs on the plot the player enters; inert empty plots retain roof behavior.
- `ShopController` (2026-10-22): a holder with your sword shows the bag marker and takes over its TakeBackPrompt. `PlotService` puts the owner's nameplate (avatar bust and name) over each claimed plot. Icons: VectorIcons decals, [[Art/Icon Library]].
- `Hud` (2026-10-22): coins and reputation pills above the gem button (the reputation pill hidden since 2026-10-24), "+N" for coins and gems coming in. `RewardCard` (2026-10-22): a card after hilt/polish/etch (read from SmithState diffs) and for a first-collected metal (`Discovered` remote from ForgeService), waiting for station cameras and pickers. `CommissionController` also lists and fills board orders (`Order` remote). See [[Sessions/2026-10-22#Core loop: requests, reputation, heat/luck, HUD, reward card]].
- `Hotbar`: nine item slots plus bag button (`~`), rarity colours, ingot stacking, backpack overflow, drag/drop and click/tap equip. Gamepad R1/L1 cycle through the bar and then the bag (2026-10-22). [[Art/UI Design]] records the chosen styling.

Etched polishing now brightens the body at polish levels; preparation spreads over frames and the last etch remains warm for 5 s after leaving. This is a recorded hitch fix awaiting Play verification.

## Local builders and authoring

- `Models/Village/build_simple.luau` builds the live map; `build_shops.luau` builds shop/workshop shells, then `build_workshop.luau` builds the room furniture, loot box and delivery pieces. `build_big_sword_stand.luau` (2026-10-23) builds `Shop.Displays.BigSwordStand` and its pad marker on the template.
- `build_street.luau` and `build_town.luau` are retained historical builders for the parked maps, not the live-map entry point.
- Studio copies live in `ServerStorage.Builders`; compare copies after edits. Builder source modules are executed with `loadstring(...Source)()`, rather than required as ordinary modules.
- `ServerStorage.Builders.bake_sword_meshes` is an ordinary require-able module, run from a fresh clone with the local `Development/sword_mesh_bake.py` helper. See [[Development/Sword Mesh Pipeline]] for upload/bake instructions.
- `Models/Stations/AnvilV2/build_anvil_v2.py` (headless Blender) builds the stylized anvil: `AnvilV2.fbx`/`.glb`, `Textures/anvil_v2_color.png`, `review/`, `qa.json`; `contact_sheet.py` makes the review sheet. Not in the Studio place yet.
- Blender/Blockbench sources and exports remain under `Models/`. `Prototypes/` contains runnable sources; keep internal paths stable.
- `ServerStorage.Legacy` retains old maps, scripts and assets. Offline cleanup did not remove anything inside the Studio place.

## Tests and evidence

| Entry point | Recorded scope |
|---|---|
| `ServerStorage.Tests.BladeCoreSpec` + `BladeGolden` | Luau port; local instructions in [[Prototypes/tanto-forge/roblox/README.md]]. |
| `ServerStorage.Tests.ForgeCheckSpec` | Server finish/polish validation; historical 35-check record. Recheck current limits against live code. |
| `ServerStorage.Tests.EtchingSpec` | Recorded 33/33: canvas/path behavior, cache isolation, spreading, cleanup and failures. |
| `ServerStorage.Tests.SwordMeshSpec` | Recorded 110/110: baked hashes, geometry, UVs, colours, normals and cache lookup. |
| `ServerStorage.Tests.AnvilSelfCheck` | Frozen `Legacy.SharedV1` prototype behavior, not current gameplay acceptance. |

For tests requiring a fresh module, use the recorded clone pattern, e.g. `print(require(game.ServerStorage.Tests.SwordMeshSpec:Clone())())`. These results are historical; cleanup reran no Studio tests. Runtime, multiplayer and device checks remain in [[Development/Roadmap#1. Validate the current combined build]].

## Etching patterns (2026-10-22)

There are seven patterns: Flame (the band) and six stroked ones: Eclipse, Tide, Stormroot, Woven Wind (`WovenWind`), Fracture and Falling Stars (`FallingStars`). This supersedes "further patterns require confirmation" and the `EtchingSpec` 33/33 record above. Details and pictures: [[Art/Animated Blade Etching#Five more patterns (2026-10-22)]].

| Module | 2026-10-22 |
|---|---|
| `Shared/Etches` | Five more `list` entries, free, +15%, with Eclipse's body and fallback mark colour; the mark colour comes from the material. The pattern picker (`EtchingTableController`), `EtchService`, `SmithyCore` and card art read the list; nothing else lists patterns. |
| `Shared/EtchPatterns` | `STROKED` has a generator per pattern, `(length cm, widthAt) → strokes`. Fracture's shards are strokes with a `fill` polygon; it puts an upright fault on each strip seam (`EtchCanvas.strips`). |
| `Shared/EtchCanvas` | A `fill` stroke reveals its convex shape's columns as the guide passes, with sharp anti-aliased corners. `strips(length, widthAt)`. Blank images are cached by layout and body colour (weak keys) and copied. Fully covered pixels are skipped (same output). |
| `ServerStorage.Tests.EtchingSpec` | 36/36. It runs the canvas checks for every stroked pattern × blade, including "nothing on the bare strips or in the tip" and Fracture off the seams, plus 14 show runs across all seven patterns. |

- **Known seam:** a faint line one texel wide where a canvas's strips meet (1/3 and 2/3 of a katana, 1/2 of a wakizashi), because the texture wraps at the baked overlay's UV edge. Fix: inset the UVs half a texel and re-bake (`Development/Sword Mesh Pipeline`).
- **Pattern picker:** it builds a finished image per stroked pattern on the chosen sword, all at once: about 0.4 s on a katana in Studio.
- **Backups:** `ServerStorage.Legacy.<Name>_beforeEtchPatterns` for EtchPatterns, EtchCanvas, Etches and EtchingSpec.

## First session and saving (2026-10-22)

Roadmap 1–3 work; supersedes "Persistence is not implemented", "Counters reset each session" and the session-only lines above. Saving rules: [[Development/Saving]].

| Script | 2026-10-22 |
|---|---|
| `ServerScriptService.Profiles` (new) | DataStore key `u<UserId>` in `Profiles_v1` (Studio: `Profiles_Studio_v1`). Session lock via `UpdateAsync`, save tokens, `VERSION` 1 and `migrations`. `Profiles.new(options)` runs the same rules over any store (tests). |
| `ServerScriptService.SmithyCore` | SmithData adds `blueprints`, `discovered`, `upgrades`, `commissions`, `rack`, `displayed`, `funnel`. Loads on join, autosaves every 60 s, saves on leave and `BindToClose`. `snapshot` = `encode` + `onSave` hooks; `onLeave` hooks run after the snapshot (use them, not `PlayerRemoving`, for anything the save reads). `waitLoaded`, `funnel(player, step)` (AnalyticsService onboarding funnel, steps in `FUNNEL`), Studio-only `resetProgress`. Display sword models stream atomically. |
| `PlotService` | Claims a lot only after `waitLoaded`; releases through `SmithyCore.onLeave`. |
| `TycoonService` | Purchases go in `d.upgrades`; `onPrepare` re-buys them on the new copy (Upgraded Store push included) before it appears. |
| `RackService` | Rack contents are `d.rack`, shown on claim. `listOf` also sends refinement and etch. |
| `ForgeService` | `onSave`: furnace ingots (hot) and uncollected/mid-roll ore (cold). Collecting marks `d.discovered`. Player clean-up in `onLeave`. |
| `ShopService` | Displayed swords in `d.displayed` by holder path, put back on claim. One offer card at a time per owner (`askOwner` waits). Teaching commissions: visitor NPC (`CommissionId`, `Plot` attributes, `CommissionPrompt`), `Remotes.Commission` (`accept`, `deliver`). |
| `SmithService` | `BeginForge` refuses blueprints not in `d.blueprints`; `AttachHilt` checks `Hilts.fits`. |
| `DevTools` / `DevPanel` | Studio buttons **Skip tutorial** (`DevSkipTutorial`) and **Reset progress** (`DevResetProgress`). |
| `Shared/Commissions` (new) | `IronWakizashi`, `Katana`; `title`, `mismatch`, `due`. |
| `Shared/Blueprints`, `Shared/Hilts` | `tradition` field; `Hilts.fits(hilt, tradition)`. |
| `StarterPlayerScripts.Guide` (new) | Goal line (`GuideGui`) and arrow (`GuideArrow`). |
| `StarterPlayerScripts.CommissionController` (new) | Visitor and request-board pickers, hand-in. Board prompt: `RequestsPrompt` on `Shop.<Starter/Upgraded>.Shell.CommissionBoard.Board` (template and `build_shops`). |
| `AnvilController` | Learned blueprints only; closing the blade picker no longer locks the anvil; gamepad R2 strikes, B leaves; the blade follows the anvil after the push; a failed save waits for Finish. |
| `Hotbar` | Gamepad R1/L1 cycle through the bar and bag; hidden over `PolishHud` and `HiltSeatGui`; the bag stays below the top bar. |
| `ShopController`, `TycoonController` | Gamepad: Y accepts and L2 declines an offer; Y buys on a pad (it wins over the card). |
| Station controllers, `ItemPicker`, `SwordRenderer` | Picker open-flags set after `open`; etched/polished swords drawn as such on every picker card; baked meshes preloaded; a sword whose Handle arrives late renders later. |
| `ServerStorage.Tests.SaveSpec` (new) | 38/38: lock rules over an in-memory store, encode → JSON → decode, commission rules. |
| Template | `Workshop.InsideZone` reaches 1 stud further toward the street, closing the 0.7-stud roof gap at the shop door (before and after the push). |

Backups: `ServerStorage.Legacy.<Name>_beforeSaving` for every changed script.

## Inbox fixes, gems and street life (2026-10-22)

From Allen's Random thoughts list. Backups: `ServerStorage.Legacy.<Name>_before<Task>` (`_beforeShopPolish`, `_beforeGems`, `_beforeTutorialFinish`, `_beforeHiltDrag`, `_beforeUiFixes`, `_beforeAtmosphere`).

| Script | 2026-10-22 |
|---|---|
| `ShopService` | Offer event carries the customer (`npc`, `pos`). No price tag on displayed swords. Collision groups `Npcs` / `PlayerChars` (NPCs don't collide with players or each other). Customers at once and walk-in interval come from the owner's gem levels (`GemUpgrades.maxCustomers`, `spawnInterval`). |
| `ShopController`, `ShopHud.OfferCard` | The offer is a BillboardGui `OfferBubble` over the customer (owner only, AlwaysOnTop, the card as its template): "$N [+x%]" green/red, countdown, haggling hint, Y / L2 on gamepad. + markers centred on each holder (`SWORD_MID`, `SPREAD`), AlwaysOnTop, shown within `SHOW_RANGE` 9 studs of the character. |
| `StreetLife` (new) | 5 villagers in `workspace.Villagers` strolling the street centre (z -200 ± 8, x 455–835), `Npcs` group. |
| `Shared/GemUpgrades` (new) | `DAILY`, `list`/`byId` (Advertising, Clients), `spawnInterval`, `maxCustomers`, `price`, `today`, `daily`. |
| `SmithyCore` | `gems`, `gemUpgrades`, `streak`, `lastClaim` (saved); `addGems`, `spendGems`, `gemLevel(player?, id)`; leaderstats `Gems`. |
| `GemService` (new), `GemController` (new) | `Remotes.Gems` ("state", "claim", "buy"). Gem button on the left edge (amber dot = reward waiting), Daily Reward window on join, Gem Shop window; D-pad left on gamepad. |
| `DevTools` / `DevPanel` | "+100 gems" (`Remotes.DevAddGems`). |
| `Shared/Commissions` | First request: any metal (`materialId = nil`), id still `IronWakizashi`. |
| `Guide` | "Workshop open!" banner and confetti when Ore Slot 2 is bought after the first request (once per session, not on join). |
| `HiltBenchController` | Drag the hilt onto the tang (`SEAT_TOL`, `KEY_TIME` 0.6 s for Space / A / R2); `SeatHiltSlide` binding; chevron instead of the ring. `SeatHiltLeave` (Q / Backspace / B) or the × ring backs out before it seats, as does dying; all prompts are off during the seat (2026-10-23). |
| `AnvilController` | `drawOutlines`: target and current blade in one frame (computed from all `blade.shapes`), straightened, width ×`WIDTH_BOOST` 2.5, fine sampling near the point, current shape drawn live from `stationParams`. |
| `Hotbar` | `GAP` 16 (a clear gap past the 3 px edges). |
| `SaveSpec` | 47/47: adds gems, levels, streak and the any-metal Wakizashi. |
| `ServerStorage.Builders.build_atmosphere` (new; local `Models/Village/build_atmosphere.luau`) | Rerunnable (`loadstring(...Source)()`, SEED 31; rerun after `build_simple`). Sets Lighting (warm 16.9 h, latitude 28, Atmosphere, Bloom, new Sky and ColorCorrection, brighter indoor Ambient), rebuilds `Village.Atmosphere` (1,372 parts: Nature, Dressing, Backdrop.Forest; tree meshes cloned from `Village3D`/`Buildings3D`) and the Terrain hills and peaks outside the walls (`Terrain:Clear()` each run), and makes the village's own lanterns glow. Keeps off lots, delivery bays, the street's central 20 studs, the gate and shrine approach. Backup: `Legacy.Lighting_beforeAtmosphere`. |

## Second inbox list (2026-10-22)

Shelf, grand store, block mountains, roads, friends and the collection book ([[Sessions/2026-10-22#Second inbox list]]). Supersedes, above: the build_atmosphere row's "Terrain hills and peaks" and `Terrain:Clear()` building terrain (it now clears and builds none), and the "broad flagstone street". Backups are listed in the session note.

| Script / instance | 2026-10-22 |
|---|---|
| `Plot.Shop.Displays.WallRack1…4` | `Rack` (118 MeshParts) replaced by `Shelf` (53 Parts, `BuiltBy` build_workshop). Slots at 2.5 / 4.5 / 6.5, blade along +X; `InspectPoint` at the shelf's centre, 3.5 out. Names, attributes, holder paths unchanged. |
| `Builders.build_workshop` | New rerunnable "wall sword shelves" section builds the shelves (the racks were hand-placed template items before). |
| `Plot.Shop.Upgraded.Shell.Grand` | **Removed 2026-10-22** (in `ServerStorage.Legacy.ShopExtras_removed.Upgraded_Grand`; `grand()` deleted from `build_shops`). Was: 134 parts of Upgraded-only decor; `Shell.Roof.Kanban` is 17 × 2.2 with gold `KanbanFrame` strips. Built by `build_shops`' `grand(shell)` from `shopRoom` (Upgraded only); `chochin` takes an optional light range. Lights: shadows off, off while locked (TycoonService). A full `build_shops` rerun would undo the hand fix to `Workshop.InsideZone` (1 stud toward the street). |
| `ShopController` | `TIER` 1.5: a holder whose slots are a tier apart (the shelves) doesn't fan its + markers; tables still fan by `SPREAD`. |
| `ShopService` | `TakeBackPrompt` on E. Customers take a friend's rig from `Friends.take(owner.UserId)` (`makeNpc(c, from, toward, friend?)`); `onPlot` warms the owner's pool; the sale notice names the friend; the Offer event's `customer` is the shown name. |
| `Friends` (new ModuleScript) | `take(audience, sources?)` → `{ id, name, rig }` or nil, never waiting on the web; `warm(audience, sources?)`. A pool of 3 prebuilt R15 rigs per audience (owner UserId; the street is 0, sourced from everyone in the server). Friend lists (paged, cached), looks (`GetHumanoidDescriptionFromUserId`, cached), rigs from `CreateHumanoidModelFromDescription`, scripts stripped. One friend out at a time per server; friends in the server skipped; deleted accounts filtered; failures left alone 10 min. |
| `StreetLife` | `make(i, folk?, at?)`; starts with the 5 kimono villagers and swaps one for a friend when no player is within 60 studs (first after 10 s, then every 180–360 s). Friend villagers show their name within 30 studs. |
| `SmithyCore` | `collection` (`"<blueprintId>\|<materialId>"` → `{ etched?, polished? }`, never shrinks), saved and in `publicState`. `collect(d)` (also `SmithyCore.collect`) marks every owned sword (bag, rack, displayed); `push` and `decode` run it, so hilt, polish and etch need no hooks of their own and old saves backfill. No version bump (additive, like gems). |
| `StarterPlayerScripts.CollectionController` (new) | Book button 8 px under the gem button; window with "n / 39", rows of metals in rarity order, columns tantō / wakizashi / katana; art from `ItemPicker.artModel`, freed on close. Close ring, B, Escape, D-pad right (opens too). Under 500 px tall the window scales to 0.8. |
| `SaveSpec` | 54/54: adds the collection round trip, backfill, bad keys and an old save without it. |
| `Builders.build_atmosphere` | Mountain section: blocks named Grass / Rock / Cap (Grass, Slate, Snow; anchored, no collide or touch, query on; peaks cast no shadow). Trees stand on Grass blocks or the Baseplate where 8 probes land on one flat tier. 1,557 parts, 185 of them mountain blocks. |
| `Builders.build_simple` | `ROAD_STYLE` "earth" (live) or "stone"; `loadstring(...Source)("road")` re-surfaces only Road, Paving and Junction and rebuilds `Street.RoadStyle` (146 RoadStone, gutters via the shared `channel()` that `frontage()` uses, 6 GutterBridge); the full build calls the same `surface()` / `roadStyle()` (own `Random.new(SEED + 1)`). Ground tops add centre stones 0.26 and gutter bridges 0.62. |
| `MaterialService.TownEarth`, `TownSlab` | Ground (24 studs per tile, organic) and Pavement (16, running bond), greyscale and tinted by part colour; textures from `Models/Village/road_textures.py` (fixed seeds). `TownFlagstone` is unused. |

- **Don't require `PlotService` in Edit** (even a clone): it moves `Workspace.Plot` to `ServerStorage.PlotTemplate` and places the empty plots. It happened once during the collection work and was undone by hand.
- **Lanterns:** a full `build_simple` rebuild makes the Chochin lanterns SmoothPlastic; the live ones are Neon and `build_atmosphere` doesn't set that back (older than this work).

## Refinements (2026-10-22)

[[Sessions/2026-10-22#Refinements]]. Supersedes, above: the shelf's crest mon, `ShopController`'s `TIER` / `SPREAD` fan, "Friend villagers show their name within 30 studs", and the OfferBubble's `MaxDistance` 200 and "They love it".

| Script / instance | 2026-10-22 |
|---|---|
| `Builders.build_workshop` | Shelf section: no `Mon` discs (the `disc` helper is gone); cradles at `CX ± CRADLE` (1.45); the room-side prong is a lip to foot + 0.12; every cradle part has attribute `Holds` = `"Slot<k>"`. New "display tables" section: copies `Buildings3D.SwordTableKit` onto `Displays.DisplayTable1/2` as `Table` (`BuiltBy` build_workshop) with `Stand1…3` (turned along the table, `ROWS` (0, 1.4) / (0, 0) / (0, −1.4), front prongs −0.1, `Holds` on all but the base) and puts `Slot<k>` at stand centre − 1.8 along x, `AXIS` 4.05 up. The tables' old `SwordTable_*` meshes went to `Legacy.DisplayTable<n>_beforeKit`; the `SourceAsset` attribute is cleared. Run alone: header plus the shelf and table sections (as done), so the rest of the plot isn't moved. |
| `ServerStorage.Buildings3D.SwordTableKit` (new) | Allen's import (was `Workspace.SwordTable`): `Table` and `sword_white/red/blue` (stands; `sword_blue_katana` is the sample sword, unused). Pivot on the floor at the table's centre. |
| `ShopService` | `seat(slot, model?)`: cradles = the display's parts with `Holds` = the slot's name (home saved as attribute `Home`); the sword's length is its hilt parts plus the blade from its blueprint (`BladeOffset` + `Blueprints.blade(id).length` × `STUDS_PER_CM`), since the server has no blade parts; the sword is moved to their centre along the slot's X and they close in to `CRADLE_INSET` (0.5) from its ends; `seat(slot, nil)` in `clearSlot` sends them home. Customers: `DisplayDistanceType` None (no `DisplayName`). |
| `StreetLife` | `DisplayDistanceType` None for every villager; `NAME_RANGE` removed. |
| `ShopController` | Marker: `StudsOffsetWorldSpace` = (`SWORD_MID`, 0, 0), along the slot's own axes (the property follows the adornee's axes; a world vector put the shelf markers 1.8 below their slot); no fan. Bubble `MaxDistance` = `OFFER_RANGE` 35; `Detail` becomes the countdown on `Who`'s row, right-aligned (`Who` 40 px narrower); the hint takes `Detail`'s old row; the card is `ROW` (18) shorter. |
| `ShopController` (held sword) | A marker's click or `HolderPrompt` sends the equipped Tool's `SwordId` straight to `DisplaySword`; the picker opens only with empty hands. |
| `Builders.build_workshop` (stations) | Finishing-bench section: helpers `wallSword`, `label` (SurfaceGui text, `LightInfluence` 0), `sign` (arms, braces, cords, `SignFrame`, `Sign`); new parts per station, all non-solid, in `HiltBench.Model3D` / `PolishStation.Model3D` / `EtchingTable.Dress`: Vise*, TsubaStand/BigTsuba, GuardBoard/Guard, HiltRail/Hilt; StoneBed, wider Stone, Bucket/Hoop/BucketWater, StoneShelf/Whetstone, ClothRail/HangingCloth; ChiselCase/CaseLining/CaseLid/ChiselHandle/ChiselTip, Andon* (PointLight in `AndonPaper`), Scroll (炎), InkShelf/InkJar, ChiselBoard, EtchBand. The fittings section no longer builds the right wall's tool rail and shelf. |
| `Guide` | Over a `DisplaySlot` the arrow is adorned to `GuideHolderSpot`, an upright invisible part at the holder's centre (slot + 1.8 along X). |
| `RoofHider` | Also fades the building's `Shell` descendant `Ceiling` and sets its lights' `Enabled` to fade < 0.5. |
| `Builders.build_shops` / `Plot.Shop.Upgraded.Shell.Grand.Ceiling` | (Removed 2026-10-22 with Grand.) `grand()` built tie beams, gold bands and the chochin into `Grand.Ceiling`; the live template was moved the same way (3 TieBeam, 3 GoldBand, 4 Chochin, 8 ChochinCap, 4 Cord). |

## Genshin style (2026-10-22)

[[Sessions/2026-10-22#Genshin style rolled out]] (first a gate-street test: [[Sessions/2026-10-22#Genshin-style look test]]; the smooth trees and mountains were removed again: [[Sessions/2026-10-22#Smooth trees and mountains removed]]). Switchable; currently **on**.

| Script / instance | 2026-10-22 |
|---|---|
| `ServerStorage.Builders.build_style_test` (new; local `Models/Village/build_style_test.luau`) | `loadstring(...Source)("on" / "off")`. "on": Lighting and its Atmosphere, ColorCorrection, Bloom and SunRays values (not the Sky); makes `MaterialService.PaintStone/PaintEarth/PaintPlaster/PaintRoof/PaintWood` and puts them, with livelier colours, on the Village (not `Atmosphere.Backdrop`) and the plot's Workshop, Shop.Starter, Shop.Upgraded (its Floor too, since the same day), DeliveryBay, Yard, Shop.DeliveryDoor/DeliveryWall/Interior; softens buildings in place (`…Post`/`…Pillar` → cylinders, `…Ridge`/`…Fascia` → cylinders, rolled `Eave`, `RidgeCap`, `Plinth` in `StyleAdd` folders). Every changed property is saved first as `StyleTest_<Property>` (enums as `"Enum:<type>:<name>"`); "off" restores them and deletes `StyleAdd`. Rerun-safe. Trees and mountains untouched. |
| `MaterialService.Paint*` | Near-grey tiles tinted by part colour. FreeStylized 2K textures prepared by `Models/Village/freestylized_textures.py` (royalty free, commercial use allowed): PaintEarth (Ground_02, 24 studs per tile), PaintStone (Ground_Stones_01, 10), PaintPlaster (Concrete_Wall_01, 12), PaintStoneWall (Stones_Wall_02, Cobblestone, 8), PaintWood (Wood_10, 6), PaintWoodDark (Wood_02, Wood parts whose original colour value < 0.3, 6), PaintPlanks (Wood_11, WoodPlanks, 8). PaintRoof is still painted by `Models/Village/style_textures.py` (seed 22). [[Sessions/2026-10-22#FreeStylized textures swapped in]] |
| `Lighting.Sky` | Allen's Toolbox skybox (2026-10-22). The old one is `ServerStorage.Legacy.Sky_beforeToolboxSky`. `Models/Village/style_sky.py` (a painted skybox) is unused. |
| `Village.Atmosphere.Nature`, `Backdrop.Forest` | Empty since [[Sessions/2026-10-22#All trees, shrubs and rocks cleared]]: trees in `ServerStorage.Legacy.Trees_removed` (Nature, Landmarks, Forest, Planters), shrubs and rocks in `Legacy.ShrubsRocks_removed`. |
| `Plot.Shop` (2026-10-22) | Only what the game uses: Displays, DeliveryDoor, EntryPoint, Starter, Upgraded (Shell, Lanterns, Floor, InsideZone); DeliveryWall went 2026-10-23. `Shop.Interior` (counter) and both `Tansu` are in `ServerStorage.Legacy.ShopExtras_removed`. |
| `ReplicatedStorage.Shared.Hilts` | `BLACK_ITO` (30, 28, 30) is the grip (Ito) of Wooden, Leather, Iron and Bronze; Gold red, Gem purple. Backup `Legacy.Hilts_beforeBlackWrap`. |
| `Plot.Smithy.Anvil` (2026-10-22) | `Model3D` = Allen's fantasy_anvil meshes (anvil_body_base, anvil_head_horn_heel, anvil_head_horn_heel2 = face plate, hardy_hole, hardy_hole_rim); no `Stump`. `Face` (ForgePrompt) centred on the face plate, `BladeMount` 1.35 toward the horn on its top (y 3.46). `build_workshop` stands Model3D on the floor stone (`ANVIL_SINK`). Old body and stump: `Legacy.Anvil_oldBody`. |
| `MaterialService.BladeShine0/1/2` | Metal variants for blades: metalness 0.85 / 0.65 / 0.45 and roughness 0.55 / 0.30 / 0.15 (retuned the same day: a full-metal mirror went dark indoors). [[Sessions/2026-10-22#Shinier swords]] Since 2026-10-23 textured (near-white streaked colour; forged hammer marks / brushed lines / faint lines in normal and roughness), from `Models/Metal/metal_textures.py`; untextured originals in `Legacy.BladeShine_beforeTextures`. [[Sessions/2026-10-23#Metal textures on ingots and blades]] |
| `Shared.SwordMeshCache.shine(look, refinement)` | The BladeShine variant for a blade's average polish (same levels as the cache's meshes); "" unless the look is Metal. Used by `SwordRenderer`, `HiltBenchController`, `EtchPlayback`, `PolishController.paint` (live; on the bench the blade keeps the shine it arrived with until the whole edge is polished, then turns to BladeShine2, 2026-10-23). |
| `SwordRenderer` glint | `glint(part, length)`: an Attachment + ParticleEmitter (sparkles_main) on BladeShine2 blades, one sparkle every 2–4.5 s at a random point along the blade; stopped in `free()`. |
| `build_style_test` plot palette | Last step: `PLOT_ROLE` maps the plot parts' styled colours (roof `544e80`, ridge `3e3a64`, eave `625c92`, timber `462a1a`, slats `573621`, sign `6b4224`, plaster `ebe4d5`, transom `e0ca9e`, noren `1e346f`, vent `291b14`) to Autumn Terracotta, through `set` (originals kept for "off"). Village roots untouched. |

## Refinements 2 (2026-10-23)

[[Sessions/2026-10-23#Refinements 2]] ([[Refinements2]]). Supersedes, above: the gem button and the book button on the left edge (now `MenuGui`'s buttons and a gem counter), "Reset progress … kicks", `Shop.DeliveryWall`, and the crafter's Hire card and 14-stud reach.

| Script / instance | 2026-10-23 |
|---|---|
| `StarterGui.MenuGui`, `StarterPlayerScripts.MenuController` (new) | The HUD menu: see the `MenuGui` row in [[#Client controllers and interface]]. Settings switches fire `Remotes.Setting` (new RemoteEvent) and read the player attributes `Music` / `Sound`; they set `SoundService.Music` / `SoundService.Effects` (new SoundGroups) to 0 or 1. Put new sounds in one of the two groups (the anvil's `Clang` is in Effects). |
| `SmithyCore` | `settings` (`music`, `sound`, on by default) saved and shown as player attributes; `Setting` handled in the live block. `decode` marks `upgrades.Crafter` for a save that already has a crafter. `resetProgress` starts the player over in place (no kick): leave hooks, an empty record under this session's lock (`Profiles.wipe` then `Profiles.load`), fresh data, `onRejoin(fn)` hooks (new), `LoadCharacter`; returns true when done. |
| `PlotService` | `release` clears the player's `Plot` attribute; `SmithyCore.onRejoin(claim)`. |
| `DevTools` / `DevPanel` | After a reset DevTools fires `DevResetProgress` back; DevPanel then destroys and re-clones every StarterGui GUI and every StarterPlayerScripts script but itself and Roblox's own (PlayerModule…). Panel bottom right behind a "Dev" toggle. |
| `Shared/Upgrades` | `Crafter` (Sword Crafter, 1,000, after Anvil2), `DisplayTable3` (900, after DisplayTable2), `DisplayTable4` (1,300, after DisplayTable3). |
| `Shared/Employees` | `HIRE_PRICE` removed. |
| `EmployeeService`, `EmployeeController` | Hire on `Bought_Crafter` (signal, deferred, and at claim); `CrafterPrompt.Enabled` follows the hire once Anvil 2 is bought; remote actions `train` / `make` only, no reach check. The window opens only once hired; `MenuGui.Buttons.Crew` shows then. |
| `GemController` | `Gems` is a counter; `MenuGui.Buttons.Upgrades` toggles the Gem Shop (D-pad left too), `Daily` the daily window, whose Claim is veiled once today's is taken (claimed days ticked from `streak`). |
| `CollectionController`, `DeliveryController` | Viewport cameras made in code when missing. The book opens from `MenuGui.Buttons.Book`. |
| `ShopController` | No "Take back" label: the pill shows only on an empty holder ("For sale"). |
| `TycoonController` | The pad top under your feet tweens 0.12 studs down (`SINK`) and back, on this client only. |
| `DeliveryService` | `openDoor(plot, animate)`: slides `Shop.DeliveryDoor.Slide` by its `OpenOffset` (plot space, 4.5 studs) over 0.8 s on purchase, at once on a claimed plot that has Delivery; sets `Open`. |
| `Plot.Shop.Displays.DisplayTable3/4`, `Plot.Pads.DisplayTable3/4` | Copies of Tables 1 / 2 and their pads, 24 studs along plot x (x +12). `ViaAisle` slots, `Inspect` → their own InspectPoint. |
| `Plot.Pads.Crafter` | A copy of the Anvil 2 pad (same spot, `Workshop`). |
| `Plot.Shop.DeliveryDoor` | No longer a TycoonItem; `Slide` (Door + 2 Battens, PrimaryPart Door, `OpenOffset`) shut at plot z −28; `Noren` ×2 tagged TycoonItem, `Upgrade = Delivery`. `DeliveryWall` → `Legacy.DeliveryWall_removed`. |
| `Plot.Smithy.PolishStation`, `EtchingTable` (+ their pads) | Moved 3 and 6 studs along plot −z: centres z 10.5 and −1.56 (Hilt Bench 22.5), 3-stud gaps. |
| `EtchingTable.Dress` | `PropSwords`: three `SmithyCore.buildSword` models (ForgedSword, `Prop`, no `SwordId`; katana/Obsidian/Eclipse/Gem, wakizashi/Gold/Fracture/Gold, tantō/Blue Steel/Tide/Bronze, all polished), grips at plot z −2.7, x −23.0, heights 5.45 / 4.8 / 4.15; `RackArm` ×2 and `RackPeg` ×6; ink shelf, brackets and jars up 0.9. The part-built wall sword is in `Legacy.EtchingWallSword_beforeProps`. |

- **Hand edits, not in the builders:** the station moves, the prop swords and rack, the door's `Slide`, the removed DeliveryWall and the two new tables were made on the template directly. `build_workshop`'s finishing-bench, display-table and delivery-door sections still build the old layout; rerunning them would undo these.
- **Backups:** `ServerStorage.Legacy.<Name>_beforeRefinements2` (list in the session note), `DeliveryDoor_beforeTease`.

## Refinements 2, second list (2026-10-23)

[[Sessions/2026-10-23#Refinements 2, second list]] ([[Refinements2]]). Supersedes, above: `CommissionController`, the request board (`Shop.<Starter/Upgraded>.Shell.CommissionBoard`, `RequestsPrompt`), the commission visitors, blueprints taught by commissions, the crafter's single `crafter` record, `crafterStatus` and status bubbles, the cart's 3 s roll, the etching counter's `Blank`, and the ore roller's back corner.

| Script / instance | 2026-10-23 |
|---|---|
| `StarterGui.MailGui`, `StarterPlayerScripts.MailController` (new) | `Window` (the Gem Shop's frame, `HidesHud`; `Body` a 516×340 ScrollingFrame), `Dim`, `Templates.Letter` (`Info.Top.Title`/`New`, `Info.Want`, `Info.Reward.Coin`/`Coins`/`Gem`/`Gems`, `HandIn`), `Templates.Next` (`Icon`, `Text`), `Templates.Empty`. Opened by `MenuGui.Buttons.Mail` (LayoutOrder 0, Scroll icon, `Dot`). Lists `Commissions` letters (`offered`/`active`) and `orders`; Hand in → `ItemPicker` of your swords → `Commission("deliver")` / `Order("fill")`. Opening sends `Commission("read")` for new letters. The dot: unread letter, an order not seen this session (orders present at join count as seen), or anything fillable. Closes on B / Q / Backspace / Escape. |
| `ShopService` | No visitors: `visit`, `VISIT_TIME`, `VISIT_SPOT` gone; `offerCommission(owner)` only marks the due letter `offered`. `Commission` remote: `read` (offered → active; funnel 8), `deliver` (offered or active; no blueprint). |
| `Shared/Commissions` | Letters: `line` and `colors` removed. Statuses nil → offered (new) → active (read) → done. |
| `Shared/Upgrades`, `TycoonService` | `Upgrade.blueprint`; `WakizashiBlueprint` (60) and `KatanaBlueprint` (400, after it). `BuyUpgrade` learns `u.blueprint` and pushes. Pads `Plot.Pads.WakizashiBlueprint` / `KatanaBlueprint` at plot (−6, −0.3, 12), `Workshop`. |
| `SmithyCore` | `decode`: no blueprint from a commission; after the commissions, every blueprint upgrade and its blueprint are made to agree (either one known → both). `FUNNEL` 8–9 "Read the first letter", "Delivered the first letter". `crafter` = `{ trained, making, hired = { [id] = { made, since } }, equipped }` (an old single crafter becomes Taise, equipped); `crafterStatus` removed. |
| `Guide` | `board()` and `visitor()` gone; `blueprintPad(plot, id)`. Letter offered → "Open your mail"; active → `craft(plot, c)`, which says "Hand it in from the mail" (no target), "Buy the <pad>" (its pad) or, short of the price, the tantō loop (`craft(plot, nil)`). |
| `DevTools` | Skip tutorial marks the letters done, no blueprints. |
| `Builders.build_shops` (and `Models/Village/build_shops.luau`) | No `commissionBoard` call (the function is still there, unused). |
| `StarterPlayerScripts.HudFocus` (new) | `HidesHud` sources (ScreenGui while Enabled; GuiObject while Visible in an enabled ScreenGui) hide every `HudPart` (ScreenGui → Enabled off, a script's later Enabled kept in `wanted`; GuiObject → parked in its ScreenGui's invisible `HudHold`). Watches `PlayerGui.DescendantAdded`. Attributes set in StarterGui: `HidesHud` on AnvilHud, AnvilPoints, HiltBenchHud, PolishHud, EtchHud, HiltSeatGui, GrindMap, PickerGui.Window/CompactWindow, CollectionGui.Window, GemGui.DailyReward/GemShop, DeliveryGui.Window, MenuGui.ShopWindow/SettingsWindow, MailGui.Window, CrewGui.Window; `HudPart` on HudGui, HotbarGui, GuideGui, GemGui.Gems, MenuGui.Buttons, DeliveryGui.PinnedOrder. `Hotbar` ignores its keys while HotbarGui is off. |
| `StarterGui.CrewGui` (new), `EmployeeController`, `EmployeeService`, `Shared/Employees` | Roster / stats / station pages (`Window` 780×520 with `Fit`, DisplayOrder 4 so the picker draws over it). `Employees.CRAFTERS` (Taise, Haru, Mei, Kenji, Rin), `byId`, `FIRST = "taise"`, `ROLE`, `quality(crafter, level)`; per-crafter forge range, shared `POLISH_SECONDS`. `EmployeeService` poses one R15 per crafter into `ReplicatedStorage.Crafters` (worker and portraits clone them), spawns only the one equipped at Anvil 2, overhead role / name / "Lv. n", no bubbles; `Employee` remote: `train`, `make`, `hire` (coins + gems, blueprint gate), `equip`, `unequip`. Viewport cameras made in code. |
| `DeliveryService` | A courier NPC (Npcs group) between the cart's shafts; leave / return / back-in walks computed from the clock each frame (8 and 6 studs/s, 6-stud turns, lane 55 studs out, fade 1.5 s, return lead ≈26 s); wheels turn with distance; walk-through while moving. The old roll constants are gone; `openDoor` unchanged. |
| `Plot.Shop.DeliveryDoor` | `Slide.Door` 5.0 × 8.0 (over both jambs), Battens 4.6; new `Rail` across the door and its open spot. `OpenOffset` (0, 0, 4.5). |
| `EtchingTable.Dress` | `Blank` removed; `DemoSword` (polished Copper katana, Woven Wind, Gem hilt; ForgedSword, `Prop`, no `SwordId`) face-up on the cradles, which moved to plot z 0.35 / −2.0 and 0.8 toward the front. `EtchPlayback` hides `DemoSword` during the show. |
| `Plot.Smithy.OreRoller` (+ pads) | Left wall in front of the Ingot Rack, facing the room (plot x 17.2–21.95, z −14.95 to −2.6). Pads: OreStand2–6 (14.8, −10.1), Lucky1–3 (14.8, −5.1). |
| `StarterPlayerScripts.SlotMarker` (new), `ShopController`, `RackController` | The holder marker as a module (`ShopHud.Templates.SlotMarker`, bag icon, focus ring, E, 9 studs). RackController: a marker over the Ingot Rack and the Finished Sword Rack (+ when you carry what it takes, bag when it holds something and your hands are empty); `RackPrompt` style Custom. |

- **Hand edits, not in the builders:** the roller, its pads, the door's size and rail and the etching counter. `build_workshop` still builds the old roller corner, `Blank` and door; rerunning those sections would undo them.
- **Backups:** `ServerStorage.Legacy.<Name>_beforeRefinements3` (list in the session note).

## More refinements (2026-10-23)

[[Sessions/2026-10-23#More refinements]]

| Where | What |
|---|---|
| `EmployeeService` | `claim(station)` / `release(station)` / `releaseAll(plot)`: `CrafterBusy` on the station and its enabled prompts off (marked `CrafterOff`) from when the crafter sets off until it's done there; Ingot Rack, a furnace with `Heating` false, Polishing Station, Finished Sword Rack (given back while waiting for room). `releaseAll` after every `oneSword`, in `dismiss` and on error. |
| `ForgeService` | `refreshBoard` keeps each furnace model's `Heating` attribute; `ForgePut` refuses a `CrafterBusy` furnace; `Hook_HeatIngot(plot, materialId, model?)` heats only in `model` when given, and refuses it while something heats there. |
| `RackService`, `RackController` | Store/take refused while the rack is `CrafterBusy`; the rack's `SlotMarker` hides and the picker won't open. |
| `ShopService`, `StreetLife` | Customers walk at 6 (were 10); villagers at 6 (were 6–9). `sendCustomer`: at most More Clients + `Rickshaws.count(plot)` at once, `ctx.ride` beyond More Clients; `runCustomer(plot, ctx)`: a rider arrives with `Rickshaws.arrive`, walks via `front` (just before the bridge), and leaves with `Rickshaws.leave`; `Rickshaws.finish` after an error. |
| `Rickshaws` (new ModuleScript, ServerScriptService) | `count`, `take`, `arrive`, `leave`, `finish`. Clones `ServerStorage.Rickshaw` (attributes `Pull` 4.2, `Seat`, `Step`, `WheelCentre`, `Radius`; parts with `Wheel` turn), builds a puller (happi coat, straw hat), runs plot-space S-curve paths from the bay (`LANE` 9, `RUN` 70, 8 studs/s, `FADE` 1.2 s), rider anchored with the R15 sit animation (`SIT_LIFT` 1.4). |
| `Plot.Parking.Bay1–3`, `Plot.Pads.Parking1–3`, `ServerStorage.Rickshaw` | Built by `Models/Village/build_parking.luau` (rerun replaces them). Bays are TycoonItems of `Parking1–3`; the slab is `Slab`. |
| `Shared/Upgrades` | `Parking1–3` (Rickshaw Bay 1–3: 500 / 1,500 / 4,000, after Display Table 1); blueprint pads named Wakizashi Sword / Katana Sword. |
| `Shared/Deliveries`, `DeliveryService`, `DeliveryController` | `PAY` 0.8, `CAPACITY` {6, 9, 12, 15}, `SPECIAL_MAX` 4, `mismatch(o, sword)` (bulk: any sword), bulk titles "N× Any sword", bulk gems 1 + count ÷ 3, decode keeps up to 15. Offer cards "80% value"; crates sized to fit up to 15. |
| `ReplicatedStorage.SwordParts.Ingot`, Ingot Rack `Slots` | The ingot MeshPart (Model asset 73668137097210; `Models/Stations/Ingot`). The 12 rack slots are MeshParts of it; `SmithyCore.buildIngot` and `ItemPicker`'s ingot art clone it. |
| `ServerStorage.Tests.SaveSpec` | 73 checks: + 0.8× delivery pay, bulk vs special fit, a 15-sword order through JSON. |


## Urgency phase 1 (2026-10-23)

[[Sessions/2026-10-23#Urgency phase 1: cues, crew status, 45 s offers]].

| Where | What |
|---|---|
| `StarterPlayerScripts.Cues` (new ModuleScript) | `Cues.play(name)`: plays `SoundService.Effects.Cues[name]`, at most once per `GAP` 1.5 s per name. |
| `SoundService.Effects.Cues` (new Folder) | Sounds `FurnaceReady` (9126073001), `Offer` (9113421646, region 0–0.9 s), `Sale` (9113848780), `CartBack` (9120924459, region 0–1.4 s); `SoundGroup` Effects. |
| `ForgeController` | `showReady(part, fresh)`: your slot's `Ready` → Neon ingot, `ForgeTimers.AlwaysOnTop` while any of your slots there is ready, `FurnaceReady` when it just turned ready. |
| `ShopService` | `OFFER_TIMEOUT` 45; `CARD_GAP` 1.5 with `closedAt[owner]` in `askOwner`. |
| `ShopController`, `StarterGui.OfferPing` (new BillboardGui) | Offer: `Offer` cue unless the same NPC as the last (`rang`); `OfferPing` (Ring with `Pop` UIScale and Coin, `Time`; AlwaysOnTop, MaxDistance 400) on the bubble's adornee while the camera is beyond `OfferBubble.MaxDistance` − 2; `Sale` cue after an accepted `RespondOffer`. |
| `DeliveryController` | `tick`: `CartBack` when the active order's phase turns "back" from "going"/"returning" (`lastPhase`; not on join). |
| `EmployeeService` | `setStatus(plot, s)` → plot attribute `CrafterStatus`: fetching / heating / forging / polishing / racking, or noShape / noRack / rackFull / noIngots / furnace / polish; nil when no crafter works. |
| `EmployeeController`, `CrewGui.Window.Stats.Panel.Status` (new), `MenuGui.Buttons.Crew.Dot` (new, a copy of Daily's) | `STATUS` / `WAITING` texts; the equipped card (renamed `Working`) shows the status in `Trait`, amber while waiting; a 0.5 s loop follows `CrafterStatus` and sets the dot. |
| `Guide` | `overlapTip(plot)` before the other goals (`OVERLAP_UNTIL` 10, session flag `overlapDone`); `furnaces()` skips a `CrafterBusy` furnace as free. |

## Urgency phase 2 (2026-10-23)

[[Sessions/2026-10-23#Urgency phase 2: the crafter's furnace and your forgotten ingot]].

| Where | What |
|---|---|
| `Shared/Upgrades` | `after` may be a list: `Anvil2` after `{ IngotRack, Furnace2, SwordRack }`. |
| `TycoonService` | `available(plot, u)`: not bought, and every id in `after` (one, a list or none) bought. Restoring saved upgrades doesn't check `after`. |
| `ForgeService` | `FORGOTTEN` 10 s; `forgotten(slot)` (a player's ingot ready that long), `handBack(slot)` (into the owner's hands, hot, with a notice); new `ServerStorage.Hook_ForgottenFurnace(plot) -> furnace?`; `Hook_HeatIngot(plot, materialId, model)` hands back a forgotten ingot in `model` first. |
| `EmployeeService` | With no free furnace, `ForgottenFurnace:Invoke(plot)` picks one; it is claimed and walked to like any other. |
| `ServerStorage.Legacy.*_beforeUrgency2` | Backups of the four scripts above. |
| `RackService` | (2026-10-23) `fullSign(rack, full)`: `SwordRack.Plinth.FullSign` BillboardGui "Rack Full!" while `#swords >= SWORD_CAP`, called from `showSwords`. |

## Racks split, one ingot model, NPC walking (2026-10-23)

[[Sessions/2026-10-23#Racks split, one ingot model, NPC walking, no offer ping]].

| Where | What |
|---|---|
| `RackController` | `cards(which, onRack, store)`; `openRack` picks store (`canStore`, the marker's +) or take; `hitBox(ray, cf, size)` ray–box test and an `InputBegan` click / tap handler that takes the nearest hit item within `REACH` 12. |
| `RackService` | `INGOT_CAP` 6; `showIngots` sets slot `IngotId`, `showSwords` sets model `SwordId`. |
| `ReplicatedStorage.SwordParts.Ingot` | The ore box's ingot (mesh 82252952198503, 2.3 × 0.75 × 1.2); `IngotRack.Slots.Slot1–6` are copies, two per shelf. |
| `SmithyCore.buildIngot` | Handle at the template's size; Grip `CFrame.new(0, 0.5, 0.25)`. |
| `NpcWalk` (new ModuleScript, ServerScriptService) | `to(npc, target, fallback?)` (path, `NEXT_AT` 1.5, `ARRIVED` 1, re-issues MoveTo every 7 s, gives up when stuck), `face(npc, at)` (0.3 s ease), `animate(hum, walk)` (`AdjustSpeed(speed / 16)`). |
| `EmployeeService` | `walkTo` / `face` / walk animation via `NpcWalk`. |
| `ShopService` | Walk animation via `NpcWalk`; inside the shop `NpcWalk.to(inspect, route)` and back to EntryPoint; `NpcWalk.face` at the holder. |
| `ShopController` | Offer ping removed; `StarterGui.OfferPing` → `ServerStorage.Legacy.OfferPing_removed`. |
| `RackController` (later 2026-10-23) | One `SlotMarker` per `Slots.Slot<k>` on both racks (`itemIn(k)` reads `IngotId` / `RackSword<k>.SwordId`); the bag takes, the + opens `openRack(true)`; E: `openRack(canStore(which))`, first matching marker focused. [[Sessions/2026-10-23#Ingot grip, a marker per rack slot, polishing pose]] |
| `EmployeeService.scrub(c, seconds)` | Polishing: `ANIM.polish` = R15 toolnone (507768375), looped, and `RightShoulder.C0` tweened ±0.3 rad (yaw) every 0.45 s. |
| `SmithyCore.buildIngot` (later 2026-10-23) | Grip `CFrame.new(0, -0.3, 0.35)` (measured in Play). |
| `ItemPicker.artModel` (later 2026-10-23) | A card's etch is built deferred, spread (`SwordMeshCache.etch(..., true)`), one at a time (`etching` flag); released at once if the card is gone. [[Sessions/2026-10-23#Etching Table window no longer freezes]] |
| `PolishController`, `EtchingTableController`, `DeliveryController`, `MailController` (later 2026-10-23) | Pickers skip ineligible swords (`continue`) instead of `locked` cards; empty titles "No swords to polish" / "to etch" / "No swords fit". [[Sessions/2026-10-23#Pickers show only swords you can use]] |

## Sword-shaping prototype (2026-10-23, experiment)

[[Sessions/2026-10-23#Sword-shaping prototype (experiment)]], [[Prototypes/sword-shaping/README]]. Not part of the game's crafting; nothing in production requires these.

| Where | What |
|---|---|
| `ReplicatedStorage.Prototypes.ShapingRules` (new) | Pure. `CONFIG` (strength, radius, limits, blankWidth, base/tip locks, `perfect` band, tolerance, flag, timing); `new(targetParams)`, `reset`, `preset`, `strike(s, u, dir)`, `score(s, widths?)` → score, worst station, signed cm; `params(s, target, widths?, out?)` → BladeCore params with edge = spine − width. |
| `ReplicatedStorage.Prototypes.ShapingPrototype` (new) | Client. `start()`; `current.stop`. Builds `Workspace.ShapingPrototype` at y 600 (client only) with a `BladeView` katana, tang, tongs, hammer and anvil bed; the face-on diagram GUI; holds the camera Scriptable, sets Humanoid WalkSpeed/Jump to 0 and switches every other PlayerGui LayerCollector off, all put back on Exit. `workspace.ShapingPrototype.Inspect` (BindableFunction) returns the live state: the MCP and command bar have their own require cache. |
| `ServerStorage.Tests.ShapingRulesSpec` (new) | 19 checks. |
| `StarterPlayerScripts.DevPanel` | "Shaping prototype" button (Studio only) calls `ShapingPrototype.start()`. |

- **This place's PlayerModule has no `GetControls`** (it is the input-context version, in `StarterPlayer.PlayerModule`, not `PlayerScripts`): hold a character still through its Humanoid instead.
- Studio's `user_mouse_input` coordinates are GUI space (the top bar inset is not included), unlike screenshots.

## Metal textures (2026-10-23)

| Area | Detail |
|---|---|
| `MaterialService.IngotMetal` | Metal variant, 4 studs per tile: near-white mottled colour, hammer-dimple normal, mottled roughness about 0.45, BladeShine1's metalness. Set as `MaterialVariant` on `ReplicatedStorage.SwordParts.Ingot` and on the plot's Ingot Rack slots and ore stand `Ore` parts, so every clone has it (held ingot, ore box). It only shows while the part's Material is Metal: Stone (Slate), Obsidian (Glass), hot (SmoothPlastic) and item cards (SmoothPlastic) keep their own look. No script change. |
| `Models/Metal/metal_textures.py` | Makes the ingot and blade maps (numpy, fixed seed, 1024 px over 4 studs). Run `python -I metal_textures.py <out>`, serve the folder on localhost, upload with Studio MCP `upload_image`. |

- Roblox projects a MaterialVariant onto these meshes without UVs (checked on the ingot and a baked katana blade), so the blade meshes need no UVs for it.

### New metals (2026-10-23)

| Area | Detail |
|---|---|
| `Shared.Materials` (new metals, same day) | 18 metals: + Pewter (Common), Rose Gold (Uncommon), Jade (Rare, Glass), Dragonsteel (Legendary), Watermelon (new **Secret** rarity, ×25, 0.1%; Common takes 59.9%). Optional `texture` (MaterialVariant prefix) and `tint` (part colour; white for Watermelon, whose maps carry its colours). `Materials.dressIngot(part, m)` sets colour, look and `IngotMetal` / `<texture>Ingot`; used by `SmithyCore.buildIngot` (cold), `ForgeService` stand paint, `RackService` slots and `OreBoxShow`. Item cards stay plain. |
| `SwordMeshCache.shine(material, refinement)` | Now takes the material (was its look): `<texture>Blade` for a textured metal at every polish level, else BladeShine0/1/2 on Metal, else "". Blade sites (`SwordRenderer`, `HiltBenchController`, `PolishController`, `EtchPlayback`) colour the blade `tint or color`. The anvil's forging blade is unchanged (plain look and colour). |
| `MaterialService.DragonIngot/DragonBlade`, `WatermelonIngot/WatermelonBlade` | Dragon: Metal, scales tinted by Dragonsteel's red, 4 / 1.5 studs per tile, BladeShine1's metalness. Watermelon: Plastic, rind stripes (ingot, 4) and pink flesh with seeds (blade, 2). Maps from `metal_textures.py dragon watermelon`. `Etches.MATERIAL_FLAME` has all five. Backups `Legacy.*_beforeNewMetals` (11 scripts). |
| `Shared.Etches.CLEAR` (clear etch, same day) | White, a body colour no pattern uses. `colorsFor` returns it for a textured metal, so the etch keeps its texture visible (Allen: "ideally the texture stays visible"); it is stored and saved like any body. `BladeEtch.build` then makes the band faces only (Flame; not baked, built live); `EtchCanvas` paints a see-through ground (alpha from marks and halo) and `EtchCanvas:wear(part)` sets the texture and Transparency 0.02 (at 0 a MeshPart ignores texture alpha). `SwordMeshCache.etchBody` leaves CLEAR as is; `EtchPlayback` doesn't tint a clear band body. Dragonsteel's etch colour is gold. Backups `Legacy.*_beforeClearEtch` (Etches, SwordMeshCache, BladeEtch, EtchCanvas, EtchPlayback). |
| `Shared.Materials` (30 metals, same day) | + Black Iron (Common), Brass, Amber (Glass), Marble (Uncommon), Amethyst, Ruby (Glass), Frost Iron (Ice) (Rare), Sapphire (Glass), Magma Steel (CrackedLava) (Epic), Sunsteel (Neon) (Legendary), Cardboard, Rubber Duck (Secret). Tiers 5 / 6 / 6 / 5 / 5 / 3. Non-Metal looks take no variant and no polish shine. Every metal has an `Etches.MATERIAL_FLAME`. Backups `Legacy.Materials_beforeThirtyMetals`, `Legacy.Etches_beforeThirtyMetals`. |
| `CollectionController` rows (lazy book, same day) | Every metal gets its row and name at once (the count covers all 90), but only rows in view plus `MARGIN` (1) each side hold their three ViewportFrame entries: `refresh()` on `CanvasPosition` builds rows that come in and takes down far ones, freeing their blade meshes (each row keeps its own `meshes`). About 12–18 viewports at a time instead of 90. `RARITY` in CollectionController and Hotbar and `CHIP` in ItemPicker now have Secret (red). Backups `Legacy.*_beforeLazyBook`. |
| `CollectionController` (ingot book, same day; replaces the lazy rows above) | One card per metal (Allen: "just have every material you've discovered. we can just use the ingot"): `Materials.list` in order, 4 to a row, 104 × 128. Collected: `Materials.ICON[id]` image and name on the rarity colour; not yet: the same image in dark `ImageColor3` (a silhouette), dimmed colour, "???". Every card has `Halftone`: the staggered dot tile `rbxassetid://106477061422613` (`ScaleType.Tile`, 5.5 px: `TileSize` as a fraction of the image, since offsets are whole pixels), rotated 60°, 167 × 205 so it still covers the card, clipped by `Entry.ClipsDescendants` (to the rectangle; the rounded corners aren't clipped), black at 84% transparency. Earlier tries: the "from centre" image (dots too large), 78% and 88%, a sparse tile, the Hotbar's corner piece. |
| `Shared.Materials.ICON` | Metal id → ingot image (`rbxassetid://…`), 256 px PNGs with alpha: Studio photos of the dressed ingot on a green (magenta for Jade, Watermelon) wall, cut out by `Models/Metal/ingot_icons.py` (fixed crop, chroma key, despill, premultiplied shrink). A new metal or look needs a new photo. Backup `Legacy.Materials_beforeIngotBook`. |

### Western swords and automatic hilts (2026-10-23)

[[Sessions/2026-10-23#Western swords and automatic hilts]]. Backups: `ServerStorage.Legacy.<Name>_beforeWestern` for every script and module below.

| Area | Detail |
|---|---|
| `Shared.BladeData` | Regenerated from `Prototypes/tanto-forge` with `longsword`, `falchion`, `gladius` after the katana (Japanese sections unchanged). New profile field `doubleEdged` (longsword, gladius). [[Development/Blade Profile Authoring#Western blades (2026-10-23)]] |
| `Shared.Blueprints` | `PRICING` adds `hilt` (the hilt shape, `SwordParts.<hilt>Hilt`) to every blueprint: `Katana` for the three Japanese ones, `Longsword` / `Falchion` / `Gladius`. Western: tradition `Western`, stars 3 / 4 / 4, base price 160 / 220 / 280 (placeholders). |
| `Shared.Hilts` | Tiers lost `tradition`, and `fits` is gone. New: `best(completed)` (the highest-bonus unlocked tier), `template(blueprintId)` (the blueprint's hilt model, katana for unknown ids), `span(blueprintId)` → grip length, `BladeOffset`, `Back` (grip centre to the hilt's back end; the katana has no `Back` attribute, so grip/2 + 0.06). `dress(hilt, etch?, blueprintId?)`: a western shape dresses `Grip` = grip, `Guard` = guard, `Pommel` = pommel (or guard) and ignores etch guards and `tsuba`; the katana path is unchanged. |
| `ReplicatedStorage.SwordParts.LongswordHilt / FalchionHilt / GladiusHilt` (new) | Grip, Guard, Pommel MeshParts in the Handle frame (placed with the same transform that maps the katana hilt's upload onto `KatanaHilt`), properties copied from `KatanaHilt.Ito`. Attributes `GripLength` / `BladeOffset` / `Back`: 1.15 / 0.70 / 0.854, 0.72 / 0.44 / 0.565, 0.56 / 0.42 / 0.523; `SourceAsset` 81774722638611 / 76674556242261 / 92089099219593. Built in Blender from `Models/Hilts/build_western_hilts.py` (`WesternHilts.blend`, `*HiltGame.fbx`, review sheets in `Models/Hilts/review/western-hilts-*.png`), uploaded through Open Cloud. 2,952 / 1,672 / 1,760 triangles. |
| `Shared.BladeView` | `onBevel`: on a `doubleEdged` blade every face is a bevel, for the finish colours and for `raycast`, so the whole blade polishes bright and grinds from either side. |
| `Shared.Upgrades`, `Workspace.Plot.Pads` | `LongswordBlueprint` (1,000, after `KatanaBlueprint`) → `FalchionBlueprint` (2,000) → `GladiusBlueprint` (3,500); pads are clones of the Katana pad on the same spot. |
| `Shared.Employees` | `TRAIN_PRICE` adds longsword 2,500, falchion 4,000, gladius 6,000. |
| `SmithService.AttachHilt(bladeId, goodTaps)` | Was `(bladeId, hiltId, goodTaps)`: the server fits `Hilts.best(d.completed)`, with no tradition check. |
| `SmithyCore.buildSword` | Handle size and the `BladeOffset` attribute come from `Hilts.span(blueprintId)`; `dressHilt` passes the blueprint. The module-level `HILT_TEMPLATE` / `GRIP_LENGTH` / `BLADE_OFFSET` are gone. |
| `HiltBenchController` | No hilt picker: picking a blade seats `Hilts.best(state.completed)` in its shape. Seat view spans from `Hilts.span`. |
| `ItemPicker`, `EtchPlayback` | Sword art and the etch show dress the blueprint's hilt and frame it with `Hilts.span`. |
| `EmployeeService` | `bestHilt` replaced by `Hilts.best(d.completed)`. |
| `ReplicatedStorage.SwordMeshes` | 54 bakes: + 9 per western blueprint (`B`, `O`, Flame `E` × levels 0–2). |
| Tests | `ForgeCheckSpec` expects six blueprints and checks that each blueprint's hilt shape exists. Passing: ForgeCheckSpec, SaveSpec 73/73, AnvilSelfCheck, SwordMeshSpec 218/218. `EtchingSpec` is 35/36: "the demo tray is hidden during the show" fails because the Etching Table no longer has `Tray`/`Blank` parts (removed earlier the same day), not because of this change. |

### Shop take-back prompt on the holder (2026-10-23)

| Area | Detail |
|---|---|
| `ShopService.place` / `clearSlot` | `TakeBackPrompt` (E, `HoldDuration` 0, was 0.5) is parented to the holder part (was the sword's Handle) and destroyed in `clearSlot`. [[Sessions/2026-10-23#Taking a sword off a shop holder]] |
| `ShopController.bindSlot` | `findTakeBack` reads `part.TakeBackPrompt` (was the nearest Handle's prompt within 6 studs); `part.ChildAdded` refreshes the marker when the prompt arrives. A click on the bag calls `DisplaySword(slotIndex, nil)` (it pressed the prompt, which can't fire beyond its 6 studs while the marker shows from 9). |
| `ShopService` `DisplaySword` | With no `swordId` on a holder holding your own sword: take it back (same plot, `REACH` and `allowCall` checks). |
| `DevTools` / `DevPanel` Give sword (2026-10-23) | Studio only. Dev → **Give sword** opens a picker left of the buttons: Blade (`Blueprints.order`), Metal (`Materials.list`), Hilt (`Hilts.list`), Etch (None + `Etches.list`), Finish (unpolished / polished), each stepped with ◀ ▶; **Give & equip** fires `Remotes.DevGiveSword(spec)`. The server checks each id, builds the sword as `DevGiveSwords` does (100% grade; polished = every station refined and `polished`; etch colours from `Etches.colorsFor`), gives it and equips it. Backups `Legacy.DevTools_beforeGiveSword`, `Legacy.DevPanel_beforeGiveSword`. |
| `DevTools` / `DevPanel` Wipe inventory (2026-10-23) | Studio only. Dev → **Wipe inventory** fires `Remotes.DevWipeInventory`; the server clears `ingots`, `blades` and `swords`, destroys the player's Tools with a `SwordId` or `IngotId` (backpack and character) and pushes. Racks, holders and currencies untouched. Backups `Legacy.DevTools_beforeWipeInventory`, `Legacy.DevPanel_beforeWipeInventory`. |
| `Etches.colorsFor` (every metal see-through, same day) | Returns `Etches.CLEAR` for every metal, and a line colour that contrasts with the bare metal: `contrast(material.color)` (luminance ≥ 0.42 → 60% toward black, else 60% toward white), with `FLAME_OVERRIDE` for Dragonsteel (gold) and Watermelon (green); the old vivid `MATERIAL_FLAME` table is kept but unused. `SmithyCore.buildSword` takes both colours from `colorsFor` (not the save), so older etched swords redraw the new way. `EtchCanvas` doesn't whiten a clear canvas's marks (dark lines stay dark). `Hilts.dress` gives an etch guard's `Core` dark iron when the body is CLEAR (it went white on Dragonsteel / Watermelon before). `bake_sword_meshes` now bakes the band-only Flame skin `E|<blade>|<level>|Flame|ffffff` (9 shapes); the old dark-body bakes stay in `SwordMeshes`, unused. Backups `Legacy.*_beforeClearAll`. |

### Smelting furnace model (2026-10-23)

| Area | Detail |
|---|---|
| `Plot.Smithy.Forge` / `Forge2` `.Model3D` | Clone of `ServerStorage.Buildings3D.japanese_smelting_furnace` (attribute `SourceModel`), `ScaleTo` 2.445, turned 180° (arch faces +Z), bottom centre on the old spot (so `build_workshop`'s `bottomCentre(m.Model3D)` still places it). No separate `Door` model any more. Vents `vent_glow_*` renamed `DoorWindow` (attribute `Vent` keeps the old name); `chamber_floor_glow` Neon. [[Sessions/2026-10-23#Smelting furnace replaces the furnace model]] |
| `ForgeService` | `Forge.windows`: every `DoorWindow` BasePart in the furnace, collected in `setupForge`; `setWindow` lights them all. `SLOT_OFFSETS` `(0, 1.12, 0.9)`: the ingot sits inside, behind the door. Backups `Legacy.ForgeService_beforeSmeltingFurnace`, `Legacy.Forge_beforeSmeltingFurnace`. |
| Blue Steel's decal texture (same day) | `Materials` Blue Steel has `texture = "BlueSteel"`, `tint` white: `MaterialService.BlueSteelIngot` (4 studs per tile, IngotMetal's normal and roughness) and `BlueSteelBlade` (3, BladeShine1's), both with the decal from Allen's `Workspace["bluesteel block"]` (`rbxassetid://23053082`) as ColorMap and BladeShine1's metalness. Like every textured metal its blade has one look at every polish level. New book image `98295780323344`. `ingot_icons.py` now crops around the capture's centre (the Studio window's width changes). Backup `Legacy.Materials_beforeBlueSteelDecal`. |
| Starmetal and Rubber Duck textures (same day) | From Allen's `Art/Textures/` images. Starmetal: `galaxy.jpg`, square crop mirrored 2×2 (seamless) then shifted a quarter so a swirl is mid-tile (`rbxassetid://139779286588627`), `StarmetalIngot` (Metal, 5 studs per tile) / `StarmetalBlade` (6) on the shared metal normal, roughness and metalness. Rubber Duck: `rubber ducky.png` tiled 2×4 to a 512 square (`119018583374134`), `RubberDuckIngot` (Rubber, 4) / `RubberDuckBlade` (3), no other maps. Both `tint` white. New book images: Starmetal `86318088873854`, Rubber Duck `79110196949110`. Backup `Legacy.Materials_beforeArtTextures`. |
| Etch ink outline (same day) | On a see-through etch every band and mark has a dark ink outline (Allen: the etch colours "blend in with the texture", Falling Stars' thin trails looked "misaligned"). `EtchCanvas` (stroked patterns): the halo is ink `(14, 10, 10)` at up to 95% alpha instead of the accent, and the mark core is whitened again (`CORE`). `BladeEtch.build` (Flame): with a CLEAR body it adds an ink strip `INK_W` = 0.045 of the width along the band's wavy edge (a third colour kind `"i"`, which the part's Color can't lighten). `Etches.colorsFor` is back to the vivid `MATERIAL_FLAME` colours for every pattern (the contrast colours and FLAME_OVERRIDE are gone). Flame skins re-baked. Backups `Legacy.*_beforeInkOutline`. |

## Refinements 3 (2026-10-24)

[[Sessions/2026-10-24#Refinements 3]] ([[Refinements3]]). Supersedes, above: `build_workshop`'s shelf `CRADLE` 1.45, the sale notice naming the friend, the counter (`Shop.Interior`) living only in Legacy (it is back as `Shop.CashierCounter`), the Junction slabs in `build_simple`'s road surfacing (parked in Legacy; `build_simple` no longer builds one), `MailGui.Templates.Next`, the courier's lane 55 studs out, the crew window's crafter-only pages, `setStatus(plot, s)` writing only `CrafterStatus` and the dot following every wait, `SWORD_CAP` in the "Rack Full!" sign, `scrub` tweening `RightShoulder.C0`, a marker on every rack slot (a locked one gets none), and 30 metals (now 31; Epic has 6).

| Script / instance | 2026-10-24 |
|---|---|
| `ForgeService` | Spinning is free: `refreshLever` is `rollPrompt.Enabled = not r.rolling`. A pull runs `collectWaiting` (every unlocked stand's ore into your hands, quietly, until they're full, then one push), clears every rolled stand, then rolls; what didn't fit is rolled over. `takeOre(stand, player, quiet)` is the Collect prompt's code (cold ingot, marks it discovered, the NEW card). Both luck lines use `Upgrades.luck(plot)`. New `ServerStorage.Hook_CollectOre(plot, player)` (BindableFunction, made at runtime): false while that box rolls, or when ore still waits on Slots 2–6 after collecting ("Your hands are full (6 ingots). Use some first"), else true. The comment by the furnace prompt ("The prompt itself only opens the window") is out of date (see ForgeController). |
| `TycoonService` | `BuyUpgrade` charges `Upgrades.price(plot, u)`. Merge branch (`u.merge`): `Hook_CollectOre` first (false → nothing happens), `data.merges` + 1, the plot's `Merges` attribute, then every Ore Slot's `Bought_` flag and `d.upgrades` entry cleared and `refresh`; nothing is charged and nothing else resets. `available()`: once `Merges > 0`, "after OreStand2" counts as met for upgrades that aren't Ore Slots (Ingot Rack, Lucky Roller I, Delivery Cart). The merge pad's label reads "Luck x<factor after this merge>", the others the plot's price. `onPrepare` sets `Merges` before restoring. Buying `SwordRack2` fires `Hook_RackChanged` after `refresh`, so "Rack Full!" goes out. |
| `TycoonController` | The button label is set every Heartbeat: "Merge" on `MergeSlots`, else "Buy" ("(Y)" on gamepad). `MERGE_WAIT` 1 s: for a second after the pad under you becomes `MergeSlots`, the button is hidden and `buy()` does nothing, so mashing Buy through Ore Slot 6 can't merge; `bindPad(top ~= nil)` keeps Y on the pad meanwhile. |
| `Guide`, `GemController` | Guide: `tutorialDone(plot)` = `Bought_OreStand2` or `Merges > 0`, for the overlap tip, the "Buy Ore Slot 2" goal and the "Workshop open!" check, which never replays after a merge. GemController: the daily window's tutorial wait accepts `Merges > 0`; its comments say House. |
| `Shared/Upgrades` | `Upgrade.merge`; `MergeSlots` ("Merge Ore Slots", 0, after OreStand6, `merge = true`). `MERGE_LUCK` 0.5, `MERGE_PRICE` 1.5, `merges(plot)` (plot attribute `Merges`), `mergeFactor(n)` = 1 + 0.5n, `luck(plot)` = `LUCK[Lucky tier + 1]` × `mergeFactor`, `price(plot, u)` (Ore Slots `floor(price × 1.5^merges)`, the rest unchanged). `openSlots(slots)`: the slot parts no unbought upgrade locks (`Locked`). New: `SwordRack2` (Finished Sword Rack 2, 600, after SwordRack), `Stocker` (2,000, after Crafter), `Cashier` (3,000, after UpgradedStore), `Promoter` (Shop Promoter, 1,500, after DisplayTable1), `EtchingTable2` (2,500, after EtchingTable and SwordRack), `Etcher` (Sword Etcher, 2,000, after EtchingTable2). Crew prices are placeholders. |
| `Shared/Materials` | `roll`: luck multiplies the rarer odds from the rarest down, each tier capped by what the rarer ones left while every tier below keeps at least `MIN_COMMON` (10%). Identical below luck ~2.24 (above it Common used to go negative). At Lucky III, Legendary is 1.7%, then 2.6 / 3.5 / 4.4% after 1 / 2 / 3 merges. `alpha: number?` on the type; new **Air** after Magma Steel (Epic, (200, 232, 255), Glass, `alpha` 0.45): 31 metals. Rainbow Alloy: `texture = "Rainbow"`, tint white. Book images: Air `129317614850365`, Rainbow Alloy `92696613731822`. |
| `MaterialService.RainbowIngot`, `RainbowBlade` | Metal, `StudsPerTile` 2.3 / 7 (the ingot red in the middle, violet at the ends; the katana red at the hilt to violet at the tip on both faces). ColorMap `86305492403018`, normal `88693148403940`, roughness `116211403159266`, Starmetal's metalness `129497976100657`. The colour map is an original from `Models/Metal/metal_textures.py` `rainbow`, red → violet → red because Studio mirrors a blade's texture onto its back face; Allen's `rainbow.webp` (a watermarked stock preview) is unused. `ingot_icons.py` takes a `[green, magenta]` photo pair (each pixel from the photo whose wall it looks least like). Earlier test uploads are unused. |
| `Shared/Etches` | `MATERIAL_FLAME.Air` = (150, 220, 255). |
| `SwordRenderer`, `HiltBenchController`, `PolishController`, `EtchPlayback` | After the shine line, the blade's `Transparency = material.alpha or 0`, so an Air blade is about 45% see-through everywhere (etched too). The ingot stays solid pale glass. |
| `SmithyCore` | `merges` (0 in `fresh`, in `encode`; `decode` floors it, never below 0) and `staff` = `{ [role] = { since, count, setting } }` (`{}` in `fresh`, in `publicState`; `encode` copies each record; `decode` keeps known roles, cleans `since` and `count`, keeps a setting only if it is a string or a finite number). Both additive, no version bump. `SmithyCore.encodeSword` exported. `bladeName`: no " (Polished)". `publicState` still sends `orderAt`, which nothing reads now. |
| `ServerStorage.Tests.SaveSpec` | 85 checks: + merges round trip and repairs, a save from before merges, merge prices and luck, luck 3 and 7 still roll every rarity, staff round trip and bad roles and settings, the cashier rule, orders 3–10 minutes apart with a gap each. |
| `Shared/Orders` | `EVERY` → `GAP` = {180, 600}. `refill(…, gap)` takes the gap as a new last argument and applies it only when the clock starts or an order arrives, so each order gets its own; catch-up orders after a long absence share one (ponytail). |
| `ShopService` | `refillOrders` passes `rng:NextInteger(Orders.GAP[1], Orders.GAP[2])`. The sale notice is "Sold <`swordName`> for <n> coins" (no buyer, commas from a local `commas()`, a copy of `UiFx.commas`); the "is back in your inventory" and "is on display" notices are gone. Slot `reserved`: `clearSlot` clears it and `DisplaySword` refuses a reserved holder. `ServerStorage.Hook_Stock` (BindableFunction): `"reserve"` (holder Occupied, its `HolderPrompt` off so the + hides; returns the slot index, the inspect spot and the holder's position), `"place"` (places the sword, pushes), `"cancel"`. Cashier: `staffOf(player, role)`; `cashierFor(plot, owner)` gives his record and NPC only when he's hired, his NPC is on the plot and `sold >= 2`. Then customers don't wait for your card: he faces the customer, waits `perk("cashier", count)` and sells when `Employees.cashierSells`, through the player's accept branch (coins, sold, reputation, notice, `clearSlot`; his count + 1). A decline goes through `Customers.raise` and he checks each raise; with no NPC the card comes back. He answers every waiting customer at once, turning to each in turn (ponytail). Promoter: the walk-in gap × `perk("promoter", count)`, one more customer at once in `sendCustomer`, his count + 1 per customer reaching the EntryPoint (rickshaw riders too). |
| `MailController`, `MailGui` | `nextIn`, the "New order in m:ss" row and its countdown loop are gone; `Templates.Next` deleted. An empty inbox shows `Templates.Empty` ("No mail"). |
| `MenuGui`, `MenuController` | Buttons: `BackgroundTransparency` 1, each `UIStroke` kept but off; MenuController turns it on, amber, only for the gamepad's selection. Icons 30 → 38 px. `Upgrades.Icon` is House (`rbxassetid://15403056677`). |
| `HudGui`, `GemGui.Gems` | `Coins` and `Gems`: `BackgroundTransparency` 1, the frame's `UIStroke` deleted, `Row.Count` outlined (`UIStroke` Contextual, (43, 28, 19), 2). `HudGui.Reputation.Visible` = false; `Hud` is unchanged and still updates it. "Rank N" stays in the Deliveries window. |
| `HotbarGui`, `Hotbar` | `Templates.Slot.Count.Text` "": the count shows from 2×. New `Templates.Slot.Metal` TextLabel (bottom, 14 px, GothamSSm Bold, scaled 7–12, black stroke 1.5). A sword's title is `Blueprints.get(BlueprintId).name`, raised 11 px, with the metal under it in its rarity colour lightened 45% toward white. Ingots keep their names. |
| `DeliveryController` | An accepted, unsent order shows the packing page in place of the Orders list (the trip tracker stays below). `chosen` is local, kept per order id (`chosenFor`), and pruned on every SmithState push of swords that left or no longer fit, so the pill, "Packing n/m" and the page agree. Tap a card to pack it, a slot to take it back (only the art moves). Auto-Fill packs cheapest first; Cancel Order sends `cancel` (half-packed crates from old saves come back); Fill the Crate is veiled until every slot is full, then sends `dispatch` with the chosen ids. The page rebuilds only when the order id, packed count or fitting swords change. Pin is a session-only toggle (packing page and active order card); the pill shows only while pinned and counts chosen swords. Gamepad selects the first card. Removed: `pack()`, the ItemPicker packing flow, the old Cancel / Pack / Send buttons, `placePin`, `pin.UIStroke`. |
| `DeliveryService`, `Shared/Deliveries` | No `"pack"` action. `dispatch` takes `{ swordId }`: as many as the free slots, each yours, unique and fitting, all checked before any is taken (else nil, nothing taken). `LANE` 47 (8 short of the street's middle, as for every lot now). Deliveries: two comments only. |
| `DeliveryGui` | `Window.Body.Packing` (scrolling): `Top.Chips` (Kind, Town, Pin), `Top.Pay`, `Need`, `Hint`, `Slots` (64 px grid), `Divider`, `Swords` (130×150 grid), `Buttons` AutoFill / Cancel / Fill. `Templates.Slot`, `Templates.Sword` (PickerGui's CompactCard with a coin and price row), `Templates.Pin`. Help lines 2 and 4 reworded. `PinnedOrder`: Position (0, 12, 0.5, −104), `BackgroundTransparency` 1, no frame stroke, `Row.Label` outlined like the coins. |
| `ForgeController` | Holding a cold ingot (a Tool with `IngotId` and no `Hot`), E puts it in through `ForgePut` after the "Take out" and "Forge is full" checks: no picker, no toast. Empty hands, a hot ingot or a sword still open the picker. |
| `AnvilController` | A `picked` flag and `pickerClosed()` as both pickers' `closed`: closing one (X, B, Q, Backspace) with no blade on the anvil runs `leave()`. In `leave()`, `forging = false` comes before `ItemPicker.close()`, and `heatPrompt.Enabled = not heatPrompt:GetAttribute("CrafterOff")`. |
| `RackService`, `RackController` | `SWORD_CAP` is gone: `store` and `fullSign` use `Upgrades.openSlots` (6, or 12 with Rack 2). "Rack Full!" shows only over the first rack's plinth. RackController: locked slots get no marker and E skips them; the Sword entry also waits for `SwordRack2.Plinth.RackPrompt` (`also`) with the same handlers; a shown-prompt counter keeps the highlight and picker when you walk from one rack's prompt to the other's. Every crew take redraws every rack sword (`showSwords`), as the crafter's already did. |
| `EmployeeService` (crafter) | `scrub` turns the shoulder's `Attachment0.CFrame` on AnimationConstraint rigs (their `C0` is read-only: every sword errored there, the ingot went back on the rack and nothing was racked), `C0` on Motor6D rigs, and cancels the last tween first. `rest(c)` stops every track but idle and walk and shows the hammer; the error branch calls it. Hammer grip −90 (Roblox's tool grip), hidden while polishing (`showHammer`). `swordCap(plot)` = `Upgrades.openSlots(plot.Smithy.SwordRack.Slots)`. `rackUsed(player, d)` = the rack's swords + 1 while the Etcher has one off it; the crafter's two rack-full checks use it. The stand at the Finished Sword Rack is plot (−9.5, −13.7), in front of the plinth: `spot` no longer uses the rack model's box, which Slot7–12 widen. `promptsOf`: Rack 2's `RackPrompt` goes off with the rack's while the crafter has it. |
| `EmployeeService` (staff) | `JOBS[role] = { home, run }` and `SETTINGS[role]` (the value check). Hiring: `Bought_<upgrade>` (signal, and at claim) makes `d.staff[role]`. `staffLoop` spawns the worker and runs the job under `pcall`; after each round `putBack` returns a carried sword (rack if there's room, else the bag), a reserved holder is cancelled and a laid sword destroyed. `ReplicatedStorage.Crafters` also holds the four staff looks; `makeWorker` names a staff NPC after its pad id and gives only crafters a hammer; overhead `def.role or Employees.ROLE`. `setStatus(plot, status, attr?)` writes `<upgrade>Status` per role. `carry(c, sword)`: right hand, tool grip, welded, toolnone. The remote takes `("set", role, value)` before the crafter-only guard. `onSave` puts a carried sword on the rack (or in the bag when it's full); `onLeave` clears the jobs. |
| `EmployeeService` (Stocker, Cashier, Promoter) | `stockOne`: waits `noRack` / `noSwords` / `shopFull`; reserves a holder (`Hook_Stock`), walks to the rack, gives up if the sword is gone, carries it to the inspect spot and places it; his walk speed is the perk. While the Etcher has a pattern he leaves un-etched swords, unless `EtcherStatus` is `rackFull`. `POST`: Cashier (6, 2.75, −9) and Promoter (−9, 2.85, −50.5) in plot space, facing the street. `JOBS.cashier` only stands (ShopService does his work); `SETTINGS.cashier` takes a valid step. `waveOne` (`JOBS.promoter`): every 4 s he turns to the nearest root within 40 studs in `workspace.Customers` or `workspace.Villagers` and plays `ANIM.wave` (507770239). |
| `EmployeeService` (Etcher) | `etchOne`: waits `noPattern` / `noRack` / `noSwords`; takes the first un-etched sword, carries it to Etching Table 2, lays it there (an anchored `buildSword` at `Top * (−3.02, 0.39, 0.8)`), works it with `scrub` for `perk("etcher", count)`, applies the pattern as EtchService does (`Etches.colorsFor`, the setting re-read then), carries it back (waits `rackFull`) and racks it. `STAND.EtchingTable2` (−4, 0, −1). `SETTINGS.etcher` takes an existing `Etches.get(v)`. `syncPrompt` turns on `EtchingTable2.Top.EtcherPrompt` once the table is bought and he's hired. He also etches swords you rack by hand. |
| `Shared/Employees` | `STAFF`: stocker / Sora, cashier / Aki (`setting` 10), promoter / Kaito, etcher / Yume (`id, role, name, walk, upgrade, done, look`). `STAFF_ORDER` (the crew tabs), `JOBS_PER_LEVEL` 5 (to Lv. 11), `PERKS`: Stocker walk 8 → 12, Cashier 3 → 1 s, Promoter walk-in gap ×0.8 → ×0.65, Etcher 10 → 5 s. `level(made, per?)`, `perk(role, count)`, `walk(role, count)`. `CASHIER` {min −20, max 50, step 5}, `cashierPercent(v)` (a valid step, else +10), `cashierSells(offer, value, setting)` (`offer × 100 >= value × (100 + pct)`). All tuning knobs. |
| `EmployeeController`, `CrewGui` | The crew button and window show once anyone is hired; with staff and no crafter the window opens on the first staff page. `Window.Tabs` (from `Templates.Tab`, a column off the window's left, shown with 2+ tabs, the open one outlined green): `fillTabs` sets the window's `AnchorPoint` X to (1 − 162/780) / 2 while tabs show, so window and tabs centre together at any scale (they ran off phones before the review); fit width 980. `Window.Staff` (724×400: Obtained, Done, Walk and Perk rows, a Panel from Stats without Stars; the role in the header). `PERK_ROW`: Cashier "Answer Time", Promoter "Walk-in Speed", Etcher "Etch Time"; the Stocker's perk is his Walk row, and the posted roles hide Walk. `Staff.Setting`: the Cashier's slider (`Label`, `Value`, `Slider` with `Track` / `Fill` / `Mark` at +0% and `Knob`; drag, tap or D-pad; sends `("set", "cashier", n)` after 0.4 s still). `Staff.Etch` (`Label` "Etches", `Value`, `Pick` "Patterns"): `patterns()` ItemPicker cards on a plain katana; `openPicker(title, fill)`; `EtcherPrompt` opens his page. Status per role (`status(attr)`). `DOT` is an allow-list: any `CrafterStatus` wait, `StockerStatus` `noRack`, `EtcherStatus` `noPattern` / `noRack` / `rackFull`; an idle Stocker doesn't light it. |
| `Workspace.Plot.Smithy.SwordRack`, `SwordRack2` | `SwordRack2` is its own Model (TycoonItem, `Upgrade = SwordRack2`, not inside SwordRack: a TycoonItem inside another doesn't lock right) on the wall left of the first, with its own `Plinth.RackPrompt`. Its hooks are `SwordRack.Slots.Slot7–12` (TycoonItems of `SwordRack2`). Both racks: slots y 4.28 → 5.38 (raised 1.1), posts and caps at ±3.75, plinth 8.0, rail 7.9, stretcher 7.4, hooks 1.18 apart; 0.9 apart at the plinths. Longsword guards clear the posts by 0.055 and each other by 0.03. |
| `Workspace.Plot.Smithy.EtchingTable2` | A clone of the Etching Table (`Upgrade = EtchingTable2`), pivot plot (21.5, 2.40, 22.5), facing −x, in the right-back corner opposite the Hilt Bench. No DemoSword (the three prop swords stay). `Top.EtchPrompt` renamed `EtcherPrompt` ("Sword Etcher", off until he's hired); `Top` raised 0.05 off the counter. |
| `Workspace.Plot.Shop.CashierCounter` | The old `Interior_Counter` from `Legacy.ShopExtras_removed`: TycoonItem of `Cashier`, centred at plot (6, 1.405, −11), panel to the street, left end at x 1.7 (3.7 studs in front of the workshop door). |
| `Workspace.Plot.Pads` | `MergeSlots` (a copy of OreStand6, (14.80, −0.30, −10.10)), `SwordRack2` (−18.4, −0.3, −13.5), `Stocker` (on the SwordRack pad, (−9.5, −0.3, −13.5)), `Cashier` (6, −0.3, −9, shop), `Promoter` (−9, −0.2, −50.5, on the walkway), `EtchingTable2` and `Etcher` (17.1, −0.3, 22.5). The workshop ones have `Workshop = true`. |
| `Workspace.Village` | `PlotSlotN2` (Pad, 3 Edges) and N2's Walkway, Water, 2 Curbs and lamps moved +8 z; S2's the same −8 z. The two Junction slabs are `Legacy.Junction_beforeAlign` / `Junction_beforeAlign_S`. `workspace.Plot` pivoted to `PlotSlotN2`: (640, 0.5, −292) → (640, 0.5, −284). |
| `Builders.build_simple`, `build_atmosphere`, `build_workshop` (and `Models/Village/*.luau`) | `MID = 0` and no Junction slab line in build_simple; `{ 0, HALF }` in build_atmosphere. build_workshop: shelves `CX, HW` 0.7, 3.6, `AXIS` 0.6, `CRADLE` 1.95 (0.6 wider toward the front, the longsword 0.07 clear at each end; only that block was rerun, rebuilding all four `Shelf`s) and `PADS.MergeSlots = PADS.OreStand6`. Studio and vault copies are byte-identical. `build_parking.luau`'s comments still mention the junction. |
| `StyleTest_CFrame` attributes | After the move, 77 saved CFrames (73 in `Workspace.Plot`, 4 street LampPosts) were shifted by the same ±8 in one undoable step, so a `build_style_test` rerun keeps those parts in place. No script changed. |

- **Hand edits, not in the builders:** Finished Sword Rack 2 and both racks' raise and widening, Etching Table 2, the cashier's counter and the new pads (only `MergeSlots` is in `build_workshop`'s `PADS`). `build_workshop`'s shelf constants are updated, so its shelf section is safe to rerun; it doesn't know Etching Table 2.
- **Backups:** `ServerStorage.Legacy.<Name>_beforeRefinements3md` (list in the session note), `VillageAlign_beforeRefinements3md` (the moved street pieces), `SwordRack_beforeGuardFit`, `SwordRack2_beforeGuardFit`, `Junction_beforeAlign`, `Junction_beforeAlign_S`. New instances have none (delete to undo): `Smithy.SwordRack2`, `SwordRack.Slots.Slot7–12`, `Smithy.EtchingTable2`, `Shop.CashierCounter`, `Pads.MergeSlots/SwordRack2/Stocker/Cashier/Promoter/EtchingTable2/Etcher`.

---
title: Code Map
status: current recorded architecture — runtime verification pending
type: development
updated: "2026-10-31"
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

Recorded player-facing rule: completing forging gives **100% quality**; full polish multiplies the value by **1.10** (since 2026-10-23; it was +10% added to the other bonuses) and etching adds **+10 / +15 / +20%** (Flame, which comes with the Etching Table; Woven Wind; Fracture; 2026-11-03). Old 90%-cap descriptions in the archived map predate that rule. Blade refinement remains an internal geometry/finish concept; do not infer current displayed quality or server limits from old port/probe descriptions. Inspect live SmithService/ForgeCheck when changing either.

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
| `ForgeService` | Each plot's ore box and purchased slots; spin whenever no roll is playing, a pull replacing the ore still waiting (since Economy pass 2, 2026-10-27; it went into your hands first from 2026-10-24, which superseded collect-before-reroll, 2026-10-22; a merge still puts it in your hands); `rollFor`: the tutorial's first two pulls are a Common then an Uncommon, then rolls by `Upgrades.luck` (merges); one ingot per unlocked furnace. Heating is 3 s until first completion, then 10 s. |
| `InventoryService` | (Economy pass 2, 2026-10-27) `Remotes.Trash(kind, ids)`: throws away carried ingots (a stack's ids), a sword or a blade, for nothing; the bag's trash icon sends it. |
| `SmithService` | Begin/finish forge requests, blueprint/ingot validation through `ForgeCheck`, and hilt assembly. |
| `ShopService` | Owner-specific displays, per-plot customer routes/spawners, offers/haggling and sale payouts. 2–4 customers at once per plot (More Clients), plus one per Rickshaw Bay (`Rickshaws`, 2026-10-23), plus one with the Shop Promoter (2026-10-24). Since 2026-10-24 a hired Cashier answers offers for you. Since 2026-10-23 `DisplaySword` and the restore on claim check `Blueprints.fits` (big swords only on `BigSword` holders). |
| `PolishService` | BeginPolish/PolishSword, station reach/unlock checks, refinement replay/timing validation, state update and rebuilt sword. `PolishSword(swordId, saved, leaving)`: leaving the station sends what was polished (or nil) with `leaving = true`, which keeps a partial polish and ends the session; `PlayerPolishing` on the station from BeginPolish until then keeps the crafter off it (2026-10-23). |
| `EtchService` | Valid sword/pattern, own unlocked station/reach and one-etch-per-sword checks; accepted finish updates authoritative state. |
| `RackService` | Own-plot ingot/sword storage and retrieval; capacities 6 ingots (12 until 2026-10-23), swords up to the open hooks (`Upgrades.openSlots`: 6, or 12 with Finished Sword Rack 2, since 2026-10-24; was a fixed 6). No carry cap since 2026-10-24 (was 6 ingots). |
| `LeverAnimator` | Lever hold/release motion for plot rollers. |
| `DevTools` | Studio-only coin and example-sword grants; guarded by `RunService:IsStudio()`. |

First-sale exceptions: a listing spawns a customer immediately until `sold > 0`; later arrivals come every Better Advertising gap, 45–75 s at level 0 (since 2026-10-27; 12–22 s before, kept as `TUTORIAL_GAP` until Ore Slot 2), shorter with the Shop Promoter (since 2026-10-24); reputation no longer shortens it. The Cashier answers only from `sold >= 2`, so the first two sales stay the player's. At `sold == 0` the offer is exact value and declining ends it. At `sold == 1` a hint shows and the first decline guarantees a raise. Later sales use normal negotiation. Future direct commissions must not increment the ordinary-shop sale counter.

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
| `Shared/Etches`, `EtchPatterns`, `EtchCanvas` | Finish catalogue, stroke paths and progressive/final image work. Flame and Eclipse have build records; further patterns require confirmation. Since 2026-10-23 `EtchCanvas` draws the strong glow (GLOW_CM, GLOW, CORE, THICK at its top) and paints raised pixels once per flush; `SwordRenderer` builds world etches over frames. Since 2026-10-28 `_flush(dirty, spread)` also yields between pixels in a spread `reveal`, and `spread` may be a number: the seconds of work per frame (`sliceOf`; `true` is `SLICE`, 4 ms). `SwordMeshCache.etch` passes it through. `EtchPlayback.prepare` yields: it builds the finished etch and the show's canvas with `BUILD_SLICE` (10 ms). |
| `Shared/SwordMeshCache` | Shared, baked-first finished-sword geometry with live fallback and etch/polish appearance. |
| `SwordMeshes`, `SwordParts.KatanaHilt` | Uploaded finished meshes and dressed hilt/guard templates used by world and viewport art. |
| `Remotes` | Forge/hilt/polish/etch, state, rack, display/offer and upgrade request/event boundary. Client choices require server ownership, reach and state checks. |

`Shared/AnvilScore` keeps only the grade for a percentage (`forPercent`, `FINISH_AT`, `MAX_MULTIPLIER`) and `Shared/BladeMesh` only `stationX`/`stationWidth`; the first anvil's `BladeProfile` and outline scoring went on 2026-11-02 (backup `Legacy.BladeProfile_removed_1102`; `Tests.AnvilSelfCheck` checks the frozen copy in `Legacy.SharedV1`). Probe modules may remain test references.

## Client controllers and interface

**GUIs live in StarterGui (2026-10-23).** Every screen everyone sees is a ScreenGui (or singleton BillboardGui) in `StarterGui`, editable in Studio's UI editor; its controller finds it with `PlayerGui:WaitForChild(name)` and fills it. Repeated pieces (cards, slots, rows, chips, order cards, book entries, holder markers) are cloned from a hidden `Templates` Frame inside the GUI (a Folder doesn't hide GUI objects, so templates in one drew on screen; turn the Frame's `Visible` on to edit them); 3D art in ViewportFrames, the coin fly-in, "+N" pops and confetti stay in code. Every moved GUI has `ResetOnSpawn = false` (a respawn must not swap in a fresh copy) and arrives at the first spawn, so controllers and `ItemPicker` wait for it then. Still built in code: `DevPanel` (developer-only) and `TycoonController`'s per-pad labels. **A ViewportFrame's Camera in a StarterGui template never reaches the client** (Cameras don't replicate): make the camera in code when it's missing, as `CollectionController` and `DeliveryController` do (the book threw and never opened until 2026-10-23).

| GUI in StarterGui | Controller | Notes |
|---|---|---|
| `PickerGui` | `ItemPicker` | `Window` (desktop) and `CompactWindow` (under 500 px tall), each a `Shadow`, brown `Fill`, seigaiha `Pattern` and half-clear `Tint` with the contents in `Body`, `Toast`, `Templates.Card`/`CompactCard` (184 px `Art` with an `Outline` white-rim viewport behind it, the blade's rim from `SwordMeshCache.plain`, `Chip` as a top-left tag, square corners, charcoal gradient, [[Sessions/2026-10-26#Brighter picker cards]]); Q, Backspace and B close it. API unchanged. `PickerBlur` stays in Lighting. |
| `HudGui` | `Hud` | `Coins`, `Reputation` pills (y −52 / −104 on the left edge). Since 2026-10-24 `Coins` has no plate (the number outlined) and `Reputation` is hidden (`Visible` false; `Hud` still fills it); the rank shows only in the Deliveries window. |
| `MenuGui` | `MenuController` (+ `GemController`, `CollectionController`, `EmployeeController`) | (2026-10-23) `Buttons`: a 3-across grid at y +30 under the gem counter: `Shop`, `Upgrades` (House → Gem Shop; Charts until 2026-10-24), `Daily` (gift, `Dot`), `Book` (sword), `Crew` (shown from the start since 2026-10-30, the crew not hired yet locked inside; hidden until anyone was hired before; until 2026-10-24 the crafter), `Settings`; VectorIcons. Since 2026-10-24 just the icons (38 px, were 30): no plates, and each button's stroke shows only as an amber edge on the gamepad's selection. MenuController styles every button and runs `ShopWindow` (empty Robux shop, "Coming soon") and `SettingsWindow` (`Music` / `Sound` rows with a `Switch`), `Dim`. |
| `HotbarGui` | `Hotbar` | `Bar` (+ `Bag` button), `BagPanel` (+ `Trash` over its top-right corner since 2026-10-27: drop a stack on it to throw it away), `Templates.Slot` (with a `Metal` line since 2026-10-24); slot size, art box, gap and padding read from the instances. On touch the bar shows as many stacks as fit left of a 170 px jump-button corner; the rest sit at the front of the bag. |
| `GemGui` | `GemController` | `Gems` counter (a Frame since 2026-10-23, no plate since 2026-10-24; Hud pops "+N" on it), `DailyReward`, `GemShop`, `Templates.Day`/`Upgrade`. Opened from `MenuGui`'s Upgrades (the House) and Daily buttons. |
| `CollectionGui` | `CollectionController` | `Window` (its `Entries` a `UIListLayout` of `Templates.Section` clones, one per rarity: `Divider` (`Label`, `Line`) over a 4-wide `Grid`; [[Sessions/2026-10-28#Ingot book grouped by rarity]]), `Templates.Entry` (an `Art` ImageLabel and a `Label`; Row/Polished/Etched removed 2026-10-23); opened from `MenuGui.Buttons.Book` (its own button is gone). |
| `DeliveryGui` | `DeliveryController` | `Window` (868×450 design, `Fit`), `PinnedOrder` (since 2026-10-24 at (0, 12, 0.5, −104), the Reputation pill's old slot, with no plate, shown only while pinned; it was at y −156, or beside Reputation on screens under ~480 px tall), `Window.Body.Packing` (2026-10-24), `Templates.Order`/`Crate`/`Button`/`Slot`/`Sword`/`Pin`. |
| `RewardGui` | `RewardCard` | `Templates.Card`/`Chip`. |
| `GuideGui`, `WorkshopOpenGui`, `GuideArrow` | `Guide` | The arrow is a BillboardGui directly in StarterGui; the script sets its Adornee. |
| `PolishHud` | `PolishController` | `Panel` (+ `Fit`), `Templates.Cell`/`Bracket`. |
| `EtchHud`, `HiltSeatGui` | `EtchingTableController`, `HiltBenchController` | Matching close rings (`Close`). |
| `StrikeRingGui`, `GrindMap` | `AnvilController` | `AnvilHud` and `AnvilPoints` were already here. |
| `OfferBubble`, `ShopHud` | `ShopController` | `OfferBubble` (BillboardGui) holds the `OfferCard` that was in ShopHud; `ShopHud.Templates.SlotMarker` for the + / bag / for-sale markers. |

**Pack copies (2026-10-24):** `HudGui_Pack`, `GemGui_Pack`, `MenuGui_Pack`, `HotbarGui_Pack`, `PickerGui_Pack` and `OfferBubble_Pack`, in `ServerStorage.UIPackCopies` since the GUI review the same day (they were in StarterGui, copied into every player's PlayerGui unused), are disabled restyles in the look of Allen's free UI pack (`StarterGui.UIMegaPack`), kept for comparison. No script reads them; they have every child their controller indexes, so swapping names puts one in. See [[Sessions/2026-10-24#UI pack comparison]].

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
- `Development/Dialogue Editor/` (2026-11-03): a local page for every NPC line (shop customers, named characters, mail senders, story quests, tutorial hints). Start `dialogue-editor` in `.claude/launch.json` (port 8767); `export.luau` (run in Studio Edit) writes `studio.json` from cloned `Shared.Customers`/`Senders`/`Commissions` and `Guide`; the page autosaves Allen's edits to `edits.json`. See its README for wiring edits back.
- `ServerStorage.Legacy` holds the current round of `<Name>_before<Change>_<MMDD>` backups and `SharedV1` (read by `Tests.AnvilSelfCheck`). Older backups, maps, models and GUIs are `.rbxm` files in `Archive/Studio Backups/` (moved out 2026-11-02, see its README); its 442 script backups before that were deleted on 2026-10-27 (older place versions still hold them).

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
| `Hotbar` | `GAP` 13 between 84 × 94 slots with 2 px edges (`EDGE` read from the template's `Edge`; were 16, 100 × 112, 3 px until 2026-10-26). New stacks join the bar up to `BAR_SLOTS`, not the screen's `barCap`. |
| `SaveSpec` | 47/47: adds gems, levels, streak and the any-metal Wakizashi. |
| `ServerStorage.Builders.build_atmosphere` (new; local `Models/Village/build_atmosphere.luau`) | Rerunnable (`loadstring(...Source)()`, SEED 31; rerun after `build_simple`). Sets Lighting (warm 16.9 h, latitude 28, Atmosphere, Bloom, new Sky and ColorCorrection, brighter indoor Ambient), rebuilds `Village.Atmosphere` (1,372 parts: Nature, Dressing, Backdrop.Forest; tree meshes cloned from `Village3D`/`Buildings3D`) and leaves the Terrain alone (it makes none; the `Terrain:Clear()` it ran each time was removed in the 2026-11-02 audit), and makes the village's own lanterns glow. Keeps off lots, delivery bays, the street's central 20 studs, the gate and shrine approach. Backup: `Legacy.Lighting_beforeAtmosphere`. |

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
| `MaterialService.Paint*` | Near-grey tiles tinted by part colour. FreeStylized 2K textures prepared by `Models/Village/freestylized_textures.py` (royalty free, commercial use allowed): PaintEarth (Ground_02, 24 studs per tile), PaintStone (Ground_Stones_01, 10), PaintPlaster (Concrete_Wall_01, 12), PaintStoneWall (Stones_Wall_02, Cobblestone, 8), PaintWood (Wood_10, 6), PaintWoodDark (Wood_02, Wood parts whose original colour value < 0.3, 6), PaintPlanks (Wood_Planks_04, WoodPlanks, 8; Wood_11 until 2026-10-25), PaintCrate (Wood_Planks_23, WoodPlanks parts named `Crate`, 2.4), PaintFloor (Floor_Tiles_01, Slate, only `Plot.Workshop.Floor`, 12), PaintFurniture (Wood_09, plain Wood parts of `Shop.Displays`, `Shop.CashierCounter` and `Smithy`, 5; `build_style_test`'s `furniture()`; not the display tables' tops and sword stands, SmoothPlastic since 2026-10-25, and their corner caps are gone: `build_workshop`). PaintRoof is still painted by `Models/Village/style_textures.py` (seed 22). [[Sessions/2026-10-22#FreeStylized textures swapped in]], [[Sessions/2026-10-25#FreeStylized texture swap: shop floor, workshop floor, crates]], [[Sessions/2026-10-25#Notice board for deliveries, stylized wood on shelves and tables]] |
| `ServerStorage.Buildings3D.NoticeBoard` (2026-10-25) | FreeStylized Notice Board 01 (`Models/Props/notice_board.py`, Model 127479932837705): MeshPart 4.98 × 5.4 × 0.58, non-solid, SurfaceAppearance, papers on the front (−Z). `build_delivery` clones it as `DeliveryBay.DeliveryBoard.Board`; the board's `Panel` (invisible) keeps `DeliveryPrompt` and `Status`. |
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
| `Guide` | `board()` and `visitor()` gone; `blueprintPad(plot, id)`. Letter offered → "Open your mail"; active → `craft(plot, c)`, which says "Hand it in from the mail" (no target), "Buy the <pad>" (its pad) or, short of the price, the tantō loop (`craft(plot, nil)`). Since 2026-10-28 only `Commissions.list[1]` is guided; later letters get no goal line or spotlight. After the tutorial (Ore Slot 2 bought) picker cards and station action cards get no spotlight; only the Gem Shop tour's button does. |
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
| Doppler metal (2026-10-29) | `Materials` Doppler (Legendary, after Sunsteel, `texture = "Doppler"`, tint white): `MaterialService.DopplerIngot` (3 studs per tile) / `DopplerBlade` (3.5), `metal_textures.py doppler` maps. `Etches.MATERIAL_FLAME` near white. Book images Doppler and a re-shot Damascus. Backups `Legacy.Materials_beforeDoppler`, `Legacy.Etches_beforeDoppler`. |
| Damascus texture (2026-10-29) | `Materials` Damascus has `texture = "Damascus"`, tint white: `MaterialService.DamascusIngot` (3 studs per tile) and `DamascusBlade` (2.5), Metal, `metal_textures.py damascus` wild maps (folded layers along U, in their own greys), BladeShine1's metalness. `metal_textures.py` also has unused `damascus_drops` / `damascus_ladder` and `mythril` (drafted 2026-10-29). |
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
| `EmployeeController`, `CrewGui` | The crew button and window show once anyone is hired (until 2026-10-30: since then always, the crew not hired yet as locked cards); with staff and no crafter the window opens on the first staff page. `Window.Tabs` (from `Templates.Tab`, a column off the window's left, shown with 2+ tabs, the open one outlined green): `fillTabs` sets the window's `AnchorPoint` X to (1 − 162/780) / 2 while tabs show, so window and tabs centre together at any scale (they ran off phones before the review); fit width 980. `Window.Staff` (724×400: Obtained, Done, Walk and Perk rows, a Panel from Stats without Stars; the role in the header). `PERK_ROW`: Cashier "Answer Time", Promoter "Walk-in Speed", Etcher "Etch Time"; the Stocker's perk is his Walk row, and the posted roles hide Walk. `Staff.Setting`: the Cashier's slider (`Label`, `Value`, `Slider` with `Track` / `Fill` / `Mark` at +0% and `Knob`; drag, tap or D-pad; sends `("set", "cashier", n)` after 0.4 s still). `Staff.Etch` (`Label` "Etches", `Value`, `Pick` "Patterns"): `patterns()` ItemPicker cards on a plain katana; `openPicker(title, fill)`; `EtcherPrompt` opens his page. Status per role (`status(attr)`). `DOT` is an allow-list: any `CrafterStatus` wait, `StockerStatus` `noRack`, `EtcherStatus` `noPattern` / `noRack` / `rackFull`; an idle Stocker doesn't light it. |
| `Workspace.Plot.Smithy.SwordRack`, `SwordRack2` | `SwordRack2` is its own Model (TycoonItem, `Upgrade = SwordRack2`, not inside SwordRack: a TycoonItem inside another doesn't lock right) on the wall left of the first, with its own `Plinth.RackPrompt`. Its hooks are `SwordRack.Slots.Slot7–12` (TycoonItems of `SwordRack2`). Both racks: slots y 4.28 → 5.38 (raised 1.1), posts and caps at ±3.75, plinth 8.0, rail 7.9, stretcher 7.4, hooks 1.18 apart; 0.9 apart at the plinths. Longsword guards clear the posts by 0.055 and each other by 0.03. |
| `Workspace.Plot.Smithy.EtchingTable2` | A clone of the Etching Table (`Upgrade = EtchingTable2`), pivot plot (21.5, 2.40, 22.5), facing −x, in the right-back corner opposite the Hilt Bench. No DemoSword (the three prop swords stay). `Top.EtchPrompt` renamed `EtcherPrompt` ("Sword Etcher", off until he's hired); `Top` raised 0.05 off the counter. |
| `Workspace.Plot.Shop.CashierCounter` | The old `Interior_Counter` from `Legacy.ShopExtras_removed`: TycoonItem of `Cashier`, centred at plot (6, 1.405, −11), panel to the street, left end at x 1.7 (3.7 studs in front of the workshop door). |
| `Workspace.Plot.Pads` | `MergeSlots` (a copy of OreStand6, (14.80, −0.30, −10.10)), `SwordRack2` (−18.4, −0.3, −13.5), `Stocker` (on the SwordRack pad, (−9.5, −0.3, −13.5)), `Cashier` (6, −0.3, −9, shop), `Promoter` (−9, −0.2, −50.5, on the walkway), `EtchingTable2` and `Etcher` (17.1, −0.3, 22.5). The workshop ones have `Workshop = true`. |
| `Workspace.Village` | `PlotSlotN2` (Pad, 3 Edges) and N2's Walkway, Water, 2 Curbs and lamps moved +8 z; S2's the same −8 z. The two Junction slabs are `Legacy.Junction_beforeAlign` / `Junction_beforeAlign_S`. `workspace.Plot` pivoted to `PlotSlotN2`: (640, 0.5, −292) → (640, 0.5, −284). |
| `Builders.build_simple`, `build_atmosphere`, `build_workshop` (and `Models/Village/*.luau`) | `MID = 0` and no Junction slab line in build_simple; `{ 0, HALF }` in build_atmosphere. build_workshop: shelves `CX, HW` 0.7, 3.6, `AXIS` 0.6, `CRADLE` 1.95 (0.6 wider toward the front, the longsword 0.07 clear at each end; only that block was rerun, rebuilding all four `Shelf`s) and `PADS.MergeSlots = PADS.OreStand6`. Studio and vault copies are byte-identical. `build_parking.luau`'s comments still mention the junction. |
| `StyleTest_CFrame` attributes | After the move, 77 saved CFrames (73 in `Workspace.Plot`, 4 street LampPosts) were shifted by the same ±8 in one undoable step, so a `build_style_test` rerun keeps those parts in place. No script changed. |

- **Hand edits, not in the builders:** Finished Sword Rack 2 and both racks' raise and widening, Etching Table 2, the cashier's counter and the new pads (only `MergeSlots` is in `build_workshop`'s `PADS`). `build_workshop`'s shelf constants are updated, so its shelf section is safe to rerun; it doesn't know Etching Table 2.
- **Backups:** `ServerStorage.Legacy.<Name>_beforeRefinements3md` (list in the session note), `VillageAlign_beforeRefinements3md` (the moved street pieces), `SwordRack_beforeGuardFit`, `SwordRack2_beforeGuardFit`, `Junction_beforeAlign`, `Junction_beforeAlign_S`. New instances have none (delete to undo): `Smithy.SwordRack2`, `SwordRack.Slots.Slot7–12`, `Smithy.EtchingTable2`, `Shop.CashierCounter`, `Pads.MergeSlots/SwordRack2/Stocker/Cashier/Promoter/EtchingTable2/Etcher`.

## Refinement 4 (2026-10-24)

[[Sessions/2026-10-24#Refinement 4]] ([[refinement4]]). Supersedes, above: the crafter claiming the Ingot Rack and Finished Sword Rack (`claim(smithy.IngotRack)`, `claim(smithy.SwordRack)`, `promptsOf`'s second-rack case, the racks' `CrafterBusy` checks in RackService and RackController), `INGOT_CAP` 6, the single offer card (`current`, `bubble`, `answer(accept)`), `asking` as a boolean and askOwner's own wait, the Cashier turning to each customer and paying straight into your coins, the Promoter turning to anyone within 40 studs, plain-coloured employee looks, Customers' 70–110% openers and the furnace lights at 2.2 / 16.

| Script / instance | 2026-10-24 |
|---|---|
| `EmployeeService` (crafter) | The racks are never claimed: step 1 walks to `spot(plot, IngotRack.Slots["Slot"..<the cheapest ingot's rackSlot>], STAND.IngotRack)` and takes the cheapest ingot there is on arrival (none left: the round ends); step 5 walks to the rack and waits `rackFull` while it is full, no claim. `claim`/`release` are for stations only (furnaces, Anvil 2, the Polishing Station) and walk `station:GetDescendants()`. |
| `EmployeeService` (looks) | `ReplicatedStorage.Crafters` is parented at once; each look is built on its own thread by `dress(look, outfit)`: body colours, then `look.outfit`'s `Shirt`, `Pants`, `HairAccessory`, `HatAccessory`, `FaceAccessory` on the HumanoidDescription. A failed load warns "Employee outfit:" and builds the plain look. Each accessory's Handle is set where its `AccessoryWeld` holds it (in ReplicatedStorage nothing solves the welds, so the crew portraits had them off the head). `makeWorker` finding no look yet returns nil and the loops retry a second later. |
| `EmployeeService` (Promoter) | `waveOne(plot, …)`: `post(plot, "promoter")` gives his stand and the street point; he turns to the nearest root within 40 studs whose offset from his stand points toward the street (`to:Dot(street - stand) > 0`), else to the street, then waves. |
| `Shared/Employees` | `Look` type with `outfit = { shirt, pants, hair?, hat?, face? }` (catalog ids; accessories as comma-separated strings). Locals at the top name the shared ids: `APRON` 5318191953, `WORK_KIMONO` 6530310794, `JUDO_KIMONO` 11692674238, `DARK_PANTS` 6530312930, `HAKAMA` 3905873202, the Roblox ninja headbands `WHITE_BAND` 11297746 / `BLACK_BAND` 11297708 / `ORANGE_BAND` 11297766. Staff: Sora jinbei 5666689617, Aki haori 182766522 + `HAKAMA`, Kaito yukata 8292171266 + `ORANGE_BAND`, Yume floral kimono 5780332981 / 5780335276 + Horn Rimmed Glasses 22151904. Hair: Roblox's 398672920, 376548738, 376527350, 343584973, 80922251, 63690008. |
| `RackService` (follow-up) | `placeAll(slots, list)`: each rack item keeps `rackSlot` (slot number); a `store` with RackAction's new 5th argument (the + used) gets that slot, others or a taken/locked one get the first free open slot, and `showIngots` / `showSwords` draw from it. `take` clears it. Not saved (a rejoin fills from slot 1). `store` takes any ingot, hot or cold (`takeIngot(player, id)`), and sets it cold. |
| `RackService` | No `INGOT_CAP`: `showIngots` draws every slot in `IngotRack.Slots` and `store` caps at `Upgrades.openSlots(IngotRack.Slots)` (6, or 12 with Ingot Rack 2). No `CrafterBusy` check. `near(player, smithy, which)` measures `REACH` (12) to the nearer unlocked rack's prompt part (`IngotRack`/`IngotRack2.Shelf1`, `SwordRack`/`SwordRack2.Plinth`), not to the first rack's box, which takes in Slot7–12 (review fix; the sword racks had it since Refinements 3). |
| `RackController` | `RACKS.Ingot.also` = `IngotRack2.Shelf1.RackPrompt`. `heldId(which)`: a held cold ingot's `IngotId` (Ingot) or a held sword's `SwordId` (Sword). `storeOrOpen(slot?)` (E on either prompt with no slot, or the + marker with its slot): stores the held item through `act(which, "store", id, slot)`, else opens the picker (whose picks carry the slot too). Follow-up: `heldId` and `canStore` count any ingot, hot or cold; the store picker lists hot ones as "Hot X Ingot". `usable()` is only `not Locked`; the click-to-take no longer checks `CrafterBusy`. |
| `Shared/Upgrades` | `IngotRack2` ("Ingot Rack 2", 500, after IngotRack). |
| `EmployeeController` | `portrait(view, id)` marks the view's `Portrait` attribute; with the look not in yet (still being dressed on the server) it waits for it (30 s) and draws it if the view still wants that look (review fix: portraits opened at server start stayed blank). |
| `Workspace.Plot.Smithy.IngotRack2`, `IngotRack.Slots.Slot7–12`, `Pads.IngotRack2` | A clone of the Ingot Rack (TycoonItem, `Upgrade = IngotRack2`) at plot (−0.1, 0, +6.8) from the first, box z 5.55…12.05 on the right wall, 0.1 off the wall line to clear the post at z 6.68…7.72; its `Shelf1.RackPrompt` is the second prompt. Its six slots are `IngotRack.Slots.Slot7–12` (each TycoonItem of `IngotRack2`), so `IngotRack`'s box now spans both racks (fine for RackService's 12-stud reach). The pad is a copy of `Pads.IngotRack` moved the same, `Workshop = true`. |
| `ShopController` | One card per offer: `cards[id] = { gui, spot?, muted? }`, each `gui` a clone of `PlayerGui.OfferBubble` (the original stays disabled as the template), named `Offer<id>`, with its own buttons, countdown and fallback spot part; `close(id)`, `answer(id, accept)`. `rang` (weak keys) rings an offer once per customer. `bindPad()` binds Y / L2 while any card is up and answers `nearest()` (the card over the customer nearest you); every open card's buttons say "(Y)" / "(L2)" on a gamepad. |
| `ShopService` (offers) | `asking[owner]` counts the owner's open cards. `waitCard(owner, still)` waits for no open card only while `sold < 2` (the tutorial), and always for `CARD_GAP` (1.5 s) since the last card closed (review fix: the card after the tutorial's last sale rang over its coins); `runCustomer` calls it before reading the offer's terms and before each `say(npc, "I'll give you …")` (not for the Cashier), so the line comes with its card. `askOwner(owner, info)` no longer waits or takes `still`. |
| `ShopService` (Cashier) | No `NpcWalk.face(clerk, …)`. `till[owner]`: a sale he makes adds the offer there (not `addCoins`). `showTill(plot, owner)` dresses the plot's `Cashier` NPC: `TillPouch` (a brown Fabric ball welded in his right hand), a `TillSign` BillboardGui on it (the offer card's coin `15402839520` and the amount, AlwaysOnTop, styled like "Rack Full!"), `CollectPrompt` on his root ("Collect", E, 10 studs, no line of sight) and a looped toolnone track (`HOLD` 507768375) holding the arm out; all shown only while the till has cash. `collectTill` (the prompt, owner only) pays it into your coins. A 0.5 s loop per plot redresses him if he was made again. (Follow-up after Allen's playtest; it was a sign on the counter's coin tray, collected by walking up.) `SmithyCore.onSave` adds the till to `save.coins`; `onLeave` clears it. |
| `Shared/Customers` | `offerMin`/`offerMax`: Farmer 1.0/1.10, Adventurer 1.0/1.15, Knight 1.05/1.20. **Replaced 2026-10-30 by one Regular, 1.15/1.50 (below).** |
| `Workspace.Plot.Smithy.Forge.Fire.PointLight`, `Forge2`'s | Brightness 0.9, Range 11 (were 2.2, 16); shadows kept. No builder sets them. |
| `ReplicatedStorage.Prototypes.ShapingRules` | `CONFIG.smoothAt` 90, `timing.smooth` 1.2. `Rules.canSmooth(s)`: score ≥ smoothAt and some workable station over the target by more than 0.01 cm. `Rules.smooth(s)`: every workable station wider than the target set to it (returns how many); never widens. |
| `ReplicatedStorage.Prototypes.ShapingPrototype` | `smoothButton` ("Smooth", between Turn and Finish), shown by `drawDiagram` while `Rules.canSmooth`; `smoothOut()` sweeps base → point over `T.smooth` (each station eases in over 0.1 u as the sweep passes, flash and sparks follow it). `stats.smooths`; the Finish card adds "· smoothed"; the log line and `Inspect` report `smooths` (and `canSmooth`). |
| `ServerStorage.Tests.SaveSpec` | 88 checks: + no opening offer under value or over +20%, Ingot Rack 2 after the Ingot Rack, `openSlots` 6 then 12. |
| `ServerStorage.Tests.ShapingRulesSpec` | 26 checks: + the seven smoothing checks. `AnvilSelfCheck`'s knight range is 105–120 (131–150 liked). |
| `Workspace.Plot.Smithy.HiltBench.PropSwords`, `PolishStation.PropSwords` (follow-up) | Real swords from `SmithyCore.buildSword` (`ForgedSword`, `Prop`, no `SwordId`), as `EtchingTable.Dress.PropSwords`: `PropSword_Fittings` (katana, Steel, Gem hilt, unpolished) with its Handle at plot (−23.1, 4.25, 19.02), `PropSword_Polished` (katana, Silver, Gold hilt, fully polished) at (−23.1, 4.25, 7.72); X along +z, Y toward the room, Z (the edge) up. They replace the part-built samples (now `Legacy.HiltBenchWallSword_beforeRealSword`, `PolishStationWallSword_beforeRealSword`). Hand edits: `build_workshop`'s `sampleSword` calls would build the part ones again if its finishing section were rerun. |
| `ServerStorage.UIMegaPack` (follow-up) | Allen's free UI pack, moved out of `StarterGui` intact: its `ButtonIconScripts` replayed each button's `IdleSound` in game (the static he heard). In ServerStorage nothing of it runs or reaches clients. |

- **Hand edits, not in a builder:** Ingot Rack 2 and its pad, the furnace lights, the two wall prop swords.
- **Backups:** `ServerStorage.Legacy.<Name>_beforeRefinements4` (list in the session note). New instances have none (delete to undo): `Smithy.IngotRack2`, `IngotRack.Slots.Slot7–12`, `Pads.IngotRack2`.

## Phone HUD and station walls (2026-10-24)

[[Sessions/2026-10-24#Phone playtest: HUD, toolbox, windows, station walls]]. Supersedes, above: the left-edge stack centred on the screen (`HudGui.Coins` y −52, `GemGui.Gems` y 0 around the middle, `MenuGui.Buttons` 30 below it, `PinnedOrder` above the coins), the toolbox centred left of the jump button, the five window headers' title-and-X row, the sale notice, the Hilt Bench's part-built hanging hilts and the 2–4.5 s glint on every polished blade only.

| Script / instance | 2026-10-24 |
|---|---|
| `HudGui.Coins`, `GemGui.Gems`, `MenuGui.Buttons`, `DeliveryGui.PinnedOrder` | The left column, in StarterGui only (no script places it; `UiFx.underTopbar` / `leftColumn` and DeliveryController's follow-the-menu `place()` are gone, later the same day). Each is a lane: AnchorPoint (0, 0.5), Position (0, 12, 0.5, 29), Size Y (1, −58), a `UISizeConstraint` MaxSize Y 372, so it runs from under the 58 px top bar to the screen's foot, at most 372 tall, centred in that space. Content: `Coins.Row` y 0, `Gems.Row` y 40, `Buttons` a `UIPadding` top 90 (Size X 148, AutomaticSize None), `PinnedOrder.Row` y 194. Coins at 58 on a phone up to 430 tall, 219 at 753, 383 at 1080. **Since 2026-10-26** each lane is Size (1, 0, 1, −58) with MaxSize Y 445 and a `UIAspectRatioConstraint` 0.6 (`FitWithinMaxSize`, height dominant), and its contents are Scale: old pixels ÷ the 332 px phone lane (grid cell heights ÷ 242, the lane under its 90 px padding). Icons squared by aspect constraints; `Count` / `Label` `TextScaled`, left, 10–27 px. No `Grow` and no script sizing. |
| `Hud` | The gems' "+N" `pop` goes beside `GemGui.Gems.Row` (the `Gems` frame is its lane). Since 2026-10-26 beside `Row.Count`'s `TextBounds`, as the row spans the lane. |
| `Hotbar` | `refresh`: the bar and the bag at `UDim2.new(0.5, 0, …)` (were `-clear / 2`); `barCap` and the bag's columns from `view.X - 2 * clear` (`clear` = `JUMP` 170 on touch), so a centred bar never reaches the jump button. |
| `GemGui.GemShop`, `GemGui.DailyReward`, `MenuGui.ShopWindow`, `MenuGui.SettingsWindow`, `MailGui.Window` `.Header` | No `UIListLayout`; Size (1, 0, 0, 52), AutomaticSize None; `Title` anchor (0.5, 0.5) at the centre; `Close` anchor (1, 0) at (1, 18, 0, −12): 10 px in from the window's top-right corner through its 28 / 22 px padding. Paths unchanged (`Header.Close`). |
| `TextChatService.ChatWindowConfiguration` | `HorizontalAlignment` Right (was Left: it opened over the coins). |
| `ShopService` | No sale notice (`notice(owner, "Sold …")` removed); `commas` stays for the till's sign. |
| `SwordRenderer` | `glint(part, length, shimmer)`: with the sword's `Shimmer` attribute, glints every 0.3–0.8 s at 0.8 (else 2–4.5 s at 0.55) and a `PointLight` (range 2.2, up to 3) tweens base → tip over 0.9 s every 2.5–3.5 s. Glints and the sheen skip while the blade's `LocalTransparencyModifier` is 1 (a locked station's prop). A `Shimmer` sword glints even if not fully polished. |
| `Workspace.Plot.Smithy.PolishStation.PropSwords.PropSword_Polished` | `Shimmer` = true. |
| `Workspace.Plot.Smithy.HiltBench.PropHilts` | Five `buildSword` models with the `ForgedSword` tag removed (hilts only, no blade drawn), `Prop`, no `SwordId`: `PropHilt_katana_Gem` z 24.92, `_falchion_Gold` 25.72, `_gladius_Leather` 26.55 (under `Model3D.HiltRail`), `_longsword_Iron` 16.95, `_katana_Bronze` 17.92 (under the new `Model3D.HiltRail2`, z 16.3…18.25), at x −23.15, grip X up, Y toward the room, the guard end at y 7.05, each on a `HiltCord` from the rail. Replaces `Legacy.HiltBenchHangingHilts_beforeRealHilts`. Hand edits. |
| `HudFocus` (round 2) | `sources`, `parts`, `parked`, `wanted` are strong tables (were weak-keyed: an Instance's handle is collected while no script holds it, so entries vanished and nothing hid); `forget(x)` on `x.Destroying` clears them. |
| `UiFx.topbarIcon(name, image, order, onTap)` | `Icon.new():setName():setImage():setOrder():oneClick()` from `ReplicatedStorage.TopbarPlus.Icon`, `selected` → `onTap`; `setEnabled(false)` while `MenuGui.Buttons` is parked in a `HudHold` (HudFocus hiding the HUD). |
| `MenuController`, `GemController` (round 2) | `topbarIcon("Settings", …, 2)` → the Settings window; `topbarIcon("DailyReward", …, 1)` → the daily window. GemController's `apply`: `dailyIcon:notify(noticeClear.Event)` when today's reward starts waiting, `noticeClear:Fire()` when it's claimed. `MenuGui.Buttons.Settings` and `.Daily` `Visible` false in StarterGui (wiring kept). |
| `ReplicatedStorage.TopbarPlus` | Allen's TopbarPlus v3.5.0 package, moved from Workspace; `READ_ME` (RunContext Client, makes an "Example" icon) `Enabled` false. |
| `ShopService` (round 2) | `holding` is a strong table, cleared on the clerk's `Destroying`. |
| `AnvilController` (pick first) | `enter` is now `enterView` (forward-declared): the camera, AnvilHud and points GUI only. `use()` on the prompt: `checkIngot()`, then `enterView()` with a blade still on the anvil, else `openIngotPicker()` over the room; the blade picker's pick runs `BeginForge` and then `enterView()` (if not in it) and `startBlade`. `choosing` is true while an anvil picker is up outside the view: `PromptHidden` closes it; `pickerClosed` clears it. A failed start toasts outside the view. |
| `SlotMarker.new(adornee, offset, state, near?)` | `near`: measure `SHOW_RANGE` from that part instead of the marker. `RackController` passes each slot's nearer rack prompt part (`Shelf1` / `Plinth` of the rack or its second), so a rack's markers show together with its prompt. |
| `Workspace.Plot.Smithy.OreRoller.Stand1-6` | No `LootBox` (in `Legacy.LootBox_beforeStands`). Each stand: `Foot` (iron, 1.6 × 0.25 × 1.6, on the floor), `Post` (wood, 0.6 square), `Pedestal` = the cap (WoodPlanks 1.4 × 0.22 × 2.6; the Collect prompt's part) with an iron `Band`, and the `Ore` ingot lying along plot z, 0.02 proud of the cap. Front row x 18.3 at z −7.05 / −10.2 / −13.35 (Stand1-3, ore centre 3.0 above the floor), back row x 21.1 at z −5.475 / −8.625 / −11.775 (Stand4-6, 4.2). Tags and `Upgrade` attributes unchanged. Hand edit: `build_workshop` still builds the crate. |
| `OreBoxShow` (stands) | No lid, hinge or glow: each rolled stand's copy rises from its ingot's rest `HOVER` 1.6 studs (from `RISE_AT` 0.1 over 0.55 s), spins and flickers until it locks in (2.0 s + 0.12 s apart), and drops back at `DROP_AT` 3.05; copies are parented to the roller. `RollTime` (ForgeService's `BOX_TIME`) unchanged at 3.6. |
| `ForgeService` (labels) | `OreLabel`: no plate or corner, text stroked (30, 20, 14), 16 px, `StudsOffset` 0.95, `LightInfluence` 0. |

## Bigger ingots, no hand limit (2026-10-24)

[[Sessions/2026-10-24#No hand limit, 1.7× ingots, labels that don't overlap]]. Supersedes, above: `MAX_INGOTS` / `CARRY_CAP` 6 and "Your hands are full" (ForgeService, RackService, Guide), Hook_CollectOre's refusal when ore still waits on Slots 2–6, "what didn't fit is rolled over", the ingot's 2.3 × 0.75 × 1.2 and its Grip `(0, -0.3, 0.35)`, the stands' 3.15 spacing and 1.4 × 2.6 caps, the Ingot Racks' 5.8 × 1.3 shelves, and `OreLabel` at 150 × 44 px, 16 px, `StudsOffset` 0.95.

| Script / instance | 2026-10-24 |
|---|---|
| `ForgeService` | No carry cap: `takeOre` is false only with no ore or someone else's; the Collect prompt always takes; a pull's `collectWaiting` takes every waiting ore; `Hook_CollectOre(plot, player)` is false only while that box rolls. `OreLabel`: `Size` `UDim2.fromScale(ore.Size.X, 1.1)` (studs: an ingot long), `StudsOffset` `ore.Size.Y / 2 + 0.6`, text `TextScaled`. ponytail note: carried ingots are Tools and save entries, so stack them if hoards ever slow pushes. |
| `RackService` | `take` has no carry cap. |
| `Guide` | No `MAX_INGOTS` branch (and no `anyHot` / `anyCold`). |
| `TycoonService.padVisual` | Label `StudsOffset` y = the pad marker's `LabelHeight` attribute, else 4.2. |
| `Workspace.Plot.Pads` OreStand2–6, MergeSlots, Lucky1–3 | `LabelHeight` 1.6. `Pads.IngotRack` / `IngotRack2` at plot (18.9, z 3.45 / 12.88), in front of their racks. |
| `SmithyCore.buildIngot` | Grip `CFrame.new(0, -0.56, 0.6)`: the measured grip scaled with the bar (not measured again). |
| `ReplicatedStorage.SwordParts.Ingot` | 3.91 × 1.275 × 2.04 (1.7×). Every stand `Ore` and `IngotRack.Slots.Slot1–12` match it. `ItemPicker`'s card art keeps its own size; the furnace's glowing bar is a separate small part. |
| `Workspace.Plot.Smithy.OreRoller.Stand1–6` | Front row x 18.3 at z −6.3 / −10.6 / −14.9 (Stand1–3), back row x 21.1 at −4.15 / −8.45 / −12.75 (Stand4–6), template plot space. `Pedestal` 2.3 × 0.22 × 3.4, `Band` 2.34 × 0.06 × 3.44, `Ore` 0.02 over the cap (centre 2.96 front, 4.16 back). Stand4 is beside the lever, past its swing. Hand edit. |
| `Workspace.Plot.Smithy.IngotRack`, `IngotRack2` | Two bars a shelf: `Shelf0–2` 8.7 × 2.3 deep at x 22.0, `Back` 9.2 wide at x 23.1, `SideL/R` 2.44 deep at x 21.98, `Top` 9.4 × 2.49 at x 21.945. Rack 1 centred z 3.45 (left end unchanged), Rack 2 z 12.88 (both at the same x now). Slots at x 21.95, z centre ± 2.085, y 0.9275 / 2.4375 / 3.9875. Hand edit. |
| `Workspace.Plot.Smithy.WorkshopFittings` (shelf, brackets, bundles, crate over Rack 2) | Raised 0.5, clear of Rack 2's top. |

## Workshop rearranged (2026-10-24)

[[Sessions/2026-10-24#Planner moves applied]]. Supersedes, above: the stations' plot positions (the stands, racks, furnaces, anvils, finishing stations), the pads' spots, and the shelf over Rack 2 at z 12–18.

| Script / instance | 2026-10-24 |
|---|---|
| `EmployeeService.spot` | Turns the `STAND` offset by the station model's (or its nearest model ancestor's) `Turned` attribute before adding it. `STAND` stays as the stations stood before the moves. |
| `Workspace.Plot.Smithy` stations | Moved by the planner (table in the session note). `Turned` on Anvil2 (90), Forge and Forge2 (90), EtchingTable (90), EtchingTable2 (270), HiltBench (90), OreRoller (270). Anvil and Anvil2 0.6 higher, on the `WorkshopFittings.Hearth` (slate, top 0.3). `Anvil2.AnvilStone` clipped to the hearth, 0.06 over it. Hand edits. |
| `Workspace.Plot.Pads` | The workshop pads moved with their stations: an upgrade's own pad, OreStand/Lucky/Merge with the ore stands, Heat with the Furnace, Crafter with Anvil 2, Etcher with Etching Table 2, Stocker with the sword rack, the five blueprint pads together. |
| [Workshop layout planner](https://claude.ai/artifact/4M7MEYLC4ekJ5Xk4MfGSSA) | A claude.ai page with a db: the plan comes from an Edit export of the template (every visible part's top-down outline, walls, pads, prompts); moves are kept in `layout/moves` as `{ id: { dx, dz, rot, about } }` (plot studs, degrees of yaw about `about`). To apply: `PivotTo(pc * CFrame.new(about + d) * CFrame.Angles(0, rot, 0) * CFrame.new(-about) * pc:ToObjectSpace(pivot))` for the station and its pads, add `rot` to `Turned`, check overlaps, re-export, republish and empty `layout/moves`. `IngotRack.Slots.Slot7–12` are Ingot Rack 2's (their `Upgrade` attribute): move them with IngotRack2, not with the IngotRack model they sit in. |

## Smaller ingot, rack slots re-seated (2026-10-24)

[[Sessions/2026-10-24#Rack ingots back on their shelves, the ingot 25% smaller]]. Supersedes, above: the ingot's 3.91 × 1.275 × 2.04, Grip `(0, -0.56, 0.6)`, the stand caps' 2.3 × 3.4 and the rack slot positions.

| Script / instance | 2026-10-24 |
|---|---|
| `ReplicatedStorage.SwordParts.Ingot` | 2.93 × 0.96 × 1.53 (1.275× the first ingot); every stand `Ore` and `IngotRack.Slots.Slot1–12` match it. |
| `SmithyCore.buildIngot` | Grip `CFrame.new(0, -0.4, 0.45)`. |
| `IngotRack.Slots.Slot1–6` / `Slot7–12` | Seated from Ingot Rack's / Ingot Rack 2's own shelves: x at the shelf's middle (22.0), z the rack's centre ± a quarter of its inner width (2.15), 0.01 over each shelf. |
| `OreRoller.Stand1–6` | `Pedestal` 1.8 × 0.22 × 3.25, `Band` 1.84 × 0.06 × 3.29, `Ore` 0.02 over the cap. |

## GUI review fixes (2026-10-24)

[[Sessions/2026-10-24#GUI review against the Roblox UI skills]].

| Script / instance | 2026-10-24 |
|---|---|
| `Hud` | `here(p)` = `p − HudGui.AbsolutePosition`: a screen point in the HudGui's offsets (it ignores the inset; `AbsolutePosition` doesn't). `centre()` (the flying coins' target) and `pop()` (the "+N") go through it. |
| `DeliveryController` | `call()` returns nil at once while `busy` (one `DeliveryRemote` request at a time); the Cart's Buy returns early while `busy`. |
| `EmployeeController` | `act()` returns false at once, no toast, while `busy` (one `EmployeeRemote` request at a time). |
| `ServerStorage.UIPackCopies` | The six `_Pack` screens, moved out of StarterGui. |
| `MailGui.Window`, `MailController` | Position (0.5, 0, 0.5, 29) (was 0.5, 0); `UiFx.fit(win.Fit, 650, 570)` (was 460): 0.7 and 322 tall on a 382–390 px phone, under the top bar. [[Sessions/2026-10-24#Mail and Crew windows fit a phone]] |
| `CrewGui.Window` | 780 × 460 (was 520): `UIPadding` top / bottom 16, `Rule` y 54, `Roster` / `Stats` / `Station` / `Staff` at y 62, 724 × 366; `Stats.Panel` and `Staff.Panel` 144 tall; `Station.List` 300 tall; `Tabs` y 62. Fit unchanged (980 × 560): 322 tall at 0.7. |
| `Workspace.Plot` stations, round 2 (2026-10-24) | EtchingTable centre z 6.45, EtchingTable2 −3.44, PolishStation 18, OreRoller 1.48 (template plot space); their pads with them. [[Sessions/2026-10-24#Planner moves, round 2]]. |
| `Workspace.Plot.PlayerSpawn` | 10 × 0.3 × 5.7, centre z 7.15 (was 8 deep at z 6): starts 0.5 behind the ore stands. Moves back 12 with the Upgraded Store like the workshop. |

## Soft-bevelled stations (2026-10-24)

[[Sessions/2026-10-24#Soft-bevelled stations]]. Supersedes, above: the stations' blocks and cylinders being Parts.

| Script / instance | 2026-10-24 |
|---|---|
| `Workspace.Plot.Smithy` OreRoller, IngotRack(2), HiltBench, PolishStation, EtchingTable(2), SwordRack(2) | Every visible block / cylinder Part is a MeshPart cloned from `StationBevels`, with the Part's name, CFrame, size, colour, material, collision flags, attributes and children. `CollisionFidelity` Box (blocks) / Hull (cylinders). Hand edit: `build_workshop` still builds Parts. |
| `ServerStorage.Buildings3D.StationBevels` | 89 MeshParts from Model 113523110859732 (attribute `SourceAsset`), one per part size: `B<x>_<y>_<z>` / `C<length>_<diameter>` in millistuds (cylinders along X). To bevel a Part of a listed size, clone its key and copy the Part's properties over. |
| `ServerStorage.Legacy.<Station>_beforeBevel` | The nine stations as Parts, before the swap. |
| `Models/Stations/Bevelled/build_bevelled.py` | Blender: `build()` makes one bevelled mesh per key from `stations_parts.json` (exported from Studio) and assembles the stations for review; `export()` writes `StationBevels.fbx` (`roblox` preset). Bevel 0.2 × the smallest side, ≤ 0.09, 3/2/1 segments, weighted normals. New sizes: add them to the json, rebuild, upload again. |
| `ServerStorage.Builders.coplanar_check` | Checks Parts and wedges only, so it skips the bevelled stations; run it on `Legacy.*_beforeBevel` (the same flat faces). |
| `Workspace.Plot.Shop.Displays.WallRack1–4` | Bevelled the same way (blocks and the two `Gable` wedges; `CollisionFidelity` Box / Hull). Cradles keep `Holds`; `Legacy.WallRack<n>_beforeBevel` hold the Parts. [[Sessions/2026-10-24#The shop's wall shelves]] |
| `StationBevels` wedge keys | `W<x>_<y>_<z>`: a Roblox WedgePart (slope to −z). The mesh is about 3% under its key's size (the bevel trims the tips): set the part's full size on the clone. 103 shapes from Models 113523110859732, 70663660121319 and 80110813584400 (per-part `SourceAsset` on the later two). |
| `build_bevelled.py` (shelves) | Reads every `*_parts.json` (`stations_parts.json`, `shelves_parts.json`); `wedge_mesh` builds wedges turned 180° about the vertical to cancel Roblox's import turn; `export(keys, name)` writes only the given keys. |

## Station decorations on the walls (2026-10-24)

[[Sessions/2026-10-24#Station decorations on the walls]]. Supersedes, above: where the finishing stations' wall decor sits.

| Instance | 2026-10-24 |
|---|---|
| `Plot.Smithy.EtchingTable(2).Dress` | `Sign*` and `RackArm`/`RackPeg` + `PropSwords` turned −90° about Y onto the right wall (wall ends at plot x −23.52). Sign centres z 6.4 / −3.44; racks z 3.3 / −5.1. No `InkShelf`, `Bracket`, `InkJar`, `ChiselBoard`, wall `ChiselHandle`/`ChiselTip` or `Scroll*` any more (`Legacy.EtchingTable(2)_omittedDecor`). Counter pieces (cradles, case, stylus, andon, `DemoSword`) unchanged, so `EtchPlayback`'s hiding is unaffected. |
| `Plot.Smithy.PolishStation.Model3D` | `Sign*` x −0.5; `StoneShelf`/`Bracket`/`Whetstone` x −0.5, z +2.05; `Peg`s and `PropSwords` x −0.5, z +1.5. No `ClothRail`/`HangingCloth` (`Legacy.PolishStation_omittedDecor`). |
| `Plot.Smithy.HiltBench` | `Model3D` `Sign*`, `Guard*`, `HiltRail(2)`, `Peg` and all of `PropHilts` / `PropSwords` z +0.22 (flush to the back wall). |
| `ServerStorage.Legacy.<Station>_beforeWallDecor` | EtchingTable, EtchingTable2, PolishStation, HiltBench before the move. Hand edits: `build_workshop` still builds the old decor. |

| `ShopService` `showTill` (2026-10-24) | `TillSign.Plate` is transparent (no `UICorner` / `UIStroke`); `Plate.Amount` has a `UIStroke` (43, 28, 19), 2 px. [[Sessions/2026-10-24#The Cashier's till without a backing]] |

## NPC review fixes (2026-10-24)

[[Sessions/2026-10-24#NPC review (roblox-npc-ai)]].

| Script | 2026-10-24 |
|---|---|
| `NpcWalk` | `to`: a private `follow` (one path, or the fallback points) is tried, then once more with a fresh path; stuck = `STALL` 2 s without `HEADWAY` 0.25 studs of progress, or the old timeout; still stuck, it steps into place (target X/Z, its own height and turn) and returns false. `steady(hum)`: FallingDown, Ragdoll, Climbing off. |
| `ShopService` | `Slot.customer` is the customer's ctx or false. `runCustomer` sets `ctx.slot` / `ctx.npc`; `sendCustomer` frees the slot and destroys the NPC on an error. `makeNpc` calls `NpcWalk.steady`. |
| `EmployeeService` | `makeWorker` calls `NpcWalk.steady`; `walkTo` is just `NpcWalk.to` (it steps into place itself now). |
| `StreetLife` | Requires `NpcWalk`; `make` calls `NpcWalk.steady`. |

## Polish sparkle wave (2026-10-24)

[[Sessions/2026-10-24#The polish sparkle runs along the blade]]. Supersedes both `SwordRenderer` glint rows above.

| Script | 2026-10-24 |
|---|---|
| `SwordRenderer` | Requires `Shared.BladeCore`. `wavePath(params)`: `WAVE_POINTS` 14 blade-space points from u 0.04 to 0.96, halfway between the ridge line and the edge on each station's normal from `BladeCore.centerline`, lerped between stations. `glint(part, path, shimmer)`: one Attachment + ParticleEmitter (sparkles_main, `LockedToPart`, life 0.3–0.4 s, size 0.45 / 0.7 with `Shimmer`) per point; every 2.5–4.5 s (1.2–2 s with `Shimmer`) emits one per point in order over `WAVE_TIME` 0.5 s. With `Shimmer`, the `PointLight` attachment steps along the same points and its brightness tweens to 3 and back over the wave. The stop function only ends the loop; the attachments go when `free()` destroys the blade part. |
| `SwordRenderer` (later the same day) | Supersedes the `glint` description in the row above: one Attachment + ParticleEmitter (`LockedToPart`, life `WAVE_TIME` 0.7 s, size 0.55 / 0.8 with `Shimmer`, held from 0.15 to 0.85 of its life, RotSpeed 180). Each sweep emits one particle at `path[1]`, then on Heartbeat moves the attachment to the point at `s²` of the way along `wavePath` (`s` = time / `WAVE_TIME`, lerped between the 14 points). The `Shimmer` `PointLight` is on the same attachment. Requires `RunService`. |
| `SwordRenderer` (glare, later still) | Supersedes the sparkle in the row above. `GLARE` = `rbxasset://textures/particles/explosion01_implosion_main.dds`; `WAVE_TIME` 0.6, `GLARE_LENGTH` 0.22 of the path. `along(path, u)` lerps the 14 `wavePath` points. `glint`: a `Beam` (Stretch, Segments 1, width 0.3 / 0.45 with `Shimmer`, FaceCamera, ZOffset 0.1, LightEmission 1, LightInfluence 0, Brightness 4) between `tail` and `head` attachments; per Heartbeat `front = s²·(1 + GLARE_LENGTH)`, head at `front`, tail at `front − GLARE_LENGTH` (clamped to the path), Transparency `1 − sin(πs)`; transparent between sweeps. The `Shimmer` `PointLight` is on `head`. |

## Refinements 5 (2026-10-25)

[[Sessions/2026-10-25#Refinements 5]]. Backups: `ServerStorage.Legacy.<Name>_beforeRefinements5` (and `OreRoller_beforeRefinements5`).

| Script / instance | 2026-10-25 |
|---|---|
| `ForgeService`, `ForgeController` | No "<metal> ingot collected" notice (`takeOre`) and no "Ingot loaded" toast. |
| `RewardCard` | A first-collected metal (`Discovered`) is `ItemPicker.toast("New metal: X")`, not a card. |
| `Plot.Smithy` `IngotRack`, `IngotRack2`, `SwordRack`, `SwordRack2` | `ModelStreamingMode = Atomic`: `RackController` builds a marker per slot once, from `Slots` as it finds them, so slots still streaming in had none (4 of 6 / 1 of 6 / 3 of 6). |
| `PromptFilter` | Every prompt it guards is in `prompts`. 4×/s: a prompt near your head (within its distance + 2) whose part a ray from your head can't reach gets `MaxActivationDistance` 0 locally (`reach` keeps the old value and restores it once clear). The ray ignores the prompt part's first Model ancestor, characters/NPC models, and parts that are non-colliding or Transparency ≥ 0.95 (up to 6 skips). |
| `StarterGui.CrewGui` | `IgnoreGuiInset` true, `DeviceSafeInsets` (the Dim reaches the top). |
| `Plot.Smithy.Anvil2` | Turned to face as `Anvil` (look −z world); `AnvilStone` (the mat) left where it was; `Turned` stays 90 so the crafter's `STAND` spot stays on the room side. `Face.CrafterPrompt` replaced by a copy of `Anvil.Face.ForgePrompt`. `EtchingTable2.Top.EtcherPrompt` deleted. |
| `AnvilController` | `prompt` / `face` / `mount` become the triggered `ForgePrompt`'s anvil (`ProximityPromptService.PromptTriggered`, any `ForgePrompt` under your `Smithy`); `PromptHidden` likewise. `leave()` re-enables the prompt only without `CrafterOff`. `finish()`: on a saved blade, straight to `leave()` (no `SHOWCASE_TIME`, no result line); a failed save still shows "Couldn't save that blade". |
| `EmployeeService` | `syncPrompt` gone (no crafter/etcher prompts). `oneSword` step 3 waits while your root is within 3 studs (flat) of `Anvil2.Face`, then `claim(Anvil2)` → walk, hammer → `release(Anvil2)`. `inUseSign(station, on)`: an "In use" BillboardGui on `Anvil2.Face`, styled like "Rack Full!", from `claim` / `release`. |
| `EmployeeController` | No `PromptTriggered` handler: the crew window opens from the crew button only. |
| `EmployeeController`, `CrewGui` (staff rosters, 2026-10-26) | `rosterRole` (nil = crafters) picks what the `Roster` page shows; tabs set it and `show("roster")`. `fillStaffRoster(role)`: `Templates.Card` per member (`members = { state.staff[role] }`), named `Working`, stars/bars/price hidden, `Level` shown, `Trait` = `statusLine(…, staffLine(role, rec), …, <upgrade>Status)`; `staffLine` = the `PERK_ROW` perk or Walk Speed. `Window.Header.Back` (‹, a Close copy, shown on the Staff page; title at x 62) → `rosterRole = staffRole`, `show("roster")`. The status loop refreshes the staff card by `rosterRole`. With no crafter, `show("roster")` falls to `firstStaff()`'s roster. |
| `MailController` | `fitting(why)` → (count, cheapest fitting sword); Hand in calls `Commission("deliver", id, sword)` / `Order("fill", id, sword)` with it directly. No picker. |
| `Shared/Employees` | `LEVEL_AT` {0, 10, 30, 70, 150}, `MAX_LEVEL` = 5, `STAFF_SCALE` 2.5 (replaces `SWORDS_PER_LEVEL` 3 / `JOBS_PER_LEVEL` 5 / `MAX_LEVEL` 11); `level(made, scale?)` returns (level, into, needed); `QUALITY_STEP` 8. |
| `Shared/Upgrades` | `Lucky1–3` and `LUCK` removed; `luck(plot)` = `mergeFactor(merges)`. `Furnace2.after` = `"Heat3"`. |
| `TycoonService` `padVisual` | One TextLabel "Name · price" (commas; the merge pad "Merge Ore Slots · Luck xN"), BillboardGui 240×30, `MaxDistance` 40. |
| `TycoonController` | Every 0.2 s: each plot's pad `Label` enabled only within `LABEL_RANGE` 14 studs of your root. |
| `Plot.Pads` | `Lucky1–3` deleted. `OreStand2–6`, `MergeSlots` moved to roller-local x −1.9 (the Lucky pad's spot). The five blueprint pads at plot (2.0, 16.2), the centre of `WorkshopFittings.AnvilStone`. |
| `Plot.Smithy.OreRoller.Lever` | `ScaleTo(1.6)`; `Arm` X 0.55; `Knob` ×1.25. Base centre at roller-local (−7.4, −2.74, 4.3), its bottom 0.04 under the floor top. `Machine` (the `RollPrompt` part) on the knob, `CanCollide` false, `PivotOffset` set so the roller's pivot is unchanged (`Machine` is its PrimaryPart). |
| `StarterGui.SpotlightGui` | DisplayOrder 8, `IgnoreGuiInset`. `Hole` (round, no ring since Allen asked for it gone); `ShadeTop/Bottom/Left/Right` frames (black at 0.45) round it (the first try, a 3000-thick UIStroke, didn't render). `Guide` places the hole at the button's `AbsolutePosition` minus the screen's own (AbsolutePosition is always below the top bar). Input passes through. |
| `Guide` | `goal()` returns (text, target, button). Button steps: "Open your mail" → `MenuGui.Buttons.Mail`; "Hand it in from the mail" → the Mail button, or with the mail open that letter's `HandIn` (`mailButton(key)`); `gemTour`: `GemTour` "todo" + tutorial done + gems > 0 + the daily window closed → "Open the Gem Shop" on `Buttons.Upgrades`; "open" → "Gems buy boosts for your shop that last" on `GemShop.Body` (since 2026-10-27 the gate and the "open" step changed: [[#Tutorial fixes (2026-10-27)]]). RenderStepped places the hole over the button (+ the top-bar inset for a non-inset screen) while it and its parents are visible; `GuideGui` DisplayOrder 9 while it shows, else 1. |
| `GemController`, `GemService`, `SmithyCore.FUNNEL` | Funnel step 11 "Opened the Gem Shop" (saved like the others). Gems `state` has `toured`; `("tour")` logs step 11. The controller sets the local player attribute `GemTour` "todo" when not toured, "open" when the shop opens (and calls `tour`), clears it on close. |
| `ShapingRules` | `sandRate` 0.5 cm/s, `sandRadius` 0.04; `Rules.sand(s, u, seconds)` takes width off workable stations near u (cosine falloff), never under the target; returns cm taken. `Rules.smooth` and `timing.smooth` removed; `canSmooth` gates the Sand button. |
| `ShapingPrototype` | (Later the same day: the diagram panel is back, at the top; see the row below.) First: no diagram, a 64 px top bar (chip, match, legend); buttons at the bottom; Strike (touch) above them. `outline`: 2 × (N − 1) SmoothPlastic `TargetLine` ledges (white 245, no Neon) along the target's ring-4 edge, `LEDGE` 0.012 studs out of each face (centred at ± (thick/2·S + LEDGE/2)), `LINE` 0.008 across; `placeBlade` places them with the blade and shows only the face whose normal faces `TOWARD_CAMERA` (the camera's `ELEVATION` 64° direction, shared with `cameraFrame`). `cameraFrame` looks at the blade (x as before, y 0.05, z 0), not 0.75 in front of it. `paint` tints each station toward `TOO_WIDE` / `TOO_NARROW` by its error (and repaints on `shapeChanged`). `tool` "hammer" / "sand" (`swapTool`, the Sand / Hammer button); in sand mode a held mouse button or touch sets `sanding`, and RenderStepped runs `Rules.sand(state, smoothU, dt)` with a scrubbing `SandBlock` in place of the hammer. `info()` has `canSand`, `tool`. |
| `SaveSpec` | The luck check is merge-only (`luck` 1 → 2 at 2 merges, `Lucky1` gone) plus `Furnace2.after == "Heat3"`: 89/89. |
| `ShapingRulesSpec` | Sanding checks replace smoothing's: 27/27. |
| `ShapingPrototype` (diagram back, 2026-10-25) | The 240 px panel (chip, match, legend, the 150 px face-on `plot` with `cols`, `band`, `aimLine`, `arrow`, `readout`, `worstMark`) at the top (`AnchorPoint` 0.5, 0; y 12), `UIScale` min(1, viewport height / 600). `drawScore` redraws the columns, the match, the worst mark and the Sand button; `drawAim` (every RenderStepped) the aim band (the sand reach in sand mode), line, arrow (gold ▲ when sanding) and readout. `aimAtPlot` + `plot.InputBegan/Changed` aim from the diagram. The 3D `TargetLine` outline is gone (tried as face lines, a fin, ledges and a screen-projected line). `cameraFrame` shifts the camera up by (panel height + 12 − 52) / 2 px so the blade sits mid-way between the panel and the buttons. `ELEVATION` / `TOWARD_CAMERA` are file constants. |
| `ShapingPrototype` (silhouette, 2026-10-25) | The plot is a true-shape silhouette, not the width chart: `spineAt[i]` / `toEdge[i]` (cm, from the target's ring 1 and ring 4, turned by `YAW` so base → point runs left to right), `STRETCH` 2.5 along the normal, `SUB` 2 columns per station gap (`COLS` = 127). `layout()` fits the blank (`C.blankWidth`) to the plot whenever its unscaled width changes (`AbsoluteSize / fit.Scale`), sets `scale` (px per cm), `origin` and `colW`, and draws the target outline once (`outlineSegs`: edge, back line, base end; 2 px white). `strip(frame, a, b, across)` lays a rotated frame from a to b. `drawScore` lays each column's body / wide / gap strips from the back line; `drawAim` puts the band, line, arrow and readout on the curve; `aimAtPlot` maps x back to u along the back line. `FLOOR`, `K`, `y()` and `spineLine` are gone. |
| Test Anvil (2026-10-25, Studio only) | `Plot.Smithy.TestAnvil` (a copy of `Anvil`, `StudioOnly` attribute, `Face.ShapePrompt`, `Face.TestSign`) at plot (−8, 12). `StarterPlayerScripts.TestAnvil` (returns at once outside Studio): `ShapePrompt` → hot-ingot picker → learned-sword picker (silhouette art, as the anvil's) → `ShapingPrototype.start({ blueprintId, onFinish })`; `onFinish` invokes `Remotes.FinishShaped` and the prototype leaves when it returns true. `SmithService`: in Studio, `FinishShaped(ingotId, blueprintId, match)` (allowCall, blade cap, a number, a learned blueprint, the hot ingot) → `takeIngot` → a blade with `AnvilScore.forPercent(round(match))` and zero refinement, funnel 4; outside Studio it deletes every `TestAnvil` from `workspace.Plot` / `ServerStorage.PlotTemplate`. `ShapingRules`: `CONFIG.refWidth` 3.2; `Rules.new(target, { scale, symmetric })` puts `k`, `symmetric`, `center` and the scaled `blank`, `minWidth`, `maxWidth`, `strength`, `perfect`, `tolerance`, `flag`, `sandRate` on the state, used by `reset`, `preset`, `strike`, `score`, `canSmooth`, `sand`; `params` moves spine and edge about `center` when symmetric. `ShapingPrototype.start(opts)`: `blueprintId` (default katana), `onFinish`; scale = the target's widest / refWidth; the silhouette's columns are body + `wideA/wideB` + `gapA/gapB` from `span(w, t)` (0..w, or centred). The vault keeps `Prototypes/sword-shaping/roblox/TestAnvil.luau`. |
| `SwordMeshCache`, `SwordRenderer` (shine fix, 2026-10-25) | `SwordMeshCache.polishLevel(refinement)`: average polish → 0..`POLISH_MIRROR` (= `LEVELS`, 2); `shine` uses it for `BladeShine<level>`. `SwordRenderer` starts `glint` when `polishLevel == POLISH_MIRROR` (or `Shimmer`), not when the blade's `MaterialVariant` is `BladeShine2`, which textured and non-metal blades never wear. |
| `Shared/EtchPatterns` (etch refinement, 2026-10-25) | `EtchPatterns.strokes(id, length, widthAt)` calls a generator with `capped` (width ≤ `EtchCanvas.MOTIF_CM`) and `ctx = { limit = limitOf(length, widthAt), strips = EtchCanvas.strips(length, widthAt) }`, then moves every point (`ipairs`, and `fill` corners, each once) up by half the width over the cap. `limitOf`: first x past 0.4 length where width falls > `SLOPE` 0.25 cm/cm, else length − 1.1 × width(0.95 length). `usable(length, widthAt, limit)`. Generators `(length, widthAt, ctx)`; Fracture's `shard(poly, widthAt, ink)`; Fracture shards and Falling Stars trails set `stroke.ink`. [[Sessions/2026-10-25#Etch refinement]] |
| `Shared/EtchCanvas` (2026-10-25) | `HALO` 0.07 (was `GLOW_CM` 0.24); `self.glowCm = EtchCanvas.halo(mean of min(colW, MOTIF_CM))`. Pieces carry `ink` (`stroke.ink` or `{ solid = 0, fade = glowCm }`); `_raise(i, cover, d, ink)`: halo full to `solid`, gone at `solid + fade`. Exports `MOTIF_CM` 7, `THICK`, `CORE`, `halo(mean)`. |
| `Shared/BladeEtch` (2026-10-25) | `surface().swAt` and `build`'s sample widths divide by `clamp(w, MIN_WIDTH_CM, MOTIF_CM)`; `bandReach` and `build` scale the reach by `min(1, MOTIF_CM / width)`. Unchanged below 7 cm. |
| `SwordMeshCache.bandColor(accent)` (2026-10-25) | `accent:Lerp(white, EtchCanvas.CORE)`: the Color `SwordRenderer`, `ItemPicker` and `PolishController` give a band etch's part. |
| `ServerStorage.Tests.EtchingSpec` (2026-10-25) | Canvas checks over all seven blueprints: 63/64 (the demo-tray check fails since the tray went, 2026-10-23). |
| `ShapingRules` (fewer hits, 2026-10-25) | `CONFIG.strength` 0.4, `radius` 0.11, `perfect` 0.16, `tolerance` 0.5, `smoothRate` 8; `smoothAt` and `Rules.canSmooth` removed. `Rules.sand(s, u, seconds)`: each workable station over the target near u loses `(sandRate + smoothRate × max(0, e − neighbours' weighted mean e)) × falloff × seconds`, floored at the target (e = width − target from a snapshot; weights `falloff(·, sandRadius) × mask`). [[Sessions/2026-10-25#Anvil shaping: fewer hits, a true-width guide, sanding any time]] |
| `ShapingPrototype` (fewer hits, 2026-10-25) | `hammering` / `hammerInput`: MouseButton1 down with the hammer out, or the touch Strike button's `InputBegan`, sets it; `runQueued` queues another strike while it's set (not with the card up); MouseButton1 up, that touch ending or `swapTool` clears it. Silhouette: no `STRETCH`; `PLOT_MIN` 80 / `PLOT_MAX` 170; `layout()` sets `plotH` from the blade's span at full width and resizes `plot` and `panel` (plotH + 90); the panel's `UISizeConstraint` is gone. `sandButton` always visible. `Inspect` reports `hammering` (no `canSand`). |
| `ShapingRulesSpec` (2026-10-25) | Five sanding checks replace the eight gated ones: 28/28. |
| `BladeCore.withShape(blade, params, shape)` (2026-10-26) | Replaces `params.spine` / `params.edge` per station from `shape` (cm): single-edged `spine = shapes[5].spine`, `edge = spine − w`; double-edged about `(shapes[5].spine + shapes[5].edge) / 2` ± w/2. No-op without a shape of `stations` length. [[Sessions/2026-10-26#Test Anvil blades keep their shape]] |
| `SwordMeshCache` (2026-10-26) | `blade(id, refinement, shape?)`, `overlay(id, refinement, shape?)`, `etch(id, refinement, pattern, body, accent, spread, shape?)`: `shapeKey(shape)` (`"|S"` + widths to 0.001) appended to the key; a shaped key never uses a bake; params go through `BladeCore.withShape`. |
| Blade `shape` (2026-10-26) | `SmithService.FinishShaped(ingotId, blueprintId, match, widths?)` validates and stores `blade.shape`. `SmithyCore`: `Blade.shape`, in `encodeBlade` / `decodeBlade`, `publicState` blades and swords, `buildSword` attribute `BladeShape` (JSON). `RackService` sword lists carry it. Readers: `HiltBenchController` (seat view, blade card), `SwordRenderer` (`BladeShape`), `Hotbar` (sig and art), `ItemPicker` (`Art.shape`), `EtchPlayback`, `PolishController` (`withShape` on its live params, its etch, its card), `ShopController`, `EtchingTableController`, `RackController`, `RewardCard`, `DeliveryController` (`art.shape`). `ShapingPrototype` `onFinish(match, widths)`; `TestAnvil` passes them on. `SaveSpec` 90/90. |
| `SwordMeshCache` baking (2026-10-26) | `bakeLive` (true). `bakeContent(editable)` → `CreateDataModelContentAsync` content or nil; `bakeMesh(from, mesh)` → `CreateMeshPartAsync(content, Box collision)` with `from`'s Name, Color, Material, Transparency, Anchored, Massless, CastShadow and collision flags. `blade`, `overlay` and the band `etch` bake their live mesh and destroy it (`view:destroy()` / `part`, `mesh`); a stroked `etch` sets the overlay's `TextureContent` to the baked canvas image and `canvas:destroy()`s. Each falls back to the live mesh when the bake returns nil. [[Sessions/2026-10-26#Live sword meshes are baked]] |

## Fixes: picker grid, mail rework, mailbox (2026-10-26)

[[Sessions/2026-10-26#Fixes: picker grid, mail rework, mailbox]]. No Legacy backups.

| Script / instance | 2026-10-26 |
|---|---|
| `ItemPicker` | `UiFx.fit(REGULAR.Fit, 940, 760)`, `UiFx.fit(COMPACT.Fit, 480, 500)`. `render`: `maxCols` 3 down to 1 while `(cols × cell + gaps + chrome) × scale` overflows the width; `maxRows` 2, or 1 when two rows overflow the height under the top bar; `grid.Grid.FillDirectionMaxCells = cols`. |
| `StarterGui.PickerGui` `Window.Cards`, `CompactWindow.Cards` | `Grid.FillDirection` Horizontal, `ScrollingDirection` Y, `AutomaticCanvasSize` Y (the compact one filled down one row and scrolled on X). |
| `ForgeService` `ForgeTake` | No `notice` ("Hot X Ingot! Take it to the anvil"). |
| `Shared/Senders` (new) | `list` of { id, name, role, look (skin, shirt, pants, outfit as `Employees`), lines }; `byId`; `ORDERS` (the eight order writers); `get(id)` (falls back to `guard`); `line(id, n, sword)` picks line `n` and fills `{sword}` with a/an. |
| `Shared/Commissions` | `giver` is a Senders id (`captain`, `swordsman`); `letter` text. Statuses offered (new, waiting for Accept) → active (accepted) → done. |
| `Shared/Orders` | `GIVERS = Senders.ORDERS`; an order has `at` (os.time() made) and `accepted`; `prose(o)` ("polished Katana", "Wakizashi in Uncommon metal or better"); `letter(o)`; `decode` keeps `at`/`accepted`, an unknown giver becomes `guard`. Since 2026-10-26 also `read` (opened in the mail). |
| `Shared/Upgrades` | `Mailbox` (15, no `after`). |
| `SmithyCore` | `MAIL_LOG` 20; `SmithData.mailLog` { giver, title, text, coins?, gems?, status "done" / "declined", at }, newest first: in `fresh`, `encode`, `decode` (odd entries dropped, at most MAIL_LOG), `publicState`. `FUNNEL[8]` "Accepted the first letter". `mailRead` { [commissionId] = true } (2026-10-26): story letters opened; `fresh`, `encode` / `decode` (unknown ids dropped), `publicState` as a list. |
| `ShopService` | `logMail(d, giver, title, text, status, coins, gems)`. `offerCommission` and `refillOrders` need the plot's `Bought_Mailbox`; `onPlot` listens for it (offer, refill, push). `Commission("accept", id)` (was "read"; funnel 8) and `("deliver", id, sword)` from offered or active, logged done. `Order("accept", id)` sets `accepted`; `("decline", id)` removes it, logs declined, refills; `("fill", id, sword)` logs done. `Commission("read", id)` → `d.mailRead`, `Order("read", id)` → `order.read` (2026-10-26), each pushing once. |
| `EmployeeService` | Also poses every `Shared/Senders` look into `ReplicatedStorage.Senders` (same `dress`). |
| `Plot.Shop.Mailbox` | Model (TycoonItem, Upgrade `Mailbox`) at plot (10, −49.3), facing the street: `Post`, `Foot`, `Box`, `Band`, `RoofFront`/`RoofBack` wedges, `Ridge`, `Slot`, `SlotLip`, `FlagPole`, `Flag`. `Plot.Pads.Mailbox` on the same spot. |
| `StarterGui.MenuGui.Buttons.Mail` | `Visible` false (MailController shows it with the Mailbox); `Icon` `rbxassetid://94916333436167` (since 2026-10-26 Allen's orange mailbox, `rbxassetid://87335653488899`). |
| `StarterGui.MailGui` | `Window.Header.Back` (‹, a copy of Close on the left; letter view) and `ActiveOnly` (pill with `Box.Tick` and `Label`; list view). `Window.Letter` (516 × 340): `Portrait` (ViewportFrame 96), `Sender`, `Role`, `Paper.Text`, `Want.Title` + `Want.Reward`, `Buttons` (`Status`, `Decline`, `Accept`, `Send`). `Templates.Letter`: `Portrait` (72), `Info` moved right, `HandIn` → `Send`, `Open` (a full-row TextButton under it); `Info.Top.New` is the status chip. `Popup` (TextButton 340 × 96, anchor (1, 0.5) at (1, −16, 0.5, 0), `HudPart`, `Fit` UIScale): `Portrait`, `Title`, `Hint`. |
| `MailController` | Rewritten round `letters()` (story letters, orders by `at` desc, then `mailLog`), each { key, giver, title, text, coins, gems, status new/accepted/done/declined, story, fits, accept, decline, give }. `reading` = the letter view's key; `render` shows list or letter; `activeOnly`; `portrait(frame, giver)` clones `ReplicatedStorage.Senders.<id>` (head and shoulders). `checkNew` pops up a letter that arrived since the last state, or an unread story letter (`read` = opened this session); `POPUP_TIME` 8 s for orders. The Mail button follows the plot's `Bought_Mailbox`. Dot: a new letter or something you can send. **Since 2026-10-26:** each letter has `read` (state's `mailRead`, `order.read`; the history true); `isRead(e)` also counts `read[key]`, opened here before the server answers. `render` sends `"read"` the first time a letter opens. Dot and the row's New chip = unread; `checkNew` uses `isRead`. |
| `Guide` | `mailButton(key, want)`: shut → `Popup` if showing, else the Mail button; letter view → its `want` button (or Back); list → the row's `Send` (want "Send") or the row. After the first sale with no Mailbox: "Buy the Mailbox" at `Pads.Mailbox` (or the tantō loop when short). Offered letter: "Read the letter" / "Open your mail" / "Open the letter" / "Accept the request". "Send it from the mail" (was "Hand it in"). |
| `SaveSpec` | 95/95: an order's sender, arrival and Accept; the mail's history and its cap; the letter's wording; a/an. 97/97 since 2026-10-26: an order's read flag; story letters read (unknown ids dropped). Run it with edited `Shared` modules swapped for clones (the cached `Orders` was older). |
| `SlotMarker` / `ShopController` (bag marker by the pommel, 2026-10-26) | `SlotMarker.new(adornee, offset, state, near?, fullAt?)`: while full, `StudsOffsetWorldSpace = fullAt()`, else `offset` (no camera-space offset). `ShopController.bindSlot`'s `bagSpot()`: the lowest slot-space X (Z for an upright slot, the Big Sword Stand) of the holder model's visible non-`DisplaySlot` parts, less `BAG_GAP` 0.4 → (edge, 0, 0), or `MID` + (0, 0, edge) upright; cached until the holder's descendant count changes; `BAG_FALLBACK` −2.3 before it streams in. Template: wall racks −2.27, display tables −2.83. `RackController` passes none. `ShopHud.Templates.SlotMarker`: `Plus` 33 px, TextSize 20; `Key` 18 px at (0.5, 15, 0.5, −14), Label 12; `ForSale` at (0.5, 0, 0.5, −23). [[Sessions/2026-10-26#Take-back marker beside the sword]] |

## Bigger plots with a fence (2026-10-26)

[[Sessions/2026-10-26#Bigger plots with a fence]]

| Where | What |
|---|---|
| `Plot.Fence` (new, template) | Model of 60 `Post` and 12 `Rail` Parts on the plot's edge: plot space x −40 … 44, z −45.5 … 76; front pieces only beside the buildings, with a gap at x −36 … −30 (side yard) and the shop door and bay mouth open. Not a TycoonItem, no tags; empty plots keep it. |
| `Village.Lots.Pad` | Each 84 × 0.16 × 124 at its slot × (2, ·, 14): plot space x −40 … 44, z −48 … 76. `Lots.Edge` (curbs) removed. `PlotSlot<lot>` unchanged (still the 48.5 × 96 marker and the pivot). Backup `Legacy.Lots_beforeBigPlots`. |
| `Plot.DeliveryBay.Yard` | 0.18 tall, top 0.20 (was 0.14 / 0.16, the new pad's top). |
| `Builders.build_plot_fence` (new; local `Models/Village/build_plot_fence.luau`) | `loadstring(...Source)()`: rebuilds `Plot.Fence` and resizes every lot's Pad to the same footprint. Constants at the top (`X0, X1, Z0, Z1`, `GAP`, `SPACING`). |

| `RoofHider` (2026-10-26) | Streaming-safe: `hook(building, shell)` connects `Shell.DescendantAdded` once per shell (weak table `hooked`); a new part under `Roof` or `Ceiling` gets `apply(p, fade[building])` (LocalTransparencyModifier, or a Light's Enabled). [[Sessions/2026-10-26#Floating roof pieces on join]] |
| `Plot.Smithy.OreRoller.Lever` (2026-10-26, chunky Parts) | 41 Parts: `Base` (the slab's bottom block, the pose reference for `LeverAnimator`), `BaseTrim<n>` (top block, chamfer Wedges and CornerWedges), `Body<n>` and `Panel<n>` (stepped blocks and Wedges), `Slot1`, a Cylinder `Arm` and a Ball `Knob`. The Arm and Knob are unanchored, massless and welded to `ArmPivot` (2.0 above the floor). Base and Body parts collide. `Machine` sits on the knob, with `PivotOffset` keeping the roller's pivot. Backups `Legacy.OreLever_beforeChunky` (the old lever), `Legacy.OreLever_meshChunky` (the mesh version). [[Sessions/2026-10-26#Ore stands aligned, parts lever in]] |
| `Plot.Smithy.OreRoller.Stand4–6` | Straight behind Stand1–3 (same x), 2.8 further back, 1.2 higher. Backups `Legacy.OreRoller_Stand<n>_beforeAlign`. |
| `Models/Stations/Chunky/build_chunky.py` | Blender: `hull(points, chamfer)` (convex hull, then a 1-segment chamfer on every edge, flat shaded) is the chunky style's building block. Not used in the game now (the lever went to Parts); `build()` makes the mesh lever in `Chunky.blend` and `export()` writes `OreLeverChunky.fbx` (`roblox` preset). |
| `ReplicatedStorage.WorldText` (2026-10-26) | Billboard templates, look set in Studio: `OreLabel` (`Title`, `Rarity`; 2.93 × 1.1 studs, 1.08 over the ingot; strokes 0.114 / 0.157 ScaledSize since [[Sessions/2026-10-27#Thinner ore label outline]]), `PadLabel` (240 × 30), `Nameplate` (`Avatar`, `Title`; 30 × 15 studs), `Tag` (`Role`, `Title`, `Level`), `TillSign` (`Plate.Coin`, `Plate.Amount`), `ForgeTimers` and `ForgeSlot` (`Time`), `FullSign`, `InUseSign`, `Speech` (`Text`), `BuyButton` (studs + px size, `Shadow`, `Fill` gradient + black outline, `GlowClip.Glow` radial image 72591074430716, `Button` text only; [[Sessions/2026-10-28#Chunky Buy button]]). Floating text: Gotham Bold, `UIStroke` 22,18,16 Round (ScaledSize on stud-sized text, FixedSize ≈ 0.2 × TextSize on pixel text). Cloned by ForgeService, TycoonService, PlotService, EmployeeService, RackService, ShopService and TycoonController, which set only text, data colours, offsets and parents. Change a look here, not in code. [[Sessions/2026-10-26#World text: clay-game labels, built as Studio templates]] |

## Tips (2026-10-26)

| Where | What |
|---|---|
| `SmithyCore` | `buildBlade(blade)`: Tool named `bladeName`, tip "grade · value coins", invisible 0.6-stud Handle as the tang, sword grip, attributes `BladeId`, `BlueprintId`, `MaterialId`, `Grade`, `BladeRefinement`, `BladeShape`, `BladeOffset` 0.3, tag `ForgedBlade`. Local `syncBlades(player, d)` (above `push`): one Tool per `d.blades` entry in Backpack/Character, extras destroyed; `push` runs it once `d.loaded`, `restoreTools` clears `BladeId` tools and runs it. No service that adds or removes blades needed changing. |
| `SwordRenderer` | Draws tags `ForgedSword` and `ForgedBlade` the same way (a blade has no hilt parts). `SwordSlash` still listens only to `ForgedSword`. |
| `Hotbar` | `keyOf`: `blade:<BladeId>`; `artOf`: kind `blade` for a `BladeId` tool; the slot title/metal line as a sword's. |
| `MailController` | `fitting(why)` returns `(count, list)` cheapest first; `choose(list, giver, send)`: one → send, more → `close()` the mail and `ItemPicker.open` (title the sender's name). `close` is declared above it. |
| `Guide` | `SpotlightGui.Arrow` placed each frame from the hole (above, rotated 0; or below, 180, when the hole is within the arrow's height of the top), bobbing 6 px. `buyStep(what, pad)`: "Press Buy" (no world target) when `PlayerGui.BuyButton` is enabled with that pad's `PadVisual.Top` as Adornee, else "Stand on the pad to buy …" at the pad. |
| `StarterGui.SpotlightGui.Arrow` | Frame, AnchorPoint (0.5, 1), Scale 0.06 + `UIAspectRatioConstraint` 1.1 + `UISizeConstraint` 44×40…66×60, ZIndex 2; the four chevron Frames from `GuideArrow` in Scale. |
| `StarterPlayerScripts.FreeMouse` | Render step `FreeMouse` at `Camera + 1`: Alt held and mouse `LockCenter` (or already freed) → `MouseBehavior` Default and `CameraRotationAction.Enabled` false (found under `PlayerScripts.PlayerModule`, 10 s wait; skipped if missing). |
| `Workspace.Plot.Workshop.Shell` door wall (plot z −18) | Opening x ±4.38 (posts ±4.38…5.42), lintel and plaster above ±4.6, top plate ±4.8 (sides from ±5.0), panels from ±5.2, threshold ±4.9, noren rod ±4.40, noren three panels across ±4.46. |

## Tutorial fixes (2026-10-27)

From [[Archive/Design/Progression and Economy Review — 2026-10-27#10. The tutorial]]; [[Sessions/2026-10-27#Tutorial fixes: the best blade, a Gem Shop step that ends on a buy]].

| Where | What |
|---|---|
| `Guide` | Requires `Shared/GemUpgrades`. `craft`'s hot-ingot step names `best`: the highest `basePrice` in `state.blueprints`, never a `big` one (the tantō until you know more), so saving up for a letter's blueprint says "Forge a Wakizashi". `firstBoost` (module level): the `GemUpgrades.list` entry with the cheapest `prices[1]`. `gemTour`: "todo" needs gems ≥ `firstBoost.prices[1]` (was > 0); "open" → "Buy a shop boost with your gems" on `GemShop.Body[firstBoost.id].Buy` (the whole `Body` if the card isn't built). |
| `GemController` | A successful buy sets `GemTour` to nil (ends the guide's step), before `showShop`. |
| `Shared/GemUpgrades` | Advertising `prices` 5 / 60 / 120 (was 25 / 60 / 120). |
| `ServerStorage.Legacy` | `Guide_beforeTutorialFixes`, `GemController_beforeTutorialFixes` (both disabled), `GemUpgrades_beforeTutorialFixes`. |
| `Development/economy_model.py` (vault) | The review's pacing model: the live constants copied in, three players, merges and cherry-picking; `python economy_model.py`. |

## Economy pass 2 (2026-10-27)

From [[Design/Economy Pass 2]]; [[Sessions/2026-10-27#Economy pass 2 built]]. Built in Edit, not played.

| Where | What |
|---|---|
| `Shared/Upgrades` | Every price from the plan (the guide's Mailbox 15, Wakizashi 60, Ore Slot 2 75 unchanged). Stage gates: each stage's pads list the previous goal in `after` (`KatanaBlueprint`, `LongswordBlueprint`, `Crafter`, `FalchionBlueprint`, `Stocker`, `Promoter`, `GladiusBlueprint`, `Cashier`, `Etcher`, `ZanbatoBlueprint`). New: `ZanbatoBlueprint` (Zanbatō, 200,000, after `GladiusBlueprint`, `BigSwordStand`, `Etcher`; `blueprint = "zanbato"`), `Anvil3` (160,000, after `Anvil2`, `ZanbatoBlueprint`), `Anvil4` (250,000, after `Anvil3`: pads can't wait for a crew hire). 45 upgrades. |
| `Shared/Deliveries` | `CAPACITY_PRICE` 2,900 / 20,000 / 53,000, `SPEED_PRICE` 3,800 / 21,000 / 60,000 / 120,000; new `CAPACITY_AFTER` { [2] Crafter, [3] Stocker } and `SPEED_AFTER` { [2] Crafter, [3] Promoter, [4] Cashier }: the upgrade that opens a level. |
| `Shared/Employees` | `ANVILS` { Anvil2, Anvil3, Anvil4 }; `TRAIN_PRICE` falchion 37,000, gladius 110,000 (the rest unchanged); crew coins Haru 370,000, Mei 640,000, Kenji 420,000, Rin 1,100,000 (gems unchanged). |
| `Shared/Blueprints` | Comment only: the Zanbatō is sold on the blueprint pad. |
| `EmployeeService` | One `crafterLoop(anvil)` per crafter anvil (`task.spawn`ed from `onPlot`), `working[player][anvil]` = `CrafterJob` { ingot, worker, claims }. `claim(station, job)` / `release(station, job)` record the job's stations and `releaseJob(job)` frees only those (`releaseAll` gone). Furnaces skip `CrafterBusy` ones (and a forgotten-furnace pick another crafter took); the Polishing Station waits while another crafter has it. `crafterStatus(anvil)`: `CrafterStatus` for Anvil 2, `CrafterStatus3` / `CrafterStatus4`; `setStatus` always takes the attribute. `STAND.Anvil3` / `Anvil4` copy Anvil 2's. `bestMade(d)`: the dearest non-big blueprint you've crafted; `hire()` trains the workshop on it and sets `making`. Actions: `hire` puts the new crafter on a free bought crafter anvil; `equip(crafterId, anvil)` moves them there (whoever was there rests); `unequip(crafterId)`; `train` refuses big blueprints. `inUseSign` on any `Anvil<n>`. |
| `SmithyCore` | `crafter.equipped`: { [anvil]: crafterId } (was one id). `decode` keeps each hired crafter at one anvil at most, drops unknown anvils; a one-crafter save is Taise at Anvil 2. An old `equipped` string isn't carried over (no live players). |
| `EmployeeController` | `anvilStatus(anvil)`, `anvilOf(cr, id)`, `boughtAnvils()`. Roster: ▲/▼ against the weakest working crafter; working cards are named `Working<anvil>` and show their anvil's status; title "Sword Crafters (n/anvils)". Stats: Station "Anvil n". Station page: a card per bought crafter anvil (who works there, or "Free"), `stationPick` outlined green; Equip sends `("equip", id, stationPick)`, Unequip `("unequip", id)`. The Swords picker leaves out big swords. The status loop follows all three anvils. |
| `StarterGui.CrewGui.Window.Station.List` | `Anvil2` card 228 × 300 (was 300 wide); new `Anvil3`, `Anvil4` (copies, `LayoutOrder` 1, 2, hidden until bought). |
| `DeliveryService`, `DeliveryController` | `upgrade` refuses a level whose `*_AFTER` upgrade isn't bought; the card's Buy reads "After <upgrade name>" greyed, coin hidden (requires `Shared/Upgrades`). |
| `ForgeService` | The pull no longer calls `collectWaiting` (the merge hook still does). `rollFor(player, plot)`: with nothing ever collected and no sword finished, pull 1 a Common, pull 2 an Uncommon (`tutorialPulls`, a session count), else `Materials.roll` with the plot's luck. |
| `Guide` | Requires `Shared/Materials`. `ore()` also returns the waiting stand's `Result` and the roller's `RollAt`; `craft` says "Pull again for a rarer metal" (the lever) over a Common on the first roll, once a session (`repullAt`). |
| `Hotbar`, `StarterGui.HotbarGui.BagPanel.Trash` | `Trash`: a 64 × 64 copy of the bag button (Key and Count removed), AnchorPoint (1, 1) at (1, 0, 0, −10), icon 44 × 44 `rbxassetid://112432692268721` (Free Icon Pack Trash Can, decal 75641554610978). `drop` checks the trash before the bag; `trashStack(key)` sends `Remotes.Trash` with the stack's `IngotId`s, or its `SwordId` / `BladeId`. |
| `ServerScriptService.InventoryService` (new), `ReplicatedStorage.Remotes.Trash` (new RemoteFunction) | `Trash(kind, ids)`: loaded player, `allowCall`, 1–500 ids (one for a sword or blade); `takeIngot` / `takeSword` / out of `d.blades`, then `push`. |
| `Workspace.Plot.Smithy.Anvil3`, `.Anvil4`, `Pads.Anvil3`, `.Anvil4`, `.ZanbatoBlueprint` | Anvil 2 copies (`Upgrade` = Anvil3 / Anvil4, `Turned` 90), on the workshop floor 0.6 below the hearth: Anvil 3 at plot (14.2, 28.0) right of the hearth, Anvil 4 at (−9.3, 28.0) between the Hilt Bench and the hearth; their pads (copies of `Pads.Anvil2`, `Workshop`) on the same spots; the Zanbatō's on the blueprint pads' spot (2.0, 16.2). |
| `ServerStorage.Tests.SaveSpec` | The crafter checks use the anvil map; the merge price derives from `OreStand6.price`; Ingot Rack 2's `after` may be a list. 97/97. |
| `Development/economy_model.py` (vault) | The picking player, `STAGES` (8 h), `fit()`, `run(pass2=True)` (gates, trained on hire, three crafters via `ROSTER`, the Zanbatō every `ZANBATO_EVERY` sales). |

## Customer rate (2026-10-27)

From [[Design/Economy Pass 2#9. Customer rate]]; [[Sessions/2026-10-27#Customer rate applied]]. Not played.

| Where | What |
|---|---|
| `Shared/GemUpgrades` | `INTERVALS` { 45, 75 }, { 36, 64 }, { 30, 52 }, { 22, 42 } (were { 12, 22 }, { 10, 18 }, { 8, 15 }, { 6, 12 }). |
| `ServerScriptService.ShopService` | `TUTORIAL_GAP` { 12, 22 }: the spawn loop uses it while the plot has no `Bought_OreStand2` and no `Merges`; otherwise `GemUpgrades.spawnInterval` × the Promoter's perk. No reputation factor. |
| `Shared/Reputation` | `walkInFactor` removed. |
| `StarterGui.GemGui.Templates.Upgrade.Info.Effect` | Placeholder text "Walk-ins  45–75 s → 36–64 s" (GemController fills each card). |
| `ServerStorage.Tests.SaveSpec` | Level 0's gap 45–75, past the top 22–42. 97/97. |
| `Development/economy_model.py` (vault) | `ADVERTISING` the new gaps; `run(customers=(scale, rep), trace=…)`: walk-ins against swords waiting, the cart past `SHELF`. |

## Robux passes (2026-10-27)

From [[Design/Monetization Plan]] (ids in §11, build notes in §12); [[Sessions/2026-10-27#Pass features built]]. Not played. Not built: the Shop page, Lucky Ore's odds panel, the developer products.

| Where | What |
|---|---|
| `Shared/Store` (new) | `PASSES` (key → pass id), `MORE_COINS` 1.5, `VIP_COINS` 1.1, `LUCKY_ORE` 0.5, `SWIFT_SPEED` 20, `STARTER_GEMS` 100, `STARTER_METAL` "Gold", `KEEPS` { Rare, Epic, Legendary, Common }; `owns(player, key)` reads the attribute `Pass_<key>`; `coinBoost(player)`, `luckBonus(player)`. |
| `ServerScriptService.StoreService` (new) | Sets `Pass_<key>` from `UserOwnsGamePassAsync` on join (retried after 2, 5, 10, 20, 40 s; unknown grants nothing) and from `PromptGamePassPurchaseFinished`. Swift Boots' WalkSpeed on every spawn; the Starter Pack's 100 gems and Gold ingot once (`starterGranted`), and again after Reset progress (`onRejoin`). **In Studio** ownership comes from its attributes `AutoRoller`, `MoreCoins`, `LuckyOre`, `VIP`, `SwiftBoots`, `StarterPack` (all off). |
| `ServerScriptService.SmithyCore` | `boosted(player, amount)`, `earnCoins(player, amount)` (pays a sale × `Store.coinBoost`, returns what it paid). `settings.autoRoll` / `.autoKeep` (saved; attributes `AutoRoll` / `AutoKeep`; the `Setting` remote takes `AutoRoll` with a boolean and `AutoKeep` with one of `Store.KEEPS`); `starterGranted` (saved). |
| `ShopService`, `DeliveryService` | Sales pay through `earnCoins`: a customer, the cart, an order, a commission (the mail log and reward card show what was paid). The Cashier's till takes `boosted` coins, so its sign shows them. DevTools' coins aren't boosted. |
| `ServerScriptService.ForgeService` | `rollFor` adds `Store.luckBonus` (Lucky Ore). The lever's pull is `r.pull`, shared by the prompt and the auto loop; `r.endedAt`. The auto loop (every 0.25 s) pulls when the owner has `AutoRoll` and `Pass_AutoRoller`, `AUTO_BEAT` 1.4 s after the last roll, the tutorial is done (`Bought_OreStand2` or a merge) and no stand holds an ingot of `AutoKeep`'s rarity or rarer. |
| `StarterGui.AutoRollGui` (new; `HudPart`, DisplayOrder 2) | `Button` (ImageButton with the Auto Open `Icon`; anchored bottom-centre at (0.925, 0.7), height 0.14, 44–72 px), `Lock` on its top-right, `Keep` chip (TextButton on its bottom edge, in the rarity's colour). |
| `StarterPlayerScripts.AutoRollController` (new) | Shows the button within 12 studs of your lever with no wall (`MyPlot.blocked`) once the tutorial is done. Locked: `PromptGamePassPurchase`; owned: `Setting("AutoRoll", …)`, the chip `Setting("AutoKeep", …)`; the icon turns while on; the lock pops off on purchase. |
| `StarterPlayerScripts.ChatTags` (new) | `TextChatService.OnIncomingMessage`: a gold `[VIP]` before a `Pass_VIP` owner's name. |
| `StarterPlayerScripts.MyPlot`, `.PromptFilter` | `MyPlot.blocked(part, from)`: PromptFilter's wall check, now shared. |
| `ServerStorage.Tests.SaveSpec` | The Auto Ore Roller's settings and `starterGranted` round-trip, odd ones fall back; the coin boost. 99/99. |

## Shop tension pass (2026-10-27)

[[Design/Shop Tension Pass]]; not played.

- **Faster Heating:** `Shared/Upgrades.HEAT_TIMES` {10, 6, 4, 3} (was 10, 8, 6, 4; {10, 7, 5, 4} since 2026-10-30).
- **VIP buyers:** `Shared/Customers.vip` sits outside `list`. `Customers.pick(rng, vipOk)` returns it on a `VIP_CHANCE` (0.05) roll once the owner is past the tutorial; `ShopService.runCustomer` passes Ore Slot 2 or a merge. The VIP offers ×1.75–2.25 (×2–3.5 since 2026-10-30), never raises, waits `waits` = 60 s, and never wears a friend's avatar.
  - `askOwner` takes `info.timeout` (defaults to `OFFER_TIMEOUT`, 45).
  - `ShopController` gives a VIP's card a gold rim and "VIP · " before the sword.
- **What customers say:** `Customers.remark(rng, name, metal, rarity, etched, polished, percent)` picks one line about the sword: a Rare+ or Legendary/Secret metal, the etch, the shine, an edge of 95%+, else "<name>, hmm. Let me see...". `runCustomer` says it in place of "Hmm, let me see..." and waits 2.5 s (was 2).
- **Sunshine:** `ServerScriptService.Weather` sets `ReplicatedStorage`'s `Weather` = "Sunny" and `WeatherEnds` (server time) for 5 minutes, every 15–25 minutes (until Fixes2: now a weather is always on, see [[#Fixes2 (2026-10-28)]]).
  - `ShopService`'s walk-in loop multiplies the gap by `SUNNY_GAP` (0.5) when sunny, but not in the tutorial.
  - `WeatherController` (StarterPlayerScripts) fades in `Lighting.SunshineGrade` (a ColorCorrectionEffect whose saved values are the look) and shows `StarterGui.WeatherGui.Sunny` ("Sunshine", "2× customers m:ss", top centre, Scale with an aspect-ratio and size constraint), only to players past the tutorial.
  - Studio only: `Remotes.DevSunshine` and the DevPanel's "Sunshine now" start one.
- **Model:** `economy_model.py` takes the new `HEAT` and `VIP`/`VIP_SHARE` in `share()`. Sunshine isn't modelled.

## Shop page (2026-10-27)

From [[Design/Monetization Plan#12. Built (2026-10-27, not played)]]; [[Sessions/2026-10-27#Shop page built]]. Not played.

| Where | What |
|---|---|
| `StarterGui.MenuGui.ShopWindow.Body.List` (new; replaces "Coming soon") | ScrollingFrame 594 × 340 (the window stays the 650 × 460 design); a card per pass named by its `Shared/Store` key: `StarterPack`, `AutoRoller`, `MoreCoins`, `LuckyOre`, `VIP`, `SwiftBoots`. Each is a clone of `GemGui.Templates.Upgrade` with an `Icon` (pack icon), `Info.Top.Title`, `Info.Effect` (both set in Studio), `Buy.Price.Robux` + `.Amount` and `Owned`. |
| `StarterGui.MenuGui.OddsWindow` (new; a copy of ShopWindow, `HidesHud`) | "Lucky Ore odds": `Body.Subtitle`, `Body.Table` (`Head`, then a row per rarity named by its id: `Name`, `Now`, `Arrow`, `With`), `Body.Buy`. 516 × 432. |
| `StarterGui.MenuGui.Buttons.Shop.Dot` (new) | A copy of the Mail button's amber dot. |
| `StarterPlayerScripts.MenuController` | The Shop section: prices from `MarketplaceService:GetProductInfoAsync(id, GamePass)` (only while on sale; "—" and grey otherwise), `Owned` from `Store.owns`, the Starter Pack first until owned (`LayoutOrder` 0, then 99). Lucky Ore's Buy fills and opens `OddsWindow` (`Materials.odds` at the plot's `Upgrades.luck` and + `Store.LUCKY_ORE`, three significant figures, gains green); its Buy prompts the pass. `PolicyService` restricted, or no answer: Lucky Ore's card is hidden. The dot: tutorial done (`MyPlot.tutorialDone`), Starter Pack not owned, Shop not opened this session. |
| `Shared/Materials` | `odds(luck)`: each rarity's chance in percent (adds to 100); `roll` draws from it, unchanged (200,000 rolls match). |
| `StarterPlayerScripts.MyPlot` | `tutorialDone(plot)` (the Guide's check), used by AutoRollController and MenuController. |

## UI pass — 2026-10-27

[[Sessions/2026-10-27#Message bars, floor arrows, red closes, paper letters]]. Supersedes, above: `GuideArrow` and `GuideHolderSpot` (gone); window children directly under `Window`.

| Where | What |
| --- | --- |
| `ReplicatedStorage.GuideLook` | `Arrow` (Beam template, flat floor arrows) and `Highlight` (the target's glow). |
| `Guide` | `drawTrail(points)`, `route(from, to)` (PathfindingService, trimmed `START` 2 / `STOP` 4), `glowOf(part)`, `showWay(target)` called each tick; workspace folder `GuideTrail`. |
| Windows (Mail, Crew, Delivery, MenuGui ×3, GemGui ×2, Collection) | `Shadow` (Z0, the picker's), `Fill` (Z1, background + gradient + stroke), `Content` (Z2, padding, layout, Header, Body…); Crew: no `Content`, its frames at ZIndex 2. |
| `MailGui…Letter` | `Envelope`, `Seal`, `Paper` (ImageLabel; `Text` inside), `Rule.Diamond`, `Signature` (MailController sets "— name"). `Templates.Letter`: `PaperBg`, `Seal`. |
| Message bars | `GuideGui.Goal`, `ShopHud.Notice`, `PickerGui.Toast`, `WorkshopOpenGui.Banner`, `MailGui.Popup`: each has a `Vignette` UIGradient. |

## Fixes (2026-10-28)

From `Untitled 1.md`; [[Sessions/2026-10-28#Fixes 2026-10-28]].

| Where | What |
|---|---|
| `Guide` | Arrows: one Beam per arrow (`ARROW` 5 studs, `SPACING` 6, counted back from the path's end); `GuideLook.Arrow` TextureMode Stretch. Spotlight hole on whole pixels. `buyStep` says "Buy …". "A customer is coming!" while the first sword is on display. An accepted letter with the mail open → "Close the mail" on `Window.Content.Header.Close`. "Sell it to afford the …". No Mailbox step: nothing after the first sale until the letter. |
| `ShopService` | `offerCommission(owner, now)`: without `now` it waits `LETTER_DELAY` (45 s since round 2); on join `now`. No `Bought_Mailbox` checks. |
| `Shared.Upgrades` | No Mailbox. `Workspace.Plot.Shop.Mailbox` has no `Upgrade` or `TycoonItem`; the pad is `ServerStorage.Legacy.Pads_Mailbox_beforeFixes1028`. |
| `MailController` | The Mail button always shows. |
| `ForgeService` | Slot `shown`: the timer counts from the full heat time while a tutorial ingot heats in 3 s; the tick is 0.1 s. |
| `WorldText.ForgeTimers`, `ForgeController` | `StudsOffsetWorldSpace` 0, 6.6, 0 (was `StudsOffset`); your own furnaces' boards are always `AlwaysOnTop`. |
| `AnvilController`, `AnvilHud` | `Panel` hidden; `Progress` (320 × 14, bottom middle at 1, -124) fills `strikeIndex / #recipe`, full when forged; hidden in the showcase. |
| `HiltBenchController`, `HiltSeatGui.Ghost` | The Cursor icon slides the hilt home every 1.8 s on the first sword (`state.completed == 0`, not gamepad) until you take hold. |
| `GuideGui.Goal`, `WorkshopOpenGui.Banner`, `ShopHud.Notice`, `PickerGui.Toast`, `MailGui.Popup` | `AutomaticSize` X, padding 50–80 px, vignette 0 → 0.1 … 0.9 → 1. The popup: AnchorPoint 1, 0.5 at 1, -8, 0.5, 0. |

### Round 2 (2026-10-28)

[[Sessions/2026-10-28#Fixes 2026-10-28, round 2]].

| Where | What |
|---|---|
| `Shared.Commissions` | First letter `IronTanto` (round 3; `IronBlade` with any blade in round 2, `IronWakizashi` before): `blueprintId` "tanto", `materialId` "Iron", `minPercent` 0 (any). `mismatch` skips a nil blueprint and a 0 floor; `title` gives "Iron Tantō" (or "Iron blade" for a letter with no shape). |
| `ForgeService` | `wantedMetal(d)`: the open (offered or active) story letter with a `materialId`. `rollFor` returns it one pull in `WANT_CHANCE` (1/3). `reveal` shows `OreLabel.Wants` ("<sender> wants this!") on a matching ore. |
| `WorldText.OreLabel` | `Wants` TextLabel under the rarity (hidden by default); the billboard's ClipsDescendants off. |
| `Guide` | `route` is a straight line (no PathfindingService). For a letter's metal: "Pull again for <metal>" over a lid of another metal, "Pull the lever for <metal>", "Forge an <metal> <best blade>"; only blades of that metal count for "Fit a hilt". |
| `MailController` | A story letter's title shows "· N%+" only when `minPercent` > 0. |
| `MailGui.Popup`, `SpotlightGui` | Popup 52 px, portrait 38, text 18 / 14, padding 36. Spotlight `ScreenInsets` None. |
| `ServerStorage.Tests.SaveSpec` | Commission checks for the Iron blade letter (99 checks). |
| `Guide` (round 3) | `pickerTarget()`: with a picker up, the accepted letter's `Shape<blueprintId>` card in `PickerGui` is the spotlight target. [[Sessions/2026-10-28#Fixes 2026-10-28, round 3]] |
| `ForgeService` (round 4) | `wantedMetal` / `WANT_CHANCE` moved above `reveal` (it was nil there: every pull errored). `PickerGui.Templates.CompactCard` text 18 / 13 / 16, `CompactWindow.Body.Empty.EmptyTitle` 22. [[Sessions/2026-10-28#Fixes 2026-10-28, round 4]] |
| `CrewGui`, `MailGui`, `DeliveryGui`, `GemGui`, `HotbarGui` (phone text pass) | Text sizes raised so each reads ≥ 14 px at the window's phone scale (`UiFx.fit` at 844 × 390). Backups `ServerStorage.Legacy.<Gui>_beforePhoneText`. [[Sessions/2026-10-28#Phone text pass]] |

## On-screen action button (2026-10-28)

[[Sessions/2026-10-28#On-screen action button]].

| Where | What |
|---|---|
| `StarterGui.ActionGui` | `Action` card (Row: Key, Words.ActionText / ObjectText; Hold.Fill), `Prompt` ObjectValue. Built in Studio. |
| `StarterPlayerScripts.ActionButton` (new) | `PromptShown` / `PromptHidden` for prompts with `ScreenButton`; taps → `InputHoldBegin` / `InputHoldEnd`; `PromptButtonHoldBegan` fills Hold over `HoldDuration`. |
| Plot template prompts | HeatPrompt, ForgePrompt, PolishPrompt, RollPrompt, EtchPrompt, HiltPrompt, ShapePrompt, DeliveryPrompt: Style Custom + `ScreenButton`. |
| `ShopService` | The till's `CollectPrompt`: Style Custom + `ScreenButton`, ObjectText "Cashier" (the ore's went back to Roblox's prompt the same day). |
| `Guide` | `actionFor(target)`: the card is the spotlight target when its prompt is in the target's station (`stationOf`). |
| `Guide` (playtest fixes) | Clears old `GuideTrail` / `GuideArrow` on start; `MAX_ARROWS` 4, `SPACING` 9; `pickerTarget()` for any picker in a guided step (letter's card, else the first); `SpotlightGui.Ghost` taps the spotlit button; no `SpotlightGui.Arrow`. [[Sessions/2026-10-28#Playtest fixes: arrows, forge, cards, ghost clicks]] |
| `ForgeController` | HeatPrompt off while full with none of yours ready (and while Locked). |
| `ActionGui.Action.Hold` | One frame + `Progress` UIGradient (Offset.X -0.5 → 0.5), no Fill child. |
| `MailGui.Popup` | `Words` (Title = sender's name, Hint = "Sent you a letter · Tap to read"); `MailController` sets `Words.Title`. |
| `GuideLook.Arrow`, `ActionGui.Action`, ghosts | TextureLength 1 (Stretch repeats the texture that many times); the card at `{0.5,0},{0.938,-69}`; `SpotlightGui.Ghost` / `HiltSeatGui.Ghost` 0.09 of screen height (RelativeYY), 26–52 px. [[Sessions/2026-10-28#Single arrows, lower card, ore prompt, ghost size]] |
| `ActionGui.Action.Row.Key.Tap` | The Cursor icon in the key box on touch (`ActionButton` blanks the key's text then). |
| `Guide` (ghost, ore step) | `ghostOn`: the ghost shows only on picker cards. `actionFor` returns nil for a target inside an ore `Stand<n>`. |
| `StarterGui.ActionGui.Enabled` (switch) | Off: Roblox's prompts (ScreenButton prompts Style Default in Studio), `ActionButton` returns at once. On: `ActionButton` sets them Custom client-side and draws the card. Tap icon whenever `TouchEnabled` (not gamepad). |
| `Guide` (spotlight motion) | `FADE_IN` 0.25, `FADE_OUT` 0.2, `IRIS` 3, `GLIDE` 0.18: `shown` 0–1 drives the shade frames' transparency (from `SHADE`, their Studio value); `rectAt` / `rectSize` ease to the target. `HiltSeatGui.Chevron` removed. |
| Six more (2026-10-28) | `RewardCard` no assembled-sword card; `HiltBenchController` no inventory toast; `CompactCard` 169 × 195 and `UiFx.fit(COMPACT.Fit, 600, 320)`; `MailController.sent` closes the mail after a Send; `Hud` `waiting` coins fly when HudGui is back; `Letter.Preview`; `Commissions` `gems` (IronTanto 5) paid in `ShopService`; `GemController` tour needs the cheapest boost's gems; `GemUpgrades` stats as multipliers (`rate`). [[Sessions/2026-10-28#Six more: popups, phone cards, Send coins, previews, gems, stats]] |

## Cascading ore roll (2026-10-28)

[[Sessions/2026-10-28#Cascading ore roll]].

| Where | What |
|---|---|
| `Shared.Materials` | `CASCADE` (lockAt 1.1, gap 0.06, step 0.55, hold 0.35, drop 0.3), `climbs(m)` (Common 0 … Secret 5), `rollLength(results)`. `roll` unchanged. |
| `ForgeService` | The still box's pull sets `RollTime` = `Materials.rollLength(results)` before `RollAt` and waits that long (`BOX_TIME` only seeds it). Ore `CollectPrompt` OneGlobally; furnace board 96 wide. |
| `OreBoxShow` | Rewritten: Common flicker, lock-in, one climb per step with pop, hop, flash, ding (`Cues.RollClimb` cloned onto the ingot). Backup `ServerStorage.Legacy.OreBoxShow_beforeCascade`. |
| `SoundService.Effects.Cues.RollClimb` | New: the furnace ding at 0.3, roll-off 8–45 studs; pitch set per climb. |
| Prompts, pill, ghost | 12 station prompts OneGlobally; `RollPrompt` hold 1 s; `WorldText.ForgeSlot` pill (34 tall, round ends, text 20), `ForgeTimers` 96 × 34; Guide ghost stays put and presses. |
| `Shared.Upgrades` (Ore Slots) | OreStand4/5/6 `after` the previous slot only (no Katana / Falchion / Cashier). [[Sessions/2026-10-28#Ore Slots ungated]] |
| `SmithyCore` `rolled`, `ForgeService.reveal`, `WorldText.OreLabel.New` | Metals ever rolled (saved); NEW (its own amber line above the name) only on a metal's first roll. [[Sessions/2026-10-28#NEW on the first roll, on its own line]] |
| `AutoRollGui.Button`, `AutoRollController`, `RewardCard` | Auto-Roll is a centred pill over the hotbar (Icon 28 px + Label "Auto-Roll"; Lock under Icon; Keep under Label). No "New metal" toast. [[Sessions/2026-10-28#No New metal toast; the Auto-Roll pill]] |
| Auto-Roll stops (2026-10-28) | `Store.KEEPS` Uncommon/Rare/Epic/Legendary/None; `SmithyCore.settings.autoQuest` (saved, default on) → `AutoQuest` attribute; `ForgeService.needed`/`keeping(r, owner)`; `AutoRollGui.Button` top centre with `Label.Chips.Keep` / `Quest`; `AutoRollController` cycles / toggles them. [[Sessions/2026-10-28#Auto-Roll stop settings, at the top]] |
| `StoreService` (already own) | A closed pass prompt without a purchase checks `UserOwnsGamePassAsync` and grants when owned. |
| `AutoRollGui.Bar` (Button: Icon/Lock, Label, Switch; Config), `AutoRollController` | The Auto-Roll bar with an On/Off switch; its settings are the `Config.Drop` dropdown since 2026-10-31 (the old `AutoRollConfig` window is deleted). [[Sessions/2026-10-28#Auto-Roll bar and its window]] |
| `ServerStorage.Hook_AutoPull`, `ForgeService.autoPull`, `LeverAnimator.autoSwing` | An auto roll swings the lever over the 1 s hold, then pulls. `AutoRollGui...Switch` is a knob toggle. [[Sessions/2026-10-28#Pill toggle; Auto-Roll pulls the lever]] |
| `StoreService` (Studio) | Asks Roblox for passes in Studio too; attributes add a pass; `StudioLocked` shows every pass as not owned. Auto-Roll bar 222 + gear, no borders; locked keeps the toggle off. |
| Menu style (2026-10-28) | Every menu window: 16 px corners on the window and its `Fill`/`Pattern`/`Tint`, 5 px outline 16,20,16; cards 12 / 4, buttons 10 / 4, chips 8. Shop, Settings, Odds, Gem Shop, Daily Reward, Auto-Roll: `Header` 0 tall, `Title` on the top border, `Close` on the corner, `UiFx.fit(…, 650, 570)`, Position (0.5, 0, 0.5, 29). Scripts keep the template's edge colour/thickness (highlight +1). [[Sessions/2026-10-28#Menus match the Buy button: rounded, thick black edges]] |
| `MenuGui.ShopWindow` (2026-10-28) | `Content.Body.List`: `StarterPack` (featured gold card, LayoutOrder 0 until owned, then 99) and `Grid` (LayoutOrder 1, two-wide `UIGridLayout` of the other pass cards). `MenuController` finds cards with `FindFirstChild(key, true)`. Backup `ServerStorage.Legacy.ShopWindow_beforeGrid`. [[Sessions/2026-10-28#Shop as a featured card and a grid]] |
| Shop sections (2026-10-28) | `ShopWindow…List`: `StarterPack` (hidden once owned), `PassesHeader`, `Grid`, `CurrencyHeader`, `Currency` (cards `Gems80/200/500`, `Coins5000/20000` from `Store.PRODUCTS`, Buy nudges: no ProcessReceipt). Cards: own gradient, `Rays` (114867032143023), `Glow`, 108 px `Icon`. `UiFx.fit(scale, w, h, min?, max?)`; Shop max 1.5. `AutoRollGui.Bar` y 8, or 62 while `GuideGui.Goal` shows. [[Sessions/2026-10-28#Shop sections, bright cards, bigger on desktop; Auto-Roll up top]] |
| Developer products (2026-10-28) | `StoreService` `ProcessReceipt` (Store.PRODUCTS, GEM_PACKS, COIN_PACKS: fixed 5,000 / 20,000) → grant, `SmithyCore.addReceipt`, `saveNow`; SmithData `receipts` (≤ 100). Menu Buy buttons: `UIGradient` + `Glow`. [[Sessions/2026-10-28#Gem and coin packs sell: ProcessReceipt; Buy buttons shaded]] |
| Pack offers (2026-10-28) | `Store.packFor`; `TycoonService` BuyUpgrade returns `false, pack, amount` when short; `StarterPlayerScripts.PackOffer` (`offer(currency, key, amount)`; since 2026-10-31 Roblox's own `PromptProductPurchase`, no popup); called from `TycoonController.buy` and `GemController` (unaffordable price). [[Sessions/2026-10-28#Short of coins or gems: offer the pack that covers it]] |
| Build-in (2026-10-28) | `TycoonController` `build(item)`: an item unlocked while you watch flies its anchored visible parts in from above (`BUILD_SPREAD` 0.8, `BUILD_FLY` 0.5, Quint Out, `BulkMoveTo`), lowest first; ends on the server's CFrames. [[Sessions/2026-10-28#Bought upgrades build themselves]] |
| Shop edges (2026-10-28) | Shop cards, Buy buttons, window `Fill`: an `Edge` 9-slice ImageLabel (`rbxassetid://123259227611606`) instead of a border `UIStroke`; cards' `Rays`/`Glow` in `ArtClip`; `ShopWindow` 650 × 456 fixed. [[Sessions/2026-10-28#Hand-drawn 9-slice edges with a shadow (Shop)]] |
| Menu edges (2026-10-28) | Every menu frame's black outline is an `EdgeArt` 9-slice ImageLabel, centred (AnchorPoint 0.5); its border `UIStroke` stays at Transparency 1 and shows only for highlights (ItemPicker, GemController, MailController, DeliveryController, EmployeeController). Plain strokes: Delivery steps, Capacity, Speed, orders; Crew's green buttons. [[Sessions/2026-10-28#The hand-drawn edge on every menu]] |
| Anvil UI cleanup (2026-10-28) | `AnvilHud` keeps `Bottom` (Leave/Finish), `Progress`, `Hint`, `Result`; Panel, Tools, Hammers, ModeButton and `StarterGui.GrindMap` removed with their code. Backup `ServerStorage.Legacy.AnvilDeadUI_2026-10-28`. [[Sessions/2026-10-28#Dead anvil UI removed]] |

## Fixes2 (2026-10-28)

**Fixes3 changes (same day):** `WorldText.PadLabel` has `Title` and `Price` (TycoonService fills them; "$" prices); `WorldText.BuyButton` carries a `Label` (Title, Price) over the button, filled by TycoonController from the pad's label, which it hides while you stand there. `WorldText.OreLabel` fixed text sizes, FixedSize strokes. Guide: `drawTrail(points, glide)` runs every RenderStepped on `routePoints` (SPEED 4, fades at both ends). ShopService `FIRST_LETTER_DELAY` 3. WeatherGui: one `Icon` (ImageButton, bottom-left, image ids as attributes) with a tap `Tip`; WeatherController's roof test uses `InsideZone`s; `WeatherFx.Rain.Drops` uses the rain streak texture.

- **Tutorial's end:** the plot attribute `TutorialDone` (true once the first letter is sent): TycoonService's `onPrepare` sets it from the save, ShopService when the letter is sent, DevTools' Skip tutorial. Read by ShopService (`TUTORIAL_GAP`, VIPs, Snow), ForgeService (Rain, Auto Ore Roller), `MyPlot.tutorialDone` (Guide, MenuController, WeatherController) and GemController. Replaces `Bought_OreStand2` or `Merges` > 0.
- `Guide`: `tutorialDone` also counts the first letter `done` in your state; no re-pull step or Ore Slot 2 step; `mailButton` returns `Content.Letter` while its button shows; `closedAfterAccept`; the Gem Shop step spotlights the row. `GuideLook.Arrow.TextureSpeed` 0.
- `BladeCore.EARLY_FINISH_SHARE` (0.75) and `canFinish(blade, state)`; `ForgeCheck.evaluate` accepts from `canFinish`, grade `forPercent(100 × strikes/recipe)`, multiplier `MAX_MULTIPLIER × strikes/recipe`. `BladeData.blank` is the ingot bar (re-running the tanto-forge exporter would undo it). `AnvilController`: `finishForging` (mode `"finishing"`), Finish enabled at `ready` + `canFinish`; `AnvilHud.Bottom.Finish` has no UIGradient/Glow.
- `ServerScriptService.Weather`: `WEATHERS` (weight + effect attribute), `SPELL` 300 s, `start(w)` for a later bought weather; ReplicatedStorage attributes `Weather`, `WeatherEnds`, `WeatherCustomers`, `WeatherMail`, `WeatherLuck`, `WeatherVip`. Read by ShopService (walk-in gap, mail clock, `Customers.pick(rng, vipChance)`) and `ForgeService.rollFor` (luck). `Remotes.DevWeather` (was DevSunshine). `WeatherController` clones `ReplicatedStorage.WeatherFx` (Rain, Snow, Rainbow) to the camera (rain/snow off under a roof) and fades `Lighting.RainGrade`/`SnowGrade`/`RainbowGrade`/`SunshineGrade`; `WeatherGui` chips Sunny/Snow/Rain/Rainbow (`Bonus` attribute).
- `ShopService.makeNpc` clones `WorldText.VIPHighlight` onto VIP customers.
- `WorldText.BuyButton` 132×48 px, `StudsOffset` y 1.5; `WorldText.OreLabel` 110×42 px, `MaxDistance` 16; `WorldText.PadLabel` stroke 2, (20,84,24). MailGui Letter's `Want` row at y −54 above `Buttons`; MailGui.Popup 64 px tall.
- Shop-front `Noren`/`NorenRod` gone from `Plot.Shop.Starter/Upgraded.Shell` (in `ServerStorage.Legacy.Fixes2_1028`); `Builders.build_shops` leaves the entrance bay open.

## Upgrade order (2026-10-28)

[[Archive/Design/Upgrade Order Review — 2026-10-28]], [[Sessions/2026-10-28#Upgrade order built]]. Built in Edit, not played.

- `ReplicatedStorage.Shared.Upgrades`: the spine Katana → Sword Crafter → Longsword → Anvil 3 (Haru) → Stocker → Falchion → Anvil 4 (Mei) → Shop Promoter → Gladius → Cashier → Sword Etcher → Zanbatō; two stages open (a stage's pads `after` the goal before the last one, Anvil 3 / Anvil 4 standing for the crafters); new prices (Katana 1,300 … Zanbatō 300,000; Ore Slots 3–6 280 / 2,000 / 9,800 / 20,000). The header says how it's gated.
- `ReplicatedStorage.Shared.Deliveries`: `CAPACITY_PRICE` 1,500 / 25,000 / 64,000, `SPEED_PRICE` 2,400 / 40,000 / 55,000 / 76,000; `CAPACITY_AFTER` { LongswordBlueprint, FalchionBlueprint }, `SPEED_AFTER` { Anvil3, Anvil4, Promoter }.
- `ReplicatedStorage.Shared.Employees`: crafter `after` (an upgrade id or a crafter id: Haru `Anvil3`, Mei `Anvil4`, Kenji `mei`, Rin `kenji`) and `Employees.hireOpen(c, plot, hired)`; crew coins 23,000 / 70,000 / 460,000 / 710,000; `TRAIN_PRICE` falchion 4,000, gladius 6,000 (only for a shape the workshop lacks).
- `ServerScriptService.EmployeeService`: in `PlotService.onPlot`, `teach(switch)` trains `crafter.trained` on every non-big blueprint you know; each blueprint pad's `Bought_<id>` change runs `teach(true)`, which sets `crafter.making` to the dearest known sword; `hire()` keeps `making = making or bestMade(d)` and then teaches; the `hire` remote action also needs `Employees.hireOpen`.
- `StarterPlayer.StarterPlayerScripts.EmployeeController`: requires `Shared.Upgrades`; a roster card whose `after` isn't met shows the veil and "<upgrade or crafter> Required" in `Needs`.
- `Development/economy_model.py` (vault): the built tree as `PADS`, `GATE` for cart levels and crew, merges, crew teaching, `rate()` for payback, `fit()` (cheapest-first stage nudging), `walls()`.

## More features (2026-10-28)

[[Sessions/2026-10-28#More features]]. Built in Edit, not played. Supersedes, above: More Clients as customers at once (ShopService, `Shared/GemUpgrades`), `Orders.GAP` / `Orders.slots` and the mail opening full (`Shared/Orders`), `Customers.VIP_CHANCE` and the Rainbow's flat 15%.

- `ReplicatedStorage.Shared.GemUpgrades`: `list` Advertising, Vip, Clients, Mail (5 prices each); `spawnInterval(level)`, `mailSlots(level)` (2–7), `mailGap(level)` (180–75 s), `vipChance(level)` (0.05–0.15); `maxCustomers` removed.
- `ReplicatedStorage.Shared.Orders`: `Order.materialId`; `make(rng, id, ctx, kind)` with `ctx.metals` (collected metal ids): kind nil is a mail order (shape, metal by `pickMetal`, etched at `ETCH_CHANCE` 0.3 with `ctx.etch`); "plain" / "twist" (Deliveries) unchanged. `title` / `prose` / `mismatch` / `decode` read `materialId`.
- `ServerScriptService.ShopService`: `WALK_INS` 2; `refillOrders` uses `GemUpgrades.mailSlots(Clients)` and `mailGap(Mail)`, never opens full, passes `metals` from `d.discovered`; `runCustomer`'s VIP chance is `vipChance(Vip) × WeatherVip`. `Weather`: Rainbow `WeatherVip` 3 (a multiplier). `ForgeService.needed` matches an order's `materialId`.
- `StarterGui.GemGui.Templates.Upgrade.Info.Ticks` (`Tick1–5`, `On` / `Off` colour attributes) replaces `Top.Level`; `GemController` lights them. `StarterGui.WeatherGui.Icon.Tip`: no plate; `Title` (name, time) and `Detail` (bonus) rich text; `<Weather>` and `<Weather>Color` attributes; `WeatherController` fills them and plays `SoundService.Effects.Rain` while it rains (35% under a roof).
- `TycoonController`: other plots' `PadVisual` parts LocalTransparencyModifier 1 and CanCollide off on this screen, their labels off. `AutoRollController`: `show(here)` slides `AutoRollGui.Bar` in from above / out. `OreBoxShow`: `Cues.RollSpin` from the first stand until the last lock-in, `Cues.RollDone` from the last stand at the end (also from `destroy` if the real ore beat it by a frame).
- `SoundService.Effects.Rain` (9112852671), `Effects.Cues.RollSpin` (9125682521), `RollDone` (1841324418). `ReplicatedStorage.WeatherFx.Rain.Drops`: FacingCameraWorldUp, Squash 2. `WorldText.PadLabel` / `BuyButton.Label` strokes 3. `Shared.Upgrades`: "Sword Rack", "Sword Rack 2".
- `StarterGui.HotbarGui.Templates.Slot` / `Bar.Bag` (2026-10-28, [[Sessions/2026-10-28#Hotbar like the pickers, plainer shelves]]): the picker card's `UIGradient` and `EdgeArt`, no `Halftone`; `Edge` (4 px, amber) shows only on the stack in hand / the open bag. `Hotbar`: `ART_LIGHT` (the card's light), white rim, no `RARITY`; `EDGE` 4. Supersedes the HotbarGui row's rarity colours. `Plot.Shop.Displays.WallRack1–4.Shelf` and `build_workshop`: no Corner, Stud, Crest or Gable.
- `ServerStorage.Builders.build_outside_layouts` (2026-10-28, [[Sessions/2026-10-28#Smithy Yard Planner (drag the stations on a page)]]): look-only outside-smithy copies of `Workspace.Plot` in Workspace (no scripts, prompts, tags or attributes); `M.build()` (or calling the module) makes `Z_B_Bands`, `Z_C_ForgeRing`, `Z_D_Court`; `M.saved(doc, name, x)` builds a layout saved in the Smithy Yard Planner page (artifact ENjB8BW5rwjrQnQ5oaP9iu, collection `layouts`). Station fronts (`NOW`): furnaces and ingot racks −x, etching and polishing +x, anvils, hilt bench, ore roller −z, sword racks +z.
- **Furnace 3, Your anvil, anvil props (2026-10-28, [[Sessions/2026-10-28#Anvil stations, Your anvil, Furnace 3, the Line layout]]):** `Plot.Smithy.Forge3` (TycoonItem `Upgrade` Furnace3; pad `Plot.Pads.Furnace3`), `Shared.Upgrades` Furnace3 (5,800, after Anvil3), `Shared.Employees` Haru `after` Furnace3. `ReplicatedStorage.WorldText.YourAnvil` + `AnvilController` (`yourAnvil`, over Anvil 1's Face, hidden while forging). `ServerStorage.Builders.build_anvil_props(smithy)`: a `Props` model (QuenchTub, HammerStump) in each `Anvil<n>`; not on the live plot.

### Hilt Bench folded into the anvil (2026-10-28)

[[Sessions/2026-10-28#Hilt Bench folded into the anvil]]. Backups: `ServerStorage.Legacy.HiltBench_folded_2026-10-28` (HiltBenchController, SmithService, AnvilController, Guide, HiltBenchHud, HiltSeatGui.Close, AttachHilt, HiltPrompt). Supersedes the `AttachHilt` and `HiltBenchController` rows above.

| Where | What |
| --- | --- |
| `SmithService` | `complete(player, d, blade)`: `Hilts.best(d.completed)`, `seatBonus(SEAT_TAPS)`, `giveSword`, funnel 4 and 5; returns `{ blade, hiltId, first }`. Used by `FinishBlade` and `FinishShaped`. `MAX_BLADES` and `AttachHilt` gone. |
| `StarterPlayerScripts.HiltSeat` (new ModuleScript) | `play(blade, hiltId, surface, turn, clang, teach)`: the old bench seat (drag, `SeatHiltSlide` Space / A / R2, ghost) laid on any surface; returns when seated or the character dies. No leave binding. |
| `AnvilController` | After `FinishBlade` succeeds: `seating = true`, AnvilHud and AnvilPoints off, `HiltSeat.play(res.blade, res.hiltId, face, mount.CFrame.Rotation, clang, res.first)`, then `leave()`. RenderStepped and InputBegan skip while `seating`. |
| `Guide` | No "Fit a hilt" step; `pickerTarget` has no `Blade<id>` cards. |
| `Hotbar` | `HIDDEN_BY` without `HiltBenchHud`. |
| Unused now | `d.blades` (save field), blade Tools (`BladeId`), Hotbar blade slots, `InventoryService` blade trash, `Workspace.Plot.Smithy.HiltBench` (decor, no prompt). |
- **The outside smithy (2026-10-28, [[Sessions/2026-10-28#The outside smithy, built]]):** the plot template's `Workshop` is only `Shell` (the shop's back wall, 13 studs, the door) — no floor, InsideZone, roof or HidesRoof tag; `Plot.Grounds` (Paving, PavingSide x2, PavingStrip as a TycoonItem `UntilUpgrade` UpgradedStore, Lawn x4); `Smithy` stations in the Line layout with `Turned` updated, `WorkshopFittings` only the Hearth (Your Anvil's stone). `TycoonService.pushWorkshopBack` moves only what's in `STRIP` (|x| <= 25, z -19.5 .. -5.5): Workshop.Shell, Smithy models and Workshop pads there, players there. `EmployeeService.spot` honours `SpotCentre`. Builder `ServerStorage.Builders.build_outside_smithy` (one-shot; backup `Legacy.Plot_beforeOutsideSmithy`). Supersedes the Workshop rows above (the push of the workshop building, the workshop's InsideZone for RoofHider and the weather).

### Anvils on wooden blocks (2026-10-28)

[[Sessions/2026-10-28#Smaller anvils on wooden blocks]]

| Where | What |
| --- | --- |
| `Workspace.Plot.Smithy.Anvil` / `Anvil2-4` `.Model3D` | Scaled 0.7 (pivot was the face's top centre; `WorldPivot` reset to the new bounding box). New `WoodBase` (MeshPart from `StationBevels.B500_700_500`, 2.4 x 0.988 x 2.4). `Face`, `BladeMount`, `Props` unchanged. |

### Hilt Bench removed, carried blades gone (2026-10-28)

[[Sessions/2026-10-28#Hilt Bench removed, carried blades gone]]. Backups: `ServerStorage.Legacy.CarriedBlades_removed_2026-10-28` (SmithyCore, InventoryService, DevTools, Hotbar, SwordRenderer, SaveSpec); the bench model in `HiltBench_folded_2026-10-28`. Supersedes the "Unused now" row above.

| Where | What |
| --- | --- |
| `SmithyCore` | No `blades` field (type, `newData`, `encode`, `decode`, `publicState`); `syncBlades`, `buildBlade` gone; `push` no longer syncs Tools; the respawn rebuild clears only `IngotId` / `SwordId` Tools. `encodeBlade` / `decodeBlade` stay (a sword's blade). |
| `InventoryService` | `Trash` kinds: `ingot`, `sword`. |
| `Hotbar` | No `blade:` stack keys or blade art; trash sends ingots and swords. |
| `SwordRenderer` | Tag `ForgedSword` only. |
| `Tests.SaveSpec` | "no carried blades saved or sent"; the unknown-blueprint case is a sword. |

### Wall racks raised, cradles build in, sword pop (2026-10-29)

[[Sessions/2026-10-29#Wall racks raised, cradles build in, sword pop]]. Backup `ServerStorage.Legacy.WallRacks_beforeRaise`.

| Where | What |
| --- | --- |
| `Plot.Shop.Displays.WallRack1-4` | `Shelf` and `Slot1-3` +2.75 y; `HolderPrompt.MaxActivationDistance` 8. `Origin`, `InspectPoint` unchanged. |
| Every `Holds` cradle (wall racks, display tables) | Transparency 1 in Studio. |
| `ShopService` | `seat` sets the slot's cradles' Transparency 0 under a sword, 1 when empty; `place` / `clearSlot` set / clear the slot's `SwordId` attribute; TakeBackPrompt reach 8. |
| `TycoonController` | `build(item, only?, spread?, done?)`. Sword holders: `DisplaySlot` `Occupied` → true (a change, not a stream-in) defers `placed`: the slot's cradles build in (`CRADLE_SPREAD` 0.15), the sword model (`SwordId` match in the plot's Shop, up to `SWORD_WAIT` 2 s) is hidden until they land, then `pop` (`POP_SCALE` 1.2, `POP_TIME` 0.3: `ScaleTo` then `PivotTo` to keep the bounding-box middle) once `BladeDrawn`. |
| `SwordRenderer` | Sets `BladeDrawn` (local) at the end of `render`. |

### Back door, delivery wall, bay fence, table bases (2026-10-29)

[[Sessions/2026-10-29#Back door moved, delivery doorway walled up, bay fence gone, table bases hidden]]. Backup `ServerStorage.Legacy.Doors_beforeMove_2026-10-29`.

| Where | What |
| --- | --- |
| `Plot.Workshop.Shell` | Doorway between posts at plot x -13 and -3.2 (centre -8.1); InteriorLiners -22.845..-12.48, header -12.48..-3.72, -3.725..22.845. |
| `Plot.Shop.Starter.Shell`, `Upgraded.Shell` | Right wall at z -28: Plaster and Wainscot (mirrored from the left wall); one InteriorLiner at x 22.9 the length of the left one. `Shop.DeliveryDoor` gone. |
| `DeliveryService` | `openDoor` and `DOOR_TIME` gone; `Bought_Delivery` just runs `update`. |
| `Plot.DeliveryBay` | No low `Post` / `Rail` parts; gate `Post`s, `Lintel`, `TieBeam` stay. |
| `*_stand_base` (display tables) | Transparency 1, attribute `BaseOf` = slot; `ShopService.seat` toggles them; `TycoonController.placed` builds them in. |

### Station frames, frame swords, anvil hearths (2026-10-29)

[[Sessions/2026-10-29#Standing frames for the station signs (trial)]], [[Sessions/2026-10-29#More swords on the station frames; hearths for Anvils 2-4]]. Backups `ServerStorage.Legacy.Stations_beforeStandingFrame`, `StationSwords_beforeMore`, `Anvils_beforeHearths`.

| Where | What |
| --- | --- |
| `Smithy.PolishStation` / `EtchingTable` / `EtchingTable2` `.StandingFrame` | `Post` x2, `Beam`, `Backboard` (face on the old wall line, found from the sign arm's direction), `Cap`. Plain Parts, Wood + PaintFurniture. |
| PropSwords (those stations) | New `PropSword_Polished_<bp>` (Shimmer) x3; `PropSword_<Etch>_<bp>` x3 per etching table; extra `Peg` / `RackPeg`; `RackArm`s 1.95 longer downward. |
| `Smithy.Anvil2-4` | No `AnvilStone`; +0.56 y; `Hearth` (cloned from `WorkshopFittings.Hearth`, 10.5 x 0.6 x 8). |

### List.md (2026-10-29)

- `SoundService.Effects.Cues`: RollSpin / RollDone ids replaced; `Swings` folder (Swing1-3) played by `SwordSlash`.
- `SmithyCore`: `settings.weather` (attribute `Weather`, Setting switch), lifetime `coinsEarned` / `gemsEarned` / `played` (saved; `SmithyCore.totals(player)`); `addCoins`/`addGems` count positive amounts.
- `MenuController`: Settings rows Music, Sound, Weather. `WeatherController`: the Weather switch off draws no grade, effect or rain sound.
- `AutoRollController` steps `Store.KEEPS` (its window is now `AutoRollGui.Bar.Config.Drop`, 2026-10-31).
- `NpcWalk.animate`: R15 look-around every 7-16 s when standing.
- `AnvilController.finish` keeps the forged blade until `HiltSeat.play(blade, hiltId, surface, turn, clang, teach, at?, placed?)` has drawn its blade there; the seat camera glides (`GLIDE` 0.5 s).
- `Shared/Upgrades`: `F2Heat1-3`, `F3Heat1-3`, `Upgrades.heatTime(plot, forgeName)`; `WallRack5` (Back Wall Rack), `DisplayTable5-6`; `UpgradedStore` after WallRack2, DisplayTable1, WallRack5. `ForgeService` heats by `heatTime`.
- `Plot.Shop.Displays`: tables at plot z -41 / -29.5 / -18; `WallRack5` has `BackWall`: `TycoonService.pushWorkshopBack` moves BackWall displays, their pads, their cradles' `Home` and swords on them. `ShopService`: `AISLE_ROWS` {-2.8, 7.25, 18.75, 28.9}; customers walk to the holder's Inspect point as it is now.
- `RackService`: a big sword (Blueprint.big) takes hooks k and k+1 (not 6-7), drawn between them; hook k+1 gets `TakenBy = k`; `hooksUsed` for capacity and the full sign. `EmployeeService` counts hooks (`hooksOf`, `hooks`). `RackController` reads `TakenBy` and hides markers behind walls (`MyPlot.blocked(part, from, ignore?)`).
- `Plot.Pads.Delivery` in the bay (33, -41). `Smithy.SwordRack(2)` and their pads +4 plot z.
- `Shop.Upgraded.Shell.UpperFrame`: upper posts, side bands, side and back windows.
- `Plot.Leaderboard` (tag `PlotLeaderboard`, `Board.Face` columns Playtime / Coins / Gems, Row1-10 Who / Amount); `ServerScriptService.LeaderboardService` (OrderedDataStores `Leaderboard_<Stat>_v1`, keys `player_<UserId>`, 120 s).

## Ten new swords (2026-10-29)

- `Shared.BladeData`: profiles `machete`, `scimitar`, `cutlass`, `jian`, `khopesh`, `dadao`, `rapier`, `hooksword` (96 stations), `claymore`, `flamberge` (128 stations), appended at the end; `order` is by value (17 ids). Hand-edited in Studio: the vault's `Prototypes/tanto-forge/dist/data` + `tools/export-luau.js` no longer match. Backup `ServerStorage.Legacy.BladeData_beforeMoreSwords`.
- `Shared.Blueprints` PRICING: the ten, each with its own hilt (tradition "World" / "Chinese" / "Western", unused by code); `claymore` and `flamberge` have `big = true`. Backup `Legacy.Blueprints_beforeMoreSwords`.
- `ReplicatedStorage.SwordParts.CutlassHilt / ScimitarHilt / KhopeshHilt / FlambergeHilt`: 0.62/0.45/0.376 (137809303072726), 0.65/0.40/0.403 (135894150759729), 0.55/0.30/0.418 (132189246397043), 1.45/0.75/1.04 (85035278889349); the cutlass backstrap is in its Pommel, the flamberge's parrying lugs are in its Guard on a collar round the ricasso.
- `ReplicatedStorage.SwordParts.RapierHilt / JianHilt / DaoHilt / HookSwordHilt / ClaymoreHilt / MacheteHilt`: Grip, Guard, Pommel MeshParts in the Handle frame (X toward the blade, +Z the edge), attributes `GripLength` / `BladeOffset` / `Back` / `SourceAsset`: 0.85/0.60/0.72 (79575672671825), 0.80/0.50/0.525 (139441207379655), 1.20/0.66/0.91 (126787879838005), 0.70/0.45/1.335 (139558108475255), 1.50/0.95/1.082 (91715863201838), 0.65/0.38/0.41 (139036409025642). Built by `Models/Hilts/build_more_hilts.py` (vault). Machete rivets are in its Pommel, its tang strips in its Guard.
- `Shared.Upgrades`: `MacheteBlueprint` … `FlambergeBlueprint` (ten, a chain, each also after a spine goal); pads `Plot.Pads.<id>Blueprint`, all at the second blueprint spot, 4.5 studs left (plot −X) of the first.
- `Shared.Employees.TRAIN_PRICE`: the eight ordinary new swords.
- `ReplicatedStorage.SwordMeshes`: 171 baked shapes (all 17 blueprints).
- `ServerStorage.Builders.bake_sword_meshes` and `Tests.SwordMeshSpec`: set `SwordMeshCache.bakeLive = false` too (since 2026-10-26 live meshes drop their EditableMesh, which the bake packs).
- Tests: `ForgeCheckSpec` expects 17 blueprints and three big; `EtchingSpec` loops all 17.

## Decorate button (2026-10-29)

[[Sessions/2026-10-29#Decorate button in the shop]]. `StarterGui.DecorateGui.Bar.Button` (icon + label pill, a trimmed copy of `AutoRollGui`); `StarterPlayerScripts.DecorateController` shows it while the player's root is inside an unlocked `InsideZone` under their plot's `Shop` (Starter or Upgraded) and `MyPlot.tutorialDone`, polling every 0.25 s, with AutoRollController's slide. `Activated` isn't connected yet: the decoration system will open from it.

### UI review (2026-10-29)

- `UiFx.fit(scale, refW, refH, min?, max?)`: max defaults to `DESKTOP_MAX` 1.5 (was 1); a window over `SCREEN` (85%) of the screen is scaled back (deferred, from its AbsoluteSize). Hotbar passes max 1.2.
- `UITextSizeConstraint` caps are post-scale pixels: all StarterGui caps raised 1.5x. Shop card `Info.Top.Title`: TextScaled off, 22, wrapped.
- `HotbarGui.Templates.Slot` 84 x 100 (Art 81 x 49, Title 17, Metal 14); `Hotbar` TITLE_UP -12.

## Decorations (2026-10-29)

[[Sessions/2026-10-29#Decorations]]. Supersedes, above: the Decorate button's tap doing nothing.
- `Shared/Upgrades`: `decor: boolean?` on the type; six `Decor*` entries at the end of the list (no pads, no `after`).
- `TycoonService.BuyUpgrade`: a `decor` upgrade skips the pad lookup and reach check. `pushWorkshopBack` also moves `Plot.Shop.Decor` children with `BackWall` (the Wall Scroll).
- `workspace.Plot.Shop.Decor`: one `TycoonItem` model per decoration (`Upgrade` = id; `Left` / `Right` or `Piece` sub-models). Built by `ServerStorage.Builders.build_decor` (`require` a clone to rebuild; it replaces the folder).
- `StarterGui.DecorateMenu` (IgnoreGuiInset, DisplayOrder 7): `Dim`, `Window` (Fit, Content.Header.Title/Close, Content.Body with a UIGridLayout 180 x 176), `Templates.Item` (hidden; `Preview` ViewportFrame, `Title`, `Buy.Price.Coin/Amount`, `Owned` check).
- `DecorateController`: builds a card per `decor` upgrade at start (dropping a previous run's), fills each `Preview` on open from the plot's model (first sub-model, lights removed, camera from the plot's -z side), shows `Buy` or `Owned` from `Bought_<id>`, buys through `BuyUpgrade` (pack offer on a shortfall), closes on a buy, X, B, Escape or leaving the shop.

## Seven fictional swords (2026-10-29)

- `Shared.BladeData`: profiles `crescentfang` (96 stations), `shardblade`, `moonbite`, `serpent`, `seraph` (128), `leviathan` (96), `thornspire` (192), appended after `flamberge`; `order` has them between `hooksword` and `zanbato` (24 ids). Generated by `Models/Hilts/Fictional/design.py` (`profiles.luau`); Seraph and Thornspire from the straightened reference traced by `Fictional/trace_ref.py` (`traced.json`). Backup `Legacy.BladeData_beforeFictionalSwords`.
- `Shared.Blueprints` PRICING: the seven (tradition "Fictional", none big), each `hilt = "<Name>"`. `Shared.Upgrades`: `CrescentFangBlueprint` … `SeraphBlueprint`, a chain after `FlambergeBlueprint`; pads `Plot.Pads.<id>Blueprint` at world (652, 0.2, -339), the third spot, 4.5 past the second (plot +X). `Shared.Employees.TRAIN_PRICE`: all seven.
- `Shared.Hilts.dress`: a template part with the `KeepLook` attribute keeps its own Color and Material (any tier).
- `ReplicatedStorage.SwordParts.<Name>Hilt` for CrescentFang, ShardBlade, Moonbite, Serpent, Leviathan, Thornspire, Seraph: MeshParts in the Handle frame (the ten's rotation; position = (-z, y, -x) of the Blender bounds centre), attributes `GripLength` / `BladeOffset` / `Back` / `SourceAsset`: 0.8/0.47/0.732 (100667839864656), 0.75/0.45/0.705 (121114953403171), 0.75/0.42/0.665 (97550387621419), 0.8/0.5/0.68 (94620863875123), 1.1/0.7/0.81 (80749669246461), 1.34/0.736/1.007 (123990932459128), 1.07/1.342/0.976 (126727015651341). KeepLook parts: `Gem` (CrescentFang, Serpent, Leviathan, Seraph), `Crystal` (ShardBlade), `Moon` (Moonbite: pommel faces and the blade's moon phases), `Bands` and `Marks` (Thornspire: the blade's slot and markings), `Wings` and `Trim` (Seraph). The Seraph's gold centre line is in its `Guard`. Blade markings are thin shells 0.006 studs off the finished blade's surface. Built by `Models/Hilts/build_fictional_hilts.py` (`FictionalHilts.blend`).
- `ReplicatedStorage.SwordMeshes`: every blueprint's 9 shapes baked (216; 63 new); `SwordMeshSpec` 866 checks.
- Tests: `ForgeCheckSpec` expects 24 blueprints in order and the fictional ones not big; `EtchingSpec` loops all 24. Backups `Legacy.ForgeCheckSpec_beforeFictionalSwords`, `Legacy.EtchingSpec_beforeFictionalSwords`.
- `Development/economy_model.py`: BASE / PADS / `BLUEPRINT_PAD` with the second and third pads; the big-sword share uses the best big sword known.

## Hilt quality pass (2026-10-29)

[[Sessions/2026-10-29#Hilt quality pass]]. Backups: `ServerStorage.Legacy.<Name>Hilt_beforeQualityPass`.

- `ReplicatedStorage.SwordParts.<Name>Hilt` for Cutlass, Rapier, Khopesh, Scimitar, Flamberge, Claymore, Longsword, Falchion, Gladius, HookSword, Dao: new Grip / Guard / Pommel meshes (same names, roles, properties and `GripLength` / `BladeOffset`), placed with the ten's rotation at (-z, -y, -x) of each part's Blender bounds centre (the Y term was missing from the fictional row above; it only matters off y = 0). `Back` 0.39 / 0.704 / 0.418 / 0.4541 / 1.089 / 1.177 / 0.959 / 0.635 / 0.558 / 1.165 / 0.91; `SourceAsset` in `Models/Hilts/Quality/assets.json`. The Flamberge's `Grip` also holds the leather sleeve over the ricasso (tier grip colour); the rapier's pas d'âne and the flamberge's lugs reach past `BladeOffset` over the blade.
- Built by `Models/Hilts/build_quality_hilts.py` (`QualityHilts.blend`); review blades from `Models/Hilts/Quality/blades.json` (Studio's finished `BladeCore` params); IoU against the silhouette sheet with `Quality/iou.py`; upload with `Quality/upload.py`. JianHilt, MacheteHilt and KatanaHilt unchanged.

| `Shared/EtchPatterns` (2026-10-29) | `strokes(id, length, widthAt, edgeAt?)`.
- `core(length, widthAt, edgeAt)`, cached per `widthAt`: samples every 0.5 cm, detrends by the mean midline, opens the edges (max then min over R = 1.5 × the median capped width, shrinking into the tip), then a half-radius erosion and mean. It returns the width and the lower side's height above the edge line.
- Generators see the core width capped at 7 cm.
- `limitOf` is the start of the last steep stretch before the tip.
- Points are clamped to the face with `room` (`0.035 w + r` to `0.965 w − r`, where r = THICK × h + halo). Fill polygons are clipped straight over their x-range, and shards with nothing left are dropped.
- `Shared/BladeEtch.surface().edgeAt(x)` is the edge line in cm. [[Sessions/2026-10-29#Fictional swords: even etches and symmetric markings]] |
| `Models/Hilts/build_fictional_hilts.py` (2026-10-29) | `paint_sym(name, bm_map, polys_uw, ...)`: (u, w) outlines off the blade's middle; the keep-side half is triangulated, reflected and clamped onto the blade. `mirror_halves(obj)`: bisects at x = 0, mirrors and merges. `trace_ref.py`: `symmetric(mask, ax, pair)`, and `cb` (the blade's centre column) in `traced.json`. |

| `Shared/Deliveries` (2026-10-29) | Requires `Blueprints`. `mismatch(o, sword)` returns "Stand only" for a big blueprint before anything else, so no order takes one. `DeliveryService.refill` builds offers from known blueprints minus big ones. |

| `Shared/Orders` (2026-10-29) | `pickBlueprint(rng, known)`: the top three non-big blueprints by `basePrice`, weights 3:2:1. `Orders.typicalMetal(luck)` = Σ multiplier × `Materials.odds(luck)` / 100. `Orders.pay(value, metalMult?, typical?)` = value × max(1, typical / metalMult) × PAY. `ShopService` Order "fill" passes the sword's metal multiplier and `Upgrades.mergeFactor(d.merges)`. |

| `ServerStorage.Builders.ExportBalance` (2026-10-29) | Edit only. `(url?, mode?)`: posts `balance.json` and `golden.json` to `url` (default `http://127.0.0.1:8765`); with `mode == "hashes"` it returns the 22 sources' FNV-1a hashes. It requires a clone of `Shared` (`ExportShared`) and a SmithyCore clone pointed at it. Script constants are read by pattern (`grab`). Golden draws use `fake(seq)` (NextNumber in turn; NextInteger = a + floor(u·(b−a+1))). |
| `Development/sim/` (2026-10-29) | `rules.py` (`load()` → `Balance`: the game's formulas from `balance.json`; `FakeRng`), `test_parity.py` (unittest against `golden.json`), `check_export.py` (hash check), `receive.py` (localhost receiver). `economy_model.py` imports `rules` and takes every game number from the export. |

| `ShopService.browseEmpty(plot, ctx)` (2026-10-29) | `runCustomer` calls it when no holder of the plot has a sword. It picks a random unlocked slot (`slot.customer = ctx` while there), walks in along `slot.route` to its Inspect point, `say`s "Nothing for sale yet?", waits 2.5 s, and walks back out to `CustomerSpawn`. No rickshaw, no Promoter count. |
| `Development/sim/` step 2 (2026-10-29) | `engine.Sim` (heapq events: player, spawn, offer, answer, letter, crafter, stocker, etcher, weather, autoroll, cart_back, browsed, sample; `self.T` timings), `behavior.ARCHETYPES` / `PAYERS` / `choose_target`, `scenarios.SCENARIOS`, `run.py` (multiprocessing, seeds `<seed>:<i>`), `report.write(out_dir)`. Layout in `balance.json["layout"]`. |

| `ServerScriptService.PlaytestLog` (2026-10-29) | ModuleScript, Studio only: `log(player, kind, data)`. Batches and posts to `http://127.0.0.1:8765/playtest/<UTC start>` every 15 s and on BindToClose, keeping the events if that fails (max 50,000). Also logs `pos` every 1 s in plot space (`PlotService.plotOf(...):GetPivot()`), `prompt` / `hold` (`ProximityPromptService`, `<model>/<ActionText>`), `join` and `leave`. Hooks: ForgeService (`pull`, `collect` in `takeOre`, `furnace_put`, `furnace_take`, and the crafter `handBack` with `crafter = true`), SmithService (`forge_begin`, `forge_finish`), PolishService (`polish_begin`, `polish`), EtchService (`etch`), ShopService (`display`, `offer` in `askOwner`, `visit`, `browse`, `sale`) and TycoonService (`buy`). |
| `Development/sim/` loop and calibration (2026-10-29) | `engine`: `sw["t"]`, `loop_done`, `loops_own` / `loops_crew`, `first_pull`. `run.summarize`: `loop_own`, `loop_crew`, `first_loop`. `receive.py`: `/playtest/<session>` → `playtests/<session>.jsonl`. `calibrate.measure(events)` → (`{timing: [s]}`, extras); `main` writes `timings.json`. `timings.MEASURED` / `timings.T` (the estimates overridden by measured medians with n ≥ 5) feed `engine`, `scenarios` and `report`. |

| `Development/sim/` walking routes (2026-10-29) | `calibrate.station(e)` (event → `engine.pos` name), `measure` → `ex["routes"]` (`route_key` → [seconds moving]); `timings.json` gains `routes` (n ≥ `MIN_ROUTE` 3) and `walk_speed`. `timings.route_key(a, b, upgraded)`, `ROUTES`, `WALK_SPEED`. `engine.layout_pos(raw)`; `Sim.walk` uses `ROUTES` scaled by `WALK_SPEED / self.speed`. PlaytestLog adds `rack` (RackService.RackAction), `forge` on furnace events and `u` on `pos`. |

| `Development/sim/` gems, mail, cart, days (2026-10-29) | `rules.order_fits`, `make_delivery`, `daily`. `behavior.Archetype.mail` ("chase" or "fit") and `.gems` ("mail", "customers" or "cheapest"); `GEM_GROUPS`, `PLAY_DAY`. `engine.Sim`: `on_day`, `mail_clock`, `new_order`, `on_mail`, `mail_fit`, `task_mail`, `order_for`, `cart_refill`, `cart_fill`, `task_cart`, `task_cart_collect`, `buy_gems`, `hire_reserve`, `wants_etch`, `add_gems`; rng streams `mail` and `cart`. The result has `gems_in`, `gems_out`, `gem_levels`, `gems_left`, `mail_done`, `mail_coins`, `cart_bulk` / `special` / `skips`, `reputation`, `days`. `report` section 8. ExportBalance golden: `deliveryMake`, `orderMismatch`, `daily`; `deliveries.senders`. |

| Cart skip wait (2026-10-29) | `Shared.Deliveries.SKIP_WAIT`, `State.waiting`, `public().waiting` (seconds left); `DeliveryService.refill` drops due waits, skip queues one, the board loop refills when due; `DeliveryController`: `waitCards`, `Templates.Waiting` (Row.Icon clock, Row.Label countdown). PlaytestLog events added: `letter`, `mail`, `cart_accept` / `skip` / `send` / `collect`, `gem_buy`, `hire`. |
| `SlotMarker`, plot template racks | 2026-10-29: each marker refresh in `pcall` (one error no longer freezes every marker); `IngotRack`, `IngotRack2`, `SwordRack`, `SwordRack2` are `ModelStreamingMode` Persistent so their `Slots` never stream out. |

## Decorate mode (2026-10-29)

[[Sessions/2026-10-29#Decorate mode: walk around and press +]]. Supersedes, above (Decorations): `Plot.Shop.Decor` TycoonItems and `StarterGui.DecorateMenu`. `Plot.Shop.Decor` = spot Parts (`Kind`, `Side`, `BackWall`) plus placed clones (`Spot` attribute); `ReplicatedStorage.DecorModels.<id>` (`Kind`, `Count`; `Piece` or `Left`/`Right`); `ServerScriptService.DecorService` (`Remotes.SetDecor` RemoteFunction, `SmithData.decor` spot -> id, plot `Decor_<spot>` attributes, restore in `PlotService.onPrepare`); `DecorateController` toggles decorating (Done), SlotMarkers per spot, `ItemPicker` card art kind `model`.
| `EtchingTableController`, `EtchService` | 2026-10-29: either Etching Table (`EtchingTable`, `EtchingTable2`, both with `Top.EtchPrompt`, Persistent). |
| `PolishController`, `PolishService`, `Smithy.PolishStation2` | 2026-10-29: two Polishing Stations; the client uses the one whose prompt you used, the server the nearest bought one in reach (`PlayerPolishing` on that one). |
| `RackService` / `RackController` "fill" | 2026-10-29: Store all card; fills the rack from carried ingots / swords (dearest first, big ones need two hooks). |
| `NpcWalk` corners | 2026-10-29: early waypoint switch only on near-straight legs (25°), 0.6 at turns; AgentRadius 1.75. |
| `Shared.Store` small packs, `StoreService` Starter Pack | 2026-10-29: Coins800/1800, Gems7/15 (9 / 19 R$); Starter Pack gives `STARTER_COINS` 10,000 with its 100 gems. |
| `WeatherController` tip | 2026-10-29: `refresh()` fills the tip before showing; hover (mouse only) or a 4 s tap. |
| `MenuGui.Buttons.*.Label` | 2026-10-29: text labels on the menu buttons. |
| `DeliveryService` / `DeliveryController` / `Shared.Deliveries` queued order | 2026-10-29: `delivery.queued`; actions pack, unpack, cancel "queued"; collect promotes queued to active. |
| `ItemPicker` art queue | 2026-10-29: card art (`artModel` + `outline`) built after the window opens, ~4 ms a frame (`ART_BUDGET`, `artGen` drops stale jobs). |
| `EtchPlayback.prepare` / `load`, `EtchingTableController` warm-up | 2026-10-29: show first, images after; sword and pattern meshes warmed while picking. |
| `SlotMarker` opts, `Decorating` attribute | 2026-10-29: per-marker range and decor flag; other markers hide while decorating. |
| `EmployeeService.putBack` | 2026-10-29: a held ingot back on the rack only while it has room, else to the player. |
| `CollectionController` pages | 2026-10-29: Metals and Swords tabs; sword cards in an Entry `View` from `ItemPicker.artModel`. |

## Decorate camera mode (2026-10-29)

[[Sessions/2026-10-29#Decorate camera mode]]. Supersedes, above (Decorate mode): the Done toggle and walking with markers. `StarterGui.DecorateEditor` (HidesHud, IgnoreGuiInset, DisplayOrder 4, Enabled only while decorating): `Panel` (UISizeConstraint 900 x 230; `Shadow`, `Fill` from Settings; `Body.Tabs` chip row, `Body.Coins.Amount`, `Body.Cards` horizontal ScrollingFrame; `Close`), hidden `Templates.Tab` (the Deliveries tab look) and `Templates.Card` (`Art` ViewportFrame, `Title`, `Tag.Coin/Words`, `Edge` stroke for the pick). `DecorateController`: `setEditing` (anchors the root, `ProximityPromptService.Enabled`, `Decorating` attribute), `framing(section)` from the section's spots (`VIEW` pitch/height per section, the band between the top bar's inset and the panel's top), `PreRender` ease, SlotMarkers with range 1000 shown for the current section (bag on placed, + on empty spots fitting the picked card), `place` (BuyUpgrade then SetDecor), `takeBack`. Spots: `Section` attribute (`build_decor` `SECTION` by Kind). Old script `Legacy.DecorateController_beforeCameraMode`.

## Features and fixes (2026-10-29)

| Where | What |
|---|---|
| `CrewGui`, `EmployeeController` | `Roster` holds `Templates.Section` (Header line + `Cards` grid) per role; title "Crew"; no `Tabs`. Swords picker: Random (`glyph` card) first, "Active" chip only. Hire price never veiled; short → `PackOffer`. |
| `EmployeeService`, `SmithyCore` | `make "random"`; `oneSword` picks a trained non-big shape per sword; `teach` leaves Random alone; decode keeps `"random"`. |
| `ItemPicker`, `PickerGui` | `glyph` art kind (`Glyph` label in Card / CompactCard); spec `back` shows `Header.Back`; empty chip hides. |
| `MenuGui`, `MenuController` | `Mail` moved out of `Buttons` to the right; `Buttons.Shop.Rays` spin + icon hop; Shop `Currency` 4 a row with `Pile` art. |
| `GemGui`, `GemController` | Daily tiles 96 x 124, `Days` wraps at 4, centred; Gem Shop cards have an `Icon` (`ICONS`), never veiled. |
| `DeliveryGui`, `DeliveryController` | `Header.Rank.Tip` (hover / tap); `estimate(o)` "~coins"; Capacity / Speed short → pack. |
| `PromptFilter` | Touch: prompts' ActionText / ObjectText cleared. |
| `ReplicatedStorage.PadParts`, `TycoonService`, `TycoonController` | Bevelled pad meshes; `SINK` 0.3, `RELEASE` Back 0.35 s. |
| `NpcWalk` | `CLOSE` 4: stuck near the goal stays put; a real snap warns. |
| `Shared/Customers`, `ShopService` | `LINES`, `line(key, fill, rng)` for every bubble. |
| Brown windows' `Fill` | `Pattern` + `Tint` (the picker's seigaiha). |

## Analytics funnels (2026-10-29)

| Where | What |
|---|---|
| `ServerScriptService.Analytics` (new ModuleScript) | `log(player, kind, data)` maps PlaytestLog kinds to AnalyticsService: economy (`coins` / `gems`, summed by SKU every 120 s), counters (summed), one-off custom events (8 a player a minute, the rest counted in AnalyticsDropped), Milestone, SessionEnd and the Playtime funnel (checked every 30 s). `funnel(player, name, id, step, stepName)` for the recurring MailOrder / Delivery funnels. Loops and the `SmithyCore.onLeave` / `onRejoin` hooks start only in a running game (`shared.AnalyticsLive`). Requires SmithyCore and Shared/Materials, nothing else. See [[Development/Analytics Funnels]]. |
| `PlaytestLog` | Every event also goes to `Analytics.log`; outside Studio `log` is `Analytics.log`. Don't load-check it by `require` in Edit: it requires PlotService, which moves `workspace.Plot` to ServerStorage and builds the six empty plots. |
| `SmithyCore` | `FUNNEL` is id → `{ step, name }` (ids saved, never renumbered; GemService reads 11); `funnel` holds steps after the tutorial's end (id 9) until it comes and logs `OnboardingTime`. |
| `ForgeService`, `ShopService`, `TycoonService`, `GemService` | Onboarding ids 12 (ore collected), 13 (ingot heated), 14 (first letter opened), 10 (any pad, was Ore Slot 2), 15 (gem upgrade bought). |
| `ShopService`, `DeliveryService`, `TycoonService`, `GemService`, `EmployeeService`, `StoreService` | `PlaytestLog.log(player, "coins" / "gems", { n = ±amount, sku, type? })` after every coin or gem change; `merge`, `haggle`, `mail_decline`, `pass` kinds; MailOrder and Delivery funnel steps. |
| `CollectionGui.Templates.Entry`, `CollectionController` | `HalftoneClip` full-bleed with `Rays` (12) and `Glow` (hidden on metals); `Shadow` ViewportFrame 2 px down-right; sword cards dark brown, each sword built twice (view + shadow). |
| `OreBoxShow`, `ReplicatedStorage.OreRollFx` (Sparks, Dust, Beam), `WorldText.RarityCallout`, `Cues.RollLand` | Climb effects scale by tier (`climbed`), landing squash / dust / tink / glow (`landed`), Rare+ callout; camera shake via Humanoid.CameraOffset within 30 studs. |
| `Smithy.OreRoller.Stand1-6` | Square Pedestal/Band (3.25); back row (4-6) same height as front, 1.4 studs behind. |
| `Smithy.Anvil2-4.Hearth`, `WorkshopFittings.Hearth` | Allen's SmoothPlastic slab (WoodBase mesh, 11.75 x 0.79 x 8.59), top at 0.84; slate hearths in Legacy. |
| `Smithy.OreRoller.NavBlock`, `NpcWalk` | Invisible box over the stands, PathfindingModifier `Avoid` (CanQuery on), costed `math.huge` in NpcWalk's AGENT. |
| `EmployeeService` | `putBack` (ingot) / `putBackSword`; racking waits while `SwordRack` is missing. |
| `Cues.RollMorph`, `OreBoxShow` | Whoosh per metal change while flickering, first ingot only. |
| `HiltSeat` | Seat impact (`impact`: clang, `OreRollFx.Sparks` + PointLight from the guard, hot orange below Rare, the tier's colour from Rare up; a 0.06 s still, then the camera punch and push-in in the frame loop) and the reveal (`reveal(t)`: lift `LIFT` 0.12 toward the camera and turn to face it, the tier-coloured sweep along `SwordMeshCache.edgePath` with `Cues.HiltReveal`, the drop and fade; `finish()` at `DROP_AT + DROP` = 2.0 s). `skip()` on a press once lifted. `buzz(kind)`: a `HapticEffect` (UIHover per `TICK` 0.3 studs of slide, GameplayCollision on the seat). The blade part is inside `SeatingHilt` now. |
| `SwordMeshCache.edgePath(params)`, `.along(path, u)` | The glare line (edge bevel, 14 points, base to tip, blade space), moved from `SwordRenderer`, which uses them now (its BladeCore require is gone). |
| `SoundService.Effects.Cues.HiltReveal` | Pro Sound Effects "Sword Draw Clang Unsheathing Two Sabers 30" (9119744718), volume 0.4, SoundGroup Effects. |
| `HiltSeat` (reveal) | The light sweep is gone (2026-10-30): the reveal is lift and turn, `Cues.HiltReveal` at `RING_AT` 0.8 s, drop at 1.7 s. |
| Collision group `NpcPass`, `ShopService` | Not collidable with `Npcs` (registered in Studio and by ShopService). Set in Studio on the raised parts (bottom at least 1.7) of `Plot.Shop.Displays` tables and wall racks and `Plot.Smithy` sword and ingot racks, 59 parts. A new raised furniture part NPCs walk past should join it. |
| `NpcWalk.blockers` | Stuck and stopped-short warnings name the solid parts within about a stud of the NPC and what it stands on. |

## Faster Strikes (2026-10-30)

[[Sessions/2026-10-30#Faster Strikes]]

| Where | What |
|---|---|
| `Shared/Upgrades` | `Strikes1-5` (Faster Strikes I–V, 250 / 1,000 / 2,500 / 5,000 / 10,000; `after` Wakizashi, Katana, Crafter, Anvil3, Falchion with the level before). `STRIKE_PACE` { 1, 0.9, 0.8, 0.7, 0.6, 0.5 }; `strikePace(plot)` via `tier(plot, "Strikes")`. |
| `AnvilController` | `plot` (from `MyPlot.get()`) kept as a local. `strike()` reads `Upgrades.strikePace(plot)` each strike and scales `TIMING.windup`, `drop`, `recover` and `move`; `deform` unscaled. Sparks `round(14 + 20 × (1 − pace))`. |
| `Shared/ForgeCheck` | `MIN_SECONDS_PER_STRIKE` 0.25 (was 0.35). |
| `Workspace.Plot.Pads.Strikes1-5` | Copies of `Pads.Heat1` (Workshop) at plot (−31, −0.3, 64). |
| `ServerStorage.Builders.ExportBalance` | `B.strikePace`. |
| vault `Development/sim` | `rules.strike_pace(owned)`; `engine.task_forge` scales `T["forge"]` by it; `economy_model.player_T` subtracts `timings.T["forge"] × (1 − pace)`. |

## Mail width and delivery trip chips (2026-10-30)

[[Sessions/2026-10-30#Mail window width; delivery trip ticks]]

| Where | What |
|---|---|
| `StarterGui.MailGui.Window` | `Size` {0, 572}, {0, 0}, `AutomaticSize` Y (was XY: `Fill.Pattern`/`Tint` widened it to 791). |
| `StarterGui.DeliveryGui.Window.Content.Trip` | `UIListLayout.Padding` 4. `Step1-4` 172 / 188 / 254 / 161 × 56; `Icon` at (8, 10); `Title`, `Sub` at x 52, width {1, −60}, no AutomaticSize, truncate AtEnd; `Tick` 22 × 22, anchor (0.5, 0.5) at (40, 41), ZIndex over the icon. `DeliveryController.showTrip` unchanged (it sets text, colours and `Tick.Visible`). |

## Deliveries layout C (2026-10-30)

[[Sessions/2026-10-30#Deliveries layout C]]

| Where | What |
|---|---|
| `StarterGui.DeliveryGui` | `Header`: `CartButton` ("Upgrade cart" / "Back"), `Cancel` (brown, the old tabs' look; `Tabs` gone). `Body`: `Strip` (128 tall: `Town.Chip`, `Title`, `Crates` (UIGridLayout), `Step1-4` round badges with `Icon` and `Tick`, `Line1-3`, `Status`, `Detail`, `AutoFill`, `Send`, `Collect`, `Pin`), `Offers` (ScrollingFrame, grid 396 × 188), `Swords` (grid 130 × 150), `NoSwords`, `Cart` (unchanged cards, under the strip). `Templates`: `Offer` (new: `Art`, `Kind`, `Title`, `Chips.Town/Need`, `Rewards.Coin/Pay/Star/Rep/Gem/Gems`, `Buttons`), `Brown`; `Order`, `Crate`, `Body.Orders/Packing` and `Content.Trip` removed. Built by `ServerStorage.Builders.BuildDeliveryGuiC` (+ `DeliveryLayoutKit`). |
| `DeliveryController` | Rewritten for layout C: `showCart` replaces `tab`; `packOrder()` decides the strip's order (packing, or the queued one while the cart is out) and the page under it (`Swords` vs `Offers`); `showTrip()` paints the strip (badges, status / detail, which buttons show) and `tick()` keeps calling it; crates are `Templates.Slot` in `Strip.Crates`, interactive while packing (`makeCrates(o, onTap)`), display-only on a trip (`cartCrates`), sized by `crateSize` (≤ 6 at 40, else two rows at 20). `button()` takes a height (offers' 44). `FIXED` 122, body clamped 290–430. Unchanged: `trip`, `packOrder`, `call`, `estimate`, the cart specs / `cartTab`, the rank tip, `open` and the prompts, the pinned order and `SmithState`. Backups: `ServerStorage.Legacy.DeliveryGui_beforeLayoutC`, `DeliveryController_beforeLayoutC`. |

## Refinements (2026-10-30)

[[Sessions/2026-10-30#Refinements (2026-10-30)]]

| Where | What |
|---|---|
| `StarterGui.DeliveryGui` | `Strip` 108 tall, `Step1-4` 44 px centred at x 410, `Status`/`Detail` 300 wide on the same centre; pages at y 120. `Templates.Offer`: `Art` 64, `Title` (88, 10) 30 pt, `Kind` (88, 48), `Chips` (12, 84) no wrap, chip labels 20; `Reward` panel (12, 120) 170 × 60: `Coin`, `Pay` (gold 28), `Extra.Rep` / `Extra.GemsIcon` / `Extra.Gems` (`Rewards` row gone). Header: `Title` inside (44 pt), `Content.UIPadding.Top` 16, `CartButton` / `Cancel` 150 wide. Hand edits after `BuildDeliveryGuiC` (rerunning it would not apply them). |
| `DeliveryController` | `FIXED` 104; `crateSize` one row up to 28; no order: `Title` hidden, the status line "Pick an order below"; offers fill `card.Reward`. |
| `StarterPlayerScripts.PromptStyle` (new), `ReplicatedStorage.WorldText.Prompt` (new BillboardGui) | Default-style prompts → Custom, attribute `Styled`; one billboard per shown prompt (`Button` with `Tap` / `Key` / `Hold`, `Action`), tap/click → `InputHoldBegin/End`, hold fill on `PromptButtonHoldBegan`. Skips Custom prompts and ScreenButton ones while ActionGui is on. |
| `PromptFilter` | The touch word-clearing (`bare`) is gone. |
| `StarterGui.MenuGui` | `Mail` has `HudPart`; `Buttons.UIGridLayout.FillDirectionMaxCells` 2; LayoutOrder Book 1, Upgrades 2, Shop 3, Crew 4, Daily 5, Settings 6; labels upper case, stroke 2.5 (18, 12, 8). |
| `HudGui.Coins.Row.Count`, `GemGui.Gems.Row.Count` | Heavy, stroke 2.5 (18, 12, 8) on both layers; the label is the black under-layer (text (18, 12, 8)) and its child `Face` the white number on top, Position (0, -0.08) scale; `Hud.setCount` and `GemController` set `Face.Text` with `Text`. |
| `SmithyCore` | `swordValue(sword, withPolish?, withEtch?)`; public swords add `polishedValue` / `etchedValue` (nil once done). |
| `ItemPicker` | A chip "N → M coins" shows the coin and "N → M" with M green (RichText). |
| `EtchingTableController`, `StarterGui.EtchHud.Value` | Sword chip now → etched; subtitle names the 15%; `play(session, message, sword)` counts `Value` up with the drawing, pops and plays `Cues` "Sale" as it lands; `INSPECT_TIME` 1.0. |
| `PolishController`, `StarterGui.PolishHud.Panel.Value` | Chip now → polished; subtitle names the 10%; a finished save pops `Value`, `UiFx.countUp` 0.8 s, waits 0.6, then closes (`saving` blocks input meanwhile). |
| `UiFx` | `countUp(label, from, to, seconds)`. |

### Refinements, second round (2026-10-30)

[[Sessions/2026-10-30#Refinements, second round (Allen's playtest notes)]]

| Where | What |
|---|---|
| `DeliveryGui.Window.Content.Body.Strip` | `Crates` gone; `Load` (236 × 14 at (16, 82), `Fill` green); `Name1-4` (step names for the empty strip); `AutoFill` (258, 58) and `Send` (418, 58) 144 × 42, `Collect` (330, 58), `Pin` centred at (410, 58); `Status` (564, 24) and `Detail` (564, 54) 240 wide, centred. |
| `DeliveryGui...Body.Swords` | A UIListLayout over `Slots` (grid 52 × 52, gap 6) and `Cards` (grid 130 × 150, gap 12), both auto-height. |
| `DeliveryController` | `makeCrates(o, onTap)` into `shelf.Slots` (no strip crates, no `crateSize`); sword cards into `shelf.Cards`; `cartCrates()` only clears; `placeSteps(spread)`; `showTrip` sets the load bar, the step layout and the new status texts; Skip 76, Accept 104. |
| `PromptStyle`, `OreRoller.Machine.RollPrompt` | Attribute `PromptAt` (Vector3, the part's space) → the billboard's `StudsOffsetWorldSpace`; the lever's is (0, -1, 1.97). |
| `PickerGui.Templates.Card / CompactCard` | `Chip`, `Qty` ZIndex 5. |
| `StarterPlayerScripts.TextLayers` (new) | Binds every TextLabel's child `Face` (PlayerGui and workspace, as they appear): Text, RichText, TextTransparency and the stroke's Transparency follow the label; a TextColor3 written to the label moves to Face and the label returns to (18, 12, 8). |
| `ReplicatedStorage.WorldText` | `Face` children on Tag.Role/Title/Level, OreLabel.Title/Rarity/New/Wants, PadLabel.Title/Price, BuyButton.Label.Title/Price, Nameplate.Title, TillSign.Plate.Amount, YourAnvil.TextLabel, RarityCallout.Words, Prompt.Action; the labels themselves near-black with a slightly thinner edge. |
| `MenuGui.Buttons.*.Label`, `MenuGui.Mail.Label` | `Face` children (two layers). `HudGui`/`GemGui` counts: the black layer's edge 2, Face at -0.05. |

### Refinements, third round (2026-10-30)

[[Sessions/2026-10-30#Refinements, third round]]

| Where | What |
|---|---|
| `TextLayers` | Per Face: both UIStrokes' Thickness = clamp(TextBounds.Y × 0.075, 1, 3), on TextBounds changes. |
| `DeliveryGui...Strip` | `Step1-4` 40 px (icon 28, tick 18); buttons 40 tall at y 58; `Pay` (coin, gold `Amount`, centred at x 684); `Need` (the offer card's need chip) centred at (684, 6). |
| `DeliveryController.showTrip` | Coins go to `Pay` (`coins`), words to `Detail`; `Need` from `Deliveries.requirement(o)`, Status/Detail/Pay 12 px lower while it shows; step centres 292 + 80 i. |
| `Plot.Smithy.PolishStation(2).Top.PolishPrompt` | `PromptAt` (2, 1.3, 0). |

| Where (2026-10-30, later) | What |
|---|---|
| `PolishHud.Panel.Value`, `EtchHud.Value` | Coin and `Amount` only (`Gain`, `Pop` deleted). `PolishController`: arcade roll (`targetValue`/`shownValue`, `rollRate` = max(30, gap / 0.6) a second), no partial-save toast, no pops. `EtchingTableController`: the amount = from + (to − from) × drawing progress, linear; "Sale" cue on landing. |

### Polish Boost (2026-10-30)

| Where | What |
|---|---|
| `Shared/Upgrades` | `PolishBoost1-3`; `POLISH_BONUS` {0.10, 0.13, 0.16, 0.20}; `polishBonus(plot)`. Pads `Plot.Pads.PolishBoost1-3` at (26.5, 44). |
| `SmithyCore` | `Blade.polishBonus` (transient); `polishBonus(d)`; `applyPolish(d)` in `push`; `swordValue` uses `blade.polishBonus or POLISH_BONUS`. |
| `TycoonService` | Pushes after a PolishBoost purchase. |
| `PolishController` | Subtitle from `Upgrades.polishBonus(MyPlot.current())`. |
| `UpgradeFx` | PolishBoost → PolishStation, "Polish +a% → +b%". |
| `ExportBalance`, vault sim | `polishBoost`; `rules.polish_bonus`, `sword_value(polish_bonus=)`, engine, economy_model. |

### Customers and the mail popup (2026-10-30)

| Where | What |
|---|---|
| `Shared/Customers` | `list` = one `Regular` (offerMin 1.15, offerMax 1.50, raiseChance 0.5, patience 99, `looks` = three outfits). `raise`: chance = raiseChance x 0.5^max(0, declinesSoFar - 1). `vip` 2.0-3.5. |
| `ShopService.makeNpc` | `look` = a random entry of `c.looks` (else `c.colors`) for the HumanoidDescription colours. |
| `MailGui.Popup` | No UIListLayout: `Portrait` anchored (0, 0.5) at the left middle, `Words` at portrait width + 12. `Timer` TextLabel 20 x 16, anchor (1, 0) at (1, 24, 0, 4) in the right padding. |
| `MailController` | `POPUP_TIME` 8, `STORY_POPUP_TIME` 15; `showPopup` counts `popup.Timer` down each second then hides; `timedOut[key]` stops a story letter popping again (`checkNew`). |
| `Tests.SaveSpec`, `Tests.AnvilSelfCheck` | Offer checks 1.15-1.5; AnvilSelfCheck: every walk-in Regular, raises ~0.5 / 0.25 / 0.125. |
| `Shared/Upgrades` (2026-10-30) | `BigSwordStand.after` = { UpgradedStore }; `ZanbatoBlueprint.after` = { DadaoBlueprint, BigSwordStand } (no Cashier). |
| `Shared/Upgrades` prices (2026-10-30) | Dated comment above `Upgrades.list`; Jian/Dadao/Zanbatō 28k/60k/88k, Crafter 40k, small pads ×2. Sim: `behavior.choose_target` buys stations and cheap pads first for every type; `report.TARGETS` Zanbatō 240 min; `purchase_times.py`, `pacing.py` (waits between buys), `summarize_run.py`; scenarios `old-offers`, `prices+20/30`, `east*`, `m-*`. |

### One sword chain (2026-10-30)

| Where | What |
|---|---|
| `Shared/Upgrades` | Blueprint pads: one chain by value, `after` the sword before it, Wakizashi to Seraph. Prices: Falchion 28k, Jian 50k, Gladius 60k, Khopesh 150k, Dadao 160k. `ZanbatoBlueprint` after Gladius + BigSwordStand; `ClaymoreBlueprint` after Rapier + Zanbato; `FlambergeBlueprint` after Claymore. |
| `Workspace.Plot.Pads` | The 20 ordinary sword pads at plot (-21, 55); Zanbato, Claymore and Flamberge at (-16.5, 55); nothing at (-12, 55). |
| `Builders.build_outside_smithy` | Puts the big-sword pads `BLUEPRINT_SPOT` + 4.5 X. |
| `Guide.blueprintPad` | Walks back along `after` to the first sword you don't know (the Katana letter points at the Machete first). |
| `sim/report.py` | `HEADLINE = "Crafter"`: run notes open with the Sword Crafter and waits over 15 min. Scenarios `one-chain*`, `late*` describe the old branches. |

### SlotMarker loop (2026-10-30)

| Where | What |
|---|---|
| `StarterPlayerScripts.SlotMarker` | Refresh loop `while script.Parent` (a Dev Panel reset destroys the module; its loop kept going and warned 120 times a second); drops a marker whose `gui.Parent` is nil; `warned[m]`: one warning per marker. |

### NpcWalk arrival (2026-10-30)

| Where | What |
|---|---|
| `ServerScriptService.NpcWalk.follow` | `arrived` from `hum.MoveToFinished` (reset before each `MoveTo`): a waypoint counts as passed when the Humanoid reports it reached and is within `ARRIVED + 0.5` studs, as well as by `NEXT_AT` / `CORNER` distance. Fixes the Stocker stalling at the workshop door's turn. |

## Refinements, evening list (2026-10-30)

[[Sessions/2026-10-30#Refinements, evening list]]

| Where | What |
|---|---|
| `Shared/Commissions` | `Commission.polished`, `.want` (the letter's words naming the sword). IronTanto polished, "a polished Iron Tantō". `title` prefixes "Polished "; `mismatch(c, metal, shape, percent, polished)`. |
| `Shared/Upgrades` | PolishStation 30 (was 200); `PolishBoost1.after` PolishStation2; `Stocker.after` Crafter; Delivery no `after`; `HEAT_TIMES` {10, 7, 5, 4}. |
| `Shared/BladeCore` | `finishAt(blade)`: the strikes Finish opens at (`ceil(#recipe × EARLY_FINISH_SHARE)`, 9 of 12); `canFinish` uses it. |
| `ServerScriptService.ShopService` | Letter hand-in passes `sword.blade.polished`; `refillOrders`: More Clients' number minus the open story letters. |
| `ServerScriptService.ForgeService` | `wantPulls[player] = { id, n }`: a pull while a letter wants a metal brings it on the 1-in-3 lean or when the last pull missed (n ≥ 2). |
| `StarterPlayerScripts.Guide` | `craft`: polish step (buy `Pads.PolishStation`, then "Polish it" at `Smithy.PolishStation.Top`); `placed` and `pickerTarget` ignore polish. The cheer needs `GemTour == nil` too. |
| `StarterPlayerScripts.GemController` | `apply(s)`: `GemTour` "todo" while every gem level is 0 (kept "open" while open), nil once one is owned; `close` puts "open" back to "todo"; `toggle` opens while "todo" with the gems (sends "tour" if not toured). The join task's daily window waits for TutorialDone and, if the lessons were on at join, `GemTour == nil`. The daily top bar icon in `task.spawn` (notifies if the dot is already up). `toggle` checks `w.Visible`. |
| `StarterPlayerScripts.MenuController` | `toggle` closes only a window that's showing; the Settings top bar icon in `task.spawn`. |
| `StarterGui.WorkshopOpenGui.Banner` | "Create more swords to sell!" |
| `StarterPlayerScripts.TycoonController`, `ReplicatedStorage.WorldText.PadLabel` | `LABEL_RANGE` 22; `inSight(at, skip)` (camera → label raycast, at most 4 hits skipped: Transparency ≥ 0.9 or a model with a Humanoid); PadLabel `AlwaysOnTop` true. |
| `Workspace.Plot.Pads.Crafter`, `.Delivery` | Plot (-4.3, 59.5) and (30, 0) (were (-9.1, 66.3), (33, -41)). `build_delivery` would put the Delivery pad back if run again. |
| `Workspace.Plot.Smithy.OreRoller` | `Lever`, `Machine` 3 studs to plot -Z (lever at z 15.1); `Machine.PivotOffset` set so the roller's pivot stays (-6.8, 2.8, 23.4). |
| `StarterGui.AnvilHud.Progress.Notch`, `AnvilController.updateHud` | 4 × (bar + 10) px Frame, ZIndex 2, cream (251, 235, 213), dark UIStroke 1.5, UICorner 2; at `finishAt / #recipe`, lime (115, 220, 35) once `canFinish`. |
| `StarterPlayerScripts.HiltSeat` | `DROP_AT` 1.15 (was 1.7). |
| `SoundService.Effects.Polish`, `PolishController` | Looped Sound 9116879206, 0.3, SoundGroup Effects; the Heartbeat eases its volume to 0.3 while `lastStroke` is under 0.12 s old, else to 0, stopping it under 0.01. |
| `StarterGui.PolishHud.Ghost` (+ `Press` UIScale), `PolishController` | Copy of HiltSeatGui.Ghost. RenderStepped, tutorial only (`MyPlot.tutorialDone` false): until `stroked`, glides along `view.part` x 0.15–0.85 of the blade (`WorldToScreenPoint` minus the screen's AbsolutePosition), cycle 2.2 s; once `complete` (no unfinished runs, set in `updateHud`), presses on Save. |
| `StarterPlayerScripts.WeatherController` | At start, destroys camera children named like a `WeatherFx` template (an earlier copy's effect). |
| `StarterPlayerScripts.DecorateController`, `StarterGui.DecorateGui` | Both disabled (`Enabled` false), kept. |
| `StarterGui.HotbarGui.Templates.Slot.Trash` (+ `Icon`, `Armed`), `.Stepper` (`Pill`, `Less`, `Amount`, `More`); `Hotbar` | Bag cards only (ingots and swords). `trashStack(key, n?)` sends the first n ids (Backpack before the held tool); `armed` / `amount`; `over()` keeps a press on them from equipping or dragging. |
| `StarterGui.CrewGui`, `EmployeeController`, `MenuGui.Buttons.Crew` | Pages 350 tall (16 px to the bottom edge), stats rows 36, panels at y 206, station cards 284; `Templates.Card.Cost`, `Needs` wraps; `padLine(card, upgradeId)`: the first unbought `after` pad's "<name> Required", else its price; every section always shown; Crew button always visible. |
| `StarterGui.MailGui.Tracker` (`HudPart`), `MailGui.Templates.Track`, `MailController` | `openLetter(key)` (popup and tracker); `renderTracker()` on SmithState, popup show / hide and fold: up to 3 accepted letters (story first, then orders newest first); the want bold in #961E22 (story letters' `want`, orders' `Orders.prose`). |
| `Tests.SaveSpec` | Letter checks pass a polish; "an unpolished one doesn't" (115 checks). |
| vault `Development/sim` | `engine.offers`: `raw["padCap"]` keeps the cheapest N pads plus blueprint pads and `raw["padAlways"]`; scenarios `cap3`, `cap4`, `cap5` (padAlways Delivery). |

### Allen's answers (2026-10-30, evening)

[[Sessions/2026-10-30#Refinements, Allen's answers (evening)]]

| Where | What |
|---|---|
| `ServerScriptService.TycoonService` | `PAD_CAP` 3, `PAD_ALWAYS` { Delivery }; `standing(plot)`: blueprints and PAD_ALWAYS on offer plus the PAD_CAP cheapest of the rest (`Upgrades.price`, list order on a tie). `refresh` draws pads from it; `BuyUpgrade` refuses a non-decor pad not in it. |
| `ServerStorage.Builders.ExportBalance` | `B.padCap`, `B.padAlways` grabbed from TycoonService's source; TycoonService in `SCRIPT_SOURCES`. Sim: `engine.offers` applies it; scenario `no-cap`. |
| `Shared/Upgrades` | `HEAT_TIMES` {15, 11, 8, 6}. |
| `Shared/Employees` | `LEVEL_GEMS` {20, 55, 105, 200}; `levelGems(level)` (nil at Lv. 5). |
| `ServerScriptService.EmployeeService` | `Employee("level", crafter id or staff role)` before the crafter guard: spends `levelGems`, sets `made` / `count` to the next level's work, adds the difference to `credit`, `showLevel` / `showStaffLevel` on the worker, push. |
| `ServerScriptService.SmithyCore` | `crafter.hired[id].credit`, `staff[role].credit` (encode; decode clamps to 0..made / count, nil at 0). |
| `StarterGui.CrewGui.Window.Stats.Panel.LevelUp`, `Staff.Panel.LevelUp`; `EmployeeController` | Copies of `Templates.Card.Price` (TextButton 150 × 40, anchor (1, 0) at (1, -14, 0, 44), ZIndex 3; `Row.Coin` hidden, `Row.Coins` "Lv. N", `Row.Gems` the price). `showLevelUp(panel, id, level)` in `fillStats` / `fillStaff`; `levelTarget[button]`; short of gems → `UiFx.nudge` + `PackOffer.offer("gems", …)`, else `act("level", id)`. Made / Done rows subtract `credit`. |
| `Tests.SaveSpec` | Credit round-trip and clamping (116 checks). |
| `Guide.celebrate` | Waits while `GemGui.GemShop.Visible`. Forge line: `{materialId} {Blueprint.name}`, no "Polished". Polish step below the station's price: `craft(plot, nil)`'s line as "Sell it to afford the Polishing Station". |
| `GemController` | `tourChecked`, `closedWithoutBuy`: `GemTour` "todo" from the first state only if no level is owned and not `toured`; `close` while "open" → "todo" once, then nil; the buy's clearing comes from `apply`. `toggle` forgets a remembered-but-hidden window first. |
| `PolishController` | `polishBonus()` and the Upgrades require at the top; `stations[i].model`; `enablePrompts` skips `Locked` stations; `SCRAPE_VOLUME` from `SoundService.Effects.Polish`'s `Volume` attribute (0.3); the finished hint "+N% value" from the boost. |
| `WeatherController` | Grades' `LookBrightness/Contrast/Saturation/Tint` and the rain's `BaseVolume` attributes, set on first run, read after. |
| `TycoonController` | `buildingAt(at)`: a pad's label needs the pad and you in the same building (or both outdoors). `WorldText.PadLabel.MaxDistance` inf. |
| vault `Development/sim/engine.py` | `wants_polish(s)` (the type polishes, or the open IronTanto letter's Iron Tantō); `letter_sword` needs it polished; `mail_slots` less the open story letter; PolishStation among the tutorial buys. |
| UI review (2026-10-30) | `CrewGui.Window` y +29; `CrewGui.Window.Header.TitleRow` (UIListLayout, Back then Title; EmployeeController reads `Header.TitleRow.Title` / `.Back`); `Shared/Employees` traits shortened; `EmployeeController.WAITING` without "Waiting:"; `MailController.renderTracker` hides while `HotbarGui.BagPanel` is visible; `HotbarGui.BagPanel.Items` cells 84 × 100, centred, padding 2; `Templates.Slot.Stepper.Amount` 22 pt, `Trash.Armed` 28 × 28 at (19, 19); `MailGui.Templates.Track.Words` (+ Face) one line, truncated, ≥ 14; `Templates.Letter.Info.Want` full width, left, truncated; `PolishHud.Panel` Save / Leave at y −16, Value x −16, Leave EdgeArt; `WorkshopOpenGui` DisplayOrder 7, Banner `Outline` stroke; `WorldText.PadLabel.Title` (+ Face) scaled 14–28; `AnvilHud.Bottom` Leave / Finish 22 pt. |
| 10 hits (2026-10-30) | `Shared/BladeData`: every recipe 10 strikes (lengthen 3, taper 3, tip 4); `BladeCore.finishAt` 8; `Tests.ForgeCheckSpec` +6 checks a blade, `BladeGolden` regenerated for the prototype's 7 blades (the prototype's blank and recipes synced; README says not to copy its BladeData over Studio's 24). Vault sim: `timings.FORGE_STRIKES` 12, `engine.task_forge` scales by strikes, `calibrate.py` marks pre-change sessions 12-strike. |

### Mail tracker as a bullet list (2026-10-31)

[[Sessions/2026-10-31#The mail tracker as a bullet list]]

| Where | What |
|---|---|
| `StarterGui.MailGui.Templates.Track` | No background or UICorner; `AutomaticSize` X, height 0.3; UIListLayout (horizontal, centred, 6 px): `Bullet` ("•", a copy of `Words` with its `Face`), then `Words`. `Words` and `Face` TextScaled (14–28), left-aligned, `AutomaticSize` X. |
| `StarterGui.MailGui.Tracker` | `List` `AutomaticSize` X (as wide as its widest row), rows left-aligned, no gap; `Fold` has no background or UICorner. The frame (`SizeConstraint` RelativeYY: 266 × 100 on an 844 × 390 phone, at most 372 × 140) bounds the list's width. |

### Quest ores say who wants them (2026-10-31)

[[Sessions/2026-10-31#Quest ores say who wants them]]

| Where | What |
|---|---|
| `ReplicatedStorage.WorldText.OreLabel` | `Wants.Face` and `New.Face` `Visible` on (they were off, so only the black copy drew). |
| `ForgeService` | `RANK` and `needed(d, m)` moved above `reveal`. `needed` returns the giver of the first open story letter or order naming the metal (an old order: its rarity or rarer), or nil. `reveal` shows `Wants` "<sender> wants this!" from it; `keeping` (Auto-Roll's quest stop) uses it as before. `wantedMetal` is only the pull lean now. |

## Refinements and reviews (2026-10-31)

All built in Edit, not played. Sources: [[Sessions/2026-10-31#Refinements, Allen's new notes and the big review (evening)]] and the handoffs in `Design/Reviews 2026-10-31/`. Deleted today: `StarterGui.PackOfferGui` (pack offers are Roblox's own prompt) and `StarterGui.AutoRollConfig` (now `AutoRollGui.Bar.Config.Drop`).

### Lessons done (2026-10-31)

| Where | What |
|---|---|
| `StarterPlayerScripts.MyPlot` | `lessonsDone(plot)`: `TutorialDone` and the player's `GemTour` nil (the gem step done too). Used by `PackOffer.offer`, `MenuController.updateDot` (+ a `GemTour` listener), `AutoRollController.near`, `WorldStoreController` and the Auto Anvil pill. `tutorialDone(plot)` stays for the Guide's own steps. |

### Auto Anvil (2026-10-31)

[[Sessions/2026-10-31#Auto Anvil]]

| Where | What |
|---|---|
| `Shared/Store.PASSES.AutoAnvil` | Game pass 2058261392, 49 R$; StoreService grants it as `Pass_AutoAnvil` like every `PASSES` key. `StoreService` has an `AutoAnvil` attribute for owning it in Studio (read only with `StudioLocked` off). |
| `StarterGui.AnvilHud.Auto` | The pill (`Icon` 32 px, the pack's Hammer `rbxassetid://99067729549436`; `Switch` 52 × 28 knob). Lock icon `rbxassetid://111896329341217` without the pass. |
| `ServerScriptService.SmithyCore` | `settings.autoAnvil` (decode `== true`) → player attribute `AutoAnvil`; in the `Setting` remote's `SWITCHES`. |
| `StarterPlayerScripts.AnvilController` | `AUTO_BEAT` 0.5 s, `autoAt`, `autoOn()` (pass, switch, `lessonsDone`); each frame in `mode == "ready"` runs the same `strike()` as a tap. L1 switches it; the hammer nods only with `Prefs.motion()`; `refreshAuto` re-runs on `ReduceMotion` changes. |
| `MenuGui.ShopWindow.Content.Body.List.Grid.AutoAnvil` | Its Shop card (LayoutOrder 7, red gradient). |

### Crew levels in the world (2026-10-31)

[[Sessions/2026-10-31#Crew levels in the world (subagent)]] · [[Design/Reviews 2026-10-31/Handoff — UI notes]]

| Where | What |
|---|---|
| `ServerScriptService.EmployeeService` | Each worker NPC carries `Crew` (the id `Employee("level", …)` takes), `Level` and `Progress` (share of the next level's work; nil at Lv. 5), set in `showLevel`. |
| `ReplicatedStorage.WorldText.Tag` | 180 × 74; `Bar` (70 × 8 track, amber `Fill`) under "Lv. N", hidden in the template, shown for your own crew below Lv. 5. |
| `ReplicatedStorage.WorldText.LevelPrompt` | F / gamepad Y, `HoldDuration` 0 (was 0.6), "Lv. N · price gems". |
| `StarterPlayerScripts.EmployeeController` | Last section: the nearest own worker within 8 studs gets `LevelPrompt` (checked 4× a second; gives way to any other prompt on screen); `PromptTriggered` → `openConfirm`. The level-up burst (a copy of `UpgradeFx.padBurst`). `showLevelUp` fills `Row.Next` / `Row.Price`. Every "Lvl." is "Lv.". |
| `StarterGui.CrewGui.Confirm` | Dim + a 460 × 214 window: "Level Up", "<name> to Lv. N?", a green button with the gem icon and price; X, B, Escape close. Short of gems: shake + `PackOffer.offer`; the window stays. |
| `CrewGui.Window.Stats.Panel.LevelUp`, `Staff.Panel.LevelUp` | 170 × 62; `Row` a vertical list: `Row.Next` "Lv. 4 → Lv. 5" (22 pt), `Row.Price` (gem icon, `Gems`). |

### Purchase prompts and passes in the world (2026-10-31)

[[Sessions/2026-10-31#Robux passes you can see in the world (subagent)]] · [[Design/Reviews 2026-10-31/Handoff — UI notes]]

| Where | What |
|---|---|
| `StarterPlayerScripts.PackOffer` | `offer` calls `MarketplaceService:PromptProductPurchase` for `Store.packFor`'s pack (only while on sale), after `MyPlot.lessonsDone`. `StarterGui.PackOfferGui` deleted. Callers unchanged. |
| `Workspace.Plot.WorldStore` | Models `AutoRoller` and `LuckyOre`, each with `WorldStore = <Store key>`, `Locked` and `Owned` parts, an invisible `Anchor` with `WorldStorePrompt` ("Buy", reach 6). `LuckyOre` is the odds sign since 2026-11-01 (the glass case is `ServerStorage.Legacy.WorldStore_LuckyOreCase_1101`): `Board` (posts, `Face` 5.6 × 4.53, `Cap`, `Rail`; shown in every look) with `Face.OddsGui` (SurfaceGui, 75 px/stud, MaxDistance 60: `Body.Title` "Ore Chances", a row per rarity `Body.<Rarity>.Rarity/Now`, `Body.Lucky` with `Title`, `Price.Robux/Amount` and a cell per rarity), a clover on the cap in `Locked` (green) and `Owned` (neon, light, sparkles); the prompt's ObjectText "Lucky Ore". `MoreCoins`' chest removed 2026-11-01 (`ServerStorage.Legacy.WorldStore_MoreCoinsChest_1101`); the pass stays in the Shop. |
| `ReplicatedStorage.WorldText.PassLabel` | "<name> · <Robux icon> <price>", within 22 studs, not through walls. |
| `StarterPlayerScripts.WorldStoreController` | Your spots after `lessonsDone`; visitors see owned ones only; a spot's prompt off while another prompt is in reach; Lucky Ore's sign: `showOdds` fills `OddsGui` 5×/s within 60 studs of the camera with `Materials.odds` of ForgeService's luck (`Upgrades.luck` + the owner's `Store.luckBonus` + `WeatherLuck` once `TutorialDone`), the `Lucky` column (price, chances with +`Store.LUCKY_ORE`) only while you could buy it; no floating label; its prompt buys directly. Where paid random items are restricted only the board shows. (`MenuGui.OpenOdds` removed 2026-11-01.) |
| `Remotes.WorldStore`, `ServerScriptService.WorldStoreLog` | Custom event `WorldStore` (pass key; Shown once a session, Prompted at most every 10 s, Bought from the server's purchase-finished event). |
| Roblox pass and product icons | Set through Open Cloud (`imageFile`), from the icon pack and `Art/Weather Icons`. |

### Shop roofs (2026-10-31)

[[Sessions/2026-10-31#Shop roofs: a low beginner shop, a two-tier upgraded one (subagent)]]

| Where | What |
|---|---|
| `Workspace.Plot.Shop.Starter.Shell` | Front and side tops 11.00, eave 9.11–9.86, ridge 18.46, top 19.45; `Transom` gone; two `GableBase` blocks. Backup `ServerStorage.Legacy.StarterShell_beforeLowerRoof_1031`. |
| `Workspace.Plot.Shop.Upgraded.Shell.Roof.UpperTier` | 58 parts, louvred tier, top 38.45; no query, collide, touch or shadow; flies in last. `build_shops` would rebuild the old roofs. |

### Station views and controllers (2026-10-31)

[[Sessions/2026-10-31#Station views: controllers, glyphs, readable text, comfort, pickers (subagent)]] · [[Design/Reviews 2026-10-31/Handoff — Reduced motion]]

| Where | What |
|---|---|
| `Prefs` | `motion()` (the player's `ReduceMotion`, else Roblox's switch), `shake()` (`motion()` and `Shake` ≠ false), `haptics()` (`Haptics`). Every camera shake and rumble goes through them. |
| `StarterPlayerScripts.PolishController` | Hold R2: `PAD_PASS` 1.2 s a sweep; stick X / D-pad steers; Y saves; Q, Backspace, B leave. Pad hints and ghost glyphs. HUD text 18. |
| `StarterPlayerScripts.AnvilController` | `UiFx.fit` HUD scale; glyphs (R2 strike, B Cancel, Y Finish, L1 Auto); pitch 1.00 → 1.16 over blows 1–9, blow 10 at 0.8 ×1.4 with 60% more sparks. `AnvilHud.Hint` 23 pt. |
| `StarterPlayerScripts.HiltSeat`, etching | `Prefs` for haptics and shake; "[R2] Hold to push the hilt on"; etching's close ring wears B. |
| `ItemPicker.bestFirst` | Letter's shape, then the last-forged blade (session), then the dearest; ingots: letter's metal, then rarest. Toasts `min(6, 1.5 + 0.06 × characters)` s. |
| `StarterPlayerScripts.HudFocus` | `GuiService.TouchControlsEnabled = not hidden` with the HUD; `guideStays`, `watchSpot` keep GuideGui on while SpotlightGui is Enabled. |
| `Hud`, `CoinFly`, `Guide`, `AutoRollController` | Reduced motion: coins add straight to the count / `land()`; the station Highlight holds 0.2; the spotlight jumps (`k = 1`); the icon spins only with motion. `Guide.padSpot`: selects a new spotlit GuiButton once on a gamepad. |

### Settings (2026-10-31)

[[Sessions/2026-10-31#Settings: sections, volumes, comfort switches, music (subagent)]] · [[Design/Reviews 2026-10-31/Handoff — Settings]]

| Where | What |
|---|---|
| `StarterGui.MenuGui.SettingsWindow` | Fixed 416 × 440, `Body` ScrollingFrame; `SoundHeader`, `ScreenHeader`, `PlayHeader`; rows `Music`, `Sound` (+ `Gear`), `Weather`, `Shake`, `ReduceMotion`, `Haptics` (touch or gamepad only), `Tracker`. A row is one TextButton. |
| `StarterGui.MenuGui.VolumeWindow` | 416 × 298; rows `Music`, `Effects`, `Alerts`, each a `Slider` (`Track`, `Fill`, `Knob`), 0–1 in 0.1 steps, saved 0.4 s after the last move. X and B go back to Settings. |
| `SoundService.Alerts` | New SoundGroup; `Effects.Cues.Offer`, `FurnaceReady`, `CartBack` use it (still found under `Effects.Cues`). |
| `SoundService.Music` | Three tracks (Minimal Koto 1846310773, Kioku 1838864669, Aichaku 1838864619), Volume 0.5, not looped; `MenuController` plays them in turn from a random one, 4 s after joining. |
| `StarterPlayerScripts.MenuController` | Music = pill × MusicVolume²; Effects / Alerts = Sound pill × volume². `isOn("ReduceMotion")` follows Roblox's switch while nil. Shop icon still with motion off. `shopDot` kept from the start (no `MenuGui.Buttons` lookup at runtime). Q / Backspace close Shop, Settings, Odds. |
| `ServerScriptService.SmithyCore` | Settings keys → attributes / `Setting` names: `shake` `Shake` (true), `haptics` `Haptics` (true), `reduceMotion` `ReduceMotion` (nil), `tracker` `Tracker` (true), `cartPin` `CartPin` (false), `musicVolume` `MusicVolume` (0.7), `effectsVolume` `EffectsVolume` (1), `alertsVolume` `AlertsVolume` (1), `autoAnvil` `AutoAnvil` (false). `SmithyCore.volume(v, default)` clamps 0–1, rounds to 0.1, refuses non-finite. Encode `table.clone(d.settings)`. |
| `MailController`, `DeliveryController`, `UiFx.open` | The tracker fold follows `Tracker`; Pin follows `CartPin`; windows open in place with motion off. |
| `ServerStorage.Legacy` | `SettingsWindow_beforeSections`, `MenuController_beforeSections`. |

### Upgrade chains (2026-10-31)

[[Design/Reviews 2026-10-31/Handoff — Upgrade progression]]

| Where | What |
|---|---|
| `ReplicatedStorage.Shared.Upgrades` | After `byId`: `Upgrades.CHAINS` (Ore, IngotRack, SwordRack, Heat, Furnace2, F3Heat, Strikes, Polish, Crafters, Etcher, Shop, Parking), `Upgrades.chainOf(id)`, `Upgrades.chainStarted(plot, u)` (a chain with one upgrade bought; a merge starts the Ore chain). `Furnace2.after` Heat1. No `after` on SwordRack2 (Katana), Anvil4 (Stocker), Claymore (Rapier), RickshawBay2 (Longsword), RickshawBay3 (Falchion), Etcher (Gladius). |
| `ServerScriptService.TycoonService` | `standing(plot)`: blueprints, `PAD_ALWAYS` and `Upgrades.chainStarted` stand; `PAD_CAP` 3 picks among new chains. `PAD_ALWAYS` { Delivery, Anvil2 }. No sword pad until `TutorialDone` (refresh on it per plot). Header comment describes the chains. |
| `Workspace.Plot.Pads` | Ore Slot 2–6 and Merge (−9, 9); Heating I–III (−25, 36), Furnace 2's (−25, 44), Furnace 3's (−25, 52); Sword Crafter (−4.3, 57.5); Zanbatō / Claymore / Flamberge (−12.5, 55); Stocker (23.5, −9.5). |
| `ReplicatedStorage.PadParts.Base` | Charcoal (58, 54, 54). |
| `ServerStorage.Tests.SaveSpec`, `ServerStorage.Builders.ExportBalance` | Furnace 2 after Heating I; chain checks. `B.chains` exported. SaveSpec checks `mailGap(0) == 300` ("5:00"); 123/123. |
| vault `Development/sim` | `rules.Balance.chain_of`; `engine.offers` keeps begun chains past the cap; scenarios `cap1`–`cap5` cap only new chains; `test_begun_chains_stand_past_the_cap`. |

### Customers and values (2026-10-31)

[[Design/Reviews 2026-10-31/Handoff — Customers and values]]

| Where | What |
|---|---|
| `ServerScriptService.ShopService` | `freeSword` (chosen inside), `BROWSE_WAIT` 8, `browseFor` (was `browseEmpty`), `goTo`, `walkOut`, `FADE` / `fade` (1.2 s), each `sendCustomer` ctx's once-only `free()` (the cap counts only shoppers); rickshaw riders can browse. `RAMP_SECS, RAMP_SALES = 300, 5`. The first sale's unanswered card re-asks with 45 s. `offerCommission` passes the plot's `Bought_` attributes; a `Bought_MacheteBlueprint` listener per plot. `refillOrders` passes the last giver as `avoid`. |
| `ReplicatedStorage.Shared.Customers` | `LINES.wait` ("I'll wait my turn."). |
| `StarterPlayerScripts.AnvilController` | Shape chip `ValueFormula.value(basePrice, AnvilScore.MAX_MULTIPLIER, hilt bonus + seat bonus, metal)`; requires `AnvilScore`, `Hilts`, `ValueFormula`; `completed` from the smith state. `TestAnvil` keeps the old chip. |
| `ServerScriptService.ForgeService` | `showWants(stand, d, material)` above `reveal`; a 1 s loop over every roller's stands; a stale giver shows no line. |
| `Workspace.Plot.DeliveryBay.DeliveryBoard.Panel` | Plot (26.84, 3.36, −24) on the board's papers; `Status.StudsOffset` 3.8. `build_delivery` builds the board at z −24 with the Panel on the papers (`mesh.Size.Y / 2 + 0.5`, −0.44) and Status at 3.8. |
| `Workspace.Plot.Workshop.Shell.NavKeep` (×2) | 1.6 × 3.6 × 1.6 invisible, no collision, PathfindingModifier `Avoid`, round the back doorway's posts (x −13, −3.2); move with the shell. |
| `InspectPoint2`, `InspectPoint3` | Beside each holder's `InspectPoint`, 2 studs apart along its face; `Slot2` / `Slot3` `Inspect` point to them. Big Sword Stand unchanged. |
| Both shops' `Kanban.SurfaceGui.TextLabel` | GothamSSm Heavy, 3 px `UIStroke` (18, 12, 8). |

### Tutorial fixes (2026-10-31)

[[Design/Reviews 2026-10-31/Handoff — Tutorial fixes]]

| Where | What |
|---|---|
| `StarterPlayerScripts.Guide` | `craft` no-letter branch: `offerUp` ("A customer is coming!" → "Accept the offer!" on the customer); `holders` returns the holder. `computeWay` / `walkway`: PathfindingService corners from the target back, recomputed when 6 studs off (≤ every 0.75 s), ending 4 studs from the target in sight (`MyPlot.blocked`); straight line as fallback. `furnaces(plot, fits)`; "Black Iron isn't Iron. Pull again"; "Hold to pull the lever"; "Open Upgrades" when the Gem Shop is off screen. |
| `ServerScriptService.ForgeService` | ForgePut: 3 s heats while `completed == 0 or not TutorialDone`. `SmithyCore.onRejoin` reset clears `tutorialPulls`, `wantPulls`. |
| `StarterPlayerScripts.Hotbar` | `trashOn`: card and corner trash hidden until `TutorialDone`. |
| `StarterPlayerScripts.GemController` | The join task's daily window waits for the Gem Shop to shut, then the cheer, then 1 s. D-pad left passes while anything is selected; Q / Backspace close. |
| `ReplicatedStorage.Shared.Commissions` | Katana `afterUpgrade = "MacheteBlueprint"`; `due(statuses, sold, bought?)`. |
| `ReplicatedStorage.Shared.GemUpgrades`, `.Orders` | `MAIL_GAP` {300, 250, 210, 175, 150, 125}; `Orders.make` takes `ctx.avoid`. |
| `StarterPlayerScripts.MailController` | `showPopup` counts down only while `popupShown`; held while the bag is open; `twoLines` (a break before the blade's name); `MailPad` (D-pad down opens mail). |
| `ReplicatedStorage.WorldText.PadLabel` | 260 × 64, `Title` and `Price`. The blueprint pads' coins ÷ price bar (`Fill`, `TycoonController.showSaving`) was removed 2026-11-01 (Allen: "its unnecessary"; old label `ServerStorage.Legacy.PadLabel_beforeNoSavingBar_1101`). |
| `StarterGui.WorkshopOpenGui.Banner` | Top centre (0.5, 8, anchor 0.5, 0); its UIStroke fades with the text. |
| `DevTools` | Skip tutorial marks only the first letter done (+120 coins, +5 gems, sold ≥ 1, completed ≥ 2). |
| `ServerStorage.Builders.ExportBalance` | `shop.firstLetterDelay`, `rampSecs`, `rampSales`, commissions' `afterUpgrade`. |

### UI notes and review fixes (2026-10-31)

[[Design/Reviews 2026-10-31/Handoff — UI notes]] · [[Design/Reviews 2026-10-31/Handoff — UI review fixes]]

| Where | What |
|---|---|
| `StarterGui.MailGui.Templates.Track`, `Tracker.List` | `Bullet`, `Words` (+ Faces) fixed 18 pt, no TextScaled, sized to their text; 4 px between rows. Supersedes the morning's scaled rows. |
| `ReplicatedStorage.WorldText.Prompt.Button`, `PromptStyle` | Centred at (0.5, 30); `Grow` (UIScale) 1.5× while held; `Ring` (gold 5 px, `Progress` gradient, Offset 0.5 → −0.5) fills over the hold; ±3° rock with motion. On a gamepad `Tap` shows `GetImageForKeyCode`. |
| `StarterGui.AutoRollGui.Bar.Config` | `Arrow` (the "›" turned down/up) and `Drop` (276 wide, 8 px under the bar: "Stop at rarity" < > and "Stop at quest ores" pill). Closes from the arrow, B, Escape or walking away. `AutoRollConfig` deleted. |
| `UiFx` | `topbarIcon` destroys a same-named icon first and finds `MenuGui.Buttons` in `HudHold`; `PlayerGui.SelectionImageObject` a clone of `StarterGui.SelectionGui.Edge` (3 px amber, corner 10); `open` / `close` restore the gamepad selection (`openers`, `onScreen`, `GuiService`); `onGamepad()` used by Mail, Gem, Menu, Collection, Delivery. |
| `DevPanel` | Reset keeps PlayerGui screens named `Topbar*`. |
| `StarterGui.SelectionGui` | Disabled; holds `Edge`. |
| Windows (`OddsWindow`, `GemGui.DailyReward`, `GemGui.GemShop`, `MailGui.Window`) | `Pattern` (Z 2) and `Tint` (Z 3) as window children, `EdgeArt` in `Tint`, `Content` Z 5. Every window `Close` a clear 64 × 64 button with `Close.Art` (+ `Glyph`); Mail's and Crew's `TitleRow.Back` 64 × 64. |
| HUD and cards | `MenuGui.Buttons` `UIPadding.PaddingLeft` 0.115, Labels 2.05 × wide, MinTextSize 14; `GemGui.Templates.Upgrade` 84 tall; `MailGui…Header.ActiveOnly.Switch` knob pill; `DeliveryGui.PinnedOrder.Row.Label.Face`; `GuideGui.Goal` UIStroke 2 px; `WeatherGui.Icon.Tip` 3.2 ×; `OreLabel.Wants` without `Face`, cream text and a 1.5 px UIStroke. |
| `CollectionController`, `DeliveryController` | D-pad right passes while anything is selected; Q / Backspace close. |

### Village fixes (2026-10-31)

[[Design/Reviews 2026-10-31/Handoff — Village fixes]]

| Where | What |
|---|---|
| `Workspace.Village.ArrivalSpawn` | SpawnLocation (640, 0.11, −200), 10 × 0.3 × 5.7, Neutral, invisible, no collide / query / touch, Duration 0. |
| `ServerScriptService.PlotService` | `claim` sets `RespawnLocation = arrival` before `waitLoaded`, then the plot's spawn; a thread `RequestStreamAroundAsync` then `PivotTo` home (skipped if the character changed). Empty copies keep the `PlotLeaderboard` tag. `NAMEPLATE_AT` (0, 47, −33). |
| `ServerStorage.Legacy.WorkspaceDrafts_2026_10_31` | 20 items with `FromWorkspace = true` (A2_Zones … Z_E_Line, the x-2000 copy and its `Ground`, `GreatSwordRig`, `Sword Animations`, two empty folders with `FromPath`). `Smithy` stays in Workspace (`Shared.BladeProbe:60`). |
| `Lighting.Atmosphere`, `ColorCorrection` | Haze 0.7, Decay 178/160/150, Color 216/222/230; Saturation 0.15 (Sunshine 0.08, Rainbow 0.12). Mountain `Grass` blocks lifted, old colour in `ColorBefore_20261031`. |
| `StarterPlayerScripts.WeatherController` | `LIGHT` per weather (Brightness, Ambient, OutdoorAmbient, Atmosphere, `Terrain.Clouds`), base values in `Base<Property>` attributes; `drawn` starts false. `Workspace.Terrain.Clouds` new (Cover 0). |
| `Village.Landmarks.GateDoors`, `Village.Walls.LaneExitN` / `LaneExitS`, `Village.Walls.WallGuards` | Gate leaves; the lane exits walled; six invisible collide-only guards over the wall (y 6.6–24). |
| `Village.Atmosphere.Backdrop.Mountains` | A Model, `ModelStreamingMode` Persistent. |
| Street | 290 parts `CastShadow` off; `Street.Walkway` Slate; the 12 lamps 3 studs out (`MovedFromX`); chochin SmoothPlastic; Torii Wood. |

### Performance fixes (2026-10-31)

[[Design/Reviews 2026-10-31/Handoff — Performance fixes]] · [[Design/Reviews 2026-10-31/Handoff — Cart and rickshaw welds]]

| Where | What |
|---|---|
| `StarterPlayerScripts.Hotbar.drawArt` | One rim viewport (8 nudged copies) behind the item, `RIM_FOV`: 2 ViewportFrames a slot (was 9). |
| `StarterPlayerScripts.SwordRenderer` | `Prop = true` swords draw only with no `Locked` ancestor; world etches one at a time (`etchTurn` / `etchDone`), pcall'd; `rendered` weak-keyed. Props' `Etch` ids `FallingStars`, `WovenWind`. |
| `OreBoxAnimator`, `OreBoxShow` | Other plots' rolls play only within `RANGE` 120 (`far` starts mid-roll); camera punch on `Prefs.shake()`, rumble on `Prefs.haptics()`. |
| `StarterPlayerScripts.ShopController.bindSlot` | Own holders only (`MyPlot.owns`); `bound[part]`; one `Plot` attribute handler. |
| `ServerScriptService.ForgeService` (glow), `StarterPlayerScripts.ForgeGlow` | Slot parts tagged `ForgeSlot`; `glow(slot, from)` sets `HeatFrom`, `HeatStart`, `HeatEnd` (server time) once per heat, `clearSlot` clears them; the 10 Hz loop only runs `refreshBoard`. ForgeGlow tweens each slot (colour → HOT, light 0 → 2). |
| `StarterPlayerScripts.TycoonController` | Weak `watchedItems` / `watchedSlots` guards in `watchItem` / `watchSlot`. |
| `ServerStorage.Rickshaw`, `ServerScriptService.Rickshaws` | Body WeldConstraint'ed to `Root` (only anchored part); `WheelTurn` Weld on Root to the first `Hub`; `place` one `PivotTo` + `turn.C0 = turn * REST`; `paint` writes only changes. |
| `ServerScriptService.DeliveryService` | `rig(c, on)`: while out, the cart is welded to its `Bed` (Wheels by `Weld` C0); at home re-anchored, joints gone, parts `BulkMoveTo`'d back; `set` spins wheels through `weld.C0`; `paint` writes only changes. |

## Untitled 3 and named customers (2026-11-01)

| Where | What |
|---|---|
| `ServerScriptService.CastRigs` | `build(name)`: an R15 rig dressed from `ServerStorage.Cast.<name>` (cached per name, cloned); `dress(rig, name)`: clothes, face, accessories (own `AccessoryWeld`), loose parts by where they sit; nothing held. |
| `ServerStorage.Cast` | The 13 toolbox characters, scripts stripped. |
| `Shared.Customers` | `cast` (9 clients with `likesBlueprint`, 3 VIPs, each `model` + `lines`), `CAST_CHANCE` 0.1, `CAST_VIP_SHARE` 0.5; `pick(rng, vipChance, wants)`; `line(key, fill, rng, c)`, `remark(..., c)`. |
| `ShopService` | `makeNpc` → `CastRigs.build` for `c.model`; `runCustomer` `wants` (their blueprint on a free display), `greet` on entry. |
| `EmployeeService` (looks) | Crafters: plain rig in their skin + `CastRigs.dress(npc, "Swordsmith")`. |
| `Shared.Employees.levelGems(level, done)` | The scaled crew level price (server, crew page, confirm, world prompt). |
| `WorldText.LevelPromptGui`, `LevelPrompt` (Style Custom) | The crew Level Up key: green square, "Lv. a › Lv. b", gem icon + price (`EmployeeController.drawLevel`/`hideLevel`). |
| `CrewGui.Confirm.Window` | 340×202. `CrewGui.Templates.Card` attributes `Fill1/2/3`. |
| `AutoRollGui.Bar` | Pill-sized; `Config` tab under it (`Config.Tab`, `Config.Drop`); `Button.Switch` TextButton + `Hit` toggles. |
| `ItemPicker.makeCard` | "… N coins" chips → `Chip.Lead` + coin icon + number. |
| `WorldStore.LuckyOre.Body.Table` | `Rows` (Spacer + six rows) and `Lucky` columns; `WorldStoreController.showOdds`. |
| `Shared.Upgrades` `effect` | Optional pad line (Bays); `WorldText.PadLabel.Effect`, `BuyButton.Label.Effect`. |
| `NpcWalk` | `room`/`clear` stand points, `route`/`leg` turn points with 1.5 studs of room, `follow` reach within 1.5 studs. |
| `Shared.Orders` | `SHOP`, `SHOP_STEP` 0.1, `shopBoost(upgrades)`; `pay(value, metalMult, typical, boost)`. ShopService `shopBoost(d.upgrades)`, MailController from `Bought_*`. |
| `ServerStorage.Cast.Swordsmith` | No gasa; accessories `Mask`, `Hair`. |
| `CastRigs.dress(rig, name, skip)` | Skips accessories by name; keeps the rig's own. |
| `Shared.Employees` look `mask`, `ownHair`, `body` | Crafter variety; `MUSCLES` body part ids for Rin. `EmployeeService.dress(look, outfit, crafter)`, `pose(npc)`. |
| `Development/sim` | `rules.order_pay(…, boost)`, `shop_boost`; `pick_customer` rolls named VIPs. |
| `WorldText.PassLabel` | `Title` over `PriceRow` (`Robux`, `Price`); WorldStoreController shows it within the prompt's reach. |
| `ServerStorage.Cast.Swordsmith` `Belt`, `BeltKnot` | Deleted 2026-11-01 (Taru wears the Swordsmith's pants instead). |
| `NpcWalk.smooth(from, points)` | Leaves out skippable route points (line room ≥ tightest skipped point, no wall). |
| `Shared.Materials` `ingotAlpha` | An ingot's see-through (Air 0.3); `dressIngot` sets it on shown parts only. |
| `HotbarGui.BagPanel.Tabs` | All / Swords / Ores; `Hotbar` `filter` hides other kinds' bag cards. `BAG_COLS` 7. |
| `WorldStoreController` `spot.lit` | Auto Ore Roller lamp: `Owned.Lamp` on while `AutoRoll`, else `Locked.Lamp`. |
| `Displays.BigSwordStand2`, `BigSwordStand3` | Side-wall big sword stands (Upgrades, Shop chain, `Orders.SHOP`). |
| `Shared.Employees` look `hakama` | Layered pants asset id (Taru); `EmployeeService.dress` adds it to the HumanoidDescription. |

| `ServerScriptService.ForgeService` | 2026-11-01: `BEGINNER_LUCK` (3) and `rolledRare(d)`: `rollFor` adds it once `TutorialDone` while `d.rolled` holds no Rare+ metal. Mirrored in `Development/sim/engine.py` (`rolled_rare`). |
| `ServerScriptService.ForgeService` | 2026-11-01: `BEGINNER_LUCK` 3 → 9 (sim `engine.py` too). |
| `StarterPlayerScripts.AutoRollController` | 2026-11-01: `Bar.Config.Tab` gone; the chevron stays at Rotation 90 and swaps Text (› closed, ‹ open). |
| `Workspace.Village.Atmosphere.Backdrop.Mountains` | 2026-11-01: 16 low poly ranges (clones of `ServerStorage.MountainRanges.MountainRangeA/B/C`, Blender source `Models/Mountains/`), Persistent, non-colliding. Old boxes in `ServerStorage.Legacy.Mountains_boxes_2026-11-01`. Baseplate centred at (654, -8, -200). |
| `Workspace.Village.Atmosphere.Backdrop.Mountains` | 2026-11-01 (later): 75 block mountains (hills 1 Part, rock 2–3 stacked Parts, snow top block on tall ones; 134 parts; Dark stone grey, snow white), three rows around a rectangle 30 studs past the play bounds; generator `Models/Mountains/part_mountains.luau`. Blender ranges and pyramids in `ServerStorage.Legacy.Mountains_blender_2026-11-01` / `Mountains_pyramids_2026-11-01`. Supersedes the row above. |
| `Workspace.Village.Street.StreetLights` | 2026-11-01: 16 clones of Allen's StreetLights model (Atomic), at both ends of each walkway segment, both sides, lights range 18 / 1.6 warm; `StreetFill` sheet with a downward SurfaceLight (0.9) gate to gate; original in `ServerStorage.Legacy.StreetLights_original_20261101`. |
| `Workspace.Plot.Parking.Bay1..3` | 2026-11-01: no Post/Sign; Cobblestone `Slab`, 4 `Kerb`, 2 `Bollard` + `BollardCap` (all non-colliding); `Models/Village/build_parking.luau` matches. |
| `Workspace.Village.Landmarks` (east end) | 2026-11-01: the west gate copied to x 888 (turned 180° about (664, -200)); shrine, torii, lanterns in `ServerStorage.Legacy.Shrine_removed_20261101`; Plaza x 840..892. `Walls` at x 888 split into two runs round the opening. The builders (`build_street`, `build_town`, `build_simple`) still describe the shrine. |
| `ReplicatedStorage.Shared.DayNight` | 2026-11-01 (new): `DAY` 900, `NIGHT` 300; `clock(t)`, `night(clock)`, `now()` (adds `ReplicatedStorage.ClockOffset`). |
| `StarterPlayerScripts.DayNightController` | 2026-11-01 (new): sets `Lighting.ClockTime`, fades `Lighting.NightGrade` to its Night* attributes, toggles `NightLight`-tagged lights at night > 0.3. |
| `StarterPlayerScripts.WeatherController` | 2026-11-01: `paintLight` replaces the Lighting/Atmosphere/Clouds tweens: weather layer faded by hand (3 s Sine), then blended toward `NIGHT` by `DayNight.night()`. |
| `Workspace.Plot.NightLights` | 2026-11-01: `Fill`, an invisible 84 × 92 sheet 24 studs over the workshop yard with a downward SurfaceLight (range 40, angle 90, 1.2, warm), tagged `NightLight`, off by day (the corner lamps were removed: Allen wanted even light). |
| `DevPanel` / `DevTools` / `Remotes.DevTime` | 2026-11-01: Studio-only "Day / night" button: `ClockOffset` set so the clock jumps to 19:30 (from day) or 8:00 (from night). |
| `ServerStorage.Builders.build_yoshiwara` / `Workspace.YoshiwaraPreview` | 2026-11-01 (new): builds the preview copy at z +2000 (Village, Plot, Baseplate copies stripped of gameplay; `Yoshiwara` folder: Machiya, Median, LanternStrings, Omon, Tower, Rooftops). Preview only: delete before publishing. |
| `StarterPlayerScripts.DayNightController` (NightGlow) | 2026-11-01: parts tagged `NightGlow` go Neon in `GlowColor` at night, SmoothPlastic `DayColor` by day; applied on each change and on stream-in. |
| `ServerStorage.Builders.build_spaced_lots` / `Workspace.SpacedPreview` | 2026-11-01 (new): preview copy at z +2000: outer lots moved 28 out, `Village.GapHouses` (12 copies of the end/outer houses), plot copies on N1–N3. `YoshiwaraPreview` deleted (builder kept). Preview only: delete before publishing. |
| `Workspace.SpacedPreview` / `YoshiwaraPreview` | 2026-11-01: both deleted (Allen kept the current village); their builders stay in `ServerStorage.Builders`, unused. |
| `EtchingTableController` / `EtchHud.Hold` / `EtchService` | 2026-11-01: hold to etch: the drawing runs only while E, R2, A, a finger or the mouse is held; the etch is requested when it completes (leaving early leaves the sword as it was). `Store.owns(player, "AutoEtch")` draws by itself. EtchService refuses a pattern you don't own. [[Sessions/2026-11-01#Hold to etch, three coin etches]] |
| `Shared/Etches` / `Shared/Upgrades` (CHAINS.Etches) | 2026-11-01: Flame +15%, Woven Wind +20%, Fracture +25% on one pad chain after the Etching Table (800 / 8,000 / 40,000, saved as `Bought_<id>`); the other four have `retired = true` (still draw, never offered). `Etches.owned/owns/best/chosen` take a plot or `SmithData.upgrades`; SmithyCore's publicState has `etchValues`; the Sword Etcher uses `chosen`. |
| `Shared/Store` / `StoreService` / `MenuController` | 2026-11-01: the Starter Pack is a developer product (3727025192; ProcessReceipt grants it and sets `starterGranted`, mirrored as `Pass_StarterPack`); `AutoEtch` (2064189929) and `AutomationPack` (2064634324) passes, `Store.owns` counts the pack as the three autos; Best Value tags picked from live prices. [[Sessions/2026-11-01#Starter Pack as a product, Auto Etch, Automation Pack]] |
| `Shared/Employees` / `CastRigs.dress` / `Shared/Senders` / `DeliveryService.makeCourier` | 2026-11-01: each crafter has an outfit over the Swordsmith rig; the cart courier is Riku's look (`ReplicatedStorage.Senders.courier`). [[Sessions/2026-11-01#Crafter outfits, the courier dressed up]] |
| `Shared/Store` (`DECOYS`) / `rules.py` `pack_for` / `ExportBalance` (`store.decoys`) | 2026-11-02: `packFor` skips decoy packs (Gems200, 399 R$ on Roblox); the sim mirrors it. |
| `SmithyCore` settings `autoEtch` / `Remotes.Setting` "AutoEtch" / player attribute `AutoEtch` | 2026-11-02: the Auto Etch's switch, saved, off by default (`SaveSpec` checks it). |
| `StarterGui.EtchHud.Auto` / `EtchingTableController` | 2026-11-02: a copy of `AnvilHud.Auto` (Blue Pencil icon) beside `Hold`, at (0.5, 93, 1, -30); `refreshAuto`, `toggleAuto`, L1 bound as `AutoEtching` during the show; the drawing runs by itself while `autoEtch`. |
| `Remotes.DevPasses` / `DevTools` / `DevPanel` | 2026-11-02: Studio-only "Passes: on/off": drops every `Pass_*` (and Swift Boots' speed) and gives back what it dropped; `DevNoPasses` on the player. |
| `Workspace.Plot.Shop.Displays.Showcase1..3` / `Plot.Pads.Showcase1..3` | 2026-11-02 (new): copies of `BigSwordStand` at plot (-29 / -33 / -37, -0.40, -49.5) on the street paving, `PointLight` `ShowcaseLight` on `Slot1`; `Slot1` has `Showcase` and `AnySword` (no `BigSword`, no `ViaAisle`). `Upgrade` Showcase1..3; `Shared/Upgrades` `CHAINS.Showcase`. |
| `Shared/Blueprints.fits` | 2026-11-02: an `AnySword` holder takes any blueprint. |
| `ShopService` (`showcasePull`, `SHOWCASE_PULL`, `SHOWCASE_RARE`) / `Guide.holders` | 2026-11-02: `Showcase` holders are skipped by `freeSword`, `browseFor`, named clients' `wants`, the Stocker's `reserve` and the guide; the walk-in gap × (1 − pull). Sim: `engine.py on_spawn`; `ExportBalance` leaves them out of `layout.holders` and exports the pull. |
| `Shared/Upgrades` (`with`, `Crafter`, `Anvil2`, `CHAINS.Crafters`) / `TycoonService` (`BuyUpgrade`, `PAD_ALWAYS`) / `ExportBalance` / sim `engine.py` | 2026-11-02: the Sword Crafter costs 2,000, waits only for the Ingot Rack and Sword Rack, and brings Anvil 2 (`with = { "Anvil2" }`). `BuyUpgrade` sets each `with` id's `Bought_` and save flag before the upgrade's own, then steps players out of both. Anvil 2 has no pad that can stand (price 0, after the Crafter), so `Bought_Anvil2` and every crew check work as before. `PAD_ALWAYS` holds `Crafter` instead of `Anvil2`. The export carries `with`; the sim owns it on the buy. Backups: `ServerStorage.Legacy.<Name>_beforeCrafter15_1102` (Upgrades, TycoonService, ExportBalance). |
| `Shared/Upgrades` (`OreStand2`, `WallRack2`, `price`, `DisplayTable2`, `UpgradedStore`, `DisplayTable5`) / `SaveSpec` / sim `rules.py` | 2026-11-02: every price ends in 0: Ore Slot 2 80, Wall Sword Rack 2 110, `price` rounds merged Ore Slots to the nearest 10 (sim mirrors it; SaveSpec checks 0–5 merges). Display Table 2 after Table 1; the Upgraded Store after Wall Rack 2, Table 1, the Back Wall Rack and Table 2; Table 5 after Table 4 and the store. Backup `Upgrades_beforeEnhancements_1102`. |
| `ReplicatedStorage.WorldText.PadLabel` | 2026-11-02: sized in studs (9 × 2.8) so it shrinks as the camera pulls back; rows in scale, capped by `UISizeConstraint` at their old pixel heights (32 / 24 / 32); text `TextScaled` with `UITextSizeConstraint` (max 28 / 20, min 1); outlines stay fixed pixels, which `TextLayers` sizes to the text (a ScaledSize stroke there draws as a blob). Backup `ServerStorage.Legacy.PadLabel_beforeEnhancements_1102`. |
| `StarterGui.WeatherBannerGui` (new) / `WeatherController` | 2026-11-02: a copy of `WorkshopOpenGui.Banner` (the vignette bar); on a `Weather` change after the tutorial it shows "[Weather] bonus" from `WeatherGui.Icon.Tip`'s attributes for 4 s with the cheer's pop and fade. Not on join, not over a station's camera. |
| `StarterPlayerScripts.HeldLabel` (new) / `WorldText.HeldLabel` (new) | 2026-11-02: a copy of the pad label (rows Title, Metal, Grade) in `PlayerGui`, adorning your Head (StudsOffset 2.8) while you hold a sword (blade, metal in its rarity colour, grade) or an ingot (name, rarity). Local only; off over a station's camera. |
| `ShopService` (`fade`, `walkOut`) / `ShopController` / `Rickshaws.leave` | 2026-11-02: a leaving customer's speech bubble fades with the body, the NPC is tagged `FadeOut` (seconds in the attribute) so `ShopController` fades the bought sword's parts by `LocalTransparencyModifier` (the client-drawn blade too), and `walkOut` destroys the NPC once faded. Riders track their bought sword when they leave. Backups `*_beforeLinger_1102`. |
| `Workspace.Plot.Smithy.SwordRack.NavBlock` / `SwordRack2.NavBlock` (new) | 2026-11-02: invisible, CanCollide off, CanQuery on, `PathfindingModifier` "Avoid", over each rack's posts and across the 1-stud gap between the racks, so the Stocker's path goes round them. Locked with Sword Rack 2 while it isn't bought. |
| `UpgradeFx` / `Analytics` / `WeatherController` | 2026-11-02 review fixes: `UpgradeFx` skips ids bought `with` another (no burst at Anvil 2's empty pad); `Analytics.STAGES` has the Sword Crafter before the Longsword; the weather banner cancels a fade still running when the next weather comes. Backups `*_beforeReviewFixes_1102`. |
| `ForgeService` (`ForgePut`, `ForgeTake`) / `EmployeeService` (crafter furnace pick, `YOURS`) / sim `engine.py` (`used_at`, `YOURS`) | 2026-11-02: your put and take stamp the furnace's `PlayerUsedAt` (os.clock); a crafter skips any furnace you used in the last 30 s, and the forgotten-ingot pick too. Backups `*_beforeIdleFurnace_1102`. |

## Audit fixes (2026-11-02)

From [[Sessions/2026-11-02#Audit and its fixes]]. Backups `ServerStorage.Legacy.<Name>_beforeAudit_1102`.

| Area | Change |
| --- | --- |
| `ServerStorage.Legacy` / `ServerStorage` strays | 2026-11-02: the 352 old backups (95,374 instances, 60,079 script lines) plus `UIMegaPack`, two `EtchPatterns`, two `ModuleScript` (old NpcWalk) and `AnvilController_Backup` exported as `.rbxm` to `Archive/Studio Backups/` (git-ignored; each read back and matched before deletion) and deleted. ServerStorage 99,241 → 3,661 instances; the place 153,922 → 54,315 script lines. `Legacy` stays for new backups, with `SharedV1` (AnvilSelfCheck). Restore: Insert from File. |
| `DeliveryService` (`dropRefill`) | 2026-11-02: cancelling the active or queued order counts as a skip: the newest offer (the one its accept refilled) becomes a `SKIP_WAIT` wait, so offers + waits stay at `Deliveries.OFFERS` (no wait is added when every slot already waits). Accept then cancel no longer re-rolls offers for free. |
| `RackService` (`handBack`) | 2026-11-02: after `showSwords`, a sword with no hook (a big one with no two side by side free: the crew racks by the hook count; a save with more than the rack holds) goes back to the owner's hands, from `Hook_RackChanged` and the claim. It used to stay on the rack unseen. |
| `LeaderboardService` | 2026-11-02: the final write runs in `SmithyCore.onLeave` (totals read before SmithyCore drops the data; a `PlayerRemoving` handler could read nil), in the background; `BindToClose` writes whoever is still here once and waits up to 20 s for `pending` writes. `onRejoin` clears the written flag after Reset progress. |
| `LeverAnimator` / `Friends` | 2026-11-02: `autoSwing[plot]` dropped on `PlotService.onRelease`; a leaving player's friend list is dropped and the looks cache starts over past `LOOKS_KEPT` = 300 (expired `bad` entries go with it). |
| `SmithService` (`atAnvil`) | 2026-11-02: `BeginForge` and `FinishBlade` refuse unless you're within `REACH` = 12 studs of a bought anvil's `Face` on your plot (`Anvil`, or `Anvil2`-`4`, which you can forge at while no crafter has them; their ForgePrompts reach 8; you stand frozen there while forging). |
| `EtchingTableController` | 2026-11-02: `enablePrompts` keeps a `Locked` table's prompt off (as PolishController): no "Etch" over an unbought Table 2. |
| `AnvilController` (`hideBody`) | 2026-11-02: while forging, the body is hidden each frame from a list made at each forge's first frame (kept up by `DescendantAdded` only while forging), not a `GetDescendants` walk every frame; leaving shows the list again and forgets it, so a tool equipped since is never left hidden. |
| `WorldStoreController` | 2026-11-02: `spot.want` also needs `near`, so the frame loop's `crowdedAt` (every prompt in the world) only runs beside a store spot. |
| `EmployeeController` (`pageSig`, `shownSig`, `refreshXp`) / `MailController` (`mailSig`, `paid`) / `DeliveryController` (`offerSig`, `boosted`, `payText`) | 2026-11-02: a push redraws an open Crew roster or station page, the Mail list or the delivery offers only when what the page shows changed; XP bars and the offers' "~" pay update in place, portraits stay (`portrait` keeps a drawn rig). Coin previews (orders, story rewards, offers, packing cards, the strip's total and "Back!") include `Store.coinBoost`, as `SmithyCore.earnCoins` pays. A Mail row's Send looks its letter up again. |
| `Workspace.Plot.Smithy.Anvil` / `Forge` | 2026-11-02: `ModelStreamingMode` Persistent (AnvilController waits on both with no timeout). |
| `PlaytestLog` / `Builders.ExportBalance` / `Builders.bake_sword_meshes` | 2026-11-02: send `X-Studio: 1`; `Development/sim/receive.py` and `Development/sword_mesh_bake.py` refuse requests without it or with another Host (403), receive.py checks the JSON, the bake helper checks the op id. The tanto-forge preview moved to 8766 on 127.0.0.1 (`.claude/launch.json`, `package.json`), off receive.py's 8765. |
| `Builders.build_atmosphere` (and `Models/Village/build_atmosphere.luau`) | 2026-11-02: no `Terrain:Clear()`; it leaves the Terrain alone. |
| `Tests.SaveSpec` | 2026-11-02: odds add up to 100 with none negative at luck 1-100, Common keeps 10%, 20,000 rolls land within 1.5 points of the shown odds (luck 1, 10), `Orders.pay` lift and shop boost, `shopBoost`, `typicalMetal`. 142/142. Run it against a renamed copy of Shared (see the session note): a plain clone still requires the cached originals. |
| sim `engine.py` (`buy`) / `time_prices.json` / `upgrade_tree/build_tree.py` | 2026-11-02: the Katana-letter and AllPads checks run after the upgrade (and its `with` ids, now marked) is owned; Crafter 2,000 in `time_prices.json`; the 6-roots assert is gone. [[Development/Sim Runs/audit-fixes-2026-11-02]] |
| `RackController` | 2026-11-02 (second audit): a click takes a rack item at once; a finger only on a tap (`UserInputService.TouchTapInWorld`), so a camera swipe or pinch that starts on an item no longer takes it. `takeAt(x, y)` holds the hit test. |
| `PromptFilter` / `SwordRenderer` / `ItemPicker` | 2026-11-02 (second audit), for the Dev Panel's Reset progress (it re-copies the player scripts): a prompt switched out of reach keeps its reach in the `FilterReach` attribute, which a fresh copy puts back; drawn blade and etch parts carry `DrawnMesh` (their SwordMeshCache key), which a fresh copy releases and removes before drawing again; `ItemPicker` reuses `Lighting.PickerBlur`, switched off. |
| `Shared/AnvilScore` / `Shared/BladeMesh` / `Shared/BladeProfile` / `UiFx` / `Analytics` | 2026-11-02 (second audit): unused code removed: AnvilScore's outline scoring (`accuracy`, `smoothness`, `grade`, `evaluate`, the `BladeProfile` require), BladeMesh's EditableMesh blade (`new` and its methods; `stationX`/`stationWidth` stay), `Shared/BladeProfile` (backup `Legacy.BladeProfile_removed_1102`), `UiFx.countUp`, `Analytics.bin`. `Analytics.states` is weak-keyed. |
| `DevPanel` | 2026-11-02 (second audit): buttons in two columns of 7 (`row // 7`, `row % 7`) so all fit a phone-size screen; the Give sword picker sits left of both (x -332). |
| `StarterGui.HotbarGui.Templates.Slot`, `Bar.Bag`, `Hotbar` | 2026-11-02 (style H6): `EdgeArt` removed; new `Halftone` (CanvasGroup, 12 px corners) with `Dots` (tile `rbxassetid://106477061422613`, 5.5 px, black, 70% transparent, `UIGradient` 45° fading 1 to 0), `Outline` (Frame, `UIStroke` 2 px ink 16,20,16, ZIndex 4) and `InnerRim` (inset 3 px, 9 px corners, white stroke 1.5 at 50%). `Edge` stays the amber in-hand stroke. `sheen(base)`: the old bright band (`base:Lerp(BLACK, 0.16):Lerp(WHITE, 0.06)`) divided by 0.68 at the top, 20% darker at the foot; Bag's gradient set to the same for Common in StarterGui. [[Sessions/2026-11-02#Hotbar style H6]] |
| `SwordRenderer` shop shine | 2026-11-03: `shine(model, part, path, polished)` for a displayed sword (Model, `Prop` ~= true), stopped in `free()`; the glare `glint` now runs only on held swords and props. One `RenderStepped` loop over `shines`: within `SHINE_NEAR` 35 and not hidden (`LocalTransparencyModifier` < 1) it builds up to `SHINE_PIECES` 64 `Beam`s (FaceCamera, colour 215,225,235, Brightness 1.1, 30% clear) between `ShineLine` attachments along `edgePath` (× the model's scale), else destroys them. Lit stretch `SHINE_HALF` 0.14 each side of `u`, width `SHINE_WIDTH` 0.06 with a smoothstep taper; `u` = 0.5 − 0.5·(view·axis)/`SHINE_SIDE` 0.8 + a random bias, strength from |view·UpVector|; both re-aim only after the camera moves `SHINE_STEP` 0.4, eased at `SHINE_EASE` 6. Polished: a pulse (`PULSE_HALF` 0.09, +0.07 width, +3 brightness) over `WAVE_TIME` every 2.5–4.5 s. Widths are rewritten only when `u`, strength or a pulse changed. [[Sessions/2026-11-03#Shop shine on displayed swords]] |
| `SwordMeshCache.edgePath` | 2026-11-03: one point per station (`#params.segLen`, was `EDGE_POINTS` 14), same 0.04–0.96 span. |
| `OreBoxShow` lever cues / `SoundService.Effects.Cues.LeverPull`, `LeverRatchet` | 2026-11-03: two Sounds cloned from `RollLand`'s settings (Inverse, 10–40 studs, Effects): `LeverPull` 9116260154 vol 0.5, `LeverRatchet` 88329158538816 vol 0.45. `OreBoxShow.new` finds `roller.Lever.Base`; `pose(t)` plays `LeverPull` there on the first pose if `t` < 0.3 and `LeverRatchet` once `t` ≥ `RATCHET_AT` 0.45 (if within 0.3 of it), each a clone at `PlaybackSpeed` × 0.95–1.05, removed after 3 s. A show that streamed in late plays neither. [[Sessions/2026-11-03#Lever sounds]] |
| `OreBoxAnimator` lever wind-up / `LeverAnimator` `AutoPullAt` | 2026-11-03 (later): supersedes the ratchet in the `OreBoxShow` lever cues row (OreBoxShow keeps only `LeverPull`). `OreBoxAnimator.windUp(roller, from)` clones `Cues.LeverRatchet` (now 89774753801931, 1.0 s) onto `roller.Lever.Base` at `TimePosition` `from`, × 0.95–1.05 speed. `ProximityPromptService.PromptButtonHoldBegan` on a `RollPrompt` starts it; `PromptTriggered` lets it finish; `PromptButtonHoldEnded` (deferred, > 0.2 s after a trigger) destroys it. `LeverAnimator`'s `autoSwing` sets the OreRoller's `AutoPullAt` = server time; `watch` plays the wind-up from `now − AutoPullAt` if under 0.5 s and the roller is in range. [[Sessions/2026-11-03#Lever sounds]] |
| `OreBoxShow.ring` | 2026-11-03: the `RollDone` clone fades `Volume` to 0 over `DONE_FADE` 0.4 s after `DONE_RING` 0.6 s (TweenService delay), removed at 1.1 s. `Cues.Upgrade` (same id) unchanged. [[Sessions/2026-11-03#Lever sounds]] |
| `UiSounds` (LocalScript) / `Cues.UiClick`, `UiHover`, `Upgrade`, `Sale` | 2026-11-03: hooks every `GuiButton` in PlayerGui (existing and `DescendantAdded`, weak `hooked` set): `Activated` restarts `Cues.UiClick` (876939830, 0.5); `MouseEnter` restarts `Cues.UiHover` (124917708988713, 0.25) unless the last input was Touch. Not through `Cues.play` (its 1.5 s gap). `Cues.Upgrade` 80736831159506 vol 0.3; `Cues.Sale` 71081254550638. New Sounds cloned from `Sale` (Effects group). [[Sessions/2026-11-03#UI, buy and coin sounds]] |
| `OreBoxShow` / `SoundService.Music` / `Cues.Swings` | 2026-11-03 (later): `OreBoxShow` drops `ring`, `rung`, `last`, `doneSound` and the DONE_ fade; `Cues.RollDone` is unused. `SoundService.Music` holds one Sound `1 Theme` (138306628711326). `Cues.Swings` holds one `Swing1` (101542904500316). [[Sessions/2026-11-03#UI, buy and coin sounds]] |
| `OreBoxShow.landed` | 2026-11-03 (later): no `RollLand` sound (`landSound` removed); `Cues.RollLand` unused. |
| `Cues.Swings` | 2026-11-03 (later still): `Swing1` 126349511518680, `Swing2` 126259799790624 (Pixabay, trimmed, -12 LUFS); supersedes the one-sound row above. `SwordSlash.whoosh` picks one at random. |
| `PolishController` scrubbing / `StarterGui.PolishHud.Brush` | 2026-11-03: grime section: `buildGrime` takes `SwordMeshCache.overlay(blueprintId, refinement, shape)` (part, `{surface, layout}`), makes an EditableImage of `layout.size` (strips × 1024 × 128) and f32 `g` (dirt 0..1) plus RGBA buffers, one row built per strip and copied down (specks shifted 37 px a row); overlay Transparency 0.02, Y size × `GRIME_LIFT` 1.25 (over an etch skin). `colStation`/`stationCols` map image columns to the nearest station by `segLen` distance. `locate(hit, station)` finds x cm and w (0 edge, 1 spine) on `surface.point`'s across-lines. `wipe(x, w, amount)` lowers `g` by amount × (1 − d²/R²) in the brush disc (R = max(`BRUSH` 0.3 × mean width, `BRUSH_MIN_PX` 22 px)), tracks `colSum` and a dirty rect; `settle(from, to)` sets each station's refinement to max(old, 1 − its dirt share; 1 under 2%); `clearGrime` at `SNAP` 0.95; `flushGrime` writes the dirty rect once a frame. `polishAt` dabs every R/2 along the drag at `WIPE_PER_CM` 0.5. `paint` draws the blade `setFinish(nil)` (bright). Touch aims `TOUCH_LIFT` 0.09 of the screen above the finger; `showRing` sizes and places `PolishHud.Brush` (circle Frame, white UIStroke). `padScreen(u, w)`; R2 zigzags `padW` over `PAD_ZIG` 0.45 s. Ghost: circles of 3.5% screen height every `GHOST_SPIN` 0.6 s, drifting along 0.25–0.75 of the blade. Backup `Legacy.PolishController_beforeScrub_1103`. [[Sessions/2026-11-03#Polishing by scrubbing]] |
| `PolishController.graceCast` | 2026-11-03: returns the cursor's own blade hit if any, else the first hit on the nearer ring (0.035, then 0.07 of the screen height), else nil; no edge preference. |
| `PolishController.graceCast(screen, rings?)` | 2026-11-03 (later): `GRACE` = { 0.02 }; `showRing`'s hover cast passes `{}` (cursor ray only). |

## Sound-ids fix list (2026-11-03)

| Where | What |
|---|---|
| `Shared/Upgrades`, `Shared/Etches` | `EtchingTable` carries `etch = "Flame"` (Flame comes with the table); `EtchFlame` and its pad are gone; `EtchWovenWind` is `after` the table; `CHAINS.Etches` { EtchWovenWind, EtchFracture }; bonuses 0.10 / 0.15 / 0.20. |
| `TycoonService` | `PAD_ALWAYS` { Delivery, Crafter, EtchWovenWind }. |
| `HiltSeat`, `AnvilController` | `HiltSeat.play(..., auto)`: slides home by itself, no hint or ghost; `AnvilController` forward-declares `autoOn` and passes it. |
| `ShopService` | 1.5 s wait after a decline (then `stillThere`); plot attribute `Customers` from `onTheWay` in `sendCustomer` / `free`. |
| `SwordRenderer` | `glint(part, path, shimmer, held, mirror)`: Tools sweep (`HELD_TIME` 1.4, `HELD_LENGTH` 0.35), only in `workspace`. |
| `MenuController` | TopbarPlus `Customers` icon (order 3, image 96517349143124): label = plot `Customers`, a tap spells it out for `SPELL_TIME` 2.5 s, caption on hover. |
| `GemController`, `GemGui.Templates.Day` / `Day7` | Daily tier gradients as ColorSequence attributes, gem art One / Pile / BigPile, gold `Day7`; the tutorial's last Gem Shop buy calls `close()`. |
| `Guide` | `confetti()` from both bottom corners (skipped without `Prefs.motion()`); `crewTour()` after the first Taise hire (`seenHired` edge). |
| `MenuGui.ShopWindow` | Daily Reward's `Fill`, `Pattern`, `Tint`; `Content.ZIndex` 5. |
| `Plot.Smithy.TrainingDummy` / `SwordSlash` | 2026-11-03: the training dummy (model 110560742783067, tag `TrainingDummy`, `Pivot` 0.3; builder `Models/Props/TrainingDummy`). `SwordSlash`'s dummy loop (0.1 s): standing still within `REACH` 5.5 → face it, `swing()`, `knock()` at `HIT_AT` 0.18; a RenderStepped spring (`STIFF` 140, `DAMP` 7, `KICK` 3.4, cap 22°) tilts every part but `Feet` about the pivot, restoring the rest CFrames when still. Client-only. |
| `Plot.Smithy.SwordRack` / `SwordRack2` `.Stretcher` | 2026-11-03: rack-space z -0.19 (was -0.50), overlapping the posts. |
| `TycoonService.stepOut` | 2026-11-03: `GetPartBoundsInBox(root * (0,-0.5,0), 2×4×1)` over the bought item's collidable parts (`OverlapParams` Include, `RespectCanCollide`); out over the hit part's nearer side by `CLEAR`. |
| `Shared/GemUpgrades.list` | 2026-11-03: prices Advertising 5/20/35/55/85, Vip 15/25/40/65/100, Clients 20/30/50/80/120, Mail 15/25/40/65/100. |
| `Shared/Upgrades` `IngotRack3` / `IngotRack4`, `Plot.Smithy.IngotRack3/4`, `IngotRack.Slots.Slot13-24`, `Pads.IngotRack3/4` | 2026-11-03: two more six-ingot shelves (8,000 / 30,000); `RackService.near` lists four racks; `RackController.RACKS[*].also` is a list of prompts (Ingot: Racks 2-4; Sword: Rack 2); sim `engine.ingot_cap` counts four. |
| `CrewGui.Window.Station` / `Templates.Card` / `Stats.Panel.Body` / `EmployeeController` | 2026-11-03: Station `Top.Back`, no `Buttons`, anvil cards `Row.Face` + `Words`; `fillStation` titles "<Name>'s Station", a tap toggles equip/unequip. Card 350×328 (`UIGridLayout` 2 across): `View`, `Info` (Head: CrafterName/Lvl, Trait, Stars, Level + `XpText` / Price / Needs / Cost). `xpBar` helper; `STATUS_COLOR`. Gone: `stationPick`, Equip/Unequip handlers, `bar`, `FORGE_SCALE`, comparison arrows. |
| `CrewGui` / `EmployeeController` | 2026-11-03 (later): cards reverted to the pre-change templates (`Templates.Card` 228×300, `Stats.Panel` as before); only `Window.Station` (Top.Back, `Row.Face` + `Words`) and its `fillStation` / tap toggle stay. Portrait-card copies in `Legacy.*_portraitCards_1103`. |
| `Plot.Smithy.IngotRack1-4` | 2026-11-03 (later): no `Back` / `Top`; sides 0.24..4.03. Racks 3-4 at plot x 662 (z -312.0 / -300.1), turned 180° from Rack 2, `Turned` 0; `Slot13-24` and `Pads.IngotRack3/4` (x 665.5) moved with them. |
| `Shared/Employees` | 2026-11-03: `BATCH` 2; crafter `walk` = { Lv. 1, Lv. 5 } (6/12, 6/12, 7/13, 7/13, 8/14); `crafterWalk(c, level)`. |
| `EmployeeService` (crafters) | 2026-11-03: `CrafterJob` = { ingots, worker, claims, trips }. `oneSword` takes up to `BATCH` ingots (rack room permitting), heats each in turn, forges/polishes ×n, racks one by one (`job.ingots[1]` is the next blade's). `noteTrip` / `rateAttr`: plot attribute `CrafterRate` (`CrafterRate3`, `4`) = swords a minute over the last `RATE_TRIPS` 4 trips; `dismiss` clears it. `crafterLoop` sets `WalkSpeed = Employees.crafterWalk` each trip; `makeWorker` takes `walk[1]` for a crafter. Save puts back every ingot in hand. Backups `*_beforeCrewBatch_1103`. |
| `CrewGui.Window.Stats.Rows` / `EmployeeController` | 2026-11-03: rows 29 px (Rows 724×145), new `Rate` ("Swords / Min") and `Crew` ("Crew / Min") at y 116. `anvilRate(anvil)`; `fillStats` fills them (one decimal, "-" without data) and Walk from `crafterWalk`. |
| `ExportBalance` / sim `rules.crafter_walk`, `engine.on_crafter` | 2026-11-03: `employees.batch`, golden `quality[].walk`; the sim's crafter takes `metals` (up to batch), heat/forge/polish ×n. |
| `Village.Lots.PlotSlot*` / `Village.Lots.Pad` | 2026-11-04: back to before 2026-11-03 (slots y 0.5, flat pads; restored from `Legacy.Lots_beforeRaise_1103`). |
| `Workspace.Plot` (template) | 2026-11-04: pivot (640, 0.5, -284) again; `Grounds.Forecourt` and `Grounds.CartRamp` gone. The shop is 1 stud up: `Shop.Starter`, `Shop.Upgraded`, displays (not `Showcase1-3`), `CashierCounter`, `EntryPoint`, `Decor` with `Section = Shop`, `Workshop` and the 15 buy pads inside the shop. `Shop.Starter.Plinth` / `Shop.Upgraded.Plinth`: 49 × 1.16, plot y -0.5 to 0.66, z -47.7 to -17.1 / -5.1, Slate `PaintStone`, kerb colour; floor top 0.70. Backups `Legacy.Shop_/Workshop_/Pads_beforeShopRaise_1104`. |
| `Village.Street` gutters / street lights | 2026-11-03: the 22 `Water` parts are `Gutter` (Slate `PaintStone`, curb colour ×0.75, no reflectance). The 12 frontage `StreetLight`s were +1 stud on 2026-11-03 and are back down since 2026-11-04. |
| `DeliveryService` | 2026-11-04: back to `Legacy.DeliveryService_beforeRaise_1103` (no ground-following; the cart stays at home height on a flat route). |

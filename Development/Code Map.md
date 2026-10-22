---
title: Code Map
status: current recorded architecture — runtime verification pending
type: development
updated: 2026-10-22
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
AttachHilt → three untimed knocks → assembled sword
Optional BeginPolish / PolishSword → polish finish bonus
Optional EtchSword → accepted etch + client playback
DisplaySword → customer Offer / RespondOffer → coins + sale count
```

Recorded player-facing rule: completing forging gives **100% quality**; full polish adds **+10% value** and etching adds **+15%**. Old 90%-cap descriptions in the archived map predate that rule. Blade refinement remains an internal geometry/finish concept; do not infer current displayed quality or server limits from old port/probe descriptions. Inspect live SmithService/ForgeCheck when changing either.

Server state is authoritative: inventory, coins, completed/sold counters, racks, displays, furnace contents and bought upgrades. Since 2026-10-22 it is saved per player under a session lock ([[Development/Saving]], [[#First session and saving (2026-10-22)]]). Item pickers open even when only one valid item exists.

## Workspace and plot ownership

- `Workspace.Village`: the chosen simplified walled map, six lots, gate, shrine and broad flagstone street. `Village.Lots.PlotSlotN2` is the template's Edit pivot; other slots identify the five remaining lots.
- `Workspace.Plot` in Edit: reusable template with `Shop`, `Workshop`, `Smithy`, `Pads`, `Yard`, `PlayerSpawn`, `CustomerSpawn` and the delivery bay. At runtime PlotService moves the template to `ServerStorage.PlotTemplate`.
- Claim order: **N2, N1, N3, S2, S1, S3**. A joining player gets `Plot_<lot>` with `Lot`, `OwnerId` and `OwnerName`; the player receives a `Plot` attribute and their own respawn location. South lots turn the whole plot toward the street.
- Unclaimed lots hold inert empty plot copies. Claiming replaces one; leaving destroys the owned copy and restores the empty one. Visitors can walk through but cannot use another player's stations or buy upgrades.
- `Plot.Shop`: Starter/Upgraded shells, displays, entry point and decor-only commission boards. `Plot.Smithy`: ore roller, furnaces, anvil, hilt/polish/etch stations and racks.
- Upgraded Store pushes the workshop, stations, workshop pads, spawn and characters inside it back **12 studs** in plot space. Use plot-local coordinates for moves, cameras and customer routing.
- `Shop.DeliveryWall` uses `UntilUpgrade = Delivery`; `Shop.DeliveryDoor` uses `Upgrade = Delivery`. No `Delivery` catalogue entry/pad exists yet. The bay's `CartSpot` is reserved for future courier gameplay.

Details: [[Design/Six Plots]], [[Design/Tycoon Upgrades]], [[Art/Workshop Layout]], [[Art/Ore Loot Box]].

## ServerScriptService

| Script/module | Responsibility |
|---|---|
| `SmithyCore` | Per-player ingots/blades/swords, coin transactions, completed/sold counters, public state, item Tools/Models and respawn restoration. Sword values include fitting/polish/etch bonuses. |
| `PlotService` | Template, lot allocation, empty copies and owner/plot lookup. API: `plotOf(player)`, `plotFrom(inst)`, `ownerOf(inst)`; preparation, claim and release hooks. |
| `TycoonService` | Per-plot `Bought_<id>` flags, prerequisite pads, ownership/reach/spend checks, `TycoonItem` locking and workshop push. |
| `ForgeService` | Each plot's ore box and purchased slots; collect-before-reroll; one ingot per unlocked furnace. Heating is 3 s until first completion, then 10 s. |
| `SmithService` | Begin/finish forge requests, blueprint/ingot validation through `ForgeCheck`, and hilt assembly. |
| `ShopService` | Owner-specific displays, per-plot customer routes/spawners, offers/haggling and sale payouts. At most two customers per plot. |
| `PolishService` | BeginPolish/PolishSword, station reach/unlock checks, refinement replay/timing validation, state update and rebuilt sword. |
| `EtchService` | Valid sword/pattern, own unlocked station/reach and one-etch-per-sword checks; accepted finish updates authoritative state. |
| `RackService` | Own-plot ingot/sword storage and retrieval; recorded capacities are 12 ingots, 6 swords, 6 carried. |
| `LeverAnimator` | Lever hold/release motion for plot rollers. |
| `DevTools` | Studio-only coin and example-sword grants; guarded by `RunService:IsStudio()`. |

First-sale exceptions: a listing spawns a customer immediately until `sold > 0`; later arrivals use 12–22 s intervals. At `sold == 0` the offer is exact value and declining ends it. At `sold == 1` a hint shows and the first decline guarantees a raise. Later sales use normal negotiation. Future direct commissions must not increment the ordinary-shop sale counter.

## ReplicatedStorage

| Module/asset | Responsibility |
|---|---|
| `Shared/BladeCore`, `BladeData`, `Blueprints` | Blade geometry/progress, universal blank and tantō/wakizashi/katana data. Local port/data tools remain under `Prototypes/tanto-forge/`. |
| `Shared/BladeView`, `BladeMesh` | Active deforming blade presentation; anvil/polishing need live geometry. |
| `Shared/ForgeCheck` | Server replay and completion/refinement/timing validation. |
| `Shared/Materials`, `Hilts`, `ValueFormula`, `Customers` | Material odds/appearance/value, fittings/milestones, price rules and NPC offer/raise behavior. |
| `Shared/Upgrades` | Upgrade IDs, prices and prerequisites; pad IDs and `TycoonItem.Upgrade` attributes must match. |
| `Shared/Etches`, `EtchPatterns`, `EtchCanvas` | Finish catalogue, stroke paths and progressive/final image work. Flame and Eclipse have build records; further patterns require confirmation. |
| `Shared/SwordMeshCache` | Shared, baked-first finished-sword geometry with live fallback and etch/polish appearance. |
| `SwordMeshes`, `SwordParts.KatanaHilt` | Uploaded finished meshes and dressed hilt/guard templates used by world and viewport art. |
| `Remotes` | Forge/hilt/polish/etch, state, rack, display/offer and upgrade request/event boundary. Client choices require server ownership, reach and state checks. |

Legacy `BladeProfile`, `AnvilScore` and probe modules may remain dependencies or test references. Inspect callers before removal; they are not the current design specification.

## Client controllers and interface

- `MyPlot`: `current()`, `get()`, `owns(inst)`, `plotOf(inst)`; controllers resolve their own plot instead of `workspace.Smithy`.
- `PromptFilter` and the shop/tycoon controllers limit prompts, buy buttons and display markers to the player's plot. Server ownership checks remain authoritative.
- `AnvilController`, `ForgeController`, `HiltBenchController`, `PolishController`, `EtchingTableController`, `RackController`, `ShopController`: station pickers, interaction, framing and feedback. The hilt view follows bench orientation.
- `ItemPicker`: reusable item cards with real blade/hilt/etch art, toasts and small-screen layout. Free temporary resources on rebuild/close.
- `EtchPlayback`: private progressive canvas over a shared overlay, stylus/sparks and station camera; restore controls, camera and hidden table props on finish/interruption. Server acceptance determines the finish, even if the show is interrupted.
- `OreBoxShow` / `OreBoxAnimator`: all clients see the 3.6 s lid/ingot show; ForgeService exposes the real results at the end.
- `SwordRenderer`: held/displayed blade art and release on removal. `SwordMeshCache` uses baked finished meshes; no blanket one-live-mesh-per-finished-sword assumption remains.
- `RoofHider`: locally fades unlocked roofs on the plot the player enters; inert empty plots retain roof behavior.
- `Hotbar`: nine item slots plus bag button (`~`), rarity colours, ingot stacking, backpack overflow, drag/drop and click/tap equip. Gamepad R1/L1 cycle through the bar and then the bag (2026-10-22). [[Art/UI Design]] records the chosen styling.

Etched polishing now brightens the body at polish levels; preparation spreads over frames and the last etch remains warm for 5 s after leaving. This is a recorded hitch fix awaiting Play verification.

## Local builders and authoring

- `Models/Village/build_simple.luau` builds the live map; `build_shops.luau` builds shop/workshop shells, then `build_workshop.luau` builds the room furniture, loot box and delivery pieces.
- `build_street.luau` and `build_town.luau` are retained historical builders for the parked maps, not the live-map entry point.
- Studio copies live in `ServerStorage.Builders`; compare copies after edits. Builder source modules are executed with `loadstring(...Source)()`, rather than required as ordinary modules.
- `ServerStorage.Builders.bake_sword_meshes` is an ordinary require-able module, run from a fresh clone with the local `Development/sword_mesh_bake.py` helper. See [[Development/Sword Mesh Pipeline]] for upload/bake instructions.
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

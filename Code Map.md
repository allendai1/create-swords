---
title: Code Map
status: current (2026-10-19)
tags: [code, architecture, create-swords]
---

# Code Map

Where everything lives in the Studio place (`goku19876's Place: 10172026_1`) and how the pieces connect. The code exists only in the place file (no Rojo/Git; see [[Decisions Log]]), so **save the place** after every session. The design behind it is in [[Create Swords! GDD]]; day-by-day history is in [[Sessions/2026-10-17]].

## How a sword is made (data flow)

```
Ore Roller ──(ForgeService)──► cold ingot (Tool)
   Forge picker ─ForgePut─► slot (timer label) ─E "Take out" / ForgeTake─► hot ingot (Tool)
Anvil (AnvilController) ── choose hot ingot → blueprint ─BeginForge(ingotId, blueprintId)─► SmithService (start time)
   12 untimed strikes (BladeCore) → 90%, optional grinding → up to 100%
   Finish ─FinishBlade("Forge", blueprintId, savedState, ingotId)─► SmithService
      ForgeCheck replays the strikes, checks grinding and minimum time → grade; ingot used up → carried blade
Hilt Bench (HiltBenchController) ── pick blade + hilt, seat it (3 taps)
   ─AttachHilt(bladeId, hiltId, goodTaps)─► SmithService → completed sword (Tool)
Sword holder "+ Display a sword" ─DisplaySword(slot, swordId)─► ShopService → rack Model + price tag
Customers (ShopService) walk in → Offer → RespondOffer → coins (leaderstats)
SwordRenderer draws every sword's blade on each client with BladeCore + BladeView, from BlueprintId and BladeRefinement.
```

The server owns all state (ingots, blades, swords, coins, forge slots, rack). Clients only show it and send choices. All of it is session-only until DataStore saving is added.

## ReplicatedStorage

| Path | What it is |
|---|---|
| `Shared/BladeProfile` | (Prototype modes; still required by AnvilScore.) The blade as 40 slices of left/right half-widths (1.0 = blank). Hammer hits with falloff and grind strokes (`kind = "grind"`, segments trimmed with `cut`), undo/redo/reset per hit or stroke, `replay(hits)` with validation |
| `Shared/AnvilScore` | Accuracy %, smoothness %, Finish at 80%. Quality = the percentage (`forPercent`: name "92%", multiplier ×1.0 at 80% → ×2.0 at 100%); no grade names |
| `Shared/Blueprints` | Tantō, wakizashi, katana built from `BladeData` (2026-10-19): price and stars (placeholders), length in studs, picker silhouettes, `Blueprints.blade(id)` for BladeCore. `STUDS_PER_CM = 0.05` for anvil, held and displayed swords. `Blueprints[id]` and iteration still work for older callers |
| `Shared/BladeView` | Client EditableMesh blade from BladeCore: `setParams`, `setFinish(refinement, hot)` (dull → bright steel per section), `raycast` against the mesh itself (grinding). Used by the anvil and SwordRenderer |
| `Shared/ForgeCheck` | Server check for Finish: replays the saved state, requires all strikes, refinement 0–1, and a minimum elapsed time (0.35 s per strike + up to 2.5 s for full grinding) since BeginForge; grade from `AnvilScore.forPercent` |
| `Shared/Materials` | 13 materials, 5 rarities: roll odds, value multiplier, colour |
| `Shared/Hilts` | 6 hilts (+0–40%, unlock by swords completed), seat-the-hilt bonus |
| `Shared/ValueFormula` | base × material × quality multiplier × (1 + hilt + seat bonus) |
| `Shared/Customers` | Farmer / Adventurer (likes wakizashi) / Knight (likes 95%+ blades, i.e. ground ones): likes, offer and raise maths |
| `Shared/BladeCore` | Port of the browser study's blade core (2026-10-19): stage shapes at 64 stations, strikes, safe grinding, quality, fixed 782-vertex mesh layout, save validation, catalogue measurement. Source of truth: `Prototypes/tanto-forge/roblox/` in the vault. Used by the anvil, server check and SwordRenderer. |
| `Shared/BladeData` | Generated from the study's JSON (`tools/export-luau.js`); tantō, wakizashi, katana and the universal blank |
| `Shared/BladeProbe` | Test-only EditableMesh forging/grinding probe; runs only when `workspace` has the `BladeProbe` attribute (via `StarterPlayerScripts.BladeProbeLoader`) |
| `Shared/BladeMesh` | Client-side EditableMesh blade: ridge band and bevels (band across the blade's own width from `blueprint.ridge`, smoothed), sharpness, accent lines (ridge lines or a single shinogi, fuller, a katana's yokote; tinted from the blade colour), pointed tips |
| `Remotes/` | BeginForge, FinishBlade, AttachHilt, GetSmithState, SmithState, ForgePut, ForgeTake, DisplaySword, Offer, RespondOffer, ShopNotice |

## ServerScriptService

| Path | What it is |
|---|---|
| `SmithyCore` (module) | Per-player state (ingots, blades, swords, completed count), coins in leaderstats; builds ingot Tools and sword Tools/Models; re-gives items on respawn. `publicState` swords include materialId / blueprintId / hiltId for the picker art |
| `SmithService` | BeginForge (notes ingot, blueprint, start time), FinishBlade (mode "Forge" only, via ForgeCheck; blade stores `refinement`), AttachHilt (unlock check + seat bonus), GetSmithState. **Studio only:** `ServerStorage.DevGiveHotIngot` BindableFunction hands a player a hot ingot for playtests |
| `ForgeService` | Ore Roller roll (max 6 carried); forge: 2 shared slots, 15 s, ForgePut / ForgeTake. `ForgeTimers` BillboardGui on `Forge.Base` stacks one "Iron · Heating" label (bar + seconds) per busy slot. Slot parts `ForgeSlot1/2` carry `Slot`, `OwnerId`, `Ready` attributes for the client |
| `ShopService` | 3 sword holders (DisplaySword, take back with F), price tags; customer NPCs (walk in, inspect, offer, haggle, timeout), coins on sale |

## StarterPlayerScripts (client)

| Path | What it is |
|---|---|
| `AnvilController` (rewritten 2026-10-19) | E → hot-ingot picker → blueprint picker → BeginForge. Strike circle (Space / click / tap, one buffered tap), hammer pivoting behind the anvil, blade slides/turns/flips under it, eased local deformation, sparks, clang, shake. After 12 strikes the blade cools and the hammer is put away; hold-and-drag grinding on the edge bevel with the GrindMap strip (dull → bright, orange brackets on stretches left). Panel shows quality, strike/stage and the outline vs the finished shape. Angled overhead camera fitted to the blueprint's reach; the smith is placed and hidden. The old prototype modes are in `ServerStorage.Legacy.AnvilController_PrototypeModes` |
| `HiltBenchController` | E → picker "Choose a blade." → picker "Choose a hilt." → seat-the-hilt taps (Space / tap) → AttachHilt → toast |
| `ForgeController` | E: "Take out" when your ingot is ready (the prompt text switches), "Forge is full" toast when both slots are busy, else the picker of your cold ingots stacked by material; picking closes it, puts one in and toasts "Ingot loaded" |
| `ShopController` | "+ Display a sword" picker (sword cards with price), offer card, notices |
| `ItemPicker` (module) | The shared picker (vault: [[UI Design]]; Gotham font), built in code into its own `PickerGui`: station title + action line, grid of cards (3D item in a ViewportFrame or a blade silhouette, name, chip, ×qty; hover / gamepad focus = amber edge), close ring (B closes), blur + dim behind, empty state. Compact one-row layout when the screen is under 500 px tall. Also `toast(text, "warn"?)`. Used by the forge, anvil, holders and Hilt Bench |
| `SwordRenderer` | Draws held and displayed blades with BladeCore + BladeView (one EditableMesh per visible sword for now) |

## StarterGui

`AnvilHud` (anvil panel, hint, result banner; Tools, Hammers and ModeButton are hidden by the new controller), `AnvilPoints` (unused since the rewrite; the strike ring is built at runtime in `StrikeRingGui`, the grinding map in `GrindMap`), `HiltBenchHud` (only the Seat panel now), `ShopHud` (offer card, notices). The picker and toasts are built at runtime by `ItemPicker` (`PickerGui`).

## Workspace

`Smithy/` holds `OreRoller`, `Forge` (Base + HeatPrompt "Use forge"), `Anvil` (BladeMount, ForgePrompt, Clang sound), `HiltBench`, `DisplayRack` (Slots 1–3, each with a HolderPrompt). The blade on the anvil (`Blade`), the Trace guide and the `Customers` folder are created at runtime.

Rebuilt 2026-10-19 in the Japanese style ([[Smithy Redesign Proposal]]). Each station keeps the parts scripts read, and its look lives in a `Dress` model (plus `Stand1` on the roller):

| Station | Parts scripts read (don't move or rename) | Free to restyle |
|---|---|---|
| `Forge` | `Base` (invisible box, exact old size and CFrame; ForgeService places `ForgeSlot1/2` and `ForgeTimers` from it) + `HeatPrompt` | `Fire` (Neon + PointLight in the chamber), `Chimney`, `Dress` |
| `OreRoller` | `Machine` (now the lever post at −12.2, 1, −13.4) + `RollPrompt` | `Stand1` (`Ore` is the part a roulette reveal would recolour), `Dress` |
| `Anvil` | `BladeMount`, `Face` + `ForgePrompt`, `Clang` | `Stump`, `Waist`, `Base` (now the hornless block and banded wood base), `Dress`. `Horn` was removed |
| `HiltBench` | `Top` + `HiltPrompt` | everything else |
| `DisplayRack` | `Slots/Slot1..3` + `HolderPrompt`. Slots now sit at x 9.8 / 13 / 16.2, z −10, same rotation (blade up, broad face to +Z). ShopService's `INSPECT_POINT` (13, 3, −6.5) assumes the middle one | `Base` (the deck), `Dress` (pedestals) |

`Workshop/` is the building around them, with no scripts: `Ground` (plot pad, earth and stone floors, path), `Frame`, `Walls`, `Roof`, `Front` (signboard, noren), `Lanterns` (a chōchin on every front post, wall lamps inside). Tie beams skip the anvil bays so the forging camera stays clear. The open side faces +Z. `SpawnLocation` sits in front of it at (1.5, 0.15, 9); the Baseplate is grass. The old prototype blocks (`store`, `creation area`, two slabs) are in `ServerStorage.Archive`.

## Models (outside Studio)

`Models/Archive/SwordShop.bbmodel` (Blockbench source) and `Models/Archive/SwordShop.fbx` (import file, 1 unit = 1 stud): the historical medieval cabin, 17 named meshes on one palette texture. Never imported; superseded by `Workspace.Workshop`.

## ServerStorage.Legacy

`SharedV1` is a frozen copy of the shared modules from before the 2026-10-19 rewrite (old Blueprints, ShapingModes, FinishCheck…) and `AnvilController_PrototypeModes` (disabled) is the old anvil with its Silhouette/Trace/Clicks/Points modes. Kept for reference and for `AnvilSelfCheck`.

## Tests

- `ServerStorage/Tests/BladeCoreSpec` (with `BladeGolden`) tests the BladeCore port; see `Prototypes/tanto-forge/roblox/README.md`.
- `ServerStorage/Tests/ForgeCheckSpec`: the new blueprints and the server's Finish check (35 checks). Run `print(require(game.ServerStorage.Tests.ForgeCheckSpec)())` in the command bar.
- `ServerStorage/Tests/AnvilSelfCheck` now checks the frozen `Legacy.SharedV1` copy (old blade maths, prototype modes, customers, materials, value). Run `require(game.ServerStorage.Tests.AnvilSelfCheck)()`.

`ServerStorage/AnvilController_Backup` is the disabled pre-refactor controller. Safe to delete.

Related: [[Home]] · [[Roadmap]] · [[Create Swords! GDD]]

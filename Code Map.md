---
title: Code Map
status: current (2026-10-18)
tags: [code, architecture, create-swords]
---

# Code Map

Where everything lives in the Studio place (`goku19876's Place: 10172026_1`) and how the pieces connect. The code exists only in the place file (no Rojo/Git; see [[Decisions Log]]), so **save the place** after every session. The design behind it is in [[Create Swords! GDD]]; day-by-day history is in [[Sessions/2026-10-17]].

## How a sword is made (data flow)

```
Ore Roller ──(ForgeService)──► cold ingot (Tool)
   Forge picker ─ForgePut─► slot (timer label) ─E "Take out" / ForgeTake─► hot ingot (Tool)
Anvil (AnvilController + Modes) ── choose hot ingot, shape the 40-slice blade
   Finish ─FinishBlade(mode, blueprint, payload, ingotId)─► SmithService
      FinishCheck replays the payload → grade; the ingot is used up → carried blade
Hilt Bench (HiltBenchController) ── pick blade + hilt, seat it (3 taps)
   ─AttachHilt(bladeId, hiltId, goodTaps)─► SmithService → completed sword (Tool)
Sword holder "+ Display a sword" ─DisplaySword(slot, swordId)─► ShopService → rack Model + price tag
Customers (ShopService) walk in → Offer → RespondOffer → coins (leaderstats)
SwordRenderer draws every sword's blade mesh on each client from the Tool/Model attributes.
```

The server owns all state (ingots, blades, swords, coins, forge slots, rack). Clients only show it and send choices. All of it is session-only until DataStore saving is added.

## ReplicatedStorage

| Path | What it is |
|---|---|
| `Shared/BladeProfile` | The blade as 40 slices of left/right half-widths (1.0 = blank). Hammer hits with falloff and grind strokes (`kind = "grind"`, segments trimmed with `cut`), undo/redo/reset per hit or stroke, `replay(hits)` with validation |
| `Shared/AnvilScore` | Accuracy %, smoothness %, Finish at 80%. Quality = the percentage (`forPercent`: name "92%", multiplier ×1.0 at 80% → ×2.0 at 100%); no grade names |
| `Shared/Blueprints` | Target outlines plus price, length and fuller. Dagger and Shortsword (shape functions), Katana (drawn from real proportions along the hilt-to-point chord; `SwordRenderer` turns it to its root angle on held swords) |
| `Shared/ShapingModes` | Prototype rules: partly-formed `morph`, trace `cut`, timings; Points `pointSpot` (near edge hilt→tip, then far edge tip→hilt), `pointShape`, `gradeForHits` |
| `Shared/FinishCheck` | The server re-grades Finish from the payload for each mode (Points: `hit` = 1/0 per point, in order) |
| `Shared/Materials` | 13 materials, 5 rarities: roll odds, value multiplier, colour |
| `Shared/Hilts` | 6 hilts (+0–40%, unlock by swords completed), seat-the-hilt bonus |
| `Shared/ValueFormula` | base × material × quality multiplier × (1 + hilt + seat bonus) |
| `Shared/Customers` | Farmer / Adventurer / Knight (likes 90%+ blades): likes, offer and raise maths |
| `Shared/BladeMesh` | Client-side EditableMesh blade: ridge band and bevels (band across the blade's own width from `blueprint.ridge`, smoothed), sharpness, accent lines (ridge lines or a single shinogi, fuller, a katana's yokote; tinted from the blade colour), pointed tips |
| `Remotes/` | FinishBlade, AttachHilt, GetSmithState, SmithState, ForgePut, ForgeTake, DisplaySword, Offer, RespondOffer, ShopNotice |

## ServerScriptService

| Path | What it is |
|---|---|
| `SmithyCore` (module) | Per-player state (ingots, blades, swords, completed count), coins in leaderstats; builds ingot Tools and sword Tools/Models; re-gives items on respawn. `publicState` swords include materialId / blueprintId / hiltId for the picker art |
| `SmithService` | FinishBlade (needs a hot ingot), AttachHilt (unlock check + seat bonus), GetSmithState |
| `ForgeService` | Ore Roller roll (max 6 carried); forge: 2 shared slots, 15 s, ForgePut / ForgeTake. `ForgeTimers` BillboardGui on `Forge.Base` stacks one "Iron · Heating" label (bar + seconds) per busy slot. Slot parts `ForgeSlot1/2` carry `Slot`, `OwnerId`, `Ready` attributes for the client |
| `ShopService` | 3 sword holders (DisplaySword, take back with F), price tags; customer NPCs (walk in, inspect, offer, haggle, timeout), coins on sale |

## StarterPlayerScripts (client)

| Path | What it is |
|---|---|
| `AnvilController` + `Modes/` (Silhouette = default: hammer, grind [4], heat + reheat [R]; Trace, Clicks, Points = guided). Strike point: blows move the blade (`focus(column, side, yaw?, roll?, time?)` sets a pose: slide, turn, flip) so the struck part sits under the `AnvilHammer` model at the anvil face's centre; Points (default for now) choreographs the poses under a fixed point (`strikeScreen`) | Anvil camera, input, panel, juice (sparks, clang, shake), hot-ingot picker → shape picker (replaces the old < > blueprint buttons), finish showcase (grind sharp + accent lines). Mode switcher (M) is test-only |
| `HiltBenchController` | E → picker "Choose a blade." → picker "Choose a hilt." → seat-the-hilt taps (Space / tap) → AttachHilt → toast |
| `ForgeController` | E: "Take out" when your ingot is ready (the prompt text switches), "Forge is full" toast when both slots are busy, else the picker of your cold ingots stacked by material; picking closes it, puts one in and toasts "Ingot loaded" |
| `ShopController` | "+ Display a sword" picker (sword cards with price), offer card, notices |
| `ItemPicker` (module) | The shared picker (vault: [[UI Design]]; Gotham font), built in code into its own `PickerGui`: station title + action line, grid of cards (3D item in a ViewportFrame or a blade silhouette, name, chip, ×qty; hover / gamepad focus = amber edge), close ring (B closes), blur + dim behind, empty state. Compact one-row layout when the screen is under 500 px tall. Also `toast(text, "warn"?)`. Used by the forge, anvil, holders and Hilt Bench |
| `SwordRenderer` | Draws the blade mesh on held and displayed swords |

## StarterGui

`AnvilHud` (anvil panel, tools incl. Reheat, hammers incl. Grind, mode button, hint, result banner), `AnvilPoints` (Points-mode circles), `HiltBenchHud` (only the Seat panel now), `ShopHud` (offer card, notices). The picker and toasts are built at runtime by `ItemPicker` (`PickerGui`).

## Workspace

`Smithy/` holds `OreRoller`, `Forge` (Base + HeatPrompt "Use forge"), `Anvil` (BladeMount, ForgePrompt, Clang sound), `HiltBench`, `DisplayRack` (Slots 1–3, each with a HolderPrompt). The blade on the anvil (`Blade`), the Trace guide and the `Customers` folder are created at runtime.

## Models (outside Studio)

`Models/SwordShop.bbmodel` (Blockbench source) and `Models/SwordShop.fbx` (import file, 1 unit = 1 stud): the shop cabin as 17 named meshes on one palette texture. Not imported into the place yet.

## Tests

`ServerStorage/Tests/AnvilSelfCheck`. Run `require(game.ServerStorage.Tests.AnvilSelfCheck)()` in the command bar. It covers blade maths, scoring, the bot smith per blueprint, server Finish checks, hilts, value, customers and material odds.

`ServerStorage/AnvilController_Backup` is the disabled pre-refactor controller. Safe to delete.

Related: [[Home]] · [[Roadmap]] · [[Create Swords! GDD]]

---
title: Code Map
status: current (2026-10-19, player plot v2)
tags: [code, architecture, create-swords]
type: "development"
updated: "2026-10-19"
---

# Code Map

Where everything lives in the Studio place (`goku19876's Place: 10172026_1`) and how the pieces connect. The code exists only in the place file (no Rojo/Git; see [[Design/Decisions Log|Decisions Log]]), so **save the place** after every session. The design behind it is in [[Design/Game Design Document|Game Design Document]]; day-by-day history is in [[Sessions/2026-10-17]].

## How a sword is made (data flow)

```
Ore Roller lever (hold E) ──(ForgeService)──► every empty stand spins → result waits on the stand ─E "Collect ore"─► cold ingot (Tool)
   Forge picker ─ForgePut─► slot (timer label) ─E "Take out" / ForgeTake─► hot ingot (Tool)
Anvil (AnvilController) ── choose hot ingot → blueprint ─BeginForge(ingotId, blueprintId)─► SmithService (start time)
   12 untimed strikes (BladeCore) → 90%, auto-finish at the anvil
   Finish ─FinishBlade("Forge", blueprintId, savedState, ingotId)─► SmithService
      ForgeCheck validates the forged state and minimum time; anvil output cannot exceed 90%; ingot used up → carried blade
Hilt Bench (HiltBenchController) ── pick blade + hilt, seat it (3 taps)
   ─AttachHilt(bladeId, hiltId, goodTaps)─► SmithService → completed sword (Tool)
Etching Table (EtchingTableController) ── pick sword + pattern ─EtchSword(swordId, etchId)─► EtchService → sword.etch, rebuilt Tool (+ bonus)
Optional final Polishing Station ── pick completed sword ─BeginPolish / PolishSword─► PolishService → improved sword, up to 100%
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
| `Shared/ForgeCheck` | Server validation by BladeCore replay. Current station split: SmithService refuses anvil output above 90%; `evaluatePolish` validates saved refinement and minimum time at the dedicated Polishing Station (details below). Older combined forging/grinding timing descriptions are historical |
| `Shared/Materials` | 13 materials, 5 rarities: roll odds, value multiplier, colour |
| `Shared/Hilts` | 6 hilts (+0–40%, unlock by swords completed), seat-the-hilt bonus. Since 2026-10-20 each recipe may name a `tsuba` (Leather = Kaku, Iron = Mokko, Bronze = Kiku, Gold = Kumo, Gem = Kuruma; Wooden keeps the round template guard), and `Hilts.dress(hilt, etch?)` returns the hilt's template parts with their colours (used by `SmithyCore` for swords and `ItemPicker` for card art). `Hilts.TEMPLATE` = `ReplicatedStorage.SwordParts.KatanaHilt` |
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
| `SmithyCore` (module) | Per-player state (ingots, blades, swords, completed count), coins in leaderstats; builds ingot Tools and sword Tools/Models; re-gives items on respawn. **Hilt (2026-10-19):** `buildSword` keeps an invisible `Handle` (1.082 × 0.15 cylinder, from the template's `GripLength`) and `dressHilt` clones the 8 MeshParts of `ReplicatedStorage.SwordParts.KatanaHilt` (moved from ServerStorage 2026-10-20 so clients can draw it) onto it (stored relative to the Handle frame: X toward the blade, Z the edge side), welded and coloured per recipe: `Ito` = grip, `Fittings`/`Rim` = guard, `Kashira` = pommel or guard; `Same`, `Tsuba`, `Band`, `Habaki` keep fixed colours. `Habaki` was resized 2026-10-20 to 0.17 × 0.12 × 0.052 (local X width, Y along the blade, Z thickness), centre X 0.673. `BladeOffset` = 0.613 (template attribute). `Hilts` guard widths and pommel sizes are no longer used for the look. **Etch (prototype, 2026-10-19):** optional `Sword.etch = { pattern, body, flame, guard? }` → attributes `Etch`, `EtchBody`, `EtchFlame`; if `SwordParts.<guard or pattern>Guard` exists (e.g. `FlameGuard`, asset 85043523139786) it replaces `Tsuba` and `Rim`, coloured by part-name suffix Core = body, Rim = flame, Inner = flame lightened. The pre-hilt module is kept as `ServerStorage.Legacy.SmithyCore_beforeKatanaHilt`. Mesh source: Open Cloud asset 74688698547736 from `Models/Hilts/KatanaHiltGame.fbx`. `publicState` swords include materialId / blueprintId / hiltId for the picker art |
| `SmithService` | BeginForge (notes ingot, blueprint, start time), FinishBlade (mode "Forge" only, via ForgeCheck; since 2026-10-20 it refuses any blade above 90%, as polishing is the Polishing Station's job; blade stores `refinement`), AttachHilt (unlock check + seat bonus), GetSmithState. **Studio only:** `ServerStorage.DevGiveHotIngot` BindableFunction hands a player a hot ingot for playtests |
| `ForgeService` | Ore Roller (2026-10-20): the `RollPrompt` lever ("Pull lever", hold 1.5 s) spins every empty `OreRoller.Stand<n>` (any model with an `Ore` part): ore + `OreChunk*` flicker through `Materials.list`, slowing, for 2.6 s, then stop on `Materials.roll` with a pop, rarity-coloured `Sparkle*`, an `OreLabel` billboard (name + rarity) and the stand's `Pedestal.CollectPrompt` (E). Only the roller can collect (max 6 carried ingots); occupied or spinning stands are skipped; empty stands hide their ore. Pre-change script kept as `ServerStorage.Legacy.ForgeService_beforeOreStands`; forge: 2 shared slots, 15 s, ForgePut / ForgeTake. `ForgeTimers` BillboardGui on `Forge.Base` stacks one "Iron · Heating" label (bar + seconds) per busy slot. Slot parts `ForgeSlot1/2` carry `Slot`, `OwnerId`, `Ready` attributes for the client |
| `ShopService` | 3 sword holders (DisplaySword, take back with F), price tags; customer NPCs (walk in, inspect, offer, haggle, timeout), coins on sale. Customers appear at `Village.CustomerSpawn`, walk through `DisplayRack.EntryPoint` and stand at the chosen holder's `DisplayRack.InspectPoint1..3` (invisible marker parts), walking straight lines between them |

## StarterPlayerScripts (client)

| Path | What it is |
|---|---|
| `AnvilController` (rewritten 2026-10-19; automatic 90% finish since the recorded 2026-10-20 change) | E → hot-ingot picker → blueprint picker → BeginForge. Strike circle (Space / click / tap, one buffered tap), hammer behind the anvil, blade slides/turns/flips, eased local deformation, sparks, clang and shake. After 12 strikes the blade cools and auto-finishes at 90%; no grinding interaction at the anvil. Panel shows quality and strike/stage; overhead camera frames the blueprint. Old modes are in `ServerStorage.Legacy.AnvilController_PrototypeModes`; pre-polishing controller is preserved separately |
| `HiltBenchController` | E → picker "Choose a blade." → picker "Choose a hilt." → seat-the-hilt taps (Space / tap) → AttachHilt → toast |
| `EtchingTableController` (2026-10-20) | E at `Smithy.EtchingTable.Top.EtchPrompt` → picker "Choose a sword." (inventory swords; etched ones say so) → picker "Choose a pattern." (`Shared/Etches`) → `EtchSword` → toast. Free and instant for now |
| `EtchService` (server, 2026-10-20) | `Remotes.EtchSword(swordId, etchId)`: within 12 studs of the table, sets `sword.etch` from `Shared/Etches`, swaps the sword's Tool (backpack or hand) for a rebuilt one, pushes state |
| `Shared/Etches` (2026-10-20) | Etch patterns: `Flame` (+15% value, body/flame colours). `SmithyCore.swordValue` adds the bonus; `publicState` swords carry `etch` |
| `ForgeController` | E: "Take out" when your ingot is ready (the prompt text switches), "Forge is full" toast when both slots are busy, else the picker of your cold ingots stacked by material; picking closes it, puts one in and toasts "Ingot loaded" |
| `ShopController` | "+ Display a sword" picker (sword cards with price), offer card, notices |
| `ItemPicker` (module) | The shared picker (vault: [[Art/UI Design|UI Design]]; Gotham font), built in code into its own `PickerGui`: station title + action line, grid of cards (3D item in a ViewportFrame or a blade silhouette; hilt cards show the real dressed hilt and guard from `Hilts.dress`, tipped so the guard face shows, with `SwordParts` preloaded; blade and sword cards with a `blueprintId` draw that blueprint's real finished blade (`BladeView`, 1.5× wider for readability, on a shared square-root scale so a tantō reads short), swords with their real hilt, and the Etching Table's pattern card shows the etch on the chosen sword; these EditableMeshes are freed whenever the window is rebuilt or closed, name, chip, ×qty; hover / gamepad focus = amber edge), close ring (B closes), blur + dim behind, empty state. Compact one-row layout when the screen is under 500 px tall. Also `toast(text, "warn"?)`. Used by the forge, anvil, holders and Hilt Bench |
| `SwordRenderer` | Draws held and displayed blades with BladeCore + BladeView (one EditableMesh per visible sword for now). Swords with an `Etch` attribute also get a `BladeEtch` skin (prototype, 2026-10-19), welded with the blade |
| `Shared/BladeEtch` (prototype, 2026-10-19) | Client etch skin: a two-colour EditableMesh just above both blade faces, built from the same BladeCore station params (sampled ~4× finer) so it follows any blueprint's forged/ground shape. `PATTERNS.Flame(sw)` gives how far the band colour reaches from the edge at `sw` local blade widths from the base. Since v4 (2026-10-20) it is the reference-matched red band: even humps of 0.14 width around 28%, spaced 0.75–1.05 widths. Columns run from a 3.2% edge line to a 3.2% spine line, so bare steel shows as bright edges; per-vertex colours shade the bevel (12 cached steps). Pre-v4 module kept as `ServerStorage.Legacy.BladeEtch_beforeBand`. `build(params, pattern, body, flame)` returns the MeshPart and its EditableMesh. See [[Art/Flame Etch]] |

## StarterGui

`AnvilHud` (anvil panel, hint, result banner; Tools, Hammers and ModeButton hidden), `AnvilPoints` (unused; strike ring built at runtime in `StrikeRingGui`), `HiltBenchHud` (Seat panel) and `ShopHud` (offer card, notices). `GrindMap` belonged to the earlier anvil flow; current polishing has its own controller and progress strip (see Polishing Station below). The picker and toasts are built by `ItemPicker` (`PickerGui`).

## Workspace

`Smithy/` holds `OreRoller`, `Forge` (Base + HeatPrompt "Use forge"), `Anvil` (BladeMount, ForgePrompt, Clang sound), `HiltBench`, `DisplayRack` (Slots 1–3, each with a HolderPrompt). The blade on the anvil (`Blade`), the Trace guide and the `Customers` folder are created at runtime.

Rebuilt 2026-10-19 in the Japanese style ([[Art/Smithy Redesign|Smithy Redesign]]). Each station keeps the parts scripts read, and its look lives in a `Dress` model (plus `Stand1` on the roller):

| Station | Parts scripts read (don't move or rename) | Free to restyle |
|---|---|---|
| `Forge` | `Base` (invisible box, exact old size and CFrame; ForgeService places `ForgeSlot1/2` and `ForgeTimers` from it) + `HeatPrompt` | Since 2026-10-20: `Model3D` (the Blender mid-high forge, turned to face +Z; its trays sit under `ForgeSlot1/2`); `Fire` is now invisible and keeps only its PointLight, inside the new chamber. `Chimney` and `Dress` removed |
| `OreRoller` | `Machine` (invisible prompt part at the knob, x −8.5 since 2026-10-20) + `RollPrompt`; `Lever` (2026-10-20, Allen's reroll-lever reference: sage base, two half-disc wooden cheeks, `Arm` + `Knob` welded to the anchored invisible `ArmPivot` at the hinge, rest −25°, pulled +35°; `LeverAnimator` swings it while E is held). `Stand1` was scaled 1.35× and its `Ore` enlarged (about 2.3 × 1.2 × 2.3) so the result reads from across the room; `Stand<n>` models with `Ore` (+ optional `OreChunk*`, `Sparkle*`, `Pedestal`). ForgeService finds them by name, so a new stand is just another model | Since 2026-10-20: `Lever` (the Blender lever model on `Machine`, which is now invisible); `Stand1` holds the textured Blender stand: `Ore` (the roll recolours it), `Pedestal` (the stone base, carries `CollectPrompt`), wood/iron parts and the old `Sparkle*`. The shrine `Dress` and the old chunks are gone |
| `Anvil` | `BladeMount`, `Face` + `ForgePrompt`, `Clang` | Since 2026-10-20: `Model3D` (Blender hornless block on a low timber base). The whole station dropped 0.7, so `Face` (now invisible) tops out at 2.5 = 2.3 above the floor, flush with the new striking face. `Stump`, `Waist`, `Base` and `Dress` removed |
| `HiltBench` | `Top` + `HiltPrompt` (invisible since 2026-10-20, just under the new worktop) | `Model3D`: the Blender bench (5.0 × 2.4, worktop 2.9 above the floor) |
| `EtchingTable` (2026-10-20) | `Top` + `EtchPrompt` (EtchService measures reach from `Top`) | `Dress` (27 parts at x 11, z −30: worktop at 2.9 like the Hilt Bench, iron tray with slate bath and a half-etched blank, brush pot, three jars, andon lamp) |
| `DisplayRack` | `Slots/Slot1..3` + `HolderPrompt`: latest recorded slots are turned X down and raised to y 4.75, with the guard on the pad 3.95 above the floor and broad blade face toward each `InspectPoint`. Plan coordinates retained from the storefront layout: Slot1 x −39.5 / z 4, Slot2 x −25.5 / z 4, Slot3 x −39.5 / z −7. Invisible `EntryPoint` and `InspectPoint1..3` guide ShopService from road → entry → chosen holder and back. Keep these routes clear; the earlier y 2.92 / blade-up placement is superseded | `Holders/Holder1..3`: Blender universal holders facing their InspectPoints. Old `Dress` pedestals removed |

Plan positions from the [[Art/Player Plot Review|Player Plot Review]] pass: Forge x 2 / z −29.3 against the back wall, Anvil x 2 / z −16 on open floor about 9 studs in front, OreRoller x −9 / z −28.57, HiltBench x 20 / z −30. Vertical placement changed during Blender import (especially the lowered anvil); use current station contracts above rather than old pivot heights. Whole-station moves require checking prompts, mounts, camera and customer routes.

`Plot/` (2026-10-19, no scripts) is the player property, built to the L-shaped concept ([[Art/Japanese Village Concept Art|Japanese Village Concept Art]]) and widened after the review. Plot bounds x −50…76, z −48…30 (126 × 78 studs):

- `Pavilion`: the crafting wing, 50 × 28 studs at x −19…31, z −32…−4 (replaced the shallow 41 × 17 `Workshop`, archived as `ServerStorage.Archive.Workshop_v1`). Four front posts with 14–18 stud openings, open east side toward the lawn, `Floor` (earth floor plus a `WorkApron` running out into the courtyard), `Frame`, `Walls` (back and west), `Roof` (gable, ridge along X at z −18, 3-stud eaves), `Lanterns`. No beams cross the anvil bay below y 11.

- `Storefront`: the shop wing at x −45…−20, z −22…16, with `Frame`, `Walls`, `Roof` (gable, ridge along Z), `Front` (noren, crest), `Lanterns` and `Interior` (counter, drawer chest, sword wall racks, pots). The doorway (x −38.5…−26.5) faces the road. The 刀鍛冶 `Signboard`/`SignFrame` (under `Storefront.Front`) sit on its front gable. Holders stand in two columns either side of a clear aisle to the counter.
- `Yard`: `PlotPad` grass, `Courtyard` (three pieces around the work apron) and `FrontYard` paving, `GatePath`, `LawnCurb`. The lawn east of x 37.8, and the strip behind the pavilion, are the expansion space.
- `Fence` (entrance gap x −36…−29 at z 30; front and back runs own the corners, side runs stop short), `StoneLanterns` (gate, corners, either side of the work apron; PointLights), `Greenery` (bamboo groves at corners and boundaries, rocks, shrubs, pots), `IngotShelf` (decor on the pavilion's west wall by the ore shrine).

**No Z-fighting (build rule):** ground layers start at y 0 and never share a top height where they overlap: Baseplate 0, `PlotPad` 0.1, floors/paving/road 0.2, road edges 0.3, curbs 0.4. Where two parts meet, one face sits at least 0.04 proud of the other. On 2026-10-19 a coplanar-face check over `Plot`, `Smithy` and `Village` (axis-aligned block parts) found 157 overlaps and nudged 180 faces outward by 0.04 (2 by hand in the forge chamber); none were left. Rerun that check after building.

`Village/` holds the shared `Road` (z 34…46) and `CustomerSpawn` (−32.5, 3, 40). `SpawnLocation` is in the courtyard at (0, 0.2, 16), hidden. `ServerStorage.Archive` holds the old prototype blocks (`store`, `creation area`, two slabs), the first ground pieces (`Workshop_PlotPad`, `Workshop_FrontYard`, `Workshop_ApproachPath`) and `Workshop_v1`. The Baseplate is grass. Still one plot: every station is the single shared `Smithy`; per-player plots need the controllers and services to look up the player's own plot instead of `workspace.Smithy`.

## Models (outside Studio)

`Models/Archive/SwordShop.bbmodel` (Blockbench source) and `Models/Archive/SwordShop.fbx` (import file, 1 unit = 1 stud): the historical medieval cabin, 17 named meshes on one palette texture. Never imported; superseded by `Workspace.Plot`.

## ServerStorage.Legacy

`SharedV1` is a frozen copy of the shared modules from before the 2026-10-19 rewrite (old Blueprints, ShapingModes, FinishCheck…) and `AnvilController_PrototypeModes` (disabled) is the old anvil with its Silhouette/Trace/Clicks/Points modes. Kept for reference and for `AnvilSelfCheck`.

## Tests

- `ServerStorage/Tests/BladeCoreSpec` (with `BladeGolden`) tests the BladeCore port; see `Prototypes/tanto-forge/roblox/README.md`.
- `ServerStorage/Tests/ForgeCheckSpec`: the new blueprints and the server's Finish check (35 checks). Run `print(require(game.ServerStorage.Tests.ForgeCheckSpec)())` in the command bar.
- `ServerStorage/Tests/AnvilSelfCheck` now checks the frozen `Legacy.SharedV1` copy (old blade maths, prototype modes, customers, materials, value). Run `require(game.ServerStorage.Tests.AnvilSelfCheck)()`.

`ServerStorage/AnvilController_Backup` is the disabled pre-refactor controller. Safe to delete.

Related: [[Home]] · [[Development/Roadmap|Roadmap]] · [[Design/Game Design Document|Game Design Document]]

## Polishing Station (2026-10-20)

| Piece | What it does |
|---|---|
| `Workspace.Smithy.PolishStation` | `Model3D` (Blender bench with felt pads, whetstones, water-cooled stone wheel, bucket; asset 86416596849647) at x 27, z −30 right of the Hilt Bench; `Top` (invisible) + `PolishPrompt`; `BladeMount` (invisible, 25.3, 3.22, −29.85): the blade lies along +X from here, edge toward the player |
| `PolishController` (client) | E → picker "Choose a sword to polish." (finished swords with their %; fully polished ones locked) → BeginPolish → the sword's blade on the bench, top-down camera, hold and drag along the edge (same `BladeCore.applyGrind` as the anvil had), progress strip, Save → PolishSword / Leave (Q) |
| `PolishService` (server) | `Remotes.BeginPolish(swordId)` (within 12 studs, notes the start time) and `PolishSword(swordId, saved)`: `ForgeCheck.evaluatePolish` replays it (all strikes, refinement never lower than stored, at least `MIN_SECONDS_FULL_GRIND` × the newly polished share), then updates the sword's refinement, grade, percent, multiplier and rebuilds its Tool |
| `ForgeCheck.evaluatePolish` | Pure check, covered by `ServerStorage.Tests.ForgeCheckSpec` (90% → 100%, instant polish refused, can't undo polish, no-change save allowed) |
| `SmithyCore.publicState` | swords now also carry `percent` and `refinement` |
| `LeverAnimator` (server) | RollPrompt hold → `ArmPivot` tweens forward over the hold; let go early → springs back; completed → stays down 0.45 s then springs back |

Backups in `ServerStorage.Legacy`: `ForgeCheck_beforePolishStation`, `SmithService_beforePolishStation`, `ForgeCheckSpec_beforePolishStation`, `AnvilController_beforePolishStation`.

## Growth systems — design only

[[Design/Workshop Growth]] records employees, courier orders, weather traffic bonuses and indoor roof visibility. No scripts/services for these new systems were inspected or recorded as implemented during this documentation pass.

- Approved employee professions: furnace operator, smith, finisher, stocker and cashier. Finisher combines hilt assembly/optional polishing; stocker carries ready stock to empty retail holders. Bare-blade and finished-sword racks are separate planned handoffs; finished stock needs sale readiness and reservation rules before automated listing. No paths or services for these planned systems are claimed as existing here.

- Employee forging introduces sub-90% blades, rack ownership and player resumption at the anvil; the existing guided-player pipeline currently assumes completed forging at 90%. Data, replay/value rules and recovery need an explicit extension before implementation.
- Worker polishing ceilings must coexist with the player's ability to finish up to 100% at the Polishing Station. Preserve the separate forging/polishing stages.
- Delivery orders are a separate board/courier flow; they must not replace tutorial/direct-commission picker hand-in.
- Weather changes traffic above baseline only and must preserve the first-sale arrival gate.
- Roof fade/cutaway is a requested presentation feature; a local visual change is recommended, not server-wide removal of roof parts.

## Plot after the building redesign (2026-10-20)

`Plot.Storefront.Shell` (Blender low-poly shop, precise collision) replaced `Frame`, `Walls` and `Roof`. `Plot.Pavilion` is now `Plot.Courtyard`: `Paving` (stone flags, x −14..42, z −34..2.5) plus `StoneLanterns`. All crafting stations moved +8 in x onto it; `DisplayRack` stays in the shop. `Plot.StoneLanterns` and `Courtyard.StoneLanterns` use the Blender lantern (light on `StoneLantern_paper`). `Plot.Greenery.Bamboo1..12` are the three Blender variants. Source models live in `ServerStorage.Buildings3D`. See [[Art/Building Redesign]].

## Sword meshes, ingot ore and station order (2026-10-20)

- `Shared/SwordMeshCache` (client): finished swords share EditableMeshes. Key = blueprint + the blade's average polish rounded to 0, 0.5 or 1 (+ etch pattern). Etch meshes are colour-neutral (white band); the clone's `Color` is the band colour. `blade(bp, refinement)` / `etch(bp, refinement, pattern, body)` return a Clone plus a key; `release(key)` frees the mesh with its last clone. `SwordRenderer` and `ItemPicker` card art use it; the anvil and Polishing Station keep their own live `BladeView`.
- **Budget facts measured in Studio:** destroying an EditableMesh makes MeshParts built from it vanish, so meshes must stay alive. The client budget counts meshes (empty or 5k-vertex ones both stopped at the same count), so sharing, not vertex trimming, is what helps. The worst case is now 9 blade + 9 etch meshes.
- `OreRoller.Stand1.Ore` is now an ingot MeshPart (asset 74129223491846, 2.3 × 0.75 × 1.2). ForgeService recolours and pops it as before. The old rock is in `ServerStorage.Legacy.OreRock_beforeIngot`.
- **Station order** (Allen: left to right, no signs) along the back of the courtyard (z ≈ −29), left to right as seen from the courtyard, starting beside the shop: 1 Ore Roller (stand x −9.5, lever −5.6), 2 Forge 2, 3 Anvil 10, 4 Hilt Bench 18.5, 5 Etching Table 26, 6 Polishing Station 34.5. `Plot.IngotShelf` stands behind the forge and anvil (x 6). The step signs were removed. Backup of the earlier layout: `ServerStorage.Legacy.Smithy_beforeStepOrder`.
- **Fence parked (2026-10-20):** at Allen's request ("remove the fences for now until we settle on our plot design"), `Plot.Fence` (119 parts) moved whole to `ServerStorage.Legacy.Fence_parked`. To bring it back, rename it `Fence` and parent it to `Workspace.Plot`.
- **Forge capacity (2026-10-20):** `ForgeService.SLOT_OFFSETS` has one slot (the left tray, x −0.45), so the forge heats one ingot at a time; the ForgeTimers board sizes itself from the slot count. Backup: `ServerStorage.Legacy.ForgeService_beforeOneSlot`. Not playtested yet.

## Changes 2026-10-20 (later batch)

- **Quality:** `ForgeCheck` grades every finished blade `forPercent(MAX_QUALITY)` (100%, ×2.0); results carry `polished` and `share`. `SmithyCore.POLISH_BONUS = 0.10` joins the finish bonuses in `swordValue` when `blade.polished`; `bladeName` adds " (Polished)". `SmithService.FinishBlade` refuses a result with `share > 0`. `PolishService` sets `refinement` and `polished`.
- **AnvilController:** the silhouette is drawn straightened (distance along the blade, offset across) against `blade.shapes[4]`; `mapGui` stays off; after the showcase it calls `leave()` so the view closes. Backup `Legacy.AnvilController_beforePanelFix`.
- **HiltBenchController.seatHilt(blade, hilt):** `HiltSeatGui` ring on the kashira; 3 knocks (click or Space) slide the hilt (GAP 1.4) onto the blade on `HiltBench.Model3D.Top`; returns `Hilts.SEAT_TAPS`.
- **Anvil:** `Smithy.Anvil.Model3D.AnvilBody` is one mesh (`anvil_one_piece()` in `build_stations.py`, asset 114071521909816); `Face`, `BladeMount`, `Clang` kept.
- **ForgeService:** a stand rolls when it isn't spinning and is empty or owned by the player, so re-rolls are unlimited; `spin()` clears `materialId` first.
- **Shops:** `Plot.Storefront.Shell` is the widened Upgraded Store (asset 84499583042886, 31 × 38) with a `Roof` model and an `InsideZone` part, tagged `HidesRoof`. The Starter Shop (73411167806206, 24 × 14) is staged in `ServerStorage.Buildings3D.StarterShop`, not placed. Backup `Legacy.Storefront_beforeWider`.
- **RoofHider** (StarterPlayerScripts): for each `HidesRoof` model, fades `Shell.Roof` parts (LocalTransparencyModifier) while your HumanoidRootPart is inside `InsideZone`.
- **Racks:** `Smithy.IngotRack` (was `Plot.IngotShelf`; `Slots/Slot1..12`, `Shelf1.RackPrompt`) and `Smithy.SwordRack` (`Slots/Slot1..6`, `Plinth.RackPrompt`). `RackService` handles `Remotes.RackAction(which, "list"|"store"|"take", id)`: caps 12 ingots / 6 swords on the racks and 6 carried, reach 12 studs; stored items leave the player's inventory through `SmithyCore.takeIngot/takeSword`. `RackController` opens the item picker with "Store" (carried) and "Take" (rack) cards. Racks are session-only like the rest of the inventory.
- **Hilt seat clicks (fix 2026-10-20):** `HiltSeatGui.Ring` is a plain `Frame`; knocks come from `UserInputService.InputBegan` (MouseButton1 or Touch within 70 px of the ring, like the anvil's `nearRing`) or Space/ButtonA.
- **Quick thoughts batch (2026-10-20):**
  - **Forge:** `Model3D` has one tray (Tray2 parts removed, Tray1 centred), `SLOT_OFFSETS = { CFrame.new(0, 1.12, 1.55) }`. The `ForgeTimers` panels hold only a `Time` label: "12s", then a green "Ready!". Backups `Legacy.Forge_beforeOneTray` and `ForgeService_beforeTimerOnly`.
  - **Anvil:** `AnvilHud.Bottom.Leave` text is "Cancel"; Q still cancels.
  - **Station order:** Hilt Bench, Polishing Station (x ≈ 26.8), Etching Table (x ≈ 34.5) last.
  - **Ore stand:** `OreRoller.Stand1` is three cylinders (`Base`, `Pedestal`, `Cap`, 4.1 studs wide, top at y 2.32) plus `Ore`; textured stand and sparkles removed (backup `Legacy.OreStand1_beforeSimple`). `ForgeService.spin` floats the ore `FLOAT_HEIGHT` 1.3 above its rest CFrame, bobbing and turning on Heartbeat, then tweens it down with a bounce.
- **Later fixes (2026-10-20):**
  - `Shell.Roof` now also holds `Storefront_Roof_timber` (eave and tie beams), so `RoofHider` fades the beams too.
  - `RackController`: picking a card closes the picker; only a failure shows a toast.
  - `ForgeService.spin`: no "Rolling…" label and no result toast; the stand's label appears with the result.
  - `ItemPicker` no longer draws `spec.subtitle` or `spec.emptyHint` (callers still pass them; ignored). The anvil's idle hint is "Click the anvil" with hot ingots, nothing otherwise. Backups `Legacy.ItemPicker_beforeLessText`, `RackController_beforeClose`.  - No habaki (Allen 2026-10-20): `SwordParts.KatanaHilt` has no `Habaki` part and `BladeOffset` is 0.58, so the blade root sits inside the guard. See [[Art/Katana Hilt]].
  - `ForgeTimers` billboard `StudsOffset` is (0, 6.6, 0): centre at y 7.9, above the chimney (top y 6.32), so the furnace no longer hides it.

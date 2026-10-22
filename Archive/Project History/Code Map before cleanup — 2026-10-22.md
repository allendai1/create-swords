---
title: Code Map before cleanup — 2026-10-22
status: archived — historical snapshot; superseded by the active note
tags: [code, architecture, create-swords]
type: "development"
updated: 2026-10-22
---

# Code Map

Historical snapshot retained during the 2026-10-22 cleanup. Current guidance: [[Development/Code Map]]. Older rules and completion states below may be superseded.

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
| `WallHolder` (2026-10-20) | The wall sword holder (asset 82281277381485, 212 tris): `Holder_*` MeshParts plus invisible `Origin` (PrimaryPart, on the plaster face at floor level; +X along the wall, +Z out) and `Mount` (where the sword's Handle goes: grip centre at (−0.58, 4.4, 0.56), blade along +X, edge up). Cloned by ShopService and ShopController's preview |

## ServerScriptService

| Path | What it is |
|---|---|
| `SmithyCore` (module) | Per-player state (ingots, blades, swords, completed count), coins in leaderstats; builds ingot Tools and sword Tools/Models; re-gives items on respawn. **Hilt (2026-10-19):** `buildSword` keeps an invisible `Handle` (1.082 × 0.15 cylinder, from the template's `GripLength`) and `dressHilt` clones the 8 MeshParts of `ReplicatedStorage.SwordParts.KatanaHilt` (moved from ServerStorage 2026-10-20 so clients can draw it) onto it (stored relative to the Handle frame: X toward the blade, Z the edge side), welded and coloured per recipe: `Ito` = grip, `Fittings`/`Rim` = guard, `Kashira` = pommel or guard; `Same`, `Tsuba`, `Band`, `Habaki` keep fixed colours. `Habaki` was resized 2026-10-20 to 0.17 × 0.12 × 0.052 (local X width, Y along the blade, Z thickness), centre X 0.673. `BladeOffset` = 0.613 (template attribute). `Hilts` guard widths and pommel sizes are no longer used for the look. **Etch (prototype, 2026-10-19):** optional `Sword.etch = { pattern, body, flame, guard? }` → attributes `Etch`, `EtchBody`, `EtchFlame`; if `SwordParts.<guard or pattern>Guard` exists (e.g. `FlameGuard`, asset 85043523139786) it replaces `Tsuba` and `Rim`, coloured by part-name suffix Core = body, Rim = flame, Inner = flame lightened. The pre-hilt module is kept as `ServerStorage.Legacy.SmithyCore_beforeKatanaHilt`. Mesh source: Open Cloud asset 74688698547736 from `Models/Hilts/KatanaHiltGame.fbx`. `publicState` swords include materialId / blueprintId / hiltId for the picker art |
| `DevTools` (Studio only, 2026-10-20) | `Remotes.DevAddCoins` adds 1,000 coins; `Remotes.DevGiveSwords` gives one finished tantō, wakizashi and katana (100% forged, unpolished, random material, Wooden hilt) built like SmithService's. Does nothing on a live server (`RunService:IsStudio()`). The client `DevPanel` (StarterPlayerScripts, also Studio only) shows "+1,000 coins" and "+3 swords" buttons at the bottom left |
| `SmithService` | BeginForge (notes ingot, blueprint, start time), FinishBlade (mode "Forge" only, via ForgeCheck; since 2026-10-20 it refuses any blade above 90%, as polishing is the Polishing Station's job; blade stores `refinement`), AttachHilt (unlock check + seat bonus), GetSmithState. **Studio only:** `ServerStorage.DevGiveHotIngot` BindableFunction hands a player a hot ingot for playtests |
| `ForgeService` | Ore Roller (2026-10-20): the `RollPrompt` lever ("Pull lever", hold 1.5 s) spins every empty `OreRoller.Stand<n>` (any model with an `Ore` part): ore + `OreChunk*` flicker through `Materials.list`, slowing, for 2.6 s, then stop on `Materials.roll` with a pop, rarity-coloured `Sparkle*`, an `OreLabel` billboard (name + rarity) and the stand's `Pedestal.CollectPrompt` (E). Only the roller can collect (max 6 carried ingots); occupied or spinning stands are skipped; empty stands hide their ore. Pre-change script kept as `ServerStorage.Legacy.ForgeService_beforeOreStands`; forge: 2 shared slots, 15 s, ForgePut / ForgeTake. `ForgeTimers` BillboardGui on `Forge.Base` stacks one "Iron · Heating" label (bar + seconds) per busy slot. Slot parts `ForgeSlot1/2` carry `Slot`, `OwnerId`, `Ready` attributes for the client |
| `ShopService` | Any number of sword holders (DisplaySword, take back with F), price tags; customer NPCs (walk in, inspect, offer, haggle, timeout), coins on sale. Slots 1–3 are the floor holders (`DisplayRack.InspectPoint1..3`). **Wall holders (2026-10-20):** each `Plot.Storefront.WallSpots.Spot<n>` has a `PromptAt.BuyPrompt` ("Buy sword holder", `HOLDER_PRICE` = 100 coins, hold 0.5); buying spends coins (`SmithyCore.spendCoins`), clones `ReplicatedStorage.WallHolder` onto the spot (`DisplayRack.Holders.WallHolder<n>`), adds `DisplayRack.Slots.Slot<n>` at the template's `Mount` with a cloned `HolderPrompt`, and marks the spot `Bought`. Each slot has a `route`: floor holders walk straight to their InspectPoint; wall holders go along the centre aisle (EntryPoint's x) to the nearest clear row in `AISLE_ROWS` (z 11, −1.5, −12), across, then to 3.5 studs in front of the rack, and walk it back out. Bought holders are shared and session-only. Customers appear at `Village.CustomerSpawn` and walk through `DisplayRack.EntryPoint`. Backup `Legacy.ShopService_beforeWallHolders` |

## StarterPlayerScripts (client)

| Path | What it is |
|---|---|
| `AnvilController` (rewritten 2026-10-19; automatic 90% finish since the recorded 2026-10-20 change) | E → hot-ingot picker → blueprint picker → BeginForge. Strike circle (Space / click / tap, one buffered tap), hammer behind the anvil, blade slides/turns/flips, eased local deformation, sparks, clang and shake. After 12 strikes the blade cools and auto-finishes at 90%; no grinding interaction at the anvil. Panel shows quality and strike/stage; overhead camera frames the blueprint. Old modes are in `ServerStorage.Legacy.AnvilController_PrototypeModes`; pre-polishing controller is preserved separately |
| `HiltBenchController` | E → picker "Choose a blade." → picker "Choose a hilt." → seat-the-hilt taps (Space / tap) → AttachHilt → toast |
| `EtchingTableController` (2026-10-20; show 2026-10-21) | E at `Smithy.EtchingTable.Top.EtchPrompt` → picker "Choose a sword." (etched swords locked) → picker "Choose a pattern." (`Shared/Etches`: Flame, Eclipse) → `EtchPlayback.prepare` (if the look can't be built, nothing is requested) → `EtchSword` → on acceptance the show on the player's own table: 3.0 s drawing + 0.4 s to look, steep station camera, player frozen, `EtchHud` close ring; Q / Backspace / B leave early; death, character removal, the table leaving or a drawing error end it; a request token drops stale responses. The etch stands however the show ends. See [[Art/Animated Blade Etching#Built (2026-10-21)]] |
| `EtchPlayback` (module, 2026-10-21) | The show, making no mesh of its own: the sword copy (cached blade; cached finished etch held as proof; a share of the overlay with a private blank `EtchCanvas` as its texture, drawn by strokes or, for Flame, as a band), the hilt dressed for the new etch, a stylus with sparks and glow; lies flat on the worktop, edge toward the player, demo tray hidden locally. `step(p)`, `cameraCFrame(fov, viewport)`, `destroy()` (frees only its own things), `count()` |
| `EtchService` (server, 2026-10-20) | `Remotes.EtchSword(swordId, etchId)`: within 12 studs of the table, refuses a sword that's already etched (one etch per sword, 2026-10-21), sets `sword.etch` from `Shared/Etches`, swaps the sword's Tool (backpack or hand) for a rebuilt one, pushes state |
| `Shared/Etches` (2026-10-20) | Etch patterns: `Flame` (+15% value, body/flame colours). `SmithyCore.swordValue` adds the bonus; `publicState` swords carry `etch` |
| `ForgeController` | E: "Take out" when your ingot is ready (the prompt text switches), "Forge is full" toast when both slots are busy, else the picker of your cold ingots stacked by material; picking closes it, puts one in and toasts "Ingot loaded" |
| `ShopController` | "+ Display a sword" picker (sword cards with price), offer card, notices. Binds every `Slot<n>` in `DisplayRack.Slots` as it appears (bought wall holders included); while a wall spot's buy prompt shows, a see-through `WallHolder` previews where it would go (spots bound on ChildAdded too, for streaming). Backup `Legacy.ShopController_beforeWallHolders` |
| `ItemPicker` (module) | The shared picker (vault: [[Art/UI Design|UI Design]]; Gotham font), built in code into its own `PickerGui`: station title + action line, grid of cards (3D item in a ViewportFrame or a blade silhouette; hilt cards show the real dressed hilt and guard from `Hilts.dress`, tipped so the guard face shows, with `SwordParts` preloaded; blade and sword cards with a `blueprintId` draw that blueprint's real finished blade (`BladeView`, 1.5× wider for readability, on a shared square-root scale so a tantō reads short), swords with their real hilt, and the Etching Table's pattern card shows the etch on the chosen sword; these EditableMeshes are freed whenever the window is rebuilt or closed, name, chip, ×qty; hover / gamepad focus = amber edge), close ring (B closes), blur + dim behind, empty state. Compact one-row layout when the screen is under 500 px tall. Also `toast(text, "warn"?)` (sits 136 off the bottom, above the hotbar, since 2026-10-21). `ItemPicker.artModel(art, meshes)` lends the card art to the `Hotbar` (meshes go in the caller's list; a sword model carries `FitFrom` / `FitTo`, its hilt-to-tip line, because the blade mesh's bounds are padded far past it; backups `Legacy.ItemPicker_beforeHotbar`, `Legacy.ItemPicker_beforeRarityLook`). Used by the forge, anvil, holders and Hilt Bench |
| `Hotbar` (2026-10-21) | Replaces the Backpack core GUI (`SetCoreGuiEnabled(Backpack, false)`, retried until core scripts are ready). `HotbarGui` bottom centre, 12 off the edge: one 100 × 112 slot per stack with 10 px corners, a 3 px black `UIStroke` (white on the stack in hand) and the item's rarity colour (`RARITY` by `Materials.get(MaterialId).rarity`: Common slate, Uncommon green, Rare blue, Epic purple, Legendary gold). A `CanvasGroup` clips the corner halftone (`rbxassetid://77944995466851`, rotated −90°, 72% transparent) into the bottom-right. Key number, count (`3x`) and name in Gotham Heavy, white with a 2 px black stroke. The item: `ItemPicker.artModel` in a 96 × 66 `Art` frame, under white light with the metal lightened (blade 30%, the rest 15%), over eight Neon copies 1 px out tinted black (the rim; `Highlight` doesn't render in viewports, and the blade mesh only goes white as Neon). Swords are framed on their hilt-to-tip line (`FitFrom` / `FitTo` from `ItemPicker`) and rolled to the box's diagonal; ingots keep the picker camera. Stacks: ingots by `MaterialId` + `Hot`, each sword alone (`SwordId`; art redrawn when etch, hilt, metal or blueprint change). Keys 1–9, click or tap equip the stack's first tool; again unequips. **Bag:** the bar holds 9 stacks and ends in `BagButton` (icon `rbxassetid://15402958715`, "Backpack" by VectorIcons, decal 15402958804; key `~` / Backquote; count of stacks in the bag top-right; white edge while open). New stacks join the bar while it has room, else the bag: `Bag`, a scrolling 10-column grid (3 rows visible) above the bar. Click or tap a bag item to equip it. Drag (a press that moves 8 px; ghost copy follows the pointer): onto a slot swaps the two (bar or bag), onto the bag or its button stashes it at the bag's end, from the bag into the bar's height band joins the bar if it has room. Hit-testing by `PlayerGui:GetGuiObjectsAtPosition` and the slots' `StackKey` attribute. Order is client-only (`barKeys`, `bagKeys`), survives respawns. Backup before the bag: `Legacy.Hotbar_beforeBag`. Hidden while `AnvilHud` or `HiltBenchHud` is enabled; scales down to fit narrow screens (0.75 under 500 px tall). Nine viewports per slot. No gamepad cycling yet. Backup of the first look: `Legacy.Hotbar_beforeRarityLook` |
| `Shared/EtchPatterns` (2026-10-21) | Stroked etch patterns as ordered `{ x, y, h }` strokes in cm on the face; `STROKED`, `strokes(id, length, widthAt)`. Eclipse only so far |
| `Shared/EtchCanvas` (2026-10-21) | A stroked pattern's texture on one blade: strips of 1024×128, piece rasteriser with coverage anti-aliasing, `reveal(d)` (monotonic, order-independent), `revealBand(x, reach)` (Flame's band for the show), `at(p)` for the tool, baked body and mark colours; `layout`, `uv`, `count` Since 2026-10-21 `new(..., spread)` and `reveal(d, spread)` can yield after about 4 ms of work per frame; only the Polishing Station's fetch uses that. |
| `SwordRenderer` | Draws held and displayed blades with BladeCore + BladeView (one EditableMesh per visible sword for now). Swords with an `Etch` attribute also get their etch from `SwordMeshCache` (Flame's skin, or since 2026-10-21 a stroked pattern's textured overlay, passing the material accent), welded with the blade. Shares are given back on `Destroying` and, since 2026-10-21, when the sword leaves the game (`GetInstanceRemovedSignal("ForgedSword")`): server-destroyed tools only leave a client, and their meshes leaked |
| `Shared/BladeEtch` (prototype, 2026-10-19) | Client etch skin: a two-colour EditableMesh just above both blade faces, built from the same BladeCore station params (sampled ~4× finer) so it follows any blueprint's forged/ground shape. `PATTERNS.Flame(sw)` gives how far the band colour reaches from the edge at `sw` local blade widths from the base. Since v4 (2026-10-20) it is the reference-matched red band: even humps of 0.14 width around 28%, spaced 0.75–1.05 widths. Columns run from a 3.2% edge line to a 3.2% spine line, so bare steel shows as bright edges; per-vertex colours shade the bevel (12 cached steps). Pre-v4 module kept as `ServerStorage.Legacy.BladeEtch_beforeBand`. `build(params, pattern, body, flame)` returns the MeshPart and its EditableMesh. See [[Art/Flame Etch]] |

## StarterGui

`AnvilHud` (anvil panel, hint, result banner; Tools, Hammers and ModeButton hidden), `AnvilPoints` (unused; strike ring built at runtime in `StrikeRingGui`), `HiltBenchHud` (Seat panel) and `ShopHud` (offer card, notices; the offer card is 136 off the bottom since 2026-10-21, above the hotbar). `GrindMap` belonged to the earlier anvil flow; current polishing has its own controller and progress strip (see Polishing Station below). The picker and toasts are built by `ItemPicker` (`PickerGui`).

## Workspace

`Smithy/` holds `OreRoller`, `Forge` (Base + HeatPrompt "Use forge"), `Anvil` (BladeMount, ForgePrompt, Clang sound), `HiltBench` and the other stations. The shop is not in `Smithy`: since 2026-10-20 it is `Plot.Shop` (`Storefront`, `Displays`, `EntryPoint`; see below). The blade on the anvil (`Blade`), the Trace guide and the `Customers` folder are created at runtime.

Rebuilt 2026-10-19 in the Japanese style ([[Archive/Art/Smithy Redesign|Smithy Redesign]]). Each station keeps the parts scripts read, and its look lives in a `Dress` model (plus `Stand1` on the roller):

| Station | Parts scripts read (don't move or rename) | Free to restyle |
|---|---|---|
| `Forge` / `Forge2` door (2026-10-20) | `Door` (`Door_iron`, `Door_strap`, `DoorWindow` + `WindowLight`) flush on the furnace face; `HeatPrompt.RequiresLineOfSight = false` so E works through it | ForgeService `setWindow`: in `refreshBoard`, the window is Neon (255, 120, 35) with its light on while any slot of that forge is busy, otherwise SmoothPlastic (41, 26, 20) and the light off. A `Lit` attribute stops repeat writes |
| `Forge` | `Base` (invisible box, exact old size and CFrame; ForgeService places `ForgeSlot1/2` and `ForgeTimers` from it) + `HeatPrompt` | Since 2026-10-20: `Model3D` (the Blender mid-high forge, turned to face +Z; its trays sit under `ForgeSlot1/2`); `Fire` is now invisible and keeps only its PointLight, inside the new chamber. `Chimney` and `Dress` removed |
| `OreRoller` (mine entrance since 2026-10-20, later; soft-rock cave the same day) | `MineCave` (asset 84547516108281, same footprint and mouth as the old `MineEntrance`): `Rocks` and `Wood` MeshParts with hand-painted SurfaceAppearance colour maps and precise collision; the black `void` panel 0.6 inside the mouth collides; the `paper` lantern is Neon with `LanternLight`, under the roof's right end. No script references the mine model by name. `Track` (`Rails`, `Sleepers`, `Stop`). `CartPath`: invisible `Point1..9` along the track centreline from inside the mine out (straight, a radius-4 quarter turn to +X, straight). Its attributes are `Stop1..6` (distances along the track: 5.6 / 9.1 / 12.6 / 22.5 / 26 / 29.5) and `Hidden` (−1.6, inside the tunnel). `Stand1..6` are carts parked at their stops; each pivot sits on the track under the cart, facing along it. `Stand2..6` are TycoonItems `OreStand2..6`. `Lever` and `Machine` are left of the mouth (hinge (39.4, 1.2, −53.8)). | ForgeService: `poseAt(s)` walks the CartPath. A pull moves every unlocked cart that is empty or holds the puller's own ore into the mine (nearest first), then sends them out (furthest first, eased into the stop). Every pull takes 4 s whatever the cart count (Allen): `IN_TIME` 1.5 + `OUT_TIME` 2.5. Each trip takes 60% of its phase and the other 40% (`STAGGER`) spaces the carts out; with one cart that 40% is a pause in the dark. The ore flickers while a cart rolls and is revealed when it stops. The lever ignores pulls while carts roll. Backups: `Legacy.ForgeService_beforeCarts`, `Legacy.OreRoller_beforeEntrance`, `Legacy.OreRoller_MineEntrance_beforeCave` |
| `OreRoller` (mine since 2026-10-20) | `MineShaft` (curb, headframe, wheel, roof, bucket, winch, dirt yard; MeshParts named by colour, precise collision on stone/timber/spool), `Track` (`Rails`, `Sleepers`, `Stops`), `Lever` (`Base`, `Bracket`, `Arm` + `Knob` welded to the anchored `ArmPivot` at the hinge (50.6, 1.2, −61.6), RestDegrees −25 / PulledDegrees 35), `Machine` + `RollPrompt` at the knob, and the carts `Stand1..3` (`Body`, `Rim`, `Chassis`, `Wheels`, `Ore`) at x 37 / 42 / 47, z −57.5. `Stand2/3` are TycoonItems (`OreStand2/3`, shown as "Ore Cart 2/3"); their pads sit in front of the yard. ForgeService and LeverAnimator are unchanged apart from text; the CollectPrompt goes on each cart's `Ore`. The pre-mine roller is `Legacy.OreRoller_beforeMine` | The rows below describe the pre-mine roller |
| `OreRoller` | `Machine` (invisible prompt part at the knob, x −8.5 since 2026-10-20) + `RollPrompt`; `Lever` (2026-10-20, Allen's reroll-lever reference: sage base, two half-disc wooden cheeks, `Arm` + `Knob` welded to the anchored invisible `ArmPivot` at the hinge, rest −25°, pulled +35°; `LeverAnimator` swings it while E is held). `Stand1` was scaled 1.35× and its `Ore` enlarged (about 2.3 × 1.2 × 2.3) so the result reads from across the room; `Stand<n>` models with `Ore` (+ optional `OreChunk*`, `Sparkle*`, `Pedestal`). ForgeService finds them by name, so a new stand is just another model | Since 2026-10-20: `Lever` (the Blender lever model on `Machine`, which is now invisible); `Stand1` holds the textured Blender stand: `Ore` (the roll recolours it), `Pedestal` (the stone base, carries `CollectPrompt`), wood/iron parts and the old `Sparkle*`. The shrine `Dress` and the old chunks are gone |
| `Anvil` | `BladeMount`, `Face` + `ForgePrompt`, `Clang` | Since 2026-10-20: `Model3D` (Blender hornless block on a low timber base). The whole station dropped 0.7, so `Face` (now invisible) tops out at 2.5 = 2.3 above the floor, flush with the new striking face. `Stump`, `Waist`, `Base` and `Dress` removed |
| `HiltBench` | `Top` + `HiltPrompt` (invisible since 2026-10-20, just under the new worktop) | `Model3D`: the Blender bench (5.0 × 2.4, worktop 2.9 above the floor) |
| `EtchingTable` (2026-10-20) | `Top` + `EtchPrompt` (EtchService measures reach from `Top`) | `Dress` (27 parts at x 11, z −30: worktop at 2.9 like the Hilt Bench, iron tray with slate bath and a half-etched blank, brush pot, three jars, andon lamp) |
| `DisplayRack` (gone 2026-10-20: its `Displays` and `EntryPoint` moved to `Plot.Shop`; this row is history) | `Slots/Slot1..3` + `HolderPrompt`: latest recorded slots are turned X down and raised to y 4.75, with the guard on the pad 3.95 above the floor and broad blade face toward each `InspectPoint`. Plan coordinates retained from the storefront layout: Slot1 x −39.5 / z 4, Slot2 x −25.5 / z 4, Slot3 x −39.5 / z −7. Invisible `EntryPoint` and `InspectPoint1..3` guide ShopService from road → entry → chosen holder and back. Keep these routes clear; the earlier y 2.92 / blade-up placement is superseded | `Holders/Holder1..3`: Blender universal holders facing their InspectPoints. Old `Dress` pedestals removed |

Plan positions from the [[Archive/Art/Player Plot Review|Player Plot Review]] pass: Forge x 2 / z −29.3 against the back wall, Anvil x 2 / z −16 on open floor about 9 studs in front, OreRoller x −9 / z −28.57, HiltBench x 20 / z −30. Vertical placement changed during Blender import (especially the lowered anvil); use current station contracts above rather than old pivot heights. Whole-station moves require checking prompts, mounts, camera and customer routes.

`Plot/` (2026-10-19, no scripts) is the player property, built to the L-shaped concept ([[Archive/Art/Japanese Village Concept Art|Japanese Village Concept Art]]) and widened after the review. Plot bounds x −50…76, z −48…30 (126 × 78 studs):

- `Pavilion`: the crafting wing, 50 × 28 studs at x −19…31, z −32…−4 (replaced the shallow 41 × 17 `Workshop`, archived as `ServerStorage.Archive.Workshop_v1`). Four front posts with 14–18 stud openings, open east side toward the lawn, `Floor` (earth floor plus a `WorkApron` running out into the courtyard), `Frame`, `Walls` (back and west), `Roof` (gable, ridge along X at z −18, 3-stud eaves), `Lanterns`. No beams cross the anvil bay below y 11.

- `Storefront`: the shop wing at x −45…−20, z −22…16, with `Frame`, `Walls`, `Roof` (gable, ridge along Z), `Front` (noren, crest), `Lanterns` and `Interior` (counter, drawer chest, sword wall racks, pots). The doorway (x −38.5…−26.5) faces the road. The 刀鍛冶 `Signboard`/`SignFrame` (under `Storefront.Front`) sit on its front gable. Holders stand in two columns either side of a clear aisle to the counter.
- `Yard`: `PlotPad` grass, `Courtyard` (three pieces around the work apron) and `FrontYard` paving, `GatePath`, `LawnCurb`. The lawn east of x 37.8, and the strip behind the pavilion, are the expansion space.
- `Fence` (entrance gap x −36…−29 at z 30; front and back runs own the corners, side runs stop short), `StoneLanterns` (gate, corners, either side of the work apron; PointLights), `Greenery` (bamboo groves at corners and boundaries, rocks, shrubs, pots), `IngotShelf` (decor on the pavilion's west wall by the ore shrine).

**No Z-fighting (build rule):** ground layers start at y 0 and never share a top height where they overlap: Baseplate 0, `PlotPad` 0.1, floors/paving/road 0.2, road edges 0.3, curbs 0.4. Where two parts meet, one face sits at least 0.04 proud of the other. On 2026-10-19 a coplanar-face check over `Plot`, `Smithy` and `Village` (axis-aligned block parts) found 157 overlaps and nudged 180 faces outward by 0.04 (2 by hand in the forge chamber); none were left. Rerun that check after building.

`Village/` (before 2026-10-21) held the shared `Road` (z 34…46) and `CustomerSpawn` (−32.5, 3, 40); the folder had gone by 2026-10-21 and `Workspace.Village` is now the town street (see **Village street** below). `SpawnLocation` is in the courtyard at (0, 0.2, 16), hidden. `ServerStorage.Archive` holds the old prototype blocks (`store`, `creation area`, two slabs), the first ground pieces (`Workshop_PlotPad`, `Workshop_FrontYard`, `Workshop_ApproachPath`) and `Workshop_v1`. The Baseplate is grass. Still one plot: every station is the single shared `Smithy`; per-player plots need the controllers and services to look up the player's own plot instead of `workspace.Smithy`.

## Models (outside Studio)

`Models/Archive/SwordShop.bbmodel` (Blockbench source) and `Models/Archive/SwordShop.fbx` (import file, 1 unit = 1 stud): the historical medieval cabin, 17 named meshes on one palette texture. Never imported; superseded by `Workspace.Plot`.

## ServerStorage.Builders (2026-10-21)

Studio copies of the vault's builders, so a rebuild needs only small edits rather than pasting the whole file: `build_street` and `build_shops` (ModuleScripts holding the exact text of `Models/Village/*.luau`; `build_town` and `build_simple` since 2026-10-22, and only `build_simple` builds the live map; `build_workshop` (the workshop's layout and furniture, run after `build_shops`) since 2026-10-22; run with `loadstring(ServerStorage.Builders.<name>.Source)()` from MCP, never `require`), and `coplanar_check` (`check(parts)` returns the visible same-plane face pairs; `aabb(part)`). Keep each copy identical to the vault file: compare character count and checksum after editing either one.

- `bake_sword_meshes` (ModuleScript, 2026-10-21; use `require`, not loadstring; works on a fresh copy of Shared, because Edit's `require` serves edited modules' old code): bakes every finished sword shape into `ReplicatedStorage.SwordMeshes` through the vault's `Development/sword_mesh_bake.py` helper (glb plus Open Cloud upload). Run `print(require(game.ServerStorage.Builders.bake_sword_meshes:Clone()).run())` in Edit with the helper running. See [[Development/Sword Mesh Pipeline]].

## ServerStorage.Legacy

`SharedV1` is a frozen copy of the shared modules from before the 2026-10-19 rewrite (old Blueprints, ShapingModes, FinishCheck…) and `AnvilController_PrototypeModes` (disabled) is the old anvil with its Silhouette/Trace/Clicks/Points modes. Kept for reference and for `AnvilSelfCheck`.

## Tests

- `ServerStorage/Tests/BladeCoreSpec` (with `BladeGolden`) tests the BladeCore port; see `Prototypes/tanto-forge/roblox/README.md`.
- `ServerStorage/Tests/ForgeCheckSpec`: the new blueprints and the server's Finish check (35 checks). Run `print(require(game.ServerStorage.Tests.ForgeCheckSpec)())` in the command bar.
- `ServerStorage/Tests/EtchingSpec` (2026-10-21): the animated etching, 33 checks (a spread build yields and matches an immediate one; canvas exactness, lifts, tool surface on the real blade, cache keys, one overlay mesh across materials, isolation from the shared image, cleanup over 12 runs, a failed image, no extra mesh per show, Flame's band). Run `print(require(game.ServerStorage.Tests.EtchingSpec:Clone())())` in Edit; it stages on the template plot's table and removes its copies.
- `ServerStorage/Tests/SwordMeshSpec` (2026-10-21): the baked sword meshes, 110 checks. For each shape: baked for the blueprint's version, `Hash` equal to today's live build, uploaded mesh equal to the live one face by face (positions, UVs, colours, normals), and the cache hands out the bake. Run `print(require(game.ServerStorage.Tests.SwordMeshSpec:Clone())())` in Edit.
- `ServerStorage/Tests/AnvilSelfCheck` now checks the frozen `Legacy.SharedV1` copy (old blade maths, prototype modes, customers, materials, value). Run `require(game.ServerStorage.Tests.AnvilSelfCheck)()`.

`ServerStorage/AnvilController_Backup` is the disabled pre-refactor controller. Safe to delete.

Related: [[Home]] · [[Development/Roadmap|Roadmap]] · [[Design/Game Design Document|Game Design Document]]

## Polishing Station (2026-10-20)

| Piece | What it does |
|---|---|
| `Workspace.Smithy.PolishStation` | `Model3D` (Blender bench with felt pads, whetstones, water-cooled stone wheel, bucket; asset 86416596849647) at x 27, z −30 right of the Hilt Bench; `Top` (invisible) + `PolishPrompt`; `BladeMount` (invisible, 25.3, 3.22, −29.85): the blade lies along +X from here, edge toward the player |
| `PolishController` (client) | E → picker "Choose a sword to polish." (finished swords with their %; fully polished ones locked) → BeginPolish → the sword's blade on the bench, top-down camera, hold and drag along the edge (same `BladeCore.applyGrind` as the anvil had), progress strip, Save → PolishSword / Leave (Q). Since 2026-10-21 an etched sword shows its etch on the bench (`syncEtch`: the cached etch for the cache's polish level, fetched again when that level changes) The etch's body brightens with the polish level (`SwordMeshCache.etchBody`). Crossing a level fetches the next etch in the background (`etch(..., spread = true)`), keeping the current one until it's ready; after leaving, the last etch is held 5 s so the saved sword's art finds it warm. |
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

`Plot.Storefront.Shell` (Blender low-poly shop, precise collision) replaced `Frame`, `Walls` and `Roof`. `Plot.Pavilion` is now `Plot.Courtyard`: `Paving` (stone flags, x −14..42, z −34..2.5) plus `StoneLanterns`. All crafting stations moved +8 in x onto it; `DisplayRack` stays in the shop. `Plot.StoneLanterns` and `Courtyard.StoneLanterns` use the Blender lantern (light on `StoneLantern_paper`). `Plot.Greenery.Bamboo1..12` are the three Blender variants. Source models live in `ServerStorage.Buildings3D`. See [[Archive/Art/Building Redesign]].

## Sword meshes, ingot ore and station order (2026-10-20)

- `Shared/SwordMeshCache` (client): finished swords share meshes. **Since 2026-10-21 it uses baked meshes first:** `ReplicatedStorage.SwordMeshes` holds uploaded MeshParts named by cache key (27: 3 blueprints × 3 levels × blade, overlay and Flame skin), which cost nothing from the EditableMesh budget. A key with no bake for the blueprint's `Version` is built live with one warning. `useBaked` turns this off for the bake tool and specs. To add or change a sword, follow the routine in [[Development/Sword Mesh Pipeline#Adding a sword later]]. Before that, finished swords shared EditableMeshes. Since 2026-10-21 `etch()` takes the material accent: a stroked pattern (Eclipse) is a texture with the colour baked in, keyed `E|bp|level|pattern|body|accent`, laid on a share of `overlay()` (`O|bp|level`, one mesh shared by every stroked pattern and material); its EditableImage and overlay share are released with it. Flame's key and tinting are unchanged. Key = blueprint + the blade's average polish rounded to 0, 0.5 or 1 (+ etch pattern). Etch meshes are colour-neutral (white band); the clone's `Color` is the band colour. `blade(bp, refinement)` / `etch(bp, refinement, pattern, body)` return a Clone plus a key; `release(key)` frees the mesh with its last clone. `SwordRenderer` and `ItemPicker` card art use it; the anvil and Polishing Station keep their own live `BladeView`. **Polish sheen (2026-10-21):** `etchBody(bp, refinement, body, pattern)` lifts an etch's dark body toward (150, 190, 230), by 0.3 for a stroked pattern and 0.6 for a band (Flame's skin is tinted by its band colour), times the polish level / 2. `etch()` draws in it, and `EtchPlayback` draws its show in it (a band's body pre-tinted by the band colour). `etch(..., spread)` builds a stroked pattern's image over several frames (it yields).
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
- **Tycoon upgrades (2026-10-20, [[Design/Tycoon Upgrades]]):**
  - **Display tables (2026-10-20):** a table with a katana stand on top. Slots are rack-style (blade +X, edge up, flat face out) at tiers 2.95 / 3.65 / 4.35 above the floor, grip at (−1.77, z 0.21) in the table's frame; `TagOffset` (−1.6, 0, 0.6). Template `Buildings3D.SwordTable` (asset 100555972253981).
  - **Shop group (2026-10-20):** everything for the shop is in `Plot.Shop`: `Storefront` (`Starter`, `Upgraded`), `Displays` (`WallRack1..4`, `DisplayTable1/2`) and `EntryPoint`. ShopService finds it as `Plot:WaitForChild("Shop")`, reads `EntryPoint` from it and parents displayed swords to it. The slots themselves are still found by the `DisplaySlot` tag, and the items by `TycoonItem`. `Smithy.DisplayRack` is gone.
  - **Displays (2026-10-20, later):** `Plot.Shop.Displays.WallRack1` is the starting rack (west wall, z 12, not a TycoonItem); `WallRack2` (east wall, z 12), `DisplayTable1` (−37, −6), `WallRack3` / `WallRack4` (west / east walls, z −16.2, Upgraded Store) and `DisplayTable2` (−24.5, −7) come from pads. The floor holders (`Holders`, `Slots`, `InspectPoint1..3`) are retired to `Legacy.FloorHolders_beforeWallRacks`; `EntryPoint` is now `Plot.Shop.EntryPoint`.
  - **Shop sizes (2026-10-20):** `Storefront.Starter` 31 × 32 (x −49..−18, z −16..16, shell asset 124926846811438), `Storefront.Upgraded` 31 × 46 (z −30..16, 89878911135006). Store counter and drawer chest are at z −23 / −28.9; WallRack1 is at z 2.2 (west wall), WallRack2 at z −16.2 (east wall); the UpgradedStore pad is at (−33.5, −23).
  - **Furnace colours (2026-10-20):** `Forge` / `Forge2` stone parts rgb(66, 76, 98), plinth (48, 55, 72), soot overlays untextured (42, 47, 62); old texture in `OldTextureID`.
  - `Shared/Upgrades`: the upgrades (`list` of `{ id, name, price, after }`, `byId`). Chains branch by courtyard zone; entries with no `after` are buyable from the start (2026-10-20).
  - **Courtyard zones (2026-10-20):** ore yard back right (lever (35, −31.5), Stand1–3, Ingot Rack (35, −10.5)), forge hall back middle (Forge (8.5, −29), Forge2 (15, −29)), smithing in the middle (Anvil (11, −12), HiltBench (20, −12)), finishing back left (PolishStation (−7.5, −29), EtchingTable (0, −29)), SwordRack (−6, −8) by the shop's side door. Pads moved with their stations. Reserved spots: [[Design/Tycoon Upgrades]].
  - `TycoonService` (server) owns the plot: `Plot.OwnerId` / `OwnerName` (the first player in; when they leave, everything resets and passes on) and `Plot.Bought_<id>`. It shows a `PadVisual` (grey base, green `Top`, name + price billboard) on each available `Plot.Pads.<id>` marker. `Remotes.BuyUpgrade(id)` requires the owner, standing within 3 studs of the pad, and `SmithyCore.spendCoins`.
  - Locking: every `TycoonItem` (tag) with `Upgrade` = id unlocks when bought; `UntilUpgrade` items (the Starter Shop) lock instead. A locked item has `Locked = true`; the server switches off collision, query, touch, prompts, lights, GUIs and particles, and restores exactly those on unlock. Locked `DisplaySlot` descendants get `Locked` too.
  - `TycoonController` (client) hides locked items with `LocalTransparencyModifier` and shows the owner a `BuyButton` billboard while standing on a pad's top. Only the button buys.
  - Items: `Smithy.OreRoller.Stand2/3`, `Smithy.Forge2`, `PolishStation`, `IngotRack`, `SwordRack`, `EtchingTable`, `Plot.Shop.Displays.DisplayTable1/2` and `WallRack2/3/4` (the floor holders are retired), `Plot.Shop.Storefront.Upgraded` (Shell, Floor, Front, Interior, Lanterns, InsideZone); `Plot.Shop.Storefront.Starter` (Starter shell, 24 × 14 floor, InsideZone, kanji sign on its board, 4 chochin) is `UntilUpgrade`. Both shops are tagged `HidesRoof`; `RoofHider` skips locked ones.
  - **Display slots:** parts tagged `DisplaySlot` (a sword's Handle goes on the part's CFrame) with a `HolderPrompt` (Custom style), an `Inspect` ObjectValue, optional `ViaAisle` and `TagOffset` (in the display's frame). `ShopService` registers unlocked ones as `SlotIndex` n and drops them on lock (a displayed sword goes back to its owner). Only the plot owner can display. `ShopController` draws a round + `SlotMarker` per empty slot (owner only); the focused one shows "For sale" and E. Clicking a marker or pressing E opens the picker.
  - `ForgeService` handles every `Forge` / `Forge<n>` (own tray and timer; `ForgePut(ingotId, forgeName)`; slot numbers run across furnaces) and skips locked furnaces and stands. `ForgeController` sets up each furnace as it streams in. Rack, Etch and Polish remotes refuse while their station is locked.
  - Templates: `ServerStorage.Buildings3D.WallSwordRack` / `SwordTable` (Origin, `InspectPoint`, `Slot1..3`). Since 2026-10-20 every wall rack's look is a `Rack` model built from Allen's imported `sword_rack` (original kept at `ServerStorage.sword_rack`), scaled ×0.658 so its hook rows are 1 stud apart, Wood material in three browns. In display space the hooks sit at x −0.88 / 2.41 under each slot (slots at x −0.58, y 4/5/6, z 0.385 in the cradle). `EntryPoint` moved to x −30. Backups `Legacy.*_beforeTycoon` (ShopService, ForgeService, RackService, EtchService, PolishService, ShopController, ForgeController, RoofHider).
- **Wall holder spots (2026-10-20, superseded by the tycoon pads the same day; spots and `WallHolder` moved to `Legacy.WallSpots_beforeTycoon` / `Buildings3D.WallHolder`):** `Plot.Storefront.WallSpots.Spot1..9` (invisible parts at a holder's origin): west wall z 11.25 / 1.75 / −7.75 / −17.25, east wall z 11.25 / −7.75 / −17.25 (not the side-door bay), back wall x −43.8 / −23.2 (not behind the tansu). The old decorative `Interior.SwordRack1/2` were moved to `Legacy.InteriorSwordRack1/2_beforeWallHolders`. `SmithyCore.spendCoins(player, amount)` takes coins only if the player can afford it (backup `Legacy.SmithyCore_beforeWallHolders`).
- **Shops:** `Plot.Storefront.Shell` is the feudal Upgraded Store (asset 111190210571986, 31 × 38, two storeys; `attr SourceAsset`): six wall/ground MeshParts with precise collision, and a `Roof` model holding the roofs, upper storey, canopy and beams (no collision). `Plot.Storefront` keeps the `InsideZone` part and the `HidesRoof` tag. The 刀鍛冶 `Front.Signboard` (4 × 1.2) sits on the canopy board at z 19.8, y 13.3. The feudal Starter Shop (131094404219127, 24 × 14) is staged in `ServerStorage.Buildings3D.StarterShop`, not placed; `Buildings3D.UpgradedShop` is the Upgraded Store's source. Backups: `Legacy.Storefront_beforeFeudal`, `UpgradedShop_beforeFeudal`, `StarterShop_beforeFeudal`, `SignFrame_beforeFeudal` (and the older `Storefront_beforeWider`). See [[Archive/Art/Building Redesign]].
- **RoofHider** (StarterPlayerScripts): for each `HidesRoof` model, fades `Shell.Roof` parts (LocalTransparencyModifier) while your HumanoidRootPart is inside `InsideZone`. Since 2026-10-21 it works per plot: inside any `HidesRoof` building of a plot (the ancestor with a `Lot` attribute), every unlocked roof on that plot fades (shop, Upgraded Store upper storey, workshop). Backup: `ServerStorage.Legacy.RoofHider_beforePlotWide`.
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

## Village street (2026-10-21)

*Superseded 2026-10-22: `Workspace.Village` is now the simplified map (see **Simplified map (2026-10-22)** below). This street is parked as `ServerStorage.Legacy.Village_before_20261022052609`; `build_street.luau` is retired.*

`Workspace.Village` (Model, pivot at the street centre (17.5, 0, −560), which is also the shop's frontage centre) is the Japanese town street from [[Archive/Art/Japanese Street]], built by `Models/Village/build_street.luau` (run in Studio through MCP; seed 21; a rebuild moves the previous `Village` to `ServerStorage.Legacy`). No scripts. Rebuilt 2026-10-21 as one continuous row (see **Continuous row** below).
- `Street`: `Road` (Pavement, x −395…350, |z| < 8 in the village frame), `Curb` ×4, `Water` ×2 (gutters, |z| 8…10), `Walkway` ×2 (|z| 10…17.5), `Plaza` (east end). Ground tops: road 0.2, walkway 0.3, plaza 0.25, curbs 0.5, door bridges 0.64.
- `Rows`: `HouseN…/HouseS…` (54 Models since the continuous-row rebuild, pivot at the façade line facing the street; styles Takayama, kura, Tsumago, gable-front, single-storey). Only `Ground`, `Upper`, `Post`, door `Bridge`, `Platform` and `Bench` collide.
- `Lots`: `PlotSlotN1..N3`, `PlotSlotS1..S3` (invisible 48.5 × 96 parts at each lot's centre, y 0.5, LookVector toward the street, attribute `Side`; nothing reads them yet), the plaster walls between each lot and the neighbours' backyards (from 32 behind the façade), and `Closed<N|S><n>`: a closed shopfront on every lot without a player plot (attribute `Lot` = its slot).
- `Trees` (clones from `ServerStorage.Village3D` / `Buildings3D`), `Landmarks` (west gate 刀鍛冶の里, torii, `Shrine`, stone lanterns).
- `Mountains`: parked 2026-10-21 as `ServerStorage.Legacy.Mountains_parked` (`build_street.luau`: `MOUNTAINS = false`). Four invisible `Bound` walls stay on the old inner face line (x ±395, z ±130 in the village frame).
- `CustomerSpawn` (18.5, 3, −563, world, on the road in front of lot N2): `ShopService` waits for `workspace.Village.CustomerSpawn`; the old folder was gone, so it was restored here, first at (−32.5, 3, 40) and then moved with the plot.
- Coplanar check 2026-10-21 (first build): 36 pairs left of 2,607 block/wedge parts, all hidden (roof ends inside a neighbour's roof, display platforms on the walkway, one lantern cord).
- **Plot in lot N2 (2026-10-21, Allen; superseded by the continuous row below):** `Smithy`, `Shop` (`Starter`, `Upgraded`, `Displays`, `EntryPoint`), `Pads`, `Yard`, `SpawnLocation`, `Weapon Rack` and the six loose stone `Part`s by the mine moved by one offset, (+51, 0, −608), so the layout is unchanged; they now span x −115…123, z −689…−574 (world), with the old `GatePath` front tucked under the walkway. `PlotSlotN2` is 280 × 110 (village x −140…140): the north townhouses, backyard trees, lot walls and lamps between lots N1 and N3 (33 instances) were parked in `ServerStorage.Legacy.Village_besideN2`; `build_street.luau` repeats this so a rebuild matches. The stray `Bamboo1..12` and the top-level `Courtyard` part and model (z 58…166) were not moved. `SpawnLocation` is now (51, 0.2, −592). Moving welded parts by CFrame dragged the unanchored `OreRoller.Lever` arm three times; it was corrected and every piece checked inside the lot.
- **`ShopService.AISLE_ROWS`** were world z values (11, −1.5, −12); they are now `ENTRY_POINT.Z + 35 / + 22.5 / + 12` (the same rows, measured from `EntryPoint`) so customer aisle routes follow the shop. Backup `Legacy.ShopService_beforeStreetMove`. Not playtested.
- **Continuous row (2026-10-21, Allen: "resize all six lots to the new footprint, and give unclaimed lots a closed shopfront so the street reads as one continuous row"):** `LOT_W` 48.5 (the shop + workshop is 48 between wall faces and its corner posts reach ±24.2; neighbours start 0.07 beyond), `LOT_D` 96, house segments `(700 − 3 × 48.5) / 4` ≈ 138.6 each, `ORIGIN` x 4 → 17.5 so lot N2 is centred on the building. `TAKEN = { N2 = true }` lists lots with a player plot; the other five get `Lots.Closed*` (a `house()` with `doorBay = 0` and every bay a shutter, no lantern, sign or bench). The N2 widening, its `Village_besideN2` parking and the lot-corner lamps are gone from the builder. Backyard trees whose crowns would reach a lot are dropped (`LOTS_X`). Battens are 0.1 shorter than their shutters (they had shared top and bottom faces).
  - Plot fit: nothing in the new street touches `Plot` or `Smithy` except the intended walkway over the shop's floor edge and front wainscot.
  - Coplanar check around the plot (888 street parts): no overlaps with the plot. 448 battens shortened; four chance overlaps fixed by hand with 0.02 nudges (ridges of `HouseS26` and `HouseN29`, a cord in `HouseS26`, the roof of `ClosedS2`). A rebuild with the same seed brings those four back.
  - `ServerStorage.Legacy.Village_before_20261021233750` is the first street; `Village_besideN2` is obsolete.
- **Wider street, taller buildings (2026-10-21).** Allen: "Can we also expand the street a bit, it seems very closed and tight right now", then "also make the buildings a bit taller, right now the entrance is barely taller than the player".
  - `HALF` 16 → 22: fronts 44 apart instead of 32. Only the road grew (28 wide, was 16); walkway, gutter and bridges keep their distance from each façade, so a plot's front still fits. `ORIGIN` is now (17.5, 0, −554) = façade z −576 + HALF, so the north row and the plot template stay put and the south row is 12 further south. Gate, plaza, groves and `Bound` walls (z ±(HALF+114), the north one still at −690) follow `HALF`.
  - `LIFT` 2.5 on every ground storey: openings (door, lattice, shutters, noren rod, beam) top out at `OT` 9.7 instead of 7.2; houses are 12…14 tall on the ground floor (were 9.5…11.5), the shrine 11. Upper storeys and roofs sit on top unchanged.
  - Same seed, same street: 54 houses, 6,449 parts.
  - Fixes found by the full-street check: kura houses get three upper windows only when the shutters fit (`W / 4 > 5.25`); tree rejection uses the crown's diagonal (a turned maple reached 1 stud into lot S1 and through its workshop wall); neighbours alternate `sp.alt` (0/1, closed fronts 2) so ridges and fascias shift 0.03 apart; lanterns under rafters hang in a rafter gap. These replace the four hand nudges listed above.
  - Checks: whole street swept in 50-stud slices, 0 visible coplanar pairs; the plot on all six lots (Starter, and Upgraded with the workshop pushed back) 0 coplanar and no solid overlaps with the street; `CustomerSpawn` lands 9 from the road's centre line on N2 and S2.
  - Backup of the street before: `ServerStorage.Legacy.Village_before_20261022004542`. Not playtested.

## Shop and back-room workshop (2026-10-21)

*Depths and workshop positions below are from before the storeroom; see **Shop grows on the upgrade** further down for the current ones.*

*Workshop layout since 2026-10-22: the alcove is gone and the stations and pads are where `build_workshop.luau` puts them; see **Workshop layout (2026-10-22)** at the end.*

One townhouse on the street in lot N2, from Allen's layout `References/Concept Art/shop design` (a PNG without an extension): the shop room on the street, a centre door, and the workshop behind with the stations clockwise round its walls. Built by `Models/Village/build_shops.luau` (run in Studio through MCP after `build_street.luau`). It rebuilds `Plot.Shop.Starter.Shell`, `Plot.Shop.Upgraded.Shell`, `Plot.Workshop`, `Plot.Shop.CommissionBoard` and `Plot.Yard.ShopFront` (models carry `BuiltBy = build_shops`), and sets both shops' `Floor` and `InsideZone`. Stations, displays and pads were placed by hand (positions below). See [[Archive/Art/Japanese Street#Shop and back-room workshop (2026-10-21)]].

Building frame: centre x 17.5, 48 wide (outer x −6.5…41.5, inner faces x −6.0 / 41.0). Front wall line z −577.5, partition z −605.75…−606.25 (door x 14.1…20.9, 8 high), back wall inner face z −656.25.

| Piece | Where / what |
|---|---|
| `Plot.Shop.Starter` / `Upgraded` | The shop room only (z −577.5…−605.75). Façade with the 12.5-wide entrance, side walls (posts at 15 and 25 behind the front), roof. The Starter is one storey with its 刀鍛冶 signboard on the roof; the Upgraded Store has the black kura upper storey, pent roof and signboard. Tags `TycoonItem` and `HidesRoof` and the `UntilUpgrade` / `Upgrade` attributes are unchanged |
| `Floor` / `InsideZone` (each shop) | Floor top 0.2 over the shop room. Zone 46.8 × 12 × 28.1, so the shop roof fades only in the shop room |
| `Plot.Workshop` | Shared, always shown. `Shell`: partition with the door (`Threshold`, indigo noren on the shop side), workshop walls (eave 15.5 since the lift, 13 before; door 10.5; high lattice windows outside), the supply alcove. `Shell.Roof`: roof with the smoke vent over the furnaces. `Floor` (stone, top 0.2), `InsideZone` 46.8 × 16.5 × 49.8. Tag `HidesRoof` |
| Supply alcove (placeholder ore source) | `AlcoveStage` (top 0.9) at x −6…3.6, z −647.65…−653.2, with an `AlcoveScreen`, `AlcovePost` and `AlcoveHeader`, and a dark `Hatch` with a `Chute` on the back wall. Ore slots `Smithy.OreRoller.Stand1..6` stand on it as cedar `Pedestal` trays with the ingot `Ore` on top: front row z −649.3, back row −651.9, x 1.95 / −1.15 / −4.25 (Stand1–3 front, 4–6 back). `OreRoller.Lever` + `Machine` (the RollPrompt) at x ≈ 5.9, z ≈ −651.5, east of the alcove |
| Stations (`workspace.Smithy`) | Back wall, west to east: alcove, `Forge` (11.5, −652.95), `Forge2` (19.5, −652.95), `Anvil` pivot (28.1, −650.5), `HiltBench` (35.5, −654.05). East wall, facing west: `PolishStation` (39.7, −634), `EtchingTable` (39.8, −620). West wall, facing east: `IngotRack` (−5.0, −626). Partition, east of the door, facing the workshop: `SwordRack` (27, −607.3). The Hilt Bench keeps facing +z: `HiltBenchController` puts its camera on the bench's world +z side |
| `Plot.Shop.Displays` | Wall racks with their `Origin` on the side walls: `WallRack1` (−6.0, −586), `WallRack3` (−6.0, −596), `WallRack2` (41.0, −586), `WallRack4` (41.0, −596). `DisplayTable1` (29.5, −583), `DisplayTable2` (29.5, −594) |
| `Plot.Shop.Interior` | Moved out of the Upgraded Store, so both shops have it: the counter front-left (body at 5.5, −583) and the tansu on the partition east of the door (27, −604.8) |
| `Plot.Shop.CommissionBoard` | Board with paper slips and a 依頼 header on the partition, west of the door. Decor only; no commission system yet |
| `Upgraded.Lanterns` | Wall lamps: two on the partition (x 3.5, 24), two on the west wall (z −581.5, −596) |
| `EntryPoint` | (21, 3, −581.5), just inside the entrance. `ShopService.AISLE_ROWS` = `ENTRY_POINT.Z + 1.5 / − 8 / − 18.5`: in front of Display Table 1, between the tables, behind Display Table 2. Every slot's route (EntryPoint → row → inspect point) and the walk in from `Village.CustomerSpawn` are clear by raycast at knee and chest height |
| `Plot.Pads` | Shop: `WallRack2` (38, −586.75), `WallRack3` (−3, −596.75), `WallRack4` (38, −596.75), `DisplayTable1/2` on the tables, `UpgradedStore` (9.5, −593). Workshop: `Furnace2` (19.5, −647.5), `OreStand2..6` all at (−1.15, −645.5) in front of the alcove (the chain shows one at a time), `IngotRack` (−2.5, −626), `PolishStation` (37, −634), `EtchingTable` (37, −620), `SwordRack` (27, −610.5) |
| `SpawnLocation` | (17.5, 0.2, −630), the workshop's open floor |
| `Plot.Yard.ShopFront` | Stone `Bridge` over the water channel at the entrance, and two pots |

- **`ForgeService`:** with no `OreRoller.CartPath` points (`still`), the stands stay put. A pull hides the ores, then each flickers through the materials and settles, with the cart timing (1.5 s + 2.5 s). The `Stop1..6` attributes are kept. Backup `Legacy.ForgeService_beforeAlcove`.
- **`Shared/Upgrades`:** `OreStand2..6` are named "Ore Slot 2…6" (ids unchanged). Backup `Legacy.Upgrades_beforeAlcove`.
- **Parked in `ServerStorage.Legacy.Plot_beforeBackRoom`:** the separate workshop hall, the courtyard paving and `LawnCurb`, the mine (`Track`, `MineCave`, `MineFace`), the `CartPath` points, the cart bodies (chassis, wheels, body, rim) and the six loose mine-frame parts. Earlier: `StarterShell_beforeMachiya` and `UpgradedShell_beforeMachiya` (feudal meshes), `ShopDressing_beforeMachiya`, `Mountains_parked`.
- In Edit both shops show at once and overlap; at runtime `TycoonController` hides one. To look at one, parent the other to ServerStorage for a moment.
- **Coplanar check (2026-10-21):** same-direction faces whose overlap is visible (not underground, not inside a third part). 537 new parts against 636 nearby; the 4 hits (alcove stage / wall post, hatch / wainscot, chute rails / hatch frame) were fixed and the alcove rechecked clean. Stations were checked against the walls: only intended contacts (trays 0.02 into the stage, racks 0.05 into the wainscot).
- **First furnace unlocked (2026-10-21, Allen):** `Smithy.Forge` had `Upgrade = Furnace2` and the `TycoonItem` tag like `Forge2`, so both furnaces stayed locked until Furnace 2 was bought. Both are removed from `Forge`, so players start with one furnace; `Forge2` is still the Furnace 2 upgrade.
- **`workspace.Plot` regrouped (2026-10-21, Allen):** `Shop`, `Pads` and `Yard` had ended up loose in Workspace, so `ShopService`, `TycoonService`, `TycoonController` and `ShopController` waited forever on `WaitForChild("Plot")`. They are back under a `Plot` Model (pivot (51, 0, −631)), which also carries the `OwnerId`, `OwnerName` and `Bought_*` attributes at runtime. `Smithy`, `SpawnLocation` and `Weapon Rack` stay at the top level; no script looks for them under `Plot`. Every start-up path in those four scripts resolves in Edit.

## Six player plots (2026-10-21)

Design and checklist: [[Design/Six Plots]]. Backups of every changed script: `ServerStorage.Legacy.Scripts_beforeSixPlots`.

| Piece | What it does |
|---|---|
| `Workspace.Plot` (Edit) | The template: `Shop`, `Workshop`, `Smithy` (moved in from `workspace.Smithy`), `Pads`, `Yard`, `PlayerSpawn` (the old `SpawnLocation`) and `CustomerSpawn` (marker on the road in front of the shop). `WorldPivot` = `Village.Lots.PlotSlotN2.CFrame` (since 2026-10-22 on the simplified map: pivot (640, 0.5, −292), `PlayerSpawn` (640, 0.2, −298), `CustomerSpawn` (641, 3, −231)) |
| `ServerScriptService.PlotService` (module) | On first require: template → `ServerStorage.PlotTemplate`, then an empty copy of the plot on every lot (`Village.Lots.Empty<lot>`, since 2026-10-22; see **Simplified map**). `PlayerAdded`: first free lot in `ORDER` (N2, N1, N3, S2, S1, S3), clone → `PivotTo(PlotSlot)`, name `Plot_<lot>`, attributes `Lot` / `OwnerId` / `OwnerName`, `onPrepare` hooks run on the unparented copy, the lot's empty plot → `ServerStorage.EmptyPlots`, parent, `RespawnLocation` = `PlayerSpawn` (a character already in the world is moved there), player attribute `Plot`, then `onPlot` hooks. `PlayerRemoving`: `onRelease` hooks, destroy, empty plot back. API: `plotOf(player)`, `plotFrom(inst)`, `ownerOf(inst)` |
| `PlotService` shop sign (2026-10-21) | On claim, every `Kanban` under the copy's `Shop` (Starter and Upgraded signboards) shows the owner's `DisplayName` instead of 刀鍛冶 (Allen: "the sign outside of the plot should have players name on it not that japanese text"). The template keeps 刀鍛冶 in Edit. Backup `Legacy.PlotService_beforeSignName` |
| `StarterPlayerScripts.MyPlot` (module) | `current()`, `get()` (yields until your plot exists), `owns(inst)`, `plotOf(inst)` (any plot: the ancestor with a `Lot` attribute) |
| `StarterPlayerScripts.PromptFilter` | Keeps every ProximityPrompt on other players' plots switched off on this screen (re-applied when the server turns one on) |
| `TycoonService` | `Bought_<id>` on each plot; `refresh(plot)` locks/unlocks that plot's `TycoonItem`s and shows its pads; `onPrepare(refresh)` so a new plot appears already locked; `BuyUpgrade` uses your plot's pad |
| `ShopService` | Slots know their plot; routes are built in the plot's own frame (`AISLE_ROWS` = plot-space z offsets −1.5 / 8 / 18.5 from `EntryPoint`), so south shops route correctly. Only the plot's owner displays. Each claimed plot runs its own customer spawner (2 at a time) from its `CustomerSpawn`. Slots removed with a plot unregister |
| `ForgeService` | Rewritten around plots: furnaces keyed by model with their plot; slot numbers global and never reused; one `Roller` (track or still mode, stands, rolling flag) per plot set up in `onPlot`; only the owner pulls; `onRelease` drops the plot's furnace slots. `ForgePut` finds the named furnace on the caller's plot |
| `RackService` | Racks on the caller's plot; each rack shows its owner's contents (fixes "whoever used them last") |
| `EtchService`, `PolishService` | Reach and bought checks use the caller's own station |
| `LeverAnimator` | One lever per plot, swings for its owner only |
| `AnvilController`, `ForgeController`, `HiltBenchController`, `RackController`, `EtchingTableController`, `PolishController` | Use `MyPlot.get().Smithy` instead of `workspace.Smithy`. The hilt-seating sword and camera turn with the plot (south plots face the other way) |
| `ShopController` | `+` markers only on slots of your plot |
| `TycoonController` | Locked items hidden on every plot; Buy button only on your plot's pads |
| `Village.CustomerSpawn` | No longer read (each plot has its own) |
| Upgraded Store | Side windows removed: in the continuous row they faced the neighbours' walls |

- **Fit test (Edit):** template copies on N1, N3, S1, S2, S3 made with PlotService's math; nothing solid touches a neighbour (roof eaves overlap like the townhouses'); copies removed.
- **Not tested:** anything multi-player. `PlotService` can't be required in Edit (it would move the template).
- **Server size** is still 60; set it to 6 in Game Settings.

## Taller shop and workshop (2026-10-21)

`build_shops.luau` takes the same `LIFT` 2.5 (Allen: "also make the buildings a bit taller, right now the entrance is barely taller than the player"): shop storey `G` 13.5 (was 11), entrance and lattice tops 9.7, beam 10.45, side-wall band 10.1…10.7, workshop eave 15.5 and inner door 10.5 (noren raised with it), shop `InsideZone` 14.5 tall, workshop 16.5. The Starter's eave overhang is 3.5 (was 3.6) so it never shares a plane with a low house's fascia. `Shop.Upgraded.Lanterns.WallLamp1…4` (hand-placed) moved up 2.5 with the band. Backup `ServerStorage.Legacy.Plot_beforeLift`.

## Shop grows on the upgrade (2026-10-21)

Allen first picked a storeroom that opens into the shop ("do 1."), then: "ideally, the shop expands upon upgrade the blacksmith area just gets pushed further back instead of our current version". So the storeroom is gone, and the upgrade moves the workshop.

| Piece | Where / what |
|---|---|
| Starter layout (the template, `build_shops.luau`) | Façade-frame z: shop room 1.5…29.75; the workshop's front wall at `PZ` 30 (door ±3.4, threshold, noren); workshop 30.25…80.25; back wall to `BZ` 80.75 |
| `Shop.Starter.Shell` | Side walls and roof to 30 (posts 1.05, 15, 25); its `CommissionBoard` on the workshop wall; `Shop.Starter.Tansu` there too (z −604.8 on N2) |
| `Shop.Upgraded.Shell` | Side walls (posts 1.05, 15, 25, 35), kura upper storey and roof to `SZ` 42; its `CommissionBoard`, `Shop.Upgraded.Tansu` (−616.8) and WallLamp1/2 (−616.65) on the back wall at 42. In the Starter layout these stand inside the workshop's front 12, hidden while the Upgraded Store is locked |
| `Floor` / `InsideZone` | Starter 1.4…29.8; Upgraded 1.4…41.8 |
| `TycoonService.pushWorkshopBack` | When `UpgradedStore` is bought: moves `Plot.Workshop`, every `Plot.Smithy` child, `PlayerSpawn` and the pads with attribute `Workshop` (Furnace2, OreStand2–6, IngotRack, PolishStation, EtchingTable, SwordRack) 12 in plot space (away from the street), and any character inside the workshop's `InsideZone` with them; moved pads lose their `PadVisual` and `refresh` rebuilds it. Then the usual unlock: the Starter hides, the Upgraded Store shows. Workshop back wall ends at 92.75, inside the 96-deep lot |
| `LeverAnimator` | Rest and pulled poses are relative to `OreRoller.Lever.Base`, so the lever still swings after the move |
| `Shop.Displays` | `WallRack3/4` at façade z 30 and `DisplayTable2` at 22 (Upgraded only) stand in the 12 the shop gains |
| `ShopService.AISLE_ROWS` | −1.5 / 8 / 21.5 from `EntryPoint` |

- ForgeService, RackService, EtchService and PolishService read station positions live, so they keep working after the move. In track mode (mine carts) the roller caches its track points and would need the same treatment; the placeholder alcove has no track.
- Checks:
  - Upgrade simulated on a copy in lot S2 (south-facing) with TycoonService's move: the shop floor ends at 41.8 and the workshop floor runs 42.2…92.3.
  - No Z-fighting on 410 parts, nothing solid touching the street, only the intended contacts.
  - All 18 slot routes and the walk to the workshop clear.
  - Starter layout on N2: no Z-fighting on 395 parts, 9 routes and the walk clear.
  - TycoonService and LeverAnimator compile; the lever's rest pose reproduces exactly.
- Superseded the same day: the storeroom version (the Starter's wall at 30 with sacks and crates behind it).
- Not playtested.
- **ShopService fix (2026-10-21):** `clearSlot` skips the `HolderPrompt` when it's already gone. A display slot destroyed with its plot (or at server shutdown) raised "attempt to index nil with 'Enabled'" (15 times in Allen's playtest log).

## Town redesign (2026-10-22)

*Not chosen: parked 2026-10-22 as `ServerStorage.Legacy.TownRedesign_v2_parked` (v1: `Legacy.TownRedesign_before_20261022045159`); `build_town.luau` is retired.*

`Workspace.TownRedesign` (Model, pivot (17.5, 0, −200)): a candidate replacement for `Workspace.Village`, built beside it so Allen can compare. Brief, layout, images and checks: [[Art/Town Street Redesign References#Built for comparison (2026-10-22)]]. No script reads it. Built by `Models/Village/build_town.luau` (seed 22; Studio copy `ServerStorage.Builders.build_town`, run with `loadstring`). A rebuild moves the previous model to `ServerStorage.Legacy`.
- **Frames:** one north frame, x along the street and the north side at −z. The south side is the same plan turned 180° about the pivot.
- **Fronts:** at depth 36 (72 apart). Lots 2 and their neighbours sit at 56 (112 apart).
- **Lanes:** between frame x −107 and −83, ending at depth 150.
- **Ends:** gate at x −300, plaza x 300…356, invisible `Bound` walls at depth 190 and x −330 / 360.
- **Ground tops:** road / market / lane road 0.2, plaza 0.25, water 0.26, walkway 0.3 (lanes 0.34), curbs 0.5 (lanes 0.54).
- `Street`: `Road`, `Market` ×2, the main fronts' `Walkway` / `Curb` / `Water`, and lot-corner lamps (`LampFoot`, `LampPost`, `Andon` with a PointLight, `LampCap`).
- `Rows`: 30 townhouses on the main street (41 in v1).
- `Lanes`: `LaneRoad`, lane fronts, 10 lane townhouses (14 in v1), `LaneEndN` / `LaneEndS` (no door bridge) and `LaneEndWalk`.
- `Lots`: `PlotSlotN1..N3` / `S1..S3`, the same size, height, `Side` attribute and street-facing LookVector as `Village.Lots`, and the lot walls. `TAKEN` lists every lot, so there are no `Closed*` fronts in this build.
- `Market`: 8 `Stall` models, planters. `Trees`, `Landmarks` (gate, gate walls, plaza, torii, stone lanterns, `Shrine`).
- `PlotPreviews.Preview_<lot>`: copies of `Workspace.Plot` (624 parts each) at each slot, as a new player first sees it. Removed: `TycoonItem`s with an `Upgrade` attribute, `Pads`, `PlayerSpawn`, `CustomerSpawn`, every ProximityPrompt / ClickDetector / SpawnLocation, all tags and the root's attributes. They are snapshots of the template.
- **Calmer fronts (v2, 2026-10-22):** the builder's copy of the house kit differs from `build_street.luau`:
  - `spec(prevH, style)` takes an optional style;
  - `widths()` picks 24…34 and splits anything over 40;
  - a rafter flush with a beam end moves 0.05.
- **Styles and dressing:**
  - `houses()` takes one style per run (`MAIN`, `MARKET`, `LANE`). Corner houses (`CORNERS`: street ends, lane corners, step) are `kura` or `gable` and 30 deep.
  - Non-kura houses keep a sign 30% and a lantern 40% of the time. Metal roofs become tile.
- **Paving:** `paving()` puts the `TownFlagstone` MaterialVariant on the road, market and lane roads, tinted (226, 220, 208).
  - The variant is AI-generated, in `MaterialService.AssistantMaterials`, on Pavement, `StudsPerTile` 24 (set by hand from 10).
  - Without it the paving is plain Pavement.
- **v1** (busier fronts, herringbone paving) is kept as `ServerStorage.Legacy.TownRedesign_before_20261022045159`.
- **To make it the live street** (not done): set `TAKEN` to the template's lot only and `PREVIEW_PLOTS = false`, then rename it `Village`, or point `PlotService` at it. The template `Workspace.Plot` also has to move onto the new `PlotSlotN2`, or the town has to move onto the old pivot.
- **Checks:**
  - 0 visible coplanar pairs over 9,067 parts (v2; 50-stud slices, a hit counted only inside its own slice).
  - No solid street part inside a plot copy.
  - Every lot's `CustomerSpawn` → `EntryPoint` walk is clear at y 2 and 4.
  - Not playtested: in Play, PlotService places players on the current street.

## Simplified map (2026-10-22)

**The live map since 2026-10-22** (Allen: "I compared them. Make the simplified map the live map."). `Workspace.Village` (Model, pivot (640, 0, −200)) is the simplified six-plot map from image 06 and the brief at the top of [[Art/Town Street Redesign References]]. It was first built as `Workspace.TownSimple` beside the others; the notes below describe that comparison build, and the switch is listed at the end. Layout, images and checks: [[Art/Town Street Redesign References#Simplified map built (2026-10-22)]].
- **Builder:** `Models/Village/build_simple.luau` (seed 23). Studio copy `ServerStorage.Builders.build_simple`, run with `loadstring`. A rebuild moves the previous model to `ServerStorage.Legacy`. Its house code (part … spec) is `build_town.luau`'s.
- **Frames:** as in the redesign: a north frame, with the south side turned 180°. Gate, shrine and their walls are placed in world terms (`m` flips frame x on the south side).
- **Lots:** at frame x −72.5, 0, 72.5, with fronts at depth 36, 44, 36.
- **Lane exit:** the lane at frame x −48.25…−24.25 runs on past the back wall (depth 156) to the bounds (depth 190).
- **Walls and bounds:** gate line x −150, shrine plaza x 150…196, east wall x 198. Invisible `Bound` walls at x −180 / 208 and depth 190.
- **Ground tops:** lane paving 0.12, plot `Pad` 0.16 (under the plot's 0.2 floors), `Road` / `Junction` 0.2, `Plaza` 0.25, water 0.26, walkway 0.3, `Edge` 0.36, curbs 0.5.
  - `Road`, `Junction` and `Paving` use the `TownFlagstone` MaterialVariant. The paving is tinted (178, 170, 158).
- `Street`: `Road`, `Paving` ×4, `Junction` ×2, the lots' and end houses' walkway / curb / water strips, the outer houses' `Walkway`, and lot-corner lamps.
- `Lots`: `PlotSlotN1..N3` / `S1..S3`, with the same size, `Side` attribute and street-facing LookVector as `Village.Lots`. Also the earth `Pad`s and stone `Edge`s. No `Closed*` fronts, since `TAKEN` lists every lot.
- `Houses`: `EndN1/2`, `EndS1/2` (low style, 20 × 16, on the street front at x ±132.75, with walkway and channel) and `OuterN` / `OuterS` (20 × 14, facing the lane outside the back wall, no door bridge).
- `Walls`: `wallSeg` pieces (along z or turned along x) ending 1 short of the `Pillar`s at corners and lane exits.
- `Landmarks`: gate, plaza, torii, stone lanterns, two trees, `Shrine`.
- `PlotPreviews`: the same inert copies of `Workspace.Plot` as in the redesign.
- **Checks:**
  - 0 visible coplanar pairs over 4,190 parts;
  - no solid part inside a plot copy;
  - every lot's `CustomerSpawn` → `EntryPoint` walk is clear at y 2 and 4.
  - Not playtested.
- **Made the live map (2026-10-22):**
  - **Builder:** builds `Workspace.Village`; the previous `Village` moves to `Legacy`. No closed fronts (`TAKEN` and that code are removed) and no preview plots.
  - **Moved out:** the old street → `Legacy.Village_before_20261022052609`, the redesign → `Legacy.TownRedesign_v2_parked`. The `TownSimple` comparison copy was deleted.
  - **Template:** `Workspace.Plot` was pivoted onto the new `PlotSlotN2` (pivot (640, 0.5, −292)). After any rebuild of the map, pivot it there again.
  - **Scripts:** `PlotService` only reads `Village.Lots.PlotSlot*` and copies the template onto each slot. Its closed-front code was replaced the same day (below).
  - **Checks with the real template:**
    - 0 coplanar pairs over 2,118 parts (street and the template's Starter view);
    - no solid street part inside the template, with Starter and Upgraded both present in Edit;
    - the N2 customer walk is clear.
  - Not playtested. Loose top-level models left where they were: `Weapon Rack` (by the old street), the old courtyard `Courtyard` part and model, `Bamboo1…12`.
- **Empty plots instead of closed fronts (2026-10-22, Allen: "Why don't you just have all 6 player plots on the map. no need to replace them with another empty building when its already empty"):**
  - `PlotService`'s closed-front block is replaced. At startup it puts an empty copy of the template on every lot as `Village.Lots.Empty<lot>`.
  - **Stripped from each copy:** `TycoonItem`s with an `Upgrade` attribute, `Pads`, `PlayerSpawn`, `CustomerSpawn`, every ProximityPrompt / ClickDetector / SpawnLocation, every tag except `HidesRoof`, and the root's tags and attributes.
    - `ShopService` / `ShopController` (`DisplaySlot`) and `TycoonController` (`TycoonItem`) ignore them.
    - `PromptFilter` finds no prompts on them.
    - `RoofHider` still fades their roofs for a visitor.
  - **Claim and release:** a claim moves the lot's empty plot to `ServerStorage.EmptyPlots`; release puts it back.
  - Backup: `Legacy.PlotService_beforeEmptyPlots`.
  - **Checks:**
    - PlotService compiles;
    - its empty-plot block, run verbatim in Edit on the real lots and template, makes 6 copies (3,744 parts) with 0 prompts and 0 spawns, and only `HidesRoof` tags left (12).
    - Not required in Edit, since requiring it would move the template.
- **Plots a full frontage apart (2026-10-22, Allen: "Also expand the map and separate the houses more"):**
  - **Lots:** at frame x −96.5, 0, 96.5 (world x 543.5, 640, 736.5) with 48-wide lanes; the continuing lane is frame x −72.25…−24.25.
  - **Edges:** end houses at x ±180.75, gate line x −200, plaza x 200…246, east wall x 248, back walls at depth 172, bounds at x −230 / 258 and depth 210.
  - **Unchanged:** the street (fronts 72 apart, middle pair at 44) and the N2 slot, so the template didn't move.
  - **Size:** the map is about 490 × 420, bounds included.
- **Gable-front roofs: tried and undone (2026-10-22).**
  - **Tried:** Allen: "Also can we try to rotate the roofs so the sides so looking at it front on, the slant is left right". The shop, workshop and small houses got gable fronts, ridges running back from the street.
  - **Undone:** Allen: "actually undo it so the roofs face the entrance". The roofs have their eaves to the street again, exactly as before (`mainRoof` in `build_shops.luau`; the kit's default roof for `smallHouse`). Pictures of the try: `References/Town Street Redesign/gable-try-*.jpg`.
  - **Kept from it:** `build_shops.luau` builds wherever `Workspace.Plot` stands (`SHOP_CF` = the template's pivot, 48 toward the street), so it works on the new map.
  - `Legacy.Plot_beforeGableRoofs` is a copy of the template before the try, the same as now.
  - **Checks after the undo:**
    - 0 coplanar pairs over the whole map and the template's Starter view (1,145 parts);
    - 0 on a copy in the Upgraded layout with the workshop pushed back 12 (one apparent hit was a street face hidden by the road, which that local check left out).
    - Not playtested.

## Workshop layout (2026-10-22)

Allen's request: redesign the workshop interior from a screenshot of the old one (vault: [[Art/Workshop Layout]]).

`Models/Village/build_workshop.luau` (Studio copy `ServerStorage.Builders.build_workshop`, run with `loadstring` after `build_shops`) works on `Workspace.Plot` in its Starter layout.
- **Rerunnable:** stations go to fixed places, and models with `BuiltBy = build_workshop` are rebuilt.
- **Frame:** `build_shops`' shop frame: the template's pivot × (0, −0.5, −48). x runs across, +x is the left wall seen from the door; z runs from the façade.
- **Inside the workshop:** x ±23.5, z 30.25…80.25, floor top 0.2.

| Piece | Where / what |
|---|---|
| `Forge`, `Forge2` | Moved so their `Model3D` plinths sit on the hearth (top 0.8) at x 6 / −2, z 75.3: 1.65 between the furnace backs and the back wall. `Base`, `HeatPrompt`, `Door`, `Fire` move with them |
| `Anvil` | Body centre (2, 64.5), still facing the furnaces; the face is 0.78 higher (top 3.28). `Anvil.Stump`: `Stump` 2.0 across and 0.8 tall, two iron `Band`s, a `Flare` 2.8 across and 0.25 tall. The smith's spot (strike frame × (−0.45, 0, 1.6)) is (1.9, 62.9) and clear |
| `HiltBench` | Turned to face the right wall (LookVector −x). `Top` (HiltPrompt) at (−21.5, 2.85, 70.5) inside the counter. `Model3D` is now the hilt section (z 66…75); `Model3D.Top` is its counter, where HiltBenchController lays the sword |
| `PolishStation` | Same turn as before. `BladeMount` at (−21.35, 3.22, 65.2); `Model3D` is the polishing section (z 57…66) |
| `EtchingTable` | `Top` (EtchPrompt, and the etching show's surface) at (−21.5, 2.85, 52.5), flush with the counter, now invisible. `Dress` is the etching section (z 48…57) |
| Bench sections | Each has a `Plinth`, `Carcass` and counter (x −23.3…−19.7, top 3.0), plus a `Rail`, `Stile` and `Pull`s; a 0.06 gap between sections. Hilt: `MountBase`, `MountCheek` ×2, `FittingsBoard`, `Tsuba` ×2, `MalletHead`/`MalletHandle`, `Punch`. Polishing: `Stone`, `TrayBase`/`TraySide`/`TrayEnd`/`TrayWater`, `Cloth`. Etching: `Cradle` ×4, `Blank`, `StylusRest`, `Stylus`, `StylusPoint`, `InkPot` |
| `OreRoller` | `Stand1…6` trays at x 15.4 / 18.5 / 21.6, z 74.9 (1–3) and 77.5 (4–6), heights unchanged. `OreRoller.Chest`: `Floor` (top 0.87), `Front` (top 1.3), `Back`/`Side` (2.0), `Divider` ×3, `Strap` ×2, `Lid` leaning on the back wall. `Lever` and `Machine` unchanged at x 11.6. The chest became `LootBox` the same day: see **Ore loot box (2026-10-22)** |
| `IngotRack`, `SwordRack` | Unchanged at (22.5, 50) and (−9.5, 31.3) |
| `Smithy.WorkshopFittings` | `Hearth` x −6…10, z 71.1…79, top 0.8, and `HearthKerb` (top 0.88). `AnvilStone` 9 across at (2, 64.2), top 0.26. Right wall: `ToolRail` z 58…74, y 6…6.35, with 6 tools on `Peg`s, and `Shelf` z 49…55, y 6. Left wall: `Shelf` z 60…66, y 5.6. Back wall: `ToolRail` x −13.5…−8 with tongs and a `Poker` |
| `Plot.Pads` | `PolishStation` (−17.2, 61.5), `EtchingTable` (−17.2, 52.5), `Furnace2` (−2, 68.4), `OreStand2…6` (18.5, 71.2). Shop pads, `IngotRack` and `SwordRack` unchanged |
| `build_shops.luau` | The supply alcove is removed: `AlcoveStage`, `AlcoveScreen`, `AlcovePost`, `AlcoveHeader`, `Hatch`, `HatchFrame` ×3, `Chute`, `ChuteRail` ×2 |

- **Scripts changed:**
  - `HiltBenchController`: `turn = HiltBench:GetPivot().Rotation`, instead of the plot's pivot turned 180°. That was the same rotation for the old bench, on either side of the street. Compiles.
  - `EtchPlayback.IN_THE_WAY` gets `"Cradle"`. Compiles, and a fresh clone loads.
  - Backups: `Legacy.HiltBenchController_beforeWorkshopLayout`, `Legacy.EtchPlayback_beforeWorkshopLayout`.
- **Locking:** the polishing and etching sections are inside their stations, so `TycoonService.setLocked` turns off their collisions, queries and prompts, and `TycoonController` hides them. The hilt section, stump, chest and fittings are never locked.
- **The push:** `pushWorkshopBack` moves every `Smithy` child, so all of it moves.
- **Backups:**
  - `Legacy.Plot_beforeWorkshopLayout`: the whole template before.
  - `Legacy.Workshop_beforeLayout`: the Blender hilt bench, the polishing station model and the etching table's dress.
- **Checks in Edit:**
  - **Access:** for all 15 stations and ore slots,
    - the standing spot is clear of solid parts;
    - the prompt is within `MaxActivationDistance` (ore slots 8);
    - the server reach (forge 14, polish / etch / racks 12) is met;
    - PathfindingService (radius 1, height 5) finds a path from the shop door and from `PlayerSpawn`.
  - **Cameras:** the hilt, polishing, anvil and etching eyes, computed with each controller's formula (FOV 70, 16:9, tanto / wakizashi / katana), are all inside the workshop with a clear line to the blade, and each blade fits its section.
    - The hilt sword (z 68.2…74.2) ends in the blade mount's notch.
    - The same eyes relative to the workshop on lot N1, on lot S2 and after the push: 0.0000 studs difference.
  - **Z-fighting:**
    - workshop and stations, everything present: 0 pairs over 423 parts;
    - new plot, workshop upgrades bought, and everything bought with the push: only the shop front's `Post` / `Kick` bottoms, which the street walkway hides (the tongs pairs found on the first run were fixed).
  - **States:**
    - the locked set is unchanged;
    - pads stand on clear floor;
    - the push moves 22 objects by exactly 12, and the deepest point is 46.99 of the lot's 48;
    - PlotService's empty plot from the new template has 0 prompts and only `HidesRoof` tags.
  - **Not done:** Play.

## Ore loot box (2026-10-22)

Allen: "try to make our ore roller look like a Call of Duty loot box, where you open it, the ore floats around and spins its different types, and then falls down onto the lootbox again", and "players need to pick up their ores before rolling again". Picture and summary: [[Art/Ore Loot Box]].

| Piece | Where / what |
|---|---|
| `OreRoller.LootBox` (`build_workshop.luau`, replaces `OreRoller.Chest`) | Box x 13.9…23.3, z 73.7…78.3, top 1.75, wood (178, 112, 62): `Front`, `Back`, `Side` ×2, `Inside`, `Seam`, `Handle`, `Strap` ×2. `Lid` is a model (`Board` 0.4 thick + `Strap` ×4) whose `WorldPivot` is the hinge; `Hinge` is an invisible part on the same CFrame, at the lid's back bottom edge (18.6, 1.75, 78.35). `Glow` is an invisible part inside with a `PointLight` (255, 190, 110), range 12, brightness 0 |
| `OreRoller.Stand1…6` | On the lid: x 15.45 / 18.6 / 21.75, z 74.85 (1–3) and 77.15 (4–6), the `Ore` 0.01 over the lid. `Pedestal` is invisible and only holds the `CollectPrompt`. The template's `Ore`s are hidden, so empty plots show a bare lid; ForgeService shows them on a reveal |
| `Lever`, `Machine` | Unchanged at x 11.6 |

- **`ForgeService`** (backup `Legacy.ForgeService_beforeLootBox`):
  - **Collect first:** `refreshLever()` enables `RollPrompt` only while no roll runs and no stand holds a `materialId`. It is called at setup, on a collect, and at the start and end of a roll. The Triggered handler also returns if any ore waits.
  - **A pull** rolls every unlocked stand.
  - **Box mode** (no `CartPath` points):
    - The results are rolled at the pull and stored in `Stand<n>.Result` (material id), `OreRoller.RollStands` ("1,2,…", pull order) and `OreRoller.RollAt` (`workspace:GetServerTimeNow()`).
    - Then it waits `BOX_TIME` 3.6 (also published as `OreRoller.RollTime`) and calls `reveal()` on each stand: shown, painted, labelled, `CollectPrompt` on. If the player left, the stand is cleared.
  - **Cart mode** keeps `rollOut`, now `moveCart` → `reveal` → the pop.
- **`StarterPlayerScripts.OreBoxShow`** (ModuleScript): `new(roller, stands, results)` returns `{ pose(t), destroy() }`.
  - **Copies:** it copies each stand's `Ore` as `RollingIngot` into `LootBox`, with no collision or queries, no tags and a `PointLight` in the rarity colour.
  - **`pose(t)`:** turns the `Lid` about `Hinge` (`Hinge.CFrame * Angles(a, 0, 0) * lidRest`), sets the `Glow` brightness and places each copy. It removes a copy in the frame its real `Ore` turns visible. It returns false once no copies are left.
  - **`destroy()`:** puts the lid back, sets `Glow` to 0 and removes the copies.
- **`StarterPlayerScripts.OreBoxAnimator`** (LocalScript):
  - **Watching:** it watches every `OreRoller` in workspace, including ones streamed in later, for a new `RollAt`. A roll older than `RollTime` is skipped.
  - **Playing:** on `RenderStepped`, t = server time − `RollAt`. A show ends when its copies have all given way, at `RollTime` + 1.5, or when the roller is gone.
- **Timeline** (`OreBoxShow` constants):

| Constant | Value | Meaning |
|---|---|---|
| `OPEN`, `OPEN_ANGLE` | 0.4 s, 90° | The lid opens, ease-out-back, about 99° at the peak |
| `RISE_AT`, `RISE` | 0.2 s, 0.55 s | The copies rise from the `Glow` height under their slot |
| `HOVER`, `BACK_ROW` | 4, +1 | Studs over the slot; the back row is higher, so the rows never touch while spinning and the shutting lid passes under them |
| `TURNS`, `FLICKERS` | 6, 18 | Spins and material changes until lock-in, both on an ease-out curve |
| `LOCK_AT`, `LOCK_GAP` | 2.0 s, 0.12 s | Lock-in of copy k at 2.0 + (k − 1) × 0.12: 1.3× pop over 0.3 s, rarity light flash over 0.4 s |
| `SHUT_AT`, `SHUT` | 2.75 s, 0.3 s | The lid shuts |
| `DROP_AT`, `DROP_GAP`, `DROP` | 3.05 s, 0.03 s, 0.35 s | Each copy drops onto its slot; the sixth lands at 3.55 |

- **Checks in Edit:**
  - **Load:** `ForgeService` and both client scripts compile, and a fresh clone of `OreBoxShow` loads.
  - **The show:** stepped every 0.01 s to 3.62 with all six slots, with the lid straps queryable for the test.
    - The copies never overlap the lid or each other.
    - The lid reaches plot z 79.53 against the back wall's inner face at 80.20.
    - Each copy ends on its slot at full size.
    - `destroy()` puts the lid back to 0.0000 and leaves no copies.
  - **The push:** moving a copy of the roller by 12 keeps the `Lid` pivot on `Hinge`, so the push is safe.
  - **Z-fighting:** 0 pairs from the box. The one pair in that corner, `Wainscot` / `Plaster` inside a back-wall `Post`, is in `Legacy.Plot_beforeLootBox` too.
  - **Access:** the standing spot in front of the box is clear, PathfindingService reaches it from the shop door, and the farthest `CollectPrompt` is 6.46 from it (max 8).
  - **Not done:** Play, network timing, two players.

## First sword and delivery bay (2026-10-22)

Allen picked two quick thoughts: "first time tutorial, the furnace and other processes need to be sped up", and "each plot should have an area where we can eventually add a delivery carrier. maybe a guy with a carriage. potentially could carry over into the street."

**The first sword**
- **`ForgeService`** (backup `Legacy.ForgeService_beforeFirstSword`):
  - `HEAT_TIME` is 10 (the GDD's approved base; it was still 15).
  - `FIRST_HEAT_TIME` is 3. It is used when the player puts an ingot in while `SmithyCore.getData(player).completed == 0`, i.e. before their first sword is finished.
  - Each slot's warming uses its own `readyAt - startedAt`.
- **`SmithyCore`** (backup `Legacy.SmithyCore_beforeFirstSword`): `SmithData.sold`, starting at 0. A fresh clone loads.
- **`ShopService`** (backup `Legacy.ShopService_beforeFirstSword`):
  - An accepted offer adds 1 to the owner's `sold`.
  - `sendCustomer(plot)` sends one walk-in now unless `MAX_CUSTOMERS` are already on their way. It keeps its count per plot in `onTheWay` and replaces the onPlot loop's local count; the loop calls it every `SPAWN_MIN..SPAWN_MAX` seconds as before.
  - `DisplaySword` calls it when the player's `sold` is 0, so until the first sale a listed sword brings a customer at once.
- **Kept as they were:** the roll (1.5 s hold and the 3.6 s box), the anvil's hits and the hilt's three knocks, since they are active steps. The tutorial's fair first offer and on-screen guidance are not built.
- **Session-only:** like coins, `completed` and `sold` start again at 0 on every join until the DataStore pass, so every visit gets the quick first sword.

**The delivery bay**
- `Plot.DeliveryBay`, built by `build_workshop.luau` (`BAY`), a child of the plot rather than `Smithy`, so the Upgraded Store's push leaves it beside the shop.
- **Where:** the lots are full width (the shop and workshop fill 48.5), so the bay is in the lane on the plot's +x side, which is the left of the shop seen from the street. Every lot uses its own +x side, so each lane holds one bay per row (N1's is in the open strip at the west end).
- **Pieces:**
  - `Yard`: packed earth, x 24.9…40.9, z 2…34, top 0.16, 0.04 over the lane's paving. Its shop side is under the village's lot kerb (`Lots.Edge`, x 24.3…25.1, top 0.36).
  - A post-and-rail fence (`Post`, `Rail`) on the lane side and at the back.
  - A gateway at the street end: two 0.6 posts at x 26 and 40.55, a `Lintel` at 8.3…8.9 and a `TieBeam`, with 14 clear between the posts.
  - Three `Crate`s in the back corner by the shop.
  - `CartSpot`: invisible, 6 × 14, at (33, 19), facing the street; it marks where a cart will stand.
- **Nothing works there yet:** no prompts, tags or scripts. It is space for the delivery board (GDD 9.1).

**Checks in Edit**
- `ForgeService` and `ShopService` compile; `SmithyCore` and the builder load; the builder matches the vault copy byte for byte.
- **Z-fighting:**
  - 0 pairs between the bay and anything near it, with the Starter or the Upgraded Store shown (a first run found the lane-side gatepost's face on the yard's edge; the fence lines moved 0.05 in).
  - Placed on each of the six lots: 0 pairs and no village part inside a post, rail, crate or the gateway.
  - Pre-existing pairs elsewhere in that area are hidden: `Workshop.Shell` wainscot / plaster / band joints inside posts, and the street's `Paving` / `Junction` faces at the road's edge.
- **The cart's way:** a 7-wide lane from the gateway to the back of the yard is clear.
- **Not done:** Play (the 3 s first heat, the first customer, the second sword at 10 s).

**The delivery door** (same day). Allen asked: "When delivery is unlocked, is there a way to have a door to the delivery bay?", then, to build it hidden: "Until delivery is unlocked."
- **Where:** both shop shells have the same wall bay on the +x side, between the posts at z 15 and 25, beside the bay's `CartSpot`, with nothing inside in front of it.
- **Built by `build_workshop.luau`** (`DOOR`):
  - It removes that bay's `Wainscot` and `Plaster` from `Shop.Starter.Shell` and `Shop.Upgraded.Shell`, found by position, so a rerun of `build_shops` followed by `build_workshop` ends the same.
  - **`Shop.DeliveryWall`:** TycoonItem, `UntilUpgrade = "Delivery"`. The same panel, wainscot (x 23.45…24.05, y 0…3.2) and plaster (x 23.5…24.0, y 3.1…12.8), z 15.3…24.7.
  - **`Shop.DeliveryDoor`:** TycoonItem, `Upgrade = "Delivery"`. The wall round an opening at z 17.75…22.25, 7.8 high.
    - Frame: `Jamb` ×2, a `Lintel` across the bay (y 7.8…8.3, ending inside the posts) and a `Sill` (top 0.3).
    - Wall: side `Wainscot` and `Plaster` pieces ending inside the posts and jambs, and a header `Plaster` from 8.2.
    - The sliding `Door`, pushed open along the inside of the wall (z 22.3…26.7) with two `Batten`s.
    - Two indigo `Noren` strips outside, not solid.
- **Why outside the shells:** `TycoonController` shows or hides an item with all its descendants, and `TycoonService` keeps one saved state per part. An item inside the Starter or Upgraded shell would be shown with the shell, or come back without collisions.
- **Hidden for now:** `Shared/Upgrades` has no `Delivery` entry, so `TycoonService.refresh` locks the door on every plot and the wall stays.
  - To unlock it, add an upgrade with id `Delivery` and a `Plot.Pads.Delivery` marker.
  - PlotService's empty plots drop the door and keep the wall.
- **Backup:** `Legacy.Plot_beforeDeliveryDoor`.
- **Checks in Edit:**
  - **Z-fighting:** 0 pairs from the wall or the door in all four states (Starter or Upgraded × delivery locked or bought). The other pairs there are the shells' own wainscot / plaster / band joints inside posts at z 1.3 and 34.7 and the workshop's.
  - **Fit:** the doorway is clear for a walking character, and the slid door touches nothing.
  - **Empty plot:** an empty plot made PlotService's way has the wall and no door.
  - **Pictures:** `References/Delivery Bay/door-from-bay.jpg`, `door-from-shop.jpg`, taken with the wall and the Starter shell set aside for the shot.

## Fair first offer (2026-10-22)

The GDD's approved tutorial rule (§8, 2026-10-19): the first customer makes a guaranteed fair offer, and haggling is taught on the second ordinary sale. Allen picked it from the roadmap.

- **`ShopService.runCustomer`** (backup `Legacy.ShopService_beforeFairOffer`):
  - It reads the owner's `SmithyCore` `sold` count when the customer starts offering.
  - **`sold == 0` (first):** the offer is exactly `SmithyCore.swordValue(sword)`, whoever the customer is and whether or not they like the sword (`liked` is false, so the card shows no "They love it"). A decline gets no counter-offer: the customer says "No deal, then." and leaves.
  - **`sold == 1` (teach):** a normal offer. The first offer goes out with `teach = true`, and the first decline always brings a raise (`Customers.raise(…, sure)`). Later declines follow the customer's usual patience and raise chance.
  - From `sold == 2` on, the usual rules apply.
  - Commission deliveries will not touch `sold` (only an accepted shop offer adds to it).
- **`Shared.Customers.raise`** (backup `Legacy.Customers_beforeFairOffer`): a new optional `sure` argument skips the patience and chance checks. Checked on a clone: with `sure`, a customer with patience 0 and raise chance 0 raised 200 times out of 200; without it, never.
- **`ShopController`** (backup `Legacy.ShopController_beforeFairOffer`): a `Hint` line (a copy of `OfferCard.Detail`, terracotta) under the details reads "Decline and they may offer more". It shows only when the offer has `teach`, and the card grows 18 for it.
- **Checks in Edit:**
  - all three scripts compile, and a fresh clone of `Customers` loads;
  - the card with the hint was previewed in the viewport and then restored (`References/Tutorial/offer-haggle-hint.jpg`);
  - not tested: Play.

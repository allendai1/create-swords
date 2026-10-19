---
title: Smithy Redesign Proposal
status: built in Studio 2026-10-19 (A/B mix); playtested; place saved
date: 2026-10-19
tags: [art, environment, stations, studio, create-swords]
---

# Smithy Redesign Proposal

The stations in `Workspace.Smithy` are still blockouts from the medieval-cabin prototype. This note looks at what's there now and proposes how to rebuild each station, and the workshop around them, for the approved Japanese mountain-village setting ([[Create Swords! GDD]] §11). It builds on [[Japanese Village Concept Art]] (forge, hornless anvil, village map, evening scene). **Chosen 2026-10-19: a mix.** Direction A's materials and colours, with Direction B's chunkier proportions and extra lanterns. See [[Decisions Log]].

## Built (2026-10-19)

All five stations and the workshop are rebuilt in Studio in the chosen mix. The scripted parts are unchanged except where the table in [[Code Map]] says so. Allen saved the place with it on 2026-10-19.

![[References/Smithy Redesign/built-front.jpg]]

| Station | Built |
|---|---|
| Forge | ![[References/Smithy Redesign/built-forge.jpg]] |
| Ore shrine | ![[References/Smithy Redesign/built-ore-shrine.jpg]] |
| Anvil | ![[References/Smithy Redesign/built-anvil.jpg]] |
| Hilt Bench | ![[References/Smithy Redesign/built-hilt-bench.jpg]] |
| Holders, mid-sale | ![[References/Smithy Redesign/built-holders-sale.jpg]] |

![[References/Smithy Redesign/built-forging-camera.jpg]]

**Playtest (one full loop, real key presses and clicks):**

- Rolled a Blue Steel ingot at the lever.
- Loaded it at the forge: the ingot sat on the new tray, and the timer showed.
- Took it out hot and forged a katana to 90% on the new anvil.
- Fitted a hilt at the bench.
- Displayed it on the middle pedestal. A Village Farmer walked in through the open front and offered 382 coins, and the sale went through.

No script errors or warnings in the log, apart from Roblox's own UI warnings.

**Fixed after the playtest:**

- The cooled steel blade was hard to see on the iron face under the warm light, so the face is darker now.
- The noren were blocking the camera near the shop front, so they're shorter now.

**Still open:**

- The grinding stage wasn't played through.
- The forge timer is still 15 s in ForgeService (the GDD says 10 s); that wasn't part of this task.
- The forge chimney only just clears the ridge.
- The plot is one workshop on open grass: no mountains, trees or neighbouring plots yet.

## What's there now

![[References/Smithy Redesign/current-overview.jpg]]

Five props stand in a straight line on the default grey baseplate, about 6 studs apart, with no building, ground or lighting around them. Each is 4–9 plain blocks with Roblox's stock materials (Cobblestone, DiamondPlate, Plastic). The browns all look alike, and nothing says "Japan". The leftover prototype blocks out east (`store`, `creation area`, and two slabs called `Part`, one of them unanchored and 236 × 198 studs) are unused. Lighting is the default 2:30 pm with flat grey ambient.

| Station | Now | Critique |
|---|---|---|
| **Ore Roller** | Diamond-plate box, wooden hopper with a rock slab, toy red-ball lever, chute and tray. 3.4 studs tall | Reads as a slot machine or factory press. It has one lever and no stands, but the GDD now wants **one shared lever plus material stands** whose ore visibly cycles and stops. The only "ore" cue is a flat rock slab. |
| **Forge** | Cobblestone box, flat neon-yellow rectangle, a stepped hood and a thin chimney. 6.2 tall | Looks like a fireplace. No bellows, the most recognisable part of a Japanese forge. The two heating slots exist only as invisible parts on a ledge, so ingots float in front of a flat glow instead of sliding into a chamber. |
| **Anvil** | Navy-black western anvil with a wedge horn on a cylinder stump | The horn is western; a Japanese *kanatoko* is a plain block. From the forging camera ([[#Readability from the forging camera]]) the face reads well, but the grid baseplate fills the frame and the forge and bench poke in at the edges. |
| **Hilt Bench** | Plain 4-leg table with two sticks and a guard | Nothing says "fitting hilts". The spindly legs read thin next to the other stations. |
| **Display Rack** | A 4 × 5-stud plank wall with three pegs | A blank wall that blocks the view through the shop. The three holders have no identity of their own, which matters because holders are a per-holder upgrade. |

![[References/Smithy Redesign/current-roller-forge.jpg]]
![[References/Smithy Redesign/current-anvil.jpg]]
![[References/Smithy Redesign/current-bench-rack.jpg]]

## Two directions

Both use the same shapes, layout and kept parts. They differ in how stylised they are:

- **A · Working kajiba (recommended).** A grounded Japanese smithy: white plaster, dark charred-cedar timber, grey tile roof, clay and stone hearth, iron, with vermilion and indigo as small accents. It matches [[Japanese Village Concept Art]] and the Swordsmith Village atmosphere reference. The props still use chunky Roblox proportions so they read at a distance.
- **B · Festival smithy.** The same buildings, pushed toward *Create Pottery!* toy-likeness: posts and trim 20–30% thicker, brighter cream and red lacquer, teal tiles, round lanterns everywhere, a blossom tree at the gate. Friendlier to the 9–16 audience at a glance, but further from the concept art and noisier behind the blade.

![[References/Smithy Redesign/proposal-station-kit.svg]]

Direction B, sketched with the same layout, sizes and kept parts so the two can be compared directly:

![[References/Smithy Redesign/proposal-direction-b.svg]]

A mix is also possible: A's materials and colours on the building, with B's chunkier proportions and extra lanterns.

## Stations (Direction A)

Sizes are in studs. A player is about 5.2 tall.

### Ore Roller → ore shrine

- **Silhouette:** a small timber frame with a tiled cap and a straw rope with paper tags across it. Inside: stone pedestals, one per **material stand**, each with a wooden offering tray and a chunky faceted ore lump on top. Beside them, **one tall wooden lever** (about 3 studs, rope-wrapped grip) that every stand shares. Stand 2 is left as an empty base so the first upgrade has a visible place to go.
- **Materials:** Slate or Basalt pedestals, Wood trays, a SmoothPlastic ore lump with the rolled material's colour (later its MaterialVariant), Fabric rope.
- **Scale:** about 7 × 5 × 3, so it's no longer the smallest thing in the room.
- **Kept:** `Machine` with `RollPrompt` (hold 1.5 s, "Roll ingot") becomes the lever post. Each stand gets a named `Stand1/Ore` part so the roulette reveal can animate it later. The reveal itself is ForgeService work and not part of this rebuild. The roller moves to x ≈ −15 to make room for the forge's bellows; nothing reads its position.

### Forge → plaster hearth

- **Silhouette** (follows `forge-v1`): a dark stone plinth, a pale plaster body in a timber frame with an iron lintel, and a **recessed glowing chamber** that the two iron trays slide into. A plaster hood tapers to a dark stone chimney with glowing vents, going up through the roof. A shimenawa rope with paper tags hangs over the mouth. A box bellows sits on the left side, with a charcoal crate.
- **Materials:** Plaster, Wood, Slate. Neon only deep inside the chamber, plus the existing PointLight made warmer and larger so the forge lights the room.
- **Scale:** about 4 wide, 7–8 to the chimney cap (19 through the roof once the workshop exists).
- **Kept:** `Base` keeps its exact size and CFrame, because ForgeService places `ForgeSlot1/2` from its bottom face and hangs the `ForgeTimers` billboard on it. It becomes an **invisible, colliding** box inside the new forge, with `HeatPrompt` on it. The trays are modelled where the slots already sit, at ±0.45, 1.12 up and 1.55 forward. If the trays should move, that's a one-line change to `SLOT_OFFSETS` in ForgeService, and I'd ask first.

### Anvil → kanatoko

- **Silhouette** (follows `anvil-v1`): a **hornless** rectangular iron block on a squat wooden block with an iron band and bolts, set on a few paving stones. A small tool box (punches, scale tray) on one side and a sledgehammer and water bucket on the other, all kept low.
- **Materials:** a matte dark Metal face with a thin lighter edge, so the hot blade is the brightest thing in the frame. Warm mid-brown Wood below. Nothing shiny or busy next to the blade.
- **Kept, unchanged:** `BladeMount` (−1.35, 3.20, −14), `Face` (position, 3.0 × 0.6 × 1.3, top at y 3.2, `ForgePrompt`, PrimaryPart) and `Clang`. Any widening of the block happens **below** y 3.15. `Horn` is removed and `Stump/Waist/Base` are reshaped. No script reads them (checked AnvilController, BladeProbe, HiltBenchController and the services), but the anvil-integration session has been asked to confirm in the shared notes before the anvil is touched. **The anvil gets rebuilt last.**

### Hilt Bench → fittings desk

- **Silhouette:** a drawer desk (*tansu*) on a tatami-edged platform. Behind it, a pegboard of colour-wrapped grips (indigo, vermilion, black, gold) and three tsuba, which gives the room its strongest colour accents and reads as "hilts" at a glance. A paper lamp (*andon*), a blade on the desk and silk cord spools.
- **Kept:** `Top` (with `HiltPrompt`) stays the desk top at its current height (2.85).

### Display Rack → sword pedestals

- **Silhouette:** one wooden pedestal per holder (about 1.6 × 1.6 × 1.6) with a black-lacquer cap and red trim, sword **upright, grip up**, exactly as the slots hold them now. A paper price tag hangs on the front. Empty holders show the green **+**. They stand on a low dark deck along the open front, about 5 studs apart, so each one reads as a separate thing to buy. More holders extend the deck sideways. This matches the pedestals in `game-feel-v1` and the earlier station kit.
- **Alternative:** a horizontal *katana-kake* (blade lying flat, edge up) is more traditional. It would mean re-aiming the `Slot` parts and checking `SwordRenderer` and the price-tag offset, so it's not the default.
- **Kept:** `Slots/Slot1..3` with `HolderPrompt` (spacing changes, orientation doesn't). The rack stays near x 13 so ShopService's hard-coded `INSPECT_POINT (13, 3, −6.5)` still sits in front of the holders and inside `REACH 15`.

## Workshop and plot

![[References/Smithy Redesign/proposal-workshop.svg]]

- **One open-front building** (GDD: grows as one workshop): about 41 × 17 studs, 7 bays, a stone plinth, charred-cedar posts, plaster back and side walls with a dark lower band, and a grey hip-and-gable tile roof (ClayRoofTiles) with eaves at 11, the ridge at about 17 and the forge chimney through it. The open side faces +Z, the path customers already walk from (13, 3, 30).
- **Zones:** an earth floor (Ground/Mud) on the hot-work side (ore shrine, forge, anvil), and a stone floor on the shop side (Hilt Bench, holders) at ground level, so customer NPCs don't sink into a raised floor.
- **Front dressing:** indigo noren over the shop bays with a white sword crest, red chōchin lanterns on the corner posts, and a signboard (刀鍛冶) on the eave.
- **Ground:** a plot pad with a packed-earth yard and a stone approach path, so the grey grid isn't visible from the play camera. The full six-plot village (`village-map-v1`) is a separate step.
- **Growth hooks:** extra bays and holders to the right, a second eave tier, a bigger sign. Built as separate named models so upgrades can switch them on later.
- **Lighting:** warmer late afternoon (ClockTime ≈ 16.5, warm OutdoorAmbient, light Atmosphere haze), with PointLights in the lanterns and hearth so the anvil isn't in roof shadow. Evening, like `game-feel-v1`, can be a later preset.
- **Old blocks:** move `store`, `creation area` and the two `Part` slabs to `ServerStorage.Archive` rather than deleting them.
- **`Models/` in the vault:** the medieval cabin (`SwordShop.bbmodel/.fbx`, `SwordShop-preview.jpg`) is already marked historical in the GDD. Proposal: move it to `Models/Archive/` and build the workshop from Studio parts (nothing is imported yet, and parts are easiest to iterate through the MCP). A Blockbench or Blender pass for the roof and ornaments can come later if parts look too blocky.

## Readability from the forging camera

![[References/Smithy Redesign/current-forging-camera.jpg]]

The forging camera sits about blade length × 1.1 above the strike point, tilted 20°. In the rebuild:

- Within about 2 studs of the face, nothing is taller than y ≈ 3.5. Roof beams over the anvil stay above y ≈ 12.
- Floor under the anvil: dark earth, not grid. Anvil face matte and dark. The hot blade and its sparks are the brightest, most saturated things in the frame.
- Forge and bench keep at least 6 studs from the anvil, as now, so they only frame the shot at the edges.

## Parts the code relies on (kept)

| Part | Kept exactly | Used by |
|---|---|---|
| `Smithy` folder and the five model names | names, PrimaryParts | every controller and service |
| `Forge.Base` + `HeatPrompt` | name, size, CFrame (hidden in the new forge) | ForgeService (slot visuals, timers billboard, reach), ForgeController, AnvilController |
| `Anvil.BladeMount` | CFrame | AnvilController, BladeProbe |
| `Anvil.Face` + `ForgePrompt` | name, CFrame, size | AnvilController (`STRIKE_X`, prompt) |
| `Anvil.Clang` | Sound under the Anvil model | AnvilController, HiltBenchController |
| `OreRoller.Machine` + `RollPrompt` | name, prompt settings (position may move) | ForgeService |
| `HiltBench.Top` + `HiltPrompt` | name, height | HiltBenchController |
| `DisplayRack.Slots.Slot1..3` + `HolderPrompt` | names, orientation, near x 13 | ShopService (sword placement, `Occupied`), ShopController |

Created at runtime and left alone: `ForgeSlot1/2`, `ForgeTimers`, `AnvilHammer`, the anvil `Blade`, `TakeBackPrompt`, displayed sword models, `Customers`.

## Build order once a direction is picked

1. Workshop shell, ground and lighting first (around the stations, which aren't touched).
2. Forge, Ore shrine, Hilt Bench, holders: one station at a time. Each gets a playtest of its own flow (roll, heat and take out, attach hilt, display and sell) with the console checked for errors.
3. The anvil last, after the integration session confirms the contract in the shared notes. Then a full loop playtest.
4. Code Map, Decisions Log and the session note updated. Allen saves the place.

Part budget: roughly 30–60 parts per station and under about 600 for the whole workshop. Stock materials only, no unions.

## Pick a direction

1. **Direction:** A · Working kajiba (recommended) or B · Festival smithy.
2. Defaults I'll use unless you say otherwise:
   - **Anvil:** hornless block. `Horn` removed; `Face` and `BladeMount` untouched.
   - **Holders:** upright-sword pedestals, about 5 studs apart (not horizontal katana-kake).
   - **Ore Roller:** "ore shrine" with stone stands and one big lever.
   - **Old prototype blocks:** move to `ServerStorage.Archive`. **Cabin files:** move to `Models/Archive/`.
   - **Lighting:** warm late afternoon.

Related: [[Japanese Village Concept Art]] · [[Player Plot Concept Art]] · [[Create Swords! GDD]] · [[Code Map]] · [[Home]]

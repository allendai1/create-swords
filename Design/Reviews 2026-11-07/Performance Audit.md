---
title: Performance Audit
type: review
updated: 2026-11-07
tags: [review, performance, create-swords]
---

# Performance Audit (2026-11-07)

Second pass after [[Design/Reviews 2026-10-31/Performance Review]] and its [[Design/Reviews 2026-10-31/Handoff — Performance fixes|handoff]]. Studio stayed in **Edit** the whole time (no Play, no viewport use). Everything below is one of: an instance count read off the Edit datamodel, an `os.clock` timing on Allen's PC (marked PC; a low-end phone runs Luau about 4–6× slower), a code path with `Script:line`, or a payload size from a fresh `SmithyCore` clone required in Edit. Anything per frame on a phone is an estimate and says so. Four decorative property passes were applied inside the fence (below); **no script was changed**.

## Summary

1. The place is lighter than on 10-31: Workspace 23,632 → **20,330** instances (the drafts are gone), `ServerStorage.Legacy` 73,536 → **32,881**, and the prop etches, hotbar viewports, holder markers, furnace glow and ore shows are fixed as the handoff says.
2. **Biggest phone risk: the whole `SmithState` on every push.** Measured: a late-game state (30 carried swords, 40 ingots, 30 letters) encodes to **67.9 KB JSON**, of which **69% is the `refinement` arrays** (64–192 numbers per sword); 60 swords is 122 KB. 56 server call sites push it, 14 client scripts handle every push (`SmithyCore.publicState` 229–264).
3. **Second: the shop shine.** Every displayed sword within 35 studs gets **64 Beams + 65 Attachments** and up to 192 property writes a frame while you move (`SwordRenderer` 96, 121–145, 229–239). A full shop (39 display slots) is ~2,500 Beams in view, 18× the vault's 140-beam VFX budget.
4. **Third: the crowd.** A full late server runs ~**140 R15 Humanoids** (per plot: 8 customers, up to 3 pullers, 7 crew, courier, lever hand; plus 20 villagers); ~128 of them keep physics and the state machine running while standing. Only the courier and seated rickshaw riders are held cheaply.
5. **Fourth: always-on rendering.** The forest's **812 trees / 5,079 MeshParts / 3,938 SurfaceAppearances** sit inside the village (x 354–977) so they never stream out; each plot carries **1,280 shadow casters** (622 under 1.5 studs) and 23 lights; Bloom, SunRays and two colour grades are on; `MenuBlur` runs at 14 behind every menu; the only performance setting is Busy street.
6. **Fifth: the join.** Six full Workspace scans of 10–17 ms each (PC) ≈ 0.3–0.5 s of script time on a phone, 3,993 StarterGui instances copied per spawn (and per Dev reset), and in a full server 6 × 3,599 plot instances (75% of each plot's parts are unbought upgrades) all land on every phone.
7. Verified claims: the forest has **0** CastShadow / CanQuery / CanCollide / CanTouch on all 5,079 parts; the Backdrop mountains likewise (134 parts). Those were already clean.
8. Applied today (property-only, fence): Street CastShadow off on 672 tiny parts and CanTouch off on 1,024; Dressing CanQuery off on 132 non-colliding lantern/leaf parts and CanTouch off on 20; 11 SurfaceGuis given a MaxDistance (were 0). Exact numbers and the reversal record below.
9. Not applied, proposed with diffs: slimmer `SmithState`, fewer shine beams, holding standing NPCs, the plot template's shadows and fidelity, prompt templates set to Custom, a MenuBlur cap, Legacy export.
10. Leftovers for Allen: a stray `Workspace.Smithy` station copy (1,134 instances, 2 shadow-casting lights), `Weapon Rack`, `AuxScene` (5 unanchored parts that fall in Play), `ZanbatoPreview`, `Courtyard`, `Bamboo9`, `MaterialDemo`, `Workspace.Lighting`, and two Studio-only server Scripts (`CompareTry_1107`, `OreRollerStyleTest`) still Enabled.

## Findings

| # | Finding | Evidence | Phone impact | Fix | Status |
|---|---|---|---|---|---|
| 1 | Whole SmithState per push, dominated by refinement arrays | `SmithyCore.publicState` 229–264 sends every carried sword with `refinement` (64 numbers; flamberge/moonbite/seraph/serpent/shardblade 128, thornspire 192) and `shape`; `push` 284–289; **56** call sites (ShopService 19, EmployeeService 14, ForgeService 5, DeliveryService 4, DevTools 4, Smith/Rack/Tycoon 2, Etch/Inventory/Polish/Store 1); **14** `SmithState.OnClientEvent` listeners and 14 `GetSmithState` fetchers at join. Measured JSON: fresh 317 B; Allen's Studio save (2 swords) 2,624 B; 10 swords 21,080 B (swords 13,874); 30 swords 67,917 B (swords 52,033, refinement 46,547 = 69%; without refinement the swords would be 5,033 B); 60 swords 121,894 B. One sword entry ≈ 1,380 B. | est. 30–120 KB received and decoded on every crew action late in the game (several a minute), then 14 handlers walk it; the client's receive budget is tens of KB/s | Send a polish number, not the array (P1) | Proposed |
| 2 | Shop shine: 64 Beams per display sword in view | `SwordRenderer` 96 `SHINE_PIECES = 64`; `buildShine` 121–145 makes 65 Attachments + 64 Beams per sword within `SHINE_NEAR` 35 studs; 229–239 writes Width0/Width1/Brightness on all 64 whenever `u` moves (camera moved > 0.4 studs, eased over frames) or a polished sword pulses (every 2.5–4.5 s, 0.6 s). Plot template: **39** DisplaySlots. | est. 1,000–2,500 Beams and 3,000–7,500 property writes a frame while walking in a full shop; Beams are CPU-updated every frame | `SHINE_PIECES` 64 → 16 (P2); only ~9 of 64 pieces are ever lit (`SHINE_HALF` 0.14) | Proposed |
| 3 | ~140 server-driven R15 Humanoids, standing ones at full cost | Per plot: `WALK_INS` 2 + `Employees.promoterCrowd` ≤ 3 + `Rickshaws.count` ≤ 3 = 8 customers (`ShopService` 1533, 1655); ≤ 3 pullers; crew 3 crafters (Upgrades `Crafters` 288) + 4 staff (Employees 126–135); courier (`DeliveryService` 261–263: `EvaluateStateMachine = false`, anchored); LeverHand rig (`Plot.WorldStore.AutoRoller.Owned.LeverHand`: 236 instances, root anchored, **EvaluateStateMachine true**). `StreetLife` 24: **20** villagers (10 Extra are hidden client-side only). Only `Rickshaws` 134/216–217 holds a rig cheaply. `ShopService.makeNpc` 632–677, `EmployeeService.makeWorker` ~320–345, `StreetLife.make` 133–181 set only DisplayDistanceType, WalkSpeed, `NpcWalk.steady`, `SetNetworkOwner(nil)`. | est. 3–10 ms of a 16 ms server frame at ~128 live state machines (prior review's figure, unmeasured); every phone draws and holds ~140 rigs (friends' avatars with their own textures) because the village fits in the 1,024-stud radius | `NpcWalk.hold` at every wait (P3), villagers held while paused (P4), `EvaluateStateMachine = false` on the template's LeverHand (P5) | Proposed |
| 4 | The forest never streams out | `Village.Atmosphere.Forest`: 812 `AnimeTree` models, 11,387 instances, 5,079 parts (4,717 MeshParts, 9 unique meshes, 4 textures; 3,938 SurfaceAppearances, 3,812 of them AlphaMode Transparency and DoubleSided; 1,196 trunk Textures). Extent x 354–977, z −454–56: inside the village. RenderFidelity Automatic on all. CastShadow/CanQuery/CanCollide/CanTouch 0/0/0/0 (verified). | the largest static draw and texture load on every phone at all times; double-sided alpha-tested leaves are the costliest kind of mesh on mobile | A client-side tree cull by quality (hide every other tree beyond ~200 studs when `SavedQualityLevel` ≤ 3) or fewer leaf parts per tree (104 trees have 10 parts) | Open (Allen's call: nature comes from the Toolbox) |
| 5 | Plot template shadows and collision fidelity | 1,280 of 2,308 parts cast shadows, **622** under 1.5 studs; `Smithy` folder alone 570 casters; 1,118 MeshParts (fidelity not re-measured; 10-31: all Default). ×6 plots = 7,680 casters in a full server. | mid-range phones (graphics level ≥ 4) draw them in the shadow pass | the same pass as today's Street one, on `Workspace.Plot` (P5) | Proposed (outside the fence) |
| 6 | Join-time scans | `PromptFilter` 52 (+86 when `Plot` arrives), `PromptStyle` 38, `OreBoxAnimator` 127, `NewOreFx` 66, `WorldStoreController` 196, `TextLayers` 84 (Workspace) + 83 (PlayerGui), `HudFocus` 220, `UiSounds` 38 (PlayerGui). `ActionButton` 33 is dead code while `ActionGui.Enabled` is false (returns at 26). Measured (PC, 20,330 instances, 5 runs): `GetDescendants` 5.0–7.7 ms, IsA pass 3.5–5.6 ms, Name-compare pass (OreBoxAnimator's `watch` tests `Name` first) 8–11 ms, IsA+GetAttribute 4.5–6.7 ms → 10–17 ms per scan, ~70–90 ms for the six. Six `workspace.DescendantAdded` handlers after (PromptFilter 55, PromptStyle 41, OreBoxAnimator 126, NewOreFx 69, WorldStoreController 199, TextLayers 81). | est. 0.3–0.5 s of script time in 50–100 ms unyielding blocks during the first seconds; 6 Lua calls per streamed-in instance (~17.6k plot instances in a full server) | Template prompts `Style = Custom` in Studio so PromptStyle's scan does nothing (P6); a shared scan is **not** clean (see Applied today) | Proposed |
| 7 | Six plots on every phone | Plot template 3,599 instances / 2,308 parts; **67** TycoonItems with `Upgrade` hold 2,317 instances / **1,742 parts (75%)**; ModelStreamingMode: Default 425, **Persistent 12** (EtchingTable 170, EtchingTable2 164, Forge 182, PolishStation 110 ×2, Anvil 47, SwordRack 24, SwordRack2 11, IngotRack 31, IngotRack2–4 6 each = 867 descendants per plot that never stream out), Atomic 23 (21 prop swords, TrainingDummy, LeverHand). Streaming radius/mode: `StreamingTargetRadius`, `StreamingMinRadius`, `StreamingIntegrityMode`, `ModelStreamingBehavior`, `StreamOutBehavior` and `Lighting.Technology` are not readable from a script ("not a valid member" / lacking RobloxScript capability): read them off the Properties panel. | 21.6k plot instances in a full server, 5.2k of them persistent, on every phone | `PersistentPerPlayer` + `AddPersistentPlayer(owner)` for the 12 station models (10-31 #4, still open); keep unbought upgrades out of Workspace (large) | Open |
| 8 | Always-on post effects and the menu blur | Lighting: GlobalShadows on (softness 0.6), SunRays on, Bloom on, Atmosphere 0.32, `ColorCorrection` + `NightGrade` on (the other four grades are off now: 10-31 #13 fixed), DepthOfField off. `MenuBlur` Size 0 / disabled at rest, attribute Strength **14**; `HudFocus` 57–72 tweens it to 14 whenever a menu is open. 8 always-on cherry-blossom emitters at Rate 6 (trivial). | a full-screen blur pass for as long as any window is open, on top of Bloom and SunRays; no low-graphics path | Cap the blur at 8 and skip it at quality ≤ 3 (P7); a Low graphics switch next to Busy street | Proposed |
| 9 | Per-frame idle work on the client | `PolishController` 142 Heartbeat writes `scrape.Volume` every frame with no station open and 1049 RenderStepped calls `UiFx.onGamepad()`, `flushGrime()`, `showRing()` (a `ring.Visible = false` write) every frame; `TycoonController` 591 Heartbeat: `padUnderfoot` over 89 markers (measured 0.008 ms PC), then `press`, billboard writes, `bindPad`, `UiFx.onGamepad()` and a `button.Text` write every frame; `RoofHider` 66: `GetTagged` + 3 `FindFirstChild` per HidesRoof building (0.004 ms PC for 6); `Guide` 359 two writes a frame idle; `FreeMouse` 15 two `IsKeyDown` a frame. The rest early-return idle (`SwordRenderer` 181, `OreBoxAnimator` 131, `SwordSlash` 161, `AnvilController` 1108, `WeatherController` 230) or are scoped (HiltSeat 296, EtchingTableController 268, SecretUnlock 95, CoinFly 47). | est. 0.1–0.3 ms a frame on a phone; the two PolishController loops and TycoonController's are the ones worth gating | Connect PolishController's two loops while `active`; TycoonController's pad check at 10 Hz (P8) | Proposed (outside the fence) |
| 10 | NpcWalk route cost | `route` 153–178: one `ComputeAsync` per walk (two when stuck), then `clear`/`leg`/`smooth` run `GetPartBoundsInBox` per 0.5 stud of every leg. Measured in Edit on the template plot (a probe clone with the calls counted; the Npcs collision group isn't registered in Edit so slightly more parts count): anvil→forge 27 studs **471** overlap queries + 41 raycasts, forge→polish 69 studs **630** + 26, shop entry→slot 162 + 7; the geometry part costs **0.2–3.3 ms** per route (PC). `ComputeAsync` measured 95–117 ms wall each, which is Edit's scheduler latency on a yielding call, not CPU. `follow` 239 polls at 20 Hz per walking NPC. No route cache. | server: a 1–3 ms hitch per crew/customer walk, several a second in a full server | cache crew routes per plot and station pair, cleared on a buy | Open |
| 11 | StreetLife | 247–309: one loop at 0.5 s for 20 villagers (`shopsNear` walks `workspace:GetChildren()`, `clear` tests ~20 obstacles): cheap. Cost is the 20 Humanoids, not the loop. Villagers stand ~36% of the time (the 11-07 note: 64% moving) with physics and state machine running. | see #3 | P4 | Proposed |
| 12 | Delivery carts per frame | `DeliveryService` 650–661 Heartbeat: per bought cart `ownerOf`, `bought`, `getData`, `move` → `phase`; at home only `rig`/`set` on a state change; out, `set` pivots the welded Bed (10-31 #6 done: 1 CFrame + wheel `C0`s) and `paint` writes only changed transparencies. | fine | — | Done (10-31 #6) |
| 13 | ReplicatedStorage | 846 instances: SwordMeshes 234 MeshParts (CollisionFidelity Default on all 234; CanCollide/CanQuery/CanTouch off), SwordParts 93 (Default), DecorModels 85 parts (all collide/query/touch on), WorldText 231, TopbarPlus 22 scripts (Icon 40.9k chars), Shared 30 modules (BladeData 97k chars). Dev-only but replicated to every client: `Prototypes.ShapingPrototype` (44.2k chars) and `Shared.BladeProbe` (19.6k, gated by a workspace attribute via `BladeProbeLoader`). | ~65 KB of prototype source in every join; convex hulls for 327 sword meshes that never collide | Move the two prototypes to ServerStorage; `CollisionFidelity = Box` on SwordMeshes/SwordParts (P10) | Proposed |
| 14 | StarterGui | 3,993 descendants in 30 LayerCollectors (MenuGui 1,440, CrewGui 592 with 10 viewports, GemGui 437, DeliveryGui 393, MailGui 203, PickerGui 152…), copied into PlayerGui per spawn and per Dev reset. `ShowDevelopmentGui` is on (Studio view only; another session is capturing UI). | est. 50–150 ms of instance creation per spawn on a phone | no change; keep windows out of StarterGui that could be cloned on first open (MenuGui) | Open |
| 15 | ServerStorage.Legacy | 32,881 descendants in 363 children, **217 script backups**; top: Village_beforeWideGaps_1107 6,265, Forest_beforeAnime_1107 4,070, Village_beforeNarrowStreet_1107 4,016, Plot_beforeShopLeft_1107 3,969, Forest_beforeRealistic_1107 2,283. Also DecorCandidates 984, Cast 889, Buildings3D 734, Nature 542, UIPackCopies 417. Edit `Stats.InstanceCount` 78,360, Studio 3.2 GB. | none on players; place size, save/publish time, every server's memory | export the five big folders to .rbxm (Archive/Studio Backups) and keep only current `_before` copies (P9) | Proposed |
| 16 | Lights, Highlights, sounds | Workspace 49 lights: Plot 23 PointLights (no shadows), Village 21 (17 street lamps off by day, 4 chochin on), Courtyard 1, **Workspace.Smithy leftover 4, two with `Shadows = true`** (the only shadow lights in the place). Highlights at runtime: Guide glow 1, AnvilController BladeOutline 1, one `VIPHighlight` per VIP customer (server-side): far under 31. Sounds: 3 in Workspace, 19 in SoundService. | fine | delete the leftover | Report only |
| 17 | SurfaceGuis never culled | Before: every world SurfaceGui had MaxDistance 0 (4 station signs at 800×600 / 100 px per stud, 2 Kanban, Leaderboard Face 164 descendants, 4 GateSign, 4 in the Smithy leftover); OddsGui already 60. | small, free | set today (Applied) | Applied |
| 18 | Street and Dressing decor flags | Before: Street 1,024 of 1,042 parts CanTouch on, 672 tiny lantern parts (0.51-stud cubes) casting shadows; Dressing 132 non-colliding lantern/leaf parts CanQuery on (they also made `WeatherController` 249's roof raycast count a lantern string as a roof), 20 CanTouch on. No `.Touched` in any live script; no Seats, SpawnLocations or TouchTransmitters under either folder. | small, free | set today (Applied) | Applied |
| 19 | Leftover test objects | `Workspace.Smithy` (Folder: 16 station models, 1,134 instances, 757 parts, 570 shadow casters, 4 lights (2 with shadows), 4 SurfaceGuis) at (2020, 1, −264), 1,266 studs from the nearest lot (server memory only at the default radius); `Weapon Rack` 104 instances / 12 parts (4 unions) / 72 Decals at (−49, 3, −687), 700 studs from a lot; `AuxScene` 10 / **5 unanchored MeshParts at y 57** (they fall in Play), 451 studs; `ZanbatoPreview` 9 parts at y 302, 620 studs; `Courtyard` 6 / 3 parts + 1 light, 581 studs; `Bamboo9` 5, 651 studs; `MaterialDemo` empty; `Workspace.Lighting` 4 post effects (inert there). `ServerScriptService.CompareTry_1107` (Script, Enabled; returns at once since `Workspace.Compare_1107` is gone) and `OreRollerStyleTest` (Script, Enabled, Style "Now": requires PlotService and hooks `onPrepare` every Play). `Workspace.Compare_1107` is already gone. | the four within 1,024 studs replicate to phones; AuxScene's parts simulate | Allen decides; nothing deleted | Open |

## Applied today

Property-only changes inside the fence, run from `execute_luau` in Edit. Counted before and after in the same run; no part moved or resized; no script edited, so no script backup was needed. The exact exception lists (for an exact reversal) are stored in **`ServerStorage.Legacy.PerfAudit_1107_propertyPass`** (a StringValue, 3,219 chars, does not replicate).

| Change | Before → after | Check |
|---|---|---|
| `Village.Street`: `CastShadow = false` on every part with max dimension < 1.5 studs (the lantern brackets: `StreetLights.StreetLight` 0.51-stud WoodPlanks cubes; 672 of them) | casters 1,024 → **352** (small casters 672 → 0) | recount after the pass |
| `Village.Street`: `CanTouch = false` on all parts | 1,024 → **0** (18 were already off: Road, 2 Curb, 4 Paving, 10 Walkway, StreetFill) | recount; grep: no `.Touched` in 137 live scripts; 0 Seats/SpawnLocations/TouchTransmitters under Street |
| `Village.Dressing`: `CanQuery = false` on parts with `CanCollide = false` (LanternString `Lantern/Dark` ×64, `Lantern/Paper` ×64, CherryBlossom `pink tree/Leaf` ×4) | CanQuery 172 → **40**; non-colliding-with-query 132 → 0 | recount; the 40 left are the colliding trunks/stones NpcWalk's `room()` and StreetLife's obstacle list need |
| `Village.Dressing`: `CanTouch = false` on all parts | 20 → **0** (StoneLantern ×12 parts, CherryBlossom leaves ×4 and trunks ×4) | recount |
| `SurfaceGui.MaxDistance` where it was 0: Plot station signs ×4 → 80; `Shop.Starter/Upgraded.Shell.Roof.Kanban` → 250; `Plot.Leaderboard.Board.Face` → 200; `Village.Landmarks.GateSign` ×4 → 350 | 11 set; SurfaceGuis at 0 outside the `Workspace.Smithy` leftover: 11 → **0** (the leftover's 4 left alone) | recount; MaxDistance is measured from the camera (ui gotchas), so the values carry 2–3× the use distance |

Workspace totals after: CastShadow 3,211 → 2,539; CanQuery 2,380 → 2,248; CanTouch 1,709 → 665.

The Luau that ran (abridged to the filters; the full output is in the StringValue):

```lua
for _, d in street:GetDescendants() do
	if d:IsA("BasePart") then
		if d.CastShadow and math.max(d.Size.X, d.Size.Y, d.Size.Z) < 1.5 then d.CastShadow = false end
		if d.CanTouch then d.CanTouch = false end
	end
end
for _, d in dressing:GetDescendants() do
	if d:IsA("BasePart") then
		if not d.CanCollide and d.CanQuery then d.CanQuery = false end
		if d.CanTouch then d.CanTouch = false end
	end
end
-- SurfaceGuis: Sign -> 80, Kanban -> 250, Leaderboard Face -> 200, GateSign -> 350, only where MaxDistance == 0
```

**Why the fenced scripts were left alone.** `PromptFilter`, `PromptStyle`, `NewOreFx`, `OreBoxAnimator` and `WorldStoreController` already test `IsA` first, guard re-adds with weak tables and do nothing per frame when idle (`OreBoxAnimator` 131 loops two empty tables; `WorldStoreController` 411 loops ≤ 36 spots). A shared scan would save one `GetDescendants` per script (5–7 ms PC, ~25–35 ms on a phone each) but is not clean: the scripts start on different frames (each waits on its own `WaitForChild`s), so a snapshot taken once has a gap before each late registrant's `DescendantAdded`, and closing it means buffering every added instance until the last script registers. Not worth a streamed-in prompt going unstyled. `ActionButton` does not scan at all while `ActionGui` is off. `StreetLife`'s loop is already gated (0.5 s, no per-frame work); holding its villagers changes NPC behaviour Allen can't see verified in Edit, so it is a proposal (P4) with its test. `NpcWalk`'s cost per route is 0.2–3.3 ms of geometry plus one `ComputeAsync`; the fix that matters (a route cache) is not a one-liner.

## Proposed, not applied

**P1. Send a polish level, not the refinement array** (`SmithyCore`, `SwordMeshCache`, `PolishController`, `PolishService`). Every client reader passes `sword.refinement` into `SwordMeshCache.blade/etch/plain/shine/overlay`, which `quantize` (84–91) rounds to 0 / 0.5 / 1 anyway; only `PolishController` (181, 261, 384) needs the real array, and only while polishing.

```lua
-- SmithyCore.publicState, line 250: in the swords entry replace
	refinement = sword.blade.refinement, shape = sword.blade.shape,
-- with
	refinement = SmithyCore.polishLevel(sword.blade), shape = sword.blade.shape,
-- and add above publicState:
function SmithyCore.polishLevel(blade: Blade): number -- average refinement 0..1 (the client rounds it to thirds)
	local sum = 0
	for _, r in blade.refinement do
		sum += r
	end
	return if #blade.refinement > 0 then sum / #blade.refinement else 0
end

-- SwordMeshCache.quantize (84): accept the number
local function quantize(blade: any, refinement: ({ number } | number)?): ({ number }, string)
	local avg = 0
	if typeof(refinement) == "number" then
		avg = refinement
	elseif refinement then
		local sum = 0
		for i = 1, blade.stations do
			sum += refinement[i] or 0
		end
		avg = sum / blade.stations
	end
	local level = math.clamp(math.floor(avg * LEVELS + 0.5), 0, LEVELS)
	return table.create(blade.stations, level / LEVELS), tostring(level)
end

-- PolishService: a RemoteFunction `GetRefinement(swordId) -> { number }` that returns the owner's sword's
-- blade.refinement (rate-limited by SmithyCore.allowCall); PolishController fetches it where it reads
-- `s.refinement` at 384 and uses the number from SmithState only for art until it arrives.
```
Expected: late game 67.9 KB → ~21 KB per push (swords 52 KB → ~5.5 KB). `EtchingTableController` 331/342 and `EtchPlayback` 88 already type-check `typeof(sword.refinement) == "table"` and fall back to nil; check they still draw the right polish level (they pass the value to SwordMeshCache, which now takes the number). Risk: medium (one remote, four scripts). Test: polish a sword, re-etch it, open every picker; `DataReceiveKbps` during a crew sale.

**P2. Shop shine with fewer beams** (`SwordRenderer` 96). `local SHINE_PIECES = 64` → `local SHINE_PIECES = 16`. Only pieces within `SHINE_HALF` 0.14 of `u` have any width, so 16 pieces keep ~4 lit pieces instead of ~9; the line gets slightly coarser on a flamberge. Beams in a full shop ~2,500 → ~620; per-frame writes ÷4. Test: stand in the Upgraded shop with the racks full, MicroProfiler before/after.

**P3. Hold standing NPCs** (`NpcWalk` + callers in `EmployeeService`, `ShopService`). Add to `NpcWalk`:
```lua
-- Standing still for a while (work, a browse, the queue): no physics or state machine; `hold(npc, false)` before the next walk.
function NpcWalk.hold(npc: Model, on: boolean)
	local hum = npc:FindFirstChildOfClass("Humanoid")
	local root = npc:FindFirstChild("HumanoidRootPart") :: BasePart?
	if not hum or not root then
		return
	end
	if on then
		hum:MoveTo(root.Position) -- clear the move goal so it doesn't resume into furniture
	end
	hum.EvaluateStateMachine = not on
	root.Anchored = on
end
```
Call `NpcWalk.hold(npc, true)` after each arrival that waits (crew `work`/`scrub` and station waits, customers' `BROWSE_WAIT`/offer wait) and `NpcWalk.hold(npc, false)` before every `NpcWalk.to`. `Rickshaws.seat` 216–217 already does exactly this for riders. Risk: a hold left on makes an NPC stand forever; put the `hold(false)` at the top of `NpcWalk.to` itself so no caller can forget it. Test: crew cycle, a customer's browse and leave, a villager's shop visit.

**P4. Villagers held while paused** (`StreetLife`). With P3's `hold`: in the main loop, where a stroll ends (`v.target, v.lastAt = nil, nil` at 275 and 236) add `NpcWalk.hold(v.npc, true)`; before `v.hum:MoveTo(pick)` at 302 and before `visit(...)` at 283 add `NpcWalk.hold(v.npc, false)`; also store `walk` from `make` on the Villager and `walk:Stop(0.2)` in the hold branch, because with the state machine off `Running` no longer fires and the walk track would keep playing in place. Saves est. 7 live state machines of 20 at any moment. Test: watch five villagers for two minutes: no one freezes mid-step or slides.

**P5. Plot template pass** (`Workspace.Plot`, outside the fence). The same Luau as today's Street pass on the template: `CastShadow = false` on the 622 parts under 1.5 studs; `CollisionFidelity = Box` on MeshParts with `CanCollide` and `CanQuery` both false (count them first; 10-31 measured 661); `CanTouch = false` on the 402 parts that have it (none has a Touched listener; the pads are read by position, `TycoonController` 475–496). Leave `CanCollide`/`CanQuery` alone (PromptFilter's wall check and the pad labels raycast against them). Plus `Plot.WorldStore.AutoRoller.Owned.LeverHand.Humanoid.EvaluateStateMachine = false` (`Shared.LeverHand` poses by CFrame; its only Humanoid reference is `HumanoidRootPart` at line 34). ×6 plots: 3,732 fewer shadow casters and 6 fewer state machines.

**P6. Prompts styled in Studio** (Plot template + ForgeService/ShopService). The 21 template prompts still `Style = Default` get `Style = Custom` and the `Styled` attribute in Studio; the server-made ones (ForgeService's ore prompts, the till's Collect) are created Custom with `Styled = true`. Then `PromptStyle.adopt` becomes a no-op guard and its scan at 38 can go (`PromptFilter`'s stays: it needs every prompt). Also `OreBoxAnimator.watch` 111: test `roller:IsA("Model")` before `roller.Name == "OreRoller"` (the Name-first pass measured 8–11 ms against 3.5–5.6 ms for IsA-first).

**P7. Menu blur cap** (`HudFocus` 39, 57–72). `local BLUR = menuBlur:GetAttribute("Strength") or 14` → read the quality: `local quality = UserSettings():GetService("UserGameSettings").SavedQualityLevel.Value`, and in `setBlur` skip the effect when `quality > 0 and quality <= 3` (phones on Low); set the attribute Strength to 8. Test: open the Shop on the phone preset with quality 3 and 10.

**P8. Gate the idle loops** (`PolishController` 142, 1049; `TycoonController` 591). Connect PolishController's Heartbeat and RenderStepped when a visit starts and disconnect at leave (the two handlers already branch on `active`); run `padUnderfoot` every 0.1 s instead of every frame (the pad press has a 0.1 s tween anyway).

**P9. Legacy export.** `SerializationService` export of the five Village/Forest/Plot `_before` folders (20.6k instances) to `Archive/Studio Backups` and delete; prune the 217 script backups to the newest per script. `Stats.InstanceCount` 78k → ~55k in Edit.

**P10. ReplicatedStorage.** Move `Prototypes.ShapingPrototype` and `Shared.BladeProbe` (+ `StarterPlayerScripts.BladeProbeLoader`) to `ServerStorage.Builders`; `CollisionFidelity = Box` on `SwordMeshes` (234) and `SwordParts` (93): none collides or is queried.

**P11. Streaming (read, then decide).** Read `StreamingTargetRadius`, `StreamingIntegrityMode`, `ModelStreamingBehavior`, `StreamOutBehavior` and `Lighting.Technology` in the Properties panel and write them in the Code Map. If the target is the default 1,024, every lot streams every other lot; `PersistentPerPlayer` on the 12 station models (10-31 #4) is still the smallest win.

## Applied after the report (main session)

P5's property part and P10's fidelity part, run from `execute_luau` in Edit with the same undo convention (an attribute on every changed instance): `Workspace.Plot` CastShadow off on the 622 parts under 1.5 studs (casters 1,280 → 658), CanTouch off on 401 (the SpawnLocation kept), `CollisionFidelity = Box` on 642 non-colliding non-query MeshParts; `LeverHand.Humanoid.EvaluateStateMachine = false`; Box fidelity on the 326 MeshParts in `ReplicatedStorage.SwordMeshes` and `SwordParts`. Summary in `ServerStorage.Legacy.PerfAudit_1107_plotPass`. Not played: the look of the workshop without the small parts' shadows. Later the same afternoon **P8 and P7 went in too**: PolishController's two idle loops return early (143, 1054), TycoonController's pad check runs at 10 Hz (591), and `HudFocus.setBlur` skips the blur at `SavedQualityLevel` 1–3 (backups `*_beforeIdleGate_1107`, `HudFocus_beforeBlurCap_1107`; all compile). P1–P4, P6, P9 and P11 stay proposed.

## What to measure in Allen's next Play

Run this in the command bar with the **Client** datamodel selected (read-only; prints once after 10 s). Run it three times: standing in your empty workshop, inside the Upgraded shop with the racks full, and on the street among the villagers.

```lua
local Stats, RunService, Players = game:GetService("Stats"), game:GetService("RunService"), game:GetService("Players")
local frames, worst = {}, 0
local conn = RunService.RenderStepped:Connect(function(dt) table.insert(frames, dt) if dt > worst then worst = dt end end)
task.wait(10)
conn:Disconnect()
table.sort(frames)
local sum = 0
for _, d in frames do sum += d end
local p99 = frames[math.max(1, math.floor(#frames * 0.99))]
local function get(name) local ok, v = pcall(function() return (Stats :: any)[name] end) return if ok then v else "n/a" end
local function tag(t) local ok, v = pcall(function() return Stats:GetMemoryUsageMbForTag((Enum.DeveloperMemoryTag :: any)[t]) end) return if ok then math.floor(v) else "n/a" end
local hums, beams, parts = 0, 0, 0
for _, d in workspace:GetDescendants() do
	if d:IsA("Humanoid") then hums += 1 elseif d:IsA("Beam") then beams += 1 elseif d:IsA("BasePart") then parts += 1 end
end
print(("frame avg %.1f ms, 99th %.1f ms, worst %.1f ms (%d frames)"):format(sum / #frames * 1000, p99 * 1000, worst * 1000, #frames))
print("HeartbeatTimeMs", get("HeartbeatTimeMs"), "PhysicsStepTimeMs", get("PhysicsStepTimeMs"), "DataReceiveKbps", get("DataReceiveKbps"), "DataSendKbps", get("DataSendKbps"))
print("Drawcalls", get("SceneDrawcallCount"), "Triangles", get("SceneTriangleCount"), "Instances", get("InstanceCount"), "Primitives", get("PrimitivesCount"), "Moving", get("MovingPrimitivesCount"))
print(("memory %d MB: Gui %s, GraphicsTexture %s, GraphicsMeshParts %s, GraphicsParts %s, Script %s, Instances %s, PhysicsParts %s, Animation %s"):format(math.floor(Stats:GetTotalMemoryUsageMb()), tag("Gui"), tag("GraphicsTexture"), tag("GraphicsMeshParts"), tag("GraphicsParts"), tag("Script"), tag("Instances"), tag("PhysicsParts"), tag("Animation")))
print(("workspace: %d humanoids, %d beams, %d parts; PlayerGui %d descendants"):format(hums, beams, parts, #Players.LocalPlayer.PlayerGui:GetDescendants()))
```

What to look for:
- **DataReceiveKbps** while the crew works late in a save with 20+ carried swords: spikes per push are finding #1 (expect tens of KB per action before P1).
- **Beams** and frame ms inside the full shop against the empty workshop: finding #2.
- **Humanoids** on a server with friends joined, and the server MicroProfiler (F9 → Server → MicroProfiler): the Humanoid/physics step at 100+ rigs is finding #3.
- On a phone: Settings → Micro Profiler on, walk the street and the shop; read the **Render** (Prepare/Perform), **Physics** and **Lua** bars, and `GraphicsTexture` / `GraphicsMeshParts` memory with the forest in view (finding #4). Also note the quality level the phone picked (Settings → Graphics Mode).
- `PlayerGui` descendants after a Dev reset against a fresh join (finding #14).

## Checked (run today, Edit)

- Workspace census: 20,330 instances, 9,920 parts (6,600 MeshParts, 4 unions), 2,191 models, 55 attachments, 2,238 joints, 1 Humanoid, 49 lights (2 shadows), 0 Beams, 8 ParticleEmitters, 1,269 Decal-class (1,196 Textures), 16 SurfaceGuis, 5 BillboardGuis, 3 Sounds; `GetDescendants` 3.2–7.7 ms.
- Forest 812 trees: parts by tree 2 ×126, 5 ×130, 6 ×120, 7 ×239, 8 ×93, 10 ×104; 0/0/0/0 flags on 5,079 parts; Backdrop 134 parts 0/0/0/0.
- Plot: 69 TycoonItems (67 Upgrade, 1,742 parts = 75%), 89 pad markers, 39 DisplaySlots, 21 ForgedSword props (8 Shimmer), ModelStreamingMode 425/12/23, 8 SurfaceGuis, 5 BillboardGuis (MaxDistance 32/96/160), 23 lights, 1 Sound.
- ReplicatedStorage 846; StarterGui 3,993; StarterPlayerScripts 53 (DecorateController off); ServerScriptService 30; ServerStorage 37,290 (Legacy 32,881 / 363 / 217 script backups); `Stats.InstanceCount` 78,360; Studio 3,186 MB.
- Scan timings (5 runs) and the per-frame / loop inventory over 137 live scripts (1,920,937 source chars; > 60k: BladeData 97,326, ShopService 75,680, EmployeeService 67,564, EmployeeController 62,998).
- NpcWalk probe (clone in ServerStorage, destroyed after): 6 routes × 3 runs, query counts and ms as in #10.
- SmithState probe (clone in ServerStorage, `Profiles` path redirected, destroyed after): fresh 317 B; Allen's Studio save read-only from `Profiles_Studio_v1` (3,420 B saved; publicState 2,624 B); synthetic 10/30/60-sword states 21,080 / 67,917 / 121,894 B JSON (42 metals, 25 blueprints, 6 hilts, 7 etches from Shared).
- Property pass before/after counts as in Applied today; `ServerStorage.Legacy.PerfAudit_1107_propertyPass` written; no probe instances left (`__NpcWalkProbe`, `__SmithyCoreProbe`, `__SmithyCoreProbe2` absent).
- Not run (Edit can't): SceneAnalysisService (needs Play), MicroProfiler, any frame or network measurement on a device.

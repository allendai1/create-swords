---
title: Performance Review
type: review
updated: 2026-10-31
tags: [review, performance, mobile, streaming, network, memory, npc, create-swords]
---

# Performance Review (2026-10-31)

A read-only audit of what costs frame time, memory, network and server time in the Studio place, ranked for a low-end phone first, then for a full six-player server. Nothing in the place was changed.

**How it was measured.** Studio stayed in Edit the whole time (it was never in Play), so:
- **Measured:** instance, part, light, tag and connection-site counts on the Edit datamodel; code paths with line numbers (sources as of this afternoon); a few timings with `os.clock` on Allen's PC, marked "PC".
- **Estimated:** anything per frame on a phone, network rates and server milliseconds, marked "est.". Rule of thumb: Luau on a low-end phone runs about 4–6× slower than this PC.
- **Not readable by a script:** `Workspace.StreamingTargetRadius`, `StreamingMinRadius`, `StreamOutBehavior` ("not a valid member") and `Lighting.Technology`. Distances below assume the default 1,024-stud target. Allen, please read them off the Properties panel.
- It follows the [[Sessions/2026-10-29#Performance review|2026-10-29 review]]. Its six open items are all still open and re-measured here (drafts, locked upgrades replicated, whole state per push, ~100 NPCs, carts moved by the server, the 0.2 s pad walk and the 0.1 s furnace lerp).
- Overlaps with [[Design/Reviews 2026-10-31/Map Review — Village]] (the first spawn, Workspace leftovers): same numbers, this note adds the runtime cost.

## Top findings, ranked

| # | Finding | Where | Cost | Fix size |
|---|---|---|---|---|
| 1 | Up to ~107 server-driven R15 NPCs in a full server, customers and villagers in friends' real avatars | ShopService.makeNpc 595–636, Friends.build 99–121, EmployeeService.makeWorker 323–362, Rickshaws, DeliveryService, StreetLife | the biggest render and memory item on a phone in a full server; est. 3–10 ms per server frame | medium |
| 2 | The hotbar draws every item in 9 ViewportFrames | Hotbar 97–100, 213–246 | 45 viewports on an 844 × 390 phone's 5-slot bar, 81 on desktop; est. 2–6 ms per frame on a low-end phone | small |
| 3 | Every join builds the station prop swords' etches, 5 canvases at once | SwordRenderer 99–184 → SwordMeshCache.etch 313–380 | measured 96–256 ms of CPU each on the PC; est. ~20 ms extra per frame for several seconds after joining | small |
| 4 | All six plots, their persistent stations and every unbought upgrade go to every phone | TycoonService.setLocked 97–124; 8 Persistent station models; streaming radius | 17.6k plot instances in a full server; 72% of a plot's parts are unbought; 3.7k instances always loaded | small to large |
| 5 | Drafts, rigs and a plot copy still in Workspace | Workspace root | 19.5k of Workspace's 23,632 instances; ~6.2k within 1,024 studs of a lot; three rigs fall and a server Script runs in Play | small |
| 6 | The delivery cart (31 parts) and rickshaws (27) are moved part by part by the server every Heartbeat | DeliveryService 255–265, 570–581; Rickshaws 167–197 | est. 15–35 KB/s per moving vehicle to every client | small |
| 7 | Every change pushes the whole SmithState; 12 listeners, 12 fetches at join | SmithyCore.push 252–257, publicState 213–232; 57 call sites | tens of KB per push late in the game; 12 handlers per push; 12 full builds per join | medium |
| 8 | Every client plays every plot's ore show | OreBoxAnimator 40–63, OreBoxShow 184–346 | with Auto-Roll on six plots: 36 moving ingots, 36 lights, ~108 property writes per frame | small |
| 9 | Holder markers are built for every plot | ShopController.bindSlot 294–439, SlotMarker 42–63 | 204 billboards (≈2.9k GUI instances) refreshed 5× a second; only your 34 can show | small |
| 10 | Five full Workspace scans at start, five Workspace DescendantAdded handlers after | PromptFilter, OreBoxAnimator, ActionButton, PromptStyle, TextLayers | measured 8–10 ms per scan on the PC; est. 0.2–0.3 s at join on a phone; 5 Lua calls per streamed instance | small |
| 11 | The furnace glow is animated by the server at 10 Hz | ForgeService 884–899 | 20 replicated changes a second per heating ingot (≈360/s in a full server) | small |
| 12 | TycoonController binds a streamed-back item again | TycoonController 114–136, 236–249 | handlers stack on every stream-in, on exactly the low-memory phones that stream out | small |
| 13 | Always-on effects: 5 colour grades, Bloom, SunRays, 3 endless UI tweens | WeatherController 41–57; Lighting; MenuController 54 | small per frame; no low-graphics path | small |
| 14 | Shadows, collision fidelity and touch on decor | Plot template, Village | 595 shadow casters under 1.5 studs per plot; 1,072 meshes on Default collision fidelity, 661 never collide | small |
| 15 | ServerStorage.Legacy holds 73,536 instances | ServerStorage | server memory per server, place size, save and publish time | small |

Smaller items, the full per-frame and server-loop inventories, streaming, memory and start-up follow the details.

---

## 1. The NPC crowd

- **Where:** customers `ShopService.makeNpc` (595–636) with `Friends.build` (99–121: `CreateHumanoidModelFromDescription` from a friend's real avatar); crew `EmployeeService.makeWorker` (323–362); rickshaw pullers (Rickshaws); the delivery courier (DeliveryService); 5 villagers (StreetLife 125–127, friends' avatars swapped in over time). All server-owned (`SetNetworkOwner(nil)`), all Humanoids.
- **Count (from the code):** per plot `WALK_INS` 2 + 1 with the Shop Promoter + up to 3 rickshaw riders = 6 customers, up to 3 pullers, up to 3 crafters (Anvils 2–4) + 4 staff, 1 courier: about 17. Six plots: ~102, plus 5 villagers ≈ 107.
- **Cost on a phone (est.):** each is an R15 (15 MeshParts plus accessories); friends' avatars bring their own meshes and textures (and layered clothing when they wear it), so nothing is shared between them. With the whole village in streaming range (finding 4) every phone holds and draws all of them: est. ~15k instances, plus their texture memory. The engine already throttles far rigs' animation (`Animator.PreferLodEnabled`), but not their draw calls or memory.
- **Cost on the server (est.):** every Humanoid runs its state machine and physics each frame, standing or walking: about 30–100 µs each, so 3–10 ms of a 16 ms frame at ~107. Likely the largest server cost. Measure with the server MicroProfiler before acting.
- **Fixes:**
  - While an NPC stands to work or wait (crew in `work`/`scrub`/station waits, customers waiting for an answer), anchor its HumanoidRootPart and set `Humanoid.EvaluateStateMachine = false`; undo before the next `NpcWalk.to`. Rickshaws.seat (200–227) already does this for riders. One helper in NpcWalk (`hold(npc, on)`) and calls at the waits. Small–medium.
  - Plain looks (body colours, as the non-friend customers have) for walk-ins once four or more plots are claimed, friends kept for the first customer per plot and the street. **Allen's call:** [[Design/Decisions Log]] 2026-10-22 "Friends as customers and villagers".
  - Fewer customers at once on a full server would change the shop's pacing: Allen's call, and the sim would need the same change first.
- **Risk:** an anchored NPC still animates (the Animator runs on an anchored root); unanchor before walking or it will slide.

## 2. The hotbar's nine viewports per item

- **Where:** `Hotbar` 97–100 builds `RIM`, eight 1 px offsets; `drawArt` (213–246) makes a ViewportFrame for each offset with a white Neon copy of the model, then one for the model itself: **9 ViewportFrames per item slot**, rendered every frame while the bar shows.
- **Count:** `BAR_SLOTS` 9 at 84 px with 13 px gaps; on touch the bar leaves the 170 px jump corner. On an 844 × 390 phone (scale 0.75) that is 5 slots: **45 viewports**. On a 1080p desktop: 9 slots, **81**. The open bag's cards use the same drawing: up to 30 visible, 270 more.
- **Cost (est.):** every ViewportFrame renders its own small scene each frame. LihFolk's note on virtualized lists: "30 visible viewports are expensive on phones". Est. 2–6 ms per frame on a low-end phone for the bar alone, more with the bag open.
- **Fix:** put the eight rim copies into **one** Outline viewport behind the main one, nudged round a circle, as `ItemPicker.outline` (381) already does for picker cards: 2 viewports per slot, 10 on that phone. Same look. Small.
- **Risk:** none for the look Allen picked (the dark rim). Check the rim's thickness at 0.7 scale after.
- **Measure:** on a phone, the MicroProfiler with an empty bar, then a full bar of swords.

## 3. The prop swords' etches at every join

- **Where:** 21 `ForgedSword` models per plot inside the station models: `Smithy.EtchingTable.Dress.PropSwords` (6) + `DemoSword`, `EtchingTable2` (6), `PolishStation.PropSwords` (4, `Shimmer`), `PolishStation2` (4). The stations are Persistent, so all of them reach every phone at join, bought or not. `SwordRenderer.render` (99–184) draws each one; `SwordMeshCache.etch` builds a stroked pattern's canvas with `spread = true`, and `waitFor` (78–82) only waits on the same key, so different patterns build at the same time and their 4 ms slices stack (`EtchCanvas` `SLICE`, 41–45).
- **Unique canvases:** 5 among the props (Fracture on a wakizashi, Eclipse on a katana, Tide on a tantō, Stormroot on a gladius, Woven Wind on the DemoSword's katana); the second table's copies share their keys. It becomes 7 once the three misnamed props (Seen, not changed) are fixed.
- **Measured (PC, unspread, original modules required, nothing parented):** katana Eclipse 101 ms to make + 155 ms to reveal = **256 ms**; wakizashi Fracture 103 + 120 = **223 ms**; tantō Tide 36 + 60 = **96 ms**. Stormroot and Woven Wind weren't timed (est. 150–250 ms each). The images are 1024 × 384 (1.5 MB each while live) and 1024 × 128.
- **Cost (est.):** ~1 s of PC CPU on every join, 4–6 s on a low-end phone, as 5 × 4 ms ≈ 20 ms extra per frame until the short ones finish: a few seconds of 20–30 fps right after joining, while the HUD, the scans (10) and streaming also run. For a new player all of it is for props hidden on locked stations.
- **Also:** the 8 shimmer props per plot each run `SwordRenderer.glint` (33–77), a PointLight and a 0.6 s Heartbeat sweep every 1.2–2 s (skipped while hidden): 48 of them with six plots.
- **Fixes:**
  - SwordRenderer draws a ForgedSword only once no TycoonItem above it is `Locked`, and again when that changes. Small.
  - One queue for every `spread` build in SwordMeshCache, one at a time (the 2026-10-23 rule for etch work: several spread builds stack their slices). Small.
  - Later: the props never change; their five images could be baked once and uploaded, so they cost no canvas at all. Medium.
- **Risk:** none for gameplay. The Polishing wall's shimmer (Decisions Log: "have the sword shimmer more") stays.

## 4. Six plots on every phone

- **Measured on the template (`Workspace.Plot`):** 2,942 instances, 2,058 parts (1,072 MeshParts), 52 prompts, 19 PointLights (none cast shadows), 12 SurfaceGuis.
- **Unbought upgrades:** 48 `TycoonItem`s with an `Upgrade` hold 2,049 instances and **1,491 parts, 72% of the plot**. They replicate to everyone; the server turns off their collision, queries, touch, prompts, lights, GUIs and particles (`TycoonService.setLocked`, 97–124) and each client hides them with `LocalTransparencyModifier`. Hidden parts aren't drawn, but they cost memory, streaming and the per-part shading on every stream-in.
- **Empty lots:** about 808 instances and 485 parts each (PlotService strips the upgrades, pads and spawns).
- **Persistent:** 8 station models per plot (EtchingTable 112 parts, EtchingTable2 109, PolishStation 78, PolishStation2 78, SwordRack 20, IngotRack 19, SwordRack2 8, IngotRack2 7 = 431 parts, 622 instances with the 21 prop swords) are on every client from join and never stream out.
- **Full server:** 6 × 2,942 ≈ 17.6k plot instances and 12.3k parts on every phone; 3.7k of them persistent. The village is about 1,100 × 1,300 studs, so at the default 1,024-stud target every lot streams in every other lot and all their NPCs.
- **Fixes, smallest first:**
  - `ModelStreamingMode = PersistentPerPlayer` on the 8 station models in the template, and `model:AddPersistentPlayer(owner)` in a PlotService `onPrepare` hook (the map review's #4, [[Sessions/2026-10-30#Proposals and the map review]]). Other players' stations then stream like the rest. Your own scripts bind only your own plot's racks and stations (RackController 34; PolishController and EtchingTableController use MyPlot), and SwordRenderer re-renders on a re-tag, so the Atomic behaviour for non-owners is safe. Small.
  - Read the streaming settings. Then try `StreamingTargetRadius` 512 with `StreamOutBehavior = Opportunistic` on a phone, and `Model.LevelOfDetail = StreamingMesh` on the shop and workshop shells so far plots keep a cheap stand-in. Small to set; needs a pop-in check on the street (LihFolk's Instance Streaming note keeps 1,024 as the default for a reason).
  - Keep unbought TycoonItems in ServerStorage per plot and parent them in when bought. Large: TycoonService.setLocked/refresh, TycoonController.build (the build-in reads the parts as they unlock), ShopService's holders, the Upgraded Store push and the empty plots all assume the parts are there. The biggest memory win for every new player's plot.

## 5. Leftovers in Workspace

| What | Instances | Parts | Lights (shadow) | Where | Nearest lot |
|---|---|---|---|---|---|
| `A3_Compact` | 1,788 | 1,323 | 16 (2) | x 1,600 | 866: **in range** |
| `A2_Zones` | 1,788 | 1,323 | 16 (2) | x 1,800 | 1,066: at the edge |
| `B_OneRoof`, `Z_B_Bands`, `Z_C_ForgeRing`, `Z_D_Court`, `Z_E_Line` | 9,577 | 7,131 | 81 (11) | x 2,200–3,000 | 1,465+ |
| Plot copy at x ≈ 2,000 (`Smithy`, `Shop`, `Parking`, `DeliveryBay`, `Fence`, `Workshop`, `Ground`, `Yard`, `CustomerSpawn`, `PlayerSpawn`) | 1,925 | 1,438 | 16 (2) | x ≈ 2,000 | ~1,262 |
| `GreatSwordRig` | 1,579 (1,198 Pose, 78 Keyframe, 7 KeyframeSequence) | 22, none anchored | 0 | (741, 81, −407) | 111: **in range** |
| `Sword Animations` | 2,593 (2,303 Pose, 140 Keyframe) | 17, none anchored | 0 | (752, 88, −460) | ~177: **in range** |
| `Swordsmith` (R6 rig) | 79 | 10, 9 unanchored | 0 | (674, 3, −276), inside lot N2's footprint | 35 |
| `Weapon Rack` (72 Textures), 11 `Bamboo` models (`Bamboo1`–`12`, no 5), `AuxScene` (5 unanchored at y 57), `ZanbatoPreview` (y 304), `Courtyard`, `MaterialDemo` (empty), `Workspace.Lighting` (4 post effects that do nothing outside Lighting) | 205 | 84 | 1 | near the origin | 464–770: in range |

- **Totals:** ~19.5k of Workspace's 23,632 instances are unused (the live map is Village 1,153 + Plot 2,942 + Baseplate, Terrain, Camera). About 6.2k of them are within 1,024 studs of a lot, so every phone streams them in. The server holds all of them.
- **In Play:** the three unanchored rigs and AuxScene fall and settle (server physics, replicated); `GreatSwordRig.Great Sword.AnimController` is a server Script that, once its Tool counts as equipped, loops `while wait() do` playing Idle; `README` is a Script too; the KeyframeSequences in Workspace replicate to every client.
- **Fix:** move all of it to `ServerStorage.Legacy` (or export each to .rbxm). No script reads any of it (grep: only a SwordSlash comment names `Sword Animations`). Keep Village, Plot, Baseplate (the outer grass), Terrain, Camera. Small.
- **Risk:** Allen moves and adds things himself, so some may be his references (the Swordsmith, the bamboo, ZanbatoPreview). His call per item.

## 6. The cart and the rickshaws, part by part

- **Where:** DeliveryService `set` (255–265) does `c.model:PivotTo`, sets each wheel's CFrame and pivots the courier, from a Heartbeat (570–581) while leaving and returning; Rickshaws `place` (167–181) does the same from `run` (184–197) every Heartbeat of a trip, plus the puller and rider.
- **Measured:** `Plot.DeliveryBay.Cart` is 31 parts, all Anchored, no welds; `ServerStorage.Rickshaw` is 27 parts, all Anchored, no welds.
- **Cost (est.):** pivoting an anchored model writes every part's CFrame, and every changed CFrame replicates to every client: ~29 CFrames × ~20 bytes × 30–60 updates a second ≈ 15–35 KB/s per moving vehicle per client. A cart trip is about 40 s of driving; rickshaws come with customers; a full server moves several at once. The server also pivots 31 parts per frame and serialises them six times.
- **Fix:** weld every part to the root with WeldConstraints, unanchor the rest (Massless), keep only the root anchored and move only it: one CFrame per vehicle per frame. Wheels then turn on a Motor6D, or on clients. Small (two templates and `set`/`place`). Better later: drive it on clients from a start-time attribute, as OreBoxShow does. Medium.
- **Risk:** check the cart's collision-group swap (DeliveryService 287–291) still reaches every part.

## 7. The whole state on every change

- **Where:** `SmithyCore.push` (252–257) fires `publicState` (213–232) to the owner. 57 call sites: ShopService 18, EmployeeService 13, ForgeService 5, DeliveryService 4, DevTools 4, SmithyCore 3, TycoonService, SmithService and StoreService 2 each, Etch, Polish, Rack and Inventory 1 each.
- **What it sends every time:** every carried sword with 13 fields and its `refinement` array (one number per blade station), `collection`, `mailLog`, `orders`, `delivery`, `crafter`, `staff`.
- **Client:** 12 live scripts listen to `SmithState` (13 with the Studio-only TestAnvil) and each calls `GetSmithState` at start: 12 full builds and sends per join. Some re-render open windows on every push (DeliveryController 788–806, EmployeeController 901).
- **Cost:** the 2026-10-29 review measured about 26 KB for 30 swords; with a crew working (13 push sites) pushes come every few seconds late in the game.
- **Fixes:**
  - One client module that fetches once and hands each push to the listeners; the 12 scripts swap two lines each. Small–medium.
  - Public swords without `refinement`: art only needs the polish level (`SwordMeshCache.quantize`, 84–91, rounds to it); PolishController asks for the array when polishing starts. Medium.
  - Later: send only what changed.
- **Risk:** medium (many controllers), no gameplay change.

## 8. Every plot's ore show on every client

- **Where:** OreBoxAnimator binds every `OreRoller` in Workspace (40–52), so `OreBoxShow.new` (184) runs every plot's roll on every client: up to 6 cloned ingots, each with a PointLight (range 6), and every frame a CFrame, Size and Brightness write per ingot (`pose`, 273–346), plus cloned sounds, sparks, light columns and callouts.
- **Cost:** with the Auto Ore Roller pass every plot can roll nonstop: up to 36 moving ingots and 36 lights and ~108 property writes per frame, whether the plot is next door or 300 studs away.
- **Fix:** in `OreBoxAnimator.start`, skip the show when the roller is far from the camera (say over 120 studs) or off screen; the real ores still appear when the server reveals them. Small.
- **Risk:** a neighbour's roll seen from far away doesn't animate.

## 9. Holder markers for every plot

- **Where:** ShopController binds every `DisplaySlot` (440–443) and makes a SlotMarker (380); SlotMarker clones `ShopHud.Templates.SlotMarker` (a BillboardGui with 13 descendants) into PlayerGui (68–71) and refreshes every live marker every 0.2 s (42–63). The marker's state (381–382) is false unless `MyPlot.owns(part)`.
- **Measured:** 34 DisplaySlots per claimed plot (empty plots lose the tag). Six claimed plots: 204 markers, ≈2.9k GUI instances (plus a UIScale and 4 press connections each, and HudFocus and TextLayers bind every one), ~1,000 refreshes a second. Only your own 34 can ever show.
- **Fix:** `bindSlot` returns unless `MyPlot.owns(part)`, and binds again when the `Plot` attribute arrives (it already listens, 427). Small.

## 10. Start-up scans

- **Where:** PromptFilter 45 + 48 (and 77–81 again when your Plot arrives), OreBoxAnimator 49–52, ActionButton 33–36, PromptStyle 36–39, TextLayers 77–84 (Workspace and PlayerGui), HudFocus 139–142 (PlayerGui).
- **Measured (PC, Edit):** `workspace:GetDescendants()` of 23,632 instances took 5.1 ms and one IsA or Name pass over it 2.3–4.5 ms: 8–10 ms per scan, ≈50 ms for the six.
- **Cost (est.):** 0.2–0.3 s of script time at join on a low-end phone (less is streamed in at that moment, but every instance that arrives later goes through five Workspace `DescendantAdded` handlers: ~20k+ calls in a full server).
- **Fix:** give the prompt templates `Style = Custom` in Studio (and the `ScreenButton` ones) so PromptStyle and ActionButton need no scan; one shared prompt watcher for PromptFilter, PromptStyle and ActionButton; OreBoxAnimator on a tag. Small–medium.

## 11. The furnace glow, from the server

- **Where:** ForgeService 884–899: every 0.1 s, for each heating slot on every plot, `slot.visual.Color = …:Lerp(HOT, f)` and its PointLight `Brightness = 2 * f`; `refreshBoard` (136–160) every tick (mostly unchanged writes; the time text changes once a second).
- **Cost:** 2 replicated changes × 10 Hz per heating ingot: with three furnaces on six plots, ≈360 changes a second to every client (est. 5–7 KB/s each).
- **Fix:** set the start and end once (attributes on the slot) and let ForgeController tween the colour and the light on each client. Small.

## 12. TycoonController binds again on stream-in

- **Where:** `watchItem` (114–136, CollectionService's added signal for `TycoonItem`) and `watchSlot` (236–249, `DisplaySlot`) connect every time. A streamed-out instance comes back as the same instance and the added signal fires again (the 2026-10-29 lesson behind ShopController.bindSlot's fix).
- **Cost:** each stream-in of another plot's item stacks a `Locked` handler (GetDescendants and shading) and a DescendantAdded handler; each holder stacks an `Occupied` handler (a `swordOn` poll and a build). 50 items and 34 holders per plot. It only bites when parts stream out, which happens on low-memory phones.
- **Fix:** a weak `watched[inst]` guard, as OreBoxAnimator (39–42) has. Small.

## 13. Always-on effects

- **Colour grades:** WeatherController (41–57) enables all four weather grades with neutral values and fades between them, so five ColorCorrectionEffects are always on. Turn a grade off once its fade-out ends. Small.
- **Post effects:** Bloom (intensity 0.5, size 40, threshold 1.2), SunRays 0.06, Atmosphere (density 0.32, haze 1.6), GlobalShadows on (softness 0.6); DepthOfField off. No low-graphics path. Option: a Settings "Low graphics" switch that turns Bloom and SunRays off. Allen's call.
- **Endless UI tweens** repaint their screen every frame: MenuController 54 (the Shop button's rays, always), AutoRollController 59 and AnvilController 830 (while on). Stop each while its GUI isn't visible. Low.

## 14. Shadows, collision fidelity and touch on decor

- **Measured (template):** 1,242 of 2,058 parts cast shadows, 595 of them under 1.5 studs; all 1,072 MeshParts use CollisionFidelity Default and 661 of them never collide; CanTouch is on for 479 parts. Village: 669 casters, 4 small, CanTouch 12.
- **Cost:** shadows switch off below graphics level 4 (LihFolk, Art Budgets), so low-end phones don't pay for them; mid-range phones and PCs do. Default fidelity stores a convex decomposition for every mesh (place size, memory, query cost).
- **Fix:** one bulk pass on the template and the village: CastShadow off under 1.5 studs; CollisionFidelity Box on meshes with CanCollide and CanQuery both off; CanTouch off on decor. Small. No geometry moves, so the no-z-fighting check is unaffected.
- **Risk:** leave alone any part that should block a wall check (PromptFilter and the pad labels' raycasts use CanCollide, CanQuery and Transparency).

## 15. ServerStorage.Legacy

- **Measured:** 73,536 instances in 281 children (`TownRedesign_before_20261022045159` 10,189, `TownRedesign_v2_parked` 9,652, `Village_beforeRoads` 7,016, `Village_before_20261022004542` 6,802, `Village_before_20261022052609` 6,787, `Village_before_20261021233750` 2,528, `Plot_beforeOutsideSmithy` 2,516, …), and script backups again since the 2026-10-27 clean-up (`ShopService_beforeFixes2`, `ShopService_beforeMoreFeatures`, …). Also `DecorCandidates` 984, `Buildings3D` 669, `UIPackCopies` 417. Edit's `Stats.InstanceCount` is 121,287.
- **Cost:** not replicated, but every server loads it (memory per server), and it slows saves, publishes and Studio (3.1 GB on 2026-10-30).
- **Fix:** export to .rbxm files on disk and delete; Version History keeps them too. Allen's call.

## Smaller items

- **Idle per-frame work** (inventory below): PolishController 118 (Heartbeat) and 562 (RenderStepped) run all session, writing the scrape Sound's Volume and the ghost every frame with no station open: connect them while `active`. TycoonController 417 walks your plot's 80 pad markers (160 FindFirstChild) and writes the Buy button's Text, Adornee and Enabled every frame: keep a list of standing pads. Guide 249 writes the spotlight's Enabled, DisplayOrder and ghost every frame with nothing spotlit: return early. Small each.
- **SurfaceGuis:** the three Parking signs are FixedSize 800 × 600 (1.9 MB each once bought) for one label; the leaderboard is 700 × 430; every world SurfaceGui has MaxDistance 0 (no limit). PixelsPerStud ~40 on the signs and MaxDistance ~150 on all. Small.
- **Pathfinding:** `NpcWalk.follow` (63–123) computes a path for every walk (twice when stuck). The crew walk the same station-to-station routes on a fixed layout: cache the waypoints per plot and route, cleared on a buy. Est. ~4 ComputeAsync a second in a full server. Medium.
- **A server tween on an NPC:** `EmployeeService.scrub` (411–445) tweens a shoulder attachment on the server while polishing, replicated every frame. An animation would cost nothing. Small.
- **Friends caches:** `Friends` keeps `lists` and `looks` (28–30) for the server's life and never trims them when players leave: slow growth on long servers. Small.
- **The first spawn:** a joiner spawns before PlotService claims a plot, on another player's PlayerSpawn or nowhere, and is moved home later, so the client streams the wrong place first. Fully written up, with the fix, in [[Design/Reviews 2026-10-31/Map Review — Village#1. A joining player spawns outside their own plot until their save loads (arrival)|Map Review — Village §1]].
- **TestAnvil** (a Studio-only station) ships in every live plot: 13 instances and a ShapePrompt that does nothing outside Studio. Small.

## Client per-frame and polling inventory

| Script:line | Runs | Does | Idle cost | Could be |
|---|---|---|---|---|
| TycoonController:417 | Heartbeat, always | `padUnderfoot` over 80 markers, Buy button writes, `bindPad`, `UiFx.onGamepad` | ~0.02 ms (PC) | standing-pad list, 10 Hz |
| TycoonController:388 | every 0.2 s | every plot's 80 pad markers, `workspace:GetChildren`, `buildingAt` twice and `inSight` (≤4 raycasts) per label in range, LTM and CanCollide per pad part | measured 0.07 ms a tick for 6 plots (PC) | own plot and standing pads only |
| TycoonController:90, 151 | Heartbeat during a build or pop | `BulkMoveTo` (194 parts for the Upgraded Store) | only while building | fine |
| RoofHider:66 | RenderStepped | `GetTagged("HidesRoof")` (12 with six plots), two passes; GetDescendants only while fading | measured 0.014 ms + GetTagged (PC) | fine |
| WeatherController:128 | RenderStepped | the effect's CFrame; every 0.25 s two `inZone` and one raycast | tiny | fine |
| WeatherController:207 | every 0.25 s | the icon and tip | tiny | fine |
| Guide:90 | RenderStepped | the glow's pulse, while adorned | tiny | fine |
| Guide:199 | RenderStepped | a straight route and up to 6 beams (12 attachment CFrames) while there's a target | small | fine |
| Guide:249 | RenderStepped | the spotlight; idle, 3 writes | tiny | early return |
| Guide:769 | every 0.25 s | `goal()` | small | fine |
| AnvilController:923 | RenderStepped | returns unless forging; Auto Anvil's strike check while ready | tiny | fine |
| PolishController:118 | Heartbeat, always | the scrape's Volume | tiny | while active |
| PolishController:562 | RenderStepped, always | `MyPlot.current()`, ghost writes | tiny | while active |
| OreBoxAnimator:54 | RenderStepped | poses every plot's show | none idle; ~18 writes per show per frame | finding 8 |
| SwordRenderer:63 | Heartbeat for 0.6 s every 1.2–4.5 s, per mirror or shimmer sword | the glint sweep, a NumberSequence per frame | grows with polished swords in range (48 shimmer props with six plots) | skip far or locked |
| FreeMouse:15 | BindToRenderStep | two `IsKeyDown` | tiny | skip on touch-only |
| CoinFly:46 | Heartbeat per counter | returns at once when settled | tiny | fine |
| SlotMarker:45 | every 0.2 s | every marker's refresh | ~1,000 refreshes a second with six plots | finding 9 |
| PromptFilter:54 | every 0.25 s | all prompts; your enabled ones in range get `MyPlot.blocked` (≤6 raycasts) | small | fine |
| AutoRollController:228 | every 0.25 s | `near()`, ≤6 raycasts | tiny | fine |
| EmployeeController:906, 1100 | every 0.5 s, 0.25 s | status text; the nearest of your workers | tiny | fine |
| DeliveryController:813 | every 0.5 s | the pin and timers | tiny | fine |
| MenuController:60 | every 5–9 s | the Shop icon's hop (plus the endless rays tween, 54) | a repaint every frame | stop while hidden |
| MailController:424, ShopController:228 | 1 s per popup, 0.25 s per offer card | countdowns | tiny | fine |
| HiltSeat:284, EtchingTableController:146 | RenderStepped while in use | camera and show | only in use | fine |
| Hotbar | rendering | 9 ViewportFrames per slot | finding 2 | finding 2 |

Measured on the PC these loops are small one by one: idle Luau is about 0.1 ms a frame, est. 0.5 ms on a low-end phone, with a bump every 0.2–0.25 s when the polls line up. The big client costs are what is drawn and held (findings 1–4), not these loops.

## Server loop inventory

| Script:line | Runs | Does | Cost |
|---|---|---|---|
| ShopService:1297 | every 0.5 s per plot | the Cashier's till | cheap |
| ShopService:1305 | every 1 s per plot | the mail clock: `refillOrders`, a push when an order arrives | cheap |
| ShopService:1317 | per plot | the customer spawner (45–75 s gaps, Sunshine ×2, the Promoter) | cheap; NPCs, finding 1 |
| ForgeService:632 | every 0.25 s | Auto-Roll pulls | cheap |
| ForgeService:885 | every 0.1 s | the furnace glow and boards | finding 11 |
| ForgeService:280 | Heartbeat during a cart roll | the old mine-cart track | unused (CartPath has 0 points) |
| EmployeeService | 1–2 s waits, `work` 0.9 s, `scrub` 0.45 s | the crew's jobs; 13 push sites | cheap CPU; pushes, finding 7 |
| DeliveryService:547, 570 | every 0.5 s; Heartbeat | the board's timers; the carts | finding 6 |
| Rickshaws:194 | Heartbeat per trip | the rickshaw | finding 6 |
| NpcWalk:98–115, 165, 204 | 20 Hz per walking NPC; Heartbeat for 0.3 s per turn; 7–16 s look-around | walking | cheap; ComputeAsync per walk |
| StreetLife:153 | every 0.5 s | 5 villagers | cheap |
| Weather:67 | every 1 s | the weather clock | cheap |
| LeaderboardService:148 | every 120 s | 3 SetAsync per player, 3 GetSortedAsync, 60 labels per board | cheap |
| SmithyCore:1210, Analytics:322 | autosave, flush | saves and events | cheap |
| PlaytestLog:85, 100 | 1 s, 15 s | Studio only: positions and posts | none live |
| Friends:49, 133 | background | friend lists and rigs | web calls |

The server's big costs (est., to measure): the ~107 Humanoids (1), moving vehicles and their replication (6), pathfinding, and the 12 state builds per join (7).

## Streaming

- `StreamingEnabled` is on; the radius and stream-out behaviour can't be read by a script (see the top).
- Persistent: the 8 station models per plot (finding 4). Atomic: the 21 prop swords inside them. Everything else Default.
- The village fits inside the default 1,024 target from any lot, so streaming saves nothing between plots today.

## Memory

- **Editables are handled well:** SwordMeshCache bakes live meshes and finished etch images to static content (`CreateDataModelContentAsync`) and frees the editable at once; ItemPicker builds etched card art one at a time (214–219) and releases on close; BladeView and BladeMesh go with their sessions (AnvilController 524 and 588, PolishController 306–319, EtchPlayback 286–305).
- **The one spike:** finding 3, five live canvases at join (~6.5 MB).
- **ViewportFrames:** the hotbar (2). The Book keeps its built cards, two viewports each, while shut (CollectionController 100): fine.
- **Crew and sender looks:** EmployeeService builds 19 posed R15 rigs (5 crafters, 4 staff, 10 senders) into `ReplicatedStorage.Crafters` and `Senders` at server start, so every client gets them at join (est. 2–2.5k instances) for the portraits.
- **Connections:** guarded against re-streaming in PromptFilter, OreBoxAnimator, TextLayers, HudFocus, ShopController.bindSlot and SwordRenderer; not in TycoonController (12). SlotMarker's loop ends with its script (45).

## Start-up

1. ReplicatedStorage (727 instances, plus the ~2.3k crew and sender rigs), StarterGui into PlayerGui (2,571), 44 player scripts.
2. The character spawns before the plot (Smaller items).
3. Client scripts: the scans (10), 12 `GetSmithState` calls (7), markers for every plot's holders (9), and SwordRenderer drawing every streamed sword, the props included (3).
4. Server: the save loads, PlotService clones the template (2,942 instances) and runs its hooks; ShopService puts the displays back; TycoonService refreshes (a GetDescendants over the plot).

The biggest client items at join are 3 and 10; the biggest download is the persistent stations of every plot (4).

## Possibly in progress (other agents today)

- **Auto Anvil** (AnvilController 826–876, 952–954): the strike check runs only while forging and ready; an endless spin tween on its icon while on. No concern.
- **Crew level bars** (EmployeeController 1029–1121, `EmployeeService.showLevel` 525–530): `Level` and `Progress` attributes are set once per job (they replicate to every client, once per job), the bar updates on AttributeChanged, and a 0.25 s loop finds your nearest worker. No concern.
- **World store purchase spots, WorldStoreController, shop roofs:** not in the place yet when this was read.

## Seen, not changed

- Three prop swords name their etch by its display name: `PropSword_FallingStars_katana` and `_gladius` ("Falling Stars"), `PropSword_WovenWind_wakizashi` ("Woven Wind"). The ids are `FallingStars` and `WovenWind`, so `SwordMeshCache.etch` doesn't treat them as stroked: they likely show no etch and warn "no bake". Check in Play.
- `Workspace.Swordsmith` stands inside lot N2's footprint (x 674 within 596–680), so it would sit in the claimed N2 plot's yard in Play.

## What to measure in Play (for Allen)

These turn the estimates above into numbers. A phone run matters most; Studio's device emulator says nothing about speed.
1. **Phone frame time:** in the Roblox app's settings turn the MicroProfiler on and capture from a PC browser on the same Wi-Fi. Compare an empty hotbar with a full bar of swords (2); the first 15 s after joining with a minute later (3, 10); standing at your plot with six plots full (1, 4).
2. **Server:** with several test clients or a live server, the Developer Console's Server MicroProfiler and `HeartbeatTimeMs`, before and after anchoring idle NPCs (1).
3. **Network:** `DataReceiveKbps` while a cart or a rickshaw drives and while it's parked (6), and while three ingots heat (11).
4. **Memory:** the Developer Console's Memory tab (Instances, GraphicsTexture, GraphicsMeshParts, Animation) with one plot claimed and with six.
5. **Settings:** Workspace's streaming properties.

A read-only line to run on the Client or Server datamodel during Play (every field is readable; checked in Edit):

```luau
local S = game:GetService("Stats")
return string.format("inst=%d prims=%d moving=%d mem=%.0fMB recv=%.1fkbps send=%.1fkbps hb=%.2fms frame=%.1fms draws=%d shadowDraws=%d tris=%d",
	S.InstanceCount, S.PrimitivesCount, S.MovingPrimitivesCount, S:GetTotalMemoryUsageMb(), S.DataReceiveKbps,
	S.DataSendKbps, S.HeartbeatTimeMs, S.FrameTime * 1000, S.SceneDrawcallCount, S.ShadowsDrawcallCount, S.SceneTriangleCount)
```

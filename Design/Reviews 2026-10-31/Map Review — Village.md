---
title: Map Review — Village
type: review
updated: 2026-10-31
tags: [review, map, village, arrival, lighting, weather, performance, streaming, create-swords]
---

# Map Review — Village (2026-10-31)

Allen: "spawn map reviewers and review every part of the map, what needs to be added or changed, what doesn't match the style of our game." This note covers everything outside the plot: `Workspace.Village` (walls, gate, shrine, street, lots, street furniture), arrival, empty lots, boundaries, the backdrop, lighting and weather, and what Workspace costs. The plot itself (shop, yard, stations, pads) is the other map reviewers' area.

**How it was done.** Read-only, in Edit (Studio was never put in Play). Every number below was measured with `execute_luau`, Edit-mode pathfinding or pixel samples of `screen_capture` images; nothing was moved or changed except the Edit camera, set back to Fixed after each capture. Skills: roblox-collaboration-mode, lihfolk-worldbuilding, roblox-building, roblox-lighting, roblox-performance. Every suggestion was checked against the [[Design/Decisions Log]].

**Can't be read by a script:** `StreamingTargetRadius`, `StreamingMinRadius`, `ModelStreamingBehavior`, `StreamOutBehavior` and `StreamingIntegrityMode` aren't scriptable. Distances below assume the default 1,024-stud target. Allen, please read them off Workspace's Properties.

**While this ran:** another session's temporary `_RoofCapTmp_Starter` and `_RoofCapTmp_Upgraded` stood on lots N1 and N3 (1,318 instances, 37 prompts). They are left out of the counts below, and that session should remove them.

## Findings, most valuable first

### 1. A joining player spawns outside their own plot until their save loads (arrival)

- **Where:** `ServerScriptService.PlotService` (`claim`, lines 147–198); `Players.CharacterAutoLoads` = true; the SpawnLocations in Workspace.
- **What's wrong:** the character loads as soon as the player joins, but the plot is only handed out after `SmithyCore.waitLoaded`. Until then there's no `RespawnLocation`, so the engine picks a spawn by its own rules:
  - **First player in a server:** at runtime no spawn in Workspace is enabled. The template's `PlayerSpawn`, the only enabled one, moves to ServerStorage with the template, and the other 8 (seven drafts and the copy at x 2000) are `Enabled = false`. The player appears at the engine's default spot by the world origin, on the old 2,048 × 2,048 grass baseplate, about 650 studs west of the village. Capture V13 shows that view: open grass and the backs of the block mountains. Near that spot are 11 stray Bamboo models, the old Courtyard lanterns, a "fantasy_anvil" that is unanchored and drops from y 57, and `ZanbatoPreview` hanging at y 304.
  - **Later players:** every claimed plot's `PlayerSpawn` is enabled and Neutral, so a joiner spawns at a random **other player's** yard spawn. They stand there until their own lot is ready, then `PivotTo` jumps them home.
  - **How long:** usually a second or two. If the save is still locked by another server (a quick rejoin or a crashed server), `Profiles.load` waits up to 6 × 5 s = **30 s**, the whole time in the wrong place.
  - The jump home has no `RequestStreamAroundAsync`, so on a phone the yard may still be streaming in when they land.
- **Why it hasn't shown in Studio:** in Play Solo the character can spawn before PlotService moves the template, on the template's own spawn in N2's yard, which is also where the first player's plot goes.
- **Evidence:** the SpawnLocation list (16 in the place; in Workspace only `Plot.PlayerSpawn` is enabled). The code comment at line 187: "spawned before the claim: bring them home". The `Profiles` defaults are `tries 6`, `wait 5`.
- **Fix (small, PlotService only):** set `CharacterAutoLoads` to false and call `player:LoadCharacter()` in `claim` right after `RespawnLocation` is set. Add a fallback `LoadCharacter` at a street spawn for anyone who gets no plot (a 7th player). Or, more simply, keep auto-load and add one enabled Neutral SpawnLocation on the street in front of N2 (640, 0.2, −200), so the wait is spent in the village looking at the first shop. Then set the plots' own spawns to `Enabled = false`, after checking that `RespawnLocation` still honours a disabled spawn. Either way, call `RequestStreamAroundAsync(spawn.Position, 3)` before the pivot.
- **Decisions:** none against. [[Design/Six Plots]] says "the player spawns on the plot's PlayerSpawn", and this makes it true from the first frame.

### 2. 83% of Workspace is unused, and some of it does things at runtime (cost and clutter)

- **Where:** top-level Workspace. The counts are in [[#Workspace counts]].
- **What's wrong:**
  - **Totals:** 23,632 instances, the same total as yesterday's review. Only Village (1,153) and the Plot template (2,942) are live. The other **19,534 are unused**: seven layout drafts (13,153 instances, 113 lights), the dismantled plot copy at x 2,000 (`Smithy`, `Shop`, `Parking`, `DeliveryBay`, `Fence`, `Workshop`, `Ground`, `Yard`, `CustomerSpawn`, `PlayerSpawn`: 1,925 instances, 16 lights), two animation rigs (4,172), and 284 small leftovers.
  - **The two rigs fall at runtime.** `GreatSwordRig` (0 of 22 parts anchored) hangs at (741, 84, −407) and `Sword Animations.Sword Slashes` (0 of 17 anchored) at (752, 88, −460). Both float in Edit captures (V4) and drop when the game runs.
    - GreatSwordRig lands behind the north wall by lot N3. Its Humanoid shows its name ("GreatSwordRig") to anyone within 100 studs.
    - It carries a third-party Tool whose `AnimController` and `README` Scripts run on the server. They're harmless, but they're outside code.
    - Between them the rigs hold 3,501 keyframe `Pose`s. At 120–400 studs from every lot they are in streaming range, so every client receives about 4.2k instances, as much as the whole live map in a one-player server.
  - **Drafts in streaming range:** `A3_Compact`'s nearest part is 819–1,013 studs from the lot centres, so all six lots get it at the default radius. `A2_Zones` is 1,019 from N3/S3. Each is 1,788 instances with 16 lights.
  - **Loose NPC:** `Workspace.Swordsmith`, an R6 NPC in a straw gasa hat at (674, 3, −276), stands in lot N2's yard 12.6 studs from `TestAnvil`. It isn't part of the template, so only the first player's plot would show it. It may be today's Auto Anvil or crew work; if not, it goes too.
  - **Dead effects:** `Workspace.Lighting` is a Folder holding SunRays, DepthOfField, ColorCorrection and Bloom. Effects only work under Lighting or the Camera, so this second set does nothing and is easy to confuse with the live one. `MaterialDemo` is an empty folder.
- **Fix (small):** move all of it to `ServerStorage.Legacy`, not delete. The drafts stay there for side-by-side comparisons, and `Sword Animations` is the source of the slash animation that `SwordSlash` names. No script reads any of it: the grep found only plot-local `Parking` / `DeliveryBay` and a comment. That leaves Workspace at 4,098 instances in Edit.
- **Decisions:** yesterday's review item 3 ([[Sessions/2026-10-30#Proposals and the map review]]), still open.

### 3. The backdrop reads as dark teal walls, and it fills the first frame (look)

- **Where:** `Lighting.Atmosphere` (Density 0.32, Offset 0.22, **Haze 1.6**, Color 206/224/242, Decay 110/146/190); `Village.Atmosphere.Backdrop.Mountains` (185 blocks, 300–700 studs out, Grass 66–84 / 100–118 / 52–58).
- **What's wrong:**
  - At that distance the heavy blue haze turns the green blocks into flat dark blue-teal.
  - From a new player's spawn (capture V3: the yard, back wall and mountains) the mountains are **24% of the frame at RGB about (30, 84, 111), luminance 69–73**, against about 181 for the sky and 183 for the yard. In street and gate views they are 12–13%.
  - It's the coldest, darkest large field in a warm-afternoon look, and on phones without shadows value and colour are all that carry the scene.
  - The near haze also tints the cream town wall blue at 80 studs: (133, 172, 196).
- **Fix (small, lighting values only):**
  - Try Haze about 0.8–1.0 (LihFolk's bright-cartoon preset is 0.5) and a lighter, warmer `Decay`, part-way to the `StyleTest_*` values still stored on the Atmosphere (Color 232/206/178, Decay 150/150/172, Haze 1.3, Offset 0.1).
  - Optionally lift the blocks' Grass colours about 25% so they recede.
  - Judge on a phone. The block shapes stay as they are.
- **Decisions:** Block mountains (2026-10-22); "No smooth trees or rounded mountains" (2026-10-22: the Genshin lighting stays); warm late-afternoon lighting (2026-10-19). This tunes the approved lighting; it doesn't replace it.

### 4. Weather changes only a colour grade, and the grades stack on an already saturated base (look)

- **Where:** `StarterPlayerScripts.WeatherController`; `Lighting.ColorCorrection` (Saturation **+0.28**, Contrast −0.04) plus `SunshineGrade` (+0.15), `RainbowGrade` (+0.22), `RainGrade` (−0.30, Brightness −0.06), `SnowGrade` (−0.25).
- **What's wrong:**
  - Rain and snow fall under the same 15:12 sun: Brightness 2.7, hard shadows, clear sky, no `Clouds`. The script only fades a grade, drops the emitters around the camera and plays the rain sound.
  - Each grade is applied on top of the base ColorCorrection, so Sunny comes to about +45% saturation and Rainbow about +55%. LihFolk's bright-cartoon preset is +15%.
  - Sunny and Rainbow are half the weather by weight (35 + 15).
- **Fix (medium, client only):**
  - Give each weather a look table: Lighting Brightness and ExposureCompensation, Atmosphere Density/Haze/Color, a `Workspace.Terrain.Clouds` Cover and Density.
  - Tween it with the grade WeatherController already tweens, and keep the base saved as attributes, the way the grades' look is saved now.
  - Rain: Brightness about 1.6, Clouds Cover 0.8. Snow: a cool haze. Sunny: as now.
  - Bring the base saturation down to about +0.15 so the grades have room.
  - Settings' Weather switch already turns all of it off.
- **Decisions:** Four weathers (2026-10-27); "A weather all the time" (2026-10-28); weather can be turned off in Settings (2026-10-29). No conflict: the look shows for everyone.

### 5. The west gate and both lane exits lead to invisible walls, and the town wall can be jumped (boundaries)

- **Where:** the gate opening (x 440, z −217…−183, 34 wide); the lane exits in the north wall (x 567–617) and south wall (x 663–713); `Village.Bound` ×4 (80 tall, x 410–898, z −410…10).
- **What's wrong:**
  - Through the open gate the road runs on 28 studs and stops dead on grass, where the invisible wall stands at its end (captures V5, V6).
  - The mountain ring's only gap is right behind the gate: the skyline is 0–3.5° there and 8–24° everywhere else.
  - Each lane exit leads to a 48 × 38 paving stub beside an outer house, then an invisible wall 38 studs out (V7).
  - The town wall's solid part stops at **y 6.6**. The cap and ridge above it (to 8.1) aren't solid, and a jump reaches 7.2, so a kid can hop the wall anywhere into the 28–36-stud strip outside.
- **Fix (small):**
  - Shut the gate: a pair of timber doors, or a bar and a guard post.
  - Wall up the two lane exits, or give them shut wicket gates.
  - Turn on `CanCollide` for the 7 `WallRidge` parts (top 7.85) so the wall holds.
  - Or take direction B below and give the gate somewhere to go.
- **Decisions:** "invisible boundary walls stay" (2026-10-21); block mountains with "the west still open" (2026-10-22). Yesterday's review item 6, still open.

### 6. The street, the lanes and the lots are one flat slab of sand (readability)

- **Where:** `Street.Road` (203/162/111), the two `Street.Paving` slabs (448 × 144, 193/162/122) and the six `Lots.Pad` (84 × 124, 178/145/101). All three are Ground with `PaintEarth` at 24 studs a tile.
- **What's wrong:**
  - In greyscale the road and the paving around it differ by **1%** (luminance 168.5 vs 166.7); the pads are 11% darker.
  - Only the 1-stud gutters, the 7.5-stud walkways and the stone centre strip mark where the 56-wide street ends. From any height the village reads as one sand-coloured car park (V1, V9).
  - LihFolk's readability check (paths separate from the ground in greyscale) fails.
- **Fix (small):**
  - Pick the street style. Earth versus stone is still open: `ROAD_STYLE` (2026-10-22, "earth is live until he picks"; Roadmap: "pick the street style").
  - Then give the off-street ground its own value, as the first simplified build had ("Lanes and the open ground inside the walls use the same flagstones, greyer"): grey flagstone lanes and open ground, or a darker packed earth if the street turns stone.
- **Decisions:** Earth street with a stone centre path, stone kept to compare (2026-10-22); The simplified map is the live map (2026-10-22).

### 7. Empty lots show a blank leaderboard, and a half-empty server is still (empty lots)

- **Where:** PlotService's empty copies (`Village.Lots.Empty<lot>`, lines 54–91); `LeaderboardService` (it draws only boards tagged `PlotLeaderboard`).
- **What's wrong:**
  - An empty copy strips every tag except `HidesRoof`, so its `Leaderboard` loses `PlotLeaderboard` and shows the template's "1. —" rows forever. In a two-player server that's four blank boards.
  - The copies also drop roughly 2,000 of the template's 2,941 instances (the locked TycoonItems), with no nameplate and no customers.
  - The street's only life is 5 villagers spread over 380 studs (`StreetLife.VILLAGERS`), one per 76 studs.
- **Fix:**
  - Small: keep the board's tag in the empty copies (`if tag ~= "HidesRoof" and tag ~= "PlotLeaderboard"`). Every board shows the same all-servers top ten.
  - Optional, small: one more villager per empty lot (5 + empty, up to 9). They're server-driven with no Animate script, about 15 parts each.
- **Decisions:** Unclaimed lots show the empty plot (2026-10-22); A leaderboard on every plot (2026-10-29). Both kept.

### 8. No landmark leads the eye: the torii is half the height of a shop (composition)

- **Where:** `Village.Landmarks`: the torii's top at y 17.0 (x 848); the gate ridge at 21.9 (x 440); the Upgraded Store's roof at 35 (PlotService's `NAMEPLATE_AT` note).
- **What's wrong:**
  - The street's two ends are smaller than the players' own shops. From the gate the torii covers about 2.4° of view, and about 3.6° from the street's middle. LihFolk asks a hero for 3–5°, at least 1.5× the height of anything around it, seen from the spawn and every gate.
  - Spawns face the back wall, so nothing tells a new player where the street, gate or shrine is.
- **Fix (medium):** one tall shared form both rows can see over their roofs. For example, a fire-watch tower (hinomi-yagura, about 45–55 studs) at the street's middle, or a bigger shrine gate with a stepped approach at the east end. This is built form, not nature.
- **Decisions:** "Village-wide events deferred" (2026-10-19) isn't touched. No generated nature.

### 9. A wide street with nothing in the middle (composition)

- **Where:** the road 430 × 56; fronts 72 apart; the empty ends (x 440–501 and 778–888, with the stalls only at the corners); four `Planter`s (N1, N2, S2, S3 walkways).
- **What's wrong:**
  - Between the shop fronts there's 56 studs of open earth. The width is Allen's choice and stays.
  - The planters are bare soil boxes: their trees were cleared with all the others on 2026-10-22.
  - The east end has 110 studs of open ground before the shrine.
- **Fix:** see direction A below: a middle square between N2 and S2, the first and fourth players' shops. For the planters, the shrine plaza and the end gaps, these are where Allen might place his own trees when he picks their look. No generated plants.
- **Decisions:** The street is wider (2026-10-21); No trees, shrubs or scattered rocks for now (2026-10-22); Roadmap "Trees back on the map in a look Allen picks".

### 10. Phones may lose the skyline: streaming and lighting priority (performance and look)

- **Where:** the Backdrop sits inside the `Village` Model (ModelStreamingMode Default); `Lighting.PrioritizeLightingQuality` = true (carried over from ShadowMap: `RBX_OriginalTechnologyOnFileLoad` = 3).
- **What's wrong:**
  - The mountains are ordinary parts 300–1,000 studs out. A phone that streams a smaller radius drops them, leaving a flat grass horizon like the one through the gate.
  - With quality priority on, the LihFolk vault notes a device that lowers quality "keeps advanced shadows … at the cost of view distance". For a phone-first game that is the wrong trade for the backdrop.
- **Fix (small):**
  - Put the 185 Backdrop blocks in their own Model set to `Persistent`. They're simple blocks and cheap.
  - On a phone, try `PrioritizeLightingQuality` off: it keeps view distance and drops shading quality first. Compare frame time and look.

### 11. Shadow casters that add cost and draw nothing (performance)

- **Where:** 205 flat Street parts (0.7 studs thick or less: centre stones, curbs, walkways, gutters); 93 of the 185 mountain blocks (300+ studs away, their shadows land outside the walls); the 4 invisible `Bound` walls.
- **Fix (small):** `CastShadow` off on all of them. The village casts 666 shadows in all; this removes 302.
- **Decisions:** none.

### 12. 24 lights in permanent daylight (performance)

- **Where:** 12 `Street.Andon` (Range 18), 4 stall chochin, 4 shrine lanterns and 4 house chochin, none shadowed. Each plot adds 19 more, so a full server has about 138.
- **What's wrong:** the clock is fixed at 15:12 with Brightness 2.7, so these pools barely show. The Neon heads carry the glow.
- **Fix (small, only if the phone profile shows light cost):** drop the 12 Andon PointLights first and keep the Neon.
- **Decisions:** the Roadmap item "Match the plot's shop lanterns to the village's (Chochin lights Range 13 / Brightness 1.4)" shows Allen wants those lanterns consistent, so ask first.

### 13. Lot N2's walkway is a different material (consistency)

- **Where:** `Village.Street.Walkway` at (640, 0.15, −233.8).
- **What's wrong:** it is `Brick` with the `PaintPlanks` variant, but that variant's base is WoodPlanks, so it can't apply. It draws Roblox's default brick, a pinkish strip in front of the shop (V11, V12). The other five lot walkways are Slate with `PaintStone`. Whoever claims N2 (always the first player) gets a different front from the rest.
- **Fix (small):** match the others, or, if planks were meant, set `WoodPlanks` + `PaintPlanks` on all six.

### 14. Rickshaw Bay 3 sits against a street lamp, on every lot (street furniture)

- **Where:** `Plot.Parking.Bay3` (slab x 616.75–626.25, z −224.6…−220.8 on N2) and `Street.LampFoot` (x 617.1–618.5, z −225.7…−224.3); the same layout repeats on every lot.
- **What's wrong:** the slab overlaps the lamp's foot by about 0.3 studs, and a parked rickshaw (3.7 × 6.7, not solid) reaches the post (V11).
- **Fix (small):** move the 12 lamps 3 studs toward the lot corners, or Bay 3 three studs inward.

### 15. Small style mismatches

- **Chochin:** the gate's and the stalls' chochin are flat Neon red (190, 52, 40) with SmoothPlastic caps and look like plastic up close (V6). A paper look would be warmer: a pale-orange Fabric or SmoothPlastic shell with only a small Neon core.
- **Torii and shrine:** these are SmoothPlastic among textured surroundings. The 2026-10-30 split says surroundings keep their textures and only the things players use are smooth; red-tinted `PaintWood` would match the gate.
- **Empty folders:** `Village.Atmosphere.Nature` and `Backdrop.Forest` are empty, left from the tree clear-out.

## Arrival, end to end

- **Spawn:** each lot's `PlayerSpawn` in the yard (plot space (0, 7.1)), facing away from the street toward the back wall. That is the right way for the tutorial: the ore roller's lever is about 10 studs ahead (V3). Finding 1 covers what happens before the claim.
- **First frame:** the yard and its stations, the back fence and town wall, and the mountains filling the upper quarter (finding 3). The street, gate and shrine are behind the player.
- **Finding your plot:** you spawn on it, and you respawn on it (`RespawnLocation`).
  - A claimed plot shows the owner's avatar and "<name>'s Plot" 42 studs over the shop (BillboardGui 30 × 15 studs, MaxDistance 300, not AlwaysOnTop), and the owner's name on the shop sign.
  - From the far end of the street (N1 to the shrine, about 310 studs) your own nameplate is just past its 300-stud range.
- **Walks** (Edit pathfinding, 16 studs/s, the template at N2):

| From → to | Studs | Seconds |
|---|---|---|
| Spawn → your shop's EntryPoint | 51 | 3.2 |
| Spawn → middle of the street | 92 | 5.8 |
| Spawn → gate | 233 | 14.6 |
| Spawn → shrine plaza | 247 | 15.4 |
| Gate → shrine along the street | 404 | 25.3 |
| Lot to lot along a row (centres) | 96.5 | 6.0 |

  Every walk is within LihFolk's under-15 s from a hub. There's nothing to do at the gate or the shrine, so few players will walk the street end to end.
- **Other plots from yours:** your neighbours' yards show through the 12.5-stud lanes and low fences (V7). The other row stands 72 studs across the street, 83 from door to door (V9). The rows read as separate shops with even gaps. With the template copies in N1 and N3 they read well; the street between them is the weak part (findings 6 and 9).

## The cut-off note: four directions for the map

Allen's line in `Refinements.md`, "Also thinking of having the map so that", is still cut off. I don't know how it ends. These are four directions it might take, for Allen to pick from or ignore:

| | Direction | What it is | Cost | Rulings it touches |
|---|---|---|---|---|
| A | **A middle square** | A stone island in the road between N2 and S2, the first and fourth players' shops: a small weather shrine where anyone buys weather for the whole server (the planned Robux/gem weather, as an in-world purchase spot like Allen's 2026-10-30 note asks for), plus one big all-servers top-ten board. Villagers and couriers route round it. | Medium: the island and shrine model, a prompt into the weather purchase once it's built, StreetLife's ±8 corridor and the couriers' lanes (z −208 / −192) moved round it. | Village-wide events deferred (2026-10-19): a square isn't an event system, but it's where one would go later. A leaderboard on every plot (2026-10-29). |
| B | **The road out** | Open the west gate onto a mountain road through the gap already in the ring. Couriers and rickshaws leave and come back through it (couriers already head for `GATE_X` 440). Add a signpost or toll gate, and move the invisible wall 150+ studs out. Also fixes finding 5. | Medium: a road, two cliff sides in Allen's block style, the moved Bound, and DeliveryService's `MAX_OUT` so every lot's courier reaches the gate (from N3 it fades halfway down the street today). | Block mountains, "the west still open" (2026-10-22). No generated nature: ask before adding any. |
| C | **A visible next tier** | A grander district seen from day one but shut, for example a terrace of master workshops behind the shrine, opened by a late upgrade or rebirth. | Large: a new area, its gating and a reason to go there. | GDD §11: the plot grows in place and freeform building isn't the direction. New scope. |
| D | **A tighter town** | Keep the plots and lanes; narrow the road (56 → about 40) and trim the bare ends (about 40 studs each side). Gate to shrine would be about 320 studs (20 s instead of 25). | Medium: move walls, gate, shrine, houses, stalls, lamps and bounds; `GATE_X` in DeliveryService (StreetLife reads the road's size). | Allen widened the street twice ("it seems very closed and tight", 2026-10-21; "separate the houses more", 2026-10-22), so probably not this one; listed for completeness. |

## Measurements

### Workspace counts

Measured at the start of the review. Instances include the child itself.

| Child | Instances | Parts | Lights | Scripts | Status |
|---|---|---|---|---|---|
| `Village` | 1,153 | 1,081 | 24 | 0 | live map |
| `Plot` | 2,942 | 2,058 | 19 | 0 | template; ServerStorage at runtime |
| `A2_Zones`, `A3_Compact`, `B_OneRoof`, `Z_B_Bands`, `Z_C_ForgeRing`, `Z_D_Court`, `Z_E_Line` | 13,153 | 9,777 | 113 | 0 | drafts at x 1,600–3,000 (2 unanchored parts and 2 sounds each) |
| x-2,000 copy (`Smithy`, `Shop`, `Parking`, `DeliveryBay`, `Fence`, `Workshop`, `Ground`, `Yard`, `CustomerSpawn`, `PlayerSpawn`) | 1,925 | 1,438 | 16 | 0 | unused (nearest lot 1,223 studs) |
| `Sword Animations` | 2,593 | 17 (unanchored) | 0 | 0 | the slash animation's source |
| `GreatSwordRig` | 1,579 | 22 (unanchored) | 0 | 2 Scripts, 1 LocalScript | third-party Tool on a dummy |
| `Bamboo1`–`12` (no 5), `Weapon Rack`, `Courtyard`, `AuxScene`, `ZanbatoPreview`, `Swordsmith`, `Lighting` folder, `MaterialDemo` | 284 | 99 | 1 | 0 | old prototype bits, most by the origin |
| `Baseplate`, `Terrain`, `Camera` | 3 | 1 | 0 | 0 | the baseplate is 2,048 × 2,048 grass (top y 0) under everything |
| **Total** | **23,632** | | | | 19,534 unused |

At runtime each claimed lot holds a copy of the template (2,942 instances) and each empty lot a stripped copy (roughly 900). A full server is about 18.8k instances of live map, about as much again as the leftovers.

### Distances from the lot centres to the leftovers (nearest part, studs)

- Rigs: 120 (N3) to 400 (S1).
- Origin bits: 463–1,012.
- `A3_Compact`: 819 (N3, S3), 916 (N2, S2), 1,012 (N1, S1).
- `A2_Zones`: 1,019 (N3, S3).
- Everything else: 1,223 or more.

### The village

- **Road:** 430 × 56 (x 410–840, z −228…−172), earth, with a stone centre strip (`RoadStyle`, 188 parts).
- **Lot fronts:** a 7.5-stud stone walkway and a 1-stud gutter in front of each lot.
- **Lots:** 84 × 124 earth pads, centres 96.5 apart, 12.5-stud lanes. North lots at z −284 (yaw 180), south at −116.
- **Walls:** x 440–888, z −372…−28. Solid to y 6.6; cap and ridge to 8.1, not solid. Gaps: the gate (34 wide) and the two lane exits (50 wide).
- **Invisible bounds:** 80 tall, x 410–898, z −410…10.
- **Landmarks:**
  - The gate (top 21.9) with sign 刀鍛冶の里 and one chochin.
  - The shrine plaza, 46 × 80 at x 840–886, with the torii (top 17.0), a hokora on a stone base and four stone lanterns.
- **Houses:** 4 end houses at the street's corners and 2 outer houses beside the lane exits, blue-violet roofs (the village keeps them; the shops are Autumn Terracotta, 2026-10-22).
- **Dressing:** 4 stalls, 4 crate stacks, 4 planters.
- **Backdrop skyline from the street's middle** (highest block top per 10° of azimuth): 8–24° all round except 250–290° (west, through the gate), which is 0–3.5°.
- **Sun:** from the west at 41.8° elevation, along the street. Both rows' fronts are side-lit equally (dot ±0.08), so neither row is in shade. Looking toward the gate you look into the sun.

### Lighting (Edit values)

- **Lighting:** ClockTime 15.2, Brightness 2.7, ExposureCompensation −0.05, Ambient 116/102/92, OutdoorAmbient 150/162/196, ColorShift_Top 255/226/190, GlobalShadows on, ShadowSoftness 0.6, LightingStyle Soft, PrioritizeLightingQuality on.
- **Atmosphere:** Density 0.32, Offset 0.22, Color 206/224/242, Decay 110/146/190, Glare 0.15, Haze 1.6.
- **Effects:** Bloom 0.5 / 40 / threshold 1.2; SunRays 0.06 / 0.3; ColorCorrection Brightness 0.03, Contrast −0.04, Saturation 0.28, Tint 255/248/238; DepthOfField off.
- **Sky:** `Stylized`, Allen's Toolbox sky. No Clouds.
- **Weather grades** (faded in by WeatherController):

| Grade | Brightness | Contrast | Saturation |
|---|---|---|---|
| Sunshine | +0.06 | +0.03 | +0.15 |
| Rain | −0.06 | +0.06 | −0.30 |
| Snow | +0.04 | −0.04 | −0.25 |
| Rainbow | +0.05 | +0.05 | +0.22 |

- **Weather effects:** rain at 220/s (about 175 drops alive), snow at 70/s (about 385 flakes alive) on an 80 × 80 emitter 22 studs over the camera; the rainbow is 6 beams 380 studs away. All fine for phones.

### Checked and fine

- **Z-fighting:** 542 visible block parts in Village show 0 real coplanar overlaps. The only hits are 4 wall-cap corner overlaps of 0.4 × 0.4 at the same height, and curb sides flush with paving edges that face into the road. Plot ground against village ground: 0.
- **No holes or falls:** the baseplate runs under everything and `FallenPartsDestroyHeight` is −500.
- **No closed pockets.** The narrowest walkable gaps are 4–4.5 studs: behind the shrine, and between the outer north house and the wall.
- **Houses are solid** to y 12 (a `Ground` block plus posts), so nobody falls inside one. Crates top out at 4.3, too low to reach a roof.
- Village decor is all anchored and has no scripts, prompts or emitters.

## Captures

Taken in Edit with the camera at these positions (camera → look-at). The images aren't in the vault; retake them the same way.

| Name | Shows | Camera → look-at |
|---|---|---|
| V1 | Overview, high (heavy blue haze) | (380, 300, 160) → (660, 0, −210) |
| V2 | Arrival view through the gate, looking east | (425, 8, −200) → (650, 6, −200) |
| V3 | A new player's first frame (N2 spawn, eye height) | (640, 9, −279) → (640, 4.5, −301) |
| V4 | The two rigs floating over the north mountains | (700, 40, −330) → (746, 85, −430) |
| V5 | Looking west at the gate and its flat horizon | (520, 9, −200) → (300, 4, −200) |
| V6 | Through the gate: the road ends on grass | (448, 8, −200) → (250, 5, −200) |
| V7 | The north lane exit, from the lane | (592, 8, −330) → (592, 4, −450) |
| V8 | Down the street to the shrine | (600, 9, −195) → (870, 6, −200) |
| V9 | The north row from across the street (temp copies on N1 and N3) | (640, 26, −140) → (640, 8, −260) |
| V10 | The shrine plaza | (805, 9, −200) → (885, 9, −200) |
| V11 | Rickshaw bays and the lamp | (628, 9, −207) → (622, 1.5, −225) |
| V12 | N2's brick walkway and the gutter | (592, 7, −224) → (600, 0.3, −234) |
| V13 | What a first joiner sees at the origin | (0, 9, 13) → (0, 4, −12) |

Two more captures were spoiled by another session's UI previews (`ShowDevelopmentGui` on) and dropped.

## Yesterday's map review: status

From [[Sessions/2026-10-30#Proposals and the map review]], in my area:
- Item 3, clear the drafts out of Workspace: **not done**. The count is unchanged at 23,632 (finding 2).
- Item 6, the west gate: **not done** (finding 5).

The other items are inside the plot.

## For Allen to test (Play; I didn't start it)

1. Publish to the private game. Join with one account and watch the first seconds: where do you stand before your yard appears, and for how long? Then join with a second account: does it appear in the first player's yard before jumping home? (Finding 1.)
2. In Studio Play, look north from N3's yard: GreatSwordRig and its name label should be lying behind the wall. (Finding 2.)
3. On a phone, cycle the weathers with the Dev Panel's Weather button. Do Sunny and Rainbow look oversaturated, and do Rain and Snow read as weather while the sun stays hard? (Finding 4.)
4. On a phone, from your spawn: how dark do the mountains look, and do they stay at the edge of the view? (Findings 3, 10.)
5. In Workspace's Properties, read the streaming radius values and `ModelStreamingBehavior`, and tell me.

Related: [[Design/Six Plots]] · [[Art/Town Street Redesign References#Simplified map built (2026-10-22)]] · [[Development/Code Map#Workspace and plot ownership]] · [[Design/Refinements Proposals — 2026-10-30]] · [[Sessions/2026-10-31]]

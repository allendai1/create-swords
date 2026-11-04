---
title: Handoff — Village fixes
type: handoff
updated: 2026-10-31
tags: [review, map, village, handoff, create-swords]
---

# Handoff — Village fixes (2026-10-31)

Builder agent's report for the fixes from [[Design/Reviews 2026-10-31/Map Review — Village]]. Everything was done in Edit, and Studio was never put in Play. The camera is back on Fixed and no compile-check modules are left over. The shared vault notes weren't touched.

## Done

### 1. Joiners spawn on the street, then go home (`ServerScriptService.PlotService`)
- **New:** `Workspace.Village.ArrivalSpawn`, a SpawnLocation at (640, 0.11, −200). It is 10 × 0.3 × 5.7, so its top is at 0.26, level with the centre stones. It faces −Z, toward lot N2.
  - Settings: Enabled, Neutral, Transparency 1, no decal, CanCollide/CanQuery/CanTouch off, CastShadow off, Duration 0, AllowTeamChangeOnTouch off.
- **`claim`:** sets `player.RespawnLocation = arrival` before its first yield (`waitLoaded`).
  - Every player has a RespawnLocation from the moment they join, so the engine never picks at random among the enabled, Neutral PlayerSpawns of other players' plots.
  - I didn't disable the plots' own spawns. A third-party write-up of the spawn rules says disabled spawns are dropped before RespawnLocation is checked, so disabling them would break respawning at home.
- **Going home after the claim:** RespawnLocation becomes the plot's PlayerSpawn as before. In a separate thread, the server calls `RequestStreamAroundAsync(spawn.Position, 5)` (pcall'd), then `PivotTo`.
  - The pivot is skipped if the character changed or the plot is gone.
  - The claim isn't delayed: the `Plot` attribute and hooks are set at the same time as before.
- **`CharacterAutoLoads`:** unchanged (true), so every respawn path behaves as before.
- **Spawn flow, traced in code:**
  - **First joiner:** spawns at ArrivalSpawn on the street. Once the save loads (about 1–2 s), N2 is claimed; the server streams the yard in, then moves them to N2's spawn.
  - **Second joiner:** same as the first, on the street (never in N2's yard), then moved to N1.
  - **Rejoin with the save still locked:** waits on the street for up to about 30 s, then goes home.
  - **Respawn after death:** at their own PlayerSpawn (RespawnLocation).
  - **Studio Reset progress:** release, then claim (the street spawn first, then the new plot's spawn, with no yield in between), then `LoadCharacter` at the new plot. The streaming thread sees a new character and skips its pivot.
  - **7th player (no free lot):** always spawns at ArrivalSpawn.
- **Compile:** compiles in the wrapper. New locals (`arrival` line 47, `character`, `home`) are declared before their first use.

### 2. Workspace clutter moved to `ServerStorage.Legacy.WorkspaceDrafts_2026_10_31`
- **Moved (20 items):** each kept its name and has the attribute `FromWorkspace = true`.
  - The seven drafts: A2_Zones, A3_Compact, B_OneRoof, Z_B_Bands, Z_C_ForgeRing, Z_D_Court, Z_E_Line.
  - The x-2000 copy: Shop, Workshop, Yard, Fence, DeliveryBay, Parking, PlayerSpawn, CustomerSpawn and **Ground**. Ground is that copy's 180 × 220 slab at x 1910–2090; the world's ground is Baseplate (2048², grass, top y 0). Both spawns were inside the copy's footprint.
  - GreatSwordRig and Sword Animations. **Allen drags these back into Workspace to edit animations.** This also ends the `Animations is not a valid member of Tool` error, because Scripts in ServerStorage don't run.
  - The empty folders `Village.Atmosphere.Nature` and `Backdrop.Forest`. They also carry `FromPath`.
- **Left in Workspace:** `Smithy` (the x-2000 copy's, 1,139 instances). `ReplicatedStorage.Shared.BladeProbe:60` looks up `Workspace:FindFirstChild("Smithy")`. The probe only runs for testing and falls back to a stand-in anvil, but the rule was to leave anything still referenced. It can join the rest if the probe isn't needed.
- **Counts:** Workspace descendants went from 23,789 to 5,702 (25,073 at the start, while the roof agent's temp copies were still there). The folder holds 18,113 instances.
- **Other references the grep found:** `ServerStorage.AnvilController_Backup` (dormant), `SwordSlash` (comments only), and `build_outside_layouts` (a builder that makes new Z_* drafts if rerun).
  - `build_decor:95` reads `workspace.Courtyard`, so Courtyard must stay.
- **Left for Allen to decide:**

| Item | Contents |
|---|---|
| `Bamboo1`–`12` (no 5) | 6 instances each, near the origin |
| `Swordsmith` | 79 instances; an R6 NPC in N2's yard at (674, 3, −276) |
| `Weapon Rack` | 105 instances at (−49, 3, −687) |
| `ZanbatoPreview` | 10 instances at y 304 |
| `MaterialDemo` | empty folder |
| `Courtyard` | 7 instances: lanterns, one light |
| `AuxScene` | 11 instances, unanchored, at (81, 57, −81) |
| `Workspace.Lighting` folder | 4 dead effects |

### 3. Atmosphere (`Lighting.Atmosphere`)
- **Changed:**
  - Haze 1.6 → 0.7
  - Decay 110/146/190 → 178/160/150
  - Color 206/224/242 → 216/222/230
  - Density and Offset unchanged.
- **Mountain colour:** I also lifted the 137 `Grass` mountain blocks' colours (R×1.3, G×1.22, B×1.15; e.g. 74/110/54 → 96/134/62). Each block's old colour is kept in its `ColorBefore_20261031` attribute. Rock and Cap blocks are unchanged.
- **Result in the spawn capture: only slightly lighter.** The near mountains are still darkish teal. Their faces toward the yard are in shade, so the bluish OutdoorAmbient (150/162/196) colours them more than the haze does. A real fix means warming OutdoorAmbient, which changes the whole scene: Allen's call.

### 4. Weather light (`StarterPlayerScripts.WeatherController`)
- **Each weather now has its own light,** faded with its grade over the existing 3 s FADE:
  - Lighting Brightness, Ambient and OutdoorAmbient
  - Atmosphere Density, Haze and Color
  - `Terrain.Clouds` Cover, Density and Color

| Weather | Look |
|---|---|
| Sunny | Studio's base values |
| Rainbow | Brightness 2.9 |
| Rain | Brightness 1.6, Ambient 100/100/108, OutdoorAmbient 128/134/150, Density 0.42, Haze 2, Color 186/192/204, Clouds Cover 0.82 / Density 0.6 / 196/202/212 |
| Snow | Brightness 2.1, Ambient 118/122/136, OutdoorAmbient 170/180/204, Density 0.4, Haze 1.4, Color 224/232/246, Clouds Cover 0.7 / Density 0.4 / 240/244/250 |

- **Base values:** kept as `Base<Property>` attributes on each object the first time the script runs. A Dev Panel re-run reads them back from the attributes.
- **First update:** `drawn` now starts as `false`, so the first `update()` always fades to the right look, including back to the base when the Weather switch is off.
- **Unchanged:** the grades' Look* attributes, the rain volume's BaseVolume, and the indoor particle/sound stop.
- **New:** `Workspace.Terrain.Clouds`, Cover 0 (the sunny base), Density 0.3, white. The script waits up to 5 s for it.
- **Saturation:**
  - Base `ColorCorrection.Saturation` 0.28 → 0.15
  - `SunshineGrade.Saturation` 0.15 → 0.08
  - `RainbowGrade.Saturation` 0.22 → 0.12
  - Totals: Sunny 0.43 → 0.23, Rainbow 0.50 → 0.27, Rain −0.15, Snow −0.10.
- `ServerScriptService.Weather` is unchanged; it doesn't need anything for this.
- **Compile:** compiles in the wrapper. LIGHT, lit and base are declared before `update`.

### 5. Gate, lane exits and the wall top
- **Gate:** `Village.Landmarks.GateDoors` (7 parts).
  - Two timber leaves, 0.8 × 12.54 × 14.88 each, Wood PaintWoodDark 88/56/34, solid, from y 0.16 to 12.7, on the posts' outer half (x 438.1–438.9).
  - On the village side: two iron straps (Metal 52/50/52), a bar (PaintWoodDark 70/42/26) and two brackets, all decor.
  - Everything is clear of the chochin.
- **Lane exits:** `Village.Walls.LaneExitN` (x 591.75, z −372) and `LaneExitS` (x 688.25, z −28). Each is a copy of the town wall's WallBase, Wall, WallCap and WallRidge, built between the exit's pillars.
- **Wall top:** `Village.Walls.WallGuards`, six invisible parts: CanCollide on; CanQuery, CanTouch and CastShadow off.
  - Five sit over the wall lines, 2.6 thick, from y 6.6 to 24.
  - One sits over the gate, from y 12.7 to 24.
  - Nothing near the walls is tall enough to get over them: the tallest climbable parts are 12–12.6 tall.
- **WallRidge:** left non-solid. The guards replace that idea.

### 6. Empty lots keep their leaderboard (`PlotService`)
- The empty copies keep the `PlotLeaderboard` tag, so their boards show the all-servers top ten.
- When an empty copy comes back after a player leaves, its board can show the old list for up to 2 minutes, until the next refresh.

### 7. Mountains stay on phones
- `Village.Atmosphere.Backdrop.Mountains` was a Folder. It's now a Model with the same name and `ModelStreamingMode = Persistent`: 185 parts, no other instances.
- `PrioritizeLightingQuality` is unchanged (on). Allen should compare it off on a phone.

### 8. Shadows off
- `CastShadow` turned off on 290 parts; the village now has 379 shadow casters (669 before):
  - 193 flat Street parts at ground level: Water, RoadStone, Road, Paving, Walkway, Curb, GutterBridge
  - 93 mountain blocks (none of their shadows reached the town)
  - the 4 Bound walls
- The 12 LampCaps keep their shadows: they're raised, so their shadows show.

### 9. N2's walkway
- `Village.Street.Walkway` at (640, −233.75): Brick/PaintPlanks → Slate/PaintStone, like the other five.

### 10. Street lamps
- All 12 lamps (LampFoot, LampPost, LampCap and Andon: 48 parts) moved 3 studs along x, away from their lot's centre.
  - Each part's old x is in its `MovedFromX` attribute.
  - N2's lamps went from x 617.75 / 662.25 to 614.75 / 665.25.
- **Check:** the nearest Parking part on any of the six lots, with the template laid onto each lot, is now 1.30 studs from a lamp foot. Nothing overlaps them but the road.

### 11. Style
- **Neon chochin:**
  - The gate's chochin and the red house chochin (EndN1, OuterS): Neon 190/52/40 → SmoothPlastic 198/37/23, as the plot's lanterns are built.
  - EndS1's cream chochin: Neon → SmoothPlastic, colour kept.
  - Lights unchanged (Allen's open lantern-light item).
  - **The four stall chochin already matched** the plot's lanterns (SmoothPlastic 198/37/23), so they're unchanged.
- **Torii:** SmoothPlastic → Wood. The red parts use PaintWood, as the shrine's posts do; KasagiTop and the two ToriiFoot use PaintWoodDark. Colours unchanged.

### Extras from the coordinator
- **Nameplate:** `NAMEPLATE_AT` (0, 42, −33) → (0, 47, −33).
- **"The plot next to me has this shop setup":** this isn't PlotService. In Edit I copied the template the way PlotService makes an empty plot: no Upgraded Store, nothing above y 22. The two-storey shop beside Allen was the roof agent's `_RoofCapTmp_Upgraded` on N3, which stood in Workspace during his playtest. It's gone now.

## Checks
- **Compile:** PlotService and WeatherController both compile.
- **Coplanar check** over the 63 parts I built or moved: 14 hits. All are bottom faces at ground level (doors, WallBase, pillar bases) or ends buried inside the posts or pillars. None can be seen, so there's no visible Z-fighting.
- **Overlaps:** the new parts only meet the parts they're meant to join.
- **Captures:**
  - Before: spawn, the gate from inside, the street to the shrine, and the overview.
  - After: spawn and street.
  - **Not taken after:** the gate and the overview. The capture tool failed with "target not reachable", and for about 10 minutes a UI reviewer's preview ScreenGuis covered the screen (`StarterGui.UIFX_P`, `STN_P_*`, `SET_P_A`, not mine).
  - Retake them: the gate from (500, 10, −190) looking at (430, 7, −200); the overview from (380, 300, 160) looking at (660, 0, −210).

## Not done or open
- Proposals not built, as briefed: finding 6 (street style), 8 (landmark), 9 (the four directions) and 12 (lights).
- **`Smithy`** is still in Workspace (BladeProbe references it).
- **Mountain colour:** whether the mountains look light enough is Allen's call. The next lever is OutdoorAmbient.
- **For Allen:** read the streaming radius values off Workspace's Properties.

## What to test in Play
1. **Join:** you appear on the street in front of N2, then within a second or two you're moved to your yard. With 2 players (Test → Clients and Servers), the second never appears in the first player's yard.
2. **Respawn:** reset your character and you come back in your own yard. Use the Dev Panel's Reset progress and you get a new plot, spawning in its yard.
3. **Nameplate:** with the Upgraded Store bought, the nameplate floats clear above the roof.
4. **Empty lots:** their leaderboards show names, not "1. ---", after about 15 s.
5. **Weather:** cycle it with the Dev Panel's Weather button.
   - Rain dims the light, with grey haze and clouds rolling in over about 3 s; Snow is cool and bright with clouds; Sunny and Rainbow are less saturated than before.
   - With Settings → Weather off, it goes back to the base look.
   - Inside a shop, rain and snow still stop.
6. **Walls:** try to jump the town wall anywhere and climb the gate. You shouldn't get out. Check the gate doors and the two walled-up lane exits from the street and the lanes.
7. **Phone:** the mountains stay on the horizon. Compare `PrioritizeLightingQuality` on and off.
8. **Lamps:** a rickshaw in Bay 3 no longer touches the lamp. N2's walkway is stone.

---
title: Map Review — Yard and Smithy
type: review
updated: 2026-10-31
tags: [review, map, yard, smithy, pads, prompts, labels, paving, lighting, create-swords]
---

# Map Review — Yard and Smithy (2026-10-31)

Read-only review of everything in `Workspace.Plot` outside the shop building: `Smithy` (ore roller, furnaces, anvils and hearths, polishing and etching stations, racks), `Grounds`, `Fence`, `Workshop` (the shop's back wall and back door), `Pads`, the delivery corner, the spawn and the yard's lighting. Part of the big review in [[Sessions/2026-10-31#Refinements, Allen's new notes and the big review (evening)]]. The shop and the bay are in [[Design/Reviews 2026-10-31/Map Review — Shop and Street]], everything outside the plot in [[Design/Reviews 2026-10-31/Map Review — Village]].

**How it was measured.** Studio in Edit; nothing played, nothing moved or changed except the Edit camera (set back to Fixed after the captures). Skills: roblox-collaboration-mode, lihfolk-worldbuilding, roblox-building, roblox-lighting. Every suggestion was checked against the [[Design/Decisions Log]].
- **Coordinates** are plot-local. For lot N2 (the template's): world = (640 − x, 0.5 + y, −284 − z). Plot −z is the street, +z the back fence. Seen from the spawn facing the yard, −x (furnaces, ingot racks) is on your right and +x (polishing, etching, the bay) on your left. The yard paving's top is plot y −0.26; heights below are above the paving unless they say "plot y".
- **Starter or bought** comes from the `TycoonItem` tags and `Upgrade` attributes. Edit shows every bought item at once (and the Upgraded Store over the starter strip), so the captures show a full yard.
- **Walks:** Edit pathfinding (agent radius 2, height 5) at 16 studs/s (Swift Boots 20). Locked items are solid in Edit but not at runtime, so a few legs may be a few studs shorter in Play.
- **Prompts:** reach measured from the character's root (2.74 plot y, 3 above the paving) to each prompt's part, as Roblox does.
- **Labels on a phone:** projected for an 844 × 390 screen, FOV 70°, Roblox's default camera 12.5 studs behind the head and 20° down, and zoomed out to 20 studs. Sizes from the `WorldText` templates (pad label 260 × 64, Buy button 260 × 120, prompt square 60 × 60, ore label 200 × 54, all fixed pixel sizes). Billboards don't draw in Edit captures, so these are geometry, not screenshots: check them in Play on a phone.
- **Contrast:** WCAG luminance from the parts' colours (not sampled under the game's lighting).
- **Z-fighting:** `ServerStorage.Builders.coplanar_check` (a fresh clone) over 326 Parts and wedges, plus the 270 bevelled station meshes treated as boxes.

![[Design/Reviews 2026-10-31/Yard and Smithy/yard-from-spawn.jpg]]
*From the spawn at eye height, everything bought (Edit). Taken before the World Store items went in.*

## Findings, most valuable first

### 1. The Ore Slot / Merge pad stands in the gap between the lever and the stands

- **Where:** `Plot.Pads.OreStand2`–`OreStand6` and `MergeSlots`, all on one spot at (−4.9, 18.6), label 1.6 over the pad (`LabelHeight`). `Smithy.OreRoller.Lever` spans z 13.4–16.9; the front row of stands starts at z 22.44.
- **What's wrong:** when the lever moved 3 studs back yesterday ([[Sessions/2026-10-30#Pads]]: "so i dont accidentally click an ore when i want to roll"), its pads stayed. They were beside the lever; now they're in the 5.5-stud gap between the lever and the stands, on the walk from the lever to the left-hand stands.
- **Evidence:**
  - Edit pathfinding from the lever (0.6, 11.4) to collect Stand 1 crosses the pad's green top with 2 waypoints; to Stand 1's or Stand 4's side, 3.
  - Standing on it to collect Stand 1, its Buy button (260 × 120) covers 82–96% of Stand 1's Collect square on a phone (2,948 / 3,452 of 3,600 pt² at the default and the zoomed-out camera). A tap meant for Collect can land on Buy.
  - From the lever, its label covers 76–77% of the Roll square (2,774 / 2,736 of 3,600 pt²).
  - It stands nearly all game: Ore Slot 2 (75) is one of the five pads on a new plot, then Slots 3–6 (280 → 20,000), then Merge, then Slot 2 again.
- **Fix (small):** move the six markers to clear floor left of the lever, about **(−9, 9)**. Checked there: the label doesn't touch the Roll square at either zoom and stays on screen; the pad's edge is 7.4 studs from the spawn→lever line, 7.9 from the lever→Stand 1 path, 6.3–6.7 from the back door's paths to the lever and to Furnace 1, and 2.0 from the later lever→Ingot Rack 2 line. (−9.5, 12) was tried first and sits on that last line.
- **Rulings:** finishes Allen's 2026-10-30 lever move. The pads' spot beside the roller was Claude's (2026-10-28 "Pads moved and turned with their stations"), not a ruling.

### 2. The starter yard is 98% bare gravel (yesterday's suggestion 5, still open)

- **Where:** `Plot.Grounds.Paving`, `PavingSide` and `PavingStrip`, 7,020 sq studs.
- **What's wrong:** a new player sees the lever and one stand, Furnace 1, Anvil 1 on its hearth, the leaderboard and four green pads. Everything they'll build is hidden until bought, so nothing on the floor says "a smithy with room to grow": the three empty anvil bays, two empty furnace bays and the whole finishing side are plain gravel.
- **Evidence:**
  - Footprint of what's visible at the start (0.5-stud raster of the visible station parts): **159 sq studs, 2.3%** of the paving; with everything bought, 899 (12.8%).
  - From the spawn: lever 4–17 studs, Furnace 1 45 (6.8 tall, 8.6° of view), Anvil 1 62 (3.8 tall, 3.5°: LihFolk calls under ~2° a speck on a phone), the leaderboard 76 (11.5 tall, the tallest thing in the yard, as big in view as Furnace 1), the pads 13 / 31 / 43 / 52.
  - Only Ore Slot 2's label shows from the lever (labels show within 22 studs).
- **Fix, three options (Allen's pick):**
  - **(a) Faint previews of what's on offer (small, recommended):** `TycoonController.shade` (line 39) hides every locked item with `LocalTransparencyModifier` 1. Items whose pad stands (3–5 at a time, after the pad cap) could show at about 0.85 instead, so each pad has a faint station behind it. The build-in animation (line 84 onward) then starts from the faint copy. The items are already non-solid and their prompts off while locked (`TycoonService.setLocked`).
  - **(b) Plinths:** each crew anvil's charcoal `Hearth` slab (11.75 × 8.59, 0.6 high) and a slab under each furnace bay, always shown, the pad on it. This splits the slab out of each `TycoonItem` model.
  - **(c) Stalls:** the four finishing `StandingFrame`s (posts, beam, sign, prop swords; 10.2 tall) standing from the start as empty stalls, the bench appearing on purchase. That shows the reward (polished and etched swords) where you'll buy it (Allen 2026-10-30: "players are more likely to buy something they can see in the game"). Medium: split from the station models.
- **Rulings:** (b) changes 2026-10-29 "Anvils 2-4 on hearths … inside the anvil model, so it comes with the purchase" ([[Design/Decisions Log]] line 917). (a) has a precedent in 2026-10-20 "Buying wall holders … prompt plus a see-through preview" (line 163). No nature props (lines 272–273).

### 3. The heat pads stand in each furnace's approach lane

- **Where:** `Pads.Heat1`–`3` (−26.1, 40), `F2Heat1`–`3` (−26.1, 48), `F3Heat1`–`3` (−26.1, 56), 3 studs off each furnace's mouth (the furnaces' fronts are at x −30.89).
- **What's wrong:** the Heat prompt reaches 9.75 studs from the furnace base, so it appears as you reach x ≈ −23.4, right at the pad. You walk over the pad going in and often stand on it.
- **Evidence (phone):**
  - On the pad facing the furnace, its Buy button covers **92–100%** of the Heat square (3,320 / 3,600 of 3,600 pt²).
  - Next to it, the pad's label covers 72–77% of the Heat square and 64–85% of your own character.
  - Nine upgrades over hours use these three spots: Heat 580 → 5,200, Furnace 2 heating 1,800 → 15,600, Furnace 3 heating 7,000 → 62,000.
  - The same pattern on a smaller scale: the **Crafter** pad (−4.3, 59.5) is 2 studs in front of Anvil 2's hearth. On it you're 6.85 studs from Anvil 2's Forge prompt (reach 8), and its Buy button covers 48–72% of the Forge square.
- **Fix (small):** move the nine heat markers out of the lanes, half a bay toward the yard's front and 1 stud further out: about **(−25, 36)**, **(−25, 44)**, **(−25, 52)**. That's between the lanes, and the edges stay 2–3 studs off the walk from Ingot Rack 1 to Furnace 1. `Furnace2` / `Furnace3`'s own pads can stay, since they stand before their furnace does. A label can still cross the screen's middle from a zoomed-out camera (the label is 31% of a phone's width); the Buy-button clash is what this removes. Crafter pad: 2 studs further out, about (−4.3, 57.5).
- **Rulings:** none. "Pads on the spot their furnace's pad stood" (2026-10-29) was Claude's placement.

### 4. Pads and furnaces have almost no value contrast with the gravel

- **Where:** `ReplicatedStorage.PadParts` (`Base` 205,205,210; `Top` 40,215,60); `Grounds.Paving` (Pebble, 178,171,159, luminance 0.41).
- **What's wrong:** the pads, the main "next goal" for a new player, stand apart from the near-white gravel only by hue. In greyscale, for red-green colour-blind kids, or on a phone in sunlight, they sink into the floor. LihFolk asks gameplay objects for ≥ 3:1 against their background.
- **Evidence:**

| Against the gravel | Contrast |
|---|---|
| Pad top (green) | 1.18 : 1 |
| Pad base (light grey) | 1.44 : 1 |
| Furnace body | 1.11 : 1 |
| Ore stand tops | 1.75 : 1 |
| Lever base (sage) | 1.68 : 1 |
| Ingot racks | 2.87 : 1 |
| Anvil hearths (charcoal) | 5.24 : 1 |
| Etching / polishing wood | 6.30 : 1 |

- **Fix (small):** darken `PadParts.Base` to the hearths' charcoal (58,54,54). The ring round the green top then reads 5.2:1 on the gravel and still about 2.4:1 on a darker floor. One template part, every pad. The other option is a darker gravel (a mid stone like 120,110,98 gives the pads 2.6–3.2:1 but drops the dark stations to about 2–3:1); since the Pebble is Allen's own change, the pad base is the smaller step.
- **Rulings:** 2026-10-30 "Textured surroundings, smooth stations" (line 1093). The pad's grey base and green top follow Allen's "upgrade buy button" reference, so the base colour is his call.

### 5. The ore labels pile up again, on a phone and in two rows

- **Where:** `ReplicatedStorage.WorldText.OreLabel` (200 × 54 px, name 28 pt over rarity 20 pt, `AlwaysOnTop`, bottom 0.6 over the ingot), cloned onto each stand by `ForgeService` (line 466). The stands are 4.3 studs apart, two rows 4.7 apart at the same height.
- **What's wrong:** with fixed pixel sizes, six labels over stands 4.3 studs apart can't fit side by side from where you pull the lever.
- **Evidence:**
  - **Phone,** from the lever at the default camera: label anchors are 42–48 pt apart, and the back row only 8 pt above the front. Common names are 50–127 pt wide at 28 pt ("Iron" 50, "Copper" 90, "Black Iron" 127; the longest metal, "Rainbow Alloy", 176), so from three slots up the names overlap. From four up, the back row's labels sit on the front row's.
  - **Desktop (1080p):** anchors are 136 px apart, fine side by side. But the rows are 23 px apart vertically, so the back row's rarity line lands on the front row's name.
- **History:** the overlap was fixed once with labels sized in the world (2026-10-24, line 512: "the button text is overlapping as well as the rest of the texts on the ingots"). It came back with the steady pixel size (2026-10-28, line 874: "the ores text look small sometimes"), the back row lowered to the front row's height (2026-10-29) and the labels growing to 200 × 54.
- **Fix (small; Allen's pick):**
  - name only, the rarity shown by the name's colour (one 30-pt line, and the rows stop colliding on desktop);
  - or no label on a Common unless an open letter wants it (60% of rolls);
  - or a world-sized label again, with a `UITextSizeConstraint` floor so it never gets too small.
  
  Staggering the rows is out (2026-10-26, line 582: "each back stand directly behind a front one"). Check it in Play on a phone with all six slots first.

### 6. The strip behind the shop is a different paving from the yard

- **Where:** `Grounds.PavingStrip` (x −24…24, z −18…−6) is Slate with `PaintFloor1Soft`; `Grounds.Paving` and both `PavingSide`s are Pebble.
- **What's wrong:** a 48 × 12 band of soft square flags runs between the back door and the gravel, with a hard straight seam at z −6. You cross it on every trip between the shop and the yard, and the spawn is 10 studs past it. It stays until the Upgraded Store's floor replaces it (`UntilUpgrade`).
- **Evidence:** ![[Design/Reviews 2026-10-31/Yard and Smithy/yard-back-door-seam.jpg]] Both `PavingSide`s still carry `PaintFloor1Soft`, a Slate variant that does nothing on Pebble.
- **Fix (small):** Pebble on `PavingStrip` too (and clear the dead variant on both sides), or everything back to `PaintFloor1Soft`.
- **Rulings:** 2026-10-30 (line 1093) records `PaintFloor1Soft` as the yard paving. Allen switched the main paving to Pebble afterwards ([[Sessions/2026-10-30#The rest of the yard's stations smooth]]: "Seen"). The record needs his choice.

### 7. The World Store spots by the roller show a second prompt (being built)

- **Where:** `Plot.WorldStore.AutoRoller` (motor at x 4.6–7.3, z 13.9–16.4, beside the lever; prompt at (5.8, 3.4, 15.1), reach 6) and `WorldStore.LuckyOre` (case at (12, 26.4); prompt reach 6). Both prompts are `OnePerButton`, key E, no hold.
- **What's wrong:** the yard's station prompts are `OneGlobally` so only one shows at a time ([[Sessions/2026-10-28]] line 189: "on touch, prompts with the same key all show"). The Buy prompts are in a different exclusivity group, so in their reach a Buy square shows next to Roll or Collect.
- **Evidence (standable ground where both reach):**
  - Auto Roller's Buy: 43.5 sq studs with Roll, 33.5 with Collect 3.
  - Lucky Ore's Buy: 38.8 with Collect 3, 38.5 with Collect 6 (the right-hand stands' collecting side).
  - From the lever's usual spot (0.6, 11.4) the Auto Roller's prompt is about 6.4 studs away, just out of reach.
- **Fix (small, for the builder):** `Exclusivity` OneGlobally on the World Store prompts, so the nearest prompt wins as everywhere else in the yard. Moving the case doesn't help much: its reach only clears the stands' Collect reach about 14 studs from the pedestals (x ≈ 19), too far from the stands to read as theirs. Otherwise the spots are well placed: neither blocks the lever's front or a stand.

### 8. The two blueprint pads stand 4.5 studs apart

- **Where:** the next-sword pad at (−21, 55) and the big-sword pad (Zanbatō → Claymore → Flamberge) at (−16.5, 55), both in front of Anvil 1. Blueprints always stand (`TycoonService.standing`, lines 65–83).
- **What's wrong:** from the Zanbatō on (after the Gladius and the Big Sword Stand), both stand for the rest of the game, side by side.
- **Evidence:**
  - In a cheapest-first buying order, both stand from the 60th purchase of 80.
  - Their labels overlap 29% at Anvil 1 (66% zoomed out) and 77–85% walking up from the furnaces or the yard.
  - Furnace 3 / its heating pad (−26.1, 56) is 5.2 studs from the sword pad: 18–55% at the anvil, 72–81% walking up.
- **Fix (small):** the big-sword pad to about (−12.5, 55), between Anvil 1 and Anvil 2: 0% at the anvil, 36% zoomed out, 58–71% walking up. On a phone any two pad labels within ~20 studs of each other overlap from a distance (each is 31% of the screen's width), so the rest belongs to the label's phone size (the UI reviewers').
- **Rulings:** 2026-10-30 "The swords are one chain by value … The big swords have their own pad" (line 1114). This moves the pad, not the chain.

### 9. Z-fighting on the station sign frames

- **Where:** `StandingFrame` of `EtchingTable`, `EtchingTable2`, `PolishStation`, `PolishStation2`.
- **What's wrong:** each frame's two posts end flush with the beam's top (both at 10.19), so 8 pairs of 0.5 × 0.5 top faces share a plane. That flickers from any raised camera.
- **Evidence:**
  - The coplanar check found **20 hits**: the 8 post tops; 4 Post/Backboard slivers 0.02 wide on the two etching frames (edge contact, likely invisible); and the delivery cart's 8 Bed/Side/End pairs, known since 2026-10-28.
  - The 270 bevelled station meshes, treated as boxes (overlap over 0.15): 0 hits.
  - The ground layers are clean: the lawn and the bay ground are 0.04 under the paving where they meet, and the paving pieces only touch edge to edge.
- **Fix (small):** take 0.04 off each post's top (8 parts). The cart's are in the bay (Shop and Street's area).

### 10. Etching Table 2 is not a copy of Etching Table 1

- **Where:** `Smithy.EtchingTable` (frame centre (39.97, 23.18)) and `Smithy.EtchingTable2` ((39.83, 9.16)), 13 studs apart on the same line, facing the same way.
- **What's wrong:** Allen's rule is that a second copy matches the first. Polishing Stations 1–2, Furnaces 1–3, Anvils 2–4 and the Sword Racks match part for part; the etching tables don't.
- **Evidence:**
  - Frame 6.50 wide against 7.94 (backboard 5.24 against 6.68).
  - The frame is set 0.75 off the worktop's centre (along the table) against 1.51.
  - Different prop swords and no demo sword: 102 visible parts against 104, of which 76–78 sit somewhere else relative to the worktop.
- **Fix (small):** rebuild Etching Table 2 as a clone of Etching Table 1 at its spot (keeping its own prop swords if wanted).

### 11. Anvil blocks: three wood grain, one smooth

- **Where:** `Model3D.WoodBase` under each anvil.
- **What's wrong:** Anvils 1–3's blocks are Wood + `PaintFurniture`, the last textured wood on any station since the smooth pass. Anvil 4's is SmoothPlastic (Allen's, [[Sessions/2026-10-29#Ore stands in two rows; smooth anvil bases]]).
- **Also:** the four hearths and Anvil 4's block carry `PaintFurniture` on SmoothPlastic, which does nothing.
- **Fix (small):** SmoothPlastic on Anvils 1–3's blocks, keeping their colour, to match Anvil 4 and the smooth-stations decision (line 1093). Or Anvil 4 back to wood if the grain was meant.

### 12. The Stocker and Sword Rack pads share one spot

- **Where:** `Pads.SwordRack` and `Pads.Stocker`, both at (18.5, −9.5).
- **What's wrong:** the two have independent gates: the Sword Rack is 280 after nothing, the Stocker 36,000 after the Sword Crafter. A player who hasn't bought the Sword Rack by the time of the Crafter gets two pads in one place, their labels exactly on top of each other. Rare, since the Sword Rack is cheap and sits in the 3 cheapest.
- **Fix (small):** the Stocker's marker 5 studs aside, e.g., (23.5, −9.5) (it moves back with the wall like the other two), or gate the Stocker on the Sword Rack, which it works from.
- **Rulings:** 2026-10-30 "Stocker after the Sword Crafter only" (line 1118). Gating on the Sword Rack isn't a sword upgrade, but ask.

### 13. The spawn is an invisible 0.32-stud step

- **Where:** `Plot.PlayerSpawn` (10 × 0.3 × 5.7, Transparency 1, CanCollide on), x −5…5, z 4.3…10.
- **What's wrong:** its top is 0.32 over the paving, so a new player stands visibly in the air on their first frame, and the edge is an invisible step in front of the lever.
- **Fix (small):** CanCollide off (spawning still works), or sink it so its top is at the paving. How players arrive is in Village #1.

### 14. Bare lot ground beside the bay

- **Where:** x 40.9–44, z −46…−18, between the bay's ground (`DeliveryBay.Yard`, ends at x 40.9) and the fence (x 44). The yard's lawn starts only at z −18.
- **What's wrong:** no plot ground covers this 3 × 28 strip, so the village lot's plain `Ground` (plot y −0.34) shows, unlike the bay's `PaintEarth` beside it. The three crates stand on it.
- **Fix (small):** widen `DeliveryBay.Yard` by 3.1 studs (top still −0.30, under the paving where they meet).

### 15. The record is behind the map

For the main session (I didn't edit other notes):
- The Decisions Log (line 933) puts the leaderboard "on the lawn left of the shop facing the street". It stands at (35.5, 74), the yard's back corner, facing the yard: Allen moved it. It's the tallest thing in the yard (11.5) and pulls the eye there from the spawn; fine if that's the intent.
- Line 1093 says the yard paving is `PaintFloor1Soft`; it's Pebble (finding 6).
- `Plot.Yard` holds only the street `Bridge`, and `Plot.Workshop` only the shop's back wall. The yard's ground is `Plot.Grounds`.

## Yesterday's map suggestions, re-ranked with today's

[[Sessions/2026-10-30#Proposals and the map review]]: one is done, six are open (one replaced by today's measurements).

| Rank | Suggestion | Status | Size |
|---|---|---|---|
| 1 | Ore Slot / Merge pad out of the lever–stand gap (#1) | new | small |
| 2 | Show what the yard will hold: faint previews, plinths or stalls (#2) | yesterday's #5, open | small–medium |
| 3 | Heat pads (and the Crafter pad) out of the station lanes (#3) | new | small |
| 4 | Dark pad base so pads read on the gravel (#4) | new | small |
| 5 | Delivery cart and board into the yard corner by the pad | yesterday's #1, open; measured in Shop and Street #2–3. From the yard the cart is hidden from the spawn, lever, Furnace 1 and the back door (behind the shop's back wall), seen only from Anvil 1 (107 studs) and Polishing 1 (67). The corner by the pad (x 27–41, z −6…4) is clear paving. | small–medium |
| 6 | Ore labels readable with six slots (#5) | new; replaces yesterday's #7 ("check it on a phone") | small |
| 7 | World Store prompts OneGlobally (#7) | new, being built | small |
| 8 | Strip paving to match the yard (#6) | new | small |
| 9 | The 8 Persistent station models `PersistentPerPlayer` for their owner | yesterday's #4, open: still Persistent (431 parts a plot), no `AddPersistentPlayer` in any script | small |
| 10 | Clear the old layout drafts out of Workspace | yesterday's #3, open: still 23,632 instances (Village #2 has the breakdown) | small |
| 11 | Big-sword pad apart from the sword pad (#8) | new | small |
| 12 | Frame post tops 0.04 under the beam (#9) | new | small |
| 13 | Etching Table 2 as a clone of Table 1 (#10) | new | small |
| 14 | Anvils 1–3's blocks smooth (#11) | new | small |
| 15 | Stocker pad off the Sword Rack's spot (#12) | new | small |
| 16 | Shut the west gate | yesterday's #6, open: no doors or bar; the invisible wall is 30 studs past it (x 410 against the gate at 440) | small |
| 17 | Spawn step (#13) | new | small |
| 18 | Bay's east strip ground (#14) | new | small |
| — | Fewer pads at once | yesterday's #2, **done** (`PAD_CAP` 3 plus the blueprints and the Delivery Cart, `TycoonService` lines 43–83) | — |

## Walks in the core loop

Every hop is under LihFolk's 10 s between stations. The longest is from the polishing station to the shop's first holder, across the yard to the back door (opening x −12.5…−3.7) and back across the shop to Wall Rack 1 on its right wall.

| Starter loop (one hand-made sword) | Studs | s at 16 | s at 20 (Swift Boots) |
|---|---|---|---|
| Spawn → lever | 4.3 | 0.3 | 0.2 |
| Lever → collect at Stand 1 | 12.7 | 0.8 | 0.6 |
| Stand 1 → Furnace 1 | 36.8 | 2.3 | 1.8 |
| Furnace 1 → Anvil 1 (the hilt seat is on the anvil) | 22.2 | 1.4 | 1.1 |
| Anvil 1 → Polishing Station 1 | 61.4 | 3.8 | 3.1 |
| Polishing Station 1 → Wall Rack 1 (shop) | 101.0 | 6.3 | 5.0 |
| Wall Rack 1 → lever | 67.0 | 4.2 | 3.3 |
| **Loop** | **305.3** | **19.1** | **15.3** |

Later legs: Stand 1 → Ingot Rack 1, 27.9 (1.7 s); Ingot Rack 1 → Furnace 1, 12.2 (0.8 s); Furnace 3 → Anvil 1, 8.7 (0.5 s); Anvil 1 → Polishing 2, 55.6 (3.5 s); Polishing 1 → Etching 1, 14.2 (0.9 s); Anvil 1 → Etching 1, 67.0 (4.2 s); Etching 1 → Sword Rack 1, 32.3 (2.0 s); Sword Rack 1 → back door, 27.5 (1.7 s); Etching 2 → back door, 39.0 (2.4 s); lever → Deliveries board, 51.9 (3.2 s); back door → Wall Rack 1, 34.7 (straight).

## Prompts and pads

**Prompt reach overlaps** (standable sq studs where two prompts reach; `OneGlobally` shows only the nearer):

| Pair | sq studs |
|---|---|
| Furnace 1 + 2, Furnace 2 + 3 | 68 each |
| Roll + Collect 2 / Collect 1 / Collect 3 | 54.8 / 42.8 / 42.8 |
| Neighbouring Collects | 50–54 |
| Ingot Rack 1 + Furnace 1 | 44.5 |
| Furnace 3 + Anvil 1 | 23 (not from Anvil 1's spot: 12.6 from Furnace 3's prompt) |
| Etching 1 + 2; Etching 1 + Polishing 1 | 16.5; 15.2 |
| Anvils 2 + 3, 3 + 4 | 10.2 each |

- **Lever:** from the front (z < 13.4) no Collect prompt reaches; the pedestals are at least 12.6 away. Yesterday's move works.
- **Gap behind the lever:** Roll (hold 1 s, reach 7 from the hidden `Machine` part 1 stud behind the knob) and Collect overlap between the lever and the front row. In the back half of that gap Roll is the nearer prompt.
- **Optional:** moving `Machine` 2 studs toward the lever's front, keeping `PromptAt`, would shrink the overlap further.

**Pad spots in the yard and what stands near what:**

| Spot | Pads | Nearest station when standing | Notes |
|---|---|---|---|
| (−4.9, 18.6) | Ore Slots 2–6, Merge | lever 2.1 | finding 1 |
| (−26.1, 40 / 48 / 56) | Heating I–III of Furnaces 1 / 2 / 3; Furnace 2 / 3 | furnace mouth 3.0 | finding 3 |
| (−21, 55) | every sword | Anvil 1's hearth 4.4 | 6 studs in front of Anvil 1: the next goal by the last build ✓ |
| (−16.5, 55) | Zanbatō, Claymore, Flamberge | Anvil 1's hearth 4.4 | finding 8 |
| (−31, 64) | Faster Strikes I–V | Anvil 1's hearth 2.3 | beside the anvil, off its approach ✓ |
| (−4.3, 59.5) | Sword Crafter | Anvil 2's hearth 2.0 | finding 3 |
| (−9.1 / 9.2 / 21.2, 65–66) | Anvils 2–4 | on their own bay ✓ | |
| (−30.9, 28 / 16.1) | Ingot Racks 1–2 | other rack 5.5 | ✓ |
| (31.3, 37 / 52) | Polishing Stations 1–2 | other station 8.8 | ✓ |
| (26.5, 44) | Polish Boost I–III | polishing 5.6 | ✓ |
| (34.7, 26) | Etching Table | polishing 4.8 | ✓ |
| (34.9, 12.8) | Etching Table 2, Sword Etcher | Etching Table 2 0.8 (Etcher) | tucked against the table it follows; fine |
| (30, 0) | Delivery Cart | Etching Table 2 4.8 | clear floor, in sight from every work spot ✓ |
| (18.5 / 9.6, −9.5) | Sword Racks 1–2; Stocker | Sword Rack 0.65 (Stocker) | finding 12 |

- **Labels at once:** in a cheapest-first run of 80 purchases, at most 1–4 pad labels are in view at any station.
- **Overlaps over 20%:** only the two blueprint pads at Anvil 1 (finding 8).
- **Ore labels:** finding 5.

## Style, scale and leftovers

- **The look holds together.** Every station in `Smithy` is SmoothPlastic, Metal, Fabric, Glass, Slate (whetstones) or Neon. The only textured leftovers are the anvil blocks (finding 11) and dead variants (findings 6 and 11). The fence, the shop wall and the ground keep their textures, as decided.
- **Scale against a 5-stud player:**
  - ore stand platforms 2.6, the lever's knob 4.1 (chest height ✓), ingot racks 5.3, sword racks 5.6, furnaces 6.8, sign frames 10.2, fence 3.35;
  - the back door 8.8 wide × 10.3 tall;
  - the anvil faces 3.8: chest height, high for a real anvil, but the anvil camera, prompts and crew poses are built on it. Leave it.
- **Nothing floats or sinks:**
  - the stands sit 0.02 over the paving and the anvil props 0.04 into their hearths;
  - the hearth slabs go below the paving by design;
  - the hanging prop swords hang on their frames;
  - the Test Anvil (Studio only) stands 0.04 over the side lawn and is removed outside Studio (`SmithService` line 14).
- **Second copies face the same way,** all of them.
- **Gaps:** only the bay strip in finding 14.

## Lighting in the yard

- **Settings:** fixed afternoon, `ClockTime` 15.2, no day cycle. Brightness 2.7. Ambient 116,102,92 under OutdoorAmbient 150,162,196: a cool blue fill, but legal, each channel lower. Atmosphere 0.32 density, haze 1.6. ColorCorrection saturation +0.28. Bloom 0.5 at threshold 1.2.
- **Lights in the yard:** three furnace fires (PointLight 0.9, range 11) and two andon lamps (0.8, range 7), none shadowed. Well inside LihFolk's 8–12 local lights; in daylight they barely read. The warmth comes from the furnaces' Neon glow.
- **Why it reads cool:** with near-white gravel under a blue sky fill, the yard looks cool and bright rather than a warm smithy.
- **No global change suggested:** the look is Allen's and the street shares it. If he wants the yard warmer, the cheapest step is the gravel's colour (e.g., a warm sand 184,170,146), which is the same part as finding 4's option.
- **Phones below quality 4 draw no shadows,** so value contrast carries the look. The pads and furnaces are the weak spots (finding 4).

![[Design/Reviews 2026-10-31/Yard and Smithy/yard-lever-default-camera.jpg]]
*Roblox's default camera behind a player at the lever: the Auto Roller and Lucky Ore spots, the six stands, the anvils on their hearths, the furnaces, an ingot rack and the finishing frames (everything bought, Edit).*

![[Design/Reviews 2026-10-31/Yard and Smithy/yard-overview.jpg]]
*From above the shop: the yard inside its fence, the shop at the bottom.*

## Checked and fine

- Spawn faces the lever, 4.3 studs and 0.3 s away. LihFolk's first station under 15 s ✓.
- The lever is the central control, big and at chest height ✓.
- The next goals are in sight where you work:
  - all four starter pads from the spawn and the lever;
  - the next sword 6 studs in front of Anvil 1, Faster Strikes 10 studs beside it;
  - Ore Slot 2 at the roller (finding 1 is about where, not whether).
- No pad stands on a station that is there when the pad shows. The only overlaps are pads on the station they buy, and the Upgraded Store pads on the starter shell in Edit.
- The Delivery pad at (30, 0) is clear floor and in sight from every work spot. The cart isn't (Shop and Street #2).
- Prompts don't show through walls (`PromptFilter`), and pad labels hide behind solid parts.

## Not checked

- Anything in Play:
  - how the labels and prompts actually draw, and which prompt Roblox picks in an overlap;
  - the crew walking the yard;
  - the Upgraded Store's push.
- A real phone.
- Sound.
- The World Store items were still being built: only the Auto Roller and Lucky Ore were in `WorldStore` when looked at.
- Coplanar faces inside non-bevel meshes (furnace, anvil and hilt meshes), which a box check can't see.

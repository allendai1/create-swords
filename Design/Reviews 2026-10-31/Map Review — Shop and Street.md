---
title: Map Review — Shop and Street
type: review
updated: 2026-10-31
tags: [review, map, shop, street, deliveries, thumbnails, create-swords]
---

# Map Review — Shop and Street (2026-10-31)

Read-only review of the shop building, the street in front of the plot and the delivery bay, in the open Studio place (Edit; nothing played, nothing changed). Part of the big review in [[Sessions/2026-10-31#Refinements, Allen's new notes and the big review (evening)]].

**How it was measured.** Plot-local coordinates throughout (plot −z is the street; plot +x is the bay side, on your left seen from the street). For lot N2 (the template's lot): world = (640 − x, 0.5 + y, −284 − z). Two runtime states are modelled from `TycoonService` (the Edit template shows both shells at once): **S** = the Starter Shop at its fullest (Wall Rack 1 free, Wall Rack 2, Display Table 1, Back Wall Rack), and **U** = the Upgraded Store at its fullest (all 5 racks, 6 tables, Big Sword Stand, Cashier counter; `Workshop.Shell` and the Back Wall Rack 12 studs back, as `pushWorkshopBack` does). Customers: `PathfindingService` with `NpcWalk`'s agent (radius 1.75, height 5), walking at 6 studs/s; players at 16 studs/s. Sight lines from eye height 5 (plot y 4.7); where roofs matter, segment tests against the parts themselves (roofs are CanQuery off, so raycasts skip them). Two other agents were building while this ran (shop roofs, World Store items); each section says when it looked. Screen captures (17:45 and 21:43–21:47) are described in words, not saved in the vault.

**Not covered:** anything in Play (blades, prompts, NPC motion, phone view). The display tables' and racks' 381 MeshParts are only bounding-box checked for z-fighting.

## Findings, most valuable first

### 1. Customers stand inside each other: three holders share one stand spot

- **Where:** `ServerScriptService.ShopService` (`runCustomer` lines 1115–1123, `browseEmpty` lines 1037–1043); every holder in `Plot.Shop.Displays`.
- **What:** each of a rack's or table's 3 holders points its `Inspect` ObjectValue at the same `InspectPoint`, and the customer walks to exactly that point. Customers don't collide with each other (`Npcs`/`Npcs` off, ShopService line 550), so two customers heading for swords on the same rack merge into one body, speech bubbles stacked.
- **Evidence:** 34 holders, 12 InspectPoints: each of the 5 racks and 6 tables has one spot for its 3 holders (the Big Sword Stand's 1 holder has its own). The Starter Shop has 4 stand spots for its 12 holders, and at the start only Wall Rack 1 (3 holders, 1 spot). `WALK_INS` = 2 at once, plus one per Rickshaw Bay and one for the Shop Promoter (up to 6). So from the first minutes every second customer shares the first one's spot, for the 2.5 s look plus up to 45 s waiting on an offer.
- **Fix (small, Studio only):** two more stand parts per holder, about 2 studs apart along the holder's face, and point `Slot2`/`Slot3`'s `Inspect` at them. `register` already builds each slot's route from its own `Inspect` value, so no code change. Measured room: side-wall racks spread along z (rack faces 6.3 long, e.g. Wall Rack 1 at (20, −39.3 / −37.3 / −35.3)); tables along x in front of the top (8.5 long, e.g. Display Table 1 at (−14 / −12 / −10, −43.5); Display Table 3 at (12 / 14 / 16, −43.5) while the World Store chest of finding 6 stands left of it); the Back Wall Rack along x (14.8 / 16.8 / 18.8; the parts move back with it). Each new spot keeps the existing spot's distance to its own holder and has 2.8+ studs to walls and other furniture in both states (the tightest: Display Tables 1 and 3's spots to the front wall, as today).
- **Rulings:** none against it (customers' spots were never decided; NpcPass 2026-10-30 stays).

### 2. The delivery cart and board are still where nobody sees them

- **Where:** `Plot.DeliveryBay.Cart` (33, −31.5), `DeliveryBay.DeliveryBoard` (board mesh at (26.4, −24), facing +x into the bay); the Delivery pad at (30, 0).
- **What:** Allen's note ("delivery cart needs to be closer to the base, its so far that people won't even notice it") was answered by moving the pad; the cart and board stayed in the bay. The board is the only way into Deliveries (`DeliveryController` opens on `DeliveryPrompt`; no HUD button) and the window closes when you walk away from it. Buying the cart bursts confetti at the pad while the cart builds in 30 studs away, out of view from most of the plot.
- **Evidence (sight lines, eye height 5, Edit geometry):**

| From | Cart (33, −29) | Board (26.9, −24) |
|---|---|---|
| Spawn (0, 7) | blocked by `Workshop.Shell` (shop back wall) | blocked |
| Ore lever (0.6, 13) | blocked | blocked |
| Forge 1, Anvil 1 | blocked | blocked |
| Sword Rack (14.5, −9) | blocked | blocked |
| Shop middle, shop door, street middle | blocked (shop walls) | blocked |
| Delivery pad (30, 0) | visible, 29 studs | visible, 24 studs, but 81° off its face |
| Etching Table 2 (31, 9), Polishing Station (31, 37) | visible, 38 / 66 studs | visible |

  From the pad (capture 21:47) the cart is a small shape 30 studs down the bay and the board is a plank on edge against the shop wall. In the Upgraded state the shop reaches z −6, so the bay is hidden from even more of the yard. Walks are fine (spawn → board 50 studs, 3.1 s; Anvil 1 → the board's prompt 122 studs, 7.6 s): it's sight, not distance.

  Candidate spots, same test against every visible plot part, Upgraded walls present:

| From | Cart today (33, −29) | Bay's back (33, −15) | Yard corner (34, −3) |
|---|---|---|---|
| Spawn, lever, Forge 1 | blocked | blocked | visible |
| Anvil 1 | blocked | visible | visible |
| Sword Rack (Starter / pushed) | blocked / blocked | blocked / visible | visible / visible |
| Polishing Station | visible | visible | visible |

- **Fix (small–medium):** yesterday's map review's #1, still open: cart and board into the yard corner by the pad, the cart about (34, −3) with its shafts toward the street, the board beside it facing the yard (papers toward +z). `DeliveryService.LANE` 47 → about 73 so the lane stays at z −76 (the courier then pulls the cart out through the bay, which becomes its driveway; the bay gate at x 26.4–40.1 and the gutter bridge at x 33 still line up). The cart there leaves 7.7 studs to the Upgraded Store's back corner and 5.8 to Etching Table 2. The line from the spawn passes the pushed Sword Rack's end by about 0.4, so look at it in Play. Once the cart stands on its pad, the pad is where the upgrade appears again (the convention every other pad keeps).
- **Rulings:** 2026-10-22 "A delivery bay beside every shop" (a carrier that "could carry over into the street": kept, the bay becomes its way out); 2026-10-29 "The Delivery Cart is bought outside, in the bay"; 2026-10-30 "Delivery Cart from the start … Its pad stands in the yard's corner by the bay now". Moving the cart revisits the 2026-10-29 line, so it's Allen's call.

### 3. The board you can see doesn't open Deliveries

- **Where:** `DeliveryBay.DeliveryBoard.Panel` (invisible, holds `DeliveryPrompt` and the `Status` timer) at (26.4, 3.1, −36); `DeliveryBoard.Board` (the notice-board mesh) at (26.4, 2.9, −24).
- **What:** the mesh stands 12.0 studs from its Panel (`build_delivery` put both at z −36; the mesh was moved since, the Panel wasn't). The prompt reaches 9 studs, so standing in front of the papers (x 28.5) at z −27 / −24 / −21 you are 9.3 / 12.2 / 15.2 studs from it: no prompt. Coming from the yard you reach the board's far end first. The trip timer floats 2.6 over the empty Panel near the cart's shafts, not over the board.
- **Fix (small):** move the Panel onto the board's papers (or the board back to z −36). If finding 2 is taken, place both together in the corner.
- **Rulings:** none.

### 4. The new roof tier hides your name on the plot nameplate from the yard

- **Where:** `PlotService.NAMEPLATE_AT` = (0, 42, −33), commented "clear of the Upgraded Store's roof (top 35)", still so at 21:48; the roof builder's new `Shop.Upgraded.Shell.Roof.UpperTier` (x ±16.9, y 29.6–38.45, z −32.6…−19.9).
- **What:** the nameplate is a 30 × 15 billboard, not always-on-top, so geometry hides it. Its `Title` ("<name>'s Plot") spans y 35.4–39.9, below the tier's top (38.45). Every player sees their own nameplate from the yard most of the time.
- **Evidence (segment tests against the Upgraded roof's 286 parts, 18:06):** the name line is behind `UpperTier.TierWall`/`TierRoof` from the yard by the spawn (0, 16, 22), the lever (2, 15, 30), Forge 1 (−22, 15, 50) and a high yard camera (0, 30, 40); the lower half from Anvil 1; clear from the street (0, 12, −95). Raised by 5, every one of those is clear (only a camera pressed against the back wall still loses it).
- **Fix (small):** `NAMEPLATE_AT` (0, 47, −33) and its comment (roof top 38.45).
- **Rulings:** 2026-10-22 plot nameplate; 2026-10-31 Allen's lower roof / second roof layer.

### 5. Customers pop in and out of thin air in front of the door

- **Where:** `Plot.CustomerSpawn` (−1, 2.5, −61), 5 studs into the road, 14 studs from the shop front; `ShopService.makeNpc` and the `npc:Destroy()` after `walkTo(npc, spawnPoint)`.
- **What:** walk-in customers appear at full opacity on that spot and vanish there when they leave. Rickshaw customers fade (`Rickshaws.FADE` 1.2 s), walk-ins don't. It's straight in front of the door, so you see it from inside the shop, at the Mailbox and from the street.
- **Evidence:** spawn → `EntryPoint` (−3.5, −42.5) is 18.7 studs, 3.1 s at 6 studs/s. No client script touches `workspace.Customers`.
- **Fix (small):** fade them in over about 0.6 s after `makeNpc` and out before `Destroy`, as `Rickshaws.paint` does (it keeps each part's base transparency). Spawning them along the walkway beyond the lamps (about (±40, −60)) instead would add about 4 s of walking before the tutorial's first sale, so the fade is the better one.
- **Rulings:** none (customer speed 6 is Create Pottery's, 2026-10-23, unchanged).

### 6. The World Store's coin chest is hidden from the street and boxes in Display Table 3

- **Where:** `Plot.WorldStore.MoreCoins` (looked at 21:45–21:48): x 8.3–10.5, z −46.4…−44.4, inside the shop against the left lattice bay beside the door; its one colliding part, `Body`, z −45.85…−44.55; `Buy` prompt, 6 studs.
- **What:** (a) it's meant to be seen and bought, but the front wall hides it from the street centre, the walkway and the road (segment tests: blocked by `Slat`, `Post`, `Shoji`); only someone already inside sees it. (b) In the Upgraded state it leaves 1.5 studs between itself and Display Table 3's top (z −43.06), where the strip along the front wall was 3.3.
- **Evidence:** the customer route to Display Table 3's spot (12, −43.5) was 15.5 studs straight along the front before the chest; now pathfinding goes round the table's far end and back along the front wall: 36.8 studs (6.1 s instead of 2.6), through a strip 2.4–3 studs wide where the agent needs 3.5. Expect the corner stalls `NpcWalk` logs. In the Starter state nothing stands near it and every route is clear.
- **Fix (small):** out on the walkway left of the door, between the Mailbox (x 8.8–11.2) and the decorations' `DoorRight` spot (15.7), about (13.3, −49.3): clear of the walk-in line (x −1…−3.5) and seen from the street. Or keep it inside but not against Display Table 3's front.
- **Rulings:** 2026-10-30 proposals §2 / 2026-10-31 world purchase spots (the World Store builder's own work: comment only).
- **Other World Store items:** `AutoRoller` (1.7–7.5, 13.9–16.4) and `LuckyOre` (10.8–13.2, 25.2–27.6) stand in the yard by the ore roller, outside this area. No rope at the door or crate by the door yet at 21:48.

### 7. N2's walkway is plain Roblox brick

- **Where:** `Village.Street.Walkway` at plot (0, −50.25), 48.5 × 7.5, the walkway in front of the first plot's shop.
- **What:** Material `Brick` with MaterialVariant `PaintPlanks`. PaintPlanks is a WoodPlanks variant, so it doesn't apply to Brick and the part shows Roblox's default pink brick. The other 11 walkways are `Slate` + `PaintStone`. The part's `StyleTest_` attributes show it was Slate when the style test ran, so it was changed later (Allen's test or a stray edit).
- **Evidence:** the capture into the bay from the street (17:45) shows salmon brick in front of the shop beside the next lot's grey slate.
- **Fix (small):** Slate + PaintStone like the others, or Material WoodPlanks if a boardwalk was meant.
- **Rulings:** 2026-10-22 FreeStylized textures; 2026-10-30 "Textured surroundings" (ground keeps its texture).

### 8. From the street the shop doesn't show a single sword

- **Where:** the front lattice bays (`Shell.Shoji` + `Slat`, x ±6.7…±23.75) and the displays inside.
- **What:** every display faces inward: wall racks on the side walls (edge-on through the door), Display Table 1 behind the right-hand lattice, the Back Wall Rack 29 studs back. The 12-stud doorway shows a mostly empty floor in the Starter Shop (one table, three racks on the walls), and empty racks are bare shelf boards (cradles appear only under a sword). What says "sword shop" from the street is the kanji signboard 刀剣 and the name kanban.
- **Fix (medium, Allen's call):** (a) the two lattice bays beside the door (x ±6.7…±13) as open shop windows with prop swords on a rack facing the street (a machiya *mise*), `SmithyCore.buildSword` props with `Prop` and no `SwordId`, as on the station frames; or (b) a big hanging sword sign off the front plate. Either reads in a thumbnail and to a kid walking past. Don't bring the noren back (Allen removed them).
- **Rulings:** 2026-10-22 "Shop holds only what the game uses"; 2026-10-29 prop swords on the station frames (Allen's own ask); noren removed (Fixes2 "remove these entrance curtains", List.md, [[Sessions/2026-10-28#Fixes2]]).

### 9. Shop fronts are side-lit at best, and the south row's never get sun

- **Where:** `Lighting` (ClockTime 15.2 fixed, no day cycle; `GeographicLatitude` 28; values from `build_style_test`).
- **What:** `GetSunDirection()` is (−0.74, 0.67, 0.08): almost due west, 42° up. A north-row front (normal world +z) gets a dot of 0.08, nearly grazing; the bay side wall (plot +x) gets 0.74. South-row plots are turned round, so their fronts face north and, at latitude 28, get no direct sun at any clock time.
- **Fix:** for thumbnails (no game change) shoot N2 from the bay side (below), or move the clock only while capturing, toward midday, and check the front lights up. A game-wide change (LihFolk's "bright cartoon" preset uses 13.5) would change every view, so that's Allen's call. Medium, for thumbnails.
- **Rulings:** 2026-10-22 Genshin style rollout (its lighting values).

### 10. The name on the kanban is in a placeholder font

- **Where:** `Shop.Starter.Shell.Roof.Kanban` (9 × 2, now at y 10.6–12.6) and `Shop.Upgraded.Shell.Roof.Kanban` (17 × 2.2), their `SurfaceGui` TextLabel; `PlotService` writes `player.DisplayName` into it.
- **What:** SourceSansPro Bold, no outline (`TextStrokeTransparency` 1), cream on the Starter's dark board, gold on the Upgraded's. It's the only SourceSansPro text in the world: all 13 `ReplicatedStorage.WorldText` templates are GothamSSm Bold/Heavy. On the Starter's 9-stud board a 20-character name scales down to about 0.75 studs tall. (The `SurfaceGui`s are PixelsPerStud 40; their `CanvasSize` 800 × 600 is ignored, a leftover.)
- **Fix (small):** GothamSSm Heavy with a thin dark `UIStroke`, one layer (it's painted sign art, like the nameplate's one layer).
- **Rulings:** 2026-10-21 "Shop sign shows the owner's name".

### 11. Rickshaw Bay 3 is built into the street lamp

- **Where:** `Plot.Parking.Bay3` (slab x 14.75–23.25, z −63.2…−59.4) and `Village.Street.LampPost`/`LampFoot` at (22.25, −59). Every lot has a lamp at ±22.25 from its centre, so every plot.
- **What:** the lamp's stone foot (x 21.55–22.95, z −59.7…−58.3) overlaps the slab's corner by 1.4 × 0.3. A parked rickshaw (from `Rickshaws`: puller at bay x − 2.1, body x 16.2–22.9, z −63.1…−59.5) has its near wheel over the foot and passes 0.08 studs from the post as it pulls in.
- **Fix (small):** Bay 3's slab, sign and pad 1.5 studs toward the door (x 17.5), or the lamps out to x ±25.
- **Rulings:** 2026-10-23 rickshaw bays "on the street in front of the shop" (unchanged).

### 12. An empty planter on the walkway beside the shop

- **Where:** `Village.Atmosphere.Dressing.Planter` at plot (−27.2, −52), a cobblestone box with `Soil` and nothing in it (four in the village; the others at (69.3, −52), (−69.2, −116), (27.3, −116)).
- **What:** reads as unfinished, right at the shop's corner by the side-yard gap; in the straight-on capture (21:47) it's the brown box beyond the right lamp.
- **Fix (small):** remove them, or a built prop there. Not a plant unless Allen asks (no generated nature).

### 13. Rickshaw bay slabs are the only untextured slate on the street

- **Where:** `Plot.Parking.Bay1–3.Slab` (Slate, no MaterialVariant). In the straight-on capture they're three flat grey pads with small white signs, reading as bare concrete when no rickshaw is parked.
- **Fix (small):** MaterialVariant `PaintStone`, like the curbs, bridge and walkways.

### 14. A lone R6 "Swordsmith" stands by the shop, on lot N2 only

- **Where:** `Workspace.Swordsmith` (R6: Torso, Left Arm…, a straw gasa hat) at plot (−34.3, −8), on the side paving off the shop's back corner.
- **What:** outside `Workspace.Plot`, so only lot N2 has it; R6 among R15 crew and customers; no script uses it.
- **Fix:** if it's Allen's, decide whether it belongs on every plot (then into the template, as R15) or nowhere.

### 15. The delivery board faces into the bay

- **Where:** `DeliveryBoard.Board`, papers toward plot +x.
- **What:** 81° off its face from the Delivery pad and 73° from the bay mouth: from the yard and the street it's a plank on edge (capture from the pad, 21:47).
- **Fix:** comes with finding 2 (face the yard). If the board stays, turn it to face the passage (+z).

### 16. Small leftovers

- `build_shops` / `build_delivery` still build the removed delivery door and bay fence (already noted 2026-10-29), and `build_delivery`'s Panel position disagrees with the mesh (finding 3).
- `StyleTest_*` attributes on the plot and village parts are `build_style_test`'s undo data, live and harmless.
- The Upgraded Store's 14 `UpperFrame.UpperPost` cast shadows while no other roof part does ("roofs cast no shadow into the shop", 2026-10-22); they stand on the outer walls and their shadows fall outside, so nothing to fix.

## Roofs from the street

Final look 21:43–21:48, after the roof builder had finished (its preview copies `_RoofCapTmp_Starter`, `_RoofCapTmp_Upgraded` and `_RoofCapTmp_StarterBefore`, 1,496 parts on lots N1 and N3 and far out, were removed by 21:45). Captures from T1 and T3 below; Edit shows both shells at once, so the shapes were read from geometry.

- **Starter Shop:** walls about 2 lower (posts 12.95 → 10.95, plates 13.0 → 11.0), front eave 9.0–10.4 over the walkway (9.2 above it), ridge 17.7–19.2 at z −30, top 19.45 (was 21.65); kanban down to y 10.6–12.6, lanterns to 7.1–9.0. One low, wide storey, 47.5 wide × 19.5 high.
- **Upgraded Store:** a raised `UpperTier` on the main ridge (33.8 wide, louvred sides, its own ridge and onigawara), top 38.45 (was 34.76). With the pent roof, the upper storey and the main roof that's four steps of eaves, 47.5 wide × 38.5 high: twice the Starter's height.
- **From the street:** the tier shows from about 29 studs out (its ridge) and whole from 39 (the road's middle); from the walkway and the near half of the road the main roof hides it. Straight on at 33 studs (T3) the louvres and ridge read clearly over the main roof; from the bay side at 62 studs (T1) the stepped silhouette reads as one building growing upward. The two shapes are different enough to carry a side-by-side thumbnail.
- **Z-fighting after the roof work** (18:09, same check as below): Upgraded state 545 parts, Starter state 345: still only the cart's 0.02-stud slivers.
- **Knock-on:** the nameplate (finding 4).

## Thumbnails: beginner vs fully upgraded

**Light.** At the game's 15.2 the sun is in the west, so a north-row front is grazing-lit and the bay side wall (plot +x) is the sunlit face (finding 9). Shoot N2 from the bay side, or move the clock toward midday for the capture only.

**Cameras** (plot space, then N2 world). Same camera, weather (Sunshine) and clock for both shots.

| Shot | Camera (plot) → look at | N2 world camera → look at |
|---|---|---|
| T1 eye-level 3/4, bay side | (35, 5, −92) → (−3, 9, −42) | (605, 5.5, −192) → (643, 9.5, −242) |
| T2 high 3/4, bay side | (28, 34, −92) → (−2, 14, −34) | (612, 34.5, −192) → (642, 14.5, −250) |
| T3 straight through the door | (2, 5.5, −80) → (−4, 5, −20) | (638, 6, −204) → (644, 5.5, −264) |

- **T1** (captured 21:43): the shop left of centre, the bay gate and cart framing the left, the street's stone centre path leading to the torii at the right edge: a good leading line. The lower third is flat road; tilt up a little or crop.
- **T2:** the shop, the bay and the yard's stations behind in one frame; from (48, 42, −112) a neighbouring building cut into the corner, so this closer spot.
- **T3** (captured 21:47): the front symmetric between the two street lamps, the tier over the main roof, the Mailbox left of the door; the three empty rickshaw slabs sit in the foreground. Through the door the Upgraded Store's back shows; the Big Sword Stand at (−15.2, −10.5) is in the line of sight past Display Table 1's edge (0.3 clear), tabletops below the line.

**Beginner:** one low storey, the name kanban and two lanterns, the Mailbox, an empty walkway, Wall Rack 1 with swords seen through the door. **Fully upgraded:** the pent roof and gold kanban, the upper storey, the tier, rickshaws parked in all three bays (empty slabs look like bare pads), the Promoter on the walkway, customers in the door, and the shop-front decorations if Decorate is back by then (`ReplicatedStorage.DecorModels`: Stone Lanterns at the door spots ±15.7, Shop Banners at the poles ±22.9, Planters at the bay spots ±21.1; hidden since 2026-10-30).

**What would make the front read better**, best first: swords visible from the street (finding 8); a lit front (finding 9); customers walking in rather than popping (finding 5); the coin chest where the street can see it (finding 6); slate under the shop instead of brick (finding 7); no empty planter (finding 12); a name you can read (finding 10). Frame tight: the road is 56 studs of flat earth and fills the lower half of any street-level shot from farther than about 40 studs.

**Inside** (capture 21:47, Edit): bright and even, pale planks and white walls, the tables the only warm colour; the empty racks read as bare shelves until swords go on. Plain by Allen's choice (no extras, no wall lamps); the hidden wall decorations (Wall Scroll, Paper Lamp) would break up the white when Decorate returns.

## Checked and fine

- **Z-fighting** (the project's `coplanar_check` logic, run on each state's own parts, with the 12-stud push applied for U and the hidden-until-a-sword cradles and stand bases counted as visible): S 321 block/wedge parts, U 464 (17:50); S 345, U 545 after the roof work (18:09, World Store included); 8 pairs each time, all on the cart (`Cart.Bed` against its `Side`/`End` boards, slivers 0.02 studs high). Nothing visible. A bounding-box pass over the MeshParts of one table, one rack, the Big Sword Stand, the counter and the board found only prongs inside posts, leg feet at the floor and the counter's stacked coins. Edit-only: the two shells overlap (both floors at −0.30), as designed.
- **Room to walk inside** (widest path on a 0.25-stud grid of each state's furniture, 0–4.7 studs above the floor): from `EntryPoint` every rack is reached with 6+ studs of width and the Big Sword Stand with 4.5; tables with 3 at the last step, where the stand spot sits 0.5 off the top by design. In U the Cashier counter and Display Table 6 leave 2.75 studs between them (z −15…−12.25), but no route needs that gap. The exception is Display Table 3 since the chest (finding 6).
- **Customer paths** (Edit, all furniture present): spawn → entry 18.7 studs; entry → holders 8.6–31.3 studs (1.4–5.2 s at 6 studs/s), Display Table 3 now 36.8. The walk-in line crosses the gutter on `Yard.Bridge` (x −3…3; the line is at x −1.8) and the door at x −2.9 (opening x −6.1…6.1). The Promoter's spot (−9, −50.5) is 6.6 studs off it.
- **Doors and scale:** front opening 12.2 wide × 9.85 tall (posts at x ±6.7, beam bottom 9.55 over a −0.3 floor), now under the Starter's eave at 9.0; back doorway x −13…−3.2; bay gate 13.7 wide under a lintel at 7.8. Tables 3.05 above the floor, counter top 3.2, wall-rack shelves 4.2–8.5 (Allen's shoulder-height rule).
- **Pads in the shop** stand on clear floor in both states (nearest furniture ≥ 2.4 studs; the Cashier and table pads sit where their item goes, as every pad does). Promoter pad on the walkway (−9, −50.5). Parking 3's pad (17.2–20.8) is 0.75 from the lamp foot (finding 11).
- **Owner walks:** spawn → Wall Rack 1 60.8 studs (3.8 s), Sword Rack → Wall Rack 1 64.6 (4.0 s, round through the back doorway), Anvil 1 → Wall Rack 1 116 (7.3 s), spawn → Mailbox 65 (4.1 s). All under LihFolk's 10 s between stations.
- **Interior light:** invisible `ShopLamp` points (0.3, range 20, no shadows; 4 in the Starter, 6 in the Upgraded) and daylight once the roof fades. No night to plan for (no day cycle).
- **Ground layers:** lot pad −0.34, lawns, bay earth and shop floors −0.30, paving −0.26, walkway −0.20, bay slabs −0.26 over the −0.30 road: 0.04+ apart wherever they overlap.
- **Noren:** none at the front, as Allen asked (Fixes2, List.md); none on the back doorway (2026-10-29).
- **Fence and gate:** the front fence line (z −45.5) meets the shop's sides (0.1 gap at the right, a 1.6 slot between the shop and the bay gate post at the left, too narrow to walk); the 6-stud side-yard gap at x −36…−30 is clear.

## Seen outside my area

- The loose plot copy at x ≈ 2000 (`Workspace.Shop`, `Smithy`, `Parking`, `DeliveryBay`, `Fence`, `Workshop`, `Yard`, a disabled `PlayerSpawn`) and the seven layout drafts are still in Workspace (yesterday's map review, #3).
- `Smithy.TestAnvil` (`StudioOnly`) stands on the side lawn at (−30, −20); fine if it really goes at runtime.

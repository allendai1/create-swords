---
title: Six Plots
status: built 2026-10-21 — multi-player playtest pending
type: design
date: 2026-10-21
updated: 2026-10-24
tags: [design, multiplayer, plots, tycoon, create-swords]
---

# Six Plots

Allen (2026-10-21): "is there also 6 total player plots that players can use now?" Not yet then: the street had six lots, but only lot N2 held a plot and every script served that one plot. He asked for a plan first ("which scripts change, how plots are cloned into the lots and assigned, and what happens when a player leaves"), then said "Build it" with Claude's defaults.

## How it works

- **One template.** `Workspace.Plot` in lot N2 is the plot you edit in Studio: shop (Starter / Upgraded / Displays / Interior / EntryPoint / CommissionBoard), `Workshop`, `Smithy` (all stations), `Pads`, `Yard`, `PlayerSpawn` and `CustomerSpawn`. Its pivot is `Village.Lots.PlotSlotN2`'s CFrame. When a server starts, `PlotService` moves it to `ServerStorage.PlotTemplate`.
- **Claiming (player joins).** The player gets the first free lot in the order **N2, N1, N3, S2, S1, S3** (middle north first):
  1. A copy of the template is pivoted onto that lot's `PlotSlot`; the south lots get a turned-around copy facing the street.
  2. It is named `Plot_<lot>`, with attributes `Lot`, `OwnerId` and `OwnerName`.
  3. It is locked to "only the free items" before it appears.
  4. The lot's empty plot goes away (since 2026-10-22; a closed shopfront before).
  5. The player's `RespawnLocation` is their plot's `PlayerSpawn`, and their `Plot` attribute names the plot.
- **Visitors** can walk into anyone's shop and workshop but can't use anything: other plots' E prompts stay off on your screen, the `+` display markers and Buy buttons only show on your plot, and the server checks ownership for every action.
- **Leaving.** The plot is deleted with everything on it (bought upgrades, displayed swords, ingots in the furnace, ore on the trays), and the lot's empty plot comes back. Coins and carried swords are player data, so the plot doesn't touch them. **Since 2026-10-22 all of it is saved first** ([[Development/Saving]]): on the player's next visit, whichever lot they get is set up with their upgrades (Upgraded Store push included) before it appears, displayed swords go back on the same holders, racks are refilled, and furnace and ore-box contents come back as ingots. A plot is handed out only once its owner's progress has loaded.
- **Unclaimed lots (2026-10-22).** Allen: "Why don't you just have all 6 player plots on the map. no need to replace them with another empty building when its already empty".
  - Every unclaimed lot shows the plot itself, empty: PlotService makes these copies of the template at startup (`Village.Lots.Empty<lot>`).
  - Nothing on them can be used or picked up. Locked upgrades, pads, spawns and prompts are removed, and every tag except `HidesRoof`, so a visitor can still see inside.
  - Claiming a lot swaps its empty plot for the player's own copy; leaving swaps it back.
  - They replace the closed shopfronts.
- **Server size.** Six lots, one per player. A seventh player gets no plot. The server size is 6 (Game Settings → Places; set through the Open Cloud Places API on 2026-10-22, since a game script can't).

```
            gate          lane          lane          shrine
   north:   house  [N1 2nd]  ↑  [N2 1st]     [N3 3rd]  house
                    -------------- street --------------
   south:   house  [S1 5th]     [S2 4th]  ↓  [S3 6th]  house
```

Since 2026-10-22 the map is the simplified town ([[Art/Town Street Redesign References#Simplified map built (2026-10-22)]]). Lot centres are 96.5 studs apart (world x 543.5, 640, 736.5). Paved lanes 48 wide (a full frontage) separate the lots, and the arrows mark the two lanes that run on through the back wall. N2 and S2 face each other across the street. **Since 2026-10-24 they line up with the other lots** (Allen: "The shop building is misaligned with the actual street"): they stood 8 further back as a junction, so their gutter, walkway and lamps stepped back from the street's gutter line. Both lots and their frontage moved 8 studs onto the line, the template's pivot is now (640, 0.5, −284) (was (640, 0.5, −292)), the two Junction slabs are parked in `Legacy`, and the delivery courier's lane is 47 studs out, 8 short of the street's middle, as for every lot ([[Sessions/2026-10-24#Refinements 3]]). On the earlier town street the lots were about 187 apart (world x −169.6, 17.5, 204.6).

## What changed in code

See [[Archive/Project History/Code Map before cleanup — 2026-10-22#Six player plots (2026-10-21)]] for the full list.

- New: `ServerScriptService.PlotService` (template, claim, release, `plotOf`, `plotFrom`, `ownerOf`, `onPrepare` / `onPlot` / `onRelease` hooks), `StarterPlayerScripts.MyPlot` (the local player's plot) and `StarterPlayerScripts.PromptFilter`.
- Per plot: TycoonService, ShopService, ForgeService, RackService, EtchService, PolishService and LeverAnimator on the server; the station controllers, ShopController and TycoonController on the client. The hilt-seating view now turns with the plot, so a south plot's camera is on its street side.

## Checks done

- Every changed script compiles; `MyPlot` and `Upgrades` load from a clone.
- **Fit test in Edit.** Copies of the plot on the other five lots, made the way PlotService makes them, were checked and removed:
  - each faces the street, with its door, customer spawn (on the road) and player spawn (on the workshop floor) in place;
  - no solid part touches a neighbour; only roof eaves reach over, as every house's do;
  - the Upgraded Store's side windows faced the neighbours' walls, so they were removed.
- **Not run:** a multi-player test. Allen's checklist:
  - **Test → Clients and Servers** with 2–3 players: each gets their own lot in order, and spawns in their workshop.
  - On your own plot, every station, pad and display works; on someone else's, nothing does.
  - Customers come to each shop.
  - When a player leaves, their plot goes and the empty plot comes back.

Related: [[Design/Tycoon Upgrades]] · [[Archive/Art/Japanese Street]] · [[Development/Code Map]] · [[Sessions/2026-10-21]] · [[Home]]

---
title: Six Plots
status: built 2026-10-21 — multi-player playtest pending
type: design
date: 2026-10-21
updated: 2026-10-21
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
  4. The lot's closed shopfront goes away.
  5. The player's `RespawnLocation` is their plot's `PlayerSpawn`, and their `Plot` attribute names the plot.
- **Visitors** can walk into anyone's shop and workshop but can't use anything: other plots' E prompts stay off on your screen, the `+` display markers and Buy buttons only show on your plot, and the server checks ownership for every action.
- **Leaving.** The plot is deleted with everything on it (bought upgrades, displayed swords, ingots in the furnace, ore on the trays), and the closed shopfront goes back up. Coins and carried swords are player data, so the plot doesn't touch them; there is no saving yet (session-only, like before).
- **Server size.** Six lots, one per player. A seventh player gets no plot. Set the server size to 6 in Game Settings → Places (a script can't).

```
            gate                        street                         shrine
   north:   houses  [N1 2nd]  houses   [N2 1st]   houses  [N3 3rd]  houses
   south:   houses  [S1 5th]  houses   [S2 4th]   houses  [S3 6th]  houses
```

Lot centres are about 187 studs apart along the street (world x −169.6, 17.5, 204.6); N2 and S2 face each other across it.

## What changed in code

See [[Development/Code Map#Six player plots (2026-10-21)]] for the full list.

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
  - When a player leaves, their plot goes and the closed front comes back.

Related: [[Design/Tycoon Upgrades]] · [[Art/Japanese Street]] · [[Development/Code Map]] · [[Sessions/2026-10-21]] · [[Home]]

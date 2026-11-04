---
title: Handoff — Performance fixes
type: handoff
updated: 2026-10-31
tags: [performance, handoff, create-swords]
---

# Handoff: performance fixes (2026-10-31)

Fixes for [[Design/Reviews 2026-10-31/Performance Review]], made in the Studio place (Edit) with multi_edit. Studio stayed in Edit the whole time. Nothing was required from SmithyCore, PlaytestLog or PlotService. Every edited script was compile-checked (the `return function() … end` wrapper), and OreBoxShow was load-checked from a fresh clone. For each new local, I checked that its `local` line comes before its first use.

## Done

| # | Script | Change | Before → after |
|---|---|---|---|
| 2 | `StarterPlayerScripts.Hotbar` `drawArt` (+ `RIM_FOV` under `RIM`) | The eight white rim copies now sit in one rim viewport behind the item. Each copy is nudged in 3D by one box pixel at the item's depth, the same way `ItemPicker.outline` does it. The rim viewport is 1 px bigger on every side, and its camera FOV is widened to `RIM_FOV` so the scale doesn't change. That lets the rim stand past the box edge the way the nudged viewports did; without it the katana's tip rim was clipped. Neon white copies and the rarity sheen are unchanged. | 9 → 2 ViewportFrames per slot: phone bar 45 → 10, desktop 81 → 18, open bag (30 cards) 270 → 60 |
| 3 | `StarterPlayerScripts.SwordRenderer` | A sword with `Prop = true` is drawn only when no ancestor is `Locked`. It waits on that ancestor's `Locked` attribute and is drawn once the station unlocks. World etches now build one at a time through a FIFO (`etchTurn` / `etchDone`; checked: 5 queued builds ran in order, at most 1 at a time). The etch call is pcall'd, and a sword that left while it was waiting skips its build. `rendered` is now weak-keyed. | Before: at join, every prop on every plot was built, with 5 canvases at once (slices stacked to about 20 ms a frame). After: no builds for locked stations, and 4 ms of slice per frame at most for world swords. |
| 3b | Template props `Plot.Smithy.EtchingTable.Dress.PropSwords.PropSword_FallingStars_katana`, `EtchingTable2…PropSword_FallingStars_gladius`, `EtchingTable2…PropSword_WovenWind_wakizashi` | `Etch` attribute changed from "Falling Stars" / "Woven Wind" to the ids `FallingStars` / `WovenWind`, so these props now get their etch | 5 → 8 unique prop canvases, built only on unlocked stations, one at a time |
| 8 | `OreBoxAnimator`, `OreBoxShow` | Your own plot's rolls always play. Another plot's roll plays only within `RANGE` 120 studs of the camera. A far roll waits in `far` and starts mid-roll if the camera comes within range. Otherwise the stands just show the real ores ForgeService reveals at the end, so nothing is left wrong. The camera punch runs only when `Prefs.shake()` is true, and the gamepad rumble only when `Prefs.haptics()` is true. | Auto-Roll on six plots: up to 36 ingots, 36 lights and about 108 writes a frame → only the shows near you |
| 9 | `ShopController.bindSlot` | Binds only `MyPlot.owns` holders. A `bound[part] = unbind` table blocks a second bind while one is pending or live. One global `Plot` attribute handler unbinds holders that are no longer yours and binds the new ones. The 34 per-slot `Plot` connections are gone. | 204 markers (about 2.9k GUI instances, about 1,000 refreshes a second) → 34 |
| 11 | `ForgeService` (glow only) + new `StarterPlayerScripts.ForgeGlow` | The server tags each slot part `ForgeSlot`. `glow(slot, from)` sets `HeatFrom`, `HeatStart` and `HeatEnd` (server time) once at both put sites (player and crafter), and `clearSlot` clears them. The 10 Hz loop now only runs `refreshBoard`. ForgeGlow animates every plot's slots with tweens (colour → HOT, light 0 → 2). Tested on a scratch part: f = 0.5 gave (202,144,104), against the server formula's (203,145,105); it ended at HOT and 2.00. | 20 replicated changes a second per heating ingot (about 360 a second in a full server) → 3 attribute sets per heat |
| 12 | `TycoonController` | Weak `watchedItems` / `watchedSlots` guards in `watchItem` and `watchSlot`. They are separate tables because one instance (in Legacy) carries both tags. | 1 extra set of handlers per stream-in → 0 |

**Etch build times** (PC, unspread make + reveal, measured while other agents were working, so noisy): Eclipse 491–1,331 ms, Tide 316, Fracture 486, Stormroot 263, WovenWind on katana 993, **new:** FallingStars on katana 858–1,422, FallingStars on gladius 170–505, WovenWind on wakizashi 1,730–3,032 ms. These are heavier than the review's numbers. Baking the 8 prop images once, as the review's "later" item suggests, would remove them entirely.

## NOT done

- **#6, the cart and rickshaw welds.** Not started in the scripts. What I found and tested:
  - Edit test: `PivotTo` on 5 anchored parts with no welds writes 5 CFrames. With the parts welded to an anchored root, it writes 1. Changing a `Weld.C0` writes 0 CFrames, so the wheels can spin through C0.
  - **Rickshaw:** `ServerStorage.Rickshaw` already has `Root` as its PrimaryPart. Plan: WeldConstraint the 16 body parts to Root (unanchored, Massless); weld one wheel Hub to Root with a `Weld` and WeldConstraint the other 9 wheel parts to that Hub; in `place`, set the hub weld's `C0 = turn * hubBase` instead of each wheel's CFrame.
  - **Cart:** it is a TycoonItem (`Upgrade = Delivery`). TycoonController's build-in flies only *anchored* parts, so permanent welds would make the cart drop in as one piece when bought. Plan: weld at runtime only while it is out (`rig(c, state ~= "home")` in `move`: WeldConstraints to the Bed, `Weld`s on the two Wheels with C0 spin), then re-anchor and unweld at home.
  - Also seen: `paint` writes every part's Transparency each frame during the 1.5 s fades (cart plus courier, about 50 a frame), and Rickshaws' `run` calls `paint` every frame (no-op writes outside the fades).
- Not done: freeing a prop when its station locks again (dev Reset only); the prop images baked to assets; captures of a prop sword.
- Later items as the brief listed: #1, #4, #5, #7, #10, #13, #14, #15.

## Seen, not changed

- `StarterGui.UIFX_P` (DisplayOrder 100) and, earlier, `STN_P_Anvil` (20001) plus a polish HUD preview: other agents' preview ScreenGuis in StarterGui. Play copies anything in StarterGui. `ShowDevelopmentGui` was on when they were in use; I turned it off after my capture.
- `ForgeController.showReady` sets the slot's `Material` to Neon locally. The server's later `Material = SmoothPlastic` doesn't replicate when the server's value is already SmoothPlastic, so the owner's next ingot in that furnace probably starts as Neon. Pre-existing; check in Play.
- ForgeService, Hotbar and TycoonController were being edited by other agents at the same time. My edits were exact-string edits and didn't overlap theirs.

## What to test in Play

1. Hotbar: swords and ingots look as before, with the white rim intact (including the katana tip at the top edge), on the bar and in the bag, on desktop and at phone scale.
2. A new player's join: smooth first seconds. Etching Table and Polishing Station props appear with their etches and shimmer when the station is bought.
3. The FallingStars props (Etching Table: katana; Etching Table 2: gladius) and the WovenWind wakizashi now show their etch; the output has no "no bake for E|…|Falling Stars" warning.
4. Ore rolls: your own always animate. A neighbour's roll animates when you're within about 120 studs, and from far away its ores simply appear. Walk over mid-roll and it picks up. With Reduce Motion or Shake off, Epic+ rolls give no camera punch; with Vibration off, no rumble.
5. Shop holder markers on your plot: +, bag, E and taking a sword back all work. Another plot's holders show nothing. Markers come back after streaming out and back in.
6. Furnaces: the ingot warms to orange and its light brightens as before, also on other plots, after a rejoin mid-heat and for the crafter's ingots. Board timers still count.
7. Pads, bought items building themselves in, and holder pops all behave as before (TycoonController guard).
8. Developer Console: `DataReceiveKbps` while three ingots heat should be lower than before.

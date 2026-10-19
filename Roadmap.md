---
title: Sell Swords! — Roadmap
status: active
tags: [roadmap, create-swords]
---

# Sell Swords! — Roadmap

From [[Create Swords! GDD]] to a playable game. Phases match GDD §14. Tick boxes as work lands; log choices in [[Decisions Log]]. Where the code lives: [[Code Map]].

## Phase 0 — POC: the anvil (do this first)

Goal: hammering a blank to match a silhouette feels good, and the score is right. Nothing else.

- [x] **Project setup:** code lives directly in the Studio place, edited through the Studio MCP (no Rojo/Git; see [[Decisions Log]]). Strict Luau.
- [x] **Blade profile module** (`ReplicatedStorage.Shared.BladeProfile`): 40 columns of left/right half-widths, `hit(side, column, hammer)` with cosine falloff, undo/redo, reset, server `replay(hits)` with hit validation
- [x] **Scoring module** (`ReplicatedStorage.Shared.AnvilScore`): accuracy % and smoothness %, Finish at 80%, quality shown as the % (grade names dropped 2026-10-18); self-check in `ServerStorage.Tests.AnvilSelfCheck`
- [x] **2 blueprints** (`ReplicatedStorage.Shared.Blueprints`): Dagger and Shortsword target profiles
- [x] **Anvil scene:** anvil model (`Workspace.Smithy.Anvil`, blockout), E to Forge locks the camera over the blade, Q / Leave button exits
- [x] **Blade rendering:** smooth EditableMesh blade (`Shared/BladeMesh`): spine and bevels (ground sharp on Finish), pointed tips, accent lines (bevel lines + fuller) on finished swords, material colour; click/tap a side of the blade to hammer it
- [x] **Silhouette panel UI** (`StarterGui.AnvilHud`): Target (white) vs Yours (orange) lines, Accuracy bar with a Finish tick at 80%, hammer picker (Heavy / Normal / Fine, keys 1-3), Undo / Redo / Reset (Z / Y), blueprint picker, Finish (enabled at 80%, shows the grade)
- [x] **Juice:** sparks, clang sound, small camera shake per hit, all scaled by hammer (`JUICE` table in AnvilController)
- [x] **Shaping prototypes** (see [[Decisions Log]]): Trace (concept 1), Clicks (concept 2), Points (concept 3; **guided since 2026-10-18**: fixed point, the blade slides, turns and flips under it; the default for now) as switchable modes at the anvil (Mode button / M), all fed by the forge (see Forge v2). Pick the winner in the playtest.
- [x] **Ore Roller:** hold E to roll a random ingot (all 13 materials, GDD odds), carried as an item (max 6 for now)
- [x] **Forge v2:** E opens a window: put a cold ingot in (2 shared slots), live timer, take it out hot after 15 s; every anvil mode needs a hot ingot, chosen from the anvil's ingot window
- [x] **Materials** (`Shared/Materials`): rarity multiplies value and the material colours the blade
- [x] **Katana** blueprint (held edge-forward); redrawn 2026-10-18 from real proportions with a smooth curve and a pointed kissaki
- [x] **Server check:** Finish sends the shaping data; `SmithService` re-grades it with `FinishCheck` (Silhouette hit replay, Trace segment replay; Points hit count is trusted for now)
- [x] **Hilt Bench** (pulled forward from Phase 4): carried blades + unlockable hilts → completed sword Tool in the inventory, kept across respawns
- [ ] **Playtest:** 3–5 people try it; guided Points against hand-forging Silhouette: time each sword, ask which felt best; tune hammer strength, cooling, grind bite, and Points' move time (0.3 s) and point life (2 s)

## Phase 1 — Vertical slice (one full loop)

- [ ] ~~Quench barrel with timer~~ (dropped 2026-10-17: the forge is the only timed step)
- [x] **Seat the hilt** step at the Hilt Bench (three timed taps on a sweeping marker, +2% each, click or Space)
- [x] **Sword holders:** "+ Display a sword" prompt on each empty holder opens a picker of your completed swords (replaces "hold a sword + E")
- [ ] Polish station (coverage minigame)
- [x] Display rack + price tags (3 shared holders; F to take back). Art pass: concept art shows separate holders with the blade down ([[Player Plot Concept Art]])
- [x] 3 NPCs (Farmer, Knight, Adventurer) walk in, inspect, offer; accept/decline, with haggling (raise or leave)
- [x] Coins (leaderstats, session-only) + value formula (GDD §6.4)
- [ ] Saving (session-locked DataStore)

## Phase 2 — Shop tycoon

- [ ] Blueprint shop (Longsword, Cutlass, Claymore…; Katana is already in the anvil picker, free for now)
- [ ] Lucky Roller, Material Index (the full 13-material table is done)
- [ ] Haggling (patience, counter-offers), reputation
- [ ] Coin upgrades: more sword holders, more forge slots, faster heating, ingot storage
- [ ] 6-plot village, plot assignment on join (max 6 players); spacious plots with room for upgrades ([[Player Plot Concept Art]] v2)
- [x] Shop building model: log cabin, enterable, 36.5 × 28.5 stud floor (`Models/SwordShop.fbx`, Blockbench). Next: import into Studio, set collision, move the display rack inside

## Phase 3 — Phone & gems

- [ ] Phone UI, commission texts with target picture
- [ ] Gems, gem upgrades (customers, special customers, clients, regulars)
- [ ] Special NPCs (Ninja, Noble, Dragon Slayer)
- [ ] Robux products (GDD §15)

## Phase 4 — Automation & launch polish

- [ ] Cashier, Apprentice Smith
- [ ] Remaining finishes (etching, gem socket); the hilt is done
- [ ] Art pass, sounds, tutorial, thumbnails/icon
- [x] **Picker UI** from the Figma designs ([[UI Design]]): one shared picker for the forge, anvil, sword holders and Hilt Bench, plus the forge timer label, toasts and "Forge is full" (built in Studio 2026-10-18)
- [ ] Rest of the UI pass: anvil panel, offer card, seat-the-hilt panel polish, HUD
- [ ] Public test, then launch

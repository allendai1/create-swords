---
title: Sell Swords! — Roadmap
status: historical snapshot
tags: [roadmap, create-swords]
type: archive
---

# Sell Swords! — Roadmap

From [[Design/Game Design Document|Game Design Document]] to a playable game. Phases match GDD §14. Tick boxes as work lands; log choices in [[Design/Decisions Log|Decisions Log]]. Where the code lives: [[Development/Code Map|Code Map]].

## Current revision — 2026-10-19

**Browser tantō study built (2026-10-19), awaiting Allen's review:** `Prototypes/tanto-forge/` runs the 12-strike forge to 90% and optional grinding to 100%, with reusable profile data and 19 passing core tests. Pacing and proportions are exploratory. Review questions in [[Current Status|Current Status]].

The approved [[Design/Game Design Document|Game Design Document]] v0.3 supersedes conflicting tasks below. Checked boxes in the historical phase list record earlier prototype work; they do not mean the new direction is implemented.

- [ ] After the Iron Wakizashi delivery, introduce buying a **second material stand for the Ore Roller** as the first workshop upgrade (price pending).
- [ ] Commission delivery: select the completed sword through the commission picker and pay the agreed reward; no display listing or haggling.
- [ ] After the first tantō sale, introduce the wakizashi teaching commission and provide its blueprint at commission start; request an **Iron Wakizashi at 90% quality or higher** (grinding optional), using Iron from the starter Ore Roller’s Common pool.
- [ ] Tutorial sales: guaranteed fair offer on the first sale; introduce haggling on the second ordinary shop sale (commission delivery is separate).
- [ ] Tutorial: suppress customer visits during the first craft; listing the first sword triggers the first customer arrival.
- [ ] One shared lever rolls all empty material stands together through an ore-appearance roulette lasting under five seconds. Occupied stands keep their ores and cannot roll until collected. Each new roller upgrade adds a stand, not a lever; no automatic restart.
- [ ] Set base forge heating to **10 seconds** (previous prototype: 15 seconds).
- [ ] Untimed forging circles: all circles required, each improves quality, completion = 90%; remove misses and cooling countdown.
- [ ] Use a shared hit count initially; tune modest additional effort for higher-tier swords later without adding timing pressure.
- [ ] Slightly angled overhead forging camera; frame the entire blade through lengthening and repositioning.
- [ ] Staged shaping animation: lengthen the blank, establish taper/curve, then form the point and refine the outline; quick, smooth localized deformation at hammer contact, blending into neighboring metal; automatic blade slides, turns, and flips without visible tongs.
- [ ] Optional safe grinding: only remove excess metal, never decrease quality, maximum 100%.
- [ ] Replace timed hilt seating with three untimed taps.
- [ ] Start with the tantō blueprint and on-screen guidance; later local commissions introduce wakizashi → katana, with patterns provided at request start.
- [ ] Tradition-matched fittings unlocked by crafting milestones.
- [ ] Open-front Japanese workshop and one-building upgrade progression; replace medieval cabin art direction.
- [ ] Primarily local customers and early special outsider; stock-influenced regulars and reputation-gated special visitors.
- [ ] In-person and letter commissions; untimed special requests; familiarity and personal chains.
- [ ] New traditions introduced by visitor commissions, further blueprints bought with coins.
- [ ] Functional facility bonuses with cosmetic-only decoration; retain cashier and apprentice.
- [ ] Review proposed onboarding in [[Design/Core Loop Review|Core Loop Review]] before implementing its interaction and pacing recommendations.
- [ ] Playtest the revised loop, including the fifth sword and optional-grinding economy; implement saving.

## Historical implementation phases

Retained for implementation provenance. Superseded mechanics are not current requirements.

## Phase 0 — POC: the anvil (do this first)

Goal: hammering a blank to match a silhouette feels good, and the score is right. Nothing else.

- [x] **Project setup:** code lives directly in the Studio place, edited through the Studio MCP (no Rojo/Git; see [[Design/Decisions Log|Decisions Log]]). Strict Luau.
- [x] **Blade profile module** (`ReplicatedStorage.Shared.BladeProfile`): 40 columns of left/right half-widths, `hit(side, column, hammer)` with cosine falloff, undo/redo, reset, server `replay(hits)` with hit validation
- [x] **Scoring module** (`ReplicatedStorage.Shared.AnvilScore`): accuracy % and smoothness %, Finish at 80%, quality shown as the % (grade names dropped 2026-10-18); self-check in `ServerStorage.Tests.AnvilSelfCheck`
- [x] **2 blueprints** (`ReplicatedStorage.Shared.Blueprints`): Dagger and Shortsword target profiles
- [x] **Anvil scene:** anvil model (`Workspace.Smithy.Anvil`, blockout), E to Forge locks the camera over the blade, Q / Leave button exits
- [x] **Blade rendering:** smooth EditableMesh blade (`Shared/BladeMesh`): spine and bevels (ground sharp on Finish), pointed tips, accent lines (bevel lines + fuller) on finished swords, material colour; click/tap a side of the blade to hammer it
- [x] **Silhouette panel UI** (`StarterGui.AnvilHud`): Target (white) vs Yours (orange) lines, Accuracy bar with a Finish tick at 80%, hammer picker (Heavy / Normal / Fine, keys 1-3), Undo / Redo / Reset (Z / Y), blueprint picker, Finish (enabled at 80%, shows the grade)
- [x] **Juice:** sparks, clang sound, small camera shake per hit, all scaled by hammer (`JUICE` table in AnvilController)
- [x] **Shaping prototypes** (see [[Design/Decisions Log|Decisions Log]]): Trace (concept 1), Clicks (concept 2), Points (concept 3; **guided since 2026-10-18**: fixed point, the blade slides, turns and flips under it; the default for now) as switchable modes at the anvil (Mode button / M), all fed by the forge (see Forge v2). Pick the winner in the playtest.
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
- [x] Display rack + price tags (3 shared holders; F to take back). Art pass: concept art shows separate holders with the blade down ([[Archive/Player Plot Concept Art|Player Plot Concept Art]])
- [x] 3 NPCs (Farmer, Knight, Adventurer) walk in, inspect, offer; accept/decline, with haggling (raise or leave)
- [x] Coins (leaderstats, session-only) + value formula (GDD §6.4)
- [ ] Saving (session-locked DataStore)

## Phase 2 — Shop tycoon

- [ ] Blueprint shop (Longsword, Cutlass, Claymore…; Katana is already in the anvil picker, free for now)
- [ ] Lucky Roller, Material Index (the full 13-material table is done)
- [ ] Haggling (patience, counter-offers), reputation
- [ ] Coin upgrades: more sword holders, more forge slots, faster heating, ingot storage
- [ ] 6-plot village, plot assignment on join (max 6 players); spacious plots with room for upgrades ([[Archive/Player Plot Concept Art|Player Plot Concept Art]] v2)
- [x] Shop building model: log cabin, enterable, 36.5 × 28.5 stud floor (`Models/Archive/SwordShop.fbx`, Blockbench). Historical asset; superseded by the Japanese workshop, do not import as the target design

## Phase 3 — Commissions & gems

- [ ] In-person and letter commissions with target picture (replaces phone UI)
- [ ] Gems, gem upgrades (customers, special customers, clients, regulars)
- [ ] Special NPCs (Ninja, Noble, Dragon Slayer)
- [ ] Robux products (GDD §15)

## Phase 4 — Automation & launch polish

- [ ] Cashier, Apprentice Smith
- [ ] Remaining finishes (etching, gem socket); the hilt is done
- [ ] Art pass, sounds, tutorial, thumbnails/icon
- [x] **Picker UI** from the Figma designs ([[Art/UI Design|UI Design]]): one shared picker for the forge, anvil, sword holders and Hilt Bench, plus the forge timer label, toasts and "Forge is full" (built in Studio 2026-10-18)
- [ ] Rest of the UI pass: anvil panel, offer card, seat-the-hilt panel polish, HUD
- [ ] Public test, then launch

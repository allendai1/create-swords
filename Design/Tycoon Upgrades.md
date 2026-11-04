---
title: Tycoon Upgrades
status: built in Edit — the catalogue as exported 2026-11-01 16:31; not played as a whole
type: design
updated: 2026-11-01
tags: [design, tycoon, upgrades, shop, create-swords]
---

# Tycoon Upgrades

Every coin purchase on a plot, as `Shared.Upgrades` stands in the place. The table is generated from the simulator's export, `Development/sim/balance.json` (2026-11-01 16:31), so it matches the game at that time. Rerun the export before trusting it after a price change. How the prices were picked: [[Design/Economy Pass 2]], [[Design/Economy Review — 2026-10-29]] and the sim runs in `Development/Sim Runs/`. The proposed reorder is [[Design/Upgrade Tree Review — 2026-11-01]] (not built).

Older versions: [[Archive/Design/Tycoon Upgrades before update — 2026-11-01]] (the 2026-10-24 note with each change's history) and [[Archive/Design/Tycoon Upgrades before cleanup — 2026-10-22]].

## How it works

- **Floor pads.** Walk onto a pad and press its **Buy** button; touching alone doesn't buy. The server checks owner, distance, gates and coins. Short of coins, the pack that covers it is offered ([[Sessions/2026-10-28#Short of coins or gems: offer the pack that covers it]]).
- **Only a few pads at once.** Of the chains you haven't started, only the **3 cheapest** put a pad on the floor (`PAD_CAP`). A chain you've started always shows its next pad, and so do the next sword and the pads in `PAD_ALWAYS` (the Delivery Cart and the Sword Crafter; Anvil 2 until 2026-11-02). About 9–10 pads stand in the first hours. Allen: "Keep the cap" ([[Sessions/2026-10-30#Refinements, Allen's answers (evening)]]); since 2026-10-31 it counts only new chains, so a started chain's dearer next level no longer drops off ([[Design/Reviews 2026-10-31/Handoff — Upgrade progression]]).
- **Labels.** One line, "Name · price", within 22 studs. Bays add an effect line ("+1 customer at once", [[Sessions/2026-11-01#Untitled 3 fixes: crew, Auto-Roll, signs, bays, NPC paths]]).
- **Building.** A bought item flies together piece by piece on your screen ([[Sessions/2026-10-28#Bought upgrades build themselves]]); the pad rings with confetti and the station reacts ([[Sessions/2026-10-30#Upgrade purchase effects]]).
- **Saving.** Upgrades are saved and re-bought on whichever lot you get next time ([[Development/Saving]]).
- **Not on pads:** decorations (bought and placed in Decorate mode, [[Sessions/2026-10-29#Decorate mode: walk around and press +]]; **hidden for a later release** since 2026-10-30, Allen: "Hide the decorate feature for later release", [[Sessions/2026-10-30#Fixes]]); delivery Capacity and Speed (the Deliveries window); crafters after the first (hire cards in the Crew window); Robux passes (the Shop page and their spots in the world, [[Design/Monetization Plan]]).

## Starting plot

The Tantō, one ore slot, Furnace 1, Your Anvil (the hilt goes on at the anvil; the Hilt Bench was removed on 2026-10-28), the first wall rack and the mailbox. Everything else is bought.

## Catalogue

"→" means the next one waits for the one before it; ";" starts a separate chain in the same group. Gates other than the one before are in brackets.

| Group | Upgrades in order: price in coins (other gates) |
|---|---|
| Ore | Ore Slot 2 80 (75 until 2026-11-02) → Ore Slot 3 280 → Ore Slot 4 2,000 → Ore Slot 5 9,800 → Ore Slot 6 20,000 → Merge Ore Slots free; after merges each costs ×1.5 per merge, to the nearest 10 |
| Swords | Wakizashi Sword 60 → Machete Sword 360 → Katana Sword 1,300 → Scimitar Sword 3,600 → Longsword 10,200 → Cutlass Sword 26,000 → Falchion Sword 28,000 → Jian Sword 50,000 → Gladius Sword 60,000 → Khopesh Sword 150,000 → Dadao Sword 160,000 → Rapier Sword 270,000 → Hook Sword 290,000 → Crescent Fang Sword 370,000 → Shard Blade 400,000 → Moonbite Sword 530,000 → Serpent Sword 570,000 → Leviathan Cleaver Sword 640,000 → Thornspire Sword 740,000 → Seraph Sword 840,000 |
| Big swords | Zanbatō Sword 88,000 (after Gladius Sword, Big Sword Stand) → Claymore Sword 340,000 → Flamberge Sword 430,000 |
| Heating | Faster Heating I 580 → Faster Heating II 3,000 → Faster Heating III 5,200 |
| Furnace 2 | Furnace 2 2,800 → Furnace 2 Heating I 1,800 → Furnace 2 Heating II 9,000 → Furnace 2 Heating III 15,600 |
| Anvils and the first crafter | Sword Crafter 2,000 with Anvil 2 included (after Ingot Rack, Sword Rack; since 2026-11-02, was Anvil 2 3,400 after Ingot Rack, Furnace 2, Sword Rack → Sword Crafter 20,000) → Anvil 3 14,000 → Anvil 4 22,000; Furnace 3 11,600 (after Anvil 3) |
| Furnace 3 heating | Furnace 3 Heating I 7,000 (after Furnace 3) → Furnace 3 Heating II 36,000 → Furnace 3 Heating III 62,000 |
| Faster Strikes | Faster Strikes I 500 → Faster Strikes II 2,000 → Faster Strikes III 5,000 → Faster Strikes IV 10,000 → Faster Strikes V 20,000 |
| Finishing | Polishing Station 30 → Etching Table 1,580 → Polishing Station 2 5,000 (after Polishing Station) → Polish Boost I 4,000 → Polish Boost II 16,000 → Polish Boost III 50,000; Etching Table 2 240,000 (after Etching Table, Flame Etch) → Sword Etcher 270,000 |
| Storage | Ingot Rack 460 → Ingot Rack 2 2,000 → Ingot Rack 3 8,000 → Ingot Rack 4 30,000 (2026-11-03); Sword Rack 280 → Sword Rack 2 2,600 |
| Staff | Stocker 12,000 (after Sword Crafter); Shop Promoter 40,000 (after Sword Crafter); Cashier 50,000 (after Upgraded Store, Sword Crafter) |
| Shop | Wall Sword Rack 2 110 (106 until 2026-11-02) → Display Table 1 440 → Back Wall Rack 900, and Display Table 2 9,000 → Display Table 3 42,000 → Display Table 4 46,000 on the starter floor; Upgraded Store 15,000 after all four (since 2026-11-02; it came after the first three) → Wall Sword Rack 3 6,400 → Wall Sword Rack 4 30,000; Display Table 5 80,000 (after Table 4 and the store) → Display Table 6 120,000 |
| Big Sword Stands | Big Sword Stand 36,000 (after Upgraded Store) → Big Sword Stand 2 90,000 → Big Sword Stand 3 140,000 |
| Bays | Bay 1 2,200 → Bay 2 44,000 → Bay 3 152,000 |
| Delivery | Delivery Cart 6,200 |
| Decorations (Decorate mode, hidden for now; no pads) | Planters 150; Wall Scroll 300; Paper Lamp 600; Bonsai Pine 1,000; Stone Lanterns 1,800; Shop Banners 3,000 |

**Merge Ore Slots** puts Slots 2–6 back to unbought for luck ×(1 + 0.5 × merges); each merge makes the Ore Slots ×1.5 dearer. Repeatable.

**Crew window hires** (coins plus gems): Haru 23,000 + 10 (after Furnace 3), Mei 70,000 + 25 (after Anvil 4), Kenji 460,000 + 40 (after Mei), Taru 710,000 + 80 (after Kenji; id `rin`). Crew levels top out at Lv. 5 and can be bought with gems.

**Deliveries window:** Capacity 6 → 9 → 12 → 15 for 1,500 / 25,000 / 64,000; Speed 2,400 / 40,000 / 55,000 / 76,000. No gates past the cart since 2026-11-02.

## Layout

- **The smithy is outside** since 2026-10-28: the workshop's walls and roof are gone, and the stations stand round an open yard behind the shop ([[Sessions/2026-10-28#The outside smithy, built]]). Furnaces 1–3 and the ingot racks down one side, Your Anvil and the crew's Anvils 2–4 across the back, polishing and the etching tables up the other side.
- **The ore roller** is in the middle of the yard, turned so its lever faces the shop; the Ore Slot and Merge pads go with it ([[Sessions/2026-10-29#Ore Roller to the middle of the yard]], [[Sessions/2026-11-01#Taru, the lamp, Air, the bag, two more Big Sword Stands, the Ore Slot pad]]).
- **Sword pads:** the 20 ordinary swords share one spot in front of Your Anvil, one pad at a time; the 3 big swords share the spot beside it ([[Sessions/2026-10-30#One sword chain in the game]]).
- **Upgraded Store** deepens the shop and still pushes what stands behind it 12 studs back. Big Sword Stands 2–3 go on its side walls between the wall racks.
- Plots are bigger with a fence since 2026-10-26 ([[Sessions/2026-10-26#Bigger plots with a fence]]); six of them, see [[Design/Six Plots]].

## Open

- **Gates since 2026-11-02:** an upgrade waits only for the one before it in its line, or for what it's used with; swords gate only swords; staff wait for the Sword Crafter ([[Design/Upgrade Tree Review — 2026-11-01#Overhaul proposal — 2026-11-02]], [[Sessions/2026-11-02#Upgrade overhaul built]]). Not played yet.
- The sim still shows a trough after the Zanbatō: 22 ordinary buys and 6 milestones across 4–20 h ([[Design/Upgrade Time Model — 2026-11-02]]).
- None of this order has been played start to finish. [[Development/Roadmap]] has the Play checks.

References: [[Development/Code Map]], [[Art/Workshop Layout]], [[Art/Ore Loot Box]], `Development/Upgrade Tree.html` (the tree drawn from the export).
- **Every price ends in 0 (2026-11-02):** Allen: "Upgrades in the game should try to end in 0 ... round up or down to the nearest 10". Ore Slot 2 80, Wall Sword Rack 2 110; `Upgrades.price` rounds merged Ore Slots to the nearest 10 (SaveSpec checks every price at 0–5 merges).

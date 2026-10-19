---
title: Sell Swords! — Game Design Document
status: draft v0.2
source: "[[Create Swords!]]"
tags: [gdd, roblox, create-swords]
---

# Sell Swords! — Game Design Document

*Working title: **Sell Swords!** (alternatives were Create Swords! and Craft Swords!).*

> Refined from the original brainstorm in [[Create Swords!]]. The brainstorm is left untouched; this note is the working design.
> Decisions Allen has made are logged in [[#13. Decisions log]].

---

## 1. One-line pitch

**Forge swords by hand, sell them to colorful heroes from your village shop, and grow a tiny smithy into a legendary forge.**

A cozy crafting tycoon in the style of *Create Pottery!*, where the pottery wheel becomes an anvil and clay becomes metal.

## 2. Pillars

1. **The hammer feels good.** Shaping a sword on the anvil is the heart of the game; every hit should be satisfying (sparks, sound, visible dent).
2. **Skill shows up in the price.** A better silhouette, a rarer metal and more finishing work always mean more money, and the player can see why.
3. **Every customer is a little story.** NPCs are recognizable characters with tastes, so selling feels like matchmaking, not a menu.
4. **Always something to unlock next.** A short loop (a few minutes per sword) feeding a long tycoon progression.

## 3. Target & platform

- **Platform:** Roblox (PC, mobile, console). All interactions must work with touch: the anvil minigame is tap/click based.
- **Audience:** 9–16, fans of *Create Pottery!*, cozy tycoons and simulator games.
- **Session:** 10–30 minutes, with offline-friendly quench timers that reward coming back.

## 4. Core loop

*Updated 2026-10-17 from Allen's start-to-finish loop in [[Create Swords!]].*

```
 Roll ingot ──► Forge (drop in, ~15 s) ──► Anvil: pick ingot + blueprint, shape ──► Hilt Bench: pick hilt, seat it
     ▲                                                                                        │
     │                                                                                        ▼
 Upgrades ◄── Coins (& gems) ◄── NPC browses, offers, haggles ◄── Sword holder (+ → pick a sword) ◄── Inventory
                     ▲
                     └── Phone commissions (made-to-order swords for gems, later)
```

| Step | Station | What the player does |
|---|---|---|
| 1. Roll ingot | **Ore Roller** (generator) | Roll a random material block (e.g. Iron, Common). Material rarity multiplies the sword's value (§6.1). |
| 2. Heat | **Forge** | E opens the forge window: a row of your ingot cards. Tap one and the window closes and the forge starts heating it (~15 s, faster with upgrades; more forge slots later). The ingot glows in the fire, a toast says "Ingot loaded", and a small label above the forge shows "Iron · Heating" with a bar and the seconds left; when it's done it reads "Ready to collect" and a **Take out** (E) prompt appears on the forge. If both slots are busy, E doesn't open the window and a quick "Forge is full" message shows instead. No skill. The only timed step (the old quench/temper step is dropped). |
| 3. Shape | **Anvil** | E opens the hot-ingot picker, then the shape picker ("Choose a shape to make.": every blueprint as a black blade silhouette with stars and its price in that metal); pick one, pick the blueprint, then shape it (§5; shaping mode still being chosen between the prototypes). |
| 4. Hilt | **Hilt Bench** | E opens the picker twice: "Choose a blade.", then "Choose a hilt." (locked hilts dimmed with their unlock count). Then **seat the hilt**: three timed hammer taps on the pommel, a small bonus for good timing (~3 s). The sword is now complete. |
| 5. Inventory | Toolbar / backpack | Completed swords go to the toolbar; extras go in the backpack (Roblox's built-in backpack for now). |
| 6. Display | **Sword holders** in the shop | Use **"+ Display a sword"** (E) on a free holder and pick a sword from your toolbar/backpack; it goes on display with a price tag (hold F to take it back). More holders is an upgrade. |
| 7. Sell | Shop floor | NPCs walk in, browse, inspect and make an offer; accept, decline or haggle (§8). |
| 8. Upgrade | Shop / phone | Spend coins on more holders, forge slots and speed, better roll odds, new blueprints and hilts. That closes the loop. |

Built (2026-10-17): the Ore Roller (hold E 1.5 s, odds as in §6.1) and the forge (2 shared slots, 15 s, owner-only collect). Material multiplies value and colours the blade. Carried ingots are capped at 6 and hot ingots don't cool for now.

Still open: blueprint prices (Allen's loop says Dagger ≈ 50, §6.2 says 20), where spare ingots and blades are stored, and whether a hot ingot cools if left out.

## 5. The anvil (core minigame, the POC)

Reference: ![[References/clay silhouette goal.png]]

**Setup.** The player brings an ingot (a rectangle) to the anvil and picks a blueprint. A panel on the left shows the **Target** silhouette (white) with **Yours** (orange) overlaid, exactly like the pottery panel. The 3D blade sits in front of the camera.

**Strike point (2026-10-18).** In every mode where you tap, the hammer always lands on the middle of the anvil face. When you tap a part of the blade, the blade slides there (0.1 s) as a hammer swings down onto it, so a tap looks like hammering that exact part; sparks, clang and shake land on impact. In Points the blade is slid, turned and flipped under a fixed point (see Concept 3, guided). Grinding and Trace's cut don't move the blade.

**Hand-forging rework (2026-10-18).** Modelled on how a sword is really made: hammer the hot metal close to shape, grind the edges to the exact outline (that's also where mistakes get fixed), and reheat when it cools.
- **Hammer [1–3]:** blows dent the edges toward the white target line drawn on the metal. Heavy and Normal blows are much stronger now, so the rough shape takes about 15–25 blows.
- **Grind [4]:** drag along an edge to grind it down to the line you drag. Works on cold metal. Each pass bites at most 0.3 of the blank's half-width, so a slip is small; a whole stroke undoes as one step.
- **Heat:** each blow cools the metal (Heavy 7%, Normal 5%, Fine 2%, so about 15–20 blows per heat). Cold metal can't be hammered; grind it or **Reheat (R)**, which takes 3 s at the anvil for now.
- Undo / Redo / free Reset stay, so a blade is never lost.

**Input.** The player hammers the **edges** of the blank. Each hit:
- dents the silhouette inward at the hit point with a soft falloff (neighbouring columns move a little less);
- has a **strength** chosen by the hammer tool (like the pottery "Fine / Precise" tool picker): *Heavy* (big dents, fast), *Normal*, *Fine* (small, precise dents);
- spawns sparks, a clang and a tiny camera shake.

**Shaping model (for implementation).** The blade is a 2D profile: an array of N columns along the blade's length, each storing a half-width (left and right edges can be separate if blueprints are asymmetric, e.g. katana curve). A hit at column *i* subtracts `strength × falloff(distance)` from nearby columns. Metal can't be added back, but **a blade is never lost**: the player can **Undo/Redo** individual hits or **Reset** the blank to its original rectangle at no cost (same as the pottery wheel). Over-hammering only costs time.

**Scoring.**
- **Accuracy %** = 1 − (area of mismatch ÷ target area), clamped 0–100.
- **Smoothness %**: penalises jagged neighbouring columns (pottery shows "Shape" and "Smooth" separately; we merge them into one bar for readability but keep both under the hood).
- The player can press **Finish** at any time once Accuracy ≥ **80%**.
- **Quality is just the percentage** (Allen, 2026-10-18): no grade names. A blade is "Iron Dagger (92%)". The price multiplier grows smoothly from **×1.0 at 80%** to **×2.0 at 100%** (90% = ×1.5).

**Alternatives under test (2026-10-17).** Three other shaping concepts from [[Create Swords!]] will be prototyped as switchable modes and compared with this one in playtest: (1) hammer the blank bigger than the guide, then trace-cut the outline; (2) eight clicks shape it automatically, quality comes only from material and finishes; (3) osu-style points within 10 s, a minimum number of hits gives a lower-grade, imperfect sword. All three start at a **forge station** (no skill), and putting a sword back in the forge resets it to the blank. See [[Decisions Log]].

**Concept 3, Points, guided (Allen, 2026-10-18).** The point never moves; the blade is moved under it like a smith working the piece. Tap the hot metal to start; it cools in 10 s. 12 points appear one at a time on the fixed strike point while the blade slides into place (0.3 s): the near edge hilt to tip (6 parts), the blade **flips over**, the far edge tip back to hilt, and the two parts nearest the tip are presented with the blade **turned 90°** (pointing up the screen).
- Strike once the blade has stopped (the point turns solid): tap or click anywhere, or Space / gamepad A. A strike while it's still moving is a miss (so mashing doesn't work); a point that shrinks away (2 s) is a miss; points the metal cools before are misses.
- Each hit dents **that part** to the target (neighbouring parts blend smoothly); a miss leaves it wide. This replaces the earlier "partly formed" even morph.
- 6+ hits make a sword; its quality is the share hit (10 of 12 = 83%). Fewer and you tap the metal to start over (the ingot stays hot).
- The server rebuilds the shape from which points were hit; the timing itself is trusted.
- A separate "Hot spots" mode (concept 4, same idea with timing tiers) was built earlier the same day and merged into this.

**Accent lines.** When a sword is finished it automatically gets ridge lines and, if its blueprint has one, a fuller (groove) down the middle. The ridge (the thickest part, where the bevels to each edge start) sits across the blade's own width (the middle 60% by default) on a smoothed path, so the lines run clean instead of copying every hammer dent; the lines are a slightly darker shade of the blade's metal. The Katana has one ridge line about a third of the way in from the spine (its shinogi) and a short yokote line across the blade where the point begins.

**No timer.** Shaping is untimed, like the pottery wheel: nothing runs out while you think. Since 2026-10-18 the metal cools per hammer blow (not over time) and you reheat to keep hammering (see the hand-forging rework above).

## 6. Materials, blueprints & finishes

### 6.1 Materials (rolled at the Ore Roller)

| Rarity | Examples | Base multiplier | Roll odds (starting) |
|---|---|---|---|
| Common | Iron, Copper, Stone | ×1 | 60% |
| Uncommon | Steel, Bronze | ×1.5 | 25% |
| Rare | Blue Steel, Silver | ×2.5 | 10% |
| Epic | Gold, Obsidian, Damascus | ×5 | 4% |
| Legendary | Mythril, Starmetal, Rainbow Alloy 🌈 | ×12 | 1% |

- Each material has a distinct texture (Damascus swirls, rainbow shimmer), mirroring *Create Pottery!*'s "Cocoa Swirl / Porcelain" clays.
- "NEW" badge and a small celebration the first time a material is rolled; a **Material Index** (collection book) tracks discoveries.
- Rarer metals take longer to quench/temper.

### 6.2 Blueprints (sword shapes)

Bought with coins; harder silhouettes sell for more.

| Blueprint | Difficulty | Base price | Unlock |
|---|---|---|---|
| Dagger | ★ | 20 | Start |
| Shortsword | ★ | 35 | Start |
| Longsword | ★★ | 60 | Shop |
| Cutlass | ★★ | 75 | Shop |
| Katana | ★★★ (curved) | 110 | Shop (in the anvil picker for now). Drawn from real proportions: ~1.7× real width, smooth curve (~1.9% of length), pointed kissaki over the last 10% |
| Rapier | ★★★ (thin) | 130 | Shop |
| Claymore | ★★★★ | 200 | Shop |
| Flamberge | ★★★★★ (wavy edge) | 350 | Late game |

### 6.3 Finishes (optional value-adds)

| Finish | Station | Minigame | Bonus |
|---|---|---|---|
| **Polish** | Polishing Wheel | Coverage % rub, like pottery glaze | +10% (shiny look) |
| **Color / Enamel** | Etching Table | Paint coverage, pick colours (rainbow = multi-colour) | +10–20%, matches NPC wants |
| **Etching / Rune** | Etching Table | Trace a pattern | +15% |
| **Hilt** | Hilt Bench | Pick a finished blade and an unlocked hilt; quick, no minigame. Completes the sword (see §6.5) | +0% to +40% price by hilt; some NPCs care |
| **Gem Socket** (late) | Hilt Bench | Insert a gem | Large bonus; consumes a gem item |

### 6.4 Sword value formula

```
Value = Blueprint base
      × Material multiplier
      × Quality multiplier (×1.0 at 80% → ×2.0 at 100%)
      × (1 + hilt bonus + other finish bonuses)
      × NPC preference bonus (see §7)
```

The tooltip on a finished sword shows each factor so players learn what to chase.

### 6.5 Hilt Bench (completing a sword)

- Finishing a blade at the anvil adds it to the player's **carried blades** (no limit for now).
- At the **Hilt Bench** the player picks a blade, then a hilt (two pickers in a row), and seats it. The sword is then **complete** and goes to the player's inventory as a sword they can hold. Later it goes on a display rack to sell (Phase 1–2).
- Hilts unlock by **swords completed** (forging milestones) until coins exist; later they can be bought.

| Hilt | Price bonus | Unlocks after |
|---|---|---|
| Wooden Grip | +0% | start |
| Leather Wrap | +5% | 2 swords |
| Iron Crossguard | +10% | 4 swords |
| Bronze Guard | +15% | 7 swords |
| Gold Guard | +25% | 10 swords |
| Gem Pommel | +40% | 15 swords |

## 7. Customers (NPCs)

NPCs walk in from the village road, browse the racks, inspect a sword (pick it up, turn it over), then make an offer.

| NPC | Wants | Pays extra for | Notes |
|---|---|---|---|
| Village Farmer | Anything cheap | — | Common, low offers, tutorial customer |
| Knight | Longsword, Claymore | Polish (shiny), Steel+ | Haggles little |
| Ninja | Katana, Dagger | Colour/Rainbow | Rare; big offers for rainbow katana |
| Pirate | Cutlass | Gold | Haggles hard |
| Noble | Rapier | Gem socket, 98%+ blades | Very high offers, picky |
| Adventurer | Shortsword | Accuracy | Mid-tier regular |
| Dragon Slayer (Special) | Claymore, Legendary metal | Everything | Special customer, gem tips |

- **Preference bonus:** matching a wanted blueprint ×1.25, plus finish/material likes stack.
- **Special customers** have a glow/aura and can tip gems.

## 8. Selling & haggling

1. NPC inspects and offers a price (roughly 80–110% of value, nudged by personality).
2. Player chooses **Accept** or **Decline**.
3. On decline, NPC either:
   - raises the offer (chance based on personality; Pirate rarely, Noble often), or
   - leaves unhappy. Each NPC has a hidden **patience** of 1–3 declines.
4. Accepting fills a small **reputation** meter; reputation raises customer frequency and unlocks special customers.

**Built so far (2026-10-17):** a 3-slot display rack with price tags; customers walk in every 12–22 s while a sword is displayed (max 2 at once). The owner gets an offer card (20 s to answer). Openers: Farmer 70–95% of value (1 decline), Adventurer 85–105% (×1.25 for Shortswords, 2 declines), Knight 90–110% (×1.25 for 90%+ blades, 2 declines). A decline gets a 5–15% raise by chance (30% / 45% / 50%), otherwise they leave.

**Cashier upgrade:** an NPC cashier auto-accepts offers above a threshold the player sets (e.g. "accept ≥ 100% of value").

## 9. Phone & commissions

A smartphone in the HUD (as in *Create Pottery!*).

- **Texts from clients:** "My blade snapped in a duel! Can you make me this?" with a picture of the target sword (blueprint + material + finish requirements).
- Rewards: coins and **gems**; commissions are the main gem source.
- Commissions have a soft timer (more reward if delivered quickly), never a hard fail in early game.
- **Regular clients** re-text periodically and build loyalty (better rewards over time).

## 10. Economy & progression

### 10.1 Currencies

| Currency | Earned from | Spent on |
|---|---|---|
| **Coins** | Selling swords | Blueprints, stations, shop expansions, decor |
| **Gems** | Commissions, special customer tips, Material Index milestones, **Robux purchase** | Customer/client upgrades, Lucky Rolls, timer skips |

### 10.2 Upgrades

**Coin upgrades (smithy & shop):**
- Extra **Ore Roller slot** (2 rolls at once, from pottery's "more space")
- Extra **display racks** and **ingot shelf** space
- Faster **quench** timers
- Better **roll odds** (Lucky Roller I–V)
- New **blueprints** and **finish stations**
- **Shop expansions** (more floor, decor that raises reputation)

**Gem upgrades (customers):**
- **More Customers**: shorter time between walk-ins
- **More Special Customers**: higher chance of special NPCs
- **More Clients**: more simultaneous commissions
- **Regular Clients**: clients text sooner

**Automation (late game):**
- **Cashier**: auto-accept offers (see §8)
- **Apprentice Smith**: auto-forges a chosen blueprint at a set accuracy (e.g. 85%) from shelf ingots, slower than the player. Keeps the shop stocked while the player chases near-perfect blades and commissions.

### 10.3 Progression arc

| Stage | Player has | Goal |
|---|---|---|
| Early (0–30 min) | Roller, anvil, 1 rack, dagger/shortsword | Learn the anvil, first sales, first Uncommon |
| Mid (1–5 h) | Polish + etching, katana/longsword, phone clients | Commissions, gem upgrades, 2nd roller slot |
| Late (5 h+) | Cashier, Apprentice, Claymore/Flamberge | Legendary metals, 98%+ blades, Material Index completion |

## 11. World & multiplayer

- **The village:** **6 players per server**, and the village has **6 house plots** around a central square and road. Each player claims one plot on join, and it becomes their smithy + shop (loaded from their save).
- **The shop building:** a medieval log cabin on a stone foundation with a blue shingle roof and a small porch roof over the door. The inside is 36.5 × 28.5 studs with 14-stud walls, room for sword holders and walking customers (`Models/SwordShop.fbx`).
- NPCs walk the shared road and visit any shop, so players can see each other's storefronts.
- Visiting another player's shop to admire their racks is a light social layer; no player-to-player trading in v1.
- Art direction: low-poly, warm and cozy, matching the pottery references (soft wood, grass, stone paths).

## 12. Technical notes (Roblox)

*Updated 2026-10-17 to match what's built. The full file-by-file map is in [[Code Map]].*

- **Where the code lives:** directly in the Studio place, edited through the Studio MCP (no Rojo/Git).
- **Server-authoritative.** The client runs the anvil minigame for responsiveness, then sends the shaping data (hit list, cut strokes or hit count). The server's `FinishCheck` replays it to compute the grade; it never trusts a client accuracy or price. The server owns ingots, blades, swords, coins, forge slots and the rack.
- **Blade rendering.** A client-side `EditableMesh` (`BladeMesh`) built from the 40-slice outline: spine and bevels, pointed tips, accent lines. Held and displayed swords carry their outline as attributes, and every client draws the mesh (`SwordRenderer`). Check Roblox's EditableMesh rules for published games before launch.
- **Data.** Session-only for now. Next: save coins, gems, ingots, blades, swords, unlocks, material index, upgrades and plot layout with session-locked DataStores.
- **Timers** (forge) use server time; switch to timestamps when saving lands, so they progress while offline.
- **Server size:** max 6 players, one plot each (Phase 2); for now one shared smithy and rack.

## 13. Decisions log

| # | Question | Decision (Allen, 2026-10-17) |
|---|---|---|
| 1 | Name | **Sell Swords!** for now |
| 2 | Does metal cool while hammering? | **No timer**: shaping is untimed, no forge/reheat step |
| 3 | What does "6 houses" mean? | **6 players per server, 6 plots**, one per player |
| 4 | Can a blade be ruined? | **Always recoverable** (undo/redo + free reset) |
| 5 | Can gems be bought with Robux? | **Yes** (see §15) |

Still open: shaping depth (2D outline only vs. thickness/bevel later).

## 14. Build plan

| Phase | Scope | Done when |
|---|---|---|
| **0. POC** | Ore roller (Common/Uncommon only) → anvil minigame with 2 blueprints, Accuracy bar, undo/reset, Finish at 80% | Hammering a blank to match a silhouette feels good and the score is right |
| **1. Vertical slice** | Quench timer, polish finish, 1 display rack, 3 NPCs with accept/decline, coins, saving | A full roll → sell loop works |
| **2. Shop tycoon** | Blueprint shop, upgrades, more NPCs + haggling, reputation, roller slots | 1 hour of progression |
| **3. Phone & gems** | Commissions, gem upgrades, special customers | Gem economy works |
| **4. Automation & polish** | Cashier, Apprentice, Material Index, village plots, juice | Ready for public test |


## 15. Monetization (Robux)

Guiding rule: Robux speeds things up or adds style, but anyone can earn everything by playing.

| Product | Type | What it gives |
|---|---|---|
| Gem packs | Developer product | Gems (same currency earned from commissions) |
| 2× Coins | Game pass | Double coins from sales |
| Auto Cashier | Game pass | Cashier from the start (still unlockable with coins later) |
| VIP Rack | Game pass | Extra golden display rack, NPCs pay +10% there |
| Lucky Roll | Developer product | One roll with boosted rare odds |
| Instant Quench | Developer product | Skip the current quench timer (also purchasable with gems) |

Prices are set during Phase 3 tuning.

---

Related: [[Home]] · [[Roadmap]] · [[Decisions Log]] · [[Create Swords!]] · References: ![[References/Screenshot 2026-10-16 230815.png]]

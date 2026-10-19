---
title: Decisions Log
tags: [decisions, create-swords]
---

# Decisions Log

Every game-direction decision, newest at the bottom. Add a row whenever something is decided (in a Claude thread or on your own) and link the [[Sessions/2026-10-17|session note]] where it happened. The [[Create Swords! GDD]] should always match this log.

| Date | Decision | Why / notes | Where |
|---|---|---|---|
| 2026-10-17 | Working title is **Sell Swords!** | "for now"; alternatives were Create Swords! and Craft Swords! | [[Sessions/2026-10-17]] |
| 2026-10-17 | **No timer** on anvil shaping; no forge/reheat step | Simpler; matches the pottery wheel | [[Sessions/2026-10-17]] |
| 2026-10-17 | **6 players per server, 6 plots**, one per player | | [[Sessions/2026-10-17]] |
| 2026-10-17 | Blades are **always recoverable** (undo/redo + free reset) | Over-hammering only costs time | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Gems can be bought with Robux** | Everything stays earnable by playing (GDD §15) | [[Sessions/2026-10-17]] |
| 2026-10-17 | **No Rojo:** code lives in the Studio place, edited through the Studio MCP | Simpler setup; replaces the Rojo/GitHub item in the [[Roadmap]] | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Prototype and compare** the three new shaping concepts from [[Create Swords!]] against the current silhouette anvil, as switchable modes; keep the winner after playtest | Current anvil stays as the baseline | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Forge is just a station** (put ingot in, wait, take out), no skill | Supersedes "no forge/reheat step" for the new concepts | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Forge resets the blade:** putting a sword back in the forge returns the metal to the rectangular blank | Keeps blades always recoverable | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Concept 3 (osu points, 10 s):** hitting at least a minimum number of points produces a sword with a lower grade and an imperfect shape; you can always reheat to start over | Adds a timer for this mode only | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Concept 2 (8 clicks):** shaping gives no quality; value comes only from material and finishes | | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Concept 3 imperfect shape = "partly formed":** the blade morphs evenly from the rectangular blank toward the target; each hit moves it 1/12 of the way, so misses leave it too wide all over rather than wavy | Chosen over "wobbly all over" and "lumps where you missed" | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Blade is drawn with an EditableMesh** (one smooth mesh, vertices moved after each hit) instead of stacked slices | Stacked slices looked jagged; wedge slices were the fallback. Check Roblox's EditableMesh rules for published games before launch | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Accent lines appear automatically on the finished sword** (bevel lines on every blade; a fuller groove where the blueprint has one), no extra step | Chosen over fuller/etching skill steps; etching at the etching table stays in GDD §6.3 | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Sharpened edges:** blades have a spine and bevels sloping to a thin edge; a light bevel while shaping, ground fully sharp on Finish | Partly answers the shaping-depth question (shaping stays 2D, the look is 3D) | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Hilt Bench**: pick a carried blade + an unlocked hilt, attach (quick, no minigame); the sword is then complete and goes to the inventory as a held Tool | Display/selling to NPCs comes with the shop phase | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Hilts give a % price bonus** (+0% to +40%) and **unlock by swords completed** until coins exist | Replaces the GDD's earlier "+flat value" | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Finished blades go into a carried list** (no limit for now) | A limited blade rack was the alternative | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Shop v1:** one shared 3-slot display rack; the sword's owner gets the offers; coins in leaderstats; Farmer / Adventurer (likes Shortswords) / Knight (likes Fine+ until Longswords exist) | Shared rack until the 6 player plots (Phase 2) | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Blueprints can be traced from Creator Store swords** (option 2); bending store meshes (option 3) is blocked by Roblox for meshes we don't own | First one: Katana from "Sword katana" by Haantoca | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Self-check: ★–★★ blueprints must be Masterwork-reachable by the bot, ★★★+ at least Superior** | Harder silhouettes are meant to be harder (GDD §6.2) | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Core loop (Allen's version):** roll ingot → forge → anvil (pick ingot + blueprint) → Hilt Bench → inventory → sword holder (+ to pick a sword) → NPC sale → upgrades | Replaces the GDD §4 loop | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Forge: drop in, collect later** (~15 s, upgradeable); heating comes before every sword | Supersedes "no forge step" for the main loop | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Quench/temper step dropped**; the forge is the only timed step | Avoids two waits per sword | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Seat the hilt**: three timed hammer taps on the pommel, small bonus for good timing | Quick interactive hilt step | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Roblox's built-in backpack** for the toolbar/inventory for now | Custom 8-slot toolbar later if capacity upgrades are wanted | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Holder + is a proximity prompt** ("+ Display a sword", E) rather than a floating clickable + | Native on keyboard, touch and gamepad, and testable; a clickable floating + can come back in the art pass | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Forge and anvil open a window of your ingots** (forge: put in / take out with timers; anvil: choose a hot ingot), the same picker as the sword holders | Allen: selecting from a window instead of holding the item | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Blades are 0.06 studs thick** (about 1/12 of the blank's width) | The held Dagger looked too thick | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Held swords: upright, sharp edge leading**, flat side sideways | Matches a real katana grip; replaced a flat-forward grip | [[Sessions/2026-10-17]] |
| 2026-10-17 | **UI is designed in Figma first** ([[UI Design]]), starting with the forge window | Style follows the station-kit concept art; Luckiest Guy + Fredoka (both Roblox fonts) | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Forge window is just your ingot cards**: tap one, the window closes and the forge starts heating it. No Put in button, no slots or timers in the window | Allen: the first Figma draft was over-engineered. Replaces "take it out from the same window" | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Window titles name the action** ("PICK AN INGOT"), not the station ("FORGE") | Allen | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Taking a hot ingot out:** a timer floats above the forge while it heats; when done, a native **Take out** (E) prompt appears on the forge | Allen. Chosen over "goes straight to your inventory" | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Forge full:** if both slots are busy, E doesn't open the window; a quick "Forge is full" message shows | Allen. Chosen over greyed-out cards | [[Sessions/2026-10-17]] |
| 2026-10-17 | **One picker style** for every "put something into a station" window (forge, anvil, holders, Hilt Bench): icon + action title + close, row of cards, tap to pick | Allen | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Sword holder and Hilt Bench use the picker style**: "PICK A SWORD" (price tag); Hilt Bench is two pickers in a row, "PICK A BLADE" (grade tag) then "PICK A HILT" (bonus tag) | Allen asked for the same style; showing only unlocked hilts is Claude's default, easy to change | [[Sessions/2026-10-17]] |
| 2026-10-17 | **Dark picker style after *Create Pottery!*'s "Select Wet Pottery" window**: translucent dark panel with dot texture, thin border, Montserrat Title Case titles ("Select Ingot"), ring close button; accents from rarity-glow cards and a title-bar shimmer; empty state with an orange hint | Allen: the first look was too basic and too bright. Replaces the chunky wood/parchment style and the "PICK AN INGOT" wording | [[Sessions/2026-10-17]] |
| 2026-10-18 | **Pickers follow [[UI Concept - Furnace]]**: warm chocolate window, station name + action subtitle ("Forge" / "Choose an ingot to heat."), big 3D item cards, stacked quantities, muted rarity chips, amber hover; after picking a toast "Ingot loaded" + "Iron · Heating" billboard. Locked hilts show dimmed | Allen. The name stays **Forge** (not Furnace) and "Forge is full" stays. Replaces the dot texture, shimmer, rarity glow and "Select Ingot" titles | [[Sessions/2026-10-18]] |
| 2026-10-18 | **Forge Take out uses the same E prompt** ("Use forge" becomes "Take out" when your ingot is ready) instead of a second prompt | Two E prompts at one station would fight over the key | [[Sessions/2026-10-18]] |
| 2026-10-18 | **Gotham font** for the game UI (pickers, toasts, notices, forge timer, seat panel) | Allen. Replaces Fredoka / Nunito in Studio; Figma keeps them since Gotham isn't in Figma | [[Sessions/2026-10-18]] |
| 2026-10-18 | **Anvil: choose the hot ingot first, then the shape** from a picker of black blade silhouettes (priced for that metal) | Allen; replaces shape-first from earlier the same day. Dropping the < > buttons is Claude's default | [[Sessions/2026-10-18]] |
| 2026-10-18 | **Hot spots (concept 4)** prototyped as the main candidate and made the anvil's default mode: timed strikes on glowing parts of the edges, every run makes a sword, timing sets the grade | Allen asked for it after the anvil friction review; the other modes stay switchable (M) for the playtest | [[Sessions/2026-10-18]] |
| 2026-10-18 | **Silhouette becomes hand-forging**: stronger hammer blows, a Grind tool (drag an edge, the fixing step), and heat that drops per blow with Reheat; it's the default anvil mode again | Allen: Hot spots left no room to fix mistakes and didn't feel hand-made; real smithing is hammer, grind, reheat. Supersedes "metal does not cool" for this mode | [[Sessions/2026-10-18]] |
| 2026-10-18 | Reheat happens **at the anvil** (3 s) for now | Prototype shortcut; carrying the blade back to the forge is still open | [[Sessions/2026-10-18]] |
| 2026-10-18 | **Quality is a percentage, no grade names** (no Crude / Fine / Superior / Masterwork). Price multiplier grows smoothly: ×1.0 at 80% → ×2.0 at 100%; the Knight likes 90%+ | Allen: "I don't need the masterwork label. It should just be percentages." Keeping the price link and the smooth curve are Claude's defaults | [[Sessions/2026-10-18]] |
| 2026-10-18 | **Strike point:** in tapping modes the hammer always lands on the anvil face's centre and the blade slides so the tapped part is under it | Allen's idea, so a tap reads as hammering that part of the blade | [[Sessions/2026-10-18]] |
| 2026-10-18 | **Guided Hot spots (option A):** the ring stays fixed on the strike point and the game moves the blade under it: near edge hilt→tip, flip, far edge tip→hilt; tip parts turned 90°. Hot spots is the default anvil mode while Allen tries it | Allen: points stay still, the blade moves, with turns and flips for interest. Chosen over the player dragging the blade (option B). Silhouette keeps free aim | [[Sessions/2026-10-18]] |
| 2026-10-18 | **The fixed-point idea belongs to Points (concept 3)**: Hot spots merged into Points and removed. Points keeps 12 points, 10 s cooling and 6+ hits, now one at a time on the fixed strike point with the blade slid / turned / flipped under it | Allen: "I was thinking of this for the method 3"; chose the merge over varied spots or keeping both | [[Sessions/2026-10-18]] |
| 2026-10-18 | Points: **each hit dents its own part** of the blade (misses leave that part wide); a strike while the blade is still moving is a miss | Follows from "hitting the point = hammering that part"; supersedes the 2026-10-17 "partly formed" even morph for Points. Claude's defaults | [[Sessions/2026-10-18]] |
| 2026-10-18 | **Katana redrawn from real katana proportions** (smooth curve, proper pointed tip, ~1.7× real width so it's playable), replacing the Creator Store trace | Allen: the silhouettes looked off; the trace had a zig-zag spine and a blunt tip. The curve is ~1.9% of the length (real ~2.6%): each edge must stay on its side of the blade's axis, so the axis runs hilt-to-point and held swords turn the blade ~7.6° at the guard | [[Sessions/2026-10-18]] |
| 2026-10-18 | **Accent lines redone**: the ridge sits across the blade's own width on a smoothed path, lines are a darker shade of the metal; the Katana gets a single shinogi ridge (~1/3 from the spine) and a yokote line | Allen: the Katana's line looked like a sharpie: it hugged one edge (measured from the off-centre axis), copied hammer dents and was a fixed dark grey | [[Sessions/2026-10-18]] |

## Open questions

- [x] Quality: no grade names, just the percentage (Allen, 2026-10-18). Price still grows with it (×1.0 at 80% → ×2.0 at 100%).
- [ ] Reheat: stay at the anvil, or carry the blade back to the forge?

- [x] Shaping depth: shaping stays a 2D outline; bevels are automatic (light while shaping, sharp on Finish).
- [ ] Blueprint prices: Dagger ≈ 50 (core-loop note) or 20 (GDD §6.2)?
- [ ] Where do spare ingots and finished blades wait (ingot shelf / blade rack)? Does a hot ingot cool if left out?
- [x] Concept 3: 12 points, 6+ for a sword, below that start over on the same hot ingot; each hit dents its part (2026-10-18).
- [ ] Concept 1: how does the "hammer until bigger" step work, and how is the trace-cut scored?
| 2026-10-18 | **Shop building is a log cabin** (stone foundation, blue shingle roof, porch roof over the door), made in Blockbench and imported as meshes | Allen asked for a medieval wooden cabin, mid-poly, enterable; the blue roof keeps the concept art's look | [[Sessions/2026-10-18]] |

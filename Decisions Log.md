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

| 2026-10-18 | **Historical shop asset: medieval log cabin** | Superseded by the open-front Japanese workshop on 2026-10-19; retain model as an earlier asset | [[Sessions/2026-10-18]] |

## Historical questions

The earlier open questions about reheat, timed Points, Trace, and dagger starting prices are superseded by the 2026-10-19 direction. Historical prototype behavior remains in the session notes and archived GDD. Storage capacity and new progression prices still need design/tuning.

## 2026-10-19 — Japanese village and simplified crafting

These approved decisions supersede conflicting earlier rows. Implementation is pending.

| Date | Decision | Details | Where |
|---|---|---|---|
| 2026-10-19 | **Setting and tone** | Japanese mountain swordsmith village inspired by Swordsmith Village; cozy daily life with spectacular individual visitors. Village-wide events deferred. | [[Sessions/2026-10-19]] |
| 2026-10-19 | **Workshop** | Open-front Japanese workshop, visible forging and displays facing the path; expand one increasingly elaborate workshop. | [[Sessions/2026-10-19]] |
| 2026-10-19 | **Starting blueprints** | Tantō → wakizashi → katana, taught through local commissions that provide the pattern when each request begins. | [[Sessions/2026-10-19]] |
| 2026-10-19 | **Early customers** | Mostly locals plus an early special outsider hinting at the wider world. | [[Sessions/2026-10-19]] |
| 2026-10-19 | **Commissions** | In-person requests and letters from returning customers replace smartphone texts. | [[Sessions/2026-10-19]] |
| 2026-10-19 | **Materials** | Keep the random Ore Roller, redesigned for the village, and the full fantasy material variety available from the start. | [[Sessions/2026-10-19]] |
| 2026-10-19 | **Wider traditions** | Visitors introduce new sword traditions through a first commission with its pattern; buy additional blueprints within that tradition. | [[Sessions/2026-10-19]] |
| 2026-10-19 | **Customer arrivals** | Displayed stock influences regular visitors; reputation unlocks surprise special visitors. | [[Sessions/2026-10-19]] |
| 2026-10-19 | **Special requests** | Untimed commissions; special visitors return when the requested sword is ready. | [[Sessions/2026-10-19]] |
| 2026-10-19 | **Customer tastes** | Regular customers have flexible tastes; special commissions specify combinations. | [[Sessions/2026-10-19]] |
| 2026-10-19 | **Haggling** | Retain negotiation and the risk that a customer leaves when pushed for a higher offer. | [[Sessions/2026-10-19]] |
| 2026-10-19 | **Fittings** | Match each sword tradition; unlock through crafting milestones, without a later coin-purchase requirement. | [[Sessions/2026-10-19]] |
| 2026-10-19 | **Scope** | Craft, collect, display, and sell; no combat or testing area for now. | [[Sessions/2026-10-19]] |
| 2026-10-19 | **Automation** | Keep both cashier and apprentice smith as later upgrades. | [[Sessions/2026-10-19]] |
| 2026-10-19 | **Decoration** | Functional displays and facilities improve business; purely decorative items are cosmetic. | [[Sessions/2026-10-19]] |
| 2026-10-19 | **Relationships** | Repeat sales build familiarity; milestones unlock personal commission chains and rewards. | [[Sessions/2026-10-19]] |
| 2026-10-19 | **Character roster** | Original village regulars plus recognizable fictional and historical special visitors. Leave their coexistence unexplained. | [[Sessions/2026-10-19]] |
| 2026-10-19 | **Quality** | Keep visible percentages and a price link, without named quality tiers. | [[Sessions/2026-10-19]] |
| 2026-10-19 | **Forging** | Hit every circle; each hit improves quality. No time limit, timing windows, misses, or cooling countdown. Supersedes earlier timed-strike/retry discussion. | [[Sessions/2026-10-19]] |
| 2026-10-19 | **Grinding** | All circles gives 90%; optional freehand grinding improves toward 100%. Remove only excess metal, stop at the target, never reduce quality. | [[Sessions/2026-10-19]] |
| 2026-10-19 | **Hilt assembly** | Three untimed taps, without timing bonuses or penalties. | [[Sessions/2026-10-19]] |

| 2026-10-19 | **Always open pickers** | Every item-selection interaction opens its picker, even with one valid item. No automatic current-workpiece selection or picker bypass. Supersedes the review recommendation. | [[Sessions/2026-10-19]] |

| 2026-10-19 | **10-second base heating** | Forge heating takes 10 seconds, replacing the 15-second prototype duration. Implementation pending. | [[Sessions/2026-10-19]] |

| 2026-10-19 | **First customer arrives after listing** | No customers visit the player’s shop during the first sword craft. Putting the sword on sale triggers the tutorial customer arrival. Replaces the proposed pre-craft/waiting customer; later sales-interruption policy remains open. | [[Sessions/2026-10-19]] |

| 2026-10-19 | **Starting tantō blueprint and guidance** | Players start with the tantō blueprint and simple on-screen instructions. Later local commissions introduce wakizashi and katana. Supersedes giving the first tantō pattern through a customer commission. | [[Sessions/2026-10-19]] |

| 2026-10-19 | **First sale guaranteed fair; haggle on second** | First tutorial customer gives a guaranteed fair offer. Introduce haggling on the second sale, keeping the first reward straightforward. Exact fair-price calculation remains untuned. | [[Sessions/2026-10-19]] |

| 2026-10-19 | **Wakizashi commission after first sale** | The next goal after selling the first tantō is a local wakizashi teaching commission, providing its blueprint at commission start. No required upgrade purchase or additional tantō sale first. | [[Sessions/2026-10-19]] |

| 2026-10-19 | **Wakizashi commission specifies a rollable material** | Require a specific material available from the player’s current Ore Roller, rather than accepting any material. Exact material undecided; no guaranteed drop or odds change approved. | [[Sessions/2026-10-19]] |

| 2026-10-19 | **First commission: Iron Wakizashi** | Iron chosen for the wakizashi teaching commission after the first tantō sale. Iron is in the starter roller’s Common pool. No guaranteed drop or altered odds approved. | [[Sessions/2026-10-19]] |

| 2026-10-19 | **Deliver commissions through a picker** | Select the completed sword through the commission and receive the agreed reward, without listing or haggling. Applies to the first Iron Wakizashi. Haggling tutorial therefore belongs to the second ordinary shop sale, not commission delivery. | [[Sessions/2026-10-19]] |

| 2026-10-19 | **Iron Wakizashi: minimum 90% quality** | Completing every forging circle meets the first commission’s quality requirement. Grinding remains optional; higher-quality swords also qualify. | [[Sessions/2026-10-19]] |

| 2026-10-19 | **First upgrade after Iron Wakizashi** | Completing the Iron Wakizashi commission leads into the first workshop upgrade, introducing spending earnings to grow the business. Upgrade type and price remain undecided. | [[Sessions/2026-10-19]] |

| 2026-10-19 | **First upgrade: second Ore Roller** | Each roller yields one material per roll; two rollers provide more chances to obtain a desirable material. This adds a roller rather than changing per-roll rarity odds. Price and activation/cooldown behavior remain undecided. | [[Sessions/2026-10-19]] |

| 2026-10-19 | **Automatic rollers with one waiting output** | Each roller automatically produces one material, waits until it is collected, then starts its next roll. Replaces manual hold-to-roll activation. Roll duration remains undecided. | [[Sessions/2026-10-19]] |

| 2026-10-19 | **Lever-operated ore roulette; under five seconds** | Player activates the lever; the stand rapidly cycles ore appearances and stops on the rolled material. Suggested visual method: change the displayed material. Result waits for collection; no automatic restart. Supersedes the earlier automatic-roller decision. Exact reveal duration remains untuned. | [[Sessions/2026-10-19]] |

| 2026-10-19 | **One lever, multiple material stands** | Buying another roller adds a stand, not a lever. The shared lever rolls all empty stands together; occupied stands retain their ores and cannot roll until collected. More stands give more results per activation. Supersedes separate-lever wording. | [[Sessions/2026-10-19]] |

| 2026-10-19 | **Grounded starter blades, extravagant later designs** | Tantō, wakizashi, and katana establish the craft with distinct silhouettes and slightly exaggerated readable proportions. Later special blueprints introduce unusual fantasy shapes. Exact profiles and shaping choreography remain open. | [[Sessions/2026-10-19]] |

| 2026-10-19 | **Staged blade shaping** | Early hammer hits lengthen the blank, middle hits establish taper and curve, and final hits form the point and refine the outline. Each impact visibly changes the area beneath the hammer. Exact intermediate profiles, hit counts, and pacing remain open. | [[Sessions/2026-10-19]] |

| 2026-10-19 | **Blade repositions without tongs** | The blade automatically slides, turns, and flips beneath the hammer between strikes, with no visible tongs or manual positioning. | [[Sessions/2026-10-19]] |

| 2026-10-19 | **Smooth localized impact deformation** | Each hammer impact quickly deforms the struck area and blends into neighboring metal. Flatten/stretch according to the stage; avoid shape snapping, wobbling, and slow melting. Timing and falloff remain untuned. | [[Sessions/2026-10-19]] |

| 2026-10-19 | **90% blade: clean, subtly rough** | Correct recognizable silhouette, subtle excess metal along the edge, and a dull finish. Grinding refines it; skipping grinding should still yield an attractive sword after assembly. | [[Sessions/2026-10-19]] |

| 2026-10-19 | **One universal starting blank** | All sword blueprints start from the same blank shape and size, then stretch to the chosen blade’s length during forging. Material appearance still follows the rolled material. Replaces proposed blueprint-sized blanks. | [[Sessions/2026-10-19]] |

| 2026-10-19 | **Equal initial hit count; modest tier effort later** | Start with the same hit count across sword blueprints. Higher-tier swords should eventually take a bit more effort. Exact scaling and form of extra effort remain undecided; preserve untimed forging. | [[Sessions/2026-10-19]] |

| 2026-10-19 | **Angled overhead forging camera** | Slightly angled overhead view preserves silhouette readability, blade thickness, hammer movement, and anvil depth. Keep the full blade visible as it lengthens and repositions. | [[Sessions/2026-10-19]] |

| 2026-10-19 | **Starter blades use real lengths and curvature** | Tantō 25.8 cm with a slight inward curve (sori −0.1 cm), wakizashi 50 cm (sori 1.2 cm), katana 70 cm (sori 1.8 cm), measured the catalogue way. Representative values from research; sori varies by period. Widths, thickness, kissaki and tangs remain exploratory. Sources in [[Blade Profile Authoring]]. | [[Sessions/2026-10-19]] |

| 2026-10-19 | **Smithy art direction: A/B mix** | Allen chose a mix of the two directions in [[Smithy Redesign Proposal]]: Direction A's materials and colours (white plaster, dark charred-cedar timber, grey tile roof, stone, iron, small vermilion and indigo accents) with Direction B's chunkier proportions (thicker posts and trim, bolder silhouettes) and extra lanterns (one on every front post). | [[Smithy Redesign Proposal]] |

| 2026-10-19 | **Station shapes for the rebuild** | The proposal's defaults, which Allen didn't change: hornless kanatoko anvil (`Face` and `BladeMount` unchanged), upright-sword pedestals as sword holders, an "ore shrine" Ore Roller with stone stands and one shared lever, warm late-afternoon lighting, old prototype blocks moved to `ServerStorage.Archive`, cabin files moved to `Models/Archive/`. | [[Smithy Redesign Proposal]] |

| 2026-10-19 | **Workshop built; choices made while building** | Claude's defaults, made during the build: holders at x 9.8 / 13 / 16.2 (3.2 apart, not 5, so the middle one stays at ShopService's inspect point), the Ore Roller lever post moved to x −12.2 and the stands to x ≈ −15, SpawnLocation moved to (1.5, 0.15, 9) as a low stone slab, Baseplate turned to grass, lighting set to ClockTime 16.4 with warm ambient (was 14.5 with grey 70/70/70). The anvil `Face` was darkened to 30/31/36 because the cooled steel blade was hard to see on it under the warm light. The noren were shortened to 1.4 studs so they don't block the player camera. | [[Smithy Redesign Proposal]] |

| 2026-10-19 | **Starter blueprints replace the prototype set** | The game's blueprints are now the tantō, wakizashi and katana from the blade data, replacing Dagger, Shortsword and the old Katana. Placeholder prices 20 / 45 / 110 coins and 1–3 stars until the economy pass. The Adventurer now likes wakizashi (was Shortsword); the Knight likes 95%+ blades (was 90%, which every forged blade now reaches). | [[Sessions/2026-10-19]] |

| 2026-10-19 | **First-person hammering arm deferred** | Tried a first-person view with the character's arm swinging the hammer; Allen chose to leave the arm for later as unimportant for now. The anvil keeps the angled overhead camera with the hammer in view (pivoting from behind the anvil so it never covers the blade). | [[Sessions/2026-10-19]] |

| 2026-10-19 | **Larger plot with storefront and crafting area** | Each player needs a spacious property with distinct retail and crafting spaces. L-shaped connected wings are a visual proposal; exact layout and dimensions remain open. | [[Sessions/2026-10-19]] |

## Current open design work

- Review [[Core Loop Review]]: first-session flow, picker clarity, heating pace, sales interruptions, and grinding incentive.
- Tune circle count, grinding duration/scoring, Japanese blueprint prices, fittings milestones, and visitor unlocks.
- Define the letter interface, storage, and exact customer taste matching. Commission delivery is through a sword picker.
- Choose specific special characters and their requests.

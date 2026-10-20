---
title: Flame Etch
status: pattern v4 in the game via the Etching Table (2026-10-20) — free, instant; no prices or minigame yet
type: art
date: 2026-10-19
updated: 2026-10-19
tags: [art, etching, blade, hilt, prototype, create-swords]
---

# Flame Etch

First etching pattern for the Etching Table idea ([[Design/Game Design Document]] §6 finishes: "Etching / Rune — trace a pattern"). An **original** flame motif — not a copy of the Demon Slayer "Rengoku" sword Allen pasted as a reference — on our procedural blades, plus a matching flame tsuba. Prototype only: a sword gets it when its record has an `etch` field; nothing in the game hands one out yet.

![[Models/Hilts/review/flame-etch-ingame-v1.jpg]]

*First in-game look (v0): the flame guard, and an early etch covering too much of the blade in orange. Superseded by pattern v2 below.*

## Blade etch

- `ReplicatedStorage.Shared.BladeEtch`: a thin two-colour skin 0.004 studs above both flat faces of the blade, built from the same `BladeCore` station params as `BladeView`, so it follows the forged and ground shape of the tantō, wakizashi and katana. Station params are interpolated about 4× finer than the 64 stations (16 samples per flame tongue).
- Each sample row has columns at the edge, the ridge crease, and the colour boundary twice (one vertex per colour), so the two colours meet in a crisp line that follows the pattern.
- **Pattern `Flame`:** a function of position along the blade giving how far the flame colour reaches from the edge toward the spine. Current shape: see Pattern v2 below. (v1 reached 8–58% of the width and read as scallops.)
- Colours come from the sword: `body` (dark) and `flame` (e.g. orange); defaults 6,12,20 and 165,14,10 since v4 (were 28,26,32 and 226,72,30).
- `SwordRenderer` builds it for any sword with an `Etch` attribute, welds it with the blade and destroys its EditableMesh with the sword. The anvil's blade has no etch.

## Pattern v2 (after Allen: "the etches don't look right")

![[Models/Hilts/review/flame-etch-v2.jpg]]

v1 (`flame-etch-v1-scallops.jpg`) read as rounded black scallops biting into a thin orange hem. The tongues had concave flanks on both sides, so the orange tips were needle-thin, and they reached only about a third of an already narrow blade. v2 uses the same profile that worked on the flame guard: each tongue rises steeply on the hilt side to a sharp tip leaning back toward the hilt, then comes down a rounded belly toward the point. There are fewer, bigger tongues (one per 0.45 studs: 3 / 6 / 8 on tantō / wakizashi / katana) and no small in-between tongues. Flames reach 8–85% of the width, 42% on average. Checked in a playtest on all three blades, laid flat.

## Pattern v4: matched to Allen's reference (in the game, 2026-10-20)

![[Models/Hilts/review/flame-etch-v4-ingame.jpg]]
![[Models/Hilts/review/flame-etch-v4-three-blades.jpg]]

Allen approved the even-peak preview. It's in `Shared/BladeEtch` as the same vertex-coloured skin (no texture was needed, because the band is a single boundary):

- `PATTERNS.Flame(sw)` is the preview's `reach()` with deterministic hashed spacing. `sw` counts local blade widths from the base, about 14 rows per width.
- The skin runs from 3.2% to 96.8% of the width, so the blade's own steel shows as thin bright lines on the edge and the spine.
- Bevel shading comes from vertex colours: the band darkens away from the edge, and the dark body takes a cool sheen near the guard that fades along the blade.
- Colours (`Shared/Etches` Flame and `SwordRenderer` defaults): body 6,12,20 and band 165,14,10. The flame guard follows: dark core, red rim, inlay lightened toward gold.
- Playtest: etched katana, wakizashi and tantō built on the server and drawn on the client, with no script errors. The old module is kept as `ServerStorage.Legacy.BladeEtch_beforeBand`. Swords etched earlier in a session keep their old colours until they're re-etched (data is session-only).

### Preview and measurements

![[Models/Hilts/review/flame-etch-v4-vs-reference.png]]

Allen replaced the v3 direction with a screenshot to match (`References/Etching Table/flame-band-reference.webp`). He asked to match the red band's placement and width and to trace its shallow, rounded, uneven boundary with occasional small points. Most of the blade stays dark metallic, with thin bright edges and visible bevel shading. He wanted the reference and the revision side by side at the same orientation.

- **Measured from the reference** (`Prototypes/etch/measure_reference.py`): the red band reaches 28% of the width from the edge line (19–38% across the humps). The dark humps come about once per 0.6–1.0 blade widths in the screenshot (the closer end is about 1.0; perspective shortens the rest), with an amplitude of 10–17% of the width. Each red dip is broad and rounded, deepest at 45% of a hump.
- **Pattern** (`Prototypes/etch/flame_etch_preview.py`, `reach()`): the hump period is random from 0.75 to 1.05 local widths. Every hump has the same height, 0.14 of the width (`AMP`). Allen asked for even peaks, so the random heights and the small red points were removed. The position is counted in local blade widths, so the tantō keeps the same rhythm at its own scale.
- **Look:** red 165,14,10 → 108,9,8; dark steel 30,56,84 (lit bevel near the guard) → 6,12,20; thin bright lines (3% of the width) on the edge and spine; faint ridge line. The bevel sheen fades along the blade.
- **Measured on the revision, the same way as the reference:** the band reaches 27% on average (18–36%).
- **Supersedes v3** (curved tongues, `flame-etch-v3-flat-preview.png`). The game plan is unchanged: an EditableImage texture on an etch overlay, replacing the v2 vertex skin.

## Pattern v3 proposal (superseded by v4)

![[Models/Hilts/review/flame-etch-v3-flat-preview.png]]

Allen asked for connected, curved flame tongues that grow from a narrow edge band and vary in size and spacing. He also asked for a clear dark body and a metallic bevel, with a flat preview shown first. Source: `Prototypes/etch/flame_etch_preview.py`, drawn on the true tantō, wakizashi and katana outlines.

- **Across the face, edge to spine:** a bare polished steel strip (16% of the width), a narrow flame band (7% of the etched width), tongues rising from the band, then a dark body up to the spine. The ridge line is kept faint.
- **Tongues:** each S-curves forward, then whips its tip back toward the hilt. The base is full and the tip thin. Neighbours join through the band with rounded joins.
- **Variety:** spacing is 0.6–1.05× the etched width. Every third tongue (plus random extras) is a big one reaching 75–92% of the width; the others reach 40–64%. Some big tongues throw a small side tongue. Tongues calm down near the point.
- **Sizes:** everything is sized from the etched width, so the tantō gets the same flame shapes at its own scale.
- **Reading of "metallic bevel":** the steel strip along the cutting edge. The alternative is to keep the flames on the flat above the ridge and leave the whole bevel bare steel.
- **Game plan after approval:** port the pattern to Luau, draw it into a cached EditableImage per blueprint length and colours, and map it onto an etch overlay that covers only the etched part of the face. This replaces the v2 two-colour vertex skin.

## Colour from the material (2026-10-20)

Allen: "the color of the material should be part of it".

![[Models/Hilts/review/flame-etch-material-colours.jpg]]

- `Shared/Etches.MATERIAL_FLAME` gives each material a vivid band colour on the same dark body:
  - Iron silver, Steel icy white, Silver bright white.
  - Copper orange, Bronze amber, Gold gold.
  - Blue Steel blue, Mythril cyan, Starmetal violet, Obsidian purple.
  - Stone sand, Damascus warm tan, Rainbow Alloy pink.
- `Etches.colorsFor(etch, materialId)` returns the body and flame colours. `EtchService` stores them on the sword, so the blade band and the flame guard's rim and inlay take them. The Etching Table's pattern card previews the chosen sword's colours.
- Unknown materials fall back to the pattern's red.
- Playtest: etched Iron, Gold and Blue Steel katanas got flame colours c4ccd8, fac424 and 3a80f0, and drew silver, gold and blue.
- Backups: `ServerStorage.Legacy.*_beforeMaterialColour` (Etches, EtchService, EtchingTableController).
- **Found during the test:** with about nine swords drawn at once, the client hit Roblox's **EditableMesh memory budget** ("Failed to create empty EditableMesh … memory budget limits"), and later blades and etches didn't draw. Each sword uses one EditableMesh for the blade and one for the etch; picker cards add more. See the open item in [[Development/Roadmap]].

## How to etch a sword in game (2026-10-20)

Walk to the **Etching Table** on the pavilion's back wall, between the forge and the Hilt Bench. Press E, choose a finished sword from your inventory, then choose **Flame**. The sword comes back etched, with the flame guard and +15% value. It's free and instant for now: Allen chose no prices and no minigame yet.

![[References/Etching Table/picker-choose-sword.jpg]]
![[References/Etching Table/etched-katana-held.jpg]]

The command-bar snippet that used to be here was removed. Code run from the command bar or the Studio MCP gets its own copy of `SmithyCore`, so it never saw the game's real swords.

## Flame guard

![[Models/Hilts/review/flame-guard-34.png]]

- Modelled from code in `Models/Hilts/build_hilt.py` (`build_flame_guard`, `FLAME` settings). The outline breaks into 7 flame tongues; each swells up a rounded belly to a sharp tip and drops steeply, so they swirl round the guard. A first version with symmetric spikes read as a sawblade and was replaced.
- **Three colour-role parts:**
  - `FlameRim`: a bright band following the outline, full thickness.
  - `FlameCore`: a dark plate, slightly thinner, so the rim stands proud.
  - `FlameInner`: a smaller flame inlay on both faces, with its tongues between the outer ones.
- Same frame as the hilt's tsuba. About 4.8k triangles. Roblox QA passes; accepted warnings are the hidden faces where the core meets the rim and the inlay.
- Exported with the `roblox` preset (`Models/Hilts/FlameGuard.fbx`) and uploaded with the Open Cloud API as Model asset **85043523139786**. Stored as `ServerStorage.SwordParts.FlameGuard`, in the Handle frame and centred on the grip axis.
- **Import note:** this import came in with a different part orientation from the katana hilt's (right vector (0,0,1) instead of (0,0,−1)). The axis mapping is not fixed per upload, so place each new import from its measured part offsets, not an assumed rotation.

## How a sword gets it

- `SmithyCore`: `Sword.etch = { pattern, body, flame, guard? }`.
- `buildSword` sets the `Etch`, `EtchBody` and `EtchFlame` attributes.
- `dressHilt` looks for `SwordParts.<guard or pattern>Guard`. If it exists, that guard replaces `Tsuba` and `Rim`, and its parts take the etch colours by name suffix: Core = body, Rim = flame, Inner = flame lightened toward gold.

## Verified

- **Studio playtest:** an etched katana displayed on `Slot2` (exactly as `ShopService` places swords), one in open space, and one held by the player. On the client, each had its Blade, Etch and flame guard parts, with no script errors. Earlier, all three blueprints (tantō, wakizashi, katana) rendered the etch.
- Pattern v2 was then checked in a playtest on all three blades (see above).
- **Untouched dialog:** a "Disconnected … Recover (Error 0x89AF2)" dialog appeared over the play view again, even though the pasted reference katanas are now gone. Nothing was clicked.

## Not started (by design)

The Etching Table station, buying patterns, the trace minigame, the value bonus, saving the etch, and the picker art for etched swords.

Related: [[Art/Katana Hilt]] · [[Development/Code Map]] · [[Sessions/2026-10-19]]

---
title: Blender Station Review
status: archived — historical art or layout review; current build supersedes geometry
type: art
date: 2026-10-19
updated: 2026-10-22
tags: [art, blender, stations, review, create-swords]
---

# Blender Station Review

Historical review retained for reference. Current map and station layout: [[Art/Town Street Redesign References]], [[Art/Workshop Layout]] and [[Current Status]]. Earlier dimensions, tasks and proposed rules below are not the active roadmap.

**Additional visual exploration (2026-10-20):** [[References/Smithy Redesign/ore-roller-low-poly-prompt-v1|Low-poly ore roller concept]] shows one roofless ore stand and a separate shared lever, with the exact generation prompt. It is a concept image requested by Allen, not a replacement of the current imported geometry.

Review of Claude's five-station Blender lineup, requested by Allen and saved so Claude can use it for another modeling pass.

![[Models/Stations/preview-lineup.png]]

Source assets: `Models/Stations/Stations.blend`, `Models/Stations/build_stations.py`, and the individual station FBX exports in the same folder. This is a visual critique of the preview, not an inspection of Blender geometry or a fresh Studio test. No models were changed during this review.

## Allen's feedback

- Dislikes the roof over the ore rollers.
- Wants the ore roller units to be independent models that can be replicated.
- The anvil does not look like an anvil.
- The furnace has too many details.
- The display pedestal on the right looks odd.

The following changes are recommendations responding to that feedback. Specific proportions and construction choices still need review in the next preview.

## Overall direction

The models are stylistically consistent, but their decorative shapes communicate more strongly than their functions. At lineup distance they read as a small building, a barrel with a tray, a shrine, a cabinet, and a red post. Each station should be recognizable through its main shape and working surface before decoration is added.

**Palette context:** the initial critique compared the teal/red/yellow/lavender palette with the earlier grounded plaster/timber direction. The latest session note records that Allen specifically requested bright, cartoony low-poly models. Preserve that requested direction; simplify competing accents and improve functional readability rather than treating the earlier palette as a requirement to revert. Final material appearance cannot be fully judged from this preview alone.

## Revision recommendations

### Ore stands and shared lever

Remove the shared roof and supporting shrine frame. The roof dominates the assembly, makes it feel like one fixed structure, and would add clutter beneath the workshop's existing roof.

- Make each ore stand a self-contained, repeatable model: base, ore presentation surface, and a defined ore position.
- Use a squat stone or timber stand with a shallow tray and a large, readable ore chunk.
- Keep the **one shared lever as a separate model**. Replicating a stand must not duplicate the control or introduce one lever per stand; preserve the agreed shared-lever behavior.
- Arrange stands as separate units with clear spacing. Express the Japanese setting through restrained joinery and materials rather than another miniature building.

### Anvil

The thin overhanging top and orange cylindrical support read as a tray on a barrel. The support has more visual weight than the striking block.

- Make a thick, solid rectangular iron block the defining shape, with a broad flat working face and a small edge bevel.
- Mount it on a squat, simple timber base that looks capable of supporting hammer blows.
- Retain the approved **hornless Japanese anvil**; a western horn is not required for recognition.
- Remove surrounding accessories while resolving the core silhouette, then add only useful supporting details.
- Check the blade and hammer against the working face before finalizing proportions.

### Furnace / forge

The chimney cap, colored chimney sections, yellow windows, red bands, hanging ornaments, framed opening, side boxes, and individual flames compete for attention. The chimney reads like a miniature tower.

- Reduce the design to a heavy masonry body, dark recessed fire opening, simple hood/chimney, and one bellows.
- Preserve the functional ingot trays and show their connection into the heated chamber.
- Concentrate orange heat inside the dark opening rather than scattering yellow accents across the structure.
- Reduce trim, ornaments, and unrelated side props. Establish a clear body/opening/chimney silhouette before restoring detail.

### Display pedestal

The red column, black cap, white rectangle, and brown piece on top read as a bollard or donation box. The preview does not explain how a sword is held.

- Use a stable timber plinth with a visible blade support and upper guide for the approved upright sword presentation.
- Keep the price label subordinate to the sword and its support.
- Model and review it **with a sword installed first**. The sword should dominate the finished silhouette.
- Then remove the sword and check that the empty holder still communicates where a sword belongs.

### Hilt bench

The grips and fittings communicate customization most clearly in this lineup, though the body reads more as a cabinet than a workbench.

- Broaden and deepen the worktop, reduce the drawer count, and establish one obvious assembly area.
- Lower or simplify the tall display frame if it overwhelms the working surface.
- Preserve useful color cues on the actual fittings.

## Next-preview checks

- [ ] Resolve plain station silhouettes and one clear functional detail before adding decoration.
- [ ] Show independent ore stands with one separate shared lever, including a layout with additional replicated stands.
- [ ] Show the anvil with a blade and hammer, the forge with an ingot in its tray, and the holder with a displayed sword.
- [ ] Review each station alone and beneath the workshop roof at normal gameplay distance and avatar scale.
- [ ] Check the combined set for visual crowding and keep accent colors focused on meaningful features.
- [ ] Before Studio integration, recheck working heights, attachment positions, collision, and script dependencies in [[Development/Code Map]].

## Revised station concept sheet

At Allen's request, generated this concept sheet with the built-in image generation tool on 2026-10-19. It explores the recommendations above; it is not an approved production model or a change to station capacity, behavior, or working heights.

![[References/Smithy Redesign/blender-station-concepts-v1.png]]

The sheet shows a simpler forge, thick hornless anvil, broad hilt bench, three independent roofless ore stands with one separate shared lever, and identical empty/loaded sword holders. The ore stand count is illustrative. Preserve the requested bright/cartoon style during modeling; the generated stone/wood surface detail is richer than necessary for the final low-poly assets. Holder dimensions and sword support still need checking against the actual in-game blades.

Exact prompt: [[References/Smithy Redesign/blender-station-concepts-prompt-v1]].

## Wall-mounted sword holder concepts

Allen requested wall-holder concepts as a follow-up. Generated three options with the built-in image generation tool, using the station concept sheet as a style reference:

![[References/Smithy Redesign/wall-sword-holder-concepts-v1.png]]

- **Single horizontal holder:** two separate wood mounting blocks and paired padded cradles. Recommended basic wall display: clear blade silhouette and repeatable one-sword modules.
- **Three-tier rack:** two rails with three pairs of cradles. Potential later upgrade for denser stock; capacity and upgrade behavior remain illustrative.
- **Vertical holder:** a slim wall strip with a collar and tip cup, preserving grip-up/blade-down presentation. Useful for narrow wall sections.

Each is shown loaded and empty. Horizontal presentation is an alternative proposal to the previously approved upright pedestals, not an approved change to sword orientation or slot behavior. Holder spacing and attachment points need checking against all actual blade lengths, particularly short blades; the generated examples are not measured construction plans. The wall fragments are presentation backdrops, not part of the repeatable holder asset.

Exact prompt: [[References/Smithy Redesign/wall-sword-holder-concepts-prompt-v1]].

## v2 model pass (2026-10-19)

Modeled from the recommendations above and the concept sheet, keeping the bright cartoony palette. Same file and script (`Models/Stations/build_stations.py` now builds v2; the v1 lineup image is kept above for comparison).

![[Models/Stations/preview-v2.png]]

- **Forge:** cream masonry hearth, one dark chamber with the glow kept inside, two railed iron trays at the ForgeSlot positions (x ±0.45, z 1.12), plain hood, short charcoal chimney with no cap, one box bellows. No rope, tags, crate, flames or coloured bands.
- **Anvil:** a 3.0 × 1.3 × 1.65 iron block (its top is the scripted `Face`, z 3.2) on a squat block of four upright timbers with one iron band. No tools or bucket.
- **Ore stands:** `OreStand` is one self-contained model (feet, stone base, railed tray, iron ore seat, `Ore` part). The preview shows three copies: cyan ore, iron-grey ore, empty. **`OreLever` is its own model**, so adding stands never adds levers.
- **Sword holder:** wood plinth with a tip socket, two side uprights and an iron collar just under the guard; shown loaded and empty at the same heights. Small cream tag on the plinth.
- **Hilt bench:** wide 5.0 × 2.4 worktop at z 2.85, two drawers, square legs, a low pegboard with three grips and three tsuba; a grip and two guards on the worktop.
- Preview-only props (hot ingot, raw blade, hammer, katana) live in a `PreviewProps` collection and are not exported. Z-fighting check: 0 pairs.

Exports: `Forge.fbx`, `Anvil.fbx`, `HiltBench.fbx`, `OreStand.fbx`, `OreLever.fbx`, `SwordHolder.fbx` (the v1 `OreShrine` and `DisplayPedestal` exports were removed).

**Next-preview checks done in v2:** plain silhouettes first; independent stands with one separate lever, shown replicated; anvil with blade and hammer, forge with an ingot, holder with a sword. **Still open:** review under the workshop roof at gameplay distance and avatar scale; holder heights against the real displayed blades (`Slot` y 2.92 suggests the tip sits near the plinth top, which this assumes); Studio import and the script-dependency recheck.

## v2 feedback (Allen, 2026-10-19)

- **Anvil** still the biggest issue: tall narrow block reads as a safe. Lower and broader, clear horizontal striking face, slight bevel between top and sides, hornless. Check beside an avatar with a hammer; posture matters more than the concept's proportions.
- **Forge** still reads as a fireplace: remove trim layers, make the opening deeper and heavier, trays should visibly run into a dark glowing chamber, give the bellows one recognisable moving part.
- **Ore stands** the strongest: keep the shape, add a couple of broad stone joints, keep the ore the focus and don't let rails hide small results.
- **Sword holders** look like goalposts: end the uprights just above the collar, soften the caps, make the tip socket legible, test with the real tantō, wakizashi and katana.
- **Preview:** neutral background, level camera, one avatar, matching close-ups.

## v3 model pass (2026-10-19)

Measured in Studio first (read-only; floor = 0): anvil `Face` top **3.0** above the floor, forge trays top **0.93** with the ingot slot 0.15 inside the mouth, hilt bench top **2.9**, and a displayed sword's grip (0.75) is **centred on its `Slot`** with the guard just below it (`SmithyCore.buildSword`).

Renders in `Models/Stations/review-v3/`: neutral grey stage, level camera, one blocky 5.2-stud avatar, every close-up from the same angle with only its own station visible.

![[Models/Stations/review-v3/anvil-side.png]]

- **Anvil:** 3.6 × 2.0 iron block, chamfered, with a lighter 3.2 × 1.62 striking face on top; low timber base. Face top proposed at **2.3** (today 3.0). Side views: at 2.3 the arm swings down to about waist height; at today's 3.0 the arm is level with the shoulder (`anvil-side-today-3.0.png`). **To use it in Studio** the whole Anvil station moves down 0.7 with `PivotTo` (scripts read anvil parts relative to the station); the forging camera and strike feel need a playtest. The scripted `Face` (3.0 × 1.3) fits inside the visual face and can stay as is.
- **Forge:** cream surround and sill removed; one heavy iron lintel; a real 1.5-deep chamber with dark lining, glowing coals and back wall; trays 2.2 long running from deep in the fire to past the mouth; bellows with a red push-pull handle on two rods.
- **Ore stands:** two stone courses with offset joints in two cream tones; low rails (top 1.4) and a raised iron seat (top 1.52) so even a small ore sits above the rails.
- **Sword holders:** uprights end just above the collar with soft wood caps; red tip rest with a dark slot. **Test with the real blades** (nagasa × 0.05 studs/cm: tantō 1.29, wakizashi 2.5, katana 3.5): the guard height is fixed by the slot, so one collar fits all three, but **one collar-to-socket distance does not**. With the collar at 3.95 the katana tip lands in the rest (0.45), the wakizashi tip hangs at 1.45 and the tantō at 2.66. Also, for an open holder the katana needs the slot at 4.43 above the floor (Studio `Slot` y 2.92 → about 4.63); at today's height its blade would go through the floor. Decision needed: keep the rest as a katana-only cue, drop it, or another option.
- **Hilt bench:** top raised to the measured 2.9.

![[Models/Stations/review-v3/swordholder.png]]

Close-ups: `forge.png`, `anvil.png`, `hiltbench.png`, `orestand.png`, `swordholder.png`, `lineup.png`. Z-fighting check: 0 pairs. FBX exports updated.

## Texture style test: one ore stand (2026-10-19)

Allen asked to texture one ore stand as a style test, keeping geometry and palette, then wait for feedback before treating the others.

![[Models/Stations/review-v3/orestand-texture-compare.png]]

- `Models/Stations/station_textures.py` (was `texture_ore_stand.py`) paints six tileable 512 px PNGs into `Models/Stations/Textures/` (wood, dark wood, stone, dark stone, iron, dark iron): broad painted wood grain (4 bands per tile), soft stone patches and pits, light iron wear patches and a few scratches. Each averages to its palette colour, so the stand stays bright.
- UVs are box-projected at one tile per 2 studs, with the grain following each board. The stand is joined into one mesh per texture (6) plus the separate flat-colour `Ore`, so a roll can still recolour it.
- `Models/Stations/OreStand_Textured.fbx` embeds the textures. In Roblox, each MeshPart gets its PNG as `TextureID`; textures repeat, so the UV tiling carries over.
- At gameplay distance the grain and stone patches read; the iron wear is very faint on the near-black feet and seat, by design. Not applied to other stations yet.

## v3 and texture-test feedback (Allen, 2026-10-19)

- **Texture:** the stand looks richer without crowding at gameplay distance; keep that. Wood reads as straight stripes: add gently curved grain, occasional tapered strokes, maybe one knot, aligned with each board. Stone patches repeat diagonally across blocks and look stamped: vary placement and scale per stone, softer and less directional. Iron wear works as is; don't add scratches. Aim for more intentional variation, not more density.
- **Anvil:** much better proportions. The lighter face still looks like a lid: thinner or nearly flush. The final height should come from the real avatar and hammer animation.
- **Forge:** the functional changes help. The ingot is near-pure yellow and loses its shape: orange body with a brighter centre. Add restrained soot around the mouth.
- **Sword holders:** a real design problem; the shorter blades hang above an unused socket. Remove the bottom socket from a universal holder and make the support under the guard clearly carry the sword, or offer sizes. The tall frame still overwhelms the tantō; the wall-holder concepts suit small blades better.
- **Hilt bench:** shape works. Next: wood texture and recognisable fittings (guard openings, wrap marks on the grips).
- **Preview:** the lineup crops the outer objects; pull back.
- **Recommendation:** keep the geometry direction, resolve the universal holder, one more ore-stand texture pass before texturing the rest.

## v4 pass (2026-10-19)

Renders in `Models/Stations/review-v4/`, same stage and angles as v3.

![[Models/Stations/review-v4/orestand-texture-compare.png]]

- **Ore stand texture, pass 2:** wood has soft broad bands, seven gently curved anti-aliased grain lines that thicken and thin, tapered strokes, and one knot that the grain bows around. Stone uses round mixed-size blobs (no sine directions) with soft edges, and **every board and stone gets its own random UV offset** (stones also a 0.8–1.25 scale), so no two neighbours share marks. Iron unchanged.
- **Anvil:** striking face is now a 0.05 plate almost flush with the block top, a shade lighter than the iron.
- **Forge:** ingot is an orange body with a bright yellow core strip. Soot: one transparent `forge_soot.png` spread over three thin planes (crown above the lintel, the course, the lower hood), darkest just above the mouth and fading upward, at most 60% opaque. In Roblox these become MeshParts with a transparent texture (or the PNG can be used as a Decal).
- **Sword holder (universal):** bottom socket removed. Two dark crossbar halves with red pads carry the guard; the blade drops through the slot between them, so any length fits and the empty holder shows the slot. Uprights still end just above the crossbar. Height is still set by the katana, so it still dwarfs the tantō: **open decision** between this universal holder, sized holders, or wall holders for short blades (`References/Smithy Redesign/wall-sword-holder-concepts-v1.png`).
- **Hilt bench:** guards have a central blade opening (shows the board or worktop behind); peg grips carry three wrap diamonds on the front face, the worktop grip three cream wrap bands. Wood texture waits for the ore-stand texture sign-off.
- **Lineup:** camera pulled back; nothing cropped.

![[Models/Stations/review-v4/forge-front.png]]

Z-fighting check: 0 pairs. FBX exports updated and now embed textures (`Forge.fbx` carries the soot; `OreStand_Textured.fbx` the stand textures). Anvil height is still a proposal pending the real avatar and hammer animation in Studio.

## Mid-high poly (2026-10-19)

Allen asked for the stations in mid-high poly. One switch at the top of `build_stations.py` (`DETAIL = "mid-high"`, or `"low"` for the earlier look) drives every part. At mid-high:

- sharp edges get 3-segment rounded bevels (1.4× the old widths; parts thicker than 0.12 that had none get 0.025), with smooth shading split at 35° so flat faces stay crisp;
- cylinders get at least 28 sides;
- ore, coal and embers use a finer faceted icosphere and stay flat-shaded, so they still read as cut;
- the FBX files now export smoothed normals.

Same designs, heights and textures as v4; Z-fighting check 0 pairs. Triangles per model: forge 4.8k, hilt bench 5.9k, ore stand 2.5k, sword holder 1.4k, anvil 1.4k, lever 0.8k; no single part above 760 (Roblox allows 20k per MeshPart).

![[Models/Stations/review-midhigh/hiltbench.png]]

Renders: `Models/Stations/review-midhigh/` (same angles as v4). Exports: `Models/Stations/MidHigh/*.fbx`; the low-poly exports stay in `Models/Stations/`. This pass rounds and smooths the existing forms; it doesn't add sculpted detail such as carved stone faces, plank seams or rope.

## Forge reimagining — sculpted concept (2026-10-19)

Allen requested a completely reimagined medium-to-high-poly forge and selected **concept image first**. Generated this new direction with the built-in image generation tool:

![[References/Smithy Redesign/forge-reimagined-v1.png]]

A broad rounded ivory clay shell, volcanic-stone base and arched mouth replace the rectangular fireplace and pyramidal hood. A curved shoulder leads into an offset dark chimney; one integrated timber/leather bellows connects into the chamber. Two supported ingot trays extend into a deep ember-lined opening. Front, three-quarter and rear views explore the same design.

This is a rendered concept image, not a generated 3D mesh or an approved production design. It explores higher geometric detail through smooth curves and softened edges. The generated surface treatment is more weathered and realistic than the earlier cartoon lineup; a final game model can retain the silhouette with broader, cleaner painted textures. Working heights, dimensions and script attachments still need a modeling/integration pass if this direction is selected.

Exact prompt: [[References/Smithy Redesign/forge-reimagined-prompt-v1]].

## Roblox QA and export (2026-10-19)

Adopted two installed Blender agent skills (`blender-agent-skills` 1.1.0): **blender-asset-qa** (`qa_check.py`, profile `roblox`) and **blender-export-pipelines** (`export_asset.py`, preset `roblox`). `build_stations.py` now has `qa()` and an `export_fbx()` that calls the preset.

- **First run:** every solid-colour part failed for having no UV map; the textured ore stand failed for UVs outside 0–1; the tray floor's underside overlapped the rails'.
- **Fixes:** every part gets a simple box-projected UV in 0–1 (`auto_uv`); textured parts are shifted into 0–1 with a random fitted placement (repeat now 2.7 studs); cylinder caps are triangle fans instead of n-gons; the tray floor sits inside the rails.
- **Result:** Anvil, Hilt Bench, Ore Stand, Ore Lever, Sword Holder and the textured stand pass. The forge passes except its soot decals, which are flagged "floating"; they sit 0.02 off the surface on purpose to avoid Z-fighting, so that is accepted.
- **Accepted warnings:** hidden back-to-back faces where parts touch (a few wasted triangles each), overlapping UVs on solid-colour parts (no texture), and open edges on the decals.
- **Exports:** `Models/Stations/MidHigh/*.fbx` via the `roblox` preset (FBX unit scale, triangulated, textures copied and embedded; no `bake_space_transform`).
- **Scale test pending:** `Models/Stations/ScaleTest/ScaleTest.fbx` and `.glb` hold a 1 × 1 × 5 post, a 1-stud cube on top and an arrow pointing at the station front. Once they're imported into Studio with Import 3D, their measured size settles whether 1 Blender unit = 1 stud holds (the skill's note says 1 stud ≈ 0.28 m).

Related: [[Archive/Art/Smithy Redesign]] · [[Archive/Art/Player Plot Review]] · [[Sessions/2026-10-19]]

## In the game (2026-10-20)

Allen: "can you import the blender stations you created and replace the existing ones".

![[Models/Stations/review-ingame/pavilion.jpg]]
![[Models/Stations/review-ingame/storefront-holders.jpg]]

- **Upload:** the `MidHigh` FBX files went up through Open Cloud: Anvil 88910023014005, Forge 95489199917505, HiltBench 117052021303151, OreLever 80532740934891, OreStand (textured) 100188404268789, SwordHolder 105428217718912. Staged in `ServerStorage.Stations3D`.
- **Colours:** FBX colours don't import, so each part was coloured from its Blender material (read from `Stations.blend`, converted to sRGB). Glowing materials became Neon. Textured parts are white, so their textures show true.
- **Orientation:** imported fronts face −Z, so every station is turned 180° to face the open floor.
- **Forge:** the new trays land on the scripted `ForgeSlot1/2` (x ±0.45, top 0.93 above the floor), and the bellows ends up where the old one was. The `Fire` light moved into the new chamber.
- **Anvil:** following the v3 proposal, the whole station dropped 0.7, so the scripted `Face` tops out at 2.3 above the floor, flush with the new striking face. **The forging camera and strike feel need a playtest.**
- **Ore roller:** the shrine and old lever are gone. `Stand1` holds the textured stand, with its ore named `Ore` and its stone base named `Pedestal` (that's where `ForgeService` puts the collect prompt). The lever model stands on the invisible `Machine`.
- **Hilt bench:** the new bench sits on the floor; the old platform went with the rest. `Top` stays as the invisible prompt part.
- **Sword holders (universal v4):** each slot now holds the sword blade-down, with the guard on the crossbar pads. Each `Slot` is turned over and raised to 4.75, and each holder faces its customer's `InspectPoint`. A katana tip ends about 0.4 above the floor.
- **Checks:** the bounding-box face check between the new meshes and the plot or smithy parts found 0 coplanar faces (mesh undersides on the floor excluded).
- **Backup:** `ServerStorage.Legacy.Smithy_beforeStations3D` holds the old Smithy.
- **Not verified yet:** Studio's Play stuck on "Start play hasn't finished yet", so nothing has been playtested: rolling ore, heating, forging on the lowered anvil, the hilt bench, and displaying a sword on a holder.

**Later validation update:** the subsequent Polishing Station session in [[Sessions/2026-10-19]] records a forged tantō auto-finishing at 90%, a Steel Katana polished and saved at 97%, and a successful animated lever/ore roll. Allen then saved the place, covering the imports. The complete post-import heat → hilt → all holders → customer sale loop remains open; the earlier "nothing playtested" statement above describes the initial import session only. Current requirements: [[Current Status]] and [[Development/Roadmap]]. Employee workstation growth and roof cutaway remain design additions in [[Design/Workshop Growth]].

## Anvil with a horn (2026-10-20)

Allen: "make the anvil look like an actual anvil with the horn". This replaces the hornless block direction.

![[Models/Stations/review-ingame/anvil-horned.png]]

- `anvil_horned()` in `build_stations.py`: a banded log stump, flared iron feet, a waist, and a 3.0 × 1.3 body with a lighter striking face, all at the same `ANVIL_TOP` 2.3 as the scripted `Face`.
- A 1.5-long horn points to −X (the blade mount's end). The heel steps down to +X, with a square hardy hole and a round pritchel hole.
- QA passes with no Z-fighting. Uploaded as Model asset **101524963962681**.
- **Not swapped in yet:** Allen was in a playtest. The swap replaces `Smithy.Anvil.Model3D`, keeping `Face`, `BladeMount`, `Clang` and the prompt, then needs a playtest of forging.

## Low-poly furnace from concept (2026-10-20)

Allen: model `References/Concept Art/furnace.png` in Blender, "keeping the same low poly style". Then: "remove the spikes" and "remove the fake fire you added".

- `furnace()` in `build_stations.py`: a stone block in an iron corner frame (posts with chamfered bottom, middle and top collars), a stone lid, a barred fire mouth with cut top corners, a slot above the mouth, a three-slot side vent on +X, and a grate on top. It is 4.4 × 3.8 × 3.8 studs and faces −Y.
- Always flat-shaded with single chamfers (it forces `DETAIL = "low"`), unlike the mid-high set. New swatches: `stone`, `stone_dk`, `frame`, `fire`.
- No pyramid rivets and no modelled flames. Only a flat orange glow panel sits behind the bars.
- QA passes with no Z-fighting: 39 parts, about 1,070 faces. Exported to `Models/Stations/Furnace.fbx`. Built in `Buildings.blend` at (110, −10).
- **Not uploaded or placed in the game.** Gameplay points (tray, ingot slot) are not modelled yet.

## Blockbench anvil test (2026-10-20)

Allen: "Try creating an Anvil in our blockbench MCP". This is a trial of the Blockbench MCP (`localhost:3000/bb-mcp`). It must be running before a Claude session starts, or you reconnect it with `/mcp`.

- The horned anvil (`anvil_horned()` dimensions, 1 stud = 10 Blockbench units, Generic Model format) is built in one undoable `risky_eval` script. Body, face and heel are cubes; stump, band, feet, waist and an 8-sided horn are small meshes; there are four solid palette textures.
- Saved as `Models/Stations/Anvil.bbmodel`. Not exported or uploaded.
- The plugin's `delete_offscreen_view` threw `onContextMenu is not defined`. The view is cleared when the MCP session ends.
- **Retry (Allen: "just the anvil, nothing below it. the horn doesn't seem to be attached"):** removed the stump and band, so the feet stand on the floor and the face top is at 1.32. The horn now starts from the body's own cross-section at the −X end (chamfered 8-point rings), keeps its top level with the face, and its underside sweeps up to the tip. Note: Blockbench mesh faces take at most four vertices, so caps are triangle fans.
- **Wedge horn (Allen: "why dont you use a wedge instead of this weird cone"):** the horn is now a 5-face wedge. Its flat top is level with the face, it narrows to a point at −3.05, and its underside slopes up to the tip.

## Furnace v2: textured stone shell, separate door (2026-10-20)

Allen (with a reference image of a grey stone furnace with an arched iron door): "Can you model this in blender. Build the furnace shell as a simple mesh. Keep the door separate. Use UV-mapped textures for the stone blocks and mortar, with a normal map for shallow depth. Do not model individual bricks."

![[Models/Stations/FurnaceV2/review/furnace_v2_sheet.png]]

- **Source:** `Models/Stations/FurnaceV2/build_furnace_v2.py`, run headless (`blender --background --python build_furnace_v2.py`). It writes `FurnaceV2.blend`, `FurnaceV2.fbx` (Roblox preset), `Textures/`, `review/` and `qa.json` next to itself.
- **`Furnace_Shell` (one mesh; 460 triangles before the smooth bevels, now 1,908):**
  - a chamfered plinth (5.2 × 4.4);
  - a body tapering on the sides and back, with a vertical front, an arched recess for the door (boolean) and a raised arch band;
  - a sloped hood with a ledge, a neck, two posts and a chimney cap;
  - 6.05 studs tall.
- **No modelled bricks:** a running-bond block pattern (0.8 × 0.4 studs, two greys with mottling, darker mortar) is laid along each face in studs. It is baked into `Textures/furnace_v2_color.png`, and its recessed mortar and fine grain into `furnace_v2_normal.png` (OpenGL / tangent, shallow). Both are 1024², the Roblox SurfaceAppearance maximum, on the shell's unique 0–1 `UVMap`.
- **`Furnace_Door` (separate mesh; 1,088 triangles, now 1,776):** arched iron panel with a raised rim, glowing slot in an iron frame, two pointed strap hinges with knuckles and rivets, and a ring handle on a boss. Flat materials (iron, strap, emissive glow). Its origin is on the hinge line (left edge, bottom), so it can swing.
- **QA (`roblox` profile):** no errors, no warnings. The first pass found inward normals, coplanar faces and a floating strap and boss on the door; all fixed.
- **Stone texture pass (Allen: "give it a stone texture"):** the clean brick look became cut stone.
  - Blocks are larger (1.1 × 0.55 studs, every third course 0.6 as long), and the joints are wobbled by noise so they look hand-cut.
  - Each block has its own tone, plus cloudy stains and granite speckle; the mortar is darker and warmer.
  - The normal map has rounded, chipped block edges, chisel facets and pitting.
  - The arch band is laid out around the arch as wedge-shaped voussoirs, so it no longer repeats the wall pattern behind it and looks see-through.
  - Same mesh and triangle counts; QA clean; FBX re-exported.
- **No block lines (Allen: "without the brick lines"):** the block and mortar pattern is gone. The texture is plain stone: two greys blended by broad clouds, with finer stains and granite speckle. The normal map keeps soft chisel facets, fine grain and pits. The arch band's stone is offset so it doesn't repeat the wall behind it. QA clean; FBX re-exported.
- **Stone tints (Allen: "add some coloring", chose "Stone tints"):** warm sandy (0.50, 0.45, 0.39) and cool blue-grey (0.36, 0.39, 0.45) patches blend through the grey at 42% by their own broad clouds, plus a few faint mossy-green patches. A 55% first try read as camouflage and 30% barely showed. QA clean; FBX re-exported.
- **Smooth bevels (Allen: "can you smooth out the bevels"):**
  - Every bevel is now 3 segments with a round profile, and a bit wider: plinth and cap 0.12, body and hood 0.08, neck 0.06, posts 0.05, arch band 0.04 (it had none), door panel 0.03, slot frame 0.02.
  - Shading is smooth across the rounded edges (`smooth_shade`: smooth below 40°, 50° on the door) with weighted normals, so the flat faces stay flat and real corners like the recess stay sharp.
  - The ring handle has more segments (16 × 8).
  - Normal map re-baked. Shell 1,908 tris, door 1,776. QA clean; FBX re-exported.
- **Not in the game.** For Studio: upload the FBX, then give `Furnace_Shell` a SurfaceAppearance with both PNGs (FBX colour textures don't import). Gameplay points (tray, ingot slot, timer anchor) aren't modelled yet.

### The v2 door on the current forges (2026-10-20)

Allen: "Can we replace our edit our current forge in studio to have the same door", then "the door window should glow when something is inside, and not glow when inactive", and "the door isnt attached if you look from the side".

- `FurnaceDoor.fbx` is the door split by material (`build_furnace_v2.py`, `export_door_parts`). It was uploaded as asset 110924074428709 and stored as the `Buildings3D.FurnaceDoor` template: `Door_iron` (40, 44, 56), `Door_strap` (70, 76, 92) and `DoorWindow` (41, 26, 20), which has a `WindowLight` PointLight (range 9, off).
- `Forge.Door` and `Forge2.Door` are scaled to the old mouth. They sit flush on the furnace face (local z 1.61–1.82, x ±1.30, y −0.55 to 1.25), with the arch's top tucked behind the lintel so no gap shows from the side. The trays moved back a net 1.45 so their pull ends sit behind the door. The ingot slot offset is unchanged.
- The full Furnace v2 shell swap was not done; it was interrupted. The shell, textures and FBX are still only in Blender.

## Ore Roller stand v2, low poly (2026-10-20)

Allen: "can you design a low poly ore roller stand"

![[Models/Stations/OreStandV2/review/ore_stand_v2_sheet.png]]

- **Based on Allen's Studio blockout** (`Smithy.OreRoller.Stand1`): a brown base disc, a cream drum, a brown cap disc and the ingot-shaped `Ore`. It keeps that silhouette, those colours (92, 60, 40) and (236, 222, 196), the 4.1-stud width, and the cap top at 2.25 with the ore resting on 2.29.
- **Low-poly finish:** octagonal and flat-shaded, with one-segment chamfers (`build_stations.DETAIL = "low"`).
  - The drum swells at the waist like a taiko drum.
  - Two iron hoops carry 8 gold tacks each.
  - A lighter wooden seat on the cap holds the ore.
- **Source:** `Models/Stations/OreStandV2/build_ore_stand_v2.py`, run headless. It reuses the `build_stations.py` helpers and writes `OreStandV2.blend`, `OreStandV2.fbx` (Roblox preset, stand only), `review/` and `qa.json`.
- **Numbers:** 928 triangles (the 16 tacks are about half of them). QA (`roblox` profile) passes with no errors. The only warnings are UV overlap, which is expected for flat-colour parts with no bake. The coplanar check finds 0 pairs.
- **Not in the game.** Studio's `Ore` mesh stays the part the roll recolours. The model has no ore; the cyan ingot in the renders is a stand-in.

## Mine shaft: where the ore comes from (2026-10-20, layout sketch)

Allen asked whether ore coming from a pedestal makes sense lore-wise. Claude suggested a mine shaft with a winch: the lever works the winch, a bucket comes up, and the ore lands in mine carts. Allen: "yes do it in blender".

![[Models/Stations/MineShaft/review/mine_shaft_sheet.png]]

- **Pieces (plan in studs, shaft centre at (0, 2)):**
  - **`MineShaft`:**
    - a 7 × 7 stone curb, 1.2 high, with a timber-lined 4.2 opening and a black void;
    - two timber A-frames, 8.5 high, under a crossbeam with an iron sheave wheel and a small slate-tile gable roof;
    - a bucket hanging at the shaft mouth;
    - a winch drum on two trestles at x 6.5, with rope over the wheel to the drum;
    - a 22 × 16 dirt yard.
  - **`Lever`:** a brake lever beside the winch at (8.6, −0.4), the roll lever.
  - **`Track`:** a rail track along x at y −4.5, with sleepers and end stops.
  - **`Cart1`–`Cart3`:** wooden mine tubs with iron straps and four wheels, at x −5 / 0 / 5. The ore's bottom sits on 1.7 inside the rim.
- **How it maps to today's code:** each cart is a stand (a model with an `Ore` part the roll recolours), so the Ore Roller logic carries over. More carts means more stands. "Dig deeper" could replace luck upgrades, with the fantasy materials coming from the deep veins.
- **Source:** `Models/Stations/MineShaft/build_mine_shaft.py`, run headless. It reuses the `build_stations.py` helpers, flat-shaded low poly like Ore Stand v2.
- **Numbers:** MineShaft 1,348 triangles, Lever 176, Track 268, each cart 320. QA (`roblox` profile) passes on every model. The coplanar check finds 0 pairs, after the first pass flagged mirrored beams, rail ends, the cart straps, a floating ridge and a reversed roof pitch.
- **In the game (2026-10-20, later):** Allen: "Export and upload the mine shaft, lever, track and carts, and swap them in for the Ore Roller so the roll fills the carts."
  - `export_mine_shaft.py` (run on `MineShaft.blend`) joins each model into one mesh per colour, named after the palette key, and writes `Mine_MineShaft.fbx`, `Mine_Lever.fbx`, `Mine_Track.fbx`, `Mine_Cart1.fbx` and `parts.json` (each part's centre).
  - Assets: MineShaft 87668833460136, Lever 70931016393860, Track 94793876325507, Cart 135588990042995.
  - Placed with the Blender origin at Roblox (42, 0.2, −62), front toward +Z. The yard spans x 31–53, z −52.5 to −68.5.
- **Open points:**
  - The shaft is only 1.2 deep, a black floor inside the curb. A real hole would need the plot floor cut.
  - The bucket and the carts don't move during the roll; only the ore floats and flickers, as before.

## Mine entrance: carts roll out of the ground (2026-10-20, design pass)

Allen, after the shaft went in: "I was thinking more so the carts from in from underground... as i trigger the lever, the cart comes rolling out one by one with a different ore... draw it out before you implement". A wall-and-cave plan was sketched first. Then Allen sent a Clash of Clans gold mine reference: "it just comes out of the ground".

![[Models/Stations/MineEntrance/review/mine_entrance_review.png]]

- **`MineEntrance`:**
  - a log A-frame tunnel mouth: 6 logs a side and a ridge log, with the log ends staggered;
  - the frame sinks 1.2 studs over 7 into a rocky earth mound with boulders;
  - two iron straps over the logs;
  - a black panel 2 studs inside closes the tunnel, so a cart that rolls in vanishes;
  - a plank floor in the mouth, base rocks and rubble;
  - a red-capped paper lantern under the ridge;
  - a crate of gold ingots beside the mouth.
- **`Track`:** six cart stops, the most a player can own (Allen: "the game will have a max of 6 carts/rolls, so can we build out the 6. and then another 3 with the track turning right").
  - The track runs straight out of the mouth past stops 1–3 (y −5.2 / −8.7 / −12.2).
  - It then makes a quarter turn of radius 4 to the right as you face the mine (+X).
  - Stops 4–6 sit on the second leg, then an end stop. The track is 31.6 studs long.
  - Rails are mitred sweeps along the path. Sleepers alternate 0.12 / 0.14 so the angled ones on the curve never share a top plane.
  - Stop 1 is nearest the mouth. With N carts, the first cart out goes to stop N and the rest stop behind it, so small owners stay close to the mine.

![[Models/Stations/MineEntrance/review/mine_entrance_6carts.png]]
- **Reused from the shaft:** the carts and the lever (left of the mouth). The headframe, wheel, roof, bucket, winch and curb go.
- **Source:** `Models/Stations/MineEntrance/build_mine_entrance.py`, which imports `build_mine_shaft.py` for the palette, `beam()` and `cart()`.
- **Numbers:** MineEntrance 2,100 triangles, Track 200, Lever 176, cart 320. The coplanar check finds 0 pairs. QA only flags the rubble stones as "detached"; they rest on the plot floor, not on the model.
- **Planned behaviour, not built:** pulling the lever rolls any parked carts (empty, or holding your own uncollected ore) back into the dark. They then come out one by one, about 0.6 s apart, each revealing its ore as it stops. Collected carts stay parked until the next pull.
- **In the game (2026-10-20, later):** Allen: "Upload the mine entrance and the 6-stop track, swap them in for the mine shaft, and make the carts roll back in and then out one by one along the track when I pull the lever."
  - `export_mine_entrance.py` (run on `MineEntrance.blend`) joins by colour. Assets: MineEntrance 103967104952089, Track 78597689951275.
  - Placed with the Blender origin (the middle of the mouth, on the floor) at Roblox (44, 0.2, −58), front toward +Z. The first leg runs along x 44 to z −40; the second runs along z −39.8 to x 58.7.
  - The shaft is gone (backup `Legacy.OreRoller_beforeEntrance`). The lantern is Neon with a warm PointLight.
  - The black panel collides, so players can't walk into the tunnel.


## Mine cave: soft rocks and a plank portal (2026-10-20)

Allen sent two references of a stylised mine entrance ([[References/Concept Art/mine-cave-ref-1.png|clay]], [[References/Concept Art/mine-cave-ref-2.png|painted, night]]): "can you make the mineshaft look more like this. Ignore the details of the trees and rocks, just look the silhouette of the cave. soft bevels, and soft looking rocks, with handpainted texturing."

![[Models/Stations/MineCave/review/mine_cave_sheet.png]]

- **Silhouette:** a mound of chunky, softly rounded boulders stacked in tiers. It peaks at the back at 7.6 studs, about twice the portal's height as in the references. A plank portal is set into its front: two posts, a lintel, a six-plank roof whose back end the rocks sit on, plank side walls and rope lashings. The footprint, mouth and track are the old entrance's. The black panel stays 0.6 inside the mouth, so carts still vanish into it.
- **Rocks:** each boulder is a dense ellipsoid with lumps. A few big facets are planed off it (biased to the top and sides, so tops read as flat planes), the creases are smoothed into wide soft bevels, and it is decimated to about 280 tris. A big core boulder fills the gaps so the mound reads as one mass.
- **Hand-painted texture:** baked from an emission shader into `Textures/mine_cave_rocks.png` and `mine_cave_wood.png` (1024², colour only; no normal map, because the softness comes from the real bevels).
  - Rocks: each one runs from light at its top to dark at its foot, with up-facing planes lighter. A pale highlight is painted along each upper shoulder, crevices are dark blue-grey (AO against the other rocks, the wood and the ground), and broad brushy value and hue drift, plus a little moss at the feet.
  - Wood: warm browns with painted grain lines along each plank, per-plank tone shifts, lit edges and dark joints. The rope is straw-coloured with a twist stripe.
- **Rework (2026-10-20, later):** Allen, comparing with the clay reference: "it looks like a messy pile of rocks on top of the wooden mine shaft... the idea is that the mineshaft is built out of the giant boulder."
  - A single slabbed dome came next. Allen: "now it looks too round like a ball or igloo".
  - Allen then gave a brief:
    - an asymmetric pile of large angular boulders, varied in size, depth and rotation;
    - broad, flatter faces with chipped edges and restrained bevels;
    - stepped rocks at the top, with boulders protruding along the sides and base;
    - a recessed entrance with a dark interior and depth behind the timber frame, kept clear of rocks.
  - Now: 21 angular blocks fused into one mass. Each is a convex hull of a jittered box with 2–4 chipped corners and a 3-segment bevel (≤ 0.22 studs). The mass is heavier on the right (+X) and steps up to a peak at 8 studs at the back right, with a hidden core block filling the gaps between blocks.
  - The rock face comes forward beside the posts, and a rock face rises behind the roof so the planks run into it. The tunnel is cut out of each block separately; each cut sits 0.02 studs deeper, buried in the wood, so no two cut faces share a plane.
  - The tunnel is 2.8 studs deep (was 1.8): the black panel moved back to y 0.4, where the rails start, and a black floor runs inside the frame. The wall and roof planks fade to dark toward the panel. A cart at `CartPath.Hidden` (y 2.0) is still wholly behind the panel, so ForgeService is unchanged.
  - Numbers: Rocks 10,368 tris, Wood 5,568, void 24. The coplanar check finds 0 pairs, QA passes and the tunnel is clear. Review: `Models/Stations/MineCave/review/mine_cave_sheet.png`. **Not yet swapped into Studio**; the game still has the first version below.
- **Outcrop pass (2026-10-20, later, Blender only):** Allen: the rocks "look like stacked rectangular blocks". He asked for large, irregular angular boulders that interlock into a cohesive outcrop, with an asymmetric stepped top, a few protruding masses, the entrance excavated into it with timber supporting the mouth, and more tunnel depth fading into darkness instead of a flat black panel.
  - Boulders: each is the convex hull of eight corners, every one pulled in by its own amount per axis and skewed sideways (so no two faces sit square), plus four ellipsoid points. A broad top and one or two broad sides are sliced off at random angles, two to four upper corners are chipped, and each gets a soft 3-segment bevel (≤ 0.32 studs) and up to 12° of tilt in any yaw.
  - The outcrop: 21 boulders and a core plus a high filler, so nothing shows through. It is heavier on the right and steps down to the left and front from the peak at the back right (7.6 studs), with masses protruding at the sides and base. Three blocks frame the mouth, kept square to it: the two jambs and a slab over the awning.
  - The tunnel: a solid rock lining runs from just inside the posts to a black closure 5.8 studs back (it was 2.8). It narrows to 85% and drops to 94%, its walls and ceiling are rough, and its paint fades to black with depth. Two support frames inside (y 0 and 2) dim with depth too. The plank side walls are gone, and the awning's back runs into the slab.
  - Each boulder is cut on its own, just inside the lining's outer face, before the pile is joined (cuts staggered 0.02, all hidden). Rocks are 15,324 tris, Wood 5,568, void 12. The coplanar check finds 0 pairs, QA passes, and no rock reaches into the mouth or the cart run.
  - **To go in the game:** raise `CartPath.Hidden` to −4.5 (y 4.9) so a parked cart sits behind the deeper closure; ForgeService already carries the path straight back for negative distances. The Track's rails start at y 0.4, so they should run on into the tunnel too.
  - Known detail for a later pass: a few bevels show small light dashes in the baked texture.
  - Review: `Models/Stations/MineCave/review/mine_cave_sheet.png` (clay and textured from the reference angle, front and side, the mouth, and night). **Not in Studio**; the game still has the first version.
- **Rock-shape pass (2026-10-20, later, Blender only):** Allen: the rocks "look too sharp and crystalline". He asked for heavy, worn boulders with broad irregular faces and gently rounded corners, no triangular peaks or wedge points (especially the pointed right rock and the big tilted top rock), upper rocks set deeper into their neighbours, a cohesive asymmetric stepped outcrop, and a cleaner texture. The tunnel, supports, timber, ropes, footprint and cart clearance are unchanged.
  - Boulders: the top corners are pulled in less than the bottom ones, so no ridge or wedge forms. Each has a broad, gently sloped top, one or two broad sides and one to three worn corners. A wide single bevel and two levels of subdivision round the corners while the faces stay broad, then each boulder is decimated to about 700 tris. Upper boulders tilt at most 4°, the rest 8°.
  - Layout: the peak is broad and low (5.6 × 4.8 × 3.8), sunk into the mass. The other upper boulders are lower and wider; the right jamb is shorter, with a new boulder stepping up behind it. Side protrusions moved in, so the rock now spans x −6.2…6.6 and the peak is at 7.0 studs.
  - Texture: the rim highlight that drew broken white lines is gone. Highlights now sit only on faces turned toward a key light (above, front left) near each boulder's top. The cloudy mottling became a per-boulder tone plus very broad, quiet value and hue drift. The AO crevices stay, and the moss is a faint wash at the foot only.
  - Rocks 16,056 tris. The coplanar check finds 0 pairs, QA passes, and the mouth and cart run are clear.
  - Compared with the reference: the reference packs more, smaller rounded boulders into the mound, while this outcrop has fewer, larger flat-topped masses. Two tiny dents from worn-corner cuts show in the clay views.
  - Review: `Models/Stations/MineCave/review/mine_cave_sheet.png` (clay and textured from the reference angle, front and side, plus the mouth and night). **Not in Studio.**
- **Rock-definition pass (2026-10-20, later, Blender only):** Allen asked for clearer boulder separation above the entrance, the huge top-right rock and tall right face broken up, broad flat faces with rounding only at the corners ("my previous feedback pushed softness too far"), restrained painted variation instead of a plain, rubbery look, and the awning projecting from the rock face rather than the front rock pressing on it.
  - Boulders: subdivision is gone. A 3-segment corner bevel (≤ 0.38 studs) keeps the face centres flat. Each boulder gets two or three near-vertical changes of plane (no ridges) and one to three small chips.
  - Layout: the right jamb is split into a low block and a smaller one set back on top. The big right mass and the top are each split into two offset boulders (a step, then the peak behind it). The slab over the mouth moved back and narrowed, and the awning now runs back to y 0, so it projects from the slab's face. The core and filler sit behind the front cluster, where they never show. Two blocks that read as shards were reseeded.
  - Paint: soft warm and cool patches, darker faces turned down, and a soft key light on upturned faces. Upper-edge highlights come from the Bevel shader's normal (the rounded corners only, upper half), so they're wide and soft with no broken lines. Crevices use a tighter, darker AO (0.7 studs).
  - Rocks 15,562 tris. The coplanar check finds 0 pairs, and the mouth and cart run are clear. QA reports one overlapping tri pair in Rocks. It is a false positive of the 2D triangle test: the two triangles are disjoint (y 0.48–0.96 against −0.50 to −0.01), both on the lining's underside at z −0.21, under the floor.
  - Review: `Models/Stations/MineCave/review/mine_cave_sheet.png`. **Not in Studio.**
- **Finishing pass (2026-10-20, later, Blender only):** Allen's list, in priority order: rock/roof intersections, the remaining wedges, painted surface detail, and plank edges.
  - Awning: the block that poked a point into the right plank sits lower and further out, under the awning's right end. A new check (`rock_verts_in_awning` in qa.json) keeps every rock out of the awning's projecting part (x ±3.15, y −3.45…−0.7, z 3.6…4.3), and it finds none. The planks' rear edge (y 0) is buried in the slab.
  - Wedges: only the upper-right peak and the right-flank pieces (seeds in `FULL`) changed. Their corners are pulled in less (fuller bodies), their tops are flatter and their side planes shallower, they tilt at most 3°, and they get a softer 0.14 × size bevel. The thin flank pieces are also thicker. The other rocks are unchanged.
  - Paint: stronger warm and cool patches. Sparse shallow cracks are thin, faint Voronoi-edge lines broken into short runs by two noise masks. A second, tighter AO (0.25 studs) darkens the contact crevices.
  - Planks: front ends are uneven by up to 0.48 studs, and about 60% have a worn, slanted front corner.
  - Allen, during the pass: "rotate the roof planks so they're left to right". The awning is now five planks laid across (x about ±3.1, lengths uneven at both ends), 0.55–0.66 studs wide, stacked from the front edge (y −3.15) back to the rock (y 0, buried). About 60% have a worn corner on one end. Wood 5,474 tris, and the awning is still clear of rock.
  - Rocks 15,346 tris, Wood 5,754. The coplanar check finds 0 pairs, and the mouth, cart run and awning are clear of rock. QA's one flagged pair is the same verified false positive under the floor.
  - Review: `Models/Stations/MineCave/review/mine_cave_sheet.png`. **Not in Studio.**
- **Polish pass (2026-10-20, later, Blender only, local edits):** Allen asked to unify the rock style on the soft slab over the mouth, replace the V-shaped groove on the top-right boulder with subtle fractures, break the stepped shelves at the right base, and add restrained blue-grey, warm-grey and muted green patches.
  - Rock style: the right-side blocks (`SOFTEN`) merge near-flat hull facets up to 20° into broad faces and take the slab's softer bevel (0.13 × size). The fuller rocks (`FULL`) pull their corners in less (0.7) and skip their chips. The chips are still drawn on a scratch copy, so the random sequence, and every other boulder, is unchanged.
  - The V groove was a corner of the peak's own hull. The peak got a new seed (61) at the same position and size, plus a slight hand-set lean, so it doesn't read as a box.
  - Right base: hand-set tilts (`TILT`) on the front-right base block (44) and the block under the awning's right end (55), so their tops no longer step up as even shelves.
  - Paint: separate blue-grey, warm-grey and muted green patches (green on upturned faces only), darker downward faces and feet. Fractures are now Voronoi edges on noise-warped coordinates, so the lines wander, vary in width (0.004–0.028) and darkness, and fade out under a sparse mask. The tight contact AO stays.
  - Rocks 13,164 tris, Wood 5,474. The coplanar check finds 0 pairs, and the mouth, cart run and awning are clear of rock. QA's one flagged pair is the same verified false positive under the floor.
  - Review: `Models/Stations/MineCave/review/mine_cave_sheet.png` (clay reference angle; textured reference angle, front, side). **Not in Studio.**
- **Right-side finishing pass (2026-10-20, later, Blender only, local edits):** Allen's list: the tall boulder right of the awning still looked crystalline with a pointed foot; thin wedges and sharp triangular contacts on the right side; dotted or serrated pale lines along upper edges in the texture; restrained variation within individual rocks.
  - The tall boulder (seed 53, `GROUNDED`): it keeps its turn and proportions, but drops the three low hull points that tapered its foot. Its corners are fuller (0.78), it gets a flat broad base, and it has the fuller rocks' no-chip, soft-bevel treatment.
  - Right-side contacts: the wedge under the awning's right end (55) moved back and down into the mass. The pointed flank piece (43) is tucked in, the sliver-topped back block (36) is lowered, and the core is a little narrower, so it no longer pokes out at the far right. The low right jamb (52) got the fuller treatment, and the front base block (44) has a gentler hand-set tilt.
  - Serrated pale lines: the cause was the bake. Island edges rasterised stair-stepped, and the default "extend" margin smeared those steps outward, so a highlight on a UV seam filtered into a serrated pale line. The bake now uses `margin_type="ADJACENT_FACES"` (each seam's margin is filled from the face across it) at 2048 px, scaled down to 1024 px (antialiased edges). It builds in about 3 minutes.
  - Paint: broad cool-grey and warm-grey patches (noise scale 0.25, sized to sit within one rock), much fainter green, soft shoulder highlights where upturned faces roll toward the key light, and the dark feet and contact AO kept. Cracks are fainter (darkness 0.15–0.45) and sparser.
  - Rocks 12,894 tris, Wood 5,474. The coplanar check finds 0 pairs, and the mouth, cart run and awning are clear of rock. **blender-asset-qa now passes outright** (the earlier false positive went away with the core change).
  - Left as is: one small V where the front base stone's corner rises against the jamb.
  - Review: `Models/Stations/MineCave/review/mine_cave_sheet.png` (close-up of the entrance's right side, textured and clay reference angle, front). **Not in Studio.**
- **Source:** `Models/Stations/MineCave/build_mine_cave.py` (headless; writes the blend, FBX, textures, review renders and `qa.json`).
- **Numbers:** Rocks 6,440 tris, Wood 5,568, void 12. The coplanar check finds 0 pairs, blender-asset-qa (roblox profile) passes, and no rock reaches into the tunnel under the roof. QA's only warning is that the asset dips below z 0 (rock bases and post feet are buried in the floor on purpose).
- **The lantern** is the game's old Neon lantern (with its PointLight), now hung under the right end of the roof, clear of the carts. A short rope in the Wood mesh holds it.
- **In the game (2026-10-20):** uploaded as Model 84547516108281 and placed with the Blender origin at Roblox (44, 0.2, −58), mouth toward +Z. Colour maps: rocks `rbxassetid://81144495990773`, wood `rbxassetid://115779032060290` (SurfaceAppearance).
  - The new model is `Smithy.OreRoller.MineCave` (`Rocks`, `Wood`, `void`, `paper`, `red`).
  - Rocks and Wood use precise collision; the black `void` panel collides.
  - The old `MineEntrance` is in `ServerStorage.Legacy.OreRoller_MineEntrance_beforeCave`. The Track, CartPath, carts and lever are untouched.
  - Studio coplanar check: the only real contact is the post feet at y 0.1 on the PlotPad, buried inside the Courtyard paving (top 0.2), so it is never visible.

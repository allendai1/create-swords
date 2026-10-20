---
title: Blender Station Review
status: mid-high stations imported — full post-import validation pending
type: art
date: 2026-10-19
updated: 2026-10-19
tags: [art, blender, stations, review, create-swords]
---

# Blender Station Review

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

Related: [[Art/Smithy Redesign]] · [[Art/Player Plot Review]] · [[Sessions/2026-10-19]]

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

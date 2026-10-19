---
title: Blade Implementation Research
status: research recommendation — not an approved implementation spec
date: 2026-10-19
tags: [research, forging, roblox, modeling]
---

# Blade Implementation Research

## Recommendation

Use a hybrid workflow: author precise silhouettes and intermediate shapes, then animate one continuous blade mesh in Studio through EditableMesh. Blender is valuable for reviewing proportions and making fittings, hammer, and anvil models. Image generation supplies art direction; it does not supply trustworthy model dimensions or deformation data.

This is a researched recommendation, not a claim that the pipeline has been implemented or tested. The current Studio place was not accessible through a dedicated Studio tool in this session. Existing implementation details below come from [[Code Map]] and prior session notes; no local Luau source/place files were found in the vault.

## What we already have

The vault documents a 40-section profile, client-side EditableMesh blade renderer, bevel/ridge generation, and blade repositioning beneath a fixed hammer. That is a useful starting point. The documented profile primarily changes edge widths; the new design also needs longitudinal growth, centerline curvature, and thickness through staged shapes. Old timing/miss rules and silhouette scoring do not match the new design.

## Methods compared

| Method | Useful role | Fit for our design |
|---|---|---|
| Studio Parts/wedges | Graybox the hammer, anvil, camera, and motion | Quick to assemble, but segmented geometry is a poor final blade surface. |
| Studio solid modeling / CSG | Author rigid props or test cut effects | Not recommended for repeated forging deformation: topology changes complicate predictable stage morphs. Roblox advises against many asynchronous solid-modeling calls in rapid succession. [Official documentation](https://create.roblox.com/docs/parts/solid-modeling) |
| Procedural EditableMesh | Continuous blade stretching, local impact changes, bounded grinding | Recommended runtime foundation. Roblox exposes vertex editing; fixed-size meshes permit position changes without adding/removing geometry. [EditableMesh](https://create.roblox.com/docs/reference/engine/classes/EditableMesh) |
| Blender static models | Precise final shapes, fittings, props, display fallbacks | Excellent art-authoring route. Import supports FBX, OBJ, and glTF; rigging and animation data are also supported on appropriate formats. [Studio importer](https://create.roblox.com/docs/studio/importer) |
| Blender rigged/skinned blade | Authored bending/stretching motion | Possible alternative, but precise point formation and local grind boundaries would require more specialized rigging. Bone motion changes appearance rather than collision. [Rigging and skinning](https://create.roblox.com/docs/art/modeling/rigging) |
| Discrete prebuilt blade stages | Cheap visual fallback | Easier than continuous deformation, but changes can pop. Would compromise the approved smooth local morph; use only as a disclosed fallback if needed. |
| Image generation | Mood, silhouette exploration, textures/reference | Keep as reference. Our generated sheet already has inconsistent proportions and an exaggerated hammer dent. |

## Shape authoring

For each starter blueprint, define five corresponding states: universal blank, lengthened blank, tapered/curved preform, clean 90% forged blade, and refined 100% blade. All states for a given blade must share vertex correspondence and connectivity. Independent exports with unrelated vertex order are not automatically morph-compatible.

Two practical authoring routes:

1. **Profile-first, recommended for the first prototype.** Define lengthwise stations with position along the blade, centerline offset, edge widths, thickness, and ridge placement. Generate the surface consistently from those stations. Start from the existing 40-section renderer, adding resolution only if the tip/curve needs it. This is enough for the three starter blades without requiring complex assets.
2. **Blender-assisted, for stronger art control.** Author the matching states as shape keys or corresponding meshes, keeping topology stable. Export explicit vertex positions or sampled profile data through a small exporter into versioned Luau data. Blender shape keys store vertex-position changes; stable topology is the recommended authoring practice. [Blender shape-key documentation](https://docs.blender.org/manual/en/4.5/animation/shape_keys/introduction.html)

Do not assume a normal FBX import will automatically turn arbitrary Blender shape keys into runtime sword morph controls. This research did not establish that pipeline. Explicit shape-data export plus EditableMesh avoids depending on it. Imported vertex IDs/order also need a mapping; never assume separately imported meshes preserve the same IDs.

Author the three final profiles at a consistent scale before tuning the animations. Include a stable hilt/tang attachment point and nonzero thickness. Inspect top and side views as well as the game camera. Grounded style does not require physically conserving metal volume: the universal blank and fantasy materials are deliberate game abstractions.

## Runtime forging sequence — proposed approach

Keep whole-object motion and surface deformation separate:

- **Pose:** slides, flips, and turns position the selected section under the fixed hammer. No tongs.
- **Shape:** a per-strike target changes the actual blade surface.

Use a deterministic strike recipe for each blueprint. Each entry names the stage, affected region, pose, and target deformation. Spread the stage transformation across strikes; do not globally blend every vertex by the same amount on each hit. During lengthening, a struck section may extend and move the downstream sections to preserve a continuous blade. During taper and tip work, changes are concentrated around that region. Validate stage endpoints ahead of time so the final hit does not cause a large catch-up snap.

Suggested input sequence: prepare next pose → show persistent ready circle → accept tap → swing hammer → contact → deform and emit effects → recover/reposition. Prevent overlapping swings; test a one-input buffer so tapping during recovery is not treated as a miss. No timer or failure window is introduced.

A rigged hammer can use Studio's Animation Editor with a Contact marker; Roblox exposes marker signals through GetMarkerReachedSignal(). Trigger the impact sound, sparks, small camera impulse, deformation, and progress update from that same contact event. A scripted hammer motion can instead use one shared phase controller. [Animation events](https://create.roblox.com/docs/animation/events)

Starting values for a feel test only: brief 0.1–0.2 s wind-up, roughly 0.05–0.1 s deformation, and short recovery overlapping repositioning. These are not approved timings. Exact feedback and motion need playtesting. Recalculate surface normals where necessary, preserve crisp bevel boundaries, and ensure material patterns do not visibly swim or stretch badly.

For camera framing, start by fitting the selected blueprint's maximum extent across its planned poses. Avoid constant zooming per hit. Keep the slightly angled overhead view and entire blade visible, including during flips and tip work.

## Optional safe grinding

Generate the 90% state with a small positive edge allowance relative to the final profile. Track refinement per section. A drag moves covered sections toward their final target and clamps there; it cannot overcut or decrease progress. Keep per-section refinement in saved sword data so partially ground swords reproduce correctly. Quality can be computed as 90 plus ten times weighted refinement coverage, with weights tuned later. It should measure refinement work, not simply triangle count.

Geometry and edge shading should both communicate improvement. Reuse the same blueprint definition for anvil, picker silhouette, held sword, and display sword; otherwise the finished sword can look different after transfer.

## Multiplayer and practical constraints

The server should own the ingot, chosen blueprint, validated strike progress, grind state, and final value. Clients render motion responsively from compact events/state. Do not treat a client-reported 100% as authoritative or stream every animation vertex each frame. Use sequence/session IDs to prevent duplicate strike/finish rewards and reconstruct a late observer from the latest confirmed state.

EditableMesh requires the Mesh/Image API setting for published games, appropriate asset permissions when loading assets, and attention to client memory limits. Fixed-size meshes can help memory usage; editable creation can fail when the budget is exhausted. Visual edits and collision rebuilding are separate. [EditableMesh](https://create.roblox.com/docs/reference/engine/classes/EditableMesh), [CreateEditableMesh](https://create.roblox.com/docs/reference/engine/classes/AssetService/CreateEditableMesh.html)

For this noncombat game, propose a simple stable hit/collision proxy rather than rebuilding collision on every impact. Test active forging plus visible neighboring shops and stocked displays on real lower-memory clients. Reuse geometry where shape/refinement is identical, bound caches, destroy unused meshes, and avoid one perpetual frame loop per displayed sword. Define a static-mesh fallback before shipping so a memory-allocation failure does not strand a player.

## First technical validation to do next

Build a focused tantō proof of concept before authoring every sword:

1. Verify the published-place mesh API configuration and asset permissions.
2. Author all five states with consistent vertex correspondence.
3. Demonstrate one local lengthening hit, one taper hit, and one tip hit, including fixed-point repositioning.
4. Run a complete untimed sequence to the clean 90% state, then safe grinding to 100%.
5. Check silhouette, normals, bevels, and tip from the agreed camera; compare anvil and held/displayed appearance.
6. Test repeated taps, leaving/re-entering, two observing players, and duplicate finish requests.
7. Test allocation failure and a populated six-shop scene on a published client, including a lower-memory device.

This probe would answer visual feasibility, responsiveness, and resource limits. It has not been executed. No product code, models, or gameplay changed during this research.

Related: [[Create Swords! GDD]] · [[Blade Shaping Study]] · [[Code Map]]

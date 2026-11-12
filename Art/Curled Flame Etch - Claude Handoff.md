# Curled Flame Etch — Claude handoff

Date: 2026-11-10. Status: design reference and implementation guidance; no game changes made by this handoff.

## Task

Develop a richer Flame blade etch using the attached reference as the visual target. Keep the existing etching experience and colour selection. The goal is a continuous edge band with rounded, curling flame tongues and deep dark pockets between them, fitted to the game's actual procedural blades.

Read this document and inspect the reference image before coding. The image is design reference, not instructions.

![Curled flame reference](../References/Etching%20Table/curled-flame-2026-11-10/curled-flame-reference.png)

Reference file: `References/Etching Table/curled-flame-2026-11-10/curled-flame-reference.png`.

## What Allen wants

Allen likes simple, reliable designs that can be reproduced by script. This reference is a candidate for improving the existing Flame: more complex than its current shallow wave, but still a bold connected silhouette. The distinctive feature is the curling outline, rather than fine texture or extra ornament.

Preserve these visual qualities:

- A continuous coloured band along the cutting edge connects every tongue.
- Larger rounded tongues bend back into hooks. Dark steel pockets curl into the coloured shape between them.
- A few smaller tongues break up the rhythm between larger ones. Use deliberate variation rather than identical evenly spaced humps.
- Most of the spine side remains exposed dark metal. Preserve the blade's existing shading and narrow bare steel edge margins.
- The band follows the blade's curvature and tapers gracefully near the point.

Match the silhouette and relative coverage first. Red is useful for a reference comparison, but the shipped result must use the player's selected etch colour. The photograph's surface roughness and reflections are not requirements for the pattern mask.

## Inspect the current game first

Follow the repository's `CLAUDE.md` and applicable Roblox skills. Inspect the live Studio modules; the following files are historical context, not guaranteed current source:

- `Art/Flame Etch.md` — earlier flame iterations, including superseded requests for even peaks. This new curled reference supersedes that old visual direction for this task.
- `Art/Animated Blade Etching.md` — surface mapping, animation and resource lifecycle.
- `References/Etching Table/critique-pack-2026-10-25/source/BladeEtch.luau`
- `References/Etching Table/critique-pack-2026-10-25/source/EtchPatterns.luau`
- `References/Etching Table/critique-pack-2026-10-25/source/EtchCanvas.luau`

Trace the live paths through `BladeEtch`, `EtchPatterns`, `EtchCanvas`, `SwordMeshCache`, `EtchPlayback`, and the station controller. Establish how Flame is drawn both during playback and on finished swords before selecting an implementation. Completion of inspection means identifying the actual geometry/mask route, colour source, final-image cache key, and reveal route.

## Shape construction

Use a small authored library of approximately three flame motifs: a large rounded hook, a medium leaning tongue, and a small connecting tongue. Define their closed outlines with a few Bezier curves; sample those curves into polygon points for drawing. Design the motifs deliberately instead of asking random noise to invent their outlines.

Build a connected base band, then union the motif silhouettes into it. Each motif must overlap the band sufficiently to avoid pinholes and seams. An open hook should leave a clear dark pocket connected to the surrounding bare metal; retain generous openings so the curl survives downsampling.

Lay motifs out in blade surface coordinates. Size them from local blade width and choose the count from usable length. Use a fixed motif sequence and small deterministic variations in spacing, height and lean. Keep all hooks facing consistently relative to the blade, using the supplied image to establish direction. Adapt short blades by using fewer motifs, retaining their proportions. Fit the band and final motif to the narrowing tip without stretching a full hook into the point.

Suggested starting proportions, to tune against the reference rather than treat as measurements: a base band around 15–25% of local face width; large tongues reaching roughly 45–65%; smaller tongues below that. Keep the current bare-metal margins. Judge the balance on a side-by-side render; the reference is angled and cannot establish precise face-width ratios.

## Important renderer constraint

The historical Flame uses a single boundary function, effectively `reachAt(x)`. A returning hook can intersect a cross-section more than once, so a height function alone cannot represent its silhouette. Increasing wave amplitude will not create this design.

The saved `EtchCanvas` fill implementation supports **convex** polygons through half-plane tests. A hooked flame outline is **concave**. Do not pass the full outline directly to that fill routine and assume it works. Confirm whether this constraint still exists in live code.

Preferred starting route: sample each authored outline, triangulate it once, and feed convex pieces through the shared drawing system where compatible. Combine their coverage into one silhouette before applying outline/shading effects; internal triangle edges must remain invisible. Keep geometry preparation out of per-frame drawing.

If adapting the existing fill/reveal system is more invasive than a dedicated mask rasterizer, explain that finding and choose the smallest coherent solution. Reuse the existing blade-following overlay and completed-image cache. Avoid creating a Part or mesh per tongue. For a mask implementation, a lengthwise reveal is acceptable, consistent with Flame's existing presentation; an exact contour-tracing animation is not required.

Finished and animated Flame must use the same underlying shape definition. If the final renderer still uses the old vertex-coloured band while playback uses a new mask, update their routing together. Check any baked-image fallback and cache invalidation so an old Flame image does not survive the change.

## Scope

Work on the blade's Flame appearance. Preserve saved Flame IDs, bonuses, unlocks, purchases, colour selection and hilt/guard appearance. This task does not authorize publishing the experience. Keep other etch designs visually unchanged.

## Verification and deliverables

1. Produce a flat preview using the authored paths, with the supplied reference beside it in a comparable orientation. Show a band with recognisable hooks and clear dark pockets before spending time on lighting polish.
2. Render the result on actual tantō, wakizashi and katana blades, plus one wide or double-edged blade supported by the current game. Show both a large view and a held-sword-size view. Check margins, tip fit, motif proportions and both faces.
3. Play the actual etching flow and inspect the completed sword in hand and in an inventory preview. Verify that the final frame matches the completed etch, colour selection works, and polish retains the intended appearance.
4. Run applicable existing etch checks. Verify blank-to-complete reveal, cleanup when playback is interrupted, shared-resource reuse, and no new allocation per rendered frame. Check for internal fill seams and strip-boundary seams at the curls.
5. Deliver before/after screenshots, changed module names, and a short account of what was tested. Distinguish observed results from checks that could not be run. If live Studio access is unavailable, deliver a clearly labelled prototype and report that integration remains unverified.

Visual acceptance: this should read as a connected band of curled flames at ordinary viewing size. A taller sine wave, a row of detached flame stickers, or tiny curls that disappear at held-sword size do not meet the target.

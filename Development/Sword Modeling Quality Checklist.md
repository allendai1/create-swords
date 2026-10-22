---
title: Sword Modeling Quality Checklist
status: working reference
date: 2026-10-19
tags: [swords, modeling, blender, roblox, checklist]
type: "development"
updated: "2026-10-19"
---

# Sword Modeling Quality Checklist

A good game sword combines **a strong silhouette, intentional proportions, readable surface planes, cohesive materials, and controlled detail**. More polygons or decoration do not automatically make it better. Evaluate the big shapes before the small ones.

Use this checklist while modeling in Blender, reviewing a sword generated with Claude, and testing the imported asset in Roblox. These are art-review guidelines, not approved dimensions or engine limits.

## Fit the game's art direction

For *Create Swords!*, the current direction is grounded starter tantō, wakizashi, and katana with slightly exaggerated proportions and distinct silhouettes, followed by more extravagant special designs. Check [[Design/Game Design Document|Game Design Document]], [[Art/Sword Silhouettes|Sword Silhouettes]], and [[Development/Blade Profile Authoring|Blade Profile Authoring]] before changing a blade's identity or dimensions. Reference illustrations are not dimensioned specifications.

A central ridge, crossguard, fuller, or European-style pommel is **not mandatory**. Choose construction appropriate to the sword. A flat-sided blade can look excellent when its thickness, edge planes, and tip are intentional.

## Using this checklist to help Claude create better swords

Give Claude this note **before designing or modeling**, together with the intended sword type, the game's art direction, and visual references. Use it throughout creation as well as for the final review. It provides priorities and concrete checks; it does not guarantee an attractive result without visual judgment and revision.

1. **Set the design brief.** Identify whether this is a grounded starter blade or an extravagant special sword. Supply references, established dimensions, character scale, and any known asset budget. Explain what you like about each reference: its outline, proportions, color hierarchy, or restraint.
2. **Establish the main shapes.** Have Claude create a simple blockout and inspect black silhouettes from front, side, and three-quarter views. Resolve identity, proportions, and gameplay-size readability before adding decoration.
3. **Build the surfaces.** Develop intentional thickness, cross-section, bevels, tip construction, and hilt connections. Inspect gray clay views under neutral lighting; code that generates a mesh is not evidence that the mesh looks good.
4. **Add materials and selective detail.** Choose a cohesive palette and a clear focal point. Add only details that support the design and remain useful at the intended viewing distance.
5. **Inspect and revise.** At each stage, compare actual screenshots or renders against the brief and checklist. Fix the highest-impact visible weaknesses, then capture the same views again to judge the change.
6. **Validate in Roblox.** Check the imported sword with the actual character, camera, lighting, and motion. Keep any unavailable import or performance checks explicitly unverified.

**Evidence matters:** Claude should not mark every checkbox as passed merely because it intended to satisfy it. Visual claims require inspected images; mesh and performance claims require the relevant model data or measurements. If Claude cannot view the output or access Roblox, it should state the limitation and identify the evidence needed to continue that review.

The creation prompt below guides this process. The separate review prompt is for evaluating an existing result and proposing improvements.

### Applying the criteria to ornate Roblox swords

The criteria also apply to elaborate fantasy swords like the three examples discussed from another Roblox game. Their visible strengths were distinct silhouettes, cohesive silver-and-accent palettes, shaped hilts, and selective decoration. The broad, quieter blade on the red-accented sword and the distinctive hooked outline on the middle sword illustrate different ways to establish identity.

Use those principles as references for special swords while retaining the simpler direction of our starter blades. Small notches and fine markings still need a gameplay-distance check. A front screenshot can support a design assessment, but cannot establish blade thickness, bevel quality, hidden topology, or runtime performance. Treat these examples as visual references rather than fully verified models.

## Practical modeling checklist

Duplicate this section for each review. Check an item only after inspecting it; mark genuinely inapplicable items `N/A` with a short reason.

### 1. Silhouette and proportions — highest priority

- [ ] The sword is recognizable as a solid black shape at its expected on-screen size.
- [ ] Blade length, width, curve, and tip establish a clear identity.
- [ ] Related swords remain distinguishable when shown together at a shared scale; differences are not only color changes.
- [ ] Blade-to-grip and guard-to-blade proportions feel deliberate and fit the intended hand and character scale.
- [ ] Width taper, curvature, and tip transitions flow cleanly without accidental bulges, kinks, or abrupt narrowing.
- [ ] Front, side, and three-quarter views all work; the blade does not become an unintended paper-thin strip from the side.
- [ ] The silhouette has one clear focal idea, with supporting shapes that do not compete for attention.
- [ ] Exaggeration improves readability while preserving the chosen sword type and the game's grounded or fantastical direction.

### 2. Blade cross-section and bevels

The outline defines the blade's identity; the cross-section defines how its surfaces catch light. Two blades with the same outline can look very different if one is a flat slab and the other has intentional angled faces.

- [ ] The blade has an intentional cross-section appropriate to its design: flat-sided, ridged, diamond-like, or another justified form.
- [ ] Spine, blade faces, cutting bevels, and edge are distinguishable where the design calls for them.
- [ ] Broad planes produce readable light-and-dark changes under neutral lighting.
- [ ] Any ridge or fuller follows the blade's taper and curvature cleanly; neither is added solely to increase detail.
- [ ] Thickness and edge thickness are controlled along the blade and into the tip, without an accidental swollen point.
- [ ] The cutting edge reads as sharp at gameplay distance without relying on fragile, effectively invisible geometry.
- [ ] Bevel widths support the design's scale: large enough to catch light, restrained enough to avoid a melted or inflated look.
- [ ] The tip is deliberately constructed and shades cleanly from multiple angles.
- [ ] Surface smoothing preserves important planes instead of making the blade look rounded like a spoon.

### 3. Guard, grip, and pommel or end cap

- [ ] The guard or collar supports the blade's visual language and has a clear, intentional connection to it.
- [ ] Guard thickness and layering remain legible without overpowering the blade.
- [ ] The grip has enough usable space for the intended pose and number of hands.
- [ ] Grip shape, taper, wrap, or facets make it feel designed rather than an unmodified cylinder.
- [ ] Wraps and seams have consistent spacing and scale; they do not create visual noise.
- [ ] A pommel or end cap, where appropriate, finishes the grip and balances the composition.
- [ ] Parts align and meet convincingly, with no unintended gaps, floating ornaments, or visible interpenetration.
- [ ] Modular blade and hilt combinations are checked at their shared connection, including the widest and narrowest intended pairings.

### 4. Materials and color

- [ ] A limited palette establishes a dominant material, supporting material, and restrained accent where useful.
- [ ] Blade, grip, guard, and decorations separate through value and surface response as well as hue.
- [ ] Metal, leather, wood, or other intended surfaces are distinguishable under ordinary game lighting.
- [ ] Roughness and reflectivity support the style without turning every component into glossy plastic.
- [ ] The blade retains readable planes when bright reflections disappear.
- [ ] Accent colors reinforce the focal point and do not compete across every component.
- [ ] The design still reads in grayscale and against both light and dark backgrounds.
- [ ] The imported result is inspected in Roblox; the Blender appearance alone is not treated as proof of the final look.

### 5. Details and craftsmanship

- [ ] Detail follows a hierarchy: primary shape first, structural features second, small ornament last.
- [ ] Engravings, gems, wraps, and motifs fit a coherent theme and have a clear purpose.
- [ ] Quiet areas give the eye somewhere to rest.
- [ ] Wear, if present, is selective and placed where contact would make sense; it does not uniformly cover every surface.
- [ ] Repeated elements have consistent spacing, depth, and alignment unless variation is intentional.
- [ ] Small details survive at their intended viewing distance; otherwise they are simplified, enlarged, or removed.
- [ ] Decorative forms look attached or integrated rather than pasted onto the surface.

### 6. Topology, shading, and performance

- [ ] Geometry is concentrated where it improves silhouette, surface planes, deformation, or visible detail.
- [ ] Hidden faces and redundant subdivisions are removed when they serve no modeling or runtime purpose.
- [ ] There are no accidental duplicate faces, zero-area faces, flipped normals, or holes in surfaces intended to be closed.
- [ ] Hard edges and smooth surfaces are intentional; shading is checked before and after export.
- [ ] Triangulation does not introduce visible pinching or change the intended blade faces.
- [ ] Bevels and other modifiers produce the expected exported shape.
- [ ] UVs, where used, avoid unintended stretching and allocate resolution to visible areas; deliberate mirroring is documented.
- [ ] Triangle counts, texture sizes, material count, and separate parts fit the project's actual asset budget.
- [ ] Collision is kept as simple as gameplay allows, and visual decoration does not produce unintended interaction.
- [ ] Scale, orientation, origin or pivot, and attachment placement are verified after import.

There is no universal “good sword” polygon count. Judge cost against the number of swords visible at once, target devices, camera distance, and measured game performance. Clean shading matters more than forcing every static surface into quads.

### 7. In-game readability and polish

- [ ] The sword is identifiable at the normal gameplay camera distance, not just in a close-up render.
- [ ] Blade, hilt, and focal accent remain distinguishable while moving.
- [ ] The sword is checked against representative environments and lighting conditions.
- [ ] Equip, idle, attack, and other relevant poses have convincing hand placement and no distracting clipping.
- [ ] Effects, if present, support the sword without continuously hiding its silhouette.
- [ ] Similar weapons can be told apart at the sizes used in gameplay and inventory previews.
- [ ] The asset remains readable at the smallest intended display size and lower graphics settings.
- [ ] A representative scene with multiple visible swords performs acceptably on target hardware.

## Review workflow

### Pass 1 — Black silhouette

Render or display a solid black sword on a plain light background. Compare front, side, and three-quarter views, then shrink them to gameplay size. Compare related blades at a shared scale.

**Resolve:** identity, proportions, taper, curve, tip, and hilt balance. If the silhouette fails, return to the main shapes before adding ornament.

### Pass 2 — Gray clay render

Apply one neutral gray material to every part and use simple lighting that reveals the surfaces. Rotate the sword and light so one flattering angle cannot hide problems.

**Resolve:** cross-section, thickness, bevels, tip construction, part connections, and shading. Strong broad planes should remain readable without color or textures.

### Pass 3 — Final materials

Restore materials. Review under neutral light and lighting representative of the game. Inspect grayscale separation and light/dark backgrounds.

**Resolve:** material distinction, palette, focal hierarchy, roughness, and detail density. Materials should reinforce the geometry.

### Pass 4 — Roblox in-game test

Import the asset and inspect it with the actual character, camera, poses, and environment. Test at normal gameplay distance, in motion, and in an inventory preview if applicable. Include representative simultaneous asset counts and target devices.

**Resolve:** scale, grip and attachment alignment, clipping, lost details, material differences, effects, and runtime cost. Return to the earliest failing pass, fix the underlying issue, then recheck later passes affected by that change.

Save comparison images from consistent views so revisions can be judged fairly.

## Weighted 100-point scoring rubric

Score each subcriterion from **0 to 5**: 0 = missing or broken; 1 = major problems; 2 = needs substantial work; 3 = acceptable; 4 = strong; 5 = excellent at the intended viewing distance.

**Points earned = maximum points × rating ÷ 5.** Add all points and round only the final total. These weights are a review aid, not a validated quality standard.

| Category | Subcriterion | Maximum points |
|---|---|---:|
| Silhouette / proportions | Recognizable identity and distinction from related swords | 15 |
| | Blade, hilt, and character-scale proportions | 12 |
| | Taper, curve, tip, and outline flow | 8 |
| **Silhouette / proportions subtotal** | | **35** |
| Geometry / construction | Cross-section, blade planes, and thickness | 10 |
| | Bevels, edge, and tip construction | 8 |
| | Hilt connections, mesh integrity, and shading | 7 |
| **Geometry / construction subtotal** | | **25** |
| Materials / colors | Palette, value separation, and focal hierarchy | 8 |
| | Material distinction and surface response | 7 |
| **Materials / colors subtotal** | | **15** |
| Detailing / craftsmanship | Purposeful detail, theme, and restraint | 8 |
| | Alignment, spacing, finish, and selective wear | 7 |
| **Detailing / craftsmanship subtotal** | | **15** |
| Gameplay readability / polish | Readability at gameplay distance and in motion | 5 |
| | Import, hand fit, clipping, and performance | 5 |
| **Gameplay readability / polish subtotal** | | **10** |
| **Total** | | **100** |

Suggested interpretation:

- **90–100:** Strong candidate for final acceptance after all required in-game checks.
- **80–89:** Strong overall; fix the few weaknesses that still affect the presentation.
- **70–79:** Serviceable, but needs another targeted pass.
- **Below 70:** Revisit the largest shape or construction weaknesses before adding detail.

Score appropriate execution, not feature count: a clean, undecorated blade can earn full detailing points. If evidence is unavailable, mark the subcriterion **unverified** and report the earned points against only the assessed maximum; do not invent a full 100-point score. Unresolved import failures, serious clipping, or unacceptable performance block final acceptance regardless of the art score.

## Common flaws and practical fixes

| Flaw | What to change |
|---|---|
| Looks generic despite lots of decoration | Revisit blade profile, tip, guard, and proportions in silhouette. Establish one recognizable feature. |
| Blade looks like a flat plank | Design its cross-section and cutting planes; test them in gray clay. Add a ridge only if appropriate to the blade type. |
| Blade looks soft or inflated | Reduce oversized bevels, restore broad planes, and inspect smoothing and normals. |
| Tip looks swollen, pinched, or abruptly cut off | Rebuild the width and thickness transitions together; inspect both outline and side view. |
| Starter blades look like resized copies | Compare at shared scale and refine their intended curve, taper, tip, and hilt relationships. Check established design references first. |
| Guard dominates or grip feels unusable | Rebalance against the blade and test with the actual character hand and poses. |
| Metal reads as plastic | Review surface response and lighting, then confirm the result in Roblox. Do not rely only on darker color or stronger shine. |
| Materials blend into one muddy mass | Improve value separation and simplify the palette; reserve the strongest contrast for the focal area. |
| Ornament becomes noise or disappears | Remove low-value detail, enlarge selected motifs, and preserve quiet surfaces. |
| Shading contains streaks or dents | Check topology, normals, smoothing, bevel intersections, and exported triangulation. |
| Fine in Blender, weak in-game | Inspect actual camera distance, lighting, scale, and materials; exaggerate only the forms that lose readability. |
| Too expensive when many swords are visible | Remove unseen geometry, simplify small forms, reduce unnecessary material or part splits, and retest the representative scene. |
| Modular parts have gaps or collisions | Check connection dimensions and alignment across the intended blade/hilt combinations. |

## Reusable Claude design and modeling prompt

Use this when commissioning a new sword or a substantial model revision. Fill in the brief and provide this note plus the relevant references.

```text
Design and model a sword in Blender for Create Swords! in Roblox, using our
Sword Modeling Quality Checklist throughout the work.

Sword identity and theme: [name, type, and intended character]
Art direction: [grounded starter or extravagant special sword]
Visual references and what to learn from them: [images and specific qualities]
Established dimensions and modular connections: [constraints or unknown]
Target character, camera distance, and display size: [details]
Asset budget and target devices: [constraints or unknown]
Deliverables: [Blender file, export, comparison views, etc.]

Read the relevant vault art direction and blade specifications first. Preserve
established decisions. State any assumptions where the brief leaves room for judgment.

Work in stages:
1. Block out the blade and hilt. Establish a recognizable silhouette, deliberate
   proportions, and one clear focal idea. Inspect front, side, and three-quarter
   black silhouettes at both close-up and intended gameplay size.
2. Resolve the main shape weaknesses before decorating. Model an appropriate
   cross-section, thickness, edge planes, bevels, tip, and convincing connections.
   Do not add a ridge, fuller, guard, or pommel solely to satisfy a generic formula.
3. Inspect neutral gray clay views. Correct shading problems, weak planes,
   awkward transitions, and unintended gaps before moving to final materials.
4. Add a cohesive palette and selective detail. Keep quiet areas and preserve
   the silhouette. Check value separation and readability when viewed small.
5. Inspect the actual rendered output after each meaningful revision. Describe
   the most important visible weaknesses, fix them within the authorized scope,
   and compare matching views. Do not equate successful script execution with
   a successful visual result or claim checks passed without evidence.
6. When Roblox access is available, inspect the imported sword with the intended
   character, camera, lighting, and poses, and assess the relevant asset budget.
   Otherwise mark those checks unverified and provide a concrete test handoff.

Use the 100-point rubric to assess the result, retaining its exact subcriterion
weights. Report earned points against only the assessed maximum when evidence
is incomplete. Do not invent a full score or inflate ratings to declare success.

Deliver the requested files and comparison views, a brief account of the visual
improvements, and any unresolved issues or unverified checks. If image inspection
or required tools are unavailable, state what could not be assessed and what is
needed; do not present an uninspected model as visually approved.
```

## Reusable Claude review prompt

Copy this prompt and supply the relevant images, model data, and project constraints.

```text
Review this stylized game sword for Create Swords!, modeled in Blender for Roblox.

Sword / intended identity: [name and type]
Art direction: [grounded starter or special design; references]
Target character, camera distance, and display size: [details]
Asset budget and target devices: [known constraints, or unknown]
Evidence supplied: [silhouette views, gray clay views, final material views,
Blender mesh information, Roblox screenshots/video, performance measurements]

Use our Sword Modeling Quality Checklist. Prioritize silhouette and proportions,
then construction, then materials and detail. Judge the intended sword type;
do not require a ridge, fuller, crossguard, or European-style pommel on every sword.
Preserve established project dimensions and design decisions unless you explicitly
identify a reason to propose a change.

1. State what you can assess from the supplied evidence and what remains unverified.
   Do not infer hidden topology, triangle counts, performance, or successful Roblox
   import from a render. Request the specific evidence needed for those checks.
2. Identify the three highest-impact weaknesses. For each, give the visible evidence,
   why it matters at gameplay distance, and a concrete Blender or in-game fix.
3. Review silhouette/proportions, blade cross-section/bevels, guard/grip/end cap,
   materials/colors, detailing, topology/performance, and gameplay readability.
   Separate observed problems from hypotheses and optional stylistic alternatives.
4. Apply the rubric's subcriterion weights with 0–5 ratings:
   silhouette/proportions 35; geometry/construction 25; materials/colors 15;
   detailing/craftsmanship 15; gameplay readability/polish 10.
   Show points and reasons. If evidence is missing, mark it unverified and report
   earned points / assessed maximum instead of inventing a full 100-point score.
5. Recommend fixes in this order: black silhouette → gray clay → final materials
   → Roblox in-game test. Give a specific recheck for each proposed fix.
6. Name the strongest features to preserve. Prefer a few meaningful improvements
   over adding more decoration or polygons. Flag any issue that blocks acceptance
   regardless of score.

Give the review first. Do not modify the model unless I have authorized edits.
```

Related: [[Home]] · [[Design/Game Design Document|Game Design Document]] · [[Art/Sword Silhouettes|Sword Silhouettes]] · [[Archive/Art/Blade Shaping Study|Blade Shaping Study]] · [[Development/Blade Profile Authoring|Blade Profile Authoring]] · [[Development/Blade Implementation Research|Blade Implementation Research]]

Source: Adapted and expanded from the “Sword Model Checklist” conversation, with the vault's current art direction used as context.

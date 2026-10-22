---
title: Animated Blade Etching
type: design-handoff
status: v1 built 2026-10-21 (Eclipse + Flame playback); the other five patterns built 2026-10-22; Edit-mode checks pass; playtest pending
updated: 2026-10-22
tags: [etching, blades, implementation, handoff]
---

# Animated Blade Etching

Players should watch the pattern being etched onto their actual procedural sword on the Etching Table. An engraving tool follows the design, and the material-coloured marks appear directly behind its tip. Keep the existing blade generation and extend the decorative surface rendering.

Allen requested this handoff for Claude on 2026-10-21 after reviewing new pattern concepts and asking whether visible etching works with the current blades. This document records the requested experience and a recommended first implementation. It is not a Studio inspection or a claim that anything here has been built.

## Scope and first deliverable

- Requested: visible, progressive etching on the real blade shape, compatible with the existing procedural swords.
- Recommended v1: automatic stroke-by-stroke playback after choosing a sword and pattern. The player watches; cursor tracing, scoring, failure, prices and new bonuses remain outside this change.
- Start with **Eclipse** as a proof pattern because its separated rings and gaps exercise the new renderer. This is an implementation recommendation, not evidence that Allen selected it as the only final pattern.
- Preserve the existing Flame option and appearance. Give it visible playback too, using a lengthwise reveal if an exact tracing path would unnecessarily delay the first working version.
- The other five new designs are candidates, not a requirement to ship all six in this first pass. Build the pattern format so they can be added without rewriting the renderer.
- Keep the existing optional station placement/order, material colours, sword quality, hilt rules and +15% etch bonus. Re-etching replaces the finish rather than stacking bonuses.

## Experience on the table

1. Use the existing finished-sword picker, then the pattern picker.
2. Stage a correctly scaled copy of the selected sword flat on the player's own Etching Table. Use its real blueprint, material, refinement/polish and hilt rather than a generic katana illustration.
3. Frame the whole blade with a slightly angled overhead station camera. Preserve visible curvature; adjust framing for tantō, wakizashi and katana. Begin with minimal UI and the existing back/close interaction.
4. Once the server accepts the etch, clear the preview's previous decorative etch and begin the new pattern. This removal is presentation on the staged copy only.
5. A small engraving stylus traces ordered paths on the face. The visible mark grows immediately behind the contact point. Lift the tool and stop contact effects while moving between disconnected strokes.
6. Use restrained contact sparks and a quiet scratch sound only while drawing. Reuse an appropriate available sound or report a missing asset; do not invent a working sound asset ID.
7. Show the completed blade for a short inspection beat, then restore the normal camera and controls. The finished pattern appears consistently on the held sword, displays, picker cards and hotbar.

Suggested tuning defaults, not approved balance: approximately 3 seconds of drawing plus a 0.4-second inspection beat, configurable together. Weight timing by stroke length so short arcs do not take as long as a full-blade line. Provide a way to leave playback without losing the accepted finish.

## Existing implementation to inspect first

Read [[Development/Code Map]], especially **Sword meshes, ingot ore and station order** and **Six player plots**, plus [[Art/Flame Etch]]. Inspect the live scripts before changing them: the vault has older entries that describe superseded per-sword meshes and shared Workspace stations.

| Component | Recorded responsibility / implication |
|---|---|
| `Shared/BladeCore`, `Shared/BladeView` | Procedural station-based blade geometry. Reuse the actual profile and surface information. |
| `Shared/BladeEtch` | Two-colour skin just above both blade faces. Existing Flame uses a single edge-to-spine colour boundary along the length. Disconnected rings and branches need a richer representation. |
| `Shared/SwordMeshCache` | Finished swords share colour-neutral meshes. Recorded API: `blade(bp, refinement)`, `etch(bp, refinement, pattern, body)`, `release(key)`. Inspect actual keys and reference counting. |
| `Shared/Etches` | Pattern registry and material-derived colours; keep existing material lookup/fallback behaviour. |
| `EtchingTableController` | Sword/pattern pickers; natural owner for the local station presentation and its cleanup. |
| `EtchService` | Server validates and applies the selected etch, rebuilds the Tool and pushes state. |
| `SwordRenderer`, `ItemPicker`, `Hotbar` | Final sword appearance and inventory previews; all must show the same selected pattern. |
| `MyPlot`, `PlotService` | Resolve the player's own station. The upgraded store can move the workshop; use current table transforms. |

## Rendering approach

### Surface coordinates

Extend the existing blade-following skin with texture coordinates. A point on the pattern should describe both its position along the blade and its position across the local blade width. Use the same sampling to locate the tool tip on the 3D face.

- The overlay follows the refined blade's curve, taper and bevel/ridge geometry on both faces. Reuse or expose the surface sampling used by the blade/etch builders; a bounding-box plane will not follow the blade.
- Preserve narrow bare-metal strips at the cutting edge and spine, consistent with the current finish.
- Define pattern paths in blade-relative coordinates with length/width-aware spacing. Simple normalization alone can stretch circles across different blade proportions. Adjust repeat count and spacing by blueprint; taper or omit motifs near the tip rather than crushing them into it.
- Mirror the opposite face deliberately and keep both faces aligned. V1 may etch the visible face while preparing the matching reverse pattern for the finished sword; a second full animation or blade flip is optional polish.
- These are coloured surface markings. Physical engraved grooves and changes to the forged silhouette are outside v1.

### Pattern definition and drawing order

Keep one pattern definition responsible for both its completed image and its progressive reveal. A useful record contains an ID, display name, ordered strokes/shapes, width/spacing rules and supported colour roles. Match the project's current module conventions rather than introducing a framework.

For a line-like stroke, store a path plus a width profile. For a broad filled motif, store its filled shape and a drawing guide; progressively reveal only the part covered by the guide/brush. That prevents the final result from depending on an unrelated second artwork file.

- Represent a stroke with points in the blade coordinates above, pen-up travel between strokes, and a duration weight derived from path length.
- Use the same coordinates to advance the tool and reveal the next section of the image. Advance by travelled distance rather than point index, so irregular point spacing does not make the tool jump.
- At progress 0 the new pattern is absent. Progress only increases, and progress 1 exactly matches the completed pattern, including disconnected details and gaps.
- Keep visible stroke thickness sufficient for a held sword and an inventory viewport. The concept sheet's fine detail is a visual direction, not a guarantee of readability at game scale.

### Temporary drawing texture and completed finish

Recommended route: one mutable `EditableImage` for the active local table preview. Draw/copy bounded regions as strokes advance, using current supported Roblox image APIs. Start with a modest texture such as 1024 × 128, then adjust after inspecting the real mapped blade and checking current API limits.

Only the in-progress preview owns mutable drawing state. Completed swords use reusable final pattern textures/masks and the existing shared-mesh strategy. Runtime-generated final images, if needed for blueprint or colour variants, are cached and reference-counted; ordinary finished swords do not each allocate their own live canvas.

The final layer should preserve the dark body, material-derived accent, bright edge strips and existing shading intent. Verify how vertex colours, MeshPart colour and texture colour multiply in the live renderer; avoid tinting the accent twice or losing the blade's material identity. Existing Flame can fall back to its current vertex-coloured renderer if image creation fails. For a new pattern, prepare its visual resources before submitting the apply request; a preparation failure preserves the current finish. If rendering fails after acceptance, preserve the accepted inventory record, restore controls and report a visual retry outcome rather than silently showing Flame as Eclipse.

**Cache ownership is critical:** mutating a mesh/image borrowed from `SwordMeshCache` can change every sword sharing it. Clone the preview's visual instances as needed, allocate only the mutable resources the animation actually requires, and leave borrowed shared resources unchanged. Add the pattern identity to relevant final cache keys; include any baked colour/blueprint variant that genuinely changes the cached output. Preserve reference counting and free only resources owned by the closing session.

## Authority and interruption behaviour

Recommended v1 keeps the existing instant server etch as the authoritative operation; the new animation is cosmetic playback of an accepted result. This preserves the current free/instant gameplay semantics while adding something to watch.

1. The client sends the existing sword ID and pattern ID, following the current remote convention.
2. The server validates ownership, valid/allowed pattern, the player's own unlocked station, reach and existing sword eligibility; applies one finish through the canonical sword record; then returns/publishes the accepted result through a correlated response.
3. The controller starts playback only for that accepted sword/pattern request. Reuse existing response/state mechanisms when possible; add a small request token or revision if required to distinguish old responses from a new selection.
4. The preview is a cosmetic copy; the real sword is never removed from canonical inventory for the animation. Prevent a duplicate visible equipped sword during the station view using the project's existing presentation conventions.
5. Closing the view, walking away, death, respawn, plot release, table streaming out or presentation failure ends playback and restores control. A server-accepted finish stays applied. A rejected request preserves the old finish and returns cleanly to the existing flow.
6. Prevent overlapping local presentations and stale callbacks. Server validation/rate limits still apply to repeated requests. Never trust client brush pixels, colour values, progress or elapsed time to award an etch.

Only the requesting player needs to see the tracing animation in v1; other clients still see the canonical finished sword. This is a scoped implementation default, not a decision that shared table animations are impossible. If observers are added later, replicate an accepted pattern ID, sword appearance, start time and session token; draw effects locally instead of streaming pixels or per-frame tool positions.

If live inspection shows existing etch rules require a timed transaction, report that discrepancy before replacing the above with reservations, partial-progress saves or completion rewards. Those introduce different gameplay and lifecycle rules.

## Built (2026-10-21)

Allen asked to implement the handoff: stage the sword on the Etching Table, move an engraving tool along the pattern, and reveal the material-coloured marks behind it. Eclipse proves the textured overlay and stroke animation; Flame keeps its look and gets a lengthwise reveal; the other five concepts stay candidates. It plays automatically; there's no tracing minigame.

![[References/Etching Table/eclipse-static-blades-materials.jpg]]

*Eclipse on the real overlays: katana in Iron, Copper and Blue Steel, wakizashi Iron, tantō Copper, and a katana flipped to show the reverse face.*

![[References/Etching Table/eclipse-progress-12-38-62-100.jpg]]

*The show on the table at 12%, 38%, 62% and 100% (copies lifted out and enlarged ×4 for the capture): connectors first, then the rings, then the star; the stylus lifts between strokes.*

![[References/Etching Table/eclipse-staged-on-table.jpg]]

*The katana staged on the template plot's Etching Table, demo tray hidden (Edit capture from further back than the in-game camera).*

![[References/Etching Table/flame-preview-vs-held.jpg]]

*Flame preview after its reveal (top) next to the cached held-sword Flame (bottom): the same band.*

### How it works

| Piece | What it does |
|---|---|
| `Shared/EtchPatterns` (new) | Pattern definitions as ordered strokes of `{ x, y, h }` in real centimetres on the face (x along, y across from the edge line, h half-width). Eclipse: connector pieces with diamond nodes, then for each ring an open crescent and a small inner sliver (gaps alternate toward the tip and the hilt), then a four-point star before the tip. Rings are 0.33 of the local width in radius; ring count comes from the usable length (4 on the katana, 3 wakizashi, 1 tantō); motifs stop 1.9 widths short of the tip. |
| `Shared/EtchCanvas` (new) | The face unrolled into an image: 1024-pixel strips of 128 rows, as many as keep a pixel about square on the steel (katana 1024×384, wakizashi 1024×256, tantō 1024×128). Strokes are cut into pieces of at most 0.1 cm; `reveal(d)` rasterises every piece ending within d cm of pen-down travel with coverage-based anti-aliasing (coverage only grows, so any reveal order ends in the same pixels). `at(p)` gives the tool's place, with lifts three times faster than drawing. Colours are baked: Flame's dark body with its cool bevel sheen, marks in the material colour darkening away from the light. |
| `Shared/BladeEtch` | `surface(params)`: the face by x cm and w (and `swAt`, local widths from the base), used by the overlay and the stylus tip. `buildTextured(S, L)`: both faces, UV-mapped to the strips, no texture of its own. `bandReach(S, pattern)`: a band pattern's reach, so Flame can be drawn into a canvas. `build` is Flame's vertex skin, unchanged. |
| `Shared/SwordMeshCache` | `overlay(bp, refinement)`: one overlay mesh per blueprint and polish level, shared by every stroked pattern and material (a clone plus `{ surface, layout }`). `etch(bp, refinement, pattern, body, accent?)`: a stroked pattern is a finished canvas on a share of that overlay, keyed with the accent colour (one image per blueprint, polish level and material colour, no extra mesh); Flame's key is unchanged. Release frees the image and the overlay share. `SwordRenderer` and `ItemPicker` pass the accent. |
| `Shared/Etches` | `Eclipse` added: +15% like Flame, same dark body, fallback mark colour 196,214,236; material colours as before. |
| `EtchPlayback` (new, client module) | `prepare(top, sword, etch, viewer)` builds the copy on the player's own table before anything is requested, making no mesh of its own: the cached blade, the cached finished etch (fetched and held to prove it can be built; the sword wears it next), and a share of the overlay with a private blank canvas as its texture, drawn stroke by stroke (Eclipse) or as a band from the base up with the stylus riding the band's wavy edge (Flame); the hilt dressed for the new etch, a stylus (wood shaft, brass ferrule, steel point), sparks and a small glow in the mark colour. The sword lies flat, centred, edge toward the player, resting on its guard, 0.12 studs forward of the jars; the demo tray is hidden locally. `step(p)`, `cameraCFrame(fov, viewport)` (74° down, fits the whole sword), `destroy()` frees exactly what the session owns. |
| `EtchingTableController` | Prepare → `EtchSword` → on acceptance the show: 3.0 s drawing + 0.4 s to look, camera and player frozen, prompt off, `EtchHud` close ring (top right); Q / Backspace / B or the ring leave early. Death, character removal, the table leaving the workspace or a drawing error end it; a request token makes a late response or one from before a respawn stale. The etch stands however the show ends. |
| `Hotbar` | Hides while `EtchHud` is enabled. |
| `EtchService` | Unchanged: it already validates the sword, the pattern (now including Eclipse), the player's own bought table, reach and rate, and replaces any earlier etch (no stacking). |

### Differences from this handoff

- **A MeshPart's `Color` doesn't tint a texture, and transparent texture pixels don't show it either** (tested in Studio). So the stroked marks bake the material colour and the cache keys on it, instead of one colour-neutral image tinted per sword.
- A `SurfaceAppearance` in Overlay mode *does* show `Color` through transparent pixels, but its texture properties were only proven settable from a plugin, not from a game script, so it wasn't used. Worth revisiting to cut images to one per blueprint.
- Vertex colours multiply a texture, so the overlay has none; shading is baked into the pixels.
- The stylus has no scratch sound: the place has no suitable sound asset (only the anvil clang). A hook is left in `EtchPlayback`.
- Flame plays as a lengthwise reveal along its band, not a traced path. During the show it's drawn into a canvas (same shapes, colours and shading as the vertex skin); swords keep the vertex skin.

### Verified in Studio (Edit mode)

- `ServerStorage.Tests.EtchingSpec`, run with `print(require(game.ServerStorage.Tests.EtchingSpec:Clone())())`: 29 checks, 0 failed at first (32 after the fixes below). They cover:
  - **Canvas:** progress 0 is blank; coverage never decreases. Progressive drawing equals the finished image byte for byte, in the buffer and the uploaded image, on all three blades. Lifts draw nothing.
  - **Tool:** the stylus surface sits on the real blade (raycast at base, middle and tip × edge, middle and spine; worst gap 0.0005 studs).
  - **Cache keys:** separate keys per material for Eclipse; Flame's key unchanged.
  - **Isolation:** the show draws on its own image and the shared finished image stays byte-identical. Another sword holding the same cache entry keeps the shared image.
  - **Cleanup:** the tray is hidden and restored. Twelve open/step/close runs (4 stopped early; Flame and Eclipse; three blades; Iron, Copper and Blue Steel) return sessions, cache entries and canvases to their baseline. A double close is harmless.
  - **Failure:** a simulated image-allocation failure makes preparing fail cleanly, with nothing left allocated, so nothing is requested.
  - **Flame:** the fully revealed hidden band equals the normal Flame skin (5,664 faces).
- Static renders on all three blades and three contrasting materials, both faces (screenshots above). Build time 0.08–0.25 s per blade/material image.
- Camera framing computed for 1582×753, 1280×720 and 844×390 viewports: the whole sword spans 70–86% of the width, centred.
- All changed scripts compile.

### Not yet verified (needs a playtest)

- The real flow in Play: picker → show → camera → close ring / Q / Backspace / B → toast. Camera, freezing and controls restored. Hotbar hidden during the show.
- Interruptions in a live client: dying or respawning mid-show; spamming the prompt; a rejected request (locked table, too far).
- Two players at their own tables (Test → Clients and Servers): no cross-talk, and other players see only the finished sword.
- Upgraded workshop (moved table).
- Held, displayed, picker and hotbar swords showing Eclipse in a live client.
- More than 20 visible swords, including viewport previews: memory and frame time, and the EditableImage budget on a lower-memory client. Each material and blueprint pair adds a 0.5–1.5 MB image.
- A failed image allocation in a live client: there, `SwordRenderer` would show the sword without its etch. Preparing at the table fails safely (checked above).

### After the first playtest (2026-10-21)

Allen: "works, but going from etching -> polish, the etch isn't present during the polish?" and "\"couldn't prepare that etch\" when trying flame".

- **Flame couldn't prepare** because the client hit Roblox's EditableMesh memory budget ("Failed to create empty EditableMesh … memory budget limits" in the console). The Flame show built a private mesh, and each Eclipse material had built its own copy of the same overlay mesh. Some held swords' etches failed to draw for the same reason.
  - **Fix:** one overlay mesh per blueprint and polish level is shared by every stroked pattern and material (`SwordMeshCache.overlay`). A material now costs only an image.
  - The show makes no mesh of its own: Flame is drawn into a canvas on that shared overlay (`EtchCanvas:revealBand`). The private hidden-band Flame skin is gone.
- **The Polishing Station showed no etch:** `PolishController` lays the sword's cached etch on the polishing blade. It uses the material colours EtchService stores, follows the cache's polish level, and is fetched again only when that level changes. Polishing only moves the edge line (at most 0.14 cm, measured), so the etch stays on the live blade.
- **Checks:** `EtchingSpec` now has 32 checks, 0 failed. The new ones:
  - Two Eclipse materials share one overlay mesh.
  - A second show on the same blade adds no meshes (Flame and Eclipse).
  - Flame's band only grows and ends as the band.

  The Flame show was rendered next to a held Flame sword (below).
- **Not verified:** the Polishing Station etch in Play; the budget with many swords on screen.

![[References/Etching Table/flame-band-show-50-100-vs-held.jpg]]

*Flame show at 50% and 100% (canvas on the shared overlay), and a held Flame katana (vertex skin), Copper.*

### Mesh leak found (2026-10-21)

Allen couldn't etch an iron tantō in the next playtest. Every new EditableMesh failed, even an empty one and the Polishing Station's own blade, while only 7 distinct meshes were in view, so meshes were alive but unseen.

- **Likely cause:** `SwordRenderer` gave a sword's meshes back only on its Tool's `Destroying`. Checked in Studio: `Destroying` fires when an ancestor is destroyed, but not when an instance merely leaves the game. On a client, tools the server destroys (re-etched, polished, sold, respawn) can arrive as a removal, so their cache shares were never released.
- **Fix:** `SwordRenderer` also frees on `CollectionService:GetInstanceRemovedSignal("ForgedSword")`, the free is idempotent, and in-flight builds check `IsDescendantOf(game)`.
- **Less demand:** picker cards and hotbar slots now pass the sword's polish (`art.refinement`), so they share the sword's own meshes instead of holding unpolished-level copies.
- `EtchingSpec` is still 32/32. Edit allows 400+ meshes, so the client budget (about a dozen, measured earlier) can only be checked in Play.
- **Not verified:** that this was the whole leak. That needs a playtest: etch, polish and respawn several times, then etch again.
- Backups: `ServerStorage.Legacy.*_beforeMeshLeakFix` (SwordRenderer, PolishController, Hotbar, ItemPicker).

### Polish shows on an etched sword (2026-10-21)

Allen: "i notice that it lags when i go from etching -> polishing. the look also stays the same. is this intended?" Neither was intended. He chose "Etch gets a sheen" from three options; the others were a bare cutting edge and a see-through etch on the bench.

- **Why the look stayed the same:** both etch skins cover the whole face, edge to spine, and polish brightens that face. So an etched blade looked identical at every polish, on the bench and in hand.
- **The sheen:** the etch's dark body now lifts toward the cool sheen (150, 190, 230) at each polish level the cache draws (0, ½, 1):
  - Eclipse by up to 0.3;
  - Flame by up to 0.6, because its skin is multiplied by the band colour. On Copper that gives a dark-brown glow; on lighter metals, a steel blue.

  Picked from renders on Copper and Iron; 0.45 for both washed out Eclipse's copper marks.
  - It's computed in `SwordMeshCache.etchBody`. The etching show uses the same colour, with Flame's body pre-tinted, so it ends on what you'll hold.
  - The 6 Flame bakes at levels 1 and 2 were re-baked.
- **Why it lagged:** crossing 25% or 75% while polishing fetched the next level's etch at once. For Eclipse that's painting a 1024×384 image: about 100 ms blank plus 75 ms of strokes (katana, Studio).
  - **Fix:** the bench fetches it in the background, spread over frames (`EtchCanvas` yields after about 4 ms per frame), and keeps the current etch until the next is ready.
  - After leaving, the bench holds its etch 5 s, so the saved sword's Hotbar and held art reuse it instead of rebuilding it.
- **Checks:**
  - `EtchingSpec` 33/33; the new check is that a spread build yields and draws the same image.
  - `SwordMeshSpec` 110/110.
  - Everything compiles.
- **Not verified in Play:** how the sheen reads at the bench, and whether the hitch is gone.

### Five more patterns (2026-10-22)

Allen asked for the concept sheet's other five to be built: Tide, Stormroot, Woven Wind, Fracture and Falling Stars. Each is a stroked pattern like Eclipse: the stylus draws it on the table, and held, displayed, picker and hotbar swords wear it. All are free for now (Allen), +15% like the others.

![[References/Etching Table/etch-six-patterns-katana-iron.jpg]]

*The six stroked patterns on Iron katanas, as the cache builds them for held swords: Eclipse, Tide, Stormroot, Woven Wind, Fracture, Falling Stars.*

![[References/Etching Table/etch-five-wakizashi-copper-tanto-bluesteel.jpg]]

*The five new patterns on Copper wakizashis and Blue Steel tantōs.*

| Pattern | What's drawn, in order | Katana / wakizashi / tantō |
|---|---|---|
| Tide | One ribbon low on the edge side: trough, a long back rising to each crest, then the face dropping straight down into the next trough. Then each crest's curl, forward over the hollow to a claw. Then a thin current under each back. | 4 / 3 / 2 crests (at least two) |
| Stormroot | The trunk first: a zigzag across the middle, thick at the guard, kinked between turns, thinning to a point. Then each angular branch (forking outward and forward) and its twig. | 47 / 34 / 16 strokes |
| Woven Wind | Two ribbons twisting round each other, widest where they cross and narrow at the turns. At each crossing one passes over and the other breaks into tapered points around it, alternating. First ribbon, then second. | 3 / 2 / 1 twists |
| Fracture | Filled shards between dark faults (5% of the width) in a band that narrows along the blade: broad panels at the guard, some split diagonally, then diamonds and slivers toward the tip, a few missing. The stylus scribbles over each shard, guard end first, and the shard appears behind it. | 26 / 18 / 9 shards |
| Falling Stars | Per star: two long tapered trails falling toward the edge and the tip, then the star (long upright rays, a long streak back toward the guard, two short diagonals). | 3 / 2 / 1 stars |

Sizes come from the local blade width, so the shapes keep their proportions on all three blades, and motifs stop short of the narrowing tip (checked below).

![[References/Etching Table/tide-progress-15-40-70-100.jpg]]
![[References/Etching Table/stormroot-progress-15-40-70-100.jpg]]
![[References/Etching Table/woven-wind-progress-15-40-70-100.jpg]]
![[References/Etching Table/fracture-progress-15-40-70-100.jpg]]
![[References/Etching Table/falling-stars-progress-15-40-70-100.jpg]]

*The real show (`EtchPlayback`) at 15%, 40%, 70% and 100%, lifted off the table: Tide in Iron, Stormroot in Blue Steel, Woven Wind in Mythril, Fracture in Gold, Falling Stars in Starmetal. The stylus lifts between strokes. Studio drew the stylus's sparks attachment as a green ball, so it was removed from these copies only.*

![[References/Etching Table/fracture-show-camera-55.jpg]]

*Fracture at 55%, in Copper, framed by the show's own station camera (`cameraCFrame`).*

![[References/Etching Table/pattern-card-art-seven.jpg]]

*The seven pattern cards' sword art from `ItemPicker.artModel`, laid out in the world (the real cards are viewports with their own light).*

**How it's built:**

- `Shared/Etches.list`: five entries (`Tide`, `Stormroot`, `WovenWind` "Woven Wind", `Fracture`, `FallingStars` "Falling Stars"). Each has Eclipse's dark body and fallback mark colour, and its mark colour comes from the material as before. The pattern picker, `EtchService`, `SmithyCore` and the card art all read this list. The picker grid shows two cards per row and scrolls to the rest. No new guards: only Flame has one.
- `Shared/EtchPatterns`: one generator per pattern in `STROKED`, plus small shared helpers. Eclipse's strokes are unchanged (compared point by point).
- `Shared/EtchCanvas`: **filled shapes**. A stroke may carry a `fill`, a convex polygon. Its points are the guide the stylus scribbles along, and each piece reveals the columns of the shape it has passed, with the shape's own anti-aliased edge. The corners stay sharp, and it costs about one pixel test per pixel of the shard. Progress 1 still matches the finished image byte for byte.
- **A seam where texture strips meet.** A katana's image is three strips (a wakizashi's two), and a faint dark line one texel wide shows across any mark at 1/3 and 2/3 of a katana (1/2 of a wakizashi). The texture wraps at the baked overlay's UV edge there. It's older than this change; Eclipse's marks cross it too. Fracture's broad shards made it obvious, so Fracture puts an upright fault on each seam (`EtchCanvas.strips`). The real fix is to inset the overlay UVs by half a texel and re-bake the overlays (roadmap).
- **The pattern picker's cost.** It builds a finished image per stroked pattern on the chosen sword, all at once. With six that was about 0.85 s on a katana in Studio, against 0.14 s with Eclipse alone. Two changes bring it to about 0.4 s:
  - `EtchCanvas` keeps each blank image (by layout and body colour; it goes with its layout) and copies it, instead of painting it again. Painting the blank was about 82 ms of each build.
  - Pixels a stroke has already fully covered are skipped.

  Stroke pixels are byte-identical to the canvas from before today.
- The show still draws for 3.0 s whatever the pattern, so the stylus moves faster on the longer ones: Fracture's scribble is 130 cm on a katana, Falling Stars 76 cm.
- Backups: `ServerStorage.Legacy.*_beforeEtchPatterns` (EtchPatterns, EtchCanvas, Etches, EtchingSpec).

**Checks (Edit):**

- `EtchingSpec` 36/36 (4.3 s). It now runs the canvas checks for every stroked pattern on every blade:
  - blank at 0, coverage only grows, progressive equals finished (buffer and uploaded image), lifts draw nothing;
  - new: nothing on the bare edge and spine strips or in the narrowing tip, and Fracture keeps off the strip seams.

  The show runs are now 14, across all seven patterns, three blades and three metals, and leave nothing behind.
- Fresh clones of the changed modules load. Every pattern in `Etches.list` has a drawing (band or strokes).
- All seven sword cards built by `ItemPicker.artModel` carry their etch (picture above).
- Build times per katana image after the blank: 25–90 ms of strokes (Woven Wind the most).

**Not verified (needs Play):**

- The five at the real table: picker, show, held, displayed and hotbar art, and the toast.
- How the pattern picker's ~0.4 s build feels on a real client, and the EditableImage budget with six card images (about 1.5 MB each on a katana) on a lower-memory device.
- Whether the strip seam is visible at game distances.
- How the sparser patterns (Falling Stars, Stormroot's twigs) read in a 96 × 66 hotbar slot.

## Pattern concepts and first tracing path

![[References/Etching Table/etch-pattern-concepts-v1.png]]

Concept image generated with the built-in image-generation tool on 2026-10-21. It illustrates graphic direction; it is not a UV-ready texture, an exact game render, or proof that the patterns have been implemented.

| Candidate | Graphic identity | Suggested stroke order |
|---|---|---|
| Tide | Sweeping wave crests with trailing currents | Main edge-side ribbon, then each crest/trail. A simplified continuous band can use the existing renderer. |
| Stormroot | Angular branching lightning/root line | Main trunk, then branches with pen-up travel between them. |
| Eclipse | Offset incomplete rings linked along the ridge | Connector, separate ring arcs, then sparse accents. First proof pattern. |
| Woven Wind | Long crossing ribbons with dark over/under gaps | First ribbon, then second; preserve the intended crossing masks. |
| Fracture | Broad angular regions separated by dark faults | Reveal each filled region with a guide while preserving the fault gaps. |
| Falling Stars | Sparse starbursts with long tapered trails | Trails, then starburst strokes; lift between separated motifs. |

All five were built on 2026-10-22 in these stroke orders; see **Five more patterns (2026-10-22)** above.

## Implementation sequence and evidence

- [x] Inspect the actual Studio sources, current cache and etch remote flow. Record any differences from this handoff before relying on the documented names. (2026-10-21: names matched; differences under **Built**.)
- [x] Prove a static Eclipse texture on the real katana overlay; verify both faces, edge strips, tint and held/viewport appearance. Keep Flame working. (Edit renders; held and viewport appearance still to see in a playtest.)
- [x] Give Eclipse a stroke definition and a private progressive canvas. Verify its completed pixels/appearance match its static final definition. (Byte-identical on all three blades.)
- [x] Connect that progress to a tool tip sampled on the actual blade surface. Verify curves, ridge/bevel contact and pen-up moves; then add restrained sound/sparks. (Sparks and glow; no sound asset.)
- [ ] Integrate server-accepted playback into the existing picker flow, with camera/control restoration and interruption cleanup. (Built and compiled; playtest pending.)
- [x] Check all current blueprints and contrasting materials: at least Iron, Copper and Blue Steel. Inspect tantō, wakizashi and katana at their real sizes, not only enlarged art cards. (Edit renders at real size.)
- [ ] With two swords sharing a cached final pattern, animate/re-etch one and prove the other remains unchanged. Also verify two players can use their own stations without cross-talk. (First half passes in EtchingSpec; two players pending.)
- [ ] Repeat open/start/close at least 10 times, including early close, death/respawn and rejected/stale requests. Track mesh/image and connection counts returning to their warm-cache baseline; no missing inventory or duplicate bonuses. (12 module-level runs pass; live death/respawn/stale pending.)
- [ ] Test unlocked/locked and wrong-owner stations; request spam; workshop movement after an upgrade; multiplayer observers seeing the final state; and 20+ visible swords including viewport previews. Measure allocations and frame time, especially on a lower-memory client.
- [ ] Exercise an image-allocation/load failure: keep inventory valid, restore controls, and show a valid supported finish or explicit retry outcome. A blank successful-looking sword is not a pass. (Preparing fails cleanly before any request; a held sword whose image fails would show no etch: open.)
- [x] Update the build evidence in Code Map/Roadmap and the relevant session note. Separate actual Studio/device checks from unrun cases. No publishing is part of this handoff.

Useful small automated checks: path-to-surface mapping at base/middle/tip; clamped monotonic progress; exact final-mask agreement; pen-up travel drawing nothing; cache-key separation; session cleanup and stale-response handling. Use the existing project test/probe setup where available.

## API references

Verify current signatures and runtime constraints before implementation:

- [EditableMesh](https://create.roblox.com/docs/reference/engine/classes/EditableMesh): UV coordinates, face UVs and geometry.
- [EditableImage](https://create.roblox.com/docs/reference/engine/classes/EditableImage): line drawing, region copying and pixel buffers.
- [MeshPart](https://create.roblox.com/docs/reference/engine/classes/MeshPart): texture content on the rendered mesh.

Related: [[Art/Flame Etch]] · [[Development/Code Map]] · [[Development/Roadmap]] · [[Design/Game Design Document]]

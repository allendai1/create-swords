---
title: Vault cleanup — 2026-10-22
type: history
status: completed — documentation and file organization only
updated: 2026-10-22
tags: [vault, cleanup, history, create-swords]
---

# Vault cleanup — 2026-10-22

Allen requested organizing the vault, deleting old files and updating roadmaps for completed work. This pass reconciled saved records through 2026-10-22. It made no Studio changes and ran no game playtests; Edit-only and unrun runtime checks remain pending.

## Active notes

- [[Home]] is the entry point; [[Current Status]] summarizes recorded implementation and verification limits.
- [[Development/Roadmap]] now contains remaining implementation and validation work, without completed implementation checkboxes or superseded layout/import tasks.
- [[Development/Code Map]] describes current recorded ownership, services, controllers, builders and tests instead of mixing the current architecture with a long append-only timeline.
- [[Design/Core Loop Review]] and [[Design/Tycoon Upgrades]] consolidate the current opening, optional finishing and purchase chains.
- [[Design/Game Design Document]] and [[Design/Workshop Growth]] now reflect 100% player forging, separate polish value, collect-before-reroll, bought ore slots, six owned plots, implemented purchases, roof fading and baked finished meshes. Older employee quality/recovery targets are explicitly unresolved against the newer manual-crafting rule; no new employee balance was chosen.
- [[Random thoughts]] is the single active idea inbox. [[Archive/Design/Completed quick thoughts — 2026-10-22]] retains the completed batch's original wording.
- [[Art/UI Design]] distinguishes the implemented backpack/chosen hotbar from its earlier iterations. [[Design/Decisions Log]] keeps dated decisions separate from current open questions.

## Preserved history

Seven older art/layout notes moved to `Archive/Art/`: Blade Shaping Study, Blender Station Review, Building Redesign, Japanese Street, Japanese Village Concept Art, Player Plot Review and Smithy Redesign. Their text/reference material remains, with historical notices and updated incoming links.

Historical snapshots preserve the pre-cleanup rules and detailed implementation records:

- [[Archive/Project History/Code Map before cleanup — 2026-10-22]]
- [[Archive/Project History/Roadmap before cleanup — 2026-10-22]]
- [[Archive/Design/Core Loop Review before cleanup — 2026-10-22]]
- [[Archive/Design/Tycoon Upgrades before cleanup — 2026-10-22]]
- [[Archive/Design/GDD before cleanup — 2026-10-22]]

Existing links to dated Code Map sections now target the retained snapshot. General Code Map links open the concise current architecture. Session chronology remains history; link destinations were updated when notes moved.

## Deleted disposable files

**13 files removed:**

- Four byte-identical image copies: the v3/v4 flame previews formerly duplicated under `Models/Hilts/review/`, and Takayama/Kawagoe photos copied into the town redesign pack. Canonical images remain in `Prototypes/etch/` and `References/Japanese Village/`; image embeds now use those originals.
- Seven Blender `.blend1` autosave backups, each with its corresponding nonempty `.blend` source retained: Buildings, KatanaHilt, Stations, MineCave, MineEntrance, MineShaft and OreStandV2.
- Two generated Python `.pyc` files and their empty cache directories. `.gitignore` now excludes Python bytecode caches as well as Blender backups.

Unique model sources, exports, screenshots, concept variants, reference videos, generation prompts and runnable prototypes were retained. Older map builders remain useful source history and were not deleted.

## Reference repairs and verification

The initial audit found **12 unresolved wiki references**, all in the older Japanese Village Concept Art note. The spacious-plot image and prompt now link to their actual `References/Concept Art/` locations. Ten missing original files are explicitly labeled as unavailable, using literal paths rather than broken embeds/links; unrelated art was not substituted. Two older relative Markdown links in the browser prototype README were also redirected to the current GDD and research note.

Final verification covers wiki/embedded-file resolution, heading targets, relative Markdown paths, duplicate image consolidation, retained Blender sources, generated-file removal and `git diff --check`. Completion of these vault checks does not establish gameplay correctness. See [[Development/Roadmap]] for the remaining runtime work.

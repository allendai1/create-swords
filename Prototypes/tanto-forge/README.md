# Sword forging study

Browser prototype of the approved forging flow for the starter blades (tantō, wakizashi, katana) (see [Create Swords! GDD](../../Create%20Swords!%20GDD.md) §5 and [Blade Implementation Research](../../Blade%20Implementation%20Research.md)). It is for judging feel before the Roblox port. It does not prove Roblox performance or EditableMesh access in a published game.

## Run it

```bash
python3 -m http.server 8765 --directory Prototypes/tanto-forge/dist
```

Then open <http://localhost:8765> for the forge study (pick a blueprint at the bottom, or open `#katana` / `#wakizashi`) and <http://localhost:8765/editor.html> for the profile editor. Opening `index.html` straight from disk will not work, because the page fetches its data files. No install or build step: `dist/` is the site. Three.js r160 is vendored in `dist/vendor/` (MIT, licence included).

Tests (plain Node, any version from 14):

```bash
node Prototypes/tanto-forge/tests/blade-core.test.js
```

## What's where

| Path | Role | Ports to Roblox? |
|---|---|---|
| `dist/data/blank.json` | The universal starting blank (shared by every blueprint) | Yes, as data |
| `dist/data/tanto.json`, `wakizashi.json`, `katana.json` | Stage shapes, 90% edge allowance, 12-strike recipe, tang, catalogue spec | Yes, as data |
| `dist/data/profiles.json` | Which blueprints the pages and tests load, in order | Yes |
| `dist/js/blade-core.js` | Shape sampling, strike/grind state, quality, mesh positions, save/load, profile checks, file format | Yes, rewrite in Luau |
| `dist/js/main.js` | Three.js scene, hammer, input, sparks, sound, HUD | No, exploratory |
| `dist/js/blade-map.js` | Top-down blade diagram with the grinding heatmap | The idea ports; the drawing code doesn't |
| `dist/editor.html`, `dist/js/editor.js` | Profile editor: drag outline points, catalogue measurements, reference image, 3D preview, checks, comparison, JSON export | No, authoring tool |
| `tests/blade-core.test.js` | The core suite run for every blueprint (68 checks, including each blade measuring to its catalogue nagasa and sori), plus file-format round-trips | Port alongside the core |

## How the blade works

- Each shape (blank → lengthened → preform → forged 90% → refined 100%) is sampled at 64 stations along the blade. Every state uses the same 782-vertex mesh, so vertex correspondence never changes.
- Length is stored per segment, so a strike that lengthens one section pushes everything downstream. Curvature is per-segment bend.
- Each strike adds a local, cosine-falloff share of its stage. Shares are normalised so every station reaches exactly 100% of a stage on that stage's last strike (no catch-up snap).
- The 90% blade is the refined blade plus a 0.14 cm edge allowance and a duller edge. Grinding moves sections from 90% toward 100% only, clamps there, and can't overcut.
- After forging, a diagram shows the blade from above with the edge bevel shaded from dull (unground) to bright (ground), ember brackets under every stretch still to grind, and a marker where the stone is. `unfinishedRuns()` in the core finds those stretches.
- The saved state is just `strikeIndex` plus per-station `refinement`. Strike progress is replayed from the recipe, which is how a server would validate it.

## Not approved (exploratory)

All three blade profiles; 12 strikes and their order/positions/turns/flips; swing, impact and move timings; exact tantō proportions, blank size, tang and heat glow; 7.5% per strike; grinding speed (about four passes).

`.openai/hosting.json` is left from the earlier session's private Site registration and is unused here.

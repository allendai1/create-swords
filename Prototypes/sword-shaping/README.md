# Sword-shaping prototype (experiment)

Question under test: does choosing where to hammer, turning the blade and correcting its shape feel satisfying enough that players would want to personally craft their rare materials? **An experiment, not an approved replacement for the current crafting.** It uses a test katana blank, takes no items, sends nothing to the server and leaves forging, inventory, purchases, saving and sword value untouched. Built and played 2026-10-23 ([Session note](../../Sessions/2026-10-23.md#sword-shaping-prototype-experiment)).

## Launch and turn off

1. Press **Play** in Studio.
2. Bottom right: **Dev** → **Shaping prototype**. You're taken to a forge corner of your own (far above the village, on this client only). Your character is held still, and every other screen is switched off.
3. **Exit** (bottom right of the prototype) puts back the camera, character movement and all screens.

To remove it entirely, delete `ReplicatedStorage.Prototypes` and the "Shaping prototype" block in `StarterPlayerScripts.DevPanel` (and `ServerStorage.Tests.ShapingRulesSpec`). Nothing else refers to them.

## The Test Anvil (Studio only, 2026-10-25)

To try the new process start to finish: heat an ingot, press E at the **Test Anvil** in the workshop (plot −8, 12), pick the ingot and any sword you know, shape it, and press **Finish**. The match becomes the blade's quality (92% → a 92% blade), and you carry on at the Hilt Bench as usual. Since 2026-10-26 the blade keeps the shape you hammered through hilting, display and sale (`shape` on the blade, `BladeCore.withShape`; [session note](../../Sessions/2026-10-26.md#test-anvil-blades-keep-their-shape)). The anvil and its remote exist only in Studio. Every sword works: the rules scale to each blade's width, and double-edged blades are shaped on both edges. Script: `roblox/TestAnvil.luau` (`StarterPlayerScripts.TestAnvil`); server side `SmithService.FinishShaped`.

## Controls

| | Mouse / keyboard | Touch (built, **not tested**) |
|---|---|---|
| Choose where | Move the mouse along the blade, or along the diagram | Drag on the blade or the diagram |
| Strike | Click; **hold** to keep striking, about 3 a second, wherever you aim (2026-10-25) | **Strike** button (shown on touch devices); hold it to keep striking |
| Turn the blade | **R** or **Turn blade** | **Turn blade** |
| Sand (any time) | **Sand** swaps the hammer for a sanding block; hold the mouse on the blade and drag to sand the bumps down to the line; **Hammer** swaps back (Refinements 5, 2026-10-25; a one-click Smooth in Refinement 4; any time, not from 90%, since later on 2026-10-25) | hold a finger on the blade and drag |
| Score it | **Finish** (card: Keep shaping / New blank) | same |
| Start over | **Reset blank** | same |
| Developer | **Dev: narrow-tip preset** (Studio only): a good blade with one section near the point hammered too narrow | same |

Edge up, a strike **narrows** the section under the hammer; flat, it **widens** it. The chip at the top left always says which.

**The view (Refinements 5, 2026-10-25):** the blade and anvil fill the screen, with a thin bar on top (side, shape match, legend). The face-on diagram is gone. A true-shape silhouette sits in a panel across the top of the screen (the blade face-on as it lies, its curve, point and widths all at one scale; yours filled, the target a white outline; about 27 px per cm on a 1920-wide screen). Widths were stretched 2.5× until later on 2026-10-25, when Allen found the guide "not representative of the blade itself", and the blade is centred below it. Lines drawn on the blade itself were tried and couldn't show millimetres at this camera (~13 px a cm), and the steel reads red where it's too wide and blue where it's too narrow. Allen: "the actual sword and anvil need to be the main view"; he picked the guide lines "Overlay on the blade".

## Rules (`ShapingRules`)

- The blade's length, curvature and back (spine) line are the finished katana's and never change. Only the edge moves: width per station (64), in cm.
- A strike changes width by `strength` (0.4 cm) at the aimed point, easing to zero `radius` (11% of the blade, about 7.7 cm) either side (0.15 cm and 7% until later on 2026-10-25, Allen: "it takes too many manual hits"; a careful katana went from ~65 strikes to ~13 for 99%). Nothing else moves. The tang end and the point are fixed, blended in smoothly.
- Strikes never look at the target: you can overwork a section past the line either way. Limits 0.8–4.4 cm keep the mesh valid.
- **Shape match** is worked out from the final geometry alone: each station within `perfect` (0.16 cm) of the target counts fully; further off, it falls away over `tolerance` (0.5 cm) (0.08 and 0.25 until later on 2026-10-25: Allen wanted it "a bit more generous" and picked 2×). Too wide and too narrow both count as error. Strike counts, turns and corrections cost nothing. The score is separate from the game's quality and sale values.
- **Sand** (Allen, Refinements 5, 2026-10-25: "the smoothing should be another manual step. It should involve holding mouse down and basically 'sand down' the bumps"): the Sand button is always there (from a 90% match until later on 2026-10-25, Allen: "players should be able to smooth whenever", and it "should smooth out the surrounding bumps ... never past that line"). Held at a spot, the block takes `sandRate` (0.5 cm/s) off under its centre, plus `smoothRate` (8/s) × how far a station stands over its neighbours' average, so a sharp bump rounds off first. It eases to nothing `sandRadius` (4% of the blade) either side and never cuts past the target line (`Rules.sand`). It never adds material, so a section hammered too narrow still costs; sanding a wide-but-close blade all along scores 100%. It replaces Refinement 4's one-click Smooth ([session note](../../Sessions/2026-10-24.md#refinement-4)). [Session note](../../Sessions/2026-10-25.md#refinements-5).
- All tuning (strength, radius, limits, blank width, score band, sanding threshold, rate and reach, animation timing) is in `ShapingRules.CONFIG`.

## Files

| File | Studio location | Role |
|---|---|---|
| `roblox/ShapingRules.luau` | `ReplicatedStorage.Prototypes.ShapingRules` | Pure rules and tuning (above). |
| `roblox/ShapingPrototype.luau` | `ReplicatedStorage.Prototypes.ShapingPrototype` | Client presentation: forge corner, `BladeView` mesh, the target outline on the blade, hammer, sanding block, tongs, top bar, input, camera, Exit. `workspace.ShapingPrototype.Inspect:Invoke()` reads the live state for checks. |
| `roblox/ShapingRulesSpec.luau` | `ServerStorage.Tests.ShapingRulesSpec` | 28 checks (5 for sanding, 4 for other blades; 2026-10-25). Command bar: `print(require(game.ServerStorage.Tests.ShapingRulesSpec:Clone())())` |
| (edit) | `StarterPlayerScripts.DevPanel` | The "Shaping prototype" button. |
| `screenshots/` | | Play captures, numbered in order of the correction sequence. |

Reused unchanged: `Shared/BladeView` (mesh), `Shared/BladeCore` (geometry, params), `Shared/Blueprints` (katana target), BladeProbe's tween pattern, the anvil's Clang sound.

## Play results (2026-10-23)

All play went through the normal controls (mouse clicks, R, buttons), driven through Studio's input tools; nothing was set from code. The durations include the agent's pauses between input batches, so a person would be faster.

| Attempt | Start | Result | Strikes | Turns | Corrections | Time |
|---|---|---|---|---|---|---|
| 1 | Blank, then the full correction sequence near the point | 95.2% (before the score band) | 64 | 2 | 2 | 2:45 |
| 2 | Blank, planned from what attempt 1 showed (more passes toward the point) | 99.997% (shows 100%) | 62 | 0 | 0 | 2:01 |
| 3 | Developer preset | 99.99% (shows 100%) | 5 | 2 | 1 | 0:24 |

Attempt 2 needed fewer corrections than attempt 1: the taper was clear after one try, so the passes could be planned. The last two strikes of attempt 2 were picked with a search over the live shape, not by eye. A simulated careful player reaches 100% in about 69 strikes.

Checked in Play (numbers from `Inspect`):

- A strike visibly changes only the selected region: a smooth dip in the diagram, the flash on the blade, sparks, the clang.
- **Turning alone changed no width** (max difference 0.000000) and kept the aim on the same section.
- Edge up narrows and flat widens. Both overshoot: −0.34 cm overworked, then +0.13 cm widened past the line.
- Corrections near the point left everything more than one radius away **exactly** as it was, three times.
- Moving toward the target raised the score and moving away lowered it (spec, and live: 88.8 → 90.1 → 93.4 → 95.2 through the sequence).
- 400 passes of each direction keep the mesh valid (spec).
- **Reset** restores the exact blank.
- **Exit** restored all 16 screens, the Custom camera on the Humanoid, FOV 70, walk 16 and jump 50. The ordinary anvil then opened its forge picker as usual (closed without forging).
- The hammer face lands within 0.04 studs (about 0.7 cm on a 70 cm blade) of the aimed point.

## Known limits

- **Touch not tested**: Studio's input tools only send mouse and keyboard. Gamepad isn't built.
- In 3D the width change is small on a true-proportioned katana (3 cm across 70 cm). Edge up you see the edge, not the width. The magnified diagram does most of the reading; flat, the blade face does show waists and bulges.
- The fade into the locked point (0.90–0.97) is the fiddliest place: strikes there land weaker and spill onto 0.90. It counts for less in the score but is where the last points are lost.
- One strike strength. A lighter tap (e.g. Shift-click at about ⅓ strength) wasn't needed once the score band was added, but would make finishing gentler.
- The hammer lands where you aimed, but it hovers to the side at rest. The bed is a long flat anvil, so the blade never slides.
- The game's HudFocus left some HUD pieces showing over the real anvil too, which predates this work. The prototype switches every screen off itself.

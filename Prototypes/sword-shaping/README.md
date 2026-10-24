# Sword-shaping prototype (experiment)

Question under test: does choosing where to hammer, turning the blade and correcting its shape feel satisfying enough that players would want to personally craft their rare materials? **An experiment, not an approved replacement for the current crafting.** It uses a test katana blank, takes no items, sends nothing to the server and leaves forging, inventory, purchases, saving and sword value untouched. Built and played 2026-10-23 ([Session note](../../Sessions/2026-10-23.md#sword-shaping-prototype-experiment)).

## Launch and turn off

1. Press **Play** in Studio.
2. Bottom right: **Dev** → **Shaping prototype**. You're taken to a forge corner of your own (far above the village, on this client only). Your character is held still, and every other screen is switched off.
3. **Exit** (bottom right of the prototype) puts back the camera, character movement and all screens.

To remove it entirely, delete `ReplicatedStorage.Prototypes` and the "Shaping prototype" block in `StarterPlayerScripts.DevPanel` (and `ServerStorage.Tests.ShapingRulesSpec`). Nothing else refers to them.

## Controls

| | Mouse / keyboard | Touch (built, **not tested**) |
|---|---|---|
| Choose where | Move the mouse along the blade, or along the diagram | Drag on the blade or the diagram |
| Strike | Click | **Strike** button (shown on touch devices) |
| Turn the blade | **R** or **Turn blade** | **Turn blade** |
| Score it | **Finish** (card: Keep shaping / New blank) | same |
| Start over | **Reset blank** | same |
| Developer | **Dev: narrow-tip preset** (Studio only): a good blade with one section near the point hammered too narrow | same |

Edge up, a strike **narrows** the section under the hammer; flat, it **widens** it. The chip at top left of the panel always says which.

## Rules (`ShapingRules`)

- The blade's length, curvature and back (spine) line are the finished katana's and never change. Only the edge moves: width per station (64), in cm.
- A strike changes width by `strength` (0.15 cm) at the aimed point, easing to zero `radius` (7% of the blade, about 4.9 cm) either side. Nothing else moves. The tang end and the point are fixed, blended in smoothly.
- Strikes never look at the target: you can overwork a section past the line either way. Limits 0.8–4.4 cm keep the mesh valid.
- **Shape match** is worked out from the final geometry alone: each station within `perfect` (0.08 cm) of the target counts fully; further off, it falls away over `tolerance` (0.25 cm). Too wide and too narrow both count as error. Strike counts, turns and corrections cost nothing. The score is separate from the game's quality and sale values.
- All tuning (strength, radius, limits, blank width, score band, animation timing) is in `ShapingRules.CONFIG`.

## Files

| File | Studio location | Role |
|---|---|---|
| `roblox/ShapingRules.luau` | `ReplicatedStorage.Prototypes.ShapingRules` | Pure rules and tuning (above). |
| `roblox/ShapingPrototype.luau` | `ReplicatedStorage.Prototypes.ShapingPrototype` | Client presentation: forge corner, `BladeView` mesh, hammer, tongs, face-on diagram, input, camera, Exit. `workspace.ShapingPrototype.Inspect:Invoke()` reads the live state for checks. |
| `roblox/ShapingRulesSpec.luau` | `ServerStorage.Tests.ShapingRulesSpec` | 19 checks. Command bar: `print(require(game.ServerStorage.Tests.ShapingRulesSpec:Clone())())` |
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

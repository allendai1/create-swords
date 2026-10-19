# Blade core for Roblox

Luau port of `../dist/js/blade-core.js`, plus a Studio probe that forges and grinds a blade on an EditableMesh. Tested in the game's Studio place on 2026-10-19.

| File | Studio location | Role |
|---|---|---|
| `BladeCore.luau` | `ReplicatedStorage.Shared.BladeCore` | Shape sampling, strikes, grinding, quality, mesh layout, save/load validation, catalogue measurement, profile checks. Pure Luau, `--!strict`. |
| `BladeData.luau` | `ReplicatedStorage.Shared.BladeData` | **Generated** from `dist/data/*.json`. Do not edit by hand. |
| `BladeProbe.luau` | `ReplicatedStorage.Shared.BladeProbe` | Test-only client probe: hammer, poses, deformation, mesh grinding, timings. |
| `BladeProbeLoader.client.luau` | `StarterPlayer.StarterPlayerScripts.BladeProbeLoader` | Starts the probe only when `workspace` has the attribute `BladeProbe` (`true`, or `"tanto"`, `"wakizashi"`, `"katana"`). |
| `BladeCoreSpec.luau` | `ServerStorage.Tests.BladeCoreSpec` | 31 tests, including number-for-number checks against the JavaScript core. |
| `BladeGolden.luau` | `ServerStorage.Tests.BladeGolden` | **Generated**: values the JavaScript core computes. |
| `run-tests.luau` | (not in Studio) | Runs the spec in the stand-alone Luau CLI. |

## After changing blade data

```bash
node Prototypes/tanto-forge/tools/export-luau.js
```

That rewrites `BladeData.luau` and `BladeGolden.luau`. Copy both into Studio (same locations), then run the tests.

## Running the tests

In Studio's command bar:

```lua
local r = require(game.ServerStorage.Tests.BladeCoreSpec)(require(game.ReplicatedStorage.Shared.BladeCore), require(game.ReplicatedStorage.Shared.BladeData), require(game.ServerStorage.Tests.BladeGolden)) print(r.passed, "passed", r.failed, "failed")
```

Outside Studio, with the [Luau CLI](https://github.com/luau-lang/luau/releases) (0.740 used):

```bash
luau Prototypes/tanto-forge/roblox/run-tests.luau
```

## Trying the probe

In the command bar, then press Play:

```lua
workspace:SetAttribute("BladeProbe", "katana")
```

Space or click strikes; after 12 strikes, hold and drag along the edge to grind; R restarts. Clear the attribute (`workspace:SetAttribute("BladeProbe", nil)`) to switch it off. It doesn't touch the real AnvilController and sends nothing to the server.

## Things learned in Studio

- `EditableMesh:RaycastLocal(origin, direction)` returns **face id first**, then position, barycentric weights and the three vertex ids. The direction's length is the ray's length.
- A MeshPart's bounds are fixed when it's created, so add a zero-area triangle spanning the furthest the blade can reach (the existing `Shared/BladeMesh` does the same). Collision uses those bounds, so raycast the mesh, not the part.
- Automatic normals stay correct after `SetPosition`, as long as crease vertices are duplicated (they are in this layout).
- The default camera scripts take the camera back when the character spawns; hold `Scriptable` each frame while forging.

---
title: Sword Mesh Pipeline
type: plan
status: built 2026-10-21; 27 shapes baked; waiting on Allen's budget playtest
tags: [swords, meshes, performance, pipeline]
---

# Sword Mesh Pipeline

Allen, 2026-10-21, after the EditableMesh budget ran out in a playtest: "yes that'd be ideal and make there's an established way so that we can add more swords later".

**Goal:** finished swords stop using the client's EditableMesh budget, and adding a sword later is a short, repeatable routine.

## Why

Each player's device has a small memory budget for EditableMeshes, the meshes our scripts build at runtime. A Studio test (2026-10-20) stopped at about a dozen. When it's full, new swords, etches and the Polishing Station blade silently fail to draw.

Today every *different-looking* finished sword on screen costs live meshes:

| Kind | How many can exist | Built by |
|---|---|---|
| Blade | 3 blueprints × 3 polish levels = 9 | `SwordMeshCache.blade` → `BladeView` |
| Flame skin | 9 | `SwordMeshCache.etch` → `BladeEtch.build` |
| Etch overlay (Eclipse and future stroked patterns) | 9 | `SwordMeshCache.overlay` → `BladeEtch.buildTextured` |
| Live station blade | 1 at a time | `AnvilController`, `PolishController` (`BladeView`) |

The worst case is about 28, well over the budget. A varied collection can break drawing even without leaks.

The fix: finished swords only come in a fixed set of shapes (blueprint × polish level). Bake those shapes once into normal mesh assets, which don't count against the budget. Keep EditableMeshes only where the shape changes live: the anvil while forging and the Polishing Station while grinding, one at a time.

## Design (as built, 2026-10-21)

Allen: "Go ahead and build the bake tool, bake the swords and switch SwordMeshCache to baked-first."

### Baked meshes in the place

- `ReplicatedStorage.SwordMeshes` holds one MeshPart per baked shape, named by its cache key. There are 27:
  - `B|<bp>|<level>`: blades;
  - `O|<bp>|<level>`: etch overlays, UV-mapped, shared by Eclipse and future stroked patterns;
  - `E|<bp>|<level>|Flame|060c14`: Flame skins (060c14 is Flame's body colour, the same for every material).

  The blueprints are tanto, wakizashi and katana, at levels 0, 1 and 2 (polish 0, 0.5 and 1).
- **Attributes:**
  - `Version`: the blueprint's version when baked.
  - `Hash`: an FNV-1a hash of the packed live mesh it was baked from.
  - `PartName`: the live part's name (`Blade` or `Etch`).
  - `AssetId`: the uploaded Model asset.
- **Properties:** copied from the live part (Color, Material, collision and query flags, Massless, CastShadow and so on). `RenderFidelity` is Precise, so distance LODs don't simplify the blade.
- **No `Offset` attribute after all.** The helper adds one degenerate triangle that mirrors the mesh's bounds, so every bake is centred on the live mesh's origin. A baked part placed at the live part's CFrame then lines up exactly. Etches stay welded at the blade's CFrame with no caller changes. Side effect: the overlay's and Flame skin's `Size` is symmetric (about twice as long as before); nothing reads it.

### Runtime: `SwordMeshCache` looks there first

- **Lookup:** `blade()`, `overlay()` and `etch()` for Flame call `useBake(key, blade, params)` before building.
  - If `SwordMeshes` has the key with the blueprint's current `Version`, a clone of it becomes the key's template: no EditableMesh, no budget.
  - Otherwise the old live build runs, with one warning per key (only when the folder exists). A new blueprint works at once on live meshes; it just costs budget until it's baked.
- **Unchanged:**
  - The API, so `SwordRenderer`, `ItemPicker`, `Hotbar`, `EtchPlayback`, `PolishController` and `HiltBenchController` are untouched.
  - Refcounting: baked templates are released like live ones.
- **Stroked patterns:** Eclipse's texture is still an EditableImage per blueprint, level and material colour. It's drawn on the baked overlay, so an Eclipse sword now costs no mesh, only its image.
- `SwordMeshCache.useBaked` (default true): the bake tool and `SwordMeshSpec` turn it off to build the live meshes.
- **Runtime check:** only `Version`, which is cheap. `Hash`, checked by `SwordMeshSpec`, catches code changes that alter the geometry without a version bump.
- Backup: `ServerStorage.Legacy.SwordMeshCache_beforeBaked`.

### The bake tool: `ServerStorage.Builders.bake_sword_meshes`

- `run(filter?)` goes through `shapes()`: every blueprint in `Blueprints.order` × levels 0, 1 and 2 × blade, overlay and Flame skin. For each one it:
  1. builds the shape live through the cache, using the game's own code;
  2. packs it per face corner (`pack`) and hashes it (`hash`);
  3. skips it if `SwordMeshes` already has the key with the same `Hash` and `Version`;
  4. otherwise posts it to the helper and waits for the asset;
  5. loads it with `InsertService:LoadAsset`, copies the live part's properties, and replaces the old part.

  It returns one report line per key: `baked <assetId>`, `up to date` or `FAILED …`.
- **Helper:** `Development/sword_mesh_bake.py` (vault). It listens on 127.0.0.1:34999.
  - `POST /bake/<key>`: dump → glb → Open Cloud upload. The glb has positions, colours, UVs and normals, is turned 180° about Y to cancel the importer's turn, and gets the bounds-mirroring triangle.
  - `GET /op/<id>`: polls the operation.

  It reads `ROBLOX_API_KEY` from the environment and never prints it. It replaces the spike's `sword_mesh_recv.py` and `sword_mesh_glb.py`.
- **Fresh copy (2026-10-21):** `run` works on a fresh copy of Shared, removed afterwards. Edit-mode `require` keeps serving a module's old code after it's edited, so a bake through the real modules missed the polish sheen change. The first re-bake after the sheen replaced exactly the 6 Flame skins at levels 1 and 2.
- **Timing:** a full bake of 27 took about 9 minutes, almost all of it waiting on uploads and moderation. Each was approved.

### Adding a sword later

1. Add the blueprint to `Shared/Blueprints` and its id to `Blueprints.order`. It forges and renders at once on live meshes, with a "no bake" warning per shape.
2. In a terminal: `python -I Development/sword_mesh_bake.py` (leave it running).
3. In Studio, Edit: `print(require(game.ServerStorage.Builders.bake_sword_meshes:Clone()).run())`. It bakes only what's new or changed: 9 shapes per new blueprint.
4. Check with `print(require(game.ServerStorage.Tests.SwordMeshSpec:Clone())())`; 0 failed is the bar.
5. Stop the helper and save the place.

Changing a blueprint's shape needs its `version` bumped, which makes the old bakes unused until re-baked. Changing `BladeView` or `BladeEtch` code without a version bump is caught by `SwordMeshSpec` (`Hash`). Re-run the bake, and it replaces exactly the shapes whose hash changed.

## The spike's questions

These decided the route. Points 1–4 passed (results below); point 5 is Allen's playtest.

1. **Publishing:** can `AssetService:CreateAssetAsync` publish an EditableMesh as a Mesh asset from Studio for this account?
   - If not, the fallback route: export each mesh to a file with Python and upload it through Open Cloud with the existing `ROBLOX_API_KEY`, as the flame guard was.
2. **Vertex colours:** do they survive publishing? The blade's polish finish and Flame's band live in vertex colours.
   - If not, the finish moves into a small per-shape texture.
3. **Tint:** does the part's `Color` still multiply the vertex colours on the baked part, as it does now? That's how one shape serves every material.
4. **Fit:** do bounds, pivot and orientation round-trip exactly (`Offset`)? Do UVs survive on the overlay?
5. **Budget:** in Play, put 20+ different swords on screen and confirm no budget errors and steady frame time.

## Spike results (2026-10-21)

Tested on the katana at full polish: its blade (785 vertices, 769 faces, two vertex colours) and its etch overlay (4,180 faces, UV-mapped), with the Eclipse texture on top.

| Point | Result |
|---|---|
| 1. Publishing | `AssetService:CreateAssetAsync` fails: "CreateAssetAsync and CreateAssetVersionAsync are not available yet". The fallback works (route below). Each upload was approved by moderation within about 10 seconds. |
| 2. Vertex colours | Survive exactly: every face corner's colour matches (worst difference 0). |
| 3. Tint | `Color` still multiplies the vertex colours. A baked blade in copper looks the same as the live one, and a white one shows the plain finish. |
| 4. Fit | Positions, UVs and winding match exactly (worst 0) once two corrections are made. The importer merged one duplicate vertex (785 → 784). Size matches to 1e-6. |
| 5. Budget | Not tested yet. It needs Play with 20+ swords, after the bake is built. |

**The two corrections:**
- **Rotation:** Roblox's glTF import turns the mesh 180° about Y. The first upload came in mirrored: half the faces matched nothing and the colours were swapped. The exporter cancels this by negating x and z, normals included. After that, all faces match.
- **Offset:** an uploaded mesh is re-centred on its bounding box. A live EditableMesh part keeps the mesh's origin, which is how `SwordRenderer` can weld the etch at the blade's CFrame.
  - The blade's bounds triangle centres it, so its `Offset` is 0.
  - The overlay spans 0 to 3.49 studs along the blade, so it needs `Offset` (1.7452, 0, −0.1341). Placed at `bladeCf * CFrame.new(Offset)`, it lines up with the live etch. Without it, it sits 1.75 studs toward the base.

![[References/Sword Meshes/spike-live-vs-baked-rows.jpg]]

*Rows, top to bottom:*
- *live blade (copper);*
- *baked blade (copper);*
- *baked blade (white);*
- *live blade with live Eclipse overlay;*
- *baked overlay without `Offset`;*
- *baked overlay with `Offset`.*

![[References/Sword Meshes/spike-etch-live-vs-baked.jpg]]

*Live etch (top) and baked etch with `Offset` (bottom): same strokes, same places.*

### The route that works

1. **Studio, Edit (MCP or command bar):** pack the mesh per face corner:
   - position f32×3;
   - colour u8×3;
   - UV f32×2;
   - normal f32×3.

   `POST` it with `HttpService:RequestAsync` to the local helper. Plugin context can reach `127.0.0.1` in Edit.
2. **`Development/sword_mesh_recv.py`:** a 10-line local HTTP receiver that writes each upload to a file. Run it with `python -I sword_mesh_recv.py <dir>` (port 34999).
3. **`Development/sword_mesh_glb.py <dump> <out.glb>`:** writes the glb, with:
   - POSITION, COLOR_0, TEXCOORD_0 and NORMAL;
   - x and z negated.
4. **Open Cloud upload:** `POST /assets/v1/assets` (`assetType` `Model`, `model/gltf-binary`, creator 14722022, header `x-api-key` from `ROBLOX_API_KEY`), then poll the operation for `assetId`.
5. **Studio:** `InsertService:LoadAsset(assetId)` gives a Model containing a MeshPart with the new `MeshId`. Keep that MeshPart, and set `Offset` to the live mesh's bounds centre.

Going through files avoids passing mesh data through the chat. The receiver is the one piece that has to be running during a bake.

*As built:* steps 2–4 are one helper, `Development/sword_mesh_bake.py`. A centring triangle replaced `Offset` (see Design).

Spike assets left on the account:
- 108113735457116 (first, mirrored);
- 94828405630027 (blade);
- 134004016139646 (overlay).

They aren't used anywhere.

## Checks (2026-10-21)

- **`ServerStorage.Tests.SwordMeshSpec`** (new), run with `print(require(game.ServerStorage.Tests.SwordMeshSpec:Clone())())`. **110 checks, 0 failed.** For each of the 27 shapes:
  - it's baked for the blueprint's version;
  - its `Hash` matches today's live build;
  - the uploaded mesh matches the live one face by face (worst values below);
  - a fresh cache hands out the baked part: a `MeshId`, no EditableMesh, the right name.

  The worst face-by-face values:
  - position 3.3e-7 studs;
  - UV 0;
  - colour 0;
  - normal 0.0008, under 0.05°.

  Finally, the cache is empty after releases.
  - The first run flagged Flame colours (0.77). The importer had not lost anything: Flame's band edge has corners and zero-width faces in the same place with different colours, and the spec took the first match. Ties now go to the closest corner.
- **`EtchingSpec` 32/32.** Two checks changed:
  - The overlay share check accepts one `MeshId`.
  - "Tool surface on the real blade" raycasts a live-built blade. A raycast hits collision geometry, which on an uploaded mesh is an approximate hull (wakizashi 0.0195 studs off). Scripts can't change `CollisionFidelity`, and the game never raycasts blades.
- **Render:** all three blueprints, plain, Flame and Eclipse, in copper, live (left) and baked (right) from a fresh cache. They're indistinguishable.

![[References/Sword Meshes/baked-vs-live-all.jpg]]

- **Not verified:** anything in Play.
  - The budget with 20+ swords on screen.
  - Mesh streaming: a baked sword's mesh downloads the first time it's seen, so it may pop in.
  - The etch, polish and respawn loop.

## Cost and effects

- About 27 assets now (3 blueprints × 3 levels × 3 kinds), plus 9 per future blueprint. Each needs moderation, which went quickly for earlier uploads.
- No change to how swords look (checked face by face). The anvil and Polishing Station keep live meshes because their shape changes as you work.
- Removes the budget risk for finished swords instead of managing it. The leak fix (`SwordRenderer` releasing on removal) stays either way.

## Order of work

1. ~~Spike (points 1–4 above), with results recorded here.~~ Done 2026-10-21: passed.
2. ~~Bake tool and `SwordMeshes` folder; bake the 27 shapes.~~ Done 2026-10-21.
3. ~~`SwordMeshCache`: baked-first lookup with fallback.~~ Done 2026-10-21.
4. ~~`SwordMeshSpec`; renders; Edit checks.~~ Done 2026-10-21.
5. Allen playtests (point 5 and the etch/polish/respawn loop).
6. ~~Vault: Code Map, Roadmap, this note's status, and the "Adding a sword" routine linked from [[Development/Code Map]].~~ Done 2026-10-21.

Related: [[Art/Animated Blade Etching]] · [[Development/Code Map]] · [[Development/Roadmap]]

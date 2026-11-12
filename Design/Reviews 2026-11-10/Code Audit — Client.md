---
title: Code Audit — Client
type: review
updated: 2026-11-10
tags: [review, code-audit, client, create-swords]
---

# Code Audit — Client (2026-11-10)

This is the client half of the re-run of [[Design/Reviews 2026-11-07/Code Audit]]. The server half is [[Design/Reviews 2026-11-10/Code Audit — Server]]. It is a read-only audit using the lihfolk:audit method, roblox-luau-patterns and roblox-performance.

- Nothing in Studio was changed and Play was not started.
- Sources were read out of the Edit place with `execute_luau` (Source only) into a scratch folder, and checked there.
- Two Studio reads of template properties settled leads: `WorldText` ResetOnSpawn, `LevelPrompt.HoldDuration`, and the plot's ModelStreamingMode.
- Two helper agents read 48 of the files in full. I opened every line cited below myself, except where it says **not confirmed**.

## Summary

- **Scope: 71 scripts.**
  - StarterPlayerScripts: 55 (DecorateController is disabled and was only skimmed).
  - ReplicatedStorage.Shared: SwordMeshCache, BladeView, BladeMesh, BladeEtch, EtchCanvas, EtchPatterns, BladeCore, DayNight, LeverHand, Hilts, AnvilScore, NewSilhouetteBlades and BladeProbe.
  - ReplicatedStorage.Prototypes: ShapingPrototype, PackingPrototype and ShapingRules. Only the Dev Panel requires these.
  - Left out: TopbarPlus, BladeData, and the server half.
- **LihFolk checker: 71 files, 0 errors, 14 warnings, 109 info.**
  - The checker skips a `.lua` file that never calls `GetService`, so its first pass saw only 65 files. I renamed the copies to `.luau` and ran it again.
  - All 14 warnings are false positives (list below).
  - I did not review the 109 `findfirstchild-chain` infos one by one. Top files: DevPanel 12, MenuController 10, EmployeeController 10, TycoonController 8, Guide 8.
- **Findings from reading the code: 13 in total.** None are applied.

| P | Count |
|---|---|
| P0 | 0 |
| P1 | 0 |
| P2 | 5 |
| P3 | 8 |

- **Overall:** the client holds up well.
  - Every client `InvokeServer`, `GetProductInfoAsync` and `PolicyService` call is pcalled.
  - Lucky Metal stays hidden until PolicyService answers.
  - The 11-07 per-frame fixes (P8) are in place.
  - The etch images are spread over frames.
- **Gaps:**
  - The anvil's live blade mesh is still unguarded (old #5).
  - A failed live mesh build leaks its EditableMesh.
  - The gamepad offer keys take Y from the stations.
  - Two phone hitches: the Hotbar's art, and the lever hand's per-frame posing.

## Old findings

| # (11-07) | Status | Evidence |
|---|---|---|
| 5 (AnvilController EditableMesh unguarded) | **Still open, lines moved** | `startBlade` 733 calls `BladeView.new` at 743 with no pcall. `onPick` calls `enterView()` at 972 and then `startBlade(bp)` at 974, after `BeginForge` succeeded at 957. PolishController 471 and SwordMeshCache 221 do pcall theirs. |
| 1–4, 6, 7 | Server side | Covered in the Server note. |
| Perf P8 (client idle work) | Fixed | PolishController 154–158: the Heartbeat returns while idle. PolishController 1246–1256: the RenderStepped returns while idle. TycoonController 645–650: the pad check runs at 10 Hz. |
| Perf P2 (64 shine beams) | Unchanged | `SwordRenderer` 96 `SHINE_PIECES = 64`, and the frame loop at 180–242. The Performance Audit owns it. |
| Perf P6 (join-time scans) | Unchanged | `workspace:GetDescendants()` at WorldStoreController 198, OreBoxAnimator 127, NewOreFx 66, PromptFilter 52/86, PromptStyle 38 and ActionButton 33. |

## Ranked findings (proposed, not applied)

| # | P | Area | File:line | What breaks for a player, and when | Proposed fix | Effort |
|---|---|---|---|---|---|---|
| 1 | P2 | Phones / meshes | `AnvilController` 743 (`startBlade`), called at 974 after `enterView()` at 972 | Old #5, still open. If the client's EditableMesh budget is full (a phone with swords on screen), `BladeView.new` throws inside `onPick`. By then the camera is in the anvil view and the HUD is up, but there's no blade: `mode` stays idle and `blueprint` is set to the pick while `view` stays nil. The player has to back out with Leave. BeginForge has already run on the server, but the ingot is only taken on Finish, so nothing is lost. Static, not measured. | pcall `BladeView.new` in `startBlade`. On failure, `clearBlade()` and `leave()`, then toast "Couldn't start, try again" (the existing text). | S |
| 2 | P2 | Phones / meshes | `Shared.BladeView` 49–71; `Shared.BladeEtch` 212–280 (`buildTextured`) and 315–441 (`build`) | Each one calls `CreateEditableMesh` first and `CreateMeshPartAsync` last, with nothing guarding the middle. If anything in between throws (most likely `CreateMeshPartAsync` refusing on a full client), the EditableMesh is never destroyed. The callers pcall (SwordMeshCache 221 and 299–311, PolishController 471), but they never get the mesh back to free it. So each failure eats more of the budget it failed on, and the next retry (another polish, another sword in view) is more likely to fail too. Static, not measured. | In each builder, pcall the steps after `CreateEditableMesh`. On failure, `mesh:Destroy()` and re-raise. | S |
| 3 | P2 | Gamepad | `ShopController` 177–185 (`bindPad`) | While any offer card exists, `AnswerOffer` is bound at High priority to **Y** and **L2** and always returns Sink. Effects:<br>• At the Etching Table, Y (`EtchColors`, EtchingTableController 304, Default priority) never fires.<br>• At the Polishing Station, `PolishSave` (1092) ties at High, so the most recent bind wins, and `bindPad` re-binds on every new offer.<br>• `nearest()` (161–173) picks among all cards, including ones far away or hidden while a station HUD is up. A gamepad player can accept or decline an offer they can't see. | Return `Pass` when `HudHidden` is set, or when the nearest card isn't enabled and within its MaxDistance. | S |
| 4 | P2 | Phones / hitch | `Hotbar` 403 (`refresh`), 468–471, 276–300 (`drawArt`) | `refresh` (deferred once at 536–541) rebuilds the art of every slot whose signature changed, all in one frame. Each slot gets the blade clone (`ItemPicker.artModel`, a live build for a Test-Anvil shape), two ViewportFrames, the 8 rim copies and the shadow. Bursts like this happen on join, after a batch of swords lands, and when the bag fills. This is the same pattern ItemPicker had to fix (ItemPicker 572–605, `queueArt` / `ART_BUDGET` 4 ms). Static, not measured. | Queue `drawArt` through the same budgeted queue ItemPicker uses (one slot per ~4 ms). | M |
| 5 | P2 | Phones / per frame | `WorldStoreController` 427–449, `Shared.LeverHand` 33–60, 77–82 | Every Heartbeat, for each owned Auto-on roller within 120 studs, `LeverHand.hold` runs `pose()` twice. Each run is a breadth-first walk over about 15 parts × their RigAttachments × 15 `FindFirstChild`, with string `:sub` and new tables, then 15 CFrame writes. It runs while the lever is still, too. With 6 plots in view that's about 1–2 ms a frame on a phone. Static, not measured. | Skip when the knob's CFrame hasn't changed since the last frame. Cache each rig's (parent part, attachment, child part, attachment) pairs once. | M |
| 6 | P3 | Leak | `UiSounds` 21–37 | `hooked` is a weak-keyed table with Instance keys. When Luau drops a button's wrapper, which happens when no script holds it (HudFocus 28–31 notes the same for its tables), the key goes. HudFocus re-parents MenuGui.Buttons and HUD pieces on every window open and close, so `DescendantAdded` fires again and each button gains another Activated and MouseEnter handler. The sound only restarts, so nobody hears it; the connections grow over a session. | Mark hooked buttons with an attribute (`UiSoundsHooked`), as `UiFx.press` does. | S |
| 7 | P3 | Leak | `ShopController` 368–372 | The `SwordId` clink connection is made with `:Connect` rather than `on(...)`, so the stream-out unbind (the rule at 381–383) never cuts it. Each stream-out and stream-in of a holder adds one more. Cues' gap hides the extra clinks. | Register it with `on(...)` after `on` is defined (384). | S |
| 8 | P3 | Store | `WorldStoreController` 80–98 (`fetch`) | After 5 failed `GetProductInfoAsync` tries (about 77 s), `fetching[key]` stays true and `info[key]` stays nil. That pass's world spot then has no label, no prompt and no price for the rest of the session (`offer` needs `info`, 382). A Marketplace hiccup at join costs that session's in-world sales. | Clear `fetching[key]` after the last try, so the 0.2 s loop asks again later (or keep retrying every 60 s). | S |
| 9 | P3 | Phones / hitch | `PolishController` 522 → `buildGrime` 636–757 | The grime skin (1024 × 128–384 px, plus the sheen fill added 11-09) is built in one frame inside `begin`. The session note measured 8.8 ms for a katana on PC before the sheen fill, so a phone would take roughly 25–45 ms (estimate), once per visit. It also allocates four buffers of up to 1.5 MB. | Accept it, or spread the row loop with the EtchCanvas `SLICE` pattern while the camera eases in. | M |
| 10 | P3 | Phones / hitch | `SwordRenderer` 281–296 `etching`, `ItemPicker` 91 `etching`, `EtchingTableController` 431 (`warmEtch`), `PolishController` 289–291 (`syncEtch`) | Each module spreads its etch image builds at 4 ms a frame (`EtchCanvas` 45), but each keeps its own "one at a time" flag. Opening the etching picker while a rack of etched swords streams in can stack two or three 4 ms slices in the same frame. Static, not measured. | Move the turn-taking (`etchTurn` / `etchDone`) into SwordMeshCache, so all etch builds share one queue. | S |
| 11 | P3 | Per tick | `TycoonController` 611–640 | Every 0.2 s it walks every plot's pads (6 plots × about 89 markers). Per pad it runs a recursive `FindFirstChild("Label", true)`, and it writes `LocalTransparencyModifier` and `CanCollide` on every pad part every tick, even when nothing changed. For your own nearby pads it also calls `buildingAt(root)` again per pad, and `inSight` raycasts. Static, not measured. | Compute `buildingAt(root)` once per tick. Hide other plots' pads once, plus on DescendantAdded. Cache each pad's label. | M |
| 12 | P3 | Dev Panel reset | `AnvilController` 504 (AnvilSparks + PointLight), `PolishController` 246 (PolishSparks), `OreBoxShow` 202–213 (RollingIngot mid-roll), `ShopController` 255–260 (fallback spot parts), `TycoonController` 344–349 (BuyButton in PlayerGui), `VipIntro` 196–255 | Reset progress re-runs player scripts, and these leave their old copies behind:<br>• Each rerun adds another `AnvilSparks` / `PolishSparks` to Terrain. AnvilController 398 already cleans its outline this way.<br>• A reset during a VIP intro leaves the root **anchored** and `ProximityPromptService.Enabled = false` for the session, because the new copy never restores them.<br>• Admins only. | Destroy the previous run's copy by name at startup, as Guide 80–89 and WeatherController 31–35 do. In VipIntro, set `ProximityPromptService.Enabled = true` at startup and unanchor the root if it is anchored. | S |
| 13 | P3 | Leak | `EmployeeController` 1445–1447 | `prompt.Destroying:Once(...)` is added on every PromptShown. A long-lived worker's prompt collects one per show until the NPC goes. | Connect it once where the prompt is set up. | S |

## Leads not confirmed (worth one look in Play)

- **HUD pieces indexed at startup:** GemController 58 `.Buttons`, CollectionController 91 `.Buttons.Book`, MailController 67 `.Mail`, ShopController 114 `HudGui.Coins…`. HudFocus parks these pieces in HudHold while a HidesHud screen is up. If a script starts while one is parked (after a Dev reset), the index errors and that script dies. I couldn't show a normal join where this happens.
- **Hud 162–173:** the "coins fly in when the HUD is back" wait watches `HudGui.Enabled`, but HudFocus parks `HudGui` (it carries HudPart). Check whether coins earned while hidden fly toward an invisible pill.
- **SwordSlash 104–120:** `tool.Activated:Connect(swing)` has no hooked check. If a tagged Tool fires InstanceAdded twice, each click swings twice.
- **Loops that could spin:** `Shared.BladeEtch` 85–96 (`flame`) and `Shared.EtchPatterns` 743–752 only end on a numeric condition. A NaN width, or a zero-width piece, would never end. No path I read feeds one.
- **UpgradeFx 118–121, HeldLabel 36–58, GemController 195–207:** a 3 s join grace window, a held label that doesn't refresh on `Hot`, and taps dropped while `busy`. These are small UX edges.

## Hard gates (system rubric, client side)

| Gate | Result | Decided by |
|---|---|---|
| Runs without errors in Studio | UNKNOWN | No Play. |
| Client never trusted for currency or ownership | PASS | No client in scope sets a price or an amount. Every remote call passes ids or choices (`BeginForge`, `PolishSword`, `RespondOffer`, `Musashi` "design"/"deal" ids). `MusashiController` 124 `wallet()` is only a nudge before the server's check. |
| Remote and web calls guarded | PASS | Every `InvokeServer` in scope is pcalled (for example AnvilController 780/839/957, PolishController 402/445/453, MusashiController 108, ForgeController 57/110/121/224). `GetProductInfoAsync` at WorldStoreController 86; `PolicyService` at WorldStoreController 104, failing closed. |
| Paid random items: odds shown, Policy fails closed | PASS (client) | The Lucky Metal board shows the odds before the buy (WorldStoreController `showOdds` 282–334). `luckBarred` starts true and stays true on a Policy error (102–106). Server-side luck for restricted regions is in the Server note. |
| No deprecated APIs, no unbounded loops | PASS | No bare `wait(`/`spawn(`/`delay(`. Every `while true` in scope either yields or returns (25 loops checked by script). See the two numeric loops under Leads. |
| StreamingEnabled-safe bindings | PASS | Station controllers bind to Persistent models: Anvil, Forge, IngotRack 1–4, SwordRack 1–2, PolishStation 1–2, EtchingTable 1–2, and `Plot.Musashi` (Persistent, checked today). Forge2/Forge3 are Default; ForgeController 220–226 binds them on `ChildAdded` (209–215) and watches slots that stream in (191–199). |
| ScreenGuis survive respawn | PASS | No StarterGui LayerCollector has `ResetOnSpawn = true`. The `WorldText.BuyButton` and `LevelPromptGui` clones put in PlayerGui are both `ResetOnSpawn = false` (checked today). |

## Dismissed

| Id / lead | Location | Why dismissed |
|---|---|---|
| instance-new-parent ×12 | DevPanel 59, 129, 145, 156, 166, 167, 173, 222, 223, 229, 256, 287 | `Instance.new("UICorner", x)` with one property, in a client-only admin panel. Nothing replicates and nothing is half-built. |
| instance-new-parent | Prototypes.ShapingPrototype 285 | Same (a UICorner), in a Dev-Panel-only prototype. |
| paid-random-no-policy | AnvilController 151 | `Random.new()` is the camera shake. The purchase in the file is the Auto Anvil pass, which is not random. |
| Buy button lost on respawn | TycoonController 344–349, EmployeeController 1422/1444 | The templates are `ResetOnSpawn = false` (Studio, today). |
| Level prompt tap never fires | EmployeeController 1433–1436 | `WorldText.LevelPrompt.HoldDuration` is 0 (Studio, today). |
| Deliveries loop dies on `waiting = nil` | DeliveryController 839, 869 | `Shared.Deliveries.view` always sends `waiting` as a table (155); a missing slot reads `or 0`. |
| Forge2/3 prompt dead after stream-out | ForgeController 64–107 | A streamed-out part is parented to nil and comes back as the same instance with its children. The code relies on this elsewhere too (ShopController 381, TycoonController 175), so the prompt's handler survives. |
| `others` grows with stream cycles | WorldStoreController 168–176 | Same reason: a streamed prompt is the same key, not a new one. |

## Checked, fine

- **Edit-time budget:**
  - SwordMeshCache pcalls its live blade (221), overlay (299–311), etch canvas (358) and sheen image (427–432).
  - It bakes to static content when it can (`bakeContent` 41–48), and frees a failed canvas's overlay share (359–362).
  - PolishController's grime image falls back to no skin when the image budget is full (641–647).
  - EtchCanvas.new raises cleanly when `CreateEditableImage` fails (248–251).
  - EtchPlayback.prepare / load are pcalled by EtchingTableController (462, 491).
- **New code:**
  - MusashiController binds to the Persistent stall. `busy` is reset after its pcall (103–113). Its cards' connections die with the cards. B, Q and Backspace close it, and walking 14 studs away closes it too.
  - StreetCrowd defers its reparent and finds its folder again on a rerun.
  - The sheen and polish sounds follow the idle early-outs.
- **SwordRenderer:** each tool frees its blade, etch and sheen shares on Destroying or untag (298–468, `Destroying:Once` at 450). A late build checks `IsDescendantOf(game)` before welding.
- **Reruns handled:** Guide's trail and arrows, WeatherController's camera effect, AnvilController's outline (398) and spin, ForgeController's fire sound (67), EtchingTable's scratch sound (36), HudFocus's blur, MailController's tracker rows, GemController's boost icons.
- **Per-frame idle early-outs:** PolishController, AnvilController (1223), SwordRenderer (181), CoinFly and RoofHider are all cheap when idle.
- **Helper agents' "fine" lists:** MenuController, MailController, GemController, ItemPicker, HudFocus, CollectionController, SlotMarker, PromptFilter, PromptStyle, ActionButton, CoinFly, UiFx, TextLayers, Cues, Prefs, CrewFaces, NewOreFx, ChatTags, FreeMouse, SecretUnlock, Hud, DevPanel, MyPlot, DayNight, ForgeGlow, RoofHider, AutoRollController, RackController, OreBoxAnimator/OreBoxShow, WeatherController, EmployeeController, Guide and DeliveryController. I spot-checked these and did not re-read them line by line.

## Not checked

- Play behaviour, the Output window and any runtime timing. Every hitch above is static, apart from the 8.8 ms grime build quoted from a session note.
- luau-lsp or type checking: the LihFolk checker is regex-based.
- The 109 `findfirstchild-chain` infos, one by one.
- Read only in part:
  - AnvilController: 395–505, 725–760, 935–1060, 1100–1252.
  - PolishController: 140–330, 436–520, 630–760, 1086–1100, 1246–1262.
  - EtchingTableController: 300–312, 405–460.
  - EtchPlayback: 60–130, 190–240.
  - HiltSeat: 200–212, 258–300, 376–384.
  - SwordMeshCache: 36–80, 150–529.
  - BladeView: in full. EtchCanvas: 39–48, 134–143, 240–256. BladeEtch: 80–96 and its mesh calls.
- Not read beyond grep: BladeCore, EtchPatterns, NewSilhouetteBlades, Hilts, AnvilScore, BladeMesh, BladeProbe and BladeProbeLoader (test-only), and the three Prototypes (Dev Panel only). DecorateController (disabled) was skimmed.
- StarterGui instances beyond ResetOnSpawn and HudPart: which HidesHud screens exist, and the CutsceneGui `In` attributes.

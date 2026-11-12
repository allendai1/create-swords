# Code Audit (2026-11-07)

Read-only Luau audit of the live scripts, done with the lihfolk:audit method plus roblox-luau-patterns. Nothing in Studio was changed; Play was not started. Sources were read out of the Edit place (`execute_luau`, Source only) into a scratch folder and checked there.

## Summary

- **Scope:** 114 scripts: ServerScriptService 30, ReplicatedStorage 31 (Shared, Prototypes), StarterPlayerScripts 53. StarterGui, ReplicatedFirst and Workspace hold no scripts. Left out: TopbarPlus (vendored, 27 modules), `Shared.BladeData` (a data table), ServerStorage.Tests, Legacy and Builders.
- **LihFolk checker:** 1 error, 27 warnings, 218 info. I opened the error and all 27 warnings, and every one turned out to be a false positive (list below). I did not review the 218 `findfirstchild-chain` infos one by one.
- **Findings from reading the code:** 7 in total: 0 P0, 1 P1, 4 P2, 2 P3. None are applied.
- **Overall:** the core server paths hold up. Save locking, receipts, remote validation and leave clean-up are careful and mostly well defended. The real gaps are a few places where one unexpected error stops more than it should.

| P | Count |
|---|---|
| P0 | 0 |
| P1 | 1 |
| P2 | 4 |
| P3 | 2 |

## Applied 2026-11-08

- **P1 (snapshot guard):** `SmithyCore.safeSnapshot` (pcall + warn) now used by `leave`, the autosave loop and BindToClose; a throwing snapshot skips that player's write only. `saveNow` keeps the raw call (ProcessReceipt pcalls it and retries). Backup `Legacy.SmithyCore_beforeSaveGuard_1108`.
- **P2 (receipt twice):** `StoreService.grantProduct` wraps its three `PlaytestLog.log` calls and `SmithyCore.push` in pcall, so nothing after `addGems` / `addCoins` can throw before `addReceipt`. Backup `Legacy.StoreService_beforeSaveGuard_1108`.
- **Checked (Edit):** both compile wrapped in a function; a fresh SmithyCore clone requires; `safeSnapshot` declared above its first use. **Not played.**

## Ranked findings (proposed, not applied)

| # | P | Area | File:line | What breaks for a player, and when | Proposed fix | Effort |
|---|---|---|---|---|---|---|
| 1 | P1 | Data | `ServerScriptService.SmithyCore` 1277–1286 (autosave loop), 1287–1298 (BindToClose), 1219–1236 (`leave`) | `SmithyCore.snapshot` → `encode` runs with no pcall in all three places. Only the save hooks inside it are pcalled (1039). If one player's data makes encode throw (for example a sword whose `etch.body`/`flame` isn't a Color3, so `:ToHex()` at 657 errors), that error takes down the **whole server's** autosave thread: no one on that server is autosaved again. In BindToClose it ends the loop, so the players after that one get no shutdown save. In `leave` it stops before the leave hooks run: the plot isn't released, `data[player]` stays, and that player's last save never happens. Likelihood is low, since encode is simple. Impact is every player on the server. | Take each snapshot with `pcall(SmithyCore.snapshot, player)`. On failure, warn (and log to Analytics) and skip only that player. In `leave`, run the leave hooks and clear `data` whatever the snapshot does. | S |
| 2 | P2 | Data | `SmithyCore` 1117–1138 (`write`), `Profiles` 49, 56–70 | The leaving save (`release = true`) gets 3 attempts over about 6 s. If they all fail (a DataStore hiccup at leave time), it gives up with only a warn. The player loses up to 60 s (AUTOSAVE) of progress, and the lock stays on the key until LOCK_TTL. On their next join, `Profiles.load` waits 6 × 5 s ≈ 30 s on that dead lock before taking it over, and they stand on the street with no plot meanwhile. | When a `release` write returns "error", retry in the background with backoff (for example 3 more over ~30 s). `pending` already makes BindToClose wait for it. | S |
| 3 | P2 | Purchases | `ServerScriptService.StoreService` 124–148, 158–163 | `grantProduct` adds the gems/coins and then calls `SmithyCore.push` and `PlaytestLog.log`, all before `addReceipt` (162). If anything after `addGems` throws (push builds and fires the whole SmithState), the pcall returns NotProcessedYet with no receipt recorded. Roblox's retry then grants the pack **again** in the same session. Likelihood is low. | Keep only the value changes in the grant. Call `addReceipt` straight after them, and run `push` and the logs after the pcall. | S |
| 4 | P2 | Remotes / load | `SmithService` 129 (`GetSmithState`), `RackService` 199–201 (`RackAction` "list"), `GemService` 25–27 ("state") | These read-only remotes have no rate limit: "list" returns before `allowCall` (202), and GetSmithState never calls it. GetSmithState builds and returns the full `publicState`, the large payload in Performance Audit #1. A scripted client calling it in a tight loop uses server CPU and outbound bandwidth that every player on the server shares. Static, not measured. | Add a per-player throttle (for example 0.5 s) on these. Between calls, return the last state or nil. | S |
| 5 | P2 | Client / phones | `StarterPlayerScripts.AnvilController` 647 (`startBlade` → `BladeView.new` → `CreateEditableMesh`), called at 859 after `enterView()` at 857 | Nothing guards the anvil blade's EditableMesh. `SwordMeshCache` 221 and `PolishController` 501–509 pcall theirs because the client's mesh/image budget can be full. If the mesh can't be made on a phone, `onPick` errors after the camera has moved into the anvil view: no blade, `mode` left idle, and the player has to back out by hand. BeginForge already succeeded. Static, not measured. | pcall `BladeView.new`. On failure, `leave()` and toast "Couldn't start, try again" (the existing text). | S |
| 6 | P3 | Robustness | `ServerScriptService.ForgeService` 547–627 (`pull`) | `r.rolling = true` is set at 563 and cleared only at 590/625. Any error in between (`rollFor`, `reveal`, `moveCart`) leaves the lever disabled (`refreshLever`) and the Auto Ore Roller stopped (676) on that plot until the player rejoins. I found no path that errors today; this is hardening. | Wrap the roll in pcall (or `task.spawn` + an always-run reset) so `rolling`/`endedAt`/`refreshLever` are always reset. | S |
| 7 | P3 | Release hygiene | `ServerScriptService.CompareTry_1107`, `ServerScriptService.OreRollerStyleTest` | Both are enabled Scripts, so they run on live servers. Today both do nothing: `Workspace.Compare_1107` is absent and `Style` = "Now". If Compare_1107 comes back, any player gets the `/compare` teleport command and the server runs two Heartbeat CFrame loops. Any Style other than Now makes live servers require `ServerStorage.Builders.restyle_ore_roller` (an Edit-time tool) inside `onPrepare`, which must not yield. | Delete both once the roller style is chosen, as their headers say. Add them to the publish checklist. | S |

## Hard gates (system rubric)

| Gate | Result | Decided by |
|---|---|---|
| Runs without errors in Studio / tests pass | UNKNOWN | No Play run (Allen playtests). Not checked in this audit. |
| Server-authoritative remotes (type, range, rate; client never trusted for currency or ownership) | PASS | Every OnServerInvoke/OnServerEvent was read: SmithService 81/96, PolishService 71/122, EtchService 43, ForgeService 736/789, TycoonService 388, ShopService 329/557/861/929, RackService 184, DeliveryService 464, EmployeeService 1526, GemService 24, InventoryService 15, DecorService 61, SmithyCore 1259, WorldStoreLog 41, the Dev remotes (all `Admins.allowed`). Prices and amounts are computed on the server. The read-only remotes are unthrottled (#4). |
| Data: pcall + retry, session lock, BindToClose, idempotent ProcessReceipt | PASS (with #1–#3) | `Profiles` 56–70 (UpdateAsync, 3 retries), 74–99 (lock), 103–122 (save token, lost lock); `SmithyCore` 1287 BindToClose; `StoreService` 150–172 (receipt ids in the save; only a save that went through answers PurchaseGranted) |
| Paid random items: odds shown, PolicyService fail-closed | UNKNOWN | In game: Lucky Ore's card is hidden unless `ArePaidRandomItemsRestricted` is false, failing closed (`MenuController` 559–560, `WorldStoreController` 102–103). The server applies `Store.luckBonus` (`ForgeService` 463) to any owner, whatever their region. Store-tab purchases bypass the check. Both are already open release blockers (Monetization Plan §11–12). Not re-judged here. |
| No deprecated APIs, no unbounded loops | PASS | Grep: no bare `wait(` / `spawn(` / `delay(` outside TopbarPlus. Every `while true` loop read has a `task.wait`. |

No rubric score: the evidence covers the gates, not the criteria. `/lihfolk:council` can give an independent score.

## Dismissed checker findings

| Id | Location | Why dismissed |
|---|---|---|
| client-sets-currency (error) | `EmployeeController` 1344 | `prompt:SetAttribute("Gems", price)` is the level prompt's display price, not currency. |
| remote-unvalidated-args ×15 | DeliveryService 464, EmployeeService 1526, EtchService 43, GemService 24, InventoryService 15, PolishService 122, RackService 184, ShopService 329/557/761/861/929, SmithService 81/96, WorldStoreLog 41 | Each flagged argument is only compared for equality with server values or literals (`action == "fill"`, `accept == true`, `id == swordId`) or looked up in server tables (`Etches.colorOf`, `hasHotIngot`, `Commissions.byId`). Wrong types fall through to a refusal. |
| instance-new-parent ×11 | DeliveryService 273, EmployeeService 418, Rickshaws 156/221, ShopService 667, StreetLife 167 (`Instance.new("Animator", hum)`), DevPanel 53/119/135/162, ShapingPrototype 285 (`UICorner`) | An Animator with no properties set, or a UICorner with one property: nothing is half-built or replicated twice. |
| paid-random-no-policy | `AnvilController` 141 | The purchase there is the Auto Anvil pass, which is not a random item. Lucky Ore's gate is covered under Hard gates. |

## Checked, fine

- **Profiles session lock:** the lock is taken in `UpdateAsync`, a live lock is waited on, a lost lock stops saving and kicks, a newer-version save is refused, and a lost reply is caught by the `saved` token.
- **SmithyCore saves:** `write` serializes saves per player (`d.saving`). A rejoin on the same server waits for the old Player's saves (`busy`). Leaving during load gives the lock back. A load error kicks without saving. BindToClose waits up to 25 s on `pending`.
- **ProcessReceipt:** unknown product, a missing or still-loading player, or the same purchase id in flight all return NotProcessedYet. A known receipt only saves again. The Starter Pack can be granted twice, which is the documented ponytail decision (StoreService 128–134).
- **Leave clean-up:** every per-player table I found is cleared on leave or rejoin: SmithService/PolishService sessions, ForgeService tutorial/want pulls and furnace slots, ShopService till/cards/slots, EmployeeService working/staffJobs, DecorService, DevTools, WorldStoreLog, Friends pools/lists, Analytics. The onSave hooks put carried, heating, rolled and till items into the save before the leave hooks clear them.
- **Customer sale race:** taking a sword back while its offer card is open can't pay for it. `stillThere()` is checked after `askOwner` (ShopService 1468).
- **Ownership on prompts:** collecting ore is owner-only, the lever and its animation are owner-only, the Cashier's Collect is owner-only, and Take back is owner-only.
- **Customers:** `runCustomer` is pcalled per customer and frees the plot's count either way (ShopService 1549–1566).
- **Web calls:** ComputeAsync, GetFriendsAsync, GetHumanoidDescriptionFromUserId, Marketplace/Policy/ProductInfo calls, AnalyticsService calls and leaderboard SetAsync/GetSortedAsync are all pcalled.
- **Dev remotes:** every handler checks `Admins.allowed` on the server, including `SmithyCore.resetProgress`.
- **UI and connections:** every StarterGui ScreenGui has `ResetOnSpawn = false`, so client references survive respawns. The client's per-use RenderStepped/Heartbeat connections (HiltSeat, EtchingTableController, SecretUnlock, VipIntro, TycoonController build/pop) are disconnected when they finish. EmployeeController cards are fresh clones, and `xpBars` is cleared on redraw.
- **Streaming:** the stations the client controllers `WaitForChild` on (Anvil, Forge, IngotRack 1–4, SwordRack 1–2, PolishStation 1–2, EtchingTable 1–2) are `Persistent` in the template.
- **Locals above their declaration:** a top-level scan of all 114 files found 17 hits, all false positives (nested locals, type fields).
- **Forge timing (noted, not a defect):** ForgeCheck's floors (0.25 s a strike) let a scripted client finish a blade in ~2.5 s instead of ~4–8 s. Hot ingots cap the gain.

## Not checked

- Play behaviour, the Output window and any runtime measurement (all performance notes are static).
- luau-lsp or type checking: the LihFolk checker is regex-based.
- The 218 `findfirstchild-chain` infos, one by one. Top files: ShopService 28, EmployeeService 22, DeliveryService 11, EmployeeController 10, Rickshaws 10.
- Read only in part:
  - EmployeeService 1–1480 (crew and staff loops)
  - SmithyCore.decode 774–1011
  - ShopService 1–150, 610–750 and 1119–1370 (customer walk-in and NPC set-up)
  - ForgeService 1–380
  - TycoonService 1–300
  - DeliveryService 1–330
- Not read beyond grep spot checks: NpcWalk, StreetLife, Rickshaws, CastRigs, Analytics, Guide, MailController, MenuController (only its purchase lines), DeliveryController, ShopController, Hotbar, ItemPicker, CollectionController, WeatherController, GemController, OreBoxShow/OreBoxAnimator, SwordRenderer, SwordMeshCache (only its pcalls), EtchCanvas, BladeCore, BladeEtch, EtchPatterns, and the other Shared data modules.
- DecorateController (disabled), TopbarPlus, ServerStorage.Tests, Legacy and Builders.
- Areas the Performance Audit covers: SmithState size, shine beams, NPC humanoids and idle loops.

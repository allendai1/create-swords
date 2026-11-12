---
title: Code Audit — Server (2026-11-10)
type: review
updated: 2026-11-10
tags: [review, code-audit, server, security, data]
---

# Code Audit — Server (2026-11-10)

Read-only re-run of [[Design/Reviews 2026-11-07/Code Audit]], server half: the lihfolk:audit method (its checker on every file, then a ranked security / data / exploit / performance list), with roblox-luau-patterns and roblox-security. Nothing in Studio was changed and Play was not started. SmithyCore was read as text and never required. The sources were read out of the Edit place with `execute_luau` (Source only) into a scratch folder and checked there. The client scripts are in [[Design/Reviews 2026-11-10/Code Audit — Client]].

## Summary

- **Scope:** 52 files. These are all 32 scripts in ServerScriptService and 20 ReplicatedStorage.Shared modules: Store, Showcase, GemUpgrades, Upgrades, Orders, Commissions, Deliveries, Employees, Customers, Materials, ValueFormula, Admins, Musashi, DayNight, Reputation, ForgeCheck, Hilts, Blueprints, Etches and Senders. Every file's line count matched Studio's.
- **LihFolk checker:** 0 errors, 22 warnings, 127 info. I opened all 22 warnings, and each one is a false positive (listed below). I did not review the 127 `findfirstchild-chain` infos one by one.
- **Locals used above their declaration:** a top-level scan of the 52 files found 10 hits. All 10 are false positives: nested locals, type fields or parameters.
- **Old findings:** 2 are fixed (the old P1 and one P2), 4 are still open, and 1 is on the client side (see the Client note).
- **New findings:** 3 (1 P2, 2 P3). None of them is applied.
- **Overall:** the new code is careful about money and saves. Musashi, gem and Robux weather, 50% More Gems, the bundles, the Showcase families, gem-priced pads, letters from the rack, the bag cap and the leaderboards all check on the server. The server sets every price and amount, and the save decode filters Musashi's new field. I found no P0 or P1.

Open findings on the server side, old and new together:

| P | Count |
|---|---|
| P0 | 0 |
| P1 | 0 |
| P2 | 3 |
| P3 | 4 |

## Old findings (2026-11-07)

| # | Was | Now | Evidence |
|---|---|---|---|
| 1 | P1: snapshot not pcalled (autosave, BindToClose, leave) | **Fixed** | `SmithyCore` 1305–1312 `safeSnapshot` (pcall + warn). It is used by `leave` 1316, the autosave loop 1376 and BindToClose 1387. `leave` always runs its hooks and clears `data` (1320–1327). |
| 2 | P2: a leaving save that fails all 3 tries is given up | **Still open** | `SmithyCore.write` 1219–1221 only warns on "error". `Profiles.update` 56–70 makes 3 tries over about 6 s. There is no background retry for a `release` write. |
| 3 | P2: a throw after `addGems` makes the receipt grant twice | **Fixed** | `StoreService.grantProduct` 140–161: the logs and `push` are pcalled. The only other new call, `weatherBought:Fire` (156), is a BindableEvent and can't throw into it. `addReceipt` follows at 176. |
| 4 | P2: read-only remotes have no throttle | **Still open, and wider** | `SmithService` 129–131 (`GetSmithState`, no `allowCall`), `RackService` 201–203 ("list" before `allowCall`), `GemService` 44–46 ("state"). The new `MusashiService` 86–88 ("state") is the same: it builds the window and, once an hour, rolls the stock through `Hook_StandingPads`. |
| 5 | P2: the anvil's EditableMesh is unguarded (`AnvilController`) | Client | Not re-checked here. See the Client note. |
| 6 | P3: one error in a roll leaves the lever off | **Still open (lines moved)** | `ForgeService.pull` 550–630: `r.rolling = true` at 566 is cleared only at 593 and 628. `rollOut` runs in `task.spawn` (617–620). If it throws, `busy` never reaches 0, so `while busy > 0 do task.wait() end` (625–627) spins every frame for that plot until it goes, and the lever and the Auto Ore Roller stay stopped. I found no path that throws today. |
| 7 | P3: `CompareTry_1107` and `OreRollerStyleTest` run on live servers | **Still open, harmless today** | Both are still enabled Scripts in ServerScriptService. `Workspace.Compare_1107` is absent, so CompareTry returns at line 12. `Style` = "Now". |

## Ranked findings (proposed, not applied)

| # | P | Area | File:line | What breaks for a player, and when | Proposed fix | Effort |
|---|---|---|---|---|---|---|
| 1 | P2 | Data | `SmithyCore` 1202–1223 (`write`), `Profiles` 56–70 | (Old #2.) A DataStore hiccup while a player leaves loses up to 60 s of their progress. The lock also stays on their key, so their next join waits about 30 s on it with no plot. | When a `release` write returns "error", retry it in the background (for example 3 more tries over about 30 s). `pending` already makes BindToClose wait for it. | S |
| 2 | P2 | Remotes / load | `SmithService` 129, `RackService` 201, `GemService` 44, `MusashiService` 86 | (Old #4, now with Musashi's "state".) A scripted client can call these in a tight loop. `GetSmithState` returns the whole `publicState`. That costs server CPU and outbound bandwidth that everyone on the server shares. Static, not measured. | Add a per-player throttle (about 0.5 s) on these four calls. Between calls, return the last result. | S |
| 3 | P2 | Purchases | `StoreService` 114–122 | `PromptGamePassPurchaseFinished` grants the pass for the session when `purchased` is true. It does not check with Roblox first. The passes include earning perks whose results are saved (50% More Coins, 50% More Gems, VIP, Lucky Metal, the Everything Bundle). If an exploit could fake that event, it would get all of them free for the session, and the extra coins, gems and luck would be saved. The LihFolk vault (`Game Passes` §2, `AI Pitfalls - Data and Monetization` §7) says this is **unverified**: the event comes from the engine, not from a remote. It advises re-checking with `UserOwnsGamePassAsync` before granting anything that is saved. This is hardening, not a proven hole. | Grant only when `owns(player, id)` says true. Because ownership can lag a fresh purchase by a few seconds, poll it a few times (for example every 2 s for 10 s) while `purchased` is true. `WorldStoreLog` 70 only logs this event, so leave it as is. | S |
| 4 | P3 | Robustness | `ForgeService` 550–630 | (Old #6.) Any error during a roll leaves the lever off and the Auto Ore Roller stopped on that plot until the owner rejoins. A throw inside `rollOut` also leaves a per-frame wait loop running (625–627). | Run the roll in a pcall (or in `task.spawn` with a reset that always runs) so that `rolling`, `endedAt` and `refreshLever` always reset. Decrement `busy` in a pcall wrapper around `rollOut`. | S |
| 5 | P3 | Release hygiene | `ServerScriptService.CompareTry_1107`, `ServerScriptService.OreRollerStyleTest` | (Old #7.) They do nothing today. If `Compare_1107` comes back, any player gets `/compare`, plus two Heartbeat loops. Any `Style` other than Now makes live servers require an Edit-only builder. | Delete both once the roller style is chosen. | S |
| 6 | P3 | Leaderboards | `DevTools` 57–69 → `SmithyCore.addCoins` 576–585 / `addGems` 640–647 → `LeaderboardService` 88–101 | The Dev panel runs live for `Admins.USERS`. Its +1,000 / +500,000 coins and +100 gems count as earned (`coinsEarned`, `gemsEarned`), and those totals feed the all-servers Coins and Gems boards. A live test session puts Allen's account at the top of every plot's board. | Skip `Admins.USERS` in `LeaderboardService.write` on live servers, or have DevTools take its grant back out of `coinsEarned` / `gemsEarned`. | S |
| 7 | P3 | Purchases | `Weather` 14–15, 42, 104–108 | A bought weather (Robux or gems) lives only in this server. If the server shuts down (for example a restart for an update) during its 5 minutes, or while it waits in the queue, the buyer loses what they paid for, with no make-good. This is a known `shortcut:` in the script, and it is rare because the client greys the buttons while one runs. | Leave it as it is unless logs show it. The fix that keeps it would be a `weatherOwed` field in the buyer's save, granted again on their next join. | M |

## Hard gates (system rubric)

| Gate | Result | Decided by |
|---|---|---|
| Runs without errors in Studio / tests pass | UNKNOWN | No Play run. Not checked in this audit. |
| Server-authoritative remotes (type, range, rate; client never trusted for currency or ownership) | PASS | I read every server handler: SmithService 81/96/129, PolishService 71/122, EtchService 44, ForgeService 739/792, TycoonService 401 and its hooks (Hook_BuyDeal 512, Hook_StandingPads 500), ShopService 76/368/596/800/833/928/991, RackService 186, DeliveryService 494, EmployeeService 1602, GemService 43, MusashiService 85/178, InventoryService 15, DecorService 61, SmithyCore 1354 (Setting), WorldStoreLog 41, Weather 84, and every Dev remote (all check `Admins.allowed`). Prices, discounts and rewards are computed on the server. Musashi's deals come from the saved, server-rolled stock, and `pct` is clamped to 1–90 (TycoonService 518). The read-only remotes are unthrottled (#2). |
| Data: pcall + retry, session lock, BindToClose, idempotent ProcessReceipt | PASS (with #1) | `Profiles` 56–70, 74–99, 103–122. `SmithyCore` 1305–1331, 1372–1397. `StoreService` 164–186 (the receipt id is saved with the progress; only a save that went through answers PurchaseGranted). Musashi's new save field is decoded with type and range checks (`SmithyCore` 1073–1093). |
| Paid random items: odds shown, PolicyService fail-closed | UNKNOWN | Not re-judged here (the pre-release checklist covers it). Showcase Luck swords add `StandLuck` to every roll (`Store.luckBonus` 144–146), as Lucky Metal does. |
| No deprecated APIs, no unbounded loops | PASS | Grep: no bare `wait(` / `spawn(` / `delay(`. Every `while true` loop I opened yields. The one loop that waits on a counter is #4. |

No rubric score: the evidence covers the gates, not the criteria.

## Checker false positives

| Id | Location | Why dismissed |
|---|---|---|
| remote-unvalidated-args ×16 | DeliveryService 494, EmployeeService 1602, EtchService 44, GemService 43, InventoryService 15, MusashiService 85, PolishService 122, RackService 186, ShopService 368/596/800/928/991, SmithService 81/96, WorldStoreLog 41 | Every argument is type-checked, compared for equality with literals or server values, or looked up in server tables before use. Examples: Musashi's `typeof(id) == "string"` plus `table.find(m.stock, id)`, the Delivery "unpack" `typeof(arg) == "number"` plus range and NaN checks, the etch colour `^%x%x%x%x%x%x$` plus the field check, and EmployeeService's `SETTINGS` checks. A wrong type falls through to a refusal or a thrown call, never a grant. |
| instance-new-parent ×6 | DeliveryService 303, EmployeeService 452, Rickshaws 156/221, ShopService 706, StreetLife 167 | `Instance.new("Animator", hum)` with no properties set: nothing is half-built. |

## Checked, fine

- **Musashi (new):** `isOpen` uses only the flag and the Crafter. A design charges only when it is in this hour's stock and not already owned (`Musashi.qualifies`). A deal goes through TycoonService's own `buy`, which checks `available` and `standing`. A gem pad's deal discounts its gems. The stock is seeded by the hour, so the same hour always rolls the same. `MusashiShift` and `DevMusashi` are admin-only.
- **Weather (new):** gem weather requires the tutorial to be done and no bought weather running (`GemService` 73–80). A Robux weather fires once, inside the receipt's grant, and a retried receipt only saves again.
- **50% More Gems and the bundles:** `earnGems` applies only to letters, orders and carts. Bundles grant every member, and the Everything Bundle's AutomationPack recurses once.
- **Bag cap:** every pick-up the player chooses checks `bagFull` before it moves anything: ore, the furnace, both racks, display take-back and cart unpack. Returns and put-backs skip the check, as designed.
- **Letters from the rack:** `letterSword` / `takeLetterSword` remove the sword from exactly one list. Crew jobs `table.remove` a rack sword when they take it, and they check it is still there after walking (`EmployeeService` 1101–1110, 1217–1222), so no sword can be used twice.
- **Showcase families:** these attributes are set on the owner by the server (clients can't set them on the server). Every family is capped (`Showcase.CAP`), so the walk-in timer's factor stays above 0.
- **Staff "off" and three-per-role:** hiring and switching members (`EmployeeService` 1622–1664) are validated, and gems are checked before coins are spent. The level price is capped by the price shown, never raised by it.
- **LeaderboardService:** every SetAsync and GetSortedAsync is pcalled, and BindToClose waits on its writes. With 6 players that is 3 SetAsync calls each every 120 s, well inside the budget.
- **Live analytics:** on live servers `PlaytestLog.log` is `Analytics.log`, whose every AnalyticsService call is pcalled. So the logging inside money paths can't throw.
- **Shutdown:** `Workspace.ThumbnailStaging` (6,463 instances, only LocalScripts `Animate`, which don't run in Workspace) and `NewSwordGallery` are destroyed by their own scripts outside Studio.

## Not checked

- Play behaviour, the Output window and any runtime measurement. All performance notes are static.
- Type checking (luau-lsp): the LihFolk checker is regex-based.
- The 127 `findfirstchild-chain` infos, one by one. Top files: ShopService 28, EmployeeService 22, DeliveryService 11, Rickshaws 10, CastRigs 10, TycoonService 9.
- Read in full: StoreService, GemService, Weather, MusashiService, SmithService, Profiles, PlotService, LeaderboardService, PlaytestLog, Analytics, InventoryService, Shared Store, Showcase, Musashi, ForgeCheck, Admins.
- Read in part:
  - SmithyCore 1–160, 454–693, 1060–1443 (not `publicState` / `push` 201–453 or encode / decode 694–1059, apart from Musashi's decode)
  - ShopService 60–688, 760–1298, 1490–1768 (not 1–59, 689–759 or the customer walk-in 1299–1489)
  - TycoonService 58–91, 280–554
  - EmployeeService 1051–1118, 1197–1226, 1273–1420, 1530–1771
  - ForgeService 236–320, 440–860
  - DeliveryService 440–696
  - RackService 150–352
  - DevTools 1–56 plus its admin checks
  - EtchService 40–84, PolishService 60–140, DecorService 55–112, WorldStoreLog 36–70
- Not read beyond grep: NpcWalk, StreetLife, Rickshaws, CastRigs, Friends, LeverAnimator, CompareTry_1107 and OreRollerStyleTest (headers only), and the Shared data modules Upgrades, Orders, Commissions, Deliveries, Employees, Customers, Materials, ValueFormula, DayNight, Reputation, Hilts, Blueprints, Senders, GemUpgrades (daily and coin rate only) and Etches (`colorOf` / `owns` only).
- Release gates (on-sale status, `Musashi.ENABLED`, which is still `true`, and paid-random policy) are the pre-release checklist's.

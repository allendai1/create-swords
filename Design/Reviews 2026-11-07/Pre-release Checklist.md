---
title: Pre-release Checklist
type: review
updated: 2026-11-07
tags: [review, release, security, monetization, data, create-swords]
---

# Pre-release Checklist (2026-11-07)

Read-only audit against the `roblox-publish-checklist` gates, with `roblox-security`, `roblox-monetization` and `roblox-data`. Studio stayed in **Edit** (no Play, nothing changed, SmithyCore never required: its source was read as text). Evidence is `Script:line` from the live Studio source, Edit-datamodel readbacks through `execute_luau`, and read-only Open Cloud GETs on universe 10771581195. Related: [[Design/Reviews 2026-11-07/Performance Audit]], [[Design/Monetization Plan]].

## Summary

**NOT READY. 6 blockers. Of 14 gates, 8 PASS (ready) and 6 FAIL; 6 items NOT CHECKED.**

- The server code is in good shape: every remote checks its arguments and the player's state on the server, money only moves on the server, the receipt handler is written correctly, and saves have session locks, retries and BindToClose.
- What blocks going public is monetization policy and cleanup: what Lucky Ore's odds show isn't what the game rolls, Lucky Ore can still be bought in restricted regions, managed pricing is off on all 27 items, the live Dev panel needs a keep-or-remove call, Studio writes to the live global leaderboards, and test objects and scripts are still in the place.

## Gates

### 1. Remotes: validation, rate limits, server authority — PASS (one warning)

- 34 remotes in `ReplicatedStorage.Remotes` (readback). Every one that takes client input has a server handler in ServerScriptService: 19 `OnServerInvoke` and 13 `OnServerEvent` (line scan). `SmithState`, `ShopNotice`, `Offer` and `VipIntro` only go from server to client (`ShopService:70`).
- **Flood guard:** `SmithyCore.allowCall` (146–153, `CALL_GAP = 0.25` s per player) is called by BeginForge/FinishBlade (`SmithService:83, 98`), BeginPolish/PolishSword (`PolishService:74, 89`), BuyUpgrade (`TycoonService:405`), Gems (`GemService:29`), Commission/Order (`ShopService:864, 931`), Delivery (`DeliveryService:467`), Employee (`EmployeeService:1533, 1548`), Trash (`InventoryService:17`), EtchSword (`EtchService:45`), DisplaySword take-back (`ShopService:339`). Setting has its own 0.1 s guard (`SmithyCore:1264`), SetDecor its own GAP (`DecorService:65–69`), WorldStore logs once per spot plus a 10 s cooldown (`WorldStoreLog:46–61`).
- **Types and bounds:** `typeof` checks at every handler I read; Trash caps ids at 500 (`InventoryService:13, 17`); SetDecor caps the name at 40 chars (`DecorService:62`); volumes refuse NaN and inf (`SmithyCore:156–160`).
- **Authority:** forging and polishing replay the client's work through `ForgeCheck.evaluate`/`evaluatePolish` with server time (`SmithService:105`, `PolishService:97`), so the client never sends a quality. Distance checks: anvil 12 studs (`SmithService:43–58`), polish station 12 (`PolishService:29–49`), pad (`TycoonService:395–403`), holder (`ShopService:334–337`), forge (`ForgeService:740, 791`). Owner checks on ProximityPrompts: ore stand (`ForgeService:528`), lever (`ForgeService:548`, `LeverAnimator:77`), till (`ShopService:1098`), take-back (`ShopService:273`). An offer answer is only a boolean on an offer id that belongs to that player (`ShopService:557–566`). Prices come from the server (`TycoonService:428`, `GemService:44`); the crew-level price is capped at what the player was shown (`EmployeeService:1562`).
- **Warning:** `GetSmithState` (`SmithService:129–131`) has no `allowCall`. Each call encodes the whole state (the Performance Audit measured 68 KB late game), so a script spamming it costs server CPU and bandwidth.
- Not read line by line: the rest of RackService, Delivery and Employee past their first checks, and ForgePut past line 746.

### 2. Currency, shop, sales, rewards granted by the server — PASS

- Coins live in `leaderstats.Coins` and gems in SmithData, and only the server changes them (`SmithyCore:545–627`); spending checks the balance first (`590–597`, `619–627`). The client can't set them: a Player attribute or value a client changes doesn't replicate to the server.
- Sales pay from server values: Commission deliver checks the sword against the letter (`ShopService:888`), then `earnCoins(c.reward)` (`892`). The daily reward and its streak are worked out on the server (`GemService:33–39`).
- Passes are attributes the server sets (`StoreService:51–63`), read through `Store.owns` (`Store:86–89`).

### 3. ProcessReceipt and developer products — PASS (one note)

- `StoreService:150–172`: an unknown product, a player who isn't here, a purchase already being granted, or a save that hasn't loaded all return `NotProcessedYet`. A purchase id already in the save isn't granted again (`hasReceipt`, `SmithyCore:578`); the last 100 ids are kept and saved (`SmithyCore:115, 582–587, 766, 928–930`). `PurchaseGranted` is returned only after `saveNow` succeeds (`StoreService:164–168`).
- Open Cloud readback: the products that aren't built (Sunshine, Rainbow, Rain, Snow, Epic Ingot, Legendary Ingot) are **off sale**, so their receipts can't get stuck on the unknown-product path. The Starter Pack, 6 coin packs and 5 gem packs are on sale.
- Note: inside the pcall, `grantProduct` runs before `addReceipt` (`StoreService:160–163`). If the grant errors halfway (gems added, then an error), Roblox's retry grants it again. This is unlikely. Moving `addReceipt` before the grant would close it.
- Note: a second Starter Pack receipt is granted on purpose (`StoreService:128–134`).

### 4. Game passes — PASS

- One registry (`Store.PASSES`, `Store:7–20`). Join and purchase go through the same `grant` (`StoreService:51–63, 81–116`). A failed ownership check retries 5 times and counts as unknown, not as not-owned (`66–79`). The pass attributes only take effect in Studio (`88–91`; readback: every StoreService attribute is false, `StudioLocked=false`).
- Open Cloud readback: 8 passes on sale (Auto Ore Roller, 50% More Coins, Lucky Ore, VIP, Swift Boots, Auto Anvil, Auto Etch, Automation Pack). The old Starter Pack pass 2057171214 is off sale.

### 5. Paid random items: odds shown before purchase — FAIL

- An odds panel exists. The Shop's Lucky Ore Buy opens OddsWindow first (`MenuController:523–524, 471–481`), and the world sign shows odds too (`WorldStoreController:275–287`). Both work out odds with `Materials.odds`, the function the roll uses (`Materials:174–182, 210–211`).
- **But the odds shown aren't the odds rolled:**
  - The server adds **beginner's luck +9** until the player first rolls a Rare (`ForgeService:418–421, 462–463`). The comment says "Not on the odds sign". At no merges that is roughly Epic 40% and Legendary 10%, while the panel shows 4% and 1%.
  - Shop panel: the luck is `Upgrades.luck(plot)` only (`MenuController:473`). It leaves out rain's `WeatherLuck`, which the server adds (`ForgeService:461`). The world sign does include rain (`WorldStoreController:283–284`).
  - While an open letter or order wants a metal, every second pull is that metal no matter the odds (`ForgeService:433–444`). Neither panel shows this.
- Rain as a paid product isn't built and its product is off sale, so this gate is about Lucky Ore only.

### 6. Restricted regions (PolicyService) — FAIL

- The restriction is checked only on the client: the Shop hides Lucky Ore's card (`MenuController:558–562, 438`), and so does the world store (`WorldStoreController:99–102`). The server never checks it. `StoreService.grant` gives the pass to anyone who owns it (`StoreService:51–63, 92–93`), and the roll applies `Store.luckBonus` (`Store:97–99`, `ForgeService:463`). The pass is on sale (readback), so someone in a restricted region can buy it from the experience's Store tab and get the luck.
- The found-metal ingot that replaces Lucky Ore in restricted regions isn't built (Epic and Legendary Ingot products are off sale, readback).

### 7. Pricing — FAIL

- Open Cloud readback: `isManagedPricingEnabled = false` and `enabledFeatures = []` on all **9 passes and 18 products**. The API can't turn it on.

### 8. Save data — PASS

- **Session lock:** `Profiles.load` takes the lock with UpdateAsync and waits on another session's lock that is under 300 s old, up to 6 × 5 s, then takes it over (`Profiles:74–99`). Every save first checks the lock is still this session's and answers "lost" if not (`103–122`). On "lost" the server stops saving and kicks the player (`SmithyCore:1128–1133`). A save that got through but lost its reply is recognised by its token, so a retry doesn't write it twice (`Profiles:105–111`).
- **Retries:** 3 attempts with 2 s and 4 s waits (`Profiles:56–70`). If the load fails, the live server kicks rather than starting a blank save (`SmithyCore:1169–1172`).
- **Lifecycle:** autosave every 60 s (`SmithyCore:36, 1277–1286`); a save on leaving that also gives up the lock (`1219–1236`); BindToClose saves everyone and waits up to 25 s for saves still running (`1287–1298`); writes for one player run in order (`1117–1123`); someone who rejoins the same server waits until their old save has landed (`1155–1157`).
- **Schema:** `Profiles.VERSION = 1` with a migration chain, and a save from a newer version is refused (`Profiles:17–34`, `SmithyCore:1177–1184`). Decode fixes duplicate or missing ids (`SmithyCore:774–793`).
- **Studio kept apart:** `Profiles_Studio_v1` in Studio and `Profiles_v1` live (`Profiles:140`). The key is `u<UserId>` (`152`), so a right-to-be-forgotten delete can find it.
- Not run: `ServerStorage.Tests.SaveSpec` (it would need SmithyCore required).

### 9. Global leaderboards (OrderedDataStore) — FAIL

- `LeaderboardService:21` uses `Leaderboard_<stat>_v1`, and Studio and live use the same name (no `IsStudio` anywhere in the script). Studio playtests with API access write their totals to the boards the live game reads, including Dev-panel coins, because `addCoins` adds to `coinsEarned` (`SmithyCore:551–553`, `DevTools:57–62`, +500,000 a press). The key is `player_<UserId>` (`LeaderboardService:5`), which is fine.

### 10. Live Dev panel (Shared/Admins) — FAIL until decided

- `Admins.allowed` is true for anyone in Studio and for UserId 14722022 on live servers (`Admins:12–18`). Every Dev handler checks it on the server: DevTools (`57–229`, all 9), `ShopService:762, 795`, `Weather:63`, `SmithyCore.resetProgress:1308`. The client panel checks it too, but that only hides the buttons (`DevPanel:29`). There's no security hole.
- Live, Allen's account can add coins and gems, give swords, drop passes, change the weather and the clock, and **wipe its own live save** (`Admins:6`). This needs his keep-or-remove decision before going public, and the coins feed the global leaderboard (gate 9).

### 11. Leftover dev/test objects and Studio-only scripts — FAIL

Readback (Edit):

| Object | What it is |
|---|---|
| `ServerScriptService.CompareTry_1107` | Script, **Enabled**. Returns at line 13 because `Workspace.Compare_1107` is gone, so it does nothing |
| `ServerScriptService.OreRollerStyleTest` | Script, **Enabled**, Style = "Now", so it does nothing (`52`). Still requires PlotService on every server |
| `Workspace.Smithy` | 1,134 descendants, **2 unanchored** parts |
| `Workspace.AuxScene` | 10 descendants, **5 unanchored** (they fall in Play) |
| `Workspace.Weapon Rack` / `ZanbatoPreview` / `Courtyard` / `Bamboo9` | 104 / 9 / 6 / 5 descendants, all anchored |
| `Workspace.MaterialDemo` | empty Folder |
| `Workspace.Lighting` | Folder, 4 post effects (do nothing in Workspace) |
| `ReplicatedStorage.Prototypes` | ShapingPrototype (44 KB) and ShapingRules, sent to every client |
| `ReplicatedStorage.Shared.BladeProbe` | 19.6 KB, sent to every client; `BladeProbeLoader` returns unless `workspace.BladeProbe` is set |
| `ServerStorage.Legacy` | 34,058 descendants (server memory only) |
| `ServerStorage.Tests`, `Builders` | server only, fine |

- The `SmithService:140` DevGiveHotIngot hook is Studio-only. PlaytestLog posts over HTTP only in Studio (`PlaytestLog:16`). `DecorateController` is Disabled.

### 12. StreamingEnabled safety — PASS (partly checked)

- `workspace.StreamingEnabled = true`. In the plot template, 12 models are Persistent, 23 Atomic and 425 Default (readback). The radius properties didn't read in Edit (n/a). I didn't check client `WaitForChild` and streaming paths in this pass; the Performance Audit covers the join scans.

### 13. Analytics — PASS

- `Analytics` sends economy (`154`), funnel (`181`, `296`) and custom events (`76`), all in pcall and only from the server, with a per-player budget (`18–19`). The onboarding funnel is `SmithyCore:316`. The WorldStore funnel counts "Bought" only from Roblox's purchase event, not from anything the client says (`WorldStoreLog:70–81`).

### 14. Secrets and text — PASS

- Code that reaches clients has no API key, `apis.roblox.com` URL or webhook (scan of ReplicatedStorage, StarterPlayer, StarterGui, ReplicatedFirst). StarterGui has no TextBox, so players never enter text that would need filtering.

### NOT CHECKED

- Any Play-mode flow: buying, leave/rejoin, shutdown, two servers at once, a ProcessReceipt retry. I didn't play, and Allen playtests himself.
- Device and phone checks, input modes, memory and network profiles (see Performance Audit and UI Audit).
- Creator Hub: the maturity questionnaire, experience privacy, thumbnails and devices. The public games API shows maxPlayers 6 and 3 visits, but not privacy.
- Whether Studio's "Enable Studio Access to API Services" is on.
- `SaveSpec`, `ForgeCheckSpec` and the other specs (not run).
- A rollback plan: the place has version history, but none was recorded for this release.

## Blockers, ranked (fixes proposed, none applied)

0. **Turn Musashi off** (added 2026-11-10; Allen: "I was thinking this could be released in a future update for the game, not initially in the launch ... for now since i haven't tested it, keep it on but remember to turn it off for release."): set `ReplicatedStorage.Shared.Musashi` `Musashi.ENABLED = false` and publish; check no plot has his rug and the Dev Panel has no "Musashi restock". Turn it back on in the update that ships him. [[Sessions/2026-11-10#Musashi behind a feature flag]]
1. **Lucky Ore's odds don't match the roll** (gate 5). Proposed fix: move the luck sum into one shared function, `Materials.luckFor(plot, player, beginner)` = `Upgrades.luck(plot) + Store.luckBonus(player) + rain + beginner`, and call it from `ForgeService.rollFor:461–463`, `MenuController:473` and `WorldStoreController:283–284`. The server shows beginner's luck as a player attribute (`BeginnerLuck = true` while `not rolledRare(d)`), so both panels add `BEGINNER_LUCK`. For the wanted-metal pull (`ForgeService:433–444`), add a line to the panel ("while a letter needs a metal, every second pull is that metal"), or take it out of `rollFor` while Lucky Ore is on sale. **Decided 2026-11-08 (Allen):** "the paid luck boosts apply to paid items, our is not that. it doesn't need to be disclosed the odds for the first pull." Beginner's luck stays hidden. Rain dropped too (Allen: the panel shows permanent odds, a weather is temporary), and the wanted-metal pull is tutorial-only since 2026-11-08. **Closed.**
2. **Lucky Ore bought outside the in-game policy check** (gate 6). Allen's call, as the memory note says. Either (a) take pass 2058881145 off sale and sell Lucky Ore as a one-time developer product prompted only after the server checks `ArePaidRandomItemsRestricted` in ProcessReceipt, or (b) keep the pass and build the found-metal ingot (products 3723120551/3723120555) for restricted players, plus a server-side check in `StoreService.grant` that skips `Pass_LuckyOre` for a restricted player. With (b), work out what that player gets instead, because they paid.
3. **Managed pricing off on all 27 items** (gate 7). In Creator Hub > Monetization, turn on managed pricing (price optimization / regional pricing) for each pass and product. **2026-11-08:** Allen: "Managed pricing should be on for every purchase." The API does turn it on (`isManagedPricingEnabled=true` in the PATCH form) but refuses until the terms are accepted once in Creator Hub ("Managed pricing must be accepted before it can be enabled", tried on 7 Gems). Then Claude switches on all 27.
4. **Studio writes to the live leaderboards** (gate 9). In `LeaderboardService:21`: `"Leaderboard_" .. stat .. (if RunService:IsStudio() then "_Studio_v1" else "_v1")`. Then use `_v2` for the live name at launch, so the entries written from Studio so far aren't shown.
5. **Live Dev panel** (gate 10). Ask Allen whether it stays. If not, empty `Admins.USERS` (`Admins:12–14`) before going public. If it stays, have `SmithyCore.addCoins` leave out Dev amounts (a `dev` flag from `DevTools:61` that skips `coinsEarned`), so the global board stays honest.
6. **Test leftovers** (gate 11). Delete `ServerScriptService.CompareTry_1107` and `OreRollerStyleTest` (their own comments say to), `Workspace.Smithy`, `AuxScene`, `ZanbatoPreview`, `MaterialDemo` and `Workspace.Lighting` (move its effects to `game.Lighting` if wanted). Ask Allen about `Weapon Rack`, `Courtyard` and `Bamboo9`. Move `ReplicatedStorage.Prototypes` and `Shared.BladeProbe` (with `BladeProbeLoader`) to ServerStorage. Back them up as .rbxm first (Archive/Studio Backups), and rerun the load check on anything that required them.

**Warnings (not blocking):** `GetSmithState` has no flood guard (`SmithService:129`; add `if not SmithyCore.allowCall(d) then return nil end` and check the 14 join-time fetchers handle nil). `addReceipt` comes after the grant (`StoreService:161–162`): fixed 2026-11-08, the log and push after the grant can't throw any more. A second Starter Pack receipt is granted on purpose.

**2026-11-08:** blocker 3 (managed pricing) done on the launch universe: all 26 Swordsmith Tycoon copies on (readback). [[Sessions/2026-11-08#Managed pricing: the group has it, the user account doesn't]]

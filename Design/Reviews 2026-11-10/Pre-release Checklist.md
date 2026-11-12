---
title: Pre-release Checklist
type: review
updated: 2026-11-10
tags: [review, release, security, monetization, data, create-swords]
---

# Pre-release Checklist (2026-11-10)

A re-run of [[Design/Reviews 2026-11-07/Pre-release Checklist]] against the `roblox-publish-checklist` gates, with `roblox-security`, `roblox-monetization` and `roblox-data`. It is read-only. Studio stayed in **Edit**: no Play, nothing changed, and SmithyCore was never required (its source was read as text). The evidence is `Script:line` from the live Studio source of Swordsmith Tycoon (place 93453899201090), Edit readbacks through `execute_luau` (modules required from a fresh clone of `Shared`), and GETs only on universe 10769630190 (Open Cloud and Roblox's public web APIs). Related: [[Design/Monetization Plan]], [[Sessions/2026-11-08]], [[Sessions/2026-11-09]], [[Sessions/2026-11-10]].

## Summary

**NOT READY. 6 blockers. Of 22 gates, 16 PASS and 6 FAIL. 9 items NOT CHECKED.**

- Fixed since 11-07: managed pricing is on for all 26 items the code sells, and every pass and product id in the code matches a Swordsmith Tycoon item. Allen closed the odds blocker by decision. Most of the old Workspace test models are gone.
- New systems check out on the server: bought weather, Golden Hour, gem-priced pads, the bundles, 50% More Gems and Musashi's remote all take prices from the server and check the player's state.
- **New and urgent:** Roblox reports the universe as **Public**, with a server size of **40**. The map has 6 plots, so a 7th player gets no plot. Allen should confirm who can join today.
- Still open: Musashi is on, Lucky Metal has no server-side region check, the live Dev panel, Studio and live share the leaderboards, and the test scripts are still in the place.

## Gates

### 1. Remotes: validation, rate limits, server authority — PASS (two warnings)

- `ReplicatedStorage.Remotes` holds 37 remotes (34 on 11-07, plus Musashi, DevMusashi and DevLearnSwords). Order, Delivery, Employee and two more are made at runtime (`ShopService:986`, `DeliveryService:30`, `EmployeeService:74`, `SmithService:29`, `ForgeService:44`). Every remote that takes client input has a server handler (line scan of ServerScriptService).
- **New handlers checked:**
  - `Musashi` (`MusashiService:85–122`): the id must be a string; the save loaded; `allowCall`; the stall open (the flag and the Sword Crafter, `41–43`); the design in this hour's stock; `Musashi.qualifies`. Prices come from `Musashi.byId` (`101`). A deal must be in this hour's deals (`112–113`). TycoonService re-checks it and clamps the discount to 1–90% (`TycoonService:512–519`).
  - `DevMusashi`: the flag and `Admins.allowed` (`MusashiService:178–183`). `DevLearnSwords`: `Admins.allowed` (`DevTools:185–186`).
  - Employee `"off"`: a known role, hired, a boolean, `allowCall` (`EmployeeService:1622–1625`).
- `allowCall` (`SmithyCore:156`, `CALL_GAP = 0.25` at `36`) still guards BeginForge/FinishBlade (`SmithService:83, 98`), BuyUpgrade (`TycoonService:418`), Gems (`GemService:48`), Commission and Order (`ShopService:931, 993`) and the rest.
- **Warning:** `GetSmithState` still has no flood guard (`SmithService:129–131`). Musashi's `"state"` action has none either (`MusashiService:86–88`), but it is cheap: it only rolls stock once an hour.

### 2. Currency, shop, sales, rewards granted by the server — PASS

- Coins are spent and added only on the server (`SmithyCore:576–628`); gems the same (`640–666`). Every spend checks the balance first (`623`, `660`).
- The new spends: gem pads (`TycoonService:445–455`), bought weather for gems (`GemService:73–80`), Musashi's designs (`MusashiService:101`). Each uses a server price.

### 3. ProcessReceipt and developer products — PASS (one warning)

- `StoreService:164–186`: an unknown product, a missing player, a purchase already being granted, or a save not loaded all return `NotProcessedYet`. A receipt already in the save isn't granted again (`174–177`). `PurchaseGranted` is returned only after `saveNow` succeeds (`181–182`).
- The 11-08 fix is in place: the logs and the push inside `grantProduct` are in pcall (`148, 152, 157, 161`), so a throw can't skip `addReceipt`.
- Bought weather goes through the same path (`154–158`): a retried receipt never starts a second weather.
- Products the code doesn't know (Rain, Rainbow, Epic Ingot, Legendary Ingot) are **off sale** (readback), so no receipt can get stuck on them.
- **Warning:** a Robux weather bought while another bought weather runs waits in a queue that lives only in that server (`Weather:14–15, 104–108`). If the server shuts down first, the buyer paid and got nothing.

### 4. Game passes — PASS

- One registry (`Store:7–29`). Join and purchase use the same `grant` (`StoreService:55–67, 85–123`). A bundle grants each member as if bought (`62–65`), and the Everything Bundle's Automation Pack grants its three in turn.
- Readback (fresh Shared): every pass is in the Everything Bundle (none missing); `Store.owns` counts bundles (`Store:124–134`).
- Open Cloud: all 11 passes in the code are on sale. The other 22 passes in the universe (the old bridge game's) are all off sale.

### 5. Paid random items: odds shown before purchase — PASS (risk accepted by Allen)

- The roll: `ForgeService:466` = plot luck + `Store.luckBonus` (Lucky Metal + Showcase luck) + rain + beginner's luck. The Shop's odds panel uses the plot's luck + Showcase luck, with and without the pass (`MenuController:626–627`). The board uses `Store.luckBonus` (`WorldStoreController:291`).
- The pass description's odds match `Materials.odds`. Readback at luck 1 and 1.5: Common 59.9 → 39.85, Uncommon 25 → 37.5, Rare 10 → 15, Epic 4 → 6, Legendary 1 → 1.5, Secret 0.1 → 0.15.
- The wanted-metal pull is tutorial only now (`ForgeService:436`).
- **Accepted risk:** beginner's luck +9 is still left out of every odds view (`ForgeService:420–423, 465`). Allen's call, 2026-11-08: "it doesn't need to be disclosed the odds for the first pull." Rain is left out of the Shop panel on purpose (a temporary boost).

### 6. Restricted regions (PolicyService) — FAIL

- `ArePaidRandomItemsRestricted` is still read only on the client (`MenuController:770–775`, `WorldStoreController:102–106`). The server never checks it. `StoreService.grant` gives `Pass_LuckyOre` to anyone who owns the pass (`StoreService:55–67, 93–103`), and the roll adds the luck (`Store:144–146`, `ForgeService:466`).
- This is now wider: the **Everything Bundle** (2075914814) holds Lucky Metal and is on sale too. Both can be bought from the experience's Store tab.
- The found-metal ingots for restricted players (3729904305, 3729904292) are still off sale and not built.

### 7. Pricing — PASS (fixed)

- Open Cloud readback: all 11 passes and 15 products the code uses have `isManagedPricingEnabled = true` and `enabledFeatures = ["RegionalPricing"]`. Prices match the [[Design/Monetization Plan]].

### 8. Save data — PASS

- **Session lock** unchanged: `Profiles:74–99` (load), `103–122` (save checks the lock, a lost reply is recognised by its token). On "lost" the server stops saving and kicks (`SmithyCore:1213–1218`).
- **Retries:** 3 attempts with backoff (`Profiles:56–70`). A failed load kicks on live servers and never starts a blank save (`SmithyCore:1254–1258`).
- **Lifecycle:** autosave every 60 s (`SmithyCore:37, 1372–1382`); save on leave with the lock released (`1314–1331`); BindToClose saves everyone and waits up to 25 s (`1383–1397`). `safeSnapshot` (`1305–1312`), so one bad save doesn't stop the others.
- **Schema:** `Profiles.VERSION = 1` with a migration chain; a newer save is refused (`Profiles:18–34`, `SmithyCore:1262–1267`). The new fields are checked on load: `musashi` (`SmithyCore:1074–1090`, each id and percent bounded) and a staff member's `off` (`788, 951`).
- **Studio kept apart:** `Swords_Profiles_Studio_v1` and `Swords_Profiles_v1` (`Profiles:140`); key `u<UserId>` (`152`).

### 9. Global leaderboards (OrderedDataStore) — FAIL

- `LeaderboardService:21` uses `Swords_Leaderboard_<stat>_v1` in Studio and live alike (renamed on 11-08, still no `IsStudio`). Readback: the Coins board already has 4 entries.
- Dev-panel coins still count as earned (`DevTools:61` → `SmithyCore:582–584`), so they reach the board.

### 10. Live Dev panel (Shared/Admins) — FAIL until decided

- Unchanged: anyone in Studio and UserId 14722022 on live servers (`Admins:12–18`). Every Dev handler checks it on the server: `DevTools` (10 handlers, `58–244`), `ShopService:801, 834`, `Weather:85`, `MusashiService:179`, `SmithyCore:1407`. No hole, but Allen's live account can add coins and gems and wipe its own live save.
- **Warning:** the Dev weather button calls `start()`, which clears the buyer, so it cuts a bought weather short (`Weather:84–89, 55`).

### 11. Leftover dev/test objects and Studio-only scripts — FAIL

Gone since 11-07: `Workspace.Smithy` (now `ServerStorage.OldSmithy`), `AuxScene`, `ZanbatoPreview`, `MaterialDemo`, `Weapon Rack`, `Courtyard`, `Bamboo9`.

Still there (readback, Edit):

| Object | What it is |
|---|---|
| `ServerScriptService.CompareTry_1107` | Script, **Enabled**. Returns at line 13 (no `Compare_1107`) |
| `ServerScriptService.OreRollerStyleTest` | Script, **Enabled**, Style "Now", so it does nothing (`52`). Still requires PlotService |
| `Workspace.Lighting` | Folder with 4 post effects (no effect in Workspace) |
| `ReplicatedStorage.Prototypes` | ShapingPrototype (44 KB), ShapingRules (9 KB), **PackingPrototype (42 KB, new)** and PackingParts (5 meshes). Sent to every client; only the Dev panel uses them (`DevPanel:327, 335`) |
| `ReplicatedStorage.Shared.BladeProbe` | 19.6 KB to every client; `BladeProbeLoader` (Enabled) returns unless `workspace.BladeProbe` is set (`BladeProbeLoader:8–11`) |
| `ServerStorage.Legacy` | **73,019** descendants (34,058 on 11-07); server memory only |
| `ServerStorage.OldSmithy`, `ThumbnailStages`, `Tests`, `Builders` | Server only, fine |

### 12. StreamingEnabled safety — PASS (partly checked)

- `workspace.StreamingEnabled = true`. The new `Plot.Musashi` is Persistent (readback). Client `WaitForChild` paths weren't checked.

### 13. Analytics — PASS

- `Analytics` sends economy (`154`), funnel (`181`, `296`) and custom events (`76`), in pcall, from the server, with a per-player budget (`33`, `86`). WorldStoreLog counts "Bought" only from Roblox's purchase event (`WorldStoreLog:70–79`).

### 14. Secrets and text — PASS

- No API key, `apis.roblox.com` URL, `x-api-key` or webhook in any script (scan of ServerScriptService, ReplicatedStorage, StarterPlayer, StarterGui, Workspace). PlaytestLog posts only in Studio, to 127.0.0.1 (`PlaytestLog:16–19, 26`).
- The only TextBox is the Dev panel's search, which filters a local list (`DevPanel:158`).

### 15. Ids in code match the Swordsmith Tycoon items (new) — PASS

- `Store:7–29` (11 passes) and `Store:46–75` (15 products) match the Monetization Plan and the Open Cloud readback, 26 of 26. A scan finds no old Sell Swords! id in any live script. Every purchase prompt reads `Store.PASSES` or `Store.PRODUCTS` (`MenuController:645–647`, `PackOffer:42`, `WorldStoreController:275, 463`, `AnvilController:1133`, `EtchingTableController:140`, `AutoRollController:124`).

### 16. Bought weather and Golden Hour (new) — PASS (two warnings)

- Robux: `StoreService:154–158` fires `Weather.Bought` inside the receipt path. Gems: `GemService:73–80` checks the key, the tutorial letter is done, no bought weather is running, then spends `WEATHER_GEMS` (60 / 60 / 120, `Store:77`). Golden Hour is bought only and has no luck (`Weather:32–34`), so it is not a paid random item.
- Sunshine and Snow are on sale (readback). **Warning:** Golden Hour (3730123757) is **off sale**, so its Shop card can only be bought with gems. The queue warning is under gate 3.

### 17. Gem-priced pads (new) — PASS

- Readback: Showcase Stand 2 costs 100 gems and Stand 3 costs 250, with coin price 0. `TycoonService:445–455` spends gems, refuses when short and offers the covering gem pack. Musashi's deals discount the gem price too (`446–448`).

### 18. Bundle and pack grants (new) — PASS (one warning)

- Everything Bundle and Automation Pack: gate 4. Starter Pack: 250 gems and 5,000 coins (`Store:98, 101`), which matches its Roblox description ("250 gems and 5,000 coins, once.").
- **Warning:** a bundle bought on the Store tab by someone who owns a member charges for it again. The Shop hides the card in that case (Monetization Plan, Open).

### 19. 50% More Gems math (new) — PASS

- `SmithyCore:651–655`: `math.round(amount * 1.5)`. Readback: 1→2, 2→3, 3→5, 5→8, 10→15. It applies to letters (`ShopService:956`), mail orders (`ShopService:1040`) and carts (`DeliveryService:595`), not to the daily gift (`GemService:58`) or bought packs (`StoreService:147`). This matches the pass description.

### 20. Musashi feature flag (new) — FAIL

- `Shared.Musashi:22`: `Musashi.ENABLED = true`. Readback: 10 `musashi*` blueprints load, and `Plot.Musashi` is in the template. MusashiService removes the stall and stays shut when the flag is off (`MusashiService:41–43, 164–171`).

### 21. Studio-only objects that would ship (new) — PASS by code (not played)

- `Workspace.ThumbnailStaging` (6,463 descendants, 11 inert Animate LocalScripts, 38 unanchored parts) is destroyed at server start by `ThumbnailStagingCleanup:4–7`. That runs before any player joins.
- `Workspace.NewSwordGallery` (309 descendants) destroys itself outside Studio (`NewSwordGallery.StudioOnly:2–4`).
- Neither has been seen gone in a running server. Both still add to the place file and the server's start.
- 23 Dev-panel-only blueprints ship to every client (the bō-hi katana and 22 new silhouettes, `BladeData:3036–3043`, `Shared.NewSilhouetteBlades` 44.9 KB). The Book hides them (`CollectionController:287`). Only `DevLearnSwords` gives them, and it is admin only.

### 22. Experience settings (new) — FAIL

- Open Cloud `universes/10769630190`: `visibility = PUBLIC`, `ageRating = AGE_RATING_ALL`, voice chat on, desktop, phone, tablet and VR on, console off, **description empty**. The public develop API also reads `privacyType: Public`, `isActive: true`, `audiences: [1, 4]`. The session notes up to 11-09 call the game private.
- The place's `serverSize` is **40**. The map has **6 plots**, and `PlotService:13` says "a seventh player gets no plot (set the server size to 6 in Game Settings)".
- The place was last published 2026-11-10 22:00:05 UTC. 0 badges; an icon and 3 thumbnails exist, but I didn't look at them.

### NOT CHECKED

- Any Play-mode flow: Robux and gem weather, the bundles, gem pads, Musashi buys, the bag cap, leave/rejoin, shutdown, a receipt retry, and the two Studio-only cleanups in a running server.
- Phones, input modes, memory and network.
- What `audiences: [1, 4]` means, so whether the public can join today. Creator Hub's maturity questionnaire and the thumbnails' content.
- Whether Studio API access is on. The games API says `studioAccessToApisAllowed: false`. In Edit, a DataStore `GetAsync` was refused ("Access forbidden"), but reading the Coins leaderboard and listing data stores worked.
- What the live version holds, Musashi on or off. Published versions can't be read from Edit.
- `SaveSpec` (it requires SmithyCore). `SwordMeshSpec`, `EtchingSpec` and `BladeCoreSpec` were not re-run; the 11-10 note has SwordMeshSpec at 214 stale bakes. **Run:** `ForgeCheckSpec` on a fresh Shared, 1,227 ok, 0 failed.
- Who wrote the 4 Coins leaderboard entries (Studio or live).
- RackService, DeliveryService and EmployeeService past the handlers named above.
- A rollback plan: none is recorded for this release.

## Blockers, ranked (fixes proposed, none applied)

**Status 2026-11-10 (later):** 1 Allen set the server size to 6 and keeps the game public. 2–6 fixed in Edit, not played, not published: Musashi off; Lucky Metal a one-time product refused in restricted regions (pass off sale, out of the bundle); Dev panel kept for goku19876, its coins off the boards; leaderboards `_v2` / `_Studio_v1`; test leftovers moved or dropped on live. [[Sessions/2026-11-10#Release gates: the fixes]]

1. **Server size 40 with 6 plots, and the game reads Public** (gate 22). Universe readback `visibility PUBLIC`, place `serverSize 40`, `PlotService:13`. Fix: set the server size to 6 (Creator Hub > Places > Settings, or an Open Cloud place PATCH with Allen's OK). Allen confirms whether the public should be able to join now. If not, make it private until blockers 2–6 are closed, because the live version may already have Musashi and the Dev panel.
2. **Musashi is on** (gate 20, old blocker 0, still open). `Shared.Musashi:22`. Fix: `ENABLED = false`, check `Plot.Musashi` is removed in Play and the Dev panel has no "Musashi restock", then publish.
3. **Lucky Metal and the Everything Bundle have no server-side region check** (gate 6, old blocker 2, still open and wider). `StoreService:55–67, 93–103`. Fix (Allen picks): (a) sell Lucky Metal as a developer product, granted only after `ArePaidRandomItemsRestricted` is checked in ProcessReceipt, and take pass 2075536519 out of the bundle; or (b) keep the passes, have `grant` skip `LuckyOre` for a restricted player, and build the found-metal ingot (3729904305 / 3729904292) as what they get instead.
4. **Live Dev panel** (gate 10, old blocker 5, still open). `Admins:12–14`. Fix: empty `Admins.USERS` before going public, or keep it and have `addCoins` skip `coinsEarned` for Dev amounts (`DevTools:61`).
5. **Studio and live share the leaderboards** (gate 9, old blocker 4, still open). `LeaderboardService:21`. Fix: `"Swords_Leaderboard_" .. stat .. (if RunService:IsStudio() then "_Studio_v1" else "_v1")`, and use `_v2` at launch so the 4 entries written so far don't show.
6. **Test leftovers** (gate 11, old blocker 6, partly fixed). Fix: delete `CompareTry_1107` and `OreRollerStyleTest`. Delete `Workspace.Lighting`, or move its effects to `game.Lighting`. Move `ReplicatedStorage.Prototypes` and `Shared.BladeProbe` (with `BladeProbeLoader`) to ServerStorage, and drop the Dev panel's prototype buttons or load them only in Studio. Back them up as .rbxm first, then rerun the load checks.

**Old blockers:** 0 Musashi still open (2). 1 odds closed by Allen's decision; the formula was checked again (gate 5). 2 region check still open (3). 3 managed pricing **fixed** (gate 7). 4 leaderboards still open (5). 5 Dev panel still open (4). 6 leftovers partly fixed (6).

## Warnings (not blocking)

- `GetSmithState` has no flood guard (`SmithService:129`); Musashi `"state"` neither (`MusashiService:86`).
- The Lucky Metal pass description on Roblox shows garbled arrows ("â†’" for "→") in its odds line. The Everything Bundle's description still says "Lucky Ore".
- Golden Hour is off sale while its Shop card shows (gate 16).
- A queued Robux weather is lost if the server shuts down (`Weather:14–15`).
- The Dev weather button cuts a bought weather short (`Weather:84–89`).
- Bundles bought on the Store tab charge again for passes already owned.
- A second Starter Pack receipt is granted on purpose (`StoreService:133–141`).
- `ServerStorage.Legacy` doubled to 73,019 descendants. Dev-only blueprints and their profiles ship to clients (gate 21).
- The experience description is empty, and voice chat is on.

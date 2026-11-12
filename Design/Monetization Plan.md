---
title: Monetization Plan
status: decided 2026-10-27; the six passes and the Shop page built, not played; passes on sale (game private), products off sale
type: design
updated: 2026-10-27
tags: [monetization, robux, game-pass, developer-product, ore, weather, create-swords]
---

# Monetization Plan

Allen, 2026-10-27: "research all the potential developer products we can have for purchase with robux. gamepasses, 1 starter pack. gamepasses that ease the experience, or provide better bonuses, luck, etc. 1 of them in my mind is an auto ore roller that shows up on your screen for purchase whenever youre near the ore roller itself. its would be a small popup with a lock icon to show you can buy it."

Builds on [[Design/Game Design Document#15. Monetization (Robux)|GDD §15]] (its rule stays: **Robux speeds things up or adds style, but anyone can earn everything by playing**) and [[Archive/Design/Progression and Economy Review — 2026-10-27#9. Game passes and developer products|the review's §9]]. Pace numbers are `Development/economy_model.py` after [[Design/Economy Pass 2]] and its customer rate: a casual player who keeps Rare+ ore.

**Decided with Allen on 2026-10-27** in a walkthrough of the first draft's questions ([[Sessions/2026-10-27#Monetization walkthrough]]); his answers are at the end. **Nothing here is built;** prices are starting points for Roblox's price test (§7). The passes and products exist on Roblox (ids in §11); the passes are on sale while the game is private.

## The short version

- **Passes:** the Auto Ore Roller (Allen's popup, §5), 50% More Coins, Lucky Metal (luck one merge higher), VIP (+10% on every sale) and Swift Boots.
- **One Starter Pack:** 250 gems and 5,000 coins for 99 R$ (since later on 2026-11-08; 25,000 coins earlier that day).
- **Weather for the whole server, about 5 minutes, bought with Robux or gems** (Allen's design, §3): sunshine brings customers, a rainbow VIP customers, rain luck, snow mail.
- **Coin packs and gem packs**, and an ingot of a found metal for players where paid luck is restricted.
- **Pace:** 50% More Coins and VIP together bring Rin from 13 h 17 to 8 h 32. The Auto Ore Roller is comfort (12 h 30); Lucky Metal is for collectors (12 h 58).

## 1. Game passes (bought once, kept)

| Pass | What it does | Start price | Rin | Notes |
|---|---|---|---|---|
| **Auto Ore Roller** | Pulls the lever for you until a kept rarity lands (§5) | 149 R$ | 13 h 17 → 12 h 30 | Allen's idea. Not a paid random item: the rolls stay free, it buys the pulling |
| **50% More Coins** | Every coin you earn ×1.5: sales, carts, orders | 199 R$ | → 9 h 18 | Allen chose +50% over the draft's 2× (which made it 7 h 15) |
| **Lucky Metal** | Luck one merge higher (+0.5), on top of your merges | 149 R$ | → 12 h 58 | **Paid random item:** the odds panel before buying (§4). Close to Create Pottery!'s Lucky Clay (about ×1.7 on Rare+) |
| **VIP** | +10% on every sale; a gold name tag; VIP customers twice as often (since 2026-11-07) | 299 R$ | → 12 h 12 | Allen: "+10% on every sale", in place of the draft's golden rack |
| **Swift Boots** | Walk 50% faster (WalkSpeed 16 → 24, since 2026-11-09; 20 before) | 99 R$ | not modelled | Kept by default; plots are walk-heavy |

| Time to | Katana | Longsword | Crafter | Falchion | Gladius | Zanbatō | Rin |
|---|---|---|---|---|---|---|---|
| No passes | 21 min | 1 h 20 | 2 h 05 | 3 h 12 | 5 h 45 | 8 h 46 | 13 h 17 |
| Auto Ore Roller | 18 min | 1 h 13 | 1 h 55 | 3 h 03 | 5 h 24 | 8 h 16 | 12 h 30 |
| Lucky Metal | 20 min | 1 h 17 | 2 h 01 | 3 h 08 | 5 h 37 | 8 h 34 | 12 h 58 |
| VIP | 19 min | 1 h 14 | 1 h 55 | 3 h 00 | 5 h 19 | 8 h 04 | 12 h 12 |
| 50% More Coins | 16 min | 58 min | 1 h 27 | 2 h 16 | 4 h 06 | 6 h 09 | 9 h 18 |
| 50% More Coins + VIP | 16 min | 54 min | 1 h 20 | 2 h 05 | 3 h 46 | 5 h 41 | 8 h 32 |
| All four | 13 min | 48 min | 1 h 13 | 1 h 57 | 3 h 32 | 5 h 21 | 8 h 02 |

Method: `economy_model.run` for that player with the live customer rate; 50% More Coins = every price ÷ 1.5, VIP = ÷ 1.1 (counted on all income), Lucky Metal = luck 1.5 in `picked`, Auto Ore Roller = 1 s of pulling a sword. Weather isn't modelled. The model lets the Auto Roller pull instantly; in the game it pulls every ~5 s, which keeps up while you craft (a Rare+ result takes ~33 s of pulling with one ore slot, ~6 s with six).

## 2. The Starter Pack (one)

- **Coins 5,000 (later on 2026-11-08):** Allen: "Starter coins 5,000", from [[Design/Economy and Progression Review — 2026-11-08#3. The Starter Pack's 25,000 coins buy the first half hour in one tap; its gems are what speed the game]]: 25,000 bought a new player's first 19 pads, the Sword Crafter too, in one tap, while the 250 gems give most of the pack's speed-up (sim, casual Zanbatō 11:01 without the pack, 9:52 gems only, 9:47 with 5,000, 9:36 with 25,000). `Store.STARTER_COINS` 5000; product description "250 gems and 5,000 coins, once." (PATCH 204, read back). The live tag now works out 2× VALUE (224.5 + 16.7 R$ against 99, floored).
- **Contents (2026-11-08, until the change above):** **250 gems and 25,000 coins** (Allen: "it's a huge card for seemingly very little reward"; Claude's recommendation; a Gold ingot too until Allen's "dont give ingots ... and starterpack too" the same day). The card shows two tiles and a live "3× VALUE" tag (the shop's cheapest rate per item: 224.5 + 83.3 R$ against 99; the ingot counted as nothing). The ingot doesn't fill Gold's book page. Product description on Roblox updated the same day. [[Sessions/2026-11-08#Starter Pack: 250 gems, 25,000 coins and a Gold ingot]]
- **Contents 2026-10-29 to 2026-11-08:** 100 gems and **10,000 coins** (Allen: "our starterpack is not very enticing, should give a set amount of gold not just a gold ingot"; he chose coins only). Until then: 100 gems (exactly Better Advertising II + More Clients I) and a **Gold ingot** (Epic ×5, a fixed metal, so not a paid random item). The ingot doesn't fill Gold's book page; that still has to be rolled. No etch (Allen).
- **Price:** 99 R$, the best value in the shop (gem packs give fewer gems per Robux).
- **Kind: a developer product since 2026-11-01** (Allen: "Starterpack should be a dev product, not game pass. but obviously single purchase only"; it was a game pass, now off sale). One purchase is kept by the game: `ProcessReceipt` grants the gems and coins and sets `starterGranted` in the save (the purchase id saved like every product's); that flag is the player attribute `Pass_StarterPack`, so once it's granted the Shop card is gone and the client never prompts it. A second receipt anyway (two servers prompting at once) is still granted, since the player paid, and logged. Studio's Reset progress clears the flag, so it can be bought again. A product doesn't show on the experience's Store tab.
- **Offer:** after the tutorial, the Shop button gets the amber dot the Mail button uses, and the pack sits first in the Shop window until bought. No popup, no countdown, nothing in the first session's tutorial.

## 3. Weather (Allen's design)

Allen: "the weather should only be around 5 minutes. sunshine can give 2x more customers, rainbow can give higher chance of vip customer, rain gives higher luck for rolling, snowing for more mail/custom requests"

| Weather | For every shop in the server, about 5 min | Needs |
|---|---|---|
| **Sunshine** | Customers come twice as often | The free Sunshine (built in [[Design/Shop Tension Pass]], `ServerScriptService.Weather`) |
| **Rainbow** | VIP customers come more often | VIP buyers (built in the shop tension pass: `Customers.VIP_CHANCE` 5%) |
| **Rain** | Luck one merge higher (+0.5) at every roller; adds to Lucky Metal | The odds panel when bought (§4) |
| **Snow** | Mail orders and commissions come twice as often | The mail clock (built) |

- **Free and bought:** weather also comes on its own (GDD §7): since Fixes2 (2026-10-28) one of the four is always on, 5 min each, the better ones rarer (Sunshine 35, Snow 30, Rain 20, Rainbow 15; [[Design/Decisions Log#Fixes2 — 2026-10-28]]). A bought weather starts at once, or straight after another bought one; the buyer is named beside the weather's HUD icon.
- **Price:** 79 R$ or 60 gems each. Gems from daily rewards (192 a week since 2026-11-09, gems only) or gem packs can buy it, so gems keep a use after the Gem Shop's 325 (Allen). The Gem Shop costs 990 in all since 2026-11-03 (gentler prices).
- **Guardrails:** a plot still in the tutorial gets no weather bonus (the first-sale gate, GDD §7); one weather at a time; no Robux offers pop up during one.
- **Rain is a paid random item** when bought, with Robux or with gems (gems can be bought with Robux): the odds panel before buying, and players where that's restricted can't buy rain (they still get it when it falls).

Supersedes GDD §7's "other weather stays at the normal baseline" and [[Design/Workshop Growth#Weather and customer traffic|Workshop Growth]]'s "No paid weather controls were chosen."

## 4. Luck and Roblox's paid random items rules

Roblox counts luck boosts as paid random items: here **Lucky Metal** and **bought rain**. Before anyone pays, the game shows every rarity's odds as percentages adding to 100, now and with the boost, for that player's luck (merges and weather change it). An (i) button alone is not enough.

**The odds panel** follows Allen's screenshot of Create Pottery!'s "Lucky Clay odds" (shared in chat on 2026-10-27; Lucky Clay doubles the weight of Rare and above): a title ("Lucky Metal odds"), one line ("Your chance of each rarity on your next pull."), two columns **Now → With Lucky Metal**, rarity names in their colours and the gains in green. It opens from the pass in the Shop window before Roblox's purchase window; rain's opens from the weather picker the same way. At no merges:

| | Common | Uncommon | Rare | Epic | Legendary | Secret |
|---|---|---|---|---|---|---|
| Now | 59.9% | 25% | 10% | 4% | 1% | 0.1% |
| With Lucky Metal (or rain) | 39.9% | 37.5% | 15% | 6% | 1.5% | 0.15% |

**Restricted players** (`PolicyService:GetPolicyInfoForPlayerAsync(player).ArePaidRandomItemsRestricted`) see no Lucky Metal and can't buy rain. They can buy an **Ingot of a found metal** instead: an Epic or Legendary metal their book already has, 29 / 99 R$ (Allen). Merging still gives everyone earned luck.

Nothing else here changes odds or sells a random item.

## 5. The Auto Ore Roller

**The popup (Allen's design):** near your own ore roller, a small round button fades in on screen: the pack's **Auto Open** icon (two circling arrows) with the **Lock** icon (`rbxassetid://111896329341217`, already uploaded) on its corner. No text: Roblox's purchase window shows the name and price.

- **Where:** right side, above the jump button, clear of the hotbar and the left HUD; checked at phone size first (most players are on phones).
- **When:** within the lever's reach (about 12 studs) of your own roller, and not through a wall, like every prompt. Hidden until the tutorial is done (the check the Gem Shop uses).
- **Tap while locked:** `MarketplaceService:PromptGamePassPurchase`. After the purchase the lock pops off and the same button becomes the switch.
- **Tap when owned:** Auto on or off. On, the arrows turn slowly and the roller pulls by itself every ~5 s (the 3.6 s show plus a beat), the same pace as pulling by hand.
- **Keep rule:** it stops while a kept result lies on a stand, so it never replaces good ore; you collect, it carries on. A small chip on the button cycles **Rare+ → Epic+ → Legendary+ → Any** (Any pulls only onto empty stands). Rare+ to start, the tutorial's lesson. Saved.
- **Rolls only** (Allen): it never collects; you do.

**Server:** the lever's pull in `ForgeService` becomes one function the prompt and the auto loop both call, so the auto pull obeys the same rules (owner only, one roll at a time, tutorial rig). The loop runs only while the owner is in the server with the pass and Auto on. The client only sends on/off and the keep choice through one remote; the server checks the pass and the value.

## 6. Other developer products (bought again and again)

| Product | What it does | Start price | Notes |
|---|---|---|---|
| **Coin pack** | 5,000 / 20,000 coins (fixed since 2026-10-28; was 30 min or 2 h of income) | 49 / 149 R$ | Allen |
| **Gem pack** | 80 / 200 / 500 gems | 99 / 399 / 449 R$ | Allen. Gems also buy weather (§3). 200 is the decoy since 2026-11-02 (was 229) |
| **Ingot of a found metal** | Pick an Epic or Legendary metal your book already has | 29 / 99 R$ | Only for players where paid luck is restricted (§4) |

## 7. How every product works (the monetization skill's rules)

- **Prompt on the client, grant on the server.** `PromptProductPurchaseFinished` and the client's word are never proof.
- **Passes:** one server registry from pass id to benefit. `UserOwnsGamePassAsync` on join (a failed check means unknown, not "doesn't own": retry) and the server's `PromptGamePassPurchaseFinished` both go through the same grant, which sets a player attribute (`Pass_AutoRoller`, …) the services read.
- **Developer products:** one `ProcessReceipt`. Each purchase id is saved in the player's save together with what it granted, so a repeat receipt grants nothing. `NotProcessedYet` when the player is gone, the save isn't loaded, the product is unknown or the save fails; Roblox retries.
- **Weather for gems** is spent and started on the server, like a Gem Shop upgrade; the client only asks.
- **Prices come from Roblox at runtime** (`GetProductInfoAsync`), never typed into the UI. Managed Pricing (regional prices, and price tests of about three weeks that recommend the best prices) is on by default only for items made in Creator Hub; the ones made through Open Cloud have it off (§11).
- **Where offers appear:** where the player already is (the roller's popup, the Shop window, the weather picker); never during the tutorial, a weather or an offer's countdown (2026-10-31: since Fixes2 one of the four weathers is always on, so "a weather" can only mean a bought one; Claude's reading, for Allen to confirm); an unaffordable pad or gem upgrade still gets its "Not enough coins" notice or shake, and **since 2026-10-28 also offers the smallest coin or gem pack that covers the gap** (Allen: "when buying an upgrade they don't have enough for, we should popup a currency purchase for robux with the small amount needed to complete the purchase"; supersedes the review's no-prompt rule). Only after the tutorial and only while that pack is on sale.
- **Checks before players:** Studio test purchases of each, a repeated receipt, a player leaving mid-purchase, a failed save; then the economy logged with AnalyticsService.

Code when built: `Shared/Store` (ids and what each gives, read by both sides), `ServerScriptService.StoreService` (registry, receipts, PolicyService), a store page in `MenuGui.ShopWindow` (today "Coming soon"), the popup in its own ScreenGui made in Studio, and a receipts list in `SmithyCore`'s save.

## 8. Considered and left out

- **Dropped in the walkthrough:** 2× Coins (50% More Coins instead), 2× Coins for 30 min (coin packs cover it), Customer Rush (sunshine), Lucky Hour (rain), 2× Luck (Lucky Metal), the Etch Pack and the Starter Pack's etch (no buyers-only etches).
- **Anvil 3 early / a fourth crafter:** sells a stage of the spine, and Allen capped active crafters at three.
- **Auto Cashier / auto till:** the Cashier is a crew hire now; one system per effect.
- **Instant heat:** competes with the Faster Heating upgrades.
- **Finish the cart trip now:** trips are 1:10–2:30, too short to pay to skip.
- **2× Gems:** gem packs cover buying gems.

## 9. Robux without a product

- **Private servers:** switch on in the experience settings (free helps friends play together; a monthly price earns Robux). Allen's call.
- **Rewarded video:** a free player watches an ad for a reward (a few gems, a short sunny spell). Open platform-wide; Roblox plans a Studio plug-in in Q4 2026. Check age and region rules before building.
- **Premium Payouts** come from Premium players' time in the game, no code; **subscriptions** only once there's something monthly to give.
  - **Correction (2026-10-31, the monetization brainstorm):** Roblox replaced Premium Payouts with **Creator Rewards** on 2025-07-24; see [[Design/Monetization Ideas — 2026-10-31]] for what pays now (and Roblox Plus).

## 10. Order and who does what

1. **Done 2026-10-27:** Claude created the passes and products through Open Cloud, all off sale (§11). Each goes on sale when its feature is built; the experience goes public at release.
2. **Claude:** `StoreService`, the receipts list and the store page with live prices.
3. **Claude:** the Auto Ore Roller: popup, switch, keep chip, auto loop.
4. **Claude:** the Starter Pack, 50% More Coins, VIP and Swift Boots.
5. **Claude:** Lucky Metal with the odds panel, and the found-metal ingot for restricted players.
6. **Claude:** weather: bought Sunshine on top of the free one, then snow (the mail clock exists), rain (the odds panel) and the rainbow (VIP buyers exist); then weather for gems, coin packs and gem packs.

## 11. On Roblox (created 2026-10-27)

Universe **10771581195** ("create swords": private, Allen's account, root place 134592579197772). The `ROBLOX_UNIVERSE_ID` environment variable points at another game (Build Across! [GRAND CANYON]), so scripts pass this id. Created through Open Cloud at the prices above, with no images and **all off sale** at first. **The six passes went on sale on 2026-10-27** while the game is private (Allen: "Put all six passes on sale while the game is private, so the Shop shows prices and I can test buying."); the developer products stay off sale until built. Roblox then quoted Allen's account about 10% less than the set prices (135, 180, 90 and 270 R$) with no regional or managed pricing on the passes, so the difference is on the account's side; the Shop shows each player what Roblox quotes them. Managed pricing and regional prices are off (the API's default).

| Game pass | Id | Price |
|---|---|---|
| Auto Ore Roller | 2057783160 | 149 R$ |
| 50% More Coins | 2058251193 | 199 R$ |
| Lucky Metal | 2058881145 | 149 R$ |
| VIP | 2057315118 | 299 R$ |
| Swift Boots | 2057291128 | 99 R$ |
| Starter Pack (off sale since 2026-11-01: now the developer product below) | 2057171214 | 99 R$ |
| Auto Anvil (2026-10-31) | 2058261392 | 49 R$ |
| Auto Etch (2026-11-01) | 2064189929 | 49 R$ |
| Automation Pack (2026-11-01) | 2064634324 | 179 R$ |

**Auto Anvil** (2026-10-31, Allen: "auto-anvil clicker that can be super cheap?"): created through Open Cloud on sale (the game is private), description "Your anvil strikes by itself. Switch it on at the anvil and watch the blade take shape. You can still forge by hand any time." `Shared/Store.PASSES.AutoAnvil`. Price Claude's ("super cheap": half the cheapest pass, Swift Boots). It's comfort, not speed: strikes land at the player's own Faster Strikes pace. [[Sessions/2026-10-31#Auto Anvil]]

| Developer product | Id | Price |
|---|---|---|
| Starter Pack (2026-11-01, one-time) | 3727025192 | 99 R$ |
| Sunshine | 3723120522 | 79 R$ |
| Rainbow | 3723120527 | 79 R$ |
| Rain | 3723120529 | 79 R$ |
| Snow | 3723120534 | 79 R$ |
| 5,000 Coins (was Coin Pack (30 min)) | 3723120538 | 49 R$ |
| 20,000 Coins (was Coin Pack (2 h)) | 3723120543 | 149 R$ |
| 100,000 Coins (2026-10-28) | 3723420023 | 449 R$ |
| 300,000 Coins (2026-10-28) | 3723420024 | 999 R$ |
| 800 Coins (2026-10-29) | 3723663374 | 9 R$ |
| 1,800 Coins (2026-10-29) | 3723663378 | 19 R$ |
| 7 Gems (2026-10-29) | 3723663391 | 9 R$ |
| 15 Gems (2026-10-29) | 3723663397 | 19 R$ |
| 80 Gems | 3723120545 | 99 R$ |
| 200 Gems | 3723120547 | 399 R$ (decoy, 2026-11-02, Allen: "I want it"; was 229) |
| 500 Gems | 3723120548 | 449 R$ |
| Epic Ingot | 3723120551 | 29 R$ |
| Legendary Ingot | 3723120555 | 99 R$ |

- **Lucky Metal's and Rain's descriptions carry the odds** at no merges, since a pass can also be bought from the experience's Store tab.
- **On sale when built:** `PATCH https://apis.roblox.com/game-passes/v1/universes/10771581195/game-passes/{id}` or `https://apis.roblox.com/developer-products/v2/universes/10771581195/developer-products/{id}` with the form field `isForSale=true`. The API key reads and writes both. Whether Studio's test purchases need a pass on sale is unchecked.

## 12. Built (2026-10-27, not played)

Allen: "after this, work on the actual features the passes give". What each pass does is in the game ([[Development/Code Map#Robux passes (2026-10-27)]]); they're bought from the Shop page or the Auto Ore Roller's button (§5).

- **VIP's gold name tag** is a gold [VIP] before the name in chat.
- **The coin passes multiply** (×1.65 with both) and pay when the coins land: the offer card still shows the customer's offer; the Cashier's till holds the boosted coins, so its sign shows them.
- **Lucky Metal adds +0.5** to the merges' luck: one merge higher at any count.
- **Auto starts off;** its switch and keep chip are saved like the Settings switches.
- **In Studio** nobody owns a pass: tick them on `StoreService`'s attributes to try them; a test purchase grants one for the session.
- **The Shop page** (Allen: "Build the Shop page next: the other passes with live prices, the Starter Pack's dot and Lucky Ore's odds panel"; [[Development/Code Map#Shop page (2026-10-27)]]): a scrolling list of the six passes, carded like the Gem Shop, each price from Roblox ("—" while a pass is off sale) and "Owned" once yours. The Starter Pack is first until bought; after the tutorial the Shop button's amber dot shows until you open the Shop, each session.
- **Lucky Metal's Buy opens its odds panel** (§4): every rarity now and with it, for your own luck; the purchase is made from there. Where paid random items are restricted (or `PolicyService` can't say) its card is hidden; the found-metal ingot that replaces it there comes with the developer products.
- **Not built:** the developer products, images on Roblox.
- **2026-10-28:** gem and coin packs built (`StoreService.ProcessReceipt`, saved receipts; coin packs = minutes of income over the last 15 min, floor 50/min), **on sale since later that day** (Allen: "wire in the products"), coin packs fixed at 5,000 / 20,000; Allen confirmed the test purchases work (2026-10-28). [[Sessions/2026-10-28#Gem and coin packs sell: ProcessReceipt; Buy buttons shaded]]

## Open

- **"VIP" twice:** the VIP pass and the rainbow's VIP customers share a name; one may want another.
- **Numbers to tune:** how often free weather comes (the review suggested every 10–15 minutes), the rainbow's boost and the gem prices.
- **Lucky Metal on the Store tab:** a pass can also be bought on the experience's page, where the game can't check `PolicyService`, and Roblox's paid-random-items page doesn't cover that case. Before the game goes public: keep the pass, or sell Lucky Metal as a one-time in-game product (the pass then goes off sale). It's on sale now only because the game is private.
- **Images:** none of the 17 has one yet.

## Allen's answers (2026-10-27)

1. **Luck:** "It should be an increased luck pass, but doesn't have to be necessarily 2x. I notice in the clay game they have the odds available", with the Lucky Clay screenshot. Then ×1.5, one merge higher: **Lucky Metal**.
2. **Starter Pack:** "keep the gems, the ingots, no buyers-only etch".
3. **Coins:** "50% more coins, coin packs, gem packs, control the weather ( control the temporary server boost), vip pass gives +10% on every sale". Then the four weathers (§3), and gems buy weather too.
4. **Auto Ore Roller:** roll only, with the chip (Rare+ to start).
5. **Restricted regions:** an ingot of a found metal.

## Sources

- Paid random items, luck boosts counted, odds as percentages: https://create.roblox.com/docs/production/monetization/paid-random-items · Korea's rules made disclosure worldwide: https://www.techtimes.com/articles/319148/20260626/koreas-loot-box-rules-push-roblox-disclose-item-odds-worldwide.htm
- Tycoon pass prices (2× cash 150–399 R$, auto-collect 95–299, VIP ~499): https://www.sportskeeda.com/roblox-news/5-best-gamepasses-use-roblox-war-tycoon · https://www.rolimons.com/gamepass/7635163 · https://deltiasgaming.com/?p=400270 · https://rt3.fandom.com/wiki/Shop
- Developer products for consumables: https://www.creation.dev/learn/roblox-developer-products-guide
- Managed pricing, price tests, regional prices: https://create.roblox.com/docs/production/monetization/managed-pricing · https://create.roblox.com/docs/production/monetization/price-optimization · https://create.roblox.com/docs/production/monetization/regional-pricing
- Subscriptions: https://create.roblox.com/docs/production/monetization/subscriptions · Roblox Plus: https://www.businesswire.com/news/home/20260410099173/en/Roblox-Announces-Roblox-Plus-a-New-Subscription-Plan-Offering-Exclusive-Platform-Benefits
- Rewarded video: https://www.mediapost.com/publications/article/417959/roblox-plans-expanded-placement-options-for-rewar.html · https://www.emarketer.com/content/roblox-expands-rewarded-video-tools-creators-advertisers · https://ppc.land/magnite-secures-robloxs-151-million-daily-users-for-programmatic-video/
- Open Cloud game passes (`CreateGamePass`): https://create.roblox.com/docs/cloud-services/http-service

---

Related: [[Design/Game Design Document#15. Monetization (Robux)|GDD §15]] · [[Design/Economy Pass 2]] · [[Archive/Design/Progression and Economy Review — 2026-10-27]] · [[Archive/Design/Urgency Review]] · [[Design/Workshop Growth]] · [[Art/Icon Library]] · [[Sessions/2026-10-27#Monetization plan]] · [[Sessions/2026-10-27#Monetization walkthrough]]

**Auto Ore Roller stops (2026-10-28):** the pass's pill has a rarity chip (Uncommon+ … Legendary+, or off) and a Quests chip (stop on ores an open letter or order needs). [[Sessions/2026-10-28#Auto-Roll stop settings, at the top]]

## Starter Pack as a product, Auto Etch, Automation Pack (2026-11-01)

Allen: "Starterpack should be a dev product, not game pass. but obviously single purchase only" and "a pack that combines all the automation gamepasses"; he chose to add a new **Auto Etch** pass to the pack. Later the same night: "look into a decoy purchase in shop and a best value label" (the label is built; the decoy is a separate proposal). [[Sessions/2026-11-01#Starter Pack as a product, Auto Etch, Automation Pack]]

- **Starter Pack:** developer product **3727025192**, 99 R$, on sale (the game is private), the old pass's description ("10,000 coins and 100 gems, once."). The pass 2057171214 is off sale. §2 has how one purchase is kept.
- **Auto Etch:** pass **2064189929**, 49 R$ (as the Auto Anvil), on sale, "Your etches draw themselves. You can still hold to etch by hand any time." The etching table's hold-to-etch reads `Store.owns(player, "AutoEtch")` (built by another session).
- **Automation Pack:** pass **2064634324**, **179 R$**, on sale, "Auto Ore Roller, Auto Anvil and Auto Etch together, for less than the three apart." The three apart are 149 + 49 + 49 = 247 R$; 179 is about 28% off (Claude's price). `Store.owns` counts it as all three. The Shop shows it only while you own none of the three (Claude's default: with one owned, the pack would charge for it again), with a **Best Value** tag.
- **Best Value** also marks the coin pack and the gem pack that give the most per Robux at Roblox's live prices (today 300,000 Coins, ~300 coins per R$, and 500 Gems, ~1.11 gems per R$), worked out in the Shop, so it follows a price change.
- **Open:** whether the pack should still be offered (at a lower price) to someone who owns one or two of the three; a pack bought by someone who already owns one pays for that one twice, which the hidden card prevents only inside the game (the Store tab still sells it).

**2026-11-08:** managed pricing goes on for every pass and product (Allen); waiting on the one-time terms acceptance in Creator Hub. Beginner's luck stays out of Lucky Metal's odds (Allen: it isn't a paid boost).

## Swordsmith Tycoon copies (created 2026-11-08)

Sell Swords! will launch on Allen's group game Swordsmith Tycoon (formerly Build a Bridge / Build Across! [GRAND CANYON], universe **10769630190**), which already passed Roblox's 250 highly engaged players bar for under-16s. Every live pass and product was copied there through Open Cloud with the same name, description, price and icon, **all off sale**. The retired Starter Pack pass 2057171214 wasn't copied. Managed pricing is off on the copies. Since later on 2026-11-08 `Shared/Store` uses these ids (Allen: "cant you do this right now?"), so Studio's place has to be published to Swordsmith Tycoon for purchases to work.

| | Name | Sell Swords! id | Swordsmith Tycoon id | Price |
| --- | --- | --- | --- | --- |
| pass | Automation Pack | 2064634324 | **2076118417** | 179 R$ |
| pass | Auto Etch | 2064189929 | **2074450621** | 49 R$ |
| pass | Auto Anvil | 2058261392 | **2075458562** | 49 R$ |
| pass | Swift Boots | 2057291128 | **2074456550** | 99 R$ |
| pass | VIP | 2057315118 | **2074438497** | 299 R$ |
| pass | Lucky Metal | 2058881145 | **2075536519** (off sale since 2026-11-10; now product **3730271492**) | 149 R$ |
| pass | 50% More Coins | 2058251193 | **2074216539** | 199 R$ |
| pass | Auto Ore Roller | 2057783160 | **2075830643** | 149 R$ |
| product | Starter Pack | 3727025192 | **3729904181** | 99 R$ |
| product | 15 Gems | 3723663397 | **3729904188** | 19 R$ |
| product | 7 Gems | 3723663391 | **3729904194** | 9 R$ |
| product | 1,800 Coins | 3723663378 | **3729904201** | 19 R$ |
| product | 800 Coins | 3723663374 | **3729904208** | 9 R$ |
| product | 300,000 Coins | 3723420024 | **3729904220** | 999 R$ |
| product | 100,000 Coins | 3723420023 | **3729904234** | 449 R$ |
| product | Legendary Ingot | 3723120555 | **3729904292** | 99 R$ |
| product | Epic Ingot | 3723120551 | **3729904305** | 29 R$ |
| product | 500 Gems | 3723120548 | **3729904312** | 449 R$ |
| product | 200 Gems | 3723120547 | **3729904320** | 399 R$ |
| product | 80 Gems | 3723120545 | **3729904326** | 99 R$ |
| product | 20,000 Coins | 3723120543 | **3729904336** | 149 R$ |
| product | 5,000 Coins | 3723120538 | **3729904342** | 49 R$ |
| product | Snow | 3723120534 | **3729904352** | 79 R$ |
| product | Rain | 3723120529 | **3729904356** | 79 R$ |
| product | Rainbow | 3723120527 | **3729904366** | 79 R$ |
| product | Sunshine | 3723120522 | **3729904376** | 79 R$ |

- **The old bridge game's own items are still on sale:** 10 of its 22 passes (Auto Build, BuilderBot, 2x–100x Training) and its 85 products (Wheel Spins, Lucky Planks, Speed, Strength). **Off sale since 2026-11-08** (Allen: "Yes, retry it"): 9 passes and 65 products, read back with 0 left on sale. The list of what was on sale is in `Development/Build a Bridge on sale before 2026-11-08.json`. Passes can't be deleted.
- **On sale (2026-11-08, Allen: "Yes, put them on sale"):** the 8 passes and 13 products whose Sell Swords! originals are on sale. Weather (Sunshine, Rainbow, Rain, Snow) and the Epic and Legendary ingots stay off sale, as before. The game is private, so only the Shop's prices show. **Checked:** each of the 26 read back, all match the originals.
- **Checked:** all 26 copies read back by API: name, description, price, off sale and an icon each, 0 mismatches.

**Managed pricing on the copies (2026-11-08):** all 26 Swordsmith Tycoon copies have managed pricing on (Allen: "Yes, all 26"); readback 26 of 26, `enabledFeatures` ["RegionalPricing"], prices unchanged, still off sale. Allen's user account hasn't accepted the terms, so the Sell Swords! originals stay off; they never ship. [[Sessions/2026-11-08#Managed pricing: the group has it, the user account doesn't]]

**Bought weather built (2026-11-08):** Sunshine and Snow, from the Shop's WEATHER cards (79 R$ or 60 gems), one bought weather at a time, the buyer named on the banner and tip; the game reads the Swordsmith Tycoon copies (3729904376, 3729904352), off sale for now, so Robux buys wait for those to go on sale; the Sell Swords! originals are on sale but unused. Rainbow and Rain (odds panel, server policy check) not built. [[Sessions/2026-11-08#Bought weather: Sunshine and Snow]]
- **2026-11-08 (Allen: "Yes, both"):** the Swordsmith Tycoon Sunshine (3729904376) and Snow (3729904352) copies are on sale (readback), so the game's Robux weather buys work; the other copies stay off sale. [[Sessions/2026-11-08#Bought weather: Sunshine and Snow]]

## Coin packs after the 2026-11-09 repricing

Late prices went up x1.3 (every price of 10,000+, with walk-ins 1.5x). The coin packs are fixed amounts, so a 100,000 or 300,000 pack buys about 23% less of the late catalogue than before. Income is higher too, so how many minutes of income a pack is worth barely moves. No pack change proposed. [[Sessions/2026-11-09#Walk-ins 1.5x and 10,000+ prices x1.3, built]]

## Showcase families and the passes (2026-11-09)

Showcase Stands now boost one stat each, by the sword's metal (Customers, VIP, Coins, Luck, Swift, Mail). Every cap stays well under its pass, so each pass is still the bigger step. In the sim, efficient players over 10 h: Coins stands +15% against 50% More Coins +107%; VIP stands +14% against the VIP pass +40%; Swift stands +3% against Swift Boots +16%; Luck stands +2% against Lucky Metal +3%.

**Odds:** the stands' luck (`StandLuck`, up to +0.15) counts in every odds view: the Ore Chances sign, the Shop's Lucky Metal panel and the merge window. Each shows the odds a roll really uses, with and without the pass. [[Sessions/2026-11-09#Showcase families built: six stats by metal]]

## Everything Bundle (2026-11-09)

Allen: "a pass/product that packs all of the gamepasses together in one bundle and offers a discount. it should show the total price and then crossed it out with the new price." [[Sessions/2026-11-09#Everything Bundle; the Shop wider, three cards a row]]

| | Name | Sell Swords! id | Swordsmith Tycoon id | Price |
| --- | --- | --- | --- | --- |
| pass | Everything Bundle | 2076052826 | **2075914814** | 599 R$ |

- **What it holds:** all seven passes (993 R$ apart; 599 is about 40% off, Claude's price). `Store.owns` counts it as each. Created through Open Cloud on sale in both universes (the game is private); managed pricing on for the Swordsmith Tycoon copy (read back `RegionalPricing`), off on the Sell Swords! one (the user account can't). Icon: the pack's Crown.
- **Odds:** it includes Lucky Metal, so its description carries the odds and the Shop's Buy opens the odds panel first; where paid random items are restricted its card is hidden. The Store-tab question for Lucky Metal (Open) applies to the bundle too.
- **Open:** like the Automation Pack it shows only while you own none of its passes; whether to offer a cheaper bundle to someone who owns some is Allen's call.

## 50% More Gems (2026-11-09)

Allen: "I also want a 1.5x gem pack or 50% whatever u call it". [[Sessions/2026-11-09#50% More Gems pass]]

| | Name | Sell Swords! id | Swordsmith Tycoon id | Price |
| --- | --- | --- | --- | --- |
| pass | 50% More Gems | 2074816877 | **2075140783** | 199 R$ |

- Gems from letters, mail orders and cart deliveries ×1.5, rounded half up; not the daily reward, the Starter Pack or gem packs. On sale in both universes (private game); managed pricing on for the Swordsmith Tycoon copy.
- **Everything Bundle:** now eight passes (1,192 R$ apart) at 599 R$, about 50% off; its description updated in both universes.

## Golden Hour (2026-11-09)

Allen: "lets do golden hour" ([[Design/Monetization Ideas — 2026-11-09]]). A bought-only weather: Sunshine, Snow and Rainbow's bonuses at once (2x customers, 2x mail, 3x VIPs), no luck, so not a paid random item. 149 R$ or 120 gems (Claude's prices).

| Kind | Item | Swordsmith id | Price |
|---|---|---|---|
| product | Golden Hour | **3730123757** | 149 R$ (off sale like the other weathers; managed pricing on) |

Also made by mistake in the old Sell Swords! universe: 3730123763, off sale, unused (Allen: new items in Swordsmith only). [[Sessions/2026-11-09#Golden Hour (in progress) and the brainstorm's answers]]

## Bigger Bag (2026-11-10)

Allen: the bag holds 30, a pass doubles it, "49 robux". Created through Open Cloud in Swordsmith Tycoon only.

| Kind | Item | Swordsmith id | Price |
|---|---|---|---|
| pass | Bigger Bag | **2075410974** | 49 R$ (on sale, regional and managed pricing on) |

Description: "Carry twice as much: your bag holds 60 swords and ingots instead of 30." No icon yet. In the Everything Bundle (Allen: "Add it to the bundle"): nine passes at 599 R$, 1,241 R$ apart (about 52% off); the bundle's description names it. [[Sessions/2026-11-10#Bag cap and the Bigger Bag pass]]

## Lucky Metal as a one-time product (2026-11-10)

Allen: "just do one-time product then makes no difference" (the release gates' blocker 3). **Developer product 3730271492**, "Lucky Metal", 149 R$, managed pricing on (readback: RegionalPricing), icon copied from the pass. The pass **2075536519 is off sale** (readback). The game keeps the key `LuckyOre`: `Store.PRODUCTS.LuckyOre`, `Store.ONCE` (one-time, as the Starter Pack), `SmithData.luckyGranted` shown as `Pass_LuckyOre`, so every `Store.owns(player, "LuckyOre")` works as before. `StoreService.ProcessReceipt` answers NotProcessedYet (no grant) where `ArePaidRandomItemsRestricted` is true or `PolicyService` can't say; the client still hides the card and the board's Buy there.

- **Everything Bundle:** Lucky Metal left it (a pass sold on the Store tab can't hold paid luck). 8 passes, still 599 R$; its Roblox description now lists the eight with no odds (readback). Its Shop card's Lucky Metal tile is in `ServerStorage.Legacy`.
- **Not verified:** whether Roblox refunds a developer product receipt that is never granted (a restricted player who forces a prompt). Only a hand-made prompt gets there.
- **The found-metal ingot for restricted players** stays unbuilt; they simply see no Lucky Metal.

## Gifts (2026-11-10)

Allen: "add a gift button so players can gift their friends a gamepass or currency or whatever it is from the shop". [[Sessions/2026-11-10#Gifts from the Shop]]

A pass can't be bought for another player, so every giftable item has its own developer product, "Gift: <item>", at the item's price. Created through Open Cloud in Swordsmith Tycoon only (universe 10769630190), on sale, managed and regional pricing on, icon copied from the item (readback 21 of 21). `Shared/Store.GIFTS` maps item key → gift product.

| Item key | Gift product | Price |
|---|---|---|
| AutoRoller | 3730309427 | 149 R$ |
| AutoAnvil | 3730309438 | 49 R$ |
| MoreCoins | 3730309447 | 199 R$ |
| MoreGems | 3730309455 | 199 R$ |
| VIP | 3730309464 | 299 R$ |
| SwiftBoots | 3730309469 | 99 R$ |
| BiggerBag | 3730309473 | 49 R$ |
| AutoEtch | 3730309477 | 49 R$ |
| AutomationPack | 3730309485 | 179 R$ |
| EverythingBundle | 3730309487 | 599 R$ |
| Gems7 / 15 / 80 / 200 / 500 | 3730309496 / 3730309502 / 3730309505 / 3730309506 / 3730309511 | 9 / 19 / 99 / 399 / 449 R$ |
| Coins800 / 1800 / 5000 / 20000 | 3730309517 / 3730309521 / 3730309530 / 3730309537 | 9 / 19 / 49 / 149 R$ |
| Coins100000 / 300000 | 3730309547 / 3730309552 | 449 / 999 R$ |

- **Rules (§7 holds):** the client only asks (`Remotes.Gift`: key, UserId of a player in the server); the server checks the key, the friend (in the server, loaded, not the buyer, doesn't own the pass or any pass in the bundle), a 1 s cooldown, notes `giftTo[key]` in the buyer's save and prompts the product itself. `ProcessReceipt` gives it, saving the friend first; a friend who left gets it from the inbox DataStore (`Swords_Gifts_v1`, key `u<UserId>`) on their next load. Both saves record the purchase id, so a retry never gives twice; any failed save or DataStore call is `NotProcessedYet`.
- **Not giftable:** the Starter Pack and Lucky Metal (one-time; Lucky Metal is paid luck, checked against the buyer's own policy) and weather (for the whole server already).
- **Gifted passes** are a save flag (`SmithData.gifted`), not Roblox ownership: they work in this game only and don't show on the friend's Roblox inventory. A friend who later buys the same pass on Roblox has paid twice (the Shop shows it as Owned, so only the experience's Store tab sells it to them).
- **Prices:** the gift product's price is set on its own: a price change to an item must be made to its gift too.

## Price changes (2026-11-11)

Allen: "Yes, apply them" ([[Design/Monetization Pricing Pass — 2026-11-11]]). Swordsmith Tycoon (10769630190) only; the older price tables above keep their dates.

| Item | Id | Was | Now |
|---|---|---|---|
| 50% More Coins (pass) | 2074216539 | 199 | **249 R$** |
| Gift: 50% More Coins | 3730309447 | 199 | **249 R$** |
| VIP (pass) | 2074438497 | 299 | **199 R$** |
| Gift: VIP | 3730309464 | 299 | **199 R$** |
| 50% More Gems (pass) | 2075140783 | 199 | **149 R$** |
| Gift: 50% More Gems | 3730309455 | 199 | **149 R$** |
| Sunshine | 3729904376 | 79 | **39 R$** (60 gems unchanged) |
| Snow | 3729904352 | 79 | **39 R$** (60 gems unchanged) |
| Golden Hour | 3730123757 | 149 | **99 R$** (120 gems unchanged; still off sale) |

- **Checked:** each of the 9 read back from Roblox at its new price, managed pricing still on.
- **Everything Bundle:** still 599 R$; its eight passes are now 1,042 R$ apart (about 43% off). The Shop works that total out from live prices (`MenuController`).
- **Not changed:** `Shared/Store` (its comments still name the old prices; the Shop reads prices from Roblox), the Sell Swords! originals, the Rainbow and Rain products (off sale, 79 R$).

## First buy of each gem pack gives double (2026-11-11)

Allen: "Yes, build it". Built, not played. [[Sessions/2026-11-11#First buy of each gem pack gives double]]

- The first time a save buys each gem pack it gets twice the gems (`Store.FIRST_BUY` 2): 7 → 14, 15 → 30, 80 → 160, 200 → 400, 500 → 1,000. Each pack once, so at most 802 bonus gems for 975 R$.
- The gem card reads "500 +500" (the +500 green) until that pack is bought. No new product; the Roblox names and descriptions still say the plain amount.
- Not doubled: gifts (they do not use the double up either), coin packs, the Starter Pack.
- Best Value and the Starter Pack's "× VALUE" tag still use the plain amounts.

## Daily Deal (2026-11-11)

Allen: "Yes, Daily Deal". Built, not played. [[Sessions/2026-11-11#Daily Deal]]

| Kind | Item | Swordsmith id | Price |
|---|---|---|---|
| product | Daily Deal | **3730335103** | 29 R$ (on sale, managed and regional pricing on; icon: the 80 Gems art, asset 122817339628061) |

- **40 gems, once a UTC day** per player: 1.38 gems a Robux against 1.11 for the 500 pack and 0.78 for 7 Gems. Description on Roblox: "40 gems, once a day."
- A real limit, no countdown offer: once bought the card shows the time until the next UTC day in place of Buy.
- The limit is kept by the client, as the Starter Pack's: a second receipt the same day (two servers prompting at once, or a hand-made prompt) is paid for, so it is granted.
- Not a gem pack: no first-buy double, no gift, never the short-of-gems offer, not in Best Value.

## Starter Pack: 29 R$, 100 gems and 5,000 coins (2026-11-11)

Allen: "yes lets do 29 robux". Supersedes §2's 99 R$ and 250 gems. [[Sessions/2026-11-11#Starter Pack 29 R$ with 100 gems; the Daily Deal tag shines]]

- Product **3729904181**: 29 R$ (readback), description "100 gems and 5,000 coins, once.", on sale, managed pricing on.
- 100 gems + 5,000 coins is about 106 R$ at the best packs' rates (90 + 17), so the card's tag reads "3× VALUE"; 3.4 gems a Robux against the Daily Deal's 1.38.
- **Until the place is published the live game still gives 250 gems** for the new price (`STARTER_GEMS` changed in Studio only).

## Lucky Rolls (2026-11-11)

Allen: "build it". Built, not played. [[Sessions/2026-11-11#Lucky Rolls]]

| Kind | Item | Swordsmith id | Price |
|---|---|---|---|
| product | 10 Lucky Rolls | **3730342441** | 9 R$ |
| product | 25 Lucky Rolls | **3730342445** | 19 R$ |
| product | 50 Lucky Rolls | **3730342453** | 29 R$ |

- All three on sale, managed and regional pricing on, Lucky Metal's icon, the odds at no merges in the description (readback).
- **What one does:** your next pull is one merge luckier (+0.5, as Lucky Metal) on every stand; used when the pull ends. With 6 stands and no merges a pull has a Legendary 5.9% of the time, 8.7% with a Lucky Roll, 11.4% with Lucky Metal too (1 - (1 - p)^6 for p = 1%, 1.5%, 2%; the 2% follows the odds table's pattern and was not run).
- **Paid random item** (Roblox counts luck boosts): the Shop's odds panel opens before the purchase with the buyer's own odds now and with a Lucky Roll; the Ore Chances sign shows the boosted odds while rolls are held; restricted players see no card and a forced receipt is never granted. Roblox's policy page (read 2026-11-11) lists hiding the item as an accepted treatment and names no age rule beyond `ArePaidRandomItemsRestricted`; the experience questionnaire was not looked at.
- Not giftable, no gem price, no first-buy double.
- **Until the place is published** the products are on sale but nothing in the live game sells them.

**Lucky Rolls sizes (2026-11-11, later):** 5 / 15 / 30 pulls for 9 / 19 / 29 R$ (1.80 / 1.27 / 0.97 R$ a pull), in place of 10 / 25 / 50. The products keep their ids and are renamed "5 / 15 / 30 Lucky Rolls" with matching descriptions (readback 3 of 3). Five large packs (145 R$) last about 12 minutes of pulling, against Lucky Metal's 149 R$ for good. [[Sessions/2026-11-11#Lucky Rolls: 5, 15 and 30]]

## VIP's description; Auto Anvil 129 R$ (2026-11-11)

[[Sessions/2026-11-11#VIP's description; Auto Anvil 129 R$]]

- **VIP** (pass 2074438497, gift 3730309464): description now "VIP customers come twice as often, +10% coins on every sword you sell, and a gold name tag." (readback). Price unchanged, 199 R$.
- **Auto Anvil** (pass 2075458562, gift 3730309438): **129 R$** (was 49; readback, both on sale).
- **Bundles, unchanged prices:** the Automation Pack's three are 327 R$ apart (149 + 129 + 49), so 179 R$ is about 45% off; the Everything Bundle's eight are 1,122 R$ apart, so 599 R$ is about 47% off. The Shop works the crossed-out total out live.
- **Open:** whether doubling the VIP customer chance counts as a paid random item under Roblox's rule (a boost to a random outcome); not checked. If it does, VIP needs its odds shown before purchase, as Lucky Metal.

## Auto Polish; an image on every pass (2026-11-11)

Allen asked for both. Built, not played. [[Sessions/2026-11-11#Auto Polish; an image on every pass]]

| Kind | Item | Swordsmith id | Price |
|---|---|---|---|
| pass | Auto Polish | **2078408322** | 49 R$ (on sale, managed and regional pricing on, the pack's Stars icon) |
| product | Gift: Auto Polish | **3730343868** | 49 R$ |

- Description: "Your swords polish themselves at the Polishing Station while you watch. You can still polish by hand any time."
- **Automation Pack** (179 R$): now four passes, 376 R$ apart (149 + 129 + 49 + 49), about 52% off. Description: "Auto Ore Roller, Auto Anvil, Auto Etch and Auto Polish together, for less than the four apart." (pass and gift, readback).
- **Everything Bundle** (599 R$): now nine passes, 1,171 R$ apart, about 49% off. Description names all nine (pass and gift, readback).
- **Until the place is published** the bundles' descriptions promise Auto Polish but the live game doesn't have it.
- **Images:** Bigger Bag's pass had the universe's placeholder (133448903949274, shared with the 13 off-sale bridge passes); it now has its own (98404767996184, from the Shop card's icon). The other 10 passes on sale and all 41 products on sale each had their own image already (readback).

**Correction, pass images (2026-11-11, later):** Auto Etch (2074450621) and the Automation Pack (2076118417) showed Roblox's default grey ticket; each had its own `iconAssetId`, so comparing ids did not catch it (Allen did: "the automation and etch passes dont have icons"). Auto Etch now has its Shop pencil; the Automation Pack a new image, its four passes' icons two by two (900 x 900, built from the icons' own thumbnails). Their gift copies (3730309477, 3730309485) got the same. Checked by downloading what Roblox serves: no pass or product on sale shows the ticket; the Automation Pack pass's thumbnail was still Pending. Shared images that are meant (one gem, one coin, one clover) are real art. [[Sessions/2026-11-11#Auto Etch and Automation Pack icons]]


**Lucky Rolls on the board (2026-11-11):** Lucky Metal's board by the ore stands sells the three packs beside its "Forever" button; the odds are on the board itself, so the purchase is made from there, as Lucky Metal's. Restricted players see no buttons (the board is Hidden for them). [[Sessions/2026-11-11#Lucky Rolls on Lucky Metal's board]]

**Visibility review (2026-11-11):** how players find the Shop and the offers, not prices: [[Design/Monetization Visibility Review — 2026-11-11]] (proposals, waiting for Allen).

## 2x Coins (2026-11-11)

Allen: "would 2x coins be a better look than saying 50% more coins? ... 2x is more catchy", then "lets set it to 2x" (offered: rename to 1.5x, or make it a real 2x at a higher price). The pass now doubles coins; calling a 1.5x pass "2x" would have been a false description.

| | Id | Was | Now |
|---|---|---|---|
| pass | 2074216539 | 50% More Coins, 249 R$ | **2x Coins, 349 R$** (Claude's price: 2x cash is 299–399 elsewhere) |
| gift | 3730309447 | Gift: 50% More Coins, 249 R$ | **Gift: 2x Coins, 349 R$** |

- Description (pass; the gift adds "A gift for another player: "): "Every coin you earn is doubled: shop sales, cart deliveries and mail orders." The Everything Bundle's pass and gift descriptions name "2x Coins". Readback 4 of 4: on sale, managed pricing on.
- **Game:** `Shared/Store.MORE_COINS` 2 (was 1.5); the Shop's pass card and the bundle tile read "2x Coins" / "2x coins on every sale". The key stays `MoreCoins`, so owners keep it with no save change.
- **Pace (sim):** Efficient player, 30 seeds, 10 h, from the 2026-11-11 balance export: last sword (Seraph) free 7:20, 1.5x 5:25, 2x 4:12; coins at 10 h +102% at 1.5x, +209% at 2x. Casual: free doesn't reach the Seraph in 10 h, 1.5x 8:01, 2x 6:49. The paying player reaches the end of the sword chain, and its post-Seraph gap, about 1 h 10 sooner than at 1.5x.
- **Bundles:** the Everything Bundle stays 599 R$; its nine passes are now 1,271 R$ apart (about 53% off; the Shop sums the live prices).
- Not changed: 50% More Gems (still 1.5x, still its name). [[Sessions/2026-11-11#2x Coins]]

## 2x Gems (2026-11-11)

Allen: "Yes, 2x Gems". Gems from letters, mail orders and carts are doubled (`Store.MORE_GEMS` 2, was 1.5); not the daily gift or bought packs, as before.

| | Id | Was | Now |
|---|---|---|---|
| pass | 2075140783 | 50% More Gems, 149 R$ | **2x Gems, 199 R$** (Claude's price: twice the effect, back to its 2026-11-09 price) |
| gift | 3730309455 | Gift: 50% More Gems, 149 R$ | **Gift: 2x Gems, 199 R$** |

- Description: "Every gem you earn from letters, mail orders and cart deliveries is doubled." The Everything Bundle's pass and gift descriptions name "2x Coins, 2x Gems". Readback 4 of 4, on sale, managed pricing on.
- Shop card and bundle tile: "2x Gems" / "2x gems from orders". Everything Bundle: 599 R$, its nine passes 1,321 R$ apart (about 55% off). [[Sessions/2026-11-11#2x Gems]]

**Lucky Rolls in the Shop (2026-11-12):** one card with ×5 / ×15 / ×30 chips, a Buy for the picked pack and an Odds button, in place of three cards. [[Sessions/2026-11-12#Lucky Rolls: one Shop card with size chips]]

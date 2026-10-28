---
title: Monetization Plan
status: decided 2026-10-27; the six passes and the Shop page built, not played; passes on sale (game private), products off sale
type: design
updated: 2026-10-27
tags: [monetization, robux, game-pass, developer-product, ore, weather, create-swords]
---

# Monetization Plan

Allen, 2026-10-27: "research all the potential developer products we can have for purchase with robux. gamepasses, 1 starter pack. gamepasses that ease the experience, or provide better bonuses, luck, etc. 1 of them in my mind is an auto ore roller that shows up on your screen for purchase whenever youre near the ore roller itself. its would be a small popup with a lock icon to show you can buy it."

Builds on [[Design/Game Design Document#15. Monetization (Robux)|GDD §15]] (its rule stays: **Robux speeds things up or adds style, but anyone can earn everything by playing**) and [[Design/Progression and Economy Review — 2026-10-27#9. Game passes and developer products|the review's §9]]. Pace numbers are `Development/economy_model.py` after [[Design/Economy Pass 2]] and its customer rate: a casual player who keeps Rare+ ore.

**Decided with Allen on 2026-10-27** in a walkthrough of the first draft's questions ([[Sessions/2026-10-27#Monetization walkthrough]]); his answers are at the end. **Nothing here is built;** prices are starting points for Roblox's price test (§7). The passes and products exist on Roblox (ids in §11); the passes are on sale while the game is private.

## The short version

- **Passes:** the Auto Ore Roller (Allen's popup, §5), 50% More Coins, Lucky Ore (luck one merge higher), VIP (+10% on every sale) and Swift Boots.
- **One Starter Pack:** 100 gems and a Gold ingot for 99 R$.
- **Weather for the whole server, about 5 minutes, bought with Robux or gems** (Allen's design, §3): sunshine brings customers, a rainbow VIP customers, rain luck, snow mail.
- **Coin packs and gem packs**, and an ingot of a found metal for players where paid luck is restricted.
- **Pace:** 50% More Coins and VIP together bring Rin from 13 h 17 to 8 h 32. The Auto Ore Roller is comfort (12 h 30); Lucky Ore is for collectors (12 h 58).

## 1. Game passes (bought once, kept)

| Pass | What it does | Start price | Rin | Notes |
|---|---|---|---|---|
| **Auto Ore Roller** | Pulls the lever for you until a kept rarity lands (§5) | 149 R$ | 13 h 17 → 12 h 30 | Allen's idea. Not a paid random item: the rolls stay free, it buys the pulling |
| **50% More Coins** | Every coin you earn ×1.5: sales, carts, orders | 199 R$ | → 9 h 18 | Allen chose +50% over the draft's 2× (which made it 7 h 15) |
| **Lucky Ore** | Luck one merge higher (+0.5), on top of your merges | 149 R$ | → 12 h 58 | **Paid random item:** the odds panel before buying (§4). Close to Create Pottery!'s Lucky Clay (about ×1.7 on Rare+) |
| **VIP** | +10% on every sale; a gold name tag | 299 R$ | → 12 h 12 | Allen: "+10% on every sale", in place of the draft's golden rack |
| **Swift Boots** | Walk 25% faster (WalkSpeed 16 → 20) | 99 R$ | not modelled | Kept by default; plots are walk-heavy |

| Time to | Katana | Longsword | Crafter | Falchion | Gladius | Zanbatō | Rin |
|---|---|---|---|---|---|---|---|
| No passes | 21 min | 1 h 20 | 2 h 05 | 3 h 12 | 5 h 45 | 8 h 46 | 13 h 17 |
| Auto Ore Roller | 18 min | 1 h 13 | 1 h 55 | 3 h 03 | 5 h 24 | 8 h 16 | 12 h 30 |
| Lucky Ore | 20 min | 1 h 17 | 2 h 01 | 3 h 08 | 5 h 37 | 8 h 34 | 12 h 58 |
| VIP | 19 min | 1 h 14 | 1 h 55 | 3 h 00 | 5 h 19 | 8 h 04 | 12 h 12 |
| 50% More Coins | 16 min | 58 min | 1 h 27 | 2 h 16 | 4 h 06 | 6 h 09 | 9 h 18 |
| 50% More Coins + VIP | 16 min | 54 min | 1 h 20 | 2 h 05 | 3 h 46 | 5 h 41 | 8 h 32 |
| All four | 13 min | 48 min | 1 h 13 | 1 h 57 | 3 h 32 | 5 h 21 | 8 h 02 |

Method: `economy_model.run` for that player with the live customer rate; 50% More Coins = every price ÷ 1.5, VIP = ÷ 1.1 (counted on all income), Lucky Ore = luck 1.5 in `picked`, Auto Ore Roller = 1 s of pulling a sword. Weather isn't modelled. The model lets the Auto Roller pull instantly; in the game it pulls every ~5 s, which keeps up while you craft (a Rare+ result takes ~33 s of pulling with one ore slot, ~6 s with six).

## 2. The Starter Pack (one)

- **Contents:** 100 gems (exactly Better Advertising II + More Clients I) and a **Gold ingot** (Epic ×5, a fixed metal, so not a paid random item). The ingot doesn't fill Gold's book page; that still has to be rolled. No etch (Allen).
- **Price:** 99 R$, the best value in the shop (gem packs give fewer gems per Robux).
- **Kind: a game pass**, so Roblox keeps it to one purchase and it shows on the game's Store tab. Its gems and ingot are granted once through the same path as every pass (§7), with a `starterGranted` flag in the save.
- **Offer:** after the tutorial, the Shop button gets the amber dot the Mail button uses, and the pack sits first in the Shop window until bought. No popup, no countdown, nothing in the first session's tutorial.

## 3. Weather (Allen's design)

Allen: "the weather should only be around 5 minutes. sunshine can give 2x more customers, rainbow can give higher chance of vip customer, rain gives higher luck for rolling, snowing for more mail/custom requests"

| Weather | For every shop in the server, about 5 min | Needs |
|---|---|---|
| **Sunshine** | Customers come twice as often | The free Sunshine (built in [[Design/Shop Tension Pass]], `ServerScriptService.Weather`) |
| **Rainbow** | VIP customers come more often | VIP buyers (built in the shop tension pass: `Customers.VIP_CHANCE` 5%) |
| **Rain** | Luck one merge higher (+0.5) at every roller; adds to Lucky Ore | The odds panel when bought (§4) |
| **Snow** | Mail orders and commissions come twice as often | The mail clock (built) |

- **Free and bought:** weather also comes on its own (GDD §7): the free Sunshine is built (5 min, every 15–25 min, [[Design/Shop Tension Pass]]); the other three aren't yet. A bought weather starts at once, or straight after another bought one; the buyer is named beside the weather's HUD icon.
- **Price:** 79 R$ or 60 gems each. Gems from daily rewards (90 a week) or gem packs can buy it, so gems keep a use after the Gem Shop's 325 (Allen).
- **Guardrails:** a plot still in the tutorial gets no weather bonus (the first-sale gate, GDD §7); one weather at a time; no Robux offers pop up during one.
- **Rain is a paid random item** when bought, with Robux or with gems (gems can be bought with Robux): the odds panel before buying, and players where that's restricted can't buy rain (they still get it when it falls).

Supersedes GDD §7's "other weather stays at the normal baseline" and [[Design/Workshop Growth#Weather and customer traffic|Workshop Growth]]'s "No paid weather controls were chosen."

## 4. Luck and Roblox's paid random items rules

Roblox counts luck boosts as paid random items: here **Lucky Ore** and **bought rain**. Before anyone pays, the game shows every rarity's odds as percentages adding to 100, now and with the boost, for that player's luck (merges and weather change it). An (i) button alone is not enough.

**The odds panel** follows Allen's screenshot of Create Pottery!'s "Lucky Clay odds" (shared in chat on 2026-10-27; Lucky Clay doubles the weight of Rare and above): a title ("Lucky Ore odds"), one line ("Your chance of each rarity on your next pull."), two columns **Now → With Lucky Ore**, rarity names in their colours and the gains in green. It opens from the pass in the Shop window before Roblox's purchase window; rain's opens from the weather picker the same way. At no merges:

| | Common | Uncommon | Rare | Epic | Legendary | Secret |
|---|---|---|---|---|---|---|
| Now | 59.9% | 25% | 10% | 4% | 1% | 0.1% |
| With Lucky Ore (or rain) | 39.9% | 37.5% | 15% | 6% | 1.5% | 0.15% |

**Restricted players** (`PolicyService:GetPolicyInfoForPlayerAsync(player).ArePaidRandomItemsRestricted`) see no Lucky Ore and can't buy rain. They can buy an **Ingot of a found metal** instead: an Epic or Legendary metal their book already has, 29 / 99 R$ (Allen). Merging still gives everyone earned luck.

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
| **Coin pack** | 30 min or 2 h of your current income, worked out on the server | 49 / 149 R$ | Allen |
| **Gem pack** | 80 / 200 / 500 gems | 99 / 229 / 449 R$ | Allen. Gems also buy weather (§3) |
| **Ingot of a found metal** | Pick an Epic or Legendary metal your book already has | 29 / 99 R$ | Only for players where paid luck is restricted (§4) |

## 7. How every product works (the monetization skill's rules)

- **Prompt on the client, grant on the server.** `PromptProductPurchaseFinished` and the client's word are never proof.
- **Passes:** one server registry from pass id to benefit. `UserOwnsGamePassAsync` on join (a failed check means unknown, not "doesn't own": retry) and the server's `PromptGamePassPurchaseFinished` both go through the same grant, which sets a player attribute (`Pass_AutoRoller`, …) the services read.
- **Developer products:** one `ProcessReceipt`. Each purchase id is saved in the player's save together with what it granted, so a repeat receipt grants nothing. `NotProcessedYet` when the player is gone, the save isn't loaded, the product is unknown or the save fails; Roblox retries.
- **Weather for gems** is spent and started on the server, like a Gem Shop upgrade; the client only asks.
- **Prices come from Roblox at runtime** (`GetProductInfoAsync`), never typed into the UI. Managed Pricing (regional prices, and price tests of about three weeks that recommend the best prices) is on by default only for items made in Creator Hub; the ones made through Open Cloud have it off (§11).
- **Where offers appear:** where the player already is (the roller's popup, the Shop window, the weather picker); never during the tutorial, a weather or an offer's countdown; an unaffordable pad keeps its shake, not a Robux prompt (the review's rule).
- **Checks before players:** Studio test purchases of each, a repeated receipt, a player leaving mid-purchase, a failed save; then the economy logged with AnalyticsService.

Code when built: `Shared/Store` (ids and what each gives, read by both sides), `ServerScriptService.StoreService` (registry, receipts, PolicyService), a store page in `MenuGui.ShopWindow` (today "Coming soon"), the popup in its own ScreenGui made in Studio, and a receipts list in `SmithyCore`'s save.

## 8. Considered and left out

- **Dropped in the walkthrough:** 2× Coins (50% More Coins instead), 2× Coins for 30 min (coin packs cover it), Customer Rush (sunshine), Lucky Hour (rain), 2× Luck (Lucky Ore), the Etch Pack and the Starter Pack's etch (no buyers-only etches).
- **Anvil 3 early / a fourth crafter:** sells a stage of the spine, and Allen capped active crafters at three.
- **Auto Cashier / auto till:** the Cashier is a crew hire now; one system per effect.
- **Instant heat:** competes with the Faster Heating upgrades.
- **Finish the cart trip now:** trips are 1:10–2:30, too short to pay to skip.
- **2× Gems:** gem packs cover buying gems.

## 9. Robux without a product

- **Private servers:** switch on in the experience settings (free helps friends play together; a monthly price earns Robux). Allen's call.
- **Rewarded video:** a free player watches an ad for a reward (a few gems, a short sunny spell). Open platform-wide; Roblox plans a Studio plug-in in Q4 2026. Check age and region rules before building.
- **Premium Payouts** come from Premium players' time in the game, no code; **subscriptions** only once there's something monthly to give.

## 10. Order and who does what

1. **Done 2026-10-27:** Claude created the passes and products through Open Cloud, all off sale (§11). Each goes on sale when its feature is built; the experience goes public at release.
2. **Claude:** `StoreService`, the receipts list and the store page with live prices.
3. **Claude:** the Auto Ore Roller: popup, switch, keep chip, auto loop.
4. **Claude:** the Starter Pack, 50% More Coins, VIP and Swift Boots.
5. **Claude:** Lucky Ore with the odds panel, and the found-metal ingot for restricted players.
6. **Claude:** weather: bought Sunshine on top of the free one, then snow (the mail clock exists), rain (the odds panel) and the rainbow (VIP buyers exist); then weather for gems, coin packs and gem packs.

## 11. On Roblox (created 2026-10-27)

Universe **10771581195** ("create swords": private, Allen's account, root place 134592579197772). The `ROBLOX_UNIVERSE_ID` environment variable points at another game (Build Across! [GRAND CANYON]), so scripts pass this id. Created through Open Cloud at the prices above, with no images and **all off sale** at first. **The six passes went on sale on 2026-10-27** while the game is private (Allen: "Put all six passes on sale while the game is private, so the Shop shows prices and I can test buying."); the developer products stay off sale until built. Roblox then quoted Allen's account about 10% less than the set prices (135, 180, 90 and 270 R$) with no regional or managed pricing on the passes, so the difference is on the account's side; the Shop shows each player what Roblox quotes them. Managed pricing and regional prices are off (the API's default).

| Game pass | Id | Price |
|---|---|---|
| Auto Ore Roller | 2057783160 | 149 R$ |
| 50% More Coins | 2058251193 | 199 R$ |
| Lucky Ore | 2058881145 | 149 R$ |
| VIP | 2057315118 | 299 R$ |
| Swift Boots | 2057291128 | 99 R$ |
| Starter Pack | 2057171214 | 99 R$ |

| Developer product | Id | Price |
|---|---|---|
| Sunshine | 3723120522 | 79 R$ |
| Rainbow | 3723120527 | 79 R$ |
| Rain | 3723120529 | 79 R$ |
| Snow | 3723120534 | 79 R$ |
| Coin Pack (30 min) | 3723120538 | 49 R$ |
| Coin Pack (2 h) | 3723120543 | 149 R$ |
| 80 Gems | 3723120545 | 99 R$ |
| 200 Gems | 3723120547 | 229 R$ |
| 500 Gems | 3723120548 | 449 R$ |
| Epic Ingot | 3723120551 | 29 R$ |
| Legendary Ingot | 3723120555 | 99 R$ |

- **Lucky Ore's and Rain's descriptions carry the odds** at no merges, since a pass can also be bought from the experience's Store tab.
- **On sale when built:** `PATCH https://apis.roblox.com/game-passes/v1/universes/10771581195/game-passes/{id}` or `https://apis.roblox.com/developer-products/v2/universes/10771581195/developer-products/{id}` with the form field `isForSale=true`. The API key reads and writes both. Whether Studio's test purchases need a pass on sale is unchecked.

## 12. Built (2026-10-27, not played)

Allen: "after this, work on the actual features the passes give". What each pass does is in the game ([[Development/Code Map#Robux passes (2026-10-27)]]); they're bought from the Shop page or the Auto Ore Roller's button (§5).

- **VIP's gold name tag** is a gold [VIP] before the name in chat.
- **The coin passes multiply** (×1.65 with both) and pay when the coins land: the offer card still shows the customer's offer; the Cashier's till holds the boosted coins, so its sign shows them.
- **Lucky Ore adds +0.5** to the merges' luck: one merge higher at any count.
- **Auto starts off;** its switch and keep chip are saved like the Settings switches.
- **In Studio** nobody owns a pass: tick them on `StoreService`'s attributes to try them; a test purchase grants one for the session.
- **The Shop page** (Allen: "Build the Shop page next: the other passes with live prices, the Starter Pack's dot and Lucky Ore's odds panel"; [[Development/Code Map#Shop page (2026-10-27)]]): a scrolling list of the six passes, carded like the Gem Shop, each price from Roblox ("—" while a pass is off sale) and "Owned" once yours. The Starter Pack is first until bought; after the tutorial the Shop button's amber dot shows until you open the Shop, each session.
- **Lucky Ore's Buy opens its odds panel** (§4): every rarity now and with it, for your own luck; the purchase is made from there. Where paid random items are restricted (or `PolicyService` can't say) its card is hidden; the found-metal ingot that replaces it there comes with the developer products.
- **Not built:** the developer products, images on Roblox.

## Open

- **"VIP" twice:** the VIP pass and the rainbow's VIP customers share a name; one may want another.
- **Numbers to tune:** how often free weather comes (the review suggested every 10–15 minutes), the rainbow's boost and the gem prices.
- **Lucky Ore on the Store tab:** a pass can also be bought on the experience's page, where the game can't check `PolicyService`, and Roblox's paid-random-items page doesn't cover that case. Before the game goes public: keep the pass, or sell Lucky Ore as a one-time in-game product (the pass then goes off sale). It's on sale now only because the game is private.
- **Images:** none of the 17 has one yet.

## Allen's answers (2026-10-27)

1. **Luck:** "It should be an increased luck pass, but doesn't have to be necessarily 2x. I notice in the clay game they have the odds available", with the Lucky Clay screenshot. Then ×1.5, one merge higher: **Lucky Ore**.
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

Related: [[Design/Game Design Document#15. Monetization (Robux)|GDD §15]] · [[Design/Economy Pass 2]] · [[Design/Progression and Economy Review — 2026-10-27]] · [[Design/Urgency Review]] · [[Design/Workshop Growth]] · [[Art/Icon Library]] · [[Sessions/2026-10-27#Monetization plan]] · [[Sessions/2026-10-27#Monetization walkthrough]]

---
title: Monetization Review — 2026-11-08
status: proposed
type: design
updated: 2026-11-08
tags: [monetization, robux, weather, compliance, create-swords]
---

# Monetization Review — 2026-11-08

Allen: "Can you improve our game monetization. Use all the roblox monetization skills available for knowledge". **Proposals only:** nothing built, no product or price moved on Roblox. Skills read: roblox-monetization, LihFolk monetization compliance, roblox-player-psychology. Checked against [[Design/Monetization Plan]], [[Design/Monetization Ideas — 2026-10-31]] (its 8 questions were never answered), [[Design/Decisions Log]], [[Design/Economy and Progression Review — 2026-11-08]] and [[Design/Reviews 2026-11-07/Pre-release Checklist]].

## What the game sells today

- **Passes (one-time):** 8 on sale, all power or comfort. A player who buys every pass spends about **1,000 R$** once (149 + 199 + 149 + 299 + 99 + 49 + 49 = 993), and then the only thing left to buy is more coins or gems.
- **Repeatable:** coin and gem packs only. The four weathers (Sunshine 3723120522, Rainbow 3723120527, Rain 3723120529, Snow 3723120534) exist on Roblox, off sale, and are **not wired**: Studio grep finds no weather id in `Shared/Store` or `StoreService` (2026-11-08).
- **Cosmetics:** none.
- **Restricted regions:** `ArePaidRandomItemsRestricted` is read only on the client (`MenuController:575`, `WorldStoreController:103`); `StoreService` never checks it (Studio grep, 2026-11-08). Same as the 2026-11-07 checklist's gate 6.

## Ranked: build

1. **Bought weather: Sunshine and Snow first** (Plan §3, decided 2026-10-27; the economy review's gem sink). 79 R$ or 60 gems, the whole server for 5 min, the buyer named by the weather icon. The only repeatable item that isn't currency; everyone in the server sees who bought it, which is the strongest honest prompt the game has. Rainbow next. Rain last: it's a paid random item, so it needs the odds panel and a server policy check. About 3–4 h for Sunshine + Snow.
2. ~~Images on all 27 items.~~ **Dropped (readback later the same day):** the items already have icons (e.g. 7 Gems `iconImageAssetId` 103733435271727, Auto Anvil `iconAssetId` 94979932657605), and the Build a Bridge copies carry one each. The Plan's "none has an image" is out of date.
3. **A cosmetic shelf: Fireworks 19 R$ and Slash Trails 49 R$** (Ideas §3, items 3 and 4). Raises the spend ceiling past the 1,000 R$ of passes without touching "anyone can earn everything". Fireworks are repeatable and the whole server sees them. About 2–3 h each.
4. **At release: paid private servers and a quiet Roblox Plus button** (Ideas §3, items 2 and 9). Private servers at **143 R$ a month** earn Roblox's full 100 R$ per Plus member who plays an hour in one (99 R$ earns 69). The Plus button earns 250 R$ a month for three months per sign-up through the game's prompt. Both tiny.

## Ranked: fix before going public

5. **Lucky Ore's restricted-region check on the server.** Recommended with it: sell Lucky Ore as a one-time developer product (as the Starter Pack is), prompted only after the server's `PolicyService` check (fail closed), and take pass 2058881145 off sale. A pass can be bought on the Store tab, where the game can't check. Owners keep it: `Store.owns` reads the pass or the saved flag. Allen's call ([[Design/Monetization Plan#Open]]).
6. **The found-metal ingot** for restricted players (Epic 29 R$, Legendary 99 R$; products exist, off sale).
7. **Managed pricing:** the terms are accepted per owner. Allen's user account (owner of Sell Swords!, 10771581195) still returns 400 InvalidManagedPricing on passes and products; the Allen group's Build a Bridge (10769630190), where the game launches, already has it on for 27 of its own products. So it goes on the 26 Build a Bridge copies; the Sell Swords! items never ship.

## Left out (already ruled)

Crew XP boosts, timed 2× coins, skips, offers after a roll or on a full rack, pads or crew for Robux, countdown bundles ([[Design/Monetization Ideas — 2026-10-31#Don't]]).

## Questions for Allen

1. Build bought weather now, Sunshine and Snow first?
2. Lucky Ore: switch to a one-time developer product, or keep the pass?
3. Fireworks and Slash Trails: yes?
4. At release: private servers at 143 R$ a month, and the Plus button?

**2026-11-08, later:** item 7 done: managed pricing on for all 26 Build a Bridge copies (readback 26 of 26). Build a Bridge is for playtesters only for now (Allen), not public.

**2026-11-08, later:** item 1 built (Sunshine and Snow): [[Sessions/2026-11-08#Bought weather: Sunshine and Snow]]

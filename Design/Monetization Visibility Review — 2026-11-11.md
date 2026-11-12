---
title: Monetization Visibility Review — 2026-11-11
status: picks built 2026-11-11/12 (1–3, 5, 8; not played); 7 bell approved, not built
type: design
updated: 2026-11-11
tags: [monetization, shop, ui, world-store, robux, create-swords]
---

# Monetization Visibility Review — 2026-11-11

Allen: "i want to examine our monetization. do research on monetization strategies for tycoon games similar to ours. examine our shop UI hierarchy and style. is there no incentive or reason to buy anything? are we not pushing it enough? is there no reason to open the shop? do we need more physical views for players to see and buy? are prices too high? are purchases not advertised well enough in game?"

**Nothing was changed.** Read in Studio during Allen's Play session (client, read-only: `PlayerGui.MenuGui`, a viewport capture) and in Edit (`StarterGui.MenuGui.ShopWindow` layout orders, `WorldStoreController`, the `PromptGamePassPurchase` callers). Checked against [[Design/Monetization Plan]], [[Design/Monetization Pricing Pass — 2026-11-11]], [[Design/Monetization Review — 2026-11-08]], [[Design/Monetization Ideas — 2026-10-31]] and the [[Design/Decisions Log]]. Skills: roblox-collaboration-mode, roblox-monetization.

## What this rests on

- **No buyers yet.** Analytics Query API, Swordsmith Tycoon (10769630190): DAU 4, 4, 7, 10, 5, 1, 3 for 2026-11-04 to 2026-11-10, all playtesters; 0 paying users (pricing pass, same day). The Shop funnel (built 2026-11-10) has no openings logged. So every verdict below is from the build and from other games, not from our players.
- **Prices were just reset** this morning (nine changes, Starter Pack 29 R$, Daily Deal, Lucky Rolls, first-buy double). This review is about whether players **see** and **want** them.

## Short answers

| Question | Answer |
|---|---|
| No reason to buy? | The reasons exist (50% More Coins is +107% coins over 10 h in the sim; four autos remove the most repeated actions), but a player only meets most of them inside the Shop. |
| Not pushing enough? | Yes, after the first session. The only push that brings players to the Shop, its dot, shows once a session and **never again once the 29 R$ Starter Pack is owned**. |
| No reason to open the Shop? | Right. Nothing in it is free, nothing in it changes day to day that the HUD tells you about, and its button looks like Book, Crew and Upgrades. |
| More physical views? | Yes. One thing in the world sells today (Lucky Metal's board). The other passes have no object, and other players' plots show only the lever hand. |
| Prices too high? | Not the problem now. The ladder starts at 9 R$; the first buy is 29 R$ at 3× value. Only the 100,000 and 300,000 coin packs are still badly priced (open since this morning). |
| Advertised well enough? | No. Except weather (buyer named), a purchase is silent: nobody else in the server learns that someone bought VIP, a bundle or a pack. |

## The Shop today

**The button.** `MenuGui.Buttons.Shop` is one of four equal 44 × 44 icons in the 2×2 grid (Book, Shop / Crew, Upgrades since today), 64 × 50 px on a 1578 × 753 screen. Same size, same label style as the other three. Its amber "!" dot is the same dot Crew uses. There is no "+" next to the coin or gem counters.

**The dot's rule** (`MenuController:611`): `not shopSeen and lessonsDone and not owns("StarterPack")`. Once a session, and only until the Starter Pack is bought. At 29 R$ that will be most buyers' first purchase, after which the Shop never calls again.

**The list, top to bottom** (Edit layout orders, one scrolling list 2,925 px tall in a 436 px window at desktop, about 6.7 screens):

| # | Section | Cards | Height |
|---|---|---|---|
| 1 | Featured | Starter Pack (gone once owned), Automation Pack | 198 |
| 2 | Everything Bundle | one card with nine pass tiles | 444 |
| 3 | GAME PASSES | Auto Ore Roller, 50% More Coins, 50% More Gems, Lucky Metal, VIP, Swift Boots, Auto Anvil, Auto Etch, Auto Polish, Bigger Bag | 832 |
| 4 | WEATHER | Sunshine, Snow, Golden Hour | 190 |
| 5 | CURRENCY | Daily Deal, 7–500 Gems, 800–300,000 Coins, 5 / 15 / 30 Lucky Rolls | 959 |

What that order means:
- **The first phone screen is the Starter Pack, the Automation Pack and the top of a 599 R$ bundle** (the 2026-11-10 phone capture shows exactly that). Fine while the Starter Pack is there; once it's owned, the first screen is two big asks.
- **The cheap and repeatable things are at the bottom.** The Daily Deal (29), Lucky Rolls (9 / 19 / 29) and the 9 R$ packs sit about 70–100% of the way down, Lucky Rolls after the 999 R$ coin pack. The weather (39 R$, the item everyone in the server sees) is two-thirds down.
- **Nothing on the cards says "new" or "today".** The Daily Deal resets every UTC day, but nothing outside the Shop says so.
- **The card art is strong** (bright family colours, sparkles, big icons, gift buttons, crossed-out bundle totals). The style isn't the problem; the order and the way in are.

## Where the game sells today

| Place | What | Shows when |
|---|---|---|
| Shop window | everything | the player opens it |
| Shop button's dot | the Shop | once a session, until the Starter Pack is owned |
| Auto-Roll bar's lock | Auto Ore Roller | near your lever, after the lessons |
| Anvil / Etching / Polishing HUD locks | Auto Anvil, Auto Etch, Auto Polish | at that station |
| Lucky Metal's board | Lucky Metal, Lucky Rolls | by the ore stands, near it |
| Short of coins or gems | the smallest covering pack, Roblox's prompt | tapping a pad or level you can't afford |
| Weather | the buyer's name by the weather icon | while a bought weather runs |
| Other players' plots | the lever-hand villager (Auto Ore Roller), the Lucky board's "You" column | when that owner has it |

Gone at Allen's word: the 50% More Coins chest in the shop (2026-11-01, "i dont want the physical 50% more coins purchase in the sword shop") and the Auto Ore Roller's sign by the lever (2026-11-10, "nothing physical there", then "just remove it"). The lesson from both: a world spot has to be a real object that does something, as the Lucky board does, not a sign that only sells.

No world spot or visible sign for: 50% More Coins, 50% More Gems, VIP, Swift Boots, Bigger Bag, the bundles, the Starter Pack, Fireworks (not built).

## What other tycoons and Roblox say

From a research subagent (web, read-only). **S** = the source says it; **I** = inferred. No public data compares in-world pads with a shop window, and no source gives shop-open rates.

- **Roblox names shop visibility as a cause of low conversion.** "Poor item or shop visibility" is on its list, with "devote as much creativity and attention to your storefront as you do to the rest of the game" (S, [Monetization analytics](https://create.roblox.com/docs/production/analytics/monetization)). The shop should be easy to find and quick to get in and out of (S, [Monetization foundations](https://create.roblox.com/docs/production/game-design/monetization-foundations)).
- **Contextual purchases, Roblox's guide.** Offer the right item at a natural pause, never stack popups, and pair items (Bee Swarm's paired passes). A world object can advertise items; if it doesn't hold the whole range, using it should lead to the main shop. Shop badges are its own example of a contextual UI cue (S, [Contextual purchases](https://create.roblox.com/docs/production/game-design/contextual-purchases)).
- **Tycoon kits put pass buttons among the buy pads** (common). Players complain about them shining in their faces and about accidental prompts from mashing buttons on a phone (S, DevForum, one-offs). We already avoid this: our locks sit in station HUDs, and the Lucky board needs a tap.
- **Starter pack** (the agent quoting a Roblox design page I couldn't open, so **unverified**): 2–10% revenue lift; show it from the first spawn, because hiding it behind a tutorial means fewer players see it; a HUD button plus a top store slot; at most one popup, at a high point. Ours waits until the tutorial and its gem buy are done (2026-10-31 decision) and has no HUD button, only the Shop dot.
- **Roblox's own Shop button** (S per DevForum, **not verified** by me): a storefront Roblox launched in July 2026, an optional top-left Shop button with a blue dot for new offers, and `MarketplaceService:OpenShop()` since September. Roblox quotes ">5% Robux spend per user" for one game. Worth a look once we're public.
- **Selling outside the game** (S, [Passes](https://create.roblox.com/docs/production/monetization/passes)): listed passes appear in search and after a Robux purchase; passes can be opted in as Buy Robux bonus items; developer products can be listed on the game's page. `RankProductsAsync` can order a shop per player.
- **Numbers** (S, [GameAnalytics 2025 Roblox report](https://www.gameanalytics.com/reports/2025-roblox-report)): daily spend per paying player, median about $0.72, rising from $0.48 for 0–3 min sessions to $2.12 for 25+ min. Payer conversion of 1–3% (2–3% for tycoons) comes from a calculator site with no source, so treat it as low confidence.
- **What Roblox warns against** (S, checked myself on [Monetization](https://create.roblox.com/docs/production/monetization)):
  - a "deal of the day" that says it lasts 24 hours but returns every login;
  - countdown timers that aren't accurate or restart;
  - an item that is always "on sale";
  - pushy wording with minors ("GET IT NOW"; use "View Item", "See Price", "Open Shop").

  **Our Daily Deal:** it claims no expiry, and its once-a-day limit is real, so it doesn't match the warned case. But a "Deal" tag that never changes is close to an "always on sale" item. Don't light the HUD for it every day (proposal 2 leaves it out).

## Proposals, ranked

Each is small and reversible. None opens a window by itself, none fires after a roll, none sells pads or crew (the [[Design/Monetization Ideas — 2026-10-31#Don't]] list).

1. **A reason to open the Shop every day: a free gift card at the top.** The daily reward (today a top-bar icon) moves into the Shop as its first card, "Free gift", with the Shop button's dot lit whenever it's ready. Every claim walks the player past the Starter Pack, the Daily Deal and the weather. No new currency: the same reward, a new place. The research found no source for a free gift inside the shop, so this one rests on our own reasoning. About 2 h. **Touches:** the top-bar Daily icon goes (or opens the Shop at that card).
2. **The Shop button's dot follows what's new, not just the Starter Pack.** Lit when the free gift is ready, a new item goes on sale, or the Starter Pack is unowned. Not for the Daily Deal (Roblox's "deal of the day" warning, above). Cleared when the Shop opens. A different colour from Crew's "!" (e.g. a green dot with a small gift glyph) so it reads as "something for you" rather than "something to do". About 1 h.
3. **"+" on the coin and gem counters.** Tap opens the Shop at Currency. Every simulator has this; ours has none. About 30 min.
4. **Reorder for the phone's first screen.** Featured becomes: Starter Pack (while unowned), Daily Deal, Sunshine. The Everything Bundle shrinks to one short banner (title, crossed-out total, price, "See all nine") that expands, instead of a 444 px card. Lucky Rolls move up next to Lucky Metal in Passes, behind the same odds panel. About 2 h, plus the UI audit at 388 px.
5. **Say who bought what, once.** A short line in the server's chat or the weather banner's spot when someone buys a pass, a bundle or the Starter Pack: "goku19876 got VIP!". Weather already does this. No amounts, no packs of currency (that's spending status, row 30 of the Don't list). About 1–2 h. Allen's call: some cozy games skip this.
6. **Make owned passes visible on other plots.** Each owned pass leaves a small mark others can walk past, like the lever hand: a gold name tag over a VIP owner's head (the VIP description already promises one: check it shows to others), a faint dust trail on Swift Boots, a gold coin burst on a More Coins owner's sales, the auto-stations' small villager helpers. About 1 h each. These are the honest adverts: a neighbour's better shop.
7. **Two new world objects that do something.** (a) **A weather bell** on the street by the gate: anyone rings it to buy Sunshine or Snow for the server (39 R$ or 60 gems), the buyer named. A real object with a real effect, in the shared space where the whole server sees it. (b) **Fireworks crate** by your shop sign (19 R$, asked 2026-10-31, 2026-11-08 and this morning; never answered). About 3 h each.
8. **Show the Starter Pack earlier.** Give it its own small HUD button (the chest art, the price under it) beside the 2×2 menu while it's unowned. Show it from the first sale rather than after the gem buy. Its one popup, if any, comes at the first sale's cheer. This reverses part of the 2026-10-31 "Robux offers wait for the gem step" decision. About 1 h.
9. **At release: list passes outside the game.** Opt them into the Buy Robux bonus items, and list developer products on the game's page (Ideas 2026-10-31 #6). About 30 min in Creator Hub.
10. **Leave prices alone until there are buyers.** Managed pricing is on for every item; Roblox will test once traffic exists. Settle the two big coin packs (this morning's open question: leave, income-based, or off sale).

## Conflicts to rule on

- **Proposal 5** goes beyond the plan's "the buyer named" for weather only. Kids reading "X got VIP!" is a mild push.
- **Proposal 1** moves the daily reward. The top-bar icon was Allen's layout.
- **Proposal 8** puts the Starter Pack in front of players before the gem step, against the 2026-10-31 decision. The Shop's own Buy buttons were never gated.
- **Proposal 6, Swift Boots trail and coin burst** are new effects: one system per effect ([[upgrade-design-rules]]) holds, since each only marks a pass that already exists.

## How we'll know

The Shop funnel (`ShopFunnel` Opened → Pressed Buy → Bought) and the `WorldStore` and `PassPrompt` events (CF3 source Shop / World / Lock / Offer) are built. After the public release: Shop openings per daily player, Buy presses per opening, and which source sells. A tycoon with a healthy Shop sees most players open it in their first session; if ours is under half, the way in is the problem, not the prices.

## Questions for Allen

1. Which to build: 1 free gift card, 2 dot rules, 3 "+" buttons, 4 reorder, 5 purchase line, 6 visible passes, 7 bell / fireworks, 8 Starter Pack button?
2. Proposal 5: show "X got VIP!" to the server, yes or no?
3. The two big coin packs: leave, income-based, or off sale?

---

Related: [[Design/Monetization Plan]] · [[Design/Monetization Pricing Pass — 2026-11-11]] · [[Sessions/2026-11-11#Monetization visibility review]]

## Allen's picks (2026-11-11)

- **Built (Edit, not played):** 3 the "+" buttons, 5 the chat line, 8 the Starter Pack button (after the tutorial). [[Sessions/2026-11-11#Visibility picks: + buttons, chat line, Starter Pack button, free gift mockup]]
- **Built 2026-11-12 (not played):** 1–2 the daily reward as the Free Gift card at the top of the Shop, replacing the join popup ([[Sessions/2026-11-12#Daily reward in the Shop; a plain + on the counters]]). Mockup: ![[Art/UI/free-gift-1111/free-gift-mockup-desktop.jpg]]
- **Approved, not built:** 7 the weather bell on the street, after the tutorial.
- Also from this review: 50% More Coins and 50% More Gems became real **2x Coins** (349 R$) and **2x Gems** (199 R$). [[Design/Monetization Plan#2x Coins (2026-11-11)]]

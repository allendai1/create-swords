---
title: Shop Star Rating Research — 2026-11-11
status: research — nothing changed in Studio; waits for Allen's pick
type: design
updated: 2026-11-11
tags: [design, reputation, rating, personalisation, create-swords]
---

# Shop Star Rating Research — 2026-11-11

Allen: "what about a customer rating for the store. like some games like restaurant tycoon have a 5 star system that shows how their store is. im not sure how it works, can you take a look and research". **Nothing was changed in the place.**

## How other tycoons do it

Sources are fan guides and wikis, not the developers; treat exact numbers as unconfirmed.

| Game | What feeds the stars | Can it drop? | What stars give | Where it shows |
|---|---|---|---|---|
| **Restaurant Tycoon 3** | A fixed checklist: 36 yes/no factors in five categories (Service, Food, Atmosphere, Expansions, Hygiene), each adding a fixed slice (e.g. 8 chefs, 20 mains on the menu, music playing, 3 toilets, Floor 2) | Only if you stop meeting a "keep" factor | Not stated by the wiki | Stars over the door; a board lists every factor |
| **Restaurant Tycoon 2** | Food, service, design, popularity, experience, eco; cleanliness (dirty dishes) and slow service pull it down | Yes: neglect lowers it | More customers, bigger tips, VIP diners at 5.0 | A ratings board at the front |
| **Theme Park Tycoon 2** | Guest happiness, finances, park value, variety; litter hurts | Yes | Prestige; the last half star is hard | Top-left of the screen |

Three models, then:
1. **Checklist** (RT3): stars are a to-do list. Every missing star says what to build. Never judges you, never punishes.
2. **Live satisfaction** (RT2, TPT2): unhappy customers and mess drag it down. Needs chores to keep up.
3. **Points** (our current Reputation): sales add points, ranks never drop.

## What we already have

- **Reputation:** +1 a sale, +3 an order, +5 a commission; 8 ranks at 0 / 5 / 15 / 30 / 50 / 80 / 120 / 175; **never drops** (cozy rule, [[Design/Decisions Log]] 2026-10-22).
- It shows only as "Rank N" in the Deliveries window. Ranks 6–8 do nothing ([[Design/Economy and Progression Review — 2026-11-08#7. Reputation has no effect after Rank 5, and its two effects are hard to see]]).
- **More customers does nothing:** walk-ins outnumber swords 5–11× all game, so no sword waits for a customer ([[Design/Economy Pass 2]]). A star effect of "more walk-ins" would be invisible.
- The GDD already says **reputation unlocks surprise special visitors** (§7), and [[Design/Major Updates Plan — 2026-11-07]] has Legendary Commissions.
- The shop sign already shows the owner's display name; Decorate is built and hidden ([[Sessions/2026-11-11]]).

## Options for Sell Swords!

**A. Reputation becomes stars (smallest).** The 8 ranks show as ½-star steps (Rank 1 = ½★ … Rank 8 = 4★, a 5★ cap later) on the shop's signboard under the owner's name, and in the HUD where "Rank" is. Same points, same effects, never drops. About 2–3 hours. Fixes "the rank is hidden"; still says nothing about *how* the shop is.

**B. Checklist stars (recommended).** RT3's model, sized to our game: five categories, one star each, each made of 3–4 yes/no ticks the player can see on a board by the door.

| Star | Ticks (examples, numbers to tune) |
|---|---|
| **Display** | every rack and table slot filled; a Big Sword Stand filled; 10 swords on show |
| **Craft** | a polished sword on show; an etched sword on show; a Rare-or-better metal on show; 5 sword designs known |
| **Service** | a Cashier hired; a Stocker hired; a Promoter hired |
| **Fame** | Reputation rank 3 / 5 / 8 (the current points live on as one star) |
| **Look** | the Upgraded Store; 2 / 4 / 6 decorations placed |

- **Never drops below what you earned?** RT3 lets "keep" ticks fall (an empty rack). Our cozy rule says reputation never drops. Proposal: Display and Craft ticks are live (they read the shop now: fill the racks and the star comes back); the rest are permanent.
- **What stars give:** not walk-ins (they change nothing). Proposal: each full star sends a **special visitor** (the GDD's) who buys at a higher price, and 5★ puts a gold frame on the sign. Any coin effect changes `Development/sim` in the same pass ([[Design/Decisions Log]], sim mirrors game rules).
- **Look counts decorations**, which gives Decorate a reason, but it **changes the "purely cosmetic" rule** (2026-10-19, 2026-10-28). Allen's call.
- About 1–2 days with the board UI, the sign and the sim.

**C. Live satisfaction (not recommended).** Customers who leave unhappy after a haggle pull the stars down. Breaks "reputation never drops", punishes the haggle the GDD wants players to try, and kids read a falling score as failing.

## Questions for Allen

1. A, B or C?
2. If B: may the Look star count decorations (ends "purely cosmetic")?
3. What should a star give: special visitors, a price bonus, or only the sign?
4. Do Ranks 6–8 become stars, or go (the 11-08 review's other choice)?

## Follow-up: input, and how a customer's taste would work (draft)

Allen: "If its tied to things they will get eventually then the player really doesnt have much customization or input on it?", then "How would we decide what a customer likes". Agreed: a checklist of main-path buys is progress relabelled. The draft rates **how each customer was served** instead.

- **Conflict first:** "No favourite swords" (2026-10-30, two kinds of customer) removed tastes. This brings a version back. Allen's call.
- **Taste vocabulary = the board orders' twists** (`Shared/Orders`, not re-read today: Studio MCP down), so players learn one set: a **shape family** (Japanese, Western, Big), a **metal floor** (Uncommon+, Rare+), a **finish** (polished, etched).
- **Who wants what:** a regular has one want, drawn only from what the player can already make (as order twists wait for their station); a VIP has their character's fixed taste plus one more (e.g. the big-sword VIP wants a Big Sword Stand sword).
- **Shown** as one icon over the customer's head as they walk in (no text). They head for a matching sword if one is on display, and still buy something if none is (cozy).
- **Review:** match and finished 5★, match 4★, no match 3★; one star off when a haggle drags past the first decline. Stars come from **counting 5★ reviews** (never drops) unless Allen picks a moving average.
- **The player's input:** what they put out (the display mix), which swords they finish, how hard they haggle.
- About 1 day on top of the rating's sign and board.

## Sources

- [Restaurant Tycoon 3 rating categories (Bloxodes wiki)](https://bloxodes.com/wiki/restaurant-tycoon-3/rating-categories)
- [Restaurant Tycoon 2: How to Increase Cleanliness (RobloxDen)](https://robloxden.com/game-codes/restaurant-tycoon-2/guides/restaurant-tycoon-2-how-to-increase-cleanliness)
- [Restaurant Tycoon 2 beginner's guide](https://www.narcosis-the-game.com/?p=2002)
- [Restaurant Tycoon 2 tier list (earnaldo)](https://earnaldo.com/blog/restaurant-tycoon-2-tier-list-2026)
- [How to get 5 stars in Theme Park Tycoon 2 (TouchTapPlay)](https://www.touchtapplay.com/how-to-get-5-stars-in-theme-park-tycoon-2-roblox/)
- [Theme Park Tycoon 2 forum: stuck at 4.5 stars](https://themeparktycoon2.com/forum/tpt2-help/how-to-get-a-5-star-park-in-theme-park-tycoon-2)

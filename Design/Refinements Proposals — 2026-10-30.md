---
title: Refinements Proposals — 2026-10-30
status: 1 and 3 built, 2 proposed (2026-10-30)
type: design
updated: 2026-10-30
tags: [design, tycoon, upgrades, monetization, create-swords]
---

# Refinements Proposals — 2026-10-30

From Allen's evening list in [[Refinements]]: the items that are his call. What was built from the same list is in [[Sessions/2026-10-30#Refinements, evening list]].

## 1. Fewer pads on the floor

**Built** (Allen: "Go thru with the upgrades pads"): option A, cap 3. The Sword Crafter's pad waits under the cap too (Allen: "Keep the cap"). [[Sessions/2026-10-30#Refinements, Allen's answers (evening)]]

Allen: "I think there's too many upgrades on the floor at one time. Ideally players shouldn't have TOO much to choose from. Use the lihfolk skills for help or suggestions with ordering and suggest how can we order our upgrades in a better way."

**Now** (simulated players' buys, median per type; [[Development/Sim Runs/padcap-2026-10-30]]):

| Minutes in | 0 | 10 | 30 | 60 | 120 | 240 | Peak |
|---|---|---|---|---|---|---|---|
| Pads on the floor | 7 | 8–9 | 8–10 | 7–11 | 7–10 | 6–7 | 10–12 |

Seven chains run side by side (ore slots, swords, heat, strikes, polish and etch, racks, shop holders), plus the parking bays, the Delivery Cart and the crew.

**LihFolk** (Genre Playbook - Tycoons §2, §3, §11; Onboarding by Genre):
- Keep 1–3 buy buttons available at once. Ten is "a menu nobody reads on a phone".
- The next button sits by the last build, and the next purchase shows with its price.
- Buttons available together should pay back about equally; otherwise players buy the best one first anyway.
- A wait ceiling of about 2 min early and 5–10 min late.

**Option A, recommended: only the cheapest few.** Of the pads whose gates are met, only the 3 cheapest stand on the floor, plus the next sword (the main goal) and the Delivery Cart ("should always be available"). Buying one brings the next cheapest. No gate changes; it's a filter in TycoonService's `refresh`.
- Simulated, cap 3 / 4 / 5 against today's game (150 free players a type): nobody slower. Sword Crafter efficient 2:00 / 2:02 / 2:04 (2:11 today), manager 1:46 / 1:41 / 1:41 (1:50), grinder and casual unchanged; Seraph within 30 min either way; waits over 15 min the same.
- Pads on the floor with cap 3: 4–5 the whole game (cap 4: 5–6, cap 5: 6–7).
- Trade-off: you can't see far-off goals on the floor. The Upgrades tree or a "next" list could show them if that matters.

**Option B: one pad per zone.** The yard's left (furnaces, ingot racks), back (anvils, swords, strikes), right (polish, etch), the ore roller, the shop floor and the street each show their cheapest available pad. About 6 on the floor; it spreads them out, but doesn't get near 1–3.

**Option C: stages.** A stage's 3–4 pads, all bought, then the next stage's; each ends on a reveal (a sword, a crew member). The clearest, but every pad's order becomes fixed, and the shop floor and the smithy stop growing at their own rates (Allen 2026-10-29: "The shop upgrades and the smithy upgrades should progress at their own rate").

Cost: A is small (one filter on the server, the sim's `padCap` already models it); B small; C medium (every gate rewritten).

## 2. Buying with Robux in the world

Allen: "look into ways we can have physical in-game purchases. players are more likely to buy something they can see in the game rather than opening shop and clicking."

The LihFolk vault has no number for in-world against menu sales, but it does say "contextual offers are the strongest converter", and has these rules (Clickable and Interactive Parts; Lobby and Hub Design; Game Passes; Paid Random Items and Odds Disclosure; Ethical Design and Player Trust):
- A ProximityPrompt on the object at chest height; not a touch pad (it fires per body part).
- Roblox's own purchase window already confirms, so no "Are you sure?".
- Nothing during the tutorial.
- Lucky Ore is paid luck: its odds show before the buy, and it's hidden where paid random items are restricted (as the Shop does today).
- Ownership comes from one server cache; prices come from Roblox at runtime.

**Proposal: each pass where it works, shown locked until owned.** Six spots on your own plot, after the tutorial; each shows its Robux price on a one-line label like a pad's, and the prompt opens Roblox's purchase window:
1. **Auto Ore Roller**: a motor on the ore roller, dark until owned, then cranking the lever by itself. It sits where the player pulls the lever over and over.
2. **Lucky Ore**: a gold-lit ore case beside the stands; its prompt opens the odds window first.
3. **50% More Coins**: a coin chest at the shop's counter, full once owned.
4. **Swift Boots**: a pair on a stand on the path between the shop and the yard, the walk they speed up.
5. **VIP**: a gold rope at the shop door, where VIP customers come in.
6. **Starter Pack**: a crate by the shop door, gone once bought (it's one-time).

Start with 1–3, and add a funnel per place (prompt shown → bought, world against the Shop window) to see which sells. Fits the Monetization Plan's "where the player already is" (§7). Cost: medium (three small models, one client script reading `Shared/Store`).

## 3. Crew levels for gems

**Built** at 20 / 55 / 105 / 200 (Allen: "Crew levels increase those gems cost by 1/3"). [[Sessions/2026-10-30#Refinements, Allen's answers (evening)]]

Allen: "Maybe add option to upgrade employees level with gems if player doesn't want to wait for it to level up."

- **Now:** crew reach Lv. 2 / 3 / 4 / 5 at 10 / 30 / 70 / 150 swords (about 12 min, 40 min, 1.5 h, 3 h); a crafter gets +8% quality a level.
- **Proposal:** a "Level up" button by the level bar on the crew page, in gems for the next level. A start: Lv. 2 15, Lv. 3 40, Lv. 4 80, Lv. 5 150. That's inside the Gem Shop's 5–380 range, and a new gem sink beside it.
- **Fit:** it competes with no coin upgrade (the Monetization Plan left out "Instant heat" because it did), and levels are only crew's (one system per effect).
- **Before pricing:** simulate gem income against it (one simulated casual player had earned about 780 gems by the end of a run).

## 4. Questions back to Allen

- **"Early game rolls rarity needs a boost, seems like its"**: cut off. Today at no merges: Common 60%, Uncommon 25, Rare 10, Epic 4, Legendary 1, Secret 0.1, an average metal ×1.57. What did you see: Commons too often in a row? Options:
  - a pity (a Rare at least every N pulls);
  - better base odds (e.g. Common 50 / Uncommon 30 / Rare 13: about ×1.74, +11% income; the sim has `rare-odds+50` to test).
- **"Also thinking of having the map so that"**: cut off. A map review is in progress with the LihFolk worldbuilding notes; its suggestions will be in the session note.
- **Anvil hits 12 → 10** ("Thinking of reducing"; then "Yes do 10 hits": **built**, [[Sessions/2026-10-30#The anvil takes 10 hits (subagent)]]): every blade's recipe in `Shared/BladeData` is 12 strikes over three stages (24 recipes); BladeCore checks each stage covers the blade and the golden test replays them. About an hour to change, and forging gets about 17% quicker. Faster Strikes already halves the strike time by Lv. 5. Do it?

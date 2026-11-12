---
title: Tycoon Psychology Review — 2026-11-09
status: review; one small pass built in Edit (Quest marks), not played; the rest waits for Allen
type: design
updated: 2026-11-09
tags: [design, review, choices, economy, onboarding, create-swords]
---

# Tycoon Psychology Review — 2026-11-09

Allen asked me to apply [[Design/Tycoon Psychology and Meaningful Choices - 2026-11-09]] to the game as it stands. That note describes an earlier version, so every point below was checked against the live Studio place (Edit), the GDD, the Decisions Log and the session notes up to 2026-11-09.

**Three kinds of claim, kept apart:**
- **Built** means it's in the place in Edit. Nothing here has been played.
- **Measured** means it comes from the sim or from Allen's timed playtests (`Development/sim/timings.json`, 2026-10-29).
- **Hypothesis** means it comes from the research or is my reading. It needs a playtest.

## Short answer

- **Most of what the research asks for is already in the game.** The display choice exists as the Showcase Stands. The craft choice is polish and etch, and both pickers show "now → after" coins. Commissions exist as mail orders and deliveries, and both show their pay before you accept. Upgrades come as several chains at once.
- **The gap is where a sword ends up.** Before this pass, a sword that an open letter wanted looked like any other sword everywhere outside the mail. Delivery Auto-fill packed the cheapest swords first, so it could put a quest sword in a crate at 0.8× its value. That sword was worth 1.2–3.7× plus gems as the letter's answer. The ore already had "<sender> wants this!", but the sword never did. **This pass fixes that** (below).
- **The late game is the biggest open problem.** It's already in [[Design/Economy and Progression Review — 2026-11-08]]: from about 10 h on, engaged players only buy Ore Slots and merges. That needs new content (Legendary Commissions), not new friction.

## Why players would enjoy each part (hypotheses, with what supports them)

| Pleasure | What the game gives now | Read |
|---|---|---|
| Crafting | 10 strikes with sparks that build, the ingot shaped on the anvil, the hilt seat clang, scrubbing grime off, a hold-to-etch show, a "now → after" value at every step | Strong. The step-by-step value cards are the competence feedback the research asks for |
| Progression | Pads that build the workshop where you can see it; the next sword's pad fills a bar toward its price; crew who walk and work | Strong for about the first 10 h (sim) |
| Collecting | A Book of 42 metals plus the swords, NEW cards with a gold star, secret swords by surprise letter, ??? cards | Good. Rarity changes how a sword looks (textures), not only its value, which answers the research's worry |
| Ownership | Showcase Stands on the street, the shop shine, your name on the Upgraded Store's sign; Decorate is hidden for a later release | Middling. Showcase is the only place a sword is kept on purpose |
| Optimisation | Choosing chains, picking rare ore, merges, the cart, the Cashier slider, crew placement | Good in the mid game; thin after the Seraph |

## The five choices, tested for trade-off, consequence and feedback

### 1. Sell or display

- **Now:** Showcase Stands 1–3 hold one sword each and never sell it. Each adds walk-in pull (`Shared/Showcase`): metal tier 2–10%, +1% for each sword-type step past the first, +1% polished, +1% etched. The stands add up. The picker shows each sword's pull, strongest first. You can take a sword back off a stand.
- **The trade-off is real (measured from the prices and pulls):**
  - A plain Iron Katana gives +4% and gives up about 370 coins of sale.
  - A polished, etched Gold Katana gives +10% and gives up about 2,260.
  - At 1,000 coins a minute, with the shop short of customers, they pay back in about 9 and about 20 minutes. So "my best sword" and "the best deal" are different swords. That is a real curation choice.
  - Pull does nothing once the shop has more customers than swords.
- **Gap:** the Showcase picker shows the pull but not what the sword would sell for, so the cost can't be seen. *Proposal P2.*
- **Validate:** in Play, put two swords up and see whether the picker gives enough to choose between them. Later, track how often swords are placed on stands and how long they stay (an analytics event; not built).

### 2. Quick or premium craft

- **Now:** polish is ×1.10 on the whole value (×1.13–1.20 with Polish Boost). Etch is +15 / 20 / 25%, added with the hilt and seat bonuses. Both pickers show "now → after" coins. Auto Etch and the crew take over the routine work later.
- **Measured hand times:** forge 10.8 s, polish 6.2 s, etch 2.2 s, plus about 4 s of walking for the two stations. Polish now takes three passes (2026-11-07), so it's probably slower than 6.2 s; that hasn't been timed again.
- **Economy check:** the premium route (polish + etch) adds about 12–18 s for ×1.23–1.44 value.
  - **The shop is short of customers** (walk-ins 45–75 s at base, about 1 a minute, while a hand smith makes about 2 swords a minute): value per sword decides income, so premium wins by 23–44%.
  - **The extra sword goes to the cart at 0.8×:** the same 15 s makes about half a quick sword, worth about 40–48% of a sword's value. That's level with the premium gain.
  - **So the choice is real but close.** It depends on demand, which is what the research wants. I'd add no cost and no friction (hypothesis). Do time the three-pass polish in the reference run.
- **Gap:** none to build. The quick route's coins a minute isn't shown anywhere, and it doesn't need to be. Players can feel it.

### 3. Use valuable ore now or save it

- **Now:**
  - Pulls are free and unlimited, and nothing limits what you carry or rack.
  - A rolled ore that an open letter names says "<sender> wants this!", and Auto-Roll can stop on quest ores.
  - Since 2026-11-08 a letter's metal rolls at the normal odds after the tutorial. Letters lean toward commoner metals you've already collected.
- **Read:** saving costs nothing, so there's no dilemma. The research says not to manufacture one. The only real choice is *which sword the rare ore becomes*, and the anvil card already shows the finished price before you forge.
- **Gap:** none for ore. The same gap appeared one step later, on the finished sword (choice 4).

### 4. Which commission, and which sword answers it

- **Now:**
  - **Mail orders** ask for one of your top three swords in one metal (sometimes etched). They show the exact coins and gems. Accept or Decline, no expiry, 2–7 open at once.
  - **Deliveries** are Bulk (any sword, 0.8×) or Special (a twist). They show the pay (~ before packing), reputation and gems. Skip and Accept.
  - **The quest board** ticks a slip when a sword in your bag fits.
- **The trade-off (measured from `Shared/Orders`, `Deliveries`, `Customers`):**

| Where a fitting sword goes | Pays |
|---|---|
| The letter | 1.2× its value, at least a typical metal, × the shop boost (1.0–3.1×) = **1.2–3.7×**, + 2–6 gems |
| A regular customer | 1.15–1.5× |
| A VIP | 2–3.5× |
| The cart | 0.8× |

  - Early on, a VIP can beat a letter. Late, the letter wins by far. That's a real choice, with the pay shown on both sides.
- **Gap (now built):** nothing outside the mail said a sword was spoken for. The places a sword can leave by were the shop holder, the Showcase, the Sword Rack (where the Stocker sells it on) and the cart, where Auto-fill packs the cheapest first. The sim already assumes players hold quest swords back (`"order" not in s` in `engine.py`), so the game now does what the sim models.

### 5. What to upgrade next

- **Now:** chains, with the 3 cheapest new ones open and any started chain always showing its next pad:
  - speed: Heat, Furnaces, Strikes;
  - value: the sword chain, Polish, Etches;
  - capacity: Shop, Parking, Showcase;
  - automation: Crafters, staff;
  - luck: Ore and Merge.
  
  Pads show their sword's silhouette, a lock with what they need, and one-line labels near them.
- **Read:** several real priorities exist in the first hours (sim: casual players buy cheap pads first, efficient ones head for swords, and both are viable). After the Seraph only Ore Slots and merges are left, so the branches end in one optimal loop. That's finding 1 of the 2026-11-08 review.
- **Gap:** late content. *Proposal P4* (already open).

## Onboarding and routine work

- **Tutorial:** measured. Allen finished it in 1:57; the sim gives efficient 2:01 and casual 2:24. It teaches roll, heat, forge, sell, polish, letter and gem buy, and ends on a buy. That fits the research's "complete the loop, show one visible improvement".
- **First goals:** from the sim. Katana at 0:07–0:22, Sword Crafter at 0:16–0:37. The first hour is healthy.
- **Routine work:**
  - Hand crafting stays (10 strikes, scrubbing).
  - The crew takes it over from about 15 min, and passes can automate the anvil, etch and roller.
  - Polishing grew to three passes on 2026-11-07, and that's the step most likely to feel like a chore (hypothesis). Time it in the reference run before changing anything.
- **Later goals:** thin after about 10 h for engaged players. Same as above.

## Built in this pass (Edit, not played)

**Quest marks.** A sword that an open letter or mail order wants is now marked, and Auto-fill leaves it:

- `Shared/Orders.wantedBy(state, sword)` returns the giver of an open story letter (offered or active) or mail order that the sword fits, or nil. These are the same letters the mail's Send offers it to.
- **The Sword Holder and Showcase Stand pickers** (`ShopController`): the card's chip reads **Quest** in dark orange (`ItemPicker.CHIP.Quest`), with the glowing edge.
- **The Sword Rack's Store and Take pickers** (`RackController`): the same mark. Stored on the rack, the Stocker would sell the sword. On the rack, a crafter's sword that fits a letter now shows, so you can take it and send it. `RackService`'s list view now includes `polished` and `percent`, so the story letters' polish rule is checked there too.
- **Deliveries' packing page** (`DeliveryController`): the card's rarity chip reads Quest. **Auto-fill skips quest swords** and greys out when only quest swords are left. A tap still packs one.
- **No change to saves, remotes, prices or the sim.**

## Proposals for Allen (not built)

| # | What | Why | Size / risk |
|---|---|---|---|
| P1 | **The Stocker and Store all skip quest swords**, and the mail's Send also offers rack swords | GDD §10.4 already says the Stocker "preserves swords reserved for commissions". Today a crafter's sword that fits a letter is stocked and sold at 1.15–1.5×. Skipping it alone would hide it on the rack, because the mail counts only the bag, so both halves go together | Server (EmployeeService, RackService, ShopService's fill). Medium |
| P2 | **The Showcase picker shows the sale value beside the pull**, e.g. "+10% · 2,260" | Makes the cost of displaying visible (choice 1) | Client text. Small; needs a phone-size render |
| P3 | **Keep a sword:** a lock on a sword in the bag that every picker, Auto-fill, Store all and the Stocker respect | The research's "keep rather than sell" and its ore lock; lets players keep favourites | A new save field (`roblox-data`). Medium |
| P4 | **Legendary Commissions as the next content build** (already open, [[Design/Major Updates Plan — 2026-11-07]]) | Late goals: the only fix for the post-Seraph loop that doesn't slow casual players | Large |
| P5 | **The quest's reward on the Quest chip** ("Quest · 3,100") | The opportunity cost at a glance where the sword would otherwise go | Client. Small, but the chip gets longer: render it first |

## Research points not adopted

- **Passive income from displays:** the Showcase already earns through walk-ins. A second payout would stack, and would need the research's payback modelling.
- **Deadlines on orders:** Allen's letters never expire (decided 2026-10-22). That's kept.
- **Costs on polish or etch to "make a dilemma":** the trade-off is already close (choice 2).
- **Upgrade branches that exclude each other:** Allen's rule is one chain per effect, and every chain can be maxed. That's kept ([[Design/Decisions Log]], 2026-10-31).

## What to test (Allen, Play)

1. Accept a mail order for a sword you can make, then make it.
2. Open a Sword Holder and a Showcase Stand. The sword shows **Quest** with a glowing edge; other swords show coins or pull as before.
3. Store it on the Sword Rack, then open Take. It shows Quest there too.
4. With the cart's Bulk order open, press Auto-fill. The quest sword stays out. Tap it and it packs.
5. Send the sword from the mail. Its Quest mark is gone everywhere.

Related: [[Design/Tycoon Psychology and Meaningful Choices - 2026-11-09]] · [[Design/Economy and Progression Review — 2026-11-08]] · [[Design/Shop Pricing and Showcase Proposals — 2026-11-01]] · [[Sessions/2026-11-09#Quest marks on swords a letter wants]]

## P2 grown: Showcase swords as shop buffs (Allen, 2026-11-09; not decided)

Allen: "the display stand is basically a store-wide buff right, currently we're talking about pull, but it could really be anything? like certain ones could offer more gold generation, or higher ore luck, or more gem luck, or more of whatever stats are in our game. the only question is how do we decide on this."

**Claude's proposal:**
- **What decides which stat:** the sword's **metal family**. Rarity, sword type, polish and etch keep deciding how much, the way pull is worked out today.
- **The stats:** use only ones the game already has and shows on Store › Stats:
  - Customers (today's pull)
  - VIP chance
  - Mail (time between letters)
  - Crew speed
- **Left out:**
  - ore luck: merging is the only luck (2026-10-25), and Lucky Ore's odds panel shows only permanent luck;
  - gems: a Robux currency, and gems already pile up late;
  - plain coins or sale price: it would beat every other stat, and VIP sells +10% a sale.
- **How the numbers get set:**
  1. Allen picks the families and the metal → family table.
  2. The sim compares three stands of each family at 1 / 4 / 10 h.
  3. The target is that each family is the best pick at some stage and none at every stage.
- **The picker and stand show** the family's icon, the amount and the sale value (P2).
- **No save change:** the buffs come from swords already on the stands.

Open: the families, metal or another key (etch pattern, a fixed stat per stand), and whether luck is wanted despite the 2026-10-25 rule.

## Showcase buffs: the metal decides (Allen, 2026-11-09)

Allen picked **"Its metal family"**: the sword's metal decides which stat a Showcase sword boosts, and rarity, sword type, polish and etch decide how much. The four stats are Customers, VIP chance, Mail and Crew speed, as proposed above (ore luck, gems and coins left out).

**Draft metal → family table (Claude's, for Allen to edit):**

| Rarity | Customers | VIP | Mail | Crew |
|---|---|---|---|---|
| Common | Iron, Copper, Stone | Marble | Pewter | Black Iron |
| Uncommon | Bronze | Brass | Amber | Steel, Gunmetal |
| Rare | Jade | Silver, Rose Gold | Ice, Amethyst | Blue Steel, Obsidian |
| Epic | Emerald, Runestone | Gold, Ruby | Sapphire, Air | Damascus, Magma Steel |
| Legendary | Sunsteel, Mythril, Bloodmoon | Rainbow Alloy, Diamond, Prism | Starmetal, Raijin, Doppler | Dragonsteel, Soulfire, Infernal, Oni Steel |
| Secret | Watermelon | Rubber Duck | Cardboard | none |
| **Metals** | 11 | 10 | 10 | 11 |
| **Share of rolls at base luck** | ~38% | ~19% | ~19% | ~24% |

**Why it's laid out this way:**
- **Themes:**
  - Customers: plain everyday metals, plus Sunsteel (Sunshine weather brings customers) and Watermelon (festival food);
  - VIP: precious metals and gems, plus Rainbow Alloy (the Rainbow weather brings VIPs);
  - Mail: sky, water and travel, plus Ice (Snow brings mail) and Cardboard (parcels);
  - Crew: forge, fire and hard work.
- **Every family has a Common and an Uncommon metal,** so a new player can fill any stand.
- **Customers rolls most often,** because it's the stat that matters when Showcase 1 arrives. Crew matters later, once crafters are hired.

**Starting strengths for the sim (to be tuned):** a sword's points are today's pull (2-16).
- Customers: 1 point = walk-ins 1% sooner (today's rule).
- VIP: 1 point = +0.2 percentage points of VIP chance.
- Mail: 1 point = 1% less time between letters.
- Crew: 1 point = crew work 1% faster.

**Next:**
1. Allen edits the table.
2. The sim runs three stands of each family at 1, 4 and 10 h. The target is that each family is the best pick at some stage, none at every stage, and three full stands stay at or below the Promoter's effect.
3. Build, then a UI audit at phone size.

## Are some Showcase stats better than others? (Allen, 2026-11-09)

Allen: "aren't some of the stats better than others, for example higher vip chance is probably a better stat for the most part than customer increase no? also is this the exhaustive list of what stat boosts we can have?"

**Yes. At the same rate per point, VIP chance would beat Customers, because it pays in both of the shop's states.** The math (live `Shared/Customers` and `GemUpgrades`):
- **What a sale pays:** a regular pays 1.15-1.5x a sword's value (about 1.35x on average), a VIP 2-3.5x (about 2.75x). The VIP chance is 5-15% from More VIPs, and the Rainbow multiplies it.
- **+1 percentage point of VIP chance** is about +1.0% on every shop sale, whatever state the shop is in.
- **+1% sooner walk-ins** is about +1% sales, but only while the shop is waiting for customers. Once the shop has more customers than swords, it gives nothing.

| Stat | Shop waiting for customers (early-mid) | Shop waiting for swords (late) | Pays in |
|---|---|---|---|
| Customers | strong | nothing | coins |
| VIP chance | medium | medium | coins |
| Crew speed | little | strong | coins |
| Mail | small | small | mostly gems (2-6 a letter) |

- **The draft's 0.2 pp a point had VIP at a fifth of Customers,** so VIP was the bad pick, not the best one.
- **Revised starting rule:** the specialists (Customers, Crew) pay 1% a point in their own moment. VIP is the all-rounder at **0.5 pp a point, capped at +10 pp from all stands.** It's added after the VIP pass and the Rainbow multiply the base, so payers don't get it doubled, and so VIPs stay special (the cap keeps them under about 1 in 4 customers).
- **Which pays most then depends on the stage:** Customers early, Crew late, VIP a safe pick in between, Mail for gems. The sim checks this.

**The four stats are not every stat the game has.** The full list, sorted:
- **In:**
  - walk-ins sooner (Customers);
  - VIP chance;
  - time between letters (Mail);
  - crafter speed (Crew).
- **Possible:**
  - cart pay or trip time ("Cart", the volume-seller playstyle);
  - furnace heating time ("Forge");
  - letters at once;
  - letter coins;
  - the More raise chance;
  - polish and etch bonus (these two overlap Polish Boost and the etch chain);
  - how fast the crew levels (gem levels are a sink).
- **Out:**
  - ore luck: merging is the only luck, and Lucky Ore's paid odds;
  - plain coins or the regular offer size: the 50% More Coins and VIP passes, and coins would be the right pick every time;
  - walk speed: the Swift Boots pass;
  - gems: sold for Robux;
  - customers at once: Allen's cap of 8;
  - cart capacity and Faster Strikes: bought chains;
  - weather: it's server-wide;
  - reputation: does nothing after Rank 5.

Claude's pick: keep four for now, so the stand icons stay readable for 9-16, with Cart as the first fifth if deliveries need a reason.

## The left-out stats, reconsidered (Allen, 2026-11-09)

Allen: "the ones you left out, some are viable. just because i made decision before doesn't mean we shouldn't consider them. if the odds and stats are done correctly, the game passes and purchases can still be viable, while also offering players something to grind for"

**The rule that keeps passes worth buying:** a family's best (three top swords) is at most **half** of the pass it overlaps, and it stacks with the pass, never replaces it.

| Stat | Viable? | How | Cap (3 stands) | What to watch |
|---|---|---|---|---|
| Ore luck | Yes, as a chase family | Luck added like a merge's | +0.25 luck (Lucky Ore is +0.5) | Odds: Lucky Ore's panel and the Ore Chances sign must show the odds with the stands' luck; it snowballs (more luck, rarer ore, stronger luck swords) until the cap. Supersedes "merging is the only luck" (2026-10-25) for stands only, if Allen agrees |
| Coins | Yes, weak | % on all coins earned | +15% (the pass is +50%) | An all-rounder like VIP, so keep it below VIP's worth |
| Walk speed | Yes | % walk speed | +12% (Swift Boots is +50%) | Feel; check the Swift Boots card's "50% faster" still reads right stacked |
| Gems | Yes, small | +1 gem on a letter or cart trip, by chance | about +1 gem in 3 hand-ins | Gems pile up late (the 11-08 review); best early |
| Past a maxed chain | Yes | Cart capacity +1-3 crates; strikes or heating a little past Lv. max | per chain | Late grind; the chain's own levels stay the way to get most of it |
| Bigger regular offers | Maybe | Offer range up | small | Overlaps the VIP pass's +10% a sale and VIP chance: two all-rounders already |
| Customers at once | No | | | Performance, not the old decision: about 140 Humanoids on a full server (Performance Audit 2026-11-07) |
| Weather | Only as "your shop gets more from it" | e.g. Sunshine x2 -> x2.3 for you | small | Weather is server-wide; a stand can't change other players' weather |
| Reputation | Not yet | | | It does nothing past Rank 5; viable once ranks do something (Legendary Commissions) |

**How it fits the metal table:** about 8 families is more than there are early metals (11 Common and Uncommon). So:
- **Early families** each get a Common or Uncommon metal: Customers, VIP, Mail, Crew.
- **Chase families** come only from Rare and up (Luck, Coins, Walk, Gems, and the past-max ones). They're the grind Allen wants: a reason to roll, merge and keep a Legendary.

**Next:** Allen picks the families; Claude redrafts the table with early and chase families; the sim checks the caps against each pass's own payoff (the Monetization Plan's hours to Rin); then the build.

## Showcase families, redraft 2 (Allen: "Yes, redraft", 2026-11-09)

Ten families: four **early** ones, which Common and Uncommon metals give, and six **chase** ones, Rare and up only. Every metal is in exactly one family (42). Supersedes the first draft table above.

| Family | Common | Uncommon | Rare | Epic | Legendary | Secret | Share of ore at base luck |
|---|---|---|---|---|---|---|---|
| **Customers** | Iron, Copper, Stone | Bronze | | Emerald | Sunsteel | Watermelon | 35.6% |
| **VIP** | Marble | Brass | Silver | Ruby | Rainbow Alloy, Bloodmoon | | 17.1% |
| **Mail** | Pewter | Amber | | Sapphire | Starmetal | | 15.6% |
| **Crew** | Black Iron | Steel, Gunmetal | | Damascus | Oni Steel | | 20.6% |
| **Luck** (chase) | | | Jade | Runestone | Doppler, Prism | Rubber Duck | 2.1% (1 in 47) |
| **Coins** (chase) | | | Rose Gold | Gold | Mythril | | 2.0% (1 in 50) |
| **Swift** (chase) | | | Ice | Air | Raijin | | 2.0% (1 in 50) |
| **Gems** (chase) | | | Amethyst | | Diamond | | 1.5% (1 in 66) |
| **Forge** (chase) | | | Obsidian | Magma Steel | Soulfire, Infernal | | 2.1% (1 in 48) |
| **Cart** (chase) | | | Blue Steel | | Dragonsteel | Cardboard | 1.5% (1 in 65) |

"Share of ore" is per ore result at base luck (a pull gives one to six). Merges and Lucky Ore raise the chase shares.

**Themes:**
- Customers are everyday metals, plus Sunsteel (Sunshine brings customers) and Watermelon (festival food).
- VIP are the precious ones, plus Rainbow Alloy (the Rainbow brings VIPs).
- Mail is sky and travel. Crew is hard work.
- Luck is charms: Jade, runes, rainbow Prism and Doppler, a lucky Rubber Duck.
- Coins is gold. Swift is ice, air and lightning (Raijin). Gems are the gemstones.
- Forge is fire and black glass. Cart is the sturdy ones, plus Cardboard (boxes).

**Strength:** a sword's points are today's pull formula. Metal tier: Common 2, Uncommon 3, Rare 4, Epic 6, Legendary 8, Secret 10; +1 a sword-type step; +1 polished; +1 etched. That's 2-16 points. The three stands' points add up within a family, then the cap applies.

| Family | Per point | Cap from all stands | Overlaps | Pass check |
|---|---|---|---|---|
| Customers | walk-ins 1% sooner | none (today's rule) | Promoter, Better Advertising | none |
| VIP | +0.5 percentage points of VIP chance, added after the pass and Rainbow multipliers | +10 pp | More VIPs, VIP pass (x2) | the pass's x2 stays the bigger step |
| Mail | 1% less time between letters | -30% | Quicker Mail | none |
| Crew | crew work 1% faster | +30% | crew levels | none |
| Luck | +0.01 luck | +0.25 | merges, Lucky Ore (+0.5), Rain | half of Lucky Ore; both odds panels show it |
| Coins | +0.5% coins | +15% | 50% More Coins | under a third of the pass |
| Swift | +0.5% walk speed | +12% | Swift Boots (+50%) | under a quarter of the pass |
| Gems | +1% chance of +1 gem on each letter or cart trip | 33% | | about +1 gem every 3rd hand-in |
| Forge | heating and strikes 0.5% faster | +10% | Heating I-III, Faster Strikes, Auto Anvil | past max; the chains stay the main gain |
| Cart | +1 crate per 14 points | +3 crates | Cart Capacity (6-15) | past max |

**To check in the sim:**
1. Three stands of each family at 1, 4 and 10 h, for casual and efficient players.
2. No family is the best pick at every stage.
3. Each pass still pays in hours saved (the Monetization Plan's "hours to Rin") with full stands.
4. Luck's loop: luck finds rarer metals, which make stronger luck swords. Check it stops at the cap.

**Not decided:**
- the families and the metal for each;
- every number above;
- the family icons;
- whether Customers keeps "every sword pulls customers" (in this draft only Customers metals do).

## Teaching the Showcase, and when it comes (Allen, 2026-11-09)

Allen: "we also need to decide then how to inform the player of this mechanic. would we introduce the display rack at the beginning as tutorial? or once they buy the display rack? if then would we want to introduce the sword display into the progression sooner?"

**When it comes now (sim, 10 seeds each, free players, medians):**

| | Display Table 1 (440) | Showcase 1 (3,000) | Showcase 2 (25,000) | Showcase 3 (90,000) |
|---|---|---|---|---|
| casual | 9 min | 43 min | 3 h 30 | not by 6 h |
| efficient | 22 min | 1 h 00 | 3 h 31 | 5 h 45 (2 of 10) |

**The moment it misses:** Beginner's luck (+9, 2026-11-01) makes the first pull after the tutorial very likely Rare or better (Epic 40%, Legendary 10%). So every player gets a special ore about 2-3 minutes in, and today nothing gives it a use but coins for about 40 more minutes.

**Claude's proposal:**
- **Not in the opening tutorial.** It's 1:57 now and ends on the gem buy. A stand there would be a step before the player knows why, and against the guidance rules (spotlight only on a real step; no step you can't use yet).
- **Bring Showcase 1 earlier:**
  - a few hundred coins (about 600-1,000; the sim sets it), right after Display Table 1, so it lands at about 10-20 min;
  - that's near the first special ore and the Sword Crafter (about 15 min);
  - Showcases 2 and 3 stay late goals.
- **Teach it when it's bought, once,** the way the Ingot Rack step after hiring Taise works:
  1. The pad's one-line label (as every pad).
  2. On buying, one Guide line, "Put a sword on the stand", with arrows to it, until a sword is on it. It's optional: it ends after a while or when the player walks away.
  3. **The picker teaches the families:** each card shows its stat's icon and amount ("+6% Customers"), strongest first.
  4. **The stand's label** (already shown when you're close) shows its stat's icon and amount, and Store › Stats shows the total.
- **The Book shows each collected metal's stat icon,** so players learn the families by collecting, with no text.
- **Not proposed:** popups, toasts, or a card per family.

**What the sim checks:** whether an earlier Showcase 1 at 600-1,000 delays the Sword Crafter (target about 15 min) or the Katana, and what keeping a sword instead of selling it costs a new player in the first 30 min.

## Showcase families in the sim (2026-11-09)

Allen: "Run the sim". The full tables are in [[Development/Sim Runs/showcase-families-2026-11-09]].

- **Only four families move income.** The sim's shop is short of customers for all 10 h, so Customers, VIP, Coins and a little Luck pay. Crew, Forge, Swift, Cart, Mail and Gems stay within about ±3% of nothing, even with Crew doubled.
- **Redraft 2's Customers wins every stage** (+80% late for casual players). Capped at 20%, with Coins at 8% and Luck at 0.15, efficient players have a real choice: Customers is best at 1-4 h, VIP at 4-10 h, Coins close behind. Casual players still get the most from Customers late (+36%).
- **The passes stay well ahead of full stands:** Coins +13% against +88%, VIP +14% against +44%, Swift +1.5% against +18%, Luck about 0% against +3%.

**Claude's recommendation:** six families, not ten.
- **The four that pay:** Customers (cap 15-20%), VIP (0.5 pp a point, cap +10 pp), Coins (cap 8%) and Luck (cap 0.15; its pull is collecting rarer metals, not coins).
- **Swift:** kept for feel. Walking faster is felt at once, even if coins barely move.
- **Mail:** shorter letters and the gem chance in one family.
- **Crew, Forge and Cart's metals** move into these six. Those three pay nothing while the shop is short of customers, and a stat that sounds strong but does nothing is a trap pick.

## Showcase families: built (2026-11-09)

Allen: "just do 6 for now, maybe later we can add more". Built in Edit, not played: [[Sessions/2026-11-09#Showcase families built: six stats by metal]]. Final sim: [[Development/Sim Runs/showcase-families-2026-11-09#Run 4: six families on the new walk-in rate]]. Not built yet: the stat icons in the Book.

# LihFolk Vault Review — 2026-10-30

Allen: "take a look and see what useful information may apply to our tycoon game. Our is not a typical dropper tycoon game keep in mind. But look at anything involving tycoons and game economy and progression".

**Source.** About 45 notes from `C:\Users\Allen\Downloads\LIH.FOLK.VAULT.V2.FULL\LihFolk Vault V2\LihFolk Vault V2`, read by three readers:
- economy and pricing (folders 09, 10, 11, 40, 48, 52)
- tycoon and retention (10, 24, 43, 47, 57, 58)
- monetization and case studies (11, 32, 38, 49, 59, 60)

**Caveat.** Many of the vault's numbers come from one RNG combat game it calls the "reference project", or are its rules of thumb. Treat them as starting points, not tycoon data. Nothing here is decided; these are proposals to weigh against the [[Design/Decisions Log]].

## Progression and pacing

- **Price in minutes of income.** `T = price / income at the moment it becomes relevant`.
  - Bands: small 1–3 min, meaningful 5–15 min, big unlock 15–45 min.
  - The first ring of buys costs 1–2 min; capstones cost 1–2 h.
  - The vault's lesson from a hand-priced item that came out 10x off: "fix the model, then derive every price from it again." (Economy Inflation Sinks and Faucets Math §1; Progression Levels and Unlocks §3)
- **Plot the wait along the pad chain.** `wait(k) = cost(k+1) / R(k)`, where R(k) is income after k buys.
  - "Spikes are where players leave."
  - Early waits stay under ~2 min; late waits 5–10 min.
  - After any long wait, the next buy should be a "spectacle" one: something big to look at, not just income. (Genre Playbook - Tycoons §3, §9)
  - Our sim can draw this per archetype.
- **Sawtooth pacing.**
  - The time to afford the next buy should rise slowly within a stretch, then drop at a milestone. For us the milestones are each new blueprint and the Sword Crafter.
  - Only the ratio of price growth to income growth matters. Anchor on the Zanbatō at ~4 h and the Seraph at 10–14 h. (Progression and Pacing Design §1, §4)
- **A near goal and a far goal at every stage.**
  - One thing should be 1–5 min away and another hours away.
  - Keep 1–3 buys available at once, next to the last build.
  - The reference project added a Next Goal tracker with a trail and a small payout per goal, after players felt "thrown in the game without knowing what to do".
  - This backs the pinned next goal for casual players. (Core Loops and Session Design §7)
- **Walls need two ways past.**
  - The reference project lost 82% of players at a gate with only one route.
  - For a casual player, the Zanbatō and Seraph gates could open a second route through mail orders or the cart.

## The simulator

- **Session shape.** The vault's archetypes:
  - casual: 55% of players, 0.8 sessions a day of 12 min (exponentially distributed)
  - regular: 1.5 sessions a day of 25 min
  - grinder: 2.5 sessions a day of 55 min
  - Churn: 8% a day, +10% on days a player ends more than 60 min from their next goal.
  - Ours plays 1 h a day for everyone (Allen 2026-10-29), which hides the casual gap. At ~10 min a day, the Sword Crafter would be about 12 days in for a casual player.
  - Not changed: this would be a choice for Allen. (Simulating an Economy Before Launch §2, §4)
- **Use the sim to compare runs on the same seeds, not to predict.** Fail a check when a key metric moves more than 10%.
- **Discovery counts play days.** Playtime counts only up to 60 min per player per day; retention is ranked over Day 1, Days 2–7 and Days 8–28.
  - So the targets read better as sessions: the Seraph at 10–14 h is 10+ days.
  - Every 20–45 min session should hand out at least one visible upgrade.

## Economy health

- **Hours of income held** = coins / income per hour.
  - Healthy mid-game: under 1–2 h.
  - Late game over 20 h means there is no top-end sink.
  - The vault's no-sink sim ended with top players holding 99.3% of all coins.
  - Without rebirth, the late game needs a repeatable sink with escalating returns. (Inflation Math §4; Economies and Currencies §2)
- **Fixed rewards fade** in an exponential economy. Pay mail, orders and the daily reward as a share of the next gate's price.
  - Power per tier should be 1.25–1.5x; at 2x "each tier invalidates the last".
  - This is the stale mid-tier problem: check the value ratio between blueprints.
  - Orders and quests for older blueprints, paid at today's scale, keep them worth making.
- **Lv. 5 tracks.**
  - Players buy greedily, by benefit per coin. Fix a track nobody buys by changing its benefit per coin, not by adding prerequisites.
  - Five levels can be five fixed prices in a table.
  - Round to 2 significant figures, then check each level costs more than the one before. (Pricing Curves and Upgrade Costs §3, §5, §7, §10)
- **Payer gap.**
  - Write a maximum down, for example 3x.
  - Stack multipliers in one function: five 1.5x sources multiplied together give 7.6x.
  - Ours: 50% More Coins, VIP, Promoter, weather and the Gem Shop.
- **Rare ore odds.**
  - For a 1-in-N item: median 0.69N rolls, p90 2.30N.
  - A player's next unseen tier should be a median of 1–2 sessions away.
  - Luck shifts outcomes down by `log_r(L)` tiers; stack it additively and cap it. (Rarity Ladders and Drop Pacing Math §1–5)

## Retention

- **Offline earnings.**
  - The reference numbers: 15% of active income, capped at 8 h, nothing for absences under 5 min, nothing until the tutorial is done.
  - Compute it from a server `lastSeen`.
  - Show a "Welcome Back" count-up, sharing one card with the daily reward and the next goal.
  - Grow a Garden sells itself on "GROW OFFLINE".
  - For us the rate would come from crew output; a banked ore roll per X minutes away fits the ore slots.
  - The vault counts this among the core return hooks; ours is "later".
- **Daily reward.**
  - Our never-resetting streak is the kind shape with the weaker pull; players learn to care only about day 7.
  - A 7-day track should total 1–2 days of normal play income.
  - Reset at UTC with an offset.
  - On phones, show 3 tiles: yesterday, today, tomorrow.
- **Celebrations.**
  - Reveal length by rarity: 0.3 s for common up to 5–6 s for the top tiers.
  - First-of-a-kind and milestones (the first hire, the first Zanbatō) get the full moment.
  - Count-ups scale with the log of the amount.
  - Keep animation under ~10% of play.
- **Pop-up gate.** None in the first 180 s, none over another panel, at least 8 s apart, and at most one unprompted Robux offer in a non-payer's first session.
- **Rebirth.**
  - The vault calls it "the standard long loop on Roblox", but also says a reset "feels like punishment" when the long goal is collection. That backs our collection book and blueprint ladder.
  - Merge Ore Slots should follow its rules: a NOW vs AFTER panel, the multiplier growing slightly slower than the cost, and a save right after.

## Monetization (checked against [[Design/Monetization Plan]])

- **Premium Payouts ended on 2025-07-24.** Creator Rewards replaced them. Plan §"Premium Payouts" (line ~133) is out of date.
- **Roblox Plus (2026-04-30).**
  - Plus gives members 10% off, which Roblox pays for, so our share of each sale is unchanged.
  - The 135/180/90/270 quotes are list × 0.9, which suggests Allen's account has Plus.
  - Each Plus sign-up through our prompt pays 250 R$ a month for 3 months.
- **Regional pricing** has been on by default for passes since 2026-03-30. Check each pass in Creator Hub before release.
- **A custom 16:9 thumbnail** has been required for Home recommendations since 2026-10-19.
- **Price ladders.** Value per Robux should rise with smaller jumps toward the top. Ours grow toward the top:
  - gems: 0.78 → 1.11 per R$
  - coins: 89 → 300 per R$
- **Size of the store.** The vault says start with 3–5 passes; we have 6 passes and 17 products.
- **50% More Coins (199 R$) is the core-loop pass but costs less than VIP (299 R$).** The vault prices the core-loop pass highest.
- **Odds disclosure.**
  - Lucky Ore, Rain and merges should feed one `EffectiveLuck` value that the roll and the odds panel both read.
  - Odds shown must update while a boost is active, including weather someone else bought.
  - Rainbow raises the VIP chance from 5%, so show its before and after chance.
- **"Not enough coins" pack offer:** give it a cooldown and a cap per session.
- **The 500-gem pack is more than the whole Gem Shop costs (325).**

## Doesn't apply

Dropper parts, conveyors, upgraders and collector pads; plot auto-assignment; raids and PvP; trading and markets; seasonal wipes; event currencies (until events exist); ad payback; experiments (they need ~1,000 DAU).

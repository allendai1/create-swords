# Pacing check, 2026-10-30

The waits between buys in run [[Development/Sim Runs/prices-2026-10-30]] (today's live prices, 150 free players a type). This is the check suggested by [[Design/LihFolk Vault Review — 2026-10-30]]: keep the wait between buys under ~2 min early and 5–10 min late, because "spikes are where players leave". Biggest unlocks are allowed 15–45 min.

## Buys per hour of play (median player)

| Type | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Efficient | 34 | 24 | 20 | 15 | 13 | 7 | **4** | 8 | 6 | 9 | 4 | 9 |
| Manager | 37 | 21 | 18 | 15 | 12 | 8 | **3** | **2** | 7 | 9 | 4 | 8 |
| Grinder | 36 | 19 | 17 | 12 | 15 | 9 | 7 | 5 | 6 | 5 | 7 | 3 |
| Automator | 32 | 10 | **5** | **4** | 8 | 9 | 8 | 9 | 7 | 8 | 6 | 3 |
| Casual | 24 | 13 | 10 | 9 | 8 | 4 | 7 | 3 | 3 | 7 | 4 | 7 |

## What it shows

**The first 4 hours are on target for good players.** Median waits are 1–3 min. The longest single waits are 7–9 min, for the Cutlass, Dadao, Mei and Zanbatō.

**After the Zanbatō, good players hit a trough.** From about 5 h, efficient and manager players buy 2–4 things an hour, against 13 in hour 4. Almost every pad is bought by then. What's left are the fictional blueprints, each the only thing to save for, at 20–30 min of income apiece:
- Hook Sword 25 min
- Crescent Fang 24
- Shard Blade 23
- Moonbite 24–31
- Serpent 24–30
- Leviathan 21–23
- Seraph 20

**It's a flat chain, not a sawtooth.** Each wait matches price ÷ income at the time (within 1–2 min), so the player is saving for that one blueprint. Each blueprint raises income by about as much as the next one costs more, so the wait never drops after a milestone.

**Automator players stall early.** Hours 2–3 bring 4–5 buys an hour, because they save for crew at 15–38 min each: Crafter 16, Stocker 18, Anvil4 16, PolishBoost3 30, Mei 38.

**Casual players' waits run about twice as long** as efficient players'. From 3 h they are 10–17 min (Cap2, Cutlass, Jian, Big Sword Stand, Sword Crafter, Promoter). At 1 h a day, that still gives 3+ buys every session.

Script: the inline Python in the session note (buys from `players.jsonl`, wait = time since the previous buy).

## Fixes simulated

Allen: "Yes, simulate the fixes." Run [[Development/Sim Runs/trough-2026-10-30]], 100 free players per type, each played until every pad is bought. Times are medians in h:mm; the last three columns are counts of buys or waits in minutes. Check any run with `python pacing.py <run>`.

**Scenarios:**
- `late70` / `late50`: the 8 fictional blueprints (Hook Sword to Seraph) at 70% / 50% of their price.
- `-west`: the Western swords worth more than the Dadao (Gladius 360, Khopesh 400, Rapier 450), so good players buy them in the trough.

| Scenario | Type | Seraph | Last pad | Fewest buys in an hour | Waits over 15 min | Longest wait |
|---|---|---|---|---|---|---|
| baseline | efficient | 10:51 | 11:57 | 3 | 14 | 31 |
| late70 | efficient | 8:40 | 10:37 | 4 | 11 | 25 |
| late50 | efficient | 7:07 | 9:35 | 6 | 7 | 22 |
| late100-west | efficient | 14:05 | 14:05 | 3 | 19 | 43 |
| late70-west | efficient | 9:02 | 10:33 | 4 | 10 | 22 |
| baseline | manager | 11:11 | 12:20 | 2 | 15 | 34 |
| late50 | manager | 7:19 | 9:59 | 4 | 8 | 22 |
| baseline | casual | 25:38 | 25:38 | 1 | 43 | 49 |
| late50 | casual | 19:50 | 20:06 | 2 | 34 | 39 |

The Sword Crafter is unchanged in every scenario: efficient 2:01, manager 1:41, casual 4:20.

**What it shows:**
- **Cheaper fictional blueprints fix the trough only by shortening the game.**
  - At half price, efficient players' waits over 15 min halve (14 → 7) and the worst hour has 6 buys, not 3.
  - But the Seraph comes 3 h 45 sooner (7:07), and the last pad 2 h 20 sooner.
- **Worth-more Western swords make it worse.**
  - Efficient players buy the Gladius at 4.8 h and the Rapier at 6.4 h.
  - The Rapier (450) is then worth more than the Hook Sword (430), so the fictional chain waits until 12 h. The Seraph comes 3 h later.
- **Casual players' waits are long all game, not just after the Zanbatō** (43 waits over 15 min). Late prices barely touch that.
- **Conclusion: the trough is the game's length.** About 13 lone 20–30 min saves are what carry good players from 5 h to 11 h. To fix it without shortening the game, the 5–11 h window needs more things to buy between the blueprints: new pads or upgrades priced at 5–10 min of income there. Cheaper prices can't do it.

## One sword chain instead of branches

Allen: "Would merging all the swords into one upgrade system help instead of them branching off".

Run [[Development/Sim Runs/one-chain-2026-10-30]], same seeds. `one-chain` puts every non-big sword in one line by value: Wakizashi, Machete, Katana, Scimitar, Longsword, Cutlass, Falchion, Jian, Gladius, Khopesh, Dadao, Rapier, Hook Sword … Seraph. Today's 20 blueprint prices are handed out low to high along it. The first six keep their price; the changes are:
- Falchion 28k, Jian 50k, Gladius 60k
- Khopesh 150k, Dadao 160k

The Zanbatō waits on the Gladius (now 60k, the Dadao's old price); the Claymore waits on the Rapier.

| Scenario | Type | Sword Crafter | Seraph | Last pad | Waits over 15 min | Longest wait (min) |
|---|---|---|---|---|---|---|
| baseline | efficient | 2:01 | 10:51 | 11:57 | 14 | 31 |
| one-chain | efficient | 2:10 | 11:53 | 11:53 | 16 | 26 |
| one-chain-late70 | efficient | 2:10 | 10:23 | 10:48 | 11 | 24 |
| baseline | manager | 1:41 | 11:11 | 12:20 | 15 | 34 |
| one-chain | manager | 1:50 | 12:08 | 12:08 | 17 | 27 |
| baseline | casual | 4:20 | 25:38 | 25:38 | 43 | 49 |
| one-chain | casual | 4:23 | 26:39 | 26:39 | 46 | 50 |

**What it shows:**
- **One chain fixes the stale Western swords.** Every sword is worth buying when it comes up: efficient players buy the Gladius at 2.1 h, not 9.4 h, and the Seraph is the last pad. The longest wait drops by 5–7 min.
- **One chain doesn't fix the trough.** There are as many waits over 15 min, or 2 more. The game is the same length (last pad 11:53 vs 11:57).
- **The Zanbatō moves to 4.2 h** (from 3.8) and the Sword Crafter 9 min later. Both still sit near their targets.
- **With the fictional swords at 70% as well,** efficient players have 11 long waits instead of 14, and the game is about 1 h shorter. On their own, 70% prices made it 1 h 20 shorter at the same 11 long waits, because the chain puts the Western swords in front.

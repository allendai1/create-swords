---
title: Crafter Pull Options — 2026-11-02
type: design
status: answered — no pull built (Allen: "players dont necessarily have to buy the swordcrafter")
updated: 2026-11-02
tags: [proposal, crew, pacing, tutorial, create-swords]
---

# Crafter Pull Options — 2026-11-02

**Answered 2026-11-02:** none built. Allen: "players dont necessarily have to buy the swordcrafter". The 15-minute target means he's there and within reach, not that everyone buys him then. On the live game a casual player's pad for him stands at 12 min, and they've earned 2,000 since by 17 min ([[Development/Sim Runs/crafter-pull-2026-11-02]] baseline). Hiring later is their choice.

The Sword Crafter costs 2,000 with Anvil 2 since today, after the Ingot Rack and Sword Rack ([[Sessions/2026-11-02#The 15-minute Sword Crafter built]]). Engaged players now hire him at 15–20 min. Casual players hire at 34 min, because they buy every cheaper pad first. In Create Pottery, Allen walked past six cheaper pads to save for the Apprentice ([[Design/Pottery Playthrough 2026-11-02]]). Allen: "Yes, propose options" for what draws casual players to him.

## What the sim says

[[Development/Sim Runs/crafter-pull-2026-11-02]] (100 players a type, 8 h, free, seed 1; live export). Medians:

| | Casual hires at (p10–p90) | Casual buys before | Casual save for him | Engaged |
|---|---|---|---|---|
| Today | 34 min (27–44) | 18 | 2 min | 15–20 min |
| Players head for him once his pad stands (`crafter-goal`) | **17 min (12–25)** | 9 | 4½ min | 11–17 min |
| No new chain opens while his pad stands (`crafter-hold`) | 27 min (21–35) | 13 | 2 min | 15–17 min |

"Players head for him" is the best case: every player answers the cue. A real cue lands somewhere between 17 and 34 min. Holding new chains helps a little, but casual players still buy the next level of chains they've already started (Back Wall Rack, the Katana, Ore Slot 4, Ingot Rack 2) first.

## Options

What each touches: the 2026-10-29 call against a pinned goal ("no pinned goal for now", when the Longsword path got cheaper instead), and the guide rules (one cue per thing; tutorial steps only for the first letter and the Gem Shop; every guided buy needs a way on when it's unaffordable).

1. **A letter from Taise when his pad first stands (recommended).** It pops up like the story letters (countdown, mail dot) and says he's looking for work, with a short "Show me" that walks you to his pad on the floor arrows.
   - Fits the mail the game already runs on. Pottery's own hire came after phone messages.
   - It's not a pinned HUD goal, and it comes once.
   - It needs a new kind of letter with no sword to send (all letters today are commissions).
   - About an hour's work.
2. **One guide step, once, when his pad first stands:** "Hire a Sword Crafter" with the floor arrows to his pad, ending when he's hired or you walk away from the pad.
   - Reuses the Guide's pad step ("Buy …", then "Press Buy").
   - Under 2,000 it needs a way on: "Save 2,000 for a Sword Crafter" for a while, which edges toward the pinned goal you turned down.
   - About 30 min of work.
3. **Taise waits by his pad in person**, idle, with his name and "Lv. 1" overhead like the hired crew. No text.
   - The world shows the hire is a person.
   - Whether it pulls players can't be measured before a playtest.
   - Needs a pose and a spot clear of the pad. About an hour's work.
4. **Hold new chains while his pad stands** (TycoonService `standing`: no new chain while the Crafter's pad is up).
   - Measured: casual 34 → 27 min.
   - No UI, but it hides choices for ~10 min. It's also a quiet rule players can't see.
   - About 15 min of work, with the sim's `holdFor` mirrored.

Options 1 and 4 can go together. Option 1 is the cue, and option 4 stops cheaper new pads from tempting players away while they save.

## Not recommended

- **A lower price.** To be the cheapest pad around him at ~13 min he'd cost ~500, and he'd stop feeling like a milestone. At 1,500 casual players still take 22 min (`first1.5k`, [[Development/Sim Runs/crafter-15min-2026-11-02]]).

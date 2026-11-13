# Drop-off Fixes — 2026-11-12

Allen: "Yes, propose fixes" (for the two drop-off points in [[Sessions/2026-11-12#Analytics: progression pace and the simulator]]). Proposals only; nothing built.

## The numbers

**Before the first pull** (Analytics Query API, 2026-11-11 to 2026-11-12):

> **Corrected 2026-11-12 afternoon:** the funnel (players, not sessions) says phones lose **23%** before the first pull (404 joined, 310 pulled), tablets 11%, computers 16%. The 45% below divided session ends by LoadTime counts that started partway through 11 Nov. The letter step (accepted → delivered, 20% lost) is now the bigger drop: [[Sessions/2026-11-12#Analytics re-read: afternoon]].

| Platform | Sessions loaded | Left before the first pull | Load time |
|---|---|---|---|
| Phone | 223 | 100 (45%) | 9.5 s |
| Tablet | 102 | 18 (18%) | 5.7 s |
| Computer | 77 | 22 (29%) | 4.4 s |

- They leave about 36 s in (SessionEnd "Joined", 0.6 min). The players who do pull take 26 s on a phone (FirstPrompt `OreRoller/Pull lever`).
- The guide line on screen when they left: "Hold to pull the lever" for 101 of them. LoadQuit (left while loading): 9.
- The lever needs a 1 s hold (`RollPrompt.HoldDuration` 1, since the 2026-10-31 review: "a tap does nothing you can see") from within 7 studs. The plot's spawn is 10 studs from the lever, so a new player must walk before the prompt shows.

**After the tutorial:**
- 45% of joiners finish the tutorial (3 min 42 s in) and 25% reach 10 min.
- 155 first sessions end with "Bought a gem upgrade" as the furthest step, at 10.5 min. 205 of the quits after the tutorial had no guide line on screen.
- Still open from [[Design/Reviews 2026-10-31/First 10 Minutes Review]] finding 4: "After the cheer there is no next goal" (`Guide.goal` returns nil once the gem step is done). Not decided since.
- 41% of offer cards go unanswered (they wait 35 s). The review's finding 5 offered a customer-waiting chip; only the 2 s spotlight for far offers was built (2026-11-10).

## Proposals, best first

### The first 30 seconds

1. **A tap pulls the lever until your first pull.** `RollPrompt.HoldDuration` 0 for a new save's first pull, then 1 s as now. The guide says "Tap the lever" for that pull. The lever still swings (LeverAnimator gets a short swing, about 0.4 s). Small. The 2026-10-31 reason for the hold was that a tap did nothing visible; with no hold, the tap starts the roll at once.
2. **Spawn at the lever, facing it.** Move the plot's `PlayerSpawn` to about 4 studs in front of the lever, turned to face it, so the prompt is up the moment the yard loads. Small; one part in the plot template (place for the +12 push, [[plot-template-starter-layout]]).
3. **Log why the first pull doesn't happen.** One event, `FirstPull`, CF1: Pulled / HoldReleased (hold started, let go before it filled) / NeverShown (the prompt never showed) / Left. Plus the seconds from join to the yard streamed in. Tells us which of 1, 2 or 4 matters. Small.
4. **A loading screen** (your note, [[Optimizing first 1-2 minutes]]): ReplicatedFirst holds a title card until the plot and the lever have streamed in (up to about 10 s), so a phone never shows a half-built yard. Medium.

### After the tutorial

5. **A pinned next goal that follows the sword chain.** After the cheer, a small chip under the quest board: "Next: Katana · 312 / 800" with a fill bar. It names the next blueprint in the chain (Wakizashi, Katana, Scimitar, ...), turns green with an arrow to the pad when you can afford it, and moves to the next blade when bought. Medium. It never names Ore Slot 2 (Fixes2: "Don't prompt to buy ore slot 2"). The sim's note from 2026-10-29: "A pinned next goal is what moves Casual."
6. **A customer-waiting chip** (finding 5b): "Customer waiting · 28 s" on the HUD while an offer is up and you're out of range; tap to face the shop. Medium. In 2026-10-29's sim run, a shop-counter scenario got the casual player to the Gladius 44 min sooner.
7. **The next letter comes at the cheer.** A guided letter is the one goal players already follow (the first letter: 315 opened, 313 accepted). The next one would arrive with the cheer and ask for a Wakizashi, so the goal and the blueprint arrive together. Small to medium; check it against letter timing first.

## Suggested batch

1 + 2 + 3 in one update (small, and they share the first 30 seconds), then 5. Compare the funnel a day after each: phone share past the first pull (55% now) and share reaching 10 min (25% now).

## Not proposed

- Making the tutorial shorter: it's 3 min 42 s and 79% of the players who sell finish it (151 of 190).
- Moving prices: pace isn't the problem for the players who stay (a buy every 2.2 min).

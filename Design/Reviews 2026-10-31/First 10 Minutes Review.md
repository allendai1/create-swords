---
title: First 10 Minutes Review
type: review
updated: 2026-10-31
tags: [review, tutorial, ftue, onboarding, first-session, economy, create-swords]
---

# First 10 Minutes Review

A read-only trace of a brand-new player through the tutorial and the first 10 minutes after it. It covers the open Studio place (Edit mode, 2026-10-31 17:00–18:00) and the simulator ([[Development/Sim Runs/first-10-minutes-2026-10-31]]). Nothing in the place was changed and Play was never started.

**This is not a playtest.** Times for a child are estimates. They come from:
- the code's own numbers;
- paths PathfindingService found in `Workspace.Plot` at WalkSpeed 16;
- Allen's measured hand times (`Development/sim/timings.json`).

Read against:
- [[Sessions/2026-10-30]] (the evening's tutorial changes and the code review's 10 fixes, which aren't repeated here) and [[Sessions/2026-10-31]];
- the [[Design/Decisions Log]], [[Design/Pottery Tutorial Review]] and the [[Archive/Design/Urgency Review]] guardrails;
- the LihFolk onboarding notes (Onboarding and FTUE, First-Time User Experience, Onboarding by Genre) and the lihfolk-tutorial FTUE checklist and rubric.

Line numbers are as read at 18:00. Other sessions were editing `AnvilController` meanwhile, so its numbers may move.

## Verdict

- **The opening is strong.**
  - The player spawns facing the lever (3° off, 8 studs away). The first action comes at about 0:03, the first strike at about 0:30 and the first sale at about 1:10 (Pottery's is at 1:12).
  - The first upgrade, the Polishing Station, comes at about 2:30, paid from the first sale.
  - Every guide line is 2–7 words, with one line and one pointer per step.
  - Every branch I traced has a way on. **No step leaves a player permanently stuck.**
- **The weak points are at the edges:**
  - The first-sale step has no pointer once the player walks off.
  - Sending the letter turns on five things at once, Robux offers among them, while the lessons' last step (the gem buy) is still running.
  - The cheer and the first daily window collide.
  - After the cheer there's no next goal. At the same moment customers start coming about 3× less often, and about 40% of offer cards go unanswered.
- **The tutorial takes about 3:15–4:30** for a child who follows each line. The simulator with the game's tutorial rules, at Allen's hand speed, puts it at 2.4–4.0 min. LihFolk's target is under 3 min. The longest idle stretch is the second loop's 15 s heat.

## Findings, most serious first

Each finding gives: **When** · **Sees** (what the player sees) · **Why** (script and line) · **Fix** (with its size) · **Ruling** (the decision it touches).

### 1. The first-sale step has no pointer: a player who walks off can keep missing the offer
- **When:** about 1:00–1:10, from the first display until the first sale. The whole tutorial waits on this sale, because the letter comes only after it.
- **Sees:**
  - "A customer is coming!" and nothing else: no arrows and no glow, wherever the player is.
  - If they go back to make another sword, the line doesn't change (no "Collect the ore" and so on) and nothing points to the shop.
  - The offer card shows only within 35 studs of the camera, and the anvil is about 110 studs from the shop. From the yard they never see it; a bell rings once.
  - The first offer lasts 45 s. Declining it sends the customer away, because the first sale has no counter-offer. The next walk-in comes 12–22 s later, plus about 10 s of walking and talking.
- **Why:**
  - `Guide.craft`, the no-letter branch (lines 516–524), returns `"A customer is coming!", nil` before any other check whenever a holder holds a sword.
  - `StarterGui.OfferBubble.MaxDistance` is 35 (`ShopController` 58–59). The far coin ping was removed on 2026-10-23 (`ShopController` 26).
  - In `ShopService`: `OFFER_TIMEOUT` 45 (line 83); no raise on the first sale (1211); `TUTORIAL_GAP` 12–22 s (84). NPCs walk 6 studs/s (616), and it's 44 studs from `CustomerSpawn` to the rack.
- **Fix (small, Guide only):**
  - While waiting, return the displayed sword's holder as the target, so the arrows and glow lead back to the shop.
  - While its card is up, show "Accept the offer" with the arrow on the customer. The spotlight can't do it: it needs a ScreenGui, and the card is a BillboardGui.
- **Ruling:** 2026-10-22 "First-session guide: one line and an arrow"; 2026-10-19/22, the fair first offer with no haggling on the first sale.

### 2. "Tutorial done" fires one step before the lessons end, so Robux offers show inside the last step
- **When:** about 3:00–3:20, from Send until the gem buy.
- **Sees:** in the second the letter's 120 coins land:
  - the Starter Pack's amber dot on Shop, in the same 2 × 2 menu as the spotlit Upgrades button;
  - the weather icon;
  - the Auto-Roll bar whenever they're near the lever: locked, and a tap offers the pass;
  - in the Gem Shop step itself: a Buy on any other card (More VIPs 25, Quicker Mail 30, More Clients 40, with 5 gems) shakes and pops the Robux gem pack card ("+80", while that pack is on sale).
  - The Auto Anvil pill (new today) has the same check. It shows from the first forge after Send, and a tap prompts the 49 R$ pass directly.
- **Why:**
  - Every "after the tutorial" check reads the plot's `TutorialDone`, which `ShopService` sets when the letter is sent (806–811).
  - The checks: `PackOffer.offer` 58, `MenuController.updateDot` 196, `AutoRollController.near` 182, `AnvilController.refreshAuto` about 843, `WeatherController` 63.
  - Since 2026-10-30 the lessons end on the gem buy (`GemTour` goes nil), not on Send.
- **Fix (small):**
  - One client check, e.g. `MyPlot.lessonsDone(plot)` = `tutorialDone(plot) and player:GetAttribute("GemTour") == nil`. `GemTour` goes nil on the buy or on the second close.
  - Use it in `PackOffer`, the Shop dot, the Auto-Roll bar, the Auto Anvil pill, and in the purchase spots another session is building.
- **Ruling:**
  - [[Design/Monetization Plan]]: offers "never during the tutorial"; the Starter Pack: "nothing in the first session's tutorial".
  - 2026-10-30 "The lessons end on the gem buy".
  - Urgency guardrail: "One surprise at a time".

### 3. The cheer and the first daily window collide, or the daily never comes
- **When:** about 3:15, right after the gem buy.
- **Sees:** two possible outcomes.
  - **The Gem Shop is shut within about 3 s of the buy:** "Create more swords to sell!" and its confetti (2.9 s, DisplayOrder 7) play over the daily window. That window opens about 3.5 s after the buy (GemGui, DisplayOrder 6).
  - **The Gem Shop stays open longer** (it stays open after a buy, and nothing asks the player to close it): the daily window is skipped for the whole session. Only the top bar gift's red dot is left, so day 1 of the streak may go unclaimed.
- **Why:**
  - `GemController`'s join task (330–347) waits for `done()`, which is true from the buy. It then waits 3 s and shows the daily only `if ... not win` (344), with no retry.
  - `Guide.celebrate` (745–767) starts as soon as `GemShop.Visible` goes false.
- **Fix (small):** in that task, wait until no gem window is open and the cheer is over (`WorkshopOpenGui.Enabled` false), then show the daily.
- **Ruling:** 2026-10-30 "the cheer and the first daily window wait for it"; "One surprise at a time".

### 4. After the cheer there is no next goal
- **When:** from about 3:20.
- **Sees:**
  - No guide line, no arrows, and the quest tracker hidden (no accepted letter).
  - Five pads, each labelled within 22 studs: Wakizashi Sword $60 by the anvil, Ore Slot 2 $75 by the roller, Wall Sword Rack 2 $106 in the shop, Sword Rack $280 by the shop door, Delivery Cart $6,200 in the yard corner.
  - Their 132 coins buy any of the first three right now, but nothing says so.
- **Why:** `Guide.goal` returns nil once the letter is done and the gem step is over (lines 665–668, 703), by design since Fixes2.
- **Fix (small, Allen's call):** a one-off, non-blocking hand-off. Two ways:
  - after the cheer, "Buy an upgrade on a green pad", with the arrows to the cheapest one you can afford, ending on any pad buy;
  - or the banner's second line naming that pad.
- **Ruling:**
  - Fixes2, 2026-10-28: "Don't prompt to buy ore slot 2".
  - LihFolk principle 6, "Hand over a next goal". Its reference project had players "thrown in the game without knowing what to do" until it added a goal chain.
  - Pottery review, lesson 7: a concrete project for the next session.

### 5. At the cheer, customers come about 3× less often and about 40% of offers are missed
- **When:** from Send.
- **Sees:**
  - In the tutorial a customer came within about 10 s of each display, and then every 12–22 s.
  - From Send they come every 45–75 s, and every 36–64 s once Better Advertising I is bought, just as the banner says "Create more swords to sell!".
  - Cards show only within 35 studs (finding 1), so swords sit on the 3 holders while the child works in the yard.
  - The simulator, using Allen's measured offer habits, misses about 40% of offer cards in the first 15 minutes. With the game's rules: casual 7 missed against 8 sold, efficient 6 against 10.
- **Why:** `ShopService`'s walk-in loop (1317–1335, the switch at 1322); `GemUpgrades.INTERVALS` (line 21).
- **Fix:** either or both:
  - (a) a ramp: keep the tutorial's gap for the first 3 sales after the tutorial, or for its first 3 minutes (small, one loop);
  - (b) a HUD "customer waiting · 32s" chip. The sim's `offer-counter-25` scenario moved the casual Gladius 44 min sooner ([[Development/Gameplay Simulator Plan#Run on the current game, with a shop counter scenario (2026-10-29)]]). Small–medium; still undecided.
- **Ruling:**
  - 2026-10-27 customer rate: the tutorial keeps 12–22 s until Ore Slot 2, which became `TutorialDone` in Fixes2.
  - 2026-10-23: the far coin ping was removed (Allen: "not a fan of the coin overhead popup").

### 6. The Katana letter comes a few minutes after the tutorial with no way to it
- **When:** 45 s after the third shop sale, about 2–4 min after the tutorial.
- **Sees:**
  - Musashi's popup (15 s): "I need a Katana. Can you make one?" There's only Accept, because story letters can't be declined.
  - The tracker then shows "• Katana · 90%+" for 15–20 minutes. In the sim (game rules) the Katana pad is bought at 7.2–12.6 min by efficient, manager and grinder; only 14 of 200 casual players have it by 15 min.
  - The anvil's blade picker has no Katana. Nothing says it's the Katana Sword pad, two pads up the chain ($60, then $360, then $1,300), or that it needs 90%+: a full forge, since an early finish is 80%.
  - It takes one of the mail's two slots, so only one order fits at a time.
  - It can land within a minute of the first mail order (both around +3:00). A story letter's popup replaces an order's (`MailController` 487), so that order's popup is lost.
- **Why:** `Commissions` Katana: `afterSales` 3, after IronTanto (56–67; `due` 102–109).
- **Fix (small):** either
  - also wait for the Machete: an `afterUpgrade = "MacheteBlueprint"` that `Commissions.due` checks against the plot's `Bought_`, so the letter comes when the Katana's pad stands;
  - or let its want say where to get it ("a Katana (the sword pad by the anvil)").
- **Ruling:** 2026-10-22, the teaching commissions ("after the third shop sale"); 2026-10-28 "Only the tutorial's letter is guided".

### 7. 15 s of nothing in the tutorial's second loop
- **When:** about 1:50–2:05, while the letter's Iron heats.
- **Sees:** the guide line disappears for 15 s. The arrows end at the furnace, and there's only its timer.
- **Why:** `Guide.craft` 547–548 (`return nil, heating`). `ForgeService` 709 heats in 3 s only while `completed` is 0.
- **Fix (small):** either
  - while the letter's ingot heats, the station isn't bought and the player can afford it, show "Buy the Polishing Station" (`buyStep`). Furnace to pad is 61 studs (3.8 s), so the round trip and Buy (about 10 s) fit inside the heat;
  - or keep the 3 s heat until the tutorial is done.
- **Ruling:** 2026-10-22 "No line while an ingot heats (the furnace shows the time)"; 2026-10-22 "The first sword goes quicker"; 2026-10-30, the furnace starts at 15 s.

### 8. One tap on the bag's card trash destroys the tutorial's only item
- **When:** whenever the bag is open during the tutorial.
- **Sees:**
  - A trash icon at the top left of each ingot and sword card. One tap deletes a single item at once, and in the tutorial that's the only ingot or sword.
  - On an 844 × 390 phone the trash is 28 px of a 59 × 66 px card.
  - The cost is a whole extra loop (about 1 min). After the first sword the redo's heat is 15 s, and once an ore has been collected, the first-pull Common and Uncommon are gone too.
- **Why:** `Hotbar` 292–297 ("one item goes at once"). The trash remote has no tutorial guard.
- **Fix (small):** either arm-then-confirm for single items too (the stack path already does it), or hide the card trash until the tutorial is done.
- **Ruling:** 2026-10-30 bag card trash (Allen: "press it to delete").

### 9. An Uncommon first sale can buy the Wakizashi and cost an extra loop
- **When:** about 1:15–2:30. It happens only if the player pulls twice before collecting: the second pull is an Uncommon and its sale pays 64.
- **Sees:**
  - The Wakizashi pad ($60) stands 6 studs from the anvil while they forge the letter's sword, so it's easy to buy.
  - After that buy: "Sell it to afford the Polishing Station". They sell the letter's Iron Tantō (the haggling lesson card shows here), buy the station and make a third Iron Tantō, about 1.5–2 min more.
- **Why:** `TycoonService.standing` (65–83) always stands the next sword; `Guide` 488–492.
- **Fix (small):** either
  - don't stand blueprint pads until the letter is sent (in `standing`, refreshing the plot then);
  - or top the player up to 30 when the station step needs it.
- **Ruling:** 2026-10-30, "make sure our game is set up so they actually have enough for it"; LihFolk: "a tutorial step that can be failed by the economy: top the player up to exactly the price".

### 10. The game's first action is a hold nobody explains
- **When:** about 0:03.
- **Sees:** "Pull the lever". The prompt square needs a 1 s hold (gold fills it from the bottom), and a tap does nothing visible.
- **Why:** `Smithy.OreRoller.Machine.RollPrompt` has `HoldDuration` 1.0; the line is at `Guide` 558.
- **Fix (tiny):** "Hold to pull the lever" (5 words). Pottery's first line says to hold E at the lever.
- **Ruling:** none.

### 11. In the mail and the Gem Shop only the spotlight shows, not the guide line
- **When:** the mail steps (about 1:15–1:25, then about 3:00) and the gem step (about 3:10).
- **Sees:**
  - "Open the letter", "Accept the request", "Close the mail" and "Buy a shop boost with your gems" never draw.
  - In the letter the child gets 24 words of text with a spotlight round the whole paper (as Allen asked), but no line saying to Accept.
- **Why:**
  - `StarterGui.GuideGui` is a `HudPart`, while `MailGui.Window`, `GemGui.GemShop` and the pickers are `HidesHud`. So `HudFocus` (`apply`, 50–72) disables GuideGui while they're up.
  - SpotlightGui isn't a `HudPart`, so the spotlight still shows.
- **Fix (small):** either `HudFocus` leaves GuideGui on while `SpotlightGui.Enabled` (it already draws over the shade, at DisplayOrder 9), or delete those strings.
- **Ruling:** Refinements2 (2026-10-23), "all the other guis should disappear"; Fixes2, "spotlight the entire upgrade ... same with the letter".

### 12. The Gem Shop hidden mid-step leaves no pointer back
- **When:** the gem step.
- **Sees:** if something hides the Gem Shop without its X (another window opening), "Buy a shop boost with your gems" stays up. There's no spotlight, and nothing points to Upgrades.
- **Why:** `Guide.gemTour` 575–578 checks only `GemTour == "open"`.
- **Fix (tiny):** while the shop isn't Visible, treat "open" like "todo", so the Upgrades button is spotlit again.
- **Ruling:** 2026-10-30, the gem step.

### 13. The guide waits on a heating ingot the letter can't use
- **When:** about 1:30–2:10. It happens if a non-Iron ore was collected and heated.
- **Sees:** no line for 15 s, then "Take it out" for an ingot the letter can't use.
- **Why:** `Guide.furnaces` (344–369) doesn't return the ingot's metal; `craft` 543–548 doesn't check it.
- **Fix (small):** skip a ready or heating ingot that doesn't fit the letter.
- **Ruling:** none.

### 14. Join weight in the first seconds
- **When:** 0:00, the join.
- **Sees:** a longer load and more memory used on phones.
- **Why:** Workspace still holds 25,622 instances (the live map is about 4.1k, per the map review). Among them: the layout drafts, `A3_Compact` at x 1600 (inside the east lots' streaming range), `GreatSwordRig`, `Sword Animations`, `MaterialDemo`, `ZanbatoPreview`, and today's `_PreviewYou`, `_PreviewNpc` and `_RoofCapTmp_*` models.
- **Fix:** the map review's item 3, moving the drafts to ServerStorage (small).
- **Ruling:** [[Sessions/2026-10-30#Proposals and the map review]], item 3 (not done).

### 15. A $6,200 pad from minute 0, with a Robux pack on tap
- **When:** from 0:00.
- **Sees:**
  - "Delivery Cart $6,200" in the yard corner, 31 studs from the spawn: one of only five pads, and out of reach for an hour or more.
  - After Send, Buy on it pops the coin pack that covers the gap.
- **Why:** `TycoonService` `PAD_ALWAYS` (44).
- **Fix (Allen's call):** stand it from the first upgrade bought after the tutorial.
- **Ruling:** 2026-10-30 "Delivery upgrade should always be available".

### 16. The funnel measures the old tutorial
- **When:** the whole tutorial, on the Creator Dashboard.
- **Sees:** nothing in game; the funnel reports the tutorial's end one step early and can't show where in the second loop players drop.
- **Why:**
  - `TUTORIAL_END` is still "Delivered the first letter" (`SmithyCore` 278–283), though the lessons end on the gem buy.
  - Nothing logs the station buy or the polish. The tutorial's whole second loop (Iron, heat, forge, station, polish) sits between funnel steps 10 and 11.
- **Fix (small):** add "Bought the Polishing Station" and "Polished the letter's sword", move the end to the gem buy, and version the funnel name.
- **Ruling:** 2026-10-29 Analytics funnels.

### 17. Studio's Dev Panel tests a different tutorial from a new player's
- **When:** Allen's playtests.
- **Sees:** a different first sale and a different end to the tutorial, so a test doesn't match what a new player gets.
- **Why:**
  - **Reset progress** keeps `ForgeService`'s `tutorialPulls` and `wantPulls`, which are cleared only when the player leaves (389–392). The first pull after a reset is an Uncommon (if the old count was 1) or a plain roll (if 2), not the Common, so the first sale is 64.
  - **Skip tutorial** (`DevTools` 130–140):
    - marks the Katana letter done too;
    - pays no letter coins or gems;
    - leaves `sold` and `completed` as they were, so the first heat stays 3 s and the next two sales keep the tutorial's terms;
    - doesn't re-copy GemController, so the daily never opens by itself that session.
- **Fix (small):** clear both tables in a `SmithyCore.onRejoin` hook; Skip pays 120 coins and 5 gems and marks only the first letter.
- **Ruling:** the Dev Panel (2026-10-23).

### 18. "Black Iron" on the lid while the guide says "Pull again for Iron"
- **When:** while hunting the letter's Iron.
- **Sees:** a "Black Iron · Common" ore under "Pull again for Iron". Black Iron is 1 in 5 of the Commons, and Frost Iron is a Rare.
- **Why:** `Materials` names.
- **Fix (tiny):** "Pull again: Takeda wants Iron", or rely on the ore's "Takeda wants this!" line.
- **Ruling:** none.

### 19. No skip for live players
- **When:** the whole tutorial.
- **Sees:** no way to skip it.
- **Why:** LihFolk's tutorial rubric makes a skip a hard gate. Here the tutorial is the core loop and lasts about 3–4 min, and a rejoin resumes from the saved state.
- **Fix:** none; Allen's call.
- **Ruling:** none.

### 20. A mail popup that lands during a station view counts down unseen
- **When:** from about +3:00 after the tutorial.
- **Sees:**
  - An order (8 s) or story letter (15 s) that arrives while they're at the anvil or polishing never appears; only the mail button's dot is left.
  - A timed-out story letter doesn't pop up again that session.
- **Why:** `HudFocus` parks `MailGui.Popup` during station views, but `MailController.showPopup` (411–436) keeps counting down.
- **Fix (small):** start the countdown only once the popup is actually on screen.
- **Ruling:** 2026-10-30, every mail popup times out.

## The tutorial, step by step

All guide text is the top line (GuideGui.Goal). The pointers are the floor arrows and the target's pulsing lime glow. Pickers spotlight one card, with a ghost cursor tapping it every 1.2 s. The step comes from your own state (`Guide.goal`), so a rejoin or respawn resumes wherever you are. "[hidden]" means `HudFocus` hides the line while a window is up (finding 11).

| # | Line (words) | Shows when | Ends when | Pointer | What else is on screen | Child's clock |
|---|---|---|---|---|---|---|
| 1 | "Pull the lever" (3) | no ore, ingot or sword | a pull (1 s hold) | arrows, roller glows | the prompt square "Pull lever" | 0:00–0:05 |
| 2 | — | box rolling | ore lands (Common 1.75 s) | — | the cascade; "NEW" over a first-time metal | |
| 3 | "Collect the ore" (3) | ore on a stand | collect (8-stud prompt) | arrows, stand glows | | 0:07 |
| 4 | "Heat the ingot" (3) | cold ingot, free furnace | ingot in | Furnace 1; in the picker, the ingot card | | 0:10 |
| 5 | — | heating (3 s, first sword only) | ready | arrows to the furnace | timer runs 15 → 0 in 3 s | 0:16 |
| 6 | "Take it out" (3) | ready | taken | furnace | ding | 0:19 |
| 7 | "Forge a Tantō" (3) | hot ingot | Finish (from 8 of 10) or the 10th strike | Anvil 1; the ingot card, then the Tantō card | anvil camera, strike ring, progress bar with the 8/10 notch | 0:21–0:40 |
| 8 | — (hilt) | blade done | the hilt seated | the HiltSeat ghost slides it (first sword only); "Drag the hilt onto the blade" | camera over the anvil; hit-stop, sparks, reveal 1.45 s | 0:40–0:45 |
| 9 | "Put it on display" (4) | a sword, nothing displayed | displayed | the nearest WallRack1 holder; the sword card | cradles build, the sword pops | 0:45–1:00 |
| 10 | "A customer is coming!" (4) | a holder full, no sale yet | the sale | **none** (finding 1) | the customer walks in (7.3 s) and remarks (2.5 s); a card such as "Copper Tantō 42", Accept / Decline, 45 s | 1:00–1:10 |
| 11 | — | sold, letter not yet here | letter offered, 3 s later | — | "+42" pop, coins fly; "Pleasure doing business!" | |
| 12 | "Read the letter" / "Open your mail" (3) | offered; the popup up (15 s) / timed out | the mail opens | spotlight: the popup / the Mail button | popup: Takeda's face, "Sent you a letter", countdown | 1:13 |
| 13 | "Open the letter" (3) [hidden] | the list open | row tapped | spotlight: the row | | |
| 14 | "Accept the request" (3) [hidden] | letter open | Accept | spotlight: the whole letter | 24 words, the want "polished Iron Tantō" in bold red; reward 120 coins and 5 gems | 1:15–1:25 |
| 15 | "Close the mail" (3) [hidden] | accepted, mail open (once) | X | spotlight: X | | |
| 16 | "Pull the lever for Iron" (5) | accepted, no Iron | a pull | lever | tracker "• Polished Iron Tantō" under Mail | 1:27 |
| 17 | "Pull again for Iron" (4) | a non-Iron ore | a pull | lever | the second pull is always Iron | |
| 18 | "Collect the ore" (3) | Iron on a stand | collect | ore | "Takeda wants this!" | 1:40 |
| 19 | "Heat the ingot" (3) | cold Iron | in | furnace; the IngotIron card | | 1:45 |
| 20 | — | heating, **15 s** | ready | arrows to the furnace | timer (finding 7) | 1:50–2:05 |
| 21 | "Take it out" (3) | ready | taken | furnace | | 2:05 |
| 22 | "Forge an Iron Tantō" (4) | hot Iron | blade done and hilted | anvil; the Iron and Tantō cards | no hilt ghost now | 2:07–2:30 |
| 23 | "Buy the Polishing Station" (4), then "Press Buy" (2) | an Iron Tantō, station unbought, 30+ coins | bought | arrows to the pad (31.3, 37); the Buy billboard | confetti, gold ring, chime; the station builds | 2:30–2:38 |
| 23b | "Sell it to afford the Polishing Station" (7) | the same, under 30 coins | a sale, then 23 | the nearest holder | | (branch) |
| 24 | "Polish it" (2) | station bought, sword unpolished | fully polished and saved | station; the sword's card | polish view: the ghost glides along the blade until your first stroke, then taps Save at 100%; "Drag along the edge"; value counts 42 → 47 | 2:40–3:00 |
| 25 | "Take it back" (3) | the letter's sword on a holder or the sword rack | taken back | its handle | | (branch) |
| 26 | "Send it from the mail" (5) | a polished Iron Tantō | sent | spotlight: Mail button, then the row's Send | +120 coins, +5 gems; the mail closes; `TutorialDone` (finding 2) | 3:00 |
| 27 | "Open Upgrades" (2) | `GemTour` todo, done, 5+ gems, no daily window up | Gem Shop opens | spotlight: Upgrades | Starter Pack dot, weather icon | 3:05 |
| 28 | "Buy a shop boost with your gems" (7) [hidden] | `GemTour` open | a buy, or the second close | spotlight: the Better Advertising row | "Customers 1x → 1.2x", 5 gems | 3:08 |
| 29 | Cheer "Create more swords to sell!" (5) | `GemTour` nil and the letter done, once the shop shuts | 2.9 s | — | banner and confetti | 3:12 |
| 30 | Daily window | 3 s after the buy, if no gem window is up | Claim | — | Day 1 = 5 gems; collides with 29 (finding 3) | 3:15 |

Free play starts at about 3:20 with 132 coins, or 124 if the first sword was finished early (34 instead of 42). Each Common Tantō is worth 42, since the hilt seat always adds 6%. The player also has 5 gems (if the daily was claimed) and Better Advertising I.

### Branches

| What the player does | What happens | Exit |
|---|---|---|
| Wanders off mid-step | The arrows run straight from their feet to the target from anywhere, through walls; the glow shows through walls | Always, except step 10 (finding 1) |
| Leaves a station mid-step | Anvil: the strikes are dropped, the hot ingot stays hot, "Forge a Tantō" again. Polish: Leave saves the partial polish, "Polish it" again. Hilt: no backing out (the sword is already made) | Yes |
| Sells the letter's sword instead of sending it | "Take it back" while it's on a holder. Once sold: back to the lever, Iron again by the second pull. The haggling lesson shows on that sale | Yes, about 1.5 min lost |
| Trashes the tutorial sword or ingot | The guide starts over from the lever. Once an ore has been collected, pulls use the normal odds; after the first sword, heats take 15 s | Yes, about 1 min lost (finding 8) |
| Rolls a non-Iron ore | "Pull again for Iron"; the next pull is always Iron. Collecting the wrong one anyway just leaves it in the bag | Yes (finding 13) |
| Can't afford the station (30) | "Sell it to afford the Polishing Station": sell the only sword, buy, make another | Yes, about 1.5–2 min (finding 9) |
| Declines or misses the first offer | The customer leaves, with no counter-offer on the first sale; the next one comes in 12–22 s plus about 10 s | Yes (finding 1) |
| Closes the Gem Shop without buying | "Open Upgrades" once more; the second close ends the step and the cheer plays. Any other card's Buy offers a Robux gem pack (finding 2) | Yes |
| Taps the top bar gift early and claims day 1 | 5 gems early. Buying Better Advertising I then skips the gem step, and the cheer plays at Send | Yes |
| Dies or resets | Ingots and swords come back on respawn; the anvil and polish views leave; the HiltSeat ends on Died; the guide re-reads state | Yes |
| Dev Panel Reset progress / Skip tutorial | A different tutorial from a new player's (finding 17) | Studio only |

### Rejoining halfway

The guide reads state, so a rejoin resumes. What comes back in each case:

| Left during | On rejoin |
|---|---|
| A roll, or ore not collected | It comes back as a cold ingot: "Heat the ingot" |
| A heat | The ingot comes back hot: "Forge a Tantō" |
| The anvil | Strikes lost, ingot still hot: "Forge" again |
| First sword on display, before the sale | Re-seated: "A customer is coming!". The customer isn't sent at once (that happens only on the display action); the tutorial loop sends one in 12–22 s plus about 10 s |
| The 3 s after the sale | The letter arrives on join (`offerCommission(player, true)`) |
| Letter offered, unread | Its popup comes again on join |
| Letter read but not accepted | "Open your mail", spotlight on Mail |
| Letter accepted | The craft steps; the Iron counter starts again (1 in 3, by the second pull) |
| Letter sent, gem shop never opened | The daily window opens on join (`fresh` is false then); "Open Upgrades" follows it; the cheer comes after the buy |
| Letter sent, gem shop opened once without a buy | `toured` is saved, so `GemTour` is nil: no gem step and no cheer (only the end beat is lost) |

## Minute by minute

The tutorial's clock is in the step table above. After it, for a child who takes the ores that come (Common or Uncommon), has one furnace and makes a sword every 60–75 s:

| Time | What happens | Coins (child) |
|---|---|---|
| 0:00–1:10 | The first loop: lever, collect, heat (3 s), forge, hilt, display, first sale | 0 → 42 |
| 1:13–3:00 | The letter: accept, Iron by the second pull, 15 s heat, forge, Polishing Station, polish, send | 42 → 12 → 132 |
| 3:00–3:20 | Gem step, cheer, daily window. Starter Pack dot, weather icon, pack offers and the Auto-Roll bar all appear at Send | 132, 5 gems |
| +0:00 (3:20) | No line and no goal. Five pads: $60, $75, $106, $280, $6,200 | 132 |
| +0:10 | First post-tutorial buy is possible (the Wakizashi or Ore Slot 2) | 72 or 57 |
| +0:15 | At the lever, the Auto-Roll bar slides down, locked | |
| +0:50 | First forge after the tutorial: the Auto Anvil pill, locked; a tap opens a 49 R$ prompt | |
| +1:00–1:30 | Second shop sale, the haggling lesson: "Decline and they may offer more". Walk-ins every 36–64 s now (were 12–22) | +48–63 a Common Tantō; +109–143 a Common Wakizashi |
| +2:00–3:00 | Third shop sale; the Katana letter 45 s later (finding 6) | |
| +3:00 | First mail order, an 8 s popup (1:30 in Snow): e.g. an Iron Tantō for 79 and 2 gems, or a Wakizashi for about 179 | |
| +3:00–5:00 | Ore Slot 2, Wall Sword Rack 2. Next on the floor: Ore Slot 3 $280, Display Table 1 $440, Machete $360 | |
| +5:00 | The weather changes (every 5 min; Sunshine doubles walk-ins, Snow the mail) | |
| +5:00–10:00 | Sword Rack $280, Ore Slot 3 $280, Machete $360. Waits: 15 s a heat, 36–64 s between walk-ins, 3:00 between orders | |

Simulator, game rules (median coins held and earned):

| Type | Held at 5 / 10 / 15 min | Earned by 5 / 10 / 15 min |
|---|---|---|
| casual | 71 / 196 / 353 | 230 / 994 / 2,489 |
| efficient | 168 / 622 / 1,240 | 455 / 2,996 / 8,353 |

The sim is an upper bound for a child: its players re-pull for Uncommon+ (casual) or Rare+ (the others), have Allen's hand speed, and never stop to read.

## Taps and walking per sword

Paths are from PathfindingService on `Workspace.Plot` (agent radius 1.5), at WalkSpeed 16.

| Leg | Studs | Seconds | Taps (touch) |
|---|---|---|---|
| Spawn → lever | 5 | 0.3 | 1 hold (1 s) |
| Lever → ore stands | 16 | 1.0 | 1 (Collect) |
| Stands → Furnace 1 | 39 | 2.4 | 2 (prompt and ingot card; 1 if holding the ingot) |
| (heat 3 s, then 15 s) | | | 1 (Take out) |
| Furnace → Anvil 1 | 22 | 1.4 | 3 (prompt, ingot, blade) and 10 strikes (or 8 and Finish), 1 drag |
| Anvil → shop holder | 115 | 7.2 | 2 (+ and the card), 1 (Accept) |
| Shop → lever | 67 | 4.2 | |
| **A sword, unpolished** | **about 259** | **about 16** | **about 21 taps, 1 hold, 1 drag** |
| With polish: anvil → station 70, station → shop 119 | about 333 | about 21 | + prompt, card, 6–10 strokes, Save |
| Furnace → Polishing Station pad | 61 | 3.8 | (for finding 7) |

The longest leg is the anvil to the shop (115 studs). LihFolk's guide is under 10 s between stations, and every leg is within it. Allen walks his measured routes at 10.8 studs/s, so real walks run about 1.5× these figures.

## Simulator

Full run note: [[Development/Sim Runs/first-10-minutes-2026-10-31]]. Unit tests: 38 passed. 200 free players per type, 15 min each, as the sim stands ("stock") and with four of the game's tutorial rules patched in by a throwaway script ("game rules"). The sim's code wasn't changed.

**Disagreements between the sim and the code** (Allen's rule: the sim mirrors the game):
1. The first letter arrives 45 s after the first sale in the sim; the game sends it at 3 s.
2. The sim has no first-pull Common and second-pull Uncommon.
3. The sim has no Iron lean and no Iron by the second pull.
4. `engine.pick_target` treats the Wakizashi and Ore Slot 2 as the Guide's buys and targets the Wakizashi before the station. The game prompts only the station, so in the sim the letter's first Iron Tantō is usually sold to pay for the Wakizashi.
5. Not patched: the game sends the first customer the moment the first sword is displayed; the sim waits for its spawn clock.
6. Not patched: the sim pays the day-1 daily at 0:00, which makes no difference.

**What patching 1–4 changes:**
- The tutorial ends 2.2–3.7 min sooner. The letter is sent at 2.4 / 2.6 / 2.5 / 4.0 min (manager, efficient, grinder, casual), against 4.3 / 4.8 / 4.7 / 7.7 in the stock sim.
- The station is bought at 1.2–2.1 min.
- Coins earned by 15 min move under 7%, so the long-run pacing reports stand.

**Buys by 15 min, game rules:**
- every type: the Polishing Station, then the Wakizashi;
- then Machete and Ore Slot 2 (efficient, manager), or Ore Slot 2 and Wall Sword Rack 2 (grinder, casual).
- Katana at 8.6 (efficient), 7.2 (manager) and 12.6 (grinder, 156/200 players). Casual has the Machete at 10.8 min; 14/200 casual players have the Katana by 15 min.

**Offers missed in 15 min:** 6 / 2 / 6 / 7 (efficient, manager, grinder, casual), against 10 / 11 / 10 / 8 sold.

## Against good FTUE practice

| LihFolk target | Sell Swords! | |
|---|---|---|
| Join to control in about 10 s | Not measured; 25.6k Workspace instances (finding 14) | ? |
| Spawn facing the first target, walk under 10 s | Facing the lever, 8 studs | ✓ |
| First objective in 8 words or fewer | 2–7 words, every line | ✓ |
| First meaningful action under 20 s | About 0:03, if they hold (finding 10) | ✓ |
| First reward under 60 s, with sound, number and celebration | The ore reveal at about 0:05; the first sale's "+42" at about 1:10 (Pottery 1:12) | ~ |
| One goal, one pointer | Yes, except step 10 (finding 1) | ~ |
| Core loop 3+ times in 5 min | 2 in the tutorial, 1 more by about 4:30 | ~ |
| Number up, one choice, a spend that changes the verb | Coins up ✓; the station adds polishing ✓; the first real choice comes after the tutorial | ~ |
| A tutorial purchase guaranteed affordable | Yes, unless the Wakizashi is bought first (finding 9) | ~ |
| Locked features shown with a lock and price | Pads within 22 studs, locked crew cards, Auto-Roll and Auto Anvil locks | ✓ |
| No pop-ups until the tutorial ends | The daily waits ✓; the Starter Pack dot and pack offers come one step early (finding 2); the gift's red dot shows from join | ✗ |
| End: a celebration, then a next goal | The cheer ✓, but it collides with the daily (finding 3); no next goal (finding 4) | ✗ |
| Skip, rejoin, death, friends | No skip (finding 19); rejoin ✓; death ✓; friends never blocked ✓ | ~ |
| Guidance fades with competence | It ends with the lessons; ghosts tap until you pick | ~ |
| Phone targets of 44 px or more | Yes (UI reviews 2026-10-30), except the card trash at 28 px (finding 8) | ~ |
| Funnel for every step | 14 steps, but the second loop is one black box and the end is one step early (finding 16) | ~ |
| Whole tutorial under 3 min | About 3:15–4:30 | ~ |
| Tycoon row: first upgrade from income, the next priced in view | The station from the first sale ✓; five priced pads ✓; three affordable at the end ✓ | ✓ |

## Other sessions' work seen at 18:00

- **`StarterGui._LevelPreview`:** an enabled ScreenGui at DisplayOrder 10000 (3 frames). It looks like the crew level bars' preview copy. Left there, it would draw over every new player's screen from 0:00.
- **Workspace temp models:** `_PreviewYou`, `_PreviewNpc`, `_RoofCapTmp_Starter` and `_RoofCapTmp_Upgraded` (from the shop roofs work). They should go before Play.
- **The Auto Anvil:**
  - its pill (`AnvilHud.Auto`) is hidden on `TutorialDone`, so both tutorial forges are by hand ✓;
  - but it shows during the gem step (finding 2), and a locked tap prompts the 49 R$ pass on the first post-tutorial forge.
  - Suggestion: wait for the lessons' end and a few hand-made swords, so the core verb isn't sold away in minute one.
- **In-world purchase spots:** not in the place yet. Key them to the lessons' end (finding 2), not `TutorialDone`, and keep them off the first loop's paths (the lever, furnace, anvil and shop holders).

## Questions for Allen

1. Should the Robux surfaces (the pack offer, Starter Pack dot, Auto-Roll and Auto Anvil locks, purchase spots) wait for the gem buy rather than the letter? Recommended.
2. A one-off next goal after the cheer, such as "Buy an upgrade on a green pad" with arrows to the cheapest one you can afford? Or keep free play silent (Fixes2)?
3. After the tutorial: a short walk-in ramp, or the "customer waiting" HUD chip, or both?
4. Should the Katana letter wait until its pad stands (the Machete bought)?
5. The second heat: 3 s until the tutorial ends, or buy the Polishing Station while it heats?
6. A confirm on the bag's single-item trash, or no card trash until the tutorial is done?
7. A skip for live players (LihFolk's hard gate), or not, since the tutorial is the loop?

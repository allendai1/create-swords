---
title: Core Loop Review
status: proposal — awaiting discussion and playtest
tags: [design, onboarding, gameplay, create-swords]
type: "design"
updated: "2026-10-19"
---

# Core Loop Review

Reviewed 2026-10-19 against the approved [[Design/Game Design Document|Game Design Document]]. **Onboarding, pacing, and balance changes below remain proposals unless explicitly marked confirmed.** Allen confirmed that item pickers must open every time, even with one valid item; the automatic-selection proposal was rejected. Base heating is 10 seconds. The first-sale tutorial has no customers while the first sword is being made; putting it on sale triggers the first customer arrival.

**Station-order reconciliation:** the anvil now ends forging at 90% automatically. Hilt assembly follows; etching is optional, then freehand polishing at its own station is the optional final step on the completed sword. The proposed walkthrough below is aligned to that later confirmed direction. [[Design/Workshop Growth]] adds employee training/recovery, separate optional courier orders, bonus-only weather and indoor roof visibility; these do not replace the starting tutorial or direct commissions.

## Assessment

The loop is understandable: get metal, make a sword, sell it, improve the workshop. Untimed circles and safe grinding make individual actions accessible. The total interaction chain still risks feeling cumbersome because players repeatedly choose and transfer the same workpiece.

Fun is plausible, not verified. With failure and timing pressure removed, satisfaction must come from visible transformation, responsive hammer feedback, attractive materials, customer reactions, and meaningful next goals. Circles alone may become repetitive. Avoid trying to solve this immediately by adding more mandatory minigames.

## Recommended first session

Times are provisional playtest targets, not promises. Aim for the first completed sale within roughly 3–5 minutes.

| Moment | Player action | Purpose / recommended handling |
|---|---|---|
| Join, first 20–30 seconds | Arrive beside an assigned open-front smithy; see the anvil, forge, and display | Avoid a long walk or plot-selection task before crafting. Show one objective: “Make your first tantō.” |
| Begin crafting without customers | Tutorial guidance directs the first tantō craft; no customers visit yet | **Confirmed:** first customer arrives only after the sword is put on sale. **Confirmed:** start with the tantō blueprint and simple on-screen instructions. Local commissions introduce wakizashi and katana afterward. |
| Roll and heat | Activate the lever, watch the ore roulette stop, collect the result, then load and collect it at the forge | Introduce material surprise. Use the confirmed **10-second base heat**; brief tutorial guidance can explain the next step without introducing a customer. |
| Forge | Choose the starting tantō blueprint and hit its circles | Each hit visibly changes the sword. Show progress clearly, keep targets readable on touch, and avoid tiny precision demands. |
| Assemble | Use the starter matching fittings and tap three times | Celebrate the complete sword with a clear name, quality, and value. |
| Decide on final refinement | After assembly and any chosen etch, optionally take the completed sword to the Polishing Station | **Confirmed station order:** the anvil auto-finishes at 90%; final polishing can improve to 100% safely. Explain the choice without forcing polishing or teaching every optional finish during the first craft. |
| First sale | Put the sword on sale on the nearby holder; this triggers the tutorial customer to walk in, inspect, and offer | **Confirmed arrival trigger:** listing the first sword, not joining or starting crafting. **Confirmed:** the first customer gives a guaranteed fair offer; haggling begins on the second ordinary shop sale. Commission delivery uses a picker and pays the agreed reward; ordinary customer scheduling remains separate design work. |
| First reward | Accept the offer and see coins and progress toward the next unlock | **Confirmed:** introduce haggling on the second ordinary shop sale; the first sale uses a guaranteed fair offer. Fund one modest useful upgrade within the first few sales. |
| Immediately after the first sale | Introduce a local wakizashi teaching commission and provide its blueprint when the commission begins | **Confirmed:** this is the next goal, rather than a required upgrade purchase or another tantō sale. The player repeats the crafting loop with a new shape and purpose. Katana follows through a later local commission. **Confirmed:** the first commission requests an **Iron Wakizashi at 90% quality or higher**; Iron is in the starter roller’s Common pool. Grinding is optional. |
| Deliver the Iron Wakizashi | Open the commission, choose the completed sword in its picker, and receive the agreed reward | **Confirmed:** no display listing or haggling for commission delivery. Teach haggling at the next ordinary shop sale, not this delivery. |
| After the Iron Wakizashi delivery | Direct the player toward their first workshop upgrade | **Confirmed:** buy a second material stand for the Ore Roller. One shared lever rolls all empty stands together, yielding one material per stand through an ore-appearance roulette lasting under five seconds. Occupied stands retain their ores and cannot roll until collected; no automatic restart. Price and exact reveal duration remain undecided; tune affordability around tutorial earnings. This does not itself change per-roll rarity odds. |
| Early special visit | A memorable outsider leaves an untimed request after the first successful loop | Hint at future possibilities. Schedule this introductory appearance; later special visits can remain reputation-gated surprises. Do not interrupt the first forging interaction. |

Katana is a visible early aspiration, not necessarily awarded in the first few minutes. Do not introduce all currencies, finishing stations, automation, and letter systems during the first sword.

## Friction and proposed remedies

| Friction | Why it matters | Recommendation to test |
|---|---|---|
| Repeated pickers | Forge ingot, anvil ingot, shape, blade, fitting, and display selection can feel like paperwork | **Confirmed: keep the picker every time, including when only one item is valid.** Improve clarity and responsiveness within that flow; do not bypass selection. |
| Heating wait and collection | The confirmed base wait is **10 seconds**, reduced from the 15-second prototype | Keep the 10-second heat legible; use the tutorial wait purposefully. Later allow loading the next ingot while working on a sword. |
| Walking between stations | Travel can exceed meaningful interaction time | Keep roller → forge → anvil → hilt bench → optional etching/final polishing → display routes readable and short. Employee anvils and racks must not block that route. |
| Sales interrupt crafting | Existing offer cards expire after 20 seconds | Queue offers or pause their response window while the player is in crafting interaction. Haggling can still lose a customer by choice; unrelated UI should not cause the loss. |
| Random materials block requests | A fixed rare-material request can become repeated rolling instead of crafting | **Confirmed:** the first commission requires an Iron Wakizashi, using Iron from the starter roller’s Common pool. Do not substitute an any-material request. Test how long players wait for that roll; no guaranteed drop or altered odds has been approved. Preserve ordinary sales while working toward requests. |
| Grinding feels mandatory | Existing multipliers give 100% swords ~33% more value than 90% swords | Compare coins per minute with and without grinding. Tune bonus and duration so both routine stock-making and refinement are worthwhile. Do not change the approved 90/100 quality endpoints. |
| Repetition | Identical circles and three taps on every sword can become mechanical | Vary blade transformations and customer purpose; keep sequences short. Add depth through materials, fittings, customer matching, and workshop choices before adding input difficulty. |
| Unclear next step | A sale can leave the player wondering what to do | Show one primary next objective and nearby progress, such as the next teaching commission or fitting milestone. |
| Employees replace all player crafting | Automation could remove the game's main activity | **Confirmed five-role direction:** starter smiths train from below 90% toward 90% and deposit bare blades; finishers combine hilt assembly and optional polish; stockers carry ready swords from the finished rack to holders; furnace operators and cashiers cover heating/sales. Players can finish employee forging to 90% and final polishing to 100%. Test speed/quality and recovery effort; values remain open. |

## Simple enough?

Yes at the action level. The player should describe the loop as **“Get metal → make a sword → sell it → improve my shop.”** Heating, grinding, and fitting are understandable parts of making a sword, but excessive menus can make the same loop feel complex. Keep the required path short; present refinement as a clear optional branch.

## What makes it fun?

- **Transformation:** a blank visibly becomes a sword under the player's hammer.
- **Discovery:** material reveals and unfamiliar visitors create variety.
- **Ownership:** choose fittings, refine the blade, and see it on display.
- **Social payoff:** a customer reacts to the specific sword, and negotiation produces a result.
- **Progress:** a sale moves a visible workshop, blueprint, fitting, or relationship goal forward.

The main risk is repetitive clicking once the novelty fades. Test the fifth sword, not just the first. Strong effects do not by themselves guarantee that repeating the activity stays fun.

## First playtest questions

Use a small initial group (for example 3–5 new players) to find obvious problems, not to claim statistical certainty. Include touch and desktop input.

- Can they find the first objective and start without verbal coaching?
- How long until their first hammer hit, complete sword, and sale? Record time spent walking, waiting, selecting, and crafting separately.
- Can they complete a second sword without help, and do they choose to make another?
- Do they understand that 90% is a valid stopping point and grinding is optional?
- Does grinding dominate earnings per minute, and do players describe it as satisfying or obligatory?
- Can they explain their next goal after a sale?
- Are offers or tutorial messages interrupting crafting?
- Do courier orders remain optional and distinct from direct commissions? Does weather preserve the first-sale customer trigger?
- Can players understand employee blade-rack handoffs and the difference between completing forging and final polishing?
- Does the indoor roof cutaway keep the route and station cameras readable?
- After roughly five swords, what do they enjoy and what are they trying to skip?

## Recommended next design decision

Review the first-session sequence above, with the confirmed starting tantō blueprint and on-screen guidance before any customer arrives. Keep explicit picker selection at every item-selection step. Once agreed, translate that flow into a focused implementation plan. No new mechanics are required to test the basic experience.

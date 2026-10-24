---
title: Building urgency in the game
type: design
status: observations and analysis — applications proposed, not approved changes
updated: 2026-10-23
tags: [design, psychology, progression, employees, create-swords]
---

# Building urgency in the game

**The strongest pattern in Allen's notes is a business that keeps giving him a worthwhile next job, with a visible path toward doing those jobs more efficiently.** Making an item feeds the shop; a sale creates space; empty space gives production a purpose; production makes the next employee affordable. Urgency emerges from understanding those connections.

Working recommendation for Sell Swords!: build a manageable operating rhythm around the existing workshop, then use occasional opportunities to vary it. Preserve relaxed swordmaking and let growth change the player's responsibilities.

## Evidence and scope

Organized from Allen's personal Create Pottery! play impressions. [[Archive/Design/Building urgency — original thoughts — 2026-10-23|The original wording is preserved unchanged]]. These impressions explain what motivated Allen; they do not establish why every player stays or prove a retention effect. The event examples are ideas in the original note, not independently verified Create Pottery! rules.

[[Design/Pottery Tutorial Review]] separately analyzes a 3:44 recording of the opening. That recording does not establish the later employee/delivery rhythm described here. Current Sell Swords! context comes from [[Current Status]], [[Sessions/2026-10-23]], [[Design/Decisions Log]], [[Design/Workshop Growth]] and [[Design/Alignment Review — 2026-10-23]]. Later dated decisions take precedence over older paragraphs. No Studio inspection or playtest was performed for this analysis.

The explanations below are design hypotheses informed by Allen's account and the cited research. Applications are proposals for discussion; this note does not change the GDD, economy, or implementation plan.

## 1. What Allen experienced

| Observation from the notes | What it felt like / why it mattered |
|---|---|
| While one pot fired, another could be shaped. Finishing the second gave a reason to return to the kiln. | Time spent on one job advanced another. There was a useful sequence to manage. |
| Finished pots needed to reach the shop so customers had something to buy. | Making objects served a visible business need. Empty shelves invited action. |
| Employees needed clay on their supply shelf. Running out felt like wasting time. | The worker made unused production capacity visible. Restocking restarted something Allen owned. |
| Specific customer requests required a particular item/material. | Some crafts had an individual purpose beyond filling shelves. |
| Bulk deliveries needed six pieces; another batch could be prepared during the trip. | A larger goal ran alongside individual pots and sales. Six is a reference-game observation, not our selected order size. |
| The potter automated shaping/glazing; a later kiln operator removed another responsibility. | Each hire gave understandable relief and made the business feel larger. |
| Spare stations still allowed personal work. | Automation added capacity while preserving involvement. |
| Highlighted VIP arrivals caught attention. Checking nearby customer offers created a reason to revisit the shop. | Customers punctuated the production routine and made the retail space matter. |

**Additional ideas:** a short rush with more customers, or a temporary improvement to ore rarity odds. The example of 2× traffic for three minutes is a suggestion to evaluate, not a chosen balance value.

## 2. Why this can pull a player forward

### Overlapping jobs make waiting useful

The kiln creates an interval in which another useful action can happen. Returning from that action produces a payoff: the first pot is ready. This can make sequencing itself satisfying.

The important relationship is **wait → useful action elsewhere → return to visible progress**. A long wait with nothing worth doing would not reproduce the experience. Nor would a collection of unrelated chores. Here, all the jobs contribute to the same shop.

Several goals sit at different distances: finish this pot, fill this delivery, afford this employee, grow this business. Completing one can bring another within reach. That is a plausible explanation for Allen's repeated decision to continue; labeling it an “unfinished-task effect” would not prove the cause.

### The player can see that their decisions work

Restocking the clay shelf makes the employee work again. Filling the shop produces sales. Choosing which job to do next changes the business. That provides feedback about being capable and in control. Research on games links perceived competence and autonomy with enjoyment and motivation to play; applying that explanation to this particular workshop is an inference. [Ryan, Rigby & Przybylski, 2006](https://selfdeterminationtheory.org/SDT/documents/2006_RyanRigbyPrzybylski_MandE.pdf)

This helps explain the “large business” feeling. It comes from coordinating a connected operation, even with a modest number of stations. Merely adding more stations would not establish it.

### Idle equipment makes opportunity cost visible

Allen's empty-clay observation is especially revealing: the employee could be producing, but is waiting for him. The cost is foregone output rather than money being deducted. An empty retail shelf communicates a similar gap.

That creates a concrete reason to act now. It can also become tiresome if supplies run out so quickly that the player cannot complete anything else. The design question is how much useful independence a stocked workshop buys the player.

### Automation rewards understanding the work

The player first learns and performs a job, then earns the ability to delegate it. The purchase has meaning because its benefit is already familiar: “I no longer have to handle every pot myself.”

The strongest progression in this account is **learn the job → build a working routine → hire help → use the freed time to expand or pursue a special project**. A hire should noticeably reduce attention spent on its task. If it immediately creates just as much compulsory handling elsewhere, the promised relief may be weak.

### A nearby improvement gives the next sale extra meaning

When the next employee is close, one more sale helps reach a specific change in how the game plays. Research on reward programs found increased effort as participants approached rewards. That supports testing clear, attainable milestones here; it does not establish the right prices or predict Roblox retention. [Kivetz, Urminsky & Zheng, 2006](https://business.columbia.edu/sites/default/files-efs/pubfiles/1200/goalgradient.pdf)

Show the actual remaining cost and what the purchase changes. Include prerequisites and training when explaining the cost of a working employee, so the apparent finish line is honest.

### Arrivals and bonuses can change priorities

A highlighted visitor or temporary opportunity can make the familiar shop feel different for a while. An interesting visitor might make a particular sword worth preparing; a traffic bonus might make stored stock useful.

Their value depends on whether the player has a meaningful response. More customers do little when there is nothing to sell. More rare ore does little when storage is blocked. Variation should give the operating routine a new choice.

## 3. Choose the kind of urgency

These are possible directions, not three systems to add together.

| Direction | Player experience | Trade-off |
|---|---|---|
| **Operating rhythm — recommended foundation** | “I can finish this sword, then restock and collect the cart.” | Needs readable stock, useful parallel jobs and enough buffer to finish the chosen action. |
| Occasional bonus opportunities | “This is a good time to sell my prepared stock.” | Adds variation, but needs production headroom and a clear benefit. |
| Frequent expiring demands | “I need to leave this sword now or miss another sale.” | Creates stronger immediate pressure, but conflicts with relaxed crafting if it dominates play. |

Allen did find proximity-based selling motivating. Preserve the purpose of visiting the shop while testing whether the response window fits the other activities. The recorded Sell Swords! offer lasts **20 seconds**, with its bubble visible nearby, and can run during a station interaction. [[Design/Alignment Review — 2026-10-23]] already flags this conflict.

My recommendation is to make it practical to finish the current craft before serving the next customer: investigate an adequate waiting period or a bounded waiting queue. Exact timing is open. Keep negotiation at the customer. Do not assume that making offers expire faster will improve the experience.

An interruption experiment found that people could work faster while reporting greater stress and frustration. It studied work tasks, not Roblox players, but it is a useful reason to measure enjoyment alongside activity. [Mark, Gudith & Klocke, 2008](https://www.ics.uci.edu/~gmark/chi08-mark.pdf)

## 4. Apply the pattern to the game we actually have

### Use the current crafter as the starting point

Our recorded crafter already takes cold rack ingots, heats them, forges, fits a hilt, polishes when available, and deposits complete swords on the Finished Sword Rack. It therefore automates more of the production chain than the potter in Allen's account. Copying Pottery's employee sequence literally could duplicate work that is already delegated.

| Part of the operation | Latest recorded support | Application to test |
|---|---|---|
| Supply | Player-operated roller; Ingot Rack capacity 12; crafter takes the cheapest available ingot. | Make remaining supply legible in the rack/crew view. Consider a player-controlled reserve for special materials. Preserve the decision against worker speech bubbles. |
| Production | One active crafter at Anvil 2; the player has the original anvil. Furnaces and polishing are shared. | Check that the player can complete a personal sword while the worker makes useful progress. A spare anvil alone does not guarantee access to every shared station. |
| Output | Finished Sword Rack capacity 6; the player transfers its swords onward. | Observe whether batching transfers feels satisfying or whether the rack repeatedly blocks production. This is the clearest reason to test a stocker next. |
| Retail | Physical displays, nearby offers and haggling; cashier is a selected later role. | Keep stock and customer needs readable. Test a cashier when serving offers becomes the responsibility the player most wants to delegate. |
| Personal work | All requests now arrive through Mail; blueprints are bought on pads. | Let the player pursue a chosen request or new shape while routine production continues. Do not revive removed request visitors/boards. |
| Bulk outlet | Cart deliveries, one active order, packing, trips and offline trip completion. | Use trips as time for retail and reserve production. Preparing the exact next order requires knowing its requirements; that visibility is not established in the notes. |
| Next ambition | Purchasable upgrades and worker training; more sword content remains open. | Keep one chosen improvement visible, with its practical benefit. After automation, retain new designs and special projects worth doing personally. |

These are build records, not fresh runtime findings. Supply reservations, new status cues, stocker/cashier behavior and customer timing changes still require design and implementation.

### Give the three sales routes different purposes

The current records put mail orders at **1.2× the submitted sword's value**, with one new order every three minutes while there is room, and deliveries at **1.1× packed sword value**. Shop offers vary. Earlier instant-refill and 1.3× delivery figures are superseded.

The desired choices are: stock the shop for immediate retail opportunities, make a particular sword for a mail request, or assemble a batch for the cart. If one route reliably pays best with the least effort and no effective limit, players can reasonably ignore the others. Then the varied operating rhythm disappears.

Compare actual earnings **and attention required**, including stock committed to the cart, walking, packing, waiting, customer preferences, gems and reputation. A lower payout multiplier alone does not prove that an outlet is balanced.

### Let each hire change the player's role

The current transition is from personally making everything to supplying the crafter, allocating its output, serving customers and making chosen swords. A possible next sequence is stocker, cashier, then the already-selected later ore attendant. This is a recommendation, not a finalized role ladder.

**Stocker versus cashier should follow observed friction:** choose the stocker first if finished racks fill and hauling dominates; choose the cashier first if customer response repeatedly disrupts enjoyable crafting. Avoid adding more crafters until output handling and demand can use their production. The latest decision currently keeps one active crafter.

Do not lengthen the ten-second base furnace wait merely to imitate Pottery's kiln. Find out whether the existing wait already fits useful parallel work.

## 5. A concrete rhythm to test

Illustrative session after the crafter and cart are unlocked; no new timers or prices are implied:

1. Check the selected delivery, mail request and shop stock. Choose what this production batch is for.
2. Supply enough ordinary ingots for the crafter to keep working during a personal craft.
3. Make a chosen sword at the player's anvil while the crafter handles routine stock. Observe competition for heat and polish.
4. Move completed swords to the shop or pack them for the current cart order. Keep special-purpose swords separate; reliable reservations would be a proposed addition.
5. Dispatch the cart, then use the trip for shop sales, another personal sword, or a reserve batch.
6. Collect earnings and reach a visible upgrade. Experience the time or capacity it actually adds.

The rhythm should include satisfying completion points: a stocked shop, a dispatched order, a new hire. Progress survives leaving; the existing offline cart completion already supports that. New offline workshop earnings remain a separate later feature.

## 6. Where rushes and VIPs fit

Start with the ordinary operation. The alignment review estimates more baseline customer arrivals than manually produced swords; its rates are estimates pending play. If supply already limits sales, a 2× customer event mostly empties shelves sooner. **Twice the traffic is not necessarily twice the income.**

A traffic rush becomes more useful when the player can prepare stock or has spare production capacity. Evaluate whether they sell additional swords and enjoy responding, rather than merely seeing more NPCs. A rarity event instead pressures rolling and storage; it needs a useful way to handle ordinary results and a clear description of the odds change.

VIP retail customers could give stocked swords a distinctive buyer and moment of recognition. Keep this separate from the removed in-person commission system. If a VIP generates a request, the current delivery channel is Mail. Appearance, preferences, rewards and return rules remain to design.

Positive weather traffic bonuses already have approved direction. A broader rush-event system would revisit the GDD's deferred village-wide events. Neither “2× for three minutes” nor a temporary luck boost is selected by this analysis. First test one opportunity after the core rhythm works.

## 7. Smallest useful playtest

Test the normal manual loop, then a comparable session with the existing crafter and cart. Use several players rather than only Allen; separate desktop and touch observations. Check new-player understanding separately from the established business routine.

| Question | Evidence to collect | What it tells us |
|---|---|---|
| Can players choose a useful next action? | Hesitation after a sale, ready furnace or cart dispatch; their explanation of the next job. | Whether the connections are understood. |
| Can they finish a personal craft? | Customers missed mid-craft; abandoned station interactions; actual response/travel time. | Whether urgency supports or interrupts the main activity. |
| What limits the business? | Worker time without input, waiting for stations, blocked by full output; empty retail holders. | Which capacity or employee upgrade has a real job. |
| Does automation feel like progress? | Attention spent on the delegated job before/after; what players choose with the freed time. | Whether a hire delivers relief and new possibilities. |
| Do the outlets remain useful? | Swords and earnings through retail, mail and cart; why players chose each. | Whether one route makes the others redundant. |
| Do players want another session? | Enjoyment, perceived pressure, a remembered next project; later voluntary returns. | Whether longer activity reflects an experience worth returning to. |

Ask after play: “What were you trying to do next?”, “What did you wish you could delegate?”, and “Was there a moment you wanted to finish your sword but felt you had to leave it?” Record both satisfying and frustrating moments.

Recommended order: **verify the existing operation → make its needs legible → tune buffers and offer timing → choose the next employee from observed friction → test one bonus opportunity**. Session length is one outcome, alongside enjoyable crafting, understandable choices and a clear reason to return.

Related: [[Design/Pottery Tutorial Review]] · [[Design/Core Loop Review]] · [[Design/Workshop Growth]] · [[Design/Alignment Review — 2026-10-23]] · [[Design/Game Design Document]]

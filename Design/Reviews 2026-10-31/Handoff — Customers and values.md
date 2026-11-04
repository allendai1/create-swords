---
title: Handoff — Customers and values
type: review
updated: 2026-10-31
tags: [handoff, shop, customers, deliveries, create-swords]
---

# Handoff — Customers, offers, deliveries and sword values (2026-10-31)

Builder agent's report. Everything built in Edit, **not played**. Session ended early: the sim part is not done (below).

## Allen's notes: diagnosis and what changed

### "only 1 offer at a time ... customer walk ins are linked to what is in the store" (Refinements 186–187)

**Why:** after the first sale walk-ins already came on the rate alone (45–75 s, Better Advertising, Sunshine, Promoter), but:
- a customer picked their sword **on the road**, and the cap (2 + Promoter + bays) counted them **until they had walked back out**. With 2 swords out, both customers held a sword each and every later walk-in was refused or found "nothing free".
- a walk-in who found every sword taken by another customer said "Nothing for sale yet?" and left, with swords on the shelf. His playtest log (`Development/sim/playtests/2026-11-01_000807.jsonl`, the 20:08 session) has 57 `browse` against 22 `visit`.
- one offer at a time is mostly the decided rate itself: a walk-in every 45–75 s (Economy Pass 2, 2026-10-27) with offers answered in seconds rarely overlaps. Rate unchanged; several cards at once was already allowed after the tutorial's two sales.

Note: "More Clients" is the mail's letters at once (Allen's own More features note), not shop customers; the shop cap stays WALK_INS 2 + Promoter + Rickshaw Bays (Decisions Log 2026-10-27).

**Changed (`ServerScriptService.ShopService`):**
- A walk-in chooses its sword **once inside** (`freeSword`, liked first). The tutorial's first-sale customer still claims it from the road, so no second customer waits beside them.
- Nothing free: they look over a holder no one has and **wait up to `BROWSE_WAIT` (8 s)** for a sword (one put out, another customer done), saying `Customers.LINES.wait` ("I'll wait my turn.") when the shop has swords, "empty" when it has none; then "later" and leave. `browseEmpty` is gone (now `browseFor`).
- **The cap counts only customers still shopping:** `sendCustomer` gives each ctx a once-only `free()`, called when their business ends (sale, walk-off, no answer, gave up), so one walking out makes room.
- Rickshaw riders can now also be browsers (they go back to their rickshaw).
- Shared out: `goTo` (to a holder's stand spot) and `walkOut` (back route, rickshaw or road).
- The first-sale "wait and ask again" and the ramp code (other agent) are untouched.
- `ReplicatedStorage.Shared.Customers`: new `wait` line pool.

### "at the forge it says 720 coins ... at the polishing station ... 1018" (line 184)

**Why:** the anvil's shape picker showed `basePrice × metal` only: the blade at ×1 grade with no hilt. A sword with every strike done is ×2 (`ForgeCheck`), plus its hilt (`Hilts.best(completed)`) and the full seat bonus (+6%). Allen's Steel Crescent Fang: 480 × 1.5 = 720 on the chip, 480 × 1.5 × 2 × 1.06 = 1,526 after forging (his Stone one, 1,018). The polishing station already shows the server's `SmithyCore.swordValue`.

**Changed (`StarterPlayer.StarterPlayerScripts.AnvilController`):** the chip is now `ValueFormula.value(basePrice, AnvilScore.MAX_MULTIPLIER, hilt bonus + seat bonus, metal)`: exactly what the sale pays for that sword forged with every strike, unpolished. New requires `AnvilScore`, `Hilts`, `ValueFormula`; `completed` comes from the smith state (`applyState`). Checked: Steel Crescent Fang at 0 completed = 1,526 (matches his polish card). An early finish (8 of 10 strikes) still sells for less than the chip. `StarterPlayerScripts.TestAnvil` (Studio-only) still has the old chip: not changed.

### "fix the deliveries, since i moved the board" (line 136)

**Why:** the board's invisible `Panel` (DeliveryPrompt, 9-stud reach, the trip timer `Status`, and DeliveryService's 14-stud REACH via `boardOf`) stayed at plot (26.4, −36); the board is at (26.4, −24).

**Changed (Studio, `Workspace.Plot.DeliveryBay.DeliveryBoard`):** `Panel` moved onto the board's papers (plot (26.84, 3.36, −24), facing like the board); `Status.StudsOffset` 2.6 → 3.8 so the timer floats over the board's top (y 6.06) instead of inside it. No code change: everything follows the Panel. `ServerStorage.Builders.build_delivery` still places the Panel at z −36 (leftover, not edited).

### "delivery offers seem to get new ones frequently?" (line 139)

**What it is:** offers never expire; **accepting refills the slot at once**; a skipped slot waits `Deliveries.SKIP_WAIT` (300 s). That matches what was decided (Deliveries.lua 2026-10-29: "Accepting refills at once"), so nothing changed.
**Proposal for Allen:** give an accepted offer's slot the same wait as a skip (e.g. 3–5 min), so the board fills at the pace of the cart rather than instantly. It needs `DeliveryService` (accept branch: `table.insert(s.waiting, now + Deliveries.ACCEPT_WAIT)`) and the sim's `task_cart` (it calls `cart_refill` at once).

### "not seeing the 'x wants this!' when i have a black iron quest" (line 150)

**Why:** with today's `needed` the line does show for his case: tested in Edit against fresh modules with a Black Iron Wakizashi mail order: "Jiro wants this!". His screenshot is from the 20:08 playtest; the Black Iron was rolled at about t = 1071 s and shows no pill. Either that playtest ran before the morning's fix, or the order was accepted or arrived after the roll: the line was only set when the ore landed.
**Changed (`ServerScriptService.ForgeService`):** `showWants(stand, d, material)` (above `reveal`), used by `reveal` and by a new 1 s loop over every roller's stands (after the Auto-Roll loop), so a waiting ore's line follows the mail. A stale giver id no longer errors (`Senders.get` nil → no line).

### NpcWalk: "Stocker stuck ... against goku19876 / Workshop.Shell.Post" (lines 130–131)

**Why:** both stalls are at plot (−5.1, −3.5): right outside the back doorway's post at x −3.2 with the Upgraded Store (the shell pushed to z −6). The Stocker was turning round that post (into the shop to Wall Rack 1's spot, and back out to the Sword Rack). Pathfinding's waypoints hug the post (0.3–1.4 studs from its edge in Edit, despite AgentRadius 1.75) and the body catches it. The player listed in the first warning was only nearby: NPCs and players don't collide (`Npcs`/`PlayerChars`), so no path-around-players code was added.
**Changed (Studio):** two `NavKeep` parts in `Workspace.Plot.Workshop.Shell` (they move with the shell), copies of the ore roller's `NavBlock` (invisible, no collision, PathfindingModifier `Avoid`), 1.6 × 3.6 × 1.6 round the doorway's posts at x −13 and −3.2. Path test in Edit (pathfinding service, the NPC agent): routes through the doorway now pass 2.1–3.8 studs from the posts (were 0.3–1.4) and still use the doorway. At 2.0 and up the doorway closed in Edit, but Edit has Display Table 5 standing in it (locked tables have no collision in Play), so 1.6 is the safe value. **Not checked in Play or on other lots.**

## Shop map review items

- **#1 stand spots:** each rack/table holder has its own spot. `InspectPoint2/3` added beside each `InspectPoint` (copies), Slot2/Slot3's `Inspect` re-pointed; 2 studs apart along the holder's face. Wall racks along z (e.g. Wall Rack 1: 20, −39.3 / −37.3 / −35.3), tables along x (−14/−12/−10 and 10/12/14), Display Table 3 at 12/14/16 (clear of the coin chest), Back Wall Rack (WallRack5) 14.8/16.8/18.8. Big Sword Stand unchanged (one holder). No code change (`register` and `goTo` read each slot's own `Inspect`). Table spots at ±2 stand about 1.3 studs from the table's front legs; the customer's body sits in front of them, not in them.
- **#5 walk-ins fade:** in and out over 1.2 s (`fade` in ShopService: tweens every part's and decal's transparency from its own base, root stays hidden; out starts so it ends as they reach the road spot). Rickshaw riders keep the Rickshaws fade (the bay is now taken before the NPC is made, so the two never mix).
- **#10 kanban:** both shops' `Kanban.SurfaceGui.TextLabel` → GothamSSm Heavy with a 3 px `UIStroke` (18, 12, 8). PlotService still writes only `.Text`.
- **#11 Rickshaw Bay 3 / lamp:** already fixed by the village agent (lamp at x 25.25, foot clear of the slab's 23.25). Not touched.
- **#12 planter:** left (Allen's trees later).

## Checks run

- ShopService, ForgeService, AnvilController compile (wrapped in a function) after the last edit.
- New locals declared before first use: ShopService `TweenService` 1024, `FADE` 1025, `fadeBase` 1026, `fade` 1027, `BROWSE_WAIT` 1049, `freeSword` 1052, `goTo` 1071, `browseFor` 1085, `walkOut` 1118, all above `runCustomer` (1148); ForgeService `showWants` 342, used 376 and 667, `needed` 322, `rollers` 201; AnvilController `AnvilScore`/`Hilts`/`ValueFormula` 49–51, `completed` 115.
- Customers loads from a fresh clone; `line("wait")` works.
- `needed` with a Black Iron mail order → "merchant" → Jiro.
- Anvil chip formula: Steel Crescent Fang 1,526 / 1,670 / 2,102 at 0 / 5 / 15+ swords completed.
- Stand spots: 22 new spots listed; collision scan only hits table legs within 1.75 and the Edit-only shell overlap for the Upgraded racks.

## NOT done (session ended)

- **Sim:** not changed, not re-exported, tests not run, no `customers-2026-10-31` run. To mirror: `engine.on_spawn`'s browse branch should hold `inshop` for `there + BROWSE_WAIT` (not `2 * there + 2.5`), since walkers-out no longer count; add `browseWait = tonumber(grab("ShopService", "local BROWSE_WAIT = (%d+)"))` to `ServerStorage.Builders.ExportBalance`'s `B.shop` (the ramp agent is editing those lines too), re-export, `python -m unittest`, then `python run.py --name customers-2026-10-31 --players 150 --hours 2` against `Development/Sim Runs/final-2026-10-30.md`. The sim already frees a sale's room at the sale. No rate or delivery timing changed, so nothing else to mirror.
- Delivery accept wait: proposed only (above).
- No screenshots/renders (the Panel, kanban and spots were placed by numbers).
- `PolishController`: no change needed (its value is the server's).

## Outside my fence, seen

- `ServerStorage.Builders.build_delivery` still builds the Panel at z −36.
- `StarterPlayerScripts.TestAnvil` keeps the old ×1 chip.
- ShopService's line numbers moved under me (the ramp and first-offer agent); all my edits were exact-string multi_edits on fresh reads.

## What to test in Play

1. Put 1 sword out after the tutorial, wait: a second walk-in should come in, say a "wait" line, stand at its own spot ~8 s, then leave. Take the first customer's offer quickly: the waiting one should go for the next sword if you put one out.
2. With 2+ swords out, check customers keep coming while others walk out (more than two people around at times), and several offer cards can be up at once.
3. Walk-ins fade in on the road and fade out as they leave; rickshaw customers look as before.
4. Two customers at the same rack or table stand side by side, not inside each other.
5. Anvil shape picker: note the chip, forge with all strikes, check the polishing station's "now" value matches it.
6. Delivery board: the E prompt appears standing in front of the papers; the trip timer floats just over the board.
7. Roll a metal a mail order wants: "<name> wants this!" under it. Also roll first, then accept the order: the line should appear within a second.
8. Stocker with the Upgraded Store: watch it go through the back doorway several times; no "NpcWalk: Stocker stuck" by the post. Check its route isn't sent round the front door instead.
9. The tutorial's first sale: still exactly one customer, the fair offer, and nobody else waiting.
10. Kanban name in GothamSSm Heavy with an outline, both shops.

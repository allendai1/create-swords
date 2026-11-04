# Handoff — Upgrade progression (2026-10-31)

Builder agent, Allen's playtest notes in `Refinements.md` (lines 152, 155, 157, 160, 176, 189). Built in Edit, **not played**.

## What caused each note

Every note has the same cause: the pad cap from 2026-10-30. Only the 3 cheapest pads whose gates are met stand (`TycoonService.standing`, `PAD_CAP` 3). So the dearer next level of a chain you had already started dropped off the floor whenever cheaper pads elsewhere took the 3 places. I checked this by running the old `standing` logic on test plots in Studio:
- **Line 152, Faster Heating:** with Heat I bought, the cap showed Back Wall Rack 900, Etching Table 1,580 and Ore Slot 4 2,000. Heating II (3,000) was hidden behind Ingot Rack 2 and Faster Strikes II (both 2,000). It wasn't gated on Ore Slot 3. It was simply the 4th–6th cheapest pad.
- **Line 155, "bought everything in the base shop, nothing to buy":** with Wall Rack 2, Display Table 1 and the Back Wall Rack bought, the Upgraded Store (6,000) came 8th by price. The cap showed Etching Table, Ore Slot 4 and Ingot Rack 2, so the shop dead-ended until yard pads were bought.
- **Line 157, Display Table 5 after the Cashier:** it never needed the Cashier (it comes after Display Table 4 only). At 80,000 it was the dearest pad on offer, the last of 8 hidden. Buying anything, the Cashier included, moved it up the queue.
- **Line 160, the employee pad:** Anvil 2 (the crew's first pad) needs the Ingot Rack, Furnace 2 and the Sword Rack. Furnace 2 needed **Faster Heating III**, which is the "upgrade them fully" in Allen's note. Then the cap hid Anvil 2 as well (the 2026-10-30 "Keep the cap" ruling).
- **Line 176, the 6th ore slot:** after one merge, Ore Slot 6 costs 20,000 × 1.5 = 30,000. It was hidden behind the Ingot Rack 460, Faster Strikes I 500 and Back Wall Rack 900. It had no merge-count limit and no gate.
- **Line 189, "ore 3 then can't buy 4 but ingot rack is available":** Ore Slot 4 (2,000) came after the Ingot Rack (460) by price.

## What changed (in Studio)

1. **Chains** (`ReplicatedStorage.Shared.Upgrades`): new `Upgrades.CHAINS`, `Upgrades.chainOf` and `Upgrades.chainStarted(plot, u)`, placed after `byId`. Once one upgrade of a chain is bought, whatever else of that chain is on offer always stands, whatever the cap. For the Ore Slots a merge also counts. The cap now only picks which **new** chains open. The chains:
   - Ore: Ore Slots 2–6 and Merge
   - Ingot Rack: Racks 1 and 2
   - Sword Rack: Racks 1 and 2
   - Heat: Heating I–III
   - Furnace 2: the furnace and its Heating I–III
   - F3Heat: Furnace 3's Heating I–III
   - Strikes: Faster Strikes I–V
   - Polish: Polishing Station 2 and Polish Boost I–III
   - Crafters: Anvil 2, Sword Crafter, Anvil 3, Furnace 3 (Haru waits for it), Anvil 4
   - Etcher: Etching Table 2 and the Sword Etcher
   - Shop: Wall Rack 2 → Display Table 1 → Back Wall Rack → Upgraded Store, then Wall Racks 3–4, Display Tables 2–6 and the Big Sword Stand
   - Parking: Bays 1–3

   The blueprint chains already stood, and still do.
2. **`ServerScriptService.TycoonService.standing`**: adds `or Upgrades.chainStarted(plot, u)` next to the blueprint and `PAD_ALWAYS` check. `PAD_ALWAYS` is now `{ Delivery, Anvil2 }`. The other agent's "no sword pad until TutorialDone" guard is kept.
3. **Gates removed** (Allen: "once an upgrade is available, it shouldn't then be locked behind something else"). Each of these sat partway along a chain:
   - Furnace 2 waits for **Heating I**, not Heating III. This supersedes the Refinements 5 ruling "Furnace 2 only after Faster Heating III".
   - Sword Rack 2: the Katana gate is gone.
   - Anvil 4: the Stocker gate is gone.
   - Claymore: the Rapier gate is gone (it waits for the Zanbatō only).
   - Rickshaw Bay 2: the Longsword gate is gone. Bay 3: the Falchion gate is gone.
   - Sword Etcher: the Gladius gate is gone. It was redundant, since its table already waits for the Gladius, so nothing changes in play.
4. **Base stations, and what I chose:** today's gates define "base stations" as Anvil 2's requirements: the Ingot Rack, Sword Rack and Furnace 2, which are the crafter's input, output and own furnace. I kept those three. Furnace 2 now needs only Heating I, and **Anvil 2 always stands once those are bought** (`PAD_ALWAYS`), with the Sword Crafter right after it as the next pad in the Crafters chain. This supersedes the 2026-10-30 "Keep the cap" ruling for the crafter.
5. **Gates kept**, all at the start of a chain, never partway along:
   - Ingot Rack after Ore Slot 2.
   - Faster Strikes I after the Wakizashi.
   - Polishing Station 2 after the Etching Table.
   - Zanbatō after the Gladius and the Big Sword Stand (it sells only on the stand).
   - Cashier after the Upgraded Store and the Stocker (his post is in the Upgraded Store; this is a crew pad waiting on the shop, not the other way round).
   - Shop Promoter after Display Table 1 and the Longsword.
   - Rickshaw Bay 1 after Display Table 1 and the Katana.
   - Etching Table 2 after the Etching Table, Sword Rack and Gladius.
   - Stocker after the Crafter.
   - Furnace 3 after Anvil 3.

   **The shop chain waits only on itself**, so Display Table 5 never needs the Cashier.
6. **Pads moved** (`Workspace.Plot.Pads`, marker parts only, Y and rotation kept):
   - Ore Slot 2–6 and Merge → (−9, 9)
   - Heating I–III → (−25, 36)
   - Furnace 2 Heating I–III → (−25, 44)
   - Furnace 3 Heating I–III → (−25, 52)
   - Sword Crafter → (−4.3, 57.5)
   - Zanbatō, Claymore and Flamberge → (−12.5, 55)
   - Stocker → (23.5, −9.5), 5 studs from the Sword Rack's pad. It still moves back with the wall: it's in the strip and tagged Workshop.

   **The pad base** (`ReplicatedStorage.PadParts.Base`) is now the hearths' charcoal (58, 54, 54).
7. **Test and builder outside the fence** (both needed for this change):
   - `ServerStorage.Tests.SaveSpec`: "Furnace 2 comes after Faster Heating III" became "…Faster Heating I". I added a check that, past its first upgrade, each chain waits only on itself, that Heat I begins its chain, and that a merge begins the Ore Slots'.
   - `ServerStorage.Builders.ExportBalance`: now exports `B.chains`.
8. **Sim** (`Development/sim`):
   - `rules.Balance.chain_of`.
   - `engine.offers` keeps the next pads of every chain already started, past the cap.
   - New test `test_begun_chains_stand_past_the_cap`.
   - `scenarios` `cap1`–`cap5` now cap only new chains and keep the exported `padAlways`.
   - Re-exported `balance.json` with ExportBalance in Edit (the receiver on 8765 was already up).

## Checks run
- Upgrades loads from a fresh clone (86 upgrades). TycoonService and SaveSpec compile with the wrapper. My new SaveSpec checks pass when run on their own. The whole SaveSpec wasn't run, because it requires SmithyCore.
- Chain rule check: every chain past its first upgrade waits only inside itself. 0 violations after the Etcher fix.
- Standing, re-run on the same test plots with the new rule:
  - Heating II stands.
  - The Upgraded Store stands with the base shop done.
  - Display Table 5 stands.
  - Ore Slot 6 stands after a merge.
  - Anvil 2 stands with the base stations bought.
  - A new plot (tutorial done) still shows 5 pads.
- New pad spots: no parts in the pad's box (the Stocker spot touches only the hidden Upgraded Store shell, and is clear once pushed to (23.5, 2.5)). The Crafter pad is now 8.84 from Anvil 2's prompt, past its reach of 8 (it was 6.84). **The heat pads are still 9.06 from their furnace's prompt (reach 9.75)**, so the Heat prompt still shows while you stand on the pad. I followed the map review's spot, which judged the screen clash cleared; check it on a phone.
- Sim tests: `python -m unittest` 39/39.
- Sim runs, 150 free players a type (`Development/sim/results/`). The "before" runs use the pre-change `balance.json`.

  | | efficient | manager | grinder | casual |
  |---|---|---|---|---|
  | Sword Crafter, 4 h runs, before → after | 2:03 → 2:12 | 1:46 → 1:52 | 2:17 → 2:18 | over 4 h, both |
  | Sword Crafter, 12 h runs, before → after | 2:03 → 2:12 | 1:46 → 1:52 | 2:17 → 2:18 | 4:21 → 4:20 |
  | Waits over 15 min, 4 h runs, before → after | 2 → 1 | 2 → 1 | 0 → 0 | 2 → 2 |
  | Longest wait, 4 h runs, before → after | 24 → 16 min | 23 → 15 min | 13 → 13 min | 18 → 17 min |
  | Waits over 15 min, 12 h runs, before → after | 16 → 16 | 16 → 16 | 14 → 15 | 17 → 17 |
  | Zanbatō, 12 h runs, before → after | 2:59 → 4:14 | 2:39 → 2:53 | 4:07 → 4:51 | 11:42 → 11:47 |

  - The runs: `progression-2026-10-31` (the brief's run) against `progression-before-2026-10-31`, both 4 h; `progression-12h-2026-10-31` against `progression-before-12h-2026-10-31`, both 12 h.
  - The "before" runs match `Sim Runs/final-2026-10-30` exactly (2:03 / 1:46 / 2:17 / 4:21).
  - The Zanbatō is later because with more pads standing, efficient players buy side pads before climbing the sword chain. Its target was about 4 h.
- **Pads on the floor over time** (scratch `padcount.py`, 30 players a type, 8 h):

  | | Hour 1 | Hours 2–3 | Hours 4–5 | Hour 8 | Most at once |
  |---|---|---|---|---|---|
  | Before | 4–5 | about 4 | about 4 | 4–5 | 5 |
  | After | 9–10 | 9–10 | about 8 | 5–7 | 12 |

  **That is about double the floor Allen trimmed on 2026-10-30.** Lowering the new-chain cap barely changes timing: `progression-cap-2026-10-31`, cap 1 or 2, gives the crafter within 2 min and the Zanbatō within 1 min. I didn't measure the pad counts at cap 1 or 2. Fewer new chains would at most take 1–2 pads off those counts.

## Not done
- Vault notes (Session, Decisions Log, Code Map, Tycoon Upgrades) aren't updated: that's the main session's job. The Decisions Log needs these supersessions: Refinements 5 "Furnace 2 only after Faster Heating III"; 2026-10-30 "Keep the cap" for the crafter; the 2026-10-28 stage gates on Sword Rack 2, Anvil 4 and Rickshaw Bays 2–3; the Claymore waiting for the Rapier.
- `TycoonService`'s header comment still says "4–5 pads at a time".
- No `Sim Runs/progression-2026-10-31.md` note written; the numbers are above.
- Map review finding 11 (anvil block materials) is outside my fence and not done.
- The sim doesn't model `available`'s Ore Slot 2 merge exception (it existed before this change).

## Open questions for Allen
1. About 9–10 pads now stand in the first hours (4–5 before). Keep the new-chain cap at 3, or lower it to 1? Timing is the same either way.
2. Is Furnace 2 after Heating I right, or should it need nothing at all?
3. The efficient Zanbatō moves 2:59 → 4:14. Is that fine against the 4 h target?

## What to test in Play
- Buy Faster Heating I with lots of cheap pads around. Heating II must stand right away, then III.
- Buy Wall Rack 2, Display Table 1 and the Back Wall Rack. The Upgraded Store pad must stand straight after, then Wall Rack 3, Display Table 2 and the Big Sword Stand together.
- Display Table 5 stands right after Table 4, without the Cashier.
- Buy Ore Slots 2–6, merge, and buy them again: each next slot, the 6th included, always stands at (−9, 9), clear of the lever's walk and the Roll prompt.
- Buy the Ingot Rack, Sword Rack, Heating I and Furnace 2: Anvil 2's pad must stand, then the Sword Crafter's pad at (−4.3, 57.5) without Anvil 2's prompt over it.
- The heat pads beside the furnaces, not in front of their mouths. Check on a phone whether the Heat prompt and the Buy button clash.
- The Zanbatō pad at (−12.5, 55). The Stocker pad 5 studs right of the Sword Rack's, and both after the Upgraded Store push.
- The darker pad base reads well on the gravel.
- How the floor feels with more pads standing.

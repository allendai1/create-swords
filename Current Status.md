---
title: Current Status
aliases: [Next Session Handoff]
status: active
type: status
updated: 2026-10-19
tags: [status, create-swords]
---

# Current Status

Current project snapshot, consolidated from the latest saved build notes on 2026-10-19. This is a documentation reconciliation, not a new Studio inspection or fresh test run. See [[Design/Game Design Document]] for intended behavior and [[Development/Code Map]] for implementation details.

## Built and recorded

- **Browser forge study and profile editor:** tantō, wakizashi, and katana; 12 untimed strikes to 90%, safe grinding to 100%, grinding map, blueprint selection, save/load, and profile editing. Source and run instructions: [[Prototypes/tanto-forge/README.md]].
- **Roblox BladeCore port and anvil integration:** the new blade data drives forging, optional grinding, server Finish checks, and held/displayed blade rendering. Old prototype modes are preserved in `ServerStorage.Legacy`.
- **Japanese smithy rebuild:** workshop, forge, hornless anvil, ore-shrine visuals, hilt bench, and three display pedestals rebuilt. Latest smithy note records that Allen saved the place. See [[Art/Smithy Redesign]].
- **Plot redesign (2026-10-20, playtested):** a low-poly Blender shop is the only building; the crafting stations work outdoors on a stone-flag courtyard 8 studs east of it, with new bamboo and standing stone lanterns. See [[Art/Building Redesign]].
- **Later 2026-10-20 batch (not playtested yet):** forging gives 100% and a full polish adds +10% value; hilt seated by three knocks; one-piece anvil; unlimited ore re-rolls; wider Upgraded Store with a roof that fades inside (Starter Shop staged only); Ingot Rack and Finished Sword Rack. See [[Development/Code Map]].
- **Polishing Station (recorded 2026-10-20):** final polishing on a completed sword supports 90% → 100%; the recorded playtest saved a Steel Katana at 97%. The anvil auto-finished a tantō at 90%. The reroll lever hold animation and enlarged ore display were also tested. The session records Allen saving after this work, covering the earlier imports, guards, etch and picker changes. These are recorded results, not checks rerun here.
- **Blender stations in the game (recorded 2026-10-20):** mid-high forge, lowered anvil, ore stand/lever, hilt bench and three blade-down universal holders replaced the part-built ones. Initial import notes reported Play blocked; the subsequent polishing session tested forging and rolling, but a full post-import heat → hilt → all holders → customer sale loop and final picker framing remain unverified. See [[Art/Blender Station Review]] and [[Sessions/2026-10-19]].
- **Recorded validation:** the port note reports 31 Luau checks; the editor notes report a broader 65-test browser suite. Anvil integration and the later smithy rebuild have recorded Studio playtests; the latter completed roll → heat → katana forge → hilt → display → customer sale. These are historical results, not checks rerun during vault organization.
- **Player plot (one, v2):** the L-shaped property, 126 × 78 studs: storefront wing with tall holders along an aisle, a deep 50 × 28 crafting pavilion with the anvil on open floor in front of the forge, courtyard with work apron, expansion lawn, fence, gate and village road. Reworked from [[Art/Player Plot Review]]; playtested roll → heat → katana → hilt → display → customer walks in and buys. See [[Development/Code Map]] (`Workspace.Plot`) and `References/Player Plot/`.
- **Town street (2026-10-21, awaiting review):** `Workspace.Village`, a 790-stud Japanese street with 26 townhouses, six empty plot lots, a gate, a shrine and the cliff-ring mountains, north of the current plot pieces. The plot has not been moved into a lot. See [[Art/Japanese Street]].
- **Concept art:** large connected storefront/crafting plot, labeled overhead layout, early/mid/late progression, and transparent cutout are saved in [[Art/Japanese Village Concept Art]]. These are visual directions; the full six-player village and large plot progression are not recorded as built.

## Design versus implementation gaps

| Area | Agreed design | Latest documented build |
|---|---|---|
| Heating | 10 seconds | ForgeService still uses 15 seconds |
| Ore Roller | Shared lever rolls empty stands; results wait for collection | Built 2026-10-20: the lever spins every empty stand (2.6 s reveal), results wait until collected, occupied stands skip. One stand; buying more stands is still to do |
| Etching | Optional +15% finish; approved interim flow is free and instant, trace minigame deferred | Flame v4 and table are built; prices, trace minigame and persistence remain future work ([[Art/Flame Etch]]) |
| Polishing | Optional step on the assembled sword before etching; a full polish adds +10% value; forging alone gives 100% | Dedicated station built; recorded partial-polish save at 97%. Full 100% walkthrough and final sound/stone feedback remain validation/polish work |
| First session | Starter tantō → first listing triggers fair-price customer → Iron Wakizashi commission → second ore stand | Tutorial/commission progression not recorded as implemented |
| Hilt assembly | Three untimed taps, tradition-matched fittings | Built 2026-10-20: three untimed knocks slide the hilt onto the blade; full seat bonus always. Playtest pending |
| Player properties | Six players with spacious retail/crafting plots and expansion | One spacious plot built (126 × 78: storefront, crafting pavilion, courtyard, lawn); six plots, plot assignment and the village surroundings remain future work |
| Saving | Persistent inventory, currency, unlocks, and upgrades | Latest Code Map says session-only |
| Employees | Five professions: furnace operator, smith, finisher (hilt + optional polish), stocker and cashier. Separate bare-blade/finished-sword racks; stock only ready-for-sale swords. Starter smiths train toward 90%; player can finish both stages | Roster and handoffs confirmed in [[Design/Workshop Growth]]; no employee production, stocking or sub-90% recovery implementation recorded. Separate hilter/polisher question is resolved |
| Remote orders | Separate delivery board with courier/cart, packing, return payout, and speed/capacity upgrade directions | Design confirmed; no delivery system recorded. Direct commission hand-in stays separate |
| Weather | Sunshine can boost traffic; other weather stays at normal baseline | Design confirmed; no weather-to-traffic implementation recorded |
| Roof visibility | Fade/hide roof indoors and restore it outside | Requested direction and reference screenshots recorded; not recorded as implemented |

## Next work

1. Finish post-import and Polishing Station checks: camera/strike feel, full final polish, picker framing, all blade lengths on holders, and customer traversal. Tune polish incentive; the current 12 hits and blueprint prices remain tuning values.
2. Bring heat duration and hilt assembly into line with the design, implement additional stand purchases, then complete the tutorial/direct-commission loop. Ore roll/collection behavior is already recorded as built.
3. Reduce per-sword EditableMesh resource pressure and test published clients, phones, and multiplayer observers.
4. Build six-plot assignment (per-player stations instead of the shared `Workspace.Smithy`) and the village surroundings after the first-session loop is stable. One spacious plot already exists as the template.
5. Finish plot comfort validation before six-plot replication. The deeper pavilion, wider bays and revised displays from [[Art/Player Plot Review]] are already built; full camera rotations, phone framing and six-plot fit remain open.
6. Plan the confirmed growth work in [[Design/Workshop Growth]]: employee production/training and player completion, separate courier orders, bonus-only weather traffic, and indoor roof visibility. Prices, timers, capacity and employee quality curves remain untuned; these additions are not recorded as built.

Active tasks: [[Development/Roadmap]]. Open design questions: [[Design/Decisions Log#Current open design work]].

## Resume and reference

Run the browser study from the **vault root**:

```bash
python3 -m http.server 8765 --directory Prototypes/tanto-forge/dist
```

Open `http://localhost:8765`; `editor.html` opens the profile editor. Use a Python executable available on the machine.

The registered private Site is `appgprj_6ad655f29424819195e6e42693b729ae`, recorded in `Prototypes/tanto-forge/.openai/hosting.json`. The saved notes do not record a deployment. Reuse that identity if publication is resumed; obtain fresh credentials rather than storing tokens in notes.

Detailed earlier questions, test history, and port notes are preserved in [[Archive/Project History/Handoff before vault organization — 2026-10-19]]. Daily activity belongs in [[Sessions/2026-10-19]], rather than being appended to this status note.


Sword shelf - remove the sakura decoration. The sword holder is not centered. it skews to the left. the + icons are not at the right shelf position. they should be inbetween the left and right holders. If a sword is short like the tanto, it the sword holder positions should adjust so that it looks like the sword is still resting on the holder. The front piece of the sword holder should be less tall, otherwise it blocks part of the blade. the blade should be the highlight.

Sword Table - I inported a SwordTable. I want to use that in replace of our current one. Wire up the swords to be on it. Also make sure again the + icons are in between the holders and at the right levels.

Also I like the table style of having bevels on the edges.


NPC - names should not be shown on the NPCs. Their offer GUI is visible from anywhere. It should be based on proximity. For the GUI. instead of having the timer under the price, have the timer on the same row as the name, on the top right. Remove the description of "They love it" for example.

I can see the beams and the lights while the roof is invisible.

For the stations:

- Enlarge the main tool or work surface of each station so players can recognize its purpose at a glance.
- Decorate the empty walls with station-specific racks, shelves, tools, and sample swords.
- Add three overhead station signs or Japanese-style hanging banners, integrated into the wooden architecture.
- Introduce subtle spacing and divider beams only if the stations still look too similar.

→ Done 2026-10-22 (not played yet): [[Sessions/2026-10-22#Refinements]].
→ Stations done 2026-10-22 (not played yet): [[Sessions/2026-10-22#Station refinements]].

## Found 2026-10-23 (code and place audit, not played)

Allen: "look for more refinement or improvement areas." Three reviewers read the live scripts (UI, crafting stations, server), and the place was checked for z-fighting, prompts, lights and anchoring. Studio's viewport rendered black, so there was **no visual pass**: look-and-feel notes like the shelf ones above still need screenshots or Allen's eye. Items already in [[Design/Alignment Review — 2026-10-23]] (sound, polishing gamepad, offers timing out mid-craft, etch hitches, economy) are left out. Pick by number; 1–5 were fixed the same day.

**Bugs**

1. **Leaving polishing throws the work away.** Q or Leave drops every stroke; the next visit starts dull again. The anvil keeps a half-forged blade. *Fix:* send the partial polish on leave (the server already accepts partial polish). `PolishController:272` → **Fixed 2026-10-23, not played** ([[Sessions/2026-10-23#Refinement bugs 1–5 fixed]]).
2. **The hilt seat has no way out.** No Q, B or on-screen button, so a wrong hilt can't be backed out of. The bench's own "E" bubble sits in the seat view, the Polishing Station's prompt (7 studs away) can open over it, and dying mid-seat isn't handled. `HiltBenchController:93–277` → **Fixed 2026-10-23, not played** ([[Sessions/2026-10-23#Refinement bugs 1–5 fixed]]).
3. **The crafter's furnace looks free.** While the crafter heats an ingot, the slot has no `OwnerId`, so you press E, pick an ingot, and only then hear "The forge is full"; the guide can point you there too. `ForgeService:597`, `ForgeController:86`, `Guide:132` → **Fixed 2026-10-23, not played** ([[Sessions/2026-10-23#Refinement bugs 1–5 fixed]]).
4. **The crafter can take the Polishing Station from under you.** It only sees you within 7 studs, but the prompt opens from 8 and the server allows 12; that polish is then lost. *Fix:* mark the station busy from start to save. `EmployeeService:340`, `PolishService:19` → **Fixed 2026-10-23, not played** ([[Sessions/2026-10-23#Refinement bugs 1–5 fixed]]).
5. **Customer speech overflows its bubble.** A fixed 200×40 label without wrapping; "I need a Katana. Let me show you how." is about 290 px wide, right when the tutorial needs it read. `ShopService:438` → **Fixed 2026-10-23, not played** ([[Sessions/2026-10-23#Refinement bugs 1–5 fixed]]).
6. **Phones:** the Deliveries window shrinks to about 7 px text and 21 px buttons; hotbar slot 9 and the bag sit under the jump button; the pinned delivery order covers hotbar slot 1. `DeliveryController:461`, `Hotbar:338`, `DeliveryController:545` → **Fixed 2026-10-23, not played** ([[Sessions/2026-10-23#GUIs moved into StarterGui]]).
7. **Gamepad D-pad left opens the Gem Shop over any window** (picker, Deliveries), and the gem and book buttons can stack a second window over the picker. `GemController:273` → **D-pad half fixed 2026-10-23**; tapping the gem or book button can still open a window over a picker ([[Sessions/2026-10-23#GUIs moved into StarterGui]]).
8. **The cart stays home** if a delivery is sent while it's still rolling back in (3 s), and old crates stay on it. Pay and timing are right. `DeliveryService:110`
9. **The crafter stands at Furnace 1 while its ingot glows in Furnace 2.** `EmployeeService:306`
10. **A save from a newer version** kicks the player without releasing their lock, so their next join waits about 30 s. `SmithyCore:836`

**Friction**

11. **The anvil's ending can't be skipped:** about 3.5 s after strike 12 (cool tween, server, a fixed 2.5 s wait), then it always sends you out, even with more hot ingots in hand. *Fix:* any strike input skips; reopen the ingot picker if you hold one. `AnvilController:53, 582–601, 933`
12. **Forging is slower than it needs to be:** the blade slides after each recovery instead of during it, so about 45% of each strike is waiting. Running both together saves about 3.5 s a sword (server floor 0.35 s a strike). `AnvilController:627–648`
13. **Collecting ore takes one E per slot,** with a toast each: six presses and six toasts at 6 slots. *Fix:* one press collects all (up to the hand limit), one summary. `ForgeService:351–388`
14. **The rack window closes after every store or take,** so moving six ingots is six rounds. `RackController:42–86`
15. **Every station leaves differently:** anvil Q/B and a button; polish Q only and a mouse-only Save; etching Q/Backspace/B; the hilt seat nothing; pickers close only with B or ×. *Fix:* one rule everywhere: Q/Backspace/B leaves, Space/Enter/A confirms. `ItemPicker:428` → **Pickers now close on Q/Backspace/B (2026-10-23)**; the hilt seat got Q/Backspace/B earlier the same day; polish Save still has no key ([[Sessions/2026-10-23#GUIs moved into StarterGui]]).
16. **Polish at 100% needs the Save button hunted down.** *Fix:* save on its own when the edge is done, with a shine sweep. `PolishController:364`
17. **Messages repeat what you just saw** (minimal-text rule):
    - "Sold X to Y for N coins", "X is on display", "X is back in your inventory", "Iron ingot collected", and "Hot Iron Ingot! Take it to the anvil" every time.
    - Hilt, polish and etch each show a success toast and the reward card.

    *Fix:* keep notices for failures, the reward card for successes. `ShopService:179, 233, 771`, `ForgeService:384, 570`, `HiltBenchController:288`, `PolishController:373`, `EtchingTableController:95, 174`
18. **The daily-reward window opens on a new player's very first join,** before the first roll, covering the guide line. *Fix:* hold it until Ore Slot 2 is bought. `GemController:281` → **Fixed 2026-10-23, not played** ([[Sessions/2026-10-23#GUIs moved into StarterGui]]).
19. **Take back is a hidden 0.5 s hold.** The custom marker shows no progress, so a tap seems to do nothing; gamepads see no button. *Fix:* a tap, like the + marker. `ShopController:363`, `ShopService:199`
20. **The forged panel says "polish it at the Polishing Station"** even before one is bought (the real next step is the hilt bench), and shows the base price (20) for a sword worth about 42. `AnvilController:549`
21. **"Can't afford" works three ways:** a silent brown button (Gem Shop), a green button then a bottom toast (cart), a green Buy then a top notice (pads). *Fix:* grey out what you can't afford, everywhere. → **Gem Shop and cart fixed 2026-10-23** (veil + shake); the pads' server notice is unchanged ([[Sessions/2026-10-23#GUIs moved into StarterGui]]).
22. **The crafter window says "Locked" without a reason;** the hilt picker says "Locked · 10 swords". *Fix:* "Forge one first". `EmployeeController:84`
23. **The Polishing Station while the crafter uses it:** you pick a sword, then get "Couldn't start polishing, try again". *Fix:* the prompt says the crafter is using it. `PolishController:290`
24. **The Deliveries prompt shows through the shop wall** at Wall Rack 1 (4.7 studs, line of sight off on every prompt). *Fix:* turn line of sight on for the delivery board.

**Juice and polish**

25. **The finishing blow is like every other strike** (14 sparks, same clang). *Fix:* a bigger burst, a deeper clang, a short push-in. `AnvilController:624`
26. **A Legendary lands in the loot box like an Iron** (same pop, only the light colour differs). *Fix:* lock the rarest last, slower, with a bigger pop and particles for Epic and up. `OreBoxShow:97`
27. **Thin payoffs at the hilt and the etch:** the hilt seats with a clang and a 0.18 s nudge; the finished etch is on screen for 0.4 s. *Fix:* a spark puff at the collar; about 1.2 s to admire the etch, skippable. `HiltBenchController:192`, `EtchingTableController:33`
28. **Station cameras cut** in and out at all four stations. *Fix:* a 0.25 s blend.
29. **Buying an upgrade has no moment:** the pad vanishes and the item pops in. *Fix:* fade or grow it in over 0.4 s with a small burst. `TycoonController:23`
30. **Money is written three ways:** "$4514 [+20%]" on the offer bubble, "4000 coins" on pads and notices, "4,000" with the coin icon in the HUD and windows. *Fix:* the HUD's style everywhere. → **Client screens fixed 2026-10-23**; pad labels and server notices still say "N coins" ([[Sessions/2026-10-23#GUIs moved into StarterGui]]).
31. **The board's "New order · in m:ss" doesn't count down** while open, and an order that arrives isn't added. `CommissionController:144`
32. **Prompt labels are inconsistent:** Anvil 2 says "Sword Crafter" as its action, the board says "Requests" with no name; the rest read verb + station ("Use forge · Forge").
33. **Mobile hitch risks:** each polish drag recolours about 780 points and rebuilds the brackets; forging hides your body by walking the character every frame. `PolishController:346`, `AnvilController:980`

**Server hardening (low)**

34. Forge, hilt, commission and order remotes don't check your plot or distance: an exploit could make swords from anywhere, faster but worth no more per sword. `SmithService:46`, `ShopService:614`
35. Three read calls aren't rate-limited (state, rack list, gem state). `SmithService:120`, `RackService:96`, `GemService:23`

**Checked and fine:** no z-fighting on the plot or village (only the alternate shop shells overlap, and they never show together); 18 plot lights with 2 shadow casters; no stray unanchored parts; no double-spend, cross-plot or save-field gaps; order, trip and streak clocks are server-side; DevTools is Studio-only.

# Handoff: Allen's UI notes (Refinements.md 100, 119, 162–181), 2026-10-31

Built in Edit, **not played**. All edited scripts pass the compile check (the Script/LocalScript wrapper; modules required as fresh clones): EmployeeController, MailController, AutoRollController, PromptStyle, MenuController, DevPanel, UiFx, PackOffer.

## Done

1. **Crew level-up button** (line 100, "lvl 4 -> lvl 5 and then 105 gems with the icon below"). `CrewGui.Window.Stats.Panel.LevelUp` and `Staff.Panel.LevelUp` are now 170 × 62. `Row` is a vertical list: `Row.Next` reads "Lv. 4 → Lv. 5" (22 pt, fixed 160 × 26), and under it `Row.Price` holds the gem icon and `Gems`. The hidden coin icon and the gap are gone. Script: `EmployeeController.showLevelUp`.
   - **"Lv." everywhere** (style review #17): the cards, the Stats and Staff panels (4 script lines and the template texts) now say "Lv. N", not "Lvl. N".
2. **Tap, then confirm** (lines 178–181).
   - `ReplicatedStorage.WorldText.LevelPrompt` HoldDuration is now 0.
   - A tap opens the new `CrewGui.Confirm`: a dim plus a small 460 × 214 window cloned from the crew window's frame. Its title is "Level Up", the line reads "<name> to Lv. N?", and the green button shows the gem icon and the price. The red X, B or Escape close it.
   - The button sends `Employee("level", id)`. If you're short of gems it shakes and opens Roblox's own Robux prompt for the smallest pack that covers the gap. The window stays open so you can confirm after buying.
   - Code: `EmployeeController`, new block after `LEVEL_PROMPT`; `PromptTriggered` now calls `openConfirm`.
3. **No more custom pack popup** ("it should just pop upon the official roblox buy with robux").
   - `PackOffer.offer` now calls `MarketplaceService:PromptProductPurchase` for `Store.packFor`'s pack directly.
   - The other agent's `MyPlot.lessonsDone` gate is kept as it was.
   - `StarterGui.PackOfferGui` is deleted.
   - Every caller already goes through `PackOffer.offer`, so none of them changed: the TycoonController pads, the GemController Gem Shop, DeliveryController, DecorateController, the EmployeeController crew page and the new confirm.
4. **Icons on Roblox for every pass and product** (universe 10771581195, Open Cloud PATCH `imageFile`; all 24 returned 204). The images are from the Free Icon Pack (1st Outline 256px, unedited) or the game's own `Art/Weather Icons`.
   - **Passes:** Auto Ore Roller → Auto Open; 50% More Coins → Golden Coin; Lucky Ore → Clover; VIP → VIP; Swift Boots → Red Shoe; Starter Pack → Chest; Auto Anvil → Hammer. These match the Shop cards.
   - **Products:**
     - Sunshine, Rainbow, Rain and Snow each use their Weather icon.
     - The six coin packs (800, 1,800, 5,000, 20,000, 100,000 and 300,000) use Golden Coin. The pack has no coin pile.
     - The five gem packs (7, 15, 80, 200 and 500) use Purple Diamond.
     - Epic Ingot uses Silver and Legendary Ingot uses Gold. The pack has no purple ingot.
   - A read-back shows new icon ids, for example Auto Ore Roller 75385401632796 and 80 Gems 111075096855932.
   - The script is `set_product_icons.py` in the session scratchpad. It never prints the key.
5. **Mail tracker on phones** (line 162).
   - **Cause:** the row text used TextScaled together with AutomaticSize X, so each row kept the width from the first, taller layout. Measured in Edit: going from portrait to landscape left a box 207 px wide around 162 px of text, which is the gap in Allen's screenshot.
   - **Fix:** `MailGui.Templates.Track` Bullet and Words (and their Faces) now use fixed 18 pt text with no TextScaled and no size constraint, and size to their text in both directions. `Tracker.List` also sizes to its rows, with 4 px between rows.
   - **Two lines:** `MailController.twoLines` puts a line break before the blade's name, so the row reads "Black Iron" then "Wakizashi". "Katana" alone stays on one line.
   - Measured at 750 × 390: one row ends at x 734, flush with the Mail button's right edge at 734. The result no longer depends on what the screen did before.
6. **The roll button while held** (line 167). `WorldText.Prompt.Button` is now centred at (0.5, 30) and has two new children:
   - `Grow`, a UIScale.
   - `Ring`, a gold 5 px edge just outside the square. It fills from the bottom with a `Progress` gradient: Offset (0, 0.5) is empty and (0, −0.5) is full.

   In `PromptStyle`, while any hold prompt is held:
   - the square grows to 1.5× (Back easing, 0.15 s);
   - the ring fills over the hold time;
   - the square rocks ±3° (0.06 s), unless `Prefs.motion()` is off.

   All of this resets on release, on trigger and on hide. I rendered it in a ScreenGui copy to check.
7. **Auto-Roll dropdown** (line 170).
   - The gear on `AutoRollGui.Bar.Config` is now a chevron, `Config.Arrow`: the "›" glyph turned 90° so it points down, and up while open.
   - `Config.Drop` hangs 8 px under the bar, right-aligned with it, 276 px wide. It's a dark panel styled like the pill (43,28,19, 3 px outline, corner 16) and holds:
     - "Stop at rarity", with the < Rare+ > selector (38 px buttons, the value in its rarity's colour);
     - "Stop at quest ores", with a 48 × 26 knob pill.
   - The text is 18–20 px, unscaled. The panel is Active, so taps on it don't reach the world.
   - It hides nothing. `StarterGui.AutoRollConfig`, the old HidesHud window, is deleted.
   - It closes from the arrow, B, Escape or walking away. Code: `AutoRollController`.
8. **Top bar icons sometimes missing** (line 173).
   - **Cause:** the Dev Panel's Reset progress / Skip tutorial destroyed every PlayerGui screen, TopbarPlus's `Topbar*` ScreenGuis included. TopbarPlus's module stays required, so the fresh scripts made their icons inside destroyed screens. Re-joining fixed it, which matches what Allen saw.
   - **Fix, in `DevPanel` (outside my fence, one line):** it now keeps screens whose names start with "Topbar".
   - **Fix, in `UiFx.topbarIcon`:**
     - It destroys an icon of the same name before making a new one, so there are no duplicates after a reset.
     - It finds `MenuGui.Buttons` even while it's parked in `HudHold`. The old `WaitForChild("Buttons")` waited forever if the HUD was hidden at that moment.
9. **Console error** (line 119, `Buttons is not a valid member of ScreenGui MenuGui`, MenuController:196). MenuController now keeps a reference to the Shop dot from the start, in `local shopDot`, beside `menuButtons`. `updateDot` writes `shopDot.Visible`, so it still works while HudFocus has Buttons parked in HudHold. The other agent's `lessonsDone` / StarterPack condition is unchanged.

## Not done / open

- **Are the developer products on sale?** The Monetization Plan says they stay off sale until built. `PackOffer` only prompts a product that `GetProductInfoAsync` reports as on sale. If they're off sale, a short-of-gems tap just shakes; there is no prompt. Check on the Creator Dashboard.
- **The level-up price can change while the confirm is open.** If the crew member levels up from work meanwhile, the server charges the new level's price. Rare; nothing guards it.
- **Phone and desktop text sizes don't scale.** The tracker rows are 18 px and the Auto-Roll dropdown 18–20 px on every screen, as the bar already was. They're readable on a phone and smallish on a 1080p desktop.
- **Outside my fence:**
  - `UiFx.topbarIcon` and the one-line `DevPanel` fix.
  - `EmployeeController` line 78 (`MenuGui.Buttons.Crew`) runs only at startup, so it's fine.
  - Other scripts that read `MenuGui.Buttons.X` at runtime could hit the same HudHold error. I didn't audit them.
- **Not checked:** the confirm and the dropdown with a gamepad.
- **Not rendered in Play:** I rendered the confirm, the LevelUp button, the tracker, the dropdown and the hold ring as ScreenGui copies in Edit. BillboardGuis don't draw in Edit.

## What to test in Play (phone emulator first)

1. Crew window, crafter's Stats page: the button shows "Lv. N → Lv. N+1" over the gem icon and price. The panel's level says "Lv.", as do the cards.
2. Walk up to a worker and tap the square once, with no hold. The "Level Up" window should open with "<name> to Lv. N?". Press the green button with enough gems and the worker levels up with the pad burst. Press it short of gems and Roblox's Robux prompt should come up with no card first, and the window should stay open. X, B and Escape close it.
3. Gem Shop card, crew page button and an unaffordable coin pad: each should go straight to Roblox's prompt. During the tutorial and the gem step there should be no prompt.
4. Accept a Black Iron Wakizashi letter. The tracker shows "Black Iron" over "Wakizashi", ending flush with the Mail button's right edge. Rotate the emulated phone, or join in portrait and then turn to landscape. Try two or three quests at once.
5. Hold Roll at the ore lever. The square grows round your finger, a gold ring fills from the bottom outside it, and it rocks. Turn on Reduce motion: no rocking. Let go early: it snaps back.
6. Auto-Roll bar (with the pass): tap the down arrow. A small panel drops under the bar, the HUD stays visible, the rarity < > and the quest pill work, and the arrow points up. Tap the arrow again or walk away and it closes.
7. Top bar: Settings and gift icons show on join. Use Dev Panel Reset progress, then Skip tutorial: both icons should still show, once each. Open a station and they hide; close it and they come back.
8. Open a station or window, finish the tutorial or close the gem step while the HUD is hidden. The console should show no "Buttons is not a valid member" error.
9. Check the passes' and products' icons in the Shop's Robux prompts.

---
title: Handoff — UI review fixes
type: handoff
updated: 2026-10-31
tags: [ui, review, fixes, handoff, create-swords]
---

# Handoff — UI review fixes (2026-10-31)

Fixes from [[Design/Reviews 2026-10-31/UI Review — Style and Layout]] (S#) and [[Design/Reviews 2026-10-31/UI Review — Accessibility and Input]] (A#). Studio stayed in Edit and was never put in Play. Scripts were edited only with multi_edit. The session ended early, so part of the list is not done (see below).

## Fixed

**Instances (StarterGui / WorldText)**
- **S1, desktop half-screen windows:** `MenuGui.OddsWindow`, `GemGui.DailyReward`, `GemGui.GemShop` and `MailGui.Window` now have `Pattern` (Z 2) and `Tint` (Z 3) as window children, with `EdgeArt` inside `Tint` and `Content` at Z 5. EdgeArt went inside Tint, not beside it: as a direct window child it made the auto-height window 30 design units too tall (measured).
  - Measured on a Settings-shaped copy: 1080p 465 px for 447 of content (it was 810); phone 209 px, the same as before.
  - The remaining 12 design units come from `Shadow.Image`. This is the same result as the reviewer's copy.
  - The Settings window was not changed: the other agent's rebuild made it a fixed 416 × 440 window with a scrolling body, so S1 no longer applies to it.
- **S2, Gem Shop on a 390 px phone:** `GemGui.Templates.Upgrade` is now 84 tall (was 100), and its `Info` list padding is 4 (was 6). The four cards come to 444 design units, 311 px on a phone. I chose this over a scroll so the guide's spotlit Buy button can never be scrolled out of view.
- **S6/A9, HUD menu labels:** `MenuGui.Buttons` has `UIPadding.PaddingLeft` 0.115. The grid's CellSize X is 0.2496 and its CellPadding X is 0.261, so the buttons stay 44 px. Each `Label` is now 2.05 × the button's width, and each Label and Face has a `UITextSizeConstraint` with MinTextSize 14.
  - Measured: all four labels are 14 px on 844 × 390 and on 667 × 375, and 19 px at 1080p. There is no overlap, and COLLECTION starts at x 11.
  - The 2 × 2 grid now sits about 22 px further right on a phone.
- **S8, Crew title:** `CrewGui.Window.Header.TitleRow` X offset changed from −14 to +14.
- **S11, weather tip:** `WeatherGui.Icon.Tip` width changed from 4 to 3.2 × the icon. It now ends at x ≈ 200, before hotbar slot 1 (x 209). The icon itself was not moved (A17 is Allen's call).
- **S12, pinned order:**
  - `DeliveryGui.PinnedOrder.Row.Label` now has two layers: a new `Face` child (cream), and the label itself is the dark copy. TextLayers drives them.
  - The row moved up (Y scale 0.648 → 0.618), so it now ends above the hotbar's top.
- **S13, guide line:** `GuideGui.Goal` has a Contextual UIStroke, 2 px (16, 20, 16), copied from `ShopHud.Notice`.
- **S16, Mail "Active only":** the ✓ Box was replaced by a knob pill, `Header.ActiveOnly.Switch` (48 × 26, cream knob, Settings' Outline). `ActiveOnly` is now 64 tall with a clear background.
- **S18, green-button words:** white instead of cream on Daily `Claim.Label`, Deliveries `Send` / `Collect` labels, the cart Buy `Price.Label` and `Max`, `Templates.Button.Label`, and Crew `Templates.Card.Price.Row.Coins` / `Gems`.
- **S19, corners and edges:**
  - Corner radius changed from 12 to 10 on: Deliveries `CartButton`, `Cancel`, `AutoFill`, `Send`, `Collect`, the cart `Buy`s, and `Templates.Button` / `Brown` / `Slot`; the book's `Tabs.Metals` / `Swords`; and `OfferBubble.OfferCard.Accept` / `Decline`.
  - The bag `Trash` radius changed from 8 to 10.
  - The offer card's Decline got Accept's thin EdgeArt.
  - `HotbarGui.BagPanel` got the thin EdgeArt, pushed out by its 8 px padding. Its black UIStroke is now hidden (Transparency 1).
- **S20/A10, Deliveries sword card:** `Templates.Sword` chip label and price are 20 pt (were 18), 14 px on a phone. The title is 23 pt (was 21) with TextTruncate AtEnd.
- **S4, ore pill:** `ReplicatedStorage.WorldText.OreLabel.Wants` lost its `Face`. It now has cream text and one Contextual UIStroke, 1.5 px (18, 12, 8).
- **A13, Odds rows:** `OddsWindow…Table.Epic.Name` and `Secret.Name` got Rare's 2.5 px stroke.
- **A8, tap targets (where the look could stay the same):**
  - Every window X (Collection, Daily, Gem Shop, Deliveries, Shop, Odds, Mail, Crew) is now a clear 64 × 64 button (44.8 px on a phone). The red 52 square inside it, `Close.Art` with `Glyph`, looks as before.
  - Mail's and Crew's `TitleRow.Back` ‹ is now 64 × 64, left-aligned. The row padding is −28, so the title stays where it was.
- **S14, selection look:** new `StarterGui.SelectionGui` (disabled) holds `Edge`: a clear frame with a 3 px amber (242, 169, 59) stroke and corner 10. UiFx sets `PlayerGui.SelectionImageObject` to a clone of it.

**Scripts**
- **UiFx:**
  - The selection edge above.
  - `UiFx.open` remembers what a gamepad had selected outside the window, and `UiFx.close` gives the selection back 0.1 s later, once HudFocus has un-parked the HUD (A12, focus restored).
  - Added the `GuiService` local, plus the `openers` and `onScreen` helpers.
- **MailController:**
  - The popup is held, with its countdown paused, while the bag is open. This happens in `showPopup`, and the bag's Visible signal brings it back (S5).
  - The Active-only switch is painted in `render` (S16).
  - `GamepadEnabled` changed to `UiFx.onGamepad()`.
  - New `MailPad` action: D-pad down opens the mail when nothing is selected and the Mail button is on screen (A11).
- **GemController:** the GemShop D-pad left action passes whenever anything is selected (A6, this also fixes Daily turning into the Gem Shop). Q and Backspace now close it (A16). `onGamepad`.
- **CollectionController:** D-pad right passes whenever anything is selected (A6). Q and Backspace close (A16). `onGamepad`. Focus stays on the grid, because the cards aren't buttons and the pad scrolls the book.
- **MenuController:** Q and Backspace close Shop, Settings and Odds (A16). `onGamepad`.
- **DeliveryController:** Q and Backspace close (A16). `onGamepad`.
- **PromptStyle (A7):** on a gamepad, the prompt square shows `GetImageForKeyCode(prompt.GamepadKeyCode)` in its `Tap` image. It falls back to the old letter if there is no image.

## Checks
- Compile check (each script wrapped in a function): MailController, GemController, MenuController, CollectionController, DeliveryController, PromptStyle and UiFx: 7/7 ok. New locals are declared above their first use: `bag`, `C.on` / `C.off`, `openers`, `onScreen`, `GuiService`, `pad` / `padImage`.
- Measured in CoreGui test frames:
  - S1 heights, before and after, on all five windows.
  - Menu labels at 844 × 390, 667 × 375 and 1920 × 1080 (all four the same size, at least 14 px on a phone).
- Rendered: only the HUD at 844 × 390, 667 × 375 and 1080p (one third), before and after the label change.
- **Not rendered:** the changed windows (Odds, Daily, Gem Shop, Mail, Deliveries, Crew, the X and Back buttons, the Active-only pill, the bag panel edge). The session ended first.
- Previews deleted (`UIFX_P`, `ServerStorage.UIFX_RenderKit`). The camera is Fixed. `ShowDevelopmentGui` was left on because another agent's `__HotbarPreview` still exists.

## Not fixed
- **A11, select the spotlit button on a pad:** this belongs in `Guide`, which is outside my fence (line style only). The suggested patch goes at the end of Guide's loop, after `spotTarget = …` (about line 938): `if spotTarget and spotTarget:IsA("GuiButton") and UiFx.onGamepad() and GuiService.SelectedObject ~= spotTarget then GuiService.SelectedObject = spotTarget end`.
- **S10, title sizes:** not done. The book's title is 54 at 0.8. Mail and Deliveries are 44, inside the window by Allen's call. The picker's title is in another agent's fence.
- **S15, one Back look:** Crew's `Stats.Top.Back` and `Station.Buttons.Back` word buttons are wired in EmployeeController, which is not in my fence. The bare ‹ in `TitleRow` already exists.
- **S19, chips and Pin:** Deliveries' `Town` / `Need` chips and `Pin` keep their plain 2.5 px stroke. They lay out with a UIListLayout, so an EdgeArt child would be placed in the list.
- **S20, strip buttons:** they are still 40 design tall. The strip is 108 tall with the buttons at y 58, so 52 would run past it. Making them taller needs a strip re-layout.
- **A8, still to do:**
  - Settings switches: Settings' content is another agent's.
  - Shop `Buy`: the script colours the button itself, so it can't hide its art inside a bigger hit box without a MenuController change.
  - Deliveries buttons (see S20).
  - Crew buttons: EmployeeController / CrewGui content.
  - Tracker rows: `MailGui.Tracker` is fenced.
  - Rack/holder markers (`ShopHud.Templates.SlotMarker`).
  - Settings' X: Settings is another agent's.
- **Other agents' work seen:**
  - The new `MenuGui.VolumeWindow` has the S1 layout (auto height with Pattern and Tint in Fill), so it will be half-screen tall on desktop. Its owner should apply the same restack.
  - UiFx gained `Prefs` (reduced motion) from another agent while I worked. My edits sit around it.
- **AutoRollConfig, PackOfferGui, the picker, and the station HUDs:** fenced, not touched.

## Open questions for Allen
- The menu grid now sits about 22 px further right, so COLLECTION fits at 14 px. Alternatively, shorter words would let it stay at the edge.
- Weather icon (A17): it stays bottom-left. Only its tip got narrower.

## What to test in Play
1. **Desktop:** open Odds, Daily, Upgrades and Mail. Each window should end just under its rows, with no brown band. Check that the hand-drawn edge still shows on all four.
2. **Phone emulator (844 × 390):**
   - Open Upgrades: all four cards and the bottom border should be on screen.
   - The HUD labels COLLECTION, UPGRADES, SHOP and CREW should all be the same size.
   - Pin an order with a long name and check it stays above the hotbar.
   - Tap the weather icon: its tip should end before slot 1.
3. **Mail:**
   - Toggle "Active only" with the knob pill.
   - Open a letter and press the bare ‹. It should be easier to hit, and the title should not move.
   - Open the bag while a new letter's popup is up. The popup should hide and come back when the bag shuts, with its countdown paused meanwhile.
4. **Every window's X:** easier to hit on a phone, and it looks the same as before.
5. **Gamepad:**
   - Every selected button should show the amber edge, with no Roblox box.
   - Open the Upgrades with D-pad left and press D-pad left again inside: it should move, not close. Do the same in the book (D-pad right) and in Daily.
   - D-pad down opens the mail.
   - Select a HUD button in UI mode, open its window, then close it with B: the focus should come back to that HUD button.
   - Prompts show the pad's own button picture (try a PlayStation pad).
6. **Keyboard:** Q and Backspace close Upgrades, Daily, the book, Deliveries, Shop, Settings and Odds.
7. **Ore roll for a letter's metal:** the "<name> wants this!" pill should show cream words with a thin dark outline and no inner box.
8. **Deliveries packing page on a phone:** the sword cards' chip and price read 14 px, and a long title ends with "…".

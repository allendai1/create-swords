---
title: Handoff — Phone UI review
type: handoff
updated: 2026-10-31
tags: [ui, review, phone, accessibility, create-swords]
---

# Handoff — Phone UI review (2026-10-31)

Everything below was done in Edit. Play was never started. Each panel was cloned into a preview screen sized to the target resolution, with the runtime scales applied: `UiFx.fit` with its 0.85 shrink, the Hotbar's barFit and slot count, and the Deliveries body height. Each one was captured and then measured with AbsolutePosition and AbsoluteSize. Billboards (the prompt ring and the slot markers) were drawn as ScreenGui copies.

## What I rendered and found

The checks were: text under 12 px on a phone, tap targets under 36 px, and anything off screen.

**844 × 390 (windows at 0.7, hotbar at 0.75 with 5 slots)**

| Panel | Size on screen | Smallest text | Tap targets under 36 px |
|---|---|---|---|
| Odds | 361 × 265 | 16.1 | none |
| Daily | 333 × 280 | 16.8 | none |
| Gem Shop | 445 × 311 | 16.1 | none |
| Mail list | 400 × 318 | 14.0 | none |
| Mail letter | 400 × 291 | 14.0 | Decline / Accept / Send are 73 × 35 |
| Deliveries | 609 × 316 | 14.0 | strip AutoFill, Send, Collect and Pin are 28 tall |
| Crew roster | 568 × 301 | 14.0 | Card.Price 148 × 28 |
| Crew Stats | 568 × 301 | 14.0 | Top tabs 91 × 31 |
| Crew Staff | 568 × 301 | 14.0 | Cashier slider 31 tall, Etch.Pick 91 × 31 |
| Crew Confirm | 322 × 150 | 18.2 | none (Buy 140 × 39, X 45) |
| Settings | 291 × 308 | 17.5 | Sound gear 32 × 32. The pills are 50 × 27, but the whole 252 × 48 row toggles, so they're fine. |
| Volume | 291 × 209 | 17.5 | none |

- **HUD:**
  - The Auto-Roll bar is at x 284–560, y 66–112.
  - Its dropdown is at y 120–246, with 18 px text. Its `Quest.Switch` is a 48 × 26 tap target.
  - The tracker rows are 18 px text. Rows were 36 tall with two lines and 18–31 tall with one line, and the Fold was 30 × 30.
  - The hold ring at 1.5× is 90 px with a 114 px ring. The billboard doesn't clip, so all of it shows.
- **Overlaps:** Confirm sits at x 261–583 and clears the menu grid and the tracker. The dropdown and Confirm would overlap if both were open at once (unlikely: walking away closes the dropdown).

**667 × 375 (windows at 0.7, hotbar at 0.70 with 3 slots)**
- Window sizes are the same as on 844. Mail and Shop end 1 px past the bottom edge.
- **Found:** "COLLECTION" was cut to "COLLECTIO". Its label was 13.8 px tall, under the 14 px minimum text size.
- The Hotbar's slot titles are 11 px and its key caps 9 px. This is accessibility review finding #3, in the Hotbar's fence.
- Confirm's X ends about 4 px from the tracker's Fold.

**1920 × 1080 (windows at 1.5)**
- None of the windows show the half-screen band:
  - Odds 774 × 567, Daily 714 × 600, Gem Shop 954 × 666
  - Mail 858 × 681, Deliveries 1302 × 810, Crew 1218 × 645
  - Confirm 690 × 321, Settings 624 × 660, Volume 624 × 447
- Text is at least 30 px.

**VolumeWindow before and after the restack:** 1080p 624 × 447 before and after, phone 291 × 209 before and after. Volume is a fixed 416 × 298 window, not auto-height, so it never had the half-screen problem. I applied the restack so it's built the same way as the other windows.

## What I fixed

Copies of everything from before these changes are in `ServerStorage.Legacy.PhoneReview_before_2026-10-31`.

- **`MenuGui.VolumeWindow`:** `Pattern` and `Tint` are now window children at Z 2 and Z 3, with `EdgeArt` inside `Tint`, and `Content` is at Z 5. This is the same as OddsWindow.
- **Settings X and Volume X:** both are now a copy of the Odds X: a clear 64 × 64 button (45 px on a phone) with the red 52 `Art` and `Glyph` inside. The centre didn't move.
- **`SettingsWindow…Sound.Gear`:** a clear 64 × 64 hit box (45 px) at {1,−75}, so the centre didn't move, with the 46 `Art` inside it. It leaves a 3 px gap to the pill.
- **Shop `Buy`, all 18 (StarterPack, Grid, Currency):** each is now a clear hit box 64 tall, with `Art` (the old colour, corner, gradient, Glow and EdgeArt) at the old height. `Price` stays on the button. Bottom-anchored buttons moved down by half the growth, so their centres didn't move.
  - On a phone: 111 × 45 and 76 × 45, up from 29.
  - The hit boxes stay inside their cards (Info ends at y 336, the hit box starts at y 335).
  - **`MenuController`:** the 3 lines that wrote `card.Buy.BackgroundColor3` now write `card.Buy.Art.BackgroundColor3` (showCard, the Odds copy and the product price).
- **Crew:**
  - `Templates.Card.Price`: 212 × 56 hit box with `Art` 40 inside it, 39 px on a phone. It fills the gap between Forge and the card's bottom.
  - `Stats.Top.Back`, `Swords` and `Station`: 54 tall, growing downward only. The `Art` TextLabel carries the text, the strokes and the EdgeArt. 38 px on a phone.
  - `Staff.Etch.Pick`: 54 tall, centred, 38 px.
  - `Staff.Setting.Slider`: 60 tall at y 40. The track and knob are centred, so they didn't move. 42 px.
  - EmployeeController needed no change: it never colours these buttons.
- **Rack and holder markers:**
  - `ShopHud.Templates.SlotMarker.Plus` is now a clear 44 × 44 hit box. The 33 px circle is the `Face` TextLabel, with the Ring, stroke and Bag inside it.
  - **`SlotMarker`:** `face` now holds the "+" and the colour; `ring` and `bag` are read from Face.
- **Mail tracker:**
  - `MailGui.Templates.Track` has `UIPadding` of 4 top and 4 bottom.
  - The gap between rows in `Tracker.List` is 8 (it was 4).
  - The Fold is 24% bigger and its arrow didn't move.
  - Rows are now 44 tall with two lines and 26 with one line. The Fold is 37 px.
  - Three two-line rows on a 667 × 375 phone end at y 284, above the jump button at 285.
- **HUD labels:** each `MenuGui.Buttons.*.Label` has a `UISizeConstraint` with MinSize 88 × 14.
  - All four labels now fit at 14 px on 667 × 375 and 640 × 360.
  - They are 14 px on 844 and 19 px at 1080p, the same as before.

## Checks
- **Compile check** (wrapped in a function): MenuController and SlotMarker both compile.
- **Load check:** SlotMarker's fresh clone can't load in Edit. It waits on the LocalPlayer and PlayerGui, as any client module does there.
- **New locals:** `face`, declared above its first use.
- **Clean-up:**
  - The previews and the render kit are deleted; nothing named `__PR` is left.
  - `ShowDevelopmentGui` is back to false, as I found it.
  - The camera is Fixed.

## What's left for another fence or for Allen
- **Auto-Roll dropdown, `Quest.Switch` (48 × 26):** AutoRollController paints it. The fix is to make the Quest row the toggle, the way Settings rows work.
- **Deliveries strip buttons (28 px):** this needs a strip re-layout (S20) or `Art` hit boxes, and DeliveryController colours them.
- **Mail letter Decline / Accept / Send (73 × 35):** 1 px short of 36. The `Buttons` row has no room to grow.
- **Hotbar text at 667:** titles are 11 px and key caps 9 px (accessibility finding #3).
- **Crew "Lv. 4 → Lv. 5":** the → glyph draws as a small circled arrow, about 8 px on a phone. `EmployeeController.showLevelUp` could use "›" or "to" instead.
- **Crew Confirm doesn't hide the HUD:** the HUD stays bright and tappable above its dim, because CrewGui's DisplayOrder is 4 and the HUD's is 6–7. Allen's call: add `HidesHud` to `CrewGui.Confirm`?
- **Gamepad:** the amber selection edge now outlines the bigger hit boxes (Buy, the crew tabs and price, the gear, the markers), a little outside the art.
- **Marker spacing:** Sword Rack slots are 1.18 studs apart, about 32–37 px on a phone. Neighbouring 44 px hit boxes overlap the outer 5–10 px of the next circle. A tap on a circle's centre always hits the right marker.

## What to test in Play (phone emulator)
1. Shop: tap just above and below each green Buy button. It should prompt, and the look and price should be unchanged.
2. Settings: the X, and the gear's edge. Tapping near the gear should open Volume and leave Sound on.
3. Crew: the card price, the Back, Station and Swords tabs, Patterns, and the Cashier slider.
4. Racks: tap the edge of a + and of a bag marker.
5. Tracker: three accepted letters on a 667 × 375 phone, clear of the jump button.

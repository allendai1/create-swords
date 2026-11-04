---
title: UI Review — Style and Layout
type: review
updated: 2026-10-31
tags: [review, ui, style, layout, phone, desktop, billboards, create-swords]
---

# UI Review — Style and Layout (2026-10-31)

Scope: every ScreenGui in `StarterGui` (the Dev Panel excepted) and the billboards in `ReplicatedStorage.WorldText`, checked against Allen's style system ([[Art/UI Design]], the 2026-10-28 rulings in [[Design/Decisions Log]]) for fonts, corners, edges, outlines, colours, button styles, spacing, icons, text sizes, wording, overlaps with Roblox's top bar, thumbstick and jump button, panels open together, z-order and cut-off text. Reference phone 844 × 390 landscape; desktop 1920 × 1080. Read-only: no GUI, script or property was changed and Studio was never put in Play.

Sibling note: [[Design/Reviews 2026-10-31/UI Review — Accessibility and Input]] covers text size, touch targets, gamepad and contrast in depth. Where a finding here overlaps one there, it says so; this note keeps the style and layout side.

**How it was done.**
- Measured: each GUI was cloned into a CoreGui ScreenGui inside 844 × 390, 1920 × 1080 and 667 × 375 frames, its `Fit` UIScale set as its controller sets it (`UiFx.fit` numbers below), lists filled from its `Templates` with the longest real strings (Leviathan Cleaver, Rainbow Alloy, "Etched Rainbow Alloy Leviathan Cleaver · 90%+", "Furnace 3 Heating III", Lord Hideo), then `AbsolutePosition`, `AbsoluteSize` and `TextBounds` read. A GUI with `IgnoreGuiInset` off was placed 58 px down (Roblox's top bar). No notch insets.
- Rendered: 13 captures, each with the phone at 1:1 (or 0.73–0.76) and the 1080p desktop at one third, using temporary `UIR_P_*` copies in StarterGui with `ShowDevelopmentGui` on; an overlay marked the 58 px top bar, Roblox's top-left buttons (assumed x 12–112), the thumbstick and the jump button. Billboards were drawn as ScreenGui frames at their pixel size, with `TextLayers`' runtime edge thickness applied (7.5% of the text height, 1–3 px). All copies were deleted after each capture; `ShowDevelopmentGui` is off and the camera is Fixed.
- Window scales used: menus, Gem Shop, Daily, Mail, Auto-Roll 650 × 570 → 0.70 phone / 1.5 desktop; Crew 860 × 560 → 0.70 / 1.5; Deliveries 900 × 556 → 0.70 / 1.5; book 570 × 488 → 0.80 / 1.5; pack offer 0.75 / 1.5; mail popup 0.78 / 1.1; phone picker (`CompactWindow`, 600 × 320) ≈ 1.2; desktop picker 1.42; polishing panel 0.93 / 1.5; hotbar 0.75 / 1.2, bag 0.70 / 1.2; anvil HUD `min(1, height / 560)` = 0.70 / 1.0.

## Findings, most valuable first

### 1. On desktop and tablets, six windows are never shorter than half the screen: a band of empty brown under their contents

- **Where:** `MenuGui.SettingsWindow`, `MenuGui.OddsWindow`, `AutoRollConfig.Window`, `GemGui.DailyReward`, `GemGui.GemShop`, `MailGui.Window` (the windows built on the Settings layout: `AutomaticSize` Y, with `Fill.Pattern` and `Fill.Tint` sized {1,0,1,0} inside `Fill`).
- **What's wrong:** an auto-height window whose `Fill` holds scale-sized children comes out at least half the screen tall in its own units, whatever its content. On a 390 px phone half is 195, under every window's content, so phones look right; on desktop and tablets the window grows past its rows.
- **Evidence** (window height vs content, design units; px at the window's scale):

  | Window | Content | At 1080p | Empty band at 1080p (×1.5) | At 768 tall (×1.35) |
  |---|---|---|---|---|
  | Auto-Roll | 264 | 540 | 414 px | 162 px |
  | Settings | 298 | 540 | 363 px | 116 px |
  | Lucky Ore odds | 378 | 540 | 243 px | 8 px |
  | Daily Reward | 400 | 540 | 210 px | 0 |
  | Mail | 454 | 540 | 129 px | 0 |
  | Upgrades (Gem Shop) | 508 | 540 | 48 px | 0 |

  Reproduced in a real ScreenGui at Studio's 1582 × 753 viewport (Settings 376.5 = 753 / 2, content 298). Hiding `Fill.Pattern` and `Fill.Tint` brings it back to the content; `PickerGui.Window`, which has Pattern and Tint as direct children, is not affected (3 cards at 1080p: 529 px, body 503). Renders: the desktop Settings, Daily Reward, Odds and Auto-Roll windows each show the band (Auto-Roll's window is more than twice its two rows).
- **Fix (small):** lay these six out like `PickerGui.Window`: move `Pattern`, `Tint` and `EdgeArt` out of `Fill` to the window, ZIndex Shadow 0, Fill 1, Pattern 2, Tint 3, EdgeArt 4, Content 5. Checked on a copy of Settings: 1080p 465 px tall (content 447) instead of 810; phone unchanged (209 px).
- **Ruling:** 2026-10-28 window style (no change to the look).

### 2. The Upgrades window (Gem Shop) runs off a 390 px phone

- **Where:** `GemGui.GemShop` with its four upgrade cards (`Templates.Upgrade`, 100 tall, 14 apart).
- **What's wrong:** 4 × 100 + 3 × 14 + padding 48 + list gap 18 = 508 design, 356 px at 0.7. Centred 29 px low, it spans y 46–402 on 844 × 390: the bottom 12 px (the last card's edge and the window's bottom border) are off the screen and the title sits at y 26–67, inside Roblox's 58 px top bar. On 667 × 375 it is 19 px off the bottom. The body has no scroll. It was fine with three upgrades; Quicker Mail (2026-10-29) made it four.
- **Evidence:** measured window [199, 46, 445 × 356] on 844 × 390; render R3 shows the cut bottom edge.
- **Fix (small):** put `Content.Body` in a ScrollingFrame capped at about 300 design (what Mail does), or make the cards 84 tall (444 → 311 px), or two columns.
- **Ruling:** [[Sessions/2026-10-30#UI review of the evening's work]] item 1 (windows clear the top bar).

### 3. The phone picker reaches into Roblox's top bar; on a 667 px phone its X is off the screen

- **Where:** `PickerGui.CompactWindow` (every station's picker on a phone), placed by `ItemPicker.render` at (0.5, 0, 0.5, 29) with `UiFx.fit(COMPACT.Fit, 600, 320)`.
- **What's wrong:** on a phone this window scales up (≈ 1.2, for "Bigger cards always"), so with three cards it is 706 × 322 px and its title, on the top border, is the largest on the phone.
  - 844 × 390: window top y 52; the title "Choose a shape" spans y 26–78 from x 72, so its first letters sit where Roblox draws the chat button.
  - 667 × 375: the window is 644 px wide from x 12; the title starts at x 14, under Roblox's menu button, and the X is 58 px wide at x 620–678, 11 px past the right edge.
  - The window's bottom-right corner also sits under the jump button (x 749–773, y 300–374 on 844 × 390); the third card ends at x 747.
- **Evidence:** measured, and render R7 (the title under the top-left pill of the overlay).
- **Fix (small):** cap the compact window's scale so its top stays at least 58 + half the title below the screen top (in `render`, after sizing: `s = math.min(s, (view.Y - 58 - 26) / height)`), and cap its width at the screen width minus 2 × 47 so the X stays on; or keep 3 columns only from 700 px wide.
- **Ruling:** 2026-10-26 "Bigger cards always" (keep big cards; this only stops the top row and the X going under Roblox's buttons).

### 4. The rolled ore's "Lord Hideo wants this!" pill draws a box inside itself at runtime

- **Where:** `ReplicatedStorage.WorldText.OreLabel.Wants` and `Wants.Face`.
- **What's wrong:** both labels' UIStrokes are `ApplyStrokeMode` **Border** (0.2 px in Studio). `TextLayers` sets every Face pair's strokes to 7.5% of the text height at runtime, 1.4 px here, so in Play the pill gets a dark rounded border and the Face draws a dark square around the words inside it; the cream words themselves have no outline. The 2026-10-31 session made the Face visible, so this is new.
- **Evidence:** render R11 with the runtime thickness: the pill shows its border and an inner rectangle round "Lord Hideo wants this!" (193 × 19 px text in the 260 × 26 pill).
- **Fix (small):** dark pills keep one layer: delete `Wants.Face`, give `Wants` the cream colour (251, 235, 213) and one UIStroke in Contextual mode (about 1.5 px, near-black). `TextLayers` then leaves it alone.
- **Ruling:** 2026-10-30 "Overhead and HUD text is two layers everywhere … dark pills and speech bubbles keep one layer"; 2026-10-29 status pills "no border".

### 5. A letter's popup covers the open bag's right-hand column

- **Where:** `MailGui.Popup` (DisplayOrder 6) over `HotbarGui.BagPanel` (2).
- **What's wrong:** the tracker steps aside while the bag is open (2026-10-30 fix), the popup doesn't. It covers the last column's cards and their trash buttons.
- **Evidence:** overlap 83 × 49 px on 844 × 390 (popup [581, 170, 255 × 50], bag [179, 128, 486 × 163]), 66 × 47 on 667 × 375, 35 × 54 at 1080p, 211 × 70 at 1334 × 750. Render R2.
- **Fix (small):** in `MailController`, hold the popup (or its countdown) while `bag.Visible`, as `renderTracker` already does for the tracker.

### 6. The four HUD menu labels come out at four sizes; COLLECTION is 9 px on a phone

- **Where:** `MenuGui.Buttons.<Book|Upgrades|Shop|Crew>.Label` (TextScaled, no size constraint, box 1.3 × the button's width).
- **What's wrong:** each label scales to fit its own word, so the 2 × 2 grid mixes sizes: COLLECTION 9 px, UPGRADES 10, SHOP 14, CREW 14 on 844 × 390 (12 / 14 / 19 / 19 at 1080p; 8 / 10 / 13 / 13 on 667 × 375). Also in the sibling review (#9) for size; here the point is that they don't match.
- **Fix (small):** give all four the same `UITextSizeConstraint` max (one size for the set) and widen the label boxes to about 1.7 × the button so COLLECTION reaches 12 px; the grid's 0.09 padding leaves the room. Shorter words would be Allen's call.
- **Ruling:** 2026-10-30 "HUD menu is 2 × 2 … HUD labels in capitals".

### 7. Finish is the only green action button without the bevel and glow

- **Where:** `AnvilHud.Bottom.Finish` (flat lime 115, 220, 35; no UIGradient, no Glow).
- **What's wrong:** every other green action button (Shop and Gem Shop Buy, Send, Accept, Claim, Save, the pack offer, the offer card's Accept) has the bevel gradient and the radial glow. Side by side in render R10 Finish reads flat next to Polishing's Save.
- **Fix (small):** copy `PolishHud.Panel.Save`'s UIGradient and Glow into Finish (Words is already a separate label).
- **Ruling:** 2026-10-28 "One button style … Every green action button is the Shop's lime bevel with a glow and hand-drawn edge".

### 8. The Crew window's titles stick out past its left border

- **Where:** `CrewGui.Window.Header.TitleRow` at x −14 inside a window whose own UIPadding (28) insets its Fill.
- **What's wrong:** on every other window the title starts 14 design px inside the left border; Crew's starts 14 px outside it ("Crew", "Sword Crafter", "Where should Taise work?"): −9.8 px on the phone, −21 px at 1080p.
- **Evidence:** measured title left − Fill left: −9.8 px (Crew) vs +9.8 (Shop, Settings, Upgrades, Daily, Auto-Roll, Odds). Renders R5 and R13.
- **Fix (trivial):** `TitleRow.Position` X offset −14 → +14.
- **Ruling:** [[Design/Decisions Log]] 2026-10-28 "Every window's title on its border".

### 9. Station HUDs scale three different ways

- **Where:** `PolishHud.Panel.Fit` (`UiFx.fit` 560 × 420: 0.93 phone, 1.5 desktop), `AnvilHud.UIScale` (`min(1, height / 560)`: 0.70 phone with no 0.7 floor, 1.0 desktop), `EtchHud` and `HiltSeatGui` (no scale: 1.0 everywhere).
- **What's wrong:** at 1080p Polishing's buttons are 195 × 72 px while the anvil's Cancel / Finish are 140 / 180 × 52 and the etch X is 52 px (window Xs are 78). On a phone the anvil HUD is the smallest: its hint is 11 px ("Click the anvil"), Polishing's status and hint 13 px. The anvil hint also says "Click" on touch screens, and "Strike inside the circle." is the only line with a full stop. Text sizes overlap the sibling review (#10).
- **Fix (small):** one rule for station HUDs (`UiFx.fit` with the 0.7 floor and a 1.5 cap, as Polishing), hint and status text at 20 pt or more, and "Tap the anvil" on touch.
- **Ruling:** 2026-10-29 "Window text is at least 23 pt … chips 20"; [[Art/UI Design]] Gotham Heavy + outline for station text.

### 10. Window titles are five different sizes on a phone

- **Where:** title text on each window.
- **What's wrong:** on 844 × 390: phone picker 49 px (40 pt × 1.2), book count 43 px (54 × 0.8), menus and Crew 38 px (54 × 0.7), Mail and Deliveries 31 px (44 × 0.7, inside the window by Allen's 2026-10-30 call). The phone picker's title also starts 2 design px from its left edge (others 14) and its X is 63 px (others 36).
- **Fix (small):** follows from #3: once the compact window's scale is capped, set its title to 54 pt × its scale ≈ 38 px and `Title` X offset to +14 like the menus.

### 11. The weather tip runs over the first hotbar slot; the icon sits on the thumbstick

- **Where:** `WeatherGui.Icon` (bottom-left, 43 px at x 12–55, y 335–378) and its `Tip` (172 × 51 to its right).
- **What's wrong:** on 844 × 390 the tip's text spans x 63–225 and the bar's first slot starts at x 209 (WeatherGui draws above HotbarGui), so "Rainbow 4:59" overlaps slot 1 for the 4 s after a tap (667 × 375: x 61–212 vs 202). The icon itself is in the thumbstick's zone (sibling review #17).
- **Fix (small):** move the icon up the left lane (above the thumbstick, under the pinned order at about y 0.75 of the lane) and open the tip above the icon rather than beside it.
- **Ruling:** 2026-10-28 "an icon on the bottom left like this" (Create Pottery's) — the move keeps it bottom-left, just above the thumb.

### 12. The pinned order is one-layer HUD text and reaches the hotbar

- **Where:** `DeliveryGui.PinnedOrder.Row.Label` (TextScaled Bold, one UIStroke, no Face).
- **What's wrong:** the coin and gem counts, menu labels and the mail tracker are two-layer (Face over a black copy); the pinned order isn't. With a long order ("3× Leviathan Cleaver 0/3", 225 × 20 px) its right half sits 0–2 px above slots 1–2 of the bar (label bottom y 305, bar top 303; 1 px on 667 × 375). The weather tip (#11) is one-layer too.
- **Fix (small):** add a `Face` child (copy of the label, white, its own stroke) as the counts have; cap the label's width at the lane's width so long orders shrink before reaching the bar.
- **Ruling:** 2026-10-30 "Overhead and HUD text is two layers everywhere".

### 13. The tutorial's guide line still uses the old faint text stroke

- **Where:** `GuideGui.Goal` (Heavy 22, `TextStrokeTransparency` 0.55, no UIStroke).
- **What's wrong:** the line players read most in their first session is the only message bar without a UIStroke outline; the notice (`ShopHud.Notice`, 2 px), the picker toast (2 px) and the cheer banner (3.5 px, fixed 2026-10-30) have one.
- **Fix (trivial):** add a Contextual UIStroke, 2 px, (16, 20, 16), as `ShopHud.Notice` has.
- **Ruling:** 2026-10-28 "light menu text has a black outline".

### 14. Gamepad selection looks different from window to window

- **Where:** no GuiObject sets `SelectionImageObject`, so Roblox draws its default selection box on every selected button. Five controllers add Allen's amber edge on `SelectionGained` (ItemPicker, Mail, Gem, Deliveries, Menu); Crew, the book, the pack offer and Auto-Roll don't.
- **What's wrong:** in five windows the selected button shows Roblox's box and the amber edge together; in four only Roblox's box. Focus behaviour is in the sibling review (#12).
- **Fix (small):** set `PlayerGui.SelectionImageObject` to an empty transparent frame once, and give the amber edge to every button through one `UiFx` helper (`UiFx.press` could do it).
- **Ruling:** [[Art/UI Design]] 2026-10-24 "a gamepad's selection still shows an amber edge".

### 15. "Back" comes in three styles

- **Where:** a bare ‹ left of the title (Mail letter view, Crew staff pages: `TitleRow.Back`); a dark 52 px ‹ square with the thin edge (pickers: `Body.Header.Back`); and word buttons — `CrewGui.Window.Stats.Top.Back` (dark green 38, 56, 32 with a visible 4 px green UIStroke) and `Station.Buttons.Back` (brown).
- **What's wrong:** four looks for one action; the green-bordered one is the only bordered button in the menus.
- **Fix (small):** the bare ‹ in the title row everywhere (the 2026-10-30 choice for Mail and staff pages); drop the Stats and Station word buttons.
- **Ruling:** [[Sessions/2026-10-30#UI review of the evening's work]] item 3.

### 16. Mail's "Active only" is a checkbox

- **Where:** `MailGui.Window.Content.Header.ActiveOnly` (a 22 px Box with a ✓ text glyph, a UIStroke round the box, on a black 15%-opaque button).
- **What's wrong:** every other on/off is the knob pill (Settings, Auto-Roll, Stop at quest ores, the Auto Anvil switch); it's also 25 px tall on a phone.
- **Fix (small):** replace Box with a copy of `SettingsWindow.Content.Body.Music.Switch` scaled to 48 × 26, keep the words.
- **Ruling:** memory checklist "On/off is a knob pill toggle"; 2026-10-29 "Pill toggles get a black outline".

### 17. "Lv." and "Lvl." side by side

- **Where:** crew cards (`Templates.Card.Level.Lvl` "Lvl. 1"), the Stats and Staff panels ("Lvl. 3"), their LevelUp buttons ("Lv. 2"), NPC tags (`WorldText.Tag.Level` "Lv. 1").
- **What's wrong:** the crafter's panel shows "Lvl. 3" next to its "Lv. 4" level-up button (render R13).
- **Fix (trivial):** "Lv." everywhere (the shorter one, already on the NPC tags and buttons).

### 18. Green buttons' words are white on some, cream on others

- **Where:** cream (251, 235, 213): `GemGui.DailyReward…Claim.Label`, `DeliveryGui…Strip.Send.Label` and `Collect.Label`, `CrewGui.Templates.Card.Price.Row.Coins`. White: every other green button.
- **Fix (trivial):** white (255, 255, 255) on all; their outlines are already there.
- **Ruling:** 2026-10-28 green action buttons "white words with black outline".

### 19. Corner radii and plain borders that differ from the system

- **Where / what:**
  - Buttons at 12 (the cards' radius) instead of 10: every Deliveries button (`CartButton`, `Cancel`, `AutoFill`, `Send`, `Collect`, the cart `Buy`s, `Templates.Button/Brown/Slot`), the book's `Tabs.Metals/Swords`, the offer card's Accept and Decline. The bag's `Trash` is 8.
  - Plain UIStroke borders where the hand-drawn thin edge is the rule: `HotbarGui.BagPanel` (black 2 px, and a charcoal panel unlike every other panel), `BagPanel.Trash` (black 2 px), Deliveries' `Town` and `Need` chips and `Pin` (2.5 px), the Stats Back (#15). The offer bubble's Decline has no edge art while its Accept has.
- **Fix (small):** radius 10 on those buttons; swap the borders for the thin `EdgeArt` (`rbxassetid://122361462361934`, centred, as on the Bag button).
- **Ruling:** 2026-10-28 "buttons 10 / 4, chips 8", "The hand-drawn edge on every menu".

### 20. Delivery sword cards' chip and price are 12.6 px on a phone

- **Where:** `DeliveryGui.Templates.Sword` (`Chip.Label` and `Price.Amount` 18 pt, `Title` 21 pt).
- **What's wrong:** under the 20 pt chip floor (12.6 px at 0.7) and the 23 pt window floor; "Rainbow Alloy Leviathan Cleaver" doesn't fit the card's two lines. Same window: Send and Auto-fill are 28 px tall on a phone. Overlaps the sibling review (#8, #10).
- **Fix (small):** chip and price 20 pt, title 23 pt with `TextTruncate`, strip buttons 52 tall.
- **Ruling:** 2026-10-29 "Window text is at least 23 pt … chips 20".

### Further findings (lower value)

21. **Tick and arrow glyphs mix with icons.** Ticks are a ✓ text glyph on Daily (`Templates.Day.Done`), crew cards (`Check`), the picker toast and Mail's checkbox, but the pack's Checkmark icon on the Deliveries steps. Arrows: "<" ">" on Auto-Roll's selector, "‹" "›" elsewhere, "→" in Odds. Fix (small): the pack Checkmark (`rbxassetid://98899943650975`) for every tick; "‹ ›" for the selector.
22. **Hotbar slot text 7–11 px on a phone** (sibling #3): title 7 px, and "Leviathan Cleaver" still doesn't fit at its 7 pt minimum (shows "Leviathan"); metal 8 px; key number 9 px; count 11 px. Layout angle: the key numbers mean nothing on touch and take the top row; hiding them on touch gives the title room. Medium.
23. **Small tap targets at 0.7** (sibling #8): every window X 36 px, Send / Accept / Decline / Buy 35–38 px, the bag card trash 28 px, its − + 29 × 28, "Active only" 25 px, the menu buttons 44 × 40, the Auto Anvil switch 81 × 36.
24. **Odds window: Epic and Secret names have no outline** (sibling #13), while Common, Uncommon, Rare and Legendary do. Trivial.
25. **The book's names scale card by card:** on a phone "Rainbow Alloy" is 13 px and "Iron" 20 px in the same grid (`CollectionGui.Templates.Entry.Label`, TextScaled with min 1). Fix: one max size for the grid (about 15 pt at 0.8).
26. **Shop holders keep the old prompt look:** `ShopHud.Templates.SlotMarker` shows a cream "For sale" pill with a copper border (15 px dark text) and an 18 px black "E" chip (12 px), while every other prompt is the 60 px hand-drawn square (2026-10-30 "Square everywhere") and status pills are dark with white text and no border. Small; Allen's call whether the holder markers count as prompts.
27. **Status pills are three sizes:** furnace `ForgeSlot` 96 × 34, text 20, fully round; `FullSign` 150 × 44, text 24, corner 14; `InUseSign` 110 × 40, text 22, corner 14. Trivial.
28. **Deliveries' X sits 13 px higher than every other window's:** its centre is 6 design px above the top edge (`Header.Close` at (1, 18, 0, −24)); the other ten windows put it 10 px below (1, 22, 0, −10). Trivial.
29. **The mail popup's countdown is 11 px** on a phone (`Popup.Timer` 15 pt × 0.78). Trivial.
30. **Notices and the cheer banner land on an open bag:** `ShopHud.Notice` (y 128–170) and `WorkshopOpenGui.Banner` (y 157–225) draw over the bag's first row on a phone (R2). Rare; the notice could sit under the top bar only while the bag is closed, or above the bag.
31. **Offer cards use a plain 4 px stroke** (`DeliveryGui.Templates.Offer`, the kind's colour lightened 40%) instead of the thin hand-drawn edge every other card has. The colour carries the order kind, which the 2026-10-28 ruling lets keep a plain stroke; flagging only for Allen.

## Other agents' work seen (possibly in progress)

- **Auto Anvil switch** (`AnvilHud.Auto`): matches the Auto-Roll pill (dark 43, 28, 19 pill, 3 px Outline, knob switch with a 2 px Outline) but has no name beside the icon (Auto-Roll's says "Auto-Roll"), its switch is 52 × 28 (Auto-Roll's 48 × 26), and its icon `rbxassetid://99067729549436` (also the Shop's new Auto Anvil card) isn't in [[Art/Icon Library]] yet. It takes the anvil HUD's 0.70 scale on a phone: 81 × 36 px at y 64–100, clear of the top bar.
- **Crew level bar** (`WorldText.Tag.Bar`, hidden): the Tag billboard is 66 px tall and its four rows need 69 with the bar, so the role line is pushed 3 px above the box when the bar shows.
- **Pass label** (`WorldText.PassLabel`): "Auto Ore Roller · 149" with the Robux icon after the number; every Robux price in the menus puts it before.
- **Level prompt** (`WorldText.LevelPrompt`, seen in another agent's preview): "Lv. 3 · 55 gems" under an F square — "gems" as a word where the crew window uses the gem icon, and F where other prompts use E.

## Checked and fine

- **Fonts:** Gotham (GothamSSm Bold, Heavy, Medium) everywhere; Merriweather and Kalam only on the letters (Allen's letter art); no Fredoka.
- **Windows:** Fill gradients 120, 72, 40 → 92, 54, 30 (Shop 58, 48, 42 → 38, 31, 27), corners 16, the heavy edge on all 10 windows; titles Gotham Heavy 54 with a 5 px outline on the border (Shop, Settings, Upgrades, Daily, Auto-Roll, Odds, Crew, desktop picker); every X red 222, 50, 46, 52 design px, corner 10, thin edge, at the same spot (6 in, 10 down) on ten of eleven windows.
- **Two-layer text:** all 29 Faces match their base label (font, size, constraints, alignment, wrap, both strokes).
- **Icons:** every image is the Free Icon Pack's 1st Outline set except Allen's mailbox, the outlined Robux, the original weather icons, the letter art and the in-progress Auto Anvil icon.
- **Light text outlines:** present everywhere except #13 and #24; dark text on paper and pills has none, as it should.
- **Dims:** every window's ScreenGui ignores the top-bar inset, so the dim covers the whole screen.
- **Phone fits (844 × 390):** Shop y 64–383, Settings 120–329, Odds 92–357, Daily 84–364, Auto-Roll 132–317, Mail 65–383, Crew 74–375, Deliveries 66–382, book 70–378, pack offer and popup inside. The HUD clears the top bar (coins at y 58) and the hotbar sits between the thumbstick and the jump button (x 209–636, 5 stacks + bag); Auto-Roll's bar is under the top bar at y 66; the mail tracker shows its longest title at 14 px with "…".
- **Desktop:** pickers, Shop, Crew, Deliveries and the book scale to 1.5 (1.42) and stay inside 1080 p.

## Not checked

- Mail's letter view, Crew's Station and Staff pages and the Deliveries cart page were measured in part, not rendered (the letter view was rendered by the 2026-10-30 review).
- Several offer cards at once on a phone (each `OfferBubble` card is a fixed 280 × 132 px) — verify in Play.
- Roblox's real top-bar buttons: the 58 px band and buttons at x ≈ 12–112 are assumed, not measured in Play; #3 depends on them.
- Decorate (hidden for a later release), ActionGui (disabled) and the Dev Panel (excluded).

## Captures

R1 HUD at rest (phone + 1080p) · R2 bag + popup + notice + banner · R3 Upgrades · R4 Mail list · R5 Crew roster · R6 Deliveries packing · R7 pickers · R8 Daily + Odds · R9 Auto-Roll + pack offer · R10 Polishing + anvil HUD · R11 billboards with runtime edges · R12 book + etch + hilt seat · R13 Crew stats + Deliveries offers. Taken in Edit from temporary copies, all deleted; not saved to the vault.

---
title: UI Review — Accessibility and Input
type: review
updated: 2026-10-31
tags: [review, ui, accessibility, input, touch, gamepad, keyboard, contrast, colour-blind, motion, localization, create-swords]
---

# UI Review — Accessibility and Input (2026-10-31)

Scope: every screen and control, checked for text size, contrast, colour-only information, touch targets, gamepad, keyboard and mouse, motion and flashing, reading load, sound/visual pairing, localization readiness and safe areas. The reference device is an 844 × 390 landscape phone. Players are mostly 7–14 and 70%+ are on phones.

**How it was done.** Read-only, in Edit. Studio was never put in Play. No GUI, script or property was changed, and `ShowDevelopmentGui` was not touched (another agent had it on by the end).
- Each StarterGui ScreenGui (and the `ReplicatedStorage.WorldText` billboards) was cloned into a temporary ScreenGui under CoreGui, inside 844 × 390 and 1920 × 1080 frames, then destroyed. Every UIScale was set to the value its controller gives on that screen (table below). Repeated pieces were measured as clones placed in their real containers, using the longest real strings.
- Rendered size is `TextBounds` (it includes UIScale) or `TextSize × scale`. A `UITextSizeConstraint` clamps the size **after** UIScale, in screen pixels (checked: TextSize 8 with MinTextSize 14 draws 14 px inside a 0.7 UIScale).
- The phone frame has no notch insets. On a notched iPhone, `DeviceSafeInsets` takes about 47 px off each side, so the Scale-sized HUD lanes come out about 6% smaller than measured here.
- Contrast is WCAG 2 relative luminance, text against the colour actually behind it. Colour-blind checks use the Machado 2009 full-severity matrices and CIEDE2000 (script: scratchpad `cvd.py`, with a self-check).
- Input was read from the controllers' source. Anything that depends on the live PlayerModule is marked **verify in Play**.

**Possibly in progress (other agents, measured as found):** the Auto Anvil switch `AnvilHud.Auto` and its Shop pass card, the crew level bar `WorldText.Tag.Bar` (hidden), and the pad and Buy-button billboards. No "Level Up" prompt on crew NPCs existed yet.

| Window (UIScale source) | Phone 844 × 390 | Desktop 1920 × 1080 |
|---|---|---|
| Menu, Gem, Daily, Mail, Crew, Auto-Roll windows (`UiFx.fit` 650 × 570 / 860 × 560) | 0.70 | 1.5 |
| Deliveries (900 × 556) | 0.70 | 1.5 |
| Collection (552 × 488) | 0.80 | 1.5 |
| Pack offer (460 × 520) | 0.75 | 1.5 |
| Mail popup (900 × 500, max 1.1) | 0.78 | 1.1 |
| Phone picker `CompactWindow` (600 × 320, then the 85% rule) | 1.18 | (desktop window 1.42) |
| Polishing panel (560 × 420) | 0.93 | 1.5 |
| Hotbar bar / bag (max 1.2) | 0.75 / 0.70 | 1.2 / 1.2 |
| Anvil HUD (`AnvilController.enterView`: `min(1, height / 560)`, **no 0.7 floor**) | 0.696 (0.67 on a 375 px phone) | 1.0 |

## Findings, most valuable first

### 1. Roblox's thumbstick and jump button stay live in every station view, and the hilt sits in the thumbstick's zone (phones; verify in Play)

- **Where:**
  - `AnvilController.enterView`, `PolishController.begin`, `HiltSeat.play` and `EtchingTableController.play` take the camera and anchor the root, but never hide the touch controls. Neither `GuiService.TouchControlsEnabled` nor `UserInputService.ModalEnabled` is used anywhere.
  - All four stations' input handlers drop processed input: `if processed then return end` (AnvilController's `InputBegan` near the end of the script, which is moving while Auto Anvil is built; PolishController 537; HiltSeat 317).
- **What's wrong:**
  - With `DevTouchMovementMode = UserChoice` most phones use the dynamic thumbstick. Its zone is the left 40% of the screen and the bottom two thirds (x < 338, y > 130 on 844 × 390), and it sinks any touch that starts there.
  - **Hilt seat:** the camera puts the sword's +X to the right (worked out from `camCf`), so the hilt starts on the **left**, at about x 5–30% and mid-height. That is inside the zone, so a finger pressed on the hilt likely never reaches `nearHilt`. There is no other touch path, because Space, A and R2 are keyboard and gamepad only.
  - **Polishing:** the blade fills the screen width, so strokes that *start* on its left 40% are lost. The tutorial ghost's sweep starts at 15% along the blade, on the left.
  - The jump button and thumbstick also draw over every station view (the bottom-right 170 px corner, where the Hotbar keeps clear of it).
- **Evidence:** code reading only. The zone size is from the stock PlayerModule (`DynamicThumbstickFrame` 0.4 × 2/3). Allen's phone tests have been on the emulator; it is not recorded whether the hilt drag was tried there since 2026-10-28.
- **Fix (small, about 6 lines):** set `GuiService.TouchControlsEnabled = false` when a station view starts and back to `true` in each leave or close. Or set it once in HudFocus while a `HidesHud` ScreenGui with a Scriptable camera is up. Even if the sinking turns out not to happen, this declutters the station views.
- **Decisions:** none against. It serves "Mobile first" (2026-10-24).

### 2. A controller can't polish, and B doesn't leave the station, so a console player can't finish the tutorial

- **Where:** `PolishController` lines 537–557. The only input is Q and mouse or touch dragging. There is no ButtonB, R2 or thumbstick handling, and nothing sets `GuiService.SelectedObject` for Save or Leave.
- **What's wrong:**
  - The first letter wants a **polished** Iron Tantō (Commissions line 39), and TutorialDone waits for that letter.
  - So on a gamepad the guide stays on "Polish it" for good, and everything gated on the tutorial waits with it: the weather icon, Auto-Roll, the Shop dot, the daily window and Auto Anvil.
  - Once inside the station, B does nothing. The only way out is the hidden Select-button UI mode, reaching Leave.
- **Evidence:** the code above. The Decisions Log entry of 2026-10-22 already says "Polishing still has no gamepad input"; the 2026-10-30 letter change made it a blocker.
- **Fix (medium, about 40 lines in PolishController):**
  - Bind ButtonB (and Backspace) to `leave`, as the etching table does.
  - Hold R2 (or A) to polish: a cursor sweeps along the edge, or follows the left stick's X, and feeds the existing `polishAt` from the blade's screen points.
  - Show "Hold R2" as the hint when `UiFx.onGamepad()`, and select Save once the blade is complete.
- **Decisions:** 2026-10-22 *Gamepad controls for the core loop* (closes its gap); 2026-10-30 *The tutorial's letter wants a polished Iron Tantō*.

### 3. Hotbar names, metal lines and counts are 5–12 px on a phone, and 10 px on desktop

- **Where:** `HotbarGui.Templates.Slot`: `Title` is TextScaled in a 17-unit box with constraint 7–23; `Metal` is a 14-unit box with 6–18; `Count` is TextSize 15. They draw inside the bar's Fit (0.75) or the bag's (0.70).
- **What's wrong (measured, phone):**

  | Text | Bar (0.75) | Bag (0.70) | Desktop (1.2) |
  |---|---|---|---|
  | "Leviathan Cleaver" | 6 px | 5 px | 10 px |
  | "Hot Rose Gold" | 8 | 7 | — |
  | "Wakizashi" / "Katana" | 11 / 12 | — | — |
  | Metal "Rainbow Alloy" / "Iron" | 8 / 10 | 7 | 13 |
  | Count "×12" | 11.2 | 10.5 | — |
  | Key "1"–"9", bag "~" (key caps, excepted) | 9.8 | — | — |

  - The box itself is only 12.75 px tall on the bar, so no name can reach 14 px.
  - At 14 px "Katana" needs 47 px and "Leviathan Cleaver" 116 px; the slot is 63 px wide.
  - The 2026-10-29 review sized these lines as "17 / 14 tall" in design units, before the 0.75 scale.
  - The key numbers also show on touch, where they mean nothing.
- **Fix (small to medium):**
  - Add one **held-item line** centred above the bar: name, metal and rarity word, at least 16 px. The Hotbar already knows the stack in hand (`held`).
  - Let the slot titles stay as small tags, or drop them on touch.
  - Hide the key numbers when `PreferredInput` is Touch.
  - The same line fixes finding 4.
- **Decisions:** *Phone text floor* (2026-10-28) and *Text reads at least 14 px on a phone, key-cap hints excepted* (2026-10-29); *Smaller hotbar* (2026-10-26: six slots on a phone); *Sword titles* (2026-10-24: the metal small). A held-item line keeps all three.

### 4. Rarity on the hotbar is colour only, and Rare and Epic are the same blue to a deuteranope

- **Where:** `Hotbar.refresh` line 389 (`UIGradient` = `sheen(rarity colour)`) and `Shared.Materials.rarities`.
- **What's wrong:**
  - The hotbar and bag are the only place where an item's rarity has no word, letter or icon. Pickers have the chip word, ore labels a rarity line, the book a divider, the Odds window the names, and the callout "EPIC!".
  - Simulated rarity colours, CIEDE2000:

  | Pair | Normal | Deuteranopia | Protanopia | Tritanopia |
  |---|---|---|---|---|
  | Rare (90,160,255) vs Epic (190,110,255) | far | **1.3** (94,152,253 vs 87,148,252) | **8.0** | ok |
  | Uncommon (110,210,110) vs Legendary (255,190,60) | far | 11.3 | **6.6** | ok |
  | Uncommon vs Secret (255,70,70) | far | 10.0 | ok | ok |

  - About 1 boy in 12 has red-green colour blindness.
  - The muted picker chips (`ItemPicker.CHIP`) collide too (Rare/Epic 0.5 in deuteranopia, Common/Uncommon 5.3, Uncommon/Secret 5.6), but every chip carries its rarity word, so that's fine.
- **Fix (small):** a second cue on the slot. Either the held-item line from finding 3, or a corner pip count of 1–6 (readable without reading). An optional palette tweak, Epic → (230,100,200), lifts the worst pair from 1.3 to 6.6. No hue change separates all six, so the second cue is the real fix.
- **Decisions:** *Hotbar slots are a metal sheen in their item's rarity colour* (2026-10-30, Allen's pick). This adds a cue; it doesn't replace the sheen.

### 5. One tap on a 28 px icon deletes a single sword, and it sits beside the card you tap to equip

- **Where:** `HotbarGui.Templates.Slot.Trash` (40 × 40 design units → **28 × 28 px** in the phone bag), `Stepper.Less` and `More` (29 × 28), and `Hotbar` lines 293–301.
- **What's wrong:**
  - For a single item (every sword), the first tap throws it away: `#stack > 1` arms; anything else trashes. There is no undo.
  - The trash sits in the top-left corner of a 58 × 70 card that is itself tappable (equip) and draggable.
  - A Legendary sword is one mis-tap from gone, for a 7-year-old on a phone.
- **Fix (small):**
  - Arm on the first tap for single items too (the red Armed chip already exists), and delete on the second.
  - Give the trash an invisible 44 px hit pad by making the button larger than its icon.
- **Decisions:** 2026-10-30 *Bag cards get a trash and a − N + count* ("One item goes at the first tap"). This changes Allen's rule for single items; it's his call.

### 6. On a gamepad, D-pad right closes the Collection and D-pad left closes the Gem Shop, while you navigate inside them

- **Where:**
  - `CollectionController` lines 347–356: `CollectionBook` on DPadRight.
  - `GemController` lines 316–325: `GemShop` on DPadLeft.
- **What's wrong:**
  - Both pass only when the selected object is **outside** their own GUI. Inside, they toggle.
  - In the book's 4-wide grid, or moving from the Metals tab to Swords, D-pad right shuts the book.
  - In the Gem Shop D-pad left shuts it, and in the Daily window D-pad left swaps it for the Gem Shop.
  - The Collection also opens with focus on its ScrollingFrame (`SelectedObject = grid`, line 335), not on an entry.
- **Fix (tiny):** pass whenever `SelectedObject` is set at all, so the shortcuts only fire when no window has focus. Select the first entry instead of the grid.
- **Decisions:** UI Design 2026-10-23: "D-pad left no longer opens the Gem Shop over another window". This finishes that rule.

### 7. Controller buttons are named as Xbox letters, and on PlayStation the prompt's "X" is the jump button

- **Where:**
  - `PromptStyle` lines 97–99: `GamepadKeyCode.Name:gsub("^Button", "")` gives "X" on every prompt square.
  - `ShopController` 157–158: "Accept (Y)", "Decline (L2)".
  - `TycoonController` 436: "Buy (Y)".
  - `HiltSeat` 274: "Hold A to push the hilt on".
  - `AnvilController`: "Press R2".
- **What's wrong:** on a DualShock the prompt key `ButtonX` is □ and `ButtonA` is ✕. A child reading "X" presses ✕, which jumps.
- **Fix (small):** draw `UserInputService:GetImageForKeyCode(prompt.GamepadKeyCode)` in the prompt square (an ImageLabel next to `Key`). Build the inline labels from `GetStringForKeyCode` or an icon. TopbarPlus already does this.
- **Decisions:** 2026-10-22 *Gamepad controls* ("the buttons say (Y) and (L2) on a gamepad"). The same buttons, drawn for each platform.

### 8. Many tap targets are under 36 px tall on the phone, and the window X buttons are 36 px

Measured at 844 × 390 (Allen's target is 44 px; anything under 36 is flagged):

| Control | Phone size | Note |
|---|---|---|
| Hotbar bag card trash / − / + | 28 × 28 / 29 × 28 | destructive (finding 5) |
| Mail `Header.TitleRow.Back` ‹ | **22** × 33 | also Crew's ‹ |
| Mail `ActiveOnly` toggle | 117 × **25** | |
| Settings `Music` / `Sound` / `Weather` `Switch` | 50 × **26** | only the pill toggles, not the row |
| Auto-Roll config `Quest.Switch` / `Selector.Left` and `Right` | 50 × 26 / **32 × 32** | |
| Deliveries strip `AutoFill`, `Send`, `Collect`, `Pin` | 101 / 101 / 112 / 61 × **28** | the crate slots are 36 px with 4 crates; 28 or 14 px with more (Sessions 2026-10-30) |
| Crew `Card.Price`, `Stats.Panel.LevelUp`, `Stats.Top` tabs, `Staff.Etch.Pick`, `Setting.Slider` | 148 × 28, 105 × 28, 91 × 30, 91 × 30, 506 × 30 | |
| Shop `Buy` (passes / currency) | 110 × **29** / 75 × 29 | |
| Mail tracker rows / `Fold` | 120–244 × **30**, no gap between rows / 30 × 30 | each row opens a different letter |
| Pack offer `Buy` / `Close` | 130 × 31 / 39 × 39 | |
| `ShopHud` SlotMarker circle (world, fixed px) | 33 × 33 | racks put six side by side |
| Mail letter `Decline` / `Accept` / `Send` | 72 × 35 | |
| Every window's X (52 design units × 0.7) | 36 × 36 | Collection 41, the phone picker's is fine |
| Anvil `Cancel` / `Finish`, `Auto` (in progress) | 97 / 125 / 80 × 36 | the anvil's scale has no 0.7 floor (0.67 on a 375 px phone) |
| HUD menu buttons / Mail | 44 × 40 / 46 × 42 | 7 px between rows |
| Weather icon | 42 × 42 | in the thumbstick corner (finding 17) |

- **Fine:** the world prompt square (60 px), the pad Buy button (132 × 48), the bag button (63 × 75), the bag's drop trash (45 px), the picker cards and the X on the phone picker, Daily Claim (168 × 42), and the station drags. The anvil counts a tap within 70 px of the 44 px ring (a 140 px circle), the hilt grabs within 70 px, and polishing searches 14 and 27 px rings round the finger.
- **Fix (medium, StarterGui only):**
  - Keep the visuals and grow the hit area. A button can be bigger than its visible art: a transparent TextButton 44 px tall holding the 26 px pill, or a UIPadding'd parent.
  - Make each Settings row the toggle.
  - Put 8 px between tracker rows.
  - Clamp the anvil HUD scale at 0.7, as `UiFx.fit` does.
- **Decisions:**
  - 2026-10-26: the SlotMarker made 33 px (Allen: "like 25% smaller"). Keep the look and pad only the hit area.
  - *Toggles are knob pills* (2026-10-28) and *The mail tracker is a bullet list* (2026-10-31): looks unchanged.

### 9. "COLLECTION" is 9 px and "UPGRADES" 10 px under their HUD icons

- **Where:** `MenuGui.Buttons.<name>.Label`: TextScaled in a box 57 × 14 px on the phone (76 × 19 at 1080p).
- **What's wrong:** SHOP and CREW reach 14 px, MAIL 15, UPGRADES 10 and COLLECTION 9. On desktop they are 14 and 12.
  - At 14 px, Gotham Heavy "COLLECTION" needs 84 px and "UPGRADES" 73.
  - The 2 × 2 grid's column pitch is 62 px (44 px buttons, an 18 px gap), inside a 199 px lane.
- **Fix (small, StarterGui):** widen the grid's horizontal padding so the pitch is about 90 px, give each label the full cell width, and add `UITextSizeConstraint` MinTextSize 14 to each label and its Face.
- **Decisions:** 2026-10-30 *HUD menu is 2 × 2 … HUD labels in capitals with a thick dark outline*. Spacing only; the names stay.

### 10. Station and popup text under 14 px

| Label | Phone size | Source |
|---|---|---|
| `AnvilHud.Hint` ("Strike inside the circle.", "Press R2", "Couldn't start, try again") | **11.1 px** | TextSize 16 × 0.696 |
| `MailGui.Popup.Timer` (the countdown) | 11.7 | 15 × 0.78 |
| Deliveries packing card `Chip.Label` and `Price.Amount` | 12.6 | 18 × 0.70 |
| `PolishHud.Panel.Hint` ("Drag along the edge", "+13% value") | 13.0 | 14 × 0.93 |
| `CollectionGui` entry label ("Rainbow Alloy") | 13.0 | TextScaled, no min |
| `PolishHud.Panel.Status` ("Polished 87%") | 13.9 | 15 × 0.93 |
| `WorldText.Tag.Role` (crew NPC) | 14.0 | world, fixed px |

- **Fix (small):** TextSize Hint 16 → 21, Timer 15 → 18, packing chip and price 18 → 20, polish Hint 14 → 16 and Status 15 → 16, and the Collection label constraint min 14. The anvil Hint also gains from the 0.7 clamp in finding 8.
- **Decisions:** the phone text floor; 2026-10-29 *Polishing text cut to the percentage and one short line* (sizes only; the words stay).

### 11. Gamepad players can't reach the HUD menu or the tutorial's buttons without a hidden mode

- **Where:** `MenuController`, `MailController`, `Guide` and the HUD buttons.
- **What's wrong:**
  - Mail, Shop, Crew, the bag, the Auto-Roll bar, the new-letter popup and the anvil's Finish and Auto have no gamepad button. They are reachable only through Roblox's Select-button UI mode, which nothing on screen mentions.
  - D-pad left (Upgrades) and D-pad right (Collection) work (finding 6), and so does D-pad up (TopbarPlus: Daily and Settings), but none of them is shown either.
  - The tutorial's button steps — the popup, Mail, Accept, Send, the House — are all spotlit taps.
- **Fix (small):**
  - In `Guide`, when the step's `button` is set and `UiFx.onGamepad()`, set `GuiService.SelectedObject = button`, so A presses what the spotlight shows. That's about 4 lines.
  - Bind D-pad down to Mail.
  - Bind ButtonY to Finish at the anvil while it is lit.
- **Decisions:** Spotlight (Refinements 5): "anything that involves clicking on the UI should have a spotlight". This makes the spotlight pressable from a pad.

### 12. Gamepad focus: decided by "a pad is connected", drawn by Roblox's default box, lands on lists, and isn't restored

- **What's wrong:**
  - Eight controllers set `SelectedObject` when `UserInputService.GamepadEnabled`, which is true whenever a pad is connected, even an idle one: ItemPicker 628, Mail 451, Gem 103, Collection 334, Delivery 703, Employee 745, Menu 108, PackOffer. The labels already moved to `UiFx.onGamepad()` for this reason (2026-10-30).
  - `SelectionImageObject` is set nowhere. Only HUD buttons, picker cards, Gem and Delivery buttons and Mail's Send show the amber edge; everything else gets Roblox's default box.
  - 8 of 10 list ScrollingFrames are `Selectable`, an extra stop that highlights the whole list.
  - `AutoRollController.open` sets no focus.
  - Closing a window sets `SelectedObject = nil` instead of returning to the button that opened it.
- **Fix (small):**
  - Use `UiFx.onGamepad()` (or `PreferredInput == Gamepad`) at those eight sites.
  - Add one shared selection ring in StarterGui, assigned in `UiFx.press`, which already touches every button.
  - Set `Selectable = false` on the eight lists.
  - Remember and restore the opener on close.
- **Decisions:** none.

### 13. The Odds window's "Epic" and "Secret" names have no outline (2.9:1 and 2.6:1)

- **Where:** `MenuGui.OddsWindow.Content.Body.Table.Epic.Name` and `.Secret.Name`. The other four rows' Names have a 2.5 px stroke.
- **Evidence:** (190,110,255) on the window fill (106,63,35 average) is 2.92:1; (255,70,70) is 2.65:1. That is at 16 px on a phone, where 4.5:1 is needed and even large text needs 3:1.
- **Fix (tiny):** copy the `UIStroke` from the `Rare.Name` row.
- **Decisions:** 2026-10-28 *light menu text has a black outline*.

### 14. Every bright card's white text depends on its outline; keep it on everything

- **What:** without its outline, white text measures 1.75:1 on the Shop's lime cards (117,220,30), 1.87 on gold, 2.03 on teal, 2.51 on orange, 3.23 on pink, 3.81 on red (Auto Anvil), 4.08 on blue and 4.13 on purple. Buy buttons are 2.66:1. The green pad and Buy-button text sits over the world.
- **Today:** the outlines are 2.5–5 px (0.1–0.16 of the text size, with a near-black colour), which makes the text readable. Every outline-less failure found is in finding 13. All other contrast failures (Crew 37, Deliveries 33, Gem 15, Mail 18, Shop 90) are outlined white or cream text.
- **Fix:** none needed. When adding text on a coloured card, add the stroke (new-ui-checklist item 1).

### 15. No reduced-motion path; the camera shakes and loops can't be turned down

- **Where:** no game script reads `GuiService.ReducedMotionEnabled` (only TopbarPlus does).
- **What moves:**

  | Effect | Size and timing | Where |
  |---|---|---|
  | Hilt seat punch | random jitter 0.15–0.40 studs (rarity tier) for 0.3 s, plus a push-in | `HiltSeat` 288–298 |
  | Ore roll punch, Epic and up | 0.15–0.35 studs for 0.25 s, also from a neighbour's roll within 30 studs | `OreBoxShow.punch` (`NEAR = 30`) |
  | Anvil | 0.03 studs for 0.15 s on each of 10 strikes | `AnvilController.impact` |
  | Ore flicker | 10 metal swaps (dark Black Iron ↔ light Iron) over about 1 s, starting near 30 swaps a second (easeOut) | `OreBoxShow` 305–321 |
  | Ore climb flash | a PointLight burst every 0.55 s (1.8 a second), up to brightness 12.5, red for Secret | `OreBoxShow` 339–343 |
  | Shop icon | rays turn every 8 s; the icon hops every 5–9 s, forever | `MenuController` 52–72 |
  | Station glow (tutorial) | fill pulse 0.8 Hz | `Guide` 90–94 |
  | Auto-Roll and Auto Anvil icons | turn every 4 s while on | |

- **Flashing:** nothing exceeds 3 flashes a second over a large area. The 30-a-second flicker is six small ingots, well under WCAG's area limit, so the risk is low.
- **Fix (small):**
  - Read `GuiService.ReducedMotionEnabled` once in `UiFx` (`UiFx.calm`).
  - When it's on: zero the camera shakes and punches, cap the flicker at about 6 swaps a second, stop the Shop hop and rays, and hold the station glow steady.
  - Optionally add a Settings row, beside Allen's existing Weather switch (2026-10-29), which is already an accessibility option.
- **Decisions:** 2026-10-29 *Ore rolls escalate with rarity* (camera shake from Epic); 2026-10-30 *The hilt seat hits harder*; 2026-10-29 the Shop icon hop (Allen). Only when the player asks for less motion.

### 16. Keyboard: half the windows have no close key, and Polishing has no B

- **What:**
  - Pickers, Mail and the etching table close on Q, Backspace and B.
  - The Gem Shop, Daily, Collection, Deliveries, Crew, Shop, Settings, Odds, Auto-Roll config and pack offer bind only ButtonB. Keyboard players must click X, and Escape opens Roblox's menu.
  - Polishing leaves only on Q.
- **Bag key:** `Backquote`, labelled "~". On many non-US layouts that key is ^, ` or ²; `GetStringForKeyCode(Enum.KeyCode.Backquote)` gives the right label.
- **No conflicts found with Roblox defaults:**
  - Backspace drop is off (`CanBeDropped = false`).
  - Space at the anvil can't jump (the root is anchored).
  - The core Backpack is disabled.
  - Hover states exist on every `UiFx.press` button, and picker cards get an amber edge.
- **Fix (tiny):** add Q and Backspace to those `BindAction` calls, and ButtonB to PolishController.
- **Decisions:** UI Design 2026-10-23: "Q and Backspace close a picker as well as gamepad B". This extends it.

### 17. The weather icon sits where a thumb rests to walk

- **Where:** `WeatherGui.Icon`, 42 × 42 at (12, 335)–(54, 377) on 844 × 390, the bottom-left corner of the thumbstick zone.
- **What's wrong:** a touch that starts on the icon goes to the icon, so the character doesn't move and the tip opens.
- **Fix (tiny):** move it into the left column under the menu, or above the hotbar's left end.
- **Decisions:** 2026-10-28, Allen: "have [an icon] on the bottom left". Moving it is his call.

### 18. Gamepad and keyboard hints are missing at the anvil and the markers

- **What:**
  - While forging, the anvil shows no "R2" hint. "Press R2" appears only in the idle state.
  - Shop holder and rack markers light up for a gamepad (`focus(on, keyboard = false)`) but show no button; only "E" shows for a keyboard.
  - The Auto Anvil switch (in progress) has an icon and a knob but no words.
- **Fix (small):** a small glyph in the strike ring or beside Finish when `onGamepad()`; the gamepad glyph in `SlotMarker.focus`.
- **Decisions:** 2026-10-30 *The anvil's bar marks where Finish opens*.

### 19. Toasts vanish after 2.5 s whatever their length

- **Where:** `ItemPicker.toast` line 709.
- **What's wrong:** "Couldn't save the polish, keep going and try again" is 9 words in 2.5 s, about 216 words a minute. Readers aged 7–9 read 100–150. The cheer banner (5 words, 2.4 s) and the mail popup (8 or 15 s with a countdown) are fine.
- **Fix (tiny):** `task.delay(math.max(2.5, 1.2 + 0.35 * words), …)`.
- **Decisions:** none. The minimal-text rule makes most toasts short.

### 20. Offers and a finished furnace rely on sound when they're off-screen

- **Where:** `Cues`. Its own rule says "every cue has a visual twin", but the twins are in the world:
  - The offer bubble is AlwaysOnTop but MaxDistance 35, and only shows when the customer is on screen.
  - The furnace's "Ready!" pill and the cart's return have a 2D sound only, unless the order is pinned.
- **What's wrong:** many kids play phones muted, and an offer lasts 20 s.
- **Fix (small):** a dot on the HUD (Mail-button style) or a screen-edge pip while an offer waits.
- **Decisions:** none.

### 21. Localization isn't ready (flag only)

- **What:**
  - There is no LocalizationTable. `AutoLocalize` is on everywhere (0 GUI objects off).
  - 42 of the 157 `.Text =` writes in the client scripts build the string by interpolation, for example `Polished {pct}%`, `VIP · {sword}`, `Sell it to afford the {name}`, `Pull the lever for {metal}`, "Accept (Y)". So do the servers' `"<sender> wants this!"` and prompt texts. Auto-translation can't match these; they need `Translator:FormatByKey` with parameters.
  - RichText `<font>` tags sit inside translatable strings (offer amount, picker chips, weather tip).
  - `UiFx.commas` hard-codes "," as the thousands separator.
  - Fixed TextScaled boxes would shrink longer languages further: the HUD labels' 57 × 14, the hotbar's 57 × 12, the pad titles' 14–28.
  - Fonts: GothamSSm on 1,066 labels, Merriweather and Kalam on the letters, and no legacy fonts on text that shows.
- **Fix:** none until a language is planned. Then use keyed strings for the dynamic lines first.

### 22. Safe areas: mostly right; check chat and the player list in Play

- **Fine:**
  - The windows and HUD use `DeviceSafeInsets` with `IgnoreGuiInset`, and station HUDs use `CoreUISafeInsets`.
  - The picker, Collection and etching ring read `GuiService.TopbarInset`.
  - The dims cover the whole screen.
- **Check:**
  - The other windows and the HUD lanes hard-code the top bar: `(0.5, 0, 0.5, 29)` and `{1, 0, 1, -58}`.
  - The chat window is set to the top right (`ChatWindowConfiguration` Right/Top). On a phone, opened chat would cover the Mail button (y 89–131) and the tracker (y 143–243).
  - `leaderstats` exists, so on desktop the player list also draws at the top right.
  - The Hotbar's jump clearance is a fixed 170 px, not measured from `TouchGui`.
  - There is no TV-safe margin for console: the HUD is 12 px from the edge, and `IsTenFootInterface` isn't used.
- **Fix:** read `TopbarInset` where it's hard-coded (small). Look at chat and the player list on a phone and on desktop.

### 23. Reading load: good tutorial lines, a few hard words

- **Good:** the guide's lines are short and concrete: "Pull the lever", "Heat the ingot", "Put it on display", "A customer is coming!". Numbers have commas, and the Gem Shop stats are "1x → 1.2x".
- **Harder:**
  - The first letter opens with an idiom, "Word is a new smith opened on the street" (23 words).
  - Lucky Ore's card says "Luck one merge higher" ("merge" is unexplained).
  - The anvil says "Click the anvil" on a phone (`AnvilController` 415).
  - The odds show "0.150%".
- **Fix (tiny, copy):** "I heard a new smith opened here!"; "Find rarer ore"; "Tap the anvil" on touch.
- **Decisions:** the letter texts are Claude's defaults; the odds format follows Create Pottery (2026-10-28).

### 24. Window text at 14–15.4 px meets the floor but misses the checklist's 16

Crew `Value` labels (14 px: the roster's Quality and Forge Time, every Stats and Staff row), Mail letter rows (gems 14, preview 15.4, the letter's want 14), Delivery chips (Town and Need 14, extras 15.4, packing titles 14.7), the anvil's Cancel and Finish (15.3), and the offer bubble's detail and hint (15, world). TextSize 20 → 23 in a 0.7 window gives 16.1 px. **Small.**

## What's already good

- **States never rely on hue alone:**
  - Toggles move their knob; the Gem Shop ticks are 8.7:1 on/off; Daily tiles show a ✓; toasts carry ✓ or !.
  - Offer percentages have a sign; delivery steps get tick badges; locked cards get a dark veil; the stack in hand gets an edge.
  - Chips name their rarity.
- **Drags are forgiving:** the anvil counts a tap within 70 px of its 44 px ring, the hilt grabs within 70 px, and polishing searches grace rings round the finger. The strike and hilt are untimed.
- **Gamepad basics exist:** B closes every window, pickers select their first card, lists are SelectionGroups, the Crew slider takes the D-pad, the hotbar cycles on R1/L1, and Y and L2 answer offers.
- **Motion and flashing:** nothing over 3 flashes a second; the confetti is short and once; the hilt reveal can be skipped; there's haptic feedback.
- **Text:** windows in the Shop, Gem Shop, Daily, picker, Auto-Roll and pack offer are all ≥ 16 px on a phone; the guide line is 22 px; the world prompt is 60 px with 20 px words.
- **Settings:** a Weather switch that drops weather visuals and sound (a real comfort option).

## To test in Play (Allen)

1. **Phone or emulator:** forge a sword. At the hilt seat, press on the hilt (left side) and drag right. Does it move? Then polish starting from the blade's left end. If either fails, that's finding 1.
2. **Controller:** finish the tutorial with only a pad. Expect to be stuck at "Polish it", and that B won't leave the polishing station.
3. **Controller:** open the book (D-pad right), then press D-pad right again on an entry: it closes. Open Daily and press D-pad left: it becomes the Gem Shop.
4. **PlayStation pad, or the emulator set to PS:** the prompt square says "X".
5. **Phone:** read a hotbar sword name and a rack's markers, and try to hit the bag card's trash without equipping the card.
6. **Desktop with chat open and a second player:** the top-right corner (chat, player list, Mail button, tracker).

## Measurement appendix

### Text under 14 px on the phone (all screens)

| Where | Size |
|---|---|
| Hotbar slot Title / Metal / Count / Key | 5–12 / 7–10 / 10.5–11.2 / 9.8 (key cap) |
| HUD menu labels COLLECTION / UPGRADES (SETTINGS, hidden: 12) | 9 / 10 |
| `AnvilHud.Hint` | 11.1 |
| Mail popup timer | 11.7 |
| `ShopHud` SlotMarker key "E" | 12 (key cap) |
| Deliveries packing chip and price | 12.6 |
| Polish Hint / Status | 13.0 / 13.9 |
| Collection entry name (longest) | 13.0 |

Desktop 1920 × 1080: only the hotbar names (10 px for the longest, metal 13) and COLLECTION (12) are under 14.

### Window minimum text on the phone

Shop 16.1 · Settings 17.5 · Odds 16.1 · Daily 16.8 · Gem Shop 16.1 · Auto-Roll config 16.8 · Pack offer 17.2 · Phone picker 23.5 · Polishing 13.0 · Mail 14.0 · Crew 14.0 · Deliveries 12.6 · Collection 13.0 · Anvil 11.1.

### Contrast without an outline (fails)

`OddsWindow` Epic 2.92:1, Secret 2.65:1. Everything else under 4.5:1 is outlined (finding 14). The Mail letter rows are dark text on the paper image (`PaperBg`); the image's colour can't be read by script, so they weren't scored.

### Gamepad map (as built)

| Context | Buttons |
|---|---|
| World prompts | X (hold for the lever) |
| Pads | Y buys |
| Offers | Y accept, L2 decline |
| Hotbar | R1 / L1 cycle; no bag, trash or reorder |
| HUD | D-pad left: Upgrades; D-pad right: Collection; D-pad up: top bar (Daily, Settings); everything else only through Select-mode |
| Pickers | first card selected, A picks, B closes |
| Windows | B closes; focus on X (Menu windows, Crew), first item (Mail, Gem, Deliveries), the list frame (Collection), Buy (pack offer), none (Auto-Roll) |
| Anvil | R2 strikes or opens the ingot picker, B leaves; Finish and Auto have no button |
| Hilt seat | hold A or R2 |
| Polishing | **nothing** |
| Etching | B leaves |

### Keyboard map

E prompts · Q / Backspace close pickers, Mail and etching · Q leaves the anvil and polishing · Space / Enter strike · Space holds the hilt · 1–9 hotbar · ` (shown "~") bag · Escape → Roblox's menu, which closes windows.

Related: [[Development/Code Map]] · [[Design/Decisions Log]] · [[Art/UI Design]] · [[Sessions/2026-10-30#UI review of the evening's work]] · [[Design/Reviews 2026-10-31/Map Review — Village]]

---
title: "Handoff — Settings"
type: handoff
updated: 2026-10-31
tags: [settings, audio, qol, accessibility, create-swords]
---

# Handoff — Settings (2026-10-31)

All the work below is in Studio, in Edit. The new code compiles or loads, and SaveSpec passes all 5 of my new checks. Its other 2 failures (Quicker Mail, Furnace 2) were not caused by these changes. Nothing has been tested in Play. Source: [[Design/QoL and Settings Ideas — 2026-10-31]] (C1–C5, top-10 items 2, 3, 4, 5 and 10).

## Done

**`StarterGui.MenuGui.SettingsWindow`** is now one scrolling page at a fixed 416 × 440 (it was auto-height). It draws at 291 × 308 px on an 844 × 390 phone (0.7) and at 624 × 660 px on 1920 × 1080 (1.5).
- **Body:** a ScrollingFrame, 388 × 374. It uses the Shop list's bar: 6 px, copper 168,106,62, inset Always. Padding is L 6 / T 6 / B 16, with 14 between items.
- **Content padding** is now 14 on each side (it was 28). The title and X were moved so they sit where they did before.
- **Section headers** are copies of the Shop's GAME PASSES header, 360 × 30, Gotham Heavy 25: `SoundHeader`, `ScreenHeader`, `PlayHeader`.
- **Rows** are 360 × 68 TextButtons with today's look (label, knob pill, EdgeArt). Tapping anywhere on a row flips it. Each row is one gamepad stop; the pill itself has `Selectable` off.
  - **SOUND:** `Music`, `Sound`. Sound has `Gear`, a copy of the Auto-Roll bar's gear (46 × 46), 12 px left of the pill.
  - **SCREEN:** `Weather`, `Shake` ("Camera shake"), `ReduceMotion` ("Reduce motion"), `Haptics` ("Vibration"). Vibration only shows on touch or with a gamepad.
  - **PLAY:** `Tracker` ("Quest tracker"). This is the mail tracker's fold, and it is saved.

**`StarterGui.MenuGui.VolumeWindow`** (new) uses the Settings frame at a fixed 416 × 298. Its title is "Volume", and its X and B go back to Settings.
- Three rows of 360 × 68: `Music`, `Effects`, `Alerts`.
- Each row has a `Slider` (220 × 38) built from the pill's parts:
  - `Track`: 190 × 16, dark 74,58,48, the pill's corner and 2 px black `Outline`.
  - `Fill`: green 93,187,70.
  - `Knob`: cream, 30 × 30, black outline.
- Steps are 0–100% in 10s. You can drag or tap anywhere on a row, or use the D-pad or left stick.
- The value is saved 0.4 s after the last move. If the server drops it, it is sent again up to 3 times.
- When you let go, Effects plays the Sale cue and Alerts plays the Offer cue. At 0 the label dims.

**`SoundService`**
- **New `Alerts` SoundGroup** (volume 1). `Effects.Cues.Offer`, `FurnaceReady` and `CartBack` now have `SoundGroup = Alerts`. No other sounds call you somewhere.
  - They stay in `Effects.Cues` because `Cues.play` looks them up there.
- **`Music`** has three APM tracks (APMOfficial, Roblox's licensed library). Each has Volume 0.5, is not looped and is not playing in Edit. They play in a loop starting from a random one:
  - `1 Minimal Koto`: 1846310773, 120.9 s
  - `2 Kioku`: 1838864669, 83.4 s
  - `3 Aichaku`: 1838864619, 160.3 s
  - They were picked by name and length; nobody has listened to them. To swap one, change its SoundId.

**`MenuController`**
- The Settings rows and how the groups mix:
  - Music volume is set by the Music pill times (Music volume)².
  - Effects and Alerts are set by the Sound pill times (their volume)².
  - Turning music off pauses the track.
- The Volume window, with its X and B going back to Settings; Escape closes everything.
- The music player starts 4 s after you join. If an older copy of the script left a track playing (after a Dev Panel reset), it carries on from it.
- The Shop icon's rays pause and its hops are skipped while `Prefs.motion()` is false.

**`UiFx.open`**: when `Prefs.motion()` is false, windows appear in place at once with no rise. A real fade would need a CanvasGroup per window or a tween on every descendant.

**`MailController`**: the fold starts from the `Tracker` attribute, a tap sends `Setting("Tracker")`, and the fold follows the attribute (so the Settings pill and the fold stay the same).

**`DeliveryController`**: Pin works the same way with `CartPin` (off by default).

**`SmithyCore`** gets these new keys, used in its type, `fresh()`, decode, `showSettings` and the `Setting` whitelist:

| Key | Attribute and `Setting` name | Default |
|---|---|---|
| `shake` | `Shake` | true |
| `haptics` | `Haptics` | true |
| `reduceMotion` | `ReduceMotion` | nil (follows Roblox's switch) |
| `tracker` | `Tracker` | true |
| `cartPin` | `CartPin` | false |
| `musicVolume` | `MusicVolume` | 0.7 |
| `effectsVolume` | `EffectsVolume` | 1 |
| `alertsVolume` | `AlertsVolume` | 1 |

- The switches only accept booleans.
- New `SmithyCore.volume(v, default)`: anything that isn't a finite number is refused; numbers are clamped to 0–1 and rounded to 0.1.
- All of these go through `allowCall`.
- encode is now `table.clone(d.settings)`.
- No migration: a missing key loads as its default.

**`ServerStorage.Tests.SaveSpec`**: 5 new checks covering defaults, a full round trip, reduce motion staying off, odd and missing values loading as defaults, and clamping and refusals.

Copies of the old window and script are in `ServerStorage.Legacy` as `SettingsWindow_beforeSections` and `MenuController_beforeSections`.

## Checks
- **Compile and load:** MenuController, MailController and DeliveryController compile; UiFx loads from a fresh clone; SmithyCore loads in the sandbox.
- **SaveSpec in the sandbox: 120/122** (gsubs 1 / 10 / 2). All 5 new checks pass. The 2 failures are "Quicker Mail: a letter every 3:00" and "Furnace 2 comes after Faster Heating III". They test `GemUpgrades` and `Upgrades`, which this work didn't touch.
- **Renders at 844 × 390 (0.7):**
  - The window spans x 276–568 and y 70–378, with the title from y 51, so it clears the top bar.
  - Rows are 252 × 48 px with equal 19.6 px margins. The smallest text is 17.5 px.
  - The longest label is "Reduce motion" at 118 px, with 61 px to spare before the pill. The gear is 32 px.
  - The Volume window spans y 120–328. Its tracks are 133 × 11 px and the knob is 21 px.
- **Renders at 1920 × 1080 (1.5):** Settings is 624 × 660 with 42 px margins on each side; Volume is 624 × 447.
- **States rendered:** on and off, scrolled to the top and the bottom, Vibration hidden, volumes at 0 / 30 / 100%. The previews are deleted, ShowDevelopmentGui is back off, and the camera is Fixed.

## Not done
- **`Prefs.motion()` needs a change** (Prefs isn't in this fence). At the moment, if Roblox's Reduce Motion is on, the player can't turn motion back on: the pill moves but motion stays reduced. Suggested fix: `local c = player:GetAttribute("ReduceMotion"); if c == nil then return not GuiService.ReducedMotionEnabled end; return c ~= true`.
- **Reduced motion not wired yet:** coins flying to the HUD (Hud/CoinFly), the spotlight glide (Guide), the station glow pulse, the Auto-Roll and Auto Anvil icon spins, and the camera shakes and haptics. The station scripts need to call Prefs for those.
- **The Cashier's slider** (`CrewGui`, `EmployeeController`) still has its old look; the note asks for it to get the same restyle.
- **No number on the slider's knob:** at 30 units it would draw under 14 px on a phone.
- **The Code Map** isn't updated: it needs `SoundService.Alerts`, the new attributes and `Setting` names.
- **Not checked in Play:** that Alerts still rings with Effects at 0 (their folder sits under the Effects group). That the music is calm and at a good loudness.

## Questions for Allen
1. Are these three APM tracks right, and is a default of 70% music (0.245 effective) the right loudness?
2. Should Vibration sit in SCREEN or PLAY? It's one LayoutOrder change.
3. Is a Volume window that opens from Settings, with its X going back to Settings, the right flow?

## What to test in Play
1. Join and wait about 4 s: koto music plays quietly. The Music pill stops and resumes it; Music volume at 0 silences it.
2. Open Settings: the page scrolls, and tapping anywhere on a row flips its pill.
3. Sound gear → Volume:
   - Drag each slider; you hear the Sale and Offer samples when you let go.
   - Set Effects to 0: the anvil goes silent, but a customer's offer still rings.
   - With the Sound pill off, nothing plays except music.
4. Rejoin: every pill and volume comes back as you left it.
5. Reduce motion on: the Shop icon stops hopping and its rays stop, and windows appear without rising. Roblox's own Reduce Motion should turn the pill on until you choose.
6. Fold the mail tracker, rejoin: it's still folded. The Settings Quest tracker pill folds it too.
7. Pin a cart order, rejoin: it's still pinned.
8. Gamepad: each row is one stop, A flips it, the D-pad moves the volume sliders, and B in Volume goes back to Settings.
9. Phone: Vibration shows. On PC with no gamepad it is hidden.

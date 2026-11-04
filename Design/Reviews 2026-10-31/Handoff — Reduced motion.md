---
title: "Handoff — Reduced motion"
type: handoff
updated: 2026-10-31
tags: [settings, accessibility, gamepad, create-swords]
---

# Handoff — Reduced motion (2026-10-31)

All of this was done in Studio, in Edit. Every edited script compiles, and CoinFly and Prefs load from fresh clones. Nothing has been tested in Play. This picks up the "Not done" list in [[Handoff — Settings]] and A11 in [[Handoff — UI review fixes]].

## 1. `Prefs.motion()` — no change needed
`Prefs.motion()` (lines 15–21) already has the suggested fix. When the player hasn't set ReduceMotion, it follows Roblox's switch. Once they set it, their choice wins either way. I checked the other code that reads the same setting, and it all agrees:
- MenuController's `isOn("ReduceMotion")` (line 174) returns Roblox's switch while the attribute is nil. `flip` always sends a real true or false, and SmithyCore accepts only booleans.
- `Prefs.shake()` is `motion() and Shake ~= false`.
- `Prefs.haptics()` depends only on the Vibration switch.

## 2. Reduced motion wired in
- **Hud**
  - Line 23: requires Prefs.
  - Line 99: when `flyCoins` runs with motion off, it adds the amount to the count and returns. No popup and no flying coins.
- **CoinFly** (the Polish and Etch value pill)
  - Line 16: requires Prefs.
  - Line 95: with motion off, `fly()` skips the coin and calls `land()` straight away, so the number still rolls up.
- **Guide**
  - Line 51: requires Prefs.
  - Line 98: the station Highlight holds a steady fill of 0.2 (its brightest) instead of pulsing.
  - Line 367: with motion off, the spotlight jumps to its target (`k = 1`). This also skips the opening iris. The shade still fades in.
- **AutoRollController**
  - Line 35: requires Prefs.
  - Line 87: the icon spins only when the toggle is on and motion is on.
  - Lines 111 and 114: `refresh` now also runs when the ReduceMotion attribute or Roblox's ReducedMotionEnabled changes.
- **AnvilController** (Auto Anvil)
  - Line 914: the hammer nods only when it's on and motion is on.
  - Lines 950–951: the same two triggers re-run `refreshAuto`.

**Shakes and rumbles:** every one is already gated. The anvil blow shake (AnvilController line 370), the hilt seat's punch (HiltSeat line 285) and the roll's CameraOffset shake (OreBoxShow line 119) all check `Prefs.shake()`. The HiltSeat `buzz` (line 66) and the OreBoxShow pad rumble (line 134) check `Prefs.haptics()`. I found none that skip the check.

## 3. Guide: select the spotlit button on a pad (A11)
- Line 36: `GuiService` added. Line 52: `UiFx` required.
- Line 408: new `padSpot`, the target the pad selection last jumped to.
- Line 953, after `spotTarget = …`: when the spotlight moves to a new target that is on screen, and that target is a GuiButton while a gamepad is in use, it sets `GuiService.SelectedObject` to it. This happens once per new target, so the player can move the selection off it.
- If the target isn't on screen yet, it waits until it is. Letter frames (not buttons) are skipped.

## Checks
- **Compile:** Hud, Guide, AutoRollController, AnvilController, CoinFly and Prefs all compile (each wrapped in a temporary ModuleScript, required in pcall, then destroyed).
- **Load:** CoinFly and Prefs load from fresh clones.

## Left / not touched
- Still moving with reduced motion, outside this fence:
  - AnvilController's strike ring pulse (line 1036)
  - TycoonController's buy bar glow (line 381)
  - the Guide ghost cursor's press and the confetti
  - the Shop icon's hop (already gated)
  - the Hud reputation badge pulse
  - TycoonController's build fly-in
  - OreBoxShow's ingot bob and pulse
- If the pad has never been used, the first spotlit button isn't selected when you pick up the pad later. It's only selected when the spotlight moves to a new target.
- Play test: turn Reduce motion on in Settings and sell a sword (the count jumps with no coins). Then polish (the number rolls with no coins). Then walk the tutorial with a pad: the spotlight jumps, the glow is steady, and A presses the spotlit button.

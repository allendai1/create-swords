---
title: UI Design
status: in progress
tags: [ui, figma, create-swords]
type: "art"
updated: "2026-10-22"
---

# UI Design

**Current inventory:** the chosen rarity-coloured hotbar has nine item slots plus a bag button, overflow, drag/drop and click/tap equip. Earlier square/translucent/ten-slot examples below are iteration history. See **Hotbar look, chosen** and **Backpack** for the latest build.

**Planned growth UI:** [[Design/Workshop Growth]] adds an employee management/upgrade window (hire, role, level, speed and applicable quality limits), a separate delivery board with pinned-order/crate/dispatch/return-payout states, and clear feedback for weather traffic bonuses. These screens are requirements to design, not UI recorded as implemented. Preserve the established picker behavior for player item selection and direct commission delivery.

Employee UI starts with five professions: furnace operator, smith, finisher, stocker and cashier; the 2026-10-22 direction adds an ore attendant as a later upgrade. Include paid training per sword shape after a personal first craft, covering permitted supplied materials without separate combination training; price and training ownership remain open. Show smith quality progression toward the confirmed 100% ceiling. Finisher controls include selected fittings, optional polishing and pause for player etching; finished-rack controls distinguish ready-for-sale stock from commission/delivery/further-finishing reservations. Stocker feedback should explain waiting for eligible stock or an empty holder. A separate hilter/polisher screen is not needed.

The game's screens are designed in Figma first, then rebuilt in Studio.

**Figma file:** [Sell Swords! UI](https://www.figma.com/design/rSuEIR8tY5vMayspRojWJ4) (Allen Dai's team, Drafts)

## Style

Follows [[Art/UI Concept - Furnace|UI Concept - Furnace]] (Allen's concept, built on *Create Pottery!*'s picker): warm dark chocolate, cream text, thin muted copper edge, big cards with a 3D item, one decision per window. No texture, no ornaments.

| Role | Value |
|---|---|
| Window | gradient `#3E281A` → `#301F14`, 2 px `#A86A3E` copper edge, 28 px corners (18 on phone), soft shadow. The world behind is blurred and dimmed (in Studio: a `BlurEffect` while open) |
| Title | station name, Fredoka Bold, `#FBEBD5` ("Forge") |
| Subtitle | the action, Nunito SemiBold, `#E9D6BF` ("Choose an ingot to heat.") |
| Close | ring: `#9A6E4E` circle, cream × |
| Card | gradient `#553928` → `#45301F`, 2 px `#7A5638` border, 20 px corners. Hover / gamepad focus: 3 px amber `#F2A93B` border + amber glow |
| Card content | 3D item (in Studio: a `ViewportFrame`), name in Fredoka SemiBold, a small chip, quantity "×4" top right |
| Chips (muted, colour + word) | Common `#6E5A4C`, Uncommon `#4F5E36`, Rare `#2F4E7A`; accuracy % chips use the Common colour; price and bonus `#7A5A1E`; locked `#3A2C22` |
| Heat | amber `#FFC24A` → `#F28A1F`; hot ingots get an amber glow on the anvil |
| Success | sage green: toast border `#7FA65A`, check `#5DBB46`, ready bar |
| Empty state | white line + orange hint `#F2A65A` |

**Fonts:** **Gotham** (Roblox's `GothamSSm`) everywhere in the game UI: Bold for titles, names, chips and the forge timer; Medium for subtitles and hints (Allen, 2026-10-18). The Figma file still uses Fredoka / Nunito, because Gotham isn't available in Figma; Montserrat is the closest stand-in there.

**Picker pattern:** every window where you put something into a station (forge, anvil, sword holder, Hilt Bench) looks the same: station name + action subtitle, close ring, then a grid of cards (2 across on desktop, one row on phone; scrolls when there are more). Same items stack with a quantity. Tap a card and the window closes and the station does its thing. No confirm buttons, no status panels. In Studio this is the one shared `ItemPicker` module.

**After picking (forge):** the window closes, the ingot glows in the fire, a toast says "Ingot loaded", and a billboard over the forge shows "Iron · Heating", an amber bar and the seconds left. When done it reads "Iron · Ready to collect" and the native Take out (E) prompt appears. If both slots are busy, E shows "Forge is full" instead of the window.

**Phone:** design at 844×390 landscape. Keep windows inside the safe area (below the 58 px Roblox top bar, 47 px in from each side for the notch) and tap targets at least 44 px.

## Components (in the Figma file)

- **Picker Card**: Size (Regular 270×250 / Compact 130×150) × State (Default / Hover). Properties: Name, Tag, Qty, Show Qty, Icon (swap)
- **Icons** (shaded, 3D look): Ingot (Top / Front / End), Sword (BladeL / BladeR / Guard / Grip / Pommel), Blade, Hilt. Blade colour = material, hilt parts = hilt type
- **Close Button** (ring)
- **Forge Timer (billboard)**: Heating (amber bar + "12s") / Ready (full green bar); Label and Time properties
- **Toast**: check + message ("Ingot loaded")

## Screens

Desktop (1920×1080) and phone landscape (844×390) for each, over the blurred plot concept art. Phone frames have a red safe-area guide layer; hide it before export.

| Screen | Status | Notes |
|---|---|---|
| Forge picker | Draft v4 | "Forge" / "Choose an ingot to heat.": Iron ×4 (hover), Copper ×2, Steel, Blue Steel |
| Forge picker, empty | Draft v4 | "No ingots yet" / "Roll one at the Ore Roller first." |
| Forge, after picking | Draft v4 (desktop) | Timer billboard + "Ingot loaded" toast over the plot |
| "Forge is full" message | Use the game's existing notice | Shown instead of the window when both slots are busy |
| Anvil pickers | Built in Studio | Step 1 "Choose a hot ingot to shape.": hot ingots glow amber. Step 2 "Choose a shape to make.": every blueprint as a black blade silhouette (true proportions, point up-right), chip = stars + price in the chosen metal. Not in Figma yet |
| Sword holder picker | Draft v4 | "Sword Holder" / "Choose a sword to display.": chip = price in coins |
| Hilt Bench pickers | Draft v4 | "Hilt Bench" / "Choose a blade." (chip = accuracy %), then "Choose a hilt." (chip = bonus; locked hilts dimmed with "Locked · 10 swords"). Then the seat-the-hilt taps |
| Offer card | To do | |

Allen checked the v4 screens on 2026-10-18.

## In Studio

Built on 2026-10-18 as the shared `ItemPicker` module ([[Development/Code Map|Code Map]]). Differences from Figma:
- The 3D items are simple parts in a `ViewportFrame` (an ingot is a block with two sloped sides; swords are flat bars), so they're plainer than the Figma art. Swap in meshes or images in the art pass.
- Fonts are Gotham (`GothamSSm`), not the Figma file's Fredoka / Nunito.
- Hot ingots on the anvil get a 30% orange tint so the metal still shows.
- The forge timer label isn't AlwaysOnTop (Studio's capture couldn't show it that way); it floats 4.6 studs up so it clears your head.
- Phone (under 500 px tall): one row of compact cards, centred below the Roblox top bar.

Related: [[Home]] · [[Design/Game Design Document|Game Design Document]] · [[Development/Code Map|Code Map]]

## Hotbar (2026-10-21)

Allen: "can you implement a custom toolbar that replaces roblox's default one. I'm thinking something like this. except the background is a translucent black, with 0 corner radius. a darker black border around it. if you have the same ingots, they should stack and say 2x, or 3x, or whatever it is." His reference was a row of cream rounded tiles (number top-left, count top-right, item, name) with a backpack button at the end.

- Built as `StarterPlayerScripts.Hotbar` in place of Roblox's bar:
  - Black slots at 0.45 transparency, square corners, a 2-px black border. The border turns light on the stack in hand.
  - Same layout as the reference, in Gotham Bold.
- **Stacks:** ingots of the same metal and heat share a slot (`2x`, `3x`); every sword has its own (`1x`).
- **Controls:** keys 1–9 and 0, a click or a tap equip; again puts it away.
- **At this early iteration:** the backpack button was absent. The later [[Art/UI Design#Backpack (2026-10-21)|Backpack]] section records its implementation. Gamepad cycling remains to confirm/complete.

![[References/hotbar-mock.jpg]]

*Mock in Edit with stand-in ingot icons; the real bar draws swords with their blade and hilt.*


### Hotbar halftones (2026-10-21, in testing)

Allen: "this website has halftones you can download and then import into studio and try https://ui-resources.com/". Six white-on-transparent halftones from its Halftones section were resized to at most 512 px, uploaded as Decals under user 14722022, and passed moderation. The site's Terms of Service page was a 404, so there's no stated licence; credit the creators if one ships.

| Name | Source (creator) | Decal | Image (use in ImageLabel) |
|---|---|---|---|
| corner | amz, White_Corner_Piece_Halftone | 125232234447028 | rbxassetid://77944995466851 |
| squares corner | amz, WHalf_Tone_7 | 84222578349197 | rbxassetid://91552993275825 |
| diagonal | angelz, Haldtonefromcentertotopleft | 110857914812892 | rbxassetid://100487902471709 |
| band | terry, Terry_Texture_2 | 81226516654110 | rbxassetid://116775024801046 |
| linear | sinister, halftone | 97661412300159 | rbxassetid://95235950580832 |
| long | LongWhiteCircle_Halftone | 115475022231464 | rbxassetid://136287015859304 |

The three corner and diagonal pieces are densest at their bottom-left; rotate −90° to put the dots in a slot's bottom-right. Clip with a CanvasGroup that has the slot's UICorner.

![[References/hotbar-halftone-assets.png]]

### Hotbar look, chosen (2026-10-21)

Allen first said the swords weren't clear, then asked for sizes, brighter renders, rounded corners, an opaque background, halftones, playful palettes and a black outline. Each was tried live in his playtest, side by side. Then: "Use rarity colours with a black 1px item outline and ink-black slot edges and text strokes, corner halftone, L size with hilt, 10px corners, bright lighting."

- **Slot:** 100 × 112, 10 px corners, a 3 px black edge (white on the stack in hand).
- **Background:** the item's rarity colour, from its metal: Common slate, Uncommon green, Rare blue, Epic purple, Legendary gold. Stone, copper and iron are all Common, so early on the bar is slate.
- **Halftone:** the "corner" halftone in the bottom-right at 72% transparency.
- **Text:** white Gotham Heavy with a black stroke.
- **Item:**
  - Lit white, with lighter metal.
  - A 1 px black rim; thicker lines swallowed the thin blades.
  - Swords drawn whole with the hilt and framed on their hilt-to-tip line, corner to corner.
- **Why not the rest:**
  - Blade-only lost the sword's identity.
  - Roblox's `Highlight` doesn't render inside viewports.
  - Black outlines of 1.5 px and more turned iron blades black.
  - Widening the blades made them look chunky.

Comparison sheets: `References/hotbar-size-options.jpg`, `hotbar-look-options*.{jpg,png}`, `hotbar-neon-outline.png`, `hotbar-background-options*.png`, `hotbar-halftone-assets*.png`, `hotbar-playful-palettes*.png`, `hotbar-rarity-black-outline*.png`.

![[References/hotbar-rarity-black-outline-2-zoom.png]]

*Top row is the chosen outline (black 1 px); the shipped slots also have the ink edges of the bottom row.*

### Backpack (2026-10-21)

Allen: "can you implement a backpack so when players have over 9 in their toolbar, they can drag things into the bag or they overfill into the bag. like in the screenshot i had sent before." The bag icon is his pick, `https://create.roblox.com/store/asset/15402958804` ("Backpack" by VectorIcons).

- **Bar:** 9 slots, keys 1–9. The 10th slot is the bag button in charcoal with the backpack icon, key `~`. It shows how many stacks are in the bag and gets a white edge while the bag is open.
- **Bag:** a charcoal panel above the bar, 10 slots wide, scrolling after 3 rows. Its slots look like the bar's but have no key number.
- **Overflow:** stacks past the ninth go straight into the bag.
- **Drag:**
  - Onto another slot to swap.
  - Onto the bag or its button to stash.
  - From the bag onto the bar, if there's room.
- **Equip:** click or tap any slot.

![[References/hotbar-bag-mock.jpg]]

*Mock in Edit with stand-in ingots; the live bar draws the real items.*

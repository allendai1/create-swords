---
title: UI Design
status: in progress
tags: [ui, figma, create-swords]
type: "art"
updated: "2026-10-24"
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
- **2026-10-26:** cards are square with a charcoal-to-black gradient; a bigger 3D item (184 px) with a thin white rim (gold until later that day) and lighter blades, the name below it, and the chip as a top-left tag; a chip every card shares is hidden (prices always show). The light pool tried earlier was removed. The picker windows have a tiled seigaiha (wave-scale) pattern under their brown at half strength (Allen's pick from wave and seigaiha boards). [[Sessions/2026-10-26#Brighter picker cards]]

**2026-10-22:** coins/reputation HUD and gem button use VectorIcons ([[Art/Icon Library]]); the Deliveries window follows Create Pottery!'s ([[Sessions/2026-10-22#Deliveries]]); a holder you can pick up from shows the bag icon ([[Sessions/2026-10-22#Pick-up marker]]). Earned coins pop up mid-screen and fly into the coin pill ([[Sessions/2026-10-22#Coins fly to the balance]]).

**2026-10-23, editable in Studio:** every screen everyone sees now lives in `StarterGui` (pickers, coins/reputation, hotbar and bag, Gem Shop and daily reward, collection book, Deliveries, reward card, guide, polish/etch/hilt-seat HUDs, the offer bubble), so it can be restyled in Studio's UI editor; repeated pieces are in each GUI's hidden `Templates` frame (turn its `Visible` on to edit them). In Edit only what a new player sees at join shows: the coins and reputation pills, the gem button and the book button. Map: [[Development/Code Map#Client controllers and interface]]. Polish applied with it:
- **Feel:** buttons and cards pop under the cursor or finger (1.04 hover, 0.94 held); windows rise 16 px as they open; things you can't do yet (locked cards, unaffordable Gem Shop and cart upgrades, Deliveries' Accept/Pack/Send while unavailable) get a dark veil and shake when tapped.
- **Phone (844×390):** windows scale to the screen but never below 0.7 (Deliveries was shrinking to 0.45), and long content scrolls instead; tap targets are at least 44 px. On touch the hotbar shows as many stacks as fit left of the jump button (6 + bag at 844×390); the rest sit at the front of the bag. The pinned delivery order moved off hotbar slot 1 into the left HUD stack.
- **Numbers:** amounts have thousands commas; a coin amount on its own shows the coin icon (the offer bubble's "$4514" is now coin + "4,514").
- **Type and colour:** Gotham (`GothamSSm`) everywhere, Bold for titles, names, chips and buttons, Medium for hints; close rings identical; toast green is the sage `#7FA65A`.
- **Controls:** Q and Backspace close a picker as well as gamepad B; D-pad left no longer opens the Gem Shop over another window.

**2026-10-23, HUD menu** ([[Sessions/2026-10-23#Refinements 2]]): the left edge is the reputation, coin and gem counters (gems no longer a button), then a 3-across grid of 44 px icon buttons in the counters' style, VectorIcons ([[Art/Icon Library]]): **Shop** (an empty Robux shop for now), **Charts** (the Gem Shop's store upgrades; the House icon since 2026-10-24), **gift** (daily reward, with the amber dot), **sword** (collection book), **crew** (the sword crafter's window, once hired) and **Settings** (Music and Sound switches). Shop and Settings windows match the Gem Shop. The Studio-only Dev panel sits bottom right behind a "Dev" button. This supersedes "the gem button and the book button" above.

**2026-10-23, mail, crew window, the HUD stepping aside** ([[Sessions/2026-10-23#Refinements 2, second list]]): a **Mail** button (Scroll icon) is first in the menu; its inbox is a Gem Shop-style window of rows (sender, New tag, the sword wanted, coin/gem reward, a green Hand in that is veiled and shakes when nothing fits) and a "New order in m:ss" row (removed 2026-10-24; an empty inbox now says "No mail"). The **crew window** follows Create Pottery!'s three screens: a roster of crafter cards (stars, role, name, trait, Quality and Forge Time bars with ▲/▼ against the one at work, price or Lvl + XP or a lock), a stats page (rows, portrait, XP bar) and "Where should <name> work?". While a station HUD or any window is up, the counters, menu, hotbar, guide line and pinned order hide and come back on close (`HudFocus`). The workshop racks show the shop holders' + and bag markers instead of Roblox's prompt box.

**2026-10-24, the left HUD is just icons** ([[Sessions/2026-10-24#Refinements 3]]): Allen: "Remove the background on left UIs so its just the icons." The menu buttons, the coin and gem counters and the pinned order have no plate or border; their numbers have a dark outline (2 px, RGB 43, 28, 19); icons are 38 px (were 30) in the 44 px buttons. A gamepad's selection still shows an amber edge. The Gem Shop button is the **House** icon ([[Art/Icon Library]]). The reputation (star/level) pill is hidden; reputation shows only as "Rank N" in the Deliveries header. The pinned order is off by default: **Pin** on the packing page or on the active order card turns it on for the session. It sits where the reputation pill was, and turns green "Ready!" when the cart is back (text only, no border). This supersedes the plates, the reputation pill and the Charts button above.

**2026-10-24, the delivery packing page:** Allen: "once i accept a delivery. it should show a page that i can then choose which swords to fill into the delivery. look at the clay game reference". Accepting an order opens the packing page in place of the Orders list, after Create Pottery!'s; the trip tracker stays below.
- **Top:** order chips (Bulk/Special, town, Pin), the pay, what it wants, "Tap swords to pack them".
- **Crate:** one slot per sword (64 px grid; up to 15 wrap onto two rows).
- **Your swords:** only the ones that fit, as compact cards (130×150): what the cart pays, art, name, metal chip. Cheapest first.
- **Buttons:** **Auto-Fill** (cheapest first, keeping your best for the shop), **Cancel Order**, **Fill the Crate** (veiled, and shakes, until every slot is full).
- Tap a card to pack it and a slot to take it back; a card shakes when the crate is full. On a gamepad the first card is selected. Half-packed crates from old saves show as locked full slots.
- **Known:** the Pin chip is 44 px tall, about 31 px on a phone (under the 44 px rule); the card prices can add up to 1 off the total (rounding; the total is the real pay); etched swords show no etch on their card art.

**2026-10-24, crew window tabs and staff pages:** with the four new employees ([[Design/Decisions Log#Refinements 3 — 2026-10-24]]) the crew window gets a **tab per hired role**, in a column off the window's left edge (shown from two tabs; the open tab outlined green). The window and its tabs stay centred together, so they fit screens from 660 px wide.
- **Staff page** (one per employee): the role as the title, portrait, name, Lv and XP bar (n / 5), Obtained, jobs done, the perk (Walk Speed, Answer Time, Walk-in Speed, Etch Time) and the live status line (amber while waiting).
- **Cashier setting:** a slider, "Sells offers of at least" / "value +10%", −20% to +50% in 5% steps, a mark at +0%. Drag, tap the bar, or d-pad left/right.
- **Etcher setting:** "Etches <pattern>" and a **Patterns** button. It opens a picker of katana cards, one per pattern; his current one has a green "Etching" chip.
- The crew button shows once anyone is hired. Its dot lights only when someone waits on you (the crafter out of ingots or rack space, the Etcher without a pattern or a free hook), not for a Stocker who's simply idle.

Related: [[Home]] · [[Design/Game Design Document|Game Design Document]] · [[Development/Code Map|Code Map]] · [[Art/Icon Library]]

## Hotbar (2026-10-21)

Allen: "can you implement a custom toolbar that replaces roblox's default one. I'm thinking something like this. except the background is a translucent black, with 0 corner radius. a darker black border around it. if you have the same ingots, they should stack and say 2x, or 3x, or whatever it is." His reference was a row of cream rounded tiles (number top-left, count top-right, item, name) with a backpack button at the end.

- Built as `StarterPlayerScripts.Hotbar` in place of Roblox's bar:
  - Black slots at 0.45 transparency, square corners, a 2-px black border. The border turns light on the stack in hand.
  - Same layout as the reference, in Gotham Bold.
- **Stacks:** ingots of the same metal and heat share a slot (`2x`, `3x`); every sword has its own (`1x`). Since 2026-10-24 there is no `1x`: the count shows only from 2x ([[Art/UI Design#Sword titles (2026-10-24)|Sword titles]]).
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
| from centre | `Art/halftonefromcenter.png` (added by Allen 2026-10-23) | — | rbxassetid://120711750535473 |
| quelly 2 | `Art/quelly2.png` (2026-10-23) | — | rbxassetid://88275800038595 |
| quelly 4 | `Art/quelly4.png` (2026-10-23) | — | rbxassetid://115124542347724 |
| quelly 5 | `Art/quelly5.png` (2026-10-23) | — | rbxassetid://95005144131326 |
| dense tile | generated, staggered dot tile for `ScaleType.Tile` (2026-10-23) | — | rbxassetid://106477061422613 |

The 2026-10-23 four were made white (alpha kept), shrunk to at most 512 px and uploaded as images through Studio. `Art/Terry_Texture_2.png` is the "band" above (already uploaded). Tried on the collection book's cards, `ScaleType.Crop` over the whole card, dark and white at 70% ([[Sessions/2026-10-23#Collection book: one ingot per metal]]).

The three corner and diagonal pieces are densest at their bottom-left; rotate −90° to put the dots in a slot's bottom-right. Clip with a CanvasGroup that has the slot's UICorner.

![[References/hotbar-halftone-assets.png]]

### Hotbar look, chosen (2026-10-21)

Allen first said the swords weren't clear, then asked for sizes, brighter renders, rounded corners, an opaque background, halftones, playful palettes and a black outline. Each was tried live in his playtest, side by side. Then: "Use rarity colours with a black 1px item outline and ink-black slot edges and text strokes, corner halftone, L size with hilt, 10px corners, bright lighting."

- **Slot:** 100 × 112, 10 px corners, a 3 px black edge (white on the stack in hand). Since 2026-10-26: 84 × 94, 8 px corners, a 2 px edge ([[Art/UI Design#Smaller hotbar (2026-10-26)|Smaller hotbar]]).
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

### Sword titles (2026-10-24)

From [[Refinements3]] ([[Sessions/2026-10-24#Refinements 3]]): a sword slot says the blade, with the metal small underneath (Allen chose "Metal, small"; his note broke off at "The type can be").
- **Title:** the blade's name ("Katana"), raised 11 px.
- **Metal line:** a small label at the slot's bottom (14 px tall, Gotham Bold, scaled 7–12 px, black stroke 1.5). It is tinted by the metal's rarity, lightened 45% toward white: the plain rarity colour almost vanished on a slot already filled with it.
- **Ingots** show the metal ("Hot Iron", "Rose Gold"; "Ingot" dropped 2026-10-26) in the title's old place, with no metal line.
- **Count:** only from 2x; a single item shows none.
- **Known:** the raised title overlaps the bottom 8 px of the art box (only the hilt or tip corner in the diagonal framing); not yet seen with real art.

### Smaller hotbar (2026-10-26)

Allen, on a phone: "the toolbars borders are too thick. the half-tones are only on a part of the entire box, also only 4 are on that actual toolbox. i want to be able to fit 6 in the toolbar including the backpack, so make them a bit smaller." [[Sessions/2026-10-26#Smaller hotbar]]

- **Slots:** 84 × 94 (were 100 × 112), everything inside scaled to 0.84, gap 13. Edges 2 px (were 3), on the slots, the bag button and the bag.
- **Halftone:** the "diagonal" one (`rbxassetid://100487902471709`) over the whole slot, densest bottom-right, still 72% transparent. The stretched "corner" one only reached half the slot.
- **Fit:** a phone shows 5 stacks + the bag at 812 × 375 and more on wider phones; desktop still 9 + the bag.
- **Why only 3 showed:** new stacks went into the bag whenever the bar's phone cap was low at that moment (at join), and stayed there. They now join the bar up to 9; any past the screen's room wait at the front of the bag, as designed.
- **Palette:** a new UI palette is open; three options went to Allen (A Bright forge, B Night forge, C Sky smith). Nothing changed yet.

### Left column sized in StarterGui (2026-10-26)

Allen: "Icons are a bit small right now on desktop", then "convert the left column to Scale + constraints in StarterGui and remove the runtime Grow". The coins, gems, menu and pinned order lanes are Scale of their lane (the screen under the top bar, at most 445 px, 0.6 as wide as tall), so Edit shows what a desktop player sees: 59 px menu buttons, 37 px coin, 26 px numbers. A 390 px-tall phone keeps the old 44 px buttons, 28 px coin and 20 px numbers. Icons are kept square by aspect constraints; numbers are `TextScaled` with a 10 to 27 px bound. Windows and pickers still use `Fit` + `UiFx.fit` at runtime. [[Sessions/2026-10-26#Bigger left HUD on desktop]]

### Staff rosters (2026-10-26)

Each staff tab in the crew window opens a roster like the crafters' (Allen: "make it so its like Crafters, where you can select your cashier or shop promoter"): the crafter card per member with portrait, role, name, level and XP, and the status line or perk where a crafter has its trait; no stars or bars. Tapping it opens the Staff page, which has a ‹ Back in the window header. [[Sessions/2026-10-26#Staff rosters in the crew window]]

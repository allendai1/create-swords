---
title: "QoL and Settings Ideas — 2026-10-31"
type: design
status: proposed
updated: 2026-10-31
tags: [design, qol, settings, accessibility, performance, audio, ui, create-swords]
---

# QoL and Settings Ideas — 2026-10-31

Allen, 2026-10-29 ([[Features and fixes]]): "also come up with more settings we can add for quality of life, or performance." Again on 2026-10-31 ([[Sessions/2026-10-31#Refinements, Allen's new notes and the big review (evening)]]): "more convenience features. more quality of life features. more granular settings controls."

**Nothing here is built or decided.** Sources: the live place, read in Edit without changes on 2026-10-31; this vault; the LihFolk vault; and the web (listed at the end). Each idea names the [[Design/Decisions Log]] ruling it touches. Every free convenience was checked against the Robux passes ([[Design/Monetization Plan]]) and the crew for "one system per effect".

Sizes: **S** = one or two scripts or one StarterGui piece, no new saved field. **M** = a new saved field, a server-checked action, or three or more scripts. **L** = a new system.

## Build next (top 10)

| # | Idea | Size | Why now |
|---|---|---|---|
| 1 | **Pickers open on what you'd pick:** your last-forged blade first, swords best first | S | The anvil lists every blade cheapest first. With all 24 learned, a phone (3 cards a row) puts the best ones in row 8, so you scroll for every sword |
| 2 | **Music for the Music switch** | S | The switch drives `SoundService.Music`, which is empty: the game has no music |
| 3 | **Volume per channel behind a gear on Sound:** Music, Effects, Alerts | S–M | Turning the anvil down also silences the offer ring. The on/off pills stay as they are |
| 4 | **Camera shake and Vibration switches** | S | The camera shakes on every strike, at the hilt seat and on Epic+ rolls. The hilt seat and rolls also vibrate |
| 5 | **Reduce motion**, which follows Roblox's own switch | S–M | No game script reads `GuiService.ReducedMotionEnabled`. The Shop icon hops every 5–9 s |
| 6 | **Lock items** | M | The bag's corner trash throws away a whole stack with no undo. Locks also answer "protecting special metals from the crafter", open since 2026-10-23 |
| 7 | **Fill at a shop holder** | S–M | A shelf takes 6 taps and the Upgraded Store has about 30 slots. The racks already have Store all |
| 8 | **Performance mode:** one switch, with details behind a gear | M | 70%+ of players are on phones, and six plots run effects at once. Measure on a phone first |
| 9 | **Pinned next goal** | M | Casual players wait over 15 min between buys 46 times ([[Development/Sim Runs/final-2026-10-30]]) |
| 10 | **Keep the tracker's fold and the cart's Pin between sessions** | S | Both reset every join. Allen asked for "an option to hide it too" |

Details: A1 (#1), A2 (#6), B1 (#7), A3 (#9), A4 (#10) and the settings in C (#2–5, #8).

## What exists now (live place, 2026-10-31)

### Settings and saved choices

| What | Where | Saved | What it does |
|---|---|---|---|
| Music on/off | Settings (top bar gear, TopbarPlus) | `settings.music` | Sets `SoundService.Music` to 0 or 1. **That group is empty: there is no music in the game** |
| Sound on/off | Settings | `settings.sound` | Sets `SoundService.Effects` to 0 or 1, which covers every sound in the game |
| Weather on/off | Settings | `settings.weather` | `WeatherController` drops the colour grade, rain, snow, rainbow and the rain loop. The bonus stays |
| Auto-Roll on/off | Auto-Roll bar (pass) | `settings.autoRoll` | Pulls the lever every ~5 s |
| Stop at rarity, Stop at quest ores | Auto-Roll window (its gear) | `autoKeep`, `autoQuest` | Uncommon+ … Legendary+, or none; and ores a letter or order needs |
| Cashier threshold | Crew page (slider) | staff record | Sells offers at or above the value plus a set %, from −20% to +50% in 5% steps |
| Etcher pattern, crafter shape or Random | Crew pages | staff and crafter records | |
| Quest tracker fold | The tracker's › | No: session only | |
| Delivery Pin | Deliveries | No: session only | Off by default |
| Hotbar and bag order | Drag | No: this client only, lost on rejoin | |

Roblox's own menu also has graphics quality, master volume, camera, Text Size, Reduce Motion and Background Transparency. The game reads none of them; only TopbarPlus does.

### How settings are saved

- `MenuController` fires `Remotes.Setting(name, value)`.
- SmithyCore accepts only whitelisted names:
  - the switches in `SWITCHES` (`Music`, `Sound`, `Weather`, `AutoRoll`, `AutoQuest`), each with a boolean;
  - `AutoKeep`, with one of `Store.KEEPS`.
- `allowCall` rate-limits the remote. The value goes into `d.settings`, is saved with the profile, and is mirrored as a player attribute, which the client displays.
- Defaults: everything on, except Auto-Roll (off) and its stop rarity (Rare).
- Window (`MenuGui.SettingsWindow`):
  - 416 wide with automatic height: 298 with today's three rows.
  - Rows are 360 × 68 and 14 apart: a 25 pt label and a knob pill (72 × 38, 2 px black outline).
  - The body has 28 / 20 / 28 padding.
  - On a phone, `UiFx.fit` scales it to about 0.7, so it is 291 px wide. It doesn't scroll.

### Sound

- **Two SoundGroups:** `Music`, which is empty, and `Effects`, which holds everything:
  - the rain loop (0.35) and the polish scrape (0.3);
  - 11 cues: `Offer`, `FurnaceReady`, `CartBack`, `Sale`, `Upgrade`, `HiltReveal` and five roll sounds;
  - three sword swings;
  - each anvil's `Clang` (0.6).
- **Not in the game:** UI clicks, voices (customers talk in bubbles), ambience apart from the rain, and `AudioPlayer` (the new audio API).
- **Three sounds call you somewhere:** `Offer`, `FurnaceReady` and `CartBack`. With Sound off they go silent too.

### Motion, effects and comfort

- **Camera shake** happens in three places:
  - every anvil strike (`AnvilController`, 0.15 s);
  - the hilt seat's punch (`HiltSeat`, harder for rarer metals);
  - Epic+ rolls (`OreBoxShow`, 0.25 s).
- **Haptics:**
  - the hilt seat's ticks and hit (`HapticEffect`, on phones and gamepads);
  - the gamepad rumble on Epic+ rolls.
- **Flashes** are lights on objects (ore lock-ins, the hilt guard, upgrade bursts), not full-screen flashes.
- **Particles made in code:** anvil, polish and etch sparks; hilt sparks; ore pops and light columns; upgrade confetti; rain and snow; crafter sparks (made on the server, so everyone sees them).
- **Idle loops:**
  - the Shop icon's rays turn once every 8 s, and the icon hops every 5–9 s;
  - every mirror-polished sword glints every few seconds, on every plot.
- **Lighting:** Bloom, SunRays, DepthOfField, Atmosphere and five colour grades, with GlobalShadows on.
- **Not handled:** nothing reads `ReducedMotionEnabled`, `PreferredTextSize` or `PreferredTransparency`, and nothing handles `Player.Idled`.

### Already covered (no work needed)

- **Store all** on the racks (2026-10-29).
- Held items go straight in: an ingot into the furnace, a sword onto a holder or a rack.
- **Auto-fill** at the cart.
- **Send** in the mail takes the one fitting sword, or offers a picker when several fit.
- The mail is already a history.
- You can leave the etch show early (the ring, Q, Backspace, B), and a press skips the hilt reveal.
- The Rank tip in Deliveries.

## Frictions in the flows

| Flow | Now | Friction |
|---|---|---|
| Store 6 ingots | 2 taps with empty hands (+ or E, then Store all). 3 taps if you're holding an ingot (E stores that one, then + and Store all) | Solved |
| Take 6 items off a rack | 6 taps, one per slot marker | No Take all |
| Collect 6 rolled ores | 6 presses: one prompt per stand, 8-stud reach, one prompt shown at a time | Fine while picking. A chore when feeding the crew |
| Forge your best blade late in the game | E, then an ingot card, then the blade picker: up to 24 shapes, cheapest first. On a phone, the Seraph is in row 7 and the Flamberge in row 8 | Every sword |
| Fill one shelf (3 swords) | 6 taps: hold the sword and tap the slot, or tap + and then a card. About 30 slots in the Upgraded Store | Until the Stocker |
| Choose a sword for a holder | The picker lists swords in inventory order, unsorted | Finding the best one |
| Trash a stack | Open the bag, arm the card's trash, set − N +, tap again: 3+ taps. Or drag the stack onto the corner trash: the whole stack goes, with no undo | No protection for rare items |
| Pack the cart | Walk to the bay (about 108 studs from Anvil 1, 6.8 s), then E, Accept, Auto-fill, Send: 4 taps. Later: walk back, E, Collect | Fine |
| Find a sword in the bag | A grid in an order kept on this client only, lost on rejoin, with no sort | Grows with every sword |
| Keep the tracker folded or an order pinned | Resets every join | Small, but every session |
| Answer an offer | Walk within 35 studs; 45 s to answer (VIPs 60 s); one ring | Intended: the walk between workshop and shop is the job |
| Go idle for 20 minutes | Roblox disconnects you without warning | The crew stops |

## How other games do it

- **Settings are short lists of switches:**
  - Grow a Garden has a cog top left with Sound Effects, Favorite Icons and Receive Gifts, plus a codes box ([1]).
  - Bee Swarm Simulator's System page has music on/off, Pollen Text, Abbreviate Pollen, Trade Requests and show/hide other players ([2]).
  - Pet Simulator 99 keeps its settings behind a gear in the Pets menu ([3]).
  - None of these lists per-channel sliders. LihFolk still ranks a music slider with a mute as the top small QoL win ("Top 25 QoL Wins by Effort").
- **Favourites protect items from bulk actions.** In Grow a Garden, Sell Inventory skips favourited fruit. You favourite with a long-press on a phone and a right-click on PC ([4], [5]).
- **Best-first defaults:** Pet Simulator 99 equips your best pets for you ([6]).
- **"Hide effects" requests come with lag:** Bee Swarm fans ask for a way to hide bees and particles to raise the frame rate (a speculative fan post, [7]).
- **Automation is what gets sold**, while sorting, picking and protecting items stay free. LihFolk: "Passes sell convenience, not power", and "pain-to-pay friction" is the dark pattern ("Ethical Design and Player Trust").
- **Not found:** no reliable source on Adopt Me's or Create Pottery!'s settings menus. Most game-specific pages are SEO guides, so read them as hints.
- **Roblox's guidance** ([8], [9], [10]):
  - Respect Text Size (`GuiService.PreferredTextSize`). `TextScaled` text ignores it, and the setting went global on 2025-08-27.
  - Respect Reduce Motion (`ReducedMotionEnabled`): use zero-time tweens or fades.
  - Respect Background Transparency (`PreferredTransparency`).
  - More than 5% of people are colour-blind, so pair colours with symbols.
  - Don't signal events by sound alone.
  - Let players set the volumes of sound effects, music and speech separately.
  - Follow the player's text and UI scaling.
- **Red-green colour blindness** is the most common kind, and more common in boys because it is X-linked ([11], [12]). Our players are 9–16.
- **Idle disconnects:** `Player.Idled` fires about 2 minutes after a player goes idle, then every 30 s, in client scripts only. "Roblox automatically disconnects players that have been idle for at least 20 minutes" ([13]).
- **Haptics:** `HapticEffect` has presets and custom waveforms, and runs on phones and controllers ([14]).
- **Graphics quality:** `UserGameSettings.SavedQualityLevel` can only be read on the client, and Automatic doesn't reveal the level ([15]). Roblox's own graphics slider already trades quality for speed ([16]), so don't rebuild it.

## A. Quality of life (friction removers)

★ marks a top-10 item.

| # | Idea | What it does | Serves | Where | Size | Ruling it touches |
|---|---|---|---|---|---|---|
| A1 ★1 | Pickers open on what you'd pick | The anvil's blade picker shows your last-forged blade first, then the rest by value, best first. Holder, polishing, etching and mail-send pickers list swords by value, best first. The ingot picker lists rarest first. The cart's Auto-fill stays cheapest first | Every forge late in the game, and finding the right sword | The existing pickers (`ItemPicker` callers) | S | Always open pickers (2026-10-19): the picker still opens and nothing is chosen for you. Auto-fill cheapest first (2026-10-24) stays |
| A2 ★6 | Lock items | While the bag is open, a lock sits top-right on each card (the trash is top-left). A locked card loses its trash and shows a small lock, on its hotbar slot too. The server enforces it: the trash refuses locked items (both kinds), Auto-fill and Fill skip them, and crafters skip locked ingots on the Ingot Rack. Displaying, sending or storing by tap still works. Setting: Lock Epic and up | A Legendary stack dragged onto the corner trash; a crafter using up your Dragonsteel; fast tapping | Bag cards; Settings → PLAY | M | Trash "never asks first" (Allen: "Never", 2026-10-27): a lock asks nothing. "Protecting special metals from the crafter stays open" (2026-10-23): this answers it |
| A3 ★9 | Pinned next goal | After the tutorial's cheer, a slim bar under the coins shows the next sword's icon and price and fills as coins come in. It turns green when you can afford it. Tap it and the guide's floor arrows point to its pad for 10 s. It hides while a window or station view is open, and Settings can turn it off | Casual players waiting over 15 min between buys 46 times; feeling "thrown in the game without knowing what to do" ([[Design/LihFolk Vault Review — 2026-10-30]]) | Left HUD column, in the old reputation pill's spot | M | Minimal UI text (2026-10-20): an icon, a bar and a number. One cue per thing (tutorial rules): no spotlight. The pacing note already lists "A pinned next goal" as the idea on the table |
| A4 ★10 | Keep the fold and the Pin | The tracker's fold and the cart's Pin are saved. A Quest tracker switch in Settings does the same as the fold | Both reset every join | Settings → PLAY; Deliveries | S | "There should be an option to hide it too" (2026-10-30). The pinned order stays off by default (2026-10-24) |
| A5 | Sort the bag | A button on the open bag's top-left corner sorts it best first: swords by value, ingots by rarity. The bar stays as you arranged it | Finding a sword among many | Bag panel | S | The bag's order is kept per client (2026-10-21) |
| A6 | Save the bar's order | The stacks in the bar come back in the same slots after a rejoin | Re-dragging every session | Hotbar (a saved field) | M | Order kept per client (2026-10-21) |
| A7 | Rarity marks | One to six small pips in a corner of hotbar slots and item cards (Common 1 … Secret 6) | Rare (Oklab L 0.70) and Epic (0.69) are blue and purple, which red-green colour-blind players confuse. Common (0.83) and Legendary (0.84) have the same lightness. The hotbar shows rarity by colour only | Hotbar, picker cards | S–M | Hotbar rarity sheen (2026-10-30): the colour stays. Minimal UI text: pips aren't words |
| A8 | Idle warning | Uses `Player.Idled`. After 17 min idle, the message bar says "Still there? Tap to stay" and the Alerts chime plays. Any input clears it | Kids who leave the crew working get disconnected at 20 min with no warning | The message bar (the tutorial's dark bar) | S | No ruling. Asks whether AFK crew play is wanted (LihFolk: AFK rewards are economy design) |
| A9 | Order popups switch | When off, mail orders don't pop up; the Mail dot and the tracker still show them. Story letters always pop up | Players who find the popups noisy | Settings → PLAY | S | Letters pop up middle right (2026-10-26) and time out (2026-10-30) |
| A10 | Hide HUD for a picture | A Settings button hides the HUD until your next tap | Showing off a shop; thumbnails | Settings | S | None |

## B. Free conveniences (checked against passes and crew)

| # | Idea | What it does | Could undercut | Verdict | Where | Size | Ruling it touches |
|---|---|---|---|---|---|---|---|
| B1 ★7 | Fill at a holder | Like the rack's Store all, the holder picker's first card reads "Fill ×N". It fills that holder's free cradles with your best fitting swords, skipping locked swords and any sword an open letter or order wants. It shows only when at least 2 cradles are free and at least 2 swords fit. The server checks each slot as `DisplaySword` does | The Stocker (crew, rack → holders) | Safe. Fill only uses your bag, while you stand at the holder. The Stocker serves the crafter's rack while you're elsewhere | Holder picker | S–M | Store all on the racks (Allen's request, 2026-10-29). A held sword goes straight on (2026-10-22). Pickers still open |
| B2 | Take all at the racks | The take picker's first card is "Take all ×N", which moves everything into your bag | Nothing | Safe | Rack take picker | S | Store and take stay separate (2026-10-23): this card sits in the take list |
| B3 | Collect all ore | When 2+ ores are waiting, a Collect all prompt on the roller (or holding on a stand) takes them all | The Auto Ore Roller, which only pulls the lever | Safe: you still collect ("Rolls only … it never collects; you do", Monetization Plan §5) | Ore roller | M | "Spin as often as you like" and a pull replaces waiting ore (2026-10-27): picking stays the default. Touch shows one prompt at a time (OneGlobally), so this needs a design |
| B4 | Keep forging | A setting, off by default: after a sword, if you still hold hot ingots, the anvil's ingot picker opens again. You can close it | Auto Anvil, Faster Strikes | Safe: it saves one E press, not any strikes | Anvil; Settings → PLAY | M | Always open pickers holds. Closing the anvil's picker leaves the anvil (2026-10-24) |
| B5 | Lock Epic and up | New Epic, Legendary and Secret items arrive locked (part of A2) | Nothing | Safe | Settings → PLAY | with A2 | — |

## C. Settings

### C1. The window on a phone

- **One window: one scrolling page with three sections**, like the Crew window (Allen, 2026-10-29: "one scrollable page with the sections"). No tabs.
- **Size:** `MenuGui.SettingsWindow` gets a fixed 416 × 440, which is 291 × 308 px on an 844 × 390 phone at 0.7. It sits at (0.5, 0, 0.5, 29) like Mail, clear of Roblox's top bar.
- **Body:** a vertical ScrollingFrame with a 4 px bar and the canvas sized by its list. About four and a half rows show on a phone.
- **Section headers:** SOUND, SCREEN and PLAY, in the Shop's GAME PASSES / CURRENCY header style, at 20 pt or more (at least 14 px on a phone).
- **Rows:**
  - 360 × 68 as now, which is 48 px tall on a phone.
  - Label on the left (Gotham Bold 25, cream, black outline), one control on the right.
  - Tapping anywhere on a pill's row flips it.
  - A row shows only once its feature exists: no dead switches.
- **Gears:** the Auto-Roll bar's gear, 46 × 46, sits left of the row's pill. It opens a small window cloned from `AutoRollConfig.Window`: the same frame, the title on the border and the red X.
- **Gamepad:**
  - every row is one selection stop;
  - A flips a pill;
  - left / right moves a selector or slider (D-pad and left stick);
  - B closes the window, as now.

```
┌─ Settings ───────────────────────[X]┐
│ SOUND ──────────────────────────────│
│ [ Music                      (  ●) ]│
│ [ Sound                ⚙     (  ●) ]│
│ SCREEN ─────────────────────────────│
│ [ Weather                    (  ●) ]│
│ [ Camera shake               (  ●) ]│
│ [ Reduce motion              (●  ) ]│  ← phone: scrolls from here
│ [ Performance mode     ⚙     (●  ) ]│
│ PLAY ───────────────────────────────│
│ [ Vibration                  (  ●) ]│
│ [ Quest tracker              (  ●) ]│
│ [ Next goal                  (  ●) ]│
│ [ Lock Epic and up           (  ●) ]│
│ [ Order popups               (  ●) ]│
└─────────────────────────────────────┘
```

### C2. The controls (all built from existing pieces)

| Control | For | Look |
|---|---|---|
| Knob pill | On / off | As now: a 72 × 38 capsule, no text. On: green 93,187,70 with the cream knob on the right. Off: dark 74,58,48 with the knob on the left. 2 px black outline (16,20,16) |
| Selector | 3–5 choices | The Auto-Roll window's < value >: 46 px dark arrows (corner 10, white outlined text) with the value between, placed inline on the right of the row |
| Slider | Volume | The Cashier's slider, restyled to match the pill. Track: a 190 × 16 capsule, dark 74,58,48, with the pill's 2 px black outline. A green fill runs up to the knob, which is the pill's cream 30 × 30 knob with a black outline. Steps: 0–100% in 10% steps. Input: tap or drag anywhere across the row's height; D-pad and left stick step 10% (the Cashier's slider only takes the D-pad). The number shows on the knob only while dragging. At 0 the label dims. The value sends 0.4 s after the last move (the Cashier's `SEND_AFTER`). Restyle the Cashier's slider the same way, so the game has one slider |
| Gear | A small settings window | The Auto-Roll bar's gear |

### C3. Rows in the main window

| Section | Row | Control | Default | What it does | Size | Ruling it touches |
|---|---|---|---|---|---|---|
| SOUND | Music ★2 | Pill | On | Turns the Music group on or off. Add 2–3 calm loops (Allen picks them from the Creator Store; Music slider at 70%), or hide the row until there is music | S | Music and Sound on/off, saved (2026-10-23) |
| SOUND | Sound ★3 | Pill + gear | On | Turns every sound except music on or off. The gear opens Volume (C4) | S–M | Allen picked on/off over volume sliders (2026-10-23): the pills stay, and the sliders sit behind a gear, as Auto-Roll's settings do (2026-10-28) |
| SCREEN | Weather | Pill | On | As now | — | Weather can be turned off; the bonus stays (2026-10-29) |
| SCREEN | Camera shake ★4 | Pill | On | When off: no shake at the anvil, the hilt seat or on Epic+ rolls | S | Ore rolls escalate (2026-10-29); the hilt seat hits harder (2026-10-30). On by default keeps both |
| SCREEN | Reduce motion ★5 | Pill | Follows Roblox's Reduce Motion | When on: shakes stop; the Shop icon stops hopping and its rays stop turning; windows fade in instead of rising (`UiFx.open`); coins that fly in become a quick fade, and the counter still counts up; the spotlight jumps instead of gliding. Once you flip it, your choice wins over Roblox's | S–M | Shop icon rays and hop (2026-10-29); coins fly into the value (2026-10-30). Both stay the default |
| SCREEN | Performance mode ★8 | Pill + gear | Off | Applies the Graphics preset (C4) | M | Follows the Weather switch's pattern (2026-10-29): changes only the look; every bonus stays |
| PLAY | Vibration ★4 | Pill | On | When off: no hilt-seat ticks or hit, no roll rumble. Shown only on touch and gamepad | S | Hilt seat haptics (2026-10-30) |
| PLAY | Quest tracker ★10 | Pill | On | Same as the tracker's fold, but saved | S | Mail tracker (2026-10-30, 2026-10-31) |
| PLAY | Next goal | Pill | On | Shows the next-goal bar (A3) | with A3 | — |
| PLAY | Lock Epic and up | Pill | On | B5 | with A2 | — |
| PLAY | Order popups | Pill | On | A9 | S | 2026-10-26, 2026-10-30 |
| PLAY | Keep forging | Pill | Off | B4 | with B4 | — |

Some settings stay where they are, because each belongs to its own system and lives in one place: the Auto-Roll stop rules, the Cashier threshold, the Etcher's pattern and the crafter's shape.

### C4. Behind the gears

**Volume** (the gear on the Sound row):

| Slider | Default | Covers |
|---|---|---|
| Music | 70% | The Music group |
| Effects | 100% | Anvil, polish, rolls, swings, hilt reveal, sale, the upgrade chime |
| Alerts | 100% | The three sounds that call you somewhere: `Offer`, `FurnaceReady`, `CartBack`. They move to a new `SoundService.Alerts` group; only their `SoundGroup` changes, not where they live, so every script still finds them |
| Weather (only if more ambience comes) | 100% | The rain loop. Today the Weather switch covers it |

- **Groups sit side by side, not nested,** so Effects at 0 still leaves Alerts audible. The Sound pill sets all of them to 0, or back to their slider values.
- **Volume curve:** volume = position², which sounds even (LihFolk "Audio Mixer Settings with SoundGroups"). A group's volume never goes above 1.
- **Left out on purpose:**
  - UI click sounds or voices added just to fill a slider;
  - a master slider (Roblox's own volume is the master).

**Graphics** (the gear on the Performance mode row):

| Row | Control | Normal | Performance mode |
|---|---|---|---|
| Effects | < Full · Less · Off > | Full | Less |
| Other shops' effects | Pill | On | Off |
| Sword shine | Pill | On | Off |
| Sun rays and blur | Pill | On | Off |

- **Effects:** every particle `Emit` and rate goes through one scale: anvil, polish, etch, hilt, ore pops and light columns, confetti, rain and snow, crafter sparks.
  - Less is about 35% (LihFolk sample value).
  - Off means no particles.
  - Lights, sounds and every number stay.
- **Other shops' effects:** other plots' roll sparks and light columns, upgrade bursts and crafter sparks.
- **Sword shine:** the glint loop on every mirror-polished sword, on every plot.
- **Sun rays and blur:** turns off Lighting's SunRays and DepthOfField on this client only. Bloom stays, because the etches are made to bloom.
- **Custom:** changing any row turns Performance mode off. Roblox's own graphics slider stays Roblox's.
- **Measure first** (thin evidence: no phone measurements exist yet; published-device checks are still open in the [[Development/Roadmap]]):
  - Record frame time and memory on a low-end Android and an older iPhone with all six plots in use.
  - Keep only the rows that move those numbers.

### C5. Saving

- **Same path as today:** `Remotes.Setting(name, value)` → SmithyCore's whitelist → `d.settings` (saved) → a player attribute → the client. No new remote.
- **Booleans** join `SWITCHES`: `Shake`, `Vibration`, `Performance`, `Tracker`, `CartPin`, `NextGoal`, `AutoLock`, `Popups`, `KeepForging`.
- **Reduce motion has three states:** nil follows Roblox's switch; true or false once the player has chosen.
- **`Effects`** must be one of Full, Less or Off.
- **Volumes** are numbers: refused unless finite, then clamped to 0–1 and rounded to 0.1.
- **Timing:** the client applies a change at once, during a drag too, and sends it 0.4 s after the last move. `allowCall` still rate-limits it.
- **Skills:** load `roblox-data`, `roblox-networking` and `roblox-security` when building this (CLAUDE.md routing).
- **No migration needed:** there are no live players.

### C6. Accessibility audit (not settings)

- **Roblox's Text Size:** the `TextScaled` labels (tracker rows, pad labels) ignore it. Check that windows with fixed `TextSize` don't overflow at Largest.
- **Sound alone:** the offer ring always comes with the card over the customer, but only within 35 studs. If a player has sound off, the card over the customer is the only cue. Keep that rule in mind for any future alert.

## Avoid

- **A "confirm before trashing" step.** Allen: "Never" (2026-10-27). The lock (A2) protects instead.
- **Auto-accepting offers over a %.** That's the Cashier's job (2026-10-24). One system per effect: Monetization Plan §8 already left out an Auto Cashier.
- **Filling every holder from anywhere, or auto-display.** That's the Stocker's job.
- **Answering offers from anywhere, or showing offer prices on the HUD.** The walk between workshop and shop is the job ([[Archive/Design/Urgency Review]]: "you can miss gains, but never lose what you have"). Allen also removed the coin ping over far customers (2026-10-23).
- **A free auto-roll or hold-to-roll.** That's the Auto Ore Roller pass.
- **Hold-to-strike or a free auto-strike.** Allen turned down hold-to-strike (2026-10-30), and Auto Anvil is a pass (2026-10-31).
- **A run toggle or a Home teleport.**
  - Swift Boots sells walking speed.
  - Roblox's Reset already respawns you at your plot.
  - The town is small.
- **Free skips of heat or cart timers.** They compete with Faster Heating and the cart's Speed (Monetization Plan §8: "Instant heat").
- **Auto-collecting the cart's pay.** GDD §9.1 has the payout collected at the station (confirmed 2026-10-19). Ask before changing it.
- **A UI size slider.** UI sizes live in StarterGui with no runtime resizing (Allen asked twice). Honour Roblox's Text Size instead (C6).
- **Rebuilding Roblox's own settings:** graphics quality, master volume, camera sensitivity. LihFolk: "Read, do not replace".
- **A missed-notifications log.** The mail already keeps a history: New, Sent, Declined.
- **"Saved!" toasts after a setting change.** The switch moving already shows it (minimal UI text).
- **Volume sliders in the main window.** Allen picked on/off (2026-10-23).
- **A per-section reset, a settings search or a master slider.** Not needed at this size. Add them if the list ever grows past one screen per section.

## Questions for Allen

1. **Music:** add 2–3 calm loops (you pick them), or hide the Music row until there is music?
2. **Volume sliders behind the Sound gear:** build them, or keep only on/off (your 2026-10-23 pick)? Three channels, or four with Weather?
3. **Locks:**
   - Should crafters skip locked ingots on the Ingot Rack? That answers the "protect special metals" question.
   - Should Lock Epic and up be on by default?
4. **Next goal:** show only the next sword, or the next spine goal (the Sword Crafter when it's next)? Is under the coins the right spot?
5. **AFK:** do you want players to leave the crew working? If yes, build the idle warning (A8); if no, skip it.
6. **Rarity pips:** always on, or a setting?
7. **Performance mode:** only in Settings, or switched on once for slow phones?
8. **Collect all ore:** is it worth a second prompt at the roller, given that picking ore is the point?

## Sources

**Live place (read only, 2026-10-31):**
- `MenuController`, `SmithyCore` (the `Setting` handler and `settings`);
- `StarterGui.MenuGui.SettingsWindow`, `AutoRollConfig`, `CrewGui.Window.Staff.Setting` (the Cashier's slider);
- `SoundService` (groups and sounds);
- `RackController` (Store all), `ShopController` (holder picker), `AnvilController` (pickers, shake), `ItemPicker` (phone layout), `Hotbar` (bag, trash, order);
- `ForgeService` (collect prompts), `HiltSeat`, `OreBoxShow`, `SwordRenderer`, `EtchingTableController`, `Guide`, `Lighting`.

**This vault:** [[Design/Decisions Log]], [[Design/Game Design Document]], [[Development/Code Map]], [[Design/Monetization Plan]], [[Archive/Design/Urgency Review]], [[Design/LihFolk Vault Review — 2026-10-30]], [[Sessions/2026-10-29]], [[Sessions/2026-10-30]], [[Sessions/2026-10-31]], [[Features and fixes]].

**LihFolk vault** (folders 58 Player QoL and Game Tweaks, 42 Accessibility and Inclusive Design, 05 UI and UX). Most numbers in these notes are rules of thumb.
- QoL and inventory: Top 25 QoL Wins by Effort; Inventory QoL - Sort Filter Search Stack and Lock; Confirmation and Undo Patterns for Destructive and Paid Actions; AFK Detection Idle Kicks and AFK Reward Rules; Notification Queues and Limits.
- Settings, audio and graphics: Settings Menu Essentials and Persistence; Settings Menu Design for Roblox - Layout, Controls and Motion; Audio Mixer Settings with SoundGroups; Graphics and Performance Toggles for Low-End Devices; UI Scale HUD Hide and Compact Mode; Controller Support QoL.
- Accessibility: Colour-Blind Safe Design; Readable Text and UI Scale; Accessibility; Motion Sensitivity and Camera Comfort.
- Monetization ethics: Ethical Design and Player Trust.

**Web:**
1. Grow a Garden's settings menu: https://backyarddrunkard.com/games/roblox-grow-a-garden-codes/
2. Bee Swarm Simulator System Page (read through a search summary; the page itself refused the fetch): https://bee-swarm-simulator.fandom.com/wiki/System_Page
3. Pet Simulator 99 keybinds and settings gear: https://www.ginx.tv/en/pet-sim-99-keybinds
4. Grow a Garden favourites: https://allthings.how/how-to-unfavorite-fruits-and-crops-in-grow-a-garden/
5. Grow a Garden 2's Sell Inventory skips favourites: https://nerdschalk.com/grow-a-garden-2-roblox-how-to-sell-your-inventory-bulk-selling-protecting-favorites-and-crop-value-guide/
6. Pet Simulator 99 auto-equips your best pets: https://www.videogameschronicle.com/guide/pet-simulator-99-unequip-pets/
7. Bee Swarm QoL wishes (speculative): https://roonby.com/2026/09/02/bee-swarm-simulator-qol-update-guide-what-is-coming/
8. Roblox accessibility guidelines: https://create.roblox.com/docs/production/publishing/accessibility
9. Roblox adaptive design guidelines: https://create.roblox.com/docs/production/publishing/adaptive-design
10. Roblox's global Text Size (2025-08-27): https://caniplaythat.com/2025/08/27/roblox-introduces-global-text-size-accessibility-setting/
11. NEI, types of colour vision deficiency: https://www.nei.nih.gov/eye-health-information/eye-conditions-and-diseases/color-blindness/types-color-vision-deficiency
12. NEI, causes: https://www.nei.nih.gov/eye-health-information/eye-conditions-and-diseases/color-blindness/causes-color-vision-deficiency
13. `Player.Idled` and the 20-minute disconnect: https://create.roblox.com/docs/reference/engine/classes/Player
14. `HapticEffect`: https://create.roblox.com/docs/reference/engine/classes/HapticEffect
15. `SavedQualitySetting`: https://create.roblox.com/docs/reference/engine/enums/SavedQualitySetting
16. Roblox Help, graphics quality: https://en.help.roblox.com/hc/en-us/articles/203314310

Related: [[Design/Refinements Proposals — 2026-10-30]] · [[Design/Monetization Ideas — 2026-10-31]] (the parallel brainstorm) · [[Development/Roadmap]]

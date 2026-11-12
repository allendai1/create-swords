---
tags: [design, thumbnails, packaging, create-swords]
---

# Thumbnail Concepts — 2026-11-08

Allen's raw list is [[thumbnail ideas]]. This note turns each idea into an image-generator prompt and says which ones can be staged in Studio first. Prompts rewritten 2026-11-08 (Allen: "can you help re-write the prompts"): one self-contained block per shot, matched to what the Studio references show.

## Rules for every thumbnail

- **One idea, 1–2 subjects.** It has to read at phone size (about 400×225). Check it at that size before uploading.
- **Show only what is in the game.** Since June 2026 Roblox tracks First-Play Bounce Rate, so a thumbnail that promises something the first minutes don't deliver costs ranking.
- **No text in the prompt.** Generators garble letters. Add numbers and words afterwards (the Blood Crow title is already set up in `Models/Thumbnail/Thumbnail.blend`). At most 3 words or one number per side.
- **No anime characters** and none of the one-letter-off names (Zaro, Tenjiro…). Visitors in thumbnails are original: a knight, a pirate, a samurai warlord.
- **Give the generator a Studio capture as the image reference** where one exists, so it copies our real anvil, shop and Taru instead of inventing them.
- Size 1920×1080, 16:9. Upload 2–5 at once so Roblox's thumbnail personalization finds the winner.

## How to use the prompts

Written for **Codex with ChatGPT's image generation** (Allen, 2026-11-08: "codex already has access to our vault, so include where the images are in the prompt"). Paths are from the vault root.

1. Paste one whole block into Codex. It names its reference images by vault path and where to save the result, in `Art/Thumbnail/Generated/` (v1, v2…; nothing is overwritten).
2. Fix it in the same Codex thread, one thing at a time, and say what stays: "Keep everything the same, only make the sparks bigger. Save as v2." A new full prompt makes it redraw everything.
3. If it comes back 3:2 instead of 16:9, crop the top and bottom; keep heads and swords out of the top and bottom tenth.
4. If it drifts from the reference (a different mask, a grey anvil), reply "Look at the reference image again and match it more closely: the same mask, the blue anvil."
5. The image model draws text well, but the title and numbers still go on afterwards in Blender, so every thumbnail uses the same Blood Crow lettering.

What the game looks like, for any prompt you write yourself: a **chunky blue cartoon anvil**, a gravel smithy yard, a **white plaster Japanese building with dark timber beams and a terracotta roof**, **pink brick furnaces**, pink cherry trees, green trees, a painted blue sky with big white clouds. The crafters wear a **pink-faced hyottoko mask with round eyes and a white headscarf**.

## Staging map (Studio)

`Workspace.ThumbnailStaging` (2026-11-08, Allen: "create a staging map that i can edit myself and move them around", then "also create the store so i can move my camera around. and fill the racks and tables with actual good looking swords"):

- **`UpgradedShop (lot N1)`**: a fully upgraded copy of the plot on the empty lot N1 (left of the template plot, same street), built from the template as the game builds it: every upgrade bought (the Starter Shop and the strip's paving gone), the Upgraded Store's 12-stud push applied, pads, spawns, prompts and scripts stripped. Walk the Studio camera through the door; it has its ceiling and the real village around it.
- **Every display filled** (39 swords, mirror-polished, each a different blueprint/metal, Gold or Gem hilts), seated on the cradles as ShopService does: wall racks 1–5 (katana Gold/Sapphire, wakizashi Ruby; longsword Silver, rapier Mythril, cutlass Rose Gold; jian Jade, dadao Obsidian, hook sword Amethyst; katana Obsidian, katana Damascus, katana Sapphire (WallRack4, swapped 2026-11-10 for contrast); Crescent Fang Ice, Moonbite Starmetal, Serpent Emerald), display tables 1–6 (katana Mythril, tantō Ruby, wakizashi Gold; Thornspire Bloodmoon, Seraph Sunsteel, Shard Blade Diamond; Leviathan Dragonsteel, Serpent Raijin, Crescent Fang Soulfire; longsword Rainbow Alloy, rapier Prism, gladius Doppler; katana Oni Steel, jian Infernal, dadao Runestone; machete Magma Steel, falchion Blue Steel, scimitar Air), big stands (Zanbatō Magma Steel, claymore Dragonsteel, flamberge Sunsteel), showcases (Seraph Diamond, Leviathan Infernal, katana Rainbow Alloy). Each holder's swords are in its `Swords` folder; move, delete or duplicate them freely.
- **The workshop Sword Rack filled too** (Allen: "can you fill the sword rack with expensive swords too"; `Smithy.SwordRack.Swords`), hung as RackService hangs them (Handle at the hook; a big sword between two hooks): Seraph Mythril, Thornspire Sunsteel, Leviathan Diamond, Serpent Prism, flamberge Diamond (hooks 5–6), Moonbite Doppler, Shard Blade Rainbow Alloy, Crescent Fang Bloodmoon, Hook Sword Oni Steel, claymore Soulfire (hooks 11–12). Shot: `Art/Thumbnail/Staging/Sword rack full.jpg`.
- **The cast**, one anchored model each, lined up in that copy's yard (x 498–562, z −316 and −309), to drag into the shop or anywhere:

  - **Posed:** Taru (flexing), Taise (holding tantō), Swordsmith (hammer up), Bacon Hair cashier (shocked), Rengoku (walking in).
  - **Props:** cashier counter, Zanbatō (Magma Steel), tantō (Iron), katana (Silver, polished).
  - **Standing:** all 12 named characters as the shop spawns them (Zoro … Zenitsu).
- Drag a whole model (click it in the Explorer, or select it in the viewport). Ctrl+D duplicates one. The poses are fixed; ask Claude for a new pose.
- **Taru needs his joints.** His hakama is layered clothing, which wraps to the body through the rig: with the joints deleted it renders broken (a floating torso, the hakama as shorts), sometimes only after a while or from some distances. His rigs keep Motor6D joints (the pose baked into their C0), with attachments and the AnimationConstraints Studio draws removed.
- `ServerScriptService.ThumbnailStagingCleanup` deletes the folder when the game runs, so nothing in it reaches Play or live servers. The shop copy adds about 3,600 parts to the place file, so delete the folder once the thumbnails are done.
- For a screenshot: frame the Studio camera, hide the Explorer selection (click empty sky), then the Studio screenshot button or Win+Shift+S; save it in the concept's folder under `Art/Thumbnail/`.

## The concepts

| # | Concept | Format | Best made in |
|---|---|---|---|
| 1 | Three swords: tantō, katana, mystery | before & after (×3) | Composite from existing renders |
| 2 | Hot ingot → legendary sword | before & after | Studio stage → generator |
| 3 | Taru, the muscle crafter | one character / vs | **Staged** → generator |
| 4 | Cozy forging close-up | one subject + action | **Staged** → generator |
| 5 | Behind the counter | two-character scene | 5c **staged** → generator |
| 6 | First person: packing a crate | first person | Generator only |
| 7 | Silhouette collection + title | new concept | Composite from existing renders |

### 1. Three swords: tantō, katana, mystery

Like the pug / shark / magpie reference: three panels, value going up left to right, the last one hidden. Best made as a composite: `Art/Thumbnail/Swords/` has the Tantō, `Katana - Gold.png` and `Butter Stick - Gold.png` (fill it black for the silhouette). The prompt is a fallback.

```text
Create a wide 16:9 landscape image.
Reference images in the vault, one per sword: `Art/Thumbnail/Swords/Steel/Tantō - Steel.png` (left), `Art/Thumbnail/Swords/Metals/Katana - Gold.png` (middle), `Art/Thumbnail/Swords/Metals/Butter Stick - Gold.png` (right, drawn only as a solid black silhouette). Keep each sword's shape and hilt as in its image.
Three tall vertical panels side by side, separated by two thick white slanted bars.
Left panel, flat grey background: a small plain steel tantō with a simple wrapped handle, standing blade up, centred.
Middle panel, glowing royal-blue background: a gleaming gold katana with a navy wrapped hilt and gold guard, standing blade up, a sharp white glint along the edge.
Right panel, deep purple background with radiating light rays: a solid black silhouette of a strange sword, a thick rectangular block on a katana hilt, with a huge glossy red 3D question mark in front of it.
Each sword fills its panel from top to bottom, bright rim light on each.
Style: Roblox game thumbnail, glossy stylized 3D render, saturated colours, clean edges. No text, letters, logos or watermark. Keep the Roblox look: blocky characters and simple shapes, not a realistic or Pixar-style render.
Save the image as `Art/Thumbnail/Generated/1 Three swords v1.png` (v2, v3 for later tries; never overwrite).
```

- The mystery is the **Butter Stick**: a block on a hilt is strange enough to click on and honest (it's a real secret sword).

### 2. Hot ingot → legendary sword

Like the hammer → +1T sword reference. Not staged yet; this prompt works without a reference.

```text
Create a wide 16:9 landscape image.
Reference images in the vault: the anvil and the yard in `Art/Thumbnail/Concept 4 - Forging close-up/Studio ref A - sword on anvil.png`; the greatsword is `Art/Thumbnail/Swords/Metals/Zanbatō - Magma Steel.png` (keep its shape, cracks and navy wrapped hilt).
Two halves split by a thick white diagonal bar.
Left half: a grinning blocky Roblox avatar mid-swing brings a steel hand hammer down onto a glowing orange-hot metal bar lying on a chunky blue cartoon anvil, bright sparks bursting from the hit. Behind: a gravel smithy yard, a white plaster Japanese building with dark timber beams, blue sky.
Right half: an enormous straight single-edged greatsword floating upright, black blade with glowing orange lava cracks, dark wrapped hilt, swirling gold energy rings and sparkles around it, light rays behind.
A thick glossy red curved arrow arcs from the hot bar on the left to the sword on the right.
Leave empty sky at the top of each half.
Style: Roblox game thumbnail, glossy stylized 3D render, blocky Roblox characters, saturated colours, bright daylight, clean edges. No text, letters, logos or watermark. Keep the Roblox look: blocky characters and simple shapes, not a realistic or Pixar-style render.
Save the image as `Art/Thumbnail/Generated/2 Ingot to sword v1.png` (v2, v3 for later tries; never overwrite).
```

- Text afterwards: the real sale price of a starter sword on the left, of a Zanbatō on the right (not made-up numbers).

### 3. Taru, the muscle crafter

**3a hero.** Reference `Art/Thumbnail/Concept 3 - Taru/Studio ref 3a - Taru hero.png`:

```text
Create a wide 16:9 landscape image.
Reference image in the vault: `Art/Thumbnail/Concept 3 - Taru/Studio ref 3a - Taru hero.png`. Use it for the character, the sword and the layout.
Keep the character exactly: a blocky Roblox swordsmith in a pink-faced hyottoko mask with round eyes and a white headscarf, bare muscular chest, black hakama with a white waist tie, barefoot. Keep the giant black greatsword with glowing orange lava cracks planted tip-down in the ground beside him.
Make his muscles huge and cartoon-exaggerated, flexing both biceps, chest puffed out.
Camera low, looking up at him so he towers over the frame.
Background: bright blue sky with big white clouds, the white Japanese building and pink cherry trees, softly blurred.
Warm sunlight with a golden rim light on his shoulders and arms, small sparkles along the sword.
Style: Roblox game thumbnail, glossy stylized 3D render, saturated colours, clean edges. No text, letters, logos or watermark. Keep the Roblox look: blocky characters and simple shapes, not a realistic or Pixar-style render.
Save the image as `Art/Thumbnail/Generated/3a Taru hero v1.png` (v2, v3 for later tries; never overwrite).
```

**3b vs.** Reference `Art/Thumbnail/Concept 3 - Taru/Studio ref 3b - Taise vs Taru.png`:

```text
Create a wide 16:9 landscape image.
Reference image in the vault: `Art/Thumbnail/Concept 3 - Taru/Studio ref 3b - Taise vs Taru.png`. Use it for both characters and the sword.
Split the image into two halves with a thick white diagonal bar.
Left half, dull grey-blue background: the smaller swordsmith from the reference (same hyottoko mask and white headscarf, olive kimono, dark hakama), skinny and hunched, nervously holding a tiny plain knife, a big sweat drop beside his mask.
Right half, bright orange-gold background with light rays: the huge muscular swordsmith from the reference (same mask, bare chest, black hakama, barefoot) flexing both biceps, the giant black lava-cracked greatsword planted beside him, glowing orange.
The right figure is clearly bigger than the left one.
Leave space at the top of each half.
Style: Roblox game thumbnail, glossy stylized 3D render, saturated colours, clean edges. No text, letters, logos or watermark. Keep the Roblox look: blocky characters and simple shapes, not a realistic or Pixar-style render.
Save the image as `Art/Thumbnail/Generated/3b Taise vs Taru v1.png` (v2, v3 for later tries; never overwrite).
```

**3c side by side, standing** (Allen: "can you set up a shot of taise and taru next to each other. no poses, just standing"): `Art/Thumbnail/Concept 3 - Taru/Studio ref 3c - Taise and Taru standing.png` (close, on the street in front of the staging shop) and `… standing, wide.png` (with the Swordsmith sign and the shop front). In the staging map as `Standing/Taru (standing)` and `Standing/Taise (standing)`.

- Text afterwards on 3b: "Lv. 1" / "Lv. 5" (crafters really level to 5).
- Both crafters wear the same mask (Taise since 2026-11-06), so the contrast is body and sword, not face.
- References (Edit, 16:9): 3a low angle, Taru in a double-biceps flex, the Magma Steel Zanbatō planted beside him; 3b Taise (the first crafter) hunched with a plain iron tantō next to Taru. The stage is kept in `ServerStorage.ThumbnailStages.Concept3_Taru` (cameras in its Note attribute); the rigs are anchored with their joints removed, so rebuild them to change a pose.

### 4. Cozy forging close-up

Like the two Create Pottery! wheel shots: one without a character, one with.

**4A sword on the anvil.** Reference `Art/Thumbnail/Concept 4 - Forging close-up/Studio ref A - sword on anvil.png`:

```text
Create a wide 16:9 landscape image.
Reference image in the vault: `Art/Thumbnail/Concept 4 - Forging close-up/Studio ref A - sword on anvil.png`. Use it for the anvil, the katana and the layout.
Keep the chunky blue cartoon anvil and the katana lying across it: silver blade, red wrapped hilt, gold flower-shaped guard.
Make it a cozy, bright close-up: camera a little closer and lower, the katana filling the middle of the frame.
The blade tip glows orange-hot with a few small sparks, and a sharp white glint runs along the edge.
Background: the white Japanese building, green trees and pink cherry blossoms, strongly blurred (shallow depth of field).
Warm late-afternoon sunlight from the left, soft shadows.
Style: Roblox game thumbnail, glossy stylized 3D render, saturated colours, clean edges. No text, letters, logos or watermark. Keep the Roblox look: blocky characters and simple shapes, not a realistic or Pixar-style render.
Save the image as `Art/Thumbnail/Generated/4A Sword on anvil v1.png` (v2, v3 for later tries; never overwrite).
```

**4B crafter at the anvil.** Reference `Art/Thumbnail/Concept 4 - Forging close-up/Studio ref B - crafter at anvil.png`:

```text
Create a wide 16:9 landscape image.
Reference image in the vault: `Art/Thumbnail/Concept 4 - Forging close-up/Studio ref B - crafter at anvil.png`. Use it for the character, the anvil, the katana and the layout.
Keep the blocky Roblox swordsmith: pink-faced hyottoko mask with round eyes, white headscarf, grey kimono with a pale star pattern, grey sash.
He brings the small hand hammer down onto the katana on the chunky blue anvil; a bright burst of orange sparks flies from the strike, and the blade glows orange where it is hit.
Keep the wooden water tub and the hammer stump in the front corners.
Background: pink brick furnaces, the white Japanese building and cherry trees, softly blurred.
Bright warm daylight.
Style: Roblox game thumbnail, glossy stylized 3D render, saturated colours, clean edges. No text, letters, logos or watermark. Keep the Roblox look: blocky characters and simple shapes, not a realistic or Pixar-style render.
Save the image as `Art/Thumbnail/Generated/4B Crafter at anvil v1.png` (v2, v3 for later tries; never overwrite).
```

- References (Edit, 16:9): A the polished Silver katana prop on the yard anvil, flat to the camera; B the Swordsmith crafter behind the anvil with a hand hammer raised. The stage is kept in `ServerStorage.ThumbnailStages.Concept4_ForgingCloseUp` (both cameras in its Note attribute, FOV 40); the blade is the baked `B|katana|2` mesh, coloured as SwordRenderer does.

### 5. Behind the counter

Not staged yet; these prompts work without a reference.

**5a cashier's view:**

```text
Create a wide 16:9 landscape image.
Reference image in the vault for the katana on the counter: `Art/Thumbnail/Swords/Metals/Katana - Gold.png`.
Eye-level view from behind the wooden counter of a Japanese sword shop.
In the foreground on the counter: a katana on a small stand and a tray of gold coins.
Across the counter, a blocky Roblox knight in shiny silver full armour leans in, visor up, smug grin, holding up a fat sack of gold coins.
A huge glossy red 3D question mark floats above his head.
Behind him: wall racks of swords, white plaster walls with dark timber beams, a bright open doorway.
Style: Roblox game thumbnail, glossy stylized 3D render, blocky Roblox characters, saturated colours, bright daylight, clean edges. No text, letters, logos or watermark. Keep the Roblox look: blocky characters and simple shapes, not a realistic or Pixar-style render.
Save the image as `Art/Thumbnail/Generated/5a Cashier view v1.png` (v2, v3 for later tries; never overwrite).
```

**5b "who just walked in"** (like the durian reference):

```text
Create a wide 16:9 landscape image.
Over-the-shoulder shot from behind a blocky Roblox shopkeeper in a dark work kimono, standing at a wooden shop counter.
He has turned back toward the camera in shock: wide eyes, open mouth, three yellow comic shock lines by his head.
In the bright open doorway beyond the counter stands a towering samurai warlord in red-and-black armour, ducking under the door frame, backlit by sunlight.
Sword racks on the white plaster walls.
Style: Roblox game thumbnail, glossy stylized 3D render, blocky Roblox characters, saturated colours, clean edges. No text, letters, logos or watermark. Keep the Roblox look: blocky characters and simple shapes, not a realistic or Pixar-style render.
Save the image as `Art/Thumbnail/Generated/5b Who walked in v1.png` (v2, v3 for later tries; never overwrite).
```

**5c Rengoku walks in, the bacon-hair cashier in shock** (Allen: "where rengoku walks into the store and the cashier is shocked", "i want the bacon hair boy to be the cashier"). Reference `Art/Thumbnail/Concept 5 - Behind the counter/Studio ref 5c - Rengoku walks in.png`:

```text
Create a wide 16:9 landscape image.
Reference images in the vault: the layout is `Art/Thumbnail/Concept 5 - Behind the counter/Studio ref 5c - Rengoku walks in.png`; the visitor's look is `Art/VIP NPCs/Rengoku (Renguko) - VIP.png`. Keep both characters, the counter and the shop as in the layout image.
Setting: inside a bright Japanese sword shop, with pale wooden floor planks, white plaster walls with dark timber beams, a slatted wooden ceiling, empty wall shelves, and a dark wooden counter with a light top.
Foreground, left third, large and cut off at the waist: the cashier, the classic Roblox "bacon hair" noob: messy orange-brown hair, a black open jacket over a blue T-shirt with a black motorcycle print, standing behind the counter facing the camera. He is in total shock: eyes wide, mouth wide open, both hands thrown up, three yellow comic shock lines beside his head and a sweat drop.
Background, centre right, in the bright open front doorway: the visitor striding in, a blocky Roblox swordsman with spiky golden hair tipped red, fierce orange eyes and a confident grin, a white cape with a red-and-yellow flame pattern at the hem over a dark red uniform, a sword with a flame-shaped guard at his hip. Strong sunlight behind him, orange flames and embers swirling around his feet and cape, light rays spilling into the shop.
The cashier and the visitor both in sharp focus; the shelves and side walls slightly blurred.
Style: Roblox game thumbnail, glossy stylized 3D render, saturated colours, clean edges. No text, letters, logos or watermark. Keep the Roblox look: blocky characters and simple shapes, not a realistic or Pixar-style render.
Save the image as `Art/Thumbnail/Generated/5c Rengoku walks in v1.png` (v2, v3 for later tries; never overwrite).
```

- Reference (Edit, 16:9, 1108×622): a clone of Allen's Bacon Hair Boy as the cashier, behind a copy of the Upgraded Store's CashierCounter moved up to the front door (the real counter sits behind a wall frame of the overlapping shells in Edit); Rengoku from `CastRigs.build` in the doorway. Kept in `ServerStorage.ThumbnailStages.Concept5c_RengokuWalksIn` (camera in its Note attribute, FOV 50).
- Rengoku is a recognisable Demon Slayer character: in the thumbnail he's a bigger copyright and moderation risk than inside the game, where his name is a letter off. If it's flagged, swap in the samurai warlord from 5b.

- The question mark in 5a teases the offer system (customers offer a price, you accept or not). That's the honest hook.
- Studio: the shop interior, counter and customer NPCs exist. The giant visitor in 5b is a scaled-up rig.

### 6. First person: packing a crate

Generator only (first-person hands are awkward to stage in Studio).

```text
Create a wide 16:9 landscape image.
Reference image in the vault for the katana and the anvil yard's look: `Art/Thumbnail/Concept 4 - Forging close-up/Studio ref A - sword on anvil.png`.
First-person view looking down at two blocky Roblox hands lowering a gleaming katana with a red wrapped hilt into an open wooden crate lined with golden straw.
Two more swords lie packed side by side in the crate, and a paper delivery tag is tied to its edge with string.
Through an open wooden bay door ahead, a wooden delivery cart waits on a sunny village street with cherry trees.
Style: Roblox game thumbnail, glossy stylized 3D render, saturated colours, bright daylight, clean edges. No text, letters, logos or watermark. Keep the Roblox look: blocky characters and simple shapes, not a realistic or Pixar-style render.
Save the image as `Art/Thumbnail/Generated/6 Packing a crate v1.png` (v2, v3 for later tries; never overwrite).
```

- The etching version is left out for now: the etch is instant in the game today, so a "tracing a glowing pattern" shot would promise a minigame that isn't there.

### 7. Silhouette collection + title

Like the BOOK window: a grid of black sword silhouettes on sunburst tiles, "???" under each, one tile revealed in full colour with a gold glow, title across the top.

- No generator needed: `Art/Sword Silhouettes/` has 23 silhouettes and `Art/Thumbnail/Swords/Metals/` the coloured versions. Composite it.
- **Title is open.** The game is "Sell Swords!" in the current thumbnail; the ideas note suggests "Create Swords!" or "Swordshop Tycoon". The thumbnail title should match the game's name on Roblox.

## Next

- [x] Allen picked 4 first, then 3, then 5c (Rengoku walks in); all staged 2026-11-08 (above). Next suggested: 2.
- [ ] Composite 1 and 7 from the existing renders (no Studio or generator needed).

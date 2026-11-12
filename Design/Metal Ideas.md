# Metal Ideas

Brainstorm from 2026-10-23 (Allen: "They could be from fantasy or completely random like a watermelon ingot or dragon ingot"). **Built** marks the ones in the game ([[Sessions/2026-10-23#New metals]], [[Sessions/2026-10-24#Refinements 3]]); the rest are ideas. Current roster and odds: [[Design/Game Design Document#6.1 Materials (rolled at the Ore Roller)]].

Cost to add: **tint** = a row in `Shared/Materials`, uses the shared IngotMetal / BladeShine maps; **texture** = its own `<texture>Ingot` / `<texture>Blade` MaterialVariants (`Models/Metal/metal_textures.py`); **effect** = texture plus glow, particles or a moving texture (no system for that yet).

## Grounded and Japanese
- Tamahagane: dark steel with a wavy hamon line (texture)
- Black Iron: near-black, rough (tint) — **built, Common**
- Rose Gold (tint) — **built, Uncommon**
- Meteorite Iron: Widmanstätten crosshatch (texture)
- Brass (tint) — **built, Uncommon**
- Pewter (tint) — **built, Common**
- Shakudō: blue-black copper-gold (tint)

## Crystals and stone
- Jade (veined polished-stone texture since 2026-11-05) — **built, Rare**
- Amethyst (cut gem texture since 2026-11-05) — **built, Rare**; Moonstone (texture or Glass tint)
- Ruby — **built, Epic**; Sapphire — **built, Epic**; Emerald — **built, Epic** (all cut gem texture since 2026-11-05)
- Amber (honey bands and bubbles texture since 2026-11-05) — **built, Uncommon**; one with a bug inside could be a Secret
- Marble (Roblox Marble) — **built, Uncommon**

## Elemental and fantasy
- Dragonsteel: scales (texture) — **built, Legendary**; ember glow in the cracks would be an effect
- Frost Iron (Roblox Ice) — **built, Rare**; Magma Steel (Roblox CrackedLava, glowing cracks) — **built, Epic**; Storm Silver (effect)
- Sunsteel (Neon, glows) — **built, Legendary**; Voidsteel, Spirit Glass (tint or effect)
- Sakura Steel: pale pink, petal etch; a festival metal (texture)
- Kitsune Gold, Orichalcum, Adamantite (texture)
- Doppler: CS:GO-style red / green / blue candy smoke over dark metal (texture, `metal_textures.py doppler`) — **built 2026-10-29, Legendary**
- Air: pale blue-white glass, the blade about 45% see-through, a solid ingot (Glass tint with an `alpha`; Allen: "an airsword that is part transparent?") — **built, Epic** (2026-10-24)
- Rainbow Alloy: soft spectrum bands with paper grain, a katana red at the hilt to violet at the tip (texture, `metal_textures.py` `rainbow`, an original after Allen's watermarked `rainbow.webp`) — **texture built 2026-10-24**, Legendary; sized for the katana, so a tantō shows red to yellow and a longsword runs on into blue

## Joke (Secret tier, 0.1%, ×25)
- Watermelon: striped rind ingot, pink seeded blade (texture) — **built**
- Cheese, Chocolate (gold-foil variant), Candy Cane, Bubblegum, Toast, Jelly (texture)
- Rubber Duck (Roblox Rubber) — **built, Secret**; a squeak when held would need a sound
- Lava Lamp (effect), Pixel and Noob (texture), Cardboard (Roblox Cardboard) — **built, Secret** at ×25 like the others

Event metals (Sakura, Candy Cane) could be time-limited roller pools.

## Brainstorm 2026-11-04

Allen: "also brainstorm more ores", with the tier pass (Rose Gold to Rare, Ruby to Epic, Obsidian to Rare, Marble to Common, [[Sessions/2026-11-04]]). After it the tiers hold 6 / 4 / 7 / 6 / 6 / 3, so Uncommon has the most room. Not built.

**Claude's top picks**
- Diamond (Glass, white-blue, a sparkle effect) — Legendary: the one every kid expects
- Tamahagane (dark steel with a wavy hamon line, texture) — Epic: the katana steel, fits the Japanese smithy
- Emerald (Glass tint) — Epic, beside Ruby and Sapphire
- Cobalt (deep blue metal, tint) and Quartz (clear white Glass) — Uncommon, to fill it back to 6
- Sushi (salmon on rice, texture) — Secret: a joke metal that fits the town

**Common / Uncommon (tint, cheap)**
- Tin, Lead (dull grey-blue), Granite (Roblox Granite), Brick (Roblox Brick) — Common
- Cobalt, Quartz, Nickel, Titanium (pale blue-grey), Verdigris Copper (green patina, texture) — Uncommon

**Rare / Epic**
- Platinum (bright white metal), Topaz (amber-yellow Glass), Pearl (white with a soft sheen), Tungsten (heavy dark grey) — Rare
- Emerald, Tamahagane, Meteorite Iron (Widmanstätten crosshatch, texture), Toxic Steel (Neon green, glows) — Epic
- Storm Silver (silver with small lightning flickers, effect) — Epic

**Legendary**
- Diamond, Adamantite (dark green-black, texture), Orichalcum (red-gold, texture)
- Phoenix Steel (orange-red with ember sparks, effect), Voidsteel (black with slow purple swirl, texture)
- Spirit Glass (pale green, see-through like Air, ghost wisps as an effect)

**Secret (jokes, ×25)**
- Sushi, Onigiri, Mochi (pastel, soft), Ramen (noodle texture) — the town's food
- Cheese (holes texture), Cookie (choc chips), Gummy (translucent Neon), Slime (green, see-through)
- Glitch (the pink-and-black missing-texture checker), Noob (blocky yellow-blue)

**Events (time-limited roller pools)**
- Sakura Steel (spring), Pumpkin (Halloween), Candy Cane (winter), Firework (new year)

**Allen's picks (2026-11-04):** "just throwing some names out Diamond, Pearl, Void, Nimbus, Ice, Candy, Emerald, Sakura, Tempest, Panda, Gunmetal", at Claude's tiers:
- Gunmetal (dark blue-grey metal, tint) — **built, Uncommon**; Pearl (soft white with a pink-blue sheen, texture) — Uncommon
- Ice — **built: Frost Iron renamed**, Rare
- Emerald (Glass tint) — **built, Epic**; Sakura (pale pink, petals, texture), Nimbus (white cloud, part see-through, texture) — Epic
- Diamond (icy-blue faceted texture, `metal_textures.py diamond`; sparkle later) — **built, Legendary**; Void (black, purple swirl), Tempest (storm grey-blue, lightning streaks) — Legendary, textures
- Candy (stripes), Panda (black-and-white print) — Secret, textures
[[Sessions/2026-11-04#New ores: Ice, Gunmetal, Emerald, Diamond]]

## Brainstorm 2026-11-05

Allen: "can you brainstorm more materials to use in our game", then "less food themes, more cool concepts". New names only (not repeating the lists above). The roster is 35: 6 / 5 / 7 / 7 / 7 / 3, so Uncommon and Secret have the most room. Not built.

**Cool concepts**
- Black Hole (black core, an orange glowing rim along the edge, texture) — Secret
- Synthwave (pink and cyan grid on black, texture) — Legendary
- Circuit (green board with gold traces, texture) — Epic
- Soulfire (black steel, blue flames up the blade, texture; flicker later) — Legendary
- Runestone (dark stone, glowing carved runes, texture) — Epic
- Clockwork (brass gears, texture) — Epic
- Bloodmoon (deep red, a dark moon near the tip, texture) — Legendary
- Seraph Steel (white gold, feather pattern) and Infernal (black, red cracks), a pair — Legendary
- Prism (clear Glass that splits into a rainbow edge) — Legendary
- Antimatter (inverted colours: white with black glow) — Secret
- Static (grey TV noise), Code Rain (green falling symbols on black), Glitch (above) — Secret
- Chrome (perfect mirror) — Rare; Carbon Fiber (woven black) — Uncommon
- Fossil (stone with a bone imprint, texture) — Rare

**Japanese myth**
- Kitsunebi (foxfire: pale blue flames) — Legendary
- Raijin (storm drums: yellow lightning on dark blue) and Fujin (wind: pale green swirls), a pair — Legendary
- Oni Steel (red with black cracks) — Legendary
- Yūrei (ghost white, fades to see-through at the tip, like Air) — Epic
- Koi Steel (white with orange and black koi patches) — Epic; Sumi Ink (ink-wash brush strokes) — Epic
- Iron Sand / Satetsu (black, sparkly grain) — Common; Urushi Lacquer (glossy red, black edges) — Uncommon

**Cheap: reuse a texture we already have** (a tint on an existing `<texture>Ingot` / `<texture>Blade`)
- Gem facets: Topaz (amber-yellow), Garnet (deep red-brown), Tanzanite (blue-violet), Peridot (lime) — Uncommon to Rare
- Jade veins: Turquoise (sky blue-green, dark veins) — Uncommon
- Amber bands: Malachite (green bands), Tiger's Eye (gold-brown bands) — Rare
- Roblox materials: Rusty Iron (CorrodedMetal) — Common; Ghost Steel (ForceField, shimmers with no effect system; check it shows on the blade mesh) — Legendary; Holo (rainbow sticker shine, Foil) — Legendary

**Stone and crystal**
- Flint, Basalt (Roblox Basalt), Bone (off-white, rough) — Common
- Electrum (pale gold-silver, tint) — Uncommon
- Lapis Lazuli (deep blue, gold flecks), Hematite (mirror black-silver), Opal (white, colour flecks) — Rare
- Bismuth (rainbow stair-step crystals, texture) — Epic
- Abyssal (dark teal, glowing blue spots), Aurora (green-to-purple bands), Lunar Silver (pale silver, crescent, pairs with Sunsteel) — Epic to Legendary

**Claude's top picks:** Carbon Fiber and Turquoise (Uncommon, to 7), Circuit (Epic), Soulfire and Synthwave (Legendary), Black Hole (Secret).

**Textures made 2026-11-05** (Allen: "can u implement these so i can choose which to keep"): all 21 cool concepts and Japanese myth metals in `Models/Metal/concept_metals.py`; pick in `Models/Metal/concept_picker.html`. Allen kept seven, **built 2026-11-05**: Runestone (Epic), Soulfire, Bloodmoon, Infernal, Prism, Raijin, Oni Steel (Legendary). The other 14 stay ideas.

## Secret metals redo 2026-11-10

Allen found the Secrets bland and opened the lineup. Picked: every Secret gets a **moving texture layer plus a particle trickle**, on held swords too; the Secret tier becomes **Galaxy** (nebula, drifting stars, twinkles), **Lava Lamp** (rising blobs, soft colour shift) and **Glitch** (jumping pink-and-black checker). Watermelon, Cardboard and Rubber Duck leave the roll. Not built. [[Sessions/2026-11-10#Secret metals: moving textures and a new lineup]]

**Built 2026-11-10:** Galaxy, Lava Lamp, Glitch (Secret, moving, `Models/Metal/secret_metals.py`); Watermelon and Rubber Duck moved to Epic, Cardboard to Rare. [[Sessions/2026-11-10#Moving Secret metals built]]

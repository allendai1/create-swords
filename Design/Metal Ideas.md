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
- Jade (Glass look, tint) — **built, Rare**
- Amethyst (Glass) — **built, Rare**; Moonstone (texture or Glass tint)
- Ruby (Glass) — **built, Rare**; Sapphire (Glass) — **built, Epic**; Emerald (Glass tint)
- Amber (Glass) — **built, Uncommon**; one with a bug inside could be a Secret
- Marble (Roblox Marble) — **built, Uncommon**

## Elemental and fantasy
- Dragonsteel: scales (texture) — **built, Legendary**; ember glow in the cracks would be an effect
- Frost Iron (Roblox Ice) — **built, Rare**; Magma Steel (Roblox CrackedLava, glowing cracks) — **built, Epic**; Storm Silver (effect)
- Sunsteel (Neon, glows) — **built, Legendary**; Voidsteel, Spirit Glass (tint or effect)
- Sakura Steel: pale pink, petal etch; a festival metal (texture)
- Kitsune Gold, Orichalcum, Adamantite (texture)
- Air: pale blue-white glass, the blade about 45% see-through, a solid ingot (Glass tint with an `alpha`; Allen: "an airsword that is part transparent?") — **built, Epic** (2026-10-24)
- Rainbow Alloy: soft spectrum bands with paper grain, a katana red at the hilt to violet at the tip (texture, `metal_textures.py` `rainbow`, an original after Allen's watermarked `rainbow.webp`) — **texture built 2026-10-24**, Legendary; sized for the katana, so a tantō shows red to yellow and a longsword runs on into blue

## Joke (Secret tier, 0.1%, ×25)
- Watermelon: striped rind ingot, pink seeded blade (texture) — **built**
- Cheese, Chocolate (gold-foil variant), Candy Cane, Bubblegum, Toast, Jelly (texture)
- Rubber Duck (Roblox Rubber) — **built, Secret**; a squeak when held would need a sound
- Lava Lamp (effect), Pixel and Noob (texture), Cardboard (Roblox Cardboard) — **built, Secret** at ×25 like the others

Event metals (Sakura, Candy Cane) could be time-limited roller pools.

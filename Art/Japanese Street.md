---
title: Japanese Street
status: built 2026-10-21, awaiting Allen's review
type: art
date: 2026-10-21
updated: 2026-10-21
tags: [environment, village, map, architecture, create-swords]
---

# Japanese Street

Allen (2026-10-21): "I have some references in Japanese Village/ for how I want our map to feel and look like. It's a street in a Japanese town. Note the architecture and the design. Can you create such map for our game?"

References in `References/Japanese Village/`: Kawagoe kura row (`Edo-Post-Towns_04-Kawagoe-1024x683.jpg`), Takayama Sanmachi (`Old-Town-in-Takayama-scaled.webp`, `images (2).jfif`), Tsumago-juku (`5streets_14.webp`, `images.jfif`), a Gifu canal street (`images (1).jfif`) and Kanazawa's chaya district (`image.jpg`).

## What the references share

- **One straight, narrow street** lined on both sides by continuous two-storey townhouses (machiya). It runs to a vanishing point with mountains or trees at the end.
- **Eaves face the street.** Most roofs run parallel to it, with deep overhangs. A low pent roof over the ground floor shelters the walkway. Some houses turn a gable to the street (Gifu, Tsumago).
- **Ground floor:** dark timber posts with fine vertical lattice (koshi), sliding shutters, open shop fronts and indigo curtains (noren) at the doors.
- **Upper floor, three families:**
  - **Takayama:** a low upper storey with a lattice window band and cream plaster.
  - **Kawagoe kura:** thick black or white plaster storehouses with heavy ridges, big end tiles (onigawara), small shuttered windows and a large signboard on the pent roof.
  - **Tsumago:** an upper storey projecting over the street, with a balcony railing and wooden shutters.
- **Street life:** potted plants, benches, red and white lanterns, vertical shop signs, copper gutters and downpipes, and a narrow water channel with stone slab crossings (Gifu, Takayama). Kanazawa paves the whole street in stone flags.
- **Colours:** dark brown timber, cream or white plaster, blue-grey tiles, indigo noren, red lanterns, and green and autumn-red trees.

## Built: `Workspace.Village` (2026-10-21)

Built by `Models/Village/build_street.luau` (run in Studio through MCP; same seed = same street). One model, pivot at the street centre (4, 0, −560), so it can be moved with `PivotTo`. It sits north of the current plot pieces and touches none of them.

![[References/Japanese Village/street-v1-west.jpg]]

- **Street:** 790 studs long, 32 between façades. A 16-wide stone-paved road (Pavement material), water channels with stone curbs and slab bridges at every door, and 6-wide walkways under the eaves.
- **26 townhouses** in five styles mixed at random: Takayama (lattice band, rafters), kura (black or white plaster, onigawara, roof signboard), Tsumago (projecting balcony), gable-front, and single-storey. Every house has a noren door. Most have a lantern, a vertical shop sign, pots, a bench or goods on an open platform. Neighbouring roofs always differ in height and pitch.
- **Six plot lots**, three per side, 140 × 110, open to the street with white plaster walls (tile cap, stone base) between them and the houses, and standing lamps at the corners. `Village.Lots.PlotSlotN1..N3 / S1..S3` are invisible markers at each lot's centre, facing the street, for when the plot is cloned into them. Lot N2 (north, middle) holds the current plot and is 280 wide (see below).
- **West end:** a roofed village gate with the sign 刀鍛冶の里 ("swordsmith village"), walls out to the cliffs, pines and bamboo.
- **East end:** a stone plaza, vermilion torii, stone lanterns, sakura and maple, and a small shrine with a copper-green roof and a shimenawa rope. It is the street's vanishing point.
- **Mountains:** the Blender `CliffRing` from `ServerStorage.Village3D`, stretched in X so its inner face meets the street ends. The cliff mesh does not collide; four invisible `Bound` walls on the inner face line keep players in. **Parked 2026-10-21** (Allen: "remove the mountains, we will work on it later"); the `Bound` walls stay.
- Backyards behind the houses hold pines, sakura, maple and bamboo, scaled up so they show over the roofs.
- Lanterns and lamps carry warm PointLights for evening (checked at ClockTime 18.9). The lighting itself was not changed.

![[References/Japanese Village/street-v1-shrine.jpg]]
![[References/Japanese Village/street-v1-gate.jpg]]
![[References/Japanese Village/street-v1-facades.jpg]]
![[References/Japanese Village/street-v1-dusk.jpg]]
![[References/Japanese Village/street-v1-top.jpg]]

**Z-fighting:** the coplanar-face check over all 2,607 block and wedge parts left 36 pairs, all hidden (roof ends inside a neighbour's roof, display platforms resting on the walkway, one lantern cord). The builder insets façade trim 0.05 from the side walls, and beams and rails end inside the posts.

## Shops and workshop (2026-10-21)

Allen: "Make our normal shop and upgraded shop blend seamlessly with the surrounding houses. it should seem like our shop is part of the street. The shops should match the same architectural style as the other buildings on the street. ... I also think we can have the smelting and sword creation process inside a building as well".

![[References/Japanese Village/street-v2-starter.jpg]]
![[References/Japanese Village/street-v2-upgraded.jpg]]

- **Built from the townhouses' own pieces** (`Models/Village/build_shops.luau`): the same palette, posts, koshi lattice bays with shoji behind, beam and transom, noren, chochin, a vertical shop sign, pots on the walkway and a stone slab over the water channel. Roofs are ClayRoofTiles with eaves to the street.
- **On the façade line:** both shops stand in the house row in lot N2, posts on the walkway like their neighbours'. Same frontage (31.5) and street front, so the Upgraded Store still replaces the Starter in place.
- **Starter Shop:** a single-storey machiya, like the street's low houses. Four lattice bays and a 12.5-wide entrance under an indigo 刀 noren, with the 刀鍛冶 signboard standing on the roof above the deep eave. Plaster-and-timber side walls, since it has no neighbour wall to lean on.
- **Upgraded Store:** a two-storey black kura, like the Kawagoe houses. Shuttered windows front and sides, a hachimaki band, the 刀鍛冶 signboard on the pent roof, a copper gutter and downpipe, and onigawara at the ridge ends. It is the tallest building on the street (ridge ≈ 31), as the big merchant house should be.
- Both open an east side door toward the workshop. Everything above the eave fades indoors.

![[References/Japanese Village/street-v2-lot.jpg]]

- **Workshop hall** behind the courtyard, 74 × 71: a plaster-and-timber hall (dark board wainscot, white plaster, timber bands) with high lattice windows. A smoke vent (koshi-yane) sits on the ridge over the furnaces. The main door has a brown noren, red chochin and a 鍛冶場 signboard, and a side door faces the shop. It encloses the ore carts and mine entrance, both furnaces, the anvil, Hilt Bench, Etching Table, Polishing Station and racks where they already stood, with room left for upgrades.

![[References/Japanese Village/street-v2-workshop-inside.jpg]]

The mountains are parked, so the street ends in open grass for now.

## Shop and back-room workshop (2026-10-21)

Allen's layout, `References/Concept Art/shop design`: "Shop + back-room workshop", with the shop on the street, a workshop door, and crafting clockwise round the workshop. He asked to build it with Claude's defaults and a placeholder supply alcove for the ore.

![[References/Japanese Village/backroom-top.jpg]]

- **One building, like a real machiya:** the shop room on the street (48 × 28) and the workshop behind it (48 × 50), joined by a centre door with an indigo noren. From the street it is one shop front in the house row, with the taller workshop roof and smoke vent rising behind it. It replaces the separate hall and courtyard from earlier the same day.
- **Shop room:** the counter front-left, display tables on the right, two wall racks on each side wall, a 依頼 commissions board and a tansu on the partition. The Starter / Upgraded Store swap changes only the front: one storey, or the black kura.
- **Workshop, clockwise from the door:** ore alcove, furnace, furnace 2, anvil and Hilt Bench along the back wall; Polishing Station then Etching Table down the right wall; the finished-sword rack by the door; the ingot rack on the left wall; open floor in the middle.
- **Placeholder ore alcove:** a raised cedar stage in the back-west corner, under a dark hatch with a wooden chute, with up to six ore trays and the lever beside it. The trays flicker and settle in place. The mine, rails and carts are parked until the ore source is chosen.

![[References/Japanese Village/backroom-shop.jpg]]
![[References/Japanese Village/backroom-workshop.jpg]]
![[References/Japanese Village/backroom-street-starter.jpg]]
![[References/Japanese Village/backroom-street-upgraded.jpg]]

## Continuous row (2026-10-21)

Allen asked "why are there so many empty spaces?", then: "shrink lot N2 to the building, bring the parked townhouses back, resize all six lots to the new footprint, and give unclaimed lots a closed shopfront so the street reads as one continuous row."

![[References/Japanese Village/street-v3-row.jpg]]

- **Lots are the building's width** (48.5 × 96), so the shop + workshop stands shoulder to shoulder with the townhouses. The street was rebuilt from `build_street.luau` with the same seed: 54 townhouses now fill the segments between the lots (the earlier parked ones are replaced by this row).
- **Closed shopfronts** stand on the five lots without a player plot: a townhouse of the lot's width with every bay shuttered, and no door, noren, lantern or sign.
- Behind the house row, plaster walls divide each lot from the neighbours' backyards; backyard trees stay off the lots.

![[References/Japanese Village/street-v3-closed.jpg]]
![[References/Japanese Village/street-v3-top.jpg]]

## Open

- **Plot moved into lot N2 (2026-10-21; superseded by the continuous row):** Allen asked to move the current plot pieces, `SpawnLocation` and `CustomerSpawn` into the middle north lot. The pieces span 238 × 114, wider than a 140 lot, so on Allen's pick the lot was widened to 280 by parking the townhouses either side of it, and everything moved by one offset so the in-progress layout is unchanged. `CustomerSpawn` stands on the road in front of the lot. See [[Development/Code Map#Village street (2026-10-21)]].

![[References/Japanese Village/street-v1-plot-n2.jpg]]

- ~~The other five lots are empty … size all six lots to it.~~ Done 2026-10-21: lots are 48.5 × 96 and the empty ones have closed shopfronts.
- `CustomerSpawn` had gone missing from the place, which left `ShopService` waiting forever at startup; it is back as `Village.CustomerSpawn`.
- ~~With most lots empty, the street has gaps.~~ Closed shopfronts since 2026-10-21. When player plots come, a claimed lot swaps its closed front for that player's shop.

Related: [[Art/Japanese Village Concept Art]] · [[Art/Anime Village Architecture]] · [[Development/Code Map]] · [[Design/Game Design Document]] · [[Sessions/2026-10-21]] · [[Home]]

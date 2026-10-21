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
- **Mountains:** the Blender `CliffRing` from `ServerStorage.Village3D`, stretched in X so its inner face meets the street ends. The cliff mesh does not collide; four invisible `Bound` walls on the inner face line keep players in.
- Backyards behind the houses hold pines, sakura, maple and bamboo, scaled up so they show over the roofs.
- Lanterns and lamps carry warm PointLights for evening (checked at ClockTime 18.9). The lighting itself was not changed.

![[References/Japanese Village/street-v1-shrine.jpg]]
![[References/Japanese Village/street-v1-gate.jpg]]
![[References/Japanese Village/street-v1-facades.jpg]]
![[References/Japanese Village/street-v1-dusk.jpg]]
![[References/Japanese Village/street-v1-top.jpg]]

**Z-fighting:** the coplanar-face check over all 2,607 block and wedge parts left 36 pairs, all hidden (roof ends inside a neighbour's roof, display platforms resting on the walkway, one lantern cord). The builder insets façade trim 0.05 from the side walls, and beams and rails end inside the posts.

## Open

- **Plot moved into lot N2 (2026-10-21):** Allen asked to move the current plot pieces, `SpawnLocation` and `CustomerSpawn` into the middle north lot. The pieces span 238 × 114, wider than a 140 lot, so on Allen's pick the lot was widened to 280 by parking the townhouses either side of it, and everything moved by one offset so the in-progress layout is unchanged. `CustomerSpawn` stands on the road in front of the lot. See [[Development/Code Map#Village street (2026-10-21)]].

![[References/Japanese Village/street-v1-plot-n2.jpg]]

- The other five lots are empty until the plot exists per player. The 140 × 110 lot size comes from the earlier cliff-ring layout (`Models/Village/build_village.py`) and does not fit the current plot; settle the plot footprint, then size all six lots to it.
- `CustomerSpawn` had gone missing from the place, which left `ShopService` waiting forever at startup; it is back as `Village.CustomerSpawn`.
- With most lots empty, the street has gaps. Unclaimed lots could get a closed shopfront or a "for sale" look.

Related: [[Art/Japanese Village Concept Art]] · [[Art/Anime Village Architecture]] · [[Development/Code Map]] · [[Design/Game Design Document]] · [[Sessions/2026-10-21]] · [[Home]]

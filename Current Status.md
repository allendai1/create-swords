---
title: Current Status
aliases: [Next Session Handoff]
status: current build record — recent Play checks pending
type: status
updated: 2026-10-22
tags: [status, create-swords]
---

# Current Status

Consolidated from build records through **2026-10-22**. This cleanup did not inspect Studio or rerun the game. “Built” means implementation is recorded; it does not mean the latest combined build has passed Play, multiplayer, or device testing.

## Built and recorded

| Area | Latest recorded implementation | Evidence |
|---|---|---|
| Core crafting | Ore → heat → guided forging → three untimed hilt knocks → display → customer sale. Player forging gives 100% quality; optional full polishing adds +10% value. | [[Sessions/2026-10-19]], [[Development/Code Map]] |
| First sales | Heating is 3 s until the first sword is completed, then 10 s. A listing brings a customer immediately until the first sale. The first offer equals sword value; the second ordinary sale teaches haggling. Counters are saved since 2026-10-22. | [[Sessions/2026-10-22#The first sword goes quicker; a delivery bay on every plot]], [[Sessions/2026-10-22#Fair first offer, haggling on the second sale]] |
| Ore loot box | 3.6 s lid/ingot reveal; up to six bought slots on one box. Collect all waiting ore before rolling again. Ore Slot 2–6 purchases already exist. | [[Art/Ore Loot Box]], [[Design/Tycoon Upgrades]] |
| Village and plots | Simplified six-lot village; each player gets an owned plot, with per-plot stations, shop, pads and customers. Unclaimed lots show unusable empty plots. | [[Design/Six Plots]], [[Art/Town Street Redesign References]] |
| Workshop | Chest back-left, furnace hearth, central anvil, right-wall hilt/polish/etch bench. Station cameras and mounts were adjusted. | [[Art/Workshop Layout]] |
| Upgrades and storage | Floor-pad purchases, second furnace, ore slots, finishing stations, ingot/sword racks and displays. Upgraded Store deepens the shop and pushes the workshop back 12 studs. | [[Design/Tycoon Upgrades]] |
| Roofs and inventory | Local roof fading, custom rarity-coloured hotbar, backpack overflow and drag/drop inventory. | [[Development/Code Map]], [[Art/UI Design#Backpack (2026-10-21)]] |
| Etching and polishing | Flame and Eclipse playback; etched swords show polish sheen. The recorded hitch fix spreads image preparation over frames. | [[Art/Animated Blade Etching]], [[Sessions/2026-10-22#Etching → polishing: lag and no visible polish]] |
| Finished sword meshes | Baked-first mesh pipeline with 27 recorded shapes and live fallback. Active forging/polishing still uses deforming geometry. | [[Development/Sword Mesh Pipeline]] |
| Delivery space | Bay on every plot and a shop door hidden behind the future `Delivery` unlock. The board, upgrade entry, courier and payouts are not built. | [[Sessions/2026-10-22#The first sword goes quicker; a delivery bay on every plot]] |
| Authoring tools | Browser forge study/profile editor, BladeCore Luau port, local model sources and village/workshop builders. | [[Prototypes/tanto-forge/README.md]], [[Prototypes/tanto-forge/roblox/README.md]] |
| First-session journey (2026-10-22) | Tantō-only start; a guide line and arrow for every step; the Guard Captain's Iron Wakizashi request (blueprint on accepting, picker hand-in at the request board, 120 coins, not a sale); then "Buy Ore Slot 2"; the Wandering Swordsman's Katana request after the third sale. Fittings match the blade's tradition. Onboarding funnel logged. | [[Sessions/2026-10-22#Roadmap 1–3: build audit, first-session journey and saving]], [[Development/Code Map#First session and saving (2026-10-22)]] |
| Saving (2026-10-22) | Session-locked DataStore saves of coins, items and finishes, racks, displays, blueprints, upgrades, metals found, commissions and counters, with recovery rules; upgrades reapplied on the new lot. Studio uses its own store. | [[Development/Saving]] |
| Build audit fixes (2026-10-22) | Anvil soft-lock after closing the blade picker, hotbar over the polishing/hilt HUDs, offers overwriting each other, gamepad input for the anvil, pads, offers and hotbar, picker art and flags, display-sword streaming, roof gap at the shop door. | [[Sessions/2026-10-22#Roadmap 1–3: build audit, first-session journey and saving]] |

## Verification limits

- A complete roll → heat → katana → hilt → display → sale loop was historically playtested before the latest map/workshop changes. It is not proof of the current combined build.
- Recent map, workshop, loot-box, first-sale and polish-sheen changes have recorded Edit checks but no recorded full Play pass.
- Recorded module results include `EtchingSpec` 33/33 and `SwordMeshSpec` 110/110. They were not rerun during cleanup.
- Two-player ownership, south-lot cameras, plot release/reclaim, upgrade movement, many visible swords, image/mesh budgets and published/mobile clients still need runtime checks.
- Latest session notes repeatedly request saving the place; this vault cannot confirm the current Studio save state. Gameplay scripts live in the place, not in a Rojo checkout.
- 2026-10-22 (Edit only): `SaveSpec` 38/38, `ForgeCheckSpec`, `BladeCoreSpec` 31/31 and `SwordMeshSpec` 110/110 pass; the session lock was exercised against the real Studio DataStore with a throwaway key; changed modules load and changed scripts compile. The guide, commissions, saving across a rejoin and the new gamepad input have not been played. The server size was 50 and was set to 6 through Open Cloud (read back as 6).

## Missing systems

- Material Index and discovery feedback (discoveries are saved, not shown); polishing on gamepad.
- Customer reputation/familiarity, letters, personal commission chains, special arrivals and additional sword traditions.
- Employee hiring/training/production, bare-blade rack and worker/player handoffs.
- Functional courier delivery board, packing, dispatch/return and payouts; weather traffic bonuses.
- Further progression balance, sound/feedback, UI/input polish, environment finishing and launch validation.

Detailed remaining tasks: [[Development/Roadmap]]. Confirmed design: [[Design/Game Design Document]]. Open ideas: [[Random thoughts]].

## Recommended next milestone

A new player understands the first craft, sells a tantō, completes the Iron Wakizashi commission, buys the second ore slot, and returns with progress intact. All of it is built as of 2026-10-22; the milestone is now to play it through (opening, both requests, a rejoin) and run the first new-player sessions ([[Development/Roadmap]] 1–3).

## Resume and references

- Run the browser study from the vault root: `python -m http.server 8765 --directory Prototypes/tanto-forge/dist`; open `http://localhost:8765` or `editor.html` for the profile editor.
- Private Site identity, if needed: `appgprj_6ad655f29424819195e6e42693b729ae`, recorded in `Prototypes/tanto-forge/.openai/hosting.json`. The notes do not establish a deployment; reuse the identity and obtain fresh credentials.
- [[Sessions/2026-10-22]] contains the latest detailed build evidence. [[Archive/Project History/Vault cleanup — 2026-10-22]] records this reconciliation and retained history.

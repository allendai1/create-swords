---
title: Home
type: index
updated: 2026-11-01
tags: [index, create-swords]
---

# Sell Swords! — Home

Start with [[Current Status]] for the recorded build and verification limits, then [[Development/Roadmap]] for remaining work. [[Design/Game Design Document]] owns intended behavior. The latest reviews: economy [[Design/Economy Review — 2026-10-29]], upgrade tree [[Design/Upgrade Tree Review — 2026-11-01]], first session [[Design/Reviews 2026-10-31/First 10 Minutes Review]].

## Design and progression

| Note | Purpose |
|---|---|
| [[Design/Economy Pass 2]] | Built 2026-10-27, not played: prices for players who pick rare ore, a spine of goals (the next sword, the next employee) to about 13 h, stage gates, three working crafters, the Zanbatō, the lid and the bag's trash |
| [[Design/Monetization Plan]] | Decided 2026-10-27; the six passes, the Auto Ore Roller's button and the Shop page built, not played: passes (Auto Ore Roller with its popup by the roller, 50% More Coins, Lucky Metal, VIP, Swift Boots), one Starter Pack, weather for Robux or gems, coin and gem packs, the odds panel and the paid-random-item rules |
| [[Design/Game Design Document]] | Confirmed game direction, with unbuilt scope identified |
| [[Design/Pottery Tutorial Review]] | Timestamped reference-video analysis and proposed onboarding lessons |
| [[Design/Tycoon Upgrades]] | Current starting plot, branching purchases and recorded prices |
| [[Design/Six Plots]] | Claiming, ownership, visitors, empty plots and leaving |
| [[Design/Workshop Growth]] | Employee/delivery/weather design and unresolved tuning |
| [[Design/Decisions Log]] | Dated decisions; later entries supersede older choices |
| [[Design/Upgrade Tree Review — 2026-11-01]] | Proposal only: illogical gates, the Upgraded Store coming too early, hire pads that hide their station needs |
| [[Design/Economy Review — 2026-10-29]] | Economy and progression with 24 swords on three blueprint pads |
| [[Design/Refinements Proposals — 2026-10-30]] | The items from Allen's 2026-10-30 list that are his call |
| [[Design/Monetization Ideas — 2026-10-31]] | Proposals only: convenience and impulse purchases |
| [[Design/QoL and Settings Ideas — 2026-10-31]] | Quality-of-life and performance settings ideas |
| [[Design/Kids and Reward Loops Research — 2026-10-31]] | How kids play Roblox and what reward loops mean for us |
| [[Design/Shop Tension Pass]] | Offer spread, customer rush and a felt first heating upgrade |
| [[Design/Pottery Playthrough 2026-10-27]] | Create Pottery from a fresh start, frame by frame |
| [[Design/Pottery Playthrough 2026-11-02]] | Create Pottery to its first employee: prices, unlock order, our Sword Crafter beside it |
| [[Design/Metal Ideas]] | Metal brainstorm; **Built** marks the ones in the game |
| [[Design/Sword Profile Ideas]] | More blade shapes to pick from |
| [[Design/LihFolk Vault Review — 2026-10-30]] | What the LihFolk vault means for this game |
| [[Design/tycoon-game-design-checklist]] | Generic tycoon checklist, unticked |
| `Design/Reviews 2026-10-31/` | The 2026-10-31 map, UI, first-10-minutes and performance reviews and their handoffs |
| [[Random thoughts]] | Single inbox for unimplemented ideas and questions |

## Development

| Note | Purpose |
|---|---|
| [[Development/Roadmap]] | Remaining implementation and validation tasks |
| [[Development/Code Map]] | Current recorded services, controllers, ownership and source locations |
| [[Development/Saving]] | What is saved, recovery rules, the session lock and schema versions |
| [[Development/Gameplay Simulator Plan]] | The gameplay simulator (`Development/sim`); runs are in `Development/Sim Runs/` |
| [[Development/Analytics Funnels]] | Server-side AnalyticsService funnels |
| [[Development/Sword Mesh Pipeline]] | Implemented baked-mesh pipeline and adding a sword |
| [[Development/Blade Implementation Research]] | Approach comparisons and historical Studio probes |
| [[Development/Blade Profile Authoring]] | Shape data, measurements and profile editor |
| [[Development/Sword Modeling Quality Checklist]] | Modeling checks and review rubric |
| [[Prototypes/tanto-forge/README.md]] | Browser forge study and profile editor |
| [[Prototypes/tanto-forge/roblox/README.md]] | BladeCore port and Studio probe workflow |

## Current art and interface references

| Note | Purpose |
|---|---|
| [[Art/Town Street Redesign References]] | Chosen simplified map and preserved comparisons |
| [[Art/Workshop Layout]] | Current room layout, cameras and station positions |
| [[Art/Ore Loot Box]] | Current roll presentation and collect-before-reroll behavior |
| [[Art/Katana Hilt]] | Imported hilt, guards and modeling history |
| [[Art/Flame Etch]] | Flame pattern history and chosen appearance |
| [[Art/Animated Blade Etching]] | Playback implementation, polish sheen, patterns and pending checks |
| [[Art/UI Design]] | Implemented picker, chosen hotbar and backpack; remaining UI work |
| [[Art/Icon Library]] | Icon ids from the Free Icon Pack |
| [[Art/UI Review 2026-10-26]] | Every StarterGui screen captured for critique |
| [[Art/UI Concept - Furnace]] | Picker visual proposal |
| [[Art/Sword Silhouettes]] | Sword-shape reference |
| [[Art/Anime Village Architecture]] | Optional atmosphere/architecture studies |

## History and files

- **Sessions:** [[Sessions/2026-11-01]] · [[Sessions/2026-10-31]] · [[Sessions/2026-10-30]] · [[Sessions/2026-10-29]] · [[Sessions/2026-10-28]] · [[Sessions/2026-10-27]] · [[Sessions/2026-10-26]] · [[Sessions/2026-10-25]] · [[Sessions/2026-10-24]] · [[Sessions/2026-10-23]] · [[Sessions/2026-10-22]] · [[Sessions/2026-10-21]] · [[Sessions/2026-10-19]] · [[Sessions/2026-10-18]] · [[Sessions/2026-10-17]]. Entries describe the build at that time.
- **Fix lists:** Allen's lists in the vault root are worked through and recorded in Sessions. Finished ones (and their screenshots) move to `Archive/Fix Lists/`; [[Archive/Project History/Vault cleanup — 2026-11-01]] has the list.
- **Older art/layouts:** `Archive/Art/` contains the retired smithy, Blender station review, building redesign, plot review, Japanese street, village concepts and blade-shaping study. Their references remain linked.
- **Replaced reviews:** the urgency notes, Alignment Review 2026-10-23, Core Loop Review, Progression and Economy Review 2026-10-27, Upgrade Order Review 2026-10-28 (`Archive/Design/`) and Technical Debt 2026-10-24 (`Archive/Project History/`); each opens with what replaced it.
- **Older rules/plans:** `Archive/Design/` and `Archive/Project History/` retain historical versions, the original brainstorm and cleanup records. [[Archive/Project History/Vault cleanup — 2026-10-22]] explains the latest changes.
- **References:** screenshots, concept images, prompts and videos. Duplicate copies were consolidated; unique source assets remain.
- **Models:** editable model sources, exports and builders; `Models/Archive/` holds superseded models. Keep runnable/source paths stable.
- **Prototypes:** browser/Luau experiments and tooling; these are working assets, not vault clutter.

## Keep the vault current

1. Update **GDD** when behavior is agreed; record the reason/date in **Decisions Log**.
2. Replace stale **Current Status** summaries; link detailed evidence instead of appending a build diary.
3. Keep **Roadmap** to remaining work. Remove completed implementation once its record exists; retain unrun verification tasks.
4. Put chronological changes in **Sessions**. Preserve historical rules as history rather than presenting them as current.
5. Keep new ideas in **Random thoughts** until resolved or moved to their owning design note. Archive completed batches.
6. Label superseded art/plans, update links when moving files, and distinguish Edit checks from Play/multiplayer/device evidence.

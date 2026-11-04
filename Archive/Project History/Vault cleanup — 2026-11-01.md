---
title: Vault cleanup — 2026-11-01
type: history
status: completed — file moves and Home only
updated: 2026-11-01
tags: [vault, cleanup, history, create-swords]
---

# Vault cleanup — 2026-11-01

Allen: "can u clean up our vault. i have lots of notes i havent touched in a while."

Nothing was deleted and no note's text changed. Every fix list moved here already had its own Sessions entry.

## Moved to `Archive/Fix Lists/`

| Was | Now | Worked on in |
|---|---|---|
| `Untitled.md` | [[Untitled — 2026-10-26]] | [[Sessions/2026-10-26#Bigger plots with a fence]] |
| `Untitled 1.md` | [[Untitled 1 — 2026-10-28]] | [[Sessions/2026-10-28#Fixes 2026-10-28]], [[Sessions/2026-10-28#Fixes 2026-10-28, round 2]] |
| `Untitled 2.md` | [[Untitled 2 — 2026-11-01]] | [[Sessions/2026-11-01#Lucky Ore odds sign, no pad saving bar, no coin chest]] |
| `tips.md` | [[tips]] | [[Sessions/2026-10-26#Tips document (tips.md)]] |
| `Fixes.md` | [[Fixes]] | [[Sessions/2026-10-26#Fixes: picker grid, mail rework, mailbox]] |
| `Fixes2.md`, `Fixes3.md` | [[Fixes2]], [[Fixes3]] | [[Sessions/2026-10-28#Fixes2]], [[Sessions/2026-10-28#Fixes3 (and Fixes2's additions)]] |
| `More features.md` | [[More features]] | [[Sessions/2026-10-28#More features]] |
| `Upgrades.md` | [[Upgrades]] | [[Sessions/2026-10-28#Upgrades note: cream interior, floating shelves, plot size options]] |
| `Refinement.md`, `Refinements2.md`, `More refinements.md` | [[Refinement]], [[Refinements2]], [[More refinements]] | [[Sessions/2026-10-22]], [[Sessions/2026-10-23]] |
| `Refinements3.md`, `refinement4.md` | [[Refinements3]], [[refinement4]] | [[Sessions/2026-10-24#Refinements 3]], [[Sessions/2026-10-24#Refinement 4]] |
| `Refinements5.md` | [[Refinements5]] | [[Sessions/2026-10-25#Refinements 5]] |
| `List.md`, `bugs and changes.md`, `Features and fixes.md` | [[List]], [[bugs and changes]], [[Features and fixes]] | [[Sessions/2026-10-29#List.md]], [[Sessions/2026-10-29#Features and fixes.md]] |

The seven root screenshots went with them: `buggy shelf.png`, `buttons clickable thru wall2.png`, `buttons clickable thru walls.png`, `cluttered ui.png`, `misaligned sword rack.png` (named in [[Sessions/2026-10-25]] as "in the vault root"), `misaligned shop and street.png` and `wrong hammer hold.png` (named in [[Refinements3]]).

The three Untitled notes got a date in their name so a new `Untitled.md` in the root can't clash with them. Nothing linked to them; the Sessions and Code Map mention them by their old file names.

## Moved to `Design/`

- [[Archive/Design/Building urgency in the game]] (then archived in the second pass below)
- [[Design/tycoon-game-design-checklist]] (nothing linked to it)

## Left in the root

[[Home]], [[Current Status]], `CLAUDE.md`, [[Random thoughts]], [[Refinements]] (Allen's running list), and today's notes: [[Untitled 3]] (its upgrade tree item is still a proposal, [[Design/Upgrade Tree Review — 2026-11-01]]), [[tonights notes]], [[video ideas]], [[demon slayer yoshiwara]].

## Home

[[Home]] now lists the sessions through 2026-11-01 and the notes added since 2026-10-27 (the reviews, ideas notes, simulator, analytics, icon library, UI review).

Links to the moved notes are by name, so they still open. Checked after the moves: see [[Sessions/2026-11-01#Vault cleanup]].

## Second pass: replaced reviews

Allen: "Yes, review them" (the design notes newer reviews may have replaced). Each moved note now opens with an **Archived 2026-11-01** line naming what replaced it, and links to it were rewritten to the new path (39 notes).

| Note | Now in | Replaced by |
|---|---|---|
| Building urgency in the game, Urgency Review, Workshop Urgency Recommendations | `Archive/Design/` | VIP buyers, weather, [[Design/Shop Tension Pass]], [[Design/Decisions Log]] |
| Alignment Review — 2026-10-23 | `Archive/Design/` | [[Design/Economy Review — 2026-10-29]], [[Design/Upgrade Tree Review — 2026-11-01]], [[Development/Roadmap]] |
| Core Loop Review | `Archive/Design/` | [[Design/Reviews 2026-10-31/First 10 Minutes Review]] |
| Progression and Economy Review — 2026-10-27 | `Archive/Design/` | [[Design/Economy Pass 2]], [[Design/Monetization Plan]], [[Design/Economy Review — 2026-10-29]] |
| Upgrade Order Review — 2026-10-28 | `Archive/Design/` | [[Design/Upgrade Tree Review — 2026-11-01]] |
| Technical Debt and Deferred Features (2026-10-24) | `Archive/Project History/` | [[Development/Roadmap]] |

Kept: [[Design/Pottery Tutorial Review]] (still the reference video), [[Design/Six Plots]], [[Design/Workshop Growth]], [[Design/Tycoon Upgrades]], [[Development/Blade Implementation Research]] (already marked as history).

Fixed in place: [[Development/Gameplay Simulator Plan]] said "plan only, nothing built"; it now says built. [[Random thoughts]] lost the street-style question (cut stone, picked 2026-11-01). [[Home]] lists the latest reviews instead of the archived ones.

[[Current Status]] and [[Design/Tycoon Upgrades]] were stale (2026-10-22 and 2026-10-24); see the third pass.

## Third pass: Current Status and Tycoon Upgrades rewritten

Allen: "Yes, update them".

- [[Design/Tycoon Upgrades]]: the catalogue table is generated from `Development/sim/balance.json` (exported from Studio 2026-11-01 16:31), with the pad rules, starting plot, crew and delivery prices and the outside layout from the sessions. Old version: [[Archive/Design/Tycoon Upgrades before update — 2026-11-01]].
- [[Current Status]]: one row per area of the game as it is now, what Allen has played, the checks, and what's open. Built from the session notes of 2026-10-23 to 2026-11-01 (two read-only subagents summarised them; later sessions override earlier ones). Its old "start here" link pointed at a heading that doesn't exist. Old version: [[Archive/Project History/Current Status before update — 2026-11-01]].
- Three links in [[Archive/Project History/Technical Debt and Deferred Features]] to the old "Missing systems" heading now point at the snapshot.

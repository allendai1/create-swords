---
title: UI Concept - Furnace
status: visual proposal
tags: [concept-art, ui, create-swords]
type: "art"
updated: "2026-10-19"
---

# UI Concept — Furnace

![[References/Concept Art/furnace-ui-v1.png]]

A visual proposal based on the Create Pottery! ingot/clay selection reference and [[Archive/Player Plot Concept Art|Player Plot Concept Art]]. Generated with the built-in image generation tool. This is a design mockup, not implemented UI.

## Visual language

- Warm dark-brown panels, cream text, thin copper outlines, lightly rounded corners.
- Large item cards: a recognizable item render, name, owned quantity, and a small rarity badge with both color and words.
- Amber for furnace heat and hover/focus; muted green for successful actions; rarity accents kept small.
- Friendly rounded title font, simpler readable body font, minimal texture behind text.
- One main decision per station window. Whole cards are tappable, with equal feedback for touch, mouse, and gamepad.

## Interaction

1. Interact with an empty furnace slot to open **Furnace — Choose an ingot to heat.**
2. Show the ingots the player owns, grouped by material with quantity. Scroll the grid for more types.
3. Tap/click an ingot card once. Load one ingot; close the selector once loading succeeds and make the ingot visible in the furnace.
4. Show a brief **Ingot loaded** notice and a small timer over that furnace. The player can leave and use other stations.
5. Once ready, change the label to **Ready to collect** and offer collection.

The main loop's current heat duration is approximately 15 seconds. The timer and bar in the artwork illustrate the visual treatment; an implementation should derive both from the same actual remaining duration.

If the player has no ingots, show **No ingots yet** and a short direction to the ore roller. If all furnace slots are occupied, show their heating/ready states rather than opening a picker that cannot accept anything. An additional available slot can open the same picker.

Prevent duplicate loads while a selection is processing. If loading fails, keep the picker available and show a short reason. The close button dismisses the window without taking an item.

## Reuse across the game

Use the same card/grid system for choosing a blade at the Hilt Bench and a sword for an empty display holder. Add more detail only when the choice requires it: hilt bonuses and locked unlock progress at the bench, sword name/value/material when stocking a holder.

Keep the main plot HUD small so the land, stations and sword displays remain the focus.

Full generation prompt: [[References/Concept Art/furnace-ui-prompt-v1]].

## Status

Adopted on 2026-10-18 for all pickers (see [[Art/UI Design|UI Design]]), with two changes: the station keeps the name **Forge**, and when both slots are busy E shows a quick "Forge is full" message instead of the slots' states.

Related: [[Home]] · [[Design/Game Design Document|Game Design Document]] · [[Archive/Player Plot Concept Art|Player Plot Concept Art]]

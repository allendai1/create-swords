---
title: Completed quick thoughts — 2026-10-22
type: history
status: archived — implementation recorded; runtime checks remain on Roadmap
updated: 2026-10-22
---

# Completed quick thoughts — 2026-10-22

Original ideas retained after their implementations were recorded. Current verification tasks live in [[Development/Roadmap]]; this is not an active inbox.

* try to make our ore roller look like a Call of Duty loot box, where you open it, the ore floats around and spins its different types, and then falls down onto the lootbox again. reference in the vault. *(Built 2026-10-22: [[Art/Ore Loot Box]].)*
* players need to pick up their ores before rolling again. so until then, the ores should just stay on top. there's 6 ore rolls late game, so the box should be able to fit all 6 at a time even if only 1 is rolled early on. *(Built 2026-10-22: [[Art/Ore Loot Box]].)*
* each plot should have an area where we can eventually add a delivery carrier. maybe a guy with a carriage. potentially could carry over into the street. *(Space built 2026-10-22: the delivery bay beside each shop; see [[Archive/Project History/Code Map before cleanup — 2026-10-22#First sword and delivery bay (2026-10-22)]].)*
* etching station - automatic animation for etching the design on. *(Built 2026-10-21: [[Art/Animated Blade Etching]].)*
* first time tutorial, the furnace and other processes need to be sped up *(Built 2026-10-22: 3 s first heat, a customer at once until the first sale; see [[Archive/Project History/Code Map before cleanup — 2026-10-22#First sword and delivery bay (2026-10-22)]].)*

## Resolved inbox list (2026-10-22)

Allen's "Ideas still to resolve" as written, before it was answered and built ([[Sessions/2026-10-22#Inbox items resolved]]):

- Give the level more polish and atmosphere while preserving the chosen simplified map.
- Employees should visibly create swords using the relevant crafting animation.
- Players and employees should not use the same station simultaneously; settle assignment and priority rules.
- Consider unlocking each employee when the corresponding second station is bought, such as a furnace operator after Furnace 2 or a smith after a second anvil.
- Consider making the cashier available after the shop upgrade.
- The + icons next to racks are on the left side when it should be in the middle. they should be spaced out better. they also collide with things around it, causing parts to be chopped off. they should only be visible when close, i shouldnt be able to see them once i walk away.
- needs to be a small gap between inventory items/toolbar items
- the accept/decline of a sale should be a popup from the NPC, not as a popup just on the bottom right of our screen
- NPCs should be non-collidable with player
- Random NPCs walking the street would be a nice detail touch.
- Need to establish Daily Rewards
- Price of the sword on display rack does not need to be shown. we just need to know how much the player gets for example $100 [+20%] on the gui, so it shows how extra they're getting compared to how much it's worth. so in this case, 100 is how much it's worth x 1.20.
- the anvil accuracy chart doesn't align - it doesn't look like a sword anymore
- the hilting station where we click the bottom of the handle 3 times doesn't seem very interactive, and seems like 3 unnecessary clicks
- Current tutorial has player rolling until they get iron (from the comission they receive) - it may take many rolls to actually get one ..
- After buying ore slot 2 - tutorial seems to finish? no indication of whats next

## Second inbox list (2026-10-22)

Allen's second list as written, before it was answered and built ([[Sessions/2026-10-22#Second inbox list]]). The manual-etching note stays in [[Random thoughts]].

* The F to take back on the sword holder clashes with the E GUI to put on sale.
* The wall sword rack is a bit small, leaving the swords tightly packed together
* We could create a shelf that holds the 3 swords, look at the reference in concept art
* Could we have the roaming customers and also customers be people from our friends list?
* could possibly have a collection book that players can open and display all the swords they've unlocked, and ones they still need to unlock. might be a lot of variations?
* instead of the current mountain set up, could we try to just do rectangular blocks as mountains
* The roads look ugly.
* The upgraded shop doesn't seem rewarding enough, the growth seems pretty small.

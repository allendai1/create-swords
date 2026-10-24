---
title: Saving
status: built 2026-10-22 — Play checks pending
type: development
updated: 2026-10-24
tags: [saving, datastore, code, create-swords]
---

# Saving

Saved progress, built 2026-10-22 for [[Development/Roadmap#3. Persistent progress]]. Scripts: `ServerScriptService.Profiles` (store and lock) and `ServerScriptService.SmithyCore` (what is saved, when). Checks: `ServerStorage.Tests.SaveSpec`. Architecture: [[Development/Code Map]].

## What is saved

One DataStore key per player, `u<UserId>`, in the store `Profiles_v1` (Studio uses `Profiles_Studio_v1`, so testing never touches live saves). The key holds `{ data, lock, saved }`; `data` is:

| Field | Contents |
|---|---|
| `v` | Schema version (1) |
| `coins`, `completed`, `sold`, `nextId` | Coins, swords assembled (fitting unlocks), ordinary shop sales (first-sale rules, commission timing), next item id |
| `ingots`, `blades`, `swords` | Carried items. Swords keep their blade (blueprint, metal, grade, quality, multiplier, polish refinement, polished), hilt, seat bonus and etch (pattern and colours as hex) |
| `rack` | Ingot Rack and Finished Sword Rack contents. Since 2026-10-24 the sword list also holds Finished Sword Rack 2's hooks 7–12 (in code one rack of 12) |
| `displayed` | Swords on shop holders, keyed by the holder's path in the plot (`Shop/Displays/WallRack1/Slot2`) |
| `blueprints`, `discovered`, `upgrades` | Learned blueprints, metals ever collected (for the Material Index later), bought tycoon upgrades |
| `merges` | How many times Merge Ore Slots was used (0 = never): luck ×(1 + 0.5 × merges) on top of Lucky Roller, Ore Slot prices ×1.5 per merge. A merge also takes Ore Slots 2–6 out of `upgrades`. Added 2026-10-24 ([[Sessions/2026-10-24#Refinements 3]]) without a version bump; an older save loads 0, and odd values are repaired (rounded down, never below 0) |
| `gems`, `gemUpgrades`, `streak`, `lastClaim` | Gems; Gem Shop levels (`{ Advertising = n, Clients = n }`, missing = 0); daily days claimed (0–7, next is `streak % 7 + 1`); UTC day number of the last claim (0 = never). Added 2026-10-22; older saves load with none |
| `commissions`, `funnel` | Teaching commission status (`offered` / `active` / `done`) and first-session funnel steps already logged |
| `collection` | The collection book: `"<blueprintId>\|<materialId>"` → `{ etched = true?, polished = true? }`, every blade × metal ever made as a sword; entries are never removed. Added 2026-10-22 without a version bump; an older save loads with an empty book that fills from the swords it still owns. Keys whose blade or metal no longer exists are dropped |
| `reputation`, `orders`, `nextOrder`, `orderAt` | Reputation points; the request board's open orders; the next order id (2026-10-22); `os.time()` when the board's next order comes, missing while the board is full (2026-10-23); since 2026-10-24 each gap is a fresh random 3–10 minutes |
| `delivery` | Courier state: offers, the active order with its packed swords and return time, Capacity and Speed levels, orders delivered (2026-10-22). Since 2026-10-24 the swords are chosen on the packing page and leave the inventory only when the crate is filled (one dispatch call), so an order being packed saves no swords; the choice itself isn't saved. Half-packed crates in older saves still load (shown as full slots) and Cancel Order returns them |
| `crafter` | The sword crafter, nil until hired: swords made (its level), trained shapes, the shape it makes (2026-10-23). Since the hire became the `Crafter` pad (same day), a save with a crafter also loads `upgrades.Crafter`. Since [[Sessions/2026-10-23#Refinements 2, second list]] a roster: `{ trained, making, hired = { [id] = { made, since } }, equipped }`; an older single crafter loads as Taise, equipped; unknown crafters are dropped |
| `staff` | The other employees, one per role, each hired on its pad (so also in `upgrades`): `{ [role] = { since, count, setting } }` for `stocker`, `cashier`, `promoter` and `etcher`. `count` is jobs done (their level); `setting` is the Cashier's slider % or the Etcher's pattern. Only known roles are kept, `since` and `count` are cleaned, and a setting is kept only if it is a string or a finite number. Added 2026-10-24 ([[Sessions/2026-10-24#Refinements 3]]) without a version bump; an older save loads with none |
| `settings` | `{ music, sound }`, the Settings window's switches (2026-10-23); an older save loads with both on. Shown to the client as player attributes `Music` / `Sound` |

## Recovery rules

| Thing | On rejoin |
|---|---|
| Displayed swords | Back on the same holders; into the bag if that holder no longer exists or is taken |
| Racks | Back on the racks |
| Sword an employee is carrying (2026-10-24) | Back on the Finished Sword Rack, or in the bag if the rack is full |
| Upgrades | Re-bought on whichever lot the player gets, before it appears; the Upgraded Store's 12-stud push is reapplied |
| Ingot in a furnace | In the bag, **hot** (it finished heating while away) |
| Ore rolled but not collected (including mid-roll) | In the bag as cold ingots |
| Blade being forged | The hot ingot is still in the bag; strikes restart (the ingot is only used when the blade is finished) |
| Sword being polished | Unchanged; polishing restarts |
| Etch | Applied by the server at once, so either done or not; the show is only presentation |
| Blade waiting for a hilt | In the bag as a blade |
| Commission not yet accepted | Its visitor comes back to the shop; it is also on the request board |

Items or upgrades whose blueprint, metal, hilt, etch or upgrade id no longer exists are dropped on load (an unknown hilt becomes the Wooden Grip); duplicate or missing ids get fresh ones.

## When it saves

- **Load:** on join, before the plot is handed out (`PlotService` waits), so saved upgrades can be applied to the new copy.
- **Autosave:** every 60 s.
- **Leave:** `SmithyCore` takes the snapshot first, then runs every service's leave clean-up (`SmithyCore.onLeave`), then saves and releases the lock. Services must not clear saved things in their own `PlayerRemoving`.
- **Server close:** `BindToClose` saves everyone still in and waits up to 25 s for saves in flight.

One player's saves run in order, so an older snapshot never lands after a newer one. Someone who leaves and rejoins the **same** server is a new Player under this server's own lock, so their load first waits until the old Player's saves have landed.

Only the first `SmithyCore` in a server runs these loops; requiring a copy (tests, load checks) never starts a second set. `SaveSpec` refuses to run during Play.

## Session lock

Loading takes the key's lock with `UpdateAsync`. If another session refreshed its lock in the last 5 minutes (normally the server the player just left, still saving), the new server checks again every 5 s and takes the lock over after 6 tries (about 30 s). A lock older than 5 minutes is taken at once. Each save first checks that this session still holds the lock; a session that lost it stops saving and kicks the player, so an older server can never overwrite newer progress or duplicate items. Store errors are retried three times with backoff. If the final release fails, the lock goes stale after 5 minutes.

If loading fails in a live server, the player is kicked with a rejoin message rather than playing on a blank profile. In Studio without DataStore access the session plays unsaved, with a warning.

## Versions

`Profiles.VERSION` is 1 (still 1 after 2026-10-24: `merges` and `staff` were additive, missing fields load as defaults). To change the saved shape: bump it and add `migrations[old]`, a function turning a version-`old` save into the next version. A save with a newer version than the server's is never loaded or overwritten (live: kicked to rejoin a newer server).

## Studio buttons

`DevPanel` (Studio only; bottom right behind a "Dev" button since 2026-10-23) adds **Skip tutorial** (all blueprints, both teaching commissions done) and **Reset progress**. Reset wipes the Studio save and, since 2026-10-23, starts you over in place instead of kicking (a kick ended the playtest): the old run stops saving, the leave clean-up runs (the plot goes), the key gets an empty record under this session's lock again, the join hooks (`SmithyCore.onRejoin`) hand out a new plot, you respawn with an empty bag, and every screen and client script restarts from its Starter copy.

## Checks

- `ServerStorage.Tests.SaveSpec` (Edit only): `print(require(game.ServerStorage.Tests.SaveSpec:Clone())())`, 38/38 on 2026-10-22, 47/47 after gems were added, 54/54 after the collection book, 66/66 after economy pass 1 (2026-10-23: the board's clock, order and delivery pay, polish ×1.10), 68/68 after Refinements 2 (settings, the crafter's pad), 71/71 after its second list (letters teach nothing, blueprint pads and blueprints agree, the crafter roster), 85/85 after [[Sessions/2026-10-24#Refinements 3]] (merges round trip and repairs, merge prices and luck, luck 3 and 7 still roll every rarity, staff round trip and bad roles/settings, the cashier rule, random order gaps; run with every Shared module fresh). Run it with a fresh clone of any edited Shared module swapped in: Studio's plugin VM caches required modules, and `fresh` only clones SmithyCore, Profiles and Commissions. It runs the lock rules over an in-memory store, save → JSON → load, and the commission rules.
- On 2026-10-22 the lock sequence was also run against the real Studio store with a throwaway key: wait on a live lock, take it over, refuse the old session, release, reload. The key was removed afterwards.
- Not yet: Play, rejoining, two servers, a published server ([[Development/Roadmap#3. Persistent progress]]).

Related: [[Design/Game Design Document#12. Technical notes (Roblox)]], [[Current Status]].

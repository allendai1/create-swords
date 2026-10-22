---
title: Saving
status: built 2026-10-22 — Play checks pending
type: development
updated: 2026-10-22
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
| `rack` | Ingot Rack and Finished Sword Rack contents |
| `displayed` | Swords on shop holders, keyed by the holder's path in the plot (`Shop/Displays/WallRack1/Slot2`) |
| `blueprints`, `discovered`, `upgrades` | Learned blueprints, metals ever collected (for the Material Index later), bought tycoon upgrades |
| `commissions`, `funnel` | Teaching commission status (`offered` / `active` / `done`) and first-session funnel steps already logged |

## Recovery rules

| Thing | On rejoin |
|---|---|
| Displayed swords | Back on the same holders; into the bag if that holder no longer exists or is taken |
| Racks | Back on the racks |
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

`Profiles.VERSION` is 1. To change the saved shape: bump it and add `migrations[old]`, a function turning a version-`old` save into the next version. A save with a newer version than the server's is never loaded or overwritten (live: kicked to rejoin a newer server).

## Studio buttons

`DevPanel` (Studio only) adds **Skip tutorial** (all blueprints, both teaching commissions done) and **Reset progress** (wipes the Studio save and kicks; rejoin as a new player).

## Checks

- `ServerStorage.Tests.SaveSpec` (Edit only): `print(require(game.ServerStorage.Tests.SaveSpec:Clone())())`, 38/38 on 2026-10-22. It runs the lock rules over an in-memory store, save → JSON → load, and the commission rules.
- On 2026-10-22 the lock sequence was also run against the real Studio store with a throwaway key: wait on a live lock, take it over, refuse the old session, release, reload. The key was removed afterwards.
- Not yet: Play, rejoining, two servers, a published server ([[Development/Roadmap#3. Persistent progress]]).

Related: [[Design/Game Design Document#12. Technical notes (Roblox)]], [[Current Status]].

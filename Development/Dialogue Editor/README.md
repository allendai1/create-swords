# Dialogue Editor

A local page for reading and editing every NPC line in Sell Swords!

## Open it

1. Start the `dialogue-editor` server (`.claude/launch.json`), or run `node "Development/Dialogue Editor/server.js"`.
2. Open http://127.0.0.1:8767

## Files

| File | What it is |
| --- | --- |
| `studio.json` | What the game has now. Written by `export.luau`; don't edit by hand. |
| `edits.json` | Allen's edits. The page autosaves it; it is deleted when the edits match the game. |
| `export.luau` | Run in Studio (Edit) through MCP `execute_luau` while the server runs. It requires a clone of `ReplicatedStorage.Shared` and posts `studio.json`. |

## Where each tab's text lives in Studio

| Tab | Source |
| --- | --- |
| Shop visits | `ReplicatedStorage.Shared.Customers` → `Customers.LINES` |
| Characters | `Customers.cast` (`client(...)`, `vip(...)`: name, sword, lines) |
| Mail senders | `ReplicatedStorage.Shared.Senders` → `Senders.list[*].lines` |
| Story quests | `ReplicatedStorage.Shared.Commissions` → `Commissions.list` |
| Tutorial hints | `StarterPlayer.StarterPlayerScripts.Guide` string literals (line numbers in the tab) |

## Wiring edits into Studio (Claude)

1. Read the Changes tab (or diff `edits.json` against `studio.json`).
2. Back up each module you touch into `ServerStorage.Legacy` (`<Name>_beforeDialogue_<MMDD>`).
3. Change the string literals in place with `multi_edit`; keep the comments. Added or removed lines are table entries; added keys on a cast member become new `key = { ... }` rows.
4. A tutorial hint replaces every occurrence of that text in `Guide`, including the comparisons (`text == "Put it on display"`).
5. Require a fresh clone of each changed module to prove it loads.
6. Rerun `export.luau`. When `studio.json` matches `edits.json`, press **Discard all edits** (or delete `edits.json`).

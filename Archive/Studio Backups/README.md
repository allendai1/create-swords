# Studio Backups

Backups taken out of the Studio place, as `.rbxm` files (one per item). The files stay on this computer: `.gitignore` keeps them out of the public repo.

## 2026-11-02 (audit cleanup)

- `Legacy 2026-11-02/`: the 352 items that were in `ServerStorage.Legacy` (old script copies, old towns, plots and drafts; 95,374 instances, 60,079 script lines). Numbered in name order.
- `ServerStorage strays 2026-11-02/`: `AnvilController_Backup`, two old `EtchPatterns` copies, two `ModuleScript`s (old NpcWalk copies) and `UIMegaPack` (the unused free UI pack, 38,521 script lines). Nothing in the game referenced any of them.

Every file was read back into Studio and matched its original (same instance count, same script source) before the originals were deleted. The one difference: `347 WorkspaceDrafts_2026_10_31.rbxm` lacks the great sword rig's `Humanoid.Status`, a runtime object Roblox never saves.

`ServerStorage.Legacy` stays in the place for new backups (`<Name>_before<Change>_<MMDD>`), and `Legacy.SharedV1` stays because `ServerStorage.Tests.AnvilSelfCheck` reads it.

## Restore one

In Studio, right-click `ServerStorage.Legacy` > **Insert from File...** and pick the `.rbxm`. Older versions of the whole place are also in Studio's File > Version History.

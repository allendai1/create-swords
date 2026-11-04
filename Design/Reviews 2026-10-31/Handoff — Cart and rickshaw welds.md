---
title: Handoff — Cart and rickshaw welds
type: handoff
updated: 2026-10-31
tags: [performance, handoff, create-swords]
---

# Handoff: cart and rickshaw welds (performance review #6)

Follows [[Design/Reviews 2026-10-31/Handoff — Performance fixes]] ("NOT done" #6). Everything was done in Edit with multi_edit; Play was never started.

## What changed

- **`ServerStorage.Rickshaw` (model):** Root is still the only anchored part. The 16 body parts are WeldConstraint'ed to Root. The first `Hub` is joined to Root by a new `Weld` named `WheelTurn` (on Root, C0 = the hub's rest offset), and the other 9 wheel parts are WeldConstraint'ed to that Hub. Every part except Root is now unanchored and Massless. The welds live in the model, so every clone works as it is.
- **`ServerScriptService.Rickshaws`:**
  - L40–42: `REST` = WheelTurn's C0 at rest.
  - Trip type: `wheels` is replaced by `turn: Weld`, plus `fade` and `shown`.
  - L98 `paint`: returns early when the fade hasn't changed, and writes a part only when its value changed.
  - L185 `place`: one `PivotTo`, then `t.turn.C0 = turn * REST` (the per-wheel CFrame loop is gone).
  - L255–256: the trip takes the clone's WheelTurn (the wheel-collecting loop is gone).
- **`ServerScriptService.DeliveryService`** (moves the cart):
  - Cart type gets `bed`, `parts`/`at` (every part's CFrame as built), `joints`, `turns`, `shown`. Wheels now store `c0` (their offset from the Bed).
  - L175 `paint`: writes a part only when its value changed.
  - L192 new `rig(c, on)`. On: a `Weld` from the Bed to each Wheel (C0 = c0), WeldConstraints from the Bed to the other 28 parts, everything except the Bed unanchored. Off: everything anchored again, the joints destroyed, each part `BulkMoveTo`'d to its built CFrame, and `WorldPivot = home`.
  - L305 `set`: spins the wheels through `weld.C0` (there are no welds at home, where odo is 0).
  - L333 `move`: `rig(c, true)` before any non-home frame. L365: `rig(c, false)` after the home placement.
  - The cart model in the plot template is unchanged. It is welded only at runtime, so TycoonController's build-in still flies its anchored parts.

## Numbers (Edit, on clones)

| | Before | After |
|---|---|---|
| Rickshaw, CFrame writes per `place` | 37 (27 parts + 10 wheel writes) | 1 (Root) + 1 Weld.C0 |
| Cart, CFrame writes per `set` | 33 (31 parts + 2 wheels) | 1 (Bed) + 2 Weld.C0 |
| Rickshaw `paint` outside fades | every tracked part each frame (rickshaw + puller + rider, about 60) | 0 |
| Fades (both) | every part each frame | only parts whose value changed (always-invisible parts and hidden crates are skipped) |

**Checks:**
- Rickshaw, fresh clone: 5 PivotTo + C0 steps. All 27 parts followed (body error 0, wheel error 1e-5 against the old formula).
- Cart clone: 5 rigged steps. The parts followed, with wheels spinning (error under 3e-5). After going home and unrigging, 31 of 31 parts were exactly at their built CFrames, all were anchored, there were 0 joints, and the pivot equalled `home`.
- All clones and compile modules were removed afterwards. The template cart has 0 joints.

**Compile:** Rickshaws OK, DeliveryService OK (the `return function() … end` wrapper).

## Test in Play

1. Rickshaw Bay: the rickshaw runs in, its wheels turn and it fades in. It parks square, the customer steps out, and on leaving it runs off and fades. Nothing is left floating or left behind.
2. Delivery: send the cart. It rolls out in one piece with the wheels turning, and fades out by the gate. The walk back and the backing in are smooth. When parked, the cart sits exactly where it was built, is solid, and the crates show or hide correctly.
3. Rejoin or join a server while the cart is out: it appears mid-trip, intact.
4. Buy Delivery on a new plot: the cart still builds itself in piece by piece.
5. Developer Console: lower server send (`DataSendKbps`) while a cart or rickshaw is moving.

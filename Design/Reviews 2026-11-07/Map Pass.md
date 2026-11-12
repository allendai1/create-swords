---
title: Map Pass
type: review
updated: 2026-11-07
tags: [review, map, create-swords]
---

# Map Pass (2026-11-07)

A whole-map check after today's moves (plots 30 apart, the 32-wide street, 11.6 walls with stone caps, the shop 13 left, the anime forest, square posts and eaves), none of which had been checked together. Run in Edit through the Studio MCP while Allen was away; skills roblox-collaboration-mode, roblox-building, lihfolk-worldbuilding, roblox-lighting. Nothing was played. The only changes are the 24 parts under [[#Fixed]] (z-fight trims of 0.04–0.10 studs, each part keeping its old CFrame and Size as `MapPass1107_CFrame` / `MapPass1107_Size` attributes; ChangeHistory waypoints "MapPass1107 before fixes" / "MapPass1107 z-fight fixes"). The Edit camera was set back to Fixed, FOV 70 at the end. Two other agents were working at the same time (CastShadow/CanQuery on the forest, mountains and dressing; StarterGui), so the counts here are from about 14:30–15:20.

World studs throughout. The plot template `Workspace.Plot` sits on lot N2 (pivot 640, 0.5, −272); plot −z is the street. Village.Lots.Pad centres: N1 (524, −286), N2 (638, −286), N3 (752, −286), S1 (528, −114), S2 (642, −114), S3 (756, −114), each 84 × 124, top 0.16. Road x 392.5–857.5, z −216…−184, top 0.2; curbs at z −218…−216 and −184…−182, top 0.5; walkways top 0.3; grass paving top 0.12; plaza x 857.5–909.5, top 0.25.

## Summary

1. **Coplanar pairs, village** (Street, Dressing, Landmarks, Houses, Lots; 1,573 visible parts in one list): 3,282 found. 3,277 are inside the 16 street-lamp models (Allen's Toolbox lamp, 64 parts and about 204 same-plane slivers each; 0 between a lamp and the street). The other 5 (wall caps flush with their wall's end face) are fixed: 0 left outside the lamps.
2. **Backdrop**: 134 blocks, 0 pairs, 0 blocks floating free. Skyline (highest block top per 2° of azimuth) 12.0–30.1° from the street's middle, 13.1–44.9° inside the west gate, 14.4–47.5° inside the east gate: no sector under 5°, so the 10-31 west gap is closed.
3. **Plot, Starter state** (1,329 visible parts + 19 village parts round N2): 20 found, 8 fixed (sign-frame post tops), 12 accepted (8 cart bed slivers of 0.03, 4 edge contacts of 0.02). **Upgraded state** (a nil-parented clone with the 12-stud push applied as `TycoonService.pushWorkshopBack` does; 1,606 + 19): 40 found, 28 fixed (the 8 above, 6 shop side posts 0.05 into their UpperPosts, 6 back UpperPosts that the pushed workshop posts ran 0.10 into), the same 12 accepted. Plot × village: 0 in both states.
4. **Lot seams**, the template cloned onto all six PlotSlots: 0 plot × village pairs at any lot (640 plot perimeter parts against 139–152 village parts each).
5. **Floating**: 2 real things. `Village.Atmosphere.ForestStones` (Allen's five kept stones) hang 13.2 studs over the grass at (882, 13–20, −231), and one `AnimeTree` (kind 3) stands 11.7 studs above the grass at the north lane end (569.6, 56.4, −359.8). Everything else the ray test raised is a spanning or hanging member of a grounded thing (gate roofs, lintels, signs, wall racks, tie beams, the stacked crate).
6. **Sunk**: 0 visible parts with their top under the ground. Trees: 124 of 812 sit 1.0–2.9 studs deeper than their kind's ground line (by kind the mean is 0.3–0.9 deeper, a deliberate sink); kinds 3, 5 and 7 carry 11.4 / 8.0 / 14.1 studs of mesh below their ground line at scale 1 (the pack's own geometry), which is why their lowest points read 5–19 studs under.
7. **Trees out of place**: 0 on a plot pad, 0 on the road, 0 in the street band between the walls, 0 on the plaza, 0 in an end house.
8. **Bounds**: the inner ring (EdgeGuards, gate doors, the two gate guards) and the outer `Bound` ring are closed on all 8 sides at y 3, 6, 9 and 12 (1-stud samples, no run of 2 uncovered); the gate guards (3.4 × 11.3 × 29.4 at x 422.1 and 905.9, y 12.7–24) sit over colliding doors.
9. **Walkable**: 0 unanchored parts a player stands on (4 unanchored in all: the ore lever's knob and arm, the lever hand's two accessory handles); 0 invisible colliders in the street band; `Plot.PlayerSpawn` is still the 0.32-stud invisible step from 10-31.
10. **Leftovers**: `Workspace.Compare_1107` is no longer in the place (0 instances by that name anywhere). The six origin bits and the x-2000 `Smithy` folder are all below the mountain skyline from the street and both gates; AuxScene's 5 parts are still unanchored.

## Checked

| Region | Parts checked | Pairs found | Fixed | Accepted and why |
|---|---|---|---|---|
| Street: road, 2 curbs, 4 paving, 12 walkways, StreetFill, 16 lamps | 1,041 visible | 3,277 | 0 | 3,277 inside the 16 `Street.StreetLights.StreetLight` models (64 Parts each, about 204 slivers of 0.04–1.7 studs at y 8.4–10.3 inside the lamp head; one lamp alone gives 204). Allen's model (2026-11-01 "use the streetlights model i added"), so not edited. 0 pairs among road, curbs, paving and walkways; 0 between a lamp and the walkway, curb or paving (each lamp checked with everything within 2 studs). |
| Dressing: 8 gap walls with caps, 8 lantern strings, 6 cherry blossoms, 4 stone lanterns, 4 yatai, 2 handcarts, yagura, well, notice board | 260 visible | 5 | 5 (4 caps, see Fixed) | — |
| Landmarks: both gates, plaza, StyleAdd | 51 | 0 | | GatePosts are cylinders (no faces to check); the plaza's edge meets the road edge to edge. |
| Houses: EndN1, EndN2, EndS1, EndS2 | 215 | 0 | | OuterN is an empty Model. |
| Lots: 6 pads | 6 | 0 | | Pads top 0.16 against grass paving 0.12, walkway 0.3, road 0.2. |
| Cross-folder, village | all 1,573 in one list | 0 outside a folder | | |
| EdgeGuards, Bound | 12 invisible | not run | | Transparency 1: nothing to fight. |
| Backdrop.Mountains | 134 | 0 | | Also 0 blocks with a gap > 0.5 under them that touch no other block. |
| Plot, Starter (everything whose upgrade chain does not pass UpgradedStore: left out BigSwordStand 1–3, Cashier, DisplayTable5/6, WallRack3/4, the Zanbatō/Claymore/Flamberge blueprints, Shop.Upgraded) + village within 8 studs of the N2 pad | 1,329 + 19 | 20 | 8 | 8 `DeliveryBay.Cart` Bed/Side/End slivers of 0.03 (known since 10-28, 0.02 before the 1.6× cart); 4 `EtchingTable`/`EtchingTable2 StandingFrame.Post | Backboard` edge contacts 0.02 wide (the board's end touches the post's face). |
| Plot, Upgraded (clone: Shop.Starter and Grounds.PavingStrip removed as UntilUpgrade; Workshop.Shell, SwordRack, SwordRack2, WallRack5, Decor.Wall and 3 pads pushed 12) + the same 19 | 1,606 + 19 | 40 | 28 | the same 12 |
| Box pass, faceless parts (meshes, cylinders) against other things, overlap > 0.15 on all axes | 864 (S) / 909 (U) | 41 pairs | 0 | listed under Seen: cherry trunks into walls, hearths into the paving (by design), the dummy's feet. |
| Lot seams, template cloned onto PlotSlotN1…S3: Fence, Grounds, DeliveryBay, Parking, both shells, Leaderboard, Workshop, Showcase1–3 against village parts within 6 studs | 640 + 139–152 per lot | 0 plot × village (731–741 within one side per lot: the two shells over each other in Edit, the pairs above) | 0 | |
| Re-run after the fixes | village without lamps 549 → 0; Starter 1,348 → 12; Upgraded 1,625 → 12 | | | |

Other checks, each with its own script below: the bounds scan (8 segments, 1,312 samples × 4 heights), the floating pass (217 things, 3,308 parts rayed with `BruteForceAllSlow`, since the forest, mountains and part of the dressing are CanQuery off now), the buried-part test (same parts, ground from an Include ray over Baseplate, street, plaza, pads and plot grounds; Terrain has 0 cells), the tree pass (812 trees by kind), the footprint tests, the leftovers' sight lines and the skyline.

### How it was run

`ServerStorage.Builders.coplanar_check` was cloned and required fresh in every call (`local clone = SS.Builders.coplanar_check:Clone(); local CC = require(clone); clone:Destroy()`). Visible = `Transparency < 1`. Each snippet below is the code as run (the preamble above and the `aabb` helper are repeated where they were used).

**Village, one list, pairs tallied by folder** (the full run; the "without lamps" run is the same with `not (d:IsDescendantOf(V.Street.StreetLights) and d.Name ~= "StreetFill")` added to the filter):

```lua
local V = workspace.Village
local list, counts = {}, {}
local function add(root, label)
	local n = 0
	if root:IsA("BasePart") and root.Transparency < 1 then table.insert(list, root); n += 1 end
	for _, d in root:GetDescendants() do
		if d:IsA("BasePart") and d.Transparency < 1 then table.insert(list, d); n += 1 end
	end
	counts[label] = n
end
for _, name in { "Street", "Dressing", "Landmarks", "Houses", "Lots" } do add(V[name], name) end
local hits = CC.check(list)
local function region(path) return path:match("^[^.]+%.[^.]+%.([^.]+)") or path end
local byRegion = {}
for _, h in hits do
	local pa, rest = h:match("^(.-) | (.+)$")
	local pb = rest and rest:match("^(.-)  %(") or ""
	local ra, rb = region(pa or ""), region(pb)
	local key = ra == rb and ra or (ra < rb and (ra .. "+" .. rb) or (rb .. "+" .. ra))
	byRegion[key] = (byRegion[key] or 0) + 1
end
```

**Lamps against their surroundings** (per lamp: its parts plus every visible Street/Dressing/Lots/Houses/Landmarks part within 2 studs of its box; pairs kept only when exactly one side is inside `StreetLights`): 0 over 16 lamps.

**Plot, Starter state** (post-store items from `ReplicatedStorage.Shared.Upgrades` by parsing `id = "…"` / `after = …` and closing over "UpgradedStore"):

```lua
local src = game.ReplicatedStorage.Shared.Upgrades.Source
local after = {}
for line in (src .. "\n"):gmatch("(.-)\n") do
	local id = line:match('id%s*=%s*"([%w_]+)"')
	if id then
		local l = {}
		local blk = line:match('after%s*=%s*(%b{})')
		if blk then for a in blk:gmatch('"([%w_]+)"') do table.insert(l, a) end
		else local one = line:match('after%s*=%s*"([%w_]+)"'); if one then table.insert(l, one) end end
		after[id] = l
	end
end
local memo = {}
local function isPost(id)
	if id == "UpgradedStore" then return true end
	if memo[id] ~= nil then return memo[id] end
	memo[id] = false
	for _, a in after[id] or {} do if isPost(a) then memo[id] = true; break end end
	return memo[id]
end
local plot = workspace.Plot
local function excludedS(d)
	local a = d
	while a and a ~= plot do
		local u = a:GetAttribute("Upgrade")
		if u and isPost(u) then return true end
		a = a.Parent
	end
	return false
end
local list = {}
for _, d in plot:GetDescendants() do
	if d:IsA("BasePart") and d.Transparency < 1 and not excludedS(d) then table.insert(list, d) end
end
local V = workspace.Village
local pad
for _, p in V.Lots:GetChildren() do if p.Name == "Pad" and (p.Position - Vector3.new(638, 0, -286)).Magnitude < 3 then pad = p end end
local plo, phi = CC.aabb(pad)
plo, phi = plo - Vector3.new(8, 8, 8), phi + Vector3.new(8, 8, 8)
for _, root in { V.Street, V.Dressing, V.Landmarks, V.Houses, V.Lots } do
	for _, d in root:GetDescendants() do
		if d:IsA("BasePart") and d.Transparency < 1 then
			local a, b = CC.aabb(d)
			if a.X <= phi.X and plo.X <= b.X and a.Y <= phi.Y and plo.Y <= b.Y and a.Z <= phi.Z and plo.Z <= b.Z then table.insert(list, d) end
		end
	end
end
local hits = CC.check(list) -- then split by whether each path starts with Workspace.Plot
-- box pass: parts without checkable faces (not a Block Part or WedgePart) against parts of another thing
local roots = { [plot] = true, [plot.Shop] = true, [plot.Shop.Displays] = true, [plot.Shop.Decor] = true, [plot.Smithy] = true, [plot.Parking] = true, [plot.WorldStore] = true, [plot.DeliveryBay] = true, [V.Street] = true, [V.Street.StreetLights] = true, [V.Dressing] = true, [V.Landmarks] = true, [V.Houses] = true, [V.Lots] = true }
local function thingOf(p) local a = p; while a.Parent and not roots[a.Parent] do a = a.Parent end; return a end
local function hasFaces(p) return (p:IsA("Part") and p.Shape == Enum.PartType.Block) or p:IsA("WedgePart") end
local boxes = {}
for i, p in list do local lo, hi = CC.aabb(p); boxes[i] = { lo, hi, thingOf(p), hasFaces(p) } end
local res = {}
for a = 1, #list do
	local ba = boxes[a]
	for b = a + 1, #list do
		local bb = boxes[b]
		if (not ba[4] or not bb[4]) and ba[3] ~= bb[3] then
			local ox = math.min(ba[2].X, bb[2].X) - math.max(ba[1].X, bb[1].X)
			if ox > 0.15 then
				local oy = math.min(ba[2].Y, bb[2].Y) - math.max(ba[1].Y, bb[1].Y)
				local oz = math.min(ba[2].Z, bb[2].Z) - math.max(ba[1].Z, bb[1].Z)
				if oy > 0.15 and oz > 0.15 then table.insert(res, { ox * oy * oz, a, b, math.min(ox, oy, oz) }) end
			end
		end
	end
end
```

**Plot, Upgraded state** (a clone outside the DataModel; the template never moves):

```lua
local copy = workspace.Plot:Clone()
for _, d in copy:GetDescendants() do
	if d.Parent and d:GetAttribute("UntilUpgrade") == "UpgradedStore" then d:Destroy() end
end
local SHIFT = 12
local STRIP = { cx = -13, x = 25, z0 = -19.5, z1 = -18 + SHIFT + 0.5 } -- TycoonService's STRIP
local pivot = copy:GetPivot()
local function inStrip(at) local l = pivot:PointToObjectSpace(at); return math.abs(l.X - STRIP.cx) <= STRIP.x and l.Z >= STRIP.z0 and l.Z <= STRIP.z1 end
local d = pivot:VectorToWorldSpace(Vector3.new(0, 0, SHIFT))
local moving = {}
local shell = copy.Workshop:FindFirstChild("Shell")
if shell then table.insert(moving, shell) end
for _, m in copy.Smithy:GetChildren() do
	local at = if m:IsA("Model") then m:GetBoundingBox().Position elseif m:IsA("BasePart") then m.Position else nil
	if at and inStrip(at) then table.insert(moving, m) end
end
for _, m in copy.Shop.Displays:GetChildren() do if m:GetAttribute("BackWall") then table.insert(moving, m) end end
for _, m in copy.Shop.Decor:GetChildren() do if m:GetAttribute("BackWall") then table.insert(moving, m) end end
for _, pad in copy.Pads:GetChildren() do if pad:GetAttribute("Workshop") and inStrip(pad.Position) then table.insert(moving, pad) end end
for _, x in moving do
	if x:IsA("Model") then x:PivotTo(x:GetPivot() + d) elseif x:IsA("BasePart") then x.CFrame += d end
end
local list = {}
for _, p in copy:GetDescendants() do
	if p:IsA("BasePart") and p.Transparency < 1 then table.insert(list, p) end
end
-- + the same 19 village parts round the N2 pad, then CC.check(list), the box pass, copy:Destroy()
```

**Lot seams**:

```lua
local V = workspace.Village
local slots = {}
for _, s in V.Lots:GetChildren() do if s.Name:match("^PlotSlot") then table.insert(slots, s) end end
local villageParts = {}
for _, root in { V.Street, V.Dressing, V.Landmarks, V.Houses, V.Lots } do
	for _, d in root:GetDescendants() do if d:IsA("BasePart") and d.Transparency < 1 then table.insert(villageParts, d) end end
end
for _, slot in slots do
	local copy = workspace.Plot:Clone()
	copy:PivotTo(slot.CFrame) -- as PlotService line 166
	local list = {}
	local function addAll(root)
		if root:IsA("BasePart") and root.Transparency < 1 then table.insert(list, root) end
		for _, d in root:GetDescendants() do if d:IsA("BasePart") and d.Transparency < 1 then table.insert(list, d) end end
	end
	for _, r in { copy.Fence, copy.Grounds, copy.DeliveryBay, copy.Parking, copy.Shop.Starter, copy.Shop.Upgraded, copy.Leaderboard, copy.Workshop } do addAll(r) end
	for _, m in copy.Shop.Displays:GetChildren() do if m.Name:match("^Showcase") then addAll(m) end end
	local lo, hi -- box of the plot parts, grown by 6
	for _, p in list do
		local a, b = CC.aabb(p)
		lo = lo and Vector3.new(math.min(lo.X, a.X), math.min(lo.Y, a.Y), math.min(lo.Z, a.Z)) or a
		hi = hi and Vector3.new(math.max(hi.X, b.X), math.max(hi.Y, b.Y), math.max(hi.Z, b.Z)) or b
	end
	lo, hi = lo - Vector3.new(6, 6, 6), hi + Vector3.new(6, 6, 6)
	for _, p in villageParts do
		local a, b = CC.aabb(p)
		if a.X <= hi.X and lo.X <= b.X and a.Y <= hi.Y and lo.Y <= b.Y and a.Z <= hi.Z and lo.Z <= b.Z then table.insert(list, p) end
	end
	local hits = CC.check(list) -- split: one path starting "Plot" and one "Workspace.Village" = cross
	copy:Destroy()
	task.wait()
end
```

**Bounds ring** (a sample is covered when a CanCollide part's box reaches within 2.5 studs of the plane and 0.5 of the height; colliders from Street, Dressing, Landmarks, Houses, Lots, EdgeGuards, Plot and Village's own parts):

```lua
local function scan(label, axis, v, a, b)
	local half = 2.5
	local cands = {}
	for _, c in colliders do
		local lo, hi = c[1], c[2]
		if axis == "x" then
			if lo.X <= v + half and hi.X >= v - half and lo.Z <= b and hi.Z >= a then table.insert(cands, c) end
		else
			if lo.Z <= v + half and hi.Z >= v - half and lo.X <= b and hi.X >= a then table.insert(cands, c) end
		end
	end
	local gaps = {}
	for _, y in { 3, 6, 9, 12 } do
		local run, runStart = 0, nil
		for t = a, b, 1 do
			local px, pz = (axis == "x") and v or t, (axis == "x") and t or v
			local covered = false
			for _, c in cands do
				local lo, hi = c[1], c[2]
				if lo.Y <= y + 0.5 and hi.Y >= y - 0.5 and lo.X <= px + half and hi.X >= px - half and lo.Z <= pz + half and hi.Z >= pz - half then covered = true; break end
			end
			if not covered then
				if run == 0 then runStart = t end
				run += 1
			else
				if run >= 2 then table.insert(gaps, ("y%d %s=%g..%g (%d studs)"):format(y, axis == "x" and "z" or "x", runStart, t - 1, run)) end
				run = 0
			end
		end
		if run >= 2 then table.insert(gaps, ("y%d %s=%g..%g (%d studs)"):format(y, axis == "x" and "z" or "x", runStart, b, run)) end
	end
end
scan("inner west x=422.5", "x", 422.5, -360, -40); scan("inner east x=905.5", "x", 905.5, -360, -40)
scan("inner north z=-360", "z", -360, 422.5, 905.5); scan("inner south z=-40", "z", -40, 422.5, 905.5)
scan("outer west x=392.5", "x", 392.5, -398, -2); scan("outer east x=915.5", "x", 915.5, -398, -2)
scan("outer north z=-398", "z", -398, 392.5, 915.5); scan("outer south z=-2", "z", -2, 392.5, 915.5)
```

Result: candidate colliders 16 / 14 / 5 / 5 / 4 / 3 / 4 / 4, gaps of 2+ samples: none on any side at any height.

**Floating and buried** (the first version started the ray 0.02 above each bottom, which begins inside thin slabs a part is sunk into and reports it floating; this version starts 1 stud up, so a sunk part reads as supported). A "thing" is a child of each region folder (a lamp, a stall, a station, a fence part); a thing floats when none of its visible anchored parts has anything within 0.1 below its bottom centre:

```lua
local rp = RaycastParams.new()
rp.FilterType = Enum.RaycastFilterType.Exclude
rp.RespectCanCollide = false
rp.BruteForceAllSlow = true -- the forest, mountains and part of the dressing are CanQuery off
local function gapBelow(part)
	local lo = aabb(part)
	rp.FilterDescendantsInstances = { part }
	local o = Vector3.new(part.Position.X, lo.Y + 1, part.Position.Z)
	local r = workspace:Raycast(o, Vector3.new(0, -(lo.Y + 41), 0), rp)
	if r then return lo.Y - r.Position.Y, r.Instance end
	return 999, nil
end
-- things: children of Street, Street.StreetLights, Dressing, Landmarks, Landmarks.StyleAdd, Houses, Lots, Atmosphere.ForestStones,
-- Plot.Smithy, Shop.Displays, Parking, WorldStore, DeliveryBay, Fence, Grounds, Leaderboard, Workshop, both shells' children, CashierCounter
for _, t in things do
	local parts = {} -- visible, anchored BaseParts of the thing
	local minGap, support = 999, nil
	for _, p in parts do
		local gap, hit = gapBelow(p)
		if gap < minGap then minGap, support = gap, hit end
		if gap > 0.5 and gap < 999 and hit and hit.Transparency >= 1 and not hit:IsDescendantOf(P.Pads) then -- rests over an invisible part
		end
	end
	if minGap > 0.1 then -- floating thing
	end
end
-- buried: a visible anchored part whose box top is under the ground surface at its centre; ground = an Include ray over
-- Baseplate, Landmarks.Plaza, DeliveryBay.Yard, Street's direct BaseParts, Lots, Plot.Grounds, from y 80 down 120
-- Backdrop: a block with gapBelow > 0.5 counts as floating only if no other block's box overlaps its box
```

**Trees by kind** (kind matched by the tree's `GroundToPivot` attribute; scale = the tree's box height over the kind's; "ground line" = where the kind's pack ground (y 157.41) lands after scaling, against the real ground under the pivot):

```lua
local PACK_GROUND = 157.41
local kinds = {}
for _, k in game.ServerStorage.Nature.AnimeTreeKinds:GetChildren() do
	local lo, hi = aabbOf(k)
	kinds[k.Name] = { g2p = k:GetAttribute("GroundToPivot"), h = hi.Y - lo.Y, under = PACK_GROUND - lo.Y }
end
for _, tree in V.Atmosphere.Forest:GetChildren() do
	local g2p = tree:GetAttribute("GroundToPivot")
	local kname
	for name, k in kinds do if g2p and math.abs(k.g2p - g2p) < 0.01 then kname = name end end
	local lo, hi = aabbOf(tree)
	if lo and kname then
		local k = kinds[kname]
		local scale = (hi.Y - lo.Y) / k.h
		local pv = tree:GetPivot().Position
		local gy = groundY(pv.X, pv.Z)
		local baseHeight = (lo.Y + k.under * scale) - gy -- 0 = the kind's ground line on the real ground
	end
end
-- footprints: pivot x,z inside a Lots.Pad box, the road band (392.5..857.5, -216..-184), the street band (422.5..905.5, -228..-172),
-- the plaza (857.5..909.5, -228..-172) or an end house's box
```

**Skyline** (per 2° of azimuth, the highest Backdrop block top along a horizontal ray from the eye; 0° = +x east, 90° = +z south, 180° = west, 270° = north; sectors of 10° report min/max):

```lua
local function skyline(eye, set)
	local res = {}
	for az = 0, 358, 2 do
		local r = math.rad(az)
		local dx, dz = math.cos(r), math.sin(r)
		local best = 0
		for _, b in set do
			local tmin, tmax = -1e9, 1e9
			for _, ax in { { eye.X, dx, b.lo.X, b.hi.X }, { eye.Z, dz, b.lo.Z, b.hi.Z } } do
				local o, d, l, h = ax[1], ax[2], ax[3], ax[4]
				if math.abs(d) < 1e-9 then
					if o < l or o > h then tmin, tmax = 1, 0 end
				else
					local t1, t2 = (l - o) / d, (h - o) / d
					if t1 > t2 then t1, t2 = t2, t1 end
					tmin, tmax = math.max(tmin, t1), math.min(tmax, t2)
				end
			end
			if tmax >= math.max(tmin, 0) then
				local e = math.deg(math.atan2(b.hi.Y - eye.Y, math.max(tmin, 0.5)))
				if e > best then best = e end
			end
		end
		res[az] = best
	end
	return res
end
-- eyes: street middle (640, 5.5, -200), inside the west gate (435, 5.5, -200), inside the east gate (895, 5.5, -200)
```

**Fixes** (every part keeps its old CFrame and Size as attributes first):

```lua
local function fixPart(p, newSize, newCFrame, note)
	if p:GetAttribute("MapPass1107_CFrame") == nil then
		p:SetAttribute("MapPass1107_CFrame", p.CFrame)
		p:SetAttribute("MapPass1107_Size", p.Size)
	end
	p.Size = newSize
	p.CFrame = newCFrame
end
-- 1. sign-frame posts (Y up): Size - (0, 0.04, 0), CFrame - (0, 0.02, 0)
-- 2. Upgraded Shell.Post, 1.04 wide, top 14.45 (X up): Size.X - 0.05, CFrame - (0, 0.025, 0)
-- 3. Upgraded Roof.UpperFrame.UpperPost with box z < -265, bottom 14.40 (Y up): Size - (0, 0.10, 0), CFrame + (0, 0.05, 0)
-- 4. Dressing.GapWall.WallCap whose box end equals the Wall's box end (|dx| < 0.001): 0.04 shorter at that end, centre moved 0.02 the other way
```

## Fixed

24 parts, all axis-aligned, nothing moved sideways. Undo: set each part's CFrame and Size back from its `MapPass1107_CFrame` / `MapPass1107_Size` attributes, or step back to the "MapPass1107 before fixes" waypoint.

| Part | Fought | Old → new Size | Old → new position |
|---|---|---|---|
| `Plot.Smithy.EtchingTable.StandingFrame.Post` ×2 (600.03, −298.75 / −291.61) | its `Beam` (9.98–10.43): post top 10.43 flush with the beam top, 0.5 × 0.5 | 0.5, 10.19, 0.5 → 0.5, 10.15, 0.5 | y 5.335 → 5.315 (top 10.39, bottom 0.24 kept) |
| `Plot.Smithy.EtchingTable2.StandingFrame.Post` ×2 (600.17, −278.31 / −284.01) | same | same | same |
| `Plot.Smithy.PolishStation.StandingFrame.Post` ×2 (601.59, −311.45 / −304.95) | same | same | same |
| `Plot.Smithy.PolishStation2.StandingFrame.Post` ×2 (601.59, −326.45 / −319.95) | same | same | same |
| `Plot.Shop.Upgraded.Shell.Post` ×6, the 1.04-wide side posts at x 629.25 / 676.75, z −239 / −249 / −259 | its `Roof.UpperFrame.UpperPost` (bottom 14.40): the post's top at 14.45 ran 0.05 into it with both side faces on the same planes (12 pairs of 0.05 × 1.04) | 13.45, 1.04, 1.04 → 13.40, 1.04, 1.04 (X is up) | y 7.725 → 7.700 (top 14.40, bottom 1.00 kept) |
| `Plot.Shop.Upgraded.Shell.Roof.UpperFrame.UpperPost` ×6, the back row at z −266, x 629.25 / 640 / 648.1 / 656.2 / 666 / 676.75 | `Plot.Workshop.Shell.Post` after the Upgraded Store's 12-stud push (top 14.50): the UpperPost's bottom at 14.40 took the workshop post 0.10 into it, side faces shared (8 pairs of 1.04 × 0.10). In Edit the workshop stands 12 studs forward, so these hang over nothing either way. | 1.04, 8.64, 1.04 → 1.04, 8.54, 1.04 | y 18.72 → 18.77 (bottom 14.50, top 23.04 kept) |
| `Village.Dressing.GapWall.WallCap` at 798.0–826.4 (south-east end wall) | its `Wall` (1.72–10.72): the cap (10.67–11.6) is 0.05 into the wall top by design, and at both ends its end face was on the wall's end plane (0.05 × 1.10 at x 798.0 and 826.4) | 28.4 → 28.32 long | centre 812.2 kept (0.04 off each end) |
| `WallCap` at 453.6–484.7 (south-west end wall) | same at x 453.6, the house end | 31.1 → 31.06 | x 469.15 → 469.17 |
| `WallCap` at 453.6–480.7 (north-west end wall) | same at x 453.6 | 27.1 → 27.06 | x 467.15 → 467.17 |
| `WallCap` at 795.3–826.4 (north-east end wall) | same at x 826.4 | 31.1 → 31.06 | x 810.85 → 810.83 |

Re-run after: village without the lamps 549 parts, 5 → 0; Starter 1,348 parts, 20 → 12; Upgraded 1,625 parts, 40 → 12 (the 12 are the accepted cart slivers and edge contacts in both). Readback: all 8 frame posts top 10.390 / bottom 0.240; all 6 side posts top 14.400 / bottom 1.000; all 6 back UpperPosts bottom 14.500 / top 23.040.

![[Design/Reviews 2026-11-07/Map Pass/frame-post-top.jpg]]
*The Etching Table's sign frame after the trim: one beam over the posts. Camera (607, 12.5, −293) → (600, 10.3, −295.3).*

![[Design/Reviews 2026-11-07/Map Pass/cap-house-end.jpg]]
*The south-west end wall's stone cap meeting house EndS2 under its eave. Camera (461, 14, −187) → (453.6, 11, −173.5).*

## Seen, not changed

- **Allen's street lamp** (`Village.Street.StreetLights.StreetLight` ×16, 64 Parts each, 1,024 parts, all casting shadows): about 204 same-plane slivers inside each head (0.04–1.7 studs, y 8.4–10.3). The only z-fighting left in the village; it is his model (2026-11-01), so left as is. A cleaned copy (one mesh or union per head) would also drop 1,000 parts and 1,000 shadow casters.
- **`Village.Atmosphere.ForestStones`** (Allen's five kept stones): box (874.3, 13.3, −237.6)–(889.8, 20.5, −226.9), 13.2 studs over the grass north of the plaza, in the lantern string's line. They sat at (938.7, 13.9, −198.4) when they came out of a tree this morning, so they have been moved since and still carry that tree's height. ![[Design/Reviews 2026-11-07/Map Pass/forest-stones-floating.jpg]] *Camera (858, 9, −196) → (882, 16.5, −231).*
- **One floating tree**: `Village.Atmosphere.Forest.AnimeTree` (kind 3, scale 0.99) pivot (569.6, 56.4, −359.8), its base 11.7 studs over the grass (ground 0.12), right on the inner guard line at the north lane end. It is one of this morning's 53 fill trees; the ground ray there probably met `Houses.OuterN` before it was emptied.
- **Trees sunk deeper than their kind**: 124 of 812 by 1.0–2.9 studs (the deepest, kind 1 at (951.2, 38.1, −440.3), 2.87); by kind the mean sink is 0.27–0.85. Kinds 3, 5, 7 carry 11.4 / 8.0 / 14.1 studs of mesh under their own ground line, so 344 trees have their lowest point more than 3 under the ground by the pack's design, not by placement. Trees: 812 (814 this morning); kind counts 118 / 126 / 121 / 93 / 120 / 130 / 104.
- **Cherry blossoms in the walls** (box pass): the N2 and S2 `Dressing.CherryBlossom` trunk meshes (`Cherry blossom 1.Dead tree-squid game.MeshPart`, `pink tree.Leaf`) overlap `GapWall.Wall` and `WallBase` by 1.1–1.6 studs on all axes, the plot's corner `Fence.Pillar` by 2.6 and the `Street.Curb` by 0.38. They moved 8 studs out along their plot's −x today; a mesh box is wider than its trunk, so look at the N2 tree (x 575–602, z −236…−204) in Studio before judging.
- **Hearths and the dummy**: `Smithy.Anvil2/3/4.Hearth` and `WorkshopFittings.Hearth` run 0.2 into `Grounds.Paving` and 0.16 into the lot pad (by design, 10-31); `Smithy.TrainingDummy.Feet` 0.2 into the paving.
- **Not flagged, noted**: the 8 Upgraded front posts (1.17 wide) also stop at 14.45 under 1.04-wide UpperPosts, but their faces are on different planes, so nothing fights; `Workshop.Shell.Post` tops (14.5) meet the Starter roof in the Starter state with no shared plane.
- **End-wall caps and today's 1.3 rule**: the south-east cap (798.04–826.36) is not trimmed 1.3 short of lot S3's corner pillar (796.7–799.3), unlike the other seven pillar ends, and the south middle cap (685.3–714.7) runs 0.7 past its wall's end (714) into S3's other pillar. In game both ends are inside the pillars, so nothing shows; in Edit the empty lot shows the cap end.
- **`Plot.PlayerSpawn`**: 10 × 0.3 × 5.7, Transparency 1, CanCollide on, top 0.56 over the 0.24 paving: the 0.32-stud invisible step from the 10-31 yard review, still there.
- **Invisible colliders** (19): the station prompt parts (`EtchingTable/2.Top`, `PolishStation/2.Top`, `Forge/2/3.Base`, `Anvil/2/3/4.Face`, `OreRoller.Stand1–6.Ore`), the lever hand's `HumanoidRootPart`, the spawn above. None in the street band.
- **Unanchored** (4): `OreRoller.Lever.Knob` and `.Arm` (the moving lever), the lever hand's two accessory `Handle`s.
- **Ground-like parts a player passes through**: 24 `Houses.End*.StyleAdd.Plinth` (0.7 × 1.89 × 1.89 post bases, CanCollide off) and the 3 `Parking.Bay*.Slab` (8.5 × 0.1 × 3.8, top 0.24, 0.04 over the road, CanCollide off).
- **Stacked crate**: the top `DeliveryBay.Crate` (598.5, 3.45, −251.2) sits 0.02 into the crate below with half its footprint past that crate's edge (−251.23), so its bottom centre hangs over the lower crate's corner.
- **Things that stand over invisible markers** (21 parts, all inside grounded things): sword-rack rails over their `NavBlock`s, ingot-rack shelves, lanterns and roof caps over `Lots.PlotSlotN2` (a non-colliding marker at y 0–1), the cart over `CartSpot`. Nothing stands on an invisible floor.
- **`Village.Street.StreetLights.StreetFill`**: 527 × 1 × 56 at y 26 over the street, Transparency 1, no collide, no query (the night light's fill).
- **Lane stubs**: `Street.Paving` 550.2–615.8 × z −398…−360 and 664.2–729.8 × z −40…−2 lie outside the inner guard ring (z −360 / −40), each with 10 forest trees on it; a player at a lane's end looks into the trees through the invisible guard.
- **`Houses.OuterN`**: an empty Model, as Allen left it.
- **Plot side walls**: solid to 6.6 (`Fence.Wall`), the stone `WallCap` is CanCollide off, so a jump (7.2) clears them into the 30-stud gaps; everything behind is inside the guards.
- **The other agent's property pass, as seen at 14:35**: Forest 5,079 parts with CanQuery and CastShadow off; Backdrop 134 off; Dressing 172 of 268 CanQuery, 110 cast shadows; Street 1,041 of 1,042 CanQuery, 1,024 cast shadows (the lamps); Houses 28 of 215 CanQuery; Landmarks 13 of 51.
- **Gate doors**: `Landmarks.GateDoors` ×2, the two `Door`s per gate collide and query (0.8 × 12.54 × 14.88, y 0.16–12.7), straps, bars and brackets do not; the posts are cylinders 17.6 tall on 1-stud feet.
- **Terrain**: 0 cells; the Baseplate (2,048 × 16 × 2,048, top 0) is the ground under the forest.

## Leftovers

Report only, nothing deleted. Sight lines from the street's middle (640, 6, −200), inside the west gate (432, 6, −200), inside the east gate (896, 6, −200) and N1's yard (526, 6, −300), brute-force rays; and the top of each against the mountain skyline in its direction.

| Leftover | Where (box) | Parts | From the street |
|---|---|---|---|
| `Workspace.Compare_1107` | **not in the place**: 0 instances by that name in Workspace, ServerStorage, ReplicatedStorage, Lighting, StarterGui, ServerScriptService at 14:30 | — | — |
| `Bamboo9` | (−78.1, −0.1, 128.5)–(−71.0, 12.6, 135.8) | 5, anchored | 788 / 606 / 1,026 / 740 studs; rays stop at the gap wall, the gate doors, EndN1; its top is 0.5° up against 24.7° of mountains |
| `Weapon Rack` | (−53.7, 0, −689.8)–(−45.3, 6.0, −683.2) | 12 (104 descendants: textures, welds) | 844 / 684 / 1,063 / 693; hidden (0° against 25.5°) |
| `ZanbatoPreview` | (−7, 299, −3)–(7, 309, 3) | 9 | 734 / 562 / 965 / 675; its top is 24.4° up from the street against 28.6° of mountains, 32.4° against 42.2° from the west gate, 18.3° against 20.6° from the east gate: hidden, but closest to showing |
| `AuxScene` (fantasy_anvil) | (80.6, 56.8, −81.5)–(81.9, 57.8, −80.8) | 5, **0 anchored** (falls at runtime) | 574 / 374 / 825 / 498; hidden (5.2° against 29.1°) |
| `Courtyard` (StoneLanterns) | (−13.3, 0.2, 98.3)–(−11.1, 5.3, 100.8) | 3 | 718 / 536 / 956 / 670; hidden |
| `MaterialDemo` | empty Folder | 0 | — |
| `Lighting` (Folder) | SunRays, DepthOfField, ColorCorrection, Bloom | 0 | effects do nothing outside the Lighting service |
| `Smithy` (root Folder) | (1963.8, 0.05, −266.1)–(2057.2, 10.2, −186.4), the old x-2000 station copy | 757 (1,134 descendants), 2 unanchored | 1,371 / 1,579 / 1,115 / 1,486; hidden (0.2° against 28.4°) |

With StreamingEnabled on, all of these are within the default 1,024-stud target radius from at least one lot except the x-2000 `Smithy`.

## Proposals

Ranked; each respects no generated nature, Blender low-poly props only, the stone street, the 32-wide road, 30-stud gaps, 11.6 walls, the forest ring and the block mountains.

1. **A hero the street can see: the yagura off the gate axis and taller.** Move it from the plaza's centre line (868.9–880.8, z −205…−195, top 11.7) to the plaza's north half (about x 875, z −216) and rebuild it 30–35 studs tall in the same look. Why: nothing leads the eye (10-31 #8): the gates are 21.9, the shops 38.5, the yagura was kept short only so the gate sign stays visible on the axis; off the axis it can grow, and a 33-stud tower at 450 studs covers 4.2° from the west gate (LihFolk's 3–5°). Cost: medium (one Blender model, the four plaza corner strings re-tied to it). Touches 2026-11-04 "yagura sized to keep the gate's sign in view" (Claude's sizing).
2. **Ground the two floaters** where they do a job: the ForestStones as a story group at the forest edge by the north lane end (about (583, 0.1, −357)) with the floating tree re-seated beside them. Why: a story group at a path's end marks the edge (LihFolk nodes); today both hang in the air. Cost: tiny, Allen's move.
3. **A cleaned street lamp.** One mesh or union for the lamp head in Allen's model, re-copied to the 16 posts (the lights and positions kept). Why: 204 same-plane slivers per head are the village's only z-fighting left, and 1,024 parts with shadows are the street's biggest draw. Cost: small (one model edit, a swap script). His model, his call.
4. **Something on the empty side of every door.** The right of each door has the three showcase stands; the left is bare until Decorate ships (hidden 10-30). One stone lantern (the Decorate "Stone Lanterns" model, a free fixed copy, not a purchase) at each `Shop.Decor.DoorLeft` spot. Why: 10-31 "prop groups at doors", LihFolk's medium props at nodes; a bare front reads unfinished. Cost: small (one clone in the template). Touches the 2026-10-29 decorations economy, so Allen decides.
5. **A centre band down the road.** One 5-wide slab strip the road's length, the same stone 10% darker, top 0.24 (0.04 over the road). Why: the 32-wide road is one even beige plane; a line down its middle leads the eye gate to gate and to the hero (LihFolk leading lines). Cost: tiny. Touches 2026-11-04's beige tint (Claude's pick); still a stone street.
6. **A visible stop at the two lane ends.** A fence piece in the gap-wall kit (pillar, wall, stone cap, 30 wide) across each lane end at z −359 and z −41, just inside the guards. Why: a player walking a lane today stops on an invisible wall with 10 trees behind it; LihFolk wants edges that contain the space to be seen. Cost: small (clone a GapWall, turn it 90°).
7. **Apply today's cap rule to the two odd ends.** Trim the south-east cap 1.3 short of lot S3's corner pillar (798 → 799.3) and pull the south middle cap back from 714.7 to 712.7. Why: consistency with the other seven pillar ends; only Edit shows the difference. Cost: tiny.

## Not checked

- Anything in Play: the Upgraded push on a live plot, the pushed workshop posts against the UpperPosts in game, prompts, NPCs, phones.
- Coplanar faces inside meshes (the stations' bevelled meshes, the anime trees, the lamp heads' textures): the check only knows block Parts and wedges; meshes got the box pass.
- The forest's own part-to-part overlaps (5,079 MeshParts).
- The cherry blossoms' trunks against the walls by eye: the box pass flags them, a capture would settle it (budget spent).
- Lighting and streaming values that scripts cannot read.

Related: [[Design/Reviews 2026-10-31/Map Review — Village]] · [[Design/Reviews 2026-10-31/Map Review — Shop and Street]] · [[Design/Reviews 2026-10-31/Map Review — Yard and Smithy]] · [[Sessions/2026-11-07]]

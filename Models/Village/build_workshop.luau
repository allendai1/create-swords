-- build_workshop.luau: the workshop's layout and furniture (2026-10-22).
-- Allen: "Redesign the workshop interior using this screenshot as the starting point" (a top view of the old layout):
-- supply chest in the back-left corner, furnaces freestanding on a shared stone hearth, the anvil in front of them on a
-- substantial stump as the room's focal point, a continuous-looking finishing bench along the right wall (hilt assembly
-- → polishing → etching, toward the shop door) built as matching sections so each station keeps its own unlock, the
-- racks where they were, a few tool rails and shallow shelves; simple geometry, sparse detail.
-- Run in Studio (Edit) through MCP execute_luau after build_shops.luau, on Workspace.Plot (the template every player's
-- plot is copied from) in its Starter layout. Rerunnable: stations go to fixed places and every model this script
-- built is replaced; a model it didn't build goes to ServerStorage.Legacy.Workshop_beforeLayout on the first run.
-- Built here:
--   HiltBench.Model3D, PolishStation.Model3D, EtchingTable.Dress: each station's bench section (dark timber base,
--     counter at waist height) with its own equipment. Inside the station, so it hides and stops colliding with it
--     while locked (TycoonService / TycoonController).
--   Anvil.Stump; OreRoller.LootBox (the ore box: the ingots lie on its lid; the client's OreBoxShow swings its Lid
--     about Hinge and lights Glow during a roll); Smithy.WorkshopFittings: hearth, the anvil's floor stone, tool rails,
--     shelves.
--   Plot.DeliveryBay: a fenced yard in the lane beside the shop, kept for a delivery cart later.
--   Shop.DeliveryWall / Shop.DeliveryDoor: the shop's wall onto the bay, swapped for a doorway by the Delivery upgrade.
-- Script contracts kept: station names and the parts scripts read (Top, BladeMount, Face, Base, Door, prompts, Stand<n>
-- with Pedestal and Ore, Lever, Machine, Slots) stay inside their stations and move with them. HiltBench.Model3D.Top is
-- the bench's worktop (HiltBenchController lays the sword on it; its view turns with the bench). The etching section's
-- practice blade and cradle are named Blank and Cradle, which EtchPlayback hides while the real sword lies there.
-- Everything but the delivery bay is a child of Smithy, so the Upgraded Store's push (TycoonService.pushWorkshopBack)
-- moves it all; the bay stays beside the shop.
--
-- Frame: build_shops.luau's shop frame: local z = 0 on the street side, +z into the lot, local x across (+x is the
-- screenshot's left). Workshop inside: walls at x ±23.5 (posts to ±23.35), door wall at z 30.25, back wall at z 80.25
-- (posts to 80.1); floor top y 0.2.

local P = workspace.Plot
local F = P:GetPivot() * CFrame.new(0, -0.5, -48) -- the shop frame: the template's pivot is its lot's centre
local S = P.Smithy
local SS = game:GetService("ServerStorage")
local LEGACY = SS:FindFirstChild("Legacy") or SS
local M = Enum.Material
local rad = math.rad

local C = {
	timberDk = Color3.fromRGB(56, 38, 28),
	timber = Color3.fromRGB(92, 63, 42),
	cedar = Color3.fromRGB(134, 94, 60),
	plinth = Color3.fromRGB(40, 28, 22),
	stone = Color3.fromRGB(122, 118, 110),
	stoneDk = Color3.fromRGB(96, 92, 86),
	stoneLt = Color3.fromRGB(168, 162, 152),
	whetstone = Color3.fromRGB(184, 180, 168),
	iron = Color3.fromRGB(58, 58, 62),
	steel = Color3.fromRGB(170, 174, 180),
	water = Color3.fromRGB(62, 92, 96),
	indigo = Color3.fromRGB(38, 54, 96),
	cloth = Color3.fromRGB(226, 218, 196),
	brass = Color3.fromRGB(176, 140, 70),
	jar = Color3.fromRGB(150, 96, 64),
	earth = Color3.fromRGB(128, 102, 74),
	plaster = Color3.fromRGB(232, 226, 212), -- the shells' walls (build_shops)
}

local FLOOR = 0.2
local COUNTER = 3.0 -- waist-height countertops (the old benches' worktops were 2.9…3.1)
local BACK, FRONT, LIP = -23.3, -19.9, -19.7 -- bench carcass back (0.05 off the wall posts) and front; counter front
local SECTIONS = { HiltBench = { 66, 75 }, PolishStation = { 57, 66 }, EtchingTable = { 48, 57 } } -- back → door
local HEARTH = { x0 = -6, x1 = 10, z0 = 70.6, z1 = 79, top = 0.8 }
local FORGES = { Forge = 6, Forge2 = -2 } -- x of each furnace on the hearth
local FORGE_Z = 75.3 -- 1.65 between the furnaces' backs and the back wall: freestanding
local ANVIL_X, ANVIL_Z = 2, 64.5 -- the anvil body's centre, between the furnaces and about 6 in front of the hearth
local STUMP_H, STUMP_D = 0.8, 2.0 -- the anvil stands the smith 1.6 from the face's centre line: a body 0.6 deep clears it
local BOX = { x0 = 13.9, x1 = 23.3, z0 = 73.7, z1 = 78.3, top = 1.75, lid = 0.4 } -- the ore box, back-left corner
local BOX_COLS, BOX_ROWS = { 15.45, 18.6, 21.75 }, { 74.85, 77.15 } -- the ingots on its lid: Stand1…3 front, 4…6 back
local BOX_STRAPS = { 17.025, 20.175 } -- iron straps, between the ingot columns
local PADS = { PolishStation = { -17.2, 61.5 }, EtchingTable = { -17.2, 52.5 }, Furnace2 = { -2, 68.4 } }
for i = 2, 6 do PADS["OreStand" .. i] = { 18.5, 71.2 } end -- the chain shows one at a time
local BAY = { x0 = 24.9, x1 = 40.9, z0 = 2, z1 = 34, top = 0.16 } -- the delivery bay, in the lane; x0 under the lot's kerb (x 24.3…25.1)
local DOOR = { z0 = 17.75, z1 = 22.25, top = 7.8 } -- the delivery door's opening in the shop's +x wall (x 23.5…24.0)

local function part(parent, name, size, cf, col, mat, o)
	o = o or {}
	local p = Instance.new(o.wedge and "WedgePart" or "Part")
	if o.shape then p.Shape = o.shape end
	p.Name = name
	p.Anchored = true
	p.Size = size
	p.CFrame = cf
	p.Color = col
	p.Material = mat or M.SmoothPlastic
	p.TopSurface = Enum.SurfaceType.Smooth
	p.BottomSurface = Enum.SurfaceType.Smooth
	p.CanCollide = o.solid == true
	p.CanQuery = o.solid == true
	p.CanTouch = false
	if size.X * size.Y * size.Z < 2 then p.CastShadow = false end
	p.Parent = parent
	return p
end
local function L(x, y, z) return F * CFrame.new(x, y, z) end
local function box(parent, name, x0, x1, y0, y1, z0, z1, col, mat, o)
	return part(parent, name, Vector3.new(x1 - x0, y1 - y0, z1 - z0), L((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), col, mat, o)
end
local UPRIGHT = CFrame.Angles(0, 0, math.pi / 2) -- a cylinder's axis (part X) turned up
local ALONG_Z = CFrame.Angles(0, math.pi / 2, 0)
local function cyl(parent, name, len, d, cf, col, mat, o)
	o = o or {}
	o.shape = Enum.PartType.Cylinder
	return part(parent, name, Vector3.new(len, d, d), cf, col, mat, o)
end

local backup = LEGACY:FindFirstChild("Workshop_beforeLayout")
local function fresh(parent, name)
	local old = parent:FindFirstChild(name)
	if old then
		if old:GetAttribute("BuiltBy") == "build_workshop" then
			old:Destroy()
		else
			if not backup then
				backup = Instance.new("Folder")
				backup.Name = "Workshop_beforeLayout"
				backup.Parent = LEGACY
			end
			old.Name = parent.Name .. "_" .. name
			old.Parent = backup
		end
	end
	local m = Instance.new("Model")
	m.Name = name
	m:SetAttribute("BuiltBy", "build_workshop")
	m.Parent = parent
	return m
end

-- move a model so a world point of it lands on a shop-frame point
local function bring(m, from, to)
	m:PivotTo(m:GetPivot() + (L(to.X, to.Y, to.Z).Position - from))
end
local function bottomCentre(m)
	local cf, size = m:GetBoundingBox()
	return cf.Position - Vector3.new(0, size.Y / 2, 0)
end

-- ---------------------------------------------------------------- stations to their places
for name, x in FORGES do
	local m = S:FindFirstChild(name)
	if m then bring(m, bottomCentre(m.Model3D), Vector3.new(x, HEARTH.top - 0.02, FORGE_Z)) end
end
bring(S.Anvil, bottomCentre(S.Anvil.Model3D), Vector3.new(ANVIL_X, FLOOR + STUMP_H - 0.02, ANVIL_Z))
-- the hilt bench turns to the right wall; its pivot is its Top (the prompt), inside the counter, LookVector at the wall
S.HiltBench:PivotTo(L(-21.5, COUNTER - 0.15, (SECTIONS.HiltBench[1] + SECTIONS.HiltBench[2]) / 2) * CFrame.Angles(0, math.pi / 2, 0))
-- the polishing station keeps its turn: its blade mount at the section's back end, so the blade lies along the stone
bring(S.PolishStation, S.PolishStation.BladeMount.Position, Vector3.new(-21.35, 3.22, SECTIONS.PolishStation[2] - 0.8))
-- the etching table: Top (prompt, and the surface the etching show lays the sword on) flush with the counter
S.EtchingTable:PivotTo(L(-21.5, COUNTER - 0.15, (SECTIONS.EtchingTable[1] + SECTIONS.EtchingTable[2]) / 2) * CFrame.Angles(0, math.pi / 2, 0))
S.EtchingTable.Top.Transparency = 1 -- the counter is the visible top now
for i = 1, 6 do -- each ingot lies on the box's lid; its tray (Pedestal) only holds the collect prompt now
	local stand = S.OreRoller:FindFirstChild("Stand" .. i)
	if stand then
		bring(stand, stand.Ore.Position, Vector3.new(BOX_COLS[(i - 1) % 3 + 1], BOX.top + BOX.lid + stand.Ore.Size.Y / 2 + 0.01, BOX_ROWS[(i - 1) // 3 + 1]))
		stand.Pedestal.Transparency = 1
		stand.Ore.Transparency = 1 -- an ingot on the lid means rolled ore waiting (ForgeService shows it); empty plots keep a bare lid
	end
end
for id, at in PADS do
	local pad = P.Pads:FindFirstChild(id)
	if pad then
		local rel = F:ToObjectSpace(pad.CFrame)
		pad.CFrame = L(at[1], rel.Y, at[2]) * rel.Rotation
	end
end

-- ---------------------------------------------------------------- finishing bench: one section per station
local function benchSection(m, z0, z1, counterName)
	z0, z1 = z0 + 0.03, z1 - 0.03 -- a hairline joint between sections: no shared faces
	local zc, q = (z0 + z1) / 2, (z1 - z0) / 4
	box(m, "Plinth", BACK + 0.2, FRONT - 0.3, FLOOR, FLOOR + 0.4, z0 + 0.25, z1 - 0.25, C.plinth, M.Wood, { solid = true })
	box(m, "Carcass", BACK, FRONT, FLOOR + 0.4, COUNTER - 0.3, z0, z1, C.timberDk, M.Wood, { solid = true })
	box(m, counterName, BACK, LIP, COUNTER - 0.3, COUNTER, z0, z1, C.timber, M.Wood, { solid = true })
	box(m, "Rail", FRONT, FRONT + 0.05, COUNTER - 0.75, COUNTER - 0.6, z0 + 0.2, z1 - 0.2, C.plinth, M.Wood)
	box(m, "Stile", FRONT, FRONT + 0.05, FLOOR + 0.5, COUNTER - 0.75, zc - 0.07, zc + 0.07, C.plinth, M.Wood)
	for _, s in { -1, 1 } do
		box(m, "Pull", FRONT, FRONT + 0.1, COUNTER - 1.1, COUNTER - 0.98, zc + s * q - 0.3, zc + s * q + 0.3, C.iron, M.Metal)
	end
end

do -- hilt assembly: blade mount at the back end, guards and a collar on a fittings board, mallet and punch at the back
	local z0, z1 = SECTIONS.HiltBench[1], SECTIONS.HiltBench[2]
	local m = fresh(S.HiltBench, "Model3D")
	benchSection(m, z0, z1, "Top") -- the worktop HiltBenchController seats the hilt on
	-- the seated sword lies along the bench 0.25 toward the wall from its middle (x -21.75): everything else clears it
	box(m, "MountBase", -22.35, -20.95, COUNTER, COUNTER + 0.22, z1 - 0.9, z1 - 0.3, C.cedar, M.Wood)
	for _, x in { -22.2, -21.1 } do
		box(m, "MountCheek", x - 0.15, x + 0.15, COUNTER + 0.22, COUNTER + 0.55, z1 - 0.85, z1 - 0.35, C.cedar, M.Wood)
	end
	box(m, "FittingsBoard", -20.75, -19.95, COUNTER, COUNTER + 0.08, z0 + 0.4, z0 + 1.6, C.timberDk, M.Wood)
	for _, z in { z0 + 0.75, z0 + 1.3 } do
		cyl(m, "Tsuba", 0.06, 0.45, L(-20.35, COUNTER + 0.11, z) * UPRIGHT, C.iron, M.Metal)
	end
	box(m, "MalletHead", -23.1, -22.7, COUNTER, COUNTER + 0.4, z0 + 1.6, z0 + 2.3, C.cedar, M.Wood)
	cyl(m, "MalletHandle", 1.1, 0.13, L(-22.9, COUNTER + 0.2, z0 + 2.85) * ALONG_Z, C.timber, M.Wood)
	cyl(m, "Punch", 0.6, 0.08, L(-22.9, COUNTER + 0.04, z0 + 4.2) * ALONG_Z, C.steel, M.Metal)
end

do -- polishing: a long stone set into the counter under the blade, a shallow water tray at the back, a cloth
	local z0, z1 = SECTIONS.PolishStation[1], SECTIONS.PolishStation[2]
	local m = fresh(S.PolishStation, "Model3D")
	benchSection(m, z0, z1, "Counter")
	local mx = F:PointToObjectSpace(S.PolishStation.BladeMount.Position).X
	box(m, "Stone", mx - 0.6, mx + 0.6, COUNTER - 0.05, COUNTER + 0.1, z0 + 1.4, z1 - 0.4, C.whetstone, M.Slate)
	local tz0, tz1 = z0 + 2, z0 + 6
	box(m, "TrayBase", -23.1, -22.3, COUNTER, COUNTER + 0.06, tz0, tz1, C.timberDk, M.Wood)
	for _, x in { -23.06, -22.34 } do
		box(m, "TraySide", x - 0.04, x + 0.04, COUNTER + 0.06, COUNTER + 0.2, tz0, tz1, C.timberDk, M.Wood)
	end
	for _, z in { tz0 + 0.04, tz1 - 0.04 } do
		box(m, "TrayEnd", -23.02, -22.38, COUNTER + 0.06, COUNTER + 0.2, z - 0.04, z + 0.04, C.timberDk, M.Wood)
	end
	box(m, "TrayWater", -23.02, -22.38, COUNTER + 0.06, COUNTER + 0.15, tz0 + 0.08, tz1 - 0.08, C.water, M.SmoothPlastic)
	box(m, "Cloth", -20.65, -19.95, COUNTER, COUNTER + 0.04, z0 + 0.35, z0 + 1.15, C.cloth, M.Fabric)
end

do -- etching: a blade cradle with a practice blank, the engraving stylus on its rest, an ink pot
	local z0, z1 = SECTIONS.EtchingTable[1], SECTIONS.EtchingTable[2]
	local zc = (z0 + z1) / 2
	local m = fresh(S.EtchingTable, "Dress")
	benchSection(m, z0, z1, "Counter")
	for _, z in { zc - 1.9, zc + 1.9 } do
		box(m, "Cradle", -22.0, -21.0, COUNTER, COUNTER + 0.22, z - 0.25, z + 0.25, C.cedar, M.Wood)
		box(m, "Cradle", -21.95, -21.05, COUNTER + 0.22, COUNTER + 0.26, z - 0.22, z + 0.22, C.indigo, M.Fabric)
	end
	box(m, "Blank", -21.56, -21.44, COUNTER + 0.26, COUNTER + 0.31, zc - 2.4, zc + 2.4, C.steel, M.Metal)
	box(m, "StylusRest", -23.05, -22.65, COUNTER, COUNTER + 0.14, z0 + 1.2, z0 + 1.6, C.timberDk, M.Wood)
	cyl(m, "Stylus", 0.9, 0.08, L(-22.85, COUNTER + 0.18, z0 + 1.75) * ALONG_Z, C.timberDk, M.Wood)
	cyl(m, "StylusPoint", 0.12, 0.05, L(-22.85, COUNTER + 0.18, z0 + 2.26) * ALONG_Z, C.brass, M.Metal)
	cyl(m, "InkPot", 0.3, 0.32, L(-22.85, COUNTER + 0.15, z1 - 1.1) * UPRIGHT, C.jar, M.SmoothPlastic)
end

-- ---------------------------------------------------------------- anvil stump
do
	local m = fresh(S.Anvil, "Stump")
	cyl(m, "Stump", STUMP_H, STUMP_D, L(ANVIL_X, FLOOR + STUMP_H / 2, ANVIL_Z) * UPRIGHT, C.timber, M.Wood, { solid = true })
	-- a low, wider root flare: a heavier-looking stump that stays under the smith's feet
	cyl(m, "Flare", 0.25, STUMP_D + 0.8, L(ANVIL_X, FLOOR + 0.125, ANVIL_Z) * UPRIGHT, C.timberDk, M.Wood, { solid = true })
	for _, y in { FLOOR + 0.18, FLOOR + STUMP_H - 0.14 } do
		cyl(m, "Band", 0.1, STUMP_D + 0.06, L(ANVIL_X, y, ANVIL_Z) * UPRIGHT, C.iron, M.Metal)
	end
end

-- ---------------------------------------------------------------- ore loot box (back-left corner)
-- Allen 2026-10-22: the ore roller as a loot box (References/Concept Art/ingot crate opening): on a pull the lid swings
-- open, the ingots float out spinning through the materials and drop onto the closed lid, where all six fit. It
-- replaces the open supply chest of earlier the same day.
do
	local old = S.OreRoller:FindFirstChild("Chest")
	if old and old:GetAttribute("BuiltBy") == "build_workshop" then old:Destroy() end
	local m = fresh(S.OreRoller, "LootBox")
	local x0, x1, z0, z1, top, t = BOX.x0, BOX.x1, BOX.z0, BOX.z1, BOX.top, 0.25
	local wood, seam = Color3.fromRGB(178, 112, 62), Color3.fromRGB(120, 72, 40)
	box(m, "Front", x0, x1, FLOOR, top, z0, z0 + t, wood, M.WoodPlanks, { solid = true })
	box(m, "Back", x0, x1, FLOOR, top, z1 - t, z1, wood, M.WoodPlanks, { solid = true })
	box(m, "Side", x0, x0 + t, FLOOR, top, z0 + t, z1 - t, wood, M.WoodPlanks, { solid = true })
	box(m, "Side", x1 - t, x1, FLOOR, top, z0 + t, z1 - t, wood, M.WoodPlanks, { solid = true })
	box(m, "Inside", x0 + t, x1 - t, FLOOR, FLOOR + 0.3, z0 + t, z1 - t, C.plinth, M.Wood, { solid = true })
	box(m, "Seam", x0 + 0.05, x1 - 0.05, 0.92, 0.98, z0 - 0.02, z0, seam, M.Wood) -- the plank joint across the front
	box(m, "Handle", 17.8, 19.4, 1.05, 1.45, z0 - 0.09, z0, C.iron, M.Metal)
	local lid = Instance.new("Model")
	lid.Name = "Lid"
	box(lid, "Board", x0 - 0.05, x1 + 0.05, top, top + BOX.lid, z0 - 0.05, z1 + 0.05, wood, M.WoodPlanks, { solid = true })
	for _, x in BOX_STRAPS do
		box(m, "Strap", x - 0.28, x + 0.28, FLOOR + 0.02, top, z0 - 0.05, z0, C.iron, M.Metal)
		box(lid, "Strap", x - 0.28, x + 0.28, top + BOX.lid, top + BOX.lid + 0.04, z0 - 0.05, z1 + 0.05, C.iron, M.Metal)
		box(lid, "Strap", x - 0.28, x + 0.28, top, top + BOX.lid + 0.04, z0 - 0.1, z0 - 0.05, C.iron, M.Metal)
	end
	local hinge = L((x0 + x1) / 2, top, z1 + 0.05) -- the lid's back bottom edge; local +x turns the lid up and back
	lid.WorldPivot = hinge
	lid.Parent = m
	part(m, "Hinge", Vector3.new(0.2, 0.2, 0.2), hinge, C.iron).Transparency = 1
	local glow = part(m, "Glow", Vector3.new(0.2, 0.2, 0.2), L((x0 + x1) / 2, 1.0, (z0 + z1) / 2), C.cloth)
	glow.Transparency = 1
	local light = Instance.new("PointLight") -- off until the show lights it
	light.Color, light.Range, light.Brightness, light.Shadows = Color3.fromRGB(255, 190, 110), 12, 0, false
	light.Parent = glow
end

-- ---------------------------------------------------------------- fittings: hearth, floor stone, rails and shelves
do
	local m = fresh(S, "WorkshopFittings")
	-- one hearth under both furnaces (Furnace 2's bay stays ready before it is bought), with a stone kerb in front
	box(m, "Hearth", HEARTH.x0, HEARTH.x1, FLOOR, HEARTH.top, HEARTH.z0 + 0.5, HEARTH.z1, C.stoneDk, M.Slate, { solid = true })
	box(m, "HearthKerb", HEARTH.x0 - 0.1, HEARTH.x1 + 0.1, FLOOR, HEARTH.top + 0.08, HEARTH.z0, HEARTH.z0 + 0.5, C.stone, M.Cobblestone, { solid = true })
	-- a round stone under the anvil and the smith: the room's focal point
	cyl(m, "AnvilStone", 0.06, 9, L(ANVIL_X, FLOOR + 0.03, ANVIL_Z - 0.3) * UPRIGHT, C.stoneDk, M.Slate, { solid = true })

	-- right wall, over the hilt and polishing sections: a rail with hammers, tongs and files on pegs
	local rx = -23.33 -- 0.02 off the wall posts' faces
	local tx = rx + 0.35 -- the hanging tools' middle, in front of the rail
	box(m, "ToolRail", rx, rx + 0.25, 6.0, 6.35, SECTIONS.PolishStation[1] + 1, SECTIONS.HiltBench[2] - 1, C.timberDk, M.Wood)
	local function peg(z) cyl(m, "Peg", 0.22, 0.1, L(rx + 0.36, 6.15, z), C.timber, M.Wood) end
	local tools = {
		function(z) -- hammer
			box(m, "Handle", tx - 0.06, tx + 0.06, 4.8, 6.05, z - 0.06, z + 0.06, C.timber, M.Wood)
			box(m, "Head", tx - 0.13, tx + 0.13, 4.5, 4.8, z - 0.38, z + 0.38, C.iron, M.Metal)
		end,
		function(z) -- tongs
			for _, s in { -1, 1 } do
				part(m, "Tongs", Vector3.new(0.07, 1.9, 0.07), L(tx + s * 0.02, 5.1, z + s * 0.08) * CFrame.Angles(s * rad(4), 0, 0), C.iron, M.Metal) -- arms 0.04 apart: no shared face
			end
		end,
		function(z) -- file
			box(m, "File", tx - 0.03, tx + 0.03, 4.9, 6.05, z - 0.1, z + 0.1, C.steel, M.Metal)
		end,
	}
	for i = 1, 6 do
		local z = SECTIONS.PolishStation[1] + 1.8 + (i - 1) * 2.8
		peg(z)
		tools[(i - 1) % 3 + 1](z)
	end

	-- right wall, over the etching section: a shallow shelf with jars and a box
	local ez0, ez1 = SECTIONS.EtchingTable[1] + 1, SECTIONS.EtchingTable[2] - 2
	box(m, "Shelf", rx, rx + 0.7, 6.0, 6.18, ez0, ez1, C.timber, M.Wood)
	for _, z in { ez0 + 0.6, ez1 - 0.6 } do
		box(m, "Bracket", rx, rx + 0.45, 5.45, 6.0, z - 0.08, z + 0.08, C.timberDk, M.Wood)
	end
	cyl(m, "Jar", 0.45, 0.4, L(rx + 0.35, 6.18 + 0.225, ez0 + 1.4) * UPRIGHT, C.jar, M.SmoothPlastic)
	cyl(m, "Jar", 0.36, 0.34, L(rx + 0.35, 6.18 + 0.18, ez0 + 2.1) * UPRIGHT, C.stone, M.SmoothPlastic)
	box(m, "Box", rx + 0.1, rx + 0.6, 6.18, 6.55, ez1 - 2.0, ez1 - 1.1, C.cedar, M.Wood)

	-- left wall, between the ingot rack and the chest: a shallow shelf with cloth bundles and a crate
	local lx = 23.33
	box(m, "Shelf", lx - 0.7, lx, 5.6, 5.78, 60, 66, C.timber, M.Wood)
	for _, z in { 60.6, 65.4 } do
		box(m, "Bracket", lx - 0.45, lx, 5.05, 5.6, z - 0.08, z + 0.08, C.timberDk, M.Wood)
	end
	box(m, "Bundle", lx - 0.6, lx - 0.1, 5.78, 6.12, 60.5, 61.5, C.cloth, M.Fabric)
	box(m, "Bundle", lx - 0.6, lx - 0.1, 5.78, 6.08, 61.7, 62.6, C.indigo, M.Fabric)
	box(m, "Crate", lx - 0.65, lx - 0.05, 5.78, 6.3, 64.2, 65.6, C.cedar, M.WoodPlanks)

	-- back wall, right of the hearth: tongs and a poker within reach of the anvil
	local bz = 79.83 -- 0.02 off the back wall posts' faces (z 80.1 - 0.25)
	local tz = bz - 0.1 -- the hanging tools' middle
	box(m, "ToolRail", -13.5, -8.0, 5.6, 5.95, bz, bz + 0.25, C.timberDk, M.Wood)
	for _, x in { -12.6, -11.0, -9.4 } do
		cyl(m, "Peg", 0.22, 0.1, L(x, 5.75, bz - 0.11) * ALONG_Z, C.timber, M.Wood)
	end
	for _, x in { -12.6, -11.0 } do
		for _, s in { -1, 1 } do
			part(m, "Tongs", Vector3.new(0.07, 1.9, 0.07), L(x + s * 0.08, 4.7, tz + s * 0.02) * CFrame.Angles(0, 0, s * rad(4)), C.iron, M.Metal)
		end
	end
	box(m, "Poker", -9.44, -9.36, 3.0, 5.65, tz - 0.04, tz + 0.04, C.iron, M.Metal)
end

-- ---------------------------------------------------------------- delivery bay (in the lane beside the shop)
-- Allen 2026-10-22: "each plot should have an area where we can eventually add a delivery carrier. maybe a guy with a
-- carriage. potentially could carry over into the street." The lots are full width, so the bay is in the lane on the
-- plot's +x side; that is every lot's own side, so each lane holds one bay per row. A yard of packed earth, fenced on
-- the lane side and at the back, opens to the street through a gateway, so a cart can roll straight out onto the road.
-- Nothing works here yet: CartSpot (invisible) is where the cart will stand, facing the street, for the delivery board
-- (GDD 9.1). The lane's paving under it has its top at 0.12.
do
	local m = fresh(P, "DeliveryBay")
	box(m, "Yard", BAY.x0, BAY.x1, 0.02, BAY.top, BAY.z0, BAY.z1, C.earth, M.Ground, { solid = true })
	local sunk = BAY.top - 0.06 -- posts and crates stand 0.06 into the yard
	local gz, fx, fz = BAY.z0 + 0.5, BAY.x1 - 0.35, BAY.z1 - 0.35 -- the gateway's line; fence lines on the lane side and at the back (posts inside the yard's edge)
	local function post(x, z, w, h)
		box(m, "Post", x - w / 2, x + w / 2, sunk, BAY.top + h, z - w / 2, z + w / 2, C.timberDk, M.Wood, { solid = true })
	end
	for i = 1, 7 do -- lane side, from the gatepost to the back corner
		post(fx, gz + (fz - gz) * i / 7, 0.5, 3)
	end
	for i = 0, 3 do -- the back, to the corner post
		post(BAY.x0 + 0.5 + (fx - BAY.x0 - 0.5) * i / 4, fz, 0.5, 3)
	end
	for _, y in { 1.1, 2.4 } do -- rails run into the end posts; the back's sit 0.1 higher, so the two never share a face
		box(m, "Rail", fx - 0.1, fx + 0.1, BAY.top + y, BAY.top + y + 0.25, gz, fz, C.timber, M.Wood, { solid = true })
		box(m, "Rail", BAY.x0 + 0.5, fx, BAY.top + y + 0.1, BAY.top + y + 0.35, fz - 0.1, fz + 0.1, C.timber, M.Wood, { solid = true })
	end
	-- the gateway: two tall posts, a lintel and a tie beam
	local gx = BAY.x0 + 1.1
	for _, x in { gx, fx } do
		post(x, gz, 0.6, 8.4)
	end
	box(m, "Lintel", gx - 0.6, fx + 0.6, BAY.top + 8.1, BAY.top + 8.7, gz - 0.35, gz + 0.35, C.timberDk, M.Wood, { solid = true })
	box(m, "TieBeam", gx, fx, BAY.top + 7.0, BAY.top + 7.3, gz - 0.15, gz + 0.15, C.timber, M.Wood, { solid = true })
	-- a few crates in the back corner by the shop, out of the cart's way
	box(m, "Crate", 26.0, 28.4, sunk, BAY.top + 2.4, 30.4, 32.8, C.cedar, M.WoodPlanks, { solid = true })
	box(m, "Crate", 26.3, 28.1, BAY.top + 2.38, BAY.top + 4.2, 30.7, 32.5, C.cedar, M.WoodPlanks, { solid = true })
	box(m, "Crate", 28.8, 30.8, sunk, BAY.top + 2.0, 31.0, 33.0, C.cedar, M.WoodPlanks, { solid = true })
	local spot = part(m, "CartSpot", Vector3.new(6, 0.2, 14), L(33, BAY.top + 0.1, 19), C.cloth)
	spot.Transparency = 1
end

-- ---------------------------------------------------------------- delivery door (the shop's wall onto the bay)
-- Allen 2026-10-22: a door from the shop to the delivery bay, "until delivery is unlocked" hidden. Both shop shells have
-- the same wall bay between their posts at z 15 and 25, beside the bay's CartSpot, with nothing inside in front of it.
-- Its panel (wainscot and plaster) leaves the shells for Shop.DeliveryWall, shown until the Delivery upgrade is bought
-- (UntilUpgrade); then Shop.DeliveryDoor (Upgrade) takes its place: the same wall round a doorway, with a frame, a sill,
-- a sliding door pushed open inside and a noren outside. Both are TycoonItems outside the shells, because an item inside
-- another one would be shown along with it (TycoonController) and restored wrongly (TycoonService). There is no
-- "Delivery" upgrade yet, so the door stays hidden until one is added to Shared/Upgrades.
do
	local Shop = P.Shop
	for _, shell in { Shop.Starter, Shop.Upgraded } do
		for _, p in shell:GetDescendants() do
			if p:IsA("BasePart") and (p.Name == "Wainscot" or p.Name == "Plaster") then
				local c = F:PointToObjectSpace(p.Position)
				if math.abs(c.X - 23.75) < 0.2 and math.abs(c.Z - 20) < 0.2 then p:Destroy() end
			end
		end
	end
	local function item(name, attribute)
		local m = fresh(Shop, name)
		m:SetAttribute(attribute, "Delivery")
		m:AddTag("TycoonItem")
		return m
	end
	-- the shells' wall, as build_shops makes it: wainscot to 3.2, plaster from 3.1 (thinner, so no face is shared)
	local function wainscot(m, z0, z1) box(m, "Wainscot", 23.45, 24.05, 0, 3.2, z0, z1, C.timberDk, M.Wood, { solid = true }) end
	local function plaster(m, y0, y1, z0, z1) box(m, "Plaster", 23.5, 24.0, y0, y1, z0, z1, C.plaster, M.Plaster, { solid = true }) end

	local wall = item("DeliveryWall", "UntilUpgrade")
	wainscot(wall, 15.3, 24.7)
	plaster(wall, 3.1, 12.8, 15.3, 24.7)

	local m = item("DeliveryDoor", "Upgrade")
	for _, z in { { 15.3, DOOR.z0 - 0.15 }, { DOOR.z1 + 0.15, 24.7 } } do -- each side ends inside a post and a jamb
		wainscot(m, z[1], z[2])
		plaster(m, 3.1, DOOR.top + 0.1, z[1], z[2])
	end
	plaster(m, DOOR.top + 0.4, 12.8, 15.3, 24.7)
	box(m, "Lintel", 23.3, 24.2, DOOR.top, DOOR.top + 0.5, 15.2, 24.8, C.timberDk, M.Wood, { solid = true })
	for _, z in { DOOR.z0 - 0.35, DOOR.z1 } do
		box(m, "Jamb", 23.32, 24.18, 0.05, DOOR.top + 0.2, z, z + 0.35, C.timberDk, M.Wood, { solid = true })
	end
	box(m, "Sill", 23.3, 24.2, 0.02, 0.3, DOOR.z0 - 0.3, DOOR.z1 + 0.3, C.timber, M.Wood, { solid = true })
	-- the sliding door, pushed open along the inside of the wall, and a two-piece noren outside
	box(m, "Door", 23.02, 23.2, 0.3, DOOR.top - 0.1, DOOR.z1 + 0.05, DOOR.z1 + 4.45, C.timber, M.Wood, { solid = true })
	for _, y in { 2.0, 5.6 } do
		box(m, "Batten", 22.92, 23.04, y, y + 0.3, DOOR.z1 + 0.25, DOOR.z1 + 4.25, C.timberDk, M.Wood)
	end
	local mid = (DOOR.z0 + DOOR.z1) / 2
	box(m, "Noren", 24.22, 24.28, DOOR.top - 2.5, DOOR.top - 0.05, DOOR.z0 + 0.05, mid - 0.05, C.indigo, M.Fabric)
	box(m, "Noren", 24.22, 24.28, DOOR.top - 2.5, DOOR.top - 0.05, mid + 0.05, DOOR.z1 - 0.05, C.indigo, M.Fabric)
end

local n = 0
for _, d in P:GetDescendants() do if d:IsA("BasePart") and d:FindFirstAncestorWhichIsA("Model") and d:FindFirstAncestorWhichIsA("Model"):GetAttribute("BuiltBy") == "build_workshop" then n += 1 end end
return ("Workshop laid out: %d new parts"):format(n)

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
--     Since the station refinements each also has a large hero tool, its own wall fittings with a sample sword, and a
--     hanging kanban sign (kanji and name) on timber arms from the wall's band beam.
--   OreRoller.LootBox (the ore box: the ingots lie on its lid; the client's OreBoxShow swings its Lid
--     about Hinge and lights Glow during a roll); Smithy.WorkshopFittings: hearth, the anvil's floor stone, the back
--     wall's tool rail, the left wall's shelf.
--   Plot.DeliveryBay: a fenced yard in the lane beside the shop, kept for a delivery cart later.
--   Shop.DeliveryWall / Shop.DeliveryDoor: the shop's wall onto the bay, swapped for a doorway by the Delivery upgrade.
--   Shop.Displays.WallRack1…4.Shelf: the wall sword shelves (2026-10-22, below); each display's slots go onto its tiers.
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
-- The anvil is Allen's fantasy_anvil (2026-10-22: "replace our anvil with te fantasy_anvil i put in"), meshes in Anvil.Model3D:
-- it has its own pedestal, so it stands on its floor stone (0.06 thick), sunk ANVIL_SINK, with no stump.
local ANVIL_SINK = 0.02
local BOX = { x0 = 13.9, x1 = 23.3, z0 = 73.7, z1 = 78.3, top = 1.75, lid = 0.4 } -- the ore box, back-left corner
local BOX_COLS, BOX_ROWS = { 15.45, 18.6, 21.75 }, { 74.85, 77.15 } -- the ingots on its lid: Stand1…3 front, 4…6 back
local BOX_STRAPS = { 17.025, 20.175 } -- iron straps, between the ingot columns
local PADS = { PolishStation = { -17.2, 61.5 }, EtchingTable = { -17.2, 52.5 }, Furnace2 = { -2, 68.4 } }
for i = 2, 6 do PADS["OreStand" .. i] = { 18.5, 71.2 } end -- the chain shows one at a time
PADS.MergeSlots = PADS.OreStand6 -- Merge Ore Slots, on the same spot once Ore Slot 6 is bought (Refinements3 2026-10-23)
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
bring(S.Anvil, bottomCentre(S.Anvil.Model3D), Vector3.new(ANVIL_X, FLOOR + 0.06 - ANVIL_SINK, ANVIL_Z))
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

-- Station refinements (Allen 2026-10-22, Refinement.md): "Enlarge the main tool or work surface of each station so players
-- can recognize its purpose at a glance", "Decorate the empty walls with station-specific racks, shelves, tools, and sample
-- swords", "Add three overhead station signs or Japanese-style hanging banners, integrated into the wooden architecture".
-- Each station's hero piece sits at an end of its section, clear of the middle where the sword is shown; its wall gets
-- its own fittings and a finished sample sword on pegs; a kanban hangs over the counter's front edge from two timber arms
-- socketed into the wall's band beam, with knee braces. Everything is in the station's model, so it hides with it while
-- locked (signs' SurfaceGuis and the andon's light too: TycoonService). The station cameras look down from about y 6,
-- below the signs (8.35…9.55). Wall pieces keep clear of the wall posts (z 54.8…55.6, 63.2…64.0, 71.6…72.4).
local WALL = -23.48 -- 0.02 off the plaster
local function wallSword(m, z0, y, blade, bladeMat, wrap, metal)
	-- a finished sword on two pegs: grip from z0, blade toward +z, edge up, flat to the room (x -23.2 its middle)
	local x = -23.2
	for _, z in { z0 + 0.6, z0 + 3.2 } do
		cyl(m, "Peg", 0.3, 0.08, L(-23.34, y - 0.12, z), C.timberDk, M.Wood)
	end
	box(m, "Grip", x - 0.07, x + 0.07, y - 0.1, y + 0.1, z0, z0 + 1.0, wrap, M.Fabric)
	box(m, "Kashira", x - 0.08, x + 0.08, y - 0.11, y + 0.11, z0 - 0.08, z0 + 0.04, metal, M.Metal)
	cyl(m, "Tsuba", 0.06, 0.5, L(x, y, z0 + 1.03) * ALONG_Z, metal, M.Metal)
	box(m, "Habaki", x - 0.045, x + 0.045, y - 0.09, y + 0.13, z0 + 1.06, z0 + 1.2, C.brass, M.Metal)
	box(m, "Blade", x - 0.02, x + 0.02, y - 0.08, y + 0.2, z0 + 1.1, z0 + 4.0, blade, bladeMat)
	box(m, "Blade", x - 0.02, x + 0.02, y - 0.04, y + 0.14, z0 + 4.0, z0 + 4.25, blade, bladeMat) -- the tip steps in, end to end
	box(m, "Blade", x - 0.02, x + 0.02, y, y + 0.08, z0 + 4.25, z0 + 4.45, blade, bladeMat)
	return x
end
local function label(p, face, lines)
	-- text side by side on one face of a part: { { text, size, colour } }
	local g = Instance.new("SurfaceGui")
	g.Face = face
	g.SizingMode = Enum.SurfaceGuiSizingMode.PixelsPerStud
	g.PixelsPerStud = 100
	g.LightInfluence = 0 -- readable in the dim workshop
	local list = Instance.new("UIListLayout")
	list.FillDirection = Enum.FillDirection.Horizontal
	list.HorizontalAlignment = Enum.HorizontalAlignment.Center
	list.VerticalAlignment = Enum.VerticalAlignment.Center
	list.Padding = UDim.new(0, 18)
	list.Parent = g
	for i, l in lines do
		local t = Instance.new("TextLabel")
		t.LayoutOrder = i
		t.BackgroundTransparency = 1
		t.AutomaticSize = Enum.AutomaticSize.XY
		t.Size = UDim2.new()
		t.Text = l[1]
		t.TextSize = l[2]
		t.TextColor3 = l[3]
		t.FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Bold)
		t.Parent = g
	end
	g.Parent = p
end
local function sign(m, zc, kanji, name)
	-- arms from the band beam (x -23.45, y 10.04…10.34) out over the counter's front, knee braces under them, cords down
	-- to a dark board in a cedar frame with the station's kanji and name in gold and cream
	for _, s in { -1, 1 } do
		local z = zc + s * 1.15
		box(m, "SignArm", -23.45, -20.5, 10.04, 10.34, z - 0.13, z + 0.13, C.timberDk, M.Wood) -- under the band's bottom: no shared face
		part(m, "SignBrace", Vector3.new(0.18, 1.41, 0.18), L(-22.95, 9.6, z) * CFrame.Angles(0, 0, -math.pi / 4), C.timberDk, M.Wood)
		box(m, "SignCord", -20.78, -20.72, 9.55, 10.04, z - 0.03, z + 0.03, C.timberDk, M.Fabric)
	end
	box(m, "SignFrame", -20.85, -20.75, 8.25, 9.55, zc - 1.4, zc + 1.4, C.cedar, M.Wood)
	local board = box(m, "Sign", -20.79, -20.67, 8.35, 9.45, zc - 1.3, zc + 1.3, C.plinth, M.Wood)
	label(board, Enum.NormalId.Right, { { kanji, 70, Color3.fromRGB(222, 178, 92) }, { name, 30, Color3.fromRGB(240, 228, 204) } })
end

do -- hilt assembly: a hilt vise at the back end, a big tsuba on a stand at the front, guards on the wall
	local z0, z1 = SECTIONS.HiltBench[1], SECTIONS.HiltBench[2]
	local m = fresh(S.HiltBench, "Model3D")
	benchSection(m, z0, z1, "Top") -- the worktop HiltBenchController seats the hilt on
	-- the seated sword lies along the bench 0.25 toward the wall from its middle (x -21.75), z 68.1…72.9 for a katana:
	-- everything else clears it
	box(m, "VisePlate", -22.6, -20.9, COUNTER, COUNTER + 0.32, z1 - 1.45, z1 - 0.25, C.cedar, M.Wood)
	for _, x in { -22.35, -21.15 } do
		box(m, "ViseCheek", x - 0.2, x + 0.2, COUNTER + 0.32, COUNTER + 1.0, z1 - 1.35, z1 - 0.35, C.cedar, M.Wood)
	end
	cyl(m, "ViseScrew", 1.9, 0.12, L(-21.75, COUNTER + 0.8, z1 - 0.85), C.brass, M.Metal)
	cyl(m, "ViseKnob", 0.16, 0.32, L(-20.73, COUNTER + 0.8, z1 - 0.85), C.brass, M.Metal)
	box(m, "TsubaStand", -23.15, -22.55, COUNTER, COUNTER + 0.12, z0 + 0.3, z0 + 1.1, C.timberDk, M.Wood)
	cyl(m, "BigTsuba", 0.08, 0.95, L(-22.85, COUNTER + 0.57, z0 + 0.7), C.brass, M.Metal)
	cyl(m, "TsubaHole", 0.1, 0.24, L(-22.85, COUNTER + 0.57, z0 + 0.7), C.plinth, M.Metal)
	box(m, "FittingsBoard", -20.75, -19.95, COUNTER, COUNTER + 0.08, z0 + 0.4, z0 + 1.6, C.timberDk, M.Wood)
	for _, z in { z0 + 0.75, z0 + 1.3 } do
		cyl(m, "Tsuba", 0.06, 0.45, L(-20.35, COUNTER + 0.11, z) * UPRIGHT, C.iron, M.Metal)
	end
	box(m, "MalletHead", -23.15, -22.6, COUNTER, COUNTER + 0.5, z0 + 1.5, z0 + 2.35, C.cedar, M.Wood)
	cyl(m, "MalletHandle", 1.1, 0.14, L(-22.88, COUNTER + 0.25, z0 + 2.9) * ALONG_Z, C.timber, M.Wood)
	-- wall: a board of guards, a sample sword under it, finished hilts hanging past the post
	box(m, "GuardBoard", WALL, -23.4, 5.35, 7.95, z0 + 0.4, z0 + 5.3, C.timber, M.Wood)
	local metals = { C.iron, C.brass, Color3.fromRGB(184, 115, 51), C.plinth }
	for r = 0, 1 do
		for c = 0, 3 do
			local at = L(-23.36, 7.3 - r * 1.3, z0 + 1.0 + c * 1.2)
			cyl(m, "Guard", 0.06, 0.62, at, metals[(r * 2 + c) % 4 + 1], M.Metal)
			cyl(m, "GuardHole", 0.08, 0.14, at, C.plinth, M.Metal)
		end
	end
	wallSword(m, z0 + 0.5, 4.75, C.steel, M.Metal, C.indigo, Color3.fromRGB(212, 168, 80))
	box(m, "HiltRail", WALL, -23.25, 7.7, 7.95, z1 - 2.4, z1 - 0.1, C.timberDk, M.Wood)
	for i, wrap in { C.indigo, C.plinth, Color3.fromRGB(122, 40, 32) } do
		local z = z1 - 2.0 + (i - 1) * 0.75
		box(m, "Hilt", -23.32, -23.18, 6.45, 7.6, z - 0.1, z + 0.1, wrap, M.Fabric)
		box(m, "HiltCap", -23.33, -23.17, 6.35, 6.47, z - 0.11, z + 0.11, C.brass, M.Metal)
		box(m, "HiltCord", -23.27, -23.23, 7.6, 7.7, z - 0.03, z + 0.03, C.cloth, M.Fabric)
	end
	sign(m, (z0 + z1) / 2, "柄", "HILT BENCH")
end

do -- polishing: a wide stone on a cedar bed, a water bucket, graded stones and cloths on the wall
	local z0, z1 = SECTIONS.PolishStation[1], SECTIONS.PolishStation[2]
	local m = fresh(S.PolishStation, "Model3D")
	benchSection(m, z0, z1, "Counter")
	local mx = F:PointToObjectSpace(S.PolishStation.BladeMount.Position).X
	box(m, "StoneBed", mx - 0.9, mx + 0.95, COUNTER, COUNTER + 0.05, z0 + 1.25, z1 - 0.25, C.cedar, M.Wood)
	box(m, "Stone", mx - 0.75, mx + 0.75, COUNTER - 0.05, COUNTER + 0.1, z0 + 1.4, z1 - 0.4, C.whetstone, M.Slate)
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
	-- the bucket at the front end, by the wall: hooped staves, water just under the rim, a handle
	local bx, bz = -22.6, z0 + 0.75
	cyl(m, "Bucket", 0.9, 0.95, L(bx, COUNTER + 0.45, bz) * UPRIGHT, C.cedar, M.WoodPlanks)
	for _, y in { 0.2, 0.7 } do
		cyl(m, "Hoop", 0.06, 0.99, L(bx, COUNTER + y, bz) * UPRIGHT, C.brass, M.Metal)
	end
	cyl(m, "BucketWater", 0.05, 0.83, L(bx, COUNTER + 0.885, bz) * UPRIGHT, C.water, M.SmoothPlastic)
	for _, s in { -1, 1 } do
		box(m, "BucketEar", bx - 0.05, bx + 0.05, COUNTER + 0.8, COUNTER + 1.25, bz + s * 0.42 - 0.04, bz + s * 0.42 + 0.04, C.cedar, M.Wood)
	end
	box(m, "BucketHandle", bx - 0.04, bx + 0.04, COUNTER + 1.2, COUNTER + 1.3, bz - 0.44, bz + 0.44, C.cedar, M.Wood)
	-- wall: graded stones from coarse to fine on a shelf, a polished sample under it, cloths past the post
	box(m, "StoneShelf", WALL, -22.85, 6.2, 6.36, z0 + 0.6, z0 + 5.9, C.timber, M.Wood)
	for _, z in { z0 + 0.9, z0 + 5.6 } do
		box(m, "Bracket", WALL, -23.1, 5.7, 6.2, z - 0.07, z + 0.07, C.timberDk, M.Wood)
	end
	local grades = { Color3.fromRGB(96, 92, 86), Color3.fromRGB(140, 120, 100), Color3.fromRGB(184, 160, 128), Color3.fromRGB(210, 196, 170), Color3.fromRGB(236, 228, 210) }
	for i, col in grades do
		local z = z0 + 0.9 + (i - 1) * 0.98
		box(m, "Whetstone", -23.4, -22.95, 6.36, 6.58, z, z + 0.75, col, M.Slate)
	end
	wallSword(m, z0 + 1.2, 4.75, Color3.fromRGB(238, 240, 244), M.Foil, C.plinth, C.iron)
	box(m, "ClothRail", WALL, -23.3, 7.4, 7.6, z1 - 1.75, z1 - 0.15, C.timberDk, M.Wood)
	box(m, "HangingCloth", -23.3, -23.27, 6.0, 7.4, z1 - 1.6, z1 - 1.05, C.cloth, M.Fabric)
	box(m, "HangingCloth", -23.3, -23.27, 6.2, 7.4, z1 - 0.9, z1 - 0.35, C.indigo, M.Fabric)
	sign(m, (z0 + z1) / 2, "研", "POLISHING")
end

do -- etching: a blade cradle with a practice blank, a chisel case and an andon lamp, a pattern scroll on the wall
	local z0, z1 = SECTIONS.EtchingTable[1], SECTIONS.EtchingTable[2]
	local zc = (z0 + z1) / 2
	local m = fresh(S.EtchingTable, "Dress")
	benchSection(m, z0, z1, "Counter")
	for _, z in { zc - 1.9, zc + 1.9 } do
		box(m, "Cradle", -22.0, -21.0, COUNTER, COUNTER + 0.22, z - 0.25, z + 0.25, C.cedar, M.Wood)
		box(m, "Cradle", -21.95, -21.05, COUNTER + 0.22, COUNTER + 0.26, z - 0.22, z + 0.22, C.indigo, M.Fabric)
	end
	box(m, "Blank", -21.56, -21.44, COUNTER + 0.26, COUNTER + 0.31, zc - 2.4, zc + 2.4, C.steel, M.Metal)
	-- the chisel case at the front end, open, its lid against the wall
	box(m, "ChiselCase", -23.15, -22.15, COUNTER, COUNTER + 0.18, z0 + 0.35, z0 + 1.75, C.cedar, M.Wood)
	box(m, "CaseLining", -23.08, -22.22, COUNTER + 0.18, COUNTER + 0.2, z0 + 0.42, z0 + 1.68, C.indigo, M.Fabric)
	box(m, "CaseLid", -23.32, -23.2, COUNTER, COUNTER + 1.3, z0 + 0.35, z0 + 1.75, C.cedar, M.Wood)
	for k = 0, 4 do
		local z = z0 + 0.6 + k * 0.23
		cyl(m, "ChiselHandle", 0.5, 0.1, L(-22.85, COUNTER + 0.25, z), C.brass, M.Metal)
		box(m, "ChiselTip", -22.6, -22.3, COUNTER + 0.22, COUNTER + 0.26, z - 0.03, z + 0.03, C.steel, M.Metal)
	end
	box(m, "StylusRest", -23.05, -22.65, COUNTER, COUNTER + 0.14, z0 + 2.1, z0 + 2.5, C.timberDk, M.Wood)
	cyl(m, "Stylus", 0.9, 0.08, L(-22.85, COUNTER + 0.18, z0 + 2.65) * ALONG_Z, C.timberDk, M.Wood)
	cyl(m, "StylusPoint", 0.12, 0.05, L(-22.85, COUNTER + 0.18, z0 + 3.16) * ALONG_Z, C.brass, M.Metal)
	cyl(m, "InkPot", 0.3, 0.32, L(-22.85, COUNTER + 0.15, z1 - 2.0) * UPRIGHT, C.jar, M.SmoothPlastic)
	-- an andon at the back end: a paper box in a timber frame, lit warm
	local ax, az = -22.75, z1 - 0.85
	box(m, "AndonBase", ax - 0.3, ax + 0.3, COUNTER, COUNTER + 0.1, az - 0.3, az + 0.3, C.timberDk, M.Wood)
	local paper = box(m, "AndonPaper", ax - 0.25, ax + 0.25, COUNTER + 0.1, COUNTER + 0.8, az - 0.25, az + 0.25, C.cloth, M.SmoothPlastic)
	for _, sx in { -1, 1 } do
		for _, sz in { -1, 1 } do
			box(m, "AndonPost", ax + sx * 0.27 - 0.03, ax + sx * 0.27 + 0.03, COUNTER + 0.1, COUNTER + 0.86, az + sz * 0.27 - 0.03, az + sz * 0.27 + 0.03, C.timberDk, M.Wood)
		end
	end
	box(m, "AndonTop", ax - 0.31, ax + 0.31, COUNTER + 0.86, COUNTER + 0.92, az - 0.31, az + 0.31, C.timberDk, M.Wood)
	local light = Instance.new("PointLight")
	light.Color, light.Range, light.Brightness, light.Shadows = Color3.fromRGB(255, 196, 130), 7, 0.8, false
	light.Parent = paper
	-- wall: a pattern scroll by the door end, an etched sample under a shelf of inks, chisels hanging past the post
	box(m, "ScrollMount", WALL, -23.46, 4.45, 8.35, z0, z0 + 1.65, C.indigo, M.Fabric)
	local scroll = box(m, "Scroll", -23.47, -23.43, 4.7, 8.1, z0 + 0.2, z0 + 1.45, Color3.fromRGB(240, 232, 212), M.Fabric)
	label(scroll, Enum.NormalId.Right, { { "炎", 90, Color3.fromRGB(176, 40, 32) } })
	for _, y in { 4.4, 8.4 } do
		cyl(m, "ScrollRod", 1.85, 0.12, L(-23.42, y, z0 + 0.83) * ALONG_Z, C.timberDk, M.Wood)
	end
	local bx = wallSword(m, z0 + 2.0, 4.75, C.steel, M.Metal, C.plinth, C.brass)
	box(m, "EtchBand", bx + 0.02, bx + 0.06, 4.77, 4.85, z0 + 3.4, z0 + 5.9, Color3.fromRGB(176, 40, 32), M.SmoothPlastic)
	box(m, "EtchBand", bx + 0.02, bx + 0.06, 4.87, 4.92, z0 + 3.7, z0 + 5.6, Color3.fromRGB(20, 26, 40), M.SmoothPlastic)
	box(m, "InkShelf", WALL, -22.85, 6.5, 6.66, z0 + 2.2, z0 + 6.5, C.timber, M.Wood)
	for _, z in { z0 + 2.5, z0 + 6.2 } do
		box(m, "Bracket", WALL, -23.1, 6.0, 6.5, z - 0.07, z + 0.07, C.timberDk, M.Wood)
	end
	for i, j in { { 0.4, Color3.fromRGB(30, 30, 40) }, { 0.34, Color3.fromRGB(150, 40, 30) }, { 0.36, C.brass }, { 0.3, C.jar } } do
		cyl(m, "InkJar", j[1] + 0.05, j[1], L(-23.15, 6.66 + (j[1] + 0.05) / 2, z0 + 2.8 + (i - 1) * 0.9) * UPRIGHT, j[2], M.SmoothPlastic)
	end
	box(m, "ChiselBoard", WALL, -23.42, 5.2, 6.6, z1 - 1.2, z1 - 0.1, C.timberDk, M.Wood)
	for k = 0, 3 do
		local z = z1 - 1.0 + k * 0.27
		cyl(m, "ChiselHandle", 0.5, 0.1, L(-23.35, 6.2, z) * UPRIGHT, C.brass, M.Metal)
		box(m, "ChiselTip", -23.37, -23.33, 5.55, 5.96, z - 0.03, z + 0.03, C.steel, M.Metal)
	end
	sign(m, zc, "彫", "ETCHING")
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

	-- the right wall above the finishing bench is dressed by each station (its own racks, sample sword and sign)

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

-- ---------------------------------------------------------------- wall sword shelves (the shop's side walls)
-- Allen 2026-10-22: "The wall sword rack is a bit small, leaving the swords tightly packed together" and "We could create
-- a shelf that holds the 3 swords, look at the reference in concept art" (References/Concept Art/sword shelf.png); he chose
-- to replace all four wall racks with it, same prices, 3 swords each. A chunky warm wooden shelf: three tiers 2 apart,
-- each sword lying along the wall on two cradles, gold caps on the post ends, a crest board with a flower mon on top.
-- Each Displays.WallRack<n> keeps its name, attributes, Origin, InspectPoint and Slot1…3 (DisplaySlot tag, HolderPrompt,
-- Inspect), so ShopService, TycoonService, saved displays (kept by holder path) and customer routes carry on; its mesh
-- Rack (WallSwordRack.fbx, 119 parts) gives way to a Shelf of parts and the slots move onto the tiers. The racks as they
-- were: ServerStorage.Legacy.WallRack<n>_beforeShelf.
-- Display frame: the Origin, on the wall's face; x along the wall the way the swords point, +z into the room, y 0.2 the
-- floor's top. A sword lies along its slot's +x from the grip, edge up and flat to the room (ShopService puts the
-- Handle on the slot). A katana runs from 0.54 behind the grip's centre to 4.10 ahead of it (KatanaHilt's bounds,
-- BladeOffset 0.58 + blade 3.52), so its middle is 1.78 ahead (ShopController's SWORD_MID 1.8); its curved blade stays
-- within 0.35 of the slot's axis across and the tsuba within 0.26 of it in depth.
-- Refinements3 (Allen 2026-10-23: the longsword "pokes into the shelf's side posts"): the longsword, 6.05 long, is now the
-- longest shelf sword (a big sword can't go on a shelf); ShopService.seat centres it between its cradles, and the posts
-- stand 6.2 apart inside, 0.07 to spare at each end. The shelf grew 0.6 away from the wall's structural post (CX 1.0 to
-- 0.7, HW 3.3 to 3.6; WallRack3's end is then 0.05 from the delivery door's open slide). The cradles moved out to 1.95 so
-- the longsword's and falchion's guards clear the grip-side cradle, and AXIS 0.55 to 0.6 lifts the longsword's guard
-- (0.58 either side of the axis) off the board.
-- Refinements (Allen 2026-10-22): no flower mon on the crest; the two cradles stand evenly either side of the shelf's middle
-- (they sat 0.33 to one side); the room-side prong is a low lip so the blade shows; every cradle part carries Holds = its
-- slot's name, so ShopService can centre a displayed sword on them and close them in under a short one.
do
	local CX, HW = 0.7, 3.6 -- the shelf's middle along the wall (a displayed sword's middle) and its half width
	local MID, AXIS, SZ = 1.78, 0.6, 0.8 -- each slot sits MID behind CX, AXIS over its board and SZ out from the wall
	local TIERS = { 1.95, 3.95, 5.95 } -- board tops: Slot1 (bottom) … Slot3
	local CAP = 7.55 -- the top board's underside
	local CRADLE = 1.95 -- each cradle's distance from the shelf's middle (under a longsword's grip, clear of its guard, and its blade)
	local wood, woodDk, planks = Color3.fromRGB(146, 84, 48), Color3.fromRGB(98, 56, 34), Color3.fromRGB(122, 70, 40)
	local solid = { solid = true }
	for i = 1, 4 do
		local d = P.Shop.Displays:FindFirstChild("WallRack" .. i)
		if d then
			local O = d.Origin.CFrame
			local function D(x, y, z) return O * CFrame.new(x, y, z) end
			local function dbox(m, name, x0, x1, y0, y1, z0, z1, col, mat, o)
				return part(m, name, Vector3.new(x1 - x0, y1 - y0, z1 - z0), D((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), col, mat, o)
			end
			local rack = d:FindFirstChild("Rack")
			if rack then rack:Destroy() end
			local m = fresh(d, "Shelf")
			for s = -1, 1, 2 do
				local px = CX + s * (HW - 0.25)
				dbox(m, "Post", px - 0.25, px + 0.25, 0.15, CAP + 0.05, 0.15, 1.55, wood, M.Wood, solid)
				for _, y in { TIERS[1], TIERS[2], TIERS[3], CAP - 0.3 } do -- a gold cap at each board's end, with a stud
					dbox(m, "Corner", px - 0.21, px + 0.21, y - 0.4, y + 0.1, 1.55, 1.6, C.brass, M.Metal)
					part(m, "Stud", Vector3.new(0.18, 0.18, 0.08), D(px, y - 0.15, 1.64) * CFrame.Angles(0, 0, math.pi / 4), C.brass, M.Metal)
				end
			end
			dbox(m, "Back", CX - HW + 0.45, CX + HW - 0.45, 0.25, CAP + 0.07, 0.1, 0.3, planks, M.WoodPlanks, solid)
			dbox(m, "Kick", CX - HW + 0.45, CX + HW - 0.45, 0.15, TIERS[1] - 0.25, 1.15, 1.3, woodDk, M.Wood, solid)
			dbox(m, "Top", CX - HW - 0.05, CX + HW + 0.05, CAP, CAP + 0.4, 0.2, 1.75, wood, M.Wood, solid)
			for k, top in TIERS do
				dbox(m, "Board", CX - HW + 0.45, CX + HW - 0.45, top - 0.3, top, 0.2, 1.4, wood, M.Wood, solid)
				local axis = top + AXIS
				-- cradles under the grip and under the blade: a foot, a prong behind the sword and a low lip in front of it;
				-- the blade's foot is lower, as a katana's spine drops toward the tip (edge up)
				for _, c in { { -CRADLE, 0.14 }, { CRADLE, 0.24 } } do
					local x, foot = CX + c[1], axis - c[2]
					local parts = { dbox(m, "Cradle", x - 0.22, x + 0.22, top - 0.05, foot, SZ - 0.32, SZ + 0.32, woodDk, M.Wood) }
					table.insert(parts, dbox(m, "Cradle", x - 0.12, x + 0.12, foot - 0.05, axis + 0.06, SZ - 0.29, SZ - 0.17, woodDk, M.Wood))
					table.insert(parts, dbox(m, "Cradle", x - 0.12, x + 0.12, foot - 0.05, foot + 0.12, SZ + 0.17, SZ + 0.29, woodDk, M.Wood))
					for _, p in parts do p:SetAttribute("Holds", "Slot" .. k) end
				end
				local slot = d:FindFirstChild("Slot" .. k)
				if slot then -- the sword's x along the wall, its y (the Handle's) into the wall, edge up
					slot.CFrame = O * CFrame.fromMatrix(Vector3.new(CX - MID, axis, SZ), Vector3.xAxis, -Vector3.zAxis, Vector3.yAxis)
				end
			end
			-- crest: a board on the top with a shallow gable over its middle
			dbox(m, "Crest", CX - HW + 0.7, CX + HW - 0.7, CAP + 0.35, CAP + 1.0, 0.25, 0.55, wood, M.Wood)
			for s = -1, 1, 2 do
				part(m, "Gable", Vector3.new(0.38, 0.6, 1.6), D(CX + s * 0.8, CAP + 1.25, 0.4) * CFrame.fromMatrix(Vector3.zero, Vector3.new(0, 0, s), Vector3.yAxis), wood, M.Wood, { wedge = true })
			end
			if d:FindFirstChild("InspectPoint") then d.InspectPoint.CFrame = D(CX, 3, 3.5) end -- where a customer looks from
		end
	end
end

-- ---------------------------------------------------------------- display tables (the shop floor)
-- Allen 2026-10-22: "I imported a SwordTable. I want to use that in replace of our current one. Wire up the swords to be on
-- it", and he likes its bevelled edges. The import (ServerStorage.Buildings3D.SwordTableKit; Table plus three stands
-- sword_white/red/blue, all grey, unanchored) is copied onto each Displays.DisplayTable<n> in wood and brass. Its stands ran
-- across the table, which would show a customer the blades edge-on, so each is turned to run along it (Allen confirmed), one
-- behind another on the table's middle (Allen: "have them aligned in the middle"): Slot1 front, Slot2 middle, Slot3 back.
-- The room-side prongs (prong_<n>_2 once turned) are lowered so they don't cover the blade. Each stand's post, foot,
-- prongs and cap carry Holds = its slot's name (ShopService centres the sword on them, as on the shelves). The display keeps
-- its name, attributes, Origin, InspectPoint and Slot1…3; the mesh table it had goes to
-- ServerStorage.Legacy.DisplayTable<n>_beforeKit. Display frame as the shelves': the Origin on the floor at the table's
-- centre, +z toward the shop front, a sword along its slot's +x from the grip.
do
	local KIT = SS:FindFirstChild("Buildings3D") and SS.Buildings3D:FindFirstChild("SwordTableKit")
	local MID = 1.8 -- a katana's middle ahead of its grip (ShopController's SWORD_MID): the slot sits this far behind a stand's centre
	local AXIS = 4.05 -- the swords' axis over the floor: where the import's prongs hold its katana
	local ROWS = { { 0, 1.4 }, { 0, 0 }, { 0, -1.4 } } -- each slot's stand centre (x, z)
	local LIP = 0.1 -- how far the room-side prongs come down
	local wood, woodDk = Color3.fromRGB(146, 84, 48), Color3.fromRGB(98, 56, 34)
	local TURN = CFrame.Angles(0, math.pi / 2, 0) -- a stand's length (import z) along the table (x), grip to -x
	local SOLID = { tabletop = true, leg = true, apron = true }
	local function dress(p, col, mat, solid)
		p.Anchored = true
		p.Color = col
		p.Material = mat
		p.CanCollide = solid
		p.CanQuery = solid
		p.CanTouch = false
		if p.Size.X * p.Size.Y * p.Size.Z < 2 then p.CastShadow = false end
	end
	for i = 1, 2 do
		local d = KIT and P.Shop.Displays:FindFirstChild("DisplayTable" .. i)
		if d then
			local O = d.Origin.CFrame
			local kitAt = KIT:GetPivot() -- the import's floor centre
			-- the old mesh table, once
			local old = {}
			for _, c in d:GetChildren() do
				if c:IsA("BasePart") and c.Name:match("^SwordTable_") then table.insert(old, c) end
			end
			if #old > 0 then
				local keep = Instance.new("Model")
				keep.Name = "DisplayTable" .. i .. "_beforeKit"
				for _, c in old do c.Parent = keep end
				keep.Parent = LEGACY
			end
			d:SetAttribute("SourceAsset", nil)
			local m = fresh(d, "Table")
			for _, src in KIT.Table:GetDescendants() do
				-- no brass corner caps, and a plain plastic top (Allen 2026-10-25: "remove the corner caps from the tables. Make the
				-- table top have a plastic finish, no wood grains")
				if src:IsA("BasePart") and not src.Name:match("^corner_cap") then
					local p = src:Clone()
					p.CFrame = O * kitAt:ToObjectSpace(src.CFrame)
					local kind = src.Name:match("^(%a+)")
					dress(p, if src.Name:match("foot") then woodDk else wood, if kind == "tabletop" then M.SmoothPlastic else M.Wood, SOLID[kind] == true)
					p.Parent = m
				end
			end
			for k, stand in { KIT.sword_blue.sword_blue_stand, KIT.sword_red.sword_red_stand, KIT.sword_white.sword_white_stand } do
				-- the stand's centre in the import: midway between its two posts, on the floor
				local a, b
				for _, p in stand:GetDescendants() do
					if p:IsA("BasePart") then
						if p.Name:match("post_1$") then a = p elseif p.Name:match("post_2$") then b = p end
					end
				end
				local mid = kitAt:PointToObjectSpace((a.Position + b.Position) / 2)
				local from = kitAt * CFrame.new(mid.X, 0, mid.Z) -- import stand frame
				local to = O * CFrame.new(ROWS[k][1], 0, ROWS[k][2]) * TURN
				local sm = Instance.new("Model")
				sm.Name = "Stand" .. k
				sm.Parent = m
				for _, src in stand:GetDescendants() do
					if src:IsA("BasePart") then
						local p = src:Clone()
						p.CFrame = to * from:ToObjectSpace(src.CFrame)
						if src.Name:match("prong_%d_2$") then p.CFrame -= Vector3.new(0, LIP, 0) end
						local brass = src.Name:match("cap_gold")
						dress(p, if brass then C.brass else woodDk, if brass then M.Metal else M.SmoothPlastic, false) -- plastic like the top (2026-10-25)
						if not src.Name:match("base$") then p:SetAttribute("Holds", "Slot" .. k) end
						p.Parent = sm
					end
				end
				local slot = d:FindFirstChild("Slot" .. k)
				if slot then -- the sword's x along the table, its y (the Handle's) away from the front, edge up
					slot.CFrame = O * CFrame.fromMatrix(Vector3.new(ROWS[k][1] - MID, AXIS, ROWS[k][2]), Vector3.xAxis, -Vector3.zAxis, Vector3.yAxis)
				end
			end
		end
	end
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

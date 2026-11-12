-- Restyles an ore stand and the ore lever with the OreRollerV3 meshes (build_ore_roller_v3.py; Studio imports in
-- ServerStorage.OreRollerV3: Stand, LeverBody, LeverArm, Shrine, ShrineBell, each the uploaded FBX as imported). Paste into the Studio
-- command bar (or MCP execute_luau) after `local Restyle = ...` returns this table.
--   Restyle.stand(standModel): keeps Ore and Pedestal (ForgeService parents the collect prompt to Pedestal; it goes
--     invisible), deletes Foot, Band and Post, adds Wood, Trim and Eye on the stand's floor (Foot's bottom).
--   Restyle.lever(leverModel): keeps Base (invisible; LeverAnimator poses the arm from it) and ArmPivot, deletes the
--     Parts body, Arm and Knob, adds Stone, Wood and Iron on the floor (ArmPivot's height - HINGE) and the arm's Iron,
--     Grip, Wrap and Brass welded to ArmPivot (they swing with it, as Arm and Knob did).
local HINGE = 2.015 -- the hinge over the floor, as in the Blender file
local src = game.ServerStorage:WaitForChild("OreRollerV3")

local LOOK = {
	-- name in the import = { name, material, colour, collides, MaterialVariant }: the game's painted variants (2026-11-07,
	-- Allen: "it seems like the textures are different?"; stock Wood and Slate looked photographic beside the stations)
	["Wood.008"] = { "Wood", Enum.Material.Wood, Color3.fromRGB(232, 182, 110), true, "PaintFurniture" },
	Trim = { "Trim", Enum.Material.Wood, Color3.fromRGB(196, 146, 84), false, "PaintFurniture" },
	Eye = { "Eye", Enum.Material.SmoothPlastic, Color3.fromRGB(60, 40, 28), false },
	["Stone.003"] = { "Stone", Enum.Material.Slate, Color3.fromRGB(135, 130, 120), true, "PaintStone" },
	["Wood.009"] = { "Wood", Enum.Material.Wood, Color3.fromRGB(128, 88, 54), true, "PaintWood" },
	["Iron.001"] = { "Iron", Enum.Material.Metal, Color3.fromRGB(62, 60, 58), false },
	["Iron.002"] = { "ArmIron", Enum.Material.Metal, Color3.fromRGB(62, 60, 58), false },
	Grip = { "Grip", Enum.Material.SmoothPlastic, Color3.fromRGB(204, 54, 38), false }, -- vermilion: reads like the old red knob
	Wrap = { "Wrap", Enum.Material.Fabric, Color3.fromRGB(28, 24, 22), false },
	Brass = { "Brass", Enum.Material.Metal, Color3.fromRGB(184, 134, 43), false },
	-- the shrine draw (Models/Props/ShrineDraw)
	["Stone.004"] = { "ShrineStone", Enum.Material.Slate, Color3.fromRGB(135, 130, 120), true, "PaintStone" },
	["Wood.010"] = { "ShrineWood", Enum.Material.Wood, Color3.fromRGB(150, 108, 70), true, "PaintWood" },
	Lattice = { "Lattice", Enum.Material.SmoothPlastic, Color3.fromRGB(48, 36, 28), false },
	["Roof.005"] = { "ShrineRoof", Enum.Material.ClayRoofTiles, Color3.fromRGB(67, 73, 82), false, "PaintRoof" }, -- the shop roof's grey
	Vermilion = { "Vermilion", Enum.Material.SmoothPlastic, Color3.fromRGB(204, 62, 40), false },
	["Rope.003"] = { "Shimenawa", Enum.Material.Fabric, Color3.fromRGB(196, 152, 80), false },
	["Paper.003"] = { "Shide", Enum.Material.SmoothPlastic, Color3.fromRGB(246, 244, 236), false },
	Bell = { "Bell", Enum.Material.Metal, Color3.fromRGB(196, 150, 60), false },
	Slit = { "Slit", Enum.Material.SmoothPlastic, Color3.fromRGB(40, 32, 24), false },
	RopeRed = { "RopeRed", Enum.Material.Fabric, Color3.fromRGB(196, 40, 36), false },
	RopeWhite = { "RopeWhite", Enum.Material.Fabric, Color3.fromRGB(240, 236, 226), false },
	Tassel = { "Tassel", Enum.Material.Fabric, Color3.fromRGB(196, 40, 36), false },
	-- the sorting benches (build_sort_bench.py)
	Bench = { "Bench", Enum.Material.Wood, Color3.fromRGB(128, 88, 54), true, "PaintWood" },
	["Straw.001"] = { "Straw", Enum.Material.Fabric, Color3.fromRGB(214, 184, 120), false },
	Weave = { "Weave", Enum.Material.Fabric, Color3.fromRGB(160, 124, 68), false },
}
local BELL_PIVOT, FRONT = 3.95, -1.2 -- the shrine's crossbeam underside over the floor, and its frame's depth (Blender y)

-- the import's frame: the Blender origin, found from a part and its Blender bbox centre height (the import sits each
-- model's lowest point on y 0, so the arm, which reaches 0.24 below its hinge, is lifted by that)
-- `at` is that centre in the part's own axes (Blender (x, y, z) -> (-x, z, y)); the result keeps the import's turn
-- (Studio may insert it facing the camera), so place() works in the import's frame
local function origin(model: Model, name: string, at: Vector3): CFrame
	local p = model:FindFirstChild(name)
	assert(p and p:IsA("BasePart"), model:GetFullName() .. " has no part " .. name)
	return p.CFrame * CFrame.new(-at)
end

local function weldAll(pivot: BasePart, parts: { BasePart })
	for _, p in parts do
		local w = Instance.new("WeldConstraint")
		w.Part0, w.Part1 = pivot, p
		w.Parent = p
	end
end

local OLD_LEVER = { Slot1 = true, Arm = true, Knob = true, Stone = true, Wood = true, Iron = true, ArmIron = true, Grip = true,
	Wrap = true, Brass = true }
local function clearLever(lever: Model)
	for _, p in lever:GetChildren() do
		if p:IsA("BasePart") and (OLD_LEVER[p.Name] or p.Name:match("^Body") or p.Name:match("^Panel") or p.Name:match("^BaseTrim")
			or p.Name:match("^Hdl")) then
			p:Destroy()
		end
	end
end

local function place(model: Model, ref: CFrame, frame: CFrame, parent: Instance, anchored: boolean): { BasePart }
	local made = {}
	for _, p in model:GetChildren() do
		local look = LOOK[p.Name]
		if p:IsA("MeshPart") and look then
			local c = p:Clone()
			c.Name, c.Material, c.Color = look[1], look[2], look[3]
			c.MaterialVariant = look[5] or ""
			c.CanCollide, c.CanQuery, c.CanTouch = look[4], look[4], false
			if look[4] then
				c.CollisionFidelity = Enum.CollisionFidelity.Box
			end
			c.Anchored = anchored
			c.CFrame = frame * ref:ToObjectSpace(p.CFrame)
			c.Parent = parent
			table.insert(made, c)
		end
	end
	return made
end

local Restyle = {}

-- a child that must be there: a clear error instead of indexing nil
local function need(parent: Instance, name: string): BasePart
	local c = parent:FindFirstChild(name)
	assert(c and c:IsA("BasePart"), parent:GetFullName() .. " has no part " .. name)
	return c
end

function Restyle.stand(stand: Model)
	local foot = stand:FindFirstChild("Foot") :: BasePart?
	local pedestal = need(stand, "Pedestal")
	if not foot then
		return -- done already
	end
	local floor = foot.Position.Y - foot.Size.Y / 2
	local m = src.Stand
	place(m, origin(m, "Wood.008", Vector3.new(0, 1.38, 0)), CFrame.new(pedestal.Position.X, floor, pedestal.Position.Z) * pedestal.CFrame.Rotation, stand, true)
	for _, n in { "Foot", "Band", "Post" } do
		local p = stand:FindFirstChild(n)
		if p then
			p:Destroy()
		end
	end
	pedestal.Transparency = 1
end

-- the floor under a stand: its Foot's bottom, or (once restyled) 2.615 under its ingot's bottom
local function floorOf(stand: Model): number
	local foot = stand:FindFirstChild("Foot")
	if foot and foot:IsA("BasePart") then
		return foot.Position.Y - foot.Size.Y / 2
	end
	local ore = need(stand, "Ore")
	return ore.Position.Y - ore.Size.Y / 2 - 2.615
end

-- Restyle.tray(standModel): the slot becomes a straw tray (Straw, Weave) where the ingot lay; Foot, Band, Post (or the
-- sanbo's Wood, Trim, Eye) go, Ore and the invisible Pedestal stay. Inside the stand, so it hides with the slot.
function Restyle.tray(stand: Model)
	local pedestal = need(stand, "Pedestal")
	if stand:FindFirstChild("Straw") then
		return -- done already
	end
	local floor = floorOf(stand)
	local m = src.Tray
	-- along the ingot (the Pedestal is turned 90 degrees; a square never showed it)
	place(m, origin(m, "Straw.001", Vector3.new(0, 2.66, 0)), CFrame.new(pedestal.Position.X, floor, pedestal.Position.Z) * need(stand, "Ore").CFrame.Rotation, stand, true)
	for _, n in { "Foot", "Band", "Post", "Wood", "Trim", "Eye" } do
		local p = stand:FindFirstChild(n)
		if p then
			p:Destroy()
		end
	end
	pedestal.Transparency = 1
end

-- Restyle.benches(parent, stands): a sorting bench under each row of stands (stands sharing a Z), centred on the row,
-- in a Model "Benches" under `parent`; it shows in every look (no Upgrade), the trays on it come with the slots.
function Restyle.benches(parent: Instance, stands: { Model })
	if parent:FindFirstChild("Benches") then
		return -- done already
	end
	local rows: { [number]: { Model } } = {}
	for _, s in stands do
		local z = math.round(need(s, "Pedestal").Position.Z * 10) / 10
		rows[z] = rows[z] or {}
		table.insert(rows[z], s)
	end
	local benches = Instance.new("Model")
	benches.Name = "Benches"
	local m = src.Bench
	for _, row in rows do
		local x = 0
		for _, s in row do
			x += need(s, "Pedestal").Position.X
		end
		local p = need(row[1], "Pedestal")
		local at = CFrame.new(x / #row, floorOf(row[1]), p.Position.Z) * need(row[1], "Ore").CFrame.Rotation
		place(m, origin(m, "Bench", Vector3.new(0, 1.26, 0)), at, benches, true)
	end
	benches.Parent = parent
end

function Restyle.lever(lever: Model)
	local pivot = need(lever, "ArmPivot")
	local base = need(lever, "Base")
	if lever:FindFirstChild("Grip") then
		return -- done already
	end
	local body, arm = src.LeverBody, src.LeverArm
	local floor = CFrame.new(base.Position.X, pivot.Position.Y - HINGE, base.Position.Z) * base.CFrame.Rotation
	clearLever(lever)
	place(body, origin(body, "Stone.003", Vector3.new(0, 0.16, 0)), floor, lever, true)
	-- the arm: handle A, the red ball knob (2026-11-07, Allen: "i like the red ball knob"; src.LeverArm, the vermilion
	-- cord grip, is no longer used)
	Restyle.handle(lever, "A")
	base.Transparency = 1
end

-- Restyle.handle(leverModel, letter): swaps the restyled lever's arm for handle option A (red ball knob), B (turned
-- wooden grip), C (wooden T-bar) or D (rope-bound wooden haft) from src.Handles (build_lever_handles.py), welded to
-- ArmPivot like the arm it replaces (2026-11-07, Allen: "i dont like the handle design", "build them all so i can compare").
local HANDLE_LOOK = {
	Iron = { Enum.Material.Metal, Color3.fromRGB(62, 60, 58) },
	Brass = { Enum.Material.Metal, Color3.fromRGB(184, 134, 43) },
	Knob = { Enum.Material.SmoothPlastic, Color3.fromRGB(204, 54, 38) },
	Grip = { Enum.Material.Wood, Color3.fromRGB(232, 182, 110), "PaintFurniture" },
	Cap = { Enum.Material.Wood, Color3.fromRGB(70, 46, 32), "PaintWoodDark" },
	Bar = { Enum.Material.Wood, Color3.fromRGB(232, 182, 110), "PaintFurniture" },
	Haft = { Enum.Material.Wood, Color3.fromRGB(160, 112, 66), "PaintWoodDark" },
	Rope = { Enum.Material.Fabric, Color3.fromRGB(214, 184, 120) },
}
local ARM_PARTS = { ArmIron = true, Grip = true, Wrap = true, Brass = true }
function Restyle.handle(lever: Model, letter: string)
	local pivot = need(lever, "ArmPivot")
	for _, p in lever:GetChildren() do
		if p:IsA("BasePart") and (ARM_PARTS[p.Name] or p.Name:match("^Hdl")) then
			p:Destroy()
		end
	end
	local m = src.Handles
	local ref = origin(m, "HdlA_Iron", Vector3.new(0, 0.855, 0)) -- every option shares the hinge origin
	for _, p in m:GetChildren() do
		local l, kind = p.Name:match("^Hdl(%u)_(%a+)$")
		local look = if kind then HANDLE_LOOK[kind] else nil
		if p:IsA("MeshPart") and l == letter and look then
			local c = p:Clone()
			c.Material, c.Color, c.MaterialVariant = look[1], look[2], look[3] or ""
			c.Anchored, c.CanCollide, c.CanQuery, c.CanTouch = false, false, false, false
			c.CFrame = pivot.CFrame * ref:ToObjectSpace(p.CFrame)
			c.Parent = lever
			weldAll(pivot, { c })
		end
	end
end

-- Restyle.autoRoller(autoRollerModel, kind): WorldStore.AutoRoller rebuilt as "WW" (water wheel), "KD" (karakuri doll)
-- or "CW" (clockwork weight) from src.AutoRollers (build_auto_rollers.py; 2026-11-07, Allen: "i feel like the auto
-- roller doesn't look good", "Build all three"). The old meshes go; Anchor and the Locked/Owned ball lamps stay, moved
-- to the option's lamp point. Turning parts (Wheel, Hub, Gear, Drum) get the Spin pose in the new Axle's space, so
-- WorldStoreController turns them as it turned the flywheel. The doll's arm is DollArm, anchored, with its shoulder
-- in the DollShoulder attribute (a CFrame) for whatever animates it.
local AUTO_LOOK = {
	Stone = { Enum.Material.Slate, Color3.fromRGB(135, 130, 120), true, "PaintStone" },
	Water = { Enum.Material.SmoothPlastic, Color3.fromRGB(90, 150, 200), false },
	Wood = { Enum.Material.Wood, Color3.fromRGB(128, 88, 54), true, "PaintWood" },
	Bamboo = { Enum.Material.Wood, Color3.fromRGB(120, 160, 70), false, "PaintFurniture" },
	Wheel = { Enum.Material.Wood, Color3.fromRGB(96, 64, 40), false, "PaintWoodDark" },
	Hub = { Enum.Material.Metal, Color3.fromRGB(58, 58, 62), false },
	Axle = { Enum.Material.Metal, Color3.fromRGB(58, 58, 62), false },
	Robe = { Enum.Material.SmoothPlastic, Color3.fromRGB(196, 52, 40), false },
	Obi = { Enum.Material.SmoothPlastic, Color3.fromRGB(40, 34, 52), false },
	Face = { Enum.Material.SmoothPlastic, Color3.fromRGB(241, 226, 200), false },
	Hair = { Enum.Material.SmoothPlastic, Color3.fromRGB(28, 24, 22), false },
	Arm = { Enum.Material.SmoothPlastic, Color3.fromRGB(196, 52, 40), false },
	Gear = { Enum.Material.Metal, Color3.fromRGB(184, 134, 43), false },
	Drum = { Enum.Material.Wood, Color3.fromRGB(96, 64, 40), false, "PaintWoodDark" },
	Rope = { Enum.Material.Fabric, Color3.fromRGB(214, 184, 120), false },
	Weight = { Enum.Material.Slate, Color3.fromRGB(135, 130, 120), false, "PaintStone" },
}
-- each option's stone centre and lamp point, in Roblox axes from the Blender origin (Blender (x, y, z) -> (-x, z, y))
local AUTO = {
	WW = { stone = Vector3.new(0.2, 0.37, 0), lamp = Vector3.new(-0.9, 2.75, -1.05) },
	KD = { stone = Vector3.new(-2.2, 0.12, 0), lamp = Vector3.new(-2.2, 3.72, -0.05), shoulder = Vector3.new(-2.68, 2.78, -0.05) },
	CW = { stone = Vector3.new(0.4, 0.12, 0), lamp = Vector3.new(0.4, 4.45, 0) },
}
local SPINS = { Wheel = true, Hub = true, Gear = true, Drum = true }
function Restyle.autoRoller(model: Model, kind: string)
	local spec = AUTO[kind]
	assert(spec, "autoRoller kind should be WW, KD or CW")
	local stone = need(model, "Stone")
	-- the old roller's Blender origin: its stone's centre on the floor, in the stone's own axes
	local frame = CFrame.new(stone.Position.X, stone.Position.Y - stone.Size.Y / 2, stone.Position.Z) * stone.CFrame.Rotation
	for _, n in { "Wood", "Stone", "Iron", "Axle", "Flywheel", "Hub" } do
		local p = model:FindFirstChild(n)
		if p then
			p:Destroy()
		end
	end
	local m = src.AutoRollers
	local ref = origin(m, kind .. "_Stone", spec.stone)
	local made: { [string]: BasePart } = {}
	for _, p in m:GetChildren() do
		local k, part = p.Name:match("^(%u%u)_(%a+)$")
		local look = if part then AUTO_LOOK[part] else nil
		if p:IsA("MeshPart") and k == kind and look then
			local c = p:Clone()
			c.Name = if part == "Arm" then "DollArm" else part
			c.Material, c.Color, c.MaterialVariant = look[1], look[2], look[4] or ""
			c.CanCollide, c.CanQuery, c.CanTouch = look[3], look[3], false
			if look[3] then
				c.CollisionFidelity = Enum.CollisionFidelity.Box
			end
			if part == "Water" then
				c.Transparency = 0.25
			end
			c.Anchored = true
			c.CFrame = frame * ref:ToObjectSpace(p.CFrame)
			c.Parent = model
			made[part] = c
		end
	end
	local axle = made.Axle
	if axle then
		for part, c in made do
			if SPINS[part] then
				c:SetAttribute("Spin", axle.CFrame:ToObjectSpace(c.CFrame))
			end
		end
	end
	if spec.shoulder and made.Arm then
		made.Arm:SetAttribute("DollShoulder", frame * CFrame.new(spec.shoulder))
	end
	for _, group in { "Locked", "Owned" } do
		local g = model:FindFirstChild(group)
		local lamp = if g then g:FindFirstChild("Lamp") else nil
		if lamp and lamp:IsA("BasePart") then
			lamp.CFrame = frame * CFrame.new(spec.lamp)
		end
	end
end

-- Restyle.shrine(leverModel): the lever becomes a wayside shrine facing +Z (the path side, where players come from):
-- the fixed Shrine meshes on the floor, ArmPivot moved up to the bell frame's crossbeam (upright at rest, RestDegrees 0;
-- PulledDegrees 20 swings the rope toward the player), the Bell, Slit, rope and Tassel welded to it. Base stays invisible.
function Restyle.shrine(lever: Model)
	local pivot = need(lever, "ArmPivot")
	local base = need(lever, "Base")
	if lever:FindFirstChild("Bell") then
		return -- done already
	end
	local shrine, bell = src.Shrine, src.ShrineBell
	local floor = CFrame.new(base.Position.X, pivot.Position.Y - HINGE, base.Position.Z) * base.CFrame.Rotation * CFrame.Angles(0, math.pi, 0)
	clearLever(lever)
	place(shrine, origin(shrine, "Stone.004", Vector3.new(0, 0.15, -0.175)), floor, lever, true)
	pivot.CFrame = floor * CFrame.new(0, BELL_PIVOT, FRONT)
	pivot:SetAttribute("RestDegrees", 0)
	pivot:SetAttribute("PulledDegrees", 20)
	weldAll(pivot, place(bell, origin(bell, "Bell", Vector3.new(0, -0.36, 0)), pivot.CFrame, lever, false))
	base.Transparency = 1
end

return Restyle

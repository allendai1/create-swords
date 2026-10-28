-- build_style_test.luau: the Genshin-style look on the live map (2026-10-22), switchable. First a test on the gate
-- street (Allen: "build the Genshin-style test of the gate street: lighting, painted road/wall/roof textures, one smooth
-- tree and one softened building"), then rolled out (Allen: "Roll the Genshin style out across the village: smooth
-- trees for the pines and bamboo, rounded mountains, a painted sky, and the other houses and plot softened.").
-- Run in Studio (Edit) through MCP execute_luau: loadstring(game.ServerStorage.Builders.build_style_test.Source)("on")
-- or ("off"). "on" saves every property it changes as a StyleTest_<Property> attribute first, so "off" puts the old
-- look back exactly; rerunning "on" is safe. The rollout's smooth trees and rounded mountains were removed the same day
-- (Allen: "Remove all the trees and mountains you added, they're hideous"); the low-poly trees and block mountains stay.
-- What "on" does:
--   Lighting: clear afternoon, cool soft shadows, blue haze, more saturation, softer bloom. The sky is Allen's own
--     toolbox skybox (2026-10-22, replacing the painted one from Models/Village/style_sky.py); the builder leaves it be.
--   Textures: MaterialVariants on Ground, Slate, Plaster, Cobblestone, Wood (dark timber its own), WoodPlanks and
--     ClayRoofTiles parts of the Village and of the plot's buildings (Workshop, Starter and Upgraded shells, delivery bay, yard,
--     delivery door), with livelier colours. Stations, displays and pads are left alone (their colours mean things).
--   Buildings, in place (no clones, so scripts keep their parts): upright slender wood ...Post / ...Pillar parts turn
--     into chunky round posts (village houses also get stone plinths), ...Ridge and ...Fascia parts turn round, a ridge
--     gets ball end caps, a clay ...Roof gets a rolled eave on its low edge and the Inazuma blue-violet if it was a dark
--     grey. Added parts go in a StyleAdd folder beside the part, inside the same Roof model (RoofHider fades them with
--     it) and the same building (TycoonController hides them with it).
--   Plot palette: the shop and workshop take Autumn Terracotta (end of the script).

local mode = ... or "on"
local Lighting = game:GetService("Lighting")
local MS = game:GetService("MaterialService")
local village = workspace:FindFirstChild("Village")
assert(village, "Workspace.Village missing")
local plot = workspace:FindFirstChild("Plot")
local backdrop = village.Atmosphere.Backdrop
local M = Enum.Material

-- Textures: FreeStylized 2K (Models/Village/freestylized_textures.py; royalty free, commercial use allowed), except the
-- roof, still painted by Models/Village/style_textures.py.
local ORG, REG = Enum.MaterialPattern.Organic, Enum.MaterialPattern.Regular
local VARIANTS = { -- material -> variant name, colour, normal, roughness, studs per tile, pattern
	[M.Ground] = { "PaintEarth", "rbxassetid://89948982146959", "rbxassetid://126058962761680", "rbxassetid://95097504493005", 24, ORG }, -- ground_02
	[M.Slate] = { "PaintStone", "rbxassetid://99302594416483", "rbxassetid://92973951386631", "rbxassetid://129688876765248", 10, ORG }, -- ground_stones_01
	[M.Plaster] = { "PaintPlaster", "rbxassetid://114247096053626", "rbxassetid://120651475898439", "rbxassetid://123719430392581", 12, ORG }, -- concrete_wall_01
	[M.Cobblestone] = { "PaintStoneWall", "rbxassetid://102112150562734", "rbxassetid://78427713544782", "rbxassetid://87281238737955", 8, REG }, -- stone_wall_02
	[M.Wood] = { "PaintWood", "rbxassetid://72745151340574", "rbxassetid://140198157126085", "rbxassetid://100215486081163", 6, REG }, -- wood_10
	[M.WoodPlanks] = { "PaintPlanks", "rbxassetid://105972709052239", "rbxassetid://121504611557776", "rbxassetid://128123986434735", 8, REG }, -- wood_planks_04 (wood_11 until 2026-10-25)
	[M.ClayRoofTiles] = { "PaintRoof", "rbxassetid://137400459495419", "rbxassetid://106493324917155", "rbxassetid://121070485923113", 6, REG }, -- painted
}
-- dark timber (original colour value under DARK) takes the charred wood_02 instead of PaintWood
local DARK, WOOD_DARK = 0.3, { "PaintWoodDark", "rbxassetid://93837455108828", "rbxassetid://124033836867990", "rbxassetid://137594363565195", 6, REG }
-- WoodPlanks parts named Crate take the crate face (wood_planks_23, one per side), the workshop floor big stone tiles
-- (floor_tiles_01) instead of PaintStone (2026-10-25)
local CRATE = { "PaintCrate", "rbxassetid://130954007368883", "rbxassetid://100407329175578", "rbxassetid://114032215629679", 2.4, REG }
local FLOOR = { "PaintFloor", "rbxassetid://101845192412037", "rbxassetid://121592573740112", "rbxassetid://91814594551450", 12, REG }
-- shelves and tables (Allen 2026-10-25: "the wood material on the shelves and tables, can we find a replacement on the
-- site too"): plain Wood parts of the shop displays, the cashier counter and the workshop stations take wood_09; their
-- colours stay (they mean things)
local FURNITURE = { "PaintFurniture", "rbxassetid://80000437047508", "rbxassetid://111894518273687", "rbxassetid://121990948339552", 5, REG }
local LIGHT = {
	ClockTime = 15.2, Brightness = 2.7, ExposureCompensation = -0.05,
	OutdoorAmbient = Color3.fromRGB(150, 162, 196), ColorShift_Top = Color3.fromRGB(255, 226, 190),
	EnvironmentSpecularScale = 1, ShadowSoftness = 0.6, -- 1 (was 0.2): metal reflects again; the painted tiles are rough anyway
}
local EFFECTS = {
	Atmosphere = { Density = 0.32, Offset = 0.22, Color = Color3.fromRGB(206, 224, 242), Decay = Color3.fromRGB(110, 146, 190), Glare = 0.15, Haze = 1.6 },
	ColorCorrection = { Brightness = 0.03, Contrast = -0.04, Saturation = 0.28, TintColor = Color3.fromRGB(255, 248, 238) },
	Bloom = { Intensity = 0.5, Size = 40, Threshold = 1.2 },
	SunRays = { Intensity = 0.06, Spread = 0.3 },
}
local PAL = {
	roof = Color3.fromRGB(84, 78, 128), ridge = Color3.fromRGB(62, 58, 100), eave = Color3.fromRGB(98, 92, 146),
	stone = Color3.fromRGB(156, 150, 142),
}
-- ---------------------------------------------------------------- saving and restoring
-- an original is saved once as an attribute (enums as "Enum:<type>:<name>", which attributes can't hold)
local function set(inst, prop, value)
	local key = "StyleTest_" .. prop
	if inst:GetAttribute(key) == nil then
		local old = inst[prop]
		inst:SetAttribute(key, typeof(old) == "EnumItem" and ("Enum:%s:%s"):format(tostring(old.EnumType), old.Name) or old)
	end
	inst[prop] = value
end
local function restore(inst)
	for key, v in inst:GetAttributes() do
		local prop = key:match("^StyleTest_(.+)$")
		if prop then
			local et, en
			if type(v) == "string" then et, en = v:match("^Enum:(%w+):(%w+)$") end
			inst[prop] = if et then (Enum :: any)[et][en] else v
			inst:SetAttribute(key, nil)
		end
	end
end

-- the parts the look applies to: the Village (not the block mountains) and the plot's buildings
local function roots()
	local list = { village }
	if plot then
		for _, path in { { "Workshop" }, { "Shop", "Starter" }, { "Shop", "Upgraded" }, { "DeliveryBay" }, { "Yard" }, { "Shop", "DeliveryDoor" }, { "Shop", "DeliveryWall" }, { "Shop", "Interior" } } do
			local inst = plot
			for _, n in path do inst = inst and inst:FindFirstChild(n) end
			if inst then table.insert(list, inst) end
		end
	end
	return list
end
local function furniture() -- the plain Wood parts the shelves-and-tables texture goes on
	local parts = {}
	for _, path in { { "Shop", "Displays" }, { "Shop", "CashierCounter" }, { "Smithy" } } do
		local inst = plot
		for _, n in path do inst = inst and inst:FindFirstChild(n) end
		for _, p in inst and inst:GetDescendants() or {} do
			if p:IsA("BasePart") and p.Material == M.Wood and (p.MaterialVariant == "" or p.MaterialVariant == FURNITURE[1]) then
				table.insert(parts, p)
			end
		end
	end
	return parts
end
local function scope()
	local parts = {}
	for _, root in roots() do
		for _, p in root:GetDescendants() do
			if p:IsA("BasePart") and not p:IsDescendantOf(backdrop) and p.Parent.Name ~= "StyleAdd" then
				table.insert(parts, p)
			end
		end
	end
	return parts
end

if mode == "off" then
	restore(Lighting)
	for _, e in Lighting:GetChildren() do restore(e) end
	for _, root in roots() do
		for _, d in root:GetDescendants() do
			if d:IsA("Folder") and d.Name == "StyleAdd" then d:Destroy() end
		end
	end
	for _, p in scope() do restore(p) end
	for _, p in furniture() do restore(p) end
	return "style off: lighting, materials, colours and shapes restored"
end

-- ---------------------------------------------------------------- lighting, materials, colours
for k, v in LIGHT do set(Lighting, k, v) end
for name, props in EFFECTS do
	local e = Lighting:FindFirstChild(name)
	if e then for k, v in props do set(e, k, v) end end
end
local function variant(material, d)
	local v = MS:FindFirstChild(d[1]) or Instance.new("MaterialVariant")
	v.Name, v.BaseMaterial = d[1], material
	v.ColorMap, v.NormalMap, v.RoughnessMap, v.MetalnessMap = d[2], d[3], d[4], ""
	v.StudsPerTile, v.MaterialPattern = d[5], d[6]
	v.Parent = MS
end
for material, d in VARIANTS do variant(material, d) end
variant(M.Wood, WOOD_DARK)
variant(M.WoodPlanks, CRATE)
variant(M.Slate, FLOOR)
variant(M.Wood, FURNITURE)

local function vivid(c) -- more saturation (light colours less, so the road and plaster don't go yellow), lifted darks
	local h, s, v = c:ToHSV()
	return Color3.fromHSV(h, math.min(1, s * (1.3 - 0.25 * v)), v ^ 0.85)
end
local function darkGrey(c)
	local _, s, v = c:ToHSV()
	return s < 0.3 and v < 0.55
end

-- ---------------------------------------------------------------- buildings, in place
local function add(near, name, size, cf, color, material, shape)
	local f = near.Parent:FindFirstChild("StyleAdd")
	if not f then
		f = Instance.new("Folder")
		f.Name, f.Parent = "StyleAdd", near.Parent
	end
	local p = Instance.new("Part")
	p.Name, p.Size, p.CFrame, p.Color, p.Material, p.Shape = name, size, cf, color, material, shape
	local d = VARIANTS[material]
	if d then p.MaterialVariant = d[1] end
	p.Anchored, p.CanCollide, p.CanQuery, p.CanTouch = true, false, false, false
	p.TopSurface, p.BottomSurface = Enum.SurfaceType.Smooth, Enum.SurfaceType.Smooth
	p.Parent = f
	return p
end
local CYL, BALL = Enum.PartType.Cylinder, Enum.PartType.Ball
local TO_Y, TO_Z = CFrame.Angles(0, 0, math.pi / 2), CFrame.Angles(0, math.pi / 2, 0) -- turn a cylinder's X axis to Y / Z

-- a block's long axis as the cylinder's axis, in place; d: the new diameter
local function round(p, d)
	local s = p:GetAttribute("StyleTest_Size") or p.Size
	local cf = p:GetAttribute("StyleTest_CFrame") or p.CFrame
	local len, turn
	if s.X >= s.Y and s.X >= s.Z then len, turn = s.X, CFrame.identity
	elseif s.Y >= s.Z then len, turn = s.Y, TO_Y
	else len, turn = s.Z, TO_Z end
	set(p, "Shape", CYL)
	set(p, "Size", Vector3.new(len, d, d))
	set(p, "CFrame", cf * turn)
	return cf, s, len, turn
end

local function mid(s) -- the middle of a size's three extents
	return s.X + s.Y + s.Z - math.max(s.X, s.Y, s.Z) - math.min(s.X, s.Y, s.Z)
end

local function soften(p, house)
	if not p:IsA("Part") then return end
	local n = p.Name
	local s0 = p:GetAttribute("StyleTest_Size") or p.Size
	local cf0 = p:GetAttribute("StyleTest_CFrame") or p.CFrame
	if (n:match("Post$") or n:match("Pillar$")) and p.Material == M.Wood and math.abs(cf0.UpVector.Y) > 0.99
		and s0.Y > 3 * math.max(s0.X, s0.Z) and math.max(s0.X, s0.Z) <= 2.2 then
		round(p, math.max(s0.X, s0.Z) * 1.3)
		local foot = cf0.Position - Vector3.new(0, s0.Y / 2, 0)
		if house and foot.Y < 1 then -- a stone plinth round the foot (ends inside it, top clear of every ground layer)
			add(p, "Plinth", Vector3.new(0.7, s0.X * 2.1, s0.X * 2.1), CFrame.new(foot.X, 0.5, foot.Z) * TO_Y, PAL.stone, M.Slate, CYL)
		end
	elseif n:match("Ridge$") and p.Material == M.ClayRoofTiles then
		local cf, _, len, turn = round(p, math.max(mid(s0) * 1.15, 1.2))
		if darkGrey(p:GetAttribute("StyleTest_Color") or p.Color) then set(p, "Color", PAL.ridge) end
		local axis = (cf * turn).RightVector
		for sgn = -1, 1, 2 do
			add(p, "RidgeCap", Vector3.one * (p.Size.Y + 0.5), CFrame.new(cf.Position + axis * sgn * (len / 2 + 0.2)), p.Color, M.ClayRoofTiles, BALL)
		end
	elseif n:match("Fascia$") and p.Material == M.Wood then
		round(p, mid(s0) * 1.5)
	elseif n:match("Roof$") and p.Material == M.ClayRoofTiles then
		if darkGrey(p:GetAttribute("StyleTest_Color") or p.Color) then set(p, "Color", PAL.roof) end
		-- the lowest of the four edge midpoints; the roll runs along that edge
		local best, along, lenA = nil, nil, 0
		for _, e in { { Vector3.new(s0.X / 2, 0, 0), "Z" }, { Vector3.new(-s0.X / 2, 0, 0), "Z" }, { Vector3.new(0, 0, s0.Z / 2), "X" }, { Vector3.new(0, 0, -s0.Z / 2), "X" } } do
			local w = cf0:PointToWorldSpace(e[1])
			if not best or w.Y < best.Y then best, along = w, e[2] end
		end
		if cf0.Position.Y - best.Y > 0.5 then -- pitched
			lenA = along == "X" and s0.X or s0.Z
			local rot = cf0.Rotation * (along == "X" and CFrame.identity or TO_Z)
			add(p, "Eave", Vector3.new(lenA + 0.5, 1.1, 1.1), CFrame.new(best) * rot * CFrame.new(0, -0.1, 0), PAL.eave, M.ClayRoofTiles, CYL)
		end
	end
end

for _, p in scope() do
	local d = VARIANTS[p.Material]
	if d == VARIANTS[M.Wood] and select(3, (p:GetAttribute("StyleTest_Color") or p.Color):ToHSV()) < DARK then d = WOOD_DARK end
	if d == VARIANTS[M.WoodPlanks] and p.Name == "Crate" then d = CRATE end
	if d == VARIANTS[M.Slate] and plot and p == plot.Workshop:FindFirstChild("Floor") then d = FLOOR end
	if d then set(p, "MaterialVariant", d[1]) end
	if p.Material ~= M.Neon then set(p, "Color", vivid(p:GetAttribute("StyleTest_Color") or p.Color)) end
end
local furnished = furniture()
for _, p in furnished do set(p, "MaterialVariant", FURNITURE[1]) end
local nAdd = 0
for _, root in roots() do
	for _, f in root:GetDescendants() do -- clear earlier additions, so a rerun doesn't double them
		if f:IsA("Folder") and f.Name == "StyleAdd" then f:Destroy() end
	end
end
for _, p in scope() do
	soften(p, p:IsDescendantOf(village.Houses))
end
for _, root in roots() do
	for _, f in root:GetDescendants() do
		if f:IsA("Folder") and f.Name == "StyleAdd" then nAdd += #f:GetChildren() end
	end
end

-- The plot's palette, Autumn Terracotta (Allen 2026-10-22, picked from five copies on the lots): the shop and
-- workshop's roof, timber, slats, plaster and noren, found by the colour the steps above give them (so every rerun
-- maps the same); the village keeps its own colours.
local rgb = Color3.fromRGB
local AUTUMN = { roof = rgb(176, 88, 54), timber = rgb(70, 46, 32), slat = rgb(160, 112, 66), plaster = rgb(242, 228, 198), noren = rgb(44, 86, 64) }
local BLACK, WHITE = Color3.new(0, 0, 0), Color3.new(1, 1, 1)
local PLOT_ROLE = {
	["544e80"] = AUTUMN.roof, ["3e3a64"] = AUTUMN.roof:Lerp(BLACK, 0.28), ["625c92"] = AUTUMN.roof:Lerp(WHITE, 0.12),
	["462a1a"] = AUTUMN.timber, ["573621"] = AUTUMN.slat, ["6b4224"] = AUTUMN.slat:Lerp(AUTUMN.timber, 0.35),
	["ebe4d5"] = AUTUMN.plaster, ["e0ca9e"] = AUTUMN.plaster:Lerp(BLACK, 0.06), ["1e346f"] = AUTUMN.noren,
	["291b14"] = AUTUMN.timber:Lerp(BLACK, 0.4),
}
local nPalette = 0
for _, root in roots() do
	if root ~= village then
		for _, p in root:GetDescendants() do
			local c = p:IsA("BasePart") and PLOT_ROLE[p.Color:ToHex():lower()]
			if c then
				set(p, "Color", c)
				nPalette += 1
			end
		end
	end
end

-- A bright shop (Allen 2026-10-22: "i want our shop to be lit up and bright ... i think it'll make the swords pop
-- more too"): the shop's roof and ceiling cast no shadow (RoofHider only fades them, so the room sat in their shade),
-- a pale floor, and soft lamps under the roof (a StyleAdd folder in each shop, so it locks with its building and
-- "off" removes it).
local SHOP_FLOOR = rgb(198, 166, 124)
local nLamps = 0
for _, name in { "Starter", "Upgraded" } do
	local shop = plot and plot.Shop:FindFirstChild(name)
	if shop then
		for _, part in { shop.Shell:FindFirstChild("Roof"), shop.Shell:FindFirstChild("Ceiling", true) } do
			for _, p in part and part:GetDescendants() or {} do
				if p:IsA("BasePart") then set(p, "CastShadow", false) end
			end
		end
		local floor = shop:FindFirstChild("Floor")
		if floor then
			set(floor, "Color", SHOP_FLOOR)
			local folder = shop:FindFirstChild("StyleAdd") or Instance.new("Folder")
			folder.Name = "StyleAdd"
			folder:ClearAllChildren()
			folder.Parent = shop
			local rows = if floor.Size.Z > 34 then 3 else 2
			for i = 1, 2 do
				for j = 1, rows do
					local lamp = Instance.new("Part")
					lamp.Name = "ShopLamp"
					lamp.Size = Vector3.one * 0.2
					lamp.Transparency = 1
					lamp.Anchored, lamp.CanCollide, lamp.CanQuery, lamp.CanTouch, lamp.CastShadow = true, false, false, false, false
					lamp.CFrame = floor.CFrame * CFrame.new((i - 1.5) * floor.Size.X / 2, 10.5, ((j - 0.5) / rows - 0.5) * floor.Size.Z)
					local light = Instance.new("PointLight")
					light.Color, light.Brightness, light.Range, light.Shadows = rgb(255, 240, 220), 0.3, 20, false
					light.Parent = lamp
					lamp.Parent = folder
					nLamps += 1
				end
			end
		end
	end
end

return ("style on: %d parts restyled, %d furniture parts, %d parts added to buildings, %d plot parts in Autumn Terracotta, %d shop lamps"):format(#scope(), #furnished, nAdd, nPalette, nLamps)

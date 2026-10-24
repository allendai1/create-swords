-- build_atmosphere.luau: lighting, nature, a mountain backdrop and light street dressing for the live map (2026-10-22).
-- Allen: "Give the level more polish and atmosphere while preserving the chosen simplified map." He picked lighting &
-- sky, nature (trees, bamboo, shrubs, rocks round the walls and lanes; mountains outside the walls) and street dressing
-- (a few stalls, crates, barrels and planters at the street's edges). No ambient life (smoke, particles, birds, sounds).
-- Run in Studio (Edit) through MCP execute_luau: loadstring(game.ServerStorage.Builders.build_atmosphere.Source)().
-- Rerunnable: sets Lighting, clears and rebuilds Workspace.Village.Atmosphere (block mountains included) and clears the
-- Terrain (the builder owns all terrain and makes none). It also lights the village's own lanterns (Andon, Chochin,
-- the plaza's stone lanterns); the plot template's lanterns are left alone. Same SEED = same result. Rerun it after
-- build_simple.
-- Frames and lots are build_simple's (x along the street, west −; "depth" from the street centre; the south side is
-- the north plan turned 180°). Kept clear: the lots (48.5 × 96) and their delivery bays with the way in from the street,
-- the street (depth < 28; dressing only at the edges), the gate, the shrine plaza and the lane running through the
-- back wall. Old pre-plot props near the world origin are left untouched (the backdrop skips the west).

local SEED = 31
local SS = game:GetService("ServerStorage")
local Lighting = game:GetService("Lighting")
local M = Enum.Material
local rad = math.rad
local rng = Random.new(SEED)
local function r(a, b) return a + (b - a) * rng:NextNumber() end
local function pick(t) return t[rng:NextInteger(1, #t)] end

local village = workspace:FindFirstChild("Village")
assert(village, "Workspace.Village missing: run build_simple first")
local ORIGIN = village.WorldPivot -- (640, 0, −200): the street's centre
local NF, SF = ORIGIN, ORIGIN * CFrame.Angles(0, math.pi, 0)
local STREET = CFrame.Angles(0, math.pi, 0) -- facing the street in a frame
local HALF, LOT_W, LOT_D = 36, 48.5, 96
local LOTS = { { -96.5, HALF }, { 0, HALF }, { 96.5, HALF } } -- lot centre x and front depth (one line since 2026-10-23)
local LANE = { -72.25, -24.25 } -- the lane that runs on through the back wall

local C = {
	timber = Color3.fromRGB(92, 63, 42),
	cedar = Color3.fromRGB(134, 94, 60),
	stone = Color3.fromRGB(122, 118, 110),
	moss = Color3.fromRGB(104, 112, 90),
	soil = Color3.fromRGB(86, 64, 46),
	indigo = Color3.fromRGB(38, 54, 96),
	norenW = Color3.fromRGB(222, 216, 198),
	red = Color3.fromRGB(190, 52, 40),
	black = Color3.fromRGB(24, 22, 22),
	straw = Color3.fromRGB(200, 174, 112),
	lamp = Color3.fromRGB(255, 196, 128),
}
local LEAF = { Color3.fromRGB(78, 120, 58), Color3.fromRGB(96, 136, 62), Color3.fromRGB(64, 104, 56), Color3.fromRGB(110, 140, 70) }
local ROCK = { Color3.fromRGB(122, 118, 110), Color3.fromRGB(140, 134, 124), Color3.fromRGB(104, 102, 98) }
local GOODS = { Color3.fromRGB(214, 196, 150), C.red, Color3.fromRGB(232, 226, 212), Color3.fromRGB(120, 92, 60), Color3.fromRGB(70, 90, 120) }

-- ---------------------------------------------------------------- lighting
-- Warm late afternoon with cool sky-lit shadows; interiors kept readable by a raised indoor Ambient. LightingStyle
-- (Soft) and PrioritizeLightingQuality are left as they are (the place migrated from ShadowMap).
local LIGHT = {
	ClockTime = 16.9, GeographicLatitude = 28, Brightness = 2.4, ExposureCompensation = 0.05,
	Ambient = Color3.fromRGB(116, 102, 92), OutdoorAmbient = Color3.fromRGB(128, 128, 144),
	ColorShift_Top = Color3.fromRGB(255, 214, 168), ColorShift_Bottom = Color3.fromRGB(0, 0, 0),
	EnvironmentDiffuseScale = 1, EnvironmentSpecularScale = 0.6, GlobalShadows = true, ShadowSoftness = 0.25,
}
for k, v in LIGHT do Lighting[k] = v end
local function effect(class, name, props)
	local e = Lighting:FindFirstChild(name) or Instance.new(class)
	e.Name = name
	for k, v in props do e[k] = v end
	e.Parent = Lighting
end
effect("Atmosphere", "Atmosphere", {
	Density = 0.3, Offset = 0.1, Color = Color3.fromRGB(232, 206, 178), Decay = Color3.fromRGB(150, 150, 172),
	Glare = 0.3, Haze = 1.3,
})
effect("Sky", "Sky", { SunAngularSize = 12, MoonAngularSize = 9, CelestialBodiesShown = true })
effect("BloomEffect", "Bloom", { Intensity = 0.7, Size = 28, Threshold = 1.5 })
effect("SunRaysEffect", "SunRays", { Intensity = 0.04, Spread = 0.2 })
effect("ColorCorrectionEffect", "ColorCorrection", {
	Brightness = 0, Contrast = 0.06, Saturation = 0.06, TintColor = Color3.fromRGB(255, 242, 228),
})

-- ---------------------------------------------------------------- helpers
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
	if o.noShadow or size.X * size.Y * size.Z < 30 then p.CastShadow = false end
	p.Parent = parent
	return p
end
local UP = CFrame.Angles(0, 0, math.pi / 2)
local function cyl(parent, name, h, d, cf, col, mat, o)
	o = o or {}
	o.shape = Enum.PartType.Cylinder
	return part(parent, name, Vector3.new(h, d, d), cf * UP, col, mat, o)
end
local function glow(p, range, bright)
	local l = p:FindFirstChildOfClass("PointLight") or Instance.new("PointLight")
	l.Color = Color3.fromRGB(255, 176, 104)
	l.Range = range
	l.Brightness = bright
	l.Shadows = false
	l.Parent = p
end
local function chochin(parent, cf)
	glow(cyl(parent, "Chochin", 1.9, 1.5, cf, C.red), 12, 1.4)
	cyl(parent, "ChochinCap", 0.22, 1.0, cf * CFrame.new(0, 1.03, 0), C.black)
	cyl(parent, "ChochinCap", 0.22, 1.0, cf * CFrame.new(0, -1.03, 0), C.black)
end
-- a clone of a mesh model, ground under its lowest point; foliage never collides, trunks do inside the walls
local function placeModel(src, cf, scale, parent, groundY, solidTrunk)
	local mdl = src:Clone()
	if scale ~= 1 then mdl:ScaleTo(scale) end
	mdl:PivotTo(cf)
	local bcf, bs = mdl:GetBoundingBox()
	mdl:TranslateBy(Vector3.new(0, groundY - (bcf.Y - bs.Y / 2), 0))
	for _, d in mdl:GetDescendants() do
		if d:IsA("BasePart") then
			d.Anchored = true
			local trunk = solidTrunk and (d.Name:find("bark") or d.Name:find("bamboo")) ~= nil
			d.CanCollide, d.CanQuery, d.CanTouch = trunk, trunk, false
		end
	end
	mdl.Parent = parent
	return mdl
end

local V3 = SS.Village3D
local B3 = SS.Buildings3D
local TREE = { pine = { V3.Pine1, V3.Pine2 }, maple = { V3.Maple1 }, sakura = { V3.Sakura1, V3.Sakura2 }, bamboo = { B3.Bamboo1, B3.Bamboo2, B3.Bamboo3 } }
local SCALE = { pine = { 1.6, 2.2 }, maple = { 1.3, 1.6 }, sakura = { 1.2, 1.5 }, bamboo = { 1.0, 1.3 } }

-- keep-out rectangles in frame terms {x0, x1, d0, d1}: lots (with the customers' walk in front), delivery bays with the
-- way in from the street, the through-lane's middle, the small house by it, the end houses, the street
local KEEP = { { LANE[1] + 12, LANE[2] - 12, 26, 260 }, { -96, -66, 170, 214 }, { -194, -168, 26, 58 }, { 168, 194, 26, 58 }, { -999, 999, -28, 28 } }
for _, lot in LOTS do
	table.insert(KEEP, { lot[1] - 24.75, lot[1] + 24.75, lot[2] - 14, lot[2] + LOT_D + 1.5 })
	table.insert(KEEP, { lot[1] - 43, lot[1] - 23, 26, lot[2] + 37 })
end
-- and in world offsets from ORIGIN {x0, x1, z0, z1}: the gate road and the shrine plaza
local KEEPW = { { -240, -194, -34, 34 }, { 194, 252, -46, 46 } }
local function clear(F, x, d, reach)
	for _, k in KEEP do
		if x + reach > k[1] and x - reach < k[2] and d + reach > k[3] and d - reach < k[4] then return false end
	end
	local o = ORIGIN:PointToObjectSpace((F * CFrame.new(x, 0, -d)).Position)
	for _, k in KEEPW do
		if o.X + reach > k[1] and o.X - reach < k[2] and o.Z + reach > k[3] and o.Z - reach < k[4] then return false end
	end
	return true
end

-- ---------------------------------------------------------------- rebuild the folder
local old = village:FindFirstChild("Atmosphere")
if old then old:Destroy() end
local root = Instance.new("Folder")
root.Name = "Atmosphere"
root.Parent = village
local function folder(name, parent)
	local f = Instance.new(parent == workspace and "Model" or "Folder")
	f.Name = name
	f.Parent = parent or root
	return f
end
local Nature, Dressing, Backdrop = folder("Nature"), folder("Dressing"), folder("Backdrop")
local skipped = {}

local function tree(F, kind, x, d, groundY)
	local src = pick(TREE[kind])
	local sc = r(SCALE[kind][1], SCALE[kind][2])
	local _, size = src:GetBoundingBox()
	local reach = math.sqrt(size.X ^ 2 + size.Z ^ 2) / 2 * sc * (kind == "bamboo" and 0.6 or 0.8)
	if not clear(F, x, d, reach) then
		table.insert(skipped, ("%s %.0f,%.0f"):format(kind, x, d))
		return
	end
	local g = groundY or 0.02
	if kind == "bamboo" then -- a clump: a second, smaller stand beside the first
		placeModel(pick(TREE.bamboo), F * CFrame.new(x, 0, -d + r(-3, 3)) * CFrame.Angles(0, r(0, 6.28), 0), sc * 0.8, Nature, g, g > 0)
	end
	return placeModel(src, F * CFrame.new(x, 0, -d) * CFrame.Angles(0, r(0, 2 * math.pi), 0), sc, Nature, g, g > 0)
end
-- a low clump of squashed spheres; never collides or casts shadows
local function shrub(F, x, d, s, groundY)
	if not clear(F, x, d, s * 0.6) then
		table.insert(skipped, ("shrub %.0f,%.0f"):format(x, d))
		return
	end
	local m = Instance.new("Model")
	m.Name = "Shrub"
	local base = F * CFrame.new(x, groundY or 0.12, -d)
	for i = 1, 3 do
		local w = s * r(0.7, 1.1) * (i == 1 and 1.2 or 0.9)
		local off = i == 1 and Vector3.zero or Vector3.new(r(-0.5, 0.5) * s, 0, r(-0.5, 0.5) * s)
		part(m, "Leaves", Vector3.new(w, w * r(0.55, 0.75), w), base * CFrame.new(off + Vector3.new(0, w * 0.22, 0)), pick(LEAF), M.SmoothPlastic, { shape = Enum.PartType.Ball, noShadow = true })
	end
	m.Parent = Nature
end
-- a rock: a tilted block and a smaller one leaning on it, sunk into the ground
local function rock(F, x, d, s, groundY)
	if not clear(F, x, d, s * 0.6) then return end
	local m = Instance.new("Model")
	m.Name = "Rock"
	local base = F * CFrame.new(x, groundY or 0.12, -d) * CFrame.Angles(0, r(0, 2 * math.pi), 0)
	part(m, "Stone", Vector3.new(s, s * r(0.5, 0.7), s * r(0.7, 0.9)), base * CFrame.new(0, s * 0.15, 0) * CFrame.Angles(r(-0.25, 0.25), 0, r(-0.3, 0.3)), pick(ROCK), M.Slate, { solid = true })
	part(m, "Stone", Vector3.new(s * 0.55, s * 0.4, s * 0.5), base * CFrame.new(s * 0.55, s * 0.08, s * 0.2) * CFrame.Angles(r(-0.4, 0.4), r(0, 3), r(-0.4, 0.4)), C.moss, M.Slate, { solid = true })
	m.Parent = Nature
end

-- ---------------------------------------------------------------- nature inside the walls (both sides alike)
-- Trees behind the lots and in the corners, bamboo against the lanes' workshop walls (back halves, away from the bays),
-- a forest corner by the gate and a grove framing the shrine. Lane paving top 0.12.
local PLAN = {
	-- behind the lots, in front of the back wall (lot backs at depth 132.8 / 140.8, wall at 172)
	{ "pine", -116, 153 }, { "maple", -94, 150 }, { "bamboo", -6, 165 }, { "pine", 14, 158 }, { "sakura", 84, 154 },
	{ "pine", 110, 158 },
	-- west corner (gate side in the north frame): lot 1's bay is at x −137…−121, so trees keep west and back
	{ "pine", -186, 76 }, { "maple", -162, 96 }, { "pine", -184, 118 }, { "pine", -152, 140 }, { "bamboo", -190, 158 },
	{ "sakura", -136, 112 },
	-- east corner
	{ "pine", 146, 88 }, { "maple", 172, 76 }, { "pine", 186, 118 }, { "sakura", 150, 130 }, { "bamboo", 190, 160 },
	{ "pine", 166, 160 },
	-- lanes: bamboo by the workshop walls' back halves (7 out, so no leaf reaches through a wall)
	{ "bamboo", -65, 104 }, { "bamboo", -65, 124 }, { "bamboo", -31.5, 112 }, { "bamboo", 31.5, 96 }, { "bamboo", 31.5, 122 },
	{ "bamboo", 65, 104 },
}
-- round the shrine, east of the street's end (x > 200 in world terms, so placed north and south in the north frame)
local SHRINE = { { "pine", 214, 66 }, { "pine", 236, 84 }, { "maple", 218, 112 }, { "pine", 238, 140 }, { "pine", 212, 160 } }
local SHRUBS = {
	{ -68, 92, 3.5 }, { -68, 134, 3 }, { -28, 98, 3 }, { -28, 128, 3.5 }, { 28, 84, 3 }, { 28, 134, 3.5 }, { 68, 92, 3 },
	{ 68, 130, 3.5 }, { -120, 160, 4 }, { 40, 162, 4 }, { 120, 164, 3.5 }, { -170, 70, 4 },
	{ -194, 96, 3.5 }, { -142, 156, 4 }, { 140, 70, 4 }, { 190, 96, 3.5 },
}
local ROCKS = {
	{ -102, 166, 3 }, { -56, 168, 2.4 }, { 30, 166, 2.6 }, { 126, 166, 3 }, { -192, 136, 3.2 }, { -174, 84, 2.2 },
	{ 192, 70, 2.8 }, { -70, 114, 2.2 }, { 70, 116, 2.4 }, { -32, 148, 2 },
}
for _, F in { NF, SF } do
	for _, t in PLAN do tree(F, t[1], t[2], t[3]) end
	for _, s in SHRUBS do shrub(F, s[1], s[2], s[3]) end
	for _, k in ROCKS do rock(F, k[1], k[2], k[3]) end
	task.wait()
end
for _, s in { -1, 1 } do
	for _, t in SHRINE do tree(NF, t[1], t[2], s * t[3]) end
	for _, k in { { 206, 52, 3.5 }, { 244, 56, 3 }, { 228, 162, 4 } } do shrub(NF, k[1], s * k[2], k[3]) end
	for _, k in { { 244, 100, 3.2 }, { 210, 150, 2.4 } } do rock(NF, k[1], s * k[2], k[3]) end
end

-- outside the back walls, inside the map's bounds (depth 173…210, baseplate at 0): a row of trees the lane exit looks
-- out on, and two either side of the gate road
for _, F in { NF, SF } do
	for _, x in { -240, -212, -186, -158, -130, -4, 26, 58, 88, 120, 152, 184, 214, 244 } do
		tree(F, rng:NextNumber() < 0.75 and "pine" or "maple", x + r(-5, 5), r(186, 202), -0.05)
	end
	for _, x in { -110, 4, 70, 136, 200 } do shrub(F, x + r(-6, 6), r(178, 182), r(3, 4.5), 0) end
end
for _, s in { -1, 1 } do
	tree(NF, "pine", -218, s * 52, -0.05)
	tree(NF, "pine", -210, s * 76, -0.05)
	shrub(NF, -206, s * 40, 3.5, 0)
end

-- ---------------------------------------------------------------- street dressing
-- One stall per street corner (between the end houses and the end lots, clear of lot 1's bay), a crate-and-barrel stack
-- beside it, and a planted stone box at each lane mouth. All at depth ≥ 30, off the walking street.
local function stall(cf)
	local m = Instance.new("Model")
	m.Name = "Stall"
	local function L(x, y, z) return cf * CFrame.new(x, y, z) end
	part(m, "Counter", Vector3.new(7, 2.4, 2.6), L(0, 1.4, 0), C.cedar, M.WoodPlanks, { solid = true })
	for _, px in { -3.3, 3.3 } do -- posts reach just into the canopy, which slopes down 12° to the front
		part(m, "Post", Vector3.new(0.35, 6.74, 0.35), L(px, 3.57, -1.6), C.timber, M.Wood)
		part(m, "Post", Vector3.new(0.35, 7.4, 0.35), L(px, 3.9, 1.6), C.timber, M.Wood)
	end
	part(m, "Canopy", Vector3.new(8.4, 0.15, 5.2), L(0, 7.3, 0) * CFrame.Angles(-rad(12), 0, 0), C.norenW, M.Fabric)
	part(m, "Valance", Vector3.new(8.2, 0.8, 0.08), L(0, 6.3, -2.5), C.indigo, M.Fabric)
	chochin(m, L(3.0, 5.6, -2.2))
	local gx = -3.1
	while gx < 2.4 do
		local s = r(0.8, 1.3)
		if rng:NextNumber() < 0.5 then
			cyl(m, "Barrel", s * 1.1, s, L(gx + s / 2, 2.6 + s * 0.55, r(-0.4, 0.4)), pick(GOODS))
		else
			part(m, "Goods", Vector3.new(s, s * 0.7, s), L(gx + s / 2, 2.6 + s * 0.35, r(-0.4, 0.4)) * CFrame.Angles(0, r(-0.3, 0.3), 0), pick(GOODS), M.Fabric)
		end
		gx += s + 0.35
	end
	m.WorldPivot = cf
	m.Parent = Dressing
end
local function stack(cf)
	local m = Instance.new("Model")
	m.Name = "Stack"
	local function L(x, y, z) return cf * CFrame.new(x, y, z) end
	part(m, "Crate", Vector3.new(2.6, 2.4, 2.6), L(0, 1.25, 0) * CFrame.Angles(0, r(-0.2, 0.2), 0), C.cedar, M.WoodPlanks, { solid = true })
	part(m, "Crate", Vector3.new(2.0, 1.9, 2.0), L(0.2, 3.35, 0.1) * CFrame.Angles(0, r(0.3, 0.6), 0), C.timber, M.WoodPlanks, { solid = true })
	part(m, "Crate", Vector3.new(2.2, 2.1, 2.2), L(-2.9, 1.1, 0.5) * CFrame.Angles(0, r(0.2, 0.5), 0), C.cedar, M.WoodPlanks, { solid = true })
	for i, p in { Vector3.new(2.9, 0, -0.4), Vector3.new(3.4, 0, 2.2) } do -- sake barrels: straw wrap, rope bands
		local h = i == 1 and 3.0 or 2.6
		local b = cyl(m, "Barrel", h, 2.3, L(p.X, 0.05 + h / 2, p.Z), C.straw, M.Fabric, { solid = true })
		cyl(m, "Band", 0.22, 2.42, b.CFrame * UP:Inverse() * CFrame.new(0, h * 0.3, 0), C.indigo, M.Fabric)
		cyl(m, "Band", 0.22, 2.42, b.CFrame * UP:Inverse() * CFrame.new(0, -h * 0.3, 0), C.indigo, M.Fabric)
		cyl(m, "Lid", 0.12, 2.0, b.CFrame * UP:Inverse() * CFrame.new(0, h / 2 + 0.04, 0), C.cedar, M.Wood)
	end
	m.WorldPivot = cf
	m.Parent = Dressing
end
local function planter(cf)
	local m = Instance.new("Model")
	m.Name = "Planter"
	part(m, "Box", Vector3.new(3.6, 1.5, 3.6), cf * CFrame.new(0, 0.8, 0), C.stone, M.Cobblestone, { solid = true })
	part(m, "Soil", Vector3.new(3.0, 0.2, 3.0), cf * CFrame.new(0, 1.58, 0), C.soil, M.Ground) -- 0.13 proud of the rim
	m.Parent = Dressing
	local pine = placeModel(pick(TREE.pine), cf * CFrame.Angles(0, r(0, 6.28), 0), r(0.42, 0.5), m, 1.64, false)
	for _, d in pine:GetDescendants() do if d:IsA("BasePart") then d.CastShadow = false end end
end
for _, F in { NF, SF } do
	-- bottoms 0.1 (stall) and 0.05 (the rest): just under the lane paving's top (0.12)
	stall(F * CFrame.new(-158, -0.1, -33) * STREET)
	stack(F * CFrame.new(-148, 0, -40) * CFrame.Angles(0, r(-0.3, 0.3), 0))
	stall(F * CFrame.new(146, -0.1, -33) * STREET)
	stack(F * CFrame.new(136, 0, -40) * CFrame.Angles(0, math.pi + r(-0.3, 0.3), 0))
	-- lane mouths: only on the side without a delivery bay (each bay's lintel faces the street)
	for _, x in { LANE[1] + 3, -LANE[2] + 3 } do planter(F * CFrame.new(x, 0, -32)) end
	task.wait()
end

-- ---------------------------------------------------------------- lanterns that glow
-- The village's own lamps: the standing andon get warm neon paper and a stronger light, the hanging chochin a stronger
-- light, the plaza's stone lanterns neon paper and a light.
local nLamps = 0
for _, d in village:GetDescendants() do
	if d:IsA("BasePart") and not d:IsDescendantOf(root) then
		if d.Name == "Andon" then
			d.Material, d.Color = M.Neon, C.lamp
			glow(d, 18, 1.5)
			nLamps += 1
		elseif d.Name == "Chochin" then -- red paper stays paper (neon red reads as flat plastic); a stronger light
			glow(d, 13, 1.4)
			nLamps += 1
		elseif d.Name == "StoneLantern_paper" then
			d.Material, d.Color = M.Neon, C.lamp
			glow(d, 10, 1.2)
			nLamps += 1
		end
	end
end

-- ---------------------------------------------------------------- mountain backdrop (blocks) and its forest
-- Allen 2026-10-22: "instead of the current mountain set up, could we try to just do rectangular blocks as mountains".
-- The terrain hills' and peaks' ring, now stepped blocks: low forested hills just past the map's bounds closing the
-- valley, higher peaks behind them, each a stack of boxes narrowing upward, every tier turned and shifted a little and
-- kept inside the top below (no overhanging ledge), the summit drifting one way (a steep side and a long one). Hills:
-- grass tiers. Peaks: two grass tiers, rock above, a pale cap on the tallest, and a lower shoulder beside each. The
-- west, where the road comes in, stays open. Anchored, never collide (the map's bounds keep players in); only the near
-- hills cast shadows. No terrain any more.
workspace.Terrain:Clear() -- ponytail: the builder owns all terrain (none now); clear by region if terrain is ever added inside the walls
local Mountains = folder("Mountains", Backdrop)
local CEN = ORIGIN.Position + Vector3.new(14, 0, 0) -- middle of the bounds (x 410…898, z −410…10)
local BX, BZ = 244, 210 -- half extents of the bounds
local function ring(th, ax, bz) -- a squarish ellipse round the bounds
	local c, s = math.cos(th), math.sin(th)
	return Vector3.new(ax * math.sign(c) * math.abs(c) ^ 0.5, 0, bz * math.sign(s) * math.abs(s) ^ 0.5)
end
-- darker than the village's own, as the haze pales them
local HILL = { Color3.fromRGB(74, 110, 54), Color3.fromRGB(84, 118, 58), Color3.fromRGB(66, 100, 52) }
local CRAG = { Color3.fromRGB(84, 82, 80), Color3.fromRGB(76, 74, 74), Color3.fromRGB(92, 88, 84) }
local CAP = Color3.fromRGB(218, 224, 232)
-- tiers { height, "grass" | "rock" } from 4 below ground up; base w × d, each tier w·shrink × d·shrink, sunk 0.5 into the
-- one below; cap: a pale slab on the top tier, 0.4 past its sides. CanQuery on, so the forest's rays stop on the blocks
-- (trees go on grass tiers only).
local function mountain(pos, yaw, w, d, tiers, shrink, far, cap)
	if pos.X - math.max(w, d) / 2 < 80 then return end -- clear of the old props near the world origin
	local cf = CFrame.new(pos.X, -4, pos.Z) * CFrame.Angles(0, yaw, 0) -- the tier's bottom centre
	local lx, lz = rng:NextNumber() < 0.5 and -1 or 1, r(-1, 1) -- which way the summit drifts
	for i, t in tiers do
		local h, grass = t[1], t[2] == "grass"
		part(Mountains, grass and "Grass" or "Rock", Vector3.new(w, h, d), cf * CFrame.new(0, h / 2, 0), pick(grass and HILL or CRAG), grass and M.Grass or M.Slate, { noShadow = far }).CanQuery = true
		if i == #tiers then
			if cap then part(Mountains, "Cap", Vector3.new(w + 0.8, 4, d + 0.8), cf * CFrame.new(0, h + 1.5, 0), CAP, M.Snow, { noShadow = far }).CanQuery = true end
			break
		end
		local nw, nd, turn = w * shrink * r(0.94, 1.04), d * shrink * r(0.94, 1.04), r(-0.12, 0.12)
		local c, s = math.abs(math.cos(turn)), math.abs(math.sin(turn))
		local ex, ez, m = (nw * c + nd * s) / 2, (nw * s + nd * c) / 2, 2 + 0.04 * math.min(w, d) -- next tier's half extents here, margin
		local f = math.min(1, (w / 2 - m) / ex, (d / 2 - m) / ez) -- shrink further if it would not fit
		nw, nd, ex, ez = nw * f, nd * f, ex * f, ez * f
		local sx, sz = math.max(w / 2 - ex - m, 0), math.max(d / 2 - ez - m, 0)
		cf = cf * CFrame.new(lx * sx * r(0.3, 1), h - 0.5, lz * sz * r(0.3, 1)) * CFrame.Angles(0, turn, 0)
		w, d = nw, nd
	end
end
local function along(th) return -th - math.pi / 2 + r(-0.2, 0.2) end -- long side roughly along the ring
for i = 0, 33 do
	local th = i / 34 * 2 * math.pi + r(-0.04, 0.04)
	if math.abs(math.cos(th)) < 0.97 or math.cos(th) > 0 then -- leave the road's way west open
		local R = r(80, 125)
		local p = CEN + ring(th, BX + 34 + 0.94 * R, BZ + 34 + 0.94 * R)
		mountain(p, along(th), R * r(1.7, 2.1), R * r(1.3, 1.6), {
			{ 4 + R * r(0.2, 0.26), "grass" }, { R * r(0.16, 0.22), "grass" }, { R * r(0.12, 0.18), "grass" },
		}, r(0.62, 0.74), false)
	end
	if i % 6 == 0 then task.wait() end
end
local function peak(p, yaw, R, H, n)
	local tiers = {}
	for k = 1, n do
		tiers[k] = { H / n * r(0.85, 1.15), k <= 2 and "grass" or "rock" }
	end
	mountain(p, yaw, R * r(1.2, 1.5), R * r(0.9, 1.2), tiers, r(0.64, 0.74), true, H > 230)
end
for i = 0, 15 do
	local th = i / 16 * 2 * math.pi + r(-0.08, 0.08)
	if math.cos(th) > -0.6 then -- no far peaks in the west (the road's valley, and the old props near the origin)
		local R, H, yaw = r(200, 280), r(170, 260), along(th)
		local p = CEN + ring(th, BX + 200 + 0.7 * R, BZ + 200 + 0.7 * R)
		peak(p, yaw, R, H, rng:NextInteger(4, 6))
		local side = Vector3.new(math.cos(yaw), 0, -math.sin(yaw)) * R * r(0.5, 0.8) * (rng:NextNumber() < 0.5 and -1 or 1)
		peak(p + side, yaw + r(-0.3, 0.3), R * 0.6, H * r(0.5, 0.65), rng:NextInteger(3, 4)) -- the shoulder, along the ring
	end
	task.wait()
end

-- pines on the grass tiers and in the grass between the bounds and the hills, where a tree has room: eight probes round
-- most of its crown land on the same tier at the same height, so no branch pokes into a block
local Forest = folder("Forest", Backdrop)
local ray = RaycastParams.new()
ray.FilterType = Enum.RaycastFilterType.Include
ray.FilterDescendantsInstances = { Mountains, workspace:FindFirstChild("Baseplate") }
local function down(x, z) return workspace:Raycast(Vector3.new(x, 400, z), Vector3.new(0, -500, 0), ray) end
local nForest = 0
for i = 1, 1400 do
	if nForest >= 220 then break end
	local th = r(0, 2 * math.pi)
	local w = CEN + ring(th, BX + r(14, 240), BZ + r(14, 240))
	local src, sc = rng:NextNumber() < 0.95 and pick(TREE.pine) or V3.Maple1, r(2.2, 3.4)
	local _, size = src:GetBoundingBox()
	local reach = math.max(size.X, size.Z) * sc * 0.4
	local o = ORIGIN:PointToObjectSpace(w)
	local hit = not (o.X < -230 and math.abs(o.Z) < 40) and down(w.X, w.Z) -- not on the road west
	local ok = hit and hit.Position.Y < 120 and (hit.Instance.Name == "Grass" or hit.Instance.Name == "Baseplate")
	for k = 0, 7 do
		if not ok then break end
		local h2 = down(w.X + math.cos(k * math.pi / 4) * reach, w.Z + math.sin(k * math.pi / 4) * reach)
		ok = h2 and h2.Instance == hit.Instance and math.abs(h2.Position.Y - hit.Position.Y) < 0.05
	end
	if ok then
		placeModel(src, CFrame.new(hit.Position) * CFrame.Angles(0, r(0, 6.28), 0), sc, Forest, hit.Position.Y - 0.6, false)
		nForest += 1
	end
	if i % 40 == 0 then task.wait() end
end

local n, nBlocks = 0, #Mountains:GetChildren()
for _, d in root:GetDescendants() do if d:IsA("BasePart") then n += 1 end end
return ("Atmosphere built: %d parts (%d mountain blocks), %d forest trees, %d lanterns lit, %d skipped%s"):format(n, nBlocks, nForest, nLamps, #skipped, #skipped > 0 and (": " .. table.concat(skipped, "; ")) or "")

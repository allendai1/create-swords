--!strict
-- Street dressing (2026-11-04, Allen: "do a map passthrough, feels like it's missing some extra decorations that make the
-- game feel bland"). No trees or rocks (Allen rejected generated nature). New props are low-poly Blender models
-- (Allen, 2026-11-04: "if you're going to create models, create them in Blender with a low poly style"), cloned from
-- ServerStorage.Buildings3D; the lantern strings stay part-built ("can keep the latnern strings"):
--   * festival lantern strings across the road at the gaps between plots and at the street's two ends (parts)
--   * nobori banners at both ends of each grass gap's mouth (Buildings3D.Nobori, cloth recoloured per copy) and a stretch
--     of the town wall across each mouth on the plots' front line (copies of Village.Walls' pieces; they collide)
--   * the shrine plaza: food stalls, stone lanterns, a well and a notice board (see "Plaza pieces")
--   * sakura trees in planters down the road's middle (Buildings3D.SakuraTree, 2026-11-05)
-- Everything sits on the ground under it (a ray), anchored; decor doesn't collide, CanQuery off, small parts cast no
-- shadow. Rerun-safe: it replaces workspace.Village.Dressing. Run in Edit:
--   loadstring(game.ServerStorage.Builders.build_street_dressing.Source)()
-- Street frame (measured 2026-11-04): the road runs along x 410..840, z -228..-172 (centre z -200); the plots' lots stand
-- at x 543.5 / 640 / 736.5 (85 wide), north and south, so the gaps between them are at x 591.75 and 688.25; the gate end
-- houses are at x 459, the shrine end ones at x 821; the plaza is x 840..892.

local village = workspace:WaitForChild("Village")
local old = village:FindFirstChild("Dressing")
if old then
	old:Destroy()
end
local root = Instance.new("Folder")
root.Name = "Dressing"
root.Parent = village

local rgb = Color3.fromRGB
local DARK = { Enum.Material.Wood, "PaintWoodDark", rgb(70, 46, 32) }
local ROOF = { Enum.Material.ClayRoofTiles, "PaintRoof", rgb(176, 88, 54) }
local ROOF_TRIM = { Enum.Material.ClayRoofTiles, "PaintRoofTrim", rgb(176, 88, 54) } -- round trims: no tiles (2026-11-05)
local ROPE = { Enum.Material.SmoothPlastic, "", rgb(34, 30, 30) }
local RED = { Enum.Material.SmoothPlastic, "", rgb(198, 37, 23) }
local PAPER = { Enum.Material.SmoothPlastic, "", rgb(242, 232, 212) }
local INDIGO = { Enum.Material.Fabric, "", rgb(40, 52, 92) }
local CLOTH_RED = { Enum.Material.Fabric, "", rgb(170, 40, 36) }

local UP = CFrame.Angles(0, 0, math.rad(90)) -- a cylinder's axis (X) stood up

local rays = RaycastParams.new()
rays.FilterType = Enum.RaycastFilterType.Exclude
rays.FilterDescendantsInstances = { root }
-- The ground's top under (x, z): the street, the lots, the plaza.
local function ground(x: number, z: number): number
	local hit = workspace:Raycast(Vector3.new(x, 60, z), Vector3.new(0, -120, 0), rays)
	return if hit then hit.Position.Y else 0
end

local function part(parent: Instance, name: string, look: { any }, size: Vector3, cf: CFrame, shape: Enum.PartType?): Part
	local p = Instance.new("Part")
	p.Name = name
	p.Anchored = true
	p.CanCollide, p.CanTouch, p.CanQuery = false, false, false
	p.Material, p.MaterialVariant, p.Color = look[1], look[2], look[3]
	p.TopSurface, p.BottomSurface = Enum.SurfaceType.Smooth, Enum.SurfaceType.Smooth
	if shape then
		p.Shape = shape
	end
	p.Size = size
	p.CFrame = cf
	p.CastShadow = size.Magnitude > 3
	p.Parent = parent
	return p
end
local function model(parent: Instance, name: string): Model
	local m = Instance.new("Model")
	m.Name = name
	m.Parent = parent
	return m
end
-- A cylinder from a to b (its axis along the line).
local function rod(parent: Instance, name: string, look: { any }, a: Vector3, b: Vector3, thick: number): Part
	local mid = (a + b) / 2
	return part(parent, name, look, Vector3.new((b - a).Magnitude, thick, thick), CFrame.lookAt(mid, b) * CFrame.Angles(0, math.rad(90), 0), Enum.PartType.Cylinder)
end

-- Lantern strings across the road -----------------------------------------------------------------------------------
local ROAD_N, ROAD_S = -234, -166 -- the poles stand 6 studs outside the road on each side
local POLE_H, SAG = 15, 1.6
-- A sagging rope from a to b with n lanterns alternating red and paper white. The lanterns are the Blender
-- Buildings3D.StreetLantern (2026-11-05, Allen: "uses real lanterns from toolbox for the street string lights or make a
-- better looking one in blender"; Models/Props/Notes1105): its pivot is the top of its cord, hung on the rope; its Paper
-- part takes the colour. The rope stays parts.
local LANTERN = game:GetService("ServerStorage"):WaitForChild("Buildings3D"):WaitForChild("StreetLantern") :: Model
local function hangLanterns(m: Model, a: Vector3, b: Vector3, n: number)
	local mid = (a + b) / 2 - Vector3.new(0, SAG, 0)
	rod(m, "Rope", ROPE, a, mid, 0.08)
	rod(m, "Rope", ROPE, mid, b, 0.08)
	local yaw = math.atan2(-(b - a).X, -(b - a).Z) -- every lantern turned along its rope
	for i = 1, n do
		local t = i / (n + 1)
		local onRope = if t < 0.5 then a:Lerp(mid, t * 2) else mid:Lerp(b, (t - 0.5) * 2)
		local look = if i % 2 == 1 then RED else PAPER
		local lantern = LANTERN:Clone()
		lantern.Name = "Lantern"
		;(lantern :: any).Paper.Color = look[3]
		lantern:PivotTo(CFrame.new(onRope) * CFrame.Angles(0, yaw, 0))
		lantern.Parent = m
	end
end
-- A dark pole with a tiled cap; returns the rope's tie point just under the cap.
local function pole(m: Model, x: number, z: number, h: number): Vector3
	local g = ground(x, z)
	part(m, "Pole", DARK, Vector3.new(h, 0.5, 0.5), CFrame.new(x, g + h / 2 - 0.1, z) * UP, Enum.PartType.Cylinder)
	part(m, "Cap", ROOF_TRIM, Vector3.new(0.8, 0.8, 0.8), CFrame.new(x, g + h, z), Enum.PartType.Ball)
	return Vector3.new(x, g + h - 0.6, z)
end
local function lanternString(x: number)
	local m = model(root, "LanternString")
	hangLanterns(m, pole(m, x, ROAD_N, POLE_H), pole(m, x, ROAD_S, POLE_H), 9)
end

-- Plaza pieces (second pass, 2026-11-04, Allen: "Yes, fill it more"). Nothing walks the plaza (a dead end at the closed
-- gate), so the big solid pieces collide.
local SS = game:GetService("ServerStorage")
-- A clone of a ServerStorage model, its bounding box's bottom centre on the ground at (x, z).
local function placeClone(src: Model, x: number, z: number, yaw: number, scale: number): Model
	local m = src:Clone()
	m:PivotTo(CFrame.new(m:GetPivot().Position) * CFrame.Angles(0, math.rad(yaw), 0))
	m:ScaleTo(m:GetScale() * scale)
	local cf, sz = m:GetBoundingBox()
	m:PivotTo(m:GetPivot() + Vector3.new(x - cf.X, ground(x, z) - (cf.Y - sz.Y / 2), z - cf.Z))
	m.Parent = root
	return m
end

-- A clone of a ServerStorage model whose pivot is its foot (the Blender props), on the ground at (x, z), turned by yaw.
local function placeAt(src: Model, x: number, z: number, yaw: number): Model
	local m = src:Clone()
	m:PivotTo(CFrame.new(x, ground(x, z), z) * CFrame.Angles(0, math.rad(yaw), 0))
	m.Parent = root
	return m
end
-- Nobori banner (Blender, Models/Props/Festival): its cloth hangs on the pole's +X side once turned (yaw 90) or -X (yaw -90),
-- facing the road.
local function nobori(x: number, z: number, yaw: number, cloth: { any })
	local m = placeAt(SS.Buildings3D.Nobori, x, z, yaw)
	m.Cloth.Color = cloth[3]
end
local function yatai(x: number, z: number, yaw: number) -- its counter faces -z before turning
	placeAt(SS.Buildings3D.Yatai, x, z, yaw)
end

-- Placement ---------------------------------------------------------------------------------------------------------------
local GAPS = { 591.75, 688.25 } -- between the plots
local ENDS = { 488, 795 } -- between the end houses and the first / last plots
for _, x in GAPS do
	lanternString(x)
end
for _, x in ENDS do
	lanternString(x)
end
-- Map pass 2 (2026-11-04, from a blind review against the references): a banner at both ends of each grass gap's mouth on
-- the street (between two plot pads, or a pad and an end house), so every plot front has a banner at each corner: indigo
-- between plots, red at the street's ends. Walls between plots (2026-11-04, Allen picked "Walls between plots" from the
-- review): each mouth is closed by a stretch of the town's own wall (copies of Village.Walls' plaster, stone base, tile
-- cap and ridge at the same sizes and heights) on the plots' front line (their corner posts stand at z -238.5 / -161.5),
-- with a pillar at each end beside the plot's corner post, so the street front runs unbroken from plot to plot.
-- Mouths measured from Village.Lots pads and the end houses (x from, x to, wall z, banner z, cloth); the west end
-- houses' side is x 471.1.
local MOUTHS = {
	{ 471.1, 499.5, -238.5, -233.6, CLOTH_RED }, { 583.5, 596, -238.5, -233.6, INDIGO }, { 680, 692.5, -238.5, -233.6, INDIGO }, { 776.5, 808.9, -238.5, -233.6, CLOTH_RED },
	{ 471.1, 503.5, -161.5, -166.4, CLOTH_RED }, { 587.5, 600, -161.5, -166.4, INDIGO }, { 684, 696.5, -161.5, -166.4, INDIGO }, { 780.5, 808.9, -161.5, -166.4, CLOTH_RED },
}
-- the town wall's pieces (Village.Walls became the forest, 2026-11-06; one of each kept in ServerStorage.WallPieces)
local TOWN_WALL = game:GetService("ServerStorage"):WaitForChild("WallPieces")
-- A copy of one of the town wall's pieces, unturned (long along X; the ridge is a cylinder whose axis is X).
local function wallPiece(m: Model, name: string, size: Vector3, pos: Vector3)
	-- lihfolk-ignore: findfirstchild-chain (a type cast, checked by the assert below)
	local src = TOWN_WALL:FindFirstChild(name) :: BasePart?
	assert(src, "ServerStorage.WallPieces has no " .. name)
	local p = src:Clone()
	p.Size = size
	p.CFrame = CFrame.new(pos)
	p.Parent = m
end
-- Since the plot fences became walls too (2026-11-05, build_plot_walls: a pillar at each plot corner), a gap wall runs
-- from pad edge to pad edge with no pillars of its own: its ends tuck into the plots' corner pillars (an unclaimed lot
-- has no plot, so the end shows plain there).
for _, mo in MOUTHS do
	local x0, x1, wz, bz, cloth = mo[1], mo[2], mo[3], mo[4], mo[5]
	local m = model(root, "GapWall")
	local g = ground((x0 + x1) / 2, wz)
	local L, mid = x1 - x0, (x0 + x1) / 2
	wallPiece(m, "WallBase", Vector3.new(L, 1.6, 1.6), Vector3.new(mid, g + 0.8, wz))
	wallPiece(m, "Wall", Vector3.new(L, 5, 1.1), Vector3.new(mid, g + 4.1, wz))
	wallPiece(m, "WallCap", Vector3.new(L, 0.5, 2.2), Vector3.new(mid, g + 6.8, wz))
	wallPiece(m, "WallRidge", Vector3.new(L, 1.2, 1.2), Vector3.new(mid, g + 7.2, wz))
	nobori(x0 + 1.3, bz, 90, cloth) -- cloth toward the mouth, facing the road
	nobori(x1 - 1.3, bz, -90, cloth)
end
-- The plaza (x 840..888, z -240..-160; the closed gate at x 888 between posts at z -216 / -184): a row of two stalls on
-- each side, stone lanterns flanking the gate, a well and a notice board.
-- The middle (z -215..-185) stays open to the gate.
for _, x in { 848, 862 } do
	yatai(x, -236, 180) -- the north side, facing into the plaza
	yatai(x, -164, 0)
end
for _, z in { -222, -178 } do
	placeClone(SS.Buildings3D.StoneLantern, 880, z, 0, 1.6)
end
placeClone(SS.Buildings3D.Well, 872, -235, 180, 1) -- the Blender well (Models/Props/Well), its bucket toward the plaza
local board = SS.Buildings3D.NoticeBoard:Clone()
board.Anchored = true
board.CFrame = CFrame.new(872, ground(872, -163) + board.Size.Y / 2, -163)
board.Parent = root

-- Map pass (2026-11-04, Allen: "keep doing a pass of the map until it looks like a nice japanese village street"; the
-- vault's references: Anime Village town-v1, Town Street Redesign 01): a bon-odori yagura as the plaza's centrepiece
-- (its ladder toward the street), lantern strings from its eaves to poles at the plaza's corners, a handcart at each end
-- of the street, and stone lanterns inside the west gate like the plaza's pair.
local YX, YZ, YS = 858, -200, 1 -- 11.6 tall: the gate's sign (y 14.3..17.1) stays in view over it from the street (1.2 hid it)
placeAt(SS.Buildings3D.Yagura, YX, YZ, 90):ScaleTo(YS)
local yg = ground(YX, YZ)
for _, c in { { 843, -238, -1, -1 }, { 843, -162, -1, 1 }, { 885, -238, 1, -1 }, { 885, -162, 1, 1 } } do
	local m = model(root, "LanternString")
	hangLanterns(m, pole(m, c[1], c[2], 14), Vector3.new(YX + c[3] * 4.3 * YS, yg + 8.8 * YS, YZ + c[4] * 4.3 * YS), 7)
end
placeAt(SS.Buildings3D.Handcart, 479, -165.5, 90) -- the west end, by the south end house, in front of the wall, shafts toward the gate
placeAt(SS.Buildings3D.Handcart, 836, -238, 180) -- the east end, by the north end house, shafts toward the road
for _, z in { -222, -178 } do
	placeClone(SS.Buildings3D.StoneLantern, 448, z, 0, 1.6)
end

-- Sakura in planters down the road's middle (2026-11-05, Allen: "middle of the street could use some trees. carve out
-- parts of the middle of the street to have a sakura tree"): the Blender Buildings3D.SakuraTree (its own stone kerb and
-- soil, 5.1 across, pivot at the trunk's foot), on the centre line z -200. Clear of the rickshaw lanes (z -213.7 /
-- -186.3), the courier cart's (8 off the middle), the lantern strings (x 488 / 591.75 / 688.25 / 795) and the arrival
-- spawn (640, -200).
for _, x in { 543.5, 616, 664, 736.5 } do
	placeAt(SS.Buildings3D.SakuraTree, x, -200, if x < 640 then 15 else -15)
end

local parts = 0
for _, d in root:GetDescendants() do
	if d:IsA("BasePart") then
		parts += 1
	end
end
return parts

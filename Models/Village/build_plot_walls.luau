--!strict
-- Plot walls (2026-11-05, Allen: "i like the wall we have inbetween plots, lets just replace the fences with walls too").
-- The plot template's low wooden fence (build_plot_fence, 2026-10-26) becomes the town's own wall: copies of
-- the town wall's WallBase (Cobblestone), Wall (Plaster), WallCap and WallRidge (ClayRoofTiles) at the town wall's sizes
-- and heights (ridge top 7.8), with a Pillar + PillarBase + PillarCap at each corner and at each end of a run, along the
-- fence's lines and keeping its openings (the shop door, the bay mouth, the side yard's 6-stud gap). The model keeps the
-- name Fence. Rerunnable, in Edit:
--   loadstring(game.ServerStorage.Builders.build_plot_walls.Source)()
-- Plot space (the template's pivot = PlotSlotN2; -z toward the street, +x the delivery bay's side): x -40..44,
-- z -45.5..76; ground at y -0.5 (world 0).

local X0, X1, Z0, Z1 = -40, 44, -45.5, 76
local GAP = { -36, -30 } -- the side yard's front gap: its pillars stand outside it, so it stays 6 wide
local PILLAR_HALF = 1.5 -- a pillar's base
local SHOP_X = -24.6 -- the front run ends just off the shop's plinth (x -24.5; no pillar there)
local BAY_X = 41 -- just off the outer face of the bay's front post at 40.5 (no pillar there: the post stands)
local G = -0.5 -- ground, plot space

local plot = workspace:WaitForChild("Plot") :: Model
local piv = plot:GetPivot()
-- the town wall's pieces (Village.Walls became the forest, 2026-11-06; one of each kept in ServerStorage.WallPieces)
local town = game:GetService("ServerStorage"):WaitForChild("WallPieces")

-- lihfolk-ignore: findfirstchild-chain (a type cast, checked below)
local fence = plot:FindFirstChild("Fence") :: Model?
local legacy = game:GetService("ServerStorage"):WaitForChild("Legacy")
if fence and not legacy:FindFirstChild("PlotFence_beforeWalls_1105") then
	local keep = fence:Clone()
	keep.Name = "PlotFence_beforeWalls_1105"
	keep.Parent = legacy
end
if fence then
	fence:ClearAllChildren()
else
	local m = Instance.new("Model")
	m.Name = "Fence"
	m.Parent = plot
	fence = m
end
local root = fence :: Model

local function piece(name: string, size: Vector3, at: CFrame)
	-- lihfolk-ignore: findfirstchild-chain (a type cast, checked by the assert)
	local src = town:FindFirstChild(name) :: BasePart?
	assert(src, "ServerStorage.WallPieces has no " .. name)
	local p = src:Clone()
	p.Size = size
	p.CFrame = piv * at
	p.Parent = root
end

local pillars: { [string]: boolean } = {}
local function pillar(x: number, z: number)
	local key = string.format("%.2f,%.2f", x, z)
	if pillars[key] then
		return
	end
	pillars[key] = true
	piece("PillarBase", Vector3.new(3, 1.8, 3), CFrame.new(x, G + 0.9, z))
	piece("Pillar", Vector3.new(2.6, 7.6, 2.6), CFrame.new(x, G + 3.8, z))
	piece("PillarCap", Vector3.new(3.4, 0.6, 3.4), CFrame.new(x, G + 7.9, z))
end

-- a straight wall from a to b (plot-space XZ), pillars at the ends unless told not to
local function run(a: Vector2, b: Vector2, pillarA: boolean, pillarB: boolean)
	local d = b - a
	local L, mid = d.Magnitude, (a + b) / 2
	-- every piece is long along its own X: turned 90° for a run along Z
	local turn = if math.abs(d.X) >= math.abs(d.Y) then CFrame.identity else CFrame.Angles(0, math.rad(90), 0)
	local function at(y: number): CFrame
		return CFrame.new(mid.X, y, mid.Y) * turn
	end
	piece("WallBase", Vector3.new(L, 1.6, 1.6), at(G + 0.8))
	piece("Wall", Vector3.new(L, 5, 1.1), at(G + 4.1))
	piece("WallCap", Vector3.new(L, 0.5, 2.2), at(G + 6.8))
	piece("WallRidge", Vector3.new(L, 1.2, 1.2), at(G + 7.2))
	if pillarA then
		pillar(a.X, a.Y)
	end
	if pillarB then
		pillar(b.X, b.Y)
	end
end

local V = Vector2.new
run(V(X0, Z0), V(X0, Z1), true, true) -- the side yard's side
run(V(X0, Z1), V(X1, Z1), true, true) -- the back
run(V(X1, Z1), V(X1, Z0), true, true) -- the bay's side
run(V(X1, Z0), V(BAY_X, Z0), true, false) -- the corner to the bay's outer post
run(V(X0, Z0), V(GAP[1] - PILLAR_HALF, Z0), true, true) -- the side yard's front, either side of its gap
run(V(GAP[2] + PILLAR_HALF, Z0), V(SHOP_X, Z0), true, false)

-- the wall faces in slate, PaintFloor1 (2026-11-06, Allen: "set the plot walls to slate material paint floor 1"); the town
-- wall (WallPieces) keeps its plaster. Village.Dressing.GapWall, the walls between plots, was set the same by hand.
for _, d in root:GetDescendants() do
	if d:IsA("BasePart") and d.Name == "Wall" then
		d.Material, d.MaterialVariant = Enum.Material.Slate, "PaintFloor1"
	end
end

local n = 0
for _, d in root:GetDescendants() do
	if d:IsA("BasePart") then
		n += 1
	end
end
-- what stood on the fence's line moves clear of the wall (2026-11-05): the bay's crates in from the bay's side, the
-- leaderboard forward from the back corner's pillar
local function nudge(inst: Instance?, by: Vector3)
	if inst and inst:GetAttribute("NudgedForWalls") ~= true then
		inst:SetAttribute("NudgedForWalls", true)
		if inst:IsA("Model") then
			inst:PivotTo(inst:GetPivot() + piv:VectorToWorldSpace(by))
		elseif inst:IsA("BasePart") then
			inst.CFrame += piv:VectorToWorldSpace(by)
		end
	end
end
for _, c in (plot :: any).DeliveryBay:GetChildren() do
	if c.Name == "Crate" then
		nudge(c, Vector3.new(-0.6, 0, 0))
	end
end
nudge(plot:FindFirstChild("Leaderboard"), Vector3.new(-0.6, 0, -1.4))
return n

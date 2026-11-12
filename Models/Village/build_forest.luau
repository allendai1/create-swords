--!strict
-- The forest round the village (2026-11-06, Allen: "Can we remove the outer walls and add a thick green forest so it
-- seems the street is surrounded by trees in a forest"; then "find trees in the toolbox, dont make your own").
-- Clones of ServerStorage.ForestTrees (Toolbox trees, scripts-free, cleaned: Leaves + Trunk MeshParts, pivot at the foot
-- centre): PineS1-3 / PineL1-2 (Cliosow's "Low-Poly Pine Trees Asset Pack", 8559395722) and BroadRound / BroadTall /
-- BroadSmall (from "Low poly tree pack", 93913450362981). Fills the ring between the old town wall line (x 440..888,
-- z -372..-28, now Village.EdgeGuards, invisible) and the hills' feet: broadleaf-and-pine clumps at the inner edge,
-- taller pines behind, sizes growing outward. Keeps clear of the road and gate ends, the two lane exits and every part of
-- the village (houses, street, landmarks, dressing, plot) and the hills. Decor only: no collision, touch or query;
-- CastShadow only on the front band. Seeded, rerunnable, in Edit:
--   loadstring(game.ServerStorage.Builders.build_forest.Source)()
-- Output: Workspace.Village.Atmosphere.Forest (one Atomic Model per tree).

local SS = game:GetService("ServerStorage")
local TREES = SS:WaitForChild("ForestTrees")
local village = workspace:WaitForChild("Village")
local atmosphere = village:WaitForChild("Atmosphere")

local WALL = { x0 = 440, x1 = 888, z0 = -372, z1 = -28 } -- the old town wall line
local OUTER = { x0 = 375, x1 = 955, z0 = -462, z1 = 62 } -- to the hills' feet
local FRONT = 16 -- the front band's depth (broadleaf mix, shadows on)
-- keep-outs (x0, x1, z0, z1): road + west gate (the road ends at x 410), plaza + east gate, the lane exits and their houses
local KEEP = {
	{ 398, 442, -238, -162 },
	{ 886, 922, -238, -162 },
	{ 528, 628, -416, -370 },
	{ 652, 750, -30, 16 },
}
-- canopy half-width of each template at scale 1 (measured from its bounding box)
local SPECIES = {
	PineS1 = 4, PineS2 = 4, PineS3 = 4, PineL1 = 6.9, PineL2 = 6.2,
	BroadRound = 8.3, BroadTall = 6.8, BroadSmall = 5.2,
}
-- the templates and their heights at scale 1
local TEMPLATE: { [string]: Model } = {}
local HEIGHT: { [string]: number } = {}
for name in SPECIES do
	local t = TREES:FindFirstChild(name)
	assert(t and t:IsA("Model"), "ServerStorage.ForestTrees has no " .. name)
	TEMPLATE[name] = t
	HEIGHT[name] = select(2, t:GetBoundingBox()).Y
end
local GREENS = {
	Color3.new(0.17, 0.4, 0.11), Color3.new(0.2, 0.45, 0.15), Color3.new(0.24, 0.5, 0.17), Color3.new(0.15, 0.36, 0.13),
}

local rng = Random.new(1106)
local function pick(list: { string }): string
	return list[rng:NextInteger(1, #list)]
end

local function depth(x: number, z: number): number
	local dx = math.max(WALL.x0 - x, 0, x - WALL.x1)
	local dz = math.max(WALL.z0 - z, 0, z - WALL.z1)
	return math.max(dx, dz)
end

local function kept(x: number, z: number, r: number): boolean
	for _, k in KEEP do
		if x > k[1] - r and x < k[2] + r and z > k[3] - r and z < k[4] + r then
			return true
		end
	end
	return false
end

-- species and scale for a spot: noise patches of pines vs broadleaf, trees grow taller further out
local function choose(x: number, z: number, d: number): (string, number)
	local n = math.noise(x / 55, z / 55, 1.7)
	local name
	if d < FRONT then
		if n > 0.15 then
			name = pick({ "PineS1", "PineS2", "PineS3", "PineL1", "PineL2" })
		else
			name = pick({ "BroadRound", "BroadRound", "BroadSmall", "BroadSmall", "BroadTall" })
		end
	elseif n < -0.25 then
		name = pick({ "BroadTall", "BroadRound" })
	else
		name = pick({ "PineL1", "PineL2", "PineL1", "PineL2", "PineS2" })
	end
	local base = (name:sub(1, 5) == "PineS") and 1.6 or 1
	local grow = 1 + math.min(d, 70) / 70 * 0.9
	return name, base * grow * rng:NextNumber(0.85, 1.15)
end

-- the village and the hills, for overlap checks
local solid = OverlapParams.new()
solid.FilterType = Enum.RaycastFilterType.Include
local inc = { workspace:FindFirstChild("Plot") }
for _, n in { "Houses", "Street", "Landmarks", "Dressing", "Lots" } do
	table.insert(inc, village:FindFirstChild(n))
end
solid.FilterDescendantsInstances = inc
local hills = OverlapParams.new()
hills.FilterType = Enum.RaycastFilterType.Include
hills.FilterDescendantsInstances = { atmosphere:WaitForChild("Backdrop") }

local old = atmosphere:FindFirstChild("Forest")
if old then
	old:Destroy()
end
local root = Instance.new("Folder")
root.Name = "Forest"
root.Parent = atmosphere

-- dart throwing on a 16-stud grid hash: centres at least 0.55 x (r1 + r2) apart, so canopies overlap into a thick wall
local CELL = 16
local grid: { [number]: { { number } } } = {}
local function key(cx: number, cz: number): number
	return cx * 4096 + cz
end
local function free(x: number, z: number, r: number): boolean
	local cx, cz = math.floor(x / CELL), math.floor(z / CELL)
	for i = cx - 2, cx + 2 do
		for j = cz - 2, cz + 2 do
			for _, t in grid[key(i, j)] or {} do
				local need = 0.55 * (r + t[3])
				if (t[1] - x) ^ 2 + (t[2] - z) ^ 2 < need * need then
					return false
				end
			end
		end
	end
	return true
end

local placed = 0
for attempt = 1, 40000 do
	local x = rng:NextNumber(OUTER.x0, OUTER.x1)
	local z = rng:NextNumber(OUTER.z0, OUTER.z1)
	local d = depth(x, z)
	if d > 0 then
		local name, s = choose(x, z, d)
		local r = SPECIES[name] * s
		local t = TEMPLATE[name]
		local h = HEIGHT[name] * s
		if d >= math.max(3, 0.45 * r) and not kept(x, z, 0.7 * r) and free(x, z, r) then
			-- from 1.5 up, so the paving and kerbs at the wall line don't count; houses, lamps and roofs do
			local canopy = workspace:GetPartBoundsInBox(CFrame.new(x, 0.75 + h / 2, z), Vector3.new(1.4 * r, h - 1.5, 1.4 * r), solid)
			-- the whole tree clear of the hills (a canopy inside a hill block shows as leaf bits on its top)
			local foot = workspace:GetPartBoundsInBox(CFrame.new(x, h / 2, z), Vector3.new(1.4 * r, h, 1.4 * r), hills)
			if #canopy == 0 and #foot == 0 then
				local m = t:Clone()
				m:ScaleTo(s)
				m:PivotTo(CFrame.new(x, -0.25 * s, z) * CFrame.Angles(0, rng:NextNumber(0, 2 * math.pi), 0))
				local front = d < FRONT
				local green = GREENS[rng:NextInteger(1, #GREENS)]
				for _, p in m:GetChildren() do
					if p:IsA("BasePart") then
						p.CastShadow = front
						if p.Name == "Leaves" and name:sub(1, 5) == "Broad" then
							p.Color = green
						end
					end
				end
				m.Parent = root
				local c = key(math.floor(x / CELL), math.floor(z / CELL))
				grid[c] = grid[c] or {}
				table.insert(grid[c], { x, z, r })
				placed += 1
				if placed % 60 == 0 then
					task.wait()
				end
			end
		end
	end
	if attempt % 2000 == 0 then
		task.wait()
	end
end
print("build_forest: placed", placed)
return placed

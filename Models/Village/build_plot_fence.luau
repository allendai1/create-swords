-- Plot fence and bigger lots (Allen 2026-10-26: "Make the plot each player owns larger, and add fences around it";
-- he picked option B, 84 x 122). Rerunnable: loadstring(game.ServerStorage.Builders.build_plot_fence.Source)().
-- Plot space (the template's pivot = PlotSlotN2; -z toward the street, +x the delivery bay's side):
--   fence line x -40..44, z -45.5 (just behind the walkway) .. 76 (12 short of the back wall).
--   Front pieces only where no building is: shop wall (x -24) to the corner with a 6-stud gap (x -36..-30) into the
--   side yard, and the bay's outer post (40.5) to the corner. The shop door and the bay mouth stay open.
-- Village.Lots.Pad<each lot> grows to the same footprint (front edge stays at z -48, under the walkway); the old curb
-- Edges go (the fence replaces them). Backup of both: ServerStorage.Legacy.Lots_beforeBigPlots.

local X0, X1, Z0, Z1 = -40, 44, -45.5, 76
local PAD_FRONT = -48
local GAP = { -36, -30 }
local SPACING = 6 -- most studs between posts
local FOOT, TOP = -0.5, 3.1 -- post bottom (world 0, under the lot pad's top) and top, plot space
local POST, RAIL_T, RAIL_H = 0.6, 0.3, 0.4
local RAILS = { 0.9, 2.3 } -- rail centre heights, plot space (the bay's rails are at 0.9 and 2.2)

local plot = workspace:WaitForChild("Plot") :: Model
local piv = plot:GetPivot()

local old = plot:FindFirstChild("Fence")
if old then
	old:Destroy()
end
local fence = Instance.new("Model")
fence.Name = "Fence"

local function part(name: string, size: Vector3, at: CFrame, variant: string, hex: string)
	local p = Instance.new("Part")
	p.Name = name
	p.Anchored = true
	p.TopSurface, p.BottomSurface = Enum.SurfaceType.Smooth, Enum.SurfaceType.Smooth
	p.Material = Enum.Material.Wood
	p.MaterialVariant = variant
	p.Color = Color3.fromHex(hex)
	p.Size = size
	p.CFrame = piv * at
	p.Parent = fence
end

local function post(x: number, z: number)
	part("Post", Vector3.new(POST, TOP - FOOT, POST), CFrame.new(x, (TOP + FOOT) / 2, z), "PaintWoodDark", "462e20")
end

-- a straight run from a to b (plot-space XZ), posts at both ends and evenly between; rails end inside the end posts
local function run(a: Vector2, b: Vector2, posts: { [string]: boolean })
	local d = b - a
	local n = math.max(1, math.ceil(d.Magnitude / SPACING))
	for i = 0, n do
		local p = a + d * (i / n)
		local key = string.format("%.2f,%.2f", p.X, p.Y)
		if not posts[key] then -- corner posts are shared
			posts[key] = true
			post(p.X, p.Y)
		end
	end
	local mid = (a + b) / 2
	local alongX = math.abs(d.X) > math.abs(d.Y)
	for _, y in RAILS do
		local size = if alongX
			then Vector3.new(d.Magnitude, RAIL_H, RAIL_T)
			else Vector3.new(RAIL_T, RAIL_H, d.Magnitude)
		part("Rail", size, CFrame.new(mid.X, y, mid.Y), "PaintWood", "805836")
	end
end

local posts = { ["40.50,-45.50"] = true } -- the bay's own front post stands there
local V = Vector2.new
run(V(X0, Z0), V(X0, Z1), posts) -- side yard's side
run(V(X0, Z1), V(X1, Z1), posts) -- back
run(V(X1, Z1), V(X1, Z0), posts) -- bay's side
run(V(X1, Z0), V(40.5, Z0), posts) -- corner to the bay's outer front post; the rails end inside it
run(V(X0, Z0), V(GAP[1], Z0), posts) -- side yard's front, either side of the gap
run(V(GAP[2], Z0), V(-24.4, Z0), posts) -- the last post stands just off the shop's side wall (x -24)
fence.Parent = plot

-- the lots' ground: same footprint on every lot (PlotService turns the plot onto each slot the same way)
local lots = workspace.Village.Lots
local legacy = game.ServerStorage:WaitForChild("Legacy")
if not legacy:FindFirstChild("Lots_beforeBigPlots") then
	local keep = Instance.new("Folder")
	keep.Name = "Lots_beforeBigPlots"
	for _, c in lots:GetChildren() do
		if c.Name == "Pad" or c.Name == "Edge" then
			c:Clone().Parent = keep
		end
	end
	keep.Parent = legacy
end
for _, c in lots:GetChildren() do
	if c.Name == "Edge" then
		c:Destroy()
	end
end
for _, slot in lots:GetChildren() do
	local lot = slot.Name:match("^PlotSlot(%u%d)$")
	if lot and slot:IsA("BasePart") then
		-- each lot's pad sits at its slot's centre; take the nearest
		local pad, best = nil, math.huge
		for _, c in lots:GetChildren() do
			if c.Name == "Pad" and c:IsA("BasePart") then
				local dist = (c.Position - slot.Position) * Vector3.new(1, 0, 1)
				if dist.Magnitude < best then
					pad, best = c, dist.Magnitude
				end
			end
		end
		if pad then
			local h = pad.Size.Y
			pad.Size = Vector3.new(X1 - X0, h, Z1 - PAD_FRONT)
			pad.CFrame = slot.CFrame * CFrame.new((X0 + X1) / 2, h / 2 - slot.Position.Y, (PAD_FRONT + Z1) / 2)
		end
	end
end

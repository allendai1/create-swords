-- Part mountains (2026-11-01): stacked rectangular blocks (Allen: "rectangular not actually like mountain shaped"), snow top over 150 studs,
-- three rows (green hills, rock, tall rock) along each side of a rectangle around the village. Seeded, so reruns match.
-- Run in Edit via execute_luau; it replaces Backdrop.Mountains.
local SS = game.ServerStorage
local Backdrop = workspace.Village.Atmosphere.Backdrop
local old = Backdrop:FindFirstChild("Mountains")
if old then
	old:Destroy() -- this script rebuilds it
end
local M = Instance.new("Model")
M.Name = "Mountains"
M.ModelStreamingMode = Enum.ModelStreamingMode.Persistent

local rng = Random.new(20261101)
-- Allen: "dark stone grey": every hill and rock block is BrickColor Dark stone grey (two tables keep the seeded sequence)
local GREY = { BrickColor.new("Dark stone grey").Color }
local ROCK, GREEN = GREY, GREY
local SNOW = Color3.fromRGB(242, 245, 250)
local BASE_Y = -2

-- Each mountain is a stack of rectangular blocks that shrink toward the top; the top block of a tall rock one is snow.
local function block(parent, cf, size, color)
	local p = Instance.new("Part")
	p.Anchored, p.CanCollide, p.CanQuery, p.CanTouch, p.CastShadow = true, false, false, false, false
	p.Material = Enum.Material.SmoothPlastic
	p.TopSurface, p.BottomSurface = Enum.SurfaceType.Smooth, Enum.SurfaceType.Smooth
	p.Color = color
	p.Size = size
	p.CFrame = cf
	p.Parent = parent
end

local count = 0
-- place(off) gives the centre for a depth offset outward from the rectangle; rot turns the long side along it
local function mountain(place, front, h, kind, rot)
	local m = Instance.new("Model")
	m.Name = "Mountain"
	local w = h * rng:NextNumber(1.6, 2.4)
	local d = h * rng:NextNumber(1.2, 1.8)
	local x, z = place(front + d / 2) -- front face stays on the row line, never inside the rectangle
	local yaw = (rot or 0) + math.rad(rng:NextNumber(-8, 8))
	local tiers = if kind == "hill" then 1 else rng:NextInteger(2, 3)
	local color = if kind == "hill" then GREEN[rng:NextInteger(1, #GREEN)] else ROCK[rng:NextInteger(1, #ROCK)]
	local y, ox, oz = BASE_Y, 0, 0
	for t = 1, tiers do
		local th = h / tiers * rng:NextNumber(0.85, 1.15)
		local k = 1 - (t - 1) / tiers * 0.7
		local sw, sd = w * k * rng:NextNumber(0.9, 1.05), d * k * rng:NextNumber(0.9, 1.05)
		if t > 1 then
			ox += rng:NextNumber(-0.08, 0.08) * w
			oz += rng:NextNumber(-0.08, 0.08) * d
		end
		local snow = kind ~= "hill" and h > 150 and t == tiers
		block(m, CFrame.new(x, 0, z) * CFrame.Angles(0, yaw, 0) * CFrame.new(ox, y + th / 2, oz), Vector3.new(sw, th, sd), if snow then SNOW else color)
		y += th
	end
	m.Parent = M
	count += 1
end

-- inner rectangle (play bounds x 410..898, z -410..10, 30 studs margin)
local X0, X1, Z0, Z1 = 380, 928, -440, 40
local ROWS = {
	{ d = 0, hMin = 35, hMax = 70, kind = "hill", step = 70 },
	{ d = 60, hMin = 120, hMax = 200, kind = "rock", step = 130 },
	{ d = 160, hMin = 220, hMax = 320, kind = "rock", step = 190 },
}
local function side(from, to, at)
	for _, r in ROWS do
		local t = from - r.d
		while t < to + r.d do
			local h = rng:NextNumber(r.hMin, r.hMax)
			local off = r.d + rng:NextNumber(0, 20)
			at(t + rng:NextNumber(-r.step * 0.2, r.step * 0.2), off, h, r.kind)
			t += r.step * rng:NextNumber(0.8, 1.1)
		end
		task.wait()
	end
end
side(X0, X1, function(t, off, h, k) mountain(function(o) return t, Z0 - o end, off, h, k) end) -- north
side(X0, X1, function(t, off, h, k) mountain(function(o) return t, Z1 + o end, off, h, k) end) -- south
side(Z0, Z1, function(t, off, h, k) mountain(function(o) return X0 - o, t end, off, h, k, math.pi / 2) end) -- west
side(Z0, Z1, function(t, off, h, k) mountain(function(o) return X1 + o, t end, off, h, k, math.pi / 2) end) -- east
M.Parent = Backdrop
return "mountains " .. count

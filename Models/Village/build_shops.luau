-- build_shops.luau: the shop and its back-room workshop as one street townhouse (2026-10-21).
-- Allen, first: "Make our normal shop and upgraded shop blend seamlessly with the surrounding houses ... we can have
-- the smelting and sword creation process inside a building as well". Then his layout References/Concept Art/shop
-- design ("Shop + back-room workshop"): the shop on the street, a centre door into the workshop behind it, stations
-- clockwise round the workshop walls. Like a real machiya: shop in front, workshop running back behind it.
-- Same parts, palette and details as build_street.luau's townhouses (posts, koshi lattice bays, noren, pent roof, kura
-- upper storey, ClayRoofTiles roofs). Run in Studio (Edit) through MCP execute_luau after the map builder
-- (build_simple.luau since 2026-10-22); it builds wherever Workspace.Plot stands (its pivot is its lot's centre).
-- Roofs keep their eaves to the street: gable fronts were tried on 2026-10-22 and undone (Allen: "undo it so the roofs
-- face the entrance").
-- Rebuilds Shop.Starter.Shell and Shop.Upgraded.Shell (the shop room; they swap on the Upgraded Store pad) and sets
-- their Floor and InsideZone, and rebuilds Plot.Workshop (front wall with the door, workshop walls, floor, roof) and
-- Yard.ShopFront. A model this script didn't build goes to Legacy instead.
-- Stations, displays and pads are placed by hand or by build_workshop.luau (the workshop's furniture and layout, run
-- after this script); this script only builds the building.
-- Workspace.Plot in lot N2 is the template every player's plot is copied from (PlotService, vault: Design/Six Plots).
-- Its pivot is PlotSlotN2's CFrame, 48 behind the façade line.
-- The shop grows on the upgrade (Allen 2026-10-21: "the shop expands upon upgrade [and] the blacksmith area just gets
-- pushed further back"): the Starter's shop room ends at the workshop's front wall (PZ); the Upgraded Store's walls
-- and roof run 12 further, to SZ, and TycoonService moves the workshop back 12 when the upgrade is bought.
-- This builds the Starter layout: the workshop at PZ.
--
-- Frame (like the townhouses): local z = 0 on the street side, +z goes in, local x runs across the frontage
-- (the 180° turn makes local +x world west). 48 wide: walls 0.5 thick on 0.8 posts, inner faces at x ±23.5.
-- Starter: shop room z 1.5 … 29.75, workshop front wall 29.75 … 30.25, workshop 30.25 … 80.25, back wall to 80.75.
-- Upgraded: shop room 1.5 … 41.75, everything of the workshop 12 further back (back wall to 92.75, inside the lot).
-- Everything above a room's eave is under its Shell.Roof, so RoofHider fades it while you're in that room.

local SHOP_CF = workspace.Plot:GetPivot() * CFrame.new(0, -0.5, -48) -- frontage centre on the façade line
local T = 0.5 -- wall thickness
local HW = 24 -- half width
local XS = HW - T / 2 -- side wall centre line
local PZ = 30 -- the workshop's front wall in the Starter layout: the back of the Starter's shop room
local SZ = 42 -- the back of the Upgraded Store's shop room, where the workshop's front wall goes on the upgrade
local BZ = 80.75 -- back of the workshop (Starter layout)
-- Ground storeys 2.5 taller (Allen 2026-10-21: "right now the entrance is barely taller than the player"), as on the
-- street: openings top out at OT 9.7, the shop's storey is 13.5, the workshop's eave 15.5 and its door 10.5.
local LIFT = 2.5
local OT = 7.2 + LIFT

local SS = game:GetService("ServerStorage")
local CS = game:GetService("CollectionService")
local M = Enum.Material
local rad = math.rad
local LEGACY = SS:FindFirstChild("Legacy") or SS

local C = {
	timberDk = Color3.fromRGB(56, 38, 28),
	timber = Color3.fromRGB(92, 63, 42),
	cedar = Color3.fromRGB(134, 94, 60),
	slat = Color3.fromRGB(72, 50, 36),
	plaster = Color3.fromRGB(232, 226, 212),
	cream = Color3.fromRGB(220, 200, 160),
	kuroPl = Color3.fromRGB(44, 44, 46),
	tile = Color3.fromRGB(80, 86, 94),
	tileDk = Color3.fromRGB(58, 62, 68),
	stoneLt = Color3.fromRGB(168, 162, 152),
	indigo = Color3.fromRGB(38, 54, 96),
	red = Color3.fromRGB(190, 52, 40),
	paper = Color3.fromRGB(240, 226, 196),
	black = Color3.fromRGB(24, 22, 22),
	interior = Color3.fromRGB(30, 22, 18),
	pot = Color3.fromRGB(160, 92, 62),
	pipe = Color3.fromRGB(150, 94, 60),
}

-- part / cyl / ball / glow / label / chochin: as in build_street.luau
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
local UP = CFrame.Angles(0, 0, math.pi / 2)
local function cyl(parent, name, h, d, cf, col, mat)
	return part(parent, name, Vector3.new(h, d, d), cf * UP, col, mat, { shape = Enum.PartType.Cylinder })
end
local function ball(parent, name, d, cf, col, mat)
	return part(parent, name, Vector3.new(d, d, d), cf, col, mat, { shape = Enum.PartType.Ball })
end
local function glow(p, range)
	local l = Instance.new("PointLight")
	l.Color = Color3.fromRGB(255, 176, 104)
	l.Range = range or 14
	l.Brightness = 1.3
	l.Shadows = false
	l.Parent = p
end
local function label(p, text, col, vertical)
	local g = Instance.new("SurfaceGui")
	g.Face = Enum.NormalId.Front
	g.SizingMode = Enum.SurfaceGuiSizingMode.PixelsPerStud
	g.PixelsPerStud = 40
	g.LightInfluence = 1
	local t = Instance.new("TextLabel")
	t.BackgroundTransparency = 1
	t.Size = UDim2.fromScale(0.84, 0.9)
	t.Position = UDim2.fromScale(0.08, 0.05)
	t.Font = Enum.Font.SourceSansBold
	t.TextScaled = true
	t.TextColor3 = col
	if vertical then
		local cs = {}
		for _, c in utf8.codes(text) do table.insert(cs, utf8.char(c)) end
		t.Text = table.concat(cs, "\n")
	else
		t.Text = text
	end
	t.Parent = g
	g.Parent = p
end
local function chochin(parent, cf, col)
	local b = cyl(parent, "Chochin", 1.9, 1.5, cf, col)
	cyl(parent, "ChochinCap", 0.22, 1.0, cf * CFrame.new(0, 1.03, 0), C.black)
	cyl(parent, "ChochinCap", 0.22, 1.0, cf * CFrame.new(0, -1.03, 0), C.black)
	part(parent, "Cord", Vector3.new(0.08, 1.0, 0.08), cf * CFrame.new(0, 1.6, 0), C.black)
	glow(b, 12)
end

local L = function(x, y, z) return SHOP_CF * CFrame.new(x, y, z) end
local function box(parent, name, x0, x1, y0, y1, z0, z1, col, mat, o)
	return part(parent, name, Vector3.new(x1 - x0, y1 - y0, z1 - z0), L((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), col, mat, o)
end

local function fresh(parent, name)
	local old = parent:FindFirstChild(name)
	if old then
		if old:GetAttribute("BuiltBy") == "build_shops" then
			old:Destroy()
		else
			old.Name = (parent == workspace and "" or parent.Name) .. name .. "_beforeBackRoom"
			old.Parent = LEGACY
		end
	end
	local m = Instance.new("Model")
	m.Name = name
	m:SetAttribute("BuiltBy", "build_shops")
	return m
end

-- One wall between post centres a and b. axis "z": a side wall on the line x = at; axis "x": a cross wall on the line
-- z = at; out is the sign of its outside. kind "wall", "window" (high lattice window outside) or "door" (open below
-- w.doorH). Cross-wall plates sit 0.02 lower than side-wall plates, so the corner overlaps never share a face.
local function wallRun(m, axis, at, out, a, b, kind, w)
	local function seg(name, s0, s1, y0, y1, th, off, col, mat, solid)
		local c = at + off
		local size = axis == "z" and Vector3.new(th, y1 - y0, s1 - s0) or Vector3.new(s1 - s0, y1 - y0, th)
		local cf = axis == "z" and L(c, (y0 + y1) / 2, (s0 + s1) / 2) or L((s0 + s1) / 2, (y0 + y1) / 2, c)
		return part(m, name, size, cf, col, mat, { solid = solid })
	end
	local G = w.G
	local s0, s1 = math.min(a, b) + 0.3, math.max(a, b) - 0.3
	local dp = axis == "x" and 0.02 or 0
	seg("Plate", s0 - 0.2, s1 + 0.2, G - 0.7 - dp, G - dp, T + 0.22, 0, C.timberDk, M.Wood)
	if kind == "door" then
		seg("Lintel", s0, s1, w.doorH, w.doorH + 0.7, T + 0.16, 0, C.timberDk, M.Wood, true)
		seg("Plaster", s0, s1, w.doorH + 0.6, G - 0.65, T, 0, C.plaster, M.Plaster, true)
		return
	end
	seg("Wainscot", s0, s1, 0, 3.2, T + 0.1, 0, C.timberDk, M.Wood, true)
	seg("Plaster", s0, s1, 3.1, G - 0.65, T, 0, C.plaster, M.Plaster, true)
	seg("Band", s0, s1, 7.6 + LIFT, 8.2 + LIFT, T + 0.16, 0, C.timberDk, M.Wood)
	if kind == "window" then
		local cx, ww = (s0 + s1) / 2, math.min(4.2, s1 - s0 - 1.6)
		local y0, y1 = 8.9 + LIFT, G - 1.7
		local face = out * T / 2
		seg("WinPane", cx - ww / 2, cx + ww / 2, y0, y1, 0.06, face + out * 0.02, C.interior)
		seg("WinSill", cx - ww / 2 - 0.3, cx + ww / 2 + 0.3, y0 - 0.25, y0, 0.3, face + out * 0.13, C.timberDk, M.Wood)
		seg("WinHead", cx - ww / 2 - 0.3, cx + ww / 2 + 0.3, y1, y1 + 0.25, 0.3, face + out * 0.13, C.timberDk, M.Wood)
		local n = math.max(3, math.floor(ww / 0.45))
		for k = 1, n - 1 do
			local sx = cx - ww / 2 + k * ww / n
			seg("WinSlat", sx - 0.08, sx + 0.08, y0 - 0.05, y1 + 0.05, 0.12, face + out * 0.08, C.slat, M.Wood)
		end
	end
end

-- Posts and walls: side walls on x = ±XS through the z posts in w.sides[±1] (kinds in w.sideKinds[±1]), and cross
-- walls in w.runs ({ at, out, list of x posts, kinds }). Posts listed in w.skip ("x,z") belong to another model.
local function walls(m, w)
	local made = table.clone(w.skip or {})
	local function post(x, z)
		local key = ("%.2f,%.2f"):format(x, z)
		if made[key] then return end
		made[key] = true
		part(m, "Post", Vector3.new(0.8, w.G - 0.05, 0.8), L(x, (w.G - 0.05) / 2, z), C.timberDk, M.Wood, { solid = true })
	end
	for s = -1, 1, 2 do
		local list = w.sides[s]
		if list then
			for i = 1, #list do
				post(s * XS, list[i])
				if i > 1 then
					wallRun(m, "z", s * XS, s, list[i - 1], list[i], w.sideKinds and w.sideKinds[s] and w.sideKinds[s][i - 1] or "wall", w)
				end
			end
		end
	end
	for _, run in w.runs or {} do
		for i = 1, #run.list do
			post(run.list[i], run.at)
			if i > 1 then
				wallRun(m, "x", run.at, run.out, run.list[i - 1], run.list[i], run.kinds and run.kinds[i - 1] or "wall", w)
			end
		end
	end
end

-- Main roof with its ridge parallel to the street (the townhouses' non-gable-front roof, from build_street.luau).
local function mainRoof(roof, o)
	local th = o.th or 0.6
	local p = rad(o.pitch)
	local t, cs, sn = math.tan(p), math.cos(p), math.sin(p)
	local zr = (o.front + o.D) / 2
	local yr = o.H + (zr - o.front) * t
	local zf, zb = o.front - o.ovF, o.D + o.ovB
	local xl = 2 * HW + 2 * o.ovS
	local runF, runB = zr - zf, zb - zr
	local cF = Vector3.new(0, yr - runF / 2 * t, (zf + zr) / 2) + Vector3.new(0, cs, -sn) * (th / 2 - 0.05)
	part(roof, "Roof", Vector3.new(xl, th, runF / cs), L(cF.X, cF.Y, cF.Z) * CFrame.Angles(-p, 0, 0), o.roofCol, M.ClayRoofTiles)
	local cB = Vector3.new(0, yr - runB / 2 * t, (zr + zb) / 2) + Vector3.new(0, cs, sn) * (th / 2 - 0.05)
	part(roof, "Roof", Vector3.new(xl + 0.08, th, runB / cs), L(cB.X, cB.Y, cB.Z) * CFrame.Angles(p, 0, 0), o.roofCol, M.ClayRoofTiles)
	part(roof, "Ridge", Vector3.new(xl + 0.2, o.ridgeH, 1.3), L(0, yr + th + o.ridgeH / 2 - 0.35, zr), C.tileDk, M.ClayRoofTiles)
	if o.oni then
		for sgn = -1, 1, 2 do
			part(roof, "Onigawara", Vector3.new(1.0, o.ridgeH + 1.4, 2.0), L(sgn * (xl / 2 + 0.3), yr + th + (o.ridgeH + 1.4) / 2 - 0.4, zr), C.tileDk, M.ClayRoofTiles)
		end
	end
	if o.ovF > 1 then
		part(roof, "Fascia", Vector3.new(xl - 0.08, 0.5, 0.3), L(0, o.H - o.ovF * t - 0.1, zf + 0.1), C.timberDk, M.Wood)
	end
	local gh = yr - o.H + 0.05 -- gables start 0.05 down inside the plate below
	for sgn = -1, 1, 2 do
		part(roof, "Gable", Vector3.new(0.5, gh, zr - o.front), L(sgn * (HW - 0.3), o.H - 0.05 + gh / 2, (o.front + zr) / 2), o.gableCol, M.Plaster, { wedge = true })
		part(roof, "Gable", Vector3.new(0.5, gh, o.D - zr), L(sgn * (HW - 0.3), o.H - 0.05 + gh / 2, (zr + o.D) / 2) * CFrame.Angles(0, math.pi, 0), o.gableCol, M.Plaster, { wedge = true })
	end
	return yr, zr
end

-- A slab whose underside runs from (z0, y0) to (z1, y1), xw wide around x = cx.
local function slope(parent, name, cx, xw, z0, y0, z1, y1, th, col, mat)
	local d = Vector3.new(0, y1 - y0, z1 - z0)
	local up = Vector3.new(0, math.abs(d.Z), -d.Y * math.sign(d.Z)) / d.Magnitude
	local mid = Vector3.new(cx, (y0 + y1) / 2, (z0 + z1) / 2) + up * (th / 2 - 0.05)
	return part(parent, name, Vector3.new(xw, th, d.Magnitude), L(mid.X, mid.Y, mid.Z) * CFrame.fromMatrix(Vector3.zero, Vector3.xAxis, up), col, mat)
end

-- ---------------------------------------------------------------- shop room (Starter / Upgraded front)
-- The Starter is one storey with a deep eave; the Upgraded Store is a two-storey black kura with its signboard on the
-- pent roof (like the street's 呉服 and 酒造 houses). Each runs back to where the workshop's front wall stands with it:
-- the Starter to PZ (28 deep), the Upgraded Store to SZ (40 deep).
local G, F0 = 11 + LIFT, 1.5
local FRONT_POSTS = { -23.75, -18.4, -13, -6.7, 6.7, 13, 18.4, 23.75 } -- bay 4 is the entrance (12.5 clear)
-- side-wall posts, clear of the wall racks (z 8…12 for racks 1 and 2, 28…32 for racks 3 and 4)
local STARTER_SIDES = { 1.05, 15, 25, PZ }
local UPGRADED_SIDES = { 1.05, 15, 25, 35, SZ }
local CROSS_POSTS = { -XS, -13, -3.4, 3.4, 13, XS } -- the workshop's front wall; door between ±3.4

-- commissions board on a back wall, west of the door; E opens the shop's requests (CommissionController, 2026-10-22)
local function commissionBoard(parent, z) -- z: the wall's shop face
	local b = Instance.new("Model")
	b.Name = "CommissionBoard"
	local board = box(b, "Board", 7.0, 12.0, 3.2, 6.6, z - 0.2, z + 0.01, C.cedar, M.WoodPlanks) -- clear of the posts at x 3.4 and 13
	local prompt = Instance.new("ProximityPrompt")
	prompt.Name = "RequestsPrompt"
	prompt.ActionText = "Requests"
	prompt.KeyboardKeyCode = Enum.KeyCode.E
	prompt.HoldDuration = 0
	prompt.MaxActivationDistance = 8
	prompt.RequiresLineOfSight = false
	prompt.Parent = board
	box(b, "BoardFrame", 6.8, 12.2, 6.6, 7.0, z - 0.3, z + 0.02, C.timberDk, M.Wood)
	box(b, "BoardFrame", 6.8, 12.2, 2.9, 3.2, z - 0.3, z + 0.02, C.timberDk, M.Wood)
	local header = box(b, "Header", 8.4, 10.6, 7.0, 7.9, z - 0.25, z - 0.05, C.timberDk, M.Wood)
	label(header, "依頼", C.paper)
	for i, slip in { { 7.8, 5.2 }, { 9.1, 5.5 }, { 10.4, 5.0 }, { 11.4, 5.6 }, { 8.5, 3.9 }, { 10.7, 3.8 } } do
		box(b, "Slip" .. i, slip[1] - 0.45, slip[1] + 0.45, slip[2] - 0.6, slip[2] + 0.6, z - 0.26, z - 0.2, C.paper)
	end
	b.Parent = parent
end

-- a doorway's threshold and a short indigo noren on its shop side (wall centre line z)
local function doorDressing(parent, z)
	box(parent, "Threshold", -3.4, 3.4, 0, 0.3, z - 0.3, z + 0.3, C.timber, M.Wood, { solid = true })
	local nw, x0, x1 = 3, -3.0, 3.0
	for k = 0, nw - 1 do
		local w = (x1 - x0) / nw
		part(parent, "Noren", Vector3.new(w - 0.08, 2.4, 0.08), L(x0 + w * (k + 0.5), 6.5 + LIFT, z - 0.45), C.indigo, M.Fabric)
	end
	part(parent, "NorenRod", Vector3.new(x1 - x0 + 0.9, 0.15, 0.15), L(0, 7.75 + LIFT, z - 0.45), C.timberDk, M.Wood)
end

local function shopFront(m, transomCol)
	for _, x in FRONT_POSTS do
		part(m, "Post", Vector3.new(0.9, G - 0.35, 0.9), L(x, 0.3 + (G - 0.35) / 2, F0 - 0.45), C.timberDk, M.Wood, { solid = true })
	end
	for i = 1, #FRONT_POSTS - 1 do
		local x0, x1 = FRONT_POSTS[i] + 0.45, FRONT_POSTS[i + 1] - 0.45
		local cx, cw = (x0 + x1) / 2, x1 - x0
		if i == 4 then
			local nw = cw / 5
			for k = 0, 4 do
				local strip = part(m, "Noren", Vector3.new(nw - 0.08, 2.7, 0.08), L(x0 + nw * (k + 0.5), OT - 1.35, F0 - 0.95), C.indigo, M.Fabric)
				if k == 2 then label(strip, "刀", C.paper) end
			end
			part(m, "NorenRod", Vector3.new(cw + 0.1, 0.15, 0.15), L(cx, OT + 0.05, F0 - 0.95), C.timberDk, M.Wood)
		else
			part(m, "Kick", Vector3.new(cw + 0.1, 1.2, 0.35), L(cx, 0.9, F0 - 0.25), C.timberDk, M.Wood, { solid = true })
			part(m, "Rail", Vector3.new(cw + 0.1, 0.4, 0.35), L(cx, OT + 0.2, F0 - 0.25), C.timberDk, M.Wood)
			part(m, "Shoji", Vector3.new(cw + 0.1, OT - 1.5, 0.1), L(cx, (1.5 + OT) / 2, F0 - 0.1), C.paper, nil, { solid = true })
			local n = math.max(2, math.floor(cw / 0.55))
			for k = 1, n - 1 do
				part(m, "Slat", Vector3.new(0.22, OT - 1.5, 0.3), L(x0 + k * cw / n, (1.5 + OT) / 2, F0 - 0.35), C.slat, M.Wood)
			end
		end
	end
	part(m, "Beam", Vector3.new(2 * XS, 0.8, 0.7), L(0, OT + 0.75, F0 - 0.3), C.timberDk, M.Wood)
	part(m, "Transom", Vector3.new(2 * XS - 0.4, G - OT - 1.25, 0.1), L(0, (OT + 1.15 + G - 0.1) / 2, F0 - 0.1), transomCol, M.Plaster)
	part(m, "FrontPlate", Vector3.new(2 * XS + 0.2, 0.7, 0.5), L(0, G - 0.37, F0 - 0.27), C.timberDk, M.Wood) -- 0.02 off the posts' back faces
	local sign = part(m, "Signboard", Vector3.new(1.5, 4.4, 0.3), L(13, OT - 2.3, F0 - 1.1), C.timber, M.Wood)
	label(sign, "刀剣", C.black, true)
end

local function shopRoom(model, U)
	local shell = fresh(model, "Shell")
	local roof = Instance.new("Model")
	roof.Name = "Roof"
	roof.Parent = shell
	shopFront(shell, U > 0 and C.kuroPl or C.cream)
	-- side walls back to the workshop's front wall; the façade's corner posts and the workshop's corner posts aren't ours
	local back = if U > 0 then SZ else PZ
	local sides = if U > 0 then UPGRADED_SIDES else STARTER_SIDES
	walls(shell, {
		G = G, sides = { [-1] = sides, [1] = sides },
		skip = {
			[("%.2f,%.2f"):format(-XS, 1.05)] = true, [("%.2f,%.2f"):format(XS, 1.05)] = true,
			[("%.2f,%.2f"):format(-XS, back)] = true, [("%.2f,%.2f"):format(XS, back)] = true,
		},
	})
	commissionBoard(shell, back - T / 2)
	local H = G + U
	if U > 0 then
		-- kura upper storey: black plaster block, shuttered windows, hachimaki band, pent roof with the signboard
		local F1 = F0 + 0.05
		part(roof, "Upper", Vector3.new(2 * HW, U + 0.05, SZ - F1), L(0, G - 0.05 + (U + 0.05) / 2, (F1 + SZ) / 2), C.kuroPl, M.Plaster)
		local wy = H - 3.4
		for i = 1, 4 do
			local wx = -HW + i * 2 * HW / 5
			part(roof, "WinSurround", Vector3.new(2.8, 3.0, 0.35), L(wx, wy, F1 - 0.175), C.kuroPl, M.Plaster)
			part(roof, "Window", Vector3.new(2.0, 2.2, 0.1), L(wx, wy, F1 - 0.34), C.interior)
			for sgn = -1, 1, 2 do
				part(roof, "WinShutter", Vector3.new(1.1, 2.6, 0.45), L(wx + sgn * 2.05, wy, F1 - 0.4), C.kuroPl, M.Plaster)
			end
		end
		part(roof, "Hachimaki", Vector3.new(2 * HW - 0.2, 1.0, 0.6), L(0, H - 0.54, F1 - 0.3), C.kuroPl, M.Plaster)
		local pp = rad(22)
		local tp = math.tan(pp)
		local zLo, yLo = -4.2, G - 0.2
		local zHi = F1 + 0.3
		local yHi = yLo + (zHi - zLo) * tp
		local nrm = Vector3.new(0, math.cos(pp), -math.sin(pp))
		local c = Vector3.new(0, (yLo + yHi) / 2, (zLo + zHi) / 2) + nrm * 0.2
		part(roof, "PentRoof", Vector3.new(2 * HW - 0.28, 0.5, (zHi - zLo) / math.cos(pp)), L(c.X, c.Y, c.Z) * CFrame.Angles(-pp, 0, 0), C.tileDk, M.ClayRoofTiles)
		part(roof, "PentFascia", Vector3.new(2 * HW - 0.36, 0.55, 0.25), L(0, yLo - 0.05, zLo + 0.1), C.timberDk, M.Wood)
		for _, px in FRONT_POSTS do
			part(roof, "BeamEnd", Vector3.new(0.55, 0.65, F0 + 0.3 - zLo - 0.6), L(px, G - 0.55, (F0 + 0.3 + zLo + 0.6) / 2), C.timberDk, M.Wood)
		end
		part(roof, "Gutter", Vector3.new(2 * HW - 0.2, 0.35, 0.35), L(0, yLo - 0.45, zLo + 0.05), C.pipe, M.Metal, { shape = Enum.PartType.Cylinder })
		cyl(roof, "Downpipe", yLo - 0.75, 0.3, L(-(HW - 0.6), 0.3 + (yLo - 0.75) / 2, zLo + 0.05), C.pipe, M.Metal)
		local kanban = part(roof, "Kanban", Vector3.new(12, 2.0, 0.35), L(0, G + 2.5, F1 - 1.3), C.timberDk, M.Wood)
		label(kanban, "刀鍛冶", C.paper)
		mainRoof(roof, { front = F1, D = SZ, H = H, pitch = 26, ovF = 2.6, ovB = 0.2, ovS = 0.6, ridgeH = 1.8, oni = true, roofCol = C.tileDk, gableCol = C.kuroPl })
		for sgn = -1, 1, 2 do chochin(shell, L(sgn * 9, G - 1.6, -2.4), C.red) end
	else
		-- one storey under a deep eave; the signboard stands on the roof above it (the eave hides the transom)
		local kanban = part(roof, "Kanban", Vector3.new(9, 2.0, 0.35), L(0, 11.4 + LIFT, -0.6), C.timberDk, M.Wood)
		label(kanban, "刀鍛冶", C.paper)
		-- ovF 3.5, not the low houses' 3.6: next to one of the same height their fascias would share a plane
		mainRoof(roof, { front = F0, D = PZ, H = H, pitch = 26, ovF = 3.5, ovB = 0.2, ovS = 0.6, ridgeH = 0.9, roofCol = C.tile, gableCol = C.plaster })
		for sgn = -1, 1, 2 do chochin(shell, L(sgn * 9, G - 3.2, -0.9), C.red) end
	end
	shell.Parent = model

	-- floor and roof-fade zone run back to the workshop's front wall
	local floor, zone = model.Floor, model.InsideZone
	floor.Size = Vector3.new(2 * 23.55, 0.2, back - 0.2 - 1.4)
	floor.CFrame = L(0, 0.1, (1.4 + back - 0.2) / 2)
	zone.Size = Vector3.new(46.8, 12 + LIFT, back - 0.35 - 1.55)
	zone.CFrame = L(0, 6.2 + LIFT / 2, (1.55 + back - 0.35) / 2)
end

local plot = workspace.Plot
local shops = plot.Shop
shopRoom(shops.Starter, 0)
task.wait()
shopRoom(shops.Upgraded, 8.5)
task.wait()

-- ---------------------------------------------------------------- workshop (shared, behind the shop)
-- Eave 15.5 (13 before the lift), a smoke vent (koshi-yane) on the ridge over the furnaces, high lattice windows outside. The front wall (PZ)
-- has the centre door (indigo noren on the shop side). The ore slots stand in a supply chest built by build_workshop.luau
-- (2026-10-22; a raised alcove with a hatch and chute in the back wall before).
do
	local ws = fresh(plot, "Workshop")
	local shell = Instance.new("Model")
	shell.Name = "Shell"
	local roof = Instance.new("Model")
	roof.Name = "Roof"
	roof.Parent = shell
	local WG = 13 + LIFT
	local SIDE = { PZ, 38.4, 46.8, 55.2, 63.6, 72, BZ - T / 2 }
	walls(shell, {
		G = WG, doorH = 8 + LIFT,
		sides = { [-1] = SIDE, [1] = SIDE },
		sideKinds = { [-1] = { [2] = "window", [4] = "window", [6] = "window" }, [1] = { [2] = "window", [4] = "window" } },
		runs = {
			{ at = PZ, out = -1, list = CROSS_POSTS, kinds = { [3] = "door" } },
			{ at = BZ - T / 2, out = 1, list = { -XS, -15.85, -7.9, 0, 7.9, 15.85, XS }, kinds = { [2] = "window", [3] = "window", [4] = "window" } },
		},
	})
	doorDressing(shell, PZ)

	box(ws, "Floor", -23.55, 23.55, 0, 0.2, PZ + 0.2, BZ - T + 0.05, C.stoneLt, M.Slate, { solid = true })

	local yr, zr = mainRoof(roof, { front = PZ, D = BZ, H = WG, pitch = 22, ovF = 0.3, ovB = 2.0, ovS = 1.5, th = 0.7, ridgeH = 1.2, roofCol = C.tileDk, gableCol = C.plaster })
	-- smoke vent over the furnaces (local x -6 … 10): louvred box on the ridge with its own small roof
	local vx, vl = 2, 16
	part(roof, "VentBox", Vector3.new(vl, 2.6, 4.6), L(vx, yr + 1.0, zr), C.interior)
	for s = -1, 1, 2 do
		for _, ly in { 0.35, 1.0, 1.65 } do
			part(roof, "Louvre", Vector3.new(vl - 0.4, 0.2, 0.14), L(vx, yr + ly, zr + s * 2.35), C.timber, M.Wood)
		end
		part(roof, "VentPost", Vector3.new(0.6, 2.6, 0.5), L(vx + s * (vl / 2 - 0.25), yr + 1.0, zr - 2.3), C.timberDk, M.Wood) -- 0.05 past the box ends
		part(roof, "VentPost", Vector3.new(0.6, 2.6, 0.5), L(vx + s * (vl / 2 - 0.25), yr + 1.0, zr + 2.3), C.timberDk, M.Wood)
	end
	local yE, rise = yr + 1.9, 3.2 * math.tan(rad(22)) -- the vent roof's underside meets the box top 0.05 inside it
	slope(roof, "VentRoof", vx, vl + 1.2, zr - 3.2, yE, zr, yE + rise, 0.5, C.tileDk, M.ClayRoofTiles)
	slope(roof, "VentRoof", vx, vl + 1.28, zr + 3.2, yE, zr, yE + rise, 0.5, C.tileDk, M.ClayRoofTiles)
	part(roof, "VentRidge", Vector3.new(vl + 1.5, 0.6, 0.9), L(vx, yE + rise + 0.55, zr), C.tileDk, M.ClayRoofTiles)

	local zone = part(ws, "InsideZone", Vector3.new(46.8, 14 + LIFT, BZ - T - PZ - 0.35 - 0.1), L(0, 7.2 + LIFT / 2, (PZ + 0.35 + BZ - T - 0.1) / 2), C.plaster)
	zone.Transparency = 1
	shell.Parent = ws
	CS:AddTag(ws, "HidesRoof")
	ws.Parent = plot
end

-- ---------------------------------------------------------------- street pieces both shops share
do
	-- stone slab over the water channel and potted plants either side of the door
	local yard = plot.Yard
	local f = fresh(yard, "ShopFront")
	part(f, "Bridge", Vector3.new(6, 0.14, 2.3), L(0, 0.57, -7), C.stoneLt, M.Slate, { solid = true })
	for _, x in { -15.7, 15.7 } do
		cyl(f, "Pot", 1.1, 1.2, L(x, 0.85, -0.8), C.pot)
		ball(f, "Plant", 1.7, L(x, 1.95, -0.8), Color3.fromRGB(78, 120, 58), M.Grass)
	end
	f.Parent = yard
end

local n = 0
for _, m in { shops.Starter.Shell, shops.Upgraded.Shell, plot.Workshop } do
	for _, d in m:GetDescendants() do if d:IsA("BasePart") then n += 1 end end
end
return ("Shop and workshop built: %d parts"):format(n)

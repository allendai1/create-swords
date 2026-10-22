-- build_town.luau: the redesigned town street for Create Swords!, built beside the current street to compare (2026-10-22).
-- Allen: "Can you look at Town Street Redesign References for re-designing our map? Can you build it parallel to our
-- existing map so I can compare as well." Brief and images: vault Art/Town Street Redesign References and
-- References/Town Street Redesign/: a broader paved street, a market widening at the middle lots, two staggered side
-- lanes, the town gate west and the shrine east, six identical lots for the real plot template.
-- Run in Studio (Edit) through MCP execute_luau. Rebuilds Workspace.TownRedesign (an earlier build moves to
-- ServerStorage.Legacy); Workspace.Village is not touched and no script reads TownRedesign. Same SEED = same town.
-- The townhouse kit (part … widths) is build_street.luau's, with two changes for calmer fronts (Allen 2026-10-22, "try
-- that out", after Claude found the fronts busier than the references): spec() takes an optional style, and widths()
-- makes wider houses (about 22…34 instead of 16…26). A rafter that would sit flush with a beam end also moves 0.05.
-- ponytail: the kit lives in both builders until Allen picks a street; then delete the builder he drops.
--
-- Plan, in the north frame (x along the street, west −; the north side at −z; "depth" = distance from the street centre):
--   main-street fronts at depth 36 (72 apart; the current street is 44). Lot 2 and its neighbours stand SET 20 further
--   back (112 apart): the market widening, with stalls in front of the townhouses and a tree at the step.
--   north, west to east: houses | lot N1 | houses | lane | houses | lot N2 | houses ‖ step | houses | lot N3 | houses
--   (x −280…280). The south side is the same plan turned 180° about ORIGIN: its lane is east, its lots run S1…S3 west to
--   east, so N2 and S2 face each other across the market.
--   Every front has the current street's cross-section (walkway 1.5 under the façade to 6 out, water channel 6…8 out), so
--   a plot's shop front, bridge and CustomerSpawn fit as they do on the current street.
--   Lanes are 24 between the fronts of their houses, with the same walkway and channel, and end at depth 150 at a house
--   that closes the view. Town gate at x −300 (32-wide opening, walls out to the bounds); plaza, torii, shrine x 300…356.
-- Ground tops: road 0.2, plaza 0.25, water 0.26, walkway 0.3 (lanes 0.34), curbs 0.5 (lanes 0.54). Same-kind ground parts
-- never overlap; where a lane crosses a main front, the lane's strips sit 0.04 higher.
-- House parts never share a plane with a neighbour: widths are w - 0.04 and neighbouring heights and pitches differ.

local SEED = 22
local LIFT = 2.5 -- ground storeys as tall as the current street's (openings top out at OT 9.7)
local OT = 7.2 + LIFT

local SS = game:GetService("ServerStorage")
local M = Enum.Material
local rad = math.rad
local rng = Random.new(SEED)
local function r(a, b) return a + (b - a) * rng:NextNumber() end
local function pick(t) return t[rng:NextInteger(1, #t)] end
local function chance(p) return rng:NextNumber() < p end

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
	rust = Color3.fromRGB(128, 66, 50),
	copper = Color3.fromRGB(86, 132, 114),
	stone = Color3.fromRGB(122, 118, 110),
	stoneLt = Color3.fromRGB(168, 162, 152),
	walk = Color3.fromRGB(136, 130, 122),
	road = Color3.fromRGB(164, 156, 144),
	water = Color3.fromRGB(62, 92, 96),
	indigo = Color3.fromRGB(38, 54, 96),
	brown = Color3.fromRGB(116, 70, 42),
	norenW = Color3.fromRGB(222, 216, 198),
	red = Color3.fromRGB(190, 52, 40),
	paper = Color3.fromRGB(240, 226, 196),
	black = Color3.fromRGB(24, 22, 22),
	vermilion = Color3.fromRGB(204, 72, 42),
	interior = Color3.fromRGB(30, 22, 18),
	pot = Color3.fromRGB(160, 92, 62),
	pipe = Color3.fromRGB(150, 94, 60),
	straw = Color3.fromRGB(200, 174, 112),
}
local GOODS = { Color3.fromRGB(214, 196, 150), C.red, C.plaster, Color3.fromRGB(120, 92, 60), Color3.fromRGB(70, 90, 120) }
local PLANT = { Color3.fromRGB(78, 120, 58), Color3.fromRGB(96, 140, 64), Color3.fromRGB(60, 100, 52) }
local FLOWERS = { Color3.fromRGB(236, 196, 60), Color3.fromRGB(214, 72, 64), C.plaster, Color3.fromRGB(200, 110, 170) }
local SIGNS = { "茶屋", "酒", "宿", "米", "菓子", "薬", "呉服", "蕎麦", "味噌", "豆腐", "団子", "刃物", "油", "紙", "染物", "醤油", "漬物", "筆", "煎餅", "鰻" }
local BIG = { "呉服", "酒造", "茶舗", "米穀", "金物", "醤油" }
local STYLES = { "takayama", "takayama", "takayama", "kura", "tsumago", "tsumago", "gable", "low" }

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
	if o.refl then p.Reflectance = o.refl end
	p.Parent = parent
	return p
end
local UP = CFrame.Angles(0, 0, math.pi / 2)
local function cyl(parent, name, h, d, cf, col, mat, o)
	o = o or {}
	o.shape = Enum.PartType.Cylinder
	return part(parent, name, Vector3.new(h, d, d), cf * UP, col, mat, o)
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
local function label(p, text, col, face, vertical)
	local g = Instance.new("SurfaceGui")
	g.Face = face or Enum.NormalId.Front
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

-- One townhouse. hcf: ground at the façade line, centre of the frontage, LookVector toward the street
-- (local z = 0 is the façade line, +z goes into the house).
local function house(parent, name, hcf, w, sp)
	local m = Instance.new("Model")
	m.Name = name
	local function L(x, y, z) return hcf * CFrame.new(x, y, z) end
	local function P(n, size, cf, col, mat, o) return part(m, n, size, cf, col, mat, o) end
	local W = w - 0.04
	local hw = W / 2
	local WD = W - 0.1 -- posts stop 0.05 short of the side walls; beams and rails end inside the posts (WD - 0.1)
	local hd = WD / 2
	local G, U, D = sp.G, sp.U, sp.D
	local H = G + U
	local F0, F1 = 1.5, sp.F1
	local postCol = sp.postCol or C.timberDk
	-- neighbours alternate sp.alt (0 / 1, closed fronts 2) so ridges and fascias of equal-depth roofs never share a plane
	local alt = 0.03 * (sp.alt or 0)

	P("Ground", Vector3.new(W, G, D - F0), L(0, G / 2, (F0 + D) / 2), sp.groundCol or C.timberDk, M.Wood, { solid = true })
	if U > 0 then
		P("Upper", Vector3.new(W, U, D - F1), L(0, G + U / 2, (F1 + D) / 2), sp.upperCol, sp.upperMat, { solid = true })
	end

	-- ground floor: posts, then one bay between each pair
	local nb = math.max(1, math.floor(W / 4.2 + 0.5))
	local px = {}
	for i = 0, nb do
		px[i + 1] = math.clamp(-hw + i * W / nb, -hd + 0.45, hd - 0.45)
		P("Post", Vector3.new(0.9, G - 0.3, 0.9), L(px[i + 1], 0.3 + (G - 0.3) / 2, F0 - 0.45), postCol, M.Wood, { solid = true })
	end
	local door = sp.doorBay or rng:NextInteger(1, nb)
	local doorX, doorPost
	for i = 1, nb do
		local x0, x1 = px[i] + 0.45, px[i + 1] - 0.45
		local cx, cw = (x0 + x1) / 2, x1 - x0
		local kind = pick(sp.bays)
		if i == door then
			kind, doorX, doorPost = "door", cx, px[i]
		end
		if kind == "lattice" then
			P("Kick", Vector3.new(cw, 1.2, 0.35), L(cx, 0.9, F0 - 0.25), C.timberDk, M.Wood)
			P("Rail", Vector3.new(cw, 0.4, 0.35), L(cx, OT + 0.2, F0 - 0.25), C.timberDk, M.Wood)
			P("Shoji", Vector3.new(cw, OT - 1.5, 0.1), L(cx, (1.5 + OT) / 2, F0 - 0.1), (sp.paper or chance(0.4)) and C.paper or C.interior)
			local n = math.max(2, math.floor(cw / 0.55))
			for k = 1, n - 1 do
				P("Slat", Vector3.new(0.22, OT - 1.5, 0.3), L(x0 + k * cw / n, (1.5 + OT) / 2, F0 - 0.35), C.slat, M.Wood)
			end
		elseif kind == "door" then
			P("Doorway", Vector3.new(cw, OT - 0.3, 0.1), L(cx, (0.3 + OT) / 2, F0 - 0.1), C.interior)
			local nw = cw / 3
			for k = 0, 2 do
				local strip = P("Noren", Vector3.new(nw - 0.08, 2.7, 0.08), L(x0 + nw * (k + 0.5), OT - 1.35, F0 - 0.95), sp.noren, M.Fabric)
				if k == 1 and sp.sign then label(strip, utf8.char(utf8.codepoint(sp.sign, 1)), sp.noren == C.norenW and C.black or C.paper) end
			end
			P("NorenRod", Vector3.new(cw, 0.15, 0.15), L(cx, OT + 0.05, F0 - 0.95), C.timberDk, M.Wood)
		elseif kind == "open" then
			P("Interior", Vector3.new(cw, OT - 0.3, 0.1), L(cx, (0.3 + OT) / 2, F0 - 0.1), C.interior)
			P("Platform", Vector3.new(cw - 0.08, 1.4, 1.6), L(cx, 1.0, F0 - 0.8), C.cedar, M.WoodPlanks, { solid = true })
			local gx = x0 + 0.4
			while gx < x1 - 1.4 do
				local s = r(0.7, 1.1)
				if chance(0.5) then
					cyl(m, "Barrel", s * 1.2, s, L(gx + s / 2, 1.7 + s * 0.6, F0 - 0.8), pick(GOODS))
				else
					P("Goods", Vector3.new(s, s * 0.8, s), L(gx + s / 2, 1.7 + s * 0.4, F0 - 0.8) * CFrame.Angles(0, r(-0.3, 0.3), 0), pick(GOODS), M.Fabric)
				end
				gx += s + 0.3
			end
		else
			P("Shutter", Vector3.new(cw, OT - 0.6, 0.3), L(cx, OT / 2, F0 - 0.2), sp.shutterCol or C.cedar, M.Wood)
			for k = 1, 2 do
				P("Batten", Vector3.new(0.18, OT - 0.7, 0.14), L(x0 + k * cw / 3, OT / 2, F0 - 0.41), C.timber, M.Wood) -- ends inside the shutter's
			end
		end
	end
	P("Beam", Vector3.new(WD - 0.1, 0.8, 0.7), L(0, OT + 0.75, F0 - 0.3), postCol, M.Wood)
	if G - (OT + 1.15) > 0.4 then
		P("Transom", Vector3.new(WD - 0.3, G - OT - 1.25, 0.1), L(0, (OT + 1.15 + G - 0.1) / 2, F0 - 0.1), sp.transomCol or C.cream, M.Plaster)
	end

	-- pent roof over the walkway
	local zLo, yLo = -4.2, G - 0.2
	if sp.pent then
		local pp = rad(sp.pentPitch)
		local t = math.tan(pp)
		local zHi = F1 + 0.3
		local yHi = yLo + (zHi - zLo) * t
		local nrm = Vector3.new(0, math.cos(pp), -math.sin(pp))
		local c = Vector3.new(0, (yLo + yHi) / 2, (zLo + zHi) / 2) + nrm * 0.2
		P("PentRoof", Vector3.new(WD - 0.18, 0.5, (zHi - zLo) / math.cos(pp)), L(c.X, c.Y, c.Z) * CFrame.Angles(-pp, 0, 0), sp.roofCol, sp.roofMat)
		P("PentFascia", Vector3.new(WD - 0.26, 0.55, 0.25), L(0, yLo - 0.05, zLo + 0.1), C.timberDk, M.Wood)
		for i = 1, #px do
			P("BeamEnd", Vector3.new(0.55, 0.65, F0 + 0.3 - zLo - 0.6), L(px[i], G - 0.55, (F0 + 0.3 + zLo + 0.6) / 2), postCol, M.Wood)
		end
		if sp.rafters then
			local n = math.floor(WD / 1.1)
			for k = 1, n do
				local rx = -hd + (k - 0.5) * WD / n
				for _, x in px do -- a rafter's side flush with a beam end's flickers (seen at width 25): move it off
					if math.abs(math.abs(rx - x) - 0.15) < 0.02 then
						rx += 0.05
						break
					end
				end
				P("Rafter", Vector3.new(0.25, 0.25, 2.4), L(rx, yLo + 1.3 * t - 0.17, zLo + 1.3) * CFrame.Angles(-pp, 0, 0), C.timberDk, M.Wood)
			end
		end
		if chance(0.45) then
			part(m, "Gutter", Vector3.new(WD, 0.35, 0.35), L(0, yLo - 0.45, zLo + 0.05), C.pipe, M.Metal, { shape = Enum.PartType.Cylinder })
			local gx = (chance(0.5) and 1 or -1) * (hd - 0.5)
			cyl(m, "Downpipe", yLo - 0.75, 0.3, L(gx, 0.3 + (yLo - 0.75) / 2, zLo + 0.05), C.pipe, M.Metal)
		end
	end

	-- upper floor
	if U > 0 and (sp.style == "takayama" or sp.style == "gable") then
		local upx = {}
		local nu = math.max(1, math.floor(W / 3.6 + 0.5))
		for i = 0, nu do
			upx[i + 1] = math.clamp(-hw + i * W / nu, -hd + 0.3, hd - 0.3)
			P("UPost", Vector3.new(0.6, U - 0.14, 0.3), L(upx[i + 1], G + 0.04 + (U - 0.14) / 2, F1 - 0.1), postCol, M.Wood)
		end
		P("UTop", Vector3.new(WD - 0.1, 0.7, 0.36), L(0, H - 0.39, F1 - 0.15), postCol, M.Wood)
		P("USill", Vector3.new(WD - 0.1, 0.35, 0.36), L(0, G + 2.0, F1 - 0.15), postCol, M.Wood)
		local wb = math.min(G + 5.4, H - 1.0) - (G + 2.2)
		local winCol = chance(0.5) and C.paper or C.interior
		for i = 1, nu do
			if sp.style == "gable" and nu > 2 and (i == 1 or i == nu) then continue end
			local x0, x1 = upx[i] + 0.3, upx[i + 1] - 0.3
			local cw = x1 - x0
			P("UBack", Vector3.new(cw, wb, 0.1), L((x0 + x1) / 2, G + 2.2 + wb / 2, F1 - 0.12), winCol)
			local n = math.max(2, math.floor(cw / 0.42))
			for k = 1, n - 1 do
				P("USlat", Vector3.new(0.16, wb, 0.15), L(x0 + k * cw / n, G + 2.2 + wb / 2, F1 - 0.3), C.slat, M.Wood)
			end
		end
	elseif U > 0 and sp.style == "kura" then
		local nwin = W / 4 > 5.25 and 3 or 2 -- shutters reach 2.6 either side of a window
		local wy = H - 3.4
		for i = 1, nwin do
			local wx = -hw + i * W / (nwin + 1)
			P("WinSurround", Vector3.new(2.8, 3.0, 0.35), L(wx, wy, F1 - 0.175), sp.upperCol, M.Plaster)
			P("Window", Vector3.new(2.0, 2.2, 0.1), L(wx, wy, F1 - 0.34), C.interior)
			for sgn = -1, 1, 2 do
				P("WinShutter", Vector3.new(1.1, 2.6, 0.45), L(wx + sgn * 2.05, wy, F1 - 0.4), sp.upperCol, M.Plaster)
			end
		end
		P("Hachimaki", Vector3.new(WD - 0.1, 1.0, 0.6), L(0, H - 0.54, F1 - 0.3), sp.upperCol, M.Plaster)
		if sp.bigSign then
			local b = P("Kanban", Vector3.new(math.min(W - 3, 12), 2.0, 0.35), L(0, G + 2.5, F1 - 1.3), C.timberDk, M.Wood)
			label(b, sp.bigSign, C.paper)
		end
	elseif U > 0 and sp.style == "tsumago" then
		local dz0 = F1 - 1.6
		P("Deck", Vector3.new(WD, 0.4, 1.6), L(0, G + 0.2, F1 - 0.8), C.timber, M.WoodPlanks)
		for i = 1, #px do
			P("Joist", Vector3.new(0.55, 0.7, F0 + 0.3 - dz0), L(px[i], G - 0.39, (F0 + 0.3 + dz0) / 2), postCol, M.Wood)
		end
		P("Amado", Vector3.new(WD, U - 1.2, 0.15), L(0, G + 0.4 + (U - 1.2) / 2, F1 - 0.12), sp.shutterCol or C.cedar, M.Wood)
		P("UTop", Vector3.new(WD - 0.1, 0.8, 0.35), L(0, H - 0.44, F1 - 0.15), postCol, M.Wood)
		local nbat = math.max(2, math.floor(W / 1.8))
		for k = 1, nbat - 1 do
			P("Batten", Vector3.new(0.14, U - 1.3, 0.12), L(-hd + k * WD / nbat, G + 0.4 + (U - 1.2) / 2, F1 - 0.25), C.timber, M.Wood)
		end
		local rz = F1 - 1.45
		P("RailTop", Vector3.new(WD - 0.1, 0.25, 0.3), L(0, G + 3.1, rz), C.timber, M.Wood)
		P("RailMid", Vector3.new(WD - 0.1, 0.2, 0.25), L(0, G + 1.6, rz), C.timber, M.Wood)
		local nbal = math.floor(WD / 0.9)
		for k = 0, nbal do
			P("Baluster", Vector3.new(0.2, 2.7, 0.2), L(-hd + 0.1 + k * (WD - 0.2) / nbal, G + 1.75, rz), C.timber, M.Wood)
		end
	end

	-- main roof
	local front = U > 0 and F1 or F0
	local th = 0.6
	local p = rad(sp.pitch)
	local t, cs, sn = math.tan(p), math.cos(p), math.sin(p)
	local ovF, ovB, ovS = sp.ovF, 2.0, sp.ovS or 0.6
	local gCol, gMat = sp.gableCol or sp.upperCol or C.plaster, sp.upperMat or M.Plaster
	if sp.ridgeZ then
		local yr = H + hw * t
		local zf, zb = front - ovF, D + ovB
		local run = hw + ovS
		for sgn = -1, 1, 2 do
			local c = Vector3.new(sgn * run / 2, yr - run / 2 * t, (zf + zb) / 2) + Vector3.new(sgn * sn, cs, 0) * (th / 2 - 0.05)
			P("Roof", Vector3.new(run / cs, th, zb - zf + (sgn > 0 and 0.08 or 0)), L(c.X, c.Y, c.Z) * CFrame.Angles(0, 0, -sgn * p), sp.roofCol, sp.roofMat)
			for _, zg in { front + 0.3, D - 0.3 } do
				P("Gable", Vector3.new(0.5, yr - H, hd), L(sgn * hd / 2, H + (yr - H) / 2, zg) * CFrame.Angles(0, -sgn * math.pi / 2, 0), gCol, gMat, { wedge = true })
			end
		end
		P("Ridge", Vector3.new(1.2 + alt, sp.ridgeH, zb - zf + 0.2), L(0, yr + th + sp.ridgeH / 2 - 0.35, (zf + zb) / 2), C.tileDk, sp.roofMat)
		P("TieBeam", Vector3.new(WD - 0.1, 0.6, 0.4), L(0, H + 0.34, front + 0.05), postCol, M.Wood)
		P("KingPost", Vector3.new(0.5, yr - H - 0.6, 0.32), L(0, H + (yr - H) / 2 + 0.3, front + 0.05), postCol, M.Wood)
	else
		local zr = (front + D) / 2
		local yr = H + (zr - front) * t
		local zf, zb = front - ovF, D + ovB
		local xl = W + 2 * ovS
		local runF, runB = zr - zf, zb - zr
		local cF = Vector3.new(0, yr - runF / 2 * t, (zf + zr) / 2) + Vector3.new(0, cs, -sn) * (th / 2 - 0.05)
		P("Roof", Vector3.new(xl, th, runF / cs), L(cF.X, cF.Y, cF.Z) * CFrame.Angles(-p, 0, 0), sp.roofCol, sp.roofMat)
		local cB = Vector3.new(0, yr - runB / 2 * t, (zr + zb) / 2) + Vector3.new(0, cs, sn) * (th / 2 - 0.05)
		P("Roof", Vector3.new(xl + 0.08, th, runB / cs), L(cB.X, cB.Y, cB.Z) * CFrame.Angles(p, 0, 0), sp.roofCol, sp.roofMat)
		P("Ridge", Vector3.new(xl + 0.2, sp.ridgeH, 1.3 + alt), L(0, yr + th + sp.ridgeH / 2 - 0.35, zr), C.tileDk, sp.roofMat)
		if sp.oni then
			for sgn = -1, 1, 2 do
				P("Onigawara", Vector3.new(1.0, sp.ridgeH + 1.4, 2.0), L(sgn * (xl / 2 + 0.3), yr + th + (sp.ridgeH + 1.4) / 2 - 0.4, zr), C.tileDk, sp.roofMat)
			end
		end
		P("Fascia", Vector3.new(xl - 0.08, 0.5, 0.3), L(0, H - ovF * t - 0.1, zf + 0.1 + alt), C.timberDk, M.Wood)
		for sgn = -1, 1, 2 do
			P("Gable", Vector3.new(0.5, yr - H, zr - front), L(sgn * (hw - 0.3), H + (yr - H) / 2, (front + zr) / 2), gCol, gMat, { wedge = true })
			P("Gable", Vector3.new(0.5, yr - H, D - zr), L(sgn * (hw - 0.3), H + (yr - H) / 2, (zr + D) / 2) * CFrame.Angles(0, math.pi, 0), gCol, gMat, { wedge = true })
		end
	end

	-- street dressing
	if doorX and sp.lantern then
		local ly, lz = G - 1.6, -2.4
		if not sp.pent then ly, lz = (sp.balcony and G - 1.6 or G - 3.2), (sp.balcony and F1 - 0.9 or -0.9) end
		local lx = doorX + 1.6
		if sp.pent and sp.rafters then -- hang it in the gap between two rafters, its cord clear of them
			local step = WD / math.floor(WD / 1.1)
			lx = -hd + math.floor((lx + hd) / step + 0.5) * step
		end
		chochin(m, L(lx, ly, lz), sp.lanternCol)
	end
	if sp.sign and doorPost then
		local b = P("Signboard", Vector3.new(1.5, 4.4, 0.3), L(doorPost, OT - 2.3, F0 - 1.1), C.cedar, M.Wood)
		label(b, sp.sign, C.black, nil, true)
		if sp.sign == "酒" then ball(m, "Sugidama", 1.8, L(doorX - 1.2, G - 1.9, -2.2), Color3.fromRGB(104, 112, 60), M.Grass) end
	end
	for _ = 1, rng:NextInteger(0, 3) do
		local x = r(-hw + 1, hw - 1)
		if doorX and math.abs(x - doorX) < 2 then continue end
		cyl(m, "Pot", 1.1, 1.2, L(x, 0.85, -0.8), C.pot)
		ball(m, "Plant", 1.7, L(x, 1.95, -0.8), pick(PLANT), M.Grass)
		if chance(0.5) then
			for _ = 1, 3 do ball(m, "Flower", 0.55, L(x + r(-0.5, 0.5), 2.7 + r(0, 0.3), -0.8 + r(-0.5, 0.5)), pick(FLOWERS)) end
		end
	end
	if sp.bench then
		local bx = r(-hw + 3, hw - 3)
		P("Bench", Vector3.new(3.6, 0.3, 1.2), L(bx, 1.75, -0.9), C.cedar, M.WoodPlanks, { solid = true })
		for sgn = -1, 1, 2 do P("BenchLeg", Vector3.new(0.3, 1.3, 1.0), L(bx + sgn * 1.5, 0.95, -0.9), C.timber, M.Wood) end
	end
	if doorX then P("Bridge", Vector3.new(3.2, 0.14, 2.3), L(doorX, 0.57, -7), C.stoneLt, M.Slate, { solid = true }) end

	m.WorldPivot = hcf
	m.Parent = parent
	return m
end

local function spec(prevH, style)
	local st = style or pick(STYLES)
	local sp = {
		style = st, D = 24 + 2 * rng:NextInteger(0, 3), ridgeH = 0.9, ovS = 0.6,
		noren = pick({ C.indigo, C.indigo, C.brown, C.norenW }), lantern = chance(0.7),
		lanternCol = chance(0.6) and C.red or C.paper,
		roofCol = chance(0.5) and C.tile or C.tileDk, roofMat = M.ClayRoofTiles,
		sign = chance(0.6) and pick(SIGNS) or nil,
	}
	local Ur
	if st == "takayama" then
		sp.F1, sp.pent, sp.pentPitch, sp.rafters = 1.0, true, 20, true
		sp.upperCol, sp.upperMat = C.cream, M.Plaster
		sp.bays = { "lattice", "lattice", "lattice", "open", "shutter" }
		sp.pitch, sp.ovF, Ur = r(22, 26), 3.2, { 6.5, 7.5 }
	elseif st == "kura" then
		sp.F1, sp.pent, sp.pentPitch = 1.5, true, 22
		sp.upperCol, sp.upperMat = chance(0.5) and C.kuroPl or C.plaster, M.Plaster
		sp.transomCol = sp.upperCol
		sp.bays = { "open", "open", "lattice" }
		sp.pitch, sp.ovF, Ur = r(28, 31), 2.6, { 8.5, 8.5 }
		sp.ridgeH, sp.oni, sp.bigSign, sp.sign = 1.8, true, pick(BIG), nil
	elseif st == "tsumago" then
		sp.F1, sp.balcony, sp.bench = -1.0, true, chance(0.6)
		sp.upperCol, sp.upperMat, sp.transomCol = C.timber, M.Wood, C.timber
		sp.bays = { "shutter", "shutter", "lattice", "open" }
		sp.pitch, sp.ovF, Ur = r(19, 23), 3.0, { 6.0, 7.0 }
		if chance(0.3) then sp.roofCol, sp.roofMat = C.rust, M.Metal end
	elseif st == "gable" then
		sp.F1, sp.pent, sp.pentPitch, sp.ridgeZ = 1.0, true, 20, true
		sp.upperCol, sp.upperMat = C.plaster, M.Plaster
		sp.bays = { "lattice", "shutter", "open" }
		sp.pitch, sp.ovF, sp.ovS, Ur = r(30, 34), 1.6, 1.2, { 6.0, 7.0 }
	else -- low: single storey
		sp.F1, sp.transomCol = 1.5, C.timber
		sp.bays = { "lattice", "shutter", "shutter" }
		sp.pitch, sp.ovF, Ur = r(24, 28), 3.6, { 0, 0 }
	end
	repeat
		sp.G = 9.5 + LIFT + 0.5 * rng:NextInteger(0, 4)
		sp.U = Ur[1] + 0.5 * rng:NextInteger(0, math.floor((Ur[2] - Ur[1]) * 2))
	until math.abs(sp.G + sp.U - prevH) >= 0.75
	return sp
end

local function widths(total)
	local ws, left = {}, total
	while left > 0 do
		local w = pick({ 24, 26, 28, 30, 32, 34 })
		if left - w < 22 then w = left end
		if w > 40 then
			local a = math.floor(w / 2)
			table.insert(ws, a)
			left -= a
			w -= a
		end
		table.insert(ws, w)
		left -= w
	end
	return ws
end

-- ---------------------------------------------------------------- town plan
local HALF, SET = 36, 20
local LOT_W, LOT_D = 48.5, 96
local ORIGIN = CFrame.new(17.5, 0, -200) -- 354 south of the current street's centre, clear of the old courtyard bamboo
local NF, SF = ORIGIN, ORIGIN * CFrame.Angles(0, math.pi, 0) -- north and south frames
local STREET, EAST, WEST = CFrame.Angles(0, math.pi, 0), CFrame.Angles(0, -math.pi / 2, 0), CFrame.Angles(0, math.pi / 2, 0) -- facings in a frame
local LANE_W, LANE_E, LANE_END = -107, -83, 150 -- the lane's fronts (x) and the depth of the house closing it
local STEP = 80 -- the market widening runs from the lane to here
local GX, GH, PX, BZ = -300, 16, 300, 190 -- gate x, half its opening, plaza start, bounds' depth
local ROW = { -- x0, x1, lot number or "H" (houses), front depth
	{ -280, -204.25, "H", HALF },
	{ -204.25, -155.75, 1, HALF },
	{ -155.75, LANE_W, "H", HALF },
	{ LANE_E, -24.25, "H", HALF + SET },
	{ -24.25, 24.25, 2, HALF + SET },
	{ 24.25, STEP, "H", HALF + SET },
	{ STEP, 155.75, "H", HALF },
	{ 155.75, 204.25, 3, HALF },
	{ 204.25, 280, "H", HALF },
}
-- Lots without a closed shopfront. Comparison build: a preview plot on every lot (a full server). For a live street,
-- PlotService gives each claimed lot its plot and the others keep the closed front.
local TAKEN = { N1 = true, N2 = true, N3 = true, S1 = true, S2 = true, S3 = true }
local PREVIEW_PLOTS = true -- copies of Workspace.Plot as a new player first sees it, made inert (no prompts, tags, spawns or pads)

local function Wd(x, y, z) return ORIGIN * CFrame.new(x, y, z) end

-- ground rectangle in frame F: x0..x1, depth d0..d1
local function slab(parent, name, F, x0, x1, d0, d1, top, col, mat)
	return part(parent, name, Vector3.new(x1 - x0, top, d1 - d0), F * CFrame.new((x0 + x1) / 2, top / 2, -(d0 + d1) / 2), col, mat, { solid = true })
end

-- walkway, curbs and water channel along a front. fcf: on the façade line at the run's middle, LookVector toward the
-- street; the run is len long along its local x. lift raises walkway and curbs (lanes: 0.04 over the main fronts).
local function frontage(parent, fcf, len, lift)
	local function at(z, y) return fcf * CFrame.new(0, y, z) end
	part(parent, "Walkway", Vector3.new(len, 0.3 + lift, 7.5), at(-2.25, (0.3 + lift) / 2), C.walk, M.Slate, { solid = true })
	part(parent, "Curb", Vector3.new(len, 0.5 + lift, 0.5), at(-6.25, (0.5 + lift) / 2), C.stone, M.Slate, { solid = true })
	part(parent, "Water", Vector3.new(len, 0.26, 1.0), at(-7, 0.13), C.water, M.SmoothPlastic, { solid = true, refl = 0.12 })
	part(parent, "Curb", Vector3.new(len, 0.5 + lift, 0.5), at(-7.75, (0.5 + lift) / 2), C.stone, M.Slate, { solid = true })
end

-- plaster wall with a tile cap, at x = wx in frame F from depth d0 to d1
local function wall(parent, F, wx, d0, d1)
	local len = d1 - d0
	local function at(y) return F * CFrame.new(wx, y, -(d0 + d1) / 2) end
	part(parent, "WallBase", Vector3.new(1.6, 1.6, len), at(0.8), C.stone, M.Cobblestone, { solid = true })
	part(parent, "Wall", Vector3.new(1.1, 5.0, len), at(4.1), C.plaster, M.Plaster, { solid = true })
	part(parent, "WallCap", Vector3.new(2.2, 0.5, len + 0.6), at(6.85), C.tile, M.ClayRoofTiles)
	part(parent, "WallRidge", Vector3.new(0.7, 0.45, len + 0.7), at(7.25), C.tileDk, M.ClayRoofTiles)
end

-- a market stall: cf on the ground at its middle, LookVector toward its customers
local function stall(parent, cf)
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
	chochin(m, L(3.0, 5.6, -2.2), C.red)
	local gx = -3.1
	while gx < 2.4 do
		local s = r(0.8, 1.3)
		if chance(0.5) then
			cyl(m, "Barrel", s * 1.1, s, L(gx + s / 2, 2.6 + s * 0.55, r(-0.4, 0.4)), pick(GOODS))
		else
			part(m, "Goods", Vector3.new(s, s * 0.7, s), L(gx + s / 2, 2.6 + s * 0.35, r(-0.4, 0.4)) * CFrame.Angles(0, r(-0.3, 0.3), 0), pick(GOODS), M.Fabric)
		end
		gx += s + 0.35
	end
	m.WorldPivot = cf
	m.Parent = parent
end

-- standing lamp on a lot's front corner
local function lamp(parent, cf)
	part(parent, "LampFoot", Vector3.new(1.4, 0.6, 1.4), cf * CFrame.new(0, 0.5, 0), C.stone, M.Slate, { solid = true })
	part(parent, "LampPost", Vector3.new(0.6, 7.4, 0.6), cf * CFrame.new(0, 4.5, 0), C.timberDk, M.Wood, { solid = true })
	glow(part(parent, "Andon", Vector3.new(1.6, 2.2, 1.6), cf * CFrame.new(0, 9.3, 0), C.paper), 16)
	part(parent, "LampCap", Vector3.new(2.4, 0.4, 2.4), cf * CFrame.new(0, 10.6, 0), C.tileDk, M.ClayRoofTiles)
end

local function torii(parent, cf, k) -- the current street's torii, scaled by k from its base
	local function at(y, z) return cf * CFrame.new(0, 0.25 + (y - 0.25) * k, z * k) end
	for s = -1, 1, 2 do
		cyl(parent, "ToriiPillar", 14.5 * k, 1.5 * k, at(7.5, s * 7.5), C.vermilion, M.SmoothPlastic, { solid = true })
		cyl(parent, "ToriiFoot", 1.0 * k, 2.0 * k, at(0.75, s * 7.5), C.black)
	end
	part(parent, "Nuki", Vector3.new(0.8, 0.9, 19) * k, at(11.2, 0), C.vermilion)
	part(parent, "Kasagi", Vector3.new(1.3, 0.9, 21.5) * k, at(14.4, 0), C.vermilion)
	part(parent, "KasagiTop", Vector3.new(1.6, 0.7, 23) * k, at(15.15, 0), C.black)
	part(parent, "Gakuzuka", Vector3.new(0.6, 2.4, 0.9) * k, at(12.85, 0), C.vermilion)
end

-- ---------------------------------------------------------------- build
local old = workspace:FindFirstChild("TownRedesign")
if old then
	old.Name = "TownRedesign_before_" .. os.date("!%Y%m%d%H%M%S")
	old.Parent = SS:FindFirstChild("Legacy") or SS
end
local town = Instance.new("Model")
town.Name = "TownRedesign"
town.WorldPivot = ORIGIN
town.Parent = workspace
local function folder(name)
	local f = Instance.new("Folder")
	f.Name = name
	f.Parent = town
	return f
end
local Street, Rows, Lanes, Lots, Market, Trees, Landmarks = folder("Street"), folder("Rows"), folder("Lanes"), folder("Lots"), folder("Market"), folder("Trees"), folder("Landmarks")

-- no backyard tree over a lot or a lane's houses (frame x0, x1, depth d0, d1)
local KEEP = { { LANE_W - 34, LANE_E + 34, HALF, LANE_END + 30 } }
for _, it in ROW do
	if type(it[3]) == "number" then table.insert(KEEP, { it[1], it[2], it[4], it[4] + LOT_D }) end
end

local function placeModel(src, cf, scale, parent, groundY)
	local mdl = src:Clone()
	if scale and scale ~= 1 then mdl:ScaleTo(scale) end
	mdl:PivotTo(cf)
	local bcf, bs = mdl:GetBoundingBox()
	mdl:TranslateBy(Vector3.new(0, (groundY or 0) - (bcf.Y - bs.Y / 2), 0))
	mdl.Parent = parent
	return mdl
end
local TREES = { SS.Village3D.Pine1, SS.Village3D.Pine2, SS.Village3D.Pine1, SS.Village3D.Sakura1, SS.Village3D.Sakura2, SS.Village3D.Maple1, SS.Buildings3D.Bamboo1, SS.Buildings3D.Bamboo2, SS.Buildings3D.Bamboo3 }
local function grove(F, x0, x1, d0, d1, n, scale0, scale1)
	for _ = 1, n do
		local mdl = placeModel(pick(TREES), F * CFrame.new(r(x0, x1), 0, -r(d0, d1)) * CFrame.Angles(0, r(0, 2 * math.pi), 0), r(scale0, scale1), Trees)
		local cf, size = mdl:GetBoundingBox()
		local q = F:PointToObjectSpace(cf.Position)
		local reach = math.sqrt(size.X ^ 2 + size.Z ^ 2) / 2 + 1 -- the crown's diagonal: any turn
		for _, k in KEEP do
			if q.X + reach > k[1] and q.X - reach < k[2] and -q.Z + reach > k[3] and -q.Z - reach < k[4] then
				mdl:Destroy()
				break
			end
		end
	end
end

-- Styles: one per run of houses (a run is a segment between lots, lanes and steps: 2…3 houses), storehouses and
-- gable fronts at the corners, merchant kura round the market.
local CORNER, MAIN, MARKET, LANE = { "kura", "gable" }, { "takayama", "takayama", "tsumago" }, { "kura", "takayama" }, { "takayama", "tsumago", "low" }
local CORNERS = { [1] = { first = true }, [3] = { last = true }, [4] = { first = true }, [7] = { first = true }, [9] = { last = true } } -- ROW items: street ends, lane, step

local nH = 0
-- houses side by side from a to b, all in one style from run except corner houses (corners.first / .last: kura or
-- gable, 30 deep so a lane's houses start behind them); at(centre) gives the house's CFrame. Returns the last height.
local function houses(parent, tag, a, b, at, prevH, run, corners)
	local ws, c = widths(b - a), a
	local st = pick(run)
	for i, w in ws do
		local corner = (i == 1 and corners.first) or (i == #ws and corners.last)
		local sp = spec(prevH, corner and pick(CORNER) or st)
		if corner then sp.D = 30 end
		if sp.style ~= "kura" then -- plain townhouses: a sign or lantern now and then, so shops and stalls stand out
			if not chance(0.3) then sp.sign = nil end
			if not chance(0.4) then sp.lantern = false end
		end
		if sp.roofMat == M.Metal then sp.roofCol, sp.roofMat = C.tileDk, M.ClayRoofTiles end -- tile roofs only
		prevH = sp.G + sp.U
		nH += 1
		sp.alt = nH % 2
		house(parent, ("House%s%02d"):format(tag, nH), at(c + w / 2), w, sp)
		c += w
		task.wait()
	end
	return prevH
end

-- road paving: the generated flagstone MaterialVariant (MaterialService "TownFlagstone" on Pavement, StudsPerTile 24) when
-- the place has it, plain Pavement otherwise
local FLAGS = game:GetService("MaterialService"):FindFirstChild("TownFlagstone", true)
local function paving(p)
	if FLAGS then p.MaterialVariant, p.Color = FLAGS.Name, Color3.fromRGB(226, 220, 208) end
	return p
end

paving(part(Street, "Road", Vector3.new(PX - (GX - 30), 0.2, 2 * (HALF - 8)), Wd((PX + GX - 30) / 2, 0.1, 0), C.road, M.Pavement, { solid = true }))

for _, F in { NF, SF } do
	local tag = F == NF and "N" or "S"
	local prevH = 0
	for i, it in ROW do
		local x0, x1, kind, d = it[1], it[2], it[3], it[4]
		if kind == "H" then
			if i == 4 then prevH = 0 end -- across the lane
			prevH = houses(Rows, tag, x0, x1, function(x) return F * CFrame.new(x, 0, -d) * STREET end, prevH, (i == 4 or i == 6) and MARKET or MAIN, CORNERS[i] or {})
			grove(F, x0 + 5, x1 - 5, d + 34, d + 104, 3, 1.4, 2.0)
		else
			prevH = 0
			local name = tag .. (tag == "N" and kind or 4 - kind)
			local slot = part(Lots, "PlotSlot" .. name, Vector3.new(LOT_W, 1, LOT_D), F * CFrame.new((x0 + x1) / 2, 0.5, -(d + LOT_D / 2)) * STREET, C.plaster)
			slot.Transparency = 1
			slot:SetAttribute("Side", tag)
			-- walls between the lot and the neighbours' backyards, starting behind the house row (houses are ≤ 30 deep)
			wall(Lots, F, x0 - 1.4, d + 32, d + LOT_D)
			wall(Lots, F, x1 + 1.4, d + 32, d + LOT_D)
			for _, lx in { x0 + 2, x1 - 2 } do lamp(Street, F * CFrame.new(lx, 0, -(d - 11))) end -- on the road, clear of the shop door
			if not TAKEN[name] then
				local sp = spec(0)
				sp.doorBay, sp.bays, sp.lantern, sp.sign, sp.bigSign, sp.bench, sp.alt = 0, { "shutter" }, false, nil, nil, false, 2
				local m = house(Lots, "Closed" .. name, F * CFrame.new((x0 + x1) / 2, 0, -d) * STREET, LOT_W, sp)
				m:SetAttribute("Lot", slot.Name)
			end
		end
	end

	-- fronts: gate to the lane, the widening (lane to the step), step to the plaza
	for _, run in { { GX, LANE_W - 1.5, HALF }, { LANE_E + 1.5, STEP, HALF + SET }, { STEP, PX, HALF } } do
		frontage(Street, F * CFrame.new((run[1] + run[2]) / 2, 0, -run[3]) * STREET, run[2] - run[1], 0)
	end
	paving(slab(Street, "Market", F, LANE_E, STEP, HALF - 8, HALF + SET - 8, 0.2, C.road, M.Pavement))

	-- side lane: road, a front along each side, its houses (behind the 30-deep corner houses), the house closing it
	paving(slab(Lanes, "LaneRoad", F, LANE_W + 8, LANE_E - 8, HALF - 8, LANE_END, 0.2, C.road, M.Pavement))
	local z0, z1 = HALF - 8, LANE_END + 1.5
	frontage(Lanes, F * CFrame.new(LANE_W, 0, -(z0 + z1) / 2) * EAST, z1 - z0, 0.04)
	frontage(Lanes, F * CFrame.new(LANE_E, 0, -(z0 + z1) / 2) * WEST, z1 - z0, 0.04)
	houses(Lanes, tag, HALF + 32, LANE_END, function(z) return F * CFrame.new(LANE_W, 0, -z) * EAST end, 0, LANE, {})
	houses(Lanes, tag, HALF + SET + 32, LANE_END, function(z) return F * CFrame.new(LANE_E, 0, -z) * WEST end, 0, LANE, {})
	local sp = spec(0, pick(CORNER))
	sp.lantern, sp.alt = true, 2
	local laneEnd = house(Lanes, "LaneEnd" .. tag, F * CFrame.new((LANE_W + LANE_E) / 2, 0, -LANE_END) * STREET, LANE_E - LANE_W, sp)
	if laneEnd:FindFirstChild("Bridge") then laneEnd.Bridge:Destroy() end -- no channel runs across the lane's end
	slab(Lanes, "LaneEndWalk", F, LANE_W + 8, LANE_E - 8, LANE_END - 6, LANE_END + 1.5, 0.3, C.walk, M.Slate) -- between the side curbs

	-- market: stalls in front of the widening's townhouses (clear of lot 2's door and lamps), a sakura at the step
	for _, x in { -66, -46, 38, 54 } do stall(Market, F * CFrame.new(x, 0, -(HALF + 4)) * STREET) end
	cyl(Market, "Planter", 0.9, 7, F * CFrame.new(STEP - 10, 0.65, -(HALF + 4)), C.stone, M.Cobblestone, { solid = true })
	cyl(Market, "Soil", 0.1, 6.4, F * CFrame.new(STEP - 10, 1.15, -(HALF + 4)), Color3.fromRGB(70, 52, 38), M.Ground)
	placeModel(SS.Village3D.Sakura2, F * CFrame.new(STEP - 10, 0, -(HALF + 4)), 1.5, Trees, 1.1)

	-- outside the gate, and between the gate and the first houses
	local m = tag == "N" and 1 or -1 -- frame x of a west-east offset
	wall(Landmarks, F, m * GX, GH + 1, BZ)
	grove(F, m * (GX - 26), m * (GX - 6), HALF + 4, BZ - 8, 5, 1.5, 2.1)
	grove(F, m * (GX + 6), m * -284, HALF + 34, BZ - 8, 3, 1.5, 2.1)
end

-- west: town gate (刀鍛冶の里, "swordsmith village")
for s = -1, 1, 2 do
	part(Landmarks, "GateFoot", Vector3.new(3, 1.0, 3), Wd(GX, 0.7, s * GH), C.stone, M.Slate, { solid = true })
	part(Landmarks, "GatePost", Vector3.new(2, 17.6, 2), Wd(GX, 10.0, s * GH), C.timberDk, M.Wood, { solid = true })
end
part(Landmarks, "GateBeam", Vector3.new(1.4, 1.2, 2 * GH - 1.9), Wd(GX, 13.5, 0), C.timberDk, M.Wood)
part(Landmarks, "GateLintel", Vector3.new(1.8, 1.6, 2 * GH + 6), Wd(GX, 18.2, 0), C.timberDk, M.Wood)
local gateSign = part(Landmarks, "GateSign", Vector3.new(10, 2.8, 0.4), Wd(GX, 15.7, 0) * CFrame.Angles(0, math.pi / 2, 0), C.timberDk, M.Wood)
label(gateSign, "刀鍛冶の里", C.paper, Enum.NormalId.Front)
label(gateSign, "刀鍛冶の里", C.paper, Enum.NormalId.Back)
do
	local gp, run, yb = rad(28), 3.4, 19.0
	for sgn = -1, 1, 2 do
		local c = Vector3.new(GX + sgn * run / 2, yb + run / 2 * math.tan(gp), 0) + Vector3.new(sgn * math.sin(gp), math.cos(gp), 0) * 0.25
		part(Landmarks, "GateRoof", Vector3.new(run / math.cos(gp), 0.6, 2 * GH + (sgn > 0 and 7.08 or 7)), ORIGIN * CFrame.new(c) * CFrame.Angles(0, 0, -sgn * gp), C.tileDk, M.ClayRoofTiles)
	end
	part(Landmarks, "GateRidge", Vector3.new(1.1, 0.7, 2 * GH + 7.4), Wd(GX, yb + run * math.tan(gp) + 0.5, 0), C.tileDk, M.ClayRoofTiles)
end
chochin(Landmarks, Wd(GX, 11.4, 0), C.red)

-- east: plaza, torii, stone lanterns and the shrine closing the street
part(Landmarks, "Plaza", Vector3.new(56, 0.25, 2 * HALF + 16), Wd(PX + 28, 0.125, 0), C.stoneLt, M.Cobblestone, { solid = true })
torii(Landmarks, Wd(PX + 10, 0, 0), 1.35)
for s = -1, 1, 2 do
	placeModel(SS.Buildings3D.StoneLantern, Wd(PX + 18, 0, s * 8), 1.6, Landmarks, 0.25)
	placeModel(SS.Buildings3D.StoneLantern, Wd(PX + 26, 0, s * 8), 1.6, Landmarks, 0.25)
	placeModel(s < 0 and SS.Village3D.Sakura1 or SS.Village3D.Maple1, Wd(PX + 44, 0, s * (HALF + 2)), 1.9, Trees, 0.25)
	placeModel(SS.Village3D.Pine2, Wd(PX + 6, 0, s * (HALF + 5)), 1.6, Trees, 0.25)
end
part(Landmarks, "ShrineBase", Vector3.new(24, 1.6, 26), Wd(PX + 39, 0.8, 0), C.stone, M.Cobblestone, { solid = true })
part(Landmarks, "ShrineStep", Vector3.new(1.5, 0.6, 10), Wd(PX + 24.75, 0.3, 0), C.stone, M.Cobblestone, { solid = true })
part(Landmarks, "ShrineStep", Vector3.new(1.5, 1.1, 10), Wd(PX + 26.25, 0.55, 0), C.stone, M.Cobblestone, { solid = true })
do
	local hcf = Wd(PX + 29, 1.6, 0) * CFrame.Angles(0, math.pi / 2, 0)
	house(Landmarks, "Shrine", hcf, 20, {
		style = "shrine", G = 13, U = 0, D = 17, F1 = 1.5, pitch = 32, ovF = 3.8, ovS = 1.8, ridgeH = 1.6,
		roofCol = C.copper, roofMat = M.Metal, postCol = C.vermilion, groundCol = C.plaster, transomCol = C.plaster,
		bays = { "lattice" }, paper = true, doorBay = 0,
	})
	part(Landmarks, "Shimenawa", Vector3.new(16, 0.9, 0.9), hcf * CFrame.new(0, 9.5, -0.3), C.straw, M.Fabric, { shape = Enum.PartType.Cylinder })
	for _, sx in { -4, 0, 4 } do part(Landmarks, "Shide", Vector3.new(0.5, 1.2, 0.05), hcf * CFrame.new(sx, 8.5, -0.8), C.plaster) end
	part(Landmarks, "OfferingBox", Vector3.new(4, 1.8, 1.6), hcf * CFrame.new(0, 0.9, -1.6), C.cedar, M.WoodPlanks, { solid = true })
end

-- invisible walls round the town (only matters if it becomes the live street)
for _, b in { { (GX - 30 + PX + 60) / 2, BZ, PX + 60 - (GX - 30), 2 }, { (GX - 30 + PX + 60) / 2, -BZ, PX + 60 - (GX - 30), 2 }, { GX - 30, 0, 2, 2 * BZ }, { PX + 60, 0, 2, 2 * BZ } } do
	local wb = part(town, "Bound", Vector3.new(b[3], 80, b[4]), Wd(b[1], 40, b[2]), C.plaster, nil, { solid = true })
	wb.Transparency = 1
end

-- preview plots: what a new player first sees on each taken lot, with nothing a script could pick up
local nP = 0
if PREVIEW_PLOTS and workspace:FindFirstChild("Plot") then
	local Previews = folder("PlotPreviews")
	for _, slot in Lots:GetChildren() do
		local lot = slot.Name:match("^PlotSlot(%u%d)$")
		if not lot or not TAKEN[lot] then continue end
		local p = workspace.Plot:Clone()
		for _, d in p:GetDescendants() do -- locked upgrades (the Upgraded Store, Furnace 2, extra racks and ore slots)
			if d.Parent and d:HasTag("TycoonItem") and d:GetAttribute("Upgrade") then d:Destroy() end
		end
		for _, n in { "Pads", "PlayerSpawn", "CustomerSpawn" } do
			local c = p:FindFirstChild(n)
			if c then c:Destroy() end
		end
		for _, d in p:GetDescendants() do
			if d:IsA("ProximityPrompt") or d:IsA("ClickDetector") or d:IsA("SpawnLocation") then
				d:Destroy()
			elseif d.Parent then
				for _, t in d:GetTags() do d:RemoveTag(t) end
			end
		end
		for _, t in p:GetTags() do p:RemoveTag(t) end
		for k in p:GetAttributes() do p:SetAttribute(k, nil) end
		p.Name = "Preview_" .. lot
		p:PivotTo(slot.CFrame)
		p.Parent = Previews
		nP += 1
		task.wait()
	end
end

local n = 0
for _, d in town:GetDescendants() do if d:IsA("BasePart") then n += 1 end end
return ("TownRedesign built: %d houses, %d preview plots, %d parts"):format(nH, nP, n)

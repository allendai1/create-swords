-- build_street.luau: the Japanese town street map for Create Swords! (2026-10-21).
-- Allen: "It's a street in a Japanese town. Note the architecture and the design." References in
-- References/Japanese Village/ (Kawagoe kura row, Takayama Sanmachi, Tsumago-juku, Kanazawa chaya street).
-- Run in Studio (Edit) through MCP execute_luau. Rebuilds Workspace.Village; an earlier build moves to
-- ServerStorage.Legacy. Same SEED = same street.
--
-- Local frame: ORIGIN is the street centre, the street runs along X, façades at z = ±16.
--   road 16 wide (|z| < 8), gutters with water (8..10), walkways (10..17.5).
--   each side, west to east: houses 70 | lot 140 | houses 70 | lot 140 | houses 70 | lot 140 | houses 70 (x -350..350)
--   west gate zone x -395..-350, shrine plaza x 350..395. Lots are 110 deep (|z| 16..126).
--   Lots.PlotSlot<N|S><1..3>: invisible 140 x 110 markers, centre of the lot, LookVector toward the street.
--   Mountains: the Blender CliffRing (ServerStorage.Village3D) stretched in X so its inner face is x ±395, z ±130.
-- House parts never share a plane with a neighbour: widths are w - 0.04 and neighbouring heights and pitches differ.

local ORIGIN = CFrame.new(4, 0, -560)
local SEED = 21
local HALF, LOT_W, LOT_D, SEG_W = 16, 140, 110, 70
local ROW = { "H", "L", "H", "L", "H", "L", "H" }

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
			P("Rail", Vector3.new(cw, 0.4, 0.35), L(cx, 7.4, F0 - 0.25), C.timberDk, M.Wood)
			P("Shoji", Vector3.new(cw, 5.7, 0.1), L(cx, 4.35, F0 - 0.1), (sp.paper or chance(0.4)) and C.paper or C.interior)
			local n = math.max(2, math.floor(cw / 0.55))
			for k = 1, n - 1 do
				P("Slat", Vector3.new(0.22, 5.7, 0.3), L(x0 + k * cw / n, 4.35, F0 - 0.35), C.slat, M.Wood)
			end
		elseif kind == "door" then
			P("Doorway", Vector3.new(cw, 6.9, 0.1), L(cx, 3.75, F0 - 0.1), C.interior)
			local nw = cw / 3
			for k = 0, 2 do
				local strip = P("Noren", Vector3.new(nw - 0.08, 2.7, 0.08), L(x0 + nw * (k + 0.5), 5.85, F0 - 0.95), sp.noren, M.Fabric)
				if k == 1 and sp.sign then label(strip, utf8.char(utf8.codepoint(sp.sign, 1)), sp.noren == C.norenW and C.black or C.paper) end
			end
			P("NorenRod", Vector3.new(cw, 0.15, 0.15), L(cx, 7.25, F0 - 0.95), C.timberDk, M.Wood)
		elseif kind == "open" then
			P("Interior", Vector3.new(cw, 6.9, 0.1), L(cx, 3.75, F0 - 0.1), C.interior)
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
			P("Shutter", Vector3.new(cw, 6.6, 0.3), L(cx, 3.6, F0 - 0.2), sp.shutterCol or C.cedar, M.Wood)
			for k = 1, 2 do
				P("Batten", Vector3.new(0.18, 6.6, 0.14), L(x0 + k * cw / 3, 3.6, F0 - 0.41), C.timber, M.Wood)
			end
		end
	end
	P("Beam", Vector3.new(WD - 0.1, 0.8, 0.7), L(0, 7.95, F0 - 0.3), postCol, M.Wood)
	if G - 8.35 > 0.4 then
		P("Transom", Vector3.new(WD - 0.3, G - 8.45, 0.1), L(0, (8.35 + G - 0.1) / 2, F0 - 0.1), sp.transomCol or C.cream, M.Plaster)
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
				P("Rafter", Vector3.new(0.25, 0.25, 2.4), L(-hd + (k - 0.5) * WD / n, yLo + 1.3 * t - 0.17, zLo + 1.3) * CFrame.Angles(-pp, 0, 0), C.timberDk, M.Wood)
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
		local nwin = W >= 20 and 3 or 2
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
			P("Batten", Vector3.new(0.14, U - 1.2, 0.12), L(-hd + k * WD / nbat, G + 0.4 + (U - 1.2) / 2, F1 - 0.25), C.timber, M.Wood)
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
		P("Ridge", Vector3.new(1.2, sp.ridgeH, zb - zf + 0.2), L(0, yr + th + sp.ridgeH / 2 - 0.35, (zf + zb) / 2), C.tileDk, sp.roofMat)
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
		P("Ridge", Vector3.new(xl + 0.2, sp.ridgeH, 1.3), L(0, yr + th + sp.ridgeH / 2 - 0.35, zr), C.tileDk, sp.roofMat)
		if sp.oni then
			for sgn = -1, 1, 2 do
				P("Onigawara", Vector3.new(1.0, sp.ridgeH + 1.4, 2.0), L(sgn * (xl / 2 + 0.3), yr + th + (sp.ridgeH + 1.4) / 2 - 0.4, zr), C.tileDk, sp.roofMat)
			end
		end
		P("Fascia", Vector3.new(xl - 0.08, 0.5, 0.3), L(0, H - ovF * t - 0.1, zf + 0.1), C.timberDk, M.Wood)
		for sgn = -1, 1, 2 do
			P("Gable", Vector3.new(0.5, yr - H, zr - front), L(sgn * (hw - 0.3), H + (yr - H) / 2, (front + zr) / 2), gCol, gMat, { wedge = true })
			P("Gable", Vector3.new(0.5, yr - H, D - zr), L(sgn * (hw - 0.3), H + (yr - H) / 2, (zr + D) / 2) * CFrame.Angles(0, math.pi, 0), gCol, gMat, { wedge = true })
		end
	end

	-- street dressing
	if doorX and sp.lantern then
		local ly, lz = G - 1.6, -2.4
		if not sp.pent then ly, lz = (sp.balcony and G - 1.6 or G - 3.2), (sp.balcony and F1 - 0.9 or -0.9) end
		chochin(m, L(doorX + 1.6, ly, lz), sp.lanternCol)
	end
	if sp.sign and doorPost then
		local b = P("Signboard", Vector3.new(1.5, 4.4, 0.3), L(doorPost, 4.9, F0 - 1.1), C.cedar, M.Wood)
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

local function spec(prevH)
	local st = pick(STYLES)
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
		sp.G = 9.5 + 0.5 * rng:NextInteger(0, 4)
		sp.U = Ur[1] + 0.5 * rng:NextInteger(0, math.floor((Ur[2] - Ur[1]) * 2))
	until math.abs(sp.G + sp.U - prevH) >= 0.75
	return sp
end

local function widths(total)
	local ws, left = {}, total
	while left > 0 do
		local w = pick({ 16, 18, 20, 22, 24, 26 })
		if left - w < 16 then w = left end
		if w > 30 then
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

local function Wd(x, y, z) return ORIGIN * CFrame.new(x, y, z) end
local function facing(s) return s < 0 and CFrame.Angles(0, math.pi, 0) or CFrame.identity end

local function wall(parent, wx, s, d0, d1)
	local len, dm = d1 - d0, (d0 + d1) / 2
	part(parent, "WallBase", Vector3.new(1.6, 1.6, len), Wd(wx, 0.8, s * dm), C.stone, M.Cobblestone, { solid = true })
	part(parent, "Wall", Vector3.new(1.1, 5.0, len), Wd(wx, 4.1, s * dm), C.plaster, M.Plaster, { solid = true })
	part(parent, "WallCap", Vector3.new(2.2, 0.5, len + 0.6), Wd(wx, 6.85, s * dm), C.tile, M.ClayRoofTiles)
	part(parent, "WallRidge", Vector3.new(0.7, 0.45, len + 0.7), Wd(wx, 7.25, s * dm), C.tileDk, M.ClayRoofTiles)
end
local function andon(parent, cf)
	part(parent, "LampBase", Vector3.new(1.1, 0.6, 1.1), cf * CFrame.new(0, 0.3, 0), C.stone, M.Slate, { solid = true })
	part(parent, "LampPost", Vector3.new(0.45, 4.6, 0.45), cf * CFrame.new(0, 2.9, 0), C.timberDk, M.Wood, { solid = true })
	glow(part(parent, "Lamp", Vector3.new(1.2, 1.5, 1.2), cf * CFrame.new(0, 5.65, 0), C.paper), 16)
	part(parent, "LampCap", Vector3.new(1.6, 0.3, 1.6), cf * CFrame.new(0, 6.55, 0), C.timberDk, M.Wood)
end

-- ---------------------------------------------------------------- build
local old = workspace:FindFirstChild("Village")
if old then
	old.Name = "Village_before_" .. os.date("!%Y%m%d%H%M%S")
	old.Parent = SS:FindFirstChild("Legacy") or SS
end
local village = Instance.new("Model")
village.Name = "Village"
village.WorldPivot = ORIGIN
village.Parent = workspace
local function folder(name)
	local f = Instance.new("Folder")
	f.Name = name
	f.Parent = village
	return f
end
local Street, Rows, Lots, Props, Trees, Landmarks = folder("Street"), folder("Rows"), folder("Lots"), folder("Props"), folder("Trees"), folder("Landmarks")

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
local function grove(x0, x1, s, d0, d1, n, scale0, scale1)
	for _ = 1, n do
		placeModel(pick(TREES), Wd(r(x0, x1), 0, s * r(d0, d1)) * CFrame.Angles(0, r(0, 2 * math.pi), 0), r(scale0, scale1), Trees)
	end
end

-- street: road, gutters, walkways (ground layers: road 0.2, walkway 0.3, curbs 0.5, plaza 0.25)
local rx0, rx1 = -395, 350
local rl, rc = rx1 - rx0, (rx0 + rx1) / 2
part(Street, "Road", Vector3.new(rl, 0.2, 16), Wd(rc, 0.1, 0), C.road, M.Pavement, { solid = true })
for s = -1, 1, 2 do
	part(Street, "Curb", Vector3.new(rl, 0.5, 0.5), Wd(rc, 0.25, s * 8.25), C.stone, M.Slate, { solid = true })
	part(Street, "Water", Vector3.new(rl, 0.12, 1.0), Wd(rc, 0.06, s * 9.0), C.water, M.SmoothPlastic, { solid = true, refl = 0.12 })
	part(Street, "Curb", Vector3.new(rl, 0.5, 0.5), Wd(rc, 0.25, s * 9.75), C.stone, M.Slate, { solid = true })
	part(Street, "Walkway", Vector3.new(rl, 0.3, 7.5), Wd(rc, 0.15, s * 13.75), C.walk, M.Slate, { solid = true })
end
part(Street, "Plaza", Vector3.new(45, 0.25, 48), Wd(372.5, 0.125, 0), C.stoneLt, M.Cobblestone, { solid = true })

-- house rows and lots
local x, nH, nLot = -350, 0, 0
for _, kind in ROW do
	if kind == "H" then
		for s = -1, 1, 2 do
			local xx, prevH = x, 0
			for _, w in widths(SEG_W) do
				local sp = spec(prevH)
				prevH = sp.G + sp.U
				nH += 1
				house(Rows, ("House%s%02d"):format(s < 0 and "N" or "S", nH), ORIGIN * CFrame.new(xx + w / 2, 0, s * HALF) * facing(s), w, sp)
				xx += w
				task.wait()
			end
			grove(x + 5, x + SEG_W - 5, s, 50, 120, 5, 1.4, 2.0)
		end
		x += SEG_W
	else
		nLot += 1
		for s = -1, 1, 2 do
			local side = s < 0 and "N" or "S"
			local slot = part(Lots, ("PlotSlot%s%d"):format(side, nLot), Vector3.new(LOT_W, 1, LOT_D), ORIGIN * CFrame.new(x + LOT_W / 2, 0.5, s * (HALF + LOT_D / 2)) * facing(s), C.plaster)
			slot.Transparency = 1
			slot:SetAttribute("Side", side)
			wall(Lots, x + 0.9, s, HALF + 1.5, HALF + LOT_D)
			wall(Lots, x + LOT_W - 0.9, s, HALF + 1.5, HALF + LOT_D)
			andon(Props, Wd(x + 3, 0.3, s * 13.2))
			andon(Props, Wd(x + LOT_W - 3, 0.3, s * 13.2))
		end
		x += LOT_W
		task.wait()
	end
end

-- west: village gate (刀鍛冶の里, "swordsmith village") and walls out to the cliffs
local gx = -372
for s = -1, 1, 2 do
	part(Landmarks, "GatePost", Vector3.new(1.6, 14.7, 1.6), Wd(gx, 8.45, s * 13), C.timberDk, M.Wood, { solid = true })
	part(Landmarks, "GateFoot", Vector3.new(2.4, 0.8, 2.4), Wd(gx, 0.7, s * 13), C.stone, M.Slate, { solid = true })
	wall(Landmarks, gx, s, 14, 130)
	grove(-392, -380, s, 22, 125, 4, 1.5, 2.1)
	grove(-366, -354, s, 22, 125, 4, 1.5, 2.1)
end
part(Landmarks, "GateBeam", Vector3.new(1.2, 1.0, 28.5), Wd(gx, 11.0, 0), C.timberDk, M.Wood)
part(Landmarks, "GateLintel", Vector3.new(1.4, 1.3, 31), Wd(gx, 14.6, 0), C.timberDk, M.Wood)
local gateSign = part(Landmarks, "GateSign", Vector3.new(8, 2.2, 0.4), Wd(gx, 12.8, 0) * CFrame.Angles(0, math.pi / 2, 0), C.timberDk, M.Wood)
label(gateSign, "刀鍛冶の里", C.paper, Enum.NormalId.Front)
label(gateSign, "刀鍛冶の里", C.paper, Enum.NormalId.Back)
do
	local gp, run = rad(28), 2.6
	for sgn = -1, 1, 2 do
		local c = Vector3.new(gx + sgn * run / 2, 15.25 + run / 2 * math.tan(gp), 0) + Vector3.new(sgn * math.sin(gp), math.cos(gp), 0) * 0.2
		part(Landmarks, "GateRoof", Vector3.new(run / math.cos(gp), 0.5, sgn > 0 and 33.08 or 33), ORIGIN * CFrame.new(c) * CFrame.Angles(0, 0, -sgn * gp), C.tileDk, M.ClayRoofTiles)
	end
	part(Landmarks, "GateRidge", Vector3.new(0.9, 0.6, 33.4), Wd(gx, 15.25 + run * math.tan(gp) + 0.45, 0), C.tileDk, M.ClayRoofTiles)
end
chochin(Landmarks, Wd(gx, 8.8, 0), C.red)

-- east: torii and shrine at the end of the street
local tx = 358
for s = -1, 1, 2 do
	cyl(Landmarks, "ToriiPillar", 14.5, 1.5, Wd(tx, 7.5, s * 7.5), C.vermilion, M.SmoothPlastic, { solid = true })
	cyl(Landmarks, "ToriiFoot", 1.0, 2.0, Wd(tx, 0.75, s * 7.5), C.black)
	placeModel(SS.Buildings3D.StoneLantern, Wd(366, 0, s * 6), 1.3, Landmarks, 0.25)
	placeModel(SS.Buildings3D.StoneLantern, Wd(372, 0, s * 6), 1.3, Landmarks, 0.25)
	placeModel(s < 0 and SS.Village3D.Sakura1 or SS.Village3D.Maple1, Wd(384, 0, s * 17), 1.8, Trees, 0.25)
	placeModel(SS.Village3D.Pine2, Wd(364, 0, s * 20), 1.6, Trees, 0.25)
end
part(Landmarks, "Nuki", Vector3.new(0.8, 0.9, 19), Wd(tx, 11.2, 0), C.vermilion)
part(Landmarks, "Kasagi", Vector3.new(1.3, 0.9, 21.5), Wd(tx, 14.4, 0), C.vermilion)
part(Landmarks, "KasagiTop", Vector3.new(1.6, 0.7, 23), Wd(tx, 15.15, 0), C.black)
part(Landmarks, "Gakuzuka", Vector3.new(0.6, 2.4, 0.9), Wd(tx, 12.85, 0), C.vermilion)
part(Landmarks, "ShrineBase", Vector3.new(16, 1.2, 18), Wd(384, 0.6, 0), C.stone, M.Cobblestone, { solid = true })
part(Landmarks, "ShrineStep", Vector3.new(1.5, 0.55, 7), Wd(373.75, 0.275, 0), C.stone, M.Cobblestone, { solid = true })
part(Landmarks, "ShrineStep", Vector3.new(1.5, 0.9, 7), Wd(375.25, 0.45, 0), C.stone, M.Cobblestone, { solid = true })
do
	local hcf = Wd(378, 1.2, 0) * CFrame.Angles(0, math.pi / 2, 0)
	house(Landmarks, "Shrine", hcf, 14, {
		style = "shrine", G = 8.5, U = 0, D = 12, F1 = 1.5, pitch = 32, ovF = 3.4, ovS = 1.5, ridgeH = 1.4,
		roofCol = C.copper, roofMat = M.Metal, postCol = C.vermilion, groundCol = C.plaster, transomCol = C.plaster,
		bays = { "lattice" }, paper = true, doorBay = 0,
	})
	part(Landmarks, "Shimenawa", Vector3.new(11, 0.8, 0.8), hcf * CFrame.new(0, 7.0, -0.3), C.straw, M.Fabric, { shape = Enum.PartType.Cylinder })
	for _, sx in { -3, 0, 3 } do part(Landmarks, "Shide", Vector3.new(0.5, 1.2, 0.05), hcf * CFrame.new(sx, 6.0, -0.75), C.plaster) end
	part(Landmarks, "OfferingBox", Vector3.new(3.4, 1.6, 1.4), hcf * CFrame.new(0, 0.8, -1.4), C.cedar, M.WoodPlanks, { solid = true })
end

-- mountains: stretch the cliff ring so its inner face sits at x ±395, z ±130 around the street
do
	local ring = SS.Village3D.CliffRing:Clone()
	local c0 = ring:GetBoundingBox().Position
	local SX = 790 / 460
	for _, bp in ring:GetDescendants() do
		if bp:IsA("BasePart") then
			local rel = bp.Position - c0
			bp.Size = Vector3.new(bp.Size.X * SX, bp.Size.Y, bp.Size.Z)
			bp.Position = c0 + Vector3.new(rel.X * SX, rel.Y, rel.Z)
			bp.CanCollide, bp.CanQuery, bp.CanTouch = false, false, false
		end
	end
	local c1 = ring:GetBoundingBox().Position
	ring:TranslateBy(Vector3.new(ORIGIN.X - c1.X, 0, ORIGIN.Z - c1.Z))
	ring.Name = "Mountains"
	ring.Parent = village
	-- invisible walls on the inner face line (the cliff mesh itself does not collide)
	for _, b in { { 0, 130, 790, 2 }, { 0, -130, 790, 2 }, { 395, 0, 2, 260 }, { -395, 0, 2, 260 } } do
		local wb = part(village, "Bound", Vector3.new(b[3], 80, b[4]), Wd(b[1], 40, b[2]), C.plaster, nil, { solid = true })
		wb.Transparency = 1
	end
end

-- Lot N2 widened for the current plot (2026-10-21, Allen): the north houses, backyard trees, lot walls and lamps
-- between lots N1 and N3 go to ServerStorage.Legacy.Village_besideN2 and PlotSlotN2 becomes 280 wide (x -140..140).
do
	local park = Instance.new("Folder")
	park.Name = "Village_besideN2"
	local function inside(pos)
		local l = ORIGIN:PointToObjectSpace(pos)
		return l.Z < -10 and l.X > -139.9 and l.X < 139.9
	end
	for _, f in { Rows, Trees } do
		for _, m in f:GetChildren() do
			if inside(m:GetPivot().Position) then m.Parent = park end
		end
	end
	for _, f in { Lots, Props } do
		for _, p in f:GetChildren() do
			if p:IsA("BasePart") and not p.Name:match("^PlotSlot") and inside(p.Position) then p.Parent = park end
		end
	end
	Lots.PlotSlotN2.Size = Vector3.new(280, 1, LOT_D)
	park.Parent = SS:FindFirstChild("Legacy") or SS
end

-- ShopService waits for Village.CustomerSpawn: on the road in front of lot N2.
local spawn = part(village, "CustomerSpawn", Vector3.new(2, 1, 2), CFrame.new(18.5, 3, -563), C.plaster)
spawn.Transparency = 1

local n = 0
for _, d in village:GetDescendants() do if d:IsA("BasePart") then n += 1 end end
return ("Village built: %d houses, %d lots, %d parts"):format(nH, nLot * 2, n)

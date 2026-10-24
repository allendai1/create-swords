-- build_simple.luau: the live map of Create Swords!, a simplified town of six separated plots (2026-10-22). Built first
-- beside the town street and its redesign to compare; then Allen: "Make the simplified map the live map."
-- Allen: "could we also try a simplified map. there should 3 new files for how to generate it in the vault": the brief
-- at the top of Art/Town Street Redesign References, References/Town Street Redesign/06-simple-separated-plots-v1.png and
-- simplified-map-prompt.md. Six identical plots, three per side of one broad paved street, each separated from the next
-- by a paved lane a full frontage wide (half a frontage at first; Allen: "expand the map and separate the houses more");
-- all six fronts on one line (Allen 2026-10-23: "The shop building is misaligned with the actual street"; the middle
-- pair stood 8 back as a junction till then); the lane between lots 1 and 2 runs
-- on through the back wall (turned on the south side: between S2 and S3); a timber gate west, a small shrine east; a few
-- small townhouses at the edges only. No stalls, trees or filler houses.
-- Run in Studio (Edit) through MCP execute_luau. Rebuilds Workspace.Village (an earlier build moves to
-- ServerStorage.Legacy), which PlotService reads: Village.Lots.PlotSlot<lot>. PlotService puts an empty copy of the plot
-- on every unclaimed lot at runtime (Allen 2026-10-22: "have all 6 player plots on the map"), so the map has no closed
-- shopfronts. Same SEED = same map. After a rebuild, pivot Workspace.Plot (the plot template) onto PlotSlotN2.
-- The townhouse kit (part … spec) is build_town.luau's, copied unchanged. build_street.luau and build_town.luau are
-- retired (their maps are parked in ServerStorage.Legacy).
--
-- Plan, in the north frame (x along the street, west −; the north side at −z; "depth" = distance from the street centre):
--   lots 48.5 × 96 at x −96.5, 0, 96.5 with 48-wide lanes between; fronts at depth 36 (72 apart).
--   Each lot: an earth pad with stone edging on its sides and back (outside the building) and the current street's
--   front cross-section (walkway 1.5 under the façade to 6 out, water channel 6…8 out), so the plot template fits.
--   Small single-storey houses on the street front at x ±180.75, and one by each side lane outside the back wall.
--   Town wall: gate line x −200, back walls at depth 172, the east wall behind the shrine plaza at x 248.
--   The south side is the same plan turned 180° about ORIGIN; gate, shrine and their walls are placed in world terms.
-- Ground tops: lane paving 0.12, plot pads 0.16, street 0.2, plaza 0.25, water 0.26, centre stones 0.26,
-- walkway 0.3, edging 0.36, curbs 0.5, gutter bridges 0.62. Same-kind ground parts never overlap.
--
-- Street surfaces (Allen 2026-10-22: "The roads look ugly."; the generated TownFlagstone read as noisy, high-contrast
-- grey tiles). ROAD_STYLE picks one of two to compare. "earth": packed earth (period Edo), a strip of cut stones down
-- the middle, and the plots' stone gutter (curb, water, curb) carried along the open stretches of the street's edges,
-- with a stone bridge at each delivery way. "stone": even cut-stone slabs in one calm grey. Both are tiling textures
-- uploaded from Models/Village/road_textures.py (MaterialVariants TownEarth and TownSlab, made here).
-- loadstring(...Source)("road") restyles the live street only (Road, Paving, Junction, Street.RoadStyle), leaving the
-- rest of the map, and anything moved by hand, alone; a full build makes the same street.

local MODE = ... -- nil: build the whole map; "road": restyle the live street only
local ROAD_STYLE = "earth" -- "earth" | "stone"
local SEED = 23
local LIFT = 2.5 -- ground storeys as tall as the street's (openings top out at OT 9.7)
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

-- ---------------------------------------------------------------- simple map plan
local HALF, MID = 36, 0 -- fronts at depth 36 (72 apart); MID: the middle pair's setback (8, a junction, till 2026-10-23)
local LOT_W, LOT_D = 48.5, 96
local LOTS = { { -96.5, HALF }, { 0, HALF + MID }, { 96.5, HALF } } -- lot centre x and front depth, lots 1…3 west to east
local LANE = { -72.25, -24.25 } -- the lane between lots 1 and 2 (48 wide), which runs on through the back wall
local ORIGIN = CFrame.new(640, 0, -200) -- where it was built for the comparison, clear of everything
local NF, SF = ORIGIN, ORIGIN * CFrame.Angles(0, math.pi, 0) -- north and south frames
local STREET, EAST = CFrame.Angles(0, math.pi, 0), CFrame.Angles(0, -math.pi / 2, 0) -- facings in a frame
local XW, XE, XB = -200, 200, 248 -- town wall and gate (west), shrine plaza start (east), wall behind the shrine
local BACK, BZ, GH = 172, 210, 16 -- back walls' depth, bounds' depth, half the gate's opening
local CORNER_X = 180.75 -- small townhouses on the street front at both ends, 20 wide, a lane's width past the end lots
local LANE_COL, EARTH = Color3.fromRGB(178, 170, 158), Color3.fromRGB(168, 140, 104)

local function Wd(x, y, z) return ORIGIN * CFrame.new(x, y, z) end

-- ground rectangle in frame F: x0..x1, depth d0..d1
local function slab(parent, name, F, x0, x1, d0, d1, top, col, mat)
	return part(parent, name, Vector3.new(x1 - x0, top, d1 - d0), F * CFrame.new((x0 + x1) / 2, top / 2, -(d0 + d1) / 2), col, mat, { solid = true })
end

-- street surfaces: the style's MaterialVariant (made or updated in MaterialService) on the road, junctions and lanes;
-- the textures are greyscale, tinted by the part colour
local MS = game:GetService("MaterialService")
local function variant(name, base, colorMap, normalMap, studs, pattern)
	local v = MS:FindFirstChild(name) or Instance.new("MaterialVariant")
	v.Name, v.BaseMaterial, v.ColorMap, v.NormalMap, v.StudsPerTile, v.MaterialPattern = name, base, colorMap, normalMap, studs, pattern
	v.Parent = MS
	return name
end
local SURFACE = ROAD_STYLE == "earth" and {
	base = M.Ground, road = Color3.fromRGB(196, 160, 116), lane = Color3.fromRGB(184, 158, 124),
	variant = variant("TownEarth", M.Ground, "rbxassetid://126923524824747", "rbxassetid://95753092475786", 24, Enum.MaterialPattern.Organic),
} or {
	base = M.Pavement, road = Color3.fromRGB(150, 148, 144), lane = Color3.fromRGB(150, 148, 144),
	variant = variant("TownSlab", M.Pavement, "rbxassetid://134124888275477", "rbxassetid://126594211996820", 16, Enum.MaterialPattern.Regular),
}
local function surface(p, kind) -- kind: "road" (the street and junctions) or "lane"
	p.Material, p.MaterialVariant, p.Color = SURFACE.base, SURFACE.variant, SURFACE[kind]
	return p
end

-- the stone water channel (curb, water, curb) 6…8 out from a front. fcf: on the façade line at the run's middle,
-- LookVector toward the street; the run is len long along its local x.
local function channel(parent, fcf, len)
	local function at(z, y) return fcf * CFrame.new(0, y, z) end
	part(parent, "Curb", Vector3.new(len, 0.5, 0.5), at(-6.25, 0.25), C.stone, M.Slate, { solid = true })
	part(parent, "Water", Vector3.new(len, 0.26, 1.0), at(-7, 0.13), C.water, M.SmoothPlastic, { solid = true, refl = 0.12 })
	part(parent, "Curb", Vector3.new(len, 0.5, 0.5), at(-7.75, 0.25), C.stone, M.Slate, { solid = true })
end
-- walkway and channel along a front
local function frontage(parent, fcf, len)
	part(parent, "Walkway", Vector3.new(len, 0.3, 7.5), fcf * CFrame.new(0, 0.15, -2.25), C.walk, M.Slate, { solid = true })
	channel(parent, fcf, len)
end

-- plaster wall with a tile cap; cf on the ground at its middle, its length along local z
local function wallSeg(parent, cf, len)
	part(parent, "WallBase", Vector3.new(1.6, 1.6, len), cf * CFrame.new(0, 0.8, 0), C.stone, M.Cobblestone, { solid = true })
	part(parent, "Wall", Vector3.new(1.1, 5.0, len), cf * CFrame.new(0, 4.1, 0), C.plaster, M.Plaster, { solid = true })
	part(parent, "WallCap", Vector3.new(2.2, 0.5, len + 0.6), cf * CFrame.new(0, 6.85, 0), C.tile, M.ClayRoofTiles)
	part(parent, "WallRidge", Vector3.new(0.7, 0.45, len + 0.7), cf * CFrame.new(0, 7.25, 0), C.tileDk, M.ClayRoofTiles)
end
local function wallZ(parent, F, x, d0, d1) wallSeg(parent, F * CFrame.new(x, 0, -(d0 + d1) / 2), d1 - d0) end
local function wallX(parent, F, x0, x1, d) wallSeg(parent, F * CFrame.new((x0 + x1) / 2, 0, -d) * CFrame.Angles(0, math.pi / 2, 0), x1 - x0) end
-- where walls meet or end: walls stop 1 short of its centre, so their ends and caps are inside it
local function pillar(parent, F, x, d)
	part(parent, "PillarBase", Vector3.new(3.0, 1.8, 3.0), F * CFrame.new(x, 0.9, -d), C.stone, M.Cobblestone, { solid = true })
	part(parent, "Pillar", Vector3.new(2.6, 7.6, 2.6), F * CFrame.new(x, 3.8, -d), C.plaster, M.Plaster, { solid = true })
	part(parent, "PillarCap", Vector3.new(3.4, 0.6, 3.4), F * CFrame.new(x, 7.9, -d), C.tileDk, M.ClayRoofTiles)
end

-- standing lamp on a lot's front corner
local function lamp(parent, cf)
	part(parent, "LampFoot", Vector3.new(1.4, 0.6, 1.4), cf * CFrame.new(0, 0.5, 0), C.stone, M.Slate, { solid = true })
	part(parent, "LampPost", Vector3.new(0.6, 7.4, 0.6), cf * CFrame.new(0, 4.5, 0), C.timberDk, M.Wood, { solid = true })
	glow(part(parent, "Andon", Vector3.new(1.6, 2.2, 1.6), cf * CFrame.new(0, 9.3, 0), C.paper), 16)
	part(parent, "LampCap", Vector3.new(2.4, 0.4, 2.4), cf * CFrame.new(0, 10.6, 0), C.tileDk, M.ClayRoofTiles)
end

local function torii(parent, cf, k) -- the street's torii, scaled by k from its base
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

local function placeModel(src, cf, scale, parent, groundY)
	local mdl = src:Clone()
	if scale and scale ~= 1 then mdl:ScaleTo(scale) end
	mdl:PivotTo(cf)
	local bcf, bs = mdl:GetBoundingBox()
	mdl:TranslateBy(Vector3.new(0, (groundY or 0) - (bcf.Y - bs.Y / 2), 0))
	mdl.Parent = parent
	return mdl
end

-- a small plain single-storey townhouse, eaves to the street like the plots' shops
local function smallHouse(parent, name, hcf, w, d)
	local sp = spec(0, "low")
	sp.D, sp.sign, sp.bench = d, nil, false
	return house(parent, name, hcf, w, sp)
end

-- the earth style's stones and gutters, in Street.RoadStyle (empty for "stone")
local function roadStyle(Street)
	local f = Instance.new("Folder")
	f.Name = "RoadStyle"
	f.Parent = Street
	if ROAD_STYLE ~= "earth" then return end
	local rs = Random.new(SEED + 1) -- its own stream, so the map's (house styles) is the same with either style
	-- cut stones down the middle, 5 wide, from the road's west end to the plaza
	local x = XW - 29
	while true do
		local len, g = rs:NextNumber(2.2, 3.2), rs:NextInteger(-6, 6)
		if x + len > XE - 1 then break end
		part(f, "RoadStone", Vector3.new(len, 0.16, 5), Wd(x + len / 2, 0.18, 0), Color3.fromRGB(168 + g, 162 + g, 152 + g), M.Slate, { solid = true })
		x += len + 0.22
	end
	-- gutters where no front's channel lines the street (lane mouths, gaps by the end houses),
	-- in line with the fronts' (depth 28…30), and a bridge across at each delivery way (lot centre − 33)
	local w = LOT_W / 2
	for _, F in { NF, SF } do
		for _, s in { { XW + 0.9, -CORNER_X - 10 }, { -CORNER_X + 10, LOTS[1][1] - w }, { LOTS[1][1] + w, LOTS[2][1] - w } } do
			for _, k in { 1, -1 } do -- and mirrored: the street's plan is symmetric about x = 0
				channel(f, F * CFrame.new(k * (s[1] + s[2]) / 2, 0, -HALF) * STREET, s[2] - s[1])
			end
		end
		for _, lot in LOTS do
			part(f, "GutterBridge", Vector3.new(6, 0.52, 2.6), F * CFrame.new(lot[1] - 33, 0.36, -(HALF - 7)), C.stone, M.Slate, { solid = true })
		end
	end
end

if MODE == "road" then -- restyle the live street only
	local Street = workspace.Village.Street
	for _, p in Street:GetChildren() do
		if p.Name == "Road" or p.Name == "Junction" then
			surface(p, "road")
		elseif p.Name == "Paving" then
			surface(p, "lane")
		elseif p.Name == "RoadStyle" then
			p:Destroy()
		end
	end
	roadStyle(Street)
	local n = 0
	for _, d in Street.RoadStyle:GetDescendants() do if d:IsA("BasePart") then n += 1 end end
	return ("Street restyled (%s): %d parts in RoadStyle"):format(ROAD_STYLE, n)
end

-- ---------------------------------------------------------------- build
local old = workspace:FindFirstChild("Village")
if old then
	old.Name = "Village_before_" .. os.date("!%Y%m%d%H%M%S")
	old.Parent = SS:FindFirstChild("Legacy") or SS
end
local town = Instance.new("Model")
town.Name = "Village"
town.WorldPivot = ORIGIN
town.Parent = workspace
local function folder(name)
	local f = Instance.new("Folder")
	f.Name = name
	f.Parent = town
	return f
end
local Street, Houses, Lots, Walls, Landmarks = folder("Street"), folder("Houses"), folder("Lots"), folder("Walls"), folder("Landmarks")

surface(part(Street, "Road", Vector3.new(XE - (XW - 30), 0.2, 2 * (HALF - 8)), Wd((XE + XW - 30) / 2, 0.1, 0), C.road, M.Pavement, { solid = true }), "road")
roadStyle(Street)

for _, F in { NF, SF } do
	local tag = F == NF and "N" or "S"
	local m = tag == "N" and 1 or -1 -- frame x of a west-east (world) offset
	local lo, hi = math.min(m * XW, m * XB), math.max(m * XW, m * XB)

	-- lanes and buffers: one paving slab from the street's edge to the back wall, and the lane on past it
	surface(slab(Street, "Paving", F, lo, hi, HALF - 8, BACK, 0.12, LANE_COL, M.Pavement), "lane")
	surface(slab(Street, "Paving", F, LANE[1], LANE[2], BACK, BZ, 0.12, LANE_COL, M.Pavement), "lane")

	for n, lot in LOTS do
		local xc, d = lot[1], lot[2]
		local x0, x1 = xc - LOT_W / 2, xc + LOT_W / 2
		local name = tag .. (tag == "N" and n or 4 - n)
		local slot = part(Lots, "PlotSlot" .. name, Vector3.new(LOT_W, 1, LOT_D), F * CFrame.new(xc, 0.5, -(d + LOT_D / 2)) * STREET, C.plaster)
		slot.Transparency = 1
		slot:SetAttribute("Side", tag)
		-- earth pad, and stone edging on the sides and back, just outside the lot (the shop's posts reach ±24.2)
		slab(Lots, "Pad", F, x0, x1, d, d + LOT_D, 0.16, EARTH, M.Ground)
		for _, ex in { x0 - 0.4, x1 + 0.4 } do
			part(Lots, "Edge", Vector3.new(0.8, 0.36, LOT_D - 0.7), F * CFrame.new(ex, 0.18, -(d + 1.5 + d + LOT_D + 0.8) / 2), C.stone, M.Slate, { solid = true })
		end
		part(Lots, "Edge", Vector3.new(LOT_W, 0.36, 0.8), F * CFrame.new(xc, 0.18, -(d + LOT_D + 0.4)), C.stone, M.Slate, { solid = true })
		frontage(Street, F * CFrame.new(xc, 0, -d) * STREET, LOT_W)
		for _, lx in { x0 + 2, x1 - 2 } do lamp(Street, F * CFrame.new(lx, 0, -(d - 11))) end -- on the road, clear of the shop door
		task.wait()
	end

	-- small houses: one on the street front at each end, one by the lane outside the back wall (on its own walkway)
	for i, cx in { -CORNER_X, CORNER_X } do
		smallHouse(Houses, ("End%s%d"):format(tag, i), F * CFrame.new(cx, 0, -HALF) * STREET, 20, 16)
		frontage(Street, F * CFrame.new(cx, 0, -HALF) * STREET, 20)
	end
	local fx = LANE[1] - 2
	local outer = smallHouse(Houses, "Outer" .. tag, F * CFrame.new(fx, 0, -(BACK + 16)) * EAST, 20, 14)
	if outer:FindFirstChild("Bridge") then outer.Bridge:Destroy() end -- no channel along the lane
	slab(Street, "Walkway", F, fx - 1.5, fx + 4, BACK + 6, BACK + 26, 0.3, C.walk, M.Slate)

	-- town walls: gate line west, back wall (open where the lane runs on), pillars at the corners and the opening
	wallZ(Walls, F, m * XW, GH + 1, BACK - 1)
	wallX(Walls, F, lo + 1, LANE[1] - 1, BACK)
	wallX(Walls, F, LANE[2] + 1, hi - 1, BACK)
	for _, x in { lo, hi, LANE[1], LANE[2] } do pillar(Walls, F, x, BACK) end
end
wallZ(Walls, NF, XB, -(BACK - 1), BACK - 1) -- behind the shrine, from back wall to back wall

-- west: timber town gate (刀鍛冶の里, "swordsmith village")
for s = -1, 1, 2 do
	part(Landmarks, "GateFoot", Vector3.new(3, 1.0, 3), Wd(XW, 0.7, s * GH), C.stone, M.Slate, { solid = true })
	part(Landmarks, "GatePost", Vector3.new(2, 17.6, 2), Wd(XW, 10.0, s * GH), C.timberDk, M.Wood, { solid = true })
end
part(Landmarks, "GateBeam", Vector3.new(1.4, 1.2, 2 * GH - 1.9), Wd(XW, 13.5, 0), C.timberDk, M.Wood)
part(Landmarks, "GateLintel", Vector3.new(1.8, 1.6, 2 * GH + 6), Wd(XW, 18.2, 0), C.timberDk, M.Wood)
local gateSign = part(Landmarks, "GateSign", Vector3.new(10, 2.8, 0.4), Wd(XW, 15.7, 0) * CFrame.Angles(0, math.pi / 2, 0), C.timberDk, M.Wood)
label(gateSign, "刀鍛冶の里", C.paper, Enum.NormalId.Front)
label(gateSign, "刀鍛冶の里", C.paper, Enum.NormalId.Back)
do
	local gp, run, yb = rad(28), 3.4, 19.0
	for sgn = -1, 1, 2 do
		local c = Vector3.new(XW + sgn * run / 2, yb + run / 2 * math.tan(gp), 0) + Vector3.new(sgn * math.sin(gp), math.cos(gp), 0) * 0.25
		part(Landmarks, "GateRoof", Vector3.new(run / math.cos(gp), 0.6, 2 * GH + (sgn > 0 and 7.08 or 7)), ORIGIN * CFrame.new(c) * CFrame.Angles(0, 0, -sgn * gp), C.tileDk, M.ClayRoofTiles)
	end
	part(Landmarks, "GateRidge", Vector3.new(1.1, 0.7, 2 * GH + 7.4), Wd(XW, yb + run * math.tan(gp) + 0.5, 0), C.tileDk, M.ClayRoofTiles)
end
chochin(Landmarks, Wd(XW, 11.4, 0), C.red)

-- east: plaza, torii, stone lanterns and a small shrine closing the street
part(Landmarks, "Plaza", Vector3.new(46, 0.25, 80), Wd(XE + 23, 0.125, 0), C.stoneLt, M.Cobblestone, { solid = true })
torii(Landmarks, Wd(XE + 8, 0, 0), 1.1)
for s = -1, 1, 2 do
	placeModel(SS.Buildings3D.StoneLantern, Wd(XE + 15, 0, s * 7), 1.4, Landmarks, 0.25)
	placeModel(SS.Buildings3D.StoneLantern, Wd(XE + 21, 0, s * 7), 1.4, Landmarks, 0.25)
	placeModel(s < 0 and SS.Village3D.Sakura1 or SS.Village3D.Maple1, Wd(XE + 36, 0, s * 30), 1.6, Landmarks, 0.25)
end
part(Landmarks, "ShrineBase", Vector3.new(20, 1.6, 22), Wd(XE + 33, 0.8, 0), C.stone, M.Cobblestone, { solid = true })
part(Landmarks, "ShrineStep", Vector3.new(1.5, 0.6, 9), Wd(XE + 20.75, 0.3, 0), C.stone, M.Cobblestone, { solid = true })
part(Landmarks, "ShrineStep", Vector3.new(1.5, 1.1, 9), Wd(XE + 22.25, 0.55, 0), C.stone, M.Cobblestone, { solid = true })
do
	local hcf = Wd(XE + 25, 1.6, 0) * CFrame.Angles(0, math.pi / 2, 0)
	house(Landmarks, "Shrine", hcf, 16, {
		style = "shrine", G = 8.5 + LIFT, U = 0, D = 14, F1 = 1.5, pitch = 32, ovF = 3.4, ovS = 1.5, ridgeH = 1.4,
		roofCol = C.copper, roofMat = M.Metal, postCol = C.vermilion, groundCol = C.plaster, transomCol = C.plaster,
		bays = { "lattice" }, paper = true, doorBay = 0,
	})
	part(Landmarks, "Shimenawa", Vector3.new(12, 0.8, 0.8), hcf * CFrame.new(0, 7.0 + LIFT, -0.3), C.straw, M.Fabric, { shape = Enum.PartType.Cylinder })
	for _, sx in { -3, 0, 3 } do part(Landmarks, "Shide", Vector3.new(0.5, 1.2, 0.05), hcf * CFrame.new(sx, 6.0 + LIFT, -0.75), C.plaster) end
	part(Landmarks, "OfferingBox", Vector3.new(3.4, 1.6, 1.4), hcf * CFrame.new(0, 0.8, -1.4), C.cedar, M.WoodPlanks, { solid = true })
end

-- invisible walls round the map (only matters if it becomes the live map)
for _, b in { { (XW - 30 + XB + 10) / 2, BZ, XB + 10 - (XW - 30), 2 }, { (XW - 30 + XB + 10) / 2, -BZ, XB + 10 - (XW - 30), 2 }, { XW - 30, 0, 2, 2 * BZ }, { XB + 10, 0, 2, 2 * BZ } } do
	local wb = part(town, "Bound", Vector3.new(b[3], 80, b[4]), Wd(b[1], 40, b[2]), C.plaster, nil, { solid = true })
	wb.Transparency = 1
end

local n = 0
for _, d in town:GetDescendants() do if d:IsA("BasePart") then n += 1 end end
return ("Village built: %d parts"):format(n)

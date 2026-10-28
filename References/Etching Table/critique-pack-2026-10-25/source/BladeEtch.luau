--!strict
-- Etched pattern on a finished blade (client): a thin two-colour skin just above both flat faces of a
-- BladeView blade, built from the same BladeCore station params and sampled finer than the stations,
-- so it follows the forged and ground shape of every blueprint (tantō, wakizashi, katana). Built once
-- per sword by SwordRenderer; the anvil's blade has no etch.
--
-- A pattern is a function of sw (position along the blade in local blade widths, 0 at the base) returning
-- how far the second colour reaches from the edge toward the spine, as a fraction of the width. Each sample
-- row has columns at the edge line, the boundary (twice, one per colour), the ridge crease and the spine
-- line, so the colours meet crisply. Thin strips at the edge and spine stay bare, so the blade's own steel
-- shows as bright edge lines. Vertex colours shade the bevel: lit near the edge, fading toward the ridge
-- and along the blade. Pattern design and numbers: vault Art/Flame Etch (v4, Prototypes/etch).
-- Blade space as in BladeView: X along the blade, Y through the thickness, cutting edge toward +Z.
-- ponytail: one extra EditableMesh per etched sword; fold it into the blade mesh if memory gets tight.
--
-- Stroked patterns (2026-10-21, vault: Art/Animated Blade Etching; Eclipse first): the same skin, but textured
-- from Shared/EtchCanvas through UVs instead of vertex colours, so rings, gaps and separate motifs can be drawn.
-- buildTextured makes that overlay; its geometry depends only on the blade, so SwordMeshCache shares one per blade
-- and polish level and each copy gets its own texture. surface(params) is the face both skins use, and where the
-- Etching Table's tool touches the blade; bandReach() lets a band pattern (Flame) be drawn into a canvas too.
-- 2026-10-25: a band is laid out on the width capped at EtchCanvas.MOTIF_CM, as the stroked patterns are: its humps
-- are counted in capped widths and its reach is scaled to the capped width. On the zanbato (18.5 cm, its ridge 0.22
-- of the width from the edge) the band was clamped under the ridge into a flat line. Narrower blades are unchanged.

local AssetService = game:GetService("AssetService")

local Shared = script.Parent
local BladeCore = require(Shared:WaitForChild("BladeCore")) :: any
local Blueprints = require(Shared:WaitForChild("Blueprints")) :: any
local EtchCanvas = require(Shared:WaitForChild("EtchCanvas")) :: any
local Etches = require(Shared:WaitForChild("Etches")) :: any

local BladeEtch = {}

local LIFT_CM = 0.08 -- skin height above the blade surface (0.004 studs)
local SAMPLES_PER_WIDTH = 14 -- rows per local blade width (one hump is 0.75-1.05 widths)
local MIN_WIDTH_CM = 0.8 -- floor for the width when counting widths, so the point stays finite
local EDGE_LINE, SPINE_LINE = 0.032, 0.032 -- bare steel strips, fraction of the width
local SHEEN = Color3.fromRGB(150, 190, 230) -- what the lit bevel leans toward on the dark body
local SHADES = 12 -- shading steps (colour ids are cached per step)
local INK, INK_W = Color3.fromRGB(14, 10, 10), 0.045 -- a see-through band's outline colour and width (fraction of the width)

local function hash(i: number): number
	local x = math.sin(i * 127.1 + 311.7) * 43758.5453
	return x - math.floor(x)
end

-- Flame v4, matched to Allen's reference: a red band along the edge whose boundary is an even run of
-- rounded humps (0.14 of the width) at uneven spacing (0.75-1.05 widths), red deepest at 45% of each hump.
local BASE, AMP = 0.28, 0.14
local K = math.log(0.5) / math.log(0.45)
local function flame(sw: number): number
	local s, i = -0.3, 0
	while true do
		local period = 0.75 + 0.3 * hash(i)
		if sw < s + period then
			local ph = math.clamp((sw - s) / period, 0, 1)
			return BASE + AMP * (math.sin(math.pi * ph ^ K) ^ 2 - 0.5)
		end
		s += period
		i += 1
	end
end

BladeEtch.PATTERNS = { Flame = flame }

-- The blade's face by position: x in cm along the blade (0 at the base, `length` at the tip) and w across it
-- (0 at the cutting edge, 1 at the spine), interpolated between stations the same way the skins are built.
-- point(x, w, side, liftCm) is in studs, blade space, on the top (+1) or bottom (-1) face.
function BladeEtch.surface(params: any): any
	local N = #params.segLen
	local scale = Blueprints.STUDS_PER_CM
	local cl = BladeCore.centerline(params)
	local cum, swCum = table.create(N, 0), table.create(N, 0) -- cm, and local blade widths, from the base
	for i = 1, N - 1 do
		cum[i + 1] = cum[i] + params.segLen[i]
		local w = (params.spine[i] + params.spine[i + 1] - params.edge[i] - params.edge[i + 1]) / 2
		swCum[i + 1] = swCum[i] + params.segLen[i] / math.clamp(w, MIN_WIDTH_CM, EtchCanvas.MOTIF_CM)
	end
	local total = math.max(cum[N], 1e-6)
	local function locate(x: number): (number, number)
		x = math.clamp(x, 0, total)
		local lo, hi = 1, N - 1
		while lo < hi do
			local mid = (lo + hi + 1) // 2
			if cum[mid] <= x then
				lo = mid
			else
				hi = mid - 1
			end
		end
		local seg = cum[lo + 1] - cum[lo]
		return lo, if seg > 0 then (x - cum[lo]) / seg else 0
	end
	local function lerp(name: string, a: number, f: number): number
		local list = params[name]
		return list[a] + (list[a + 1] - list[a]) * f
	end
	local S = { length = total }
	function S.widthAt(x: number): number
		local a, f = locate(x)
		return lerp("spine", a, f) - lerp("edge", a, f)
	end
	function S.ridgeAt(x: number): number -- the ridge crease, as w
		local a, f = locate(x)
		return math.clamp(1 - lerp("ridge", a, f), 0.05, 0.95)
	end
	function S.swAt(x: number): number -- local blade widths from the base (a band pattern's position)
		local a, f = locate(x)
		return swCum[a] + (swCum[a + 1] - swCum[a]) * f
	end
	function S.point(x: number, w: number, side: number, liftCm: number): Vector3
		local a, f = locate(x)
		local px = cl.px[a] + (cl.px[a + 1] - cl.px[a]) * f
		local py = cl.py[a] + (cl.py[a + 1] - cl.py[a]) * f
		local angle = cl.angle[a] + (cl.angle[a + 1] - cl.angle[a]) * f
		local nx, ny = -math.sin(angle), math.cos(angle)
		local spine, edge = lerp("spine", a, f), lerp("edge", a, f)
		local wr = math.clamp(1 - lerp("ridge", a, f), 0.05, 0.95)
		local t, te = lerp("thick", a, f) / 2, lerp("edgeT", a, f) / 2
		local ts = lerp("thick", a, f) * lerp("spineT", a, f) / 2
		local off = edge + w * (spine - edge)
		local h = if w <= wr then te + (t - te) * (w / wr) else t + (ts - t) * ((w - wr) / (1 - wr))
		return Vector3.new(px + nx * off, side * (h + liftCm), -(py + ny * off)) * scale
	end
	return S
end

-- A band pattern's reach (how far its colour comes from the edge, as w) at x cm, clamped as the vertex skin
-- clamps it; nil if the pattern isn't a band.
function BladeEtch.bandReach(S: any, pattern: string): ((number) -> number)?
	local reachOf = BladeEtch.PATTERNS[pattern]
	if not reachOf then
		return nil
	end
	return function(x: number): number
		return math.clamp(reachOf(S.swAt(x)) * math.min(1, EtchCanvas.MOTIF_CM / S.widthAt(x)), EDGE_LINE + 0.01, S.ridgeAt(x) - 0.01)
	end
end

-- The overlay for a canvas: both faces, edge line to spine line, UV-mapped to the canvas strips (a row of
-- vertices at every strip boundary belongs to both strips). No texture yet: set TextureContent on each copy.
local TEX_ROWS_PER_WIDTH = 8
function BladeEtch.buildTextured(S: any, L: any): (MeshPart, EditableMesh)
	local mesh = AssetService:CreateEditableMesh()
	for _, side in { 1, -1 } do
		for strip = 0, L.strips - 1 do
			local xa, xb = strip * L.length / L.strips, (strip + 1) * L.length / L.strips
			local xs = { xa }
			local x = xa
			while true do
				x += math.max(S.widthAt(x) / TEX_ROWS_PER_WIDTH, 0.15)
				if x >= xb - 0.05 then
					break
				end
				table.insert(xs, x)
			end
			table.insert(xs, xb)
			local rows = table.create(#xs)
			for k, rx in xs do
				local wr = S.ridgeAt(rx)
				local ws = { EDGE_LINE, EDGE_LINE + (wr - EDGE_LINE) / 3, EDGE_LINE + 2 * (wr - EDGE_LINE) / 3, wr, (wr + 1 - SPINE_LINE) / 2, 1 - SPINE_LINE }
				local row = table.create(#ws)
				for c, w in ws do
					row[c] = { mesh:AddVertex(S.point(rx, w, side, LIFT_CM)), mesh:AddUV(EtchCanvas.uv(L, rx, w, strip)) }
				end
				rows[k] = row
			end
			for k = 1, #rows - 1 do
				local r0, r1 = rows[k], rows[k + 1]
				for c = 1, #r0 - 1 do
					local quad = { r0[c], r1[c], r1[c + 1], r0[c + 1] }
					for _, tri in { { 1, 2, 4 }, { 2, 3, 4 } } do
						local v = { quad[tri[1]], quad[tri[2]], quad[tri[3]] }
						if side < 0 then
							v[2], v[3] = v[3], v[2]
						end
						local face = mesh:AddTriangle(v[1][1], v[2][1], v[3][1])
						mesh:SetFaceUVs(face, { v[1][2], v[2][2], v[3][2] })
					end
				end
			end
		end
	end
	local part = AssetService:CreateMeshPartAsync(Content.fromObject(mesh))
	part.Name = "Etch"
	part.Material = Enum.Material.SmoothPlastic -- a canvas bakes its colours; Color doesn't tint a texture
	part.CanCollide, part.CanQuery, part.CanTouch = false, false, false
	part.Massless = true
	part.CastShadow = false
	return part, mesh
end

-- Returns the etch MeshPart (unparented; CFrame it like the blade part) and its EditableMesh, or nil for a
-- pattern that isn't a band. body = dark colour, flame = band colour (both at full light on the bevel). A body of
-- Etches.CLEAR builds the band faces only, so a textured metal shows between band and spine, and a thin dark ink line
-- (INK_W of the width) along the band's wavy edge, so the band reads on any metal (Allen 2026-10-23: the etch colours
-- "blend in with the texture").
function BladeEtch.build(params: any, pattern: string, body: Color3, flame: Color3): (MeshPart?, EditableMesh?)
	local reachOf = BladeEtch.PATTERNS[pattern]
	if not reachOf then
		return nil, nil
	end
	local N = #params.segLen
	local scale = Blueprints.STUDS_PER_CM
	local cl = BladeCore.centerline(params)
	local cum = table.create(N, 0)
	local widths = 0
	for i = 1, N - 1 do
		cum[i + 1] = cum[i] + params.segLen[i]
		local w = (params.spine[i] + params.spine[i + 1] - params.edge[i] - params.edge[i + 1]) / 2
		widths += params.segLen[i] / math.clamp(w, MIN_WIDTH_CM, EtchCanvas.MOTIF_CM)
	end
	local total = math.max(cum[N], 1e-6)
	local samples = math.max(4 * (N - 1), math.ceil(widths * SAMPLES_PER_WIDTH))

	local mesh = AssetService:CreateEditableMesh()
	local ids: { [string]: number } = {}
	local function colorId(kind: string, lit: number): number
		local step = math.floor(math.clamp(lit, 0, 1) * SHADES + 0.5)
		local key = kind .. step
		if not ids[key] then
			local s = step / SHADES
			local c = if kind == "f"
				then flame:Lerp(Color3.new(0, 0, 0), 0.35 * (1 - s)) -- the band darkens away from the light
				elseif kind == "i" then INK -- the outline: dark whatever the part's Color tints it
				else body:Lerp(SHEEN, 0.2 * s) -- the dark body picks up a cool sheen on the lit bevel
			ids[key] = mesh:AddColor(c, 1)
		end
		return ids[key]
	end

	-- one pass for the sample positions in widths (shared by both faces)
	local sws = table.create(samples + 1, 0)
	do
		local prevCm, prevW = 0, params.spine[1] - params.edge[1]
		for k = 1, samples do
			local s = k / samples * (N - 1)
			local i = math.min(math.floor(s), N - 2)
			local f = s - i
			local cm = cum[i + 1] + (cum[i + 2] - cum[i + 1]) * f
			local w = params.spine[i + 1] + (params.spine[i + 2] - params.spine[i + 1]) * f
				- (params.edge[i + 1] + (params.edge[i + 2] - params.edge[i + 1]) * f)
			sws[k + 1] = sws[k] + (cm - prevCm) / math.clamp((w + prevW) / 2, MIN_WIDTH_CM, EtchCanvas.MOTIF_CM)
			prevCm, prevW = cm, w
		end
	end

	local clear = body == Etches.CLEAR
	local quads = if clear then 3 else 4 -- band, reach seam, then the ink line (clear) or reach-to-ridge and ridge-to-spine (body)
	for _, side in { 1, -1 } do -- top face (+Y), then bottom face (-Y)
		local rows = table.create(samples + 1)
		for k = 0, samples do
			local s = k / samples * (N - 1)
			local i = math.min(math.floor(s), N - 2)
			local f = s - i
			local a, b = i + 1, i + 2
			local function at(name: string): number
				local list = params[name]
				return list[a] + (list[b] - list[a]) * f
			end
			local px = cl.px[a] + (cl.px[b] - cl.px[a]) * f
			local py = cl.py[a] + (cl.py[b] - cl.py[a]) * f
			local angle = cl.angle[a] + (cl.angle[b] - cl.angle[a]) * f
			local nx, ny = -math.sin(angle), math.cos(angle)
			local spine, edge = at("spine"), at("edge")
			local wr = math.clamp(1 - at("ridge"), 0.05, 0.95) -- ridge crease, measured from the edge
			local t, te = at("thick") / 2, at("edgeT") / 2
			local ts = at("thick") * at("spineT") / 2
			local u = (cum[a] + (cum[b] - cum[a]) * f) / total
			local reach = math.clamp(reachOf(sws[k + 1]) * math.min(1, EtchCanvas.MOTIF_CM / (spine - edge)), EDGE_LINE + 0.01, wr - 0.01)
			local along = math.clamp(1 - u / 0.5, 0.25, 1) -- the bevel sheen fades along the blade

			local function point(w: number): Vector3 -- w: 0 at the edge, 1 at the spine
				local off = edge + w * (spine - edge)
				local h = if w <= wr then te + (t - te) * (w / wr) else t + (ts - t) * ((w - wr) / (1 - wr))
				return Vector3.new(px + nx * off, side * (h + LIFT_CM), -(py + ny * off)) * scale
			end
			local function lit(w: number): number
				return (if w < wr then (1 - w / wr) ^ 1.4 else 0) * along
			end
			local cols = if clear
				then { { EDGE_LINE, "f" }, { reach, "f" }, { reach, "i" }, { math.min(reach + INK_W, wr - 0.005), "i" } }
				else { { EDGE_LINE, "f" }, { reach, "f" }, { reach, "b" }, { wr, "b" }, { 1 - SPINE_LINE, "b" } }
			local row = table.create(5)
			for c, col in cols do
				row[c] = { mesh:AddVertex(point(col[1])), colorId(col[2], lit(col[1])) }
			end
			rows[k + 1] = row
		end
		for k = 1, samples do
			local r0, r1 = rows[k], rows[k + 1]
			for c = 1, quads do
				local quad = { r0[c], r1[c], r1[c + 1], r0[c + 1] } -- along the blade, then toward the spine
				for _, tri in { { 1, 2, 4 }, { 2, 3, 4 } } do
					local v = { quad[tri[1]], quad[tri[2]], quad[tri[3]] }
					if side < 0 then
						v[2], v[3] = v[3], v[2] -- the bottom skin faces -Y
					end
					local face = mesh:AddTriangle(v[1][1], v[2][1], v[3][1])
					mesh:SetFaceColors(face, { v[1][2], v[2][2], v[3][2] })
				end
			end
		end
	end

	local part = AssetService:CreateMeshPartAsync(Content.fromObject(mesh))
	part.Name = "Etch"
	part.Color = Color3.new(1, 1, 1) -- the vertex colours carry the pattern
	part.Material = Enum.Material.Metal
	part.CanCollide, part.CanQuery, part.CanTouch = false, false, false
	part.Massless = true
	part.CastShadow = false
	return part, mesh
end

return BladeEtch

--!strict
-- Stroked etch patterns (vault: Art/Animated Blade Etching). One definition gives both the finished image and
-- the order it's drawn in: a pattern is a list of strokes, each a polyline of { x, y, h } in centimetres on the
-- blade's face (x along the blade from its base, y across from the cutting-edge line, h the stroke's half-width
-- there). Real centimetres keep rings round on every blade; sizes and repeats are worked out from the blade's own
-- length and width, and motifs stop short of the narrowing tip. Drawn by Shared/EtchCanvas, in list order, with
-- the tool lifted between strokes. Flame stays the vertex-coloured band in Shared/BladeEtch.
-- 2026-10-22: the concept sheet's other five (Tide, Stormroot, Woven Wind, Fracture, Falling Stars) joined Eclipse.
-- Fracture's shards are filled shapes: a stroke whose `fill` is a convex polygon, drawn by a scribbled guide.
-- 2026-10-25 (etch refinement, vault: Art/Animated Blade Etching): generators see the width capped at
-- EtchCanvas.MOTIF_CM and their motifs are centred on a wider face (the zanbato's were a few enormous shapes); motifs
-- stop where the edge starts rising into a sloped tip (the face's coordinates follow the edge, so they bent with it).
-- Eclipse's mouths, Woven Wind's crossings, Stormroot's root, Fracture's composition and Falling Stars were reworked.

local EtchCanvas = require(script.Parent:WaitForChild("EtchCanvas")) :: any

export type Stroke = { { number } } -- { x, y, h } points

local EtchPatterns = {}

local STEP = 0.12 -- cm between stroke points

-- A polyline from fx(t), fy(t), fh(t) for t in [0, 1], sampled about every STEP cm.
local function trace(lengthCm: number, fx: (number) -> number, fy: (number) -> number, fh: (number) -> number): Stroke
	local n = math.max(2, math.ceil(lengthCm / STEP))
	local pts = table.create(n + 1)
	for i = 0, n do
		local t = i / n
		pts[i + 1] = { fx(t), fy(t), fh(t) }
	end
	return pts
end

-- 0 at both ends of a stroke, 1 in the middle: tapered tips
local function taper(t: number, tip: number): number
	return math.clamp(math.min(t, 1 - t) / tip, 0, 1)
end

-- 0 at both ends, rising to 1 at `peak` (0..1) along concave flanks: a sparkle's ray, a shard of lightning
local function spike(t: number, peak: number): number
	local s = if t < peak then t / peak else (1 - t) / (1 - peak)
	return math.clamp(s, 0, 1) ^ 1.6
end

-- deterministic 0..1 for the irregular patterns (as Shared/BladeEtch's Flame spacing)
local function hash(i: number): number
	local x = math.sin(i * 127.1 + 311.7) * 43758.5453
	return x - math.floor(x)
end

-- Where motifs go: from x0, clear of the guard, to x1, short of the tip and of `limit` (where a sloped tip starts,
-- EtchPatterns.strokes); and the mean width between.
local function usable(length: number, widthAt: (number) -> number, limit: number): (number, number, number)
	local x0 = 0.8 * widthAt(0)
	local x1 = math.min(length - 1.9 * widthAt(length * 0.9), limit - 0.5 * widthAt(limit))
	local mean = 0
	for i = 0, 8 do
		mean += widthAt(x0 + (x1 - x0) * i / 8) / 9
	end
	return x0, x1, mean
end

-- Add a traced piece to a stroke being built (its first point repeats the stroke's last one).
local function extend(stroke: Stroke, piece: Stroke)
	for i = if #stroke > 0 then 2 else 1, #piece do
		table.insert(stroke, piece[i])
	end
end

-- Eclipse: thin connectors along the middle of the face linking crescent "eclipses" (an open ring and a small
-- inner sliver on its open side), gaps alternating toward the tip and the hilt, diamond nodes on the connectors
-- and a small four-point star before the tip. Drawn connector pieces first, then the rings, then the accents.
local function eclipse(length: number, widthAt: (number) -> number, ctx: any): { Stroke }
	local strokes: { Stroke } = {}
	local w0 = widthAt(0)
	local x0, x1, mean = usable(length, widthAt, ctx.limit)
	local n = math.max(1, math.floor((x1 - x0) / (4.4 * mean)))
	local rings = {}
	for i = 1, n do
		local xc = x0 + (i - 0.5) * (x1 - x0) / n
		local w = widthAt(xc)
		table.insert(rings, { x = xc, y = 0.5 * w, r = 0.33 * w, w = w, open = if i % 2 == 1 then 1 else -1 })
	end

	-- connectors: lead-in, between rings, tail toward the tip; a diamond node bulges in the middle of each
	local function connector(xa: number, xb: number, node: boolean)
		if xb - xa < 0.3 then
			return
		end
		table.insert(strokes, trace(xb - xa, function(t)
			return xa + (xb - xa) * t
		end, function(t)
			return 0.5 * widthAt(xa + (xb - xa) * t)
		end, function(t)
			local x = xa + (xb - xa) * t
			local w = widthAt(x)
			local h = 0.032 * w * (0.35 + 0.65 * taper(t, 0.12))
			if node then
				local d = math.abs(x - (xa + xb) / 2) / (0.34 * w)
				h = math.max(h, 0.085 * w * math.max(0, 1 - d))
			end
			return h
		end))
	end
	local gap = 0.2
	connector(x0 - 0.5 * w0, rings[1].x - rings[1].r - gap * rings[1].w, false)
	for i = 1, n - 1 do
		local a, b = rings[i], rings[i + 1]
		connector(a.x + a.r + gap * a.w, b.x - b.r - gap * b.w, true)
	end
	local last = rings[n]
	local tailEnd = math.min(ctx.limit, last.x + last.r + 2.6 * last.w)
	connector(last.x + last.r + gap * last.w, tailEnd, false)

	-- rings: the outer crescent leaves a mouth facing `open` (+1 toward the tip); the inner sliver sits in that mouth,
	-- clear of the crescent's ends (2026-10-25: a thinner crescent, a wider mouth and a smaller sliver; drawn 1.7x wide
	-- with its halo the old crescent closed into a disc)
	for _, ring in rings do
		local facing = if ring.open > 0 then 0 else math.pi
		local a0, a1 = facing + math.rad(55), facing + math.rad(305)
		table.insert(strokes, trace((a1 - a0) * ring.r, function(t)
			return ring.x + ring.r * math.cos(a0 + (a1 - a0) * t)
		end, function(t)
			return ring.y + ring.r * math.sin(a0 + (a1 - a0) * t)
		end, function(t)
			return ring.w * (0.01 + 0.05 * math.sin(math.pi * t) ^ 0.8)
		end))
		local cx, r2 = ring.x + ring.open * 0.3 * ring.r, 0.42 * ring.r
		local b0, b1 = facing - math.rad(60), facing + math.rad(60)
		table.insert(strokes, trace((b1 - b0) * r2, function(t)
			return cx + r2 * math.cos(b0 + (b1 - b0) * t)
		end, function(t)
			return ring.y + r2 * math.sin(b0 + (b1 - b0) * t)
		end, function(t)
			return ring.w * (0.006 + 0.035 * math.sin(math.pi * t) ^ 0.8)
		end))
	end

	-- accent: a four-point star on the tail, two crossing tapered strokes
	local sx = math.min(tailEnd - 0.6 * widthAt(tailEnd), last.x + last.r + 1.7 * last.w)
	local sw = widthAt(sx)
	local sy, s = 0.5 * sw, 0.2 * sw
	table.insert(strokes, trace(2 * s, function(t)
		return sx
	end, function(t)
		return sy - s + 2 * s * t
	end, function(t)
		return 0.07 * sw * taper(t, 0.5)
	end))
	table.insert(strokes, trace(2.6 * s, function(t)
		return sx - 1.3 * s + 2.6 * s * t
	end, function(t)
		return sy
	end, function(t)
		return 0.07 * sw * taper(t, 0.5)
	end))
	return strokes
end

-- Tide: a ribbon of waves on the edge side of the face. Each crest climbs a long back, peaks, and its face drops
-- into the trough under a curl hooking toward the tip; a thin current runs under each back. Drawn as the ribbon,
-- then the curls, then the currents. At least two crests, so a tanto still reads as waves.
local function tide(length: number, widthAt: (number) -> number, ctx: any): { Stroke }
	local x0, x1, mean = usable(length, widthAt, ctx.limit)
	local n = math.max(2, math.floor((x1 - x0) / (4.4 * mean)))
	local P = (x1 - x0) / n
	local LOW, HIGH = 0.16, 0.74 -- trough and crest, fractions of the width
	local FACE = 1.3 -- the face's run into the trough, in widths
	local start = x0 - 0.5 * widthAt(0)
	local tailEnd = math.min(ctx.limit, x1 + 0.5 * widthAt(x1))
	local crests = {}
	for i = 1, n do
		local xc = x0 + (i - 0.38) * P
		table.insert(crests, { x = xc, w = widthAt(xc), back = math.max(x0 + (i - 1) * P, xc - 3.2 * widthAt(xc)) })
	end
	local function ends(x: number): number -- the ribbon tapers in from its start and out at its tail
		return math.clamp(math.min((x - start) / widthAt(start), (tailEnd - x) / (1.5 * widthAt(x))), 0, 1) ^ 0.7
	end
	local ribbon: Stroke = {}
	local at = start
	local function trough(xb: number)
		local xa = at
		if xb - xa > 0.05 then
			extend(ribbon, trace(xb - xa, function(t)
				return xa + (xb - xa) * t
			end, function(t)
				return LOW * widthAt(xa + (xb - xa) * t)
			end, function(t)
				local x = xa + (xb - xa) * t
				return 0.028 * widthAt(x) * ends(x)
			end))
		end
		at = xb
	end
	for _, c in crests do
		trough(c.back)
		local xa, xc = c.back, c.x
		-- the back: rising slowly, then steeply into the crest, thickening as it climbs
		extend(ribbon, trace(1.1 * (xc - xa), function(t)
			return xa + (xc - xa) * t
		end, function(t)
			return (LOW + (HIGH - LOW) * t ^ 3) * widthAt(xa + (xc - xa) * t)
		end, function(t)
			local x = xa + (xc - xa) * t
			return (0.028 + 0.04 * t ^ 1.5) * widthAt(x) * ends(x)
		end))
		-- the face: straight down from the crest (the wave's hollow), then out along the trough
		local function faceX(t: number): number
			return xc + FACE * c.w * (1 - math.cos(t * math.pi / 2)) ^ 1.6
		end
		extend(ribbon, trace(1.4 * FACE * c.w, faceX, function(t)
			return (HIGH - (HIGH - LOW) * math.sin(t * math.pi / 2)) * widthAt(faceX(t))
		end, function(t)
			return (0.068 - 0.04 * t) * widthAt(faceX(t)) * ends(faceX(t))
		end))
		at = faceX(1)
	end
	trough(tailEnd)
	local strokes: { Stroke } = { ribbon }
	-- the curls: from each crest, forward over the hollow and down round a tightening turn to a claw
	for _, c in crests do
		local w = c.w
		local RX, RY, A0, A1 = 0.26 * w, 0.2 * w, math.rad(115), math.rad(-50)
		local cx, cy = c.x - RX * math.cos(A0), HIGH * w - RY * math.sin(A0)
		table.insert(strokes, trace((A0 - A1) * RX * 0.8, function(t)
			return cx + RX * (1 - 0.35 * t) * math.cos(A0 + (A1 - A0) * t)
		end, function(t)
			return cy + RY * (1 - 0.35 * t) * math.sin(A0 + (A1 - A0) * t)
		end, function(t)
			return w * (0.006 + 0.064 * (1 - t) ^ 0.9)
		end))
	end
	-- the currents: thin lines under the upper part of each back
	for _, c in crests do
		local xa, xc = c.back, c.x
		table.insert(strokes, trace(0.6 * (xc - xa), function(t)
			return xa + (xc - xa) * (0.4 + 0.52 * t)
		end, function(t)
			local s = 0.4 + 0.52 * t
			return (LOW + (HIGH - LOW) * s ^ 3 - 0.12) * widthAt(xa + (xc - xa) * s)
		end, function(t)
			return 0.022 * c.w * math.sin(math.pi * t) ^ 0.8
		end))
	end
	return strokes
end

-- Stormroot: a jagged trunk zigzagging along the middle of the face, thick at the guard and thinning to a point,
-- with angular branches forking outward and forward. Drawn trunk first, then each branch with its twig.
-- 2026-10-25: the trunk swells in from a narrow root instead of starting as a round blob, and is slimmer; branches are
-- a third of the trunk's width where they leave it, so trunk and branches read apart.
local function stormroot(length: number, widthAt: (number) -> number, ctx: any): { Stroke }
	local _, x1 = usable(length, widthAt, ctx.limit)
	local xs, xe = 0.4 * widthAt(0), x1 + 0.3 * widthAt(x1)
	local turns = {} -- { x, y } cm
	local x, k = xs, 0
	while x < xe do
		local w = widthAt(x)
		local side = if k % 2 == 0 then -1 else 1
		table.insert(turns, { x, (if k == 0 then 0.5 else 0.5 + side * (0.1 + 0.12 * hash(k))) * w })
		x += w * (0.8 + 0.5 * hash(k + 50))
		k += 1
	end
	table.insert(turns, { xe, 0.5 * widthAt(xe) })
	local function thick(px: number): number -- the trunk's half-width
		local u = math.clamp((px - xs) / (xe - xs), 0, 1)
		local w = widthAt(px)
		local root = math.clamp((px - xs) / (1.2 * w), 0, 1) ^ 0.7
		return w * (0.022 + 0.05 * (1 - u) ^ 1.3) * (0.35 + 0.65 * root) * math.clamp((xe - px) / w, 0, 1) ^ 0.6
	end
	local trunk: Stroke = {}
	for i, p in turns do
		table.insert(trunk, { p[1], p[2], thick(p[1]) * (0.85 + 0.3 * hash(i + 70)) })
		local q = turns[i + 1]
		if q then -- a kink between turns, off the straight line
			local f = 0.4 + 0.2 * hash(i + 90)
			local mx, my = p[1] + (q[1] - p[1]) * f, p[2] + (q[2] - p[2]) * f
			table.insert(trunk, { mx, my + (hash(i + 110) - 0.5) * 0.12 * widthAt(mx), thick(mx) * (0.8 + 0.3 * hash(i + 130)) })
		end
	end
	local strokes: { Stroke } = { trunk }
	-- a branch: two straight runs bending outward, tapering to a point, shortened to stay on the face
	local function branch(px: number, py: number, h0: number, side: number, angle: number, len: number, seed: number): Stroke?
		local w = widthAt(px)
		local bend = angle + side * (hash(seed) - 0.3) * 0.5
		local reachY = (math.sin(angle) + math.sin(bend)) * 0.5 * len
		local room = (if side > 0 then 0.88 * w - py else py - 0.12 * w) / math.abs(reachY)
		len *= math.min(1, room)
		if len < 0.12 * w then
			return nil
		end
		local bx, by = px + math.cos(angle) * 0.5 * len, py + math.sin(angle) * 0.5 * len
		return { { px, py, h0 }, { bx, by, 0.55 * h0 }, { bx + math.cos(bend) * 0.5 * len, by + math.sin(bend) * 0.5 * len, 0 } }
	end
	for j = 2, #trunk - 1 do
		local p = trunk[j]
		local w = widthAt(p[1])
		if hash(j + 150) > 0.25 then
			local side = if p[2] > 0.5 * w then 1 else -1
			if hash(j + 170) < 0.25 then
				side = -side
			end
			local u = math.clamp((p[1] - xs) / (xe - xs), 0, 1)
			local angle = side * (0.5 + 0.5 * hash(j + 190))
			local b = branch(p[1], p[2], 0.34 * p[3], side, angle, w * (0.3 + 0.35 * hash(j + 200)) * (1 - 0.4 * u), j + 210)
			if b then
				table.insert(strokes, b)
				local twig = branch(b[2][1], b[2][2], 0.6 * b[2][3], side, side * math.min(math.abs(angle) + 0.55, 1.3), 0.45 * math.sqrt((b[3][1] - p[1]) ^ 2 + (b[3][2] - p[2]) ^ 2), j + 230)
				if twig and hash(j + 250) > 0.35 then
					table.insert(strokes, twig)
				end
			end
		end
	end
	return strokes
end

-- Woven Wind: two ribbons twisting round each other along the face, widest where they cross the middle and narrow
-- at the turns. At each crossing one passes over and the other breaks into tapered points round it, alternating,
-- so they read as woven. Drawn first ribbon, then second.
-- 2026-10-25: the break is sized for the ribbon as drawn (EtchCanvas.THICK times wider, plus half its halo), so the
-- crossing keeps a clear gap.
local function wovenWind(length: number, widthAt: (number) -> number, ctx: any): { Stroke }
	local x0, x1, mean = usable(length, widthAt, ctx.limit)
	local n = math.max(1, math.floor((x1 - x0) / (7 * mean) + 0.5)) -- full twists
	local P = (x1 - x0) / n
	local A, GAP = 0.32, 0.04 -- swing either side of the middle, clear gap at a crossing (fractions of the width)
	local halo = EtchCanvas.halo(mean)
	local function phase(x: number): number
		return 2 * math.pi * (x - x0) / P + math.pi / 2
	end
	local function half(x: number): number
		return widthAt(x) * (0.028 + 0.055 * math.abs(math.cos(phase(x))))
	end
	local strokes: { Stroke } = {}
	for rib = 1, 2 do
		local sign = if rib == 1 then 1 else -1
		-- where this ribbon goes under: every other crossing, clear of the other ribbon by GAP
		local cuts = {}
		for j = 1, 2 * n do
			if j % 2 + 1 == rib then
				local xc = x0 + P / 4 + (j - 1) * P / 2
				local w = widthAt(xc)
				local m = A * w * 2 * math.pi / P -- each ribbon's slope there
				local d = (EtchCanvas.THICK * half(xc) + 0.5 * halo + GAP * w) * math.sqrt(1 + m * m) / (2 * m)
				table.insert(cuts, { xc - d, xc + d })
			end
		end
		local runs, from = {}, x0
		for _, cut in cuts do
			table.insert(runs, { from, cut[1] })
			from = cut[2]
		end
		table.insert(runs, { from, x1 })
		for _, run in runs do
			local a, b = run[1], run[2]
			local ta = if a == x0 then 1.2 else 0.5 -- taper into a point: long at the ribbon's ends, short at a gap
			local tb = if b == x1 then 1.2 else 0.5
			table.insert(strokes, trace(1.2 * (b - a), function(t)
				return a + (b - a) * t
			end, function(t)
				local x = a + (b - a) * t
				return widthAt(x) * (0.5 + sign * A * math.sin(phase(x)))
			end, function(t)
				local x = a + (b - a) * t
				local w = widthAt(x)
				return half(x) * math.clamp(math.min((x - a) / (ta * w), (b - x) / (tb * w)), 0, 1) ^ 0.8
			end))
		end
	end
	return strokes
end

-- The part of a convex polygon ({ x, y } points) where nx * x + ny * y <= c.
local function clip(poly: { { number } }, nx: number, ny: number, c: number): { { number } }
	local out = {}
	for i, a in poly do
		local b = poly[i % #poly + 1]
		local da, db = nx * a[1] + ny * a[2] - c, nx * b[1] + ny * b[2] - c
		if da <= 0 then
			table.insert(out, a)
		end
		if (da <= 0) ~= (db <= 0) then
			local t = da / (da - db)
			table.insert(out, { a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t })
		end
	end
	return out
end

-- A convex polygon shrunk by g on every side (a fault's half-width).
local function inset(poly: { { number } }, g: number): { { number } }
	local area = 0
	for i, a in poly do
		local b = poly[i % #poly + 1]
		area += a[1] * b[2] - b[1] * a[2]
	end
	local s = if area > 0 then 1 else -1
	local out = poly
	for i, a in poly do
		local b = poly[i % #poly + 1]
		local dx, dy = b[1] - a[1], b[2] - a[2]
		local len = math.sqrt(dx * dx + dy * dy)
		if len > 1e-6 then
			local nx, ny = s * dy / len, -s * dx / len -- outward
			out = clip(out, nx, ny, nx * a[1] + ny * a[2] - g)
		end
	end
	return out
end

-- A filled shard: the guide zigzags across it from its hilt end to its tip end (Shared/EtchCanvas reveals the
-- shape behind it). `ink` is its crisp dark border.
local function shard(poly: { { number } }, widthAt: (number) -> number, ink: any): Stroke
	local xmin, xmax = math.huge, -math.huge
	for _, p in poly do
		xmin, xmax = math.min(xmin, p[1]), math.max(xmax, p[1])
	end
	local function span(x: number): (number, number) -- the shard's lowest and highest y at x
		local lo, hi = math.huge, -math.huge
		for i, a in poly do
			local b = poly[i % #poly + 1]
			if (a[1] - x) * (b[1] - x) <= 0 and a[1] ~= b[1] then
				local y = a[2] + (b[2] - a[2]) * (x - a[1]) / (b[1] - a[1])
				lo, hi = math.min(lo, y), math.max(hi, y)
			end
		end
		return lo, hi
	end
	local m = math.max(2, math.ceil((xmax - xmin) / (0.14 * widthAt((xmin + xmax) / 2))))
	local pts: Stroke = {}
	for k = 0, m do
		local x = xmin + (xmax - xmin) * k / m
		local lo, hi = span(x)
		if lo > hi then
			lo, hi = poly[1][2], poly[1][2]
		end
		local inner = 0.2 * (hi - lo)
		table.insert(pts, { x, if k % 2 == 0 then lo + inner else hi - inner, 0 })
	end
	(pts :: any).fill = poly;
	(pts :: any).ink = ink
	return pts
end

-- Fracture: one connected band of angular shards split by clean dark faults, broad panels at the guard (often split
-- along a diagonal) shrinking steadily into diamonds and slivers toward the tip as the band narrows. Faults lean
-- either way; one stands upright on each seam between the canvas's strips (Shared/EtchCanvas.strips), so no shard is
-- cut by it. Each shard has a crisp dark border half a fault wide (EtchCanvas `ink`), so the faults are solid dark
-- gaps and the band has a clean edge. The tool scribbles over each shard, guard end first.
-- 2026-10-25: was scattered tiles (corners sliding far along the faults, shards missing, diamonds from mid-blade) with
-- a soft halo; on the zanbato a few huge panels, an empty stretch and one fragment.
local function fracture(length: number, widthAt: (number) -> number, ctx: any): { Stroke }
	local _, x1 = usable(length, widthAt, ctx.limit)
	local xs, xe = 0.4 * widthAt(0), x1 + 0.3 * widthAt(x1)
	local GAP = 0.06 -- fault width, fraction of the width
	local strips = ctx.strips
	local at, upright, seam = { xs }, { false }, 1
	while at[#at] < xe do
		local x = at[#at]
		local w = widthAt(x)
		local u = math.clamp((x - xs) / (xe - xs), 0, 1)
		local nextX = math.min(xe, x + w * (1.5 - 0.95 * u) * (0.85 + 0.3 * hash(#at - 1)))
		while seam < strips and seam * length / strips <= x + 0.4 * w do
			seam += 1
		end
		local s = seam * length / strips
		local snap = seam < strips and s < xe and s <= nextX + 0.4 * w
		if snap then
			seam += 1
		end
		table.insert(at, if snap then s else nextX)
		table.insert(upright, snap)
	end
	-- no sliver of a cell at the end: the last fault takes the one before's place
	if #at > 2 and at[#at] - at[#at - 1] < 0.35 * widthAt(at[#at]) and not upright[#at - 1] then
		table.remove(at, #at - 1)
		table.remove(upright, #upright - 1)
	end
	local faults = {} -- each { bottom x, bottom y, top x, top y }
	for k, x in at do
		local u = math.clamp((x - xs) / (xe - xs), 0, 1)
		local w = widthAt(x)
		local halfH = (0.38 - 0.2 * u) * w
		-- leaning, but never into a neighbour
		local room = 0.35 * math.min(if at[k - 1] then x - at[k - 1] else math.huge, if at[k + 1] then at[k + 1] - x else math.huge)
		local lean = if upright[k] then 0 else (if hash(k + 309) > 0.5 then 1 else -1) * math.min(room, (0.4 + 0.5 * hash(k + 299)) * halfH)
		table.insert(faults, { x - lean, 0.5 * w - halfH, x + lean, 0.5 * w + halfH })
	end
	local strokes: { Stroke } = {}
	for i = 1, #faults - 1 do
		local f, g = faults[i], faults[i + 1]
		local function on(fl: { number }, t: number): { number } -- a point along a fault, bottom (0) to top (1)
			return { fl[1] + (fl[3] - fl[1]) * t, fl[2] + (fl[4] - fl[2]) * t }
		end
		local u = (f[1] - xs) / (xe - xs)
		-- corners slide a little along the faults, so the band's edge is broken but stays one band
		local quad = { on(f, 0.08 * hash(i + 500)), on(g, 0.08 * hash(i + 510)), on(g, 1 - 0.08 * hash(i + 520)), on(f, 1 - 0.08 * hash(i + 530)) }
		-- in the last third the cells turn to diamonds, pointed at both faults
		local diamond = u > 0.62 and hash(i + 540) > 0.4
		if diamond then
			local function between(t: number, s: number): { number } -- along the band's bottom (0) or top (1) edge
				local a, b = on(f, t), on(g, t)
				return { a[1] + (b[1] - a[1]) * s, a[2] + (b[2] - a[2]) * s }
			end
			quad = { on(f, 0.4 + 0.2 * hash(i + 550)), between(0, 0.35 + 0.3 * hash(i + 560)), on(g, 0.4 + 0.2 * hash(i + 570)), between(1, 0.35 + 0.3 * hash(i + 580)) }
		end
		local w = widthAt((f[1] + g[3]) / 2)
		local pieces = { quad }
		if not diamond and u < 0.62 and hash(i + 400) > 0.3 and (g[1] - f[1]) > 0.7 * w then
			-- split along a diagonal fault, low on one side and high on the other
			local low, high = 0.2 + 0.2 * hash(i + 410), 0.6 + 0.2 * hash(i + 420)
			if hash(i + 430) > 0.5 then
				low, high = high, low
			end
			local p, q = on(f, low), on(g, high)
			local nx, ny = -(q[2] - p[2]), q[1] - p[1]
			local c = nx * p[1] + ny * p[2]
			pieces = { clip(quad, -nx, -ny, -c), clip(quad, nx, ny, c) }
		end
		local ink = { solid = 0.5 * GAP * w, fade = 0.012 * w }
		for p, piece in pieces do
			local poly = inset(piece, 0.5 * GAP * w)
			if #poly >= 3 and not (u > 0.88 and hash(i * 3 + p + 600) > 0.6) then -- one or two dropped right at the end
				table.insert(strokes, shard(poly, widthAt, ink))
			end
		end
	end
	return strokes
end

-- Falling Stars: a few bright four-point stars dropping toward the tip and the edge, each trailing three thin tapered
-- streaks back toward the guard and up toward the spine, the middle one longest. The star carries the pattern; the
-- trails are a third of its rays' width with half the halo. Drawn per star: the star, then its trails.
-- 2026-10-25: the trails were thick leaf shapes falling ahead of the stars, as heavy as the stars themselves.
local function fallingStars(length: number, widthAt: (number) -> number, ctx: any): { Stroke }
	local x0, x1, mean = usable(length, widthAt, ctx.limit)
	local n = math.max(2, math.floor((x1 - x0) / (5.5 * mean) + 0.5)) -- at least two, so a tanto isn't half bare
	local seg = (x1 - x0) / n
	local thin = { solid = 0, fade = 0.5 * EtchCanvas.halo(mean) }
	local strokes: { Stroke } = {}
	local function line(ax: number, ay: number, bx: number, by: number, h: number, peak: number)
		table.insert(strokes, trace(math.sqrt((bx - ax) ^ 2 + (by - ay) ^ 2), function(t)
			return ax + (bx - ax) * t
		end, function(t)
			return ay + (by - ay) * t
		end, function(t)
			return h * spike(t, peak)
		end))
	end
	for i = 1, n do
		local xs = x0 + i * seg - 0.45 * widthAt(x0 + i * seg)
		local w = widthAt(xs)
		local ys = (if i % 2 == 1 then 0.47 else 0.52) * w
		-- the star: long upright and lengthwise rays crossing in a bright core, two short diagonals (big enough to read
		-- on a held sword at phone size)
		line(xs, ys - 0.36 * w, xs, ys + 0.36 * w, 0.085 * w, 0.5)
		line(xs - 0.4 * w, ys, xs + 0.4 * w, ys, 0.085 * w, 0.5)
		line(xs - 0.17 * w, ys - 0.17 * w, xs + 0.17 * w, ys + 0.17 * w, 0.035 * w, 0.5)
		line(xs - 0.17 * w, ys + 0.17 * w, xs + 0.17 * w, ys - 0.17 * w, 0.035 * w, 0.5)
		-- the trails: from just behind the star, rising away from it, thickest there and fading out
		local L = math.max(w, math.min(2.6 * w, seg - 0.9 * w))
		for k = -1, 1 do
			local len = L * (if k == 0 then 1 elseif k < 0 then 0.75 else 0.55)
			local ax, ay = xs - 0.44 * w, ys + 0.05 * k * w
			local rise = (0.18 + 0.06 * k) * w * len / L
			local trail = trace(len, function(t)
				return ax - len * t
			end, function(t)
				return ay + rise * t
			end, function(t)
				return 0.022 * w * (1 - t) ^ 1.3 * math.min(1, t / 0.06)
			end);
			(trail :: any).ink = thin
			table.insert(strokes, trail)
		end
	end
	return strokes
end

EtchPatterns.STROKED = {
	Eclipse = eclipse,
	Tide = tide,
	Stormroot = stormroot,
	WovenWind = wovenWind,
	Fracture = fracture,
	FallingStars = fallingStars,
} :: { [string]: (number, (number) -> number, any) -> { Stroke } }

-- Where a sloped tip begins: the first place past 40% of the blade where the width falls faster than SLOPE cm per cm
-- (the zanbato's chisel, the gladius' long point, a katana's kissaki), else short of the tip as before.
local SLOPE = 0.25
local function limitOf(length: number, widthAt: (number) -> number): number
	local limit = length - 1.1 * widthAt(length * 0.95)
	local step = 0.25
	local x = 0.4 * length
	while x + step < limit do
		if widthAt(x) - widthAt(x + step) > SLOPE * step then
			return x
		end
		x += step
	end
	return limit
end

-- The strokes of a pattern on a blade of this length (cm) and width (cm at x), or nil if it isn't stroked.
-- Generators see the width capped at EtchCanvas.MOTIF_CM; on a wider face their strokes are moved to its middle.
function EtchPatterns.strokes(id: string, length: number, widthAt: (number) -> number): { Stroke }?
	local make = EtchPatterns.STROKED[id]
	if not make then
		return nil
	end
	local cap = EtchCanvas.MOTIF_CM
	local function capped(x: number): number
		return math.min(widthAt(x), cap)
	end
	local strokes = make(length, capped, { limit = limitOf(length, widthAt), strips = EtchCanvas.strips(length, widthAt) })
	local moved = {} -- clipped shards can share corner points
	local function shift(p: { number })
		if not moved[p] then
			moved[p] = true
			p[2] += 0.5 * (widthAt(p[1]) - capped(p[1]))
		end
	end
	for _, stroke in strokes do
		for _, p in ipairs(stroke) do -- points only, not the `fill` and `ink` fields
			shift(p)
		end
		for _, p in (stroke :: any).fill or {} do
			shift(p)
		end
	end
	return strokes
end

return EtchPatterns

--!strict
-- The texture of a stroked etch (Shared/EtchPatterns) on one blade, and its progressive reveal (vault: Art/Animated
-- Blade Etching). The blade's face is unrolled into an image: x along the blade, w (0 at the cutting-edge line, 1 at
-- the spine) across it. A long blade is cut into STRIPS rows of STRIP_W x STRIP_H pixels so a pixel is about as long
-- as it is wide on the steel. Shared/BladeEtch maps the image onto the overlay with the same mapping.
--
-- Colours are baked: a MeshPart's Color doesn't tint a texture (checked in Studio 2026-10-21), so each material gets
-- its own image. The body is Flame's dark steel with its cool sheen on the lit bevel, the marks are the material's
-- accent. Edges are anti-aliased by coverage.
-- Strong glow (Allen 2026-10-23, picked from a side-by-side render: "Strong glow"; dark metals' marks were hard to
-- read): strokes are THICK times wider, their core is the accent lifted CORE toward white, they dim only slightly away
-- from the light, and a soft halo of the accent spreads GLOW_CM around every mark (and fill) over the dark body, up to
-- GLOW of the way to the accent. Neon can't do this: the texture overrides it. vault: References/Atmosphere/etch-pop-compare.jpg.
-- Halo by width (2026-10-25, etch refinement): a fixed 0.24 cm halo was most of a tanto's marks and a hairline on the
-- zanbato, so it is now HALO of the blade's mean width (capped at MOTIF_CM, as Shared/EtchPatterns sizes motifs). A
-- stroke may carry `ink = { solid, fade }` (cm): a crisp border, fully dark to `solid` and gone by solid + fade,
-- instead of the soft halo (Fracture's shards, so the faults between them read as clean dark gaps).
--
-- Strokes are cut into short pieces; reveal(d) draws every piece that ends within d cm of pen-down travel. Coverage
-- only ever grows (max per pixel), so any reveal order ends in exactly the same pixels as drawing it all at once:
-- progress 1 is the finished image. at(p) gives the tool's place at progress p, with lifts between strokes.
-- A stroke with a `fill` (a convex polygon of { x, y } cm; 2026-10-22, Fracture's shards) is a filled shape instead:
-- its points are the guide the tool scribbles along (x only increasing), and each piece reveals the shape's columns
-- the guide has passed, with the shape's own anti-aliased edge, so its corners stay sharp.

local AssetService = game:GetService("AssetService")

local Etches = require(script.Parent:WaitForChild("Etches")) :: any

export type Layout = { length: number, strips: number, cols: number, size: Vector2, colW: { number }, colWr: { number } }

local EtchCanvas = {}
EtchCanvas.__index = EtchCanvas

EtchCanvas.STRIP_W, EtchCanvas.STRIP_H = 1024, 128
local STRIP_W, STRIP_H = EtchCanvas.STRIP_W, EtchCanvas.STRIP_H
local PIECE_CM = 0.25 -- longest piece a stroke is cut into (0.1 before the glow: each piece repaints its halo, 2026-10-23)
local LIFT_SPEED = 3 -- the tool travels between strokes this many times faster than it draws
local SHEEN = Color3.fromRGB(150, 190, 230) -- as Shared/BladeEtch: the lit bevel's cool sheen on the dark body
local LEVELS = 64 -- light steps the colours are precomputed for
local SLICE = 0.004 -- seconds of work per frame when a build is spread over frames
local HALO, GLOW, CORE, THICK = 0.07, 0.85, 0.55, 1.7 -- halo reach (fraction of the mean width) and strength, core whitening, stroke width
-- Motifs are sized from the blade's width up to this many cm (Shared/EtchPatterns centres them on a wider face)
EtchCanvas.MOTIF_CM = 7
EtchCanvas.THICK, EtchCanvas.CORE = THICK, CORE

-- The soft halo's reach (cm) on a blade whose capped mean width is `mean`.
function EtchCanvas.halo(mean: number): number
	return HALO * mean
end
-- On a see-through canvas the halo is dark ink instead of the accent (Allen 2026-10-23: the marks "blend in with the
-- texture" and Falling Stars' thin trails looked "misaligned" on bare metal): every mark sits in an engraved groove that
-- reads on any metal or texture.
local INK, INK_ALPHA = { 14, 10, 10 }, 0.95

local alive = 0 -- canvases not yet destroyed (for checks)
-- blank images by layout and body colour: painting one is most of a build, and the Etching Table's pattern picker
-- builds one per pattern on the same blade (2026-10-22); weak, so a blank goes with its layout
local blanks: { [any]: { [string]: buffer } } = setmetatable({}, { __mode = "k" }) :: any

-- A fill polygon as half-planes ex * x + ey * y <= ec (outward normals), and its bounds.
local function shard(poly: { { number } }): any
	local area = 0
	for i, a in poly do
		local b = poly[i % #poly + 1]
		area += a[1] * b[2] - b[1] * a[2]
	end
	local s = if area > 0 then 1 else -1 -- outward is to the right of each edge going counter-clockwise
	local F = { ex = {}, ey = {}, ec = {}, xmin = math.huge, xmax = -math.huge, ymin = math.huge, ymax = -math.huge }
	for i, a in poly do
		local b = poly[i % #poly + 1]
		local dx, dy = b[1] - a[1], b[2] - a[2]
		local len = math.sqrt(dx * dx + dy * dy)
		if len > 1e-9 then
			local nx, ny = s * dy / len, -s * dx / len
			table.insert(F.ex, nx)
			table.insert(F.ey, ny)
			table.insert(F.ec, nx * a[1] + ny * a[2])
		end
		F.xmin, F.xmax = math.min(F.xmin, a[1]), math.max(F.xmax, a[1])
		F.ymin, F.ymax = math.min(F.ymin, a[2]), math.max(F.ymax, a[2])
	end
	return F
end

-- How many strips a blade of this length (cm) and width (cm at x) is cut into. Where two strips meet the texture
-- shows a faint seam one texel wide (it wraps there), so Shared/EtchPatterns keeps broad fills off those lines.
function EtchCanvas.strips(length: number, widthAt: (number) -> number): number
	local mean = 0
	for i = 0, 15 do
		mean += widthAt(length * i / 15) / 16
	end
	return math.clamp(math.floor(length / mean * STRIP_H / STRIP_W + 0.5), 1, 6)
end

-- Blade length (cm), width at x (cm) and ridge crease at x (fraction of the width from the edge) -> image layout.
function EtchCanvas.layout(length: number, widthAt: (number) -> number, ridgeAt: (number) -> number): Layout
	local strips = EtchCanvas.strips(length, widthAt)
	local cols = strips * STRIP_W
	local colW, colWr = table.create(cols), table.create(cols)
	for gc = 0, cols - 1 do
		local x = (gc + 0.5) / cols * length
		colW[gc + 1] = math.max(widthAt(x), 0.05)
		colWr[gc + 1] = ridgeAt(x)
	end
	return { length = length, strips = strips, cols = cols, size = Vector2.new(STRIP_W, strips * STRIP_H), colW = colW, colWr = colWr }
end

-- Where a point (x cm along, w across) lands in the image, as UV (for the overlay mesh). Strip s covers
-- x in [s, s + 1) * length / strips.
function EtchCanvas.uv(L: Layout, x: number, w: number, strip: number): Vector2
	local gx = x / L.length * L.cols - strip * STRIP_W
	return Vector2.new(gx / STRIP_W, (strip + math.clamp(w, 0, 1)) / L.strips)
end

-- body, accent: the dark steel and the material's mark colour (both at full light on the bevel). A body of
-- Etches.CLEAR is see-through (alpha from the marks and their halo), so a textured metal shows around them.
-- `spread`: yield between columns so painting the blank image never holds one frame for long (the Polishing
-- Station fetches the next polish level's etch while you work, 2026-10-21); the show and card art build at once.
function EtchCanvas.new(L: Layout, strokes: { { { number } } }, body: Color3, accent: Color3, spread: boolean?)
	local self = setmetatable({}, EtchCanvas) :: any
	self.L = L
	self.clear = body == Etches.CLEAR
	-- body, mark core and halo colours (0..255) at each light level
	self.bodyLv, self.markLv, self.haloLv = table.create(LEVELS + 1), table.create(LEVELS + 1), table.create(LEVELS + 1)
	for lv = 0, LEVELS do
		local lit = lv / LEVELS
		local b = body:Lerp(SHEEN, 0.2 * lit)
		local h = accent:Lerp(Color3.new(0, 0, 0), 0.12 * (1 - lit))
		local m = h:Lerp(Color3.new(1, 1, 1), CORE) -- a bright core (in its ink groove on a see-through canvas)
		self.bodyLv[lv + 1] = { b.R * 255, b.G * 255, b.B * 255 }
		self.markLv[lv + 1] = { m.R * 255, m.G * 255, m.B * 255 }
		self.haloLv[lv + 1] = { h.R * 255, h.G * 255, h.B * 255 }
	end
	local mean = 0
	for _, w in L.colW do
		mean += math.min(w, EtchCanvas.MOTIF_CM) / L.cols
	end
	self.glowCm = EtchCanvas.halo(mean)
	self.cover = buffer.create(L.cols * STRIP_H) -- coverage 0..255 per pixel, column-major by global column
	self.glow = buffer.create(L.cols * STRIP_H) -- halo 0..255, the same layout
	-- pixels raised since the last flush, painted once there (a halo pixel is raised by many pieces in a row)
	self.pend, self.pendList = buffer.create(L.cols * STRIP_H), {} :: { number }
	self.rgba = buffer.create(STRIP_W * L.strips * STRIP_H * 4)
	-- pieces with the pen-down distance where each ends; moves for the tool (draws and lifts) with their time
	local pieces, moves = {}, {}
	local drawn, time = 0, 0
	local last: { number }? = nil
	for _, stroke in strokes do
		local poly = (stroke :: any).fill
		local fill = if poly then shard(poly) else nil
		local ink = (stroke :: any).ink or { solid = 0, fade = self.glowCm }
		local from = -math.huge -- a fill piece reveals the columns from the previous piece's end up to its own
		local first = stroke[1]
		if last then
			local len = math.sqrt((first[1] - last[1]) ^ 2 + (first[2] - last[2]) ^ 2)
			table.insert(moves, { down = false, a = last, b = first, t0 = time, t1 = time + len / LIFT_SPEED, d0 = drawn, d1 = drawn })
			time += len / LIFT_SPEED
		end
		for i = 1, #stroke - 1 do
			local a, b = stroke[i], stroke[i + 1]
			local len = math.sqrt((b[1] - a[1]) ^ 2 + (b[2] - a[2]) ^ 2)
			local n = math.max(1, math.ceil(len / PIECE_CM))
			for k = 1, n do
				local f0, f1 = (k - 1) / n, k / n
				local pa = { a[1] + (b[1] - a[1]) * f0, a[2] + (b[2] - a[2]) * f0, a[3] + (b[3] - a[3]) * f0 }
				local pb = { a[1] + (b[1] - a[1]) * f1, a[2] + (b[2] - a[2]) * f1, a[3] + (b[3] - a[3]) * f1 }
				if fill then
					local upto = if i == #stroke - 1 and k == n then math.huge else pb[1]
					table.insert(pieces, { fill = fill, x0 = from, x1 = upto, d = drawn + len * f1, ink = ink })
					from = upto
				else
					table.insert(pieces, { a = pa, b = pb, d = drawn + len * f1, ink = ink })
				end
			end
			table.insert(moves, { down = true, a = a, b = b, t0 = time, t1 = time + len, d0 = drawn, d1 = drawn + len })
			drawn += len
			time += len
		end
		last = stroke[#stroke]
	end
	self.pieces, self.moves = pieces, moves
	self.total, self.duration = drawn, time -- cm drawn; time units (cm at drawing speed)
	self.next = 1 -- first piece not yet drawn
	self.revealed = 0
	local byBody = blanks[L] or {}
	blanks[L] = byBody
	local bodyKey = ("%.9g %.9g %.9g"):format(body.R, body.G, body.B)
	local blank = byBody[bodyKey]
	if blank then
		buffer.copy(self.rgba, 0, blank)
	else
		local slice = os.clock()
		for gc = 0, L.cols - 1 do
			for r = 0, STRIP_H - 1 do
				self:_paint(gc, r)
			end
			if spread and os.clock() - slice > SLICE then
				task.wait()
				slice = os.clock()
			end
		end
		blank = buffer.create(buffer.len(self.rgba))
		buffer.copy(blank, 0, self.rgba)
		byBody[bodyKey] = blank
	end
	local ok, image = pcall(AssetService.CreateEditableImage, AssetService, { Size = L.size })
	if not ok or not image then
		error("EtchCanvas: couldn't create the image: " .. tostring(image))
	end
	self.image = image :: EditableImage
	self.image:WritePixelsBuffer(Vector2.zero, L.size, self.rgba)
	alive += 1
	return self
end

-- Bake one pixel's colour from its coverage (global column gc, row r).
function EtchCanvas:_paint(gc: number, r: number)
	local L = self.L
	local w = (r + 0.5) / STRIP_H
	local wr = L.colWr[gc + 1]
	local u = (gc + 0.5) / L.cols
	local along = math.clamp(1 - u / 0.5, 0.25, 1) -- the bevel sheen fades along the blade
	local lit = (if w < wr then (1 - w / wr) ^ 1.4 else 0) * along
	local lv = math.floor(lit * LEVELS + 0.5) + 1
	local b, m, h = self.bodyLv[lv], self.markLv[lv], self.haloLv[lv]
	local i = gc * STRIP_H + r
	local k = buffer.readu8(self.cover, i) / 255
	local g = buffer.readu8(self.glow, i) / 255 * GLOW -- the halo tints the body under the mark
	local r0, g0, b0 = b[1] + (h[1] - b[1]) * g, b[2] + (h[2] - b[2]) * g, b[3] + (h[3] - b[3]) * g
	local alpha = 255
	if self.clear then -- no body: a dark ink halo (the groove) fading out over a see-through ground
		r0, g0, b0 = INK[1], INK[2], INK[3]
		alpha = math.floor(math.max(k, g / GLOW * INK_ALPHA) * 255 + 0.5)
	end
	local o = (((gc // STRIP_W) * STRIP_H + r) * STRIP_W + gc % STRIP_W) * 4
	buffer.writeu8(self.rgba, o, math.floor(r0 + (m[1] - r0) * k + 0.5))
	buffer.writeu8(self.rgba, o + 1, math.floor(g0 + (m[2] - g0) * k + 0.5))
	buffer.writeu8(self.rgba, o + 2, math.floor(b0 + (m[3] - b0) * k + 0.5))
	buffer.writeu8(self.rgba, o + 3, alpha)
end

-- Raise pixel i's coverage to `cover` and its halo for distance d (cm outside the mark), full to `ink.solid` and
-- fading out over `ink.fade`; true if either grew, and then the pixel waits to be painted at the next flush.
function EtchCanvas:_raise(i: number, cover: number, d: number, ink: any): boolean
	local grew = false
	if cover > buffer.readu8(self.cover, i) then
		buffer.writeu8(self.cover, i, cover)
		grew = true
	end
	local f = if d <= ink.solid then 1 else 1 - (d - ink.solid) / ink.fade
	local glow = if f > 0 then math.floor(f * f * 255 + 0.5) else 0
	if glow > buffer.readu8(self.glow, i) then
		buffer.writeu8(self.glow, i, glow)
		grew = true
	end
	if grew and buffer.readu8(self.pend, i) == 0 then
		buffer.writeu8(self.pend, i, 1)
		table.insert(self.pendList, i)
	end
	return grew
end

-- Mark one pixel dirty (strip boxes of changed pixels, pushed by _flush).
local function touch(dirty: { [number]: { number } }, gc: number, r: number)
	local strip, c = gc // STRIP_W, gc % STRIP_W
	local box = dirty[strip]
	if box then
		box[1], box[2], box[3], box[4] = math.min(box[1], c), math.max(box[2], c), math.min(box[3], r), math.max(box[4], r)
	else
		dirty[strip] = { c, c, r, r }
	end
end

-- Raise coverage under one piece (a tapered capsule) and mark the touched pixels dirty.
function EtchCanvas:_piece(p: any, dirty: { [number]: { number } })
	if p.fill then
		self:_fill(p, dirty)
		return
	end
	local L = self.L
	local ax, ay, ah, bx, by, bh = p.a[1], p.a[2], p.a[3] * THICK, p.b[1], p.b[2], p.b[3] * THICK
	local hmax = math.max(ah, bh)
	local pix = L.length / L.cols -- cm per column, the anti-aliasing width
	local ink = p.ink
	local halo = ink.solid + ink.fade
	local reach = hmax + pix + halo
	local gc0 = math.max(0, math.floor((math.min(ax, bx) - reach) / L.length * L.cols))
	local gc1 = math.min(L.cols - 1, math.ceil((math.max(ax, bx) + reach) / L.length * L.cols))
	local dx, dy = bx - ax, by - ay
	local len2 = dx * dx + dy * dy
	for gc = gc0, gc1 do
		local x = (gc + 0.5) / L.cols * L.length
		local W = L.colW[gc + 1]
		local r0 = math.max(0, math.floor((math.min(ay, by) - reach) / W * STRIP_H))
		local r1 = math.min(STRIP_H - 1, math.ceil((math.max(ay, by) + reach) / W * STRIP_H))
		for r = r0, r1 do
			local i = gc * STRIP_H + r
			if buffer.readu8(self.cover, i) < 255 then -- overlapping pieces of a thick stroke find most of it already full
				local y = (r + 0.5) / STRIP_H * W
				local t = if len2 > 0 then math.clamp(((x - ax) * dx + (y - ay) * dy) / len2, 0, 1) else 0
				local ex, ey = ax + dx * t - x, ay + dy * t - y
				local e2, hr = ex * ex + ey * ey, ah + (bh - ah) * t
				local far = hr + halo
				if e2 < far * far then -- the box's corners are past the halo: no sqrt for them
					local d = math.sqrt(e2) - hr
					if self:_raise(i, math.floor(math.clamp(0.5 - d / pix, 0, 1) * 255 + 0.5), d, ink) then
						touch(dirty, gc, r)
					end
				end
			end
		end
	end
end

-- Raise coverage inside a fill piece's shape, over the columns whose centres lie in [x0, x1).
function EtchCanvas:_fill(p: any, dirty: { [number]: { number } })
	local L, F = self.L, p.fill
	local pix = L.length / L.cols + p.ink.solid + p.ink.fade -- the halo reaches past the edge
	local perCm = L.cols / L.length
	local gc0 = math.max(0, math.ceil(math.max(p.x0, F.xmin - pix) * perCm - 0.5))
	local gc1 = math.min(L.cols - 1, math.ceil(math.min(p.x1, F.xmax + pix) * perCm - 0.5) - 1)
	local aa = L.length / L.cols -- the anti-aliasing width
	local ex, ey, ec = F.ex, F.ey, F.ec
	for gc = gc0, gc1 do
		local x = (gc + 0.5) / L.cols * L.length
		local W = L.colW[gc + 1]
		local r0 = math.max(0, math.floor((F.ymin - pix) / W * STRIP_H))
		local r1 = math.min(STRIP_H - 1, math.ceil((F.ymax + pix) / W * STRIP_H))
		for r = r0, r1 do
			local y = (r + 0.5) / STRIP_H * W
			local d = -math.huge -- distance outside the shape (negative inside)
			for e = 1, #ex do
				d = math.max(d, ex[e] * x + ey[e] * y - ec[e])
			end
			local i = gc * STRIP_H + r
			if self:_raise(i, math.floor(math.clamp(0.5 - d / aa, 0, 1) * 255 + 0.5), d, p.ink) then
				touch(dirty, gc, r)
			end
		end
	end
end

-- Draw every piece ending within `dist` cm of pen-down travel (never undraws), and push the changed pixels.
-- `spread`: as EtchCanvas.new, yield between pieces (the image shows nothing new until the end).
function EtchCanvas:reveal(dist: number, spread: boolean?)
	if not self.image then
		return
	end
	local dirty: { [number]: { number } } = {}
	local slice = os.clock()
	while self.next <= #self.pieces and self.pieces[self.next].d <= dist + 1e-6 do
		self:_piece(self.pieces[self.next], dirty)
		self.next += 1
		if spread and os.clock() - slice > SLICE then
			task.wait()
			if not self.image then -- destroyed while waiting
				return
			end
			slice = os.clock()
		end
	end
	self.revealed = math.max(self.revealed, math.min(dist, self.total))
	self:_flush(dirty)
end

-- A band pattern (Flame, Shared/BladeEtch.bandReach): the colour from the edge up to reachAt(x) (as w), drawn
-- column by column from the base up to x cm. Like reveal, it only ever adds.
function EtchCanvas:revealBand(x: number, reachAt: (number) -> number)
	if not self.image then
		return
	end
	local L = self.L
	local from, upto = self.bandNext or 0, math.min(L.cols - 1, math.floor(x / L.length * L.cols))
	local dirty: { [number]: { number } } = {}
	for gc = from, upto do
		local reach = reachAt((gc + 0.5) / L.cols * L.length)
		for r = 0, math.min(STRIP_H - 1, math.ceil(reach * STRIP_H) + 1) do
			local cover = math.floor(math.clamp((reach - (r + 0.5) / STRIP_H) * STRIP_H + 0.5, 0, 1) * 255 + 0.5)
			local i = gc * STRIP_H + r
			if cover > buffer.readu8(self.cover, i) then
				buffer.writeu8(self.cover, i, cover)
				self:_paint(gc, r)
				touch(dirty, gc, r)
			end
		end
	end
	self.bandNext = math.max(from, upto + 1)
	self:_flush(dirty)
end

function EtchCanvas:_flush(dirty: { [number]: { number } })
	for _, i in self.pendList do
		self:_paint(i // STRIP_H, i % STRIP_H)
		buffer.writeu8(self.pend, i, 0)
	end
	table.clear(self.pendList)
	for strip, box in dirty do
		local c0, c1, r0, r1 = box[1], box[2], box[3], box[4]
		local w, h = c1 - c0 + 1, r1 - r0 + 1
		local sub = buffer.create(w * h * 4)
		for r = r0, r1 do
			buffer.copy(sub, (r - r0) * w * 4, self.rgba, ((strip * STRIP_H + r) * STRIP_W + c0) * 4, w * 4)
		end
		self.image:WritePixelsBuffer(Vector2.new(c0, strip * STRIP_H + r0), Vector2.new(w, h), sub)
	end
end

-- The tool at progress p (0..1 of the whole run, lifts included): x and y in cm, whether it's drawing, and the
-- pen-down distance drawn by then.
function EtchCanvas:at(p: number): (number, number, boolean, number)
	local t = math.clamp(p, 0, 1) * self.duration
	for _, m in self.moves do
		if t <= m.t1 then
			local f = if m.t1 > m.t0 then (t - m.t0) / (m.t1 - m.t0) else 1
			return m.a[1] + (m.b[1] - m.a[1]) * f, m.a[2] + (m.b[2] - m.a[2]) * f, m.down, m.d0 + (m.d1 - m.d0) * f
		end
	end
	local m = self.moves[#self.moves]
	return m.b[1], m.b[2], false, self.total
end

-- Show this canvas on an overlay part. A clear canvas needs the part a hair transparent: at Transparency 0 a MeshPart
-- draws its texture opaque and ignores the alpha (checked in Studio 2026-10-23).
function EtchCanvas:wear(part: MeshPart)
	part.TextureContent = Content.fromObject(self.image)
	part.Transparency = if self.clear then 0.02 else 0
end

function EtchCanvas:destroy()
	if self.image then
		self.image:Destroy()
		self.image = nil
		alive -= 1
	end
end

-- For checks: canvases (and their images) still alive.
function EtchCanvas.count(): number
	return alive
end

return EtchCanvas

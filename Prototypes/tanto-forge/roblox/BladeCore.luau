--!strict
-- Blade shape and forging state for Create Swords!. Port of Prototypes/tanto-forge/dist/js/blade-core.js.
-- Pure Luau (no Roblox services), so the same module runs in Studio, on the server for validation,
-- and in the stand-alone Luau CLI tests. Shapes are sampled at a fixed number of stations, so every
-- state shares one vertex layout (stable correspondence for a FixedSize EditableMesh). The whole
-- forging state is { strikeIndex, refinement }: strike progress is replayed from the recipe.
--
-- Indexing: stations, strikes, stages and vertices are 1-based. `strikeIndex` is the number of
-- strikes done (0 … #recipe), as in the JavaScript core.

local BladeCore = {}

-- ---------- types ----------

export type Points = { { number } } -- { { u, value }, ... }, u from 0 (base) to 1 (point)

export type Shape = {
	length: number,
	curve: { sori: number, center: number, spread: number },
	spine: Points,
	edge: Points,
	ridge: Points,
	thickness: Points,
	edgeThickness: Points,
	spineThickness: Points,
}

export type Strike = {
	stage: string,
	u: number,
	radius: number,
	side: string,
	flip: boolean,
	turn: number?,
}

export type Spec = { nagasa: number?, sori: number? }

export type Profile = {
	id: string,
	name: string,
	version: number,
	stations: number,
	tang: { length: number, width: number }?,
	spec: Spec?,
	stages: { lengthened: Shape, preform: Shape, refined: Shape },
	forgedAllowance: { edge: number, edgeThickness: number },
	recipe: { Strike },
}

-- Per-station parameters, keyed by PARAMS names.
export type Params = { [string]: { number } }

export type RecipeStrike = Strike & { stageIndex: number }

export type Blade = {
	id: string,
	name: string,
	version: number,
	stations: number,
	shapes: { Params }, -- 1 blank, 2 lengthened, 3 preform, 4 forged (90%), 5 refined (100%)
	recipe: { RecipeStrike },
	contrib: { { number } },
	minCoverage: { number },
	lastStrikeOfStage: { number },
	grindWeight: { number },
	grindWeightTotal: number,
	length: number,
	tang: { length: number, width: number },
	profile: Profile,
	blank: Shape,
}

export type State = {
	strikeIndex: number,
	progress: { { number } },
	refinement: { number },
	lastResidual: number,
}

export type Target = {
	station: number,
	point: { number }, -- blade-local x, y, z (x along the blade, y through the thickness, z = -planeY)
	angle: number,
	thickness: number,
	halfWidth: number,
	flip: boolean,
	turn: number,
	stage: string,
}

export type SavedState = {
	blade: string,
	version: number,
	strikeIndex: number,
	totalStrikes: number,
	refinement: { number },
	quality: number,
}

export type CheckResult = { name: string, ok: boolean, detail: string }

BladeCore.STAGES = { "lengthen", "taper", "tip" }
BladeCore.PARAMS = { "segLen", "bend", "spine", "edge", "ridge", "thick", "edgeT", "spineT" }
BladeCore.RING = 12 -- vertices per station, see buildPositions
BladeCore.FORGED_QUALITY = 90
BladeCore.MAX_QUALITY = 100
-- Refinement per centimetre of stone travel along the edge. Exploratory pacing: about four passes.
BladeCore.GRIND_PER_CM = 0.25
-- Half-width of the grinding stone's reach along the blade, in cm, so longer blades take longer passes.
BladeCore.STONE_RADIUS_CM = 1.8

local STAGES = BladeCore.STAGES
local PARAMS = BladeCore.PARAMS
local RING = BladeCore.RING

local function stageIndexOf(name: string): number?
	return table.find(STAGES, name)
end

local function zeros(n: number): { number }
	return table.create(n, 0)
end

local function isFinite(x: number): boolean
	return x == x and x ~= math.huge and x ~= -math.huge
end

local function roundTo(x: number, step: number): number
	return math.floor(x / step + 0.5) * step
end

-- ---------- curves ----------

-- Monotone cubic (Fritsch–Carlson) through { { u, v }, ... }; flat outside the first and last point.
function BladeCore.makeCurve(points: Points): (number) -> number
	local n = #points
	local xs, ys = table.create(n, 0), table.create(n, 0)
	for k, p in points do
		xs[k], ys[k] = p[1], p[2]
	end
	if n == 1 then
		local only = ys[1]
		return function(_u: number): number
			return only
		end
	end
	local d = table.create(n - 1, 0)
	for k = 1, n - 1 do
		d[k] = (ys[k + 1] - ys[k]) / (xs[k + 1] - xs[k])
	end
	local m = table.create(n, 0)
	m[1] = d[1]
	m[n] = d[n - 1]
	for k = 2, n - 1 do
		m[k] = if d[k - 1] * d[k] <= 0 then 0 else (d[k - 1] + d[k]) / 2
	end
	for k = 1, n - 1 do
		if d[k] == 0 then
			m[k], m[k + 1] = 0, 0
		else
			local a, b = m[k] / d[k], m[k + 1] / d[k]
			local s = a * a + b * b
			if s > 9 then
				local t = 3 / math.sqrt(s)
				m[k], m[k + 1] = t * a * d[k], t * b * d[k]
			end
		end
	end
	return function(u: number): number
		if u <= xs[1] then
			return ys[1]
		end
		if u >= xs[n] then
			return ys[n]
		end
		local k = 1
		while u > xs[k + 1] do
			k += 1
		end
		local h = xs[k + 1] - xs[k]
		local t = (u - xs[k]) / h
		local t2, t3 = t * t, t * t * t
		return (2 * t3 - 3 * t2 + 1) * ys[k]
			+ (t3 - 2 * t2 + t) * h * m[k]
			+ (-2 * t3 + 3 * t2) * ys[k + 1]
			+ (t3 - t2) * h * m[k + 1]
	end
end

local function falloff(distance: number, radius: number): number
	local x = math.abs(distance) / radius
	return if x >= 1 then 0 else 0.5 * (1 + math.cos(math.pi * x))
end

-- ---------- shapes ----------

-- Samples one stage shape at every station into per-parameter arrays.
function BladeCore.sampleShape(shape: Shape, stations: number): Params
	local out: Params = {}
	for _, p in PARAMS do
		out[p] = zeros(stations)
	end
	local curves = {
		spine = BladeCore.makeCurve(shape.spine),
		edge = BladeCore.makeCurve(shape.edge),
		ridge = BladeCore.makeCurve(shape.ridge),
		thick = BladeCore.makeCurve(shape.thickness),
		edgeT = BladeCore.makeCurve(shape.edgeThickness),
		spineT = BladeCore.makeCurve(shape.spineThickness),
	}
	local segLen = shape.length / (stations - 1)
	-- Curvature (sori) is spread over the segments with a gaussian around `center`.
	local sori, center, spread = shape.curve.sori, shape.curve.center, shape.curve.spread
	local density = zeros(stations - 1)
	local total = 0
	for i = 1, stations - 1 do
		local mid = (i - 0.5) / (stations - 1)
		local w = math.exp(-(((mid - center) / spread) ^ 2))
		density[i] = w
		total += w
	end
	for i = 1, stations do
		local u = (i - 1) / (stations - 1)
		out.segLen[i] = if i < stations then segLen else 0
		out.bend[i] = if i < stations then (sori * density[i]) / total else 0
		out.spine[i] = curves.spine(u)
		out.edge[i] = curves.edge(u)
		out.ridge[i] = curves.ridge(u)
		out.thick[i] = curves.thick(u)
		out.edgeT[i] = curves.edgeT(u)
		out.spineT[i] = curves.spineT(u)
	end
	return out
end

local function copyParams(params: Params): Params
	local out: Params = {}
	for _, p in PARAMS do
		out[p] = table.clone(params[p])
	end
	return out
end

-- The 90% shape: the refined blade plus a small edge allowance and a duller edge.
local function forgedFrom(refined: Params, allowance: { edge: number, edgeThickness: number }): Params
	local out = copyParams(refined)
	for i = 1, #out.edge do
		out.edge[i] -= allowance.edge
		out.edgeT[i] += allowance.edgeThickness
	end
	return out
end

-- ---------- blade definition ----------

function BladeCore.createBlade(blank: Shape, profile: Profile): Blade
	local N = profile.stations
	local refined = BladeCore.sampleShape(profile.stages.refined, N)
	-- Each forging stage moves from shapes[s] to shapes[s + 1]; grinding is 4 → 5.
	local shapes = {
		BladeCore.sampleShape(blank, N),
		BladeCore.sampleShape(profile.stages.lengthened, N),
		BladeCore.sampleShape(profile.stages.preform, N),
		forgedFrom(refined, profile.forgedAllowance),
		refined,
	}

	-- Normalise each strike's falloff by the stage's total coverage, so every station reaches
	-- exactly 100% of its stage change on the stage's last strike: no catch-up snap.
	local recipe: { RecipeStrike } = {}
	for k, s in profile.recipe do
		local si = stageIndexOf(s.stage)
		if not si then
			error(`strike {k}: unknown stage "{s.stage}"`)
		end
		if k > 1 and si < recipe[k - 1].stageIndex then
			error(`strike {k}: stages out of order`)
		end
		recipe[k] = {
			stage = s.stage, u = s.u, radius = s.radius, side = s.side, flip = s.flip, turn = s.turn,
			stageIndex = si,
		}
	end
	local coverage = { zeros(N), zeros(N), zeros(N) }
	local raw: { { number } } = {}
	for k, s in recipe do
		local w = zeros(N)
		for i = 1, N do
			w[i] = falloff((i - 1) / (N - 1) - s.u, s.radius)
			coverage[s.stageIndex][i] += w[i]
		end
		raw[k] = w
	end
	local minCoverage = {}
	for si, c in coverage do
		local lowest = math.huge
		for _, v in c do
			lowest = math.min(lowest, v)
		end
		minCoverage[si] = lowest
		if not (lowest > 0.15) then
			error(`stage "{STAGES[si]}" leaves part of the blade unshaped (min coverage {string.format("%.3f", lowest)})`)
		end
	end
	local contrib: { { number } } = {}
	for k, w in raw do
		local c = zeros(N)
		local cov = coverage[recipe[k].stageIndex]
		for i = 1, N do
			c[i] = w[i] / cov[i]
		end
		contrib[k] = c
	end
	local lastStrikeOfStage = { 0, 0, 0 }
	for k, s in recipe do
		lastStrikeOfStage[s.stageIndex] = k
	end

	-- Grinding work is weighted by how much excess metal each station carries.
	local grindWeight = zeros(N)
	local grindWeightTotal = 0
	for i = 1, N do
		local len = if i < N then refined.segLen[i] else refined.segLen[N - 1] / 2
		grindWeight[i] = len
			* (math.abs(shapes[4].edge[i] - refined.edge[i]) + math.abs(shapes[4].edgeT[i] - refined.edgeT[i]))
		grindWeightTotal += grindWeight[i]
	end

	local length = 0
	for _, v in refined.segLen do
		length += v
	end
	local tang = { length = 6, width = 1.8 }
	if profile.tang then
		tang = { length = profile.tang.length, width = profile.tang.width }
	end

	return {
		id = profile.id,
		name = profile.name,
		version = profile.version,
		stations = N,
		shapes = shapes,
		recipe = recipe,
		contrib = contrib,
		minCoverage = minCoverage,
		lastStrikeOfStage = lastStrikeOfStage,
		grindWeight = grindWeight,
		grindWeightTotal = grindWeightTotal,
		length = length,
		tang = tang,
		profile = profile,
		blank = blank,
	}
end

-- ---------- state ----------

function BladeCore.createState(blade: Blade): State
	return {
		strikeIndex = 0,
		progress = { zeros(blade.stations), zeros(blade.stations), zeros(blade.stations) },
		refinement = zeros(blade.stations),
		lastResidual = 0,
	}
end

function BladeCore.totalStrikes(blade: Blade): number
	return #blade.recipe
end

function BladeCore.isForged(blade: Blade, state: State): boolean
	return state.strikeIndex >= #blade.recipe
end

function BladeCore.isRefined(blade: Blade, state: State): boolean
	if not BladeCore.isForged(blade, state) then
		return false
	end
	for _, r in state.refinement do
		if r ~= 1 then
			return false
		end
	end
	return true
end

local function cloneState(state: State): State
	return {
		strikeIndex = state.strikeIndex,
		progress = { table.clone(state.progress[1]), table.clone(state.progress[2]), table.clone(state.progress[3]) },
		refinement = table.clone(state.refinement),
		lastResidual = state.lastResidual,
	}
end

-- One hammer strike. Returns a new state, or nil when forging is already complete.
function BladeCore.applyStrike(blade: Blade, state: State): State?
	local k = state.strikeIndex + 1
	if k > #blade.recipe then
		return nil
	end
	local nextState = cloneState(state)
	local s = blade.recipe[k]
	local g = nextState.progress[s.stageIndex]
	local c = blade.contrib[k]
	for i = 1, #g do
		g[i] += c[i]
	end
	nextState.lastResidual = 0
	if blade.lastStrikeOfStage[s.stageIndex] == k then
		-- Normalisation already sums to 1; this only removes floating-point dust.
		for i = 1, #g do
			nextState.lastResidual = math.max(nextState.lastResidual, math.abs(1 - g[i]))
			g[i] = 1
		end
	else
		for i = 1, #g do
			g[i] = math.min(1, g[i])
		end
	end
	nextState.strikeIndex = k
	return nextState
end

-- Safe grinding at position u (0 base … 1 point). Only works after forging; refinement only rises
-- and clamps at 1, so the blade can never be cut past the refined shape.
function BladeCore.applyGrind(blade: Blade, state: State, u: number, amount: number, radiusCm: number?): State
	if not BladeCore.isForged(blade, state) or not (amount > 0) or not isFinite(u) or not isFinite(amount) then
		return state
	end
	local radius = (radiusCm or BladeCore.STONE_RADIUS_CM) / blade.length
	local nextState = cloneState(state)
	local N = blade.stations
	for i = 1, N do
		local ui = (i - 1) / (N - 1)
		-- Within one stone width of either end the stone overhangs it, so the end sections are as
		-- easy to finish as the rest.
		local overhang = (u < 2 * radius and ui < u) or (u > 1 - 2 * radius and ui > u)
		local w = if overhang then 1 else falloff(ui - u, radius)
		if w > 0 then
			local r = nextState.refinement[i] + amount * w
			if r >= 0.999 then
				r = 1
			end
			nextState.refinement[i] = math.min(1, math.max(nextState.refinement[i], r))
		end
	end
	return nextState
end

-- Stretches of the edge that still need grinding, as station ranges { start, finish } (inclusive).
function BladeCore.unfinishedRuns(blade: Blade, state: State): { { number } }
	local runs = {}
	if not BladeCore.isForged(blade, state) then
		return runs
	end
	local start: number? = nil
	for i, r in state.refinement do
		if r < 1 and not start then
			start = i
		end
		if r == 1 and start then
			table.insert(runs, { start, i - 1 })
			start = nil
		end
	end
	if start then
		table.insert(runs, { start, blade.stations })
	end
	return runs
end

function BladeCore.quality(blade: Blade, state: State): number
	local strikes = #blade.recipe
	if state.strikeIndex < strikes then
		return (BladeCore.FORGED_QUALITY * state.strikeIndex) / strikes
	end
	local done = 0
	for i = 1, blade.stations do
		done += blade.grindWeight[i] * state.refinement[i]
	end
	return BladeCore.FORGED_QUALITY
		+ (BladeCore.MAX_QUALITY - BladeCore.FORGED_QUALITY) * (done / blade.grindWeightTotal)
end

-- Shown to players: never rounds up to a percentage the blade hasn't earned.
function BladeCore.displayQuality(blade: Blade, state: State): number
	if BladeCore.isRefined(blade, state) then
		return BladeCore.MAX_QUALITY
	end
	return math.floor(BladeCore.quality(blade, state) + 1e-9)
end

-- ---------- shape at a state ----------

-- Current per-station parameters: blank + each stage's change × that station's progress, then the
-- grinding change × refinement.
function BladeCore.stationParams(blade: Blade, state: State): Params
	local shapes = blade.shapes
	local N = blade.stations
	local out: Params = {}
	for _, p in PARAMS do
		local v = table.clone(shapes[1][p])
		for s = 1, 3 do
			local g, a, b = state.progress[s], shapes[s][p], shapes[s + 1][p]
			for i = 1, N do
				if g[i] ~= 0 then
					v[i] += (b[i] - a[i]) * g[i]
				end
			end
		end
		local r, a, b = state.refinement, shapes[4][p], shapes[5][p]
		for i = 1, N do
			if r[i] ~= 0 then
				v[i] += (b[i] - a[i]) * r[i]
			end
		end
		out[p] = v
	end
	return out
end

function BladeCore.lerpParams(a: Params, b: Params, t: number, out: Params?): Params
	local result: Params = out or {}
	for _, p in PARAMS do
		local x, y = a[p], b[p]
		local o = result[p]
		if not o then
			o = zeros(#x)
			result[p] = o
		end
		for i = 1, #x do
			o[i] = x[i] + (y[i] - x[i]) * t
		end
	end
	return result
end

export type Centerline = { px: { number }, py: { number }, angle: { number } }

-- Centreline in the blade's own plane. x runs base → point; y points toward the spine. Positive
-- bend curves the point toward the spine (edge on the outside of the curve).
function BladeCore.centerline(params: Params): Centerline
	local N = #params.segLen
	local px, py, angle = zeros(N), zeros(N), zeros(N)
	local seg = zeros(math.max(N - 1, 1))
	local acc = 0
	for i = 1, N - 1 do
		seg[i] = acc + params.bend[i] / 2
		acc += params.bend[i]
	end
	for i = 1, N - 1 do
		px[i + 1] = px[i] + params.segLen[i] * math.cos(seg[i])
		py[i + 1] = py[i] + params.segLen[i] * math.sin(seg[i])
	end
	for i = 1, N do
		angle[i] = if i == 1 then seg[1] elseif i == N then seg[N - 1] else (seg[i - 1] + seg[i]) / 2
	end
	return { px = px, py = py, angle = angle }
end

-- Where a strike lands (strikeIndex = strikes already done), in blade-local 3D.
function BladeCore.strikeTarget(blade: Blade, params: Params, strikeIndex: number): Target
	local s = blade.recipe[math.min(strikeIndex + 1, #blade.recipe)]
	local N = blade.stations
	local i = math.floor(s.u * (N - 1) + 0.5) + 1
	local cl = BladeCore.centerline(params)
	local ridgeY = params.spine[i] + params.ridge[i] * (params.edge[i] - params.spine[i])
	local across = if s.side == "edge"
		then (ridgeY + params.edge[i]) / 2
		elseif s.side == "spine" then (ridgeY + params.spine[i]) / 2
		else (params.spine[i] + params.edge[i]) / 2
	local nx, ny = -math.sin(cl.angle[i]), math.cos(cl.angle[i])
	local thickness = if s.side == "edge" then (params.thick[i] + params.edgeT[i]) / 2 else params.thick[i]
	return {
		station = i,
		point = { cl.px[i] + nx * across, 0, -(cl.py[i] + ny * across) },
		angle = cl.angle[i],
		thickness = thickness,
		halfWidth = (params.spine[i] - params.edge[i]) / 2,
		flip = s.flip,
		turn = math.rad(s.turn or 0),
		stage = s.stage,
	}
end

-- ---------- geometry ----------
-- Ring per station (cross-section, spine → edge → back), as 1-based offsets 1…12:
--   1 spine top · 2 ridge top (flat face) · 3 ridge top (bevel) · 4 edge top (bevel)
--   5 edge bottom (bevel) · 6 ridge bottom (bevel) · 7 ridge bottom (flat) · 8 spine bottom
--   9/10 spine top/bottom (mune face) · 11/12 edge top/bottom (edge face)
-- Duplicated corners keep creases crisp when normals are computed per vertex. After the stations
-- come two caps (base, point): 6 outline vertices + a centre each.

local RING_FACES = { { 1, 2 }, { 3, 4 }, { 11, 12 }, { 5, 6 }, { 7, 8 }, { 10, 9 } }
local CAP_RING = { 1, 2, 4, 5, 6, 8 }
BladeCore.BEVEL_RING = { [3] = true, [4] = true, [5] = true, [6] = true, [11] = true, [12] = true }

function BladeCore.vertexCount(stations: number): number
	return stations * RING + 2 * (#CAP_RING + 1)
end

-- Triangles as a flat list of 1-based vertex numbers, three per triangle (outward winding).
function BladeCore.buildIndex(stations: number): { number }
	local idx = {}
	for i = 0, stations - 2 do
		local a, b = i * RING, (i + 1) * RING
		for _, pq in RING_FACES do
			local p, q = pq[1], pq[2]
			table.move({ a + p, a + q, b + p, a + q, b + q, b + p }, 1, 6, #idx + 1, idx)
		end
	end
	local capBase = stations * RING
	local caps = { { capBase, true }, { capBase + #CAP_RING + 1, false } }
	for _, cap in caps do
		local start, reverse = cap[1] :: number, cap[2] :: boolean
		local centre = start + #CAP_RING + 1
		for j = 1, #CAP_RING do
			local v0 = start + j
			local v1 = start + (j % #CAP_RING) + 1
			if reverse then
				table.move({ centre, v1, v0 }, 1, 3, #idx + 1, idx)
			else
				table.move({ centre, v0, v1 }, 1, 3, #idx + 1, idx)
			end
		end
	end
	return idx
end

-- Vertex positions as a flat list x1, y1, z1, x2, … in blade-local centimetres.
function BladeCore.buildPositions(params: Params, out: { number }?): { number }
	local N = #params.segLen
	local result: { number } = out or table.create(BladeCore.vertexCount(N) * 3, 0)
	local cl = BladeCore.centerline(params)
	local function put(v: number, x: number, planeY: number, h: number)
		local o = (v - 1) * 3
		result[o + 1], result[o + 2], result[o + 3] = x, h, -planeY
	end
	local ringXY = table.create(RING * 2, 0)
	local ringH = table.create(RING, 0)
	local function ringPositions(i: number)
		local spine, edge = params.spine[i], params.edge[i]
		local ridge = spine + params.ridge[i] * (edge - spine)
		local t, te, ts = params.thick[i] / 2, params.edgeT[i] / 2, (params.thick[i] * params.spineT[i]) / 2
		local nx, ny = -math.sin(cl.angle[i]), math.cos(cl.angle[i])
		local offsets = { spine, ridge, ridge, edge, edge, ridge, ridge, spine, spine, spine, edge, edge }
		local heights = { ts, t, t, te, -te, -t, -t, -ts, ts, -ts, te, -te }
		for r = 1, RING do
			ringXY[r * 2 - 1] = cl.px[i] + nx * offsets[r]
			ringXY[r * 2] = cl.py[i] + ny * offsets[r]
			ringH[r] = heights[r]
		end
	end
	for i = 1, N do
		ringPositions(i)
		for r = 1, RING do
			put((i - 1) * RING + r, ringXY[r * 2 - 1], ringXY[r * 2], ringH[r])
		end
	end
	for c, i in { 1, N } do
		local start = N * RING + (c - 1) * (#CAP_RING + 1)
		ringPositions(i)
		local cx, cy = 0, 0
		for j, r in CAP_RING do
			put(start + j, ringXY[r * 2 - 1], ringXY[r * 2], ringH[r])
			cx += ringXY[r * 2 - 1]
			cy += ringXY[r * 2]
		end
		put(start + #CAP_RING + 1, cx / #CAP_RING, cy / #CAP_RING, 0)
	end
	return result
end

function BladeCore.stationOfVertex(vertex: number, stations: number): number
	if vertex <= stations * RING then
		return (vertex - 1) // RING + 1
	end
	return if vertex <= stations * RING + #CAP_RING + 1 then 1 else stations
end

-- Ring offset 1…12, or 0 for cap vertices.
function BladeCore.ringOfVertex(vertex: number, stations: number): number
	return if vertex <= stations * RING then (vertex - 1) % RING + 1 else 0
end

-- ---------- save / load ----------

function BladeCore.exportState(blade: Blade, state: State): SavedState
	local refinement = table.create(blade.stations, 0)
	for i, r in state.refinement do
		refinement[i] = roundTo(r, 0.0001)
	end
	return {
		blade = blade.id,
		version = blade.version,
		strikeIndex = state.strikeIndex,
		totalStrikes = #blade.recipe,
		refinement = refinement,
		quality = roundTo(BladeCore.quality(blade, state), 0.01),
	}
end

-- Rebuilds a state from saved (or client-sent) data by replaying the recipe. Validates everything,
-- so the server can use it on untrusted input. Returns nil and a reason when the data is invalid.
function BladeCore.importState(blade: Blade, data: unknown): (State?, string?)
	if typeof(data) ~= "table" then
		return nil, "state must be a table"
	end
	local t = data :: { [string]: unknown }
	if t.blade ~= blade.id then
		return nil, "state is for a different blade"
	end
	if t.version ~= blade.version then
		return nil, "state is for a different blade version"
	end
	local k = t.strikeIndex
	if typeof(k) ~= "number" or k ~= math.floor(k) or k < 0 or k > #blade.recipe then
		return nil, "invalid strikeIndex"
	end
	local r = t.refinement
	if typeof(r) ~= "table" then
		return nil, "invalid refinement length"
	end
	local list = r :: { unknown }
	if #list ~= blade.stations then
		return nil, "invalid refinement length"
	end
	local refinement = table.create(blade.stations, 0)
	for i = 1, blade.stations do
		local v = list[i]
		if typeof(v) ~= "number" or not isFinite(v) or v < 0 or v > 1 then
			return nil, "refinement values must be 0–1"
		end
		if k < #blade.recipe and v > 0 then
			return nil, "cannot grind before forging is complete"
		end
		refinement[i] = if v >= 0.999 then 1 else v
	end
	local state = BladeCore.createState(blade)
	for _ = 1, k do
		state = BladeCore.applyStrike(blade, state) :: State
	end
	state.refinement = refinement
	return state, nil
end

-- ---------- catalogue measurements ----------

-- Measures a shape the way sword catalogues do. nagasa: straight line from the back of the blade at
-- its base (mune-machi) to the point. sori: the largest gap between the back of the blade and that
-- line, positive when the back dips below it, negative for an inward curve (uchizori).
function BladeCore.measureShape(shape: Shape, stations: number): { nagasa: number, sori: number }
	local p = BladeCore.sampleShape(shape, stations)
	local cl = BladeCore.centerline(p)
	local N = stations
	local function back(i: number): (number, number)
		return cl.px[i] - math.sin(cl.angle[i]) * p.spine[i], cl.py[i] + math.cos(cl.angle[i]) * p.spine[i]
	end
	local x0, y0 = back(1)
	local tipOffset = (p.spine[N] + p.edge[N]) / 2
	local x1 = cl.px[N] - math.sin(cl.angle[N]) * tipOffset
	local y1 = cl.py[N] + math.cos(cl.angle[N]) * tipOffset
	local nagasa = math.sqrt((x1 - x0) ^ 2 + (y1 - y0) ^ 2)
	local nx, ny = -(y1 - y0) / nagasa, (x1 - x0) / nagasa
	local sori = 0
	for i = 2, N - 1 do
		local x, y = back(i)
		local below = -((x - x0) * nx + (y - y0) * ny)
		if math.abs(below) > math.abs(sori) then
			sori = below
		end
	end
	return { nagasa = nagasa, sori = sori }
end

-- ---------- validation ----------

function BladeCore.signedVolume(pos: { number }, index: { number }): number
	local v = 0
	for t = 1, #index, 3 do
		local a, b, c = (index[t] - 1) * 3, (index[t + 1] - 1) * 3, (index[t + 2] - 1) * 3
		v += pos[a + 1] * (pos[b + 2] * pos[c + 3] - pos[b + 3] * pos[c + 2])
			- pos[a + 2] * (pos[b + 1] * pos[c + 3] - pos[b + 3] * pos[c + 1])
			+ pos[a + 3] * (pos[b + 1] * pos[c + 2] - pos[b + 2] * pos[c + 1])
	end
	return v / 6
end

-- Every state a player can see: the blank, after each strike, and fully ground.
function BladeCore.forgingStates(blade: Blade): { State }
	local s = BladeCore.createState(blade)
	local states = { s }
	while not BladeCore.isForged(blade, s) do
		s = BladeCore.applyStrike(blade, s) :: State
		table.insert(states, s)
	end
	local refined = cloneState(s)
	refined.refinement = table.create(blade.stations, 1)
	table.insert(states, refined)
	return states
end

-- Runs the profile checks and returns { { name, ok, detail } }. Never throws.
function BladeCore.validateProfile(blank: Shape, profile: Profile): { CheckResult }
	local results: { CheckResult } = {}
	local function check(name: string, fn: () -> string?)
		local ok, detail = pcall(fn)
		table.insert(results, { name = name, ok = ok, detail = if ok then (detail or "") else tostring(detail) })
	end
	local blade: Blade? = nil
	check("Builds, and every stage is covered by its strikes", function()
		blade = BladeCore.createBlade(blank, profile)
		return nil
	end)
	local b = blade
	if not b then
		return results
	end
	local N = b.stations
	local states = BladeCore.forgingStates(b)
	check("Spine stays above the edge, with valid thickness and segments", function()
		for k, st in states do
			local p = BladeCore.stationParams(b, st)
			for i = 1, N do
				if not (p.spine[i] > p.edge[i]) then
					error(`state {k}, station {i}: edge above spine`, 0)
				end
				if not (p.thick[i] > 0 and p.edgeT[i] > 0 and p.spineT[i] > 0) then
					error(`state {k}, station {i}: thickness`, 0)
				end
				if not (p.ridge[i] >= 0 and p.ridge[i] <= 1) then
					error(`state {k}, station {i}: ridge outside the blade`, 0)
				end
				if i < N and not (p.segLen[i] > 0) then
					error(`state {k}, segment {i} collapsed`, 0)
				end
			end
		end
		return nil
	end)
	check("Mesh is finite and faces outward", function()
		local index = BladeCore.buildIndex(N)
		for k, st in states do
			local pos = BladeCore.buildPositions(BladeCore.stationParams(b, st))
			for _, v in pos do
				if not isFinite(v) then
					error(`state {k}: non-finite vertex`, 0)
				end
			end
			if not (BladeCore.signedVolume(pos, index) > 0) then
				error(`state {k}: inside-out or empty`, 0)
			end
		end
		return nil
	end)
	check("Each stage ends without a catch-up snap", function()
		for k, st in states do
			if st.lastResidual > 1e-9 then
				error(`state {k}: {st.lastResidual}`, 0)
			end
		end
		return nil
	end)
	local spec = profile.spec
	if spec and spec.nagasa and spec.sori then
		local wantNagasa, wantSori = spec.nagasa :: number, spec.sori :: number
		check("Finished blade matches its catalogue nagasa and sori", function()
			local m = BladeCore.measureShape(profile.stages.refined, N)
			if math.abs(m.nagasa - wantNagasa) > 0.05 or math.abs(m.sori - wantSori) > 0.02 then
				error(string.format("measures %.1f cm, sori %.2f cm", m.nagasa, m.sori), 0)
			end
			return string.format("%.1f cm, sori %.2f cm", m.nagasa, m.sori)
		end)
	end
	check("Grinding finishes in a few edge-to-edge passes", function()
		local s = states[#states - 1]
		local passes = 0
		local step = 0.5 / b.length
		while not BladeCore.isRefined(b, s) and passes < 20 do
			local u = 0.02
			while u <= 0.98 do
				s = BladeCore.applyGrind(b, s, u, 0.5 * BladeCore.GRIND_PER_CM)
				u += step
			end
			passes += 1
		end
		if not BladeCore.isRefined(b, s) then
			error("not finished after 20 passes", 0)
		end
		if passes > 6 then
			error(`{passes} passes`, 0)
		end
		return `{passes} passes`
	end)
	return results
end

return BladeCore

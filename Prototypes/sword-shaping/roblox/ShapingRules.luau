--!strict
-- Sword-shaping experiment (2026-10-23), the rules half: one katana's local width, changed by hammer strikes.
-- An experiment, not the game's crafting: nothing here touches items, quality percentages or sword value.
-- Pure Luau (no services), so ServerStorage.Tests.ShapingRulesSpec runs it in Edit.
--
-- Length, curvature and the back (spine) line stay the target's; only the edge moves. Width = spine - edge in cm,
-- per BladeCore station (64 on the katana). A strike adds dir × strength × a cosine bump around u (0 = base,
-- 1 = point), scaled by `mask` (0 at the tang end and at the point, which never move). Strikes never look at the
-- target: it is only for guidance and the score.
-- Every blade (Refinements 5, the Test Anvil: "every sword"): CONFIG is tuned on the katana (refWidth 3.2 cm at its
-- widest). Rules.new(target, { scale, symmetric }) scales every cm value by `scale` (the blade's widest / refWidth;
-- default 1, the katana) into the state (s.blank, s.strength, s.perfect, ...), and a double-edged blade (`symmetric`)
-- moves both edges evenly about its centre line instead of the edge alone.

local Rules = {}

Rules.CONFIG = {
	strength = 0.4, -- cm of width at the centre of one strike (0.15 until 2026-10-25: ~65 strikes a katana, now ~15)
	radius = 0.11, -- a strike reaches this far either side (fraction of the blade, ≈ 7.7 cm on the katana; was 0.07)
	minWidth = 0.8, -- cm: geometry limits, roomy enough for real mistakes
	maxWidth = 4.4,
	blankWidth = 3.5, -- cm: the hot blank (the target runs from 3.2 at the base to 2.2 before the point)
	base = { 0.02, 0.07 }, -- u: fixed up to the first, fully workable from the second, smooth between
	tip = { 0.97, 0.9 }, -- u: fully workable up to the second, fixed from the first
	perfect = 0.16, -- cm: a station this close counts fully matched (2026-10-25, Allen: "more generous", 2x; was 0.08)
	tolerance = 0.5, -- cm beyond `perfect`: a station that much further off counts 37% matched (was 0.25)
	flag = 0.15, -- cm: a local error worth pointing at
	refWidth = 3.2, -- cm: the katana's widest, what the cm values here are tuned on
	sandRate = 0.5, -- cm a second the sanding block takes off under its centre (Rules.sand)
	smoothRate = 8, -- per second: how much faster a station standing proud of its neighbours comes down
	sandRadius = 0.04, -- it reaches this far either side (fraction of the blade, ≈ 2.8 cm on the katana)
	timing = { windup = 0.12, drop = 0.06, deform = 0.1, recover = 0.18, turn = 0.45 }, -- seconds
}
local C = Rules.CONFIG

export type State = {
	n: number,
	k: number, -- the CONFIG cm values' scale for this blade (1: the katana)
	symmetric: boolean, -- double-edged: width grows and shrinks evenly about `center`
	center: { number }, -- cm, the target's centre line (spine + edge) / 2
	blank: number, minWidth: number, maxWidth: number, strength: number, -- the scaled CONFIG values
	perfect: number, tolerance: number, flag: number, sandRate: number,
	u: { number }, -- station positions, 0…1
	mask: { number }, -- how much a strike can move each station, 0…1
	spine: { number }, -- cm, the target's back line (fixed)
	target: { number }, -- cm, target width
	width: { number }, -- cm, current width
}

local function smooth(a: number, b: number, x: number): number -- 0 at a, 1 at b (either order)
	local t = math.clamp((x - a) / (b - a), 0, 1)
	return t * t * (3 - 2 * t)
end

-- 1 at the centre, easing to 0 at `radius` and beyond.
function Rules.falloff(d: number, radius: number): number
	local x = math.abs(d) / radius
	return if x >= 1 then 0 else 0.5 * (1 + math.cos(math.pi * x))
end

-- `target`: BladeCore params of the finished blade (Blueprints.blade(id).shapes[5]). opts.scale: the blade's widest /
-- CONFIG.refWidth (default 1); opts.symmetric: a double-edged blade.
function Rules.new(target: { [string]: { number } }, opts: { scale: number?, symmetric: boolean? }?): State
	local n = #target.spine
	local k = opts and opts.scale or 1
	local s: State = {
		n = n,
		k = k,
		symmetric = opts ~= nil and opts.symmetric == true,
		center = table.create(n, 0),
		blank = C.blankWidth * k, minWidth = C.minWidth * k, maxWidth = C.maxWidth * k, strength = C.strength * k,
		perfect = C.perfect * k, tolerance = C.tolerance * k, flag = C.flag * k, sandRate = C.sandRate * k,
		u = table.create(n, 0),
		mask = table.create(n, 0),
		spine = table.clone(target.spine),
		target = table.create(n, 0),
		width = table.create(n, 0),
	}
	for i = 1, n do
		local u = (i - 1) / (n - 1)
		s.u[i] = u
		s.mask[i] = smooth(C.base[1], C.base[2], u) * smooth(C.tip[1], C.tip[2], u)
		s.target[i] = target.spine[i] - target.edge[i]
		s.center[i] = (target.spine[i] + target.edge[i]) / 2
	end
	Rules.reset(s)
	return s
end

-- The starting blank: blankWidth wherever the blade can be worked, the target's own width at the tang end and point.
function Rules.reset(s: State)
	for i = 1, s.n do
		s.width[i] = s.target[i] + (s.blank - s.target[i]) * s.mask[i]
	end
end

-- Developer preset: a well-shaped blade with one section near the point hammered too narrow.
function Rules.preset(s: State)
	for i = 1, s.n do
		local wobble = 0.03 * math.sin(i * 1.7)
		local dip = 0.55 * Rules.falloff(s.u[i] - 0.8, 0.06)
		s.width[i] = s.target[i] + (wobble - dip) * s.k * s.mask[i]
	end
end

-- One hammer strike at u. dir -1 narrows (edge up), +1 widens (flat). The limits stop a strike from pushing past
-- them, never pull a station back inside. Returns the first and last station it moved (0, -1 when none).
function Rules.strike(s: State, u: number, dir: number): (number, number)
	local first, last = 0, -1
	for i = 1, s.n do
		local k = Rules.falloff(s.u[i] - u, C.radius) * s.mask[i]
		if k > 0 then
			local w = s.width[i]
			local moved = w + dir * s.strength * k
			s.width[i] = if dir < 0 then math.max(moved, math.min(w, s.minWidth)) else math.min(moved, math.max(w, s.maxWidth))
			if first == 0 then
				first = i
			end
			last = i
		end
	end
	return first, last
end

-- Shape match 0…100 from the geometry alone (strike counts play no part), plus the worst station and its signed
-- error in cm (+ too wide, - too narrow).
function Rules.score(s: State, widths: { number }?): (number, number, number)
	local w = widths or s.width
	local sum, weight, worst, worstE = 0, 0, 1, 0
	for i = 1, s.n do
		local e = w[i] - s.target[i]
		local over = math.max(0, math.abs(e) - s.perfect)
		sum += s.mask[i] * math.exp(-(over / s.tolerance) ^ 2)
		weight += s.mask[i]
		if math.abs(e) * s.mask[i] > math.abs(worstE) * s.mask[worst] then
			worst, worstE = i, e
		end
	end
	return 100 * sum / weight, worst, worstE
end

-- Sanding (Refinements 5 made it a held, manual step; 2026-10-25, Allen: "players should be able to smooth whenever",
-- and it "should smooth out the surrounding bumps, if its near the line never past that line ... a sharp rough bump
-- would turn smoother"): held over the blade at u for `seconds`, any time, it takes width off the workable stations
-- around u: steadily (`sandRate`), and faster where a station stands proud of its neighbours (`smoothRate` × how far
-- it's over their average), so a sharp bump rounds off first. Never past the target line, never adds material, so a
-- section hammered too narrow still costs. Returns the cm it took off in all.
function Rules.sand(s: State, u: number, seconds: number): number
	local e = table.create(s.n, 0)
	for i = 1, s.n do
		e[i] = s.width[i] - s.target[i]
	end
	local took = 0
	for i = 1, s.n do
		local k = Rules.falloff(s.u[i] - u, C.sandRadius)
		if k > 0 and s.mask[i] > 0 and e[i] > 0 then
			local sum, weight = 0, 0 -- the neighbours' error, within the block's reach of this station
			for j = 1, s.n do
				local wj = Rules.falloff(s.u[j] - s.u[i], C.sandRadius) * s.mask[j]
				sum += wj * e[j]
				weight += wj
			end
			local proud = math.max(0, e[i] - sum / weight)
			local w = math.max(s.target[i], s.width[i] - (s.sandRate + C.smoothRate * proud) * k * seconds)
			took += s.width[i] - w
			s.width[i] = w
		end
	end
	return took
end

-- BladeCore params for widths `w` (default the current ones): the target's, with the edge at spine - width (a
-- double-edged blade: spine and edge each half the width either side of its centre line).
-- Pass `out` to reuse the tables.
function Rules.params(s: State, target: { [string]: { number } }, w: { number }?, out: { [string]: { number } }?): { [string]: { number } }
	local result = out
	if not result then
		result = {}
		for k, v in target do
			(result :: any)[k] = table.clone(v)
		end
	end
	local widths = w or s.width
	local spine, edge = (result :: any).spine, (result :: any).edge
	for i = 1, s.n do
		if s.symmetric then
			spine[i], edge[i] = s.center[i] + widths[i] / 2, s.center[i] - widths[i] / 2
		else
			edge[i] = s.spine[i] - widths[i]
		end
	end
	return result :: any
end

return Rules

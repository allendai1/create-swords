-- Checks for the sword-shaping experiment's rules (ReplicatedStorage.Prototypes.ShapingRules). In Edit's command bar:
--   print(require(game.ServerStorage.Tests.ShapingRulesSpec:Clone())())
-- Requires a fresh clone of the rules, so an edited module is what gets tested.

return function(): string
	local Rules = require(game.ReplicatedStorage.Prototypes.ShapingRules:Clone()) :: any
	local BladeCore = require(game.ReplicatedStorage.Shared.BladeCore) :: any
	local Blueprints = require(game.ReplicatedStorage.Shared.Blueprints) :: any
	local C = Rules.CONFIG
	local blade = Blueprints.blade("katana")
	local target = blade.shapes[5]

	local passed, failed, lines = 0, 0, {}
	local function check(name: string, ok: boolean, detail: string?)
		if ok then
			passed += 1
		else
			failed += 1
			table.insert(lines, "FAIL " .. name .. (if detail then ": " .. detail else ""))
		end
	end
	local function near(i: number, u: number): boolean
		return math.abs((i - 1) / (blade.stations - 1) - u) < C.radius
	end

	-- a strike changes only its own region, most at the centre
	local s = Rules.new(target)
	local before = table.clone(s.width)
	local centre = 32
	local u = s.u[centre]
	Rules.strike(s, u, -1)
	local outside, maxDrop, maxAt = true, 0, 0
	for i = 1, s.n do
		local d = before[i] - s.width[i]
		if not near(i, u) and d ~= 0 then
			outside = false
		end
		if d > maxDrop then
			maxDrop, maxAt = d, i
		end
	end
	check("strike leaves the rest of the blade unchanged", outside)
	check("strike is strongest at the centre", maxAt == centre and math.abs(maxDrop - C.strength) < 0.01, `{maxAt} {maxDrop}`)

	-- opposite orientations move width in opposite directions
	local w0 = s.width[centre]
	Rules.strike(s, u, 1)
	check("widening raises the width", s.width[centre] > w0)
	Rules.strike(s, u, -1)
	check("narrowing lowers the width", math.abs(s.width[centre] - w0) < 1e-9)

	-- overshoot both ways, without consulting the target
	Rules.reset(s)
	local k = 0
	while s.width[centre] > s.target[centre] - 0.3 and k < 100 do
		Rules.strike(s, u, -1)
		k += 1
	end
	check("narrowing can go past the target", s.width[centre] < s.target[centre] - 0.3, `{k} strikes`)
	k = 0
	while s.width[centre] < s.target[centre] + 0.3 and k < 100 do
		Rules.strike(s, u, 1)
		k += 1
	end
	check("widening can go past the target", s.width[centre] > s.target[centre] + 0.3)

	-- the preset: well shaped except one narrow section near the point
	Rules.preset(s)
	local score, worst, worstE = Rules.score(s)
	check("preset's worst spot is the narrow one near the point", worstE < -0.4 and near(worst, 0.8), `{worst} {worstE}`)
	check("preset still scores well overall", score > 80 and score < 98, tostring(score))

	-- inside the perfect band everywhere is 100%, either side of the line
	local inBand = Rules.new(target)
	for i = 1, inBand.n do
		inBand.width[i] = inBand.target[i] + (if i % 2 == 0 then 0.9 else -0.9) * C.perfect
	end
	check("a blade inside the band everywhere scores 100", Rules.score(inBand) == 100, tostring(Rules.score(inBand)))

	-- moving toward the target improves the score; moving away worsens it
	local s0 = Rules.score(s)
	Rules.strike(s, 0.8, 1)
	local s1 = Rules.score(s)
	check("widening the narrow spot improves the score", s1 > s0, `{s0} -> {s1}`)
	Rules.strike(s, 0.8, -1)
	Rules.strike(s, 0.8, -1)
	check("narrowing it further worsens the score", Rules.score(s) < s0)

	-- local corrections preserve distant sections
	Rules.preset(s)
	local kept = table.clone(s.width)
	for _, step in { { 0.8, -1 }, { 0.8, -1 }, { 0.8, 1 }, { 0.8, 1 }, { 0.8, 1 }, { 0.8, 1 }, { 0.8, 1 }, { 0.79, -1 } } do
		Rules.strike(s, step[1], step[2])
	end
	local distant = true
	for i = 1, s.n do
		if not near(i, 0.8) and not near(i, 0.79) and s.width[i] ~= kept[i] then
			distant = false
		end
	end
	check("corrections near the point leave the rest of the blade as it was", distant)

	-- the tang end and the point never move
	Rules.reset(s)
	local blank = table.clone(s.width)
	for _ = 1, 40 do
		Rules.strike(s, 0.0, -1)
		Rules.strike(s, 1.0, -1)
		Rules.strike(s, 0.02, 1)
	end
	check("tang end fixed", s.width[1] == blank[1] and s.width[2] == blank[2])
	check("point fixed", s.width[s.n] == blank[s.n] and s.width[s.n - 1] == blank[s.n - 1])

	-- repeated input cannot make invalid geometry
	local index = BladeCore.buildIndex(s.n)
	local function valid(): (boolean, string)
		local p = Rules.params(s, target)
		for i = 1, s.n do
			if not (p.spine[i] > p.edge[i]) or p.edge[i] ~= p.edge[i] then
				return false, `station {i}`
			end
		end
		local pos = BladeCore.buildPositions(p)
		for _, x in pos do
			if x ~= x or math.abs(x) > 1e4 then
				return false, "bad vertex"
			end
		end
		local v = BladeCore.signedVolume(pos, index)
		return v > 0, `volume {v}`
	end
	for _, dir in { -1, 1 } do
		Rules.reset(s)
		for _ = 1, 400 do
			for j = 0, 20 do
				Rules.strike(s, j / 20, dir)
			end
		end
		local ok, why = valid()
		check(`400 passes of {if dir < 0 then "narrowing" else "widening"} keep the mesh valid`, ok, why)
		local inLimits = true
		for i = 1, s.n do
			if s.mask[i] > 0 and (s.width[i] < C.minWidth - 1e-9 or s.width[i] > C.maxWidth + 1e-9) then
				inLimits = false
			end
		end
		check("widths stay inside the limits", inLimits)
	end

	-- reset restores the blank
	Rules.reset(s)
	local same = true
	for i = 1, s.n do
		if s.width[i] ~= blank[i] then
			same = false
		end
	end
	check("reset restores the starting blank", same)

	-- sanding (Refinements 5; one-click smoothing in Refinement 4): only when close, only near the block, only takes
	-- excess off, and a wide-but-close blade sanded all along finishes at 100%
	local function sweep() -- the block held a second at every spot from base to point
		for k = 0, 200 do
			Rules.sand(s, k / 200, 1)
		end
	end
	check("no sanding on the blank", not Rules.canSmooth(s))
	local function offset(cm: number)
		for i = 1, s.n do
			s.width[i] = s.target[i] + cm * s.mask[i]
		end
	end
	offset(0.3)
	check("no sanding while still far off", Rules.score(s) < C.smoothAt and not Rules.canSmooth(s), `{Rules.score(s)}`)
	offset(0.15)
	check("sanding once close and wide", Rules.score(s) >= C.smoothAt and Rules.canSmooth(s), `{Rules.score(s)}`)
	local far = s.width[math.floor(0.2 * (s.n - 1)) + 1]
	local took = Rules.sand(s, 0.5, 0.1)
	check("a moment's sanding takes a little, only near the block", took > 0 and s.width[math.floor(0.2 * (s.n - 1)) + 1] == far, `{took}`)
	sweep()
	check("sanding all along stops on the line: 100%", math.abs(Rules.score(s) - 100) < 1e-6, `{Rules.score(s)}`)
	check("nothing left to sand after", not Rules.canSmooth(s))
	offset(-0.15)
	local narrow = table.clone(s.width)
	check("no sanding when only too narrow", not Rules.canSmooth(s))
	sweep()
	local kept = true
	for i = 1, s.n do
		if s.width[i] ~= narrow[i] then
			kept = false
		end
	end
	check("sanding never adds material", kept)

	table.insert(lines, 1, `{passed} passed, {failed} failed`)
	return table.concat(lines, "\n")
end

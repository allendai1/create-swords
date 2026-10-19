--!strict
-- Tests for BladeCore. Runs in the Luau CLI (roblox/run-tests.luau) and in Studio
-- (require(ServerStorage.Tests.BladeCoreSpec)(BladeCore, BladeData, BladeGolden)).
-- Mirrors tests/blade-core.test.js and also checks every result against BladeGolden, the values
-- the JavaScript core computes, so the two ports can't drift apart.

type Report = { passed: number, failed: number, lines: { string } }

return function(BladeCore: any, BladeData: any, BladeGolden: any): Report
	local report: Report = { passed = 0, failed = 0, lines = {} }
	local currentBlade = ""

	local function test(name: string, fn: () -> ())
		local ok, err = pcall(fn)
		if ok then
			report.passed += 1
			table.insert(report.lines, `  ok   {currentBlade}: {name}`)
		else
			report.failed += 1
			table.insert(report.lines, `  FAIL {currentBlade}: {name}\n       {err}`)
		end
	end

	local function near(a: number, b: number, tol: number, what: string)
		if math.abs(a - b) > tol then
			error(`{what}: {a} vs expected {b}`, 0)
		end
	end

	local function expect(cond: boolean, what: string)
		if not cond then
			error(what, 0)
		end
	end

	local function forgedState(blade: any): any
		local s = BladeCore.createState(blade)
		while not BladeCore.isForged(blade, s) do
			s = BladeCore.applyStrike(blade, s)
		end
		return s
	end

	local blank = BladeData.blank
	for _, id in BladeData.order do
		local profile = BladeData.profiles[id]
		local golden = BladeGolden[id]
		local blade = BladeCore.createBlade(blank, profile)
		local N = blade.stations
		currentBlade = blade.name

		test("mesh layout matches the JavaScript core", function()
			expect(BladeCore.vertexCount(N) == golden.vertexCount, "vertex count")
			expect(#BladeCore.buildIndex(N) == golden.indexCount, "index count")
			near(blade.length, golden.length, 1e-6, "blade length")
		end)

		test("quality after every strike matches, ending at exactly 90%", function()
			local states = BladeCore.forgingStates(blade)
			for k = 1, #states - 1 do
				near(BladeCore.quality(blade, states[k]), golden.qualityByStrike[k], 1e-6, `quality after {k - 1} strikes`)
			end
			expect(BladeCore.quality(blade, states[#states - 1]) == 90, "forged quality is not exactly 90")
			expect(BladeCore.applyStrike(blade, states[#states - 1]) == nil, "extra strikes must be refused")
		end)

		test("every stage ends without a catch-up snap", function()
			local s = BladeCore.createState(blade)
			while not BladeCore.isForged(blade, s) do
				s = BladeCore.applyStrike(blade, s)
				expect(s.lastResidual < 1e-9, `residual {s.lastResidual}`)
			end
		end)

		test("vertex positions match the JavaScript core at blank, strike 6, forged and refined", function()
			local states = BladeCore.forgingStates(blade)
			local samples = {
				{ golden.blank, states[1] },
				{ golden.strike6, states[7] },
				{ golden.forged, states[#states - 1] },
				{ golden.refined, states[#states] },
			}
			for _, pair in samples do
				local g, st = pair[1], pair[2]
				local pos = BladeCore.buildPositions(BladeCore.stationParams(blade, st))
				local sum = 0
				for _, v in pos do
					sum += math.abs(v)
				end
				-- JavaScript stores positions as 32-bit floats; Luau keeps doubles.
				near(sum, g.absSum, 1e-3 * math.max(1, g.absSum / 1000), "sum of |positions|")
				for _, vtx in g.vertices do
					local o = (vtx[1] - 1) * 3
					for axis = 1, 3 do
						near(pos[o + axis], vtx[axis + 1], 1e-4, `vertex {vtx[1]} axis {axis}`)
					end
				end
			end
		end)

		test("first strike target matches", function()
			local t = BladeCore.strikeTarget(blade, BladeCore.stationParams(blade, BladeCore.createState(blade)), 0)
			expect(t.station == golden.firstStrike.station, `station {t.station}`)
			for axis = 1, 3 do
				near(t.point[axis], golden.firstStrike.point[axis], 1e-6, `point axis {axis}`)
			end
			near(t.angle, golden.firstStrike.angle, 1e-6, "angle")
			near(t.thickness, golden.firstStrike.thickness, 1e-6, "thickness")
		end)

		test("grinding matches, only improves, never passes the target edge, and reaches 100%", function()
			local s = forgedState(blade)
			s = BladeCore.applyGrind(blade, s, 0.3, 0.5)
			s = BladeCore.applyGrind(blade, s, 0.9, 0.25)
			near(BladeCore.quality(blade, s), golden.groundQuality, 1e-6, "quality after two grinds")
			local runs = BladeCore.unfinishedRuns(blade, s)
			expect(#runs == #golden.groundRuns, "number of unfinished stretches")
			for i, run in runs do
				expect(run[1] == golden.groundRuns[i][1] and run[2] == golden.groundRuns[i][2], `stretch {i}`)
			end
			-- Monotonic and bounded under a deterministic pseudo-random sequence.
			local seed = 12345
			local function rand(): number
				seed = (seed * 1103515245 + 12345) % 2147483648
				return seed / 2147483648
			end
			local prev = BladeCore.quality(blade, s)
			for _ = 1, 300 do
				s = BladeCore.applyGrind(blade, s, rand() * 1.1 - 0.05, rand() * 0.2)
				local q = BladeCore.quality(blade, s)
				expect(q >= prev - 1e-12, "quality dropped")
				expect(q <= 100 + 1e-9, "quality above 100")
				prev = q
				local p = BladeCore.stationParams(blade, s)
				for i = 1, N do
					local lo = math.min(blade.shapes[4].edge[i], blade.shapes[5].edge[i])
					local hi = math.max(blade.shapes[4].edge[i], blade.shapes[5].edge[i])
					expect(p.edge[i] >= lo - 1e-9 and p.edge[i] <= hi + 1e-9, `edge {i} past the target`)
				end
			end
			local passes = 0
			while not BladeCore.isRefined(blade, s) and passes < 10 do
				local u = 0.02
				while u <= 0.98 do
					s = BladeCore.applyGrind(blade, s, u, 0.5 * BladeCore.GRIND_PER_CM)
					u += 0.5 / blade.length
				end
				passes += 1
			end
			expect(BladeCore.quality(blade, s) == 100 and BladeCore.displayQuality(blade, s) == 100, "not exactly 100")
			for _, bad in { -1, 0, 0 / 0 } do
				local before = BladeCore.quality(blade, s)
				s = BladeCore.applyGrind(blade, BladeCore.applyGrind(blade, s, 0.5, bad), 0 / 0, 0.5)
				expect(BladeCore.quality(blade, s) == before, "bad grind input changed quality")
			end
		end)

		test("grinding does nothing before forging is complete", function()
			local s = BladeCore.createState(blade)
			s = BladeCore.applyStrike(blade, s)
			local g = BladeCore.applyGrind(blade, s, 0.5, 1)
			for _, r in g.refinement do
				expect(r == 0, "refined before forging")
			end
		end)

		test("save → load round-trips; tampered saves are rejected", function()
			local s = BladeCore.applyGrind(blade, forgedState(blade), 0.3, 0.6)
			local saved = BladeCore.exportState(blade, s)
			local loaded, err = BladeCore.importState(blade, saved)
			expect(loaded ~= nil, `load failed: {err}`)
			local again = BladeCore.exportState(blade, loaded)
			for i = 1, N do
				expect(again.refinement[i] == saved.refinement[i], `refinement {i}`)
			end
			local function with(changes: { [string]: any }): any
				local t = table.clone(saved)
				for k, v in changes do
					t[k] = v
				end
				return t
			end
			local zeros = table.create(N, 0)
			local halves = table.create(N, 0.5)
			local short = table.clone(saved.refinement)
			table.remove(short)
			local bad = {
				"not a table",
				with({ blade = "not-a-blade" }),
				with({ version = 99 }),
				with({ strikeIndex = #blade.recipe + 1 }),
				with({ strikeIndex = 2.5 }),
				with({ refinement = short }),
				with({ refinement = table.create(N, 1.5) }),
				with({ refinement = table.create(N, 0 / 0) }),
				with({ strikeIndex = 3, refinement = halves }),
			}
			for i, b in bad do
				local st = BladeCore.importState(blade, b)
				expect(st == nil, `bad save {i} was accepted`)
			end
			local mid = BladeCore.importState(blade, with({ strikeIndex = 7, refinement = zeros }))
			expect(mid ~= nil and mid.strikeIndex == 7, "mid-forge save")
		end)

		test("catalogue measurement matches the JavaScript core and the spec", function()
			local m = BladeCore.measureShape(profile.stages.refined, N)
			near(m.nagasa, golden.measured.nagasa, 1e-6, "nagasa")
			near(m.sori, golden.measured.sori, 1e-6, "sori")
			near(m.nagasa, profile.spec.nagasa, 0.05, "nagasa vs spec")
			near(m.sori, profile.spec.sori, 0.02, "sori vs spec")
		end)

		test("shared profile validation passes", function()
			for _, r in BladeCore.validateProfile(blank, profile) do
				expect(r.ok, `{r.name}: {r.detail}`)
			end
		end)
	end

	currentBlade = "validation"
	test("a broken profile is reported, not thrown", function()
		local broken = table.clone(BladeData.profiles.tanto)
		local stages = table.clone(broken.stages)
		local refined = table.clone(stages.refined)
		refined.edge = { { 0, 2 }, { 1, 2 } }
		stages.refined = refined
		broken.stages = stages
		broken.recipe = { broken.recipe[1], broken.recipe[2], broken.recipe[3] }
		local results = BladeCore.validateProfile(blank, broken)
		local anyFailed = false
		for _, r in results do
			anyFailed = anyFailed or not r.ok
		end
		expect(anyFailed, "broken profile passed")
	end)

	return report
end

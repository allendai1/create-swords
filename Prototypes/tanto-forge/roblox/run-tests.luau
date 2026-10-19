--!strict
-- Runs BladeCoreSpec in the stand-alone Luau CLI: `luau roblox/run-tests.luau` (exit code 1 on failure).
local BladeCore = require("./BladeCore")
local BladeData = require("./BladeData")
local BladeGolden = require("./BladeGolden")
local spec = require("./BladeCoreSpec")

local start = os.clock()
local report = spec(BladeCore, BladeData, BladeGolden)
print(table.concat(report.lines, "\n"))
print(`\n{report.passed} passed, {report.failed} failed ({string.format("%.0f", (os.clock() - start) * 1000)} ms)`)
if report.failed > 0 then
	error("BladeCore tests failed", 0)
end

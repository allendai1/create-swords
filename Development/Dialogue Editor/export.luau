-- Dialogue Editor export: run in Studio (Edit) via MCP execute_luau while server.js runs.
-- Requires a clone of Shared (never the live modules) and POSTs studio.json to the editor.
local HttpService = game:GetService("HttpService")
local shared = game.ReplicatedStorage.Shared:Clone()
local ok, result = pcall(function()
	local Customers = require(shared.Customers)
	local Senders = require(shared.Senders)
	local Commissions = require(shared.Commissions)
	local Blueprints = require(shared.Blueprints)
	local function hex(c)
		return c and string.format("#%02x%02x%02x", c.R * 255 + 0.5, c.G * 255 + 0.5, c.B * 255 + 0.5) or nil
	end
	local data = { customerLines = Customers.LINES, cast = {}, senders = {}, commissions = {}, tutorial = {}, blueprints = {} }
	for _, c in Customers.cast do
		table.insert(data.cast, { id = c.id, name = c.name, vip = c.vip == true, likesBlueprint = c.likesBlueprint, lines = c.lines })
	end
	local orderSet = {}
	for _, id in Senders.ORDERS do
		orderSet[id] = true
	end
	for _, s in Senders.list do
		table.insert(data.senders, { id = s.id, name = s.name, role = s.role, lines = s.lines, orders = orderSet[s.id] == true,
			shirt = hex(s.look.shirt), skin = hex(s.look.skin), pants = hex(s.look.pants) })
	end
	for _, c in Commissions.list do
		table.insert(data.commissions, { id = c.id, giver = c.giver, letter = c.letter, want = c.want, blueprintId = c.blueprintId,
			materialId = c.materialId, minPercent = c.minPercent, polished = c.polished == true, reward = c.reward, gems = c.gems or 0,
			afterSales = c.afterSales, after = c.after, afterUpgrade = c.afterUpgrade })
	end
	for _, id in Blueprints.order do
		local bp = Blueprints.get(id)
		table.insert(data.blueprints, { id = id, name = bp and bp.name or id, big = bp and bp.big == true or false })
	end
	-- tutorial hints: the string literals the Guide shows as its top line, one entry per text (the same text can be
	-- returned and compared on several lines; editing it renames every one)
	local byText = {}
	local i = 0
	for line in (game.StarterPlayer.StarterPlayerScripts.Guide.Source .. "\n"):gmatch("(.-)\n") do
		i += 1
		local code = line:gsub("%-%-.*$", "")
		if code:find("return") or code:find("text = ") or code:find("elseif ") then
			for q, s in code:gmatch("([\"`])([A-Z][^\"`]-)%1") do
				if s:find(" ") then
					local e = byText[s]
					if not e then
						e = { text = s, template = q == "`", lines = {} }
						byText[s] = e
						table.insert(data.tutorial, e)
					end
					table.insert(e.lines, i)
				end
			end
		end
	end
	data.exportedAt = os.date("!%Y-%m-%dT%H:%M:%SZ")
	return HttpService:JSONEncode(data)
end)
shared:Destroy()
if not ok then
	return "ERR " .. tostring(result)
end
local res = HttpService:RequestAsync({ Url = "http://127.0.0.1:8767/studio", Method = "POST", Body = result,
	Headers = { ["Content-Type"] = "application/json" } })
return res.StatusCode .. " " .. res.Body .. " bytes=" .. #result

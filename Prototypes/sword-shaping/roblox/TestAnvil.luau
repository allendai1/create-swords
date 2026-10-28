--!strict
-- The Test Anvil (Studio only; Refinements 5, Allen: "take the prototype and apply it to a sample anvil so i can test the
-- flow start to finish with this new process"; his picks: a new Studio-only anvil, the shape match is the blade's
-- quality, every sword). E at your plot's Smithy.TestAnvil: pick a hot ingot, then a sword you know, and the shaping
-- prototype (ReplicatedStorage.Prototypes.ShapingPrototype) opens on that sword. Finish sends the match and the widths
-- you hammered to SmithService's FinishShaped, which turns the ingot into a blade of that quality and that shape, and
-- you're back in the workshop; from there the Hilt Bench, display and sale run as usual, the sword keeping your shape
-- (2026-10-26). Exit leaves with the ingot still hot. Anvils 1 and 2 keep
-- the current forging.

local Players = game:GetService("Players")
local ProximityPromptService = game:GetService("ProximityPromptService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

if not RunService:IsStudio() then
	return
end

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Blueprints = require(Shared:WaitForChild("Blueprints")) :: any
local Materials = require(Shared:WaitForChild("Materials")) :: any
local Shaping = require(ReplicatedStorage:WaitForChild("Prototypes"):WaitForChild("ShapingPrototype")) :: any
local ItemPicker = require(script.Parent:WaitForChild("ItemPicker")) :: any
local MyPlot = require(script.Parent:WaitForChild("MyPlot")) :: any
local Remotes = ReplicatedStorage:WaitForChild("Remotes")
local FinishShaped = Remotes:WaitForChild("FinishShaped") :: RemoteFunction
local GetSmithState = Remotes:WaitForChild("GetSmithState") :: RemoteFunction
local SmithState = Remotes:WaitForChild("SmithState") :: RemoteEvent

local S = Blueprints.STUDS_PER_CM
local state: any = { ingots = {}, blueprints = {} }
SmithState.OnClientEvent:Connect(function(s)
	state = s
end)
task.spawn(function()
	local ok, s = pcall(GetSmithState.InvokeServer, GetSmithState)
	if ok and s then
		state = s
	end
end)

local function shape(ingot: any, blueprintId: string)
	Shaping.start({
		blueprintId = blueprintId,
		onFinish = function(match: number, widths: { number }): boolean
			local ok, res = pcall(FinishShaped.InvokeServer, FinishShaped, ingot.id, blueprintId, match, widths)
			if ok and res then
				return true
			end
			ItemPicker.toast("Couldn't save that blade, try again", "warn")
			return false
		end,
	})
end

local function pickSword(ingot: any)
	local known: { [string]: boolean } = {}
	for _, id in state.blueprints or {} do
		known[id] = true
	end
	local mult = Materials.multiplier(ingot.materialId) or 1
	local cards = {}
	for _, id in Blueprints.order do
		local bp = Blueprints[id]
		if known[id] and Blueprints.blade(id) then
			table.insert(cards, {
				name = `Shape{id}`,
				title = bp.name,
				chip = `{string.rep("★", bp.difficulty)}  ·  {math.floor(bp.basePrice * mult + 0.5)} coins`,
				chipColor = ItemPicker.CHIP.Gold,
				art = { kind = "silhouette", left = bp.left, right = bp.right, length = bp.length, halfWidth = S },
				onPick = function()
					ItemPicker.close()
					shape(ingot, id)
				end,
			})
		end
	end
	ItemPicker.open({ title = "Test Anvil", subtitle = "Choose a sword to shape.", cards = cards, emptyTitle = "", emptyHint = "" })
end

local function pickIngot()
	local stacks: { [string]: { any } } = {}
	local order: { string } = {}
	for _, i in state.ingots or {} do
		if i.hot then
			if not stacks[i.materialId] then
				stacks[i.materialId] = {}
				table.insert(order, i.materialId)
			end
			table.insert(stacks[i.materialId], i)
		end
	end
	local cards = {}
	for _, materialId in order do
		local material = Materials.get(materialId)
		local stack = stacks[materialId]
		table.insert(cards, {
			name = `Ingot{materialId}`,
			title = materialId,
			chip = material.rarity,
			qty = #stack,
			glow = true,
			art = { kind = "ingot", color = material.color, hot = true },
			onPick = function()
				pickSword(stack[1])
			end,
		})
	end
	ItemPicker.open({
		title = "Test Anvil",
		subtitle = "Choose a hot ingot to shape.",
		cards = cards,
		emptyTitle = "No hot ingots yet",
		emptyHint = "Heat one at the forge first.",
	})
end

ProximityPromptService.PromptTriggered:Connect(function(prompt)
	if prompt.Name == "ShapePrompt" and MyPlot.owns(prompt) and not Shaping.current then
		pickIngot()
	end
end)

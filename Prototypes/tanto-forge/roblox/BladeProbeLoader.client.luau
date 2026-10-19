--!strict
-- Test-only loader (StarterPlayerScripts). Starts the blade probe when the place has the workspace
-- attribute BladeProbe set to true or to a blueprint id ("tanto", "wakizashi", "katana").
-- Set it from the command bar before pressing Play: workspace:SetAttribute("BladeProbe", "katana")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Workspace = game:GetService("Workspace")

local setting = Workspace:GetAttribute("BladeProbe")
if setting == nil or setting == false then
	return
end
local Shared = ReplicatedStorage:WaitForChild("Shared")
local BladeProbe = require(Shared:WaitForChild("BladeProbe")) :: any
BladeProbe.start(if typeof(setting) == "string" then setting else nil)

--!strict
-- Rickshaw parking (vault: More refinements 2026-10-23, "upgrading parking space means more cars can pull in and means
-- more customers"; Allen chose rickshaws, the bays adding to More Clients). Run in Edit through the Studio MCP.
-- Builds:
--   ServerStorage.Rickshaw   the rickshaw Rickshaws (ServerScriptService) clones: pivot on the ground under the axle,
--                            facing -Z; parts with Wheel = true turn about WheelCentre; attributes Pull (the puller
--                            stands this far ahead of the axle), Seat (where a rider's seat top is), Step (where a rider
--                            gets out, on the left).
--   Workspace.Plot.Parking.Bay1..3   TycoonItems of Parking1..3: a slate slab (Slab) on the street in front of the
--                            shop, just past its gutter, its top 0.04 proud, and a post with a 車 sign at the far end.
--                            (Until 2026-10-24 the middle lots stood 8 back and the bays sat on a paved junction;
--                            since the lots lined up with the street, the same plot-space spot is on the street.)
--   Workspace.Plot.Pads.Parking1..3  pad markers on the bays (copies of Pads.Delivery).
-- Plot space: +z is into the lot (the shop), the street is at z < -56 (past the gutter's outer curb), its top is
-- world y 0.2.
-- Rerunning replaces all of it.

local CollectionService = game:GetService("CollectionService")
local ServerStorage = game:GetService("ServerStorage")

local plot = workspace:FindFirstChild("Plot") :: Model
local pv = plot:GetPivot()

local BAYS = { 9.5, -10, 19 } -- plot-space x of each bay's centre, in buying order
local BAY_Z = -61.3
local GROUND = 0.2 -- world y of the street's top
local SLAB = Vector3.new(8.5, 0.1, 3.8)

local LACQUER = Color3.fromRGB(70, 22, 20)
local WOOD = Color3.fromRGB(120, 80, 45)
local DARK_WOOD = Color3.fromRGB(48, 34, 26)
local SPOKE = Color3.fromRGB(196, 156, 98)
local BRASS = Color3.fromRGB(200, 160, 70)
local CLOTH = Color3.fromRGB(165, 40, 35)
local HOOD = Color3.fromRGB(32, 28, 30)

local function part(parent: Instance, name: string, size: Vector3, cf: CFrame, color: Color3, material: Enum.Material?, shape: Enum.PartType?): Part
	local p = Instance.new("Part")
	p.Name = name
	if shape then
		p.Shape = shape
	end
	p.Size, p.CFrame, p.Color = size, cf, color
	p.Material = material or Enum.Material.SmoothPlastic
	p.Anchored, p.CanCollide, p.CanTouch, p.CanQuery = true, false, false, false
	p.TopSurface, p.BottomSurface = Enum.SurfaceType.Smooth, Enum.SurfaceType.Smooth
	p.Parent = parent
	return p
end

-- The rickshaw ---------------------------------------------------------------------------------------------------
local old = ServerStorage:FindFirstChild("Rickshaw")
if old then
	old:Destroy()
end
local r = Instance.new("Model")
r.Name = "Rickshaw"
local root = part(r, "Root", Vector3.new(0.2, 0.2, 0.2), CFrame.new(), Color3.new(1, 1, 1))
root.Transparency = 1
r.PrimaryPart = root

local AXLE_Y, RADIUS, TRACK = 1.8, 1.8, 1.65
for _, side in { -1, 1 } do
	local c = CFrame.new(side * TRACK, AXLE_Y, 0)
	local cyl = Enum.PartType.Cylinder -- a cylinder's axis is its X: across the rickshaw
	part(r, "Wheel", Vector3.new(0.16, RADIUS * 2, RADIUS * 2), c, DARK_WOOD, Enum.Material.Wood, cyl)
	for k = 0, 2 do -- three bars through the hub: six spokes, 0.04 proud of the wheel on both faces
		part(r, "Spoke", Vector3.new(0.24, RADIUS * 2 - 0.3, 0.14), c * CFrame.Angles(math.rad(60 * k), 0, 0), SPOKE, Enum.Material.Wood)
	end
	part(r, "Hub", Vector3.new(0.36, 0.7, 0.7), c, BRASS, Enum.Material.Metal, cyl)
end
for _, p in r:GetChildren() do
	if p.Name == "Wheel" or p.Name == "Spoke" or p.Name == "Hub" then
		p:SetAttribute("Wheel", true)
	end
end
part(r, "Axle", Vector3.new(TRACK * 2, 0.18, 0.18), CFrame.new(0, AXLE_Y, 0), Color3.fromRGB(40, 40, 44), Enum.Material.Metal, Enum.PartType.Cylinder)

-- body over the axle; the seat faces forward (-Z)
part(r, "Body", Vector3.new(2.7, 1, 1.7), CFrame.new(0, 2.55, 0.1), LACQUER, Enum.Material.SmoothPlastic)
part(r, "Cushion", Vector3.new(2.4, 0.3, 1.45), CFrame.new(0, 3.2, 0), CLOTH, Enum.Material.Fabric)
part(r, "Backrest", Vector3.new(2.7, 1.7, 0.25), CFrame.new(0, 3.9, 0.825), LACQUER, Enum.Material.SmoothPlastic)
part(r, "BackPad", Vector3.new(2.3, 1.2, 0.08), CFrame.new(0, 3.95, 0.66), CLOTH, Enum.Material.Fabric)
-- the folded hood over the seat, on two posts
part(r, "HoodTop", Vector3.new(2.8, 0.08, 1.4), CFrame.new(0, 5.2, 0.3) * CFrame.Angles(math.rad(10), 0, 0), HOOD, Enum.Material.Fabric)
part(r, "HoodBack", Vector3.new(2.72, 1.3, 0.08), CFrame.new(0, 4.6, 1.05) * CFrame.Angles(math.rad(-14), 0, 0), HOOD, Enum.Material.Fabric)
for _, side in { -1, 1 } do
	part(r, "HoodPost", Vector3.new(0.08, 2.2, 0.08), CFrame.new(side * 1.36, 4.15, -0.3), DARK_WOOD, Enum.Material.Wood)
end
-- footboard in front of the seat
part(r, "Footboard", Vector3.new(2.3, 0.14, 1), CFrame.new(0, 1.35, -1.35), LACQUER, Enum.Material.SmoothPlastic)
for _, side in { -1, 1 } do
	part(r, "FootBracket", Vector3.new(0.12, 0.7, 0.12), CFrame.new(side * 1, 1.7, -0.75), DARK_WOOD, Enum.Material.Wood)
end
-- shafts from the body to the crossbar the puller holds
local SHAFT_X, BAR_Z, BAR_Y = 1.15, -4.85, 2.85
for _, side in { -1, 1 } do
	local a, b = Vector3.new(side * SHAFT_X, 2.5, -0.6), Vector3.new(side * SHAFT_X, BAR_Y, BAR_Z - 0.05)
	part(r, "Shaft", Vector3.new(0.16, 0.16, (b - a).Magnitude), CFrame.lookAt((a + b) / 2, b), WOOD, Enum.Material.Wood)
end
part(r, "Crossbar", Vector3.new(SHAFT_X * 2 + 0.24, 0.14, 0.14), CFrame.new(0, BAR_Y, BAR_Z), WOOD, Enum.Material.Wood)
-- a paper lantern on the left hood post
part(r, "Lantern", Vector3.new(0.45, 0.6, 0.45), CFrame.new(-1.36, 4.55, -0.55), Color3.fromRGB(220, 70, 50), Enum.Material.Neon, Enum.PartType.Ball)

r:SetAttribute("Pull", 4.2)
r:SetAttribute("Seat", Vector3.new(0, 3.35, 0.05))
r:SetAttribute("Step", Vector3.new(-2.6, 0, 0))
r:SetAttribute("WheelCentre", Vector3.new(0, AXLE_Y, 0))
r:SetAttribute("Radius", RADIUS)
r.Parent = ServerStorage

-- The bays ---------------------------------------------------------------------------------------------------------
local folder = plot:FindFirstChild("Parking")
if folder then
	folder:Destroy()
end
folder = Instance.new("Folder")
folder.Name = "Parking"
folder.Parent = plot
for i, x in BAYS do
	local bay = Instance.new("Model")
	bay.Name = `Bay{i}`
	local centre = pv * CFrame.new(x, 0, BAY_Z)
	local slabCf = CFrame.new(centre.Position.X, GROUND + 0.04 - SLAB.Y / 2, centre.Position.Z) * centre.Rotation
	local slab = part(bay, "Slab", SLAB, slabCf, Color3.fromRGB(112, 106, 98), Enum.Material.Slate)
	slab.CanQuery = true
	-- a post at the far (-x) end on the shop side, its sign facing the street
	local post = part(bay, "Post", Vector3.new(0.3, 2.8, 0.3), slabCf * CFrame.new(-SLAB.X / 2 - 0.4, 1.4 + SLAB.Y / 2, SLAB.Z / 2 - 0.3), DARK_WOOD, Enum.Material.Wood)
	post.CanCollide = true
	local sign = part(bay, "Sign", Vector3.new(1.2, 1.2, 0.12), post.CFrame * CFrame.new(0, 0.9, -0.21), Color3.fromRGB(226, 205, 168), Enum.Material.Wood)
	local gui = Instance.new("SurfaceGui")
	gui.Face = Enum.NormalId.Front -- toward the street (plot -z)
	gui.PixelsPerStud = 80
	gui.LightInfluence = 1
	local t = Instance.new("TextLabel")
	t.Size = UDim2.fromScale(1, 1)
	t.BackgroundTransparency = 1
	t.Text = "車"
	t.TextScaled = true
	t.TextColor3 = Color3.fromRGB(60, 24, 20)
	t.FontFace = Font.new("rbxasset://fonts/families/SourceSansPro.json", Enum.FontWeight.Bold) -- as the shop's kanji signs
	t.Parent = gui
	gui.Parent = sign
	bay:SetAttribute("Upgrade", `Parking{i}`)
	CollectionService:AddTag(bay, "TycoonItem")
	bay.Parent = folder

	-- its pad, a copy of the Delivery pad's marker, on the bay
	local pads = plot:FindFirstChild("Pads") :: Folder
	local oldPad = pads:FindFirstChild(`Parking{i}`)
	if oldPad then
		oldPad:Destroy()
	end
	local src = pads:FindFirstChild("Delivery") :: BasePart
	local pad = src:Clone()
	pad:ClearAllChildren()
	pad.Name = `Parking{i}`
	pad.CFrame = CFrame.new(centre.Position.X, src.Position.Y, centre.Position.Z) * src.CFrame.Rotation
	pad.Parent = pads
end

return `Rickshaw ({#r:GetChildren()} parts), {#BAYS} bays and pads`

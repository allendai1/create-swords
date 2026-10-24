-- build_delivery.luau: the delivery cart, its board and the delivery pads on the plot template (Allen 2026-10-22: "Also
-- implement the delivery feature"; vault: Shared/Deliveries, DeliveryService). Run in Studio (Edit) after
-- build_workshop (which rebuilds Plot.DeliveryBay without them):
--   loadstring(game.ServerStorage.Builders.build_delivery.Source)()
-- Rerunning replaces what it built. Everything is in plot space (workspace.Plot's pivot; the shop is at -z, the street
-- beyond it).
--   DeliveryBay.Cart: a two-wheeled handcart on the bay's CartSpot, shafts toward the street gateway, with Crate1-6 on its
--     bed (DeliveryService shows one per packed sword and rolls the cart out and back). TycoonItem, Upgrade = Delivery.
--   DeliveryBay.DeliveryBoard: a notice board by the shop wall facing the cart; its Panel holds the DeliveryPrompt and
--     the Status timer. TycoonItem, Upgrade = Delivery.
--   Pad: Delivery inside the shop in front of the delivery wall (the cart's Capacity and Speed are bought in the
--     Deliveries window, as in Create Pottery!'s van page).

local CollectionService = game:GetService("CollectionService")
local plot = workspace:FindFirstChild("Plot")
assert(plot, "workspace.Plot (the template) missing")
local pv = plot:GetPivot()
local bay = plot.DeliveryBay
local rgb = Color3.fromRGB
local C = {
	timber = rgb(70, 46, 32), plank = rgb(160, 112, 66), wheel = rgb(92, 62, 40), iron = rgb(58, 56, 60),
	cedar = rgb(176, 120, 72), band = rgb(112, 74, 44), paper = rgb(242, 228, 198), roof = rgb(176, 88, 54),
}
local M = Enum.Material

for _, name in { "Cart", "DeliveryBoard" } do
	local old = bay:FindFirstChild(name)
	if old then old:Destroy() end
end

local function part(parent, name, size, cf, color, material, shape)
	local p = Instance.new("Part")
	p.Name = name
	p.Size = size
	p.CFrame = cf
	p.Color = color
	p.Material = material or M.Wood
	if shape then p.Shape = shape end
	p.Anchored, p.CanCollide, p.CanQuery, p.CanTouch = true, false, false, false
	p.TopSurface, p.BottomSurface = Enum.SurfaceType.Smooth, Enum.SurfaceType.Smooth
	p.Parent = parent
	return p
end

local function item(name)
	local m = Instance.new("Model")
	m.Name = name
	m:SetAttribute("Upgrade", "Delivery")
	m:SetAttribute("BuiltBy", "build_delivery")
	CollectionService:AddTag(m, "TycoonItem")
	return m
end

local ground = bay.Yard.Position.Y + bay.Yard.Size.Y / 2 -- the yard's top

-- ---------------------------------------------------------------- the cart
-- cart space: origin on the ground under CartSpot's centre, -Z toward the street (CartSpot faces it), X across
local spot = bay.CartSpot
local O = CFrame.new(spot.Position.X, ground, spot.Position.Z) * spot.CFrame.Rotation
local cart = item("Cart")
local function c(name, size, x, y, z, color, material, shape, turn)
	return part(cart, name, size, O * CFrame.new(x, y, z) * (turn or CFrame.identity), color, material, shape)
end
local BED_Y = 2.2 -- bed centre; top 2.4
c("Bed", Vector3.new(4.6, 0.4, 6.4), 0, BED_Y, 0, C.plank, M.WoodPlanks)
for _, s in { -1, 1 } do
	c("Side", Vector3.new(0.25, 0.9, 6.4), s * 2.175, 2.83, 0, C.timber)
	c("Shaft", Vector3.new(0.25, 0.25, 5.2), s * 1.5, 1.95, -5.7, C.timber, M.Wood, nil, CFrame.Angles(math.rad(-6), 0, 0))
	c("Wheel", Vector3.new(0.35, 2.8, 2.8), s * 2.75, 1.42, 0.6, C.wheel, M.Wood, Enum.PartType.Cylinder)
	c("Hub", Vector3.new(0.45, 0.7, 0.7), s * 2.75, 1.42, 0.6, C.iron, M.Metal, Enum.PartType.Cylinder)
end
for _, z in { -3.075, 3.075 } do
	c("End", Vector3.new(4.1, 0.9, 0.25), 0, 2.83, z, C.timber)
end
c("Axle", Vector3.new(5.2, 0.3, 0.3), 0, 1.42, 0.6, C.iron, M.Metal, Enum.PartType.Cylinder)
c("Crossbar", Vector3.new(3.3, 0.25, 0.25), 0, 1.68, -8.1, C.timber)
for i, at in { { -1.05, -2 }, { 1.05, -2 }, { -1.05, 0 }, { 1.05, 0 }, { -1.05, 2 }, { 1.05, 2 } } do -- up to the top Capacity (6)
	local crate = Instance.new("Model")
	crate.Name = "Crate" .. i
	part(crate, "Box", Vector3.new(1.8, 1.6, 1.8), O * CFrame.new(at[1], 2.38 + 0.8, at[2]), C.cedar, M.WoodPlanks)
	for _, y in { 0.45, 1.15 } do -- two bands round it, 0.04 proud
		part(crate, "Band", Vector3.new(1.88, 0.16, 1.88), O * CFrame.new(at[1], 2.38 + y, at[2]), C.band)
	end
	crate.Parent = cart
end
cart.WorldPivot = O
cart.Parent = bay

-- ---------------------------------------------------------------- the board
-- board space: front (-Z) toward +x in plot space (into the bay), standing by the shop wall on the street side of the door
local B = CFrame.lookAt(pv:PointToWorldSpace(Vector3.new(26.4, 0, -36)), pv:PointToWorldSpace(Vector3.new(27.4, 0, -36)))
B = CFrame.new(B.Position.X, ground, B.Position.Z) * B.Rotation
local board = item("DeliveryBoard")
local function b(name, size, x, y, z, color, material)
	return part(board, name, size, B * CFrame.new(x, y, z), color, material)
end
for _, s in { -1, 1 } do
	b("Post", Vector3.new(0.35, 5.2, 0.35), s * 1.95, 2.6, 0, C.timber)
end
local panel = b("Panel", Vector3.new(3.6, 2.4, 0.2), 0, 3.4, 0, C.plank, M.WoodPlanks)
b("Cap", Vector3.new(4.6, 0.25, 0.9), 0, 5.32, 0, C.roof, M.ClayRoofTiles)
for i, x in { -0.95, 0.15, 1.05 } do -- order slips pinned on, 0.04 proud
	b("Slip", Vector3.new(0.7, 0.9, 0.04), x, 3.25 + (i % 2) * 0.25, -0.12, C.paper, M.SmoothPlastic)
end
local face = Instance.new("SurfaceGui") -- the Storage box (VectorIcons, vault: Art/Icon Library) on the board
face.Name = "Icon"
face.Face = Enum.NormalId.Front
face.PixelsPerStud = 50
face.LightInfluence = 1
local icon = Instance.new("ImageLabel")
icon.BackgroundTransparency = 1
icon.AnchorPoint = Vector2.new(0, 0.5)
icon.Position = UDim2.fromScale(0.03, 0.27)
icon.Size = UDim2.fromScale(0.2, 0.3)
icon.ScaleType = Enum.ScaleType.Fit
icon.Image = "rbxassetid://15403012566"
icon.Parent = face
face.Parent = panel
local prompt = Instance.new("ProximityPrompt")
prompt.Name = "DeliveryPrompt"
prompt.ActionText = "Deliveries"
prompt.ObjectText = "Delivery Board"
prompt.KeyboardKeyCode = Enum.KeyCode.E
prompt.GamepadKeyCode = Enum.KeyCode.ButtonX
prompt.HoldDuration = 0
prompt.MaxActivationDistance = 9
prompt.RequiresLineOfSight = false
prompt.Parent = panel
local status = Instance.new("BillboardGui") -- the forge timer's look (ForgeService)
status.Name = "Status"
status.Size = UDim2.fromOffset(110, 44)
status.StudsOffset = Vector3.new(0, 2.6, 0)
status.MaxDistance = 60
status.Enabled = false
local label = Instance.new("TextLabel")
label.Name = "Text"
label.Size = UDim2.fromScale(1, 1)
label.BackgroundColor3 = rgb(43, 28, 19)
label.BackgroundTransparency = 0.08
label.FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Bold)
label.TextSize = 24
label.TextColor3 = rgb(251, 235, 213)
Instance.new("UICorner", label).CornerRadius = UDim.new(0, 14)
local edge = Instance.new("UIStroke", label)
edge.ApplyStrokeMode, edge.Color, edge.Thickness = Enum.ApplyStrokeMode.Border, rgb(168, 106, 62), 1.5
label.Parent = status
status.Parent = panel
board.Parent = bay

-- ---------------------------------------------------------------- pads
local src = plot.Pads.WallRack2 -- a shop pad marker
local rel = pv:ToObjectSpace(src.CFrame)
local function pad(name, x, z)
	local p = plot.Pads:FindFirstChild(name) or src:Clone()
	p.Name = name
	for k in p:GetAttributes() do p:SetAttribute(k, nil) end
	for _, ch in p:GetChildren() do ch:Destroy() end
	p.CFrame = pv * CFrame.new(x, rel.Y, z) * rel.Rotation
	p.Parent = plot.Pads
end
pad("Delivery", 19.5, -28)
for _, old in { "Courier1", "Courier2" } do
	local p = plot.Pads:FindFirstChild(old)
	if p then p:Destroy() end
end

return ("delivery: cart %d parts, board %d parts, 1 pad"):format(#cart:GetDescendants(), #board:GetDescendants())

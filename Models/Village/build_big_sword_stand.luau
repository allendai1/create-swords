-- build_big_sword_stand.luau: the Big Sword Stand (2026-10-23).
-- Allen: "the big swords would require you to purchase a standing big sword rack and it only holds one. they can sell for
-- a lot", then "Build the one-sword Big Sword Stand next." One big sword (Blueprints.big, the Zanbatō first) stands upright,
-- blade up and its flat to the room, its grip in a socket on a two-step plinth, in front of a torii-like frame whose upper
-- crossbar has a brass clip either side of the blade. The tip rises past the frame's top.
-- Run in Studio (Edit) through MCP execute_luau on Workspace.Plot (the template every player's plot is copied from).
-- Rerunnable: the display and its pad marker are replaced if this script built them.
-- Built here:
--   Shop.Displays.BigSwordStand: TycoonItem, Upgrade = BigSwordStand (Shared/Upgrades, after the Upgraded Store), with
--     Origin, InspectPoint (where a customer stands), Stand (the parts) and Slot1: DisplaySlot tag, HolderPrompt (a copy
--     of Display Table 2's), Inspect, ViaAisle, BigSword = true (Blueprints.fits: only big swords here, and big swords
--     only here), SwordMid = 3 (ShopController puts the + marker this far up the blade).
--   Pads.BigSwordStand: its pad marker, on the floor under the stand, as Display Table 2's pad is under its table.
-- Where: by the Upgraded Store's back wall (the workshop's door wall once the Upgraded Store pushes the workshop 12 back;
-- its face is then at plot z -6.52), left of the door, centred on the wall's post at plot x -13, so DisplayTable2
-- (z -27.4…-22.3) and the customers' back aisle row (z about -21) stay clear. Plot space: -z toward the street.
-- Display frame: the Origin on the floor's top at the stand's centre, +z toward the shop front, y up.
-- The sword: ShopService puts its Handle on Slot1; it runs along the slot's +x from the grip (here straight up), the
-- slot's y into the wall (flat to the room), so its edge points along the slot's z (-x of the display). With the katana
-- hilt the Zanbatō has for now, the pommel is 0.54 below the Handle and the blade's base 0.58 above it; the blade is
-- 0.92 wide and 4.92 long (100 cm at 0.05 studs per cm).

local P = workspace.Plot
local F = P:GetPivot()
local AT = { x = -13, z = -9 } -- the stand's centre, plot space
local O = F * CFrame.new(AT.x, -0.3, AT.z) * CFrame.Angles(0, math.pi, 0) -- display frame: y 0 the floor's top, +z to the street
local M = Enum.Material
local C = {
	wood = Color3.fromRGB(146, 84, 48), -- the wall shelves' and tables' wood
	woodDk = Color3.fromRGB(98, 56, 34),
	plinth = Color3.fromRGB(40, 28, 22),
	brass = Color3.fromRGB(176, 140, 70),
}

local H = 1.55 -- the Handle's height: the pommel (0.54 below) sits in the socket, the grip shows above it
local BLADE_HALF = 0.46 -- half the Zanbatō's width
local FRAME_Z = -0.62 -- the frame's posts, behind the blade

local function part(parent, name, size, cf, col, mat, o)
	o = o or {}
	local p = Instance.new(o.wedge and "WedgePart" or "Part")
	p.Name = name
	p.Anchored = true
	p.Size = size
	p.CFrame = cf
	p.Color = col
	p.Material = mat or M.SmoothPlastic
	p.TopSurface = Enum.SurfaceType.Smooth
	p.BottomSurface = Enum.SurfaceType.Smooth
	p.CanCollide = o.solid == true
	p.CanQuery = o.solid == true
	p.CanTouch = false
	if size.X * size.Y * size.Z < 2 then p.CastShadow = false end
	p.Parent = parent
	return p
end
local function D(x, y, z) return O * CFrame.new(x, y, z) end
local function box(parent, name, x0, x1, y0, y1, z0, z1, col, mat, o)
	return part(parent, name, Vector3.new(x1 - x0, y1 - y0, z1 - z0), D((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), col, mat, o)
end
local function marker(parent, name, cf, size)
	local p = part(parent, name, size or Vector3.one * 0.2, cf, C.brass)
	p.Transparency = 1
	p.CastShadow = false
	return p
end

local displays = P.Shop.Displays
local old = displays:FindFirstChild("BigSwordStand")
if old then
	assert(old:GetAttribute("BuiltBy") == "build_big_sword_stand", "Shop.Displays.BigSwordStand wasn't built by this script")
	old:Destroy()
end
local d = Instance.new("Model")
d.Name = "BigSwordStand"
d:SetAttribute("BuiltBy", "build_big_sword_stand")
d:SetAttribute("Upgrade", "BigSwordStand")
d:AddTag("TycoonItem")

marker(d, "Origin", O)
local inspect = marker(d, "InspectPoint", D(0, 3, 3.6), Vector3.one) -- where a customer looks from (as the shelves')

local m = Instance.new("Model")
m.Name = "Stand"
m.Parent = d
local solid = { solid = true }
-- the plinth: two steps, brass caps on the upper step's corners (faces 0.04 proud of the wood: no shared planes)
box(m, "Plinth", -1.6, 1.6, 0, 0.4, -1.2, 1.2, C.plinth, M.Wood, solid)
box(m, "Step", -1.2, 1.2, 0.4, 0.75, -0.9, 0.9, C.wood, M.Wood, solid)
for _, sx in { -1, 1 } do
	for _, sz in { -1, 1 } do
		box(m, "Corner", sx * 1.2 - 0.18, sx * 1.2 + 0.18, 0.36, 0.79, sz * 0.9 - 0.18, sz * 0.9 + 0.18, C.brass, M.Metal)
	end
end
-- the socket the grip stands in: a block with a dark mouth on top
box(m, "Socket", -0.45, 0.45, 0.75, 1.3, -0.35, 0.35, C.woodDk, M.Wood, solid)
box(m, "SocketMouth", -0.22, 0.22, 1.3, 1.34, -0.14, 0.14, C.plinth, M.SmoothPlastic)
box(m, "SocketBand", -0.49, 0.49, 1.12, 1.24, -0.39, 0.39, C.brass, M.Metal)
-- the frame: two posts behind the blade, a crossbar (nuki) and a wider top beam (kasagi) with brass end caps
for _, sx in { -1, 1 } do
	local x = sx * 0.85
	box(m, "Post", x - 0.15, x + 0.15, 0.75, 6.2, FRAME_Z - 0.15, FRAME_Z + 0.15, C.wood, M.Wood, solid)
	box(m, "PostFoot", x - 0.22, x + 0.22, 0.71, 0.95, FRAME_Z - 0.22, FRAME_Z + 0.22, C.brass, M.Metal) -- sunk 0.04 into the step: not level with the post's foot
	box(m, "BeamCap", sx * 1.32 - 0.12, sx * 1.32 + 0.12, 6.16, 6.6, FRAME_Z - 0.22, FRAME_Z + 0.22, C.brass, M.Metal)
end
box(m, "Nuki", -1.05, 1.05, 4.75, 5.0, FRAME_Z - 0.1, FRAME_Z + 0.1, C.woodDk, M.Wood)
box(m, "Kasagi", -1.3, 1.3, 6.2, 6.56, FRAME_Z - 0.18, FRAME_Z + 0.18, C.wood, M.Wood)
-- brass clips from the crossbar, either side of the blade
for _, sx in { -1, 1 } do
	local x = sx * (BLADE_HALF + 0.08)
	box(m, "Clip", x - 0.05, x + 0.05, 4.78, 4.97, FRAME_Z + 0.1, 0.1, C.brass, M.Metal)
end

-- the holder: the Handle here, the blade straight up, flat to the room
local slot = marker(d, "Slot1", O * CFrame.fromMatrix(Vector3.new(0, H, 0), Vector3.yAxis, -Vector3.zAxis, -Vector3.xAxis))
slot.CanQuery = false
slot:AddTag("DisplaySlot")
slot:SetAttribute("ViaAisle", true)
slot:SetAttribute("BigSword", true)
slot:SetAttribute("SwordMid", 3)
local prompt = (displays.DisplayTable2.Slot1:FindFirstChild("HolderPrompt") :: ProximityPrompt):Clone()
prompt.Enabled = true
prompt.Parent = slot
local ref = Instance.new("ObjectValue")
ref.Name = "Inspect"
ref.Value = inspect
ref.Parent = slot

d.Parent = displays

-- the pad marker
local pads = P.Pads
local oldPad = pads:FindFirstChild("BigSwordStand")
if oldPad then
	assert(oldPad:GetAttribute("BuiltBy") == "build_big_sword_stand", "Pads.BigSwordStand wasn't built by this script")
	oldPad:Destroy()
end
local pad = pads.DisplayTable2:Clone()
pad:ClearAllChildren()
pad.Name = "BigSwordStand"
pad:SetAttribute("BuiltBy", "build_big_sword_stand")
pad.CFrame = F * CFrame.new(AT.x, -0.3, AT.z)
pad.Parent = pads

return "Big Sword Stand built"

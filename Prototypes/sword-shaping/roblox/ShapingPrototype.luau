--!strict
-- Sword-shaping experiment (2026-10-23), the client half: a forge corner of its own, far above the village, where you
-- shape one hot katana blank by choosing where to hammer and which way the blade lies. Edge up, a strike narrows the
-- section under the hammer; flat, it widens it (rules and tuning: ShapingRules). Started from the Studio DevPanel
-- ("Shaping prototype"); Exit puts the camera, controls and HUD back. Not the game's crafting: it uses no items and
-- sends nothing to the server. Tweens as in Shared/BladeProbe, mesh from Shared/BladeView.
--
-- Opening it holds the character still (Humanoid WalkSpeed/Jump 0) and switches every other screen off.
-- Mouse: move to choose where (on the blade or the diagram), click (or hold) to strike. R or Turn blade turns it. Touch:
-- drag on the blade or the diagram to choose, Strike (or hold it) to hit. Finish scores the shape; Reset blank starts over; Exit leaves.
-- Refinements 5 (Allen: "the actual sword and anvil need to be the main view"; the guide lines "Overlay on the blade"):
-- the blade and anvil are the main view, centred below the panel; a true-shape silhouette (yours filled, the target outlined) sits at the top
-- (lines drawn on the blade itself were tried and couldn't show millimetres at this camera), and the steel reads red
-- where it's too wide and blue where it's too narrow. Sand (any time, 2026-10-25) swaps the hammer for a sanding block:
-- hold the mouse (or a finger) on the blade and drag to sand the bumps down to the line, never past it, sharp bumps
-- first (Rules.sand). Hammer swaps back. Holding the mouse (or Strike) with the hammer out keeps striking, about 3 a
-- second, wherever you aim (2026-10-25, Allen: "hold down to hit automatically").
-- Shaping.start(opts?): opts.blueprintId (default "katana": any blueprint with a BladeCore blade; Rules scales to its
-- width and double-edged blades shape both edges), opts.onFinish(match, widths) -> saved: Finish hands it the match and
-- the widths (cm per station) and leaves when it says saved, instead of the score card (the Studio-only Test Anvil, TestAnvil LocalScript).

local ContextActionService = game:GetService("ContextActionService")
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")
local SoundService = game:GetService("SoundService")
local UserInputService = game:GetService("UserInputService")
local Workspace = game:GetService("Workspace")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local BladeCore = require(Shared:WaitForChild("BladeCore")) :: any
local BladeView = require(Shared:WaitForChild("BladeView")) :: any
local Blueprints = require(Shared:WaitForChild("Blueprints")) :: any
local Rules = require(script.Parent:WaitForChild("ShapingRules")) :: any
local C = Rules.CONFIG
local T = C.timing

local Shaping = {}
Shaping.current = nil :: any
Shaping.attempts = {} :: { any } -- one entry per Finish this session

local S = Blueprints.STUDS_PER_CM
local ORIGIN = CFrame.new(0, 600, 0) -- the anvil's top centre; far above the village, every part local to this client
local BASE_X = -1.6 -- studs: where the blade's base sits along the anvil
local HOVER, RAISE = 0.2, 0.7 -- hammer face above the blade while aiming, and wound up (studs)
local FLASH_TIME = 0.35
local RING = BladeCore.RING
local ROLL = { edge = -math.pi / 2, flat = 0 } -- turned about the blade's length; -90° puts the edge on top
local ELEVATION = math.rad(64) -- the camera's, steep enough that edge up reads as a thin line and flat as the full face
local TOWARD_CAMERA = Vector3.new(0, math.sin(ELEVATION), math.cos(ELEVATION))

local HOT = Color3.fromRGB(232, 104, 36)
local AIM = Color3.fromRGB(255, 212, 120)
local FLASH = Color3.fromRGB(255, 250, 228)
local NARROW = Color3.fromRGB(110, 190, 255)
local WIDEN = Color3.fromRGB(255, 168, 64)
local TOO_WIDE = Color3.fromRGB(235, 72, 56)
local TOO_NARROW = Color3.fromRGB(72, 150, 255)
local PANEL = Color3.fromRGB(43, 28, 19)
local GOLD = Color3.fromRGB(242, 184, 64)
local TEXT = Color3.fromRGB(239, 230, 218)
local FONT = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Bold)

type Tween = { start: number, duration: number, fn: (number) -> (), done: () -> () }

local function easeOut(t: number): number
	return 1 - (1 - t) ^ 3
end
local function easeIn(t: number): number
	return t * t * t
end
local function easeInOut(t: number): number
	return if t < 0.5 then 4 * t * t * t else 1 - (-2 * t + 2) ^ 3 / 2
end

function Shaping.start(opts: { blueprintId: string?, onFinish: ((number, { number }) -> boolean)? }?)
	if Shaping.current then
		return
	end
	Shaping.current = {}
	local player = Players.LocalPlayer
	local camera = Workspace.CurrentCamera
	local blueprintId = opts and opts.blueprintId or "katana"
	local onFinish = opts and opts.onFinish
	local blade = Blueprints.blade(blueprintId)
	local N: number = blade.stations
	local target = blade.shapes[5]
	local widest = 0
	for i = 1, N do
		widest = math.max(widest, target.spine[i] - target.edge[i])
	end
	local state = Rules.new(target, { scale = widest / C.refWidth, symmetric = blade.profile.doubleEdged == true })
	local shown = table.clone(state.width) -- what's drawn; eases toward state.width after a strike
	local params = Rules.params(state, target, shown)

	local folder = Instance.new("Folder")
	folder.Name = "ShapingPrototype"
	local function block(name: string, size: Vector3, cf: CFrame, color: Color3, material: Enum.Material?): Part
		local p = Instance.new("Part")
		p.Name = name
		p.Anchored = true
		p.CanCollide, p.CanTouch, p.CanQuery = false, false, false
		p.CastShadow = false
		p.Size = size
		p.CFrame = cf
		p.Color = color
		p.Material = material or Enum.Material.SmoothPlastic
		p.TopSurface, p.BottomSurface = Enum.SurfaceType.Smooth, Enum.SurfaceType.Smooth
		p.Parent = folder
		return p
	end

	-- ---------- the forge corner ----------
	local bladeLen = blade.length * S
	local bedLen = bladeLen + 0.6
	local midX = BASE_X + bladeLen / 2
	local bed = block("AnvilBed", Vector3.new(bedLen, 0.3, 0.55), ORIGIN * CFrame.new(midX, -0.15, 0), Color3.fromRGB(58, 58, 62), Enum.Material.Metal)
	block("AnvilBody", Vector3.new(bedLen * 0.75, 1.3, 0.42), ORIGIN * CFrame.new(midX, -0.95, 0), Color3.fromRGB(38, 38, 41), Enum.Material.Metal)
	block("Stump", Vector3.new(bedLen * 0.85, 0.6, 1.1), ORIGIN * CFrame.new(midX, -1.9, 0), Color3.fromRGB(74, 50, 34), Enum.Material.Wood)
	block("Floor", Vector3.new(16, 0.2, 10), ORIGIN * CFrame.new(midX, -2.3, 1), Color3.fromRGB(46, 40, 36), Enum.Material.Slate)
	block("Wall", Vector3.new(16, 8, 0.2), ORIGIN * CFrame.new(midX, 1.7, -3), Color3.fromRGB(40, 30, 24), Enum.Material.Brick)
	local sparkPoint = Instance.new("Attachment")
	sparkPoint.Parent = bed
	local sparks = Instance.new("ParticleEmitter")
	sparks.Rate = 0
	sparks.Lifetime = NumberRange.new(0.12, 0.3)
	sparks.Speed = NumberRange.new(1.5, 3.5)
	sparks.SpreadAngle = Vector2.new(75, 75)
	sparks.EmissionDirection = Enum.NormalId.Top
	sparks.Size = NumberSequence.new(0.03, 0)
	sparks.Acceleration = Vector3.new(0, -9, 0)
	sparks.Drag = 2
	sparks.LightEmission = 1
	sparks.Color = ColorSequence.new(Color3.fromRGB(255, 232, 150), Color3.fromRGB(255, 120, 40))
	sparks.Parent = sparkPoint
	local clang = Instance.new("Sound")
	clang.SoundId = "rbxassetid://9125361455" -- the anvil's Clang
	clang.Volume = 0.3
	clang.SoundGroup = SoundService:FindFirstChild("Effects") :: SoundGroup?
	clang.Parent = folder

	-- ---------- the blade, its tang and the tongs ----------
	local view = BladeView.new(blueprintId, params, blade.length + 10)
	view.part.Material = Enum.Material.SmoothPlastic
	view.part.Color = Color3.new(1, 1, 1) -- the vertex colours carry the heat
	view.part.Parent = folder
	local glow = Instance.new("PointLight")
	glow.Color = HOT
	glow.Range = 4
	glow.Brightness = 1.6
	glow.Parent = view.part
	-- Turn the blade in its own plane so the line from base to point runs along the anvil; then rolling it about
	-- that line keeps both ends on the anvil whichever way up it lies.
	local cl = BladeCore.centerline(params)
	local YAW = math.atan2(-cl.py[N], cl.px[N])
	local baseMid = (target.spine[1] + target.edge[1]) / 2
	local tangLen, tangWidth, tangThick = blade.tang.length * S, blade.tang.width * S, target.thick[1] * 0.75 * S
	local tang = block("Tang", Vector3.new(tangLen, tangThick, tangWidth), CFrame.identity, Color3.fromRGB(96, 44, 26))
	local tongParts: { { part: Part, offset: CFrame } } = {}
	local IRON = Color3.fromRGB(34, 34, 38)
	local function tongPart(name: string, size: Vector3, offset: CFrame)
		table.insert(tongParts, { part = block(name, size, CFrame.identity, IRON, Enum.Material.Metal), offset = offset })
	end
	-- In the tang's frame (x toward the point): jaws clamp the tang's flat faces, a rivet, then the reins splay
	-- apart through the blade's thickness, so turning the blade visibly turns them too.
	local jawY = tangThick / 2 + 0.012
	tongPart("JawTop", Vector3.new(0.4, 0.024, tangWidth * 0.8), CFrame.new(-0.05, jawY, 0))
	tongPart("JawBottom", Vector3.new(0.4, 0.024, tangWidth * 0.8), CFrame.new(-0.05, -jawY, 0))
	tongPart("Rivet", Vector3.new(0.09, 0.09, 0.09), CFrame.new(-0.32, 0, 0))
	local REIN = 1.5
	for _, side in { 1, -1 } do
		local from, to = Vector3.new(-0.32, side * jawY, 0), Vector3.new(-0.32 - REIN, side * 0.16, 0)
		tongPart("Rein", Vector3.new(0.03, 0.03, (to - from).Magnitude), CFrame.lookAt((from + to) / 2, to))
	end

	local roll, lift = ROLL.edge, 0
	local function placeBlade()
		local cf = ORIGIN * CFrame.new(BASE_X, lift, 0) * CFrame.Angles(roll, 0, 0) * CFrame.Angles(0, YAW, 0)
		view.part.CFrame = cf
		local tangCf = cf * CFrame.new(-tangLen / 2, 0, -baseMid * S)
		tang.CFrame = tangCf
		local grip = tangCf * CFrame.new(-tangLen * 0.05, 0, 0)
		for _, t in tongParts do
			t.part.CFrame = grip * t.offset
		end
	end
	-- How high the blade must sit so its lowest point rests on the anvil, lying at roll r.
	local function liftFor(r: number): number
		local rot = CFrame.Angles(r, 0, 0) * CFrame.Angles(0, YAW, 0)
		local low, p = math.huge, view.positions
		for v = 1, view.vertexCount do
			local o = (v - 1) * 3
			low = math.min(low, (rot * Vector3.new(p[o + 1], p[o + 2], p[o + 3])).Y)
		end
		return -low * S
	end

	local shapeChanged = true -- the error tint repaints
	local function refreshMesh()
		Rules.params(state, target, shown, params)
		view:setParams(params)
		shapeChanged = true
	end


	-- A station's world point the hammer lands on: halfway across the blade, on its top.
	local function topOf(i: number): Vector3
		local cf, p = view.part.CFrame, view.positions
		local function at(r: number): Vector3
			local o = ((i - 1) * RING + r - 1) * 3
			return cf:PointToWorldSpace(Vector3.new(p[o + 1], p[o + 2], p[o + 3]) * S)
		end
		local mid = (at(1) + at(4)) / 2 -- spine top and edge top
		local top = -math.huge
		for r = 1, RING do
			top = math.max(top, at(r).Y)
		end
		return Vector3.new(mid.X, top, mid.Z)
	end
	local function contactAt(u: number): Vector3
		local f = u * (N - 1) + 1
		local i = math.clamp(math.floor(f), 1, N - 1)
		return topOf(i):Lerp(topOf(i + 1), f - i)
	end

	-- ---------- hammer ----------
	local HEAD = 0.34
	local HDIR = Vector3.new(0.7, 0, -0.72).Unit -- handle to the right and away from the camera, never over the blade
	local WRIST = HDIR * 1.35 + Vector3.new(0, HEAD / 2 + 0.22, 0)
	local SWING = HDIR:Cross(Vector3.yAxis).Unit
	local head = block("HammerHead", Vector3.new(HEAD, 0.17, 0.17), CFrame.identity, Color3.fromRGB(70, 70, 76), Enum.Material.Metal)
	head.Shape = Enum.PartType.Cylinder
	local handleFrom = Vector3.new(0, HEAD / 2, 0)
	local handle = block("HammerHandle", Vector3.new(0.06, 0.06, (WRIST - handleFrom).Magnitude), CFrame.identity, Color3.fromRGB(110, 76, 46), Enum.Material.Wood)
	local HEAD_LOCAL = CFrame.new(0, HEAD / 2, 0) * CFrame.Angles(0, 0, math.pi / 2)
	local HANDLE_LOCAL = CFrame.lookAt((handleFrom + WRIST) / 2, WRIST)
	local hammerHeight = HOVER
	-- the sanding block (Refinements 5): rides on the blade where you aim while Sand is out, scrubbing while held
	local sandBlock = block("SandBlock", Vector3.new(0.42, 0.14, 0.26), CFrame.identity, Color3.fromRGB(150, 112, 70), Enum.Material.Fabric)
	sandBlock.Transparency = 1
	local function placeHammer(contact: Vector3)
		-- swung from the wrist; at height 0 the face sits on `contact`
		local wrist = contact + WRIST
		local cf = CFrame.new(wrist) * CFrame.fromAxisAngle(SWING, -hammerHeight / WRIST.Magnitude) * CFrame.new(-WRIST)
		head.CFrame = cf * HEAD_LOCAL
		handle.CFrame = cf * HANDLE_LOCAL
	end

	-- ---------- tweens on RenderStepped (as in BladeProbe) ----------
	local tweens: { Tween } = {}
	local function tween(duration: number, fn: (number) -> ())
		local thread = coroutine.running()
		table.insert(tweens, {
			start = os.clock(),
			duration = duration,
			fn = fn,
			done = function()
				task.spawn(thread)
			end,
		})
		coroutine.yield()
	end
	local function parallel(...: () -> ())
		local fns = { ... }
		local remaining = #fns
		local thread = coroutine.running()
		for _, fn in fns do
			task.spawn(function()
				fn()
				remaining -= 1
				if remaining == 0 then
					task.spawn(thread)
				end
			end)
		end
		coroutine.yield()
	end

	-- ---------- interface ----------
	local gui = Instance.new("ScreenGui")
	gui.Name = "ShapingPrototype"
	gui.ResetOnSpawn = false
	gui.DisplayOrder = 60
	local function corner(parent: Instance, r: number)
		Instance.new("UICorner", parent).CornerRadius = UDim.new(0, r)
	end
	local function text(parent: Instance, s: string, size: number, color: Color3): TextLabel
		local l = Instance.new("TextLabel")
		l.BackgroundTransparency = 1
		l.FontFace = FONT
		l.TextSize = size
		l.TextColor3 = color
		l.Text = s
		l.Parent = parent
		return l
	end
	local function button(parent: Instance, s: string, width: number): TextButton
		local b = Instance.new("TextButton")
		b.Size = UDim2.new(0, width, 1, 0)
		b.BackgroundColor3 = PANEL
		b.BackgroundTransparency = 0.08
		b.FontFace = FONT
		b.TextSize = 16
		b.TextColor3 = GOLD
		b.Text = s
		b.AutoButtonColor = true
		corner(b, 10)
		b.Parent = parent
		return b
	end

	-- The panel with the face-on diagram, at the top (Refinements 5, Allen: "the actual sword and anvil need to be the main
	-- view, while the sword guide lines should be on the top"; lines drawn on the blade itself couldn't show millimetres
	-- at this camera, ~13 px a cm, so the magnified diagram is back). The camera centres the blade below it.
	local panel = Instance.new("Frame")
	panel.AnchorPoint = Vector2.new(0.5, 0)
	panel.Position = UDim2.new(0.5, 0, 0, 12)
	panel.Size = UDim2.new(1, -24, 0, 240) -- full width (the silhouette is true width and needs the room); layout() sets the height
	panel.BackgroundColor3 = PANEL
	panel.BackgroundTransparency = 0.08
	corner(panel, 12)
	local fit = Instance.new("UIScale") -- smaller on a phone, so the blade keeps room below it
	fit.Scale = math.min(1, camera.ViewportSize.Y / 600)
	fit.Parent = panel
	local pad = Instance.new("UIPadding")
	for _, k in { "PaddingLeft", "PaddingRight", "PaddingTop", "PaddingBottom" } do
		(pad :: any)[k] = UDim.new(0, 12)
	end
	pad.Parent = panel
	panel.Parent = gui

	local chip = text(panel, "", 15, Color3.fromRGB(20, 14, 10))
	chip.BackgroundTransparency = 0
	chip.Size = UDim2.fromOffset(190, 28)
	corner(chip, 8)
	local scoreLabel = text(panel, "", 20, GOLD)
	scoreLabel.AnchorPoint = Vector2.new(1, 0)
	scoreLabel.Position = UDim2.fromScale(1, 0)
	scoreLabel.Size = UDim2.fromOffset(300, 28)
	scoreLabel.TextXAlignment = Enum.TextXAlignment.Right
	local legend = text(panel, '<font color="#ffffff">━</font> target    <font color="#c45c28">■</font> yours    <font color="#eb4838">■</font> too wide    <font color="#4896ff">■</font> too narrow', 13, TEXT)
	legend.RichText = true
	legend.AnchorPoint = Vector2.new(0, 1)
	legend.Position = UDim2.fromScale(0, 1)
	legend.Size = UDim2.new(1, 0, 0, 16)
	legend.TextXAlignment = Enum.TextXAlignment.Left

	-- The silhouette (Allen, Refinements 5: "a true-shape silhouette: curved, with the point ... my blade filled and the
	-- target as an outline", like Create Pottery!'s Target / Yours). The blade face-on as it lies, base left, true to
	-- shape: back line, curve and widths all at one scale (2026-10-25: the 2.5x width stretch made it look unlike the
	-- blade; the panel spans the screen instead, so errors still show). Yours is filled (red past the target, blue where
	-- it falls short); the target is a white outline.
	-- (Until then a straightened width chart, widths under 1.4 cm cut off, ~4x taller than long: "it doesnt seem" like
	-- the blade.)
	local PLOT_MIN, PLOT_MAX, PAD, SUB = 80, 170, 8, 2 -- px (the plot's height fits the blade), px, columns per station gap
	local plotH = PLOT_MAX
	local plot = Instance.new("Frame")
	plot.Position = UDim2.fromOffset(0, 38)
	plot.Size = UDim2.new(1, 0, 0, plotH)
	plot.BackgroundColor3 = Color3.fromRGB(24, 16, 11)
	plot.Active = true
	corner(plot, 6)
	plot.Parent = panel
	local function bar(color: Color3, transparency: number, z: number): Frame
		local f = Instance.new("Frame")
		f.BorderSizePixel = 0
		f.BackgroundColor3 = color
		f.BackgroundTransparency = transparency
		f.ZIndex = z
		f.Parent = plot
		return f
	end
	-- a frame as a strip from a to b (px), `across` px wide
	local function strip(f: Frame, a: Vector2, b: Vector2, across: number)
		local d = b - a
		f.AnchorPoint = Vector2.new(0.5, 0.5)
		f.Position = UDim2.fromOffset((a.X + b.X) / 2, (a.Y + b.Y) / 2)
		f.Size = UDim2.fromOffset(across, math.max(d.Magnitude, 0.5))
		f.Rotation = math.deg(math.atan2(d.Y, d.X)) - 90
	end
	-- a list (numbers or Vector2s) at fractional station f
	local function sampleAt(list: { any }, f: number): any
		local i = math.clamp(math.floor(f), 1, N - 1)
		return list[i] + (list[i + 1] - list[i]) * (f - i)
	end
	-- the back line and the way to the edge per station (cm), turned like the blade on the anvil: base -> point left to right
	local spineAt: { Vector2 }, toEdge: { Vector2 } = {}, {}
	do
		local tp = BladeCore.buildPositions(Rules.params(state, target, state.target))
		local turn = CFrame.Angles(0, YAW, 0)
		for i = 1, N do
			local function ring(r: number): Vector2
				local o = ((i - 1) * RING + r - 1) * 3
				local v = turn * Vector3.new(tp[o + 1], 0, tp[o + 3])
				return Vector2.new(v.X, v.Z)
			end
			spineAt[i] = ring(1)
			toEdge[i] = (ring(4) - ring(1)).Unit
		end
	end
	local COLS = (N - 1) * SUB + 1
	local cols = {}
	for k = 1, COLS do -- the steel, what sticks out past the target (either side, double-edged), what falls short
		cols[k] = { body = bar(Color3.fromRGB(196, 92, 40), 0, 1), wideA = bar(TOO_WIDE, 0, 2), wideB = bar(TOO_WIDE, 0, 2),
			gapA = bar(TOO_NARROW, 0.5, 2), gapB = bar(TOO_NARROW, 0.5, 2) }
	end
	-- Where steel `w` wide lies across station f, in cm from the target's back line (the target runs 0 to t): from the
	-- back line out, or (double-edged) centred on the target's centre line.
	local function span(w: number, t: number): (number, number)
		if state.symmetric then
			return (t - w) / 2, (t + w) / 2
		end
		return 0, w
	end
	local outlineSegs = {} -- the target: edge, back line, base end
	for k = 1, 2 * (N - 1) + 1 do
		outlineSegs[k] = bar(Color3.new(1, 1, 1), 0, 5)
	end
	-- Fit the blank to the plot (on its first draw and whenever the plot's width changes): px per cm and where cm 0,0 is.
	local scale, origin, colW, laidOutFor = 1, Vector2.zero, 2, -1
	local function toPx(p: Vector2): Vector2
		return origin + p * scale
	end
	local function edgePx(f: number, width: number): Vector2
		return toPx(sampleAt(spineAt, f)) + sampleAt(toEdge, f).Unit * width * scale
	end
	local function layout(): boolean
		local w = plot.AbsoluteSize.X / math.max(fit.Scale, 0.01) -- the UIScale shrinks AbsoluteSize; offsets are unscaled
		if w <= 0 then
			return false
		end
		if w == laidOutFor then
			return true
		end
		laidOutFor = w
		local lo, hi = Vector2.new(math.huge, math.huge), Vector2.new(-math.huge, -math.huge)
		for i = 1, N do
			local a, b = span(state.blank, state.target[i])
			for _, p in { spineAt[i] + toEdge[i] * a, spineAt[i] + toEdge[i] * b } do
				lo = Vector2.new(math.min(lo.X, p.X), math.min(lo.Y, p.Y))
				hi = Vector2.new(math.max(hi.X, p.X), math.max(hi.Y, p.Y))
			end
		end
		local span = hi - lo
		scale = (w - 2 * PAD) / span.X
		plotH = math.clamp(span.Y * scale + 2 * PAD, PLOT_MIN, PLOT_MAX)
		scale = math.min(scale, (plotH - 2 * PAD) / span.Y)
		plot.Size = UDim2.new(1, 0, 0, plotH)
		panel.Size = UDim2.new(1, -24, 0, plotH + 90)
		origin = Vector2.new(w - span.X * scale, plotH - span.Y * scale) / 2 - lo * scale
		colW = math.ceil((spineAt[N] - spineAt[1]).Magnitude * scale / (COLS - 1)) + 1
		for i = 1, N - 1 do
			strip(outlineSegs[i], edgePx(i, state.target[i]), edgePx(i + 1, state.target[i + 1]), 2)
			strip(outlineSegs[N - 1 + i], toPx(spineAt[i]), toPx(spineAt[i + 1]), 2)
		end
		strip(outlineSegs[2 * (N - 1) + 1], toPx(spineAt[1]), edgePx(1, state.target[1]), 2)
		return true
	end
	local band = bar(AIM, 0.82, 3)
	local aimLine = bar(AIM, 0.1, 6)
	aimLine.AnchorPoint = Vector2.new(0.5, 0)
	aimLine.Size = UDim2.new(0, 2, 1, 0)
	local arrow = text(plot, "", 18, NARROW)
	arrow.AnchorPoint = Vector2.new(0.5, 0)
	arrow.Size = UDim2.fromOffset(20, 18)
	arrow.ZIndex = 7
	local readout = text(plot, "", 13, TEXT)
	readout.AnchorPoint = Vector2.new(0.5, 0)
	readout.Size = UDim2.fromOffset(90, 16)
	readout.ZIndex = 7
	readout.TextStrokeTransparency = 0.2 -- readable over the coloured fills
	local worstMark = text(plot, "▼", 14, TOO_NARROW)
	worstMark.AnchorPoint = Vector2.new(0.5, 1)
	worstMark.Size = UDim2.fromOffset(16, 12)
	worstMark.ZIndex = 7

	local row = Instance.new("Frame")
	row.AnchorPoint = Vector2.new(1, 1)
	row.Position = UDim2.new(1, -12, 1, -12)
	row.Size = UDim2.fromOffset(600, 40)
	row.BackgroundTransparency = 1
	local list = Instance.new("UIListLayout")
	list.FillDirection = Enum.FillDirection.Horizontal
	list.HorizontalAlignment = Enum.HorizontalAlignment.Right
	list.Padding = UDim.new(0, 8)
	list.SortOrder = Enum.SortOrder.LayoutOrder
	list.Parent = row
	row.Parent = gui
	local turnButton = button(row, "Turn blade · R", 150)
	local sandButton = button(row, "Sand", 100)
	local finishButton = button(row, "Finish", 100)
	local resetButton = button(row, "Reset blank", 120)
	local exitButton = button(row, "Exit", 80)
	for k, b in { turnButton, sandButton, finishButton, resetButton, exitButton } do
		b.LayoutOrder = k
	end
	local presetButton: TextButton? = nil
	if RunService:IsStudio() then
		local holder = Instance.new("Frame")
		holder.Position = UDim2.fromOffset(12, 12)
		holder.Size = UDim2.fromOffset(200, 34)
		holder.BackgroundTransparency = 1
		holder.Parent = gui
		presetButton = button(holder, "Dev: narrow-tip preset", 200)
		;(presetButton :: TextButton).TextSize = 14
	end
	local strikeButton: TextButton? = nil
	if UserInputService.TouchEnabled then
		local holder = Instance.new("Frame")
		holder.AnchorPoint = Vector2.new(1, 1)
		holder.Position = UDim2.new(1, -24, 1, -64)
		holder.Size = UDim2.fromOffset(110, 110)
		holder.BackgroundTransparency = 1
		holder.Parent = gui
		strikeButton = button(holder, "Strike", 110)
		;(strikeButton :: TextButton).TextSize = 22
		corner(strikeButton :: TextButton, 55)
	end

	local card = Instance.new("Frame")
	card.AnchorPoint = Vector2.new(0.5, 0.5)
	card.Position = UDim2.fromScale(0.5, 0.4)
	card.Size = UDim2.fromOffset(400, 196)
	card.BackgroundColor3 = PANEL
	card.Visible = false
	corner(card, 14)
	card.Parent = gui
	local cardScore = text(card, "", 30, GOLD)
	cardScore.Position = UDim2.fromOffset(0, 18)
	cardScore.Size = UDim2.new(1, 0, 0, 34)
	local cardLines = text(card, "", 15, TEXT)
	cardLines.Position = UDim2.fromOffset(16, 60)
	cardLines.Size = UDim2.new(1, -32, 0, 60)
	cardLines.TextWrapped = true
	local cardRow = Instance.new("Frame")
	cardRow.AnchorPoint = Vector2.new(0.5, 1)
	cardRow.Position = UDim2.new(0.5, 0, 1, -16)
	cardRow.Size = UDim2.fromOffset(300, 40)
	cardRow.BackgroundTransparency = 1
	local cardList = list:Clone()
	cardList.HorizontalAlignment = Enum.HorizontalAlignment.Center
	cardList.Parent = cardRow
	cardRow.Parent = card
	local keepButton = button(cardRow, "Keep shaping", 140)
	local againButton = button(cardRow, "New blank", 120)
	againButton.LayoutOrder = 2

	-- ---------- state of play ----------
	local side = "edge" -- "edge" narrows, "flat" widens
	local tool = "hammer" -- or "sand" (Refinements 5)
	local sanding = false -- the mouse / a finger held down with the sanding block out
	local hammering = false -- the mouse / Strike held with the hammer out: strikes keep coming, wherever you aim
	local hammerInput: InputObject? = nil -- the touch holding Strike
	local aimU = 0.5
	local smoothU = aimU
	local lockedU: number? = nil -- where a strike in progress lands
	local busy = false
	local queued: string? = nil
	local flash, flashU = 0, 0
	local paintedU = -1
	local lastImpact: any = nil
	local stats = { strikes = 0, turns = 0, corrections = 0, worse = 0, smooths = 0, started = nil :: number?, history = {} :: { { number } }, preset = false }

	local function place(u: number): string
		return if u < 0.34 then "near the base" elseif u < 0.67 then "in the middle" else "near the point"
	end
	local function cm(e: number): string
		return string.format("%.2f cm", math.abs(e))
	end

	local function drawScore()
		if layout() then
			for k = 1, COLS do
				local f = 1 + (k - 1) / SUB
				local w, t = math.min(sampleAt(shown, f), state.maxWidth), sampleAt(state.target, f)
				local lo, hi = span(w, t)
				local close = math.abs(w - t) <= state.perfect
				local strength = math.min(math.abs(w - t) / (0.4 * state.k), 1)
				local c = cols[k]
				local function piece(frame: Frame, a: number, b: number, transparency: number)
					frame.Visible = b > a + 1e-6
					if frame.Visible then
						strip(frame, edgePx(f, a), edgePx(f, b), colW)
						frame.BackgroundTransparency = transparency
					end
				end
				if close then
					piece(c.body, lo, hi, 0)
					c.wideA.Visible, c.wideB.Visible, c.gapA.Visible, c.gapB.Visible = false, false, false, false
				else
					piece(c.body, math.max(lo, 0), math.min(hi, t), 0)
					piece(c.wideA, lo, math.min(0, hi), 0.45 - 0.4 * strength)
					piece(c.wideB, math.max(t, lo), hi, 0.45 - 0.4 * strength)
					piece(c.gapA, 0, math.min(lo, t), 0.6 - 0.45 * strength)
					piece(c.gapB, math.max(hi, 0), t, 0.6 - 0.45 * strength)
				end
			end
		end
		local score, worst, worstE = Rules.score(state, shown)
		scoreLabel.Text = string.format("Shape match %d%%", math.floor(score + 0.5))
		worstMark.Visible = math.abs(worstE) > state.flag
		local mark = toPx(spineAt[worst])
		worstMark.Position = UDim2.fromOffset(mark.X, mark.Y - 1)
		worstMark.TextColor3 = if worstE > 0 then TOO_WIDE else TOO_NARROW
		end

	-- Where the tool is aimed, on the silhouette (every frame: the aim, the shape and the side all move it).
	local function drawAim()
		if not layout() then
			return
		end
		local u = lockedU or aimU
		local reach = if tool == "sand" then C.sandRadius else C.radius
		local function xOf(v: number): number
			return toPx(sampleAt(spineAt, math.clamp(v, 0, 1) * (N - 1) + 1)).X
		end
		local x0, x1 = xOf(u - reach), xOf(u + reach)
		band.Position = UDim2.fromOffset(x0, 0)
		band.Size = UDim2.new(0, x1 - x0, 1, 0)
		aimLine.Position = UDim2.fromOffset(xOf(u), 0)
		local f = u * (N - 1) + 1
		local w, t = sampleAt(shown, f), sampleAt(state.target, f)
		local _, reachOut = span(w, t)
		local tip = edgePx(f, math.max(reachOut, t))
		local y = math.min(tip.Y + 4, plotH - 34)
		arrow.Text = if tool == "sand" then "▲" elseif side == "edge" then "▲" else "▼"
		arrow.TextColor3 = if tool == "sand" then GOLD elseif side == "edge" then NARROW else WIDEN
		arrow.Position = UDim2.fromOffset(tip.X, y)
		readout.Position = UDim2.fromOffset(tip.X, y + 17)
		local e = w - t
		if math.abs(e) <= state.perfect then
			readout.Text, readout.TextColor3 = "on the line", Color3.fromRGB(150, 230, 140)
		else
			readout.Text = cm(e) .. (if e > 0 then " wide" else " narrow")
			readout.TextColor3 = if e > 0 then TOO_WIDE:Lerp(Color3.new(1, 1, 1), 0.3) else TOO_NARROW:Lerp(Color3.new(1, 1, 1), 0.3)
		end
	end

	local function drawSide()
		if tool == "sand" then
			chip.Text, chip.BackgroundColor3 = "SAND · DOWN TO THE LINE", GOLD
		else
			chip.Text = if side == "edge" then "EDGE UP · NARROWS" else "FLAT · WIDENS"
			chip.BackgroundColor3 = if side == "edge" then NARROW else WIDEN
		end
		sandButton.Text = if tool == "sand" then "Hammer" else "Sand"
	end

	-- Hot steel, red where it's too wide and blue where it's too narrow (as the diagram was), brighter where the tool is
	-- aimed, flashing where it just struck.
	local stationColors = table.create(N, HOT)
	local function paint()
		local u = lockedU or smoothU
		for i = 1, N do
			local e = shown[i] - state.target[i]
			local off = math.max(0, math.abs(e) - state.perfect)
			local c = HOT:Lerp(if e > 0 then TOO_WIDE else TOO_NARROW, math.min(off / (0.3 * state.k), 1) * 0.85 * state.mask[i])
			c = c:Lerp(AIM, 0.45 * Rules.falloff(state.u[i] - u, if tool == "sand" then C.sandRadius else C.radius))
			if flash > 0 then
				c = c:Lerp(FLASH, flash * Rules.falloff(state.u[i] - flashU, C.radius))
			end
			stationColors[i] = c
		end
		for v = 1, view.vertexCount do
			view.mesh:SetColor(view.colorIds[v], stationColors[BladeCore.stationOfVertex(v, N)])
		end
		paintedU = u
		shapeChanged = false
	end

	-- ---------- aiming ----------
	local stationX = table.create(N, 0)
	local LO, HI = C.base[1], C.tip[1]
	local function uOfX(x: number): number
		if x <= stationX[1] then
			return LO
		end
		for i = 1, N - 1 do
			if x <= stationX[i + 1] then
				local u = state.u[i] + (state.u[i + 1] - state.u[i]) * (x - stationX[i]) / (stationX[i + 1] - stationX[i])
				return math.clamp(u, LO, HI)
			end
		end
		return HI
	end
	local function aimAtRay(ray: Ray)
		if math.abs(ray.Direction.Y) < 1e-4 then
			return
		end
		local t = (ORIGIN.Y + 0.05 - ray.Origin.Y) / ray.Direction.Y
		if t > 0 then
			aimU = uOfX(ORIGIN:PointToObjectSpace(ray.Origin + ray.Direction * t).X)
		end
	end
	local function aimAtPlot(x: number)
		if not layout() then
			return
		end
		local lx = (x - plot.AbsolutePosition.X) / math.max(fit.Scale, 0.01)
		local u = HI
		for i = 1, N - 1 do
			local a, b = toPx(spineAt[i]).X, toPx(spineAt[i + 1]).X
			if lx <= b then
				u = state.u[i] + (state.u[i + 1] - state.u[i]) * math.clamp((lx - a) / (b - a), 0, 1)
				break
			end
		end
		aimU = math.clamp(u, LO, HI)
	end

	-- ---------- strike and turn ----------
	local strike: () -> ()
	local turn: () -> ()
	local function runQueued()
		local q = queued or (if hammering and tool == "hammer" and not card.Visible then "strike" else nil)
		queued = nil
		if q == "strike" then
			task.spawn(strike)
		elseif q == "turn" then
			task.spawn(turn)
		end
	end

	strike = function()
		if busy then
			queued = "strike"
			return
		end
		busy = true
		local u = aimU
		local dir = if side == "edge" then -1 else 1
		lockedU = u
		tween(T.windup, function(t)
			hammerHeight = HOVER + (RAISE - HOVER) * easeOut(t)
		end)
		tween(T.drop, function(t)
			hammerHeight = RAISE * (1 - easeIn(t))
		end)
		-- impact: note where the face came down, against where the player aimed
		local aimedX = stationX[1]
		for i = 1, N - 1 do
			if state.u[i + 1] >= u then
				aimedX = stationX[i] + (stationX[i + 1] - stationX[i]) * (u - state.u[i]) / (state.u[i + 1] - state.u[i])
				break
			end
		end
		placeHammer(contactAt(u)) -- the frame's own placement runs after this; measure the face where it lands
		lastImpact = { u = u, side = side, faceX = ORIGIN:PointToObjectSpace((head.CFrame * CFrame.new(-HEAD / 2, 0, 0)).Position).X, aimedX = aimedX }
		local centre = math.clamp(math.floor(u * (N - 1) + 0.5) + 1, 1, N)
		local errBefore = math.abs(state.width[centre] - state.target[centre])
		local before = table.clone(state.width)
		Rules.strike(state, u, dir)
		stats.started = stats.started or os.clock()
		stats.strikes += 1
		if math.abs(state.width[centre] - state.target[centre]) > errBefore then
			stats.worse += 1
		end
		for k = #stats.history, 1, -1 do -- reversing the last nearby strike's direction = a correction
			local h = stats.history[k]
			if math.abs(h[1] - u) < C.radius then
				if h[2] ~= dir then
					stats.corrections += 1
				end
				break
			end
		end
		table.insert(stats.history, { u, dir })
		local contact = contactAt(u)
		sparkPoint.WorldPosition = contact
		sparks:Emit(10)
		clang.PlaybackSpeed = (if dir < 0 then 1.12 else 0.94) * (0.97 + math.random() * 0.06)
		clang.TimePosition = 0
		clang:Play()
		flash, flashU = 1, u
		parallel(function()
			tween(T.deform, function(t)
				local e = easeOut(t)
				for i = 1, N do
					shown[i] = before[i] + (state.width[i] - before[i]) * e
				end
				refreshMesh()
				drawScore()
			end)
		end, function()
			tween(T.recover, function(t)
				hammerHeight = HOVER * easeOut(t)
			end)
		end)
		lockedU = nil
		busy = false
		runQueued()
	end

	turn = function()
		if busy then
			queued = "turn"
			return
		end
		busy = true
		side = if side == "edge" then "flat" else "edge"
		stats.turns += 1
		drawSide()
		local from, to = roll, ROLL[side]
		local lift0, lift1 = lift, liftFor(to)
		local clear = 0.12 + (state.blank * S) / 2
		tween(T.turn, function(t)
			local e = easeInOut(t)
			roll = from + (to - from) * e
			lift = lift0 + (lift1 - lift0) * e + math.sin(math.pi * t) * clear
			hammerHeight = HOVER + math.sin(math.pi * t) * 0.35
			placeBlade()
		end)
		roll, lift = to, lift1
		placeBlade()
		busy = false
		runQueued()
	end

	-- Hammer ⇄ sanding block. Sanding itself runs every frame while held (RenderStepped below).
	local function swapTool()
		if busy then
			return
		end
		tool = if tool == "sand" then "hammer" else "sand"
		sanding, hammering = false, false
		if strikeButton then
			(strikeButton :: TextButton).Visible = tool == "hammer"
		end
		drawSide()
		drawScore()
	end

	local function newAttempt(preset: boolean)
		if preset then
			Rules.preset(state)
		else
			Rules.reset(state)
		end
		shown = table.clone(state.width)
		side, roll = "edge", ROLL.edge
		lift = liftFor(roll)
		placeBlade()
		refreshMesh()
		stats = { strikes = 0, turns = 0, corrections = 0, worse = 0, smooths = 0, started = nil, history = {}, preset = preset }
		card.Visible = false
		if tool == "sand" then
			swapTool()
		end
		drawScore()
		drawSide()
	end

	local function finish()
		local score, worst, worstE = Rules.score(state)
		local seconds = if stats.started then os.clock() - stats.started else 0
		local attempt = {
			score = score,
			seconds = seconds,
			strikes = stats.strikes,
			corrections = stats.corrections,
			worse = stats.worse,
			turns = stats.turns,
			smooths = stats.smooths,
			worstU = state.u[worst],
			worstCm = worstE,
			preset = stats.preset,
		}
		table.insert(Shaping.attempts, attempt)
		print(string.format("[Shaping] attempt %d%s: match %.1f%%, %d s, %d strikes, %d corrections, %d made it worse, %d turns, %d smooths, worst %+.2f cm at %.2f",
			#Shaping.attempts, if stats.preset then " (preset)" else "", score, math.floor(seconds + 0.5), stats.strikes, stats.corrections,
			stats.worse, stats.turns, stats.smooths, worstE, state.u[worst]))
		cardScore.Text = string.format("Shape match %d%%", math.floor(score + 0.5))
		local worstLine = if math.abs(worstE) > state.flag
			then `Worst spot: {cm(worstE)} too {if worstE > 0 then "wide" else "narrow"} {place(state.u[worst])}`
			else "No spot off by more than " .. cm(state.flag)
		cardLines.Text = string.format("%s\n%d:%02d · %d strikes · %d corrections · %d turns%s", worstLine,
			seconds // 60, math.floor(seconds % 60), stats.strikes, stats.corrections, stats.turns, if stats.smooths > 0 then " · sanded" else "")
		card.Visible = true
	end

	-- ---------- camera, controls, input ----------
	local previousType, previousFov, previousSubject = camera.CameraType, camera.FieldOfView, camera.CameraSubject
	local FOV = 30
	local function cameraFrame(): CFrame
		local vp = camera.ViewportSize
		local aspect = vp.X / math.max(1, vp.Y)
		local hHalf = math.atan(math.tan(math.rad(FOV / 2)) * aspect)
		local spanHalf = (bladeLen + tangLen + 1.6) / 2
		local dist = spanHalf / math.tan(hHalf)
		local look = ORIGIN * Vector3.new(midX - tangLen / 2 - 0.4, 0.05, 0) -- the blade itself, mid-screen (Refinements 5: it sat high, room for the old bottom panel)
		local cf = CFrame.lookAt(look + TOWARD_CAMERA * dist, look)
		local studsPerPx = 2 * dist * math.tan(math.rad(FOV / 2)) / math.max(1, vp.Y)
		local lowerBy = (panel.AbsoluteSize.Y + 12 - 52) / 2 -- px: half of (the panel on top minus the buttons below)
		return cf + cf.UpVector * lowerBy * studsPerPx
	end
	-- The place's PlayerModule has no GetControls, so the character is held still through its Humanoid.
	local character = player.Character
	local humanoid = character and character:FindFirstChildOfClass("Humanoid")
	local held = humanoid and { walk = humanoid.WalkSpeed, jump = humanoid.JumpPower, height = humanoid.JumpHeight }
	if humanoid then
		humanoid.WalkSpeed, humanoid.JumpPower, humanoid.JumpHeight = 0, 0, 0
	end
	-- Every other screen (HUD, hotbar, DevPanel, billboards) is switched off and put back as it was on Exit.
	local hiddenGuis: { [LayerCollector]: boolean } = {}
	for _, g in player:WaitForChild("PlayerGui"):GetChildren() do
		if g:IsA("LayerCollector") and g.Enabled then
			hiddenGuis[g] = true
			g.Enabled = false
		end
	end

	local connections: { RBXScriptConnection } = {}
	local function connect(signal: RBXScriptSignal, fn: (...any) -> ())
		table.insert(connections, signal:Connect(fn))
	end
	local stop: () -> ()

	ContextActionService:BindActionAtPriority("ShapingTurn", function(_, inputState)
		if inputState == Enum.UserInputState.Begin then
			task.spawn(turn)
		end
		return Enum.ContextActionResult.Sink
	end, false, 3000, Enum.KeyCode.R)
	connect(UserInputService.InputBegan, function(input: InputObject, processed: boolean)
		if processed or card.Visible then
			return
		end
		local kind = input.UserInputType
		if kind == Enum.UserInputType.MouseButton1 or kind == Enum.UserInputType.Touch then
			aimAtRay(camera:ScreenPointToRay(input.Position.X, input.Position.Y))
			if tool == "sand" then
				sanding = true
				stats.started = stats.started or os.clock()
				stats.smooths += 1 -- sanding passes
			elseif kind == Enum.UserInputType.MouseButton1 then
				hammering = true
				task.spawn(strike)
			end
		end
	end)
	connect(UserInputService.InputEnded, function(input: InputObject)
		if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
			sanding = false
		end
		if input.UserInputType == Enum.UserInputType.MouseButton1 or input == hammerInput then
			hammering, hammerInput = false, nil
		end
	end)
	connect(UserInputService.InputChanged, function(input: InputObject, processed: boolean)
		if processed then
			return
		end
		if input.UserInputType == Enum.UserInputType.MouseMovement or input.UserInputType == Enum.UserInputType.Touch then
			aimAtRay(camera:ScreenPointToRay(input.Position.X, input.Position.Y))
		end
	end)
	for _, signal in { plot.InputBegan, plot.InputChanged } do
		connect(signal, function(input: InputObject)
			local kind = input.UserInputType
			if kind == Enum.UserInputType.MouseMovement or kind == Enum.UserInputType.Touch or kind == Enum.UserInputType.MouseButton1 then
				aimAtPlot(input.Position.X)
			end
		end)
	end
	connect(turnButton.Activated, function()
		task.spawn(turn)
	end)
	local saving = false
	connect(finishButton.Activated, function()
		if not onFinish then
			finish()
		elseif not saving and not busy then -- the Test Anvil: hand the match over and leave once it's saved
			saving = true
			local saved = onFinish((Rules.score(state)), table.clone(state.width))
			saving = false
			if saved then
				stop()
			end
		end
	end)
	connect(sandButton.Activated, swapTool)
	connect(resetButton.Activated, function()
		newAttempt(false)
	end)
	connect(exitButton.Activated, function()
		stop()
	end)
	connect(keepButton.Activated, function()
		card.Visible = false
	end)
	connect(againButton.Activated, function()
		newAttempt(false)
	end)
	if presetButton then
		connect(presetButton.Activated, function()
			newAttempt(true)
		end)
	end
	if strikeButton then
		connect(strikeButton.InputBegan, function(input: InputObject)
			if input.UserInputType == Enum.UserInputType.Touch or input.UserInputType == Enum.UserInputType.MouseButton1 then
				hammering, hammerInput = true, input
				task.spawn(strike)
			end
		end)
	end

	connect(RunService.RenderStepped, function(dt: number)
		-- The default camera scripts take the camera back; hold it every frame.
		camera.CameraType = Enum.CameraType.Scriptable
		camera.FieldOfView = FOV
		camera.CFrame = cameraFrame()
		local now = os.clock()
		for i = #tweens, 1, -1 do
			local tw = tweens[i]
			local t = math.clamp((now - tw.start) / tw.duration, 0, 1)
			tw.fn(t)
			if t >= 1 then
				table.remove(tweens, i)
				tw.done()
			end
		end
		if lockedU then
			smoothU = lockedU
		else
			smoothU += (aimU - smoothU) * (1 - math.exp(-dt * 20))
		end
		if sanding and tool == "sand" and not busy and Rules.sand(state, smoothU, dt) > 0 then
			table.move(state.width, 1, N, 1, shown)
			refreshMesh()
			drawScore()
			if math.random() < 0.5 then
				sparkPoint.WorldPosition = contactAt(smoothU)
				sparks:Emit(1)
			end
		end
		local flashing = flash > 0
		flash = math.max(0, flash - dt / FLASH_TIME)
		if flashing or shapeChanged or math.abs(smoothU - paintedU) > 0.002 then
			paint()
		end
		drawAim()
		local sandOut = tool == "sand"
		head.Transparency = if sandOut then 1 else 0
		handle.Transparency = head.Transparency
		sandBlock.Transparency = if sandOut then 0 else 1
		if sandOut then
			local scrub = if sanding then math.sin(os.clock() * 30) * 0.06 else 0
			sandBlock.CFrame = CFrame.new(contactAt(smoothU) + Vector3.new(scrub, if sanding then 0.07 else 0.17, 0))
		else
			placeHammer(contactAt(smoothU))
		end
	end)

	stop = function()
		ContextActionService:UnbindAction("ShapingTurn")
		for _, c in connections do
			c:Disconnect()
		end
		table.clear(tweens)
		gui:Destroy()
		folder:Destroy()
		view:destroy()
		camera.CameraType = previousType
		camera.FieldOfView = previousFov
		camera.CameraSubject = previousSubject
		if humanoid and held and humanoid.Parent then
			humanoid.WalkSpeed, humanoid.JumpPower, humanoid.JumpHeight = held.walk, held.jump, held.height
		end
		for g in hiddenGuis do
			if g.Parent then
				g.Enabled = true
			end
		end
		Shaping.current = nil
	end

	-- first frame
	roll = 0
	placeBlade()
	for i = 1, N do -- where each station sits along the anvil; turning about the length never moves these
		stationX[i] = ORIGIN:PointToObjectSpace(topOf(i)).X
	end
	roll = ROLL.edge
	lift = liftFor(roll)
	placeBlade()
	folder.Parent = Workspace
	gui.Parent = player:WaitForChild("PlayerGui")
	paint()
	drawScore()
	drawSide()

	-- For playtest checks (reads only; play goes through the controls above). Also as a BindableFunction, since the
	-- command bar and plugins have their own require cache: workspace.ShapingPrototype.Inspect:Invoke().
	local function info()
		local score, worst, worstE = Rules.score(state)
		return {
			widths = table.clone(state.width),
			target = table.clone(state.target),
			side = side,
			roll = roll,
			aimU = aimU,
			busy = busy,
			score = score,
			worst = worst,
			worstCm = worstE,
			strikes = stats.strikes,
			corrections = stats.corrections,
			turns = stats.turns,
			smooths = stats.smooths,
			hammering = hammering,
			tool = tool,
			hammer = head.Position,
			impact = lastImpact,
			attempts = Shaping.attempts,
		}
	end
	local inspect = Instance.new("BindableFunction")
	inspect.Name = "Inspect"
	inspect.OnInvoke = info
	inspect.Parent = folder
	Shaping.current = { stop = stop, info = info }
end

return Shaping

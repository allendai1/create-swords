--!strict
-- Client probe: forges one blade on an EditableMesh with the browser study's flow, to test
-- feasibility in Studio. Test-only: BladeProbeLoader starts it when workspace has the attribute
-- BladeProbe = true (or a blueprint id such as "katana"). It does not touch the real
-- AnvilController and sends nothing to the server.
--
-- Controls: Space or click to strike (one buffered tap while the hammer is busy). After 12 strikes,
-- hold the mouse on the edge and drag to grind. R restarts. Timings print to the Output window and
-- are stored as workspace attributes (BladeProbeStrikeMs, BladeProbeFrameMsMax).

local AssetService = game:GetService("AssetService")
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local UserInputService = game:GetService("UserInputService")
local Workspace = game:GetService("Workspace")

local Shared = script.Parent
local BladeCore = require(Shared:WaitForChild("BladeCore")) :: any
local BladeData = require(Shared:WaitForChild("BladeData")) :: any

local BladeProbe = {}
BladeProbe.current = nil :: any

-- ---------- exploratory pacing and scale (not approved) ----------
local STUDS_PER_CM = 0.1 -- katana ≈ 7 studs, tantō ≈ 2.6 studs
local TIMING = { windup = 0.13, drop = 0.06, deform = 0.09, recover = 0.22, move = 0.34, cool = 0.9 }
local REST, WIND, PARKED = -0.38, -0.62, -1.15
local HANDLE = 1.5 -- studs
local HEAD_HALF = 0.22
local HOT = Color3.fromRGB(190, 70, 22)

type Tween = { start: number, duration: number, fn: (number) -> (), done: () -> () }

local function lerp(a: number, b: number, t: number): number
	return a + (b - a) * t
end
local function easeOut(t: number): number
	return 1 - (1 - t) ^ 3
end
local function easeIn(t: number): number
	return t * t * t
end
local function easeInOut(t: number): number
	return if t < 0.5 then 4 * t * t * t else 1 - (-2 * t + 2) ^ 3 / 2
end

function BladeProbe.start(blueprintId: string?)
	local profile = BladeData.profiles[blueprintId or "tanto"] or BladeData.profiles.tanto
	local blade = BladeCore.createBlade(BladeData.blank, profile)
	local N: number = blade.stations
	local state = BladeCore.createState(blade)
	local params = BladeCore.stationParams(blade, state)

	local folder = Instance.new("Folder")
	folder.Name = "BladeProbe"
	folder.Parent = Workspace

	-- Where the blade sits: the anvil's BladeMount if the place has one, else a stand-in anvil.
	local origin = CFrame.new(0, 4, 0)
	local smithy = Workspace:FindFirstChild("Smithy")
	local anvil = smithy and smithy:FindFirstChild("Anvil")
	local mount = anvil and anvil:FindFirstChild("BladeMount")
	if mount and mount:IsA("BasePart") then
		origin = CFrame.new(mount.Position + Vector3.new(0, mount.Size.Y / 2, 0))
	else
		local block = Instance.new("Part")
		block.Name = "ProbeAnvil"
		block.Anchored = true
		block.Size = Vector3.new(2.4, 1, 0.8)
		block.CFrame = origin * CFrame.new(0, -0.5, 0)
		block.Color = Color3.fromRGB(45, 44, 46)
		block.Material = Enum.Material.Metal
		block.Parent = folder
	end

	-- ---------- mesh ----------
	local mesh = AssetService:CreateEditableMesh()
	local vertexCount: number = BladeCore.vertexCount(N)
	local index: { number } = BladeCore.buildIndex(N)
	local positions: { number } = BladeCore.buildPositions(params)
	local vertexIds: { number } = table.create(vertexCount, 0)
	local colorIds: { number } = table.create(vertexCount, 0)
	local function vec(v: number): Vector3
		local o = (v - 1) * 3
		return Vector3.new(positions[o + 1], positions[o + 2], positions[o + 3]) * STUDS_PER_CM
	end
	for v = 1, vertexCount do
		vertexIds[v] = mesh:AddVertex(vec(v))
		colorIds[v] = mesh:AddColor(Color3.new(1, 1, 1), 1)
	end
	local firstVertexOfFace: { [number]: number } = {} -- face id → one of its layout vertices
	for t = 1, #index, 3 do
		local a, b, c = index[t], index[t + 1], index[t + 2]
		local face = mesh:AddTriangle(vertexIds[a], vertexIds[b], vertexIds[c])
		mesh:SetFaceColors(face, { colorIds[a], colorIds[b], colorIds[c] })
		firstVertexOfFace[face] = a
	end
	-- Normals are automatic, as in Shared/BladeMesh: crease vertices are duplicated in the layout,
	-- so bevels stay crisp. A MeshPart's bounds are fixed when it is created, so a zero-area triangle
	-- spans the furthest the blade can reach; the part's local origin is then the blade's base.
	local reachStuds = (BladeData.blank.length + profile.stages.refined.length + profile.stages.preform.length) * STUDS_PER_CM
	mesh:AddTriangle(
		mesh:AddVertex(Vector3.new(-reachStuds, -0.5, -reachStuds)),
		mesh:AddVertex(Vector3.new(reachStuds, 0.5, reachStuds)),
		mesh:AddVertex(Vector3.new(reachStuds, 0.5, reachStuds))
	)

	local function updateMesh()
		BladeCore.buildPositions(params, positions)
		for v = 1, vertexCount do
			mesh:SetPosition(vertexIds[v], vec(v))
		end
	end

	-- Dull steel brightens per section as it is ground; bevels catch more light than the flats.
	local DULL_FLAT, BRIGHT_FLAT = Color3.new(0.2, 0.2, 0.21), Color3.new(0.56, 0.57, 0.6)
	local DULL_BEVEL, BRIGHT_BEVEL = Color3.new(0.27, 0.27, 0.28), Color3.new(0.95, 0.96, 0.98)
	local hot = true
	local function updateColors()
		for v = 1, vertexCount do
			if hot then
				mesh:SetColor(colorIds[v], Color3.new(1, 1, 1))
				continue
			end
			local r: number = state.refinement[BladeCore.stationOfVertex(v, N)]
			local bevel = BladeCore.BEVEL_RING[BladeCore.ringOfVertex(v, N)] == true
			local color = if bevel then DULL_BEVEL:Lerp(BRIGHT_BEVEL, r) else DULL_FLAT:Lerp(BRIGHT_FLAT, r)
			mesh:SetColor(colorIds[v], color)
		end
	end

	updateColors()
	local part = AssetService:CreateMeshPartAsync(Content.fromObject(mesh))
	part.Name = "ProbeBlade"
	part.Anchored = true
	part.CanCollide = false
	part.CanQuery = true
	part.Material = Enum.Material.Metal
	part.Parent = folder

	-- ---------- hammer (fixed point) ----------
	local hammerPivot = Instance.new("Part")
	hammerPivot.Name = "ProbeHammer"
	hammerPivot.Anchored = true
	hammerPivot.CanCollide = false
	hammerPivot.Transparency = 1
	hammerPivot.Size = Vector3.new(0.1, 0.1, 0.1)
	hammerPivot.Parent = folder
	local handle = Instance.new("Part")
	handle.Anchored = true
	handle.CanCollide = false
	handle.Size = Vector3.new(0.08, 0.08, HANDLE)
	handle.Color = Color3.fromRGB(90, 62, 40)
	handle.Parent = folder
	local head = Instance.new("Part")
	head.Shape = Enum.PartType.Cylinder
	head.Anchored = true
	head.CanCollide = false
	head.Size = Vector3.new(HEAD_HALF * 2, 0.32, 0.32)
	head.Color = Color3.fromRGB(61, 61, 64)
	head.Material = Enum.Material.Metal
	head.Parent = folder
	local hammerAngle = REST
	local HAMMER_PIVOT_Y = 0.12 + HEAD_HALF
	local function placeHammer()
		local pivotCf = origin * CFrame.new(0, HAMMER_PIVOT_Y, -HANDLE) * CFrame.Angles(hammerAngle, 0, 0)
		handle.CFrame = pivotCf * CFrame.new(0, 0, HANDLE / 2)
		head.CFrame = pivotCf * CFrame.new(0, 0, HANDLE) * CFrame.Angles(0, 0, math.pi / 2)
	end
	local function contactAngle(y: number): number
		return math.asin(math.clamp((HAMMER_PIVOT_Y - HEAD_HALF - y) / HANDLE, -0.5, 0.5))
	end

	-- ---------- pose: put a point of the blade under the hammer ----------
	local pose = { point = Vector3.zero, yaw = 0, flip = 0, thickness = 1, lift = 0 }
	local function applyPose()
		local pivotCf = origin
			* CFrame.new(0, (pose.thickness / 2) * STUDS_PER_CM + pose.lift, 0)
			* CFrame.Angles(0, pose.yaw, 0)
			* CFrame.Angles(pose.flip * math.pi, 0, 0)
		part.CFrame = pivotCf * CFrame.new(-pose.point * STUDS_PER_CM)
	end
	local function poseFor(target: any)
		return {
			point = Vector3.new(target.point[1], target.point[2], target.point[3]),
			yaw = (if target.flip then target.angle else -target.angle) + target.turn,
			flip = if target.flip then 1 else 0,
			thickness = target.thickness,
			halfWidth = target.halfWidth,
		}
	end

	-- ---------- tweens on RenderStepped ----------
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

	local frameMs: { number } = {}
	local function moveTo(nextPose: any, duration: number)
		local from = { point = pose.point, yaw = pose.yaw, flip = pose.flip, thickness = pose.thickness }
		local liftHeight = if from.flip ~= nextPose.flip then ((nextPose.halfWidth or 1.5) + 0.8) * STUDS_PER_CM else 0.025
		tween(duration, function(t)
			local e = easeInOut(t)
			pose.point = from.point:Lerp(nextPose.point, e)
			pose.yaw = lerp(from.yaw, nextPose.yaw, e)
			pose.flip = lerp(from.flip, nextPose.flip, e)
			pose.thickness = lerp(from.thickness, nextPose.thickness, e)
			pose.lift = math.sin(math.pi * t) * liftHeight
			applyPose()
		end)
		pose.lift = 0
		applyPose()
	end

	local mode = "ready"

	-- ---------- HUD ----------
	local player = Players.LocalPlayer
	local gui = Instance.new("ScreenGui")
	gui.Name = "BladeProbeHud"
	gui.ResetOnSpawn = false
	local label = Instance.new("TextLabel")
	label.Size = UDim2.new(0, 420, 0, 60)
	label.Position = UDim2.new(0, 16, 0, 16)
	label.BackgroundTransparency = 0.3
	label.BackgroundColor3 = Color3.fromRGB(21, 17, 14)
	label.TextColor3 = Color3.fromRGB(239, 230, 218)
	label.TextXAlignment = Enum.TextXAlignment.Left
	label.Font = Enum.Font.GothamMedium
	label.TextSize = 16
	label.Parent = gui
	gui.Parent = player:WaitForChild("PlayerGui")
	local STAGE_LINES = { lengthen = "Stage 1 of 3 · Lengthen", taper = "Stage 2 of 3 · Taper and curve", tip = "Stage 3 of 3 · Form the point" }
	local function updateHud()
		local q = BladeCore.displayQuality(blade, state)
		local line = if BladeCore.isRefined(blade, state) then "Finished · fully refined"
			elseif BladeCore.isForged(blade, state) then "Forged · hold and drag along the edge to grind"
			else `{STAGE_LINES[blade.recipe[state.strikeIndex + 1].stage]} · strike {state.strikeIndex + 1} of {#blade.recipe}`
		label.Text = `  {blade.name} probe   {q}%\n  {line}`
		-- Readable from the command bar or a test harness during play.
		Workspace:SetAttribute("BladeProbeMode", mode)
		Workspace:SetAttribute("BladeProbeStrikes", state.strikeIndex)
		Workspace:SetAttribute("BladeProbeQuality", BladeCore.quality(blade, state))
	end

	-- ---------- camera: slightly angled overhead, whole reach in view ----------
	local camera = Workspace.CurrentCamera
	local previousCameraType = camera.CameraType
	local cameraCf = camera.CFrame
	local function fitCamera(reachCm: number)
		local vHalf = math.rad(camera.FieldOfView / 2)
		local aspect = camera.ViewportSize.X / math.max(1, camera.ViewportSize.Y)
		local hHalf = math.atan(math.tan(vHalf) * aspect)
		local dist = (reachCm * STUDS_PER_CM) / math.tan(hHalf)
		local elevation = math.rad(64)
		cameraCf = CFrame.lookAt(origin.Position + Vector3.new(0, math.sin(elevation) * dist, math.cos(elevation) * dist), origin.Position)
	end
	local maxLength = math.max(BladeData.blank.length, profile.stages.lengthened.length, profile.stages.preform.length, profile.stages.refined.length)
	fitCamera(blade.tang.length + maxLength + 3)

	-- ---------- forging ----------
	local queued = false
	local strikeMs: { number } = {}
	local function contactY(target: any): number
		return (pose.thickness / 2 + target.thickness / 2) * STUDS_PER_CM
	end

	local strike: () -> ()
	local function finishForging()
		local mid = math.floor((N - 1) / 2) + 1
		local cl = BladeCore.centerline(params)
		local across = (params.spine[mid] + params.edge[mid]) / 2
		local centre = {
			point = Vector3.new(cl.px[mid] - math.sin(cl.angle[mid]) * across, 0, -(cl.py[mid] + math.cos(cl.angle[mid]) * across)),
			yaw = -cl.angle[mid],
			flip = 0,
			thickness = params.thick[mid],
			halfWidth = 1.5,
		}
		parallel(function()
			tween(0.5, function(t)
				hammerAngle = lerp(REST, PARKED, easeInOut(t))
				placeHammer()
			end)
		end, function()
			moveTo(centre, 0.6)
		end, function()
			-- Hot metal glows (Neon); once cool it turns to dull steel that grinding brightens.
			tween(TIMING.cool * 0.5, function(t)
				part.Color = HOT:Lerp(Color3.fromRGB(60, 20, 8), easeInOut(t))
			end)
			hot = false
			updateColors()
			part.Material = Enum.Material.Metal
			tween(TIMING.cool * 0.5, function(t)
				part.Color = Color3.fromRGB(60, 60, 64):Lerp(Color3.new(1, 1, 1), easeInOut(t))
			end)
		end)
		fitCamera(blade.tang.length + blade.length / 2 + 2)
		mode = "grind"
		updateHud()
		local avg = 0
		for _, ms in strikeMs do
			avg += ms
		end
		avg /= math.max(1, #strikeMs)
		local worst = 0
		for _, ms in frameMs do
			worst = math.max(worst, ms)
		end
		Workspace:SetAttribute("BladeProbeStrikeMs", avg)
		Workspace:SetAttribute("BladeProbeFrameMsMax", worst)
		print(string.format("[BladeProbe] %s forged: mesh update %.2f ms per deform frame on average, %.2f ms worst; %d vertices",
			blade.name, avg, worst, vertexCount))
	end

	strike = function()
		if mode ~= "ready" then
			if mode == "busy" and not BladeCore.isForged(blade, state) then
				queued = true
			end
			return
		end
		mode = "busy"
		local k = state.strikeIndex
		local target = BladeCore.strikeTarget(blade, params, k)
		local hitAngle = contactAngle(contactY(target))
		tween(TIMING.windup, function(t)
			hammerAngle = lerp(REST, WIND, easeOut(t))
			placeHammer()
		end)
		tween(TIMING.drop, function(t)
			hammerAngle = lerp(WIND, hitAngle, easeIn(t))
			placeHammer()
		end)
		local before = params
		state = BladeCore.applyStrike(blade, state)
		local after = BladeCore.stationParams(blade, state)
		updateHud()
		local scratch = {}
		parallel(function()
			tween(TIMING.deform, function(t)
				local t0 = os.clock()
				params = BladeCore.lerpParams(before, after, easeOut(t), scratch)
				updateMesh()
				local ms = (os.clock() - t0) * 1000
				table.insert(frameMs, ms)
				table.insert(strikeMs, ms)
				local p = BladeCore.strikeTarget(blade, params, k).point
				pose.point = Vector3.new(p[1], p[2], p[3])
				applyPose()
			end)
		end, function()
			tween(TIMING.recover, function(t)
				hammerAngle = lerp(hitAngle, REST, easeOut(t))
				placeHammer()
			end)
		end)
		params = after
		if BladeCore.isForged(blade, state) then
			queued = false
			finishForging()
			return
		end
		moveTo(poseFor(BladeCore.strikeTarget(blade, params, state.strikeIndex)), TIMING.move)
		mode = "ready"
		updateHud()
		if queued then
			queued = false
			task.spawn(strike)
		end
	end

	-- ---------- grinding ----------
	local grinding = false
	local lastLocal: Vector3? = nil
	local function grindAt(screen: Vector2)
		-- Raycast the mesh itself, not the MeshPart's collision box (which spans the fixed bounds).
		local ray = camera:ViewportPointToRay(screen.X, screen.Y)
		local localOrigin = part.CFrame:PointToObjectSpace(ray.Origin)
		local localDirection = part.CFrame:VectorToObjectSpace(ray.Direction * 500)
		-- Returns face id, hit position, barycentric weights, then the face's three vertex ids.
		local faceId, hitPosition = mesh:RaycastLocal(localOrigin, localDirection)
		local v = faceId and firstVertexOfFace[faceId]
		if not hitPosition or not v then
			lastLocal = nil
			return
		end
		local localCm = hitPosition / STUDS_PER_CM
		local best = BladeCore.stationOfVertex(v, N)
		local ring = BladeCore.ringOfVertex(v, N)
		local onEdge = BladeCore.BEVEL_RING[ring] == true or (ring == 0 and best == N)
		if lastLocal and onEdge then
			local cm = math.min(3, (localCm - lastLocal).Magnitude)
			if cm > 0.01 then
				local was = BladeCore.quality(blade, state)
				state = BladeCore.applyGrind(blade, state, (best - 1) / (N - 1), cm * BladeCore.GRIND_PER_CM)
				if BladeCore.quality(blade, state) > was then
					params = BladeCore.stationParams(blade, state)
					updateMesh()
					updateColors()
					updateHud()
				end
			end
		end
		lastLocal = localCm
		if BladeCore.isRefined(blade, state) then
			mode = "done"
			grinding = false
			updateHud()
		end
	end

	-- ---------- input and loop ----------
	local connections: { RBXScriptConnection } = {}
	local function restart() end
	table.insert(connections, UserInputService.InputBegan:Connect(function(input, processed)
		if processed then
			return
		end
		if input.KeyCode == Enum.KeyCode.R then
			restart()
		elseif input.KeyCode == Enum.KeyCode.Space or input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
			if mode == "grind" and input.KeyCode ~= Enum.KeyCode.Space then
				grinding = true
				lastLocal = nil
				grindAt(Vector2.new(input.Position.X, input.Position.Y))
			elseif mode == "ready" or mode == "busy" then
				task.spawn(strike)
			end
		end
	end))
	table.insert(connections, UserInputService.InputChanged:Connect(function(input)
		if grinding and (input.UserInputType == Enum.UserInputType.MouseMovement or input.UserInputType == Enum.UserInputType.Touch) then
			grindAt(Vector2.new(input.Position.X, input.Position.Y))
		end
	end))
	table.insert(connections, UserInputService.InputEnded:Connect(function(input)
		if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
			grinding = false
			lastLocal = nil
		end
	end))
	table.insert(connections, RunService.RenderStepped:Connect(function()
		-- The default camera scripts reclaim the camera when the character spawns; hold it here.
		camera.CameraType = Enum.CameraType.Scriptable
		camera.CFrame = cameraCf
		-- Keep the player's own character out of the shot (local only).
		local character = player.Character
		if character then
			for _, d in character:GetDescendants() do
				if d:IsA("BasePart") or d:IsA("Decal") then
					d.LocalTransparencyModifier = 1
				end
			end
		end
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
	end))

	local function stop()
		for _, c in connections do
			c:Disconnect()
		end
		local character = player.Character
		if character then
			for _, d in character:GetDescendants() do
				if d:IsA("BasePart") or d:IsA("Decal") then
					d.LocalTransparencyModifier = 0
				end
			end
		end
		folder:Destroy()
		gui:Destroy()
		mesh:Destroy()
		camera.CameraType = previousCameraType
	end
	restart = function()
		stop()
		task.defer(BladeProbe.start, blueprintId)
	end

	-- Inspection handle for playtest checks (not gameplay).
	BladeProbe.current = {
		strike = function()
			task.spawn(strike)
		end,
		grindScreen = grindAt,
		setGrinding = function(on: boolean)
			grinding = on
			lastLocal = nil
		end,
		info = function()
			return {
				mode = mode,
				strikeIndex = state.strikeIndex,
				quality = BladeCore.quality(blade, state),
				display = BladeCore.displayQuality(blade, state),
				frameMs = frameMs,
				vertexCount = vertexCount,
			}
		end,
		part = part,
		params = function()
			return params
		end,
		blade = blade,
	}

	part.Color = HOT
	part.Material = Enum.Material.Neon
	placeHammer()
	local first = poseFor(BladeCore.strikeTarget(blade, params, 0))
	pose.point, pose.yaw, pose.flip, pose.thickness = first.point, first.yaw, first.flip, first.thickness
	applyPose()
	updateHud()
	return stop
end

return BladeProbe

--!strict
-- Etch patterns for the Etching Table (GDD §6.3 "Etching / Rune"). An etched sword shows the pattern on
-- its blade (Shared/BladeEtch) and, when SwordParts has a matching "<id>Guard", that guard; the bonus adds
-- to the sword's value like a hilt bonus. Free and applied instantly for now (Allen 2026-10-20); prices,
-- buying the table and the trace minigame come later.

export type Etch = { id: string, name: string, bonus: number, body: Color3, flame: Color3 }

local Etches = {}

-- The see-through body: the etch draws only its band or marks and the blade's own metal shows between them. First for
-- metals with their own texture (Allen 2026-10-23: "ideally the texture stays visible"), then for every metal (same
-- day: "lets do the see through etch on every metal like we do with dragonsteel and watermlon"). Shared/BladeEtch skips
-- the body faces and Shared/EtchCanvas leaves the body see-through. No real body is white. The patterns' own `body`
-- (dark steel) is what saves from before carry; SmithyCore draws every sword with CLEAR whatever it saved.
Etches.CLEAR = Color3.new(1, 1, 1)

Etches.list = {
	{ id = "Flame", name = "Flame", bonus = 0.15, body = Color3.fromRGB(6, 12, 20), flame = Color3.fromRGB(165, 14, 10) },
	-- 2026-10-21 (vault: Art/Animated Blade Etching): the first stroked pattern, drawn by Shared/EtchPatterns; same
	-- dark body and bonus as Flame, its marks in the material's colour
	{ id = "Eclipse", name = "Eclipse", bonus = 0.15, body = Color3.fromRGB(6, 12, 20), flame = Color3.fromRGB(196, 214, 236) },
	-- 2026-10-22: the concept sheet's other five, stroked like Eclipse, with its body, bonus and fallback colour
	{ id = "Tide", name = "Tide", bonus = 0.15, body = Color3.fromRGB(6, 12, 20), flame = Color3.fromRGB(196, 214, 236) },
	{ id = "Stormroot", name = "Stormroot", bonus = 0.15, body = Color3.fromRGB(6, 12, 20), flame = Color3.fromRGB(196, 214, 236) },
	{ id = "WovenWind", name = "Woven Wind", bonus = 0.15, body = Color3.fromRGB(6, 12, 20), flame = Color3.fromRGB(196, 214, 236) },
	{ id = "Fracture", name = "Fracture", bonus = 0.15, body = Color3.fromRGB(6, 12, 20), flame = Color3.fromRGB(196, 214, 236) },
	{ id = "FallingStars", name = "Falling Stars", bonus = 0.15, body = Color3.fromRGB(6, 12, 20), flame = Color3.fromRGB(196, 214, 236) },
} :: { Etch }

-- The band / mark colour comes from the sword's material (Allen 2026-10-20: "the color of the material should be part
-- of it"): a vivid version of each metal. On the bare metal of a see-through etch it reads because every band and mark
-- has a dark ink outline (Shared/BladeEtch, Shared/EtchCanvas; 2026-10-23, after a gold band vanished on a gold blade).
Etches.MATERIAL_FLAME = {
	Iron = Color3.fromRGB(196, 204, 216),
	Copper = Color3.fromRGB(222, 112, 48),
	Stone = Color3.fromRGB(178, 166, 140),
	Steel = Color3.fromRGB(214, 232, 250),
	Bronze = Color3.fromRGB(214, 138, 44),
	["Blue Steel"] = Color3.fromRGB(58, 128, 240),
	Silver = Color3.fromRGB(240, 242, 250),
	Gold = Color3.fromRGB(250, 196, 36),
	Obsidian = Color3.fromRGB(150, 70, 235),
	Damascus = Color3.fromRGB(204, 176, 128),
	Mythril = Color3.fromRGB(96, 226, 240),
	Starmetal = Color3.fromRGB(132, 112, 255),
	["Rainbow Alloy"] = Color3.fromRGB(255, 100, 200),
	Pewter = Color3.fromRGB(170, 184, 206),
	["Rose Gold"] = Color3.fromRGB(252, 168, 150),
	Jade = Color3.fromRGB(90, 232, 150),
	Dragonsteel = Color3.fromRGB(255, 196, 60), -- gold: red-orange vanished on its red scales
	Watermelon = Color3.fromRGB(110, 220, 80),
	["Black Iron"] = Color3.fromRGB(150, 156, 170),
	Brass = Color3.fromRGB(240, 200, 90),
	Amber = Color3.fromRGB(255, 170, 40),
	Marble = Color3.fromRGB(220, 214, 200),
	Amethyst = Color3.fromRGB(190, 120, 255),
	Ruby = Color3.fromRGB(255, 50, 80),
	["Frost Iron"] = Color3.fromRGB(150, 230, 255),
	Sapphire = Color3.fromRGB(70, 130, 255),
	["Magma Steel"] = Color3.fromRGB(255, 120, 30),
	Sunsteel = Color3.fromRGB(255, 230, 120),
	Cardboard = Color3.fromRGB(150, 100, 50),
	["Rubber Duck"] = Color3.fromRGB(255, 150, 30),
	Air = Color3.fromRGB(150, 220, 255), -- Refinements3 (2026-10-23)
} :: { [string]: Color3 }

-- The colours an etch takes on a sword of this material: body, flame.
function Etches.colorsFor(etch: Etch, materialId: any): (Color3, Color3)
	return Etches.CLEAR, Etches.MATERIAL_FLAME[materialId] or etch.flame
end

function Etches.get(id: any): Etch?
	for _, etch in Etches.list do
		if etch.id == id then
			return etch
		end
	end
	return nil
end

return Etches

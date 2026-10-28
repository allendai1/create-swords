# Sell Swords!

## Roblox skill routing

`roblox-collaboration-mode` is not enough on its own. Before changing code in Studio, also load the domain skill for that work:

| Work | Load |
| --- | --- |
| Writing or changing any ModuleScript or Script | `roblox-luau-patterns` (+ `roblox-luau-types` for type errors, `roblox-luau-core` for Luau syntax) |
| Save data, SmithyCore saves, session locks, adding a save field | `roblox-data` |
| Adding or changing a RemoteEvent/RemoteFunction | `roblox-networking` + `roblox-security` |
| Currency, shop, sales, rewards granted by the server | `roblox-security` |
| Etching, EditableImage, many parts, phone lag, client hitches | `roblox-performance` |
| Sparks, particles, tweens, polish/hit effects, NPC work animations | `roblox-animation-vfx` |
| Sounds, music, volume | `roblox-audio` |
| Lighting, atmosphere, workshop mood | `roblox-lighting` |
| Camera moves, station close-ups, cutscenes | `roblox-camera` |
| Touch, gamepad, keyboard bindings, action buttons | `roblox-input` |
| Where a new system lives, splitting scripts, require order | `roblox-architecture` |
| Leaderboards, cross-server events, MemoryStore | `roblox-server-data` |
| Before a test release or publish | `roblox-publish-checklist` |

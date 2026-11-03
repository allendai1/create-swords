"""Seconds the player's hands take, for the simulator. Not in balance.json because the game doesn't state them: each is
an ESTIMATE until a PlaytestLog measures it (vault: Development/Gameplay Simulator Plan §4.5). Numbers the game does state
(heat times, the ore box's show, the crew's times, customers' walk speed) come from balance.json, not from here.
Every report lists these values, so a result that leans on them can be read for what it is."""

import json
import os

ESTIMATE = {
    "pull_hold": 1.0,       # holding E on the lever before the box rolls
    "collect": 0.5,         # E on one ore slot to take its ingot
    "furnace_put": 1.0,     # the picker, an ingot into a furnace
    "furnace_take": 0.8,    # "Take out" a hot ingot
    "forge": 22.0,          # the anvil from opening to the finished blade, at FORGE_STRIKES strikes; 2026-10-23 note: "anvil visit ~25 s"
    "hilt_seat": 0.5,       # the seat taps after forging, part of the anvil now (Allen 2026-10-29: "basically 0.5 seconds")
    "polish": 12.0,         # the Polishing Station, a full polish
    "etch": 10.0,           # the Etching Table, picking a pattern and the etch show
    "place": 1.5,           # one sword onto a shop holder
    "rack": 0.6,            # one ingot or sword on or off a rack
    "buy": 2.0,             # standing on a pad and pressing Buy
    "menu": 3.0,            # a window purchase (crew, gem shop, cart levels)
    "cart_visit": 3.0,      # the cart's board, prompt to the cart leaving: Accept, Auto-Fill, Fill the Crate (Allen: "like 3 seconds")
    "letter": 3.0,          # handing a sword in from the mail (Allen 2026-10-29: "the GUI is probably open for like 3 seconds")
    "detour": 1.3,          # path length / straight line between stations (tables, doors, the shop step)
}
# Measured in playtests (calibrate.py writes timings.json from PlaytestLog): those medians replace the estimates.
_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "timings.json")
MEASURED, ROUTES, WALK_SPEED, OFFERS = {}, {}, None, None
# Strikes per blade behind T["forge"]; the engine scales it by each blueprint's strikes (balance.json). The estimate and
# every playtest before the 10-strike recipe (2026-10-30, Allen: "Yes do 10 hits") forged 12; calibrate.py stamps its own.
FORGE_STRIKES = 12
if os.path.exists(_path):
    with open(_path, encoding="utf-8") as _f:
        _j = json.load(_f)
    MEASURED = {k: v["median"] for k, v in _j["timings"].items() if k in ESTIMATE}
    FORGE_STRIKES = _j["timings"].get("forge", {}).get("strikes", FORGE_STRIKES)
    # seconds walking each route, at WALK_SPEED (the player's measured studs/s); the engine scales them to its own speed
    ROUTES = {k: v["median"] for k, v in _j.get("routes", {}).items()}
    WALK_SPEED = _j.get("walk_speed")
    OFFERS = _j.get("offers")  # your offer cards: median answer seconds, share missed, n (behavior.offer_habits)
T = dict(ESTIMATE, **MEASURED)


def route_key(a, b, upgraded):
    """One walk between two stations (engine.pos names), either way round; the Upgraded Store moves the workshop back."""
    return "-".join(sorted((a, b))) + (" upgraded" if upgraded else "")

# Code-stated, copied here only for the first-sword furnace (ForgeService FIRST_HEAT_TIME; not in balance.json yet)
FIRST_HEAT = 3.0

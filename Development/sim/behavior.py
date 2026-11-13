"""Modelled players for the simulator: what they choose and how fast they react. These are ASSUMPTIONS, not game rules
(those are in rules.py): each archetype is a stated policy plus noise, and a conclusion only counts if it survives
changing these numbers (vault: Development/Gameplay Simulator Plan §5-6)."""

import json
import math
import os
from dataclasses import dataclass, field, replace

import timings


@dataclass(frozen=True)
class Archetype:
    name: str
    buy: str            # "cheapest" | "income" | "crew" | "blueprints" | "grinder" | "manager"
    keep: int           # rarity index kept for your own swords (1 Uncommon+, 2 Rare+)
    rack_keep: int      # rarity index racked for the crew (0 = anything)
    polish: bool        # polishes its own swords once the station is bought
    etch: bool          # etches its own swords once the table is bought
    haggle: bool        # declines an offer under 1.1x value once, hoping for a raise (off for all: with customers the
                        # shop's limit, a walk-off costs more than a raise brings; an ESTIMATE to test)
    miss: float         # chance an offer card goes unanswered (busy, not looking)
    react: float        # mean seconds to answer an offer card
    idle_chance: float  # chance, at a decision, to idle a while
    idle_len: tuple     # seconds idled (min, max)
    waste_chance: float # chance a walk goes the wrong way first
    tend: bool          # keeps racks stocked, the shop full and the cart running before forging (the Manager)
    cart: str           # "overflow" (when the shop is full) | "active" (keeps it running) | "never"
    mail: float = 1.0  # share of mail orders it works on (keeps an ore for, forges, hands in); any order it hands in a
                       # sword that happens to fit (Allen 2026-10-29: casual players "will do a mail order 10% of the time")
    gems: str = "cheapest"  # gem shop: "mail" | "customers" (that pair first, then the rest) | "cheapest" next level
    sit_back: float = 0.0  # own forging given up once the crew runs the shop (engine.sitting_back; ESTIMATE, 2026-10-29)
    order: tuple = ()  # a recorded player's purchases in order (engine ids: pads, "hire:<id>", "MergeSlots", "Cap<n>")
    gem_order: tuple = ()  # and their gem buys in order (gem upgrade ids, one per level)
    slack: float = 1.0  # all-in seconds per action over the measured hand times (engine.run_task; allen.py fits it)
    learn: float = 1.0  # and on top of it while the tutorial runs: reading the lines, finding the controls
    forge: float = 100.0  # forge percent of your own swords (AnvilScore; live players average 97, ForgeGrade 2026-11-12)


ARCHETYPES = {
    # learn 1.2: a casual player finishes the tutorial about 20% after an efficient one (2026-11-09, Allen: "my number
    # [1:57] is probably close to what an efficient player should be, and casual is probably at most 25% more")
    "casual": Archetype("casual", "cheapest", keep=1, rack_keep=0, polish=True, etch=False, haggle=False, miss=0.05,
                        react=6.0, idle_chance=0.05, idle_len=(20, 90), waste_chance=0.10, tend=False, cart="overflow",
                        mail=0.1, sit_back=0.7, learn=1.2),
    "efficient": Archetype("efficient", "income", keep=2, rack_keep=1, polish=True, etch=True, haggle=False, miss=0.02,
                           react=2.0, idle_chance=0.02, idle_len=(5, 20), waste_chance=0.02, tend=False, cart="overflow",
                           gems="customers", sit_back=0.3),
    "automator": Archetype("automator", "crew", keep=2, rack_keep=0, polish=True, etch=False, haggle=False, miss=0.04,
                           react=5.0, idle_chance=0.04, idle_len=(20, 90), waste_chance=0.08, tend=False, cart="overflow", sit_back=0.8),
    "rusher": Archetype("rusher", "blueprints", keep=2, rack_keep=1, polish=True, etch=True, haggle=False, miss=0.03,
                        react=2.0, idle_chance=0.03, idle_len=(5, 20), waste_chance=0.02, tend=False, cart="overflow",
                        gems="customers", sit_back=0.3),
    "grinder": Archetype("grinder", "grinder", keep=2, rack_keep=1, polish=True, etch=True, haggle=False, miss=0.03,
                         react=3.0, idle_chance=0.0, idle_len=(0, 0), waste_chance=0.02, tend=False, cart="overflow",
                         gems="mail"),
    "manager": Archetype("manager", "manager", keep=2, rack_keep=1, polish=True, etch=True, haggle=False, miss=0.01,
                         react=1.5, idle_chance=0.0, idle_len=(0, 0), waste_chance=0.01, tend=True, cart="active",
                         gems="mail", sit_back=0.3),
}

# Paying players (Shared/Store): the passes each tier owns from the start; the Starter Pack is 100 gems and 5,000 coins (2026-11-11; 250 gems from 2026-11-08)
PAYERS = {
    "free": (),
    "starter": ("StarterPack",),
    "allpasses": ("StarterPack", "AutoRoller", "MoreCoins", "MoreGems", "LuckyOre", "VIP", "SwiftBoots"),
}

# The gem shop's pairs (Allen 2026-10-29: gem buys differ by type: Manager and Grinder mail first, Efficient and Rusher
# customers first, Casual (and the Automator, not stated) the cheapest next level). Better Advertising I comes first for
# everyone: the Guide's gem shop step.
GEM_GROUPS = {"customers": ("Advertising", "Vip"), "mail": ("Clients", "Mail")}
PLAY_DAY = int(__import__("os").environ.get("SIM_PLAY_DAY", 3600))  # run.py --play-day sets it for the workers; seconds played a day (Allen 2026-10-29: "1 h a day"); a daily reward each day, the cart and mail catch up between


def category(uid, B):
    """What a purchase is for (behaviour's grouping; the ids are the game's)."""
    u = B.upgrades.get(uid)
    if (u and u.get("blueprint")) or uid.startswith("design:"):  # a Musashi design is a sword like a blueprint pad
        return "blueprint"
    if u and u.get("etch"):  # the etch pads (2026-11-01): bought like the stations
        return "stations"
    if uid.startswith(("OreStand", "MergeSlots")):
        return "ore"
    if uid.startswith(("Heat", "F2Heat", "F3Heat", "Furnace")):
        return "heat"
    if uid.startswith(("Anvil", "Crafter", "Stocker", "Etcher")) or uid.startswith("hire:"):
        return "crew"
    if uid.startswith(("IngotRack", "SwordRack")):
        return "racks"
    if uid.startswith(("WallRack", "DisplayTable", "BigSwordStand", "UpgradedStore")):
        return "holders"
    if uid.startswith(("PolishStation", "EtchingTable")):
        return "stations"
    return "other"  # Parking, Delivery, Promoter, Cashier, cart levels, ...


def ancestors(B, ids):
    """Every upgrade some of `ids` needs first."""
    out, todo = set(), list(ids)
    while todo:
        for a in B.upgrades[todo.pop()]["after"]:
            if a not in out:
                out.add(a)
                todo.append(a)
    return out


STATION_UPS = ("Strikes", "PolishBoost")  # upgrades to a station's work, bought like the stations


def choose_target(arche, B, offers, value_of_bp, best_value, grinder_ok):
    """The purchase this player saves for, from offers [(id, price)], or None. value_of_bp(id) is a blueprint pad's
    sword base (0 for a big one); best_value the best non-big base it knows. Every type, whatever it saves for, buys a
    station or a station upgrade once it's within reach (not before a cheaper goal), and anything under a tenth of its goal (Allen 2026-10-30: "any
    sensible player would have bought the stations as they're available"; rushers bought no rack or furnace for 4 h and
    grinders no station for 15 h)."""
    if not offers:
        return None
    cheapest = min(offers, key=lambda o: o[1])
    stations = [o for o in offers if category(o[0], B) == "stations" or o[0].startswith(STATION_UPS)]
    station = min(stations, key=lambda o: o[1], default=None)
    goal = _goal(arche, B, offers, cheapest, value_of_bp, best_value, grinder_ok)
    if station is not None and station[1] <= 4 * cheapest[1] + 2000 and (goal is None or station[1] <= goal[1]):
        return station  # not before a cheaper goal (a 2,000 Polish Boost isn't worth more than a 1,300 Katana)
    return cheapest if goal is not None and cheapest[1] <= 0.1 * goal[1] else goal


def _goal(arche, B, offers, cheapest, value_of_bp, best_value, grinder_ok):
    by = lambda cats: [o for o in offers if category(o[0], B) in cats]
    raises = [o for o in by({"blueprint"}) if value_of_bp(o[0]) > best_value or value_of_bp(o[0]) == 0]
    if arche.buy == "cheapest":
        return cheapest
    if arche.buy == "blueprints":
        return min(by({"blueprint"}), key=lambda o: o[1], default=cheapest)
    near = lambda o: o is not None and o[1] <= 4 * cheapest[1] + 2000  # don't sit on a far goal while cheap buys wait
    if arche.buy == "crew":  # crew first, with the same guard as income (Allen 2026-10-29)
        pick = min(by({"crew", "racks"}), key=lambda o: o[1], default=None)
        return pick if near(pick) else cheapest
    if arche.buy == "grinder":
        # what makes more, and the holders and cart to sell it (2026-10-29: without them its swords piled up in thousands)
        ok = [o for o in offers if o[0] in grinder_ok or o[0] == "Delivery" or o[0].startswith(("Cap", "Spd"))
              or category(o[0], B) in {"blueprint", "crew", "ore", "heat", "racks", "holders"}]
        if all(category(o[0], B) == "ore" for o in ok):  # only ore slots and merges left of its kinds (they come back
            return cheapest                                  # after every merge): the rest, cheapest first
        return min(ok, key=lambda o: o[1])
    # income / manager: the best value per coin first: a sword that raises your best, then the crew, then the rest
    for group in (raises, by({"crew"}), by({"ore", "heat", "racks"}) + (by({"holders"}) if arche.buy == "manager" else [])):
        if group:
            pick = min(group, key=lambda o: o[1])
            if near(pick):
                return pick
    return cheapest


# Allen as the reference player (2026-11-09, Allen: "instead of different profiles, just use me as an average or above
# average player, and record how quickly im progressing"): allen.py fits allen.json to his recorded run, so "allen" buys
# what he bought in his order, with his gem buys and his pace (`slack`), and past his list as ALLEN_BASE would.
# "newplayer" is him NEW_PLAYER_SLACK times slower, answering offer cards as the casual type does (Claude's default:
# a new player doesn't know the game as its maker does).
ALLEN_BASE = "efficient"
NEW_PLAYER_SLACK = 1.25  # 2026-11-09, Allen: a casual player takes "at most 25% more" (1.4 before, Claude's guess)
ALLEN_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "allen.json")


def allen_profiles(j):
    """The "allen" and "newplayer" archetypes from an allen.json dict."""
    allen = replace(ARCHETYPES[ALLEN_BASE], name="allen", order=tuple(j["order"]), gem_order=tuple(j["gem_order"]),
                    slack=j["slack"])
    return {"allen": allen, "newplayer": replace(allen, name="newplayer", slack=j["slack"] * NEW_PLAYER_SLACK)}


if os.path.exists(ALLEN_PATH):
    with open(ALLEN_PATH, encoding="utf-8") as _f:
        ARCHETYPES.update(allen_profiles(json.load(_f)))

# "live": the casual type with live players' habits (2026-11-11, Allen: "Add it", from the ad-day analytics): pads in the
# order real players bought them (average minutes played, only pads `min_players` or more bought; after them the casual
# pick), offer cards missed at the live share and answered at the live average; since 2026-11-12 also the share of mail
# orders worked (filled / arrived), etching once the table is bought, and the average forge percent. live.json holds the numbers.
LIVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "live.json")


def live_profile(j):
    # "moved": a pad that took another's place in the game since the data was read stands at that pad's minutes
    times = {uid: tn for uid, tn in j["pads"].items() if uid not in j.get("moved", {}).values()}
    for uid, was in j.get("moved", {}).items():
        times[uid] = j["pads"][was]
    pads = sorted((t, uid) for uid, (t, n) in times.items() if n >= j["min_players"])
    offers = j["offers"]
    total = sum(n for n, _ in offers.values())
    base = ARCHETYPES["casual"]
    return replace(base, name="live", order=tuple(uid for _, uid in pads),
                   miss=round(offers["Missed"][0] / total, 3), react=offers["Accepted"][1], slack=j["slack"],
                   mail=j.get("mail", base.mail), etch=j.get("etch", base.etch), forge=j.get("forge", base.forge))


if os.path.exists(LIVE_PATH):
    with open(LIVE_PATH, encoding="utf-8") as _f:
        ARCHETYPES["live"] = live_profile(json.load(_f))


# Offer cards. Missed: each type's own `miss`, 1-5% (2026-11-09, Allen: "about 95-100% of players aren't missing it";
# the 38.6% measured 2026-10-29 came from feature tests with nobody watching the shop). Answer time: Allen's measured
# median once calibrate.py has a real run (timings.OFFERS), times these (only the second number is used now); else `react`.
OFFER_SCALE = {"casual": (1.25, 1.5), "manager": (0.5, 0.5), "newplayer": (1.25, 1.5)}


def offer_habits(arche, miss=None):
    """(chance an offer card goes unanswered, mean seconds to answer one) for this type; `miss` replaces the type's
    share missed (a scenario)."""
    m = timings.OFFERS
    share = arche.miss if miss is None else miss
    if not m:
        return share, arche.react
    return share, m["react"] / math.log(2) * OFFER_SCALE.get(arche.name, (1.0, 1.0))[1]  # exponential: mean = median / ln 2


def with_overrides(arche, **kw):
    return replace(arche, **kw)

"""Balance experiments: each scenario changes a copy of balance.json (and, for hand-action times, the timings), never
the game. Compare runs with the same seeds (run.py), so a difference comes from the change, not from luck."""

import copy

import rules
import timings


def _upgrade_prices(raw, f, ids=None):
    for u in raw["upgrades"]:
        if not u["decor"] and u["price"] > 0 and (ids is None or u["id"] in ids):
            u["price"] = max(1, round(u["price"] * f))


EAST = {"JianBlueprint", "DadaoBlueprint", "ZanbatoBlueprint"}
TUTORIAL = {"WakizashiBlueprint", "OreStand2"}  # the tutorial keeps its prices

SMALL = {"racks", "heat", "other", "stations", "holders"}  # behavior.category groups that are neither swords, crew nor ore


FICTIONAL = {f"{n}Blueprint" for n in ("HookSword", "CrescentFang", "ShardBlade", "Moonbite", "Serpent", "Leviathan",
                                        "Thornspire", "Seraph")}
WEST_UP = {"gladius": 360, "khopesh": 400, "rapier": 450}  # above the Dadao (340), the Rapier above the Hook Sword (430)


def _west_up(raw):
    for b in raw["blueprints"]:
        b["basePrice"] = WEST_UP.get(b["id"], b["basePrice"])


def _one_chain(raw):
    """Every non-big sword in one line by value (Allen 2026-10-30: "Would merging all the swords into one upgrade system
    help instead of them branching off"), today's blueprint prices handed out low to high along it. The Zanbato and
    Claymore wait on the sword now at their old gate's price (the Dadao's, the Rapier's) and the Big Sword Stand."""
    value = {b["id"]: b["basePrice"] for b in raw["blueprints"] if not b["big"]}
    pads = sorted((u for u in raw["upgrades"] if u.get("blueprint") in value), key=lambda u: value[u["blueprint"]])
    old = {u["id"]: u["price"] for u in pads}
    for i, (u, price) in enumerate(zip(pads, sorted(old.values()))):
        u["after"], u["price"] = ([pads[i - 1]["id"]] if i else []), price
    at = {u["price"]: u["id"] for u in pads}
    for u in raw["upgrades"]:
        if u["id"] in ("ZanbatoBlueprint", "ClaymoreBlueprint"):
            u["after"] = [at[old["DadaoBlueprint" if u["id"] == "ZanbatoBlueprint" else "RapierBlueprint"]], "BigSwordStand"]


def _milestone(raw, crafter, small, keep=frozenset()):
    _upgrade_prices(raw, 0.35, EAST)
    for u in raw["upgrades"]:
        if u["id"] in ("BigSwordStand", "ZanbatoBlueprint"):
            u["after"] = [a for a in u["after"] if a != "Cashier"]
        if u["id"] == "Crafter":
            u["price"] = crafter
    if small:
        import behavior
        B = rules.Balance(raw)
        _upgrade_prices(raw, 2.0, {u["id"] for u in raw["upgrades"] if behavior.category(u["id"], B) in SMALL} - TUTORIAL - keep)


SCENARIOS = {
    "baseline": lambda raw, t: None,
    "prices-10": lambda raw, t: _upgrade_prices(raw, 0.9),
    "prices+10": lambda raw, t: _upgrade_prices(raw, 1.1),
    "prices+20": lambda raw, t: _upgrade_prices(raw, 1.2),
    "prices+30": lambda raw, t: _upgrade_prices(raw, 1.3),
    "rare-odds+50": lambda raw, t: [r.__setitem__("odds", r["odds"] * 1.5) for r in raw["materials"]["rarities"][2:]],
    "forge-20": lambda raw, t: (t.__setitem__("forge", t.get("forge", timings.T["forge"]) * 0.8),
                                [c.__setitem__("forge", [x * 0.8 for x in c["forge"]]) for c in raw["employees"]["crafters"]]),
    "values+10": lambda raw, t: [b.__setitem__("basePrice", b["basePrice"] * 1.1) for b in raw["blueprints"]],
    # a pinned next goal players follow (2026-10-29; the Longsword path's 60% prices are in the game since): the Katana,
    # then the Longsword path
    "ls-pinned-k": lambda raw, t: raw.__setitem__("goalFirst", ["KatanaBlueprint", "MacheteBlueprint", "ScimitarBlueprint", "LongswordBlueprint"]),
    # players keep forging at full speed with the crew hired (sitting back off: the engine before 2026-10-29)
    "no-sit-back": lambda raw, t: t.__setitem__("sit_back_scale", 0.0),
    # a shop counter on screen, customers browsing and offers waiting (Allen 2026-10-29: "maybe with the visible customers
    # count, we can say that the percent goes down to 25%"): offer cards missed 25% instead of the measured share
    "offer-counter-25": lambda raw, t: t.__setitem__("offer_miss", 0.25),
    # the customers before 2026-10-30 (Farmer / Adventurer / Knight averaged about 1.0-1.15x, VIP 1.75-2.25x; likes and
    # their raise odds left out): what the two-type customers changed
    "old-offers": lambda raw, t: [c.update(offerMin=1.75, offerMax=2.25) if c["vip"] else c.update(offerMin=1.0, offerMax=1.15)
                                  for c in raw["customers"]["list"]],
    # the Zanbato at about 4 h (Allen 2026-10-30: "make the zanbato target of say 4 hours instead of 8"): the Eastern pad's
    # Jian, Dadao and Zanbato x k; "+10" also raises every other price 10%
    **{f"east{round(k * 100)}": (lambda k: lambda raw, t: _upgrade_prices(raw, k, EAST))(k) for k in (0.5, 0.35, 0.25)},
    **{f"east{round(k * 100)}+10": (lambda k: lambda raw, t: (_upgrade_prices(raw, k, EAST),
                                                               _upgrade_prices(raw, 1.1, {u["id"] for u in raw["upgrades"]} - EAST - TUTORIAL)))(k)
       for k in (0.35, 0.25)},
    # ... and the Big Sword Stand without the Cashier (it waited on her: efficient players buy her late)
    **{f"east{round(k * 100)}-nocash{tag}": (lambda k, f: lambda raw, t: (
        _upgrade_prices(raw, k, EAST), _upgrade_prices(raw, f, {u["id"] for u in raw["upgrades"]} - EAST - TUTORIAL),
        [u.__setitem__("after", [a for a in u["after"] if a != "Cashier"]) for u in raw["upgrades"] if u["id"] in ("BigSwordStand", "ZanbatoBlueprint")]))(k, f)
       for k in (0.5, 0.35) for tag, f in (("", 1.0), ("+10", 1.1))},
    # the first employee as a milestone (Allen 2026-10-30: "It should feel like a milestone to finally have your first
    # employee", "the upgrades should not be necessarily too easy to get either"), on the 4 h Zanbato (east35-nocash):
    # the Sword Crafter at 40k / 60k, and "small2" doubles the racks, heat, stations, holders and other small pads
    **{f"m-c{c // 1000}{tag}": (lambda c, small: lambda raw, t: _milestone(raw, c, small))(c, small)
       for c in (10000, 40000, 60000) for tag, small in (("", False), ("-small2", True))},
    # the package: a 40k crafter, small pads x2 but the Big Sword Stand (the Zanbato's gate) as it is
    "m-c40-small2-stand": lambda raw, t: _milestone(raw, 40000, True, {"BigSwordStand"}),
    # the trough after the Zanbato (pacing check 2026-10-30): fictional blueprints cheaper, and/or the Western swords worth
    # more than the Dadao so good players buy them between the fictional ones (they skip them: Gladius 280 < Dadao 340)
    **{f"late{round(k * 100)}{tag}": (lambda k, west: lambda raw, t: (_upgrade_prices(raw, k, FICTIONAL), west and _west_up(raw)))(k, west)
       for k in (0.5, 0.7, 1.0) for tag, west in (("", False), ("-west", True)) if (k, west) != (1.0, False)},
    "one-chain": lambda raw, t: _one_chain(raw),
    "one-chain-late70": lambda raw, t: (_one_chain(raw), _upgrade_prices(raw, 0.7, FICTIONAL)),
    # fewer pads on the floor (Refinements 2026-10-30, Allen: "there's too many upgrades on the floor at one time"): the
    # cheapest N pads show, plus the next sword and the Delivery Cart ("should always be available"). The game has cap 3
    # since that evening (balance.json padCap, from TycoonService); "no-cap" is every pad on offer, as before.
    # since 2026-10-31 a begun chain's next levels stand past the cap (balance.json chains), so capN caps new chains only
    **{f"cap{n}": (lambda n: lambda raw, t: raw.update(padCap=n))(n) for n in (1, 2, 3, 4, 5)},
    "no-cap": lambda raw, t: raw.update(padCap=0),
}


def build(name, base_raw):
    """(Balance, timing overrides) for a scenario."""
    raw, timing = copy.deepcopy(base_raw), {}
    SCENARIOS[name](raw, timing)
    return rules.Balance(raw), timing


def _overhaul(raw, t):
    """(Built 2026-11-02 in a different form: Anvil 2, Furnace 3 and Haru kept their gates. Run it on an older export only.)
    Upgrade overhaul proposal 2026-11-02: an upgrade waits only for the one before it in its line, or for what it
    is used with; swords gate only swords; price does the pacing."""
    gates = {
        "IngotRack": [], "Strikes1": [], "Parking1": [], "PolishStation2": ["PolishStation"],
        "Anvil2": ["IngotRack", "SwordRack"], "Furnace3": ["Crafter"], "Anvil3": ["Crafter"],
        "Cashier": ["UpgradedStore", "Crafter"], "Promoter": ["Crafter"], "EtchingTable2": ["EtchingTable"],
    }
    for u in raw["upgrades"]:
        if u["id"] in gates:
            u["after"] = gates[u["id"]]
        if u["id"] == "UpgradedStore":
            u["after"], u["price"] = ["WallRack5"], 15000
    for c in raw["employees"]["crafters"]:
        c.pop("needs", None)
        c["after"] = {"haru": "Anvil3", "mei": "Anvil4"}.get(c["id"], c.get("after"))
    raw["deliveries"]["capacityAfter"] = ["Delivery"] * 2
    raw["deliveries"]["speedAfter"] = ["Delivery"] * 3
    ch = raw["chains"]
    ch["Crafters"] = ["Anvil2", "Crafter", "Anvil3", "Anvil4"]
    ch["F3Heat"] = ["Furnace3", "F3Heat1", "F3Heat2", "F3Heat3"]


SCENARIOS["overhaul"] = _overhaul


def _crafter_price(raw, price):
    for u in raw["upgrades"]:
        if u["id"] == "Crafter":
            u["price"] = price


# an earlier first crafter (2026-11-02, Allen picked "Earlier first crafter"; target 1 h 30 since 2026-10-29): Taise's
# 40,000 sits ~4x above the pads round him, so cheapest-first players buy ~50 pads before him
for _p in (10000, 15000, 20000, 25000):
    SCENARIOS[f"crafter{_p // 1000}k"] = (lambda p: lambda raw, t: _crafter_price(raw, p))(_p)
    SCENARIOS[f"overhaul-crafter{_p // 1000}k"] = (lambda p: lambda raw, t: (_overhaul(raw, t), _crafter_price(raw, p)))(_p)
    # the same with players forging on after hiring (sitting back is an estimate): what the crafter alone is worth
    SCENARIOS[f"crafter{_p // 1000}k-no-sit-back"] = (
        lambda p: lambda raw, t: (_crafter_price(raw, p), t.__setitem__("sit_back_scale", 0.0)))(_p)


def _stocker_price(raw, price):
    for u in raw["upgrades"]:
        if u["id"] == "Stocker":
            u["price"] = price


# Taise's swords wait hours on a full rack before the Stocker (36,000) comes: a cheap Stocker right behind him
SCENARIOS["crafter15k-stocker12k"] = lambda raw, t: (_crafter_price(raw, 15000), _stocker_price(raw, 12000))
SCENARIOS["crafter15k-stocker12k-no-sit-back"] = lambda raw, t: (
    _crafter_price(raw, 15000), _stocker_price(raw, 12000), t.__setitem__("sit_back_scale", 0.0))


def _set_prices(raw, prices):
    """Coin prices by sim buy id: an upgrade id, hire:<crafter>, CapN / SpdN (Deliveries window levels)."""
    for u in raw["upgrades"]:
        u["price"] = prices.get(u["id"], u["price"])
    for c in raw["employees"]["crafters"]:
        c["coins"] = prices.get("hire:" + c["id"], c.get("coins"))
    D = raw["deliveries"]
    for key, lst in (("Cap", D["capacityPrice"]), ("Spd", D["speedPrice"])):
        for i in range(len(lst)):
            lst[i] = prices.get(f"{key}{i + 1}", lst[i])


def _timed(raw, t):
    """Prices from the time model (time_model.py writes time_prices.json) on the game's gates."""
    import json, os
    _set_prices(raw, json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "time_prices.json"))))


SCENARIOS["timed"] = _timed


def _hire_first(raw, price, gate):
    """Create Pottery's order (Pottery Playthrough 2026-11-02: the Apprentice before the second station): the Sword
    Crafter brings his own anvil (no Anvil 2 pad; the engine counts Anvil2 as his once he's hired), waits only for
    `gate`, and stands as soon as it opens."""
    raw["upgrades"] = [u for u in raw["upgrades"] if u["id"] != "Anvil2"]
    _crafter_price(raw, price)
    for u in raw["upgrades"]:
        if u["id"] == "Crafter":
            u["after"] = list(gate)
    raw["chains"]["Crafters"] = [c for c in raw["chains"]["Crafters"] if c != "Anvil2"]
    raw["padAlways"] = [p for p in raw.get("padAlways", ()) if p != "Anvil2"] + ["Crafter"]


# the first Sword Crafter at about 15 min of casual play (Allen 2026-11-02, from Create Pottery's Apprentice: 55% of
# 15-min income, one cheap step in front). "c2k" keeps today's gate (Anvil 2 after Furnace 2 and the racks) to show
# what the price alone does; "first" folds Anvil 2 into the hire and gates him on his rack and ingots only
SCENARIOS["c2k"] = lambda raw, t: _crafter_price(raw, 2000)
for _p in (1500, 2000, 3000):
    SCENARIOS[f"first{_p / 1000:g}k"] = (lambda p: lambda raw, t: _hire_first(raw, p, ("IngotRack", "SwordRack")))(_p)
    # ... with players who head for him once he stands, as Allen did for Pottery's Apprentice (walked past six cheaper
    # pads); the sim's types otherwise buy the cheaper pads round him first
    SCENARIOS[f"first{_p / 1000:g}k-goal"] = (lambda p: lambda raw, t: (_hire_first(raw, p, ("IngotRack", "SwordRack")),
                                                                         raw.__setitem__("goalFirst", ["Crafter"])))(_p)
# players forging on after the hire (sitting back is an estimate): how much of the coin drop it is
SCENARIOS["first2k-no-sit-back"] = lambda raw, t: (_hire_first(raw, 2000, ("IngotRack", "SwordRack")), t.__setitem__("sit_back_scale", 0.0))

# What draws casual players to the 2,000 Sword Crafter (built 2026-11-02), on the live export: "crafter-goal" players head
# for his pad once it stands (a letter or guide step that works); "crafter-hold" no new chain's pad opens while his
# stands unbought (begun chains and the next sword still do)
SCENARIOS["crafter-goal"] = lambda raw, t: raw.__setitem__("goalFirst", ["Crafter"])
SCENARIOS["crafter-hold"] = lambda raw, t: raw.__setitem__("holdFor", "Crafter")

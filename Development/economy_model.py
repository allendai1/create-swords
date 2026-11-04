"""Sell Swords! pacing model (vault: Design/Upgrade Order Review — 2026-10-28; before it Design/Economy Pass 2 and
Design/Progression and Economy Review — 2026-10-27).
Game numbers come from sim/balance.json, Studio's export (ServerStorage.Builders.ExportBalance; vault: Development/
Gameplay Simulator Plan): re-export after a reprice and rerun: python economy_model.py (python economy_model.py fit
re-prices). Only the player's pace and habits below are this model's own guesses. Estimates, not measurements: seconds per sword come from the 2026-10-23 playtest note (anvil visit ~25 s,
walk to a customer ~5.6 s, "about 35-60 s" a personal sword). Mail orders and the cart's trips are left out.
Picking (Allen 2026-10-27: "Plan the economy pass around players picking rare ore"): a picker pulls until a Rare+ ore
shows, for its own swords and the crafters'. The upgrade order (Allen 2026-10-28): PADS is the tree as built, the
two-stages-open gate baked into its `after` lists; GATE opens the cart levels and the crew window's hires; a new sword
teaches the crew; buying Ore Slot 6 merges at once. fit() prices it for a casual picker who buys the cheapest thing on
offer, with walk-ins."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "sim"))
import rules  # noqa: E402  (sim/rules.py: the game's own rules, parity-tested against Studio)
import timings  # noqa: E402  (sim/timings.py: measured hand times)

GAME = rules.load()
_B = GAME.raw
BASE = {i: p["basePrice"] for i, p in GAME.blueprints.items()}
BIG = {i for i, p in GAME.blueprints.items() if p["big"]}  # only the Big Sword Stand takes one (not the cart), so crafters don't make them
ZANBATO_EVERY = 3  # with the stand holding one, about every third sword you make is its big one (to time)
HILTS = [(h["unlockAt"], h["bonus"]) for h in GAME.hilts]
SEAT = _B["hilts"]["seatTaps"] * _B["hilts"]["seatBonus"]  # crafters and the anvil seat all three taps
POLISH = 1 + _B["grade"]["polishBonus"]
RAR = [(r["multiplier"], r["odds"]) for r in GAME.rarities]
HEAT = _B["heatTimes"]  # Faster Heating 0-3
CRAFTER_AT = _B["employees"]["levelAt"]
# quality at Lv. 1 (+QUALITY_STEP a level), forge seconds at Lv. 1 and the top (Shared/Employees); each hire starts at Lv. 1
ROSTER = {c["id"].capitalize(): (c["quality"], c["forge"][0], c["forge"][1]) for c in _B["employees"]["crafters"]}
PULL = 5.0  # seconds a lever pull, the hold included (to time)
RARE = 2  # a picker keeps Rare and better (index into RAR)
MERGE_LUCK, MERGE_PRICE = _B["merge"]["luck"], _B["merge"]["price"]


def odds(luck=1.0):
    return GAME.odds(luck)


def avg_metal(luck=1.0):
    return sum(m * p for (m, _), p in zip(RAR, odds(luck))) / 100


def picked(slots, tier=RARE, luck=1.0):  # a picked ore's metal multiplier, and the seconds of pulling it takes
    w = odds(luck)
    p = sum(w[tier:]) / 100
    return sum(RAR[i][0] * w[i] for i in range(tier, 6)) / 100 / p, PULL / (slots * p)


def hilt(made):
    return max(b for at, b in HILTS if made >= at)


def grade(q):  # x1.0 at 80% -> x2.0 at 100% (AnvilScore.forPercent)
    return GAME.grade(q)[1]


_VIP = GAME.customers["VIP"]
VIP, VIP_SHARE = _B["gemUpgrades"]["levels"][0]["vipChance"], (_VIP["offerMin"] + _VIP["offerMax"]) / 2  # after the tutorial


def share(bp, q=100):  # expected first offer / value: the walk-ins' mean share by weight, x the preference bonus when liked
    pref = _B["customers"]["preferenceBonus"]
    walk = sum(c["weight"] * (c["offerMin"] + c["offerMax"]) / 2 * (pref if GAME.likes(c["id"], bp, q) else 1) for c in GAME.walk_ins)
    return walk / sum(c["weight"] for c in GAME.walk_ins) * (1 - VIP) + VIP * VIP_SHARE


# Shared.Upgrades as exported (model ids: the blueprint pads drop "Blueprint"); id, price, after. Merge Ore Slots is
# free and comes with Ore Slot 6 here; decorations are cosmetic and left out.
def _mid(i):
    return i[:-9] if i.endswith("Blueprint") else i


PADS = [(_mid(u["id"]), u["price"], [_mid(a) for a in u["after"]]) for u in _B["upgrades"] if not u["decor"] and not u["merge"]]
_D = _B["deliveries"]
WINDOW = [(f"Cap{k + 1}", p) for k, p in enumerate(_D["capacityPrice"])] + [(f"Spd{k + 1}", p) for k, p in enumerate(_D["speedPrice"])]
CREW = [(c["id"].capitalize(), c["coins"]) for c in _B["employees"]["crafters"] if c["id"] != _B["employees"]["first"]]  # gems aren't modelled
GATE = {f"Cap{k + 2}": _mid(a) for k, a in enumerate(_D["capacityAfter"])} | {f"Spd{k + 2}": _mid(a) for k, a in enumerate(_D["speedAfter"])}     | {c["id"].capitalize(): (c["after"].capitalize() if c["after"] in GAME.crafters else _mid(c["after"]))
       for c in _B["employees"]["crafters"] if c.get("after")}  # Shared/Deliveries and the crew's `after`
BLUEPRINT_PAD = {_mid(u["id"]): u["blueprint"] for u in _B["upgrades"] if u.get("blueprint")}
GUIDE = ("Wakizashi", "OreStand2")  # the tutorial's buys (the Mailbox is on every plot since 2026-10-28)
FIXED = {"Wakizashi", "OreStand2"}  # the tutorial keeps its prices (Allen 2026-10-27: "Keep them")
STAGES = [  # goal, the minute a casual picker should buy it, the rest of its stage (fit() nudges a stage's prices together)
    ("Katana", 20, ["WallRack2", "PolishStation", "SwordRack", "DisplayTable1", "IngotRack", "Heat1", "OreStand3"]),
    ("Crafter", 60, ["EtchingTable", "Heat2", "OreStand4", "IngotRack2", "Heat3", "Furnace2", "Anvil2"]),
    ("Longsword", 105, ["SwordRack2", "Parking1", "Delivery", "Cap1", "Spd1"]),
    ("Haru", 150, ["UpgradedStore", "WallRack3", "DisplayTable2", "Anvil3", "Furnace3"]),
    ("Stocker", 190, ["Parking2", "Cap2"]),
    ("Falchion", 235, ["WallRack4", "DisplayTable3", "Spd2"]),
    ("Mei", 285, ["Anvil4"]),
    ("Promoter", 330, ["DisplayTable4", "Cap3", "Parking3"]),
    ("Gladius", 380, ["Spd3"]),
    ("Cashier", 425, ["Spd4"]),
    ("Etcher", 440, ["EtchingTable2"]),
    ("Zanbato", 480, ["BigSwordStand"]),  # today's last floor pad at 8 h (Allen 2026-10-27; the Katana stays at 20 min)
    ("Kenji", 560, []), ("Rin", 660, []),
]
FIRST_MERGE = 120  # minutes (Allen 2026-10-28: "first merge about 2 hours in")
SWORDS = ["Katana", "Longsword", "Falchion", "Gladius", "Zanbato"]  # each costs more than the last, as does each crafter
CREWS = ["Crafter", "Haru", "Mei", "Kenji", "Rin"]
CURRENT = {i: p for i, p, _ in PADS} | dict(WINDOW) | dict(CREW)

# Customers (customers=(scale, rep); vault: Design/Economy Pass 2#9. Customer rate). Walk-ins come every Better
# Advertising gap (seconds, levels 0-3, Shared/GemUpgrades) x scale, x (1 - 0.06 a reputation rank) when rep, x the Shop
# Promoter's perk; one takes the oldest sword waiting and pays its offer. Swords past SHELF go by cart at 0.8x value.
# Without customers every sword sells as it's made. The game since 2026-10-27 is customers=(1, False).
ADVERTISING = [tuple(l["walkIn"]) for l in _B["gemUpgrades"]["levels"][:4]]  # Shared/GemUpgrades levels 0-3 (4-5 not in the timeline)
ADVERTISED_AT = [0, 10, 180, 360]  # minutes of play by which a casual player has Advertising 0-3 (5 / 60 / 120 gems; a guess)
REP_AT = _B["reputation"]["thresholds"]  # Shared/Reputation points for ranks 1-8: one a sword sold or carted
SHELF = 20  # swords the shop's holders and the Finished Sword Rack hold, roughly


def run(focused=False, slow=1.0, hours=12.0, tier=RARE, prices=None, customers=(1, False), trace=None):
    """One player from the first second. Returns log (first minute each thing was bought), order (minute, id, price,
    coins a minute made before and after it, what was on offer next), merges (minutes) and earned (coins by second).
    trace gets (minute, swords made, sold, carted, waiting) each minute."""
    prices = prices or {}
    owned, t, coins, made, sales = set(), 0, 0.0, 0, 0
    known = ["tanto"]
    made_by, cprog, crafter_bp = {}, {}, None  # swords made and progress, by crafter; what the crafters make
    prog, merged = 0.0, 0
    log, order, merges, earned = {}, [], [], [0.0]
    stock, walk, sold, carted = [], 0.0, 0, 0  # swords waiting for a customer: (offer, value)
    letters = {"wak": False, "kat": False}
    T0 = 50 if focused else 75  # seconds a plain sword, roll to sale, heating not counted

    def ore():  # (metal multiplier, seconds of pulling) for one of your ingots
        slots = 1 + sum(f"OreStand{k}" in owned for k in range(2, 7))
        luck = 1 + MERGE_LUCK * merged
        return picked(slots, tier, luck) if tier is not None else (avg_metal(luck), 5.6 / slots)

    def player_T():
        T = T0 + ore()[1] - timings.T["forge"] * (1 - GAME.strike_pace(owned))  # Faster Strikes shortens your forging
        if not focused:
            T += HEAT[sum(f"Heat{k}" in owned for k in (1, 2, 3))]  # waits at the furnace
            T += 15 if "PolishStation" in owned else 0
        T += 10 if GAME.best_etch(owned) else 0  # a bought etch (2026-11-01)
        return T * slow

    def value(bp, q=100, polish=None, etch=None, metal=None):
        polish = ("PolishStation" in owned and not focused) if polish is None else polish
        etch = (GAME.best_etch(owned) is not None) if etch is None else etch
        metal = ore()[0] if metal is None else metal
        polish_mult = 1 + GAME.polish_bonus(owned)  # Polish Boost raises every polished sword's bonus
        return BASE[bp] * metal * grade(q) * (polish_mult if polish else 1) * (1 + hilt(made) + SEAT + (GAME.etch_bonus(owned) if etch else 0))

    def best():  # the best sword you make for the shelves (a big one needs the stand)
        return max((b for b in known if b not in BIG), key=lambda b: BASE[b])

    def crafter(c):  # seconds a sword, quality
        start, slow_forge, fast_forge = ROSTER[c]
        lvl = max(i + 1 for i, at in enumerate(CRAFTER_AT) if made_by.get(c, 0) >= at)
        forge = slow_forge + (fast_forge - slow_forge) * (lvl - 1) / 4
        return 45 + forge + HEAT[sum(f"Heat{k}" in owned for k in (1, 2, 3))], min(100, start + 8 * (lvl - 1))

    def working():  # the crafters at work: your best three, one per crafter anvil
        if "Crafter" not in owned or not crafter_bp:
            return []
        hired = ["Taise", *(c for c in ROSTER if c in owned)]
        n = sum(a in owned for a in ("Anvil2", "Anvil3", "Anvil4"))
        return sorted(hired, key=lambda c: -grade(crafter(c)[1]) / crafter(c)[0])[:n]

    def rate():  # coins a minute being made right now (yours + the working crafters')
        bp = best()
        v = value(bp) * share(bp)
        big = max((b for b in known if b in BIG), key=lambda b: BASE[b], default=None)  # the stand's best big sword
        if big:
            v = v * (1 - 1 / ZANBATO_EVERY) + value(big) * share(big) / ZANBATO_EVERY
        feed, crew = 0.0, 0.0
        for c in working():
            cT, q = crafter(c)
            crew += 60 / cT * value(crafter_bp, q=q, polish="PolishStation" in owned, etch="Etcher" in owned) * share(crafter_bp, q)
            feed += (1 / cT) * ore()[1] * slow if tier is not None else 0
        return 60 / player_T() * (1 - feed) * v + crew

    def price(i, p):
        p = prices.get(i, p)
        return int(p * MERGE_PRICE ** merged) if i.startswith("OreStand") else p

    def candidates():
        out = [(i, price(i, p)) for i, p, a in PADS if i not in owned and all(x in owned for x in a)]
        if "Delivery" in owned:
            out += [(i, prices.get(i, p)) for i, p in WINDOW if i not in owned and (i[-1] == "1" or f"{i[:-1]}{int(i[-1]) - 1}" in owned)]
        if "Crafter" in owned:
            out += [(i, prices.get(i, p)) for i, p in CREW if i not in owned]
        return [x for x in out if x[0] not in GATE or GATE[x[0]] in owned]

    def pick():
        c = candidates()
        if not c:
            return None
        for want in GUIDE:
            for x in c:
                if x[0] == want:
                    return x
        if focused:  # blueprints (the cheapest on offer), then the crafter chain, then cheapest
            bps = [x for x in c if x[0] in BLUEPRINT_PAD]
            if bps:
                return min(bps, key=lambda x: x[1])
            for want in ("IngotRack", "SwordRack", "Heat1", "Heat2", "Heat3", "Furnace2", "Anvil2", "Crafter", "Stocker"):
                for x in c:
                    if x[0] == want:
                        return x
        return min(c, key=lambda x: x[1])

    nxt = pick()
    while t < hours * 3600:
        t += 1
        before = coins
        prog += 1 / player_T()
        if prog >= 1:
            prog -= 1
            made += 1
            if not letters["wak"] and "wakizashi" in known:
                letters["wak"] = True
                coins += 120
            elif not letters["kat"] and "katana" in known and sales >= 3:
                letters["kat"] = True
                coins += 300
            else:
                big = max((b for b in known if b in BIG), key=lambda b: BASE[b], default=None)
                bp = big if big and sales % ZANBATO_EVERY == 0 else best()
                if sales == 0:
                    coins += value(bp, metal=1)  # the tutorial's customer comes at once
                elif customers:
                    stock.append((value(bp) * share(bp) * (1.06 if focused else 1), value(bp)))
                else:
                    coins += value(bp) * share(bp) * (1.06 if focused else 1)
                sales += 1
        for c in working():
            cT, q = crafter(c)
            cprog[c] = cprog.get(c, 0.0) + 1 / cT
            if cprog[c] >= 1:
                cprog[c] -= 1
                made_by[c] = made_by.get(c, 0) + 1
                v = value(crafter_bp, q=q, polish="PolishStation" in owned, etch="Etcher" in owned)
                if customers:
                    stock.append((v * share(crafter_bp, q), v))
                else:
                    coins += v * share(crafter_bp, q)
                if tier is not None:
                    prog -= ore()[1] * slow / player_T()  # the pulls for its ingot were yours
        if customers:
            scale, rep = customers
            lo, hi = ADVERTISING[sum(t / 60 >= m for m in ADVERTISED_AT) - 1]
            gap = (lo + hi) / 2 * scale * (1 - 0.06 * (sum(sold + carted >= p for p in REP_AT) - 1) if rep else 1)
            walk += 1 / (gap * (0.72 if "Promoter" in owned else 1))
            if walk >= 1:
                walk -= 1
                if stock:  # nobody comes in to an empty shop
                    coins += stock.pop(0)[0]
                    sold += 1
            while len(stock) > SHELF and "Delivery" in owned:
                coins += stock.pop(0)[1] * 0.8
                carted += 1
        if trace is not None and t % 60 == 0:
            trace.append((t // 60, made + sum(made_by.values()), sold, carted, len(stock)))
        earned.append(earned[-1] + coins - before)
        while nxt and coins >= nxt[1]:
            i, p = nxt
            r0 = rate()
            coins -= p
            owned.add(i)
            log.setdefault(i, t / 60)
            if i in BLUEPRINT_PAD:
                known.append(BLUEPRINT_PAD[i])
                if crafter_bp and BLUEPRINT_PAD[i] not in BIG:  # a new sword teaches the crew (Allen 2026-10-28)
                    crafter_bp = BLUEPRINT_PAD[i]
            if i == "Crafter":  # comes making your best sword ("Trained on hire")
                crafter_bp = best()
            if i == "OreStand6":  # merge: Ore Slots 2-6 go back to unbought, luck +0.5, their prices x1.5
                owned.difference_update({f"OreStand{k}" for k in range(2, 7)})
                merged += 1
                merges.append(t / 60)
            nxt = pick()
            order.append((t / 60, i, p, r0, rate(), candidates()))
    return log, order, merges, earned


def nice(x):  # two significant figures
    return int(float(f"{max(1, x):.2g}"))


def fit(rounds=40, prices=None, **profile):
    """Prices that put each stage's goal near its minute for this player buying the cheapest thing on offer: each round
    nudges a stage's prices together by how long it took against its plan, and Ore Slots 5-6 by the first merge against
    FIRST_MERGE; each sword and each crafter costs more than the last, and the Zanbato more than the Etcher. Keeps the
    round whose run was closest. Start from today's prices (or `prices`)."""
    prices = dict(prices or CURRENT)
    best = (1e9, prices)
    for _ in range(rounds):
        tried = dict(prices)
        log, _, merges, _ = run(prices=prices, hours=STAGES[-1][1] / 60 + 3, **profile)
        first = merges[0] if merges else 900
        prev_t, prev_a, worst = 0.0, 0.0, abs(first - FIRST_MERGE)
        for goal, at, rest in STAGES:
            a = log.get(goal, 900)
            f = min(1.35, max(0.75, ((at - prev_t) / max(5, a - prev_a)) ** 0.4))
            worst = max(worst, abs(a - at))
            for i in (goal, *rest):
                if i not in FIXED:
                    prices[i] = nice(prices[i] * f)
            prev_t, prev_a = at, a
        g = min(1.35, max(0.75, (FIRST_MERGE / first) ** 0.4))
        for i in ("OreStand5", "OreStand6"):
            prices[i] = nice(prices[i] * g)
        for chain in (SWORDS, CREWS):
            for a, b in zip(chain, chain[1:]):
                prices[b] = max(prices[b], nice(prices[a] * 1.15))
        prices["Zanbato"] = max(prices["Zanbato"], nice(prices["Etcher"] * 1.1))
        if worst < best[0]:
            best = (worst, tried)
    return best[1]


def fmt(m):
    return f"{int(m // 60)} h {int(m % 60):02d}" if m >= 60 else f"{m:.0f} min"


def walls(order, upto, most=2, at_least=10):  # stretches of at_least minutes with `most` or fewer things on offer
    return [(a[0], b[0], len(a[5])) for a, b in zip(order, order[1:]) if a[0] < upto and len(a[5]) <= most and b[0] - a[0] >= at_least]


if __name__ == "__main__":
    assert abs(sum(odds(1)) - 100) < 1e-9 and round(avg_metal(1), 3) == 1.569
    assert hilt(15) == 0.40 and hilt(14) == 0.25 and grade(70) == 1 and grade(100) == 2
    assert round(picked(1)[0], 2) == 3.94 and round(picked(1)[1]) == 33 and nice(1234) == 1200 and nice(37.4) == 37
    prices = None
    if "fit" in sys.argv[1:]:
        prices = fit()
        print("fitted prices (casual Rare+ picker, cheapest first):")
        for goal, _, rest in STAGES:
            print(f"   {goal} {prices[goal]:,} | " + ", ".join(f"{i} {prices[i]:,}" for i in rest))
    goals = [g for g, _, _ in STAGES]
    for name, kw in (("casual picker", {}), ("relaxed picker (casual x1.5)", dict(slow=1.5)),
                     ("focused picker (50 s a sword, blueprints first)", dict(focused=True)),
                     ("casual, never picks", dict(tier=None))):
        log, order, merges, _ = run(hours=16, prices=prices, **kw)
        z = log.get("Zanbato", 1e9)
        print(f"\n== {name}, cheapest first: Zanbato {fmt(z) if z < 1e9 else 'after 16 h'}")
        print("   " + ", ".join(f"{g} {fmt(log[g])}" for g in goals if g in log))
        print("   merges: " + ", ".join(fmt(m) for m in merges[:8]) + f" ({len(merges)} by 16 h)")
        w = walls(order, z)
        print("   two or fewer things on offer for 10+ min: " + ("; ".join(f"{fmt(a)}-{fmt(b)}" for a, b, _ in w) if w else "never"))
        if name == "casual picker":
            gaps = [b[0] - a[0] for a, b in zip(order, order[1:]) if a[0] < z]
            print(f"   {len(gaps) + 1} buys before the Zanbato, longest gap {max(gaps):.0f} min")
            print("   minutes to pay for itself: " + ", ".join(f"{i} {p / (r1 - r0):.0f}" for _, i, p, r0, r1, _ in order
                                                          if r1 - r0 > 1 and not i.startswith("OreStand")))

    # the second and third blueprint pads (2026-10-29), for a casual picker over 40 h
    log, *_ = run(hours=40)
    late = ["Machete", "Scimitar", "Cutlass", "Jian", "Khopesh", "Dadao", "Rapier", "HookSword", "Claymore", "Flamberge",
            "CrescentFang", "ShardBlade", "Moonbite", "Serpent", "Leviathan", "Thornspire", "Seraph"]
    print("\n== casual picker, 40 h: the second and third pads")
    print("   " + ", ".join(f"{g} {fmt(log[g]) if g in log else 'after 40 h'}" for g in late))

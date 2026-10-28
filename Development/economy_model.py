"""Sell Swords! pacing model (vault: Design/Progression and Economy Review — 2026-10-27, Design/Economy Pass 2).
Constants copied from the live Studio modules on 2026-10-27 (Shared.Upgrades, Blueprints, Hilts, Materials,
Customers, Employees, Deliveries); update them here after a reprice and rerun: python economy_model.py
Estimates, not measurements: seconds per sword come from the 2026-10-23 playtest note
(anvil visit ~25 s, walk to a customer ~5.6 s, "about 35-60 s" a personal sword). Orders, the cart and
customer shortages are left out.
Picking (Allen 2026-10-27: "Keep unlimited free spins. Plan the economy pass around players picking rare ore"): a picker
pulls until a Rare+ ore shows, for its own swords and the crafter's (tier RARE); fit() prices the planned buys (STAGES)
so a casual picker makes each at its minute."""

from functools import lru_cache

BASE = dict(tanto=20, wakizashi=45, katana=110, longsword=160, falchion=220, gladius=280, zanbato=1000)
BIG = {"zanbato"}  # big swords: only the Big Sword Stand takes one, so crafters aren't trained on them
ZANBATO_EVERY = 3  # with the stand holding one, about every third sword you make is its Zanbatō (to time)
HILTS = [(0, 0.0), (2, 0.05), (4, 0.10), (7, 0.15), (10, 0.25), (15, 0.40)]
SEAT, ETCH, POLISH = 0.06, 0.15, 1.10
RAR = [(1, 60), (1.5, 25), (2.5, 10), (5, 4), (12, 1), (25, 0.1)]
HEAT = [10, 6, 4, 3]  # Faster Heating 0-3 (Shop Tension Pass 2026-10-27; was 10, 8, 6, 4)
TRAIN = dict(tanto=200, wakizashi=600, katana=1500, longsword=2500, falchion=4000, gladius=6000)
CRAFTER_AT = [0, 10, 30, 70, 150]
# quality at Lv. 1 (+8 a level), forge seconds at Lv. 1 and Lv. 5 (Shared/Employees); each hire starts at Lv. 1
ROSTER = dict(Taise=(70, 30, 15), Haru=(72, 28, 14), Mei=(76, 26, 13), Kenji=(79, 24, 12), Rin=(85, 20, 10))
SLOTS_TOTAL = 75 + 300 + 900 + 2000 + 4000
PULL = 5.0  # seconds a lever pull, the hold included (to time)
RARE = 2  # a picker keeps Rare and better (index into RAR)


def odds(luck=1.0):
    w, left = [0] * 6, 90.0
    for i in range(5, 0, -1):
        w[i] = min(RAR[i][1] * luck, left - 10 * (i - 1))
        left -= w[i]
    w[0] = left + 10
    return w


def avg_metal(luck=1.0):
    return sum(m * p for (m, _), p in zip(RAR, odds(luck))) / 100


@lru_cache
def picked(slots, tier=RARE, luck=1.0):  # a picked ore's metal multiplier, and the seconds of pulling it takes
    w = odds(luck)
    p = sum(w[tier:]) / 100
    return sum(RAR[i][0] * w[i] for i in range(tier, 6)) / 100 / p, PULL / (slots * p)


def hilt(made):
    return max(b for at, b in HILTS if made >= at)


def grade(q):  # x1.0 at 80% -> x2.0 at 100%, clamped below 80
    return 1 + max(0, q - 80) / 20


VIP, VIP_SHARE = 0.05, 2.0  # Shared/Customers: 1 walk-in in 20 is a VIP offering x1.75-2.25 (Shop Tension Pass; after the tutorial)


def share(bp, q=100):  # expected first offer / value
    knight = 1.125 * (1.25 if q >= 95 else 1)
    adv = 1.075 * (1.25 if bp == "wakizashi" else 1)
    return (5 * 1.05 + 3 * adv + 2 * knight) / 10 * (1 - VIP) + VIP * VIP_SHARE


PADS = [  # id, price, after
    ("Mailbox", 15, []), ("Wakizashi", 60, []), ("OreStand2", 75, []),
    ("WallRack2", 150, []), ("IngotRack", 200, ["OreStand2"]), ("PolishStation", 250, []),
    ("SwordRack", 250, []), ("DisplayTable1", 250, ["WallRack2"]), ("OreStand3", 300, ["OreStand2"]),
    ("Heat1", 300, []), ("Katana", 400, ["Wakizashi"]), ("WallRack3", 400, ["UpgradedStore"]),
    ("Parking1", 500, ["DisplayTable1"]), ("IngotRack2", 500, ["IngotRack"]), ("Furnace2", 500, ["Heat3"]),
    ("SwordRack2", 600, ["SwordRack"]), ("DisplayTable2", 600, ["UpgradedStore"]), ("WallRack4", 700, ["WallRack3"]),
    ("EtchingTable", 800, ["PolishStation"]), ("OreStand4", 900, ["OreStand3"]), ("Heat2", 900, ["Heat1"]),
    ("DisplayTable3", 900, ["DisplayTable2"]), ("Longsword", 1000, ["Katana"]), ("Crafter", 1000, ["Anvil2"]),
    ("Delivery", 1200, ["OreStand2"]), ("DisplayTable4", 1300, ["DisplayTable3"]), ("Anvil2", 1500, ["IngotRack", "Furnace2", "SwordRack"]),
    ("UpgradedStore", 1500, ["DisplayTable1"]), ("Promoter", 1500, ["DisplayTable1"]), ("Parking2", 1500, ["Parking1"]),
    ("OreStand5", 2000, ["OreStand4"]), ("Falchion", 2000, ["Longsword"]), ("Stocker", 2000, ["Crafter"]),
    ("Etcher", 2000, ["EtchingTable2"]), ("Heat3", 2500, ["Heat2"]), ("EtchingTable2", 2500, ["EtchingTable", "SwordRack"]),
    ("BigSwordStand", 2500, ["UpgradedStore"]), ("Cashier", 3000, ["UpgradedStore"]), ("Gladius", 3500, ["Falchion"]),
    ("OreStand6", 4000, ["OreStand5"]), ("Parking3", 4000, ["Parking2"]),
    # pass 2 (Allen 2026-10-27): "at most 3 active sword crafter at a time ... 3 anvils can exist", and "Sell the Zanbatō"
    ("Anvil3", 1500, ["Anvil2"]), ("Anvil4", 1500, ["Anvil3"]), ("Zanbato", 0, ["Gladius", "BigSwordStand"]),
]
PASS2_PADS = {"Anvil3", "Anvil4", "Zanbato"}
WINDOW = [("Cap1", 600), ("Cap2", 1500), ("Cap3", 3500), ("Spd1", 800), ("Spd2", 1600), ("Spd3", 3000), ("Spd4", 5000)]
CREW = [("Haru", 2500), ("Mei", 6000), ("Kenji", 12000), ("Rin", 25000)]
BLUEPRINT_PAD = dict(Wakizashi="wakizashi", Katana="katana", Longsword="longsword", Falchion="falchion", Gladius="gladius",
                     Zanbato="zanbato")
GUIDE = ("Mailbox", "Wakizashi", "OreStand2")
CURRENT = {i: p for i, p, _ in PADS} | dict(WINDOW) | dict(CREW) | {"Train_" + b: p for b, p in TRAIN.items()}

# Economy pass 2 (vault: Design/Economy Pass 2): the order a player buys things in, in stages. Each stage ends on a goal,
# the next sword or the next employee (Allen 2026-10-27: "it should take a meaningful amount of time to get the next
# sword and to also get an employee"), which a casual picker buys at its minute of play; the small buys before it share
# the rest of the stage. Hiring the Sword Crafter trains him on your best sword, so the training left to buy is the
# Falchion's and the Gladius's. After the Etcher: the Zanbatō, then the crew window's crafters, Haru at Anvil 3 and Mei at
# Anvil 4 working beside Taise; Kenji and Rin replace the weakest of the three.
STAGES = [  # goal, minute, the small buys before it
    ("Katana", 20, ["WallRack2", "PolishStation", "SwordRack", "DisplayTable1", "IngotRack", "Heat1", "OreStand3"]),
    ("Longsword", 80, ["EtchingTable", "OreStand4", "Heat2", "Parking1", "IngotRack2", "SwordRack2", "Delivery", "Cap1", "Spd1"]),
    ("Crafter", 125, ["Heat3", "Furnace2", "Anvil2"]),
    ("Falchion", 190, ["UpgradedStore", "Parking2", "Cap2", "Spd2"]),
    ("Stocker", 235, ["Train_falchion", "DisplayTable2", "WallRack3", "OreStand5"]),
    ("Promoter", 280, ["DisplayTable3", "EtchingTable2", "Cap3"]),
    ("Gladius", 345, ["WallRack4", "Spd3", "Parking3"]),
    ("Cashier", 415, ["Train_gladius", "DisplayTable4"]),
    ("Etcher", 480, ["OreStand6", "Spd4"]),  # today's last floor pad at 8 h (Allen 2026-10-27; the Katana stays at 20 min)
    ("Zanbato", 525, ["BigSwordStand"]),
    ("Haru", 590, ["Anvil3"]), ("Mei", 680, ["Anvil4"]), ("Rin", 790, ["Kenji"]),
]
GOAL_SHARE = 0.4  # the share of its stage you spend saving for the goal itself; the small buys split the rest by today's prices
PLAN = [*GUIDE, *[i for goal, _, small in STAGES for i in (*small, goal)]]
# Pass 2's rules (run(pass2=True)): a stage's pads, cart levels and goal appear only once the stage before ended on its
# goal; the Sword Crafter comes trained on your best sword; up to three crafters work (Anvils 2-4), your best three.
GATE = {i: STAGES[k - 1][0] for k in range(1, len(STAGES)) for i in (*STAGES[k][2], STAGES[k][0])}

# Customers (run(customers=(scale, rep)); vault: Design/Economy Pass 2#9. Customer rate). Walk-ins come every Better
# Advertising gap (seconds, levels 0-3, Shared/GemUpgrades) x scale, x (1 - 0.06 a reputation rank) when rep, x the Shop
# Promoter's perk (0.8 at Lv. 1 to 0.65 at Lv. 5); one takes the oldest sword waiting and pays its offer. Swords past
# SHELF go by cart at 0.8x value. Without customers every sword sells as it's made, as before. The game since
# 2026-10-27 is customers=(1, False): these gaps, reputation not speeding walk-ins (they were 12-22 / 10-18 / 8-15 /
# 6-12 s with reputation's 6% a rank; the tutorial keeps 12-22 s until Ore Slot 2, not modelled).
ADVERTISING = [(45, 75), (36, 64), (30, 52), (22, 42)]
ADVERTISED_AT = [0, 10, 180, 360]  # minutes of play by which a casual player has Advertising 0-3 (5 / 60 / 120 gems; a guess)
REP_AT = [0, 5, 15, 30, 50, 80, 120, 175]  # Shared/Reputation points for ranks 1-8: one a sword sold or carted
SHELF = 20  # swords the shop's holders and the Finished Sword Rack hold, roughly


def run(focused, slow=1.0, hours=12.0, tier=None, prices=None, plan=None, pass2=False, customers=None, trace=None):
    # plan: buy in this order; trace: a list that gets (minute, swords made, sold, carted, waiting) each minute
    prices = prices or {}
    owned, t, coins, made, sales = set(), 0, 0.0, 0, 0
    known = ["tanto"]
    made_by, cprog, crafter_bp, trained = {}, {}, None, set()  # swords made and progress, by crafter
    prog = 0.0
    log, order, earned = {}, [], [0.0]  # earned: coins made by each second
    stock, walk, sold, carted = [], 0.0, 0, 0  # swords waiting for a customer: (offer, value)
    letters = {"wak": False, "kat": False}
    T0 = 50 if focused else 75  # seconds a plain sword, roll to sale, heating not counted

    def ore():  # (metal multiplier, seconds of pulling) for one of your ingots
        slots = 1 + sum(f"OreStand{k}" in owned for k in range(2, 7))
        return picked(slots, tier) if tier is not None else (avg_metal(), 5.6 / slots)

    def player_T():
        T = T0 + ore()[1]
        if not focused:
            T += HEAT[sum(f"Heat{k}" in owned for k in (1, 2, 3))]  # waits at the furnace
            T += 15 if "PolishStation" in owned else 0
        T += 10 if "EtchingTable" in owned else 0
        return T * slow

    def value(bp, q=100, polish=None, etch=None, metal=None):
        polish = ("PolishStation" in owned and not focused) if polish is None else polish
        etch = ("EtchingTable" in owned) if etch is None else etch
        metal = ore()[0] if metal is None else metal
        return BASE[bp] * metal * grade(q) * (POLISH if polish else 1) * (1 + hilt(made) + SEAT + (ETCH if etch else 0))

    def best():  # the best sword you make for the shelves (a big one needs the stand)
        return max((b for b in known if b not in BIG), key=lambda b: BASE[b])

    def crafter(c):  # seconds a sword, quality
        start, slow_forge, fast_forge = ROSTER[c]
        lvl = max(i + 1 for i, at in enumerate(CRAFTER_AT) if made_by.get(c, 0) >= at)
        forge = slow_forge + (fast_forge - slow_forge) * (lvl - 1) / 4
        return 45 + forge + HEAT[sum(f"Heat{k}" in owned for k in (1, 2, 3))], min(100, start + 8 * (lvl - 1))

    def working():  # the crafters at work: your best, one per crafter anvil (pass 2: Anvils 2-4; before it, Taise)
        if "Crafter" not in owned or not crafter_bp:
            return []
        if not pass2:
            return ["Taise"]
        hired = ["Taise", *(c for c in ROSTER if c in owned)]
        n = sum(a in owned for a in ("Anvil2", "Anvil3", "Anvil4"))
        return sorted(hired, key=lambda c: -grade(crafter(c)[1]) / crafter(c)[0])[:n]

    def candidates():
        out = [(i, prices.get(i, p)) for i, p, a in PADS
               if i not in owned and all(x in owned for x in a) and (pass2 or i not in PASS2_PADS)]
        if "Delivery" in owned:
            out += [(i, prices.get(i, p)) for i, p in WINDOW if i not in owned and (i[-1] == "1" or f"{i[:-1]}{int(i[-1]) - 1}" in owned)]
        if "Crafter" in owned:
            out += [("Train_" + b, prices.get("Train_" + b, TRAIN[b])) for b in known if b not in trained and b not in BIG]
            out += [(i, prices.get(i, p)) for i, p in CREW if i not in owned]
        return [x for x in out if not pass2 or x[0] not in GATE or GATE[x[0]] in owned]

    def pick():
        c = candidates()
        if not c:
            return None
        if plan and any(i not in owned for i in plan):
            nxt = next(i for i in plan if i not in owned)
            return next(x for x in c if x[0] == nxt)  # a plan lists every item after the ones it needs
        for want in GUIDE:
            for x in c:
                if x[0] == want:
                    return x
        if focused:  # blueprints, then the crafter chain, then the best training, then cheapest
            for x in c:
                if x[0] in BLUEPRINT_PAD:
                    return x
            for want in ("IngotRack", "SwordRack", "Heat1", "Heat2", "Heat3", "Furnace2", "Anvil2", "Crafter", "Stocker"):
                for x in c:
                    if x[0] == want:
                        return x
            tr = [x for x in c if x[0].startswith("Train_")]
            if tr:
                return max(tr, key=lambda x: BASE[x[0][6:]])
        return min(c, key=lambda x: x[1])

    nxt = pick()
    while t < hours * 3600:
        t += 1
        before = coins
        prog += 1 / player_T()
        if prog >= 1:
            prog -= 1
            made += 1
            if not letters["wak"] and "wakizashi" in known and "Mailbox" in owned:
                letters["wak"] = True
                coins += 120
            elif not letters["kat"] and "katana" in known and sales >= 3:
                letters["kat"] = True
                coins += 300
            else:
                bp = "zanbato" if "zanbato" in known and sales % ZANBATO_EVERY == 0 else best()
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
            coins -= p
            owned.add(i)
            log[i] = t / 60
            bp = best()
            rate = 60 / player_T() * value(bp) * share(bp)  # coins a minute from your own swords right now
            order.append((t / 60, i, p, p / rate))
            if i in BLUEPRINT_PAD:
                known.append(BLUEPRINT_PAD[i])
            if i == "Crafter" and pass2:
                crafter_bp = best()
                trained.add(crafter_bp)
            if i.startswith("Train_") and (crafter_bp is None or BASE[i[6:]] > BASE[crafter_bp]):
                crafter_bp = i[6:]
            trained.add(i[6:]) if i.startswith("Train_") else None
            nxt = pick()

    run.stats = dict(sold=sold, carted=carted, waiting=len(stock))  # with customers: swords sold, carted, still waiting
    # coins a minute once everything is bought (player + crafter at Lv. 5); pass 2 measures its last ten minutes
    if pass2:
        return log, order, (earned[-1] - earned[-601]) / 10, earned
    bp = best()
    feed = ore()[1] * slow / (45 + 15 + 4) if tier is not None else 0
    end_rate = 60 / player_T() * (1 - feed) * value(bp) * share(bp) * (1.06 if focused else 1)
    end_rate += 60 / (45 + 15 + 4) * value(crafter_bp or bp, polish=True, etch=True) * share(crafter_bp or bp)
    return log, order, end_rate, earned


def nice(x):  # two significant figures
    return int(float(f"{x:.2g}"))


def fit(rounds=12, **profile):
    """Prices that put every planned buy at its minute for this player following PLAN: each costs the coins made since
    the buy before it (the tutorial's three keep theirs). Prices move the earnings, so a few rounds settle it. A small buy
    takes at most 3/4 of the goal's share of its stage, so the goal stays the dearest thing in it."""
    prices = {}
    for _ in range(rounds):
        log, _, _, earned = run(prices=prices, plan=PLAN, hours=STAGES[-1][1] / 60 + 1, pass2=True, **profile)

        def made(m):  # coins made by minute m, averaged over 4 minutes so one sale's lump doesn't set a price
            w = earned[max(0, round(m * 60) - 120):round(m * 60) + 120]
            return sum(w) / len(w)

        a = last = log["OreStand2"]
        for goal, b, small in STAGES:
            w = [min((1 - GOAL_SHARE) * CURRENT[i] / sum(CURRENT[j] for j in small), 0.75 * GOAL_SHARE) for i in small]
            times = [a + (b - a) * sum(w[:k + 1]) for k in range(len(small))] + [b]
            for i, at in zip((*small, goal), times):
                prices[i] = nice(made(at) - made(last))
                last = at
            a = b
    return prices


def fmt(m):
    return f"{int(m // 60)} h {int(m % 60):02d}" if m >= 60 else f"{m:.0f} min"


if __name__ == "__main__":
    assert abs(sum(odds(1)) - 100) < 1e-9 and round(avg_metal(1), 3) == 1.569
    assert hilt(15) == 0.40 and hilt(14) == 0.25 and grade(70) == 1 and grade(100) == 2
    assert round(picked(1)[0], 2) == 3.94 and round(picked(1)[1]) == 33 and nice(1234) == 1200 and nice(37.4) == 37
    print("avg metal by merges 0..8:", [round(avg_metal(1 + 0.5 * k), 2) for k in range(9)])
    profiles = [("focused (50 s/sword)", True, 1.0), ("casual (75 s + waits + finishing)", False, 1.0),
                ("relaxed (casual x1.5)", False, 1.5)]
    keys = ["OreStand2", "Katana", "Longsword", "UpgradedStore", "Falchion", "Gladius", "Crafter", "Stocker", "Cashier",
            "Parking3", "Spd4", "Rin"]
    for name, foc, slow in profiles:
        log, order, end_rate, _ = run(foc, slow)
        last = order[-1][0]
        pads = max(log[i] for i, _, _ in PADS if i not in PASS2_PADS)
        print(f"\n== {name}: every floor pad {fmt(pads)}, everything {fmt(last)}, then ~{end_rate:,.0f} coins/min")
        print("   " + ", ".join(f"{k} {fmt(log[k])}" for k in keys if k in log))
        for lo, hi in ((0, 15), (15, 60), (60, 1e9)):
            gaps = [b[0] - a[0] for a, b in zip(order, order[1:]) if lo <= a[0] < hi]
            if gaps:
                print(f"   purchases {lo}-{'end' if hi > 1e8 else hi} min: {len(gaps)}, median gap {sorted(gaps)[len(gaps) // 2] * 60:.0f} s")
        # the merge treadmill after that: cycle k re-buys Ore Slots 2-6 at x1.5^k
        rate, total, out = end_rate, 0.0, []
        for k in range(1, 13):
            cost = SLOTS_TOTAL * 1.5 ** k
            total += cost / rate
            rate = end_rate * avg_metal(1 + 0.5 * k) / avg_metal(1)
            out.append(f"{k}:{fmt(total)}")
        print("   merges after that (cumulative):", " ".join(out))
        mins = {i: m for _, i, _, m in order}
        print("   minutes of own income at purchase:", ", ".join(f"{k} {mins[k]:.1f}" for k in
              ("Katana", "Longsword", "Falchion", "Gladius", "UpgradedStore", "Anvil2", "Cashier", "OreStand6", "Parking3", "Spd4", "Rin") if k in mins))

    # cherry-picking: rolls are free and unlimited, so forge only rare ore (5 s a pull incl. the hold)
    w = odds(1)
    for slots in (1, 6):
        for name, tiers in (("Rare+", range(2, 6)), ("Epic+", range(3, 6))):
            p = sum(w[i] for i in tiers) / 100
            mult = sum(RAR[i][0] * w[i] for i in tiers) / 100 / p
            pull_s = PULL / (slots * p)
            gain = mult / avg_metal() * 55.6 / (55.6 + pull_s)
            print(f"cherry-pick {name} with {slots} slot(s): x{mult / avg_metal():.2f} value, +{pull_s:.0f} s a sword, income x{gain:.2f}, {1 / p - 1:.0f} junk ingots a sword")

    # the economy pass: prices for a casual Rare+ picker following the plan, then every player type on them
    prices = fit(focused=False, tier=RARE)
    print("\n== economy pass: stage goal (minute) price | small buys, was -> now")
    for goal, at, small in STAGES:
        was = lambda i: f"{CURRENT[i]:,}" if CURRENT[i] else "new"
        print(f"   {goal} ({fmt(at)}) {was(goal)}->{prices[goal]:,} | " + ", ".join(f"{i} {was(i)}->{prices[i]:,}" for i in small))
    goals = [g for g, _, _ in STAGES]
    for name, foc, slow, tier, plan, pass2 in (("casual picker, follows the plan", False, 1.0, RARE, PLAN, True),
                                               ("casual picker, cheapest first", False, 1.0, RARE, None, True),
                                               ("focused picker, blueprints first", True, 1.0, RARE, None, True),
                                               ("relaxed picker, cheapest first", False, 1.5, RARE, None, True),
                                               ("casual, never picks, cheapest first", False, 1.0, None, None, True)):
        log, order, end_rate, _ = run(foc, slow, 40, tier, prices, plan, pass2)
        pads = max(log.get(i, 1e9) for i, _, _ in PADS if i not in PASS2_PADS)
        print(f"\n== {name}: today's floor pads {fmt(pads)}, everything planned {fmt(max(log.get(i, 1e9) for i in PLAN))}, then ~{end_rate:,.0f} coins/min")
        print("   " + ", ".join(f"{k} {fmt(log[k])}" for k in goals if k in log))
        for lo, hi in ((0, 60), (60, 180), (180, 330), (330, 1e9)):
            gaps = [b[0] - a[0] for a, b in zip(order, order[1:]) if lo <= a[0] < hi]
            if gaps:
                print(f"   purchases {lo}-{'end' if hi > 1e8 else hi} min: {len(gaps)}, median gap {sorted(gaps)[len(gaps) // 2]:.1f} min")

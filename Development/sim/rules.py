"""Sell Swords! game mechanics for the simulator, mirrored from the Studio modules (vault: Development/Gameplay Simulator
Plan). Every number comes from balance.json (Studio's ServerStorage.Builders.ExportBalance); every function here has a
Luau original named in its docstring, and test_parity.py checks them against golden.json, the originals' own answers.
Change a rule here only when the Luau changes, then re-export and run the tests. Player behaviour does not live here."""

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load(path=None):
    with open(path or os.path.join(HERE, "balance.json"), encoding="utf-8") as f:
        return Balance(json.load(f))


def _round(x):
    """Luau math.floor(x + 0.5)."""
    return math.floor(x + 0.5)


class FakeRng:
    """The golden vectors' stand-in Random (ExportBalance `fake`): next_number returns seq in turn; next_integer(a, b)
    turns the next one into a + floor(u * (b - a + 1)), at most b. The simulator passes a real generator with the same
    two methods."""

    def __init__(self, seq):
        self.seq, self.i = list(seq), 0

    def next_number(self):
        self.i += 1
        return self.seq[(self.i - 1) % len(self.seq)]

    def next_integer(self, a, b):
        return min(b, a + math.floor(self.next_number() * (b - a + 1)))


class Balance:
    def __init__(self, b):
        self.raw = b
        self.upgrades = {u["id"]: u for u in b["upgrades"]}
        self.upgrade_order = [u["id"] for u in b["upgrades"]]
        # Upgrades.CHAINS (2026-10-31): once a chain has a level bought, its next levels stand whatever the pad cap
        self.chain_of = {i: name for name, ids in b.get("chains", {}).items() for i in ids}
        self.blueprints = {p["id"]: p for p in b["blueprints"]}
        self.blueprint_order = [p["id"] for p in b["blueprints"]]
        self.rarities = b["materials"]["rarities"]
        self.rarity_index = {r["id"]: i for i, r in enumerate(self.rarities)}
        self.metals = {m["id"]: m for m in b["materials"]["list"]}
        self.hilts = b["hilts"]["list"]
        self.etches = {e["id"]: e for e in b["etches"]}
        self.customers = {c["id"]: c for c in b["customers"]["list"]}
        self.customers.update({i: self.customers["VIP"] for i in b["customers"]["castVips"]})  # named VIPs deal as the VIP
        self.walk_ins = [c for c in b["customers"]["list"] if not c["vip"]]
        self.crafters = {c["id"]: c for c in b["employees"]["crafters"]}

    # --- Shared/Materials -----------------------------------------------------------------------------------------
    def odds(self, luck=1.0):
        """Materials.odds: each rarity's chance in percent at this luck."""
        mc = self.raw["materials"]["minCommon"]
        n = len(self.rarities)
        weights, left = [0.0] * n, 100 - mc
        for i in range(n - 1, 0, -1):  # Luau i = #rarities .. 2 (1-based)
            weights[i] = min(self.rarities[i]["odds"] * luck, left - mc * (i - 1))
            left -= weights[i]
        weights[0] = left + mc
        return weights

    def metal_multiplier(self, metal_id):
        """Materials.multiplier (1 for unknown ids)."""
        m = self.metals.get(metal_id)
        return self.rarities[self.rarity_index[m["rarity"]]]["multiplier"] if m else 1

    def climbs(self, metal_id):
        """Materials.climbs: tiers an ore climbs from Common in the roll's show."""
        return self.rarity_index[self.metals[metal_id]["rarity"]]

    def roll_length(self, metal_ids):
        """Materials.rollLength: seconds the ore box's cascade show takes for these results, in slot order."""
        c = self.raw["materials"]["cascade"]
        return max((c["lockAt"] + k * c["gap"] + self.climbs(m) * c["step"] + c["hold"] + c["drop"] for k, m in enumerate(metal_ids)), default=0)

    def roll(self, rng, luck=1.0):
        """Materials.roll: a rarity by its odds, then a metal of that rarity (draw order as the Luau)."""
        weights = self.odds(luck)
        rarity = self.rarities[0]["id"]
        x = rng.next_number() * 100
        for r, w in zip(self.rarities, weights):
            x -= w
            if x < 0:
                rarity = r["id"]
                break
        pool = [m for m in self.metals.values() if m["rarity"] == rarity]
        return pool[rng.next_integer(1, len(pool)) - 1]["id"]

    # --- Shared/AnvilScore, ValueFormula, SmithyCore ----------------------------------------------------------------
    def grade(self, percent):
        """AnvilScore.forPercent: (percent shown, price multiplier)."""
        g = self.raw["grade"]
        p = max(0, min(100, math.floor(percent + 1e-9)))
        f = max(0.0, min(1.0, (p - g["finishAt"]) / (100 - g["finishAt"])))
        return p, 1 + (g["maxMultiplier"] - 1) * f

    def hilt_bonus(self, hilt_id):
        return next(h["bonus"] for h in self.hilts if h["id"] == hilt_id)

    def sword_value(self, blueprint_id, metal_id, percent, polished=False, hilt_id="Wooden", seat_bonus=0.0, etch=None, polish_bonus=None):
        """SmithyCore.swordValue = ValueFormula.value(base, grade × polish, hilt + seat + etch, metal); polish_bonus: the owner's
        Polish Boost (polish_bonus(owned)), the base bonus when not given."""
        polish = 1 + (self.raw["grade"]["polishBonus"] if polish_bonus is None else polish_bonus) if polished else 1
        bonus = self.hilt_bonus(hilt_id) + (seat_bonus or 0) + (self.etches[etch]["bonus"] if etch else 0)
        base = self.blueprints[blueprint_id]["basePrice"]
        return _round(base * self.metal_multiplier(metal_id) * (self.grade(percent)[1] * polish) * (1 + bonus))

    # --- Shared/Hilts -------------------------------------------------------------------------------------------
    def best_hilt(self, made):
        """Hilts.best: the best tier unlocked by this many completed swords."""
        best = self.hilts[0]
        for h in self.hilts:
            if made >= h["unlockAt"] and h["bonus"] > best["bonus"]:
                best = h
        return best["id"]

    def seat_bonus(self, taps):
        """Hilts.seatBonus."""
        if not isinstance(taps, (int, float)) or taps != taps:
            return 0
        h = self.raw["hilts"]
        return max(0, min(h["seatTaps"], math.floor(taps))) * h["seatBonus"]

    # --- Shared/Customers -----------------------------------------------------------------------------------------
    def offer(self, customer_id, value, liked, rng):
        """Customers.offer: the first offer for a sword worth `value`."""
        c = self.customers[customer_id]
        share = c["offerMin"] + (c["offerMax"] - c["offerMin"]) * rng.next_number()
        return max(1, _round(value * share * (self.raw["customers"]["preferenceBonus"] if liked else 1)))

    def raise_offer(self, customer_id, offer, declines, rng, sure=False):
        """Customers.raise: a better offer after a decline, or None if they walk away; the chance halves after each raise
        (declines counts this one: 2026-10-30)."""
        c = self.customers[customer_id]
        chance = c["raiseChance"] * 0.5 ** max(0, declines - 1)
        if not sure and (declines > c["patience"] or rng.next_number() > chance):
            return None
        cu = self.raw["customers"]
        bump = cu["raiseMin"] + (cu["raiseMax"] - cu["raiseMin"]) * rng.next_number()
        return max(offer + 1, _round(offer * (1 + bump)))

    def pick_customer(self, rng, vip_chance=None):
        """Customers.pick: a VIP at vip_chance (None in the tutorial; half are named ones), else a walk-in by weight.
        ponytail: named clients (CAST_CHANCE, only while their sword is shown) aren't modelled."""
        if vip_chance is not None and rng.next_number() < vip_chance:
            cast = self.raw["customers"]["castVips"]  # named VIPs: the VIP's numbers, another face (2026-11-01)
            if cast and rng.next_number() < self.raw["customers"]["castVipShare"]:
                return cast[rng.next_integer(1, len(cast)) - 1]
            return "VIP"
        x = rng.next_number() * sum(c["weight"] for c in self.walk_ins)
        for c in self.walk_ins:
            x -= c["weight"]
            if x <= 0:
                return c["id"]
        return self.walk_ins[-1]["id"]

    def likes(self, customer_id, blueprint_id, percent):
        """Customers.likes."""
        c = self.customers[customer_id]
        return c.get("likesBlueprint") == blueprint_id or (c.get("likesQuality") is not None and (percent or 0) >= c["likesQuality"])

    # --- Shared/Orders ------------------------------------------------------------------------------------------
    def order_pay(self, value, metal_mult=None, typical=None, boost=None):
        """Orders.pay: PAY × value, its metal counted at no less than `typical`, × the shop's boost."""
        lift = max(1, typical / metal_mult) if metal_mult and typical and metal_mult > 0 else 1
        return _round(value * lift * self.raw["orders"]["pay"] * (boost or 1))

    def shop_boost(self, owned):
        """Orders.shopBoost: 1 + SHOP_STEP per shop upgrade owned (racks, tables, store, stand, bays, Promoter, Cashier)."""
        return 1 + self.raw["orders"]["shopStep"] * sum(1 for i in self.raw["orders"]["shop"] if i in owned)

    def typical_metal(self, luck):
        """Orders.typicalMetal: an average ore's multiplier at this luck."""
        return sum(r["multiplier"] * o / 100 for r, o in zip(self.rarities, self.odds(luck)))

    def _pick_blueprint(self, rng, known):
        """Orders' pickBlueprint: the three most valuable non-big known swords, 3:2:1."""
        top = sorted(((self.blueprints[i]["basePrice"], i) for i in known if i in self.blueprints and not self.blueprints[i]["big"]),
                     key=lambda t: (-t[0], t[1]))
        if not top:
            return known[rng.next_integer(1, len(known)) - 1]
        weights = [3, 2, 1][: len(top)]
        x = rng.next_number() * sum(weights)
        for w, (_, i) in zip(weights, top):
            x -= w
            if x <= 0:
                return i
        return top[0][1]

    def _pick_metal(self, rng, metal_ids):
        """Orders' pickMetal: each metal half as likely as one a rarity commoner."""
        weight = lambda i: 0.5 ** self.rarity_index[self.metals[i]["rarity"]] if i in self.metals else 0
        x = rng.next_number() * sum(weight(i) for i in metal_ids)
        for i in metal_ids:
            x -= weight(i)
            if i in self.metals and x <= 0:
                return i
        return None

    def make_order(self, rng, givers, blueprints, metals, polish, etch, level, kind=None):
        """Orders.make (without id and time): what an order asks for, drawing in the Luau's order."""
        o = {"blueprintId": self._pick_blueprint(rng, blueprints)}
        o["giver"] = givers[rng.next_integer(1, len(givers)) - 1]
        o["gems"] = 1
        if kind is None:
            o["materialId"] = self._pick_metal(rng, metals or []) or "Iron"
            if etch and rng.next_number() < self.raw["orders"]["etchChance"]:
                o["etched"] = True
            o["gems"] = 2 * (1 + (1 if self.rarity_index.get(self.metals.get(o["materialId"], {}).get("rarity"), -1) >= 2 else 0) + (1 if o.get("etched") else 0))
            return o
        roll = 0 if kind == "plain" else (0.35 + rng.next_number() * 0.65 if kind == "twist" else rng.next_number())
        if roll < 0.35:
            pass
        elif roll < 0.55:
            if polish:
                o["polished"] = True
        elif roll < 0.7:
            if etch:
                o["etched"] = True
        if roll >= 0.7 or (kind == "twist" and not (o.get("polished") or o.get("etched"))):
            o["rarity"] = "Rare" if level >= 4 and rng.next_number() < 0.35 else "Uncommon"
        twist = o.get("rarity") or o.get("polished") or o.get("etched")
        o["gems"] = 1 + (1 if twist else 0) + (1 if level >= 5 else 0)
        return o

    def order_fits(self, need, sword):
        """Orders.mismatch(need, sword) is nil. sword: blueprintId, materialId, polished, etch."""
        if sword["blueprintId"] != need["blueprintId"]:
            return False
        if need.get("materialId") and sword.get("materialId") != need["materialId"]:
            return False
        if need.get("rarity"):
            m = self.metals.get(sword.get("materialId"))
            if not m or self.rarity_index[m["rarity"]] < self.rarity_index[need["rarity"]]:
                return False
        if need.get("polished") and not sword.get("polished"):
            return False
        return not (need.get("etched") and not sword.get("etch"))

    def make_delivery(self, rng, givers, blueprints, polish, etch, level, capacity):
        """Deliveries.make (without id; recipient as an index): a cart offer, drawing in the Luau's order."""
        D = self.raw["deliveries"]
        kind = "bulk" if rng.next_number() < 0.5 else "special"
        need = self.make_order(rng, givers, blueprints, None, polish, etch, level, "plain" if kind == "bulk" else "twist")
        if kind == "bulk":
            count = rng.next_integer(max(2, capacity - 1), capacity)
        else:
            count = rng.next_integer(2, max(2, min(capacity - 1, D["specialMax"])))
        recipient = rng.next_integer(1, D["senders"])
        gems = 1 + count // 3 if kind == "bulk" else need["gems"]  # a Special pays its order's gems (2026-10-29)
        return {"kind": kind, "need": need, "count": count, "gems": gems, "recipient": recipient}

    def daily(self, streak, last, today):
        """GemUpgrades.daily: (streak day 1-7, gems), or (0, 0) when today's is claimed."""
        if last >= today:
            return 0, 0
        days = self.raw["gemUpgrades"]["daily"]
        day = streak % len(days) + 1
        return day, days[day - 1]

    # --- Shared/Upgrades ----------------------------------------------------------------------------------------
    def price(self, upgrade_id, merges=0):
        """Upgrades.price: Ore Slots cost MERGE_PRICE more per merge, compounding, to the nearest 10 (2026-11-02)."""
        p = self.upgrades[upgrade_id]["price"]
        if not upgrade_id.startswith("OreStand"):
            return p
        return 10 * math.floor(p * self.raw["merge"]["price"] ** merges / 10 + 0.5)  # Luau math.round: half away from 0

    def luck(self, merges, lucky_ore=False):
        """Upgrades.luck (+ Store.luckBonus with the Lucky Ore pass)."""
        return 1 + self.raw["merge"]["luck"] * merges + (self.raw["store"]["luckyOre"] if lucky_ore else 0)

    def heat_time(self, owned, forge="Forge"):
        """Upgrades.heatTime: a furnace's own Faster Heating chain (Heat1-3, F2Heat1-3, F3Heat1-3)."""
        prefix = f"F{forge[5:]}Heat" if forge[5:].isdigit() else "Heat"
        n = 0
        while f"{prefix}{n + 1}" in owned:
            n += 1
        return self.raw["heatTimes"][n]

    def strike_pace(self, owned):
        """Upgrades.strikePace: the anvil's strike cycle as a share, by Faster Strikes (Strikes1-5)."""
        n = 0
        while f"Strikes{n + 1}" in owned:
            n += 1
        return self.raw["strikePace"][n]

    def polish_bonus(self, owned):
        """SmithyCore.polishBonus: Polish Boost 0-3 (PolishBoost1-3) picks from polishBoost."""
        n = 0
        while f"PolishBoost{n + 1}" in owned:
            n += 1
        return self.raw.get("polishBoost", [self.raw["grade"]["polishBonus"]])[n]

    def best_etch(self, owned):
        """Shared/Etches.best (2026-11-01): the strongest pattern on offer whose Upgrades pad (`etch`) is bought, or None."""
        ids = {u["etch"] for i, u in self.upgrades.items() if u.get("etch") and i in owned}
        mine = [e for e in self.etches.values() if e["id"] in ids and not e.get("retired")]
        return max(mine, key=lambda e: e["bonus"])["id"] if mine else None

    def etch_bonus(self, owned):
        """The best owned pattern's bonus, 0 with none."""
        e = self.best_etch(owned)
        return self.etches[e]["bonus"] if e else 0.0

    def available(self, owned):
        """The pads on offer: not owned, every `after` owned (TycoonService). Decorations are bought in a window."""
        return [i for i in self.upgrade_order if i not in owned and all(a in owned for a in self.upgrades[i]["after"])]

    # --- Shared/Employees ---------------------------------------------------------------------------------------
    def staff_level(self, made, scale=None):
        """Employees.level: (level, made into it, made the level spans)."""
        at = lambda l: math.floor(self.raw["employees"]["levelAt"][l - 1] * (scale or 1))
        top = len(self.raw["employees"]["levelAt"])
        level = 1
        while level < top and made >= at(level + 1):
            level += 1
        return (level, 0, 0) if level >= top else (level, made - at(level), at(level + 1) - at(level))

    def crafter_quality(self, crafter_id, level):
        """Employees.quality."""
        return min(100, self.crafters[crafter_id]["quality"] + self.raw["employees"]["qualityStep"] * (level - 1))

    def level_seconds(self, level, rng_range):
        """Employees.seconds: lerp from Lv. 1 to the top level."""
        top = len(self.raw["employees"]["levelAt"])
        return rng_range[0] + (rng_range[1] - rng_range[0]) * (level - 1) / (top - 1)

    def crafter_walk(self, crafter_id, level):
        """Employees.crafterWalk: walk speed lerped by level (2026-11-03)."""
        return self.level_seconds(level, self.crafters[crafter_id]["walk"])

    def perk(self, role, count):
        """Employees.perk."""
        e = self.raw["employees"]
        return self.level_seconds(self.staff_level(count, e["staffScale"])[0], e["perks"][role])

    def staff_walk(self, role, count):
        """Employees.walk."""
        return self.perk(role, count) if role == "stocker" else self.raw["employees"]["staff"][role]["walk"]

    def cashier_percent(self, v):
        """Employees.cashierPercent."""
        r = self.raw["employees"]["cashier"]
        if isinstance(v, (int, float)) and not isinstance(v, bool) and r["min"] <= v <= r["max"] and (v - r["min"]) % r["step"] == 0:
            return v
        return self.raw["employees"]["staff"]["cashier"]["setting"]

    def cashier_sells(self, offer, value, setting):
        """Employees.cashierSells."""
        return offer * 100 >= value * (100 + self.cashier_percent(setting))

    # --- Shared/Reputation, Deliveries, Store -------------------------------------------------------------------
    def reputation_level(self, points):
        """Reputation.level: (level, points into it, points it spans)."""
        t = self.raw["reputation"]["thresholds"]
        level = max(i + 1 for i, need in enumerate(t) if points >= need)
        return (level, points - t[level - 1], t[level] - t[level - 1] if level < len(t) else 0)

    def cart_capacity(self, level):
        c = self.raw["deliveries"]["capacity"]
        return c[max(0, min(len(c) - 1, level))]

    def cart_trip(self, level):
        t = self.raw["deliveries"]["trip"]
        return t[max(0, min(len(t) - 1, level))]

    def cart_pay(self, values):
        """Deliveries.pay."""
        return _round(sum(values) * self.raw["deliveries"]["pay"])

    def cart_takes(self, blueprint_id):
        """Deliveries.mismatch for a Bulk Order: any sword but a big one."""
        return not self.blueprints[blueprint_id]["big"]

    def pack_for(self, currency, short):
        """Store.packFor: the smallest pack covering a shortfall, (key, amount) or (None, None); never a decoy (2026-11-02)."""
        s = self.raw["store"]
        packs = s["gemPacks"] if currency == "gems" else s["coinPacks"] if currency == "coins" else {}
        decoys = set(s.get("decoys", []))
        best = min(((n, k) for k, n in packs.items() if n >= short and k not in decoys), default=None)
        return (best[1], best[0]) if best else (None, None)

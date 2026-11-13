"""Discrete-event simulation of one Sell Swords! player (vault: Development/Gameplay Simulator Plan §3). Time jumps from
event to event. The game's rules come from rules.py (parity-tested), its numbers from balance.json; hand-action times
from timings.py (ESTIMATE); every choice the player makes from behavior.py. Rules this engine applies that aren't in
rules.py are the station flow read from the server scripts, each noted where it is used.

simulate(B, arche, payer, seed, hours) -> a dict of what happened (milestones, income, time use, waits ...).

Play comes in days of behavior.PLAY_DAY seconds: each brings the daily gem reward, and between them the cart comes back
and the mail fills up (both run on the server clock while you are away); nothing else runs offline.

Not modelled yet: declining mail orders, Robux currency packs, haggling beyond one decline, the workshop push when the
Upgraded Store is bought (racks move 12 studs; measured walking routes cover it), the Ore Roller's Iron lean while the
first letter is open, the crew forging for Special Orders."""

import heapq
import math
import random
import time

import behavior
import timings

T = timings.T
BIG_STAND = "BigSwordStand"
YOURS = 30  # EmployeeService.YOURS: seconds a furnace you just used stays yours, not a crafter's (2026-11-02)


def layout_pos(raw):
    """Plot-space (x, z) of every place the player walks to, by name."""
    L = raw["layout"]
    pos = {k: tuple(v["at"]) for k, v in L["stations"].items()}
    pos.update({k: tuple(v["at"]) for k, v in L["holders"].items()})
    pos.update({"pad:" + k: tuple(v) for k, v in L["pads"].items()})
    pos.update({k: tuple(v) for k, v in L["points"].items() if v})
    pos["shop"] = (0.0, -32.0)  # middle of the shop floor
    return pos


LOOK_WALK = 2.0  # s a customer walks between two holders on their look round (ShopService, 2026-11-05)
STROLL = 40  # studs up or down the street a walk-in starts: the middle of ShopService.STROLL 30-50 (2026-11-07)

# A recorded player buys the first of their next ORDER_LOOKAHEAD recorded buys that stands here; with none of them
# standing, their type's own choice (the sim's pads can open in another order than they did in the game).
ORDER_LOOKAHEAD = 3

def _drop(items, x):
    """Removes x itself, not an equal sword (two swords can be equal dicts; Orders.held keeps a particular one)."""
    del items[next(i for i, s in enumerate(items) if s is x)]


class Sim:
    def __init__(self, B, arche, payer, seed, hours, first_heat=timings.FIRST_HEAT, timing=None):
        self.B, self.A, self.raw = B, arche, B.raw
        self.T = dict(timings.T, **(timing or {}))
        self.horizon = hours * 3600
        self.first_heat = first_heat
        s = f"{seed}"
        self.rng = {k: random.Random(f"{s}:{k}") for k in ("ore", "cust", "weather", "act", "crew", "mail", "cart", "stand", "musashi")}
        self.passes = set(behavior.PAYERS[payer])
        self.speed = self.raw["store"]["swiftSpeed"] if "SwiftBoots" in self.passes else self.raw["player"]["walkSpeed"]
        self.boost = (self.raw["store"]["moreCoins"] if "MoreCoins" in self.passes else 1) * (self.raw["store"]["vipCoins"] if "VIP" in self.passes else 1)
        L = self.raw["layout"]
        self.pos = layout_pos(self.raw)
        self.holders_def = L["holders"]
        self.offer_miss, self.offer_react = behavior.offer_habits(arche, self.T.get("offer_miss"))
        self.grinder_ok = behavior.ancestors(B, [i for i, u in B.upgrades.items() if u.get("blueprint")])
        # --- state ---
        self.t = 0.0
        self.q, self.seq = [], 0
        self.coins, self.gems, self.till = 0.0, 0, 0.0
        self.earned = self.spent = 0.0
        # away earnings (SmithyCore.noteIncome / incomeRate / takeAway, 2026-11-11): coins earned with their time, the last
        # AWAY_WINDOW minutes kept; the rate the last day ended with; coins the Cashier brought in between days
        self.income_log, self.prev_rate, self.away_coins, self.away_sold = [], None, 0.0, 0
        self.owned, self.merges = set(), 0
        self.bought_n, self._pads, self._best = 0, (-1, []), {}
        self.wall_limit = None  # seconds of computer time before run() gives up on this player (run.py sets it)
        # until_done: stop once every pad (not decorations; the repeatable merge aside) has been bought at least once
        self.until_done, self.done = False, False
        self.all_pads = {i for i, u in B.upgrades.items() if not u["decor"] and i != "MergeSlots"}  # purchases so far; offers()' pad list and the count it was built at
        self.gem_levels = {g["id"]: 0 for g in self.raw["gemUpgrades"]["list"]}
        self.gems_in, self.gems_out = {}, {}  # gems by source / by what they bought
        self.day = self.streak = 0
        self.day_start = 0.0  # self.t when today's session began (income_rate)
        self.daily_held = False  # the first daily reward, waiting for the lessons' end (on_day)
        self.reputation = 0
        self.discovered = set()  # metals collected (Orders: a mail order's metal is one of them)
        self.orders, self.order_id, self.mail_due = [], 0, None  # open mail orders (rules.make_order dicts + id, have)
        self.mail_done, self.mail_coins = 0, 0.0
        self.quest_times = []  # minutes each letter or mail order was handed in (allen.py compares them with a run)
        self.cart, self.cart_offers, self.cart_retry = None, [], 0.0  # cart: None home, else {back, pay, gems, count, kind}
        self.cart_bulk = self.cart_special = self.cart_skips = 0
        self.cart_waiting = 0  # offer slots waiting after a skip
        self.cart_queue = None  # (offer, swords) packed while the cart is out, sent when it's collected
        self.known = {"tanto"}
        self.cap_lv = self.spd_lv = -1  # cart levels: -1 none (no cart), 0 = the cart's own level
        self.at = "Anvil"
        # your ingots as (metal, minute collected), so a sword knows when its loop began; the crew's as metals; swords in hand
        self.cold, self.cold_rack, self.hot, self.swords = [], [], [], []
        self.loops_own, self.loops_crew = [], []  # (ore to sold, of it: making, getting out, selling) seconds
        self.first_pull = None
        self.furnaces = {"Forge": None}  # name -> {who, metal, ready} or None
        self.used_at = {}  # furnace -> when you last put in or took out an ingot (ForgeService PlayerUsedAt)
        self.ingot_rack, self.sword_rack = [], []
        self.slots = []  # shop holder slots: {holder, big, sword, claimed}
        self._add_holder("WallRack1")
        self.stands = []  # ores waiting on the ore box (Auto Ore Roller)
        self.inshop = 0
        self.due = False  # a walk-in came due while the shop was full (ShopService, 2026-11-10)
        self.weather = None
        self.tutorial_done = False
        self.tutorial_pulls = 0  # ForgeService tutorialPulls: a new player's pulls (Common, then Uncommon)
        self.rolled_rare = False  # a Rare or better rolled yet (ends the old beginner's luck, a scenario since 2026-11-10)
        self.first_pull_given = False  # ForgeService firstPullGiven / d.rolled[FIRST_PULL_METAL]
        self.want_pulls = 0  # ForgeService wantPulls: pulls since the open letter's metal last came
        self.ramp = None  # (time, sales) when the tutorial ended: ShopService's walk-in ramp (2026-10-31)
        self.sold = self.own_made = self.crew_made = self.carted = self.letters = 0
        self.missed = self.lost = self.browsed = self.passed_on = 0
        self.letter = None  # ("IronTanto" | "Katana", since)
        self.letters_done, self.letters_offered = set(), set()
        self.hired = {}  # crafter id -> swords made
        self.equipped = {}  # anvil -> crafter id
        self.crafter_busy = {}  # anvil -> True while its loop runs
        self.staff = {}  # role -> jobs done
        self.target = None
        # a recorded player (behavior "allen", allen.py): their buys and gem buys still to come, in their order
        self.order_left, self.gem_order_left = list(arche.order), list(arche.gem_order)
        self.milestones, self.progress = {}, []
        self.minutes = []  # (earned, held, spent, own made, crew made)
        self.purchases = []
        self.use = {}
        self.crew_wait = {}
        self.luck_got = self.luck_exp = 0.0
        self.ores_seen = [0] * len(B.rarities)
        self.cust_id = 0
        # Musashi's stall (Shared/Musashi, 2026-11-10); off when the export (or a scenario) has no "musashi" or the
        # game has it switched off (musashi.enabled false: ships in a later update)
        self.mu_on = bool(self.raw.get("musashi")) and self.raw["musashi"].get("enabled", True) is not False
        self.mu_hour, self.mu_seen = 0, -1  # wall-clock hours begun / the one whose stock was rolled (first seen)
        self.mu_stock, self.mu_deals, self.mu_missed = [], {}, {}  # design ids, {pad: percent off}, Musashi floor counts
        self.mu_designs, self.mu_deal_buys, self.mu_saved, self.mu_gems_saved = [], 0, 0.0, 0

    # ---------------------------------------------------------------- plumbing
    def push(self, dt, kind, *data):
        self.seq += 1
        heapq.heappush(self.q, (self.t + dt, self.seq, kind, data))

    def dist(self, a, b):
        (x1, z1), (x2, z2) = self.pos[a], self.pos[b]
        return math.hypot(x1 - x2, z1 - z2) * self.T["detour"]

    def street_in(self):
        """Studs a walk-in walks from the street to the door: STROLL along the road, across to EntryPoint."""
        return math.hypot(STROLL, self.dist("CustomerSpawn", "EntryPoint"))

    def walk(self, to, speed=None):
        """Seconds for the player to walk to `to` (and now be there)."""
        if to == self.at:
            return 0.0
        # a route walked in playtests (calibrate.py): its measured seconds at this player's speed; else the layout's
        measured = None if speed else timings.ROUTES.get(timings.route_key(self.at, to, "UpgradedStore" in self.owned))
        spd = self.speed * (1 + self.stand_effects()["Swift"])  # Swift swords on the stands (Store.walkSpeed, 2026-11-09)
        d = measured * timings.WALK_SPEED / spd if measured else self.dist(self.at, to) / (speed or spd)
        # no wrong turns while the tutorial's line and arrows lead (2026-11-09, Allen: a casual player takes "at most 25%
        # more" than his 1:57 to finish it)
        if self.rng["act"].random() < self.A.waste_chance and self.tutorial_done:
            d += 8.0
        self.at = to
        return d

    def spend(self, cat, secs):
        self.use[cat] = self.use.get(cat, 0.0) + secs

    def mark(self, key):
        if key not in self.milestones:
            self.milestones[key] = self.t / 60

    def add_gems(self, n, source):
        if source in ("mail", "cart") and n > 0 and self.rng["stand"].random() < self.stand_effects()["Gems"]:
            n += 1  # Mail swords on the stands: one more (Showcase.bonusGem, 2026-11-09)
        if source in ("letters", "mail", "cart") and "MoreGems" in self.passes:
            n = int(n * self.raw["store"]["moreGems"] + 0.5)  # 50% More Gems, rounded half up (SmithyCore.earnGems, 2026-11-09)
        self.gems += n
        self.gems_in[source] = self.gems_in.get(source, 0) + n

    def rep_level(self):
        return self.B.reputation_level(self.reputation)[0]

    def view(self, s):
        """A sword as Orders.mismatch sees it."""
        return {"blueprintId": s["bp"], "materialId": s["metal"], "polished": s["polished"], "etch": s["etch"]}

    def coin_boost(self):
        """Store.coinBoost: the passes, then Coins swords on the stands (2026-11-09)."""
        return self.boost * (1 + self.stand_effects()["Coins"])

    def earn(self, coins):
        c = coins * self.coin_boost()
        self.coins += c
        self.earned += c
        self.note_income(c)

    def note_income(self, c):
        """SmithyCore.noteIncome: sales, the Cashier's till, carts, orders and letters count toward the away rate."""
        self.income_log.append((self.t, c))
        window = self.raw["employees"]["away"]["window"] * 60
        while self.income_log and self.income_log[0][0] <= self.t - window:
            self.income_log.pop(0)

    def income_rate(self):
        """SmithyCore.incomeRate: coins a minute over the last AWAY_WINDOW played minutes; while today is shorter, the last
        day's rate fills the rest (none: a short day spreads over AWAY_MIN)."""
        a = self.raw["employees"]["away"]
        window = a["window"]
        total = sum(c for t, c in self.income_log if t > self.t - window * 60)
        minutes = min((self.t - self.day_start) / 60, window)
        if self.prev_rate is not None:
            return (total + self.prev_rate * (window - minutes)) / window
        return total / max(minutes, a["min"])

    def settle_away(self):
        """Between days (ShopService on join, SmithyCore.takeAway): with the Cashier hired (the sim never switches him off),
        AWAY_SHARE of the rate the day ended with for each minute away, up to Aki's cap (the sim hires no other Cashier),
        plus the displayed swords customers bought meanwhile.
        A day is PLAY_DAY of play in 24 h, so the time away is always past the cap. Into his till, collected as his sales are."""
        if "cashier" not in self.staff:
            self.prev_rate = None  # SmithyCore.awayOut saves nothing without a Cashier at work
            return
        a = self.raw["employees"]["away"]
        rate = self.prev_rate = self.income_rate()
        secs = min(24 * 3600 - behavior.PLAY_DAY, a["cap"]["aki"])
        c = math.floor(rate * a["share"] * secs / 60)
        # away selling (ShopService on join, 2026-11-13): a customer every AWAY_PACE seconds buys a displayed sword at its
        # value with the boost, the most valuable first; those swords are gone. Counted as sales, not as income.
        # shortcut: the pace's mean, not the game's one random draw a stretch (keeps the customer stream as it was)
        n = int(secs // (sum(a["pace"]) / 2))
        full = sorted((s for s in self.slots if s["sword"] and not s["claimed"]), key=lambda s: -self.value(s["sword"]))[:n]
        if full:  # SmithyCore.boosted on the swords' total
            c += math.floor(sum(self.value(slot["sword"]) for slot in full) * self.coin_boost() + 0.5)  # Luau math.round
        for slot in full:
            slot["sword"] = None
        self.sold += len(full)
        self.away_sold += len(full)
        self.till += c
        self.earned += c
        self.away_coins += c

    # ---------------------------------------------------------------- the plot
    def _add_holder(self, name):
        h = self.holders_def[name]
        for _ in range(h["slots"]):
            self.slots.append({"holder": name, "big": h["big"], "sword": None, "claimed": False})

    def furnaces_owned(self):
        return [f for f in ("Forge", "Forge2", "Forge3") if f in self.furnaces]

    def heat_time(self, forge):
        if self.own_made == 0 or not self.tutorial_done:
            return self.first_heat  # ForgeService FIRST_HEAT_TIME until the tutorial's letter is sent (2026-10-31; was the first sword)
        return self.B.heat_time(self.owned, forge)

    def slots_n(self):
        return 1 + sum(f"OreStand{k}" in self.owned for k in range(2, 7))

    def luck(self):
        rain = 0
        if self.tutorial_done and self.weather and self.weather["effect"] == "WeatherLuck":
            rain = self.weather["value"]
        beginner = self.raw.get("beginnerLuck", 0) if self.tutorial_done and not self.rolled_rare else 0  # the 2026-11-01 rule (+9), now only a scenario
        return self.B.luck(self.merges, "LuckyOre" in self.passes) + rain + beginner + self.stand_effects()["Luck"]

    # --- the Showcase Stands (Shared/Showcase families, 2026-11-09) ---------------------------------------------------
    def stand_swords(self):
        """What the player puts on the Showcase Stands it owns: its best sword (polished and etched once it can) in its
        rarest collected metals, a different metal a stand, as the picker lists the strongest first.
        ponytail: never taken off sale, and every stand counts as filled."""
        n = sum(f"Showcase{k}" in self.owned for k in (1, 2, 3))
        if not n:
            return []
        S = self.raw["shop"]["showcase"]
        metals = sorted((m for m in self.discovered if m in S["family"]),
                        key=lambda m: (-S["tier"][self.B.metals[m]["rarity"]], m))[:n]
        bp, pol, etched = self.best_bp(), "PolishStation" in self.owned, self.B.best_etch(self.owned) is not None
        return [(m, bp, pol, etched) for m in metals]

    def stand_effects(self):
        """Showcase.totals over stand_swords: each family's points (pull x100) added up, x its rate, capped; Gems from Mail's."""
        key = (sum(f"Showcase{k}" in self.owned for k in (1, 2, 3)), len(self.discovered), self.best_bp(),
               "PolishStation" in self.owned, self.B.best_etch(self.owned) is not None)
        if getattr(self, "_stand_key", None) == key:
            return self._stand_eff
        S = self.raw["shop"]["showcase"]
        points = {}
        for m, bp, pol, etched in self.stand_swords():
            f = S["family"][m]
            points[f] = points.get(f, 0) + int(self.B.showcase_pull(m, bp, pol, etched) * 100 + 0.5)
        eff = {f: min(S["cap"][f], S["rate"][f] * points.get(f, 0)) for f in S["rate"]}
        eff["Gems"] = min(S["gems"]["cap"], S["gems"]["rate"] * points.get("Mail", 0))
        self._stand_key, self._stand_eff = key, eff
        return eff

    def ingot_cap(self):
        return 6 * sum(r in self.owned for r in ("IngotRack", "IngotRack2", "IngotRack3", "IngotRack4"))  # six a shelf (Racks 3-4: 2026-11-03)

    def sword_cap(self):
        return 6 * (("SwordRack" in self.owned) + ("SwordRack2" in self.owned))

    def hooks(self, swords):
        return sum(2 if self.B.blueprints[s["bp"]]["big"] else 1 for s in swords)

    def best_bp(self, big=False):
        key = (len(self.known), big)  # blueprints are only ever learned, so the count says when it changes
        if key not in self._best:
            c = [b for b in self.known if self.B.blueprints[b]["big"] == big]
            self._best[key] = max(sorted(c), key=lambda b: self.B.blueprints[b]["basePrice"]) if c else None
        return self._best[key]

    def value(self, s):
        return self.B.sword_value(s["bp"], s["metal"], s["pct"], s["polished"], s["hilt"], s["seat"], s["etch"], self.B.polish_bonus(self.owned))

    def make_sword(self, bp, metal, pct, polished=False):
        return {"bp": bp, "metal": metal, "pct": pct, "polished": polished, "hilt": self.B.best_hilt(self.own_made),
                "seat": self.B.seat_bonus(self.raw["hilts"]["seatTaps"]), "etch": None}

    # ---------------------------------------------------------------- buying
    def offers(self):
        if self._pads[0] != self.bought_n:  # the pads on offer change only with a purchase
            self._pads = (self.bought_n, [(i, self.B.price(i, self.merges)) for i in self.B.available(self.owned)
                                          if not self.B.upgrades[i]["decor"]])
        # gem pads (Showcase Stands 2-3, 2026-11-09): bought with gems, so on offer only once they're in hand
        out = [o for o in self._pads[1] if self.gems >= self.pad_gems(o[0])]
        if not self.tutorial_done:  # TycoonService.standing: no sword pad until the tutorial's letter is sent (2026-10-31)
            out = [o for o in out if not self.B.upgrades[o[0]].get("blueprint")]
        cap = self.raw.get("padCap")
        if cap:  # only the cheapest `cap` pads stand on the floor, plus the swords' and padAlways' (TycoonService, 2026-10-30)
            always = set(self.raw.get("padAlways", ()))
            # and every begun chain's next levels (Upgrades.chainStarted, 2026-10-31): the cap only opens new chains
            started = {self.B.chain_of[i] for i in self.owned if i in self.B.chain_of}
            if self.merges:
                started.add("Ore")
            # and what such a chain's next level waits for outside it (TycoonService.standing, 2026-11-05: Furnace 3 waits
            # for Furnace 2, so Furnace 2 stands once Anvil 3 is bought)
            waited = {a for i, u in self.B.upgrades.items() if i not in self.owned and self.B.chain_of.get(i) in started
                      and all(b in self.owned for b in u["after"] if self.B.chain_of.get(b) == self.B.chain_of.get(i))
                      for a in u["after"]}  # only for the chain's next level (its afters inside the chain bought)
            keep = [o for o in out if self.B.upgrades[o[0]].get("blueprint") or o[0] in always or self.B.chain_of.get(o[0]) in started
                    or o[0] in waited]
            hold = self.raw.get("holdFor")  # scenario: no new chain opens while this pad stands unbought
            out = keep + sorted((o for o in out if o not in keep), key=lambda o: o[1])[:0 if any(o[0] == hold for o in keep) else cap]
        D = self.raw["deliveries"]
        if "Delivery" in self.owned:
            for lv, key, prices, afters in ((self.cap_lv, "Cap", D["capacityPrice"], D["capacityAfter"]),
                                            (self.spd_lv, "Spd", D["speedPrice"], D["speedAfter"])):
                if lv + 1 < len(prices) + 1 and lv + 1 >= 1 and lv < len(prices):
                    nxt = lv + 1  # level to buy (1-based)
                    gate = afters[nxt - 2] if 2 <= nxt <= len(afters) + 1 else None  # no gates since the 2026-11-02 overhaul
                    if gate is None or gate in self.owned:
                        out.append((f"{key}{nxt}", prices[nxt - 1]))
        if "Crafter" in self.owned:
            for c in self.raw["employees"]["crafters"]:
                if c["id"] in self.hired or c["id"] == self.raw["employees"]["first"]:
                    continue
                a = c.get("after")
                if (a is None or a in self.owned or a in self.hired) and self.gems >= (c.get("gems") or 0):
                    out.append(("hire:" + c["id"], c["coins"]))  # its gems too: listed once you have them
        # Musashi's designs on sale, for coins (no type spends gems on swords)
        out += [("design:" + d, self.B.designs[d]["coins"]) for d in self.mu_stock if d not in self.known]
        return out

    def pad_gems(self, uid):
        """A gem pad's gems, at Musashi's deal price while it's one of his deals."""
        g = self.B.upgrades[uid].get("gems") or 0
        return self.B.musashi_discounted(g, self.mu_deals[uid]) if g and uid in self.mu_deals else g

    def musashi_look(self):
        """A sensible player looks at the stall at login and when a new stock comes: the hour's stock is rolled when
        first seen (Musashi.stock, then .seen), with its deals on the pads standing now."""
        if not self.mu_on or self.mu_seen == self.mu_hour or not self.B.musashi_open(self.owned, self.known):
            return
        self.mu_seen = self.mu_hour
        r = _Rng(self.rng["musashi"])
        self.mu_stock = self.B.musashi_stock(r, self.known, self.mu_missed)
        self.B.musashi_seen(self.mu_stock, self.known, self.mu_missed)
        # shortcut: "standing" is offers(), so a gem pad counts only once its gems are in hand
        self.mu_deals = dict(self.B.musashi_deals(r, [o[0] for o in self.offers() if o[0] in self.B.upgrades]))
        self.target = None  # re-pick at the new prices

    def on_musashi(self):
        self.mu_hour += 1

    def pick_target(self):
        """The type's pick, at Musashi's deal price when it's one of his deals (a pad it would buy anyway)."""
        o = self._pick_target()
        if o and o[0] in self.mu_deals and o[1] > 0:
            return o[0], self.B.musashi_discounted(o[1], self.mu_deals[o[0]])
        return o

    def _pick_target(self):
        offers = self.offers()
        if not offers:
            return None
        on = {o[0]: o for o in offers}
        for uid in self.order_left[:ORDER_LOOKAHEAD]:  # a recorded player: their next buys that stand here, in their order
            if uid in on:
                return on[uid]
        for o in offers:  # the tutorial's one buy first (the Guide's Polishing Station, for the letter's polish), then the free merge
            if o[0] == "MergeSlots" or (o[0] == "PolishStation" and not self.tutorial_done):
                return o
        for o in offers:  # scenario: a pinned goal players follow (raw["goalFirst"], ids)
            if o[0] in self.raw.get("goalFirst", ()):
                return o
        best = self.B.blueprints[self.best_bp()]["basePrice"]

        def bp_value(uid):
            b = uid[7:] if uid.startswith("design:") else self.B.upgrades[uid]["blueprint"]
            return 0 if self.B.blueprints[b]["big"] else self.B.blueprints[b]["basePrice"]

        return behavior.choose_target(self.A, self.B, offers, bp_value, best, self.grinder_ok)

    def buy(self, uid, price):
        self.coins -= price
        self.bought_n += 1
        if uid in self.order_left:
            self.order_left.remove(uid)
        self.spent += price
        self.purchases.append((self.t / 60, uid, price))
        self.progress.append(self.t)
        self.mark(uid)
        pad_gems = self.pad_gems(uid) if uid in self.B.upgrades else None
        if uid in self.mu_deals:  # one of Musashi's deals: the pad bought at his price
            self.mu_deal_buys += 1
            self.mu_saved += self.B.price(uid, self.merges) - price
            self.mu_gems_saved += (self.B.upgrades[uid].get("gems") or 0) - (pad_gems or 0)
            del self.mu_deals[uid]
        if uid.startswith("design:"):  # a Musashi design: a blueprint learned (Shared/Musashi)
            self.known.add(uid[7:])
            self.mu_designs.append((round(self.t / 60, 1), uid[7:]))
            return
        if pad_gems:  # a gem pad (TycoonService, 2026-11-09)
            self.gems -= pad_gems
            self.gems_out["pads"] = self.gems_out.get("pads", 0) + pad_gems
        if uid.startswith("hire:"):
            cid = uid[5:]
            if self.gems < (self.B.crafters[cid].get("gems") or 0):
                return
            self.gems -= self.B.crafters[cid].get("gems") or 0
            self.gems_out["hires"] = self.gems_out.get("hires", 0) + (self.B.crafters[cid].get("gems") or 0)
            self.hired[cid] = 0
            self.equip()
            return
        if uid.startswith("Cap"):
            self.cap_lv += 1
            return
        if uid.startswith("Spd"):
            self.spd_lv += 1
            return
        if uid == "MergeSlots":  # Ore Slots 2-6 go back to unbought, luck +MERGE_LUCK, their prices x MERGE_PRICE
            self.merges += 1
            self.owned -= {f"OreStand{k}" for k in range(2, 7)}
            self.mark(f"Merge{self.merges}")
            return
        self.owned.add(uid)
        u = self.B.upgrades[uid]
        self.owned.update(u.get("with") or ())  # bought with it, no pad of its own: the Sword Crafter's Anvil 2 (2026-11-02)
        for w in u.get("with") or ():
            self.mark(w)
        # after owned: the Katana letter's gate is the Machete itself; AllPads counts the with-items (hires, caps, speeds, merges aren't pads)
        if any(c.get("afterUpgrade") == uid for c in self.raw["commissions"]):
            self.maybe_katana_letter()  # ShopService: a letter waiting on this buy comes letterDelay after it
        if self.until_done and uid in self.all_pads and self.all_pads <= self.milestones.keys():
            self.mark("AllPads")
            self.done = True
        if u.get("blueprint"):
            self.known.add(u["blueprint"])
        if uid in ("Furnace2", "Furnace3"):
            self.furnaces["Forge" + uid[-1]] = None
        if uid in self.holders_def:
            self._add_holder(uid)
        if uid == "Delivery":
            self.cap_lv = self.spd_lv = 0
            self.cart_refill()
        if uid == "Crafter":
            self.hired[self.raw["employees"]["first"]] = 0
        if uid in ("Crafter", "Anvil3", "Anvil4"):
            self.equip()
        if uid in ("Stocker", "Etcher"):
            self.staff[uid.lower()] = 0
            self.push(1, uid.lower())
        if uid in ("Cashier", "Promoter"):
            self.staff[uid.lower()] = 0

    def equip(self):
        """The best crafters work, one per crafter anvil bought (Anvil2 with the Sword Crafter, Anvil3, Anvil4)."""
        anvils = [a for a in self.raw["employees"]["anvils"] if (a == "Anvil2" and "Crafter" in self.owned) or a in self.owned]
        def rate(cid):
            lv = self.B.staff_level(self.hired[cid])[0]
            return self.B.grade(self.B.crafter_quality(cid, lv))[1] / self.B.level_seconds(lv, self.B.crafters[cid]["forge"])
        best = sorted(self.hired, key=rate, reverse=True)[: len(anvils)]
        self.equipped = dict(zip(anvils, best))
        for a in anvils:
            if not self.crafter_busy.get(a):
                self.crafter_busy[a] = True
                self.push(0.5, "crafter", a, "start")

    def hire_reserve(self):
        """Gems kept for the next crafter whose gate is open (EmployeeService hires for coins + gems), or for the next gem
        pad standing (Showcase Stands 2-3, 2026-11-09): the cheaper of the two."""
        need = [self.B.upgrades[i]["gems"] for i in self.B.available(self.owned) if self.B.upgrades[i].get("gems")]
        if "Crafter" in self.owned:
            E = self.raw["employees"]
            need += [c.get("gems") or 0 for c in E["crafters"] if c["id"] not in self.hired and c["id"] != E["first"]
                     and (c.get("after") is None or c["after"] in self.owned or c["after"] in self.hired)]
        return min(need, default=0)

    def buy_gems(self):
        """GemService "buy": Better Advertising I first (the Guide's step), then this type's pair, then the cheapest. Not
        before the tutorial's letter is sent: the Guide's gem step comes after it, with the letter's gems."""
        if not self.tutorial_done:
            return
        while True:
            nxt = {g["id"]: g["prices"][self.gem_levels[g["id"]]] for g in self.raw["gemUpgrades"]["list"]
                   if self.gem_levels[g["id"]] < len(g["prices"])}
            if not nxt:
                return
            if self.gem_order_left:  # a recorded player: their gem buys in their order, each once they have the gems
                pick = self.gem_order_left[0]
                if pick not in nxt:
                    self.gem_order_left.pop(0)
                    continue
                if self.gems < nxt[pick]:
                    return
                self.gem_order_left.pop(0)
            else:
                guide = self.gem_levels["Advertising"] == 0 and "Advertising" in nxt
                pool = ["Advertising"] if guide else [g for g in behavior.GEM_GROUPS.get(self.A.gems, ()) if g in nxt] or list(nxt)
                pick = min(pool, key=lambda g: nxt[g])
                if self.gems < nxt[pick] or (not guide and self.gems - nxt[pick] < self.hire_reserve()):
                    return
            self.gems -= nxt[pick]
            self.gems_out[pick] = self.gems_out.get(pick, 0) + nxt[pick]
            self.gem_levels[pick] += 1
            self.mark(f"{pick}{self.gem_levels[pick]}")
            self.progress.append(self.t)
            self.mail_clock()  # More Clients may make room

    # ---------------------------------------------------------------- the player's decisions
    def decide(self):
        A, r = self.A, self.rng["act"]
        self.buy_gems()
        self.musashi_look()
        if self.daily_held and self.lessons_done():
            self.claim_daily()
            self.buy_gems()
        if self.target is None or self.target[0] not in {o[0] for o in self.offers()}:
            self.target = self.pick_target()
        # 1. the letter, from the mail anywhere
        if self.letter and self.letter_sword() is not None:
            return self.task_letter()
        fit = self.mail_fit()
        if fit:
            return self.task_mail(*fit)
        # 2. the Cashier's till, when it covers what we save for
        if self.till > 0 and self.target and self.coins < self.target[1] <= self.coins + self.till:
            return self.task_till()
        # 3. buy
        if self.target and self.coins >= self.target[1]:
            return self.task_buy(*self.target)
        if A.idle_chance and r.random() < A.idle_chance and self.tutorial_done:  # no idling while the tutorial leads
            return self.task_idle(r.uniform(*A.idle_len))
        if A.tend:
            t = self.tend_tasks()
            if t:
                return t
        # 4-5. forge a hot ingot (in hand, or ready in a furnace)
        if self.hot:
            return self.task_forge()
        ready = [f for f in self.furnaces_owned() if self.furnaces[f] and self.furnaces[f]["who"] == "p" and self.furnaces[f]["ready"] <= self.t]
        if ready:
            return self.task_take(ready[0])
        # 6. finish swords
        if any(self.needs_finish(s) for s in self.swords):
            return self.task_finish()
        # 7-10. the shop, the racks, the cart
        t = self.tend_tasks() if not A.tend else None
        if t:
            return t
        # 10b. sitting back: no new sword of its own; the crew still gets its ingots
        if self.sitting_back():
            free = [f for f in self.furnaces_owned() if self.furnaces[f] is None]
            if free and any(self.order_for(c[0]) for c in self.cold):  # an ingot kept for a mail order is still worked
                return self.task_heat(free[0])
            rack_room = self.equipped and len(self.ingot_rack) + len(self.cold_rack) < self.ingot_cap()
            spare = [c for c in self.cold if not self.order_for(c[0])]
            if spare and rack_room:
                self.cold.remove(spare[-1])
                self.cold_rack.append(spare[-1][0])
                return self.task_rack_ingots()
            if rack_room and not spare:
                return self.task_ore()
            return self.task_idle(r.uniform(30, 120))
        # 11. heat
        free = [f for f in self.furnaces_owned() if self.furnaces[f] is None]
        if self.cold and free:
            return self.task_heat(free[0])
        # 12. ore
        if self.want_ore():
            return self.task_ore()
        waiting = [self.furnaces[f]["ready"] - self.t for f in self.furnaces_owned() if self.furnaces[f] and self.furnaces[f]["who"] == "p"]
        return self.task_idle(max(1.0, min(waiting)) if waiting else 3.0, cat="wait")

    def sitting_back(self):
        """Allen 2026-10-29: "once players get automated employees, the actual player production tends to fall off. they
        like to just sit back and collect money". The chance this decision skips starting a sword of one's own: the type's
        sit_back, a third each for the Sword Crafter, the Stocker and the Cashier (the shop runs without you)."""
        crew = sum(x in self.owned for x in ("Crafter", "Stocker", "Cashier")) / 3
        p = self.A.sit_back * crew * self.T.get("sit_back_scale", 1.0)
        return p > 0 and self.rng["act"].random() < p

    def tend_tasks(self):
        A = self.A
        crew = bool(self.equipped)
        if self.cold_rack and crew and len(self.ingot_rack) < self.ingot_cap():
            return self.task_rack_ingots()
        empty = [s for s in self.slots if s["sword"] is None and not s["claimed"]]
        ready = [s for s in self.swords if not self.needs_finish(s) and "order" not in s]  # what task_stock places
        if ready and any(self.fits(sw, sl) for sw in ready for sl in empty):
            return self.task_stock()
        if (len(self.sword_rack) > len(self.held()) and "Stocker" not in self.owned and empty  # held: kept for a letter (P1)
                and (A.tend or len(self.sword_rack) >= self.sword_cap() or not any(s["sword"] for s in self.slots))):
            return self.task_rack_to_shop()
        if "Delivery" in self.owned and A.cart != "never":
            if self.cart and self.cart["back"] <= self.t:
                return self.task_cart_collect()
            cap = self.B.cart_capacity(self.cap_lv)
            spare = sorted((s for s in self.swords if not self.B.blueprints[s["bp"]]["big"] and not self.needs_finish(s)
                            and "order" not in s), key=self.value)
            out = self.cart is not None and self.cart["back"] != float("inf")
            if (self.cart is None or (out and self.cart_queue is None)) and self.t >= self.cart_retry and (
                    (A.cart == "active" and len(spare) >= max(2, cap // 2) and not empty) or len(spare) >= cap):
                return self.task_cart(spare, queue=out)
        spare = [c for c in self.cold if not self.order_for(c[0])]  # an ingot kept for a mail order stays (as sitting_back)
        if crew and A.tend and spare and len(self.ingot_rack) < self.ingot_cap() // 2:
            self.cold.remove(spare[-1])
            self.cold_rack.append(spare[-1][0])
            return self.task_rack_ingots()
        return None

    def fits(self, sword, slot):
        return self.B.blueprints[sword["bp"]]["big"] == slot["big"]

    def wants_etch(self, s):
        """Etched by this player: its type etches, or the mail order it was made for asks for it."""
        return (self.A.etch or bool(s.get("order", {}).get("etched"))) and self.B.best_etch(self.owned) is not None and s["etch"] is None  # a bought etch (2026-11-01)

    def wants_polish(self, s):
        """Polished by this player: its type polishes, or it's the tutorial letter's Iron Tantō (polished since 2026-10-30;
        the guide has everyone polish it)."""
        letter = self.letter is not None and self.letter[0] == "IronTanto" and s["bp"] == "tanto" and s["metal"] == "Iron"
        return (self.A.polish or letter) and "PolishStation" in self.owned and not s["polished"]

    def needs_finish(self, s):
        return self.wants_polish(s) or self.wants_etch(s)

    def want_ore(self):
        mine = len(self.cold) + len(self.hot) + sum(1 for f in self.furnaces_owned() if self.furnaces[f] and self.furnaces[f]["who"] == "p")
        rack_room = bool(self.equipped) and len(self.ingot_rack) + len(self.cold_rack) < self.ingot_cap()
        return mine < len(self.furnaces_owned()) or rack_room

    def letter_sword(self):
        name = self.letter[0]
        for i, s in enumerate(self.swords):
            if name == "IronTanto" and s["bp"] == "tanto" and s["metal"] == "Iron" and s["polished"]:
                return i
            if name == "Katana" and s["bp"] == "katana" and s["pct"] >= 90:
                return i
        return None

    # ---------------------------------------------------------------- the player's tasks: (seconds, then what happens)
    def run_task(self, secs, cat, done):
        if cat not in ("wait", "idle"):
            secs *= self.A.slack * (1.0 if self.tutorial_done else self.A.learn)  # allen.py fits slack; learn: the tutorial
        self.spend(cat, secs)
        self.push(secs, "player", done)
        return True

    def task_idle(self, secs, cat="idle"):
        return self.run_task(secs, cat, lambda: None)

    def task_letter(self):
        name = self.letter[0]

        def done():
            i = self.letter_sword() if self.letter else None
            if i is None:
                return
            self.swords.pop(i)
            spec = next(c for c in self.raw["commissions"] if c["id"] == name)
            self.earn(spec["reward"])
            self.add_gems(spec.get("gems") or 0, "letters")
            self.reputation += self.raw["reputation"]["commission"]
            self.letters += 1
            self.quest_times.append(self.t / 60)
            self.letters_done.add(name)
            self.mail_clock()  # the first letter opens the mail's orders
            self.letter = None
            self.mark("Letter" + name)
            self.progress.append(self.t)
            if name == "IronTanto":
                self.tutorial_done = True
                self.ramp = (self.t, self.sold)
                self.mark("TutorialDone")
        return self.run_task(self.T["letter"], "letters", done)

    def task_till(self):
        secs = self.walk("shop") + 1.0

        def done():
            self.coins += self.till  # already counted in earned at the sale
            self.till = 0.0
        return self.run_task(secs, "stock", done)

    def task_buy(self, uid, price):
        window = uid.startswith(("hire:", "Cap", "Spd", "design:"))  # shortcut: Musashi's stall as a window, no walk
        secs = self.T["menu"] if window else self.walk("pad:" + uid if "pad:" + uid in self.pos else "Anvil") + self.T["buy"]
        self.target = None

        def done():
            if self.coins >= price:
                self.buy(uid, price)
        return self.run_task(secs, "buy", done)

    def task_take(self, forge):
        secs = self.walk(forge) + self.T["furnace_take"]

        def done():
            f = self.furnaces[forge]
            if f and f["who"] == "p":
                self.hot.append((f["metal"], f["ore"]))
                self.furnaces[forge] = None
                self.used_at[forge] = self.t
        return self.run_task(secs, "furnace", done)

    def task_heat(self, forge):
        secs = self.walk(forge) + self.T["furnace_put"]

        def done():
            if self.furnaces[forge] is None and self.cold:
                metal, ore_t = self.pick_cold()
                self.furnaces[forge] = {"who": "p", "metal": metal, "ore": ore_t, "ready": self.t + self.heat_time(forge)}
                self.used_at[forge] = self.t
        return self.run_task(secs, "furnace", done)

    def pick_cold(self):
        iron = next((c for c in self.cold if c[0] == "Iron"), None)
        if self.letter and self.letter[0] == "IronTanto" and iron:
            self.cold.remove(iron)
            return iron
        kept = next((c for c in self.cold if self.order_for(c[0])), None)  # an ingot kept for a mail order goes first
        if kept:
            self.cold.remove(kept)
            return kept
        best = max(self.cold, key=lambda c: self.B.metal_multiplier(c[0]))
        self.cold.remove(best)
        return best

    def task_forge(self):
        # ponytail: the whole visit scales with the strike pace, and with the blade's strikes over the ones T["forge"] was
        # measured on (timings.FORGE_STRIKES; 10 of 12 since 2026-10-30). Timed for best_bp(): a letter or an order can
        # swap the blueprint in done(), the same strikes while every blueprint has 10.
        strikes = self.B.blueprints[self.best_bp()]["strikes"] / timings.FORGE_STRIKES
        secs = self.walk("Anvil") + self.T["forge"] * strikes * self.B.strike_pace(self.owned) + self.T["hilt_seat"]
        metal, ore_t = self.hot.pop(0)

        def done():
            bp = self.best_bp()
            if self.order_for(metal):
                order = self.order_for(metal)
                order["have"] = "sword"
                sw = self.make_sword(order["blueprintId"], metal, self.A.forge)
                sw["t"], sw["order"] = {"ore": ore_t, "forged": self.t}, order
                self.swords.append(sw)
                self.own_made += 1
                return
            elif self.letter and self.letter[0] == "IronTanto" and metal == "Iron":
                bp = "tanto"
            elif self.letter and self.letter[0] == "Katana" and "katana" in self.known:
                bp = "katana"
            else:
                big = self.best_bp(big=True)
                stand = [s for s in self.slots if s["big"]]
                if big and stand and all(s["sword"] is None for s in stand) and not any(self.B.blueprints[s["bp"]]["big"] for s in self.swords):
                    bp = big
            sw = self.make_sword(bp, metal, self.A.forge)
            sw["t"] = {"ore": ore_t, "forged": self.t}
            self.swords.append(sw)
            self.own_made += 1
            self.mark("Sword1") if self.own_made == 1 else None
        return self.run_task(secs, "forge", done)

    def task_finish(self):
        secs = 0.0
        todo = [s for s in self.swords if self.needs_finish(s)]
        polish = [s for s in todo if self.wants_polish(s)]
        etch = [s for s in todo if self.wants_etch(s)]
        if polish:
            secs += self.walk("PolishStation") + self.T["polish"] * len(polish)
        if etch:
            secs += self.walk("EtchingTable") + self.T["etch"] * len(etch)

        def done():
            for s in polish:
                s["polished"] = True
            for s in etch:
                s["etch"] = self.B.best_etch(self.owned)
        return self.run_task(secs, "finish", done)

    def task_stock(self):
        secs = self.walk("shop")
        placed = []
        for sw in [s for s in self.swords if not self.needs_finish(s) and "order" not in s]:
            sl = next((x for x in self.slots if x["sword"] is None and not x["claimed"] and self.fits(sw, x)), None)
            if sl:
                sl["claimed"] = True  # ours while we walk over
                placed.append((sw, sl))
        secs += self.T["place"] * len(placed)
        for sw, _ in placed:
            self.swords.remove(sw)

        def done():
            for sw, sl in placed:
                sl["sword"], sl["claimed"] = self.placed(sw), False
            if placed and self.sold == 0:  # ShopService: until the first sale, a display sends a customer at once
                self.send_customer(first=True)
        return self.run_task(secs, "stock", done)

    def task_rack_ingots(self):
        room = self.ingot_cap() - len(self.ingot_rack)
        n = min(room, len(self.cold_rack))
        secs = self.walk("IngotRack") + self.T["rack"] * n
        moving = [self.cold_rack.pop() for _ in range(n)]

        def done():
            self.ingot_rack.extend(moving)
        return self.run_task(secs, "racks", done)

    def task_rack_to_shop(self):
        empty = [s for s in self.slots if s["sword"] is None and not s["claimed"]]
        take = []
        held = self.held()  # kept for a letter (P1)
        for sw in list(self.sword_rack):
            if any(sw is h for h in held):
                continue
            sl = next((x for x in empty if self.fits(sw, x) and x not in [p[1] for p in take]), None)
            if sl:
                take.append((sw, sl))
        for sw, sl in take:
            _drop(self.sword_rack, sw)
            sl["claimed"] = True
        secs = self.walk("SwordRack") + self.T["rack"] * len(take) + self.walk("shop") + self.T["place"] * len(take)

        def done():
            for sw, sl in take:
                sl["sword"], sl["claimed"] = self.placed(sw), False
        return self.run_task(secs, "stock", done)

    # --- the cart (DeliveryService) --------------------------------------------------------------------------------
    def cart_refill(self):
        """Offers up to Deliveries.OFFERS, the same kinds of sword as the mail but no big ones."""
        bps = sorted(b for b in self.known if not self.B.blueprints[b]["big"])
        D = self.raw["deliveries"]
        while len(self.cart_offers) + self.cart_waiting < D["offers"]:
            self.cart_offers.append(self.B.make_delivery(_Rng(self.rng["cart"]), ["courier"], bps, "PolishStation" in self.owned,
                                                         self.B.best_etch(self.owned) is not None, self.rep_level(), self.B.cart_capacity(self.cap_lv)))

    def cart_fill(self, offer, spare):
        """The cheapest spare swords that fill this offer, or None."""
        fits = spare if offer["kind"] == "bulk" else [s for s in spare if self.B.order_fits(offer["need"], self.view(s))]
        return fits[:offer["count"]] if len(fits) >= offer["count"] else None

    def send_cart(self, offer, swords):
        self.cart = {"back": self.t + self.B.cart_trip(self.spd_lv), "pay": self.B.cart_pay([self.value(s) for s in swords]),
                     "gems": offer["gems"], "count": len(swords), "kind": offer["kind"]}
        self.carted += len(swords)

    def task_cart(self, spare, queue=False):
        """At the bay's board: the offer it can fill that pays the most gems (skipping up to three for new ones), packed
        with the cheapest swords that fit; the cart leaves, or with `queue` (the cart is out) it waits packed as the next
        order (DeliveryService's queued order, 2026-10-29). Nothing fits: back to work, and look again in a minute."""
        secs = self.walk("DeliveryBay")
        best = None
        for _ in range(4):
            fills = [(o["gems"], o["count"], i, self.cart_fill(o, spare)) for i, o in enumerate(self.cart_offers)]
            fills = [f for f in fills if f[3]]
            if fills:
                best = max(fills, key=lambda f: (f[0], f[1]))
                break
            if not self.cart_offers:
                break
            self.cart_offers.pop(0)  # skip the oldest: its slot's new offer comes Deliveries.SKIP_WAIT later
            self.cart_waiting += 1
            self.push(self.raw["deliveries"]["skipWait"], "cart_offer")
            self.cart_skips += 1
            secs += 1.0
        if not best:  # a look at the board, nothing it can fill
            self.cart_retry = self.t + secs + self.T["menu"] + 60
            return self.run_task(secs + self.T["menu"], "cart", lambda: None)
        offer = self.cart_offers.pop(best[2])
        swords = best[3]
        for s in swords:
            self.swords.remove(s)
        secs += self.T["cart_visit"]  # one visit, whatever the count: Auto-Fill packs the crate in one tap

        def done():
            if queue:
                self.cart_queue = (offer, swords)
            else:
                self.send_cart(offer, swords)
            self.cart_refill()
        return self.run_task(secs, "cart", done)

    def task_cart_collect(self):
        """The board's prompt pays at once (DeliveryController); a queued order becomes the cart's and goes out on it."""
        q = self.cart_queue
        secs = self.walk("DeliveryBay") + (self.T["cart_visit"] if q else 0.0)
        c = self.cart

        def done():
            self.earn(c["pay"])
            self.add_gems(c["gems"], "cart")
            self.reputation += c["count"]  # one per sword, as the window says
            if c["kind"] == "bulk":
                self.cart_bulk += 1
            else:
                self.cart_special += 1
            self.cart = None
            self.progress.append(self.t)
            if q:
                self.cart_queue = None
                self.send_cart(*q)
        self.cart = dict(c, back=float("inf"))  # being collected
        return self.run_task(secs, "cart", done)

    # --- mail orders (Shared/Orders, ShopService.refillOrders) -------------------------------------------------------
    def mail_slots(self):
        """Room for orders: More Clients' letters at once, less the story letter open (ShopService, 2026-10-30)."""
        return max(0, self.raw["gemUpgrades"]["levels"][self.gem_levels["Clients"]]["mailSlots"] - (1 if self.letter else 0))

    def mail_clock(self):
        """After the first letter: a new order comes Quicker Mail's gap after the last while the mail has room."""
        if "IronTanto" not in self.letters_done or self.mail_due is not None or len(self.orders) >= self.mail_slots():
            return
        self.mail_due = self.t + self.raw["gemUpgrades"]["levels"][self.gem_levels["Mail"]]["mailGap"] * (1 - self.stand_effects()["Mail"])
        self.push(self.mail_due - self.t, "mail", self.mail_due)

    def new_order(self):
        o = self.B.make_order(_Rng(self.rng["mail"]), ["sender"], sorted(self.known), sorted(self.discovered),
                              "PolishStation" in self.owned, self.B.best_etch(self.owned) is not None, self.rep_level())
        self.order_id += 1
        o["id"] = self.order_id
        o["chase"] = self.rng["act"].random() < self.A.mail  # one it works on (behavior.Archetype.mail)
        self.orders.append(o)

    def on_cart_offer(self):
        self.cart_waiting -= 1
        self.cart_refill()

    def on_mail(self, due):
        if due != self.mail_due:
            return  # superseded (a day's catch-up)
        self.mail_due = None
        if len(self.orders) < self.mail_slots():
            self.new_order()
        self.mail_clock()

    def order_for(self, metal):
        """The open order an ingot of this metal was kept for (chasing players), or None."""
        return next((o for o in self.orders if o.get("have") == "ingot" and o.get("materialId") == metal), None)

    def held(self):
        """The rack swords the Stocker leaves for a letter (Orders.held, 2026-11-09, P1): for each order it works on
        (`chase`, the game's Accept) that no sword in hand fits, the first rack sword that fits it, one an order."""
        held = []
        for o in self.orders:
            if not o.get("chase") or any(self.B.order_fits(o, self.view(s)) for s in self.swords):
                continue
            sw = next((s for s in self.sword_rack if not any(s is h for h in held) and self.B.order_fits(o, self.view(s))), None)
            if sw is not None:
                held.append(sw)
        return held

    def mail_fit(self):
        """(sword, order) for a finished sword in hand, or on the Sword Rack (ShopService sends it from there since
        2026-11-09, P1), that an open mail order takes, or None."""
        if not self.orders or not (self.swords or self.sword_rack):
            return None
        shapes = {o["blueprintId"] for o in self.orders}  # only swords of a shape some order asks for can fit
        swords = [s for s in self.swords if s["bp"] in shapes and not self.needs_finish(s)]
        swords += [s for s in self.sword_rack if s["bp"] in shapes]
        for o in self.orders:
            for s in swords:
                if s["bp"] == o["blueprintId"] and self.B.order_fits(o, self.view(s)) and s.get("order", o) is o:
                    return s, o
        return None

    def task_mail(self, sw, o):
        """Hand the sword in from the mail (anywhere): PAY x its value, its metal at no less than a typical ingot, x the shop boost, + gems."""
        _drop(self.swords if any(sw is s for s in self.swords) else self.sword_rack, sw)
        self.orders.remove(o)
        for s in self.swords:  # a sword made for this order but beaten to it by another that fit: free again
            if s.get("order") is o:
                del s["order"]

        def done():
            pay = self.B.order_pay(self.value(sw), self.B.metal_multiplier(sw["metal"]), self.B.typical_metal(self.B.luck(self.merges)),
                                    self.B.shop_boost(self.owned))
            self.earn(pay)
            self.mail_coins += pay * self.coin_boost()
            self.add_gems(o["gems"], "mail")
            self.reputation += self.raw["reputation"]["order"]
            self.mail_done += 1
            self.quest_times.append(self.t / 60)
            self.progress.append(self.t)
            self.mail_clock()
        return self.run_task(self.T["letter"], "letters", done)

    def on_day(self):
        """A new day's session (behavior.PLAY_DAY of play): today's daily reward. Between days the cart came back, the
        mail filled up and the Cashier earned (settle_away): they run on the server clock while you are away."""
        if self.day > 0:
            self.settle_away()
            self.income_log = []
            self.day_start = self.t
            if self.cart and self.cart["back"] > self.t and self.cart["back"] != float("inf"):
                self.cart["back"] = self.t
            if "IronTanto" in self.letters_done:
                while len(self.orders) < self.mail_slots():
                    self.new_order()
                self.mail_due = None
        if self.day == 0 and not self.lessons_done():
            # GemController: the first daily window waits for the lessons' end (the letter sent, then the gem step);
            # decide() claims it then. shortcut: a second day that comes first finds it still held and gives nothing
            # more (a player an hour into the tutorial), fine unless the sim's first hour is ever that slow
            self.daily_held = True
        else:
            self.claim_daily()
        if self.t + behavior.PLAY_DAY < self.horizon:
            self.push(behavior.PLAY_DAY, "day")
        if self.mu_on:  # a new wall-clock hour since the last session; shortcut: each session starts at a random minute
            self.mu_hour += 1  # of the hour, so a 1 h session sees the next stock come once, at the hour mark
            self.push(self.raw["musashi"]["clock"] * (1 - self.rng["musashi"].random()), "musashi")

    def lessons_done(self):
        """MyPlot.lessonsDone: the tutorial's letter sent and the gem step's buy made."""
        return self.tutorial_done and any(self.gem_levels.values())

    def claim_daily(self):
        self.daily_held = False
        self.day += 1
        _, gift = self.B.daily(self.streak, self.day - 1, self.day)
        self.streak += 1
        self.add_gems(gift.get("gems", 0), "daily")
        if gift.get("coinMinutes"):  # coins the game gives unboosted (GemService), counted as earned
            c = self.B.gift_coins(gift["coinMinutes"], self.B.coin_rate(self.earned, self.t))
            self.coins += c
            self.earned += c

    def task_ore(self):
        """Pull until the box shows something worth keeping (or collect the Auto Ore Roller's), take what's kept."""
        if "AutoRoller" in self.passes:
            secs = self.walk("OreRoller")
            if self.first_pull is None:
                self.first_pull = self.t + secs
                self.mark("FirstPull")
            ores = list(self.stands)
            self.stands = []
            if not ores:
                return self.task_idle(2.0, cat="wait")
            secs += self.T["collect"] * self.keep_ores(ores)
            return self.run_task(secs, "ore", lambda: None)
        secs = self.walk("OreRoller")
        if self.first_pull is None:
            self.first_pull = self.t + secs
            self.mark("FirstPull")
        pulls, kept = 0, 0
        while kept == 0 and pulls < 12:
            luck = self.luck()
            res = [self.roll_ore(luck) for _ in range(self.slots_n())]
            self.count_luck(res, luck)
            secs += self.T["pull_hold"] + self.B.roll_length(res)
            pulls += 1
            relax = 1 if pulls >= 6 else 0
            kept = self.keep_ores(res, relax)
            secs += self.T["collect"] * kept
        return self.run_task(secs, "ore", lambda: None)

    def roll_ore(self, luck):
        """ForgeService.rollFor, one stand: the open letter's metal (the first letter's Iron) one pull in 3 and always by the
        second (wantPulls); for a new player who has collected nothing and made nothing, a Common, then an Uncommon
        (tutorialPulls); else Materials.roll."""
        spec = next((c for c in self.raw["commissions"] if self.letter and c["id"] == self.letter[0]), None)
        if spec and spec.get("materialId") and not self.tutorial_done:  # the tutorial only (2026-11-08)
            self.want_pulls += 1
            if self.want_pulls >= 2 or self.next_number() < 1 / 3:
                self.want_pulls = 0
                return spec["materialId"]
        if not self.discovered and self.own_made == 0:
            self.tutorial_pulls += 1
            rarity = {1: "Common", 2: "Uncommon"}.get(self.tutorial_pulls)
            if rarity:
                pool = [m for m in self.B.metals.values() if m["rarity"] == rarity]
                return pool[self.next_integer(1, len(pool)) - 1]["id"]
        # ForgeService FIRST_PULL_METAL (Allen 2026-11-10, "Legendary"): the first stand rolled after the tutorial brings a
        # Mythril for a player whose roller has never rolled one; the other stands and later pulls roll the usual odds
        gift = self.raw.get("firstPull", "Mythril")
        if gift and self.tutorial_done and not self.first_pull_given:
            self.first_pull_given = True
            return gift
        return self.B.roll(self, luck)

    def next_number(self):  # rules.roll draws through this Sim (the ore stream)
        return self.rng["ore"].random()

    def next_integer(self, a, b):
        return self.rng["ore"].randint(a, b)

    def count_luck(self, res, luck):
        for m in res:
            if m == self.raw.get("firstPull", "Mythril"):
                self.first_pull_given = True  # rolled already (d.rolled), in the tutorial or as the gift
            if self.B.rarity_index[self.B.metals[m]["rarity"]] >= 2:
                self.rolled_rare = True
            self.ores_seen[self.B.rarity_index[self.B.metals[m]["rarity"]]] += 1
            self.luck_got += self.B.metal_multiplier(m)
            self.luck_exp += self.B.typical_metal(luck)

    def keep_ores(self, res, relax=0):
        """Takes what this player keeps: its own (rarity >= keep), the first letter's Iron, the crew's (rack_keep)."""
        rank = lambda m: self.B.rarity_index[self.B.metals[m]["rarity"]]
        keep = self.A.keep - relax if self.sold > 0 else 0
        kept = 0
        mine_room = max(0, len(self.furnaces_owned()) + 1 - len(self.cold))
        for m in sorted(res, key=rank, reverse=True):
            # an ore an open mail order it works on asks for, kept for it
            o = next((o for o in self.orders if o.get("chase") and o.get("materialId") == m and not o.get("have")
                      and o["blueprintId"] in self.known), None)
            if o:
                o["have"] = "ingot"
                self.cold.append((m, self.t))
                self.discovered.add(m)
                kept += 1
                continue
            letter_iron = self.letter and self.letter[0] == "IronTanto" and m == "Iron" and not any(c[0] == "Iron" for c in self.cold)
            if (rank(m) >= keep and mine_room > 0) or letter_iron:
                self.cold.append((m, self.t))
                self.discovered.add(m)
                mine_room -= 1
                kept += 1
            elif self.equipped and rank(m) >= self.A.rack_keep and len(self.ingot_rack) + len(self.cold_rack) < self.ingot_cap():
                self.cold_rack.append(m)
                self.discovered.add(m)
                kept += 1
        return kept

    # ---------------------------------------------------------------- the world
    def on_player(self, done):
        done()
        self.decide()

    def on_autoroll(self):
        if "AutoRoller" not in self.passes:
            return
        keep_rank = self.B.rarity_index.get(self.raw["store"]["keeps"][1], 2)  # the chip's default, Rare
        if any(self.B.rarity_index[self.B.metals[m]["rarity"]] >= keep_rank for m in self.stands):
            self.push(2.0, "autoroll")
            return
        luck = self.luck()
        res = [self.B.roll(self, luck) for _ in range(self.slots_n())]
        self.count_luck(res, luck)
        self.stands = res
        self.push(self.B.roll_length(res) + 0.3, "autoroll")

    def on_weather(self):
        W = self.raw["weather"]["list"]
        choices = [w for w in W if w is not self.weather]
        x = self.rng["weather"].random() * sum(w["weight"] for w in choices)
        for w in choices:
            x -= w["weight"]
            if x <= 0:
                self.weather = w
                break
        self.push(self.raw["weather"]["spell"], "weather")

    def weather_is(self, effect):
        return self.tutorial_done and self.weather and self.weather["effect"] == effect

    def on_spawn(self):
        r = self.rng["cust"]
        if not self.tutorial_done:
            lo, hi = self.raw["shop"]["tutorialGap"]
            f = 1.0
        else:
            lo, hi = self.raw["gemUpgrades"]["levels"][self.gem_levels["Advertising"]]["walkIn"]
            f = 1 / (self.weather["value"] if self.weather_is("WeatherCustomers") else 1)
            if self.ramp:  # ShopService: eases from the tutorial's gap over rampSecs or rampSales sales (2026-10-31)
                S = self.raw["shop"]
                k = max((self.t - self.ramp[0]) / S.get("rampSecs", 300), (self.sold - self.ramp[1]) / S.get("rampSales", 5))
                if k < 1:
                    tlo, thi = S["tutorialGap"]
                    lo, hi = tlo + (lo - tlo) * k, thi + (hi - thi) * k
        if "promoter" in self.staff:
            f *= self.B.perk("promoter", self.staff["promoter"])
        # ShopService.showcasePull: each Showcase Stand owned holds a sword and brings walk-ins sooner by its pull
        # (Showcase.pull, 2026-11-04). ponytail: every stand counts as filled, its sword not taken from sale, with the best
        # sword known in a Rare metal, polished once the Polishing Station is bought, etched once an etch is
        f *= 1 - self.stand_effects()["Customers"]  # since 2026-11-09 only Customers swords, capped (Showcase families)
        gap = r.uniform(lo * f, hi * f)
        # ShopService (2026-11-10): a walk-in due while the shop is full waits for room (within a second of one leaving),
        # and the next gap starts once they're sent
        if self.send_customer() == "full":
            self.due = True
            return
        self.push(gap, "spawn")

    def send_customer(self, first=False):
        """ShopService.sendCustomer. first: the tutorial's customer, sent the moment a sword goes on display before the
        first sale (ShopService, since 2026-10-22), fading in at CustomerSpawn with no stroll up the street (2026-11-09)."""
        r = self.rng["cust"]
        # ShopService.sendCustomer: nobody past the shop's room
        # the Promoter adds +1 / +2 / +3 by level (Employees.promoterCrowd, 2026-11-07)
        crowd = self.B.promoter_crowd(self.staff["promoter"]) if "promoter" in self.staff else 0
        room = self.raw["shop"]["walkIns"] + crowd + sum(f"Parking{k}" in self.owned for k in (1, 2, 3))
        if self.inshop >= room:
            return "full"
        choices = [s for s in self.slots if s["sword"] is not None and not s["claimed"]]
        if not choices:  # runCustomer's browseFor (2026-10-31): nothing free, they wait BROWSE_WAIT inside and leave
            if self.sold == 0:  # not before the first sale (Allen 2026-10-29)
                return
            self.inshop += 1
            self.browsed += 1
            there = (self.street_in() + self.dist("EntryPoint", "shop")) / self.raw["shop"]["npcWalkSpeed"]
            # their room frees when they give up, not once out (sendCustomer's free())
            # ponytail: a sword freed during the wait isn't taken up; the game's browser would go for it
            self.push(there + self.raw["shop"]["browseWait"], "browsed")
            return
        vip = None
        if self.tutorial_done:
            vip = self.raw["gemUpgrades"]["levels"][self.gem_levels["Vip"]]["vipChance"] * (self.weather["value"] if self.weather_is("WeatherVip") else 1)
            if "VIP" in self.passes:  # the VIP pass: VIP customers twice as often (Store.VIP_CUSTOMERS, 2026-11-07)
                vip *= self.raw["store"].get("vipCustomers", 2)
            vip += self.stand_effects()["Vip"]  # VIP swords on the stands, after the multipliers (2026-11-09)
        cid = self.B.pick_customer(_Rng(r), vip)
        slot = choices[r.randint(0, len(choices) - 1)]
        for s in choices:
            if self.B.likes(cid, s["sword"]["bp"], s["sword"]["pct"]):
                slot = s
                break
        slot["claimed"] = True
        self.inshop += 1
        if "promoter" in self.staff:
            self.staff["promoter"] += 1
        street = self.dist("CustomerSpawn", "EntryPoint") if first else self.street_in()
        walk = (street + self.dist("EntryPoint", slot["holder"])) / self.raw["shop"]["npcWalkSpeed"]
        # ShopService (2026-11-05): a look over up to browseLooks other swords on sale, lookTime s each, then remarkTime s
        # reading theirs. ponytail: LOOK_WALK s between holders, not measured
        S = self.raw["shop"]
        looks = min(S.get("browseLooks", 0), sum(1 for s in self.slots if s["sword"] is not None) - 1)
        self.push(walk + max(0, looks) * (S.get("lookTime", 0) + LOOK_WALK) + S.get("remarkTime", 2.5), "offer", slot, cid, None, 0)

    def on_offer(self, slot, cid, offer, declines, passed=0):
        sw = slot["sword"]
        value = self.value(sw)
        if offer is None and self.sold >= 2 and not self.B.customers[cid].get("vip"):
            # ShopService.runCustomer (2026-11-10, More Sales): an offer at the buy chance (the level, + polish, + etch),
            # else they pass and try one other free sword (a 1.5 s beat, the walk, its read), then leave
            G = self.raw["gemUpgrades"]
            p = min(1, G["levels"][self.gem_levels["Sales"]]["buyChance"] + (G["buyPolished"] if sw["polished"] else 0)
                    + (G["buyEtched"] if sw["etch"] else 0))
            if self.rng["cust"].random() >= p:
                self.passed_on += 1
                other = [s for s in self.slots if s is not slot and s["sword"] is not None and not s["claimed"]] if passed == 0 else []
                if not other:
                    return self.leave(slot)
                slot["claimed"] = False
                nxt = other[self.rng["cust"].randint(0, len(other) - 1)]
                nxt["claimed"] = True
                return self.push(1.5 + LOOK_WALK + self.raw["shop"].get("remarkTime", 2.5), "offer", nxt, cid, None, 0, passed + 1)
        if offer is None:
            liked = self.sold > 0 and self.B.likes(cid, sw["bp"], sw["pct"])
            offer = value if self.sold == 0 else self.B.offer(cid, value, liked, _Rng(self.rng["cust"]))
        c = self.B.customers[cid]
        # ShopService.runCustomer (2026-11-09): with the Cashier your card still shows, for his answer time (his perk); a
        # card you don't answer by then is his: he sells by his setting (cashierSells, default any offer) into his till
        clerk = "cashier" in self.staff and self.sold >= 2
        timeout = self.B.perk("cashier", self.staff["cashier"]) if clerk else (c.get("waits") or self.raw["shop"]["offerTimeout"])
        # the tutorial points at the card ("Accept the offer!"): nobody misses it, and each type answers at its own
        # pace (Archetype.react), not the measured habits, which came from feature tests with nobody watching the shop
        tutorial = not self.tutorial_done
        react = self.A.react if tutorial else self.offer_react
        delay = None if self.rng["cust"].random() < (0.0 if tutorial else self.offer_miss) else self.rng["cust"].expovariate(1 / react)
        if clerk and (delay is None or delay >= timeout):
            return self.push(timeout, "answer", slot, cid, offer, declines, self.B.cashier_sells(offer, value, None), value, True)
        if delay is None:  # missed: they leave when the card times out
            return self.push(timeout, "answer", slot, cid, offer, declines, None, value, False)
        # an answer comes before the card times out (a later one is a miss, counted above)
        accept = not (self.A.haggle and declines == 0 and offer < 1.1 * value and c["raiseChance"] >= 0.3 and self.sold >= 2)
        self.push(min(delay, timeout - 0.5), "answer", slot, cid, offer, declines, accept, value, False)

    def on_answer(self, slot, cid, offer, declines, accept, value, cashier=False):
        if accept is None:  # no answer in time: they leave
            self.missed += 1
            return self.leave(slot)
        if accept:
            if cashier:
                c = offer * self.coin_boost()
                self.till += c
                self.earned += c
                self.note_income(c)
                self.staff["cashier"] += 1
            else:
                self.earn(offer)
            self.sold += 1
            self.reputation += self.raw["reputation"]["sale"]
            self.loop_done(slot["sword"])
            if self.sold == 1:
                self.mark("FirstSale")
                self.push(self.raw["shop"].get("firstLetterDelay", 3), "letter", "IronTanto")  # ShopService FIRST_LETTER_DELAY
            if self.sold >= 3:  # Commissions.due after every sale (ShopService.offerCommission)
                self.maybe_katana_letter()
            slot["sword"] = None
            slot["claimed"] = False
            self.room_freed()
            return
        declines += 1
        teach = self.sold == 1 and declines == 1
        raised = None if self.sold == 0 else self.B.raise_offer(cid, offer, declines, _Rng(self.rng["cust"]), teach)
        if raised is None:
            self.lost += 1
            return self.leave(slot)
        self.push(1.0, "offer", slot, cid, raised, declines)

    def placed(self, sw):
        sw.setdefault("t", {})["placed"] = self.t
        return sw

    def loop_done(self, sw):
        """A sold sword's loop: yours from the ore you collected, the crew's from the ingot it fetched off the rack."""
        t = sw.get("t", {})
        if "ore" in t and "placed" in t:
            self.loops_own.append((self.t - t["ore"], t["forged"] - t["ore"], t["placed"] - t["forged"], self.t - t["placed"]))
        elif "fetched" in t and "placed" in t:
            self.loops_crew.append((self.t - t["fetched"], t["forged"] - t["fetched"], t["placed"] - t["forged"], self.t - t["placed"]))

    def leave(self, slot):
        slot["claimed"] = False
        self.room_freed()

    def on_browsed(self):
        self.room_freed()

    def room_freed(self):
        """sendCustomer's free(): one shopper fewer; a walk-in that came due while full is sent on the spawn loop's next
        1 s check (ShopService, 2026-11-10)."""
        self.inshop -= 1
        if self.due:
            self.due = False
            self.push(1.0, "spawn")

    def on_letter(self, name):
        if name not in self.letters_done:
            self.letter = (name, self.t)

    def maybe_katana_letter(self):
        gate = next((c.get("afterUpgrade") for c in self.raw["commissions"] if c["id"] == "Katana"), None)
        if (self.sold >= 3 and "IronTanto" in self.letters_done and "Katana" not in self.letters_offered and self.letter is None
                and (gate is None or gate in self.owned)):  # Commissions.due: after the Machete (2026-10-31)
            self.letters_offered.add("Katana")
            self.push(self.raw["shop"]["letterDelay"], "letter", "Katana")

    # --- the crew (EmployeeService) ------------------------------------------------------------------------------
    def crew_waits(self, anvil, why, secs=3.0):
        self.crew_wait[why] = self.crew_wait.get(why, 0.0) + secs
        self.push(secs, "crafter", anvil, "start")

    def on_crafter(self, anvil, phase, job=None):
        cid = self.equipped.get(anvil)
        if cid is None:
            self.crafter_busy[anvil] = False
            return
        lv = self.B.staff_level(self.hired[cid])[0]
        walk = self.B.crafter_walk(cid, lv)  # grows with level (2026-11-03)
        if phase == "start":
            making = self.best_bp()
            if not making or making == "tanto" and "SwordRack" not in self.owned:
                return self.crew_waits(anvil, "noShape")
            if "SwordRack" not in self.owned:
                return self.crew_waits(anvil, "noRack")
            if self.hooks(self.sword_rack) >= self.sword_cap():
                return self.crew_waits(anvil, "rackFull")
            if not self.ingot_rack:
                return self.crew_waits(anvil, "noIngots")
            # as many of the cheapest as it carries at its level (Employees.crafterCarry: 1 at Lv. 1-2 since 2026-11-05), no more than the Finished
            # Sword Rack has room for (EmployeeService). ponytail: one hook per crafter sword (crafters make no big swords)
            metals = []
            for _ in range(min(self.B.crafter_carry(lv), self.sword_cap() - self.hooks(self.sword_rack), len(self.ingot_rack))):
                m = min(self.ingot_rack, key=self.B.metal_multiplier)
                self.ingot_rack.remove(m)
                metals.append(m)
            secs = self.dist(anvil, "IngotRack") / walk
            return self.push(secs, "crafter", anvil, "furnace", {"metals": metals, "bp": making, "fetched": self.t})
        if phase == "furnace":
            # not one you used in the last YOURS s (EmployeeService, 2026-11-02, Allen: "Only when it's idle")
            idle = [f for f in self.furnaces_owned() if self.t - self.used_at.get(f, -1e9) >= YOURS]
            free = [f for f in idle if self.furnaces[f] is None]
            if not free:
                for f in idle:  # a forgotten ingot of yours comes out into your hands
                    x = self.furnaces[f]
                    if x["who"] == "p" and x["ready"] + 10 <= self.t:
                        self.hot.append((x["metal"], x.get("ore", self.t)))
                        self.furnaces[f] = None
                        free = [f]
                        break
            if not free:
                self.crew_wait["furnace"] = self.crew_wait.get("furnace", 0.0) + 2.0
                return self.push(2.0, "crafter", anvil, "furnace", job)
            # each ingot into the next free furnace, so free furnaces heat together (2026-11-04); in rounds when fewer.
            # ponytail: the walk between furnaces and a furnace freeing up mid-trip are left out
            use = free[:len(job["metals"])]
            rounds = -(-len(job["metals"]) // len(use))
            heat = max(self.B.heat_time(self.owned, f) for f in use) * rounds
            for f in use:
                self.furnaces[f] = {"who": cid, "metal": job["metals"][0], "ready": self.t + heat}
            job["forges"] = use
            return self.push(self.dist("IngotRack", use[0]) / walk + heat, "crafter", anvil, "forge", job)
        if phase == "forge":
            for f in job["forges"]:
                self.furnaces[f] = None
            secs = self.dist(job["forges"][0], anvil) / walk + self.B.level_seconds(lv, self.B.crafters[cid]["forge"]) * len(job["metals"])
            return self.push(secs, "crafter", anvil, "polish", job)
        if phase == "polish":
            secs = 0.0
            # either Polishing Station since 2026-11-04. ponytail: the sim never modelled waiting for a station, so Station 2
            # changes nothing here; distances stay Station 1's
            job["polished"] = "PolishStation" in self.owned
            if job["polished"]:
                secs = self.dist(anvil, "PolishStation") / walk + self.B.level_seconds(lv, self.B.crafters[cid]["polish"]) * len(job["metals"])  # each crafter's own (2026-11-04)
            return self.push(secs + self.dist("PolishStation" if job["polished"] else anvil, "SwordRack") / walk, "crafter", anvil, "rack", job)
        if phase == "rack":
            while job["metals"]:  # racked one by one; a full rack holds the rest in hand
                sw = self.make_sword(job["bp"], job["metals"][0], self.B.crafter_quality(cid, lv), job["polished"])
                sw["t"] = {"fetched": job["fetched"], "forged": self.t}
                if self.hooks(self.sword_rack) + self.hooks([sw]) > self.sword_cap():
                    self.crew_wait["rackFull"] = self.crew_wait.get("rackFull", 0.0) + 3.0
                    return self.push(3.0, "crafter", anvil, "rack", job)
                self.sword_rack.append(sw)
                job["metals"].pop(0)
                self.hired[cid] += 1
                self.crew_made += 1
            return self.push(self.dist("SwordRack", anvil) / walk, "crafter", anvil, "start")

    def on_stocker(self):
        if "Stocker" not in self.owned:
            return
        speed = self.B.staff_walk("stocker", self.staff["stocker"])
        free = [x for x in self.slots if x["sword"] is None and not x["claimed"]]
        room = self.B.carry(self.B.staff_level(self.staff["stocker"], self.raw["employees"]["staffScale"])[0])
        loads = []  # as many swords a trip as he carries at his level (2026-11-04), each to a free holder it fits
        # etched swords first, then any (2026-11-05, Allen: "have stocker prioritize etched swords, but if there's none
        # then just grab a sword"); he no longer leaves un-etched ones for the Etcher
        held = self.held()  # kept for an accepted letter: the mail sends it (Orders.held, 2026-11-09, P1)
        for sw in sorted(self.sword_rack, key=lambda s: s["etch"] is None) if free else ():
            if len(loads) >= room:
                break
            if any(sw is h for h in held):
                continue
            sl = next((x for x in free if self.fits(sw, x) and not x["claimed"]), None)
            if sl:
                _drop(self.sword_rack, sw)
                sl["claimed"] = True
                loads.append((sl, sw))
        if not loads:
            return self.push(3.0, "stocker")
        # ponytail: holder to holder taken as the farther one's way from the rack, each placed on the way there
        far = max(self.dist("SwordRack", sl["holder"]) for sl, _ in loads) / speed
        for k, (sl, sw) in enumerate(loads, 1):
            self.staff["stocker"] += 1
            self.push(self.dist("SwordRack", sl["holder"]) / speed + self.T["place"] * k, "stocked", sl, sw)
        return self.push(2 * far + self.T["place"] * len(loads), "stocker")

    def on_stocked(self, sl, sw):
        sl["sword"], sl["claimed"] = self.placed(sw), False

    def on_etcher(self):
        if "Etcher" not in self.owned:
            return
        sw = next((s for s in self.sword_rack if s["etch"] is None), None)
        if not sw or self.B.best_etch(self.owned) is None:  # no pattern bought: he waits (2026-11-01)
            return self.push(3.0, "etcher")
        self.sword_rack.remove(sw)
        secs = 2 * self.dist("SwordRack", "EtchingTable2") / self.raw["employees"]["staff"]["etcher"]["walk"] + self.B.perk("etcher", self.staff["etcher"])
        self.push(secs, "etched", sw)

    def on_etched(self, sw):
        sw["etch"] = self.B.best_etch(self.owned)  # your best (EmployeeService: Etches.chosen)
        self.staff["etcher"] += 1
        if self.hooks(self.sword_rack) + self.hooks([sw]) <= self.sword_cap():
            self.sword_rack.append(sw)
        else:
            self.swords.append(sw)  # ponytail: the real Etcher waits for room; handing it over is close enough
        self.push(0.5, "etcher")

    def on_sample(self):
        self.minutes.append((self.earned, self.coins, self.spent, self.own_made, self.crew_made))
        self.push(60, "sample")

    # ---------------------------------------------------------------- run
    def run(self):
        self.on_weather()
        self.push(5, "spawn")
        self.push(0, "sample")
        if "AutoRoller" in self.passes:
            self.push(1, "autoroll")
        if "StarterPack" in self.passes:
            self.add_gems(self.raw["store"]["starterGems"], "starter")
            self.coins += self.raw["store"].get("starterCoins", 10000)  # coins, not a Gold ingot, since 2026-10-29
        self.on_day()
        self.decide()
        handlers = {"player": self.on_player, "spawn": self.on_spawn, "offer": self.on_offer, "answer": self.on_answer,
                    "letter": self.on_letter, "day": self.on_day, "mail": self.on_mail, "cart_offer": self.on_cart_offer, "crafter": self.on_crafter,
                    "stocker": self.on_stocker, "stocked": self.on_stocked, "etcher": self.on_etcher, "etched": self.on_etched,
                    "weather": self.on_weather, "autoroll": self.on_autoroll, "sample": self.on_sample,
                    "browsed": self.on_browsed, "musashi": self.on_musashi}
        still = 0  # events in a row at one instant: a loop that takes no time would never end
        start, n = time.monotonic(), 0
        while self.q:
            n += 1
            if self.wall_limit and n % 20000 == 0 and time.monotonic() - start > self.wall_limit:
                raise RuntimeError(f"over {self.wall_limit} s of computer time at {self.t / 3600:.1f} h of play "
                                   f"({len(self.swords)} swords in hand, {len(self.q)} events queued)")
            t, _, kind, data = heapq.heappop(self.q)
            if t > self.horizon or self.done:
                break
            still = still + 1 if t == self.t else 0
            if still > 20000:
                raise RuntimeError(f"no time passes at {t:.0f} s (last event: {kind}, {getattr(data[0], '__qualname__', '') if data else ''})")
            self.t = t
            handlers[kind](*data)
        return self.result()

    def gem_milestones(self):
        """The gem shop targets (minutes, once reached): every upgrade at Lv. 1, this type's pair at Lv. 3 (the cheapest
        buyer's first pair to get there), and any pair at Lv. 5."""
        M = self.milestones

        def both(ids):
            return max(M[i] for i in ids) if all(i in M for i in ids) else None
        pairs = list(behavior.GEM_GROUPS.values())
        mine = [behavior.GEM_GROUPS[self.A.gems]] if self.A.gems in behavior.GEM_GROUPS else pairs
        found = {"GemsAllLv1": both([f"{g}1" for g in self.gem_levels]),
                 "GemPairLv3": min((x for x in (both([f"{g}3" for g in p]) for p in mine) if x is not None), default=None),
                 "GemPairLv5": min((x for x in (both([f"{g}5" for g in p]) for p in pairs) if x is not None), default=None)}
        return {k: v for k, v in found.items() if v is not None}

    def result(self):
        exp = self.luck_exp or 1
        return {"milestones": dict(self.milestones, **self.gem_milestones()), "minutes": self.minutes, "purchases": self.purchases, "use": self.use,
                "crew_wait": self.crew_wait, "progress": self.progress, "luck": self.luck_got / exp, "ores": self.ores_seen,
                "sold": self.sold, "carted": self.carted, "missed": self.missed, "lost": self.lost, "browsed": self.browsed, "passed_on": self.passed_on, "letters": self.letters,
                "own_made": self.own_made, "crew_made": self.crew_made, "earned": self.earned, "away_coins": self.away_coins, "coins": self.coins,
                "merges": self.merges, "horizon_min": (self.t if self.done else self.horizon) / 60, "loops_own": self.loops_own, "loops_crew": self.loops_crew,
                "first_pull": self.first_pull, "gems_in": self.gems_in, "gems_out": self.gems_out, "gem_levels": self.gem_levels,
                "mail_done": self.mail_done, "mail_coins": self.mail_coins, "cart_bulk": self.cart_bulk,
                "cart_special": self.cart_special, "cart_skips": self.cart_skips, "reputation": self.reputation,
                "orders_open": len(self.orders), "days": self.day, "gems_left": self.gems, "quests": self.quest_times,
                "musashi": {"designs": self.mu_designs, "deals": self.mu_deal_buys, "saved": round(self.mu_saved),
                            "gems_saved": self.mu_gems_saved}}


class _Rng:
    """random.Random with rules.py's next_number / next_integer."""
    def __init__(self, r):
        self.r = r

    def next_number(self):
        return self.r.random()

    def next_integer(self, a, b):
        return self.r.randint(a, b)


def simulate(B, arche_name, payer, seed, hours, timing=None, arche=None, wall_limit=None, until_done=False):
    sim = Sim(B, arche or behavior.ARCHETYPES[arche_name], payer, seed, hours, timing=timing)
    sim.wall_limit, sim.until_done = wall_limit, until_done
    return sim.run()

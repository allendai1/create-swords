"""Engine sanity checks (no game rules here: test_parity.py has those). python -m unittest test_engine"""

import unittest

import engine
import rules

B = rules.load()


class Engine(unittest.TestCase):
    def test_same_seed_same_player(self):
        a = engine.simulate(B, "casual", "free", "t:1", 1)
        b = engine.simulate(B, "casual", "free", "t:1", 1)
        self.assertEqual(a["milestones"], b["milestones"])
        self.assertEqual(a["earned"], b["earned"])

    def test_time_adds_up(self):
        """The player does one thing at a time: its tasks fill the horizon (the last may run past it)."""
        for arche in ("casual", "efficient", "manager", "grinder", "automator", "rusher"):
            for payer in ("free", "allpasses"):
                r = engine.simulate(B, arche, payer, "t:2", 2)
                used = sum(r["use"].values())
                self.assertGreaterEqual(used, 2 * 3600 - 1, (arche, payer))
                self.assertLess(used, 2 * 3600 + 600, (arche, payer))

    def test_money_and_shop_stay_sane(self):
        sim = engine.Sim(B, engine.behavior.ARCHETYPES["efficient"], "free", "t:3", 3)
        r = sim.run()
        self.assertGreaterEqual(sim.coins, 0)
        self.assertGreaterEqual(sim.inshop, 0)
        self.assertLessEqual(r["sold"], r["own_made"] + r["crew_made"])
        for minute, uid, price in r["purchases"]:
            self.assertGreaterEqual(price, 0, uid)

    def test_gems_add_up(self):
        """Every gem in is spent or still held; days, mail and the cart run."""
        for arche in ("grinder", "manager"):
            r = engine.simulate(B, arche, "free", "t:4", 6)
            self.assertEqual(sum(r["gems_in"].values()) - sum(r["gems_out"].values()), r["gems_left"], arche)
            self.assertGreaterEqual(r["gems_left"], 0)
            self.assertEqual(r["days"], 6)
            self.assertGreater(r["mail_done"], 0, arche)
        self.assertGreater(r["cart_bulk"] + r["cart_special"], 0)


    def test_begun_chains_stand_past_the_cap(self):
        """Upgrades.CHAINS (2026-10-31): a begun chain's next level is on offer whatever the pad cap; new chains are capped."""
        sim = engine.Sim(B, engine.behavior.ARCHETYPES["efficient"], "free", "t:5", 1)
        sim.owned |= {"Heat1", "OreStand2", "OreStand3", "OreStand4", "OreStand5", "WallRack2", "DisplayTable1", "WallRack5", "SwordRack"}
        sim.bought_n += 1
        ids = {o[0] for o in sim.offers()}
        # Display Table 2 before the Upgraded Store since 2026-11-02 (the store waits for it)
        self.assertTrue({"Heat2", "OreStand6", "DisplayTable2", "SwordRack2"} <= ids and "UpgradedStore" not in ids, ids)
        capped = [i for i in ids if i in B.upgrades and not B.upgrades[i].get("blueprint") and i not in B.raw["padAlways"]
                  and B.chain_of.get(i) not in {B.chain_of.get(o) for o in sim.owned}]
        self.assertLessEqual(len(capped), B.raw["padCap"], capped)


    def test_what_a_begun_chain_waits_for_stands(self):
        """TycoonService.standing (2026-11-05): Furnace 3 waits for Furnace 2 too, so once the crafters' chain has begun
        Furnace 2 stands past the cap; Etching Table 2 comes in the etch line after Lightning (Fracture until 2026-11-10)."""
        self.assertEqual(sorted(B.upgrades["Furnace3"]["after"]), ["Anvil3", "Furnace2"])
        self.assertEqual(B.upgrades["EtchingTable2"]["after"], ["EtchLightning"])
        sim = engine.Sim(B, engine.behavior.ARCHETYPES["efficient"], "free", "t:5", 1)
        sim.owned |= {"IngotRack", "SwordRack", "Crafter", "Anvil2", "Anvil3", "OreStand2", "WallRack2", "Heat1"}
        sim.bought_n += 1
        ids = {o[0] for o in sim.offers()}
        self.assertIn("Furnace2", ids)
        self.assertNotIn("Furnace3", ids)
        # before Anvil 3, Furnace 3 isn't the chain's next level, so Furnace 2 is only one more pad under the cap
        early = engine.Sim(B, engine.behavior.ARCHETYPES["efficient"], "free", "t:5", 1)
        early.owned |= {"IngotRack", "SwordRack", "Crafter", "Anvil2"}
        early.raw = dict(early.raw, padCap=1)  # one new chain only: Ore Slot 2 (80) is the cheapest
        early.bought_n += 1
        self.assertNotIn("Furnace2", {o[0] for o in early.offers()})

    def test_stocker_takes_etched_first_then_any(self):
        """EmployeeService.stockOne (2026-11-05): etched swords first; with none, a bare one (no longer left for the Etcher)."""
        sim = engine.Sim(B, engine.behavior.ARCHETYPES["efficient"], "free", "t:5", 1)
        etch = next(i for i in B.upgrades if i.startswith("Etch") and i not in ("EtchingTable", "EtchingTable2"))
        sim.owned |= {"SwordRack", "Stocker", "Etcher", "EtchingTable", etch}
        self.assertIsNotNone(B.best_etch(sim.owned))
        bp = next(k for k, v in B.blueprints.items() if not v["big"])
        bare, etched = sim.make_sword(bp, "Iron", 1.0), sim.make_sword(bp, "Iron", 1.0)
        etched["etch"] = B.best_etch(sim.owned)
        sim.slots = [{"holder": "WallRack1", "big": False, "sword": None, "claimed": False}]
        sim.sword_rack = [bare, etched]
        sim.staff.setdefault("stocker", 0)
        sim.on_stocker()
        self.assertEqual(sim.sword_rack, [bare])  # the etched one went
        sim.slots.append({"holder": "WallRack1", "big": False, "sword": None, "claimed": False})
        sim.on_stocker()
        self.assertEqual(sim.sword_rack, [])  # no etched left: he takes the bare one

    def test_stocker_leaves_a_letters_sword_and_the_mail_sends_it(self):
        """Orders.held (2026-11-09, P1): one rack sword per accepted (chased) order nothing in hand fits stays for the
        mail, which sends it from the rack (ShopService.takeLetterSword); the rest are stocked."""
        sim = engine.Sim(B, engine.behavior.ARCHETYPES["efficient"], "free", "t:5", 1)
        sim.owned |= {"SwordRack", "Stocker"}
        bp = next(k for k, v in B.blueprints.items() if not v["big"])
        a, b, c = sim.make_sword(bp, "Gold", 1.0), sim.make_sword(bp, "Gold", 1.0), sim.make_sword(bp, "Iron", 1.0)
        order = {"blueprintId": bp, "materialId": "Gold", "gems": 2, "chase": True}
        sim.orders, sim.swords = [order], []
        sim.sword_rack = [a, b, c]
        self.assertEqual(len(sim.held()), 1)
        self.assertIs(sim.held()[0], a)
        sim.slots = [{"holder": "WallRack1", "big": False, "sword": None, "claimed": False} for _ in range(3)]
        sim.staff.setdefault("stocker", 0)
        sim.on_stocker()
        self.assertEqual(len(sim.sword_rack), 1)
        self.assertIs(sim.sword_rack[0], a)  # kept for the letter
        order["chase"] = False
        self.assertEqual(sim.held(), [])  # not accepted: nothing kept
        fit = sim.mail_fit()
        self.assertIsNotNone(fit)
        self.assertIs(fit[0], a)  # the mail still sends it from the rack
        sim.task_mail(*fit)
        self.assertEqual(sim.sword_rack, [])
        self.assertEqual(sim.orders, [])

    def test_cashier_and_promoter_work(self):
        """Staff are stored lowercase: the Cashier answers at the till (its sale counted as earned at once) and the
        Promoter widens the shop's room (2026-11-10 audit: both were no-ops since the sim began)."""
        sim = engine.Sim(B, engine.behavior.ARCHETYPES["efficient"], "free", "t:5", 1)
        sim.buy("Cashier", 0)
        sim.buy("Promoter", 0)
        bp = next(k for k, v in B.blueprints.items() if not v["big"])
        slot = {"holder": "WallRack1", "big": False, "sword": sim.make_sword(bp, "Iron", 1.0), "claimed": True}
        sim.sold, pushed = 2, []
        sim.push = lambda dt, kind, *a: pushed.append((dt, kind, a))
        cid = next(iter(B.customers))
        sim.tutorial_done = True
        sim.offer_miss, sim.offer_react = 0.0, 0.01  # watching: you answer first, the sale is yours (ShopService, 2026-11-09)
        sim.on_offer(slot, cid, 100.0, 0)
        self.assertFalse(pushed[-1][2][-1])
        sim.offer_miss = 1.0  # not watching: the Cashier answers at his perk time, into his till
        sim.on_offer(slot, cid, 100.0, 0)
        dt, kind, args = pushed[-1]
        self.assertEqual(kind, "answer")
        self.assertTrue(args[-1])
        self.assertAlmostEqual(dt, B.perk("cashier", sim.staff["cashier"]))
        earned = sim.earned
        sim.on_answer(*args[:4], True, *args[5:])  # accepted
        self.assertGreater(sim.till, 0)
        self.assertAlmostEqual(sim.earned - earned, sim.till)
        sim.slots = [{"holder": "WallRack1", "big": False, "sword": sim.make_sword(bp, "Iron", 1.0), "claimed": False}]
        sim.inshop = B.raw["shop"]["walkIns"]  # full without a Promoter
        sim.send_customer()
        self.assertEqual(sim.inshop, B.raw["shop"]["walkIns"] + 1)

    def test_cashier_earns_while_away(self):
        """SmithyCore.takeAway (2026-11-11): 20% of the last 15 minutes' coins a minute, for Aki's 2 h, into his till;
        nothing without a Cashier; a short next day blends in the rate the last one ended with."""
        sim = engine.Sim(B, engine.behavior.ARCHETYPES["efficient"], "free", "t:5", 1)
        sim.t = 3600.0
        sim.note_income(3000.0)  # 3,000 in the window: 200 a minute
        sim.settle_away()
        self.assertEqual(sim.away_coins, 0)  # no Cashier
        sim.staff["cashier"] = 0
        sim.note_income(0.0)
        sim.settle_away()
        self.assertEqual(sim.away_coins, 200 * 0.2 * 120)  # 4,800
        self.assertEqual(sim.till, 4800)
        sim.income_log, sim.day_start, sim.t = [], 3600.0, 3600.0 + 300  # 5 minutes into a new day, nothing earned
        self.assertAlmostEqual(sim.income_rate(), 200 * 10 / 15)

    def test_tending_keeps_an_orders_ingot(self):
        """A Manager racking ingots for the crew skips one kept for a mail order (as sitting_back does)."""
        sim = engine.Sim(B, engine.behavior.ARCHETYPES["manager"], "free", "t:5", 1)
        sim.equipped = {"Anvil2": "x"}
        sim.owned |= {"IngotRack"}
        sim.slots = []
        sim.orders = [{"blueprintId": "katana", "materialId": "Silver", "gems": 2, "have": "ingot"}]
        sim.cold = [("Silver", 0.0)]
        sim.tend_tasks()
        self.assertEqual(sim.cold, [("Silver", 0.0)])
        self.assertEqual(sim.cold_rack, [])

    def test_crafter_polishes_each_sword(self):
        """EmployeeService: a crafter carrying two ingots polishes two swords, as it forges two."""
        sim = engine.Sim(B, engine.behavior.ARCHETYPES["manager"], "free", "t:5", 1)
        sim.buy("Crafter", 0)
        sim.owned |= {"PolishStation"}
        anvil, cid = next(iter(sim.equipped.items()))
        secs = {}
        for n in (1, 2):
            pushed = []
            sim.push = lambda dt, kind, *a: pushed.append(dt)
            sim.on_crafter(anvil, "polish", {"metals": ["Iron"] * n, "bp": "tanto"})
            secs[n] = pushed[-1]
        one = B.level_seconds(B.staff_level(sim.hired[cid])[0], B.crafters[cid]["polish"])
        self.assertAlmostEqual(secs[2] - secs[1], one)

    def test_same_seed_any_hash_seed(self):
        """Results don't depend on Python's string hashing (set order): equal-priced blueprints once split runs."""
        import os, subprocess, sys
        code = "import engine, rules; print(round(engine.simulate(rules.load(), 'manager', 'free', 'snap:3', 12)['earned']))"
        runs = {subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env={**os.environ, "PYTHONHASHSEED": h},
                               cwd=os.path.dirname(os.path.abspath(engine.__file__))).stdout for h in ("1", "2")}
        self.assertEqual(len(runs), 1, runs)

    def test_showcase_families(self):
        """Shared/Showcase families (2026-11-09): a stand sword's metal picks its stat, its points (pull x100) how much;
        each family's points add up, capped; Mail gives the gem chance too. The same cases as the Studio spec."""
        sim = engine.Sim(B, engine.behavior.ARCHETYPES["efficient"], "free", "t:5", 1)
        self.assertEqual(sim.stand_effects()["Customers"], 0)  # no stand
        sim.owned |= {"Showcase1", "Showcase2"}
        sim.stand_swords = lambda: [("Iron", "katana", True, True), ("Gold", "katana", True, True)]
        sim._stand_key = None
        eff = sim.stand_effects()
        self.assertAlmostEqual(eff["Customers"], 0.06)
        self.assertAlmostEqual(eff["Coins"], 0.04)  # Gold Rare since 2026-11-10: 4 + 2 + 1 + 1 points x 0.005
        self.assertEqual(eff["Vip"], 0)
        sim.stand_swords = lambda: [("Doppler", "seraph", True, True)] * 3
        sim._stand_key = None
        self.assertAlmostEqual(sim.stand_effects()["Luck"], 0.15)  # capped
        sim.stand_swords = lambda: [("Starmetal", "katana", True, True)]
        sim._stand_key = None
        eff = sim.stand_effects()
        self.assertGreater(eff["Mail"], 0)
        self.assertAlmostEqual(eff["Gems"], eff["Mail"])
        self.assertEqual(len(B.raw["shop"]["showcase"]["family"]), len(B.metals))


class Tutorial(unittest.TestCase):
    """The game's tutorial rules (2026-10-31, the first-10-minutes review's four disagreements and the day's fixes)."""

    def sim(self, seed="t:6"):
        return engine.Sim(B, engine.behavior.ARCHETYPES["casual"], "free", seed, 1)

    def test_first_pulls_common_then_uncommon(self):
        for k in range(20):
            s = self.sim(f"t:6:{k}")
            got = [B.metals[s.roll_ore(1.0)]["rarity"] for _ in range(2)]
            self.assertEqual(got, ["Common", "Uncommon"])

    def test_letter_iron_by_the_second_pull(self):
        for k in range(20):
            s = self.sim(f"t:7:{k}")
            s.discovered.add("Copper")  # past the first pulls
            s.letter = ("IronTanto", 0.0)
            self.assertIn("Iron", [s.roll_ore(1.0) for _ in range(2)])

    def test_no_sword_pads_and_one_guided_buy_before_the_letter(self):
        s = self.sim()
        s.coins = 1000.0
        self.assertFalse(any(B.upgrades[i].get("blueprint") for i, _ in s.offers() if i in B.upgrades))
        self.assertEqual(s.pick_target()[0], "PolishStation")
        s.tutorial_done = True
        s.bought_n += 1  # the pad list is cached per purchase count
        self.assertIn("WakizashiBlueprint", {i for i, _ in s.offers()})

    def test_tutorial_heats_and_the_katana_wait(self):
        s = self.sim()
        s.own_made = 2
        self.assertEqual(s.heat_time("Forge"), s.first_heat)
        s.tutorial_done = True
        self.assertGreater(s.heat_time("Forge"), s.first_heat)
        s.letters_done.add("IronTanto")
        s.sold = 3
        s.maybe_katana_letter()
        self.assertNotIn("Katana", s.letters_offered)  # the Wakizashi isn't bought (the Machete until 2026-11-11)
        s.owned.add("WakizashiBlueprint")
        s.maybe_katana_letter()
        self.assertIn("Katana", s.letters_offered)

class Browse(unittest.TestCase):
    def test_browser_holds_room_for_walk_in_plus_browse_wait(self):
        """ShopService.browseFor (2026-10-31): nothing free, they hold a place for the walk in + BROWSE_WAIT, not the walk out."""
        s = engine.Sim(B, engine.behavior.ARCHETYPES["efficient"], "free", "t:6", 1)
        s.sold, s.q = 1, []
        for slot in s.slots:
            slot["sword"] = None
        s.on_spawn()
        self.assertEqual(s.inshop, 1)
        there = (s.street_in() + s.dist("EntryPoint", "shop")) / s.raw["shop"]["npcWalkSpeed"]
        t = next(t for t, _, kind, _ in s.q if kind == "browsed")
        self.assertAlmostEqual(t - s.t, there + s.raw["shop"]["browseWait"])


class SensibleBuys(unittest.TestCase):
    def test_every_type_takes_stations_and_cheap_pads(self):
        import behavior
        B = rules.load()
        for name, A in behavior.ARCHETYPES.items():
            self.assertEqual(behavior.choose_target(A, B, [("KatanaBlueprint", 1300), ("PolishStation", 100)], lambda i: 100, 10, set())[0],
                             "PolishStation", name)
            self.assertEqual(behavior.choose_target(A, B, [("JianBlueprint", 80000), ("SwordRack2", 1300)], lambda i: 300, 100, set())[0],
                             "SwordRack2", name)


if __name__ == "__main__":
    unittest.main()

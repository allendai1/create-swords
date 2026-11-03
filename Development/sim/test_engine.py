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
        for minute, uid, price, _ in r["purchases"]:
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
        self.assertNotIn("Katana", s.letters_offered)  # the Machete isn't bought
        s.owned.add("MacheteBlueprint")
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
        there = (s.dist("CustomerSpawn", "EntryPoint") + s.dist("EntryPoint", "shop")) / s.raw["shop"]["npcWalkSpeed"]
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

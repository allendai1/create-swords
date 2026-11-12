"""Musashi's stall (rules.py musashi_*, 2026-11-10): stock, floor and deal invariants; the engine buys from it.
python -m unittest test_musashi"""

import random
import unittest

import engine
import rules

B = rules.load()
M = B.raw["musashi"]


class R:
    def __init__(self, seed):
        self.r = random.Random(seed)

    def next_number(self):
        return self.r.random()

    def next_integer(self, a, b):
        return self.r.randint(a, b)


ALL_PINNED = {d["pinned"] for d in M["designs"]}


class Stock(unittest.TestCase):
    def test_open_needs_only_the_crafter(self):  # 2026-11-10: the Katana gate was dropped (Allen: "i cant trade")
        self.assertTrue(B.musashi_open({"Crafter"}, {"tanto"}))
        self.assertFalse(B.musashi_open(set(), {"katana"}))
        self.assertTrue(B.musashi_open({"Crafter"}, {"katana"}))

    def test_stock_qualifies_and_fits(self):
        rng = R(1)
        for k in range(500):
            known = {"tanto"} | set(random.Random(k).sample(sorted(ALL_PINNED), 4)) | {"musashi1"}
            stock = B.musashi_stock(rng, known, {})
            self.assertLessEqual(len(stock), M["slots"])
            self.assertEqual(len(stock), len(set(stock)))
            for d in stock:
                self.assertIn(B.designs[d]["pinned"], known)
                self.assertNotIn(d, known)

    def test_floor_forces_a_missed_design(self):
        """A Legendary missed floor-1 stocks is in the next one; seen clears it and counts the others."""
        known = ALL_PINNED | {"tanto"}
        missed = {"musashi10": M["floor"] - 1}
        for seed in range(50):
            self.assertIn("musashi10", B.musashi_stock(R(seed), known, missed))
        stock = ["musashi10", "musashi1", "musashi2"]
        B.musashi_seen(stock, known, missed)
        self.assertNotIn("musashi10", missed)
        self.assertEqual(missed["musashi3"], 1)
        self.assertNotIn("musashi1", missed)

    def test_no_design_waits_past_the_floor(self):
        known, missed, rng = ALL_PINNED | {"tanto"}, {}, R(3)
        for _ in range(400):
            B.musashi_seen(B.musashi_stock(rng, known, missed), known, missed)
            self.assertTrue(all(v < M["floor"] + 3 for v in missed.values()), missed)  # 10 designs, 3 slots: a queue

    def test_deals(self):
        standing = ["MergeSlots", "Anvil2", "Showcase2", "IngotRack", "SwordRack", "KatanaBlueprint"]
        pcts = {p for p, _ in M["discounts"]}
        for seed in range(200):
            deals = B.musashi_deals(R(seed), standing)
            self.assertEqual(len(deals), M["deals"])
            self.assertEqual(len({i for i, _ in deals}), len(deals))
            for i, pct in deals:
                self.assertNotIn(i, ("MergeSlots", "Anvil2"))  # the merge, and a free pad
                self.assertIn(pct, pcts)
        self.assertEqual(B.musashi_deals(R(0), ["MergeSlots"]), [])


class Engine(unittest.TestCase):
    @unittest.skipUnless(B.raw["musashi"].get("enabled"), "Musashi is off in this export (Shared/Musashi.ENABLED, off for launch)")
    def test_players_buy_designs_and_mail_never_asks(self):
        sim = engine.Sim(B, engine.behavior.ARCHETYPES["efficient"], "free", "t:mu", 6)
        r = sim.run()
        self.assertTrue(r["musashi"]["designs"], "no design bought in 6 h")
        self.assertTrue(all(not B.blueprints[o["blueprintId"]].get("shop") for o in sim.orders))
        self.assertGreaterEqual(sim.coins, 0)

    def test_off_without_the_export(self):
        import scenarios
        Boff, _ = scenarios.build("no-musashi", B.raw)
        r = engine.simulate(Boff, "efficient", "free", "t:mu", 3)
        self.assertEqual(r["musashi"], {"designs": [], "deals": 0, "saved": 0, "gems_saved": 0})

    def test_off_when_disabled_in_the_game(self):
        import copy
        raw = copy.deepcopy(B.raw)
        raw["musashi"]["enabled"] = False
        r = engine.simulate(rules.Balance(raw), "efficient", "free", "t:mu", 3)
        self.assertEqual(r["musashi"]["designs"], [])
        self.assertEqual(r["musashi"]["deals"], 0)


if __name__ == "__main__":
    unittest.main()

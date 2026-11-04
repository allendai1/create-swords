"""Parity tests: rules.py against the real Luau's answers (golden.json, written by Studio's ExportBalance with
balance.json). Run from the vault: python -m unittest Development/sim/test_parity.py (or pytest, if installed).
A failure means the game and the simulator disagree: fix rules.py (or re-export) before trusting any simulation."""

import json
import math
import os
import random
import unittest

import rules

HERE = os.path.dirname(os.path.abspath(__file__))
B = rules.load()
with open(os.path.join(HERE, "golden.json"), encoding="utf-8") as f:
    G = json.load(f)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1, abs(a), abs(b))


class Export(unittest.TestCase):
    def test_same_export(self):
        self.assertEqual(G["sources"], B.raw["sources"], "balance.json and golden.json come from different exports")

    def test_gates_known(self):
        for u in B.raw["upgrades"]:
            for a in u["after"]:
                self.assertIn(a, B.upgrades, f"{u['id']} comes after unknown {a}")

    def test_blueprint_pads(self):
        for u in B.raw["upgrades"]:
            if u.get("blueprint"):
                self.assertIn(u["blueprint"], B.blueprints, u["id"])


class Materials(unittest.TestCase):
    def test_odds(self):
        for c in G["odds"]:
            got = B.odds(c["luck"])
            self.assertTrue(all(close(a, b) for a, b in zip(got, c["out"])), (c["luck"], got, c["out"]))
            self.assertTrue(close(sum(got), 100))

    def test_typical_metal(self):
        for c in G["typicalMetal"]:
            self.assertTrue(close(B.typical_metal(c["luck"]), c["out"]), c)

    def test_roll_length(self):
        for c in G["rollLength"]:
            self.assertTrue(close(B.roll_length(c["metals"]), c["out"]), c)

    def test_roll_distribution(self):
        """200,000 rolls each at luck 1 and 3 against Materials.odds (chi-square, p < 0.001 fails)."""
        rng = random.Random(7)

        class R:
            def next_number(self):
                return rng.random()

            def next_integer(self, a, b):
                return rng.randint(a, b)

        r = R()
        for luck in (1, 3):
            n, counts = 200_000, [0] * len(B.rarities)
            for _ in range(n):
                counts[B.rarity_index[B.metals[B.roll(r, luck)]["rarity"]]] += 1
            exp = [o / 100 * n for o in B.odds(luck)]
            chi = sum((c - e) ** 2 / e for c, e in zip(counts, exp) if e > 0)
            self.assertLess(chi, 20.5, (luck, counts, exp))  # 5 dof, p = 0.001


class Value(unittest.TestCase):
    def test_grade(self):
        for c in G["forPercent"]:
            p, m = B.grade(c["percent"])
            self.assertEqual(p, c["pct"], c)
            self.assertTrue(close(m, c["out"]), c)

    def test_sword_value(self):
        for c in G["swordValue"]:
            got = B.sword_value(c["blueprintId"], c["materialId"], c["percent"], c["polished"], c["hiltId"], c["seatBonus"], c.get("etch"))
            self.assertEqual(got, c["out"], c)

    def test_hilts(self):
        for c in G["hiltBest"]:
            self.assertEqual(B.best_hilt(c["made"]), c["out"], c)
        for c in G["seatBonus"]:
            self.assertTrue(close(B.seat_bonus(c["taps"]), c["out"]), c)


class Customers(unittest.TestCase):
    def test_offer(self):
        for c in G["offer"]:
            self.assertEqual(B.offer(c["customer"], c["value"], c["liked"], rules.FakeRng([c["u"]])), c["out"], c)

    def test_raise(self):
        for c in G["raise"]:
            got = B.raise_offer(c["customer"], c["offer"], c["declines"], rules.FakeRng(c["seq"]), c["sure"])
            self.assertEqual(-1 if got is None else got, c["out"], c)

    def test_pick(self):
        for c in G["pick"]:
            vip = c["vipChance"] if c["vipChance"] >= 0 else None
            self.assertEqual(B.pick_customer(rules.FakeRng(c["seq"]), vip), c["out"], c)

    def test_likes(self):
        for c in G["likes"]:
            self.assertEqual(B.likes(c["customer"], c["blueprintId"], c["percent"]), c["out"], c)


class Orders(unittest.TestCase):
    def test_pay(self):
        for c in G["orderPay"]:
            mm = c["metalMult"] if c["metalMult"] >= 0 else None
            typ = c["typical"] if c["typical"] >= 0 else None
            boost = c["boost"] if c["boost"] >= 0 else None
            self.assertEqual(B.order_pay(c["value"], mm, typ, boost), c["out"], c)

    def test_shop_boost(self):
        for c in G["shopBoost"]:
            self.assertAlmostEqual(B.shop_boost(set(c["owned"])), c["out"], 9, c)

    def test_make(self):
        for c in G["orderMake"]:
            got = B.make_order(rules.FakeRng(c["seq"]), G["givers"], c["blueprints"], c["metals"], c["polish"], c["etch"], c["level"], c.get("kind"))
            want = {k: v for k, v in c["out"].items()}
            self.assertEqual(got, want, c)


class Upgrades(unittest.TestCase):
    def test_price(self):
        for c in G["price"]:
            self.assertEqual(B.price(c["id"], c["merges"]), c["out"], c)

    def test_heat_time(self):
        for c in G["heatTime"]:
            self.assertEqual(B.heat_time(set(c["bought"]), c["forge"]), c["out"], c)


class Employees(unittest.TestCase):
    def test_level(self):
        for c in G["level"]:
            self.assertEqual(list(B.staff_level(c["made"], c["scale"] if c["scale"] > 0 else None)), c["out"], c)

    def test_quality_and_seconds(self):
        for c in G["quality"]:
            self.assertEqual(B.crafter_quality(c["crafter"], c["level"]), c["out"], c)
            self.assertTrue(close(B.level_seconds(c["level"], B.crafters[c["crafter"]]["forge"]), c["seconds"]), c)
            self.assertTrue(close(B.crafter_walk(c["crafter"], c["level"]), c["walk"]), c)

    def test_perk(self):
        for c in G["perk"]:
            self.assertTrue(close(B.perk(c["role"], c["count"]), c["out"]), c)
            self.assertTrue(close(B.staff_walk(c["role"], c["count"]), c["walk"]), c)

    def test_cashier(self):
        for c in G["cashierSells"]:
            self.assertEqual(B.cashier_sells(c["offer"], c["value"], c["setting"]), c["out"], c)


class Misc(unittest.TestCase):
    def test_reputation(self):
        for c in G["reputation"]:
            self.assertEqual(list(B.reputation_level(c["points"])), c["out"], c)

    def test_deliveries(self):
        for c in G["deliveries"]:
            self.assertEqual(B.cart_capacity(c["level"]), c["capacity"], c)
            self.assertEqual(B.cart_trip(c["level"]), c["trip"], c)
        for c in G["deliveryPay"]:
            self.assertEqual(B.cart_pay(c["values"]), c["out"], c)
        for c in G["deliveryMismatch"]:
            self.assertEqual(B.cart_takes(c["blueprintId"]), c["out"] == "", c)

    def test_delivery_make(self):
        for c in G["deliveryMake"]:
            got = B.make_delivery(rules.FakeRng(c["seq"]), G["givers"], c["blueprints"], c["polish"], c["etch"], c["level"], c["capacity"])
            want = c["out"]
            self.assertEqual((got["kind"], got["count"], got["gems"], got["need"]), (want["kind"], want["count"], want["gems"], want["need"]), c)

    def test_order_fits(self):
        for c in G["orderMismatch"]:
            self.assertEqual(B.order_fits(c["need"], c["sword"]), c["out"] == "", c)

    def test_daily(self):
        for c in G["daily"]:
            self.assertEqual(B.daily(c["streak"], c["last"], c["today"]), (c["day"], c["gems"]), c)

    def test_pack_for(self):
        for c in G["packFor"]:
            key, amount = B.pack_for(c["currency"], c["short"])
            self.assertEqual([key or "", amount or 0], c["out"], c)


if __name__ == "__main__":
    unittest.main()

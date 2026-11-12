"""allen.py and the recorded-player fields (behavior.Archetype order / gem_order / slack). python -m unittest test_allen"""

import json
import os
import tempfile
import unittest

import allen
import behavior
import engine
import rules

B = rules.load()


def write(path, events):
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(json.dumps(dict(e, p=1)) + "\n" for e in events)


class Timeline(unittest.TestCase):
    def test_sittings_join_and_keys(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = os.path.join(d, "a.jsonl"), os.path.join(d, "b.jsonl")
            write(a, [{"k": "pull", "t": 6}, {"k": "forge_finish", "t": 30}, {"k": "sale", "t": 60},
                      {"k": "buy", "id": "PolishStation", "t": 90}, {"k": "buy", "id": "DecorLamp", "t": 100},
                      {"k": "gem_buy", "id": "Advertising", "level": 1, "t": 110}, {"k": "leave", "t": 120}])
            write(b, [{"k": "buy", "id": "OreStand2", "t": 30}, {"k": "merge", "n": 1, "t": 60},
                      {"k": "coins", "sku": "Cart capacity", "n": -500, "t": 90}, {"k": "hire", "id": "haru", "t": 120},
                      {"k": "buy", "id": "NotAPad", "t": 125}, {"k": "letter", "id": "IronTanto", "t": 126},
                      {"k": "mail", "sword": 9, "pay": 50, "gems": 1, "t": 127}])
            r = allen.timeline([a, b], B)
        m = r["milestones"]
        self.assertEqual(m["FirstPull"], 0.1)
        self.assertEqual(m["PolishStation"], 1.5)
        self.assertEqual(m["OreStand2"], 2.5)  # the second sitting starts where the first ended (120 s)
        self.assertNotIn("DecorLamp", m)  # decorations aren't in the sim
        self.assertEqual(r["order"], ["PolishStation", "OreStand2", "MergeSlots", "Cap1", "hire:haru"])
        self.assertEqual(r["gem_order"], ["Advertising"])
        self.assertEqual(r["unknown"], ["NotAPad"])
        self.assertEqual(r["played"], 4.12)
        self.assertEqual(r["quests"], [4.1, 4.12])  # the letter and the mail order


class RecordedPlayer(unittest.TestCase):
    def test_follows_the_order(self):
        order = ("PolishStation", "WakizashiBlueprint", "OreStand2", "OreStand3")
        a = behavior.allen_profiles({"order": order, "gem_order": (), "slack": 1.0})["allen"]
        r = engine.simulate(B, None, "free", "t:allen", 1, arche=a)
        bought = [uid for _, uid, _ in r["purchases"]]
        # the recorded buys come first; one whose pad doesn't stand yet (no sword pad before the tutorial letter) waits
        # while the next of them (engine.ORDER_LOOKAHEAD) goes ahead
        self.assertEqual(bought[0], "PolishStation")
        self.assertEqual(set(bought[:4]), set(order))

    def test_slack_slows_the_player(self):
        base = behavior.allen_profiles({"order": (), "gem_order": (), "slack": 1.0})["allen"]
        # summed over seeds: one seed's customers can come sooner for the slower player
        when = lambda a: sum(engine.simulate(B, None, "free", f"t:slack{i}", 1, arche=a)["milestones"].get("OreStand3", 60)
                             for i in range(6))
        self.assertGreater(when(behavior.replace(base, slack=2.0)), when(base))

    def test_new_player_is_slower(self):
        p = behavior.allen_profiles({"order": (), "gem_order": (), "slack": 1.2})
        self.assertAlmostEqual(p["newplayer"].slack, 1.2 * behavior.NEW_PLAYER_SLACK)
        self.assertEqual(p["newplayer"].name, "newplayer")


if __name__ == "__main__":
    unittest.main()

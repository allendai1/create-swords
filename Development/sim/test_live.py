import unittest

import behavior


class LiveProfile(unittest.TestCase):
    def test_order_miss_and_slack_from_the_numbers(self):
        j = {"min_players": 5, "slack": 1.5,
             "pads": {"KatanaBlueprint": [19.4, 28], "OreStand2": [10.0, 59], "IngotRack2": [49.3, 3]},
             "offers": {"Accepted": [6, 7.8], "Missed": [3, 30.0], "Declined": [1, 9.0]}}
        live = behavior.live_profile(j)
        self.assertEqual(live.name, "live")
        self.assertEqual(live.order, ("OreStand2", "KatanaBlueprint"))  # by minutes; too few players left out
        self.assertEqual(live.miss, 0.3)
        self.assertEqual(live.react, 7.8)
        self.assertEqual(live.slack, 1.5)
        self.assertEqual(live.buy, behavior.ARCHETYPES["casual"].buy)  # casual's pick after the order
        casual = behavior.ARCHETYPES["casual"]
        self.assertEqual((live.mail, live.etch, live.forge), (casual.mail, casual.etch, 100.0))  # casual's when live.json has none

    def test_mail_etch_and_forge_from_the_numbers(self):
        j = {"min_players": 5, "slack": 1.5, "pads": {}, "mail": 0.56, "etch": True, "forge": 97.1,
             "offers": {"Accepted": [6, 7.8], "Missed": [3, 30.0], "Declined": [1, 9.0]}}
        live = behavior.live_profile(j)
        self.assertEqual((live.mail, live.etch, live.forge), (0.56, True, 97.1))


if __name__ == "__main__":
    unittest.main()

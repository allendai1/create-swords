"""calibrate.measure on a made-up playtest: one sword from ore to sale. python -m unittest test_calibrate"""

import json
import os
import tempfile
import unittest

import calibrate
import engine
import rules
import timings


def ev(t, k, **d):
    return dict(d, t=t, k=k, p=1)


class Measure(unittest.TestCase):
    def test_one_sword(self):
        events = [
            ev(0, "hold", at="OreRoller/Pull lever"), ev(1.2, "pull", roll=1.75, fresh=True),
            ev(4, "collect", ingot=7, metal="Iron", quiet=False), ev(4.6, "collect", ingot=8, metal="Iron", quiet=False),
            ev(10, "prompt", at="Forge/Open"), ev(11.5, "furnace_put", ingot=7, metal="Iron", heat=3),
            ev(16, "furnace_take", ingot=7, waited=1), ev(16, "prompt", at="Forge/Use forge"),
            ev(20, "forge_begin", ingot=7, blueprint="Tanto"),
            ev(45, "forge_finish", ingot=7, sword=9, blueprint="Tanto", metal="Iron", percent=90, secs=25),
            ev(58, "pos", x=0.0, z=0.0), ev(59, "pos", x=10.0, z=0.0), ev(60, "pos", x=10.0, z=0.0), ev(62, "display", sword=9, slot=1),
            ev(80, "visit", sword=9, vip=False), ev(84, "offer", offer=30, value=30, vip=False, timeout=45, answer=True, secs=3),
            ev(84, "sale", sword=9, offer=30, value=30, clerk=False, declines=0, n=1),
        ]
        m, ex = calibrate.measure(events)
        self.assertAlmostEqual(m["pull_hold"][0], 1.2)
        self.assertAlmostEqual(m["collect"][0], 0.6)
        self.assertEqual((m["furnace_put"], m["furnace_take"], m["forge"], m["place"]), ([1.5], [0.0], [25], [3]))
        self.assertEqual(ex["loops"], [(80, 41, 17, 22)])
        self.assertEqual((ex["first_loop"], ex["customers"], ex["offers"]), (84 - 1.2, 1, [3]))

    def test_reset_mid_session(self):
        """Played on an old save, then Reset progress: ids start over and only the fresh save's loop counts."""
        events = [
            ev(0, "pull", roll=1, fresh=False), ev(3, "collect", ingot=7, metal="Gold", quiet=False),
            ev(10, "sale", sword=3, offer=500, value=500, clerk=False, declines=0, n=40),
            ev(100, "pull", roll=1, fresh=True), ev(103, "collect", ingot=7, metal="Iron", quiet=False),
            ev(140, "forge_finish", ingot=7, sword=9, blueprint="Tanto", metal="Iron", percent=90, secs=25),
            ev(150, "display", sword=9, slot=1), ev(170, "sale", sword=9, offer=30, value=30, clerk=False, declines=0, n=1),
        ]
        _, ex = calibrate.measure(events)
        self.assertEqual((ex["loops"], ex["first_loop"]), ([(67, 37, 10, 20)], 70))

    def test_route(self):
        """Ore roller to furnace: 3 s moving, then standing at the furnace's picker."""
        events = [ev(0, "collect", ingot=1, metal="Iron", quiet=False), ev(6, "furnace_put", ingot=1, forge="Forge2")]
        events += [ev(t, "pos", x=16.0 * min(t, 3), z=0.0) for t in range(7)]
        _, ex = calibrate.measure(sorted(events, key=lambda e: e["t"]))
        self.assertEqual(ex["routes"], {"Forge2-OreRoller": [3]})

    def test_forge_seconds_at_todays_strikes(self):
        """A session named before the 10-strike recipe forged 12 strikes: its forge seconds scale to today's; later ones stay."""
        got = []
        with tempfile.TemporaryDirectory() as d:
            for name in ("2026-10-29_192223", "2026-11-01_120000"):
                path = os.path.join(d, name + ".jsonl")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(json.dumps(ev(45, "forge_finish", ingot=7, sword=9, blueprint="tanto", percent=100, secs=24)) + "\n")
                got += calibrate.measure(calibrate.load([path])[0])[0]["forge"]
        self.assertEqual(got, [24 * calibrate.STRIKES_NOW / 12, 24])

    def test_engine_walks_measured_route(self):
        saved = dict(timings.ROUTES), timings.WALK_SPEED
        try:
            timings.ROUTES.clear()
            timings.ROUTES[timings.route_key("OreRoller", "Anvil", False)] = 10.0
            timings.WALK_SPEED = 16.0
            sim = engine.Sim(rules.load(), engine.behavior.with_overrides(engine.behavior.ARCHETYPES["manager"], waste_chance=0.0), "free", "t:r", 1)
            sim.at = "Anvil"
            self.assertAlmostEqual(sim.walk("OreRoller"), 10.0 * 16.0 / sim.speed)
            self.assertNotAlmostEqual(sim.walk("Forge"), 10.0 * 16.0 / sim.speed)  # not measured: the layout's distance
        finally:
            timings.ROUTES.clear()
            timings.ROUTES.update(saved[0])
            timings.WALK_SPEED = saved[1]


if __name__ == "__main__":
    unittest.main()

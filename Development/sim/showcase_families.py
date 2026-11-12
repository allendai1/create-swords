"""Showcase families experiment (2026-11-09; vault: Development/Sim Runs/showcase-families-2026-11-09).

python showcase_families.py [seeds] [hours]

The engine applies the game's families (Shared/Showcase via balance.json's shop.showcase: family, rate, cap, gems) to
whatever stand_swords puts on the stands. Here each run fills every stand with ONE family's best collected metal
("none": nothing on the stands) and compares coins earned per stage against "none", then the passes against full stands
of the family they overlap. Before 2026-11-09 (evening) this file wrapped the engine with its own copy of the effects.
"""

import statistics as st
import sys

import behavior
import engine
import rules

CHECKS = (3600, 4 * 3600)  # stage edges: 0-1 h, 1-4 h, 4 h-end


class FamilySim(engine.Sim):
    def __init__(self, B, arche, payer, seed, hours, family):
        super().__init__(B, arche, payer, seed, hours)
        self.family = family
        self.at_checks = []

    def stand_swords(self):
        n = sum(f"Showcase{k}" in self.owned for k in (1, 2, 3))
        if not n or self.family == "none":
            return []
        S = self.raw["shop"]["showcase"]
        mine = [m for m in self.discovered if S["family"].get(m) == self.family]
        if not mine:
            return []
        best = max(mine, key=lambda m: S["tier"][self.B.metals[m]["rarity"]])
        return [(best, self.best_bp(), "PolishStation" in self.owned, self.B.best_etch(self.owned) is not None)] * n

    def earn(self, coins):
        while len(self.at_checks) < len(CHECKS) and self.t >= CHECKS[len(self.at_checks)]:
            self.at_checks.append(self.earned)
        super().earn(coins)


def run(B, arche, payer, family, seeds, hours, sim_class=None):
    rows = []
    for k in range(seeds):
        sim = (sim_class or FamilySim)(B, behavior.ARCHETYPES[arche], payer, f"fam:{k}", hours, family)
        r = sim.run()
        checks = sim.at_checks + [r["earned"]] * (len(CHECKS) - len(sim.at_checks))
        m = r["milestones"]
        rows.append({"stages": [checks[0], checks[1] - checks[0], r["earned"] - checks[1]], "earned": r["earned"],
                     "gems": sum(r["gems_in"].values()), "zanbato": m.get("ZanbatoBlueprint"), "seraph": m.get("SeraphBlueprint"),
                     "effect": sim.stand_effects().get(family, 0.0)})
    return rows


def med(xs):
    xs = [x for x in xs if x is not None]
    return st.median(xs) if xs else None


def main(seeds=12, hours=10):
    B = rules.load()
    fams = ["none"] + list(B.raw["shop"]["showcase"]["rate"])
    for arche in ("casual", "efficient"):
        base = run(B, arche, "free", "none", seeds, hours)
        b = [med([r["stages"][i] for r in base]) for i in range(3)]
        bg = med([r["gems"] for r in base])
        print(f"\n{arche}, free, {seeds} seeds, {hours} h: coins earned by stage, % over stands that give nothing")
        print(f"{'family':10s} {'0-1 h':>7s} {'1-4 h':>7s} {'4-10 h':>7s} {'gems':>6s} {'Zanbato':>8s} {'Seraph':>7s} {'end effect':>10s}")
        for fam in fams:
            rows = base if fam == "none" else run(B, arche, "free", fam, seeds, hours)
            s = [med([r["stages"][i] for r in rows]) for i in range(3)]
            pct = [f"{(s[i] / b[i] - 1) * 100:+6.1f}%" if b[i] else "    -  " for i in range(3)]
            z, se, g, eff = med([r["zanbato"] for r in rows]), med([r["seraph"] for r in rows]), med([r["gems"] for r in rows]), med([r["effect"] for r in rows])
            print(f"{fam:10s} {pct[0]} {pct[1]} {pct[2]} {g - bg:+6.0f} {(f'{z / 60:6.2f}h' if z else '     -'):>8s} "
                  f"{(f'{se / 60:5.2f}h' if se else '    -'):>7s} {eff:10.3f}")
    print("\npasses vs full stands (efficient, coins earned in 10 h, % over free with stands that give nothing)")
    for fam, pas in (("Luck", "LuckyOre"), ("Coins", "MoreCoins"), ("Swift", "SwiftBoots"), ("Vip", "VIP")):
        behavior.PAYERS[pas] = (pas,)
        base = med([r["earned"] for r in run(B, "efficient", "free", "none", seeds, hours)])
        stand = med([r["earned"] for r in run(B, "efficient", "free", fam, seeds, hours)])
        paid = med([r["earned"] for r in run(B, "efficient", pas, "none", seeds, hours)])
        both = med([r["earned"] for r in run(B, "efficient", pas, fam, seeds, hours)])
        print(f"{fam:6s} stands {(stand / base - 1) * 100:+6.1f}%   {pas} pass {(paid / base - 1) * 100:+6.1f}%   both {(both / base - 1) * 100:+6.1f}%")


if __name__ == "__main__":
    main(*(int(a) for a in sys.argv[1:]))

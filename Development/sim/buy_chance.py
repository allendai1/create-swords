"""More Sales' buy chance against every walk-in offering (2026-11-10; vault: Development/Sim Runs/buy-chance-2026-11-10).

python buy_chance.py [seeds] [hours]

Each case sets every level's buy chance (and the polish / etch bonus) and reports the milestone times, coins earned
and walk-ins that passed, against the old game (always buys: chance 1).
"""

import sys

import customer_rate as cr
import engine
import rules


def load(base=None, step=0.06, bonus=0.10):
    B = rules.load()
    G = B.raw["gemUpgrades"]
    if base is not None:
        for i, lv in enumerate(G["levels"]):
            lv["buyChance"] = min(1, base + step * i)
        G["buyPolished"] = G["buyEtched"] = bonus
    return B


def main(seeds=12, hours=20):
    cases = [("old: always buys", load(1.0, 0, 0)), ("60%, +6%/lv, +10%", load()), ("70%, +5%/lv, +10%", load(0.7, 0.05)),
             ("50%, +8%/lv, +10%", load(0.5, 0.08))]
    for arche in ("casual", "efficient"):
        print(f"\n{arche}, free, {seeds} seeds, {hours} h (h:mm)")
        print(f"{'case':20s} {'Crafter':>8s} {'Katana':>8s} {'Show1':>8s} {'Longsw':>8s} {'Zanbato':>9s} {'Seraph':>10s} {'earned':>10s} {'passed':>7s} {'Sales5':>7s}")
        for label, B in cases:
            rows = []
            for s in range(seeds):
                r = engine.simulate(B, arche, "free", f"cr:{s}", hours)
                rows.append((cr.one(B, arche, f"cr:{s}", hours), r["passed_on"], r["milestones"].get("Sales5")))
            c = {k: cr.st.median([x[0][k] for x in rows if x[0][k] is not None]) if any(x[0][k] is not None for x in rows) else None for k in rows[0][0]}
            n = {k: sum(1 for x in rows if x[0][k] is not None) for k in rows[0][0]}
            s5 = [x[2] for x in rows if x[2] is not None]
            print(f"{label:20s} " + " ".join(f"{cr.fmt(c[m], n[m], seeds):>8s}" for m in cr.MILESTONES[:4])
                  + f" {cr.fmt(c['ZanbatoBlueprint'], n['ZanbatoBlueprint'], seeds):>9s} {cr.fmt(c['SeraphBlueprint'], n['SeraphBlueprint'], seeds):>10s}"
                  + f" {c['earned']:>10.3g} {cr.st.median(x[1] for x in rows):>7.0f} {cr.fmt(cr.st.median(s5) if s5 else None, len(s5), seeds):>7s}")


if __name__ == "__main__":
    main(*(int(a) for a in sys.argv[1:]))

"""Walk-ins more often, coin prices up to match (2026-11-09; vault: Development/Sim Runs/customer-rate-2026-11-09).

python customer_rate.py [seeds] [hours]

Each case divides every Better Advertising level's walk-in gap by `rate` and multiplies every coin price of MIN_PRICE
or more (pads, cart capacity and speed, crafter hires) by `k`; the tutorial's cheap pads stay. Reports the milestone
times, waits over 15 min between buys and the buys after the Seraph, against today's game.
"""

import statistics as st
import sys

import behavior
import engine
import rules

MIN_PRICE = 100
MILESTONES = ("Crafter", "KatanaBlueprint", "Showcase1", "LongswordBlueprint", "ZanbatoBlueprint", "SeraphBlueprint")


def load(rate=1.0, k=1.0):
    B = rules.load()
    for lv in B.raw["gemUpgrades"]["levels"]:
        lv["walkIn"] = [x / rate for x in lv["walkIn"]]
    for u in B.upgrades.values():
        if u["price"] >= MIN_PRICE:
            u["price"] = int(round(u["price"] * k, -1))
    D = B.raw["deliveries"]
    D["capacityPrice"] = [int(round(p * k, -1)) for p in D["capacityPrice"]]
    D["speedPrice"] = [int(round(p * k, -1)) for p in D["speedPrice"]]
    for c in B.raw["employees"]["crafters"]:
        if c.get("coins"):
            c["coins"] = int(round(c["coins"] * k, -1))
    return B


def one(B, arche, seed, hours):
    r = engine.simulate(B, arche, "free", seed, hours)
    buys = sorted(r["purchases"])
    times = [0.0] + [m for m, *_ in buys]
    waits = sum(1 for a, b in zip(times, times[1:]) if b - a > 15)
    m = r["milestones"]
    seraph = m.get("SeraphBlueprint")
    after = sum(1 for t, uid, *_ in buys if seraph and t > seraph and not uid.startswith("OreStand") and uid != "MergeSlots")
    return {**{k: m.get(k) for k in MILESTONES}, "waits": waits, "after": after if seraph else None, "earned": r["earned"]}


def case(B, arche, seeds, hours):
    rows = [one(B, arche, f"cr:{s}", hours) for s in range(seeds)]
    out = {}
    for k in rows[0]:
        xs = [r[k] for r in rows if r[k] is not None]
        out[k] = (st.median(xs) if xs else None, len(xs))
    return out


def fmt(v, n, seeds, minutes=True):
    if v is None:
        return "-"
    s = (f"{int(v // 60)}:{int(v % 60):02d}" if v >= 60 else f"{v:.0f}m") if minutes else f"{v:.0f}"
    return s if n == seeds else f"{s} ({n})"


def main(seeds=12, hours=20):
    cases = [("now", 1.0, 1.0), ("x1.5", 1.5, 1.0), ("x1.5, prices x1.3", 1.5, 1.3), ("x1.5, prices x1.45", 1.5, 1.45),
             ("x1.5, prices x1.6", 1.5, 1.6)]
    for arche in ("casual", "efficient"):
        print(f"\n{arche}, free, {seeds} seeds, {hours} h (h:mm; a count in brackets: runs that got there)")
        print(f"{'case':20s} {'Crafter':>8s} {'Katana':>8s} {'Show1':>8s} {'Longsw':>8s} {'Zanbato':>9s} {'Seraph':>10s} {'waits>15':>8s} {'after Seraph':>12s}")
        for label, rate, k in cases:
            c = case(load(rate, k), arche, seeds, hours)
            print(f"{label:20s} " + " ".join(f"{fmt(*c[m], seeds):>8s}" for m in MILESTONES[:4])
                  + f" {fmt(*c['ZanbatoBlueprint'], seeds):>9s} {fmt(*c['SeraphBlueprint'], seeds):>10s}"
                  + f" {fmt(*c['waits'], seeds, False):>8s} {fmt(*c['after'], seeds, False):>12s}")


if __name__ == "__main__":
    main(*(int(a) for a in sys.argv[1:]))

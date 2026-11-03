"""Time model for upgrade prices (LihFolk vault, Genre Playbook - Tycoons §3: wait(k) = cost(k+1) / income(k)).
1. Order: every coin buy in the order engaged players first buy them today (sim run ORDER_RUN, gates kept).
2. Schedule: the decided targets (ANCHORS) split the order into stretches; each stretch's time is shared out over its
   buys by wait(t), a milestone taking 3 buys' worth (a bigger save, then cheap buys again). Buy k lands at T(k).
3. Price = its share of time x income at T(k) x the stretch's correction. Run the sim, re-measure income, correct each
   stretch by how late or early players reach its target, and repeat.
The schedule is fixed, so no buy chases its own price (pricing each buy by when players happen to buy it ran away).

    python time_model.py [passes]   writes time_prices.json (read by the "timed" scenario) and prints the schedule
"""
import json
import math
import os
import statistics as st
import subprocess
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "time_prices.json")
REF = "efficient,manager,grinder"  # engaged players set the prices; casual players take longer on the same prices
ORDER_RUN = ("order-2026-11-02", "baseline")  # today's gates and prices: run.py --name order-2026-11-02 --players 30 --hours 22 --archetypes efficient,manager,grinder
HOURS, PLAYERS = 22, 30


def wait(t):  # minutes of income for an ordinary buy at minute t: 1.5 at the start to 12 at 12 h (vault: rising slowly)
    return 1.5 + 10.5 * min(t, 720) / 720


MILESTONE = {"Crafter", "UpgradedStore", "ZanbatoBlueprint", "ClaymoreBlueprint", "FlambergeBlueprint",
             "SeraphBlueprint", "EtchingTable2", "Etcher", "hire:haru", "hire:mei", "hire:kenji", "hire:rin"}
# Decided targets, minutes (Decisions Log 2026-10-29: Katana 15 min, Longsword 40 min, Crafter 1 h 30, Seraph 20 h;
# 2026-10-30: Zanbato 4 h)
# The Sword Crafter left the anchors 2026-11-02: his target is ~15 min (beside the Katana's) and his price is pinned below.
ANCHORS = {"KatanaBlueprint": 15, "LongswordBlueprint": 40, "ZanbatoBlueprint": 240, "SeraphBlueprint": 1200}
FIXED = {"WakizashiBlueprint": 60, "OreStand2": 75, "PolishStation": 30,  # the tutorial's buys keep their prices
         "Crafter": 2000, "Stocker": 12000}  # Allen 2026-11-02: the first hire at ~15 min ("Yes, build it"); "Yes, both" (the Stocker)


def sig2(x):
    if x < 100:
        return max(1, round(x))
    p = 10 ** (int(math.log10(x)) - 1)
    return int(round(x / p) * p)


def load(name, scen=None):
    rows = [json.loads(l) for l in open(os.path.join(HERE, "results", name, "players.jsonl"), encoding="utf-8")]
    return [r for r in rows if r["archetype"] in REF.split(",") and (scen is None or r["scenario"] == scen)]


def income(rows):
    """Median coins per minute at each minute, over a 15-minute window ('earned' is per minute to 60, then per 5)."""
    curves = []
    for r in rows:
        e = r["earned"]
        mins = [k if k <= 60 else 60 + 5 * (k - 60) for k in range(len(e))]
        curves.append((mins, e))
    def at(t):
        vals = []
        for mins, e in curves:
            a, b = max(0, t - 7.5), t + 7.5
            if b > mins[-1]:
                continue
            ia = max(i for i, m in enumerate(mins) if m <= a); ib = min(i for i, m in enumerate(mins) if m >= b)
            vals.append((e[ib] - e[ia]) / (mins[ib] - mins[ia]))
        return st.median(vals) if vals else None
    return at


def gates():
    raw = json.load(open(os.path.join(HERE, "balance.json"), encoding="utf-8"))
    g = {u["id"]: list(u["after"]) for u in raw["upgrades"] if not u["decor"] and u["price"] > 0}
    ids = {c["id"] for c in raw["employees"]["crafters"]}
    for c in raw["employees"]["crafters"]:
        if c.get("coins"):
            a = c.get("after")
            g["hire:" + c["id"]] = ["Crafter"] + (["hire:" + a if a in ids else a] if a else [])
    D = raw["deliveries"]
    for key, lst in (("Cap", D["capacityPrice"]), ("Spd", D["speedPrice"])):
        for i in range(len(lst)):
            g[f"{key}{i + 1}"] = ["Delivery"] + ([f"{key}{i}"] if i else [])
    return g


def order():
    g, when = gates(), defaultdict(list)
    for r in load(*ORDER_RUN):
        seen = set()
        for t, uid, *_ in r["buys"]:  # first buy only: a merge re-buys the Ore Slots later
            if uid not in seen:
                seen.add(uid)
                when[uid].append(t)
    key = {u: st.median(when[u]) if when[u] else 1e9 for u in g}
    left, done, out = sorted(g, key=lambda u: key[u]), set(), []
    while left:  # earliest first, but never before its gates
        u = next(u for u in left if all(a in done or a not in g for a in g[u]))
        left.remove(u); done.add(u); out.append(u)
    return out


def schedule(seq, R, fix):
    """(plan, prices): plan is (id, T, share of time, stretch). fix: stretch -> price correction."""
    weight, t = {}, 0.0
    for u in seq:  # provisional times from wait() alone, for the weights
        weight[u] = 0 if u in FIXED else wait(t) * (3 if u in MILESTONE else 1)
        t += weight[u]
    plan, t0, stretch, seg = [], 0.0, 0, []
    for u in seq:
        seg.append(u)
        if u in ANCHORS or u == seq[-1]:
            total = sum(weight[x] for x in seg)
            span = ANCHORS[u] - t0 if u in ANCHORS else total  # past the last target: wait() as it stands
            t = t0
            for x in seg:
                share = span * weight[x] / total if total else 0
                t += share
                plan.append((x, t, share, stretch))
            t0, stretch, seg = t, stretch + 1, []
    prices = {}
    for u, T, share, k in plan:
        r = R(T)
        prices[u] = FIXED.get(u) or (sig2(share * r * fix.get(k, 1)) if r else None)
    last = next(p for p in reversed([prices[u] for u, *_ in plan]) if p)
    for u, *_ in plan:  # past the run's horizon: keep the last priced buy's price
        prices[u] = prices[u] or last
    return plan, prices


def correct(rows, plan, fix):
    """Per stretch: target length / the players' median length (anchor to anchor), halfway in ratio."""
    first = defaultdict(list)
    for r in rows:
        ms = r["milestones"]
        for a in ANCHORS:
            first[a].append(ms.get(a, 1e9))
    ends = [(k, u) for u, T, share, k in plan if u in ANCHORS]
    prev_t, prev_a = 0.0, 0.0
    for k, a in ends:
        actual = min(st.median(first[a]), HOURS * 60) - prev_a  # never reached: count the run's end
        target = ANCHORS[a] - prev_t
        fix[k] = fix.get(k, 1) * min(1.25, max(0.8, (target / max(actual, 1)) ** 0.5))  # small steps: a cheaper stretch raises income for every later one
        prev_t, prev_a = ANCHORS[a], min(st.median(first[a]), HOURS * 60)
    return fix


def run(name):
    subprocess.run([sys.executable, "-X", "utf8", "run.py", "--name", name, "--players", str(PLAYERS), "--hours",
                    str(HOURS), "--archetypes", REF, "--scenarios", "timed"], cwd=HERE, check=True, stdout=subprocess.DEVNULL)
    return load(name)


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    seq, fix = order(), {}
    R = income(load(*ORDER_RUN))
    prices = None
    for i in range(n + 1):
        plan, new = schedule(seq, R, fix)
        if prices:
            print(f"pass {i}: median price move {100 * st.median(abs(new[u] / prices[u] - 1) for u in new):.0f}%",
                  {a: f"{int(T // 60)}:{int(T % 60):02d}" for a, T in actual.items()}, flush=True)
        prices = new
        json.dump(prices, open(OUT, "w"), indent=1, sort_keys=True)
        if i < n:
            rows = run(f"time-model-{i}")
            R, fix = income(rows), correct(rows, plan, fix)
            actual = {a: st.median(r["milestones"].get(a, 1e9) for r in rows) for a in ANCHORS}
    for u, T, share, k in plan:
        print(f"{int(T // 60)}:{int(T % 60):02d}  {share:5.1f} min  {prices[u]:>10,}  {u}")

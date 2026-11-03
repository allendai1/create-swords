"""Measured hand-action times from Studio playtests (ServerScriptService.PlaytestLog -> receive.py -> playtests/*.jsonl).
Writes timings.json, whose medians replace timings.py's estimates in every later run, and prints what it measured and
what play looked like (offers, customers, the ore-to-sale loop). Keys with fewer than MIN_N samples stay estimates.

python calibrate.py                      (every session in playtests/)
python calibrate.py playtests/2026-10-30_181500.jsonl ...

Walking: each route between two stations in a row (either way round, and apart before and after the Upgraded Store)
gets its seconds spent moving; with MIN_ROUTE walks its median replaces the layout's distance x detour.

A session can start from your save or from Reset progress: only a fresh save's first pull and first sale make the
first loop, and loops restart there. These are Allen's hands: an expert's times. Archetypes differ by how they choose
and react (behavior.py), not by these."""

import glob
import json
import math
import os
import sys

import engine
import rules
import timings

HERE = os.path.dirname(os.path.abspath(__file__))
MIN_N = 5
MIN_OFFERS = 10  # offer cards before your answer time and miss rate replace the player types' guesses
MIN_ROUTE = 3  # walks of one route before its measured seconds replace the layout's distance x detour
# Forge seconds are kept at today's strikes per blade (balance.json) and timings.json says which (timings.FORGE_STRIKES).
# Sessions (named by their UTC start) from before the 10-strike recipe reached the place forged 12: load() marks them.
# ponytail: one count for every blueprint (the tantō's); per-blueprint scaling if blueprints ever differ.
TEN_STRIKES_FROM = "2026-10-31_013839"
STRIKES_NOW = rules.load().blueprints["tanto"]["strikes"]


def quant(xs, q):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(q * len(xs)))] if xs else None


def last_before(events, i, pred, within):
    """The latest event before events[i], at most `within` seconds earlier, that pred accepts."""
    t = events[i]["t"]
    for j in range(i - 1, -1, -1):
        if t - events[j]["t"] > within:
            return None
        if pred(events[j]):
            return events[j]
    return None


def prompt_gap(events, i, pred, within):
    """Seconds from the prompt pred accepts to events[i]: 0 when one fired in the same instant (an action straight off its
    prompt, like taking from the furnace), else from the latest one up to `within` seconds before; None if none."""
    t = events[i]["t"]
    if any(abs(e["t"] - t) < 0.05 and pred(e) for e in events[max(0, i - 5):i + 6]):
        return 0.0
    p = last_before(events, i, pred, within)
    return None if p is None else t - p["t"]


def arrived(pos, t, within):
    """When the player last stopped walking before t (the end of their last moving step), or None."""
    for p, q in zip(reversed(pos[:-1]), reversed(pos[1:])):
        if q["t"] > t:
            continue
        if t - q["t"] > within:
            return None
        if math.hypot(q["x"] - p["x"], q["z"] - p["z"]) / max(0.01, q["t"] - p["t"]) > 2:
            return q["t"]
    return None


def prompt_at(word):
    return lambda e: e["k"] in ("prompt", "hold") and word in e.get("at", "")


def station(e):
    """Where the player stood for this event, by the simulator's station names (engine.pos), or None."""
    k = e["k"]
    if e.get("crafter"):
        return None
    if k in ("pull", "collect"):
        return "OreRoller"
    if k in ("furnace_put", "furnace_take"):
        return e.get("forge", "Forge")
    if k == "rack":
        return e["rack"] + "Rack"
    if k in ("cart_accept", "cart_send", "cart_collect"):
        return "DeliveryBay"
    if k == "buy":
        return "pad:" + e["id"]
    return {"forge_begin": "Anvil", "polish_begin": "PolishStation", "etch": "EtchingTable", "display": "shop"}.get(k)


def measure(events):
    """events: one player's, in time order. Returns ({timing key: [seconds]}, extras)."""
    m = {k: [] for k in timings.ESTIMATE}
    pos = [e for e in events if e["k"] == "pos"]
    ex = {"offers": [], "missed": 0, "customers": 0, "loops": [], "speeds": [], "first_loop": None}
    by_ingot, by_sword = {}, {}
    first_pull, was_fresh = None, False
    for i, e in enumerate(events):
        k = e["k"]
        if k == "pull":
            if e.get("fresh") and not was_fresh:  # a new save, or Reset progress: its ids start over
                first_pull = e["t"]
                by_ingot.clear()
                by_sword.clear()
            was_fresh = e.get("fresh", False)
            h = last_before(events, i, lambda x: x["k"] == "hold", 5)
            if h:
                m["pull_hold"].append(e["t"] - h["t"])
        elif k == "collect":
            by_ingot.setdefault(e["ingot"], {})["ore"] = e["t"]
            prev = last_before(events, i, lambda x: x["k"] == "collect" and not x.get("quiet"), 5)
            if prev and not e.get("quiet"):
                m["collect"].append(e["t"] - prev["t"])
        elif k in ("furnace_put", "furnace_take") and not e.get("crafter"):
            gap = prompt_gap(events, i, prompt_at("Forge"), 30)
            if gap is not None:
                m[k].append(gap)
        elif k == "forge_finish":
            m["forge"].append(e["secs"] * STRIKES_NOW / e.get("strikes", STRIKES_NOW))
            by_sword[e["sword"]] = dict(by_ingot.get(e["ingot"], {}), forged=e["t"])
        elif k == "polish" and e.get("polished"):
            m["polish"].append(e["secs"])
        elif k == "etch":
            gap = prompt_gap(events, i, prompt_at("Etch"), 120)
            if gap is not None:
                m["etch"].append(gap)
        elif k == "display":  # the holder's + is on screen, not a prompt: from stopping by it (or the last one placed)
            a = arrived(pos, e["t"], 20)
            prev = last_before(events, i, lambda x: x["k"] == "display", 20)
            start = max([x for x in (a, prev and prev["t"]) if x is not None], default=None)
            if start is not None:
                m["place"].append(e["t"] - start)
            if e["sword"] in by_sword:
                by_sword[e["sword"]]["placed"] = e["t"]
        elif k == "rack" and e.get("action") in ("store", "take"):  # one ingot or sword: from the last one, or the prompt
            prev = last_before(events, i, lambda x: x["k"] == "rack", 10)
            gap = e["t"] - prev["t"] if prev else prompt_gap(events, i, prompt_at("Rack"), 30)
            if gap is not None:
                m["rack"].append(gap)
        elif k == "buy":  # the pad's Buy button is on screen: from stopping on the pad
            a = arrived(pos, e["t"], 20)
            if a is not None:
                m["buy"].append(e["t"] - a)
        elif k == "cart_send":  # the whole board visit, from its prompt to the cart leaving (Auto-Fill packs in one tap)
            gap = prompt_gap(events, i, prompt_at("Deliver"), 300)
            if gap is not None:
                m["cart_visit"].append(gap)
        elif k == "offer":
            if e["answer"] == "none":
                ex["missed"] += 1
            else:
                ex["offers"].append(e["secs"])
        elif k in ("visit", "browse"):
            ex["customers"] += 1
        elif k == "sale":
            s = by_sword.get(e["sword"], {})
            if {"ore", "forged", "placed"} <= s.keys():  # your own swords, from ore to sale
                ex["loops"].append((e["t"] - s["ore"], s["forged"] - s["ore"], s["placed"] - s["forged"], e["t"] - s["placed"]))
            if e.get("n") == 1 and first_pull is not None:  # the save's first sale, from its first pull
                ex["first_loop"] = e["t"] - first_pull
    # walking: speed while moving; between two stations in a row, the seconds spent moving (that route's walk) and how
    # much longer the path is than the straight line
    step = lambda p, q: math.hypot(q["x"] - p["x"], q["z"] - p["z"]) / max(0.01, q["t"] - p["t"])
    for a, b in zip(pos, pos[1:]):
        if 2 < step(a, b) < 60:
            ex["speeds"].append(step(a, b))
    ex["routes"] = {}
    stops = [(e["t"], station(e)) for e in events if station(e)]
    for (ta, sa), (tb, sb) in zip(stops, stops[1:]):
        seg = [p for p in pos if ta - 0.5 <= p["t"] <= tb + 0.5]
        if sa == sb or tb - ta > 90 or len(seg) < 3:
            continue
        moving = sum(q["t"] - p["t"] for p, q in zip(seg, seg[1:]) if 2 < step(p, q) < 60)
        if moving > 0:
            ex["routes"].setdefault(timings.route_key(sa, sb, any(p.get("u") for p in seg)), []).append(moving)
        path = sum(math.hypot(q["x"] - p["x"], q["z"] - p["z"]) for p, q in zip(seg, seg[1:]))
        straight = math.hypot(seg[-1]["x"] - seg[0]["x"], seg[-1]["z"] - seg[0]["z"])
        if straight >= 12 and tb - ta <= 60:
            m["detour"].append(max(1.0, path / straight))
    ex["minutes"] = (events[-1]["t"] - events[0]["t"]) / 60 if events else 0
    return m, ex


def load(paths):
    """Every player's events from every session, each list in time order."""
    players = []
    for path in paths:
        by = {}
        twelve = os.path.basename(path) < TEN_STRIKES_FROM
        with open(path, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    e = json.loads(line)
                    if twelve and e["k"] == "forge_finish":
                        e.setdefault("strikes", 12)
                    by.setdefault(e["p"], []).append(e)
        players += [sorted(v, key=lambda e: e["t"]) for v in by.values()]
    return players


def main(paths):
    paths = paths or sorted(glob.glob(os.path.join(HERE, "playtests", "*.jsonl")))
    if not paths:
        sys.exit("no playtest logs yet: run receive.py, then play in Studio")
    m, ex = {k: [] for k in timings.ESTIMATE}, {"offers": [], "missed": 0, "customers": 0, "loops": [], "speeds": [],
                                                "first_loop": [], "minutes": 0, "routes": {}}
    for events in load(paths):
        pm, pe = measure(events)
        for k in m:
            m[k] += pm[k]
        for k in ("offers", "loops", "speeds"):
            ex[k] += pe[k]
        ex["missed"] += pe["missed"]
        ex["customers"] += pe["customers"]
        ex["minutes"] += pe["minutes"]
        for r, xs in pe["routes"].items():
            ex["routes"].setdefault(r, []).extend(xs)
        if pe["first_loop"] is not None:
            ex["first_loop"].append(pe["first_loop"])

    out = {}
    print(f"{len(paths)} session(s), {ex['minutes']:.0f} min of play\n")
    print(f"{'action':14} {'estimate':>8} {'measured':>9} {'25-75%':>13} {'n':>4}")
    for k, xs in m.items():
        med = quant(xs, 0.5)
        if xs and len(xs) >= MIN_N:
            out[k] = {"median": round(med, 2), "p25": round(quant(xs, 0.25), 2), "p75": round(quant(xs, 0.75), 2), "n": len(xs)}
        spread = f"{quant(xs, 0.25):.1f}-{quant(xs, 0.75):.1f}" if xs else ""
        print(f"{k:14} {timings.ESTIMATE[k]:8.1f} {'' if med is None else f'{med:.1f}':>9} {spread:>13} {len(xs):>4}"
              + ("" if k in out else "   (stays estimate)"))
    answered = len(ex["offers"])
    print(f"\noffers: answered {answered}, median {quant(ex['offers'], 0.5) or 0:.1f} s; missed "
          f"{ex['missed']} ({ex['missed'] / max(1, answered + ex['missed']):.0%})")
    print(f"customers: {ex['customers'] / max(1, ex['minutes']):.2f} per minute; walking {quant(ex['speeds'], 0.5) or 0:.1f} studs/s")
    if ex["loops"]:
        L = ex["loops"]
        med = [quant([x[i] for x in L], 0.5) for i in range(4)]
        print(f"ore to sale (your swords, n={len(L)}): {med[0]:.0f} s = making {med[1]:.0f} + getting out {med[2]:.0f} "
              f"+ selling {med[3]:.0f}")
    if ex["first_loop"]:
        print(f"first pull to first sale: {quant(ex['first_loop'], 0.5) / 60:.1f} min (n={len(ex['first_loop'])})")
    if "forge" in out:
        out["forge"]["strikes"] = STRIKES_NOW
    n_offers = answered + ex["missed"]
    offers = ({"react": round(quant(ex["offers"], 0.5), 2), "miss": round(ex["missed"] / n_offers, 3), "n": n_offers}
              if n_offers >= MIN_OFFERS and answered else None)
    walk_speed = quant(ex["speeds"], 0.5)
    routes = {}
    pos, detour = engine.layout_pos(rules.load().raw), out.get("detour", {}).get("median", timings.ESTIMATE["detour"])
    print(f"\n{'walk (either way)':40} {'layout est.':>11} {'measured':>9} {'n':>4}")
    once = 0
    for r, xs in sorted(ex["routes"].items(), key=lambda kv: -len(kv[1])):
        if len(xs) == 1:  # walked once: not printed, still kept for later sessions to add to
            once += 1
            continue
        a, b = r.split(" ")[0].split("-")
        est = (math.hypot(pos[a][0] - pos[b][0], pos[a][1] - pos[b][1]) * detour / walk_speed
               if a in pos and b in pos and walk_speed else None)
        if len(xs) >= MIN_ROUTE:
            routes[r] = {"median": round(quant(xs, 0.5), 2), "p25": round(quant(xs, 0.25), 2),
                         "p75": round(quant(xs, 0.75), 2), "n": len(xs)}
        print(f"{r:40} {'' if est is None else f'{est:.1f}':>11} {quant(xs, 0.5):9.1f} {len(xs):>4}"
              + ("" if r in routes else "   (layout until 3)"))
    if once:
        print(f"(+ {once} routes walked once)")
    with open(os.path.join(HERE, "timings.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"timings": out, "routes": routes, "offers": offers, "walk_speed": round(walk_speed, 2) if walk_speed else None,
                   "sessions": [os.path.basename(p) for p in paths]}, f, indent=1)
    print(f"\nwrote timings.json: {', '.join(out) or 'no actions measured enough yet'}; {len(routes)} walking routes")


if __name__ == "__main__":
    main(sys.argv[1:])

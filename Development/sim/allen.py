"""Allen as the simulator's reference player (2026-11-09, Allen: "just use me as an average or above average player, and
record how quickly im progressing through the playtest from start to wherever i stop").

Record (Studio): keep `python receive.py` running, tick ServerScriptService.StoreService's StudioLocked (you own every
pass as the group's owner; locked, you play as a free player), Dev panel > Reset progress, then play as you would. Stop
when you like; a later sitting carries on from your save and is joined on (the time between sittings is left out).
Don't use Dev panel coins, gems or Skip tutorial during the run.

Then:
    python calibrate.py playtests/<the run's files>                     (your hand times, from this run)
    python allen.py playtests/<the run's files> --name allen-2026-11-10  (optional: --hours 6 --seeds 16)

It reads the run as one timeline, writes allen.json (your purchases in order, your gem buys, and `slack`: the pace that
makes the sim's timeline match yours), runs "allen" and "newplayer" (behavior.py) past where you stopped, and writes
the side-by-side note Development/Sim Runs/<name>.md. run.py uses allen and newplayer by default once allen.json exists."""

import argparse
import datetime
import json
import math
import os
import statistics
import sys

import behavior
import engine
import rules

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.join(HERE, "..", "Sim Runs")
CART = {"Cart capacity": "Cap", "Cart speed": "Spd"}  # DeliveryService logs a cart level as coins with these skus
MIN_ACTUAL = 0.5  # minutes: milestones before this are the first seconds of play, too short to fit a pace on
SLACK_RANGE = (0.3, 5.0)


def read_events(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def timeline(paths, B):
    """Your run as {key: minute} (first time each), the purchase order and gem order as the engine names them, the
    minutes played, and the logged ids the sim doesn't know. Sittings are joined end to start."""
    milestones, order, gem_order, unknown, quests = {}, [], [], [], []
    offset, cart, merges = 0.0, {"Cap": 0, "Spd": 0}, 0
    player = None
    for path in paths:
        events = sorted(read_events(path), key=lambda e: e["t"])
        if player is None:  # the run's player: the one who bought or pulled first
            player = next((e["p"] for e in events if e["k"] in ("pull", "buy", "join")), None)
        mine = [e for e in events if e.get("p") == player]
        for e in mine:
            k, t = e["k"], (offset + e["t"]) / 60

            def mark(key):
                milestones.setdefault(key, round(t, 2))
            if k == "buy":
                u = B.upgrades.get(e["id"])
                if u is None:
                    unknown.append(e["id"])
                elif not u["decor"]:
                    mark(e["id"])
                    order.append(e["id"])
            elif k == "hire":
                mark("hire:" + e["id"])
                order.append("hire:" + e["id"])
            elif k == "merge":
                merges += 1
                mark(f"Merge{merges}")
                order.append("MergeSlots")
            elif k == "coins" and e.get("sku") in CART:
                key = CART[e["sku"]]
                cart[key] += 1
                mark(f"{key}{cart[key]}")
                order.append(f"{key}{cart[key]}")
            elif k == "gem_buy":
                mark(f"{e['id']}{e['level']}")
                gem_order.append(e["id"])
            elif k == "letter":
                mark("Letter" + e["id"])
                quests.append(round(t, 2))
            elif k == "mail":  # a mail order handed in
                quests.append(round(t, 2))
            elif k == "sale":
                mark("FirstSale")
            elif k == "pull":
                mark("FirstPull")
            elif k == "forge_finish":
                mark("Sword1")
        offset += max((e["t"] for e in mine), default=0.0)
    return {"milestones": milestones, "order": order, "gem_order": gem_order, "played": round(offset / 60, 2),
            "unknown": sorted(set(unknown)), "player": player, "quests": quests}


def run_many(B, arche, seeds, hours, payer="free"):
    """Each seed's milestones, with its quest times (minutes) under "_quests"."""
    out = []
    for i in range(seeds):
        r = engine.simulate(B, None, payer, f"allen:{i}", hours, arche=arche)
        out.append(dict(r["milestones"], _quests=r["quests"]))
    return out


def quests_by(sims, minute):
    """The sims' median count of quests (letters and mail orders) handed in by `minute`."""
    return statistics.median(sum(1 for q in m["_quests"] if q <= minute) for m in sims)


def compare(sims, actual):
    """{key: (your minute, the sims' median, share of sims that got there)} for your milestones the sims reach in at least
    half their runs."""
    out = {}
    for key, mine in actual.items():
        got = [m[key] for m in sims if key in m and key != "_quests"]
        if len(got) * 2 >= len(sims):
            out[key] = (mine, statistics.median(got), len(got) / len(sims))
    return out


def score(sims, actual):
    """Median log(sim / you) over your milestones past MIN_ACTUAL: 0 when the sims keep your pace."""
    pairs = [(m, s) for m, s, _ in compare(sims, actual).values() if m >= MIN_ACTUAL and s > 0]
    return statistics.median(math.log(s / m) for m, s in pairs) if pairs else None


def fit_slack(B, base, actual, seeds, hours, payer="free", steps=9):
    """The slack where the sims' milestones fall at your times (bisection on log slack; more slack, later milestones)."""
    lo, hi = math.log(SLACK_RANGE[0]), math.log(SLACK_RANGE[1])
    f = lambda x: score(run_many(B, behavior.replace(base, slack=math.exp(x)), seeds, hours, payer), actual)
    s_lo, s_hi = f(lo), f(hi)
    if s_lo is None:
        raise SystemExit("no milestone of yours that the sims reach: is the run long enough (past the first sale)?")
    if s_lo >= 0:
        return math.exp(lo), s_lo
    if s_hi is not None and s_hi <= 0:
        return math.exp(hi), s_hi
    best = (math.exp(lo), s_lo)
    for _ in range(steps):
        mid = (lo + hi) / 2
        s = f(mid)
        if s is None:
            hi = mid
            continue
        best = min(best, (math.exp(mid), s), key=lambda b: abs(b[1]))
        if s < 0:
            lo = mid
        else:
            hi = mid
    return best


def fmt(m):
    if m is None:
        return "-"
    m = round(m)
    return f"{m // 60} h {m % 60:02d}" if m >= 60 else f"{m} min"


def note(name, files, run, slack, fit_score, allen_sims, new_sims, hours, seeds):
    actual = run["milestones"]
    a = compare(allen_sims, actual)
    lines = [f"# Sim run: {name}", "",
             f"Allen's recorded run as the reference player ({datetime.date.today()}; `allen.py`). Files: "
             + ", ".join(f"`{os.path.basename(p)}`" for p in files) + f". Played {fmt(run['played'])}.", "",
             f"- **Fitted pace:** slack {slack:.2f} (the sim's seconds per action x {slack:.2f} matches you; median "
             f"log ratio {fit_score:+.3f}). New player: x {behavior.NEW_PLAYER_SLACK} slower, offers as the casual type.",
             f"- **Sims:** {seeds} seeds each, {hours} h, free player, today's balance.json.",
             f"- **Quests handed in (letters and mail orders) by {fmt(run['played'])}:** you {len(run['quests'])}, Allen sim "
             f"{quests_by(allen_sims, run['played']):g}, new player sim {quests_by(new_sims, run['played']):g} (medians).",
             f"- **Your order:** {len(run['order'])} buys, {len(run['gem_order'])} gem buys."
             + (f" Not in the sim (left out): {', '.join(run['unknown'])}." if run["unknown"] else ""), "",
             "## Your milestones and the sim's", "",
             "| Milestone | You | Allen sim (median) | New player sim | Sims there |", "|---|---|---|---|---|"]
    new = {k: statistics.median([m[k] for m in new_sims if k in m]) for k in actual if any(k in m for m in new_sims)}
    for key, mine in sorted(actual.items(), key=lambda kv: kv[1]):
        sim = a.get(key)
        lines.append(f"| {key} | {fmt(mine)} | {fmt(sim[1]) if sim else '-'} | {fmt(new.get(key))} | "
                     f"{f'{sim[2]:.0%}' if sim else 'under half'} |")
    later = {}
    for m in allen_sims:
        for k, t in m.items():
            if k not in actual and k != "_quests":
                later.setdefault(k, []).append(t)
    later = sorted(((statistics.median(v), k, len(v)) for k, v in later.items() if len(v) * 2 >= len(allen_sims)))
    new_later = {}
    for m in new_sims:
        for k, t in m.items():
            if k != "_quests":
                new_later.setdefault(k, []).append(t)
    lines += ["", f"## After you stopped (the sims, to {hours} h)", "",
              "| Milestone | Allen sim (median) | New player sim (median) |", "|---|---|---|"]
    for t, k, n in later:
        nl = new_later.get(k)
        lines.append(f"| {k} | {fmt(t)} | {fmt(statistics.median(nl)) if nl and len(nl) * 2 >= len(new_sims) else 'later'} |")
    os.makedirs(NOTES, exist_ok=True)
    path = os.path.join(NOTES, f"{name}.md")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    return path


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--name", default=f"allen-{datetime.date.today()}")
    ap.add_argument("--hours", type=float, default=None, help="how far the sims run (default: twice your run, 6 h at least)")
    ap.add_argument("--seeds", type=int, default=16)
    ap.add_argument("--out", default=behavior.ALLEN_PATH)
    a = ap.parse_args(argv)
    B = rules.load()
    run = timeline(a.files, B)
    if not run["order"]:
        raise SystemExit("no purchases in these files: is this the run?")
    base = behavior.allen_profiles({"order": run["order"], "gem_order": run["gem_order"], "slack": 1.0})["allen"]
    fit_hours = run["played"] / 60 * 1.5 + 0.25
    slack, s = fit_slack(B, base, run["milestones"], max(6, a.seeds // 2), fit_hours)
    profile = {"order": run["order"], "gem_order": run["gem_order"], "slack": round(slack, 3), "files": [os.path.basename(p) for p in a.files],
               "played_min": run["played"], "fit": round(s, 4), "written": str(datetime.date.today())}
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(profile, f, indent=1)
    prof = behavior.allen_profiles(profile)
    hours = a.hours or max(6.0, round(run["played"] / 60 * 2, 1))
    allen_sims = run_many(B, prof["allen"], a.seeds, hours)
    new_sims = run_many(B, prof["newplayer"], a.seeds, hours)
    path = note(a.name, a.files, run, slack, s, allen_sims, new_sims, hours, a.seeds)
    print(f"slack {slack:.2f} (fit {s:+.3f}); wrote {a.out} and {path}")


if __name__ == "__main__":
    main(sys.argv[1:])

"""Run simulated players: every archetype x payer x scenario on the same player seeds (vault: Development/Gameplay
Simulator Plan §6), in parallel, then write the report.

python run.py --name first-look --players 300 --hours 24
python run.py --name prices --players 500 --hours 12 --archetypes casual,efficient --scenarios baseline,prices-10,prices+10

Writes results/<name>/players.jsonl (one line per simulated player), report.html and the vault note
Development/Sim Runs/<name>.md."""

import argparse
import json
import multiprocessing as mp
import os
import time

import behavior
import engine
import report
import rules
import scenarios

HERE = os.path.dirname(os.path.abspath(__file__))
_BUILT = {}
PLAYER_LIMIT = 120  # seconds of computer time per simulated player (a 24 h Manager takes ~3): past it, skipped and named


def series(minutes):
    """Cumulative coins earned: every minute to 60, then every 5 minutes."""
    return [round(m[0]) for k, m in enumerate(minutes) if k <= 60 or k % 5 == 0]


def summarize(r, extra):
    mins = r["minutes"]
    earned = [m[0] for m in mins]

    def at(k):
        return earned[min(k, len(earned) - 1)] if earned else 0

    def rate(a, b):
        a, b = max(0, a), min(len(earned) - 1, b)
        return (at(b) - at(a)) / max(1, b - a)

    buys = []
    for minute, uid, price, _ in r["purchases"]:
        k = int(minute)
        buys.append((round(minute, 2), uid, price, round(rate(k - 15, k), 1), round(rate(k, k + 15), 1)))
    progress = [0.0] + [t / 60 for t in sorted(r["progress"])] + [r["horizon_min"]]
    gaps = [(round(a, 1), round(b - a, 1)) for a, b in zip(progress, progress[1:]) if b - a >= 10]
    made = {str(k): [mins[min(k, len(mins) - 1)][3], mins[min(k, len(mins) - 1)][4]] for k in (5, 10, 15, 30, 60)}

    def loop(L):  # the player's median loop and its parts, seconds: [total, making, getting out, selling, swords]
        if not L:
            return None
        med = lambda i: sorted(x[i] for x in L)[len(L) // 2]
        return [round(med(i), 1) for i in range(4)] + [len(L)]
    first = r["milestones"].get("FirstSale")
    first_loop = round(first - r["first_pull"] / 60, 2) if first is not None and r["first_pull"] is not None else None
    return dict(extra, milestones={k: round(v, 2) for k, v in r["milestones"].items()}, earned=series(mins), made=made,
                use={k: round(v) for k, v in r["use"].items()}, crew_wait={k: round(v) for k, v in r["crew_wait"].items()},
                luck=round(r["luck"], 4), ores=r["ores"], sold=r["sold"], carted=r["carted"], missed=r["missed"], lost=r["lost"],
                browsed=r["browsed"], letters=r["letters"], own_made=r["own_made"], crew_made=r["crew_made"],
                merges=r["merges"], buys=buys, stuck=gaps, horizon=r["horizon_min"], loop_own=loop(r["loops_own"]),
                loop_crew=loop(r["loops_crew"]), first_loop=first_loop, gems_in=r["gems_in"], gems_out=r["gems_out"],
                gem_levels=r["gem_levels"], gems_left=r["gems_left"], mail_done=r["mail_done"], mail_coins=round(r["mail_coins"]),
                earned_total=round(r["earned"]), cart_bulk=r["cart_bulk"], cart_special=r["cart_special"],
                cart_skips=r["cart_skips"], reputation=r["reputation"], orders_open=r["orders_open"])


def work(job):
    scen, arche, payer, seed, hours, until_done, limit = job
    if scen not in _BUILT:
        _BUILT[scen] = scenarios.build(scen, rules.load().raw)
    B, timing = _BUILT[scen]
    try:
        r = engine.simulate(B, arche, payer, seed, hours, timing=timing, wall_limit=limit, until_done=until_done)
    except RuntimeError as e:  # the engine's stuck-loop guard: skip this player, say which, keep the run going
        return {"error": f"{scen} {arche} {payer} {seed}: {e}"}
    return summarize(r, {"scenario": scen, "archetype": arche, "payer": payer, "seed": seed})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--players", type=int, default=200)
    ap.add_argument("--hours", type=float, default=24)
    ap.add_argument("--archetypes", default=",".join(behavior.ARCHETYPES))
    ap.add_argument("--payers", default="free")
    ap.add_argument("--scenarios", default="baseline")
    ap.add_argument("--seed", default="1")
    ap.add_argument("--procs", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    ap.add_argument("--until-done", action="store_true", help="stop each player once every pad is bought (--hours caps it)")
    ap.add_argument("--player-limit", type=float, default=PLAYER_LIMIT, help="seconds of computer time per player")
    a = ap.parse_args()
    seeds = [f"{a.seed}:{i}" for i in range(a.players)]  # the same players in every scenario, archetype and payer
    jobs = [(s, ar, p, seed, a.hours, a.until_done, a.player_limit) for s in a.scenarios.split(",") for ar in a.archetypes.split(",")
            for p in a.payers.split(",") for seed in seeds]
    out_dir = os.path.join(HERE, "results", a.name)
    os.makedirs(out_dir, exist_ok=True)
    t0 = time.time()
    errors = []
    with mp.Pool(a.procs) as pool, open(os.path.join(out_dir, "players.jsonl"), "w", encoding="utf-8") as f:
        for i, res in enumerate(pool.imap_unordered(work, jobs, chunksize=4)):
            if "error" in res:
                errors.append(res["error"])
                print("SKIPPED", res["error"], flush=True)
                continue
            f.write(json.dumps(res) + "\n")
            if (i + 1) % 500 == 0:
                print(f"{i + 1}/{len(jobs)} players, {time.time() - t0:.0f} s", flush=True)
    meta = {"name": a.name, "players": a.players, "hours": a.hours, "seed": a.seed, "scenarios": a.scenarios.split(","),
            "archetypes": a.archetypes.split(","), "payers": a.payers.split(","), "seconds": round(time.time() - t0),
            "exported": rules.load().raw["exportedAt"]}
    with open(os.path.join(out_dir, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f)
    print(f"{len(jobs) - len(errors)} players in {time.time() - t0:.0f} s" + (f"; {len(errors)} skipped (stuck)" if errors else ""))
    report.write(out_dir)


if __name__ == "__main__":
    main()

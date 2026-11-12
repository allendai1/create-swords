"""Pacing of a run: how long players wait between buys (the LihFolk vault's check, 2026-10-30: "Spikes are where
players leave"; under ~2 min early, 5-10 min late). Prints a markdown table per scenario and type, medians over players.

    python pacing.py <run> [scenario,...] [type,...]
"""
import json
import os
import statistics as st
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
INF = float("inf")


def fmt(m):
    return "never" if m == INF else f"{int(m // 60)}:{int(m % 60):02d}"


def player(p):
    buys = [b[0] for b in p["buys"]]
    gaps = [b - a for a, b in zip([0.0] + buys, buys)]
    end = buys[-1] if buys else 0
    per_hour = [sum(1 for t in buys if h * 60 <= t < (h + 1) * 60) for h in range(int(end // 60))]  # full hours with buys left
    return dict(crafter=p["milestones"].get("Crafter", INF), seraph=p["milestones"].get("SeraphBlueprint", INF), done=end,
                worst=min(per_hour[1:], default=0), long=sum(g > 15 for g in gaps), longest=max(gaps, default=0))


def main(run, scens=None, types=None):
    G = defaultdict(list)
    for line in open(os.path.join(HERE, "results", run, "players.jsonl"), encoding="utf-8"):
        p = json.loads(line)
        if (not scens or p["scenario"] in scens) and (not types or p["archetype"] in types):
            G[(p["scenario"], p["archetype"])].append(player(p))
    print("| scenario | type | Swordsmith | Seraph | last pad | fewest buys in an hour | waits over 15 min | longest wait |")
    print("|---|---|---|---|---|---|---|---|")
    for (s, a), g in G.items():
        med = lambda k: st.median(x[k] for x in g)
        print(f"| {s} | {a} | {fmt(med('crafter'))} | {fmt(med('seraph'))} | {fmt(med('done'))} | {med('worst'):.0f} | "
              f"{med('long'):.0f} | {med('longest'):.0f} min |")


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], a[1].split(",") if len(a) > 1 else None, a[2].split(",") if len(a) > 2 else None)

"""Median minute of each milestone by scenario and type, for a run in results/<name>. python summarize_run.py <name> [types]"""
import collections
import json
import sys

G = [("KatanaBlueprint", "Katana"), ("LongswordBlueprint", "Longsw"), ("Crafter", "Crafter"), ("JianBlueprint", "Jian"),
     ("FalchionBlueprint", "Falch"), ("DadaoBlueprint", "Dadao"), ("BigSwordStand", "BigStand"), ("ZanbatoBlueprint", "Zanb"),
     ("GladiusBlueprint", "Gladius"), ("hire:rin", "Taru"), ("SeraphBlueprint", "Seraph")]


def fmt(m):
    return "   —" if m >= 1e8 else f"{int(m) // 60}:{int(m) % 60:02d}"


if __name__ == "__main__":
    name = sys.argv[1]
    types = sys.argv[2].split(",") if len(sys.argv) > 2 else ["efficient", "grinder", "manager", "casual"]
    by = collections.defaultdict(list)
    for line in open(f"results/{name}/players.jsonl", encoding="utf-8"):
        r = json.loads(line)
        by[(r["scenario"], r["archetype"])].append(r)
    scen = list(dict.fromkeys(s for s, _ in by))
    print(" " * 18 + " ".join(f"{n:>8}" for _, n in G))
    for a in types:
        print("==", a)
        for s in scen:
            rs = by[(s, a)]
            med = lambda k: sorted(r["milestones"].get(k, 1e9) for r in rs)[len(rs) // 2]
            print(f"{s:18}" + " ".join(f"{fmt(med(k)):>8}" for k, _ in G))

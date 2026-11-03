"""Vault note: the median time each player type reaches each purchase, for one or more runs/scenarios.
python purchase_times.py <out.md> <run>:<scenario>:<title> ..."""
import collections
import json
import sys

import scenarios

TYPES = ["casual", "efficient", "automator", "rusher", "grinder", "manager"]
SKIP = {"FirstPull", "Sword1", "GemsAllLv1", "MergeSlots", "LetterIronTanto", "LetterKatana"}
CREW = {"haru": "Haru (2nd crafter)", "mei": "Mei (3rd crafter)", "kenji": "Kenji (4th crafter)", "rin": "Taru (5th crafter)"}
GEM = {"Advertising": "Better Advertising", "Vip": "More VIPs", "Clients": "More Clients", "Mail": "Quicker Mail"}


def label(k, names):
    if k in names:
        return names[k]
    if k.startswith("hire:"):
        return CREW.get(k[5:], k[5:].capitalize())
    if k.startswith("Merge"):
        n = int(k[5:])
        return f"Merge {n}"
    if k[:3] in ("Cap", "Spd") and k[3:].isdigit():
        return ("Cart capacity " if k[:3] == "Cap" else "Cart speed ") + k[3:]
    for p, n in GEM.items():
        if k.startswith(p) and k[len(p):].isdigit():
            return f"{n} {k[len(p):]} (gems)"
    return {"FirstSale": "First sale", "TutorialDone": "Tutorial done", "AllPads": "Every pad bought"}.get(k, k)


def fmt(m):
    return "—" if m is None else (f"{int(m)} min" if m < 60 else f"{int(m) // 60}:{int(m) % 60:02d}")


def table(run, scen):
    by = collections.defaultdict(list)
    for line in open(f"results/{run}/players.jsonl", encoding="utf-8"):
        r = json.loads(line)
        if r["scenario"] == scen:
            by[r["archetype"]].append(r["milestones"])
    keys = {k for rs in by.values() for m in rs for k in m} - SKIP
    med = {}
    for a, rs in by.items():
        for k in keys:
            v = sorted(m.get(k, 1e9) for m in rs)
            x = v[len(v) // 2]
            med[(a, k)] = None if x >= 1e8 else x
    return med, keys


if __name__ == "__main__":
    out, specs = sys.argv[1], sys.argv[2:]
    raw = json.load(open("balance.json", encoding="utf-8"))
    names = {u["id"]: u["name"] for u in raw["upgrades"]}
    lines = []
    for spec in specs:
        run, scen, title = spec.split(":", 2)
        B, _ = scenarios.build(scen, raw)
        price = {u["id"]: u["price"] for u in B.raw["upgrades"]} | {f"hire:{c['id']}": c.get("coins") for c in B.raw["employees"]["crafters"]}
        med, keys = table(run, scen)
        order = sorted(keys, key=lambda k: (med.get(("efficient", k)) or 1e9, min((med.get((a, k)) or 1e9) for a in TYPES)))
        lines += [f"## {title}", "", f"Run `{run}`, scenario `{scen}`: median of 100 free players per type (— = fewer than half got there).", "",
                  "| Purchase | Price | " + " | ".join(t.capitalize() for t in TYPES) + " |", "|---|---|" + "---|" * len(TYPES)]
        for k in order:
            p = price.get(k)
            lines.append(f"| {label(k, names)} | {p:,} | " if p else f"| {label(k, names)} | | ")
            lines[-1] += " | ".join(fmt(med.get((a, k))) for a in TYPES) + " |"
        lines.append("")
    with open(out, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(lines))

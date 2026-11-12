"""Upgrade tree page for Sell Swords!: reads the exported balance and the latest sim run, lays the pads out left to right
by how many buys deep they sit (layout runs in the page, so rewiring re-lays it), and writes Development/Upgrade Tree.html (data + layout baked in).
    python build_tree.py [run]   (run: a folder in sim/results for the sim's times)
Then publish that page with the Artifact tool to https://claude.ai/artifact/UNFWP14KsNwNwFdJEpaQnD (Allen's, private)."""
import json
import os
import sys

SIM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Development/sim
OUT = os.path.join(os.path.dirname(SIM), "Upgrade Tree.html")
RUN = sys.argv[1] if len(sys.argv) > 1 else "prices-recheck-2026-11-10"

b = json.load(open(os.path.join(SIM, "balance.json"), encoding="utf-8"))

STAFF = {"Cashier", "Promoter", "Stocker", "Etcher"}


def cat(u):
    i = u["id"]
    if u.get("blueprint"):
        return "sword"
    if i in STAFF:
        return "staff"
    if i.startswith(("OreStand", "MergeSlots")):
        return "ore"
    if i.startswith(("Heat", "F2Heat", "F3Heat", "Furnace")):
        return "heat"
    if i.startswith(("Anvil", "Crafter")) or i.startswith("hire:"):
        return "crew"
    if i.startswith(("IngotRack", "SwordRack")):
        return "storage"
    if i.startswith(("WallRack", "DisplayTable", "BigSwordStand", "UpgradedStore")):
        return "shop"
    if i.startswith(("PolishStation", "EtchingTable", "PolishBoost", "Strikes")):
        return "stations"
    return "cart"


nodes = {}
for u in b["upgrades"]:
    if u["decor"]:
        continue
    nodes[u["id"]] = dict(id=u["id"], name=u["name"].replace(" Sword", "") if u.get("blueprint") else u["name"],
                          price=u["price"], after=list(u["after"]), cat=cat(u))
nodes["MergeSlots"]["name"] = "Merge Ore Slots"
for c in b["employees"]["crafters"]:
    if c["id"] == b["employees"]["first"]:
        continue
    a = c["after"]
    a = f"hire:{a}" if a in {x["id"] for x in b["employees"]["crafters"]} else a
    nodes[f"hire:{c['id']}"] = dict(id=f"hire:{c['id']}", name=f"Hire {c['name'] if 'name' in c else c['id'].capitalize()}",
                                    price=c["coins"], after=[a], cat="crew", gems=c.get("gems"))
nodes["Crafter"]["name"] = "Swordsmith (1st hire)"

# medians from the sim run (minutes), efficient and casual
times = {}
path = os.path.join(SIM, "results", RUN, "players.jsonl")
by = {}
for line in open(path, encoding="utf-8"):
    r = json.loads(line)
    if r["scenario"] == "baseline":
        by.setdefault(r["archetype"], []).append(r["milestones"])
for a in ("efficient", "casual"):
    rs = by[a]
    for i in nodes:
        v = sorted(m.get(i, 1e9) for m in rs)
        x = v[len(v) // 2]
        nodes[i].setdefault("t", {})[a] = None if x >= 1e8 else round(x)

assert all(a in nodes for n in nodes.values() for a in n["after"]), "every prerequisite is a node"
data = json.dumps(list(nodes.values()), ensure_ascii=False, separators=(",", ":"))
html = open(os.path.join(os.path.dirname(__file__), "template.html"), encoding="utf-8").read()
open(OUT, "w", encoding="utf-8", newline="").write(html.replace("/*DATA*/[]", data).replace("{{RUN}}", RUN))
print(len(nodes), "nodes")

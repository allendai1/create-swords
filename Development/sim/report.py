"""The simulation report (vault: Development/Gameplay Simulator Plan §7): seven metrics by scenario, archetype and payer,
and scenario-vs-baseline comparisons on the same players. Writes report.html beside players.jsonl and a short vault note
in Development/Sim Runs/. python report.py results/<name> rebuilds both."""

import html
import json
import math
import os
import random
import sys
from collections import defaultdict

import behavior
import pacing
import timings

HERE = os.path.dirname(os.path.abspath(__file__))
VAULT_RUNS = os.path.join(os.path.dirname(HERE), "Sim Runs")
INF = math.inf
# Allen's targets (2026-10-29): Economy Pass 2's stages, then the Seraph at about 20 h, for a casual player
# Minutes of play for a casual player (Allen 2026-10-29: Katana 15 min, Longsword 40 min, Sword Crafter 1 h 30, and "Use
# the proposed targets as they are" for the rest: the crew, staff, merges and gem levels; the Falchion, Gladius,
# Zanbatō and Seraph unchanged). Gem levels are engine.gem_milestones; at an hour a day, hours are days.
# The Zanbatō 8 h -> 4 h (Allen 2026-10-30: "make the zanbato target of say 4 hours instead of 8").
# The main point is the Sword Crafter, not the Zanbatō (Allen 2026-10-30: "i dont want zanbato to necessarily be the main
# point to track", "Yes track the sword crafter"), with waits over 15 min between buys for the rest of the game.
# The Sword Crafter at about 15 min since 2026-11-02 (Allen, after Create Pottery's Apprentice; was 1 h 30).
HEADLINE = "Crafter"
TARGETS = {"KatanaBlueprint": 15, "Crafter": 15, "LongswordBlueprint": 40, "Merge1": 120, "hire:haru": 180, "GemsAllLv1": 180,
           "Stocker": 210, "FalchionBlueprint": 240, "Merge2": 240, "hire:mei": 360, "GladiusBlueprint": 380, "Promoter": 400,
           "Merge3": 420, "Cashier": 450, "ZanbatoBlueprint": 240, "Etcher": 510, "GemPairLv3": 600, "hire:kenji": 630,
           "hire:rin": 750, "SeraphBlueprint": 1200, "GemPairLv5": 1200}
NAMES = {"KatanaBlueprint": "Katana", "LongswordBlueprint": "Longsword", "Crafter": "Sword Crafter", "Merge1": "1st merge",
         "hire:haru": "Haru (2nd crafter)", "GemsAllLv1": "Gems: all Lv. 1", "Stocker": "Stocker", "FalchionBlueprint": "Falchion",
         "Merge2": "2nd merge", "hire:mei": "Mei (3rd crafter)", "GladiusBlueprint": "Gladius", "Promoter": "Shop Promoter",
         "Merge3": "3rd merge", "Cashier": "Cashier", "ZanbatoBlueprint": "Zanbatō", "Etcher": "Sword Etcher",
         "GemPairLv3": "Gems: own pair Lv. 3", "hire:kenji": "Kenji (4th crafter)", "hire:rin": "Taru (5th crafter)",
         "SeraphBlueprint": "Seraph", "GemPairLv5": "Gems: a pair Lv. 5"}


def name(m):
    return NAMES.get(m, m.replace("Blueprint", ""))


BY = [5, 10, 15, 30, 60, 120, 300, 600, 1200]
CHECK = [5, 10, 15, 30, 60, 120, 240, 480, 720, 960, 1200, 1440]
STUCK = 10  # minutes without a purchase, unlock, hire or merge


def pct(xs, p):
    """p-th percentile (0-100) with inf for never; nearest rank."""
    if not xs:
        return None
    s = sorted(xs)
    return s[min(len(s) - 1, max(0, math.ceil(p / 100 * len(s)) - 1))]


def fmt_min(m):
    if m is None or m == INF:
        return "—"
    return f"{m:.0f} min" if m < 60 else f"{int(m // 60)} h {int(m % 60):02d}"


def series_minute(k):
    return k if k <= 60 else 60 + 5 * (k - 60)


def earned_at(p, minute):
    s = p["earned"]
    if minute <= 60:
        k = int(minute)
    else:
        k = 60 + int((minute - 60) // 5)
    return s[min(k, len(s) - 1)]


def income(p, a, b):
    return (earned_at(p, b) - earned_at(p, a)) / max(1, b - a)


def load(out_dir):
    with open(os.path.join(out_dir, "meta.json"), encoding="utf-8") as f:
        meta = json.load(f)
    with open(os.path.join(out_dir, "players.jsonl"), encoding="utf-8") as f:
        players = [json.loads(line) for line in f]
    return meta, players


def groups(players):
    g = defaultdict(list)
    for p in players:
        g[(p["scenario"], p["archetype"], p["payer"])].append(p)
    for k in g:
        g[k].sort(key=lambda p: p["seed"])
    return g


def milestone_ids(players):
    seen = defaultdict(int)
    for p in players:
        for k in p["milestones"]:
            seen[k] += 1
    first = defaultdict(list)
    for p in players:
        for k, v in p["milestones"].items():
            first[k].append(v)
    return sorted(seen, key=lambda k: pct(first[k], 50))


def when(p, key):
    return p["milestones"].get(key, INF)


def bootstrap(diffs, n=1000, seed=0):
    r = random.Random(seed)
    meds = sorted(pct([r.choice(diffs) for _ in diffs], 50) for _ in range(n))
    return meds[int(0.025 * n)], meds[int(0.975 * n) - 1]


# ------------------------------------------------------------------------------------------------- html bits
def table(head, rows, cls=""):
    h = "".join(f"<th>{html.escape(str(x))}</th>" for x in head)
    b = "".join("<tr>" + "".join(f"<td>{x}</td>" for x in r) + "</tr>" for r in rows)
    return f'<table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>'


def chart(lines, title, ymax=None):
    """lines: [(label, [(minute, value)], colour)] -> an inline SVG line chart, x in hours."""
    W, H, L, B = 760, 280, 60, 30
    xs = [x for _, pts, _ in lines for x, _ in pts]
    ys = [y for _, pts, _ in lines for _, y in pts]
    if not xs:
        return ""
    xmax, ymax = max(xs) or 1, ymax or (max(ys) or 1) * 1.05
    X = lambda x: L + (W - L - 10) * x / xmax
    Y = lambda y: H - B - (H - B - 10) * y / ymax
    out = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="{html.escape(title)}">']
    for i in range(5):
        y = ymax * i / 4
        out.append(f'<line x1="{L}" x2="{W - 10}" y1="{Y(y):.1f}" y2="{Y(y):.1f}" class="grid"/><text x="{L - 6}" y="{Y(y) + 4:.1f}" class="ax" text-anchor="end">{y:,.0f}</text>')
    for h in range(0, int(xmax / 60) + 1, max(1, int(xmax / 60 / 8))):
        out.append(f'<text x="{X(h * 60):.1f}" y="{H - 8}" class="ax" text-anchor="middle">{h} h</text>')
    for label, pts, colour in lines:
        d = " ".join(f"{X(x):.1f},{Y(y):.1f}" for x, y in pts)
        out.append(f'<polyline points="{d}" fill="none" stroke="{colour}" stroke-width="2"/>')
    out.append("</svg>")
    legend = " ".join(f'<span class="key" style="--c:{c}"></span>{html.escape(l)}' for l, _, c in lines)
    return f'<figure><figcaption>{html.escape(title)}</figcaption>{"".join(out)}<div class="legend">{legend}</div></figure>'


COLOURS = ["#2a6fdb", "#d1495b", "#2e9e5b", "#e8a33d", "#7b4fd6", "#4a4a4a", "#13a4b4", "#b5651d"]

CSS = """
:root { --bg:#fbfaf7; --fg:#1d1d1f; --mut:#6b6b70; --line:#e2dfd8; --head:#f1eee7; }
@media (prefers-color-scheme: dark) { :root { --bg:#17171a; --fg:#ececee; --mut:#a0a0a8; --line:#33333a; --head:#222227; } }
body { background:var(--bg); color:var(--fg); font:14px/1.45 system-ui, sans-serif; margin:0 auto; padding:16px; max-width:1100px; }
h1 { font-size:22px; } h2 { font-size:18px; margin-top:28px; border-bottom:1px solid var(--line); padding-bottom:4px; }
h3 { font-size:15px; margin-top:18px; } p.note, .mut { color:var(--mut); }
table { border-collapse:collapse; margin:8px 0 14px; font-size:13px; display:block; overflow-x:auto; }
th, td { border:1px solid var(--line); padding:3px 7px; text-align:right; white-space:nowrap; }
th { background:var(--head); } td:first-child, th:first-child { text-align:left; }
.good { color:#2e9e5b; } .bad { color:#d1495b; }
figure { margin:10px 0; } figcaption { font-weight:600; margin-bottom:4px; }
svg.chart { width:100%; max-width:760px; height:auto; } .grid { stroke:var(--line); } .ax { fill:var(--mut); font-size:11px; }
.key { display:inline-block; width:12px; height:3px; background:var(--c); margin:0 4px 3px 10px; }
"""


def write(out_dir):
    meta, players = load(out_dir)
    G = groups(players)
    keys = sorted(G, key=lambda k: (k[0] != "baseline", k[0], meta["archetypes"].index(k[1]) if k[1] in meta["archetypes"] else 9, k[2]))
    horizon = meta["hours"] * 60
    label = lambda k: f"{k[1]} · {k[2]}" + ("" if k[0] == "baseline" else f" · {k[0]}")
    base = [k for k in keys if k[0] == keys[0][0]]
    ms = milestone_ids(players)
    parts = [f"<h1>Simulation: {html.escape(meta['name'])}</h1>",
             f"<p class='note'>{meta['players']} players per group × {len(meta['archetypes'])} archetypes × {len(meta['payers'])} payer tiers × "
             f"{len(meta['scenarios'])} scenarios, {meta['hours']:g} h of play each, seed {html.escape(meta['seed'])}, {meta['seconds']} s. "
             f"Game data exported from Studio at {meta['exported']} (balance.json). Times are minutes of play.</p>"]

    # 1. milestones
    parts.append("<h2>1. Time to each milestone</h2><h3>The targets (median, with the 10th–90th percentile)</h3>")
    rows = []
    for m, target in TARGETS.items():
        row = [f"{name(m)}<br><span class='mut'>target {fmt_min(target)}</span>"]
        for k in base:
            xs = [when(p, m) for p in G[k]]
            med = pct(xs, 50)
            cls = "" if med == INF else ("good" if med <= target * 1.15 else "bad" if med > target * 1.5 else "")
            row.append(f'<span class="{cls}">{fmt_min(med)}</span><br><span class="mut">{fmt_min(pct(xs, 10))} – {fmt_min(pct(xs, 90))}</span>')
        rows.append(row)
    parts.append(table(["milestone"] + [label(k) for k in base], rows))
    parts.append("<h3>Share of players who have it by…</h3>")
    for m in TARGETS:
        rows = []
        for k in base:
            g = G[k]
            xs = [when(p, m) for p in g]
            rows.append([label(k)] + [f"{sum(x <= b for x in xs) / len(xs) * 100:.0f}%" for b in BY if b <= horizon] + [f"{sum(x == INF for x in xs) / len(xs) * 100:.0f}%"])
        parts.append(f"<p><b>{name(m)}</b></p>" + table(["group"] + [fmt_min(b) for b in BY if b <= horizon] + ["never"], rows))
    parts.append("<h3>Every milestone (median; P25–P75; % reaching it)</h3>")
    rows = []
    for m in ms:
        row = [m]
        for k in base:
            xs = [when(p, m) for p in G[k]]
            row.append(f"{fmt_min(pct(xs, 50))}<br><span class='mut'>{fmt_min(pct(xs, 25))}–{fmt_min(pct(xs, 75))} · {sum(x < INF for x in xs) / len(xs) * 100:.0f}%</span>")
        rows.append(row)
    parts.append(table(["milestone"] + [label(k) for k in base], rows))

    # 2. crafting
    parts.append("<h2>2. Swords made</h2>")
    rows = []
    for k in base:
        g = G[k]
        row = [label(k)]
        for t in ("5", "10", "15", "30", "60"):
            own = [p["made"][t][0] for p in g]
            crew = [p["made"][t][1] for p in g]
            row.append(f"{pct(own, 50)} + {pct(crew, 50)}<br><span class='mut'>{pct(own, 10)}–{pct(own, 90)}</span>")
        own_rate = [p["horizon"] * 60 / p["own_made"] for p in g if p["own_made"]]
        row.append(f"{pct(own_rate, 50):.0f} s")
        rows.append(row)
    parts.append("<p class='note'>Yours + the crew's by each time (median; yours P10–P90), and played seconds per sword of your own.</p>")
    parts.append(table(["group", "5 min", "10 min", "15 min", "30 min", "60 min", "s / own sword"], rows))
    cats = sorted({c for p in players for c in p["use"]})
    rows = []
    for k in base:
        g = G[k]
        tot = sum(sum(p["use"].values()) for p in g) or 1
        rows.append([label(k)] + [f"{sum(p['use'].get(c, 0) for p in g) / tot * 100:.0f}%" for c in cats])
    parts.append("<p class='note'>Where the player's time goes (each task's walk included).</p>" + table(["group"] + cats, rows))

    # 2b. the loop
    parts.append("<h2>2b. The loop: ore to sale</h2><p class='note'>The first loop: from the first lever pull to the first sale "
                 "(minutes). Then every sold sword's loop (each player's median, seconds), in three parts: <b>making</b> (ore collected "
                 "→ forged, furnace waits included), <b>getting out</b> (forged → on a holder: finishing and walking) and <b>selling</b> "
                 "(on the holder → sold). The crew's run from the ingot fetched off the rack; their getting out is the wait on the "
                 "Finished Sword Rack.</p>")
    rows = []
    for k in base:
        g = G[k]
        fl = [p["first_loop"] for p in g if p.get("first_loop") is not None]
        row = [label(k), f"{pct(fl, 50):.1f}<br><span class='mut'>{pct(fl, 10):.1f}–{pct(fl, 90):.1f}</span>" if fl else "—"]
        for key in ("loop_own", "loop_crew"):
            L = [p[key] for p in g if p.get(key)]
            if not L:
                row += ["—"] * 4
                continue
            for i in range(4):
                xs = [x[i] for x in L]
                row.append(f"{pct(xs, 50):.0f}<br><span class='mut'>{pct(xs, 10):.0f}–{pct(xs, 90):.0f}</span>")
        rows.append(row)
    parts.append(table(["group", "first loop (min)", "yours: total s", "making", "getting out", "selling",
                        "crew: total s", "making", "rack wait", "selling"], rows))

    # 3. income
    parts.append("<h2>3. Income</h2>")
    rows = []
    for k in base:
        g = G[k]
        row = [label(k)]
        for t in CHECK:
            if t > horizon:
                continue
            a = max(0, t - 10) if t <= 60 else t - 30
            xs = [income(p, a, t) for p in g]
            row.append(f"{pct(xs, 50):,.0f}<br><span class='mut'>{pct(xs, 10):,.0f}–{pct(xs, 90):,.0f}</span>")
        rows.append(row)
    parts.append("<p class='note'>Coins a minute (over the 10 minutes before, or 30 after the first hour): median, P10–P90.</p>")
    parts.append(table(["group"] + [fmt_min(t) for t in CHECK if t <= horizon], rows))
    free = [k for k in base if k[2] == base[0][2]]
    lines = []
    for i, k in enumerate(free):
        pts = []
        for t in range(10, int(horizon) + 1, 10 if horizon <= 120 else 30):
            pts.append((t, pct([income(p, t - 10, t) for p in G[k]], 50)))
        lines.append((k[1], pts, COLOURS[i % len(COLOURS)]))
    parts.append(chart(lines, f"Median coins a minute ({base[0][2]})"))

    # 4. purchases
    parts.append("<h2>4. Purchases: cost against income</h2><p class='note'>For each purchase, at the moment it's bought: its price in "
                 "minutes of the player's income (the 15 minutes before), and minutes to pay back (price ÷ the rise in income over the "
                 "next 15 minutes; only where income rose). Median; % of players who bought it.</p>")
    for k in base[:6]:
        by_id = defaultdict(list)
        for p in G[k]:
            for minute, uid, price, before, after in p["buys"]:
                by_id[uid].append((minute, price, before, after))
        rows = []
        for uid, xs in sorted(by_id.items(), key=lambda kv: pct([x[0] for x in kv[1]], 50)):
            cost = [x[1] / x[2] for x in xs if x[2] > 0]
            pay = [x[1] / (x[3] - x[2]) for x in xs if x[3] > x[2]]
            rows.append([uid, f"{len(xs) / len(G[k]) * 100:.0f}%", fmt_min(pct([x[0] for x in xs], 50)), f"{xs[0][1]:,}",
                         f"{pct(cost, 50):.0f}" if cost else "—", f"{pct(pay, 50):.0f}" if pay else "—"])
        parts.append(f"<h3>{label(k)}</h3>" + table(["purchase", "bought", "median at", "price", "min of income", "payback min"], rows, "small"))

    # 5. stuck
    parts.append(f"<h2>5. Stuck time ({STUCK}+ minutes without a purchase, unlock, hire or merge)</h2>")
    rows = []
    for k in base:
        g = G[k]
        n = [len([s for s in p["stuck"] if s[0] + s[1] < p["horizon"]]) for p in g]
        longest = [max([s[1] for s in p["stuck"]], default=0) for p in g]
        first_hour = sum(any(s[0] < 60 for s in p["stuck"]) for p in g) / len(g) * 100
        bins = []
        for h0 in (0, 1, 2, 4, 8, 12, 16, 20):
            if h0 * 60 >= horizon:
                break
            h1 = {0: 1, 1: 2, 2: 4, 4: 8, 8: 12, 12: 16, 16: 20, 20: 24}[h0]
            share = sum(sum(max(0, min(s[0] + s[1], h1 * 60) - max(s[0], h0 * 60)) for s in p["stuck"]) for p in g) / (len(g) * (h1 - h0) * 60)
            bins.append(f"{share * 100:.0f}%")
        rows.append([label(k), pct(n, 50), fmt_min(pct(longest, 50)), f"{first_hour:.0f}%"] + bins)
    parts.append("<p class='note'>Stretches per player (closed ones), the longest (median), players stuck at some point in the first hour, "
                 "and the share of play spent stuck in each period (0–1 h, 1–2 h, 2–4 h, 4–8 h, …).</p>")
    parts.append(table(["group", "stretches", "longest", "in hour 1", "0–1 h", "1–2 h", "2–4 h", "4–8 h", "8–12 h", "12–16 h", "16–20 h", "20–24 h"], rows))

    # 6. luck
    parts.append("<h2>6. Ore luck</h2><p class='note'>A player's luck: the value of every ore they rolled against the odds' expectation "
                 "(1.00 = average). Milestones for the unluckiest and luckiest tenth of the same group.</p>")
    rows = []
    for k in base:
        g = sorted(G[k], key=lambda p: p["luck"])
        tenth = max(1, len(g) // 10)
        lo, hi = g[:tenth], g[-tenth:]
        row = [label(k), f"{pct([p['luck'] for p in g], 10):.2f} / {pct([p['luck'] for p in g], 50):.2f} / {pct([p['luck'] for p in g], 90):.2f}"]
        for m in ("Crafter", "LongswordBlueprint", "ZanbatoBlueprint"):
            row.append(f"{fmt_min(pct([when(p, m) for p in lo], 50))} vs {fmt_min(pct([when(p, m) for p in hi], 50))}")
        rows.append(row)
    parts.append(table(["group", "luck P10 / P50 / P90", "Crafter: unlucky vs lucky", "Longsword", "Zanbatō"], rows))
    ores = [sum(p["ores"][i] for p in players) for i in range(len(players[0]["ores"]))]
    tot = sum(ores) or 1
    parts.append("<p>Every ore rolled, by rarity: " + ", ".join(f"{n / tot * 100:.2f}%" for n in ores) + " (Common → Secret).</p>")

    # 7. waiting
    parts.append("<h2>7. Waiting and lost sales</h2>")
    whys = sorted({w for p in players for w in p["crew_wait"]})
    rows = []
    for k in base:
        g = G[k]
        rows.append([label(k)] + [f"{pct([p['crew_wait'].get(w, 0) / 60 for p in g], 50):.0f}" for w in whys]
                    + [pct([p["missed"] for p in g], 50), pct([p["browsed"] for p in g], 50), pct([p["sold"] for p in g], 50),
                       pct([p["carted"] for p in g], 50), pct([p["lost"] for p in g], 50)])
    parts.append("<p class='note'>Crew minutes spent waiting, by reason (summed over crafters; median), offers missed, walk-ins to an empty "
                 "shop, swords sold and sent by cart, customers who walked off.</p>")
    parts.append(table(["group"] + [f"crew: {w}" for w in whys] + ["missed offers", "empty-shop visits", "sold", "carted", "walked off"], rows))

    # 8. gems, mail and the cart
    parts.append("<h2>8. Gems, mail orders and the cart</h2>")
    srcs, sinks = ["daily", "letters", "mail", "cart", "starter"], ["Advertising", "Vip", "Clients", "Mail", "hires"]
    rows = []
    for k in base:
        g = G[k]
        rows.append([label(k)] + [pct([p["gems_in"].get(s, 0) for p in g], 50) for s in srcs]
                    + [pct([p["gems_out"].get(s, 0) for p in g], 50) for s in sinks] + [pct([p["gems_left"] for p in g], 50)]
                    + ["/".join(str(pct([p["gem_levels"][x] for p in g], 50)) for x in sinks[:4])])
    parts.append("<p class='note'>Gems by where they came from and what they bought (median over the run), what's left, and the "
                 "gem shop levels reached (Advertising / VIPs / Clients / Mail). A day is "
                 f"{behavior.PLAY_DAY // 60} min of play: one daily reward each.</p>")
    parts.append(table(["group"] + [f"in: {s}" for s in srcs] + [f"out: {s}" for s in sinks] + ["left", "levels"], rows))
    rows = []
    for k in base:
        g = G[k]
        rows.append([label(k), pct([p["mail_done"] for p in g], 50),
                     f"{pct([p['mail_coins'] / max(1, p['earned_total']) * 100 for p in g], 50):.0f}%",
                     pct([p["orders_open"] for p in g], 50), pct([p["cart_bulk"] for p in g], 50),
                     pct([p["cart_special"] for p in g], 50), pct([p["cart_skips"] for p in g], 50), pct([p["reputation"] for p in g], 50)])
    parts.append("<p class='note'>Mail orders handed in, their share of all coins earned, orders still open at the end, cart "
                 "trips (Bulk / Special), offers skipped at the board, and reputation points (median).</p>")
    parts.append(table(["group", "mail orders", "mail share of coins", "open at end", "cart: bulk", "cart: special", "skips",
                        "reputation"], rows))

    # comparisons
    others = [s for s in meta["scenarios"] if s != keys[0][0]]
    if others:
        parts.append(f"<h2>Scenarios against {keys[0][0]}</h2><p class='note'>The same players (seeds) in both. Median change in minutes "
                     "(players who reach it in both), with its bootstrap 95% interval, and the change in the share who reach it by the "
                     "target time. <b>Meaningful</b>: the interval excludes 0 and the change is at least 5 minutes and 5%.</p>")
        for s in others:
            rows = []
            for k in base:
                sk = (s, k[1], k[2])
                if sk not in G:
                    continue
                a, b = {p["seed"]: p for p in G[k]}, {p["seed"]: p for p in G[sk]}
                row = [label(k)]
                for m, target in TARGETS.items():
                    d = [when(b[x], m) - when(a[x], m) for x in a if x in b and when(a[x], m) < INF and when(b[x], m) < INF]
                    reach = (sum(when(b[x], m) <= target for x in b) - sum(when(a[x], m) <= target for x in a)) / max(1, len(a)) * 100
                    if len(d) < 10:
                        row.append("—")
                        continue
                    med, (lo, hi) = pct(d, 50), bootstrap(d)
                    base_med = pct([when(a[x], m) for x in a], 50)
                    real = (lo > 0 or hi < 0) and abs(med) >= 5 and (base_med == INF or abs(med) >= 0.05 * base_med)
                    cls = ("good" if med < 0 else "bad") if real else "mut"
                    row.append(f'<span class="{cls}">{med:+.0f} min</span><br><span class="mut">[{lo:+.0f}, {hi:+.0f}] · {reach:+.0f} pts</span>')
                rows.append(row)
            parts.append(f"<h3>{html.escape(s)}</h3>" + table(["group"] + [name(m) for m in TARGETS], rows))

    parts.append("<h2>Assumptions in this run</h2><p class='note'>Hand-action seconds (* measured in playtests, the rest ESTIMATE): "
                 + ", ".join(f"{k} {v:g}{'*' if k in timings.MEASURED else ''}" for k, v in timings.T.items()) +
                 ". Archetypes, haggling (off), what each keeps from the ore box, how it treats mail orders, its gem shop order and "
                 "how often it idles are in behavior.py. Not modelled: declining mail orders, Robux currency packs, the "
                 "workshop push, the crew forging for Special Orders; offline, only the cart and the mail run.</p>")
    page = f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>Sim {html.escape(meta['name'])}</title><style>{CSS}</style></head><body>{''.join(parts)}</body></html>"
    path = os.path.join(out_dir, "report.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(page)
    note(meta, G, base, out_dir)
    print("report:", path)
    return path


def note(meta, G, base, out_dir):
    """A short vault note: the targets table and where the full report is."""
    os.makedirs(VAULT_RUNS, exist_ok=True)
    lines = [f"# Sim run: {meta['name']}", "",
             f"{meta['players']} players per group, {meta['hours']:g} h each; archetypes {', '.join(meta['archetypes'])}; payers "
             f"{', '.join(meta['payers'])}; scenarios {', '.join(meta['scenarios'])}; seed {meta['seed']}. Full report: "
             f"`Development/sim/results/{meta['name']}/report.html` (not in git). Hand-action times: "
             + (f"measured in playtests for {', '.join(timings.MEASURED)}, the rest estimates" if timings.MEASURED else "estimates")
             + " ([[Development/Gameplay Simulator Plan]]).", "",
             "Main point, median (`pacing.py` for more):"]
    lines += [f"- **{k[1]} · {k[2]}:** Sword Crafter {fmt_min(pct([when(p, HEADLINE) for p in G[k]], 50))}, "
              f"{pct([pacing.player(p)['long'] for p in G[k]], 50):.0f} waits over 15 min between buys" for k in base]
    lines += ["", "Median time to each target, by payer (10th–90th percentile in the full report):"]
    for payer in dict.fromkeys(k[2] for k in base):
        ks = [k for k in base if k[2] == payer]
        lines += ["", f"**{payer}**", "", "| Milestone | Target | " + " | ".join(k[1] for k in ks) + " |",
                  "|---|---|" + "---|" * len(ks)]
        for m, target in TARGETS.items():
            lines.append(f"| {name(m)} | {fmt_min(target)} | " + " | ".join(fmt_min(pct([when(p, m) for p in G[k]], 50)) for k in ks) + " |")
    with open(os.path.join(VAULT_RUNS, f"{meta['name']}.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    write(sys.argv[1])

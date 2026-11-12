---
tags: [sim, create-swords]
---
# Buy chance (More Sales), 2026-11-10

`python Development/sim/buy_chance.py 8 20`: 8 seeds, 20 h, free players. Each case sets every More Sales level's buy chance; polish and etch add the bonus. "passed": walk-ins that passed on a sword (median per run). "Sales5": when More Sales reached Lv. 5 (none did in 20 h).

```
casual, free, 8 seeds, 20 h (h:mm)
case                  Crafter   Katana    Show1   Longsw   Zanbato     Seraph     earned  passed  Sales5
old: always buys          17m      15m      20m     1:13      6:46      12:46   5.24e+07       0       -
60%, +6%/lv, +10%         18m      16m      20m     1:13      6:48      13:03   5.32e+07     761       -
70%, +5%/lv, +10%         18m      15m      20m     1:13      6:47      12:57   5.22e+07     399       -
50%, +8%/lv, +10%         17m      14m      18m     1:13      7:01      12:54   5.23e+07    1122       -

efficient, free, 8 seeds, 20 h (h:mm)
case                  Crafter   Katana    Show1   Longsw   Zanbato     Seraph     earned  passed  Sales5
old: always buys          14m       5m      38m      32m      3:38       8:10   8.49e+07       0       -
60%, +6%/lv, +10%         14m       5m      38m      31m      3:41       8:21   8.49e+07     885       -
70%, +5%/lv, +10%         13m       6m      37m      32m      3:42       8:20   8.41e+07     480       -
50%, +8%/lv, +10%         14m       5m      38m      33m      3:47       8:33    8.4e+07    1432       -
```

**Reading:** the built 60% case costs a casual player about 17 minutes to the Seraph (12:46 → 13:03) and an efficient one about 11 (8:10 → 8:21); earnings are within noise. Swords, not customers, still limit sales: a walk-in who passes leaves the sword for the next one. So More Sales, like Better Advertising, pays little while the shop is short of swords; it matters once holders outnumber what customers can take. Sim model: `engine.on_offer` (a pass frees the sword, tries one other free one after 1.5 s + `LOOK_WALK` + `remarkTime`, then leaves); the tutorial's first two sales and VIPs always offer.

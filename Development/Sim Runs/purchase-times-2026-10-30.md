# Purchase times — 2026-10-30

Allen: "Can u tell me what time each player takes to reach each purchase?" Hours of play (h:mm) for each simulated player type, sorted by when an efficient player gets it. Types ([[Development/Gameplay Simulator Plan]]): **casual** buys the cheapest thing first; **efficient** buys the best income per coin; **automator** hires crew first; **rusher** saves for swords; **grinder** buys what makes and sells more; **manager** keeps every rack, shelf, cart and mail full. Since Allen's "any sensible player would have bought the stations as they're available", every type also buys a station or station upgrade once it's within reach (not before a cheaper goal) and anything under a tenth of what it's saving for (behavior.choose_target). Gem upgrades are bought with gems, not coins.

## Today's game (Big Sword Stand without the Cashier)

Run `sensible-2026-10-30`, scenario `baseline`: median of 100 free players per type (— = fewer than half got there).

| Purchase | Price | Casual | Efficient | Automator | Rusher | Grinder | Manager |
|---|---|---|---|---|---|---|---|
| First sale | | 1 min | 1 min | 1 min | 1 min | 1 min | 1 min |
| Ore Slot 2 | 75 | 3 min | 2 min | 2 min | 2 min | 2 min | 1 min |
| Wakizashi Sword | 60 | 4 min | 2 min | 3 min | 3 min | 2 min | 2 min |
| Polishing Station | 100 | 5 min | 3 min | 4 min | 3 min | 3 min | 2 min |
| Tutorial done | | 6 min | 3 min | 4 min | 4 min | 4 min | 3 min |
| Faster Strikes I | 250 | 11 min | 4 min | 7 min | 4 min | 7 min | 3 min |
| Machete Sword | 360 | 14 min | 5 min | 17 min | 5 min | 9 min | 5 min |
| Etching Table | 790 | 18 min | 7 min | 10 min | 7 min | 11 min | 6 min |
| Faster Strikes II | 1,000 | 20 min | 9 min | 12 min | 9 min | 12 min | 7 min |
| Wall Sword Rack 2 | 53 | 4 min | 9 min | 12 min | 9 min | 3 min | 8 min |
| Katana Sword | 1,300 | 25 min | 11 min | 20 min | 11 min | 14 min | 9 min |
| Sword Rack | 140 | 6 min | 11 min | 5 min | 17 min | 4 min | 9 min |
| Ingot Rack | 230 | 10 min | 11 min | 6 min | 17 min | 5 min | 10 min |
| Ore Slot 3 | 280 | 11 min | 11 min | 15 min | 18 min | 7 min | 10 min |
| Faster Heating I | 290 | 13 min | 12 min | 16 min | 18 min | 8 min | 11 min |
| Ingot Rack 2 | 1,000 | 23 min | 13 min | 14 min | 23 min | 13 min | 17 min |
| Sword Rack 2 | 1,300 | 29 min | 14 min | 22 min | 28 min | 15 min | 18 min |
| Faster Heating II | 1,500 | 30 min | 16 min | 25 min | 32 min | 16 min | 18 min |
| Polish Boost I | 2,000 | 33 min | 17 min | 26 min | 13 min | 18 min | 12 min |
| Ore Slot 4 | 2,000 | 36 min | 18 min | 27 min | 35 min | 19 min | 19 min |
| Faster Strikes III | 2,500 | 39 min | 19 min | 29 min | 15 min | 20 min | 14 min |
| Polishing Station 2 | 2,500 | 42 min | 20 min | 30 min | 17 min | 22 min | 15 min |
| Display Table 1 | 220 | 8 min | 21 min | 15 min | 17 min | 5 min | 9 min |
| Scimitar Sword | 3,600 | 1:06 | 23 min | 1:13 | 20 min | 34 min | 17 min |
| Faster Heating III | 2,600 | 45 min | 24 min | 32 min | 36 min | 23 min | 21 min |
| Furnace 2 | 1,400 | 46 min | 25 min | 33 min | 37 min | 24 min | 21 min |
| Anvil 2 | 3,400 | 1:04 | 26 min | 35 min | 50 min | 32 min | 22 min |
| Furnace 2 Heating I | 900 | 46 min | 26 min | 36 min | 37 min | 25 min | 23 min |
| Back Wall Rack | 450 | 16 min | 26 min | 18 min | 20 min | 10 min | 17 min |
| Furnace 2 Heating II | 4,500 | 1:11 | 28 min | 1:16 | 52 min | 36 min | 26 min |
| Rickshaw Bay 1 | 1,100 | 27 min | 29 min | 22 min | 28 min | 57 min | 28 min |
| Faster Strikes IV | 5,000 | 1:19 | 30 min | 39 min | 23 min | 40 min | 29 min |
| Polish Boost II | 8,000 | 1:32 | 33 min | 42 min | 32 min | 59 min | 32 min |
| More VIPs 1 (gems) | | 2:00 | 36 min | 46 min | 38 min | — | — |
| Faster Strikes V | 10,000 | 1:45 | 37 min | 48 min | 35 min | 1:03 | 35 min |
| Longsword | 10,200 | 1:59 | 40 min | 1:59 | 27 min | 56 min | 38 min |
| Sword Crafter | 10,000 | 1:52 | 44 min | 53 min | 1:34 | 52 min | 41 min |
| Anvil 3 | 14,000 | 2:08 | 48 min | 1:03 | 1:36 | 1:07 | 46 min |
| Furnace 3 | 5,800 | 2:11 | 50 min | 1:24 | 1:38 | 1:09 | 48 min |
| Furnace 3 Heating I | 3,500 | 2:14 | 51 min | 1:27 | 1:38 | 1:09 | 48 min |
| Furnace 2 Heating III | 7,800 | 1:25 | 54 min | 1:42 | 1:12 | 44 min | 51 min |
| Ore Slot 5 | 9,800 | 1:39 | 57 min | 1:49 | 1:32 | 47 min | 53 min |
| Upgraded Store | 3,000 | 51 min | 58 min | 1:03 | 46 min | 26 min | 23 min |
| Delivery Cart | 3,100 | 54 min | 58 min | 1:06 | 47 min | 28 min | 55 min |
| Cart capacity 1 | | 55 min | 59 min | 1:06 | 47 min | 28 min | 55 min |
| Cart speed 1 | | 57 min | 1:00 | 1:08 | 48 min | 29 min | 56 min |
| Wall Sword Rack 3 | 3,200 | 1:00 | 1:01 | 1:11 | 49 min | 31 min | 24 min |
| Furnace 3 Heating II | 18,000 | 2:37 | 1:07 | 3:37 | 3:01 | 1:20 | 1:54 |
| Ore Slot 6 | 20,000 | 2:49 | 1:13 | 3:55 | 3:04 | 1:25 | 2:27 |
| Merge 1 | | 2:49 | 1:13 | 3:55 | 3:04 | 1:25 | 2:27 |
| Display Table 2 | 4,500 | 1:15 | 1:21 | 1:19 | 53 min | 38 min | 28 min |
| Polish Boost III | 25,000 | 4:21 | 1:30 | 2:15 | 59 min | 1:54 | 1:05 |
| Cutlass Sword | 26,000 | 4:55 | 1:37 | 5:08 | 46 min | 2:05 | 1:13 |
| Falchion Sword | 50,000 | 8:34 | 1:50 | 7:19 | 1:11 | 3:15 | 1:27 |
| Haru (2nd crafter) | 23,000 | 4:02 | 1:55 | 1:44 | 3:18 | 1:47 | 1:32 |
| Stocker | 36,000 | 6:05 | 2:02 | 2:34 | 4:28 | 2:30 | 1:41 |
| Anvil 4 | 22,000 | 6:16 | 2:07 | 2:46 | 4:30 | 2:33 | 1:46 |
| Merge 2 | | 5:14 | 2:13 | 5:22 | 4:16 | 2:12 | 2:47 |
| Furnace 3 Heating III | 31,000 | 5:48 | 2:25 | 5:47 | 4:23 | 2:23 | 2:57 |
| Better Advertising 2 (gems) | | 10:00 | 2:28 | 5:33 | 2:07 | — | — |
| Merge 3 | | 7:56 | 2:34 | 6:52 | 7:40 | 2:59 | 3:17 |
| Wall Sword Rack 4 | 15,000 | 2:24 | 2:45 | 2:55 | 1:42 | 1:13 | 1:49 |
| Jian Sword | 80,000 | 12:53 | 3:00 | 9:58 | 1:30 | 4:30 | 2:11 |
| Mei (3rd crafter) | 70,000 | 11:34 | 3:14 | 3:45 | 9:40 | 4:17 | 2:22 |
| Merge 4 | | 10:50 | 3:26 | 8:46 | 9:32 | 3:57 | 3:45 |
| Display Table 3 | 21,000 | 3:17 | 3:38 | 4:21 | 3:08 | 1:35 | 2:36 |
| Rickshaw Bay 2 | 22,000 | 3:32 | 3:43 | 4:30 | 3:13 | 6:27 | 3:58 |
| Display Table 4 | 23,000 | 3:47 | 3:48 | 4:41 | 3:16 | 1:41 | 2:40 |
| Merge 5 | | 13:25 | 4:03 | 10:23 | 10:54 | 4:44 | 4:13 |
| More VIPs 2 (gems) | | 14:00 | 4:07 | 6:30 | 4:00 | — | — |
| Cart capacity 2 | | 4:39 | 4:21 | 4:54 | 3:23 | 1:59 | 4:31 |
| Big Sword Stand | 36,000 | 6:36 | 4:26 | 6:00 | 4:34 | 2:39 | 3:02 |
| Gladius Sword | 150,000 | 14:37 | 4:48 | 12:50 | 2:07 | 5:15 | 4:49 |
| Etching Table 2 | 120,000 | 15:09 | 5:02 | 13:14 | 3:38 | 6:39 | 5:04 |
| Khopesh Sword | 160,000 | 16:51 | 5:22 | 14:52 | 2:34 | 6:08 | 5:22 |
| Merge 6 | | 15:48 | 5:39 | 14:21 | 11:02 | 5:34 | 5:39 |
| Shop Promoter | 40,000 | 6:51 | 5:58 | 6:15 | 6:33 | 10:00 | 5:57 |
| Better Advertising 3 (gems) | | 25:12 | 5:59 | 15:55 | 6:04 | — | — |
| Display Table 5 | 40,000 | 7:14 | 6:03 | 6:26 | 6:36 | 2:45 | 3:10 |
| Cart speed 2 | | 7:34 | 6:05 | 6:37 | 6:40 | 2:51 | 6:01 |
| Dadao Sword | 170,000 | 17:25 | 6:23 | 15:11 | 2:59 | 6:26 | 6:18 |
| Cashier | 50,000 | 8:57 | 6:27 | 7:35 | 7:45 | 11:02 | 6:23 |
| Cart speed 3 | | 9:24 | 6:32 | 7:51 | 8:23 | 3:25 | 6:27 |
| Merge 7 | | 18:07 | 6:51 | 16:35 | 11:16 | 6:59 | 7:12 |
| Display Table 6 | 60,000 | 9:54 | 7:14 | 8:08 | 8:57 | 3:35 | 3:34 |
| Zanbatō Sword | 250,000 | 19:30 | 7:34 | 17:11 | 4:59 | 7:39 | 6:50 |
| Cart capacity 3 | | 10:20 | 7:39 | 8:26 | 9:00 | 3:47 | 7:35 |
| GemPairLv3 | | — | 7:41 | 18:00 | 8:32 | 7:12 | 8:56 |
| More VIPs 3 (gems) | | — | 7:41 | 18:00 | 8:32 | — | — |
| Rapier Sword | 270,000 | 20:14 | 7:58 | 17:29 | 4:12 | 8:00 | 7:56 |
| Hook Sword | 290,000 | 21:20 | 8:19 | 17:50 | 5:27 | 8:39 | 8:19 |
| Sword Etcher | 270,000 | 20:52 | 8:35 | 14:02 | 11:28 | 8:20 | 8:37 |
| Rickshaw Bay 3 | 76,000 | 11:58 | 8:41 | 9:24 | 10:13 | 13:31 | 8:41 |
| Cart speed 4 | | 12:25 | 8:43 | 9:40 | 10:19 | 10:03 | 8:46 |
| Claymore Sword | 340,000 | 21:47 | 8:59 | 18:14 | 6:00 | 8:59 | 9:04 |
| Crescent Fang Sword | 370,000 | 22:59 | 9:17 | 19:17 | 6:30 | 9:57 | 9:23 |
| Shard Blade | 400,000 | 23:27 | 9:34 | 19:36 | 7:07 | 10:21 | 9:41 |
| Flamberge Sword | 430,000 | 23:56 | 9:51 | 19:59 | 7:36 | 10:43 | 9:59 |
| Moonbite Sword | 530,000 | 25:45 | 10:10 | 21:05 | 8:18 | 12:04 | 10:22 |
| Better Advertising 4 (gems) | | — | 10:14 | — | — | — | — |
| Serpent Sword | 570,000 | 26:14 | 10:29 | 21:26 | 8:55 | 12:27 | 10:42 |
| Leviathan Cleaver Sword | 640,000 | 26:45 | 10:49 | 21:52 | 9:30 | 12:47 | 11:05 |
| Thornspire Sword | 740,000 | 27:38 | 11:10 | 22:18 | 10:10 | 13:29 | 11:27 |
| Seraph Sword | 840,000 | 28:52 | 11:31 | 23:24 | 10:51 | 14:31 | 11:48 |
| Every pad bought | | 28:52 | 11:31 | 23:24 | 11:28 | 14:31 | 11:48 |
| Quicker Mail 1 (gems) | | 5:00 | — | 2:00 | — | 44 min | 1:00 |
| More Clients 1 (gems) | | 6:39 | — | 3:38 | — | 1:43 | 2:40 |
| Quicker Mail 2 (gems) | | 18:14 | — | 9:00 | — | 3:00 | 4:00 |
| More Clients 2 (gems) | | 21:41 | — | 11:54 | — | 4:00 | 5:00 |
| Quicker Mail 3 (gems) | | — | — | 20:00 | — | 5:42 | 6:49 |
| More Clients 3 (gems) | | — | — | 22:33 | — | 7:12 | 8:56 |
| Merge 8 | | 22:13 | — | 18:36 | — | 9:16 | — |
| Quicker Mail 4 (gems) | | — | — | — | — | 9:28 | 11:23 |
| Kenji (4th crafter) | 460,000 | 24:22 | — | 12:19 | — | 11:00 | — |
| Merge 9 | | 24:52 | — | 20:23 | — | 11:23 | — |
| More Clients 4 (gems) | | — | — | — | — | 12:27 | — |
| Rin (5th crafter) | 710,000 | 27:13 | — | 16:15 | — | 13:09 | — |
| Merge 10 | | 28:04 | — | 22:43 | — | 13:53 | — |
| Better Advertising 1 (gems) | | 0 min | 0 min | 0 min | 0 min | 0 min | 0 min |
| Quicker Mail 5 (gems) | | — | — | — | — | — | — |

## Proposed package (Eastern pad 35%, Sword Crafter 40,000, small pads ×2)

Run `sensible-2026-10-30`, scenario `m-c40-small2-stand`: median of 100 free players per type (— = fewer than half got there).

| Purchase | Price | Casual | Efficient | Automator | Rusher | Grinder | Manager |
|---|---|---|---|---|---|---|---|
| First sale | | 1 min | 1 min | 1 min | 1 min | 1 min | 1 min |
| Ore Slot 2 | 75 | 3 min | 2 min | 2 min | 2 min | 2 min | 1 min |
| Wakizashi Sword | 60 | 4 min | 2 min | 3 min | 3 min | 2 min | 2 min |
| Polishing Station | 200 | 6 min | 3 min | 4 min | 3 min | 4 min | 3 min |
| Tutorial done | | 6 min | 3 min | 4 min | 3 min | 4 min | 3 min |
| Machete Sword | 360 | 11 min | 5 min | 22 min | 5 min | 7 min | 4 min |
| Faster Strikes I | 500 | 16 min | 6 min | 9 min | 7 min | 9 min | 5 min |
| Wall Sword Rack 2 | 106 | 5 min | 7 min | 18 min | 7 min | 3 min | 6 min |
| Katana Sword | 1,300 | 22 min | 9 min | 27 min | 9 min | 13 min | 7 min |
| Ore Slot 3 | 280 | 8 min | 9 min | 22 min | 13 min | 5 min | 8 min |
| Sword Rack | 280 | 10 min | 9 min | 6 min | 13 min | 6 min | 8 min |
| Etching Table | 1,580 | 24 min | 11 min | 13 min | 11 min | 14 min | 10 min |
| Faster Strikes II | 2,000 | 27 min | 13 min | 17 min | 13 min | 16 min | 11 min |
| Scimitar Sword | 3,600 | 45 min | 15 min | 38 min | 16 min | 23 min | 13 min |
| Ingot Rack | 460 | 14 min | 15 min | 7 min | 16 min | 9 min | 14 min |
| Faster Heating I | 580 | 17 min | 16 min | 24 min | 19 min | 10 min | 14 min |
| Ore Slot 4 | 2,000 | 30 min | 17 min | 32 min | 32 min | 17 min | 16 min |
| Ingot Rack 2 | 2,000 | 32 min | 18 min | 21 min | 33 min | 19 min | 17 min |
| Sword Rack 2 | 2,600 | 38 min | 19 min | 30 min | 36 min | 20 min | 29 min |
| Faster Heating II | 3,000 | 41 min | 21 min | 35 min | 53 min | 22 min | 30 min |
| Display Table 1 | 440 | 13 min | 21 min | 23 min | 16 min | 8 min | 14 min |
| Polish Boost I | 4,000 | 49 min | 23 min | 40 min | 19 min | 25 min | 18 min |
| Faster Strikes III | 5,000 | 53 min | 24 min | 42 min | 22 min | 27 min | 20 min |
| Polishing Station 2 | 5,000 | 56 min | 26 min | 46 min | 23 min | 29 min | 22 min |
| Faster Heating III | 5,200 | 1:00 | 28 min | 48 min | 1:12 | 31 min | 32 min |
| Furnace 2 | 2,800 | 1:03 | 29 min | 50 min | 1:13 | 32 min | 33 min |
| Anvil 2 | 3,400 | 1:07 | 31 min | 52 min | 1:13 | 34 min | 34 min |
| Furnace 2 Heating I | 1,800 | 1:03 | 31 min | 52 min | 1:13 | 33 min | 34 min |
| Back Wall Rack | 900 | 19 min | 32 min | 25 min | 24 min | 11 min | 15 min |
| Faster Strikes IV | 10,000 | 1:52 | 36 min | 1:13 | 28 min | 59 min | 25 min |
| More VIPs 1 (gems) | | 2:00 | 40 min | 46 min | 41 min | — | — |
| Longsword | 10,200 | 1:58 | 40 min | 1:59 | 32 min | 1:02 | 28 min |
| Furnace 2 Heating II | 9,000 | 1:31 | 44 min | 1:06 | 1:29 | 47 min | 40 min |
| Ore Slot 5 | 9,800 | 1:46 | 47 min | 1:54 | 1:33 | 56 min | 45 min |
| Rickshaw Bay 1 | 2,200 | 35 min | 48 min | 33 min | 34 min | 1:21 | 45 min |
| Polish Boost II | 16,000 | 2:17 | 53 min | 1:20 | 57 min | 1:25 | 50 min |
| Faster Strikes V | 20,000 | 2:28 | 58 min | 1:28 | 1:01 | 1:29 | 54 min |
| Cutlass Sword | 26,000 | 3:13 | 1:05 | 5:08 | 44 min | 1:41 | 1:00 |
| Furnace 2 Heating III | 15,600 | 2:08 | 1:09 | 3:09 | 2:00 | 1:08 | 1:04 |
| Ore Slot 6 | 20,000 | 2:38 | 1:15 | 4:25 | 2:19 | 1:15 | 1:07 |
| Merge 1 | | 2:38 | 1:15 | 4:25 | 2:19 | 1:15 | 1:07 |
| Upgraded Store | 6,000 | 1:11 | 1:21 | 55 min | 1:24 | 37 min | 36 min |
| Delivery Cart | 6,200 | 1:16 | 1:23 | 58 min | 1:26 | 40 min | 1:13 |
| Cart capacity 1 | | 1:17 | 1:24 | 58 min | 1:26 | 40 min | 1:13 |
| Cart speed 1 | | 1:19 | 1:25 | 59 min | 1:26 | 40 min | 1:14 |
| Wall Sword Rack 3 | 6,400 | 1:25 | 1:26 | 1:02 | 1:28 | 43 min | 37 min |
| Jian Sword | 28,000 | 3:25 | 1:30 | 5:24 | 52 min | 1:49 | 1:18 |
| Merge 2 | | 3:37 | 1:35 | 5:36 | 2:53 | 1:55 | 2:02 |
| Display Table 2 | 9,000 | 1:37 | 1:40 | 1:08 | 1:31 | 51 min | 42 min |
| Polish Boost III | 50,000 | 7:02 | 1:48 | 3:50 | 1:40 | 3:16 | 1:27 |
| Better Advertising 2 (gems) | | 7:59 | 1:48 | 5:08 | 2:00 | — | — |
| Dadao Sword | 59,500 | 7:59 | 1:57 | 7:54 | 1:24 | 3:39 | 1:36 |
| Sword Crafter | 40,000 | 4:20 | 2:01 | 1:44 | 4:24 | 2:17 | 1:41 |
| Anvil 3 | 14,000 | 4:24 | 2:03 | 1:51 | 4:25 | 2:19 | 1:43 |
| Stocker | 36,000 | 4:46 | 2:07 | 2:17 | 4:30 | 2:30 | 1:47 |
| Anvil 4 | 22,000 | 4:54 | 2:10 | 2:33 | 4:32 | 2:34 | 1:50 |
| Furnace 3 | 11,600 | 4:27 | 2:11 | 2:42 | 4:26 | 2:20 | 1:51 |
| Furnace 3 Heating I | 7,000 | 4:29 | 2:14 | 2:59 | 4:27 | 2:21 | 1:55 |
| Haru (2nd crafter) | 23,000 | 4:35 | 2:14 | 2:58 | 4:29 | 2:26 | 1:57 |
| Furnace 3 Heating II | 36,000 | 5:09 | 2:23 | 6:05 | 4:33 | 2:38 | 2:18 |
| Merge 3 | | 6:13 | 2:29 | 6:57 | 5:45 | 2:57 | 2:46 |
| Mei (3rd crafter) | 70,000 | 9:10 | 2:32 | 4:27 | 8:00 | 4:15 | 2:13 |
| Furnace 3 Heating III | 62,000 | 8:15 | 2:44 | 8:06 | 7:16 | 3:46 | 3:04 |
| Merge 4 | | 8:47 | 2:54 | 8:30 | 7:56 | 4:01 | 3:11 |
| Merge 5 | | 10:50 | 3:15 | 9:55 | 9:19 | 4:42 | 3:39 |
| Cart capacity 2 | | 3:00 | 3:28 | 4:52 | 2:23 | 1:35 | 3:49 |
| Wall Sword Rack 4 | 30,000 | 3:57 | 3:33 | 5:56 | 2:59 | 2:04 | 2:13 |
| Big Sword Stand | 36,000 | 4:09 | 3:37 | 6:15 | 3:02 | 2:10 | 2:24 |
| Zanbatō Sword | 87,500 | 10:09 | 3:46 | 9:26 | 3:10 | 4:32 | 2:36 |
| More VIPs 2 (gems) | | 12:00 | 4:00 | 6:17 | 3:13 | — | — |
| Merge 6 | | 12:31 | 4:00 | 12:08 | 9:32 | 5:28 | 4:18 |
| Cart speed 2 | | 5:22 | 4:17 | 6:25 | 4:36 | 2:43 | 4:35 |
| Display Table 3 | 42,000 | 5:38 | 4:21 | 6:34 | 5:08 | 2:49 | 2:40 |
| Rickshaw Bay 2 | 44,000 | 5:56 | 4:25 | 6:47 | 5:41 | 9:25 | 4:41 |
| Display Table 4 | 46,000 | 6:45 | 4:30 | 7:19 | 5:51 | 3:09 | 2:57 |
| Falchion Sword | 50,000 | 7:20 | 4:35 | 7:28 | 1:11 | 3:23 | 4:44 |
| Cart speed 3 | | 7:39 | 4:39 | 7:41 | 6:29 | 3:31 | 4:50 |
| Merge 7 | | 14:24 | 4:59 | 15:26 | 9:49 | 6:12 | 5:10 |
| Cart capacity 3 | | 8:32 | 5:20 | 8:18 | 7:19 | 3:54 | 5:32 |
| Better Advertising 3 (gems) | | 22:30 | 5:41 | 15:06 | 6:00 | — | — |
| Hook Sword | 290,000 | 17:21 | 5:43 | 16:28 | 3:33 | 7:13 | 5:56 |
| Shop Promoter | 80,000 | 9:26 | 5:51 | 8:54 | 8:33 | 13:17 | 6:02 |
| Cart speed 4 | | 9:39 | 5:56 | 9:02 | 8:37 | 13:20 | 6:07 |
| Display Table 5 | 80,000 | 9:53 | 6:00 | 9:14 | 8:40 | 4:23 | 3:27 |
| Crescent Fang Sword | 370,000 | 19:04 | 6:22 | 17:54 | 4:22 | 8:39 | 6:31 |
| Shard Blade | 400,000 | 19:32 | 6:45 | 18:16 | 5:06 | 9:02 | 6:56 |
| Merge 8 | | 18:13 | 7:02 | 17:12 | — | 7:57 | 7:15 |
| Cashier | 100,000 | 10:28 | 7:21 | 9:39 | 9:14 | 13:43 | 7:37 |
| GemPairLv3 | | — | 7:34 | 17:16 | 7:59 | 7:14 | 9:52 |
| More VIPs 3 (gems) | | — | 7:34 | 17:16 | 7:59 | — | — |
| Kenji (4th crafter) | 460,000 | 20:25 | 7:39 | 11:12 | — | 10:08 | 8:50 |
| Display Table 6 | 120,000 | 11:34 | 7:46 | 11:28 | 9:24 | 5:02 | 4:02 |
| Moonbite Sword | 530,000 | 21:49 | 8:09 | 19:41 | 6:26 | 11:12 | 8:04 |
| Serpent Sword | 570,000 | 22:16 | 8:32 | 20:06 | 7:13 | 11:32 | 8:29 |
| Merge 9 | | 20:53 | 8:52 | 18:59 | — | 10:30 | 9:13 |
| Gladius Sword | 150,000 | 12:02 | 9:16 | 11:47 | 1:59 | 5:16 | 9:36 |
| Rickshaw Bay 3 | 152,000 | 13:24 | 9:22 | 12:50 | 9:42 | 13:45 | 9:41 |
| Etching Table 2 | 240,000 | 15:38 | 9:29 | 13:44 | 6:42 | 9:35 | 9:48 |
| Leviathan Cleaver Sword | 640,000 | 22:47 | 9:50 | 20:29 | 7:49 | 11:54 | 10:14 |
| Sword Etcher | 270,000 | 16:55 | 9:58 | 14:17 | 10:03 | 9:49 | 10:23 |
| Khopesh Sword | 160,000 | 13:47 | 10:04 | 13:09 | 2:16 | 5:53 | 10:29 |
| Thornspire Sword | 740,000 | 23:42 | 10:22 | 20:55 | 8:31 | 12:35 | 10:50 |
| Seraph Sword | 840,000 | 24:57 | 10:45 | 22:02 | 9:11 | 13:40 | 11:11 |
| Rin (5th crafter) | 710,000 | 23:19 | 10:59 | 15:14 | — | 12:16 | 11:28 |
| Merge 10 | | 24:06 | 11:14 | 21:18 | — | 12:57 | 11:44 |
| Better Advertising 4 (gems) | | — | 11:28 | — | — | — | — |
| Rapier Sword | 270,000 | 16:18 | 11:34 | 16:06 | 2:50 | 6:52 | 12:03 |
| Claymore Sword | 340,000 | 17:48 | 11:41 | 16:52 | 3:58 | 7:36 | 12:10 |
| Flamberge Sword | 430,000 | 19:58 | 11:48 | 18:34 | 5:38 | 9:23 | 12:18 |
| Every pad bought | | 24:57 | 11:48 | 22:02 | 10:03 | 13:45 | 12:18 |
| Quicker Mail 1 (gems) | | 3:38 | — | 1:36 | — | 47 min | 46 min |
| More Clients 1 (gems) | | 6:00 | — | 3:27 | — | 1:30 | 1:42 |
| Quicker Mail 2 (gems) | | 15:31 | — | 8:11 | — | 3:00 | 3:50 |
| More Clients 2 (gems) | | 18:32 | — | 11:00 | — | 3:59 | 5:00 |
| Quicker Mail 3 (gems) | | — | — | 19:35 | — | 5:45 | 6:34 |
| More Clients 3 (gems) | | — | — | — | — | 7:14 | 9:52 |
| Quicker Mail 4 (gems) | | — | — | — | — | 9:44 | — |
| More Clients 4 (gems) | | — | — | — | — | 12:42 | — |
| Better Advertising 1 (gems) | | 0 min | 0 min | 0 min | 0 min | 0 min | 0 min |

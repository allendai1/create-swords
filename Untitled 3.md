
after upgrading the sign has some blank space. Also remove the glowing shamrock above. ![[Pasted image 20261101115309.png]]

Need to completely re-evaluate the upgrade path tree. Things are locked behind things that seem illogical.

Upgraded store is available after only 3 shop upgrades, seems a bit quick to get to

First employee Taise says it requires 40,000 coins but doesnt state that you also need the stations bought as well

![[Pasted image 20261101115728.png]]
the text hierarchy is bad. it should be lvl. 2 and then 20 gems underneath it, using the gem icon instead of "gems". It should also say lvl 1 ->lvl 2 to show it's an expedited upgrade. The button color should be a bright green to show its a purchase. The gem price should also scale with how close they are to the next level if it doesn't already.

![[Pasted image 20261101120002.png]]
the bottom button needs padding, it could also be much smaller of a window.

![[Pasted image 20261101120045.png]]the down button is misaligned. Was also hoping its part of the auto-roll gui, where it sits in the bottom middle of it to expand it. right now the pill toggle activates on the whole gui, just make it activate on the pill itself because of this.

![[Pasted image 20261101120314.png]]
use coin icon not "coins"

![[Pasted image 20261101121154.png]]
people dont know what rickshaws are, just have it say Bay 1. but its also unclear what it does? need to show the benefits of it.

stocker and other npcs still get stuck
``` 12:15:51.987  NpcWalk: jvillafranco stopped short at 648.3231201171875, 3.1934401988983154, -240.32669067382812 of 650, 3, -240.48104858398438; against [Workspace.Plot_N2.Shop.Displays.DisplayTable1.Table.apron_short_2, Workspace.Plot_N2.Shop.Displays.DisplayTable1.Table.tabletop, Workspace.Plot_N2.Shop.Displays.DisplayTable1.Table.leg_2, Workspace.Plot_N2.Shop.Displays.DisplayTable1.Table.apron_long_1], standing on Workspace.Plot_N2.Shop.Upgraded.Floor  -  Server - NpcWalk:139
  12:16:09.851   ▶ AnalyticsService: LogCustomEvent event fired. (x3)  -  Studio
  12:16:40.951   ▶ AnalyticsService: LogEconomyEvent event fired. (x17)  -  Studio
  12:16:41.867  NpcWalk: Stocker stuck at 645.212890625, 3.431640625, -280.4296875, stepped to 620, 3, -248.6999969482422; against [], standing on Workspace.Plot_N2.Grounds.Paving  -  Server - NpcWalk:142
  12:16:52.734  NpcWalk: Stocker stuck at 645.60546875, 3.431640625, -279.587890625, stepped to 621.5, 3.5, -286.29998779296875; against [Workspace.Plot_N2.Workshop.Shell.Post], standing on Workspace.Plot_N2.Grounds.Paving  -  Server - NpcWalk:142
  12:17:01.733  NpcWalk: Stocker stuck at 645.837890625, 3.392578125, -276.857421875, stepped to 620, 3, -244.6999969482422; against [Workspace.Plot_N2.Workshop.Shell.Post], standing on Workspace.Plot_N2.Shop.Upgraded.Floor  -  Server - NpcWalk:142
  12:17:13.066  NpcWalk: Stocker stuck at 645.611328125, 3.431640625, -279.673828125, stepped to 621.5, 3.5, -286.29998779296875; against [Workspace.Plot_N2.Workshop.Shell.Post], standing on Workspace.Plot_N2.Grounds.Paving  -  Server - NpcWalk:142
```

do the mail quests scale with our progression? seems like if i have lots of upgrades, the quests still give very little coins. gems should still stay the same though

![[Pasted image 20261101122436.png]]
could we make the crew cards different colors to match their stars.

**Done 2026-11-01** (not played yet): all but the upgrade tree (a proposal: [[Design/Upgrade Tree Review — 2026-11-01]]). Mail scaling done after: +10% coins per shop upgrade. [[Sessions/2026-11-01]]

![[Pasted image 20261101141159.png]]
seems too intrusive and large. hierarchy should be text and then the price below it. should only show when they're close enough to buy.

```  14:10:19.431  nil  -  Client
  14:10:19.696  ContentId: rbxassetid://203785492 failed due to: Asset type does not match requested type  -  Studio
  14:10:20.044  nil  -  Server
  14:10:20.827  ContentId: rbxassetid://343445389 failed due to: Request asset was not found  -  Studio
  14:10:20.853  [TopbarPlus]: Please consider a one-time donation (from 5 Robux) at https://www.roblox.com/games/start?placeId=106966695720565 to support this project (this message only ever appears to non-donators in-studio)  -  Client - Attribute:46
  14:10:20.985   ▶ AnalyticsService: LogCustomEvent event fired. (x2)  -  Studio
  14:10:21.367  ContentId: rbxassetid://4399600835 failed due to: Asset is not approved for the requester  -  Studio
  14:10:21.430  ContentId: rbxassetid://237875975 failed due to: Asset is not approved for the requester  -  Studio
  14:10:23.559  [robloxstudio-mcp] /ready failed for instance:v7y-r43/server: RequestAsync threw for http://localhost:58741/ready: HttpError: ConnectFail  -  Server
  14:10:25.764  [robloxstudio-mcp] proxy register failed for goku19876: RequestAsync threw for http://localhost:58741/ready: HttpError: ConnectFail  -  Server
  14:11:09.427   ▶ AnalyticsService: LogCustomEvent event fired. (x3)  -  Studio
  14:12:46.624   ▶ AnalyticsService: LogEconomyEvent event fired. (x4)  -  Studio
  14:12:46.625  AnalyticsService: LogCustomEvent event fired.  -  Studio
  14:13:17.745  ContentId: rbxassetid://182850160 failed due to: Asset is not approved for the requester  -  Studio
  14:13:34.999  ContentId: rbxassetid://43556891 failed due to: Asset is not approved for the requester  -  Studio
```

**Done 2026-11-01** (not played yet): the pass label is name over price and shows only at the prompt; the log's failing assets are toolbox leftovers (gone) and the ManBun hair loads again. [[Sessions/2026-11-01#Pass label, Rin's look, smoother Stocker]]




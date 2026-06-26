# Subnautica 2 Telemetry Report

Live progression telemetry and configuration summary generated via SSH from gaming rig `jake@192.168.0.100`. All binary saves and plaintext configs are mirrored locally in `backups/`.

## Session Specifications
* **Game Title**: Subnautica 2 (Early Access Standalone | Unreal Engine 5)
* **Gaming Host**: `pc` (`192.168.0.100` | Windows 11 x64 | User: `jake`)
* **Platform Provider**: Steam (`OnlineSubsystemSteam` | Player ID `76561198797039235`)
* **Active Save File**: `savegame_1.sav` (1095.9 KB | Last Saved: `2026-06-25 23:32:43`)
* **Auto-Save State**: **Enabled** (`UWESaveSystemUserSetting.ini` | `bAutoSaveEnabled=True`)
* **Display Config**: `1280x720` dynamic render resolution scaling to `3840x2160` output (TSR Upscaling Quality Mode 3 | FPS Cap: 120)
* **Remote Git Repository**: `C:/Users/jake/AppData/Local/Subnautica2/Saved/.git/` (Pristine tree `4df49f6`)
* **Save Directory**: `C:/Users/jake/AppData/Local/Subnautica2/Saved/SaveGames/`
* **Log File**: `C:/Users/jake/AppData/Local/Subnautica2/Saved/Logs/Subnautica2.log`

## Equipment Status
Raw extracted equipment items and resource nodes actively discovered in workspace:

| Category | Discovered Symbols | Verification Status |
| :--- | :--- | :--- |
| **Tools** | `'CZzQuartz`, `'Game/Bluepnts/Items/BP BasicBattery`, `(Game/Bluepnts/Items/Tools/BP Scanner`, `)Salt`, `)Saltalt`, `- Chap (silver)3k` | Equipped in active `AUWEBaseItem` slots. |
| **Survival Gear** | `.*Jubilee2 QuartzChi`, `.KGTitanium`, `/Resource/DA Titanium`, `1ToolsFlares`, `1bo2.`, `2o2c` | +45.0 Max Oxygen Set Component verified. |
| **Raw Resources** | `3O2$2`, `84PFabricCurtaiSeaWSolarPaneradlhBatteryTerminHalf`, `8DA Water.Count`, `9!BP MedKit`, `9!MedKit`, `9E'BP BasicBattery`, `A(Scanner`, `BA(Scanner`, `BranchingCoralWaterslug`, `Builder` | Serialized in resource node prototypes. |

## Biome Coordinates
Telemetry engine confirms player traversal across the following core world partitions:

| Partition / Zone | Evaluated Telemetry Symbols | Approx Depth | Distance & Direction from Pod | Relative to Angel Comb Habitat | Threat Level |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Safe Shallows / Pod** | `L_Main`, `Lifepod_SignalOriginal` | ~0m | Origin (`X: 0m, Y: 0m`) | ~238m East | None |
| **Angel Comb Habitat** | `CoralGardens`, `BioBed`, `SolarPanel` | ~30m | ~238m West (`X: 0.1m, Y: -237.8m W`) | Core Base Reference Point | Low |
| **Crashed Black Box** | `CoralGardensRadioMessageBlackBox` | ~45m | ~380m North | ~250m Northeast | Low |
| **Kelp Forest Border** | `FeatherKelp`, `KelpRandomNode` | ~50m-90m | ~250m-400m West / Southwest | Directly South & Adjacent | Medium |
| **Welcome Center BioLab**| `DA__Signal_WelcomeCent_Hide` | ~60m | ~500m Northwest | ~300m North-Northwest | Medium |
| **Abandoned Basecamp** | `InvesgPOI_PZ_Basecamp`, `ColonistBunker052` | ~70m | ~420m West | ~180m West along canyon shelf | High |
| **Thermal Vents** | `SmallVent`, `VentFall` | ~80m-120m | ~450m Northeast / East | ~550m East-Northeast | High |

## Narrative Quests & Radio Signals
* **Welcome Center Signal**: `DA__Signal_WelcomeCent_Hide`
* **Habitat Beacon**: `DA__Signal_Habitat_Hide`
* **Emergency Lifepod**: `Lifepod_SignalOriginal`
* **Black Box Investigation**: `CoralGardensRadioMessageBlackBox`

## Constructed Facilities & Vehicles
* **Base Modules & Tech**: `"Corridor&NkDoor`, `"Corridor&NkDoorOveeSnapping`, `$ BasePiece Processor`, `($Tools DeployableLocker`, `(BioLab`, `+Bluepnts/ing/BP Hatch C`, `,E*Items/ToolsWakemaker`, `,E*Wakemaker`, `-Blueprints/ing/BP Locker Wall C`, `/+TadpolePensNoA Trigger%JFPlateBlue4HydroelectricTurbineExodus1PTransmiCeiLSmPedSalGeordiCell`
* **Submersibles & Hulls**: `Tadpole Fragment`, `TadpolePens06`
* **Discovered POIs**: `/InvesgPOI PZ Basecamp`, `7WandTrigger CoralGardens`, `AcidRaion SGFeatherKelprancWerslug`, `Art/Environment/BioalGarden/efabsWafers/BP CG  02b`, `BFrKelpABranGsPsh1`, `Blueprints/EnvironmenalGardenG BulbFlx`, `CampOne+*%`, `EnvironmenalGardens/4`
* **World Engine Milestones**: `.dPrototypDied Blackbox`, `/+BlackBox Investigation Quaker`, `/Narrative//DA  Signal Habitat Hide`, `Blackbox 2GCNoA`, `ClosedEventStoryGoal`, `ClosedEventStoryGoals`, `DA OxygenTunic StoryGoal`, `I2jxdPlayerDied Blackbox`
* **Decoded Progression Guide**: [savegame_1_decoded.md](./backups/savegame_1_decoded.md)

## Live Spatial Geometry (Save Coordinates Matrix)
* `BP_WorldSupplyLocker (X=-0, Y=116, Z=-0) | ~1.2m dist, -0.0m depth`
* `BP_WorldSupplyLocker (X=-0, Y=9293, Z=-0) | ~92.9m dist, -0.0m depth`
* `BP_WorldSupplyLocker (X=-240806, Y=0, Z=0) | ~2408.1m dist, 0.0m depth`
* `BP_WorldSupplyLocker (X=-3878, Y=-0, Z=9293) | ~38.8m dist, 92.9m depth`
* `BP_WorldSupplyLocker (X=-3878, Y=0, Z=-0) | ~38.8m dist, -0.0m depth`
* `BP_WorldSupplyLocker (X=-9692, Y=0, Z=0) | ~96.9m dist, 0.0m depth`
* `BP_WorldSupplyLocker (X=0, Y=-26184, Z=-0) | ~261.8m dist, -0.0m depth`
* `BP_WorldSupplyLocker (X=14462, Y=0, Z=0) | ~144.6m dist, 0.0m depth`
* `BP_WorldSupplyLocker (X=34148, Y=0, Z=0) | ~341.5m dist, 0.0m depth`
* `BP_WorldSupplyLocker (X=9293, Y=-0, Z=-0) | ~92.9m dist, -0.0m depth`
* `Beacon (X=-0, Y=-71434, Z=0) | ~714.3m dist, 0.0m depth`
* `Beacon (X=0, Y=2455, Z=0) | ~24.6m dist, 0.0m depth`
* `BioBed (X=-0, Y=-1312, Z=0) | ~13.1m dist, 0.0m depth`
* `BioBed (X=-0, Y=-422, Z=2) | ~4.2m dist, 0.0m depth`
* `BioBed (X=-0, Y=135, Z=-0) | ~1.3m dist, -0.0m depth`

## Graphics Configuration
Summary extracted from [GameUserSettings.ini](./backups/GameUserSettings.ini):
* **Resolution**: ResolutionSizeX=1280, ResolutionSizeY=720
* **Frame Rate Cap**: FrameRateLimit=120.000000
* **Upscaling Quality**: ScalabilityQuality_TSR=3

## Recent Engine Events
Snapshot of diagnostic gameplay session events logged by engine:

```text
[2026.06.26-06.37.11:793][666]LogBlueprintUserMessages: [WBP_CompilingShadersScreen_C_2147480722] *** DECONSTRUCT
access-control-expose-headers: x-sentry-error,x-sentry-rate-limits,retry-after
[2026.06.26-06.37.11:910][666]LogMoviePlayer: Shutting down movie player
[2026.06.26-06.37.12:394][666]LogRHI: FPipelineFileCacheManager Incremental saved 182 total, 10 new, 0 removed, 0 c
[2026.06.26-06.37.12:827][666]LogHttp: Warning: 	verb=[POST] url=[https://api.live.subnautica.net/api/v1/player/log
```

## Reference Links
* **Progression Guide**: [GUIDE.md](./GUIDE.md)
* **Progression Roadmap**: [TODO.md](./TODO.md)
* **Primary Project Guide**: [README.md](./README.md)
* **Multiplayer Cloud SOP**: [MULTIPLAYER.md](./MULTIPLAYER.md)
* **Previous Chat Archive**: [subnuatica_2_previous_chat.md](./backups/subnuatica_2_previous_chat.md)
* **Local Engine Log Dump**: [Subnautica2.log](./backups/Subnautica2.log)
* **Local Backups Vault**: [backups/](./backups)
* **Developer Toolkit**: [Makefile](./Makefile)
* **Unified Toolkit**: [subnautica_scraper.py](./subnautica_scraper.py)
* **Project Changelog**: [CHANGELOG.md](./CHANGELOG.md)
* **Steam News Hub**: [store.steampowered.com/news/app/1962700](https://store.steampowered.com/news/app/1962700)
* **Dev Kanban Board**: [subnautica2.nolt.io/kanban](https://subnautica2.nolt.io/kanban)
* **Official Site News**: [unknownworlds.com/en/news](https://unknownworlds.com/en/news)
* **Subnautica 2 Official Wiki**: [subnautica.fandom.com/wiki/Subnautica_2](https://subnautica.fandom.com/wiki/Subnautica_2)
* **Subnautica 2 Interactive Map**: [subnauticamap.io](https://subnauticamap.io)
* **Official Website**: [subnautica.com](https://subnautica.com)

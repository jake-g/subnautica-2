# Subnautica 2 Telemetry Report

Live progression telemetry and configuration summary generated via SSH from gaming rig `jake@192.168.0.100`. All binary saves and plaintext configs are mirrored locally in `backups/`.

## 🖥️ Session Specifications
* **Game Title**: Subnautica 2 (Early Access Standalone | Unreal Engine 5)
* **Gaming Host**: `pc` (`192.168.0.100` | Windows 11 x64 | User: `jake`)
* **Platform Provider**: Steam (`OnlineSubsystemSteam` | Player ID `76561198797039235`)
* **Active Save File**: `savegame_1.sav` (1175.1 KB | Last Saved: `2026-06-27 17:49:59`)
* **Auto-Save State**: **Enabled** (`UWESaveSystemUserSetting.ini` | `bAutoSaveEnabled=True`)
* **Display Config**: `3840x2160` (Streaming Session (Steam Remote Play) | FPS Cap: 120)
* **Remote Git Repository**: `C:/Users/jake/AppData/Local/Subnautica2/Saved/.git/` (Pristine tree `4df49f6`)
* **Save Directory**: `C:/Users/jake/AppData/Local/Subnautica2/Saved/SaveGames/`
* **Log File**: `C:/Users/jake/AppData/Local/Subnautica2/Saved/Logs/Subnautica2.log`

## 🛠️ Discovered Equipment & Resources

| Category | Discovered Items | Verification Status |
| :--- | :--- | :--- |
| **Tools** | `1bo2.`, `2o2c`, `3O2$2`, `3o2C`, `Battery`, `Biobed` | Equipped in active slots. |
| **Survival Gear** | `CG DomSonicResonatoicadaWreck02Lea`, `CG DomSonicResonatoicadaWreck02LeaProcess`, `Copper`, `Copper Wire`, `Corridor`, `CuubThPo2` | +45.0 Max Oxygen Set Component verified. |
| **Raw Resources** | `Emergency Lifepod Signal`, `Fiber Mesh`, `First Aid Kit`, `Flare`, `Flashlight`, `Glass`, `Habitat Builder`, `JO2D`, `Lead`, `Lyo2Y` | Serialized in resource node prototypes. |

## 🏗️ Constructed Facilities & Vehicles

| Category | Discovered Assets |
| :--- | :--- |
| **Base Modules & Tech** | `Beacon`, `Biobed`, `Biolab`, `Chair`, `Corridor`, `Fabricator`, `Foundation`, `Hatch`, `Hydroelectric Turbine`, `Locker` |
| **Submersibles & Hulls** | `Moonpool Dock`, `Tadpole Submersible` |
| **Discovered POIs** | `Alterra Basecamp`, `BFrKelpABranGsPsh1`, `Blueprints/EnvironmenalGardenG BulbFlx`, `Blueprints/EnvironmentGardenG BulbFlx`, `Camp One Wreckage`, `DA  NarrativeSignal Investigation CoralGardens 2 Anita`, `Emergency Lifepod Signal`, `EnvironmenalGardens/BP CG BulbFl` |

## 📡 Active Signals & Story Goals

| Signal / Quest | Status | Details |
| :--- | :--- | :--- |
| **Habitat Beacon** | 🟢 Active | Base builder tutorial signal |

## 🗺️ Biome Coordinates
Player traversal history across core world partitions:

| Partition / Zone | Approx Depth | Distance & Direction from Pod | Relative to Angel Comb Habitat | Threat Level |
| :--- | :---: | :--- | :--- | :---: |
| **Safe Shallows / Pod** | ~0m | Origin (`X: 0m, Y: 0m`) | ~238m East | None |
| **Angel Comb Habitat** | ~30m | ~238m West (`X: 0.1m, Y: -237.8m W`) | Core Base Reference Point | Low |
| **Crashed Black Box** | ~45m | ~380m North | ~250m Northeast | Low |
| **Kelp Forest Border** | ~50m-90m | ~250m-400m West / Southwest | Directly South & Adjacent | Medium |
| **Welcome Center BioLab**| ~60m | ~500m Northwest | ~300m North-Northwest | Medium |
| **Abandoned Basecamp** | ~70m | ~420m West | ~180m West along canyon shelf | High |
| **Thermal Vents** | ~80m-120m | ~450m Northeast / East | ~550m East-Northeast | High |

## 📍 Live Spatial Geometry (Save Coordinates Matrix)
* `BP_WorldSupplyLocker (X=-0, Y=-2275, Z=-0) | ~22.7m dist, -0.0m depth`
* `BP_WorldSupplyLocker (X=-0, Y=116, Z=-0) | ~1.2m dist, -0.0m depth`
* `BP_WorldSupplyLocker (X=-0, Y=9293, Z=-0) | ~92.9m dist, -0.0m depth`
* `BP_WorldSupplyLocker (X=-2275, Y=-0, Z=0) | ~22.7m dist, 0.0m depth`
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
* `BioBed (X=-0, Y=-12081, Z=0) | ~120.8m dist, 0.0m depth`

## ⚙️ Graphics Configuration
Summary extracted from [GameUserSettings.ini](./backups/GameUserSettings.ini):
* **Resolution**: 3840x2160 (Last Confirmed: 1280x720)
* **Frame Rate Cap**: 120.000000 FPS
* **Upscaling Quality**: ScalabilityQuality_TSR=3

## 📝 Recent Engine Events
Snapshot of diagnostic gameplay session events logged by engine:

```text
[2026.06.28-00.50.05:689][784]LogBlueprintUserMessages: [WBP_CompilingShadersScreen_C_2147480720] *** DECONSTRUCT
access-control-expose-headers: x-sentry-error,x-sentry-rate-limits,retry-after
[2026.06.28-00.50.05:866][784]LogMoviePlayer: Shutting down movie player
[2026.06.28-00.50.06:186][784]LogRHI: FPipelineFileCacheManager Incremental saved 215 total, 0 new, 0 removed, 0 co
[2026.06.28-00.50.06:428][784]LogHttp: Warning: 	verb=[POST] url=[https://api.live.subnautica.net/api/v1/player/log
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

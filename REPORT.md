# Subnautica 2 Telemetry Report

Live progression telemetry and configuration summary generated via SSH from gaming rig `jake@192.168.0.100`. All binary saves and plaintext configs are mirrored locally in `backups/`.

## Session Specifications
* **Game Title**: Subnautica 2 (Early Access Standalone | Unreal Engine 5)
* **Gaming Host**: `pc` (`192.168.0.100` | Windows 11 x64 | User: `jake`)
* **Platform Provider**: Steam (`OnlineSubsystemSteam` | Player ID `76561198797039235`)
* **Active Save File**: `savegame_1.sav` (1000.4 KB | Last Saved: `2026-06-16 23:29:18`)
* **Auto-Save State**: **Enabled** (`UWESaveSystemUserSetting.ini` | `bAutoSaveEnabled=True`)
* **Display Config**: `1280x720` dynamic render resolution scaling to `3840x2160` output (TSR Upscaling Quality Mode 3 | FPS Cap: 120)
* **Remote Git Repository**: `C:/Users/jake/AppData/Local/Subnautica2/Saved/.git/` (Pristine tree `4df49f6`)
* **Save Directory**: `C:/Users/jake/AppData/Local/Subnautica2/Saved/SaveGames/`
* **Log File**: `C:/Users/jake/AppData/Local/Subnautica2/Saved/Logs/Subnautica2.log`

## Equipment Status
Raw extracted equipment items and resource nodes actively discovered in workspace:

| Category | Discovered Symbols | Verification Status |
| :--- | :--- | :--- |
| **Tools** | Habitat Builder (`BP_Builder`), Scanner (`BP_Scanner`), Flashlight (`Tools_Flashlight`) | Equipped in active `AUWEBaseItem` slots. |
| **Survival Gear** | Small Oxygen Tank (`BP_OxygenTank_Small`), Basic Battery (`BP_BasicBattery`), First Aid MedKit (`BP_MedKit`) | +45.0 Max Oxygen Set Component verified. |
| **Raw Resources** | Titanium (`DA_Titanium`), Copper (`DA_Copper`), Quartz (`DA_Quartz`), Silver (`DA_Silver`), Lead (`DA_Lead`), Glass (`FullGlass`), Copper Wire (`CopperWire`) | Serialized in resource node prototypes. |

## World Traversal
Telemetry engine confirms player traversal across the following core world partitions:
1. **Safe Shallows / Main Hub** (`L_Main`)
2. **Client Lobby / Outpost** (`L_ClientLobby`)
3. **Coral Gardens** (`BP_CG_BulbFlower`, `CoralGardensRadioMessage`)
4. **Thermal Vents** (`SmallVent`, `VentFall`)
5. **Kelp Forest Border** (`KelpRandomNode`, `FeatherKelp`)

## Narrative Quests
* **Welcome Center Signal**: `DA__Signal_WelcomeCent_Hide`
* **Habitat Beacon**: `DA__Signal_Habitat_Hide`
* **Emergency Lifepod**: `Lifepod_SignalOriginal`
* **Black Box Investigation**: `CoralGardensRadioMessageBlackBox`

## Constructed Facilities
* **Base Modules**: `/Game/Art/Bases/BasePieces/Hatch/SM__ASkeletal`, `/Game/Blueprints/BaseBuilding/BP_Hatch_C`, `6Investig_BioBed__CoralGardensRadioMessageBlackBoxbChoi`, `7BioBed_TriggbayInsidChiManifest_DB`, `8Hatch`, `BP_SupplyLocker`, `BP_WorldSupplyLocker`, `BTubaJubileeP_DestroyedBiobed`
* **Discovered POIs**: `/InvesgPOI_PZ_Basecamp`, `6Investig_BioBed__CoralGardensRadioMessageBlackBoxbChoi`, `6ingBioLab_WelcomeCenter`, `CampOne`, `Lifepod_SignalOriginal`, `P/Narrative//DA__Signal_WelcomeCent_Hide`
* **World Engine Milestones**: `CrateHasBeenOpe`, `CrateHasBeenOpeItem`, `StartupItemsHaveBeenAdd`, `aFAbandonedBase`, `bStartupItemsHaveBeenAdd`, `bStartupItemsHaveBeenAdded`
* **Decoded Progression Guide**: [savegame_1_decoded.md](file:///Users/jakegarrison/Downloads/projects/subnautica-2/backups/savegame_1_decoded.md)

## Graphics Configuration
Summary extracted from [GameUserSettings.ini](file:///Users/jakegarrison/Downloads/projects/subnautica-2/backups/GameUserSettings.ini):
* **Resolution**: ResolutionSizeX=1280, ResolutionSizeY=720
* **Frame Rate Cap**: FrameRateLimit=120.000000
* **Upscaling Quality**: ScalabilityQuality_TSR=3

## Recent Engine Events
Snapshot of diagnostic gameplay session events logged by engine:

```text
[2026.06.17-06.29.26:083][848]LogBlueprintUserMessages: [WBP_CompilingShadersScreen_C_2147480838] *** DECONSTRUCT
access-control-expose-headers: x-sentry-error,x-sentry-rate-limits,retry-after
[2026.06.17-06.29.26:278][848]LogMoviePlayer: Shutting down movie player
[2026.06.17-06.29.26:794][848]LogRHI: FPipelineFileCacheManager Incremental saved 160 total, 13 new, 0 removed, 0 c
[2026.06.17-06.29.27:175][848]LogHttp: Warning: 	verb=[POST] url=[https://api.live.subnautica.net/api/v1/player/log
```

## Reference Links
* **Master Project Guide**: [README.md](file:///Users/jakegarrison/Downloads/projects/subnautica-2/README.md)
* **Previous Chat Archive**: [subnuatica_2_previous_chat.md](file:///Users/jakegarrison/Downloads/projects/subnautica-2/backups/subnuatica_2_previous_chat.md)
* **Local Engine Log Dump**: [Subnautica2.log](file:///Users/jakegarrison/Downloads/projects/subnautica-2/backups/Subnautica2.log)
* **Local Backups Vault**: [backups/](file:///Users/jakegarrison/Downloads/projects/subnautica-2/backups)
* **Developer Toolkit**: [Makefile](file:///Users/jakegarrison/Downloads/projects/subnautica-2/Makefile)
* **Scraper Automation**: [subnautica_scraper.py](file:///Users/jakegarrison/Downloads/projects/subnautica-2/subnautica_scraper.py)
* **File Sync Engine**: [sync_remote_vault.py](file:///Users/jakegarrison/Downloads/projects/subnautica-2/sync_remote_vault.py)
* **Project Changelog**: [CHANGELOG.md](file:///Users/jakegarrison/Downloads/projects/subnautica-2/CHANGELOG.md)
* **Official Website**: [subnautica.com](https://subnautica.com)

# Subnautica 2 Master Coaching Guide & Telemetry Engine

**IMPORTANT**: Live gameplay inspection snapshot generated via SSH from windows gaming host `jake@192.168.0.100`. All configuration profiles, historical chat archives, local backup vaults (`backups/`), and progress parsing automation scripts are tracked locally in the workspace directory. Remote save games and configs are version-controlled in Git (`C:/Users/jake/AppData/Local/Subnautica2/Saved/.git/`).

---

## Action Roadmap & Coaching Walkthrough

Active coaching roadmap structured in **reverse chronological order** (newest coaching instructions at the **top**, oldest completed setup milestones at the **bottom**).

### 🚀 Pending Next Steps (Active Coaching Focus)
* [ ] **TODO-8 (Base Construction)**: Travel to **Coral Gardens** (flat terrain, safe area ~350m N) and construct your starter habitat base. Build a **Foundation / Square Room**, attach a **Hatch**, install **2 Solar Panels** on the roof immediately for power/O₂, and build **4-5 Wall Lockers** inside so you can finally get dropped items off the lifepod floor!
* [ ] **TODO-7 (Cloud Sync Safety)**: Before experimenting with multiplayer cloud-share codes (`Upload to Cloud` / `Import Save`), always stow personal gear and equipment inside base lockers so Early Access character imports don't clear your inventory.
* [ ] **TODO-6 (Story Investigation)**: Track down and investigate the **Coral Gardens Radio Message / Black Box** emergency transmission signal.
* [ ] **TODO-5 (Depth & Survival Upgrades)**: Craft a higher-capacity **Standard Oxygen Tank** (using discovered Silver/Wiring Kit) and a **Rebreather** to scout deeper West/Northwest trenches.
* [ ] **TODO-4 (Vehicle Scouting)**: Explore Thermal Vents and Kelp borders to locate and scan vehicle fragments (`Seaglide`, submersible modules).

### ✅ Completed Tasks & Setup History (Oldest at Bottom)
* [x] **TODO-3 (Remote Git Rollback Engine)**: Version-controlled remote Windows save directory `C:/Users/jake/AppData/Local/Subnautica2/Saved/` (`.git` commit `4df49f6`) with custom `.gitignore` to prevent save corruption and enable gameplay rollback.
* [x] **TODO-2 (Telemetry Bridge Setup)**: Configured local SSH scraper `subnautica_scraper.py` and developer toolkit `Makefile` locally to inspect live Unreal Engine 5 saves (`savegame_1.sav`) on gaming PC (`192.168.0.100`).
* [x] **TODO-1 (First Base Shopping List & Tool Crafting)**: Scouted ~239m W into **Infected Crevasse** (near Infected Angel Bloom), extracted spiky grey Silver nodes from narrow crawlspace veins, collected Titanium/Quartz/Copper, and crafted the **Habitat Builder** tool (`BP_Builder`).

---

## Game Coaching & Guide: Journey Assessment

Synthesis of past chat coaching combined with live binary save inspection (`savegame_1.sav`).

### 1. Where You Currently Are
* **Resource Hoarding Phase**: You successfully scouted the **Infected Crevasse** (~239m West of lifepod) near the Infected Angel Bloom landmark. By checking halfway up the cliff walls and hidden crawlspace tunnels for spiky grey metallic rocks, you secured **Silver** alongside Titanium, Copper, and Quartz.
* **Storage Overflow**: You returned to the emergency lifepod, crafted your **Habitat Builder** tool (`BP_Builder`), but completely ran out of container storage, leaving spare gathered materials dropped on the floor.

### 2. Immediate Coaching Walkthrough: Your First Habitat Base
To resolve storage bottlenecks and unlock interior crafting:
1. **Pick the Site**: Swim to **Coral Gardens** (or a flat sandy shelf near your lifepod). Flat terrain prevents clipping errors.
2. **Build Core Frame**: Place a basic room/corridor and attach a **Side Hatch** for entry.
3. **Energize Immediately**: Place **2 Solar Panels** on the roof. Without external power, the habitat will not generate breathable oxygen inside.
4. **Deploy Wall Lockers**: Step inside and construct 4 to 5 **Wall Lockers**. Transfer all floor clutter and excess Titanium/Quartz into these organized containers.

---

## Multiplayer Cloud Sharing & Save Hygiene S.O.P.

Reference documentation coaching on Subnautica 2 Early Access multiplayer snapshot semantics.

### 1. Manual Snapshot Semantics (Not Live Lobby)
The built-in cloud-share system in Subnautica 2 is an asynchronous **copy/paste snapshot tool**, not a live cloud synchronized lobby.
* **Host Sharing**: Person A clicks **"Upload to Cloud"** from the main menu. The server generates a unique one-time-use **8-digit share code**.
* **Guest Importing**: Person B enters this code via **"Import Save"**. Person B receives an exact isolated local clone of Person A's world. Any subsequent building Person B does solo exists **solely on Person B's PC**.

### 2. "Pass the Torch" Re-Sync Workflow
To merge Person B's solo base expansions back to Person A:
1. Person B saves solo progress, returns to main menu, clicks **"Upload to Cloud"**, and generates a **new 8-digit code**.
2. Person B transmits this code to Person A.
3. Person A clicks **"Import Save"** and inputs the new code, overwriting their older local save tree with Person B's progressed world.

> [!WARNING]
> **Zero Merge Capability**: If Person A and Person B both play solo on diverged copies simultaneously, their worlds cannot be merged. Only one designated player should progress the master save solo at any time.

> [!CAUTION]
> **Early Access Inventory Reset Bug**: Importing cloud saves frequently resets personal player inventories or respawns characters at the starter pod. **Always deposit all gear, tools, and raw minerals into a base wall locker before uploading or importing cloud codes.**

*Community Tools*: For PC Steam players seeking automated syncing, community utilities like [SaveSync](https://savesync.games) run background daemons to automatically push/pull save snapshots on session exit (discussed on [Reddit](https://www.reddit.com) and [Steam Community](https://steamcommunity.com)).

---

## Telemetry Capabilities & Refresh Scope Matrix

Catalog of progression registers and configuration parameters to distinguish between live refreshed data and static curated coaching.

| Telemetry Category | Evaluated Registers & Game Fields | Refresh Behavior | Source File & Extraction Method |
| :--- | :--- | :--- | :--- |
| **Save File Geometry** | File size, modification timestamp, backup `.bak` counts | **Live Refreshed** | Scraped via `os.path.getsize` on `savegame_1.sav` |
| **Equipped Survival Gear**| Hotbar symbols (`BP_Builder`, `BP_Scanner`, `BP_OxygenTank_Small`) | **Live Refreshed** | Binary regex extraction of `AUWEBaseItem` instances |
| **Gathered Resources** | Raw ore inventory (`DA_Titanium`, `DA_Quartz`, `DA_Copper`, `DA_Silver`)| **Live Refreshed** | Binary regex extraction of serialized resource prototypes |
| **Visited Map Partitions**| Hub zones (`L_Main`, `L_ClientLobby`, `CoralGardens`, `ThermalVents`) | **Live Refreshed** | Serialized world partition loading strings |
| **Unlocked PDA Tech** | Base pieces (`BP_Hatch`, `WallLocker`), flora/fauna scans | **Live Refreshed** | Serialized `Blueprint` and `Unlocked` symbol flags |
| **Radio & Quests** | Active narrative signals (`WelcomeCent`, `HabitatSignal`, `BlackBox`) | **Live Refreshed** | Serialized `StoryGoal` and `Transmission` objects |
| **Graphics & Engine INIs**| Dynamic resolution, TSR mode, 120 FPS limit, auto-save state | **Live Refreshed** | Plaintext parsing of `GameUserSettings.ini` |
| **Remote Version Control**| Active Git commit hash of remote save tree | **Live Refreshed** | Queried via `git rev-parse --short HEAD` over SSH |
| **Local Vault Backups**| Synchronized binary `.sav` files flat in `backups/`| **Live Refreshed** | Transferred via `make pull` base64 SFTP helper |
| **Action Roadmap** | Reverse-chronological coaching instructions (`TODO-4` to `8`)| **Static Guidance**| Curated coaching milestones documented manually |
| **Multiplayer S.O.P.** | Manual 8-digit cloud copy/paste semantics & gotchas | **Static Guidance**| Technical reference synthesized from community research |

---

## Live Telemetry & Progression Matrix

Master reference and telemetry status snapshot for current save file.

### Session Specifications
* **Game Title**: Subnautica 2 (Early Access v0.10.3 | Unreal Engine 5 Standalone)
* **Gaming Host**: `pc` (`192.168.0.100` | Windows 11 x64 | User: `jake`)
* **Platform Provider**: Steam (`OnlineSubsystemSteam` | Player ID `76561198797039235`)
* **Active Save File**: `savegame_1.sav` (1000.4 KB | Last Saved: `2026-06-16 23:29:18`)
* **Auto-Save State**: **Enabled** (`UWESaveSystemUserSetting.ini` | `bAutoSaveEnabled=True`)
* **Display Config**: `1280x720` dynamic render resolution scaling to `3840x2160` output (TSR Upscaling Quality Mode 3 | FPS Limit: 120)
* **Remote Git Repository**: `C:/Users/jake/AppData/Local/Subnautica2/Saved/.git/` (On Windows PC | Pristine tree `4df49f6`)
* **Save Directory**: `C:/Users/jake/AppData/Local/Subnautica2/Saved/SaveGames/`
* **Log File**: `C:/Users/jake/AppData/Local/Subnautica2/Saved/Logs/Subnautica2.log`

### Live Inventory & Equipment Matrix
Raw extracted equipment items and resource nodes actively discovered in workspace:

| Category | Discovered Symbols & Items | Telemetry Verification |
| :--- | :--- | :--- |
| **Tools & Equipment matrix** | Habitat Builder (`BP_Builder`), Scanner (`BP_Scanner`), Flashlight (`Tools_Flashlight`) | Equipped in active `AUWEBaseItem` slots. |
| **Survival Gear** | Small Oxygen Tank (`BP_OxygenTank_Small`), Basic Battery (`BP_BasicBattery`), First Aid MedKit (`BP_MedKit`) | +45.0 Max Oxygen Set Component verified. |
| **Raw Resources** | Titanium (`DA_Titanium`), Copper (`DA_Copper`), Quartz (`DA_Quartz`), Silver (`DA_Silver`), Lead (`DA_Lead`), Glass (`FullGlass`), Copper Wire (`CopperWire`) | Serialized in resource node prototypes. |

### Map Discovery & Biomes Visited
Telemetry engine confirms player traversal across the following core world partitions:
1. **Safe Shallows / Main Hub** (`/Game/Maps/Main/L_Main`)
2. **Client Lobby / Outpost** (`/Game/Maps/L_ClientLobby`)
3. **Coral Gardens** (`BP_CG_BulbFlower`, `CoralGardensRadioMessage`)
4. **Thermal & Volcanic Vents** (`SmallVent`, `VentFall`)
5. **Kelp Forest Border** (`KelpRandomNode`, `FeatherKelp`)

### Narrative & Quest Signals
* **Welcome Center Signal**: `DA__Signal_WelcomeCent_Hide`
* **Habitat Beacon**: `DA__Signal_Habitat_Hide`
* **Emergency Lifepod**: `Lifepod_SignalOriginal`
* **Black Box Investigation**: `CoralGardensRadioMessageBlackBox`

### Rich Gameplay Progression & World State
* **Constructed Facilities & Storage**: `/Game/Art/Bases/BasePieces/Hatch/SM__ASkeletal`, `/Game/Blueprints/BaseBuilding/BP_Hatch_C`, `6Investig_BioBed__CoralGardensRadioMessageBlackBoxbChoi`, `7BioBed_TriggbayInsidChiManifest_DB`, `8Hatch`, `BP_SupplyLocker`, `BP_WorldSupplyLocker`, `BTubaJubileeP_DestroyedBiobed`
* **Discovered POIs & Outposts**: `/InvesgPOI_PZ_Basecamp`, `6Investig_BioBed__CoralGardensRadioMessageBlackBoxbChoi`, `6ingBioLab_WelcomeCenter`, `CampOne`, `Lifepod_SignalOriginal`, `P/Narrative//DA__Signal_WelcomeCent_Hide`
* **World Engine Milestones**: `CrateHasBeenOpe`, `CrateHasBeenOpeItem`, `StartupItemsHaveBeenAdd`, `aFAbandonedBase`, `bStartupItemsHaveBeenAdd`, `bStartupItemsHaveBeenAdded`
* **Decoded Progression Guide**: [savegame_1_decoded.md](file:///Users/jakegarrison/Downloads/projects/subnautica-2/backups/savegame_1_decoded.md) (Complete decoded catalog of all 216 extracted world progression registers across 5 domain classifications)

---

## Recent Log Telemetry

Snapshot of last 5 diagnostic gameplay session events logged by engine:

```text
[2026.06.17-06.29.26:083][848]LogBlueprintUserMessages: [WBP_CompilingShadersScreen_C_2147480838] *** DECONSTRUCT
access-control-expose-headers: x-sentry-error,x-sentry-rate-limits,retry-after
[2026.06.17-06.29.26:278][848]LogMoviePlayer: Shutting down movie player
[2026.06.17-06.29.26:794][848]LogRHI: FPipelineFileCacheManager Incremental saved 160 total, 13 new, 0 removed, 0 c
[2026.06.17-06.29.27:175][848]LogHttp: Warning: 	verb=[POST] url=[https://api.live.subnautica.net/api/v1/player/log
```

---

## Reference Links & Files

* **Local Master Guide**: [subnautica.md](file:///Users/jakegarrison/Downloads/projects/subnautica-2/subnautica.md)
* **Previous Chat Archive**: [subnuatica_2_previous_chat.md](file:///Users/jakegarrison/Downloads/projects/subnautica-2/backups/subnuatica_2_previous_chat.md)
* **Local Engine Log Dump**: [Subnautica2.log](file:///Users/jakegarrison/Downloads/projects/subnautica-2/backups/Subnautica2.log)
* **Local Backups Vault (`backups/`)**: [backups/](file:///Users/jakegarrison/Downloads/projects/subnautica-2/backups)
* **Developer Toolkit**: [Makefile](file:///Users/jakegarrison/Downloads/projects/subnautica-2/Makefile)
* **Scraper Automation**: [subnautica_scraper.py](file:///Users/jakegarrison/Downloads/projects/subnautica-2/subnautica_scraper.py)
* **File Sync Engine**: [sync_remote_vault.py](file:///Users/jakegarrison/Downloads/projects/subnautica-2/sync_remote_vault.py)
* **Remote Git Tree**: `C:/Users/jake/AppData/Local/Subnautica2/Saved/.git/`
* **Remote Save Path**: `C:/Users/jake/AppData/Local/Subnautica2/Saved/SaveGames/`
* **Project Changelog**: [CHANGELOG.md](file:///Users/jakegarrison/Downloads/projects/subnautica-2/CHANGELOG.md)
* **Official Website**: [subnautica.com](https://subnautica.com)
* **Live API Endpoint**: [api.live.subnautica.net](https://api.live.subnautica.net)
* **SaveSync Community Tool**: [savesync.games](https://savesync.games)

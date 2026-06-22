# Subnautica 2 Telemetry Toolkit

A dedicated engineering toolkit and automated coaching bridge for **Subnautica 2** (Early Access Standalone / Unreal Engine 5). This repository connects to a remote Windows 11 gaming rig over SSH (`192.168.0.100`), inspects live binary Unreal Engine 5 SaveGame files (`.sav`), synchronizes save vaults locally, and generates clinical coaching walkthroughs and diagnostic telemetry reports ([REPORT.md](file:///Users/jakegarrison/Downloads/projects/subnautica-2/REPORT.md)).

## Features
- **Remote Telemetry Bridge**: Connects to the gaming rig (`jake@192.168.0.100`), runs Python regex parsers against binary save files, and extracts player inventory, equipped tools, and visited biomes.
- **File Synchronization**: Bi-directional base64 transfer tool (`sync_remote_vault.py`) that pulls binary saves (`.sav`) and engine config profiles (`GameUserSettings.ini`) flat into local backups (`backups/`).
- **SaveGame Decoder**: Plaintext converter (`decode_sav.py`) that filters out boilerplate UE5 serialization noise and dumps progression registers to markdown guides.
- **Remote Rollback**: Tracks remote progression states directly inside `C:/Users/jake/AppData/Local/Subnautica2/Saved/.git` on the gaming host, preventing save corruption.
- **Diagnostic Telemetry**: Synthesizes live binary save inspection and GameUserSettings.ini profiles into [REPORT.md](file:///Users/jakegarrison/Downloads/projects/subnautica-2/REPORT.md).

## Action Roadmap
Active coaching roadmap structured in reverse chronological order (newest coaching instructions at the top, oldest completed milestones at the bottom).

### Pending Focus
* [ ] **TODO-8 (Base Construction)**: Travel to **Coral Gardens** (flat terrain, safe area ~350m N) and construct your starter habitat base. Build a Foundation / Square Room, attach a Hatch, install 2 Solar Panels on the roof immediately for power/O₂, and build 4-5 Wall Lockers inside so you can finally get dropped items off the lifepod floor!
* [ ] **TODO-7 (Cloud Sync Safety)**: Before experimenting with multiplayer cloud-share codes (`Upload to Cloud` / `Import Save`), always stow personal gear and equipment inside base lockers so Early Access character imports don't clear your inventory.
* [ ] **TODO-6 (Story Investigation)**: Track down and investigate the **Coral Gardens Radio Message / Black Box** emergency transmission signal.
* [ ] **TODO-5 (Depth Upgrades)**: Craft a higher-capacity Standard Oxygen Tank (using discovered Silver/Wiring Kit) and a Rebreather to scout deeper West/Northwest trenches.
* [ ] **TODO-4 (Vehicle Scouting)**: Explore Thermal Vents and Kelp borders to locate and scan vehicle fragments (`Seaglide`, submersible modules).

### Completed Setup
* [x] **TODO-3 (Remote Git Rollback Engine)**: Version-controlled remote Windows save directory `C:/Users/jake/AppData/Local/Subnautica2/Saved/` with custom `.gitignore` to prevent save corruption.
* [x] **TODO-2 (Telemetry Bridge Setup)**: Configured local SSH scraper `subnautica_scraper.py` and developer toolkit `Makefile` locally to inspect live Unreal Engine 5 saves on gaming PC (`192.168.0.100`).
* [x] **TODO-1 (First Base Shopping List)**: Scouted ~239m W into Infected Crevasse, extracted Silver nodes from narrow crawlspace veins, collected Titanium/Quartz/Copper, and crafted the Habitat Builder tool (`BP_Builder`).

## Journey Assessment
Synthesis of past chat coaching combined with live binary save inspection (`savegame_1.sav`).

### Current Status
* **Resource Hoarding Phase**: You successfully scouted the Infected Crevasse (~239m West of lifepod) near the Infected Angel Bloom landmark. By checking halfway up cliff walls and crawlspace tunnels, you secured Silver alongside Titanium, Copper, and Quartz.
* **Storage Overflow**: You returned to the emergency lifepod, crafted your Habitat Builder tool (`BP_Builder`), but completely ran out of container storage, leaving spare gathered materials dropped on the floor.

### First Base Walkthrough
To resolve storage bottlenecks and unlock interior crafting:
1. **Pick the Site**: Swim to Coral Gardens (or a flat sandy shelf near your lifepod). Flat terrain prevents clipping errors.
2. **Build Core Frame**: Place a basic room/corridor and attach a Side Hatch for entry.
3. **Energize Immediately**: Place 2 Solar Panels on the roof. Without external power, the habitat will not generate breathable oxygen inside.
4. **Deploy Lockers**: Step inside and construct 4 to 5 Wall Lockers. Transfer all floor clutter and excess Titanium/Quartz into these organized containers.

## Multiplayer SOP
Reference documentation on Subnautica 2 Early Access multiplayer cloud copy/paste snapshot semantics.

### Snapshot Semantics
The built-in cloud-share system in Subnautica 2 is an asynchronous copy/paste snapshot tool, not a live cloud synchronized lobby.
* **Host Sharing**: Person A clicks "Upload to Cloud" from the main menu. The server generates a unique 8-digit share code.
* **Guest Importing**: Person B enters this code via "Import Save". Person B receives an isolated local clone of Person A's world. Any subsequent building Person B does solo exists solely on Person B's PC.

### Torch Re-Sync Workflow
To merge Person B's solo base expansions back to Person A:
1. Person B saves solo progress, returns to main menu, clicks "Upload to Cloud", and generates a new 8-digit code.
2. Person B transmits this code to Person A.
3. Person A clicks "Import Save" and inputs the new code, overwriting their older local save tree.

> [!WARNING]
> **Zero Merge Capability**: If Person A and Person B both play solo on diverged copies simultaneously, their worlds cannot be merged. Only one designated player should progress the master save solo at any time.

> [!CAUTION]
> **Early Access Inventory Reset Bug**: Importing cloud saves frequently resets player inventories or respawns characters at the starter pod. Always deposit all gear, tools, and raw minerals into a base locker before uploading or importing cloud codes.

## Telemetry Capabilities
Catalog of progression registers and config parameters to distinguish between live refreshed data and static curated coaching.

| Category | Evaluated Registers | Refresh Behavior | Extraction Method |
| :--- | :--- | :--- | :--- |
| **Save Geometry** | File size, modification timestamp, backup counts | Live Refreshed | Scraped via `os.path.getsize` on `savegame_1.sav` |
| **Equipped Gear** | Hotbar symbols (`BP_Builder`, `BP_Scanner`, `BP_OxygenTank_Small`) | Live Refreshed | Binary regex extraction of `AUWEBaseItem` instances |
| **Gathered Ore** | Raw ore inventory (`DA_Titanium`, `DA_Quartz`, `DA_Copper`) | Live Refreshed | Binary regex extraction of serialized resource prototypes |
| **Visited Zones** | Hub zones (`L_Main`, `L_ClientLobby`, `CoralGardens`) | Live Refreshed | Serialized world partition loading strings |
| **Unlocked Tech** | Base pieces (`BP_Hatch`, `WallLocker`), flora scans | Live Refreshed | Serialized Blueprint and Unlocked symbol flags |
| **Narrative Quests**| Narrative signals (`WelcomeCent`, `HabitatSignal`, `BlackBox`) | Live Refreshed | Serialized StoryGoal and Transmission objects |
| **Graphics Profiles**| Render resolution, TSR mode, 120 FPS limit | Live Refreshed | Plaintext parsing of `GameUserSettings.ini` |
| **Remote VCS** | Active Git commit hash of remote save tree | Live Refreshed | Queried via `git rev-parse` over SSH |
| **Vault Backups** | Synchronized binary `.sav` files flat in `backups/` | Live Refreshed | Transferred via `make pull` base64 SFTP helper |
| **Action Roadmap** | Reverse-chronological coaching instructions | Static Guidance | Curated coaching milestones documented manually |
| **Multiplayer SOP** | Manual 8-digit cloud copy/paste semantics | Static Guidance | Technical reference synthesized from community research |

## Structure
| File | Description |
| :--- | :--- |
| [subnautica_scraper.py](file:///Users/jakegarrison/Downloads/projects/subnautica-2/subnautica_scraper.py) | Main telemetry scraper and diagnostic report generator. |
| [decode_sav.py](file:///Users/jakegarrison/Downloads/projects/subnautica-2/decode_sav.py) | Unreal Engine 5 SaveGame binary decoder. |
| [sync_remote_vault.py](file:///Users/jakegarrison/Downloads/projects/subnautica-2/sync_remote_vault.py) | Bi-directional base64 file synchronization bridge over SSH. |
| [Makefile](file:///Users/jakegarrison/Downloads/projects/subnautica-2/Makefile) | Developer CLI automation targets. |
| [REPORT.md](file:///Users/jakegarrison/Downloads/projects/subnautica-2/REPORT.md) | Generated live progression telemetry and game settings report. |
| [CHANGELOG.md](file:///Users/jakegarrison/Downloads/projects/subnautica-2/CHANGELOG.md) | Chronological ledger recording developer milestones. |
| `backups/` | Local flat archive containing synced `.sav` files, INI configs, and logs. |

## Usage
Use the included [Makefile](file:///Users/jakegarrison/Downloads/projects/subnautica-2/Makefile) to manage remote inspection and vault sync:

```bash
# Scrape live save game over SSH and regenerate REPORT.md
make report

# Pull remote save games and config INIs locally
make pull

# Decode local backup saves and format guides
make format

# Check remote Git save repo status on gaming PC
make git-status
```

## Reference Links
* **Diagnostic Report**: [REPORT.md](file:///Users/jakegarrison/Downloads/projects/subnautica-2/REPORT.md)
* **Previous Chat Archive**: [subnuatica_2_previous_chat.md](file:///Users/jakegarrison/Downloads/projects/subnautica-2/backups/subnuatica_2_previous_chat.md)
* **Engine Log Dump**: [Subnautica2.log](file:///Users/jakegarrison/Downloads/projects/subnautica-2/backups/Subnautica2.log)
* **Backups Vault**: [backups/](file:///Users/jakegarrison/Downloads/projects/subnautica-2/backups)
* **Changelog**: [CHANGELOG.md](file:///Users/jakegarrison/Downloads/projects/subnautica-2/CHANGELOG.md)
* **Official Website**: [subnautica.com](https://subnautica.com)

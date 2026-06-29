# Subnautica 2 Telemetry Toolkit

A dedicated engineering toolkit and automated coaching bridge for **Subnautica 2** (Early Access Standalone / Unreal Engine 5). This repository connects to a remote Windows 11 gaming rig over SSH (`192.168.0.100`), inspects live binary Unreal Engine 5 SaveGame files (`.sav`), synchronizes save vaults locally, and generates clinical coaching walkthroughs and diagnostic telemetry reports ([REPORT.md](./REPORT.md)).

## Features
- **Remote Telemetry Bridge**: Connects to the gaming rig (`jake@192.168.0.100`), runs Python regex parsers against binary save files, and extracts player inventory, equipped tools, and visited biomes.
- **File Synchronization**: Bi-directional base64 transfer tool (`sync_remote_vault.py`) that pulls binary saves (`.sav`) and engine config profiles (`GameUserSettings.ini`) flat into local backups (`backups/`).
- **SaveGame Decoder**: Plaintext converter (`decode_sav.py`) that filters out boilerplate UE5 serialization noise and dumps progression registers to markdown guides.
- **Remote Rollback**: Tracks remote progression states directly inside `C:/Users/jake/AppData/Local/Subnautica2/Saved/.git` on the gaming host, preventing save corruption.
- **Diagnostic Telemetry**: Synthesizes live binary save inspection and GameUserSettings.ini profiles into [REPORT.md](./REPORT.md).

## 📚 Documentation

This repository enforces a strict separation of concerns across its core Markdown documents to ensure seamless navigation between live telemetry, macro strategy, and granular checklists:

| Document | Primary Scope | Update Lifecycle |
| :--- | :--- | :--- |
| **[README.md](./README.md)** | Technical project architecture, SSH telemetry bridge pipeline capabilities, SaveGame parser de-noising boundaries, and developer CLI automation targets (`Makefile`). | Updated when tooling or bridge features expand. |
| **[REPORT.md](./REPORT.md)** | **Live Diagnostic Telemetry**: Dynamic progression state, equipped tool loadouts, gathered ore registers, spatial base coordinates (`X, Y, Z`), and loaded world partition flags decoded from `savegame_1.sav`. | **Dynamically regenerated** on every `make report` run. |
| **[GUIDE.md](./GUIDE.md)** | **High-Level Progression Guide & Compendium**: Macro progression phases (Phases 1–4 without spoilers), clinical biome geometry matrix, beginner survival wisdom, transition criteria, and official dev news links. | Static reference updated for new game updates. |
| **[TODO.md](./TODO.md)** | **Immediate Action Roadmap**: Actionable pending checklists sequenced for efficient geographic sweeps (crafting milestones, shopping lists, and systematic exploration verification SOPs). | Updated as items are completed in-game. |
| **[MULTIPLAYER.md](./MULTIPLAYER.md)**| **Multiplayer Cloud Sharing & Save SOP**: Clinical reference on Subnautica 2 cloud copy/paste snapshot semantics, Pass the Torch re-sync protocol, inventory reset gotchas, and automated background daemons. | Static reference synthesized from community research. |
| **[CHANGELOG.md](./CHANGELOG.md)** | **Reverse-Chronological Ledger**: Historical record of completed coaching milestones and base construction achievements. | Updated whenever pending TODOs are completed. |

## Architecture & Capabilities
This repository automates live gameplay inspection, file synchronization, and clinical coaching guide generation using a three-tier telemetry bridge:
1. **Live Remote Scraping (`make report`)**: Connects to the gaming rig (`jake@192.168.0.100`) via SSH, inspects active binary Unreal Engine 5 SaveGame files (`.sav`) and `GameUserSettings.ini`, and synthesizes diagnostic summaries into [REPORT.md](./REPORT.md).
2. **Vault Synchronization (`make pull` / `make push`)**: Bi-directional base64 transfer engine (`subnautica_scraper.py`) that mirrors remote `.sav` vaults and configuration profiles flat into local archives (`backups/`).
3. **SaveGame Decoder (`make decode`)**: Strips UE5 serialization noise from binary save archives, extracts progression registers (`backups/savegame_1_decoded.md`), and updates [TODO.md](./TODO.md).
4. **Remote Git Rollback Engine**: Tracks remote progression states directly inside `C:/Users/jake/AppData/Local/Subnautica2/Saved/.git` on the gaming PC, preventing save corruption.

## Multiplayer
For comprehensive guidelines on Subnautica 2 Early Access multiplayer cloud copy/paste snapshot semantics, "Pass the Torch" re-sync protocols, inventory reset bugs, and third-party background syncing daemons (`SaveSync`), consult [MULTIPLAYER.md](./MULTIPLAYER.md).

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
| **Action Roadmap** | Reverse-chronological coaching instructions | Static Guidance | Curated coaching milestones in [TODO.md](./TODO.md) |
| **Multiplayer SOP** | Manual 8-digit cloud copy/paste semantics | Static Guidance | Technical reference synthesized from community research |

## SaveGame Telemetry Scope

When inspecting live binary Unreal Engine 5 `.sav` files (`savegame_1.sav`), the telemetry scraper distinguishes between raw serialized registers and manual player verification requirements.

### What CAN Be Extracted / Inferred
- **Equipped Gear & Hotbar Items**: Serialized instances of `AUWEBaseItem` (e.g., `BP_Builder`, `BP_Scanner`, `Tools_Flashlight`, `BP_OxygenTank_Small`).
- **Constructed Base Modules**: Serialized world partition blueprint prototypes (`BP_Hatch_C`, `BP_WorldSupplyLocker`, `SolarPanel`, `BioBed`).
- **Gathered Ores & Resources**: Serialized resource node prototypes (`DA_Titanium`, `DA_Silver`, `DA_Copper`, `DA_Quartz`, `FullGlass`, `CopperWire`).
- **Major StoryGoal & Signal Flags**: High-level narrative flags and unlocked signals (`DA__Signal_WelcomeCent_Hide`, `DA__Signal_Habitat_Hide`, `CoralGardensRadioMessageBlackBox`, `Lifepod_SignalOriginal`, `ColonistBunker052`).
- **Unlocked Blueprints**: Fully researched blueprint symbols listed under `::Unlocked` or standard craftable items.
- **World Partitions Visited**: Instantiated world streaming regions (`L_Main`, `CoralGardens`).
- **Engine & Graphics Configs**: Render resolutions, upscaling modes, and FPS caps from `GameUserSettings.ini`.

### What CANNOT Be Extracted / Inferred Reliably
- **Partial Fragment Scan Counts (e.g., 1/3 Seaglide Scanned)**: Unreal Engine 5 SaveGames serialize complete blueprint unlock flags (`::Unlocked`) once fully researched, but intermediate scanning progress (e.g., scanning 1 out of 3 vehicle fragments or 1 out of 2 interior lab benches) is packed into compressed binary property structs that do not expose plaintext ASCII strings.
- **Individual PDA Datapad Journal & Audio Text**: While StoryGoal triggers confirm that a narrative landmark was reached, the exact plaintext datapad entries read by the player are indexed internally by localization keys (e.g., `StringTs/Phase2Narratives/...`) rather than saved as raw strings.
- **Precise Quantities per Individual Storage Locker**: While gathered resource types (`DA_Silver`, `DA_Titanium`) are detected in the serialized registry, mapping exact item counts to specific individual `BP_WorldSupplyLocker` containers requires full struct deserialization of UE5 property arrays.
- **Unexplored / Missing Map POIs**: The binary save file only contains records for entities and streaming regions that have been instantiated or visited. Unscanned tech fragments or unvisited alien artifacts in unexplored ravines leave zero footprint in `.sav` files.

## Structure
| File | Description |
| :--- | :--- |
| [subnautica_scraper.py](subnautica_scraper.py) | Unified telemetry scraper, vault sync engine, and binary save decoder. |
| [Makefile](Makefile) | Developer CLI automation targets. |
| [TODO.md](TODO.md) | Active exploration tracker, crafting milestones, and habitat progression roadmap. |
| [REPORT.md](REPORT.md) | Generated live progression telemetry and game settings report. |
| [CHANGELOG.md](CHANGELOG.md) | Chronological ledger recording developer milestones. |
| `backups/` | Local flat archive containing synced `.sav` files, INI configs, and logs. |

## Usage
Use the included [Makefile](Makefile) to manage remote inspection and vault sync:


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

## Archive
* **Previous Chat Archive**: [subnuatica_2_previous_chat.md](./backups/subnuatica_2_previous_chat.md)
* **Engine Log Dump**: [Subnautica2.log](./backups/Subnautica2.log)
* **Backups Vault**: [backups/](./backups)

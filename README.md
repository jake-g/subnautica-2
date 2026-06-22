# 🌊 Subnautica 2 Telemetry Toolkit & Progression Engine

A dedicated engineering toolkit and automated coaching bridge for **Subnautica 2** (Early Access Standalone / Unreal Engine 5). This repository connects to a remote Windows 11 gaming rig over SSH (`192.168.0.100`), inspects live binary Unreal Engine 5 SaveGame files (`.sav`), synchronizes save vaults locally, and generates dynamic clinical coaching walkthroughs and progression matrix guides.

## ✨ Key Features

- **📡 Remote SSH Telemetry Bridge**: Automatically connects to the gaming rig (`jake@192.168.0.100`), executes Python regular expression parsers against binary save files, and extracts player inventory, equipped tools, and visited biomes.
- **🔄 Flat File Synchronization Engine**: Bi-directional base64 transfer tool (`sync_remote_vault.py`) that pulls binary saves (`.sav`) and engine configuration profiles (`GameUserSettings.ini`) flat into local backups (`backups/`), bypassing Windows OpenSSH SCP negotiation bugs.
- **🧬 Binary SaveGame Decoder**: Clinical plaintext converter (`decode_sav.py`) that filters out boilerplate UE5 object serialization noise and dumps high-fidelity progression registers to structured markdown guides.
- **🛡️ Remote Git Rollback Engine**: Tracks remote progression states directly inside `C:/Users/jake/AppData/Local/Subnautica2/Saved/.git` on the gaming host, preventing save corruption and enabling gameplay rollback.
- **🧭 Master Coaching Walkthrough**: Synthesizes live binary save inspection with historical chat archives to generate [subnautica.md](file:///Users/jakegarrison/Downloads/projects/subnautica-2/subnautica.md) with reverse-chronological action roadmaps and multiplayer cloud-share SOPs.

## 📂 Repository Structure

| File / Folder | Description |
| :--- | :--- |
| [subnautica_scraper.py](file:///Users/jakegarrison/Downloads/projects/subnautica-2/subnautica_scraper.py) | Main telemetry scraper and master coaching guide generator. |
| [decode_sav.py](file:///Users/jakegarrison/Downloads/projects/subnautica-2/decode_sav.py) | Unreal Engine 5 SaveGame binary decoder and guide generator. |
| [sync_remote_vault.py](file:///Users/jakegarrison/Downloads/projects/subnautica-2/sync_remote_vault.py) | Bi-directional base64 file synchronization bridge over SSH. |
| [Makefile](file:///Users/jakegarrison/Downloads/projects/subnautica-2/Makefile) | Developer CLI automation targets (`make report`, `make pull`, `make status`). |
| [subnautica.md](file:///Users/jakegarrison/Downloads/projects/subnautica-2/subnautica.md) | Generated master coaching walkthrough and progression telemetry report. |
| [CHANGELOG.md](file:///Users/jakegarrison/Downloads/projects/subnautica-2/CHANGELOG.md) | Chronological ledger recording developer milestones and feature additions. |
| `backups/` | Local flat archive containing synced `.sav` files, INI configs, and logs. |

## 🚀 Quickstart & CLI Usage

Use the included [Makefile](file:///Users/jakegarrison/Downloads/projects/subnautica-2/Makefile) to manage remote inspection and vault synchronization:

```bash
# Scrape live Windows save game over SSH and regenerate subnautica.md report
make report

# Pull remote Unreal Engine save games and config INIs into local backups/
make pull

# Decode all local backup save files and format progression guides
make format

# Check remote Git save repository status on gaming PC
make git-status
```

## 📈 Current Progression Status

- **Current Location**: ~239m West of emergency lifepod in **Infected Crevasse** (mined crawlspace veins for Silver ore).
- **Active Focus**: Base construction at **Coral Gardens** (~350m North) to resolve inventory storage bottlenecks.
- **Equipped Gear**: Habitat Builder (`BP_Builder`), Scanner (`BP_Scanner`), Flashlight (`Tools_Flashlight`), Small Oxygen Tank (+45 O₂).

---
*For detailed progression history, see [CHANGELOG.md](file:///Users/jakegarrison/Downloads/projects/subnautica-2/CHANGELOG.md) and [subnautica.md](file:///Users/jakegarrison/Downloads/projects/subnautica-2/subnautica.md).*

# Makefile for Subnautica 2 Telemetry Scraping, Diagnostics, and Remote Inspection.

PC_SSH ?= jake@192.168.0.100
REMOTE_SAVE_ROOT ?= C:/Users/jake/AppData/Local/Subnautica2/Saved
LOCAL_SCRIPT ?= subnautica_scraper.py

.PHONY: help report status configs pull push pull-saves push-saves sync format decode git-status git-log git-diff snapshot ssh logs tail test lint

help:
	@echo "===================================================================="
	@echo "                Subnautica 2 Telemetry Toolkit                    "
	@echo "===================================================================="
	@echo "Telemetry & Reporting:"
	@echo "  make report     - Scrape live Windows save games over SSH and update report"
	@echo "  make format     - Re-format progression guides and auto-decode all saves"
	@echo "  make status     - Query active save files and modification dates over SSH"
	@echo "  make configs    - Dump active GameUserSettings.ini graphics/fps settings"
	@echo ""
	@echo "File Synchronization & Vault Management (Mac <-> Windows PC):"
	@echo "  make pull       - Synchronize remote saves (.sav) and INIs into local backups"
	@echo "  make push       - Push local backup vault files back to remote gaming host"
	@echo "  make sync       - Bi-directional pull snapshot helper"
	@echo ""
	@echo "Version Control & Rollback (Remote Windows PC Git):"
	@echo "  make git-status - Check working tree status of remote save repository"
	@echo "  make git-log    - View recent save and config snapshot commit history"
	@echo "  make git-diff   - Inspect unstaged modifications to INIs or .sav files"
	@echo "  make snapshot   - Stage and commit current progression state over SSH"
	@echo ""
	@echo "Diagnostics & Logs:"
	@echo "  make logs       - View last 50 lines of live Subnautica2.log engine log"
	@echo "  make tail       - Stream real-time engine log output during gameplay"
	@echo ""
	@echo "Remote Access:"
	@echo "  make ssh        - Open interactive SSH terminal session into gaming PC"
	@echo "===================================================================="

report:
	@echo "-> Triggering Subnautica 2 save game inspection over SSH ($(PC_SSH))..."
	python3 $(LOCAL_SCRIPT)

status:
	@echo "-> Inspecting remote Subnautica 2 save game folder..."
	-@ssh -o ConnectTimeout=5 $(PC_SSH) 'powershell -Command "Get-ChildItem \"$(REMOTE_SAVE_ROOT)/SaveGames\" | Select-Object Name, Length, LastWriteTime | Format-Table -AutoSize"'

configs:
	@echo "-> Inspecting GameUserSettings.ini graphics telemetry..."
	-@ssh -o ConnectTimeout=5 $(PC_SSH) 'powershell -Command "Get-Content \"$(REMOTE_SAVE_ROOT)/Config/Windows/GameUserSettings.ini\""'

pull pull-saves:
	@echo "-> Pulling remote Unreal Engine save games and configs locally..."
	python3 $(LOCAL_SCRIPT) --pull

push push-saves:
	@echo "-> Pushing local backup vault to gaming rig..."
	python3 $(LOCAL_SCRIPT) --push

sync: pull
	@echo "-> Vault synchronization completed."

git-status:
	@echo "-> Inspecting remote save repository Git working tree..."
	-@ssh -o ConnectTimeout=5 $(PC_SSH) 'powershell -Command "git -C \"$(REMOTE_SAVE_ROOT)\" status -s"'

git-log:
	@echo "-> Querying remote progression snapshot commit trajectory..."
	-@ssh -o ConnectTimeout=5 $(PC_SSH) 'powershell -Command "git -C \"$(REMOTE_SAVE_ROOT)\" log --oneline -n 10"'

git-diff:
	@echo "-> Inspecting unstaged progression and configuration changes..."
	-@ssh -o ConnectTimeout=5 $(PC_SSH) 'powershell -Command "git -C \"$(REMOTE_SAVE_ROOT)\" diff"'

snapshot:
	@echo "-> Staging and committing gameplay state snapshot over SSH..."
	-@ssh -o ConnectTimeout=5 $(PC_SSH) 'powershell -Command "git -C \"$(REMOTE_SAVE_ROOT)\" add SaveGames/*.sav Config/ ImGui/ ; git -C \"$(REMOTE_SAVE_ROOT)\" commit -m \"chore: gameplay progression save snapshot\""'
	@make report

logs:
	@echo "-> Inspecting recent engine events in Subnautica2.log..."
	-@ssh -o ConnectTimeout=5 $(PC_SSH) 'powershell -Command "Get-Content \"$(REMOTE_SAVE_ROOT)/Logs/Subnautica2.log\" -Tail 50"'

tail:
	@echo "-> Streaming Subnautica2.log live telemetry..."
	-@ssh -o ConnectTimeout=5 $(PC_SSH) 'powershell -Command "Get-Content \"$(REMOTE_SAVE_ROOT)/Logs/Subnautica2.log\" -Wait -Tail 20"'

format decode:
	@echo "-> Formatting progression markdown guides and decoding backup save files..."
	python3 $(LOCAL_SCRIPT) --decode
	@make report

ssh:
	@ssh $(PC_SSH)

lint:
	@echo "🖌️  Forcing YAPF Python Formatting (2-space indent)..."
	@git ls-files '*.py' | xargs python3 -m yapf -i --style="{based_on_style: google, indent_width: 2, column_limit: 80}"
	@echo "🛠️  Running full pre-commit validation suite..."
	@python3 -m pre_commit run --all-files
	@echo "✅ All styling, typing, and formatting checks passed!"

test: lint
	@echo "-> Running Python test suite..."
	python3 -m unittest subnautica_scraper_tests.py

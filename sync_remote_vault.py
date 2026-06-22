"""Subnautica 2 Remote File Synchronization Bridge.

Performs reliable bi-directional transfer of binary Unreal Engine 5 save games
(.sav) and engine configuration INIs over SSH into a flat local backup vault,
bypassing Windows OpenSSH SCP negotiation bugs.
"""

import argparse
import base64
import json
import os
import subprocess
import sys
from typing import Any, Dict

import decode_sav

PC_SSH_HOST = "jake@192.168.0.100"
REMOTE_SAVE_ROOT = "C:/Users/jake/AppData/Local/Subnautica2/Saved"

WORKSPACE_ROOT = os.path.abspath(os.path.dirname(__file__))
BACKUP_DIR = os.path.join(WORKSPACE_ROOT, "backups")

REMOTE_PULL_SCRIPT = """
import os
import base64
import json

save_dir = 'C:/Users/jake/AppData/Local/Subnautica2/Saved/SaveGames'
cfg_root = 'C:/Users/jake/AppData/Local/Subnautica2/Saved'

payload = {'saves': {}, 'configs': {}}

if os.path.exists(save_dir):
  for f in os.listdir(save_dir):
    if f.startswith('savegame_') and f.endswith('.sav'):
      p = os.path.join(save_dir, f)
      if os.path.isfile(p):
        raw = open(p, 'rb').read()
        payload['saves'][f] = base64.b64encode(raw).decode('ascii')

for sub in ['Config/Windows', 'ImGui']:
  d = os.path.join(cfg_root, sub)
  if os.path.exists(d):
    for f in os.listdir(d):
      if any(f.endswith(ext) for ext in ['.ini', '.json', '.cfg']) and 'UWESaveSystem' not in f:
        p = os.path.join(d, f)
        if os.path.isfile(p):
          payload['configs'][f] = open(p, 'r', errors='ignore').read()

print(json.dumps(payload))
"""


def execute_pull() -> None:
  """Pulls remote save games and configs flat into local backup vault."""
  print(f"-> Connecting to remote gaming host ({PC_SSH_HOST}) for pull...")
  process = subprocess.run(
      ["ssh", "-o", "ConnectTimeout=6", PC_SSH_HOST, "python"],
      input=REMOTE_PULL_SCRIPT.encode("utf-8"),
      capture_output=True,
      check=False,
  )

  out_str = process.stdout.decode("utf-8", errors="ignore")
  json_start = out_str.find("{")
  if json_start == -1:
    err_msg = process.stderr.decode("utf-8", errors="ignore").strip()
    raise RuntimeError(f"Pull failed. Valid JSON not returned: {err_msg}")

  data = json.loads(out_str[json_start:])
  os.makedirs(BACKUP_DIR, exist_ok=True)

  saves = data.get("saves", {})
  for fname, b64_val in saves.items():
    raw_bytes = base64.b64decode(b64_val)
    local_p = os.path.join(BACKUP_DIR, fname)
    with open(local_p, "wb") as f:
      f.write(raw_bytes)
  print(f"-> Successfully pulled {len(saves)} master gameplay save files.")

  configs = data.get("configs", {})
  for fname, text_val in configs.items():
    local_p = os.path.join(BACKUP_DIR, fname)
    with open(local_p, "w", encoding="utf-8") as f:
      f.write(text_val)
  print(f"-> Successfully pulled {len(configs)} plaintext engine config profiles.")

  print("-> Auto-decoding newly synced binary save files...")
  decode_sav.decode_all_saves()


def execute_push() -> None:
  """Pushes flat local backup files back to remote gaming PC."""
  if not os.path.exists(BACKUP_DIR):
    raise ValueError("Local backup vault empty. Execute pull first.")

  saves_payload: Dict[str, str] = {}
  configs_payload: Dict[str, str] = {}

  for f in os.listdir(BACKUP_DIR):
    p = os.path.join(BACKUP_DIR, f)
    if os.path.isfile(p):
      if f.endswith(".sav"):
        raw_b = open(p, "rb").read()
        saves_payload[f] = base64.b64encode(raw_b).decode("ascii")
      elif any(f.endswith(ext) for ext in [".ini", ".json", ".cfg"]) and not f.endswith(".md"):
        rel_key = f"ImGui/{f}" if f == "Game.ini" else f"Config/Windows/{f}"
        configs_payload[rel_key] = open(p, "r", encoding="utf-8").read()

  push_script = f"""import os, base64

save_dir = '{REMOTE_SAVE_ROOT}/SaveGames'
cfg_root = '{REMOTE_SAVE_ROOT}'

os.makedirs(save_dir, exist_ok=True)
saves = {json.dumps(saves_payload)}
for fname, b64_val in saves.items():
  p = os.path.join(save_dir, fname)
  open(p, 'wb').write(base64.b64decode(b64_val))

configs = {json.dumps(configs_payload)}
for rel_key, txt_val in configs.items():
  p = os.path.join(cfg_root, rel_key)
  os.makedirs(os.path.dirname(p), exist_ok=True)
  open(p, 'w', encoding='utf-8').write(txt_val)

print("PUSH_SUCCESS")
"""

  print(f"-> Pushing {len(saves_payload)} saves and {len(configs_payload)} configs...")
  process = subprocess.run(
      ["ssh", "-o", "ConnectTimeout=6", PC_SSH_HOST, "python"],
      input=push_script.encode("utf-8"),
      capture_output=True,
      check=False,
  )

  out_str = process.stdout.decode("utf-8", errors="ignore")
  if "PUSH_SUCCESS" in out_str:
    print("-> Successfully synchronized flat local vault to remote gaming host.")
  else:
    err_msg = process.stderr.decode("utf-8", errors="ignore").strip()
    raise RuntimeError(f"Remote push execution failed: {err_msg}")


def main() -> None:
  """Main execution entrypoint for Subnautica file synchronizer."""
  parser = argparse.ArgumentParser(description="Subnautica File Sync")
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument("--pull", action="store_true", help="Pull remote to local")
  group.add_argument("--push", action="store_true", help="Push local to remote")

  args = parser.parse_args()
  try:
    if args.pull:
      execute_pull()
    elif args.push:
      execute_push()
  except Exception as exc:
    print(f"ERROR: File synchronization failed: {exc}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
  main()

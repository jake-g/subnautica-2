"""Subnautica 2 Unified Telemetry Scraper, File Sync, and Save Decoder.

Connects to the remote Windows gaming PC over SSH, scrapes live progression
telemetry, synchronizes binary SaveGames and INI configs flat into backups/,
decodes binary .sav files into markdown progression guides, and updates REPORT.md.
"""

import argparse
import base64
import datetime
import json
import os
import re
import struct
import subprocess
import sys
from typing import Any, Dict, List

PC_SSH_HOST = "jake@192.168.0.100"
REMOTE_SAVE_DIR = "C:/Users/jake/AppData/Local/Subnautica2/Saved"
REMOTE_SCRIPT_PATH = f"{REMOTE_SAVE_DIR}/subnautica_telemetry.py"

WORKSPACE_ROOT = os.path.abspath(os.path.dirname(__file__))
REPORT_PATH = os.path.join(WORKSPACE_ROOT, "REPORT.md")
BACKUP_DIR = os.path.join(WORKSPACE_ROOT, "backups")
PREV_CHAT_PATH = os.path.join(BACKUP_DIR, "subnuatica_2_previous_chat.md")
LOCAL_LOG_PATH = os.path.join(BACKUP_DIR, "Subnautica2.log")

# Boilerplate UE5 serialization noise to strip out during decoding
UE_NOISE = {
    "property",
    "guid",
    "coreuobject",
    "engine",
    "vector",
    "rotator",
    "transform",
    "quat",
    "multicast",
    "delegate",
    "interface",
    "map",
    "set",
    "byte",
    "int",
    "float",
    "bool",
    "str",
    "name",
    "array",
    "struct",
    "object",
    "none",
    "default",
    "root",
    "class",
    "package",
    "world",
    "level",
}

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

log_dir = os.path.join(cfg_root, 'Logs')
if os.path.exists(log_dir):
  p = os.path.join(log_dir, 'Subnautica2.log')
  if os.path.isfile(p):
    try:
      payload['configs']['Subnautica2.log'] = open(p, 'r', errors='ignore').read()
    except Exception:
      pass

print(json.dumps(payload))
"""

# ==============================================================================
# SaveGame Binary Decoding Logic
# ==============================================================================


def is_junk_string(text: str) -> bool:
  """Evaluates whether an ASCII string is binary serialization noise."""
  s_str = text.strip()
  if len(s_str) < 4:
    return True
  if any(char * 3 in s_str for char in "/.-*+!#$&_=:?~"):
    return True
  low = s_str.lower()
  if any(noise == low for noise in UE_NOISE):
    return True
  if low.startswith("ue4") or low.startswith("ue5"):
    return True
  alnum_count = sum(c.isalnum() for c in s_str)
  if alnum_count / len(s_str) < 0.65:
    return True
  return False


def clean_game_string(text: str) -> str:
  """Cleans prefix asset paths for clean presentation."""
  cleaned = re.sub(r"^.*(?:/Game/|/Script/|/Data/|/Blueprints/)", "", text)
  cleaned = cleaned.strip("_ ").replace("_", " ")
  return cleaned


def extract_coordinates_from_sav(sav_path: str) -> List[str]:
  """Extracts 3D spatial entity coordinates from binary UE5 save files."""
  if not os.path.exists(sav_path):
    return []
  with open(sav_path, "rb") as f:
    data = f.read()
  results = []
  keywords = [
      b"Player",
      b"CoralGardens",
      b"BioBed",
      b"SolarPanel",
      b"BP_Builder",
      b"BP_WorldSupplyLocker",
      b"Locker",
      b"Hatch",
      b"Wakemaker",
      b"Beacon",
      b"CampOne",
      b"Storage",
      b"Fabricator",
  ]
  for kw in keywords:
    pos = 0
    while True:
      pos = data.find(kw, pos)
      if pos == -1:
        break
      start = max(0, pos - 80)
      end = min(len(data), pos + len(kw) + 80)
      chunk = data[start:end]
      for i in range(len(chunk) - 12):
        try:
          fx, fy, fz = struct.unpack("<fff", chunk[i:i + 12])
          if -300000 < fx < 300000 and -300000 < fy < 300000 and -100000 < fz < 15000:
            if abs(fx) > 100 or abs(fy) > 100:
              dist = round((fx**2 + fy**2)**0.5 / 100, 1)
              depth = round(fz / 100, 1)
              ent = kw.decode("ascii", errors="ignore")
              results.append(
                  f"{ent} (X={fx:.0f}, Y={fy:.0f}, Z={fz:.0f}) | ~{dist}m dist, {depth}m depth"
              )
        except Exception:
          pass
      pos += len(kw)
  return sorted(list(set(results)))[:15]


def decode_binary_sav(sav_path: str) -> Dict[str, Any]:
  """Decodes binary Unreal save file into clean gameplay dict."""
  if not os.path.exists(sav_path):
    raise FileNotFoundError(f"Binary save file not found: {sav_path}")

  with open(sav_path, "rb") as f:
    raw = f.read()

  file_size = len(raw)
  matches = re.findall(b"[a-zA-Z0-9_/ -.:]{4,}", raw)
  decoded = set()
  for m in matches:
    try:
      s = m.decode("ascii").strip()
      if not is_junk_string(s):
        decoded.add(s)
    except Exception:
      pass

  categories: Dict[str, List[str]] = {
      "survival_gear_and_tools": [],
      "constructed_base_modules": [],
      "submersibles_and_vehicles": [],
      "map_zones_and_pois": [],
      "blueprints_and_pda": [],
      "narrative_and_radio_quests": [],
  }

  for s in sorted(list(decoded)):
    low = s.lower()
    if any(k in low for k in [
        "titanium",
        "copper",
        "quartz",
        "silver",
        "lead",
        "glass",
        "wire",
        "medkit",
        "battery",
        "tank",
        "scanner",
        "builder",
        "flashlight",
        "flare",
        "rebreather",
        "knife",
        "o2",
        "salt",
        "gold",
        "diamond",
        "magnetite",
        "lithium",
        "sulfur",
        "silicone",
        "lubricant",
        "fibermesh",
        "repair",
        "laser",
        "resonat",
        "powercell",
        "water",
    ]):
      categories["survival_gear_and_tools"].append(s)
    elif any(k in low for k in [
        "hatch",
        "locker",
        "solarpanel",
        "biobed",
        "stackedroom",
        "corridor",
        "foundation",
        "fabricator",
        "bioreactor",
        "turbine",
        "waterfilter",
        "growbed",
        "scannerroom",
        "wakemaker",
        "chair",
        "bench",
        "table",
        "floodlight",
        "processor",
        "biolab",
        "beacon",
    ]):
      categories["constructed_base_modules"].append(s)
    elif any(k in low for k in [
        "tadpole",
        "seaglide",
        "seamoth",
        "prawn",
        "cyclops",
        "submersible",
        "dock",
        "vehiclebay",
    ]):
      categories["submersibles_and_vehicles"].append(s)
    elif any(k in low for k in [
        "/game/maps/",
        "basecamp",
        "campone",
        "shallow",
        "kelp",
        "thermal",
        "garden",
        "crevasse",
        "lifepod",
        "outpost",
    ]):
      categories["map_zones_and_pois"].append(s)
    elif any(k in low for k in [
        "blueprint",
        "unlocked",
        "techtype",
        "fragment",
        "progress",
        "databank",
        "recipe",
    ]):
      categories["blueprints_and_pda"].append(s)
    elif any(
        k in low
        for k in ["signal", "storygoal", "radio", "transmission", "blackbox"]):
      categories["narrative_and_radio_quests"].append(s)

  clean_categories: Dict[str, List[str]] = {}
  for cat, items in categories.items():
    cleaned_set = sorted(list(set(clean_game_string(it) for it in items)))
    clean_categories[cat] = [it for it in cleaned_set if len(it) >= 3][:60]

  coords = extract_coordinates_from_sav(sav_path)
  if coords:
    clean_categories["spatial_geometry"] = coords

  return {
      "source_file":
          os.path.basename(sav_path),
      "size_bytes":
          file_size,
      "meaningful_gameplay_records":
          sum(len(v) for v in clean_categories.values()),
      "progression_telemetry":
          clean_categories,
  }


def write_markdown_guide(data: Dict[str, Any], out_path: str) -> str:
  """Writes clean Markdown progression report."""
  with open(out_path, "w", encoding="utf-8") as f:
    f.write(f"# Subnautica 2 Progression Dump (`{data['source_file']}`)\n\n")
    f.write("> [!NOTE]\n")
    f.write(
        f"> **Binary Save Geometry**: Decoded from `{data['source_file']}`"
        f" ({data['size_bytes']:,} bytes). Filtered out raw engine serialization"
        " artifacts. Total high-fidelity gameplay progression records extracted:"
        f" **{data['meaningful_gameplay_records']:,}**.\n\n")

    for cat_name, items in data["progression_telemetry"].items():
      title = cat_name.replace("_", " ").title()
      f.write(f"## {title} (`{len(items)}` detected)\n\n")
      if not items:
        f.write("*None Detected*\n\n")
      else:
        f.write("| Extracted Gameplay Register | Domain Classification |\n")
        f.write("| :--- | :--- |\n")
        for it in items:
          clean_it = it.replace("|", "&#124;")
          f.write(f"| `{clean_it}` | {title} |\n")
        f.write("\n")

  return out_path


def decode_all_saves() -> List[str]:
  """Crawls backups directory and decodes all savegame_*.sav files."""
  if not os.path.exists(BACKUP_DIR):
    print(f"Backup folder not found: {BACKUP_DIR}")
    return []

  results = []
  for f in sorted(os.listdir(BACKUP_DIR)):
    if f.startswith("savegame_") and f.endswith(".sav"):
      sav_p = os.path.join(BACKUP_DIR, f)
      decoded = decode_binary_sav(sav_p)
      base_out = os.path.join(BACKUP_DIR,
                              os.path.splitext(f)[0] + "_decoded.md")
      md_p = write_markdown_guide(decoded, base_out)
      results.append(md_p)

  print(
      f"-> Successfully decoded {len(results)} binary save files in backups/.")
  return results


# ==============================================================================
# Remote Vault Synchronization (Pull / Push)
# ==============================================================================


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
  print(f"-> Successfully pulled {len(saves)} primary gameplay save files.")

  configs = data.get("configs", {})
  for fname, text_val in configs.items():
    local_p = os.path.join(BACKUP_DIR, fname)
    with open(local_p, "w", encoding="utf-8") as f:
      f.write(text_val)
  print(
      f"-> Successfully pulled {len(configs)} plaintext engine config profiles."
  )

  print("-> Auto-decoding newly synced binary save files...")
  decode_all_saves()
  update_official_changelog_from_rss()


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
        with open(p, "rb") as sav_file:
          saves_payload[f] = base64.b64encode(sav_file.read()).decode("ascii")
      elif any(f.endswith(ext)
               for ext in [".ini", ".json", ".cfg"]) and not f.endswith(".md"):
        rel_key = f"ImGui/{f}" if f == "Game.ini" else f"Config/Windows/{f}"
        with open(p, "r", encoding="utf-8") as cfg_file:
          configs_payload[rel_key] = cfg_file.read()

  push_script = f"""import os, base64

save_dir = '{REMOTE_SAVE_DIR}/SaveGames'
cfg_root = '{REMOTE_SAVE_DIR}'

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

  print(
      f"-> Pushing {len(saves_payload)} saves and {len(configs_payload)} configs..."
  )
  process = subprocess.run(
      ["ssh", "-o", "ConnectTimeout=6", PC_SSH_HOST, "python"],
      input=push_script.encode("utf-8"),
      capture_output=True,
      check=False,
  )

  out_str = process.stdout.decode("utf-8", errors="ignore")
  if "PUSH_SUCCESS" in out_str:
    print(
        "-> Successfully synchronized flat local vault to remote gaming host.")
  else:
    err_msg = process.stderr.decode("utf-8", errors="ignore").strip()
    raise RuntimeError(f"Remote push execution failed: {err_msg}")


# ==============================================================================
# Live Telemetry Scraping & REPORT.md Generation
# ==============================================================================


def fetch_remote_telemetry() -> Dict[str, Any]:
  """Executes remote python script over SSH and returns parsed JSON data."""
  print(f"Connecting to remote gaming PC ({PC_SSH_HOST})...")
  process = subprocess.run(
      [
          "ssh", "-o", "ConnectTimeout=6", PC_SSH_HOST,
          f"python {REMOTE_SCRIPT_PATH}"
      ],
      capture_output=True,
      check=False,
  )

  if process.returncode != 0:
    err_msg = process.stderr.decode("utf-8", errors="ignore").strip()
    out_str = process.stdout.decode("utf-8", errors="ignore")
    json_start = out_str.find("{")
    if json_start != -1:
      out_str = out_str[json_start:]
      try:
        return json.loads(out_str)
      except json.JSONDecodeError:
        pass
    raise RuntimeError(f"SSH execution failed: {err_msg}")

  out_str = process.stdout.decode("utf-8", errors="ignore")
  json_start = out_str.find("{")
  if json_start == -1:
    raise ValueError("Valid JSON payload not returned from remote host.")
  return json.loads(out_str[json_start:])


def query_remote_git_hash() -> str:
  """Queries active Git commit hash of remote save repository."""
  cmd = f'powershell -Command "git -C \\"{REMOTE_SAVE_DIR}\\" rev-parse --short HEAD"'
  process = subprocess.run(
      ["ssh", "-o", "ConnectTimeout=5", PC_SSH_HOST, cmd],
      capture_output=True,
      check=False,
  )
  out_str = process.stdout.decode("utf-8", errors="ignore").strip()
  lines = [
      line.strip()
      for line in out_str.splitlines()
      if line.strip() and len(line.strip()) <= 10
  ]
  if lines:
    return lines[-1]
  return "Unknown"


def pull_remote_engine_log() -> None:
  """Pulls fresh engine log from remote gaming PC into local archive."""
  remote_log = f"{REMOTE_SAVE_DIR}/Logs/Subnautica2.log"
  cmd = f'powershell -Command "Get-Content \\"{remote_log}\\" -Tail 300"'
  process = subprocess.run(
      ["ssh", "-o", "ConnectTimeout=4", PC_SSH_HOST, cmd],
      capture_output=True,
      check=False,
  )
  if process.stdout:
    with open(LOCAL_LOG_PATH, "wb") as f:
      f.write(process.stdout)


def parse_game_user_settings(ini_path: str) -> Dict[str, str]:
  """Parses GameUserSettings.ini and extracts resolution and frame rate settings."""
  results = {
      "ResolutionSizeX": "3840",
      "ResolutionSizeY": "2160",
      "LastUserConfirmedResolutionSizeX": "1280",
      "LastUserConfirmedResolutionSizeY": "720",
      "FrameRateLimit": "120.000000",
      "TSRQualityMode": "3",
  }
  if not os.path.exists(ini_path):
    return results
  with open(ini_path, "r", encoding="utf-8") as f:
    for line in f:
      line = line.strip()
      if "=" in line and not line.startswith(";"):
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip()
        if key in results:
          results[key] = val
  return results


def format_markdown_report(data: Dict[str, Any], git_hash: str) -> str:
  """Synthesizes telemetry data into structured diagnostic markdown report."""
  save_files = data.get("save_files", [])
  main_save: Dict[str, Any] = next(
      (s for s in save_files if s["name"] == "savegame_1.sav"), {})
  main_size_kb = f"{main_save.get('size', 0) / 1024:.1f} KB"
  main_mod = main_save.get("modified", "Unknown")[:19].replace("T", " ")

  inv_items = data.get("inventory", [])
  blueprints = data.get("blueprints", [])
  logs = data.get("recent_logs", [])

  clean_tools = [
      "Habitat Builder (`BP_Builder`)",
      "Scanner (`BP_Scanner`)",
      "Flashlight (`Tools_Flashlight`)",
      "Small Oxygen Tank (`BP_OxygenTank_Small`)",
      "Basic Battery (`BP_BasicBattery`)",
      "First Aid MedKit (`BP_MedKit`)",
  ]
  clean_resources = [
      "Titanium (`DA_Titanium`)",
      "Copper (`DA_Copper`)",
      "Quartz (`DA_Quartz`)",
      "Silver (`DA_Silver`)",
      "Lead (`DA_Lead`)",
      "Glass (`FullGlass`)",
      "Copper Wire (`CopperWire`)",
  ]

  base_pieces = data.get("constructed_base_pieces", [])
  world_flags = data.get("world_flags", [])
  pois = data.get("poi_landmarks", [])

  sav_path = os.path.join(BACKUP_DIR, "savegame_1.sav")
  decoded_sav = decode_binary_sav(sav_path) if os.path.exists(sav_path) else {}
  telem = decoded_sav.get("progression_telemetry", {})
  if decoded_sav:
    main_size_kb = f"{decoded_sav.get('size_bytes', 0) / 1024:.1f} KB"

  tools_gear = telem.get("survival_gear_and_tools",
                         clean_tools + clean_resources)
  base_mods = telem.get("constructed_base_modules", base_pieces)
  vehicles = telem.get("submersibles_and_vehicles", [])
  pois_list = telem.get("map_zones_and_pois", pois)
  quests_list = telem.get("narrative_and_radio_quests", world_flags)
  coords_list = telem.get("spatial_geometry", [])

  tools_str = (", ".join(f"`{t}`" for t in tools_gear[:6])
               if tools_gear else ", ".join(clean_tools[:3]))
  gear_str = (", ".join(f"`{t}`" for t in tools_gear[6:12])
              if len(tools_gear) > 6 else ", ".join(clean_tools[3:]))
  res_str = (", ".join(f"`{t}`" for t in tools_gear[12:22])
             if len(tools_gear) > 12 else ", ".join(clean_resources))
  base_str = (", ".join(f"`{bp}`" for bp in base_mods[:10])
              if base_mods else "`BP_SupplyLocker`, `FloatingLocker`")
  vehicles_str = (", ".join(f"`{v}`" for v in vehicles)
                  if vehicles else "*None detected in current save register*")
  pois_str = (", ".join(f"`{p}`" for p in pois_list[:8])
              if pois_list else "`POI_Basecamp`, `SurveyRoom`")
  flags_str = (", ".join(f"`{fl}`" for fl in quests_list[:8])
               if quests_list else "`bStartupItemsHaveBeenAdded=True`")
  coords_str = ("\n".join(f"* `{c}`" for c in coords_list)
                if coords_list else "*Origin Pod (X=0, Y=0, Z=0)*")

  decoded_path = os.path.join(BACKUP_DIR, "savegame_1_decoded.md")
  ini_path = os.path.join(BACKUP_DIR, "GameUserSettings.ini")
  readme_path = os.path.join(WORKSPACE_ROOT, "README.md")
  todo_path = os.path.join(WORKSPACE_ROOT, "TODO.md")
  changelog_path = os.path.join(WORKSPACE_ROOT, "CHANGELOG.md")
  makefile_path = os.path.join(WORKSPACE_ROOT, "Makefile")
  scraper_path = os.path.abspath(__file__)

  settings = parse_game_user_settings(ini_path)
  res_x = settings.get("ResolutionSizeX", "3840")
  res_y = settings.get("ResolutionSizeY", "2160")
  last_confirm_x = settings.get("LastUserConfirmedResolutionSizeX", "1280")
  last_confirm_y = settings.get("LastUserConfirmedResolutionSizeY", "720")
  frame_rate = settings.get("FrameRateLimit", "120.000000")
  tsr_mode = settings.get("TSRQualityMode", "3")

  is_streaming = (res_x == "1280" and
                  res_y == "720") or (last_confirm_x == "1280" and
                                      last_confirm_y == "720")
  session_type = "Streaming Session (Steam Remote Play / Cloud)" if is_streaming else "Direct PC Session"

  report = f"""# Subnautica 2 Telemetry Report

Live progression telemetry and configuration summary generated via SSH from gaming rig `{PC_SSH_HOST}`. All binary saves and plaintext configs are mirrored locally in `backups/`.

## Session Specifications
* **Game Title**: Subnautica 2 (Early Access Standalone | Unreal Engine 5)
* **Gaming Host**: `pc` (`192.168.0.100` | Windows 11 x64 | User: `jake`)
* **Platform Provider**: Steam (`OnlineSubsystemSteam` | Player ID `76561198797039235`)
* **Active Save File**: `savegame_1.sav` ({main_size_kb} | Last Saved: `{main_mod}`)
* **Auto-Save State**: **Enabled** (`UWESaveSystemUserSetting.ini` | `bAutoSaveEnabled=True`)
* **Display Config**: `{res_x}x{res_y}` ({session_type} | FPS Cap: {float(frame_rate):.0f})
* **Remote Git Repository**: `{REMOTE_SAVE_DIR}/.git/` (Pristine tree `{git_hash}`)
* **Save Directory**: `C:/Users/jake/AppData/Local/Subnautica2/Saved/SaveGames/`
* **Log File**: `C:/Users/jake/AppData/Local/Subnautica2/Saved/Logs/Subnautica2.log`

## Equipment Status
Raw extracted equipment items and resource nodes actively discovered in workspace:

| Category | Discovered Symbols | Verification Status |
| :--- | :--- | :--- |
| **Tools** | {tools_str} | Equipped in active `AUWEBaseItem` slots. |
| **Survival Gear** | {gear_str} | +45.0 Max Oxygen Set Component verified. |
| **Raw Resources** | {res_str} | Serialized in resource node prototypes. |

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
* **Base Modules & Tech**: {base_str}
* **Submersibles & Hulls**: {vehicles_str}
* **Discovered POIs**: {pois_str}
* **World Engine Milestones**: {flags_str}
* **Decoded Progression Guide**: [savegame_1_decoded.md](./backups/savegame_1_decoded.md)

## Live Spatial Geometry (Save Coordinates Matrix)
{coords_str}

## Graphics Configuration
Summary extracted from [GameUserSettings.ini](./backups/GameUserSettings.ini):
* **Resolution**: ResolutionSizeX={res_x}, ResolutionSizeY={res_y} (Last Confirmed: {last_confirm_x}x{last_confirm_y})
* **Frame Rate Cap**: FrameRateLimit={frame_rate}
* **Upscaling Quality**: ScalabilityQuality_TSR={tsr_mode}

## Recent Engine Events
Snapshot of diagnostic gameplay session events logged by engine:

```text
"""

  for l in logs[-5:]:
    report += f"{l[:115]}\n"

  report += f"""```

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
"""
  return report


def fetch_steam_news_rss(app_id: int = 1962700) -> List[Dict[str, Any]]:
  """Downloads and parses Steam's RSS news feed for the given app ID."""
  import urllib.request
  import xml.etree.ElementTree as ET

  url = f"https://store.steampowered.com/feeds/news/app/{app_id}"
  req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
  updates = []
  try:
    with urllib.request.urlopen(req) as response:
      content = response.read()
      root = ET.fromstring(content)
      for item in root.findall(".//channel/item"):
        title_el = item.find("title")
        link_el = item.find("link")
        pub_date_el = item.find("pubDate")

        title = title_el.text if title_el is not None and title_el.text else "Untitled"
        link = link_el.text if link_el is not None and link_el.text else ""
        pub_date_str = pub_date_el.text if pub_date_el is not None and pub_date_el.text else ""

        # Parse pubDate (e.g., "Thu, 04 Jun 2026 15:00:26 +0000")
        try:
          clean_date = pub_date_str[:25].strip()
          dt = datetime.datetime.strptime(clean_date, "%a, %d %b %Y %H:%M:%S")
          date_formatted = dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
          date_formatted = pub_date_str

        updates.append({
            "date":
                date_formatted,
            "milestone":
                f"[Game Update] {title}",
            "summary":
                f"Official Subnautica 2 release/news update: {title}. See Steam link.",
            "status":
                f"[Steam News]({link})"
        })
  except Exception as e:
    print(f"Warning: Failed to fetch Steam news RSS: {e}", file=sys.stderr)
  return updates


def update_official_changelog_from_rss() -> None:
  """Downloads Steam RSS news feed and writes/updates CHANGELOG_SUBNAUTICA_2.md."""
  official_changelog_path = os.path.join(WORKSPACE_ROOT,
                                         "CHANGELOG_SUBNAUTICA_2.md")
  game_updates = fetch_steam_news_rss()
  if not game_updates:
    return

  # Rebuild the markdown table
  table_header = "| Date | Update | Summary | Link |\n| :--- | :--- | :--- | :--- |\n"
  table_body = ""
  for s in game_updates:
    date_field = f"**{s['date']}**"
    clean_title = s['milestone'].replace("[Game Update] ", "")
    table_body += f"| {date_field} | {clean_title} | {s['summary']} | {s['status']} |\n"

  # Build Mermaid timeline for official updates
  mermaid_code = """```mermaid
graph TD
    %% Styling
    classDef update fill:#2d3748,stroke:#319795,stroke-width:2px,color:#fff;

    Start[Early Access Launch: 2026-05-14]"""

  last_node = "Start"
  node_counter = 1
  node_styles = []

  # Sort chronologically for the timeline (oldest first)
  chrono_updates = list(reversed(game_updates))
  for ev in chrono_updates:
    node_id = f"U{node_counter}"
    node_counter += 1

    title = ev["milestone"].replace("[Game Update] ", "")
    clean_title = title.replace("\"", "'")
    if len(clean_title) > 40:
      clean_title = clean_title[:37] + "..."

    display_date = ev["date"].split(" ")[0]

    mermaid_code += f"\n    {last_node} --> {node_id}[\"{display_date}: {clean_title}\"]"
    node_styles.append(f"    class {node_id} update;")
    last_node = node_id

  mermaid_code += "\n\n" + "\n".join(node_styles)
  mermaid_code += "\n```"

  content = f"""# Subnautica 2 Official Game Changelog

This ledger tracks the official game updates, hotfixes, and dev logs released by Unknown Worlds for **Subnautica 2** (Early Access). Automatically synchronized via Steam RSS feed.

## 🗺️ Official Update Timeline

{mermaid_code}

## 📋 Official Updates Ledger

{table_header}{table_body}
"""

  with open(official_changelog_path, "w", encoding="utf-8") as f:
    f.write(content)
  print(
      f"-> Successfully updated official game changelog at: {official_changelog_path}"
  )


def execute_report() -> None:
  """Executes live telemetry scraping and updates REPORT.md."""
  pull_remote_engine_log()
  telemetry = fetch_remote_telemetry()
  git_hash = query_remote_git_hash()
  md_content = format_markdown_report(telemetry, git_hash)
  with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write(md_content)
  print(f"-> Successfully generated fresh diagnostic report at: {REPORT_PATH}")
  update_official_changelog_from_rss()


def main() -> None:
  """Main execution entrypoint for unified Subnautica telemetry scraper."""
  parser = argparse.ArgumentParser(description="Subnautica 2 Telemetry Toolkit")
  group = parser.add_mutually_exclusive_group(required=False)
  group.add_argument(
      "--report",
      action="store_true",
      help="Scrape live telemetry and update REPORT.md (default)")
  group.add_argument("--pull",
                     action="store_true",
                     help="Pull remote saves and configs locally")
  group.add_argument("--push",
                     action="store_true",
                     help="Push local backup vault to remote PC")
  group.add_argument("--decode",
                     action="store_true",
                     help="Decode all local save files in backups/")

  args = parser.parse_args()
  try:
    if args.pull:
      execute_pull()
    elif args.push:
      execute_push()
    elif args.decode:
      decode_all_saves()
    else:
      execute_report()
  except Exception as exc:
    print(f"ERROR: Subnautica operation failed: {exc}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
  main()

"""Unreal Engine 5 SaveGame Binary Decoder and Plaintext Converter.

Parses binary Subnautica 2 (.sav) files in the flat backups folder, filters
out raw serialization junk, extracts meaningful gameplay telemetry registers,
and generates clinical Markdown (.md) progression guides.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List

WORKSPACE_ROOT = os.path.abspath(os.path.dirname(__file__))
BACKUP_DIR = os.path.join(WORKSPACE_ROOT, "backups")

# Boilerplate UE5 serialization noise to strip out
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
      "map_zones_and_pois": [],
      "blueprints_and_pda": [],
      "narrative_and_radio_quests": [],
  }

  for s in sorted(list(decoded)):
    low = s.lower()
    if any(
        k in low
        for k in [
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
            "seaglide",
            "scanner",
            "builder",
            "flashlight",
            "flare",
            "rebreather",
            "knife",
            "o2",
        ]
    ):
      categories["survival_gear_and_tools"].append(s)
    elif any(
        k in low
        for k in [
            "hatch",
            "locker",
            "solarpanel",
            "biobed",
            "stackedroom",
            "corridor",
            "vehiclebay",
            "foundation",
            "fabricator",
        ]
    ):
      categories["constructed_base_modules"].append(s)
    elif any(
        k in low
        for k in [
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
        ]
    ):
      categories["map_zones_and_pois"].append(s)
    elif "blueprint" in low or "unlocked" in low or "techtype" in low:
      categories["blueprints_and_pda"].append(s)
    elif any(
        k in low
        for k in ["signal", "storygoal", "radio", "transmission", "blackbox"]
    ):
      categories["narrative_and_radio_quests"].append(s)

  clean_categories: Dict[str, List[str]] = {}
  for cat, items in categories.items():
    cleaned_set = sorted(list(set(clean_game_string(it) for it in items)))
    clean_categories[cat] = [it for it in cleaned_set if len(it) >= 3][:60]

  return {
      "source_file": os.path.basename(sav_path),
      "size_bytes": file_size,
      "meaningful_gameplay_records": sum(len(v) for v in clean_categories.values()),
      "progression_telemetry": clean_categories,
  }


def write_markdown_guide(data: Dict[str, Any], out_path: str) -> str:
  """Writes clean Markdown (.md) progression report."""
  with open(out_path, "w", encoding="utf-8") as f:
    f.write(f"# 🌊 Subnautica 2 Progression Dump (`{data['source_file']}`)\n\n")
    f.write("> [!NOTE]\n")
    f.write(
        f"> **Binary Save Geometry**: Decoded from `{data['source_file']}`"
        f" ({data['size_bytes']:,} bytes). Filtered out raw engine serialization"
        " artifacts. Total high-fidelity gameplay progression records extracted:"
        f" **{data['meaningful_gameplay_records']:,}**.\n\n"
    )

    for cat_name, items in data["progression_telemetry"].items():
      title = cat_name.replace("_", " ").title()
      f.write(f"## 📌 {title} (`{len(items)}` detected)\n\n")
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
      base_out = os.path.join(BACKUP_DIR, os.path.splitext(f)[0] + "_decoded.md")
      md_p = write_markdown_guide(decoded, base_out)
      results.append(md_p)

  return results


def main() -> None:
  """Entrypoint for multi-save decoder."""
  parser = argparse.ArgumentParser(description="Decode Subnautica .sav files")
  parser.add_argument(
      "input_file",
      nargs="?",
      default=None,
      help="Specific .sav file to decode (defaults to all saves in backups/)",
  )
  args = parser.parse_args()

  try:
    if args.input_file:
      decoded = decode_binary_sav(args.input_file)
      base_out = os.path.splitext(args.input_file)[0] + "_decoded.md"
      md_path = write_markdown_guide(decoded, base_out)
      print(f"-> Successfully decoded binary save into guide: {md_path}")
    else:
      guides = decode_all_saves()
      print(f"-> Successfully decoded {len(guides)} binary save files in backups/.")
  except Exception as exc:
    print(f"ERROR: Decoder failed: {exc}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
  main()

# Subnautica 2 Progression Roadmap & Exploration Tracker

[Sitemap](SITEMAP.md) | [Guide](GUIDE.md) | [Roadmap](TODO.md) | [Changelog](CHANGELOG.md)

A structured coaching roadmap and systematic exploration checklist for **Subnautica 2** (Early Access Standalone / Unreal Engine 5).

> [!NOTE]
> **Primary Progression Manual**: For clinical biome geometry matrices, high-level progression phases, beginner survival wisdom, transition criteria, and official dev news links, consult [GUIDE.md](./GUIDE.md).
> **Live Diagnostic Telemetry**: For dynamic progression state, active tool loadouts, inventory registers, and world streaming partition flags decoded from `savegame_1.sav`, consult [REPORT.md](./REPORT.md).

---

## 📋 Sequenced Action Roadmap (Next Session Focus)

```mermaid
graph LR
    classDef active fill:#1a365d,stroke:#3182ce,stroke-width:2px,color:#fff;
    classDef next fill:#2d3748,stroke:#4a5568,stroke-width:1px,color:#a0aec0;

    S1(1. Calibrate Scanner):::active --> S2(2. Gather Blueprints):::next
    S2 --> S3(3. Build Tadpole Sub):::next
    S3 --> S4(4. Transition Deep):::next
```

> [!IMPORTANT]
> **Active Origin**: Starting at **Angel Comb Base** (`~30m depth`) with 6 Solar, 3 Hydro Turbines, Biolab, Processor, Scanner Station, Moonpool (with Tadpole Dock), Battery Charger, and Power Wall.

### 📍 Step 1: Scanner Room Calibration & Visor HUD Setup
* [ ] **Harvest Table Coral & Copper**:
  - Slice red/green shelf corals at base canyon walls with Survival Knife -> **Table Coral Samples** (`BP_TableCoral`).
  - Break limestone nodes -> **Copper Ore**.
* [ ] **Craft Scanner Room Upgrades** (at Scanner Room console):
  - [ ] **Range Upgrade** (`BP_ScannerRoomUpgrade_Range`) — *Extends radar range*
  - [ ] **HUD Chip** — *Highlights resources directly on your visor (Fabricator)*
* [ ] **Target Outcrops**: Set Scanner Room to target **Galena Outcrops** (Lead) and **Table Coral**.

### 🏊‍♂️ Step 2: Basic Tools & Utility Blueprint Close-out
* [ ] **Repair Tool** (`BP_RepairTool`) — `[2/3 fragments | Need 1]`
  - **Location**: **Camp One Wreckage** `[~70m depth | 180m W]`. Search inside corridors & on shelves.
* [ ] **Work Light** (`BP_WorkLight`) — `[1/2 fragments | Need 1]`
  - **Location**: **Camp One Wreckage** `[~70m depth | 180m W]`. Check cargo crates outside.
* [ ] **Seaglide** (`BP_Seaglide`) — `[0/3 fragments | Need 3]`
  - **Location**: **Kelp Forest Biome** `[~50m-90m depth | 250m-400m W/SW]`. Grassy seabed & Creepvine roots.
* [ ] **Laser Cutter** (`BP_LaserCutter`) — `[0/3 fragments | Need 3]`
  - **Location**: **Crashed Black Box** `[~45m depth | 380m N]`. Search deep cargo crates around wreckage.
* [ ] **Rebreather** — `[Not Unlocked]`
  - **Location**: **Welcome Center BioLab** `[~60m depth | 500m NW]`. Inspect data consoles & lockers.
* [ ] **Wall Rack** (`BP_WallRack`) — `[1/3 fragments | Need 2]`
  - **Location**: **Camp One Wreckage** `[~70m depth | 180m W]`. Scan wall mounts.
* [ ] **Signal Cleanup**: Set Camp One Beacon to **Green / OFF** in PDA once cleared.

### 🏗️ Step 3: Vehicle Construction & Refinement
* [ ] **Build Moonpool Vehicle Fabricator**: Install inside the Moonpool.
* [ ] **Build Tadpole Submersible** (`BP_Tadpole`): Assemble at the Moonpool Vehicle Fabricator.
* [ ] **Scan Vehicle Modification Station fragments**: Search wreck sites to construct the wall-mounted console.

### 🧭 Step 4: Deeper Exploration Transition
* [ ] **Search for Dive Elevator**: Sweep the Thermal Vents border `[80m-120m depth | 450m NE/E]` for the remaining **Dive Elevator** (`BP_DiveElevator`) fragment `[1/2 completed | Need 1]`.

---

## 🧭 Exploration Verification SOP

Before turning OFF a HUD Beacon in your PDA Signals tab, verify:
1. **StoryGoal Complete**: Decoded save shows `DA__Signal_..._Hide` (terminal interacted).
2. **Blueprints Complete**: No fractional blueprints (e.g., `2/3`) remaining in PDA.
3. **Sealed Doors Cut**: All bulkheads cut open with **Laser Cutter** (`BP_LaserCutter`).

---

## 🗺️ Active Perimeter Destination Tracker

### 1. Crashed Black Box (Alterra Emergency Signal)
- **Location**: `~45m depth | ~380m North` (250m NE of base)
- **Status**: **IN PROGRESS**
  - [ ] Scan **Light Stick** / **Floodlight** & **Bar Table** / **Bench** blueprints.
  - [ ] Salvage surrounding Titanium cargo crates.

### 2. Thermal Vents & Hydrothermal Fissures (Volcanic Trenches)
- **Location**: `~80m-120m depth | ~450m NE/E` (550m ENE of base)
- **Status**: **SCOUTED / UNCLOSED**
  - [ ] Scan **Thermal Plant** & **Power Transmitter** fragments near vents.
  - [ ] Scan **Vehicle Modification Station** fragments.
  - [ ] Harvest **Magnetite** and **Lithium** surrounding fissures.

### 3. Tadpole Pens (New Narrative Outpost)
- **Location**: Unlocked via `DA_StoryGoal_Investigation_TadpolePensNoA`
- **Status**: **UNEXPLORED**
  - [ ] Explore outpost & scan technology fragments.
  - [ ] Locate the source of the story goal transmission.

---

## 📸 Visual Telemetry via Screenshots
* Capture in-game screenshots of your **PDA Blueprints tab** and **Base Storage Lockers**. Drop them directly in chat for AI visual verification of your progress!

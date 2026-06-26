# Subnautica 2 Progression Roadmap & Exploration Tracker

A structured coaching roadmap and systematic exploration checklist for **Subnautica 2** (Early Access Standalone / Unreal Engine 5).

> [!NOTE]
> **Primary Progression Manual**: For clinical biome geometry matrices, high-level progression phases, beginner survival wisdom, transition criteria, and official dev news links, consult [GUIDE.md](./GUIDE.md).
> **Live Diagnostic Telemetry**: For dynamic progression state, active tool loadouts, inventory registers, and world streaming partition flags decoded from `savegame_1.sav`, consult [REPORT.md](./REPORT.md).

---

## 📋 Sequenced Action Roadmap (Next Session Focus)

> [!IMPORTANT]
> **Active Origin**: Starting safely inside **Angel Comb Base** (`~30m depth`) with a functional power grid (6 Solar, 3 Hydro Turbines), Biolab, Processor, and Scanner Station.

### 📍 Step 1: Scanner Room Calibration & visor HUD Setup
* [ ] **Harvest Table Coral & Copper**: Use your Survival Knife on canyon walls to slice red/green shelf corals for **Table Coral Samples** (`BP_TableCoral`). Gather Copper.
* [ ] **Craft Scanner Room Upgrades**:
  - [ ] Craft **Scanner Room Range Upgrades** (`BP_ScannerRoomUpgrade_Range`) at the Scanner Room console to extend radar coverage.
  - [ ] Craft the **Scanner Room HUD Chip** at the Fabricator and equip it. *This highlights scanned resources directly on your visor!*
* [ ] **Locate Key Materials**: Set Scanner Room to target **Galena Outcrops** (for Lead) and **Table Coral** to stock up on building materials.

### 🏊‍♂️ Step 2: Wreckage Clean-up & Blueprint Close-out
Set your Scanner Room to target **Technology Fragments** to pinpoint these items:
* [ ] **Close out Camp One Wreckage** *(Swim ~180m West | ~70m depth)*:
  - [ ] Scan final **Repair Tool** (`BP_RepairTool`) fragment (2/3 completed, `+1` left). *Then craft it at your Fabricator!*
  - [ ] Scan final **Work Light** (`BP_WorkLight`) fragment (1/2 completed, `+1` left).
  - [ ] Scan remaining **Wall Rack** (`BP_WallRack`) fragments (1/3 completed, `+2` left).
  - [ ] Scan broken **Battery Charger** (`BP_BatteryCharger`) terminals on bunker walls (`2` scans needed to unlock battery recharging).
  - [ ] Set Camp One Beacon to **Green** / OFF once clear.
* [ ] **Scan Mobile Vehicle Bay Fragments**: Check along the 100m shelf border and near the Welcome Center BioLab hangar for floating **Mobile Vehicle Bay** (`BP_MobileVehicleBay`) consoles. Scan to unlock.

### 🏗️ Step 3: Vehicle Construction & Refinement
* [ ] **Process Advanced Alloys**: Gather raw Titanium and Germanium, and use your base **Processor** to refine:
  - [ ] **Titanium Ingots**
  - [ ] **Germanium Ingots**
* [ ] **Build & Deploy Mobile Vehicle Bay**: Craft at the Fabricator, take it to the surface, and deploy it.
* [ ] **Build Tadpole Submersible**: Use the Mobile Vehicle Bay to construct your unlocked **Tadpole Submersible** (`BP_Tadpole`).

### 🧭 Step 4: Deeper Exploration Transition
* [ ] **Search for Dive Elevator**: Sweep the Thermal Vents border and deeper areas for the remaining **Dive Elevator** (`BP_DiveElevator`) fragment (1/2 completed, `+1` left) to enable easy vertical transport to deeper biomes.
* [ ] **HUD Triage**: Toggle OFF/Green any cleared beacons (`Wu Lianghai`, `Old Habitat`, `Blackbox - Ruby`, `Camp One`) to keep your compass clean.

---

## 🧭 Exploration Verification SOP ("Closing Out" & Disabling Signals)

Before marking an area as **Closed / Fully Explored** and toggling OFF its HUD Beacon in your PDA Signals tab, verify against these 3 concrete pieces of evidence:
1. **Telemetry StoryGoal Trigger (`_Hide`)**: Check [savegame_1_decoded.md](./backups/savegame_1_decoded.md#L227). When you interact with a major signal's core terminal, the engine records `DA__Signal_..._Hide`. If `_Hide` is present, the primary narrative objective is 100% complete.
2. **Zero Partial Blueprints (No Leftover Crates)**: Open your PDA **Blueprints** tab under `In Progress`. If you have unresolved fractions (like `2/3 Repair Tool`, `1/2 Dive Elevator`), wreckage sites you previously visited still contain un-scanned cargo crates!
3. **Sealed Bulkhead Audit (Laser Cutter Check)**: Many crashed Alterra structures contain sealed titanium bulkhead doors requiring a **Laser Cutter** (`BP_LaserCutter`). Do not disable its signal until you return with a cutting tool!

### Active Perimeter Destination Tracker

#### 1. Crashed Black Box (Alterra Emergency Signal)
- **Approx Location**: `~45m depth` | `~380m North` of Lifepod (`~250m Northeast` of Angel Comb Base).
- **Status**: **IN PROGRESS**
  - [ ] Scan Light Stick / Floodlight fragments and Bar Table / Bench decorative furniture blueprints.
  - [~] Emergency Radio Transmission Audio Log retrieved. *(Verify via Databank tab)*.
  - [ ] Salvage nearby Titanium cargo crates and copper wire nodes.

#### 2. Abandoned Basecamp & Habitat Beacon (Infected Crevasse Wreckage)
- **Approx Location**: `~70m depth` | `~420m West` of Lifepod (`~180m West` of Angel Comb Base along canyon shelf).
- **Status**: **NEEDS VERIFICATION (100%)**
  - [ ] Scan Multipurpose Room fragments (if partial), Composite Corridor sections, Exterior Growbed, Floodlight, and Battery Charger fragments.
  - [~] Colonist Bunker Pad #052 extracted. *(Verify via Databank tab)*.

#### 3. Thermal Vents & Hydrothermal Fissures (Volcanic Trenches)
- **Approx Location**: `~80m-120m depth` | `~450m NE/E` of Lifepod (`~550m ENE` of Angel Comb Base).
- **Status**: **SCOUTED / UNCLOSED**
  - [ ] Scan Thermal Plant fragments and Power Transmitter fragments near active volcanic vents.
  - [ ] Scan Vehicle Modification Station fragments.
  - [ ] Identify and harvest Magnetite and crystalline Lithium deposits surrounding hydrothermal fissures.

#### 4. Tadpole Pens (New Narrative Outpost)
- **Approx Location**: Unlocked via PDA story goal (`DA_StoryGoal_Investigation_TadpolePensNoA`).
- **Status**: **UNEXPLORED**
  - [ ] Explore the Tadpole Pens area and scan technology fragments.
  - [ ] Locate the source of the story goal transmission.

* **Visual Telemetry via Screenshots**: Capture in-game screenshots of your **PDA Blueprints tab** and **Base Storage Lockers**. Share or drop these screenshots directly in chat for 100% AI vision verification!

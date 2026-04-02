> **English.** Korean (정본): [SEMICONDUCTOR_MATERIALS_BRIDGE.md](SEMICONDUCTOR_MATERIALS_BRIDGE.md)

# Semiconductor / fabless ↔ real materials (`3_meterial`) bridge

**Purpose:** State what `Fabless`, `Foundry_Implementation_Engine`, and L4 `design_workspace` **do not replace**, and where **wafer feedstock, gases, dopants, and metals** should grow inside `3_meterial` element foundations.

---

## 1. Keep two layers separate

| Layer | Scope | Typical paths | Documented non-goals |
|-------|--------|---------------|----------------------|
| **Design / handoff gates** | φ,n,p,J-style eval, Ω, DRC/LVS/timing **readiness** tick | `2_operational/40_SPATIAL_LAYER/Fabless/`, `_staging/Foundry_Implementation_Engine/`, `_staging/design_workspace/` | Not fab **process physics, yield, or capacity** ([FOUNDRY_AND_FABLESS_NAV_EN.md](../../../../_staging/design_workspace/docs/FOUNDRY_AND_FABLESS_NAV_EN.md)) |
| **Materials / supply / screening** | Refining, impurities, thermal budget, **hype filters** | `Silicon_Foundation`, `Fluorine_Foundation`, `Boron_Foundation`, `Gallium_Germanium_Foundation`, `Copper_Zinc_Foundation`, `Arsenic_Antimony_Bismuth_Foundation`, … | Not GDSII / PDK / layout |

Prefer **chemical and metallurgy constraints the fab consumes** as element foundations, and use design-stack engines for **contracts and observations**, not a full process simulator crammed into `3_meterial`.

---

## 2. Short reading order

1. Term split: [FOUNDRY_AND_FABLESS_NAV_EN.md](../../../../_staging/design_workspace/docs/FOUNDRY_AND_FABLESS_NAV_EN.md)  
2. Spatial-layer semiconductor eval stub: `2_operational/40_SPATIAL_LAYER/SemiconductorPhysics_Eval_Engine/`  
3. Materials anchors: `Silicon_Foundation` → then `Phosphorus_Foundation`, `Boron_Foundation`, `Fluorine_Foundation`, `Gallium_Germanium_Foundation` / `Indium_Thallium_Foundation`, `Copper_Zinc_Foundation` / `Aluminum_Titanium_Foundation`, `Arsenic_Antimony_Bismuth_Foundation` as needed  
4. Fabless structural roadmap: `Fabless/docs/REAL_FABLESS_ENGINE_EXTENSION_ANALYSIS_AND_DESIGN.md`

---

## 3. Suggested materials expansion priority

**Strengthen cross-links first (foundations already exist)**  
Wafer narrative: `Silicon_Foundation`  
Etch / clean / halides: `Fluorine_Foundation`, `Sulfur_Foundation` (sulfuric loops)  
Dopants / glass: `Boron_Foundation`, `Phosphorus_Foundation`, `Arsenic_Antimony_Bismuth_Foundation`  
Contacts / interconnect: `Copper_Zinc_Foundation`, `Silver_Gold_Foundation`, `Aluminum_Titanium_Foundation`  
High-κ adjacency: no standalone Hf engine yet — reuse `Zirconium_Hafnium_Foundation` separation narrative where useful  

**Process consumables (partially covered)**  
Photoresist + CMP slurry framing: **`Photolithography_CMP_Foundation`** (`3_meterial/`) — EHS/waste screening; not EDA.  
Specialty gas mixes / leak safety: bridge `Element_Capture_Foundation` + `Fluorine_Foundation` (room for a dedicated axis)  

Update **[ELEMENT_REGISTRY.md](../ELEMENT_REGISTRY.md)** before adding folders.

---

## 4. “Toilet” axis (spacecraft waste) — not wafer materials

If **toilet** means **habitat waste / ventilation contingencies**, the repo has `_staging/Spacecraft_Waste_Loop_Foundation/` (toilet / urine loop / fan faults). That axis is **ECLSS / fluids / air quality**, not chip materials; natural ties: `Element_Capture_Foundation`, `Oxygen_Foundation`, `Hydrogen_Foundation`.

---

## 5. One-line takeaway

**Fabless / foundry tick** = design **gates**; **fab chemicals, metals, gases** = grow **`3_meterial` foundations**. Next concrete work: (A) cross-link READMEs across the table above, (B) scaffold **specialty gas / wet clean** gaps, or (C) tighten **Fabless Phase 1–2 contracts** — pick one sequence.

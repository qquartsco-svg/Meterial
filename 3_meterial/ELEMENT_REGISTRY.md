# Element Registry

> `3_meterial` 안 원소·복합·공정 foundation의 상태, 정본 위치, 연결 대상을 추적하는 등록부.

## 경로 표기

- 허브의 현재 로컬/문서 표기는 **`3_meterial/`** 로 통일한다.
- 아래 **Source of Truth** 열도 논리 경로 `3_meterial/<Folder>/` 로 적는다.

## 목적

- 원소명·Z·**단일/복합/클러스터** 구분
- 상태: `active` | `planned` | `scaffold`
- 정본 위치(허브 폴더)
- 직접 연결되는 형제 엔진(요약)

새 폴더를 만들기 전에 **이 표를 먼저 갱신**한다.

---

## 기초 루트 (원소 슬롯 아님)

| 엔진 | Status | Source of Truth | 역할 요약 |
|------|--------|-----------------|-----------|
| **Chemical_Reaction_Foundation** | `active` | `3_meterial/Chemical_Reaction_Foundation/` | 반응 동역학·평형·전기화학 공통층 |
| **Element_Capture_Foundation** | `active` | `3_meterial/Element_Capture_Foundation/` | CO₂·H₂·He·O₂·N₂ 등 포집·분리 |

---

## 원소·복합 foundation (`active`, Z 순)

단일 Z는 한 행. 둘 이상은 **Z** 열에 `·` 로 묶는다. **Kind**: `single` | `pair` | `cluster` | `family`.

| Z | Symbol(s) | Name (요약) | Kind | Source of Truth | Primary Links (요약) |
|---|-----------|-------------|------|-----------------|----------------------|
| 1 | H | Hydrogen | single | `3_meterial/Hydrogen_Foundation/` | `Chemical_Reaction_Foundation`, `Element_Capture`, 배터리·수소경제 |
| 2 | He | Helium | single | `3_meterial/Helium_Foundation/` | `Chemical_Reaction_Foundation`, `Element_Capture`, 극저온 |
| 3 | Li | Lithium | single | `3_meterial/Lithium_Foundation/` | `Chemical_Reaction_Foundation`, `Battery_Dynamics_Engine` |
| 4 | Be | Beryllium | single | `3_meterial/Beryllium_Foundation/` | 경량·독성·가공 |
| 5 | B | Boron | single | `3_meterial/Boron_Foundation/` | 유리·복합재·도핑 |
| 6 | C | Carbon | single | `3_meterial/Carbon_Foundation/` | 동소체·CO₂≠C·흑연; `Carbon_Composite_Stack`·C1 환원과 정합 |
| 7 | N | Nitrogen | single | `3_meterial/Nitrogen_Foundation/` | `Element_Capture`, Haber·ASU, 비료 축 |
| 8 | O | Oxygen | single | `3_meterial/Oxygen_Foundation/` | `Element_Capture`, `Hydrogen`, 산화제 |
| 9 | F | Fluorine | single | `3_meterial/Fluorine_Foundation/` | 전해질·HF 리스크 |
| 11·17 | Na·Cl | Sodium / Chlorine | pair | `3_meterial/Sodium_Chlorine_Foundation/` | 염·chlor-alkali·부식 |
| 12·20 | Mg·Ca | Magnesium / Calcium | pair | `3_meterial/Magnesium_Calcium_Foundation/` | 전해질·합금 부식 |
| 13·22 | Al·Ti | Aluminum / Titanium | pair | `3_meterial/Aluminum_Titanium_Foundation/` | 구조재·갈바닉 |
| 14 | Si | Silicon | single | `3_meterial/Silicon_Foundation/` | `Foundry_Implementation_Engine`, `Fabless`, `SemiconductorPhysics_Eval_Engine`, PV |
| 15 | P | Phosphorus | single | `3_meterial/Phosphorus_Foundation/` | 비료·ATP·N-P-K |
| 16 | S | Sulfur | single | `3_meterial/Sulfur_Foundation/` | 황산·Li-S |
| 19 | K | Potassium | single | `3_meterial/Potassium_Foundation/` | 전해질·포타시 |
| 21·39 | Sc·Y | Scandium / Yttrium | pair | `3_meterial/Scandium_Yttrium_Foundation/` | 합금·YSZ·RE 꼬리 |
| 23 | V | Vanadium | single | `3_meterial/Vanadium_Foundation/` | VRFB·합금 |
| 24·28 | Cr·Ni (스테인리스) | Chromium / Nickel | pair | `3_meterial/Chromium_Nickel_Stainless_Foundation/` | 스테인리스·피팅 |
| 25·27·28 | Mn·Co·Ni | MCN | cluster | `3_meterial/Manganese_Cobalt_Nickel_Foundation/` | NMC·배터리 |
| 26 | Fe | Iron | single | `3_meterial/Iron_Foundation/` | 제강·부식 |
| 29·30 | Cu·Zn | Copper / Zinc | pair | `3_meterial/Copper_Zinc_Foundation/` | 도체·황동·부식 |
| 31·32 | Ga·Ge | Gallium / Germanium | pair | `3_meterial/Gallium_Germanium_Foundation/` | 전력·RF·박막 |
| 37·55 | Rb·Cs | Rubidium / Cesium | pair | `3_meterial/Rubidium_Cesium_Foundation/` | 1족 확장·반응성 |
| 38·56 | Sr·Ba | Strontium / Barium | pair | `3_meterial/Strontium_Barium_Foundation/` | 2족·화종·시추 |
| 40·72 | Zr·Hf | Zirconium / Hafnium | pair | `3_meterial/Zirconium_Hafnium_Foundation/` | 핵·세라믹·분리 |
| 41·73 | Nb·Ta | Niobium / Tantalum | pair | `3_meterial/Niobium_Tantalum_Foundation/` | 합금·커패시터 |
| 42 | Mo | Molybdenum | single | `3_meterial/Molybdenum_Foundation/` | 합금·촉매 |
| 47·79 | Ag·Au | Silver / Gold | pair | `3_meterial/Silver_Gold_Foundation/` | 접점·비용 |
| 48·80 | Cd·Hg | Cadmium / Mercury | pair | `3_meterial/Cadmium_Mercury_Foundation/` | 중금속·규제 |
| 49·81 | In·Tl | Indium / Thallium | pair | `3_meterial/Indium_Thallium_Foundation/` | ITO·CIGS·Tl 독성 |
| 50·82 | Sn·Pb | Tin / Lead | pair | `3_meterial/Tin_Lead_Foundation/` | 납땜·RoHS |
| — | Pt·Pd·Rh | Platinum group | family | `3_meterial/Platinum_Group_Foundation/` | 촉매·PGM |
| — | Ru·Ir·Os | PGM 확장 | family | `3_meterial/Ruthenium_Iridium_Osmium_Foundation/` | 전기촉매·Os 독성 |
| — | Nd·Dy… | 희토 자석 | cluster | `3_meterial/Rare_Earth_Magnet_Foundation/` | 자석·공급 |
| — | Ce·La | 산소저장·촉매 | pair | `3_meterial/Ceria_Lanthanum_Foundation/` | CeO₂·촉매 슬러리 |
| — | La·Ce·Pr | 경량 란타너드 | cluster | `3_meterial/Lanthanum_Cerium_Praseodymium_Foundation/` | 분리 연쇄 |
| — | Co·Mn 스피넬 | 스피넬 | cluster | `3_meterial/Cobalt_Manganese_Spinel_Foundation/` | 배터리·열 |
| 74 | W | Tungsten | single | `3_meterial/Tungsten_Foundation/` | 초고온·경도 |
| 75 | Re | Rhenium | single | `3_meterial/Rhenium_Foundation/` | Mo/W 다음 6족 |
| — | U·Th | Actinide (연료) | pair | `3_meterial/Uranium_Thorium_Foundation/` | 핵연료·폐기물 |
| 94 | Pu | Plutonium | single | `3_meterial/Plutonium_Foundation/` | 임계·거버넌스 |
| — | Am·Cm | Actinide (확장) | pair | `3_meterial/Americium_Curium_Foundation/` | α원·RTG |
| — | Ne·Ar·Kr·Xe | 희가스 확장 | cluster | `3_meterial/Rare_Gas_Extended_Foundation/` | ASU·극저온 |
| 86 | Rn | Radon | single | `3_meterial/Radon_Foundation/` | 실내·U/Th 연쇄 |
| 33·51·83 | As·Sb·Bi | Pnictogen 준금속 | cluster | `3_meterial/Arsenic_Antimony_Bismuth_Foundation/` | 독성·도핑 |
| — | Tc·Pm | 합성 불안정 | pair | `3_meterial/Technetium_Promethium_Foundation/` | 의료·동위원소 |
| 35·53 | Br·I | Bromine / Iodine | pair | `3_meterial/Iodine_Bromine_Foundation/` | 해수·할로겐 |
| 34·52 | Se·Te | Selenium / Tellurium | pair | `3_meterial/Selenium_Tellurium_Foundation/` | PV·Te 부산물 |

---

## 공정·비료·수계 번들 (주기 슬롯 밖, `active`)

| 엔진 | Source of Truth | 역할 요약 |
|------|-----------------|-----------|
| Syngas_Water_Gas_Shift_Foundation | `3_meterial/Syngas_Water_Gas_Shift_Foundation/` | CO+H₂·WGS |
| Methanol_Synthesis_Foundation | `3_meterial/Methanol_Synthesis_Foundation/` | CH₃OH 합성 |
| Fischer_Tropsch_Liquids_Foundation | `3_meterial/Fischer_Tropsch_Liquids_Foundation/` | FT 액체 |
| Ammonia_Process_Integration_Foundation | `3_meterial/Ammonia_Process_Integration_Foundation/` | NH₃ 플랜트 |
| Urea_CO2_Loop_Foundation | `3_meterial/Urea_CO2_Loop_Foundation/` | 요소·CO₂ 루프 |
| Nitric_Ammonium_Foundation | `3_meterial/Nitric_Ammonium_Foundation/` | 질산·AN |
| Ammonium_Phosphate_Foundation | `3_meterial/Ammonium_Phosphate_Foundation/` | MAP/DAP |
| Potassium_Chloride_Brine_Foundation | `3_meterial/Potassium_Chloride_Brine_Foundation/` | MOP·브라인 |
| NPK_Blend_Eutrophication_Foundation | `3_meterial/NPK_Blend_Eutrophication_Foundation/` | NPK·부영양화 |
| Seawater_Bittern_MgCl2_Foundation | `3_meterial/Seawater_Bittern_MgCl2_Foundation/` | 비턴·MgCl₂·배출 |
| Silicate_Fertilizer_Foundation | `3_meterial/Silicate_Fertilizer_Foundation/` | 규산염 비료 |
| Organic_Matter_Microbial_Fertilizer_Foundation | `3_meterial/Organic_Matter_Microbial_Fertilizer_Foundation/` | 유기·미생물 비료 |
| Photolithography_CMP_Foundation | `3_meterial/Photolithography_CMP_Foundation/` | 포토레지스트·CMP; EHS·폐액; EDA 비대체 |

---

## 응용 스택 (원소 표와 별도, `active`)

| 엔진 | Source of Truth | 비고 |
|------|-----------------|------|
| Carbon_Composite_Stack | `3_meterial/Carbon_Composite_Stack/` | 탄소 복합재 경화·구조; **원소 탄소 서사는 `Carbon_Foundation`** 과 병행 |
| Cooking_Process_Foundation | `3_meterial/Cooking_Process_Foundation/` | 요리·식품 화학 |
| Battery_Dynamics_Engine | `3_meterial/Battery_Dynamics_Engine/` | 전기화학 응용 (허브 복사본·`SOURCE_OF_TRUTH.md` 참고) |

---

## `planned` · 미승격

| Z | Symbol | 비고 |
|---|--------|------|
| 11 | Na | 단독 폴더 없음 → **`Sodium_Chlorine_Foundation`** 에서 active. |
| 12 | Mg | 단독 폴더 없음 → **`Magnesium_Calcium_Foundation`** 에서 active. |
| 17 | Cl | 단독 폴더 없음 → **`Sodium_Chlorine_Foundation`** 에서 active. |

---

## 반도체 소재 ↔ 설계 스택

웨이퍼 이전 **Si** 와, **B / P / As·Sb·Bi / F / Cu·Al / Ga·Ge / …** 를 칩 공급망 서사로 묶는 우선순위·비목표는 [docs/SEMICONDUCTOR_MATERIALS_BRIDGE.md](docs/SEMICONDUCTOR_MATERIALS_BRIDGE.md) 를 본다. (산업 “파운드리” vs `foundry.implementation.tick` 용어 분리: `_staging/design_workspace/docs/FOUNDRY_AND_FABLESS_NAV.md`.)

---

## Reading Rules

1. **`active`** — README·tests·signature 등으로 foundation 로 읽을 수 있음 (허브 기준).  
2. **`scaffold`** — 폴더는 있으나 규약 미완.  
3. **`planned`** — 폴더 없이 필요성만 기록.

*마지막 동기화: 허브 `3_meterial/` 내 `VERSION` 보유 폴더 기준 전수 대조.*

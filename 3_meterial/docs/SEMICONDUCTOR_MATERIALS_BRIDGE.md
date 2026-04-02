> **한국어 (정본).** English: [SEMICONDUCTOR_MATERIALS_BRIDGE_EN.md](SEMICONDUCTOR_MATERIALS_BRIDGE_EN.md)

# 반도체·팹리스 ↔ 실제 소재(3_meterial) 브리지

**목적:** `Fabless` / `Foundry_Implementation_Engine` / L4 `design_workspace` 가 **무엇을 하지 않는지**와, **웨이퍼·전구·가스·금속** 같은 **물질 층**을 `3_meterial` 원소 foundation 어디에서 키울지 한 장으로 고정한다.

---

## 1. 두 층을 섞지 않기

| 층 | 다루는 것 | 대표 경로 | 비목표(문서상) |
|----|-----------|-----------|----------------|
| **설계·인도 게이트** | φ,n,p,J 시뮤, Ω, DRC/LVS/timing **준비도** 틱 | `2_operational/40_SPATIAL_LAYER/Fabless/`, `_staging/Foundry_Implementation_Engine/`, `_staging/design_workspace/` | 팹 **공정 물리·수율·CAPA** 를 대체하지 않음 ([FOUNDRY_AND_FABLESS_NAV.md](../../../../_staging/design_workspace/docs/FOUNDRY_AND_FABLESS_NAV.md)) |
| **소재·공급망·스크리닝** | 정제, 불순물, 열예산, **과장 주장 필터** | `Silicon_Foundation`, `Fluorine_Foundation`, `Boron_Foundation`, `Gallium_Germanium_Foundation`, `Copper_Zinc_Foundation`, `Arsenic_Antimony_Bismuth_Foundation`, … | GDSII·PDK·레이아웃 엔진이 아님 |

즉 **칩을 “만드는 공정 시뮬레이터”** 를 `3_meterial` 에 억지로 넣기보다, **공정이 먹는 화학·금속·가스의 현실 제약**을 원소 foundation 으로 쌓고, 설계 축 엔진은 **계약·관측**으로 연결하는 편이 서사가 안 꼬인다.

---

## 2. 읽기 순서 (짧게)

1. 용어 분리: [FOUNDRY_AND_FABLESS_NAV.md](../../../../_staging/design_workspace/docs/FOUNDRY_AND_FABLESS_NAV.md)  
2. 설계 측 반도체 물리 eval (허브 내): `2_operational/40_SPATIAL_LAYER/SemiconductorPhysics_Eval_Engine/`  
3. 소재 축 앵커: `Silicon_Foundation` → (필요 시) `Phosphorus_Foundation`(n형 도펀트 서사), `Boron_Foundation`(p형/유리·도핑), `Fluorine_Foundation`(HF·특가스), `Gallium_Germanium_Foundation` / `Indium_Thallium_Foundation`(III–V·박막), `Copper_Zinc_Foundation` / `Aluminum_Titanium_Foundation`(배선·금속 층), `Arsenic_Antimony_Bismuth_Foundation`(준금속·도핑·독성)  
4. 팹리스 “실제 엔진 구조” 로드맵(계약·프리셋): `Fabless/docs/REAL_FABLESS_ENGINE_EXTENSION_ANALYSIS_AND_DESIGN.md`

---

## 3. 소재 확장 우선순위 (제안)

**이미 있는 foundation 으로 덮는 범위 (먼저 정합만 강화)**  
- Si 웨이퍼·다이 이전 **재료 스토리**: `Silicon_Foundation`  
- 절연·식각·세정 쪽 **할로겐/산**: `Fluorine_Foundation`, `Sulfur_Foundation`(황산 루프와 교차)  
- **도펀트·유리**: `Boron_Foundation`, `Phosphorus_Foundation`, `Arsenic_Antimony_Bismuth_Foundation`  
- **접촉·배선·범프**: `Copper_Zinc_Foundation`, `Silver_Gold_Foundation`, `Aluminum_Titanium_Foundation`  
- **고k·레어 인접**(개념): `Hafnium` 은 아직 단독 엔진 없음 → `Zirconium_Hafnium_Foundation` 에서 분리 난이도 서사 활용 가능  

**공정 소모품 (일부 반영됨)**  
- 포토레지스트·CMP 슬러리: **`Photolithography_CMP_Foundation`** (`3_meterial/`) — EHS·폐액 스크리닝; EDA 대체 아님.  
- 특가스 믹스·누설 안전: `Element_Capture_Foundation` + `Fluorine_Foundation` 브리지 (별도 축으로 더 쌓을 수 있음)  

새 폴더 전에 **[ELEMENT_REGISTRY.md](../ELEMENT_REGISTRY.md)** 부터 갱신하는 것이 레포 원칙이다.

---

## 4. “토일렛” 축 (우주선 폐기물) — 칩과 분리

사용자 표현 **토일렛** 이 **우주 거주체 폐기물/환기 루프** 를 가리키는 경우, 코드베이스에서는 `_staging/Spacecraft_Waste_Loop_Foundation/` 이 **변기·소변 루프·팬 고장** 을 상위 contingencies 와 묶는다.  
이 축은 **웨이퍼 소재** 가 아니라 **생명유지·유체·공기질** 이며, 확장 시 `Element_Capture_Foundation`(O₂/H₂O), `Oxygen_Foundation`, `Hydrogen_Foundation` 과의 **거주환경 정합**이 자연스럽다.

---

## 5. 한 줄 정리

- **팹리스/파운드리 틱** = 설계·인도 **게이트**; **공정 약품·금속·가스** = `3_meterial` **원소·복합 foundation** 쪽으로 확장.  
- 다음 작업은 (A) 위 표의 **기존 엔진 README 상호 링크** 보강, (B) **특가스·세정** 등 남은 공정 화학 축 스캐폴드, (C) `Fabless` 쪽 **Phase 1–2 계약 문서** 강화 — 중 하나를 택해 순차 적용하면 된다.

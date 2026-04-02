# 3_meterial — 메테리얼 레이어

> **인식론적 위치:** E5 Chemistry — [EPISTEMIC_LAYER_MAP.md](../../../EPISTEMIC_LAYER_MAP.md)

`0_observers`(물리 관측) · `1_calculator`(수학 계산) · `2_operational`(운영 레이어)과 같은 레벨의 **화학 전용 허브**.

> **중요:** 이 폴더는 우선 **meterial connection hub / index hub** 로 읽는 것이 맞다.  
> 여기 있는 엔진 중 일부는 `_staging` 또는 `2_operational/*` 쪽에 이미 정본이 있고,  
> `3_meterial` 은 그 정본들을 **화학·소재 축 관점에서 다시 묶어 보는 연결 허브**다.

---

## 왜 별도 허브인가

화학은 공학(E4)과 생물학(E6) 사이를 잇는 다리 역할을 한다.
기존에 화학 관련 엔진들이 `40_SPATIAL`, `60_APPLIED`, `_staging` 등에 흩어져 있었다.
이 폴더에 실체 복사본을 모아서 **화학 레이어의 연결 흐름**을 한눈에 볼 수 있게 정리한다.
즉 목적은 “중복 저장”이 아니라, **화학 관점의 구조 읽기와 graft 실험**에 가깝다.

```
0_observers/   ← 물리 관측 (Newton → Feynman)
1_calculator/  ← 수학 계산 (CMP, VectorSpace)
2_operational/ ← 운영 레이어 (PLANET → TRIBES)
3_meterial/    ← ★ 메테리얼 레이어 (반응, 원소, 재료, 수소, 배터리, 요리)
```

---

## 반도체·팹리스 ↔ 소재 확장

팹리스(`40_SPATIAL_LAYER/Fabless`)·파운드리 인도 틱(`Foundry_Implementation_Engine`)은 **설계·게이트** 층이고, **웨이퍼·약품·가스·금속** 은 이 허브의 **원소 foundation** 층에서 키운다. 경계와 우선순위는 [docs/SEMICONDUCTOR_MATERIALS_BRIDGE.md](docs/SEMICONDUCTOR_MATERIALS_BRIDGE.md) 에 정리했다. (영문: [SEMICONDUCTOR_MATERIALS_BRIDGE_EN.md](docs/SEMICONDUCTOR_MATERIALS_BRIDGE_EN.md))

---

## 폴더 구조

> **물리 배치와 개념 배치는 다르다.**
> 현재 실제 폴더는 호환성과 기존 링크 유지를 위해 **flat layout** 으로 둔다.
> 대신 읽는 방식은 아래의 **chemical root -> element foundations -> applied engines** 순서를 따른다.

```
3_meterial/
├── README.md                        ← 이 문서
├── FOLDER_STRUCTURE.md              ← flat layout을 어떻게 읽는지 설명
├── ELEMENT_REGISTRY.md              ← 원소 등록부
├── ELEMENT_FOUNDATION_TEMPLATE.md   ← 새 원소 scaffold 규격
├── CHEMICAL_GOVERNANCE.md           ← 운영 규칙
│
│  ── 핵심 기초 ──
├── Chemical_Reaction_Foundation/    ← 반응 동역학 기초 (ΔG, Arrhenius, K_eq, Nernst)
├── Element_Capture_Foundation/      ← 원소 포집·분리·저장 (CO₂, H₂, He, O₂, N₂)
├── Hydrogen_Foundation/             ← Z=1 수소 (생산, 저장, 연료전지, 안전, 스크리닝)
├── Syngas_Water_Gas_Shift_Foundation/ ← CO+H₂·WGS (개질·비율·CO 독성; H₂ 다음)
├── Methanol_Synthesis_Foundation/   ← CH₃OH (평형·재순환·촉매; syngas 다음)
├── Fischer_Tropsch_Liquids_Foundation/ ← FT 액체 (ASF 분포·경가스·CO₂ 꼬리; syngas 다음)
├── Helium_Foundation/               ← Z=2 헬륨 (조달, 극저온, 희소성, 스크리닝)
├── Lithium_Foundation/              ← Z=3 리튬 (추출, 배터리 결합, 열안전, 재활용 스크리닝)
├── Phosphorus_Foundation/           ← Z=15 인 (인광석, ATP 루프, N-P-K, 스크리닝)
├── Ammonium_Phosphate_Foundation/   ← MAP/DAP (N-P 결합·습기·토양 pH 카툰)
├── Silicon_Foundation/              ← Z=14 규소 (정제, 결함/수율, 열예산, 스크리닝)
├── Photolithography_CMP_Foundation/ ← 포토레지스트·CMP (EHS·폐액; EDA·게이트 틱 비대체)
├── Silicate_Fertilizer_Foundation/  ← 규산염·슬래그 비료 (풍화·즉시 P/Si 과장 스크리닝)
├── Iron_Foundation/                 ← Z=26 철 (제강 경로, 부식, 탄소집약도 스크리닝)
├── Sodium_Chlorine_Foundation/      ← Z=11/17 Na/Cl (염분부식, chlor-alkali, 안전)
├── Magnesium_Calcium_Foundation/    ← Z=12/20 Mg/Ca (전해질 항상성 + 경량합금 부식)
├── Aluminum_Titanium_Foundation/    ← Z=13/22 Al/Ti (구조재 선택 + 갈바닉 + 공정에너지)
├── Copper_Zinc_Foundation/          ← Z=29/30 Cu/Zn (전도도-가공성-부식 트레이드오프)
├── Potassium_Foundation/            ← Z=19 칼륨 (전해질 안전 + 포타시 비료 제약)
├── Potassium_Chloride_Brine_Foundation/ ← MOP KCl (증발·용액 채광·브라인 꼬리)
├── Seawater_Bittern_MgCl2_Foundation/ ← 해수·비턴·MgCl₂ (담수화 꼬리·배출·부식)
├── Manganese_Cobalt_Nickel_Foundation/ ← Z=25/27/28 MCN (NMC cathode 비율 트레이드오프)
├── Sulfur_Foundation/               ← Z=16 황 (황산 공정 + Li-S 셔틀 효과 제약)
├── Chromium_Nickel_Stainless_Foundation/ ← Z=24/28 Cr/Ni (스테인리스 수동피막 + 피팅)
├── Fluorine_Foundation/             ← Z=9 F (전해질 성능 vs HF/지속성 리스크)
├── Boron_Foundation/                ← Z=5 B (보로실리케이트/복합재/도핑 제약)
├── Carbon_Foundation/               ← Z=6 C (동소체·CO₂≠탄소·흑연; CFRP와 구분)
├── Vanadium_Foundation/             ← Z=23 V (VRFB 레독스 저장 + 미세합금)
├── Molybdenum_Foundation/           ← Z=42 Mo (고온합금 + 촉매 내구/중독 제약)
├── Tungsten_Foundation/             ← Z=74 W (초고온/초경도 + 산화/취성 제약)
├── Rhenium_Foundation/              ← Z=75 Re (Mo/W 이후 6족: 초합금·개질 촉매·희소)
├── Silver_Gold_Foundation/          ← Z=47/79 Ag/Au (전도·접점 안정성 vs 비용)
├── Platinum_Group_Foundation/       ← Pt/Pd/Rh (촉매 활성 vs 중독/공급 임계성)
├── Ruthenium_Iridium_Osmium_Foundation/ ← Ru/Ir/Os (PGM 확장·전기촉매·Os 독성)
├── Rare_Earth_Magnet_Foundation/    ← Nd/Dy (자속 밀도 vs 열탈자/공급 집중)
├── Gallium_Germanium_Foundation/    ← Z=31/32 Ga/Ge (전력/RF/광전자 성능 vs 열/공급)
├── Indium_Thallium_Foundation/      ← In/Tl (13족 Ga/Ge 이후: ITO·CIGS vs Tl 급성독)
├── Niobium_Tantalum_Foundation/     ← Z=41/73 Nb/Ta (합금/커패시터 성능 vs 공급/고장)
├── Zirconium_Hafnium_Foundation/    ← Z=40/72 Zr/Hf (핵/고온세라믹 + 분리 난이도)
├── Ceria_Lanthanum_Foundation/      ← Ce/La (산소저장 촉매 + 공정폐기물 제약)
├── Cobalt_Manganese_Spinel_Foundation/ ← Co-Mn 스피넬 (열안전/공급망 제약)
├── Uranium_Thorium_Foundation/      ← U/Th (핵연료주기 + 안전거버넌스 제약)
├── Tin_Lead_Foundation/             ← Z=50/82 Sn/Pb (납땜·RoHS·납 독성·무연 수염)
├── Plutonium_Foundation/            ← Pu (임계성·안전보장·분리·폐기물; U/Th 보완축)
├── Americium_Curium_Foundation/     ← Am/Cm (Pu 이후: 밀봉 α원·RTG 꼬리·거버넌스)
├── Rare_Gas_Extended_Foundation/    ← Ne/Ar/Kr/Xe (ASU 꼬리·극저온·Xe 수요 변동)
├── Radon_Foundation/                ← Rn (희가스+방사: 실내·U/Th 붕괴 연쇄)
├── Beryllium_Foundation/            ← Z=4 Be (경량 강성 vs 분진·베릴리움증·가공)
├── Cadmium_Mercury_Foundation/      ← Cd/Hg (중금속·증기·규제·대체재)
├── Arsenic_Antimony_Bismuth_Foundation/ ← As/Sb/Bi (준금속 독성·환경이동·응용 분리)
├── Scandium_Yttrium_Foundation/     ← Z=21/39 Sc/Y (미세합금·YSZ·희토 부산물·분리 꼬리)
├── Lanthanum_Cerium_Praseodymium_Foundation/ ← La/Ce/Pr (경량 란타너드 분리 연쇄·촉매/배터리 인접)
├── Technetium_Promethium_Foundation/ ← Tc/Pm (합성·비안정: 의료 Tc·Pm 무안정동위원소)
├── Iodine_Bromine_Foundation/       ← I/Br (해수·브라인 공급·할로겐 부식·상호대체 불가)
├── Rubidium_Cesium_Foundation/      ← Rb/Cs (1족 K 이후: 반응성·발화·저장·공급)
├── Strontium_Barium_Foundation/     ← Sr/Ba (2족 Mg/Ca 이후: 화종·시추·페라이트)
├── Selenium_Tellurium_Foundation/   ← Se/Te (16족 S 이후: 박막 PV·부산물 Te)
├── Nitrogen_Foundation/             ← Z=7 질소 (공기분리, Haber 카툰, LN₂, 스크리닝)
├── Ammonia_Process_Integration_Foundation/ ← NH₃ 플랜트 (H₂ 결합·에너지·순환; N 다음)
├── Urea_CO2_Loop_Foundation/        ← 요소 NH₃+CO₂ (스트리퍼·CO₂ 순도·포집)
├── Nitric_Ammonium_Foundation/      ← 질산·AN (Ostwald·NOx·산화제 위험)
├── NPK_Blend_Eutrophication_Foundation/ ← NPK 혼합·시비 (도편·유출·부영양화)
├── Organic_Matter_Microbial_Fertilizer_Foundation/ ← 유기질·미생물제 (C:N·무기화·병원체)
├── Oxygen_Foundation/               ← Z=8 산소 (ASU, LOX, 전기분해 연동, 산화제 안전)
│
│  ── 재료·공정 ──
├── Carbon_Composite_Stack/          ← 탄소 복합재 물성·경화 동역학·공정
├── Battery_Dynamics_Engine/         ← 배터리 전기화학 (Nernst, SOC, 열관리)
│
│  ── 응용 화학 ──
└── Cooking_Process_Foundation/      ← 요리 화학 (Maillard, 열전달, 식품 안전)
```

현재 실제 폴더를 바로 옮겨서

- `_00_root/`
- `_10_elements/`
- `_20_applied/`

처럼 재배치하지 않는 이유는,
이미 다른 문서와 엔진 링크가 이 flat layout을 기준으로 얽혀 있기 때문이다.
지금 단계에서는 **실제 배치 변경보다, 읽는 규칙과 정본 표식을 먼저 고정**하는 편이 안전하다.

---

## 이 허브를 어떻게 읽어야 하는가

`3_meterial` 은 다음 세 질문에 답하기 위한 보기 창이다.

1. 화학의 **기초 원리**는 어디에 있는가?
2. 그 원리가 어떤 **응용 화학 엔진**으로 내려가는가?
3. 공학(E4)과 생물(E6) 사이에서 화학이 **무슨 연결 축**을 담당하는가?

그래서 여기서는 “정본이 어디 있나?”보다 먼저,
**“화학 흐름이 어디서 시작해 어디로 내려가는가?”** 를 읽는 것이 중요하다.

### 주기·족 축 정합 (읽는 순서 힌트)

폴더가 flat 이더라도, **이미 있는 족(族) 엔진 다음**에 확장 엔진을 붙여 읽으면 개념이 꼬이지 않는다.

- **1족(알칼리):** `Potassium_Foundation` → `Rubidium_Cesium_Foundation` (Na·Li는 각각 `Sodium_Chlorine_Foundation`, `Lithium_Foundation`)
- **2족(알칼리 토류):** `Magnesium_Calcium_Foundation` → `Strontium_Barium_Foundation`
- **16족(칼코젠):** `Sulfur_Foundation` → `Selenium_Tellurium_Foundation` (CdTe 논의는 `Cadmium_Mercury_Foundation` 과 교차)
- **할로겐:** `Fluorine_Foundation`, `Iodine_Bromine_Foundation`, `Sodium_Chlorine_Foundation`(Cl) — 상호 대체 불가·부식 차이는 `Iodine_Bromine_Foundation` 에서 정리
- **6족(난용·촉매 꼬리):** `Molybdenum_Foundation` · `Tungsten_Foundation` → `Rhenium_Foundation`
- **PGM 확장:** `Platinum_Group_Foundation` → `Ruthenium_Iridium_Osmium_Foundation`
- **13족(디스플레이·박막):** `Gallium_Germanium_Foundation` → `Indium_Thallium_Foundation` (In과 Tl 독성 계급 혼동 금지)
- **희가스·방사:** `Rare_Gas_Extended_Foundation` → `Radon_Foundation` (붕괴 원천·실내 농도는 `Uranium_Thorium_Foundation` 과 연계)
- **합성·비안정(란타너드 인접):** `Lanthanum_Cerium_Praseodymium_Foundation` → `Technetium_Promethium_Foundation`
- **악티니드 후단:** `Plutonium_Foundation` → `Americium_Curium_Foundation`
- **C1 공정 가스 (수소 다음):** `Hydrogen_Foundation` → `Syngas_Water_Gas_Shift_Foundation` → `Methanol_Synthesis_Foundation` / `Fischer_Tropsch_Liquids_Foundation` (평형·열적분은 `Chemical_Reaction_Foundation` 전제)
- **질 비료·산화 질소:** `Nitrogen_Foundation` (N₂·Haber 개요) → `Ammonia_Process_Integration_Foundation` (NH₃ 플랜트·H₂ 결합) → `Urea_CO2_Loop_Foundation` (NH₃+CO₂) / `Nitric_Ammonium_Foundation` (HNO₃·AN)
- **N-P·칼리 염:** `Phosphorus_Foundation` → `Ammonium_Phosphate_Foundation` (MAP/DAP); `Potassium_Foundation` → `Potassium_Chloride_Brine_Foundation` (MOP·브라인)
- **혼합비료·수계:** `Urea_CO2_Loop_Foundation` · `Ammonium_Phosphate_Foundation` · `Potassium_Chloride_Brine_Foundation` → `NPK_Blend_Eutrophication_Foundation` (도편·유출·부영양화)
- **해수·비턴·MgCl₂:** `Potassium_Chloride_Brine_Foundation` → `Seawater_Bittern_MgCl2_Foundation` (담수화 농축액·배출·부식·에너지)
- **규산염 비료:** `Silicon_Foundation`(소재 규소와 개념 분리) → `Silicate_Fertilizer_Foundation` (풍화 동역학·용해성 인산과 혼동 금지)
- **유기·미생물:** `NPK_Blend_Eutrophication_Foundation` → `Organic_Matter_Microbial_Fertilizer_Foundation` (C:N·무기화 지연·병원체·염)
- **탄소 원소:** `Carbon_Foundation` (동소체·CO₂ 혼동) → `Carbon_Composite_Stack` · C1 환원 명시 시 `Syngas_Water_Gas_Shift_Foundation` 계열
- **포토·CMP:** `Silicon_Foundation` → `Photolithography_CMP_Foundation` (소모품·EHS; `Foundry_Implementation_Engine` 과 비목표 분리)

---

## 엔진 인덱스

| # | 엔진 | 역할 | 허브 내 성격 | 정본 위치 | 버전 |
|---|------|------|-----------|------|
| 1 | **Chemical_Reaction_Foundation** | 반응 동역학 기초: 종, 열역학, 동역학, 평형, 전기화학, ATHENA 스크리닝 | **기초 root** | `_staging/` | v0.1.0 |
| 2 | **Element_Capture_Foundation** | 원소 포집: CO₂·H₂·He·O₂·N₂ 대기/용해/전기분해/극저온 분리, TerraCore 브리지 | **자원 회수 응용** | `_staging/` | ✅ |
| 3 | **Hydrogen_Foundation** | 수소 전체: 생산, 저장, 연료전지, 안전, 우주/그리드/수송, ATHENA 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 4 | **Helium_Foundation** | 헬륨: 천연가스 조달, 액체 He 끓어오름, 질식·저온, 무한 자원 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 5 | **Lithium_Foundation** | 리튬: brine/hard-rock 추출, LFP/NMC 결합, 열화·재활용 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 6 | **Nitrogen_Foundation** | 질소: 극저온 ASU, Haber 평형 카툰, LN₂, 무상 비료 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 7 | **Oxygen_Foundation** | 산소: ASU, LOX, 전기분해 O₂–H₂ 화학양론, 산화제·MOXIE 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 8 | **Carbon_Composite_Stack** | 탄소 복합재: 경화 동역학(Arrhenius), 비강도, 재활용, Type IV 수소 탱크 | **재료 응용** | `_staging/` | ✅ |
| 9 | **Battery_Dynamics_Engine** | 배터리 전기화학: Nernst OCV, 내부 저항(Arrhenius), SOC/SOH, 열관리, 팩 설계 | **전기화학 응용** | `_staging/` 및 `2_operational/60_APPLIED_LAYER/` | ✅ |
| 10 | **Cooking_Process_Foundation** | 요리 화학: Maillard 반응 동역학, 열전달, 수분 활성도, 식품 안전 온도, 상업화 분석 | **공정/생활 화학 응용** | `_staging/` | ✅ |
| 11 | **Phosphorus_Foundation** | 인: 인광석 추출, ATP 재생 루프, 비료(N-P-K) 결합, 오염/고갈 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 12 | **Silicon_Foundation** | 규소: Siemens 정제, PV/로직 결함·열예산·수율, 무한효율 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 13 | **Iron_Foundation** | 철: blast furnace/DRI-EAF 경로, 부식 현실, 저탄소 제강 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 14 | **Sodium_Chlorine_Foundation** | Na/Cl: 염분 부식, chlor-alkali(Cl₂/NaOH/H₂), 전력 의존성 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 15 | **Magnesium_Calcium_Foundation** | Mg/Ca: 전해질 항상성(생체) + 경량합금 부식(재료) 결합 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 16 | **Aluminum_Titanium_Foundation** | Al/Ti: 구조재 트레이드오프, 갈바닉 부식, 공정 에너지 한계 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 17 | **Copper_Zinc_Foundation** | Cu/Zn: 전도도-가공성-부식 균형, 황동(Brass) 현실성 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 18 | **Potassium_Foundation** | 칼륨: 고/저칼륨혈증 리스크, 포타시 비료 유실/관리 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 19 | **Manganese_Cobalt_Nickel_Foundation** | MCN: Ni/Co/Mn 비율에 따른 에너지-수명-안전-공급망 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 20 | **Sulfur_Foundation** | 황: SOx 제어가 필요한 황산 공정 + Li-S 배터리 셔틀효과 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 21 | **Chromium_Nickel_Stainless_Foundation** | Cr/Ni: 스테인리스 수동피막, chloride 피팅, Ni 공급망/비용 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 22 | **Fluorine_Foundation** | F: LiPF6 계열 성능 이점 vs HF 생성/환경 지속성 리스크 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 23 | **Boron_Foundation** | B: 유리 열충격 저감, 복합재 강성-취성 트레이드오프, 도핑 과장 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 24 | **Vanadium_Foundation** | V: VRFB 저장(장주기) + 합금 미세강화, 전해질 유지보수 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 25 | **Molybdenum_Foundation** | Mo: 고온 크리프 내성 강화 + 촉매 중독/내구성 제약 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 26 | **Tungsten_Foundation** | W: 초고온/경도 장점과 산화·취성 트레이드오프 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 27 | **Silver_Gold_Foundation** | Ag/Au: 전도·접점 안정성과 비용/이행(migration) 리스크 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 28 | **Platinum_Group_Foundation** | Pt/Pd/Rh: 촉매 활성 이점과 중독/공급 집중 리스크 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 29 | **Rare_Earth_Magnet_Foundation** | Nd/Dy: 자석 성능, 열탈자, 희토류 공급·재활용 임계성 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 30 | **Gallium_Germanium_Foundation** | Ga/Ge: 전력·RF·광전자 성능 이점 vs 열관리·by-product 공급 리스크 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 31 | **Niobium_Tantalum_Foundation** | Nb/Ta: 고온합금·커패시터 밀도 이점 vs 공급 집중·고장모드 제약 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 32 | **Zirconium_Hafnium_Foundation** | Zr/Hf: 핵급 순도 분리와 고온세라믹 성능의 공정 난이도 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 33 | **Ceria_Lanthanum_Foundation** | Ce/La: 산소저장 촉매 성능과 슬러리/폐기물 처리 제약 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 34 | **Cobalt_Manganese_Spinel_Foundation** | Co-Mn spinel: 성능 이점과 열안전/코발트 공급 제약 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 35 | **Uranium_Thorium_Foundation** | U/Th: 연료주기·폐기물·안전거버넌스 불가피성 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 36 | **Tin_Lead_Foundation** | Sn/Pb: 납땜 신뢰성·RoHS·납 독성·무연 주석 수염 리스크 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 37 | **Plutonium_Foundation** | Pu: 임계성 공학·안전보장·분리·폐기물 부담 스크리닝 (허가/설계 대체 아님) | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 38 | **Rare_Gas_Extended_Foundation** | Ne/Ar/Kr/Xe: ASU 꼬리경제·극저온 비용·Xe 수요 스파이크 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 39 | **Beryllium_Foundation** | Be: 비중 대비 강성 이점 vs 분진·흡입 독성(베릴리움증)·가공 통제 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 40 | **Cadmium_Mercury_Foundation** | Cd/Hg: 노출·생물농축·수은 증기·RoHS/폐기물 규제 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 41 | **Arsenic_Antimony_Bismuth_Foundation** | As/Sb/Bi: 응용 분리·독성 계급 혼동·비소 환경이동 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 42 | **Scandium_Yttrium_Foundation** | Sc/Y: Al-Sc·YSZ 기능 소재 vs 부산물 공급·분리 꼬리비용 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 43 | **Lanthanum_Cerium_Praseodymium_Foundation** | La/Ce/Pr: 다단 분리·공동생산 vs 단일공정 순도/제로에너지 주장 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 44 | **Iodine_Bromine_Foundation** | I/Br: 공급 원천·변동 vs 할로겐 상호대체·부식·독성 부정 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 45 | **Rubidium_Cesium_Foundation** | Rb/Cs: 중알칼리 반응성·발화·수반응 vs Na/K 동급 취급 주장 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 46 | **Strontium_Barium_Foundation** | Sr/Ba: 용액성 바륨 vs BaSO4 화종 혼동·Sr 공정/방사 맥락 분리 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 47 | **Selenium_Tellurium_Foundation** | Se/Te: S와 동일 위험 프레임 부정·Te 부산물·박막 PV 인접 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 48 | **Rhenium_Foundation** | Re: Mo/W 이후 초합금·개질 촉매 vs 희소·Mo 대체 착각 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 49 | **Ruthenium_Iridium_Osmium_Foundation** | Ru/Ir/Os: PGM 확장·박막 전극 vs Os 화학 독성·PGM 무한 공급 주장 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 50 | **Indium_Thallium_Foundation** | In/Tl: Ga/Ge 이후 디스플레이·박막 vs In=Tl 안전 혼동·인듐 무한 부산물 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 51 | **Radon_Foundation** | Rn: 희가스+α선량 vs Ne/Ar류 무해 혼동·지질·U/Th 붕괴 연쇄 부정 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 52 | **Technetium_Promethium_Foundation** | Tc/Pm: 천연 대량·Pm 안정 재고 착각·의료/분열 꼬리 공급 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 53 | **Americium_Curium_Foundation** | Am/Cm: 무규제 취급·무한 소비재 Am 착각 vs α원·허가·규모 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 54 | **Syngas_Water_Gas_Shift_Foundation** | Syngas·WGS: CO 독성·N₂ 혼동 방지·shift 무손실 주장 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 55 | **Methanol_Synthesis_Foundation** | 메탄올: 단일패스 완전전환·촉매 무열화 주장 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 56 | **Fischer_Tropsch_Liquids_Foundation** | FT: 디젤 단일생산·FT 무CO₂ 부산물 주장 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 57 | **Ammonia_Process_Integration_Foundation** | NH₃: 무에너지 Haber·H₂ 무관 착각 vs 플랜트·촉매·H₂ 결합 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 58 | **Urea_CO2_Loop_Foundation** | 요소: 무상 CO₂·무스트리퍼 스팀 착각 vs 순도·포집 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 59 | **Nitric_Ammonium_Foundation** | 질산·AN: 요소와 동급 안전·NOx 무비용 착각 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 60 | **Ammonium_Phosphate_Foundation** | MAP/DAP: 무차별 교체·무습도 케이킹 착각 vs N/P·저장 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 61 | **Potassium_Chloride_Brine_Foundation** | MOP: 해수 KCl 무에너지·무불순물 착각 vs 채광·Cd 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 62 | **NPK_Blend_Eutrophication_Foundation** | NPK: 비료=부영양 무관·완전 균질 혼합 착각 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 63 | **Seawater_Bittern_MgCl2_Foundation** | 해수·비턴·MgCl₂: 무에너지 농축·순수 Mg 착각 vs 배출·부식 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 64 | **Silicate_Fertilizer_Foundation** | 규산염 비료: 용해성 인산 동급·즉시 Si 흡수 과장 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 65 | **Organic_Matter_Microbial_Fertilizer_Foundation** | 유기·미생물: 무조건 안전·즉시 무기화 N 착각 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 66 | **Carbon_Foundation** | 탄소: CO₂=원소탄소·무한 흑연 착각 vs 동소체·순환 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |
| 67 | **Photolithography_CMP_Foundation** | 포토·CMP: 무EHS·무폐액 착각 vs 소모품; EDA 대체 아님 스크리닝 | **도메인 foundation** | `3_meterial/` (정본) | v0.1.0 |

---

## 화학 레이어 연결 흐름

```
Chemical_Reaction_Foundation  (반응의 "왜"와 "얼마나" — 모든 화학 엔진의 뿌리)
    │
    ├── ΔG = ΔH − TΔS              → 반응 가능성 판정
    ├── k = A·exp(−Ea/RT)           → 반응 속도 (Arrhenius)
    ├── K_eq = exp(−ΔG°/RT)         → 평형 위치
    └── E = E° − (RT/nF)·ln Q      → 전기화학 전위 (Nernst)
         │
         ├──→ Element_Capture          Nernst로 분리 전위 결정
         │    └── H₂, O₂, CO₂, He, N₂ 포집 경로
         │
         ├──→ Hydrogen_Foundation      전기분해 전압, 연료전지 OCV, SMR 평형
         │    ├── 생산: V_cell = E_rev + η_act + j·R_ohm
         │    ├── 저장: ṁ_boiloff = Q_leak / L_vap
         │    └── 연료전지: E = E°(T) + (RT/2F)·ln(...)
         │
         ├──→ Syngas_Water_Gas_Shift_Foundation  개질·WGS·H2/CO·CO 안전
         │
         ├──→ Methanol_Synthesis_Foundation  평형·루프·촉매
         │
         ├──→ Fischer_Tropsch_Liquids_Foundation  ASF·경가스·열적분
         │
         ├──→ Helium_Foundation        천연가스 조달, He 끓어오름, MRI/융합 맥락
         │
         ├──→ Lithium_Foundation       Li 추출, LFP/NMC 성능-수명-안전 삼각, 재활용 필요성
         │
         ├──→ Phosphorus_Foundation    인광석, ATP 재생 루프, N-P-K 연계
         │
         ├──→ Ammonium_Phosphate_Foundation  MAP/DAP N-P·습기
         │
         ├──→ Silicon_Foundation       반도체/PV 물질 코어, 결함-수율-열예산 제약
         │
         ├──→ Photolithography_CMP_Foundation  포토·CMP 소모품·EHS
         │
         ├──→ Silicate_Fertilizer_Foundation  토양 규산염·풍화 동역학
         │
         ├──→ Iron_Foundation          구조재/제강 경로, 부식 수명 비용, 탄소집약도
         │
         ├──→ Sodium_Chlorine_Foundation  염분 부식 + chlor-alkali 공정(Cl₂/NaOH/H₂)
         │
         ├──→ Magnesium_Calcium_Foundation  전해질(Ca/Mg) 항상성 + Mg합금 부식
         │
         ├──→ Aluminum_Titanium_Foundation  구조재 Al/Ti 선택, 갈바닉 인터페이스
         │
         ├──→ Copper_Zinc_Foundation  도체/접점 소재 Cu-Zn 트레이드오프
         │
         ├──→ Potassium_Foundation    K+ 전해질 안정성과 비료 흐름 제약
         │
         ├──→ Potassium_Chloride_Brine_Foundation  MOP·브라인·매장지
         │
         ├──→ Seawater_Bittern_MgCl2_Foundation  비턴·MgCl₂·담수화 꼬리
         │
         ├──→ Manganese_Cobalt_Nickel_Foundation  NMC cathode 비율(에너지-수명-안전)
         │
         ├──→ Sulfur_Foundation       황산 공정 환경 제약 + Li-S 셔틀 효과
         │
         ├──→ Chromium_Nickel_Stainless_Foundation  Cr 수동피막 + Ni 안정성 + 피팅 위험
         │
         ├──→ Fluorine_Foundation     전해질 성능 개선 vs HF/지속성 제약
         │
         ├──→ Boron_Foundation        보로실리케이트 열충격 개선 + 복합재 취성 제약
         │
         ├──→ Carbon_Foundation       동소체·CO₂ vs C·흑연 서사
         │
         ├──→ Vanadium_Foundation     VRFB 장주기 저장 + V 미세합금 강화
         │
         ├──→ Molybdenum_Foundation   고온합금 크리프 안정 + 촉매 중독 내구성
         │
         ├──→ Tungsten_Foundation     초고온/초경도 적용 + 산화/취성 관리
         │
         ├──→ Rhenium_Foundation      Mo/W 다음 6족: 초합금·촉매·희소
         │
         ├──→ Silver_Gold_Foundation  고신뢰 접점/배선 성능 vs 비용·이행 위험
         │
         ├──→ Platinum_Group_Foundation  촉매 성능 vs 중독/공급 임계성
         │
         ├──→ Ruthenium_Iridium_Osmium_Foundation  Ru/Ir/Os 전기촉매·Os 위험
         │
         ├──→ Rare_Earth_Magnet_Foundation  고자속 모터 성능 vs 열탈자/희토류 병목
         │
         ├──→ Gallium_Germanium_Foundation  전력/RF/광전자 성능 vs 열·공급 제약
         │
         ├──→ Indium_Thallium_Foundation  ITO·CIGS vs Tl 독성 혼동 방지
         │
         ├──→ Niobium_Tantalum_Foundation   고온합금/커패시터 밀도 vs 공급·신뢰성 제약
         │
         ├──→ Zirconium_Hafnium_Foundation  Zr/Hf 분리 난이도 + 핵/고온세라믹 공정성
         │
         ├──→ Ceria_Lanthanum_Foundation  산소저장 촉매 + 공정 폐기물 처리
         │
         ├──→ Cobalt_Manganese_Spinel_Foundation  스피넬 안정성과 코발트 공급 리스크
         │
         ├──→ Uranium_Thorium_Foundation  핵연료주기·폐기물·거버넌스 제약
         │
         ├──→ Tin_Lead_Foundation  납땜·RoHS·납 독성·무연 주석 수염
         │
         ├──→ Plutonium_Foundation  Pu 임계성·안전보장·분리·폐기물 (서술/스크리닝)
         │
         ├──→ Americium_Curium_Foundation  Am/Cm 밀봉 α·RTG·거버넌스
         │
         ├──→ Rare_Gas_Extended_Foundation  Ne/Ar/Kr/Xe ASU·극저온·Xe 추진/조명 수요
         │
         ├──→ Radon_Foundation  Rn 실내·붕괴 연쇄·선량
         │
         ├──→ Beryllium_Foundation  경량 강성 vs 분진·베릴리움증·가공
         │
         ├──→ Cadmium_Mercury_Foundation  중금속 노출·증기·규제
         │
         ├──→ Arsenic_Antimony_Bismuth_Foundation  준금속 독성·환경이동·응용 분리
         │
         ├──→ Scandium_Yttrium_Foundation  미세합금·YSZ·RE 부산물·분리
         │
         ├──→ Lanthanum_Cerium_Praseodymium_Foundation  경량 란타너드 분리 연쇄
         │
         ├──→ Technetium_Promethium_Foundation  Tc/Pm 합성·비안정·의료/분열 꼬리
         │
         ├──→ Iodine_Bromine_Foundation  I/Br 공급·할로겐 위험 혼동 방지
         │
         ├──→ Rubidium_Cesium_Foundation  K 다음 1족: 반응성·발화·저장
         │
         ├──→ Strontium_Barium_Foundation  Mg/Ca 다음 2족: 화종·유체
         │
         ├──→ Selenium_Tellurium_Foundation  S 다음 16족: PV·Te 부산물
         │
         ├──→ Nitrogen_Foundation      ASU N₂, Haber(N₂+3H₂⇌2NH₃) 카툰, LN₂
         │
         ├──→ Ammonia_Process_Integration_Foundation  NH₃ 플랜트·H₂·에너지
         │
         ├──→ Urea_CO2_Loop_Foundation  NH₃+CO₂·스트리퍼·CO₂
         │
         ├──→ Nitric_Ammonium_Foundation  Ostwald·NOx·AN 위험
         │
         ├──→ NPK_Blend_Eutrophication_Foundation  혼합·유출·수계
         │
         ├──→ Organic_Matter_Microbial_Fertilizer_Foundation  C:N·무기화·병원체
         │
         ├──→ Oxygen_Foundation        ASU O₂, LOX, ṅ_O₂ = ½ ṅ_H₂ (전기분해)
         │
         ├──→ Carbon_Composite         Arrhenius로 수지 경화 속도
         │    └── Type IV 수소 탱크 CFRP 설계
         │
         ├──→ Battery_Dynamics         Nernst OCV, Arrhenius 내부 저항
         │    └── SEI 성장 = 부반응 (side-reaction)
         │
         └──→ Cooking_Process          Maillard = Arrhenius 동역학
              └── 열전달, 수분 활성도, 식품 안전 온도
```

같은 흐름을 계층으로 읽으면 이렇게 볼 수 있다.

```text
Chemical_Reaction_Foundation
  -> Hydrogen_Foundation
  -> Syngas_Water_Gas_Shift_Foundation
  -> Methanol_Synthesis_Foundation
  -> Fischer_Tropsch_Liquids_Foundation
  -> Helium_Foundation
  -> Lithium_Foundation
  -> Phosphorus_Foundation
  -> Ammonium_Phosphate_Foundation
  -> Silicon_Foundation
  -> Photolithography_CMP_Foundation
  -> Silicate_Fertilizer_Foundation
  -> Iron_Foundation
  -> Sodium_Chlorine_Foundation
  -> Magnesium_Calcium_Foundation
  -> Aluminum_Titanium_Foundation
  -> Copper_Zinc_Foundation
  -> Potassium_Foundation
  -> Potassium_Chloride_Brine_Foundation
  -> Seawater_Bittern_MgCl2_Foundation
  -> Manganese_Cobalt_Nickel_Foundation
  -> Sulfur_Foundation
  -> Chromium_Nickel_Stainless_Foundation
  -> Fluorine_Foundation
  -> Boron_Foundation
  -> Carbon_Foundation
  -> Vanadium_Foundation
  -> Molybdenum_Foundation
  -> Tungsten_Foundation
  -> Rhenium_Foundation
  -> Silver_Gold_Foundation
  -> Platinum_Group_Foundation
  -> Ruthenium_Iridium_Osmium_Foundation
  -> Rare_Earth_Magnet_Foundation
  -> Gallium_Germanium_Foundation
  -> Indium_Thallium_Foundation
  -> Niobium_Tantalum_Foundation
  -> Zirconium_Hafnium_Foundation
  -> Ceria_Lanthanum_Foundation
  -> Cobalt_Manganese_Spinel_Foundation
  -> Uranium_Thorium_Foundation
  -> Tin_Lead_Foundation
  -> Plutonium_Foundation
  -> Americium_Curium_Foundation
  -> Rare_Gas_Extended_Foundation
  -> Radon_Foundation
  -> Beryllium_Foundation
  -> Cadmium_Mercury_Foundation
  -> Arsenic_Antimony_Bismuth_Foundation
  -> Scandium_Yttrium_Foundation
  -> Lanthanum_Cerium_Praseodymium_Foundation
  -> Technetium_Promethium_Foundation
  -> Iodine_Bromine_Foundation
  -> Rubidium_Cesium_Foundation
  -> Strontium_Barium_Foundation
  -> Selenium_Tellurium_Foundation
  -> Nitrogen_Foundation
  -> Ammonia_Process_Integration_Foundation
  -> Urea_CO2_Loop_Foundation
  -> Nitric_Ammonium_Foundation
  -> NPK_Blend_Eutrophication_Foundation
  -> Organic_Matter_Microbial_Fertilizer_Foundation
  -> Oxygen_Foundation
  -> Element_Capture_Foundation
  -> Battery_Dynamics_Engine
  -> Carbon_Composite_Stack
  -> Cooking_Process_Foundation
```

즉 `Chemical_Reaction_Foundation` 이 화학의 “왜/얼마나”를 잡고,
나머지 엔진들은 그 원리가 자원, 전기화학, 재료, 공정으로 흘러가는 **응용 가지**들이다.

이 흐름을 통제하는 문서:

- [ELEMENT_REGISTRY.md](/Users/jazzin/Desktop/00_BRAIN/02_SYSTEMS/ENGINE_HUB/3_meterial/ELEMENT_REGISTRY.md)
- [ELEMENT_FOUNDATION_TEMPLATE.md](/Users/jazzin/Desktop/00_BRAIN/02_SYSTEMS/ENGINE_HUB/3_meterial/ELEMENT_FOUNDATION_TEMPLATE.md)
- [CHEMICAL_GOVERNANCE.md](/Users/jazzin/Desktop/00_BRAIN/02_SYSTEMS/ENGINE_HUB/3_meterial/CHEMICAL_GOVERNANCE.md)
- [FOLDER_STRUCTURE.md](/Users/jazzin/Desktop/00_BRAIN/02_SYSTEMS/ENGINE_HUB/3_meterial/FOLDER_STRUCTURE.md)
- [CHEMICAL_HYGIENE_STATUS.md](/Users/jazzin/Desktop/00_BRAIN/02_SYSTEMS/ENGINE_HUB/3_meterial/CHEMICAL_HYGIENE_STATUS.md)

---

## 정본과 복사본 원칙

현재 `3_meterial` 안 엔진들은 두 부류로 나뉜다.

- **정본이 다른 위치에 있는 복사본**
  - 예: `Battery_Dynamics_Engine`, `Element_Capture_Foundation`, `Carbon_Composite_Stack`, `Cooking_Process_Foundation`, `Chemical_Reaction_Foundation`
- **현재 이 폴더를 정본으로 삼는 엔진**
  - 예: `Hydrogen_Foundation`, `Syngas_Water_Gas_Shift_Foundation`, `Methanol_Synthesis_Foundation`, `Fischer_Tropsch_Liquids_Foundation`, `Helium_Foundation`, `Lithium_Foundation`, `Carbon_Foundation`, `Phosphorus_Foundation`, `Ammonium_Phosphate_Foundation`, `Silicon_Foundation`, `Photolithography_CMP_Foundation`, `Silicate_Fertilizer_Foundation`, `Nitrogen_Foundation`, `Ammonia_Process_Integration_Foundation`, `Urea_CO2_Loop_Foundation`, `Nitric_Ammonium_Foundation`, `NPK_Blend_Eutrophication_Foundation`, `Organic_Matter_Microbial_Fertilizer_Foundation`, `Potassium_Foundation`, `Potassium_Chloride_Brine_Foundation`, `Seawater_Bittern_MgCl2_Foundation`, `Oxygen_Foundation`

따라서 유지 원칙은 다음과 같다.

1. 기능 수정은 **정본 위치**에서 먼저 한다.
2. `3_meterial` 은 화학 연결 흐름을 보기 위한 **index/graft hub** 로 유지한다.
3. 장기적으로는 복사본보다 `manifest`, `symlink`, `SOURCE_OF_TRUTH` 안내가 더 바람직하다.

이 원칙을 지키지 않으면, 화학 축은 좋아 보여도 실제 구현은 빠르게 드리프트한다.

---

## VectorSpace 연결

`VectorSpace_102`의 `axis_registry.py`에 각 엔진의 Ω 축이 정의되면,
이 폴더의 엔진들은 `from_chemical_assessment` 어댑터를 통해
`GlobalSystemVectorV0`에 통합된다.

---

## 외부 연결 (다른 허브의 엔진)

| 엔진 | 화학 연결 | 위치 |
|------|-----------|------|
| `TerraCore_Stack` | 전기분해, Sabatier CO₂ 환원, 가스 순환 | `40_SPATIAL_LAYER/` |
| `FusionCore_Stack` | D-T 핵반응, 삼중수소 화학 | `40_SPATIAL_LAYER/` |
| `Antimatter_Foundation` | 쌍소멸 에너지학 (개념적 연결) | `50_DIAGNOSTIC_LAYER/` |
| `Token_Dynamics_Foundation` | 에너지 토큰 아날로지 | `_staging/` |
| `Higgs_Phenomenology_Foundation` | 질량 생성 (개념적 아날로지) | `_staging/` |

---

## 다음으로 좋은 확장

1. 새 원소 추가 전 [ELEMENT_REGISTRY.md](/Users/jazzin/Desktop/00_BRAIN/02_SYSTEMS/ENGINE_HUB/3_meterial/ELEMENT_REGISTRY.md) 먼저 갱신
2. 새 원소 foundation은 [ELEMENT_FOUNDATION_TEMPLATE.md](/Users/jazzin/Desktop/00_BRAIN/02_SYSTEMS/ENGINE_HUB/3_meterial/ELEMENT_FOUNDATION_TEMPLATE.md) 기준으로 scaffold 생성
3. 운영 규칙은 [CHEMICAL_GOVERNANCE.md](/Users/jazzin/Desktop/00_BRAIN/02_SYSTEMS/ENGINE_HUB/3_meterial/CHEMICAL_GOVERNANCE.md) 에 고정
4. 장기적으로 `Chemical_Reaction_Foundation -> element foundations -> applied chemistry engines` 브리지 계약 명시

---

*ENGINE_HUB/3_meterial — 메테리얼 레이어 허브. 반응·원소(H, He, N, O, …)·재료·배터리·요리를 하나의 흐름으로.*

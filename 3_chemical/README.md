# 3_chemical — 화학 레이어

> **인식론적 위치:** E5 Chemistry — [EPISTEMIC_LAYER_MAP.md](../../../EPISTEMIC_LAYER_MAP.md)

`0_observers`(물리 관측) · `1_calculator`(수학 계산) · `2_operational`(운영 레이어)과 같은 레벨의 **화학 전용 허브**.

> **중요:** 이 폴더는 우선 **chemistry connection hub / index hub** 로 읽는 것이 맞다.  
> 여기 있는 엔진 중 일부는 `_staging` 또는 `2_operational/*` 쪽에 이미 정본이 있고,  
> `3_chemical` 은 그 정본들을 **화학 축 관점에서 다시 묶어 보는 연결 허브**다.

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
3_chemical/    ← ★ 화학 레이어 (반응, 원소, 재료, 수소, 배터리, 요리)
```

---

## 폴더 구조

> **물리 배치와 개념 배치는 다르다.**
> 현재 실제 폴더는 호환성과 기존 링크 유지를 위해 **flat layout** 으로 둔다.
> 대신 읽는 방식은 아래의 **chemical root -> element foundations -> applied engines** 순서를 따른다.

```
3_chemical/
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
├── Helium_Foundation/               ← Z=2 헬륨 (조달, 극저온, 희소성, 스크리닝)
├── Lithium_Foundation/              ← Z=3 리튬 (추출, 배터리 결합, 열안전, 재활용 스크리닝)
├── Phosphorus_Foundation/           ← Z=15 인 (인광석, ATP 루프, N-P-K, 스크리닝)
├── Silicon_Foundation/              ← Z=14 규소 (정제, 결함/수율, 열예산, 스크리닝)
├── Iron_Foundation/                 ← Z=26 철 (제강 경로, 부식, 탄소집약도 스크리닝)
├── Sodium_Chlorine_Foundation/      ← Z=11/17 Na/Cl (염분부식, chlor-alkali, 안전)
├── Magnesium_Calcium_Foundation/    ← Z=12/20 Mg/Ca (전해질 항상성 + 경량합금 부식)
├── Aluminum_Titanium_Foundation/    ← Z=13/22 Al/Ti (구조재 선택 + 갈바닉 + 공정에너지)
├── Copper_Zinc_Foundation/          ← Z=29/30 Cu/Zn (전도도-가공성-부식 트레이드오프)
├── Potassium_Foundation/            ← Z=19 칼륨 (전해질 안전 + 포타시 비료 제약)
├── Manganese_Cobalt_Nickel_Foundation/ ← Z=25/27/28 MCN (NMC cathode 비율 트레이드오프)
├── Sulfur_Foundation/               ← Z=16 황 (황산 공정 + Li-S 셔틀 효과 제약)
├── Chromium_Nickel_Stainless_Foundation/ ← Z=24/28 Cr/Ni (스테인리스 수동피막 + 피팅)
├── Fluorine_Foundation/             ← Z=9 F (전해질 성능 vs HF/지속성 리스크)
├── Boron_Foundation/                ← Z=5 B (보로실리케이트/복합재/도핑 제약)
├── Vanadium_Foundation/             ← Z=23 V (VRFB 레독스 저장 + 미세합금)
├── Molybdenum_Foundation/           ← Z=42 Mo (고온합금 + 촉매 내구/중독 제약)
├── Tungsten_Foundation/             ← Z=74 W (초고온/초경도 + 산화/취성 제약)
├── Silver_Gold_Foundation/          ← Z=47/79 Ag/Au (전도·접점 안정성 vs 비용)
├── Platinum_Group_Foundation/       ← Pt/Pd/Rh (촉매 활성 vs 중독/공급 임계성)
├── Rare_Earth_Magnet_Foundation/    ← Nd/Dy (자속 밀도 vs 열탈자/공급 집중)
├── Nitrogen_Foundation/             ← Z=7 질소 (공기분리, Haber 카툰, LN₂, 스크리닝)
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

`3_chemical` 은 다음 세 질문에 답하기 위한 보기 창이다.

1. 화학의 **기초 원리**는 어디에 있는가?
2. 그 원리가 어떤 **응용 화학 엔진**으로 내려가는가?
3. 공학(E4)과 생물(E6) 사이에서 화학이 **무슨 연결 축**을 담당하는가?

그래서 여기서는 “정본이 어디 있나?”보다 먼저,
**“화학 흐름이 어디서 시작해 어디로 내려가는가?”** 를 읽는 것이 중요하다.

---

## 엔진 인덱스

| # | 엔진 | 역할 | 허브 내 성격 | 정본 위치 | 버전 |
|---|------|------|-----------|------|
| 1 | **Chemical_Reaction_Foundation** | 반응 동역학 기초: 종, 열역학, 동역학, 평형, 전기화학, ATHENA 스크리닝 | **기초 root** | `_staging/` | v0.1.0 |
| 2 | **Element_Capture_Foundation** | 원소 포집: CO₂·H₂·He·O₂·N₂ 대기/용해/전기분해/극저온 분리, TerraCore 브리지 | **자원 회수 응용** | `_staging/` | ✅ |
| 3 | **Hydrogen_Foundation** | 수소 전체: 생산, 저장, 연료전지, 안전, 우주/그리드/수송, ATHENA 스크리닝 | **도메인 foundation** | `3_chemical/` (정본) | v0.1.0 |
| 4 | **Helium_Foundation** | 헬륨: 천연가스 조달, 액체 He 끓어오름, 질식·저온, 무한 자원 스크리닝 | **도메인 foundation** | `3_chemical/` (정본) | v0.1.0 |
| 5 | **Lithium_Foundation** | 리튬: brine/hard-rock 추출, LFP/NMC 결합, 열화·재활용 스크리닝 | **도메인 foundation** | `3_chemical/` (정본) | v0.1.0 |
| 6 | **Nitrogen_Foundation** | 질소: 극저온 ASU, Haber 평형 카툰, LN₂, 무상 비료 스크리닝 | **도메인 foundation** | `3_chemical/` (정본) | v0.1.0 |
| 7 | **Oxygen_Foundation** | 산소: ASU, LOX, 전기분해 O₂–H₂ 화학양론, 산화제·MOXIE 스크리닝 | **도메인 foundation** | `3_chemical/` (정본) | v0.1.0 |
| 8 | **Carbon_Composite_Stack** | 탄소 복합재: 경화 동역학(Arrhenius), 비강도, 재활용, Type IV 수소 탱크 | **재료 응용** | `_staging/` | ✅ |
| 9 | **Battery_Dynamics_Engine** | 배터리 전기화학: Nernst OCV, 내부 저항(Arrhenius), SOC/SOH, 열관리, 팩 설계 | **전기화학 응용** | `_staging/` 및 `2_operational/60_APPLIED_LAYER/` | ✅ |
| 10 | **Cooking_Process_Foundation** | 요리 화학: Maillard 반응 동역학, 열전달, 수분 활성도, 식품 안전 온도, 상업화 분석 | **공정/생활 화학 응용** | `_staging/` | ✅ |
| 11 | **Phosphorus_Foundation** | 인: 인광석 추출, ATP 재생 루프, 비료(N-P-K) 결합, 오염/고갈 스크리닝 | **도메인 foundation** | `3_chemical/` (정본) | v0.1.0 |
| 12 | **Silicon_Foundation** | 규소: Siemens 정제, PV/로직 결함·열예산·수율, 무한효율 스크리닝 | **도메인 foundation** | `3_chemical/` (정본) | v0.1.0 |
| 13 | **Iron_Foundation** | 철: blast furnace/DRI-EAF 경로, 부식 현실, 저탄소 제강 스크리닝 | **도메인 foundation** | `3_chemical/` (정본) | v0.1.0 |
| 14 | **Sodium_Chlorine_Foundation** | Na/Cl: 염분 부식, chlor-alkali(Cl₂/NaOH/H₂), 전력 의존성 스크리닝 | **도메인 foundation** | `3_chemical/` (정본) | v0.1.0 |
| 15 | **Magnesium_Calcium_Foundation** | Mg/Ca: 전해질 항상성(생체) + 경량합금 부식(재료) 결합 스크리닝 | **도메인 foundation** | `3_chemical/` (정본) | v0.1.0 |
| 16 | **Aluminum_Titanium_Foundation** | Al/Ti: 구조재 트레이드오프, 갈바닉 부식, 공정 에너지 한계 스크리닝 | **도메인 foundation** | `3_chemical/` (정본) | v0.1.0 |
| 17 | **Copper_Zinc_Foundation** | Cu/Zn: 전도도-가공성-부식 균형, 황동(Brass) 현실성 스크리닝 | **도메인 foundation** | `3_chemical/` (정본) | v0.1.0 |
| 18 | **Potassium_Foundation** | 칼륨: 고/저칼륨혈증 리스크, 포타시 비료 유실/관리 스크리닝 | **도메인 foundation** | `3_chemical/` (정본) | v0.1.0 |
| 19 | **Manganese_Cobalt_Nickel_Foundation** | MCN: Ni/Co/Mn 비율에 따른 에너지-수명-안전-공급망 스크리닝 | **도메인 foundation** | `3_chemical/` (정본) | v0.1.0 |
| 20 | **Sulfur_Foundation** | 황: SOx 제어가 필요한 황산 공정 + Li-S 배터리 셔틀효과 스크리닝 | **도메인 foundation** | `3_chemical/` (정본) | v0.1.0 |
| 21 | **Chromium_Nickel_Stainless_Foundation** | Cr/Ni: 스테인리스 수동피막, chloride 피팅, Ni 공급망/비용 스크리닝 | **도메인 foundation** | `3_chemical/` (정본) | v0.1.0 |
| 22 | **Fluorine_Foundation** | F: LiPF6 계열 성능 이점 vs HF 생성/환경 지속성 리스크 스크리닝 | **도메인 foundation** | `3_chemical/` (정본) | v0.1.0 |
| 23 | **Boron_Foundation** | B: 유리 열충격 저감, 복합재 강성-취성 트레이드오프, 도핑 과장 스크리닝 | **도메인 foundation** | `3_chemical/` (정본) | v0.1.0 |
| 24 | **Vanadium_Foundation** | V: VRFB 저장(장주기) + 합금 미세강화, 전해질 유지보수 스크리닝 | **도메인 foundation** | `3_chemical/` (정본) | v0.1.0 |
| 25 | **Molybdenum_Foundation** | Mo: 고온 크리프 내성 강화 + 촉매 중독/내구성 제약 스크리닝 | **도메인 foundation** | `3_chemical/` (정본) | v0.1.0 |
| 26 | **Tungsten_Foundation** | W: 초고온/경도 장점과 산화·취성 트레이드오프 스크리닝 | **도메인 foundation** | `3_chemical/` (정본) | v0.1.0 |
| 27 | **Silver_Gold_Foundation** | Ag/Au: 전도·접점 안정성과 비용/이행(migration) 리스크 스크리닝 | **도메인 foundation** | `3_chemical/` (정본) | v0.1.0 |
| 28 | **Platinum_Group_Foundation** | Pt/Pd/Rh: 촉매 활성 이점과 중독/공급 집중 리스크 스크리닝 | **도메인 foundation** | `3_chemical/` (정본) | v0.1.0 |
| 29 | **Rare_Earth_Magnet_Foundation** | Nd/Dy: 자석 성능, 열탈자, 희토류 공급·재활용 임계성 스크리닝 | **도메인 foundation** | `3_chemical/` (정본) | v0.1.0 |

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
         ├──→ Helium_Foundation        천연가스 조달, He 끓어오름, MRI/융합 맥락
         │
         ├──→ Lithium_Foundation       Li 추출, LFP/NMC 성능-수명-안전 삼각, 재활용 필요성
         │
         ├──→ Phosphorus_Foundation    인광석, ATP 재생 루프, N-P-K 연계
         │
         ├──→ Silicon_Foundation       반도체/PV 물질 코어, 결함-수율-열예산 제약
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
         ├──→ Vanadium_Foundation     VRFB 장주기 저장 + V 미세합금 강화
         │
         ├──→ Molybdenum_Foundation   고온합금 크리프 안정 + 촉매 중독 내구성
         │
         ├──→ Tungsten_Foundation     초고온/초경도 적용 + 산화/취성 관리
         │
         ├──→ Silver_Gold_Foundation  고신뢰 접점/배선 성능 vs 비용·이행 위험
         │
         ├──→ Platinum_Group_Foundation  촉매 성능 vs 중독/공급 임계성
         │
         ├──→ Rare_Earth_Magnet_Foundation  고자속 모터 성능 vs 열탈자/희토류 병목
         │
         ├──→ Nitrogen_Foundation      ASU N₂, Haber(N₂+3H₂⇌2NH₃) 카툰, LN₂
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
  -> Helium_Foundation
  -> Lithium_Foundation
  -> Phosphorus_Foundation
  -> Silicon_Foundation
  -> Iron_Foundation
  -> Sodium_Chlorine_Foundation
  -> Magnesium_Calcium_Foundation
  -> Aluminum_Titanium_Foundation
  -> Copper_Zinc_Foundation
  -> Potassium_Foundation
  -> Manganese_Cobalt_Nickel_Foundation
  -> Sulfur_Foundation
  -> Chromium_Nickel_Stainless_Foundation
  -> Fluorine_Foundation
  -> Boron_Foundation
  -> Vanadium_Foundation
  -> Molybdenum_Foundation
  -> Tungsten_Foundation
  -> Silver_Gold_Foundation
  -> Platinum_Group_Foundation
  -> Rare_Earth_Magnet_Foundation
  -> Nitrogen_Foundation
  -> Oxygen_Foundation
  -> Element_Capture_Foundation
  -> Battery_Dynamics_Engine
  -> Carbon_Composite_Stack
  -> Cooking_Process_Foundation
```

즉 `Chemical_Reaction_Foundation` 이 화학의 “왜/얼마나”를 잡고,
나머지 엔진들은 그 원리가 자원, 전기화학, 재료, 공정으로 흘러가는 **응용 가지**들이다.

이 흐름을 통제하는 문서:

- [ELEMENT_REGISTRY.md](/Users/jazzin/Desktop/00_BRAIN/02_SYSTEMS/ENGINE_HUB/3_chemical/ELEMENT_REGISTRY.md)
- [ELEMENT_FOUNDATION_TEMPLATE.md](/Users/jazzin/Desktop/00_BRAIN/02_SYSTEMS/ENGINE_HUB/3_chemical/ELEMENT_FOUNDATION_TEMPLATE.md)
- [CHEMICAL_GOVERNANCE.md](/Users/jazzin/Desktop/00_BRAIN/02_SYSTEMS/ENGINE_HUB/3_chemical/CHEMICAL_GOVERNANCE.md)
- [FOLDER_STRUCTURE.md](/Users/jazzin/Desktop/00_BRAIN/02_SYSTEMS/ENGINE_HUB/3_chemical/FOLDER_STRUCTURE.md)
- [CHEMICAL_HYGIENE_STATUS.md](/Users/jazzin/Desktop/00_BRAIN/02_SYSTEMS/ENGINE_HUB/3_chemical/CHEMICAL_HYGIENE_STATUS.md)

---

## 정본과 복사본 원칙

현재 `3_chemical` 안 엔진들은 두 부류로 나뉜다.

- **정본이 다른 위치에 있는 복사본**
  - 예: `Battery_Dynamics_Engine`, `Element_Capture_Foundation`, `Carbon_Composite_Stack`, `Cooking_Process_Foundation`, `Chemical_Reaction_Foundation`
- **현재 이 폴더를 정본으로 삼는 엔진**
  - 예: `Hydrogen_Foundation`, `Helium_Foundation`, `Lithium_Foundation`, `Phosphorus_Foundation`, `Silicon_Foundation`, `Nitrogen_Foundation`, `Oxygen_Foundation`

따라서 유지 원칙은 다음과 같다.

1. 기능 수정은 **정본 위치**에서 먼저 한다.
2. `3_chemical` 은 화학 연결 흐름을 보기 위한 **index/graft hub** 로 유지한다.
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

1. 새 원소 추가 전 [ELEMENT_REGISTRY.md](/Users/jazzin/Desktop/00_BRAIN/02_SYSTEMS/ENGINE_HUB/3_chemical/ELEMENT_REGISTRY.md) 먼저 갱신
2. 새 원소 foundation은 [ELEMENT_FOUNDATION_TEMPLATE.md](/Users/jazzin/Desktop/00_BRAIN/02_SYSTEMS/ENGINE_HUB/3_chemical/ELEMENT_FOUNDATION_TEMPLATE.md) 기준으로 scaffold 생성
3. 운영 규칙은 [CHEMICAL_GOVERNANCE.md](/Users/jazzin/Desktop/00_BRAIN/02_SYSTEMS/ENGINE_HUB/3_chemical/CHEMICAL_GOVERNANCE.md) 에 고정
4. 장기적으로 `Chemical_Reaction_Foundation -> element foundations -> applied chemistry engines` 브리지 계약 명시

---

*ENGINE_HUB/3_chemical — 화학 레이어 허브. 반응·원소(H, He, N, O, …)·재료·배터리·요리를 하나의 흐름으로.*

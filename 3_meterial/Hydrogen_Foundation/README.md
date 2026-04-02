> **한국어 (정본).** English: [README_EN.md](README_EN.md)

# Hydrogen_Foundation v0.1.0

**"수소란 무엇인가?"**

이 엔진은 수소에 관한 모든 것을 하나의 기초 레이어로 정리한다.
생산, 저장, 연료전지, 안전, 경제성, 스크리닝 — 각 층은
*수소가 왜 중요한지*, *어디서 막히는지*, *무엇이 과장인지*를
관찰할 수 있는 환경을 제공한다.

이 엔진은 하나의 답을 제시하지 않는다.
동역학 흐름으로 답을 유추할 수 있는 환경을 제시한다.

---

## 인식론적 위치

| 계층 | 역할 |
|------|------|
| **E5 화학** | `3_meterial/` 화학 레이어 허브 — Chemical_Reaction → Element_Capture → Carbon_Composite → **Hydrogen** |
| **E2 수학 코어** | `VectorSpace_102` — 수소 축(production, storage, safety, fc, econ)을 상태 벡터에 통합 |

---

## 수소가 무엇인가

수소(H₂)는 우주에서 가장 풍부한 원소이자, 가장 가벼운 분자이다.

| 속성 | 값 |
|------|-----|
| 분자량 | 2.016 g/mol |
| STP 밀도 | 0.0899 kg/m³ |
| LHV | 120 MJ/kg (33.3 kWh/kg) |
| HHV | 141.8 MJ/kg |
| 끓는점 | 20.28 K (−253 °C) |
| 가연 범위 | 4–75 vol% in air |
| 자연 발화 온도 | 585 °C |

**핵심 주의**: 수소는 에너지 *원(source)*이 아니라 에너지 *운반체(carrier)*이다.
수소를 만드는 데 에너지가 필요하고, 저장·수송·변환 과정에서 반드시 손실이 발생한다.

---

## 레이어 구조

```
L0  contracts.py           — 전체 데이터 계약
L1  properties.py          — H₂ 물성 카드, 이상기체/Van der Waals, 압축인자
L2  production.py          — 전기분해 (PEM/Alkaline/SOEC), SMR, 색상 코드
L3  storage.py             — 압축 가스, 액체 수소, 금속 수소화물
L4  fuel_cell.py           — Nernst OCV, PEMFC/SOFC/AFC 효율, 전력 밀도
L5  safety.py              — 가연 범위, 환기, 수소취성, 폭발 과압
L6  screening.py           — ATHENA 7-플래그 4단 판정
L7  extension_hooks.py     — 형제 엔진 브리지 9개, 미래 확장 13태그
    domain_space.py        — LOX/LH₂, ISRU, 생명유지
    domain_grid.py         — P2G 왕복 효율, LCOH
    domain_transport.py    — FCEV 주행거리, 충전 시간
    foundation.py          — 통합 진입점 + 건강도 5축
```

---

## 핵심 수식

| # | 이름 | 수식 | 레이어 |
|---|------|------|--------|
| 1 | 전해 셀 전압 | $V_{cell} = E_{rev} + \eta_{act} + j \cdot R_{ohm}$ | L2 |
| 2 | 페러데이 생산 | $\dot{m}_{H_2} = \eta_F \cdot I / (n \cdot F)$ | L2 |
| 3 | 전해 효율 | $\eta = E°_{rev} / V_{cell} \times \eta_F$ | L2 |
| 4 | SMR 평형 | $K_{eq} = \exp(-\Delta H° / RT + C)$ | L2 |
| 5 | 압축 일 | $W = nRT \ln(P_2/P_1) / \eta_{is}$ | L3 |
| 6 | 끓어오름 | $\dot{m}_{boiloff} = Q_{leak} / L_{vap}$ | L3 |
| 7 | 금속수소화물 | $\ln(P/P_{ref}) = (\Delta H/R)(1/T_{ref} - 1/T)$ | L3 |
| 8 | Nernst OCV | $E = E°(T) + \frac{RT}{2F} \ln\frac{P_{H_2}\sqrt{P_{O_2}}}{P_{H_2O}}$ | L4 |
| 9 | 열역학 효율 | $\eta_{max} = \Delta G / \Delta H \approx 83\%$ | L4 |
| 10 | 환기 유량 | $Q = (\dot{m}/\rho_{H_2}) / (C_{target}/100)$ | L5 |

---

## 빠른 시작

```python
from hydrogen import run_hydrogen_foundation, HydrogenClaimPayload

report = run_hydrogen_foundation()
print(f"생산 효율: {report.production.efficiency:.1%}")
print(f"저장 왕복 효율: {report.storage.round_trip_efficiency:.1%}")
print(f"연료전지 전기 효율: {report.fuel_cell.efficiency_electric:.1%}")
print(f"안전 수준: {report.safety.risk_level}")
print(f"건강도: {report.health.verdict.value}")
print(f"  Ω_production: {report.health.omega_production:.3f}")
print(f"  Ω_storage:    {report.health.omega_storage:.3f}")
print(f"  Ω_conversion: {report.health.omega_conversion:.3f}")
print(f"  Ω_safety:     {report.health.omega_safety:.3f}")
print(f"  Ω_economics:  {report.health.omega_economics:.3f}")
print(f"  Ω_composite:  {report.health.composite_omega:.3f}")

# 주장 스크리닝
claim = HydrogenClaimPayload(
    claim_text="무한 재활용 수소 시스템",
    tags=["perpetual"],
)
report = run_hydrogen_foundation(claim=claim)
print(f"스크리닝: {report.screening.verdict.value}")
print(f"  플래그: {report.screening.flags}")
```

---

## ATHENA 스크리닝 (L6)

| 판정 | 조건 |
|------|------|
| **Positive** | Ω ≥ 0.65, 플래그 없음 |
| **Neutral** | Ω ≥ 0.45 |
| **Cautious** | Ω ≥ 0.25 |
| **Negative** | Ω < 0.25 |

7가지 플래그:

| 플래그 | 의미 |
|--------|------|
| `thermodynamics_violation` | 효율 > 100 % 또는 에너지 밀도 > HHV |
| `impossible_cost` | 물리적 에너지 바닥 아래의 비용 주장 |
| `perpetual_hydrogen` | 외부 에너지 없는 폐쇄 순환 주장 |
| `ignored_storage_losses` | 압축/끓어오름/왕복 손실 무시 |
| `over_unity_fuel_cell` | 연료전지 효율 > ΔG/ΔH (~83 %) |
| `safety_handwave` | 가연성·수소취성 미언급 |
| `colour_washing` | 색상 코드 오분류 |

---

## 수소 색상 코드

| 색상 | 생산 경로 | CO₂ 강도 |
|------|-----------|----------|
| 🟢 Green | 재생에너지 전기분해 | ~0 |
| 🔵 Blue | SMR + CCS | ~1 kg/kg |
| ⚪ Grey | SMR (CCS 없음) | ~10 kg/kg |
| 🩷 Pink | 원자력 전기분해 | ~0 |
| 🩵 Turquoise | 메탄 열분해 | 고체 탄소 |

---

## 형제 엔진 연결

| 엔진 | 연결 유형 |
|------|-----------|
| `Chemical_Reaction_Foundation` | **직접** — ΔG, Arrhenius, Nernst, Faraday 공유 |
| `Element_Capture_Foundation` | **직접** — H₂ 포집 종, TerraCore 브리지 |
| `Carbon_Composite_Stack` | **직접** — Type IV 압축 탱크 CFRP |
| `TerraCore_Stack` | **직접** — WaterCycle.h2_from_electrolysis() |
| `FusionCore_Stack` | **동위원소** — D-T 핵연료 = 수소 동위원소 |
| `Battery_Dynamics_Engine` | **상보적** — 전기화학 공유 (Nernst, 과전위) |
| `Token_Dynamics_Foundation` | **개념적 아날로지** — H₂ = 에너지 토큰 |
| `Antimatter_Phenomenology_Engine` | **개념적** — 에너지 운반체 비교 |
| `VectorSpace_102` | **허브** — 수소 축 → 상태 벡터 통합 |

---

## 건강도 5축 (Ω)

| 축 | 의미 |
|----|------|
| `omega_production` | 생산 효율 / 목표 (80 %) |
| `omega_storage` | 저장 왕복 효율 / 목표 (90 %) |
| `omega_conversion` | 연료전지 효율 / 목표 (60 %) |
| `omega_safety` | 안전 상태 (이진 → 0.85 또는 0.30) |
| `omega_economics` | 비용 정규화 (1 − cost/20) |

**Cold Audit 경고**: 모든 축 > 0.90 → "현실 마찰 미반영" 경고.

---

## 현재 한계

- **열역학 정밀도**: 모든 수식은 tree-level cartoon. NIST 물성 표나 Aspen 수준의 정밀도가 아님.
- **연료전지**: 분극 곡선(V-I curve) 피팅 없음. 단일 작동점 평가.
- **안전**: TNT 등가 과압은 screening-level 추정. CFD/FEA 대체 불가.
- **경제성**: LCOH는 간이 계산. 실제 프로젝트는 DCF 모델 필요.
- **수송**: 파이프라인 블렌딩, 암모니아 크래킹 미구현.

---

## 테스트

```
pytest tests/ -v
95 passed in 0.08s
```

| 범주 | 테스트 수 |
|------|-----------|
| constants | 8 |
| properties | 9 |
| production | 14 |
| storage | 11 |
| fuel_cell | 10 |
| safety | 10 |
| screening | 6 |
| extension_hooks | 4 |
| domain_space | 3 |
| domain_grid | 3 |
| domain_transport | 4 |
| foundation | 8 |
| integrity | 4 |
| **합계** | **95** |

---

## 다음 계획 (v0.2)

- 분극 곡선 피팅 (PEMFC/SOFC)
- 암모니아 크래킹 동역학
- LOHC 탈수소화
- 수소 파이프라인 블렌딩
- 지질학적 저장 (소금동굴)
- 수소취성 피로 모델
- LCOH 테크노-이코노미 모듈
- VectorSpace 어댑터 통합

---

*Hydrogen_Foundation v0.1.0 — 수소의 생산·저장·변환·안전·경제성을 관찰하는 기초 레이어.*

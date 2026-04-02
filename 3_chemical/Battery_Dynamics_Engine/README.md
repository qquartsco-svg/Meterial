# Battery Dynamics Engine — 배터리 ECM 물리·시뮬레이션·검증 엔진

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://python.org)
[![Tests](https://img.shields.io/badge/tests-252%20passed-brightgreen)](#테스트)
[![Version](https://img.shields.io/badge/version-0.4.0-orange)](#버전-히스토리)
[![License](https://img.shields.io/badge/license-MIT-green)](#)

순수 Python으로 구현된 **배터리 셀·팩 동역학 평가 엔진**.
1RC/2RC 등가회로(ECM) + 실측 OCV 곡선 + Arrhenius 온도 의존 저항 + 1D 팩 열 체인 기반으로
SOC·분극전압·온도·단자전압을 시간에 따라 계산하고, EKF 추정기·팩 밸런서·Ω 지수로 상태를 평가합니다.

> **📐 엔진 정체성** — Layer A (단일 셀 ECM) + Layer B (배터리 팩 시스템) 2-레이어 구조.
> 셀 레벨: `x = [SOC, V_RC1, (V_RC2), T]`, 팩 레벨: `PackState(cells=[...]) + PackObservation(Ω_global)`.

> **⚠️ 범위 안내** — ECM 기반 설계 탐색·마진 추정·시나리오 분석 도구입니다.
> Butler-Volmer 전기화학 상세 모델·SPICE/TCAD 수준 정밀도는 범위 밖입니다.
> 모든 수치는 ECM 추정치이며, 상용 배터리 시뮬레이터를 대체하지 않습니다.

---

## 목차

1. [특징](#특징)
2. [아키텍처](#아키텍처)
3. [빠른 시작](#빠른-시작)
4. [ECM 물리 모델](#ecm-물리-모델)
5. [OCV 테이블 & Arrhenius R(T)](#ocv-테이블--arrhenius-rt)
6. [CC-CV 충전](#cc-cv-충전)
7. [EKF SOC 추정기](#ekf-soc-추정기)
8. [Observer Ω 5레이어](#observer-ω-5레이어)
9. [Layer B — 배터리 팩 시스템](#layer-b--배터리-팩-시스템)
10. [시뮬레이션 API](#시뮬레이션-api)
11. [파라미터 스윕](#파라미터-스윕)
12. [시나리오 시뮬레이션](#시나리오-시뮬레이션)
13. [공정 프리셋](#공정-프리셋)
14. [API 레퍼런스](#api-레퍼런스)
15. [테스트](#테스트)
16. [버전 히스토리](#버전-히스토리)

---

## 특징

| 기능 | 설명 |
|------|------|
| **1RC / 2RC ECM** | 단기·장기 분극 자동 전환, `v_rc2` 상태 추가 |
| **OCV 테이블** | NMC·LFP·LCO 실측 곡선 구간선형 보간, 선형 fallback |
| **Arrhenius R(T)** | `R(T) = R_ref·exp(Eₐ/kB·(1/T−1/T_ref))`, 저온 임피던스 자동 반영 |
| **CC-CV 충전** | CC→CV 페이즈 자동 전환, 전류 테이퍼, `charge_phase` 기록 |
| **EKF 추정기** | 1RC/2RC 자동, Joseph 공분산, `soh_from_discharge()` |
| **방전 시뮬레이션** | 정전류, 종지 전압/SOC 자동 종료 |
| **Observer Ω** | 5레이어 건강 지수(0~1), HEALTHY/STABLE/FRAGILE/CRITICAL 판정 |
| **플래그 11종** | `critical_soc` / `thermal_critical` / `aging_warning` 등 실시간 경보 |
| **파라미터 스윕** | C-rate · SOH · 온도 · SOC 스냅샷 4종 스윕 |
| **시나리오** | 고C-rate 붕괴 · 열 스트레스 · 3단계 사이클 노화 감쇠 3종 |
| **셀 프리셋** | NMC_18650 / LFP_POUCH / LCO_PHONE / NMC_EV / NMC_AGED / LFP_COLD |
| **팩 시스템 (Layer B)** | nSnP 토폴로지, 셀 산포 모델, 1D 열 체인, 패시브/액티브 밸런서, Ω_global |
| **의존성 없음** | 순수 stdlib (math, dataclasses) — NumPy/SciPy 불필요 |

---

## 아키텍처

```
Battery Dynamics Engine v0.4.0
│
├── Layer A — 단일 셀 (battery_dynamics/)
│   ├── schema.py        — ECMParams, BatteryState, DischargeStep, Observation
│   ├── ecm.py           — OCV table/linear, 2RC ECM, Arrhenius R(T), 유틸리티
│   ├── observer.py      — Ω_battery 5레이어 관측 + diagnose 권고
│   ├── design_engine.py — 시뮬레이션·CC-CV·스윕·검증·시나리오 오케스트레이션
│   ├── estimator.py     — EKF SOC 추정기 + soh_from_discharge
│   └── presets.py       — NMC/LFP/LCO 화학종별 셀 프리셋 (OCV table 내장)
│
└── Layer B — 배터리 팩 (battery_pack/)
    ├── pack_schema.py   — PackTopology, CellVariation, PackParams, PackState (Composition)
    ├── pack_thermal.py  — 1D 열 체인 (전도·냉각·자동 sub-stepping)
    ├── balancer.py      — PassiveBalancer (블리딩) / ActiveBalancer (에너지 이동)
    ├── pack_observer.py — Ω_global = 0.60×Ω_min + 0.40×Ω_mean, 팩 플래그 7종
    └── pack_runtime.py  — build_pack_state, step_pack, simulate_pack_discharge/charge_cccv
```

**계층 상태공간:**

```
Layer A (셀)
  입력  u = I_cell [A]
  상태  x = [SOC, V_RC1, (V_RC2), T]
  출력  V_term + Ω_battery ∈ [0,1]
  추정  SOC_est = EKF(V_meas, I, dt)

Layer B (팩)
  입력  I_pack [A]  →  I_cell = I_pack / n_parallel
  상태  PackState(cells=[BatteryState × n_cells])
  출력  V_pack = n_series × V_cell_group + Ω_global ∈ [0,1]
  플래그  cell_imbalance / severe_imbalance / hot_cell / weak_cell / pack_degraded ...
```

## FrequencyCore 연결

[FrequencyCore_Engine](/Users/jazzin/Desktop/00_BRAIN/_staging/FrequencyCore_Engine/README.md)은
Battery Dynamics의 전압/전류/RC 리플을 주파수 도메인으로 보는 **공통 frequency kernel**이다.

대표 연결:

- `DischargeStep.v_term` → 전압 리플 지배 주파수
- `DischargeStep.current_a` → 충방전 제어기 ripple screening
- `DischargeStep.v_rc`, `v_rc2` → 분극 진동성 관측
- `BatteryFrequencyBridge` → `Ω_freq`, `harmonic_distortion`, `ripple_freq_hz`

실행 예:

```bash
python3 /Users/jazzin/Desktop/00_BRAIN/_staging/FrequencyCore_Engine/examples/run_real_engine_bridge_demo.py
```

이 연결은 ECM/팩 물리를 대체하지 않는다.
대신 **전압 리플과 제어기 진동성을 공통 척도로 관찰하는 screening 보강층**으로 쓰는 것이 자연스럽다.

---

## 빠른 시작

```python
from battery_dynamics import (
    NMC_18650,
    simulate_discharge,
    simulate_charge_cccv,
    observe_battery,
    EKFBatteryEstimator,
    BatteryState,
)

# 1. NMC 18650 셀 1C 방전 시뮬레이션
steps = simulate_discharge(NMC_18650, current_a=3.4, dt_s=10.0)

# 2. 결과 확인
for s in steps[::30]:
    print(f"t={s.t_s:5.0f}s  SOC={s.soc:.3f}  "
          f"V={s.v_term:.3f}V  T={s.temp_k - 273.15:.1f}°C  "
          f"Ω={s.omega_battery:.3f}  [{s.verdict}]")
```

```
t=    0s  SOC=1.000  V=4.199V  T=25.0°C  Ω=0.955  [HEALTHY]
t=  300s  SOC=0.916  V=4.147V  T=25.4°C  Ω=0.955  [HEALTHY]
t=  900s  SOC=0.748  V=4.041V  T=25.8°C  Ω=0.955  [HEALTHY]
t= 1800s  SOC=0.496  V=3.883V  T=26.0°C  Ω=0.955  [HEALTHY]
t= 2700s  SOC=0.244  V=3.596V  T=26.1°C  Ω=0.820  [STABLE]
t= 3240s  SOC=0.100  V=3.299V  T=26.1°C  Ω=0.637  [FRAGILE]
```

```python
# 3. CC-CV 충전 (1C, 20% → 만충)
cc_cv_steps = simulate_charge_cccv(NMC_18650, current_cc_a=3.4, soc_init=0.20)
cc_count = sum(1 for s in cc_cv_steps if s.charge_phase == "CC")
cv_count = sum(1 for s in cc_cv_steps if s.charge_phase == "CV")
print(f"CC: {cc_count}스텝  CV: {cv_count}스텝  에너지: {cc_cv_steps[-1].energy_wh:.2f}Wh")

# 4. EKF SOC 추정 (측정 전압 기반)
ekf = EKFBatteryEstimator(NMC_18650, soc_init=0.80)
for step in steps[:60]:
    est = ekf.step(V_meas=step.v_term, I_a=3.4, dt_s=10.0)
print(f"SOC_true={steps[60].soc:.4f}  SOC_est={est.soc_est:.4f}  σ={est.soc_std:.5f}")
```

---

## ECM 물리 모델

### 1RC / 2RC 등가회로

```
OCV(z) = table_interp(z)           ← 화학종별 실측 OCV 구간선형 보간
       = V₀ + k_ocv × z            ← ocv_table=None 시 선형 fallback

dz/dt      = −I / Q_eff                     [SOC 동역학]
dV_RC1/dt  = −V_RC1/(R₁C₁) + I/C₁         [1차 RC 분극]
dV_RC2/dt  = −V_RC2/(R₂C₂) + I/C₂         [2차 RC 분극, r2_ohm>0 시]

R₀(T) = R₀_ref · exp(Eₐ/(kB) · (1/T − 1/T_ref))   [Arrhenius 온도 의존]

V_term = OCV(z) − I·R₀(T) − V_RC1 − V_RC2          [단자전압]

C_th·dT/dt = I²·(R₀+R₁) − h·(T−T_amb)             [열 proxy]
```

**부호 규약**: I > 0 = 방전, I < 0 = 충전

```python
from battery_dynamics import (
    ocv, ocv_linear, terminal_voltage, step_ecm,
    c_rate, time_to_discharge, steady_state_temperature,
    NMC_18650, BatteryState,
)

p = NMC_18650
s = BatteryState(soc=1.0, v_rc=0.0, temp_k=298.15)

# OCV — table 보간 (NMC_18650은 24-point 실측 곡선)
print(f"OCV(SOC=1.0) = {ocv(1.0, p):.3f}V")   # 4.200V
print(f"OCV(SOC=0.5) = {ocv(0.5, p):.3f}V")   # 3.860V  ← 비선형

# C-rate 계산
I = 6.8
print(f"{I}A = {c_rate(I, p):.1f}C")   # 2.0C

# 1C 완전 방전 예상 시간
t_full = time_to_discharge(p, current_a=p.q_ah)
print(f"1C 완전 방전: {t_full:.0f}s ({t_full/3600:.2f}h)")   # 3600s

# 정상상태 온도 (2C)
T_ss = steady_state_temperature(current_a=p.q_ah * 2, p=p)
print(f"2C 정상상태 온도: {T_ss - 273.15:.1f}°C")
```

---

## OCV 테이블 & Arrhenius R(T)

### OCV 구간선형 보간

실측 화학종별 OCV 곡선을 내장 — 선형 근사 대비 SOC 추정 정확도가 크게 향상됩니다.

| 화학종 | 특성 | 포인트 수 |
|--------|------|----------|
| NMC | S-curve, 3.0~4.2V | 24 |
| LFP | 평탄 구간 3.24~3.32V (SOC 20~80%) | 30 |
| LCO | 고전압 S-curve, 3.0~4.35V | 24 |
| NMC EV | 플랫 구간 확대, 2.8~4.2V | 24 |

```python
from battery_dynamics import ocv, d_ocv_d_soc, LFP_POUCH, NMC_18650

# LFP: SOC 20~80% 구간 전압 변화 < 60mV (평탄 특성)
v25 = ocv(0.25, LFP_POUCH)   # ≈ 3.25V
v75 = ocv(0.75, LFP_POUCH)   # ≈ 3.31V
print(f"LFP 평탄 구간 ΔV = {(v75-v25)*1000:.1f}mV")   # ~60mV

# EKF Jacobian용 수치 기울기
slope_nmc = d_ocv_d_soc(0.5, NMC_18650)   # V/SOC
slope_lfp = d_ocv_d_soc(0.5, LFP_POUCH)   # ≈ 0.06 V/SOC (매우 완만)

# ocv_table=None → 선형 OCV fallback (v0.2 호환)
from battery_dynamics import get_preset
p_linear = get_preset("nmc_18650", ocv_table=None)
```

### Arrhenius 온도 의존 저항

저온에서 R0 급등, 고온에서 감소 — 실측 배터리 임피던스 온도 거동 반영.

```
R(T) = R_ref · exp(Eₐ / kB · (1/T − 1/T_ref))

  Eₐ = 0.35 eV  (NMC)   → −10°C에서 R0 ≈ 2.3× 증가
  Eₐ = 0.55 eV  (LFP)   → −10°C에서 R0 ≈ 4× 증가 (저온 민감)
  Eₐ = 0        → 상수 저항 (v0.2 호환)
```

```python
from battery_dynamics import r_at_temperature, NMC_18650, LFP_COLD

# NMC: −10°C vs 25°C
R_cold = r_at_temperature(NMC_18650.r0_ohm, 263.15, NMC_18650)
R_ref  = NMC_18650.r0_ohm
print(f"NMC R0(-10°C) = {R_cold*1000:.1f}mΩ  ({R_cold/R_ref:.1f}×)")

# LFP_COLD: Arrhenius 자동 처리 (수동 배율 불필요)
R_lfp_cold = r_at_temperature(LFP_COLD.r0_ohm, 263.15, LFP_COLD)
print(f"LFP R0(-10°C) = {R_lfp_cold*1000:.2f}mΩ  ({R_lfp_cold/LFP_COLD.r0_ohm:.1f}×)")
```

---

## CC-CV 충전

CC 정전류 → CV 정전압 2단계 충전. V_term이 `v_charge_max_v`에 도달하면 자동으로 CV 페이즈로 전환되고, 전류가 `I_cc × cv_cutoff_ratio` 이하로 떨어지면 종료됩니다.

```python
from battery_dynamics import simulate_charge_cccv, NMC_18650

steps = simulate_charge_cccv(
    NMC_18650,
    current_cc_a   = 3.4,      # CC 전류 [A] (1C)
    soc_init       = 0.20,     # 초기 SOC
    cv_voltage     = 4.20,     # CV 목표 전압 (None → v_charge_max_v)
    cv_cutoff_ratio= 0.05,     # 종지: I < 1C × 5% = 0.17A
    dt_s           = 1.0,
)

# 페이즈별 분석
cc_steps = [s for s in steps if s.charge_phase == "CC"]
cv_steps = [s for s in steps if s.charge_phase == "CV"]

print(f"CC: {cc_steps[-1].t_s:.0f}s  →  SOC={cc_steps[-1].soc:.3f}  V={cc_steps[-1].v_term:.3f}V")
print(f"CV: {len(cv_steps)}스텝  최종 전류={abs(cv_steps[-1].current_a):.3f}A")
print(f"총 충전 에너지: {steps[-1].energy_wh:.3f}Wh")
```

```
CC: 2890s  →  SOC=0.926  V=4.200V
CV: 410스텝  최종 전류=0.168A
총 충전 에너지: 12.847Wh
```

> **📌 CC 전용과의 차이** — `simulate_charge()`는 CC 구간만 시뮬레이션합니다.
> 만충 정확도·충전 에너지 계산이 목적이라면 `simulate_charge_cccv()`를 사용하세요.

---

## EKF SOC 추정기

측정 단자전압으로 SOC를 실시간 추정하는 확장 칼만 필터(EKF). 순수 stdlib — NumPy 없음.

```
상태 (1RC): x = [SOC, V_RC1]
상태 (2RC): x = [SOC, V_RC1, V_RC2]

예측:
  SOC_{k+1}   = SOC_k − (I/Q_eff)·dt
  V_RC1_{k+1} = V_RC1_k·(1 − dt/τ₁) + I/C₁·dt
  P_pred = F · P · F^T + Q

갱신:
  h(x)  = OCV(SOC) − I·R₀(T) − V_RC1 − V_RC2
  H     = [dOCV/dSOC, −1, (−1)]
  K     = P·H^T / (H·P·H^T + R)
  x     = x_pred + K·(V_meas − h(x))
  P     = (I − K·H)·P·(I − K·H)^T + K·R·K^T   [Joseph 형식]
```

```python
from battery_dynamics import (
    EKFBatteryEstimator, EKFState,
    simulate_discharge, soh_from_discharge,
    NMC_18650, NMC_EV, BatteryState, step_ecm, terminal_voltage,
)

# ── 1RC EKF 기본 사용 ──────────────────────────────────────────
ekf = EKFBatteryEstimator(NMC_18650, soc_init=0.80, r_meas=1e-3)

s = BatteryState(soc=0.80, v_rc=0.0, temp_k=298.15)
for _ in range(100):
    s = step_ecm(s, I_a=3.4, dt_s=1.0, p=NMC_18650)
    V_meas = terminal_voltage(s, 3.4, NMC_18650)
    est = ekf.step(V_meas=V_meas, I_a=3.4, dt_s=1.0)

print(f"SOC_true={s.soc:.4f}  SOC_est={est.soc_est:.4f}  σ={est.soc_std:.5f}")
# SOC_true=0.7221  SOC_est=0.7198  σ=0.00412

# ── 2RC EKF (NMC_EV) ───────────────────────────────────────────
ekf_2rc = EKFBatteryEstimator(NMC_EV, soc_init=0.75)
print(f"RC 차수: {ekf_2rc.n_rc}")   # 2

# ── BatteryState 변환 ──────────────────────────────────────────
bs = ekf.to_battery_state()           # → BatteryState (simulate 입력으로 재사용)

# ── SOH 추정 (방전 궤적 전류 적분) ────────────────────────────
steps = simulate_discharge(NMC_18650, current_a=3.4, dt_s=1.0)
soh = soh_from_discharge(steps, NMC_18650)
print(f"SOH 추정: {soh:.3f}")   # ≈ 1.000 (신품)
```

---

## Observer Ω 5레이어

모든 물리 지표를 0~1 범위의 건강 지수로 통합:

| 레이어 | 가중치 | 기반 지표 |
|--------|--------|-----------|
| Ω_soc | 0.30 | SOC 잔량 (soc_floor=10%, soc_warn=20%) |
| Ω_voltage | 0.25 | 단자전압 마진 (t_cutoff_v 기준) |
| Ω_thermal | 0.20 | 온도 상태 (−5°C~45°C 정상, 60°C 위험) |
| Ω_impedance | 0.15 | SOH + R0 절대값 기반 저항 열화 |
| Ω_aging | 0.10 | SOH 기반 수명 건강도 |

```
Ω_battery = 0.30·Ω_soc + 0.25·Ω_voltage + 0.20·Ω_thermal
           + 0.15·Ω_impedance + 0.10·Ω_aging
```

**강제 하향 임계**: `critical_soc` 또는 `thermal_critical` 플래그 활성 시 Ω ≤ 0.29 → CRITICAL 강제 판정

| Ω_battery | 판정 |
|-----------|------|
| ≥ 0.75 | HEALTHY |
| ≥ 0.52 | STABLE |
| ≥ 0.30 | FRAGILE |
| < 0.30 | CRITICAL |

```python
from battery_dynamics import observe_battery, diagnose, NMC_18650, BatteryState

s = BatteryState(soc=0.8, v_rc=0.01, temp_k=300.0)
obs = observe_battery(s, I_a=1.0, p=NMC_18650)
print(f"Ω={obs.omega_battery:.3f}  {obs.verdict}")
print(f"  soc={obs.omega_soc:.3f}  volt={obs.omega_voltage:.3f}  "
      f"therm={obs.omega_thermal:.3f}")

for line in diagnose(obs):
    print(f"  ▸ {line}")
```

### 플래그 11종

| 플래그 | 발생 조건 |
|--------|---------|
| `critical_soc` | SOC ≤ 10% |
| `low_soc` | SOC ≤ 20% |
| `discharge_cutoff` | V_term ≤ t_cutoff_v |
| `voltage_low` | V_term ≤ t_cutoff_v × 1.05 |
| `thermal_critical` | T ≥ 60°C |
| `thermal_warning` | T ≥ 45°C 또는 T < −5°C |
| `aging_critical` | SOH < 70% |
| `aging_warning` | 70% ≤ SOH < 80% |
| `high_impedance` | R0 > 200mΩ |
| `impedance_degraded` | R0 > 120mΩ |
| `power_limited` | SOC 낮음 또는 온도 경고 또는 전압 낮음 |

---

## Layer B — 배터리 팩 시스템

### 팩 토폴로지 & 셀 산포

```python
from battery_pack import (
    PackTopology, CellVariation, PackParams,
    build_pack_state, simulate_pack_discharge, simulate_pack_charge_cccv,
    observe_pack, PassiveBalancer, ActiveBalancer, PackThermal1D,
)
from battery_dynamics import NMC_18650

# 2직렬 3병렬 (2s3p) 팩
topo = PackTopology(n_series=2, n_parallel=3)  # → label="2s3p", 6셀

# 셀 산포 (제조 편차 시뮬레이션)
var  = CellVariation(soc_std=0.02, capacity_std=0.01, r0_std=0.05, temp_std_k=1.5, seed=42)
params = PackParams(cell_params=NMC_18650, topology=topo, variation=var)

# 팩 초기화 (Box-Muller 랜덤 산포 적용)
state = build_pack_state(params, soc_init=1.0, temp_init_k=298.15)
print(f"셀 수={len(state.cells)}  SOC spread={state.soc_spread:.4f}")
```

### 팩 방전 시뮬레이션

```python
# 패시브 밸런서 적용 방전
balancer = PassiveBalancer(soc_tolerance=0.02, bleed_current_a=0.1)
steps = simulate_pack_discharge(
    params, I_pack=10.2,   # 1C × 3p
    dt_s=10.0, n_steps=500,
    balancer=balancer,
)
last = steps[-1]
print(f"V_pack={last.v_pack:.3f}V  SOC_mean={last.soc_mean:.3f}  종료={last.terminated}")
```

### 1D 팩 열 체인

```python
# 양끝 냉각, 중앙 셀이 가장 뜨거워지는 구조
thermal = PackThermal1D(
    n_cells=6, cell_thermal_c=200.0,
    coolant_temp_k=298.15, h_cool_w_per_k=5.0,
)
# step()은 내부 auto sub-stepping으로 수치 안정 보장
steps = simulate_pack_discharge(params, I_pack=10.2, dt_s=10.0, thermal=thermal)
```

### Ω_global 팩 관측

```python
from battery_pack import observe_pack

obs = observe_pack(state, params, I_pack=10.2)
print(f"Ω_global={obs.omega_global:.4f}  verdict={obs.verdict}")
print(f"flags={obs.flags}")
# → Ω_global=0.9123  verdict=HEALTHY  flags=[]
```

**팩 전용 플래그:**

| 플래그 | 조건 |
|--------|------|
| `cell_imbalance` | SOC 편차 > 5% |
| `severe_imbalance` | SOC 편차 > 10% |
| `hot_cell` | 최고 셀 온도 ≥ 45°C |
| `critical_hot_cell` | 최고 셀 온도 ≥ 60°C → Ω_global ≤ 0.29 강제 |
| `temp_gradient` | 셀 간 온도 차이 > 5K |
| `weak_cell` | 최약 셀 SOC ≤ 15% |
| `pack_degraded` | 평균 Ω < 0.52 |

**Ω_global 공식:** `Ω_global = Ω_min × 0.60 + Ω_mean × 0.40` (최약 셀 중심)

---

## 시뮬레이션 API

### 방전 시뮬레이션

```python
from battery_dynamics import simulate_discharge, NMC_18650

steps = simulate_discharge(
    NMC_18650,
    current_a   = 6.8,       # 2C
    dt_s        = 1.0,
    n_steps     = 7200,
    soc_init    = 1.0,
    temp_init_k = 298.15,
)

last = steps[-1]
print(f"방전 완료: t={last.t_s:.0f}s  SOC={last.soc:.3f}  V={last.v_term:.3f}V")
print(f"방전 에너지: {last.energy_wh:.3f}Wh")
```

### CC-CV 충전 시뮬레이션

```python
from battery_dynamics import simulate_charge_cccv, NMC_18650

steps = simulate_charge_cccv(
    NMC_18650,
    current_cc_a    = 3.4,     # 1C CC 전류
    soc_init        = 0.20,
    cv_cutoff_ratio = 0.05,    # CV 종지: I < 5% × I_cc
    dt_s            = 1.0,
)

print(f"SOC: {steps[0].soc:.3f} → {steps[-1].soc:.3f}")
print(f"충전 시간: {steps[-1].t_s / 3600:.2f}h")
print(f"페이즈 전환 시점: "
      f"{next(s.t_s for s in steps if s.charge_phase=='CV'):.0f}s")
```

### CC 전용 충전 (단순)

```python
from battery_dynamics import simulate_charge, NMC_18650

steps = simulate_charge(
    NMC_18650,
    current_a  = 3.4,
    soc_init   = 0.20,
    soc_target = 0.95,    # CC 목표 SOC
    dt_s       = 10.0,
)
```

---

## 파라미터 스윕

### C-rate 스윕

```python
from battery_dynamics import sweep_c_rate, NMC_18650

results = sweep_c_rate(
    NMC_18650,
    c_rate_range = [0.5, 1.0, 2.0, 3.0, 5.0],
    dt_s         = 5.0,
)

for r in results:
    print(f"  {r['c_rate']}C  →  {r['duration_s']:.0f}s  "
          f"{r['capacity_ah']:.2f}Ah  "
          f"V_min={r['min_v_term']:.3f}V  "
          f"T_max={r['max_temp_k'] - 273.15:.1f}°C")
```

출력 예시 *(NMC_18650 프리셋 기준 — 실제 셀 특성과 차이 가능)*:
```
  0.5C  →  7128s  2.976Ah  V_min=3.048V  T_max=25.1°C
  1.0C  →  3518s  2.924Ah  V_min=3.003V  T_max=25.3°C
  2.0C  →  1724s  2.830Ah  V_min=2.840V  T_max=25.8°C
  3.0C  →  1116s  2.760Ah  V_min=2.827V  T_max=26.3°C
  5.0C  →   629s  2.601Ah  V_min=2.801V  T_max=27.1°C
```

### SOH 스윕 (노화 분석)

```python
from battery_dynamics import sweep_soh, NMC_18650

results = sweep_soh(
    NMC_18650,
    soh_range = [1.0, 0.90, 0.80, 0.75, 0.70],
    dt_s      = 10.0,
)

for r in results:
    print(f"  SOH={r['soh']:.2f}  용량={r['capacity_ah']:.2f}Ah  "
          f"에너지={r['energy_wh']:.2f}Wh  Ω={r['final_omega']:.3f}")
```

### 온도 스윕

```python
from battery_dynamics import sweep_temperature, NMC_18650

results = sweep_temperature(
    NMC_18650,
    T_range = [253.15, 273.15, 298.15, 318.15, 338.15],
    dt_s    = 10.0,
)

for r in results:
    print(f"  T={r['T_c']:.0f}°C  "
          f"용량={r['capacity_ah']:.2f}Ah  "
          f"T_peak={r['max_temp_k'] - 273.15:.1f}°C  "
          f"[{r['final_verdict']}]")
```

### SOC 스냅샷 스윕

```python
from battery_dynamics import sweep_soc_snapshot, NMC_18650

results = sweep_soc_snapshot(
    NMC_18650,
    soc_range = [1.0, 0.8, 0.6, 0.4, 0.2, 0.1],
    current_a = 3.4,
)

for r in results:
    print(f"  SOC={r['soc']:.2f}  V={r['v_term']:.3f}V  "
          f"P={r['power_w']:.1f}W  Ω={r['omega_battery']:.3f}  [{r['verdict']}]")
```

---

## 시나리오 시뮬레이션

> **📌 모델 의존 수치** — 아래 시나리오의 모든 수치(전압 붕괴 C-rate, 열 위험 온도, 노화 사이클 수 등)는
> ECMParams 설정(R0, R1, C1, C_th, h 등)과 OCV 곡선에 **강하게 의존**합니다.
> 실제 셀 측정치·JEDEC 규격·제조사 데이터시트와 직접 대응하지 않으며,
> 설계 탐색·마진 평가·시나리오 비교 목적으로 해석해야 합니다.

### 고C-rate 방전 붕괴 탐색

```python
from battery_dynamics import scenario_fast_discharge_collapse, NMC_18650

result = scenario_fast_discharge_collapse(
    NMC_18650,
    c_rate_range = [0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0],
)
print(result["summary"])

for r in result["per_c_rate"]:
    print(f"  {r['c_rate']:5.1f}C  →  {r['duration_s']:6.0f}s  "
          f"V_min={r['min_v_term']:.3f}V")
```

출력 예시 *(NMC_18650 프리셋 기준)*:
```
전압 붕괴 임계: 50.0C (방전 즉시 종지) | 60s 이상 지속 최대 C-rate: 5.0C
   0.5C  →    7128s  V_min=3.048V
  10.0C  →     212s  V_min=2.804V
  50.0C  →       1s  V_min=2.799V
```

### 열 스트레스 분석

```python
from battery_dynamics import scenario_thermal_stress, NMC_18650

result = scenario_thermal_stress(
    NMC_18650,
    T_range   = [273.15, 298.15, 318.15, 328.15, 338.15, 348.15],
    current_a = 3.4,
)
print(result["summary"])

for r in result["per_temperature"]:
    flag = "⚠ THERMAL" if r["thermal_flag_active"] else "✓"
    print(f"  T_amb={r['T_c']:.0f}°C  "
          f"T_peak={r['max_temp_k'] - 273.15:.1f}°C  "
          f"{r['final_verdict']}  {flag}")
```

### 사이클 노화 — 3단계 감쇠 모델

v0.3.0의 `scenario_aging_capacity_fade()`는 3단계 노화 모델을 기본으로 사용합니다.

```
Phase 1 (SEI 형성, 0~n_knee1):    SOH = 1 − c·√n          [초기 빠른 감쇠]
Phase 2 (선형 중기, n_knee1~n_knee2): SOH = SOH_k1 − rate·Δn  [일정 감쇠]
Phase 3 (무릎 후 가속, n_knee2~):  SOH = SOH_k2 − accel·Δn  [가속 감쇠]
```

```python
from battery_dynamics import scenario_aging_capacity_fade, NMC_18650

result = scenario_aging_capacity_fade(
    NMC_18650,
    use_3phase  = True,       # 기본값
    n_knee1     = 200,        # SEI 안정화 사이클
    n_knee2     = 800,        # 무릎점 (NMC 대표값)
    sei_coeff   = 0.0015,     # Phase 1 계수
    linear_rate = 1.5e-4,     # Phase 2 감쇠율 [/cy]
    accel_rate  = 6e-4,       # Phase 3 가속 감쇠율 [/cy]
    cycle_range = [0, 100, 200, 500, 800, 1000, 1500, 2000],
)
print(result["summary"])

for r in result["per_cycle"]:
    print(f"  {r['cycle']:5d}cy  SOH={r['soh']:.3f}  "
          f"용량={r['capacity_ah']:.2f}Ah  [{r['phase']}]  Ω={r['final_omega']:.3f}")
```

출력 예시 *(NMC_18650 3단계 모델, 무릎점 800cy 기준)*:
```
3단계 노화 모델 (무릎점 800cy) | EOL (SOH<80%): 1500사이클
      0cy  SOH=1.000  용량=2.92Ah  [SEI]       Ω=0.955
    200cy  SOH=0.979  용량=2.86Ah  [SEI]       Ω=0.943
    500cy  SOH=0.934  용량=2.74Ah  [LINEAR]    Ω=0.923
    800cy  SOH=0.889  용량=2.61Ah  [POST_KNEE] Ω=0.905
   1500cy  SOH=0.749  용량=2.15Ah  [POST_KNEE] Ω=0.832
```

> **`use_3phase=False`** → v0.2 호환 선형 모델 (`capacity_fade_per_cycle` 파라미터 사용)

---

## 공정 프리셋

| 프리셋 | 화학종 | 폼팩터 | Q_ah | V_cutoff | OCV table | Eₐ [eV] | 용도 |
|--------|--------|--------|------|----------|-----------|---------|------|
| `NMC_18650` | NMC | 원통형 | 3.4Ah | 2.8V | ✓ (24pt) | 0.35 | 모바일·노트북 |
| `LFP_POUCH` | LFP | 파우치 대형 | 100Ah | 2.5V | ✓ (30pt) | 0.55 | EV·중대형 ESS |
| `LCO_PHONE` | LCO | 파우치 슬림 | 4.0Ah | 3.0V | ✓ (24pt) | 0.30 | 스마트폰 |
| `NMC_EV` | NMC | 각형 EV | 230Ah | 2.8V | ✓ (24pt) | 0.35 | 전기차 팩 (2RC) |
| `NMC_AGED` | NMC | 원통형 노화 | 3.4Ah | 2.8V | ✓ | 0.35 | SOH=0.78 노화 셀 |
| `LFP_COLD` | LFP | 파우치 저온 | 100Ah | 2.5V | ✓ | 0.55 | −10°C 환경 |

> **NMC_EV** — 2RC 모드: τ₁=56s(단기 분극) + τ₂=150s(장기 분극 R₂=0.3mΩ, C₂=500kF)
> **LFP_COLD** — Arrhenius Eₐ=0.55eV → −10°C에서 R₀ 자동 ~4배 증가

```python
from battery_dynamics import get_preset, list_presets

print(list_presets())
# ['lfp_cold', 'lfp_pouch', 'lco_phone', 'nmc_18650', 'nmc_aged', 'nmc_ev']

# 프리셋 + 파라미터 오버라이드
hot_cell   = get_preset("nmc_18650", t_amb_k=318.15)       # 45°C 환경
aged_ev    = get_preset("nmc_ev",    soh=0.80)              # 20% 노화 EV 팩
no_table   = get_preset("lfp_pouch", ocv_table=None)        # 선형 OCV fallback
```

---

## API 레퍼런스

### ECM 물리 (`ecm.py`)

```python
# OCV
ocv(soc, p)                                # OCV [V] — table 보간 or 선형 fallback
ocv_linear(soc, p)                         # OCV [V] — 선형 근사 (v0.2 호환)
ocv_at_soc(soc, p)                         # ocv() alias
d_ocv_d_soc(soc, p, eps=1e-4)             # dOCV/dSOC 수치 기울기 (EKF Jacobian용)

# 온도 의존 저항
r_at_temperature(r_ref, T_k, p)            # Arrhenius R(T) [Ω]

# ECM 적분
terminal_voltage(s, I_a, p)                # V_term [V]  (2RC + Arrhenius 반영)
step_ecm(s, I_a, dt_s, p)                 # 1스텝 적분 → BatteryState (1RC/2RC 자동)

# 파생 지표
c_rate(current_a, p)                       # C-rate 배수
effective_capacity_ah(p)                   # SOH 반영 실효 용량 [Ah]
internal_resistance_total(p)               # R0+R1+(R2) [Ω]
voltage_drop_at_current(current_a, p)      # ΔV = I·R_total [V]
time_to_discharge(p, current_a, ...)       # 선형 근사 방전 시간 [s]
soc_at_time(t_s, current_a, p, ...)        # SOC(t) 선형 근사
thermal_time_constant(p)                   # τ_th = C_th/h [s]
steady_state_temperature(current_a, p)     # T_ss [K]
max_continuous_current(p, t_max_k)         # 온도 제한 최대 전류 [A]
power_capability(s, p)                     # 순시 전력 공급 능력 [W]
```

### EKF 추정기 (`estimator.py`)

```python
# 추정기 클래스
EKFBatteryEstimator(params, soc_init, ...)  # 1RC/2RC 자동 EKF
  .predict(I, dt, T_k)                      # 예측 스텝
  .update(V_meas, I, T_k)                   # 갱신 스텝
  .step(V_meas, I_a, dt_s, T_k)            # predict + update → EKFState
  .reset(soc, v_rc1, v_rc2, ...)           # 재초기화
  .to_battery_state(T_k, t_s)             # → BatteryState

# SOH 추정
soh_from_discharge(steps, params, ...)     # 방전 궤적 전류 적분 → SOH 추정값
```

### Observer (`observer.py`)

```python
observe_battery(s, I_a, p, ...)            # → BatteryObservation (Ω 5레이어)
diagnose(obs)                              # → List[str]  Athena 권고 메시지
```

### 설계 엔진 (`design_engine.py`)

```python
# 시뮬레이션
simulate_discharge(p, current_a, dt_s, n_steps, ...)  # → List[DischargeStep]
simulate_charge(p, current_a, dt_s, n_steps, ...)      # → List[DischargeStep] (CC 전용)
simulate_charge_cccv(p, current_cc_a, dt_s, ...)       # → List[DischargeStep] (CC-CV)

# 스윕
sweep_c_rate(p, c_rate_range, dt_s, n_steps)
sweep_soh(p, soh_range, current_a, ...)
sweep_temperature(p, T_range, current_a, ...)
sweep_soc_snapshot(p, soc_range, current_a)

# 검증
verify_battery(state, params, current_a)               # → VerificationReport

# 시나리오
scenario_fast_discharge_collapse(p, c_rate_range, ...)
scenario_thermal_stress(p, T_range, current_a, ...)
scenario_aging_capacity_fade(p, cycle_range, use_3phase, ...)
```

### 프리셋 (`presets.py`)

```python
get_preset(name, **overrides)              # → ECMParams
list_presets()                             # → List[str]
```

---

## 테스트

```bash
# 전체 테스트 실행
cd Battery_Dynamics_Engine
python -m pytest tests/ -v

# 파일별
python -m pytest tests/test_battery.py    -v   # §1~§8  Layer A v0.2  (101 tests)
python -m pytest tests/test_battery_v3.py -v   # §1~§7  Layer A v0.3   (87 tests)
python -m pytest tests/test_pack.py       -v   # §1~§10 Layer B v0.4   (64 tests)
```

**테스트 구성 (총 252 tests):**

| 파일 | 섹션 | 내용 | 수 |
|------|------|------|----|
| `test_battery.py` | §1 ECM 물리 | OCV·step_ecm·terminal_voltage | 18 |
| | §2 파생 지표 | c_rate·시간·열 함수 | 12 |
| | §3 Observer Ω | 5레이어·플래그·diagnose | 16 |
| | §4 시뮬레이션 | 방전·충전·종료 조건 | 12 |
| | §5 파라미터 스윕 | c_rate·SOH·온도·SOC | 12 |
| | §6 검증 보고서 | PASS/MARGINAL/FAIL | 8 |
| | §7 프리셋 | 6종·get_preset·list | 11 |
| | §8 시나리오 | 3종 시나리오 | 12 |
| `test_battery_v3.py` | §1 OCV table | 보간·LFP 평탄·단조성 | 13 |
| | §2 2RC ECM | RC2 분극·시정수·호환 | 7 |
| | §3 Arrhenius | 저온/고온·Ea=0 호환 | 7 |
| | §4 CC-CV | 페이즈 전환·종지·에너지 | 14 |
| | §5 EKF | predict/update·수렴·1RC/2RC | 16 |
| | §5b SOH 추정 | 방전 적분 기반 | 4 |
| | §6 3단계 노화 | SEI/LINEAR/POST_KNEE·EOL | 11 |
| | §7 하위호환 | v0.2 API 전수 | 15 |
| `test_pack.py` | §1 PackSchema | 토폴로지·PackState·파생지표 | 12 |
| | §2 PackThermal1D | 수렴·발열·기울기·안정성 | 6 |
| | §3 PassiveBalancer | 밸런싱 판단·전류 벡터 | 6 |
| | §4 ActiveBalancer | 에너지 이동·효율·정보 | 5 |
| | §5 build_pack_state | 셀 수·산포·재현성 | 6 |
| | §6 step_pack | SOC 감소·열 업데이트 | 5 |
| | §7 simulate_pack_discharge | 종료·단조성·팩 전압 | 8 |
| | §8 simulate_pack_charge_cccv | 충전·종지 | 4 |
| | §9 PackObserver | Ω_global·플래그·verdicts | 7 |
| | §10 Integration | 밸런싱 수렴·열 기울기·LFP | 5 |

---

## 버전 히스토리

| 버전 | 내용 |
|------|------|
| **v0.4.0** | Layer B 팩 시스템 — battery_pack 패키지: nSnP 토폴로지·CellVariation·PackThermal1D·PassiveBalancer·ActiveBalancer·Ω_global Observer · 252 tests |
| **v0.3.0** | Layer A 심화 — OCV table (A1) · 2RC ECM (A2) · Arrhenius R(T) (A3) · CC-CV 충전 (A4) · EKF SOC 추정기 (B1) · 3단계 노화 모델 (B3) · 188 tests |
| **v0.2.0** | 완전 독립형 팹리스화 — design_engine·presets·5레이어 Observer·시나리오 3종·101 tests |
| **v0.1.0** | 초기 릴리스: ECM 1RC + 간략 열 proxy + 단순 Observer |

---

## 관련 저장소

- **[RAM (Memory Engine)](https://github.com/qquartsco-svg/RAM)** — DRAM/SRAM 반도체 메모리 설계·시뮬레이션·검증 엔진
- **[ENGINE_HUB](https://github.com/qquartsco-svg/ENGINE_HUB)** — 동역학 시뮬레이션 엔진 허브
- **[SNN_Backends](https://github.com/qquartsco-svg/SNN_Backends)** — 스파이킹 신경망 백엔드

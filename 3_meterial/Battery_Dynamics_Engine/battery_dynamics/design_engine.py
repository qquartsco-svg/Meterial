"""배터리 설계 엔진 — 시뮬레이션·스윕·검증·시나리오.

아키텍처
─────────
  시뮬레이션  — simulate_discharge / simulate_charge
  스윕        — sweep_c_rate / sweep_soh / sweep_temperature / sweep_soc_snapshot
  검증        — verify_battery
  시나리오    — scenario_fast_discharge_collapse
               scenario_thermal_stress
               scenario_aging_capacity_fade

모든 함수는 순수 Python stdlib 기반.
외부 패키지(numpy/scipy) 의존성 없음.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional

from .schema import (
    BatteryState,
    DischargeStep,
    ECMParams,
    VerificationReport,
)
from .ecm import (
    c_rate as _c_rate,
    effective_capacity_ah,
    ocv_linear,
    ocv,
    r_at_temperature,
    step_ecm,
    terminal_voltage,
    time_to_discharge,
)
from .observer import observe_battery, diagnose


# ══════════════════════════════════════════════════════════════════════════════
# 내부 헬퍼
# ══════════════════════════════════════════════════════════════════════════════

def _make_step(
    s: BatteryState,
    I_a: float,
    p: ECMParams,
    energy_wh: float,
    terminated: bool,
    charge_phase: str = "",
) -> DischargeStep:
    vt  = terminal_voltage(s, I_a, p)
    cr  = _c_rate(I_a, p)
    pw  = abs(I_a) * max(0.0, vt)
    obs = observe_battery(s, I_a, p)
    return DischargeStep(
        t_s           = round(s.t_s, 4),
        soc           = round(s.soc, 6),
        v_term        = round(vt, 6),
        temp_k        = round(s.temp_k, 4),
        current_a     = round(I_a, 6),
        v_rc          = round(s.v_rc, 6),
        c_rate        = round(cr, 4),
        power_w       = round(pw, 4),
        energy_wh     = round(energy_wh, 6),
        omega_battery = obs.omega_battery,
        verdict       = obs.verdict,
        terminated    = terminated,
        v_rc2         = round(s.v_rc2, 6),
        charge_phase  = charge_phase,
    )


# ══════════════════════════════════════════════════════════════════════════════
# 시뮬레이션
# ══════════════════════════════════════════════════════════════════════════════

def simulate_discharge(
    params: ECMParams,
    current_a: float,
    dt_s: float = 1.0,
    n_steps: int = 7200,
    soc_init: float = 1.0,
    temp_init_k: Optional[float] = None,
    v_rc_init: float = 0.0,
) -> List[DischargeStep]:
    """정전류 방전 시뮬레이션.

    Args
    ----
    params      : ECM 파라미터.
    current_a   : 방전 전류 [A] (양수).
    dt_s        : 시뮬레이션 스텝 [s].
    n_steps     : 최대 스텝 수.
    soc_init    : 초기 SOC.
    temp_init_k : 초기 셀 온도 [K] (None → params.t_amb_k).
    v_rc_init   : 초기 RC 분극 전압 [V].

    Returns
    -------
    DischargeStep 리스트 (t_cutoff_v 도달 또는 n_steps 종료 시).

    Notes
    -----
    - SOC = 0 또는 V_term ≤ t_cutoff_v 에서 자동 종료.
    - 마지막 스텝은 terminated=True.
    """
    I      = max(0.0, float(current_a))
    dt     = max(1e-6, float(dt_s))
    T_init = float(temp_init_k) if temp_init_k is not None else params.t_amb_k

    s = BatteryState(
        soc    = max(0.0, min(1.0, float(soc_init))),
        v_rc   = float(v_rc_init),
        temp_k = T_init,
        t_s    = 0.0,
    )

    steps: List[DischargeStep] = []
    energy_wh = 0.0

    for _ in range(int(n_steps) + 1):
        vt = terminal_voltage(s, I, params)
        terminated = vt <= params.t_cutoff_v or s.soc <= 0.0

        steps.append(_make_step(s, I, params, energy_wh, terminated))

        if terminated:
            break

        # 에너지 누적
        energy_wh += abs(I) * max(0.0, vt) * dt / 3600.0

        # 상태 갱신
        s = step_ecm(s, I, dt, params)

    return steps


def simulate_charge(
    params: ECMParams,
    current_a: float,
    dt_s: float = 1.0,
    n_steps: int = 7200,
    soc_init: float = 0.20,
    soc_target: float = 0.95,
    temp_init_k: Optional[float] = None,
) -> List[DischargeStep]:
    """정전류 충전 시뮬레이션 (CC 구간).

    Args
    ----
    current_a  : 충전 전류 [A] (양수 입력, 내부에서 음수 처리).
    soc_target : 목표 SOC (달성 시 종료).

    Returns
    -------
    DischargeStep 리스트 (I 음수로 기록됨 — 충전 방향).
    """
    I_charge = -abs(float(current_a))    # 충전 = 음수 전류
    dt       = max(1e-6, float(dt_s))
    T_init   = float(temp_init_k) if temp_init_k is not None else params.t_amb_k

    s = BatteryState(
        soc    = max(0.0, min(1.0, float(soc_init))),
        v_rc   = 0.0,
        temp_k = T_init,
        t_s    = 0.0,
    )

    steps: List[DischargeStep] = []
    energy_wh = 0.0

    for _ in range(int(n_steps) + 1):
        vt = terminal_voltage(s, I_charge, params)
        # 충전 종지: SOC ≥ soc_target 또는 Vterm ≥ v_charge_max_v
        terminated = (s.soc >= float(soc_target)) or (vt >= params.v_charge_max_v)

        steps.append(_make_step(s, I_charge, params, energy_wh, terminated))

        if terminated:
            break

        energy_wh += abs(I_charge) * max(0.0, vt) * dt / 3600.0
        s = step_ecm(s, I_charge, dt, params)

    return steps


def simulate_charge_cccv(
    params: ECMParams,
    current_cc_a: float,
    dt_s: float = 1.0,
    n_steps: int = 14400,
    soc_init: float = 0.20,
    temp_init_k: Optional[float] = None,
    cv_voltage: Optional[float] = None,
    cv_cutoff_ratio: float = 0.05,
) -> List[DischargeStep]:
    """CC-CV 충전 시뮬레이션.

    Phase 1 (CC): 정전류 I_cc로 충전 → V_term ≥ v_cv 에서 Phase 2 전환.
    Phase 2 (CV): V_term = v_cv 고정 → 전류 테이퍼 → I < I_cc × ratio 에서 종지.

    Args
    ----
    params          : ECM 파라미터.
    current_cc_a    : CC 충전 전류 [A] (양수 입력, 내부 음수 처리).
    dt_s            : 시뮬레이션 스텝 [s].
    n_steps         : 최대 스텝 수.
    soc_init        : 초기 SOC.
    temp_init_k     : 초기 온도 [K] (None → params.t_amb_k).
    cv_voltage      : CV 목표 전압 [V] (None → params.v_charge_max_v).
    cv_cutoff_ratio : CV 종지 전류 비율 (I < I_cc × ratio 에서 종지).

    Returns
    -------
    DischargeStep 리스트. charge_phase = "CC" or "CV".
    """
    I_cc    = -abs(float(current_cc_a))   # 충전 = 음수 전류
    v_cv    = float(cv_voltage) if cv_voltage is not None else params.v_charge_max_v
    dt      = max(1e-6, float(dt_s))
    T_init  = float(temp_init_k) if temp_init_k is not None else params.t_amb_k
    cutoff  = abs(I_cc) * max(1e-6, float(cv_cutoff_ratio))

    s = BatteryState(
        soc    = max(0.0, min(1.0, float(soc_init))),
        v_rc   = 0.0,
        v_rc2  = 0.0,
        temp_k = T_init,
        t_s    = 0.0,
    )

    steps: List[DischargeStep] = []
    energy_wh = 0.0
    phase = "CC"

    for _ in range(int(n_steps) + 1):
        # 현재 스텝 전류 결정
        if phase == "CC":
            I = I_cc
        else:
            # CV: V_term = v_cv 유지 전류 계산
            # v_cv = OCV(soc) − I·R0(T) − V_RC1 − V_RC2
            # I_cv = (OCV − V_RC1 − V_RC2 − v_cv) / R0
            R0_t = r_at_temperature(params.r0_ohm, s.temp_k, params)
            I_raw = (ocv(s.soc, params) - s.v_rc - s.v_rc2 - v_cv) / max(1e-12, R0_t)
            # 충전 방향(음수)으로 클램프, 최대 크기 = I_cc
            I = max(I_cc, min(0.0, I_raw))

        vt = terminal_voltage(s, I, params)

        # CC → CV 전환
        if phase == "CC" and vt >= v_cv:
            phase = "CV"

        # 종지 조건
        terminated = (
            (phase == "CV" and abs(I) <= cutoff)
            or s.soc >= 1.0
        )

        steps.append(_make_step(s, I, params, energy_wh, terminated, phase))

        if terminated:
            break

        energy_wh += abs(I) * max(0.0, vt) * dt / 3600.0
        s = step_ecm(s, I, dt, params)

    return steps


# ══════════════════════════════════════════════════════════════════════════════
# 파라미터 스윕
# ══════════════════════════════════════════════════════════════════════════════

def sweep_c_rate(
    params: ECMParams,
    c_rate_range: List[float],
    dt_s: float = 1.0,
    n_steps: int = 7200,
) -> List[Dict[str, Any]]:
    """C-rate 스윕 → 방전 성능 비교.

    각 C-rate에서 전체 방전 시뮬레이션 후 요약 지표 반환.

    Returns
    -------
    List of {c_rate, current_a, duration_s, capacity_ah,
              energy_wh, min_v_term, max_temp_k, final_omega,
              final_verdict}
    """
    results = []
    for cr in c_rate_range:
        I = max(1e-6, float(cr)) * params.q_ah
        steps = simulate_discharge(params, current_a=I, dt_s=dt_s, n_steps=n_steps)
        if not steps:
            continue

        last = steps[-1]
        duration = last.t_s
        capacity = abs(I) * duration / 3600.0   # Ah
        energy   = last.energy_wh
        min_v    = min(st.v_term for st in steps)
        max_t    = max(st.temp_k for st in steps)

        results.append({
            "c_rate":       round(float(cr), 4),
            "current_a":    round(I, 4),
            "duration_s":   round(duration, 2),
            "capacity_ah":  round(capacity, 4),
            "energy_wh":    round(energy, 4),
            "min_v_term":   round(min_v, 4),
            "max_temp_k":   round(max_t, 4),
            "final_omega":  last.omega_battery,
            "final_verdict": last.verdict,
        })
    return results


def sweep_soh(
    params: ECMParams,
    soh_range: List[float],
    current_a: Optional[float] = None,
    dt_s: float = 1.0,
    n_steps: int = 7200,
) -> List[Dict[str, Any]]:
    """SOH 스윕 → 노화에 따른 방전 성능 변화.

    Returns
    -------
    List of {soh, current_a, duration_s, capacity_ah,
              energy_wh, min_v_term, final_omega, final_verdict}
    """
    import dataclasses
    I = float(current_a) if current_a is not None else params.q_ah * 1.0   # 1C
    results = []
    for soh in soh_range:
        p = dataclasses.replace(params, soh=max(0.01, min(1.0, float(soh))))
        steps = simulate_discharge(p, current_a=I, dt_s=dt_s, n_steps=n_steps)
        if not steps:
            continue
        last = steps[-1]
        cap  = abs(I) * last.t_s / 3600.0
        results.append({
            "soh":           round(float(soh), 4),
            "current_a":     round(I, 4),
            "duration_s":    round(last.t_s, 2),
            "capacity_ah":   round(cap, 4),
            "energy_wh":     round(last.energy_wh, 4),
            "min_v_term":    round(min(st.v_term for st in steps), 4),
            "final_omega":   last.omega_battery,
            "final_verdict": last.verdict,
        })
    return results


def sweep_temperature(
    params: ECMParams,
    T_range: List[float],
    current_a: Optional[float] = None,
    dt_s: float = 1.0,
    n_steps: int = 7200,
) -> List[Dict[str, Any]]:
    """주변 온도 스윕 → 온도 의존 방전 성능.

    Returns
    -------
    List of {T_k, T_c, current_a, duration_s, capacity_ah,
              energy_wh, min_v_term, max_temp_k, final_omega, final_verdict}
    """
    import dataclasses
    I = float(current_a) if current_a is not None else params.q_ah * 1.0
    results = []
    for T_k in T_range:
        p = dataclasses.replace(params, t_amb_k=float(T_k))
        steps = simulate_discharge(p, current_a=I, dt_s=dt_s, n_steps=n_steps,
                                   temp_init_k=float(T_k))
        if not steps:
            continue
        last = steps[-1]
        cap  = abs(I) * last.t_s / 3600.0
        results.append({
            "T_k":           round(float(T_k), 2),
            "T_c":           round(float(T_k) - 273.15, 2),
            "current_a":     round(I, 4),
            "duration_s":    round(last.t_s, 2),
            "capacity_ah":   round(cap, 4),
            "energy_wh":     round(last.energy_wh, 4),
            "min_v_term":    round(min(st.v_term for st in steps), 4),
            "max_temp_k":    round(max(st.temp_k for st in steps), 4),
            "final_omega":   last.omega_battery,
            "final_verdict": last.verdict,
        })
    return results


def sweep_soc_snapshot(
    params: ECMParams,
    soc_range: List[float],
    current_a: float = 1.0,
) -> List[Dict[str, Any]]:
    """SOC 스냅샷 스윕 → 각 SOC에서 순간 Ω·전압·전력 평가.

    배터리 방전 궤적의 '스냅샷' 분석.
    각 SOC에서 정상상태 V_RC = I·R1 근사.

    Returns
    -------
    List of {soc, v_term, omega_battery, verdict, power_w,
              flags, power_limited}
    """
    I  = float(current_a)
    results = []
    for soc in soc_range:
        soc_c  = max(0.0, min(1.0, float(soc)))
        v_rc_ss = I * params.r1_ohm              # 정상상태 분극 근사
        s = BatteryState(soc=soc_c, v_rc=v_rc_ss,
                         temp_k=params.t_amb_k, t_s=0.0)
        vt  = terminal_voltage(s, I, params)
        obs = observe_battery(s, I, params)
        pw  = abs(I) * max(0.0, vt)
        results.append({
            "soc":           round(soc_c, 4),
            "v_term":        round(vt, 4),
            "power_w":       round(pw, 4),
            "omega_battery": obs.omega_battery,
            "verdict":       obs.verdict,
            "flags":         obs.flags,
            "power_limited": obs.power_limited,
        })
    return results


# ══════════════════════════════════════════════════════════════════════════════
# 검증
# ══════════════════════════════════════════════════════════════════════════════

def verify_battery(
    state: BatteryState,
    params: ECMParams,
    current_a: float = 0.0,
) -> VerificationReport:
    """배터리 상태 정적 검증 → PASS / MARGINAL / FAIL.

    판정 기준
    ---------
    FAIL   : Ω < 0.30, 또는 critical_soc / thermal_critical / discharge_cutoff 플래그
    MARGINAL: 0.30 ≤ Ω < 0.60, 또는 low_soc / thermal_warning / aging_critical
    PASS   : Ω ≥ 0.60, 경고 플래그 없음

    Args
    ----
    state     : 검증할 배터리 상태.
    params    : ECM 파라미터.
    current_a : 현재 전류 (Ω 계산용, 기본=정지).

    Returns
    -------
    VerificationReport.
    """
    obs  = observe_battery(state, current_a, params)
    vt   = terminal_voltage(state, current_a, params)
    notes: List[str] = []
    flags = obs.flags

    fail_flags    = {"critical_soc", "thermal_critical", "discharge_cutoff"}
    marginal_flags = {"low_soc", "thermal_warning", "aging_critical",
                      "aging_warning", "high_impedance", "voltage_low"}

    has_fail     = bool(set(flags) & fail_flags)
    has_marginal = bool(set(flags) & marginal_flags)

    if has_fail or obs.omega_battery < 0.30:
        verdict = "FAIL"
        notes.append(f"Ω={obs.omega_battery:.3f} (< 0.30 또는 치명 플래그 활성)")
        for f in flags:
            if f in fail_flags:
                notes.append(f"  ✗ {f}")
    elif has_marginal or obs.omega_battery < 0.60:
        verdict = "MARGINAL"
        notes.append(f"Ω={obs.omega_battery:.3f} (경고 구간)")
        for f in flags:
            if f in marginal_flags:
                notes.append(f"  ⚠ {f}")
    else:
        verdict = "PASS"
        notes.append(f"Ω={obs.omega_battery:.3f} — 정상 운용 범위")

    # 추가 상세 메모
    notes.append(f"SOC={state.soc:.3f}  Vterm={vt:.3f}V  SOH={params.soh:.2f}")
    notes.append(f"T={state.temp_k - 273.15:.1f}°C  R0={params.r0_ohm*1000:.1f}mΩ")

    return VerificationReport(
        verdict       = verdict,
        soc           = round(state.soc, 4),
        v_term        = round(vt, 4),
        omega_battery = obs.omega_battery,
        notes         = notes,
        flags         = flags,
    )


# ══════════════════════════════════════════════════════════════════════════════
# 시나리오 시뮬레이션
# ══════════════════════════════════════════════════════════════════════════════

def scenario_fast_discharge_collapse(
    params: ECMParams,
    c_rate_range: Optional[List[float]] = None,
    dt_s: float = 0.5,
    n_steps: int = 14400,
) -> Dict[str, Any]:
    """고C-rate 방전 → 전압 붕괴 임계 탐색.

    C-rate를 순차 증가시키며 방전 지속시간·최저전압·에너지 변화를
    추적하고, 전압 붕괴(V_term < t_cutoff_v 즉시 도달)가 시작되는
    임계 C-rate를 탐색합니다.

    Returns
    -------
    {
      "per_c_rate": [...],
      "collapse_c_rate": float | None,   # 방전 즉시 종지되는 C-rate
      "usable_c_rate_max": float | None, # duration > 60s 유지 최대 C-rate
      "summary": str,
    }
    """
    if c_rate_range is None:
        c_rate_range = [0.2, 0.5, 1.0, 2.0, 3.0, 5.0, 8.0, 10.0]

    per_cr = sweep_c_rate(params, c_rate_range, dt_s=dt_s, n_steps=n_steps)

    collapse_cr   = None
    usable_cr_max = None

    for row in per_cr:
        dur = row["duration_s"]
        cr  = row["c_rate"]
        if dur <= dt_s * 2 and collapse_cr is None:
            collapse_cr = cr
        if dur > 60.0:
            usable_cr_max = cr

    parts = []
    if collapse_cr is not None:
        parts.append(f"전압 붕괴 임계: {collapse_cr}C (방전 즉시 종지)")
    else:
        parts.append(f"테스트 범위 내 전압 붕괴 없음 (최대 {max(c_rate_range):.1f}C)")
    if usable_cr_max is not None:
        parts.append(f"60s 이상 지속 최대 C-rate: {usable_cr_max}C")

    return {
        "per_c_rate":        per_cr,
        "collapse_c_rate":   collapse_cr,
        "usable_c_rate_max": usable_cr_max,
        "summary":           " | ".join(parts),
    }


def scenario_thermal_stress(
    params: ECMParams,
    T_range: Optional[List[float]] = None,
    current_a: Optional[float] = None,
    dt_s: float = 1.0,
    n_steps: int = 7200,
) -> Dict[str, Any]:
    """온도 스트레스 시뮬레이션 → 열 폭주 위험 분석.

    다양한 주변 온도에서 방전 수행 후:
    - 최고 셀 온도 추적
    - FRAGILE/CRITICAL 판정 온도 탐색
    - thermal_critical 플래그 활성화 시점 탐색

    Returns
    -------
    {
      "per_temperature": [...],
      "thermal_warn_T_k": float | None,   # thermal_warning 첫 온도 [K]
      "thermal_collapse_T_k": float | None, # CRITICAL 첫 온도 [K]
      "safe_T_max_k": float | None,        # HEALTHY 유지 최대 온도 [K]
      "summary": str,
    }
    """
    if T_range is None:
        T_range = [273.15, 283.15, 298.15, 308.15, 318.15, 328.15, 338.15, 348.15]

    I = float(current_a) if current_a is not None else params.q_ah * 1.0
    per_T = sweep_temperature(params, T_range, current_a=I, dt_s=dt_s, n_steps=n_steps)

    thermal_warn_T  = None
    thermal_coll_T  = None
    safe_T_max      = None

    # 각 온도 시뮬레이션에서 플래그 재확인
    import dataclasses
    per_result = []
    for row, T_k in zip(per_T, T_range):
        p_t = dataclasses.replace(params, t_amb_k=float(T_k))
        steps = simulate_discharge(p_t, current_a=I, dt_s=dt_s, n_steps=n_steps,
                                   temp_init_k=float(T_k))
        thermal_flagged = any(
            "thermal_critical" in st.verdict or "thermal_critical" in []
            for st in steps
        )
        # 최고 온도에서 관측
        peak_step = max(steps, key=lambda s: s.temp_k) if steps else None
        thermal_flag_active = False
        if peak_step:
            s_peak = BatteryState(
                soc=peak_step.soc, v_rc=peak_step.v_rc,
                temp_k=peak_step.temp_k, t_s=peak_step.t_s,
            )
            obs_peak = observe_battery(s_peak, I, p_t)
            thermal_flag_active = "thermal_critical" in obs_peak.flags

        r = dict(row)
        r["thermal_flag_active"] = thermal_flag_active
        per_result.append(r)

        if thermal_flag_active and thermal_coll_T is None:
            thermal_coll_T = T_k
        if row["final_verdict"] in ("FRAGILE", "CRITICAL") and thermal_warn_T is None:
            thermal_warn_T = T_k
        if row["final_verdict"] in ("HEALTHY", "STABLE"):
            safe_T_max = T_k

    parts = []
    if thermal_coll_T is not None:
        parts.append(f"열 위험 임계: {thermal_coll_T - 273.15:.1f}°C ({thermal_coll_T:.1f}K)")
    else:
        parts.append(f"테스트 범위 열 위험 없음 (최대 {max(T_range) - 273.15:.1f}°C)")
    if safe_T_max is not None:
        parts.append(f"HEALTHY/STABLE 유지 최대: {safe_T_max - 273.15:.1f}°C")

    return {
        "per_temperature":       per_result,
        "thermal_warn_T_k":      thermal_warn_T,
        "thermal_collapse_T_k":  thermal_coll_T,
        "safe_T_max_k":          safe_T_max,
        "summary":               " | ".join(parts),
    }


def _soh_3phase(
    n: int,
    sei_coeff: float,
    n_knee1: int,
    linear_rate: float,
    n_knee2: int,
    accel_rate: float,
    soh_floor: float,
) -> float:
    """3단계 SOH 감쇠 모델: SEI 형성 → 선형 → 무릎 후 가속."""
    if n <= 0:
        return 1.0
    if n <= n_knee1:
        soh = 1.0 - sei_coeff * math.sqrt(float(n))
    elif n <= n_knee2:
        soh_k1 = 1.0 - sei_coeff * math.sqrt(float(n_knee1))
        soh    = soh_k1 - linear_rate * (n - n_knee1)
    else:
        soh_k1 = 1.0 - sei_coeff * math.sqrt(float(n_knee1))
        soh_k2 = soh_k1 - linear_rate * (n_knee2 - n_knee1)
        soh    = soh_k2 - accel_rate * (n - n_knee2)
    return max(float(soh_floor), soh)


def scenario_aging_capacity_fade(
    params: ECMParams,
    cycle_range: Optional[List[int]] = None,
    # v0.2 호환 선형 파라미터 (3단계 모드가 우선)
    capacity_fade_per_cycle: float = 2e-4,
    resistance_rise_per_cycle: float = 5e-5,
    # v0.3.0 3단계 노화 모델 파라미터
    use_3phase: bool = True,
    sei_coeff: float = 0.0015,         # Phase 1: SEI sqrt(n) 계수
    n_knee1: int = 200,                # Phase 1 종료 사이클
    linear_rate: float = 1.5e-4,      # Phase 2: 선형 감쇠율 [/cycle]
    n_knee2: int = 800,               # Phase 3 시작 (무릎점)
    accel_rate: float = 6e-4,         # Phase 3: 가속 감쇠율 [/cycle]
    soh_floor: float = 0.40,          # SOH 하한
    current_a: Optional[float] = None,
    dt_s: float = 1.0,
    n_steps: int = 7200,
) -> Dict[str, Any]:
    """사이클 노화 → 용량 감쇠 궤적 시뮬레이션 (3단계 모델).

    use_3phase=True (기본):
      Phase 1 (SEI 형성, 0~n_knee1): SOH = 1 − sei_coeff × √n  [초기 빠른 감쇠]
      Phase 2 (선형 중기, n_knee1~n_knee2): SOH = SOH_k1 − linear_rate × Δn
      Phase 3 (무릎 후 가속, n_knee2~): SOH = SOH_k2 − accel_rate × Δn

    use_3phase=False: v0.2 호환 선형 모델 (capacity_fade_per_cycle 사용).

    Args
    ----
    cycle_range  : 시뮬레이션할 사이클 수 목록.
    use_3phase   : True → 3단계 모델 (기본), False → 선형 (v0.2 호환).
    sei_coeff    : Phase 1 SEI 계수 (기본 0.0015 → 200cy에서 SOH≈97.9%).
    n_knee1      : SEI 안정화 사이클 (기본 200cy).
    linear_rate  : Phase 2 사이클당 SOH 감소 (기본 1.5e-4/cy).
    n_knee2      : 무릎점 사이클 (기본 800cy, NMC 대표값).
    accel_rate   : Phase 3 가속 감쇠율 (기본 6e-4/cy).
    soh_floor    : SOH 하한 클램프 (기본 0.40).

    Returns
    -------
    {
      "per_cycle": [{cycle, soh, r0_ohm, capacity_ah, energy_wh,
                     final_omega, final_verdict, phase}, ...],
      "eol_cycle": int | None,          # SOH < 0.80 첫 사이클
      "eol_strict_cycle": int | None,   # SOH < 0.70
      "knee_cycle": int | None,         # n_knee2 (3단계 모드)
      "summary": str,
    }
    """
    import dataclasses

    if cycle_range is None:
        cycle_range = [0, 50, 100, 200, 300, 400, 500, 600, 800, 1000, 1200, 1500, 2000]

    I    = float(current_a) if current_a is not None else params.q_ah * 1.0
    r0_0 = params.r0_ohm

    per_cycle = []
    eol_cycle        = None
    eol_strict_cycle = None

    for n in cycle_range:
        # SOH 계산
        if use_3phase:
            soh_n = _soh_3phase(int(n), sei_coeff, n_knee1, linear_rate,
                                n_knee2, accel_rate, soh_floor)
            # 단계 레이블
            if n <= n_knee1:
                age_phase = "SEI"
            elif n <= n_knee2:
                age_phase = "LINEAR"
            else:
                age_phase = "POST_KNEE"
        else:
            soh_n     = max(soh_floor, 1.0 - n * float(capacity_fade_per_cycle))
            age_phase = "LINEAR"

        # R0 상승 (선형, 두 모드 공통)
        r0_n = r0_0 * (1.0 + n * float(resistance_rise_per_cycle))
        p_n  = dataclasses.replace(params, soh=soh_n, r0_ohm=r0_n)

        steps = simulate_discharge(p_n, current_a=I, dt_s=dt_s, n_steps=n_steps)
        if not steps:
            continue

        last = steps[-1]
        cap  = abs(I) * last.t_s / 3600.0

        per_cycle.append({
            "cycle":         int(n),
            "soh":           round(soh_n, 4),
            "r0_ohm":        round(r0_n, 6),
            "capacity_ah":   round(cap, 4),
            "energy_wh":     round(last.energy_wh, 4),
            "final_omega":   last.omega_battery,
            "final_verdict": last.verdict,
            "phase":         age_phase,
        })

        if soh_n < 0.80 and eol_cycle is None:
            eol_cycle = int(n)
        if soh_n < 0.70 and eol_strict_cycle is None:
            eol_strict_cycle = int(n)

    parts = []
    if use_3phase:
        parts.append(f"3단계 노화 모델 (무릎점 {n_knee2}cy)")
    if eol_cycle is not None:
        parts.append(f"EOL (SOH<80%): {eol_cycle}사이클")
    else:
        parts.append(f"테스트 범위 내 SOH≥80% 유지")
    if eol_strict_cycle is not None:
        parts.append(f"EOL 엄격 (SOH<70%): {eol_strict_cycle}사이클")
    if per_cycle:
        last_row = per_cycle[-1]
        parts.append(
            f"최종 용량: {last_row['capacity_ah']:.2f}Ah "
            f"(초기 {params.q_ah:.1f}Ah 대비 "
            f"{last_row['capacity_ah']/params.q_ah*100:.1f}%)"
        )

    return {
        "per_cycle":          per_cycle,
        "eol_cycle":          eol_cycle,
        "eol_strict_cycle":   eol_strict_cycle,
        "knee_cycle":         n_knee2 if use_3phase else None,
        "summary":            " | ".join(parts),
    }

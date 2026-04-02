"""배터리 ECM 물리 코어.

v0.3.0 확장
───────────
  OCV       : ocv_linear (선형, v0.2 호환) + ocv (table dispatch) + d_ocv_d_soc
  저항       : r_at_temperature (Arrhenius R(T))
  step_ecm  : 1RC → 2RC 자동 전환 + Arrhenius R(T) 적용
  단자전압  : terminal_voltage — 2RC + OCV table 반영
  유틸리티  : c_rate, effective_capacity_ah, internal_resistance_total,
              voltage_drop_at_current, time_to_discharge, soc_at_time,
              thermal_time_constant, steady_state_temperature,
              max_continuous_current, power_capability

부호 규약: I > 0 = 방전, I < 0 = 충전
"""

from __future__ import annotations

import math
from typing import List, Optional, Tuple

from .schema import BatteryState, ECMParams

_KB_EV = 8.617333e-5   # Boltzmann 상수 [eV/K]


# ══════════════════════════════════════════════════════════════════════════════
# OCV 함수
# ══════════════════════════════════════════════════════════════════════════════

def ocv_linear(soc: float, p: ECMParams) -> float:
    """SOC → 개회로 전압 (선형 근사, v0.2 호환).

    OCV(z) = soc_v0 + soc_ocv_v_per_unit × clamp(z, 0, 1)
    """
    s = max(0.0, min(1.0, float(soc)))
    return p.soc_v0 + p.soc_ocv_v_per_unit * s


def _ocv_interp(soc: float, table: List[Tuple[float, float]]) -> float:
    """구간선형 OCV lookup.

    table: [(soc₀, v₀), …, (soc_n, v_n)] — soc 오름차순 정렬.
    """
    s = max(0.0, min(1.0, float(soc)))
    if s <= table[0][0]:
        return table[0][1]
    if s >= table[-1][0]:
        return table[-1][1]
    for i in range(len(table) - 1):
        s0, v0 = table[i]
        s1, v1 = table[i + 1]
        if s0 <= s <= s1:
            t = (s - s0) / max(1e-12, s1 - s0)
            return v0 + t * (v1 - v0)
    return table[-1][1]


def ocv(soc: float, p: ECMParams) -> float:
    """SOC → OCV. table이 있으면 구간선형 lookup, 없으면 선형 근사.

    >>> ocv(0.5, ECMParams()) == ocv_linear(0.5, ECMParams())
    True
    """
    if p.ocv_table is not None:
        return _ocv_interp(soc, p.ocv_table)
    return ocv_linear(soc, p)


def d_ocv_d_soc(soc: float, p: ECMParams, eps: float = 1e-4) -> float:
    """OCV의 SOC에 대한 수치 기울기 [V/SOC] (EKF Jacobian 용).

    중심차분: (OCV(z+ε) − OCV(z−ε)) / 2ε
    """
    hi = ocv(min(1.0, soc + eps), p)
    lo = ocv(max(0.0, soc - eps), p)
    return (hi - lo) / (2 * eps)


def ocv_at_soc(soc: float, p: ECMParams) -> float:
    """ocv()의 가독성 alias."""
    return ocv(soc, p)


# ══════════════════════════════════════════════════════════════════════════════
# Arrhenius 온도 의존 저항
# ══════════════════════════════════════════════════════════════════════════════

def r_at_temperature(r_ref: float, T_k: float, p: ECMParams) -> float:
    """Arrhenius 온도 의존 저항 [Ω].

    R(T) = R_ref · exp(Ea_r / kB · (1/T − 1/T_ref))

    Ea_r_ev = 0 → R = R_ref (온도 불변, v0.2 호환).
    저온에서 R0 급등, 고온에서 감소하는 실측 거동 반영.
    """
    if p.Ea_r_ev == 0.0:
        return float(r_ref)
    factor = math.exp(p.Ea_r_ev / _KB_EV * (1.0 / max(1.0, T_k) - 1.0 / max(1.0, p.T_ref_k)))
    return float(r_ref) * factor


# ══════════════════════════════════════════════════════════════════════════════
# ECM 적분 (1RC / 2RC 자동 전환)
# ══════════════════════════════════════════════════════════════════════════════

def terminal_voltage(s: BatteryState, I_a: float, p: ECMParams) -> float:
    """단자전압 [V].

    V_term = OCV(SOC) − I·R0(T) − V_RC1 − V_RC2
    """
    R0 = r_at_temperature(p.r0_ohm, s.temp_k, p)
    return ocv(s.soc, p) - float(I_a) * R0 - s.v_rc - s.v_rc2


def step_ecm(
    s: BatteryState,
    I_a: float,
    dt_s: float,
    p: ECMParams,
) -> BatteryState:
    """오일러 1스텝 ECM 적분 (1RC / 2RC 자동 전환, Arrhenius R(T) 적용).

    I > 0 = 방전, I < 0 = 충전.

    1RC 모드: p.r2_ohm == 0 (기본, v0.2 호환)
    2RC 모드: p.r2_ohm > 0 and p.c2_farad > 0

    Returns
    -------
    새 BatteryState (soc, v_rc, v_rc2, temp_k, t_s 갱신).
    """
    dt = max(0.0, float(dt_s))
    I  = float(I_a)

    # SOC
    q_eff = max(1e-9, p.q_ah * 3600.0 * max(0.01, p.soh))
    soc   = max(0.0, min(1.0, s.soc - (I / q_eff) * dt))

    # RC1 분극
    tau1  = max(1e-9, p.r1_ohm * p.c1_farad)
    v_rc1 = s.v_rc + dt * (-s.v_rc / tau1 + I / max(1e-9, p.c1_farad))

    # RC2 분극 (2RC 모드)
    if p.r2_ohm > 0.0 and p.c2_farad > 0.0:
        tau2  = max(1e-9, p.r2_ohm * p.c2_farad)
        v_rc2 = s.v_rc2 + dt * (-s.v_rc2 / tau2 + I / max(1e-9, p.c2_farad))
    else:
        v_rc2 = s.v_rc2

    # 열 proxy (Arrhenius R0 반영)
    R0    = r_at_temperature(p.r0_ohm, s.temp_k, p)
    r_tot = R0 + p.r1_ohm
    p_heat = I * I * r_tot
    c_th   = max(1e-6, p.thermal_c_j_per_k)
    h      = max(1e-9, p.thermal_h_w_per_k)
    t_k    = s.temp_k + dt * (p_heat - h * (s.temp_k - p.t_amb_k)) / c_th

    return BatteryState(
        soc    = soc,
        v_rc   = v_rc1,
        v_rc2  = v_rc2,
        temp_k = t_k,
        t_s    = s.t_s + dt,
    )


# ══════════════════════════════════════════════════════════════════════════════
# 파생·유틸리티 함수 (v0.2 API 유지)
# ══════════════════════════════════════════════════════════════════════════════

def c_rate(current_a: float, p: ECMParams) -> float:
    """전류 → C-rate 배수."""
    return abs(float(current_a)) / max(1e-9, p.q_ah)


def effective_capacity_ah(p: ECMParams) -> float:
    """SOH 반영 실효 용량 [Ah]."""
    return p.q_ah * max(0.01, p.soh)


def internal_resistance_total(p: ECMParams) -> float:
    """R_total = R0 + R1 (+ R2) [Ω]."""
    return p.r0_ohm + p.r1_ohm + p.r2_ohm


def voltage_drop_at_current(current_a: float, p: ECMParams) -> float:
    """정상상태 전압 강하: ΔV = I·(R0+R1+R2) [V]."""
    return abs(float(current_a)) * internal_resistance_total(p)


def time_to_discharge(
    p: ECMParams,
    current_a: float,
    soc_init: float = 1.0,
    soc_target: float = 0.0,
) -> float:
    """선형 근사 방전 시간 [s]."""
    delta_soc = max(0.0, float(soc_init) - max(0.0, float(soc_target)))
    q_eff = effective_capacity_ah(p) * 3600.0
    return delta_soc * q_eff / max(1e-9, abs(float(current_a)))


def soc_at_time(
    t_s: float,
    current_a: float,
    p: ECMParams,
    soc_init: float = 1.0,
) -> float:
    """선형 근사 SOC(t): clamp(z0 − I·t / Q_eff, 0, 1)."""
    q_eff = effective_capacity_ah(p) * 3600.0
    return max(0.0, min(1.0, float(soc_init) - abs(float(current_a)) * float(t_s) / q_eff))


def thermal_time_constant(p: ECMParams) -> float:
    """열 시정수 τ_th = C_th / h [s]."""
    return max(1e-9, p.thermal_c_j_per_k) / max(1e-9, p.thermal_h_w_per_k)


def steady_state_temperature(current_a: float, p: ECMParams) -> float:
    """정상상태 셀 온도 T_ss = T_amb + I²·R_total / h [K]."""
    r_tot  = internal_resistance_total(p)
    p_heat = float(current_a) ** 2 * r_tot
    return p.t_amb_k + p_heat / max(1e-9, p.thermal_h_w_per_k)


def max_continuous_current(p: ECMParams, t_max_k: float = 333.15) -> float:
    """온도 제한 기반 최대 연속 전류 [A]."""
    delta_t = max(0.0, t_max_k - p.t_amb_k)
    r_tot   = max(1e-9, internal_resistance_total(p))
    h       = max(1e-9, p.thermal_h_w_per_k)
    return math.sqrt(delta_t * h / r_tot)


def power_capability(s: BatteryState, p: ECMParams) -> float:
    """순시 전력 공급 능력 추정 [W] (단기, V_RC ≈ 현재값 유지 가정)."""
    ocv_v = ocv(s.soc, p)
    R0    = r_at_temperature(p.r0_ohm, s.temp_k, p)
    i_max = (ocv_v - s.v_rc - s.v_rc2 - p.t_cutoff_v) / max(1e-9, R0)
    i_max = max(0.0, i_max)
    v_at  = ocv_v - i_max * R0 - s.v_rc - s.v_rc2
    return i_max * max(0.0, v_at)

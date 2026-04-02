"""Ω_battery 5레이어 관측 시스템.

5레이어 Ω 아키텍처
──────────────────
  Ω_soc        0.30 — SOC 잔량 건강도
  Ω_voltage    0.25 — 단자전압 마진 건강도
  Ω_thermal    0.20 — 온도 상태 건강도
  Ω_impedance  0.15 — 내부저항 열화 건강도
  Ω_aging      0.10 — SOH 수명 건강도

  Ω_battery = 0.30·Ω_soc + 0.25·Ω_voltage + 0.20·Ω_thermal
             + 0.15·Ω_impedance + 0.10·Ω_aging

판정 기준
─────────
  HEALTHY  : Ω ≥ 0.75
  STABLE   : Ω ≥ 0.52
  FRAGILE  : Ω ≥ 0.30
  CRITICAL : Ω < 0.30

플래그 (11개)
─────────────
  low_soc             / critical_soc
  thermal_warning     / thermal_critical
  high_impedance      / impedance_degraded
  aging_warning       / aging_critical
  voltage_low         / power_limited
  discharge_cutoff
"""

from __future__ import annotations

from typing import List
from .ecm import ocv_linear, ocv, terminal_voltage, internal_resistance_total
from .schema import BatteryObservation, BatteryState, ECMParams


# ══════════════════════════════════════════════════════════════════════════════
# 판정 임계값
# ══════════════════════════════════════════════════════════════════════════════

_VERDICTS = [
    (0.75, "HEALTHY"),
    (0.52, "STABLE"),
    (0.30, "FRAGILE"),
]

# 레이어 가중치
_W_SOC   = 0.30
_W_VOLT  = 0.25
_W_THERM = 0.20
_W_IMP   = 0.15
_W_AGING = 0.10


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


# ══════════════════════════════════════════════════════════════════════════════
# 레이어별 Ω 계산
# ══════════════════════════════════════════════════════════════════════════════

def _omega_soc(soc: float, soc_floor: float = 0.10, soc_warn: float = 0.20) -> float:
    """Ω_soc — SOC 잔량 건강도.

    SOC ≥ soc_warn → 1.0 (정상)
    soc_floor ≤ SOC < soc_warn → 선형 감소
    SOC < soc_floor → 0 (위험)
    """
    if soc >= soc_warn:
        return 1.0
    if soc <= soc_floor:
        return 0.0
    return (soc - soc_floor) / max(1e-9, soc_warn - soc_floor)


def _omega_voltage(v_term: float, v_cutoff: float, v_nominal: float) -> float:
    """Ω_voltage — 단자전압 마진 건강도.

    V ≥ v_nominal → 1.0
    v_cutoff < V < v_nominal → 선형 스케일
    V ≤ v_cutoff → 0.0
    """
    if v_term >= v_nominal:
        return 1.0
    if v_term <= v_cutoff:
        return 0.0
    return (v_term - v_cutoff) / max(1e-9, v_nominal - v_cutoff)


def _omega_thermal(
    temp_k: float,
    t_amb_k: float,
    t_warn_k: float = 318.15,   # 45°C
    t_crit_k: float = 333.15,   # 60°C
    t_low_k:  float = 268.15,   # −5°C
) -> float:
    """Ω_thermal — 온도 상태 건강도.

    온도가 [t_low, t_warn] 범위 내 → 1.0
    t_warn ~ t_crit → 선형 감소
    > t_crit or < t_low → 0.0
    """
    if temp_k < t_low_k:
        # 저온: t_low 아래 → 0
        return max(0.0, (temp_k - (t_low_k - 20.0)) / 20.0)
    if temp_k <= t_warn_k:
        return 1.0
    if temp_k >= t_crit_k:
        return 0.0
    return (t_crit_k - temp_k) / max(1e-9, t_crit_k - t_warn_k)


def _omega_impedance(p: ECMParams, r_ref_factor: float = 3.0) -> float:
    """Ω_impedance — 내부저항 열화 건강도.

    SOH 기반 + R0 절대값 기준 이중 평가.
    r_ref_factor: 신품 대비 허용 최대 배율 (기본 3×).
    """
    # SOH 기반 (SOH=1 → 1.0, SOH=0.5 → 0.0 선형)
    soh_pen  = _clamp01((p.soh - 0.5) / 0.5)

    # R0 절대값 기반: R0 ≤ 0.1Ω → 1.0, R0 ≥ r_ref_factor×0.1 → 0.0
    r_thresh = 0.10 * r_ref_factor
    r_pen    = _clamp01(1.0 - (p.r0_ohm - 0.10) / max(1e-9, r_thresh - 0.10))

    return 0.60 * soh_pen + 0.40 * r_pen


def _omega_aging(p: ECMParams) -> float:
    """Ω_aging — SOH 기반 수명 건강도.

    SOH → [0, 1] 선형 매핑.
    """
    return _clamp01(p.soh)


# ══════════════════════════════════════════════════════════════════════════════
# 플래그 판정
# ══════════════════════════════════════════════════════════════════════════════

def _compute_flags(
    s: BatteryState,
    I_a: float,
    p: ECMParams,
    vt: float,
    *,
    soc_floor: float,
    soc_warn: float,
    t_warn_k: float,
    t_crit_k: float,
    t_low_k: float,
) -> List[str]:
    flags: List[str] = []

    # SOC
    if s.soc <= soc_floor:
        flags.append("critical_soc")
    elif s.soc <= soc_warn:
        flags.append("low_soc")

    # 전압
    if vt <= p.t_cutoff_v:
        flags.append("discharge_cutoff")
    elif vt <= p.t_cutoff_v * 1.05:
        flags.append("voltage_low")

    # 온도
    if s.temp_k >= t_crit_k:
        flags.append("thermal_critical")
    elif s.temp_k >= t_warn_k:
        flags.append("thermal_warning")
    if s.temp_k < t_low_k:
        flags.append("thermal_warning")  # 저온도 경고

    # 임피던스/노화
    if p.soh < 0.70:
        flags.append("aging_critical")
    elif p.soh < 0.80:
        flags.append("aging_warning")

    if p.r0_ohm > 0.20:
        flags.append("high_impedance")
    elif p.r0_ohm > 0.12:
        flags.append("impedance_degraded")

    # 전력 제한
    if s.soc <= soc_warn * 1.15 or s.temp_k >= t_warn_k or vt <= p.t_cutoff_v * 1.08:
        flags.append("power_limited")

    # 중복 제거 (순서 유지)
    seen = set()
    deduped = []
    for f in flags:
        if f not in seen:
            seen.add(f)
            deduped.append(f)
    return deduped


# ══════════════════════════════════════════════════════════════════════════════
# 메인 Observer API
# ══════════════════════════════════════════════════════════════════════════════

def observe_battery(
    s: BatteryState,
    I_a: float,
    p: ECMParams,
    *,
    soc_floor: float   = 0.10,
    soc_warn:  float   = 0.20,
    t_warn_k:  float   = 318.15,
    t_crit_k:  float   = 333.15,
    t_low_k:   float   = 268.15,
) -> BatteryObservation:
    """Ω 5레이어 관측.

    Args
    ----
    s         : 현재 배터리 상태.
    I_a       : 방전 전류 [A] (양수=방전).
    p         : ECM 파라미터.
    soc_floor : SOC 위험 임계 (기본 10%).
    soc_warn  : SOC 주의 임계 (기본 20%).
    t_warn_k  : 온도 경고 임계 [K] (기본 45°C).
    t_crit_k  : 온도 위험 임계 [K] (기본 60°C).
    t_low_k   : 저온 임계 [K] (기본 −5°C).

    Returns
    -------
    BatteryObservation — Ω 5레이어 + 판정 + 플래그.
    """
    vt = terminal_voltage(s, I_a, p)

    # 5레이어 Ω 계산
    v_nominal = ocv(0.50, p)
    o_soc  = _omega_soc(s.soc, soc_floor, soc_warn)
    o_volt = _omega_voltage(vt, p.t_cutoff_v, v_nominal)
    o_therm= _omega_thermal(s.temp_k, p.t_amb_k, t_warn_k, t_crit_k, t_low_k)
    o_imp  = _omega_impedance(p)
    o_age  = _omega_aging(p)

    omega = _clamp01(
        _W_SOC   * o_soc
        + _W_VOLT  * o_volt
        + _W_THERM * o_therm
        + _W_IMP   * o_imp
        + _W_AGING * o_age
    )

    # 강제 임계 — 위험 조건에서 Ω 상한 적용
    if "critical_soc" in _compute_flags(s, I_a, p, vt,
            soc_floor=soc_floor, soc_warn=soc_warn,
            t_warn_k=t_warn_k, t_crit_k=t_crit_k, t_low_k=t_low_k):
        omega = min(omega, 0.29)   # → CRITICAL
    elif "thermal_critical" in _compute_flags(s, I_a, p, vt,
            soc_floor=soc_floor, soc_warn=soc_warn,
            t_warn_k=t_warn_k, t_crit_k=t_crit_k, t_low_k=t_low_k):
        omega = min(omega, 0.29)

    # 판정
    verdict = "CRITICAL"
    for thr, v in _VERDICTS:
        if omega >= thr:
            verdict = v
            break

    # 플래그
    flags = _compute_flags(
        s, I_a, p, vt,
        soc_floor=soc_floor, soc_warn=soc_warn,
        t_warn_k=t_warn_k, t_crit_k=t_crit_k, t_low_k=t_low_k,
    )

    power_limited = "power_limited" in flags
    notes = (
        f"Vterm={vt:.3f}V | SOC={s.soc:.3f} | "
        f"T={s.temp_k - 273.15:.1f}°C | SOH={p.soh:.2f}"
    )

    return BatteryObservation(
        omega_soc       = round(o_soc,   4),
        omega_voltage   = round(o_volt,  4),
        omega_thermal   = round(o_therm, 4),
        omega_impedance = round(o_imp,   4),
        omega_aging     = round(o_age,   4),
        omega_battery   = round(omega,   4),
        verdict         = verdict,
        flags           = flags,
        power_limited   = power_limited,
        notes           = notes,
    )


def diagnose(obs: BatteryObservation) -> List[str]:
    """관측 결과 → 진단 권고 메시지 리스트.

    Athena 권고 우선순위:
    1. thermal_critical       → 즉시 충전 중단, 냉각 조치
    2. critical_soc           → 즉시 부하 차단 필요
    3. discharge_cutoff       → 방전 종지 도달, 충전 필요
    4. aging_critical         → 셀 교체 권고
    5. high_impedance         → BMS 내부저항 점검
    6. aging_warning          → SOH 모니터링 강화
    7. thermal_warning        → 전류 감소 / 방열 개선
    8. low_soc                → 충전 계획 수립
    9. power_limited          → 고전력 부하 제한
    """
    flags = set(obs.flags)
    recs: List[str] = []

    if "thermal_critical" in flags:
        recs.append("[CRITICAL] 열 위험 — 즉시 충전/방전 중단, 강제 냉각 필요")
    if "critical_soc" in flags:
        recs.append("[CRITICAL] SOC 위험 수준 — 즉시 부하 차단, 과방전 방지")
    if "discharge_cutoff" in flags:
        recs.append("[WARN] 방전 종지 전압 도달 — 충전 필요")
    if "aging_critical" in flags:
        recs.append("[WARN] SOH < 70% — 셀 교체 검토")
    if "high_impedance" in flags:
        recs.append("[WARN] 내부저항 과다 — BMS 임피던스 점검")
    if "impedance_degraded" in flags and "high_impedance" not in flags:
        recs.append("[INFO] 내부저항 증가 추세 — 정기 EIS 측정 권장")
    if "aging_warning" in flags and "aging_critical" not in flags:
        recs.append("[INFO] SOH < 80% — 배터리 모니터링 강화")
    if "thermal_warning" in flags and "thermal_critical" not in flags:
        recs.append("[INFO] 온도 경고 구간 — 전류 20% 감소 또는 방열 개선")
    if "low_soc" in flags and "critical_soc" not in flags:
        recs.append("[INFO] SOC 낮음 — 충전 계획 수립 권장")
    if "power_limited" in flags:
        recs.append("[INFO] 전력 제한 상태 — 고전력 부하 감소 권장")

    if not recs:
        if obs.verdict == "HEALTHY":
            recs.append("[OK] 배터리 상태 양호 — 정상 운용 가능")
        else:
            recs.append("[OK] 이상 없음 — 모니터링 유지")

    return recs

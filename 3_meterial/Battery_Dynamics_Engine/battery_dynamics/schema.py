"""배터리 상태·파라미터·관측·검증 스키마.

v0.3.0 변경
───────────
  ECMParams   : ocv_table (OCV curve lookup) + r2_ohm/c2_farad (2RC) +
                Ea_r_ev/T_ref_k (Arrhenius R(T)) 추가
  BatteryState: v_rc2 (2nd RC 분극전압) 추가
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple


# ══════════════════════════════════════════════════════════════════════════════
# 파라미터
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class ECMParams:
    """단일 RC(or 2RC) ECM + 간략 열 proxy + OCV table + Arrhenius R(T).

    전기 모델 (1RC 기본 / 2RC 선택)
    ──────────────────────────────
      OCV(z) = table_interp(z)  if ocv_table is not None
             = soc_v0 + k_ocv·z  otherwise

      V_term = OCV − I·R0(T) − V_RC1 − V_RC2
      dz/dt  = −I / Q_eff
      dV_RC1/dt = −V_RC1/(R1·C1) + I/C1
      dV_RC2/dt = −V_RC2/(R2·C2) + I/C2   (r2_ohm > 0 일 때만)

    Arrhenius 온도 의존 저항
    ──────────────────────
      R0(T) = R0_ref · exp(Ea_r / kB · (1/T − 1/T_ref))   (Ea_r_ev > 0)
      Ea_r_ev = 0 → R0 상수 (이전 버전 호환)

    Attributes (기존)
    ─────────────────
    q_ah, r0_ohm, r1_ohm, c1_farad, soc_ocv_v_per_unit, soc_v0,
    thermal_c_j_per_k, thermal_h_w_per_k, t_amb_k, soh,
    t_cutoff_v, v_charge_max_v, label

    Attributes (v0.3.0 추가)
    ─────────────────────────
    ocv_table      : List of (soc, ocv) tuples for piecewise-linear OCV curve.
                     None → linear OCV (backward compat).
    r2_ohm         : 2nd RC 저항 [Ω]. 0.0 → 1RC mode.
    c2_farad       : 2nd RC 커패시터 [F]. 0.0 → 1RC mode.
    Ea_r_ev        : Arrhenius 활성화 에너지 [eV]. 0.0 → 상수 R.
    T_ref_k        : Arrhenius 기준 온도 [K].
    """
    # ── 기본 ECM 파라미터 (v0.1 ~ v0.2 호환)
    q_ah:               float = 5.0
    r0_ohm:             float = 0.08
    r1_ohm:             float = 0.04
    c1_farad:           float = 2000.0
    soc_ocv_v_per_unit: float = 1.0
    soc_v0:             float = 2.8
    thermal_c_j_per_k:  float = 200.0
    thermal_h_w_per_k:  float = 0.5
    t_amb_k:            float = 298.15
    soh:                float = 1.0
    t_cutoff_v:         float = 2.5
    v_charge_max_v:     float = 4.2
    label:              str   = "generic"

    # ── v0.3.0 확장 파라미터
    ocv_table: Optional[List[Tuple[float, float]]] = field(default=None)
    """OCV curve lookup table [(soc₀, ocv₀), …, (soc_n, ocv_n)].
    soc 오름차순 정렬 필요. None이면 선형 OCV 사용."""

    r2_ohm:   float = 0.0
    """2nd RC 저항 [Ω]. 0 → 1RC 모드 (v0.2 호환)."""

    c2_farad: float = 0.0
    """2nd RC 커패시터 [F]. 0 → 1RC 모드."""

    Ea_r_ev:  float = 0.0
    """Arrhenius 활성화 에너지 [eV]. 0 → 상수 저항."""

    T_ref_k:  float = 298.15
    """Arrhenius 기준 온도 [K] (R0_ref 측정 온도)."""


# ══════════════════════════════════════════════════════════════════════════════
# 동적 상태
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class BatteryState:
    """런타임 배터리 상태.

    v0.3.0: v_rc2 (2nd RC 분극전압) 추가 (기본값 0.0 → 1RC 호환).
    """
    soc:    float
    v_rc:   float           # 1st RC 분극전압 [V]
    temp_k: float
    t_s:    float = 0.0
    v_rc2:  float = 0.0     # 2nd RC 분극전압 [V] (2RC 모드 시 사용)


# ══════════════════════════════════════════════════════════════════════════════
# 시뮬레이션 스텝 결과
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class DischargeStep:
    """방전/충전 시뮬레이션 스텝 결과."""
    t_s:           float
    soc:           float
    v_term:        float
    temp_k:        float
    current_a:     float
    v_rc:          float
    c_rate:        float
    power_w:       float
    energy_wh:     float
    omega_battery: float
    verdict:       str
    terminated:    bool
    # v0.3.0
    v_rc2:         float = 0.0
    charge_phase:  str   = ""   # "CC" / "CV" / "" (방전)


# ══════════════════════════════════════════════════════════════════════════════
# Observer 관측 결과
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class BatteryObservation:
    """Ω 5레이어 관측 결과."""
    omega_soc:       float
    omega_voltage:   float
    omega_thermal:   float
    omega_impedance: float
    omega_aging:     float
    omega_battery:   float
    verdict:         str
    flags:           List[str] = field(default_factory=list)
    power_limited:   bool = False
    notes:           str = ""


# ══════════════════════════════════════════════════════════════════════════════
# 검증 보고서
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class VerificationReport:
    """배터리 상태 검증 보고서."""
    verdict:       str
    soc:           float
    v_term:        float
    omega_battery: float
    notes:         List[str] = field(default_factory=list)
    flags:         List[str] = field(default_factory=list)

"""battery_dynamics — 배터리 ECM 물리·시뮬레이션·검증 엔진.

계층 구조
─────────
  schema.py        — 데이터 모델 (ECMParams, BatteryState, DischargeStep, ...)
  ecm.py           — ECM 물리 (OCV, step_ecm, terminal_voltage, 유틸리티)
  observer.py      — Ω 5레이어 관측 + diagnose
  design_engine.py — 시뮬레이션·스윕·검증·시나리오
  estimator.py     — EKF SOC 추정기
  presets.py       — 표준 셀 프리셋 (NMC/LFP/LCO/EV)

빠른 시작
─────────
  from battery_dynamics import (
      ECMParams, BatteryState,
      simulate_discharge, observe_battery,
      NMC_18650, get_preset,
  )

  steps = simulate_discharge(NMC_18650, current_a=3.4, dt_s=1.0)
  for s in steps[::300]:
      print(f"t={s.t_s:.0f}s  SOC={s.soc:.3f}  V={s.v_term:.3f}V  Ω={s.omega_battery:.3f}")
"""

from .schema import (
    ECMParams,
    BatteryState,
    DischargeStep,
    BatteryObservation,
    VerificationReport,
)
from .ecm import (
    ocv_linear,
    ocv,
    ocv_at_soc,
    d_ocv_d_soc,
    r_at_temperature,
    terminal_voltage,
    step_ecm,
    c_rate,
    effective_capacity_ah,
    internal_resistance_total,
    voltage_drop_at_current,
    time_to_discharge,
    soc_at_time,
    thermal_time_constant,
    steady_state_temperature,
    max_continuous_current,
    power_capability,
)
from .observer import (
    observe_battery,
    diagnose,
)
from .design_engine import (
    simulate_discharge,
    simulate_charge,
    simulate_charge_cccv,
    sweep_c_rate,
    sweep_soh,
    sweep_temperature,
    sweep_soc_snapshot,
    verify_battery,
    scenario_fast_discharge_collapse,
    scenario_thermal_stress,
    scenario_aging_capacity_fade,
)
from .estimator import (
    EKFBatteryEstimator,
    EKFState,
    soh_from_discharge,
)
from .presets import (
    NMC_18650,
    LFP_POUCH,
    LCO_PHONE,
    NMC_EV,
    NMC_AGED,
    LFP_COLD,
    get_preset,
    list_presets,
)

__version__ = "0.4.0"

__all__ = [
    # 스키마
    "ECMParams",
    "BatteryState",
    "DischargeStep",
    "BatteryObservation",
    "VerificationReport",
    # ECM 물리
    "ocv_linear",
    "ocv",
    "ocv_at_soc",
    "d_ocv_d_soc",
    "r_at_temperature",
    "terminal_voltage",
    "step_ecm",
    "c_rate",
    "effective_capacity_ah",
    "internal_resistance_total",
    "voltage_drop_at_current",
    "time_to_discharge",
    "soc_at_time",
    "thermal_time_constant",
    "steady_state_temperature",
    "max_continuous_current",
    "power_capability",
    # Observer
    "observe_battery",
    "diagnose",
    # 설계 엔진
    "simulate_discharge",
    "simulate_charge",
    "simulate_charge_cccv",
    "sweep_c_rate",
    "sweep_soh",
    "sweep_temperature",
    "sweep_soc_snapshot",
    "verify_battery",
    # 시나리오
    "scenario_fast_discharge_collapse",
    "scenario_thermal_stress",
    "scenario_aging_capacity_fade",
    # EKF 추정기
    "EKFBatteryEstimator",
    "EKFState",
    "soh_from_discharge",
    # 프리셋
    "NMC_18650",
    "LFP_POUCH",
    "LCO_PHONE",
    "NMC_EV",
    "NMC_AGED",
    "LFP_COLD",
    "get_preset",
    "list_presets",
    # 버전
    "__version__",
]

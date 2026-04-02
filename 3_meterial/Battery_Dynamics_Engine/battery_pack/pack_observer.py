"""팩 레벨 Ω_global Observer.

설계 원칙
─────────
  팩은 "가장 약한 셀"이 전체를 제한한다.
  → Ω_global = Ω_min × 0.60 + Ω_mean × 0.40

  개별 셀 Ω는 battery_dynamics.observe_battery() 재사용.
  팩 전용 플래그를 추가로 계산.

팩 전용 플래그
─────────────
  cell_imbalance    : SOC 편차 > 5%
  severe_imbalance  : SOC 편차 > 10%
  hot_cell          : 최고 셀 온도 ≥ 45°C
  critical_hot_cell : 최고 셀 온도 ≥ 60°C
  temp_gradient     : 셀 간 온도 차이 > 5K
  weak_cell         : 최약 셀 SOC ≤ 15%
  pack_degraded     : 평균 Ω < 0.52
"""

from __future__ import annotations

from typing import List

from battery_dynamics.observer import observe_battery
from battery_dynamics.schema import ECMParams

from .pack_schema import PackObservation, PackParams, PackState


# ── 상수 ────────────────────────────────────────────────────────────────────

_W_MIN  = 0.60   # 최약 셀 가중치
_W_MEAN = 0.40   # 평균 셀 가중치

_VERDICTS = [
    (0.75, "HEALTHY"),
    (0.52, "STABLE"),
    (0.30, "FRAGILE"),
]

# 팩 플래그 임계
_SOC_IMBALANCE_WARN  = 0.05
_SOC_IMBALANCE_CRIT  = 0.10
_T_WARN_K            = 318.15   # 45°C
_T_CRIT_K            = 333.15   # 60°C
_T_GRADIENT_K        = 5.0
_WEAK_CELL_SOC       = 0.15


def observe_pack(
    state: PackState,
    params: PackParams,
    I_pack: float = 0.0,
) -> PackObservation:
    """팩 Ω_global 관측.

    Parameters
    ----------
    state   : PackState (Composition — BatteryState 리스트 포함)
    params  : PackParams (기준 ECMParams 포함)
    I_pack  : 팩 전류 [A] (I > 0 = 방전)

    Returns
    -------
    PackObservation — Ω_global + 팩 전용 플래그
    """
    cells = state.cells
    n     = len(cells)
    if n == 0:
        return PackObservation(
            omega_global=0.0, omega_min=0.0, omega_mean=0.0,
            verdict="CRITICAL", flags=["no_cells"],
        )

    # 병렬 셀 전류 분배 (균등 가정)
    np_ = max(1, params.topology.n_parallel)
    I_cell = I_pack / np_

    # 개별 셀 Ω 계산 — battery_dynamics.observe_battery 재사용
    def _get_cell_params(idx: int) -> ECMParams:
        if params.cell_list and idx < len(params.cell_list):
            return params.cell_list[idx]
        return params.cell_params

    cell_omegas: List[float] = []
    for i, cell in enumerate(cells):
        p = _get_cell_params(i)
        obs = observe_battery(cell, I_cell, p)
        cell_omegas.append(obs.omega_battery)

    omega_min  = min(cell_omegas)
    omega_mean = sum(cell_omegas) / n

    # Ω_global: 최약 셀 중심
    omega_global = _W_MIN * omega_min + _W_MEAN * omega_mean
    omega_global = max(0.0, min(1.0, omega_global))

    # 팩 전용 플래그
    flags: List[str] = []

    if state.soc_spread > _SOC_IMBALANCE_CRIT:
        flags.append("severe_imbalance")
    elif state.soc_spread > _SOC_IMBALANCE_WARN:
        flags.append("cell_imbalance")

    if state.temp_max >= _T_CRIT_K:
        flags.append("critical_hot_cell")
        omega_global = min(omega_global, 0.29)   # CRITICAL 강제
    elif state.temp_max >= _T_WARN_K:
        flags.append("hot_cell")

    if state.temp_spread > _T_GRADIENT_K:
        flags.append("temp_gradient")

    if state.soc_min <= _WEAK_CELL_SOC:
        flags.append("weak_cell")

    if omega_mean < 0.52:
        flags.append("pack_degraded")

    # 판정
    verdict = "CRITICAL"
    for thr, v in _VERDICTS:
        if omega_global >= thr:
            verdict = v
            break

    weakest  = state.weakest_cell_idx
    hottest  = state.hottest_cell_idx

    notes = (
        f"SOC={state.soc_mean:.3f}±{state.soc_spread:.4f} | "
        f"T={state.temp_mean - 273.15:.1f}°C±{state.temp_spread:.1f}K | "
        f"weak_cell=#{weakest}"
    )

    return PackObservation(
        omega_global     = round(omega_global, 4),
        omega_min        = round(omega_min, 4),
        omega_mean       = round(omega_mean, 4),
        verdict          = verdict,
        flags            = flags,
        cell_omegas      = [round(o, 4) for o in cell_omegas],
        weakest_cell_idx = weakest,
        hottest_cell_idx = hottest,
        notes            = notes,
    )

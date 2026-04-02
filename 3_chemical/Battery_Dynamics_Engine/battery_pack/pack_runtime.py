"""팩 런타임 — 팩 생성 · 적분 · 시뮬레이션.

핵심 함수
─────────
  build_pack_state    : PackParams → 초기 PackState (셀 편차 적용)
  step_pack           : 1스텝 팩 ECM 적분 + 1D 열 갱신
  simulate_pack_discharge  : 정전류 팩 방전 시뮬레이션
  simulate_pack_charge_cccv: CC-CV 팩 충전 시뮬레이션

셀 편차 생성
────────────
  CellVariation의 표준편차를 기반으로 Box-Muller 변환으로
  정규분포 난수 생성 (순수 stdlib — random.gauss 사용).
  seed 설정 시 재현 가능.

팩 전류 분배
────────────
  직렬 연결: 모든 셀에 동일 전류 (I_cell = I_pack / n_parallel)
  병렬 연결: 이상적 균등 분배 가정 (내부저항 균등)

밸런싱 통합
───────────
  simulate_pack_discharge/charge_cccv에 balancer 파라미터 선택적 주입.
  밸런서가 계산한 추가 전류는 각 셀 I에 더해짐.
"""

from __future__ import annotations

import math
import random
from typing import List, Optional

import dataclasses

from battery_dynamics.ecm import (
    ocv,
    r_at_temperature,
    step_ecm,
    terminal_voltage,
)
from battery_dynamics.observer import observe_battery
from battery_dynamics.schema import BatteryState, ECMParams

from .balancer import ActiveBalancer, PassiveBalancer
from .pack_observer import observe_pack
from .pack_schema import (
    PackObservation,
    PackParams,
    PackState,
    PackStep,
)
from .pack_thermal import PackThermal1D


# ══════════════════════════════════════════════════════════════════════════════
# 팩 초기화
# ══════════════════════════════════════════════════════════════════════════════

def build_pack_state(
    params: PackParams,
    soc_init: float = 1.0,
    temp_init_k: Optional[float] = None,
) -> PackState:
    """PackParams → 초기 PackState 생성 (셀 편차 적용).

    CellVariation의 soc_std / capacity_std / r0_std / temp_std_k 기반으로
    각 셀에 독립적인 편차를 부여합니다.

    Parameters
    ----------
    params      : PackParams
    soc_init    : 기준 초기 SOC
    temp_init_k : 기준 초기 온도 (None → params.cell_params.t_amb_k)

    Returns
    -------
    PackState (cells = n_cells 개 BatteryState, 편차 적용 완료)
    """
    var   = params.variation
    topo  = params.topology
    base  = params.cell_params
    n     = topo.total_cells
    T_ref = float(temp_init_k) if temp_init_k is not None else base.t_amb_k

    rng = random.Random(var.seed)

    cells: List[BatteryState] = []
    cell_list_out: List[ECMParams] = []

    for i in range(n):
        # SOC 편차
        soc_i = max(0.0, min(1.0, soc_init + rng.gauss(0, var.soc_std)))

        # 용량 편차
        cap_factor = 1.0 + rng.gauss(0, var.capacity_std)
        cap_factor = max(0.5, min(1.5, cap_factor))

        # R0 편차
        r0_factor  = 1.0 + rng.gauss(0, var.r0_std)
        r0_factor  = max(0.5, min(2.0, r0_factor))

        # 온도 편차
        temp_i = T_ref + rng.gauss(0, var.temp_std_k)

        # 셀 ECMParams 변형 (composition — 원본 안 건드림)
        if params.cell_list and i < len(params.cell_list):
            p_i = params.cell_list[i]
        else:
            p_i = dataclasses.replace(
                base,
                q_ah   = base.q_ah   * cap_factor,
                r0_ohm = base.r0_ohm * r0_factor,
            )

        cell_list_out.append(p_i)
        cells.append(BatteryState(
            soc    = soc_i,
            v_rc   = 0.0,
            v_rc2  = 0.0,
            temp_k = temp_i,
            t_s    = 0.0,
        ))

    # cell_list를 params에 캐싱 (이후 step에서 사용)
    object.__setattr__(params, "cell_list", cell_list_out)

    state = PackState(cells=cells, topology=topo, t_s=0.0)
    return state


# ══════════════════════════════════════════════════════════════════════════════
# 내부 헬퍼
# ══════════════════════════════════════════════════════════════════════════════

def _compute_pack_voltage(
    cells: List[BatteryState],
    cell_params: List[ECMParams],
    I_cell: float,
    topology,
) -> float:
    """팩 단자전압 계산.

    직렬 그룹: 각 그룹 병렬 셀의 V_term 평균 → 직렬 합산.
    """
    ns  = topology.n_series
    np_ = topology.n_parallel
    v_pack = 0.0
    for s_idx in range(ns):
        group_v = 0.0
        for p_idx in range(np_):
            cell_idx = s_idx * np_ + p_idx
            if cell_idx < len(cells):
                p_i = cell_params[cell_idx]
                group_v += terminal_voltage(cells[cell_idx], I_cell, p_i)
        v_pack += group_v / np_
    return v_pack


def _get_cell_params(params: PackParams, idx: int) -> ECMParams:
    if params.cell_list and idx < len(params.cell_list):
        return params.cell_list[idx]
    return params.cell_params


def _cell_p_heat(cell: BatteryState, p: ECMParams, I_cell: float) -> float:
    """셀 발열량 [W] = I² × (R0(T) + R1)."""
    R0 = r_at_temperature(p.r0_ohm, cell.temp_k, p)
    return I_cell ** 2 * (R0 + p.r1_ohm)


# ══════════════════════════════════════════════════════════════════════════════
# 1스텝 팩 적분
# ══════════════════════════════════════════════════════════════════════════════

def step_pack(
    state: PackState,
    I_pack: float,
    dt: float,
    params: PackParams,
    thermal: Optional[PackThermal1D] = None,
    balancer_currents: Optional[List[float]] = None,
) -> PackState:
    """1스텝 팩 ECM + 열 적분.

    Parameters
    ----------
    state             : 현재 PackState
    I_pack            : 팩 전류 [A] (I > 0 = 방전)
    dt                : 시간 스텝 [s]
    params            : PackParams
    thermal           : PackThermal1D (None → 셀 독립 열 모델)
    balancer_currents : 셀별 추가 전류 (None → 0)

    Returns
    -------
    새 PackState
    """
    np_ = max(1, params.topology.n_parallel)
    I_cell_base = I_pack / np_   # 셀 기본 전류 (균등 분배)

    n      = len(state.cells)
    b_curr = balancer_currents or [0.0] * n

    # 각 셀 ECM 적분
    new_cells: List[BatteryState] = []
    p_heat_list: List[float] = []

    for i, cell in enumerate(state.cells):
        p_i    = _get_cell_params(params, i)
        I_i    = I_cell_base + b_curr[i]   # 밸런싱 전류 합산
        ph     = _cell_p_heat(cell, p_i, I_i)
        p_heat_list.append(ph)

        if thermal is None:
            # 셀 독립 열 모델 (A레이어 방식)
            new_cell = step_ecm(cell, I_i, dt, p_i)
        else:
            # 1D 열 모델: temp_k는 thermal.step()에서 별도 갱신
            new_cell = step_ecm(cell, I_i, dt, p_i)

        new_cells.append(new_cell)

    # 1D 열 체인 갱신
    if thermal is not None:
        temps_now = [c.temp_k for c in new_cells]
        new_temps = thermal.step(temps_now, p_heat_list, dt)
        new_cells = [
            dataclasses.replace(c, temp_k=new_temps[i])
            for i, c in enumerate(new_cells)
        ]

    return PackState(
        cells    = new_cells,
        topology = state.topology,
        t_s      = state.t_s + dt,
    )


# ══════════════════════════════════════════════════════════════════════════════
# 팩 방전 시뮬레이션
# ══════════════════════════════════════════════════════════════════════════════

def simulate_pack_discharge(
    params: PackParams,
    I_pack: float,
    dt_s: float = 1.0,
    n_steps: int = 14400,
    soc_init: float = 1.0,
    temp_init_k: Optional[float] = None,
    thermal: Optional[PackThermal1D] = None,
    balancer: Optional[object] = None,   # PassiveBalancer | ActiveBalancer
) -> List[PackStep]:
    """정전류 팩 방전 시뮬레이션.

    Parameters
    ----------
    params     : PackParams
    I_pack     : 팩 방전 전류 [A] (양수)
    dt_s       : 시간 스텝 [s]
    n_steps    : 최대 스텝 수
    soc_init   : 초기 SOC
    thermal    : PackThermal1D (None → 셀 독립 열)
    balancer   : PassiveBalancer 또는 ActiveBalancer (None → 미사용)

    종지 조건
    ---------
    약한 셀(weakest) V_term ≤ t_cutoff_v OR soc_min ≤ 0

    Returns
    -------
    List[PackStep]
    """
    I   = max(0.0, float(I_pack))
    dt  = max(1e-6, float(dt_s))

    state = build_pack_state(params, soc_init=soc_init, temp_init_k=temp_init_k)

    steps: List[PackStep] = []
    energy_wh = 0.0

    for _ in range(int(n_steps) + 1):
        np_    = max(1, params.topology.n_parallel)
        I_cell = I / np_

        # 팩 전압
        cell_params_list = [_get_cell_params(params, i) for i in range(len(state.cells))]
        v_pack = _compute_pack_voltage(state.cells, cell_params_list, I_cell, params.topology)

        # 종지 판단 — 약한 셀 기준
        w_idx = state.weakest_cell_idx
        w_p   = _get_cell_params(params, w_idx)
        vt_weak = terminal_voltage(state.cells[w_idx], I_cell, w_p)
        terminated = (vt_weak <= w_p.t_cutoff_v) or (state.soc_min <= 0.0)

        # 팩 관측
        obs = observe_pack(state, params, I)

        # PackStep 캐싱 (v_pack property용)
        object.__setattr__(state, "_v_pack_cached", v_pack)

        # 밸런싱
        balancing_on = False
        b_currents = None
        if balancer is not None and hasattr(balancer, "compute_currents"):
            b_list = balancer.compute_currents(state)
            if any(b != 0.0 for b in b_list):
                b_currents = b_list
                balancing_on = True

        steps.append(PackStep(
            t_s               = round(state.t_s, 4),
            v_pack            = round(v_pack, 4),
            i_pack            = round(I, 4),
            soc_mean          = round(state.soc_mean, 6),
            soc_min           = round(state.soc_min, 6),
            soc_max           = round(state.soc_max, 6),
            soc_spread        = round(state.soc_spread, 6),
            temp_mean         = round(state.temp_mean, 4),
            temp_max          = round(state.temp_max, 4),
            temp_spread       = round(state.temp_spread, 4),
            omega_pack        = obs.omega_global,
            verdict           = obs.verdict,
            terminated        = terminated,
            energy_wh         = round(energy_wh, 6),
            balancing_active  = balancing_on,
            weakest_cell_idx  = state.weakest_cell_idx,
            hottest_cell_idx  = state.hottest_cell_idx,
        ))

        if terminated:
            break

        energy_wh += abs(I) * max(0.0, v_pack) * dt / 3600.0
        state = step_pack(state, I, dt, params, thermal, b_currents)

    return steps


# ══════════════════════════════════════════════════════════════════════════════
# 팩 CC-CV 충전 시뮬레이션
# ══════════════════════════════════════════════════════════════════════════════

def simulate_pack_charge_cccv(
    params: PackParams,
    I_cc_pack: float,
    dt_s: float = 1.0,
    n_steps: int = 28800,
    soc_init: float = 0.20,
    temp_init_k: Optional[float] = None,
    cv_voltage_pack: Optional[float] = None,
    cv_cutoff_ratio: float = 0.05,
    thermal: Optional[PackThermal1D] = None,
    balancer: Optional[object] = None,
) -> List[PackStep]:
    """CC-CV 팩 충전 시뮬레이션.

    CC: I_cc_pack 정전류 → 팩 전압 ≥ v_cv_pack 에서 CV 전환
    CV: 팩 전압 유지 → I_pack < I_cc × ratio 에서 종료

    Parameters
    ----------
    I_cc_pack       : CC 충전 전류 [A] (양수)
    cv_voltage_pack : CV 목표 전압 [V] (None → n_series × v_charge_max_v)
    """
    ns  = params.topology.n_series
    np_ = max(1, params.topology.n_parallel)
    I_cc = abs(float(I_cc_pack))

    v_cv = float(cv_voltage_pack) if cv_voltage_pack is not None else (
        ns * params.cell_params.v_charge_max_v
    )
    cutoff = I_cc * max(1e-6, float(cv_cutoff_ratio))
    dt = max(1e-6, float(dt_s))

    state = build_pack_state(params, soc_init=soc_init, temp_init_k=temp_init_k)

    steps: List[PackStep] = []
    energy_wh = 0.0
    phase = "CC"

    for _ in range(int(n_steps) + 1):
        # 충전 전류 결정
        if phase == "CC":
            I_pack = -I_cc
        else:
            # CV: R0 기반 근사 전류 계산
            R0_avg = sum(
                r_at_temperature(
                    _get_cell_params(params, i).r0_ohm,
                    state.cells[i].temp_k,
                    _get_cell_params(params, i),
                )
                for i in range(len(state.cells))
            ) / max(1, len(state.cells))
            R_pack_approx = R0_avg * ns / np_
            ocv_pack_avg = sum(
                ocv(state.cells[i].soc, _get_cell_params(params, i))
                for i in range(len(state.cells))
            ) / max(1, len(state.cells)) * ns
            I_cv_raw = (ocv_pack_avg - v_cv) / max(1e-9, R_pack_approx)
            I_pack = max(-I_cc, min(0.0, I_cv_raw))

        # 팩 전압
        I_cell = I_pack / np_
        cell_params_list = [_get_cell_params(params, i) for i in range(len(state.cells))]
        v_pack = _compute_pack_voltage(state.cells, cell_params_list, I_cell, params.topology)

        # CC → CV 전환
        if phase == "CC" and v_pack >= v_cv:
            phase = "CV"

        # 종지
        terminated = (
            (phase == "CV" and abs(I_pack) <= cutoff)
            or state.soc_min >= 1.0
        )

        obs = observe_pack(state, params, I_pack)
        object.__setattr__(state, "_v_pack_cached", v_pack)

        b_currents = None
        if balancer is not None and hasattr(balancer, "compute_currents"):
            b_list = balancer.compute_currents(state)
            if any(b != 0.0 for b in b_list):
                b_currents = b_list

        steps.append(PackStep(
            t_s               = round(state.t_s, 4),
            v_pack            = round(v_pack, 4),
            i_pack            = round(I_pack, 4),
            soc_mean          = round(state.soc_mean, 6),
            soc_min           = round(state.soc_min, 6),
            soc_max           = round(state.soc_max, 6),
            soc_spread        = round(state.soc_spread, 6),
            temp_mean         = round(state.temp_mean, 4),
            temp_max          = round(state.temp_max, 4),
            temp_spread       = round(state.temp_spread, 4),
            omega_pack        = obs.omega_global,
            verdict           = obs.verdict,
            terminated        = terminated,
            energy_wh         = round(energy_wh, 6),
            balancing_active  = b_currents is not None,
            weakest_cell_idx  = state.weakest_cell_idx,
            hottest_cell_idx  = state.hottest_cell_idx,
        ))

        if terminated:
            break

        energy_wh += abs(I_pack) * max(0.0, v_pack) * dt / 3600.0
        state = step_pack(state, I_pack, dt, params, thermal, b_currents)

    return steps

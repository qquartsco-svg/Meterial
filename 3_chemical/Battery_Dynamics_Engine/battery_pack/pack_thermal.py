"""1D 팩 열 체인 모델.

모델 구조
─────────
  셀을 1D 체인으로 배열:
    [cell_0] ─ [cell_1] ─ ... ─ [cell_n-1]

  인접 셀 간 열전도:
    q_ij = λ / dx × (T_j − T_i)   [W]

  냉각:
    q_cool_i = h_cool × (T_i − T_cool)   [W]  (냉각 위치만)

  셀 열 ODE (오일러 적분):
    C_th · dT_i/dt = P_heat_i
                   + Σ_j∈adj q_ij
                   − q_cool_i

0D vs 1D 차이
─────────────
  0D (A레이어 단일 셀): 온도 1개 숫자, 팩 공간 분포 없음
  1D (B레이어 팩):     셀 위치별 온도 → 셀 간 온도 편차 추적

  팩에서 핵심은 "어느 셀이 얼마나 뜨거운가" — 1D가 최소 요건.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class PackThermal1D:
    """1D 팩 열 체인 모델.

    Attributes
    ----------
    n_cells              : 셀 수 (체인 길이)
    cell_thermal_c       : 셀 열용량 [J/K] (battery_dynamics.ECMParams.thermal_c_j_per_k)
    cell_spacing_m       : 셀 간격 [m] (기본 3mm)
    thermal_conductivity : 셀 간 열전도율 [W/m/K] (기본 1.0 W/m/K — 알루미늄 케이스 압축)
    h_cool_w_per_k       : 냉각면 열전달 계수 [W/K] (기본 5.0)
    coolant_temp_k       : 냉각수/공기 온도 [K] (기본 25°C)
    cooling_positions    : 냉각 적용 셀 인덱스 목록
                           None → 양 끝 [0, n_cells-1]
                           []   → 냉각 없음 (단열)
    """
    n_cells:              int
    cell_thermal_c:       float = 200.0
    cell_spacing_m:       float = 0.003
    thermal_conductivity: float = 1.0
    h_cool_w_per_k:       float = 5.0
    coolant_temp_k:       float = 298.15
    cooling_positions:    Optional[List[int]] = field(default=None)

    def __post_init__(self) -> None:
        if self.cooling_positions is None:
            # 기본: 양 끝 냉각
            self.cooling_positions = [0, self.n_cells - 1] if self.n_cells > 1 else [0]

    # ── 열전도 계수 ─────────────────────────────────────────────────────────

    @property
    def k_cond(self) -> float:
        """셀 간 열전도 [W/K] = λ / dx."""
        return self.thermal_conductivity / max(1e-6, self.cell_spacing_m)

    # ── 1스텝 온도 적분 ─────────────────────────────────────────────────────

    @property
    def _dt_stable(self) -> float:
        """수치 안정 최대 dt [s] (명시적 오일러 안정 조건).

        Interior cell: dT/dt ~ 2k/C × ΔT  →  dt < C/(2k)
        Cooling  cell: dT/dt ~ h/C  × ΔT  →  dt < C/h
        Safety factor 0.4 적용.
        """
        k    = self.k_cond
        h    = self.h_cool_w_per_k
        C_th = max(1e-6, self.cell_thermal_c)
        denom = max(2.0 * k, h, 1e-6)
        return 0.4 * C_th / denom

    def _step_once(
        self,
        temps: List[float],
        p_heat: List[float],
        dt: float,
    ) -> List[float]:
        """단일 오일러 스텝 (내부 전용)."""
        n    = self.n_cells
        k    = self.k_cond
        C_th = max(1e-6, self.cell_thermal_c)
        h    = self.h_cool_w_per_k
        T_c  = self.coolant_temp_k
        cool = set(self.cooling_positions or [])

        new_temps: List[float] = []

        for i in range(n):
            dT = 0.0

            # 발열
            dT += p_heat[i] / C_th

            # 왼쪽 이웃 열전도
            if i > 0:
                dT += k * (temps[i - 1] - temps[i]) / C_th

            # 오른쪽 이웃 열전도
            if i < n - 1:
                dT += k * (temps[i + 1] - temps[i]) / C_th

            # 냉각
            if i in cool:
                dT -= h * (temps[i] - T_c) / C_th

            new_temps.append(temps[i] + dt * dT)

        return new_temps

    def step(
        self,
        temps: List[float],
        p_heat: List[float],
        dt: float,
    ) -> List[float]:
        """1D 열 체인 오일러 적분 (자동 sub-stepping으로 수치 안정 보장).

        Parameters
        ----------
        temps   : 현재 셀 온도 리스트 [K], 길이 = n_cells
        p_heat  : 각 셀 발열량 [W] (I²·R_total), 길이 = n_cells
        dt      : 시간 스텝 [s] — 내부적으로 안정 조건 초과 시 sub-step

        Returns
        -------
        새 온도 리스트 [K]
        """
        dt_max = self._dt_stable
        if dt <= dt_max:
            return self._step_once(temps, p_heat, dt)

        # sub-step으로 분할 적분
        n_sub  = int(math.ceil(dt / dt_max))
        dt_sub = dt / n_sub
        cur    = temps
        for _ in range(n_sub):
            cur = self._step_once(cur, p_heat, dt_sub)
        return cur

    # ── 정상상태 온도 추정 ──────────────────────────────────────────────────

    def steady_state_temps(self, p_heat_uniform: float) -> List[float]:
        """균일 발열 가정 시 정상상태 온도 [K] 추정.

        반복 적분으로 수렴값 계산.
        안정 dt를 자동 선택하여 발산 없이 수렴 보장 (총 시뮬레이션 5000s).
        """
        temps = [self.coolant_temp_k] * self.n_cells
        p_vec = [p_heat_uniform] * self.n_cells
        # step()의 sub-stepping 덕분에 dt=1.0 사용 가능 (내부에서 안정 분할)
        for _ in range(5000):
            temps = self.step(temps, p_vec, dt=1.0)
        return temps

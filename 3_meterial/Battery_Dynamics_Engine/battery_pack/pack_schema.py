"""Layer B 팩 스키마 — 구성(Composition) 기반 설계.

설계 원칙
─────────
  BatteryState / ECMParams 를 상속(inherit)하지 않고
  포함(contain)하는 Composition 구조.

  CellState  → BatteryState  (1개 셀)
  PackState  → List[BatteryState]  (n_series × n_parallel 셀 집합)

  공통 인터페이스는 property로만 노출.
  상위 레이어(C/D)는 PackState 안을 직접 건드리지 않음.

클래스 목록
───────────
  PackTopology   — 직·병렬 구성
  CellVariation  — 셀 간 초기 편차 분포 파라미터
  PackParams     — 팩 전체 파라미터 컨테이너
  PackState      — 런타임 팩 상태 (composition)
  PackStep       — 시뮬레이션 스텝 결과
  PackObservation — Ω_global 관측 결과
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional

from battery_dynamics.schema import BatteryState, ECMParams


# ══════════════════════════════════════════════════════════════════════════════
# 팩 토폴로지
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class PackTopology:
    """직·병렬 팩 구성 정보.

    Attributes
    ----------
    n_series   : 직렬 셀 수 (팩 전압 = n_series × V_cell)
    n_parallel : 병렬 셀 수 (팩 용량 = n_parallel × Q_cell)

    Examples
    --------
    96s4p EV 팩:  PackTopology(n_series=96, n_parallel=4)
    → 총 384 셀, V_pack ≈ 96 × 3.7V ≈ 355V
    """
    n_series:   int = 1
    n_parallel: int = 1

    @property
    def total_cells(self) -> int:
        return self.n_series * self.n_parallel

    @property
    def label(self) -> str:
        return f"{self.n_series}s{self.n_parallel}p"


# ══════════════════════════════════════════════════════════════════════════════
# 셀 편차 분포
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class CellVariation:
    """초기 셀 편차 파라미터 (4종).

    팩 내 셀은 제조 공차·사용 이력으로 편차가 생김.
    시뮬레이션 시작 시 아래 표준편차를 기반으로 각 셀에 편차 적용.

    Attributes
    ----------
    soc_std      : SOC 표준편차 (기본 2% → SOC ±2% 편차)
    capacity_std : 용량 편차 비율 (기본 1% → Q_ah ±1%)
    r0_std       : 내부저항 편차 비율 (기본 5% → R0 ±5%)
    temp_std_k   : 온도 편차 [K] (기본 1K → ±1K 온도 차이)
    seed         : 난수 시드 (None → 비결정적)
    """
    soc_std:      float = 0.02
    capacity_std: float = 0.01
    r0_std:       float = 0.05
    temp_std_k:   float = 1.0
    seed:         Optional[int] = 42


# ══════════════════════════════════════════════════════════════════════════════
# 팩 파라미터
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class PackParams:
    """팩 전체 파라미터 — Composition 구조.

    cell_params  : 기준 셀 ECMParams (편차 기준점)
    topology     : 직·병렬 구성
    variation    : 셀 간 초기 편차
    cell_list    : 명시적 셀 파라미터 리스트 (None → variation으로 자동 생성)
    label        : 팩 식별 레이블
    """
    cell_params: ECMParams
    topology:    PackTopology = field(default_factory=PackTopology)
    variation:   CellVariation = field(default_factory=CellVariation)
    cell_list:   Optional[List[ECMParams]] = field(default=None)
    label:       str = "pack"

    @property
    def n_cells(self) -> int:
        return self.topology.total_cells

    @property
    def v_nominal(self) -> float:
        """공칭 팩 전압 [V] = n_series × V_cell_nominal."""
        return self.topology.n_series * self.cell_params.v_charge_max_v

    @property
    def q_nominal_ah(self) -> float:
        """공칭 팩 용량 [Ah] = n_parallel × Q_cell."""
        return self.topology.n_parallel * self.cell_params.q_ah

    @property
    def energy_nominal_kwh(self) -> float:
        """공칭 팩 에너지 [kWh]."""
        mid_v = self.topology.n_series * (
            self.cell_params.soc_v0 + self.cell_params.soc_ocv_v_per_unit * 0.5
        )
        return mid_v * self.q_nominal_ah / 1000.0


# ══════════════════════════════════════════════════════════════════════════════
# 런타임 팩 상태 — Composition
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class PackState:
    """런타임 팩 상태.

    cells    : n_cells 개 BatteryState 리스트 (BatteryState 상속 X, 포함)
    topology : 직·병렬 구성 참조
    t_s      : 시뮬레이션 경과 시간 [s]

    v_pack, soc_mean, soc_spread 등 팩 수준 지표는 property로 제공.
    """
    cells:    List[BatteryState]
    topology: PackTopology
    t_s:      float = 0.0

    # ── 전압 ────────────────────────────────────────────────────────────────

    @property
    def v_pack(self) -> float:
        """팩 단자전압 [V].

        직렬 그룹별 병렬 평균 → 직렬 합산.
        병렬 셀은 전압을 평균, 직렬 연결은 합산.
        """
        ns = self.topology.n_series
        np_ = self.topology.n_parallel
        v_total = 0.0
        for s_idx in range(ns):
            group = self.cells[s_idx * np_ : (s_idx + 1) * np_]
            v_total += sum(c.v_rc for c in group) / np_   # placeholder
        # 실제 v_term은 PackRuntime에서 계산 후 저장되므로 여기선 v_rc 합산이 아님
        # → _v_pack_cached 참조
        return getattr(self, "_v_pack_cached", float("nan"))

    # ── SOC ─────────────────────────────────────────────────────────────────

    @property
    def soc_list(self) -> List[float]:
        return [c.soc for c in self.cells]

    @property
    def soc_mean(self) -> float:
        return sum(self.soc_list) / max(1, len(self.soc_list))

    @property
    def soc_min(self) -> float:
        return min(self.soc_list) if self.cells else 0.0

    @property
    def soc_max(self) -> float:
        return max(self.soc_list) if self.cells else 0.0

    @property
    def soc_spread(self) -> float:
        """SOC 편차 = max − min."""
        return self.soc_max - self.soc_min

    @property
    def soc_std(self) -> float:
        """SOC 표준편차."""
        if not self.cells:
            return 0.0
        mean = self.soc_mean
        var = sum((c.soc - mean) ** 2 for c in self.cells) / len(self.cells)
        return math.sqrt(var)

    # ── 온도 ────────────────────────────────────────────────────────────────

    @property
    def temp_list(self) -> List[float]:
        return [c.temp_k for c in self.cells]

    @property
    def temp_mean(self) -> float:
        return sum(self.temp_list) / max(1, len(self.temp_list))

    @property
    def temp_max(self) -> float:
        return max(self.temp_list) if self.cells else 0.0

    @property
    def temp_min(self) -> float:
        return min(self.temp_list) if self.cells else 0.0

    @property
    def temp_spread(self) -> float:
        """온도 편차 [K] = T_max − T_min."""
        return self.temp_max - self.temp_min

    # ── 약한 셀 인덱스 ───────────────────────────────────────────────────────

    @property
    def weakest_cell_idx(self) -> int:
        """SOC 최소 셀 인덱스."""
        if not self.cells:
            return 0
        return min(range(len(self.cells)), key=lambda i: self.cells[i].soc)

    @property
    def hottest_cell_idx(self) -> int:
        """온도 최고 셀 인덱스."""
        if not self.cells:
            return 0
        return max(range(len(self.cells)), key=lambda i: self.cells[i].temp_k)

    def __repr__(self) -> str:
        return (
            f"PackState(n={len(self.cells)}, "
            f"SOC={self.soc_mean:.3f}±{self.soc_spread:.4f}, "
            f"T={self.temp_mean - 273.15:.1f}°C±{self.temp_spread:.1f}K, "
            f"t={self.t_s:.0f}s)"
        )


# ══════════════════════════════════════════════════════════════════════════════
# 시뮬레이션 스텝 결과
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class PackStep:
    """팩 시뮬레이션 스텝 결과."""
    t_s:          float
    v_pack:       float       # 팩 단자전압 [V]
    i_pack:       float       # 팩 전류 [A]
    soc_mean:     float
    soc_min:      float
    soc_max:      float
    soc_spread:   float       # max − min
    temp_mean:    float       # [K]
    temp_max:     float
    temp_spread:  float       # [K]
    omega_pack:   float       # Ω_global ∈ [0, 1]
    verdict:      str
    terminated:   bool
    energy_wh:    float = 0.0
    balancing_active: bool = False
    weakest_cell_idx: int = 0
    hottest_cell_idx: int = 0


# ══════════════════════════════════════════════════════════════════════════════
# 팩 관측 결과
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class PackObservation:
    """Ω_global 팩 관측 결과.

    Ω_global = min(Ω_cells) × 0.60 + mean(Ω_cells) × 0.40
    → 가장 약한 셀에 민감하게 반응.
    """
    omega_global:     float
    omega_min:        float       # 최약 셀 Ω
    omega_mean:       float       # 평균 셀 Ω
    verdict:          str
    flags:            List[str]   = field(default_factory=list)
    cell_omegas:      List[float] = field(default_factory=list)
    weakest_cell_idx: int = 0
    hottest_cell_idx: int = 0
    notes:            str = ""

"""셀 밸런싱 알고리즘 — 패시브 / 액티브.

밸런싱 목적
───────────
  팩 내 셀은 제조 편차·사용 이력으로 SOC가 달라짐.
  SOC 편차 → 약한 셀 과방전 / 강한 셀 과충전 위험.
  밸런싱: 편차를 tolerance 이내로 줄임.

패시브 밸런싱 (PassiveBalancer)
───────────────────────────────
  가장 높은 SOC 셀의 에너지를 저항으로 소모.
  구현: 해당 셀에 추가 방전 전류 인가.
  특성: 단순·저비용 / 에너지 손실 있음.

액티브 밸런싱 (ActiveBalancer)
────────────────────────────────
  SOC 높은 셀 → SOC 낮은 셀로 에너지 이동.
  구현: 고SOC 셀 추가 방전 + 저SOC 셀 추가 충전.
  특성: 효율 높음 / 복잡·고비용.

부호 규약
─────────
  반환 전류 벡터: 양수 = 해당 셀에서 추가 방전, 음수 = 추가 충전
  (battery_dynamics 부호 규약 I > 0 = 방전 일치)
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List

from .pack_schema import PackState


# ══════════════════════════════════════════════════════════════════════════════
# 패시브 밸런서
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class PassiveBalancer:
    """SOC 최고 셀 저항 블리딩 밸런서.

    Attributes
    ----------
    soc_tolerance   : 밸런싱 필요 판단 임계 SOC 편차 (기본 2%)
    bleed_current_a : 블리딩 전류 [A] (기본 0.1A — 소전류 지속)
    max_bleed_cells : 동시 블리딩 최대 셀 수 (기본 1)
    """
    soc_tolerance:    float = 0.02
    bleed_current_a:  float = 0.1
    max_bleed_cells:  int   = 1

    def balance_needed(self, state: PackState) -> bool:
        """밸런싱 필요 여부."""
        return state.soc_spread > self.soc_tolerance

    def compute_currents(self, state: PackState) -> List[float]:
        """셀별 추가 전류 [A] 계산.

        SOC 최고 셀 중 max_bleed_cells 개에 bleed_current_a 적용.
        나머지 셀 = 0.

        Returns
        -------
        List[float] 길이 = n_cells, 양수 = 방전(SOC 소모)
        """
        n = len(state.cells)
        currents = [0.0] * n
        if not self.balance_needed(state):
            return currents

        # SOC 내림차순 정렬, 상위 max_bleed_cells 셀 선택
        ranked = sorted(range(n), key=lambda i: state.cells[i].soc, reverse=True)
        for idx in ranked[:self.max_bleed_cells]:
            # 가장 높은 셀만 블리딩 (평균 대비 편차가 tolerance 초과일 때)
            if state.cells[idx].soc - state.soc_mean > self.soc_tolerance / 2:
                currents[idx] = self.bleed_current_a

        return currents

    def info(self) -> str:
        return (
            f"PassiveBalancer(tol={self.soc_tolerance:.3f}, "
            f"I_bleed={self.bleed_current_a:.3f}A, "
            f"max={self.max_bleed_cells}셀)"
        )


# ══════════════════════════════════════════════════════════════════════════════
# 액티브 밸런서
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class ActiveBalancer:
    """SOC 편차 → 에너지 이동 밸런서.

    SOC 최고 셀에서 최저 셀로 에너지 이동.
    고SOC 셀: 추가 방전 (양수 전류)
    저SOC 셀: 추가 충전 (음수 전류)

    Attributes
    ----------
    soc_tolerance   : 밸런싱 필요 임계 (기본 2%)
    transfer_current_a : 이동 전류 크기 [A] (기본 1.0A)
    efficiency      : DC-DC 변환 효율 (기본 0.92 = 92%)
    """
    soc_tolerance:      float = 0.02
    transfer_current_a: float = 1.0
    efficiency:         float = 0.92

    def balance_needed(self, state: PackState) -> bool:
        return state.soc_spread > self.soc_tolerance

    def compute_currents(self, state: PackState) -> List[float]:
        """셀별 추가 전류 [A] 계산.

        최고 SOC 셀 → 최저 SOC 셀 에너지 이동.
        효율 반영: 방전 전류 × efficiency = 충전 전류.

        Returns
        -------
        List[float] 양수 = 방전, 음수 = 충전
        """
        n = len(state.cells)
        currents = [0.0] * n
        if not self.balance_needed(state):
            return currents

        high_idx = max(range(n), key=lambda i: state.cells[i].soc)
        low_idx  = min(range(n), key=lambda i: state.cells[i].soc)

        if high_idx == low_idx:
            return currents

        gap = state.cells[high_idx].soc - state.cells[low_idx].soc
        if gap <= self.soc_tolerance:
            return currents

        I_t = min(self.transfer_current_a, abs(gap) * 10.0)
        currents[high_idx] = I_t                        # 방전 (양수)
        currents[low_idx]  = -I_t * self.efficiency    # 충전 (음수)

        return currents

    def info(self) -> str:
        return (
            f"ActiveBalancer(tol={self.soc_tolerance:.3f}, "
            f"I_transfer={self.transfer_current_a:.2f}A, "
            f"η={self.efficiency:.2f})"
        )

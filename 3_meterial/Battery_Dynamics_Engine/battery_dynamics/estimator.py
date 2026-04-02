"""EKF(확장 칼만 필터) 기반 SOC 추정기.

v0.3.0 신규
────────────
  EKFBatteryEstimator  — 1RC / 2RC 자동 전환 EKF, 순수 stdlib
  soh_from_discharge   — 방전 궤적 에너지 적분 기반 SOH 추정
  EKFState             — 추정 상태 스냅샷

이론
────
  상태 벡터 (1RC): x = [SOC, V_RC1]
  상태 벡터 (2RC): x = [SOC, V_RC1, V_RC2]

  예측:
    SOC_{k+1}  = SOC_k − (I/Q_eff)·dt
    V_RC1_{k+1} = V_RC1_k·(1 − dt/τ1) + I/C1·dt
    V_RC2_{k+1} = V_RC2_k·(1 − dt/τ2) + I/C2·dt  [2RC만]
    P_pred = F · P · F^T + Q

  갱신:
    h(x) = OCV(SOC) − I·R0(T) − V_RC1 − V_RC2
    H    = [dOCV/dSOC, −1, (−1)]      [야코비안]
    S    = H · P · H^T + R             [혁신 분산]
    K    = P · H^T / S                 [칼만 게인]
    x    = x_pred + K·(V_meas − h(x))
    P    = (I − K·H) · P_pred

부호 규약: I > 0 = 방전, I < 0 = 충전.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from .schema import BatteryState, DischargeStep, ECMParams
from .ecm import (
    ocv,
    d_ocv_d_soc,
    r_at_temperature,
    terminal_voltage,
    effective_capacity_ah,
)


# ══════════════════════════════════════════════════════════════════════════════
# 순수 Python 미니 선형대수 헬퍼 (n×n, n ≤ 3)
# ══════════════════════════════════════════════════════════════════════════════

def _mat_mul(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    """행렬 곱 A @ B."""
    nr, nk, nc = len(A), len(B), len(B[0])
    return [
        [sum(A[i][k] * B[k][j] for k in range(nk)) for j in range(nc)]
        for i in range(nr)
    ]


def _mat_add(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    """행렬 합 A + B."""
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def _mat_T(A: List[List[float]]) -> List[List[float]]:
    """전치 행렬 A^T."""
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]


def _mat_eye(n: int) -> List[List[float]]:
    """n×n 단위 행렬."""
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def _mat_diag(v: List[float]) -> List[List[float]]:
    """대각 행렬."""
    n = len(v)
    return [[v[i] if i == j else 0.0 for j in range(n)] for i in range(n)]


def _kalman_gain_and_S(
    P: List[List[float]], H: List[float], R: float
) -> Tuple[List[float], float]:
    """K = P H^T / S,  S = H P H^T + R.  (측정 1차원 전용)

    Returns
    -------
    K : List[float]  — 칼만 게인 벡터 (n,)
    S : float        — 혁신 분산
    """
    n = len(P)
    # P H^T (컬럼 벡터, 1D → n,)
    PHt = [sum(P[i][j] * H[j] for j in range(n)) for i in range(n)]
    S   = sum(H[i] * PHt[i] for i in range(n)) + R
    K   = [PHt[i] / max(1e-12, S) for i in range(n)]
    return K, S


def _update_P_joseph(
    P: List[List[float]], K: List[float], H: List[float], R: float
) -> List[List[float]]:
    """Joseph 형식 공분산 갱신: P = (I - K H) P (I - K H)^T + K R K^T.

    수치 안정성이 표준 형식보다 우수.
    """
    n = len(P)
    KH   = [[K[i] * H[j] for j in range(n)] for i in range(n)]
    I_KH = [[(_mat_eye(n)[i][j] - KH[i][j]) for j in range(n)] for i in range(n)]
    # P1 = (I - KH) P (I - KH)^T
    P1 = _mat_mul(I_KH, _mat_mul(P, _mat_T(I_KH)))
    # P2 = K R K^T
    KcT = [[K[i] * K[j] * R for j in range(n)] for i in range(n)]
    return _mat_add(P1, KcT)


# ══════════════════════════════════════════════════════════════════════════════
# EKF 추정 상태
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class EKFState:
    """EKF 추정 상태 스냅샷.

    Attributes
    ----------
    soc_est   : 추정 SOC.
    v_rc1_est : 추정 RC1 분극전압 [V].
    v_rc2_est : 추정 RC2 분극전압 [V] (1RC 모드 시 0.0).
    P         : 공분산 행렬 (n×n).
    soc_std   : SOC 표준편차 (√P[0][0]).
    t_s       : 현재 시각 [s].
    """
    soc_est:   float
    v_rc1_est: float
    v_rc2_est: float
    P:         List[List[float]]
    soc_std:   float
    t_s:       float = 0.0


# ══════════════════════════════════════════════════════════════════════════════
# EKF 배터리 추정기
# ══════════════════════════════════════════════════════════════════════════════

class EKFBatteryEstimator:
    """확장 칼만 필터 기반 SOC / V_RC 추정기.

    Examples
    --------
    >>> from battery_dynamics import NMC_18650, EKFBatteryEstimator
    >>> ekf = EKFBatteryEstimator(NMC_18650, soc_init=0.80)
    >>> state = ekf.step(V_meas=3.95, I_a=3.4, dt_s=1.0)
    >>> print(f"SOC_est={state.soc_est:.4f}  σ={state.soc_std:.5f}")
    """

    def __init__(
        self,
        params: ECMParams,
        soc_init: float = 1.0,
        v_rc1_init: float = 0.0,
        v_rc2_init: float = 0.0,
        q_soc: float = 1e-6,       # 프로세스 노이즈: SOC
        q_rc1: float = 1e-4,       # 프로세스 노이즈: V_RC1
        q_rc2: float = 1e-4,       # 프로세스 노이즈: V_RC2
        r_meas: float = 1e-3,      # 측정 노이즈: V_term [V²]
        p0_soc: float = 0.01,      # 초기 SOC 불확실도
        p0_rc: float  = 0.001,     # 초기 RC 불확실도
    ) -> None:
        self.params  = params
        self.n_rc    = 2 if (params.r2_ohm > 0.0 and params.c2_farad > 0.0) else 1
        n            = self.n_rc + 1   # 상태 차원: 2 or 3

        # 상태 벡터
        self._x: List[float] = [
            float(soc_init),
            float(v_rc1_init),
        ]
        if self.n_rc == 2:
            self._x.append(float(v_rc2_init))

        # 공분산 행렬 초기화
        p0_diag = [float(p0_soc)] + [float(p0_rc)] * self.n_rc
        self._P: List[List[float]] = _mat_diag(p0_diag)

        # 노이즈 행렬
        q_diag = [float(q_soc)] + [float(q_rc1)]
        if self.n_rc == 2:
            q_diag.append(float(q_rc2))
        self._Q: List[List[float]] = _mat_diag(q_diag)
        self._R: float = float(r_meas)

        self._t_s: float = 0.0

    # ── 내부 헬퍼 ──────────────────────────────────────────────────────────

    def _tau1(self) -> float:
        return max(1e-9, self.params.r1_ohm * self.params.c1_farad)

    def _tau2(self) -> float:
        return max(1e-9, self.params.r2_ohm * self.params.c2_farad)

    def _q_eff(self) -> float:
        return max(1e-9, effective_capacity_ah(self.params) * 3600.0)

    def _h(self, x: List[float], I: float, T_k: float) -> float:
        """측정 함수 h(x) = OCV(SOC) − I·R0(T) − V_RC1 − V_RC2."""
        soc  = x[0]
        v_rc1 = x[1]
        v_rc2 = x[2] if self.n_rc == 2 else 0.0
        R0   = r_at_temperature(self.params.r0_ohm, T_k, self.params)
        return ocv(soc, self.params) - I * R0 - v_rc1 - v_rc2

    def _H_jacobian(self, x: List[float], I: float, T_k: float) -> List[float]:
        """관측 야코비안 H = [dOCV/dSOC, -1, (-1)]."""
        dO = d_ocv_d_soc(x[0], self.params)
        H  = [dO, -1.0]
        if self.n_rc == 2:
            H.append(-1.0)
        return H

    def _F_jacobian(self, dt: float) -> List[List[float]]:
        """상태전이 야코비안 F = ∂f/∂x (선형 → 정확)."""
        tau1 = self._tau1()
        n    = self.n_rc + 1
        F    = _mat_eye(n)
        F[0][0] = 1.0
        F[1][1] = 1.0 - dt / tau1
        if self.n_rc == 2:
            tau2    = self._tau2()
            F[2][2] = 1.0 - dt / tau2
        return F

    # ── 공개 API ───────────────────────────────────────────────────────────

    def predict(self, I: float, dt: float, T_k: Optional[float] = None) -> None:
        """EKF 예측 스텝.

        Parameters
        ----------
        I   : 전류 [A] (I > 0 = 방전, I < 0 = 충전).
        dt  : 시간 스텝 [s].
        T_k : 셀 온도 [K] (None → params.t_amb_k).
        """
        dt = max(1e-9, float(dt))
        I  = float(I)

        q_eff = self._q_eff()
        tau1  = self._tau1()
        C1    = max(1e-9, self.params.c1_farad)

        # 상태 예측
        soc_pred  = max(0.0, min(1.0, self._x[0] - (I / q_eff) * dt))
        vrc1_pred = self._x[1] * (1.0 - dt / tau1) + I / C1 * dt

        self._x[0] = soc_pred
        self._x[1] = vrc1_pred

        if self.n_rc == 2:
            tau2  = self._tau2()
            C2    = max(1e-9, self.params.c2_farad)
            vrc2_pred = self._x[2] * (1.0 - dt / tau2) + I / C2 * dt
            self._x[2] = vrc2_pred

        # 공분산 예측: P = F P F^T + Q
        F    = self._F_jacobian(dt)
        FPFt = _mat_mul(F, _mat_mul(self._P, _mat_T(F)))
        self._P = _mat_add(FPFt, self._Q)
        self._t_s += dt

    def update(self, V_meas: float, I: float, T_k: Optional[float] = None) -> None:
        """EKF 갱신 스텝.

        Parameters
        ----------
        V_meas : 측정 단자전압 [V].
        I      : 현재 전류 [A].
        T_k    : 셀 온도 [K] (None → params.t_amb_k).
        """
        T = float(T_k) if T_k is not None else self.params.t_amb_k
        I = float(I)

        H      = self._H_jacobian(self._x, I, T)
        h_pred = self._h(self._x, I, T)
        innov  = float(V_meas) - h_pred

        K, _S = _kalman_gain_and_S(self._P, H, self._R)

        # 상태 갱신
        for i in range(len(self._x)):
            self._x[i] += K[i] * innov

        # SOC 클램프
        self._x[0] = max(0.0, min(1.0, self._x[0]))

        # 공분산 갱신 (Joseph 형식)
        self._P = _update_P_joseph(self._P, K, H, self._R)

    def step(
        self,
        V_meas: float,
        I_a: float,
        dt_s: float,
        T_k: Optional[float] = None,
    ) -> "EKFState":
        """predict + update 한 번 실행 후 현재 추정 상태 반환.

        Parameters
        ----------
        V_meas : 측정 단자전압 [V].
        I_a    : 전류 [A] (양수=방전).
        dt_s   : 시간 스텝 [s].
        T_k    : 셀 온도 [K] (None → params.t_amb_k).
        """
        self.predict(I_a, dt_s, T_k)
        self.update(V_meas, I_a, T_k)
        return self.state

    @property
    def state(self) -> "EKFState":
        """현재 추정 상태 스냅샷."""
        soc_std = math.sqrt(max(0.0, self._P[0][0]))
        v_rc2   = self._x[2] if self.n_rc == 2 else 0.0
        return EKFState(
            soc_est   = round(self._x[0], 6),
            v_rc1_est = round(self._x[1], 6),
            v_rc2_est = round(v_rc2, 6),
            P         = [list(row) for row in self._P],
            soc_std   = round(soc_std, 7),
            t_s       = round(self._t_s, 4),
        )

    def reset(
        self,
        soc: float,
        v_rc1: float = 0.0,
        v_rc2: float = 0.0,
        p0_soc: float = 0.01,
        p0_rc: float  = 0.001,
    ) -> None:
        """추정기 재초기화."""
        self._x = [float(soc), float(v_rc1)]
        if self.n_rc == 2:
            self._x.append(float(v_rc2))
        p0_diag = [float(p0_soc)] + [float(p0_rc)] * self.n_rc
        self._P = _mat_diag(p0_diag)
        self._t_s = 0.0

    def to_battery_state(self, T_k: Optional[float] = None, t_s: Optional[float] = None) -> BatteryState:
        """현재 EKF 추정값 → BatteryState 변환."""
        v_rc2 = self._x[2] if self.n_rc == 2 else 0.0
        return BatteryState(
            soc    = self._x[0],
            v_rc   = self._x[1],
            v_rc2  = v_rc2,
            temp_k = float(T_k) if T_k is not None else self.params.t_amb_k,
            t_s    = float(t_s) if t_s is not None else self._t_s,
        )


# ══════════════════════════════════════════════════════════════════════════════
# SOH 추정 유틸리티
# ══════════════════════════════════════════════════════════════════════════════

def soh_from_discharge(
    steps: List[DischargeStep],
    params: ECMParams,
    soc_start: Optional[float] = None,
    soc_end: Optional[float] = None,
) -> float:
    """방전 궤적 전류 적분 → SOH 추정.

    실제 방전 용량 (I × Δt 적분) / 공칭 용량 (params.q_ah × ΔSOC) 비율.

    Parameters
    ----------
    steps      : simulate_discharge 결과 DischargeStep 리스트.
    params     : 기준 ECMParams (q_ah 참조).
    soc_start  : 방전 시작 SOC (None → steps[0].soc).
    soc_end    : 방전 종료 SOC (None → steps[-1].soc).

    Returns
    -------
    SOH 추정값 [0, 1.2 클램프].
    """
    if not steps or len(steps) < 2:
        return float("nan")

    # 전류 적분 (Coulomb counting)
    q_actual_as = 0.0
    for i in range(len(steps) - 1):
        st    = steps[i]
        dt    = steps[i + 1].t_s - st.t_s
        q_actual_as += abs(st.current_a) * dt   # [A·s]

    q_actual_ah = q_actual_as / 3600.0

    # SOC 범위 기반 공칭 용량
    s0 = float(soc_start) if soc_start is not None else steps[0].soc
    s1 = float(soc_end)   if soc_end   is not None else steps[-1].soc
    delta_soc = max(1e-6, abs(s0 - s1))
    q_nominal_ah = params.q_ah * delta_soc

    soh_est = q_actual_ah / max(1e-9, q_nominal_ah)
    return max(0.0, min(1.2, round(soh_est, 4)))

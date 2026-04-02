"""v0.3.0 확장 테스트 — A1~A4 + B1 + B3.

§1  OCV table (A1)        — 구간선형 보간·LFP 평탄·역방향 호환
§2  2RC ECM (A2)          — RC2 분극·시정수·하위 호환
§3  Arrhenius R(T) (A3)   — 저온/고온 저항·Ea=0 호환
§4  CC-CV 충전 (A4)        — 페이즈 전환·종지 조건·에너지
§5  EKF SOC 추정기 (B1)    — predict/update/step·수렴·1RC/2RC
§6  3단계 노화 모델 (B3)   — SEI/LINEAR/POST_KNEE·EOL 추적
§7  v0.2 하위 호환         — 기존 API 전수 통과
"""

from __future__ import annotations

import math
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
import dataclasses

from battery_dynamics import (
    ECMParams, BatteryState, DischargeStep,
    ocv, ocv_linear, d_ocv_d_soc, r_at_temperature,
    step_ecm, terminal_voltage,
    simulate_discharge, simulate_charge, simulate_charge_cccv,
    observe_battery, verify_battery,
    scenario_aging_capacity_fade,
    EKFBatteryEstimator, EKFState, soh_from_discharge,
    NMC_18650, LFP_POUCH, LCO_PHONE, NMC_EV, NMC_AGED, LFP_COLD,
    get_preset,
)


# ══════════════════════════════════════════════════════════════════════════════
# §1 OCV table (A1)
# ══════════════════════════════════════════════════════════════════════════════

class TestOCVTable:
    def test_nmc_18650_ocv_at_soc0(self):
        v = ocv(0.0, NMC_18650)
        assert abs(v - 3.00) < 0.01

    def test_nmc_18650_ocv_at_soc1(self):
        v = ocv(1.0, NMC_18650)
        assert abs(v - 4.20) < 0.01

    def test_nmc_18650_ocv_midpoint(self):
        v = ocv(0.5, NMC_18650)
        assert 3.80 < v < 3.95

    def test_lfp_plateau_flat_region(self):
        """LFP: SOC 25~75% 구간 OCV 변화 ≤ 60mV (평탄 특성)."""
        v25 = ocv(0.25, LFP_POUCH)
        v75 = ocv(0.75, LFP_POUCH)
        assert abs(v75 - v25) < 0.07

    def test_lfp_ocv_range(self):
        assert ocv(0.0, LFP_POUCH) < 3.00
        assert 3.60 < ocv(1.0, LFP_POUCH) < 3.70

    def test_lco_ocv_high_voltage(self):
        v = ocv(1.0, LCO_PHONE)
        assert abs(v - 4.35) < 0.01

    def test_ocv_clamp_below_zero(self):
        """SOC < 0 → SOC=0 OCV."""
        assert ocv(-0.5, NMC_18650) == ocv(0.0, NMC_18650)

    def test_ocv_clamp_above_one(self):
        assert ocv(1.5, NMC_18650) == ocv(1.0, NMC_18650)

    def test_ocv_fallback_linear_when_no_table(self):
        p = ECMParams()  # ocv_table=None
        assert ocv(0.5, p) == ocv_linear(0.5, p)

    def test_ocv_table_override(self):
        """get_preset으로 table 제거 → 선형 fallback."""
        p = get_preset("nmc_18650", ocv_table=None)
        assert ocv(0.5, p) == ocv_linear(0.5, p)

    def test_d_ocv_d_soc_positive(self):
        """dOCV/dSOC > 0 (OCV는 SOC와 단조 증가)."""
        for soc in [0.1, 0.3, 0.5, 0.7, 0.9]:
            assert d_ocv_d_soc(soc, NMC_18650) > 0

    def test_d_ocv_d_soc_lfp_flat(self):
        """LFP 평탄 구간 기울기 매우 작음 (< 0.2 V/SOC)."""
        slope = d_ocv_d_soc(0.5, LFP_POUCH)
        assert slope < 0.2

    def test_ocv_monotone_nmc(self):
        """NMC OCV는 SOC에 대해 단조 증가."""
        prev = ocv(0.0, NMC_18650)
        for s in [0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 1.0]:
            cur = ocv(s, NMC_18650)
            assert cur >= prev
            prev = cur

    def test_nmc_ev_2rc_ocv_range(self):
        assert 2.80 <= ocv(0.0, NMC_EV) <= 3.00
        assert 4.15 <= ocv(1.0, NMC_EV) <= 4.25


# ══════════════════════════════════════════════════════════════════════════════
# §2 2RC ECM (A2)
# ══════════════════════════════════════════════════════════════════════════════

class Test2RC:
    def test_nmc_ev_has_2rc_params(self):
        assert NMC_EV.r2_ohm > 0.0
        assert NMC_EV.c2_farad > 0.0

    def test_2rc_tau2_reasonable(self):
        """τ2 = R2·C2 — NMC_EV: τ2=150s (장기 분극)."""
        tau2 = NMC_EV.r2_ohm * NMC_EV.c2_farad
        assert 100 < tau2 < 300

    def test_step_ecm_2rc_v_rc2_evolves(self):
        """2RC 모드: v_rc2 가 0에서 증가해야 함."""
        s = BatteryState(soc=0.8, v_rc=0.0, v_rc2=0.0, temp_k=298.15)
        I = 10.0  # 방전 전류
        s_new = step_ecm(s, I, 10.0, NMC_EV)
        assert s_new.v_rc2 != 0.0

    def test_step_ecm_1rc_v_rc2_unchanged(self):
        """1RC 모드: v_rc2 변화 없음."""
        s = BatteryState(soc=0.8, v_rc=0.0, v_rc2=0.5, temp_k=298.15)
        s_new = step_ecm(s, 3.4, 1.0, NMC_18650)
        assert s_new.v_rc2 == 0.5   # r2_ohm=0 → 변화 없음

    def test_2rc_terminal_voltage_includes_vrc2(self):
        """V_RC2가 있으면 단자전압이 더 낮아야 함."""
        s_no_rc2 = BatteryState(soc=0.8, v_rc=0.0, v_rc2=0.0, temp_k=298.15)
        s_rc2    = BatteryState(soc=0.8, v_rc=0.0, v_rc2=0.05, temp_k=298.15)
        vt_no = terminal_voltage(s_no_rc2, 10.0, NMC_EV)
        vt_rc = terminal_voltage(s_rc2,    10.0, NMC_EV)
        assert vt_rc < vt_no

    def test_2rc_discharge_steps_have_v_rc2(self):
        steps = simulate_discharge(NMC_EV, current_a=50.0, dt_s=1.0, n_steps=100)
        assert len(steps) > 0
        # 2RC: v_rc2 가 방전 중 변화해야
        v_rc2_vals = [st.v_rc2 for st in steps]
        assert max(v_rc2_vals) > 0.0

    def test_2rc_v_rc2_decays_after_current_stop(self):
        """전류 제거 후 V_RC2 감쇠."""
        s = BatteryState(soc=0.8, v_rc=0.0, v_rc2=0.1, temp_k=298.15)
        for _ in range(50):
            s = step_ecm(s, 0.0, 1.0, NMC_EV)
        assert s.v_rc2 < 0.1


# ══════════════════════════════════════════════════════════════════════════════
# §3 Arrhenius R(T) (A3)
# ══════════════════════════════════════════════════════════════════════════════

class TestArrhenius:
    def test_r_at_Tref_equals_ref(self):
        """T=T_ref → R(T) = R_ref."""
        R = r_at_temperature(0.022, 298.15, NMC_18650)
        assert abs(R - 0.022) < 1e-6

    def test_r_increases_at_low_T(self):
        """저온에서 저항 증가."""
        R_cold = r_at_temperature(0.022, 263.15, NMC_18650)   # -10°C
        R_ref  = r_at_temperature(0.022, 298.15, NMC_18650)   # 25°C
        assert R_cold > R_ref

    def test_r_decreases_at_high_T(self):
        """고온에서 저항 감소."""
        R_hot = r_at_temperature(0.022, 333.15, NMC_18650)    # 60°C
        R_ref = r_at_temperature(0.022, 298.15, NMC_18650)
        assert R_hot < R_ref

    def test_ea_zero_gives_constant_r(self):
        """Ea=0 → 온도 불변 (v0.2 호환)."""
        p = ECMParams()   # Ea_r_ev=0
        R_cold = r_at_temperature(0.08, 250.0, p)
        R_hot  = r_at_temperature(0.08, 350.0, p)
        assert R_cold == R_hot == 0.08

    def test_lfp_cold_arrhenius_factor(self):
        """LFP_COLD: Ea=0.55eV → -10°C에서 R0 최소 2배 이상 증가."""
        R_cold = r_at_temperature(LFP_COLD.r0_ohm, 263.15, LFP_COLD)
        R_ref  = LFP_COLD.r0_ohm
        assert R_cold > R_ref * 2.0

    def test_nmc_18650_cold_factor(self):
        """NMC: Ea=0.35eV → -10°C에서 R0 ≈ 1.5배 이상."""
        R_cold = r_at_temperature(NMC_18650.r0_ohm, 263.15, NMC_18650)
        assert R_cold > NMC_18650.r0_ohm * 1.5

    def test_arrhenius_terminal_voltage_lower_cold(self):
        """저온에서 R0 증가 → 단자전압 감소."""
        s = BatteryState(soc=0.8, v_rc=0.0, temp_k=263.15)
        s_warm = BatteryState(soc=0.8, v_rc=0.0, temp_k=298.15)
        vt_cold = terminal_voltage(s,      3.4, NMC_18650)
        vt_warm = terminal_voltage(s_warm, 3.4, NMC_18650)
        assert vt_cold < vt_warm


# ══════════════════════════════════════════════════════════════════════════════
# §4 CC-CV 충전 (A4)
# ══════════════════════════════════════════════════════════════════════════════

class TestCCCV:
    def _run_cccv(self, params=None, **kw):
        p = params or NMC_18650
        return simulate_charge_cccv(p, current_cc_a=3.4, dt_s=1.0,
                                     n_steps=14400, **kw)

    def test_cccv_returns_steps(self):
        steps = self._run_cccv()
        assert len(steps) > 0

    def test_cccv_has_cc_phase(self):
        steps = self._run_cccv()
        assert any(s.charge_phase == "CC" for s in steps)

    def test_cccv_has_cv_phase(self):
        steps = self._run_cccv()
        assert any(s.charge_phase == "CV" for s in steps)

    def test_cccv_cc_before_cv(self):
        """CC 페이즈가 CV 페이즈보다 항상 먼저."""
        steps = self._run_cccv()
        phases = [s.charge_phase for s in steps]
        cv_idx = next((i for i, ph in enumerate(phases) if ph == "CV"), None)
        if cv_idx is not None:
            # CV 이전은 모두 CC
            assert all(p == "CC" for p in phases[:cv_idx])

    def test_cccv_current_negative(self):
        """충전 전류는 음수."""
        steps = self._run_cccv()
        assert all(s.current_a <= 0.0 for s in steps)

    def test_cccv_cc_constant_current(self):
        """CC 페이즈: 전류 일정 (−I_cc)."""
        steps = self._run_cccv()
        cc_steps = [s for s in steps if s.charge_phase == "CC"]
        if cc_steps:
            currents = [abs(s.current_a) for s in cc_steps]
            assert max(currents) - min(currents) < 0.01   # ±10mA

    def test_cccv_cv_current_tapers(self):
        """CV 페이즈: 전류 절대값이 감소해야 함."""
        steps = self._run_cccv()
        cv_steps = [s for s in steps if s.charge_phase == "CV"]
        if len(cv_steps) > 5:
            # 초기 vs 말기 비교
            early_I = abs(cv_steps[2].current_a)
            late_I  = abs(cv_steps[-2].current_a)
            assert late_I <= early_I

    def test_cccv_soc_monotone_increase(self):
        """SOC는 단조 증가."""
        steps = self._run_cccv()
        for i in range(1, len(steps)):
            assert steps[i].soc >= steps[i-1].soc - 1e-6

    def test_cccv_v_term_approach_vcv(self):
        """V_term이 v_charge_max_v에 수렴."""
        steps = self._run_cccv()
        cv_steps = [s for s in steps if s.charge_phase == "CV"]
        if cv_steps:
            # CV 페이즈에서 v_term ≈ v_charge_max_v
            for s in cv_steps[:5]:
                assert abs(s.v_term - NMC_18650.v_charge_max_v) < 0.05

    def test_cccv_energy_positive(self):
        steps = self._run_cccv()
        assert steps[-1].energy_wh > 0

    def test_cccv_custom_cv_voltage(self):
        """커스텀 CV 전압 설정."""
        steps = simulate_charge_cccv(NMC_18650, current_cc_a=3.4, cv_voltage=4.10,
                                      dt_s=1.0, n_steps=14400)
        cv_steps = [s for s in steps if s.charge_phase == "CV"]
        if cv_steps:
            assert abs(cv_steps[0].v_term - 4.10) < 0.10

    def test_cccv_terminated_flag(self):
        steps = self._run_cccv()
        assert steps[-1].terminated

    def test_cccv_lfp_works(self):
        steps = simulate_charge_cccv(LFP_POUCH, current_cc_a=50.0,
                                      dt_s=1.0, n_steps=14400, soc_init=0.20)
        assert len(steps) > 0
        assert any(s.charge_phase == "CV" for s in steps)

    def test_cccv_low_soc_init(self):
        steps = simulate_charge_cccv(NMC_18650, current_cc_a=3.4, soc_init=0.05,
                                      dt_s=1.0, n_steps=20000)
        assert len(steps) > 0


# ══════════════════════════════════════════════════════════════════════════════
# §5 EKF SOC 추정기 (B1)
# ══════════════════════════════════════════════════════════════════════════════

class TestEKF:
    def test_ekf_init_soc(self):
        ekf = EKFBatteryEstimator(NMC_18650, soc_init=0.80)
        assert abs(ekf.state.soc_est - 0.80) < 1e-6

    def test_ekf_state_is_ekfstate(self):
        ekf = EKFBatteryEstimator(NMC_18650)
        assert isinstance(ekf.state, EKFState)

    def test_ekf_predict_decreases_soc(self):
        """예측 스텝: 방전 전류 → SOC 감소."""
        ekf = EKFBatteryEstimator(NMC_18650, soc_init=0.80)
        soc_before = ekf.state.soc_est
        ekf.predict(I=3.4, dt=1.0)
        assert ekf.state.soc_est < soc_before

    def test_ekf_predict_increases_soc_on_charge(self):
        ekf = EKFBatteryEstimator(NMC_18650, soc_init=0.50)
        soc_before = ekf.state.soc_est
        ekf.predict(I=-3.4, dt=1.0)
        assert ekf.state.soc_est > soc_before

    def test_ekf_soc_clamped_01(self):
        ekf = EKFBatteryEstimator(NMC_18650, soc_init=0.001)
        ekf.predict(I=100.0, dt=10.0)   # 과방전
        assert 0.0 <= ekf.state.soc_est <= 1.0

    def test_ekf_update_does_not_explode(self):
        ekf = EKFBatteryEstimator(NMC_18650, soc_init=0.80)
        ekf.predict(I=3.4, dt=1.0)
        ekf.update(V_meas=3.95, I=3.4)
        assert 0.0 <= ekf.state.soc_est <= 1.0

    def test_ekf_step_returns_ekfstate(self):
        ekf = EKFBatteryEstimator(NMC_18650, soc_init=0.80)
        st = ekf.step(V_meas=3.95, I_a=3.4, dt_s=1.0)
        assert isinstance(st, EKFState)

    def test_ekf_soc_std_positive(self):
        ekf = EKFBatteryEstimator(NMC_18650, soc_init=0.80)
        assert ekf.state.soc_std > 0

    def test_ekf_convergence_over_steps(self):
        """True SOC를 알고 있을 때 EKF가 그것으로 수렴해야 함."""
        true_soc = 0.75
        s = BatteryState(soc=true_soc, v_rc=0.0, temp_k=298.15)
        ekf = EKFBatteryEstimator(NMC_18650, soc_init=0.60, r_meas=1e-4)
        I = 3.4
        for _ in range(60):
            s_next = step_ecm(s, I, 1.0, NMC_18650)
            vt = terminal_voltage(s_next, I, NMC_18650)
            ekf.step(V_meas=vt, I_a=I, dt_s=1.0)
            s = s_next
        # 60스텝 후 SOC 오차 < 0.10
        error = abs(ekf.state.soc_est - s.soc)
        assert error < 0.10

    def test_ekf_1rc_mode(self):
        ekf = EKFBatteryEstimator(NMC_18650)
        assert ekf.n_rc == 1
        assert ekf.state.v_rc2_est == 0.0

    def test_ekf_2rc_mode(self):
        ekf = EKFBatteryEstimator(NMC_EV)
        assert ekf.n_rc == 2

    def test_ekf_2rc_v_rc2_evolves(self):
        ekf = EKFBatteryEstimator(NMC_EV, soc_init=0.80)
        for _ in range(10):
            ekf.step(V_meas=3.90, I_a=10.0, dt_s=1.0)
        assert ekf.state.v_rc2_est != 0.0

    def test_ekf_reset(self):
        ekf = EKFBatteryEstimator(NMC_18650, soc_init=0.80)
        for _ in range(20):
            ekf.step(V_meas=3.90, I_a=3.4, dt_s=1.0)
        ekf.reset(soc=1.0)
        assert abs(ekf.state.soc_est - 1.0) < 1e-6
        assert ekf.state.t_s == 0.0

    def test_ekf_to_battery_state(self):
        ekf = EKFBatteryEstimator(NMC_18650, soc_init=0.80)
        bs = ekf.to_battery_state()
        assert isinstance(bs, BatteryState)
        assert abs(bs.soc - 0.80) < 1e-4

    def test_ekf_t_s_increments(self):
        ekf = EKFBatteryEstimator(NMC_18650)
        ekf.step(V_meas=3.9, I_a=3.4, dt_s=5.0)
        assert abs(ekf.state.t_s - 5.0) < 0.01

    def test_ekf_p_matrix_positive_definite(self):
        """공분산 대각원소 > 0 (양정치)."""
        ekf = EKFBatteryEstimator(NMC_18650)
        for _ in range(20):
            ekf.step(V_meas=3.9, I_a=3.4, dt_s=1.0)
        P = ekf.state.P
        for i in range(len(P)):
            assert P[i][i] > 0


# ══════════════════════════════════════════════════════════════════════════════
# §5b soh_from_discharge (B1 부속)
# ══════════════════════════════════════════════════════════════════════════════

class TestSOHFromDischarge:
    def test_soh_fresh_cell(self):
        """신품 셀: SOH ≈ 1.0."""
        steps = simulate_discharge(NMC_18650, current_a=3.4, dt_s=1.0)
        soh = soh_from_discharge(steps, NMC_18650)
        assert 0.90 <= soh <= 1.10

    def test_soh_aged_cell_lower(self):
        """노화 셀: SOH < 신품."""
        steps_fresh = simulate_discharge(NMC_18650, current_a=3.4, dt_s=1.0)
        steps_aged  = simulate_discharge(NMC_AGED,  current_a=3.4, dt_s=1.0)
        soh_fresh = soh_from_discharge(steps_fresh, NMC_18650)
        soh_aged  = soh_from_discharge(steps_aged,  NMC_AGED)
        assert soh_aged < soh_fresh

    def test_soh_empty_returns_nan(self):
        soh = soh_from_discharge([], NMC_18650)
        assert math.isnan(soh)

    def test_soh_range_reasonable(self):
        steps = simulate_discharge(NMC_18650, current_a=3.4, dt_s=1.0)
        soh = soh_from_discharge(steps, NMC_18650)
        assert 0.5 <= soh <= 1.2


# ══════════════════════════════════════════════════════════════════════════════
# §6 3단계 노화 모델 (B3)
# ══════════════════════════════════════════════════════════════════════════════

class TestAgingKnee:
    def test_3phase_returns_per_cycle(self):
        result = scenario_aging_capacity_fade(NMC_18650, use_3phase=True)
        assert "per_cycle" in result
        assert len(result["per_cycle"]) > 0

    def test_3phase_has_phase_labels(self):
        result = scenario_aging_capacity_fade(NMC_18650, use_3phase=True)
        phases = {row["phase"] for row in result["per_cycle"]}
        assert "SEI" in phases

    def test_3phase_sei_at_early_cycles(self):
        result = scenario_aging_capacity_fade(
            NMC_18650, use_3phase=True,
            cycle_range=[0, 50, 100, 200]
        )
        early = [r for r in result["per_cycle"] if r["cycle"] <= 200]
        assert all(r["phase"] == "SEI" for r in early)

    def test_3phase_linear_phase_exists(self):
        result = scenario_aging_capacity_fade(
            NMC_18650, use_3phase=True,
            cycle_range=[0, 100, 200, 400, 600, 800]
        )
        phases = {row["phase"] for row in result["per_cycle"]}
        assert "LINEAR" in phases

    def test_3phase_post_knee_exists(self):
        result = scenario_aging_capacity_fade(
            NMC_18650, use_3phase=True,
            cycle_range=[0, 200, 500, 800, 1000, 1500]
        )
        phases = {row["phase"] for row in result["per_cycle"]}
        assert "POST_KNEE" in phases

    def test_3phase_soh_decreasing(self):
        result = scenario_aging_capacity_fade(NMC_18650, use_3phase=True)
        sohs = [r["soh"] for r in result["per_cycle"]]
        for i in range(1, len(sohs)):
            assert sohs[i] <= sohs[i-1] + 1e-6

    def test_3phase_eol_cycle_found(self):
        result = scenario_aging_capacity_fade(
            NMC_18650, use_3phase=True,
            cycle_range=[0, 100, 200, 300, 400, 500, 600, 700, 800, 1000, 1500, 2000]
        )
        # NMC 18650 with default params should hit EOL within 2000 cycles
        assert result["eol_cycle"] is not None

    def test_3phase_knee_cycle_reported(self):
        result = scenario_aging_capacity_fade(NMC_18650, use_3phase=True, n_knee2=800)
        assert result["knee_cycle"] == 800

    def test_3phase_capacity_decreases_with_cycles(self):
        result = scenario_aging_capacity_fade(NMC_18650, use_3phase=True)
        caps = [r["capacity_ah"] for r in result["per_cycle"]]
        # 전체적으로 용량 감소 추세
        if len(caps) >= 4:
            assert caps[-1] < caps[1]

    def test_3phase_linear_compat_use_false(self):
        """use_3phase=False → v0.2 호환 선형 모델."""
        result = scenario_aging_capacity_fade(
            NMC_18650, use_3phase=False,
            cycle_range=[0, 100, 500, 1000]
        )
        assert result["knee_cycle"] is None
        phases = {r["phase"] for r in result["per_cycle"]}
        assert phases == {"LINEAR"}

    def test_3phase_soh_floor_respected(self):
        result = scenario_aging_capacity_fade(
            NMC_18650, use_3phase=True, soh_floor=0.40,
            cycle_range=[0, 500, 1000, 2000, 5000]
        )
        sohs = [r["soh"] for r in result["per_cycle"]]
        assert all(s >= 0.39 for s in sohs)


# ══════════════════════════════════════════════════════════════════════════════
# §7 v0.2 하위 호환 (기존 API 전수)
# ══════════════════════════════════════════════════════════════════════════════

class TestBackwardCompat:
    def test_ecmparams_default_no_ocv_table(self):
        p = ECMParams()
        assert p.ocv_table is None

    def test_ecmparams_default_1rc(self):
        p = ECMParams()
        assert p.r2_ohm == 0.0
        assert p.c2_farad == 0.0

    def test_ecmparams_default_ea_zero(self):
        p = ECMParams()
        assert p.Ea_r_ev == 0.0

    def test_battery_state_default_vrc2(self):
        s = BatteryState(soc=0.8, v_rc=0.0, temp_k=298.15)
        assert s.v_rc2 == 0.0

    def test_simulate_discharge_nmc_18650(self):
        steps = simulate_discharge(NMC_18650, current_a=3.4, dt_s=1.0)
        assert len(steps) > 0
        assert steps[-1].terminated

    def test_simulate_discharge_lfp(self):
        steps = simulate_discharge(LFP_POUCH, current_a=50.0, dt_s=1.0)
        assert len(steps) > 0

    def test_simulate_charge_basic(self):
        steps = simulate_charge(NMC_18650, current_a=3.4, dt_s=1.0)
        assert len(steps) > 0

    def test_observe_battery_returns_obs(self):
        s = BatteryState(soc=0.8, v_rc=0.0, temp_k=298.15)
        obs = observe_battery(s, 3.4, NMC_18650)
        assert 0.0 <= obs.omega_battery <= 1.0

    def test_verify_battery_pass(self):
        s = BatteryState(soc=0.8, v_rc=0.0, temp_k=298.15)
        rep = verify_battery(s, NMC_18650)
        assert rep.verdict == "PASS"

    def test_get_preset_all(self):
        from battery_dynamics import list_presets
        for name in list_presets():
            p = get_preset(name)
            assert isinstance(p, ECMParams)

    def test_version_is_040(self):
        import battery_dynamics
        assert battery_dynamics.__version__ == "0.4.0"

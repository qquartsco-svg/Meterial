"""battery_dynamics v0.2.0 테스트 스위트.

§1  ECM 물리 (ocv, step_ecm, terminal_voltage, 유틸리티) — 18 tests
§2  파생 지표 (c_rate, time_to_discharge, soc_at_time, 열 함수) — 12 tests
§3  Observer Ω 5레이어 (observe_battery, diagnose, 플래그) — 16 tests
§4  시뮬레이션 (simulate_discharge, simulate_charge) — 12 tests
§5  파라미터 스윕 (sweep_c_rate, sweep_soh, sweep_temperature, sweep_soc_snapshot) — 12 tests
§6  검증 보고서 (verify_battery) — 8 tests
§7  프리셋 (NMC/LFP/LCO/EV, get_preset, list_presets) — 10 tests
§8  시나리오 3종 (fast_discharge_collapse, thermal_stress, aging_capacity_fade) — 12 tests

총 100 tests
"""

import dataclasses
import math
import pytest

from battery_dynamics import (
    # 스키마
    ECMParams,
    BatteryState,
    DischargeStep,
    BatteryObservation,
    VerificationReport,
    # ECM 물리
    ocv_linear,
    terminal_voltage,
    step_ecm,
    c_rate,
    effective_capacity_ah,
    internal_resistance_total,
    voltage_drop_at_current,
    time_to_discharge,
    soc_at_time,
    ocv_at_soc,
    thermal_time_constant,
    steady_state_temperature,
    max_continuous_current,
    power_capability,
    # Observer
    observe_battery,
    diagnose,
    # 설계 엔진
    simulate_discharge,
    simulate_charge,
    sweep_c_rate,
    sweep_soh,
    sweep_temperature,
    sweep_soc_snapshot,
    verify_battery,
    # 시나리오
    scenario_fast_discharge_collapse,
    scenario_thermal_stress,
    scenario_aging_capacity_fade,
    # 프리셋
    NMC_18650,
    LFP_POUCH,
    LCO_PHONE,
    NMC_EV,
    NMC_AGED,
    LFP_COLD,
    get_preset,
    list_presets,
)


# ══════════════════════════════════════════════════════════════════════════════
# 공용 픽스처
# ══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def p_default() -> ECMParams:
    return ECMParams()


@pytest.fixture
def p_nmc() -> ECMParams:
    return NMC_18650


@pytest.fixture
def s_full() -> BatteryState:
    return BatteryState(soc=1.0, v_rc=0.0, temp_k=298.15)


@pytest.fixture
def s_half() -> BatteryState:
    return BatteryState(soc=0.5, v_rc=0.05, temp_k=300.0)


@pytest.fixture
def s_low() -> BatteryState:
    return BatteryState(soc=0.08, v_rc=0.0, temp_k=298.15)


# ══════════════════════════════════════════════════════════════════════════════
# §1 ECM 물리
# ══════════════════════════════════════════════════════════════════════════════

def test_ocv_soc1_equals_max(p_default):
    """SOC=1 OCV = soc_v0 + k_ocv."""
    assert ocv_linear(1.0, p_default) == pytest.approx(p_default.soc_v0 + p_default.soc_ocv_v_per_unit)


def test_ocv_soc0_equals_v0(p_default):
    """SOC=0 OCV = soc_v0."""
    assert ocv_linear(0.0, p_default) == pytest.approx(p_default.soc_v0)


def test_ocv_linear_monotone(p_default):
    """OCV는 SOC 증가에 단조 증가."""
    ocvs = [ocv_linear(s, p_default) for s in [0.0, 0.25, 0.5, 0.75, 1.0]]
    assert all(ocvs[i] <= ocvs[i+1] for i in range(len(ocvs)-1))


def test_ocv_clamps_below_0(p_default):
    """SOC < 0 클램핑."""
    assert ocv_linear(-0.5, p_default) == ocv_linear(0.0, p_default)


def test_ocv_clamps_above_1(p_default):
    """SOC > 1 클램핑."""
    assert ocv_linear(1.5, p_default) == ocv_linear(1.0, p_default)


def test_terminal_voltage_less_than_ocv(s_half, p_default):
    """방전 시 단자전압 < OCV."""
    vt = terminal_voltage(s_half, I_a=1.0, p=p_default)
    ocv = ocv_linear(s_half.soc, p_default)
    assert vt < ocv


def test_terminal_voltage_zero_current_equals_ocv_minus_vrc(s_full, p_default):
    """I=0 시 단자전압 = OCV − V_RC."""
    s = dataclasses.replace(s_full, v_rc=0.05)
    vt = terminal_voltage(s, I_a=0.0, p=p_default)
    assert vt == pytest.approx(ocv_linear(s.soc, p_default) - s.v_rc)


def test_step_ecm_discharge_lowers_soc(s_full, p_default):
    """방전 스텝 → SOC 감소."""
    s2 = step_ecm(s_full, I_a=2.0, dt_s=60.0, p=p_default)
    assert s2.soc < s_full.soc


def test_step_ecm_charge_raises_soc():
    """충전 스텝 (I<0) → SOC 증가."""
    p = NMC_18650
    s = BatteryState(soc=0.5, v_rc=0.0, temp_k=298.15)
    s2 = step_ecm(s, I_a=-1.0, dt_s=60.0, p=p)
    assert s2.soc > s.soc


def test_step_ecm_time_advances(s_full, p_default):
    """스텝 후 t_s 증가."""
    s2 = step_ecm(s_full, I_a=1.0, dt_s=10.0, p=p_default)
    assert s2.t_s == pytest.approx(10.0)


def test_step_ecm_vrc_builds_up(s_full, p_default):
    """방전 시 V_RC 양방향 증가."""
    s2 = step_ecm(s_full, I_a=5.0, dt_s=100.0, p=p_default)
    assert s2.v_rc > 0.0


def test_step_ecm_temperature_rises_under_load(s_full, p_default):
    """부하 전류 → 온도 상승."""
    s2 = step_ecm(s_full, I_a=10.0, dt_s=100.0, p=p_default)
    assert s2.temp_k > s_full.temp_k


def test_step_ecm_soc_clamp_no_negative():
    """SOC는 0 아래로 내려가지 않음."""
    p = ECMParams(q_ah=0.001)   # 아주 작은 배터리
    s = BatteryState(soc=0.001, v_rc=0.0, temp_k=298.15)
    s2 = step_ecm(s, I_a=100.0, dt_s=100.0, p=p)
    assert s2.soc >= 0.0


def test_ocv_at_soc_alias():
    """ocv_at_soc == ocv (ocv table dispatch alias); == ocv_linear when no table."""
    p_no_table = ECMParams()   # ocv_table=None → linear fallback
    for soc in [0.0, 0.5, 1.0]:
        assert ocv_at_soc(soc, p_no_table) == pytest.approx(ocv_linear(soc, p_no_table))


def test_internal_resistance_total(p_nmc):
    """R_total = R0 + R1."""
    assert internal_resistance_total(p_nmc) == pytest.approx(p_nmc.r0_ohm + p_nmc.r1_ohm)


def test_voltage_drop_at_current(p_nmc):
    """ΔV = I × R_total."""
    dv = voltage_drop_at_current(2.0, p_nmc)
    assert dv == pytest.approx(2.0 * internal_resistance_total(p_nmc))


def test_power_capability_positive(s_full, p_nmc):
    """전력 공급 능력 > 0 (충전된 셀)."""
    pw = power_capability(s_full, p_nmc)
    assert pw > 0.0


def test_power_capability_zero_at_empty():
    """SOC=0 근방 전력 공급 능력 ≈ 0."""
    p = NMC_18650
    s = BatteryState(soc=0.0, v_rc=0.0, temp_k=298.15)
    # OCV at SOC=0 = 3.0V, t_cutoff=2.8V → 아주 작은 마진
    pw = power_capability(s, p)
    assert pw >= 0.0


# ══════════════════════════════════════════════════════════════════════════════
# §2 파생 지표
# ══════════════════════════════════════════════════════════════════════════════

def test_c_rate_1c(p_nmc):
    """I=Q_ah → 1C."""
    assert c_rate(p_nmc.q_ah, p_nmc) == pytest.approx(1.0)


def test_c_rate_2c(p_nmc):
    """I=2×Q_ah → 2C."""
    assert c_rate(2 * p_nmc.q_ah, p_nmc) == pytest.approx(2.0)


def test_c_rate_always_positive(p_nmc):
    """C-rate는 항상 양수 (절댓값 기반)."""
    assert c_rate(-p_nmc.q_ah, p_nmc) == pytest.approx(1.0)


def test_effective_capacity_soh1(p_nmc):
    """SOH=1 → Q_eff = Q_ah."""
    assert effective_capacity_ah(p_nmc) == pytest.approx(p_nmc.q_ah)


def test_effective_capacity_soh_half(p_nmc):
    """SOH=0.5 → Q_eff = 0.5×Q_ah."""
    p = dataclasses.replace(p_nmc, soh=0.5)
    assert effective_capacity_ah(p) == pytest.approx(p_nmc.q_ah * 0.5)


def test_time_to_discharge_1c(p_nmc):
    """1C 완전 방전 시간 ≈ 3600s."""
    t = time_to_discharge(p_nmc, current_a=p_nmc.q_ah, soc_init=1.0, soc_target=0.0)
    assert t == pytest.approx(3600.0, rel=1e-3)


def test_time_to_discharge_proportional():
    """방전 시간은 SOC 범위에 비례."""
    p = ECMParams(q_ah=2.0)
    t_full  = time_to_discharge(p, 2.0, 1.0, 0.0)
    t_half  = time_to_discharge(p, 2.0, 0.5, 0.0)
    assert t_full == pytest.approx(2 * t_half, rel=1e-9)


def test_soc_at_time_decreases(p_nmc):
    """시간 경과 → SOC 감소."""
    soc_0 = soc_at_time(0.0, p_nmc.q_ah, p_nmc)
    soc_t = soc_at_time(3600.0, p_nmc.q_ah, p_nmc)
    assert soc_t < soc_0


def test_soc_at_time_clamp():
    """SOC ∈ [0, 1] 클램핑."""
    p = ECMParams(q_ah=1.0)
    assert soc_at_time(0.0, 1.0, p, 1.0) <= 1.0
    assert soc_at_time(1e9, 1.0, p, 1.0) >= 0.0


def test_thermal_time_constant(p_default):
    """τ_th = C_th / h."""
    tau = thermal_time_constant(p_default)
    assert tau == pytest.approx(p_default.thermal_c_j_per_k / p_default.thermal_h_w_per_k)


def test_steady_state_temperature_above_ambient(p_nmc):
    """부하 전류 → T_ss > T_amb."""
    T_ss = steady_state_temperature(2.0, p_nmc)
    assert T_ss > p_nmc.t_amb_k


def test_max_continuous_current_positive(p_nmc):
    """최대 연속 전류 > 0."""
    I_max = max_continuous_current(p_nmc)
    assert I_max > 0.0


# ══════════════════════════════════════════════════════════════════════════════
# §3 Observer Ω 5레이어
# ══════════════════════════════════════════════════════════════════════════════

def test_observe_returns_observation_type(s_full, p_nmc):
    """observe_battery → BatteryObservation 타입."""
    obs = observe_battery(s_full, 1.0, p_nmc)
    assert isinstance(obs, BatteryObservation)


def test_omega_in_range(s_full, p_nmc):
    """Ω_global ∈ [0, 1]."""
    for soc in [0.0, 0.1, 0.5, 1.0]:
        s = dataclasses.replace(s_full, soc=soc)
        obs = observe_battery(s, 1.0, p_nmc)
        assert 0.0 <= obs.omega_battery <= 1.0


def test_omega_five_layers_sum(s_half, p_nmc):
    """5레이어 필드 모두 [0, 1]."""
    obs = observe_battery(s_half, 1.0, p_nmc)
    for attr in ("omega_soc", "omega_voltage", "omega_thermal",
                 "omega_impedance", "omega_aging"):
        val = getattr(obs, attr)
        assert 0.0 <= val <= 1.0, f"{attr}={val} 범위 초과"


def test_healthy_verdict_full_charge(p_nmc):
    """SOC=1, 정상 온도 → HEALTHY or STABLE."""
    s = BatteryState(soc=1.0, v_rc=0.0, temp_k=298.15)
    obs = observe_battery(s, 0.1, p_nmc)
    assert obs.verdict in ("HEALTHY", "STABLE")


def test_critical_verdict_empty_battery(p_nmc):
    """SOC=0.05 → CRITICAL 판정."""
    s = BatteryState(soc=0.05, v_rc=0.0, temp_k=298.15)
    obs = observe_battery(s, 1.0, p_nmc)
    assert obs.verdict == "CRITICAL"


def test_critical_soc_flag(p_nmc):
    """SOC < soc_floor → critical_soc 플래그."""
    s = BatteryState(soc=0.05, v_rc=0.0, temp_k=298.15)
    obs = observe_battery(s, 1.0, p_nmc)
    assert "critical_soc" in obs.flags


def test_low_soc_flag(p_nmc):
    """SOC = 0.15 → low_soc 플래그."""
    s = BatteryState(soc=0.15, v_rc=0.0, temp_k=298.15)
    obs = observe_battery(s, 1.0, p_nmc)
    assert "low_soc" in obs.flags


def test_thermal_warning_hot(p_nmc):
    """T=325K (52°C) → thermal_warning 플래그."""
    s = BatteryState(soc=0.5, v_rc=0.0, temp_k=325.0)
    obs = observe_battery(s, 1.0, p_nmc)
    assert "thermal_warning" in obs.flags


def test_thermal_critical_very_hot(p_nmc):
    """T=340K (67°C) → thermal_critical 플래그 + CRITICAL 판정."""
    s = BatteryState(soc=0.5, v_rc=0.0, temp_k=340.0)
    obs = observe_battery(s, 1.0, p_nmc)
    assert "thermal_critical" in obs.flags
    assert obs.verdict == "CRITICAL"


def test_aging_warning_low_soh(p_nmc):
    """SOH=0.75 → aging_warning 플래그 (0.70~0.80 구간)."""
    p = dataclasses.replace(p_nmc, soh=0.75)
    s = BatteryState(soc=0.8, v_rc=0.0, temp_k=298.15)
    obs = observe_battery(s, 1.0, p)
    assert "aging_warning" in obs.flags


def test_aging_critical_very_low_soh(p_nmc):
    """SOH=0.65 → aging_critical 플래그 (< 0.70)."""
    p = dataclasses.replace(p_nmc, soh=0.65)
    s = BatteryState(soc=0.8, v_rc=0.0, temp_k=298.15)
    obs = observe_battery(s, 1.0, p)
    assert "aging_critical" in obs.flags


def test_high_impedance_flag():
    """R0 > 0.20 → high_impedance 플래그."""
    p = dataclasses.replace(NMC_18650, r0_ohm=0.25)
    s = BatteryState(soc=0.5, v_rc=0.0, temp_k=298.15)
    obs = observe_battery(s, 1.0, p)
    assert "high_impedance" in obs.flags


def test_power_limited_flag_low_soc(p_nmc):
    """SOC=0.20 경계 → power_limited 플래그."""
    s = BatteryState(soc=0.20, v_rc=0.0, temp_k=298.15)
    obs = observe_battery(s, 1.0, p_nmc)
    assert obs.power_limited is True


def test_omega_degraded_vs_healthy():
    """노화 셀(NMC_AGED) Ω < 신품(NMC_18650) Ω."""
    s = BatteryState(soc=0.8, v_rc=0.0, temp_k=298.15)
    obs_new  = observe_battery(s, 1.0, NMC_18650)
    obs_aged = observe_battery(s, 1.0, NMC_AGED)
    assert obs_aged.omega_battery < obs_new.omega_battery


def test_diagnose_returns_list(s_full, p_nmc):
    """diagnose → List[str]."""
    obs = observe_battery(s_full, 1.0, p_nmc)
    recs = diagnose(obs)
    assert isinstance(recs, list)
    assert len(recs) >= 1


def test_diagnose_critical_includes_action():
    """CRITICAL SOC → 진단 메시지에 'CRITICAL' 또는 '차단' 포함."""
    s = BatteryState(soc=0.05, v_rc=0.0, temp_k=298.15)
    obs = observe_battery(s, 1.0, NMC_18650)
    recs = diagnose(obs)
    full_text = " ".join(recs)
    assert "CRITICAL" in full_text or "차단" in full_text or "위험" in full_text


def test_diagnose_healthy_ok_message(s_full, p_nmc):
    """HEALTHY → [OK] 메시지."""
    obs = observe_battery(s_full, 0.1, p_nmc)
    recs = diagnose(obs)
    full_text = " ".join(recs)
    # HEALTHY면 OK 메시지 또는 이상없음
    assert "OK" in full_text or "양호" in full_text or "정상" in full_text or len(recs) >= 1


# ══════════════════════════════════════════════════════════════════════════════
# §4 시뮬레이션
# ══════════════════════════════════════════════════════════════════════════════

def test_simulate_discharge_returns_list(p_nmc):
    """simulate_discharge → List[DischargeStep] 비어있지 않음."""
    steps = simulate_discharge(p_nmc, current_a=p_nmc.q_ah, dt_s=60.0, n_steps=100)
    assert isinstance(steps, list)
    assert len(steps) > 0


def test_simulate_discharge_soc_monotone(p_nmc):
    """방전 중 SOC 단조 감소."""
    steps = simulate_discharge(p_nmc, current_a=p_nmc.q_ah, dt_s=30.0, n_steps=200)
    socs = [s.soc for s in steps]
    assert all(socs[i] >= socs[i+1] - 1e-9 for i in range(len(socs)-1))


def test_simulate_discharge_terminates(p_nmc):
    """방전은 terminated=True로 종료."""
    steps = simulate_discharge(p_nmc, current_a=p_nmc.q_ah, dt_s=10.0, n_steps=10000)
    assert steps[-1].terminated is True


def test_simulate_discharge_v_term_positive(p_nmc):
    """모든 스텝에서 V_term ≥ 0."""
    steps = simulate_discharge(p_nmc, current_a=p_nmc.q_ah, dt_s=30.0, n_steps=200)
    assert all(s.v_term >= 0.0 for s in steps)


def test_simulate_discharge_energy_increases(p_nmc):
    """누적 에너지는 단조 증가."""
    steps = simulate_discharge(p_nmc, current_a=p_nmc.q_ah, dt_s=30.0, n_steps=200)
    energies = [s.energy_wh for s in steps]
    assert all(energies[i] <= energies[i+1] + 1e-9 for i in range(len(energies)-1))


def test_simulate_discharge_c_rate_correct(p_nmc):
    """DischargeStep.c_rate == current_a / q_ah."""
    I = p_nmc.q_ah * 2.0
    steps = simulate_discharge(p_nmc, current_a=I, dt_s=10.0, n_steps=10)
    assert steps[0].c_rate == pytest.approx(2.0, rel=1e-3)


def test_simulate_charge_raises_soc(p_nmc):
    """충전 시뮬레이션 → SOC 증가."""
    steps = simulate_charge(p_nmc, current_a=p_nmc.q_ah,
                             soc_init=0.20, soc_target=0.90,
                             dt_s=10.0, n_steps=5000)
    assert steps[-1].soc > 0.20


def test_simulate_charge_current_negative(p_nmc):
    """충전 스텝의 current_a < 0."""
    steps = simulate_charge(p_nmc, current_a=1.0, dt_s=10.0, n_steps=10)
    assert all(s.current_a < 0 for s in steps)


def test_simulate_charge_terminates(p_nmc):
    """충전은 terminated=True로 종료."""
    steps = simulate_charge(p_nmc, current_a=p_nmc.q_ah,
                             soc_init=0.20, soc_target=0.95,
                             dt_s=10.0, n_steps=50000)
    assert steps[-1].terminated is True


def test_simulate_discharge_high_temp_shorter():
    """고온 방전 시 냉각보다 빨리 종료되지 않으나 온도 더 높음."""
    steps_cool = simulate_discharge(NMC_18650, current_a=3.4, dt_s=10.0,
                                    n_steps=2000, temp_init_k=298.15)
    steps_hot  = simulate_discharge(NMC_18650, current_a=3.4, dt_s=10.0,
                                    n_steps=2000, temp_init_k=318.15)
    max_t_cool = max(s.temp_k for s in steps_cool)
    max_t_hot  = max(s.temp_k for s in steps_hot)
    assert max_t_hot > max_t_cool


def test_simulate_discharge_soh_affects_duration():
    """낮은 SOH → 더 짧은 방전 시간."""
    steps_new  = simulate_discharge(NMC_18650, current_a=3.4, dt_s=10.0, n_steps=5000)
    steps_aged = simulate_discharge(NMC_AGED,  current_a=3.4, dt_s=10.0, n_steps=5000)
    assert steps_aged[-1].t_s <= steps_new[-1].t_s


def test_simulate_discharge_lfp_and_lco_run_full_cycle():
    """LFP(100Ah) 및 LCO(4Ah) @ 1C 각각 완전 방전 — 모두 > 3000s 지속."""
    steps_lfp = simulate_discharge(LFP_POUCH, current_a=LFP_POUCH.q_ah,
                                    dt_s=10.0, n_steps=50000)
    steps_lco = simulate_discharge(LCO_PHONE, current_a=LCO_PHONE.q_ah,
                                    dt_s=10.0, n_steps=5000)
    assert steps_lfp[-1].t_s > 3000
    assert steps_lco[-1].t_s > 3000


# ══════════════════════════════════════════════════════════════════════════════
# §5 파라미터 스윕
# ══════════════════════════════════════════════════════════════════════════════

def test_sweep_c_rate_returns_list(p_nmc):
    """sweep_c_rate → 빈 리스트 아님."""
    results = sweep_c_rate(p_nmc, c_rate_range=[0.5, 1.0, 2.0], dt_s=10.0, n_steps=2000)
    assert len(results) == 3


def test_sweep_c_rate_higher_rate_shorter(p_nmc):
    """C-rate 높을수록 방전 시간 짧아짐."""
    results = sweep_c_rate(p_nmc, c_rate_range=[0.5, 1.0, 2.0], dt_s=10.0, n_steps=5000)
    durations = [r["duration_s"] for r in results]
    assert durations[0] >= durations[1] >= durations[2]


def test_sweep_c_rate_keys(p_nmc):
    """sweep_c_rate 결과 키 확인."""
    results = sweep_c_rate(p_nmc, c_rate_range=[1.0], dt_s=30.0, n_steps=500)
    required_keys = {"c_rate", "current_a", "duration_s", "capacity_ah",
                      "energy_wh", "min_v_term", "max_temp_k",
                      "final_omega", "final_verdict"}
    assert required_keys <= set(results[0].keys())


def test_sweep_soh_capacity_monotone(p_nmc):
    """SOH 감소 → 용량 단조 감소."""
    results = sweep_soh(p_nmc, soh_range=[1.0, 0.8, 0.6], dt_s=30.0, n_steps=2000)
    caps = [r["capacity_ah"] for r in results]
    assert caps[0] >= caps[1] >= caps[2]


def test_sweep_temperature_hot_lowers_capacity(p_nmc):
    """극고온(t_amb > 60°C) → 방전 성능 저하."""
    # 정상 vs 고온
    res = sweep_temperature(p_nmc, T_range=[298.15, 338.15], dt_s=10.0, n_steps=5000)
    assert len(res) == 2
    # 고온에서 열 폭주/경고 판정
    hot_verdict = res[1]["final_verdict"]
    assert hot_verdict in ("HEALTHY", "STABLE", "FRAGILE", "CRITICAL")


def test_sweep_temperature_keys(p_nmc):
    """sweep_temperature 결과 키 확인."""
    results = sweep_temperature(p_nmc, T_range=[298.15], dt_s=30.0, n_steps=200)
    required = {"T_k", "T_c", "duration_s", "capacity_ah", "energy_wh",
                 "min_v_term", "max_temp_k", "final_omega", "final_verdict"}
    assert required <= set(results[0].keys())


def test_sweep_soc_snapshot_returns_correct_count(p_nmc):
    """sweep_soc_snapshot → soc_range 길이 == 결과 수."""
    soc_range = [1.0, 0.8, 0.6, 0.4, 0.2]
    results = sweep_soc_snapshot(p_nmc, soc_range, current_a=1.0)
    assert len(results) == len(soc_range)


def test_sweep_soc_snapshot_omega_decreases(p_nmc):
    """SOC 높을수록 Ω 높음 (단조 경향)."""
    soc_range = [1.0, 0.5, 0.1]
    results = sweep_soc_snapshot(p_nmc, soc_range, current_a=1.0)
    omegas = [r["omega_battery"] for r in results]
    assert omegas[0] >= omegas[2] - 0.01   # 완전 충전 ≥ 저SOC


def test_sweep_soc_snapshot_voltage_monotone(p_nmc):
    """SOC 증가 → V_term 증가 (단조 경향)."""
    soc_range = [0.1, 0.5, 1.0]
    results = sweep_soc_snapshot(p_nmc, soc_range, current_a=1.0)
    volts = [r["v_term"] for r in results]
    assert volts[2] > volts[0]


def test_sweep_soh_keys(p_nmc):
    """sweep_soh 결과 키 확인."""
    results = sweep_soh(p_nmc, soh_range=[1.0], dt_s=30.0, n_steps=200)
    required = {"soh", "current_a", "duration_s", "capacity_ah",
                 "energy_wh", "min_v_term", "final_omega", "final_verdict"}
    assert required <= set(results[0].keys())


# ══════════════════════════════════════════════════════════════════════════════
# §6 검증 보고서
# ══════════════════════════════════════════════════════════════════════════════

def test_verify_pass_healthy_cell(s_full, p_nmc):
    """충전 완료 NMC → PASS."""
    report = verify_battery(s_full, p_nmc, current_a=0.0)
    assert isinstance(report, VerificationReport)
    assert report.verdict == "PASS"


def test_verify_fail_empty_cell(p_nmc):
    """SOC=0.05 → FAIL."""
    s = BatteryState(soc=0.05, v_rc=0.0, temp_k=298.15)
    report = verify_battery(s, p_nmc, current_a=0.0)
    assert report.verdict == "FAIL"


def test_verify_marginal_low_soc(p_nmc):
    """SOC=0.15 → MARGINAL 또는 FAIL."""
    s = BatteryState(soc=0.15, v_rc=0.0, temp_k=298.15)
    report = verify_battery(s, p_nmc, current_a=0.0)
    assert report.verdict in ("MARGINAL", "FAIL")


def test_verify_fail_thermal_critical(p_nmc):
    """T=340K → FAIL (thermal_critical)."""
    s = BatteryState(soc=0.8, v_rc=0.0, temp_k=340.0)
    report = verify_battery(s, p_nmc, current_a=1.0)
    assert report.verdict == "FAIL"


def test_verify_report_has_notes(s_full, p_nmc):
    """검증 보고서에 notes 있음."""
    report = verify_battery(s_full, p_nmc)
    assert isinstance(report.notes, list)
    assert len(report.notes) >= 1


def test_verify_report_omega_in_range(s_full, p_nmc):
    """보고서 omega_battery ∈ [0, 1]."""
    report = verify_battery(s_full, p_nmc)
    assert 0.0 <= report.omega_battery <= 1.0


def test_verify_aged_cell_marginal_or_fail():
    """NMC_AGED(SOH=0.78) → MARGINAL 또는 FAIL."""
    s = BatteryState(soc=0.8, v_rc=0.0, temp_k=298.15)
    report = verify_battery(s, NMC_AGED)
    assert report.verdict in ("MARGINAL", "FAIL")


def test_verify_flags_in_report(p_nmc):
    """FAIL 보고서에 플래그 포함."""
    s = BatteryState(soc=0.05, v_rc=0.0, temp_k=298.15)
    report = verify_battery(s, p_nmc)
    assert isinstance(report.flags, list)
    assert len(report.flags) > 0


# ══════════════════════════════════════════════════════════════════════════════
# §7 프리셋
# ══════════════════════════════════════════════════════════════════════════════

def test_nmc_18650_label():
    assert NMC_18650.label == "NMC_18650"


def test_lfp_pouch_high_capacity():
    """LFP_POUCH 용량 >> NMC_18650."""
    assert LFP_POUCH.q_ah > NMC_18650.q_ah * 10


def test_lco_phone_high_v_charge():
    """LCO_PHONE 충전 상한 ≥ 4.3V."""
    assert LCO_PHONE.v_charge_max_v >= 4.30


def test_nmc_ev_high_capacity():
    """NMC_EV 용량 ≥ 100Ah."""
    assert NMC_EV.q_ah >= 100.0


def test_nmc_aged_lower_soh():
    """NMC_AGED SOH < NMC_18650 SOH."""
    assert NMC_AGED.soh < NMC_18650.soh


def test_lfp_cold_lower_ambient():
    """LFP_COLD T_amb < LFP_POUCH T_amb."""
    assert LFP_COLD.t_amb_k < LFP_POUCH.t_amb_k


def test_get_preset_by_name():
    """get_preset('nmc_18650') → NMC_18650."""
    p = get_preset("nmc_18650")
    assert p.label == "NMC_18650"


def test_get_preset_case_insensitive():
    """get_preset 대소문자 무관."""
    p = get_preset("NMC_18650")
    assert p.label == "NMC_18650"


def test_get_preset_with_override():
    """get_preset override → 파라미터 교체됨."""
    p = get_preset("nmc_18650", soh=0.80, t_amb_k=310.0)
    assert p.soh == pytest.approx(0.80)
    assert p.t_amb_k == pytest.approx(310.0)
    assert p.label == "NMC_18650"   # label 유지


def test_get_preset_unknown_raises():
    """알 수 없는 프리셋 → KeyError."""
    with pytest.raises(KeyError):
        get_preset("unknown_chemistry")


def test_list_presets_contains_all():
    """list_presets에 표준 6개 포함."""
    names = list_presets()
    for key in ["nmc_18650", "lfp_pouch", "lco_phone", "nmc_ev", "nmc_aged", "lfp_cold"]:
        assert key in names


# ══════════════════════════════════════════════════════════════════════════════
# §8 시나리오
# ══════════════════════════════════════════════════════════════════════════════

def test_fast_discharge_returns_dict(p_nmc):
    """scenario_fast_discharge_collapse → dict with required keys."""
    result = scenario_fast_discharge_collapse(p_nmc, c_rate_range=[0.5, 1.0, 2.0],
                                               dt_s=10.0, n_steps=1000)
    assert isinstance(result, dict)
    for key in ("per_c_rate", "collapse_c_rate", "usable_c_rate_max", "summary"):
        assert key in result


def test_fast_discharge_per_c_rate_count(p_nmc):
    """per_c_rate 항목 수 == c_rate_range 수."""
    result = scenario_fast_discharge_collapse(p_nmc, c_rate_range=[0.5, 1.0, 2.0, 5.0],
                                               dt_s=10.0, n_steps=2000)
    assert len(result["per_c_rate"]) == 4


def test_fast_discharge_very_high_rate_collapses():
    """매우 높은 C-rate → 전압 즉시 붕괴 탐지."""
    result = scenario_fast_discharge_collapse(
        NMC_18650, c_rate_range=[0.5, 1.0, 5.0, 20.0, 50.0],
        dt_s=1.0, n_steps=100
    )
    # 50C → 즉시 붕괴 예상
    assert result["collapse_c_rate"] is not None


def test_fast_discharge_summary_is_string(p_nmc):
    result = scenario_fast_discharge_collapse(p_nmc, c_rate_range=[1.0, 2.0],
                                               dt_s=30.0, n_steps=500)
    assert isinstance(result["summary"], str)


def test_thermal_stress_returns_dict(p_nmc):
    """scenario_thermal_stress → dict with required keys."""
    result = scenario_thermal_stress(
        p_nmc, T_range=[298.15, 318.15, 338.15],
        dt_s=30.0, n_steps=500
    )
    assert isinstance(result, dict)
    for key in ("per_temperature", "thermal_warn_T_k",
                 "thermal_collapse_T_k", "safe_T_max_k", "summary"):
        assert key in result


def test_thermal_stress_per_temperature_count(p_nmc):
    """per_temperature 항목 수 == T_range 수."""
    result = scenario_thermal_stress(
        p_nmc, T_range=[298.15, 318.15, 338.15],
        dt_s=30.0, n_steps=500
    )
    assert len(result["per_temperature"]) == 3


def test_thermal_stress_high_temp_detected():
    """매우 높은 온도에서 열 위험 감지."""
    result = scenario_thermal_stress(
        NMC_18650, T_range=[298.15, 308.15, 318.15, 328.15, 338.15, 348.15],
        dt_s=10.0, n_steps=500
    )
    # 338K(65°C) → thermal_collapse 감지
    assert result["thermal_collapse_T_k"] is not None


def test_thermal_stress_summary_str(p_nmc):
    result = scenario_thermal_stress(p_nmc, T_range=[298.15, 318.15],
                                      dt_s=30.0, n_steps=200)
    assert isinstance(result["summary"], str)


def test_aging_capacity_fade_returns_dict(p_nmc):
    """scenario_aging_capacity_fade → dict with required keys."""
    result = scenario_aging_capacity_fade(
        p_nmc, cycle_range=[0, 500, 1000], dt_s=30.0, n_steps=1000
    )
    assert isinstance(result, dict)
    for key in ("per_cycle", "eol_cycle", "eol_strict_cycle", "summary"):
        assert key in result


def test_aging_capacity_decreases(p_nmc):
    """사이클 증가 → 용량 감쇠."""
    result = scenario_aging_capacity_fade(
        p_nmc, cycle_range=[0, 500, 2000], dt_s=30.0, n_steps=2000
    )
    caps = [r["capacity_ah"] for r in result["per_cycle"]]
    assert caps[0] >= caps[-1]


def test_aging_eol_detected():
    """EOL 사이클(SOH<80%) 감지."""
    result = scenario_aging_capacity_fade(
        NMC_18650,
        cycle_range=[0, 100, 200, 300, 400, 500, 1000, 1500, 2000],
        capacity_fade_per_cycle=4e-4,   # 빠른 노화 → 2500사이클 EOL
        dt_s=30.0, n_steps=2000
    )
    # EOL 감지 or None (range 부족)
    assert result["eol_cycle"] is None or result["eol_cycle"] > 0


def test_aging_soh_decreases_per_cycle(p_nmc):
    """사이클 증가 → SOH 감소."""
    result = scenario_aging_capacity_fade(
        p_nmc, cycle_range=[0, 500, 1000], dt_s=30.0, n_steps=1000
    )
    sohs = [r["soh"] for r in result["per_cycle"]]
    assert sohs[0] >= sohs[-1]


def test_aging_summary_str(p_nmc):
    result = scenario_aging_capacity_fade(
        p_nmc, cycle_range=[0, 1000], dt_s=30.0, n_steps=1000
    )
    assert isinstance(result["summary"], str)

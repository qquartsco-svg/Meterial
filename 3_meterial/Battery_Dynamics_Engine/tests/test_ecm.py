from battery_dynamics import (
    ECMParams,
    BatteryState,
    observe_battery,
    ocv_linear,
    step_ecm,
    terminal_voltage,
)


def test_discharge_lowers_soc() -> None:
    p = ECMParams(q_ah=1.0, r0_ohm=0.1, r1_ohm=0.05, c1_farad=1000.0)
    s = BatteryState(soc=0.9, v_rc=0.0, temp_k=298.15)
    for _ in range(50):
        s = step_ecm(s, I_a=2.0, dt_s=1.0, p=p)
    assert s.soc < 0.9


def test_terminal_voltage() -> None:
    p = ECMParams()
    s = BatteryState(soc=0.5, v_rc=0.1, temp_k=300.0)
    v = terminal_voltage(s, 1.0, p)
    assert v < ocv_linear(0.5, p)


def test_observer() -> None:
    p = ECMParams()
    s = BatteryState(soc=0.8, v_rc=0.0, temp_k=300.0)
    o = observe_battery(s, 0.5, p)
    assert 0.0 <= o.omega_battery <= 1.0

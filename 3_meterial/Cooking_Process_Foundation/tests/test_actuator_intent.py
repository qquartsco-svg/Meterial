from cooking_process_foundation.actuator_intent import (
    actuator_intent_from_dict,
    actuator_intent_to_dict,
    build_actuator_intent_from_runtime,
)
from cooking_process_foundation.arbiter import ArbiterVerdict
from cooking_process_foundation import (
    FlowEngine,
    FlowStep,
    KitchenObservation,
    KitchenState,
    RecipeFlow,
    SkillRef,
)


def _eng():
    s1 = FlowStep("a", SkillRef("fr", "sear", ""), min_duration_s=1.0, next_on_success="")
    flow = RecipeFlow("f1", "t", "a", (s1,))
    st = KitchenState("a", 0.0, 80.0, None, 0.1)
    return flow, FlowEngine(flow, st)


def test_build_and_roundtrip_dict():
    flow, eng = _eng()
    arb = ArbiterVerdict(pause_mission=False, heat_cap_0_1=0.5, reasons=())
    intent = build_actuator_intent_from_runtime(
        flow, eng, arb, KitchenObservation(0.0, motion_ok=True)
    )
    d = actuator_intent_to_dict(intent)
    assert d["schema_version"] == "actuator_intent.v0.2"
    assert d["heat_ceiling_0_1"] == 0.5
    assert d["skill"]["technique"] == "sear"
    assert d["metrology_targets_active"] is False
    assert d["metrology_satisfied"] is None
    back = actuator_intent_from_dict(d)
    assert back.step_id == intent.step_id
    assert back.heat_ceiling_0_1 == 0.5


def test_estop_when_pause_and_zero_heat():
    flow, eng = _eng()
    arb = ArbiterVerdict(pause_mission=True, heat_cap_0_1=0.0, reasons=("reflex_triggered",))
    intent = build_actuator_intent_from_runtime(flow, eng, arb)
    assert intent.estop_recommended is True
    assert intent.allow_manipulator_motion is False


def test_manipulator_blocked_when_motion_required_but_not_ok():
    s1 = FlowStep(
        "m",
        SkillRef("fr", "sear", ""),
        min_duration_s=1.0,
        require_motion_ok=True,
        next_on_success="",
    )
    flow = RecipeFlow("f1", "t", "m", (s1,))
    st = KitchenState("m", 0.0, 80.0, None, 0.1)
    eng = FlowEngine(flow, st)
    arb = ArbiterVerdict(pause_mission=False, heat_cap_0_1=1.0, reasons=())
    bad = build_actuator_intent_from_runtime(flow, eng, arb, KitchenObservation(0.0, motion_ok=False))
    assert bad.allow_manipulator_motion is False
    good = build_actuator_intent_from_runtime(flow, eng, arb, KitchenObservation(0.0, motion_ok=True))
    assert good.allow_manipulator_motion is True

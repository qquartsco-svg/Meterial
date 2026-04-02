from cooking_process_foundation import (
    METROLOGY_FAIL_BRANCH_KEY,
    FlowEngine,
    FlowStep,
    KitchenObservation,
    KitchenState,
    RecipeFlow,
    SkillRef,
    metrology_failure_branch_eligible,
    metrology_gates_satisfied,
    metrology_reports_complete,
    motion_gate_satisfied,
)


def test_metrology_gates_helpers():
    step = FlowStep(
        "dose",
        SkillRef("fr", "sauce"),
        target_mass_g=100.0,
        mass_tolerance_g=1.0,
        next_on_success="",
    )
    assert not metrology_gates_satisfied(step, KitchenObservation(0.0))
    assert not metrology_gates_satisfied(step, KitchenObservation(0.0, reported_mass_g=102.0))
    assert metrology_gates_satisfied(step, KitchenObservation(0.0, reported_mass_g=100.5))


def test_motion_gate_helpers():
    step = FlowStep("m", SkillRef("fr", "stir"), require_motion_ok=True, next_on_success="")
    assert not motion_gate_satisfied(step, KitchenObservation(0.0))
    assert not motion_gate_satisfied(step, KitchenObservation(0.0, motion_ok=False))
    assert motion_gate_satisfied(step, KitchenObservation(0.0, motion_ok=True))


def test_flow_blocks_on_metrology_then_advances():
    s1 = FlowStep(
        "weigh",
        SkillRef("fr", "prep"),
        min_duration_s=0.01,
        target_mass_g=50.0,
        mass_tolerance_g=0.5,
        next_on_success="done",
    )
    s2 = FlowStep("done", SkillRef("fr", "rest"), 0.01, next_on_success="")
    flow = RecipeFlow("f", "t", "weigh", (s1, s2))
    st = KitchenState("weigh", 0.0, 25.0, None, 0.0)
    eng = FlowEngine(flow, st)
    o1 = eng.tick(KitchenObservation(0.0, reported_mass_g=40.0), 0.02)
    assert o1 is None
    o2 = eng.tick(KitchenObservation(0.1, reported_mass_g=50.2), 0.02)
    assert o2 is not None
    assert o2.next_step_id == "done"


def test_metrology_failure_branch_eligible_only_when_reports_complete():
    step = FlowStep(
        "d",
        SkillRef("fr", "dose"),
        target_mass_g=10.0,
        mass_tolerance_g=0.1,
        next_on_success="ok",
        next_on_branch={METROLOGY_FAIL_BRANCH_KEY: "rework"},
    )
    assert not metrology_reports_complete(step, KitchenObservation(0.0))
    assert not metrology_failure_branch_eligible(
        step, KitchenObservation(0.0, reported_mass_g=9.95)
    )  # within tolerance → no fail branch
    assert metrology_failure_branch_eligible(
        step, KitchenObservation(0.0, reported_mass_g=12.0)
    )


def test_flow_metrology_fail_branch():
    s_dose = FlowStep(
        "dose",
        SkillRef("fr", "sauce"),
        min_duration_s=0.0,
        target_mass_g=100.0,
        mass_tolerance_g=1.0,
        next_on_success="ok",
        next_on_branch={METROLOGY_FAIL_BRANCH_KEY: "rework"},
    )
    s_ok = FlowStep("ok", SkillRef("fr", "rest"), 0.01, next_on_success="")
    s_rw = FlowStep("rework", SkillRef("fr", "adjust"), 0.01, next_on_success="")
    flow = RecipeFlow("f", "t", "dose", (s_dose, s_ok, s_rw))
    st = KitchenState("dose", 0.0, 25.0, None, 0.0)
    eng = FlowEngine(flow, st)
    assert eng.tick(KitchenObservation(0.0), 0.02) is None
    out = eng.tick(KitchenObservation(0.1, reported_mass_g=105.0), 0.02)
    assert out is not None
    assert out.next_step_id == "rework"
    assert out.reason == f"branch:{METROLOGY_FAIL_BRANCH_KEY}"


def test_flow_branch_respects_motion_gate():
    s1 = FlowStep(
        "b",
        SkillRef("jp", "simmer"),
        min_duration_s=0.01,
        require_motion_ok=True,
        next_on_success="x",
        next_on_branch={"go": "y"},
    )
    sy = FlowStep("y", SkillRef("jp", "dashi"), 0.01, next_on_success="")
    sx = FlowStep("x", SkillRef("jp", "rest"), 0.01, next_on_success="")
    flow = RecipeFlow("f", "t", "b", (s1, sy, sx))
    st = KitchenState("b", 0.0, 80.0, None, 0.0)
    eng = FlowEngine(flow, st)
    assert eng.tick(KitchenObservation(0.0, tags=("go",)), 0.02) is None
    out = eng.tick(KitchenObservation(0.0, tags=("go",), motion_ok=True), 0.02)
    assert out is not None
    assert out.next_step_id == "y"

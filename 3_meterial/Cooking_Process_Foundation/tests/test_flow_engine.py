from cooking_process_foundation import (
    FlowEngine,
    FlowStep,
    KitchenObservation,
    KitchenState,
    RecipeFlow,
    SkillRef,
)


def test_two_step_linear_flow():
    # Step 1: time gate only (temperature gate would need long sim or sensor injection).
    s1 = FlowStep(
        step_id="heat_pan",
        skill=SkillRef("fr", "saute"),
        min_duration_s=0.2,
        next_on_success="sear",
    )
    s2 = FlowStep(
        step_id="sear",
        skill=SkillRef("fr", "saute", "high_heat"),
        min_duration_s=0.1,
        next_on_success="",
    )
    flow = RecipeFlow("f1", "demo", "heat_pan", (s1, s2))
    st = KitchenState(
        current_step_id="heat_pan",
        time_in_step_s=0.0,
        vessel_surface_temp_c=40.0,
        core_temp_c=None,
        brownness_0_1=0.0,
    )
    eng = FlowEngine(flow, st)
    t = 0.0
    outcomes = []
    for _ in range(200):
        obs = KitchenObservation(wall_clock_s=t)
        o = eng.tick(obs, dt_s=0.05)
        t += 0.05
        if o:
            outcomes.append(o)
        if eng.is_finished():
            break
    assert len(outcomes) >= 2
    assert outcomes[-1].reason == "flow_complete"
    assert outcomes[-2].next_step_id == "sear"


def test_branch_by_observation_tag():
    s1 = FlowStep(
        step_id="choose",
        skill=SkillRef("jp", "simmer"),
        min_duration_s=0.01,
        next_on_success="default_path",
        next_on_branch={"path_a": "a", "path_b": "b"},
    )
    sa = FlowStep("a", SkillRef("jp", "dashi"), 0.01, next_on_success="")
    sb = FlowStep("b", SkillRef("jp", "teriyaki_reduce"), 0.01, next_on_success="")
    flow = RecipeFlow("branch", "b", "choose", (s1, sa, sb))
    st = KitchenState("choose", 0.0, 80.0, None, 0.0)
    eng = FlowEngine(flow, st)
    o = eng.tick(KitchenObservation(0.0, tags=("path_b",)), 0.02)
    assert o is not None
    assert o.next_step_id == "b"

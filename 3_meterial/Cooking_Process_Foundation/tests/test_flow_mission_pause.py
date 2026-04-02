from cooking_process_foundation import FlowEngine, FlowStep, KitchenObservation, KitchenState, RecipeFlow, SkillRef


def test_mission_pause_freezes_state():
    s1 = FlowStep("a", SkillRef("fr", "x"), min_duration_s=1.0, next_on_success="")
    flow = RecipeFlow("f", "f", "a", (s1,))
    st = KitchenState("a", 0.0, 50.0, None, 0.0)
    eng = FlowEngine(flow, st)
    obs = KitchenObservation(0.0)
    eng.tick(obs, 0.2, mission_pause=True)
    assert eng.state.time_in_step_s == 0.0
    assert eng.state.vessel_surface_temp_c == 50.0


def test_heat_cap_reduces_temp_rise():
    s1 = FlowStep("a", SkillRef("fr", "x"), min_duration_s=10.0, next_on_success="")
    flow = RecipeFlow("f", "f", "a", (s1,))
    st = KitchenState("a", 0.0, 25.0, None, 0.0)
    eng = FlowEngine(flow, st)
    obs = KitchenObservation(0.0)
    eng.tick(obs, 0.5, heat_cap_0_1=0.0)
    t0 = eng.state.vessel_surface_temp_c
    eng2 = FlowEngine(flow, KitchenState("a", 0.0, 25.0, None, 0.0))
    eng2.tick(obs, 0.5, heat_cap_0_1=1.0)
    t1 = eng2.state.vessel_surface_temp_c
    assert t0 < t1

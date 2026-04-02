from cooking_process_foundation.contracts import SkillRef
from cooking_process_foundation.recipe_serde import (
    kitchen_observation_from_dict,
    recipe_flow_from_dict,
    recipe_flow_to_dict,
)


def test_recipe_flow_roundtrip():
    d = {
        "flow_id": "demo",
        "title": "Demo",
        "entry_step_id": "a",
        "steps": [
            {
                "step_id": "a",
                "skill": {"tradition": "fr", "technique": "saute", "variant": ""},
                "min_duration_s": 0.1,
                "next_on_success": "b",
                "next_on_branch": {"x": "b"},
            },
            {
                "step_id": "b",
                "skill": {"tradition": "fr", "technique": "rest", "variant": ""},
                "min_duration_s": 0.0,
                "next_on_success": "",
            },
        ],
    }
    f = recipe_flow_from_dict(d)
    d2 = recipe_flow_to_dict(f)
    f2 = recipe_flow_from_dict(d2)
    assert f2.flow_id == f.flow_id
    assert len(f2.steps) == 2
    assert f2.steps[0].skill == SkillRef("fr", "saute", "")


def test_kitchen_observation_defaults_wall_clock():
    o = kitchen_observation_from_dict({})
    assert o.wall_clock_s == 0.0

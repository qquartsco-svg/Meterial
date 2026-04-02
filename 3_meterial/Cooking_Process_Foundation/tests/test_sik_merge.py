from cooking_process_foundation.contracts import KitchenObservation
from cooking_process_foundation.sik_ingress import merge_kitchen_observation_with_sik


def test_merge_adds_tags_from_dict_shaped_sik():
    base = KitchenObservation(1.0, tags=("cooking_tag:foo",))
    sk = {
        "felt_sense": {"gut_risk": 0.5, "felt_tag": "premonition_ambiguous", "coherence": 0.5, "confidence": 0.5, "summary": ""},
        "reflex": {"triggered": False, "action": "monitor", "threat_bias": 0.1, "attention_focus": []},
    }
    m = merge_kitchen_observation_with_sik(base, wall_clock_s=2.0, sik_result=sk)
    assert m.wall_clock_s == 2.0
    assert any("sik.felt:" in t for t in m.tags)
    assert any("sik.gut_risk:" in t for t in m.tags)

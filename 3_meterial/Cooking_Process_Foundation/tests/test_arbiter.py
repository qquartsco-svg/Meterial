from cooking_process_foundation.arbiter import (
    ArbiterConfig,
    ArbiterVerdict,
    arbiter_from_sik_tick_result,
    arbiter_verdict_from_dict,
)


def test_arbiter_explicit_dict():
    v = arbiter_verdict_from_dict({"pause_mission": True, "heat_cap_0_1": 0.0, "reasons": ["manual"]})
    assert v.pause_mission is True
    assert v.heat_cap_0_1 == 0.0


def test_arbiter_from_sik_reflex_triggered():
    fake = {
        "reflex": {"triggered": True, "threat_bias": 0.5, "action": "x", "attention_focus": []},
        "felt_sense": {"gut_risk": 0.1, "coherence": 0.5, "confidence": 0.5, "felt_tag": "t", "summary": ""},
    }
    v = arbiter_from_sik_tick_result(fake)
    assert v.pause_mission is True
    assert v.heat_cap_0_1 == 0.0
    assert "reflex_triggered" in v.reasons


def test_arbiter_from_sik_high_gut():
    fake = {
        "reflex": {"triggered": False, "threat_bias": 0.0, "action": "idle", "attention_focus": []},
        "felt_sense": {"gut_risk": 0.9, "coherence": 0.2, "confidence": 0.3, "felt_tag": "premonition_warning", "summary": ""},
    }
    v = arbiter_from_sik_tick_result(fake, cfg=ArbiterConfig())
    assert v.pause_mission is True
    assert v.heat_cap_0_1 == 0.0


def test_arbiter_allow_all():
    assert ArbiterVerdict.allow_all().heat_cap_0_1 == 1.0

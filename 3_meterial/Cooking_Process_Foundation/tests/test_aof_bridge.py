import pytest

from cooking_process_foundation.aof_bridge import (
    kitchen_observation_from_aof,
    observation_frame_from_aof_min,
)


def test_observation_frame_from_aof_min_and_bridge():
    frame = observation_frame_from_aof_min(
        {
            "case_id": "k1",
            "duration_s": 2.5,
            "signal_intensity": 0.4,
            "raw_channels": [
                {"channel": "vision", "notes": "cooking_tag:path_a extra text"},
            ],
        }
    )
    assert frame.case_id == "k1"
    ko = kitchen_observation_from_aof(frame)
    assert ko.wall_clock_s == 2.5
    assert ko.vision_brownness_0_1 == pytest.approx(0.4)
    assert "path_a" in ko.tags

    ko2 = kitchen_observation_from_aof(
        frame,
        overlay={"reported_surface_temp_c": 180.0, "tags": ["manual"]},
    )
    assert ko2.reported_surface_temp_c == 180.0
    assert "manual" in ko2.tags
    assert "path_a" in ko2.tags

    ko3 = kitchen_observation_from_aof(
        frame,
        overlay={
            "reported_mass_g": 12.3,
            "reported_volume_ml": 5.0,
            "motion_ok": True,
        },
    )
    assert ko3.reported_mass_g == pytest.approx(12.3)
    assert ko3.reported_volume_ml == pytest.approx(5.0)
    assert ko3.motion_ok is True

import pytest

from traffic_quality.six_sigma import dpmo, sigma_level, summarize_process


def test_dpmo_calculation():
    assert dpmo(defects=10, units=100, opportunities_per_unit=2) == 50_000


def test_dpmo_rejects_invalid_units():
    with pytest.raises(ValueError):
        dpmo(defects=1, units=0)


def test_sigma_level_reasonable_for_low_defect_rate():
    assert sigma_level(10_000) > 3.0


def test_summarize_process_contains_key_metrics():
    result = summarize_process(defects=25, units=1_000)
    assert result["dpmo"] == 25_000
    assert "sigma_level" in result

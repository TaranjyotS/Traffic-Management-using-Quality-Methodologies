import pandas as pd

from traffic_quality.control_charts import add_p_chart_limits, p_chart_summary


def test_add_p_chart_limits():
    df = pd.DataFrame({"defects": [10, 12, 8], "sample": [100, 120, 90]})
    result = add_p_chart_limits(df, "defects", "sample")
    assert {"fraction_non_conforming", "ucl", "cl", "lcl", "is_out_of_control"}.issubset(result.columns)
    assert result["lcl"].min() >= 0


def test_p_chart_summary():
    df = pd.DataFrame({"vehicles_arriving": [100, 200], "vehicles_waiting_over_15_min": [10, 20]})
    result = p_chart_summary(df)
    assert result["total_vehicles"] == 300
    assert result["delay_percent"] == 10.0

import pandas as pd

from traffic_quality.pareto import pareto_table, vital_few


def test_pareto_table_sorts_and_calculates_cumulative_percent():
    df = pd.DataFrame({"ctq": ["B", "A"], "frequency": [20, 80]})
    result = pareto_table(df, "ctq", "frequency")
    assert result.loc[0, "ctq"] == "A"
    assert result.loc[1, "cumulative_percent"] == 100


def test_vital_few_includes_threshold_crossing_item():
    df = pd.DataFrame({"ctq": ["A", "B", "C"], "cumulative_percent": [65, 85, 100]})
    assert len(vital_few(df, 80)) == 2

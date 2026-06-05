from __future__ import annotations

import pandas as pd


def pareto_table(df: pd.DataFrame, category_col: str, frequency_col: str) -> pd.DataFrame:
    """Return sorted Pareto table with cumulative counts and cumulative percentage."""
    result = df[[category_col, frequency_col]].copy()
    result = result.sort_values(frequency_col, ascending=False).reset_index(drop=True)
    result["cumulative"] = result[frequency_col].cumsum()
    result["cumulative_percent"] = result["cumulative"] / result[frequency_col].sum() * 100
    return result


def vital_few(df: pd.DataFrame, threshold: float = 80.0) -> pd.DataFrame:
    """Return CTQs contributing up to the threshold, including the crossing item."""
    if "cumulative_percent" not in df.columns:
        raise ValueError("DataFrame must contain cumulative_percent")
    crossing_idx = df.index[df["cumulative_percent"] >= threshold]
    if len(crossing_idx) == 0:
        return df
    return df.loc[: crossing_idx[0]]

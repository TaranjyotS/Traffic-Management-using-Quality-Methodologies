from __future__ import annotations

import pandas as pd


def add_p_chart_limits(df: pd.DataFrame, defect_col: str, sample_col: str) -> pd.DataFrame:
    """Calculate p-chart fraction non-conforming and 3-sigma control limits."""
    result = df.copy()
    total_defects = result[defect_col].sum()
    total_samples = result[sample_col].sum()
    if total_samples <= 0:
        raise ValueError("sample total must be greater than zero")
    p_bar = total_defects / total_samples
    result["fraction_non_conforming"] = result[defect_col] / result[sample_col]
    std_error = ((p_bar * (1 - p_bar)) / result[sample_col]) ** 0.5
    result["cl"] = p_bar
    result["ucl"] = (p_bar + 3 * std_error).clip(upper=1)
    result["lcl"] = (p_bar - 3 * std_error).clip(lower=0)
    result["is_out_of_control"] = (result["fraction_non_conforming"] > result["ucl"]) | (
        result["fraction_non_conforming"] < result["lcl"]
    )
    return result


def p_chart_summary(df: pd.DataFrame) -> dict[str, float]:
    """Summarize p-chart results from a normalized traffic dataframe."""
    total_vehicles = float(df["vehicles_arriving"].sum())
    total_waiting = float(df["vehicles_waiting_over_15_min"].sum())
    fraction = total_waiting / total_vehicles
    return {
        "total_vehicles": total_vehicles,
        "vehicles_waiting_over_15_min": total_waiting,
        "fraction_non_conforming": round(fraction, 4),
        "delay_percent": round(fraction * 100, 2),
    }

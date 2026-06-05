from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "processed"


@dataclass(frozen=True)
class TrafficDataset:
    """Container for baseline/improved traffic quality datasets."""

    baseline_highways: pd.DataFrame
    baseline_non_highways: pd.DataFrame
    improved_highways: pd.DataFrame
    improved_non_highways: pd.DataFrame
    pareto: pd.DataFrame


def _normalise_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [
        str(col).strip().lower().replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "")
        for col in df.columns
    ]
    return df


def load_pchart_csv(path: Path) -> pd.DataFrame:
    """Load a p-chart CSV exported from the original Excel workbook."""
    df = pd.read_csv(path)
    df = _normalise_columns(df)
    df = df.rename(
        columns={
            df.columns[0]: "hour",
            df.columns[1]: "vehicles_arriving",
            df.columns[2]: "vehicles_waiting_over_15_min",
            df.columns[3]: "fraction_non_conforming",
            df.columns[4]: "ucl",
            df.columns[5]: "cl",
            df.columns[6]: "lcl",
        }
    )
    numeric_cols = ["hour", "vehicles_arriving", "vehicles_waiting_over_15_min", "fraction_non_conforming", "ucl", "cl", "lcl"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna(subset=["hour", "vehicles_arriving", "vehicles_waiting_over_15_min"])


def load_pareto(path: Path = DATA_DIR / "pareto_ctq.csv") -> pd.DataFrame:
    """Load Critical-to-Quality Pareto data."""
    df = pd.read_csv(path)
    df.columns = ["ctq", "frequency", "cumulative", "cumulative_percent"]
    return df


def load_all(data_dir: Path = DATA_DIR) -> TrafficDataset:
    """Load all datasets needed by the dashboard and reports."""
    return TrafficDataset(
        baseline_highways=load_pchart_csv(data_dir / "pchart_highways_baseline.csv"),
        baseline_non_highways=load_pchart_csv(data_dir / "pchart_non_highways_baseline.csv"),
        improved_highways=load_pchart_csv(data_dir / "pchart_highways_improved.csv"),
        improved_non_highways=load_pchart_csv(data_dir / "pchart_non_highways_improved.csv"),
        pareto=load_pareto(data_dir / "pareto_ctq.csv"),
    )

from __future__ import annotations

from pathlib import Path

from traffic_quality.control_charts import p_chart_summary
from traffic_quality.data_loader import load_all
from traffic_quality.six_sigma import summarize_process


def build_markdown_report(output_path: Path = Path("docs/generated_quality_summary.md")) -> Path:
    """Generate a lightweight Markdown report from the processed data."""
    ds = load_all()
    rows = []
    scenarios = {
        "Baseline Highways": ds.baseline_highways,
        "Improved Highways": ds.improved_highways,
        "Baseline Non-Highways": ds.baseline_non_highways,
        "Improved Non-Highways": ds.improved_non_highways,
    }
    for name, df in scenarios.items():
        p_summary = p_chart_summary(df)
        s_summary = summarize_process(
            p_summary["vehicles_waiting_over_15_min"], p_summary["total_vehicles"]
        )
        rows.append((name, p_summary, s_summary))

    lines = ["# Generated Traffic Quality Summary", "", "| Scenario | Vehicles | Delayed >15 min | Delay % | DPMO | Sigma |", "|---|---:|---:|---:|---:|---:|"]
    for name, p_summary, s_summary in rows:
        lines.append(
            f"| {name} | {p_summary['total_vehicles']:.0f} | {p_summary['vehicles_waiting_over_15_min']:.0f} | "
            f"{p_summary['delay_percent']:.2f}% | {s_summary['dpmo']:.2f} | {s_summary['sigma_level']:.2f} |"
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path


if __name__ == "__main__":
    print(build_markdown_report())

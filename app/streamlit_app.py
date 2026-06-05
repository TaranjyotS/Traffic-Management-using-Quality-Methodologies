from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from traffic_quality.control_charts import p_chart_summary  # noqa: E402
from traffic_quality.data_loader import load_all  # noqa: E402
from traffic_quality.six_sigma import summarize_process  # noqa: E402

st.set_page_config(page_title="Traffic Quality Analytics", page_icon="🚦", layout="wide")
st.title("🚦 Traffic Quality Analytics Platform")
st.caption("Six Sigma, DMAIC, Pareto, and p-chart analytics for traffic-delay reduction.")

ds = load_all(ROOT / "data" / "processed")

scenario_map = {
    "Baseline Highways": ds.baseline_highways,
    "Improved Highways": ds.improved_highways,
    "Baseline Non-Highways": ds.baseline_non_highways,
    "Improved Non-Highways": ds.improved_non_highways,
}

summary_rows = []
for name, df in scenario_map.items():
    p_summary = p_chart_summary(df)
    sigma = summarize_process(p_summary["vehicles_waiting_over_15_min"], p_summary["total_vehicles"])
    summary_rows.append({"scenario": name, **p_summary, **sigma})
summary_df = pd.DataFrame(summary_rows)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Baseline Highway Delay", f"{summary_df.loc[0, 'delay_percent']:.2f}%")
col2.metric("Improved Highway Delay", f"{summary_df.loc[1, 'delay_percent']:.2f}%")
col3.metric("Baseline Non-Highway Delay", f"{summary_df.loc[2, 'delay_percent']:.2f}%")
col4.metric("Improved Non-Highway Delay", f"{summary_df.loc[3, 'delay_percent']:.2f}%")

st.subheader("Process Quality Summary")
st.dataframe(summary_df, use_container_width=True)

st.subheader("Before vs After Delay Rate")
fig = px.bar(summary_df, x="scenario", y="delay_percent", text="delay_percent", title="Vehicles Waiting More Than 15 Minutes")
st.plotly_chart(fig, use_container_width=True)

st.subheader("P-Chart Explorer")
selected = st.selectbox("Select scenario", list(scenario_map.keys()))
chart_df = scenario_map[selected]
line_fig = px.line(
    chart_df,
    x="hour",
    y=["fraction_non_conforming", "ucl", "cl", "lcl"],
    markers=True,
    title=f"{selected}: Fraction Non-Conforming with Control Limits",
)
st.plotly_chart(line_fig, use_container_width=True)

st.subheader("Critical-to-Quality Pareto Analysis")
pareto_fig = px.bar(ds.pareto, x="ctq", y="frequency", title="CTQ Frequency Contribution")
st.plotly_chart(pareto_fig, use_container_width=True)
st.dataframe(ds.pareto, use_container_width=True)

st.info(
    "Portfolio framing: this app preserves the original Masters project methodology while making the analysis reproducible, testable, and presentable as a Python data analytics system."
)

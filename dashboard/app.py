from __future__ import annotations

import pandas as pd
import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data import INDICATORS, load_data_from_csv
from src.explain import explain_year_indicator, summarize_top_contributors
from src.forecast import event_aware_forecast
from src.matrix import build_association_matrix, plot_association_matrix
from src.scenarios import SCENARIOS, apply_scenario_to_links


st.set_page_config(page_title="Ethiopia Financial Inclusion Dashboard", layout="wide")

st.title("📊 Ethiopia Financial Inclusion Forecasting Dashboard")
st.caption("Event impact modeling and forecasting for financial inclusion in Ethiopia")

# Load data from CSV files
observations, events, impact_links = load_data_from_csv()

# Validate required data exists
if observations.empty:
    st.error("❌ No observations found. Please ensure data files are correctly placed in 'data/raw/'")
    st.stop()

if events.empty:
    st.warning("⚠️ No events found in the dataset")

indicator_codes = sorted(INDICATORS.keys())

col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("🎯 Scenario & Event Controls")

    scenario = st.selectbox("Scenario preset", SCENARIOS, index=1)

    enabled = set()
    for _, e in events.iterrows():
        checked = st.checkbox(
            f"{e['record_id']} — {e['indicator']} ({e['observation_date']})",
            value=True
        )
        if checked:
            enabled.add(str(e["record_id"]))

with col_right:
    st.subheader("📋 Impact Links")
    st.dataframe(impact_links, use_container_width=True, hide_index=True)

st.divider()

# Apply scenario scaling
scaled_links = apply_scenario_to_links(impact_links, scenario)

enabled_for_run = enabled if scenario != "baseline" else set()

# Build association matrix
matrix = build_association_matrix(
    events=events,
    impact_links=scaled_links,
    indicators=indicator_codes
)

st.subheader("📊 Association Matrix (Events x Indicators)")
event_labels = dict(zip(events["record_id"], events["indicator"]))
fig = plot_association_matrix(matrix, event_labels=event_labels)
st.pyplot(fig, use_container_width=True)

with st.expander("View raw matrix values"):
    st.dataframe(matrix, use_container_width=True)

st.divider()

st.subheader("📈 Forecasts (2021–2027)")

forecast_years = list(range(2021, 2028))
fc = event_aware_forecast(
    observations=observations,
    events=events,
    impact_links=scaled_links,
    forecast_years=forecast_years,
    enabled_event_ids=enabled_for_run,
)

show_inds = ["ACC_OWN", "DIG_PAY"]
fc_show = fc[fc["indicator_code"].isin(show_inds)].copy()

for ind in show_inds:
    st.markdown(f"#### {ind} — {INDICATORS[ind].name} ({INDICATORS[ind].unit})")
    tmp = fc_show[fc_show["indicator_code"] == ind][["year", "baseline", "forecast"]].set_index("year")
    st.line_chart(tmp, height=220)

st.divider()

st.subheader("🔍 Explainability (Event Contributions)")
ex_col1, ex_col2 = st.columns([1, 2])

with ex_col1:
    explain_year = st.selectbox("Year", forecast_years, index=0)
    explain_indicator = st.selectbox("Indicator", indicator_codes, index=0)

with ex_col2:
    exp = explain_year_indicator(
        year=int(explain_year),
        indicator_code=str(explain_indicator),
        events=events,
        impact_links=scaled_links,
        enabled_event_ids=enabled_for_run,
    )

    st.dataframe(exp, use_container_width=True, hide_index=True)
    st.info(summarize_top_contributors(exp, top_n=2))

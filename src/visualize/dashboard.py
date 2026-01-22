import sys
from pathlib import Path

# --- Fix Python path for Streamlit ---
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = PROJECT_ROOT / "src"
sys.path.append(str(SRC_ROOT))

import streamlit as st
import altair as alt
import sqlite3
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from analysis.bursts import detect_bursts

DB_PATH = PROJECT_ROOT / "data" / "events.db"

# Auto-refresh Streamlit every 2 seconds
st_autorefresh(interval=2000, key="live-refresh")

st.title("Filesystem Behaviour Analyzer")

# -------------------- LOAD DATA --------------------

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql(
    "SELECT timestamp, action, path FROM normalized_events",
    conn
)

bursts = detect_bursts()
bursts_df = pd.DataFrame(bursts)

conn.close()

# -------------------- TIMEZONE HANDLING --------------------

local_tz = datetime.now().astimezone().tzinfo
st.caption(f"All times shown in {local_tz}")

# Normalize event timestamps
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
df["timestamp"] = df["timestamp"].dt.tz_convert(local_tz)

# Normalize burst timestamps (ONLY if they exist)
if not bursts_df.empty and "timestamp" in bursts_df.columns:
    bursts_df["timestamp"] = pd.to_datetime(bursts_df["timestamp"], utc=True)
    bursts_df["timestamp"] = bursts_df["timestamp"].dt.tz_convert(local_tz)
    bursts_df["minute"] = bursts_df["timestamp"].dt.floor("1min")
else:
    bursts_df = pd.DataFrame(
        columns=[
            "folder",
            "type",
            "count",
            "window_seconds",
            "baseline_rate",
            "window_rate",
            "severity",
            "severity_ratio",
            "timestamp",
            "minute",
            "reason"
        ]
    )

# -------------------- TIME RANGE FILTER --------------------

st.subheader("Time Range")

range_option = st.selectbox(
    "Show data from",
    ["Last 15 minutes", "Last 1 hour", "Last 24 hours", "All time"],
    index=1
)

now = df["timestamp"].max()

if range_option == "Last 15 minutes":
    cutoff = now - pd.Timedelta(minutes=15)
elif range_option == "Last 1 hour":
    cutoff = now - pd.Timedelta(hours=1)
elif range_option == "Last 24 hours":
    cutoff = now - pd.Timedelta(days=1)
else:
    cutoff = None

if cutoff is not None:
    df = df[df["timestamp"] >= cutoff]
    bursts_df = bursts_df[bursts_df["timestamp"] >= cutoff]

if df.empty:
    st.warning("No data yet.")
    st.stop()

# -------------------- TIMELINE --------------------

st.subheader("Activity Timeline")

timeline_df = (
    df.groupby(df["timestamp"].dt.floor("1min"))
      .size()
      .reset_index(name="event_count")
)

st.line_chart(timeline_df.set_index("timestamp"))

# -------------------- ACTION DISTRIBUTION --------------------

st.subheader("Action Distribution")
st.bar_chart(df["action"].value_counts())

# -------------------- FOLDER HEATMAP --------------------

st.subheader("Folder Activity")

df["folder"] = (
    df["path"]
    .apply(lambda p: p.split("->")[-1].strip())
    .apply(lambda p: str(Path(p).parent))
)

pivot = pd.pivot_table(
    df,
    index="folder",
    columns="action",
    aggfunc="size",
    fill_value=0
)

st.dataframe(pivot)

# -------------------- BURST TIMELINE --------------------

st.subheader("Activity Timeline with Bursts")

line = alt.Chart(timeline_df).mark_line().encode(
    x="timestamp:T",
    y="event_count:Q"
)

if not bursts_df.empty:
    burst_points_df = bursts_df.merge(
        timeline_df,
        left_on="minute",
        right_on="timestamp",
        how="left"
    )

    burst_points_df["event_count"] = burst_points_df["event_count"].fillna(0)

    severity_scale = alt.Scale(
        domain=["low", "medium", "high"],
        range=["#f4d03f", "#f39c12", "#e74c3c"]
    )

    burst_points = alt.Chart(burst_points_df).mark_point(size=100).encode(
        x="minute:T",
        y="event_count:Q",
        color=alt.Color(
            "severity:N",
            scale=severity_scale,
            legend=alt.Legend(title="Burst Severity")
        ),
        tooltip=["type", "folder", "severity", "severity_ratio", "reason"]
    )

    chart = (line + burst_points).interactive()
else:
    chart = line.interactive()

st.altair_chart(chart, width="stretch")

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Eva's Fitness Dashboard", layout="wide")
st.title("🏋️‍♀️ Eva's Fitness Log — Minutes & Calories")
st.caption("Sample dataset. Use the sidebar to filter. (You can replace with your own CSV later.)")

# -----------------------
# Sample Fitness Data
# -----------------------
def sample_fitness():
    rng = pd.date_range("2025-01-01", periods=120, freq="D")
    activities = ["Running","Weightlifting","Yoga","Cycling","Walking"]
    df = pd.DataFrame({
        "date": rng,
        "activity": np.random.choice(activities, size=len(rng)),
        "minutes": np.random.randint(10, 80, size=len(rng))
    })
    # calories ≈ minutes * MET factor (randomized for demo)
    df["calories"] = (df["minutes"] * np.random.uniform(6, 10, size=len(rng))).astype(int)
    return df

df = sample_fitness()

# -----------------------
# Sidebar filters
# -----------------------
st.sidebar.header("⚙️ Filters")
# Date range
min_d, max_d = df["date"].min(), df["date"].max()
start, end = st.sidebar.date_input("Date range", (min_d.date(), max_d.date()))
start, end = pd.to_datetime(start), pd.to_datetime(end)
df = df[(df["date"] >= start) & (df["date"] <= end)]

# Activity multiselect
activities = sorted(df["activity"].unique().tolist())
chosen = st.sidebar.multiselect("Activities", activities, default=activities[:min(3, len(activities))])
if chosen:
    df = df[df["activity"].isin(chosen)]

# -----------------------
# KPIs
# -----------------------
st.subheader("📌 Summary")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Days", f"{df['date'].nunique()}")
k2.metric("Total Minutes", f"{int(df['minutes'].sum()):,}")
k3.metric("Total Calories", f"{int(df['calories'].sum()):,}")
k4.metric("Avg Minutes/Day", f"{df.groupby('date')['minutes'].sum().mean():.1f}")

# -----------------------
# Charts
# -----------------------
st.subheader("📈 Charts")

# 1) Minutes over time (stacked by activity)
by_day_act = df.groupby(["date","activity"], as_index=False)[["minutes","calories"]].sum()
fig1 = px.area(by_day_act, x="date", y="minutes", color="activity", title="Minutes per day (stacked by activity)")
st.plotly_chart(fig1, use_container_width=True)

# 2) Calories by activity (bar)
by_act = df.groupby("activity", as_index=False)[["minutes","calories"]].sum().sort_values("calories", ascending=False)
fig2 = px.bar(by_act, x="activity", y="calories", title="Total calories by activity")
st.plotly_chart(fig2, use_container_width=True)

# 3) Minutes distribution (hist)
fig3 = px.histogram(df, x="minutes", nbins=20, title="Distribution of session minutes")
st.plotly_chart(fig3, use_container_width=True)

# -----------------------
# Data preview
# -----------------------
st.subheader("🗂️ Data Preview")
st.dataframe(df.sort_values("date", ascending=False).head(200))
st.caption("Tip: Replace the sample generator with your own CSV later and keep the same column names: date, activity, minutes, calories.")

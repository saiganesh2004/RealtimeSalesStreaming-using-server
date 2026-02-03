import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime
import os

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Realtime Sales Dashboard",
    layout="wide",
    page_icon="📊"
)

st.title("📊 Realtime Sales Monitoring Dashboard")
st.caption("FastAPI • Docker • Streamlit • Plotly")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# --------------------------------------------------
# FETCH DATA
# --------------------------------------------------
@st.cache_data(ttl=2)
def fetch_sales():
    response = requests.get(
        f"{BACKEND_URL}/live-sales",
        params={"count": 500},
        timeout=5
    )
    response.raise_for_status()
    return pd.DataFrame(response.json())

df = fetch_sales()
st.subheader(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")

# --------------------------------------------------
# DATA PROCESSING
# --------------------------------------------------
if df.empty:
    st.warning("Waiting for real-time sales data...")
    st.stop()

df["Amount"] = df["amount"].astype(int)
df["Time"] = pd.to_datetime(df["time"])

# --------------------------------------------------
# METRICS
# --------------------------------------------------
c1, c2, c3 = st.columns(3)
c1.metric("💰 Total Sales", f"₹ {df['Amount'].sum():,}")
c2.metric("🧾 Orders", len(df))
c3.metric("📊 Avg Sale", f"₹ {int(df['Amount'].mean()):,}")

st.divider()

# --------------------------------------------------
# CHART
# --------------------------------------------------
fig = px.line(
    df.sort_values("Time"),
    x="Time",
    y="Amount",
    title="📈 Sales Over Time",
    markers=True
)
st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# TABLE
# --------------------------------------------------
st.subheader("📋 Latest Sales Records")
st.dataframe(df.tail(10), use_container_width=True)

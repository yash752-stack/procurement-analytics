"""
dashboard/app.py
Procurement Analytics Dashboard — Streamlit + Plotly
Mirrors Power BI dashboard structure for the Barclays BI & Data Analyst role.

Run: streamlit run dashboard/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Procurement Analytics | Yash Chaudhary",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        border-left: 4px solid #2C5282;
    }
    .metric-title { font-size: 13px; color: #718096; font-weight: 500; margin-bottom: 4px; }
    .metric-value { font-size: 26px; font-weight: 700; color: #1A2B4A; }
    .metric-delta { font-size: 12px; color: #48BB78; }
    h1, h2, h3 { color: #1A2B4A; }
    .stSelectbox label, .stMultiselect label { color: #2D3748; font-weight: 500; }
    section[data-testid="stSidebar"] { background-color: #1A2B4A; }
    section[data-testid="stSidebar"] * { color: white !important; }
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    path = "data/enriched_procurement_data.csv"
    if not os.path.exists(path):
        st.error("⚠️ Run `python data/generate_data.py` and `python pipeline/etl_pipeline.py` first.")
        st.stop()
    df = pd.read_csv(path, parse_dates=["Order_Date", "Actual_Delivery", "Delivery_Due_Date"])
    return df

df = load_data()

# ── SIDEBAR FILTERS ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📦 Procurement Analytics")
    st.markdown("---")
    st.markdown("### Filters")

    years = sorted(df["Order_Year"].unique())
    sel_years = st.multiselect("Year", years, default=years)

    categories = sorted(df["Category"].unique())
    sel_cats = st.multiselect("Category", categories, default=categories)

    departments = sorted(df["Department"].unique())
    sel_depts = st.multiselect("Department", departments, default=departments)

    statuses = sorted(df["Status"].unique())
    sel_status = st.multiselect("PO Status", statuses, default=statuses)

    st.markdown("---")
    st.markdown("**Built by:** Yash Chaudhary  \n**Stack:** Python · Pandas · Streamlit · Plotly  \n**Role Target:** Barclays BI & Data Analyst")

# ── FILTER DATA ──────────────────────────────────────────────────────────────
fdf = df[
    df["Order_Year"].isin(sel_years) &
    df["Category"].isin(sel_cats) &
    df["Department"].isin(sel_depts) &
    df["Status"].isin(sel_status)
].copy()

# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("# 📦 Procurement Analytics Dashboard")
st.markdown(f"Showing **{len(fdf):,}** purchase orders · Total Spend: **₹{fdf['Total_Value_INR'].sum()/1e7:.2f} Cr**")
st.markdown("---")

# ── KPI CARDS ────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-title">Total Spend</div>
        <div class="metric-value">₹{fdf['Total_Value_INR'].sum()/1e6:.1f}M</div>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-title">Purchase Orders</div>
        <div class="metric-value">{len(fdf):,}</div>
    </div>""", unsafe_allow_html=True)

with k3:
    delay_pct = fdf["Is_Delayed"].mean() * 100
    color = "#E53E3E" if delay_pct > 20 else "#48BB78"
    st.markdown(f"""<div class="metric-card" style="border-left-color:{color}">
        <div class="metric-title">On-Time Delivery</div>
        <div class="metric-value">{100-delay_pct:.1f}%</div>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-title">Active Suppliers</div>
        <div class="metric-value">{fdf['Supplier_ID'].nunique()}</div>
    </div>""", unsafe_allow_html=True)

with k5:
    avg_lead = fdf["Actual_Lead_Days"].mean()
    st.markdown(f"""<div class="metric-card">
        <div class="metric-title">Avg Lead Time</div>
        <div class="metric-value">{avg_lead:.0f} days</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── ROW 1: Spend Over Time + Spend by Category ───────────────────────────────
c1, c2 = st.columns([3, 2])

with c1:
    monthly = fdf.groupby("Order_Month")["Total_Value_INR"].sum().reset_index()
    monthly.columns = ["Month", "Spend"]
    fig = px.area(monthly, x="Month", y="Spend",
                  title="📈 Monthly Procurement Spend (INR)",
                  color_discrete_sequence=["#2C5282"])
    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        title_font_color="#1A2B4A", xaxis_tickangle=-45,
        yaxis_tickformat=",.0f", height=300,
        margin=dict(t=40, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    cat_spend = fdf.groupby("Category")["Total_Value_INR"].sum().reset_index()
    fig = px.pie(cat_spend, names="Category", values="Total_Value_INR",
                 title="🏷️ Spend by Category",
                 color_discrete_sequence=px.colors.sequential.Blues_r)
    fig.update_layout(
        paper_bgcolor="white", title_font_color="#1A2B4A",
        height=300, margin=dict(t=40, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

# ── ROW 2: Supplier Scorecard + Delay Analysis ───────────────────────────────
c3, c4 = st.columns([2, 3])

with c3:
    sup_perf = fdf.groupby("Supplier_Name").agg(
        Total_Spend=("Total_Value_INR", "sum"),
        Orders=("PO_ID", "count"),
        Delay_Rate=("Is_Delayed", "mean"),
        Avg_Lead=("Actual_Lead_Days", "mean")
    ).reset_index()
    sup_perf["Delay_Rate"] = (sup_perf["Delay_Rate"] * 100).round(1)
    sup_perf["Avg_Lead"]   = sup_perf["Avg_Lead"].round(1)
    sup_perf = sup_perf.sort_values("Total_Spend", ascending=False)

    fig = px.bar(sup_perf, x="Total_Spend", y="Supplier_Name",
                 orientation="h",
                 title="🏭 Supplier Spend Ranking",
                 color="Delay_Rate",
                 color_continuous_scale=["#48BB78", "#ECC94B", "#E53E3E"],
                 labels={"Total_Spend": "Total Spend (INR)", "Delay_Rate": "Delay %"})
    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        title_font_color="#1A2B4A", height=320,
        margin=dict(t=40, b=10), yaxis_title=""
    )
    st.plotly_chart(fig, use_container_width=True)

with c4:
    dept_delay = fdf.groupby(["Department", "Is_Delayed"]).size().reset_index(name="Count")
    dept_delay["Is_Delayed"] = dept_delay["Is_Delayed"].map({True: "Delayed", False: "On Time"})
    fig = px.bar(dept_delay, x="Department", y="Count", color="Is_Delayed",
                 title="⏱️ On-Time vs Delayed Orders by Department",
                 color_discrete_map={"On Time": "#2C5282", "Delayed": "#E53E3E"},
                 barmode="stack")
    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        title_font_color="#1A2B4A", height=320,
        margin=dict(t=40, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

# ── ROW 3: Spend Band Distribution + PO Status ───────────────────────────────
c5, c6 = st.columns(2)

with c5:
    band = fdf["Spend_Band"].value_counts().reset_index()
    band.columns = ["Band", "Count"]
    fig = px.bar(band, x="Band", y="Count",
                 title="💰 PO Spend Band Distribution",
                 color="Band",
                 color_discrete_sequence=["#BEE3F8", "#90CDF4", "#4299E1", "#2C5282"])
    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        title_font_color="#1A2B4A", height=280,
        margin=dict(t=40, b=10), showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

with c6:
    status_counts = fdf["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    fig = px.pie(status_counts, names="Status", values="Count",
                 title="📋 PO Approval Status",
                 color_discrete_map={
                     "Approved": "#2C5282", "Pending": "#ECC94B", "Rejected": "#E53E3E"
                 })
    fig.update_layout(
        paper_bgcolor="white", title_font_color="#1A2B4A",
        height=280, margin=dict(t=40, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

# ── ROW 4: DATA QUALITY REPORT ───────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🔍 Data Quality Report")
qr_path = "data/data_quality_report.csv"
if os.path.exists(qr_path):
    qr = pd.read_csv(qr_path)
    st.dataframe(qr, use_container_width=True, hide_index=True)
else:
    st.info("Run the pipeline first to generate the data quality report.")

# ── ROW 5: RAW DATA TABLE ────────────────────────────────────────────────────
with st.expander("📄 View Enriched Procurement Data"):
    cols = ["PO_ID", "Supplier_Name", "Category", "Department",
            "Order_Date", "Total_Value_INR", "Status",
            "Is_Delayed", "Delay_Days", "Spend_Band", "Supplier_Risk_Flag"]
    st.dataframe(fdf[cols].sort_values("Order_Date", ascending=False),
                 use_container_width=True, hide_index=True)

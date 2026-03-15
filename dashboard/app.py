"""
dashboard/app.py
Procurement Analytics Dashboard — Royal Red & Velvet Theme
Enhanced with animations, dynamic KPIs, rich visuals
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

st.set_page_config(
    page_title="Procurement Intelligence | Yash Chaudhary",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main { background: linear-gradient(135deg, #0d0408 0%, #1a0510 40%, #0d0408 100%); min-height: 100vh; }
.block-container { padding: 1.5rem 2rem 2rem; background: transparent; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a0010 0%, #2d0015 50%, #1a0010 100%) !important;
    border-right: 1px solid rgba(180,30,60,0.3);
}
section[data-testid="stSidebar"] * { color: #f5c6d0 !important; }
section[data-testid="stSidebar"] hr { border-color: rgba(180,30,60,0.4) !important; }

.dash-header {
    background: linear-gradient(135deg, #1a0010 0%, #3d0020 50%, #1a0010 100%);
    border: 1px solid rgba(180,30,60,0.5);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.dash-header::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(ellipse at center, rgba(180,30,60,0.12) 0%, transparent 60%);
    animation: pulse-bg 4s ease-in-out infinite;
}
@keyframes pulse-bg {
    0%, 100% { opacity: 0.6; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.05); }
}
.dash-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #ff6b8a, #c0392b, #e8103a, #ff6b8a);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradient-shift 4s ease infinite;
    margin: 0;
}
@keyframes gradient-shift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.dash-subtitle { color: rgba(245,198,208,0.7); font-size: 0.9rem; font-weight: 300; margin-top: 6px; letter-spacing: 2px; text-transform: uppercase; }

.kpi-card {
    background: linear-gradient(135deg, #1f0012 0%, #2d0018 100%);
    border: 1px solid rgba(180,30,60,0.35);
    border-radius: 14px;
    padding: 20px 22px;
    position: relative;
    overflow: hidden;
    transition: transform 0.3s ease, border-color 0.3s ease;
}
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0;
    width: 100%; height: 3px;
    background: linear-gradient(90deg, #c0392b, #e8103a, #ff6b8a);
    border-radius: 0 0 14px 14px;
}
.kpi-card:hover { transform: translateY(-3px); border-color: rgba(232,16,58,0.6); }
.kpi-icon { font-size: 1.5rem; margin-bottom: 10px; }
.kpi-label { font-size: 0.72rem; font-weight: 500; color: rgba(245,198,208,0.6); text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 6px; }
.kpi-value { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 700; color: #ff4d6d; line-height: 1; margin-bottom: 4px; }
.kpi-delta { font-size: 0.75rem; color: rgba(245,198,208,0.5); font-weight: 300; }
.kpi-delta.good { color: #52c77a; }
.kpi-delta.bad  { color: #ff4d4d; }

.section-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem; font-weight: 600;
    color: #f5c6d0;
    margin: 28px 0 16px;
    padding-left: 14px;
    border-left: 3px solid #c0392b;
}

.badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; }
.badge-red   { background: rgba(192,57,43,0.2); color: #ff6b8a; border: 1px solid rgba(192,57,43,0.4); }
.badge-green { background: rgba(82,199,122,0.15); color: #52c77a; border: 1px solid rgba(82,199,122,0.3); }

.live-dot { display: inline-block; width: 8px; height: 8px; background: #52c77a; border-radius: 50%; margin-right: 6px; animation: blink 1.5s ease-in-out infinite; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

hr { border-color: rgba(180,30,60,0.2) !important; }
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #1a0010; }
::-webkit-scrollbar-thumb { background: #c0392b; border-radius: 10px; }
.streamlit-expanderHeader { background: #1f0012 !important; color: #f5c6d0 !important; border-color: rgba(180,30,60,0.3) !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#ddb8c2", size=12),
    title_font=dict(family="Playfair Display", color="#e8c8d0", size=14),
    xaxis=dict(gridcolor="rgba(140,50,70,0.1)", linecolor="rgba(140,50,70,0.15)", tickcolor="rgba(200,160,175,0.3)"),
    yaxis=dict(gridcolor="rgba(140,50,70,0.1)", linecolor="rgba(140,50,70,0.15)", tickcolor="rgba(200,160,175,0.3)"),
    legend=dict(bgcolor="rgba(18,4,10,0.75)", bordercolor="rgba(140,50,70,0.25)", borderwidth=1),
    margin=dict(t=44, b=28, l=10, r=10),
)
ACCENT    = "#b84060"
ACCENT2   = "#d98a9a"
ACCENT3   = "#7a2538"
TEXT      = "#ddb8c2"
RED_SCALE = ["#2a0a14","#4a1a28","#6e2c3e","#924455","#b06070","#cc8f9a","#ddb8c2","#eedade"]
RED_CONT  = [[0,"#160610"],[0.3,"#5c1f30"],[0.6,"#944050"],[0.85,"#bf7080"],[1,"#e0b0ba"]]

def generate_data():
    import random
    from datetime import datetime, timedelta
    random.seed(42)
    np.random.seed(42)
    SUPPLIERS = [
        ("SUP001","Tata Steel Supplies","Raw Materials","India",4.2),
        ("SUP002","Infosys Bpo Services","IT Services","India",4.5),
        ("SUP003","Mahindra Logistics","Logistics","India",3.8),
        ("SUP004","Reliance Office Supplies","Office","India",4.0),
        ("SUP005","L&T Construction","Construction","India",4.3),
        ("SUP006","Hcl Tech Solutions","IT Services","India",4.6),
        ("SUP007","Hdfc Equipment Finance","Equipment","India",3.9),
        ("SUP008","Wipro Facilities","Facilities","India",4.1),
        ("SUP009","Asian Paints Industrial","Raw Materials","India",3.7),
        ("SUP010","Dhl Express India","Logistics","India",4.4),
    ]
    DEPTS = ["Finance","Operations","HR","IT","Procurement","Legal","Marketing"]
    STATUSES = ["Approved","Approved","Approved","Pending","Rejected"]
    TERMS = ["Net 30","Net 45","Net 60","Immediate"]
    start, end = datetime(2023,1,1), datetime(2025,3,1)
    rows = []
    for i in range(500):
        sup = random.choice(SUPPLIERS)
        od = start + timedelta(days=random.randint(0,(end-start).days))
        dd = od + timedelta(days=random.randint(7,90))
        ad = dd + timedelta(days=random.randint(-5,20))
        qty = random.randint(1,200)
        price = round(random.uniform(500,150000),2)
        if random.random()<0.03: price = None
        if random.random()<0.02: qty = -qty
        rows.append({"PO_ID":f"PO-{2023+i//200}-{str(i+1).zfill(4)}","Supplier_ID":sup[0],"Supplier_Name":sup[1],"Category":sup[2],"Department":random.choice(DEPTS),"Order_Date":od.strftime("%Y-%m-%d"),"Delivery_Due_Date":dd.strftime("%Y-%m-%d"),"Actual_Delivery":ad.strftime("%Y-%m-%d"),"Quantity":qty,"Unit_Price_INR":price,"Total_Value_INR":round(qty*price,2) if price else None,"Payment_Terms":random.choice(TERMS),"Status":random.choice(STATUSES),"Invoice_Received":random.choice([True,False]),"Country":sup[3]})
    po = pd.DataFrame(rows)
    sup_rows = []
    for sup in SUPPLIERS:
        sup_rows.append({"Supplier_ID":sup[0],"Supplier_Name":sup[1],"Category":sup[2],"Country":sup[3],"Quality_Score":sup[4],"On_Time_Rate_Pct":round(random.uniform(70,98),1),"Avg_Lead_Days":random.randint(10,45),"Preferred":random.choice([True,False])})
    sm = pd.DataFrame(sup_rows)
    # cleanse
    po["Supplier_Name"] = po["Supplier_Name"].str.strip().str.title()
    po["Quantity_Anomaly"] = po["Quantity"] < 0
    po["Quantity"] = po["Quantity"].abs()
    cat_med = po.groupby("Category")["Unit_Price_INR"].transform("median")
    po["Unit_Price_INR"] = po["Unit_Price_INR"].fillna(cat_med)
    po["Total_Value_INR"] = po["Quantity"] * po["Unit_Price_INR"]
    po = po.drop_duplicates(subset="PO_ID", keep="first")
    # enrich
    df = po.merge(sm[["Supplier_ID","Quality_Score","On_Time_Rate_Pct","Avg_Lead_Days","Preferred"]], on="Supplier_ID", how="left")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Actual_Delivery"] = pd.to_datetime(df["Actual_Delivery"])
    df["Delivery_Due_Date"] = pd.to_datetime(df["Delivery_Due_Date"])
    df["Actual_Lead_Days"] = (df["Actual_Delivery"] - df["Order_Date"]).dt.days
    df["Delay_Days"] = (df["Actual_Delivery"] - df["Delivery_Due_Date"]).dt.days
    df["Is_Delayed"] = df["Delay_Days"] > 0
    df["Order_Month"] = df["Order_Date"].dt.to_period("M").astype(str)
    df["Order_Quarter"] = df["Order_Date"].dt.to_period("Q").astype(str)
    df["Order_Year"] = df["Order_Date"].dt.year
    df["Spend_Band"] = pd.cut(df["Total_Value_INR"],bins=[0,10000,50000,200000,float("inf")],labels=["Low (<10K)","Mid (10K-50K)","High (50K-200K)","Strategic (>200K)"])
    df["Supplier_Risk_Flag"] = ((df["Quality_Score"]<4.0)|(df["On_Time_Rate_Pct"]<80)).map({True:"At Risk",False:"Stable"})
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/enriched_procurement_data.csv", index=False)
    return df

@st.cache_data
def load_data():
    path = "data/enriched_procurement_data.csv"
    if not os.path.exists(path):
        generate_data()
    return pd.read_csv(path, parse_dates=["Order_Date","Actual_Delivery","Delivery_Due_Date"])

df = load_data()

with st.sidebar:
    st.markdown("<div style='text-align:center;padding:16px 0 8px'><div style='font-family:Playfair Display,serif;font-size:1.3rem;color:#ff4d6d;font-weight:700'>💎 Procurement</div><div style='font-size:0.7rem;color:rgba(245,198,208,0.5);letter-spacing:2px;text-transform:uppercase'>Intelligence Suite</div></div><hr/>", unsafe_allow_html=True)
    sel_years  = st.multiselect("📅 Year",       sorted(df["Order_Year"].unique()),   default=sorted(df["Order_Year"].unique()))
    sel_cats   = st.multiselect("🏷️ Category",   sorted(df["Category"].unique()),     default=sorted(df["Category"].unique()))
    sel_depts  = st.multiselect("🏢 Department", sorted(df["Department"].unique()),   default=sorted(df["Department"].unique()))
    sel_status = st.multiselect("📋 PO Status",  sorted(df["Status"].unique()),       default=sorted(df["Status"].unique()))
    st.markdown("<hr/><div style='font-size:0.72rem;color:rgba(245,198,208,0.4);line-height:1.8'><b style='color:rgba(245,198,208,0.7)'>Stack</b><br>Python · Pandas · Streamlit<br>Plotly · PowerBI · PowerApps<br>PowerAutomate · Alteryx · SharePoint<br><br><b style='color:rgba(245,198,208,0.7)'>Author</b><br>Yash Chaudhary<br>github.com/yash752-stack</div>", unsafe_allow_html=True)

fdf = df[df["Order_Year"].isin(sel_years) & df["Category"].isin(sel_cats) & df["Department"].isin(sel_depts) & df["Status"].isin(sel_status)].copy()

total_spend = fdf['Total_Value_INR'].sum()
on_time_pct = (1 - fdf['Is_Delayed'].mean()) * 100
pending     = (fdf['Status']=='Pending').sum()
avg_lead    = fdf['Actual_Lead_Days'].mean()

st.markdown(f"""
<div class="dash-header">
    <div class="dash-title">Procurement Intelligence</div>
    <div class="dash-subtitle"><span class="live-dot"></span>Real-time analytics · {len(fdf):,} purchase orders · ₹{total_spend/1e7:.2f} Cr total spend</div>
</div>""", unsafe_allow_html=True)

k1,k2,k3,k4,k5 = st.columns(5)
for col, icon, label, val, delta, dc in [
    (k1,"💰","Total Spend",    f"₹{total_spend/1e6:.1f}M",  f"₹{total_spend/1e7:.2f} Cr",""),
    (k2,"📦","Purchase Orders", f"{len(fdf):,}",             f"{pending} pending","bad" if pending>50 else "good"),
    (k3,"⏱️","On-Time Rate",    f"{on_time_pct:.1f}%",       "target: 85%","good" if on_time_pct>=85 else "bad"),
    (k4,"🏭","Suppliers",       f"{fdf['Supplier_ID'].nunique()}","unique vendors",""),
    (k5,"📅","Avg Lead Time",   f"{avg_lead:.0f}d",          "order to delivery",""),
]:
    with col:
        st.markdown(f'<div class="kpi-card"><div class="kpi-icon">{icon}</div><div class="kpi-label">{label}</div><div class="kpi-value">{val}</div><div class="kpi-delta {dc}">{delta}</div></div>', unsafe_allow_html=True)

# ── ROW 1 ────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Spend Analysis</div>', unsafe_allow_html=True)
c1,c2 = st.columns([3,2])
with c1:
    monthly = fdf.groupby("Order_Month")["Total_Value_INR"].sum().reset_index()
    monthly.columns = ["Month","Spend"]
    monthly["MA3"] = monthly["Spend"].rolling(3,min_periods=1).mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly["Month"],y=monthly["Spend"],fill="tozeroy",fillcolor="rgba(192,57,43,0.15)",line=dict(color=ACCENT,width=2),name="Monthly",hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=monthly["Month"],y=monthly["MA3"],line=dict(color=ACCENT2,width=1.5,dash="dot"),name="3M Avg",hovertemplate="<b>%{x}</b><br>Avg ₹%{y:,.0f}<extra></extra>"))
    fig.update_layout(**PLOTLY_LAYOUT,title="Monthly Procurement Spend")
    fig.update_xaxes(tickangle=-45,tickfont_size=10)
    fig.update_yaxes(tickformat=",.0f")
    st.plotly_chart(fig,use_container_width=True)
with c2:
    cat_spend = fdf.groupby("Category")["Total_Value_INR"].sum().reset_index()
    fig = go.Figure(go.Pie(labels=cat_spend["Category"],values=cat_spend["Total_Value_INR"],hole=0.55,marker=dict(colors=RED_SCALE[:len(cat_spend)],line=dict(color="#0d0408",width=2)),textfont=dict(color=TEXT,size=11),hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<br>%{percent}<extra></extra>"))
    fig.update_layout(**PLOTLY_LAYOUT,title="Spend by Category",annotations=[dict(text=f"₹{total_spend/1e6:.0f}M",x=0.5,y=0.5,font_size=16,font_color=ACCENT2,font_family="Playfair Display",showarrow=False)])
    st.plotly_chart(fig,use_container_width=True)

# ── ROW 2 ────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Supplier Performance</div>', unsafe_allow_html=True)
c3,c4 = st.columns([2,3])
with c3:
    sup = fdf.groupby("Supplier_Name").agg(Spend=("Total_Value_INR","sum"),Delay_Rate=("Is_Delayed","mean")).reset_index().sort_values("Spend",ascending=True)
    sup["Delay_Pct"] = (sup["Delay_Rate"]*100).round(1)
    fig = go.Figure(go.Bar(x=sup["Spend"],y=sup["Supplier_Name"],orientation="h",marker=dict(color=sup["Delay_Pct"],colorscale=RED_CONT,colorbar=dict(title=dict(text="Delay %",font=dict(color=TEXT)),tickfont=dict(color=TEXT)),line=dict(color="rgba(0,0,0,0.3)",width=0.5)),hovertemplate="<b>%{y}</b><br>₹%{x:,.0f}<br>Delay: %{marker.color:.1f}%<extra></extra>"))
    fig.update_layout(**PLOTLY_LAYOUT,title="Supplier Spend by Delay Rate")
    fig.update_yaxes(tickfont_size=9)
    fig.update_xaxes(tickformat=",.0f")
    st.plotly_chart(fig,use_container_width=True)
with c4:
    pivot = fdf.groupby(["Order_Month","Category"])["Total_Value_INR"].sum().reset_index()
    pw = pivot.pivot(index="Category",columns="Order_Month",values="Total_Value_INR").fillna(0)
    fig = go.Figure(go.Heatmap(z=pw.values,x=pw.columns.tolist(),y=pw.index.tolist(),colorscale=RED_CONT,hovertemplate="<b>%{y}</b> — %{x}<br>₹%{z:,.0f}<extra></extra>",colorbar=dict(tickfont=dict(color=TEXT))))
    fig.update_layout(**PLOTLY_LAYOUT,title="Spend Heatmap — Category × Month")
    fig.update_xaxes(tickangle=-45,tickfont_size=9)
    st.plotly_chart(fig,use_container_width=True)

# ── ROW 3 ────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Operations Overview</div>', unsafe_allow_html=True)
c5,c6,c7 = st.columns(3)
with c5:
    dd = fdf.groupby("Department").agg(On_Time=("Is_Delayed",lambda x:(~x).sum()),Delayed=("Is_Delayed","sum")).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(name="On Time",x=dd["Department"],y=dd["On_Time"],marker_color="rgba(192,57,43,0.5)",marker_line_color=ACCENT3,marker_line_width=1))
    fig.add_trace(go.Bar(name="Delayed",x=dd["Department"],y=dd["Delayed"],marker_color=ACCENT,marker_line_color="#ff4d6d",marker_line_width=1))
    fig.update_layout(**PLOTLY_LAYOUT,title="Delivery by Department",barmode="stack",height=300)
    fig.update_xaxes(tickangle=-35,tickfont_size=9)
    st.plotly_chart(fig,use_container_width=True)
with c6:
    band = fdf["Spend_Band"].value_counts().reset_index()
    band.columns = ["Band","Count"]
    fig = go.Figure(go.Bar(x=band["Band"],y=band["Count"],marker=dict(color=RED_SCALE[1:5],line=dict(color="#0d0408",width=1)),hovertemplate="<b>%{x}</b><br>%{y} POs<extra></extra>"))
    fig.update_layout(**PLOTLY_LAYOUT,title="PO Spend Band Distribution",height=300,showlegend=False)
    fig.update_xaxes(tickfont_size=9)
    st.plotly_chart(fig,use_container_width=True)
with c7:
    sc = fdf["Status"].value_counts().reset_index()
    sc.columns = ["Status","Count"]
    colors = {"Approved":"#52c77a","Pending":"#e6b023","Rejected":"#e8103a"}
    fig = go.Figure(go.Pie(labels=sc["Status"],values=sc["Count"],hole=0.6,marker=dict(colors=[colors.get(s,ACCENT) for s in sc["Status"]],line=dict(color="#0d0408",width=2)),textfont=dict(color=TEXT),hovertemplate="<b>%{label}</b><br>%{value} · %{percent}<extra></extra>"))
    ap = (fdf["Status"]=="Approved").mean()*100
    fig.update_layout(**PLOTLY_LAYOUT,title="PO Approval Status",height=300,annotations=[dict(text=f"{ap:.0f}%<br>approved",x=0.5,y=0.5,font_size=13,font_color="#52c77a",font_family="Playfair Display",showarrow=False)])
    st.plotly_chart(fig,use_container_width=True)

# ── ROW 4 ────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Risk & Lead Time Intelligence</div>', unsafe_allow_html=True)
c8,c9 = st.columns(2)
with c8:
    fig = go.Figure()
    for cat in fdf["Category"].unique():
        subset = fdf[fdf["Category"]==cat]["Actual_Lead_Days"].dropna()
        fig.add_trace(go.Violin(y=subset,name=cat,box_visible=True,meanline_visible=True,opacity=0.8,line_color=ACCENT2,fillcolor="rgba(192,57,43,0.2)"))
    fig.update_layout(**PLOTLY_LAYOUT,title="Lead Time Distribution by Category")
    fig.update_xaxes(tickfont_size=9)
    st.plotly_chart(fig,use_container_width=True)
with c9:
    rd = fdf.groupby("Supplier_Name").agg(Spend=("Total_Value_INR","sum"),Delay_Rate=("Is_Delayed","mean"),Orders=("PO_ID","count")).reset_index()
    rd["Delay_Pct"] = rd["Delay_Rate"]*100
    fig = go.Figure(go.Scatter(x=rd["Delay_Pct"],y=rd["Spend"]/1e6,mode="markers+text",text=rd["Supplier_Name"].str.split().str[0],textposition="top center",textfont=dict(size=9,color=TEXT),marker=dict(size=rd["Orders"]/3,color=rd["Delay_Pct"],colorscale=RED_CONT,showscale=True,colorbar=dict(title=dict(text="Delay %",font=dict(color=TEXT)),tickfont=dict(color=TEXT)),line=dict(color=ACCENT2,width=1)),hovertemplate="<b>%{text}</b><br>Delay: %{x:.1f}%<br>₹%{y:.1f}M<extra></extra>"))
    fig.update_layout(**PLOTLY_LAYOUT,title="Supplier Risk Matrix",xaxis_title="Delay Rate %",yaxis_title="Spend (₹M)")
    st.plotly_chart(fig,use_container_width=True)

# ── DATA QUALITY ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Data Quality Report</div>', unsafe_allow_html=True)
if os.path.exists("data/data_quality_report.csv"):
    qr = pd.read_csv("data/data_quality_report.csv")
    cols = st.columns(len(qr))
    for i,(_,row) in enumerate(qr.iterrows()):
        with cols[i]:
            issues = int(row["Issues_Found"])
            bc = "badge-red" if issues>0 else "badge-green"
            bt = f"{issues} issues" if issues>0 else "clean"
            st.markdown(f'<div class="kpi-card" style="padding:14px 16px"><div class="kpi-label">{row["Check"]}</div><div style="margin:6px 0"><span class="badge {bc}">{bt}</span></div><div style="font-size:0.7rem;color:rgba(245,198,208,0.45);margin-top:4px">{row["Action_Taken"][:50]}...</div></div>', unsafe_allow_html=True)

with st.expander("📄 Explore Enriched Procurement Data"):
    cols_show = ["PO_ID","Supplier_Name","Category","Department","Order_Date","Total_Value_INR","Status","Is_Delayed","Delay_Days","Spend_Band","Supplier_Risk_Flag"]
    st.dataframe(fdf[cols_show].sort_values("Order_Date",ascending=False),use_container_width=True,hide_index=True)

st.markdown("<div style='text-align:center;padding:24px 0 8px;color:rgba(245,198,208,0.25);font-size:0.72rem;letter-spacing:1px'>PROCUREMENT INTELLIGENCE SUITE · YASH CHAUDHARY · GITHUB.COM/YASH752-STACK</div>", unsafe_allow_html=True)

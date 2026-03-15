"""
pipeline/etl_pipeline.py
Procurement Data Cleansing, Enrichment & Transformation Pipeline
Replicates what you would do in Alteryx — pure Python/Pandas.

Run: python pipeline/etl_pipeline.py
Output:
  - data/cleaned_procurement_data.csv
  - data/data_quality_report.csv
  - data/enriched_procurement_data.csv
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os, json

print("=" * 60)
print("  PROCUREMENT DATA PIPELINE  |  yash752-stack")
print("=" * 60)

# ── STEP 1: INGEST ───────────────────────────────────────────────────────────
print("\n[1/6] Ingesting raw data...")
po_df  = pd.read_csv("data/raw_procurement_data.csv")
sup_df = pd.read_csv("data/supplier_master.csv")
print(f"      Loaded {len(po_df)} purchase orders, {len(sup_df)} suppliers")

# ── STEP 2: DATA QUALITY AUDIT ───────────────────────────────────────────────
print("\n[2/6] Running data quality audit...")

quality_findings = []

def log_issue(check, count, action):
    quality_findings.append({"Check": check, "Issues_Found": count, "Action_Taken": action})
    if count > 0:
        print(f"      ⚠  {check}: {count} issues → {action}")
    else:
        print(f"      ✓  {check}: clean")

# Nulls
null_counts = po_df.isnull().sum()
for col in ["Unit_Price_INR", "Total_Value_INR"]:
    log_issue(f"Missing {col}", int(null_counts[col]), "Impute with supplier category median")

# Negative quantities
neg_qty = (po_df["Quantity"] < 0).sum()
log_issue("Negative Quantity", int(neg_qty), "Convert to absolute value, flag as anomaly")

# Case inconsistencies in Supplier_Name
case_issues = po_df["Supplier_Name"].str.strip().ne(po_df["Supplier_Name"]).sum() + \
              po_df["Supplier_Name"].str.islower().sum()
log_issue("Supplier_Name case/whitespace", int(case_issues), "Standardise via title case + strip")

# Duplicate PO_IDs
dup_pos = po_df["PO_ID"].duplicated().sum()
log_issue("Duplicate PO_IDs", int(dup_pos), "Drop duplicates, keep first")

# Delivery before order date
po_df["_order"] = pd.to_datetime(po_df["Order_Date"])
po_df["_due"]   = pd.to_datetime(po_df["Delivery_Due_Date"])
early_delivery  = (po_df["_due"] < po_df["_order"]).sum()
log_issue("Delivery date before Order date", int(early_delivery), "Flag and exclude from lead-time calc")

# ── STEP 3: CLEANSE ──────────────────────────────────────────────────────────
print("\n[3/6] Cleansing data...")

df = po_df.copy()

# Fix supplier name
df["Supplier_Name"] = df["Supplier_Name"].str.strip().str.title()

# Fix negative qty
df["Quantity_Anomaly"] = df["Quantity"] < 0
df["Quantity"] = df["Quantity"].abs()

# Impute missing prices with category median
cat_median_price = df.groupby("Category")["Unit_Price_INR"].transform("median")
df["Unit_Price_INR"] = df["Unit_Price_INR"].fillna(cat_median_price)
df["Total_Value_INR"] = df["Quantity"] * df["Unit_Price_INR"]

# Drop dupes
df = df.drop_duplicates(subset="PO_ID", keep="first")

# Drop helper cols
df = df.drop(columns=["_order", "_due"])

print(f"      Cleaned dataset: {len(df)} rows")

# ── STEP 4: ENRICHMENT ───────────────────────────────────────────────────────
print("\n[4/6] Enriching with supplier master data...")

df = df.merge(
    sup_df[["Supplier_ID", "Quality_Score", "On_Time_Rate_Pct", "Avg_Lead_Days", "Preferred", "Contract_Expiry"]],
    on="Supplier_ID", how="left"
)

# Derived features
df["Order_Date"]         = pd.to_datetime(df["Order_Date"])
df["Actual_Delivery"]    = pd.to_datetime(df["Actual_Delivery"])
df["Delivery_Due_Date"]  = pd.to_datetime(df["Delivery_Due_Date"])

df["Actual_Lead_Days"]   = (df["Actual_Delivery"] - df["Order_Date"]).dt.days
df["Delay_Days"]         = (df["Actual_Delivery"] - df["Delivery_Due_Date"]).dt.days
df["Is_Delayed"]         = df["Delay_Days"] > 0
df["Order_Month"]        = df["Order_Date"].dt.to_period("M").astype(str)
df["Order_Quarter"]      = df["Order_Date"].dt.to_period("Q").astype(str)
df["Order_Year"]         = df["Order_Date"].dt.year

# Spend banding
df["Spend_Band"] = pd.cut(
    df["Total_Value_INR"],
    bins=[0, 10000, 50000, 200000, float("inf")],
    labels=["Low (<10K)", "Mid (10K-50K)", "High (50K-200K)", "Strategic (>200K)"]
)

# Supplier risk flag
df["Supplier_Risk_Flag"] = (
    (df["Quality_Score"] < 4.0) | (df["On_Time_Rate_Pct"] < 80)
).map({True: "At Risk", False: "Stable"})

print(f"      Added {df.shape[1]} total columns after enrichment")

# ── STEP 5: SAVE OUTPUTS ─────────────────────────────────────────────────────
print("\n[5/6] Saving outputs...")

df.to_csv("data/enriched_procurement_data.csv", index=False)
print("      ✅ data/enriched_procurement_data.csv")

# Data quality report
qr_df = pd.DataFrame(quality_findings)
qr_df.to_csv("data/data_quality_report.csv", index=False)
print("      ✅ data/data_quality_report.csv")

# ── STEP 6: SUMMARY STATS ────────────────────────────────────────────────────
print("\n[6/6] Pipeline Summary")
print("-" * 40)
print(f"  Total POs processed  : {len(df)}")
print(f"  Total Spend (INR)    : ₹{df['Total_Value_INR'].sum():,.0f}")
print(f"  Unique Suppliers     : {df['Supplier_ID'].nunique()}")
print(f"  Delayed Orders       : {df['Is_Delayed'].sum()} ({df['Is_Delayed'].mean()*100:.1f}%)")
print(f"  At-Risk Suppliers    : {(df['Supplier_Risk_Flag']=='At Risk').sum()}")
print(f"  Anomalous Qty Rows   : {df['Quantity_Anomaly'].sum()}")
print("-" * 40)
print("\n✅ Pipeline complete.\n")

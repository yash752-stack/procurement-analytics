"""
generate_data.py
Generates synthetic procurement dataset simulating real supplier/PO data.
Run: python data/generate_data.py
Output: data/raw_procurement_data.csv, data/supplier_master.csv
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

random.seed(42)
np.random.seed(42)

# ── Config ──────────────────────────────────────────────────────────────────
N_ORDERS = 500
START_DATE = datetime(2023, 1, 1)
END_DATE   = datetime(2025, 3, 1)

SUPPLIERS = [
    ("SUP001", "Tata Steel Supplies",       "Raw Materials",  "India",        4.2),
    ("SUP002", "Infosys BPO Services",      "IT Services",    "India",        4.5),
    ("SUP003", "Mahindra Logistics",        "Logistics",      "India",        3.8),
    ("SUP004", "Reliance Office Supplies",  "Office",         "India",        4.0),
    ("SUP005", "L&T Construction",          "Construction",   "India",        4.3),
    ("SUP006", "HCL Tech Solutions",        "IT Services",    "India",        4.6),
    ("SUP007", "HDFC Equipment Finance",    "Equipment",      "India",        3.9),
    ("SUP008", "Wipro Facilities",          "Facilities",     "India",        4.1),
    ("SUP009", "Asian Paints Industrial",   "Raw Materials",  "India",        3.7),
    ("SUP010", "DHL Express India",         "Logistics",      "India",        4.4),
]

CATEGORIES   = ["Raw Materials", "IT Services", "Logistics", "Office", "Construction", "Equipment", "Facilities"]
DEPARTMENTS  = ["Finance", "Operations", "HR", "IT", "Procurement", "Legal", "Marketing"]
STATUSES     = ["Approved", "Approved", "Approved", "Pending", "Rejected"]   # weighted
PAYMENT_TERMS = ["Net 30", "Net 45", "Net 60", "Immediate"]

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# ── Purchase Orders ──────────────────────────────────────────────────────────
rows = []
for i in range(N_ORDERS):
    sup = random.choice(SUPPLIERS)
    order_date    = random_date(START_DATE, END_DATE)
    delivery_date = order_date + timedelta(days=random.randint(7, 90))
    actual_delivery = delivery_date + timedelta(days=random.randint(-5, 20))
    qty   = random.randint(1, 200)
    price = round(random.uniform(500, 150000), 2)

    # Inject some data quality issues for the pipeline to fix
    supplier_name = sup[1]
    if random.random() < 0.05:
        supplier_name = supplier_name.lower()          # case issue
    if random.random() < 0.04:
        supplier_name = supplier_name + "  "           # trailing spaces
    if random.random() < 0.03:
        price = None                                   # missing value
    if random.random() < 0.02:
        qty = -qty                                     # invalid negative qty

    rows.append({
        "PO_ID":              f"PO-{2023 + i // 200}-{str(i+1).zfill(4)}",
        "Supplier_ID":        sup[0],
        "Supplier_Name":      supplier_name,
        "Category":           sup[2],
        "Department":         random.choice(DEPARTMENTS),
        "Order_Date":         order_date.strftime("%Y-%m-%d"),
        "Delivery_Due_Date":  delivery_date.strftime("%Y-%m-%d"),
        "Actual_Delivery":    actual_delivery.strftime("%Y-%m-%d"),
        "Quantity":           qty,
        "Unit_Price_INR":     price,
        "Total_Value_INR":    round(qty * price, 2) if price else None,
        "Payment_Terms":      random.choice(PAYMENT_TERMS),
        "Status":             random.choice(STATUSES),
        "Invoice_Received":   random.choice([True, False]),
        "Country":            sup[3],
    })

po_df = pd.DataFrame(rows)
os.makedirs("data", exist_ok=True)
po_df.to_csv("data/raw_procurement_data.csv", index=False)
print(f"✅ Generated {len(po_df)} purchase orders → data/raw_procurement_data.csv")

# ── Supplier Master ──────────────────────────────────────────────────────────
sup_rows = []
for sup in SUPPLIERS:
    sup_rows.append({
        "Supplier_ID":       sup[0],
        "Supplier_Name":     sup[1],
        "Category":          sup[2],
        "Country":           sup[3],
        "Quality_Score":     sup[4],
        "On_Time_Rate_Pct":  round(random.uniform(70, 98), 1),
        "Avg_Lead_Days":     random.randint(10, 45),
        "Contract_Expiry":   random_date(datetime(2025, 1, 1), datetime(2026, 12, 31)).strftime("%Y-%m-%d"),
        "Preferred":         random.choice([True, False]),
    })

sup_df = pd.DataFrame(sup_rows)
sup_df.to_csv("data/supplier_master.csv", index=False)
print(f"✅ Generated {len(sup_df)} suppliers → data/supplier_master.csv")

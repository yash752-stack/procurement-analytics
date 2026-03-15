# 📦 Procurement Analytics & Workflow Automation System

> End-to-end procurement intelligence platform — SharePoint data repository, PowerApps entry form, PowerAutomate workflows, Python/Alteryx-equivalent ETL pipeline, and a live Streamlit + Plotly BI dashboard.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![PowerAutomate](https://img.shields.io/badge/PowerAutomate-Automated_Flows-0066FF?style=flat&logo=microsoft&logoColor=white)
![PowerApps](https://img.shields.io/badge/PowerApps-Canvas_App-742774?style=flat&logo=microsoft&logoColor=white)
![SharePoint](https://img.shields.io/badge/SharePoint-Data_Repository-0078D4?style=flat&logo=microsoft&logoColor=white)

---

## 🎯 Project Overview

This project simulates a real procurement analytics system as deployed in a finance/banking environment. It covers the full BI & data analyst workflow:

| Layer | Tool | Purpose |
|---|---|---|
| Data Entry | PowerApps + SharePoint | Structured PO submission form → SharePoint list |
| Automation | PowerAutomate | Approval triggers, daily summaries, Power BI refresh |
| ETL Pipeline | Python (Pandas / Alteryx-equivalent) | Cleansing, enrichment, quality documentation |
| BI Dashboard | Streamlit + Plotly | Live procurement dashboard with KPIs and drill-downs |
| Reporting | Excel (Power Query + VBA) | Template-based spend reports with scheduled refresh |

---

## 🏗️ Architecture

```
PowerApps Form
      │
      ▼
SharePoint List (Purchase Orders + Supplier Master)
      │
      ├──► PowerAutomate Flow 1: High-value PO alert + auto-approval
      ├──► PowerAutomate Flow 2: Daily summary email (8 AM)
      └──► PowerAutomate Flow 3: Power BI dataset refresh trigger
      │
      ▼
Python ETL Pipeline (pipeline/etl_pipeline.py)
  ├── Data Quality Audit    → flags nulls, negatives, duplicates, case issues
  ├── Data Cleansing        → standardise, impute, deduplicate
  ├── Data Enrichment       → supplier scores, lead time, delay flags, spend bands
  └── Quality Report        → data/data_quality_report.csv
      │
      ▼
Streamlit Dashboard (dashboard/app.py)
  ├── KPI Cards             → Total Spend, PO Count, On-Time %, Avg Lead Time
  ├── Monthly Spend Trend   → Area chart with period toggles
  ├── Spend by Category     → Pie chart
  ├── Supplier Scorecard    → Ranked bar chart coloured by delay rate
  ├── Delay Analysis        → Stacked bar by department
  ├── Spend Band Distribution
  ├── PO Status Breakdown
  └── Data Quality Report table
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Microsoft 365 account (for SharePoint / PowerApps / PowerAutomate)

### 1. Clone the repo
```bash
git clone https://github.com/yash752-stack/procurement-analytics.git
cd procurement-analytics
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate synthetic data
```bash
python data/generate_data.py
```

### 4. Run the ETL pipeline
```bash
python pipeline/etl_pipeline.py
```

### 5. Launch the dashboard
```bash
streamlit run dashboard/app.py
```

Open http://localhost:8501 in your browser.

---

## 📊 Dashboard Preview

> *(Add screenshot here after running locally)*

**Key Metrics tracked:**
- 💰 Total procurement spend (₹M)
- 📦 Purchase order volume & approval status
- ⏱️ On-time delivery rate by supplier & department
- 🏭 Supplier scorecard (quality score, delay rate, spend rank)
- 🔍 Data quality findings with actionable recommendations

---

## 🔧 Microsoft 365 Setup

### SharePoint
See [`sharepoint/SHAREPOINT_SETUP.md`](sharepoint/SHAREPOINT_SETUP.md) for step-by-step list creation.

### PowerApps
See [`powerapps/POWERAPPS_SETUP.md`](powerapps/POWERAPPS_SETUP.md) for the canvas app build guide including submit button formula and validation logic.

### PowerAutomate
See [`powerautomate/POWERAUTOMATE_SETUP.md`](powerautomate/POWERAUTOMATE_SETUP.md) for all 3 flows:
- Flow 1: New PO alert + conditional auto-approval
- Flow 2: Daily 8 AM procurement summary email
- Flow 3: Power BI dataset refresh on new PO

---

## 📁 Project Structure

```
procurement-analytics/
├── data/
│   ├── generate_data.py              # Synthetic procurement dataset generator
│   ├── raw_procurement_data.csv      # Raw data (500 POs, injected quality issues)
│   ├── enriched_procurement_data.csv # Post-pipeline enriched data
│   └── data_quality_report.csv       # Documented quality findings
├── pipeline/
│   └── etl_pipeline.py               # 6-step ETL: audit → cleanse → enrich → export
├── dashboard/
│   └── app.py                        # Streamlit + Plotly BI dashboard
├── sharepoint/
│   └── SHAREPOINT_SETUP.md           # SharePoint list setup guide
├── powerapps/
│   └── POWERAPPS_SETUP.md            # PowerApps canvas form build guide
├── powerautomate/
│   └── POWERAUTOMATE_SETUP.md        # 3 PowerAutomate flows
├── docs/
│   └── (screenshots go here)
├── requirements.txt
└── README.md
```

---

## 🔍 Data Quality Pipeline

The ETL pipeline deliberately ingests dirty data and documents every issue found:

| Check | Issues Injected | Action |
|---|---|---|
| Missing Unit_Price_INR | ~3% rows | Imputed with category median |
| Negative Quantity | ~2% rows | Absolute value + anomaly flag |
| Supplier name casing | ~5% rows | Title case + strip |
| Duplicate PO_IDs | possible | Drop duplicates, keep first |
| Delivery before Order date | edge cases | Flagged, excluded from lead-time calc |

All findings written to `data/data_quality_report.csv` and displayed in the dashboard.

---

## 👤 Author

**Yash Chaudhary**
- GitHub: [@yash752-stack](https://github.com/yash752-stack)
- LinkedIn: [linkedin.com/in/yash-chaudhary](#)
- Built for: Barclays BI & Data Analyst — Procurement (Noida)

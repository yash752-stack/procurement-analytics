# SharePoint Setup Guide

## What you're building
A SharePoint List that acts as the central data store for procurement PO entries.
PowerApps will sit on top of this as the data entry form.
PowerAutomate will trigger whenever a new PO is submitted.

---

## Step-by-Step (on friend's M365 laptop)

### 1. Create SharePoint Site
1. Go to https://www.office.com → SharePoint
2. Click **+ Create site** → Team site
3. Name: `Procurement Analytics Hub`
4. Privacy: Private
5. Click **Finish**

### 2. Create the Purchase Orders List
1. In your new site → **+ New** → **List**
2. Name it: `Purchase Orders`
3. Add these columns (click **+ Add column**):

| Column Name       | Type              | Notes                        |
|-------------------|-------------------|------------------------------|
| PO_ID             | Single line text  | Auto-generated in PowerApps  |
| Supplier_Name     | Choice            | Add the 10 suppliers         |
| Category          | Choice            | Raw Materials, IT, Logistics… |
| Department        | Choice            | Finance, Ops, HR, IT…        |
| Order_Date        | Date and time     |                              |
| Quantity          | Number            |                              |
| Unit_Price_INR    | Currency          | Set to INR                   |
| Total_Value_INR   | Calculated        | =Quantity*Unit_Price_INR     |
| Payment_Terms     | Choice            | Net 30, Net 45, Net 60       |
| Status            | Choice            | Pending (default), Approved  |
| Invoice_Received  | Yes/No            |                              |
| Submitted_By      | Person            |                              |

### 3. Create Supplier Master List
Same steps — name it `Supplier Master`
Columns: Supplier_ID, Supplier_Name, Category, Country, Quality_Score, On_Time_Rate_Pct, Preferred

---

## SharePoint → Power BI Connection
1. In Power BI Desktop → **Get Data** → **SharePoint Online List**
2. Enter your SharePoint site URL
3. Select `Purchase Orders` list
4. Transform & load

This connects your live SharePoint data to Power BI dashboards automatically.

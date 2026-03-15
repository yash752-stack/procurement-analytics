# PowerAutomate — Procurement Workflow Automation

## Flows to build (2 flows)

---

## Flow 1: New PO Notification + Approval Trigger

**Trigger:** When a new item is created in `Purchase Orders` SharePoint list

**Steps:**
1. Go to https://make.powerautomate.com
2. **+ Create** → **Automated cloud flow**
3. Name: `PO Submission Alert`
4. Trigger: **When an item is created** (SharePoint)
   - Site: your SharePoint site URL
   - List: `Purchase Orders`

**Add Actions:**

```
Action 1: Condition
  Check: Total_Value_INR is greater than 50000
  
  If YES (high-value PO):
    Action: Send an email (V2)
      To:      [your email]
      Subject: "🔔 High-Value PO Submitted: " + Title
      Body:    "Supplier: " + Supplier_Name
               "Value: ₹" + Total_Value_INR
               "Department: " + Department
               "Submitted by: " + Submitted_By
               "Status: Pending Approval"

  If NO (standard PO):
    Action: Update item (SharePoint)
      List: Purchase Orders
      ID:   ID (from trigger)
      Status: Approved   ← auto-approve low value POs
```

---

## Flow 2: Daily Procurement Summary Report

**Trigger:** Scheduled — every day at 8:00 AM

**Steps:**
1. **+ Create** → **Scheduled cloud flow**
2. Name: `Daily PO Summary`
3. Repeat: Every 1 day at 8:00 AM

**Add Actions:**

```
Action 1: Get items (SharePoint)
  List: Purchase Orders
  Filter Query: Order_Date ge '@{formatDateTime(addDays(utcNow(),-1), 'yyyy-MM-dd')}'

Action 2: Send an email (V2)
  To:      [your email]
  Subject: "📊 Daily Procurement Summary - " + formatDateTime(utcNow(), 'dd MMM yyyy')
  Body:    "New POs submitted yesterday: " + length(body('Get_items')?['value'])
           "Review pending approvals at: [SharePoint link]"
```

---

## Flow 3 (bonus): Data Refresh Trigger for Power BI

```
Trigger: When an item is created (SharePoint → Purchase Orders)
Action:  HTTP POST to Power BI dataset refresh API
  URL:   https://api.powerbi.com/v1.0/myorg/datasets/{datasetId}/refreshes
  Method: POST
  Headers: Authorization: Bearer [token]
```

This auto-refreshes your Power BI dashboard whenever a new PO is submitted.

---

## Screenshot for GitHub
Export each flow as a screenshot → save in `docs/powerautomate_flow1.png` etc.

# PowerApps — Procurement PO Entry Form

## What you're building
A canvas app that lets any department submit a Purchase Order
directly into the SharePoint `Purchase Orders` list.

---

## Step-by-Step

### 1. Create the App
1. Go to https://make.powerapps.com
2. **+ Create** → **Canvas app from blank**
3. Name: `PO Submission Form`
4. Format: Tablet

### 2. Connect to SharePoint
1. Left panel → **Data** → **+ Add data**
2. Search `SharePoint` → connect to your site
3. Select `Purchase Orders` and `Supplier Master` lists

### 3. Build the Form — Add these controls

**Screen layout (top to bottom):**

```
[Header Label]  "New Purchase Order"  — bold, navy (#1A2B4A)

[Supplier_Name]   Dropdown  → Items: Distinct(SupplierMaster, Supplier_Name)
[Category]        Dropdown  → Items: ["Raw Materials","IT Services","Logistics","Office","Equipment","Facilities"]
[Department]      Dropdown  → Items: ["Finance","Operations","HR","IT","Procurement","Legal"]
[Order_Date]      DatePicker → DefaultDate: Today()
[Quantity]        Text Input → InputTextMode: Number
[Unit_Price_INR]  Text Input → InputTextMode: Number
[Total_Value]     Label     → Text: "₹" & Text(Value(Quantity.Text) * Value(UnitPrice.Text), "#,##0")
[Payment_Terms]   Dropdown  → Items: ["Net 30","Net 45","Net 60","Immediate"]
[Invoice_Received] Toggle

[SUBMIT Button]
```

### 4. Submit Button Formula
```
Patch(
    'Purchase Orders',
    Defaults('Purchase Orders'),
    {
        Title:           "PO-" & Text(Now(), "YYYY-MM-DD-HHMMSS"),
        Supplier_Name:   SupplierDropdown.Selected.Value,
        Category:        CategoryDropdown.Selected.Value,
        Department:      DeptDropdown.Selected.Value,
        Order_Date:      OrderDatePicker.SelectedDate,
        Quantity:        Value(QuantityInput.Text),
        Unit_Price_INR:  Value(UnitPriceInput.Text),
        Total_Value_INR: Value(QuantityInput.Text) * Value(UnitPriceInput.Text),
        Payment_Terms:   PaymentDropdown.Selected.Value,
        Invoice_Received: InvoiceToggle.Value,
        Status:          "Pending"
    }
);
Notify("✅ PO submitted successfully!", NotificationType.Success);
ResetForm(EditForm1)
```

### 5. Validation Rules (add to Submit button's DisplayMode)
```
If(
    IsBlank(SupplierDropdown.Selected.Value) ||
    IsBlank(QuantityInput.Text) ||
    Value(QuantityInput.Text) <= 0 ||
    Value(UnitPriceInput.Text) <= 0,
    DisplayMode.Disabled,
    DisplayMode.Edit
)
```

### 6. Publish
1. **File** → **Save** → **Publish**
2. Share with your Microsoft account
3. Access at: https://make.powerapps.com/play/...

---

## Screenshot for GitHub
Take a screenshot of the app after building — save as `docs/powerapps_screenshot.png`

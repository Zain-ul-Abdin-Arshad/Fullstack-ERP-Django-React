# Purchase Models - Quick Reference

## Models Created

✅ **PurchaseOrder** - Purchase orders from vendors  
✅ **PurchaseItem** - Individual items with landed cost calculation

## Required Fields

### PurchaseOrder
- `vendor` (FK to Vendor) ✅
- `order_number` (unique) ✅
- `order_date` ✅
- `total_amount` (auto-calculated) ✅
- `status` (PENDING/RECEIVED) ✅

### PurchaseItem
- `purchase_order` (FK) ✅
- `item` (FK to Item) ✅
- `quantity` ✅
- `unit_cost` ✅
- `freight_cost` ✅
- `customs_duty` ✅
- `landed_cost_per_unit` (auto-calculated) ✅
- `total_landed_cost` (auto-calculated) ✅

## Landed Cost Formula

```
Additional Costs Per Unit = (Freight + Customs + Other) / Quantity
Landed Cost Per Unit = Unit Cost + Additional Costs Per Unit
Total Landed Cost = Landed Cost Per Unit × Quantity
```

## Quick Usage

```python
from purchases.models import PurchaseOrder, PurchaseItem
from vendors.models import Vendor
from inventory.models import Item
from datetime import date

# Create Purchase Order
vendor = Vendor.objects.get(name="ABC Suppliers")
po = PurchaseOrder.objects.create(
    vendor=vendor,
    order_number="PO-2024-001",
    order_date=date.today(),
    status="PENDING"
)

# Create Purchase Item (landed costs auto-calculated)
item = Item.objects.get(sku="BATT-001")
purchase_item = PurchaseItem.objects.create(
    purchase_order=po,
    item=item,
    quantity=100,
    unit_cost=50.00,
    freight_cost=500.00,
    customs_duty=200.00,
    other_costs=100.00
)

# Landed costs automatically calculated:
# landed_cost_per_unit = 58.00
# total_landed_cost = 5800.00
```

## Status Choices

- `PENDING` - Order pending
- `RECEIVED` - Fully received
- `PARTIAL` - Partially received
- `CANCELLED` - Cancelled

## Helper Methods

### PurchaseOrder
- `calculate_total()` - Recalculate total from items
- `get_item_count()` - Number of items
- `get_total_quantity()` - Total quantity
- `mark_as_received()` - Mark as received

### PurchaseItem
- `calculate_landed_cost()` - Calculate landed costs
- `get_cost_breakdown()` - Detailed cost breakdown
- `is_fully_received()` - Check if fully received
- `get_pending_quantity()` - Get pending quantity

## Files Created

- `backend/purchases/models.py` - Purchase models
- `backend/purchases/admin.py` - Admin configuration

## Next Steps

```powershell
# Create migrations
python manage.py makemigrations purchases

# Apply migrations
python manage.py migrate
```

## Example: Complete Purchase Flow

```python
# 1. Create Purchase Order
po = PurchaseOrder.objects.create(
    vendor=vendor,
    order_number="PO-001",
    order_date=date.today(),
    status="PENDING"
)

# 2. Add Items (landed costs auto-calculated)
item1 = PurchaseItem.objects.create(
    purchase_order=po,
    item=item,
    quantity=100,
    unit_cost=50.00,
    freight_cost=500.00,
    customs_duty=200.00
)

# 3. Order total auto-updated
print(po.total_amount)  # Shows total

# 4. Mark as received
po.mark_as_received()

# 5. Update received quantities
item1.received_quantity = 100
item1.save()
```


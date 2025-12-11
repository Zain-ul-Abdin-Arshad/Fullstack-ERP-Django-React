# Sales Models - Quick Reference

## Models Created

✅ **SalesOrder** - Sales orders from clients  
✅ **SalesItem** - Individual items with stock reduction logic

## Required Fields

### SalesOrder
- `client` (FK to Client) ✅
- `order_number` (unique) ✅
- `order_date` ✅
- `total_amount` (auto-calculated) ✅
- `status` (PENDING/SHIPPED/DELIVERED) ✅

### SalesItem
- `sales_order` (FK) ✅
- `item` (FK to Item) ✅
- `quantity` ✅
- `unit_price` ✅
- `line_total` (auto-calculated) ✅

## Stock Reduction Logic

### Status Flow

```
PENDING → Stock Reserved (reserved_quantity ↑)
SHIPPED → Stock Reduced (quantity ↓, reserved_quantity ↓)
DELIVERED → Stock Reduced (quantity ↓, reserved_quantity ↓)
CANCELLED → Stock Released (reserved_quantity ↓)
```

### Automatic Operations

- **Order Created (PENDING)**: Stock automatically reserved
- **Order Shipped**: Stock automatically reduced
- **Order Delivered**: Stock automatically reduced
- **Order Cancelled**: Reserved stock automatically released

## Quick Usage

```python
from sales.models import SalesOrder, SalesItem
from clients.models import Client
from inventory.models import Warehouse, Item
from datetime import date

# Create Sales Order
client = Client.objects.get(name="ABC Auto Shop")
warehouse = Warehouse.objects.get(code="WH-001")
so = SalesOrder.objects.create(
    client=client,
    order_number="SO-2024-001",
    order_date=date.today(),
    warehouse=warehouse,
    status="PENDING"  # Stock automatically reserved
)

# Create Sales Item
item = Item.objects.get(sku="BATT-001")
sales_item = SalesItem.objects.create(
    sales_order=so,
    item=item,
    quantity=10,
    unit_price=75.00,
    discount_percentage=5.00
)
# Line total auto-calculated: 712.50
# Stock automatically reserved

# Ship Order (stock automatically reduced)
so.mark_as_shipped()
```

## Status Choices

- `PENDING` - Order pending (stock reserved)
- `CONFIRMED` - Order confirmed
- `SHIPPED` - Order shipped (stock reduced)
- `DELIVERED` - Order delivered (stock reduced)
- `CANCELLED` - Order cancelled (stock released)

## Helper Methods

### SalesOrder
- `calculate_total()` - Recalculate total from items
- `get_item_count()` - Number of items
- `get_total_quantity()` - Total quantity
- `reserve_stock()` - Reserve stock
- `release_reserved_stock()` - Release reserved stock
- `reduce_stock()` - Reduce stock
- `mark_as_shipped()` - Mark as shipped & reduce stock
- `mark_as_delivered()` - Mark as delivered
- `cancel_order()` - Cancel & release stock

### SalesItem
- `calculate_line_total()` - Calculate line total
- `check_stock_availability()` - Check if stock available
- `reserve_stock()` - Reserve stock
- `release_reserved_stock()` - Release stock
- `reduce_stock()` - Reduce stock
- `get_profit_margin()` - Calculate profit margin %
- `get_profit_amount()` - Calculate total profit

## Stock Impact Example

```python
# Initial stock: quantity=100, reserved=0

# Create PENDING order (qty=10)
# → quantity=100, reserved=10, available=90

# Ship order
# → quantity=90, reserved=0, available=90

# Cancel order (if cancelled)
# → quantity=100, reserved=0, available=100
```

## Files Created

- `backend/sales/models.py` - Sales models with stock reduction
- `backend/sales/admin.py` - Admin configuration

## Next Steps

```powershell
# Create migrations
python manage.py makemigrations sales

# Apply migrations
python manage.py migrate
```

## Example: Complete Sales Flow

```python
# 1. Create Sales Order
so = SalesOrder.objects.create(
    client=client,
    order_number="SO-001",
    order_date=date.today(),
    warehouse=warehouse,
    status="PENDING"
)

# 2. Add Items (stock auto-reserved)
item1 = SalesItem.objects.create(
    sales_order=so,
    item=item,
    quantity=10,
    unit_price=75.00
)

# 3. Check stock availability
available, msg = item1.check_stock_availability()
print(f"Stock available: {available}")

# 4. Ship order (stock auto-reduced)
so.mark_as_shipped()

# 5. Or cancel order (stock auto-released)
# so.cancel_order()
```


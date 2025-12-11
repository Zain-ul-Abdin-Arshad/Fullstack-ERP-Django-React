# Purchase Models Documentation

Complete Django models for managing purchase orders and purchase items with landed cost calculations.

## Models Overview

1. **PurchaseOrder** - Purchase orders from vendors
2. **PurchaseItem** - Individual items within purchase orders with landed cost calculation

## Model Relationships

```
Vendor (1) ──→ (N) PurchaseOrder
PurchaseOrder (1) ──→ (N) PurchaseItem
Item (1) ──→ (N) PurchaseItem
```

## PurchaseOrder Model

### Required Fields (As Requested)

- `vendor` - Foreign key to Vendor (required)
- `order_number` - Unique order number (CharField, required)
- `order_date` - Date of order (DateField, required)
- `total_amount` - Total order amount (DecimalField, auto-calculated)
- `status` - Order status with choices: PENDING, RECEIVED (CharField, required)

### Additional Fields

- `expected_delivery_date` - Expected delivery date
- `received_date` - Actual received date
- `notes` - Additional notes
- `created_at`, `updated_at` - Timestamps

### Status Choices

- `PENDING` - Order is pending
- `RECEIVED` - Order has been received
- `PARTIAL` - Partially received
- `CANCELLED` - Order cancelled

### Methods

- `calculate_total()` - Calculate total from purchase items
- `get_item_count()` - Get number of items in order
- `get_total_quantity()` - Get total quantity
- `mark_as_received()` - Mark order as received

## PurchaseItem Model

### Required Fields (As Requested)

- `purchase_order` - Foreign key to PurchaseOrder (required)
- `item` - Foreign key to Item (required)
- `quantity` - Quantity ordered (IntegerField, required)
- `unit_cost` - Cost per unit (DecimalField, required)
- `freight_cost` - Freight/shipping cost (DecimalField)
- `customs_duty` - Customs duty/tariff (DecimalField)

### Additional Fields

- `other_costs` - Other costs (insurance, handling, etc.)
- `line_total` - Auto-calculated: quantity * unit_cost
- `landed_cost_per_unit` - Auto-calculated landed cost per unit
- `total_landed_cost` - Auto-calculated total landed cost
- `received_quantity` - Quantity actually received

## Landed Cost Calculation

### Formula

**Landed Cost Per Unit** = Unit Cost + (Freight Cost + Customs Duty + Other Costs) / Quantity

**Total Landed Cost** = Landed Cost Per Unit × Quantity

### Example Calculation

```
Item: Car Battery
Quantity: 100 units
Unit Cost: $50.00
Freight Cost: $500.00
Customs Duty: $200.00
Other Costs: $100.00

Additional Costs Per Unit = ($500 + $200 + $100) / 100 = $8.00
Landed Cost Per Unit = $50.00 + $8.00 = $58.00
Total Landed Cost = $58.00 × 100 = $5,800.00
```

### Why Landed Cost Matters

Landed cost includes all expenses to get the product to your warehouse:
- Purchase price
- Freight/shipping
- Customs duties/tariffs
- Insurance
- Handling fees
- Other import costs

This gives you the **true cost** of inventory for accurate pricing and profit calculations.

## Usage Examples

### Creating a Purchase Order

```python
from purchases.models import PurchaseOrder
from vendors.models import Vendor
from datetime import date

# Get vendor
vendor = Vendor.objects.get(name="ABC Suppliers")

# Create purchase order
po = PurchaseOrder.objects.create(
    vendor=vendor,
    order_number="PO-2024-001",
    order_date=date.today(),
    expected_delivery_date=date(2024, 2, 15),
    status="PENDING"
)
```

### Creating Purchase Items

```python
from purchases.models import PurchaseItem
from inventory.models import Item

# Get item
item = Item.objects.get(sku="BATT-12V-001")

# Create purchase item (landed costs auto-calculated)
purchase_item = PurchaseItem.objects.create(
    purchase_order=po,
    item=item,
    quantity=100,
    unit_cost=50.00,
    freight_cost=500.00,
    customs_duty=200.00,
    other_costs=100.00
)

# Landed costs are automatically calculated:
# landed_cost_per_unit = 50.00 + (500 + 200 + 100) / 100 = 58.00
# total_landed_cost = 58.00 * 100 = 5800.00
```

### Getting Cost Breakdown

```python
# Get detailed cost breakdown
breakdown = purchase_item.get_cost_breakdown()
print(breakdown)
# {
#     'unit_cost': Decimal('50.00'),
#     'quantity': 100,
#     'subtotal': Decimal('5000.00'),
#     'freight_cost': Decimal('500.00'),
#     'customs_duty': Decimal('200.00'),
#     'other_costs': Decimal('100.00'),
#     'total_additional_costs': Decimal('800.00'),
#     'landed_cost_per_unit': Decimal('58.00'),
#     'total_landed_cost': Decimal('5800.00'),
# }
```

### Updating Purchase Order Total

```python
# Purchase order total is auto-calculated when items are saved
# Or manually recalculate:
po.calculate_total()
print(po.total_amount)  # Total of all line items
```

### Marking Order as Received

```python
# Mark purchase order as received
po.mark_as_received()
# This updates status to 'RECEIVED' and sets received_date

# Update received quantity for items
purchase_item.received_quantity = 100
purchase_item.save()
```

### Querying Purchase Orders

```python
# Get all pending orders
pending_orders = PurchaseOrder.objects.filter(status='PENDING')

# Get orders by vendor
vendor_orders = PurchaseOrder.objects.filter(vendor=vendor)

# Get orders by date range
from datetime import date, timedelta
start_date = date.today() - timedelta(days=30)
recent_orders = PurchaseOrder.objects.filter(
    order_date__gte=start_date
)

# Get purchase items for an order
items = po.purchase_items.all()
```

### Calculating Total Landed Cost for Order

```python
# Get total landed cost for entire order
total_landed = sum(
    item.total_landed_cost 
    for item in po.purchase_items.all()
)
```

## Auto-Calculations

The models automatically calculate:

1. **Line Total** = quantity × unit_cost
2. **Landed Cost Per Unit** = unit_cost + (freight_cost + customs_duty + other_costs) / quantity
3. **Total Landed Cost** = landed_cost_per_unit × quantity
4. **Purchase Order Total** = sum of all line totals

All calculations happen automatically when you save a PurchaseItem.

## Integration with Inventory

After receiving purchase items, you can:

1. Update stock levels in the inventory module
2. Update item cost_price with landed_cost_per_unit
3. Create stock entries for received items

Example:
```python
from inventory.models import Stock, Warehouse

# After receiving purchase items
warehouse = Warehouse.objects.get(code="WH-001")
stock, created = Stock.objects.get_or_create(
    item=purchase_item.item,
    warehouse=warehouse
)
stock.quantity += purchase_item.received_quantity
stock.average_cost = purchase_item.landed_cost_per_unit
stock.save()
```

## Admin Interface

Both models are registered in Django Admin with:
- Inline editing for purchase items within purchase orders
- Read-only calculated fields (landed costs, totals)
- Search functionality
- Filters for status, dates, vendors
- Autocomplete for vendor and item selection

## Migration Commands

```powershell
# Create migrations
python manage.py makemigrations purchases

# Apply migrations
python manage.py migrate

# Check for issues
python manage.py check
```

## Best Practices

1. **Always set freight_cost, customs_duty, other_costs** - Even if 0, for accurate landed cost
2. **Use landed_cost_per_unit for inventory valuation** - This is the true cost
3. **Update received_quantity** - Track actual received vs ordered
4. **Mark orders as RECEIVED** - Use `mark_as_received()` method
5. **Calculate totals** - Use `calculate_total()` if manually updating items

## Model Features

- **Automatic calculations** - Landed costs calculated on save
- **Status tracking** - Track order status through workflow
- **Quantity tracking** - Track ordered vs received quantities
- **Cost breakdown** - Detailed cost breakdown methods
- **Database indexes** - Optimized for common queries
- **Foreign key protection** - PROTECT on delete for vendor/item

## Next Steps

1. Create serializers for REST API
2. Create viewsets for CRUD operations
3. Add purchase receipt functionality
4. Integrate with inventory stock updates
5. Create purchase order approval workflow
6. Add purchase order reporting


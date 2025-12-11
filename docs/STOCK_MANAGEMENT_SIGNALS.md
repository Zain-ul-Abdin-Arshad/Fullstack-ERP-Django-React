# Stock Management Signals Documentation

Complete guide to automatic stock management using Django signals.

## Overview

The system automatically manages stock levels through Django signals:
1. **Increase Stock** - When purchase items are received
2. **Decrease Stock** - When sales items are shipped/delivered
3. **Stock Validation** - Before allowing sales
4. **Low Stock Alerts** - Automatic alerts per warehouse

## Features

✅ Automatic stock updates  
✅ Stock validation before sales  
✅ Low stock alerts per warehouse  
✅ Weighted average cost calculation  
✅ Transaction safety  
✅ Duplicate alert prevention  

---

## 1. Increase Stock on Purchase

### How It Works

When a `PurchaseItem` is created or updated with `received_quantity > 0` and the `PurchaseOrder` status is `RECEIVED`, stock is automatically increased.

### Signal Flow

```
PurchaseOrder.status = RECEIVED
    ↓
PurchaseItem.received_quantity > 0
    ↓
Signal: update_stock_on_purchase_received()
    ↓
Stock quantity increased
Average cost updated (weighted average)
Low stock alert checked
```

### Code Location

- Signal: `backend/purchases/signals.py`
- Function: `increase_stock_from_purchase_item()`

### Example

```python
from purchases.models import PurchaseOrder, PurchaseItem
from inventory.models import Item, Warehouse

# Create purchase order
po = PurchaseOrder.objects.create(
    vendor=vendor,
    order_number="PO-001",
    order_date=date.today(),
    status="RECEIVED"
)

# Create purchase item with received quantity
item = Item.objects.get(sku="BATT-001")
purchase_item = PurchaseItem.objects.create(
    purchase_order=po,
    item=item,
    quantity=100,
    received_quantity=100,  # Stock will be increased automatically
    unit_cost=50.00,
    freight_cost=500.00,
    customs_duty=200.00
)

# Stock is automatically increased!
# - Stock quantity += 100
# - Average cost updated
# - Low stock alert checked
```

### Warehouse Selection

The system uses the following priority:
1. Purchase order's warehouse (if specified)
2. First active warehouse
3. Creates default warehouse if none exists

---

## 2. Decrease Stock on Sale

### How It Works

When a `SalesItem` is created and the `SalesOrder` status is `SHIPPED` or `DELIVERED`, stock is automatically decreased.

### Signal Flow

```
SalesOrder.status = SHIPPED/DELIVERED
    ↓
SalesItem created/updated
    ↓
Signal: validate_stock_before_sale() (pre_save)
    ↓
Stock validation (sufficient stock?)
    ↓
Signal: decrease_stock_on_sale() (post_save)
    ↓
Stock quantity decreased
Reserved quantity decreased
Low stock alert checked
```

### Code Location

- Signals: `backend/sales/signals.py`
- Functions: `validate_stock_availability()`, `decrease_stock_from_sales_item()`

### Example

```python
from sales.models import SalesOrder, SalesItem
from inventory.models import Item, Warehouse

# Create sales order
warehouse = Warehouse.objects.get(code="WH-001")
so = SalesOrder.objects.create(
    client=client,
    order_number="SO-001",
    order_date=date.today(),
    warehouse=warehouse,
    status="SHIPPED"  # Stock will be decreased automatically
)

# Create sales item
item = Item.objects.get(sku="BATT-001")
sales_item = SalesItem.objects.create(
    sales_order=so,
    item=item,
    quantity=10,
    unit_price=75.00
)

# Stock is automatically decreased!
# - Stock validation performed first
# - Stock quantity -= 10
# - Reserved quantity -= 10 (if reserved)
# - Low stock alert checked
```

### Stock Validation

Before decreasing stock, the system validates:
- Sufficient available stock exists
- Stock is available in the specified warehouse
- Raises `ValidationError` if insufficient stock

---

## 3. Stock Validation

### Pre-Save Validation

Before creating or updating a `SalesItem`, the system validates stock availability.

### Validation Rules

1. **For PENDING/CONFIRMED orders**: Validates available stock (quantity - reserved)
2. **For SHIPPED/DELIVERED orders**: Validates and decreases stock
3. **Warehouse-specific**: Validates stock in the order's warehouse
4. **Multi-warehouse**: Falls back to total stock if no warehouse specified

### Error Handling

```python
# Insufficient stock raises ValidationError
try:
    sales_item = SalesItem.objects.create(
        sales_order=so,
        item=item,
        quantity=1000  # More than available
    )
except ValidationError as e:
    print(f"Error: {e}")
    # Error: Insufficient stock: Only 50 units available...
```

### Manual Validation

You can also validate stock manually:

```python
from sales.models import SalesItem

sales_item = SalesItem(...)
is_available, message = sales_item.check_stock_availability()
if not is_available:
    print(f"Error: {message}")
```

---

## 4. Low Stock Alerts

### How It Works

When stock falls below the minimum quantity (`quantity <= min_quantity`), an alert is automatically created.

### Alert Model

The `StockAlert` model tracks:
- Current stock quantity
- Minimum required quantity
- Warehouse and item information
- Alert status (PENDING, ACKNOWLEDGED, RESOLVED)
- Timestamps

### Alert Creation

Alerts are automatically created when:
- Stock is decreased and falls below minimum
- Stock is updated and falls below minimum
- Purchase items are received but stock still low

### Code Location

- Model: `backend/inventory/models.py` - `StockAlert`
- Function: `check_and_send_low_stock_alert()`

### Example

```python
from inventory.models import Stock, StockAlert

# Get stock entry
stock = Stock.objects.get(item=item, warehouse=warehouse)

# Set minimum quantity
stock.min_quantity = 20
stock.quantity = 15  # Below minimum
stock.save()

# Alert is automatically created!
alert = StockAlert.objects.filter(
    stock=stock,
    alert_status='PENDING'
).first()

print(alert.message)
# "Low stock alert for Battery in Main Warehouse. Current quantity: 15, Minimum required: 20"
```

### Querying Alerts

```python
# Get all pending alerts
pending_alerts = StockAlert.objects.filter(alert_status='PENDING')

# Get alerts for specific warehouse
warehouse_alerts = StockAlert.objects.filter(
    warehouse=warehouse,
    alert_status='PENDING'
)

# Get alerts for specific item
item_alerts = StockAlert.objects.filter(
    item=item,
    alert_status='PENDING'
)
```

### Managing Alerts

```python
# Acknowledge alert
alert.acknowledge()
# Sets status to ACKNOWLEDGED and acknowledged_at timestamp

# Resolve alert
alert.resolve()
# Sets status to RESOLVED and resolved_at timestamp

# Check if resolved
if alert.is_resolved():
    print("Stock is now above minimum")
```

### Alert Notifications

The `send_stock_alert_notification()` function can be extended to send:
- Email notifications
- SMS alerts
- Push notifications
- Slack/Discord messages
- etc.

Currently, it logs the alert. You can extend it:

```python
# In inventory/models.py - send_stock_alert_notification()
def send_stock_alert_notification(alert):
    # Send email
    from django.core.mail import send_mail
    send_mail(
        subject=f"Low Stock Alert: {alert.item.name}",
        message=alert.message,
        from_email='alerts@erp.com',
        recipient_list=[alert.warehouse.manager_email],
    )
    
    # Send SMS (using Twilio, etc.)
    # Send Slack notification
    # etc.
```

---

## Signal Registration

Signals are automatically registered when apps are loaded.

### App Configuration

**Purchases App** (`backend/purchases/apps.py`):
```python
class PurchasesConfig(AppConfig):
    def ready(self):
        import purchases.signals
```

**Sales App** (`backend/sales/apps.py`):
```python
class SalesConfig(AppConfig):
    def ready(self):
        import sales.signals
```

### Ensure Apps Are Configured

Make sure `settings.py` uses the app config:

```python
INSTALLED_APPS = [
    # ...
    'purchases.apps.PurchasesConfig',  # Not just 'purchases'
    'sales.apps.SalesConfig',  # Not just 'sales'
    # ...
]
```

---

## Transaction Safety

All stock operations use database transactions to ensure data consistency:

```python
with transaction.atomic():
    # Stock operations
    stock.quantity += quantity
    stock.average_cost = new_average
    stock.save()
```

This ensures:
- Atomic operations (all or nothing)
- No race conditions
- Data consistency

---

## Average Cost Calculation

When stock is increased from purchases, the average cost is calculated using weighted average:

```python
# Weighted Average Formula
new_average = (old_quantity * old_cost + new_quantity * new_cost) / total_quantity
```

Example:
- Current: 50 units @ $45/unit
- Received: 100 units @ $50/unit
- New Average: (50*45 + 100*50) / 150 = $48.33/unit

---

## Testing

### Test Stock Increase

```python
# Create purchase order
po = PurchaseOrder.objects.create(..., status="RECEIVED")
purchase_item = PurchaseItem.objects.create(
    purchase_order=po,
    item=item,
    received_quantity=100,
    ...
)

# Verify stock increased
stock = Stock.objects.get(item=item, warehouse=warehouse)
assert stock.quantity == 100
```

### Test Stock Decrease

```python
# Create sales order
so = SalesOrder.objects.create(..., status="SHIPPED", warehouse=warehouse)
sales_item = SalesItem.objects.create(
    sales_order=so,
    item=item,
    quantity=10,
    ...
)

# Verify stock decreased
stock.refresh_from_db()
assert stock.quantity == 90  # 100 - 10
```

### Test Stock Validation

```python
# Try to sell more than available
try:
    sales_item = SalesItem.objects.create(
        sales_order=so,
        item=item,
        quantity=1000,  # More than available
        ...
    )
except ValidationError:
    print("Validation worked correctly!")
```

### Test Low Stock Alert

```python
# Set stock below minimum
stock.min_quantity = 20
stock.quantity = 15
stock.save()

# Verify alert created
alert = StockAlert.objects.filter(stock=stock, alert_status='PENDING').first()
assert alert is not None
assert alert.current_quantity == 15
```

---

## Troubleshooting

### Signals Not Firing

1. Check app configuration in `apps.py`
2. Ensure apps are registered in `INSTALLED_APPS` with config class
3. Restart Django server

### Stock Not Updating

1. Check purchase order status is `RECEIVED`
2. Check `received_quantity > 0`
3. Check warehouse exists
4. Check signals are imported

### Validation Errors

1. Check stock availability before creating sales items
2. Ensure warehouse is specified in sales order
3. Check `min_quantity` is set correctly

### Alerts Not Creating

1. Check `min_quantity` is set on stock
2. Verify stock quantity is below minimum
3. Check for existing pending alerts (prevents duplicates)

---

## Migration Commands

```powershell
# Create migrations for StockAlert model
python manage.py makemigrations inventory

# Apply migrations
python manage.py migrate

# Verify
python manage.py check
```

---

## Next Steps

1. **Extend notifications**: Add email/SMS alerts
2. **Add alert preferences**: Per-user alert settings
3. **Add alert thresholds**: Multiple alert levels (low, critical, etc.)
4. **Add reporting**: Alert history and statistics
5. **Add auto-reorder**: Automatic purchase order creation on low stock


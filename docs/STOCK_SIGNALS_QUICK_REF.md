# Stock Management Signals - Quick Reference

## Automatic Stock Operations

### ✅ Stock Increase (Purchase)
- **Trigger**: PurchaseItem created/updated with `received_quantity > 0` AND PurchaseOrder status = `RECEIVED`
- **Action**: Stock quantity increased, average cost updated
- **File**: `backend/purchases/signals.py`

### ✅ Stock Decrease (Sales)
- **Trigger**: SalesItem created/updated AND SalesOrder status = `SHIPPED` or `DELIVERED`
- **Action**: Stock quantity decreased, reserved quantity decreased
- **File**: `backend/sales/signals.py`

### ✅ Stock Validation
- **Trigger**: SalesItem pre_save
- **Action**: Validates sufficient stock before allowing sale
- **Raises**: ValidationError if insufficient stock

### ✅ Low Stock Alerts
- **Trigger**: Stock falls below `min_quantity`
- **Action**: Creates StockAlert record
- **Model**: `StockAlert` in `backend/inventory/models.py`

## Quick Examples

### Increase Stock

```python
# Purchase order received
po = PurchaseOrder.objects.create(..., status="RECEIVED")
PurchaseItem.objects.create(
    purchase_order=po,
    item=item,
    received_quantity=100,  # Stock auto-increased!
    ...
)
```

### Decrease Stock

```python
# Sales order shipped
so = SalesOrder.objects.create(..., status="SHIPPED", warehouse=warehouse)
SalesItem.objects.create(
    sales_order=so,
    item=item,
    quantity=10,  # Stock validated & auto-decreased!
    ...
)
```

### Low Stock Alert

```python
# Stock below minimum
stock.min_quantity = 20
stock.quantity = 15
stock.save()  # Alert auto-created!
```

## Files Created

- `backend/purchases/signals.py` - Purchase stock signals
- `backend/sales/signals.py` - Sales stock signals
- `backend/purchases/apps.py` - Signal registration
- `backend/sales/apps.py` - Signal registration
- `backend/inventory/models.py` - StockAlert model added

## Setup Required

1. **Update INSTALLED_APPS** in `settings.py`:
```python
INSTALLED_APPS = [
    # ...
    'purchases.apps.PurchasesConfig',  # Use config class
    'sales.apps.SalesConfig',  # Use config class
    # ...
]
```

2. **Run migrations**:
```powershell
python manage.py makemigrations inventory
python manage.py migrate
```

3. **Restart server** to load signals

## Alert Management

```python
# Get pending alerts
alerts = StockAlert.objects.filter(alert_status='PENDING')

# Acknowledge
alert.acknowledge()

# Resolve
alert.resolve()
```

## Validation

Stock validation happens automatically before sales. To check manually:

```python
is_available, message = sales_item.check_stock_availability()
```


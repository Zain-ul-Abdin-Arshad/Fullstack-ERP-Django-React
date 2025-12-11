# Sales Models Documentation

Complete Django models for managing sales orders and sales items with automatic stock reduction logic.

## Models Overview

1. **SalesOrder** - Sales orders from clients
2. **SalesItem** - Individual items within sales orders with stock reduction

## Model Relationships

```
Client (1) ──→ (N) SalesOrder
SalesOrder (1) ──→ (N) SalesItem
Item (1) ──→ (N) SalesItem
Warehouse (1) ──→ (N) SalesOrder
```

## SalesOrder Model

### Required Fields (As Requested)

- `client` - Foreign key to Client (required)
- `order_number` - Unique order number (CharField, required)
- `order_date` - Date of order (DateField, required)
- `total_amount` - Total order amount (DecimalField, auto-calculated)
- `status` - Order status with choices: PENDING, SHIPPED, DELIVERED (CharField, required)

### Additional Fields

- `expected_delivery_date` - Expected delivery date
- `shipped_date` - Actual shipped date
- `delivered_date` - Actual delivered date
- `discount_amount` - Total discount applied
- `warehouse` - Warehouse from which items ship
- `notes` - Additional notes
- `created_at`, `updated_at` - Timestamps

### Status Choices

- `PENDING` - Order is pending (stock is reserved)
- `CONFIRMED` - Order is confirmed
- `SHIPPED` - Order has been shipped (stock is reduced)
- `DELIVERED` - Order has been delivered (stock is reduced)
- `CANCELLED` - Order cancelled (reserved stock is released)

### Methods

- `calculate_total()` - Calculate total from sales items
- `get_item_count()` - Get number of items in order
- `get_total_quantity()` - Get total quantity
- `reserve_stock()` - Reserve stock for pending orders
- `release_reserved_stock()` - Release reserved stock
- `reduce_stock()` - Reduce stock when shipped/delivered
- `mark_as_shipped()` - Mark order as shipped and reduce stock
- `mark_as_delivered()` - Mark order as delivered
- `cancel_order()` - Cancel order and release stock

## SalesItem Model

### Required Fields (As Requested)

- `sales_order` - Foreign key to SalesOrder (required)
- `item` - Foreign key to Item (required)
- `quantity` - Quantity ordered (IntegerField, required)
- `unit_price` - Selling price per unit (DecimalField, required)

### Additional Fields

- `discount_percentage` - Discount percentage for line item
- `line_total` - Auto-calculated: (quantity × unit_price) - discount
- `shipped_quantity` - Quantity actually shipped

## Stock Reduction Logic

### How It Works

The stock reduction logic automatically manages inventory based on order status:

#### 1. **PENDING Status** (Stock Reservation)
- When order status is `PENDING`, stock is **reserved**
- `reserved_quantity` in Stock model is **increased**
- `available_quantity` is automatically **decreased**
- Stock is not physically reduced yet

#### 2. **SHIPPED/DELIVERED Status** (Stock Reduction)
- When order status changes to `SHIPPED` or `DELIVERED`:
  - `reserved_quantity` is **decreased**
  - `quantity` (actual stock) is **decreased**
  - Stock is physically reduced

#### 3. **CANCELLED Status** (Stock Release)
- When order is cancelled:
  - `reserved_quantity` is **decreased**
  - Stock reservation is released
  - No physical stock reduction

### Stock Flow Diagram

```
Order Created (PENDING)
    ↓
Stock Reserved (reserved_quantity ↑, available_quantity ↓)
    ↓
Order Shipped/Delivered
    ↓
Stock Reduced (quantity ↓, reserved_quantity ↓)
    ↓
Stock Updated
```

### Warehouse Selection

Stock reduction uses the following priority:
1. Order's specified warehouse (`sales_order.warehouse`)
2. First available stock for the item
3. Raises error if no stock found

## Usage Examples

### Creating a Sales Order

```python
from sales.models import SalesOrder, SalesItem
from clients.models import Client
from inventory.models import Warehouse
from datetime import date

# Get client and warehouse
client = Client.objects.get(name="ABC Auto Shop")
warehouse = Warehouse.objects.get(code="WH-001")

# Create sales order
so = SalesOrder.objects.create(
    client=client,
    order_number="SO-2024-001",
    order_date=date.today(),
    warehouse=warehouse,
    status="PENDING"
)
# Stock is automatically reserved when status is PENDING
```

### Creating Sales Items

```python
from inventory.models import Item

# Get item
item = Item.objects.get(sku="BATT-12V-001")

# Create sales item
sales_item = SalesItem.objects.create(
    sales_order=so,
    item=item,
    quantity=10,
    unit_price=75.00,
    discount_percentage=5.00  # 5% discount
)

# Line total is automatically calculated:
# (10 × 75.00) - (750.00 × 0.05) = 712.50
# Stock is automatically reserved
```

### Checking Stock Availability

```python
# Check if stock is available before creating order
is_available, message = sales_item.check_stock_availability()
if not is_available:
    print(f"Error: {message}")
```

### Shipping an Order (Stock Reduction)

```python
# Mark order as shipped - stock is automatically reduced
so.mark_as_shipped()
# This:
# - Sets status to SHIPPED
# - Sets shipped_date
# - Reduces stock quantity
# - Reduces reserved_quantity
```

### Delivering an Order

```python
# Mark order as delivered
so.mark_as_delivered()
# This:
# - Sets status to DELIVERED
# - Sets delivered_date
# - Reduces stock if not already shipped
```

### Cancelling an Order (Release Stock)

```python
# Cancel order - reserved stock is released
so.cancel_order()
# This:
# - Sets status to CANCELLED
# - Releases reserved stock
# - Does NOT reduce actual stock
```

### Manual Stock Operations

```python
# Manually reserve stock
so.reserve_stock()

# Manually release reserved stock
so.release_reserved_stock()

# Manually reduce stock
so.reduce_stock()
```

## Stock Impact Examples

### Example 1: Order Lifecycle

```python
# Initial stock
stock = Stock.objects.get(item=item, warehouse=warehouse)
print(f"Initial: quantity={stock.quantity}, reserved={stock.reserved_quantity}")
# Output: Initial: quantity=100, reserved=0

# Create pending order (quantity=10)
so = SalesOrder.objects.create(..., status="PENDING")
SalesItem.objects.create(sales_order=so, item=item, quantity=10, ...)

# After order creation
stock.refresh_from_db()
print(f"After PENDING: quantity={stock.quantity}, reserved={stock.reserved_quantity}")
# Output: After PENDING: quantity=100, reserved=10
#         available_quantity = 90 (auto-calculated)

# Ship order
so.mark_as_shipped()

# After shipping
stock.refresh_from_db()
print(f"After SHIPPED: quantity={stock.quantity}, reserved={stock.reserved_quantity}")
# Output: After SHIPPED: quantity=90, reserved=0
#         available_quantity = 90
```

### Example 2: Cancelled Order

```python
# Create pending order
so = SalesOrder.objects.create(..., status="PENDING")
SalesItem.objects.create(sales_order=so, item=item, quantity=10, ...)
# Stock: quantity=100, reserved=10

# Cancel order
so.cancel_order()

# After cancellation
stock.refresh_from_db()
print(f"After CANCELLED: quantity={stock.quantity}, reserved={stock.reserved_quantity}")
# Output: After CANCELLED: quantity=100, reserved=0
#         Stock is released, no physical reduction
```

## Profit Calculations

### Calculate Profit Margin

```python
# Get profit margin for a sales item
margin = sales_item.get_profit_margin()
print(f"Profit margin: {margin}%")

# Get total profit amount
profit = sales_item.get_profit_amount()
print(f"Total profit: ${profit}")
```

## Querying Sales Orders

```python
# Get all pending orders
pending_orders = SalesOrder.objects.filter(status='PENDING')

# Get orders by client
client_orders = SalesOrder.objects.filter(client=client)

# Get orders by date range
from datetime import date, timedelta
start_date = date.today() - timedelta(days=30)
recent_orders = SalesOrder.objects.filter(order_date__gte=start_date)

# Get shipped orders
shipped_orders = SalesOrder.objects.filter(status='SHIPPED')

# Get sales items for an order
items = so.sales_items.all()
```

## Admin Interface

Both models are registered in Django Admin with:
- Inline editing for sales items within sales orders
- Read-only calculated fields (line_total)
- Search functionality
- Filters for status, dates, clients, warehouses
- Admin actions: mark_as_shipped, mark_as_delivered, cancel_orders
- Autocomplete for client, warehouse, and item selection

## Migration Commands

```powershell
# Create migrations
python manage.py makemigrations sales

# Apply migrations
python manage.py migrate

# Check for issues
python manage.py check
```

## Best Practices

1. **Always check stock availability** - Use `check_stock_availability()` before creating orders
2. **Set warehouse** - Specify warehouse for accurate stock tracking
3. **Use status methods** - Use `mark_as_shipped()` and `mark_as_delivered()` instead of manual status updates
4. **Handle cancellations** - Use `cancel_order()` to properly release stock
5. **Monitor reserved stock** - Track reserved_quantity to prevent over-selling

## Stock Reduction Flow

```
1. Order Created (PENDING)
   → Stock Reserved (reserved_quantity ↑)

2. Order Shipped/Delivered
   → Stock Reduced (quantity ↓, reserved_quantity ↓)

3. Order Cancelled
   → Stock Released (reserved_quantity ↓)
```

## Error Handling

The models include error handling for:
- Insufficient stock (checked via `check_stock_availability()`)
- Missing stock records
- Negative quantities (prevented by validators)
- Stock not found scenarios

## Integration with Inventory

The Sales models integrate seamlessly with:
- **Stock model** - Automatic stock updates
- **Item model** - Product information and pricing
- **Warehouse model** - Multi-warehouse support
- **Client model** - Customer information

## Next Steps

1. Create serializers for REST API
2. Create viewsets for CRUD operations
3. Add sales invoice generation
4. Create sales reporting and analytics
5. Add payment tracking
6. Implement sales return functionality


# Inventory Models Documentation

Complete Django models for the Inventory module with relationships, validations, and helper methods.

## Models Overview

1. **Category** - Product categories with hierarchical support
2. **Warehouse** - Physical storage locations
3. **Item** - Products/spare parts with full details
4. **Stock** - Inventory levels per item per warehouse

## Model Relationships

```
Category (1) ──→ (N) Item
Vendor (1) ──→ (N) Item
Item (1) ──→ (N) Stock
Warehouse (1) ──→ (N) Stock
```

## Model Details

### Category Model

**Fields:**
- `name` - Category name (unique)
- `code` - Short category code (unique)
- `description` - Detailed description
- `parent` - Self-referential FK for hierarchical categories
- `is_active` - Active status flag
- `created_at`, `updated_at` - Timestamps

**Features:**
- Hierarchical category structure
- Unique name and code constraints
- Indexes on name, code, and is_active
- `get_full_path()` method for category hierarchy

### Warehouse Model

**Fields:**
- `name` - Warehouse name (unique)
- `code` - Short warehouse code (unique)
- `address`, `city`, `state`, `country`, `postal_code` - Location details
- `phone`, `email` - Contact information
- `manager_name` - Warehouse manager
- `is_active` - Active status flag
- `capacity` - Storage capacity
- `created_at`, `updated_at` - Timestamps

**Features:**
- Complete address information
- Contact details
- Capacity tracking
- Indexes for performance

### Item Model

**Fields:**

**Basic Information:**
- `name` - Item name
- `sku` - Stock Keeping Unit (unique)
- `barcode` - Barcode/UPC (unique, optional)
- `description` - Detailed description

**Relationships:**
- `category` - FK to Category (PROTECT on delete)
- `vendor` - FK to Vendor (PROTECT on delete, optional)

**Pricing:**
- `cost_price` - Purchase cost per unit
- `selling_price` - Retail selling price

**Inventory:**
- `unit` - Unit of measurement (choices: PCS, BOX, PKG, SET, PAIR, KG, L, M)
- `reorder_level` - Minimum stock level for reordering
- `reorder_quantity` - Standard reorder quantity

**Physical Attributes:**
- `weight` - Weight per unit (kg)
- `dimensions` - Dimensions (L x W x H)

**Vehicle Compatibility (for car spare parts):**
- `vehicle_make` - Compatible vehicle manufacturer
- `vehicle_model` - Compatible vehicle model
- `vehicle_year_from` - Earliest compatible year
- `vehicle_year_to` - Latest compatible year

**Status:**
- `is_active` - Active status flag
- `is_trackable` - Whether to track stock levels
- `allow_backorder` - Allow backorders when out of stock
- `image` - Item image

**Timestamps:**
- `created_at`, `updated_at` - Auto timestamps

**Methods:**
- `get_total_stock()` - Calculate total stock across all warehouses
- `is_low_stock()` - Check if below reorder level
- `get_margin()` - Calculate profit margin percentage

### Stock Model

**Fields:**
- `item` - FK to Item (CASCADE on delete)
- `warehouse` - FK to Warehouse (CASCADE on delete)
- `quantity` - Current stock quantity
- `reserved_quantity` - Quantity reserved for pending orders
- `available_quantity` - Auto-calculated (quantity - reserved)
- `min_quantity` - Minimum stock level for this warehouse
- `max_quantity` - Maximum stock level (optional)
- `average_cost` - Average cost per unit
- `last_restocked` - Last restocking timestamp
- `created_at`, `updated_at` - Timestamps

**Constraints:**
- Unique together: (item, warehouse)

**Methods:**
- `is_low_stock()` - Check if below minimum level
- `is_out_of_stock()` - Check if stock is zero
- `can_fulfill_order(quantity)` - Check if can fulfill order

**Auto-calculation:**
- `available_quantity` is automatically calculated on save

## Usage Examples

### Creating a Category

```python
from inventory.models import Category

# Create parent category
electronics = Category.objects.create(
    name="Electronics",
    code="ELEC",
    description="Electronic components"
)

# Create subcategory
batteries = Category.objects.create(
    name="Batteries",
    code="BATT",
    parent=electronics
)
```

### Creating a Warehouse

```python
from inventory.models import Warehouse

warehouse = Warehouse.objects.create(
    name="Main Warehouse",
    code="WH-001",
    address="123 Industrial St",
    city="New York",
    state="NY",
    country="USA",
    postal_code="10001",
    phone="+1-555-0100",
    manager_name="John Doe"
)
```

### Creating an Item

```python
from inventory.models import Item, Category
from vendors.models import Vendor

# Get category and vendor
category = Category.objects.get(code="BATT")
vendor = Vendor.objects.get(name="ABC Suppliers")

# Create item
item = Item.objects.create(
    name="12V Car Battery",
    sku="BATT-12V-001",
    barcode="1234567890123",
    category=category,
    vendor=vendor,
    cost_price=50.00,
    selling_price=75.00,
    unit="PCS",
    reorder_level=10,
    reorder_quantity=50,
    vehicle_make="Toyota",
    vehicle_model="Camry",
    vehicle_year_from=2015,
    vehicle_year_to=2020
)
```

### Creating Stock

```python
from inventory.models import Stock, Item, Warehouse

# Get item and warehouse
item = Item.objects.get(sku="BATT-12V-001")
warehouse = Warehouse.objects.get(code="WH-001")

# Create stock entry
stock = Stock.objects.create(
    item=item,
    warehouse=warehouse,
    quantity=100,
    reserved_quantity=5,
    min_quantity=10,
    max_quantity=200,
    average_cost=50.00
)

# Available quantity is auto-calculated: 100 - 5 = 95
print(stock.available_quantity)  # 95
```

### Querying Stock Levels

```python
# Get total stock for an item
item = Item.objects.get(sku="BATT-12V-001")
total_stock = item.get_total_stock()

# Check if item is low stock
if item.is_low_stock():
    print(f"Item {item.name} needs reordering!")

# Get all low stock items
low_stock_items = Item.objects.filter(
    stock_items__quantity__lte=models.F('reorder_level')
).distinct()

# Get stock for specific warehouse
warehouse_stock = Stock.objects.filter(warehouse=warehouse)
```

## Database Migrations

After creating the models, run migrations:

```powershell
# Create migrations
python manage.py makemigrations inventory
python manage.py makemigrations vendors

# Apply migrations
python manage.py migrate
```

## Admin Interface

All models are registered in Django admin with:
- List displays with key fields
- Search functionality
- Filters for common queries
- Inline editing where appropriate
- Organized fieldsets for Item model

Access admin at: `http://localhost:8000/admin/`

## Indexes and Performance

Models include database indexes on:
- Frequently queried fields (name, code, sku, barcode)
- Foreign key relationships
- Filter fields (is_active, category, vendor)
- Composite indexes for common query patterns

## Validation

Models include:
- `MinValueValidator` for numeric fields (prices, quantities)
- `MaxValueValidator` for year fields
- Unique constraints on SKU, barcode, category code, warehouse code
- Unique together constraint on Stock (item, warehouse)

## Next Steps

1. Create serializers for REST API
2. Create viewsets for CRUD operations
3. Add stock movement tracking
4. Implement reorder alerts
5. Add inventory valuation methods
6. Create reporting queries


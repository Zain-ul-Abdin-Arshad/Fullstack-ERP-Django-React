# Inventory Models - Quick Reference

## Models Created

✅ **Category** - Product categories with parent-child relationships  
✅ **Warehouse** - Physical storage locations  
✅ **Item** - Products/spare parts with full details  
✅ **Stock** - Inventory levels per item per warehouse  

## Key Relationships

```
Category ──→ Item (Many-to-One)
Vendor ──→ Item (Many-to-One, optional)
Item ──→ Stock (One-to-Many)
Warehouse ──→ Stock (One-to-Many)
```

## Quick Setup Commands

```powershell
# Navigate to backend
cd D:\ERP_SYSTEM\backend
.\venv\Scripts\Activate.ps1

# Create migrations
python manage.py makemigrations inventory
python manage.py makemigrations vendors

# Apply migrations
python manage.py migrate

# Verify
python manage.py check
```

## Model Fields Summary

### Category
- `name`, `code` (unique)
- `parent` (self-reference for hierarchy)
- `is_active`, timestamps

### Warehouse
- `name`, `code` (unique)
- Address fields (address, city, state, country, postal_code)
- Contact info (phone, email, manager_name)
- `capacity`, `is_active`, timestamps

### Item
- `name`, `sku` (unique), `barcode` (unique, optional)
- `category` (FK), `vendor` (FK, optional)
- `cost_price`, `selling_price`
- `unit` (choices: PCS, BOX, PKG, SET, PAIR, KG, L, M)
- `reorder_level`, `reorder_quantity`
- Vehicle compatibility fields
- `is_active`, `is_trackable`, `allow_backorder`
- `image`, timestamps

### Stock
- `item` (FK), `warehouse` (FK)
- `quantity`, `reserved_quantity`, `available_quantity` (auto-calculated)
- `min_quantity`, `max_quantity`
- `average_cost`, `last_restocked`
- Unique together: (item, warehouse)
- Timestamps

## Helper Methods

### Item Methods
- `get_total_stock()` - Total stock across all warehouses
- `is_low_stock()` - Check if below reorder level
- `get_margin()` - Calculate profit margin %

### Stock Methods
- `is_low_stock()` - Check if below minimum
- `is_out_of_stock()` - Check if quantity is 0
- `can_fulfill_order(qty)` - Check if can fulfill order

### Category Methods
- `get_full_path()` - Full category path with parents

## Admin Interface

All models registered in Django Admin with:
- List displays
- Search functionality
- Filters
- Inline editing

Access: `http://localhost:8000/admin/`

## Example Usage

```python
# Create category
cat = Category.objects.create(name="Batteries", code="BATT")

# Create warehouse
wh = Warehouse.objects.create(
    name="Main WH", code="WH-001",
    address="123 St", city="NYC"
)

# Create item
item = Item.objects.create(
    name="12V Battery", sku="BATT-001",
    category=cat, cost_price=50, selling_price=75
)

# Create stock
stock = Stock.objects.create(
    item=item, warehouse=wh,
    quantity=100, min_quantity=10
)
# available_quantity auto-calculated: 100
```

## Files Created

- `backend/inventory/models.py` - All inventory models
- `backend/inventory/admin.py` - Admin configuration
- `backend/vendors/models.py` - Basic Vendor model (for FK)
- `backend/vendors/admin.py` - Vendor admin config

## Next Steps

1. Run migrations
2. Create superuser: `python manage.py createsuperuser`
3. Access admin and test models
4. Create serializers for API
5. Create viewsets for REST API


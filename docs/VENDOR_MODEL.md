# Vendor Model Documentation

Complete Django model for managing vendors/suppliers in the ERP system.

## Model Overview

The **Vendor** model represents suppliers and vendors that provide products to the business.

## Required Fields

- `name` - Vendor name (unique, required)
- `country` - Country where vendor is located (required)
- `contact_number` - Primary contact phone number (required)
- `email` - Primary email address (required, validated)
- `created_at` - Auto-generated timestamp when record is created

## All Fields

### Basic Information
- `name` - Vendor company name (CharField, max 200, unique)
- `code` - Short vendor code (CharField, max 50, unique, optional)

### Contact Information
- `contact_number` - Primary phone number (CharField, max 20, required)
- `email` - Primary email address (EmailField, required, validated)
- `website` - Company website URL (URLField, optional)

### Address Information
- `address` - Street address (TextField, optional)
- `city` - City (CharField, max 100, optional)
- `state` - State/Province (CharField, max 100, optional)
- `postal_code` - Postal/ZIP code (CharField, max 20, optional)
- `country` - Country (CharField, max 100, required)

### Business Details
- `tax_id` - Tax identification number (CharField, max 50, optional)
- `payment_terms` - Standard payment terms (CharField, max 100, optional)
- `credit_limit` - Maximum credit limit (DecimalField, optional)

### Status & Notes
- `is_active` - Active status flag (BooleanField, default True)
- `notes` - Additional notes (TextField, optional)

### Timestamps
- `created_at` - Creation timestamp (DateTimeField, auto_now_add)
- `updated_at` - Last update timestamp (DateTimeField, auto_now)

## Usage Examples

### Creating a Vendor

```python
from vendors.models import Vendor

# Basic vendor with required fields
vendor = Vendor.objects.create(
    name="ABC Auto Parts Ltd",
    country="USA",
    contact_number="+1-555-0123",
    email="contact@abcautoparts.com"
)

# Vendor with complete information
vendor = Vendor.objects.create(
    name="XYZ Suppliers Inc",
    code="VND-001",
    country="Germany",
    contact_number="+49-30-12345678",
    email="info@xyzsuppliers.de",
    address="123 Industrial Street",
    city="Berlin",
    state="Berlin",
    postal_code="10115",
    website="https://www.xyzsuppliers.de",
    tax_id="DE123456789",
    payment_terms="Net 30",
    credit_limit=50000.00,
    notes="Preferred supplier for European parts"
)
```

### Querying Vendors

```python
# Get all active vendors
active_vendors = Vendor.objects.filter(is_active=True)

# Get vendors by country
us_vendors = Vendor.objects.filter(country="USA")

# Search vendors by name or email
vendors = Vendor.objects.filter(
    models.Q(name__icontains="Auto") | 
    models.Q(email__icontains="parts")
)

# Get vendor by code
vendor = Vendor.objects.get(code="VND-001")
```

### Using Helper Methods

```python
vendor = Vendor.objects.get(name="ABC Auto Parts Ltd")

# Get formatted full address
full_address = vendor.get_full_address()
# Returns: "123 Industrial Street, Berlin, Berlin, 10115, Germany"
```

## Model Features

### Database Indexes

Indexes are created on:
- `name` - For fast name lookups
- `code` - For fast code lookups
- `country` - For country-based filtering
- `is_active` - For active/inactive filtering
- `email` - For email lookups

### Validations

- Email validation using Django's EmailValidator
- Unique constraints on `name` and `code`
- Required fields: `name`, `country`, `contact_number`, `email`

### Admin Interface

The model is registered in Django Admin with:
- List display showing key fields
- Search functionality (name, code, email, contact_number, country, city, tax_id)
- Filters (is_active, country, created_at)
- Organized fieldsets for better UX
- Read-only timestamp fields

## Relationships

The Vendor model is referenced by:
- **Item** model (inventory app) - Many items can belong to one vendor
  ```python
  item.vendor  # ForeignKey relationship
  ```

## Migration Commands

```powershell
# Create migrations
python manage.py makemigrations vendors

# Apply migrations
python manage.py migrate

# Check for issues
python manage.py check
```

## Admin Access

Access the vendor admin interface at:
`http://localhost:8000/admin/vendors/vendor/`

## Model Meta Options

- **Verbose Name**: "Vendor"
- **Verbose Name Plural**: "Vendors"
- **Default Ordering**: By name (alphabetical)
- **Indexes**: Optimized for common queries

## Best Practices

1. **Always use unique codes** - Set vendor codes for easy identification
2. **Keep contact info updated** - Maintain current email and phone numbers
3. **Set credit limits** - Important for purchase order management
4. **Use payment terms** - Standardize payment terms for consistency
5. **Mark inactive vendors** - Use `is_active=False` instead of deleting

## Integration with Other Modules

- **Inventory**: Items reference vendors via ForeignKey
- **Purchases**: Purchase orders will reference vendors
- **Reports**: Vendor performance can be tracked

## Next Steps

1. Create VendorContact model for multiple contacts per vendor
2. Add vendor performance tracking
3. Create purchase history relationship
4. Add vendor rating/review system
5. Implement vendor payment tracking


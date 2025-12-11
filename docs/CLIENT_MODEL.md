# Client Model Documentation

Complete Django model for managing clients/customers in the ERP system.

## Model Overview

The **Client** model represents customers and clients that purchase products from the business.

## Required Fields (As Requested)

✅ **All requested fields are present:**

- `name` - Client name (CharField, unique, required)
- `country` - Country where client is located (CharField, required)
- `city` - City where client is located (CharField, required)
- `contact_number` - Primary contact phone number (CharField, required)
- `email` - Primary email address (EmailField, validated, required)
- `created_at` - Auto-generated timestamp when record is created (DateTimeField)

## Complete Model Code

The model is located at: `backend/clients/models.py`

### Required Fields Section

```python
class Client(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name=_("Client Name"),
        help_text=_("Name of the client/customer company or individual")
    )
    country = models.CharField(
        max_length=100,
        verbose_name=_("Country"),
        help_text=_("Country where the client is located")
    )
    city = models.CharField(
        max_length=100,
        verbose_name=_("City"),
        help_text=_("City where the client is located")
    )
    contact_number = models.CharField(
        max_length=20,
        verbose_name=_("Contact Number"),
        help_text=_("Primary contact phone number")
    )
    email = models.EmailField(
        verbose_name=_("Email Address"),
        help_text=_("Primary email address"),
        validators=[EmailValidator()]
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )
```

## Additional Fields (Bonus)

The model also includes additional useful fields for an ERP system:

- `code` - Client code for easy identification
- `address`, `state`, `postal_code` - Complete address information
- `website` - Company website
- `tax_id` - Tax identification number
- `payment_terms` - Payment terms (Net 30, COD, etc.)
- `credit_limit` - Maximum credit limit
- `discount_percentage` - Standard discount percentage
- `client_type` - Type of client (Individual, Retailer, Wholesaler, etc.)
- `is_active` - Active status flag
- `notes` - Additional notes
- `updated_at` - Last update timestamp

## Usage Examples

### Creating a Client (Using Required Fields Only)

```python
from clients.models import Client

# Create client with required fields only
client = Client.objects.create(
    name="ABC Auto Shop",
    country="USA",
    city="New York",
    contact_number="+1-555-0123",
    email="contact@abcautoshop.com"
)
```

### Creating a Client (With Additional Fields)

```python
client = Client.objects.create(
    name="XYZ Motors",
    code="CLT-001",
    country="Canada",
    city="Toronto",
    contact_number="+1-416-555-0123",
    email="info@xyzmotors.ca",
    address="123 Main Street",
    state="Ontario",
    postal_code="M5H 2N2",
    client_type="DEALER",
    payment_terms="Net 30",
    credit_limit=25000.00,
    discount_percentage=5.00
)
```

### Querying Clients

```python
# Get all active clients
active_clients = Client.objects.filter(is_active=True)

# Get clients by country
us_clients = Client.objects.filter(country="USA")

# Get clients by city
nyc_clients = Client.objects.filter(city="New York")

# Search clients by name or email
clients = Client.objects.filter(
    models.Q(name__icontains="Auto") | 
    models.Q(email__icontains="shop")
)

# Get client by code
client = Client.objects.get(code="CLT-001")
```

### Using Helper Methods

```python
client = Client.objects.get(name="ABC Auto Shop")

# Get formatted full address
full_address = client.get_full_address()
# Returns: "123 Main Street, New York, NY, 10001, USA"

# Get city and country
location = client.get_location()
# Returns: "New York, USA"
```

## Model Features

### Database Indexes

Indexes are created on:
- `name` - For fast name lookups
- `code` - For fast code lookups
- `country` - For country-based filtering
- `city` - For city-based filtering
- `is_active` - For active/inactive filtering
- `email` - For email lookups
- `client_type` - For client type filtering

### Validations

- Email validation using Django's EmailValidator
- Unique constraints on `name` and `code`
- Required fields: `name`, `country`, `city`, `contact_number`, `email`
- Discount percentage validation (0-100)

### Admin Interface

The model is registered in Django Admin with:
- List display showing key fields
- Search functionality (name, code, email, contact_number, country, city, address, tax_id)
- Filters (is_active, client_type, country, city, created_at)
- Organized fieldsets for better UX
- Read-only timestamp fields

## Migration Commands

```powershell
# Create migrations
python manage.py makemigrations clients

# Apply migrations
python manage.py migrate

# Check for issues
python manage.py check
```

## Admin Access

Access the client admin interface at:
`http://localhost:8000/admin/clients/client/`

## Model Meta Options

- **Verbose Name**: "Client"
- **Verbose Name Plural**: "Clients"
- **Default Ordering**: By name (alphabetical)
- **Indexes**: Optimized for common queries

## Relationships

The Client model can be referenced by:
- **Sales** model (sales app) - Many sales orders can belong to one client
- **Orders** model - Orders reference clients

## Status

✅ **Model is ready to use!**

All requested fields are implemented and the model is fully functional. The code is located at `backend/clients/models.py` and is ready for migrations and use.

## Next Steps

1. Run migrations: `python manage.py makemigrations clients && python manage.py migrate`
2. Create superuser (if not done): `python manage.py createsuperuser`
3. Access admin panel and test the model
4. Create serializers for REST API
5. Create viewsets for CRUD operations


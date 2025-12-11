# Django Project Setup - ERP Core

Complete guide to create the Django project 'erp_core' and all required apps.

## Prerequisites

- Python virtual environment activated
- Django installed (`pip install -r requirements.txt`)
- Navigate to `backend` directory

---

## Step 1: Create Django Project

### Terminal Commands

```powershell
# Navigate to backend directory
cd D:\ERP_SYSTEM\backend

# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Create Django project named 'erp_core'
# The dot (.) at the end creates the project in the current directory
django-admin startproject erp_core .

# Verify project creation
dir
# You should see: manage.py, erp_core/ folder, requirements.txt
```

**Expected Output:**
```
backend/
├── manage.py
├── erp_core/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── requirements.txt
```

---

## Step 2: Create Django Apps

### Terminal Commands

```powershell
# Ensure you're in backend directory with venv activated
cd D:\ERP_SYSTEM\backend
.\venv\Scripts\Activate.ps1

# Create all required apps
python manage.py startapp inventory
python manage.py startapp vendors
python manage.py startapp clients
python manage.py startapp purchases
python manage.py startapp sales
python manage.py startapp accounts

# Verify apps were created
dir
# You should see all app folders
```

**Expected Output:**
```
backend/
├── manage.py
├── erp_core/
├── inventory/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── vendors/
├── clients/
├── purchases/
├── sales/
└── accounts/
```

---

## Step 3: Register Apps in settings.py

### Edit `erp_core/settings.py`

Open `backend/erp_core/settings.py` and locate the `INSTALLED_APPS` section. Add all your apps:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    
    # Local apps - Add your apps here
    'accounts',
    'inventory',
    'vendors',
    'clients',
    'purchases',
    'sales',
]
```

**Important Notes:**
- Apps should be listed in dependency order (if one app depends on another)
- `accounts` is typically listed first as it may be used by other apps
- Keep third-party apps separate from local apps for clarity

---

## Step 4: Create Initial Migrations

### Terminal Commands

```powershell
# Create migrations for all apps
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Verify migrations
python manage.py showmigrations
```

---

## Recommended Backend Folder Structure

```
backend/
│
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── .env                               # Environment variables (DO NOT COMMIT)
├── .gitignore                         # Git ignore rules
│
├── erp_core/                          # Django project (main settings)
│   ├── __init__.py
│   ├── settings.py                    # Project settings
│   ├── urls.py                        # Main URL configuration
│   ├── wsgi.py                        # WSGI config for deployment
│   └── asgi.py                        # ASGI config for async
│
├── accounts/                          # User & Authentication app
│   ├── __init__.py
│   ├── admin.py                       # Admin configuration
│   ├── apps.py                        # App configuration
│   ├── models.py                      # User models
│   ├── views.py                       # View functions/classes
│   ├── serializers.py                 # DRF serializers
│   ├── urls.py                        # App URL patterns
│   ├── permissions.py                 # Custom permissions
│   ├── tests.py                       # Unit tests
│   └── migrations/                    # Database migrations
│
├── inventory/                         # Inventory Management app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                      # Product, Stock, Warehouse models
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── filters.py                     # Custom filters
│   ├── tests.py
│   └── migrations/
│
├── vendors/                           # Vendor/Supplier Management app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                      # Vendor, VendorContact models
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── tests.py
│   └── migrations/
│
├── clients/                           # Client/Customer Management app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                      # Client, ClientContact models
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── tests.py
│   └── migrations/
│
├── purchases/                         # Purchase Order Management app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                      # PurchaseOrder, PurchaseItem models
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── signals.py                     # Django signals
│   ├── tests.py
│   └── migrations/
│
├── sales/                             # Sales Order Management app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                      # SalesOrder, SalesItem models
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── signals.py
│   ├── tests.py
│   └── migrations/
│
├── core/                              # Shared utilities (optional)
│   ├── __init__.py
│   ├── permissions.py                 # Shared permissions
│   ├── mixins.py                      # Reusable mixins
│   ├── pagination.py                  # Custom pagination
│   ├── exceptions.py                  # Custom exceptions
│   └── utils.py                       # Utility functions
│
├── static/                            # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
│
├── staticfiles/                       # Collected static files (generated)
│
├── media/                             # User uploaded files
│   ├── documents/
│   ├── images/
│   └── exports/
│
└── templates/                         # HTML templates (if using server-side rendering)
    └── base.html
```

---

## Step 5: Configure URLs

### Update `erp_core/urls.py`

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API endpoints for each app
    path('api/accounts/', include('accounts.urls')),
    path('api/inventory/', include('inventory.urls')),
    path('api/vendors/', include('vendors.urls')),
    path('api/clients/', include('clients.urls')),
    path('api/purchases/', include('purchases.urls')),
    path('api/sales/', include('sales.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

---

## Step 6: Create URL Files for Each App

### Create `urls.py` in each app directory

**Example for `inventory/urls.py`:**

```python
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# Register viewsets here
# router.register(r'products', views.ProductViewSet)

urlpatterns = [
    # Add your URL patterns here
] + router.urls
```

**Repeat for each app:**
- `accounts/urls.py`
- `vendors/urls.py`
- `clients/urls.py`
- `purchases/urls.py`
- `sales/urls.py`

---

## Step 7: Verify Setup

### Terminal Commands

```powershell
# Check for any configuration errors
python manage.py check

# Verify all apps are registered
python manage.py showmigrations

# Run development server
python manage.py runserver
```

**Expected Output:**
```
System check identified no issues (0 silenced).
Django version X.X.X, using settings 'erp_core.settings'
Starting development server at http://127.0.0.1:8000/
```

---

## Quick Setup Script (All Commands Together)

```powershell
# Navigate to backend directory
cd D:\ERP_SYSTEM\backend

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Create Django project
django-admin startproject erp_core .

# Create all apps
python manage.py startapp inventory
python manage.py startapp vendors
python manage.py startapp clients
python manage.py startapp purchases
python manage.py startapp sales
python manage.py startapp accounts

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (optional, follow prompts)
python manage.py createsuperuser

# Run server
python manage.py runserver
```

---

## App Responsibilities

### accounts
- User authentication and authorization
- User profiles and roles
- JWT token management
- Permissions and groups

### inventory
- Product catalog management
- Stock levels and tracking
- Warehouse/location management
- Inventory movements
- Stock adjustments

### vendors
- Vendor/supplier information
- Vendor contacts
- Vendor performance tracking
- Vendor agreements/contracts

### clients
- Client/customer information
- Client contacts
- Customer credit limits
- Customer payment terms

### purchases
- Purchase orders
- Purchase order items
- Purchase receipts
- Purchase returns
- Vendor invoices

### sales
- Sales orders
- Sales order items
- Sales invoices
- Sales returns
- Delivery notes

---

## Next Steps

1. **Define Models**: Create models for each app in `models.py`
2. **Create Serializers**: Define DRF serializers in `serializers.py`
3. **Create Viewsets**: Implement API viewsets in `views.py`
4. **Configure URLs**: Set up URL routing in each app's `urls.py`
5. **Set up Admin**: Register models in each app's `admin.py`
6. **Write Tests**: Create unit tests in `tests.py`

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'erp_core'"
**Solution**: Ensure you're in the `backend` directory when running commands

### Issue: "App 'inventory' not found"
**Solution**: Verify the app is added to `INSTALLED_APPS` in `settings.py`

### Issue: "No such table" errors
**Solution**: Run `python manage.py migrate` to create database tables

### Issue: Import errors
**Solution**: Ensure all apps are in the same directory level and properly structured

---

**Setup Complete!** 🎉


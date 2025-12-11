# API Setup Guide

Complete guide to set up Django REST Framework APIs for all modules.

## Prerequisites

- Django project created
- All apps created and models migrated
- Django REST Framework installed

## Step 1: Install Required Packages

```powershell
cd D:\ERP_SYSTEM\backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Required packages:
- `djangorestframework>=3.14.0`
- `djangorestframework-simplejwt>=5.3.0`
- `django-filter>=23.0`
- `django-cors-headers>=4.3.0`

## Step 2: Update Main URLs

Update `erp_core/urls.py` (or your project's main urls.py):

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
    
    # API endpoints
    path('api/inventory/', include('inventory.urls')),
    path('api/vendors/', include('vendors.urls')),
    path('api/clients/', include('clients.urls')),
    path('api/purchases/', include('purchases.urls')),
    path('api/sales/', include('sales.urls')),
    path('api/accounts/', include('accounts.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

## Step 3: Update Settings

Ensure `settings.py` includes:

```python
INSTALLED_APPS = [
    # ... other apps ...
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    
    # Local apps
    'accounts',
    'inventory',
    'vendors',
    'clients',
    'purchases',
    'sales',
]

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

## Step 4: Verify Setup

```powershell
# Check for errors
python manage.py check

# Run migrations (if needed)
python manage.py migrate

# Start server
python manage.py runserver
```

## Step 5: Test API Endpoints

### Get Authentication Token

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Test Inventory Endpoint

```bash
curl -X GET http://localhost:8000/api/inventory/items/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## API Endpoints Summary

### Inventory
- `/api/inventory/categories/`
- `/api/inventory/warehouses/`
- `/api/inventory/items/`
- `/api/inventory/stock/`

### Vendors
- `/api/vendors/`

### Clients
- `/api/clients/`

### Purchases
- `/api/purchases/orders/`
- `/api/purchases/items/`

### Sales
- `/api/sales/orders/`
- `/api/sales/items/`

### Accounts
- `/api/accounts/payments/`
- `/api/accounts/ledger/`
- `/api/accounts/profit-loss/`

## Features

✅ Full CRUD operations for all models  
✅ Nested relationships handled  
✅ Filtering, searching, and ordering  
✅ Pagination (50 items per page)  
✅ JWT authentication  
✅ Custom actions (mark_shipped, cancel, etc.)  
✅ Calculated fields (totals, margins, etc.)  
✅ Stock reduction logic  
✅ Ledger tracking  
✅ Profit/loss calculations  

## Next Steps

1. Test all endpoints using Postman or curl
2. Create frontend application
3. Add custom permissions if needed
4. Add rate limiting
5. Add API documentation (drf-spectacular or drf-yasg)


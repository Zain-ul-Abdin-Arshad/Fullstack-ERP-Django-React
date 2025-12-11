# API Integration Guide - Django Backend & React Frontend

Complete step-by-step guide to integrate Django REST Framework APIs with React frontend.

## Table of Contents

1. [Backend Configuration](#backend-configuration)
2. [Frontend Configuration](#frontend-configuration)
3. [JWT Authentication Setup](#jwt-authentication-setup)
4. [Axios Interceptors](#axios-interceptors)
5. [Module Integration](#module-integration)
6. [Testing Guidelines](#testing-guidelines)
7. [Troubleshooting](#troubleshooting)

---

## Backend Configuration

### Step 1: Update Django Settings for CORS

Edit `backend/erp_core/settings.py` (or your project's settings.py):

```python
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ... other apps
    'corsheaders',
]

# Add to MIDDLEWARE (should be near the top)
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Add this
    'django.middleware.security.SecurityMiddleware',
    # ... rest of middleware
]

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React dev server
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
```

### Step 2: Verify REST Framework Settings

Ensure `settings.py` has:

```python
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

### Step 3: Update Main URLs

Edit `backend/erp_core/urls.py`:

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

---

## Frontend Configuration

### Step 1: Verify API Base URL

Check `frontend/src/services/api.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

Update if your backend runs on a different port.

### Step 2: Verify Axios Installation

```powershell
cd frontend
npm list axios
# Should show axios version
```

If not installed:
```powershell
npm install axios
```

---

## JWT Authentication Setup

### Backend: Token Endpoints

**Login Endpoint:**
```
POST http://localhost:8000/api/token/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Refresh Token Endpoint:**
```
POST http://localhost:8000/api/token/refresh/
Content-Type: application/json

{
  "refresh": "your_refresh_token"
}
```

**Response:**
```json
{
  "access": "new_access_token"
}
```

### Frontend: Authentication Flow

**1. Login Process** (`src/services/auth.js`):

```javascript
login: async (username, password) => {
  const response = await axios.post('http://localhost:8000/api/token/', {
    username,
    password
  });
  const { access, refresh } = response.data;
  localStorage.setItem('access_token', access);
  localStorage.setItem('refresh_token', refresh);
  return { access, refresh };
}
```

**2. Token Storage:**
- Access token: Stored in `localStorage` as `access_token`
- Refresh token: Stored in `localStorage` as `refresh_token`

**3. Logout Process:**
```javascript
logout: () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
}
```

---

## Axios Interceptors

### Request Interceptor

Automatically adds JWT token to all requests:

```javascript
// In src/services/api.js
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
```

**How it works:**
- Intercepts every API request
- Checks for access token in localStorage
- Adds `Authorization: Bearer <token>` header
- Request continues with token

### Response Interceptor

Handles token refresh on 401 errors:

```javascript
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If 401 and not already retried
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(
            'http://localhost:8000/api/token/refresh/',
            { refresh: refreshToken }
          );

          const { access } = response.data;
          localStorage.setItem('access_token', access);
          originalRequest.headers.Authorization = `Bearer ${access}`;

          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);
```

**How it works:**
- Intercepts API responses
- If 401 (Unauthorized), tries to refresh token
- Retries original request with new token
- If refresh fails, redirects to login

---

## Module Integration

### Inventory Module

#### Get All Items

**API Call:**
```javascript
import { inventoryService } from '../services/modules/inventory';

const loadItems = async () => {
  try {
    const response = await inventoryService.getItems();
    console.log(response.data);
    // Response: { results: [...], count: 100, next: "...", previous: null }
  } catch (error) {
    console.error('Error:', error.response?.data);
  }
};
```

**Sample Request:**
```http
GET http://localhost:8000/api/inventory/items/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Sample Response:**
```json
{
  "count": 50,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Car Battery 12V",
      "sku": "BATT-12V-001",
      "category_name": "Batteries",
      "cost_price": "50.00",
      "selling_price": "75.00",
      "total_stock": 100,
      "is_low_stock": false,
      "is_active": true
    }
  ]
}
```

#### Create Item

**API Call:**
```javascript
const createItem = async () => {
  const itemData = {
    name: "New Battery",
    sku: "BATT-NEW-001",
    category: 1,
    cost_price: "50.00",
    selling_price: "75.00",
    unit: "PCS",
    reorder_level: 10,
    is_active: true
  };

  try {
    const response = await inventoryService.createItem(itemData);
    console.log('Created:', response.data);
  } catch (error) {
    console.error('Error:', error.response?.data);
  }
};
```

**Sample Request:**
```http
POST http://localhost:8000/api/inventory/items/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "name": "New Battery",
  "sku": "BATT-NEW-001",
  "category": 1,
  "cost_price": "50.00",
  "selling_price": "75.00",
  "unit": "PCS",
  "reorder_level": 10
}
```

**Sample Response:**
```json
{
  "id": 2,
  "name": "New Battery",
  "sku": "BATT-NEW-001",
  "category": 1,
  "category_name": "Batteries",
  "cost_price": "50.00",
  "selling_price": "75.00",
  "total_stock": 0,
  "is_low_stock": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Get Stock Levels

**API Call:**
```javascript
const loadStock = async () => {
  try {
    const response = await inventoryService.getStock({ warehouse: 1 });
    console.log(response.data);
  } catch (error) {
    console.error('Error:', error.response?.data);
  }
};
```

**Sample Request:**
```http
GET http://localhost:8000/api/inventory/stock/?warehouse=1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Sample Response:**
```json
{
  "results": [
    {
      "id": 1,
      "item": 1,
      "item_name": "Car Battery 12V",
      "item_sku": "BATT-12V-001",
      "warehouse": 1,
      "warehouse_name": "Main Warehouse",
      "quantity": 100,
      "reserved_quantity": 5,
      "available_quantity": 95,
      "min_quantity": 10,
      "is_low_stock": false
    }
  ]
}
```

---

### Vendors Module

#### Get All Vendors

**API Call:**
```javascript
import { vendorsService } from '../services/modules/vendors';

const loadVendors = async () => {
  try {
    const response = await vendorsService.getVendors();
    console.log(response.data);
  } catch (error) {
    console.error('Error:', error.response?.data);
  }
};
```

**Sample Request:**
```http
GET http://localhost:8000/api/vendors/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Sample Response:**
```json
{
  "results": [
    {
      "id": 1,
      "name": "ABC Suppliers",
      "code": "VND-001",
      "country": "USA",
      "contact_number": "+1-555-0123",
      "email": "contact@abcsuppliers.com",
      "is_active": true,
      "items_count": 25
    }
  ]
}
```

#### Create Vendor

**API Call:**
```javascript
const createVendor = async () => {
  const vendorData = {
    name: "XYZ Suppliers",
    code: "VND-002",
    country: "Germany",
    contact_number: "+49-30-12345678",
    email: "info@xyzsuppliers.de",
    is_active: true
  };

  try {
    const response = await vendorsService.createVendor(vendorData);
    console.log('Created:', response.data);
  } catch (error) {
    console.error('Error:', error.response?.data);
  }
};
```

**Sample Request:**
```http
POST http://localhost:8000/api/vendors/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "name": "XYZ Suppliers",
  "code": "VND-002",
  "country": "Germany",
  "contact_number": "+49-30-12345678",
  "email": "info@xyzsuppliers.de"
}
```

**Sample Response:**
```json
{
  "id": 2,
  "name": "XYZ Suppliers",
  "code": "VND-002",
  "country": "Germany",
  "contact_number": "+49-30-12345678",
  "email": "info@xyzsuppliers.de",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### Clients Module

#### Get All Clients

**API Call:**
```javascript
import { clientsService } from '../services/modules/clients';

const loadClients = async () => {
  try {
    const response = await clientsService.getClients();
    console.log(response.data);
  } catch (error) {
    console.error('Error:', error.response?.data);
  }
};
```

**Sample Request:**
```http
GET http://localhost:8000/api/clients/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Sample Response:**
```json
{
  "results": [
    {
      "id": 1,
      "name": "ABC Auto Shop",
      "code": "CLT-001",
      "country": "USA",
      "city": "New York",
      "contact_number": "+1-555-0123",
      "email": "contact@abcautoshop.com",
      "client_type": "RETAILER",
      "is_active": true,
      "sales_orders_count": 15
    }
  ]
}
```

#### Create Client

**API Call:**
```javascript
const createClient = async () => {
  const clientData = {
    name: "XYZ Motors",
    code: "CLT-002",
    country: "Canada",
    city: "Toronto",
    contact_number: "+1-416-555-0123",
    email: "info@xyzmotors.ca",
    client_type: "DEALER"
  };

  try {
    const response = await clientsService.createClient(clientData);
    console.log('Created:', response.data);
  } catch (error) {
    console.error('Error:', error.response?.data);
  }
};
```

---

### Purchases Module

#### Create Purchase Order with Items

**API Call:**
```javascript
import { purchasesService } from '../services/modules/purchases';

const createPurchaseOrder = async () => {
  const orderData = {
    vendor: 1,
    order_number: "PO-2024-001",
    order_date: "2024-01-15",
    status: "PENDING",
    purchase_items: [
      {
        item: 1,
        quantity: 100,
        unit_cost: "50.00",
        freight_cost: "500.00",
        customs_duty: "200.00",
        other_costs: "100.00",
        received_quantity: 0  // Will be updated when received
      }
    ]
  };

  try {
    const response = await purchasesService.createPurchaseOrder(orderData);
    console.log('Created:', response.data);
  } catch (error) {
    console.error('Error:', error.response?.data);
  }
};
```

**Sample Request:**
```http
POST http://localhost:8000/api/purchases/orders/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "vendor": 1,
  "order_number": "PO-2024-001",
  "order_date": "2024-01-15",
  "status": "PENDING",
  "purchase_items": [
    {
      "item": 1,
      "quantity": 100,
      "unit_cost": "50.00",
      "freight_cost": "500.00",
      "customs_duty": "200.00"
    }
  ]
}
```

**Sample Response:**
```json
{
  "id": 1,
  "vendor": 1,
  "vendor_name": "ABC Suppliers",
  "order_number": "PO-2024-001",
  "order_date": "2024-01-15",
  "total_amount": "5000.00",
  "status": "PENDING",
  "purchase_items": [
    {
      "id": 1,
      "item": 1,
      "item_name": "Car Battery 12V",
      "quantity": 100,
      "unit_cost": "50.00",
      "line_total": "5000.00",
      "landed_cost_per_unit": "58.00",
      "total_landed_cost": "5800.00"
    }
  ]
}
```

#### Mark Purchase Order as Received

**API Call:**
```javascript
const markReceived = async (orderId) => {
  try {
    // First, update received_quantity for items
    const order = await purchasesService.getPurchaseOrder(orderId);
    
    // Update received quantities
    for (const item of order.data.purchase_items) {
      await purchasesService.updatePurchaseItem(item.id, {
        received_quantity: item.quantity
      });
    }
    
    // Mark order as received (triggers stock increase)
    const response = await purchasesService.markReceived(orderId);
    console.log('Order received:', response.data);
    // Stock automatically increased via signals!
  } catch (error) {
    console.error('Error:', error.response?.data);
  }
};
```

**Sample Request:**
```http
POST http://localhost:8000/api/purchases/orders/1/mark_received/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Sample Response:**
```json
{
  "id": 1,
  "status": "RECEIVED",
  "received_date": "2024-01-15",
  "total_amount": "5000.00"
}
```

**Stock Update:**
- Stock quantity automatically increased by 100
- Average cost updated
- Low stock alert checked

---

### Sales Module

#### Create Sales Order with Stock Validation

**API Call:**
```javascript
import { salesService } from '../services/modules/sales';

const createSalesOrder = async () => {
  const orderData = {
    client: 1,
    order_number: "SO-2024-001",
    order_date: "2024-01-15",
    warehouse: 1,  // Required for stock validation
    status: "PENDING",
    sales_items: [
      {
        item: 1,
        quantity: 10,
        unit_price: "75.00",
        discount_percentage: "5.00"
      }
    ]
  };

  try {
    // Stock is validated automatically by backend
    const response = await salesService.createSalesOrder(orderData);
    console.log('Created:', response.data);
    // Stock automatically reserved (PENDING status)
  } catch (error) {
    if (error.response?.data?.detail?.includes('stock')) {
      alert('Insufficient stock!');
    }
    console.error('Error:', error.response?.data);
  }
};
```

**Sample Request:**
```http
POST http://localhost:8000/api/sales/orders/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "client": 1,
  "order_number": "SO-2024-001",
  "order_date": "2024-01-15",
  "warehouse": 1,
  "status": "PENDING",
  "sales_items": [
    {
      "item": 1,
      "quantity": 10,
      "unit_price": "75.00",
      "discount_percentage": "5.00"
    }
  ]
}
```

**Sample Response (Success):**
```json
{
  "id": 1,
  "client": 1,
  "client_name": "ABC Auto Shop",
  "order_number": "SO-2024-001",
  "order_date": "2024-01-15",
  "total_amount": "712.50",
  "status": "PENDING",
  "sales_items": [
    {
      "id": 1,
      "item": 1,
      "item_name": "Car Battery 12V",
      "quantity": 10,
      "unit_price": "75.00",
      "line_total": "712.50"
    }
  ]
}
```

**Sample Response (Insufficient Stock):**
```json
{
  "detail": "Insufficient stock: Only 5 units available for item 'Car Battery 12V' in warehouse 'Main Warehouse', but 10 requested"
}
```

#### Mark Sales Order as Shipped

**API Call:**
```javascript
const markShipped = async (orderId) => {
  try {
    const response = await salesService.markShipped(orderId);
    console.log('Order shipped:', response.data);
    // Stock automatically decreased via signals!
  } catch (error) {
    console.error('Error:', error.response?.data);
  }
};
```

**Sample Request:**
```http
POST http://localhost:8000/api/sales/orders/1/mark_shipped/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Sample Response:**
```json
{
  "id": 1,
  "status": "SHIPPED",
  "shipped_date": "2024-01-15",
  "total_amount": "712.50"
}
```

**Stock Update:**
- Stock quantity automatically decreased by 10
- Reserved quantity decreased by 10
- Low stock alert checked

---

### Accounts Module

#### Create Payment

**API Call:**
```javascript
import { accountsService } from '../services/modules/accounts';

const createPayment = async () => {
  const paymentData = {
    client: 1,  // OR vendor: 1 (not both)
    amount: "5000.00",
    payment_type: "CREDIT",  // CREDIT or DEBIT
    payment_method: "BANK_TRANSFER",
    date: "2024-01-15",
    description: "Payment for invoice #12345"
  };

  try {
    const response = await accountsService.createPayment(paymentData);
    console.log('Created:', response.data);
    // Ledger entry automatically created
  } catch (error) {
    console.error('Error:', error.response?.data);
  }
};
```

**Sample Request:**
```http
POST http://localhost:8000/api/accounts/payments/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "client": 1,
  "amount": "5000.00",
  "payment_type": "CREDIT",
  "payment_method": "BANK_TRANSFER",
  "date": "2024-01-15",
  "description": "Payment for invoice"
}
```

**Sample Response:**
```json
{
  "id": 1,
  "client": 1,
  "client_name": "ABC Auto Shop",
  "amount": "5000.00",
  "payment_type": "CREDIT",
  "date": "2024-01-15",
  "description": "Payment for invoice",
  "is_reconciled": false
}
```

#### Calculate Profit/Loss

**API Call:**
```javascript
const calculateProfitLoss = async () => {
  const data = {
    start_date: "2024-01-01",
    end_date: "2024-01-31"
  };

  try {
    const response = await accountsService.calculateProfitLoss(data);
    console.log('P&L:', response.data);
  } catch (error) {
    console.error('Error:', error.response?.data);
  }
};
```

**Sample Request:**
```http
POST http://localhost:8000/api/accounts/profit-loss/calculate/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "start_date": "2024-01-01",
  "end_date": "2024-01-31"
}
```

**Sample Response:**
```json
{
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "total_revenue": "50000.00",
  "total_cost_of_goods_sold": "30000.00",
  "total_expenses": "5000.00",
  "gross_profit": "20000.00",
  "net_profit": "15000.00"
}
```

---

## Testing Guidelines

### Step 1: Test Authentication

**Test Login:**
```javascript
// In browser console or React component
import { authService } from './services/auth';

const testLogin = async () => {
  try {
    const result = await authService.login('admin', 'password');
    console.log('Login successful:', result);
    console.log('Token:', localStorage.getItem('access_token'));
  } catch (error) {
    console.error('Login failed:', error);
  }
};
```

**Expected Result:**
- Tokens stored in localStorage
- `access_token` and `refresh_token` present
- No errors

### Step 2: Test API Calls

**Test Inventory API:**
```javascript
import { inventoryService } from './services/modules/inventory';

const testInventory = async () => {
  try {
    // Get items
    const items = await inventoryService.getItems();
    console.log('Items:', items.data);
    
    // Get stock
    const stock = await inventoryService.getStock();
    console.log('Stock:', stock.data);
  } catch (error) {
    console.error('Error:', error.response?.data);
  }
};
```

**Test Vendors API:**
```javascript
import { vendorsService } from './services/modules/vendors';

const testVendors = async () => {
  try {
    const vendors = await vendorsService.getVendors();
    console.log('Vendors:', vendors.data);
  } catch (error) {
    console.error('Error:', error.response?.data);
  }
};
```

### Step 3: Test Stock Integration

**Test Purchase → Stock Increase:**
```javascript
// 1. Create purchase order
const po = await purchasesService.createPurchaseOrder({
  vendor: 1,
  order_number: "PO-TEST-001",
  order_date: "2024-01-15",
  status: "PENDING",
  purchase_items: [{
    item: 1,
    quantity: 50,
    unit_cost: "50.00",
    received_quantity: 50
  }]
});

// 2. Mark as received
await purchasesService.markReceived(po.data.id);

// 3. Check stock increased
const stock = await inventoryService.getStock({ item: 1 });
console.log('Stock after purchase:', stock.data);
// Should show increased quantity
```

**Test Sales → Stock Decrease:**
```javascript
// 1. Check current stock
const stockBefore = await inventoryService.getStock({ item: 1, warehouse: 1 });
console.log('Stock before:', stockBefore.data[0].quantity);

// 2. Create sales order
const so = await salesService.createSalesOrder({
  client: 1,
  order_number: "SO-TEST-001",
  order_date: "2024-01-15",
  warehouse: 1,
  status: "PENDING",
  sales_items: [{
    item: 1,
    quantity: 10,
    unit_price: "75.00"
  }]
});

// 3. Mark as shipped
await salesService.markShipped(so.data.id);

// 4. Check stock decreased
const stockAfter = await inventoryService.getStock({ item: 1, warehouse: 1 });
console.log('Stock after:', stockAfter.data[0].quantity);
// Should be 10 less than before
```

### Step 4: Test Error Handling

**Test Insufficient Stock:**
```javascript
const testInsufficientStock = async () => {
  try {
    // Try to create order with more than available stock
    await salesService.createSalesOrder({
      client: 1,
      order_number: "SO-TEST-002",
      order_date: "2024-01-15",
      warehouse: 1,
      status: "PENDING",
      sales_items: [{
        item: 1,
        quantity: 10000,  // More than available
        unit_price: "75.00"
      }]
    });
  } catch (error) {
    console.log('Expected error:', error.response?.data.detail);
    // Should show insufficient stock error
  }
};
```

### Step 5: Test Token Refresh

**Simulate Token Expiry:**
```javascript
// Manually expire token
localStorage.setItem('access_token', 'expired_token');

// Make API call - should auto-refresh
try {
  const items = await inventoryService.getItems();
  console.log('Token refreshed automatically:', items.data);
} catch (error) {
  console.error('Refresh failed:', error);
}
```

---

## Complete Integration Checklist

### Backend Setup
- [ ] CORS configured in settings.py
- [ ] JWT authentication configured
- [ ] All apps registered in INSTALLED_APPS
- [ ] URLs configured for all modules
- [ ] Migrations applied
- [ ] Superuser created

### Frontend Setup
- [ ] Dependencies installed (`npm install`)
- [ ] API base URL configured
- [ ] Axios interceptors set up
- [ ] Auth service configured
- [ ] All service modules created

### Testing
- [ ] Login works
- [ ] Token stored correctly
- [ ] API calls include token
- [ ] Token refresh works
- [ ] All CRUD operations work
- [ ] Stock updates work (purchase)
- [ ] Stock updates work (sales)
- [ ] Stock validation works
- [ ] Error handling works

---

## Common Issues & Solutions

### Issue 1: CORS Errors

**Error:**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution:**
1. Check `CORS_ALLOWED_ORIGINS` in Django settings
2. Ensure frontend URL matches (http://localhost:3000)
3. Restart Django server

### Issue 2: 401 Unauthorized

**Error:**
```
401 Unauthorized
```

**Solution:**
1. Check token exists: `localStorage.getItem('access_token')`
2. Verify token format: Should start with `eyJ`
3. Check token expiry
4. Try refreshing token manually

### Issue 3: Token Refresh Loop

**Error:**
```
Infinite redirect to login
```

**Solution:**
1. Clear localStorage
2. Check refresh token endpoint
3. Verify token refresh logic in interceptor

### Issue 4: Stock Not Updating

**Error:**
```
Stock not increasing/decreasing
```

**Solution:**
1. Check purchase order status is "RECEIVED"
2. Check sales order status is "SHIPPED" or "DELIVERED"
3. Verify signals are registered in apps.py
4. Check Django server logs for errors

### Issue 5: Validation Errors

**Error:**
```
400 Bad Request with validation errors
```

**Solution:**
1. Check request payload matches API expectations
2. Verify required fields are included
3. Check field types (numbers vs strings)
4. Review error response for specific field errors

---

## Testing Script

Create `frontend/src/utils/testAPI.js`:

```javascript
/**
 * API Testing Utility
 */

import { authService } from '../services/auth';
import { inventoryService } from '../services/modules/inventory';
import { vendorsService } from '../services/modules/vendors';
import { salesService } from '../services/modules/sales';
import { purchasesService } from '../services/modules/purchases';

export const testAllAPIs = async () => {
  console.log('=== Starting API Tests ===\n');

  // Test 1: Authentication
  console.log('1. Testing Authentication...');
  try {
    await authService.login('admin', 'password');
    console.log('✅ Login successful');
  } catch (error) {
    console.error('❌ Login failed:', error.message);
    return;
  }

  // Test 2: Inventory
  console.log('\n2. Testing Inventory API...');
  try {
    const items = await inventoryService.getItems();
    console.log(`✅ Got ${items.data.results?.length || 0} items`);
  } catch (error) {
    console.error('❌ Inventory API failed:', error.message);
  }

  // Test 3: Vendors
  console.log('\n3. Testing Vendors API...');
  try {
    const vendors = await vendorsService.getVendors();
    console.log(`✅ Got ${vendors.data.results?.length || 0} vendors`);
  } catch (error) {
    console.error('❌ Vendors API failed:', error.message);
  }

  // Test 4: Stock
  console.log('\n4. Testing Stock API...');
  try {
    const stock = await inventoryService.getStock();
    console.log(`✅ Got ${stock.data.results?.length || 0} stock entries`);
  } catch (error) {
    console.error('❌ Stock API failed:', error.message);
  }

  console.log('\n=== API Tests Complete ===');
};

// Run in browser console:
// import { testAllAPIs } from './utils/testAPI';
// testAllAPIs();
```

---

## Next Steps

1. **Test all endpoints** using the testing script
2. **Verify stock updates** work correctly
3. **Test error scenarios** (insufficient stock, validation errors)
4. **Add error boundaries** in React components
5. **Add loading states** for better UX
6. **Add form validation** on frontend
7. **Add pagination** for large lists
8. **Add real-time updates** (WebSockets optional)

---

## Quick Reference

### API Base URL
```
http://localhost:8000/api
```

### Authentication Endpoints
```
POST /api/token/          - Login
POST /api/token/refresh/  - Refresh token
```

### Module Endpoints
```
GET    /api/inventory/items/        - List items
POST   /api/inventory/items/        - Create item
GET    /api/inventory/stock/        - List stock
GET    /api/vendors/                - List vendors
POST   /api/vendors/                - Create vendor
GET    /api/clients/                - List clients
POST   /api/clients/                - Create client
POST   /api/purchases/orders/       - Create purchase order
POST   /api/sales/orders/           - Create sales order
POST   /api/accounts/payments/      - Create payment
```

All endpoints require `Authorization: Bearer <token>` header.


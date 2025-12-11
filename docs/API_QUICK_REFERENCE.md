# API Quick Reference

Quick reference for API endpoints and usage.

## Authentication

### Login
```javascript
POST /api/token/
Body: { username, password }
Response: { access, refresh }
```

### Refresh Token
```javascript
POST /api/token/refresh/
Body: { refresh }
Response: { access }
```

## Inventory API

### Items
```javascript
GET    /api/inventory/items/              - List items
GET    /api/inventory/items/{id}/         - Get item
POST   /api/inventory/items/              - Create item
PUT    /api/inventory/items/{id}/         - Update item
DELETE /api/inventory/items/{id}/         - Delete item
GET    /api/inventory/items/low_stock/    - Low stock items
```

### Stock
```javascript
GET    /api/inventory/stock/              - List stock
GET    /api/inventory/stock/{id}/         - Get stock entry
POST   /api/inventory/stock/              - Create stock
PUT    /api/inventory/stock/{id}/         - Update stock
GET    /api/inventory/stock/low_stock/     - Low stock entries
GET    /api/inventory/stock/out_of_stock/ - Out of stock entries
```

### Categories
```javascript
GET    /api/inventory/categories/         - List categories
POST   /api/inventory/categories/         - Create category
PUT    /api/inventory/categories/{id}/    - Update category
DELETE /api/inventory/categories/{id}/    - Delete category
```

### Warehouses
```javascript
GET    /api/inventory/warehouses/         - List warehouses
POST   /api/inventory/warehouses/         - Create warehouse
PUT    /api/inventory/warehouses/{id}/    - Update warehouse
DELETE /api/inventory/warehouses/{id}/    - Delete warehouse
```

## Vendors API

```javascript
GET    /api/vendors/                      - List vendors
GET    /api/vendors/{id}/                 - Get vendor
POST   /api/vendors/                      - Create vendor
PUT    /api/vendors/{id}/                 - Update vendor
DELETE /api/vendors/{id}/                 - Delete vendor
```

## Clients API

```javascript
GET    /api/clients/                      - List clients
GET    /api/clients/{id}/                 - Get client
POST   /api/clients/                      - Create client
PUT    /api/clients/{id}/                 - Update client
DELETE /api/clients/{id}/                 - Delete client
```

## Purchases API

### Purchase Orders
```javascript
GET    /api/purchases/orders/             - List orders
GET    /api/purchases/orders/{id}/        - Get order
POST   /api/purchases/orders/             - Create order
PUT    /api/purchases/orders/{id}/        - Update order
DELETE /api/purchases/orders/{id}/        - Delete order
POST   /api/purchases/orders/{id}/mark_received/ - Mark received
POST   /api/purchases/orders/{id}/recalculate_total/ - Recalculate total
```

### Purchase Items
```javascript
GET    /api/purchases/items/              - List items
GET    /api/purchases/items/{id}/         - Get item
POST   /api/purchases/items/              - Create item
PUT    /api/purchases/items/{id}/         - Update item
DELETE /api/purchases/items/{id}/         - Delete item
```

## Sales API

### Sales Orders
```javascript
GET    /api/sales/orders/                 - List orders
GET    /api/sales/orders/{id}/            - Get order
POST   /api/sales/orders/                 - Create order
PUT    /api/sales/orders/{id}/            - Update order
DELETE /api/sales/orders/{id}/            - Delete order
POST   /api/sales/orders/{id}/mark_shipped/ - Mark shipped
POST   /api/sales/orders/{id}/mark_delivered/ - Mark delivered
POST   /api/sales/orders/{id}/cancel/     - Cancel order
POST   /api/sales/orders/{id}/recalculate_total/ - Recalculate total
```

### Sales Items
```javascript
GET    /api/sales/items/                  - List items
GET    /api/sales/items/{id}/             - Get item
POST   /api/sales/items/                  - Create item
PUT    /api/sales/items/{id}/             - Update item
DELETE /api/sales/items/{id}/             - Delete item
```

## Accounts API

### Payments
```javascript
GET    /api/accounts/payments/            - List payments
GET    /api/accounts/payments/{id}/       - Get payment
POST   /api/accounts/payments/            - Create payment
PUT    /api/accounts/payments/{id}/       - Update payment
DELETE /api/accounts/payments/{id}/       - Delete payment
POST   /api/accounts/payments/{id}/reconcile/ - Reconcile payment
```

### Ledger
```javascript
GET    /api/accounts/ledger/               - List entries
GET    /api/accounts/ledger/{id}/          - Get entry
GET    /api/accounts/ledger/summary/       - Get summary
```

### Profit/Loss
```javascript
GET    /api/accounts/profit-loss/          - List reports
GET    /api/accounts/profit-loss/{id}/     - Get report
POST   /api/accounts/profit-loss/calculate/ - Calculate P&L
POST   /api/accounts/profit-loss/create_report/ - Create report
```

## Query Parameters

### Pagination
```
?page=1&page_size=50
```

### Filtering
```
?status=PENDING
?warehouse=1
?item=1
?vendor=1
?client=1
?start_date=2024-01-01&end_date=2024-01-31
```

### Searching
```
?search=battery
```

### Ordering
```
?ordering=-created_at
?ordering=name
```

## Frontend Usage Examples

### Using Services

```javascript
import { inventoryService } from '../services/modules/inventory';
import { vendorsService } from '../services/modules/vendors';
import { salesService } from '../services/modules/sales';
import { purchasesService } from '../services/modules/purchases';
import { accountsService } from '../services/modules/accounts';
import { authService } from '../services/auth';
```

### Get Items with Filters
```javascript
const items = await inventoryService.getItems({
  page: 1,
  search: 'battery',
  category: 1,
  is_active: true
});
```

### Create Purchase Order
```javascript
const order = await purchasesService.createPurchaseOrder({
  vendor: 1,
  order_number: "PO-001",
  order_date: "2024-01-15",
  status: "PENDING",
  purchase_items: [{
    item: 1,
    quantity: 100,
    unit_cost: "50.00",
    freight_cost: "500.00"
  }]
});
```

### Create Sales Order
```javascript
const order = await salesService.createSalesOrder({
  client: 1,
  order_number: "SO-001",
  order_date: "2024-01-15",
  warehouse: 1,
  status: "PENDING",
  sales_items: [{
    item: 1,
    quantity: 10,
    unit_price: "75.00"
  }]
});
```

## Error Handling

### Standard Error Response
```json
{
  "detail": "Error message"
}
```

### Validation Errors
```json
{
  "field_name": ["Error message"],
  "another_field": ["Error message"]
}
```

### Frontend Error Handling
```javascript
try {
  const response = await inventoryService.createItem(data);
} catch (error) {
  if (error.response?.status === 400) {
    // Validation errors
    console.error(error.response.data);
  } else if (error.response?.status === 401) {
    // Unauthorized - token refresh handled automatically
  } else {
    // Other errors
    console.error('Error:', error.message);
  }
}
```

## Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request (validation errors)
- `401` - Unauthorized (token expired/invalid)
- `403` - Forbidden
- `404` - Not Found
- `500` - Server Error

## Stock Management Flow

### Purchase Flow
1. Create Purchase Order (status: PENDING)
2. Add Purchase Items
3. Update received_quantity for items
4. Mark Order as RECEIVED
5. Stock automatically increases via signals

### Sales Flow
1. Create Sales Order (status: PENDING)
2. Add Sales Items
3. Stock automatically reserved
4. Mark Order as SHIPPED
5. Stock automatically decreases via signals

## Authentication Flow

1. User logs in → Get access & refresh tokens
2. Store tokens in localStorage
3. All API calls include token in header
4. On 401 error → Refresh token automatically
5. If refresh fails → Redirect to login

---

**All endpoints require `Authorization: Bearer <token>` header except login.**


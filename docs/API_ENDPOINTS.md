# API Endpoints Documentation

Complete REST API endpoints for all ERP modules.

## Base URL

All API endpoints are prefixed with `/api/`

## Authentication

All endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_token>
```

### Get Token

```http
POST /api/token/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

### Refresh Token

```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "your_refresh_token"
}
```

---

## Inventory API

### Categories

- `GET /api/inventory/categories/` - List all categories
- `POST /api/inventory/categories/` - Create category
- `GET /api/inventory/categories/{id}/` - Get category details
- `PUT /api/inventory/categories/{id}/` - Update category
- `PATCH /api/inventory/categories/{id}/` - Partial update
- `DELETE /api/inventory/categories/{id}/` - Delete category
- `GET /api/inventory/categories/{id}/subcategories/` - Get subcategories

**Filters:** `is_active`, `parent`  
**Search:** `name`, `code`, `description`  
**Ordering:** `name`, `code`, `created_at`

### Warehouses

- `GET /api/inventory/warehouses/` - List all warehouses
- `POST /api/inventory/warehouses/` - Create warehouse
- `GET /api/inventory/warehouses/{id}/` - Get warehouse details
- `PUT /api/inventory/warehouses/{id}/` - Update warehouse
- `PATCH /api/inventory/warehouses/{id}/` - Partial update
- `DELETE /api/inventory/warehouses/{id}/` - Delete warehouse

**Filters:** `is_active`, `country`, `city`  
**Search:** `name`, `code`, `address`, `city`, `manager_name`  
**Ordering:** `name`, `code`, `created_at`

### Items

- `GET /api/inventory/items/` - List all items
- `POST /api/inventory/items/` - Create item
- `GET /api/inventory/items/{id}/` - Get item details
- `PUT /api/inventory/items/{id}/` - Update item
- `PATCH /api/inventory/items/{id}/` - Partial update
- `DELETE /api/inventory/items/{id}/` - Delete item
- `GET /api/inventory/items/{id}/stock/` - Get stock levels for item
- `GET /api/inventory/items/low_stock/` - Get low stock items

**Filters:** `is_active`, `is_trackable`, `category`, `vendor`, `vehicle_make`, `vehicle_model`, `unit`  
**Search:** `name`, `sku`, `barcode`, `description`, `vehicle_make`, `vehicle_model`  
**Ordering:** `name`, `sku`, `created_at`, `selling_price`

### Stock

- `GET /api/inventory/stock/` - List all stock entries
- `POST /api/inventory/stock/` - Create stock entry
- `GET /api/inventory/stock/{id}/` - Get stock details
- `PUT /api/inventory/stock/{id}/` - Update stock
- `PATCH /api/inventory/stock/{id}/` - Partial update
- `DELETE /api/inventory/stock/{id}/` - Delete stock
- `GET /api/inventory/stock/low_stock/` - Get low stock items
- `GET /api/inventory/stock/out_of_stock/` - Get out of stock items

**Filters:** `item`, `warehouse`, `item__category`  
**Search:** `item__name`, `item__sku`, `warehouse__name`  
**Ordering:** `item__name`, `quantity`, `created_at`

---

## Vendors API

- `GET /api/vendors/` - List all vendors
- `POST /api/vendors/` - Create vendor
- `GET /api/vendors/{id}/` - Get vendor details
- `PUT /api/vendors/{id}/` - Update vendor
- `PATCH /api/vendors/{id}/` - Partial update
- `DELETE /api/vendors/{id}/` - Delete vendor

**Filters:** `is_active`, `country`, `city`  
**Search:** `name`, `code`, `email`, `contact_number`, `country`, `city`  
**Ordering:** `name`, `code`, `created_at`

---

## Clients API

- `GET /api/clients/` - List all clients
- `POST /api/clients/` - Create client
- `GET /api/clients/{id}/` - Get client details
- `PUT /api/clients/{id}/` - Update client
- `PATCH /api/clients/{id}/` - Partial update
- `DELETE /api/clients/{id}/` - Delete client

**Filters:** `is_active`, `country`, `city`, `client_type`  
**Search:** `name`, `code`, `email`, `contact_number`, `country`, `city`  
**Ordering:** `name`, `code`, `created_at`

---

## Purchases API

### Purchase Orders

- `GET /api/purchases/orders/` - List all purchase orders
- `POST /api/purchases/orders/` - Create purchase order (with items)
- `GET /api/purchases/orders/{id}/` - Get purchase order details
- `PUT /api/purchases/orders/{id}/` - Update purchase order
- `PATCH /api/purchases/orders/{id}/` - Partial update
- `DELETE /api/purchases/orders/{id}/` - Delete purchase order
- `POST /api/purchases/orders/{id}/mark_received/` - Mark as received
- `POST /api/purchases/orders/{id}/recalculate_total/` - Recalculate total

**Filters:** `status`, `vendor`, `order_date`  
**Search:** `order_number`, `vendor__name`, `notes`  
**Ordering:** `order_date`, `created_at`, `total_amount`

### Purchase Items

- `GET /api/purchases/items/` - List all purchase items
- `POST /api/purchases/items/` - Create purchase item
- `GET /api/purchases/items/{id}/` - Get purchase item details
- `PUT /api/purchases/items/{id}/` - Update purchase item
- `PATCH /api/purchases/items/{id}/` - Partial update
- `DELETE /api/purchases/items/{id}/` - Delete purchase item

**Filters:** `purchase_order`, `item`, `purchase_order__status`  
**Search:** `item__name`, `item__sku`, `purchase_order__order_number`  
**Ordering:** `purchase_order`, `item`, `created_at`

---

## Sales API

### Sales Orders

- `GET /api/sales/orders/` - List all sales orders
- `POST /api/sales/orders/` - Create sales order (with items)
- `GET /api/sales/orders/{id}/` - Get sales order details
- `PUT /api/sales/orders/{id}/` - Update sales order
- `PATCH /api/sales/orders/{id}/` - Partial update
- `DELETE /api/sales/orders/{id}/` - Delete sales order
- `POST /api/sales/orders/{id}/mark_shipped/` - Mark as shipped
- `POST /api/sales/orders/{id}/mark_delivered/` - Mark as delivered
- `POST /api/sales/orders/{id}/cancel/` - Cancel order
- `POST /api/sales/orders/{id}/recalculate_total/` - Recalculate total

**Filters:** `status`, `client`, `warehouse`, `order_date`  
**Search:** `order_number`, `client__name`, `notes`  
**Ordering:** `order_date`, `created_at`, `total_amount`

### Sales Items

- `GET /api/sales/items/` - List all sales items
- `POST /api/sales/items/` - Create sales item
- `GET /api/sales/items/{id}/` - Get sales item details
- `PUT /api/sales/items/{id}/` - Update sales item
- `PATCH /api/sales/items/{id}/` - Partial update
- `DELETE /api/sales/items/{id}/` - Delete sales item

**Filters:** `sales_order`, `item`, `sales_order__status`  
**Search:** `item__name`, `item__sku`, `sales_order__order_number`  
**Ordering:** `sales_order`, `item`, `created_at`

---

## Accounts API

### Payments

- `GET /api/accounts/payments/` - List all payments
- `POST /api/accounts/payments/` - Create payment
- `GET /api/accounts/payments/{id}/` - Get payment details
- `PUT /api/accounts/payments/{id}/` - Update payment
- `PATCH /api/accounts/payments/{id}/` - Partial update
- `DELETE /api/accounts/payments/{id}/` - Delete payment
- `POST /api/accounts/payments/{id}/reconcile/` - Mark as reconciled

**Filters:** `payment_type`, `payment_method`, `vendor`, `client`, `date`, `is_reconciled`  
**Search:** `description`, `reference_number`, `vendor__name`, `client__name`  
**Ordering:** `date`, `created_at`, `amount`

### Ledger Entries

- `GET /api/accounts/ledger/` - List all ledger entries
- `GET /api/accounts/ledger/{id}/` - Get ledger entry details
- `GET /api/accounts/ledger/summary/` - Get ledger summary

**Ledger Summary Parameters:**
- `start_date` - Start date (YYYY-MM-DD)
- `end_date` - End date (YYYY-MM-DD, default: today)

**Filters:** `entry_type`, `reference_type`, `date`  
**Search:** `description`  
**Ordering:** `date`, `created_at`

### Profit/Loss

- `GET /api/accounts/profit-loss/` - List all P&L reports
- `GET /api/accounts/profit-loss/{id}/` - Get P&L report details
- `POST /api/accounts/profit-loss/calculate/` - Calculate P&L (without saving)
- `POST /api/accounts/profit-loss/create_report/` - Create and save P&L report

**Calculate/Create Report Parameters:**
- `start_date` - Start date (YYYY-MM-DD, required)
- `end_date` - End date (YYYY-MM-DD, default: today)

**Filters:** `period_start`, `period_end`  
**Ordering:** `period_end`

---

## Example Requests

### Create Purchase Order with Items

```http
POST /api/purchases/orders/
Content-Type: application/json
Authorization: Bearer <token>

{
  "vendor": 1,
  "order_number": "PO-2024-001",
  "order_date": "2024-01-15",
  "status": "PENDING",
  "purchase_items": [
    {
      "item": 1,
      "quantity": 100,
      "unit_cost": 50.00,
      "freight_cost": 500.00,
      "customs_duty": 200.00
    }
  ]
}
```

### Create Sales Order with Items

```http
POST /api/sales/orders/
Content-Type: application/json
Authorization: Bearer <token>

{
  "client": 1,
  "order_number": "SO-2024-001",
  "order_date": "2024-01-15",
  "status": "PENDING",
  "warehouse": 1,
  "sales_items": [
    {
      "item": 1,
      "quantity": 10,
      "unit_price": 75.00,
      "discount_percentage": 5.00
    }
  ]
}
```

### Create Payment

```http
POST /api/accounts/payments/
Content-Type: application/json
Authorization: Bearer <token>

{
  "client": 1,
  "amount": 5000.00,
  "payment_type": "CREDIT",
  "payment_method": "BANK_TRANSFER",
  "date": "2024-01-15",
  "description": "Payment for invoice #12345"
}
```

### Calculate Profit/Loss

```http
POST /api/accounts/profit-loss/calculate/
Content-Type: application/json
Authorization: Bearer <token>

{
  "start_date": "2024-01-01",
  "end_date": "2024-01-31"
}
```

---

## Response Format

All responses follow REST conventions:

### Success Response

```json
{
  "id": 1,
  "name": "Example",
  ...
}
```

### List Response (Paginated)

```json
{
  "count": 100,
  "next": "http://example.com/api/endpoint/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Example 1",
      ...
    },
    {
      "id": 2,
      "name": "Example 2",
      ...
    }
  ]
}
```

### Error Response

```json
{
  "field_name": ["Error message"],
  "non_field_errors": ["General error message"]
}
```

---

## Pagination

All list endpoints support pagination with default page size of 50 items.

**Query Parameters:**
- `page` - Page number
- `page_size` - Items per page (max 100)

---

## Filtering

Use query parameters for filtering:

```
GET /api/inventory/items/?is_active=true&category=1
```

---

## Search

Use `search` parameter for text search:

```
GET /api/inventory/items/?search=battery
```

---

## Ordering

Use `ordering` parameter:

```
GET /api/inventory/items/?ordering=-created_at,name
```

Negative prefix (`-`) for descending order.


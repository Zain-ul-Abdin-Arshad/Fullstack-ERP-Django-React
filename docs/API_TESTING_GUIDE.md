# API Testing Guide

Complete testing procedures for Django-React API integration.

## Prerequisites

1. Backend running on `http://localhost:8000`
2. Frontend running on `http://localhost:3000`
3. Django superuser created
4. Sample data created (optional)

## Testing Tools

### Browser DevTools
- Network tab for API calls
- Console for JavaScript testing
- Application tab for localStorage inspection

### Postman/Insomnia (Optional)
- Test APIs independently
- Verify backend endpoints

## Step-by-Step Testing

### Phase 1: Authentication Testing

#### Test 1.1: Login

**Browser Console:**
```javascript
// Test login
fetch('http://localhost:8000/api/token/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'admin',
    password: 'your_password'
  })
})
.then(r => r.json())
.then(data => {
  console.log('Tokens:', data);
  localStorage.setItem('access_token', data.access);
  localStorage.setItem('refresh_token', data.refresh);
});
```

**Expected:** Tokens received and stored

#### Test 1.2: Protected Route Access

**Browser Console:**
```javascript
// Test API call with token
fetch('http://localhost:8000/api/inventory/items/', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
})
.then(r => r.json())
.then(data => console.log('Items:', data));
```

**Expected:** Items list returned

#### Test 1.3: Token Refresh

**Browser Console:**
```javascript
// Test token refresh
fetch('http://localhost:8000/api/token/refresh/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    refresh: localStorage.getItem('refresh_token')
  })
})
.then(r => r.json())
.then(data => {
  console.log('New token:', data.access);
  localStorage.setItem('access_token', data.access);
});
```

**Expected:** New access token received

---

### Phase 2: Inventory Module Testing

#### Test 2.1: Get Items

**React Component Test:**
```javascript
import { inventoryService } from '../services/modules/inventory';

useEffect(() => {
  const test = async () => {
    try {
      const response = await inventoryService.getItems();
      console.log('Items:', response.data);
      // Should see paginated results
    } catch (error) {
      console.error('Error:', error.response?.data);
    }
  };
  test();
}, []);
```

**Expected Response:**
```json
{
  "count": 50,
  "results": [...],
  "next": null,
  "previous": null
}
```

#### Test 2.2: Create Item

**Test in Browser Console:**
```javascript
const createItem = async () => {
  const token = localStorage.getItem('access_token');
  const response = await fetch('http://localhost:8000/api/inventory/items/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name: "Test Battery",
      sku: "TEST-001",
      category: 1,
      cost_price: "50.00",
      selling_price: "75.00",
      unit: "PCS"
    })
  });
  const data = await response.json();
  console.log('Created:', data);
};
createItem();
```

**Expected:** Item created with ID

#### Test 2.3: Get Stock

**Test:**
```javascript
const getStock = async () => {
  const token = localStorage.getItem('access_token');
  const response = await fetch('http://localhost:8000/api/inventory/stock/?warehouse=1', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  const data = await response.json();
  console.log('Stock:', data);
};
getStock();
```

**Expected:** Stock entries for warehouse 1

---

### Phase 3: Purchase Module Testing

#### Test 3.1: Create Purchase Order

**Test:**
```javascript
const createPO = async () => {
  const token = localStorage.getItem('access_token');
  const response = await fetch('http://localhost:8000/api/purchases/orders/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      vendor: 1,
      order_number: "PO-TEST-001",
      order_date: "2024-01-15",
      status: "PENDING",
      purchase_items: [{
        item: 1,
        quantity: 50,
        unit_cost: "50.00",
        freight_cost: "500.00",
        customs_duty: "200.00",
        received_quantity: 0
      }]
    })
  });
  const data = await response.json();
  console.log('PO Created:', data);
  return data.id;
};
const poId = await createPO();
```

**Expected:** Purchase order created with calculated totals

#### Test 3.2: Mark as Received (Stock Increase)

**Test:**
```javascript
// First update received_quantity
const updateItem = async (itemId) => {
  const token = localStorage.getItem('access_token');
  await fetch(`http://localhost:8000/api/purchases/items/${itemId}/`, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ received_quantity: 50 })
  });
};

// Then mark order as received
const markReceived = async (poId) => {
  const token = localStorage.getItem('access_token');
  const response = await fetch(`http://localhost:8000/api/purchases/orders/${poId}/mark_received/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  const data = await response.json();
  console.log('Order received:', data);
  
  // Check stock increased
  const stockResponse = await fetch('http://localhost:8000/api/inventory/stock/?item=1', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  const stock = await stockResponse.json();
  console.log('Stock after purchase:', stock);
};
markReceived(poId);
```

**Expected:**
- Order status changed to "RECEIVED"
- Stock quantity increased by 50
- Average cost updated

---

### Phase 4: Sales Module Testing

#### Test 4.1: Create Sales Order (Stock Validation)

**Test:**
```javascript
const createSO = async () => {
  const token = localStorage.getItem('access_token');
  
  // Check stock first
  const stockCheck = await fetch('http://localhost:8000/api/inventory/stock/?item=1&warehouse=1', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  const stock = await stockCheck.json();
  console.log('Available stock:', stock.results[0]?.available_quantity);
  
  // Create order
  const response = await fetch('http://localhost:8000/api/sales/orders/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
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
    })
  });
  
  if (response.ok) {
    const data = await response.json();
    console.log('SO Created:', data);
    return data.id;
  } else {
    const error = await response.json();
    console.error('Error:', error);
    // Should show stock validation error if insufficient
  }
};
const soId = await createSO();
```

**Expected:**
- Order created if stock available
- Error if insufficient stock

#### Test 4.2: Mark as Shipped (Stock Decrease)

**Test:**
```javascript
const markShipped = async (soId) => {
  const token = localStorage.getItem('access_token');
  
  // Get stock before
  const stockBefore = await fetch('http://localhost:8000/api/inventory/stock/?item=1&warehouse=1', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  const before = await stockBefore.json();
  console.log('Stock before:', before.results[0]?.quantity);
  
  // Mark as shipped
  const response = await fetch(`http://localhost:8000/api/sales/orders/${soId}/mark_shipped/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  const data = await response.json();
  console.log('Order shipped:', data);
  
  // Check stock after
  const stockAfter = await fetch('http://localhost:8000/api/inventory/stock/?item=1&warehouse=1', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  const after = await stockAfter.json();
  console.log('Stock after:', after.results[0]?.quantity);
  console.log('Difference:', before.results[0]?.quantity - after.results[0]?.quantity);
};
markShipped(soId);
```

**Expected:**
- Order status changed to "SHIPPED"
- Stock quantity decreased by order quantity
- Reserved quantity decreased

---

### Phase 5: Dashboard Testing

#### Test 5.1: Load Dashboard Data

**Test in Dashboard Component:**
```javascript
useEffect(() => {
  const loadDashboard = async () => {
    try {
      // Load all dashboard data
      const [items, sales, purchases, p_l] = await Promise.all([
        inventoryService.getItems(),
        salesService.getSalesOrders(),
        purchasesService.getPurchaseOrders(),
        accountsService.calculateProfitLoss({
          start_date: '2024-01-01',
          end_date: '2024-01-31'
        })
      ]);
      
      console.log('Dashboard data loaded:', {
        items: items.data,
        sales: sales.data,
        purchases: purchases.data,
        profitLoss: p_l.data
      });
    } catch (error) {
      console.error('Dashboard error:', error);
    }
  };
  loadDashboard();
}, []);
```

**Expected:** All data loaded successfully

---

## Integration Test Scenarios

### Scenario 1: Complete Purchase Flow

```javascript
// 1. Create purchase order
const po = await purchasesService.createPurchaseOrder({
  vendor: 1,
  order_number: "PO-FLOW-001",
  order_date: "2024-01-15",
  status: "PENDING",
  purchase_items: [{
    item: 1,
    quantity: 100,
    unit_cost: "50.00",
    freight_cost: "500.00",
    customs_duty: "200.00",
    received_quantity: 100
  }]
});

// 2. Mark as received
await purchasesService.markReceived(po.data.id);

// 3. Verify stock increased
const stock = await inventoryService.getStock({ item: 1 });
console.log('Stock after purchase:', stock.data[0].quantity);
// Should be 100 more than before
```

### Scenario 2: Complete Sales Flow

```javascript
// 1. Check available stock
const stockBefore = await inventoryService.getStock({ item: 1, warehouse: 1 });
const available = stockBefore.data[0].available_quantity;

// 2. Create sales order (less than available)
const so = await salesService.createSalesOrder({
  client: 1,
  order_number: "SO-FLOW-001",
  order_date: "2024-01-15",
  warehouse: 1,
  status: "PENDING",
  sales_items: [{
    item: 1,
    quantity: Math.min(10, available),
    unit_price: "75.00"
  }]
});

// 3. Verify stock reserved
const stockReserved = await inventoryService.getStock({ item: 1, warehouse: 1 });
console.log('Reserved:', stockReserved.data[0].reserved_quantity);

// 4. Mark as shipped
await salesService.markShipped(so.data.id);

// 5. Verify stock decreased
const stockAfter = await inventoryService.getStock({ item: 1, warehouse: 1 });
console.log('Stock after sale:', stockAfter.data[0].quantity);
```

### Scenario 3: Stock Validation

```javascript
// Try to create order with more than available stock
try {
  await salesService.createSalesOrder({
    client: 1,
    order_number: "SO-INVALID-001",
    order_date: "2024-01-15",
    warehouse: 1,
    status: "PENDING",
    sales_items: [{
      item: 1,
      quantity: 100000,  // More than available
      unit_price: "75.00"
    }]
  });
} catch (error) {
  console.log('Expected error:', error.response?.data.detail);
  // Should show insufficient stock error
}
```

---

## Network Tab Inspection

### Check Request Headers

In Browser DevTools → Network tab:
1. Select any API request
2. Check "Headers" tab
3. Verify `Authorization: Bearer <token>` present
4. Verify `Content-Type: application/json`

### Check Response

1. Select API request
2. Check "Response" tab
3. Verify JSON structure matches expected format
4. Check status code (200, 201, 400, 401, etc.)

### Check Request Payload

1. Select POST/PUT request
2. Check "Payload" tab
3. Verify data matches API requirements

---

## Error Testing

### Test 401 Unauthorized

```javascript
// Remove token
localStorage.removeItem('access_token');

// Try API call
try {
  await inventoryService.getItems();
} catch (error) {
  console.log('Expected 401:', error.response?.status);
  // Should be 401
}
```

### Test 400 Bad Request

```javascript
// Send invalid data
try {
  await inventoryService.createItem({
    name: "",  // Empty name (invalid)
    sku: "TEST"
  });
} catch (error) {
  console.log('Validation errors:', error.response?.data);
  // Should show field errors
}
```

### Test 404 Not Found

```javascript
// Try to get non-existent item
try {
  await inventoryService.getItem(99999);
} catch (error) {
  console.log('404 error:', error.response?.status);
  // Should be 404
}
```

---

## Performance Testing

### Test Large Lists

```javascript
// Test pagination
const loadAllItems = async () => {
  let page = 1;
  let allItems = [];
  
  while (true) {
    const response = await inventoryService.getItems({ page });
    allItems = [...allItems, ...response.data.results];
    
    if (!response.data.next) break;
    page++;
  }
  
  console.log(`Loaded ${allItems.length} items`);
};
```

### Test Concurrent Requests

```javascript
// Test multiple simultaneous requests
const testConcurrent = async () => {
  const start = Date.now();
  
  await Promise.all([
    inventoryService.getItems(),
    vendorsService.getVendors(),
    clientsService.getClients(),
    salesService.getSalesOrders(),
    purchasesService.getPurchaseOrders()
  ]);
  
  const duration = Date.now() - start;
  console.log(`Concurrent requests completed in ${duration}ms`);
};
```

---

## Checklist

### Authentication
- [ ] Login works
- [ ] Tokens stored correctly
- [ ] Token refresh works
- [ ] Logout clears tokens
- [ ] Protected routes require auth

### Inventory
- [ ] Get items works
- [ ] Create item works
- [ ] Update item works
- [ ] Delete item works
- [ ] Get stock works
- [ ] Filter by warehouse works

### Vendors
- [ ] Get vendors works
- [ ] Create vendor works
- [ ] Update vendor works
- [ ] Delete vendor works

### Clients
- [ ] Get clients works
- [ ] Create client works
- [ ] Update client works
- [ ] Delete client works

### Purchases
- [ ] Create purchase order works
- [ ] Add items works
- [ ] Mark received works
- [ ] Stock increases automatically

### Sales
- [ ] Create sales order works
- [ ] Stock validation works
- [ ] Insufficient stock error shown
- [ ] Mark shipped works
- [ ] Stock decreases automatically

### Dashboard
- [ ] All charts load
- [ ] Data displays correctly
- [ ] No errors in console

---

## Debugging Tips

1. **Check Network Tab**: See actual requests/responses
2. **Check Console**: JavaScript errors
3. **Check Django Logs**: Backend errors
4. **Check localStorage**: Token storage
5. **Test with Postman**: Isolate frontend/backend issues

---

## Common Test Cases

### Test Case 1: Purchase → Stock Increase
1. Note current stock
2. Create purchase order
3. Mark as received
4. Verify stock increased
5. Verify average cost updated

### Test Case 2: Sales → Stock Decrease
1. Note current stock
2. Create sales order
3. Mark as shipped
4. Verify stock decreased
5. Verify reserved quantity decreased

### Test Case 3: Insufficient Stock
1. Note available stock
2. Try to create order with more than available
3. Verify error shown
4. Verify order not created

### Test Case 4: Token Expiry
1. Wait for token expiry (or manually expire)
2. Make API call
3. Verify token refreshed automatically
4. Verify request succeeds

---

**All tests should pass before deploying to production!**


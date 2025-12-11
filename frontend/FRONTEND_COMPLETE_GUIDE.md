# Complete React Frontend Guide

Complete React frontend implementation for ERP System with all modules, components, and pages.

## Project Structure

```
frontend/
├── public/
├── src/
│   ├── components/
│   │   ├── common/          # Reusable components
│   │   │   ├── Button.jsx
│   │   │   ├── Input.jsx
│   │   │   ├── Modal.jsx
│   │   │   ├── Loading.jsx
│   │   │   └── Alert.jsx
│   │   └── layout/          # Layout components
│   │       ├── Layout.jsx
│   │       ├── Sidebar.jsx
│   │       └── Header.jsx
│   ├── pages/
│   │   ├── Login.jsx
│   │   ├── inventory/       # Inventory module
│   │   │   ├── InventoryPage.jsx
│   │   │   ├── ItemsList.jsx
│   │   │   ├── ItemForm.jsx
│   │   │   └── StockView.jsx
│   │   ├── vendors/         # Vendors module
│   │   │   ├── VendorsPage.jsx
│   │   │   └── VendorForm.jsx
│   │   ├── clients/         # Clients module
│   │   │   ├── ClientsPage.jsx
│   │   │   └── ClientForm.jsx
│   │   ├── purchases/       # Purchases module
│   │   │   ├── PurchaseOrdersPage.jsx
│   │   │   └── PurchaseOrderForm.jsx
│   │   ├── sales/           # Sales module
│   │   │   ├── SalesOrdersPage.jsx
│   │   │   └── SalesOrderForm.jsx
│   │   └── dashboard/       # Dashboard
│   │       ├── DashboardPage.jsx
│   │       ├── InventoryOverview.jsx
│   │       ├── SalesOverview.jsx
│   │       ├── PurchasesOverview.jsx
│   │       └── FinancialOverview.jsx
│   ├── services/            # API services
│   │   ├── api.js           # Axios instance with JWT
│   │   ├── auth.js          # Auth service
│   │   └── modules/         # Module-specific APIs
│   │       ├── inventory.js
│   │       ├── vendors.js
│   │       ├── clients.js
│   │       ├── purchases.js
│   │       ├── sales.js
│   │       └── accounts.js
│   ├── context/
│   │   └── AuthContext.jsx  # Auth context
│   ├── utils/
│   │   └── helpers.js       # Helper functions
│   ├── App.jsx              # Main app with routing
│   ├── index.jsx            # Entry point
│   └── index.css            # Tailwind CSS
├── package.json
└── tailwind.config.js
```

## Setup Instructions

### Step 1: Install Dependencies

```powershell
cd D:\ERP_SYSTEM\frontend
npm install
```

### Step 2: Configure Tailwind CSS

Ensure `tailwind.config.js` includes:

```javascript
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          // ... add all primary colors
          600: '#2563eb',
          700: '#1d4ed8',
        },
      },
    },
  },
  plugins: [],
}
```

### Step 3: Start Development Server

```powershell
npm start
```

App runs at `http://localhost:3000`

## Features Implemented

### ✅ Authentication
- JWT token-based authentication
- Automatic token refresh
- Protected routes
- Login page

### ✅ Inventory Module
- List all items with search
- Add/Edit/Delete items
- View stock per warehouse
- Low stock indicators
- Stock filtering by warehouse

### ✅ Vendors Module
- CRUD operations
- Search functionality
- Status management

### ✅ Clients Module
- CRUD operations
- Search functionality
- Client type management

### ✅ Purchases Module
- Create purchase orders
- Add multiple items
- Mark as received (auto-updates stock)
- Landed cost calculation display

### ✅ Sales Module
- Create sales orders
- Add multiple items
- Stock validation before creation
- Stock alerts for insufficient stock
- Mark as shipped/delivered (auto-reduces stock)
- Cancel orders (releases stock)

### ✅ Dashboard
- Inventory overview with charts
- Sales overview with status breakdown
- Purchases overview
- Financial overview (Profit/Loss)
- All charts using Recharts
- Responsive design

## API Integration

All components use Axios with:
- Automatic JWT token injection
- Token refresh on 401 errors
- Error handling
- Loading states

## Stock Management

### Purchase Orders
- When order marked as "Received", stock automatically increases
- Average cost updated (weighted average)
- Low stock alerts triggered

### Sales Orders
- Stock validated before order creation
- Alerts shown if insufficient stock
- When order marked as "Shipped" or "Delivered", stock automatically decreases
- Reserved stock released on cancellation

## Responsive Design

All pages are responsive using Tailwind CSS:
- Mobile-friendly layouts
- Responsive tables
- Adaptive grid systems
- Touch-friendly buttons

## Next Steps

1. Test all API endpoints
2. Add form validation
3. Add pagination for large lists
4. Add export functionality
5. Add print functionality
6. Add advanced filtering
7. Add user management
8. Add notifications system

## Troubleshooting

### CORS Issues
Ensure backend has CORS configured:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

### API Connection Issues
Check:
1. Backend server is running on port 8000
2. API base URL in `services/api.js`
3. CORS settings in Django

### Build Issues
```powershell
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```


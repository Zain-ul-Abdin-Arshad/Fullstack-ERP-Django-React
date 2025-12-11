# React Frontend - Quick Start Guide

## Installation

```powershell
cd D:\ERP_SYSTEM\frontend
npm install
npm start
```

## Available Pages

- `/login` - Login page
- `/dashboard` - Main dashboard with charts
- `/inventory` - Inventory management (Items & Stock)
- `/vendors` - Vendor management
- `/clients` - Client management
- `/purchases` - Purchase orders
- `/sales` - Sales orders
- `/accounts` - Accounts (to be implemented)

## Key Features

### Stock Management
- ✅ Auto-increase on purchase receipt
- ✅ Auto-decrease on sales shipment
- ✅ Stock validation before sales
- ✅ Low stock alerts

### Dashboard
- ✅ Inventory overview charts
- ✅ Sales overview charts
- ✅ Purchases overview charts
- ✅ Financial overview charts

## API Configuration

Backend API: `http://localhost:8000/api`

Update in `src/services/api.js` if different.

## Authentication

Default login uses Django superuser credentials created via:
```powershell
python manage.py createsuperuser
```

## Troubleshooting

**CORS Errors:**
- Ensure backend CORS settings allow `http://localhost:3000`

**API Connection:**
- Verify backend is running on port 8000
- Check API base URL in `services/api.js`

**Build Errors:**
```powershell
rm -rf node_modules
npm install
```


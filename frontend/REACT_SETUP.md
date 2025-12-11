# React Frontend Setup Guide

Complete guide to set up React frontend for ERP System with Tailwind CSS, Axios, Recharts, and JWT authentication.

## Prerequisites

- Node.js 16+ installed
- npm or yarn package manager
- Backend API running on http://localhost:8000

## Step 1: Create React Project

```powershell
# Navigate to frontend directory
cd D:\ERP_SYSTEM\frontend

# Create React app with Vite (recommended) or Create React App
npm create vite@latest . -- --template react

# Or using Create React App
# npx create-react-app .

# Install dependencies
npm install
```

## Step 2: Install Required Packages

```powershell
# Core dependencies
npm install axios react-router-dom

# UI and styling
npm install -D tailwindcss postcss autoprefixer
npm install @headlessui/react @heroicons/react

# Charts
npm install recharts

# Form handling
npm install react-hook-form

# Date handling
npm install date-fns

# Notifications
npm install react-hot-toast
```

## Step 3: Initialize Tailwind CSS

```powershell
# Initialize Tailwind
npx tailwindcss init -p
```

This creates `tailwind.config.js` and `postcss.config.js`

## Step 4: Configure Tailwind CSS

Update `tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
      },
    },
  },
  plugins: [],
}
```

## Step 5: Add Tailwind to CSS

Create/update `src/index.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-gray-50 text-gray-900;
  }
}

@layer components {
  .btn-primary {
    @apply bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2;
  }
  
  .btn-secondary {
    @apply bg-gray-200 text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2;
  }
  
  .input-field {
    @apply w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent;
  }
  
  .card {
    @apply bg-white rounded-lg shadow-md p-6;
  }
}
```

## Step 6: Project Structure

```
frontend/
├── public/
├── src/
│   ├── components/          # Reusable components
│   │   ├── common/         # Common components (Button, Input, etc.)
│   │   ├── layout/         # Layout components (Header, Sidebar, etc.)
│   │   └── charts/         # Chart components
│   ├── pages/              # Page components
│   │   ├── inventory/      # Inventory pages
│   │   ├── vendors/        # Vendor pages
│   │   ├── clients/        # Client pages
│   │   ├── purchases/      # Purchase pages
│   │   ├── sales/          # Sales pages
│   │   └── dashboard/      # Dashboard pages
│   ├── services/           # API services
│   │   ├── api.js          # Axios instance
│   │   ├── auth.js         # Auth service
│   │   ├── inventory.js    # Inventory API
│   │   ├── vendors.js      # Vendors API
│   │   ├── clients.js      # Clients API
│   │   ├── purchases.js    # Purchases API
│   │   └── sales.js        # Sales API
│   ├── utils/              # Utility functions
│   │   ├── auth.js         # Auth utilities
│   │   └── helpers.js      # Helper functions
│   ├── context/            # React Context
│   │   └── AuthContext.jsx # Auth context
│   ├── App.jsx             # Main App component
│   ├── index.jsx           # Entry point
│   └── index.css           # Global styles
├── package.json
├── tailwind.config.js
└── vite.config.js (or similar)
```

## Step 7: Environment Variables

Create `.env` file:

```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_API_TOKEN_URL=http://localhost:8000/api/token
```

## Step 8: Update package.json Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

## Step 9: Start Development Server

```powershell
npm run dev
```

The app will be available at `http://localhost:5173` (Vite) or `http://localhost:3000` (CRA)

## Next Steps

1. Set up API services (see services/api.js)
2. Configure JWT authentication (see services/auth.js)
3. Create components and pages
4. Set up routing

See individual component files for implementation details.


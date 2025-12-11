# ERP Frontend - React Application

Complete React frontend for the ERP System with Tailwind CSS, Axios, and Recharts.

## Prerequisites

- Node.js 16+ and npm/yarn
- Backend API running at `http://localhost:8000`

## Setup Instructions

### Step 1: Create React Project

```bash
# Navigate to ERP_SYSTEM directory
cd D:\ERP_SYSTEM

# Create React app
npx create-react-app frontend --template

# Navigate to frontend
cd frontend
```

### Step 2: Install Dependencies

```bash
# Install required packages
npm install axios recharts
npm install -D tailwindcss postcss autoprefixer

# Initialize Tailwind CSS
npx tailwindcss init -p
```

### Step 3: Configure Tailwind CSS

Update `tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Update `src/index.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Step 4: Project Structure

```
frontend/
├── public/
├── src/
│   ├── components/        # Reusable components
│   │   ├── Layout/
│   │   ├── Common/
│   │   └── Forms/
│   ├── pages/            # Page components
│   │   ├── Dashboard/
│   │   ├── Inventory/
│   │   ├── Vendors/
│   │   ├── Clients/
│   │   ├── Purchases/
│   │   └── Sales/
│   ├── services/         # API services
│   │   ├── api.js
│   │   ├── auth.js
│   │   └── modules/
│   ├── utils/           # Utility functions
│   │   ├── auth.js
│   │   └── helpers.js
│   ├── context/         # React Context
│   │   └── AuthContext.jsx
│   ├── App.jsx
│   ├── index.jsx
│   └── index.css
├── package.json
└── tailwind.config.js
```

### Step 5: Start Development Server

```bash
npm start
```

The app will run at `http://localhost:3000`

## Features

✅ JWT Authentication  
✅ CRUD Operations for all modules  
✅ Real-time stock updates  
✅ Dashboard with charts (Recharts)  
✅ Responsive design (Tailwind CSS)  
✅ Stock validation and alerts  
✅ Low stock notifications  

## API Configuration

The frontend connects to the backend API at:
- Base URL: `http://localhost:8000/api`
- Authentication: JWT Bearer tokens


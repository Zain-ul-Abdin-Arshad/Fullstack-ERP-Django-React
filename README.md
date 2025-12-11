# ERP System - Car Spare Parts Management

A high-volume, multi-branch import/export car spare parts ERP system built with Django and Django REST Framework.

## Features

- **Multi-branch Management**: Manage inventory across multiple branches
- **Import/Export Operations**: Handle high-volume import and export transactions
- **Inventory Management**: Real-time inventory tracking and management
- **Supplier & Customer Management**: Complete CRM functionality
- **Order Management**: Process orders efficiently
- **Reporting & Analytics**: Comprehensive reporting system
- **JWT Authentication**: Secure API authentication
- **RESTful API**: Complete REST API for frontend integration

## Tech Stack

- **Backend**: Django 4+ with Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Python**: 3.10+

## Quick Start

1. **Follow the complete setup guide**: See [SETUP_GUIDE.md](SETUP_GUIDE.md)

2. **Quick setup (Windows PowerShell)**:
   ```powershell
   .\scripts\setup_windows.ps1
   ```

3. **Manual setup**:
   ```powershell
   cd backend
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

## Project Structure

```
ERP_SYSTEM/
├── backend/              # Django backend
├── frontend/             # Frontend application (to be added)
├── docs/                 # Documentation
├── scripts/              # Utility scripts
└── README.md
```

## Documentation

- [Setup Guide](SETUP_GUIDE.md) - Complete installation and configuration instructions

## Development

### Running the Development Server

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

### Creating Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

### Creating Superuser

```powershell
python manage.py createsuperuser
```

## API Endpoints

- Admin Panel: http://localhost:8000/admin/
- JWT Token: http://localhost:8000/api/token/
- JWT Refresh: http://localhost:8000/api/token/refresh/

## License

[Your License Here]

## Contributing

[Contributing Guidelines]


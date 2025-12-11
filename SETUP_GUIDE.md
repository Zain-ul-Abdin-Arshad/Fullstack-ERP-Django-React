# ERP System Setup Guide

Complete step-by-step instructions for setting up a Django-based ERP system for high-volume, multi-branch import/export car spare parts management.

## Prerequisites

- Windows 10/11
- Administrator access
- Internet connection

---

## Step 1: Install Python 3.10+

### Windows Installation

1. **Download Python 3.10+**
   - Visit: https://www.python.org/downloads/
   - Download Python 3.10 or higher (recommended: Python 3.11 or 3.12)
   - Run the installer

2. **During Installation:**
   - ✅ Check "Add Python to PATH"
   - ✅ Select "Install for all users" (if you have admin rights)
   - Click "Install Now"

3. **Verify Installation:**
   ```powershell
   python --version
   ```
   Expected output: `Python 3.10.x` or higher

4. **Verify pip is installed:**
   ```powershell
   pip --version
   ```

---

## Step 2: Install PostgreSQL

### Windows Installation

1. **Download PostgreSQL**
   - Visit: https://www.postgresql.org/download/windows/
   - Download PostgreSQL 14 or higher
   - Run the installer

2. **During Installation:**
   - Choose installation directory (default: `C:\Program Files\PostgreSQL\<version>`)
   - Set **PostgreSQL superuser (postgres) password** - **SAVE THIS PASSWORD**
   - Port: `5432` (default)
   - Locale: `Default locale`

3. **Verify Installation:**
   ```powershell
   psql --version
   ```

4. **Add PostgreSQL to PATH (if not automatically added):**
   - Add `C:\Program Files\PostgreSQL\<version>\bin` to System PATH
   - Restart PowerShell/terminal

---

## Step 3: Create Project Directory Structure

### Recommended Folder Structure

```
ERP_SYSTEM/
│
├── backend/                          # Django backend application
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env                         # Environment variables (DO NOT COMMIT)
│   │
│   ├── config/                      # Django project settings
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   ├── apps/                        # Django applications
│   │   ├── __init__.py
│   │   ├── accounts/                # User management
│   │   ├── inventory/               # Inventory management
│   │   ├── branches/                # Multi-branch management
│   │   ├── import_export/           # Import/Export operations
│   │   ├── suppliers/               # Supplier management
│   │   ├── customers/               # Customer management
│   │   ├── orders/                  # Order management
│   │   └── reports/                 # Reporting & analytics
│   │
│   ├── core/                        # Core utilities
│   │   ├── __init__.py
│   │   ├── permissions.py
│   │   ├── mixins.py
│   │   └── pagination.py
│   │
│   ├── static/                      # Static files
│   ├── media/                       # User uploaded files
│   ├── templates/                   # HTML templates (if needed)
│   │
│   └── tests/                       # Test files
│
├── frontend/                        # Frontend application (React/Vue/etc)
│
├── docs/                            # Documentation
│
├── scripts/                         # Utility scripts
│   ├── setup_db.sh
│   └── backup_db.sh
│
└── README.md
```

### Create Directory Structure

```powershell
# Navigate to workspace root
cd D:\ERP_SYSTEM

# Create main directories
mkdir backend, frontend, docs, scripts

# Create backend subdirectories
cd backend
mkdir apps, core, static, media, templates, tests
mkdir config

# Create app directories
cd apps
mkdir accounts, inventory, branches, import_export, suppliers, customers, orders, reports
```

---

## Step 4: Create Python Virtual Environment

### Create Virtual Environment

```powershell
# Navigate to backend directory
cd D:\ERP_SYSTEM\backend

# Create virtual environment named 'venv'
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get an execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Verify activation (you should see (venv) prefix)
python --version
```

### Deactivate Virtual Environment (when needed)
```powershell
deactivate
```

---

## Step 5: Install Django and Dependencies

### Create requirements.txt

Create `requirements.txt` in the `backend` directory with the following content:

```txt
Django>=4.2.0,<5.0.0
djangorestframework>=3.14.0
psycopg2-binary>=2.9.0
djangorestframework-simplejwt>=5.3.0
python-decouple>=3.8
django-cors-headers>=4.3.0
```

### Install Dependencies

```powershell
# Ensure virtual environment is activated
# (You should see (venv) in your prompt)

# Upgrade pip first
python -m pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# Verify installations
pip list
```

---

## Step 6: Create Django Project

### Initialize Django Project

```powershell
# Ensure you're in backend directory with venv activated
cd D:\ERP_SYSTEM\backend

# Create Django project (replace 'config' with your project name if different)
django-admin startproject config .

# Verify project creation
dir
# You should see: manage.py, config/ folder
```

### Create Django Apps

```powershell
# Create all required apps
python manage.py startapp accounts apps/accounts
python manage.py startapp inventory apps/inventory
python manage.py startapp branches apps/branches
python manage.py startapp import_export apps/import_export
python manage.py startapp suppliers apps/suppliers
python manage.py startapp customers apps/customers
python manage.py startapp orders apps/orders
python manage.py startapp reports apps/reports
```

---

## Step 7: Setup PostgreSQL Database

### Create Database

```powershell
# Connect to PostgreSQL (you'll be prompted for postgres user password)
psql -U postgres

# In PostgreSQL prompt, run:
CREATE DATABASE erp_db;

# Create a dedicated database user (recommended for production)
CREATE USER erp_user WITH PASSWORD 'your_secure_password_here';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE erp_db TO erp_user;

# Exit PostgreSQL
\q
```

### Alternative: Using pgAdmin

1. Open **pgAdmin 4** (installed with PostgreSQL)
2. Connect to PostgreSQL server
3. Right-click **Databases** → **Create** → **Database**
4. Name: `erp_db`
5. Owner: `postgres` (or create new user)
6. Click **Save**

---

## Step 8: Configure Django Settings

### Update settings.py

Edit `backend/config/settings.py` with the following configuration:

```python
"""
Django settings for ERP System project.
"""

from pathlib import Path
from decouple import config
from datetime import timedelta

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    
    # Local apps
    'apps.accounts',
    'apps.inventory',
    'apps.branches',
    'apps.import_export',
    'apps.suppliers',
    'apps.customers',
    'apps.orders',
    'apps.reports',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='erp_db'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
        'OPTIONS': {
            'connect_timeout': 10,
        },
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files (User uploads)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

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
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# CORS Settings (Configure for production)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
]

CORS_ALLOW_CREDENTIALS = True

# Security Settings (for production)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
```

### Create .env file

Create `backend/.env` file (DO NOT commit this to version control):

```env
# Django Settings
SECRET_KEY=your-secret-key-here-generate-a-random-string
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=erp_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password_here
DB_HOST=localhost
DB_PORT=5432
```

**Important:** Generate a secure SECRET_KEY:
```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Step 9: Install python-decouple

```powershell
# Ensure venv is activated
pip install python-decouple
```

---

## Step 10: Run Migrations

```powershell
# Ensure you're in backend directory with venv activated
cd D:\ERP_SYSTEM\backend

# Create initial migrations
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
# Follow prompts to create admin user
```

---

## Step 11: Configure URLs

### Update config/urls.py

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
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/inventory/', include('apps.inventory.urls')),
    path('api/branches/', include('apps.branches.urls')),
    path('api/import-export/', include('apps.import_export.urls')),
    path('api/suppliers/', include('apps.suppliers.urls')),
    path('api/customers/', include('apps.customers.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/reports/', include('apps.reports.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

---

## Step 12: Test the Setup

### Start Development Server

```powershell
# Ensure venv is activated and you're in backend directory
python manage.py runserver
```

### Verify Installation

1. **Open browser:** http://localhost:8000/admin/
2. **Login** with superuser credentials
3. **Check API:** http://localhost:8000/api/token/ (should show login form or API endpoint)

---

## Step 13: Create .gitignore

Create `backend/.gitignore`:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
/media
/staticfiles

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Testing
.coverage
htmlcov/
.pytest_cache/
```

---

## Verification Checklist

- [ ] Python 3.10+ installed and accessible
- [ ] PostgreSQL installed and running
- [ ] Virtual environment created and activated
- [ ] All dependencies installed
- [ ] Django project created
- [ ] All apps created
- [ ] Database `erp_db` created
- [ ] `.env` file configured with correct credentials
- [ ] `settings.py` configured correctly
- [ ] Migrations applied successfully
- [ ] Superuser created
- [ ] Development server runs without errors
- [ ] Admin panel accessible
- [ ] API endpoints accessible

---

## Next Steps

1. **Configure each app:**
   - Define models for each app
   - Create serializers
   - Create viewsets
   - Configure URLs

2. **Set up authentication:**
   - Customize user model if needed
   - Configure permissions
   - Set up role-based access control

3. **Database optimization:**
   - Add indexes for frequently queried fields
   - Configure database connection pooling
   - Set up database backups

4. **Production deployment:**
   - Use environment-specific settings
   - Configure proper security settings
   - Set up logging
   - Configure static file serving
   - Set up SSL/TLS

---

## Troubleshooting

### Common Issues

1. **psycopg2 installation fails:**
   ```powershell
   # Install PostgreSQL development headers or use pre-compiled binary
   pip install psycopg2-binary
   ```

2. **Database connection error:**
   - Verify PostgreSQL is running: `Get-Service postgresql*`
   - Check credentials in `.env`
   - Verify database exists: `psql -U postgres -l`

3. **Port already in use:**
   ```powershell
   # Use different port
   python manage.py runserver 8001
   ```

4. **Virtual environment activation fails:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

---

## Additional Resources

- Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- Simple JWT: https://django-rest-framework-simplejwt.readthedocs.io/

---

**Setup completed successfully!** 🎉


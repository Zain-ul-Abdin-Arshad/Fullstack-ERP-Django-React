# Quick Setup - Django Project & Apps

## All Commands in One Place

```powershell
# 1. Navigate to backend and activate venv
cd D:\ERP_SYSTEM\backend
.\venv\Scripts\Activate.ps1

# 2. Create Django project 'erp_core'
django-admin startproject erp_core .

# 3. Create all apps
python manage.py startapp inventory
python manage.py startapp vendors
python manage.py startapp clients
python manage.py startapp purchases
python manage.py startapp sales
python manage.py startapp accounts

# 4. Register apps in erp_core/settings.py
# Edit INSTALLED_APPS and add:
# 'accounts',
# 'inventory',
# 'vendors',
# 'clients',
# 'purchases',
# 'sales',

# 5. Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser (optional)
python manage.py createsuperuser

# 7. Run server
python manage.py runserver
```

## Or Use the Automated Script

```powershell
# From ERP_SYSTEM root directory
.\scripts\create_django_project.ps1
```

## settings.py Configuration

Add to `INSTALLED_APPS` in `erp_core/settings.py`:

```python
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
    'accounts',
    'inventory',
    'vendors',
    'clients',
    'purchases',
    'sales',
]
```

## Verify Setup

```powershell
# Check for errors
python manage.py check

# Show migrations
python manage.py showmigrations

# List all apps
python manage.py shell
>>> from django.apps import apps
>>> [app.name for app in apps.get_app_configs()]
```


# Quick Command Reference

## Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Deactivate virtual environment
deactivate
```

## Django Commands

### Project Creation

```powershell
# Create Django project (in current directory)
django-admin startproject erp_core .

# Create Django project (in subdirectory)
django-admin startproject erp_core
```

### App Creation

```powershell
# Create new Django app
python manage.py startapp app_name

# Create app in specific directory
python manage.py startapp app_name apps/app_name

# Create all ERP apps
python manage.py startapp inventory
python manage.py startapp vendors
python manage.py startapp clients
python manage.py startapp purchases
python manage.py startapp sales
python manage.py startapp accounts
```

### Migrations

```powershell
# Create migrations
python manage.py makemigrations

# Create migrations for specific app
python manage.py makemigrations app_name

# Apply migrations
python manage.py migrate

# Show migrations status
python manage.py showmigrations

# Show SQL for migrations
python manage.py sqlmigrate app_name migration_number
```

### Management

```powershell
# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Run development server on specific port
python manage.py runserver 8001

# Run development server on specific IP and port
python manage.py runserver 0.0.0.0:8000

# Collect static files
python manage.py collectstatic

# Django shell
python manage.py shell

# Check for errors
python manage.py check
```

## PostgreSQL Commands

```powershell
# Connect to PostgreSQL
psql -U postgres

# List all databases
psql -U postgres -l

# Create database
psql -U postgres -c "CREATE DATABASE erp_db;"

# Drop database (careful!)
psql -U postgres -c "DROP DATABASE erp_db;"

# Connect to specific database
psql -U postgres -d erp_db
```

## Inside PostgreSQL (psql prompt)

```sql
-- List all databases
\l

-- Connect to database
\c erp_db

-- List all tables
\dt

-- Describe table structure
\d table_name

-- Exit psql
\q
```

## Pip Commands

```powershell
# Install package
pip install package_name

# Install from requirements.txt
pip install -r requirements.txt

# List installed packages
pip list

# Show package info
pip show package_name

# Uninstall package
pip uninstall package_name

# Generate requirements.txt
pip freeze > requirements.txt
```

## Project Setup Commands (In Order)

```powershell
# 1. Navigate to backend
cd backend

# 2. Create and activate venv
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file (copy from SETUP_GUIDE.md)

# 5. Create database
psql -U postgres -c "CREATE DATABASE erp_db;"

# 6. Run migrations
python manage.py migrate

# 7. Create superuser
python manage.py createsuperuser

# 8. Run server
python manage.py runserver
```

## Git Commands

```powershell
# Initialize repository
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit"

# Check status
git status

# View .gitignore
cat .gitignore
```

## Troubleshooting Commands

```powershell
# Check Python version
python --version

# Check pip version
pip --version

# Check PostgreSQL version
psql --version

# Check if PostgreSQL service is running
Get-Service postgresql*

# Start PostgreSQL service
Start-Service postgresql-x64-14  # Replace with your version

# Check Django version
python -m django --version

# Generate Django secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

